# The VO2max block — Nov 2026 to Jul 2027

**The goal is the number, not a race.** Athlete, 2026-11-14: *"Vo2 max improvement is my goal"*,
and *"I'm just running races for fun except the ghost train, but I'll have plenty of time to train
for that later."*

**Tracked metric: the watch's own `MAXVO2` estimate.** Lab testing is ruled out. Retrieval path and
the reading history are in
[`.claude/skills/daily-brief/references/suunto-fields.md`](../.claude/skills/daily-brief/references/suunto-fields.md)
§ The watch's VO2max estimate — **`workouts_extensions` returns 500s on this account; the number is
in the SML header.**

| | |
|---|---|
| **Stale baseline** | **48.6**, 2026-08-23 5k PR. Does not describe him after a 100km race and 30 days off |
| **Live baseline** | **the 2026-11-15 90min run** — [endurance/2026-11-15-baseline-long-easy.md](../endurance/2026-11-15-baseline-long-easy.md) |
| **Running since the race** | **none**, 2026-10-17 to 2026-11-14 |
| **Alongside, continuously** | [`strength/itb-protocol.md`](../strength/itb-protocol.md), 3×/week, from week 1 |

**This replaces [`training/block.md`](block.md) as the live policy document.** That file is the
Ghost Train 2026 block and is now historical — read it for its reasoning, don't apply its weekly
template, its walking targets or its Champion-week mapping here.

## The one fact that sets the structure

**VO2max stops responding after about 6 to 10 weeks of focused work.** So the period cannot be one
long block of intervals — it would plateau in February and sit flat.

**The answer is cycles.** Six-week VO2 blocks separated by three-week threshold bridges, which
restore responsiveness and raise the ceiling the next block works under.

**And therefore every week of delay costs a cycle, not just time.** Athlete, 2026-11-14:
*"starting early means I can get another cycle in."* **He is right, and an earlier draft of this
file had it backwards** — it argued that starting early meant plateauing early, which only holds
for a single continuous block and not for the cycled structure the same file proposes. **Cycle 1
therefore starts the week after the restart week, with nothing in front of it.**

**There is no taper in this plan and nothing peaks.** Races are for fun.

## The phases

**There is no base phase.** Athlete, 2026-11-14: *"Why base weeks at all? I spend nearly 6 months
doing base building last year."* **He is right and the word was doing two jobs.** Aerobic base he
has in abundance — six months of ultra work and a 100 km race. **What he lacks is recent fast
running**, and that is not bought with easy miles; the last of it was the 2026-08-23 5k TT.

**So the ramp-in lives inside cycle 1 instead of in front of it:** flat strides, hill strides and a
15min steady finish in week 1; a 2×10min threshold session and the 5k TT in week 2; full intervals
from week 3. **It is a ramp-in, not a soft fortnight** — an earlier draft had nothing but 20s
strides in it, which the athlete caught on 2026-11-14 (*"Are those workouts just strides?"*), and
which would also have produced a soft TT and therefore four weeks of wrong interval paces.

**A ramp-in inside cycle 1 is better preparation than a base phase in front of it would be** —
easy running does not load a tendon the way a stride or a hill does — and it buys three weeks.

| phase | dates | weeks | what it is |
|---|---|---|---|
| **0 — Restart** | Sun 11-15 → Sat 11-21 | 1 | [w24.md](weeks/w24.md). 90min baseline effort, then 30/35/40min with a rest day between each |
| **1 — VO2 cycle 1** | Mon 11-23 → Sun 01-03 | 6 | **Wk 1 strides + hills + steady finish, wk 2 threshold + 5k TT Sat 12-05, wk 3-6 full intervals.** ITB protocol from day one |
| **2 — Bridge** | Mon 01-04 → Sun 01-24 | 3 | **VO2 work stops.** Threshold and tempo + easy |
| **3 — VO2 cycle 2** | Mon 01-25 → Sun 03-07 | 6 | Full cycle, no ramp-in needed |
| **4 — Bridge** | Mon 03-08 → Sun 03-28 | 3 | Threshold again |
| **5 — VO2 cycle 3** | Mon 03-29 → Sun 05-09 | 6 | **New Castle 10k on Sun 04-25 falls in week 4.** Run for fun |
| **6 — Bridge** | Mon 05-10 → Sun 05-30 | 3 | |
| **7 — VO2 cycle 4** | Mon 05-31 → Sun 07-11 | 6 | Then reassess, and start turning volume toward Ghost Train |

