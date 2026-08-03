#!/usr/bin/env python3
"""Generate a static HTML calendar overview of the training plan.

Reads directly from the repo's own source-of-truth files — no separate data store:

  - endurance/*.md            authored sessions (frontmatter + intervals.icu body)
  - strength/program.liftoscript
                               lifting days, placed on real dates via the fixed
                               weekly template documented in training/block.md
                               (Mon=Lower A, Tue=Upper A, Thu=Lower B, Sun=Upper B)
                               and the week offset in strength/notes.md
                               (liftoscript_week = block_week - 8)
  - seed/runna-plan.ics       fallback placeholders for dates that don't have an
                               authored endurance/*.md file yet
  - races/*.md                race-day marker, from the filename date
  - athlete/profile.md        weekly running-time budget, for the per-week readout

Writes a single self-contained HTML file (default: calendar.html at the repo root).
No external dependencies — stdlib only.

Usage:
    python3 scripts/generate_calendar.py [--root PATH] [--out FILE]

Rerun any time endurance/, strength/program.liftoscript, or the seed changes —
this script only reads, it never writes back into the plan.
"""
from __future__ import annotations

import argparse
import calendar
import html
import re
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path

# Fixed weekly template from training/block.md — the day each strength session
# lands on. Keep in sync with that file if the template ever changes.
BLOCK_WEEK_9_START = date(2026, 8, 3)  # Monday
STRENGTH_DAY_OFFSET = {
    "lower a": 0,  # Monday
    "upper a": 1,  # Tuesday
    "lower b": 3,  # Thursday
    "upper b": 6,  # Sunday
}
LIFTOSCRIPT_WEEK_TO_BLOCK_WEEK_OFFSET = 8  # block_week = liftoscript_week + 8

SPORT_STYLE = {
    "Run": ("#2f9e44", "🏃"),
    "Ride": ("#1971c2", "🚴"),
    "Walk": ("#e8590c", "🚶"),
    "Hike": ("#5c940d", "🥾"),
    "Lift": ("#9c36b5", "🏋️"),
    "Race": ("#c92a2a", "🏁"),
}


