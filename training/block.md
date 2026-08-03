# Training block policy — block weeks 9–19

This is the policy an LLM implements when authoring or adjusting any week. It resolves three
inputs: the Runna seed (`seed/runna-plan.md`, base fitness + long-run skeleton), the supplied
Champion Plan (`seed/champion-plan.md`, structural authority), and the athlete's own hard
constraints (`athlete/profile.md`, `rules/strength-authoring.md`).

Block week 9 starts **2026-08-03** (Monday); the race is block week 19, **2026-10-17**.

## Why this block looks the way it does

Two problems with the inherited Runna plan drove the redesign:

1. **The race was modeled wrong.** Runna prescribed `50km at 5:35-5:55/km` — road-marathon logic
   for an event that's actually a flat, crewed, lapped ultra. See `races/2026-10-17-ghost-train.md`.
2. **The plan was a marathon plan.** It peaked at a 40km long run with no back-to-backs, no night
   running, no run/walk protocol, and no fueling rehearsal — none of which are optional for a
   100km-to-100mile attempt.

Two athlete-specific facts then shaped everything else:

- **Time, not fitness, is the binding constraint** (father of young kids, full-time job). This
  inverts the usual ultra-training answer: instead of maximizing time on feet, the plan optimizes
  **distance per training hour**, which is why speed work is promoted rather than demoted, and why
  meeting-time training (trainer + walking) matters so much.
- **Meeting time is a large, mostly-free pool**, splittable between trainer Z2 (aerobic base,
  non-impact) and walking (time on feet, race-specific durability — see `athlete/profile.md`).
  Walking during meetings is close to a direct answer to the ultra's real limiter: foot, calf, and
  achilles durability over 24+ hours.

## The lap rhythm and the goal

See `races/2026-10-17-ghost-train.md` for the full model. Short version: 100km primary goal, 100
miles stretch goal, crew every ~12km, and the 30h cutoff is generous — the limiter is durability and
logistics, not raw speed.

## Block-week ↔ Champion-week mapping

The athlete has ~11 weeks to race day and 8 weeks of Runna base already behind them, so block weeks
9–19 map onto **Champion weeks 6–16** — the back end of the 16-week plan. The Runna long-run
progression already tracks the Champion shape closely enough that this is mostly a relabel with two
free alignments: the seed's 42.2km run on Sep 5 lands exactly on the Champion Plan's Big Day, and
the seed's drop to 20km the following week lands exactly on its mid-cycle rest block.

| Block wk | Dates | Champion wk | Sat long (seed) | Champion prescribes | Fit |
|---|---|---|---|---|---|
| 9 | Aug 3–9 | 6 — down week | 15km | 10–16mi (16–26km) | ✓ |
| 10 | Aug 10–16 | 7 | 34km | 16–20mi (26–32km) | ✓ |
| 11 | Aug 17–23 | 8 — big | 38km | 20–25mi (32–40km) | ✓ |
| 12 | Aug 24–30 | 9 — overreach | 30km | 12–20mi (19–32km) | ✓ |
| 13 | Aug 31–Sep 6 | 10 — **BIG DAY** | **42.2km** | marathon/50k hard effort | ✓✓ already a 42.2km run |
| 14 | Sep 7–13 | 11 — mid-cycle rest | 20km | easy 10–16mi | ✓✓ seed already drops |
| 15 | Sep 14–20 | 12 | 38km | 16–20mi | ✓ |
| 16 | Sep 21–27 | 13 | 40km | 20–25mi (32–40km) | ✓✓ |
| 17 | Sep 28–Oct 4 | 14 | 23km | 14–18mi (22–29km) | ✓✓ |
| 18 | Oct 5–11 | 15 — taper | 13km | 10–14mi (16–22km) | ✓ |
| 19 | Oct 12–18 | 16 — race | **RACE (10-17)** | race | ✓ |

## What's adopted from the Champion Plan

- **Wednesday as the single big midweek workout**, replacing the seed's two midweek quality days —
  one real session plus quality embedded in the Saturday long run, everything else genuinely
  aerobic.
- **Thursday x-train, 1–2.5h easy Z2** — the Champion Plan and the meeting-time trainer land on the
  same square. Free, and now structurally justified.
