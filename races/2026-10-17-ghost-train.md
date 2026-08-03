# Ghost Train Trail Races — 30-Hour Ultra

**Date:** 2026-10-17 (Saturday), start time TBD — confirm and update this file once registration
info is set. **Location:** Brookline, NH, on the Granite Town Rail Trail.

This file replaces Runna's race model entirely. Runna prescribed `50km race at 5:35-5:55/km`
(road-marathon logic) — **discarded**. 50km isn't how this event is structured or scored, and that
pace is far too fast for a 24+ hour effort. Everything below is the real event.

## Course & format

- Out-and-back rail trail, **flat, one hill**, well-maintained, no technical terrain.
- One **lap = 24.1km (15mi) = two 7.5mi (12.1km) out-and-backs** from a central start/finish.
- **Aid station** roughly every 3.75mi (6km) — i.e. at each quarter of a lap.
- **Crew access at the start/finish and at the 7.5mi turnaround** — crew contact every ~12km,
  roughly every 75–90 minutes at ultra pace. Nothing needs to be carried far between stops.
- 30-hour cutoff, laps run continuously (no mandated sleep/rest, but nothing stops you from taking
  it).
- Prior result on this course: **50k finish, ~3 years ago.** Course and turnaround are known.

## Goal tiers

Not chasing a scored lap tier — laps here are a logistics unit, not the objective.

| Tier | Distance | Laps | Notes |
|---|---|---|---|
| Floor | 96.6km (60mi) | 4 | Below primary goal — a bad-day fallback, not a target |
| **Primary** | **~100km** | 4 laps + ~half of lap 5 | The A-goal |
| Reach | 120.7km (75mi) | 5 | If 100km comes easily and the body says go |
| **Stretch** | **160.9km (100mi)** | 6 laps + a 10mi 7th | Full commitment, requires the night to go right |

## Pacing and clock

30h cutoff = **11:11/km (18:00/mi) average including every stop** for 100 miles — generous given
existing fitness (42km training runs at ~5:40/km) and course knowledge. The limiter is not speed;
it's **durability, fueling, and sleep management** overnight. See `athlete/zones.yml` for the
`ultra_lap_early` / `ultra_lap_late` moving-pace targets used in training and race pacing.

| Lap | Distance (cum.) | Target moving pace | Est. clock (start ~7:00am Sat) |
|---|---|---|---|
| 1 | 24.1km | 7:00-7:30/km | ~10:00am |
| 2 | 48.3km | 7:15-7:45/km | ~1:15pm |
| 3 | 72.4km | 7:45-8:15/km | ~4:45pm |
| 4 | 96.6km | 8:15-8:45/km | ~8:30pm |
| **~100km** | **100km** | — | **~9:00pm** (14h in — well inside the 30h window) |
| 5 | 120.7km | 8:45-9:30/km, run/walk | ~1:00am |
| 6 | 144.8km | run/walk, night pace | ~6:30am |
| 7 (10mi) | 160.9km | run/walk, fading | ~10:00-11:00am Sun |

Splits are a training-block placeholder — refine once real long-run and lap-simulation data exists
(`log/` entries feed this). The point of the table is the margin: even the 100mi stretch goal
finishes with hours of cutoff to spare at these paces, so the deciding factor really is durability,
not fitness — train accordingly (`training/block.md`).

## Continue/stop decision tree — evaluate at every crew stop

1. **Clock check** — are you comfortably inside cutoff pace for the next tier? If no margin, stop at
   the current completed lap.
2. **GI status** — able to keep taking in calories/fluid? If GI has shut down and isn't recoverable
   at the aid station, don't start another lap; address it at the crew stop instead.
3. **Feet** — hot spots vs. actual damage. Hot spots → sock/shoe change and continue. Real damage
   (blisters compromising gait, numbness) → medical/crew call before continuing.
4. **Sleepiness (overnight laps)** — if genuinely unsafe to continue (microsleeps, poor
   coordination), take a real rest at the crew stop (see sleep-deprivation plan below) before
   deciding to extend.
5. **Gait/pain** — sharp or worsening pain that changes gait → stop and assess; dull fatigue soreness
   → continue.
6. Default when uncertain: **finish the current lap you're on, decide at the next crew stop.** Never
   decide to extend or stop mid-lap.

## Crew & drop bags

TODO — fill in with the crew roster and per-stop contents once confirmed. Suggested structure given
crew access every ~12km:

- **Start/finish bag**: full change of shoes/socks, headlamp + spare batteries, warm layer for
  overnight, full food resupply, phone charger.
- **7.5mi turnaround bag**: lighter — fluid/gel resupply, blister kit, salt tabs.

## Night kit

TODO — headlamp model, spare batteries (confirm count — see `athlete/profile.md` equipment TODOs),
backup handheld light, reflective vest if required by race rules, warm layer for the coldest overnight
hours.

## Shoe/sock rotation

TODO — plan at least one full shoe change (likely lap 3–4) and sock changes at any crew stop where
feet feel off. Rehearse the swap during lap simulations (`training/block.md` § "Two full lap
simulations").

## Sleep-deprivation plan

TODO — caffeine timing strategy (see `rules/fueling.md`), whether a planned short sleep at a crew
stop is part of the strategy for the 100mi stretch goal, and how that trades against clock margin.

## Notes from the prior 50k on this course

TODO — capture what worked last time (pacing, fueling, footwear, what surprised you about the
surface/turnaround) so it isn't lost. This is useful, hard-to-recreate information — fill it in
early rather than trying to reconstruct it close to race day.
