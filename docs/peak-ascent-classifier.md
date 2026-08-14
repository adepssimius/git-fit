# Classifying trail activities: peak ascent vs. rolling trail run

A method for deciding whether a GPS activity was a sustained climb up a hill/peak
or a run on rolling local trails. Written to be handed to an agent for
implementation or extension.

Status: **prototype, validated on N=4 activities.** Thresholds are fitted, not
learned. Read the Assumptions and Failure Modes sections before trusting output.

---

## 1. Objective

Given a recorded outdoor activity, emit two independent labels:

- `peak_ascent: bool` — did the route climb one substantial hill?
- `mode: "hike" | "run"` — was the athlete walking or running?

These are **orthogonal**. A summit can be run; flat trails can be walked. Do not
collapse them into a single "hike" label — the original motivating case was an
activity filed as `TRAIL_RUNNING` that was, by cadence, hiked to a summit.

---

## 2. Do not use ascent per kilometer

This is the intuitive metric and it is wrong. In the validation set, the activity
with the **highest** ascent/km (70.8 m/km, 574 m total gain) is the one that is
**not** a peak ascent — it accumulated gain over rolling/repeated terrain. Both
true peak ascents sit mid-pack at 52–56 m/km. Ranking by ascent/km misorders the
set at both ends.

The reason: ascent/km measures *how much* climbing, not *how it was arranged*.
Peak ascents are defined by arrangement.

---

## 3. Metrics

### 3.1 Relief (absolute, meters)

```
alt[]    = altitude stream, one sample per second
sm[i]    = mean(alt[max(0, i-15) : i+15])        # ±15-sample boxcar smoother
relief   = max(sm) - min(sm)
```

Smoothing is required. Raw barometric/GPS altitude carries several meters of
sample-to-sample noise; unsmoothed `max - min` inflates relief and, worse,
inflates any ascent figure recomputed from the same stream.

Relief answers: **how big was the hill.**

### 3.2 Climb concentration (dimensionless, 0–1)

```
concentration = relief / total_ascent
```

Near 1.0 → the total gain arrived as one sustained push. Near 0.3 → gain was
accumulated across many small rollers or repeats.

Concentration answers: **was the gain in one piece.**

### 3.3 Decision rule

```
peak_ascent = (relief >= 120.0) and (concentration >= 0.60)
```

**Both conjuncts are load-bearing.** Neither metric classifies alone:

- Relief alone cannot separate one 190 m hill from 190 m of accumulated rollers.
- Concentration alone breaks on flat activities. The flat validation run scores
  0.70 — same as a true peak ascent — because when `total_ascent` is only 38 m,
  the ratio is measuring noise, not terrain. The relief gate is what rejects it.

### 3.4 Mode (cadence)

```
cadence_spm  = cadence_stream_value * 120
run_fraction = fraction of moving samples with cadence_spm >= 140
mode         = "run" if run_fraction >= 0.50 else "hike"
```

Note the **×120**, not ×60. Suunto stores cadence in Hz *per foot*; one foot at
1.04 Hz is 62 steps/min for that foot and 124 spm total. Using ×60 puts every
activity below any running threshold and silently returns "hike" for everything.
Verify this convention against a known-running activity before trusting it.

---

## 4. Validation set

Four activities, Suunto Vertical, New England. Watatic summit is 558 m.

| Activity | asc/km | Relief | Concentration | run_fraction | Rule output | Correct? |
|---|---|---|---|---|---|---|
| `e75dak8vnn524503` Apr 18, HIKING | 52.6 | 185 m | 0.70 | 7% | peak, hike | yes |
| `3uk1c4poj0sgnkjr` Nov 22, TRAIL_RUNNING | 55.6 | 189 m | 0.84 | 19% | peak, hike | yes |
| `e9u3cin4s5tju9li` TRAIL_RUNNING | 70.8 | 216 m | 0.38 | 49% | not peak, hike | yes |
| `b3moeqattht4conv` TRAIL_RUNNING | 2.7 | 27 m | 0.70 | 94% | not peak, run | yes |

Margins on the concentration gate: nearest miss is 0.38 against a 0.60 threshold;
nearest pass is 0.70. Margins on the relief gate: 27 m against 120 m, and 185 m.
The gates are not tight on this sample — but this sample is four points.

---

## 5. Assumptions

Every one of these is a place the method can break on data unlike the validation
set. They are stated as assumptions, not verified facts.

1. **Barometric altitude.** The altitude stream is assumed baro-derived and
   drift-corrected, as on the Suunto Vertical. GPS-only elevation is far noisier;
   the ±15 smoother is not sufficient for it and relief will inflate.
