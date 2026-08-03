#!/usr/bin/env python3
"""Check the plan against the hard invariants in AGENTS.md.

Run this after authoring or editing any week. Exits non-zero if anything fails,
so it also works as a pre-commit check.

Checks, all derived from athlete/profile.md rather than hardcoded:
  1. Weekly running-time total <= time_budget.weekly_total_max_min
     (excludes concurrent: meetings sessions, and excludes type: race)
  2. Longest single session <= time_budget.long_run_max_min
  3. Weekday sessions <= time_budget.weekday_session_max_min
  4. Walking week-over-week increase <= meeting_budget.walking.weekly_ramp_max_pct
  5. The `m`-means-minutes trap: a distance-looking value written as minutes
  6. Rest steps carry an explicit target (intervals.icu requires one)
  7. Long/ultra sessions (>~2h) use target_mode hr|effort, never pace
  8. Frontmatter is well-formed and required keys are present

Usage:  python3 scripts/verify_plan.py [--root PATH]
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

REQUIRED_KEYS = ["date", "sport", "name", "type", "block_week", "duration_s", "target_mode"]
# Types that must fit the weekday door-to-door cap. `night` is deliberately excluded —
# it runs post-bedtime and has its own, larger cap (see athlete/profile.md).
WEEKDAY_TYPES = {"easy", "tempo", "intervals", "recovery"}


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

    return {
        "weekly_total_max_min": num("weekly_total_max_min", 600),
        "long_run_max_min": num("long_run_max_min", 240),
        "long_run_exception_max_min": num("long_run_exception_max_min", 360),
        "long_run_exceptions_per_block": num("long_run_exceptions_per_block", 3),
        "weekday_session_max_min": num("weekday_session_max_min", 60),
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
    weeks: dict[int, dict] = defaultdict(
        lambda: {"run": 0.0, "walk": 0.0, "ride": 0.0, "longest": 0.0, "longest_name": "",
                 "longest_flagged": False}
    )

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
        concurrent = fm.get("concurrent") == "meetings"
        w = weeks[bw]

        if concurrent:
            w["walk" if sport == "Walk" else "ride"] += dur
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
            if typ in WEEKDAY_TYPES and dur > budget["weekday_session_max_min"]:
                errors.append(
                    f"{rel}: {dur:.0f}min exceeds weekday cap "
                    f"({budget['weekday_session_max_min']}min)")
            if typ == "night" and dur > budget["night_session_max_min"]:
                errors.append(
                    f"{rel}: {dur:.0f}min exceeds night-session cap "
                    f"({budget['night_session_max_min']}min)")

        # 7. long sessions must not be pace-targeted
        if dur >= 120 and typ != "race" and fm["target_mode"] == "pace":
            errors.append(
                f"{rel}: {dur:.0f}min session uses target_mode: pace — "
                f"must be hr or effort (AGENTS.md invariant 4)")

        # Body checks only apply to files actually pushed as watch guides.
        if fm.get("publish") == "false":
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
            flags.append(f"WALK RAMP >{budget['walk_ramp_pct']}% ({prev_walk:.0f}->{d['walk']:.0f})")
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
