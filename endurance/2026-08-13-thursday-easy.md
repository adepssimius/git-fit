---
date: 2026-08-13
sport: Run
name: Thursday Easy — social run
type: easy
block_week: 10
distance_km: 8.0
duration_s: 3600
target_mode: pace
brief: >
  60min easy with company at 7:30/km. Her pace, not yours — sit in it and let the day be easy.
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

  DURATION IS THE CONSTRAINT INSTEAD. She asked for ~75min; this is authored at 60 because
  `weekday_session_max_min` is 60 and scripts/verify_plan.py errors on any weekday easy/tempo/
  intervals/recovery session over it. Unlike the long-run cap there is NO `budget_exception`
  escape for the weekday cap. Per the precedent set for 08-10 (see log/2026-08-09.md), the plan
  file stays at the cap and the log records what was actually run — the plan is not the record.
  If the athlete waives the cap for the day, this becomes 75min/10.0km and the guide re-pushes.

  Thursday also carries Lower B and the 90min meeting-time trainer ride, so this is the week's
  biggest non-long-run day. Friday's full rest absorbs it, and Lower B is low-fatigue by design
  — but per this file's earlier note, if calves or achilles are talking, THIS RUN is still the
  thing that gets cut, not the lift.
origin: authored
published:
  suunto: 2026-08-12T15:25:00Z    # guide id kyclzoto (updated in place — was the solo 45min)
---

Easy with company
- 60m 7:30/km Pace
