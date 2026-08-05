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

Session name, duration, distance, and the **full step list**, rendered so he can execute from the
brief without opening the file. Include the guide id if it's on the watch, and say plainly if it
isn't — an unpushed session is a problem he needs to know about before he's out the door.

Name the target instrument for each block (see the zone rule below). Add any meeting-time session
(trainer ride, walking) — it's free in time terms but real in recovery terms.

### 4. Strength

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

**Name the instrument whenever you say a zone.** "Zone 2" is ambiguous in this repo and the two
meanings are far apart: **ZoneSense Zone 2** runs from the aerobic to the anaerobic threshold — its
ceiling *is* threshold, it is hard — while **HR Zone 2** is 138–151 bpm, easy aerobic. They share a
number and nothing else. Always write `ZoneSense Z2` or `HR Z2`. This applies to the brief and to
anything you write into a session file.

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
