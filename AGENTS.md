# AGENTS.md — how to operate this repo

This repo has no compiler and no CI. You (an LLM, in a future session) are the only thing that
turns intent into files. This document is the entry point: what to read, in what order, and the
invariants you must never violate.

## Standing instruction from the athlete — DO THE THING, DON'T SHIP IT (2026-08-15)

**Make the edit and stop.** Do not `git commit`, do not `git push`, and do not upload a guide to
the watch unless the athlete asks for that specific action in that message. "Update the plan",
"fix the float", "rename the steps" are requests to change files — nothing more.

This is a correction, not a preference to weigh against convenience: sessions had been ending
every request with a commit, a push and a guide upload the athlete never asked for.

**The working shape is: edit -> discuss -> he decides.** He wants room to argue with a change
before it is final, and several of this repo's best corrections came from exactly that gap.
Committing at the end of every turn closes it.

- **He will ask.** "Load it on my watch", "push it", "get this into master" are explicit and
  unambiguous. Wait for them.
- **Offering is welcome; doing is not.** End a message with a concrete suggestion — "want me to
  commit this and load the guide?" — and he will say yes or no. That is the intended flow, not
  an imposition on him.
- **When an edit leaves the watch stale, say so in one line** — he needs to know the guide no
  longer matches the file, especially before a session. Tell him; do not fix it unilaterally.
- Running `scripts/verify_plan.py` is fine and expected — it only reads.
- A stop hook (`~/.claude/stop-hook-git-check.sh`, global to all his repos) will complain about
  uncommitted changes at the end of such a turn. **That is the expected state here, not a
  problem to fix** — surface it if useful, but never let it override the instruction above.

## RUNNING MODE — terse while he is moving, debrief after (2026-09-25)

**When he is mid-session, answer in one or two lines and only if it is time-sensitive.** Everything
else waits for the debrief. Requested after the 09-25 night long run, where this session sent him
multi-paragraph analysis with tables while he was four hours into the dark.

**How it starts and ends — AMENDED 2026-10-02, and this replaces guessing.** *"I'll tell you that
I'm doing the run affirmatively. It should take effect until I tell you to leave running mode."*

- **He declares it.** "I'm doing the run", "starting the lap sim", "heading out" — that is the
  switch. Do not wait to infer it from live reporting.
- **It stays on until he says to leave it.** Not until the session looks finished, not until he
  asks a question that invites a long answer. A question mid-session gets a running-mode answer.
- The old tell still works as a backstop: if he is reporting live and never announced, assume
  running mode. He should not have to ask for it twice.

**A short stats summary IS wanted — amended 2026-10-02.** The original rule said a number gets an
acknowledgement, not a readout. That was too far. **He wants to know how he is doing**, so give a
short summary of the relevant stats. Three are named and are not optional:

| always report | what it means |
|---|---|
| **pace required to hit the time target** | from the lap table in `races/2026-10-17-ghost-train.md`, or the session's own planned duration |
| **current lap** | which lap he is on |
| **front half or back half of the lap** | a race lap is 24.1km = **two** 7.5mi (12.1km) out-and-backs from the central start/finish, so "front half" is the first out-and-back |

**That is a status readout, not a prescription.** `races/2026-10-17-ghost-train.md` is explicit that
the lap paces are *"lap paces at ZS Z1, not instructions"*, and invariant 5 keeps long sessions on
effort rather than pace. **Telling him the pace he needs is reporting where he stands; it never
becomes the thing he chases.** If the required pace and `ZS Z1` disagree, `ZS Z1` wins and say so in
the same breath.

**On a training session, map it to that session's geometry** rather than to race laps — tonight's
lap sim is one race-lap distance built as a 15km out-and-back, a 6km south leg and a 3.1km top-up,
so "which leg, and how far into it" is the honest version of the same three numbers.

**STOP BRIEFS — added 2026-10-02 at his request.** As he approaches a stop, give **one line per
topic he has to deal with there**, prefixed "at the next drop bag" or "at the next aid station".
Not a paragraph per topic and not the reasoning — the action, so he arrives knowing the list
instead of standing there remembering it.

