#!/usr/bin/env python3
"""Crop the printed matter a PART is built on, for any subject.

    python3 scripts/markbank/authoring/question_art.py agricultural-science
    python3 scripts/markbank/authoring/question_art.py agricultural-science --write
    python3 scripts/markbank/authoring/question_art.py <subject> --catalogue

The worklist is the deck itself: every card whose text points at something
printed -- "Identify the conditions necessary for germination by placing a tick
in the correct box", "From your diagram above" -- and which carries no figure.
Those cards cannot be answered by a student, and the crop is the missing input.

The geometry is cs_question_figures'. It was written for Computer Science and
every hard part of it is subject-agnostic: which bands of a page are printed
matter rather than the ruled space a candidate writes in, how to follow a
table down through its own rules, how to trim a blank answer box off the top,
the foot or the side. Importing it is the point -- a second copy would drift,
and the rules it encodes were each found by opening a crop and looking at it.

What this adds is the PART BAND. Computer Science crops one figure per
question; here the worklist is per part, and a question's parts each have
their own table -- Agricultural Science 2025 OL Q5 prints a soil diagram for
(a) and (b) and a three-row tick-box for (c). So the page is cut at the part
markers and only the bands inside the part's own slice are considered.
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

import paper as PP                                          # noqa: E402
import cs_question_figures as G                             # noqa: E402
import cardlint                                             # noqa: E402

DPI = 150
PAD = 8.0
# The same test the audit uses: a reference to something PRINTED that the card
# would have to show. Kept here rather than imported so the two can be read
# side by side.
POINTS_AT = re.compile(
    r'\b(?:from your |in your |the )?(?:diagram|graph|chart|sketch|figure|fig\.?'
    r'|table|photograph|photo|image|picture|drawing|flowchart|map|extract'
    r'|passage|text|cartoon|label(?:led)?)\b[^.]{0,40}?'
    r'\b(?:above|below|shown|opposite|following|provided|supplied|attached)\b'
    r'|\b(?:above|below|opposite|shown)\b[^.]{0,20}\b(?:diagram|graph|table|figure)\b'
    r'|\bfrom (?:your|the) (?:diagram|graph|table|figure)\b'
    r'|\btick\b[^.]{0,30}\b(?:box|table|column)\b'
    r'|\brefer(?:ring)? to the (?:diagram|graph|table|figure|extract|passage)\b',
    re.I)
# Every ref shape the eleven decks use. Maths writes "2021 HL Paper 1 Q5(b)",
# Business "2021 OL Section 1 Q10", Home Economics "2021 HL Section A Q3",
# Economics both "2021 HL Section A Q4(b)" and "2021 HL Q13(b)(i)". The
# component between the level and the Q is skipped rather than parsed: it
# names a booklet or a section, and the crop is found by the question and part
# on the page.
REF = re.compile(r'^(\d{4})\s+(HL|OL)\s+(?:(?:Paper|Section)\s*\w+\s+)?'
                 r'Q(\d{1,2})'
                 r'(?:\(([a-hj-z])\))?(?:\(([ivxlc]+)\))?', re.I)
MARKER = re.compile(r'^\(([a-z]{1,4})\)')
# A card whose choices are printed in its OWN words needs no crop, and asking
# for one gets a wrong answer: 2025 OL Q2 lists its true/false statements in
# its text and the cropper handed it a soil-temperature bar chart belonging to
# another question. Mirrors attach-question-figures.py.
OPTIONS_INLINE = re.compile(r':\s*[^:]{3,}?\s+/\s+[^:]{3,}|true or false'
                            r'|\btrue\b.*\bfalse\b', re.I)


def carries_its_own_text(card):
    """Is the thing the card points at already ON the card, as its stem?

    Business's Applied Business Question says "Explain the term co-operative
    as mentioned in the text above", and the text above is the card's own
    stem: "Or-Real Irish Butter was launched in October 2021 ... a
    farmer-owned co-operative." Those cards are answerable as they stand, and
    cropping for them got the wrong section's page entirely.
    """
    text = ' '.join(f"{card.get('questionText') or ''} "
                    f"{card.get('stem') or ''}".split())
    # Only a reference to TEXT can be satisfied by the stem. "The diagram
    # shown opposite" cannot: prose is not a picture, however much of it there
    # is, and Engineering's stems are long while its diagrams are still
    # missing.
    if not re.search(r'\b(?:text|passage|information|extract|article|'
                     r'data|results?|figures|table)\b', text, re.I):
        return False
    stem = ' '.join((card.get('stem') or '').split())
    return len(stem) >= 150


def worklist(subject):
    """(year, level, q, letter, roman, card id) for every bare pointing card."""
    path = os.path.join(ROOT, 'scripts', 'markbank', 'authored', f'{subject}.json')
    out = []
    for card in json.load(open(path, encoding='utf-8')):
        if card.get('figureKey') or card.get('questionFigureKey'):
            continue
        text = ' '.join(f"{card.get('questionText') or ''} "
                        f"{card.get('stem') or ''}".split())
        if not POINTS_AT.search(text) or OPTIONS_INLINE.search(text):
            continue
        if carries_its_own_text(card):
            continue
        m = REF.match(card.get('questionRef') or '')
        if not m:
            continue
        out.append((int(m.group(1)), m.group(2).lower(), int(m.group(3)),
                    m.group(4), m.group(5), card['id']))
    return out


# The head may carry its tariff on the same line: Engineering prints
# "Question 4. (50 marks)". Demanding the number alone found no heads at all,
# so every question's span ran to the end of the paper and the crop came from
# whichever page happened to hold a matching part marker.
QHEAD_LINE = re.compile(
    r'^\s*(?:Question\s+)?(\d{1,2})\.?\s*(?:\(\s*\d{1,3}\s*marks?\s*\))?\s*$',
    re.I)


def question_span(page, q):
    """The slice of this page Question q owns, or None if it is not here.

    Pages carry more than one question. Finding the part marker anywhere on
    the page cropped 2022 HL Q10(a) as a table of calf weaning weights that
    belongs to a different question entirely — the marker was real, the
    question was not.
    """
    heads = []
    for (x0, y0, x1, y1), text in G.text_lines(page):
        m = QHEAD_LINE.match(text.strip())
        if m and x0 < page.rect.width * 0.35:
            heads.append((y0, int(m.group(1))))
    heads.sort()
    top = next((y for y, n in heads if n == q), None)
    if top is None:
        return None
    later = [y for y, n in heads if y > top + 2]
    return top, (min(later) if later else page.rect.height)


def census_worklist(subject):
    """(year, level, q, letter, roman, ref) for every PART that points at
    printed matter, taken from the census and the paper rather than the deck.

    A subject whose cards were REFUSED for pointing at a picture has no cards
    to read a worklist from -- that is the whole problem. Engineering refuses
    116 asks that way, and none of them is in the deck to be listed. So the
    paper is asked directly: every part the census knows about, whose printed
    wording points at something the card would have to show.
    """
    import reconcile as R                                    # noqa: PLC0415
    from paper_census import census_subject                  # noqa: PLC0415
    out = []
    idx = R.leaf_index(census_subject(subject))
    for (year, level, _), leaves in sorted(idx.items()):
        P = PP.Paper(subject, year, level)
        for leaf in sorted(leaves):
            q, letter, roman = leaf[-3], leaf[-2], leaf[-1]
            try:
                ask = P.text(q, letter, roman) or ''
            except Exception:                                # noqa: BLE001
                continue
            try:
                stem = P.stem(q, letter) or P.stem(q) or ''
            except Exception:                                # noqa: BLE001
                stem = ''
            text = ' '.join(f'{stem} {ask}'.split())
            # CARD LINT'S own condition, not this module's. The census mode
            # exists to satisfy that gate, and the gate is broader: it catches
            # "Identify the hybrid vehicle configuration shown opposite",
            # which names no diagram at all and so never matched POINTS_AT.
            # 116 Engineering asks are refused for pointing at a picture and
            # only 15 of them matched the narrower test.
            hit = cardlint.FIG_REF.search(text)
            table_only = bool(hit) and re.search(
                r'(?:table|chart|graph)\b', hit.group(0), re.I) \
                and cardlint.INLINE_TABLE.search(text)
            ghost = (hit and not cardlint.SELF_WORK.search(text)
                     and not cardlint.NO_DEPENDENCY.search(text)
                     and not table_only)
            lettered = (cardlint.NAMES_LETTERS.search(ask)
                        and not cardlint.INVITES_DRAWING.search(ask))
            if not (ghost or lettered) or OPTIONS_INLINE.search(text):
                continue
            if carries_its_own_text({'stem': stem, 'questionText': ask}):
                continue
            ref = (f'{year} {level.upper()} Q{q}'
                   + (f'({letter})' if letter else '')
                   + (f'({roman})' if roman else ''))
            out.append((year, level, q, letter, roman, ref))
    return out


def markers_on(page, span):
    """[(y, label)] for every part marker inside the question's span."""
    out = []
    for (x0, y0, x1, y1), text in G.text_lines(page):
        if not (span[0] - 2 <= y0 <= span[1] + 2):
            continue
        m = MARKER.match(text.strip())
        if m and x0 < page.rect.width * 0.35:
            out.append((y0, m.group(1)))
    return sorted(out)


