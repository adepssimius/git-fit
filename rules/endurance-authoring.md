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
- **Every rest step needs an explicit target, and there are two distinct recoveries — pick
  deliberately, don't default to one.** `pace.jog_recovery` (7:30-8:15/km) for floats between
  threshold/interval reps, where the point is lactate shuttling and standing would defeat it.
  `pace.walk_recovery` (9:00/km) for genuine walk breaks: strides walk-backs, rest after very
  short/fast reps (hill sprints, 400s) that a jog wouldn't clear, and crew stops / turnarounds in
  the Big Day and lap sims. **Never as a run/walk protocol inside a training run** — that is a
  race-day tactic only (`training/block.md` rule 6). `- 90s` alone is invalid or ambiguous; write
  `- 90s 8:00/km Pace` or `- 90s 9:00/km Pace` depending on which of the two applies.
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
| `R/W` | Run/Walk — **race day only** | `DAWN FIN` | Dawn Finish |
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

**A BARE PACE TARGET IS THE FAST EDGE OF A 30-SECOND BAND, NOT A POINT.** `compile_guide.py`
turns `7:30/km Pace` into a target of **7:30 to 8:00** (`PACE_BAND_SLOWER_S = 30`) — the number
you write becomes the FAST end and the watch will happily sit you 30s/km slower than you meant.
This is the single least intuitive thing in the syntax and it caused a real error:

- Every threshold float in the plan was written `7:30/km Pace`, intending the athlete's jog floor.
  It compiled to 7:30-8:00, which is **entirely inside the dead band** between his jog floor
  (7:30) and his max walk pace (9:30) — see `athlete/zones.yml` § locomotion_floors. The watch was
  asking for a pace he cannot produce by either gait.
- Corrected 2026-08-15 (athlete-spotted) to the explicit range `7:15-7:30/km Pace`, which puts
  7:30 at the SLOW edge where it was always meant to be.

**CORRECTED 2026-08-15 — the sentence that used to sit here was wrong.** It said bare targets
were "fine for quality work, where being 30s/km slower than target is just a rep you did not
quite hit." They are not. 5:25 versus 5:55 is threshold versus steady — two different sessions,
not a near miss. The 08-15 long run proved it: the reps were prescribed 5:55, the band ran to
6:25, and the athlete ignored the target entirely and ran 5:23. The band did no work at all.

**THE RULE: 30-second bands throughout, positioned by what the number MEANS.**

The width is fixed at ~30s because that is what the athlete can hold without nuisance alerts —
GPS pace fluctuates enough that a 10s band flickers in and out constantly (athlete-reported
2026-08-15). So the fix is never to narrow the band. It is to put the number in the right place
inside it.

| the number is a... | write | band | examples |
|---|---|---|---|
| **TARGET** — hit this | explicit centred range | `5:10-5:40` centres 5:25 | threshold, tempo, vo2, reps, strides, steady, long_steady |
| **CEILING** — go no faster | bare target (default is correct) | `7:00` -> 7:00-7:30 | easy, warmup, cooldown, long-run cruise |
| **FLOOR** — go no slower | explicit range, number at the slow edge | `7:10-7:40` | floats, jog recoveries |
| **SPEED CEILING** | bare target (default is correct) | `9:30` -> 9:30-10:00 | walk-backs, walk recoveries |

This is why the bare default has been quietly right in most of the plan and wrong only on the
quality steps: easy paces and walk paces ARE ceilings, so downward-only expansion encodes them
correctly. Quality paces are targets, and downward-only expansion turns the target into the
fastest acceptable pace — which is backwards.

**Before leaving any target bare, ask which of the four rows it is**, and check `written + 30s`
against `athlete/zones.yml` § locomotion_floors so the slow half of the band is not a gait he
cannot produce.

**Nothing in the guide enforces a pace band anyway.** The compiled step's `alerts` array carries
only a step-duration countdown — there is no pace alert. The band is a display. Live enforcement
is a watch-side setting (`Targets.SpeedZone`), which read "None" on the 08-15 workout. Same
situation as ZoneSense: the guide shows, the watch governs, and neither is armed by default.

**Nothing enforces a ZS Z1 step — confirmed against real workout data, 2026-08-15.** The athlete
asked whether the ZS Z1 portions carry a pace zone. They do not, at three separate layers, and it
is worth being blunt about all three because this file previously implied the watch was enforcing
it:

1. `parse_target` returns None for `ZoneSense Z1`, so the compiled step asserts NO target.
2. The wire format has no ZoneSense target field at all — only pace, HR, power, cadence.
3. The watch's own zone alarm was NOT set either. The 2026-08-12 SML header reads
   `Targets.ZoneSenseZones: "None"` (alongside HeartRateZone / PowerZone / SpeedZone, all "None").

So a ZS Z1 block is **a label plus the athlete's judgement**, with the live ZoneSense Zapp screen
(`Zapps {Id: "zzaeroen"}`, confirmed running) as the only readout — and that screen has no reading
for the first ~10min. The cross-check available after the fact is `hr.long_run_hr_ceiling` (155) in
`athlete/zones.yml`. If live enforcement is ever wanted, it is a watch-side setting
(`Targets.ZoneSenseZones`), not something the guide can carry.

