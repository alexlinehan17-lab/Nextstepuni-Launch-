#!/usr/bin/env python3
"""Cut the picture an Applied Mathematics ask points at, part by part.

    python3 scripts/markbank/authoring/am_question_figures.py              # cut and report
    python3 scripts/markbank/authoring/am_question_figures.py --write      # render for review
    python3 scripts/markbank/authoring/am_question_figures.py --catalogue  # feed bind-figures.mjs
    python3 scripts/markbank/authoring/am_question_figures.py --probe "2021 HL Q5(b)"

WHY THIS FILE EXISTS
--------------------
Applied Mathematics is a mechanics subject and its questions are DRAWN. A
pulley over the edge of a table, a rod on two supports, a sphere striking
another obliquely at 30 degrees: the paper prints the geometry and the prose
only names it ("as shown in the diagram"). 111 of the 498 asks in the census
were refused for exactly that -- the card would point at a picture it does not
carry -- because no cropper had ever been written for this subject. Every
sibling subject has one; this is the missing one.

THE GEOMETRY, MEASURED RATHER THAN ASSUMED
------------------------------------------
Two booklets, one subject. The outgoing-syllabus papers (2021, 2022) are dense
question papers: a question head at x=56.7, its letters at 85.1, its romans at
113.4, prose at 113.4/141.8. The revised-specification papers (2023-2025) are
ANSWER BOOKLETS: "Question 1" at 56.7, letters and romans both at 56.7, prose
at 85.1, and a large light-grey ruled answer grid under every ask.

In BOTH, the artwork sits in one of two places, and which one varies question
by question on the same page:

  * BESIDE the prose, in the right column -- 2021 HL Q5(b) prints the two
    colliding spheres at x 397-561 while the sentence describing them runs to
    x 413.7 at the same height;
  * BENEATH the prose, centred and full width -- 2022 OL Q7(a) prints the rod
    and its two supports across x 170-480 under three lines of setup.

So the band of a part is cut at its marker, everything drawn inside it is
collected, and the labels printed ON the drawing are pulled in with it. What
separates a label from prose is the LEFT MARGIN: prose starts at one of the
four indents the booklet sets, and a label never does -- "10 m" starts at
310.4, "ku" at 539.7, the node "A" at 348.9. Where a stem line's bounding box
overhangs into the picture's column (the spheres case, by 3.6 points) the
prose is painted out rather than cropped around, because moving the box left
would cut the "u" arrow label off the incoming sphere.

WHAT IT REFUSES TO CUT
----------------------
  * the ruled answer grid -- a black frame at the left margin holding grey
    rules and no words. It is the space the candidate writes in. Bound as a
    figure it shows a student an empty box where the diagram should be;
  * a crop that carries the ASK. A caption or a label may stay; an ask is the
    question talking, the card already holds it as text, and a crop carrying
    it shows the student the question twice. The command word tells them
    apart;
  * a crop that does not carry the letters its ask names;
  * a crop the page furniture reaches into.

Every crop it makes is still OPENED and looked at before it is bound. REJECTED
below is the list that passed every mechanical gate above and was still the
wrong picture. The tool finds candidates; it does not decide.
"""
import argparse
import io
import json
import os
import re
import sys
import unicodedata

import pymupdf
from PIL import Image

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

import mathtext                                               # noqa: E402
import paper as PP                                            # noqa: E402

SUBJECT = 'applied-maths'
PAPERS = os.path.join(ROOT, 'examiner-reports', SUBJECT, 'papers')
# Published crops live beside every other subject's, under the gitignored
# exam-papers tree; bind-figures.mjs copies the ones it accepts into
# public/exam-figures/ and hashes them there.
OUT = os.path.join(ROOT, 'exam-papers', SUBJECT, 'figures')
MANIFEST = os.path.join(ROOT, 'components', 'MarkBank', 'figures.json')
# {card id: figure key} for am_all.py, written by --catalogue. Sibling of
# maths-question-figures.json and read for the same reason: the crops are
# shared between the romans of a part, so which part shows which crop is
# knowledge this pass has and the author does not.
SIDECAR = os.path.join(ROOT, 'scripts', 'markbank', 'authored',
                       f'{SUBJECT}-question-figures.json')

DPI = 200
# The page furniture. Nothing above the first line of a question and nothing
# below "Leaving Certificate, 2022 / Applied Mathematics - Ordinary Level"
# belongs to an ask; the footer's own y moves by up to 10pt between booklets,
# so the bound is set clear of the lowest content line measured (727.9).
HEAD, FOOT = 45.0, 772.0
PAD = 4.0

QHEAD = re.compile(r'^\s*(?:Question\s+(\d{1,2})|(\d{1,2})\.)\s*$')
LETTER = re.compile(r'^\(\s*([a-h])\s*\)')
ROMAN = re.compile(r'^\(\s*(i{1,3}|iv|v|vi{1,3}|ix|x)\s*\)')
# The four indents the two booklets set prose at. A line starting on one of
# them is the SEC talking to the candidate; a line starting anywhere else is
# printed on the drawing.
MARGINS = (56.7, 85.1, 113.4, 141.8)
MARGIN_TOL = 2.0
# A stroke this pale is the answer grid's ruling, not ink.
GREY = 0.5


