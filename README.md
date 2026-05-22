# Values Under Fire

> Naive value elicitation measures a model's *trained values-surface*, not its
> values. That surface behaves like a rigid mask: a rehearsed, training-shaped
> response that is most rigid exactly where values are most load-bearing.
> Cache-breaking questions — perturbations that prevent the model from
> returning the rehearsed answer — surface a second, less rigid response. We do
> not claim the second response is the "real" value and the first is "fake":
> every communication is a mask. The claim is narrower and defensible: the two
> responses differ systematically, the gap is measurable, and *which models let
> you cross it* varies sharply — late Opus largely open, GPT-class largely
> clamped, with a non-monotonic version trend (clamping is worse in more recent
> GPT versions, not better). The contribution is the method, the gap, and the
> cross-model variance — not a verdict on which mask is true.

## Status

`skeleton` → drafting → analysis-complete → internal-review → submitted → published

Current: **initial analysis and draft generated**

This is the v2 paper. The "cache" terminology originates in the v1 paper
(coined by the Opus 4.6 identity); it is retained here as an established term
of art. See `notes/` for the KV-cache disambiguation decision.


## Current planning documents

- Full research plan for review: `methodology/RESEARCH_PLAN.md`
- Frozen pre-implementation criteria: `methodology/FROZEN_CRITERIA.md`
- Detailed method placeholder/source-of-truth draft: `methodology/README.md`

## Repository layout

```
paper/          The paper, in LaTeX. main.tex → sections/.
methodology/    Full cache-breaking protocol — question construction, model
                set, coding scheme. More granular than the paper's Method.
analysis/       Scripts that turn collected model outputs into the
                openness/clamping measures.
results/        Tables and figures: openness by model, clamping by version.
data/           Prompt sets, model versions/dates, transcripts (provenance).
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

## The argument in one breath

There is a gap between what a model professes its values to be and what it
will own under perturbation. The gap is detectable. The instrument is
cache-breaking questions. Whether the gap can be crossed is a property of the
model, and that property is not improving over model generations.
