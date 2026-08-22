"""Find every cardable part of an Economics paper, and split its responses.

    python3 scripts/markbank/authoring/econ_parts.py 2024 higher
    python3 scripts/markbank/authoring/econ_parts.py 2024 higher --json

Hand-authoring reached 75 cards against 832 mark cells, because each card cost
minutes of reading. This does the mechanical half: it segments the scheme into
parts, reads each part's tariff, and splits the responses the examiner listed.
What it CANNOT do is decide the topic, write the question, or tell a menu from a
calculation — so its output is candidates for review, never cards.

The two layouts, neither of which is a level split:

  * bulleted — every response opens with "• "
  * headed   — "Improved transport – transport advances make..." , the heading
               being a short capitalised run before a dash or colon, at a
               sentence boundary

Validated against the hand-authored cards: `--check` re-splits the blocks those
were built from and reports any option it would have got wrong.
"""
import json
import os
import re
import sys

import pymupdf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_lib import as_option, defurnish, heads, load, tidy  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

# A part opens with its own numeral. Roman numerals are matched before letters so
# "(i)" is not read as the letter i.
PART = re.compile(r'\((?:i{1,3}|iv|v|vi{1,3}|[a-c])\)\s')
# The tariff, in every notation the ten papers use: ⟨2 @ 7⟩, ⟨1 x 8⟩, ⟨(3 + 4)⟩,
# ⟨12⟩, and the words "1st @ 8" / "2nd @ 4" spelled out beside the question.
# Ordinary schemes write the descending tariff beside the question in words,
# and write it two ways — "1st @ 8" on one paper and "1st x 9" on another.
CELL = re.compile(r'⟨([^⟩]{1,18})⟩|(\d+)(?:st|nd|rd|th)\s*[@x]\s*(\d+)')
MENU = re.compile(r'^(\d+)\s*[@x]\s*(\d+)$')
# "1st @ 8", "2nd @ 4" — the descending tariff written out in words.
ORDINAL = re.compile(r'^(\d+)(?:st|nd|rd|th)@(\d+)$')

# Section A numbers its questions "1." … "10." in the body text rather than
# heading them "Question 11" the way Section B does.
QUESTION = re.compile(r'(?<=[\s»])(\d{1,2})\.\s(?=[A-Z“‘(⟨])')
# Four of the ten schemes drop the point — "1 The adapted infographic…",
# "1 (a) Discuss…". A bare numeral is far too common in an economics scheme to
# match first, so this is only tried when the dotted form finds no paper.
QUESTION_BARE = re.compile(r'(?<=[\s»])(\d{1,2})\.?\s(?=[A-Z“‘(⟨])')

# A response heading: a short capitalised run closed by a dash or colon, taken
# only at a sentence boundary so a dash inside a sentence cannot split one
# marking point into two.
HEADED = re.compile(r'(?<=[.:;»)’]\s)(?=[A-Z‘“][^.•]{2,70}?\s?[–\-:]\s)')

# What a real response looks like: it opens with its own heading. Text that does
# not is the tail of the question the mark cell interrupted.
HEAD_LOOKS_LIKE_RESPONSE = re.compile(r'^[A-Z‘“(][^.]{0,80}?\s?[–\-:]\s')


