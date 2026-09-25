# Strength notes — substitutions, equipment, cues

## Live in Liftosaur

Pushed via the Liftosaur MCP (`mcp__liftosaur__update_program`, id `haqytaxt`) as **"Ghost Train
Block"** — this replaced the athlete's pre-existing "My Program 2" (a general machine/dumbbell
hypertrophy split, unrelated to this training block; confirmed with the athlete before
overwriting). Re-push this file with the same tool whenever it changes; `strength/program.liftoscript`
is the source of truth, the app is the execution surface.

## Week ↔ block-week offset

Liftoscript `# Week 1` = block week 9 (2026-08-03). To find the Liftoscript week for any block
week: `liftoscript_week = block_week - 8`.

## Strength is best-effort — running has priority (athlete-confirmed 2026-08-12)

The athlete is time constrained and lifting is the first modality cut when the day compresses.
See `athlete/profile.md` § "Priority when time is short". Two consequences for this file:

- **The 4-day split stays as authored.** Best-effort means aim high, not lower the target.
- **Missed lifts are recorded, not escalated.** They are the expected cost of the constraint.
  Do not read a run of them as an adherence problem or a signal to re-author the program.

This is also the standing reason the pointer drift below never resolves.

## Pointer drift — the app's "next workout" is not the calendar's

**Liftosaur advances by completion; this plan advances by date.** The app's next-workout pointer
moves only when a workout is finished, so every skipped lift leaves it one session further behind
the block calendar — permanently, and it never catches up on its own.

This is expected, not a bug to fix. It is the direct consequence of the split already stated
above: **`strength/program.liftoscript` is the source of truth, the app is the execution surface.**

Two things follow, and both matter in practice:

- **Open the day the calendar says, not the day the app offers.** Tap through to the right week
  and day in the program screen. As of 2026-08-10 the app offers `Week 1 — Upper B` (last
  completed session was Week 1 Lower B on 08-06) while the calendar is on `Week 2 — Lower A`.
- **The pointer cannot be moved through the MCP.** No tool reads or sets the current week/day —
  `get_program` returns only id, name, text, and isCurrent. The only things that would move it
  are completing a workout or fabricating one, and fabricating a workout to fix a pointer puts
  invented sets into the training history to paper over a cosmetic mismatch. Don't.

So: don't try to realign the app. Reconcile the *records* instead — check `get_history` against
`log/` each morning, write down what actually happened, and navigate by hand.

