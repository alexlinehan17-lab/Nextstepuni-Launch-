#!/usr/bin/env python3
"""Re-extract the 2022 Higher Technology scheme, repairing it from glyph ids.

    python3 scripts/markbank/authoring/tech_glyphs.py            # report
    python3 scripts/markbank/authoring/tech_glyphs.py --write    # rewrite the .md

Nine of Technology's ten marking schemes reach the text layer as ordinary
text. The tenth -- 2022 Higher -- reaches it through subset fonts whose
ToUnicode CMap is wrong for EVERY character they draw, not just for the
ligatures glyphmap.json repairs:

    ">eaving Certificate Examination"     is "Leaving Certificate Examination"
    "E\\x04^\\x04 are constantly striving"  is "NASA are constantly striving"

Two things separate this from the mangling derive_glyphs.py already handles.
The wrong codepoints are ASCII (">" for "L", "d" for "T") and control
characters ("\\x03" for a space, "\\x04" for "A"), so a codepoint -> character
table like glyphmap-technology.json cannot express the repair: ">" is a real
">" in the other nine schemes, and the same PDF also draws unmangled Calibri
whose "d" is a "d". And the control characters never reach the markdown at all
-- the extractor drops them -- so the committed 2022-hl.md has no spaces
between its words at all, which is why every marking point in that sitting was
untraceable.

The glyph id is trustworthy where the ToUnicode is not, exactly as
derive_glyphs.py argues, and it is trustworthy per DRAWN CHARACTER rather than
per codepoint -- which is what resolves the two Calibris. A glyph id means one
character within one font, and the other nineteen PDFs in this subject's
corpus draw the same Calibri and Cambria glyph ids with a correct ToUnicode.
So the table is learned from them, (font, glyph id) -> character, and applied
here character by character, joined to the drawn glyph by its origin.

Nothing is hand-mapped. A glyph id the corpus never draws correctly is
reported and left exactly as the text layer gave it, so the build's glyph gate
still sees it.
"""
import argparse
import collections
import glob
import importlib.util
import json
import os
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TARGET = os.path.join(ROOT, 'examiner-reports/technology/schemes/2022-hl.pdf')
OUT_MD = os.path.join(ROOT, 'examiner-reports/technology/schemes/2022-hl.md')

# The row-and-span logic that produced every other .md in this repo. Loaded
# rather than reimplemented: an extraction that lays its lines out differently
# from its nine siblings would be a second format for the provenance gate and
# for every reader, and the difference would be invisible in review.
_spec = importlib.util.spec_from_file_location(
    'extract_scheme', os.path.join(ROOT, 'scripts/markbank/extract-scheme.py'))
EX = importlib.util.module_from_spec(_spec)
sys.modules['extract_scheme'] = EX
_spec.loader.exec_module(EX)

# What a repaired character may be. Printable ASCII plus the punctuation the
# SEC actually sets. A "repair" outside this is evidence the join went wrong,
# not a character the scheme prints.
SANE = set(chr(c) for c in range(0x20, 0x7F)) | set('–—‘’“”°±×÷Ωµ…•')

# Glyphs this file draws that no other PDF in the corpus draws at all, so the
# glyph-id table cannot reach them. Each was settled the way derive_glyphs.py
# settles its survivors: crop the glyph out of the page at 400 dpi and look at
# it. The page and the sentence are recorded so the call can be re-checked.
LOOKED_AT = {
    ('Calibri,Bold', 1094): '±',   # p5  "expressed as a +/-%"
    ('Calibri,Bold', 1105): 'Ω',   # p5  "a 100 ohm resistor"
    ('Calibri,Bold', 862): '“',    # p16 "thermistor "B" increases"
    ('Calibri,Bold', 863): '”',    # p16 the same pair, closing
    ('Calibri,Bold', 934): '€',    # p20 the "Cost (euro)" column head
}


def family(font):
    """"Calibri,BoldItalic" and "Calibri-Bold" are one font's four faces.

    A subset keeps the ORIGINAL font's glyph order and the four faces of
    Calibri share it -- gid 4 is "A" in all of them. Cambria's order differs
    (gid 18 is "O", not "C"), so the fallback stays inside a family.
    """
    return font.split(',')[0].split('-')[0]


def sightings(files):
    """(font, glyph id) -> Counter(character it extracted as)."""
    seen = collections.defaultdict(collections.Counter)
    for path in files:
        doc = pymupdf.open(path)
        for pno in range(len(doc)):
            for (font, gid), ch in _glyphs(doc[pno]).values():
                seen[(font, gid)][ch] += 1
        doc.close()
    return seen


def _glyphs(page):
    """{origin -> ((font, glyph id), character)} for every glyph drawn."""
    origin = {}
    for sp in page.get_texttrace():
        font = sp.get('font')
        for ch in sp['chars']:
            origin[(round(ch[2][0], 2), round(ch[2][1], 2))] = (font, ch[1])
    out = {}
    for blk in page.get_text('rawdict')['blocks']:
        for line in blk.get('lines', []):
            for sp in line.get('spans', []):
                for ch in sp['chars']:
                    key = (round(ch['origin'][0], 2), round(ch['origin'][1], 2))
                    if key in origin:
                        out[key] = (origin[key], ch['c'])
    return out