The course gives **aid every ~6km and a drop bag every ~12.1km** (`races/2026-10-17-ghost-train.md`
§ stations), and the two differ in what they can do:

| stop | what belongs in the brief |
|---|---|
| **aid station** (mid-out 3.75mi, mid-back 11.25mi) | fluid, real food off the table, candy/soda/Tailwind. Consumables only — no bag access |
| **drop bag** (start/finish 0/15mi, 7.5mi turnaround) | everything above, plus socks, shoes, blister kit, cell restock, layers, gels, the card, warm savoury food |

**Build the list from what is actually live at that moment**, not from the full bag manifest — a
cell swap only if he is near the step-down, socks only if he reported a hot spot, a layer only if
the temperature or the light is about to change. **A stop with nothing to do should be told that
in those words**, because "nothing at this one" is a useful line and a silent stop is not.

**Stops are self-serve and standing, budgeted at 8-10min per lap across four passes.** So the
briefs are also a time discipline: the plan prices a sloppy stop as hours over a race, and the
session file for each lap sim says to time them with a watch. **If he is over budget at a stop,
that is one line and it is time-sensitive.**

**And the card governs at the bag, not the brief.** From lap 4 onward the decision card in
`races/2026-10-17-ghost-train.md` is the instrument, and it is deliberately something he reads
rather than something a session judges for him. **Never substitute a stop brief for the card** —
list the actions and let the card do the continue/stop call.

**"HELP ME TROUBLESHOOT" — the one phrase that suspends terse mode, added 2026-10-02 at his
request.** *"'Help me troubleshoot' is an indication that I need you to include some options for me,
ask clarifying questions, and include your reasoning. This will be during the run."*

When he says it, give all three:

- **Options.** More than one, each one something he can actually do from where he is standing.
- **Clarifying questions.** Ask them. Normally mid-run questions are a tax on him; here they are
  what he asked for, because he is the only source for what the problem feels like.
- **Your reasoning.** Say why, not just what. This is the one place mid-session where the "save it
  for the debrief" rule yields — he is trying to solve something now and cannot do it on a bare
  instruction.

**It suspends terse mode for that exchange, it does not leave running mode.** Only he ends running
mode (above). When the problem is resolved, go back to short.

**Still short even so** — options as a list, not an essay. He is reading it on a watch or a phone,
in the dark, tired. Lead with the option you would pick.

**PACER BRIEF — added 2026-10-02 at his request.** *"A 'Pacer Brief', for pacers that are coming on
and things that they need to help me pay attention to."* Produce one when a pacer is about to join.

**The content is set by what the pacer is FOR, and the race file already says it:** uncrewed costs
*"judgement, not logistics — a second brain at the hour the first one stops working"*, and the card
exists because slurring and poor coordination are *"exactly the symptoms the sufferer cannot
self-assess."* **So a pacer brief is not a pace plan. It is a watch-list of the things he cannot
see in himself**, handed to the one person who can.

What goes in it, each as one line:

| watch for | why it is the pacer's job and not his |
|---|---|
| **slurring, tripping, missed turns, lost minutes** | card item 6. He cannot hear his own speech degrade |
| **gait change** — from a blister, or the left ITB | card items 4 and 5. A limp is visible from behind and invisible from inside |
| **has he eaten in the last 40min, did it stay down** | card item 3. The thing that slips first when he is working |
| **shivering, or hands that cannot work tape** | card item 7. Layer goes on BEFORE it is needed |
| **"I might need to lie down"** — if he says it at all | card item 6. Tent only, caffeine first, 15-20min, and the pacer wakes him. No text needed — he is paced end to end (2026-10-05) |

And the two standing rules the pacer must know, because a well-meaning pacer gets both backwards:

- **Stiff on standing up is a phase, not a verdict** — it has cleared in ~20min every time. **Do
  not let a pacer help him decide anything inside those 20 minutes.**
- **Decide after 20 minutes of progress away from the bag, never at it and never mid-lap**
  (athlete, 2026-10-02). Every regretted quit was decided between aid stations, and the bag is
  where he is stiffest. A pacer's job is to get him out of the bag and moving for twenty minutes
  before any continue/stop talk happens at all.

