#!/usr/bin/env python
"""Fetch a YouTube transcript as text with [MM:SS] markers ~every 30s (for citing).
Usage: get-yt-transcript.py <url|id>"""
import sys, re
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from youtube_transcript_api import YouTubeTranscriptApi


def video_id(s):
    m = re.search(r"(?:v=|youtu\.be/|/shorts/|/embed/|/live/)([A-Za-z0-9_-]{11})", s)
    if m:
        return m.group(1)
    return s if re.fullmatch(r"[A-Za-z0-9_-]{11}", s) else None


def fmt_ts(sec):
    return f"[{int(sec // 60):02d}:{int(sec % 60):02d}]"


def segments(vid):
    # youtube-transcript-api 1.x: instance .fetch(); errors propagate (no dead legacy fallback to mask them)
    for s in YouTubeTranscriptApi().fetch(vid):
        if isinstance(s, dict):
            yield s.get("start", 0.0), s.get("text", "")
        else:
            yield getattr(s, "start", 0.0), getattr(s, "text", "")


def get_text(vid):
    out, next_mark = [], 0
    for start, text in segments(vid):
        if start >= next_mark:
            out.append(f"\n{fmt_ts(start)} ")
            next_mark = (int(start) // 30 + 1) * 30
        out.append(text.strip() + " ")
    return "".join(out).strip()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: get-yt-transcript.py <youtube_url_or_id>")
        sys.exit(1)
    vid = video_id(sys.argv[1])
    if not vid:
        print("ERROR: could not parse a video ID from:", sys.argv[1])
        sys.exit(2)
    try:
        print(get_text(vid))
    except Exception as e:
        print(f"ERROR fetching transcript: {e}")
        sys.exit(3)
