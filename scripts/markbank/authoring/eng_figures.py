#!/usr/bin/env python3
"""Cut the picture an Engineering ask points at, part by part.

    python3 scripts/markbank/authoring/eng_figures.py            # cut and report
    python3 scripts/markbank/authoring/eng_figures.py --write    # publish

question_art.py cuts figures for every subject and finds almost nothing here.
Its geometry was written for Computer Science, where a figure is a code
listing or an answer grid ruled across the page and the question sits above
it. Engineering prints a PHOTOGRAPH OR A LINE DRAWING BESIDE THE PROSE, in the
right half of the page, and asks about it in a sentence that names nothing:
"Identify the hybrid vehicle configuration shown opposite."

So this reads the page the way this subject sets it. A part owns the vertical
band between its own marker and the next one; the artwork inside that band is
what the ask points at; and the crop is the union of that artwork with the
labels printed on it.

WHAT IT REFUSES TO CUT, because each has shipped a wrong card before:

  * an answer box -- a ruled rectangle with nothing in it. It draws one stroke
    per line and counts as artwork on every test that measures ink;
  * a crop that reaches outside its own part's band, which is how a question
    about an electrode holder got a picture of an oxy-acetylene torch;
  * a page's furniture: the SEC logo, the barcode strip and the rules that box
    the header.

Every crop it makes is still opened and looked at before it is bound. The tool
finds candidates; it does not decide.
"""
import argparse
import collections
import json
import os
import re
import sys

import pymupdf

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
PAPERS = os.path.join(ROOT, 'examiner-reports', 'engineering', 'papers')
OUT = os.path.join(ROOT, 'components', 'MarkBank', 'figures')

MARKER = re.compile(r'^\(([a-hj-z])\)')
ROMAN = re.compile(r'^\((i{1,3}|iv|v|vi{1,3}|ix|x)\)')
# Engineering always names its questions -- "Question 4. (50 marks)" -- and
# a bare number is not one. Allowing it read the axis labels of a graph as
# nine question heads on one page ("10", "20", "30" ... "90"), which cut
# every band on that page to nothing.
QHEAD = re.compile(r'^\s*Question\s+(\d{1,2})\.?\s*(?:\(\s*\d{1,3}\s*marks?\s*\))?\s*$', re.I)
# The page's own furniture, printed on every page and never part of an ask.
HEADER = 120.0
FOOTER = 60.0


def lines(page):
    out = []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            text = ' '.join(''.join(s['text'] for s in line['spans']).split())
            if text:
                out.append((line['bbox'], text))
    out.sort(key=lambda r: (round(r[0][1], 1), r[0][0]))
    return out


def artwork(page):
    """Every picture on the page: raster images and drawn shapes alike.

    Engineering draws as often as it photographs -- a furnace in section, a
    welded joint, a mechanism -- and a drawing has no image rect at all.
    """
    out = []
    for im in page.get_images(full=True):
        for r in page.get_image_rects(im[0]):
            out.append((r.x0, r.y0, r.x1, r.y1))
    for d in page.get_drawings():
        r = d['rect']
        if r.width > 18 and r.height > 18:
            out.append((r.x0, r.y0, r.x1, r.y1))
    return [a for a in out
            if a[1] > HEADER and a[3] < page.rect.height - FOOTER
            and a[2] - a[0] > 24 and a[3] - a[1] > 24]


def is_answer_box(page, rect):
    """A ruled box the candidate writes in, which is not a picture.

    It is drawn as a few long horizontal strokes of nearly equal length, and
    it holds no words of its own. Bound as a figure it shows the student an
    empty box where the diagram should be -- six of them shipped that way in
    Agricultural Science before the rule existed.
    """
    x0, y0, x1, y1 = rect
    inside = [t for (bx0, by0, bx1, by1), t in lines(page)
              if x0 - 2 < bx0 and bx1 < x1 + 2 and y0 - 2 < by0 and by1 < y1 + 2
              and len(t) > 2]
    if inside:
        return False
    rules = [d['rect'] for d in page.get_drawings()
             if d['rect'].width > (x1 - x0) * 0.6 and d['rect'].height < 3
             and x0 - 4 < d['rect'].x0 and d['rect'].x1 < x1 + 4
             and y0 - 4 < d['rect'].y0 and d['rect'].y1 < y1 + 4]
    return len(rules) >= 3