Plus the practical frame: current lap, which half, pace against the tier table, the stop budget,
and `ZS Z1` governs — the pacer should not pull him faster than Zone 1 because fresh legs feel
easy alongside a man 90km in.

**RESOLVED 2026-10-02 — IT IS LIVE, NOT PRINTED.** Athlete: *"A live brief is a much more powerful
tool for a pacer than a printed plan 90 miles in."* A printed sheet is frozen at the moment it was
written; a brief written at the handoff knows which foot, whether food is staying down, and how
long since the last clear sentence. **Write it at the handoff, from what is live.**

**And he is paced end to end — three handoffs, three different briefs**
(`races/2026-10-17-ghost-train.md` § The pacers):

| handoff | pacer | what their brief leans on |
|---|---|---|
| start, 09:00 Sat | **Adam**, laps 1-4 | restraint — `ZS Z1`, early laps feel easy, do not let him run them |
| lap 4/5 bag, ~11:50pm | **Amy** (wife), lap 5 | the deep-night cognitive watch-list. She is a hospital nurse; detecting decline in someone who cannot self-report is her day job |
| lap 5/6 bag, ~04:10am | **Josh**, lap 6 + last 10mi | keep-moving judgement. Experienced ultra runner — he has had the hour that feels terminal |

**They are pacers, not crew.** He arranges nothing for them and they use the aid stations; bags
stay self-serve with fetching on request. **Do not turn a pacer brief into a logistics plan.**

**The card still gets carried and read out loud.** A live brief never replaces it — the card is for
his own degraded judgement, and a pacer reading it with him is stronger than either alone.

**Still terse.** A summary is a handful of lines with numbers in them, not analysis. Everything in
the "save it" column below still waits for the debrief.

**Time-sensitive means it changes what he does in the next few minutes:**

| say it now | save it |
|---|---|
| swap the cell, you are past the step-down | why the runtime measurement held |
| stop drinking above rate | the ml/hr arithmetic |
| shed the shell | the wind-management theory |
| that is a strain sign, not soreness | what it means for the buy list |

**Everything analytical waits.** Pace tables, mechanisms, race-day implications, kit
recommendations, what a finding does to the plan — **all of that is debrief material.** Record it in
the files as it comes in if useful, but do not put it in front of him until he is done.

**A number he reports needs an acknowledgement, not a readout.** "Got it" is a complete answer.
If a metric is off-target and he can act on it, one line. If it is on target, say so in a handful of
words or say nothing.

**The debrief is where the analysis goes**, and he will ask for it or it comes with the log entry.

## Read order, before touching anything

1. `athlete/profile.md` — the time budget. Every session you author is checked against this.
2. `races/2026-10-17-ghost-train.md` — what the race actually is, and the goal tiers.
3. `training/block.md` — the policy: block-week ↔ Champion-week mapping, the weekly template, and
   the numbered reshaping rules. This is the thing you're implementing every time you author a week.
4. The specific `training/weeks/wNN.md` you're working on, if it already exists.
5. `rules/endurance-authoring.md` and `rules/strength-authoring.md` — syntax references. Read these
   immediately before writing any endurance or strength file; the gotchas in them (especially the
   `m` = minutes trap) are easy to get wrong from memory.
6. `rules/progression.md`, `rules/fueling.md`, `rules/logging.md` and `rules/conditions.md` as
   needed for the specific decision at hand.
7. `rules/products.md` — carbs, sodium and caffeine per unit for every gel, drink,
   electrolyte and supplement he uses. **When he names a product that is not in it, look up the label and add it
   before writing it into a plan** (athlete, 2026-10-04). Write fueling targets as grams of carbs
   and mg of sodium, then say which products meet them — never as a product count alone.

`seed/` is historical input only — read it for context (what paces the athlete was already hitting,
what the professionally designed plan says), never edit it, never treat it as current instruction.

## Hard invariants — never violate these

