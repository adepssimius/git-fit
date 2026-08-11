---
date: YYYY-MM-DD
readiness: null           # green | amber | red — the call you acted on (rules/progression.md)
soreness_0_10: null       # 0-10 on waking, before warmup. 1-3 green | 4-6 amber | 7+ red
rpe_0_10: null            # session-RPE for the day's main session, rated ~30min after
sleep_context: null       # WHY, not hours — "sick kid, up 3x" / "flight" / null if unremarkable

# Outdoor sessions only. Don't type this block — `python3 scripts/heat_load.py --workout-json
# <workout> --write` fills every field from the session's own GPS track (rules/conditions.md).
# Delete the whole block if the session was indoors; it refuses to write one anyway.
conditions:
  source: null            # open-meteo/forecast | open-meteo/archive
  temp_f: null            # mean over the session window
  rh_pct: null
  solar_w_m2: null        # mean global horizontal irradiance
  wbgt_sun_f: null        # the bracket: the same hour fully exposed ...
  wbgt_shade_f: null      # ... and fully shaded
  shade_pct: null         # ATHLETE — 0-100, roughly. The only field here that needs you.
                          # `n/a` when there was no sun to block (night, heavy overcast)
  wbgt_f: null            # derived from shade_pct; the number the plan reads
---

## How it felt

- **Legs:**
- **Feet:**
- **Gut:**
- **Head:**

## Sessions

- **Planned:** [name](../endurance/YYYY-MM-DD-slug.md) — done as written | short (how much, why) | moved (to when) | skipped (why)

## Unplanned

<!-- Group ride / eMTB / hiking. What it was, roughly how hard, AND the adjustment it forces
     on the rest of the week (training/block.md § "Unplanned sessions"). Delete if none. -->

<!-- Copy this file to log/YYYY-MM-DD.md. Fill what you have, leave the rest null — a null is
     honest, a guess is corruption. Full guidance and the anchored scales: rules/logging.md
     verify_plan.py skips this file; only YYYY-MM-DD.md entries are validated.

     Three fields are yours and nothing can supply them: soreness, RPE, and shade_pct.
     Everything else in the frontmatter comes from the watch or from scripts/heat_load.py. -->