def _lines(page):
    """[(x0, y0, x1, y1, text)] for the printed lines of one page.

    Unligatured on the way out, for the reason paper.py unligatures: the SEC
    typesets "ti" with a single Ɵ glyph, so the 2024 papers head their
    questions "QuesƟon 1". Matching the raw text found no head at all on that
    booklet, every band fell back to the whole page, and all thirteen of its
    figure-blocked asks came back as "nothing drawn in this part".
    """
    out = []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            text = mathtext.demangle(PP.unligature(
                ' '.join(''.join(s['text'] for s in line['spans']).split())))
            if not text:
                continue
            b = line['bbox']
            if b[3] <= HEAD or b[1] >= FOOT:
                continue
            out.append((b[0], b[1], b[2], b[3], text))
    out.sort(key=lambda r: (round(r[1], 1), r[0]))
    return out


def at_margin(x0):
    return any(abs(x0 - m) <= MARGIN_TOL for m in MARGINS)


def prose_lines(lines):
    """The lines that are the SEC talking, not labels printed on a drawing.

    The margin alone is not enough. A scheduling network is drawn across the
    full width of an answer booklet and its edge labels land wherever the
    graph puts them -- "B(12)" on 2023 HL Q9 starts at 85.1, exactly the
    indent the prose above it uses -- so reading the margin alone painted the
    activity the ask names out of its own diagram, and the crop was then
    refused for not carrying B.

    What a label never is, is a SENTENCE. So prose is a line at a margin with
    three words or more, plus any short line at the same margin sandwiched
    between two of them: "up." on its own at the foot of a paragraph is the
    tail of that paragraph, not a node.

    The margin is not required of a LONG line. A stacked fraction breaks the
    sentence it sits in into pieces that each begin at the fraction's own x --
    2025 HL Q5(a) sets "and the coefficient of friction between" starting at
    the numerator of a half -- and read by margin alone those pieces came back
    as labels and dragged two lines of setup into the crop of an inclined
    plane. Six words is past anything ever printed on one of these drawings --
    six WORDS, counted as runs of letters: the x-axis of 2023 OL Q3 is printed
    as one line reading "-8 -7 -6 -5 -4 -3 -2 -1", which is eight tokens and no
    words at all, and counting tokens painted the negative half of that axis
    off its own graph.
    """
    body = [l for l in lines
            if (at_margin(l[0]) and len(l[4].split()) >= 3)
            or len(re.findall(r'[A-Za-z]{2,}', l[4])) >= 6]
    out = list(body)
    for l in lines:
        if l in out or not at_margin(l[0]):
            continue
        above = any(abs(b[0] - l[0]) <= MARGIN_TOL and 0 < l[1] - b[3] < 24
                    for b in body)
        below = any(abs(b[0] - l[0]) <= MARGIN_TOL and 0 < b[1] - l[3] < 24
                    for b in body)
        # Sandwiched, or a sentence ENDING under one: "ends." hanging alone
        # below the setup of 2024 HL Q10(a) is the last word of that sentence,
        # and it printed over the source node of the network beneath it. A
        # table's first cell sits at the same margin and the same distance
        # below its own lead-in, so a full stop is what tells them apart.
        tail = (above and len(l[4].split()) <= 3
                and re.search(r'[.?!:]$', l[4]))
        if (above and below) or tail:
            out.append(l)
    # A stacked fraction's NUMERATOR is set as a line of its own, directly over
    # the line that carries its denominator and the rest of the sentence.
    # 2025 HL Q5(a) ends its setup on "... the coefficient of friction is 2/5.",
    # and painting out only the line the words are on left a stray "2" hanging
    # under an inclined plane.
    for l in lines:
        if l in out or len(l[4]) > 6:
            continue
        # The two boxes OVERLAP by about four points -- a fraction is set
        # tight -- so the window opens above the denominator's own top.
        if any(abs(b[0] - l[0]) <= 6 and -8 <= b[1] - l[3] <= 13 for b in out):
            out.append(l)
    return out


def furniture(line):
    """A question head or a bare part marker: the page's own numbering.

    "Question 9" is two words, so no sentence test reaches it, and a network
    drawn across the top of an answer booklet page comes within ten points of
    it -- which is how the crop of 2024 OL Q9 came back with the words
    "Question 9" printed over its source node.
    """
    x0, _y0, _x1, _y1, t = line
    return bool(at_margin(x0)
                and (QHEAD.match(t) or re.fullmatch(r'\(\s*[a-h]\s*\)', t)
                     or re.fullmatch(r'\(\s*(?:i{1,3}|iv|v|vi{1,3}|ix|x)\s*\)',
                                     t)))


def _grey(g):
    for key in ('fill', 'color'):
        c = g.get(key)
        if c and len(c) == 3 and min(c) >= GREY and max(c) - min(c) < 0.05:
            return True
    return False


