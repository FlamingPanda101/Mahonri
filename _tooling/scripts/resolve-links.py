#!/usr/bin/env python
"""Alias-aware broken-link resolver. A [[target]] is TRULY broken only if it matches
neither a note basename NOR any note's YAML alias (Obsidian resolves both). This is
more accurate than analyze-broken-links.py, whose "category B" lumps real breaks in
with alias-resolved false-positives. Reports true breaks by frequency.
Usage: resolve-links.py [vault]   (add --fix-list to emit a json of target->files)"""
import os, re, glob, sys, json
from collections import Counter, defaultdict

VAULT = r"C:\Users\Josep\hermes-advocate"
args = [a for a in sys.argv[1:] if not a.startswith("--")]
if args: VAULT = args[0]
EMIT = "--fix-list" in sys.argv

files = [f for f in glob.glob(os.path.join(VAULT, "**", "*.md"), recursive=True)
         if ".obsidian" not in f and os.sep + ".trash" not in f]

def parse_aliases(text):
    m = re.match(r'^---\n(.*?)\n---', text, re.S)
    if not m: return []
    fm, out = m.group(1), []
    am = re.search(r'^aliases:\s*\[(.*?)\]', fm, re.M)
    if am:
        out += [x.strip().strip('"\'') for x in am.group(1).split(',')]
    bm = re.search(r'^aliases:\s*\n((?:[ \t]*-[ \t]*.*\n?)+)', fm, re.M)
    if bm:
        out += [re.sub(r'^[ \t]*-[ \t]*', '', l).strip().strip('"\'') for l in bm.group(1).splitlines()]
    return [a for a in out if a]

names, aliases = set(), {}
texts = {}
for f in files:
    try: texts[f] = open(f, encoding="utf-8", errors="replace").read()
    except: texts[f] = ""
    names.add(os.path.splitext(os.path.basename(f))[0])
for f in files:
    for a in parse_aliases(texts[f]):
        aliases[a.lower()] = os.path.basename(f)

resolvable = {n.lower() for n in names} | set(aliases.keys())
link_re = re.compile(r'\[\[([^\]\|#\^]+)')
broken, where = Counter(), defaultdict(list)
for f in files:
    if os.sep + "99-meta" + os.sep in f: continue   # docs (Protocol/RESUME/Consolidation) hold illustrative [[examples]], not real links
    for m in link_re.finditer(texts[f]):
        tgt = m.group(1).strip()
        if not tgt: continue
        base = re.split(r'[\\/]', tgt)[-1]   # path-qualified [[Folder/Note]] -> Obsidian resolves by basename
        if tgt.lower() in resolvable or base.lower() in resolvable:
            continue
        broken[tgt] += 1
        where[tgt].append(os.path.relpath(f, VAULT).replace("\\", "/"))

print(f"notes={len(files)}  names={len(names)}  aliases={len(aliases)}")
print(f"TRUE broken targets: {len(broken)}   (total broken link instances: {sum(broken.values())})\n")
for tgt, n in broken.most_common(60):
    print(f"  {n:3}x  [[{tgt}]]")
if EMIT:
    json.dump({t: where[t] for t, _ in broken.most_common()},
              open(os.path.join(VAULT, "99-meta", "_broken-links.json"), "w", encoding="utf-8"), indent=1)
    print("\n-> wrote 99-meta/_broken-links.json")
