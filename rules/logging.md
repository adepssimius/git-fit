# Logging — the daily record, and the two numbers only the athlete can supply

Five of the seven signals in the readiness ladder (`rules/progression.md`) now come out of the
Suunto wellness API automatically: sleep duration, fragmentation, HRV, resting HR, body resources.
**This file covers the rest** — the two manual signals the watch cannot measure, and the context
that makes the automatic five interpretable.

Everything else in a log entry is a diary. Diaries are welcome and often turn out to matter, but
they are not what the plan reads.

## What the log is for

Three consumers, ordered by how much they actually change the plan:

1. **The readiness ladder** (`rules/progression.md`) needs **soreness** and an **RPE trend**. Both
   are manual. Without them the ladder runs on five signals instead of seven, and — more
   importantly — on five signals that all describe *the night*, none that describe *the legs*.
2. **The re-author triggers** (`rules/progression.md` § "When `log/` should trigger a re-author").
   Two consecutive amber/red weeks pushes the whole Champion-week mapping out, taper included. That
   only fires if amber and red are being written down.
3. **AGENTS.md invariant 8** — anything pulled from Suunto is DRAFT until the athlete supplies
   context. The log is where that context lands. Two corrections have already come from exactly
   this: the 08-02 30k that read as chronic mis-pacing (it was a deliberate 10k in 86°F heat), and
   the treadmill data that was briefly written off as unreliable.

## What NOT to log

**Don't retype anything the watch already recorded** — pace, distance, HR, TSS, sleep hours, HRV,
recovery time. All of it is one MCP call away, and duplicating it by hand is how a log becomes a
chore. Chores don't get done, and a log that stops after two weeks is worse than no log, because
the ladder silently degrades without announcing it.

**The log's job is the part the watch cannot see.** How the legs felt, what the gut did, why the
night was bad, what got cut and why, and what actually happened when the plan said something else.

The one exception is Suunto data with an *interpretation* attached — a pulled table plus the
reading of it, as in `log/2026-08-03.md`. That's not duplication, that's the invariant-8 record.

## One file per day

`log/YYYY-MM-DD.md`. Missing days are fine and mean "nothing worth recording" — this is not a
streak to maintain. **Never backfill a rating from memory.** `null` is honest; an invented 4 is
corruption, and it corrupts precisely the signal the ladder trusts most.

## Frontmatter

```yaml
---
date: 2026-08-04          # ISO, must match the filename
readiness: green          # green | amber | red | null — the day's call, see below
soreness_0_10: 3          # manual. The ladder's only muscular signal.
rpe_0_10: 5               # manual. Session-RPE for the day's MAIN session. null on rest days.
sleep_context: null       # WHY the night was what it was — never the hours. See below.
---
```

| Field | Required | Notes |
|---|---|---|
| `date` | yes | Must equal the filename stem; `verify_plan.py` checks it |
| `readiness` | on training days | The call you acted on, not the call the table suggests |
| `soreness_0_10` | on training days | Anchored scale below — 0–10, whole numbers |
| `rpe_0_10` | when a session happened | Session-RPE, rated ~30min after finishing, not during |
| `sleep_context` | only when there is one | Free text: "sick kid, up 3×", "flight", "watch strap loose" |
| `conditions` | outdoor sessions | Written by `scripts/heat_load.py`, not by hand — see below |

## Conditions — the one block you don't type

Ambient temperature, humidity and sun are the clearest case of "what the watch cannot see": the
Suunto sensor reads body heat off the wrist and has already produced two wrong log entries. So
they are neither retyped nor asked about — `scripts/heat_load.py` takes the session's own GPS
track, pulls the weather that was over that ground, and writes the block:

```bash
python3 scripts/heat_load.py --workout-json workout.json --shade-pct 60 --write
```

**It adds exactly one manual field: `shade_pct`.** Solar radiation is the largest term in outdoor
heat stress and shade is the only thing that removes it — worth 5–8°F of WBGT on a clear August
afternoon here, which is more than most day-to-day temperature swings. The script reports the
session both ways, fully exposed and fully shaded, and `shade_pct` is what places it between them.
Rough is fine: 0, 50, 85. Presence beats precision, and it is never asked at all when there was no
sun to block. Everything else in the block is derived.

Treat `shade_pct` exactly like soreness and RPE — **never fill it in on the athlete's behalf.** It
propagates into `wbgt_f` and into the `--history` slope, so a guess does more damage here than a
guessed rating does, and it does it silently. Full guidance, the model, and its soft spots:
`rules/conditions.md`.

**Why one RPE and not one per session.** The frontmatter stays flat and one-glance fillable. Almost
every day has exactly one session that carries real load; doubles, meeting walks and trainer rides
don't need a rating, because they're deliberately below the threshold where RPE tells you anything.
If a day genuinely had two hard efforts, rate the harder one here and describe the other in the
body. The ladder wants a *trend*, and a trend survives that simplification fine.

`sleep_context` is the field that does the most work for the least typing. Suunto already knows the
night was fragmented; it cannot know whether that was a sick kid, a late flight, alcohol, illness,
or a bad strap. Those have completely different implications for the next day, and the plan will
read the number wrongly without the sentence.

## The scales, anchored

Unanchored 0–10 scales drift — a "5" in October is not a "5" in August unless the anchors are
written down. Use these.

**Soreness (0–10)** — muscular, on waking, before any warmup:

