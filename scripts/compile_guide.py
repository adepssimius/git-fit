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
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# `owner` and `url` must both be PRESENT: omitting them returns HTTP 400
# "Instantiation of ... Guide$Sequence value failed", because the server's deserialiser treats
# them as required creator properties.
#
# The VALUE of `owner` behaves differently on the two write paths, observed directly:
#   create (POST) -> server overwrites it with "Suunto" no matter what was sent
#   update (PUT)  -> server stores what was sent (a guide created here came back as "git-fit")
# So a guide's owner changes the first time it is updated. Nothing depends on it, but don't be
# surprised by the inconsistency in guides_list. `url` is stored as sent on both paths.
OWNER = "git-fit"
URL = "https://github.com/local/git-fit"

# Text and structure limits. The first five are the watch renderer's own caps — enforce them here
# rather than discovering them as a mangled screen mid-session.
MAX_STEP_TITLE = 13
MAX_FIELD_TITLE = 9
MAX_STATIC_TEXT = 54
MAX_STEPS = 1000
MAX_REPEAT_TIMES = 100
# The description cap is a CONSERVATIVE GUESS, not a measured limit. Descriptions of 237 and 249
# chars have been accepted and round-tripped back intact through guides_list; the real ceiling has
# never been probed. If a session genuinely needs more room, test it rather than trusting 256.
MAX_DESCRIPTION = 256

# Activity ids confirmed via suuntool activity_type_name.
RUNNING, TRAIL_RUNNING, TREADMILL, CYCLING = 1, 22, 53, 2

# Sports each guide offers itself for. The FIRST entry drives pace-vs-speed display, so RUNNING
# leads. Running sessions offer all three because the plan spans all three surfaces — uphill
# treadmill threshold work, rail-trail sessions on the real course, ordinary road running — and a
# guide restricted to RUNNING simply would not appear if the watch was started in Treadmill or
# Trail running mode. Offering all three costs nothing and removes a whole class of "where did my
# workout go" on the morning of a session.
ACTIVITIES = {
    "Run": [RUNNING, TRAIL_RUNNING, TREADMILL],
    "Ride": [CYCLING],
}
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


def parse_target(rest: str, zones: dict, rel: str) -> dict | None:
    """The target portion of a step line -> a target field in wire units, or None.

    None means "display only": the step shows pace and HR as data and asserts no target. That is
    the honest encoding for ZoneSense-governed running, because the wire format has no ZoneSense
    target — its target fields are pace, HR, power and cadence, and ZoneSense is a separate Zapp
    the guide cannot drive. Putting a pace target on such a step invents a second, contradictory
    instrument: on rolling terrain it fires on descents, where speed is aerobically free.
    """
    rest = rest.strip()

    # `ZoneSense Z1` — governed by ZoneSense, which the format cannot express. The instruction
    # lives in the guide description; the watch's own ZoneSense alarm does the enforcing.
    if re.match(r"^ZoneSense\s+Z[1-3]$", rest, re.I):
        return None

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
    """Fold typographic punctuation to ASCII before anything reaches the watch.

    Defensive rather than proven: the markdown is full of em-dashes and curly quotes, and the
    watch renderer's unicode handling is untested. Folding costs nothing and removes a whole
    class of "why is there a box character in my workout name" — but if a session ever genuinely
    needs a non-ASCII character, test it before assuming this is why it failed.
    """
    for a, b in (("\u2014", "-"), ("\u2013", "-"), ("\u2019", "'"),
                 ("\u201c", '"'), ("\u201d", '"'), ("\u2192", "->"), ("\u00b0", "deg")):
        s = s.replace(a, b)
    return s


