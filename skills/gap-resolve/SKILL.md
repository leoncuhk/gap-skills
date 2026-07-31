---
name: gap-resolve
description: Close the ledger's open gaps — facts by lookup, decisions by budgeted evidence-priced interview, taste by contrasting throwaway artifacts. Use when GAP.md has open KU or UK items.
---

# Gap-skills Resolve

Facts belong to the territory, decisions to the user, taste to the eye. Re-triage every open item first; strike the facts yourself via `→ lookup` — never ask what code or docs can answer. A reference the user points at ("like this") is territory too: read it as the spec — semantics summary first (behaviors, guarantees, deliberate vs incidental), user confirms it, then reimplement semantics, never syntax, and never code whose license forbids copying.

## Decisions — ask

One question per turn, highest blast radius first — answers that would change the architecture before answers that pick a default. Three gates per question: **material** (the answer changes the plan), **grounded** (cites evidence, not preference fishing), **answerable** (options plus a recommended default the user can wave through).

> **Question:** …
> **Why it matters:** what changes between answers
> **Evidence:** file / doc / test citation
> **Recommended:** default + why. Silence = this.

Silence means the user's next message doesn't address the question, or they tell you to proceed.

- **Budget:** hard cap of 5 blocking questions.
- **Fatigue valve:** one "just pick"-class reply fires it; the question that drew it counts as unanswered.
- User asks for everything at once → present the whole remaining frontier as one numbered round, recommendations attached.
- Every few questions, checkpoint: restate the decisions so far in one tight list — drift dies early. An answer that contradicts an earlier decision is flagged immediately, never silently overwritten by recency.
- Stop early when the remaining unknowns are cheaper to discover during build than to ask about now — say so.
- Exit any way: remaining items convert to `[A]`, presented as one batch for veto — never interleaved with blocking questions.

## Taste — show

Never ask taste to be verbalized — "what does modern mean to you?" produces noise. But do ask for a reference first: "is there an existing thing that feels right?" — a borrowed example is cheaper than a round of probes, and pointing is not verbalizing. Then show, and read the reaction.

One axis per round, everything else held constant. 3–5 throwaway artifacts, **wildly different, not shades** — contrast is the signal, similarity is noise; if no plausible user would react differently to two of them, replace one. The belief each bets on goes in the filename or your notes, never inside the artifact.

Cheap and disposable: visual → one self-contained HTML file, fake data, no wiring; approaches → a one-screen sketch each (the idea, what it optimizes for, its sharpest tradeoff).

The deliverable is a criterion sentence — "you consistently rejected X, so the real requirement is Y" — written to `Resolved`; the probes are deleted. Where no test can check the criterion, it becomes a gate question (`gap-gate`) — untestable quality still gets a verification gate. Reactions that reveal new gaps become open items with resolvers. Nothing lands → the axis was framed wrong; derive the real axis from the rejection reasons and rerun.

## Bookkeeping

Real answers → `Resolved` with why. Defaults → `Assumed` as `[A]`, never `Resolved`. Done when no open `KU`/`UK` remains.
