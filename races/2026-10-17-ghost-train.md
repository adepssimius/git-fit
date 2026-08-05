# Ghost Train Trail Races — 30-Hour Ultra

**Date:** 2026-10-17 to 2026-10-18 (Sat–Sun). **30-hour ultra starts Saturday 9:00 AM**, cutoff
**Sunday 3:00 PM**. **Location:** Brookline, NH, on the Granite Town Rail Trail.
Confirmed against [UltraSignup](https://ultrasignup.com/register.aspx?did=133446) and the
[UltraRunning calendar](https://ultrarunning.com/calendar/event/ghost-train-rail-trail-races).

> **Registration confirmed (2026-08-04):** the athlete holds an entry to the 30-Hour Ultra. The
> event is listed as SOLD OUT with the waitlist capped at 175 (reportedly filled early May 2026),
> which is why this was flagged — resolved, not a live risk. Everything downstream assumes a
> start line, and that assumption now holds.

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
- Prior result on this course: **50k, 2024-10-19.** Course and turnaround are known. See the
  full report at the end of this file — it contains the single most important tactical
  lesson available to this race.

## Goal tiers

Not chasing a scored lap tier — laps here are a logistics unit, not the objective.

| Tier | Distance | Laps | Notes |
|---|---|---|---|
| Floor | 96.6km (60mi) | 4 | Below primary goal — a bad-day fallback, not a target |
| **Primary** | **~100km** | 4 laps + ~half of lap 5 | The A-goal |
| Reach | 120.7km (75mi) | 5 | If 100km comes easily and the body says go |
| **Stretch** | **160.9km (100mi)** | 6 laps + a 10mi 7th | Full commitment, requires the night to go right |

## Pacing and clock

30h cutoff = **11:11/km (18:00/mi) average including every stop** for 100 miles. See
`athlete/zones.yml` for the `ultra_lap_early` / `ultra_lap_mid` / `ultra_lap_late` moving-pace targets these splits
use — those are derived from the athlete's 5k/10k PRs, not from prescribed targets.

**Start 9:00 AM Saturday, cutoff 3:00 PM Sunday.** Splits include realistic crew stops
(8-10 min per lap, 5 on the last).

| Lap | Cum. distance | Moving pace | Lap time | Clock | Elapsed |
|---|---|---|---|---|---|
| 1 | 24.1km | 8:15/km | 3h18 | 12:26pm Sat | 3h26 |
| 2 | 48.3km | 8:30/km | 3h24 | 4:00pm Sat | 6h59 |
| 3 | 72.4km | 8:54/km | 3h34 | 7:42pm Sat 🌒 | 10h42 |
| 4 | 96.6km | 9:24/km | 3h46 | 11:36pm Sat | 14h36 |
| **~100km** | **100km** | — | — | **~12:08am Sun** | **15h08** |
| 5 | 120.7km | 10:00/km | 4h01 | 3:47am Sun | 18h47 |
| 6 | 144.8km | 10:42/km | 4h17 | 8:15am Sun ☀️ | 23h15 |
| 7 (10mi) | 160.9km | 11:12/km | 3h00 | 11:20am Sun | **26h20** |

**How to read this:**

- **100km lands around midnight Saturday, ~15 hours in, with roughly 15 hours of cutoff left.**
  That goal is not in doubt on current fitness — the question is only how it feels.
- **100 miles finishes ~11:20am Sunday with about 3h40 of margin.** Real, but not generous. It
  assumes the late laps hold near 10:00-11:00/km moving, which is where sleep, feet and GI decide
  the outcome. Losing an hour per lap over laps 5-7 — entirely plausible — eats most of that margin.

> ⚠️ **An earlier version of this file claimed a 6+ hour margin on 100 miles.** That was computed
> from pace targets Runna prescribed, which turned out to be faster than this athlete's actual 5k
> PR pace. Rebuilt on real PR data, the margin is roughly 3h40. 100km stays comfortable; 100 miles
> is a genuine stretch that depends on the back half not unravelling.

Splits are a training-block estimate. Refine them with real data from the Big Day (block week 13)
and both lap simulations — that's what `athlete/zones.yml` → `pace_review` exists for.

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

## Race-day pacing: use ZoneSense, not pace or HR

The watch already runs ZoneSense (`athlete/zones.yml`). For a 30-hour effort it is a better
pacing instrument than either pace or heart rate, because it reads current physiology and
therefore self-corrects for heat, accumulated fatigue, dehydration and the overnight hours —
all of which will move HR without reflecting real intensity. The 2026-08-02 run demonstrated
the failure mode precisely: HR reported 77% of the run at threshold or above, while ZoneSense
recorded 5.8% above the anaerobic threshold.

**The instruction is simple enough to hold at hour 20: stay in ZoneSense Zone 1.**

| Laps | Target | Meaning |
|---|---|---|
| 1-3 | **100% Zone 1** | If Zone 2 appears at all this early, you are going too fast. Walk the rise, take the break. |
| 4-5 | Zone 1, brief Zone 2 tolerated | Occasional drift on climbs is fine; sustained Zone 2 is not |
| 6+ | Zone 1 by whatever means | Run/walk ratio exists to keep you here |

Zone 3 should not appear at any point in this race.

Before race day: switch `Targets.ZoneSenseZones` on in the watch so it alarms rather than
requiring you to read a field. (The chest strap is already standard — ZoneSense does not function
on optical wrist HR at all.)

### The metric's job is front-loaded — and that's fine

There is no evidence DFA a1 behaves sensibly at hour 20, and there probably never will be; nobody
is running lab-validated 100-milers. **Assume the reading is meaningless in the back half.**

That costs less than it sounds, because of a useful symmetry. Laps 1–3 are when you feel fantastic
and want to run faster than you should — and they are also when the metric is most reliable and
when discipline compounds hardest. By hour 20 the instrument is both unvalidated and irrelevant,
because whether you keep moving is a decision, not a number.

So ZoneSense is not the back-half pacing tool. Its entire job is making the back half *survivable*,
and it does that before noon on Saturday. From roughly lap 4 onward, the governing instruments are
perceived effort and the crew-stop decision tree below — which is why that tree is written in terms
of clock margin, GI, feet, sleepiness and gait rather than any number off the watch.

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

**Decided during block week 16** (2026-09-21 to 09-27), using lap sim 1 (2026-09-19, block week
15) as the data point — locked in before lap sim 2 (block week 17) rehearses it for real. Deciding
any later leaves no on-course session left to test it against before race day. Suggested structure
given crew access every ~12km:

- **Start/finish bag**: full change of shoes/socks, headlamp + spare batteries, warm layer for
  overnight, full food resupply, phone charger.
- **7.5mi turnaround bag**: lighter — fluid/gel resupply, blister kit, salt tabs.

Physical packing happens race week (see `2026-10-16-pre-race-shakeout.md`); this is the plan those
bags get packed to.

## Night kit

**Decided during block week 16**, same timing as the crew bags above. `athlete/profile.md` already
confirms 4 headlamps available, so this is picking two plus spares/backup light/reflective vest as
required by race rules — not blocked on anything, just sequenced so lap sim 2 can test the actual
choice rather than a placeholder.

## Shoe/sock rotation

**Decided during block week 16**, informed by lap sim 1 (block week 15) — plan a full shoe change
(likely lap 3–4) and sock changes at any crew stop where feet feel off. **Lap sim 2 (block week
17) is where this gets rehearsed, not where it gets decided** — the two lap sims are 2 weeks apart
with no other on-course session between them, so deciding at week 18 (the original plan) would
leave the rotation completely untested before race day.

## Sleep-deprivation plan

**Decided during block week 16** — needs caffeine timing from `rules/fueling.md` § "Caffeine and
the overnight plan" and whether a planned short sleep at a crew stop is part of the 100mi
stretch-goal strategy, designed together rather than in isolation. Unlike the kit above, there's
no on-course session left to rehearse this against directly — the plan itself is the deliverable,
informed by the night sessions already in the block (kit shakedown wk11, past-midnight wk14, the
night long run wk16).

## Notes from the 2024-10-19 Ghost Train 50k

Two full laps plus extra. Slow, but **the limiter was not the athlete** — a friend was suffering
debilitating muscle cramps and the day was run at his pace. Self-assessment: "I could have stayed
jogging the entire time," and "I didn't have that much to complain about."

**What worked in 2024:**
- **Tailwind rather than water** at aid stations, most of the way.
- **A lot of candy, plus salty snacks.** Simple, palatable, and it held up over the distance.
- Jogging remained available throughout — aerobic capacity was never the constraint.

> **Note:** the 2026 fuelling approach is different — high-carb gels on a 20–30min watch timer with
> plain water. See `rules/fueling.md`. The 2024 detail still matters because it proves candy and
> salty snacks are tolerated by this athlete, which is the obvious fallback when gels stop being
> palatable in the back half.

### ⚠️ THE ONE THING THAT ENDED THE DAY — do not repeat it

> After two full laps he **sat down in his tent to change**. On standing up, legs that had been
> perfectly capable of jogging moments earlier were **in pain and stiff**. He crossed 50km and
> stopped.

The distance didn't end that race. **Sitting down did.** This is a well-known ultra failure mode —
stopping lets blood pool, muscles cool and stiffen, and the body shifts out of "moving" mode — but
it is much more persuasive coming from your own race than from a textbook, and it happened at
almost exactly the point on the course where this year's decision to continue must be made.

**Rules that follow directly, and they are not optional:**

1. **Do not sit down.** Not at the turnaround, not at the start/finish, not "just for a minute to
   change." Crew stops happen **standing**.
2. If something genuinely requires sitting (a serious foot issue), **time-box it hard — 3 minutes
   maximum — and stand up and walk immediately afterwards.** Do not stand still. Do not linger to
   talk. Walk out of the aid station while eating.
3. **Change kit standing up**, or lean rather than sit. Rehearse this at both lap simulations, where
   the crew-stop practice already exists — practise it standing, with a watch running.
4. Brief the crew explicitly: their job includes **not letting you sit down**, and getting you
   moving again on a timer. Someone who doesn't know this will kindly offer you a chair.

### What this changes about the 2026 goal

He covered 50km with capacity in hand, at someone else's pace, and stopped for a reason that is
entirely preventable. That materially strengthens the case for the 100km primary goal — it is not
an extrapolation from an unknown, it is the same course with the specific failure removed and a
real training block behind it.
