---
date: 2026-08-15
sport: Run
name: Long Run — threshold embedded
type: long
block_week: 10
duration_s: 14400
target_mode: effort
brief: >
  40min in, 4x(6min at 5:55 + 2min jog), then 168min continuous. Threshold early while fresh; nothing hard after.
follow: >
  ZoneSense Zone 1 for all the running; the 6min threshold reps by pace. If Zone 1 means slower, run slower.
intent: >
  Champion week 7's big threshold long run, trimmed to 4 reps to fit the long-run cap.
  Threshold blocks go early while fresh; easy aerobic carries the back half.
  Extended 2026-08-04 from 177 to 213min, and again 2026-08-14 from 213 to 240min at the
  athlete's request ("I'm fine doing a 4 hour run. I enjoy the solitude"). The added volume is
  all easy aerobic at the back, not more threshold. 240min sits EXACTLY at
  `long_run_max_min` — legal without a budget_exception, but at the ceiling, so it is not a
  precedent for drifting past it. At ~7:05/km this finally reaches the ~34km the seed skeleton
  wanted for this session; 177min was ~25km and 213min ~30km.

  Warmup shortened 40 -> 20min the same day, also athlete-requested. Consistent with this
  session's own stated design ("threshold early while fresh") and it buys 20 more minutes for
  the continuous back half, which is what the block actually wants and what the Mont Blanc 10
  checkpoint needs. One caution attached: the reps double as the threshold probe, and HR is
  the readout. 20min is an adequate warmup for 5:55/km work, but it is the short end — if rep 1
  reads oddly low, treat an under-warmed cardiovascular system as a candidate explanation
  before concluding the pace table is soft.
  The 2min float between threshold reps is a jog — per rules/endurance-authoring.md,
  jog_recovery is what belongs between threshold reps. Float corrected 8:00 -> 7:30/km on
  2026-08-12: 8:00 sits inside the dead band between the athlete's jog floor (7:30) and his
  max walk pace (9:30), so it was a shuffle, not a jog. See athlete/zones.yml locomotion_floors.

  THIS IS ALSO THE BLOCK'S NEXT THRESHOLD PROBE, added 2026-08-12. The 08-12 session came in
  at RPE 3 against an expected 6 with the reps run 6s/km FASTER than prescribed and heart rate
  never reaching LTHR — see log/2026-08-12.md. 2min reps are too short to settle HR, so they
  could not answer whether the 5:40 threshold anchor is stale. SIX-minute reps can.
  Instruction, and it costs nothing: run rep 1 at 5:55 as written and look at HR at the end of
  it. If it is under ~160 (LTHR is 169), take reps 2-4 to 5:40 and log the HR for each. If rep
  1 lands at 165+, 5:55 is honest and the table is fine. Either way this converts a session the
  plan already contains into the data zones.yml pace_review is waiting for, with no extra
  session and no extra time.

  Briefly moved to Sun 08-16 on 2026-08-12 to make room for a Friday social run, then moved
  BACK the same day when that run was rescheduled to Thursday. Saturday is the session's home:
  Friday is the mandated leg-recovery day and nothing now competes for it. Recording the
  round trip rather than silently reverting, so the guide id churn below has a reason attached.

origin: authored
published:
  suunto: 2026-08-12T22:00:00Z    # guide id 9j7cdxce (float 8:00 -> 7:30)
---

Easy aerobic
- 40m ZoneSense Z1

Threshold 4x
- 6m 5:55/km Pace
- 2m 7:10-7:40/km Pace

Easy aerobic
- 168m ZoneSense Z1