@dataclass
class Event:
    date: date
    sport: str          # Run | Ride | Walk | Lift | Race
    name: str
    duration_min: float | None = None
    distance_km: float | None = None
    detail: str = ""
    authored: bool = True   # False = seed placeholder, not yet authored in endurance/
    excluded_from_budget: bool = False  # concurrent:meetings sessions
    kind: str = ""          # frontmatter `type`
    key: bool = False       # anchor session worth spotting at a glance


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> dict:
    """Tolerant parser for this repo's flat-ish YAML frontmatter. Not a general
    YAML parser — handles plain scalars, quoted scalars, folded (`>`) block
    scalars, and skips nested mappings (e.g. `published:`)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data: dict = {}
    i = 1
    while i < len(lines) and lines[i].strip() != "---":
        line = lines[i]
        m = re.match(r"^(\w+):\s*(.*)$", line)
        if m and not line.startswith(" "):
            key, val = m.group(1), m.group(2).strip()
            if val in (">", "|", ">-", "|-") and key == "budget_exception":
                data[key] = "yes"
                i += 1
                while i < len(lines) and (lines[i].startswith("  ") or lines[i].strip() == ""):
                    i += 1
                continue
            if val in (">", "|", ">-", "|-"):
                i += 1
                buf = []
                while i < len(lines) and (lines[i].startswith("  ") or lines[i].strip() == ""):
                    if lines[i].strip():
                        buf.append(lines[i].strip())
                    i += 1
                data[key] = " ".join(buf)
                continue
            if val == "":
                # Nested mapping (e.g. `published:\n  suunto: null`) — not needed
                # for the calendar view, skip its indented body.
                i += 1
                while i < len(lines) and lines[i].startswith(" "):
                    i += 1
                data[key] = None
                continue
            if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
                val = val[1:-1]
            data[key] = val
        i += 1
    return data


def load_endurance_events(root: Path) -> list[Event]:
    events = []
    for f in sorted((root / "endurance").glob("*.md")):
        fm = parse_frontmatter(f.read_text())
        if not fm.get("date") or not fm.get("sport"):
            continue
        try:
            d = datetime.strptime(fm["date"], "%Y-%m-%d").date()
        except ValueError:
            continue
        dur = fm.get("duration_s")
        dur_min = round(int(dur) / 60) if dur and dur.strip("-").isdigit() else None
        dist = fm.get("distance_km")
        dist_km = float(dist) if dist else None
        events.append(Event(
            date=d,
            sport=fm.get("sport", "Run"),
            name=fm.get("name", f.stem),
            duration_min=dur_min,
            distance_km=dist_km,
            detail=fm.get("intent", ""),
            authored=True,
            excluded_from_budget=("concurrent" in fm),
            kind=fm.get("type", ""),
            key=(fm.get("type") in ("lap-sim", "race", "night")
                 or "budget_exception" in fm or fm.get("anchor") == "true"),
        ))
    return events


def load_strength_events(root: Path) -> list[Event]:
    path = root / "strength" / "program.liftoscript"
    if not path.exists():
        return []
    events = []
    week = None
    day_name = None
    exercises: list[str] = []

    def flush():
        if week is None or day_name is None:
            return
        key = re.sub(r"\s*—.*$", "", day_name).strip().lower()
        offset = STRENGTH_DAY_OFFSET.get(key)
        if offset is None:
            return
        block_week = week + LIFTOSCRIPT_WEEK_TO_BLOCK_WEEK_OFFSET
        d = BLOCK_WEEK_9_START + timedelta(weeks=block_week - 9, days=offset)
        events.append(Event(
            date=d,
            sport="Lift",
            name=re.sub(r"\s*—.*$", "", day_name).strip(),
            detail=", ".join(exercises),
            authored=True,
        ))

    for line in path.read_text().splitlines():
        m_week = re.match(r"^#\s+Week\s+(\d+)", line)
        m_day = re.match(r"^##\s+(.+)$", line)
        m_ex = re.match(r"^(?:main|accessory|core):\s*([^/]+)/", line)
        if m_week:
            flush()
            week = int(m_week.group(1))
            day_name = None
            exercises = []
        elif m_day:
            flush()
            day_name = m_day.group(1).strip()
            exercises = []
        elif m_ex:
            exercises.append(m_ex.group(1).strip())
    flush()
    return events


def block_week_of(d: date) -> int | None:
    """Block week for any date, from the fixed week-9 anchor. None outside the block."""
    wk = 9 + (d - BLOCK_WEEK_9_START).days // 7
    return wk if 9 <= wk <= 19 else None


def load_week_labels(root: Path) -> dict[int, str]:
    """Short label per block week, scraped from training/weeks/wNN.md headlines."""
    labels = {}
    for f in (root / "training" / "weeks").glob("w*.md"):
        m_wk = re.match(r"w(\d+)\.md", f.name)
        if not m_wk:
            continue
        m = re.search(r"\*\*Champion week \d+ — ([^.*]+)\.?\*\*", f.read_text())
        if m:
            labels[int(m_wk.group(1))] = m.group(1).strip()
    return labels


def load_race_days(root: Path) -> dict[date, str]:
    races = {}
    races_dir = root / "races"
    if not races_dir.exists():
        return races
    for f in races_dir.glob("*.md"):
        m = re.match(r"^(\d{4}-\d{2}-\d{2})-(.+)\.md$", f.name)
        if m:
            d = datetime.strptime(m.group(1), "%Y-%m-%d").date()
            races[d] = m.group(2).replace("-", " ").title()
    return races


def load_seed_placeholders(root: Path, covered_dates: set[date]) -> list[Event]:
    """Runna ICS upcoming events, shown faded only for dates the current plan doesn't
    touch at all. A date with any authored session is considered handled — e.g. the
    seed's Thursday quality runs were deliberately replaced by the Thursday x-train
    day, so they shouldn't linger as if they were unfinished work."""
    ics = root / "seed" / "runna-plan.ics"
    if not ics.exists():
        return []
    text = ics.read_text().replace("\r\n", "\n")
    events = []
    for block in text.split("BEGIN:VEVENT")[1:]:
        block = block.split("END:VEVENT")[0]
        uid_m = re.search(r"^UID:(.+)$", block, re.M)
        if not uid_m or not uid_m.group(1).startswith("UPCOMING"):
            continue
        dtstart_m = re.search(r"^DTSTART[^:]*:(\d{8})", block, re.M)
        summary_m = re.search(r"^SUMMARY:(.+)$", block, re.M)
        if not dtstart_m or not summary_m:
            continue
        d = datetime.strptime(dtstart_m.group(1), "%Y%m%d").date()
        if d in covered_dates:
            continue
        name = summary_m.group(1).strip()
        name = re.sub(r"^[^\w]+", "", name).strip()  # strip leading emoji
        events.append(Event(date=d, sport="Run", name=name, authored=False))
    return events


