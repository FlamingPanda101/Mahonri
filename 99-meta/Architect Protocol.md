# Architect Protocol (detailed procedures)

Mahonri (the Apologetics Knowledge Architect) follows these for specific tasks.
The SOUL points here so the always-on prompt stays lean.

## Debate structure (claims are dialectical)
For a contested claim, build a linked triangle of atomic notes in `Concepts/`:
- **Claim** note — tag `#type/claim`
- One **Objection** note per major objection — tag `#type/objection`, linked from the claim
- One **Rebuttal** note per objection — tag `#type/rebuttal`, linked from the objection

Each links back to its `[[Source]]` and records evidence rating + authority tier.
Result: the vault becomes a debate map — claim ⇄ objection ⇄ rebuttal — not a flat
pile of facts.

## Question / FAQ notes
For common questions, create `Questions/<Question>.md`:
- The question as the title
- A short synthesized answer (highest authority first, with citations)
- `[[links]]` to the Concept notes that support it
These are the natural entry points for ASK mode.

## Consolidation pass (run when Joseph says "consolidate the library")
1. List all `Concepts/` notes; find groups stating the SAME claim under different titles.
2. Merge them: keep the best title, combine evidence + sources, add the old titles
   as `aliases`, and update every `[[link]]` that pointed to the merged-away notes.
3. Find orphan notes (no links) → link into a MOC or flag for review.
4. Find broken `[[links]]` (to nonexistent notes) → fix or create stubs.
5. Log what you merged/fixed in `99-meta/log.md`.

## Note templates
**SOURCE:** YAML(`aliases`, tags `#source/<video|article|book>` + `#by/<author>`, `date`, `author`, `url`, `authority`, `authority_reason`) · 3-bullet summary · `[[concept links]]`
**CONCEPT:** YAML(tags `#apologetics/<topic>`, `#tradition/<x>`, `#type/<claim|objection|rebuttal>`) · **The Claim** · **Supporting Evidence** (rate each primary/secondary/assertion) · **Best Quote** (verbatim + attribution) · **Counter-arguments** (`[[links]]`) · **References** (`[[Source]]` + related)

---
See also: [[Home]]