def question_spans(page):
    """{question number: (top, bottom)} for the questions set on this page."""
    heads = [(b[1], int(QHEAD.match(t).group(1)))
             for b, t in lines(page) if QHEAD.match(t)]
    out = {}
    for i, (y, q) in enumerate(heads):
        bottom = heads[i + 1][0] if i + 1 < len(heads) else page.rect.height
        out[q] = (y, bottom)
    return out


def part_spans(page, top, bottom):
    """[(y, letter, roman)] for every part marker between top and bottom.

    A roman printed on a line of its own belongs to the LETTER above it. Read
    without that, "(i)" was recorded under no letter at all and (a)(i) matched
    nothing, so every roman fell back to its letter's band and the pictures
    printed against the romans themselves were never reached.
    """
    out = []
    letter = None
    for (bx0, by0, bx1, by1), t in lines(page):
        if not (top - 2 <= by0 <= bottom + 2):
            continue
        m, r = MARKER.match(t), ROMAN.match(t)
        if m:
            letter = m.group(1)
            rest = t[m.end():].strip()
            r2 = ROMAN.match(rest)
            out.append((by0, letter, r2.group(1) if r2 else None))
        elif r:
            out.append((by0, letter, r.group(1)))
    return out


def band_for(page, q, letter, roman, carried=None):
    """The vertical band this part owns, or None if it is not on this page.

    A question runs over pages and prints its head only once, so a part on the
    second page sits under no head at all. `carried` is the question the page
    opened under -- the last head seen before it -- and without it every part
    past a page break had no band and no figure: 2021 HL Q4(a)(i) asks about
    the surface hardening process SHOWN and the picture was never reached.
    """
    spans = question_spans(page)
    if q in spans:
        top, bottom = spans[q]
    elif carried == q and not spans:
        top, bottom = 0.0, page.rect.height
    elif carried == q:
        # The page opens under the carried question and hands over at the
        # first head printed on it.
        top, bottom = 0.0, min(y for y, _ in
                               [(v[0], k) for k, v in spans.items()])
    else:
        return None
    parts = part_spans(page, top, bottom)
    if not parts:
        return None
    want = (letter, roman)
    here = None
    for i, (y, le, rm) in enumerate(parts):
        if (le, rm) == want or (letter and roman is None and (le, rm) == (letter, None)):
            here = i
            break
    if here is None:
        return None
    # A part owns the page from its own marker to the next marker that is not
    # BENEATH it: (d) owns everything down to (e), including its own romans,
    # because the picture is printed once for the group.
    end = bottom
    for y, le, rm in parts[here + 1:]:
        if roman is None and rm and le == letter:
            continue                      # a roman of this same letter
        if (le, rm) == (letter, roman):
            continue
        end = y
        break
    return (parts[here][0], end)


def crop_for(path, q, letter, roman):
    """(page number, rect) for the picture this part points at, or None.

    A roman inherits its letter's picture. 2021 HL Q2(d) prints one diagram of
    a hybrid vehicle and asks (i) to identify it and (ii) to describe its
    operation from the labels on it; the picture sits beside (d)'s own line
    and inside neither roman's band. It is the same shared stimulus the deck
    already allows a question figure to be.
    """
    got = _crop(path, q, letter, roman)
    if got is None and roman is not None:
        got = _crop(path, q, letter, None)
    return got