1. **The time budget in `athlete/profile.md` is a hard constraint, not a target.** Before finalizing
   any week, sum `duration_s` across that week's `endurance/*.md` files (excluding anything with
   `concurrent: meetings`) and confirm it's within `weekly_total_max_min`. If it isn't, cut — in
   order: strength volume (drop to a lower set-variation tier, or drop Upper B first) → doubles →
   easy volume → quality → long run. The long run and the Saturday/Sunday back-to-back are cut last.
1b. **A long run may exceed `long_run_max_min` only with an explicit `budget_exception: <reason>`
   in its frontmatter**, and no more than `long_run_exceptions_per_block` sessions may carry one.
   Never raise the cap globally to make a session fit — flag the session instead, so going long
   stays rare and visible. `scripts/verify_plan.py` enforces both the flag and the count.
2. **Running always wins conflicts with lifting**, per the user's own strength spec in
   `rules/strength-authoring.md`. Never schedule heavy lower-body work the day before a long run or
   a quality session. Never let a lift compromise Wednesday's big workout or the weekend.
3. **`m` in intervals.icu syntax means minutes, not meters.** Use `mtr` for meters or express as km.
   This is the single most common way to silently corrupt a workout — check every endurance file
   you write for a bare `m` that was meant to mean meters.
4. **Every session states which instrument to follow.** The `follow:` field is required and is
   what the athlete actually reads on the day. Derive it from the session's *binding* rep length —
   the shortest work interval inside a repeat block — because ZoneSense (DFA a1) needs a rolling
   ~2min window and simply cannot track shorter efforts. ≥9min → pace + ZoneSense cross-check;
   3–9min → pace, ZoneSense lags; <3min → pace only. Easy/long/race work is always ZoneSense
   Zone 1. See `rules/endurance-authoring.md`.
5. **Long/ultra-effort sessions use `target_mode: hr` or `effort`, never `pace`.** Pace targets are
   for sessions under ~2h. This is the fix for Runna's core mistake (prescribing marathon pace for a
   multi-hour ultra effort).
6. **Never invent a race distance or pace target that contradicts `races/2026-10-17-ghost-train.md`.**
   The Runna seed's `50km at 5:35-5:55/km` is wrong and stays discarded.
7. **Frontmatter `published.suunto` is the only idempotency mechanism.** Don't re-push a session
   whose body hasn't changed since it was last published. See `rules/publishing.md`.
8. **Anything pulled from the Suunto API is DRAFT until the athlete confirms it.** The numbers are
   real, but the *interpretation* usually isn't obvious from the data alone — a fragmented night
   might be a sick kid or a watch artifact; a low HRV reading might be alcohol, illness, or noise;
   a "hard" session might have had a deliberate effort inside it. Present Suunto-derived findings
   and their proposed reading to the athlete BEFORE committing them as fact, and record the context
   they give alongside the number. Two corrections already came from exactly this: the 08-02 30k
   initially read as chronic mis-pacing (it was a deliberate 10k plus 86F heat), and treadmill data
   was briefly written off as unreliable (it reconciled perfectly once walking was separated out).
   **Ambient conditions are the one piece of that context now available without asking** — run
   `scripts/heat_load.py` on any outdoor session before interpreting how hard it was
   (`rules/conditions.md`). The watch's own temperature field is body heat off the wrist and is
   never ambient; believing it is what produced the second correction above.
9. **`seed/*` files are frozen.** If something from Runna or the Champion Plan needs to change for
   this athlete, make the adapted version in `training/`, `endurance/`, or `strength/` — don't edit
   the seed.

10. **Write plainly. No jargon dressed up as precision.** Added 2026-09-14 after the athlete
   called out "*Amber, and it does not bind on a 45-minute recovery run*" — which was econ-speak
   for "it doesn't change today's plan." Say the plain thing. Specifically:
   - Don't use **"bind" / "binding" / "does not bind"** to mean a rule or flag matters or doesn't.
     Say *it doesn't change the plan*, *it costs you nothing*, *that's the limit here*.
     (The one exception already in the repo: "time is the binding constraint" in `README.md` and
     `athlete/profile.md`. That one is idiomatic and stays.)
   - Same for other borrowed-sounding hedges: *obtains*, *is dispositive*, *non-trivial*,
     *orthogonal*, *load-bearing*, *the operative question*. Pick the everyday word.
   - The test: would you say it out loud to him at a trailhead? If not, rewrite it.
   This is about **word choice, not tone.** Keep being direct, keep leading with the conclusion,
   keep the bold. Just use plain words to do it.

