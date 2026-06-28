#!/usr/bin/env python
"""Categorize every broken wikilink in the vault so fixes can be prioritized.
Categories:
  A MALFORMED  - link target contains a newline (wrapped across lines); a real bug.
  B ALIAS      - target matches an existing note's YAML alias (resolves in Obsidian; scan false-positive).
  C NEAR-MISS  - target fuzzy-matches an existing note basename >=0.88 (likely typo/variant; fixable).
  D PHANTOM    - genuinely no such note; candidate for stubbing (shown frequency-sorted).
Prints a report to stdout. Changes nothing."""
import re, os, glob, difflib
from collections import defaultdict

VAULT = r"C:\Users\Josep\hermes-advocate"
LINK_RE = re.compile(r"\[\[([^\]|#]+)")

notes = [p for p in glob.glob(os.path.join(VAULT, "**", "*.md"), recursive=True)
         if ".obsidian" not in p and "Consolidation Report" not in p]
basenames = {os.path.splitext(os.path.basename(p))[0] for p in notes}
basenames_lower = {b.lower() for b in basenames}

# gather aliases from frontmatter
alias_lower = set()
fm_re = re.compile(r"^---\n(.*?)\n---", re.S)
for p in notes:
    try:
        txt = open(p, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    m = fm_re.match(txt)
    if not m:
        continue
    fm = m.group(1)
    am = re.search(r"^aliases:\s*(.*)$((?:\n[ \t]+-.*)*)", fm, re.M)
    if am:
        inline = am.group(1)
        block = am.group(2) or ""
        for q in re.findall(r'"([^"]+)"|\'([^\']+)\'', inline):
            alias_lower.add((q[0] or q[1]).lower())
        for line in block.splitlines():
            s = line.strip().lstrip("-").strip().strip('"').strip("'")
            if s:
                alias_lower.add(s.lower())

A, B, C, D = [], [], [], []
Dfreq = defaultdict(int); Dfiles = defaultdict(list)
for p in notes:
    try:
        txt = open(p, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    txt = re.sub(r"```.*?```", "", txt, flags=re.S)
    txt = re.sub(r"`[^`\n]*`", "", txt)
    src = os.path.basename(p)
    for mm in LINK_RE.finditer(txt):
        raw = mm.group(1).strip()
        tgt = os.path.basename(raw)
        if tgt.lower().endswith(".md"):
            tgt = tgt[:-3]
        if "\n" in mm.group(1):
            A.append((src, mm.group(1).strip())); continue
        low = tgt.lower()
        if low in basenames_lower:
            continue  # resolves
        if low in alias_lower:
            B.append((src, tgt)); continue
        best = difflib.get_close_matches(tgt, basenames, n=1, cutoff=0.88)
        if best:
            C.append((src, tgt, best[0]))
        else:
            D.append((src, tgt)); Dfreq[tgt] += 1; Dfiles[tgt].append(src)

print(f"TOTAL broken (scan): {len(A)+len(B)+len(C)+len(D)}")
print(f"  A MALFORMED (newline-split, real bugs): {len(A)}")
print(f"  B ALIAS (false positives, resolve in Obsidian): {len(B)}")
print(f"  C NEAR-MISS (likely typo -> existing note): {len(C)}")
print(f"  D PHANTOM (no such note): {len(D)}  across {len(Dfreq)} distinct targets")

print("\n=== A: MALFORMED (fix by joining the wikilink onto one line) ===")
for src, raw in A:
    print(f"  [{src}]  ->  {raw!r}")

print("\n=== C: NEAR-MISS (retarget link to the matched note) ===")
for src, tgt, match in C:
    print(f"  [{src}]  [[{tgt}]]  ->  [[{match}]]")

print("\n=== B: ALIAS false-positives (distinct targets) ===")
for t in sorted(set(t for _, t in B)):
    print(f"  [[{t}]]")

print("\n=== D: PHANTOM targets by frequency (>=3 = stub candidates) ===")
for tgt, n in sorted(Dfreq.items(), key=lambda kv: (-kv[1], kv[0].lower())):
    flag = "  <== STUB" if n >= 3 else ""
    print(f"  {n:3d}  [[{tgt}]]{flag}")