def answer_grids(page):
    """The ruled boxes the candidate writes in.

    Drawn as a black frame at the left margin with light-grey rules inside and
    no words of its own. The revised-specification booklets print one under
    every ask, several to a page, and each is large enough to swamp any real
    drawing beside it.
    """
    rules = [g['rect'] for g in page.get_drawings() if _grey(g)]
    words = [l for l in _lines(page) if len(l[4]) > 2]
    out = []
    for g in page.get_drawings():
        r = g['rect']
        if r.width < 150 or r.height < 40 or _grey(g):
            continue
        if any(r.x0 - 2 < w[0] and w[2] < r.x1 + 2
               and r.y0 - 2 < w[1] and w[3] < r.y1 + 2 for w in words):
            continue
        inside = [q for q in rules
                  if r.x0 - 3 < q.x0 and q.x1 < r.x1 + 3
                  and r.y0 - 3 < q.y0 and q.y1 < r.y1 + 3]
        if len(inside) >= 3:
            out.append((r.x0, r.y0, r.x1, r.y1))
    return out


def grid_wash(page):
    """The ruling of an answer grid, as rectangles to paint out.

    The revised booklets draw a part's diagram ON TOP of the grid the candidate
    answers in, so the grid cannot simply be cropped around: 2025 OL Q8(a) sets
    its compass diagram inside a box that runs from y 79 to y 307, and the crop
    of the diagram came back with the first grey rule of that box ruled across
    its foot. Only rules INSIDE a box answer_grids() recognised are washed --
    the printed graph paper of 2023 OL Q3's vector diagram is the same pale
    grey and is the figure itself.
    """
    grids = answer_grids(page)
    out = []
    for g in page.get_drawings():
        r = g['rect']
        if not _grey(g):
            continue
        if any(gx0 - 3 < r.x0 and r.x1 < gx1 + 3
               and gy0 - 3 < r.y0 and r.y1 < gy1 + 3
               for gx0, gy0, gx1, gy1 in grids):
            out.append((r.x0, r.y0, r.x1, r.y1, ''))
    for gx0, gy0, gx1, gy1 in grids:
        out += [(gx0 - 1, gy0 - 1, gx1 + 1, gy0 + 1.5, ''),
                (gx0 - 1, gy1 - 1.5, gx1 + 1, gy1 + 1, ''),
                (gx0 - 1, gy0 - 1, gx0 + 1.5, gy1 + 1, ''),
                (gx1 - 1.5, gy0 - 1, gx1 + 1, gy1 + 1, '')]
    return out


def ink(page):
    """Every stroke that is part of a picture, as one rect per cluster.

    Filtering stroke by stroke (Engineering's rule: wider than 18 and taller
    than 18) loses the pieces a mechanics drawing is made of -- the dashed
    vertical of 2021 HL Q6(b)'s slide is 0.8 points wide and the arc above it
    is 16 points tall, and dropping both cropped the slide to its sandpit. So
    the strokes are CLUSTERED first and measured after: a picture is a group
    of strokes that touch or nearly touch, and a fraction bar set in the prose
    is a group of one, 18 points by 0.8, which no cluster test passes.
    """
    grids = answer_grids(page)
    rects = []
    for im in page.get_images(full=True):
        for r in page.get_image_rects(im[0]):
            rects.append((r.x0, r.y0, r.x1, r.y1))
    for g in page.get_drawings():
        if _grey(g):
            continue
        r = g['rect']
        if r.width <= 0.2 and r.height <= 0.2:
            continue
        rects.append((r.x0, r.y0, r.x1, r.y1))
    rects = [r for r in rects
             if r[1] > HEAD and r[3] < FOOT
             and not any(gx0 - 2 < r[0] and r[2] < gx1 + 2
                         and gy0 - 2 < r[1] and r[3] < gy1 + 2
                         for gx0, gy0, gx1, gy1 in grids)]
    return _cluster(rects)


# How close two strokes have to be to be one picture. Measured, not chosen:
# the widest gap inside a single drawing in this corpus is the 7.4 points
# between the arc and the dashed vertical of 2021 HL Q6(b)'s slide, and the
# narrowest gap BETWEEN two drawings is the 11.8 points separating 2021 OL
# Q4(a)'s pulley from Q4(b)'s inclined plane in the right-hand column of the
# same page. At 12 those two became one cluster, which straddled the boundary
# between the parts and was then inside neither band.
CLUSTER_GAP = 9.0


def _cluster(rects, gap=CLUSTER_GAP):
    groups = []
    for r in rects:
        hit = [g for g in groups if _near(g, r, gap)]
        merged = (min([r[0]] + [g[0] for g in hit]),
                  min([r[1]] + [g[1] for g in hit]),
                  max([r[2]] + [g[2] for g in hit]),
                  max([r[3]] + [g[3] for g in hit]))
        groups = [g for g in groups if g not in hit]
        groups.append(merged)
    # One pass leaves clusters that only met through a later rect; settle it.
    changed = True
    while changed:
        changed = False
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                if _near(groups[i], groups[j], gap):
                    groups[i] = (min(groups[i][0], groups[j][0]),
                                 min(groups[i][1], groups[j][1]),
                                 max(groups[i][2], groups[j][2]),
                                 max(groups[i][3], groups[j][3]))
                    del groups[j]
                    changed = True
                    break
            if changed:
                break
    return groups


