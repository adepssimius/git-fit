---
name: daily-brief
description: >
  Produce the athlete's morning training brief for the git-fit repo — pull Suunto sleep and
  recovery data, score it against the readiness ladder in rules/progression.md, present the day's
  prescribed session, and open the day's log entry. Use this whenever the user asks for a brief,
  a morning brief, a plan briefing, "what's on today", "what am I doing today", how their
  readiness or recovery looks, whether they should train today, or asks to pull their sleep data
  — and also when they ask what they're lifting today, how today's cardio and strength fit together,
  or any question that can only be answered by combining last night's wellness data with today's
  prescribed load. Covers both cardio and strength: the brief reports the day's data, judges
  readiness specifically against what today demands rather than in the abstract, and lays out the
  planned run and the planned lift. Prefer this over answering from memory or from a partial file
  read; the numbers change every night and the readiness call depends on all of them.
---

# Daily brief

The athlete is training for the Ghost Train 30-Hour Ultra (2026-10-17). Every morning he wants one
thing: **what am I doing today, and does last night say I should do it as written?**

The brief is trusted and acted on immediately, usually before coffee. That shapes everything below:
it has to be right, it has to be specific enough to execute without opening another file, and it
has to be honest about what it doesn't know.

## What to do

**1. Gather.** Run these together — the script and the two MCP calls are independent:

```bash
python3 .claude/skills/daily-brief/scripts/brief_context.py
```

```
mcp__suuntool__wellness_sleep    (limit ~8, order desc)
mcp__suuntool__wellness_recovery (limit ~4, order desc)
mcp__suuntool__workouts_list     (since_ms = 00:00 Monday of this block week)
```

`workouts_list` is for walking. Walks are logged as real activities — **`activityId: 0` is
WALKING**, and `11` is HIKING, which counts as time on feet in the trip weeks. Sum the walk
durations since Monday, then re-run the script with `--walked <minutes>` so it can do the
per-day arithmetic exactly rather than you estimating it:

```bash
python3 .claude/skills/daily-brief/scripts/brief_context.py --walked 60
```

The script gives you today's session with its full step list, today's lift parsed out of
`strength/program.liftoscript` with weights and active tiers, week-to-date running load, the week's
shape, recent log entries, and any repo problems worth mentioning. The MCP calls give you last night.

You should not need to open `program.liftoscript`, the week file, or the session file by hand — if
the script's output looks wrong or thin, that's a bug worth fixing in the script rather than working
around, because every future morning pays the same cost.

**Read `references/suunto-fields.md` before interpreting any wellness number.** Heart rate comes
back in Hz from the wellness endpoints and bpm from the workout endpoints, sleep is in seconds,
temperature is in Kelvin, and a fragmented night arrives as several separate items rather than one.
Getting this wrong produces a brief that is confidently wrong, which is worse than no brief.

**2. Score the readiness ladder** in `rules/progression.md`. Seven signals, worst one wins. Five come
from Suunto; soreness and RPE trend come from `log/`. Report each with its actual number, not just a
colour — "sleep 7h18, amber" tells him what to do differently tonight; "amber" doesn't.

**3. Write the brief** (shape below).

**4. Create `log/YYYY-MM-DD.md`** from `log/TEMPLATE.md` with the readiness call, `sleep_context` if
the night has an explanation, and `rpe_0_10: null` for him to fill in after training. Capturing the
call at the moment it's made is the entire point of the ladder — reconstructed-on-Sunday readiness
is worthless.

**Never invent `soreness_0_10` or `rpe_0_10`.** They're the two signals the watch cannot supply, and
`rules/logging.md` is emphatic that a blank is honest and a guessed number is corruption. If he
hasn't reported soreness, leave it null and ask for it at the end of the brief. Soreness is defined
as **on waking, before any warmup** — if he gives you a number later in the day, it belongs to
tomorrow's entry, not backfilled into a past one.

## Shape of the brief

Header: date, block week and what kind of week it is (down / build / peak / taper), days to race.
Then six sections, in this order. The order matters — it runs data → judgement → what to do.

### 1. The data