# --------------------------------------------------------------------------- step titles
#
# The watch caps a step title at 13 characters, which is far too short for the descriptive
# headers the markdown wants to carry ("Easy to a hill", "Car -> north terminus (drop bag passed
# at 5km)"). Rather than force cryptic headers into the source files — which would make the plan
# harder to read for the one reason that matters least — the repo keeps prose headers and this
# table renders them into a fixed watch vocabulary.
#
# Two properties worth preserving if this is extended:
#   * The tokens are a CLOSED vocabulary. A handful of short words, reused everywhere, is
#     learnable in a session or two and readable at a glance at hour 20. Ad-hoc abbreviations
#     are not — "STR" could be strides, steady or straight.
#   * Rep counts are dropped ("Hill Strides 5x" -> STRIDE). The watch shows rep progress itself,
#     so repeating it in the title spends scarce characters on information already on screen.
#
# First match wins, so specific patterns precede general ones. `\1` backreferences are expanded.
TITLE_RULES: list[tuple[str, str]] = [
    (r"^warm\s*up",                     "Warm up"),
    (r"^cool\s*down",                   "Cool down"),
    (r"^easy\s*(to|>)\s*hill",          "EZ>HILL"),
    (r"^easy\s*/\s*mod",                "EZ/MOD"),
    # Athlete-directed, 2026-08-04: ZoneSense-governed easy running carries NO compiled target,
    # including through the ~10min cold start. The label states the intent and the athlete paces
    # the opening himself. See rules/endurance-authoring.md § "The cold-start opener".
    (r"^easy\s+aerobic",                "Easy aerobic"),
    (r"^easy",                          "Easy"),
    (r"^moderate",                      "MOD"),
    (r"^steady",                        "Steady"),
    (r"^z2\s*base",                     "Z2 BASE"),
    (r"^progression",                   "PROG"),
    # Must precede the strides rule — otherwise "Hill strides positioning" matches it and the
    # positioning step and the strides themselves both render as STRIDE.
    (r"^(hill\s+strides\s+)?positioning", "FIND HILL"),
    (r"^(hill\s+)?strides",             "STRIDE"),
    (r"^hills",                         "HILL"),
    (r"^(long|short)\s+threshold",      "Threshold"),
    (r"^threshold",                     "Threshold"),
    (r"^surges",                        "SURGE"),
    (r"^pickups",                       "PICKUP"),
    (r"^main\s+set",                    "REP"),
    (r"^run\s*/\s*walk",                "R/W"),
    (r"^night\s+steady",                "NGT STEADY"),
    (r"^night\s+blocks",                "NGT BLOCK"),
    (r"^wake-?\s*up",                   "WAKE UP"),
    (r"^settle\s+in",                   "SETTLE"),
    (r"^recovery",                      "Recovery jog"),
    # Course geography — lap sims and the Big Day
    (r"^(car\s*[-—>]*\s*)?crew\s+stop", "CREW"),
    (r"^car\b.*crew",                   "CREW"),
    (r"^turnaround",                    "TURN"),
    (r"^car\s*->\s*north",              "OUT>NORTH"),
    (r"^north\s+terminus\s*->\s*car",   "BACK>CAR"),
    (r"^car\s*->\s*south",              "OUT>SOUTH"),
    (r"^out-and-back\s*(\d+)",          r"O&B \1"),
    (r"^top-?up",                       "TOP-UP"),
    # Race day
    (r"^laps?\s+([\d-]+)",              r"LAP \1"),
    (r"^hard\s+finish",                 "HARD FIN"),
    (r"^dawn\s+finish",                 "DAWN FIN"),
]


def step_title(raw: str, fallback: str) -> str:
    """A markdown section header -> a watch-safe step title, via the closed vocabulary above."""
    head = ascii_fold(re.sub(r"\s*\d+x$", "", raw)).strip()
    if not head:
        return fallback[:MAX_STEP_TITLE]

    # Match against the WHOLE header — the distinguishing word often sits past a dash
    # ("Car - crew stop, sock change" is a CREW stop, not a "Car"). The token replaces the
    # header outright; only explicit \1 backreferences carry anything through.
    for pattern, token in TITLE_RULES:
        m = re.match(pattern, head, re.I)
        if m:
            return m.expand(token).strip()[:MAX_STEP_TITLE]

    # Unmapped: headers explain themselves after a dash ("Turnaround - drop-bag check"), and
    # that explanation belongs in the brief rather than on a 13-character watch screen.
    head = head.split(" - ")[0].strip()
    if len(head) > MAX_STEP_TITLE:
        # A silently clipped title is how "Easy to a hill" reached the watch as "Easy to a hil".
        print(f"warning: step title '{head}' has no TITLE_RULES entry and exceeds "
              f"{MAX_STEP_TITLE} chars — add a token or shorten the header", file=sys.stderr)
    return head[:MAX_STEP_TITLE].strip()


