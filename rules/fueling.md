# Fueling — daily baseline, gut training, race protocol

High-carb daily baseline, per the athlete's own intent ("stay super high carb... fuel as much as
possible to let recovery happen"). This file is the reference for what to prescribe in `intent:`
fields and what to rehearse on which sessions.

## Daily baseline

- High-carb, supporting both the running volume and the strength program's recovery demands.
- **Bodyweight 162 lb / 73.5 kg** (confirmed 2026-08-04).
- At this training load, **8–10 g carb/kg/day = roughly 590–735 g/day**. That is a lot of food and
  it is deliberate; carbohydrate is not the thing to restrict in this block.
- **Sweat rate is low-average**, so sodium sits at the lower end of typical guidance rather than
  the high end — see the race protocol below.

## The current system (2026) — and how it differs from 2024

**Current, and it's a good system:**
- **High-carb gels on a watch timer, every 20–30 minutes.**
- **Plain water**, deliberately — to wash the gel taste out.

**2024 Ghost Train 50k, for contrast:** Tailwind rather than water most of the way, plus a lot of
candy and salty snacks. That also worked, over 50km.

These are genuinely different strategies and the difference matters over 24 hours:

| | 2026 (gels + water) | 2024 (Tailwind + food) |
|---|---|---|
| Carbs from | gels only | drink **and** food |
| Sodium from | **nothing** — plain water | Tailwind + salty snacks |
| Decision load | **none, it's a timer** | judgement at each aid station |
| Palatability over 24h | **unproven; the main risk** | proven to 50km |

### The timer is the best part — keep it, and formalise it

Eating on a watch timer removes decision-making, and decision-making is precisely what fails at
hour 15 when you're tired and nothing sounds good. Most people's fueling collapses because they
stop *choosing* to eat, not because they can't. **Keep the timer for the entire race**, including
the hours when you feel fine and think you don't need it.

### Two gaps this system opens

1. **Sodium is now zero from drink.** Gels carry little or none, and plain water carries none at
   all. Low-average sweat rate (`athlete/profile.md`) means the requirement is at the lower end of
   typical, but "lower end for 26 hours" is still a real number. **Carry salt tabs and put them on
   the same timer**, or alternate — gel on the beep, salt tab every third beep. TODO: settle the
   dose during the Big Day and both lap sims.
2. **Gel-only will very likely fail somewhere in the back half.** Flavour fatigue over 24 hours is
   near-universal, and the 2024 race already proved that candy and salty snacks work for this
   athlete. **Plan the handover rather than discovering it at 2am**: gels while they're palatable,
   then real food, with the timer unchanged — only what's on the beep changes.

### Open question — needed to compute the actual rate

**TODO: which gel, and what carb load per gel?** At 40g every 25min that's ~96 g/hr, right in the
target band. At 30g every 30min it's ~60 g/hr, which is under-fuelled for this race. The interval
is known; the gram figure isn't, and the whole plan turns on it.

## Gut training progression — the actual training variable

Target **90–120g carbs/hour** sustained, which is what ultra performance at this distance requires
and what most runners' guts aren't trained for by default. Progress it deliberately rather than
assuming it'll work on race day:

- Early long runs (block weeks 9–11): practice at 60–75g/hr, gels/chews are fine.
- Mid-block (weeks 12–15): push toward 90g/hr on long runs and lap simulations; start introducing
  **real food**, not only gels — a 24+ hour effort cannot run on gels alone (gut fatigue, sugar
  fatigue, and simple palatability all break down well before then).
- Peak block (weeks 15–17): 90–120g/hr on the two lap simulations specifically, with the exact
  foods planned for race day, including whatever crew will be handing over at each stop.
- **Meeting-time trainer rides are a free, low-stakes place to practice this** — no impact,
  seated, easy to sip/chew consistently. Use them for repetition, not just the long runs.

## Sodium and fluids

TODO — set specific sodium (mg/hr) and fluid (mL/hr) targets once sweat rate / prior race data is
available. Rehearse whatever is set on every long run over ~90min, same as carbs — don't leave this
to be solved in real time on race day.

## Caffeine and the overnight plan

TODO — this matters specifically for the 100-mile stretch goal, which runs through a full night.
Plan caffeine timing (when to start, how to dose across ~24+ hours without a crash or tolerance
wall) and cross-reference `races/2026-10-17-ghost-train.md` § "Sleep-deprivation plan" — the two
need to be designed together, not separately.

## What to rehearse on each long-run type

- **Standard long runs** (block weeks 9–12): carb progression per the schedule above; this is where
  the habit gets built.
- **The Big Day** (block week 13): full race-day fueling protocol end to end, at real fatigue —
  the closest dress rehearsal before the actual lap simulations.
- **Lap simulations** (structured as 4×6km segments, crew stops at 12km/24km): the fueling handoff
  itself is the point — rehearse what crew hands over, how fast the exchange happens, and whether
  the planned foods still sound good at hour 2+ of continuous effort.
- **Night sessions**: rehearse fueling *and* caffeine timing together, since race night is where
  both matter most simultaneously.

## Race-day per-lap protocol

TODO once the above is dialed in through training — this section should end up as a lap-by-lap table
(what's consumed between which aid stations, what's handed over at each crew stop) that mirrors the
pacing table in `races/2026-10-17-ghost-train.md`. Build it from what actually worked in the lap
simulations, not from a generic template.
