# Progression — build the next week, deload, taper, autoregulate

## The time-budget check — run this first, every week

Sum `duration_s` across the week's `endurance/*.md` files, **excluding** any with
`concurrent: meetings`. Compare against `athlete/profile.md` → `time_budget.weekly_total_max_min`.
Also confirm no single session exceeds its per-session cap. **Do not check sessions against fixed
time-of-day slots** — scheduling is opportunistic (`athlete/profile.md`), and only the handful of
sessions carrying `time_critical:` have a real clock requirement.

**If the week busts the budget, cut in this order — never reorder it:**

1. Strength volume — drop a main lift's active tier from `!` on tier 1 down to tier 2 or 3 (see
   `rules/strength-authoring.md`), or drop the Upper B session entirely.
2. Doubles (meeting-time sessions are unaffected — they're not in this budget at all; this means
   the *running* doubles, the 40–50min pre-dawn/post-bedtime add-ons).
3. Easy-day volume (shorten Tuesday, Monday).
4. Wednesday's quality session (reduce volume, not intensity — keep the stimulus, cut the reps/sets).
5. The Saturday long run or Sunday back-to-back — **cut last**, and only ever shorten, never skip
   outright unless `log/` shows a real red flag (injury, illness).

## Readiness ladder — selects the strength tier and can downgrade a run

Check each morning against the day's plan, worst signal wins:

**Three of these four signals are now pulled automatically from Suunto wellness** rather than
hand-logged — sleep duration/quality, HRV, and resting HR all come from the nightly record, and
body-resource "balance" is sampled through the day. Only soreness and RPE need entering by hand.

| Signal | Green | Amber | Red | Source |
|---|---|---|---|---|
| Sleep duration | ≥7h30 | 6–7h30 | <6h | Suunto `wellness_sleep` |
| Sleep quality / fragmentation | ≥0.75, one block | 0.55–0.75 | <0.55, **or broken into 3+ fragments** | Suunto |
| HRV (nightly avg RMSSD) | ≥80 | 60–80 | <60 | Suunto |
| Resting HR | ≤43 | 44–48 | ≥49 | Suunto |
| Body resources ("balance") | ≥0.70 | 0.40–0.70 | <0.40 | Suunto `wellness_recovery` |
| Soreness (0–10) | ≤3 | 4–6 | ≥7 | manual, `log/` |
| RPE trend (last 3 sessions) | on target | +1 over plan | +2 or more | manual, `log/` |

Baselines to compare against are in `athlete/zones.yml` → `baseline`. **Fragmentation matters as
much as duration** — the night of 2026-08-01 totalled 8h00 but arrived in seven separate pieces
with HRV suppressed to 49, and the 30k the next morning followed. Total hours alone would have
scored that night green.

- **Green** → run the day as planned; main lifts at tier 1.
- **Amber** → main lifts drop to tier 2; easy runs stay easy (don't let effort creep); Wednesday's
  workout can proceed but consider trimming volume, not intensity.
- **Red** → main lifts drop to tier 3 or skip entirely (accessory/core only, or nothing); downgrade
  Wednesday's workout to easy aerobic; a long run under red should shorten, not intensify. Log the
  reason in `log/YYYY-MM-DD.md` so the pattern is visible later.

## Weekly build / deload / mid-cycle-rest policy

Inherited from the Champion Plan mapping in `training/block.md`:

- Block weeks 9 and 14 are **down/rest weeks** by design (Champion weeks 6 and 11) — don't add
  volume back in during these weeks even if the athlete feels strong; the adaptation happens on the
  down week, not despite it.
- Block week 11 is a **big-volume week** (Champion week 8) — the time-budget check matters most
  here; if it's tight, this is the week most likely to need a strength cut.
- Block week 13 is the **Big Day** — a moderately hard ~50k-effort long run with full race fueling,
  deliberately run to accumulate real fatigue. Do not schedule Wednesday's workout at full intensity
  that same week; let the Saturday effort be the week's single hard stimulus alongside it.
- Block weeks 18–19 are **taper** — volume drops (23km → 13km → race) but keep one short night run
  in week 18 so the circadian rehearsal doesn't go stale, and drop strength to Lower B character only
  from week 16 onward, last heavy squat day week 17, no lifting at all in race week (19).

## Pace progression

Tighten `athlete/zones.yml` → `pace.easy_ceiling` on the schedule already implied by the seed
(6:05 → 6:00 → 5:55 → 5:50, roughly every 3 weeks — see `easy_ceiling_history` in that file) as
long as the readiness ladder is staying green/amber. If a block is running consistently amber/red,
hold the current ceiling rather than tightening on schedule — the "get faster" goal is subordinate
to the time-budget and injury constraints, not the other way around.

Wednesday's session type should follow the Champion progression across the block: hills → track/
speed intervals → uphill-treadmill threshold → pre-taper tune-up. Don't run the same Wednesday
format two blocks in a row without a reason.

## Walking ramp (meeting time)

Check every week: `sport: Walk` total vs. last week's total must not increase by more than
`athlete/profile.md` → `meeting_budget.walking.weekly_ramp_max_pct` (15%). This is the most likely
source of an overuse injury in this entire plan — a sudden jump from incidental walking to hours a
day is exactly the kind of load spike that causes plantar fascia or achilles problems. If a week's
walking total would need to jump more than 15% to hit the target in `athlete/profile.md`, hold it at
the capped increase instead and let the peak arrive a week or two later than planned.

## When `log/` should trigger a re-author, not just a note

- A missed or shortened long run → don't try to "make it up" the following week; re-derive that
  week's back-to-back and Wednesday session from where fitness actually is, not where the plan
  assumed it would be.
- Two consecutive amber/red readiness weeks → treat the next scheduled hard week as a down week
  instead, and push the Champion-week mapping out by the same amount (this shifts the taper start
  too — flag it explicitly if it does, since race day itself doesn't move).
- An unplanned group ride or eMTB spin → apply `training/block.md` § "Unplanned sessions" and adjust
  the rest of that week's plan immediately, not retroactively.