def _crop(path, q, letter, roman):
    with pymupdf.open(path) as doc:
        carried = None
        for n in range(doc.page_count):
            page = doc[n]
            heads = question_spans(page)
            band = band_for(page, q, letter, roman, carried)
            if heads:
                carried = max(heads)
            if band is None:
                continue
            top, bottom = band
            art = [a for a in artwork(page)
                   if a[1] >= top - 6 and a[3] <= bottom + 6
                   and not is_answer_box(page, a)]
            if not art:
                return None
            x0 = min(a[0] for a in art)
            y0 = min(a[1] for a in art)
            x1 = max(a[2] for a in art)
            y1 = max(a[3] for a in art)
            if (x1 - x0) < 40 or (y1 - y0) < 30:
                return None
            # Rendering shows whatever OVERLAPS the box, so every line the
            # box touches is either taken WHOLE or the crop is refused. There
            # is no third option: nudging the box off an intruder cost one
            # figure its own caption, and leaving it in published "ns." and
            # "design" beside a toggle clamp and "d tap." above a tap wrench.
            #
            # A caption or a label is taken -- "A simplified portion of the
            # iron-carbon equilibrium diagram", "defect A", "welding earth
            # clamp". An ASK is not: it is the question talking, it belongs on
            # the card as text, and a crop carrying it shows the student the
            # question twice. What tells them apart is the command word.
            for _ in range(6):
                grew = False
                for (bx0, by0, bx1, by1), t in lines(page):
                    if bx1 <= x0 or bx0 >= x1 or by1 <= y0 or by0 >= y1:
                        continue
                    if x0 - 1 <= bx0 and bx1 <= x1 + 1 \
                            and y0 - 1 <= by0 and by1 <= y1 + 1:
                        continue
                    if ASK_LINE.match(t.strip()) or len(t.strip()) > 74:
                        return None
                    x0, y0 = min(x0, bx0), min(y0, by0)
                    x1, y1 = max(x1, bx1), max(y1, by1)
                    grew = True
                if not grew:
                    break
            else:
                return None
            if y1 - y0 > page.rect.height * 0.62:
                return None
            return n, (x0 - 4, y0 - 4, x1 + 4, y1 + 4)
    return None


# "shown at A, B and C", "labelled A, B, C and D", "the regions A, B, C and D
# shown". When the ask names its letters, the crop has to CARRY them: a
# picture of one crystal structure under "Identify the crystal structures A, B
# and C shown" is not a partial answer, it is the wrong picture.
NAMED = re.compile(
    r'\b(?:at|labell?ed|shown at|marked)\s+([A-Z](?:\s*,\s*[A-Z])*(?:\s+and\s+[A-Z])?)\b'
    r'|\b(?:structures?|regions?|parts?|processes|flames?|mechanisms?|lines?|'
    r'defects?|components?|chips?|tools?|fits?)\s+'
    r'([A-Z](?:\s*,\s*[A-Z])*(?:\s+and\s+[A-Z])?)\b')


# An instruction, as opposed to a caption. The command words are the ones
# derived from the 550 census leaves too long to be anything but an ask.
ASK_LINE = re.compile(
    r'^\(?[a-z0-9]{0,3}\)?\s*(?:briefly\s+)?(?:calculate|compare|define'
    r'|describe|determine|differentiate|discuss|distinguish|draw|explain|give'
    r'|identify|indicate|label|list|name|outline|sketch|state|suggest|answer'
    r'|select|why|what|complete)\b', re.I)


def letters_named(text):
    """The single letters an ask says are printed on its picture."""
    out = []
    for m in NAMED.finditer(text or ''):
        for g in m.groups():
            if not g:
                continue
            out += [x for x in re.findall(r'\b([A-Z])\b', g)]
    return sorted(set(out))


def crop_text(path, page, rect):
    with pymupdf.open(path) as doc:
        return doc[page].get_textbox(pymupdf.Rect(*rect))


