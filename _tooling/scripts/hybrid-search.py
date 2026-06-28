#!/usr/bin/env python
"""Hybrid retrieval = semantic (nomic embeddings) reranked by keyword precision.
Semantic finds concepts by MEANING; keyword boosts notes that contain the query's
exact proper nouns / scripture refs / quoted phrases (which vectors blur). Reranks the
semantic shortlist, so an exact-name hit rises even when its cosine is mid-pack.
Usage: hybrid-search.py "the question" [N=12]   (falls back to pure semantic if the
query has no strong keyword terms — that's the right division of labor.)"""
import sys, os, re, json, urllib.request
import numpy as np

OUT   = r"C:\Users\Josep\AppData\Local\hermes\scripts\embeddings"
VAULT = r"C:\Users\Josep\hermes-advocate"
vecs  = np.load(os.path.join(OUT, "vectors.npy"))
meta  = json.load(open(os.path.join(OUT, "meta.json"), encoding="utf-8"))
q = sys.argv[1]
N = int(sys.argv[2]) if len(sys.argv) > 2 else 12
CAND, LAMBDA = 120, 0.5    # rerank the top-CAND semantic hits; keyword weight

# --- semantic cosine over the whole index (aligned with meta) ---
req = urllib.request.Request("http://localhost:11434/api/embeddings",
      data=json.dumps({"model": "nomic-embed-text", "prompt": "search_query: " + q}).encode(),
      headers={"Content-Type": "application/json"})
qv = np.asarray(json.load(urllib.request.urlopen(req, timeout=60))["embedding"], dtype=np.float32)
vn = vecs / (np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-9)
sem = vn @ (qv / (np.linalg.norm(qv) + 1e-9))

# --- strong keyword terms: quoted phrases, scripture refs, Proper Nouns ---
terms = set(re.findall(r'"([^"]+)"', q))
terms |= set(re.findall(r'\b[1-3]?\s?[A-Z][a-z]+\.?\s?\d+[:.]\d+\b', q))   # John 1:1 / 1 Nephi 3.7
terms |= set(re.findall(r'\b[A-Z][a-zA-Z]{3,}\b', q))                       # Plantinga, Nicaea
terms = [t.strip() for t in terms if len(t.strip()) >= 3]

cand = np.argsort(-sem)[:CAND]
s = sem[cand]
s_norm = (s - s.min()) / (s.max() - s.min() + 1e-9)
kw = np.zeros(len(cand))
for k, i in enumerate(cand):
    if not terms: break
    try: txt = open(os.path.join(VAULT, meta[i]["rel"]), encoding="utf-8", errors="replace").read().lower()
    except Exception: txt = ""
    title = meta[i]["title"].lower()
    kw[k] = sum(txt.count(t.lower()) for t in terms) + 3 * sum(t.lower() in title for t in terms)
kw_norm = kw / kw.max() if kw.max() > 0 else kw
final = s_norm + LAMBDA * kw_norm

order = np.argsort(-final)
print(f'\nHybrid top {N} for: "{q}"   (keyword terms: {terms or "none -> pure semantic"})\n')
for k in order[:N]:
    i = cand[k]
    flag = f" +kw{int(kw[k])}" if kw[k] > 0 else ""
    print(f"  {final[k]:.3f}  (sem {sem[i]:.3f}{flag})  [{meta[i]['domain']}]  {meta[i]['title']}")