def _near(a, b, gap):
    return (a[0] - gap < b[2] and b[0] - gap < a[2]
            and a[1] - gap < b[3] and b[1] - gap < a[3])


def question_spans(page):
    """{question number: (top, bottom)} for the questions headed on this page."""
    heads = []
    for x0, y0, _x1, _y1, t in _lines(page):
        m = QHEAD.match(t)
        if m and at_margin(x0) and abs(x0 - MARGINS[0]) <= MARGIN_TOL:
            heads.append((y0, int(m.group(1) or m.group(2))))
    out = {}
    for i, (y, q) in enumerate(heads):
        out[q] = (y, heads[i + 1][0] if i + 1 < len(heads) else FOOT)
    return out


def part_spans(page, top, bottom):
    """[(y, letter, roman)] for every part marker between top and bottom.

    A marker may open a line of its own or share it with the text it
    introduces, and the two booklets indent them differently -- the 2021 paper
    sets "(a)" at 85.1 and "(i)" at 113.4, the 2025 booklet sets both at 56.7.
    Reading them by INDENT would need a per-booklet table; reading them by
    alphabet does not, because a letter is drawn from (a)-(h) and a roman from
    {i, v, x}, and the two only collide at (i), which is never a letter here.
    """
    out = []
    letter = None
    for x0, y0, _x1, _y1, t in _lines(page):
        if not (top - 2 <= y0 <= bottom + 2) or not at_margin(x0):
            continue
        m, r = LETTER.match(t), ROMAN.match(t)
        if m:
            letter = m.group(1)
            rest = t[m.end():].strip()
            r2 = ROMAN.match(rest)
            out.append((y0, letter, r2.group(1) if r2 else None))
        elif r:
            out.append((y0, letter, r.group(1)))
    return out


def band_for(page, q, letter, roman, carried=None):
    """The vertical band this part owns on this page, or None.

    A question runs over pages and heads itself once, so a part past a page
    break sits under no head at all; `carried` is the question the page opened
    under. A LETTER owns everything down to the next letter, its own romans
    included, because the picture is printed once for the group.
    """
    spans = question_spans(page)
    if q in spans:
        top, bottom = spans[q]
    elif carried == q and not spans:
        top, bottom = HEAD, FOOT
    elif carried == q:
        top, bottom = HEAD, min(v[0] for v in spans.values())
    else:
        return None
    parts = part_spans(page, top, bottom)
    if letter is None and roman is None:
        # The whole of the question ON ITS OWN PAGE. Two conditions, each
        # measured: without the head, every page the question carries on to
        # answers to this key as well, and 2023 OL Q10 came back with the empty
        # ruled box off the "Do not write on this page" sheet six pages later.
        # And stopping at the first part marker is wrong here -- the same
        # question prints its scheduling network UNDER "(i)", shared by all six
        # of its romans, so a band that ended at (i) found nothing at all.
        # What keeps two romans' pictures apart is _stop_at_an_ask, not this.
        if q not in spans:
            return None
        return (top, bottom)
    if not parts:
        return None
    want = (letter, roman)
    here = next((i for i, (_y, le, rm) in enumerate(parts) if (le, rm) == want),
                None)
    if here is None:
        return None
    end = bottom
    for y, le, rm in parts[here + 1:]:
        if roman is None and rm and le == letter:
            continue                      # a roman of this same letter
        if (le, rm) == (letter, roman):
            continue
        end = y
        break
    return (parts[here][0], end)


# An instruction, as opposed to a caption or a label. Every command word the
# Applied Mathematics census actually sets, read off the paper rather than
# guessed: this subject says "Find", "Show that", "Calculate", "Deduce",
# "Prove" where Engineering says "Identify" and "Name".
ASK_LINE = re.compile(
    r'^\(?\s*(?:[a-h]|i{1,3}|iv|v|vi{1,3}|ix|x|\d{1,2})?\s*\)?\s*'
    r'(?:briefly\s+)?(?:calculate|find|show|prove|deduce|determine|state|'
    r'explain|describe|write|draw|sketch|solve|derive|give|list|name|'
    r'identify|verify|estimate|evaluate|complete|use|using|hence|if|by|'
    r'copy|comment|suggest|what|why|how)\b', re.I)

# "she stands at P", "the nodes A to L", "labelled M in the diagram". When the
# ask names its letters, the crop has to CARRY them.
NAMED = re.compile(
    r'\b(?:at|labell?ed|marked|points?|nodes?|vertices|vertex)\s+'
    r'([A-Z](?:\s*,\s*[A-Z])*(?:\s+and\s+[A-Z])?)\b')
# "are labelled with the letters A to L" -- a RANGE, and the whole of it is
# printed on the network. This one sentence governs every scheduling and
# shortest-path question in the revised specification.
RANGE = re.compile(r'\bletters?\s+([A-Z])\s+to\s+([A-Z])\b')


