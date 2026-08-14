# Strength authoring — Liftoscript reference + house rules

`strength/program.liftoscript` is one file, the whole Liftosaur program, pushed via the Liftosaur
MCP. This is the syntax reference plus the athlete's own scheduling spec, which is a hard constraint
— not a preference — whenever it conflicts with anything else in this repo except the running plan.

## House rules — verbatim from the athlete's spec, hard constraints

- **4-day split: Upper A / Lower A / Upper B / Lower B.** Sessions 45–60 minutes. Weights in **lb**.
- **High-quality running workouts and long runs outrank lifting performance, always.**
- **Lower A** is the primary lower-body strength day — schedule it as far from the weekly long run
  as practical.
- **Lower B** is runner-specific and deliberately low-fatigue: unilateral strength, stability,
  calves, hamstrings, core, injury prevention. It must leave the legs fresh for key runs.
- **Pair upper-body days with running days** to consolidate fatigue and create genuinely complete
  recovery days.
- **Never schedule heavy lower-body lifting the day before a long run**, or the day before a quality
  session (tempo, intervals, hills), whenever avoidable.
- **One complete leg recovery day immediately before every long run.** At least one true recovery
  day every week (mobility, stretching, walking, or full rest).
- **If recovery becomes a concern, reduce lifting volume before reducing running quality.**
- **On unavoidable conflicts, the running plan wins.**
- **On doubled days, lifting is always placed after the run.**

**The cut order has ONE direction, and it does not flip on the trigger — clarified 2026-08-13
after the athlete caught a session file saying the opposite.** Lifting is cut before running,
whatever prompted the decision:

| trigger | what gets cut |
|---|---|
| time is short | the lift (`athlete/profile.md` § "Priority when time is short") |
| recovery is a concern | the lift ("reduce lifting volume before reducing running quality") |
| readiness amber/red | lift tiers drop first (`rules/progression.md`) |
| **a tissue is talking** — calves, achilles, arches | **the lift, or at least the exercise loading that tissue** |

The last row is the one that had drifted. Eight Thursday session files carried a note saying that
if calves or achilles were talking, the *run* should be cut and the lift kept — introduced in one
commit with no rationale, never traced to the spec above, and flatly contradicting two of its
verbatim lines. Corrected in all eight.

If a reason ever emerges to protect a lift over a run — a rehab protocol, say, where controlled
loading is the treatment and impact is the provocation — that is a decision for the athlete to
make explicitly and for this file to record. **It is not something a session file gets to assert
on its own.**

See `training/block.md` § "The weekly template" for how this resolves against the Champion Plan's
day pattern and the Friday blackout — Mon=Lower A, Tue=Upper A, Thu=Lower B, Sun=Upper B, Wed/Fri/Sat
carry no lifting.

## Liftoscript syntax reference

Full docs: `liftosaur.com/doc/liftoscript`. The essentials used in this repo:

- **Structure:** `# Week N` headings, `## Day Name` subheadings. One program text covers the whole
  block — Liftoscript weeks are numbered independently of calendar/block weeks; the offset is
  recorded in `training/block.md` (block week 9 = Liftoscript Week 1).
- **Exercise line:** `label: Exercise Name / sets×reps / weight / restTimer / progress: fn(...)`,
  sections separated by `/`, any order after the exercise name.
- **Labels:** `main:`, `accessory:`, `core:` — free text, used for organization/filtering.
- **Sets×reps:** `3x5` (3 sets of 5); multiple schemes comma-separated: `1x5, 1x3, 1x1`; rep ranges
  `3x8-12`; AMRAP with trailing `+`: `1x5+`.
- **Weight:** absolute (`185lb`), or `bodyweight` for unloaded work.
- **Rest timer:** plain seconds, e.g. `180s`.
- **Progression functions:**
  - `progress: lp(increment, [attempts, currentAttempt, decrementPct, decrementAttempts])` — linear
    progression. `lp(5lb, 1, 0, 10%, 1)` = add 5lb every session; after 1 failed attempt, drop 10%.
  - `progress: dp(increment, minReps, maxReps)` — double progression: add reps within the range
    before adding weight.
  - `progress: sum(repsThreshold, increment)` — sum-of-reps progression.
  - `progress: custom(...) {~ ... ~}` — full script, not used in this program; prefer `lp`/`dp`.
- **Set variations (autoregulation):** multiple set schemes separated by `/`, current one marked
  `!`: `3x5 / ! 2x5 / 1x5`. Switch which is active by editing the `!` position — this is the
  readiness ladder, see `rules/progression.md`.
- **Timers on holds:** `setTimer|restTimer`, e.g. `3x30s|30s` for a 30s hold with 30s rest.
- **Warmup sets:** `warmup: 1x5 45lb, 1x5 135lb` or `warmup: none`.
- **Descriptions:** `// visible text` (user-facing), `/// hidden text` (internal note).

## Autoregulation via set variations

Every **main** lift carries three tiers, `!` marking the currently active one — this is the
mechanical implementation of "reduce lifting volume before reducing running quality":

```
main: Squat / ! 3x5 / 2x5 / 1x5 / 185lb / 180s / progress: lp(5lb, 1, 0, 10%, 1)
```

- **Tier 1** (`3x5`, full) — green day: fresh, no conflicting session in the next 24h.
- **Tier 2** (`2x5`, reduced) — amber: general fatigue, or a quality session tomorrow that isn't
  directly conflicting.
- **Tier 3** (`1x5`, minimal) — red: high fatigue, or this session sits the day before a long run —
  present but doesn't add meaningful load.

`rules/progression.md` has the readiness check that selects the tier each session. Accessory and
core work doesn't carry variations — cut those first, and entirely, before touching a main lift's
tier.

## What's in the current program

See `strength/program.liftoscript` for the live file and `strength/notes.md` for exercise
substitutions/equipment notes. Week 1 there corresponds to block week 9 (2026-08-03).