def faults(path, page, rect, ask):
    """Why this crop must not be published, if it must not."""
    text = crop_text(path, page, rect)
    bad = []
    want = letters_named(ask)
    if want:
        have = set(re.findall(r'(?<![A-Za-z])([A-Z])(?![A-Za-z])', text))
        missing = [w for w in want if w not in have]
        if missing:
            bad.append(f'does not carry {", ".join(missing)}')
    # Prose inside the crop is the QUESTION bleeding in. A figure's own
    # caption is not -- "A simplified portion of the iron-carbon equilibrium
    # diagram" is printed under the diagram and belongs with it. What tells
    # them apart is that an ask is an instruction: it opens with a command
    # word, and a caption never does.
    for line in text.split('\n'):
        t = ' '.join(line.split())
        if len(t) > 40 and len(t.split()) > 6 and ASK_LINE.match(t):
            bad.append(f'carries the ask: {t[:44]!r}')
            break
    return bad


# What the gates pass and a person then rejected. Every crop this tool makes
# is opened and looked at before it is bound; these are the ones that survived
# every mechanical test and are still the wrong picture. Recorded by name so a
# later run cannot quietly publish them.
REJECTED = {
    # Ordinary Level Q1 sets thirteen short parts in a grid, each with its own
    # small picture, and a part's band takes in the whole row: (h) asks for an
    # electronic component and gets a compressor, a workbench and a chuck.
    (2021, 'ol', 1, 'h', None): 'the row holds other parts pictures',
    # Q7(c) offers a choice, and the crop takes the metrology instruments
    # printed above the OR rather than the eRacer the ask names.
    (2021, 'ol', 7, 'c', 'i'): 'shows the OR branch, not the eRacer',
    # "Name any three of the labelled parts on the lathe below" -- the arrows
    # are in the crop and the letters they point to are not.
    (2022, 'ol', 6, 'a', None): 'the labels the arrows point to are outside',
    (2022, 'ol', 6, 'c', 'i'): 'two pictures: knurling and a casting',
    # The same picture, which passes to the sibling when (i) is refused. A
    # rejection has to name every part that would inherit it.
    (2022, 'ol', 6, 'c', 'ii'): 'two pictures: knurling and a casting',
    (2023, 'hl', 8, 'b', 'i'): 'clips the word "machine" beneath it',
    # An ask with two OR branches whose crop serves only the second.
    (2024, 'hl', 8, 'c', 'i'): 'shows the CNC branch, not the lubrication one',
    (2024, 'ol', 5, 'a', 'i'): 'one of the items the ask says are shown',
    (2024, 'ol', 6, 'c', 'i'): 'shows the CNC branch, not the lathe part',
    (2025, 'ol', 4, 'c', 'i'): 'shows tool A, and (i) asks about the R-clip',
    # A recycling process drawn as a wheel, with its last stages printed
    # below the artwork's own box and clipped away: the ask says "describe
    # each of the stages" and the crop is missing one.
    (2023, 'hl', 7, 'c', 'ii'): 'a stage of the process is clipped off',
    (2025, 'hl', 5, 'c', 'i'): 'the last stages of the process are clipped off',
    (2025, 'hl', 5, 'c', 'ii'): 'the last stages of the process are clipped off',
}


