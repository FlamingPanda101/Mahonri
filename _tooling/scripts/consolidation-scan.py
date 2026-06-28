#!/usr/bin/env python
"""Scan the apologetics vault for rot and write a review report.
DETECTS (does NOT auto-fix): likely duplicate concept notes, broken wikilinks,
and orphan notes. Run daily; review the report and merge manually / via Mahonri."""
import sys, re, os, glob, difflib, datetime
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

VAULT = r"C:\Users\Josep\hermes-advocate"
REPORT = os.path.join(VAULT, "99-meta", "Consolidation Report.md")
LINK_RE = re.compile(r"\[\[([^\]|#]+)")

def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()

notes = [p for p in glob.glob(os.path.join(VAULT, "**", "*.md"), recursive=True)
         if ".obsidian" not in p and "Consolidation Report" not in p]
basenames = {os.path.splitext(os.path.basename(p))[0] for p in notes}
basenames_lower = {b.lower() for b in basenames}
concepts = [p for p in notes if os.sep + "Concepts" + os.sep in p]

# gather YAML aliases so alias-links aren't falsely flagged as broken (Obsidian resolves them)
_FM = re.compile(r"^---\n(.*?)\n---", re.S)
alias_lower = set()
for p in notes:
    try:
        t = open(p, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    fmm = _FM.match(t)
    if not fmm:
        continue
    am = re.search(r"^aliases:\s*(.*)$((?:\n[ \t]+-.*)*)", fmm.group(1), re.M)
    if am:
        for q in re.findall(r'"([^"]+)"|\'([^\']+)\'', am.group(1)):
            alias_lower.add((q[0] or q[1]).lower())
        for ln in (am.group(2) or "").splitlines():
            s = ln.strip().lstrip("-").strip().strip('"').strip("'")
            if s:
                alias_lower.add(s.lower())

# 1. likely-duplicate concept titles (fuzzy match - catches obvious dupes only)
titles = [os.path.splitext(os.path.basename(p))[0] for p in concepts]
dupes = []
for i in range(len(titles)):
    for j in range(i + 1, len(titles)):
        r = difflib.SequenceMatcher(None, norm(titles[i]), norm(titles[j])).ratio()
        if r >= 0.82:
            dupes.append((round(r, 2), titles[i], titles[j]))
dupes.sort(reverse=True)

# 2. broken wikilinks + inbound counts
inbound = {b: 0 for b in basenames}
broken = []
for p in notes:
    try:
        txt = open(p, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    # strip code (fenced + inline) so example [[links]] in docs aren't counted — matches Obsidian
    txt = re.sub(r"```.*?```", "", txt, flags=re.S)
    txt = re.sub(r"`[^`\n]*`", "", txt)
    for m in LINK_RE.finditer(txt):
        tgt = os.path.basename(m.group(1).strip())
        if tgt.lower().endswith(".md"):
            tgt = tgt[:-3]  # strip ONLY the .md ext; keep dotted verse refs like "1 John 5.7"
        if tgt.lower() in basenames_lower:
            if tgt in inbound:
                inbound[tgt] += 1
        elif tgt.lower() in alias_lower:
            pass  # resolves via an existing note's YAML alias (Obsidian resolves these)
        else:
            broken.append((os.path.basename(p), m.group(1).strip()))

# 3. orphan concept notes (no inbound links AND no outbound links)
orphans = []
for p in concepts:
    base = os.path.splitext(os.path.basename(p))[0]
    try:
        txt = open(p, encoding="utf-8", errors="replace").read()
    except Exception:
        txt = ""
    if inbound.get(base, 0) == 0 and not LINK_RE.search(txt):
        orphans.append(base)

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
lines = [f"# Consolidation Report", "", f"*Scanned {now} — {len(concepts)} concept notes.*",
         "", "Auto-detected. **Nothing was changed** — review and merge via Mahonri "
         "(tell it: merge note X into note Y) or by hand.", "",
         f"## Likely duplicate concepts ({len(dupes)})"]
lines += [f"- `{a}` ↔ `{b}`  (similarity {r})" for r, a, b in dupes] or ["- none"]
lines += ["", f"## Broken wiki-links ({len(broken)})"]
lines += [f"- in **{src}** → `[[{tgt}]]` (no such note)" for src, tgt in broken[:50]] or ["- none"]
lines += ["", f"## Orphan concepts — no links in or out ({len(orphans)})"]
lines += [f"- [[{o}]]" for o in orphans] or ["- none"]
lines += ["", "---", "See also: [[Home]]"]

os.makedirs(os.path.dirname(REPORT), exist_ok=True)
open(REPORT, "w", encoding="utf-8").write("\n".join(lines))
print(f"Report written: {len(dupes)} dupe candidates, {len(broken)} broken links, {len(orphans)} orphans.")
