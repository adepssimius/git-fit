# Athlete profile

The most load-bearing file in the repo. Every authored week is checked against `time_budget` and
`meeting_budget` below. Values are the user's own; the LLM must never author a week that exceeds
them without an explicit override in `log/`.

## Context

- Father of young kids, full-time job. **Training time is the binding resource** — not fitness.
  Family disruption must be minimized; this outranks training-optimality when the two conflict.
- Wants to get **faster**, not just more durable — a higher aerobic ceiling and tighter easy pace
  both reduce hours-on-course for a fixed distance, which is the time-efficient thing to chase here.
- Prior 50k finish on the Ghost Train course (~3 years ago) — course and ultra distance are both
  known quantities, not a leap into the unknown.

## Time budget — hard constraint

```yaml
time_budget:
  weekday_session_max_min: 60      # door-to-door, incl. changing
  # The weekday cap takes the same escape hatch as the long-run cap, added 2026-08-12: a session
  # over 60min is allowed when its frontmatter carries an explicit `budget_exception: <reason>`,
  # up to the ceiling below and no more than `weekday_exceptions_per_block` times.
  # Before this the weekday cap had NO exception mechanism, so a one-off longer weekday session
  # could not be expressed at all — the only ways out were to understate the duration in the
  # plan or to raise the cap for every week. A flagged, counted, visible exception is better
  # than either. The cap exists to protect family time, so if exceptions stop being rare the
  # honest reading is that the cap is wrong, not that the sessions are.
  weekday_session_exception_max_min: 90
  weekday_exceptions_per_block: 4
  weekday_sessions_per_week: 4
  # Night sessions sit outside the weekday cap on purpose: they run post-bedtime, which is
  # the whole reason training/block.md calls night running "free" in family terms. They still
  # cost recovery and sleep, so they get their own ceiling rather than no ceiling.
  night_session_max_min: 90
  long_run_max_min: 240            # default cap — buy durability with the Sunday b2b, not a 6h run
  # A few long runs may exceed the cap, but only a few — the point is that going long stays
  # special rather than becoming the default. A session over the cap MUST carry a
  # `budget_exception: <reason>` field in its frontmatter; scripts/verify_plan.py errors on any
  # over-cap session without one, and errors again if more than `long_run_exceptions_per_block`
  # carry it. That keeps "a few exceptions are fine" honest instead of quietly becoming "every
  # long run drifts long."
  long_run_exception_max_min: 430  # absolute ceiling even for flagged sessions
  # RAISED 400 -> 430 on 2026-09-07, athlete-approved, and recorded as a PACING-MODEL CORRECTION
  # rather than a cap relaxation. AGENTS.md invariant 1b forbids raising the cap to make a
  # session fit, and that is not what this is. The 400 was set when a 50k was modelled at the
  # Big Day's planned pace — 363min for 50km, i.e. ~7:16/km on a negative split. The athlete has
  # since replaced that pacing model with run/walk from the gun at ~8:20/km, walking the hills
  # and the steep descents for damage control (log/2026-09-06.md). Same 50km, 417min moving.
  # The cap did not change; the pace assumption underneath it did, and the ceiling was left
  # describing a race he has decided not to run. 430 is 50km at his real pace plus stops, and
  # nothing more — it does not create room for a longer session than the one it was derived for.
  # If the pacing model changes again, this number is downstream of it and moves with it.
                                   # (a genuine 50k at this athlete's moderate effort is ~6h)
  long_run_exceptions_per_block: 3
  sunday_b2b_max_min: 150
  weekly_total_max_min: 600        # running only; excludes meeting-time trainer/walk sessions
  doubles_ok: true                 # 40-50min easy, pre-dawn or post-bedtime
  lifting_session_min: 60          # 4x/week, 45-60min — see rules/strength-authoring.md

  # SCHEDULING IS OPPORTUNISTIC, NOT FIXED. An earlier version of this file invented
  # "protected windows" including a 05:00 weekday start. That was never the athlete's constraint
  # and is now removed — he is not getting up at 5am. Most runs get fitted into the day as it
  # allows, decided on the day.
  #
  # What actually constrains scheduling:
  #   - the weekly time budget above (hard)
  #   - the blackouts below (hard)
  #   - the strength placement rules in rules/strength-authoring.md (hard)
  #   - a handful of genuinely time-critical sessions, listed below (hard, but only those)
  # Everything else: run it whenever the day allows. Do NOT author sessions that assume a
  # specific clock time unless they carry a `time_critical:` field.
  scheduling: opportunistic

  # The ONLY sessions whose time of day actually matters. Each carries `time_critical:` in its
  # own frontmatter explaining why — see rules/endurance-authoring.md.
  time_critical_sessions:
    - 2026-08-18  # night run — needs full dark
    - 2026-09-05  # BIG DAY — early start so it finishes by noon AND sets up the next morning
    - 2026-09-06  # pre-dawn on 50k legs — 03:00, the whole point is sleep-deprived + dark
    - 2026-09-12  # lap sim 1 — dusk start (~19:00); rehearses the daylight->headlamp
                  # transition and puts ~3h of the session in the dark. Moved here from
                  # 09-19 on 2026-09-07 (possible work travel); absorbs the 09-11 night run
    - 2026-09-16  # bicarb session — needs a 1.5-2h pre-load window before the start
    - 2026-09-26  # night long run — 03:00 start, dark into dawn
    - 2026-10-06  # taper night run — needs dark

  blackout:
    # Friday morning is NO LONGER blacked out (lifted 2026-08-03). Friday is now available
    # training time. It still defaults to easy/rest because rules/strength-authoring.md requires
    # a complete leg-recovery day immediately before the Saturday long run — but that's a
    # training choice now, not a hard constraint, and Friday can absorb an easy session or an
    # upper-body lift when a week needs the room.
    []                      # no hard blackouts

  # CORRECTED 2026-08-12 (athlete): weekend afternoons were listed above as hard blackouts.
  # They are not — they are a PREFERENCE. Weekend afternoons are available training time; they
  # are simply not the first choice, and a session placed there costs family goodwill rather
  # than being forbidden. Schedule mornings by default and say so when a plan spends an
  # afternoon, but do not treat an afternoon session as an impossibility or reshape a week to
  # avoid one. The distinction matters for long runs specifically: a 213-240min session no
  # longer has to finish by noon, so it does not need a pre-dawn start to fit.
  soft_preference:
    - "sat morning preferred over sat afternoon"
    - "sun morning preferred over sun afternoon"
```

