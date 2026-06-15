# RESUME — Apologetics Library Build (handoff for a fresh session)

State as of 2026-06-15. The vault is git-backed + auto-pushed by `sync-advocate-loop.ps1`. To continue in a NEW session, read this file first.

## Where things stand
~93 sources, ~1,100+ Concepts, ~410 Scriptures, ~530 People, 346-scholar Authority Ledger. *Ancient Christians* book fully ingested. Thoughtful Faith course: hub built ([[Thoughtful Faith Apologetics Course]]); 18/55 Level-1 videos done.

## The pipeline (all reusable; scripts in `C:\Users\Josep\AppData\Local\hermes\scripts\`)
Python venv: `C:\Users\Josep\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe`
1. **Prefetch transcripts (paced, block-safe):** `prefetch-transcripts.py <N> <queuefile>` → caches to `scripts\transcripts\<vid>.txt`. YouTube IP-blocks after ~20–35 fetches per window — if all fail, **rotate the Proton VPN to a new server** (fresh IP) and retry.
2. **Build (parallel):** spawn N general-purpose agents, one per cached vid. Each: READ `scripts\transcripts\<vid>.txt` (no internet), write deep notes to `hermes-advocate\` FLAT folders (Sources/Concepts/Scriptures/People). Rules: tags lowercase-hyphenated-NO-SPACES; citations `[^n]: [[Source|Title]], [MM:SS], <url>`; ≥2 wikilinks/note; **parallelism rule** = if a Scripture/People note already exists, wikilink only (don't edit); **NEVER touch** `99-meta\`, `MOCs\`, or other sources' notes.
3. **Books (PDF, no internet):** `get-pdf-text.py <pdf> <first> <last>` → text with `[p.N]` markers (ligatures drop). Ingest CHAPTER BY CHAPTER; cite `p.NN` (no timestamp). One Source note per book; ~5–7 chapter agents.
4. **Housekeeping each wave:** `regen-index.py` (rebuilds Authority Ledger from People-note YAML + MOC sources index); recompute the queue (drop any vid whose Source note already exists); `consolidation-scan.py` (broken-link/dupe report — note: scripture links with dots are fine). Sync loop auto-commits+pushes.

## PENDING WORK
**A. 6 PDF books** (in `C:\Users\Josep\Downloads\`, NO internet needed — do these first in a fresh session):
- `The_Moral_Landscape__How_Science_Can_Determine_Human_Values.pdf` → tag course/tf-level-1, topic/ethics (Harris)
- `_OceanofPDF.com_After_Humanity_-_Michael_Ward.pdf` → course/tf-level-1, topic/ethics (Ward, on Lewis's *Abolition of Man*)
- `_OceanofPDF.com_Stealing_from_God_-_Frank_Turek.pdf` → course/tf-level-1, topic/existence-of-god
- `_OceanofPDF.com_Five_Proofs_of_the_Existence_of_God_-_Edward_Feser.pdf` → course/tf-level-1, topic/existence-of-god
- `Meyer-SciEvidforCreatorsm2.pdf` → course/tf-level-1, topic/existence-of-god (Stephen Meyer)
- `_OceanofPDF.com_Life_After_Life_-_Raymond_A_Moody_Jr.pdf` → course/tf-level-1, topic/afterlife (NDEs)

**B. 37 Thoughtful Faith Level-1 videos** — `course-l1-queue.txt` (rest of Ethics 1.3, all of God 1.4, Meaning 1.5, Challenges 1.6). Needs fresh IP. Tag `course/tf-level-1` + topic/<ethics|existence-of-god|meaning|challenges>.
**C. 27 main-list videos** — `ingest-queue.txt`. (2 have captions disabled: WGzDRhLaBf4, cMOJ9Gfjq_4 — skip.)
**D. 3 debate maps left** (`Concepts\Debate - *.md`): Book of Mormon Historicity, BoM Witnesses, Problem of Hell. (Done: Trinity, Sola Scriptura, Joseph Smith.) Method: an agent reads relevant existing Concepts and writes a Debate-map note pairing claim⇄counter + authority tiers.
**E. Quality passes:** dedup/merge near-duplicate concepts; domain sub-MOCs; semantic index (`nomic-embed-text` already pulled — Obsidian Smart Connections plugin or a Hermes-side index); stub recurring phantom links; auto-populate the course hub + future TF Levels 2–4.

## Also pending
- **Restart the apologist gateway** so Discord/Mahonri uses the corrected memory+skills (it still holds stale in-memory state). Then Discord ASK works against hermes-advocate.
- Thoughtful Faith course **Levels 2, 3, 4** content not yet provided by Joseph.
