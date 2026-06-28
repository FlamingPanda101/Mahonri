#!/usr/bin/env python
"""Build a semantic index of the vault: BATCH-embed every substantive note (Concepts,
Sources, People, Scriptures, Questions) via ollama `nomic-embed-text` (/api/embed),
store vectors (.npy) + parallel metadata (.json). INCREMENTAL: re-runs only re-embed
new/changed notes (by mtime). Batched at 64 -> ~48x faster than per-note calls.
Usage: build-embeddings.py"""
import os, re, json, glob, time, urllib.request
import numpy as np

VAULT = r"C:\Users\Josep\hermes-advocate"
OUT   = r"C:\Users\Josep\AppData\Local\hermes\scripts\embeddings"
os.makedirs(OUT, exist_ok=True)
VEC, META = os.path.join(OUT, "vectors.npy"), os.path.join(OUT, "meta.json")
EMBED_URL, MODEL, BATCH = "http://localhost:11434/api/embed", "nomic-embed-text", 64
SKIP_TOP = {"99-meta", "MOCs"}   # Glossary now indexed (labeled [Glossary]) so "define X" queries retrieve it
SKIP_BASE = {"Concepts", "People", "Scriptures", "Sources", "Sources Index", "Home", "Apologetics"}

def embed_batch(texts, retries=4):
    data = json.dumps({"model": MODEL, "input": texts, "keep_alive": "30m"}).encode()
    for i in range(retries):
        try:
            req = urllib.request.Request(EMBED_URL, data=data, headers={"Content-Type": "application/json"})
            embs = json.load(urllib.request.urlopen(req, timeout=300)).get("embeddings")
            if embs and len(embs) == len(texts):
                return embs
        except Exception:
            if i == retries - 1: raise
            time.sleep(2)

def note_text(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    name = os.path.splitext(os.path.basename(path))[0]
    body = re.sub(r'^---\n.*?\n---\n', '', t, flags=re.S)
    body = re.split(r'\n## References|\n\[\^\d+\]:|\n---\nSee also', body)[0]
    return "search_document: " + (name + "\n" + body)[:2960]   # nomic asymmetric-retrieval prefix

notes = []
for p in glob.glob(os.path.join(VAULT, "**", "*.md"), recursive=True):
    if ".obsidian" in p: continue
    rel = os.path.relpath(p, VAULT).replace("\\", "/")
    parts = rel.split("/")
    if parts[0] in SKIP_TOP or os.path.splitext(parts[-1])[0] in SKIP_BASE: continue
    notes.append((rel, p, os.path.getmtime(p)))

old_meta, old_vecs = [], None
if os.path.exists(META) and os.path.exists(VEC):
    old_meta = json.load(open(META, encoding="utf-8")); old_vecs = np.load(VEC)
old_by_rel = {m["rel"]: (i, m) for i, m in enumerate(old_meta)}

# plan: which notes reuse an old vector vs need embedding
slots = []          # per note: ("reuse", oldvec) or ("embed", text)
todo_idx, todo_text = [], []
for k, (rel, p, mt) in enumerate(notes):
    prev = old_by_rel.get(rel)
    if prev and abs(prev[1].get("mtime", 0) - mt) < 1 and old_vecs is not None:
        slots.append(("reuse", old_vecs[prev[0]], prev[1]))
    else:
        parts = rel.split("/")
        domain = parts[1] if parts[0] == "Concepts" and len(parts) > 2 else parts[0]
        slots.append(["embed", None, {"rel": rel, "title": os.path.splitext(parts[-1])[0], "domain": domain, "mtime": mt}])
        todo_idx.append(k); todo_text.append(note_text(p))

print(f"{len(notes)} notes | reuse={len(notes)-len(todo_idx)} embed={len(todo_idx)}", flush=True)
t0 = time.time()
for b in range(0, len(todo_idx), BATCH):
    chunk = todo_text[b:b+BATCH]
    embs = embed_batch(chunk)
    for j, v in enumerate(embs):
        slots[todo_idx[b+j]][1] = np.asarray(v, dtype=np.float32)
    if (b // BATCH) % 5 == 0:
        print(f"  embedded {min(b+BATCH,len(todo_idx))}/{len(todo_idx)}  {time.time()-t0:.0f}s", flush=True)

rows = [s[1] for s in slots]
meta = [s[2] for s in slots]
arr = np.vstack(rows).astype(np.float32)
np.save(VEC, arr); json.dump(meta, open(META, "w", encoding="utf-8"))
print(f"DONE: {len(meta)} notes indexed -> {arr.shape} in {time.time()-t0:.0f}s", flush=True)