**`ZoneSense Z1` — the display-only target.** Write this wherever ZoneSense governs the step
(easy, long, b2b, lap-sim, race). The wire format has **no ZoneSense target** — its target fields
are pace, HR, power and cadence, and ZoneSense is a separate Zapp the guide cannot drive. So the
compiled step shows pace and HR as *data* and asserts no target at all, which is the honest
encoding: the instruction lives in the guide description, and the watch's own ZoneSense alarm
(`Targets.ZoneSenseZones`, see `athlete/zones.yml`) does the enforcing.

**The first ~10 minutes of any activity get no ZoneSense reading at all** (athlete-confirmed cold
start, distinct from the ~2min rolling-window lag discussed below). Once one block in a session has
passed the 10min mark, every later block is fine at `ZoneSense Z1` regardless of how it's split up —
the clock is cumulative from session start, not per-step.

**The cold-start opener — athlete-directed, 2026-08-04.** An earlier version of this rule filled the
cold-start window with an explicit pace target (running) or HR band (trainer). For **easy-effort
running that is not chasing a pace, don't.** Open with `ZoneSense Z1` like the rest of the session —
which compiles to no target at all — and title the step `Easy aerobic`, which the compiler renders
to **`EZ ZS Aerobic`**. The label states the intent; the athlete paces the opening himself.

Why the change: `log/2026-08-04.md`. That session was the one run authored with an HR-band opener
(`Z2 HR`, i.e. 138–151 from `hr.zones.z2_aerobic`). He ran the whole thing at HR 124–133 and
ZoneSense *still* flagged him above its Zone 1 at the fastest point — so the band derived from LTHR
sits **above** his measured aerobic threshold, and prescribing it asks for exactly the easy-day creep
`athlete/zones.yml` names as his most likely training error. A pace opener has the same defect in a
quieter form. The athlete's call: no compiled constraint on easy running, just a label.

Two carve-outs where the opener is **not** a cold-start crutch and stays exactly as written:

- **Race and lap simulations** (`2026-10-17-ghost-train-race.md`, both `lap-simulation-*.md`) open at
  `pace.ultra_lap_early` on purpose. Per `athlete/zones.yml`, lap 1 "should feel almost
  embarrassingly slow" and the failure mode is starting anywhere near normal easy pace. That target
  is the pacing strategy, not a stand-in for a missing reading.
- **Trainer rides** keep `65-72% HR`. `bike.ftp_w` is null, ZoneSense is a running instrument here,
  and an HR band is the only real target available.

A ride step that's ≤10min entirely (most ride warmups/cooldowns) should still be an HR target
throughout, never ZoneSense at all.

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

**Never write a bare zone — qualify every mention, not just the first.** `ZS Z2`, `HR Z2`,
`Pace Z2`. Not `Z2`, not `Zone 2`. Three systems share the numbering and mean different
intensities, and the athlete reads these on a watch mid-run where there is no earlier sentence to
refer back to.

**Always name the instrument when you write a zone.** "Zone 2" is ambiguous in this repo and the
ambiguity is not cosmetic: **ZoneSense Zone 2** is everything between the aerobic and anaerobic
thresholds (its ceiling is LT2 — hard), while **HR Zone 2** is 138-151bpm (`hr.zones.z2_aerobic` —
easy aerobic). They are wildly different intensities that happen to share a number. Write
`ZoneSense Z2` or `HR Z2`, never a bare "Zone 2", especially in `follow:` — that field is what the
athlete reads on the day. Caught 2026-08-05 on the progression run, whose `follow:` said "sit
mid-Zone 2, not at its ceiling" and meant ZoneSense.

**Give block durations in `follow:` when the body is written in distance.** The same session
referred to "a ~20min continuous block" while the body prescribed 2km/3km/2.5km/1.5km — the athlete
had no way to tell which block that was without doing the arithmetic. If `follow:` singles out a
block, identify it the way the body writes it, plus the time.

**Running targets:**
- Absolute pace: `5:00/km Pace`, range `7:00-6:30/km Pace` (faster number second)
- Zone: `Z2 Pace`, `Z2-Z3 Pace`
- Percent of threshold: `60% Pace`, `78-82% Pace`
- HR: `Z2 HR`, `70% HR` (of max), `95% LTHR`, `90-95% LTHR`

