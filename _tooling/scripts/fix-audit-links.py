#!/usr/bin/env python
"""One-off: fix the mechanical broken links the quality audit surfaced —
retarget the 'Without Body' near-miss and strip erroneous .md suffixes — using
99-meta/_broken-links.json for the file list. Only touches wikilink targets."""
import json, os
VAULT = r"C:\Users\Josep\hermes-advocate"
REPL = {
  "'Without Body, Parts, or Passions' Is a 1530 Protestant Creed, Not Ancient": "Without Body Parts or Passions Is a 1530 Protestant Creed",
  "D&C 68.md": "D&C 68",
  "Proverbs.md": "Proverbs",
  "D&C 26.md": "D&C 26",
  "Exodus 32.md": "Exodus 32",
  "D&C 76.md": "D&C 76",
}
data = json.load(open(os.path.join(VAULT, "99-meta", "_broken-links.json"), encoding="utf-8"))
total = 0
for tgt, repl in REPL.items():
    for rel in sorted(set(data.get(tgt, []))):
        p = os.path.join(VAULT, rel)
        if not os.path.exists(p): continue
        t = open(p, encoding="utf-8").read()
        n = t.count("[[" + tgt)
        t2 = t.replace("[[" + tgt + "]]", "[[" + repl + "]]").replace("[[" + tgt + "|", "[[" + repl + "|")
        if t2 != t:
            open(p, "w", encoding="utf-8").write(t2)
            print(f"  {rel}: {n}x [[{tgt}]] -> [[{repl}]]")
            total += n
print(f"TOTAL wikilinks fixed: {total}")