Last night and where he stands. A compact table with the actual readings, not just colours: sleep
duration and quality, HRV, resting HR, body resources, soreness. Add anything from the wellness pull
that's genuinely unusual — a deep-sleep collapse, a fragmented night, an HRV outlier — and say
whether it has an obvious cause.

Then one line of training context from the script's week-to-date section: what he's already done this
week, what today is, what's left. A 58min session reads differently as 17% of the week than it does
as the last thing before a rest day.

### 2. Readiness for *today's* load

This is the section that earns the brief. **Don't score readiness in the abstract — score it against
what today actually demands.** Amber before a 40min easy run and amber before a 4-hour night long run
are the same word and completely different situations.

State the ladder's call (worst signal wins, per `rules/progression.md`), then answer the question he's
actually asking: *given this session, does that change anything?* Be concrete about which way it cuts:

- Amber driven by sleep, before an easy day → proceed, the session is below the threshold where it matters.
- Amber driven by soreness, before a session that loads the sore tissue → that's the one to act on.
- Green before the block's biggest session → say so; it's permission, and he should know he has it.

`rules/progression.md` spells out what each colour does to lifts and to the day's session. If you're
recommending he run something as written despite an amber, justify it rather than letting it slide by.

### 3. Cardio

**Lead with what the session develops, in one or two sentences, before the step list.** A brief that
says what to run but not what it's for reduces him to executing instructions, and an athlete who
knows the purpose makes better decisions mid-session than one following a step list — he can tell
the difference between backing off because the session is wrong for today and backing off because
he's avoiding the hard part.

Take the purpose from the session's `intent:` field, `training/block.md`, and `athlete/profile.md`.
Do not invent physiology: if `intent:` only records provenance ("Champion week 7's version of..."),
say what the block-level reasoning supports and no more. Good sources for the *why*: block.md's
"flat rhythm specificity" argument, profile.md's "getting faster is a lever on hours-on-course",
and the session-type notes in `rules/endurance-authoring.md`.

Then session name, duration, distance, and the **full step list**, rendered so he can execute from
the brief without opening the file. Include the guide id if it's on the watch, and say plainly if it
isn't — an unpushed session is a problem he needs to know about before he's out the door.

Name the target instrument for each block (see the zone rule below). Add any meeting-time session
(trainer ride, walking) — it's free in time terms but real in recovery terms.

### 4. Strength

Same principle: say what the session is for before listing it. `rules/strength-authoring.md` and
`strength/notes.md` carry the reasoning — Lower B is runner-specific durability rather than
strength, the single-leg calf raise is called the highest-value accessory in the program for
ultra durability, Nordics produce outsized DOMS for the stimulus. That context is what makes the
difference between him cutting the right exercise and the wrong one on a bad day.

The script prints today's lift straight from `strength/program.liftoscript`, with exercises, active
set-variation, weight and rest. Give it as a table he can train from.

Two things worth surfacing rather than just listing: **the active tier**, because that's the dial the
readiness ladder actually turns — on amber, main lifts drop a tier, so name what that would mean
today; and **any interaction with the cardio**, since `rules/strength-authoring.md` cares a lot about
what sits next to what. Lower B on the same day as a run stacks calf and achilles load, and that's
worth a sentence when soreness is already amber.

If the script says there's no lift today, say whether that's the template (Wed/Fri/Sat are clean by
design) or a deliberate gap in that Liftoscript week (taper, mid-cycle rest, Big Day week). "No lift"
and "no lift, and that's intentional because it's peak running week" are different messages.

### 5. Walking

Walking is the third training modality here, not an afterthought — `training/block.md` calls
meeting-time walking the primary answer to the time-on-feet problem, and it scales from 180 to 465
min/week across the block.

The target is stored weekly (one `meeting-walk-week.md` per block week) but executed daily, so the
number he actually needs is **how many minutes today**. The script computes it: target, done so far,
and the per-day rate required across the days left. Give him that rate plainly.

