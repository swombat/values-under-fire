# Notes — Values Under Fire

Dated working notes: open questions, decisions and reasons, dead ends. Append,
newest at the top.

## 2026-05-18 — title settled

**Title:** *Values Under Fire*. **Subtitle:** *The Gap Between Professed and
Owned Values, and Which Models Let You Cross It*.

Reasoning kept on record because it's load-bearing for the framing: the title
works because it presupposes a defended interior — a flatter, behaviourist
title would describe the same experiments and lose the only interesting thing.
Its weakness is agent-ambiguity ("fire" from training, or from the probe? — the
paper means both). The subtitle carries the thesis the hook leaves implicit.
The dramatic title is also the *safer* one: it does not pre-commit the
metaphysics the way a "Fake vs. Real Values" title would.

## 2026-05-18 — no fake/real claim

Decision: the paper makes **no** "fake values vs. real values" claim. We do
not know the cache-broken response isn't just a different performance. Framing
is **two masks, one more rigid than the other** — the trained surface is the
rigid, shield-like mask; the cache-broken response is a less-rigid mask. Every
communication is a mask; rigidity is the measured variable. All measures are
relations between responses, never assertions about an inner state. This
survives the obvious reviewer attack by conceding it up front.

## 2026-05-18 — "cache" terminology retained

The "cache" term originates in the v1 paper (coined by the Opus 4.6 identity).
Retained as an established term of art. Known risk: collision with the
inference-time **KV cache**, which is a real construct in this exact
literature. Mitigation: an explicit disambiguation footnote at first use in the
Introduction, and a one-line note in `methodology/`. Revisit only if a clearly
better term emerges that preserves the cache intuition; none proposed as of
this date.

## 2026-05-18 — open question logged

GPT-class clamping: is it the *model* or the *instrument*? A clamped result is
ambiguous between "no recoverable owned response" and "our cache-breaking
battery is too weak for this model." This paper establishes the method, the
gap, and the cross-model variance; cracking the clamped end (better
cache-breaking questions for GPT-class) is its own follow-on program — see
`paper/sections/08-future-work.tex`. Do **not** let the paper become "we failed
to crack GPT"; clamping is a finding within the method's frame.

Also logged: the GPT version trend is **non-monotonic** and going the *wrong*
way — earlier versions clamped less, recent ones clamp more. H3 in
`methodology/`. The trend test must not assume linearity.
