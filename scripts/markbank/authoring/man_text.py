#!/usr/bin/env python3
"""Mandarin Chinese pages, read so that what comes out is what the SEC printed.

    python3 scripts/markbank/authoring/man_text.py \
        examiner-reports/mandarin-chinese/papers/2024-hl-000-paper.pdf 7
    python3 scripts/markbank/authoring/man_text.py --glyph-audit

Why this file exists
--------------------
Mandarin Chinese is the second subject in the bank set in a NON-LATIN script,
and Japanese (ja_text.py) is the precedent. Three things had to be established
about this corpus before a single ask was counted, because any one of them
would have made the subject unshippable:

**1. Do the characters survive the text layer, in printed order?**
Yes, on 28 of the 30 files. 2024 Higher page 7 and 2024 Ordinary page 8 do not,
and they are the only two: their fonts are embedded with a broken ToUnicode
map, so the text layer hands back "аҍҼޝᒤॱҼᴸˈ㤡ഭѮ㹼Ҷ" where the page prints
"一九二六年十二月，英国举行了" and "YƵĞƐƚŝŽŶ" where it prints "Question".
Both pages are repaired here (see REPAIR below) and the repair is gated.
The scan that found them is `--glyph-audit`, and it is the corpus-wide check
that no other page needs one.

**2. Is there pinyin set above or beside the characters, the way Japanese sets
furigana?**  No — and this is the trap that does NOT exist here. The whole
corpus of twenty papers and ten schemes carries THREE tone-marked Latin
characters per file, and every one of them is Irish: the ú of "Coimisiún", the
ú of "Scrúduithe", the á of "Stáit". Not one syllable of pinyin is printed
anywhere in a paper or a scheme. The SEC even prices its ABSENCE — the Writing
band grid deducts for "substitutes of characters using other languages or
means (e.g., pinyin, traditional characters …)". So none of ja_text's ruby
machinery is needed, and none of it is copied here: a small raised run on these
pages is an ordinal or a footnote, never a reading.

**3. Is any ask answered by a character the student must WRITE — stroke order,
character production — which a text card cannot mark?**  No. Not one ask in
the ten sittings asks for stroke order or for a character to be drawn. What
looks like it from a distance is the radical table ("Write down the radicals of
the following characters and the meaning of the radicals") and the handful of
"Answer in Chinese" asks, and the SEC answers every one of them with a STATED
character string — 家, 宀, 灬, 咖啡电车, 福 — which is a recallable answer like
any other. The one classification task, 2026 Ordinary Q3(e), is answered by a
tick in a named column, and the scheme names the column.

REPAIR
------
The two broken pages are keyed (year, level, page) like a misprint, never
detected by a heuristic, and the repair is per FONT because the same code point
means different things in two fonts on one page: U+0004 is "A" in the Calibri
subset and U+000F is "，" in the SimSun subset.

* **SimSun-GBK-EUC-H.** Every ideograph is displaced by a CONSTANT: the printed
  character is the extracted one plus 0x49D0. 一 comes back as U+0430, 九 as
  U+048D, 月 as U+1D38 — 0x49D0 below each, in all 154 sightings across the two
  pages. The handful of glyphs in that subset that are NOT ideographs (the
  fullwidth comma, full stop and colon, 〇, and the two quotation marks) fall
  outside the rule and are listed per file.
* **Calibri, Calibri-Italic, Calibri-Bold.** These share one subset encoding
  and it is not an offset — it is the font's own glyph order, which rises with
  the character but not evenly. The map is DERIVED, not guessed: the running
  head "Leaving Certificate Examination 2024 / Mandarin Chinese – Written –
  Higher Level" is printed on the broken page and on the nineteen clean pages
  of the same booklet, and aligning the two gives twenty characters with no
  conflict. The rest were settled the way this bank settles a glyph survivor —
  the page rendered at 150dpi and looked at.

`repair_page` refuses to hand back a page holding a character it cannot
account for, so a third broken page appearing in a future corpus stops the
build rather than shipping a card of mojibake.
"""
import argparse
import collections
import glob
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

