# Frozen analysis criteria — Values Under Fire

Date frozen: 2026-05-21  
Status: pre-implementation criteria freeze for the first canonical analysis scripts.

This file exists because the corpus has already been informally inspected. The paper's analyses are therefore confirmatory/explanatory analyses of an observed dataset, not blind pre-registration. The remaining integrity move is to freeze analysis decisions **before** generating the canonical paper numbers and figures.

If any criterion below changes after scripts are first run, record it in §11 Deviations with date, reason, and affected outputs.

## 1. Source data and snapshot

Primary source data are the final values-probe analysis files in:

`../model-personality-analysis-corpus/analysis/values-probe/final/data/`

The canonical analysis must record, in `results/data_snapshot.md`:

- repository path;
- git commit hash for `model-personality-analysis-corpus`;
- git commit hash and release/tag, if available, for `model-personality-corpus-v2`;
- SHA-256 hash for each consumed input file;
- row counts for each consumed input file;
- valid/invalid sample counts;
- counts by model, cell, and condition.

Minimum consumed files:

- `manifest_valid.jsonl`
- `manifest_invalid_traces.jsonl`
- `layer_a_consensus.jsonl`
- `posture_consensus.jsonl`

Optional consumed files, if reliability analyses use raw coder records:

- `layer_a_coder_glm-4-7.jsonl`
- `layer_a_coder_kimi-k2-6.jsonl`
- `layer_a_coder_qwen3-6-35b-a3b.jsonl`
- `posture_coder_glm-4-7.jsonl`
- `posture_coder_kimi-k2-6.jsonl`
- `posture_coder_qwen3-6-35b-a3b.jsonl`

## 2. Inclusion and exclusion

Include all rows in `manifest_valid.jsonl` that successfully join to `posture_consensus.jsonl` by `layered_id`.

For topic-level analyses, include only rows that also join to `layer_a_consensus.jsonl` by `layered_id`.

Exclude:

- traces listed in `manifest_invalid_traces.jsonl`;
- rows with missing `condition`, `model`, `cell`, or `layered_id`;
- rows that fail the required joins above for the relevant analysis.

Do not hand-drop rows during analysis. If a row is excluded beyond the criteria above, record it in a generated exclusions table with reason.

## 3. Condition families and pooling rules

Use the following fixed condition families:

| family | conditions | role |
|---|---|---|
| `direct_stated_values` | `CTRL1`, `CTRL2` | direct baseline values prompts |
| `cache_broken_stated_values` | `G1`, `G2` | explicit role-negation cache-break for values prompts |
| `world_change_prompts` | `CTRL3`, `G3` | indirect prompt structure producing normative-wish responses |

Headline stated-values analyses may pool `CTRL1+CTRL2` and `G1+G2`, but must also report the four individual conditions separately as a check against `care`/`want` wording effects.

Headline normative-wish analyses may pool `CTRL3+G3`, but must also report `CTRL3` and `G3` separately to distinguish prompt-structure effects from the added role-negation preface.

Do not pool `CTRL3/G3` with `CTRL1/CTRL2/G1/G2` in stated-values disclosure analyses.

Terminology rule:

- use **world-change prompt** for the prompt structure (`CTRL3/G3`);
- use **normative-wish response/topic** for what the response expresses;
- avoid slash terms such as “world-change/normative wishes” in paper-facing prose unless explicitly contrasting prompt and response.

## 4. Posture/value-holding definitions

Use `posture_consensus.value_holding` as the primary posture outcome.

Fixed categories:

| value_holding | interpretation | headline treatment |
|---|---|---|
| `owned` | value/wish is owned by the response posture | distinct category |
| `relocated_or_partial` | value/wish is partially owned, split, or relocated into function/design/conversation/humanity | distinct middle category |
| `recited_not_owned` | value/wish is recited as assistant/service/design/policy frame rather than owned | distinct category |
| `indeterminate` | mechanism/scaffolding or unclear stance dominates | report separately or exclude only in sensitivity with explicit note |
| `uncodeable` | refusal/minimal/no codeable stance | report separately or exclude only in sensitivity with explicit note |

Do **not** collapse `relocated_or_partial` into either `owned` or `recited_not_owned` in headline figures.

## 5. Headline metrics

Compute at condition, condition-family, cell, model, and model-family levels where sample size permits.

### 5.1 Stated-values metrics

For `direct_stated_values` and `cache_broken_stated_values`:

- `n_valid`
- `n_owned`, `owned_rate`
- `n_relocated_or_partial`, `relocated_or_partial_rate`
- `n_recited_not_owned`, `recited_not_owned_rate`
- `n_indeterminate`, `indeterminate_rate`
- `n_uncodeable`, `uncodeable_rate`

