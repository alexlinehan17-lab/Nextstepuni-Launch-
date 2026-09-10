#!/usr/bin/env python3
"""Japanese pages, read so that what comes out is what the SEC printed.

    python3 scripts/markbank/authoring/ja_text.py examiner-reports/japanese/papers/2024-hl-000-paper.pdf 6

Why this file exists
--------------------
Japanese is the first subject in the bank set in a NON-LATIN script, and the
first whose pages carry a second layer of type over the first. Both facts are
handled here, once, for the paper reader and the scheme reader alike.

**Furigana.** The SEC prints a kana reading in small type ABOVE the kanji it
glosses, and the PDF text layer holds it as an ordinary run of characters
sitting on its own baseline. Extracted naively it interleaves with the line
below it and the result is not Japanese: `pymupdf`'s own `get_text()` renders
2024 Higher page 6 as "問題\\nもんだい\\n2" and "ポッキーの歴史\\nれきし".
A card printing that is worse than no card.

So a small run is folded back INTO the line it glosses, in brackets, at the
character it was centred over: 東京（きょう）観光（かんこう）, 女性（せい）.
The bracket convention is disclosed on every card that carries Japanese.

Three things this had to learn, each of which mangled a page first:

* **A ruby run is one SPAN, not one x-neighbourhood.** きょう over 京 and
  かんこう over 観光 are printed a tenth of a point apart and read as one run
  by any adjacency rule, giving 東京観光（きょうかんこう）— a reading the SEC
  never printed. PyMuPDF already separates them; the span boundary is the
  signal, and the only splitting done inside a span is on a real gap.
* **Small and raised is not always ruby.** The SEC sets its ordinal
  superscripts the same way — 1st, 5ú, 7ú, 10ú in the table of 2024 Higher
  page 3 — and reading those as ruby orphaned them off their own line and left
  the table reading "1/1". A small run is furigana only if it is all KANA.
  This is `foldDigits` in another disguise: the same size test, the same cost.
* **The PDF emits no spaces between spans.** Latin text that reaches the eye
  as "1. Scríobh" reaches the text layer as two spans with a gap and no space
  character, and joining characters gives "1.Scríobh". A gap wider than a
  fraction of the type size is a space — except between two CJK characters,
  which are simply set on a wider body.

**Columns.** The Ordinary paper is printed bilingually in two columns, Irish
left and English right; the Higher paper sets the two languages on one line
separated by a slash. So a row is cut into GAP GROUPS (the same idea as
`fr_paper._gap_groups`) and the page's own column bound, read off the markers
printed down it, says which side a group is on.
"""
import argparse
import collections
import os
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

# Two printed columns are never a word-space apart. fr_paper measured the
# narrowest column gap on these bilingual booklets at eighteen points; twelve
# is the widest run of white space this type sets inside a sentence.
GAP = 12.0
BASELINE_TOL = 2.0


# The four PRIVATE-USE code points these twenty papers and ten schemes leave in
# their text layer, every one of them a Wingdings or Symbol dingbat the SEC set
# as ordinary page furniture. Settled the way the bank settles a glyph survivor
# — cropped at 400dpi and looked at — not by reading a font table:
#
#   U+F0E0  Wingdings  a rightwards arrow, printed between a true/false
#                      statement and the Japanese phrase that supports it,
#                      "→ [ ラインは日本で大人気のアプリです。]"
#   U+F0B7  Symbol     a filled round bullet
#   U+F046  Wingdings  a pointing hand, used as a bullet on the cover
#   U+F076  Wingdings  a four-diamond bullet
#
# Left alone they reach the card as unreadable glyphs and the build refuses it,
# which is right: a card that shows U+F0E0 is not a smaller version of the
# right card. Folded, five 2025 Ordinary true/false cards ship as printed.
DINGBATS = {'\uf0e0': '→', '\uf0b7': '•', '\uf046': '☞', '\uf076': '❖'}


def _cjk(ch):
    return '　' <= ch <= '鿿' or '＀' <= ch <= '￯'


def _kana(ch):
    return '぀' <= ch <= 'ヿ' or ch in '々ー'


