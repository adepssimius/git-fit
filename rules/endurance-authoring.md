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
- **Step titles are capped at 13 characters on the watch.** Write the header for a human reading
  the plan; the compiler renders it into a fixed token vocabulary — see below.

## Step titles — write prose, ship tokens

Thirteen characters is far shorter than a useful header. Write the header for a human reading the
plan (`Car — crew stop, sock change, foot care`); `TITLE_RULES` in `scripts/compile_guide.py`
renders it to the watch vocabulary. Don't cramp the source file to fit the watch — that trades the
readable artifact for the throwaway one.

| Token | From | Token | From |
|---|---|---|---|
| `WU` | Warmup | `CREW` | Crew stop / Car — crew stop |
| `CD` | Cooldown | `TURN` | Turnaround |
| `EZ` | Easy | `OUT>NORTH` | Car -> north terminus |
| `EZ/MOD` | Easy/Moderate | `BACK>CAR` | North terminus -> car |
| `EZ>HILL` | Easy to hill | `OUT>SOUTH` | Car -> south end |
| `MOD` | Moderate | `O&B 1` | Out-and-back 1 |
| `STEADY` | Steady | `TOP-UP` | Top-up to a race-lap distance |
| `PROG` | Progression | `LAP 1-2` | Laps 1-2 |
| `STRIDE` | (Hill) Strides | `SETTLE` | Settle in |
| `HILL` | Hills | `WAKE UP` | Wake-up shuffle |
| `THR` | Threshold, incl. long/short | `NGT STEADY` | Night Steady |
| `SURGE` / `PICKUP` | Surges / Pickups | `NGT BLOCK` | Night Blocks |
| `REP` | Main Set | `HARD FIN` | Hard Finish |
| `R/W` | Run/Walk | `DAWN FIN` | Dawn Finish |
| `REC` | any rest step inside a repeat | | |

Two properties to preserve when extending it:

- **It is a closed vocabulary.** A handful of tokens reused everywhere is learnable in a session or
  two and readable at a glance at hour 20; ad-hoc abbreviations are not — `STR` could be strides,
  steady or straight. Add a rule to the table rather than inventing a one-off.
- **Rep counts are dropped** — `Hill Strides 5x` becomes `STRIDE`. The watch already displays rep
  progress, so repeating it spends scarce characters on information that is on screen anyway.

Anything after a dash is explanation and gets stripped — it belongs in `brief:`, not on the watch.
An unmapped header over 13 chars **warns** rather than being silently clipped; that is how
`Easy to a hill` once reached the watch as `Easy to a hil`.
- **A workout needs a description or the Suunto push errors.** Frontmatter `intent:` is not enough
  by itself — make sure the body or a description line is non-empty.

## Syntax quick reference

**Durations:** `1h`, `10m`, `30s`, `1h2m30s` (or short form `5'`, `30"`).
**Distances:** `2km`, `500mtr`, `1mi`, `4.5mi`. Never bare `m` for meters.

**`ZoneSense Z1` — the display-only target.** Write this wherever ZoneSense governs the step
(easy, long, b2b, lap-sim, race). The wire format has **no ZoneSense target** — its target fields
are pace, HR, power and cadence, and ZoneSense is a separate Zapp the guide cannot drive. So the
compiled step shows pace and HR as *data* and asserts no target at all, which is the honest
encoding: the instruction lives in the guide description, and the watch's own ZoneSense alarm
(`Targets.ZoneSenseZones`, see `athlete/zones.yml`) does the enforcing.

Do **not** put a pace target on a ZoneSense-governed step as a stand-in. On rolling terrain it is
wrong in both directions — it fires on descents, where speed is aerobically free, and under-reads
climbs — and with the ZoneSense alarm enabled it gives two alarm sources with different opinions
on a session where the instrument has already been chosen. Keep pace targets for steps where pace
genuinely is the instrument: strides, intervals, threshold reps, anything under ~9min.

**`until-lap` — the step ends only on a lap press.** Append it when the *terrain*, not the clock,
decides where a step ends: `- 4km ZoneSense Z1 until-lap` means "run easy for about 4km, and press
lap when you reach a hill." Without it, a step ends on its own distance or duration and whatever
follows begins wherever the athlete happens to be standing — which is wrong for hill strides,
anything needing a specific surface, and any block that has to start at a known landmark. The
distance still shows as a countdown, so the nominal figure is a progress cue rather than a
deadline.

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

**Every session carries two athlete-facing fields, `brief:` and `follow:`.** Together they are the
only prose that reaches the watch — `compile_guide.py` joins them, in that order, into the guide's
description in the Suunto app. So this is what gets read at the trailhead, and nothing else does.

| Field | Answers | Content |
|---|---|---|
| `brief:` | *What is going to happen?* | The blocks in order, in plain language, plus the one thing that would spoil the session — going out too fast, starting a stride cold, opening a long run at a pace that only works for an hour. One clause, not a lecture. |
| `follow:` | *What do I obey while it happens?* | The instrument, **per phase**. |

**They are joined, not duplicated.** `brief:` doesn't restate the instrument and `follow:` doesn't
re-narrate the session — if each repeated the other, the two would drift the first time one was
edited alone, and the athlete would read a contradiction on the start line.

**Derive `follow:` per phase, not per session.** An easy run with strides at the end is *ZoneSense
for the running, feel for the strides*; collapsing that into a single instrument makes it wrong for
one half or the other. The binding-rep rule still governs sessions that are **quality throughout**,
because the athlete moves between pieces continuously and needs one rule that holds across all of
them: an `8x2min` session is a 2-minute-rep session even when a 20-minute steady block follows it.
The test is whether the phases are interleaved (one instrument) or sequential (one each).

Where a phase is too short for any instrument, say so plainly — **"by feel" is a complete answer**,
and a better one than naming an instrument that cannot respond in the time available.

**The two together must fit 256 characters**, which is tighter than it sounds: roughly 120 each.
`compile_guide.py` warns rather than silently truncating, because a description cut mid-sentence
ships a guide whose last instruction is a fragment. If it won't fit, the reasoning is what to cut —
that belongs in `intent:`, which is written for the repo and never leaves it.

Thresholds for picking the instrument within a phase: **≥9min** → pace with ZoneSense as a genuine
cross-check. **3–9min** → pace; ZoneSense lags, glance between reps at most. **<3min** → pace or
feel only; a1's ~2min window cannot track it.

See `athlete/zones.yml` → `zonesense` for the reasoning and caveats.

## Scheduling: opportunistic by default

**Do not author sessions that assume a time of day.** The athlete fits most runs into the day as it
allows and decides on the day — there is no fixed morning or evening slot, and any earlier
references to "protected windows" were invented, not real.

The exception is a short list of sessions where timing *is* the stimulus: night runs, the Big Day
weekend pair, and the one bicarb session. Those carry a `time_critical: >` field in their
frontmatter stating the required time and why. If a session doesn't carry that field, it can move
freely within its day.

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
brief: >                     # REQUIRED. WHAT HAPPENS, in plain language, plus the one thing that
  Easy 4km, six 20s hill     # would spoil it.
  strides, 1.5km home...
follow: >                    # REQUIRED. WHAT TO OBEY, per phase. Joined onto `brief:` to form the
  Run it in ZoneSense Z1...  # guide description — the two together must fit 256 chars.
time_critical: >             # ONLY on sessions whose time of day is load-bearing (night runs, the
  START 03:00 because ...    # Big Day pair, the bicarb session). Omit it entirely otherwise.
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