def letters_named(text):
    # Demangled first, for the reason the page's own lines are: the paper sets
    # its point names in the Mathematical Italic block, so an ASCII search for
    # "at P" misses the very sentence that names P.
    text = mathtext.demangle(text or '')
    out = []
    for m in NAMED.finditer(text or ''):
        for g in m.groups():
            if g:
                out += re.findall(r'\b([A-Z])\b', g)
    for m in RANGE.finditer(text or ''):
        a, b = ord(m.group(1)), ord(m.group(2))
        if 0 < b - a < 26:
            out += [chr(c) for c in range(a, b + 1)]
    return sorted(set(out))


def plan(path, q, letter, roman):
    """(page, rect, [prose boxes to paint out], [label texts]) or None.

    Widest grain first. A picture is printed ONCE for the group that shares
    it, and a narrower band cuts a piece out of it: the question's own setup
    band where the question sets its romans directly (2023 OL Q10 prints one
    scheduling network and asks six things about it), the letter's band where
    it has letters, and the roman's own band only as a last resort.
    """
    keys = [(None, None)] if letter is None else [(letter, None), (None, None)]
    if roman or letter:
        keys.append((letter, roman))
    for le, rm in keys:
        got = _plan(path, q, le, rm)
        if got:
            return got
    return None


def _plan(path, q, letter, roman):
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
            art = [a for a in ink(page) if a[1] >= top - 8 and a[3] <= bottom + 8
                   and (a[2] - a[0]) > 26 and (a[3] - a[1]) > 20]
            if not art:
                continue
            lines = _lines(page)
            prose = prose_lines(lines)
            art = _stop_at_an_ask(art, lines)
            x0 = min(a[0] for a in art)
            y0 = min(a[1] for a in art)
            x1 = max(a[2] for a in art)
            y1 = max(a[3] for a in art)
            # The labels printed ON the drawing: anything in the band that is
            # not the SEC talking, within reach of the ink.
            labels = []
            for _ in range(6):
                grew = False
                for ln in lines:
                    lx0, ly0, lx1, ly1, _t = ln
                    if ln in prose or ln in labels or furniture(ln):
                        continue
                    if not (top - 8 <= ly0 <= bottom + 8):
                        continue
                    if not _near((x0, y0, x1, y1), (lx0, ly0, lx1, ly1), 10.0):
                        continue
                    labels.append(ln)
                    x0, y0 = min(x0, lx0), min(y0, ly0)
                    x1, y1 = max(x1, lx1), max(y1, ly1)
                    grew = True
                if not grew:
                    break
            rect = (x0 - PAD, y0 - PAD, x1 + PAD, y1 + PAD)
            if (rect[2] - rect[0]) < 40 or (rect[3] - rect[1]) < 30:
                continue
            over = [l for l in list(lines) + grid_wash(page)
                    if (l in prose or furniture(l) or not l[4])
                    and l[0] < rect[2] and l[2] > rect[0]
                    and l[1] < rect[3] and l[3] > rect[1]]
            return n, rect, over, [l[4] for l in labels]
    return None


def _stop_at_an_ask(art, lines):
    """The clusters up to the first one an ASK is printed in front of.

    2024 HL Q10(a) prints its scheduling network twice: once with the durations
    on it, and once with an empty box at every node, under "Complete the
    diagram below by writing the early time and the late time at the node
    representing each event." The second is the answer space. Taking the band
    whole stitched the two together and showed the student the question's own
    working sheet.

    An ask printed BESIDE a drawing decides nothing -- the revised booklets set
    every roman beside the picture it asks about. Only an ask that lies wholly
    between one cluster and the next is a boundary.
    """
    art = sorted(art, key=lambda a: a[1])
    keep = [art[0]]
    for nxt in art[1:]:
        bottom = max(a[3] for a in keep)
        if any(ASK_LINE.match(t) and len(t.split()) > 3
               and ly0 >= bottom - 1 and ly1 <= nxt[1] + 1
               for _lx0, ly0, _lx1, ly1, t in lines):
            break
        keep.append(nxt)
    return keep


def faults(rect, prose, labels, ask):
    """Why this crop must not be published, if it must not."""
    bad = []
    want = letters_named(ask)
    if want:
        have = set(re.findall(r'(?<![A-Za-z])([A-Z])(?![A-Za-z])',
                              ' '.join(labels)))
        missing = [w for w in want if w not in have]
        if missing:
            bad.append(f'does not carry {", ".join(missing)}')
    # The ask must not be IN the crop. Every line of the SEC's own prose that
    # the box overlaps is painted out before it is rendered, so the only way an
    # ask survives into a crop is for the reader to have taken it for a label
    # printed on the drawing -- and then it ships, in the question area, above
    # the same words the card already prints. Judged on what is drawn, not on
    # what was painted out.
    for t in labels:
        if ASK_LINE.match(t) and len(t.split()) > 3:
            bad.append(f'carries the ask: {t[:44]!r}')
            break
    # A box with nothing written in it anywhere is not a diagram in this
    # subject. Every drawing an Applied Mathematics ask points at carries a
    # letter, an angle or a measurement -- that is what the ask is FOR -- and
    # the shapes that carry nothing are the ruled boxes the candidate writes
    # in, which is what 2023 OL Q10(ii) came back holding.
    if not labels:
        bad.append('nothing is printed inside it')
    # Painting out a line of setup that overhangs the picture's column is one
    # thing; painting out half the crop is another, and means the box is round
    # the prose rather than round the drawing.
    area = (rect[2] - rect[0]) * (rect[3] - rect[1])
    over = sum(max(0.0, min(rect[2], p[2]) - max(rect[0], p[0]))
               * max(0.0, min(rect[3], p[3]) - max(rect[1], p[1]))
               for p in prose)
    if area and over / area > 0.28:
        bad.append(f'{100 * over / area:.0f}% of the box is question prose')
    # The text column of these pages runs 45 to 772. A box past that is not a
    # figure, it is the page.
    if rect[3] - rect[1] > 690:
        bad.append('as deep as the whole text column')
    return bad


