# AGENTS.md — how to operate this repo

This repo has no compiler and no CI. You (an LLM, in a future session) are the only thing that
turns intent into files. This document is the entry point: what to read, in what order, and the
invariants you must never violate.

## Read order, before touching anything

1. `athlete/profile.md` — the time budget. Every session you author is checked against this.
2. `races/2026-10-17-ghost-train.md` — what the race actually is, and the goal tiers.
3. `training/block.md` — the policy: block-week ↔ Champion-week mapping, the weekly template, and
   the numbered reshaping rules. This is the thing you're implementing every time you author a week.
4. The specific `training/weeks/wNN.md` you're working on, if it already exists.
5. `rules/endurance-authoring.md` and `rules/strength-authoring.md` — syntax references. Read these
   immediately before writing any endurance or strength file; the gotchas in them (especially the
   `m` = minutes trap) are easy to get wrong from memory.
6. `rules/progression.md` and `rules/fueling.md` as needed for the specific decision at hand.

`seed/` is historical input only — read it for context (what paces the athlete was already hitting,
what the professionally designed plan says), never edit it, never treat it as current instruction.

## Hard invariants — never violate these

1. **The time budget in `athlete/profile.md` is a hard constraint, not a target.** Before finalizing
   any week, sum `duration_s` across that week's `endurance/*.md` files (excluding anything with
   `concurrent: meetings`) and confirm it's within `weekly_total_max_min`. If it isn't, cut — in
   order: strength volume (drop to a lower set-variation tier, or drop Upper B first) → doubles →
   easy volume → quality → long run. The long run and the Saturday/Sunday back-to-back are cut last.
2. **Running always wins conflicts with lifting**, per the user's own strength spec in
   `rules/strength-authoring.md`. Never schedule heavy lower-body work the day before a long run or
   a quality session. Never let a lift compromise Wednesday's big workout or the weekend.
3. **`m` in intervals.icu syntax means minutes, not meters.** Use `mtr` for meters or express as km.
   This is the single most common way to silently corrupt a workout — check every endurance file
   you write for a bare `m` that was meant to mean meters.
4. **Long/ultra-effort sessions use `target_mode: hr` or `effort`, never `pace`.** Pace targets are
   for sessions under ~2h. This is the fix for Runna's core mistake (prescribing marathon pace for a
   multi-hour ultra effort).
5. **Never invent a race distance or pace target that contradicts `races/2026-10-17-ghost-train.md`.**
   The Runna seed's `50km at 5:35-5:55/km` is wrong and stays discarded.
6. **Frontmatter `published.suunto` is the only idempotency mechanism.** Don't re-push a session
   whose body hasn't changed since it was last published. See `rules/publishing.md`.
7. **`seed/*` files are frozen.** If something from Runna or the Champion Plan needs to change for
   this athlete, make the adapted version in `training/`, `endurance/`, or `strength/` — don't edit
   the seed.

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

**Adjusting a week from `log/` feedback** (fatigue, missed session, illness, an unplanned group
ride or eMTB spin): re-read `rules/progression.md` for the cut order and the unplanned-session
handling rules in `training/block.md`, then edit the affected `endurance/*.md` files in place
(don't create duplicates) and update `published.suunto` handling per `rules/publishing.md` if a
file that was already pushed changes.

**Publishing**: see `rules/publishing.md`. Push a rolling ~2-week window, not the whole plan at
once — the plan is meant to adapt to how training actually goes.

## Verification checklist (run before considering a week "done")

- [ ] Weekly running-time total ≤ `athlete/profile.md` → `time_budget.weekly_total_max_min`
- [ ] No single session exceeds its per-session cap or falls outside a `protected_windows` slot
- [ ] No heavy lower-body lift precedes a long run or Wednesday's big workout
- [ ] Friday is a true rest day (blackout + pre-long-run leg recovery)
- [ ] Every long/ultra session uses `target_mode: hr` or `effort`, not `pace`
- [ ] No endurance file uses bare `m` where meters was meant
- [ ] `sport: Walk` weekly total respects `meeting_budget.walking.weekly_ramp_max_pct`