def part_band(page, span, letter, roman):
    """(top, bottom) of the slice of this page the part owns, or None.

    Cut at the PART MARKERS, inside the question's own span. A question's
    parts each have their own printed matter and the page has to be divided
    between them, or (c)'s tick-box table is cropped for (a) as well.
    """
    marks = []
    for (x0, y0, x1, y1), text in G.text_lines(page):
        if not (span[0] - 2 <= y0 <= span[1] + 2):
            continue
        m = MARKER.match(text.strip())
        if m and x0 < page.rect.width * 0.35:
            marks.append((y0, m.group(1)))
    want = roman or letter
    if want is None:
        # A card citing the whole QUESTION takes the question's SHARED
        # stimulus -- everything above its first part -- and not the page
        # entire: 2024 OL Q3 came out as a grazing diagram with parts (b), (c)
        # and (d)'s empty answer boxes stacked underneath.
        return span[0], (marks[0][0] if marks else span[1])
    marks.sort()
    for i, (y, label) in enumerate(marks):
        if label != want:
            continue
        nxt = marks[i + 1][0] if i + 1 < len(marks) else span[1]
        return y, nxt
    return None


def pages_for(P, q):
    """(path, page, top, bottom) for everything Question q owns.

    A question owns the paper from its own heading to the NEXT heading, and
    that runs across pages: 32 of the parts this tool could not crop had their
    head on the page before. Matching only pages that CARRY the head found the
    head page and then failed to find the part marker on it, because the part
    was overleaf.
    """
    out, open_at = [], None
    for path in P.files:
        with pymupdf.open(path) as doc:
            for n in range(doc.page_count):
                page = doc[n]
                heads = []
                for (x0, y0, x1, y1), text in G.text_lines(page):
                    m = QHEAD_LINE.match(text.strip())
                    if m and x0 < page.rect.width * 0.35:
                        heads.append((y0, int(m.group(1))))
                heads.sort()
                mine = next((y for y, num in heads if num == q), None)
                if mine is not None:
                    open_at = mine
                elif open_at is None:
                    continue
                else:
                    open_at = 0.0
                later = [y for y, num in heads if num != q and y > open_at + 2]
                out.append((path, n, open_at, min(later) if later else page.rect.height))
                if later:
                    open_at = None
    return out


