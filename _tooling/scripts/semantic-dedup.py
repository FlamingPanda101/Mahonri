#!/usr/bin/env python
"""Find semantic near-duplicate CONCEPT notes (high cosine, NOT already caught by
the title-similarity scan) for review. Usage: semantic-dedup.py [threshold=0.95] [maxpairs=80]"""
import sys, json, os, difflib
import numpy as np

OUT = r"C:\Users\Josep\AppData\Local\hermes\scripts\embeddings"
vecs = np.load(os.path.join(OUT, "vectors.npy"))
meta = json.load(open(os.path.join(OUT, "meta.json"), encoding="utf-8"))
thr = float(sys.argv[1]) if len(sys.argv) > 1 else 0.95
maxp = int(sys.argv[2]) if len(sys.argv) > 2 else 80

ci = [i for i, m in enumerate(meta)
      if m["rel"].startswith("Concepts/") and "/debate-maps/" not in m["rel"]]
V = vecs[ci]; M = [meta[i] for i in ci]
Vn = V / (np.linalg.norm(V, axis=1, keepdims=True) + 1e-9)
S = Vn @ Vn.T
np.fill_diagonal(S, 0.0)

pairs = []
n = len(M)
for a in range(n):
    for b in np.where(S[a] >= thr)[0]:
        if b <= a: continue
        ta, tb = M[a]["title"], M[b]["title"]
        tsim = difflib.SequenceMatcher(None, ta, tb).ratio()
        pairs.append((float(S[a][b]), tsim, M[a]["domain"], ta, M[b]["domain"], tb))
pairs.sort(reverse=True)

print(f"Semantic near-dup CONCEPT pairs (cosine >= {thr}): {len(pairs)} total\n"
      f"(tsim = title similarity; LOW tsim = the title-scan would MISS this dup)\n")
shown = 0
for cos, tsim, da, ta, db, tb in pairs:
    if tsim > 0.82:  # the consolidation-scan already flags these
        continue
    print(f"  cos={cos:.3f} tsim={tsim:.2f}  [{da}] vs [{db}]\n     A: {ta}\n     B: {tb}")
    shown += 1
    if shown >= maxp: break
print(f"\nShown {shown} title-distinct candidates (the ones worth a human/agent look).")