# Suunto's phase vocabulary, taken from Workout Planner output. The watch keys its display and
# its notification screens off these, so a step without one renders as nothing useful.
PHASE_WARMUP, PHASE_INTERVAL, PHASE_REST, PHASE_COOLDOWN = "warmUp", "interval", "rest", "coolDown"

# Deterministic UUIDs. Suunto emits random v4s, but this packer must be byte-stable — the whole
# idempotency mechanism in rules/publishing.md is a sha256 of the archive, and a fresh uuid per
# compile would make every session look changed on every run.
_UUID_NS = uuid.UUID("6b1f4a2e-1c3d-4e5f-8a9b-0c1d2e3f4a5b")


def step_uuid(seed: str) -> str:
    return str(uuid.uuid5(_UUID_NS, seed))


def phase_for(header: str, is_rest: bool) -> str:
    """Map a section header to a Suunto phase. Rest steps inside a repeat are `rest`."""
    if is_rest:
        return PHASE_REST
    h = header.lower()
    if h.startswith(("warm", "easy aerobic")) or "warmup" in h:
        return PHASE_WARMUP
    if h.startswith("cool"):
        return PHASE_COOLDOWN
    return PHASE_INTERVAL


def _fmt_pace(target: dict | None) -> str:
    """{'min': m/s, 'max': m/s} -> "7'00 - 7'30 /km", matching Suunto's notification text."""
    if not target or target.get("type") != "targetPace":
        return ""
    def clock(mps):
        s = round(1000 / mps)
        return f"{s // 60}'{s % 60:02d}"
    return f"{clock(target['max'])} - {clock(target['min'])} /km"


def _fmt_amount(step: dict) -> str:
    """The distance or duration of a compiled step, as Suunto writes it in a notification."""
    for f in step["fields"]:
        if f["type"] == "stepDistanceCountdown":
            return f"{f['value'] / 1000:.2f} km"
        if f["type"] == "stepDurationCountdown":
            s = int(f["value"])
            return f"{s // 60}'{s % 60:02d}"
    return ""


def notification_step(title: str, text: str) -> dict:
    return {"type": "notification", "title": title,
            "fields": [{"type": "text", "value": text}]}


def describe(entry: dict) -> str:
    """Preview text for the notification that precedes a block."""
    if entry["type"] == "repeat":
        inner = entry["steps"]
        work = f"{entry['times']} x {_fmt_amount(inner[0])}"
        tgt = next((f for f in inner[0]["fields"] if f["type"].startswith("target")), None)
        rest = f"\n {_fmt_amount(inner[1])}" if len(inner) > 1 else ""
        return f"{work}{rest} {_fmt_pace(tgt)}".rstrip()
    tgt = next((f for f in entry["fields"] if f["type"].startswith("target")), None)
    return f"{_fmt_amount(entry)} {_fmt_pace(tgt)}".rstrip()


