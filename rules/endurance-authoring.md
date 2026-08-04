# Endurance authoring — intervals.icu syntax reference + house rules

Every file in `endurance/` has YAML frontmatter plus a body written in **intervals.icu workout
text syntax** (the format the Suunto MCP pushes as a SuuntoPlus Guide). This is a reference for
writing that body correctly — get it wrong and the watch guide is silently corrupted, not rejected.

## The most dangerous gotcha

**`m` means minutes, not meters.** `- 400m 4:40/km Pace` is a 400-*minute* interval, not 400 meters.
Always use `mtr` for meters (`400mtr`) or express short distances as decimal km (`0.4km`). Before
saving any endurance file, scan the body for a bare `m` immediately after a number and confirm it's
actually meant as minutes.

## Other things that will silently break a workout

- **Nested repeats are not supported.** Flatten any nested structure — e.g. Runna's
  `3 reps of: [4 sub-reps]` becomes one flat repeat block with all steps listed in order, repeated
  the outer count.
- **Every rest step needs an explicit target.** `- 90s` alone is invalid or ambiguous; write
  `- 90s 9:00/km Pace` (walk pace, from `athlete/zones.yml` → `pace.walk_recovery`).
- **Section headers are lines without a leading `-`.** `Warmup`, `Main Set 3x`, `Cooldown` are
  headers; every prescribed step is a `-` line under one. Repeat blocks (`Main Set Nx`) need a blank
  line before and after.
- **Ramps display as flat averages on Suunto**, not a real ramp. Prefer stepped blocks for anything
  that needs to guide the athlete in real time on the watch.
- **A workout needs a description or the Suunto push errors.** Frontmatter `intent:` is not enough
  by itself — make sure the body or a description line is non-empty.

## Syntax quick reference

**Durations:** `1h`, `10m`, `30s`, `1h2m30s` (or short form `5'`, `30"`).
**Distances:** `2km`, `500mtr`, `1mi`, `4.5mi`. Never bare `m` for meters.

**Running targets:**
- Absolute pace: `5:00/km Pace`, range `7:00-6:30/km Pace` (faster number second)
- Zone: `Z2 Pace`, `Z2-Z3 Pace`
- Percent of threshold: `60% Pace`, `78-82% Pace`
- HR: `Z2 HR`, `70% HR` (of max), `95% LTHR`, `90-95% LTHR`

**Cycling targets** (meeting-time trainer sessions):
- FTP percent: `65%`, `95-105%`
- Absolute watts: `220w`, `200-240w`
- Zone: `Z2`
- Cadence appended after the target: `- 40m 65% 85-95rpm`

**Repeats:** a section header ending in `Nx` (`Main Set 4x`) followed by its steps, blank line
before and after. A bare `Nx` on its own line also works as a repeat marker.

**Ramps** (rarely used here given the Suunto display caveat above): `- 10m ramp 50%-75%`.

## Which target to prescribe: ZoneSense, HR, or pace

The athlete runs ZoneSense (DFA a1) off a chest strap as the primary target. Match the instrument
to the session length — a1 needs a rolling ~2min RR window, so it cannot track short efforts:

| Session type | Prescribe |
|---|---|
| `long`, `b2b`, `lap-sim`, `race` | **ZoneSense Zone 1.** Pace in the body is a guide only. |
| `easy`, `recovery` | **ZoneSense Zone 1**, plus the `easy_ceiling` pace as an upper bound |
| `tempo` (continuous 15-20min blocks) | Pace, with ZoneSense as a cross-check |
| `intervals`, strides, anything under ~3min | **Pace or HR only** — ZoneSense cannot respond fast enough |

**Every session carries a `follow:` field stating this explicitly** — the athlete shouldn't have to
consult a table mid-run. Derive it from the *binding* rep length, which is the SHORTEST work
interval inside a repeat block, not the longest block in the file: an `8x2min` session is a
2-minute-rep session even when a 20-minute steady block follows it. Standalone continuous efforts
(a progression run with no repeats) use the longest work block instead.

