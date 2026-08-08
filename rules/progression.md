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
body-resource "balance" is sampled through the day. Only soreness and RPE need entering by hand;
**`rules/logging.md` is where they go**, along with the anchored 0–10 scales that keep them
comparable across the block and the expected-RPE-by-session-type table that defines "over plan"
in the row below.

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

- Block week 14 is the block's **down/rest week** by design (Champion week 11, mid-cycle rest) —
  don't add volume back in during it even if the athlete feels strong; the adaptation happens on
  the down week, not despite it. **Week 9 was removed from this rule 2026-08-08**: it had been
  labeled a down week via the Champion mapping, but it directly follows a zero-running vacation
  week, so the label prescribed redundant rest — it is a re-entry week (`training/weeks/w09.md`),
  and the don't-add-volume prohibition never applied to it.
- Block week 11 is a **big-volume week** (Champion week 8) — the time-budget check matters most
  here; if it's tight, this is the week most likely to need a strength cut.
- Block week 13 is the **Big Day** — a moderately hard ~50k-effort long run with full race fueling,
  deliberately run to accumulate real fatigue. Do not schedule Wednesday's workout at full intensity
  that same week; let the Saturday effort be the week's single hard stimulus alongside it.
- Block weeks 18–19 are **taper** — volume drops (23km → 13km → race) but keep one short night run
  in week 18 so the circadian rehearsal doesn't go stale. Strength recedes in a specific shape
  (see `strength/notes.md` § Taper handling): week 16 — the peak *running* week — cuts Lower A to
  reduced volume, because lifting is first in the cut order exactly when running stress peaks;
  week 17 takes the one final full Lower A (the last squat day, ~2.5 weeks out); from week 18 it's
  Lower B/Upper B character only at reduced sets; race week (19) no lifting at all.

## Pace progression

`pace.easy_ceiling` (7:00) is anchored to the athlete's measured PRs, not to a plan schedule —
`athlete/zones.yml` documents how the Runna-seeded values (6:05 tightening toward 5:50) were
contradicted by his actual 5k/10k and rebuilt from them. **Never tighten the ceiling on a
calendar.** It moves only on the `pace_review` triggers in that file: a new PR, or real
long-effort data from the Big Day and the lap simulations. If those show easy pace has genuinely
improved, update `athlete/zones.yml` deliberately (with the evidence noted in its header); and if
the readiness ladder is running amber/red, don't tighten at all — the "get faster" goal is
subordinate to the time-budget and injury constraints, not the other way around.

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

**During and just after a travel week with hiking** (`sport: Hike`, `concurrent: family`), check the
cap against *combined time-on-feet* (`sport: Walk` + `sport: Hike` that week), not the walking pool
in isolation. The injury mechanism the cap defends against is cumulative foot-time load, and hiking
loads the same tissues. A week that resumes meeting-walking at a higher figure than the *walking*
15%/week cap alone would allow is not a spike if a recent hiking week already delivered comparably
high or higher combined foot-time — the tissue has already demonstrated tolerance. Concretely: block
week 12's ~600min hiking week means block week 14's 355min pure-walking figure is a *drop* from
recent load, not a violation, even though it is +61% over week 13's 220min walking-only total. Only
throttle the walking figure in this situation if the combined-load read still shows a genuine spike.

## When `log/` should trigger a re-author, not just a note

- A missed or shortened long run → don't try to "make it up" the following week; re-derive that
  week's back-to-back and Wednesday session from where fitness actually is, not where the plan
  assumed it would be.
- Two consecutive amber/red readiness weeks → treat the next scheduled hard week as a down week
  instead, and push the Champion-week mapping out by the same amount (this shifts the taper start
  too — flag it explicitly if it does, since race day itself doesn't move).
- An unplanned group ride or eMTB spin → apply `training/block.md` § "Unplanned sessions" and adjust
  the rest of that week's plan immediately, not retroactively.
