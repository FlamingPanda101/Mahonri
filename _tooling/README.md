# _tooling — backup of the Hermes apologetics pipeline + Mahonri's brain

These are **version-controlled backup copies** of the machinery that builds and serves this
vault. The LIVE copies (what actually runs) live in `C:\Users\Josep\AppData\Local\hermes\` —
edit *those*; these are snapshots for disaster recovery and history.

## Contents
- `SOUL.md` — Mahonri's persona / operating instructions (the "brain"; live copy is
  `profiles\apologist\SOUL.md`).
- `scripts/` — the full pipeline (21 files):
  - **Ingest:** `get-yt-transcript.py`, `prefetch-transcripts.py`, `get-article.py`,
    `get-pdf-text.py`, `get-yt-meta.py`, `json3-to-txt.py`, `batch-ingest.ps1`
  - **Index / retrieval:** `build-embeddings.py` (nomic semantic index), `semantic-search.py`,
    `hybrid-search.py` (semantic + keyword rerank — what SOUL MODE 2 uses), `semantic-dedup.py`
  - **Maintenance:** `analyze-broken-links.py`, `resolve-links.py` (alias-aware, more accurate),
    `fix-broken-links.py`, `fix-audit-links.py`, `consolidation-scan.py`, `regen-index.py`,
    `shard-classify.py`, `shard-move.py`
  - **Ops:** `run-apologist-gateway.ps1` (start Mahonri), `sync-advocate-loop.ps1`
    (auto-commit+push, self-healing)

## NOT here (excluded by `.gitignore` — secrets / regenerable / huge)
- `.env`, `state.db*`, `gateway_state.json` — secrets + runtime state (**never** commit)
- `scripts/transcripts/` (~1,000 cached transcripts) and `scripts/embeddings/` (`vectors.npy`) — regenerable

## Refresh
These are snapshots. After editing a live script or the SOUL in AppData, re-copy:
```sh
cp "$LOCALAPPDATA/hermes/scripts/"*.py "$LOCALAPPDATA/hermes/scripts/"*.ps1 _tooling/scripts/
cp "$LOCALAPPDATA/hermes/profiles/apologist/SOUL.md" _tooling/SOUL.md
```
then commit. (Last synced: 2026-06-28.)