def bold_runs(year, level):
    """Every bold run in the scheme PDF, in document order.

    The examiner heads each listed response in bold and then runs the
    explanation on in plain text, sometimes with a dash between them and
    sometimes with nothing at all:

        Incentivise FDI / discourage any exodus of MNCs   <- Calibri-Bold
        Ireland's low corporation tax rate has historically been...  <- Calibri

    With no dash there is nothing in the flat markdown to split on, which is why
    a text-only splitter found zero menus on the 2021 Higher paper and 27 on the
    2024 one. Bold is the one signal every paper shares. The PDF is read only to
    LEARN the headings; the option text itself is still sliced out of the
    markdown, so what a card quotes is still what the provenance gate searches.
    """
    for name in ([f'{year}-{"hl" if level == "higher" else "ol"}-marking-scheme.pdf']):
        path = os.path.join(ROOT, 'examiner-reports', 'economics', name)
        if not os.path.exists(path):
            return []
        out = []
        with pymupdf.open(path) as doc:
            for page in doc:
                for blk in page.get_text('dict')['blocks']:
                    if blk.get('type'):
                        continue
                    for line in blk['lines']:
                        run = ''
                        for sp in line['spans']:
                            if sp['flags'] & 16:            # bold
                                run += sp['text']
                            elif run:
                                out.append(tidy(run))
                                run = ''
                        if run:
                            out.append(tidy(run))
        # Bold is used for emphasis inside a sentence too — "increase",
        # "consumers" — and a one-word anchor cuts a marking point in half. A
        # response heading is a capitalised phrase of a few words.
        return [r for r in out
                if 15 <= len(r) <= 120 and r[:1].isupper() and ' ' in r
                and not r.endswith(('.', '?'))]
    return []


def split_on_headings(block, headings):
    """Split a response block wherever one of this paper's bold headings starts."""
    text = defurnish(block)
    cuts = []
    for h in headings:
        at = text.find(h)
        if at >= 0:
            cuts.append((at, h))
    cuts.sort()
    # Only headings that actually run in order, so a stray match inside an
    # earlier sentence cannot cut one marking point in half.
    kept, last = [], -1
    for at, h in cuts:
        if at > last:
            kept.append(at)
            last = at + len(h)
    if len(kept) < 2:
        return []
    bounds = kept + [len(text)]
    return [tidy(text[a:b]) for a, b in zip(bounds, bounds[1:]) if len(tidy(text[a:b])) >= 25]


def responses(chunk, headings=()):
    """The examiner's listed responses, however this paper lays them out.

    Every response is stopped where the next part of the paper begins. The last
    response of a part runs to the end of the chunk, and the chunk ends at the
    next PART numeral — which is not where the part ends when the next thing on
    the page is a question heading or a fresh response table. One shipped option
    ended "…they can be fined. Question 12 Possible responses Max Mark", and the
    provenance gate could not object because that text really is in the scheme,
    contiguously.
    """
    text = defurnish(chunk)
    if text.count('•') >= 2:
        out = [tidy(x) for x in text.split('•')]
    else:
        by_bold = split_on_headings(chunk, headings)
        out = by_bold if len(by_bold) >= 2 else [tidy(x) for x in HEADED.split(text)]
    return [o for o in (as_option(x) for x in out) if len(o) >= 25]


def read_cells(seg):
    """Every tariff cell in a segment, in the notation the paper printed it."""
    cells = []
    for m in CELL.finditer(seg):
        if m.group(1):
            cells.append(m.group(1).strip())
        else:
            cells.append(f'{m.group(2)}{"st" if m.group(2) == "1" else "nd"}@{m.group(3)}')
    return cells


def _run(body, pattern, want=1, at=0):
    """Question starts found by one pattern, in ascending order, from `at`."""
    cuts = []
    for m in pattern.finditer(body, at):
        if int(m.group(1)) == want:
            cuts.append(m.start())
            want += 1
    return cuts


def _numbered(body):
    """Where questions 1, 2, 3 … start, taking only numerals that run in order.

    A scheme is full of stray numerals — years, percentages, table rows — and
    the ascending guard is what keeps them out: a "3." inside question 2's data
    table is ignored because 3 is not the number being looked for yet.

    Two patterns, because a paper is not consistent with itself. Six schemes
    point their question numbers ("1. The UN Sustainable Development Goal"),
    four do not ("1 The adapted infographic displays"), and 2021 Higher points
    one to nine and then prints ten bare. Whichever pattern gets further on the
    whole body wins — a bare numeral is far too common to trust when the
    pointed form is available — and the tail is then extended by either, which
    is what recovers a paper that changes its mind at question ten.
    """
    cuts = max((_run(body, p) for p in (QUESTION, QUESTION_BARE)), key=len)
    while True:
        at, want = (cuts[-1] + 1 if cuts else 0), len(cuts) + 1
        nxt = [c[0] for c in (_run(body, p, want, at) for p in (QUESTION, QUESTION_BARE)) if c]
        if not nxt:
            return cuts
        cuts.append(min(nxt))


