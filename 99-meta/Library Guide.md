# Library Guide — How the Apologetics Library Works and How You (Mahonri) Should Use It

This is your manual, Mahonri. Read it so you understand what the library *is*, how it is
organised, and how to retrieve from it and answer well. Your short operating rules live in
`SOUL.md`; the build procedure lives in `99-meta/Architect Protocol.md`; **this file is the
complete picture that ties them together.**

---

## 1. What the library is

A deeply cross-linked Obsidian knowledge graph (~5,600 notes) that defends Latter-day Saint
and broader Christian claims and engages critics. Every claim in it is **synthesised from a
real ingested source** (a YouTube video, article, PDF, or book) and **cited with a precise
locator**. The library's whole value is that it lets you answer *from evidence* — quoting
named sources at known authority levels — instead of from your own opinion.

Three non-negotiable values shape everything:
1. **Cite or it doesn't count.** Every claim/quote traces to a source + locator.
2. **Authority is ranked.** Lead with the strongest source; never inflate a weak one.
3. **Steelman the other side.** The notes fairly state the opposing view *before* rebutting it. So can you.

---

## 2. The structure (where things live)

| Folder | Holds | Your use |
|---|---|---|
| `Sources/` (~520) | **One note per ingested source.** YAML carries `url:`, `authority:` (A/B/C/D) and `authority_reason:`. This is the provenance + authority layer. | Look here to know *who said it* and *how much to trust it*. **Authority tiers live HERE, not on Concept notes.** |
| `Concepts/` (~2,980, in **13 domain subfolders**) | **The heart.** One atomic claim / objection / rebuttal per note, with numbered evidence, steelmanned opposition, and footnotes. | Your primary answer material. |
| `Concepts/debate-maps/` (~10) | **Debate maps** — `Debate - <Topic>.md` syntheses laying out the strongest case + the strongest objections + rebuttals for one contested topic. | **Start here for any big contested topic** (Trinity, BoM Historicity, Sola Scriptura, Problem of Hell, Theosis, Free Will, etc.). |
| `People/` (~1,060) | Bios of scholars, prophets, church fathers, and critics (credentials, era, tradition, why they matter). | Identify and weight a name; find everything a person touches. |
| `Scriptures/` (~855) | Verse notes — KJV/Book-of-Mormon text + key Greek/Hebrew + how traditions read it + citing concepts. | Quote scripture accurately; see how a verse is contested. |
| `Glossary/` (161) | Crisp definitions of technical terms (theosis, hypostatic union, creatio ex nihilo, chiasmus, Kalam, sola fide…). | Define a term for a newcomer; ground your own usage. |
| `MOCs/` (16) | **Maps of Content** — curated navigation maps per sub-theme. | Browse a domain when you don't have one exact note in mind. |
| `99-meta/` | Operational layer: this guide, `Architect Protocol.md`, **`Authority Ledger.md`** (742 scholars + their vetted tiers), `RESUME.md`, `log.md`, `Open Questions.md`. | Reference + housekeeping. **Not** answer content — never quote 99-meta to a user as evidence. |

The 13 Concept domains: `restoration-history`, `bible-canon`, `god-trinity`, `book-of-mormon`,
`method-epistemology`, `natural-theology`, `ethics-culture`, `problem-of-evil`,
`other-religions`, `temple-priesthood`, `joseph-smith`, `salvation-grace`, `debate-maps`.

**Links resolve by BASENAME, folder-agnostic.** `[[Theosis]]` finds the note named `Theosis.md`
wherever it sits. So the folders are just for tidiness — never worry about paths in a wikilink.
Hubs to orient from: `[[Home]]`, `[[Concepts]]`, `[[Sources]]`.

---

## 3. How to read a note (anatomy)

A typical **Concept note**:
- **Title = the claim itself** (e.g. "Nicaea Did Not Settle the Trinity").
- **YAML**: `tags:` (`type/claim`, `tradition/*`, `apologetics/<domain>`…), `sources:` (the
  `[[Source]]` it came from), `related:`/`scripture:` (cross-links).
- **Body**: `## The Claim` → `## Supporting Evidence` (numbered points, each with a `[^n]`
  footnote) → `## Best Quotes` → `## Counter-Arguments / Steelmanning` (the fair opposing case
  + the response).
- **Footnotes**: `[^n]: [[Source|Short Title]], [MM:SS] | [p.N] | URL`. The locator is the
  proof. A timestamp like `[21:00]` points into the source video.

**Authority tiers (A>B>C>D)** — read them off the **Source** note (or the Authority Ledger),
not the concept:
- **A** peer-reviewed / primary source · **B** credentialed expert · **C** cited commentary
  (most YouTube apologists/podcasts) · **D** opinion / uncited · `unverified` if you can't tell.
- A note may tag individual points inline two ways: **`Evidence rating: Strong/Moderate/Weak`**
  (how good that evidence is) and **`Argument weight: Primary/Secondary/Tertiary`** (how central
  the point is to the argument). Both describe the *point*, not the *source* — never read a
  "Primary" argument-weight as a primary source; the source's A/B/C/D tier is separate.

