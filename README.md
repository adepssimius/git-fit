# git-fit

A version-controlled training plan for **Ghost Train Trail Races** (Brookline, NH —
2026-10-17, 30-hour lapped ultra), authored and maintained by an LLM following the rules in this
repo, and pushed to devices via two MCP tools:

- **Running / cycling / walking** → a Suunto MCP tool, which consumes [intervals.icu text
  syntax](https://forum.intervals.icu/t/workout-builder-syntax-quick-guide/123701) and pushes it as
  a SuuntoPlus Guide.
- **Strength** → a Liftosaur MCP tool, which consumes
  [Liftoscript](https://www.liftosaur.com/doc/liftoscript).

There is no build step and no CI yet. The plan is plain text; an LLM (or you) edits it directly.

## Start here

Read [`AGENTS.md`](AGENTS.md) first — it's the entry point for anyone (human or LLM) picking this
repo up cold: what order to read things in, what the hard constraints are, and how to author or
adjust a week.

## Layout

| Path | What it is |
|---|---|
| `athlete/` | Who's training: time budget, zones, current maxes. Load-bearing — everything else is checked against `athlete/profile.md`. |
| `races/` | The real event model for Ghost Train: laps, aid/crew topology, goal tiers, decision tree. |
| `training/block.md` | The policy: how block weeks map to the Champion Plan, the weekly template, progression rules. |
| `training/weeks/` | One file per week — the only place running and strength are tied together. |
| `endurance/` | One file per running/cycling/walking session, in intervals.icu syntax, ready to push. |
| `strength/` | The whole Liftosaur program, in Liftoscript. |
| `rules/` | The instructions an LLM follows to author or adjust the plan — syntax references and house rules. |
| `seed/` | Frozen one-time imports: the old Runna plan and the supplied "Champion Plan." Reference only, never edited. |
| `log/` | Actuals — RPE, sleep, soreness, unplanned sessions (group rides, eMTB) — feeds autoregulation. |
| `scripts/` | `verify_plan.py` (checks the hard invariants) and `generate_calendar.py` (HTML overview). |

## Scripts

```bash
python3 scripts/verify_plan.py        # check every week against athlete/profile.md — exits non-zero on failure
python3 scripts/generate_calendar.py  # write calendar.html, a month-by-month overview
```

Both read the repo and never write back into the plan.

## Published calendar

`.github/workflows/pages.yml` builds the calendar on every push and deploys it to GitHub Pages.
The workflow runs `scripts/verify_plan.py` **first**, so a week that busts the time budget, the
long-run cap, or the `m`-means-minutes trap fails the build instead of publishing a broken plan.

To enable it once: repo **Settings → Pages → Build and deployment → Source: GitHub Actions**.

> ⚠️ **On a public repo, GitHub Pages publishes all of this to the open internet.** This repo holds
> a lot of personal information: PR times, daily schedule and protected training windows, your
> kids' bedtime, the exact location of your regular training route including where the car and drop
> bag sit on it, and **dated windows stating when you are away from home**. A home-area route plus
> precise away-from-home dates is the combination worth thinking hardest about.
>
> Options: keep the repo **private** (Pages on a private repo requires GitHub Pro), or strip
> `athlete/profile.md` and `log/` before going public.

## Why it's built this way

- **Runna is gone.** It generated the original plan but is being abandoned; `seed/runna-plan.md`
  is a frozen one-time export, not a live sync. All future authoring happens in this repo.
- **The target formats are stored directly**, not an abstract DSL — endurance files are literal
  intervals.icu syntax, strength is literal Liftoscript. No compiler, meaningful git diffs, and
  publishing is close to a direct copy of the file body.
- **Time is the binding constraint**, not fitness. The athlete is a time-limited parent training for
  a distance well past what the available hours would normally support, so the plan leans hard on
  free training time (meeting-time trainer rides and walks) and a professionally designed ultra
  plan (`seed/champion-plan.md`) adapted for a flat, crewed, lapped course. See `training/block.md`
  for the full reasoning.
