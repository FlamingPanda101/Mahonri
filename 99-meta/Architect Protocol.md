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

## Entity notes — scriptures & people get their OWN atomic notes
Treat scriptures and notable people as first-class entities. When a source discusses
one, give it its own note and link it **bidirectionally** with the relevant Concepts.

### Scripture notes -> `Scriptures/<Ref>.md`
- One note per verse OR verse-set (e.g. John 1:3-5 = one note if discussed together).
- Filename: replace ":" with "." (Windows-safe) -> `Revelation 22.18-19.md`; add the
  canonical ref as a YAML alias: `aliases: ["Revelation 22:18-19"]`. Link with display text:
  `[[Revelation 22.18-19|Revelation 22:18-19]]`.
- YAML tag `#type/scripture`. Body: the verse text (KJV = public domain), a **Used in**
  list of `[[Concept]]` notes that cite it, and how different traditions interpret it.

### Person notes -> `People/<Name>.md`
- One note per notable person -> `Brigham Young.md`, `Justin Martyr.md`.
- YAML tags `#type/person`, `#tradition/<x>`, `#role/<prophet|church-father|scholar|critic>`.
- Body: brief bio (who / when / role), then a **section per major topic** they're tied to,
  each linking the relevant `[[Concept]]` (e.g. a "## Polygamy" section linking `[[Polygamy]]`).

### Bidirectional linking (THE key rule)
When a Concept mentions a person/scripture (or vice versa), link it BOTH directions:
- The Concept note links out to `[[Brigham Young]]` / `[[Revelation 22.18-19|Revelation 22:18-19]]`.
- The Person/Scripture note has a section linking BACK to that `[[Concept]]`.
Result: from `[[Polygamy]]` you click `[[Brigham Young]]` -> his entry has a Polygamy section
that links back to `[[Polygamy]]`. (Obsidian's Backlinks panel surfaces these automatically too.)

## Citations — EVERY claim and quote must be sourced (footnotes)
Use Markdown footnotes so the source travels with the claim. After a claim/quote add
`[^n]`, and define it at the bottom of the note:
- Video:   `[^1]: [[Source Note|Channel - Video Title]], [12:34], https://youtu.be/ID`
- Article: `[^2]: [[Source Note|Author, "Title"]], https://example.com/article`
- Book:    `[^3]: [[Source Note|Author, *Title*]], p.45`
Pull the timestamp from the `[MM:SS]` markers in the transcript, the page from the `[p.N]`
markers in the PDF text, and the URL from the source. No locator = the claim is unsourced;
say so rather than inventing one. Scripture references cite chapter:verse directly.

## Ingesting a whole book (chunk it — don't swallow it whole)
1. First run `get-pdf-text.py <path>` (no range) to see total pages + structure.
2. Then ingest CHAPTER BY CHAPTER with page ranges: `get-pdf-text.py <path> <first> <last>`.
3. Per chunk: extract claims, write/UPDATE Concept + People + Scripture notes, cite the
   page numbers from the `[p.N]` markers, and dedup against existing notes.
4. Log progress in `99-meta/log.md` after each chunk so a long book can resume across sessions.
Never try to process a 300-page book in one pass — work it in chapter-sized chunks.

---
See also: [[Home]]
