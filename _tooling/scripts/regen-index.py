#!/usr/bin/env python
"""Regenerate Authority Ledger (from People-note YAML) + Apologetics MOC (sources index)."""
import re, glob, os
V = r"C:\Users\Josep\hermes-advocate"
def fm(t):
    if not t.startswith("---"): return ""
    e=t.find("\n---",3); return t[:e] if e!=-1 else ""
def field(f,k):
    m=re.search(rf'^{k}:\s*(.+)$', f, re.M); return m.group(1).strip().strip('"').strip("'") if m else ""
rows=[]
for p in glob.glob(os.path.join(V,"People","*.md")):
    f=fm(open(p,encoding="utf-8",errors="replace").read())
    a=field(f,"authority").upper()
    if a in ("A","B","C","D"):
        rows.append((a, os.path.splitext(os.path.basename(p))[0], field(f,"authority_reason")))
o={"A":0,"B":1,"C":2,"D":3}; rows.sort(key=lambda r:(o[r[0]], r[1].lower()))
led=["# Authority Ledger","","Vetted author/work ratings. **Auto-generated from each People note's YAML** (`authority:` + `authority_reason:`).","",
"**Tiers:** A = peer-reviewed / primary / university-press · B = credentialed expert · C = informed, cited commentary · D = opinion / uncited","",
"| Author / Work | Tier | Field / Notes |","|---|------|---------------|"]
led += [f"| [[{n}]] | {a} | {r} |" for a,n,r in rows] + ["","---","See also: [[Home]]"]
open(os.path.join(V,"99-meta","Authority Ledger.md"),"w",encoding="utf-8").write("\n".join(led)+"\n")
srcs=[]
for p in glob.glob(os.path.join(V,"Sources","*.md")):
    f=fm(open(p,encoding="utf-8",errors="replace").read())
    topics=", ".join(sorted(set(re.findall(r'topic/([a-z0-9-]+)', f))))
    srcs.append((os.path.splitext(os.path.basename(p))[0], field(f,"authority") or "?", topics))
srcs.sort(key=lambda s:s[0].lower())
moc=["---","title: Apologetics","tags: [moc]","---","","# Apologetics — Map of Content","",
f"Auto-generated index. **{len(srcs)} sources** ingested. Browse Concepts / Scriptures / People folders or the graph; author tiers in [[Authority Ledger]]; channels in [[Sources Index]].","",
"## Sources Ingested","","| Source | Tier | Topics |","|--------|------|--------|"]
moc += [f"| [[{n}]] | {a} | {t} |" for n,a,t in srcs] + ["","---","See also: [[Home]] · [[Sources Index]] · [[Authority Ledger]]"]
open(os.path.join(V,"MOCs","Apologetics.md"),"w",encoding="utf-8").write("\n".join(moc)+"\n")
print(f"Ledger: {len(rows)} scholars (A:{sum(1 for a,_,_ in rows if a=='A')} B:{sum(1 for a,_,_ in rows if a=='B')} C:{sum(1 for a,_,_ in rows if a=='C')} D:{sum(1 for a,_,_ in rows if a=='D')}) | MOC: {len(srcs)} sources")