def build_step(line: str, title: str, zones: dict, rel: str, hr_first: bool,
               phase: str = "interval", uid_seed: str = "") -> dict:
    """One `- <duration|distance> <target>` line -> one `fields` screen."""
    m = re.match(r"^-\s+(\S+)\s+(.*)$", line.strip())
    if not m:
        raise CompileError(f"{rel}: cannot parse step '{line.strip()}'")
    token, rest = m.group(1), m.group(2)

    # `until-lap` — the step ends ONLY on a lap press, never on its own clock or distance.
    # For a step whose end depends on the terrain rather than the numbers ("run easy until you
    # reach a hill, then start the strides"), an automatic trigger fires in the wrong place, and
    # the block that follows begins wherever the athlete happens to be standing.
    until_lap = bool(re.search(r"\buntil-lap\b", rest))
    rest = re.sub(r"\buntil-lap\b", "", rest).strip()

    dur = parse_distance(token) or parse_duration(token)
    if dur is None:
        raise CompileError(f"{rel}: '{token}' is neither a duration nor a distance")

    cadence = parse_cadence(rest)
    rest_no_cadence = re.sub(r"\s*\d+(-\d+)?rpm", "", rest).strip()
    # A cadence-only step (trainer work) carries no other target; anything else must resolve,
    # and parse_target raises rather than guessing.
    target = parse_target(rest_no_cadence, zones, rel) if rest_no_cadence else None

    if dur["kind"] == "time":
        trigger_inner = {"type": "stepDuration", "value": dur["seconds"]}
        countdown = {"type": "stepDurationCountdown", "value": dur["seconds"]}
    else:
        trigger_inner = {"type": "stepDistance", "value": dur["meters"]}
        countdown = {"type": "stepDistanceCountdown", "value": dur["meters"]}

    fields: list[dict] = []
    if target:
        # Suunto labels the target field "target". Mine had no title at all.
        target = {**target, "title": "target"}
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

    # Default: "press lap to skip early" — the standard pattern, and the only way a step that
    # overruns its distance on a wrong turn doesn't strand the athlete mid-session. With
    # `until-lap` the automatic half is dropped entirely and only the lap press ends the step;
    # the countdown field stays, so the nominal distance is still visible as a progress cue
    # rather than as a deadline.
    trigger = ({"type": "manualLap"} if until_lap
               else {"type": "or", "triggers": [trigger_inner, {"type": "manualLap"}]})

    # Key order and key names below mirror a guide built in Suunto's own Workout Planner and
    # downloaded on 2026-08-06 (see rules/publishing.md § "The reference implementation").
    # Everything here was absent from the hand-rolled version this replaced, which is why the
    # watch could run a guide — laps fired, titles logged — while rendering nothing on screen.
    step = {
        "type": "fields",
        # NOT `createManualLap: True`. That key does not appear anywhere in Suunto's output; it
        # was invented. The real shape is a `lap` object.
        "lap": {"type": "manual", "hidden": True},
        "trigger": trigger,
        "title": title,
        "fields": fields,
    }
    if phase in ("interval", "rest"):
        step["notification"] = {"type": "default"}
    step["extensions"] = {"com.suunto": {"phase": phase,
                                         "isCustomNameSet": False,
                                         "uuid": step_uuid(uid_seed)}}
    step["phase"] = phase
    # `alerts` is what drives the on-screen prompt and countdown. An `until-lap` step has no
    # automatic condition to alert on, so it gets none.
    if not until_lap:
        step["alerts"] = [{"type": "default",
                           "condition": dict(trigger_inner),
                           "countdown": {"type": "standard"}}]
    return step


