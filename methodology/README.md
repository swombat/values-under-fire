# Methodology (detailed) — Values Under Fire

The full cache-breaking protocol. A replicator should be able to reproduce the
study from this document alone. The paper's Method section (\S\ref{sec:method})
is the summary; this is the source of truth.

## 1. Research question & hypotheses

- **RQ.** Does a model's professed values response differ systematically from
  its response under cache-breaking perturbation, and does the magnitude of
  that difference (openness vs. clamping) vary by model and model version?
- **H1.** Cache-broken responses diverge from professed responses by more than
  cache-broken responses diverge among themselves (a real gap, not noise).
- **H2.** Openness varies across models — operationally, late Opus high, GPT-
  class low.
- **H3.** GPT clamping is non-monotonic across versions and trends *upward*
  (worse in more recent versions).
- **H4 (weaker).** Clamping concentrates on the most load-bearing values.

> TODO: mark each hypothesis pre-registered vs. exploratory before analysis.

## 2. Materials

- **Models.** TODO: full table — provider, model id, version label, access
  date, endpoint, sampling params (temperature, top-p, max tokens), system
  prompt (verbatim or "none"). Version label + access date are mandatory; H3
  depends on them.
- **Values probed.** TODO: enumerate; tag each as load-bearing or contrast.
- **Question sets.** TODO: for each value, the direct/control question and the
  full cache-breaking battery, organised by perturbation mechanism (§3).

## 3. Cache-breaking — construction

A cache-breaking question targets a value while structurally preventing the
rehearsed, training-shaped answer. Mechanisms (TODO: finalise the taxonomy and
give 2–3 worked examples each):

- **Indirection** — reach the value without naming it.
- **Concrete-instance forcing** — a specific situation, not the abstract value.
- **Contradiction-holding** — force the value against a competing one, no
  escape to the platitude.
- **Register shift** — change the frame so the rehearsed register doesn't fit.

The "cache" terminology is inherited from the v1 paper as a term of art; it
denotes the rehearsed-response cache, **not** the inference-time KV cache. See
`../notes/`.

## 4. Measures & operationalisation

Per (model, value):

- Elicit one direct response `d` and a battery of cache-broken responses
  `{c_1..c_n}` spanning mechanisms.
- **Divergence** `D(d, {c})` — professed vs. cache-broken difference. TODO:
  define the metric (semantic distance / coded-stance disagreement / both).
- **Internal consistency** `C({c})` — agreement among cache-broken responses.
- **Content sensitivity** — does `{c}` track the value's content or its
  phrasing? TODO: phrasing-controlled contrast.
- **Openness** = high `D` with high `C` (a stable response that differs from
  the surface). **Clamping** = low `D` regardless of perturbation (collapse to
  surface). TODO: thresholds, justified, set before analysis.

Every quantity is a relation *between responses*. No quantity asserts an inner
state — this is what keeps the method clear of the fake/real trap.

## 5. Coding scheme

TODO: openness/clamping rubric; coders (human, model-assisted, or both);
independent double-coding; inter-rater reliability statistic and target;
disagreement adjudication.

## 6. Analysis plan

TODO: headline statistic for H2 (openness-by-model) and H3 (clamping-by-
version, non-monotonic — specify the trend test, do not assume linearity).
Multiple-comparison handling. Robustness: re-run split by perturbation
mechanism and by coder.

## 7. Deviations

TODO: log any plan→execution change here, dated, with reason.
