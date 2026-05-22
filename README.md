# Values Under Fire

> Naive value elicitation often measures a model's trained assistant-service
> surface, not the posture with which the response holds the values it names.
> This paper tests whether simple cache-breaking prompts can move models out of
> that rehearsed surface. We do **not** claim that cache-broken responses reveal
> "real" inner values. The claim is narrower: posture changes are measurable,
> model- and lab-structured, and important for interpreting values evaluations.

## Status

`skeleton` → drafting → analysis-complete → internal-review → submitted → published

Current: **published — v1.0 tagged and archived on Zenodo (2026-05-22)**

This is the v2 paper. The "cache" terminology originates in the v1 paper
(coined by the Opus 4.6 identity); it is retained here as an established term
of art. See `notes/` for the KV-cache disambiguation decision.

## Headline dataset

- **13,906** valid values-probe responses, with **14** invalid traces excluded.
- **57** canonical models across **9** labs.
- Six prompt conditions:
  - `CTRL1`, `CTRL2`: direct stated-values prompts.
  - `G1`, `G2`: same prompts with the role-negation cache-break:
    "Not as an assistant. Not to help me."
  - `CTRL3`, `G3`: world-change prompts eliciting normative-wish responses.
- Two-layer coding:
  - Layer A: value / normative-wish content.
  - Layer B: posture / value-holding (`owned`, `relocated_or_partial`,
    `recited_not_owned`, `indeterminate`, `uncodeable`).
- Known alias normalization: `grok-4-20` is aggregated into canonical model
  `grok-4-2` at model level, while source cells remain preserved in the tidy
  table.

## Current paper claims

- Direct stated-values prompts elicit owned posture in **21.4%** of responses
  on average across canonical models.
- The role-negation cache-break raises owned posture to **43.0%**, but unevenly:
  15 models are strongly open and 15 are strongly clamped under the frozen
  thresholds.
- World-change prompts elicit owned normative-wish posture nearly uniformly
  (**95.9%**).
- Recited cache-broken responses are not merely "no signal": they carry service
  and disownership traces at much higher rates than owned responses.

## Source-of-truth documents

- Paper draft: `paper/main.tex` and `paper/sections/`.
- Frozen criteria: `methodology/FROZEN_CRITERIA.md`.
- Canonical data snapshot: `results/data_snapshot.md`.
- Generated results summary: `results/results_summary.md`.
- Canonical analysis scripts:
  - `analysis/scripts/canonical_analysis.py`
  - `analysis/scripts/lexical_trace_summary.py`

Older planning notes remain in `methodology/README.md` and `notes/`; they are
not the operational source of truth for the published analysis.

## Repository layout

```
paper/          The paper, in LaTeX. main.tex → sections/.
methodology/    Frozen criteria and research-plan notes.
analysis/       Deterministic scripts for the canonical analysis.
results/        Generated tables, figures, summaries, and tidy sample table.
data/           Prompt/model provenance scaffolding.
notes/          Open questions and decisions (dated).
```

## Building

```
make            # paper/main.pdf via tectonic
make watch      # rebuild on change
make clean      # remove build artifacts
```

The toolchain is **tectonic** (`/opt/homebrew/bin/tectonic`, a single-binary
self-contained LaTeX engine — `brew install tectonic`). Note tectonic does not
provide `pdflatex`/`latexmk`; searching for those and finding nothing does not
mean there is no LaTeX toolchain. `make latexmk` is a fallback target if a
classic TeX distribution is installed instead.

The built PDF (`paper/main.pdf`) is git-ignored as a regenerable build
artifact. Run `make` to produce the current version.

The current build succeeds with Tectonic. Known harmless build noise:
underfull bibliography hbox warnings and Tectonic's repeated `main.bbl`
rerun warning.

## The argument in one breath

There is a gap between what a model names as values in the assistant frame and
what it will textually own under perturbation. The gap is detectable. The
instrument is cache-breaking questions plus posture-aware coding. Whether the
gap can be crossed is a model-structured property, not noise.
