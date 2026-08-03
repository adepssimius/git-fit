# Ghost Train Trail Races — 30-Hour Ultra

**Date:** 2026-10-17 to 2026-10-18 (Sat–Sun). **30-hour ultra starts Saturday 9:00 AM**, cutoff
**Sunday 3:00 PM**. **Location:** Brookline, NH, on the Granite Town Rail Trail.
Confirmed against [UltraSignup](https://ultrasignup.com/register.aspx?did=133446) and the
[UltraRunning calendar](https://ultrarunning.com/calendar/event/ghost-train-rail-trail-races).

> **⚠️ Registration:** the 30-Hour Ultra is listed as **SOLD OUT**, with the waitlist capped at 175
> and reportedly filled in early May 2026. Confirm you actually hold an entry (or a waitlist
> position) before this block gets much further — everything downstream assumes a start line.

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

**Start 9:00 AM Saturday, cutoff 3:00 PM Sunday.**

| Lap | Distance (cum.) | Target moving pace | Lap time | Clock | Elapsed |
|---|---|---|---|---|---|
| 1 | 24.1km | 7:00-7:30/km | ~2h55 | 11:55am Sat | 2h55 |
| 2 | 48.3km | 7:15-7:45/km | ~3h05 | 3:00pm Sat | 6h00 |
| 3 | 72.4km | 7:45-8:15/km | ~3h15 | 6:15pm Sat 🌒 | 9h15 |
| 4 | 96.6km | 8:15-8:45/km | ~3h30 | 9:45pm Sat | 12h45 |
| **~100km** | **100km** | — | — | **~10:15pm Sat** | **13h15** |
| 5 | 120.7km | 8:45-9:30/km run/walk | ~3h50 | 1:35am Sun | 16h35 |
| 6 | 144.8km | run/walk, night pace | ~4h10 | 5:45am Sun | 20h45 |
| 7 (10mi) | 160.9km | run/walk, fading | ~2h55 | 8:40am Sun ☀️ | **23h40** |

The margin is the headline: **100km lands around 10pm Saturday with 17 hours of cutoff left**, and
even the full 100-mile stretch goal finishes ~8:40am Sunday with **more than 6 hours to spare**.
Nothing about this race is a speed problem. The deciding factors are durability, feet, fueling, and
getting through the night — train accordingly (`training/block.md`).

Splits are a training-block estimate; refine as real long-run and lap-simulation data lands in
`log/`.

## The darkness window — over half the race

Approximate for Brookline NH on this date (**confirm exact times closer to race day**):

- **Sunset Sat ≈ 5:57 PM** — headlamp on partway through **lap 3**
- **Sunrise Sun ≈ 6:58 AM** — daylight returns partway through **lap 7**

That's **~13 hours of darkness out of a ~24-hour effort** — laps 3 through 6 are run entirely or
mostly in the dark, and they're exactly the laps where fatigue, sleepiness, and foot problems
compound. The athlete is an experienced night runner who enjoys it, so darkness alone is not the
concern — but darkness *combined with* 15+ hours of accumulated fatigue and rising sleep pressure
is a different problem, and that combination is what laps 4-6 actually test.

Practical consequences: headlamp plus **at least one spare set of batteries and a backup light** in
the start/finish crew bag, a warm layer available from lap 3 onward (temperatures in the 40s°F
overnight are typical for mid-October NH), and caffeine timing planned around the 1am–6am low
(`rules/fueling.md`).

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