## Priority when time is short — running wins (athlete-confirmed 2026-08-12)

**This is a best-effort plan with an emphasis on running.** The athlete is time constrained. The
plan is written as an aspiration, not a contract, and the modality that gets protected when the
day compresses is running.

Order of precedence when there isn't room for everything:

1. **Running** — the prescribed session, at the prescribed intensity.
2. **Meeting-time walking / trainer** — nearly free in family terms, so it survives most squeezes.
3. **Lifting** — first to be cut. See below.

What follows from this, and it matters most for how `log/` and the daily brief are written:

- **A missed lift is an expected outcome of the constraint, not an adherence failure.** Record it
  and move on. Do not escalate a run of missed lifts into a re-author question, do not propose
  cutting the program to "what will actually get done," and do not open each morning by tallying
  them. Week 10 lost three lifts and the 08-12 brief framed that as needing a decision — that was
  the wrong read, and it is the specific thing this section exists to prevent recurring.
- **The 4-day split stays authored as written.** Best-effort means aim high and take what lands,
  not lower the target to guarantee a hit. `strength/program.liftoscript` is unchanged by this.
- **Do not manufacture make-up sessions.** A lift that misses its slot is gone; the placement rules
  in `rules/strength-authoring.md` exist precisely so lifts don't get stacked into whatever gap is
  left. The same applies to a skipped run — see the 08-11 entry, where skipping an easy run to
  sleep was the correct trade and explicitly not something to recover.
- **Liftosaur pointer drift is a permanent consequence of this**, not a bug to chase. The app
  advances by completion and this plan advances by date, so under a best-effort strength policy the
  two will never reconcile on their own. `strength/notes.md` § Pointer drift already says navigate
  by hand; this is why that will keep being true.

Where the emphasis on running does bind: it is an argument for protecting session *quality*, not
just presence. When the week compresses, the threshold and long sessions are the ones to keep
whole — easy volume is the cheapest thing on the calendar and the right thing to spend.

## Meeting time — a separate, mostly-free budget

Meeting time (work calls) can be spent on the bike trainer (aerobic base, non-impact) or walking
(time on feet, race-specific durability). Neither counts against `weekly_total_max_min`, but both
count against recovery — see `training/block.md` § "Why this block looks the way it does" and
rule 5 in § "Reshaping rules" for the full reasoning on why walking is prioritized. (Corrected
2026-08-06 — this pointed at a "Three training currencies" section that doesn't exist in that
file; either a stale rename or a section that was planned and never written.)

**Walking and the trainer are mutually exclusive PER DAY — athlete-confirmed 2026-08-06.** He has
~90-120min of meetings total on a given day, full stop, and can't be walking and on the bike in the
same block. This is stronger than "the pool is shared" — a day that carries the trainer ride
contributes **zero** walking minutes, not a reduced share. The weekly template
(`training/block.md`) fixes the meeting-time ride on **Thursday** every week of the block (see
`endurance/*-meeting-zone2-ride.md`, always a Thursday), so **only 4 days/week carry walking**
(Mon/Tue/Wed/Fri), not 5. `.claude/skills/daily-brief/scripts/brief_context.py` computes the
per-day walking rate against this real 4-day set — don't divide the weekly target by 5.

```yaml
meeting_budget:
  weekly_available_min: 600
  default_allocation: walking      # durability is the limiter; aerobic base is already largely built

  trainer:
    # No weekly floor — walking is the stated priority (default_allocation above) and takes as
    # much of the pool as the ramp cap allows; the trainer fills whatever's left. A prior 180min
    # floor was never once met across the block and fought the walking-first intent.
    session_max_min: 90              # hard per-session cap
    intensity_ceiling: "HR Z2"     # 138-151bpm. Never allowed to compete with a run quality
                                   # session. HR, not ZS: bike.ftp_w is null and ZoneSense is a
                                   # running instrument, so HR is the only real target here.
    fixed_day: Thursday              # every week of the block — see mutual-exclusivity note above

  walking:
    # Ramp deliberately — jumping straight to 10h/wk invites plantar fascia / achilles injury.
    # NOTE: the ramp cap is the binding constraint, not the peak target. Starting at 180 and
    # capped at +15%/wk, the reachable peak is ~465-480 min at block weeks 16-17, NOT 600 by
    # week 15. The cap wins; the peak arrives later and lower. Per rules/progression.md, never
    # bust the ramp to hit a target number.
    weekly_min_start: 180          # block week 9
    weekly_min_peak: 465           # realistically reached at block weeks 16-17, then tapers
    weekly_ramp_max_pct: 15        # max week-over-week increase — check this every week
    style: "brisk, sustained; incline pad optional (unconfirmed) — no weight vest, see below"
    # ACTUAL per-block-week totals (min), from the endurance/*-meeting-walk-week.md files —
    # corrected 2026-08-06, the previous version of this comment had drifted from the real files:
    # wk9 180 | wk10 205 | wk11 170 | wk12 — (hiking week, no walk target, see Travel weeks below)
    # wk13 220 | wk14 355 | wk15 405 | wk16 465 | wk17 465 | wk18 300 (taper) | wk19 150 (race week)
    #
    # wk16/wk17 are TIGHT under the 4-day rule above: 465min / 4 days = 116min/day, right at the
    # top of the stated 90-120min/day meeting budget with no slack. If a real week falls short,
    # rules/progression.md's guidance applies (miss the weekly total rather than spike to catch up)
    # — do not quietly redistribute the shortfall onto Thursday, which has zero capacity for it.

  counts_toward_weekly_total: false
```

## Unplanned sessions

Never scheduled in advance; recorded in `log/` after the fact and absorbed into the current week
per `training/block.md` § "Unplanned sessions":