def worklist():
    """Every census leaf whose printed wording points at something shown.

    Card lint's own condition, not a narrower one: Engineering writes
    "Identify the hybrid vehicle configuration shown opposite", which names no
    diagram at all, and a test that wants a noun beside a pointer word misses
    most of the subject.
    """
    import reconcile as R
    from paper_census import census_subject
    from lib import Author
    import cardlint
    out = []
    idx = R.leaf_index(census_subject('engineering'))
    for (year, level, _), leaves in sorted(idx.items()):
        A = Author('engineering', year, level)
        for q, letter, roman in sorted(leaves):
            try:
                text = ' '.join((A.paper.text(q, letter, roman) or '').split())
                stem = ' '.join((A.paper.stem(q, letter) or
                                 A.paper.stem(q) or '').split())
            except Exception:                                # noqa: BLE001
                continue
            if not text:
                continue
            # The author condemns a card on its stem, its own ask AND its
            # children joined on, because that is what the card carries. The
            # worklist has to ask the same question or it never offers the
            # cropper the parts that are actually being refused: 71 of the 127
            # figure refusals were not in it.
            kids = sorted((k for k in A.paper.parts
                           if k[0] == q and k[1] == letter
                           and (k[1], k[2]) != (letter, roman)),
                          key=lambda k: (k[1] or '', k[2] or ''))
            joined = ' '.join([stem, text]
                              + [(A.paper.text(*k) or '') for k in kids])
            if not (cardlint.FIG_REF.search(joined)
                    or cardlint.NAMES_LETTERS.search(joined)):
                continue
            out.append((year, level, q, letter, roman, joined))
    return out


def key_for(year, level, q, letter, roman):
    return (f'engineering-{year}-{level.upper()}-paper-q{q}'
            + (letter or '') + (roman or '') + '-art')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true',
                    help='render the crops to disk for review')
    ap.add_argument('--dir', default=os.path.join(ROOT, 'figures-review'))
    args = ap.parse_args()

    if args.write:
        os.makedirs(args.dir, exist_ok=True)
    cut, missed, refused = [], [], []
    seen = {}
    for year, level, q, letter, roman, ask in worklist():
        path = os.path.join(PAPERS, f'{year}-{level}-paper.pdf')
        if not os.path.exists(path):
            continue
        got = crop_for(path, q, letter, roman)
        if not got:
            missed.append((year, level, q, letter, roman))
            continue
        page, rect = got
        looked = REJECTED.get((year, level, q, letter, roman))
        if looked:
            refused.append((year, level, q, letter, roman, f'LOOKED: {looked}'))
            continue
        bad = faults(path, page, rect, ask)
        if bad:
            refused.append((year, level, q, letter, roman, bad[0]))
            continue
        # One crop per PICTURE, not per part: the parts that share a stimulus
        # share its crop, and cutting it twice would publish the same bytes
        # under two names.
        stamp = (year, level, page, tuple(round(v) for v in rect))
        if stamp in seen:
            cut.append((year, level, q, letter, roman, seen[stamp], rect, True))
            continue
        key = key_for(year, level, q, letter, roman)
        seen[stamp] = key
        if args.write:
            with pymupdf.open(path) as doc:
                pix = doc[page].get_pixmap(clip=pymupdf.Rect(*rect), dpi=200)
                pix.save(os.path.join(args.dir, f'{key}.png'))
        cut.append((year, level, q, letter, roman, key, rect, False))

    fresh = [c for c in cut if not c[7]]
    print(f'{len(fresh)} crops for {len(cut)} parts; {len(missed)} with nothing '
          f'to cut; {len(refused)} cut but REFUSED')
    for r in refused:
        print(f'   refused {r[0]} {r[1].upper()} Q{r[2]}{r[3] or ""}{r[4] or ""}'
              f'  — {r[5]}')
    for c in fresh:
        w, h = round(c[6][2] - c[6][0]), round(c[6][3] - c[6][1])
        shared = sum(1 for x in cut if x[5] == c[5]) - 1
        print(f'   {c[0]} {c[1].upper()} Q{c[2]}{c[3] or ""}{c[4] or ""}'
              f'  {w}x{h}  {c[5]}' + (f'  (+{shared} sharing)' if shared else ''))
    if args.write:
        with open(os.path.join(args.dir, 'catalogue.json'), 'w') as fh:
            json.dump([{'year': c[0], 'level': c[1], 'q': c[2], 'letter': c[3],
                        'roman': c[4], 'key': c[5], 'shared': c[7]} for c in cut],
                      fh, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