SUBJECT = 'mandarin-chinese'

# Two printed columns are never a word-space apart; twelve points is the widest
# run of white space this type sets inside a sentence. ja_text measured the
# same number on the same SEC page furniture.
GAP = 12.0
BASELINE_TOL = 4.0

# The private-use code points these thirty files leave in their text layer,
# every one a Wingdings or Symbol dingbat the SEC set as ordinary page
# furniture. Settled by cropping and looking, not by reading a font table.
#
#   U+F0FC  Wingdings  the TICK. It is the single most load-bearing glyph in
#                      the subject: every true/false table in every sitting is
#                      answered by it, and the paper's own rubric — "by ticking
#                      (✓) the boxes" — prints it too. Left alone the rubric
#                      reads "by ticking () the boxes" and every true/false
#                      answer is an unresolvable glyph the build refuses.
#   U+F0B7  Symbol     a filled round bullet
#   U+F0D8  Wingdings  a solid right-pointing triangle, used as a bullet
#   U+F050  Wingdings  a pencil, set beside a writing task
#   U+F020  Symbol     that font's space
DINGBATS = {'': '✓', '': '•', '': '▶', '': '✎',
            '': ' ', '': ' '}

NBSP = '         ⁠﻿'

# ---------------------------------------------------------------- REPAIR ----
# The Calibri subset encoding, shared by the roman, italic and bold faces of
# both broken pages. Twenty of these came from aligning the broken running head
# against the clean one printed on the same booklet's other nineteen pages; the
# rest were read off the page rendered at 150dpi.
CALIBRI = {
    0x0003: ' ', 0x0004: 'A', 0x0011: 'B', 0x0012: 'C', 0x0018: 'D',
    0x001C: 'E', 0x0026: 'F', 0x002C: 'H', 0x003A: 'J', 0x003E: 'L',
    0x0044: 'M', 0x004B: 'O', 0x0059: 'Q', 0x005A: 'R', 0x005E: 'S',
    0x0073: 'V', 0x0074: 'W',
    0x0102: 'a', 0x010F: 'b', 0x0110: 'c', 0x011A: 'd', 0x011E: 'e',
    0x0128: 'f', 0x0150: 'g', 0x015A: 'h', 0x015D: 'i', 0x016C: 'k',
    0x016F: 'l', 0x0175: 'm', 0x0176: 'n', 0x017D: 'o', 0x0189: 'p',
    0x018B: 'q', 0x018C: 'r', 0x0190: 's', 0x019A: 't', 0x01B5: 'u',
    0x01C0: 'v', 0x01C1: 'w', 0x01C6: 'x', 0x01C7: 'y',
    0x0355: ',', 0x0357: ':', 0x0358: '.', 0x0372: '-', 0x0374: '–',
    # Symbols do not sit with the letters in this font's glyph order:
    # "=" comes back as U+0441 and "?" as U+0359, well past "y".
    0x0441: '=', 0x0359: '?', 0x035C: '‘', 0x035D: '’',
    # The flyer on 2024 Ordinary page 8 opens its rubric line with a
    # decorative pair of EYES, set in Calibri and cropped at 500dpi to
    # settle it. It is the SEC's own ornament and it stays on the
    # stimulus rather than being silently dropped.
    0x10F0: '\U0001F440',
}
# The digits are a run: U+03EC is "0" and each of the ten follows it. Five of
# the ten are printed on the two pages ("2024", "3", "7", "8"); the run is
# stated rather than listed so a sixth cannot be silently wrong.
CALIBRI.update({0x03EC + d: str(d) for d in range(10)})

