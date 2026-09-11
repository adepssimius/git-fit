# Ghost Train Trail Races — 30-Hour Ultra

**Date:** 2026-10-17 to 2026-10-18 (Sat–Sun). **30-hour ultra starts Saturday 9:00 AM**, cutoff
**Sunday 3:00 PM**. **Location:** Brookline, NH, on the Granite Town Rail Trail.
Confirmed against [UltraSignup](https://ultrasignup.com/register.aspx?did=133446) and the
[UltraRunning calendar](https://ultrarunning.com/calendar/event/ghost-train-rail-trail-races).
Entry confirmed 2026-08-04.

> **REWRITTEN 2026-09-08.** The previous version of this file was built on two assumptions that
> are now known to be false: that he would be **crewed**, and that the lap paces below prescribed
> something he **could not run**. Both are resolved below. Everything the old file deferred to
> "block week 16" — crew bags, night kit, shoe rotation, the sleep plan — is decided here instead,
> because the athlete has now made the decisions and the evidence to make them arrived on
> 2026-09-06 and 09-07.
>
> Runna's race model (`50km race at 5:35-5:55/km`, road-marathon logic) remains **discarded**.

---

## The two corrections that drove this rewrite

### 1. He is running this UNCREWED (athlete decision, 2026-09-07)

*"Assume uncrewed. I might have a pacer for one lap."*

Everywhere the old file said "crew stop" or "crew bag", read **self-serve drop bag**. **The
logistics survive this almost untouched**, because the course is close to the best case for
running solo:

| station | position | stock | drop bag |
|---|---|---|---|
| **Start/finish** | 0 / 15mi | full — *"all kinds of good food"*, candy, soda, Tailwind | **yes** |
| mid-out | 3.75mi | snacks, drinks, candy/soda/Tailwind | no |
| **7.5mi turnaround** | 7.5mi | full — *"all kinds of good food"*, candy, soda, Tailwind | **yes** |
| mid-back | 11.25mi | snacks, drinks, candy/soda/Tailwind | no |

So: **aid every ~6km, a drop bag every ~12.1km**. Warm savoury food needs no crew capability —
the end stations serve it. Battery restock happens at every bag pass. The carry drops to one
inter-station gap plus reserve.

**What uncrewed actually costs is judgement, not logistics** — a second brain at the hour the
first one stops working. The old continue/stop tree was written to be *"evaluated at every crew
stop"* and included a check for slurring and poor coordination. **Those are exactly the symptoms
the sufferer cannot self-assess.** That is why the tree has been replaced by a **carried card**
(below): something fixed, printed and read, rather than a paragraph to be judged at the hour
judgement has degraded.

### 2. ~~THE LAP PACES PRESCRIBE SOMETHING HE CANNOT RUN~~ — RESOLVED 2026-09-08

The old file carried a long warning: `ultra_lap_early` is **8:15-8:30/km**, his `jog_floor_min` is
**7:30** and his `walk_max` is **9:30**, so the target sits in a dead band — too slow to jog, too
fast to walk. It concluded the opening was a binary: *~7:30 continuous, or walk breaks from the
gun*, and demanded the paces be re-derived.

**They do not need re-deriving. He has now run them, twice, on this course, and the mechanism is
the second option — deliberately chosen, not a capitulation.**

| | 2026-09-06 | 2026-09-07 |
|---|---|---|
| distance | 30.08km | 22.61km |
| pace | **8:37/km** | **8:08/km** |
| instrument | ZS Z1 only | ZS Z1 only |
| RPE | 4 | 3 |
| surface | race course, night | race course, day |

Athlete on what produced those numbers: *"I was trying to stay at my actual race day pace
basically. **walking the uphills and walking the steep downhills** since the downhills are what
cause the real damage in my experience."*

**The dead band was real and the conclusion drawn from it was wrong.** It treated 8:15-8:30 as a
pace to be *held*, and no single gait holds it. It is an **average**, and he already produces it
by run/walking to terrain at ZS Z1 without thinking about the number at all. The old file called
that *"a fundamentally different race"* — it is simply the race, and it is the one he has been
training.

Two things follow that matter more than the arithmetic:

- **Walking the steep downhills is a durability decision, not a pace concession.** His reasoning —
  descents do the damage — is the correct one over 30 hours, and it is worth protecting when the
  early laps feel easy and running them is tempting.
- **Do not chase these numbers on the day.** Follow ZS Z1 and walk to terrain; the pace is the
  *output*. 8:37/km on 09-06 also contained a porcupine.

---

## Course & format

- Out-and-back rail trail, **flat, one hill**, well-maintained.
- **SURFACE.** Not smooth crushed stone. **Mostly grassy with singletrack or packed dirt**, the
  short hill section **semi-technical**. Consequences: night footing on grass and singletrack at
  hour 15+; pace is slower than "rail trail" implies for the same effort; **fall risk late**.
- **Heavy tree canopy over essentially the whole course** (athlete-confirmed 2026-09-07). It
  neutralises daytime heat — measured `shade_pct: 98`, WBGT 65.7F against 70.1F fully exposed —
  and it makes the night **genuinely dark**, admitting no sky glow or moonlight. That sets the
  lighting requirement higher than generic night running, not lower.
- One **lap = 24.1km (15mi) = two 7.5mi (12.1km) out-and-backs** from a central start/finish.
- 30-hour cutoff, laps run continuously. No mandated rest; nothing stops you taking it.
- **Prior result on this course: 50k, 2024-10-19.** See the end of this file — it contains the
  single most important tactical lesson available, and being uncrewed makes it *more* important,
  not less.
- **He trains on the northern 6.5mi of this course.** The real turnaround, the real surface. Only
  the first mile is closed outside race day, and he has run that too, in 2024.

---

## Goal tiers — an honest reading as of 2026-09-08

| Tier | Distance | Laps | Assessment |
|---|---|---|---|
| Floor | 96.6km (60mi) | 4 | Bad-day fallback |
| **Primary** | **~100km** | 4 + ~half of 5 | **Probable.** The A-goal, and it is the right one |
| Reach | 120.7km (75mi) | 5 | Live if the night goes well |
| Stretch | 160.9km (100mi) | 6 + a 10mi 7th | **Unlikely on current preparation.** Kept as a stretch, not planned for |

**Why 100 miles is written down as unlikely rather than as a target.** Not fitness — preparation
depth. As of 2026-09-08, **the longest continuous effort of this block is 4h19** (2026-09-06),
against 26h49 in the 100-mile table below. Three weeks of near-zero running through illness and
travel (08-16 → 09-04) cost the block roughly a month of its aerobic base, and the running
actually accumulated in the 24 days to 09-08 is ~96km. Every failure found so far — the lights at
4h26, hunger, the ITB murmur — arrived at or before ~4h30, which is only evidence that the map
ends there.

**This is a statement about what has been rehearsed, not a ceiling.** He covered 50km on this
course in 2024 with capacity in hand. The remaining long sessions (09-12, 09-26, 10-03) are what
move the honest reading, and this table should be re-read after each of them.

**Race it to 100km and let the night decide the rest.** The tiers above are not a plan to abandon
at 100km — they are a plan that does not require the back half to work in order to succeed.

---

## Pacing and clock — rebuilt 2026-09-08 on the run/walk model

30h cutoff = **11:11/km (18:00/mi) average including every stop** for 100 miles.

Built from what he actually produced on this course on 09-06 and 09-07 at ZS Z1, faded by lap.
**Stops are self-serve and standing** — 8-10 minutes per lap total across two drop-bag passes and
two aid passes, 5 on the last.

| Lap | Cum. | Moving pace | Lap moving | Stop | Clock | Elapsed |
|---|---|---|---|---|---|---|
| 1 | 24.1km | 8:20/km | 3h20 | 8m | 12:28pm Sat | 3h28 |
| 2 | 48.2km | 8:35/km | 3h26 | 8m | 4:03pm Sat | 7h03 |
| 3 | 72.3km | 9:00/km | 3h36 | 9m | 7:49pm Sat 🌒 | 10h49 |
| 4 | 96.4km | 9:30/km | 3h48 | 9m | 11:47pm Sat | 14h47 |
| **~100km** | **100km** | — | — | — | **~12:24am Sun** | **15h24** |
| 5 | 120.5km | 10:15/km | 4h07 | 10m | 4:04am Sun | 19h04 |
| 6 | 144.6km | 11:00/km | 4h25 | 10m | 8:39am Sun ☀️ | 23h39 |
| 7 (10mi) | 160.7km | 11:30/km | 3h05 | 5m | 11:49am Sun | **26h49** |

**How to read this:**

- **100km lands around 00:30 Sunday, ~15h24 in, with ~14h30 of cutoff left.** That is the goal and
  it is not in doubt on fitness. The question is only how it feels.
- **100 miles finishes ~11:49am with ~3h11 of margin.** Real, but thin, and it assumes the late
  laps hold near 10:15-11:30/km. Losing an hour per lap over laps 5-7 — entirely plausible on
  4h19 of longest-ever continuous experience — eats all of it.
- **These are lap paces at ZS Z1, not instructions.** See the correction above.

Refine after 09-12, 09-26 and 10-03 (`athlete/zones.yml` → `pace_review`).

---

## The darkness window — computed, not estimated

For 42.80N, 71.66W on this date:

| | |
|---|---|
| Sunset Sat 10-17 | **18:01** |
| Full dark from | **18:30** |
| First light Sun 10-18 | **06:35** |
| Sunrise | 07:03 |
| **Continuous darkness** | **12h05** |

He is on course for essentially all of it. **Lights go on mid-lap 3**, on legs with ~60km in them
— not at a start line, fresh. **100km lands dead centre of the night.** Daylight returns during
lap 6.

Under this canopy there is no ambient light to fall back on.

---

## Race-day pacing: use ZoneSense, not pace or HR

For a 30-hour effort ZoneSense is a better instrument than pace or HR, because it reads current
physiology and self-corrects for heat, fatigue, dehydration and the overnight hours — all of which
move HR without reflecting real intensity. The 2026-08-02 run showed the failure mode: HR reported
77% of the run at threshold or above; ZoneSense recorded 5.8% above the anaerobic threshold.

**The instruction is simple enough to hold at hour 20: stay in ZoneSense Zone 1.**

| Laps | Target | Meaning |
|---|---|---|
| 1-3 | **100% Zone 1** | If Zone 2 appears this early you are going too fast. Walk the rise, take the break |
| 4-5 | Zone 1, brief Zone 2 tolerated | Drift on climbs is fine; sustained Zone 2 is not |
| 6+ | Zone 1 by whatever means | Run/walk exists to keep you here |

Zone 3 should not appear at any point in this race.

Before race day: switch `Targets.ZoneSenseZones` on so it alarms rather than requiring a field to
be read. **The chest strap is mandatory — ZoneSense does not function on optical wrist HR at all.**

### The metric's job is front-loaded, and that is fine

There is no evidence DFA a1 behaves sensibly at hour 20 and there probably never will be. **Assume
the reading is meaningless in the back half.**

That costs less than it sounds, because of a symmetry: laps 1-3 are when you feel fantastic and
want to run faster than you should, and they are also when the metric is most reliable and
discipline compounds hardest. By hour 20 the instrument is unvalidated and irrelevant, because
whether you keep moving is a decision, not a number.

**ZoneSense's entire job is making the back half survivable, and it does that before noon on
Saturday.** From lap 4 onward the governing instrument is the card below.

---

## THE CARD — carry it, do not improvise it

**Print two. One in each drop bag.** Replaces the old "evaluate at every crew stop" decision tree,
which assumed a crew and assumed working judgement. Read it out loud at every drop-bag pass from
lap 3 onward — out loud, because hearing yourself slur is the check you cannot run in your head.

> ### AT EVERY DROP BAG — say each answer out loud
>
> **1. WHAT TIME IS IT AND WHERE AM I?** Say the lap number and the clock time.
> *If that is hard to assemble, you are further gone than you feel. Eat, take caffeine, and treat
> the next answers with suspicion.*
>
> **2. CLOCK.** Am I inside cutoff pace for the next tier? *No margin → this lap is the last one.*
>
> **3. FUEL.** Have I eaten in the last 30 minutes and did it stay down?
> *No → eat something SOLID here, standing, and walk out eating. Do not start a lap behind.*
>
> **4. FEET — take the shoe off and look. Do not skip this because it is cold.**
> *Hot spot → tape it NOW (2 min here is a blister 15km later). Blister → the four branches in
> `athlete/profile.md` § Blister kit. Numbness or a blister changing your gait → stop the lap.*
>
> **5. LEFT ITB.** Whisper, or is it changing how I run?
> *Changing my gait → this lap is the last one. Not negotiable.*
>
> **6. AM I SLEEPY OR AM I STUPID?** Tripping, missing turns, losing minutes I cannot account for?
> *→ Caffeine, 20 minutes of walking, real food. **That is the plan — you are not sleeping this
> race.**
> **IF THE THOUGHT "I MIGHT NEED TO LIE DOWN" HAS OCCURRED AT ALL — SEND THE TEXT NOW.** They need
> 45 minutes and you cannot buy that back later. Sending it and not using it costs nothing.
> If it still has not cleared by the next bag: 15-20 minutes at the start/finish, alarm set,
> caffeine taken BEFORE you lie down. Never trailside.*
>
> **7. WARM ENOUGH?** *Shivering, or cold hands that will not work the tape? Put the layer on
> BEFORE you need it — it is much harder to warm up than to stay warm.*
>
> **8. LIGHTS.** Do I have two working, and two spare cells? *→ Restock to two spares at EVERY
> bag, whether or not anything died.*
>
> ### THE TWO STANDING RULES
> **STIFF ON STANDING UP IS A PHASE, NOT A VERDICT.** It has resolved in ~20 minutes every time.
> Do not decide anything — do not quit, do not force a walk — while it is happening. **Sitting is
> allowed; deciding within 20 minutes of standing up is not.**
> **DECIDE AT THE BAG, NEVER MID-LAP.** Finish the lap you are on. Every quit that has ever been
> regretted was decided between aid stations.

**Why the card and not the old tree.** The old tree had six numbered criteria and a default. It
was correct and it was unusable, because it required the athlete to remember it existed, remember
its contents, and apply judgement to each — at 03:00, alone, at hour 18. The card is read, not
recalled; it forces the shoe off rather than asking how the feet feel; and item 1 exists solely to
detect the state in which the other seven answers cannot be trusted.

---

## Drop bags and carry — DECIDED 2026-09-08

Both bags are near-identical, deliberately: **a problem gets fixed wherever it surfaces, rather
than carried 12km to the bag that has the fix.**

### On the body

| | |
|---|---|
| **Carry** | Naked Running Band |
| **Fluid** | 700ml Sportiva soft flask ×2 — one Tailwind, **one carried empty** for water or broth |
| **Eating** | **2 collapsible cups** (the race provides none), spork, gels for one inter-station gap plus reserve |
| **Lights, after dusk** | Zebralight H600Fc Mk IV on the chest · Convoy S3 in the band's side stretch pocket · Foursevens emergency |
| **Power** | **2 spare 18650 cells**, restocked to two at every bag pass |
| **Instruments** | Watch + **chest strap** |
| **Personal** | Phone, headphones. **Signal throughout the course** — the phone is the nap-notice line and the only way to call for help after a fall, alone, at 04:00. That makes its battery load-bearing, which is what the power bank is for |
| **Warm layer** | **UNRESOLVED — see open items** |

The second flask earns its ~35g three ways: fluid separation (Tailwind and water both available),
backup for a split flask or failed bite valve, and — the one that matters — **broth**. A cup means
drinking it standing; a flask means taking it with you. That is the difference between a 30-second
stop and a five-minute one, repeated across the night.

### Both bags — start/finish (0/15mi) and 7.5mi turnaround

- **Altra Lone Peak 9 (9.5)**, one pair in each. He owns three; one stays home
- **Balega Hidden Comfort**, several pairs
- **Blister kit** — 1 roll Leukotape P, alcohol wipes, Skin-Tac, 2 non-adherent pads, 4-5 × 25G
  sterile beveled needles, small scissors, nitrile gloves, ziplock. Full protocol in
  `athlete/profile.md` § Blister kit
- **Aquaphor** · **2 pairs nipple shields** · **1 spare collapsible cup** · **1 Nitecore NU25**
- **Beanie** (athlete, 2026-09-08 — staged as backup, not expected to be needed) · **spare fleece
  gloves**
- **18650 cells** — the restock pile
- **Gels**
- **Analgesic** — see open items
- **The card**

### Start/finish bag only

- **Yanii PD2 power bank** + 0.5m right-angle USB-C cables. **This IS the phone charger** — one
  object, not two (athlete, 2026-09-08). Picked up when something needs it rather than at a fixed
  time: the right-angle cables exist so a device charges **in the waistband while moving**, so the
  bank rides with him for the duration of a charge and goes back in the bag afterwards. Cells are
  ~48g each, which is why it does not start on his body at 09:00
- **Night clothing**: 120 GSM Alpha Direct hoodie, Rab approach jacket (windbreaker), fleece
  gloves, Burton headband — available from lap 3 onward. See § The full night system

Physical packing happens race week — `endurance/2026-10-16-pre-race-shakeout.md`.

### The warm layer — 120 GSM Alpha Direct hoodie (athlete, 2026-09-08)

**This is the right class of garment for this specific problem**, and worth saying why so it does
not get "upgraded" to a puffy later. Alpha Direct is **air-permeable active insulation**: it is
built to be worn *while moving* without cooking you. That matters here because the cold hours are
also the slow hours — laps 5 and 6 at 10:15-11:00/km, generating some heat but not much, for four
hours at a stretch. A conventional puffy in that situation gets put on, gets sweaty, gets taken
off, and the cycle costs stops. **This one can just stay on**, which is what makes the card's
*"put the layer on BEFORE you need it"* instruction actually followable.

At 120 GSM it is the warm end of the Alpha Direct range and still ~150g. The **hood is not a
detail** — the head is a large uninsulated heat-loss route and a hood is free to deploy and stow
with cold hands, no separate object to find in a bag at 03:00.

**The wind weakness is real and it is already covered** (athlete, 2026-09-08): a **Rab approach
jacket**, very lightweight windbreaker, goes over the top. Air-permeable is Alpha Direct's whole
design, so in wind it loses most of its warmth on its own. Two things the shell fixes for free:
the **open sections and the start/finish area**, which the canopy does not shelter, and **brush
contact** — the fibre pile is delicate and catches, on a trail where he is deliberately scanning
the sides for porcupines.

### The full night system, and the shell is the thermostat

| layer | item | when |
|---|---|---|
| next to skin | singlet | all race |
| insulation | **120 GSM Alpha Direct hoodie** | from dusk; **stays on** |
| shell | **Rab approach jacket** (lightweight windbreaker) | **on and off as needed** |
| hands | **fleece gloves** | from dusk |
| ears | **Burton headband** | from dusk |
| head, backup | **beanie, one in each drop bag** | only if needed |

**The operational point: the shell is the adjustment, not the insulation.** Alpha Direct works by
letting air through, so putting a windbreaker over it roughly doubles what it does. That gives a
two-stage system with one action — **shell on when cold, standing, or in the open; shell off on
climbs and when working.** Leave it on while working hard and it will trap the moisture the Alpha
Direct is designed to dump. This is why the layer underneath can simply stay on all night and
never needs a stop-and-strip cycle.

**Head coverage is well graduated and his instinct about the beanie is right.** Four levels with
no extra objects to carry: bare → headband → headband + Alpha Direct hood → beanie. The hood and
headband together are almost certainly the working answer, and the beanie earns its place in the
bags precisely because it is *not* expected to be needed — it costs nothing sitting there.

**One gap worth closing the same way he closed the beanie: a spare pair of gloves in each bag.**
Fleece wets out from rain, heavy dew, flask handling and aid-station cups, and **wet fleece gloves
are worse than no gloves** — they hold cold water against the skin for hours. It is the same
argument as spare socks, and the consequences are larger than the beanie's: **cold, wet hands are
what make the blister kit unusable**, and that kit already assumes fine motor work with a needle
and tape at 03:00.

---

## Night lighting and power — DECIDED 2026-09-08

Rebuilt after 2026-09-06, where **two of three light sources died inside 4h26 of darkness** —
against **12h05 required**. Full inventory in `athlete/profile.md` § Night lighting.

| light | role | cell |
|---|---|---|
| **Zebralight H600Fc Mk IV**, 4000K high CRI, frosted | chest, running light | 18650 |
| **Convoy S3 719A**, 4000K high CRI | handheld, wildlife spotting | 18650 |
| **Foursevens**, small high-output | emergency, carried | other |
| **Nitecore NU25** ×2 | backup, one per bag | built-in |

**Standardising on 18650 is the decision that fixes 09-06.** One cell type, either light, no
sorting in the dark with cold hands. The same NCR18650GA cells feed both lights and, through the
Yanii bank, everything USB.

**High CRI over raw brightness is an athlete call and it is correct here** — *"the porcupines hide
in the brush to the side of the trail so I have to pick them out by color."* Under this canopy,
with a documented recurring hazard, colour rendering is the property that does the job.

**The policy is RUN TO EMPTY, RESTOCK AT EVERY BAG — not scheduled swaps.** Athlete, 2026-09-07:
*"If I run out with one then the other light will still be functional and I'll slow to a walk while
I change the battery."* He is right: a dead light is not a crisis when a working one is on his
chest, walking to swap costs nothing he is not already paying at a hill, and scheduled swapping
throws away 40% of a part-used cell — needing 6-7 cells across the night instead of 4.

**The failure mode that actually hurts is different: "a light died and both spares are already
spent, 8km from the bag."** So:

1. **Top back up to two spare cells at every bag pass**, dead or not. Free, and it keeps the
   on-body buffer intact.
2. **Never be down to the last working light.** Two of three dead and the spares gone → walk it in
   to the bag. His rule, and it is the right invariant.
3. **One scheduled swap, and only one: start the dark section on fresh cells at dusk.** Beginning
   12 hours of night on a part-used cell is the one genuinely avoidable failure, and at dusk he is
   rested, at the start/finish, in daylight.
4. **Cold costs capacity.** 40s°F overnight takes something off every cell. Spares in a pocket
   against the body do better than spares in an outside pouch.

**Nothing here is blocked on the 09-12 session.** Runtime is measured indoors; beam pattern and
glove operation on the trail behind his house in a night 5k. The Zebralight not arriving in time
degrades the plan but does not invalidate it — the four legacy headlamps plus the NU25s remain.

**Watch power:** athlete-confirmed sufficient over 30 hours *"if I remember to charge it
beforehand."* The risk is remembering, not runtime — **charge to full Friday night and do not run
with it on Friday.** Packing-list item.

---

## Fueling — the numbers are established; the form is the finding

Full detail in `rules/fueling.md`, `log/2026-09-06.md` and `log/2026-09-07.md`.

| | |
|---|---|
| **~90 g/hr over 4h19** | 2026-09-06, gels every 30min at ~45g, no GI distress |
| **~118 g/hr over 3h16** | 2026-09-07, the highest recorded in the block, no distress |

**The rate question is closed.** Two things replace it:

1. **Hunger tracks accumulated deficit, not elapsed time.** He was hungry from the *start* on
   09-07 because 09-06 was never repaid. Over 30 hours the deficit only ever grows, so expect
   hunger **early and continuously** — eat from lap 1, not from a trigger.
2. **Solid food is what relieves it, and it is FORM not FLAVOUR.** Sunday he craved savoury;
   Monday sweet solid food fixed it, and he said so. This loosens a real constraint: he does not
   have to solve for savoury, he has to **eat something solid**. Both end stations serve it, every
   ~12.1km.

Savoury remains a preference worth respecting and likely to strengthen overnight — **broth is the
03:00 answer**, and the second flask exists to carry it. Prefer lower-fat expressions of "salty +
carbs" (salted potatoes, pretzels, rice, noodles) over the grilled cheese while the gut is holding
90 g/hr; fat slows gastric emptying.

**2024 proved candy and salty snacks are tolerated by this athlete over distance.** That is the
fallback when gels stop being palatable in the back half, and it is stocked at every station.

---

## Shoe and sock rotation — DECIDED 2026-09-08

| | |
|---|---|
| **Start in** | **Altra Mont Blanc Carbon, size 10** |
| **Change to** | **Altra Lone Peak 9, 9.5** — planned around lap 3-4, at whichever bag it falls to |
| **Socks** | Balega Hidden Comfort, changed at any bag where feet feel off or wet |
| **Lube** | Aquaphor between the toes |

**This combination carried 52.7km across 09-06 and 09-07 with zero hot spots.** That is the
strongest footwear evidence in the block and it is why the Mont Blanc starts.

**The size-10 question is closed** and the earlier confusion is worth stating plainly: the shoe
that failed a 30k with blisters and toe-joint soreness was the **9.5**. The 10 has now passed 30km
and 22.6km back-to-back clean. The 9.5 stays retired for distance.

**Toenail pain above ~20km is a standing baseline for this athlete, NOT a fit signal.** *"My big
toe always feels sore in the toenail no matter what... the only variable is distance."* Every
comparison run in the block is over 20km, so it cannot discriminate between shoes and must not be
read as one doing worse. Expect it; do not act on it.

**Callus reduction is the prevention and it is already ongoing** (athlete-confirmed 2026-09-08).
Aggressive work stops **~10-03**; light maintenance can continue after.

**Pre-taping the known sites before the start is the better move if it survives testing** — clean
dry skin at home beats degreasing an Aquaphor-lubed toe in a parking lot at 03:00. **It is in
tension with this shoe's failure mode**, which was compression, so **09-12 is the test slot**. If
it fails there, the mid-race kit stays a surprises-only kit.

---

## Sleep deprivation, caffeine, and the one pacer — DECIDED 2026-09-08

### THE PLAN IS NO SLEEP (athlete, 2026-09-08), and that is the normal choice here

**One night, run straight through.** This is what most of the field will do and it is the standard
approach for a 30-hour single-night event — sleep breaks belong to multi-day formats (200-milers,
backyard ultras, 48h+) where the deficit compounds across two or three nights. Caffeine and food
carry a single night.

**On the A-goal this barely arises.** 100km lands around **00:24**, roughly 15h24 in. Stop there
and there is no deep night to survive at all. **Sleep pressure is a 120km / 100-mile problem** —
it only becomes load-bearing on laps 5 and 6, which run through 04:00-08:00. Read this section as
tier-dependent, not as something on the critical path for the race he is most likely to run.

### Caffeine — MAINTENANCE FIRST, strategic second (athlete plan, 2026-09-08)

**He is caffeine-dependent, and that changes the shape of this entirely.** His plan, in his words:
a dose **shortly before the start** to keep headaches at bay, **a little as needed through the
night**, and **another around 08:00 Sunday**, again for the headache.

**~~Hold it back until it is needed. Do not start at 09:00.~~ — WRONG for this athlete, corrected
2026-09-08.** That is advice for a caffeine-naive runner, where the whole supply is strategic and
spending it early wastes it. For a habituated one it prescribes a **withdrawal headache**, which
sets in roughly 12-24 hours after the last dose and would land somewhere in the night — the exact
hours this plan is trying to protect. A headache at 03:00, uncrewed, on top of sleep pressure, is
not a small cost.

**The correct frame is two separate budgets that happen to use the same substance:**

| | when | why |
|---|---|---|
| **Maintenance** | pre-start, and ~08:00 Sun | **Not optional.** Prevents withdrawal. Baseline function, not performance |
| **Strategic** | 01:00-06:00, as needed | The actual boost, on laps 5-6 — the coldest hours, the deepest fatigue, and the laps that decide whether 100 miles is live |

**What survives from the original advice, narrowed:** it is the *strategic* dosing that benefits
from being spaced and modest rather than one large hit. Nothing about the maintenance doses should
be rationed. **The afternoon needs no cover** — from a pre-start dose, withdrawal would not be due
until well after dark, and the night dosing meets it there.

**The aid stations already stock the delivery mechanism.** All four serve soda, and cola through
the night gives caffeine, carbohydrate and fluid in one, warm-tolerant and palatable when gels
have stopped being. It costs nothing to carry and needs no planning beyond knowing it is there.
Caffeinated gels in the drop bags are the backup if soda stops going down.

**Track it loosely but track it.** "A little as needed" is hard to hold at 03:00 in the state
where the tracking matters most. A rough running count — or simply the rule *one at each drop bag
through the night, no more* — is enough to avoid arriving at 05:00 having taken far more or far
less than intended.

**~~The 08:00 Sunday dose is a driving-safety item.~~ — WRONG, corrected 2026-09-08.** He is
**not driving home**: the plan is a few hours lying down after the finish, then a ride. The dose
is purely headache prevention, and it should follow the post-race nap rather than a clock time —
on the middle tiers 08:00 lands in the middle of that sleep, and there is no reason to wake for
it. **Take it on waking, whenever that is.**

- `rules/fueling.md` § Caffeine is still a TODO and should be written against this section.

### The lie-down is a CONTINGENCY, not part of the plan

It exists for exactly one situation: **card item 6 — sleepy or stupid — does not clear** after
caffeine, real food and twenty minutes of walking. At that point continuing on grass and
singletrack in the dark is a fall risk, and stopping the clock briefly is the cheaper option.

If it is used:

- **15-20 minutes asleep. Not more.** Slow-wave sleep starts somewhere around 20-30 minutes in,
  and waking out of it produces grogginess that can outlast the nap. **A 35-minute nap is worse
  than a 20-minute one.**
- **Take the caffeine immediately BEFORE lying down**, not after. Onset is ~20-30 minutes, so it
  arrives as the alarm does.
- **Budget ~35-40 minutes off the clock, not 20.** The nap itself is the small half; standing up
  will hurt and the following ~20 minutes will be slow and stiff. That is the known, resolving
  phase described below, and **no continue/stop decision gets made inside it**.
- **~~Nobody is going to wake him.~~ — resolved 2026-09-08, with a condition attached.** He has
  a couple of people who can come and wake him, but **they need to be present before he lies down,
  and that takes ~45 minutes of notice.** Still do it **at the start/finish**, where there are
  people and noise — that is also the only place they can reach him.

**THE LEAD TIME IS THE REAL CONSTRAINT, AND IT INVERTS THE DECISION.** A nap cannot be decided on
at the moment it is needed; it has to be decided **~45 minutes before**, in a state that is by
definition worse at deciding things. So the two thresholds must be separated:

| | threshold | cost of being wrong |
|---|---|---|
| **Send the notice** | *"item 6 is going the wrong way"* — deliberately LOW | A phone call and someone's inconvenience |
| **Actually lie down** | item 6 has not cleared after caffeine, food and walking | — |

**Send it early and treat it as free.** A notice sent and not used costs an apology. A notice not
sent costs the option entirely, and the moment it is genuinely needed is exactly the moment he
will be least able to plan 45 minutes ahead. **The phone is on him for the whole race and there is
cell signal throughout the course** (athlete-confirmed 2026-09-08), so the notice goes out from
wherever he is, the moment the thought occurs — no waiting for a bag, no dead zones to plan
around.

**Timing works out with room to spare if the notice goes out at a bag.** At lap 5-6 pace the two
drop bags are ~2h04-2h13 apart, so a notice sent at the turnaround arrives at the start/finish
with well over an hour of slack. The tight case is realising it just *after* leaving the
start/finish — which is another argument for sending on the first suspicion rather than at the
next bag.

**Three things to arrange BEFORE race day, none of which work if left to the night:**

1. **Pre-arm it.** Agree the message in advance — one text, no explanation required — so the
   mid-race action is a single tap rather than composing a request at hour 20.
2. **Confirm they will actually be woken by it.** A phone on silent at 03:00 is the whole plan
   failing quietly. Agree the hours they are on call (realistically 01:00-06:00) and check
   notifications will get through.
3. **~~Check cell coverage.~~ — ANSWERED 2026-09-08: there is signal throughout the course.**
   So the notice genuinely can go out from anywhere, the moment the thought occurs, and no part of
   this decision is tied to reaching a particular point on the loop.

**The fallback if they do not make it is unchanged and still works:** alarm only, at the
start/finish, 15-20 minutes, among people and noise. The wakers make the nap better; they are not
what makes it possible.

**~~A planned 15-20 minute lie-down is legitimate strategy~~ — demoted 2026-09-08.** An earlier
draft of this section presented the nap as part of the plan. It is not; the athlete had already
decided on no sleep, and that decision is the mainstream one rather than a gap to be corrected.

### After the finish — a nap on site, then a ride (athlete, 2026-09-08)

**He is not driving home.** The plan is to lie down for a few hours at the finish and wait for a
ride. Two consequences, and the first is the one that actually bites:

- **~~Lying still is when he gets cold~~ — SOLVED 2026-09-08.** Athlete: **sleeping bag, sleeping
  mat and a dry set of clothes staged at the start/finish.** That is the complete answer, and the
  **mat is the half people leave out** — lying on cold ground loses heat by conduction faster than
  air does, so a bag without a mat underperforms badly. Thirty hours of sweat, an October night in
  the 40s°F and a body with nothing left to generate heat is how ultras go wrong *after* the timing
  mat; this closes it.
- **This kit is separate from the running warm layer** in the open items below, and staging it does
  not resolve that one. Different job, different garment, different hour.
- **The ride has to be arranged around a finish time that could span eleven hours** — 00:24 on the
  100km A-goal, 11:49 on the 100-mile stretch. That is not a pickup time anyone can plan blind.
  Likely the same people as the wakers above; agree in advance that the call comes when it comes.
  Signal throughout the course means he can give real notice from the last lap rather than a guess.

**One thing to be aware of rather than to fix: the contingency nap and the post-race nap now use
the same bag, on the same mat, in the same spot.** The kit does not know which one is happening.
What separates them is the decision rule already on the card — **decide at the bag, and never
inside the twenty minutes after standing up.** That rule is doing more work than it looks like it
is, because at 04:00 on lap 5 a made-up bed is the most persuasive object on the course.

### The pacer

- **One lap, and it is the single dose of external judgement available. Spend it in the deep night
  — lap 5 or 6, not lap 2.** Laps 1-3 he will be lucid and a pacer adds only company; laps 5-6 are
  the fatigue-plus-sleep-pressure-plus-darkness state this whole block was built around, and that
  is when a second opinion on feet, cognition and the stop decision is worth most.
- **The rule does not bind.** Pacers are allowed from lap 2 onward; every lap worth pacing is
  already legal. No latitude needed from anyone.

Nothing left in the calendar rehearses a full night. The night sessions that inform this: 09-12
(5 of 7 hours dark), 09-26 night long run, 10-06 taper night run.

---

## Notes from the 2024-10-19 Ghost Train 50k

Two full laps plus extra. Slow, but **the limiter was not the athlete** — a friend was suffering
debilitating muscle cramps and the day was run at his pace. Self-assessment: *"I could have stayed
jogging the entire time"*, and *"I didn't have that much to complain about."*

**What worked in 2024:** Tailwind rather than water at aid stations, most of the way; a lot of
candy plus salty snacks; jogging remained available throughout — aerobic capacity was never the
constraint.

### ⚠️ THE ONE THING THAT ENDED THE DAY — and it is NOT "he sat down"

> After two full laps he **sat down in his tent to change**. On standing up, legs that had been
> perfectly capable of jogging moments earlier were **in pain and stiff**. He crossed 50km and
> stopped.

**~~The distance didn't end that race. Sitting down did.~~ — CORRECTED 2026-09-08, by the
athlete, and this is the more useful lesson.**

His own takeaway: *"I would have been fine if I had waited another 20 minutes instead of
immediately walking, not that I should not have sat down at all."*

**What actually ended the day was reading transient post-sit stiffness as a verdict.** He stood
up, tried to walk on legs that had just stopped for the first time in six hours, found it painful,
and concluded he was done. The stiffness was a phase, not a state — and he had another 100km of
capacity underneath it.

**The 2026-09-06 data point proves the phase resolves, and this file previously drew the wrong
mechanism from it.** He was *"locked up"* getting into the car after 30.08km and *"a lot more loose
and comfortable"* twenty minutes later at home. `log/2026-09-06.md` recorded that as *"it released
once he was moving again"* — **he was sitting in a car for those twenty minutes.** He was not
moving. **Time released it, seated.** The movement explanation was assumed because it is the
textbook one, and the observation does not support it.

**Rules that follow — and they are about interpretation and timing, not about chairs:**

1. **Stiffness on standing after a stop is NOT information about whether you can continue.** It
   is the most predictable thing that will happen to you all race, it has resolved in ~20 minutes
   on both occasions it has been observed, and it arrives at exactly the moment you are most
   likely to be weighing a stop. **Never make a continue/stop decision inside that window.**
2. **Do not immediately walk it off, and do not immediately quit on it.** Both are decisions made
   during the phase. Give it time — moving gently is fine, sitting a bit longer is fine, but the
   *judgement* waits.
3. **Sitting is allowed, and it is time that has to be budgeted honestly.** A stop long enough to
   need a sit is a stop long enough that standing up will hurt and the next ~20 minutes will be
   slow. That is the real cost — not damage, not danger, just a tax that has to be worth paying.
   Change kit standing when it is a two-minute job, because it is faster, not because sitting is
   forbidden.
4. **This is what makes the contingency lie-down above usable at all.** If it is ever needed,
   expect to feel terrible standing up from it. That feeling is not the answer to whether the race
   continues — it is the twenty minutes you already knew were coming.

**The old file's rule was "brief the crew: their job includes not letting you sit down."** There
is no crew, and the rule was wrong anyway. **The job that replaces it is not enforcement, it is
patience** — and it is on the card as a rule about *when to decide*, which is the thing a card can
actually deliver at hour 18.

### What this changes about the 2026 goal

He covered 50km with capacity in hand, at someone else's pace, and stopped for a reason that is
entirely preventable. That materially strengthens the 100km primary goal — it is not an
extrapolation from an unknown, it is the same course with the specific failure removed and a real
training block behind it.

---

## Open items — the only things on this page not decided

1. **~~A WARM LAYER. Nothing is chosen and nothing is staged.~~ — CLOSED 2026-09-08.** 120 GSM
   Alpha Direct hoodie + Rab approach jacket + fleece gloves + Burton headband, beanie in each bag.
   See § The full night system. **The only thing added rather than confirmed: a spare pair of
   gloves in each drop bag** — wet fleece is worse than none, and cold wet hands are what make the
   blister kit unusable.
2. **Ibuprofen → acetaminophen.** Both bags currently carry ibuprofen. NSAIDs across 30 hours of
   dehydration and sustained muscle breakdown carry a real acute-kidney-injury risk, and it is a
   worse bet uncrewed with nobody watching him. Acetaminophen does the analgesic job without that
   mechanism. **Athlete's call; the recommendation is to swap.**
3. **`rules/fueling.md` § Caffeine is still a TODO**, and the sleep plan above is written assuming
   it will say what is written here. Reconcile the two.
4. **Re-read the goal tiers after 09-12, 09-26 and 10-03.** They are an assessment made on a
   4h19 longest effort and they should not survive unexamined once that number changes.