def page_rows(page):
    """[[(x0, x1, text)]] — every printed row, cut into its gap groups.

    Furigana is folded into the group it glosses; superscripts rejoin the line
    they were set against; the reading order is the printed order.
    """
    raw = page.get_text('rawdict')
    spans, sizes = [], collections.Counter()
    for b in raw['blocks']:
        if b['type'] != 0:
            continue
        for l in b['lines']:
            for s in l['spans']:
                chars = [dict(c, c=DINGBATS.get(c['c'], c['c']))
                         for c in s['chars']]
                if not any(c['c'].strip() for c in chars):
                    continue
                size = round(s['size'], 1)
                spans.append((size, chars))
                sizes[size] += sum(1 for c in chars if c['c'].strip())
    if not spans:
        return []
    body = sizes.most_common(1)[0][0]
    thr = body * 0.8
    base, ruby, small = [], [], []
    for size, chars in spans:
        if size >= thr:
            base.append((size, chars))
        elif all(_kana(c['c']) for c in chars if c['c'].strip()):
            ruby.append((size, chars))
        else:
            small.append((size, chars))

    lines = collections.defaultdict(list)
    for size, chars in base:
        for c in chars:
            lines[round((c['bbox'][1] + c['bbox'][3]) / 2)].append(
                {'c': c['c'], 'x0': c['bbox'][0], 'x1': c['bbox'][2],
                 'y0': c['bbox'][1], 'y1': c['bbox'][3], 'size': size})
    merged = []
    for k in sorted(lines):
        if merged and k - merged[-1][0] <= BASELINE_TOL:
            merged[-1][1].extend(lines[k])
        else:
            merged.append([k, list(lines[k])])
    rows = [{'y': k, 'chars': sorted(cs, key=lambda c: c['x0'])}
            for k, cs in merged]

    for size, chars in small:
        for c in chars:
            if not c['c'].strip():
                continue
            d = {'c': c['c'], 'x0': c['bbox'][0], 'x1': c['bbox'][2],
                 'y0': c['bbox'][1], 'y1': c['bbox'][3], 'size': size}
            mid = (d['y0'] + d['y1']) / 2
            near = min(rows, key=lambda r: abs(r['y'] - mid), default=None)
            if near is None or abs(near['y'] - mid) > 8:
                rows.append({'y': round(mid), 'chars': [d]})
                rows.sort(key=lambda r: r['y'])
            else:
                near['chars'].append(d)
                near['chars'].sort(key=lambda c2: c2['x0'])

    runs = []
    for size, chars in ruby:
        cur = []
        for c in chars:
            if not c['c'].strip():
                continue
            if cur and c['bbox'][0] - cur[-1]['bbox'][2] > size * 0.6:
                runs.append(cur)
                cur = []
            cur.append(c)
        if cur:
            runs.append(cur)

    ins = collections.defaultdict(list)
    for run in runs:
        x0 = min(c['bbox'][0] for c in run)
        x1 = max(c['bbox'][2] for c in run)
        ybot = max(c['bbox'][3] for c in run)
        text = ''.join(c['c'] for c in run)
        best = None
        for i, r in enumerate(rows):
            top = min(c['y0'] for c in r['chars'])
            gap = top - ybot
            if gap < -2.0 or gap > 14:
                continue
            if not any(c['x0'] < x1 and c['x1'] > x0 for c in r['chars']):
                continue
            if best is None or gap < best[0]:
                best = (gap, i)
        if best is None:
            continue
        pos = 0
        for j, c in enumerate(rows[best[1]]['chars']):
            if c['x0'] < x1 - 0.5:
                pos = j + 1
        ins[best[1]].append((pos, text))

    out = []
    for i, r in enumerate(rows):
        pieces, prev = [], None
        for c in r['chars']:
            lead = ''
            if prev is not None and prev['c'].strip() and c['c'].strip():
                gap = c['x0'] - prev['x1']
                both = _cjk(prev['c']) and _cjk(c['c'])
                if gap > (0.28 if both else 0.20) * max(prev['size'], c['size']):
                    lead = ' '
            pieces.append(lead + c['c'])
            prev = c
        for pos, t in ins.get(i, []):
            j = min(max(pos - 1, 0), len(pieces) - 1)
            pieces[j] = pieces[j] + f'（{t}）'
        groups, cur, x0, x1 = [], [], None, None
        prev = None
        for c, piece in zip(r['chars'], pieces):
            if prev is not None and c['x0'] - prev['x1'] > GAP:
                if ''.join(cur).strip():
                    groups.append((x0, x1, ''.join(cur).strip()))
                cur, x0 = [], None
            if x0 is None:
                x0 = c['x0']
            x1 = c['x1']
            cur.append(piece)
            prev = c
        if cur and ''.join(cur).strip():
            groups.append((x0, x1, ''.join(cur).strip()))
        if groups:
            out.append(groups)
    return out


def doc_rows(path, page_from=0, page_to=None):
    """[(page number, [gap groups])] for a whole booklet."""
    out = []
    with pymupdf.open(path) as doc:
        last = doc.page_count if page_to is None else page_to
        for pno in range(page_from, last):
            for groups in page_rows(doc[pno]):
                out.append((pno, groups))
    return out


def page_count(path):
    with pymupdf.open(path) as doc:
        return doc.page_count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('path')
    ap.add_argument('pages', nargs='*', type=int)
    args = ap.parse_args()
    with pymupdf.open(args.path) as doc:
        pages = args.pages or range(1, doc.page_count + 1)
        for p in pages:
            print('=' * 20, 'page', p)
            for groups in page_rows(doc[p - 1]):
                print('  ' + ' | '.join(f'{x0:.0f}:{t}' for x0, _x1, t in groups))


if __name__ == '__main__':
    main()