# A card that reads FROM A PASSAGE. Physics sets "Read the following passage
# and answer the questions below", Business the Applied Business Question's
# text. The thing it needs is prose, not artwork, so figure_bands never sees
# it: the crop is the TEXT REGION between the question's head and its first
# part.
READS_PASSAGE = re.compile(
    r'\b(?:read the following|the following passage|the passage above|'
    r'the text above|the information above|read the information|'
    r'with reference to the text|from the text above|'
    r'the article above|the extract above)\b', re.I)


def crop_passage(subject, year, level, q, letter, roman, write=False):
    """The question's prose stimulus: its head down to its first part."""
    P = PP.Paper(subject, year, level)
    for path, n, span_top, span_bot in pages_for(P, q):
        with pymupdf.open(path) as doc:
            page = doc[n]
            rows = [r for r in G.text_lines(page)
                    if span_top - 2 <= r[0][1] <= span_bot + 2]
            if not rows:
                continue
            first_part = None
            for (x0, y0, x1, y1), text in rows:
                if MARKER.match(text.strip()) and x0 < page.rect.width * 0.35:
                    first_part = y0 if first_part is None else min(first_part, y0)
            body = [r for r in rows
                    if first_part is None or r[0][3] <= first_part - 2]
            # Prose, not a heading and not a stray line. A passage runs to
            # several lines of real sentences; anything shorter is the ask
            # itself and the card already carries that.
            words = sum(len(t.split()) for _, t in body)
            if len(body) < 4 or words < 40:
                continue
            x0 = min(r[0][0] for r in body)
            y0 = min(r[0][1] for r in body)
            x1 = max(r[0][2] for r in body)
            y1 = max(r[0][3] for r in body)
            rect = pymupdf.Rect(max(0.0, x0 - PAD), max(0.0, y0 - PAD),
                                min(page.rect.width, x1 + PAD),
                                min(page.rect.height, y1 + PAD))
            if (rect.width * rect.height
                    > 0.75 * page.rect.width * page.rect.height):
                continue
            part = (f'q{q}' + (f'{letter}' if letter else '')
                    + (f'{roman}' if roman else ''))
            name = f'{subject}-{year}-{level.upper()}-paper-{part}-passage'
            if write:
                d = os.path.join(ROOT, 'exam-papers', subject, 'figures',
                                 f'{year}-{level}')
                os.makedirs(d, exist_ok=True)
                page.get_pixmap(clip=rect, dpi=DPI).save(
                    os.path.join(d, f'{name}.png'))
            opening = ' '.join(' '.join(t for _, t in body[:2]).split())[:90]
            return name, rect, [opening]
    return None


