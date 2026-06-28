#!/usr/bin/env python
"""Semantic search over the vault index (meaning, not keywords).
Usage: semantic-search.py "your question" [N=12] [domain]"""
import sys, json, os, urllib.request
import numpy as np

OUT = r"C:\Users\Josep\AppData\Local\hermes\scripts\embeddings"
vecs = np.load(os.path.join(OUT, "vectors.npy"))
meta = json.load(open(os.path.join(OUT, "meta.json"), encoding="utf-8"))
q = sys.argv[1]
N = int(sys.argv[2]) if len(sys.argv) > 2 else 12
domain = sys.argv[3] if len(sys.argv) > 3 else None

req = urllib.request.Request("http://localhost:11434/api/embeddings",
      data=json.dumps({"model": "nomic-embed-text", "prompt": "search_query: " + q}).encode(),
      headers={"Content-Type": "application/json"})
qv = np.asarray(json.load(urllib.request.urlopen(req, timeout=60))["embedding"], dtype=np.float32)
vn = vecs / (np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-9)
sims = vn @ (qv / (np.linalg.norm(qv) + 1e-9))
order = np.argsort(-sims)
print(f'\nTop {N} for: "{q}"' + (f"  (domain={domain})" if domain else "") + "\n")
shown = 0
for i in order:
    m = meta[i]
    if domain and m["domain"] != domain: continue
    print(f"  {sims[i]:.3f}  [{m['domain']}]  {m['title']}")
    shown += 1
    if shown >= N: break