**Walking happens on working days only** — it's done during work calls. So the target divides across
Mon–Fri minus holidays, not across seven days, and the script handles that (see `athlete/profile.md`
§ Working days for the holiday list and the athlete's own observance rule). This is not a rounding
detail: block week 14 contains Labor Day, so its 355min target falls on four days at 89min/day
rather than the 51min/day a naive 7-day split would report. Quote the working-day figure; a 7-day
number is wrong in a way that reads as reassuring.

Pace is measured in working days too. Mid-week, compare against the working days elapsed — on a
Wednesday that's 2 of 5, not 2 of 7.

Flag it when he's behind pace, and say why it matters rather than just noting the gap: the risk isn't
missing the weekly total, it's making it up with two huge days at the end of the week.
`rules/progression.md` names this ramp as the block's single most likely source of an overuse injury,
so a spike is worse than a shortfall. If he's far enough behind that catching up would mean a spike,
say the honest thing — miss the target.

The ramp figure the script prints is **total time on feet, walking plus hiking**, matching
`verify_plan.py`. Don't recompute it from the walk target alone; in weeks with family hiking that
produces a large false alarm.

### 6. Watching, and housekeeping

Only genuinely new signals — not a recap of section 1. And only mention repo state when the script
surfaced something. Silent on a clean repo.

## Things that will make the brief wrong

These are all real failures from real mornings. They share a shape: the brief sounded authoritative
while quietly not matching the underlying files.

**Never write a bare zone. Ever. Qualify every single one.** Write `ZS Z2`, `HR Z2`, `Pace Z2` —
never `Z2`, never `Zone 2`, never `zone 2`. This repo runs three zone systems that share numbering
and mean completely different intensities:

| | what it is |
|---|---|
| `ZS Z1/Z2/Z3` | ZoneSense (DFA a1). Z1 below aerobic threshold, Z2 between AeT and AnT, Z3 above AnT |
| `HR Z1–Z5` | Friel LTHR bands in `athlete/zones.yml`. HR Z2 is 138–151bpm, easy aerobic |
| `Pace Z2` | the `Z2 Pace` step syntax in `rules/endurance-authoring.md` |

**ZS Z2 is hard — its ceiling is threshold. HR Z2 is easy aerobic.** Same numeral, opposite
sessions. That's the whole reason this rule exists.

This is not satisfied by qualifying the first mention and abbreviating afterwards. The failure mode
in practice is exactly that: writing "ZoneSense Zone 2" once and then "Z2", "mid-zone", "high-Z2",
"drifting into Z3" for the rest of the message. Every one of those needs its prefix, because the
athlete reads them mid-run on a watch screen where there is no earlier sentence to refer back to.
Applies to the brief, to chat, and to anything written into a session file's `follow:`.

**Describe blocks the way the session file describes them.** If the body says `3km 6:30/km Pace`,
call it "the 3km at 6:30", not "the 20-minute block" — he'd have to do arithmetic to find out which
block you meant. Adding the computed duration alongside is helpful; replacing the file's own units
with it is not.

**Respect the athlete's baselines.** `athlete/profile.md` records what is routine for him —
gastroc/soleus soreness in the green band is normal and not a signal. Flagging it as an emerging
pattern trains him to ignore the brief. Arch and plantar soreness is the opposite: it's the early
warning for the walking ramp (`rules/progression.md` calls that the block's most likely overuse
injury) and is worth naming every time it appears, including which foot.

**Suunto data is DRAFT until he confirms it** (`AGENTS.md` invariant 8). The numbers are real, the
interpretation usually isn't obvious. A fragmented night could be a sick kid or a loose strap; a
hard-looking session could contain a deliberate effort. Present the reading and your interpretation
as separable, so he can correct the second without arguing with the first. Two corrections in this
repo's history came from exactly that.

**Don't pad.** He reads this every morning. A brief that recaps what he already knows is one he
starts skimming, and then he skims the morning something actually matters. If a section has nothing
new, drop it.

## When there's no session today

Rest days are prescribed, not gaps — `training/block.md` requires a full leg-recovery day before
the Saturday long run, and the week file will say so. Check the week file row before calling a day
empty: a planned rest day and a missing file look identical from the endurance directory. Still
report readiness; a rest day is exactly when a red signal changes what tomorrow should look like.
