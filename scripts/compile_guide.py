#!/usr/bin/env python3
"""Compile an endurance/*.md session into SuuntoPlus `guide.json` wire format.

The repo stores sessions as intervals.icu workout text (rules/endurance-authoring.md).
The watch wants a tree of `fields`/`repeat` steps with absolute units. Nothing in the
publishing path does that conversion: suuntool is byte-transparent and never opens an
archive, so this script is the compiler.

Doing this by hand per session is how the `m`-means-minutes class of error comes back one
layer below where verify_plan.py can see it — that check reads the markdown, not the wire
format, and a correct file can still compile to a wrong guide.

Wire-format facts this encodes (all of them silent corruptions if wrong):
  * pace goes out as metres/second, and the fast/slow ends INVERT (fast pace = max speed)
  * cadence is Hertz, not rpm
  * relative targets (%FTP, %HRmax) have no representation — they must resolve to
    absolute values here or the session cannot be published at all
  * nested repeats are disallowed; titles are hard-capped by the watch's own renderer

Usage:
    python3 scripts/compile_guide.py endurance/2026-08-04-easy-strides.md   # print guide.json
    python3 scripts/compile_guide.py --selftest                             # golden fixture
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The server echoes `owner` back as "Suunto" regardless of what is uploaded (observed in
# suuntool's round-trip test), so the VALUE is fiction. The key still has to be PRESENT:
# omitting it returns HTTP 400 "Instantiation of ... Guide$Sequence value failed", because the
# server's deserialiser treats it as a required creator property. Same for `url`. So these are
# set to something honest and ignored, rather than left out.
OWNER = "git-fit"
URL = "https://github.com/local/git-fit"

MAX_STEP_TITLE = 13      # the watch's renderer truncates past these; enforce rather than discover
MAX_FIELD_TITLE = 9
MAX_STATIC_TEXT = 54
MAX_STEPS = 1000
MAX_REPEAT_TIMES = 100
MAX_DESCRIPTION = 256

ACTIVITY_IDS = {"Run": 1, "Ride": 2}     # confirmed via suuntool activity_type_name
# Walk is absent on purpose: every Walk session in this repo is `publish: False` (meeting
# walks, tracked in-repo only), so no walk guide has ever needed an id. Add it when one does.

# A single prescribed pace opens the band SLOWER ONLY, never faster. athlete/zones.yml treats
# prescribed paces as ceilings ("easy days must be no FASTER than this, and slower is always
# fine"), and calls easy-day creep this athlete's most likely training error. A symmetric band
# would put the watch's own target above the ceiling the plan sets.
PACE_BAND_SLOWER_S = 30


class CompileError(Exception):
    """A session that cannot be honestly represented on the wire. Never guess past one."""


# --------------------------------------------------------------------------- parsing

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Frontmatter dict + body. Handles `key: >` folded blocks, which verify_plan.py skips."""
    if not text.startswith("---\n"):
        raise CompileError("no frontmatter")
    end = text.index("\n---\n", 3)
    fm_lines, body = text[4:end].splitlines(), text[end + 5:]

    fm: dict[str, str] = {}
    i = 0
    while i < len(fm_lines):
        m = re.match(r"^(\w+):[ \t]*(.*)$", fm_lines[i])
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        if val.startswith(">"):                      # folded scalar: take the indented block
            folded, i = [], i + 1
            while i < len(fm_lines) and (fm_lines[i].startswith(("  ", "\t")) or not fm_lines[i].strip()):
                folded.append(fm_lines[i].strip())
                i += 1
            fm[key] = " ".join(x for x in folded if x)
        else:
            fm[key] = val.split("#", 1)[0].strip()
            i += 1
    return fm, body