def load_weekly_budget(root: Path) -> int | None:
    profile = root / "athlete" / "profile.md"
    if not profile.exists():
        return None
    m = re.search(r"weekly_total_max_min:\s*(\d+)", profile.read_text())
    return int(m.group(1)) if m else None


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def month_span(dates: list[date]) -> list[tuple[int, int]]:
    if not dates:
        today = date.today()
        return [(today.year, today.month)]
    start, end = min(dates), max(dates)
    months = []
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        months.append((y, m))
        m += 1
        if m > 12:
            m = 1
            y += 1
    return months


def render_day_cell(d: date, month: int, events_by_date: dict[date, list[Event]],
                     race_days: dict[date, str], today: date) -> str:
    in_month = d.month == month
    classes = ["day"]
    if not in_month:
        classes.append("out")
    if d == today:
        classes.append("today")
    if d in race_days:
        classes.append("race")

    body = [f'<div class="daynum">{d.day}</div>']
    if in_month:
        if d in race_days:
            body.append(f'<div class="badge race-badge">🏁 {html.escape(race_days[d])}</div>')
        for ev in events_by_date.get(d, []):
            color, icon = SPORT_STYLE.get(ev.sport, ("#868e96", "•"))
            if not ev.authored:
                title = html.escape(f"Old Runna plan, not part of this block: {ev.name}")
                body.append(
                    f'<div class="badge seed" title="{title}">·&nbsp;{html.escape(ev.name)}</div>'
                )
                continue
            parts = [f"{icon} {html.escape(ev.name)}"]
            if ev.duration_min:
                parts.append(f"· {int(ev.duration_min)}m")
            if ev.distance_km:
                parts.append(f"· {ev.distance_km:g}km")
            title = html.escape(ev.detail) if ev.detail else html.escape(ev.name)
            style = f"border-left-color:{color}"
            cls = "badge key" if ev.key else "badge"
            body.append(f'<div class="{cls}" style="{style}" title="{title}">{" ".join(parts)}</div>')

    return f'<td class="{" ".join(classes)}">{"".join(body)}</td>'


def week_total_min(week_dates: list[date], events_by_date: dict[date, list[Event]]) -> int:
    total = 0
    for d in week_dates:
        for ev in events_by_date.get(d, []):
            if ev.authored and not ev.excluded_from_budget and ev.duration_min:
                if ev.sport in ("Run", "Ride", "Walk"):
                    total += ev.duration_min
    return round(total)