- **Group road rides** with friends → treated as a threshold session (replaces, doesn't add to, the
  week's second quality slot).
- **eMTB spins** → treated as active recovery (motor-assisted, low impact) — a legitimate substitute
  for a Monday recovery run.

## Champion Plan staples — low time cost, kept in the plan

```yaml
heat:
  sauna_available: true            # at the gym; athlete uses it ~20min after any gym session
  hot_tub: false                   # planned purchase, but NOT before this race — don't rely on it
  counts_toward_training_time: false   # post-session at a gym he's already at; costs nothing
  note: >
    Aerobic/plasma-volume benefit only — the race is mid-October in NH, so no heat-acclimation
    block is needed. Athlete enjoys it and will do it anyway; no need to prescribe or budget it.
  hot_weather_fallback: >
    August/September heat sometimes makes outdoor intervals impractical. Treadmill intervals at
    the gym are a legitimate substitute (and put the sauna on the way out). Prefer this over
    running a quality session in dangerous heat — treadmill pace data reconciles fine, see the
    2026-06-12 session in this file's history.
core:
  daily: "1-2 x short core routine"
```

## On the weight vest — deliberately dropped

The Champion Plan calls for weight-vest uphill hiking. That prescription exists for **mountain**
ultras with sustained steep climbing, where vest work builds the specific muscular endurance those
races demand. **Ghost Train is a flat rail trail.** The vest would buy very little here while
adding heat stress in an August/September build, altered gait, and spinal loading — for a course
that asks for none of it. The athlete's instinct that "it sounds hot" is correct.

**Recommendation: don't buy one.** The walking volume already does the durability work, and if
more stimulus is ever wanted, a slight incline is a better lever than added load.

## Travel — 2026-08-22 to 2026-09-01

**Out of state for 11 days**, landing squarely on the biggest build stretch of the block: block
week 11's Saturday long run, the whole of block week 12, and block week 13's first two days.

Constraints while away, and how the plan adapts (see `training/block.md` § "Travel weeks"):

| Lost | Adaptation |
|---|---|
| Race-course access | Nothing on-course until the Big Day (Sep 5), 4 days after returning — that session is unaffected |
| The bike trainer | Thursday x-train becomes an easy run; a hotel-gym bike or elliptical is the better substitute if one exists |
| Measured routes / track | Distance-based sessions rewritten as **time-based** so they work on any unfamiliar route |
| Reliable gym access | Bodyweight strength fallback — see `strength/notes.md` |
| A single long-run block | **Long runs split across two consecutive days**, per the athlete's own preference. Less stimulus than one long effort, but genuinely ultra-specific, and far more robust to travel logistics |

Meeting-time walking continues — the source changes (airports, exploring, hotel treadmill) but the
weekly ramp target and the 15%/week cap still apply.

```yaml
travel:
  - start: 2026-08-22
    end: 2026-09-01
    affects_block_weeks: [11, 12, 13]
    course_access: false
    trainer_access: false
    gym_access: uncertain
    long_runs: split_across_two_days
```

## Crewing — UNCREWED (athlete decision, 2026-09-07)

**He is running this race uncrewed.** Directive, not an inference: *"Assume uncrewed. I might have
a pacer for one lap."*

**This file and `races/2026-10-17-ghost-train.md` were written throughout on an assumption of crew
contact every ~12km.** `grep -l crew` returns 19 files. Everywhere "crew stop" or "crew bag"
appears, read **self-serve drop bag**, at the start/finish and at the 7.5mi turnaround — both of
which take drop bags (athlete-confirmed) and both of which are full-service aid stations.

**The logistics are covered by the race itself**, which on a looped, well-stocked course is close
to the best case for running solo:

| station | position | stock |
|---|---|---|
| **Start/finish** | 0 / 15mi | full — *"all kinds of good food"*, candy, soda, Tailwind; **drop bag** |
| mid-out | 3.75mi | snacks and drinks, candy/soda/Tailwind |
| **7.5mi turnaround** | 7.5mi | full — *"all kinds of good food"*, candy, soda, Tailwind; **drop bag** |
| mid-back | 11.25mi | snacks and drinks, candy/soda/Tailwind |

Consequences already established: warm savoury food needs no crew capability because the end
stations serve it (`log/2026-09-06.md` § Fueling); the carry drops to one inter-station gap plus
reserve rather than thirty hours of gels; and battery restock happens at every drop-bag pass,
~12.1km apart, which is what his run-to-empty light policy assumes.

### What uncrewed actually costs is judgement, and there is one dose of it available

Logistics are solved. What crew also supplies in a 30-hour race is a second brain at the hour the
first one stops working, and the race file leans on that harder than it looks — its continue/stop
decision tree is written to be *"evaluated at every crew stop"* and includes a cognition check for
slurring and poor coordination. **Those are the symptoms the sufferer cannot self-assess.**

**A pacer for one lap is possible and is the single dose of external judgement he will have.**
Spend it accordingly:

- **Put the pacer on a deep-night or late lap, not an early one.** Laps 1-3 he will be lucid and
  the pacer adds nothing but company; laps 5-6 are the *"fatigue plus sleep pressure plus
  darkness"* state the whole block has been built around, and that is when a second opinion on
  feet, cognition and the stop decision is worth most. Full darkness runs **18:30 to 06:35**.
- **The rule is confirmed and it does not bind.** Athlete, 2026-09-07: pacers are allowed
  **from lap 2 onward** (*"not before the second lap, but it's a relaxed race and nobody is going
  to care"*). Lap 2 begins around 24.1km, roughly 3-4 hours in — early Saturday afternoon —
  while full darkness does not start until **18:30**. **Every lap worth pacing is already legal**,
  so the recommendation above needs no latitude from anyone and no exception to rely on. Rule and
  plan agree; enforcement is moot.
- **The decision tree needs rewriting as a self-check regardless.** One paced lap out of five-plus
  does not cover the other four. It should become something fixed and carried — a card in the drop
  bag — not a paragraph to be evaluated by judgement at the exact hour judgement has degraded.

## Course access — a major asset

**Has training access to the northern 6.5 miles of the actual Ghost Train course.** Only the first
mile — the southern end, nearest the race start/finish — is closed outside race day. This is
unusually valuable and the plan exploits it: key sessions run on the real surface with the real
7.5mi turnaround, rather than being approximated locally.

**What this geometry means for training:**

```
race day    START(0mi) ---- aid(3.75) ---- TURNAROUND(7.5mi) ---- back ---- START   = 15mi lap
             └─ closed ─┘
training              STAGE(1mi) --------- TURNAROUND(7.5mi) --------- STAGE
                      └────────── 6.5mi each way = 13mi / 20.9km ──────────┘
```

- A **training out-and-back is 20.9km (13mi)**, not the full 24.1km race lap. Sessions that need a
  true race-lap distance add a short out-and-back from the staging point to top up.
- **The 7.5mi turnaround is accessible**, so the actual turnaround — the thing you hit 12+ times on
  race day — can be rehearsed for real.
- **Crew contact in training lands every 10.5km** (staging point ↔ turnaround) versus every 12.1km
  on race day. Close enough that fueling and crew-stop cadence transfer directly.
- The closed first mile is the one section that will be fresh on race day. It's also the section
  already run in the prior 50k here, so it's familiar rather than unknown.

**Heavy tree canopy over essentially the whole accessible section** (athlete-confirmed
2026-09-07: heavy shade for all but ~1000ft of a 22.6km session). Two standing consequences:
**heat is largely neutralised here** — measured at `shade_pct: 98` on 2026-09-07, WBGT 65.7F
against 70.1F for the same hours fully exposed, so a sunny 76F day on this ground is not the
session that number implies elsewhere; and **it is very dark at night**, admitting no sky glow or
moonlight, which sets the lighting requirement for night sessions and race night higher than
generic night running would (`log/2026-09-06.md` § lighting).

**The course is 10 minutes away**, so travel is not a meaningful constraint — it's effectively
the home training ground, and long runs should default to it rather than treating each trip as a
budgeted expense.

**The athlete's established resupply setup**, which the plan builds on rather than reinventing:

```
  south end of                  CAR                    DROP BAG          north terminus
  accessible section        (resupply hub)                              (7.5mi turnaround)
        |------- 3km -------|--------- 5km ---------|------ 2.5km ------|
        |<---------------- 10.5km accessible section ------------------>|
```

- **Car parked on the trail ~3km north of the southern end** of the accessible section — the main
  resupply point, and the natural start/finish for training sessions.
- **Drop bag ~2.5km from the northern terminus.**
- From the car: north terminus and back = **14.9km** (drop bag passed twice); south end and back
  = **6km**; the full accessible out-and-back = **20.9km**, passing the car mid-session.
- Net effect: resupply every 3–5km in training, versus aid roughly every 6km on race day. The
  existing setup already approximates race aid density — no need to engineer anything new.

```yaml
course_access:
  available: true
  coverage: "northern 6.5mi (mile 1 to the 7.5mi turnaround); first mile closed outside race day"
  travel_min_each_way: 10
  car_resupply_km_from_south: 3
  drop_bag_km_from_north_terminus: 2.5
  full_accessible_out_and_back_km: 20.9
```

## Equipment

```yaml
equipment:
  suunto_watch: true
  bike_trainer: true                # used during meetings
  emtb: true                        # unplanned, active-recovery only
  road_bike: true                   # unplanned group rides
  incline_walking_pad: null         # unconfirmed — optional, not load-bearing for the plan
  weight_vest: false                # NOT RECOMMENDED for this build — see note below
  gym_access: true                  # for strength/program.liftoscript
  headlamp: "4 available"           # legacy stock; the race setup is the two lights below
  sweat_rate: "low-average"         # informs sodium at the lower end of typical — see rules/fueling.md
```

### Night lighting — rebuilt after the 2026-09-06 failure (recorded 2026-09-08)

The old setup died mid-session: two of three lights flat inside **4h26** of darkness, against
**~12.1 hours** on race night (`log/2026-09-06.md`). Replaced with a two-light, one-cell system.

| role | light | notes |
|---|---|---|
| **Handheld — wildlife spotting** | **Convoy S3**, 18650, **4000K high-CRI** (719A emitter, Nichia-519A class) | Throw. Used intermittently |
| **Chest — running light** | **Zebralight H600Fc Mk IV**, 4000K high CRI | Frosted = pure flood, no hotspot. Chest mount gives ground texture that head-height light flattens. **NOT YET IN HAND** as of 09-08 |
| **Cells** | **Panasonic NCR18650GA ×10** | ~3500mAh, flat-top unprotected. Chosen specifically so one cell type feeds both lights |

**WHY HIGH CRI OVER BRIGHTNESS — the athlete's reasoning, and it is better than the generic
argument.** 2026-09-08: *"high CRI is more important than brightness since the porcupines hide in
the brush to the side of the trail so I have to pick them out by color."*

**That is a colour-discrimination task, not an illumination one.** Picking a brown animal out of
brown brush at the trail edge is not solved by more lumens — it is solved by rendering the colour
difference between animal and vegetation, which is exactly what CRI measures. He has had several
night-time porcupine encounters on this course; on 09-06 one of them forced him to slow enough to
contaminate the session's pace average. **Accept the 10-20% output penalty high-CRI neutral emitters
carry. It buys the thing the light is actually for.**

**Cell standardisation is the point of the whole system.** One cell type means every spare is
fungible in either light — no sorting in the dark with cold hands, which is what a mixed-format kit
costs at 03:00. Two spares carried on the body; the night's full supply in the drop bag, restocked
at every pass (~12.1km apart, ~7 passes across the night).

**Policy: run cells to empty, swap reactively** (athlete decision 2026-09-07 — see
`log/2026-09-06.md` for why scheduled swapping was rejected: it wastes partial charge and needs
*more* cells, and redundancy already means a dead light is never darkness). **One exception —
start the dark section on fresh cells.** Beginning 12 hours of night on a part-used cell is the one
avoidable failure here, and dusk is a drop-bag point in daylight.

**Open items:**
- **Low-voltage protection, and it interacts with run-to-empty.** The GA is an *unprotected* cell,
  so nothing in the battery stops an over-discharge — the light has to. Zebralight has LVP built
  in; whether the Convoy's driver does depends on the driver. **Worth confirming before running a
  cell flat in the Convoy on purpose**, or the cost of the test is a damaged cell that is then
  unsafe to recharge.
- **What goes on his head.** The H600Fc is pure flood on the chest; a chest light alone leaves
  nothing where he turns to look. A dim headlamp alongside solves it and he already owns four.
- **Measured runtime at working brightness**, which is what the 09-12 session exists to produce.
  Rated figures are not the number.

### Chafing — no history of it; shields are cheap insurance (recorded 2026-09-07)

**He has had no failures or near-failures with nipple shields.** Athlete's own words, correcting
an earlier draft of this section: *"It's just cheap insurance if I do start having problems to
have a pair where I might need them."*

**Recorded so it is not misread later.** He stages two spare pairs in each drop bag, and a first
version of this section read four staged pairs as evidence of a recurring problem. It is not.
**Provisioning is not history** — a cheap, weightless item staged redundantly says something about
the cost of carrying it, not about how often it has been needed. Chafing is currently a
**non-issue** for this athlete and there is no data suggesting otherwise.

Two notes that survive anyway, both cheap:

- **Adhesive fails when wet**, and mid-October in NH across 30 hours makes rain or heavy dew live.
  If shields are ever going to be needed it is on a wet night, on skin that has been sweating for
  hours — not on a fresh application.
- **The Aquaphor already staged in both bags is the fallback**, with tape behind it. Nothing extra
  needs staging.

## Footwear — the Mont Blanc runs small

### The rotation (recorded 2026-08-15 — none of this was in the repo before)

| shoe | size | use |
|---|---|---|
| Altra **Lone Peak 9** ×3 | 9.5 | trail. Correct fit; the fit reference. **Three pairs** (athlete-confirmed 2026-09-07) — enough to stage one in each drop bag with a spare at home |
| Altra **Mont Blanc Carbon** | 9.5 | RETIRED for distance — too narrow |
| Altra **Mont Blanc Carbon** | **10** | trail, race candidate |
| Altra **Experience Flow 2** | **10** | road, medium-high cushion |
| Altra **Escalante** | 9.5 | road |

Note he runs **9.5 in the Lone Peak and Escalante but 10 in the Experience Flow** — size varies
by model, so "size 10" was never inherently too big. That mattered on 2026-08-15 when a size-up
hypothesis for a blister was raised and then ruled out: the 08-12 threshold session was 14min of
fast running in the size 10 Experience Flow with normal Balega socks and produced nothing.

### WHY the Mont Blanc — the thing this section never recorded

Everything below documents what has gone WRONG with this shoe. It never stated what it is FOR,
and on 2026-08-15 that gap caused an LLM session to twice recommend abandoning it. **Record the
purpose of kit next to its problems, or the next reader sees only cost.**

**The carbon plate and thicker foam are a deliberate play for less trail feel and less soreness
after distance**, and measured against that it is working:

- **Zero general foot soreness after 23.5km** on 2026-08-15. Athlete: *"that would be unthinkable
  in the Lone Peak."*
- **Zero toe-joint pain** — the 9.5's reliable signature, absent in the 10.
- Less general leg soreness than the Lone Peak produces by 20km.

Feet are the primary attrition mechanism in a 30-hour race — `races/2026-10-17-ghost-train.md`
makes "feet: hot spots vs actual damage" one of six go/no-go criteria at every crew stop. A shoe
that eliminates foot soreness at 23.5km is winning the axis that decides the race, and losing one
that tape and sock choice can fix. **"Correct fit" (Lone Peak) and "right for the job" are
different axes and this file used to conflate them.**

The Lone Peak's role is therefore the **backup in the start/finish crew bag** — the shoe to
switch into if the Mont Blanc's toe box goes wrong, or late when feet swell — not the standard
the Mont Blanc must justify itself against. Race-day swap logic: stay in the Mont Blancs while
the feet are quiet, swap on the toe box talking or visible swelling, NOT at a scheduled lap.
~~Rehearse the swap at the Big Day, which already has three crew stops.~~ **Superseded
2026-09-07.** The Big Day was never run (`log/2026-09-05.md`); the swap is unrehearsed, and the
next opportunity is lap sim 1 on 2026-09-19. The race is now **uncrewed** — see § Crewing above —
so "crew stops" here means a self-serve drop bag; three pairs of Lone Peak 9.5 make staging one
at each bag straightforward.

**Altra Lone Peak 9, size 9.5 — correct fit.** The reference shoe.

**Altra Mont Blanc Carbon, size 9.5 — TOO SMALL for long distance.** Same nominal size, noticeably
narrower last. The 2026-08-02 30k in these produced blisters on both 2nd toes (where they meet the
tip of the 3rd toes) and, the following day, soreness in the toe joints nearest the ankle.

**One mechanism explains both: compression.** The athlete's own description — "felt like my foot had
been crushed together from the narrow last" — accounts for the blisters at the toe contact points
and the joint soreness together. His call, and it is the right one: **not an injury, just soreness**,
and a signal about distance rather than a health flag. Recorded here rather than under Injuries for
exactly that reason.

**The actionable constraint: don't run 30K+ in the Mont Blanc at 9.5.** Shorter runs are fine.

**Sizing up to 10** to see whether that removes the limit.

**Checkpoint 1 PASSED — morning-after verdict, 2026-08-10.** Blisters not worse, and zero
toe-joint pain after 14.2km — the joint symptom the 9.5s produced reliably is absent in the 10s.
The compression hypothesis holds. Next checkpoint: a ~30km run (Saturday 08-15 is the natural
slot), the distance class that broke the 9.5s. Until then the 10s are cleared to ~15km.

**First test of the 10s — 2026-08-09, 14.2km: mixed at the time, resolved by the morning.** Running feel: great,
athlete's word. But hotspots developed, and the still-healing 08-02 blisters (both 2nd toes) felt
"like they might become a problem" by the end. Next-morning foot state decides. If the blisters
reopen at 14km in the bigger size, the fit hypothesis weakens and the shoe — not the size — becomes
the suspect for long distance. If compression is the whole story — and
it fits the evidence cleanly — a size up should fix both symptoms.

**ONE INCIDENT, NOT A RECURRING PROBLEM — athlete correction 2026-08-12.** This matters enough to
state before any of the detail below. The blisters are a **single event on 2026-08-02, in the
9.5s, that has not finished resolving.** They are not a pattern, not a chronic issue, and — most
importantly — **the size 10s have never produced a blister.** An earlier version of this section
was drifting toward treating friction as a standing characteristic of this athlete and toward
prescribing sock and taping interventions off n=1. That is the same over-generalisation the
run/walk rule got corrected for: an observation promoted to a constraint by being written down.
Do not do it here. Until a SECOND blistering event occurs, in the 10s, there is no pattern to
manage and no kit change to justify.

**Healing rate — added 2026-08-12.** Still present at **day 10-11**: tiny, painless, improving
slowly. A normal blister closes in 3-7 days. The likeliest explanation is not slow healing but
**continuous re-irritation** — since 08-02 they have absorbed 14.2km, 10.1km and a 7x2min
threshold session, with never more than a single rest day in a row. Read a lingering blister as a
question about what it has been asked to absorb since, not about the skin. This is an observation
about *this* blister, not a standing rule.

> ## ✅ RESOLVED 2026-09-06 — checkpoint 2 passed. Read this box before the section below.
>
> The test specified below was **not** delivered by 08-15, which was run in toe socks — the one
> kit change this protocol forbids — and blistered at the callus margins. It was delivered
> instead by an unplanned **30.08km on 2026-09-06** (`log/2026-09-06.md`), which met every
> condition set out here: Mont Blanc **10**, ~30km, **Balega Hidden Comfort rather than toe
> socks**, no tape, Aquaphor between the toes, run to race strategy on the race course.
>
> **Result: no blisters, no hotspots — neither mechanism recurred.** The "new blister in a new
> location" signal named below did not fire.
>
> **The 10s now have one clean pass in the ~30km class**, at race-representative pace. This
> establishes checkpoint 2, not the race: 30km is 19% of 160km, feet swell over 20+ hours, and
> the callus-margin mechanism needs accumulated shear. **Lap sim 1 (2026-09-19) is the next
> session long enough to move it.**
>
> Two variables separate 08-15 from 09-06 — toe socks out, lubricant in — alongside far less fast
> running, so which change did the work is not isolated. It does not need to be: the working
> combination is known and free to repeat.
>
> The section below is kept as written because it is the protocol that was finally followed, and
> the reason the result is trustworthy.

**What Saturday actually tests.** Checkpoint 2, the ~30km class that broke the 9.5s. The residual
blister is a leftover from a **retired shoe**, so it is a confound to note rather than the subject
of the test:

- The clean question is "does the Mont Blanc 10 carry 30km" — and the 10s have a perfect record
  so far (checkpoint 1 passed, zero toe-joint pain, no new blistering).
- If the old blisters worsen, that reads as "30km on a 13-day-old unhealed spot," which is NOT
  the same finding as "the Mont Blanc 10 fails at 30km." Keep the two separate in the log.
- A NEW blister, in a new location, would be the real signal.

**Run Saturday in the 10s with nothing new.** Deferring costs more than it saves — block weeks 11
and 12 are travel weeks whose longest runs are 120min and 94min, so the next 30km+ opportunity
after 08-15 is the Big Day itself (09-05, a 50k on course), the worst possible place to discover a
shoe fails. Lubricant between the toes is fine if wanted: it adds no bulk and costs nothing to be
wrong about. **Do not add toe socks, tape or any other kit change for this run** — tape in
particular adds bulk to a toe box whose failure mode was compression, and changing two variables
at once on the one 30km slot available would waste the test. Kit changes belong to the block-week-16
decision, informed by data, not ahead of it.

**The fallback is already in hand:** the Lone Peak 9.5 is the reference shoe with correct fit, so
a Saturday failure costs a shoe choice, not the block.

### TWO blister mechanisms, not one — separated 2026-08-15

These had been getting conflated. They are different problems with different fixes:

| | location | skin | mechanism |
|---|---|---|---|
| **08-02**, Mont Blanc **9.5** | both 2nd toes, at 3rd toe contact | clean | **compression** — narrow last, toe-on-toe |
| **08-15**, Mont Blanc **10** | outer edge, both big toes | **at a callus margin** | **shear at a stiffness discontinuity** |
| **09-06**, Mont Blanc **10**, 30.08km | **none** | — | **neither mechanism fired.** Balega Hidden Comfort + Aquaphor between the toes, no toe socks, race-strategy pace |

**The compression problem was actually fixed by sizing up.** 23.5km including 24min at
5:15-5:32/km in the 10s and the 2nd-toe blisters did not recur.

**CALLUSES ARE THE UNDERLYING SUBSTRATE, and they are not armour.** The 08-15 blisters formed
directly above well-developed calluses extending up from the underside of the big toes. Blisters
form at the MARGIN of a callus, never on it: the callus is stiff and inelastic, the skin beside
it is not, and shear concentrates at the boundary. The 08-02 blisters were on clean skin —
athlete-confirmed — which is what separates the two mechanisms.

So the 08-15 blister is a **skin** problem that any shoe would eventually find, not a shoe
problem. Toe socks and 5:15/km pace supplied the shear; the callus decided it blistered rather
than merely complained. Every callus edge on his feet is a blister waiting for enough shear, and
a 160km race supplies plenty.

**CURRENT ROUTINE (athlete-confirmed 2026-09-08):** light sanding of the calluses, plus **Dr
Scholl's Ultra Exfoliating Foot Lotion** — a urea product, which is keratolytic at high
concentration and a humectant at low, so it does callus reduction and pliability together. This
matches the prescription below.

**One caution: that is two mechanisms at once**, mechanical and chemical, against a prescription
whose whole point is *gradual*. Doubling up is the easy way to overshoot without noticing. If the
skin turns tender or pink rather than simply thinner, back off the sanding and let the lotion work
alone. **The two halves separate on 10-03:** stop the aggressive work two weeks out, keep
moisturising through race week. Pliable skin on race day, not recently-sanded skin.

**Highest-value foot work available, and it is free:** reduce the calluses gradually — light
filing or pumice after showers, a little at a time over weeks, never one aggressive session
(freshly thinned skin is worse than the callus). Keep the skin pliable with a urea-based cream so
it deforms with the surrounding tissue instead of tearing at the seam. Start now; stop aggressive
work ~2 weeks out from the race. This outranks the shoe decision.

**Do not wear toe socks in the Mont Blancs.** Toe socks add width between every toe, and in a last
whose known defect is narrowness that pushes the outer toes into the shoe walls. Secondary to the
callus work now, but free to obey.

### Toenails — a standing baseline, NOT a fit signal (recorded 2026-09-07)

**His big-toe nails are sore past ~20km, in any shoe, and always have been.** Athlete's own
words: *"the nail pain is something that I have always experienced. It's not my toenails hitting
shoe ... my big toe always feels sore in the toenail no matter what,"* and *"the only variable is
distance. Once I go above 20k I get some nail pain."*

- **The nail is not striking the toe box.** He has investigated that specifically and ruled it
  out. The pressure is on the nail bed **from beneath**.
- **It varies with distance, not with footwear**, so it carries **no information about fit** and
  must not be read as one. Every long run in this file is over 20km, so nail soreness is expected
  on all of them — a signal that fires on every row cannot separate the rows. A session in
  2026-09 read it as a too-small-shoe signal and had to withdraw that.
- **His nails are already bruised** from previous Lone Peak runs, and he regards losing toenails
  as routine for him. He starts the race with damaged nails; that is the baseline, not a change.
- **NOT a go/no-go criterion.** `races/2026-10-17-ghost-train.md` makes "feet: hot spots vs actual
  damage" a stop check. **Big-toe nail soreness is neither** — he crosses 20km inside lap 1 of 7
  and spends ~80km above onset at the A-goal, so treating it as a stop signal would burn time and
  possibly a needless shoe change on something that was always going to appear.
- **Unknown and worth more than anything else here:** whether it plateaus past 20km or scales
  with distance. At 30km he called it *"a little."* The unasked data point is his 50k on this
  course three years ago, and whether he lost the nail then.
- **Do not attempt a large stride change before this race.** He has proposed one, and the
  mechanism reasoning is sound — plantar loading through the hallux is what stride governs. The
  objection is timing: six weeks out, with an active ITB and a history of tissue limiters, a gait
  overhaul redistributes load onto achilles, plantar fascia and calf during taper, with the payoff
  arriving long after October. **The small, already-proven version is the cadence lever below**
  (raise 5-10%), which shortens stride without rebuilding anything. The gait project is a good
  off-season question.

### Blister kit (recorded 2026-09-08)

**Leukotape P ordered 2026-09-08 — one roll per drop bag**, start/finish and the 7.5mi
turnaround, so a foot problem can be dealt with at whichever stop it surfaces at rather than
carried to the next one. Rigid zinc-oxide strapping tape — the right class for this,
because a blister is a shear injury and the tape's job is to take the shear instead of the skin.
Elastic tape (kinesiology tape, RockTape) is the wrong tool: it stretches with the skin and
transmits the shear straight through, and its adhesive lifts once a foot is properly wet.

**Tape alone is not a kit.** Four things complete it, and one of them is not optional for him:

| item | why |
|---|---|
| **Alcohol wipes** | **The critical one.** He lubes between every toe with Aquaphor, and tape will not stick to a lubed foot. Skipping the degrease is the usual reason tape fails. **Ordered 2026-09-08: MagiCare 75% alcohol sanitizing wipes** — see the caveat below |
| Sterile needle or safety pin | Draining |
| Small scissors | Cut to shape — pre-cut strips at home, for cold hands at 03:00 |
| **Non-adherent pads** (Telfa-type), 2 per bag | **Only for a deroofed blister** — they exist so the dressing does not bond to raw dermis and tear it off on removal. Ordinary gauze sticks to a weeping wound. Unused in branches 1-3, where tape goes straight on skin. Second job: the dry-wipe for bulk grease |
| **Skin-Tac wipes** | Tackifier — makes tape grab skin that is not perfectly clean. See the degreasing note below |
| **Gloves, individually wrapped** (athlete, 2026-09-08) | **Use nitrile, not latex — petrolatum degrades latex.** Their real job is not hygiene but breaking the re-contamination loop: bare fingers carrying Aquaphor will re-grease a toe that was just degreased, defeating the whole sequence. Also correct for anything involving a needle and broken skin when uncrewed with nowhere to wash. Slightly oversized goes on far easier over damp hands at 03:00 |
| **Small ziplock** | Trash pocket for used gloves and wipes — he is standing at his own drop bag, not an aid-station table |

**Skin-Tac chosen over tincture of benzoin (2026-09-08), on format.** Both are tackifiers. Benzoin
is slightly stickier under extreme sweat but is more irritating, smells, and is a mess in a bag
being rummaged in the dark. Skin-Tac comes in individually foil-wrapped wipes: no leak, single-use,
workable with cold hands at 03:00.

**Use, in one decision with four branches:**

1. **Hot spot, no fluid** — dry, wipe with alcohol, tape smooth, change the sock if wet. **This is
   the branch that matters**; a two-minute fix at 40km is a blister at 55km.
2. **Blister, roof intact, small, painless** — leave it, tape over to stop it spreading. Intact
   skin is the best dressing available.
3. **Blister, painful or large or still being loaded** — drain but **keep the roof on**: alcohol,
   pierce at the *edge*, press out, leave the flap, tape over. The roof is sterile cover and hurts
   far less than raw dermis.
4. **Already torn** — clean, antiseptic, non-stick gauze, tape. This is the race-ending one, which
   is the whole argument for fixing branch 1 promptly.

**Technique that decides whether any of it works:** clean, dry, degreased skin, **no wrinkles**. A
wrinkle in the tape is a new pressure point — it makes things worse, not better.

**Degreasing Aquaphor is harder than it looks, and worth testing rather than assuming.** Aquaphor
is petrolatum-based — a nonpolar hydrocarbon — and alcohol is a polar solvent, so it lifts
petrolatum only moderately well. 75% alcohol is a quarter water, which cuts the solvent action
further. Two things follow:

1. **Dry-wipe the bulk off first**, then alcohol, then **let it flash off completely**. Tape on
   damp skin does not stick. The two-step is what makes one wipe plausible; alcohol alone on a
   greasy toe is not.
2. **Check the wipes for emollients.** Hand-sanitiser wipes commonly carry glycerin or aloe as
   skin conditioners, which leave their own film and defeat the purpose — degreasing and
   re-greasing in one motion. If the ingredient list has them, **plain 70% isopropyl prep pads**
   (the medical kind, alcohol and nothing else) are the purpose-built tool and cost almost
   nothing. *Not verified for the specific product ordered — the ingredient list is the check.*

3. **Carry a tackifier and stop fighting for a clean foot.** Chemically, surfactant lifts
   petrolatum better than alcohol does and 91% IPA beats 75% — but none of it produces a properly
   clean foot in a parking lot at 03:00. **Skin-Tac makes the tape grab anyway**, which solves the
   real problem rather than the chemistry problem.

**Sequence: dry wipe → alcohol pad → Skin-Tac → tape.** The tackifier is an addition to the
degrease, never a replacement — Skin-Tac over Aquaphor still fails.

**Removal caution:** more adhesion means more force coming off, and feet after a hundred-miler are
macerated. Pull slowly, wet the tape if stubborn, do not rip. Well-stuck Leukotape can take soft
skin with it.

### The better move: pre-tape the known sites before the start

**This sidesteps the degreasing problem entirely for everything predictable.** Tape the two sites
he has actually blistered — big-toe callus margins and 2nd toes — at home, on clean dry skin,
unhurried, before the race. Then lube *around* the tape rather than under it. The mid-race kit
becomes a surprises-only kit.

**It needs testing first**, because this section's own warning cuts against it: tape adds bulk to a
toe box whose failure mode was compression, and 08-02 failed by compression. **2026-09-12 is the
slot** — test the whole stack at once (wipe, Skin-Tac, tape, pre-taped sites) rather than one
variable at a time, since the question is "does it hold," not which layer did the work.

**The five-minute test that settles the degreasing question:** Aquaphor on a toe, one wipe, tape
over it, see whether it holds. Kitchen, tonight — worth more than any reasoning here.

**Caveat specific to this athlete, and it is in tension with the rest of this section:** the note
above warns that *"tape in particular adds bulk to a toe box whose failure mode was compression."*
His blister sites are the toes, inside a known-narrow last, and 08-02 failed by compression. **If
he intends to tape toes on race day, test it on a long run first** rather than discovering the
trade-off at hour 6.

**And the kit is the fallback, not the plan.** The callus reduction described above is the
prevention. **Athlete-confirmed 2026-09-08: it started a while back and is ongoing.** It had never
been written into `log/`, and a 2026-09-08 note here wrongly read that absence as the work not
happening — corrected. Nothing in the log is evidence about anything the log was never asked to
record. Aggressive work stops ~2 weeks out (**10-03**); light maintenance can continue past that.

Standing rule: log blistering by **location and symmetry**, not just presence. Bilateral and
specific points at fit; unilateral points at gait, camber, or a lacing/sock issue.

## Working days — walking only happens on these

Meeting-time walking is done during work calls, so it lands on **working days only**: Mon–Fri,
minus paid holidays. The weekly target in each `endurance/*-meeting-walk-week.md` therefore divides
across ~5 days, not 7 — and across 4 in a week containing a holiday, which raises the per-day
requirement sharply. Block week 14 (Sep 7–13) contains **Labor Day, Mon 2026-09-07**: its 355min
target lands on four days, i.e. 89min/day rather than the 51min/day a 7-day split implies.

Paid holidays: New Year's Day, MLK Day, Presidents' Day, Good Friday, Memorial Day, Independence
Day, Labor Day, Thanksgiving, the Friday after Thanksgiving, Christmas.

**Observance rule (athlete-supplied):** a holiday falling on a weekend is observed on the **Friday
preceding that weekend**. This deliberately differs from the US federal convention, which shifts a
Sunday holiday forward to the Monday — don't "correct" it.

Implemented in `.claude/skills/daily-brief/scripts/brief_context.py` (`observed_holidays`,
`working_days`), including the movable-date computation for Good Friday.

## Injuries / constraints

### ITB, left — recurring, distance-dependent (first recorded 2026-08-15)

**Lateral left knee, side of the kneecap, "feels like tight IT band."** NOT patellofemoral —
the athlete was asked to distinguish and this is the ITB answer. Onset around 20-25km.

**It is recurring and it is not the shoes.** He has had the same thing in the Lone Peaks at
~25km in a 30k. On 2026-08-15 it arrived at ~20km — five kilometres early — and the likeliest
candidate is the 14 minutes at or above LTHR banked in the first 72 minutes of that run.
n >= 2, in two different shoes, so this meets the bar for a pattern that the 08-02 blisters
did not.

**It is UNILATERAL, which is the most informative thing about it.** This file's own standing
rule for blistering applies: bilateral points at equipment, unilateral points at gait, camber or
asymmetry. Left only, on flat trail, means something about him is asymmetric.

**The direct prehab lives in Lower B** — unilateral work, glute and hip stability; hip abductor
weakness is the classic ITBS driver. That does not override "Priority when time is short", but
it does change what Lower B is worth: it is no longer just accessory volume, it is the specific
countermeasure to the block's one recorded injury.

**Mid-run management** (established 2026-08-15, and it worked): raise cadence 5-10%, walk every
descent, stay off camber. Stop running the moment gait changes — compensation is how one sore
knee becomes a hip and an achilles.

None other recorded. Log anything that affects session selection here, and reference it from
`rules/progression.md`'s readiness ladder.

### If something actually hurts — DRAFT, needs athlete confirmation (raised 2026-08-13)

**The cut order does not govern pain.** `rules/strength-authoring.md`'s lifting-first rule answers
"what do I drop when time or recovery is short." That is a scarcity question. Pain is a different
category and the repo had no branch for it at all until the athlete asked — this section is the
gap he found, drafted for his confirmation rather than assumed.

**First, separate soreness from pain.** `rules/logging.md`'s scale already does this: 1-3 green
(and per the baseline note below, gastroc/soleus in that band is routine for him and means
nothing), 7+ red, 9-10 "sharp, localized, or getting worse day over day — this is an injury
signal, not soreness."

**If it is tendon pain — achilles being the realistic one here — the athlete's instinct is right
and it inverts the usual cut.** Cut the RUNNING and keep loading the tendon:

- Tendons remodel in response to load. Complete rest de-loads them, and pain typically returns on
  the return to running because nothing got stronger in the interim.
- Running is the provocation — impact plus the stretch-shortening cycle. Controlled calf work is
  not.
- So: drop or shorten the runs, keep the calf raises, and if anything bias them heavier and
  slower. Isometric holds are frequently useful early. **Lower B's single-leg calf raise stops
  being the thing to cut and becomes the thing to keep** — which is the one case where lifting
  outranks running, and it is a rehab decision, not a training-priority one.

**The exception that matters more than the rule: DO NOT load through suspected bone stress.**
This is the failure mode where "keep loading it" is actively dangerous, and this block is exposed
to it — `rules/progression.md` already names the walking ramp (180 -> 465 min/wk over nine weeks)
as the single most likely source of an overuse injury here. Rough triage, and it is triage, not
diagnosis:

| | tendon-like | bone-stress-like |
|---|---|---|
| morning | stiff, worst on first steps | not especially |
| during activity | **warms up and eases** | **worsens as you go** |
| location | along the tendon, diffuse | pinpoint on bone, tender to press |
| single-leg hop | uncomfortable | **sharply painful** |
| at rest / at night | quiet | aches |

Anything in the right-hand column: **stop, do not load, and get it imaged.** Running through a
bone stress reaction is how a season ends.

**This is training-practice guidance, not medical advice, and it is written by an LLM.** Pain that
is sharp, one-sided, worsening day over day, or still present after ~2 weeks of sensible
management belongs with a physio or sports doctor, not with this file. Record what they say here
and it becomes the constraint everything else is authored against.

**Baseline characteristic (2026-08-05):** gastroc/soleus soreness in the 1-3 (green) range is
routine for this athlete — "par for the course," his words, not a signal of anything going wrong.
`rules/logging.md`'s soreness scale is generic; read a green-band calf reading alone as noise, not
an early-warning sign. What would actually be new information: calf soreness reaching amber (4-6)
or higher, soreness anywhere else that isn't normally sore for him (arches/plantar in particular,
per the walking-ramp overuse risk below), or a sharp/one-sided reading per the scale's own anchors.