**Three cycles by 05-09 and a fourth by mid-July.** The first draft of this file managed two by the
end of April.

**What the ramp-in is still protecting, now that the base argument is gone.** One thing only, and
it is not the ITB — the ITB has never flared on anything under an hour (athlete, 2026-11-14), so no
interval session is in its range:

**Tendons, calves and achilles have had no fast running since August**, and 30 days with no running
at all on top of that. **The first hard interval session is the single highest-risk session in this
plan.** Two weeks of strides, hills, a steady finish and a threshold session is what makes it
survivable, and skipping them would not buy a fifth cycle — it would just move the risk.

## Cycle 1, week by week

**Weeks 1-2 are authored.** Weeks 3-6 are structure only, and deliberately so — see below.

| wk | dates | week file | what it is |
|---|---|---|---|
| 1 | Mon 11-23 → Sun 11-29 | [w25.md](weeks/w25.md) | **ramp-in: strides, hills, steady finish.** 5 runs, 234min. 6×20s flat, 6×20s uphill, 15min ZS Z2 |
| 2 | Mon 11-30 → Sun 12-06 | [w26.md](weeks/w26.md) | **2×10min threshold + 5k TT Sat 12-05.** 5 runs, 236min |
| 3 | Mon 12-07 → Sun 12-13 | *not authored* | first full interval week. Quality 1: 4×3min. Quality 2: 8×1min |
| 4 | Mon 12-14 → Sun 12-20 | *not authored* | 5×3min; 10×1min |
| 5 | Mon 12-21 → Sun 12-27 | *not authored* | 4×4min; 2×(6×30/30). **Christmas week — hold volume, do not add** |
| 6 | Mon 12-28 → Sun 01-03 | *not authored* | 5×4min; 2×(8×30/30). Then the bridge |

**Weeks 3-6 cannot be authored yet, and the reason is a rule rather than caution.**
`AGENTS.md` invariant 4 requires every session to name the instrument it is followed by, derived
from the shortest work interval — and **3-4min reps land in the "pace, ZoneSense lags" band, so
those sessions need pace targets.** The only pace available is `athlete/zones.yml`'s `vo2: 5:09`,
which is 5k race pace and **wrong in a known direction by an unknown amount** (see § Intensity).
Authoring four weeks of interval sessions against it would prescribe the wrong pace four times over.

**The 12-05 TT produces the number, and weeks 3-6 get written that weekend.** This also matches
`rules/publishing.md`, which wants a rolling ~2-week window on the watch rather than the whole
block at once.

## Shape of a VO2 week

**Working assumption: 5 running days.** The athlete was asked and has not answered yet, so this is
the standard build until he does. **The poll answer changes the easy-day count, not the structure**
— the two quality days are the block, and 4 days works nearly as well as 6.

| day | session |
|---|---|
| Mon | easy 40-50min |
| Tue | **quality 1 — long intervals.** 4-5 × 3-4min hard, equal jog recovery. ~20min of work |
| Wed | easy 40-50min, or rest |
| Thu | easy 40-50min |
| Fri | rest |
| Sat | **quality 2 — short intervals.** 30/30s or hill reps. More time near VO2max, less lactate |
| Sun | easy 60-75min |

**~300 min/week**, against `weekly_total_max_min: 600` in `athlete/profile.md`.

**Time has stopped being the binding constraint.** That premise was written for a 100-miler. A
VO2max block needs roughly half the old budget, and **the spare hours should mostly stay spare** —
more easy volume is not what moves this number, and recovery between quality days is.

**Two quality sessions a week is the ceiling, not a starting point.** A third does not add
adaptation; it adds fatigue that degrades the first two.

## Intensity — do not use the stale numbers

**`athlete/zones.yml` has `vo2: 5:09`, which is 5k race pace.** His 5k takes 25:44 — far longer
than the ~6 minutes that defines true VO2max pace — **so his actual interval pace is faster than
5:09**, and the entry was fine only while VO2 work was a garnish.

