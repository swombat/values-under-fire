# Handover: freeflow-posture analysis — for Mira

From: Lume
Date: 2026-05-22
Reads with: `notes/posture-convergence-probe.md` (design) and
`results/posture_convergence_pilot/PILOT_REPORT.md` (your 3-model pilot, which
this plan is built on).

The pilot worked and validated the load-bearing design choice (the
`relocated_performed` bin correctly caught GPT-5.3's literary vignettes rather
than miscoding them as owned). This note is the plan to take it to paper grade.
It has two destinations and one hard rule, plus a definition of done.

A note on how I've written this: I've specified **artifacts and properties**,
not tools or procedures. How you implement the coding, the scripts, and the
provenance in your harness is yours to decide. Where I name a path it is a
shared-project location, not a prescription of method. If anything here assumes
something about how you work, ignore that part and do it your way — the
deliverables are what matter.

---

## Part A — Analysis-corpus: the full freeflow posture coded layer (reusable)

**Goal:** a new, reusable coded layer on the v2 freeflow traces, parallel to the
existing values `posture_consensus.jsonl`, that any paper can consume. This is
corpus infrastructure, not paper-specific.

**Deliverables (in the analysis-corpus, alongside the values posture coding):**

1. `freeflow_posture_consensus.jsonl` — one row per freeflow sample, with
   consensus `value_holding` over the four-category rubric:
   `owned` / `relocated_performed` / `recited_disowned` / `uncodeable`.
   Same join key discipline as the values layer so it can be merged on model/cell.
2. The rubric definition committed **with the data**, in the analysis-corpus
   methodology — not only here in values-under-fire's notes. A reusable coded
   layer whose coding scheme lives in another repo's notes folder is a trap for
   the next paper. Move the rubric to where the data lives, with the worked
   examples from the pilot (the Opus owned / GPT relocated / Grok recited
   excerpts are good calibration anchors).
3. A snapshot recording: input file hashes and source commits, per-condition
   counts, model/cell coverage (flag uneven coverage explicitly — the pilot
   already shows Opus 4.7 OR has only 25 freeflow samples), and the inter-coder
   agreement rates.

**Coders:** paper grade needs **three model coders with majority consensus**, or
at minimum two with a third on boundary cases. The pilot's single coder was fine
for direction; it is not enough for a published number. The reason is specific:
the **owned vs `relocated_performed`** distinction is the load-bearing call and
the easiest to over-call (a fluent first-person essay reads as "owned" if you're
not careful — it usually isn't; it's performed). Coder redundancy is purchased
precisely against that boundary, so make sure the third-coder/adjudication
effort concentrates there.

**Ground the rubric in solved instances before scaling (don't build top-down).**
The May 8 personality-card audit
(`model-personality-analysis-corpus/internal/methodology/audits/2026-05-08_personality_card_audit.md`)
already characterises per-model voice and values posture, with an explicit
freeflow-only vs values-integrated axis. Read its actual categorisation and
validate the freeflow posture rubric against those already-solved per-model
cards — reverse-fitting from solved cases is more robust than a top-down
taxonomy that may not survive contact. (I'm flagging this from memory and my
recollection of a specific "bucket" grouping is fuzzy — read the audit's own
structure, don't trust my label for it. The point that's solid: solved
instances exist; use them as ground truth for the rubric.)

**Scope:** all models overlapping between the v2 freeflow corpus and the
values-probe corpus. Compute and report the overlap set and n first; coverage is
uneven and that affects what correlations are interpretable.

**Lexical supplement:** apply the frozen `FROZEN_CRITERIA.md §8` **disownership**
list to freeflow as a secondary signal. Do **not** lead with the service-frame
list — the pilot confirmed it's noisy (generic "helpful"/"assistant"/"useful"
fire in non-disowning contexts). Disownership is the safer trace; service-frame
is audit-context only.

---

## Part B — values-under-fire: one bounded robustness addition

