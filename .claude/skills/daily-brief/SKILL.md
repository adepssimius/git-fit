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

**1. Gather.** Run the script first — it prints the `since_ms` for every pull:

```bash
python3 .claude/skills/daily-brief/scripts/brief_context.py
```

Then pull, using **the script's `since_ms`, not a window of your own choosing**:

```
mcp__suuntool__wellness_sleep    (limit ~8, order desc)
mcp__suuntool__wellness_recovery (limit ~4, order desc)
mcp__suuntool__workouts_list     (since_ms from the script's "Data pulls" section)
mcp__liftosaur__get_history      (startDate from the same section)
```

**Never narrow a pull to the window that suits one question.** This rule was written the
morning it failed: the 2026-08-10 brief scoped `workouts_list` to "since Monday" because that
was all the walking count needed, and missed a **110min eMTB ride from the previous Saturday**
that no file in the repo recorded — plus the fact that the prior week's walking had come in at
97min against a planned 180. Both were sitting one day outside the window. The watermarks in
`state/pull-watermarks.yml` exist so the window is chosen by what has already been read, not
by today's question; over-pulling is free, under-pulling loses sessions permanently.

**After the pulls succeed**, stamp the watermark:

```bash
python3 .claude/skills/daily-brief/scripts/brief_context.py --record-pull
```

**Reconcile what came back against `log/`.** Anything the watch has that the repo doesn't is a
real session that never got recorded — an unplanned ride, a walk, a lift. Say so in the brief
and write it into the right day's log entry. `rules/progression.md` requires an unplanned ride
to adjust the *rest of that week* immediately, so a late discovery is worth flagging as late.

`workouts_list` is also how walking is counted. Walks are logged as real activities —
**`activityId: 0` is WALKING**, `11` is HIKING (time on feet in trip weeks), and `105` is
E_BIKING (not time on feet, but real load). Sum the walk durations since Monday, then re-run
the script with `--walked <minutes>` so it can do the per-day arithmetic exactly rather than
you estimating it:

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

**If yesterday's session was outdoors, get the conditions before judging how hard it was.** The
watch's temperature field is body heat off the wrist, not ambient — save the workout JSON and run
it through the tool, which decodes the GPS track and returns the real temperature, humidity and
solar load, in full sun and in full shade:

```bash
python3 scripts/heat_load.py --workout-json <workout.json> --write   # rules/conditions.md
```

This matters for the brief specifically because **ZoneSense self-corrects for heat**, so a
depressed aerobic threshold or an HR that looks high for the pace is the expected reading on a hot
day rather than a fitness signal. Reporting yesterday's session as harder-than-planned without the
ambient number is how the 08-02 30k got read as chronic mis-pacing. If it prompts for `shade_pct`,
ask the athlete in the brief — it is a one-word answer and the only field he owes it.

**2. Score the readiness ladder** in `rules/progression.md`. Seven signals, worst one wins. Five come
from Suunto; soreness and RPE trend come from `log/`. Report each with its actual number, not just a
colour — "sleep 7h18" next to an amber tells him what to do differently tonight; amber alone doesn't.
The number goes in the table's Reading cell and the colour in its Status cell (section 1 below, which
also says how to write the colour in Discord versus everywhere else).

**3. Write the brief** (shape below).

**4. Create `log/YYYY-MM-DD.md`** from `log/TEMPLATE.md` with the readiness call, `sleep_context` if
the night has an explanation, and `rpe_0_10: null` for him to fill in after training. Capturing the
call at the moment it's made is the entire point of the ladder — reconstructed-on-Sunday readiness
is worthless.

**Never invent `soreness_0_10` or `rpe_0_10`.** They're the two signals the watch cannot supply, and
`rules/logging.md` is emphatic that a blank is honest and a guessed number is corruption. If he
hasn't reported soreness, leave it null and ask for it at the end of the brief — and when he answers,
step 5 applies. Soreness is defined
as **on waking, before any warmup** — if he gives you a number later in the day, it belongs to
tomorrow's entry, not backfilled into a past one.

