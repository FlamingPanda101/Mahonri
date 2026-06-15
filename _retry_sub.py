import json, urllib.request, sys, time

with open(r'C:\Users\Josep\hermes-advocate\_yt_9OgkawwxnWw.info.json', encoding='utf-8') as f:
    info = json.load(f)

ac = info.get('automatic_captions') or {}
url = None
for lang in ('en', 'en-orig'):
    for fmt in ac.get(lang, []):
        if fmt.get('ext') == 'json3':
            url = fmt['url']; break
    if url: break

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
for attempt in range(6):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': ua, 'Accept-Language': 'en-US,en'})
        data = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')
        if len(data) > 200:
            open(r'C:\Users\Josep\hermes-advocate\_sub_raw.json', 'w', encoding='utf-8').write(data)
            print('OK len', len(data)); sys.exit(0)
        print('short', len(data))
    except Exception as e:
        print('attempt', attempt, repr(e)[:80])
    time.sleep(20)
sys.exit(1)