def crop_part(subject, year, level, q, letter, roman, write=False):
    """The one crop this part needs, or None."""
    P = PP.Paper(subject, year, level)
    for path, n, span_top, span_bot in pages_for(P, q):
        with pymupdf.open(path) as doc:
            page = doc[n]
            band = part_band(page, (span_top, span_bot), letter, roman)
            if band is None:
                continue
            top, bottom = band
            runs = G.mono_runs(page)
            found = G.figure_bands(page, runs)
            bands = [b for b in found if b[1] >= top - 6 and b[3] <= bottom + 6]
            if not bands:
                # A part can be one ROW of a table the whole question shares:
                # Agricultural Science 2021 OL Q7 prints one table and (a) to
                # (e) are its rows, so nothing fits INSIDE the part's slice
                # and the crop has to be the table that CONTAINS it. That is
                # the question's stimulus, which every part under it may show.
                # A band that CONTAINS the part's slice belongs to the part
                # only if no OTHER part starts inside it. Agricultural Science
                # 2021 OL Q7 is one True/False table with (a) to (e) as its
                # rows -- every marker is inside it, and it is shared by all
                # of them. Engineering 2025 OL Q4 prints one picture per part,
                # and a band holding (a)(i)'s flames and nothing else is
                # (a)(i)'s; taking it for (c)(i) as well gave the R-clip
                # question a picture of three flames.
                others = [y for y, label in markers_on(page, (span_top, span_bot))
                          if label != (roman or letter)]
                bands = [b for b in found
                         if b[1] <= top + 6 and b[3] >= bottom - 6
                         and b[3] - b[1] < 0.75 * page.rect.height
                         and (not any(b[1] - 4 < y < b[3] + 4 for y in others)
                              or len([r for r in G.rule_rows(page)
                                      if b[1] - 4 <= r[1] <= b[3] + 4]) >= 2)]
            if not bands:
                continue
            # Several bands are one picture only if what lies BETWEEN them is
            # not the candidate's answer space. 2024 OL Q3 spans a grazing
            # diagram, then part (b)'s ruled box, then (c)'s and (d)'s, and
            # the union of all of it is a crop of three empty boxes with a
            # fragment of diagram on top. A wrong crop is worse than none.
            rows = list(G.text_lines(page))
            bands.sort(key=lambda b: b[1])
            clear = True
            for a, nxt in zip(bands, bands[1:]):
                if nxt[1] - a[3] <= 4.0:
                    continue
                if not G.gap_is_clear(page, min(a[0], nxt[0]), a[3],
                                      max(a[2], nxt[2]), nxt[1], rows):
                    clear = False
                    break
            if not clear:
                continue
            x0 = min(b[0] for b in bands)
            y0 = min(b[1] for b in bands)
            x1 = max(b[2] for b in bands)
            y1 = max(b[3] for b in bands)
            # A photograph printed BESIDE the question's prose takes the
            # picture, not the prose. 2025 HL Q1(d) sets its kettlebell photo
            # to the right of the ask and the union came out as half a
            # sentence -- "t iron is often used to manufacture ... te." --
            # with the photo alongside. Only where the prose is a real line of
            # the question, not a label: an A/B/C caption is short and must be
            # kept, which is what the furnaces and the lathe are labelled by.
            pics = [ir for im in page.get_images(full=True)
                    for ir in page.get_image_rects(im[0])
                    if not G.is_a_rule(ir.x0, ir.y0, ir.x1, ir.y1)
                    and x0 - 2 <= ir.x0 and ir.x1 <= x1 + 2
                    and y0 - 2 <= ir.y0 and ir.y1 <= y1 + 2]
            if pics:
                left = min(p.x0 for p in pics)
                prose = [r for r in rows
                         if y0 - 2 < r[0][1] and r[0][3] < y1 + 2
                         and r[0][0] < left - 4 and len(r[1].strip()) > 20]
                if prose:
                    x0 = left
            # The union can still end inside the candidate's answer space when
            # the box sits hard against the picture: 2022 OL Q4(b) prints its
            # composition table and a photograph, then "Protein: / Fibre:"
            # over six ruled lines with no gap between.
            y1 = G.trim_answer_box(page, x0, y0, x1, y1, rows)
            top, bot = max(0.0, y0 - PAD), min(page.rect.height, y1 + PAD)
            # A crop may leave a line of type out; it must not show the top
            # half of one. Applied AFTER the padding, because it is the
            # padding that reaches back into the line above.
            for (lx0, ly0, lx1, ly1), _ in rows:
                if lx1 < x0 - 2 or lx0 > x1 + 2:
                    continue
                if ly0 < top < ly1:
                    top = ly1 + 1
                if ly0 < bot < ly1:
                    bot = ly0 - 1
            rect = pymupdf.Rect(max(0.0, x0 - PAD), top,
                                min(page.rect.width, x1 + PAD), bot)
            # A crop that is most of the page is the PAGE, not a figure. The
            # shared-stimulus fallback for a whole-question card can reach
            # that when the question has no part markers on the page it lands
            # on, and a card showing a student a whole exam page has not been
            # given context, it has been given the paper.
            if (rect.width * rect.height
                    > 0.55 * page.rect.width * page.rect.height):
                continue
            part = (f'q{q}' + (f'{letter}' if letter else '')
                    + (f'{roman}' if roman else ''))
            name = (f'{subject}-{year}-{level.upper()}-paper-{part}-art')
            if write:
                d = os.path.join(ROOT, 'exam-papers', subject, 'figures',
                                 f'{year}-{level}')
                os.makedirs(d, exist_ok=True)
                page.get_pixmap(clip=rect, dpi=DPI).save(
                    os.path.join(d, f'{name}.png'))
            labels = [t for b in bands for t in b[4]]
            return name, rect, labels
    return None