def truth_table():
    """(font, glyph id) -> the character the rest of the corpus draws it as."""
    corpus = [f for f in sorted(
        glob.glob(os.path.join(ROOT, 'examiner-reports/technology/schemes/*.pdf'))
        + glob.glob(os.path.join(ROOT, 'examiner-reports/technology/papers/*.pdf')))
        if os.path.abspath(f) != os.path.abspath(TARGET)]
    truth = {}
    for key, counts in sightings(corpus).items():
        total = sum(counts.values())
        best, n = counts.most_common(1)[0]
        # Agreement, not volume -- derive_glyphs.py's rule, for its reason: a
        # glyph id is one character, so one clean sighting settles it, while
        # an id that disagrees with itself settles nothing.
        if n * 10 >= total * 9 and len(best) == 1 and best in SANE:
            truth[key] = best
    by_family = collections.defaultdict(dict)
    for (font, gid), ch in truth.items():
        by_family[family(font)].setdefault(gid, ch)
    return truth, by_family


def mangled_fonts(doc):
    """Which of the target's fonts have a broken ToUnicode, counted not assumed.

    The file mixes them. Its body is set in a Calibri subset whose every
    character comes out wrong, while the "Section A - Core / 72 marks" heading
    is a Cambria subset that extracts perfectly -- and the two subsets do NOT
    share a glyph order, so repairing the sound one from the corpus turned
    "72 marks" into "32 marks". A font is repaired only where its own text
    layer is demonstrably not text.
    """
    tally = collections.defaultdict(collections.Counter)
    for pno in range(len(doc)):
        for (font, _gid), ch in _glyphs(doc[pno]).values():
            tally[font]['bad' if not _sane_text(ch) else 'ok'] += 1
    return {font for font, c in tally.items()
            if c['bad'] > (c['ok'] + c['bad']) / 2}


def _sane_text(ch):
    """Whether this character is plausibly what the page prints."""
    u = ord(ch)
    return (0x20 <= u < 0x7F) or ch in SANE or 0xC0 <= u <= 0xFF


def rebuild(truth, by_family, unknown):
    """The repaired scheme text, laid out exactly as extract-scheme.py lays it."""
    doc = pymupdf.open(TARGET)
    broken = mangled_fonts(doc)
    out = []
    for pno, page in enumerate(doc, 1):
        out.append(f'\n## Page {pno}\n')
        fixed = {}
        for key, ((font, gid), ch) in _glyphs(page).items():
            # A sound font is left alone except for the control characters it
            # emits where a space belongs: every one of these fonts draws the
            # space at glyph id 3, and the extractor drops "\\x03" entirely, so
            # a sound font's words were running together too.
            if font not in broken and ord(ch) >= 0x20:
                fixed[key] = ch
                continue
            real = (truth.get((font, gid)) or by_family[family(font)].get(gid)
                    or LOOKED_AT.get((font, gid)))
            if real is None:
                unknown[(font, gid, ch)] += 1
                real = ch
            fixed[key] = real
        lines = []
        for blk in page.get_text('rawdict')['blocks']:
            if blk.get('type') != 0:
                continue
            for line in blk.get('lines', []):
                spans = []
                for sp in line.get('spans', []):
                    text = ''.join(
                        fixed.get((round(c['origin'][0], 2),
                                   round(c['origin'][1], 2)), c['c'])
                        for c in sp['chars'])
                    if text:
                        spans.append({'text': text, 'bbox': sp['bbox'],
                                      'size': sp['size']})
                text = EX.join_spans(spans)
                if not text.strip():
                    continue
                x0, y0, x1, y1 = line['bbox']
                lines.append({'text': text, 'x': x0, 'x1': x1,
                              'y': (y0 + y1) / 2, 'h': y1 - y0})
        lines.sort(key=lambda l: (round(l['y'], 1), l['x']))
        row, row_y, row_h = [], None, 10.0
        for line in lines:
            if row_y is not None and abs(line['y'] - row_y) > max(3.0, row_h * 0.6):
                out.append(EX.render_row(row, None))
                row = []
            if not row:
                row_y, row_h = line['y'], line['h']
            row.append(line)
        if row:
            out.append(EX.render_row(row, None))
    doc.close()
    return '\n'.join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()

    truth, by_family = truth_table()
    unknown = collections.Counter()
    text = rebuild(truth, by_family, unknown)
    residue = sum(1 for c in text if ord(c) > 0xFF or (ord(c) < 0x20 and c != '\n'))
    print(f'{len(truth)} (font, glyph id) pairs learned from the corpus')
    print(f'{len(text):,} chars rebuilt; {residue} unrepaired character(s) left')
    print(f'{sum(unknown.values())} sighting(s) of a glyph id the corpus never '
          f'draws correctly')
    for key, n in unknown.most_common(20):
        print(f'   UNKNOWN {key!r} x{n}')
    if args.write:
        with open(OUT_MD, 'w', encoding='utf-8') as fh:
            fh.write(text)
        print(f'wrote {OUT_MD}')
    else:
        print()
        print(text[2500:4200])
    return 0


if __name__ == '__main__':
    sys.exit(main())
