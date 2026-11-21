#!/usr/bin/env python3
"""The sixteen small languages' Topic Atlas rows, written into their wave files.

The Atlas listed only Part I (Q1-Q6) of these papers, and none at all for some
sittings. This writes, from the cards and their filings:

  - a row for every Part II and Part III question the cards address, numbered
    by the part ("II1", "III2"; "II" for a part printed as one unnumbered
    question), as scripts/atlas-model/cardAtlasAddress.ts addresses them;
  - the whole paper, Part I included, for a sitting with cards and no Atlas
    paper, when the Paper Trail index lists that paper.

A row's heading is the one its cards are filed under (the most common, then a
second if its cards differ). Existing rows are never renumbered or retagged:
the four older papers that already list a whole part as one row (Danish 2018
rows 7 and 8, Slovenian 2018, 2023 and 2024 row 7) keep it, and their cards go there.

Usage:  python3 scripts/markbank/authoring/sl_atlas_rows.py [--check]
Then:   node scripts/paper-trail/topic-tags/build-tags.mjs --subject <subject>
        node scripts/atlas-model/build-ask-topics.mjs <subject>...
--check writes nothing and fails if a wave file would change.
"""
import collections
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
SUBJECTS = ['bulgarian', 'croatian', 'czech', 'danish', 'dutch', 'estonian', 'finnish', 'hungarian', 'latvian',
            'maltese', 'modern-greek', 'romanian', 'slovakian', 'slovenian', 'swedish', 'ukrainian']
# Mirrors SMALL_LANGUAGE_WHOLE_PART in scripts/atlas-model/cardAtlasAddress.ts.
WHOLE_PART = {('danish', 2018, 'II'): '7', ('danish', 2018, 'III'): '8',
              ('slovenian', 2018, 'II'): '7', ('slovenian', 2023, 'II'): '7', ('slovenian', 2024, 'II'): '7'}
PART = {'II': 'II', 'III': 'III', '2': 'II', '3': 'III'}


def atlas_n(subject, year, ref):
    """The Atlas row a card's printed question is: cardAtlasAddress.ts's rule for these sixteen."""
    part = re.search(r'\bSection (II|III|2|3)\b', ref)
    q = re.search(r'\bQ\s*(\d+)', ref)
    if part:
        roman = PART[part.group(1)]
        return WHOLE_PART.get((subject, year, roman)) or f'{roman}{q.group(1) if q else ""}'
    if subject == 'maltese' and year == 2019:
        if re.search(r'\bQ1A\b', ref):
            return '2'
        if q and int(q.group(1)) >= 2:
            return str(int(q.group(1)) + 1)
    return q.group(1) if q else None


def deck_fileids(subject):
    """Card id -> paper file id, read off the built deck (the authored JSON does not carry it)."""
    text = open(os.path.join(ROOT, f'components/MarkBank/cards/{subject}/higher.ts'), encoding='utf-8').read()
    # Each card object prints its paperFileid a line above its id.
    out, pending = {}, None
    for m in re.finditer(r'\bpaperFileid: "([^"]+)"|\bid: "([^"]+)"', text):
        if m.group(1):
            pending = m.group(1)
        elif pending and not m.group(2).startswith('r-'):
            out[m.group(2)], pending = pending, None
    return out


def indexed(year, fileid):
    """True when the Paper Trail index lists this paper in this year (fileids are subject-specific)."""
    if not hasattr(indexed, 'lines'):
        indexed.lines = open(os.path.join(ROOT, 'paperTrailData.ts'), encoding='utf-8').read().split('\n')
    return any(f'"year": {year},' in line and f'"f": "{fileid}"' in line for line in indexed.lines)


def order_key(n):
    m = re.fullmatch(r'(II|III)?(\d*)', n)
    part = {'': 0, 'II': 1, 'III': 2}[m.group(1) or '']
    return (part, int(m.group(2)) if m.group(2) else 0)


def rows_for(subject):
    cards = json.load(open(os.path.join(ROOT, f'scripts/markbank/authored/{subject}.json'), encoding='utf-8'))
    filing = json.load(open(os.path.join(ROOT, f'scripts/atlas-model/filings/{subject}.json'), encoding='utf-8'))['asks']
    fileids = deck_fileids(subject)
    missing = [c['id'] for c in cards if c['id'] not in fileids]
    if missing:
        raise SystemExit(f'{subject}: no paper file id in the deck for {missing[:3]}')
    papers = collections.defaultdict(lambda: collections.defaultdict(list))
    for c in cards:
        n = atlas_n(subject, c['year'], c['questionRef'])
        if not n:
            raise SystemExit(f'{c["id"]}: no Atlas row for "{c["questionRef"]}"')
        papers[(c['year'], f'{fileids[c["id"]]}.pdf')][n].append(c['id'])
    return papers, filing


def heading(card_ids, filing):
    counts = collections.Counter(t for cid in card_ids for t in filing[cid][0])
    ranked = [t for t, _ in counts.most_common()]
    row = {'primary': ranked[0]}
    if len(ranked) > 1:
        row['secondary'] = ranked[1]
    return row


def main():
    check = '--check' in sys.argv
    changed, report = [], []
    for subject in SUBJECTS:
        path = os.path.join(ROOT, f'scripts/paper-trail/topic-tags/tags/{subject}.json')
        tags = json.load(open(path, encoding='utf-8')) if os.path.exists(path) else []
        before = json.dumps(tags, ensure_ascii=False)
        papers, filing = rows_for(subject)
        added_rows, added_papers, unindexed = 0, [], []
        for (year, fileid), rows in sorted(papers.items()):
            paper = next((p for p in tags if p['year'] == year and p['fileid'] == fileid and p['level'] == 'higher'), None)
            if paper is None:
                if not indexed(year, fileid):
                    unindexed.append(year)
                    continue
                paper = {'subjectId': subject, 'level': 'higher', 'lang': 'ev', 'year': year, 'fileid': fileid,
                         'paperKey': 'single', 'q': []}
                tags.append(paper)
                added_papers.append(year)
            have = {q['n'] for q in paper['q']}
            new = [n for n in rows if n not in have]
            if paper['q'] and any(order_key(n)[0] == 0 for n in new):
                raise SystemExit(f'{subject} {year}: cards address Part I rows the Atlas paper lacks: '
                                 f'{[n for n in new if order_key(n)[0] == 0]}')
            for n in sorted(new, key=order_key):
                paper['q'].append({'n': n, **heading(rows[n], filing)})
                added_rows += 1
        tags.sort(key=lambda p: p['year'])   # every one of the sixteen lists its papers oldest first
        after = json.dumps(tags, ensure_ascii=False)
        if after != before:
            changed.append(subject)
            if not check:
                with open(path, 'w', encoding='utf-8') as fh:
                    fh.write(json.dumps(tags, ensure_ascii=False, indent=1))   # the wave files' own layout
        report.append(f'{subject:13} rows added {added_rows:3}  papers added {added_papers}'
                      + (f'  NOT IN THE INDEX {unindexed}' if unindexed else ''))
    print('\n'.join(report))
    if check and changed:
        raise SystemExit(f'wave files out of date: {changed}')


if __name__ == '__main__':
    main()