def describe(subject, year, level, q, letter, roman, labels):
    ref = (f'{year} {level.upper()} Question {q}'
           + (f'({letter})' if letter else '') + (f'({roman})' if roman else ''))
    text = (f'The table or diagram printed with {ref}, as the State '
            f'Examinations Commission set it.')
    if labels:
        text += ' It reads: ' + ', '.join(labels[:14])[:400] + '.'
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject')
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--catalogue', action='store_true')
    ap.add_argument('--census', action='store_true',
                    help='take the worklist from the census and the paper, '
                         'for a subject whose cards do not exist yet because '
                         'they were refused for pointing at a picture')
    args = ap.parse_args()

    cards = {c['id']: c for c in json.load(open(os.path.join(
        ROOT, 'scripts', 'markbank', 'authored', f'{args.subject}.json'),
        encoding='utf-8'))}
    jobs = (census_worklist(args.subject) if args.census
            else worklist(args.subject))
    made, missed, catalogue = [], [], []
    for year, level, q, letter, roman, cid in jobs:
        card = cards.get(cid, {})
        text = ' '.join(f"{card.get('questionText') or ''} "
                        f"{card.get('stem') or ''}".split())
        if args.census:
            P = PP.Paper(args.subject, year, level)
            try:
                text = ' '.join(f'{P.stem(q, letter) or P.stem(q) or ""} '
                                f'{P.text(q, letter, roman) or ""}'.split())
            except Exception:                                # noqa: BLE001
                text = ''
        cut = crop_passage if READS_PASSAGE.search(text) else crop_part
        try:
            got = cut(args.subject, year, level, q, letter, roman,
                      write=args.write or args.catalogue)
        except Exception as exc:                             # noqa: BLE001
            print(f'{cid}: {type(exc).__name__}: {exc}', file=sys.stderr)
            got = None
        if not got:
            missed.append((cid, f'{year} {level.upper()} Q{q}'
                                f'{f"({letter})" if letter else ""}'
                                f'{f"({roman})" if roman else ""}'))
            continue
        name, rect, labels = got
        made.append((cid, name, round(rect.width), round(rect.height)))
        if args.catalogue:
            catalogue.append({
                'file': f'{name}.png', 'kind': 'figure', 'truncated': False,
                'questionRef': (f'{year} {level.upper()} Q{q}'
                                + (f'({letter})' if letter else '')
                                + (f'({roman})' if roman else '')),
                'cardId': cid,
                'description': describe(args.subject, year, level, q, letter,
                                        roman, labels),
            })
    if args.catalogue:
        print(json.dumps(catalogue, ensure_ascii=False, indent=1))
        return 0
    print(f'{len(made)} cropped, {len(missed)} with nothing to crop')
    for cid, name, w, h in made:
        print(f'   {cid:26} {w:4}x{h:<4} {name}')
    for cid, ref in missed:
        print(f'   MISSED {cid:20} {ref}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