def render_month(year: int, month: int, events_by_date: dict[date, list[Event]],
                  race_days: dict[date, str], weekly_budget: int | None, today: date) -> str:
    cal = calendar.Calendar(firstweekday=0)  # Monday first
    weeks = cal.monthdatescalendar(year, month)
    header_cols = "".join(f"<th>{d}</th>" for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    header_cols += '<th class="total-col">Wk total</th>'

    rows = []
    for week in weeks:
        cells = "".join(render_day_cell(d, month, events_by_date, race_days, today) for d in week)
        total = week_total_min(list(week), events_by_date)
        budget_note = f" / {weekly_budget}" if weekly_budget else ""
        over = weekly_budget is not None and total > weekly_budget
        total_cls = "total-cell over" if over else "total-cell"
        cells += f'<td class="{total_cls}">{total}{budget_note}<br><span class="unit">min</span></td>'
        rows.append(f"<tr>{cells}</tr>")

    month_name = calendar.month_name[month]
    return f"""
    <section class="month">
      <h2>{month_name} {year}</h2>
      <table>
        <thead><tr>{header_cols}</tr></thead>
        <tbody>{"".join(rows)}</tbody>
      </table>
    </section>
    """


def build_summary(events_by_date, week_labels, weekly_budget, race_days) -> str:
    """One-row-per-block-week overview: volume, longest session, key anchor session."""
    rows = []
    for wk in range(9, 20):
        start = BLOCK_WEEK_9_START + timedelta(weeks=wk - 9)
        days = [start + timedelta(days=i) for i in range(7)]
        run = walk = ride = 0.0
        longest = 0.0
        longest_name = ""
        anchors = []
        for d in days:
            for ev in events_by_date.get(d, []):
                if not ev.authored or ev.sport == "Lift":
                    continue
                if ev.excluded_from_budget:
                    if ev.sport == "Walk":
                        walk += ev.duration_min or 0
                    else:
                        ride += ev.duration_min or 0
                    continue
                if ev.kind == "race":
                    anchors.append("🏁 RACE")
                    continue
                run += ev.duration_min or 0
                if (ev.duration_min or 0) > longest:
                    longest, longest_name = ev.duration_min, ev.name
                if ev.key:
                    anchors.append(ev.name.split("—")[0].strip())
        label = week_labels.get(wk, "")
        cls = "race" if any("RACE" in a for a in anchors) else (
              "peak" if weekly_budget and run > weekly_budget * 0.78 else "")
        hrs = f"{int(longest)//60}h{int(longest)%60:02d}" if longest else "—"
        rows.append(
            f"<tr class='{cls}'><td><b>W{wk}</b></td>"
            f"<td>{start.strftime('%b %-d')}</td>"
            f"<td>{html.escape(label)}</td>"
            f"<td class='num'>{int(run)}</td>"
            f"<td class='num'>{hrs}</td>"
            f"<td class='num'>{int(walk)}</td>"
            f"<td class='num'>{int(ride)}</td>"
            f"<td>{html.escape(', '.join(dict.fromkeys(anchors))) or '—'}</td></tr>")
    return f"""
    <h2>The block at a glance</h2>
    <table class="summary">
      <thead><tr><th>Wk</th><th>Starts</th><th>Character</th><th>Run min</th>
      <th>Longest</th><th>Walk</th><th>Ride</th><th>Anchor session</th></tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table>
    """


PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>git-fit — training plan calendar</title>
<style>
  :root {{
    color-scheme: light dark;
    --bg: #ffffff; --fg: #1a1a1a; --muted: #868e96; --border: #dee2e6;
    --card: #f8f9fa; --accent: #495057;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg: #16181d; --fg: #e9ecef; --muted: #868e96; --border: #343a40; --card: #1f2228; --accent: #adb5bd; }}
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 24px; background: var(--bg); color: var(--fg);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 14px; line-height: 1.4;
  }}
  h1 {{ font-size: 22px; margin: 0 0 4px; }}
  .subtitle {{ color: var(--muted); margin: 0 0 20px; }}
  .legend {{ display: flex; flex-wrap: wrap; gap: 14px; margin-bottom: 24px; font-size: 12.5px; }}
  .legend .item {{ display: flex; align-items: center; gap: 6px; }}
  .legend .swatch {{ width: 12px; height: 12px; border-radius: 3px; display: inline-block; }}
  .legend .seed-swatch {{ width: 12px; height: 12px; border-radius: 3px; border: 1px dashed var(--muted); }}
  section.month {{ margin-bottom: 36px; overflow-x: auto; }}
  section.month h2 {{ font-size: 17px; margin: 0 0 8px; }}
  table {{ border-collapse: collapse; width: 100%; min-width: 760px; }}
  th {{ text-align: left; font-size: 11.5px; color: var(--muted); font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.03em; padding: 4px 6px; }}
  th.total-col {{ text-align: right; }}
  td.day {{
    vertical-align: top; border: 1px solid var(--border); padding: 6px;
    width: 12.5%; height: 84px; background: var(--card);
  }}
  td.day.out {{ opacity: 0.35; }}
  td.day.today {{ outline: 2px solid var(--accent); outline-offset: -2px; }}
  td.day.race {{ background: color-mix(in srgb, #c92a2a 12%, var(--card)); }}
  .daynum {{ font-size: 11.5px; color: var(--muted); margin-bottom: 3px; }}
  .badge {{
    font-size: 11px; padding: 2px 5px; margin-bottom: 3px; border-radius: 3px;
    background: color-mix(in srgb, var(--fg) 5%, var(--card));
    border-left: 3px solid var(--muted); white-space: nowrap; overflow: hidden;
    text-overflow: ellipsis;
  }}
  .badge.race-badge {{ border-left-color: #c92a2a; font-weight: 600; }}
  .badge.key {{ font-weight: 700; background: color-mix(in srgb, var(--fg) 12%, var(--card)); }}
  .badge.seed {{ color: var(--muted); border-left-style: dashed; font-style: italic; }}
  td.total-cell {{
    text-align: right; vertical-align: middle; font-size: 12.5px; color: var(--muted);
    border: 1px solid var(--border); padding: 6px; white-space: nowrap;
  }}
  td.total-cell.over {{ color: #e03131; font-weight: 600; }}
  td.total-cell .unit {{ font-size: 10px; }}
  td.total-cell .wk {{ font-weight: 700; color: var(--fg); font-size: 12px; }}
  table.summary {{ min-width: 640px; margin-bottom: 28px; }}
  table.summary th, table.summary td {{ border: 1px solid var(--border); padding: 5px 8px;
        font-size: 12.5px; text-align: left; color: var(--fg); text-transform: none;
        letter-spacing: 0; }}
  table.summary th {{ color: var(--muted); font-size: 11.5px; text-transform: uppercase; }}
  table.summary td.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
  table.summary tr.peak td {{ background: color-mix(in srgb, var(--fg) 7%, var(--card)); }}
  table.summary tr.race td {{ background: color-mix(in srgb, #c92a2a 14%, var(--card));
        font-weight: 700; }}
  footer {{ margin-top: 32px; color: var(--muted); font-size: 12px; }}
  footer code {{ background: var(--card); padding: 1px 5px; border-radius: 3px; }}
</style>
</head>
<body>
  <h1>git-fit — training plan calendar</h1>
  <p class="subtitle">{subtitle}</p>
  <div class="legend">
    <span class="item"><span class="swatch" style="background:#2f9e44"></span>Run</span>
    <span class="item"><span class="swatch" style="background:#1971c2"></span>Ride (meeting time)</span>
    <span class="item"><span class="swatch" style="background:#e8590c"></span>Walk (meeting time)</span>
    <span class="item"><span class="swatch" style="background:#9c36b5"></span>Lift</span>
    <span class="item"><span class="swatch" style="background:#c92a2a"></span>Race day</span>
    <span class="item"><span class="seed-swatch"></span>Old Runna plan, outside this block</span>
  </div>
  {summary}
  {months}
  <footer>
    Generated by <code>scripts/generate_calendar.py</code> from
    <code>endurance/</code>, <code>strength/program.liftoscript</code>,
    <code>seed/runna-plan.ics</code>, and <code>races/</code>. Rerun any time the plan changes —
    this page reads the repo, it never writes to it. Week totals count Run/Ride/Walk minutes
    only, excluding meeting-time sessions, matching the check in <code>rules/progression.md</code>.
  </footer>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent,
                    help="repo root (default: parent of scripts/)")
    ap.add_argument("--out", type=Path, default=None,
                    help="output HTML file (default: <root>/calendar.html)")
    args = ap.parse_args()
    root: Path = args.root
    out: Path = args.out or (root / "calendar.html")

    endurance = load_endurance_events(root)
    strength = load_strength_events(root)
    race_days = load_race_days(root)
    weekly_budget = load_weekly_budget(root)

    covered = {e.date for e in endurance} | set(race_days.keys())
    seed = load_seed_placeholders(root, covered)

    all_events = endurance + strength + seed
    events_by_date: dict[date, list[Event]] = {}
    for ev in all_events:
        events_by_date.setdefault(ev.date, []).append(ev)
    for d in events_by_date:
        events_by_date[d].sort(key=lambda e: (not e.authored, e.sport))

    all_dates = list(events_by_date.keys()) + list(race_days.keys())
    months = month_span(all_dates)
    today = date.today()

    months_html = "".join(
        render_month(y, m, events_by_date, race_days, weekly_budget, today) for y, m in months
    )

    n_authored = sum(1 for e in endurance)
    n_seed = len(seed)
    subtitle = (
        f"{n_authored} authored sessions, {len(strength)} lifting days, {n_seed} untouched Runna "
        f"seed dates. Race: {next(iter(race_days.values()), '?')}, "
        f"{next(iter(race_days.keys()), '?')} 9:00 AM."
    )

    summary_html = build_summary(events_by_date, load_week_labels(root), weekly_budget, race_days)
    out.write_text(PAGE_TEMPLATE.format(subtitle=html.escape(subtitle),
                                       summary=summary_html, months=months_html))
    print(f"Wrote {out} ({len(all_events)} events across {len(months)} month(s))")


if __name__ == "__main__":
    main()
