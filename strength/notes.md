# Strength notes — substitutions, equipment, cues

## Week ↔ block-week offset

Liftoscript `# Week 1` = block week 9 (2026-08-03). To find the Liftoscript week for any block
week: `liftoscript_week = block_week - 8`. When appending a new week to
`strength/program.liftoscript`, copy the previous week's structure forward and apply that week's
readiness/taper adjustments from `rules/progression.md` and `training/block.md` rather than
reinventing the exercise selection each time.

## Substitutions (fill in as constraints arise)

None recorded yet. If an exercise is unavailable (equipment, injury, travel), record the swap here
with the reasoning, e.g.:

```
Barbell Row -> Chest-Supported Row  (lower back irritation flagged in log/2026-XX-XX.md)
```

## Equipment mapping

Assumes standard barbell/dumbbell gym access (`athlete/profile.md` → `equipment.gym_access: true`).
No specialized equipment required for the current program.

## Cues

- **Squat / RDL (Lower A):** these are the two lifts most likely to interfere with running if pushed
  too hard — this is exactly why Lower A sits as far from the long run as the weekly template
  allows. Don't chase PRs here at the expense of Saturday.
- **Nordic Hamstring Curl (Lower B):** notoriously produces significant DOMS even at low volume —
  keep it at 3x6 as programmed, don't add sets even on a green readiness day, since the soreness
  cost is disproportionate to the stimulus for a runner.
- **Single Leg Calf Raise:** this is the single highest-value accessory in the whole program for
  ultra durability — calf/achilles tolerance is a common failure point late in a long race. Don't
  cut this one when trimming volume; cut something else first.
- **Copenhagen Plank:** adductor/hip stability, directly protective against the lateral-stability
  breakdown that shows up in fatigued running form late in a race.

## Taper handling (from `training/block.md`)

- From block week 16: Lower A shifts in character toward Lower B (lighter loads, less bilateral
  work) even though it keeps the "Lower A" slot in the schedule.
- Block week 17: last heavy squat day.
- Block week 19 (race week): no lifting at all.

When editing the program for those weeks, don't just delete lines — replace main-lift entries with
lighter-load or bodyweight equivalents so the file stays a complete, pushable program for every
week rather than having gaps.