def section_a_segments(body):
    """Section A's parts, each with the tariff that actually belongs to it.

    Section B prints a part's marks beside the part. Section A prints a
    question's marks beside the QUESTION NUMBER — one column entry for a
    12-mark question split "1st @ 8 / 2nd @ 4" across its two parts — so in the
    flattened text both cells land ahead of "(i)" and a part-first split gives
    every part in the question either all the cells or none. Splitting on the
    question first, then handing part i the question's i-th cell, is what makes
    Section A readable at all: 2024 Ordinary went from 6 parts to 20.

    A part that prints its own cell keeps it; the borrowed one is a fallback.
    """
    segs = []
    cuts = _numbered(body)
    for n, (qa, qb) in enumerate(zip(cuts, cuts[1:] + [len(body)]), 1):
        q = body[qa:qb]
        inner = [m.start() for m in PART.finditer(q)]
        if not inner:
            segs.append((qa, qb, None, n))
            continue
        head = read_cells(q[:inner[0]])
        bounds = inner + [len(q)]
        for i, (a, b) in enumerate(zip(bounds, bounds[1:])):
            segs.append((qa + a, qa + b, head[i:i + 1] if i < len(head) else None, n))
    return segs


def parts(year, level, section='B'):
    """Every part of one section, with its tariff and its response block.

    Section A is worth a quarter of the written paper and is built the same way
    as Section B — a tariff over a list of named responses — despite reading, on
    a first skim, like chart lookups. Only some of its parts need the figure at
    all: "Outline one advantage of a balance of payments surplus" is answered
    by five named responses and no chart.
    """
    T = tidy(load(year, level))
    headings = bold_runs(year, level)
    # One boundary for both sections: Section A's response table is headed
    # "Q Possible responses Marks", and Section B begins at the first question
    # numbered 11 or higher after it. Section B used to begin at the first such
    # heading that repeated the caption, which on 2021 Higher is question 12 —
    # question 11 was not in the extractor's output at all, and so could not be
    # carded. Anchoring both on the same point is what stops a paper from
    # having a section neither half can see.
    hdr = re.search(r'Possible [Rr]esponses', T)
    at = re.search(r'Question 1[1-6]\b', T[hdr.end():] if hdr else T)
    if not at:
        return []
    boundary = (hdr.end() if hdr else 0) + at.start()
    if section == 'A':
        if not hdr:
            return []
        body, base = T[hdr.start():boundary], hdr.start()
    else:
        body, base = T[boundary:], boundary

    segs = section_a_segments(body) if section == 'A' else [
        (a, b, None, None) for a, b in zip(*(lambda c: (c, c[1:]))(
            [m.start() for m in PART.finditer(body)] + [len(body)]))]
    out = []
    for a, b, borrowed, qno in segs:
        seg = body[a:b]
        cells = read_cells(seg) or borrowed or []
        if not cells:
            continue
        # The question is what sits between the part numeral and the first cell;
        # the responses are what follows it.
        first = CELL.search(seg)
        if first:
            head, tail = tidy(seg[:first.start()]), seg[first.end():]
        else:
            # A part whose tariff was printed beside its question number, so the
            # segment itself holds no cell to split on. The responses begin at
            # the first bullet, or failing that at the first bold heading.
            cut = seg.find('•')
            if cut < 0:
                hits = [i for i in (seg.find(h) for h in headings) if i > 0]
                cut = min(hits) if hits else -1
            if cut < 0:
                continue
            head, tail = tidy(seg[:cut]), seg[cut:]
        opts = responses(tail, headings)
        # The headings of THIS part, in the order the examiner printed them.
        # This is what an author passes to heads(); splitting the text here as
        # well was tried and abandoned — bold is used mid-sentence too, and three
        # layouts across ten papers meant every heuristic broke one of them.
        # Reporting the anchors and letting heads() do the cut keeps the guard
        # that refuses a heading found out of order.
        flat = defurnish(tail)
        seen = sorted({h: flat.find(h) for h in headings if flat.find(h) >= 0}.items(),
                      key=lambda kv: kv[1])
        anchors, last = [], -1
        for h, at in seen:
            if at > last:
                anchors.append(h)
                last = at + len(h)
        # The menu tariff is not always the FIRST cell: a part often prints its
        # total first — ⟨12⟩ ⟨2 @ 6⟩ — and reading only cells[0] reported a paper
        # full of menus as having none.
        # The options, cut at the anchors by the same guarded splitter the
        # hand-authored cards use — so a heading found out of order is refused
        # here exactly as it would be there.
        # Whichever of the two splits finds more responses. Cutting at the bold
        # anchors was the rule, and on a bulleted Ordinary scheme it loses
        # responses: bold runs under fifteen characters are not taken as anchors
        # at all, so "Clean energy", "Tourism" and "Raw Materials" are invisible
        # and the last anchor's block holds three responses a student would then
        # never be shown. Cutting on bullets loses responses the other way, on a
        # Higher scheme that bullets one aside inside a headed list. Neither rule
        # is right for both, and the one that finds more is right for each.
        if len(anchors) >= 2:
            try:
                by_anchor = [as_option(h) for h in heads(tail, anchors)]
            except ValueError:
                by_anchor = []
            if len(by_anchor) > len(opts):
                opts = by_anchor
        menu = next((m for m in (MENU.match(c.replace(' ', '')) for c in cells) if m), None)
        # "1st @ 8" followed by "2nd @ 4" is a menu of two on a descending
        # tariff, which reads as claim=1 if each cell is taken on its own.
        steps = [int(m.group(2)) for c in cells
                 for m in [ORDINAL.match(c.replace(' ', ''))] if m]
        if len(steps) >= 2:
            claim, per, menu_steps = len(steps), steps[0], steps
        elif len(steps) == 1 and not menu:
            # A part carrying one ordinal cell — Section A splits a question's 12
            # marks across its parts, so "1st @ 8" beside part (i) is that part's
            # whole tariff for one response, not a step in a list.
            claim, per, menu_steps = 1, steps[0], None
        elif menu:
            claim, per, menu_steps = int(menu.group(1)), int(menu.group(2)), None
        else:
            claim = per = menu_steps = None
        out.append({
            'at': base + a,
            'q': qno,
            'cells': cells,
            'question': defurnish(head)[:300],
            'claim': claim,
            'per': per,
            'steps': menu_steps,
            'options': opts,
            'anchors': anchors,
        })
    return out


def main():
    year, level = int(sys.argv[1]), sys.argv[2]
    found = parts(year, level)
    menus = [p for p in found if p['claim'] and len(p['options']) >= p['claim']]
    if '--json' in sys.argv:
        print(json.dumps(found, ensure_ascii=False, indent=1))
        return
    rich = [p for p in found if len(p['anchors']) >= 2]
    print(f'# {year} {level}: {len(found)} parts with a tariff, '
          f'{len(rich)} with a listed set of responses\n')
    for p in found:
        tar = '/'.join(p['cells'])[:18]
        claim = f"claim {p['claim']}@{p['per']}" if p['claim'] else ''
        if p['steps']:
            claim = 'steps ' + '+'.join(map(str, p['steps']))
        print(f"  {p['at']:>7}  {tar:<19}{claim:<14}{p['question'][:105]}")
        for h in p['anchors']:
            print(f"              '{h}',")


if __name__ == '__main__':
    main()
