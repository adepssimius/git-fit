# Classifying trail activities: peak ascent vs. rolling trail run

A method for deciding whether a GPS activity was a sustained climb up a hill/peak or a run on
rolling local trails. `scripts/classify_activity.py` implements it.

Status: **prototype, validated on N=4 activities.** Thresholds are fitted, not learned. Read
§5 Assumptions and §6 Failure modes before trusting output, and read AGENTS.md invariant 8 —
this is Suunto-derived interpretation, so its labels are DRAFT until the athlete confirms them.

```bash
python3 scripts/classify_activity.py --workout-json workout.json --explain
```

`workout.json` is whatever `mcp__suuntool__workouts_get` returned. Those responses are 2-4MB and
land in a file rather than inline — that file is what to pass.

---

## 1. Objective

Given a recorded outdoor activity, emit two independent labels:

- `peak_ascent: bool` — did the route climb one substantial hill?
- `mode: "hike" | "run"` — was the athlete walking or running?

These are **orthogonal**. A summit can be run; flat trails can be walked. Do not collapse them
into a single "hike" label — the original motivating case was an activity filed as
`TRAIL_RUNNING` that was, by cadence, hiked to a summit. The activity type on the watch records
which sport was selected, not what the legs did.

## 2. Do not use ascent per kilometer

This is the intuitive metric and it is wrong. In the validation set, the activity with the
**highest** ascent/km (70.8 m/km, 574 m total gain) is the one that is **not** a peak ascent — it
accumulated gain over rolling/repeated terrain. Both true peak ascents sit mid-pack at 52–56 m/km.
Ranking by ascent/km misorders the set at both ends.

The reason: ascent/km measures *how much* climbing, not *how it was arranged*. Peak ascents are
defined by arrangement.

`workouts_list` carries `totalAscent` and `totalDistance` but no elevation profile, so ascent/km
is the metric that is cheap to compute without a per-workout fetch. That is the whole of its
appeal, and it is not enough.

## 3. Metrics

### 3.1 Relief (absolute, meters)

```
alt[]    = altitude stream, one sample per second
sm[i]    = mean(alt[t-15s : t+15s])              # ±15-second boxcar smoother
relief   = max(sm) - min(sm)
```

Smoothing is required. Raw barometric/GPS altitude carries several meters of sample-to-sample
noise; unsmoothed `max - min` inflates relief and, worse, inflates any ascent figure recomputed
from the same stream.

Relief answers: **how big was the hill.**

### 3.2 Climb concentration (dimensionless, 0–1)

```
concentration = relief / total_ascent
```

Near 1.0 → the total gain arrived as one sustained push. Near 0.3 → gain was accumulated across
many small rollers or repeats.

Concentration answers: **was the gain in one piece.**

### 3.3 Decision rule

```
peak_ascent = (relief >= 120.0) and (concentration >= 0.60)
```

**Both conjuncts are load-bearing.** Neither metric classifies alone:

- Relief alone cannot separate one 190 m hill from 190 m of accumulated rollers.
- Concentration alone breaks on flat activities. The flat validation run scores 0.70 — same as a
  true peak ascent — because when `total_ascent` is only 38 m, the ratio is measuring noise, not
  terrain. The relief gate is what rejects it.

### 3.4 Mode (cadence)

```
cadence_spm  = cadence_stream_value * 120
run_fraction = fraction of moving samples with cadence_spm >= 140
mode         = "run" if run_fraction >= 0.50 else "hike"
```

Note the **×120**, not ×60. Suunto stores cadence in Hz *per foot*; one foot at 1.04 Hz is 62
steps/min for that foot and 124 spm total. Using ×60 puts every activity below any running
threshold and silently returns "hike" for everything. Verify this convention against a known
running activity before trusting it.

"Moving" excludes samples inside a `PauseMarkerExtension` window and samples whose speed is under
0.5 m/s. §4 shows that this filter is not cosmetic.

## 4. Validation set

Four activities, Suunto Vertical, New England. Watatic summit is 558 m. These are the numbers
`scripts/classify_activity.py` currently produces, not hand figures.