**5. When he answers, write it into the log entry, then offer to save it.** Added 2026-10-03: he gave
soreness in reply to the brief, the brief moved on, and the number was never persisted — the one
signal the watch cannot supply, lost. So:

- **Any rating he gives in reply to the brief goes into today's entry straight away** — soreness, a
  sleep answer for `sleep_context`, `shade_pct`. A poll vote counts the same as a typed answer. If it
  changes a row in the readiness table (a `—` soreness becoming a 4), update `readiness:` in the
  frontmatter and say in one line whether the call moved.
- **Then end with a one-line offer to save the log**, e.g. *"Soreness 4 is in `log/2026-10-03.md` —
  want me to save it?"* From the fitcordllm bot, saving means its `ship` tool (a thread's edits sit
  in that thread's clone and never reach `master` until shipped); in a local session it means a
  commit. **Offer, don't do it** — `AGENTS.md`'s standing instruction applies here as everywhere:
  he says yes, then it ships.
- **Offer at the end of the brief too**, once the readiness signals are in, rather than only after a
  follow-up — the entry with the readiness call is already worth keeping. One offer per brief, not
  one per answer; a later answer just goes into the same unsaved entry.

## Shape of the brief

Header: date, block week and what kind of week it is (down / build / peak / taper), days to race.
Then six sections, in this order. The order matters — it runs data → judgement → what to do.

### 1. The data

Last night and where he stands. A compact table with the actual readings, not just colours: sleep
duration and quality, HRV, resting HR, body resources, soreness, RPE trend. Add anything from the
wellness pull that's genuinely unusual — a deep-sleep collapse, a fragmented night, an HRV outlier —
and say whether it has an obvious cause.

**The table has exactly this shape** (athlete, 2026-10-03; shown as it is written for Discord):

| Signal | Reading | Status |
|---|---|---|
| Sleep duration | 7h14, one unbroken block (00:59-08:13) | 🟡 |
| Sleep quality | 0.79, deep 1h21 (19%) | 🟢 |
| HRV | 95 ms, 83 samples — week high | 🟢 |
| Resting HR | 41 bpm, on a 40-41 baseline | 🟢 |
| Body resources | 0.87 at 08:30, climbing all morning | 🟢 |
| Soreness | 4 on waking, up from 3 | 🟡 |
| RPE trend | lap sim 4 vs 5 expected; ride 6 vs 6 | 🟢 |

Overall 🟡 — worst signal wins, and today that's the soreness, not the sleep.

