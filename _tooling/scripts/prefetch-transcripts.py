#!/usr/bin/env python
"""Prefetch YouTube transcripts SEQUENTIALLY (paced) into a cache dir, so the
rate-limited fetch step never bursts. Build-agents then read from cache (no YouTube calls).
Usage: prefetch-transcripts.py [N]   (default: next 20 from ingest-queue.txt)"""
import sys, re, os, time, subprocess
PY     = r"C:\Users\Josep\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"
SCRIPT = r"C:\Users\Josep\AppData\Local\hermes\scripts\get-yt-transcript.py"
QUEUE  = r"C:\Users\Josep\AppData\Local\hermes\scripts\ingest-queue.txt"
CACHE  = r"C:\Users\Josep\AppData\Local\hermes\scripts\transcripts"
DELAY  = 4
os.makedirs(CACHE, exist_ok=True)
n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
if len(sys.argv) > 2: QUEUE = sys.argv[2]
def vid(u):
    m = re.search(r'(?:youtu\.be/|/live/|v=)([A-Za-z0-9_-]{11})', u); return m.group(1) if m else None
urls = [l.strip() for l in open(QUEUE, encoding="utf-8") if l.strip() and not l.strip().startswith("#")][:n]
ok=[]; cached=[]; fail=[]
for u in urls:
    v = vid(u)
    if not v: continue
    fp = os.path.join(CACHE, v + ".txt")
    if os.path.exists(fp) and os.path.getsize(fp) > 200:
        cached.append(v); continue
    r = subprocess.run([PY, SCRIPT, u], capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = r.stdout or ""
    if out.startswith("ERROR") or "blocking requests from your IP" in out or len(out.strip()) < 200:
        fail.append((v, (out.strip()[:70].replace("\n"," ") or "empty")))
    else:
        open(fp, "w", encoding="utf-8").write(out); ok.append(v)
    time.sleep(DELAY)
print(f"PREFETCH: {len(ok)} newly cached | {len(cached)} already cached | {len(fail)} failed")
for v in ok: print("  OK   ", v)
for v,e in fail: print("  FAIL ", v, "|", e)