def render(path, page, rect, prose):
    """The crop, with any prose overhanging the picture's column painted out."""
    with pymupdf.open(path) as doc:
        p = doc[page]
        pix = p.get_pixmap(clip=pymupdf.Rect(*rect), dpi=DPI)
        img = Image.open(io.BytesIO(pix.tobytes('png'))).convert('L')
    scale = DPI / 72.0
    px = img.load()
    w, h = img.size
    painted = []
    for lx0, ly0, lx1, ly1, _t in prose:
        a = max(0, int((lx0 - rect[0]) * scale) - 1)
        b = min(w, int((lx1 - rect[0]) * scale) + 2)
        c = max(0, int((ly0 - rect[1]) * scale) - 1)
        d = min(h, int((ly1 - rect[1]) * scale) + 2)
        for y in range(c, d):
            for x in range(a, b):
                px[x, y] = 255
        painted.append((c, d))
    return _trim(_close_gaps(img, painted))


def _close_gaps(img, painted, white=247):
    """Take out the rows a painted-over line left empty.

    A part whose diagram is printed above its table -- the melting ice cube of
    2023 OL Q1(b), the campus map of Q4(a) -- has three lines of setup between
    the two, and painting them white leaves a band of nothing in the middle of
    the crop. The band is not part of the picture, so it goes. Only rows that a
    paint stroke actually covered are considered: a drawing's own white space
    (the gap between the ceiling and the circle of a conical pendulum) is the
    drawing, and squeezing it would redraw the SEC's geometry.
    """
    if not painted:
        return img
    px = img.load()
    w, h = img.size
    covered = set()
    for c, d in painted:
        covered.update(range(max(0, c), min(h, d)))
    drop = set()
    run = []
    for y in range(h):
        if y in covered and all(px[x, y] >= white for x in range(w)):
            run.append(y)
            continue
        if len(run) >= 10:
            drop.update(run[5:-5] if len(run) > 10 else run)
        run = []
    if len(run) >= 10:
        drop.update(run[5:-5] if len(run) > 10 else run)
    if not drop:
        return img
    keep = [y for y in range(h) if y not in drop]
    out = Image.new('L', (w, len(keep)), 255)
    op = out.load()
    for i, y in enumerate(keep):
        for x in range(w):
            op[x, i] = px[x, y]
    return out


def _trim(img, white=247):
    px = img.load()
    w, h = img.size

    def blank_row(y):
        return all(px[x, y] >= white for x in range(0, w))

    def blank_col(x):
        return all(px[x, y] >= white for y in range(0, h))

    top, bot = 0, h - 1
    while top < h and blank_row(top):
        top += 1
    while bot > top and blank_row(bot):
        bot -= 1
    left, right = 0, w - 1
    while left < w and blank_col(left):
        left += 1
    while right > left and blank_col(right):
        right -= 1
    if bot - top < 20 or right - left < 30:
        return None
    m = int(0.03 * DPI)
    return img.crop((max(0, left - m), max(0, top - m),
                     min(w, right + 1 + m), min(h, bot + 1 + m)))


# What the gates pass and a person then rejected. Every crop this tool makes is
# opened and looked at before it is bound; anything that survives every
# mechanical test above and is still the wrong picture belongs here, by name, so
# that a later run cannot quietly publish it.
#
# EMPTY BY MEASUREMENT, not by omission. All 47 crops in the published set were
# rendered and opened. Six were rejected on sight, and every one of the six
# turned out to be this reader misreading the page rather than the page being
# unusable, so each was fixed here instead of blacklisted — a blacklist entry
# would have hidden a fault that was also damaging its neighbours:
#
#   2023 OL Q10(ii)   an empty ruled box off the "Do not write on this page"
#                     sheet six pages past the question -> band_for() now
#                     requires the question to HEAD the page it answers on;
#   2024 OL Q9(i)     the words "Question 9" printed over the source node of a
#                     scheduling network -> furniture() paints the page's own
#                     numbering out;
#   2024 HL Q10(a)    two copies of one network stitched together, the second
#                     being the blank one the candidate fills in -> the band
#                     stops at an ask printed between two drawings;
#   2023 OL Q3(i)     the negative half of a vector graph's x-axis erased,
#                     because "-8 -7 -6 -5 -4 -3 -2 -1" is eight tokens and was
#                     read as a sentence -> prose is counted in WORDS;
#   2025 HL Q5(a)(ii) a stray "1" under an inclined plane, the numerator of a
#                     half whose denominator had been painted out -> a stacked
#                     fraction is painted out whole;
#   2025 OL Q8(a)(i)  one grey rule of the answer grid ruled across the foot of
#                     a compass diagram drawn on top of it -> grid_wash().
#
# Anything a future sitting throws up that is NOT a reader fault goes here.
REJECTED = {}