**How the Status colour is written depends on where the brief is read — the emoji are Discord-only.**
(Athlete, 2026-10-03: *"those style edits only apply when you are called from the context of
discord."*) You are in Discord when the session was started by the fitcordllm bot: its system
prompt says so, and your replies are posted to a Discord channel.

| context | Status cell | overall line |
|---|---|---|
| **Discord (fitcordllm)** | a literal 🟢 / 🟡 / 🔴, nothing else | "Overall 🟡 — …" |
| **anywhere else** (terminal, desktop app, cloud session) | the plain word: green / amber / red | "Overall amber — …" |

In Discord specifically:

- **Never write the bare words GREEN / AMBER / RED in the Status cell.** They do not render as
  coloured dots for him. The bot's own formatting note claims it draws dots from those words; his
  client disagrees, and his client is what he reads. He confirmed the emoji do render.
- **No emoji on the signal names.** An earlier draft put 😴 💓 🔋 on each signal and he rejected
  it: *"Not emoji for the things themselves, red/yellow/green lights."*

Everything else about the table applies in every context:

- **Numbers and qualifiers go in Reading, never in Status.** Status is the colour alone, so the
  column scans in one glance; Reading is where "sleep 7h14" tells him what to do differently tonight.
- **All seven ladder signals get a row, every morning.** A signal with no number still gets its row,
  Reading saying so ("no sleep record came through") and Status `—`. A dropped row hides a question
  he needs to be asked — see "When a ladder signal is missing" below.
- **Follow the table with a one-line overall call naming which signal drives it**, as above. "Overall
  amber" alone leaves him hunting the table for the reason; the driving signal is what section 2 acts on.

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

**Every brief carries a two-row table of today and tomorrow** (athlete, 2026-10-03 — that morning's
brief gave today only and he had to ask for it):

| Day | Session | Duration | Instrument | Watch |
|---|---|---|---|---|
| Sat 10-03 | Downhill quad bouts — no file, his call on reps | not set | effort | n/a |
| Sun 10-04 | Sunday Back-to-Back — last real volume of the block | 105min | `ZS Z1` | `94zy82s9` |

**Why tomorrow too:** on a weekend the two days are one decision — what he does today sets what
tomorrow's session lands on — and on any other day it is the line that tells him whether today's
amber matters. **A day with no prescribed file still gets its row, saying so** (rest day, his call,
no file) rather than being dropped; check the week file before deciding which it is (see "When
there's no session today"). Instrument follows the session's `follow:` and is always qualified
(`ZS Z1`, never `Z1`), per the zone rule below. Watch is the guide id, or "not pushed" — which is
worth saying in the same breath, per the paragraph below.

The table is the overview; the rest of this section is today's session in full.

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

**Strength is best-effort and running has priority** (`athlete/profile.md` § "Priority when time is
short", athlete-confirmed 2026-08-12). The athlete is time constrained; lifting is the first thing
cut when a day compresses. So **a missed lift is an expected outcome, not an adherence failure.**
Reconcile it against Liftosaur as always and write it into `log/`, but do not open the brief with a
tally of missed lifts, do not escalate a run of them into a re-author question, and do not propose
shrinking the program to what will reliably get done. The 08-12 brief did all three and had to be
corrected. Note the miss in one line, then spend the section on what today's lift actually is.

### 5. Walking — NOT a brief section any more (2026-10-02)

**Athlete, 2026-10-02:** *"I haven't really been following your walking plan. The goals you had were
more just for my reference to motivate me to take meetings while walking instead of sitting."*

**So the walking targets are a nudge, not a prescription, and were never a plan he was executing.**
`training/block.md` had already half-noticed this on 09-15, calling the target *"aspirational for
weeks."*

**What that means for the brief, concretely:**

| don't | because |
|---|---|
| compute a per-day rate | there is no commitment to pace against |
| say he is "behind pace" or "0 of 120" | he walks more than the watch records, and he never signed up for the number |
| derive a ramp % from recorded walks | both sides are undercounts of unknown size |
| give walking a section at all | it is the brief's own rule — a section that recaps what he knows trains him to skim |

**And a second, independent reason the numbers do not work:** *"It's not feasible for me to start a
session on my watch every time I go for a walk."* **`WALKING` activities are a floor.** See
`rules/progression.md` § Walking ramp.

**Mention walking only when:** he raises it himself, or a single recorded walk is unusually long
(a real spike, which he would record). **Otherwise say nothing.**

**The nudge itself is still worth keeping alive** — taking a call walking instead of sitting is free
and it is the whole point. **Encouragement, not accounting.**

**Nothing was lost by him not following it**, and the brief should not imply otherwise. The
durability question walking was meant to support was answered directly by running: 50.31 km in 7h14
on 09-12 with *"my feet are fine with zero checks and zero sock changes"*
(`training/block.md` § Meeting walking).

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
pattern trains him to ignore the brief.

**Arch and plantar soreness: NEVER RAISE IT FIRST (2026-10-02).** *"I don't typically have arch or
plantar soreness, even after 6 or 7 hour hikes with real elevation and rocky/uneven terrain."* So it
is a baseline non-event, and warning about it is the same error as flagging green-band calf soreness.
**But name it immediately if HE reports it** — a symptom with no history is high-signal exactly
because it never fires. Report, including which foot; never pre-empt.

**The session clock is UTC. It is not the athlete's date, and after 20:00 Eastern it is not even
the right day.** Added 2026-09-19 after a brief written on Saturday evening was dated Sunday,
opened `log/2026-09-20.md`, and reported a missing sleep record for a night he had not had yet.
His answer: *"It's not the next day yet so there's no sleep. It's still Saturday."*

**The date on `brief_context.py`'s first line is the only date that counts.** It reads
`timezone:` from `athlete/profile.md` and it is what the log entry, the session lookup and the
readiness call all key off. The harness's own "today's date" notice, `date`, and anything else
reading the container clock are five hours ahead of him half the day.

The script prints a loud `!!` banner whenever the two disagree, and `verify_plan.py` hard-errors
on a `log/` entry dated past the athlete's today. **If either fires, the date is the bug** —
do not reason about the data until it is right.

**A related trap: the newest sleep record is supposed to be missing in the evening.** He has not
slept yet. "No sleep record for last night" only means something in the morning.

**When a ladder signal is missing, ask him. Do not score the ones that are left and call it a
readiness call.** Added 2026-09-19 after the brief did exactly that. Four of seven signals were
missing — no sleep record for the second night running, so duration, quality, HRV and resting HR
were all absent. The brief scored the one remaining Suunto number (body resources, 0.34) as red,
opened on **"Readiness: RED"**, wrote `readiness: red` into the log's frontmatter, and recommended
cutting the 110min long run to 85. He had slept well. His answer: *"I'm not cutting anything. I had
a great night of sleep. You need to ask instead of making assumptions when there is data missing."*

The brief did label the inference DRAFT in the body — and that changed nothing, because the
frontmatter and the recommendation had already committed to it. **A draft reading that drives a
recommendation is not a draft.** So:

- **Missing signals are a question, not a gap to reason across.** "No sleep record came through —
  how did you actually sleep?" is one line and it settles the whole ladder. Ask it *before* the
  readiness call, not after the recommendation. In the table the signal keeps its row with Status
  `—`; it is never coloured from an inference.
- **One surviving signal is not a ladder.** Worst-signal-wins assumes the signals are there. With
  most of them missing, a single number is a data point, not a verdict — report it and say what it
  would mean if confirmed.
- **A signal whose source is known to be broken should not be scored at all.** The same watch was
  failing to write sleep records; the overnight resources curve comes from the same data and was
  failing the same way. Two failures with one cause.
- **Never recommend cutting a session on inferred data.** If the inference is worth acting on, it
  is worth one question first. He reads this before coffee and acts on it.

**Suunto data is DRAFT until he confirms it** (`AGENTS.md` invariant 8). The numbers are real, the
interpretation usually isn't obvious. A fragmented night could be a sick kid or a loose strap; a
hard-looking session could contain a deliberate effort. Present the reading and your interpretation
as separable, so he can correct the second without arguing with the first. Two corrections in this
repo's history came from exactly that.

**Don't pad.** He reads this every morning. A brief that recaps what he already knows is one he
starts skimming, and then he skims the morning something actually matters. If a section has nothing
new, drop it. **Two things are never padding and never dropped:** the seven-row readiness table
(section 1) and the today/tomorrow table (section 3). Their value is that they are the same shape
every morning.

## When there's no session today

Rest days are prescribed, not gaps — `training/block.md` requires a full leg-recovery day before
the Saturday long run, and the week file will say so. Check the week file row before calling a day
empty: a planned rest day and a missing file look identical from the endurance directory. Still
report readiness, and still give today its row in the today/tomorrow table, saying which it is; a
rest day is exactly when a red signal changes what tomorrow should look like.