**Every week is fully self-contained — do not rely on Liftoscript's carry-forward mechanism
(leaving a `## Day` header empty to inherit the previous week's exercise).** Tested extensively via
`run_playground` with real chained execution — Week 1 completed for real
(`complete_set()`+`finish_workout()`), then Week 2 simulated from the resulting
`updatedProgramText` — and Week 2 still returned "Exercise not found." Reproduced across six
separate test constructions, including one built directly from the Liftoscript reference's own
documented example. Root cause unconfirmed (simulator limitation vs. real engine behavior), but a
live session showing 0lb or a missing exercise isn't a risk worth taking.

**So: when appending a new week, write out every exercise explicitly** (weight, sets, reps —
nothing omitted), copying the previous week's structure and applying that week's
readiness/taper adjustments from `rules/progression.md` and `training/block.md`. Spot-check the
result with `run_playground` (`complete_set` + inspect the returned weight) before pushing,
especially for any week with a structural change (taper, dropped day, resumed day) — those are
exactly the cases most likely to silently break.

## Starting weights are estimates, not measured maxes

Squat, Romanian Deadlift, Bench Press, Bent Over Row, Overhead Press, Pull Up (added load), and
Incline Bench Press are all free-weight/barbell movements the athlete doesn't currently do — his
real numbers in "My Program 2" were on Smith Machine, Leverage Machine, or dumbbell equivalents
(and several tracked as % of an internal training max), which isn't a valid 1:1 substitute for
free-weight loading. Rather than guess a real number from mismatched equipment, Week 1 starts
deliberately conservative (see `athlete/maxes.yml`) and the file hand-steps a slow, safe
progression (~5lb/week on main lifts, 2.5lb/week on OHP and Pull Up) across the 10 weeks. **Correct
these numbers with the athlete's actual felt output as real sessions happen** — if a prescribed
weight is trivially easy, jump it by hand in the next push rather than waiting out the slow ramp.

## Substitutions

**2026-08-06 — Nordic Curl has no anchor at home.** No bench and no partner to hold the feet.
Kept as **Nordic Curl** (the exercise name and prescription are unchanged, 3x6 bodyweight) but
**couch-anchored**: hook feet under a couch or other heavy, stable furniture instead of a bench.
Same movement, same stimulus — this is a standard home substitute, not a different exercise.
Noted in the program as a `//` description on the Week 1 line, which carries forward to every
later week automatically.

**2026-08-06 — Single Leg Calf Raise and Copenhagen Plank had no way to record both sides.**
Athlete reported the app gave him one field for each, when both are unilateral. Root cause,
confirmed by comparing to Single Leg Deadlift (which DOES auto-split into left/right in the
logged history despite being authored identically, `3x10` with no `|`):

- **Per-side rep tracking (`completedRepsLeft[n]`) only applies to certain BUILT-IN exercises.**
  Single Leg Deadlift is one; the custom "Single Leg Calf Raise" (`hgctmizg`, created because no
  built-in single-leg calf variant exists) is not, and `create_custom_exercise` has no field to
  request it — this isn't a config we missed, the API has no such option.
- **Timed holds have no per-side tracking at all, regardless of built-in status.** Copenhagen
  Plank is built-in but the reference confirms there's no `completedSetTimeLeft` or equivalent.
  The `30s|30s` we'd written is `setTimer|restTimer` (hold 30s, rest 30s) — not a left/right
  split. There was never a per-side option here to miss.

**Fix: double the set count, keep the reps/hold-time and total per-side volume unchanged.**
`Single Leg Calf Raise / 4x12` → `8x12` (4 sets/leg, matching how the stats tool already counted
the old prescription — this is a recording-granularity fix, not a volume increase).
`Copenhagen Plank / 3x1 30s|30s` → `6x1 30s|30s` (3 holds/side, same as before). Description
comments on each Week 1 line tell the athlete which sets are which side; they carry forward.
Verified via `run_playground` with real `complete_set()`/`change_set_time()` calls before pushing.

**Session-length cost, worth knowing:** `get_program_stats` puts Lower B at ~50min now, up from
~36min, purely from the extra rest-timer transitions (14 more total sets, same total work).
Still under `time_budget.lifting_session_min`'s 60min cap but with less room than before.

**2026-08-04 — no barbell at home, home is the primary training location.** Athlete has an
adjustable Bowflex SelectTech 552 pair (5–52.5lb/hand, 2.5lb increments) and nothing else. Squat,
Bench Press, Bent Over Row, Overhead Press, and Incline Bench Press converted to their `, Dumbbell`
equipment variant. Romanian Deadlift has no Dumbbell variant in Liftosaur's exercise list — replaced
with **Stiff Leg Deadlift, Dumbbell** (same hip-hinge pattern, same equipment). Bulgarian Split
Squat was already dumbbell-equipment by default and needed no change.

This was a full progression *redesign*, not a mechanical halving of the barbell numbers — halving
would have exceeded the SelectTech's 52.5lb/hand ceiling by Week 4. The new progression peaks at
32.5lb/hand (Squat/Stiff Leg Deadlift, Week 9), comfortably inside range for the whole block.

**2026-08-04 (same day) — Bench Press / Bent Over Row / Overhead Press start higher.** Athlete's own
correction to the conservative initial estimate: Bench Press and Bent Over Row start at **35lb**
(not 15lb), Overhead Press at **20lb** (not 12.5lb). Same weekly cadence as originally designed,
just re-based. Squat/Stiff Leg Deadlift/Incline Bench Press were unaffected by this correction.

**2026-08-04 (evening) — re-based again, this time from real data.** The first actual session
(Week 1 Upper A, logged in Liftosaur 21:11, 24.7min) is the first evidence this program has ever
had, and it corrected the morning's guess in both directions:

| Exercise | Prescribed | Actual | Action |
|---|---|---|---|
| Bench Press, DB | 3x5 35lb | 3x5 35lb | correct — ladder unchanged |
| Bent Over Row, DB | 3x8 35lb | 3x8 **25lb** | **decoupled from Bench**, own ladder 25 → 37.5lb by Wk 9 |
| Overhead Press, DB | 3x8 20lb | 3x8 **25lb** | re-based +5: 25 → 35lb by Wk 9 |
| Pallof Press | 3x10 20lb | 3x10 **27.5lb** | re-based +7.5: 27.5 → 32.5lb |

He also took the **full 3x5 tier** on bench rather than dropping down the readiness ladder.

Bench and Row had been locked to identical numbers in all ten weeks, which was never justified —
they're different lifts with different strength. Tonight separated them, and the athlete confirmed
35 was genuinely too heavy for the row rather than a form or scheduling artifact.

**The ceiling watch now applies to BENCH ONLY.** Bench still peaks at **47.5lb/hand by Week 9**,
5lb (2 increments) under the SelectTech's 52.5lb ceiling — if it progresses even one week ahead of
schedule it runs out of dumbbell before the block ends, and at that point either hold the weight
and add reps/sets, or buy heavier dumbbells. Row now peaks at 37.5lb and is no longer near the
ceiling; that risk is retired.

Record further swaps here the same way:

```
Bent Over Row, Dumbbell -> Chest-Supported Row, Dumbbell  (reason, log/YYYY-MM-DD.md link)
```

## Equipment mapping

Home gym: adjustable dumbbells (Bowflex SelectTech 552, 5–52.5lb/hand) only, **no barbell**. The
travel fallback table below assumes gym/hotel access instead, which may have a barbell again —
don't assume the home substitutions apply on the road, check what's actually available.

## Cues

- **Squat, Dumbbell / Stiff Leg Deadlift, Dumbbell (Lower A):** these are the two lifts most likely
  to interfere with running if pushed too hard — this is exactly why Lower A sits as far from the
  long run as the weekly template allows. Don't chase PRs here at the expense of Saturday.
  "Stiff Leg Deadlift" is the RDL substitute — see Substitutions above for why.
- **Nordic Curl (Lower B):** notoriously produces significant DOMS even at low volume — keep it at
  3x6 bodyweight as programmed, don't add load even on a green readiness day, since the soreness
  cost is disproportionate to the stimulus for a runner.
- **Single Leg Calf Raise:** this is the single highest-value accessory in the whole program for
  ultra durability — calf/achilles tolerance is a common failure point late in a long race. Don't
  cut this one when trimming volume; cut something else first.
- **Copenhagen Plank:** adductor/hip stability, directly protective against the lateral-stability
  breakdown that shows up in fatigued running form late in a race.
- **Pull Up:** programmed as `Pull Up` with an `update:` script (`weights = bodyweight +
  originalWeights[ns]`) so the app displays total system weight, while `progress:`/the hand-authored
  steps only move the added-load portion. Requires bodyweight to be set in Liftosaur to display
  correctly — recorded 2026-08-04 (162lb, via `add_measurement`). Re-record when it changes; the
  `update:` script reads the current value live, so it doesn't need re-pushing with the program.
- **Custom exercises:** `Single Leg Calf Raise` and `Dead Bug` aren't in Liftosaur's built-in
  exercise list and were created as custom exercises (via `create_custom_exercise`) rather than
  substituted for something close-but-different. If either needs editing, update the existing
  custom exercise by name rather than creating a duplicate — that preserves workout history.

## Travel fallback — 2026-08-22 to 2026-09-01 (block week 12, Liftoscript Week 4)

Gym access is uncertain while away. Rather than fork the program file (which would break the
calendar's week↔day mapping), keep Liftoscript Week 4 as written and substitute per-exercise if
the equipment isn't there. Lifting is first in the cut order anyway — a travel week that loses
some strength work is working as designed, not failing.

| Programmed | Bodyweight / hotel substitute |
|---|---|
| Squat | Bulgarian split squat, or single-leg squat to a chair |
| Romanian Deadlift | Single Leg Deadlift, bodyweight, slow eccentric |
| Bench Press | Push-up variations (feet elevated to add load) |
| Bent Over Row | Inverted row under a table, or band row |
| Pull Up | Whatever bar exists; else band pulldown |
| Overhead Press | Pike push-up |
| Incline Bench Press | Decline push-up |
| Face Pull | Band pull-apart |

Lower B is nearly bodyweight already (calf raise, Nordic, single-leg RDL, Copenhagen, dead bug) —
it travels unchanged and is the session to protect if only one lift happens that week, since the
calf/achilles work is the highest-value durability item in the whole program.

## Big Day week — 2026-08-31 to 09-06 (block week 13, Liftoscript Week 5)

Champion week 10 moves the block's workout to Tuesday (`training/weeks/w13.md`), which puts
Monday's Lower A the day before a quality session — exactly what `rules/strength-authoring.md`
says to avoid whenever avoidable. Since the Tuesday placement is fixed by the calendar rather than
a morning-of readiness call, Lower A is locked to tier-3 volume (accessories cut, mains at a
single set, same weight as the normal progression) rather than left at the tier-1 default for the
readiness ladder to downgrade. Upper A (Tue) is unaffected — upper body doesn't interfere with a
running quality session.

## Hip flexor eccentrics — the loaded leg-drop (2026-09-22)

**Designed by the athlete's mother, a Pilates instructor.** It is better targeted than the reverse
Nordic curl this session proposed, and the reason is specificity: the failure mode is swing-phase
leg drive, and this is a loaded, exaggerated swing-phase deceleration. A reverse Nordic is a
kneeling lean-back, which shares the muscle but not the movement.

**The movement**, as he described it:

1. Lie supine, **hips elevated ~6 inches on a foam roller**, ankle weights on.
2. Raise the knee to the chest.
3. Extend the leg straight up.
4. **Throw the leg toward the ground and stop it before it lands.**
5. 12 reps.

**Why each part is doing work:**

| element | what it buys |
|---|---|
| **hips elevated 6"** | lets the leg travel *past horizontal* into real hip extension — the lengthened position where eccentric adaptation happens. On the floor you stop at neutral and get nothing |
| **straight leg** | long lever, so high hip torque for a small ankle weight |
| **ankle weight** | distal mass, and the dose dial |
| **"throw" then stop** | accelerating into the eccentric raises peak force — the same trick the downhill session uses |

**Which muscle it hits.** Decelerating hip extension loads **iliopsoas and rectus femoris**
together. With the knee straight, RF is lengthened at the hip but short at the knee, so the bias is
toward iliopsoas. His soreness is **front of thigh (RF)**, so a reverse Nordic is the more
RF-specific option — but it is far less like running, and specificity wins here.

### Bout 1 landed too laterally — the fix, 2026-09-24

Athlete after bout 1: *"I feel it a little too much on the outside, so I need to modify the movement
to get a little more inward."*

**Outside means TFL took a disproportionate share.** TFL flexes the hip but also **abducts and
internally rotates** it, so it gets recruited whenever the leg drifts away from the midline or the
toe turns in. Iliopsoas and the midline of rectus femoris — the tissue that actually complains at
50 km — sit medial to it.

**Cues for bouts 2 and 3, all aimed at the same two things:**

| cue | why |
|---|---|
| **Drop the leg slightly ACROSS the midline**, not straight down in its own plane | a few degrees of adduction takes TFL out of its best line of pull |
| **Toe turned slightly OUT** | TFL internally rotates, so external rotation unloads it and biases medial |
| **Pelvis square — do not let it rotate toward the working side** | pelvic rotation hands the movement to TFL |
| **Throw slightly less hard** | a violent throw recruits whatever is most available; position cannot be held while fighting momentum |

**This is a targeting fix, not a dose reduction.** The load was right — soreness 4 the day after
36 weighted reps per side is expected. It just landed a couple of inches lateral to the target.

### Dosing — the throw is the risk, not the reps

**A maximal lengthened eccentric is the exact mechanism of a hip flexor strain**, and the race is
close. So:

**~~primer Sun 09-27, real bout Mon 10-05.~~ — OVERTAKEN 2026-09-22. He did it the same day**, and
at three times the dose: **3 sets of 12 weighted throws per side**, first exposure. *"I'll be fine
by Friday."* The graded plan below is kept only to show what was proposed.

**He wants three bouts total** (athlete, 2026-09-22: *"I need 2 more bouts of hip flexor"*).

| bout | when | dose | DOMS lands on |
|---|---|---|---|
| ~~primer~~ | ~~Sun 09-27~~ | ~~unweighted, half range~~ | — |
| **1 — done** | **Tue 09-22** | **3x12/side, weighted, thrown** | Wed 09-23, Thu 09-24 |
| **2** | **Mon 10-05** | same | Tue 10-06 night run 40min, Wed 10-07 easy 47min |
| **3** | **Wed 10-07** | same | Thu 10-08 easy 30min, Fri 10-09 rest |

### Why both remaining bouts land in week 18, and nothing earlier works

Every date between 09-23 and 10-03 puts DOMS on something that cannot absorb it:

| date | DOMS lands on | blocked by |
|---|---|---|
| 09-26 | Sun rest, **Mon 09-28** | **Lower A, the block's last heavy squat day** — squats load hip flexors deep in the hole |
| **09-27** | **Mon 09-28**, **Tue 09-29** | **same heavy squat, then the threshold session.** This slot was proposed on 09-22 and is WRONG — it was scheduled before the w17 squat day was checked |
| 09-28 | Tue 09-29 | last hard midweek session of the block |
| 09-29, 09-30 | — | **travel.** Foam roller and ankle weights are at home |
| 10-01, 10-02 | Sat 10-03 | **lap simulation 2, the full dress rehearsal** |
| 10-04 | Mon 10-05 easy | workable, but it stacks eccentrics onto legs fresh off a 105min b2b — higher strain risk for no gain |
| **10-05, 10-07** | easy runs and rest only | **clear** |
| 10-08 | Sat 10-10 | final GI long run, then the 5k on 10-11 |
| 10-12 | race week | available, and the fallback if he wants wider spacing |

**10-05 and 10-07 are three days apart, which is fine** — bouts days apart still stack protection,
and bout 2's soreness should already be low. **Mon 10-12 is the alternative for bout 3** if he wants
the spacing instead; DOMS by then is minimal, but it is race week and the benefit is small.

**Bout 1 alone was probably enough.** A 3x12 weighted first exposure is a substantial bout, so 2
and 3 are reinforcement rather than the mechanism. **Nothing is lost by moving or skipping either
one** if a session needs protecting.

**What the 09-22 timing actually costs.** DOMS peaks 24-48h, so Wed 09-23 and Thu 09-24 — and
Friday's 240min night run is 3 days out, past peak. His read is probably right.

**The exposure that matters is not DOMS, it is stride.** Sore hip flexors change how the leg swings,
and Friday is four hours of swinging it. Quad DOMS makes a run uncomfortable; hip flexor DOMS
changes the movement.

**It confounds nothing worth having.** Friday's 240min reaches ~28.8 km and his onset is ~50 km
(`log/2026-09-12.md`), so it was never going to read the hip flexors anyway.

**Two things to watch on the day:**

- **The low back.** Hips elevated plus a weighted straight leg dropping wants to tip the pelvis
  into anterior tilt, and iliopsoas attaches to the lumbar spine. Keep the other knee bent with the
  foot planted, and brace so the pelvis does not tip. If it is felt in the low back, the load has
  gone to the wrong place.
  **VALIDATED 2026-09-23.** After bout 1 he reported DOMS in the **front of the thigh and the lower
  abs**, and no low back. That is the correct signature: rectus femoris took the eccentric load, and
  the anterior core held the pelvis instead of the lumbar spine absorbing it. **Lower abs is the
  marker that the brace worked** — treat its absence, or low back soreness in its place, as a cue to
  fix position before adding load.
- **Range before weight.** Stop the leg higher than feels necessary on the first bout. Peak force
  happens at the deceleration point, so a shorter range is a genuinely lower dose.
- **Strain vs soreness, and this is the one to act on.** A maximal lengthened eccentric is the
  mechanism of a hip flexor strain. **Diffuse ache across the front of the thigh is the intended
  outcome. Sharp or localised pain in the hip crease is not** — that is a different thing and it
  changes what Friday should be.

**This is reasoning from mechanism, not a validated protocol.** Nothing left in the block reaches
50 km (`log/2026-09-12.md`), so there is no way to test whether it worked before race day.

## Taper handling (from `training/block.md`)

The shape is a dip, then one last full session, then down for good — not a monotonic decline:

- **Block week 16 (Liftoscript Week 8): Lower A at reduced volume** — mains 2x5/2x6 at reduced
  load, no tiers, accessories cut. This is the peak *running* week (biggest Saturday, the 03:00
  night long run), and lifting is first in the cut order exactly when running stress peaks.
- **Block week 17 (Week 9): the one final full Lower A — last squat day of the block**, back at
  full tiers and the progression's top weight, ~2.5 weeks out. Last chance for a complete
  strength stimulus that still has time to be absorbed before race day.
- **Block week 18 (Week 10): Lower B + Upper B only**, at reduced sets.
- **Block week 19 (race week): no lifting at all** — the program deliberately has no Week 11.

When editing the program for those weeks, don't just delete lines — replace main-lift entries with
lighter-load or bodyweight equivalents so the file stays a complete, pushable program for every
week rather than having gaps.