- **Hill strides on easy days** (5–6 × 20–30s fast, jog down). Near-zero time cost, serves the
  "get faster" goal directly.
- **Uphill treadmill threshold sessions** (e.g. 8–12 × 4min at 1-hour effort, 8–10% grade) as several
  weeks' Wednesday workout — big aerobic stimulus, low impact, low injury risk.
- **Weight-vest incline walking** during meeting time — this *is* the Champion Plan's uphill/vest
  work, at zero time cost. Ramp under the same walking rules; see `athlete/profile.md`.
- **Heat training** — sauna/hot tub 20–30min on rest days. Low stress, real plasma-volume return.
- **The Big Day** (block wk 13, Sat Sep 5): a **true 50k, run as two full laps of the actual course,
  starting ~18:00 so four of its five-plus hours are in the dark** — then the mid-cycle rest block in
  week 14 absorbs it. Because the athlete has course access, this single session covers the Big Day,
  a night run, course recon, and a two-lap crew rehearsal at once. It is the only session in the
  block that rehearses distance, darkness, surface and logistics simultaneously, and it carries an
  explicit budget exception (below).
- **Strength recedes as running stress rises** — Champion drops midweek strength around its week 13
  and ends squats at week 14. Applied here: taper Lower A toward Lower B in character from block
  week 16, last heavy squat day block week 17, no strength race week.
- **Fuel long runs at 75+ g carb/hr**, building toward 90–120 g/hr (`rules/fueling.md`).
- **Core routine 1–2×/daily.**

## What's adapted for a flat rail trail

The Champion Plan is written for mountain ultras and repeatedly treats vert as more important than
mileage. Ghost Train is flat, so:

- Keep uphill treadmill and incline-walk work as a low-impact aerobic tool, not race specificity.
- Keep some downhill/eccentric work for muscle-damage resistance, but don't build weeks around it —
  100 flat miles still does real quad damage, it just isn't the primary limiter here.
- **Replace vert specificity with flat rhythm specificity**: sustained Z2/Z3 flow running on flat
  terrain — exactly what 15-mile rail-trail laps demand.
- **Skip the heat-suit block** — mid-October NH won't be hot; keep passive sauna/hot tub only.
- **Drop hiking specificity** — a flat rail trail is run and walked, not power-hiked.

## What's kept on top of it — gaps the Champion Plan doesn't cover

It's a mountain-ultra plan and says nothing about running through a night or a lapped, crewed
course. Not optional for this race:

- **Night running** — at least 3 sessions, one past 2am, one on already-tired legs, full race kit.
  The single largest gap in the supplied plan for this specific race.
- **Run/walk protocol from session one**, rehearsed in every long run — never introduced for the
  first time on race day.
- **Lap simulations** — 4 × 6km aid segments with crew stops at 12km and 24km, mirroring the real
  course topology.
- **The crew-stop decision tree** and per-lap logistics — see `races/2026-10-17-ghost-train.md`.

## The weekly template

```
Mon — Easy/recovery + heat        | Lower A     (farthest from the long run; Tue is easy, no conflict)
Tue — Easy + 5-6x20-30s hill strides | Upper A  (cheap speed; upper paired with a run day)
Wed — THE BIG WORKOUT             | —           (left clean deliberately)
Thu — X-train 1-2.5h Z2 (meeting) | Lower B     (low-fatigue, runner-specific, non-impact day)
Fri — Rest + heat                 | —           (blackout + full leg recovery before the long run)
Sat — Long run, quality embedded  | —
Sun — Easy/mod flex (run/eMTB/group ride) | Upper B  (Champion's flex day; upper on a run day)
```

Checks this satisfies against `rules/strength-authoring.md`: Lower A sits farthest from the long run
and precedes an easy day; Lower B is low-fatigue and separated from Saturday by a complete rest day;
both upper days fall on running days; Friday is simultaneously the mandated pre-long-run leg
recovery day and the week's one true recovery day; no heavy lower ever precedes Wednesday's workout
or the long run. Meeting walks/rides layer onto any day without displacing anything.

