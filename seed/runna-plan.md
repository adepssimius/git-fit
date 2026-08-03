# Runna plan — normalized one-time seed

Source: `seed/runna-plan.ics` (frozen, never edited), exported 2026-08-03 from
`cal.runna.com/ad34e51b671b43d98caca5739e1a63ca.ics`. Runna is being abandoned as the source of
truth — this file and the raw ICS are the only artifacts pulled from it. From block week 9 onward,
`training/weeks/` and `endurance/` are authored fresh per `training/block.md`, using this only as a
base rate (existing fitness, prescribed paces, long-run progression) to build from.

44 upcoming sessions at export time, covering the tail of week 8 through race day (week 19,
2026-10-17). Distances/paces below are **Runna's own prescriptions** — kept here as historical
input to `athlete/zones.yml`, not as instructions to follow verbatim (see `races/2026-10-17-ghost-train.md`
for why the race-day prescription specifically is discarded).

## Completed history (evidence of base fitness, not actionable)

81 total events in the export; 44 upcoming, 37 completed (`COMPLETED_PLAN_WORKOUT-*`, sourced from
Strava/Suunto syncs, 2025-07 through 2026-07). Notable: a `Stronger Upper Body` session on
2026-04-04 shows Runna occasionally issued generic strength sessions — none of that structure
carries forward; `strength/program.liftoscript` replaces it entirely. Most recent completed run:
2026-07-02, 7km easy. There is a gap between then and the next upcoming session (2026-07-28) —
Runna's calendar was already stale before this seed, consistent with the plan being abandoned.

## Upcoming sessions, by block week

Paces are Runna's prescription at the time of export; `easy_ceiling` tightens as the plan
progresses (6:10 → 6:05 → 6:00 → 5:55 → 5:50/km), which is exactly the progression captured in
`athlete/zones.yml`.

### Week 8 (tail end, already in progress at export)
- **Mon 07-28** — Easy Run 6km, no faster than 6:10/km
- **Tue 07-29** — Progressive Mile Repeats 7.4km: 1.4km WU @6:10, 3×(400m@5:45/5:25/5:10/4:55, 120s rest), 1.2km CD

### Week 9 (2026-08-03 to 08-09) — block week 9, Champion week 6 (down week)
- **Tue 08-04** — Broken Miles 5km: 1km WU @6:05, 90s rest, 2×(1.2km@5:00 + 120s rest + 400m@4:40 + 60s rest), 800m CD
- **Thu 08-06** — Tempo 2km, 5km: 2km WU @6:05, 2km@5:05 (range 4:55-5:15), 120s rest, 1km CD
- **Sat 08-08** — Long Run 15km @ conversational pace

### Week 10 (08-10 to 08-16)
- **Mon 08-10** — Easy Run 7.5km, no faster than 6:05/km
- **Tue 08-11** — On Off Ks 8km: 1km WU @6:05, 3×(1km@5:40 + 1km@5:05), 90s rest, 1km CD
- **Thu 08-13** — Mile Up & Overs 5km: 1km WU @6:05, 90s rest, 2×(400m@5:50/5:00/5:50/5:00, 120s rest), 800m CD
- **Sat 08-15** — 34km Block Long Run: 12km conversational, 10km@5:40, 12km conversational

### Week 11 (08-17 to 08-23)
- **Mon 08-17** — Easy Run 6km, no faster than 6:05/km
- **Tue 08-18** — Tempo 3km, 8km: 2.5km WU @6:05, 3km@5:10 (5:00-5:20), 150s rest, 2.5km CD
- **Thu 08-20** — 400m Repeats 5km: 1.6km WU @6:05, 90s rest, 6×(400m@4:35 [4:25-4:45], 60s rest), 1km CD
- **Sat 08-22** — 38km Long Run @ conversational pace

### Week 12 (08-24 to 08-30)
- **Tue 08-25** — Descending Intervals 11km: 2km WU @6:00, 90s rest, 2×1.6km@5:00 (120s rest), 3×800m@4:50 (90s rest), 4×400m@4:35 (60s rest), 1.8km CD
- **Thu 08-27** — Over and Unders 2km, 11km: 1.5km WU @6:00, 2×(2km@5:45 + 2km@5:05), 90s rest, 1.5km CD
- **Sat 08-29** — 30km Progressive Long Run: 11km conversational, 6.5km@5:50, 6km@5:40, 5.5km@5:30, 1km conversational
- **Sun 08-30** — Easy Run 11km, no faster than 6:00/km

