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
  long_run_exception_max_min: 360  # absolute ceiling even for flagged sessions
  long_run_exceptions_per_block: 3
  sunday_b2b_max_min: 150
  weekly_total_max_min: 600        # running only; excludes meeting-time trainer/walk sessions
  doubles_ok: true                 # 40-50min easy, pre-dawn or post-bedtime
  lifting_session_min: 60          # 4x/week, 45-60min — see rules/strength-authoring.md

  protected_windows:               # when training is actually possible
    - "weekdays 05:00-06:30"
    - "weekdays 20:30-22:00"       # post-bedtime — where night-running practice goes
    - "sat 06:00-10:00"

  blackout:
    - "friday morning"             # hard constraint — conveniently doubles as the pre-long-run rest day
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
    weekly_min: 180
    session_max_min: 90
    intensity_ceiling: "Z2"        # never allowed to compete with a run quality session

  walking:
    # Ramp deliberately — jumping straight to 10h/wk invites plantar fascia / achilles injury.
    # NOTE: the ramp cap is the binding constraint, not the peak target. Starting at 180 and
    # capped at +15%/wk, the reachable peak is ~465-480 min at block weeks 16-17, NOT 600 by
    # week 15. The cap wins; the peak arrives later and lower. Per rules/progression.md, never
    # bust the ramp to hit a target number.
    weekly_min_start: 180          # block week 9
    weekly_min_peak: 465           # realistically reached at block weeks 16-17, then tapers
    weekly_ramp_max_pct: 15        # max week-over-week increase — check this every week
    style: "brisk, sustained; incline pad + weight vest = the Champion Plan's uphill/vest work"
    weight_vest_from_week: 12      # introduce gradually, after a walking base is established
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
  sessions_per_week: 2             # sauna or hot tub, 20-30 min, on Mon/Fri rest days
  available: null                  # TODO: confirm sauna/hot tub access
  note: "Aerobic/plasma-volume benefit only — race is mid-October in NH, no heat acclimation block needed"
core:
  daily: "1-2 x short core routine"
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

Sessions scheduled on the course (3 trips — deliberately limited, since each costs travel time on
top of run time, which the running budget does *not* currently account for):

| Block week | Session | Why on-course |
|---|---|---|
| 13 (Sep 5) | **Big Day — 50k = 2 full laps, evening start** | Distance, night, course and crew rehearsal in one session |
| 15 (Sep 19) | Lap Simulation 1 — 1 lap | Real segment geometry and crew stop timing |
| 17 (Oct 3) | Lap Simulation 2 — 1 lap, full dress rehearsal | Final check on the real thing |

Week 16's night long run stays local on purpose — its job is the dark→dawn transition, which
doesn't need the course, and a 4th trip isn't worth the travel.

```yaml
course_access:
  available: true
  coverage: "all but the final mile"
  travel_min_each_way: null        # TODO: fill in — this is real time the budget doesn't yet model
```

## Equipment

```yaml
equipment:
  suunto_watch: true
  bike_trainer: true                # used during meetings
  emtb: true                        # unplanned, active-recovery only
  road_bike: true                   # unplanned group rides
  incline_walking_pad: null         # TODO: confirm — needed for the meeting-walk/vest lever
  weight_vest: null                 # TODO: confirm
  gym_access: true                  # for strength/program.liftoscript
  headlamp: null                    # TODO: confirm spare batteries for night sessions
```

## Injuries / constraints

None recorded yet. Log anything that affects session selection here, and reference it from
`rules/progression.md`'s readiness ladder.
