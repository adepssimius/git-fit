#!/usr/bin/env python3
"""Dump everything the daily brief needs from the repo, in one pass.

Everything here is deterministic and repo-side. The half of the brief this can't do —
the Suunto wellness pull and the readiness call itself — is the model's job, because it
needs MCP access and judgement respectively.

Run from the repo root:  python3 .claude/skills/daily-brief/scripts/brief_context.py
Optional:                --date 2026-08-05   (defaults to today)

Deliberately prints raw facts rather than prose. The skill's whole failure mode is a brief
that sounds confident about numbers nobody checked, so this exists to make the numbers
checkable — if a field is missing it says so instead of guessing.
"""
from __future__ import annotations

import argparse
import datetime
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
ENDURANCE = ROOT / "endurance"
WEEKS = ROOT / "training" / "weeks"
LOGS = ROOT / "log"


def frontmatter(path: Path) -> tuple[dict, str]:
    """Parse the repo's simple YAML frontmatter. Folded (`>`) blocks collapse to one line."""
    text = path.read_text()
    if not text.startswith("---"):
        return {}, text
    _, fm, body = text.split("---", 2)
    out, key = {}, None
    for line in fm.splitlines():
        if not line.strip():
            continue
        m = re.match(r"^(\w+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            # Scalars in this repo carry trailing `# why` comments that are for humans reading
            # the file, not values. Strip them here or they end up quoted in the brief.
            val = re.sub(r"\s+#.*$", "", val).strip()
            out[key] = "" if val in (">", "|") else val
        elif key and line.startswith((" ", "\t")):
            if line.strip().startswith("#"):
                continue  # a comment wrapped onto its own line, not a value
            # continuation of a folded block, or a nested key like `  suunto: ...`
            nested = re.match(r"^\s+(\w+):\s*(.*)$", line)
            if nested and not out.get(key):
                out[f"{key}.{nested.group(1)}"] = re.sub(r"\s+#.*$", "", nested.group(2)).strip()
            else:
                out[key] = (out[key] + " " + line.strip()).strip()
    return out, body.strip()


def mins(fm: dict) -> int:
    return int(fm.get("duration_s", 0) or 0) // 60


def sessions_on(date: str) -> list[tuple[Path, dict, str]]:
    found = []
    for p in sorted(ENDURANCE.glob("*.md")):
        fm, body = frontmatter(p)
        if fm.get("date") == date:
            found.append((p, fm, body))
    return found


def sh(*args: str) -> str:
    try:
        return subprocess.run(args, cwd=ROOT, capture_output=True, text=True).stdout.strip()
    except Exception:
        return ""


def _easter(year: int) -> datetime.date:
    """Anonymous Gregorian computus. Needed only for Good Friday, which is movable."""
    a, b, c = year % 19, year // 100, year % 100
    d, e, f = b // 4, b % 4, (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    return datetime.date(year, (h + l - 7 * m + 114) // 31, ((h + l - 7 * m + 114) % 31) + 1)


def _nth_weekday(year: int, month: int, weekday: int, n: int) -> datetime.date:
    d = datetime.date(year, month, 1)
    return d + datetime.timedelta(days=(weekday - d.weekday()) % 7, weeks=n - 1)


def _last_weekday(year: int, month: int, weekday: int) -> datetime.date:
    last = 31 if month in (1, 3, 5, 7, 8, 10, 12) else 30
    d = datetime.date(year, month, last)
    return d - datetime.timedelta(days=(d.weekday() - weekday) % 7)


def observed_holidays(year: int) -> dict[datetime.date, str]:
    """The athlete's paid holidays, as OBSERVED (see athlete/profile.md).

    House rule, athlete-supplied: a holiday landing on a weekend is observed on the Friday
    preceding that weekend. Note this differs from the US federal convention, which moves a
    Sunday holiday FORWARD to the Monday — so don't "fix" it to match federal.
    """
    tg = _nth_weekday(year, 11, 3, 4)
    raw = {
        "New Year's Day": datetime.date(year, 1, 1),
        "MLK Day": _nth_weekday(year, 1, 0, 3),
        "Presidents' Day": _nth_weekday(year, 2, 0, 3),
        "Good Friday": _easter(year) - datetime.timedelta(days=2),
        "Memorial Day": _last_weekday(year, 5, 0),
        "Independence Day": datetime.date(year, 7, 4),
        "Labor Day": _nth_weekday(year, 9, 0, 1),
        "Thanksgiving": tg,
        "Day after Thanksgiving": tg + datetime.timedelta(days=1),
        "Christmas": datetime.date(year, 12, 25),
    }
    out = {}
    for name, d in raw.items():
        if d.weekday() >= 5:
            d -= datetime.timedelta(days=d.weekday() - 4)
        out[d] = name
    return out


def working_days(start: datetime.date, end_inclusive: datetime.date) -> list[datetime.date]:
    """Mon-Fri minus observed holidays. Walking is meeting-time, so it only happens on these."""
    hol = observed_holidays(start.year) | observed_holidays(end_inclusive.year)
    days, cur = [], start
    while cur <= end_inclusive:
        if cur.weekday() < 5 and cur not in hol:
            days.append(cur)
        cur += datetime.timedelta(days=1)
    return days


# Weekday -> strength day, from the weekly template in training/block.md. Wed/Fri/Sat carry no
# lift by design: Wednesday is left clean for the big workout, Friday is the mandated leg-recovery
# day before the long run, Saturday is the long run itself.
LIFT_BY_WEEKDAY = {0: "Lower A", 1: "Upper A", 3: "Lower B", 6: "Upper B"}


def liftoscript_week(week_no: int) -> dict[str, list[str]]:
    """{day name: [exercise lines]} for one `# Week N` block of strength/program.liftoscript."""
    src = ROOT / "strength" / "program.liftoscript"
    if not src.exists():
        return {}
    days, cur, in_week = {}, None, False
    for line in src.read_text().splitlines():
        if line.startswith("# Week "):
            in_week = line.strip() == f"# Week {week_no}"
            cur = None
            continue
        if not in_week:
            continue
        if line.startswith("## "):
            cur = line[3:].split("—")[0].strip()
            days[cur] = []
        elif cur and re.match(r"^(main|accessory|core):", line):
            days[cur].append(line.strip())
    return days


def readable_exercise(line: str) -> str:
    """`main: Squat, Dumbbell / ! 3x5 / 2x5 / 1x5 / 20lb / 180s` -> something briefable.

    Tiers matter: a `!` marks which set-variation is active, and the readiness ladder in
    rules/progression.md moves that marker down on amber/red. Surfacing the tiers lets the brief
    say what dropping a tier would actually mean today.
    """
    line = line.split(" / update:")[0].strip()
    label, _, rest = line.partition(":")
    parts = [x.strip() for x in rest.split(" / ") if x.strip()]
    if not parts:
        return line
    name, fields = parts[0], parts[1:]
    weight = next((f for f in fields if re.fullmatch(r"[\d.]+lb", f)), None)
    pause = next((f for f in fields if re.fullmatch(r"\d+s", f)), None)
    sets = [f for f in fields if f not in (weight, pause)]
    active = next((s for s in sets if s.startswith("!")), sets[0] if sets else "")
    tiers = " | ".join(s.lstrip("! ").strip() for s in sets)
    out = f"{label:<9} {name:<34} {active.lstrip('! ').strip():<10}"
    if weight:
        out += f" @ {weight:<8}"
    if pause:
        out += f" rest {pause}"
    if len(sets) > 1:
        out += f"   [tiers: {tiers}]"
    return out.rstrip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--walked", type=int, default=None,
                    help="minutes of WALKING already logged this block week, from Suunto")
    args = ap.parse_args()
    date = args.date
    d = datetime.date.fromisoformat(date)

    print(f"# BRIEF CONTEXT — {d.strftime('%A %-d %B %Y')} ({date})\n")

    # ---- today's sessions -------------------------------------------------
    todays = sessions_on(date)
    block_week = next((fm.get("block_week") for _, fm, _ in todays if fm.get("block_week")), None)
    if not block_week:
        # Rest days have no session file to read block_week from, but the week context still
        # matters — it's how you tell a planned rest day from a hole. Block week 9 starts
        # Mon 2026-08-03 (training/block.md).
        anchor = datetime.date(2026, 8, 3)
        delta = (d - anchor).days
        if delta >= 0:
            block_week = str(9 + delta // 7)

    print("## Today's sessions")
    if not todays:
        print("  (none scheduled — check the week file below before calling it a rest day;")
        print("   a genuinely empty day and a missing file look identical from here)")
    for p, fm, body in todays:
        conc = fm.get("concurrent")
        pub = fm.get("published.suunto", "null")
        guide = re.search(r"guide id (\w+)", pub or "")
        print(f"\n  {p.name}")
        print(f"    name        {fm.get('name')}")
        print(f"    sport/type  {fm.get('sport')}/{fm.get('type')}"
              + (f"   concurrent: {conc}" if conc else ""))
        print(f"    duration    {mins(fm)}min" + (f"   {fm['distance_km']}km" if fm.get("distance_km") else ""))
        print(f"    target_mode {fm.get('target_mode')}")
        print(f"    published   {'guide ' + guide.group(1) if guide else pub}")
        print(f"    brief       {fm.get('brief', '')}")
        print(f"    follow      {fm.get('follow', '')}")
        print("    steps:")
        for line in body.splitlines():
            if line.strip():
                print(f"      {line}")

    # ---- the week ---------------------------------------------------------
    print("\n## Week file")
    if block_week:
        wf = WEEKS / f"w{int(block_week):02d}.md"
        if wf.exists():
            print(f"  {wf.relative_to(ROOT)}")
            for line in wf.read_text().splitlines():
                if line.startswith("**Champion") or line.startswith(f"| {d.strftime('%a')} "):
                    print(f"    {line.strip()}")
            print(f"    Liftoscript week = block_week - 8 = {int(block_week) - 8}")
        else:
            print(f"  MISSING: {wf.relative_to(ROOT)}")
    else:
        print("  (no block_week — no session file today to read it from)")

    # ---- strength ---------------------------------------------------------
    print("\n## Today's strength")
    if block_week:
        lw = int(block_week) - 8
        days = liftoscript_week(lw)
        want = LIFT_BY_WEEKDAY.get(d.weekday())
        if not want:
            print(f"  none — {d.strftime('%A')} carries no lift in the weekly template")
        elif want in days:
            print(f"  {want}   (Liftoscript Week {lw})")
            for line in days[want]:
                print(f"    {readable_exercise(line)}")
            print("    tier note: rules/progression.md drops the active tier on amber/red")
        else:
            have = ", ".join(days) if days else "nothing"
            print(f"  none — Liftoscript Week {lw} has no {want}. That week contains: {have}.")
            print(f"  (deliberate if this is a taper/rest/Big-Day week; check strength/notes.md)")
    else:
        print("  (unknown — no block week)")

    # ---- week-to-date load ------------------------------------------------
    if block_week:
        monday = d - datetime.timedelta(days=d.weekday())
        planned = done = todays_min = 0
        for p2 in sorted(ENDURANCE.glob("*.md")):
            fm, _ = frontmatter(p2)
            if fm.get("block_week") != str(block_week) or fm.get("concurrent"):
                continue
            if fm.get("sport") != "Run":
                continue
            m = mins(fm)
            planned += m
            sd = fm.get("date", "")
            if sd < date:
                done += m
            elif sd == date:
                todays_min += m
        print(f"\n## Week-to-date running load (block week {block_week})")
        print(f"  before today {done}min | today {todays_min}min | rest of week "
              f"{planned - done - todays_min}min | week total {planned}min")
        print(f"  today is {todays_min / planned * 100:.0f}% of the week's running"
              if planned else "")

    # ---- walking ----------------------------------------------------------
    # The walk target is a WEEKLY bucket (one meeting-walk-week.md per block week), but he
    # executes it daily, so the useful number is "how much today". rules/progression.md calls this
    # ramp the block's single most likely source of an overuse injury — it climbs 180 -> 465
    # min/wk — which is why falling behind and then cramming it into two days is the failure mode
    # worth naming, not just the weekly total.
    print("\n## Walking")
    def time_on_feet(bw: str) -> tuple[int, int]:
        """(walk minutes, hike minutes) for a block week. Both count as time on feet.

        verify_plan.py's ramp check sums them, so this has to as well — a ramp computed from the
        walk target alone reports a false +61% into block week 14, because block week 13 carries
        180min of family hiking that the meeting-walk file knows nothing about.
        """
        walk = hike = 0
        for p3 in sorted(ENDURANCE.glob("*.md")):
            f, _ = frontmatter(p3)
            if f.get("block_week") != bw or not f.get("concurrent"):
                continue
            if f.get("sport") == "Walk":
                walk += mins(f)
            elif f.get("sport") == "Hike":
                hike += mins(f)
        return walk, hike

    walk_target = None
    for p2 in sorted(ENDURANCE.glob("*meeting-walk-week.md")):
        fm, _ = frontmatter(p2)
        if fm.get("block_week") == str(block_week):
            walk_target = mins(fm)

    if walk_target is None:
        print(f"  no walk target for block week {block_week} — check whether this is a travel/"
              f"hiking week where hiking replaces it (training/block.md § Travel weeks)")
    else:
        monday = d - datetime.timedelta(days=d.weekday())
        sunday = monday + datetime.timedelta(days=6)
        all_wd = working_days(monday, sunday)
        left_wd = [x for x in all_wd if x >= d]
        done_wd = [x for x in all_wd if x < d]
        hol = observed_holidays(d.year)
        offdays = [x for x in (monday + datetime.timedelta(days=i) for i in range(7))
                   if x.weekday() < 5 and x in hol]

        print(f"  target      {walk_target}min this week")
        print(f"  working days {len(all_wd)} this week ({', '.join(x.strftime('%a') for x in all_wd)})"
              + (f"   [{', '.join(hol[x] + ' ' + x.strftime('%a') for x in offdays)} off]" if offdays else ""))
        print(f"              -> {walk_target / len(all_wd):.0f}min per working day if spread evenly"
              if all_wd else "              -> NO working days this week")

        if block_week:
            w_now, h_now = time_on_feet(str(block_week))
            w_prev, h_prev = time_on_feet(str(int(block_week) - 1))
            tof_now, tof_prev = w_now + h_now, w_prev + h_prev
            hike_note = f" (incl. {h_now}min hiking)" if h_now else ""
            print(f"  time-on-feet {tof_now}min this week{hike_note}, {tof_prev}min last week")
            if tof_prev:
                delta = (tof_now - tof_prev) / tof_prev * 100
                print(f"  ramp        {delta:+.0f}%"
                      + ("   OVER the 15%/wk cap — check whether hiking drives it, which "
                         "training/block.md treats as unavoidable rather than a failure"
                         if delta > 15 else ""))

        today_is_workday = d in all_wd
        print(f"  today       {d.strftime('%a')} — "
              + ("a walking day" if today_is_workday
                 else f"NOT a walking day ({hol.get(d, 'weekend')})"))

        if args.walked is None:
            print(f"  -> pull WALKING activities (activityId 0) since Mon {monday}, sum the minutes,")
            print(f"     then re-run with --walked <total> for the exact per-day number")
        else:
            done, remaining = args.walked, max(0, walk_target - args.walked)
            print(f"  done        {done}min | remaining {remaining}min")
            if left_wd:
                print(f"  -> {remaining / len(left_wd):.0f}min/day across the "
                      f"{len(left_wd)} working day(s) left ({', '.join(x.strftime('%a') for x in left_wd)})")
            else:
                print(f"  -> no working days left this week; {remaining}min will not be made up")
            # Pace is measured in working days, not calendar days — a Wednesday check-in with
            # Mon+Tue behind it should compare against 2/5 of the target, not 2/7.
            if done_wd:
                expected = walk_target * len(done_wd) / len(all_wd)
                if done < expected * 0.85:
                    print(f"     BEHIND pace ({done}min vs {expected:.0f}min expected after "
                          f"{len(done_wd)} working day(s)) — say so. Cramming the gap into two big "
                          f"days is the ramp spike rules/progression.md warns about; if catching up "
                          f"means spiking, recommend missing the target instead")

    # ---- recent log -------------------------------------------------------
    print("\n## Recent log (soreness/RPE are the ladder's only manual signals)")
    entries = sorted(p for p in LOGS.glob("*.md") if re.match(r"\d{4}-\d{2}-\d{2}\.md$", p.name))
    for p in entries[-4:]:
        fm, _ = frontmatter(p)
        print(f"  {fm.get('date'):<12} readiness={fm.get('readiness','—'):<7} "
              f"soreness={fm.get('soreness_0_10','—'):<5} rpe={fm.get('rpe_0_10','—')}")
    if not any(fm.get("date") == date for fm, _ in (frontmatter(p) for p in entries)):
        print(f"  -> log/{date}.md does NOT exist yet")

    # ---- housekeeping, only when it's actually actionable ------------------
    notes = []

    ahead = sh("git", "rev-list", "--count", "@{u}..HEAD")
    if ahead and ahead != "0":
        notes.append(f"{ahead} commit(s) not pushed to origin")

    dirty = [ln for ln in sh("git", "status", "--porcelain").splitlines() if ln.strip()]
    if dirty:
        notes.append(f"{len(dirty)} file(s) uncommitted")

    horizon = (d + datetime.timedelta(days=14)).isoformat()
    unpub = []
    for p in sorted(ENDURANCE.glob("*.md")):
        fm, _ = frontmatter(p)
        sd = fm.get("date", "")
        if not (date <= sd <= horizon):
            continue
        if str(fm.get("publish", "")).lower() == "false":
            continue
        if (fm.get("published.suunto") or "null") == "null":
            unpub.append((sd, fm.get("name", p.name)))
    if unpub:
        notes.append(f"{len(unpub)} session(s) in the next 14d not on the watch — "
                     f"soonest {unpub[0][0]} {unpub[0][1]}")

    # Week-file day tables quote durations by hand; they drift whenever a session is edited.
    stale = []
    for wf in sorted(WEEKS.glob("w*.md")):
        for m in re.finditer(r"\(\.\./\.\./endurance/(\S+?\.md)\), (\d+)min", wf.read_text()):
            sp = ENDURANCE / m.group(1)
            if not sp.exists():
                stale.append(f"{wf.name} links missing {m.group(1)}")
                continue
            fm, _ = frontmatter(sp)
            # Tolerate 1min: week files were written with rounding, mins() floors. Flagging
            # that difference is noise, and a check that cries wolf gets ignored.
            if abs(mins(fm) - int(m.group(2))) > 1:
                stale.append(f"{wf.name}: {m.group(1)} says {m.group(2)}min, file is {mins(fm)}min")
    if stale:
        notes.append(f"{len(stale)} stale week-file duration(s): " + "; ".join(stale[:3])
                     + (" ..." if len(stale) > 3 else ""))

    print("\n## Housekeeping")
    print("\n".join(f"  ! {n}" for n in notes) if notes else "  (clean — say nothing about this)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