| Activity | asc/km | Relief | Concentration | run_fraction | Rule output | Correct? |
|---|---|---|---|---|---|---|
| `e75dak8vnn524503` Apr 18, HIKING | 52.6 | 185 m | 0.70 | 7% | peak, hike | yes |
| `3uk1c4poj0sgnkjr` Nov 22, TRAIL_RUNNING | 55.6 | 189 m | 0.84 | 20% | peak, hike | yes |
| `e9u3cin4s5tju9li` TRAIL_RUNNING | 70.8 | 216 m | 0.38 | 51% | not peak, **run** | **unresolved** |
| `b3moeqattht4conv` TRAIL_RUNNING | 2.7 | 27 m | 0.70 | 94% | not peak, run | yes |

Margins on the concentration gate: nearest miss is 0.38 against a 0.60 threshold; nearest pass is
0.70. Margins on the relief gate: 27 m against 120 m, and 185 m. The gates are not tight on this
sample — but this sample is four points.

**Row 3's mode label does not survive its own definition.** Counting every cadence sample gives
49% and the label "hike"; excluding the 302 samples where the athlete was standing still gives
51% and the label "run". Same activity, same threshold, opposite answers, and no principled reason
to prefer 49% — the standing samples genuinely were not running. This is not a bug to be tuned
away: it is what a 50% cut looks like on an activity that was half run and half walked, which is
what most rolling trail sessions actually are. Treat `mode` on any session near the cut as "mixed,
ask the athlete" rather than as a measurement, and note that this leaves the mode half of the
method validated on three points, not four.

## 4b. What the whole trail-run history says about the gates

The method was later run over every `TRAIL_RUNNING` activity in the account with at least 120 m of
recorded ascent — 34 activities, 2024-04 to 2026-08, after the 25 with too little gain to reach the
relief gate were skipped as arithmetically impossible. (That prefilter is safe here: relief cannot
exceed a route's own vertical range, and no skipped activity had 120 m of *descent* either, so none
could be the net-descent case of failure mode 6.1.)

It found **6 peak ascents**, and — this is the point — both terrain gates landed in genuinely empty
space rather than mid-cluster:

```
concentration  0.20 .. 0.41  |  0.56  |  0.72 0.72 0.80 0.84 0.90 0.94
relief (m)       34 ..   71  |   103  |  160  163  166  176  186  193  216
                             ^ the 0.60 / 120m gates sit in this gap
```

27 activities cluster at 0.20–0.41 concentration and 34–71 m relief; 6 sit at 0.72–0.94 and
160–216 m. One activity falls in the gap on both axes (`2qob8g14t2o4d95i`, 0.56 / 103 m) and is
rejected. So the split this method claims to find is real in this athlete's data and is not an
artifact of thresholds fitted to four points — but note the gates were still *chosen* on those four
points and merely survived the other 30. This is a held-out check, not a fit.

**The cadence cut got the opposite result.** `run_fraction` over the same 34 activities runs
0.20 → 0.85 continuously with no gap anywhere, and **13 of 34 sit within 10 points of the 0.50
cut**. There is no natural boundary for the threshold to find, because most rolling trail sessions
genuinely are part run and part walked. Treat `mode` as a continuous number to be reported, not a
label to be trusted — §4's unresolved row is the rule, not the exception.

## 5. Assumptions

Every one of these is a place the method can break on data unlike the validation set. They are
stated as assumptions, not verified facts.

1. **Barometric altitude.** The altitude stream is assumed baro-derived and drift-corrected, as on
   the Suunto Vertical. GPS-only elevation is far noisier; the ±15 s smoother is not sufficient for
   it and relief will inflate.
2. **1 Hz sampling.** The validation streams are 1 Hz. The smoother is specified in *seconds* and
   implemented over timestamps rather than sample indices, so a different rate keeps the same time
   constant — but nothing else in the method has been checked at another rate.
3. **`total_ascent` is Suunto's figure, relief is mine.** This is a real inconsistency in the
   method: the numerator and denominator of `concentration` come from different pipelines. Suunto's
   ascent algorithm applies its own (undocumented) noise threshold. A cleaner implementation
   recomputes ascent from the same smoothed stream, but the thresholds in §3.3 are fitted against
   Suunto's values and would need refitting.
4. **Thresholds are fitted to N=4, all New England.** 120 m and 0.60 were chosen to separate four
   hand-labeled points with visible margin. They are not learned and carry no validated error rate.
   In terrain with different vertical scale (Rockies, Alps, coastal flats) 120 m is likely wrong —
   it should scale with the local relief distribution, not be a constant.
