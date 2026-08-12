#!/usr/bin/env python3
"""Check the plan against the hard invariants in AGENTS.md.

Run this after authoring or editing any week. Exits non-zero if anything fails,
so it also works as a pre-commit check.

Checks, all derived from athlete/profile.md rather than hardcoded:
  1. Weekly running-time total <= time_budget.weekly_total_max_min
     (excludes concurrent: meetings sessions, and excludes type: race)
  2. Longest single session <= time_budget.long_run_max_min
  3. Weekday sessions <= time_budget.weekday_session_max_min, unless flagged with
     `budget_exception:` and within weekday_session_exception_max_min
  4. Walking week-over-week increase <= meeting_budget.walking.weekly_ramp_max_pct
  5. The `m`-means-minutes trap: a distance-looking value written as minutes
  6. Rest steps carry an explicit target (intervals.icu requires one)
  7. Long/ultra sessions (>~2h) use target_mode hr|effort, never pace
  8. Frontmatter is well-formed and required keys are present
  9. Race-session paces sit inside the ultra bands in athlete/zones.yml, and are never
     faster than the easy-day ceiling (AGENTS.md invariant 6)
  9. log/ entries are well-formed, and the manual readiness signals they carry
     (soreness, session-RPE) are in range and consistent with the day's session
     — see rules/logging.md
 10. log/ `conditions:` blocks are internally consistent, and an over-plan RPE on a
     hot day is flagged as heat before fitness — see rules/conditions.md

Usage:  python3 scripts/verify_plan.py [--root PATH]
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

REQUIRED_KEYS = ["date", "sport", "name", "type", "block_week", "duration_s",
                 "target_mode", "follow"]
# Types that must fit the weekday door-to-door cap. `night` is deliberately excluded —
# it runs post-bedtime and has its own, larger cap (see athlete/profile.md).
WEEKDAY_TYPES = {"easy", "tempo", "intervals", "recovery"}

# ---- log/ (rules/logging.md) ----
LOG_ENTRY_RE = re.compile(r"\d{4}-\d{2}-\d{2}\.md")   # everything else in log/ is not an entry
READINESS_VALUES = {"green", "amber", "red"}
# Expected session-RPE per session type. The ladder's "RPE trend" row asks whether a session came
# in over plan; this table is what "plan" means. See rules/logging.md for the anchors.
EXPECTED_RPE = {
    "recovery": 2, "walk": 2,
    "easy": 3, "aerobic-base": 3,
    "night": 4,
    "long": 5, "b2b": 5, "lap-sim": 5,
    "tempo": 6,
    "intervals": 7,
}
RPE_OVER_PLAN = 2          # the ladder's red condition: +2 or more over plan
LOG_STALE_DAYS = 10        # warn only; a lapsed log degrades the ladder silently

# ---- conditions: (rules/conditions.md), written by scripts/heat_load.py ----
# WBGT flag boundaries in F, matching heat_load.py's FLAGS (18/23/28C).
WBGT_YELLOW_F, WBGT_RED_F, WBGT_BLACK_F = 64.4, 73.4, 82.4
# Below this sun/shade spread, heat_load.py stops asking for shade_pct, so neither should this.
SHADE_MATTERS_F = 0.9
CONDITIONS_NUMERIC = {          # field -> (low, high) sanity bounds, generously wide
    "temp_f": (-40.0, 130.0),
    "rh_pct": (0.0, 100.0),
    "solar_w_m2": (0.0, 1400.0),   # 1361 W/m2 is the solar constant; anything above is a bug
    "wbgt_sun_f": (-40.0, 130.0),
    "wbgt_shade_f": (-40.0, 130.0),
    "wbgt_f": (-40.0, 130.0),
}


def scalar(fm: dict, key: str):
    """Frontmatter value with trailing `# comment` and quotes stripped, or None for null/blank.

    The shared parser keeps the rest of the line verbatim, and log entries carry inline
    comments (`readiness: null   # green | amber | red`), so they have to come off here.
    """
    raw = fm.get(key)
    if raw is None:
        return None
    val = raw.split("#", 1)[0].strip().strip("'\"")
    return None if val in ("", "null", "~") else val


def rating(fm: dict, key: str, rel, errors: list) -> int | None:
    """A 0-10 manual rating, or None. Out-of-range or non-numeric is a data defect."""
    val = scalar(fm, key)
    if val is None:
        return None
    try:
        n = int(float(val))
    except ValueError:
        errors.append(f"{rel}: {key}: '{val}' is not a number (rules/logging.md)")
        return None
    if not 0 <= n <= 10:
        errors.append(f"{rel}: {key}: {n} is outside the 0-10 scale (rules/logging.md)")
        return None
    return n


def parse_conditions(path: Path, rel, errors: list) -> dict | None:
    """The nested `conditions:` block from a log entry, or None if it has none.

    parse_file() only sees top-level `key: value` lines, so the block is invisible to it and to
    every other check — this reads the indented rows itself. Values keep the repo convention:
    `null` and `n/a` both mean "no number", but they mean different things and only `n/a` says
    the question was asked and settled (a night session has no shade to estimate).
    """
    text = path.read_text()
    if not text.startswith("---"):
        return None
    fm_text = text.split("---\n")[1] if "---\n" in text else ""
    m = re.search(r"^conditions:.*?(?=^\w|\Z)", fm_text, re.M | re.S)
    if not m:
        return None
    out: dict = {}
    for line in m.group(0).splitlines()[1:]:
        kv = re.match(r"^\s+(\w+):\s*(.*)$", line)
        if not kv:
            continue
        val = kv.group(2).split("#", 1)[0].strip()
        out[kv.group(1)] = None if val in ("", "null", "~") else val

    for field, (lo, hi) in CONDITIONS_NUMERIC.items():
        raw = out.get(field)
        if raw is None:
            continue
        try:
            num = float(raw)
        except ValueError:
            errors.append(f"{rel}: conditions.{field}: '{raw}' is not a number "
                          f"(rules/conditions.md)")
            out[field] = None
            continue
        if not lo <= num <= hi:
            errors.append(f"{rel}: conditions.{field}: {num} is outside {lo}–{hi} — "
                          f"that is a unit or data error, not weather (rules/conditions.md)")
        out[field] = num

    shade = out.get("shade_pct")
    if shade is not None and shade != "n/a":
        try:
            shade = float(shade)
            if not 0.0 <= shade <= 100.0:
                errors.append(f"{rel}: conditions.shade_pct: {shade} is not 0–100")
                shade = None
        except ValueError:
            errors.append(f"{rel}: conditions.shade_pct: '{shade}' is not a percentage or 'n/a' "
                          f"(rules/conditions.md)")
            shade = None
        out["shade_pct"] = shade
    return out


def check_conditions(rel, cond: dict, main: dict | None, rpe: int | None,
                     errors: list, warnings: list) -> None:
    """Cross-check one log entry's conditions block. See rules/conditions.md.

    The point of this check is a specific, twice-repeated failure in this repo's own history:
    a hot session read as mis-pacing or as fitness decay because nobody had the ambient number
    (the 08-02 30k, the 08-04 run logged from the wrist sensor at 72F when it was 85F). Once
    the number is in the file, an over-plan RPE on a hot day should say so out loud.
    """
    sun, shade_wbgt = cond.get("wbgt_sun_f"), cond.get("wbgt_shade_f")
    shade_pct, eff = cond.get("shade_pct"), cond.get("wbgt_f")

    if sun is not None and shade_wbgt is not None:
        spread = sun - shade_wbgt
        if spread > SHADE_MATTERS_F and shade_pct is None:
            warnings.append(
                f"{rel}: shade was worth {spread:.1f}F of WBGT here but shade_pct is null — "
                f"without it the session cannot be placed in the bracket, and it is the one "
                f"field in the block the athlete has to supply (rules/conditions.md)")
        # A hand-edited shade_pct that no longer agrees with wbgt_f is worse than either alone.
        if isinstance(shade_pct, float) and eff is not None:
            want = sun + (shade_wbgt - sun) * shade_pct / 100.0
            if abs(want - eff) > 0.3:
                errors.append(
                    f"{rel}: conditions.wbgt_f is {eff}F but {shade_pct:.0f}% shade between "
                    f"{sun}F and {shade_wbgt}F is {want:.1f}F — re-run scripts/heat_load.py "
                    f"rather than editing the derived field by hand")

    if eff is None:
        return
    if eff >= WBGT_BLACK_F:
        warnings.append(
            f"{rel}: WBGT {eff:.1f}F — black-flag conditions. Whatever the session was, it was "
            f"not the session that was prescribed; read the week against that")
    if rpe is not None and main:
        expected = EXPECTED_RPE.get(main["type"])
        if expected is not None and rpe - expected >= RPE_OVER_PLAN and eff >= WBGT_RED_F:
            warnings.append(
                f"{rel}: RPE {rpe} ran {rpe - expected} over plan AND WBGT was {eff:.1f}F — "
                f"heat is the first explanation here, not fitness. This repo has twice "
                f"re-read a hot session as mis-pacing (AGENTS.md invariant 8); do not "
                f"re-author the week off this data point alone")


def check_logs(root: Path, sessions_by_date: dict, errors: list, warnings: list) -> None:
    """Validate log/ entries and surface the two manual readiness signals.

    Malformed data is an error; a missing rating is only ever a warning. Failing the build
    because a field is blank would train the athlete to ignore this script, and a null is a
    legitimate answer — see rules/logging.md.
    """
    log_dir = root / "log"
    if not log_dir.is_dir():
        return

    entries: list[tuple[str, str | None, int | None, int | None]] = []
    for f in sorted(log_dir.glob("*.md")):
        if not LOG_ENTRY_RE.fullmatch(f.name):
            continue                                   # TEMPLATE.md, notes, anything else
        fm, _ = parse_file(f)
        rel = f.relative_to(root)

        date = scalar(fm, "date")
        if date is None:
            errors.append(f"{rel}: log entry has no `date:` (rules/logging.md)")
            continue
        if date != f.stem:
            errors.append(f"{rel}: date '{date}' does not match the filename")
            continue

        readiness = scalar(fm, "readiness")
        if readiness is not None and readiness not in READINESS_VALUES:
            errors.append(
                f"{rel}: readiness '{readiness}' is not one of "
                f"{'/'.join(sorted(READINESS_VALUES))} (rules/progression.md)")
            readiness = None

        soreness = rating(fm, "soreness_0_10", rel, errors)
        rpe = rating(fm, "rpe_0_10", rel, errors)

        # The day's main session = its longest non-meeting session. Only that one is rated.
        day = [s for s in sessions_by_date.get(date, []) if not s["concurrent"]]
        main = max(day, key=lambda s: s["dur"]) if day else None

        cond = parse_conditions(f, rel, errors)
        if cond is not None:
            check_conditions(rel, cond, main, rpe, errors, warnings)
        entries.append((date, readiness, soreness, rpe, cond))

        if main and soreness is None and readiness is None:
            warnings.append(
                f"{rel}: trained ({main['name']}) but neither soreness nor readiness recorded — "
                f"the ladder in rules/progression.md is running on Suunto signals alone")

        if rpe is not None and main:
            expected = EXPECTED_RPE.get(main["type"])
            if expected is not None and rpe - expected >= RPE_OVER_PLAN:
                warnings.append(
                    f"{rel}: RPE {rpe} on a `{main['type']}` session ({main['name']}) — "
                    f"{rpe - expected} over the expected {expected}. "
                    + ("Easy-day creep is this athlete's most likely training error "
                       "(athlete/zones.yml)." if expected <= 3 else
                       "Check fueling and sleep debt before reading it as fitness."))

    if not entries:
        warnings.append("log/ has no dated entries — see rules/logging.md and log/TEMPLATE.md")
        return

    # ---- log readout ----
    print(f"\nlog/ — last {min(len(entries), 5)} of {len(entries)} entr"
          f"{'y' if len(entries) == 1 else 'ies'}:")
    print(f"  {'date':<12} {'readiness':<10} {'sore':>5} {'rpe':>5} {'WBGT':>7}  conditions")
    for date, readiness, soreness, rpe, cond in entries[-5:]:
        wbgt = (cond or {}).get("wbgt_f")
        note = "—"
        if cond is not None and cond.get("temp_f") is not None:
            parts = [f"{cond['temp_f']:.0f}F"]
            if cond.get("rh_pct") is not None:
                parts.append(f"{cond['rh_pct']:.0f}% RH")
            if cond.get("solar_w_m2") is not None:
                parts.append(f"{cond['solar_w_m2']:.0f} W/m2 sun")
            note = ", ".join(parts)
        elif cond is not None:
            note = "(conditions block present but empty)"
        wbgt_cell = f"{wbgt:.1f}F" if wbgt is not None else "—"
        print(f"  {date:<12} {readiness or '—':<10} "
              f"{soreness if soreness is not None else '—':>5} "
              f"{rpe if rpe is not None else '—':>5} "
              f"{wbgt_cell:>7}  {note}")

    # Two consecutive amber/red readiness calls is a re-author trigger, not just a note.
    called = [(d, r) for d, r, _, _, _ in entries if r]
    if len(called) >= 2 and all(r in ("amber", "red") for _, r in called[-2:]):
        warnings.append(
            f"readiness {called[-2][1]} then {called[-1][1]} ({called[-2][0]}, {called[-1][0]}) — "
            f"if that pattern holds for two weeks, rules/progression.md § 'When log/ should "
            f"trigger a re-author' says the next hard week becomes a down week and the "
            f"Champion-week mapping shifts (race day does not)")

    stale = (datetime.now() - datetime.strptime(entries[-1][0], "%Y-%m-%d")).days
    if stale > LOG_STALE_DAYS:
        warnings.append(
            f"newest log entry is {stale} days old ({entries[-1][0]}) — soreness and RPE do not "
            f"survive backfilling, so the ladder is down to five signals until logging resumes")


def parse_file(path: Path) -> tuple[dict, str]:
    text = path.read_text()
    parts = text.split("---\n")
    if len(parts) < 3:
        return {}, ""
    fm_text, body = parts[1], "---\n".join(parts[2:])
    fm = {}
    for m in re.finditer(r"^(\w+):[ \t]*(.*)$", fm_text, re.M):
        k, v = m.group(1), m.group(2).strip()
        if v and not v.startswith(">"):
            fm[k] = v
        elif v.startswith(">"):
            fm[k] = "<folded>"
    return fm, body


def load_budget(root: Path) -> dict:
    text = (root / "athlete" / "profile.md").read_text()

    def num(key, default):
        m = re.search(rf"{key}:\s*(\d+)", text)
        return int(m.group(1)) if m else default

    ztext = (root / "athlete" / "zones.yml").read_text()

    def pace_secs(key, which=0):
        """min:sec (or a min:sec-min:sec range) from zones.yml -> seconds/km."""
        m = re.search(rf'{key}:\s*"(\d+):(\d\d)(?:-(\d+):(\d\d))?"', ztext)
        if not m:
            return None
        g = m.groups()
        if which == 0 or not g[2]:
            return int(g[0]) * 60 + int(g[1])
        return int(g[2]) * 60 + int(g[3])

    return {
        "easy_ceiling_s": pace_secs("easy_ceiling"),
        "ultra_early_fast_s": pace_secs("ultra_lap_early", 0),
        "weekly_total_max_min": num("weekly_total_max_min", 600),
        "long_run_max_min": num("long_run_max_min", 240),
        "long_run_exception_max_min": num("long_run_exception_max_min", 360),
        "long_run_exceptions_per_block": num("long_run_exceptions_per_block", 3),
        "weekday_session_max_min": num("weekday_session_max_min", 60),
        "weekday_session_exception_max_min": num("weekday_session_exception_max_min", 90),
        "weekday_exceptions_per_block": num("weekday_exceptions_per_block", 4),
        "weekday_sessions_per_week": num("weekday_sessions_per_week", 4),
        "night_session_max_min": num("night_session_max_min", 90),
        "walk_ramp_pct": num("weekly_ramp_max_pct", 15),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = ap.parse_args()
    root, budget = args.root, load_budget(args.root)

    errors: list[str] = []
    warnings: list[str] = []
    exceptions: list[tuple] = []
    weekday_exceptions: list[tuple] = []
    weeks: dict[int, dict] = defaultdict(
        lambda: {"run": 0.0, "walk": 0.0, "ride": 0.0, "hike": 0.0, "longest": 0.0,
                 "longest_name": "", "longest_flagged": False}
    )
    sessions_by_date: dict[str, list[dict]] = defaultdict(list)   # for the log/ RPE check

    for f in sorted((root / "endurance").glob("*.md")):
        fm, body = parse_file(f)
        rel = f.relative_to(root)

        missing = [k for k in REQUIRED_KEYS if k not in fm]
        if missing:
            errors.append(f"{rel}: missing frontmatter keys: {', '.join(missing)}")
            continue

        try:
            bw = int(fm["block_week"])
            dur = int(fm["duration_s"]) / 60
        except ValueError:
            errors.append(f"{rel}: block_week/duration_s not numeric")
            continue

        sport, typ = fm["sport"], fm["type"]
        concurrent = "concurrent" in fm   # meetings | family — free time, still real load
        w = weeks[bw]
        sessions_by_date[fm["date"]].append(
            {"dur": dur, "type": typ, "name": fm["name"], "concurrent": concurrent})

        if concurrent:
            w["walk" if sport in ("Walk", "Hike") else "ride"] += dur
            if sport == "Hike":
                w["hike"] += dur
        elif typ != "race":  # the race itself isn't a training session
            w["run"] += dur
            # Over-cap long runs are allowed only when explicitly flagged, and only a few
            # per block — see athlete/profile.md. Unflagged over-cap sessions are errors.
            if dur > budget["long_run_max_min"]:
                if "budget_exception" not in fm:
                    errors.append(
                        f"{rel}: {dur:.0f}min exceeds long_run_max_min "
                        f"({budget['long_run_max_min']}min) with no `budget_exception:` reason")
                else:
                    exceptions.append((rel, dur))
                    if dur > budget["long_run_exception_max_min"]:
                        errors.append(
                            f"{rel}: {dur:.0f}min exceeds even the flagged-exception ceiling "
                            f"({budget['long_run_exception_max_min']}min)")
            # Always record the true longest session so the weekly readout reflects reality,
            # flagged or not. The per-file check above is what enforces the cap.
            if dur > w["longest"]:
                w["longest"], w["longest_name"] = dur, fm["name"]
                w["longest_flagged"] = "budget_exception" in fm
            # Mon-Fri run days, for the weekday_sessions_per_week check below. Counted as
            # distinct DAYS, not sessions, so a double doesn't consume two slots.
            if datetime.strptime(fm["date"], "%Y-%m-%d").weekday() < 5:
                w.setdefault("weekday_days", set()).add(fm["date"])
            # The weekday cap takes the same escape hatch as the long-run cap: an over-cap
            # weekday session is allowed when it carries an explicit `budget_exception:`
            # reason, and only up to a hard ceiling. Added 2026-08-12 — before this, the
            # weekday cap had NO exception mechanism at all, so a one-off longer weekday
            # session could not be expressed in the plan even when the athlete wanted it,
            # and the only options were to lie about the duration or raise the cap for
            # every week. Both are worse than a flagged, visible, counted exception.
            if typ in WEEKDAY_TYPES and dur > budget["weekday_session_max_min"]:
                if "budget_exception" not in fm:
                    errors.append(
                        f"{rel}: {dur:.0f}min exceeds weekday cap "
                        f"({budget['weekday_session_max_min']}min) with no "
                        f"`budget_exception:` reason")
                else:
                    weekday_exceptions.append((rel, dur))
                    if dur > budget["weekday_session_exception_max_min"]:
                        errors.append(
                            f"{rel}: {dur:.0f}min exceeds even the flagged weekday ceiling "
                            f"({budget['weekday_session_exception_max_min']}min)")
            if typ == "night" and dur > budget["night_session_max_min"]:
                errors.append(
                    f"{rel}: {dur:.0f}min exceeds night-session cap "
                    f"({budget['night_session_max_min']}min)")

        # 7. long sessions must not be pace-targeted
        if dur >= 120 and typ != "race" and fm["target_mode"] == "pace":
            errors.append(
                f"{rel}: {dur:.0f}min session uses target_mode: pace — "
                f"must be hr or effort (AGENTS.md invariant 4)")

        # 9. Race paces must not contradict the race model. This is the exact shape of the
        # discarded Runna prescription — a race pace faster than the athlete can hold — and it
        # recurred once already when zones were rebuilt and this file wasn't updated with them.
        # Checked BEFORE the publish skip: the race file is publish: False, but being unpublished
        # is no reason to let it stay wrong in the repo.
        if typ == "race" and budget.get("ultra_early_fast_s"):
            for m in re.finditer(r"(\d+):(\d\d)(?:-(\d+):(\d\d))?/km", body):
                fastest = (int(m.group(3)) * 60 + int(m.group(4))) if m.group(3) \
                    else (int(m.group(1)) * 60 + int(m.group(2)))
                ue = budget["ultra_early_fast_s"]
                if fastest < ue:
                    errors.append(
                        f"{rel}: race pace {m.group(0)} is faster than ultra_lap_early "
                        f"({ue // 60}:{ue % 60:02d}/km) in athlete/zones.yml — a race pace must "
                        f"never exceed the race model (AGENTS.md invariant 6)")
                ec = budget.get("easy_ceiling_s")
                if ec and fastest <= ec:
                    errors.append(
                        f"{rel}: race pace {m.group(0)} is at or faster than the EASY-DAY ceiling "
                        f"({ec // 60}:{ec % 60:02d}/km). A 30-hour race cannot be paced at "
                        f"easy-run pace.")

        # Body checks only apply to files actually pushed as watch guides.
        # Case-insensitive on purpose: the repo contains both `publish: false` and
        # `publish: False`, and a case-sensitive compare silently treats ten opted-out
        # sessions as publishable.
        if fm.get("publish", "").strip().lower() == "false":
            continue

        for line in body.splitlines():
            step = re.match(r"^-\s+(.*)$", line.strip())
            if not step:
                continue
            content = step.group(1)

            # 5. `Nm <pace>/km` where N looks like a distance => meters written as minutes
            mm = re.match(r"^([0-9.]+)m\s+.*?/km", content)
            if mm and float(mm.group(1)) >= 100:
                errors.append(
                    f"{rel}: '- {content}' — {mm.group(1)}m is MINUTES in this syntax. "
                    f"Use '{mm.group(1)}mtr' if you meant meters (AGENTS.md invariant 3)")

            # 6. every step needs a target (a pace, %, w, rpm, Z-zone, HR or free text label)
            has_target = re.search(
                r"(/km|/mi|Pace|HR|LTHR|\d+%|\d+w\b|rpm|\bZ[1-5]\b|ramp|freeride)", content)
            if not has_target and re.match(r"^[0-9.]+(s|m|h|km|mi|mtr)\b\s*$", content):
                errors.append(
                    f"{rel}: '- {content}' has no target — intervals.icu needs one "
                    f"(use '9:00/km Pace' for walk rests)")

    # ---- weekly rollups ----
    print(f"{'wk':>3} {'run':>6} {'cap':>5} {'longest':>9} {'walk':>6} {'ride':>6}   status")
    prev_walk = None
    for wk in sorted(weeks):
        d = weeks[wk]
        flags = []
        if d["run"] > budget["weekly_total_max_min"]:
            flags.append(f"OVER RUN BUDGET ({d['run']:.0f}>{budget['weekly_total_max_min']})")
        if d["longest"] > budget["long_run_max_min"] and not d["longest_flagged"]:
            flags.append(f"LONG RUN OVER CAP ({d['longest_name']})")
        if prev_walk and d["walk"] > prev_walk * (1 + budget["walk_ramp_pct"] / 100) + 1:
            msg = f"time-on-feet ramp >{budget['walk_ramp_pct']}% ({prev_walk:.0f}->{d['walk']:.0f})"
            if d["hike"] > 0:
                # Family hiking isn't a schedulable load — flag it, don't fail on it.
                warnings.append(f"block week {wk}: {msg}, driven by {d['hike']:.0f}min of "
                                f"family hiking. Unavoidable; running volume is cut to compensate. "
                                f"Watch calves/achilles and quads (descents).")
            else:
                flags.append(f"WALK RAMP >{budget['walk_ramp_pct']}% ({prev_walk:.0f}->{d['walk']:.0f})")
        # An UNDER-use warning, deliberately not an error. athlete/profile.md allows
        # weekday_sessions_per_week; for eleven weeks every single week used one fewer than
        # allowed, because the weekly template handed Thursday to the meeting-time trainer ride —
        # a session that is `concurrent:` and therefore excluded from the budget entirely.
        # Something excluded from the budget cannot also be spending it. Caught 2026-08-04 by the
        # athlete, not by this script, because the constraint was never wired up.
        used = len(d.get("weekday_days", ()))
        allowed = budget["weekday_sessions_per_week"]
        if used < allowed and d["run"] < budget["weekly_total_max_min"] * 0.95:
            warnings.append(
                f"block week {wk}: {used} of {allowed} weekday run days used "
                f"({d['run']:.0f}/{budget['weekly_total_max_min']}min) — spare capacity. "
                f"Meeting-time rides/walks do NOT fill a slot (training/block.md weekly template)")
        status = "ok" if not flags else " | ".join(flags)
        longest_s = f"{d['longest']:.0f}" + ("*" if d["longest_flagged"] else "")
        print(f"{wk:>3} {d['run']:>6.0f} {budget['weekly_total_max_min']:>5} "
              f"{longest_s:>9} {d['walk']:>6.0f} {d['ride']:>6.0f}   {status}")
        errors.extend(f"block week {wk}: {fl}" for fl in flags)
        prev_walk = d["walk"]

    print()
    if exceptions:
        limit = budget["long_run_exceptions_per_block"]
        print(f"Flagged long-run exceptions ({len(exceptions)}/{limit} allowed per block):")
        for rel, dur in exceptions:
            print(f"  • {rel}  {dur/60:.1f}h")
        if len(exceptions) > limit:
            errors.append(
                f"{len(exceptions)} flagged long-run exceptions exceeds the per-block limit "
                f"of {limit} (athlete/profile.md) — going long should stay special")
        print()

    if weekday_exceptions:
        limit = budget["weekday_exceptions_per_block"]
        print(f"Flagged weekday-cap exceptions ({len(weekday_exceptions)}/{limit} allowed per block):")
        for rel, dur in weekday_exceptions:
            print(f"  \u2022 {rel}  {dur:.0f}min")
        if len(weekday_exceptions) > limit:
            errors.append(
                f"{len(weekday_exceptions)} flagged weekday-cap exceptions exceeds the per-block "
                f"limit of {limit} (athlete/profile.md) — the weekday cap protects family time, "
                f"and routine exceptions mean the cap is wrong rather than the session")
        print()

    check_logs(root, sessions_by_date, errors, warnings)

    print()
    for wmsg in warnings:
        print(f"WARN  {wmsg}")
    if errors:
        print(f"\n{len(errors)} problem(s):")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    print("All invariant checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
