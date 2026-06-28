#!/usr/bin/env python
"""Extract text from a PDF (book/article). Usage: get-pdf-text.py <path> [first_page] [last_page]
Page range is 1-based and optional - use it to feed big books a chapter at a time."""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from pypdf import PdfReader

if len(sys.argv) < 2:
    print("usage: get-pdf-text.py <path-to-pdf> [first_page] [last_page]")
    sys.exit(1)
try:
    reader = PdfReader(sys.argv[1])
    n = len(reader.pages)
    first = (int(sys.argv[2]) - 1) if len(sys.argv) > 2 else 0
    last = int(sys.argv[3]) if len(sys.argv) > 3 else n
    parts = []
    for i in range(max(0, first), min(n, last)):
        parts.append(f"[p.{i + 1}]\n" + (reader.pages[i].extract_text() or ""))
    out = "\n\n".join(parts).strip()
    print(f"[pages {max(1, first+1)}-{min(n, last)} of {n}]\n")
    print(out if out else "(no extractable text - PDF may be scanned images; OCR needed)")
except Exception as e:
    print(f"ERROR reading PDF: {e}")
    sys.exit(2)
