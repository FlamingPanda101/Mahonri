#!/usr/bin/env python
"""Fetch and extract clean article text (with title/author/date metadata).
Usage: get-article.py <url>"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
import trafilatura

if len(sys.argv) < 2:
    print("usage: get-article.py <url>")
    sys.exit(1)
url = sys.argv[1]
try:
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        print("ERROR: could not fetch URL")
        sys.exit(2)
    text = trafilatura.extract(downloaded, include_comments=False,
                               include_tables=True, with_metadata=True)
    if not text:
        print("ERROR: could not extract article text")
        sys.exit(3)
    print(text)
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(4)