## Typical workflows

**Authoring a new week** (`training/weeks/wNN.md` doesn't exist yet):
1. Look up the block-week → Champion-week mapping in `training/block.md` to know which Champion
   week's shape to use.
2. Apply the weekly template (Mon–Sun day pattern) from `training/block.md`.
3. Write one `endurance/YYYY-MM-DD-<slug>.md` per running/riding/walking session for that week,
   following `rules/endurance-authoring.md`.
4. Confirm which Liftoscript `# Week N` corresponds to this block week (offset is fixed: block week
   9 = Liftoscript Week 1), and check `strength/program.liftoscript` already covers it — if not,
   append it following `rules/strength-authoring.md`.
5. Write `training/weeks/wNN.md` linking everything and stating the week's intent, referencing the
   verification checks below.
6. Run the invariant checks (time budget, lifting placement, `m`-for-meters).

**Recording a day** (the athlete reports how a session went, or a Suunto pull needs interpreting):
write or update `log/YYYY-MM-DD.md` per `rules/logging.md` — copy `log/TEMPLATE.md`, fill only what
was actually reported, and **never backfill a rating the athlete didn't give you**. Soreness,
session-RPE and `shade_pct` are the three signals nothing else can supply; everything else the
watch already knows and should not be retyped by hand. If the session was outdoors, fill the
`conditions:` block with the script rather than by hand or by asking:

```bash
python3 scripts/heat_load.py --workout-json <workout.json> --write   # rules/conditions.md
```

**Adjusting a week from `log/` feedback** (fatigue, missed session, illness, an unplanned group
ride or eMTB spin): re-read `rules/progression.md` for the cut order and the unplanned-session
handling rules in `training/block.md`, then edit the affected `endurance/*.md` files in place
(don't create duplicates) and update `published.suunto` handling per `rules/publishing.md` if a
file that was already pushed changes.

**Publishing**: see `rules/publishing.md`. Push a rolling ~2-week window, not the whole plan at
once — the plan is meant to adapt to how training actually goes.

## Verification — run the script

```bash
python3 scripts/verify_plan.py
```

It checks the mechanical invariants against `athlete/profile.md` (nothing is hardcoded) and exits
non-zero on failure: weekly running-time budget, per-session and long-run caps, the night-session
cap, the walking ramp limit, the `m`-means-minutes trap, rest steps missing a target, long sessions
wrongly using `target_mode: pace`, and malformed frontmatter. Run it after authoring or editing any
week.

It also validates `log/` (`rules/logging.md`) and prints the recent readiness/soreness/RPE readout.
Malformed log data is an error; a *missing* rating is only ever a warning — a blank field is a
legitimate answer, and failing the build over one would just teach the athlete to ignore the
script. The warnings worth reading are RPE running over plan for the session type (easy-day creep)
and two consecutive amber/red calls, which is a re-author trigger, not a note.

It checks the `conditions:` blocks too (`rules/conditions.md`). The one to take seriously is **an
over-plan RPE on a day whose WBGT was red or black** — that reads as heat, not fitness, and is the
exact mistake this repo has already made twice. Don't re-author a week off a hot session alone.

Then eyeball the two things a script can't judge:

- [ ] No heavy lower-body lift precedes a long run or Wednesday's big workout, and Friday is still
      a true rest day (the placement rules in `rules/strength-authoring.md`)
- [ ] Sessions carrying `time_critical:` still have their timing intact; everything else is
      free to move within the day — do not impose clock times on ordinary runs

```bash
python3 scripts/generate_calendar.py   # visual overview of the whole block
python3 scripts/heat_load.py --history # what heat and shade have actually cost this athlete
```
