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
    - "sat afternoon"
    - "sun afternoon"
```

## Meeting time — a separate, mostly-free budget

Meeting time (work calls) can be spent on the bike trainer (aerobic base, non-impact) or walking
(time on feet, race-specific durability). Neither counts against `weekly_total_max_min`, but both
count against recovery — see `training/block.md` § "Three training currencies" for the full
reasoning on why walking is prioritized.

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
    # Planned per-block-week totals (min), respecting the cap and tapering into race week:
    # wk9 180 | wk10 205 | wk11 235 | wk12 270 | wk13 310 | wk14 355
    # wk15 405 | wk16 465 | wk17 465 (hold) | wk18 300 (taper) | wk19 150 (race week)

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

**Altra Lone Peak 9, size 9.5 — correct fit.** The reference shoe.

**Altra Mont Blanc Carbon, size 9.5 — TOO SMALL, and it produced a joint symptom.** Same nominal
size, tighter last. The 2026-08-02 30k in these produced two things, and **the second matters more
than the first**:

1. **Blisters** on both 2nd toes where they meet the tip of the 3rd toes, still present four days
   later. Bilateral damage at one specific point is a fit problem — technique and mileage don't
   select a matching pair of toes.
2. **Bilateral toe-joint pain the following day, in the joints nearest the ankle** — and the athlete
   has **never experienced this in any other shoe**. That combination (new, bilateral, symmetrical,
   shoe-specific, load-related) is the profile of a mechanical cause, and it is a joint signal
   rather than a soft-tissue one. `rules/logging.md`'s scale treats sharp or localized symptoms as
   an injury signal rather than soreness, and this belongs in that category even though it resolved.

Blisters are a nuisance you can tape. A novel bilateral joint symptom is not, and it should drive
the shoe decision — not the blisters.

**Sizing up to 10 in the Mont Blanc.** That is the right first move — a too-short toe box explains
the blisters directly, and jammed toes plausibly explain joint loading too.

**But do not assume sizing fixes the joint symptom.** The Mont Blanc is carbon-plated, and a stiff
forefoot plate changes where load concentrates through the foot regardless of length. If the joint
pain returns in the 10, the mechanism is the shoe rather than the size, and the shoe is out for long
runs in this build — that is a different conclusion from "needs more break-in", and the plan should
not spend weeks discovering it slowly.

**If the joint symptom recurs, get it looked at rather than iterating on shoes.** Bilateral
load-related midfoot/forefoot joint pain in a build with rising volume is worth a professional
opinion; nothing in this repo is qualified to distinguish an irritated joint from an early stress
response, and the difference matters a great deal at this point in the block.

Why this matters beyond comfort: the Mont Blanc is the carbon-plated shoe, i.e. the likely race-day
or fast-lap candidate, and `races/2026-10-17-ghost-train.md` § Shoe/sock rotation is decided in
block week 16 off lap sim 1 data. A shoe that blisters at 30k is disqualifying at 100km, and feet
are listed there as one of the four things that actually end this race. **Do not carry an unresolved
sizing question into that decision** — the size 10 needs enough long-run mileage before block week
16 to be trusted, not just tried once.

Standing rule: log blistering by **location and symmetry**, not just presence. Bilateral and
specific points at fit; unilateral points at gait, camber, or a lacing/sock issue.

**Foot/toe joints — OPEN, 2026-08-02.** Bilateral toe-joint pain in the joints nearest the ankle,
the day after a 30k in Altra Mont Blanc Carbon 9.5. Novel — never in any other shoe. Resolved since
(soreness 2 on 2026-08-06, no arch or joint complaint). Cause is presumed mechanical and
shoe-specific; see § Footwear. **Not closed:** the size-10 test is the experiment, and recurrence
means stop testing and seek an opinion rather than continuing to iterate.

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

None recorded yet. Log anything that affects session selection here, and reference it from
`rules/progression.md`'s readiness ladder.

**Baseline characteristic (2026-08-05):** gastroc/soleus soreness in the 1-3 (green) range is
routine for this athlete — "par for the course," his words, not a signal of anything going wrong.
`rules/logging.md`'s soreness scale is generic; read a green-band calf reading alone as noise, not
an early-warning sign. What would actually be new information: calf soreness reaching amber (4-6)
or higher, soreness anywhere else that isn't normally sore for him (arches/plantar in particular,
per the walking-ramp overuse risk below), or a sharp/one-sided reading per the scale's own anchors.