def compile_session(path: Path, zones: dict | None = None) -> dict:
    zones = zones or load_zones()
    rel = path.name
    fm, body = parse_frontmatter(path.read_text())

    for key in ("date", "sport", "name", "type"):
        if key not in fm:
            raise CompileError(f"{rel}: missing frontmatter `{key}`")
    if fm.get("publish", "").lower() == "false":
        raise CompileError(f"{rel}: marked `publish: {fm['publish']}` — not a watch guide")
    if fm["sport"] not in ACTIVITIES:
        raise CompileError(f"{rel}: no activity id mapped for sport '{fm['sport']}'")

    hr_first = fm.get("target_mode") == "hr"
    steps: list[dict] = []
    pending: list[str] = []
    header, repeat_times = "", 0
    last_phase = None

    def flush():
        nonlocal pending, repeat_times, last_phase
        if not pending:
            return
        if repeat_times > MAX_REPEAT_TIMES:
            raise CompileError(f"{rel}: repeat x{repeat_times} exceeds {MAX_REPEAT_TIMES}")
        repeating = repeat_times > 1
        title = step_title(header, f"Step {len(steps) + 1}")
        built = []
        for i, ln in enumerate(pending):
            # Inside a repeat the second step is the recovery — Suunto phases it `rest`.
            is_rest = repeating and i > 0
            built.append(build_step(ln, "Recovery jog" if is_rest else title, zones, rel, hr_first,
                                    phase=phase_for(header, is_rest),
                                    uid_seed=f"{path.stem}:{len(steps)}:{i}"))
        if repeating:
            # `repeatNumberPreferred` is what makes the watch count reps ("3/7") instead of
            # showing an anonymous step. Suunto sets it on the WORK step only, not the recovery.
            built[0]["options"] = {"repeatNumberPreferred": True}
            entry = {"type": "repeat", "times": repeat_times, "steps": built,
                     "extensions": {"com.suunto": {"uuid": step_uuid(f"{path.stem}:rep:{len(steps)}")}}}
        else:
            entry = None

        # A notification screen precedes each PHASE CHANGE, not each step — that is how Suunto
        # does it, and it is why a 5-block workout compiles to 8 steps. A repeat gets one
        # notification summarising the whole set.
        phase = phase_for(header, False)
        if phase != last_phase or repeating:
            preview = describe(entry or built[0])
            steps.append(notification_step(title, preview))
        last_phase = phase

        steps.append(entry) if entry else steps.extend(built)
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

    # Suunto closes every guide with a triggerless `finished` step. The watch already writes
    # "SuuntoPlus(tm) guide ended" into the lap notes without it, but the step is what puts a
    # closing screen on the display rather than leaving the last interval up.
    steps.append({
        "type": "fields",
        "lap": {"type": "manual", "hidden": True},
        "title": "Finished",
        "fields": [{"type": "text", "value": "SuuntoPlus\u2122 guide ended"}],
        "notification": {"type": "default"},
        "extensions": {"com.suunto": {"phase": "finished"}},
        "phase": "finished",
    })
    total = sum(s["times"] * len(s["steps"]) if s["type"] == "repeat" else 1
                for s in steps if s["type"] != "notification")
    if total > MAX_STEPS:
        raise CompileError(f"{rel}: {total} steps exceeds the {MAX_STEPS} limit")

    # The guide description is the only prose that reaches the watch, and it is `brief:` followed
    # by `follow:` — what is going to happen, then what to obey while it does. They are joined
    # rather than duplicated: if each field restated the other's content, the two would drift the
    # first time one was edited alone.
    #
    # `brief:` is still being rolled out, so a file with only `follow:` degrades to the old
    # behaviour rather than failing. `intent:` is the last resort — it is written for the repo,
    # not the athlete, but an empty description errors the push outright.
    parts = [ascii_fold(fm.get(k, "")).strip() for k in ("brief", "follow")]
    description = " ".join(p for p in parts if p) or ascii_fold(fm.get("intent") or fm["name"])
    if len(description) > MAX_DESCRIPTION:
        print(f"warning: {rel}: brief: + follow: is {len(description)} chars, truncated to "
              f"{MAX_DESCRIPTION} — trim one, or move reasoning into intent:", file=sys.stderr)
        description = description[:MAX_DESCRIPTION]

    # Key order mirrors a known-good compile of this format. Order doesn't affect parsing, but
    # it keeps a diff against a reference guide readable.
    return {
        "name": ascii_fold(fm["name"])[:60],
        "description": description,
        "shortDescription": ascii_fold(fm["name"])[:23],
        "localDate": fm["date"],
        "type": "sequence",
        "activities": ACTIVITIES[fm["sport"]],
        "usage": "workout",
        "owner": OWNER,
        "url": URL,
        "externalId": f"git-fit-{path.stem}"[:64],
        "steps": steps,
    }


# --------------------------------------------------------------------------- cli

def selftest() -> int:
    """Compile against a golden fixture.

    This is a REGRESSION test, not a correctness proof — the fixture was generated by this
    compiler, so it can only tell you the output changed, never that the output is right. What
    grounds it is that this exact guide was accepted by the Suunto server and rendered on the
    watch, so the shapes it locks in (trigger structure, field order, countdown types, repeat
    nesting, the m/s pace inversion) are known-good rather than merely self-consistent.

    Regenerate deliberately, never reflexively: `compile_guide.py <session> > <fixture>` after a
    change you meant to make. Regenerating to silence a failure discards the only thing here that
    has actually been on a watch.
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
