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
  long_run_exception_max_min: 400  # absolute ceiling even for flagged sessions
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
    - 2026-09-11  # night run past midnight
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
  headlamp: "4 available"           # no shortage; pick two for the race + spares in the crew bag
  sweat_rate: "low-average"         # informs sodium at the lower end of typical — see rules/fueling.md
```

## Footwear — the Mont Blanc runs small

### The rotation (recorded 2026-08-15 — none of this was in the repo before)

| shoe | size | use |
|---|---|---|
| Altra **Lone Peak 9** | 9.5 | trail. Correct fit; the fit reference |
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
Rehearse the swap at the Big Day, which already has three crew stops.

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

**Highest-value foot work available, and it is free:** reduce the calluses gradually — light
filing or pumice after showers, a little at a time over weeks, never one aggressive session
(freshly thinned skin is worse than the callus). Keep the skin pliable with a urea-based cream so
it deforms with the surrounding tissue instead of tearing at the seam. Start now; stop aggressive
work ~2 weeks out from the race. This outranks the shoe decision.

**Do not wear toe socks in the Mont Blancs.** Toe socks add width between every toe, and in a last
whose known defect is narrowness that pushes the outer toes into the shoe walls. Secondary to the
callus work now, but free to obey.

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