def parse_duration(token: str) -> dict | None:
    """`20s` `3m` `1h` `1h2m30s` `5'` `30"` -> a time trigger. Distances return None."""
    if re.fullmatch(r"[0-9.]+(km|mi|mtr)", token):
        return None
    m = re.fullmatch(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?", token)
    if m and any(m.groups()):
        h, mi, s = (int(g or 0) for g in m.groups())
        return {"kind": "time", "seconds": h * 3600 + mi * 60 + s}
    m = re.fullmatch(r"(\d+)'", token)               # short form: minutes
    if m:
        return {"kind": "time", "seconds": int(m.group(1)) * 60}
    m = re.fullmatch(r"(\d+)\"", token)              # short form: seconds
    if m:
        return {"kind": "time", "seconds": int(m.group(1))}
    return None


def parse_distance(token: str) -> dict | None:
    """`4km` `500mtr` `1mi` -> a distance trigger. A bare `m` is MINUTES and never lands here."""
    m = re.fullmatch(r"([0-9.]+)(km|mi|mtr)", token)
    if not m:
        return None
    val, unit = float(m.group(1)), m.group(2)
    meters = round({"km": val * 1000, "mi": val * 1609.344, "mtr": val}[unit], 1)
    return {"kind": "distance", "meters": int(meters) if meters == int(meters) else meters}


def pace_to_mps(sec_per_km: float) -> float:
    return round(1000.0 / sec_per_km, 2)


def parse_pace_clock(s: str) -> float:
    mm, ss = s.split(":")
    return int(mm) * 60 + int(ss)


def parse_target(rest: str, zones: dict, rel: str) -> dict:
    """The target portion of a step line -> a target field, in wire units."""
    rest = rest.strip()

    # `7:00/km Pace` or `7:45-8:45/km Pace`
    m = re.match(r"^(\d+:\d+)(?:-(\d+:\d+))?/km\s+Pace$", rest, re.I)
    if m:
        a = parse_pace_clock(m.group(1))
        b = parse_pace_clock(m.group(2)) if m.group(2) else a + PACE_BAND_SLOWER_S
        fast, slow = min(a, b), max(a, b)
        # rules/endurance-authoring.md documents ranges as faster-second; the files in this
        # repo write faster-first. min/max here makes the compiler immune to which is meant,
        # because either ordering describes the same band.
        mn, mx = pace_to_mps(slow), pace_to_mps(fast)
        return {"type": "targetPace", "value": round((mn + mx) / 2, 2), "min": mn, "max": mx}

    # `Z2 HR`, `90-95% LTHR`, `70% HR`
    m = re.match(r"^Z([1-5])\s+HR$", rest, re.I)
    if m:
        lo, hi = zones["hr_zones"][int(m.group(1))]
        return {"type": "targetHeartRate", "value": (lo + hi) // 2, "min": lo, "max": hi}
    m = re.match(r"^(\d+)(?:-(\d+))?%\s+(LTHR|HR)$", rest, re.I)
    if m:
        base = zones["lthr"] if m.group(3).upper() == "LTHR" else zones["hrmax"]
        if base is None:
            raise CompileError(f"{rel}: '{rest}' needs an absolute anchor that athlete/zones.yml "
                               f"does not define")
        a = round(base * int(m.group(1)) / 100)
        b = round(base * int(m.group(2)) / 100) if m.group(2) else a
        return {"type": "targetHeartRate", "value": (min(a, b) + max(a, b)) // 2,
                "min": min(a, b), "max": max(a, b)}

    # Cycling percentages are %FTP, and athlete/zones.yml sets `ftp_w: null` — UNKNOWN and
    # deliberately untested this block. The guide format has no relative targets, so there is
    # nothing honest to put on the wire. Refuse rather than invent an FTP.
    if re.match(r"^\d+(-\d+)?%", rest):
        raise CompileError(
            f"{rel}: '{rest}' is a %FTP target, but athlete/zones.yml has `ftp_w: null` "
            f"(\"UNKNOWN and not worth testing for this block\") and directs trainer sessions "
            f"to prescribe HR or RPE instead. Rewrite the session's targets, or set bike.ftp_w.")

    raise CompileError(f"{rel}: unrecognised target '{rest}' — refusing to guess")


def parse_cadence(rest: str) -> dict | None:
    """`85-95rpm` -> Hertz. The wire format is Hz, not rpm; a factor-of-60 error is silent."""
    m = re.search(r"(\d+)(?:-(\d+))?rpm", rest)
    if not m:
        return None
    a = int(m.group(1))
    b = int(m.group(2)) if m.group(2) else a
    return {"type": "targetCadence", "value": round((a + b) / 2 / 60, 2),
            "min": round(min(a, b) / 60, 2), "max": round(max(a, b) / 60, 2)}


def load_zones() -> dict:
    """The handful of absolute anchors needed to resolve relative targets. Stdlib only,
    matching verify_plan.py's approach of regex-reading the athlete files."""
    text = (ROOT / "athlete" / "zones.yml").read_text()

    def num(pattern, default=None):
        m = re.search(pattern, text, re.M)
        return int(m.group(1)) if m else default

    hr_zones = {}
    for z, key in ((1, "z1_recovery"), (2, "z2_aerobic"), (3, "z3_steady"),
                   (4, "z4_threshold"), (5, "z5")):
        m = re.search(rf'{key}:\s*"(?:<)?(\d+)(?:-(\d+))?', text)
        if m:
            lo = int(m.group(1))
            hr_zones[z] = (lo, int(m.group(2)) if m.group(2) else lo)
    ftp = re.search(r"^\s*ftp_w:\s*(\S+)", text, re.M)
    return {
        "lthr": num(r"^\s*lthr:\s*(\d+)"),
        "hrmax": num(r"^\s*max:\s*(\d+)"),
        "hr_zones": hr_zones,
        "ftp": None if not ftp or ftp.group(1).startswith("null") else int(ftp.group(1)),
    }


# --------------------------------------------------------------------------- compiling

def ascii_fold(s: str) -> str:
    """The watch renderer is not reliably unicode-safe, and suunto-mcp folded these too."""
    for a, b in (("\u2014", "-"), ("\u2013", "-"), ("\u2019", "'"),
                 ("\u201c", '"'), ("\u201d", '"'), ("\u2192", "->"), ("\u00b0", "deg")):
        s = s.replace(a, b)
    return s


def step_title(raw: str, fallback: str) -> str:
    title = ascii_fold(re.sub(r"\s*\d+x$", "", raw).strip()) or fallback
    return title[:MAX_STEP_TITLE].strip()


def build_step(line: str, title: str, zones: dict, rel: str, hr_first: bool) -> dict:
    """One `- <duration|distance> <target>` line -> one `fields` screen."""
    m = re.match(r"^-\s+(\S+)\s+(.*)$", line.strip())
    if not m:
        raise CompileError(f"{rel}: cannot parse step '{line.strip()}'")
    token, rest = m.group(1), m.group(2)

    dur = parse_distance(token) or parse_duration(token)
    if dur is None:
        raise CompileError(f"{rel}: '{token}' is neither a duration nor a distance")

    cadence = parse_cadence(rest)
    target = parse_target(re.sub(r"\s*\d+(-\d+)?rpm", "", rest).strip(), zones, rel) \
        if not (cadence and not re.sub(r"\s*\d+(-\d+)?rpm", "", rest).strip()) else None

    if dur["kind"] == "time":
        trigger_inner = {"type": "stepDuration", "value": dur["seconds"]}
        countdown = {"type": "stepDurationCountdown", "value": dur["seconds"]}
    else:
        trigger_inner = {"type": "stepDistance", "value": dur["meters"]}
        countdown = {"type": "stepDistanceCountdown", "value": dur["meters"]}

    fields: list[dict] = []
    if target:
        fields.append(target)
    if cadence:
        fields.append(cadence)
    # Measurement fields follow the target. HR leads on HR-targeted steps so the number the
    # athlete is chasing sits at the top of the screen.
    fields.extend([{"type": "heartRate"}, {"type": "pace"}] if hr_first
                  else [{"type": "pace"}, {"type": "heartRate"}])
    fields.append(countdown)

    for f in fields:
        if "title" in f and len(f["title"]) > MAX_FIELD_TITLE:
            raise CompileError(f"{rel}: field title '{f['title']}' exceeds {MAX_FIELD_TITLE}")

    return {
        "type": "fields",
        # "press lap to skip early" — the standard pattern, and the only way a step that
        # overruns its distance on a wrong turn doesn't strand the athlete mid-session.
        "trigger": {"type": "or", "triggers": [trigger_inner, {"type": "manualLap"}]},
        "title": title,
        "createManualLap": True,
        "fields": fields,
    }


def compile_session(path: Path, zones: dict | None = None) -> dict:
    zones = zones or load_zones()
    rel = path.name
    fm, body = parse_frontmatter(path.read_text())

    for key in ("date", "sport", "name", "type"):
        if key not in fm:
            raise CompileError(f"{rel}: missing frontmatter `{key}`")
    if fm.get("publish", "").lower() == "false":
        raise CompileError(f"{rel}: marked `publish: {fm['publish']}` — not a watch guide")
    if fm["sport"] not in ACTIVITY_IDS:
        raise CompileError(f"{rel}: no activity id mapped for sport '{fm['sport']}'")

    hr_first = fm.get("target_mode") == "hr"
    steps: list[dict] = []
    pending: list[str] = []
    header, repeat_times = "", 0

    def flush():
        nonlocal pending, repeat_times
        if not pending:
            return
        built = [build_step(ln, step_title(header, f"Step {len(steps) + 1}"), zones, rel, hr_first)
                 for ln in pending]
        if repeat_times > 1:
            if repeat_times > MAX_REPEAT_TIMES:
                raise CompileError(f"{rel}: repeat x{repeat_times} exceeds {MAX_REPEAT_TIMES}")
            # Rest steps inside a repeat get their own title so the watch screen isn't
            # ambiguous about which half of the interval you're in.
            for s in built[1:]:
                s["title"] = "Recovery"
            steps.append({"type": "repeat", "times": repeat_times, "steps": built})
        else:
            steps.extend(built)
        pending, repeat_times = [], 0

    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- "):
            pending.append(stripped)
            continue
        flush()                                    # a header closes the previous block
        header = stripped
        m = re.search(r"(\d+)x$", stripped)
        repeat_times = int(m.group(1)) if m else 0
    flush()

    if not steps:
        raise CompileError(f"{rel}: no steps found in the body")
    total = sum(s["times"] * len(s["steps"]) if s["type"] == "repeat" else 1 for s in steps)
    if total > MAX_STEPS:
        raise CompileError(f"{rel}: {total} steps exceeds the {MAX_STEPS} limit")

    # The description is what the athlete reads in the app listing, so it leads with `follow:` —
    # which instrument to actually obey. rules/endurance-authoring.md requires it to be non-empty
    # or the push errors.
    description = ascii_fold(fm.get("follow") or fm.get("intent") or fm["name"])[:MAX_DESCRIPTION]

    # Key order mirrors a known-good compile of this format. Order doesn't affect parsing, but
    # it keeps a diff against a reference guide readable.
    return {
        "name": ascii_fold(fm["name"])[:60],
        "description": description,
        "shortDescription": ascii_fold(fm["name"])[:23],
        "localDate": fm["date"],
        "type": "sequence",
        "activities": [ACTIVITY_IDS[fm["sport"]]],
        "usage": "workout",
        "owner": OWNER,
        "url": URL,
        "externalId": f"git-fit-{path.stem}"[:64],
        "steps": steps,
    }


# --------------------------------------------------------------------------- cli

def selftest() -> int:
    """Compile against a golden fixture.

    The fixture's STRUCTURE (trigger shape, field order, countdown types, repeat nesting, the
    m/s inversion) is a verified suunto-mcp compile of this exact session, captured before that
    backend was taken out of the publishing path. The target numbers follow this repo's own
    slower-only band rule, so they are ours rather than inherited.
    """
    golden_path = ROOT / "scripts" / "testdata" / "2026-08-04-easy-strides.guide.json"
    if not golden_path.exists():
        print(f"no fixture at {golden_path.relative_to(ROOT)}")
        return 1
    got = compile_session(ROOT / "endurance" / "2026-08-04-easy-strides.md")
    want = json.loads(golden_path.read_text())
    if got == want:
        print("selftest OK — compiled output matches the golden fixture")
        return 0
    print("selftest FAILED\n--- want ---")
    print(json.dumps(want, indent=2))
    print("--- got ---")
    print(json.dumps(got, indent=2))
    return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("session", nargs="?", type=Path)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--all", action="store_true", help="compile every publishable session")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if args.all:
        zones, failed = load_zones(), 0
        for f in sorted((ROOT / "endurance").glob("*.md")):
            try:
                g = compile_session(f, zones)
                total = sum(s["times"] * len(s["steps"]) if s["type"] == "repeat" else 1
                            for s in g["steps"])
                print(f"  ok    {f.name}  ({total} steps)")
            except CompileError as e:
                msg = str(e)
                if "not a watch guide" in msg:
                    print(f"  skip  {f.name}  (publish: false)")
                else:
                    print(f"  FAIL  {msg}")
                    failed += 1
        print(f"\n{failed} session(s) could not be compiled." if failed else "\nAll compiled.")
        return 1 if failed else 0

    if not args.session:
        ap.error("give a session path, --all, or --selftest")
    try:
        print(json.dumps(compile_session(args.session), indent=2))
    except CompileError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