**Known tension:** four 45–60min lifting sessions is 3–4h/week on top of the running budget — more
than the Champion Plan's own lighter post-run routine. The user's strength spec wins that
disagreement, but lifting stays first in the cut order (see `rules/progression.md`) — if the weekly
time-budget check fails repeatedly, drop Upper B before touching anything else.

## Reshaping rules, ordered by impact on the 100-mile outcome

1. **Every week is authored against `athlete/profile.md` time_budget — hard constraint.** Sum
   `duration_s` across the week's endurance files (excluding `concurrent: meetings`) before calling
   a week done.
2. **Back-to-back weekends are the centerpiece.** Saturday long + Sunday medium-long on tired legs —
   the closest available proxy for the back half of a 100-miler, cheaper in family time than one
   monster run. Roughly 3.5–4h Saturday + 2–2.5h Sunday at peak. The long run is normally capped
   at `long_run_max_min`; cumulative weekly volume carries the load, not one long effort.
   **Exception mechanism:** a handful of sessions may exceed the cap, but each must carry an explicit
   `budget_exception: <reason>` in its frontmatter, and no more than
   `long_run_exceptions_per_block` (3) may do so. This keeps "a few long ones are fine" from quietly
   becoming "every long run drifts long" — `scripts/verify_plan.py` enforces both halves. Currently
   1 of 3 is used, by the Big Day.

2b. **Use the course access.** Three sessions are run on the real Ghost Train course — the Big Day
   (wk 13) and both lap simulations (wk 15, wk 17). Everything else stays local. Each on-course
   session costs travel time on top of run time, which the running budget does *not* model, so
   three trips is the deliberate ceiling. Week 16's night long run stays local because its purpose
   (the dark→dawn transition) doesn't need the course.
3. **Convert long runs to time-on-feet at HR/effort**, never a pace target, for anything over ~2h.
4. **Use doubles** (40–50min easy, pre-dawn or post-bedtime) to add volume without a second
   family-disruption block.
5. **Spend meeting time on walking first, trainer second** — see `athlete/profile.md`
   `meeting_budget`. This is the primary answer to the time-on-feet problem and should grow every
   week toward the peak, respecting `weekly_ramp_max_pct`.
6. **Run/walk from session one.** Fix a ratio and use it in every long run so it's automatic under
   fatigue — never introduced for the first time at mile 60.
7. **Night running is mandatory and free** — schedule it after the kids are down; it satisfies a
   non-negotiable race requirement at near-zero family cost.
8. **Two full lap simulations** (24.1km, structured as 4×6km aid segments with crew stops at 12km
   and 24km) in the peak block, rehearsing fueling handoffs, sock/shoe change, and foot care.
9. **Gut training is a training variable** — progress carb intake toward 90–120g/hr on long runs;
   rehearse real food, not only gels (`rules/fueling.md`).
10. **Keep speed work, concentrated into Wednesday** — one big midweek workout plus quality embedded
    in the long run. Progress the easy-pace ceiling per `athlete/zones.yml` and follow the Champion
    Wednesday progression (hills → track/speed → uphill-treadmill threshold → tune-up).
11. **Taper 2–3 weeks** (the seed's weeks 17–19 already trend 23km → 13km → race) but keep one short
    night run in the taper so the circadian rehearsal stays fresh.
12. **Strength runs on the 4-day Upper/Lower spec** (`rules/strength-authoring.md`), placed by the
    weekly template above. Taper Lower A toward Lower B in character in the final 6 weeks; lifting
    is always first in the cut order.

Peak long-run skeleton already in the seed, to convert to time-on-feet targets and build Sunday
back-to-backs onto: 38km (Aug 22), 30km (Aug 29), 42.2km (Sep 5), 20km (Sep 12), 38km (Sep 19),
40km (Sep 26), 23km (Oct 3), 13km (Oct 10).

## Unplanned sessions

Never scheduled in advance — recorded in `log/` after the fact, and the *remainder* of the week
adapts around them:

- **Group road ride** → treat as a threshold session; it replaces (never adds to) that week's second
  quality slot. If it lands Saturday, the Sunday back-to-back becomes easy or a walk.
- **eMTB spin** → treat as active recovery (motor keeps effort dialed down); a legitimate substitute
  for a Monday recovery run.
- Neither counts against the running time budget, but a group ride absolutely counts against
  recovery — that's the point of logging it.