Thresholds: **≥9min** → pace with ZoneSense as a genuine cross-check. **3–9min** → pace; ZoneSense
lags, glance between reps at most. **<3min** → pace only; a1's ~2min window cannot track it.

See `athlete/zones.yml` → `zonesense` for the reasoning and caveats.

## Frontmatter schema

```yaml
date: 2026-08-04            # ISO date, also the filename prefix
sport: Run                  # Run | Ride | Walk
name: Broken Miles           # short human name
type: intervals              # easy | long | b2b | tempo | intervals | night | lap-sim | aerobic-base | walk | race
block_week: 9
distance_km: 5.0             # omit or approximate for time-based sessions
duration_s: 2100             # always present — the number the time-budget check sums
target_mode: pace            # pace | hr | effort — long/ultra work (>~2h) must be hr or effort, never pace
follow: >                    # REQUIRED. Which instrument the athlete actually follows on the day.
  Pace only. ~2min reps ...  # Derived from the session's binding rep length — see the table above.
intent: One sentence — why this session exists this week, and any placement constraint it's satisfying.
origin: runna-seed           # runna-seed | authored | adapted
concurrent: meetings         # only present for meeting-time Ride/Walk sessions; excludes from the running time budget
publish: false                # only present to suppress a Suunto push (e.g. plain meeting walks)
published:
  suunto: null                # ISO timestamp, set by the publishing workflow — see rules/publishing.md
```

## Translating Runna prose (for any remaining seed transcription)

- `1.4km warm up at a conversational pace (no faster than 6:10/km)` → `- 1.4km 6:10/km Pace`
- `90s walking rest` → `- 90s 9:00/km Pace`
- `3 reps of: • 400m at 5:45/km …` → `Main Set 3x` header, then the flattened `- 400mtr 5:45/km Pace` steps
- `Repeat the following 3x: ---------- … ----------` → same, flattened
- `5:05/km (4:55-5:15/km)` → `- 2km 5:15-4:55/km Pace` (range, faster bound second)

## Worked examples

A standard interval session:

```markdown
---
date: 2026-08-04
sport: Run
name: Broken Miles
type: intervals
block_week: 9
distance_km: 5.0
duration_s: 2100
target_mode: pace
intent: Threshold touch at low volume; keep legs fresh for Saturday's long run.
origin: runna-seed
---

Warmup
- 1km 6:05/km Pace

Main Set 2x
- 1.2km 5:00/km Pace
- 120s 9:00/km Pace
- 400mtr 4:40/km Pace
- 60s 9:00/km Pace

Cooldown
- 800mtr 6:15/km Pace
```

An ultra-specific, time/HR-based session:

```markdown
---
date: 2026-09-19
sport: Run
name: Lap Simulation — full fueling rehearsal
type: lap-sim
duration_s: 13500
target_mode: hr
intent: Rehearse one 24.1km Ghost Train lap at goal effort with race fueling and race kit.
origin: authored
---

Warmup
- 10m Z1 HR

Main Set 4x
- 20m Z2 HR
- 90s 9:00/km Pace

Cooldown
- 10m Z1 HR
```

A meeting-time trainer session (Z2, unstructured enough to survive being ridden through a call):

```markdown
---
date: 2026-08-05
sport: Ride
name: Meeting Z2 + fueling practice
type: aerobic-base
duration_s: 3600
target_mode: power
concurrent: meetings
intent: Aerobic volume with zero family cost; practice 90g/hr carb intake.
origin: authored
---

- 10m 55% 85rpm
- 40m 65% 85-95rpm
- 10m 55% 85rpm
```

A meeting-time walk (tracked, not necessarily pushed to the watch):

```markdown
---
date: 2026-08-05
sport: Walk
name: Meeting walk
type: walk
duration_s: 5400
target_mode: effort
concurrent: meetings
publish: false
intent: Time on feet — foot/calf/achilles durability at near-zero recovery cost.
origin: authored
---

- 90m brisk, slight incline
```