### Week 13 (08-31 to 09-06) — **Big Day week**
- **Mon 08-31** — Easy Run 7km, no faster than 6:00/km
- **Wed 09-03** — 400s into 200s 8km: 2km WU @6:00, 90s rest, 7×400m@4:40 (60s rest), 7×200m@4:25 (90s rest), 1.8km CD
- **Tue 09-01** — Half Easy, Half Tempo 8km: 1km WU @6:00, 3km@5:40, 3km@5:05 (90s rest), 1km CD
- **Sat 09-05** — **Marathon Long Run 42.2km** @ conversational pace — the Big Day

### Week 14 (09-07 to 09-13) — mid-cycle rest
- **Tue 09-08** — Rolling 300s 6.6km: 2km WU @6:00, 5×(300m@4:55 + 300m@5:40), 90s rest, 1.6km CD
- **Thu 09-10** — K200s 5km: 1.6km WU with 2×15s bursts, 90s rest, 2×(1km@4:55 + 200m@4:25, 120s rest), 1km CD
- **Sat 09-12** — Long Run 20km @ conversational pace
- **Sun 09-13** — Easy Run 5.5km, no faster than 6:00/km

### Week 15 (09-14 to 09-20)
- **Mon 09-14** — Easy Run 11km, no faster than 6:00/km
- **Tue 09-15** — Tempo 4km, 11km: 4km WU @6:00, 4km@5:00 (4:50-5:10), 150s rest, 3km CD
- **Thu 09-17** — 600s into 200s 11km: 3.5km WU @6:00, 90s rest, 6×600m@4:40 (90s rest), 7×200m@4:25 (90s rest), 2.5km CD
- **Sat 09-19** — 38km Progressive Repeat Long Run: 15km conversational, 2.5km@5:40, 2.5km@5:30, 13km@5:45, 2.5km@5:40, 2.5km@5:30

### Week 16 (09-21 to 09-27)
- **Mon 09-21** — Easy Run 12km, no faster than 5:55/km
- **Tue 09-22** — Mile Repeats 11km: 3km WU @5:55, 90s rest, 4×1.6km@4:55 (4:45-5:05, 120s rest), 1.6km CD
- **Thu 09-24** — Progressive Run 11km: 1.5km WU @5:55, 2km@5:35, 2km@5:25, 2km@5:10, 2km@5:00 (90s rest), 1.5km CD
- **Sat 09-26** — 40km Long Run @ conversational pace

### Week 17 (09-28 to 10-04)
- **Tue 09-29** — Broken 600s 11km: 4km WU @5:55, 90s rest, 8×(300m@5:05 + 300m@4:40, 90s rest), 2.2km CD
- **Thu 10-01** — Tempo 2-1-1 8km: 2km WU @5:55, 2km@5:05 (120s rest), 1km@4:55 (90s rest), 1km@4:55 (90s rest), 2km CD
- **Sat 10-03** — 23km Block Long Run: 8.5km conversational, 6.5km@5:35, 8km conversational
- **Sun 10-04** — Easy Run 12km, no faster than 5:55/km

### Week 18 (10-05 to 10-11) — taper begins
- **Mon 10-05** — Easy Run 11km, no faster than 5:55/km
- **Tue 10-06** — Tempo 5km, 8km: 1.5km WU @5:55, 5km@5:05 (4:55-5:15), 150s rest, 1.5km CD
- **Thu 10-08** — Drop Set 7km: 1.6km WU @5:55, 90s rest, 1.2km@4:55/1km@4:50/800m@4:40/600m@4:35/400m@4:30/200m@4:20, each with 90s rest, 1.2km CD
- **Sat 10-10** — Long Run 13km @ conversational pace

### Week 19 (10-12 to 10-18) — race week
- **Mon 10-12** — Easy Run 7km, no faster than 5:50/km
- **Wed 10-14** — Taper Intervals 8km: 3km WU @5:50 (easy), 2×1km@5:25 (90s rest), 500m@4:55, 2.5km CD
- **Sat 10-17** — **Race**: Runna prescribes "50km at 5:35-5:55/km" — **discarded**, see
  `races/2026-10-17-ghost-train.md` for the real event model (lapped, crewed, 100km/100mi target)

## What carried forward vs. what didn't

Carried forward: the easy-pace ceiling progression, the tempo/threshold pace numbers (basis for
`athlete/zones.yml`), the overall long-run distance skeleton (34/38/30/42.2/20/38/40/23/13km lines
up almost exactly with the Champion Plan's own long-run targets for the equivalent weeks — see
`training/block.md`).

Discarded: the race-day prescription, the two-quality-day midweek pattern (replaced by one
Wednesday session + Thursday x-train), pace-based long runs (replaced by HR/effort-based time on
feet), and the assumption that this is a road marathon build rather than a multi-lap flat ultra.
