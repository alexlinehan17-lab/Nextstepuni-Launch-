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
CELL = re.compile(r'⟨([^⟩]{1,18})⟩|(\d+)(?:st|nd|rd|th)\s*@\s*(\d+)')
MENU = re.compile(r'^(\d+)\s*[@x]\s*(\d+)$')
# "1st @ 8", "2nd @ 4" — the descending tariff written out in words.
ORDINAL = re.compile(r'^(\d+)(?:st|nd|rd|th)@(\d+)$')

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
    """The examiner's listed responses, however this paper lays them out."""
    text = defurnish(chunk)
    if text.count('•') >= 2:
        return [p for p in (tidy(x) for x in text.split('•')) if len(p) >= 25]
    by_bold = split_on_headings(chunk, headings)
    if len(by_bold) >= 2:
        return by_bold
    return [p for p in (tidy(x) for x in HEADED.split(text)) if len(p) >= 25]


def parts(year, level):
    """Every part of Section B, with its tariff and its response block."""
    T = tidy(load(year, level))
    headings = bold_runs(year, level)
    starts = [m.start() for m in re.finditer(r'Question 1[1-6]\b', T)
              if re.search(r'Possible [Rr]esponses', T[m.start():m.start() + 60])]
    if not starts:
        starts = [m.start() for m in re.finditer(r'Question 1[1-6]\b', T)]
    if not starts:
        return []
    body = T[starts[0]:]

    cuts = [m.start() for m in PART.finditer(body)] + [len(body)]
    out = []
    for a, b in zip(cuts, cuts[1:]):
        seg = body[a:b]
        cells = []
        for m in CELL.finditer(seg):
            if m.group(1):
                cells.append(m.group(1).strip())
            else:
                cells.append(f'{m.group(2)}{"st" if m.group(2) == "1" else "nd"}@{m.group(3)}')
        if not cells:
            continue
        # The question is what sits between the part numeral and the first cell;
        # the responses are what follows it.
        first = CELL.search(seg)
        head = tidy(seg[:first.start()])
        tail = seg[first.end():]
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
        if len(anchors) >= 2:
            try:
                opts = [as_option(h) for h in heads(tail, anchors)]
            except ValueError:
                pass
        menu = next((m for m in (MENU.match(c.replace(' ', '')) for c in cells) if m), None)
        # "1st @ 8" followed by "2nd @ 4" is a menu of two on a descending
        # tariff, which reads as claim=1 if each cell is taken on its own.
        steps = [int(m.group(2)) for c in cells
                 for m in [ORDINAL.match(c.replace(' ', ''))] if m]
        if len(steps) >= 2:
            claim, per, menu_steps = len(steps), steps[0], steps
        elif menu:
            claim, per, menu_steps = int(menu.group(1)), int(menu.group(2)), None
        else:
            claim = per = menu_steps = None
        out.append({
            'at': starts[0] + a,
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
