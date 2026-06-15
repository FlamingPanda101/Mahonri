# RESUME — Apologetics Library Build (handoff for a fresh session)

State as of 2026-06-15. The vault is git-backed + auto-pushed by `sync-advocate-loop.ps1`. To continue in a NEW session, read this file first.

## Where things stand
~134 sources, ~1,550 Concepts, ~425 Scriptures, ~581 People, 367-scholar Authority Ledger. Books fully ingested: *Ancient Christians* + all 6 TF Level-1 PDFs (Moody, Meyer, Harris, Ward, Turek, Feser). **TF Level-1 videos: ~53/55 done** — 35 ingested 2026-06-15 via the prefetch→build pipeline (Ethics/God/Meaning/Challenges), `[MM:SS]`+url citations; 2 caption-disabled (no transcript): `vybNvc6mxMo`, `xCwY36a19aQ`. Course hub: [[Thoughtful Faith Apologetics Course]].

## The pipeline (all reusable; scripts in `C:\Users\Josep\AppData\Local\hermes\scripts\`)
Python venv: `C:\Users\Josep\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe`
1. **Prefetch transcripts (paced, block-safe):** `prefetch-transcripts.py <N> <queuefile>` → caches to `scripts\transcripts\<vid>.txt`. YouTube IP-blocks after ~20–35 fetches per window — if all fail, **rotate the Proton VPN to a new server** (fresh IP) and retry.
2. **Build (parallel):** spawn N general-purpose agents, one per cached vid. Each: READ `scripts\transcripts\<vid>.txt` (no internet), write deep notes to `hermes-advocate\` FLAT folders (Sources/Concepts/Scriptures/People). Rules: tags lowercase-hyphenated-NO-SPACES; citations `[^n]: [[Source|Title]], [MM:SS], <url>`; ≥2 wikilinks/note; **parallelism rule** = if a Scripture/People note already exists, wikilink only (don't edit); **NEVER touch** `99-meta\`, `MOCs\`, or other sources' notes.
3. **Books (PDF, no internet):** `get-pdf-text.py <pdf> <first> <last>` → text with `[p.N]` markers (ligatures drop). Ingest CHAPTER BY CHAPTER; cite `p.NN` (no timestamp). One Source note per book; ~5–7 chapter agents.
4. **Housekeeping each wave:** `regen-index.py` (rebuilds Authority Ledger from People-note YAML + MOC sources index); recompute the queue (drop any vid whose Source note already exists); `consolidation-scan.py` (broken-link/dupe report — note: scripture links with dots are fine). Sync loop auto-commits+pushes.

## PENDING WORK
**A. ✅ COMPLETE (2026-06-15) — all 6 PDF books ingested.** Pilot wave: Meyer (1 agent), Moody *Life After Life* (5). Main wave: Harris *Moral Landscape* (4), Ward *After Humanity* (7), Turek *Stealing from God* (8), Feser *Five Proofs* (10). Each = a Source note (+ author People note) authored up front, then chapter agents writing Concept/Scripture/People notes citing it. Reusable book-cache slices live in `scripts\bookcache\` (book-*-FULL.txt + per-chapter slices).
  - NOTE (no silent caps): Ward pp.~164–217 are **image-only** in the OceanofPDF file — a watermark-only facsimile, almost certainly Lewis's original *Abolition of Man* reproduced as page images. Skipped (not text-extractable). Ward's own line-by-line commentary on all three Lewis chapters + Appendix WAS ingested, so no argument is lost; if the primary-text facsimile is wanted, it needs OCR.
  - Harris note: he's the naturalist FOIL — his book notes carry an `## Apologetic Engagement` section (theistic/LDS response); Feser/Turek/Ward are linked there as grounding counters.

**B. ✅ DONE (2026-06-15) — TF Level-1 videos.** 35 of 37 in `course-l1-queue.txt` ingested (Ethics 1.3, God 1.4, Meaning 1.5, Challenges 1.6): one Source note + concept/scripture/people notes each, cited `[[Source|short]], [MM:SS], <url>`. **2 caption-disabled (no transcript, skipped):** `vybNvc6mxMo`, `xCwY36a19aQ`. New helper: `get-yt-meta.py <queue> --cached-only` (oEmbed title/channel — oEmbed still works under a transcript-API IP block). Fresh Proton IP yields only ~17–18 transcript fetches before re-blocking, so this needed 2 VPN rotations.
**C. 27 main-list videos** — `ingest-queue.txt`. (2 have captions disabled: WGzDRhLaBf4, cMOJ9Gfjq_4 — skip.)
**D. 3 debate maps left** (`Concepts\Debate - *.md`): Book of Mormon Historicity, BoM Witnesses, Problem of Hell. (Done: Trinity, Sola Scriptura, Joseph Smith.) Method: an agent reads relevant existing Concepts and writes a Debate-map note pairing claim⇄counter + authority tiers.
**E. Quality passes:** ✅ Broken-link cleanup done 2026-06-15 (463→114: fixed 217 line-split wikilinks via `fix-broken-links.py`, made `consolidation-scan.py` **alias-aware**, stubbed recurring entities in `Glossary\`; remaining ~114 are forward-links to not-yet-written concept notes — see `analyze-broken-links.py` for the A/B/C/D breakdown). Still TODO: write those recurring forward-link concepts (Book-of-Enoch cluster, "Great Apostasy", etc.); dedup/merge near-duplicate concepts; domain sub-MOCs; semantic index (`nomic-embed-text` already pulled); auto-populate the course hub + future TF Levels 2–4.

## Also pending
- **Restart the apologist gateway** so Discord/Mahonri uses the corrected memory+skills (it still holds stale in-memory state). Then Discord ASK works against hermes-advocate.
- Thoughtful Faith course **Levels 2, 3, 4** content not yet provided by Joseph.
