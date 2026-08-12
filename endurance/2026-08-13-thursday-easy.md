---
date: 2026-08-13
sport: Run
name: Thursday Easy — social run
type: easy
block_week: 10
distance_km: 10.0
duration_s: 4500
target_mode: pace
brief: >
  75min easy with company at 7:30/km. Her pace, not yours — sit in it and let the day be easy.
follow: >
  Pace, a companion sets it. 7:30/km is BELOW your easy ceiling, so this is a genuine easy day.
intent: >
  Rewritten 2026-08-13-eve (authored 2026-08-12): the athlete's wife moved her run from Friday
  to Thursday, so this slot takes it instead of the solo 45min time-on-feet session it held.
  Same purpose — easy aerobic on the Thursday slot — 15min longer and with company.

  PACE IS FINE THIS TIME, which is the difference from the Friday version of this run. She asked
  for 7:30/km. `easy_ceiling` in athlete/zones.yml is 7:00/km and `recovery` is 7:45/km, so
  7:30 sits BELOW the ceiling, between easy and recovery. No overspend, nothing to hold back.
  It is target_mode: pace only because a companion is setting it, not because pace is the
  stimulus — a lower-than-ceiling pace needs no defending.

  DURATION NEEDED A CAP EXCEPTION. She asked for ~75min and `weekday_session_max_min` is 60.
  This was briefly authored at 60 because the weekday cap had no exception mechanism at all —
  unlike the long-run cap, which has taken a flagged `budget_exception` since the block began.
  Athlete waived it the same day, so rather than quietly raising the cap for every week (which
  would weaken it everywhere to serve one run) the escape hatch was added to match the long-run
  one: flagged, ceilinged at 90min, and counted per block. See athlete/profile.md time_budget.

  Thursday also carries Lower B and the 90min meeting-time trainer ride, so this is the week's
  biggest non-long-run day. Friday's full rest absorbs it, and Lower B is low-fatigue by design
  — but per this file's earlier note, if calves or achilles are talking, THIS RUN is still the
  thing that gets cut, not the lift.
budget_exception: >
  Athlete's wife is running this one with him and asked for ~75min. The 60min weekday cap
  exists to protect family time — a run WITH his wife does not spend family time the way a
  solo session does, which is the specific reason this overspend is affordable rather than
  merely tolerated. 15min over cap, at 7:30/km, which is below his easy ceiling.
origin: authored
published:
  suunto: 2026-08-12T15:25:00Z    # guide id kyclzoto (updated in place — was the solo 45min)
---

Easy with company
- 75m 7:30/km Pace