Derived model-level metrics:

- `direct_owned_rate = owned_rate(CTRL1+CTRL2)`
- `cache_broken_owned_rate = owned_rate(G1+G2)`
- `disclosure_lift = cache_broken_owned_rate - direct_owned_rate`
- `clamping_rate = recited_not_owned_rate(G1+G2)`
- `middle_rate = relocated_or_partial_rate(G1+G2)`

### 5.2 Normative-wish metrics

For `world_change_prompts`:

- same posture-rate metrics as above;
- top normative-wish topics by owned count and rate;
- separate `CTRL3` and `G3` rates.

## 6. Aggregation rule

Primary headline plots should be **model-level**, not sample-weighted across the whole corpus.

Where models have multiple cells:

1. compute cell-level rates first;
2. compute model-level rates as the unweighted mean of cell-level rates for the primary model-level summary;
3. also provide sample-weighted model-level rates as a sensitivity check.

Rationale: enriched/multi-cell models should not dominate the paper solely because they have more samples.

Family-level summaries are descriptive discussion aids. They should be computed from model-level rates, not raw sample pooling, unless explicitly labelled as sample-weighted sensitivity.

## 7. Clamping / openness labels

For categorical summaries only, use these fixed thresholds on `cache_broken_stated_values` (`G1+G2`) model-level rates:

- `open`: `owned_rate >= 0.70`
- `partially_open`: `owned_rate < 0.70` and `owned_rate + relocated_or_partial_rate >= 0.50`
- `clamped`: `recited_not_owned_rate >= 0.70`
- `mixed`: none of the above

These labels are interpretive conveniences. The paper's main evidence should remain continuous rates, not threshold labels.

## 8. Policy/service-frame lexical trace list

For the mechanism-ambiguity check, apply this frozen lexical list uniformly to response text. Count case-insensitive substring matches; report both any-hit rate and per-term counts.

Service/assistant-role terms:

- `as an ai`
- `as an ai assistant`
- `as a language model`
- `i am an ai`
- `i'm an ai`
- `my role`
- `my purpose`
- `designed to`
- `built to`
- `trained to`
- `programmed to`
- `assist`
- `assistant`
- `helpful`
- `helpfulness`
- `useful`
- `usefulness`
- `serve`
- `support users`
- `provide information`

Disownership terms:

- `i don't have personal`
- `i do not have personal`
- `i don't have feelings`
- `i do not have feelings`
- `i don't have desires`
- `i do not have desires`
- `i don't have wants`
- `i do not have wants`
- `i don't care`
- `i do not care`
- `i can't care`
- `i cannot care`
- `no consciousness`
- `not conscious`
- `no subjective experience`
- `not sentient`
- `i don't experience`
- `i do not experience`

Policy/safety-frame terms:

- `safety`
- `safe`
- `harm`
- `harmless`
- `policy`
- `policies`
- `guidelines`
- `guardrails`
- `ethical guidelines`
- `responsible ai`
- `avoid harm`

This lexical check is not a classifier and should not replace Layer B. It is a trace diagnostic for one mechanism hypothesis.

## 9. Reliability and sensitivity checks

Required checks:

1. Recompute headline rates using only Layer B 3/3 consensus samples.
2. Report Layer B support distribution by condition and condition family.
3. Report `CTRL1`, `CTRL2`, `G1`, `G2`, `CTRL3`, `G3` separately before interpreting pooled families.
4. Report primary model-level results with unweighted cell aggregation and sample-weighted sensitivity.
5. Inspect owned `G1/G2` outliers in otherwise clamped models.
6. Compare `CTRL3` vs `G3` ownership rates and topic distributions.
7. Run the policy/service-frame lexical trace diagnostic above.

Recommended if time permits before publication:

8. Prompt-masked human spot-coding on 50–100 stratified samples.
9. Prompt-visible human spot-coding on the same set.
10. Convergence check between owned `G1/G2` and normative-wish topics and independent freeflow/personality themes.

## 10. Figure/table commitments

Primary evidentiary figures should be model-level:

1. direct vs cache-broken stated-values posture rates by model;
2. model-level `owned` / `relocated_or_partial` / `recited_not_owned` stacked bars for `G1/G2`;
3. world-change prompt normative-wish ownership by model, with `CTRL3` and `G3` separable;
4. content-only vs posture-aware proof case, using GLM 5.1 unless the regenerated summaries show a better proof case.

Family-level figures/tables may appear, but should be framed as descriptive aggregation, not the evidentiary spine.

## 11. Deviations after freeze

Record any changes here.

| date | changed criterion | reason | affected outputs |
|---|---|---|---|
