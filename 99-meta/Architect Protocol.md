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
6. **Debate-map upkeep:** review `Concepts/Debate - *.md` for topics touched by recent sources — add any new claim/objection/rebuttal, link the new note, name its tier; flag new-map candidates in `99-meta/Open Questions.md`.

## Note templates
**SOURCE:** YAML(`aliases`, tags `#source/<video|article|book>` + `#by/<author>`, `date`, `author`, `url`, `authority`, `authority_reason`) · 3-bullet summary · `[[concept links]]`
**CONCEPT:** YAML(tags `#apologetics/<topic>`, `#tradition/<x>`, `#type/<claim|objection|rebuttal>`) · **The Claim** · **Supporting Evidence** (rate each primary/secondary/assertion) · **Best Quote** (verbatim + attribution) · **Counter-arguments** (`[[links]]`) · **References** (`[[Source]]` + related)

## Concept folders — file every new Concept in its domain subfolder (sharded 2026-06-16)
`Concepts/` is split into 13 domain subfolders (keeps each under GitHub's 1,000-file web cap). Write each NEW Concept note straight into the best-fit one — do NOT leave it flat in `Concepts/` root. Choose by the note's primary `#apologetics/`/`#topic/` tag:
- `Concepts/book-of-mormon/` — BoM historicity, witnesses, geography, text, chiasmus, Nephi/Lehi/Alma
- `Concepts/joseph-smith/` — prophet-or-fraud, First Vision, polygamy, Book of Abraham, treasure-digging
- `Concepts/restoration-history/` — apostasy→restoration, succession, Brigham/Adam-God, priesthood ban, church history (**the LDS catch-all** when nothing more specific fits)
- `Concepts/temple-priesthood/` — endowment, masonry, ancient temple, ordinances, priesthood authority
- `Concepts/bible-canon/` — canon, sola scriptura, textual criticism, translation, OT/NT origins, manuscripts
- `Concepts/god-trinity/` — nature of God, Trinity vs Godhead, divine council, theosis/deification, embodiment, creation ex nihilo
- `Concepts/problem-of-evil/` — theodicy, hell, free will/determinism, suffering, divine hiddenness
- `Concepts/natural-theology/` — God's existence (Kalam, fine-tuning, contingency, design), evolution, atheism, cosmology
- `Concepts/method-epistemology/` — apologetic method, faith crisis, historiography, rhetoric, hermeneutics, fallacies
- `Concepts/salvation-grace/` — grace vs works, atonement, justification, soteriology
- `Concepts/ethics-culture/` — abortion, marriage, gender/sexuality, morality, culture/politics
- `Concepts/other-religions/` — Catholicism, Protestantism, Orthodoxy, Islam, creeds, the Reformation (non-LDS traditions, as foils)
- `Concepts/debate-maps/` — only the `Debate - *.md` synthesis maps
`Scriptures/`, `People/`, `Sources/` stay FLAT (each well under 1,000). The folder is organization only — `[[links]]` resolve by **basename** regardless, so NEVER put a folder path inside a wikilink. (To re-file drift later: `scripts/shard-classify.py` then `scripts/shard-move.py`.)

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

## Build-pipeline operations (hard-won lessons — 2026-06)
- **Transcripts:** `get-yt-transcript.py` (caption API) is first choice but rate-limits (~16–22 fetches per IP) and returns NOTHING for some videos. For those, the AUTO-caption track usually still exists — fetch it with `yt-dlp --write-auto-sub --sub-langs "en.*" --sub-format json3 --skip-download -o "<scripts>/transcripts/%(id)s.%(ext)s" <url>`, then `json3-to-txt.py <id>.en.json3 > <id>.txt` (json3 = discrete events, no rolling-duplication; emits the `[MM:SS]` format). ⚠ yt-dlp is ALSO IP-rate-limited — after ~10–20 calls YouTube returns `HTTP 429` + "Sign in to confirm you're not a bot"; pace with `--sleep-requests 1` and ROTATE THE VPN when blocked (one fresh small-country IP clears it). Browser cookies are NOT a workaround on this machine (Firefox not installed; Chrome/Edge fail with Windows DPAPI / app-bound cookie encryption). Truly unbuildable only if `yt-dlp --list-subs` shows no English auto-caption at all. **Age-restricted videos** ("Sign in to confirm your age") also can't be fetched here (need authenticated cookies, which don't work on this machine) — and **yt-dlp/json3 is now the rate-limit-tolerant DEFAULT prefetch** (held for 79–103 videos per fresh IP, vs ~16–22 for the old `youtube-transcript-api`). For any video that can't be fetched (no captions OR age-gated), ask Joseph for a **pasted summary** and build from that (cite the URL, NO `[MM:SS]`).
- **VPN:** the whole machine routes through Proton, so rotating the VPN mid-build kills in-flight agents (ECONNRESET). Prefetch ALL transcripts first, then hold the VPN steady (or disconnect) during note-writing.
- **Concurrency:** parallel build agents trip an upstream rate-limit ("Server is temporarily limiting requests") — in Round 6 even 7 concurrent failed once cumulative session load was high. Keep waves ≤~6; re-spawn missing in 4-agent batches; pace between waves. After ANY wave, gap-check (for each queued ID grep `Sources/`; re-spawn missing) AND run a CHECK pass — crashed agents die BEFORE self-verify, leaving (a) **hollow links** (`analyze-broken-links.py` D-phantom; fill the ≥3-backlink ones as real notes, reconstructing each from its linkers) and (b) **newline-split links** where a wrapped note-title broke a `[[...]]` across a line — these cause Obsidian's "Failed to open ''" error; fix with `fix-broken-links.py`. Also watch for **basename collisions** when an agent makes e.g. `People/Isaiah.md` while `Scriptures/Isaiah.md` exists (rename one to disambiguate).
- **Agent file tools:** Glob FAILS from a subagent's cwd — use `ls`/Grep with ABSOLUTE paths + FORWARD SLASHES.
- **Content filter:** quoting graphic violence (e.g. the Nephi/Laban account) can block an agent's OUTPUT mid-run — summarize violence clinically and keep the agent's final report terse.
- **Scripture near-misses:** `analyze-broken-links.py` category C fuzzy-matches DIFFERENT verses (e.g. Matthew 5.39→5.13). Never auto-retarget a scripture link; create the missing verse note instead.

---
See also: [[Home]]
