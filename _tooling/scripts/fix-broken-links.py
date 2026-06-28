#!/usr/bin/env python
"""One-off repair of broken wikilinks in the vault:
  A) collapse wikilinks that were split across a line (newline / '>' / indent inside [[...]]) — real bugs.
  C) retarget a few apostrophe/article typo links to the actual note filename.
Conservative: only touches text inside [[...]] pairs. Prints what it changed."""
import re, glob, os
VAULT = r"C:\Users\Josep\hermes-advocate"
notes = [p for p in glob.glob(os.path.join(VAULT, "**", "*.md"), recursive=True) if ".obsidian" not in p]

# C: (regex on the link target right after '[[')  ->  replacement.  Only safe punctuation/article variants
C_MAP = [
    (r"\[\[Atheism['‘’]s Four Bad Implications", "[[Atheisms Four Bad Implications"),
    (r"\[\[Decline of Women['‘’]s Roles in Early Christian Liturgy", "[[Decline of Womens Roles in Early Christian Liturgy"),
    (r"\[\[The Rise of the Monarchical Bishop", "[[Rise of the Monarchical Bishop"),
    (r"\[\[Monopoly Analogy for Life['‘’]s Purpose", "[[Monopoly Analogy for Lifes Purpose"),
]

def collapse(m):
    inner = m.group(1)
    if "\n" in inner:
        return "[[" + re.sub(r"[\s>]+", " ", inner).strip() + "]]"
    return m.group(0)

a_total = c_total = files_changed = 0
changed = []
for p in notes:
    txt = open(p, encoding="utf-8", errors="replace").read()
    orig = txt
    a_here = len(re.findall(r"\[\[[^\[\]]*?\n[^\[\]]*?\]\]", txt, flags=re.S))
    txt = re.sub(r"\[\[([^\[\]]+?)\]\]", collapse, txt, flags=re.S)
    c_here = 0
    for pat, repl in C_MAP:
        txt, n = re.subn(pat, repl, txt)
        c_here += n
    if txt != orig:
        open(p, "w", encoding="utf-8").write(txt)
        files_changed += 1
        a_total += a_here
        c_total += c_here
        changed.append((os.path.basename(p), a_here, c_here))

print(f"Files changed: {files_changed} | A malformed collapsed: {a_total} | C typos retargeted: {c_total}\n")
for name, a, c in sorted(changed):
    print(f"  {name}  (A:{a} C:{c})")
