# Strength notes — substitutions, equipment, cues

## Live in Liftosaur

Pushed via the Liftosaur MCP (`mcp__liftosaur__update_program`, id `haqytaxt`) as **"Ghost Train
Block"** — this replaced the athlete's pre-existing "My Program 2" (a general machine/dumbbell
hypertrophy split, unrelated to this training block; confirmed with the athlete before
overwriting). Re-push this file with the same tool whenever it changes; `strength/program.liftoscript`
is the source of truth, the app is the execution surface.

## Week ↔ block-week offset

Liftoscript `# Week 1` = block week 9 (2026-08-03). To find the Liftoscript week for any block
week: `liftoscript_week = block_week - 8`.

**Every week is fully self-contained — do not rely on Liftoscript's carry-forward mechanism
(leaving a `## Day` header empty to inherit the previous week's exercise).** Tested extensively via
`run_playground` with real chained execution — Week 1 completed for real
(`complete_set()`+`finish_workout()`), then Week 2 simulated from the resulting
`updatedProgramText` — and Week 2 still returned "Exercise not found." Reproduced across six
separate test constructions, including one built directly from the Liftoscript reference's own
documented example. Root cause unconfirmed (simulator limitation vs. real engine behavior), but a
live session showing 0lb or a missing exercise isn't a risk worth taking.

**So: when appending a new week, write out every exercise explicitly** (weight, sets, reps —
nothing omitted), copying the previous week's structure and applying that week's
readiness/taper adjustments from `rules/progression.md` and `training/block.md`. Spot-check the
result with `run_playground` (`complete_set` + inspect the returned weight) before pushing,
especially for any week with a structural change (taper, dropped day, resumed day) — those are
exactly the cases most likely to silently break.

## Starting weights are estimates, not measured maxes

Squat, Romanian Deadlift, Bench Press, Bent Over Row, Overhead Press, Pull Up (added load), and
Incline Bench Press are all free-weight/barbell movements the athlete doesn't currently do — his
real numbers in "My Program 2" were on Smith Machine, Leverage Machine, or dumbbell equivalents
(and several tracked as % of an internal training max), which isn't a valid 1:1 substitute for
free-weight loading. Rather than guess a real number from mismatched equipment, Week 1 starts
deliberately conservative (see `athlete/maxes.yml`) and the file hand-steps a slow, safe
progression (~5lb/week on main lifts, 2.5lb/week on OHP and Pull Up) across the 10 weeks. **Correct
these numbers with the athlete's actual felt output as real sessions happen** — if a prescribed
weight is trivially easy, jump it by hand in the next push rather than waiting out the slow ramp.

## Substitutions (fill in as constraints arise)

None recorded yet beyond the travel fallback below. If an exercise is unavailable (equipment,
injury, travel), record the swap here with the reasoning, e.g.:

```
Bent Over Row -> Chest-Supported Row  (lower back irritation flagged in log/2026-XX-XX.md)
```

## Equipment mapping

Assumes standard barbell/dumbbell gym access (`athlete/profile.md` → `equipment.gym_access: true`).
No specialized equipment required for the current program.

## Cues

- **Squat / RDL (Lower A):** these are the two lifts most likely to interfere with running if pushed
  too hard — this is exactly why Lower A sits as far from the long run as the weekly template
  allows. Don't chase PRs here at the expense of Saturday.
- **Nordic Curl (Lower B):** notoriously produces significant DOMS even at low volume — keep it at
  3x6 bodyweight as programmed, don't add load even on a green readiness day, since the soreness
  cost is disproportionate to the stimulus for a runner.
- **Single Leg Calf Raise:** this is the single highest-value accessory in the whole program for
  ultra durability — calf/achilles tolerance is a common failure point late in a long race. Don't
  cut this one when trimming volume; cut something else first.
- **Copenhagen Plank:** adductor/hip stability, directly protective against the lateral-stability
  breakdown that shows up in fatigued running form late in a race.
- **Pull Up:** programmed as `Pull Up` with an `update:` script (`weights = bodyweight +
  originalWeights[ns]`) so the app displays total system weight, while `progress:`/the hand-authored
  steps only move the added-load portion. Requires bodyweight to be set in Liftosaur to display
  correctly — recorded 2026-08-04 (162lb, via `add_measurement`). Re-record when it changes; the
  `update:` script reads the current value live, so it doesn't need re-pushing with the program.
- **Custom exercises:** `Single Leg Calf Raise` and `Dead Bug` aren't in Liftosaur's built-in
  exercise list and were created as custom exercises (via `create_custom_exercise`) rather than
  substituted for something close-but-different. If either needs editing, update the existing
  custom exercise by name rather than creating a duplicate — that preserves workout history.

## Travel fallback — 2026-08-22 to 2026-09-01 (block week 12, Liftoscript Week 4)

Gym access is uncertain while away. Rather than fork the program file (which would break the
calendar's week↔day mapping), keep Liftoscript Week 4 as written and substitute per-exercise if
the equipment isn't there. Lifting is first in the cut order anyway — a travel week that loses
some strength work is working as designed, not failing.

| Programmed | Bodyweight / hotel substitute |
|---|---|
| Squat | Bulgarian split squat, or single-leg squat to a chair |
| Romanian Deadlift | Single Leg Deadlift, bodyweight, slow eccentric |
| Bench Press | Push-up variations (feet elevated to add load) |
| Bent Over Row | Inverted row under a table, or band row |
| Pull Up | Whatever bar exists; else band pulldown |
| Overhead Press | Pike push-up |
| Incline Bench Press | Decline push-up |
| Face Pull | Band pull-apart |

Lower B is nearly bodyweight already (calf raise, Nordic, single-leg RDL, Copenhagen, dead bug) —
it travels unchanged and is the session to protect if only one lift happens that week, since the
calf/achilles work is the highest-value durability item in the whole program.

## Taper handling (from `training/block.md`)

- From block week 16: Lower A shifts in character toward Lower B (lighter loads, less bilateral
  work) even though it keeps the "Lower A" slot in the schedule.
- Block week 17: last heavy squat day.
- Block week 19 (race week): no lifting at all.

When editing the program for those weeks, don't just delete lines — replace main-lift entries with
lighter-load or bodyweight equivalents so the file stays a complete, pushable program for every
week rather than having gaps.
