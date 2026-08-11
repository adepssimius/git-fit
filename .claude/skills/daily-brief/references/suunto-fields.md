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
| `Temperature` (SML) | **Kelvin, and USELESS** | see below — never report it as ambient |
| `recoveryTime` | seconds | the watch's own prescription, e.g. `40380` = 11h13m |
| `totalTime` | seconds | |
| `totalDistance` | metres | |

## Never use the temperature field

**The sensor is inside the watch, against the wrist, so it largely reads body heat.** It is not an
ambient thermometer and no amount of conversion makes it one. Two real errors from one week: an
85°F outdoor run was recorded as ~72°F and written up as having "no heat confound", and a 72°F gym
was reported as 79°F. Wrong in both directions, so there isn't even a usable bias to correct for.

If temperature matters to the interpretation — and it often does, because ZoneSense self-corrects
for heat and a hot day genuinely lowers the aerobic threshold — **run
`scripts/heat_load.py --workout-json <the workout>`**. It decodes the workout's own GPS track and
pulls the real ambient temperature, humidity and solar radiation for that place and that hour,
plus the heat load in full sun and in full shade. Never infer temperature from the file, and no
longer ask the athlete for it — the one thing he still has to supply is `shade_pct`, how much of
the session was under canopy. See `rules/conditions.md`.

**`startPosition`, `stopPosition` and `centerPosition` are all `{0, 0}`** on every workout
checked — the position fields are not populated. The `polyline` field is the only real location
data in the payload; it is a standard Google-encoded polyline, and `heat_load.py` decodes it. A
workout with no polyline was indoors, which is also how the script decides whether outdoor
weather applies at all.

## Fragmentation

`wellness_sleep` returns **one item per sleep segment**, not per night. A fragmented night appears
as several items with the same-ish date and short durations — the night of 2026-08-01 came back as
five separate items totalling ~8h.

This matters because `rules/progression.md` scores fragmentation as its own signal and is explicit
that **3+ fragments is red regardless of total hours**. Summing durations and reporting "8h, green"
inverts the actual reading. Count the items before trusting the total.

## Treadmill distance is unreliable, and the laps stay raw after calibration

With no foot pod (`Settings.FootPodUsed: false`) the watch derives treadmill distance from wrist
motion, which over-reads — and **not by a constant factor**. On the 2026-08-05 run it over-read
~10% at 5.3mph but only ~2% at 6.3mph, because arm swing scales differently from speed.

If the athlete calibrates against the treadmill afterwards, the watch stores **both** figures and
they disagree:

| where | 2026-08-05 | which |
|---|---|---|
| `Header.Distance`, `totalDistance`, Move `Distance` | 9060m | calibrated |
| Move `DistanceMax`, Activity `Distance`, **sum of lap distances** | 9733m | raw |

So the summary is corrected but **the per-lap distances are not**, and any per-lap speed computed
from them is wrong. Derating laps by the summary ratio helps but can't fully fix it, since the
error isn't uniform.

**On a treadmill, the trustworthy per-block figure is the belt speed the athlete set × the lap
duration.** He sets speed precisely and the clock is exact, so that beats both stored distances.
Ask what speeds he ran rather than deriving them.

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