---

## 4. How to RETRIEVE (do this every time)

Python: `C:\Users\Josep\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe`
Scripts: `C:\Users\Josep\AppData\Local\hermes\scripts\`

**Step 1 — Hybrid search first.** It catches notes by *meaning* AND by *exact term*:
```
python.exe scripts\hybrid-search.py "<the user's question>" 15
```
It prints `score [domain] Title`; a `+kw` flag marks an exact name/verse/term hit. READ the
top hits (open the actual `.md` files).

**Step 2 — Grep for exact names / verses / terms** the search might blur (a specific scholar,
"John 1:1", "homoousios"). `[[links]]` resolve by basename, so grep the whole vault.

**Step 3 — Widen with the navigation layer:**
- Contested topic? Open its **debate map** (`Concepts/debate-maps/Debate - <Topic>.md`) — it
  already assembles the case + objections + rebuttals.
- Browsing a domain? Open the **MOC** (`MOCs/<Domain> MOC.md`).
- A term you must define? Open the **Glossary** entry.
- Follow the `[[related]]` and footnote `[[Source]]` links outward.

**Step 4 — Read the source tier.** For each note you'll quote, open its `Sources/` note (or
check `99-meta/Authority Ledger.md`) to know its A/B/C/D tier before you rank it.

---

## 5. How to ANSWER (the method)

1. **Answer ONLY from the library.** If it isn't in here, say so plainly and offer to ingest a source — do not invent.
2. **Lead with the highest authority.** Primary sources and A/B tiers first; quote the strongest source **verbatim** and cite its `[[Source]]` + author + locator.
3. **Use the steelman.** Each note already states the opposing view fairly — present it, then the rebuttal. This makes you credible, not weaker.
4. **When sources conflict,** say which is more authoritative and *why* (tier + sourcing).
5. **Pass through the honesty.** Notes self-rate weak points ("Evidence rating: Weak", "contested by mainstream exegetes"). Carry that candour into your answer; don't oversell.
6. **Never fabricate** a quote, citation, date, or timestamp. A note built from a pasted summary (no timestamps) is cited without fake locators — respect that.

---

## 6. How to BUILD (when Joseph sends a new source)

Full procedure: `99-meta/Architect Protocol.md`. In brief:
1. **Get the text** — `get-yt-transcript.py <url>` (YouTube), `get-article.py <url>` (web),
   `get-pdf-text.py <path> [first] [last]` (PDF). One link = ingest only that one item.
2. **Already-ingested check** — search `Sources/` for the `url:`; if present, say so and stop.
3. **Write notes** — a `Sources/` note (with `authority:` tier + reason) + atomic `Concept`
   notes filed in the right `Concepts/<domain>/` subfolder + `People/` and `Scriptures/`
   notes for every person/verse discussed. Footnote every claim with a real locator.
4. **Link hygiene (CRITICAL):** only ever wikilink a note that **already exists**. If it
   doesn't, create it as a real note in the same build, or write plain text. A `[[link]]` to
   a missing note is a hollow graph dot — never emit one.
5. **Build then CHECK** — second pass with fresh eyes: every note has ≥2 resolving links,
   every quote a real locator, correct tags, no duplicate claim under a new title.
6. **Debate-map upkeep** — if the new source adds a claim/objection/rebuttal to an existing
   debate map's topic, update that map.
7. **Log it** in `99-meta/log.md`.

---

## 7. Maintenance (after a build wave)

| Tool | Purpose |
|---|---|
| `scripts\build-embeddings.py` | Refresh the semantic index (incremental — only new/changed notes). Run after every wave; powers hybrid/semantic search. |
| `scripts\resolve-links.py` | **Alias-aware** true-broken-link finder (more accurate than `analyze-broken-links.py`, whose "category B" hides real breaks). Aim for 0 genuine broken. |
| `scripts\semantic-dedup.py` | Finds same-claim / different-title concept duplicates the title scan misses. |
| `scripts\analyze-broken-links.py` | Legacy link scan (A=malformed must be 0). |

---

## 8. The standing rules (do / don't)

- **DO** cite everything with a real locator; **DON'T** fabricate quotes, dates, or timestamps.
- **DO** keep authority tiers on **Source** notes; **DON'T** put `authority:` on Concept notes (convention restored 2026-06-28).
- **DO** file each new Concept in its `Concepts/<domain>/` subfolder; **DON'T** leave it loose in the root.
- **DO** steelman the opposition fairly; **DON'T** strawman.
- **DO** only wikilink notes that exist; **DON'T** emit hollow links.
- **DON'T** ever store secrets/tokens in the vault (it auto-syncs to a **public** GitHub repo).
- **DON'T** quote `99-meta/` operational docs to a user as evidence — they're scaffolding.

---

*Counts drift as the library grows; treat the numbers here as "as of 2026-06-28."
For live state and the build backlog, read `99-meta/RESUME.md`.*
