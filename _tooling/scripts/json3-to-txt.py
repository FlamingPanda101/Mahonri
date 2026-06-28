#!/usr/bin/env python
"""Convert a YouTube json3 caption file into the pipeline's [MM:SS] 30s-bucket .txt format.
json3 events are discrete (no rolling-caption duplication), so no dedup needed.
Usage: json3-to-txt.py <file.en.json3>   (writes to stdout)"""
import sys, json

data = json.load(open(sys.argv[1], encoding="utf-8", errors="replace"))
buckets = {}
for ev in data.get("events", []):
    segs = ev.get("segs")
    if not segs:
        continue
    t = int(ev.get("tStartMs", 0)) // 1000
    text = "".join(s.get("utf8", "") for s in segs).replace("\n", " ").strip()
    if not text:
        continue
    bk = (t // 30) * 30
    buckets.setdefault(bk, []).append(text)

out = []
for bk in sorted(buckets):
    mm, ss = bk // 60, bk % 60
    line = " ".join(" ".join(buckets[bk]).split())
    out.append(f"[{mm:02d}:{ss:02d}] {line}")
sys.stdout.write("\n".join(out) + "\n")