| Score | Anchor |
|---|---|
| 0 | Nothing |
| 1–3 | Noticeable on stairs or standing up; gone once warm. **Green** |
| 4–6 | Present through the warmup, changes how the first km feels. **Amber** |
| 7–8 | Alters gait, or makes you choose the flat route. **Red** |
| 9–10 | Sharp, localized, or getting worse day over day — this is an injury signal, not soreness. Stop and log it under Injuries in `athlete/profile.md` |

Sharp or one-sided beats high-and-symmetrical: 4 in one achilles matters more than 7 across both
quads after a long run.

**RPE (0–10)**, session-RPE for the whole session, rated after it settles:

| Score | Anchor |
|---|---|
| 1–2 | Recovery. Could have gone much further |
| 3 | Genuinely easy, full conversation |
| 4–5 | Steady. Talking in sentences, not paragraphs |
| 6–7 | Hard. Threshold-ish, a few words at a time |
| 8–9 | Very hard, counting down the reps |
| 10 | Maximal |

**Expected RPE by session type** — this is what "over plan" in the ladder's RPE-trend row means:

| `type` | Expected | If it comes in ≥2 higher |
|---|---|---|
| `recovery` | 2 | The easy days are not easy. This is the highest-value catch in the whole log |
| `easy`, `aerobic-base`, `walk` | 3 | Same |
| `night` | 4 | Check sleep debt before blaming fitness |
| `long`, `b2b`, `lap-sim` | 5 | Fueling first, then pace, then fatigue |
| `tempo` | 6 | Normal on a hot day; not normal twice |
| `intervals` | 7 | Trim volume, keep intensity (`rules/progression.md`) |
| `race` | — | Not rated |

`verify_plan.py` resolves the day's main session from `endurance/` by date and warns when logged
RPE runs ≥2 over the expected value for its type. Given the athlete's stated goal of getting
faster, and given that `athlete/zones.yml` calls easy-day creep his most likely training error,
**an `easy` day logged at 5 is a more useful finding than an interval session logged at 9.**

## Body — four standing prompts

A blank page gets skipped. Four prompts get answered in 30 seconds. Keep them in this order; they
run from most-frequently-informative to least.

```markdown
## How it felt

- **Legs:**
- **Feet:**
- **Gut:**
- **Head:**
```

Answer only what has something to say — "—" is a complete answer, and no answer at all is fine
too. But **feet gets its own line on purpose**, and it stays even on days there's nothing to
report. The meeting-time walking ramp is described in `rules/progression.md` as the single most
likely source of an overuse injury in this entire plan, going from 180 to 465 min/wk in nine weeks,
and plantar fascia and achilles problems announce themselves quietly for a week or two before they
stop the block. A hot spot written down three weeks early is worth more than anything else in this
file. Note the side.

**Gut** is a training variable here, not a comfort note (`rules/fueling.md`) — the open question of
the block is gel palatability past hour 15, and it gets answered by accumulating notes on long
runs, not by deciding in October. Record what was taken, what stopped being appealing, and when.

## What actually happened

```markdown
## Sessions

- **Planned:** [Easy + strides](../endurance/2026-08-04-easy-strides.md) — **done as written**
```

Status in plain words: **done as written**, **short** (say how much and why), **moved** (to when),
or **skipped** (why). The "why" is the entire value — a session cut for time is a scheduling fact
and changes nothing, while a session cut for legs is a fitness fact and may re-author the week.
Both look identical to the calendar; only the log can tell them apart.

## Unplanned sessions

Group road rides and eMTB spins are **never scheduled in advance** — they're recorded here after
the fact and the *remainder* of the week adapts (`training/block.md` § "Unplanned sessions",
`athlete/profile.md`).

```markdown
## Unplanned

- **Group road ride, ~2h, hard.** Treated as this week's second quality slot per
  training/block.md — Wednesday's session drops to easy aerobic.
```

Record what it was, roughly how hard, **and the adjustment it forces** — because the rule is that
a ride *replaces* a quality slot rather than adding to it. Neither counts against the running time
budget; a group ride absolutely counts against recovery, which is the whole reason it's logged.

Family hiking during the travel window (2026-08-22 to 09-01) belongs here too: log actual hours as
the trip goes, since those `endurance/*hiking-week.md` files carry estimates, and the return lands
four days before the Big Day (`training/block.md` § "Travel weeks", rule 7).

## Making the readiness call

The table in `rules/progression.md` proposes; you dispose. **Worst signal wins**, but record the
call you actually acted on, not the one the table computed — when they disagree, that disagreement
is the interesting part, and it's only visible later if both are written down.

Two things the table gets wrong often enough to name:

- **A single bad night after a hard day is expected**, not a red flag. It's the second and third
  night that mean something.
- **Fragmentation outranks duration.** The night of 2026-08-01 totalled 8h00 in seven pieces with
  HRV at 49; hours alone would have scored it green.

## Traps

- **Rating during the session instead of after.** Mid-session RPE tracks the hardest interval;
  session-RPE tracks the whole thing. Only the second one trends usefully. Rate it once it settles.
- **Logging the plan instead of the execution.** If the file says 60min and you ran 42, the log
  says 42. The plan is not the record — this repo already knows what was prescribed.
- **Backfilling a week on Sunday.** Soreness and RPE do not survive four days of memory; they
  regress toward "fine". A week of nulls is more useful than a week of remembered fours.
- **Editing a past entry to match how things turned out.** Append a correction with today's date
  instead. The wrong first reading of the 08-02 30k is worth keeping precisely because it was
  wrong — that's what invariant 8 exists to prevent repeating.
- **Treating a missing entry as a green day.** It isn't data. `verify_plan.py` skips nulls rather
  than assuming them.