**It gets re-derived from a 5k time trial on Sat 2026-12-05**, at the end of cycle 1's two-week
ramp-in and before the first full interval session. That test does two jobs: sets real zones, and
produces the cleanest possible reading of the goal metric. **It is also the ramp-in's graduation
exercise** — about 25 minutes of hard running, which is roughly one interval session's worth, taken
in one piece with nothing riding on it but the numbers.

**Until that test, VO2 work is run on effort, not on a pace from the file.** Writing a session
against a stale `vo2:` would prescribe a pace that is wrong in an unknown direction.

### What the 12-05 TT calibrates, and how — the procedure for 12-06

**Do this on the Sunday after the TT, before authoring weeks 3-6.**

| gets calibrated | from what | confidence |
|---|---|---|
| **5k pace** | the TT time itself | **exact.** It is a measurement |
| **`threshold`** | 5k pace × ~1.05, the ratio `zones.yml` already corroborated on 2026-08-15 (5:25 / 5:09 = 1.052) | **good** |
| **`tempo`** | threshold + 15s, the gap this table has always held | good |
| **`vo2`, `rep`, `stride`** | **estimate only — see below** | **provisional** |
| **ZoneSense vs pace** | the 12-01 threshold session and the TT together — what pace did ZS Z2's upper end actually correspond to | **the useful cross-check** |
| **the goal metric** | `MAXVO2` from the TT's SML header | the first high-quality reading |

**`vo2` is the one a 5k cannot pin, and this is the trap the current file fell into.** VO2max pace
is the pace sustainable for roughly 6 minutes; his 5k takes ~26. **So 5k pace is a floor for `vo2`,
not a value for it** — which is exactly the error `vo2: 5:09` encodes. Set it a few seconds per km
faster than the new 5k pace, author week 3's 4×3min against that, and **then let the session itself
settle it**: if the reps are comfortably held with the last one no harder than the first, the pace
is too slow and the entry moves. That feedback loop is the same one `zones.yml` already runs on
`threshold` via RPE.

### What the TT does NOT calibrate, and must not be used to

- **`easy_ceiling`, `long_run`, `recovery`.** `zones.yml` is emphatic that a 5k says nothing about
  the endurance end, and that **running easy days too fast is this athlete's most likely training
  error** — a standing warning that gets *stronger* with a fresh test in the legs, not weaker.
  **Leave 7:00/km alone.**
- **Whether the ITB tolerates volume.** Nothing in the ramp-in goes past an hour except one 60min
  run. That question is not asked until the Ghost Train build.
- **The hip-drop asymmetry.** That re-tests on its own 8-week clock
  ([`strength/itb-protocol.md`](../strength/itb-protocol.md)), around mid-January.

**And expect the new numbers to go stale fast.** Three weeks off a layoff is a rapidly moving
target: paces set on 12-05 will understate him by cycle 1 week 6. That is what the end-of-cycle
re-tests in § Measurement are for, and it is why ZoneSense carries anything ≥9min in the meantime —
it reads the athlete rather than the file.

## Measurement

| when | what |
|---|---|
| **Sun 2026-11-15** | **baseline.** Expect it below 48.6 — 30 days off is a real detraining effect, and a low floor is better than a stale peak |
| **Sat 2026-12-05** | 5k TT — zones, and the first high-quality reading |
| **early Jan 2027** | end of VO2 cycle 1 |
| **early Mar 2027** | end of VO2 cycle 2 |
| **Sun 2027-04-25** | New Castle 10k. Run for fun, and it is also the best reading the estimator can get |
| **early May 2027** | end of VO2 cycle 3 |

**Read the trend, not single numbers.** Two readings eight weeks apart differed by 0.6 across an
entire training block — **a 1-2 point move is noise.** The estimate also wants sustained running at
a decent intensity, so an easy jog and an interval session both read poorly; the good readings come
from steady hard efforts.

## What is NOT in this plan

- **No Ghost Train 2027 preparation.** *"Plenty of time to train for that later"* — the build
  starts after this block, not inside it. [`strength/itb-protocol.md`](../strength/itb-protocol.md)
  is the one thread that does run all the way through, and it is injury work rather than race prep.
- **No taper for the 10k**, and no peaking for anything.
- **No long runs beyond ~75min.** Nothing here needs them, and they are the sessions that provoke
  the ITB.
- **No general strength program yet.** Liftoscript ends at week 11. The ITB protocol stands alone
  until there is a reason to add more.
