# Conditions — the heat the session actually ran in, and what shade was worth

The watch cannot measure ambient temperature. Its sensor sits against the wrist and reads body
heat, and it is wrong in both directions — an 85°F run recorded as 72°F, a 72°F gym recorded as
79°F (`.claude/skills/daily-brief/references/suunto-fields.md`). That is not a calibration
problem with a correction factor; it is the wrong quantity.

This mattered twice before there was a fix. The 08-02 30k read as chronic mis-pacing until the
athlete said it was 86°F. The 08-04 run was written up as having "no heat confound" straight from
the wrist figure, and had to be corrected the next day — the real number was 85°F, which is the
difference between a run that says something about fitness and a run that says something about
thermoregulation. Both are exactly the AGENTS.md invariant 8 failure: a Suunto number believed
without the context that makes it interpretable.

`scripts/heat_load.py` closes that hole. It takes the session's own GPS track and clock, asks
Open-Meteo what the weather was over that ground at that time, and writes a `conditions:` block
into the day's log entry.

```bash
python3 scripts/heat_load.py --workout-json workout.json              # look
python3 scripts/heat_load.py --workout-json workout.json --shade-pct 60 --write   # log it
python3 scripts/heat_load.py --history                                # what shade has been worth
```

`workout.json` is whatever `mcp__suuntool-guides__workouts_get` (or one item from
`workouts_list`) returned — write it to a file, or pipe it in with `--workout-json -`.

## Why the number comes in a pair

Solar radiation is the biggest term in outdoor heat stress and the only one shade removes. On a
clear August afternoon here, standing in the sun versus standing under canopy is worth **5–8°F of
WBGT** — larger than most of the day-to-day temperature swings the athlete would otherwise blame
for a hard-feeling run, and larger than the difference between two adjacent flag categories.

A single WBGT number would hide that, and it would hide it in the one direction that matters:
route choice is a lever the athlete actually controls, unlike the temperature. So the script
reports the **bracket** — the same hour experienced in full sun and in full shade — and asks for
one number to place the session inside it:

```yaml
conditions:
  source: open-meteo/forecast  # 42.7717,-71.6743, from the session's GPS track
  temp_f: 85                   # mean over the session window
  rh_pct: 57
  solar_w_m2: 861              # mean global horizontal irradiance
  wbgt_sun_f: 82.4             # the bracket: fully exposed ...
  wbgt_shade_f: 77.5           # ... and fully shaded
  shade_pct: 65                # ATHLETE — 0-100, roughly. The only field here that needs you
  wbgt_f: 79.2                 # derived from shade_pct; the number the ladder reads
```

**`shade_pct` is the only manual field, and it is deliberately allowed to be rough.** A number to
the nearest 25% is enough — "open road" (0), "mixed" (50), "almost all rail-trail" (85). It does
not need to be defensible; it needs to exist, because without it the bracket stays a bracket and
the session cannot be compared to any other session. Precision here buys much less than presence.

Two conventions, and they mean different things:

- `shade_pct: null` — not answered yet. `verify_plan.py` will keep asking, but only when the
  bracket is wide enough to matter.
- `shade_pct: n/a` — **asked and settled.** There was no direct sun in the window, so there was
  nothing to shade. Night sessions land here automatically and are never asked; so does heavy
  overcast. `heat_load.py` writes `n/a` itself and fills `wbgt_f` directly.

## Outdoor only, and the script decides

A workout with no GPS track was a treadmill or a gym, and `heat_load.py` refuses to write a
conditions block for one. This is not tidiness. Outdoor weather attached to an indoor session is
worse than no number at all: it reads as real, it is precisely wrong, and it would corrupt the
`--history` comparison that the whole `shade_pct` habit is being built to feed. A treadmill room's
heat is its own variable and belongs in the body of the log, in words.

If the watch genuinely dropped GPS on a run that was outside, pass `--lat/--lon` and it will
proceed.

## The model, and where it is soft

WBGT = 0.7·T_wetbulb + 0.2·T_globe + 0.1·T_air, the standard outdoor form.