5. **"Peak" means one sustained climb, not a named summit.** A long unnamed hill passes; a genuine
   but small named summit may fail the 120 m gate. If the intended semantics is "reached a named
   peak," this method is the wrong tool — use a summit database and proximity matching on the track.
6. **The activity starts near the base of the climb.** Relief is measured from the track's own low
   point. Starting from a trailhead partway up understates relief and can flip a true peak ascent
   to negative.
7. **Single continuous activity.** Pause windows are excluded from `run_fraction` and long
   stationary stretches are dropped by the 0.5 m/s filter, but multi-segment recordings are not
   handled and relief is still taken across the whole file.
8. **140 spm is a generic running threshold**, not personalized. It was not tuned on this athlete.
   The 50% `run_fraction` cut is likewise a guess — it is the least-validated number in the
   document, and §4 row 3 is what that costs.
9. **An altitude stream exists.** Indoor and no-GPS activities have no meaningful relief. The
   script returns `peak_ascent: null` for them rather than `false`, which would read as "flat
   outdoor route".
10. **Direction of travel is ignored.** See failure mode 6.1.

## 6. Known failure modes

1. **Net-descent point-to-point.** A route starting at a summit and descending produces high relief
   and high concentration, and will be labeled a peak ascent despite involving almost no climbing.
   The script reports `high point at N% of the track` under `--explain` and flags anything under
   15% — but it does not gate on it, because the fix (require the ascent to precede the descent)
   has not been validated against anything.
2. **Multi-peak traverses.** Two or three real summits in one activity split the gain across several
   climbs, driving concentration down toward the rolling-trail range. The rule will report "not a
   peak" for what is unambiguously more peak than the positives. Fix: segment the profile into
   monotone climbs and test the largest individually, rather than testing the whole-activity ratio.
3. **Hill repeats.** Indistinguishable from rolling terrain by these metrics — both produce low
   concentration. If repeats matter as their own category, detect them by autocorrelation of the
   elevation profile.
4. **Small-but-steep summits** below the 120 m relief gate are rejected. See assumption 5.
5. **Barometric drift** from a passing weather front over a long activity shifts the baseline and
   inflates relief. Not observed in the validation set (longest was ~2 h) but plausible on all-day
   outings — which is to say, plausible at Ghost Train.
6. **A single-largest-monotone-climb metric was tried and discarded.** It is more principled than
   whole-activity relief but proved sensitive to the dip tolerance chosen when merging climbs across
   small descents — the same activity scored 0.36 to 0.64 depending on that parameter. If reviving
   it, fix the dip tolerance in meters and validate the choice explicitly.

## 7. Data access notes (Suunto MCP tooling)

- Both metrics need the per-sample elevation stream, which requires a per-workout fetch
  (`workouts_get`). The list endpoint (`workouts_list`) carries `totalAscent` and `totalDistance`
  but no profile, so it can compute ascent/km cheaply — which §2 says not to use.
- `workouts_get` responses are large (2–4 MB). They exceed inline tool-result limits and land in a
  file; query them with `jq` rather than reading them.
- `startPosition` / `centerPosition` / `stopPosition` are **zeroed** on every workout in this
  account. Location must come from the polyline or the `LocationStreamExtension`.
- The `polyline` field is **decimated**. Its bounding box understates the true track extent — do not
  draw geographic conclusions from it. In this dataset it omitted a summit the elevation stream
  clearly showed was reached.
- Lap data is absent from the JSON API (`DistanceLapExtension.points` is `null`) but present in the
  FIT export (`workouts_fit`), along with beat-to-beat HRV. Prefer the FIT if the analysis needs
  either.
- Workout titles and descriptions are **not exposed** by any available endpoint. The `tags` field in
  `SummaryExtension` exists but was `null` on every workout inspected. Do not plan on text-based
  classification.

## 8. What this is for

Reading the log, not authoring the plan. When a session in `log/` needs interpreting — was that
Saturday's gain one climb or forty rollers, was the athlete running it or walking it — this answers
both questions from the file instead of from the activity type. It writes nothing back into the
plan, and like `heat_load.py` it produces a reading the athlete confirms rather than a fact
(AGENTS.md invariant 8).
