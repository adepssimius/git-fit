#!/usr/bin/env python3
"""Was that a climb up a hill, and was it run or hiked? — two labels from the elevation
and cadence streams of a recorded session.

The motivating case: a session filed as TRAIL_RUNNING that was, by cadence, hiked to a summit.
The activity type on the watch says what sport was selected, not what the legs did, and the
distinction matters for reading the log — 190m of sustained climb at walking cadence is a
different training stimulus from the same gain accumulated over rolling trail at running cadence.

Two labels, deliberately independent (a summit can be run; flat trail can be walked):

  peak_ascent  — did the route climb one substantial hill?
  mode         — "hike" or "run", from cadence

  python3 scripts/classify_activity.py --workout-json workout.json
  cat workout.json | python3 scripts/classify_activity.py --workout-json -
  python3 scripts/classify_activity.py --workout-json a.json b.json --format json

`workout.json` is whatever `mcp__suuntool__workouts_get` returned — those responses are 2-4MB
and land in a file rather than inline, which is exactly the file to pass here.

DO NOT USE ASCENT PER KILOMETER FOR THIS. It is the intuitive metric and it is wrong: in the
validation set the activity with the *highest* ascent/km (70.8 m/km, 574m of gain) is the one
that is not a peak ascent — it accumulated that gain over rolling terrain. Ascent/km measures
how much climbing, not how it was arranged, and peak ascents are defined by the arrangement.
See rules/trail-classification.md, which also carries the assumptions and the failure modes.

PROTOTYPE. The thresholds were fitted to four hand-labeled New England activities, not learned,
and carry no validated error rate. `--explain` prints the margin against each gate so a call
that only just cleared one is visible as such.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# --- thresholds (fitted to N=4; see rules/trail-classification.md §"Assumptions") -------------
RELIEF_M_MIN = 120.0        # how big the hill has to be
CONCENTRATION_MIN = 0.60    # how much of the gain has to have arrived in one push
SMOOTH_HALFWIDTH_S = 15     # boxcar half-width, in SECONDS (the streams are 1Hz)
RUN_CADENCE_SPM = 140.0     # generic running cadence cut, not personalized
RUN_FRACTION_MIN = 0.50     # share of moving time above it to call the session a run
MOVING_SPEED_MS = 0.5       # below this the athlete was standing, not walking

# Suunto stores cadence in Hz PER FOOT. One foot at 1.04Hz is 62 steps/min for that foot and
# 124spm total, so the conversion is x120, not x60. Using x60 puts every activity under any
# running threshold and silently returns "hike" for everything.
CADENCE_HZ_TO_SPM = 120.0


# ---------------------------------------------------------------------------
# Workout parsing
# ---------------------------------------------------------------------------
def load_workout(spec: str) -> dict:
    raw = sys.stdin.read() if spec == "-" else Path(spec).read_text()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{spec}: not JSON: {exc}")
    if isinstance(data, dict) and "items" in data:      # a workouts_list response
        items = data["items"]
        if not items:
            raise SystemExit(f"{spec}: the workouts_list response has no items")
        data = items[0]
    return data


def stream(w: dict, kind: str) -> list[dict]:
    """Points of one *StreamExtension, as [{value, timestamp}, ...]."""
    for ext in w.get("extensions") or []:
        if ext.get("type") == f"{kind}StreamExtension":
            return [p for p in (ext.get("points") or [])
                    if p.get("value") is not None and p.get("timestamp") is not None]
    return []


def pause_windows(w: dict) -> list[tuple[int, int]]:
    for ext in w.get("extensions") or []:
        if ext.get("type") == "PauseMarkerExtension":
            return [(m["startTime"], m["endTime"]) for m in (ext.get("pauseMarkers") or [])
                    if m.get("startTime") is not None and m.get("endTime") is not None]
    return []


def paused(ts: int, windows: list[tuple[int, int]]) -> bool:
    return any(a <= ts <= b for a, b in windows)


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------
def smooth(points: list[dict], halfwidth_s: int = SMOOTH_HALFWIDTH_S) -> list[float]:
    """Boxcar mean over a +/-halfwidth_s window, by TIMESTAMP not by index.

    Smoothing is not optional. Raw barometric altitude carries several metres of
    sample-to-sample noise, and an unsmoothed max-min inflates relief directly. The window is
    specified in seconds rather than samples so that a stream recorded at anything other than
    1Hz keeps the same time constant.
    """
    ts = [p["timestamp"] / 1000.0 for p in points]
    val = [float(p["value"]) for p in points]
    out, lo, hi, run = [], 0, 0, 0.0
    for i, t in enumerate(ts):
        while ts[lo] < t - halfwidth_s:
            run -= val[lo]
            lo += 1
        while hi < len(ts) and ts[hi] <= t + halfwidth_s:
            run += val[hi]
            hi += 1
        out.append(run / (hi - lo))
    return out


def elevation_metrics(w: dict) -> dict | None:
    pts = stream(w, "Altitude")
    if len(pts) < 2 * SMOOTH_HALFWIDTH_S:
        return None
    sm = smooth(pts)
    relief = max(sm) - min(sm)
    ascent = w.get("totalAscent")
    # `total_ascent` is Suunto's own figure while relief is computed here, so the ratio's
    # numerator and denominator come from different pipelines. That inconsistency is real and
    # deliberate: the thresholds were fitted against Suunto's ascent, and recomputing ascent
    # from the smoothed stream would need them refitted. rules/trail-classification.md §5.3.
    concentration = relief / ascent if ascent else None
    return {
        "relief_m": relief,
        "total_ascent_m": ascent,
        "concentration": concentration,
        # Where the high point sits in the session. Near 0.0 means the track started at the top
        # and descended — high relief and high concentration, but no climb. Reported, not gated.
        "peak_position": sm.index(max(sm)) / (len(sm) - 1),
        "samples": len(pts),
    }


def cadence_metrics(w: dict) -> dict | None:
    cad = stream(w, "Cadence")
    if not cad:
        return None
    windows = pause_windows(w)
    speed = {p["timestamp"]: float(p["value"]) for p in stream(w, "Speed")}
    moving = running = 0
    for p in cad:
        ts = p["timestamp"]
        if paused(ts, windows):
            continue
        # No speed sample for this second: keep it, on the assumption of motion. Dropping it
        # would bias run_fraction by whichever direction the gaps happen to fall in.
        if speed.get(ts, MOVING_SPEED_MS) < MOVING_SPEED_MS:
            continue
        moving += 1
        if float(p["value"]) * CADENCE_HZ_TO_SPM >= RUN_CADENCE_SPM:
            running += 1
    if not moving:
        return None
    return {"run_fraction": running / moving, "moving_samples": moving}


def classify(w: dict) -> dict:
    out = {
        "key": w.get("key"),
        "activity_name": w.get("activityName"),
        "distance_km": (w.get("totalDistance") or 0) / 1000.0,
        "duration_min": (w.get("totalTime") or 0) / 60.0,
    }
    elev = elevation_metrics(w)
    cad = cadence_metrics(w)
    out.update(elev or {"relief_m": None, "concentration": None})
    out.update(cad or {"run_fraction": None})

    if elev is None or elev["concentration"] is None:
        # No altitude stream means indoor or no-GPS: there is no terrain to describe, and a
        # False here would read as "flat outdoor route" rather than "not applicable".
        out["peak_ascent"] = None
    else:
        out["peak_ascent"] = (elev["relief_m"] >= RELIEF_M_MIN
                              and elev["concentration"] >= CONCENTRATION_MIN)
    out["mode"] = None if cad is None else ("run" if cad["run_fraction"] >= RUN_FRACTION_MIN
                                            else "hike")
    return out


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------
def fmt(v, spec: str, dash: str = "  n/a") -> str:
    return dash if v is None else format(v, spec)


def report(r: dict, explain: bool) -> None:
    name = r["key"] or "?"
    print(f"{name}  {r['activity_name'] or '?'}  "
          f"{r['distance_km']:.1f}km  {r['duration_min']:.0f}min")
    print(f"  relief         {fmt(r['relief_m'], '6.0f')} m"
          f"    (gate: >= {RELIEF_M_MIN:.0f} m — how big the hill was)")
    print(f"  concentration  {fmt(r['concentration'], '6.2f')}"
          f"      (gate: >= {CONCENTRATION_MIN:.2f} — how much came in one push)")
    print(f"  run_fraction   {fmt(r['run_fraction'], '6.0%')}"
          f"      (gate: >= {RUN_FRACTION_MIN:.0%} of moving time >= {RUN_CADENCE_SPM:.0f}spm)")
    peak = {True: "peak ascent", False: "not a peak ascent", None: "peak: unknown"}[r["peak_ascent"]]
    print(f"  -> {peak}, {r['mode'] or 'mode unknown'}")

    if explain:
        if r["relief_m"] is not None:
            print(f"     ascent/km   {r['total_ascent_m'] / max(r['distance_km'], 1e-9):5.1f} m/km"
                  f"  — NOT used; misorders this set at both ends (§2)")
            print(f"     high point at {r['peak_position']:.0%} of the track"
                  + ("  — early: check this was not a net descent (failure mode 6.1)"
                     if r["peak_position"] < 0.15 else ""))
            near = min(abs(r["relief_m"] - RELIEF_M_MIN) / RELIEF_M_MIN,
                       abs(r["concentration"] - CONCENTRATION_MIN) / CONCENTRATION_MIN)
            if near < 0.15:
                print("     WARNING: within 15% of a gate. The thresholds were fitted to four"
                      " activities — a call this close is a coin flip, not a measurement.")
        if r["run_fraction"] is not None and abs(r["run_fraction"] - RUN_FRACTION_MIN) < 0.10:
            print("     WARNING: run_fraction is near the cut, and that cut is the"
                  " least-validated number in the method (assumption 8).")


def main() -> int:
    p = argparse.ArgumentParser(
        description=__doc__.split("\n\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--workout-json", metavar="PATH", nargs="+", required=True,
                   help="workouts_get JSON (or `-` for stdin); repeatable")
    p.add_argument("--explain", action="store_true",
                   help="show the margin against each gate, and the ascent/km that §2 rejects")
    p.add_argument("--format", choices=("text", "json"), default="text")
    args = p.parse_args()

    results = [classify(load_workout(spec)) for spec in args.workout_json]
    if args.format == "json":
        print(json.dumps(results, indent=2))
        return 0
    for i, r in enumerate(results):
        if i:
            print()
        report(r, args.explain)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