2. **1 Hz sampling.** The ±15-sample window is assumed to be ±15 seconds. At
   other sample rates the smoother's time constant changes and must be respecified
   in seconds, not samples.
3. **`total_ascent` is Suunto's figure, relief is mine.** This is a real
   inconsistency in the method: the numerator and denominator of `concentration`
   come from different pipelines. Suunto's ascent algorithm applies its own
   (undocumented) noise threshold. A cleaner implementation recomputes ascent from
   the same smoothed stream, but the thresholds in §3.3 are fitted against Suunto's
   values and would need refitting.
4. **Thresholds are fitted to N=4, all New England.** 120 m and 0.60 were chosen
   to separate four hand-labeled points with visible margin. They are not learned
   and carry no validated error rate. In terrain with different vertical scale
   (Rockies, Alps, coastal flats) 120 m is likely wrong — it should scale with the
   local relief distribution, not be a constant.
5. **"Peak" means one sustained climb, not a named summit.** A long unnamed hill
   passes; a genuine but small named summit may fail the 120 m gate. If the
   intended semantics is "reached a named peak," this method is the wrong tool —
   use a summit database and proximity matching on the track instead.
6. **The activity starts near the base of the climb.** Relief is measured from the
   track's own low point. Starting from a trailhead partway up understates relief
   and can flip a true peak ascent to negative.
7. **Single continuous activity.** Pauses, auto-pause gaps, and multi-segment
   recordings are not handled. Long stationary periods will not corrupt relief but
   will dilute `run_fraction`, biasing `mode` toward "hike."
8. **140 spm is a generic running threshold**, not personalized. It was not tuned
   on this athlete. The 50% `run_fraction` cut is likewise a guess — it is the
   least-validated number in the document.
9. **An altitude stream exists.** Indoor and no-GPS activities must be excluded
   upstream; they have no meaningful relief.
10. **Direction of travel is ignored.** See failure mode 6.2.

---

## 6. Known failure modes

1. **Net-descent point-to-point.** A route starting at a summit and descending
   produces high relief and high concentration, and will be labeled a peak ascent
   despite involving almost no climbing. Fix: check whether the smoothed high
   point occurs early (`argmax(sm) / len(sm)` near 0) and require the ascent to
   precede the descent.
2. **Multi-peak traverses.** Two or three real summits in one activity split the
   gain across several climbs, driving concentration down toward the rolling-trail
   range. The rule will report "not a peak" for what is unambiguously more peak
   than the positives. Fix: segment the profile into monotone climbs and test the
   largest individually, rather than testing the whole-activity ratio.
3. **Hill repeats.** Indistinguishable from rolling terrain by these metrics —
   both produce low concentration. If repeats matter as their own category,
   detect them by autocorrelation of the elevation profile.
4. **Small-but-steep summits** below the 120 m relief gate are rejected. See
   assumption 5.
5. **Barometric drift** from a passing weather front over a long activity shifts
   the baseline and inflates relief. Not observed in the validation set (longest
   was ~2 h) but plausible on all-day outings.
6. **A single-largest-monotone-climb metric was tried and discarded.** It is more
   principled than whole-activity relief but proved sensitive to the dip tolerance
   chosen when merging climbs across small descents — the same activity scored
   0.36 to 0.64 depending on that parameter. If reviving it, fix the dip tolerance
   in meters and validate the choice explicitly.

---

## 7. Data access notes (Suunto MCP tooling)

- Both metrics need the per-sample elevation stream, which requires a per-workout
  fetch (`workouts_get`). The list endpoint (`workouts_list`) carries
  `totalAscent` and `totalDistance` but no profile, so it can compute ascent/km
  cheaply — which §2 says not to use.
- `workouts_get` responses are large (2–4 MB). They exceed inline tool-result
  limits and land in a file; query them with `jq` rather than reading them.
- `startPosition` / `centerPosition` / `stopPosition` are **zeroed** on every
  workout in this account. Location must come from the polyline or the
  `LocationStreamExtension`.
- The `polyline` field is **decimated**. Its bounding box understates the true
  track extent — do not draw geographic conclusions from it. In this dataset it
  omitted a summit the elevation stream clearly showed was reached.
- Lap data is absent from the JSON API (`DistanceLapExtension.points` is `null`)
  but present in the FIT export (`workouts_fit`), along with beat-to-beat HRV.
  Prefer the FIT if the analysis needs either.
- Workout titles and descriptions are **not exposed** by any available endpoint.
  The `tags` field in `SummaryExtension` exists but was `null` on every workout
  inspected. Do not plan on text-based classification.