- **Wet bulb** comes straight from Open-Meteo, and is the *psychrometric* wet bulb standing in
  for the *natural* wet bulb the index actually specifies. This runs cool by roughly 1°C in
  strong sun and light wind. So the absolute WBGT is a slight **underestimate on the hottest
  days** — the direction to know about, since those are the days a number gets used. It does not
  distort the sun/shade spread, which is carried by the globe term.
- **Globe temperature** is solved from an energy balance on a standard 150mm black globe:
  beam absorbed over the sphere's projected area (DNI/4), diffuse over the upper hemisphere
  (DHI/2), ground-reflected over the lower (albedo·GHI/2), longwave exchange with sky and ground,
  and Ranz-Marshall convection. It is not a fitted correlation; the geometry is derived, so the
  sun/shade difference it produces is trustworthy even where the absolute value drifts.
  Spot-checked against published values: 30°C air, 50% RH, clear noon, 1 m/s gives a globe of
  53°C and WBGT of 29°C, both in line with standard tables.
- **"Full shade" is not just the beam switched off.** A canopy also hides about half the sky and
  replaces it with leaves at roughly air temperature (`--canopy-svf`, default 0.5). This is why
  the script reports shade as very slightly *warming* on a clear night — under canopy the body
  loses less heat to a cold sky, which is real, and is the correct sign.
- **Two knobs are assumptions about the athlete's own routes**, not physics, and are worth
  revisiting if the numbers ever look off: `--albedo` (default 0.20, mixed trail/road) and
  `--surface-gain` (default 0.012 °C per W/m², how much hotter sunlit ground runs than air —
  bare asphalt is nearer 0.020, deep grass 0.006).
- **Self-generated airflow is deliberately excluded.** WBGT is an environmental index measured by
  a stationary instrument, and a runner making their own 3 m/s breeze is genuinely cooler than the
  index says. Do not fold it in; read it as "the conditions", not "the athlete's heat strain".

## How much to trust this

Open-Meteo is a ~2km reanalysis grid, not a thermometer at the trailhead. It is a good estimate of
the ambient the session ran in and a far better one than the wrist sensor, but it does not know
about the road surface, the river valley, or the parking lot. It is not evidence against the
athlete's own recollection: **if he says it was hotter than this, he is right and the note goes in
the log body.** The block is a floor under the interpretation, not a ceiling on it.

The flag colours (`GREEN` / `YELLOW` / `RED` / `BLACK` at 10/18/23/28°C) are ACSM road-race
guidance for mass events with medical tents, and they are conservative for one acclimatized
athlete on a route he knows with water he carries. Read them as "how much this session was really
asking", not as permission or prohibition.

## What the plan does with it

`scripts/verify_plan.py` validates the block and raises the case this whole file exists for:
**an RPE over plan on a day whose WBGT was red or black gets flagged as heat first, not fitness.**
That is the check that would have caught the 08-02 reading before it became a wrong conclusion
about pacing. Do not re-author a week off a hot session's data alone.

It also nudges — once, and only when the bracket was wide enough to matter — if `shade_pct` is
still null, and errors if `wbgt_f` has drifted out of agreement with the bracket and `shade_pct`
(re-run the script rather than hand-editing a derived field).

`--history` tabulates every logged session's conditions against its RPE, and once there are four
or more it fits a slope: how much RPE moves per °F of effective WBGT, **for this athlete**. That
is the actual point of asking about shade every hot day. Treat the slope as descriptive only —
session type is not controlled for, and an easy day in the heat next to an interval day in the
cool will happily fake one. Read it alongside the session types, never instead of them.

## What not to do

- **Don't backfill.** The script can fetch any past date, but a conditions block on a day whose
  session you are reconstructing from memory invites the same false confidence the wrist sensor
  did. Log it when the workout syncs.
- **Don't put ambient temperature in the log body as well.** It is in the frontmatter now; a
  second hand-typed copy is the kind of duplication `rules/logging.md` exists to prevent. The body
  is for what the model cannot get: that the humidity felt worse than the number, that the last
  climb was in full sun at 2pm, that the water ran out.
- **Don't fill `shade_pct` on the athlete's behalf.** It is a manual signal exactly like soreness
  and RPE, and `rules/logging.md` is unambiguous: never backfill a rating he did not give. A null
  is honest; a guessed 50 is corruption that then propagates into `wbgt_f` and the history slope.