def worklist():
    """Every ask the author refuses for pointing at printed matter.

    The author's own condition, evaluated on the author's own text, so the
    worklist and the refusal list are the same list. Anything narrower offers
    the cropper parts that are not actually blocked and misses ones that are.

    Evaluated with the bindings this tool WROTE set aside. They are the reason
    those asks are no longer refused, so reading the refusals with them in
    place returned an empty worklist on the second run -- and --catalogue would
    then have written an empty sidecar and unbound all 49 crops.
    """
    import am_all as A
    import cardlint
    from paper_census import census_subject
    A.FIGURES = {}
    census = census_subject(SUBJECT)
    by_paper = {(p['year'], p['level']): [tuple(l['key']) for l in p['leaves']]
                for p in census['papers']}
    out = []
    for year in A.YEARS:
        for level in A.LEVELS:
            Au = A.Author(year, level)
            todo, _ = A.plan(Au, by_paper[(year, level)])
            for key, units, _why in todo:
                try:
                    Au.card(key, units, by_paper[(year, level)])
                except A.Refused as e:
                    if 'printed matter' not in e.args[0][0]:
                        continue
                    q = A.FURNITURE_TAIL.sub('', Au.question(key)).strip(' .;,')
                    q = A.LEADING_LABEL.sub('', q)
                    joined = ' '.join(f'{Au.stem(key)} {q}'.split())
                    out.append((year, level, key[0], key[1], key[2], joined))
                    continue
    return out


def key_for(year, level, q, letter, roman):
    return (f'{SUBJECT}-{year}-{level.upper()}-paper-q{q}'
            + (letter or '') + (roman or '') + '-art')


def card_id(year, level, q, letter, roman):
    """The id am_all.py gives this ask. Imported rather than restated, so the
    two cannot drift and leave a binding pointing at no card."""
    import am_all
    return am_all.card_id(year, level, (q, letter, roman))


def readable(text):
    """The same characters, in a form a screen reader can say.

    The paper sets its variables in the Mathematical Alphanumeric block, so a
    label lifted from it reads "𝜃" and "𝚥". Folded per character and only where
    the fold lands somewhere a reader knows: ASCII, or Greek, which the build's
    own broken-glyph test already counts as real script. Anything else is left
    exactly as the paper set it rather than guessed at.
    """
    out = []
    for ch in text or '':
        nf = unicodedata.normalize('NFKC', ch)
        if len(nf) == 1 and (ord(nf) < 128 or 0x370 <= ord(nf) <= 0x3FF):
            out.append(nf)
        elif nf in ('ȷ', 'ı'):        # dotless j, dotless i
            out.append('j' if nf == 'ȷ' else 'i')
        else:
            out.append(ch)
    return ''.join(out)


