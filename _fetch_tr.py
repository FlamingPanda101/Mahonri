from youtube_transcript_api import YouTubeTranscriptApi
api = YouTubeTranscriptApi()
t = api.fetch('9OgkawwxnWw')
out = []
for s in t:
    m = int(s.start // 60); sec = int(s.start % 60)
    out.append(f'[{m:02d}:{sec:02d}] {s.text}')
with open(r'C:\Users\Josep\hermes-advocate\_transcript_9Ogk.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('LINES', len(out))