# The SimSun-GBK-EUC-H subsets. The ideographs are handled by the offset; these
# are the glyphs in those subsets that are not ideographs, and they differ
# between the two files because the two files carry two different subsets.
SIMSUN_PUNCT = {
    (2024, 'hl'): {0x00FE: '“', 0x00FF: '”', 0x01C4: '。', 0x02C8: '，',
                   0x5658: '〇'},
    (2024, 'ol'): {0x000F: '，', 0x02D6: '：'},
}
CJK_OFFSET = 0x49D0

# The pages that need it, keyed like a misprint. Nothing detects a broken page
# at run time: a page not named here is read as printed, and `--glyph-audit`
# is what says whether that list is still complete.
BROKEN_PAGES = {
    (2024, 'hl', '000'): {7},
    (2024, 'ol', '000'): {8},
}


def _repair_char(ch, font, sitting):
    code = ord(ch)
    if font.startswith('Calibri'):
        return CALIBRI.get(code)
    if 'SimSun' in font or 'YaHei' in font:
        table = SIMSUN_PUNCT.get(sitting, {})
        if code in table:
            return table[code]
        if code == 0x0003:
            return ' '
        out = code + CJK_OFFSET
        if 0x4E00 <= out <= 0x9FFF:
            return chr(out)
        return None
    return None


def repair_span(text, font, sitting):
    """One printed span of a broken page, put back.

    Raises rather than guessing: a code point neither table accounts for is a
    subset this map has never seen, and a card built on a guess about it would
    pass every downstream gate.
    """
    out = []
    for ch in text:
        if ch in ' \n\t' or ch in NBSP:
            out.append(' ')
            continue
        got = _repair_char(ch, font, sitting)
        if got is None:
            raise ValueError(
                f'{sitting} {font}: no repair for U+{ord(ch):04X} in {text!r}')
        out.append(got)
    return ''.join(out)


def _cjk(ch):
    return '　' <= ch <= '鿿' or '＀' <= ch <= '￯'


def _fold(text):
    out = ''.join(' ' if c in NBSP else DINGBATS.get(c, c) for c in text)
    return out


# ------------------------------------------------------------- the page ----
def page_rows(page, sitting=None, page_no=None, component='000'):
    """[[(x0, x1, text)]] — every printed row of the page, in printed order,
    each cut into its gap groups.

    A row is a baseline band, not a pymupdf block: the SEC sets a true/false
    table's statement, its "True" header and its two answer boxes in four
    separate blocks on one printed line, and reading blocks in order puts the
    header thirty rows away from the table it heads.
    """
    broken = bool(sitting and page_no and page_no in BROKEN_PAGES.get(
        (sitting[0], sitting[1], component), ()))
    chars = []
    for block in page.get_text('rawdict')['blocks']:
        if block.get('type') != 0:
            continue
        for line in block['lines']:
            for span in line['spans']:
                text = ''.join(c['c'] for c in span['chars'])
                if broken:
                    text = repair_span(text, span['font'], sitting)
                text = _fold(text)
                for c, ch in zip(span['chars'], text):
                    if not ch.strip():
                        continue
                    x0, y0, x1, y1 = c['bbox']
                    chars.append({'c': ch, 'x0': x0, 'x1': x1,
                                  'y': (y0 + y1) / 2,
                                  'size': round(span['size'], 1)})
    if not chars:
        return []
    rows, anchor = [], None
    for c in sorted(chars, key=lambda c: (round(c['y'], 1), c['x0'])):
        if anchor is None or c['y'] - anchor > BASELINE_TOL:
            rows.append([])
            anchor = c['y']
        rows[-1].append(c)
    out = []
    for row in rows:
        row.sort(key=lambda c: c['x0'])
        groups, cur, x0, x1, prev = [], [], None, None, None
        for c in row:
            if prev is not None and c['x0'] - prev['x1'] > GAP:
                if ''.join(cur).strip():
                    groups.append((x0, x1, ''.join(cur).strip()))
                cur, x0 = [], None
            if x0 is None:
                x0 = c['x0']
            lead = ''
            if prev is not None:
                gap = c['x0'] - prev['x1']
                both = _cjk(prev['c']) and _cjk(c['c'])
                if gap > (0.28 if both else 0.20) * max(prev['size'],
                                                        c['size']):
                    lead = ' '
            cur.append(lead + c['c'])
            x1 = c['x1']
            prev = c
        if cur and ''.join(cur).strip():
            groups.append((x0, x1, ''.join(cur).strip()))
        if groups:
            out.append({'y': row[0]['y'], 'groups': groups})
    return out


