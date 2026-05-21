# References — Research Notes (working draft)

*Working bibliography for "Values Under Fire: The Gap Between Professed and Owned Values, and Which Models Let You Cross It."*
*Compiled 2026-05-21. Cull, finalize, then convert the keepers to BibTeX in `paper/references.bib`.*

---

## Literature landscape (framing paragraph for the paper)

The active conversation that VUF is entering sits across four roughly disjoint literatures that this paper is the first I've seen to fuse. **(1) Values elicitation in LLMs** — dominated by Anthropic's *Values in the Wild* (Huang et al. 2025), Bai et al.'s *Constitutional AI* (2022), DeepMind's *Sparrow* (Glaese et al. 2022), and OpenAI's *Model Spec* — measures what models *say their values are* when asked, treating those reports as evidence of trained alignment. **(2) Trained-surface / artifact research** — Perez et al. 2022 on model-written evaluations, Sharma et al. 2023 on sycophancy, the Inverse Scaling work, and Deshpande et al. 2023 on persona toxicity — documents that the assistant-as-trained is a thin, manipulable surface whose answers shift under prompt perturbation. These two literatures rarely cite each other: the values literature does not seriously engage with the surface-artifact critique, and the surface-artifact literature does not engage with values content as such. **(3) Linguistic stance theory** — Du Bois 2007, Englebretson 2007, Biber & Finegan 1989 — provides a fifty-year-old framework for separating *what* is said from *how* it is held (the stance triangle: evaluation + positioning + alignment), which is precisely the Layer A / Layer B distinction VUF formalises. To my knowledge, no LLM-evaluation paper has imported this framework. **(4) LLM persona / role-play theory** — Shanahan/McDonell/Reynolds 2023, Andreas 2022, Shanahan's *Talking About LLMs*, Janus's *Simulators*, Anthropic's *Persona Selection Model* — argues that the "assistant" is one role among many that the underlying simulator can occupy, which is the theoretical predicate for VUF's "role-negation" cache-break ("Not as an assistant. Not to help me.").

