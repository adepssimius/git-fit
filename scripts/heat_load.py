#!/usr/bin/env python3
"""Ambient conditions and heat load for an outdoor session — the numbers the watch cannot see.

The Suunto temperature sensor sits against the wrist and reads body heat, so it is not an
ambient thermometer (`.claude/skills/daily-brief/references/suunto-fields.md`). Until now the
only fix was to ask the athlete, and two log entries were already corrected after the fact
because the wrist figure was believed (08-04 read 72F when it was 85F; the 08-02 30k read as
mis-pacing when it was 86F heat). This script replaces the question with a measurement:
it takes the session's own GPS track and clock, pulls the weather that was actually over that
patch of ground, and reports the heat load two ways — **in full sun and in full shade**.

Why two numbers. Solar radiation is the largest and most variable term in outdoor heat stress,
and it is the one term that shade removes. A 25C morning under open sky and the same 25C morning
under closed canopy are not the same session, and the difference is routinely larger than the
day-to-day temperature swings the athlete would otherwise blame. Reporting a single WBGT hides
exactly the variable he can control by choosing a route. So the script brackets the day —
full sun and full shade — and asks him for one number, `shade_pct`, to place the session inside
the bracket. Accumulate enough of those and `--history` can show what shade is actually worth
to *him*, in RPE, rather than in theory.

  # normal use: pipe a workout from the Suunto MCP (workouts_get / workouts_list item)
  python3 scripts/heat_load.py --workout-json workout.json
  cat workout.json | python3 scripts/heat_load.py --workout-json -

  # no watch data: state the window and the place yourself
  python3 scripts/heat_load.py --start 2026-08-10T14:05-04:00 --end 2026-08-10T15:20-04:00 \
      --lat 42.8024 --lon -71.6626

  # place the session inside the bracket, and write the block into log/YYYY-MM-DD.md
  python3 scripts/heat_load.py --workout-json workout.json --shade-pct 70 --write

  # what has shade been worth so far?
  python3 scripts/heat_load.py --history

INDOOR SESSIONS ARE REFUSED ON PURPOSE. A workout with no GPS track was a treadmill or a gym,
where outdoor weather is not just irrelevant but actively misleading, and `--write` will not
fabricate a conditions block for one. See rules/conditions.md.

Data source: Open-Meteo (https://open-meteo.com) — free, no API key, CC-BY. Model reanalysis on
a ~2km grid, not a thermometer at the trailhead: treat it as a good estimate of the ambient the
session ran in, not as an instrument reading. rules/conditions.md § "How much to trust this".
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGS = ROOT / "log"

FORECAST_API = "https://api.open-meteo.com/v1/forecast"
ARCHIVE_API = "https://archive-api.open-meteo.com/v1/archive"
# The forecast endpoint serves recent history too, at 15-minute resolution and with less lag
# than the archive. Past that window the archive is the only source, and it is hourly.
FORECAST_PAST_DAYS_MAX = 92

HOURLY_VARS = ["temperature_2m", "relative_humidity_2m", "dew_point_2m",
               "wet_bulb_temperature_2m", "shortwave_radiation", "direct_radiation",
               "diffuse_radiation", "direct_normal_irradiance", "cloud_cover",
               "wind_speed_10m", "precipitation"]

# ---------------------------------------------------------------------------
# Physical constants and model parameters
#
# Everything below is a documented default rather than a magic number, because the sun/shade
# spread this script exists to report is sensitive to two of them (ALBEDO and SURFACE_GAIN) and
# the athlete should be able to see and change what he is assuming about his own routes.
# ---------------------------------------------------------------------------
SIGMA = 5.670374419e-8      # Stefan-Boltzmann, W/m^2/K^4
GLOBE_D = 0.15              # standard WBGT black globe diameter, m (ISO 7243)
GLOBE_EMIS = 0.95           # black globe emissivity
GLOBE_ABS = 0.95            # black globe shortwave absorptivity
AIR_K = 0.0263              # thermal conductivity of air at ~300K, W/m/K
AIR_NU = 1.57e-5            # kinematic viscosity of air at ~300K, m^2/s
AIR_PR = 0.71               # Prandtl number of air

DEF_ALBEDO = 0.20           # ground reflectance: mixed trail/road. Fresh snow would be ~0.8
DEF_SURFACE_GAIN = 0.012    # sunlit ground runs hotter than air, C per W/m^2 of local irradiance.
                            # 0.012 puts a 900 W/m^2 surface ~11C above air — right for mixed
                            # grass/dirt/asphalt. Bare asphalt is nearer 0.020, deep grass 0.006.
DEF_CANOPY_SVF = 0.5        # sky-view factor under "full shade". Shade is not merely the beam
                            # switched off: a canopy also hides half the sky and replaces it with
                            # leaves at roughly air temperature. 1.0 would be open sky.
Z0_ROUGHNESS = 0.03         # surface roughness length for the 10m -> 2m wind correction, m
WIND_FLOOR = 0.3            # m/s. Never let convection go to zero; still air still moves a little

# ACSM / road-race flag thresholds, WBGT in C. rules/conditions.md explains the running-specific
# reading of these — they are event-cancellation guidance, not a training prescription.
FLAGS = [
    (float("-inf"), "WHITE",  "cold — hypothermia risk outranks heat, dress for the finish"),
    (10.0,          "GREEN",  "low heat risk"),
    (18.0,          "YELLOW", "moderate — expect some HR drift, hold effort not pace"),
    (23.0,          "RED",    "high — cut intensity, quality work is unlikely to be honest"),
    (28.0,          "BLACK",  "extreme — move it indoors or move it in the day"),
]


def flag(wbgt_c: float) -> tuple[str, str]:
    out = FLAGS[0][1:]
    for lo, name, note in FLAGS:
        if wbgt_c >= lo:
            out = (name, note)
    return out


def c_to_f(c: float) -> float:
    return c * 9 / 5 + 32


def delta_c_to_f(c: float) -> float:
    """A temperature *difference*, which scales by 9/5 with no offset. Adding 32 to a spread is
    the classic way to turn a 6F shade dividend into a 38F one."""
    return c * 9 / 5


# ---------------------------------------------------------------------------
# Google encoded polyline -> coordinates
# ---------------------------------------------------------------------------
def decode_polyline(encoded: str, precision: int = 5) -> list[tuple[float, float]]:
    """Decode a Google-encoded polyline into (lat, lon) pairs.

    This is the only usable position source in the Suunto payload: `startPosition`,
    `stopPosition` and `centerPosition` all come back as {0, 0} on every workout checked, so
    reading them would silently place every session in the Gulf of Guinea.
    """
    coords: list[tuple[float, float]] = []
    idx = lat = lon = 0
    factor = 10 ** precision
    while idx < len(encoded):
        for axis in range(2):
            shift = result = 0
            while True:
                if idx >= len(encoded):
                    return coords                    # truncated payload; keep what decoded
                byte = ord(encoded[idx]) - 63
                idx += 1
                result |= (byte & 0x1F) << shift
                shift += 5
                if byte < 0x20:
                    break
            delta = ~(result >> 1) if result & 1 else result >> 1
            if axis == 0:
                lat += delta
            else:
                lon += delta
        coords.append((lat / factor, lon / factor))
    return coords


# ---------------------------------------------------------------------------
# The heat model
# ---------------------------------------------------------------------------
def wind_at_2m(v10: float) -> float:
    """Log-law correction from the 10m reported wind to globe/runner height."""
    scale = math.log(2.0 / Z0_ROUGHNESS) / math.log(10.0 / Z0_ROUGHNESS)
    return max(WIND_FLOOR, v10 * scale)


def convective_h(v: float) -> float:
    """Convection coefficient for a 150mm sphere, Ranz-Marshall: Nu = 2 + 0.6 Re^0.5 Pr^(1/3)."""
    re = max(v, WIND_FLOOR) * GLOBE_D / AIR_NU
    nu = 2.0 + 0.6 * math.sqrt(re) * AIR_PR ** (1 / 3)
    return nu * AIR_K / GLOBE_D


def sky_temp_k(ta_c: float, tdew_c: float, cloud_frac: float, svf: float) -> float:
    """Effective radiant temperature of the upper hemisphere, K.

    Clear-sky emissivity follows the dew-point form (Berdahl & Fromberg); cloud fills the gap
    toward a black sky; canopy replaces the hidden fraction (1 - svf) with leaves at air
    temperature. That last term works *against* the shade dividend — a canopy hides the cold
    sky the body was radiating to, so real shade is slightly warmer than merely switching the
    beam off, and on a clear night it is warmer than open sky outright.
    """
    ta_k = ta_c + 273.15
    eps_clear = min(1.0, max(0.6, 0.787 + 0.764 * math.log((tdew_c + 273.15) / 273.15)))
    eps_sky = eps_clear + (1.0 - eps_clear) * cloud_frac
    sky4 = eps_sky * ta_k ** 4                        # open sky, as a 4th-power radiance
    return (svf * sky4 + (1.0 - svf) * ta_k ** 4) ** 0.25


def globe_temp_from(ta_c: float, v2: float, beam_normal: float, diffuse: float, ghi_local: float,
                    tdew_c: float, cloud_frac: float, albedo: float, surface_gain: float,
                    svf: float) -> float:
    """Black-globe temperature, C, by energy balance on a 150mm sphere.

    Takes the irradiance components *as the globe sees them*, so the caller passes full-sky
    values for the sun end of the bracket and canopy-attenuated ones for the shade end.

    Shortwave absorbed, averaged over the sphere's surface:
      beam        DNI/4            (projected area pi r^2 over surface area 4 pi r^2)
      sky diffuse DHI/2            (isotropic upper hemisphere)
      reflected   albedo * GHI/2   (isotropic lower hemisphere)
    Longwave in is the mean of the sky and ground hemispheres; out is the globe's own emission;
    convection closes the balance. Solved by bisection — the quartic is monotonic in Tg, so the
    iteration cannot land on a spurious root and 60 halvings of a 120C bracket are exact to
    well under 0.01C.
    """
    ta_k = ta_c + 273.15
    sw_absorbed = GLOBE_ABS * (beam_normal / 4.0 + diffuse / 2.0 + albedo * ghi_local / 2.0)
    t_sky_k = sky_temp_k(ta_c, tdew_c, cloud_frac, svf)
    t_grnd_k = ta_k + surface_gain * ghi_local        # sunlit ground runs hotter than the air
    lw_in = GLOBE_EMIS * 0.5 * SIGMA * (t_sky_k ** 4 + t_grnd_k ** 4)
    h = convective_h(v2)

    def residual(tg_c: float) -> float:
        tg_k = tg_c + 273.15
        return sw_absorbed + lw_in - GLOBE_EMIS * SIGMA * tg_k ** 4 + h * (ta_c - tg_c)

    lo, hi = ta_c - 30.0, ta_c + 90.0
    for _ in range(60):
        mid = (lo + hi) / 2.0
        if residual(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def wbgt(twb_c: float, tg_c: float, ta_c: float) -> float:
    """Outdoor WBGT = 0.7 Tnwb + 0.2 Tg + 0.1 Ta.

    We substitute the *psychrometric* wet bulb for the natural wet bulb, because Open-Meteo
    supplies it directly and every published natural-wet-bulb estimator needs constants this
    script would be guessing at. The substitution runs cool in strong sun and light wind —
    on the order of 1C — so the absolute WBGT is a slight underestimate on exactly the days
    that matter most. It does NOT distort the sun/shade spread, which is what this script is
    for: the spread is carried almost entirely by the globe term. rules/conditions.md.
    """
    return 0.7 * twb_c + 0.2 * tg_c + 0.1 * ta_c


def conditions_at(step: dict, albedo: float, surface_gain: float, svf: float) -> dict:
    """Both bracket ends for one time step."""
    ta = step["temperature_2m"]
    tdew = step["dew_point_2m"]
    twb = step["wet_bulb_temperature_2m"]
    cloud = step["cloud_cover"] / 100.0
    v2 = wind_at_2m(step["wind_speed_10m"])
    dni, dhi = step["direct_normal_irradiance"], step["diffuse_radiation"]
    ghi = step["shortwave_radiation"]

    tg_sun = globe_temp_from(ta, v2, dni, dhi, ghi, tdew, cloud, albedo, surface_gain, 1.0)
    # Full shade: beam blocked, diffuse cut to the visible sky fraction, and the ground
    # underfoot lit only by what gets through.
    dhi_sh = dhi * svf
    tg_shade = globe_temp_from(ta, v2, 0.0, dhi_sh, dhi_sh, tdew, cloud,
                               albedo, surface_gain, svf)
    return {
        "ta_c": ta, "rh": step["relative_humidity_2m"], "tdew_c": tdew, "twb_c": twb,
        "ghi": ghi, "dni": dni, "dhi": dhi, "cloud_pct": step["cloud_cover"],
        "wind_ms": step["wind_speed_10m"], "precip_mm": step.get("precipitation") or 0.0,
        "tg_sun_c": tg_sun, "tg_shade_c": tg_shade,
        "wbgt_sun_c": wbgt(twb, tg_sun, ta), "wbgt_shade_c": wbgt(twb, tg_shade, ta),
    }


# ---------------------------------------------------------------------------
# Open-Meteo
# ---------------------------------------------------------------------------
def fetch(url: str, params: dict, retries: int = 4) -> dict:
    """GET with backoff. The proxy in this environment often times out the first TLS handshake
    of a session, so a single-shot fetch would fail roughly half the time it is run cold."""
    full = f"{url}?{urllib.parse.urlencode(params, doseq=True)}"
    delay = 2.0
    last = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(full, timeout=45) as resp:
                return json.load(resp)
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            last = exc
            if attempt < retries - 1:
                print(f"  ... fetch failed ({type(exc).__name__}), retry in {delay:.0f}s",
                      file=sys.stderr)
                time.sleep(delay)
                delay *= 2
    raise SystemExit(f"weather fetch failed after {retries} attempts: {last}\n"
                     f"  {full}")


def weather_window(lat: float, lon: float, start: datetime, end: datetime,
                   verbose: bool = True) -> tuple[list[dict], str, str, timezone]:
    """Time series covering [start, end], the resolution and endpoint used, and the local zone.

    Asks for `timezone=auto`, which makes Open-Meteo resolve the zone *at the run's coordinates*
    and hand back both local timestamps and the offset. That offset is the only correct basis
    for deciding which calendar day a session belongs to: this athlete runs post-bedtime and
    past midnight, and the container clock is UTC, so `datetime.astimezone()` would have filed
    the 2026-08-09 midnight run under 08-10.

    The requested date range is padded and computed in UTC, so an hour either side of the
    session is always covered no matter which side of midnight the local day falls on.
    """
    pad = timedelta(hours=1)
    day_from, day_to = (start - pad).date(), (end + pad).date()
    age_days = (datetime.now(timezone.utc).date() - day_from).days

    common = {"latitude": f"{lat:.4f}", "longitude": f"{lon:.4f}",
              "timezone": "auto", "wind_speed_unit": "ms",
              "start_date": (day_from - timedelta(days=1)).isoformat(),
              "end_date": (day_to + timedelta(days=1)).isoformat()}

    if 0 <= age_days <= FORECAST_PAST_DAYS_MAX:
        data = fetch(FORECAST_API, {**common, "minutely_15": HOURLY_VARS,
                                    "hourly": HOURLY_VARS})
        block, res, src = data.get("minutely_15"), "15min", "forecast"
        if not block or not block.get("time"):
            block, res = data["hourly"], "hourly"
    else:
        data = fetch(ARCHIVE_API, {**common, "hourly": HOURLY_VARS})
        block, res, src = data["hourly"], "hourly", "archive"

    local = timezone(timedelta(seconds=data.get("utc_offset_seconds", 0)),
                     data.get("timezone_abbreviation", ""))
    steps = []
    for i, stamp in enumerate(block["time"]):
        row = {"time": datetime.fromisoformat(stamp).replace(tzinfo=local)}
        ok = True
        for var in HOURLY_VARS:
            val = block.get(var, [None] * len(block["time"]))[i]
            if val is None and var != "precipitation":
                ok = False
                break
            row[var] = val
        if ok:
            steps.append(row)
    if verbose:
        print(f"  grid point {data['latitude']:.4f},{data['longitude']:.4f} "
              f"(elev {data.get('elevation', '?')}m), {src} endpoint, {res} resolution, "
              f"{data.get('timezone', '?')}", file=sys.stderr)
    return steps, res, src, local


def average_over(steps: list[dict], start: datetime, end: datetime, res: str) -> list[dict]:
    """The steps that overlap the session window, plus how much of each one it used."""
    span = timedelta(minutes=15) if res == "15min" else timedelta(hours=1)
    out = []
    for row in steps:
        s, e = row["time"], row["time"] + span
        overlap = (min(e, end) - max(s, start)).total_seconds()
        if overlap > 0:
            # `_span` matters for accumulated quantities only: Open-Meteo reports precipitation
            # as the total that fell *within each step*, so a 15-minute row carries mm/15min and
            # an hourly row carries mm/h. Dividing both by 3600 would quietly under-report rain
            # by 4x on exactly the higher-resolution data we prefer.
            out.append({**row, "_weight": overlap, "_span": span.total_seconds()})
    return out


# ---------------------------------------------------------------------------
# Workout parsing
# ---------------------------------------------------------------------------
def load_workout(spec: str) -> dict:
    raw = sys.stdin.read() if spec == "-" else Path(spec).read_text()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"--workout-json is not JSON: {exc}")
    if isinstance(data, dict) and "items" in data:      # a workouts_list response
        items = data["items"]
        if not items:
            raise SystemExit("--workout-json: the workouts_list response has no items")
        if len(items) > 1:
            print(f"  note: {len(items)} workouts in payload, using the first "
                  f"({items[0].get('activityName', '?')})", file=sys.stderr)
        data = items[0]
    return data


def workout_window(w: dict) -> tuple[datetime, datetime]:
    for key in ("startTime", "stopTime"):
        if key not in w:
            raise SystemExit(f"workout JSON has no `{key}` — is this a workouts_get response?")
    start = datetime.fromtimestamp(w["startTime"] / 1000, timezone.utc)
    stop = datetime.fromtimestamp(w["stopTime"] / 1000, timezone.utc)
    if stop <= start:
        raise SystemExit(f"workout window is not positive: {start} -> {stop}")
    return start, stop


def workout_location(w: dict) -> tuple[float, float, int]:
    """Representative (lat, lon) for the session, and the number of track points behind it.

    Uses the median point rather than the start: a point-to-point run can finish some way from
    where it began, and the median sits in the terrain the session actually spent its time in.
    """
    line = w.get("polyline") or ""
    pts = decode_polyline(line) if line else []
    pts = [p for p in pts if abs(p[0]) > 0.01 or abs(p[1]) > 0.01]
    if len(pts) < 2:
        return (float("nan"), float("nan"), len(pts))
    lats = sorted(p[0] for p in pts)
    lons = sorted(p[1] for p in pts)
    mid = len(pts) // 2
    return (lats[mid], lons[mid], len(pts))


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------
def weighted(rows: list[dict], key: str) -> float:
    total = sum(r["_weight"] for r in rows)
    return sum(r[key] * r["_weight"] for r in rows) / total if total else float("nan")


def summarize(rows: list[dict], albedo: float, surface_gain: float, svf: float) -> dict:
    per = [{**conditions_at(r, albedo, surface_gain, svf),
            "_weight": r["_weight"], "_span": r["_span"]} for r in rows]
    out = {k: weighted(per, k) for k in
           ("ta_c", "rh", "tdew_c", "twb_c", "ghi", "dni", "cloud_pct", "wind_ms",
            "tg_sun_c", "tg_shade_c", "wbgt_sun_c", "wbgt_shade_c")}
    out["ta_max_c"] = max(p["ta_c"] for p in per)
    out["ghi_peak"] = max(p["ghi"] for p in per)
    out["wbgt_sun_max_c"] = max(p["wbgt_sun_c"] for p in per)
    out["precip_mm"] = sum(p["precip_mm"] * p["_weight"] / p["_span"] for p in per)
    sunlit = sum(p["_weight"] for p in per if p["ghi"] > 20)
    out["daylight_frac"] = sunlit / sum(p["_weight"] for p in per)
    out["_per_step"] = per
    return out


def effective_wbgt(s: dict, shade_pct: float | None) -> float | None:
    """Place the session inside the sun/shade bracket. Linear in shade fraction — the globe term
    is very nearly linear in the beam it sees, and a runner alternating sun and canopy is
    time-averaging exactly that."""
    if shade_pct is None:
        return None
    f = max(0.0, min(100.0, shade_pct)) / 100.0
    return s["wbgt_sun_c"] * (1 - f) + s["wbgt_shade_c"] * f


# Below this, the sun/shade bracket is narrower than the model's own accuracy and asking the
# athlete to estimate his shade fraction is busywork that trains him to ignore the question.
# Night sessions collapse to zero spread by construction; heavy overcast nearly does.
SHADE_MATTERS_C = 0.5


def report(s: dict, start: datetime, end: datetime, lat: float, lon: float,
           shade_pct: float | None, res: str, local: timezone) -> None:
    dur = (end - start).total_seconds() / 60
    spread_c = s["wbgt_sun_c"] - s["wbgt_shade_c"]
    ls, le = start.astimezone(local), end.astimezone(local)
    print(f"\n## Conditions — {ls:%Y-%m-%d %H:%M} to {le:%H:%M} local ({dur:.0f}min), "
          f"{lat:.4f},{lon:.4f}, {res}\n")
    print(f"  Air            {c_to_f(s['ta_c']):.0f}F / {s['ta_c']:.1f}C mean, "
          f"{c_to_f(s['ta_max_c']):.0f}F peak")
    print(f"  Humidity       {s['rh']:.0f}%  (dew point {c_to_f(s['tdew_c']):.0f}F, "
          f"wet bulb {c_to_f(s['twb_c']):.0f}F)")
    print(f"  Solar          {s['ghi']:.0f} W/m2 mean, {s['ghi_peak']:.0f} peak  "
          f"(cloud {s['cloud_pct']:.0f}%, {s['daylight_frac'] * 100:.0f}% of the session in "
          f"daylight)")
    print(f"  Wind           {s['wind_ms']:.1f} m/s at 10m")
    if s["precip_mm"] > 0.05:
        print(f"  Precipitation  {s['precip_mm']:.1f} mm over the session")

    if spread_c < SHADE_MATTERS_C:
        wb = (s["wbgt_sun_c"] + s["wbgt_shade_c"]) / 2
        name, note = flag(wb)
        print(f"\n  Heat load:\n")
        print(f"    WBGT {c_to_f(wb):5.1f}F / {wb:4.1f}C   [{name}] {note}")
        why = ("the session ran in the dark" if s["daylight_frac"] < 0.1
               else "there was almost no direct beam to block")
        print(f"\n    Shade is worth {delta_c_to_f(abs(spread_c)):.1f}F here, i.e. nothing — "
              f"{why},\n    so route choice could not have changed this one. Not asking about "
              f"shade_pct.")
        return

    print(f"\n  Heat load, bracketed:\n")
    for label, wb, tg in (("FULL SUN  ", s["wbgt_sun_c"], s["tg_sun_c"]),
                          ("FULL SHADE", s["wbgt_shade_c"], s["tg_shade_c"])):
        name, note = flag(wb)
        print(f"    {label}  WBGT {c_to_f(wb):5.1f}F / {wb:4.1f}C   "
              f"[{name}] {note}")
        print(f"                globe {c_to_f(tg):.0f}F / {tg:.1f}C")
    print(f"\n    Shade is worth {delta_c_to_f(spread_c):.1f}F ({spread_c:.1f}C) of WBGT today.")

    eff = effective_wbgt(s, shade_pct)
    if eff is None:
        print(f"\n  -> shade_pct is the one number this cannot measure. Roughly what fraction "
              f"of the\n     session was under canopy or in building shadow? "
              f"Re-run with --shade-pct N.")
    else:
        name, note = flag(eff)
        print(f"\n    AT {shade_pct:.0f}% SHADE   WBGT {c_to_f(eff):5.1f}F / {eff:4.1f}C   "
              f"[{name}] {note}")


def fm_block(s: dict, shade_pct: float | None, lat: float, lon: float, src: str) -> str:
    """The frontmatter the log entry carries. Comment column is aligned by construction so the
    block stays readable when it lands next to the hand-written fields."""
    spread_c = s["wbgt_sun_c"] - s["wbgt_shade_c"]
    eff = effective_wbgt(s, shade_pct)
    if spread_c < SHADE_MATTERS_C:
        # No beam to block, so there is no shade question to answer and no bracket to place the
        # session inside. `n/a` says "asked and answered", which `null` would not.
        shade_val, shade_note = "n/a", "no direct sun in this window — nothing to shade"
        eff = (s["wbgt_sun_c"] + s["wbgt_shade_c"]) / 2
        eff_note = "the number the ladder reads"
    else:
        shade_val = "null" if shade_pct is None else f"{shade_pct:.0f}"
        shade_note = ("ATHLETE — 0-100, roughly. The only field here that needs you"
                      if shade_pct is None else "athlete's estimate")
        eff_note = "derived from shade_pct; the number the ladder reads"

    rows = [
        ("source", f"open-meteo/{src}", f"{lat:.4f},{lon:.4f}, from the session's GPS track"),
        ("temp_f", f"{c_to_f(s['ta_c']):.0f}", "mean over the session window"),
        ("rh_pct", f"{s['rh']:.0f}", ""),
        ("solar_w_m2", f"{s['ghi']:.0f}", "mean global horizontal irradiance"),
        ("wbgt_sun_f", f"{c_to_f(s['wbgt_sun_c']):.1f}", "the bracket: fully exposed ..."),
        ("wbgt_shade_f", f"{c_to_f(s['wbgt_shade_c']):.1f}", "... and fully shaded"),
        ("shade_pct", shade_val, shade_note),
        ("wbgt_f", "null" if eff is None else f"{c_to_f(eff):.1f}", eff_note),
    ]
    width = max(len(f"  {k}: {v}") for k, v, _ in rows)
    lines = ["conditions:                 # scripts/heat_load.py — outdoor sessions only"]
    for key, val, note in rows:
        line = f"  {key}: {val}"
        lines.append(f"{line:<{width}}  # {note}" if note else line)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Writing into log/
# ---------------------------------------------------------------------------
CONDITIONS_RE = re.compile(r"^conditions:.*?(?=^\w|\Z)", re.M | re.S)


def write_log(date_str: str, block: str) -> None:
    path = LOGS / f"{date_str}.md"
    if not path.exists():
        raise SystemExit(f"{path.relative_to(ROOT)} does not exist — copy log/TEMPLATE.md first\n"
                         f"  (heat_load.py fills a conditions block; it does not open the day)")
    text = path.read_text()
    if not text.startswith("---"):
        raise SystemExit(f"{path.relative_to(ROOT)} has no frontmatter to write into")
    _, fm, body = text.split("---", 2)

    if CONDITIONS_RE.search(fm):
        # Replacement passed as a lambda so a backslash or a \g in the block is never read as a
        # regex escape — the source field carries free text from the API.
        fm = CONDITIONS_RE.sub(lambda _: block + "\n", fm)
        verb = "updated"
    else:
        fm = fm.rstrip("\n") + "\n" + block + "\n"
        verb = "added"
    path.write_text(f"---{fm}---{body}")
    print(f"\n  {verb} the conditions block in {path.relative_to(ROOT)}")


# ---------------------------------------------------------------------------
# --history: what has shade actually been worth?
# ---------------------------------------------------------------------------
def parse_conditions(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    fm = text.split("---", 2)[1]
    m = CONDITIONS_RE.search(fm)
    if not m:
        return {}
    out = {}
    for line in m.group(0).splitlines()[1:]:
        kv = re.match(r"^\s+(\w+):\s*(.*)$", line)
        if kv:
            val = kv.group(2).split("#")[0].strip()
            out[kv.group(1)] = None if val in ("", "null", "~") else val
    return out


def scalar_fm(text: str, key: str):
    m = re.search(rf"^{key}:\s*(.*)$", text.split("---", 2)[1] if text.startswith("---") else "",
                  re.M)
    if not m:
        return None
    val = m.group(1).split("#")[0].strip()
    return None if val in ("", "null", "~") else val


def history() -> int:
    """Tabulate every logged session that carries conditions, against how it felt.

    This is the payoff for asking about shade every time. One session tells you nothing; a
    column of them tells you whether this athlete's RPE actually tracks WBGT, and whether the
    shaded routes are buying what the model says they should.
    """
    rows = []
    for path in sorted(LOGS.glob("*.md")):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}\.md", path.name):
            continue
        text = path.read_text()
        cond = parse_conditions(text)
        if not cond:
            continue
        rows.append({"date": path.stem, "rpe": scalar_fm(text, "rpe_0_10"),
                     "readiness": scalar_fm(text, "readiness"), **cond})
    if not rows:
        print("No log entry carries a conditions block yet.\n"
              "Run heat_load.py --workout-json ... --write after an outdoor session; "
              "the comparison needs a handful of days before it says anything.")
        return 0

    print(f"\n## Logged conditions — {len(rows)} session(s)\n")
    hdr = f"  {'date':<12}{'air':>6}{'RH':>5}{'sun':>7}{'sun WBGT':>10}{'shade':>7}" \
          f"{'shade%':>8}{'eff':>7}{'RPE':>5}  readiness"
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))
    for r in rows:
        def g(k, fmt=">6"):
            v = r.get(k)
            return format("—" if v is None else v, fmt)
        print(f"  {r['date']:<12}{g('temp_f')}{g('rh_pct', '>5')}"
              f"{g('solar_w_m2', '>7')}{g('wbgt_sun_f', '>10')}{g('wbgt_shade_f', '>7')}"
              f"{g('shade_pct', '>8')}{g('wbgt_f', '>7')}{g('rpe', '>5')}  "
              f"{r.get('readiness') or '—'}")

    unfilled = [r["date"] for r in rows if r.get("shade_pct") is None]
    if unfilled:
        print(f"\n  {len(unfilled)} session(s) still missing shade_pct: {', '.join(unfilled)}")
        print("  Without it the bracket stays a bracket and none of these rows can be compared.")

    paired = [r for r in rows if r.get("wbgt_f") and r.get("rpe")]
    if len(paired) < 4:
        print(f"\n  {len(paired)} session(s) have both an effective WBGT and an RPE. "
              f"Four is about where a pattern starts to be worth reading; "
              f"do not draw a line through fewer.")
    else:
        pts = [(float(r["wbgt_f"]), float(r["rpe"])) for r in paired]
        n = len(pts)
        mx = sum(p[0] for p in pts) / n
        my = sum(p[1] for p in pts) / n
        sxx = sum((p[0] - mx) ** 2 for p in pts)
        sxy = sum((p[0] - mx) * (p[1] - my) for p in pts)
        if sxx > 0:
            slope = sxy / sxx
            print(f"\n  Across {n} sessions, RPE moves {slope:+.2f} per F of effective WBGT "
                  f"(~{slope * 10:+.1f} per 10F).")
            print("  Descriptive only — session type is not controlled for here, and an easy day "
                  "in\n  the heat and an interval day in the cool will happily fake a slope. "
                  "Read it next to\n  the session types, not instead of them.")
    return 0


# ---------------------------------------------------------------------------
def main() -> int:
    p = argparse.ArgumentParser(
        description="Ambient conditions and sun/shade heat load for an outdoor session.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="See rules/conditions.md for the model, its assumptions, and how far to trust it.")
    p.add_argument("--workout-json", metavar="PATH",
                   help="Suunto workouts_get/workouts_list JSON ('-' for stdin). Supplies the "
                        "window and the location, and decides indoor vs outdoor.")
    p.add_argument("--start", help="ISO 8601 session start, e.g. 2026-08-10T14:05-04:00")
    p.add_argument("--end", help="ISO 8601 session end")
    p.add_argument("--lat", type=float)
    p.add_argument("--lon", type=float)
    p.add_argument("--shade-pct", type=float, metavar="N",
                   help="0-100, the athlete's estimate of how much of the session was shaded")
    p.add_argument("--write", action="store_true",
                   help="write the conditions block into log/YYYY-MM-DD.md (refuses indoors)")
    p.add_argument("--date", help="log date to write to; defaults to the session's local date")
    p.add_argument("--history", action="store_true",
                   help="tabulate every logged conditions block against RPE, and stop")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.add_argument("--albedo", type=float, default=DEF_ALBEDO,
                   help=f"ground reflectance (default {DEF_ALBEDO}; snow ~0.8)")
    p.add_argument("--surface-gain", type=float, default=DEF_SURFACE_GAIN,
                   help=f"sunlit ground warming, C per W/m2 (default {DEF_SURFACE_GAIN}; "
                        f"asphalt ~0.020, deep grass ~0.006)")
    p.add_argument("--canopy-svf", type=float, default=DEF_CANOPY_SVF,
                   help=f"sky-view factor under full shade (default {DEF_CANOPY_SVF})")
    args = p.parse_args()

    if args.history:
        return history()

    if (args.lat is None) != (args.lon is None):
        p.error("--lat and --lon go together; one on its own is silently ignored")
    if args.shade_pct is not None and not 0 <= args.shade_pct <= 100:
        p.error(f"--shade-pct is a percentage: {args.shade_pct} is not 0-100")

    indoor_reason = None
    if args.workout_json:
        w = load_workout(args.workout_json)
        start, end = workout_window(w)
        lat, lon, npts = workout_location(w)
        name = w.get("activityName", "?")
        print(f"\n  {name.lower().replace('_', ' ')}, "
              f"{(end - start).total_seconds() / 60:.0f}min, "
              f"{(w.get('totalDistance') or 0) / 1000:.1f}km", file=sys.stderr)
        if math.isnan(lat):
            indoor_reason = (f"no GPS track on this workout ({npts} usable points) — "
                             f"treadmill or indoor")
        else:
            print(f"  {npts} GPS points, median {lat:.4f},{lon:.4f}", file=sys.stderr)
        if args.lat is not None and args.lon is not None:
            lat, lon, indoor_reason = args.lat, args.lon, None   # explicit override wins
    else:
        if not (args.start and args.end and args.lat is not None and args.lon is not None):
            p.error("give --workout-json, or all of --start --end --lat --lon")
        start = datetime.fromisoformat(args.start)
        end = datetime.fromisoformat(args.end)
        if start.tzinfo is None or end.tzinfo is None:
            p.error("--start/--end need an explicit UTC offset — a naive timestamp on a session "
                    "that runs past midnight lands on the wrong day")
        start, end = start.astimezone(timezone.utc), end.astimezone(timezone.utc)
        if end <= start:
            p.error("--end must be after --start")
        lat, lon = args.lat, args.lon

    if indoor_reason:
        print(f"\n  INDOOR: {indoor_reason}.")
        print("  Outdoor weather does not describe this session and would be worse than no "
              "number\n  at all — a treadmill room's heat is its own thing. No conditions block "
              "written.")
        print("  If the watch dropped GPS on a run that really was outside, pass --lat/--lon.")
        return 0

    steps, res, src, local = weather_window(lat, lon, start, end)
    rows = average_over(steps, start, end, res)
    if not rows:
        raise SystemExit(f"no weather data covers {start:%Y-%m-%d %H:%M}Z–{end:%H:%M}Z at "
                         f"{lat:.4f},{lon:.4f} — the archive lags ~5 days behind today")

    s = summarize(rows, args.albedo, args.surface_gain, args.canopy_svf)
    # The log day is the day the session STARTED in local time. A night run that finishes at
    # 00:07 belongs to the evening it began, which is also how log/2026-08-09.md already reads.
    log_date = args.date or start.astimezone(local).date().isoformat()

    if args.json:
        out = {k: v for k, v in s.items() if not k.startswith("_")}
        out.update({"start_utc": start.isoformat(), "end_utc": end.isoformat(),
                    "start_local": start.astimezone(local).isoformat(),
                    "log_date": log_date, "lat": lat, "lon": lon,
                    "resolution": res, "source": src, "shade_pct": args.shade_pct,
                    "wbgt_effective_c": effective_wbgt(s, args.shade_pct)})
        print(json.dumps(out, indent=2))
        return 0

    report(s, start, end, lat, lon, args.shade_pct, res, local)
    block = fm_block(s, args.shade_pct, lat, lon, src)
    print(f"\n  Frontmatter block for the log entry:\n")
    print("\n".join("    " + ln for ln in block.splitlines()))

    if args.write:
        write_log(log_date, block)
    else:
        print(f"\n  (--write puts this in log/{log_date}.md)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
