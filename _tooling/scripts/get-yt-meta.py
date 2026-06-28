#!/usr/bin/env python
"""Fetch YouTube title + channel via the public oEmbed endpoint (no API key, lightweight).
Usage: get-yt-meta.py <queuefile> [--cached-only]
Prints one line per video:  <vid>\t<channel>\t<title>
With --cached-only, only emits videos whose transcript is already cached (>200 bytes)."""
import sys, re, json, os, time, urllib.request, urllib.parse
CACHE = r"C:\Users\Josep\AppData\Local\hermes\scripts\transcripts"
args = [a for a in sys.argv[1:] if not a.startswith("--")]
cached_only = "--cached-only" in sys.argv
queue = args[0] if args else r"C:\Users\Josep\AppData\Local\hermes\scripts\ingest-queue.txt"

def vid(u):
    m = re.search(r'(?:youtu\.be/|/live/|/shorts/|v=)([A-Za-z0-9_-]{11})', u)
    if m: return m.group(1)
    return u if re.fullmatch(r'[A-Za-z0-9_-]{11}', u) else None

urls = [l.strip() for l in open(queue, encoding="utf-8") if l.strip() and not l.strip().startswith("#")]
for u in urls:
    v = vid(u)
    if not v:
        continue
    if cached_only:
        fp = os.path.join(CACHE, v + ".txt")
        if not (os.path.exists(fp) and os.path.getsize(fp) > 200):
            continue
    try:
        oe = "https://www.youtube.com/oembed?url=" + urllib.parse.quote("https://youtu.be/" + v, safe="") + "&format=json"
        req = urllib.request.Request(oe, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            d = json.load(r)
        title = (d.get("title", "") or "").replace("\t", " ").replace("\n", " ").strip()
        author = (d.get("author_name", "") or "").replace("\t", " ").strip()
        print(f"{v}\t{author}\t{title}")
    except Exception as e:
        print(f"{v}\tERROR\t{str(e)[:80]}")
    time.sleep(1)