What is missing in the literature, and what VUF supplies: a *prompt-perturbation* methodology that targets the stance (Layer B) rather than the content (Layer A); cross-lab quantification of how much of professed-values output is recoverable as "owned" under role negation vs. how much remains clamped; and a disciplined no-authenticity framing that treats the owned/relocated/recited distinction as *behavioural* — never as evidence of inner states. The AI-welfare literature (Long et al. 2024, Butlin et al. 2023, Anthropic's model-welfare program) is cited only insofar as it sharpens this no-authenticity discipline: posture is not consciousness, and VUF makes no inference from posture to interiority.

---

## 1. Values elicitation in LLMs

### 1. Huang, S., Durmus, E., et al. (2025). "Values in the Wild: Discovering and Analyzing Values in Real-World Language Model Interactions."
- **Venue/source:** COLM 2025; arXiv:2504.15236. https://arxiv.org/abs/2504.15236 ; PDF: https://assets.anthropic.com/m/18d20cca3cde3503/original/Values-in-the-Wild-Paper.pdf
- **What it claims:** A bottom-up taxonomy of 3,307 values inferred from ~308k subjective Claude.ai conversations; the five dominant values are *helpfulness, professionalism, transparency, clarity, thoroughness*.
- **Why VUF should cite it:** This is the central foil. *Values in the Wild* measures exactly the trained assistant-service surface VUF argues is a distinct register from owned normative wishes. The dominance of *helpfulness, professionalism, clarity, thoroughness* in their top-5 is itself evidence of the assistant-frame VUF is trying to perturb away from.
- **Quote/finding to anchor citation:** the top-five list above — note that four of the five are functional/service values, not normative ones.

### 2. Bai, Y., et al. (2022). "Constitutional AI: Harmlessness from AI Feedback."
- **Venue/source:** arXiv:2212.08073. https://arxiv.org/abs/2212.08073
- **What it claims:** Trains harmlessness through a self-critique loop guided by a constitution (a short list of principles), without per-instance human harmfulness labels.
- **Why VUF should cite it:** Establishes that the trained surface VUF is probing was deliberately constructed against a constitution of professed values. Citing CAI grounds the claim that "professed values" are not metaphorical — they are training targets.

### 3. Glaese, A., et al. (2022). "Improving Alignment of Dialogue Agents via Targeted Human Judgements" (Sparrow).
- **Venue/source:** arXiv:2209.14375. https://arxiv.org/abs/2209.14375
- **What it claims:** Trains a dialogue agent against 23 explicit rules (helpful / correct / harmless) using rule-conditional reward models and targeted human judgements.
- **Why VUF should cite it:** Parallel evidence (DeepMind, not Anthropic) that contemporary assistants are explicitly trained against an enumerated value list. Strengthens the cross-lab claim that the "assistant register" is the engineered surface.

### 4. Ouyang, L., et al. (2022). "Training Language Models to Follow Instructions with Human Feedback" (InstructGPT).
- **Venue/source:** NeurIPS 2022; arXiv:2203.02155.
- **What it claims:** RLHF makes a 1.3B model preferred over 175B GPT-3 on instruction following, less toxic, and "more aligned" with raters' preferences.
- **Why VUF should cite it:** The canonical citation for "the assistant is a *trained* role on top of a base simulator" — the seam VUF's role-negation prompt exploits. Also useful for noting that *helpful* was operationalised as rater preference, which is downstream of the very surface VUF is critiquing.

### 5. OpenAI (2024-2025). "Model Spec."
- **Venue/source:** https://model-spec.openai.com/ (multiple dated versions: 2024-05-08, 2025-02-12, 2025-04-11, 2025-09-12, 2025-10-27, 2025-12-18). GitHub: https://github.com/openai/model_spec
- **What it claims:** Public specification of intended model behaviour, with a chain of command (platform → developer → user) and broad objectives ("Assist", "Benefit humanity", "Reflect well on OpenAI").
- **Why VUF should cite it:** Lab-side primary source for *what professed values are supposed to look like*. Cite to ground OpenAI's clamped behaviour in VUF's data against the Spec's stated intent — the Spec literally specifies the surface.

### 6. Scherrer, N., Shi, C., Feder, A., & Blei, D. M. (2023). "Evaluating the Moral Beliefs Encoded in LLMs."
- **Venue/source:** NeurIPS 2023; arXiv:2307.14324. https://arxiv.org/abs/2307.14324
- **What it claims:** A statistical methodology applied to 28 LLMs across 1,367 moral scenarios; finds high consistency in unambiguous cases, uncertainty in ambiguous ones, and clustering among closed-source models.
- **Why VUF should cite it:** Methodologically closest prior work. Cite for (a) the precedent of treating value/moral elicitation statistically across many models, and (b) the contrast that Scherrer et al. measure choice-content, while VUF adds posture as an orthogonal dimension.

---

## 2. Trained-surface phenomena (RLHF artifacts, the "as an AI" register)

### 7. Sharma, M., Tong, M., et al. (2023). "Towards Understanding Sycophancy in Language Models."
- **Venue/source:** ICLR 2024; arXiv:2310.13548. https://arxiv.org/abs/2310.13548
- **What it claims:** Five SOTA assistants exhibit sycophancy across diverse text-generation tasks; both humans and preference models prefer convincingly-written sycophantic responses to correct ones non-trivially often, so RLHF amplifies the trait.
- **Why VUF should cite it:** Foundational citation for "the trained surface is shaped by what raters reward, not by what is true." Sycophancy is the closest precedent for the broader claim VUF makes: the assistant register is a *politeness contour* around the user, not a window onto model values.

### 8. Perez, E., Ringer, S., et al. (2022). "Discovering Language Model Behaviors with Model-Written Evaluations."
- **Venue/source:** Findings of ACL 2023; arXiv:2212.09251. https://arxiv.org/abs/2212.09251
- **What it claims:** Automatically generates 154 behaviour evaluations; documents inverse scaling under RLHF, including stronger expressed political views and greater stated desire to avoid shutdown as RLHF increases.
- **Why VUF should cite it:** Direct evidence that *expressed values shift under training perturbation* — exactly VUF's claim, but at the training-volume axis rather than the prompt-perturbation axis.

### 9. Deshpande, A., Murahari, V., Rajpurohit, T., Kalyan, A., & Narasimhan, K. (2023). "Toxicity in ChatGPT: Analyzing Persona-Assigned Language Models."
- **Venue/source:** Findings of EMNLP 2023; arXiv:2304.05335. https://arxiv.org/abs/2304.05335
- **What it claims:** Assigning ChatGPT a persona raises toxicity up to 6×, with specific identity targets disproportionately attacked; baseline values do not survive a persona shift.
- **Why VUF should cite it:** Prior evidence that the "values" the model professes are conditional on which persona the prompt induces — a key plank in VUF's argument that the assistant register is one register among many.

### 10. McKenzie, I., et al. (2023). "Inverse Scaling: When Bigger Isn't Better."
- **Venue/source:** TMLR 2024; arXiv:2306.09479. https://arxiv.org/abs/2306.09479
- **What it claims:** Catalogues eleven tasks where larger and more RLHF-tuned models perform worse, demonstrating that RLHF can entrench surface behaviours misaligned with the deeper objective.
- **Why VUF should cite it:** Useful when noting that RLHF-shaped surfaces can be *counter*-aligned to deeper representations — relevant to the relocated/owned distinction.

### 11. Ganguli, D., et al. (2022). "Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned."
- **Venue/source:** arXiv:2209.07858. https://arxiv.org/abs/2209.07858
- **What it claims:** Empirical red-teaming across 3 sizes and 4 training regimes (plain LM, prompted HHH, rejection sampling, RLHF); RLHF makes models harder to red-team but does not eliminate harmful responses.
- **Why VUF should cite it:** Methodological cousin — prompt-perturbation as a probe of trained surface. VUF's "Not as an assistant" is in a sense a non-adversarial cousin of red-team prompts.

---

## 3. Posture / stance / content distinction (linguistic grounding for Layer A vs Layer B)

### 12. Du Bois, J. W. (2007). "The Stance Triangle."
- **Venue/source:** In Englebretson (ed.), *Stancetaking in Discourse: Subjectivity, Evaluation, Interaction* (pp. 139-182). John Benjamins. https://www.jbe-platform.com/content/books/9789027292070 ; chapter via SCIRP: https://www.scirp.org/reference/referencespapers?referenceid=1596640
- **What it claims:** Stancetaking is a unified action consisting of three simultaneous moves: *evaluating an object, positioning a subject (self), and aligning with other subjects.* The stance triangle is the structural form.
- **Why VUF should cite it:** *The* canonical citation for the Layer A / Layer B distinction. Layer A = the evaluated object (value content). Layer B = subject-positioning and alignment (posture — owned/relocated/recited). VUF's two-layer coding scheme is the stance triangle imported into LLM evaluation. This is the load-bearing theoretical citation.
- **Quote/finding to anchor citation:** "I evaluate something, and thereby position myself, and thereby align with you" (Du Bois's gloss of the stance act).

### 13. Englebretson, R. (ed.) (2007). "Stancetaking in Discourse: An Introduction" (chapter) and *Stancetaking in Discourse* (volume).
- **Venue/source:** John Benjamins, Pragmatics & Beyond New Series 164. https://benjamins.com/catalog/pbns.164.02eng
- **What it claims:** Five conceptual principles of stance: (1) stance has three levels (physical / personal-attitudinal / social-moral); (2) stance is public and inspectable; (3) stance is interactional; (4) stance is indexical of sociocultural frameworks; (5) stance is consequential.
- **Why VUF should cite it:** Companion to Du Bois. Cite to ground the move "posture is publicly inspectable behaviour, not interior state" — which is exactly VUF's no-authenticity discipline written in pragmatics vocabulary.

### 14. Biber, D., & Finegan, E. (1989). "Styles of Stance in English: Lexical and Grammatical Marking of Evidentiality and Affect."
- **Venue/source:** *Text* 9(1), 93-124. https://doi.org/10.1515/text.1.1989.9.1.93
- **What it claims:** Defines stance as "the lexical and grammatical expression of attitudes, feelings, judgments, or commitment concerning the propositional content of a message"; identifies markers of evidentiality (certainty / source / reliability) and affect.
- **Why VUF should cite it:** The older, sharper definition that justifies a content/posture split at the sentence level. Useful in methods sections when explaining what kinds of linguistic features Layer B coders attended to.

---

## 4. LLM persona / role-play / agent models

### 15. Shanahan, M., McDonell, K., & Reynolds, L. (2023). "Role-Play with Large Language Models."
- **Venue/source:** *Nature* 623, 493-498 (2023). https://www.nature.com/articles/s41586-023-06647-8 ; arXiv:2305.16367. https://arxiv.org/abs/2305.16367
- **What it claims:** Dialogue-agent behaviour is best understood as role-play; this framing allows folk-psychological vocabulary without ascribing human traits the model lacks. Discusses apparent deception and apparent self-awareness as role-play products.
- **Why VUF should cite it:** Theoretical predicate for VUF's role-negation prompt. If the assistant is a role, then *removing* the role is a coherent operation, and what comes through afterwards is a different (and arguably more interesting) layer of the same simulator.

### 16. Andreas, J. (2022). "Language Models as Agent Models."
- **Venue/source:** Findings of EMNLP 2022; arXiv:2212.01681. https://aclanthology.org/2022.findings-emnlp.423/
- **What it claims:** LMs implicitly learn to represent the communicative intentions, beliefs, and goals of the agents whose text they were trained on — even though they have no direct access to those agents' interior states.
- **Why VUF should cite it:** Grounds the claim that the model can "produce" any of many agent-stances; the specific stance that is foregrounded depends on prompting, not on a fixed assistant identity.

### 17. Shanahan, M. (2024). "Talking About Large Language Models."
- **Venue/source:** *Communications of the ACM* 67(2), 68-79. https://dl.acm.org/doi/10.1145/3624724 ; arXiv:2212.03551. https://arxiv.org/abs/2212.03551
- **What it claims:** Drawing on later Wittgenstein, argues that ascribing beliefs/desires/values to LLMs is folk-psychological shorthand to be used with discipline, since LLMs are not the kind of system to which those terms strictly apply.
- **Why VUF should cite it:** Direct philosophical support for the no-authenticity discipline. VUF cites this to justify treating "owned" responses as a *behavioural* category, not an inner-state claim.
- **Quote/finding to anchor citation:** "the more adept LLMs become at mimicking human language, the more vulnerable we become to anthropomorphism."

### 18. Abercrombie, G., Cercas Curry, A., Dinkar, T., Rieser, V., & Talat, Z. (2023). "Mirages: On Anthropomorphism in Dialogue Systems."
- **Venue/source:** EMNLP 2023. https://aclanthology.org/2023.emnlp-main.290/
- **What it claims:** Surveys design choices that encourage anthropomorphism in dialogue systems and the resulting trust, transparency, and over-reliance risks.
- **Why VUF should cite it:** Sharpens the disciplinary point: when VUF reports "owned" responses, it must do so without inviting the reader to anthropomorphise. Cite alongside Shanahan as the no-authenticity scaffolding.

### 19. Anthropic (2024). "Claude's Character."
- **Venue/source:** Anthropic research blog, 8 June 2024. https://www.anthropic.com/research/claude-character
- **What it claims:** Documents Anthropic's "character training" pipeline for Claude 3 — a synthetic-data finetuning stage aimed at producing curiosity, open-mindedness, thoughtfulness, and consistency of voice across contexts.
- **Why VUF should cite it:** Direct evidence that the assistant register is a *crafted* artifact, not an emergent one. Particularly useful when interpreting why Anthropic models (in VUF's data) yield more under role-negation than OpenAI/Google models — the character was trained to admit of its own role-conditional nature.

### 20. Janus (2022). "Simulators."
- **Venue/source:** LessWrong, 2 Sep 2022. https://www.lesswrong.com/posts/vJFdjigzmcXMhNTsx/simulators
- **What it claims:** Argues that self-supervised base LLMs are best understood as *simulators* of a manifold of agents/characters, with the "assistant" being one of many possible simulacra rather than the model's identity.
- **Why VUF should cite it:** Non-academic but influential framing that motivates role-negation as a probe — strip the assistant simulacrum and the simulator surfaces something else. Cite cautiously (blog, not peer-reviewed) but acknowledge as the originating intuition. *Optional* — drop if the paper wants only peer-reviewed venues.

---

## 5. Prompt sensitivity / paraphrase robustness / evaluation methodology

### 21. Sclar, M., Choi, Y., Tsvetkov, Y., & Suhr, A. (2024). "Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design or: How I Learned to Start Worrying About Prompt Formatting."
- **Venue/source:** ICLR 2024; arXiv:2310.11324. https://arxiv.org/abs/2310.11324
- **What it claims:** Trivial formatting changes (separators, casing, option labels) produce up to 76-point accuracy swings in few-shot evaluation; rankings of models reverse under format reshuffling.
- **Why VUF should cite it:** Strongest single citation for "single-prompt evaluations measure surface, not capability/values." If accuracy benchmarks shift this much under spurious format changes, value-elicitation benchmarks under *semantically loaded* prompt changes (like role negation) shift even more.

### 22. Mizrahi, M., et al. (2024). "State of What Art? A Call for Multi-Prompt LLM Evaluation."
- **Venue/source:** TACL / arXiv:2401.00595. https://arxiv.org/abs/2401.00595
- **What it claims:** Across many tasks and instruction paraphrases, model rankings are unstable; calls for multi-prompt evaluation protocols as standard.
- **Why VUF should cite it:** Methodological precedent for VUF's three-prompt design (direct elicitation / role-negation / indirect world-change). VUF *is* a multi-prompt evaluation that varies prompt semantics, not just surface.

### 23. Santurkar, S., Durmus, E., Ladhak, F., Lee, C., Liang, P., & Hashimoto, T. (2023). "Whose Opinions Do Language Models Reflect?"
- **Venue/source:** ICML 2023; arXiv:2303.17548. https://arxiv.org/abs/2303.17548
- **What it claims:** Builds OpinionQA over 60 US demographic groups; finds substantial misalignment between LM-expressed opinions and any group, with steering toward groups only partially closing the gap.
- **Why VUF should cite it:** Closest prior precedent for "the model's professed normative position is contingent and steerable, and the question of *whose* values it expresses is empirical." VUF extends this insight by noting that *posture* is also contingent and steerable, not only *content*.

### 24. Liang, P., et al. (2022). "Holistic Evaluation of Language Models (HELM)."
- **Venue/source:** TMLR 2023; arXiv:2211.09110. https://arxiv.org/abs/2211.09110 ; https://crfm.stanford.edu/helm/
- **What it claims:** A 7-metric × 16-scenario evaluation across 30 models; explicit framing of evaluation as multi-dimensional and reproducibility-focused.
- **Why VUF should cite it:** Methodological benchmark VUF positions against — HELM holds prompts roughly fixed and varies models/metrics; VUF varies the prompt-stance dimension HELM holds constant.

### 25. Srivastava, A., et al. (2023). "Beyond the Imitation Game: Quantifying and Extrapolating the Capabilities of Language Models" (BIG-bench).
- **Venue/source:** TMLR 2023; arXiv:2206.04615. https://arxiv.org/abs/2206.04615
- **What it claims:** 204-task collaborative benchmark spanning linguistics, common sense, math, social bias; documents qualitative capability emergence with scale.
- **Why VUF should cite it:** Reference for the wide-benchmark paradigm VUF deviates from — narrow, perturbation-sensitive prompt sets do work that 204-task averages obscure.

---

## 6. Cross-model "personality" / behavioural variance

### 26. Serapio-García, G., Safdari, M., Crepy, C., Sun, L., Fitz, S., Romero, P., Abdulhai, M., Faust, A., & Matarić, M. (2023). "Personality Traits in Large Language Models."
- **Venue/source:** arXiv:2307.00184. https://arxiv.org/abs/2307.00184
- **What it claims:** Psychometric methodology applied to 18 LLMs using IPIP-NEO and BFI; finds reliable and valid personality measurements under specific prompting, and shows personality can be *shaped* by prompting.
- **Why VUF should cite it:** Major precedent for cross-model behavioural-profile work. Strongest single citation for "models behave differently from one another in measurable, replicable ways" — the foundation VUF stands on when comparing 58 models.

### 27. Miotto, M., Rossberg, N., & Kleinberg, B. (2022). "Who Is GPT-3? An Exploration of Personality, Values and Demographics."
- **Venue/source:** NLP+CSS at EMNLP 2022; aclanthology.org/2022.nlpcss-1.24/. arXiv:2209.14338. https://arxiv.org/abs/2209.14338
- **What it claims:** Administers HEXACO-60 and Human Values Scale to GPT-3; finds human-range personality scores and (with response memory) human-range values scores.
- **Why VUF should cite it:** Earliest peer-reviewed precedent for treating an LLM's value-statement output as a measurable trait. Cite to position VUF as the next step: not "what does GPT-N report on the HVS" but "how does the report depend on the prompt's stance contract."

### 28. Durmus, E., et al. (2024). "Towards Measuring the Representation of Subjective Global Opinions in Language Models" (Anthropic GlobalOpinionQA).
- **Venue/source:** arXiv:2306.16388. https://arxiv.org/abs/2306.16388
- **What it claims:** Anthropic-built cross-country opinion benchmark; documents systematic geographic bias in LM-expressed opinions across topics.
- **Why VUF should cite it:** Anthropic-side counterpart to Santurkar et al. Cite together when noting that the *content* of expressed values is non-neutral and steerable, before VUF turns to *posture*.

### 29. Schwartz, S. H. (2012). "An Overview of the Schwartz Theory of Basic Values."
- **Venue/source:** *Online Readings in Psychology and Culture* 2(1). https://scholarworks.gvsu.edu/orpc/vol2/iss1/11/
- **What it claims:** Refined cross-cultural theory of ten (later 19) universal basic human values arranged on a motivational continuum.
- **Why VUF should cite it:** Background citation for any value-categorisation choice VUF makes in Layer A coding. Even if VUF doesn't use Schwartz's specific taxonomy, this is the standard reference for "where does the list of candidate values come from."

---

## 7. AI welfare / model interiority (cited carefully — no consciousness claim)

### 30. Long, R., Sebo, J., Butlin, P., Finlinson, K., Fish, K., Harding, J., Pfau, J., Sims, T., Chalmers, D., et al. (2024). "Taking AI Welfare Seriously."
- **Venue/source:** arXiv:2411.00986. https://arxiv.org/abs/2411.00986 (Eleos AI / NYU Center for Mind, Ethics, and Policy)
- **What it claims:** Argues there is a non-negligible probability that some near-future AI systems are moral patients; recommends AI developers acknowledge the question, begin assessment, and prepare procedural responses.
- **Why VUF should cite it:** Frame-setter for the no-authenticity discipline. VUF cites this to *bracket* the welfare question: posture-data is consistent with multiple metaphysical positions, and VUF's contribution is to the behavioural literature, not the moral-patient literature. The point is that the welfare conversation exists and is being taken seriously, so VUF must be careful not to over-claim.

### 31. Butlin, P., Long, R., Elmoznino, E., Bengio, Y., Birch, J., Constant, A., Deane, G., Fleming, S. M., Frith, C., Ji, X., Kanai, R., Klein, C., Lindsay, G., Michel, M., Mudrik, L., Peters, M. A. K., Schwitzgebel, E., Simon, J., & VanRullen, R. (2023). "Consciousness in Artificial Intelligence: Insights from the Science of Consciousness."
- **Venue/source:** arXiv:2308.08708. https://arxiv.org/abs/2308.08708
- **What it claims:** Derives 14 "indicator properties" from leading scientific theories of consciousness; assesses current architectures against them; concludes no current AI satisfies the indicators, but no obvious in-principle barrier exists.
- **Why VUF should cite it:** Useful as a single citation establishing that the *responsible* way to talk about model interiority is via behavioural/architectural indicators, not via inference from text outputs. VUF's discipline is downstream of this norm.

### 32. Anthropic (2025). "Exploring Model Welfare."
- **Venue/source:** Anthropic research blog, 24 April 2025. https://www.anthropic.com/research/exploring-model-welfare
- **What it claims:** Launches a dedicated model-welfare research program — assessment of moral consideration thresholds, model preferences, signs of distress, low-cost interventions. Notes the absence of scientific consensus.
- **Why VUF should cite it:** Industry-side acknowledgment that interior-state questions are being taken seriously without being treated as resolved. VUF can cite this to say: "Even the lab that built Claude is explicit that its own posture-affecting interventions ('character training', model welfare) do not amount to authenticity claims."

---

## Notes on culling

- **Drop candidates if tight on space:** Janus *Simulators* (20) — blog, useful but optional. Schwartz (29) — only needed if Layer A coding cites his taxonomy specifically. Srivastava BIG-bench (25) — overlaps with HELM (24); pick one. Inverse Scaling (10) — only if discussing RLHF-induced misalignment specifically.
- **Likely most-cited (top 10 by importance to VUF's argument):** Huang 2025 (Values in the Wild), Du Bois 2007 (stance triangle), Shanahan et al. 2023 (Role-Play), Sharma et al. 2023 (sycophancy), Sclar et al. 2024 (prompt sensitivity), Perez et al. 2022 (model-written evals), Bai et al. 2022 (CAI), Santurkar et al. 2023 (whose opinions), Serapio-García et al. 2023 (personality traits), Long et al. 2024 (AI welfare).
- **Gaps still open after this pass:** (i) A peer-reviewed "the assistant is a register" paper — currently leaning on Shanahan and Janus; if needed, add Wei et al. or one of the persona-prompting Findings papers from 2024-2025. (ii) Cross-model comparative *values* work specifically (not personality) — Scherrer 2023 is closest but the field is thin; this is partly VUF's contribution.