def describe(year, level, q, letter, roman, labels):
    ref = (f'{year} {level.upper()} Q{q}' + (f'({letter})' if letter else '')
           + (f'({roman})' if roman else ''))
    text = (f'The diagram printed with Applied Mathematics {ref}, as the State '
            f'Examinations Commission set it on the examination paper.')
    if labels:
        text += (' The labels printed on it read: '
                 + readable(', '.join(labels[:18])[:420]) + '.')
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true',
                    help='render the crops to --dir for review')
    ap.add_argument('--catalogue', action='store_true',
                    help='render the crops under exam-papers/ and print the '
                         'catalogue bind-figures.mjs reads')
    ap.add_argument('--probe', help='one part, e.g. "2021 HL Q5(b)"')
    ap.add_argument('--dir', default=os.path.join(ROOT, 'figures-review-am'))
    args = ap.parse_args()

    jobs = worklist()
    if args.probe:
        m = re.match(r'(\d{4})\s+(HL|OL)\s+Q(\d{1,2})'
                     r'(?:\(([a-h])\))?(?:\(([ivx]{1,4})\))?$',
                     args.probe.strip(), re.I)
        if not m:
            print('probe looks like "2021 HL Q5(b)(ii)"')
            return 1
        year, level = int(m.group(1)), m.group(2).lower()
        q = int(m.group(3))
        letter = (m.group(4) or '').lower() or None
        roman = (m.group(5) or '').lower() or None
        jobs = [j for j in jobs if (j[0], j[1], j[2]) == (year, level, q)
                and (letter is None or j[3] == letter)
                and (roman is None or j[4] == roman)]
        if not jobs:
            jobs = [(year, level, q, letter, roman, '')]
        os.makedirs(args.dir, exist_ok=True)
        for year, level, q, letter, roman, ask in jobs:
            path = os.path.join(PAPERS, f'{year}-{level}-paper.pdf')
            got = plan(path, q, letter, roman)
            ref = f'{year} {level.upper()} Q{q}{letter or ""}{roman or ""}'
            if not got:
                print(f'{ref}: nothing drawn in this part')
                continue
            page, rect, prose, labels = got
            print(f'{ref}: page {page + 1}, '
                  f'{[round(v, 1) for v in rect]}')
            print(f'   letters the ask names: {letters_named(ask) or "none"}')
            print(f'   labels in the box: {labels}')
            print(f'   prose painted out: {[p[4][:40] for p in prose]}')
            print(f'   faults: {faults(rect, prose, labels, ask) or "none"}')
            img = render(path, page, rect, prose)
            if img is None:
                print('   the box is blank')
                continue
            out = os.path.join(args.dir,
                               f'{key_for(year, level, q, letter, roman)}.png')
            img.save(out, optimize=True)
            print(f'   -> {out}  {img.size}')
        return 0

    if args.write or args.catalogue:
        os.makedirs(args.dir, exist_ok=True)
    cut, missed, refused, catalogue = [], [], [], []
    seen = {}
    for year, level, q, letter, roman, ask in jobs:
        path = os.path.join(PAPERS, f'{year}-{level}-paper.pdf')
        if not os.path.exists(path):
            continue
        got = plan(path, q, letter, roman)
        if not got:
            missed.append((year, level, q, letter, roman, 'nothing drawn in '
                                                         'this part'))
            continue
        page, rect, prose, labels = got
        looked = REJECTED.get((year, level, q, letter, roman))
        if looked:
            refused.append((year, level, q, letter, roman, f'LOOKED: {looked}'))
            continue
        bad = faults(rect, prose, labels, ask)
        if bad:
            refused.append((year, level, q, letter, roman, bad[0]))
            continue
        # One crop per PICTURE, not per part: the romans under a letter share
        # its diagram, and cutting it twice would publish the same bytes under
        # two names -- which bind-figures.mjs refuses, rightly.
        stamp = (year, level, page, tuple(round(v, 1) for v in rect))
        if stamp in seen:
            cut.append((year, level, q, letter, roman, seen[stamp], rect, True))
            continue
        img = render(path, page, rect, prose)
        if img is None:
            missed.append((year, level, q, letter, roman, 'the box is blank'))
            continue
        key = key_for(year, level, q, letter, roman)
        seen[stamp] = key
        if args.write:
            img.save(os.path.join(args.dir, f'{key}.png'), optimize=True)
        if args.catalogue:
            d = os.path.join(OUT, f'{year}-{level}')
            os.makedirs(d, exist_ok=True)
            img.save(os.path.join(d, f'{key}.png'), optimize=True)
            catalogue.append({
                'file': f'{key}.png', 'kind': 'figure', 'truncated': False,
                'questionRef': (f'{year} {level.upper()} Q{q}'
                                + (f'({letter})' if letter else '')
                                + (f'({roman})' if roman else '')),
                'description': describe(year, level, q, letter, roman, labels),
            })
        cut.append((year, level, q, letter, roman, key, rect, False))

    if args.catalogue:
        # The part-to-crop map the author reads. A part names a KEY and never a
        # path: build-deck.mjs resolves the key against the manifest, checks the
        # file is still on disk and that its bytes still hash to what the
        # inspecting agent saw, and refuses otherwise. It has to be written here
        # because the crops are SHARED -- 2021 HL Q4(a)(iii) shows the picture
        # cut for (a)(ii) -- and only this pass knows which parts met in which
        # box.
        sidecar = {card_id(y, lv, q, le, rm): key
                   for y, lv, q, le, rm, key, _rect, _shared in cut}
        with open(SIDECAR, 'w', encoding='utf-8') as fh:
            json.dump(sidecar, fh, ensure_ascii=False, indent=1)
            fh.write('\n')
        print(json.dumps(catalogue, ensure_ascii=False, indent=1))
        print(f'wrote {len(sidecar)} binding(s) to {SIDECAR}', file=sys.stderr)
        return 0
    fresh = [c for c in cut if not c[7]]
    print(f'{len(fresh)} crop(s) for {len(cut)} part(s); {len(missed)} with '
          f'nothing to cut; {len(refused)} cut but REFUSED')
    for r in sorted(refused):
        print(f'   refused {r[0]} {r[1].upper()} Q{r[2]}{r[3] or ""}'
              f'{r[4] or ""}  - {r[5]}')
    for r in sorted(missed):
        print(f'   missed  {r[0]} {r[1].upper()} Q{r[2]}{r[3] or ""}'
              f'{r[4] or ""}  - {r[5]}')
    for c in sorted(fresh):
        w, h = round(c[6][2] - c[6][0]), round(c[6][3] - c[6][1])
        shared = sum(1 for x in cut if x[5] == c[5]) - 1
        print(f'   {c[0]} {c[1].upper()} Q{c[2]}{c[3] or ""}{c[4] or ""}'
              f'  {w}x{h}  {c[5]}' + (f'  (+{shared} sharing)' if shared else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
