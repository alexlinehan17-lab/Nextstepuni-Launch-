#!/usr/bin/env python3
"""Write data/lithuanianAudio.json from the SEC archive's own listing.

    python3 scripts/markbank/authoring/lt_audio.py

CARD-STANDARD 10g (coordinator, 19 Nov 2026; Lithuanian, 20 Nov 2026): the
recording names come from the archive listing saved 31 Aug 2026
(sources-tools/sec-archive-manifest-20260831.jsonl), never typed and never
built from a pattern. Each year's "Sound File" row for Lithuanian (subjectId
550) gives the file id, and the same year's "Aural Paper" rows give the
listening booklets it belongs to. The address is the archive's exampapers path
for that year, as Portuguese, Polish and German carry it. Nothing is fetched
(the archive blocks this Mac since 19 Nov). pt_audio.py is the model.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
MANIFEST = ('/Users/alexlinehan/Documents/NextStepUni-MarkBank-Lanes-20261104/sources-tools/'
            'sec-archive-manifest-20260831.jsonl')
OUT = os.path.join(ROOT, 'data', 'lithuanianAudio.json')
ARCHIVE = 'https://www.examinations.ie/archive/exampapers'
SUBJECT = 'Lithuanian'


def listing_rows():
    rows = []
    with open(MANIFEST, encoding='utf-8') as fh:
        for line in fh:
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get('subjectName') == SUBJECT and r.get('exam') == 'lc' and r.get('view') == 'exampapers':
                rows.append(r)
    return rows


def main():
    rows = listing_rows()
    sound, aural = {}, {}
    for r in rows:
        label = str(r.get('label', ''))
        if label.startswith('Sound File'):
            if r['year'] in sound:
                raise SystemExit(f'two Sound File rows for {r["year"]}: {sound[r["year"]]["fileid"]}, {r["fileid"]}')
            sound[r['year']] = r
        elif label.startswith('Aural Paper') and label.endswith('(EV)'):
            aural.setdefault(r['year'], []).append(r['fileid'])
    out = []
    for year in sorted(sound, reverse=True):
        r = sound[year]
        if not aural.get(year):
            raise SystemExit(f'{year}: a Sound File row and no Aural Paper row')
        url = f'{ARCHIVE}/{year}/{r["fileid"]}'
        out.append({
            'year': int(year),
            'paperFileids': sorted(aural[year]),
            'source': {
                'kind': 'source-audio',
                'label': 'Lithuanian listening',
                'title': f'{year} Lithuanian · Listening Comprehension Test',
                'playbackUrl': url,
                'secFileid': r['fileid'],
                'canonicalUrl': url,
                'attribution': '© State Examinations Commission.',
                'presentationNote': ('Full official recording · Higher and Ordinary Level. '
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
    print(f'{OUT}: {len(out)} years', [(o['year'], o['source']['secFileid'], o['paperFileids']) for o in out])


if __name__ == '__main__':
    main()