**Cycling targets** (meeting-time trainer sessions):
- HR (what this repo actually uses): `Z2 HR`, `65-72% HR` — `bike.ftp_w` is null ("UNKNOWN and
  not worth testing for this block"), and the compiler *refuses* `%FTP` targets rather than
  inventing an FTP, so power targets below are documented syntax only until an FTP exists.
- FTP percent: `65%`, `95-105%` (unusable while `ftp_w` is null)
- Absolute watts: `220w`, `200-240w`
- Cadence appended after the target: `- 70m Z2 HR 85-95rpm`

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

**One deliberate exception to the first row: the Big Day** (`2026-09-05-big-day.md`). Champion week
10 prescribes a genuinely hard 50k, and its closing block is faster than `easy_ceiling` on purpose
— ZoneSense Zone 1 would cap the whole session at an easy aerobic day and lose the stimulus the
week is built around. It is also the one long session HR cannot govern either: over 6h, cardiac
drift rises as you accelerate, so an HR ceiling would force a slowdown exactly where the plan says
speed up. So it is pace-governed, with `target_mode: effort` (the paces are guides for a by-feel
progression, not a contract — AGENTS.md invariant 5 still holds). **Don't "fix" it back to
ZoneSense.** Every other `long`/`b2b`/`lap-sim`/`race` session follows the table.

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

## Translating Runna prose (historical — seed transcription is complete)

No `endurance/` file remains on `origin: runna-seed`; this table survives only as a reference for
*reading* `seed/runna-plan.md`. The paces in the left column are Runna's own historical values —
they were contradicted by the athlete's PRs and superseded by `athlete/zones.yml` (see that
file's header). Never copy them into a session.

- `1.4km warm up at a conversational pace (no faster than 6:10/km)` → `- 1.4km 6:10/km Pace`
- `90s walking rest` → `- 90s 9:00/km Pace`
- `3 reps of: • 400m at 5:45/km …` → `Main Set 3x` header, then the flattened `- 400mtr 5:45/km Pace` steps
- `Repeat the following 3x: ---------- … ----------` → same, flattened
- `5:05/km (4:55-5:15/km)` → `- 2km 5:15-4:55/km Pace` (range, faster bound second)

## Worked examples

All paces below come from `athlete/zones.yml` — an example with a pace not in that table is a bug
in this file. Every example carries `brief:` + `follow:`, both required.

A standard quality session (pace-governed throughout, per the binding-rep rule; jog recovery from
`pace.jog_recovery`):

```markdown
---
date: 2026-08-12
sport: Run
name: Threshold — 7x2min
type: tempo
block_week: 10
distance_km: 8.4
duration_s: 3315
target_mode: pace
brief: >
  2km up, 7x(2min at 5:40 + 90s float), 1.5km steady, 1km down. Floats keep moving — no
  standing rest.
follow: >
  Pace only. ~2min reps — ZoneSense's ~2min window cannot track efforts this short.
intent: The week's single big workout. Float recoveries, not standing rest.
origin: authored
---

Warmup
- 2km 7:00/km Pace

Main Set 7x
- 2m 5:40/km Pace
- 90s 7:30/km Pace

Steady
- 1.5km 6:30/km Pace

Cooldown
- 1km 7:00/km Pace
```

A ZoneSense-governed long session (note the cold-start split: an explicit pace target for the
first ~10min, ZoneSense Z1 after; walk breaks from `pace.walk_recovery`):

```markdown
---
date: 2026-09-12
sport: Run
name: Long Run — easy, on tired legs
type: long
block_week: 14
duration_s: 6600
target_mode: effort
brief: >
  15min in, 5x(15min run + 3min walk), 5min down. Easy, on last night's legs.
follow: >
  First 10min: hold the pace shown, ZoneSense has no reading yet. After: Zone 1 — go slower
  if that's what it needs.
intent: Short and easy by design; tired-legs practice at low cost.
origin: authored
---

Warmup
- 10m 7:00/km Pace
- 5m ZoneSense Z1

Easy aerobic
- 90m ZoneSense Z1

Cooldown
- 5m ZoneSense Z1
```

A meeting-time trainer session. HR-based, never %FTP — `bike.ftp_w` is null and the compiler
refuses relative power targets (`rules/publishing.md`). The 10min warmup is a single HR-band
step because ZoneSense has no reading yet (and never write `Z1 HR`: the zone table's `<138` has
no lower bound, so the compiler degenerates it to a 138–138 point target — use an explicit
`65-72% HR` band):

```markdown
---
date: 2026-08-13
sport: Ride
name: Meeting Z2 x-train
type: aerobic-base
block_week: 10
duration_s: 5400
target_mode: hr
brief: >
  90min trainer through meetings: 10 easy, 70 Z2, 10 easy. Hold ~75g carbs/hr.
follow: >
  Warmup/cooldown: ZoneSense Zone 1. Main set: Z2 HR, 138-151bpm.
concurrent: meetings
intent: Thursday x-train slot, ridden during meetings; gut-training rep.
origin: authored
---

- 10m 65-72% HR 85rpm
- 70m Z2 HR 85-95rpm
- 10m ZoneSense Z1 85rpm
```

A meeting-time walk (tracked in-repo only, not pushed to the watch):

```markdown
---
date: 2026-08-10
sport: Walk
name: Meeting walks (weekly total)
type: walk
block_week: 10
duration_s: 12300
target_mode: effort
brief: >
  205min of brisk walking spread across the week's calls.
follow: >
  Effort only, no metric. Brisk and sustainable.
concurrent: meetings
publish: false
intent: Time on feet — foot/calf/achilles durability at near-zero recovery cost.
origin: authored
---

Weekly target: **205 minutes** of brisk walking, distributed across call-heavy days.
```
