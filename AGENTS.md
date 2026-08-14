# AGENTS.md — how to operate this repo

This repo has no compiler and no CI. You (an LLM, in a future session) are the only thing that
turns intent into files. This document is the entry point: what to read, in what order, and the
invariants you must never violate.

## Read order, before touching anything

1. `athlete/profile.md` — the time budget. Every session you author is checked against this.
2. `races/2026-10-17-ghost-train.md` — what the race actually is, and the goal tiers.
3. `training/block.md` — the policy: block-week ↔ Champion-week mapping, the weekly template, and
   the numbered reshaping rules. This is the thing you're implementing every time you author a week.
4. The specific `training/weeks/wNN.md` you're working on, if it already exists.
5. `rules/endurance-authoring.md` and `rules/strength-authoring.md` — syntax references. Read these
   immediately before writing any endurance or strength file; the gotchas in them (especially the
   `m` = minutes trap) are easy to get wrong from memory.
6. `rules/progression.md`, `rules/fueling.md`, `rules/logging.md`, `rules/conditions.md` and
   `rules/trail-classification.md` as needed for the specific decision at hand.

`seed/` is historical input only — read it for context (what paces the athlete was already hitting,
what the professionally designed plan says), never edit it, never treat it as current instruction.

## Hard invariants — never violate these

1. **The time budget in `athlete/profile.md` is a hard constraint, not a target.** Before finalizing
   any week, sum `duration_s` across that week's `endurance/*.md` files (excluding anything with
   `concurrent: meetings`) and confirm it's within `weekly_total_max_min`. If it isn't, cut — in
   order: strength volume (drop to a lower set-variation tier, or drop Upper B first) → doubles →
   easy volume → quality → long run. The long run and the Saturday/Sunday back-to-back are cut last.
1b. **A long run may exceed `long_run_max_min` only with an explicit `budget_exception: <reason>`
   in its frontmatter**, and no more than `long_run_exceptions_per_block` sessions may carry one.
   Never raise the cap globally to make a session fit — flag the session instead, so going long
   stays rare and visible. `scripts/verify_plan.py` enforces both the flag and the count.
2. **Running always wins conflicts with lifting**, per the user's own strength spec in
   `rules/strength-authoring.md`. Never schedule heavy lower-body work the day before a long run or
   a quality session. Never let a lift compromise Wednesday's big workout or the weekend.
3. **`m` in intervals.icu syntax means minutes, not meters.** Use `mtr` for meters or express as km.
   This is the single most common way to silently corrupt a workout — check every endurance file
   you write for a bare `m` that was meant to mean meters.
4. **Every session states which instrument to follow.** The `follow:` field is required and is
   what the athlete actually reads on the day. Derive it from the session's *binding* rep length —
   the shortest work interval inside a repeat block — because ZoneSense (DFA a1) needs a rolling
   ~2min window and simply cannot track shorter efforts. ≥9min → pace + ZoneSense cross-check;
   3–9min → pace, ZoneSense lags; <3min → pace only. Easy/long/race work is always ZoneSense
   Zone 1. See `rules/endurance-authoring.md`.
5. **Long/ultra-effort sessions use `target_mode: hr` or `effort`, never `pace`.** Pace targets are
   for sessions under ~2h. This is the fix for Runna's core mistake (prescribing marathon pace for a
   multi-hour ultra effort).
6. **Never invent a race distance or pace target that contradicts `races/2026-10-17-ghost-train.md`.**
   The Runna seed's `50km at 5:35-5:55/km` is wrong and stays discarded.
7. **Frontmatter `published.suunto` is the only idempotency mechanism.** Don't re-push a session
   whose body hasn't changed since it was last published. See `rules/publishing.md`.
8. **Anything pulled from the Suunto API is DRAFT until the athlete confirms it.** The numbers are
   real, but the *interpretation* usually isn't obvious from the data alone — a fragmented night
   might be a sick kid or a watch artifact; a low HRV reading might be alcohol, illness, or noise;
   a "hard" session might have had a deliberate effort inside it. Present Suunto-derived findings
   and their proposed reading to the athlete BEFORE committing them as fact, and record the context
   they give alongside the number. Two corrections already came from exactly this: the 08-02 30k
   initially read as chronic mis-pacing (it was a deliberate 10k plus 86F heat), and treadmill data
   was briefly written off as unreliable (it reconciled perfectly once walking was separated out).
   **Ambient conditions are the one piece of that context now available without asking** — run
   `scripts/heat_load.py` on any outdoor session before interpreting how hard it was
   (`rules/conditions.md`). The watch's own temperature field is body heat off the wrist and is
   never ambient; believing it is what produced the second correction above.
