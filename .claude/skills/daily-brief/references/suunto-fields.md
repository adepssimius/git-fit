# Suunto API fields — units and gotchas

Read this before interpreting any number from `mcp__suuntool__*`. The units are not what you'd
guess, and a wrong conversion produces a brief that is confidently, quietly wrong — the worst
possible failure for something whose whole job is to be trusted at 6am.

## The trap: heart rate is in Hz in some places and bpm in others

This is the single most expensive mistake available here.

| Source | Field | Unit | Convert |
|---|---|---|---|
| `wellness_sleep` | `hrAvg`, `hrMin` | **Hz** | `× 60` → bpm |
| `workouts_sml` summary | `HR.Avg`, `HR.Max`, `HR.Min` | **Hz** | `× 60` → bpm |
| `workouts_sml` header | `Personal.MaxHR`, `HrZones.Zone*LowerLimit` | **Hz** | `× 60` → bpm |
| `workouts_list` / `workouts_get` | `hrdata.avg`, `hrdata.max` | **bpm already** | none |

So `hrAvg: 0.7` is a resting heart rate of **42**, not 0.7. And `HrZones.Zone2LowerLimit: 2.284`
is **137 bpm**. If a number looks absurd, check which endpoint it came from before reporting it.

Sanity check against `athlete/zones.yml` → `baseline`: resting HR should land 38–43, sleep-average
HR 41–47. A converted value far outside that is a conversion error, not a physiological event.

## Everything else

| Field | Unit | Notes |
|---|---|---|
| `duration`, `deepSleepDuration` | seconds | `26311` = 7h18m |
| `avgHrv` | ms (RMSSD) | no conversion — compare directly to the ladder's ≥80 / 60–80 / <60 |
| `avgHrvSampleCount` | count | a low count means a short or fragmented night; the HRV figure is less trustworthy |
| `quality` | 0–1 | `0.85` = 85%. The ladder's thresholds are 0.75 / 0.55 |
| `maxSpo2` | 0–1 | `0.98` = 98% |
| `balance` (wellness_recovery) | 0–1 | body resources. Ladder: ≥0.70 green, 0.40–0.70 amber |
| `stressState` | enum | low integers = calm. Not in the ladder; ignore unless something else is odd |
| `Temperature` (SML) | **Kelvin** | `295.7` = 22.5°C. The first few minutes read high — that's the watch warming on-wrist, not air temperature |
| `recoveryTime` | seconds | the watch's own prescription, e.g. `40380` = 11h13m |
| `totalTime` | seconds | |
| `totalDistance` | metres | |

## Fragmentation

`wellness_sleep` returns **one item per sleep segment**, not per night. A fragmented night appears
as several items with the same-ish date and short durations — the night of 2026-08-01 came back as
five separate items totalling ~8h.

This matters because `rules/progression.md` scores fragmentation as its own signal and is explicit
that **3+ fragments is red regardless of total hours**. Summing durations and reporting "8h, green"
inverts the actual reading. Count the items before trusting the total.

## Timestamps

Returned in local time with offset (`2026-08-05T01:04:55.520-04:00`). Unix-millisecond fields
(`startTime`, `stopTime`) need `/1000` and are best rendered in local time — the athlete runs
post-bedtime, so a UTC render silently shifts sessions to the wrong calendar day.

## Reading a workout against what was prescribed

`workouts_sml` with `streams` + `include_summary` returns per-lap windows. Useful fields per lap:
`Duration` (s), `Distance` (m), `Speed.Avg` (m/s → `1000/x` = sec/km), `HR.Avg` (Hz), `Ascent`,
`Descent`, and `IntervalNotes` — which carries the **step title from the pushed guide** (`EZ`,
`STRIDE`, `REC`, `FIND HILL`). That's how you match executed laps to prescribed steps.

`Header.ZoneSenseZones` gives `Zone1Duration` / `Zone2Duration` / `Zone3Duration` in seconds.
These sum to **less than** the activity duration — the difference is the ~10min ZoneSense cold
start, during which there is no reading at all. Report ZoneSense percentages as a share of
**tracked** time and say so, or the numbers won't reconcile.
