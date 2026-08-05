---
name: daily-brief
description: >
  Produce the athlete's morning training brief for the git-fit repo — pull Suunto sleep and
  recovery data, score it against the readiness ladder in rules/progression.md, present the day's
  prescribed session, and open the day's log entry. Use this whenever the user asks for a brief,
  a morning brief, a plan briefing, "what's on today", "what am I doing today", how their
  readiness or recovery looks, whether they should train today, or asks to pull their sleep data
  — and also when they ask a question that can only be answered by combining last night's wellness
  data with today's prescribed session. Prefer this over answering from memory or from a partial
  file read; the numbers change every night and the readiness call depends on all of them.
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
mcp__suuntool__wellness_sleep   (limit ~8, order desc)
mcp__suuntool__wellness_recovery (limit ~4, order desc)
```

The script gives you today's session with its full step list, the week's shape, recent log entries,
and any repo problems worth mentioning. The MCP calls give you last night.

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

Date, block week, days to race. Then:

**Readiness** — a small table: signal, actual reading, colour. Then the call, and one sentence on
what actually drove it. If a signal is amber for a reason that isn't fitness — a late run pushing
sleep onset, a sick kid — say so, because the number alone will read as a warning it isn't.

**Today** — session name, duration, distance, and the step list rendered so it can be run from the
brief alone. Include the guide id if it's on the watch, and say plainly if it isn't. Note the lift
(the week file's day row, and Liftoscript week = block week − 8) and any meeting-time session.

**The call** — does the ladder change the plan? Say so explicitly and give the reason. Amber usually
means proceed; `rules/progression.md` spells out what each colour does to lifts and to the day's
session. If you're recommending running it as written despite an amber, justify that rather than
letting it pass silently.

**Watching** — only genuinely new signals. Not a recap.

**Housekeeping** — only when the script surfaced something. Silent on a clean repo.

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