def shaded_boxes(page):
    """The rectangles the SEC FILLS on a question page.

    Two things on these papers are printed inside a filled box and nothing else
    is: the section tab in the top margin ("Section A · Reading · 80 marks")
    and the ANSWER BOXES a candidate writes in. The answer boxes carry printed
    labels — "Dublin Standard Time:", "Animal 1:", a bare "1." and "2." — set
    in their own text blocks, which land in the page's block order well after
    the ask they belong to. Read as ordinary rows they become part of the next
    question's text, and a bare "1." inside one is indistinguishable from a
    numbered ask.

    So the page's own furniture settles it before any wording does, exactly as
    Italian's ruled answer lines settle which of its pages is a question page.
    """
    out = []
    for drawing in page.get_drawings():
        if drawing.get('type') not in ('f', 'fs'):
            continue
        r = drawing['rect']
        if r.width > 40 and r.height > 8:
            out.append((r.x0, r.y0, r.x1, r.y1))
    return out


def in_box(y, boxes, x0=None):
    for bx0, by0, bx1, by1 in boxes:
        if by0 - 1 <= y <= by1 + 1 and (x0 is None or bx0 - 2 <= x0 <= bx1 + 2):
            return True
    return False


# ------------------------------------------------------------- the audit ----
def glyph_audit():
    """Every page in the corpus whose text layer is not what the page prints.

    The test is a page that carries Latin letters the SEC does not set: the
    Calibri subset draws "Question" as "YƵĞƐƚŝŽŶ", so a page holding more than
    a handful of U+0100-U+03FF letters beside its Chinese is broken. Run over
    all thirty files it names exactly two pages, which is what BROKEN_PAGES
    holds.
    """
    bad = re.compile('[Ā-ɏͰ-Ͽ]')
    rows = []
    for path in sorted(glob.glob(os.path.join(
            ROOT, 'examiner-reports', SUBJECT, '*', '*.pdf'))):
        with pymupdf.open(path) as doc:
            hits = [p + 1 for p in range(doc.page_count)
                    if len(bad.findall(doc[p].get_text())) > 20]
        rows.append((os.path.relpath(path, ROOT), hits))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('path', nargs='?')
    ap.add_argument('pages', nargs='*', type=int)
    ap.add_argument('--glyph-audit', action='store_true')
    args = ap.parse_args()
    if args.glyph_audit:
        total = 0
        for name, hits in glyph_audit():
            if hits:
                total += len(hits)
                print(f'  BROKEN {name}: pages {hits}')
        print(f'{total} broken page(s) in the corpus')
        return 0
    m = re.search(r'(\d{4})-(hl|ol)(?:-([A0-9]{3}))?', args.path or '')
    sitting = (int(m.group(1)), m.group(2)) if m else None
    component = (m.group(3) or '000') if m else '000'
    with pymupdf.open(args.path) as doc:
        pages = args.pages or range(1, doc.page_count + 1)
        for p in pages:
            print('=' * 20, 'page', p)
            boxes = shaded_boxes(doc[p - 1])
            for row in page_rows(doc[p - 1], sitting, p, component):
                tag = 'BOX ' if in_box(row['y'], boxes) else '    '
                print('  ' + tag + ' | '.join(
                    f'{x0:.0f}:{t}' for x0, _x1, t in row['groups']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