9. **`seed/*` files are frozen.** If something from Runna or the Champion Plan needs to change for
   this athlete, make the adapted version in `training/`, `endurance/`, or `strength/` — don't edit
   the seed.

## Typical workflows

**Authoring a new week** (`training/weeks/wNN.md` doesn't exist yet):
1. Look up the block-week → Champion-week mapping in `training/block.md` to know which Champion
   week's shape to use.
2. Apply the weekly template (Mon–Sun day pattern) from `training/block.md`.
3. Write one `endurance/YYYY-MM-DD-<slug>.md` per running/riding/walking session for that week,
   following `rules/endurance-authoring.md`.
4. Confirm which Liftoscript `# Week N` corresponds to this block week (offset is fixed: block week
   9 = Liftoscript Week 1), and check `strength/program.liftoscript` already covers it — if not,
   append it following `rules/strength-authoring.md`.
5. Write `training/weeks/wNN.md` linking everything and stating the week's intent, referencing the
   verification checks below.
6. Run the invariant checks (time budget, lifting placement, `m`-for-meters).

**Recording a day** (the athlete reports how a session went, or a Suunto pull needs interpreting):
write or update `log/YYYY-MM-DD.md` per `rules/logging.md` — copy `log/TEMPLATE.md`, fill only what
was actually reported, and **never backfill a rating the athlete didn't give you**. Soreness,
session-RPE and `shade_pct` are the three signals nothing else can supply; everything else the
watch already knows and should not be retyped by hand. If the session was outdoors, fill the
`conditions:` block with the script rather than by hand or by asking:

```bash
python3 scripts/heat_load.py --workout-json <workout.json> --write   # rules/conditions.md
```

If the session was on trails, the activity type on the watch is not evidence of what the legs did —
a `TRAIL_RUNNING` file can be a summit hiked at walking cadence. `scripts/classify_activity.py`
separates the two questions (was it one sustained climb; was it run or walked) from the elevation
and cadence streams. Its labels are draft like any other Suunto-derived reading — see
`rules/trail-classification.md`, which is candid about being fitted to four activities.

```bash
python3 scripts/classify_activity.py --workout-json <workout.json> --explain
```

**Adjusting a week from `log/` feedback** (fatigue, missed session, illness, an unplanned group
ride or eMTB spin): re-read `rules/progression.md` for the cut order and the unplanned-session
handling rules in `training/block.md`, then edit the affected `endurance/*.md` files in place
(don't create duplicates) and update `published.suunto` handling per `rules/publishing.md` if a
file that was already pushed changes.

**Publishing**: see `rules/publishing.md`. Push a rolling ~2-week window, not the whole plan at
once — the plan is meant to adapt to how training actually goes.

## Verification — run the script

```bash
python3 scripts/verify_plan.py
```

It checks the mechanical invariants against `athlete/profile.md` (nothing is hardcoded) and exits
non-zero on failure: weekly running-time budget, per-session and long-run caps, the night-session
cap, the walking ramp limit, the `m`-means-minutes trap, rest steps missing a target, long sessions
wrongly using `target_mode: pace`, and malformed frontmatter. Run it after authoring or editing any
week.

It also validates `log/` (`rules/logging.md`) and prints the recent readiness/soreness/RPE readout.
Malformed log data is an error; a *missing* rating is only ever a warning — a blank field is a
legitimate answer, and failing the build over one would just teach the athlete to ignore the
script. The warnings worth reading are RPE running over plan for the session type (easy-day creep)
and two consecutive amber/red calls, which is a re-author trigger, not a note.

It checks the `conditions:` blocks too (`rules/conditions.md`). The one to take seriously is **an
over-plan RPE on a day whose WBGT was red or black** — that reads as heat, not fitness, and is the
exact mistake this repo has already made twice. Don't re-author a week off a hot session alone.

Then eyeball the two things a script can't judge:

- [ ] No heavy lower-body lift precedes a long run or Wednesday's big workout, and Friday is still
      a true rest day (the placement rules in `rules/strength-authoring.md`)
- [ ] Sessions carrying `time_critical:` still have their timing intact; everything else is
      free to move within the day — do not impose clock times on ordinary runs

```bash
python3 scripts/generate_calendar.py   # visual overview of the whole block
python3 scripts/heat_load.py --history # what heat and shade have actually cost this athlete
```
