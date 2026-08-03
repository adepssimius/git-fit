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
  long_run_max_min: 240            # hard cap — buy durability with the Sunday b2b, not a 6h run
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
