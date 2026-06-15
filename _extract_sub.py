import json, urllib.request, sys

with open(r'C:\Users\Josep\hermes-advocate\_yt_9OgkawwxnWw.info.json', encoding='utf-8') as f:
    info = json.load(f)

cands = []
for key in ('subtitles', 'automatic_captions'):
    d = info.get(key) or {}
    for lang in ('en', 'en-orig', 'en-US'):
        if lang in d:
            for fmt in d[lang]:
                cands.append((key, lang, fmt.get('ext'), fmt.get('url')))

# prefer json3 or vtt
def score(c):
    ext = c[2] or ''
    return {'json3':0, 'vtt':1, 'srv3':2}.get(ext, 5)
cands.sort(key=score)
print('CANDIDATES:', [(c[0],c[1],c[2]) for c in cands][:10])

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
for src, lang, ext, url in cands:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': ua})
        data = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')
        if len(data) > 200:
            open(r'C:\Users\Josep\hermes-advocate\_sub_raw.txt', 'w', encoding='utf-8').write(data)
            print('OK', src, lang, ext, 'len', len(data))
            sys.exit(0)
    except Exception as e:
        print('FAIL', src, lang, ext, repr(e)[:120])
print('ALL FAILED')
sys.exit(1)