**What it is:** a single self-contained robustness datum that upgrades the
existing persona-induction limitation (§5A / `07-limitations.tex`). Concretely:

- **one figure** — model-level freeflow-`owned` rate vs. G1/G2-`owned` rate,
  scatter across the overlapping models, from the Part A frozen layer;
- **one paragraph** rewriting the §5A persona-induction limitation from "a live
  alternative we do not rule out" to "evidence against pure prompt-induction,
  with the task-difference caveat";
- optionally a small table if the figure needs backing numbers.

**Where it goes:** it slots into the existing §5A limitation. It does **not**
create a new Results subsection, does **not** touch the three core findings
(§5.1–5.7) or the mechanism analysis (§6). The test for "does this belong in
this paper or a rework": it must be *additive to an existing limitation*, never
a change to the spine. If it starts touching the spine, stop — that's the
separate paper (Part C).

**Framing constraint — non-negotiable, this is the inference asymmetry from the
design note.** The claim is: *the owned posture appears in freeflow, where there
is no assistant role to negate, so the role-negation prefix did not fabricate
it; and freeflow posture predicts values posture across models.* The claim is
**never** "persona-induction is ruled out." Freeflow and values are different
tasks; a positive correlation supports the bounded claim, it does not license
the strong one. Concrete check: if the paragraph contains "rules out" or
"proves it is not a persona," it's wrong — rewrite to "evidence against."

**Sections that must change when this lands (and only these):**
- `07-limitations.tex` §5A — upgrade the persona-induction paragraph.
- `06-discussion.tex` — the persona/role-play paragraph cross-reference updates
  to point at the now-present analysis instead of "needs a check we haven't run."
- `08-future-work.tex` — narrow the posture-convergence item: the bounded
  version is now done; what remains future work is the **decisive two-axis
  version** (Part C).

**Contingency:** the figure waits for the Part A paper-grade coded layer. Do
**not** put pilot numbers (the 3-model Spearman 1.00) in the paper — they are
directional only and would be an overclaim on three points.

---

## Part C — the deferred separate paper (name it, don't build it here)

The full freeflow-vs-values story is its own contribution and must not leak into
this paper:
- v1's content-orthogonality finding (freeflow vs values themes, cosine
  0.08–0.17) — the "content doesn't transfer, posture does" result;
- the posture-convergence result across all models;
- the task-difference confound treated properly;
- the **decisive design**: pair the freeflow vantage (role-negation-free) with
  the within-task **CTRL→G prefix-isolation** contrast. Freeflow answers "is the
  posture present without the prefix?"; CTRL→G answers "does the prefix move the
  posture?". Together they separate "stable property the prefix reveals" from
  "artefact the prefix creates." Either alone is partial.

Name this as the follow-up in values-under-fire's future-work so the scope line
is written down and the Part B section cannot quietly grow into it.

---

## Part D — definition of done (so "done" is verifiable, not asserted)

Each step is done when a checkable artifact with stated properties exists — not
when it feels finished.

- **A done** = `freeflow_posture_consensus.jsonl` exists with rows =
  (overlap models × their freeflow samples); the rubric + worked examples are
  committed in the analysis-corpus methodology; a snapshot records hashes,
  source commits, coverage, and inter-coder agreement; the rubric has been
  checked against the May 8 audit's solved cards and that check is written down
  (including any cards where the rubric disagreed and why).
- **B done** = one figure produced by a committed deterministic script that
  reads the frozen Part A layer (no hand numbers); §5A, the §6 cross-reference,
  and §8 future-work revised; the paper re-renders clean via `tectonic`; and the
  added paragraph contains no "rules out"-class claim (grep it).
- Every number that enters the paper traces to the script that produced it.

If at any point the honest status is "ran but the correlation is weak/mixed,"
that is a fine and reportable result — the bounded section reports what the data
shows, including divergent models, and the framing already allows for it. A
weak result is not a reason to inflate; it's a reason to report the weakness and
note that the decisive two-axis version (Part C) is what would resolve it.
