#!/usr/bin/env python3
"""Write data/portugueseAudio.json from the SEC archive's own listing.

    python3 scripts/markbank/authoring/pt_audio.py

CARD-STANDARD 10g (coordinator, 19 Nov 2026): the recording names come from
the archive listing saved 31 Aug 2026 (sources-tools/sec-archive-manifest-
20260831.jsonl), never typed and never built from a pattern. Each year's
"Sound File" row for Portuguese (subjectId 18) gives the file id; the
address is the archive's exampapers path for that year, as Polish and German
carry it. Nothing is fetched (the archive blocks this Mac since 19 Nov).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
MANIFEST = ('/Users/alexlinehan/Documents/NextStepUni-MarkBank-Lanes-20261104/sources-tools/'
            'sec-archive-manifest-20260831.jsonl')
OUT = os.path.join(ROOT, 'data', 'portugueseAudio.json')
ARCHIVE = 'https://www.examinations.ie/archive/exampapers'


def sound_rows():
    rows = []
    with open(MANIFEST, encoding='utf-8') as fh:
        for line in fh:
            if not line.strip():
                continue
            r = json.loads(line)
            if (r.get('subjectName') == 'Portuguese' and r.get('exam') == 'lc'
                    and r.get('view') == 'exampapers' and str(r.get('label', '')).startswith('Sound File')):
                rows.append(r)
    return rows


def main():
    rows = sound_rows()
    by_year = {}
    for r in rows:
        if r['year'] in by_year:
            raise SystemExit(f'two Sound File rows for {r["year"]}: {by_year[r["year"]]["fileid"]}, {r["fileid"]}')
        by_year[r['year']] = r
    out = []
    for year in sorted(by_year, reverse=True):
        r = by_year[year]
        url = f'{ARCHIVE}/{year}/{r["fileid"]}'
        out.append({
            'year': int(year),
            'paperFileids': ['LC018ALPA00EV.pdf', 'LC018GLPA00EV.pdf'],
            'source': {
                'kind': 'source-audio',
                'label': 'Portuguese listening',
                'title': f'{year} Portuguese · Listening Comprehension Test',
                'playbackUrl': url,
                'secFileid': r['fileid'],
                'canonicalUrl': url,
                'attribution': '© State Examinations Commission.',
                'presentationNote': ('Full official recording · Partes A–E, Higher and Ordinary Level. '
                                     'Use the player to pause, replay or move through the recording.'),
            },
            'verification': {
                'listedAt': '2026-08-31',
                'listing': 'sources-tools/sec-archive-manifest-20260831.jsonl',
                'listingRow': {k: r[k] for k in ('view', 'exam', 'year', 'subjectId', 'fileid', 'label')},
                'method': ('File name read from the SEC archive\'s own listing (CARD-STANDARD 10g, coordinator '
                           'ruling 19 Nov 2026). Not fetched or downloaded: the archive has blocked this Mac '
                           'since 19 Nov 11:19 UTC; the audio-hosting lane confirms and uploads the copy.'),
            },
        })
    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    print(f'{OUT}: {len(out)} years', [o['year'] for o in out])


if __name__ == '__main__':
    main()
