#!/usr/bin/env python
"""Execute the domain shard: move each Concepts/<file> into Concepts/<domain>/ per
the manifest. Keeps Concepts.md at the Concepts/ root. Safe to re-run (skips
files already at their destination)."""
import os, shutil

CONC = r"C:\Users\Josep\hermes-advocate\Concepts"
MANIFEST = r"C:\Users\Josep\AppData\Local\hermes\scripts\_shard-manifest.tsv"

moved = skip = missing = 0
for line in open(MANIFEST, encoding="utf-8"):
    line = line.rstrip("\n")
    if not line:
        continue
    dom, base = line.split("\t", 1)
    src = os.path.join(CONC, base)
    dstdir = os.path.join(CONC, dom)
    os.makedirs(dstdir, exist_ok=True)
    dst = os.path.join(dstdir, base)
    if not os.path.exists(src):
        skip += 1 if os.path.exists(dst) else 0
        missing += 0 if os.path.exists(dst) else 1
        continue
    shutil.move(src, dst)
    moved += 1

print(f"moved={moved}  already-in-place={skip}  missing={missing}\n")
for d in sorted(os.listdir(CONC)):
    p = os.path.join(CONC, d)
    if os.path.isdir(p):
        n = len([x for x in os.listdir(p) if x.endswith(".md")])
        print(f"  {n:5d}  Concepts/{d}/")
root_md = [x for x in os.listdir(CONC) if x.endswith(".md")]
print(f"\nroot-level .md remaining (should be only Concepts.md): {root_md}")
