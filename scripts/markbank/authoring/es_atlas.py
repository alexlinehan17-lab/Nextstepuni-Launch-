#!/usr/bin/env python3
"""Spanish cards in the Topic Atlas: every card's own printed question.

    python3 scripts/markbank/authoring/es_atlas.py            # print the table
    python3 scripts/markbank/authoring/es_atlas.py --write    # spanish-atlas.json

The Atlas holds a Spanish paper as the questions its answer map anchors
(scripts/paper-trail/answers/<year>/<fileid>.json): each anchor records WHERE
on the paper its question begins (`pP`, the page; `pY`, the height) and the
tags file (scripts/paper-trail/topic-tags/tags/spanish.json) files it under
its topics. The Higher numbering is the Atlas's own running order, not the
paper's — "n 6" is Section B Q1 in one year and Section A Q1(b) in another —
so a card cannot be joined to it on the printed address alone.

What both print is the PLACE. A card's ask is printed at a page and height
(es_paper.Row.y); the Atlas question it belongs to is the last anchor that
begins at or above it. Two checks keep the geometry honest, because a missing
anchor would otherwise hand a card to the question printed before it:

  * the anchor's label names a section ("Section B", "Sec A", "Reading") and
    that section must be the card's;
  * where the label names a question number ("Section B · Q4", "Reading Q2")
    the card's question number must be that number.

A card that fails either has no Atlas question of its own, and is reported,
never filed under its neighbour.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

OUT = os.path.join(HERE, 'spanish-atlas.json')
ANSWERS = os.path.join(ROOT, 'scripts', 'paper-trail', 'answers')
TAGS = os.path.join(ROOT, 'scripts', 'paper-trail', 'topic-tags', 'tags', 'spanish.json')

LABEL_SECTION = re.compile(r'\bSec(?:tion)?\s*([ABC])\b', re.I)
LABEL_Q = re.compile(r'\bQ\s*(\d)\b')


def anchors(year, fileid):
    path = os.path.join(ANSWERS, str(year), f'{fileid}.json')
    if not os.path.exists(path):
        return []
    with open(path, encoding='utf-8') as fh:
        data = json.load(fh)
    out = []
    for q in data['q']:
        if q.get('pP') is None or not q.get('pY'):
            continue
        out.append({'n': q['n'], 'page': q['pP'], 'y': q['pY'][0],
                    'label': q.get('label') or ''})
    return sorted(out, key=lambda a: (a['page'], a['y']))


def tags_for(year, level, fileid):
    with open(TAGS, encoding='utf-8') as fh:
        papers = json.load(fh)
    for p in papers:
        if (p['year'] == year and p['level'] == level and p['lang'] == 'ev'
                and p['fileid'] == fileid):
            return {q['n']: q for q in p['q']}
    return {}


def place(found, page, y, section, q, letter=None):
    """The Atlas question a card printed at (page, y) belongs to, or a reason."""
    # A tolerance of a hundredth of the page: the anchor and the ask are
    # read off the same line by two different readers.
    above = [a for a in found if (a['page'], a['y']) <= (page, y + 0.01)]
    # Where the labels name questions, the anchor that names the card's own
    # section and question is the answer, wherever the card's part falls: 2022
    # Higher anchors its journalistic Q1 at the top of page 8 and Q2 at the top
    # of page 9, and Q1(b)-(e) are printed on page 9 too.
    own = [a for a in above if _label_q(a['label']) == q
           and _label_section(a['label']) in (None, section[0])
           and _label_route(a['label']) in (None, section if section in ('A1a', 'A1b', 'A2') else None)]
    if q is not None and own:
        return own[-1], None
    if not above:
        return None, 'no anchor at or above the ask'
    last = max((a['page'], a['y']) for a in above)
    tied = [a for a in above if (a['page'], a['y']) == last]
    best = tied[-1]
    if len(tied) > 1:
        # Some answer maps anchor a question at its PAGE only — 2022 Higher
        # sets Q2, Q3 and Q4 of the literature route all at page 5, height 0 —
        # and then the position cannot choose between them. The label can:
        # the anchor that names the card's own question number.
        named = [a for a in tied if _label_q(a['label']) == q]
        if section == 'A2' and letter and len(named) != 1:
            # 2018 Higher anchors Question 2's two texts at one height of page
            # 6, "Section A · 2(a) Short Comprehension (Circo …)" and "… 2(b)
            # …" (2017: "Section A · Q2(a) Talgo", "… Q2(b) Drones"): the label
            # that names the card's own text is its question.
            named = [a for a in tied if re.search(rf'(?<!\d)2\s*\(\s*{letter}\s*\)', a['label'])]
        if len(named) != 1:
            return None, (f'{len(tied)} anchors begin at page {last[0]} height '
                          f'{last[1]} and the labels do not single out Q{q}')
        best = named[0]
    label = best['label']
    m = LABEL_SECTION.search(label)
    want = section[0]
    if m and m.group(1).upper() != want:
        return None, f'anchor {best["n"]} "{label}" is Section {m.group(1)}'
    if not m and re.match(r'^Reading\b', label) and want != 'A':
        return None, f'anchor {best["n"]} "{label}" is the reading section'
    # A question number in the label must be the card's — but only where the
    # label numbers questions of the card's own section: "Section A · Q1(a) ·
    # Q5" names the literature route's Q5, while "Section B · Q4" names B's.
    route = _label_route(label)
    if section in ('A1a', 'A1b', 'A2') and route is not None and route != section:
        return None, f'anchor {best["n"]} "{label}" is {route}, the card is {section}'
    named = _label_q(label)
    if named is not None and q is not None and named != q:
        return None, f'anchor {best["n"]} "{label}" is Q{named}, the card is Q{q}'
    return best, None


def _label_route(label):
    """Which of Higher Section A's three tasks an anchor's label names, if any:
    the literature route "1(a)"/"Lit", the journalistic "1(b)"/"Journ", or
    Question 2's two short items ("Q2(a)", "Q2 (Bee / …)", "2 Short …")."""
    if re.search(r'1\s*\(\s*a\s*\)|\bLit', label):
        return 'A1a'
    if re.search(r'1\s*\(\s*b\s*\)|\bJourn|\bperiod[ií]stic', label, re.I):
        return 'A1b'
    if re.search(r'\bQ\s*2\b|·\s*2\s', label) and _label_section(label) in (None, 'A'):
        return 'A2'
    return None


def _label_section(label):
    m = LABEL_SECTION.search(label)
    if m:
        return m.group(1).upper()
    return 'A' if re.match(r'^Reading\b', label) else None


def _label_q(label):
    """The question number an anchor's label names, past any "Q1(a)" route."""
    m = LABEL_Q.search(re.sub(r'Q\s*\d\s*\([ab]\)', '', label))
    return int(m.group(1)) if m else None


def _writing_n(level, section, q, letter):
    """The Atlas number of a written-production card, or None (filed by place).

    Ordinary Section B (letter; note or diary) and Higher B Q5 and C Q2 are
    Atlas questions of their own, numbered as printed. Higher C Q1 is the
    answer map's "Section C · Written production" question, found by place.
    """
    if level == 'ol' and section == 'B':
        return 'B1' if q == 1 else f'B{q}{(letter or "").upper()}'
    if level == 'hl' and (section, q) == ('B', 5):
        return 'B5'
    if level == 'hl' and (section, q) == ('C', 2):
        return 'C2'
    return None


# Printed questions the answer map never anchored, given an Atlas question of
# their own numbered by their printed address (build-spanish-exam-topic-
# crosswalk.mjs adds them): 2020 Higher journalistic Q4.
EXTRA_N = {(2020, 'hl', 'A1b', 4): 'A1b4', (2025, 'hl', 'A1b', 4): 'A1b4',
           (2024, 'hl', 'A1b', 4): 'A1b4',
           (2022, 'hl', 'A1b', 4): 'A1b4', (2022, 'hl', 'A2', None): 'A2',
           (2021, 'hl', 'A1b', 4): 'A1b4', (2019, 'hl', 'A1b', 4): 'A1b4',
           (2018, 'hl', 'A1b', 4): 'A1b4', (2017, 'hl', 'A1b', 4): 'A1b4',
           (2016, 'hl', 'A1b', 4): 'A1b4',
           (2015, 'hl', 'A1b', 4): 'A1b4',
           (2014, 'hl', 'A1b', 4): 'A1b4',
           (2013, 'hl', 'A1b', 4): 'A1b4',
           # 2016's English map anchors no Section B question; the generator
           # restores one Section B card from the Irish edition ("B").
           **{(2016, 'hl', 'B', q): 'B' for q in (1, 2, 3, 4)}}


FILEID = {('hl', 'written'): 'LC012ALP000EV.pdf', ('ol', 'written'): 'LC012GLP000EV.pdf',
          ('hl', 'aural'): 'LC012ALPA00EV.pdf', ('ol', 'aural'): 'LC012GLPA00EV.pdf'}
REF = re.compile(r'^(\d{4}) (HL|OL) Section (\w+) Q(\d*)((?:\([a-z]+\))*)')


def parse_ref(ref):
    m = REF.match(ref)
    year, level, section, q, parts = m.groups()
    letters = re.findall(r'\(([a-z]+)\)', parts)
    letter = letters[0] if letters else None
    roman = letters[1] if len(letters) > 1 else None
    return int(year), level.lower(), section, int(q) if q else None, letter, roman


def resolve(cards):
    """{card id: {fileid, n, label}} and [(card id, reason)] for the rest."""
    from es_paper import EsPaper
    papers, out, refused = {}, {}, []
    for card in cards:
        year, level, section, q, letter, roman = parse_ref(card['questionRef'])
        key = (year, level)
        if key not in papers:
            papers[key] = EsPaper(year, level)
        P = papers[key]
        if section == 'L':
            kind = 'aural'
        else:
            kind = 'written'
        fileid = FILEID[(level, kind)]
        found = anchors(year, fileid)
        tags = tags_for(year, 'higher' if level == 'hl' else 'ordinary', fileid)
        written_n = (_writing_n(level, section, q, letter)
                     or EXTRA_N.get((year, level, section, q)))
        if kind == 'aural':
            hit = next((a for a in found if a['n'] == str(q)), None)
            reason = None if hit else f'no anchor n={q}'
        elif written_n:
            # Written production is numbered in the Atlas by its PRINTED
            # address ("B1", "B2A"; Higher "B5", "C2"), not by the answer
            # map's running order, and those cards carry no answer-map anchor:
            # the card is filed under the Atlas question of that number.
            hit = {'n': written_n, 'label': f'Section {section} · Question {q}'
                                             f'{f"({letter})" if letter else ""}'}
            reason = None
        else:
            leaves = P.leaves()
            hits = [v for k, v in sorted(leaves.items(), key=lambda kv: str(kv[0]))
                    if k[0] == section and k[1] == q
                    and (letter is None or k[2] == letter)
                    and (roman is None or k[3] == roman)]
            block = next((h[2] for h in hits if h[2] is not None), None)
            if block is None:
                refused.append((card['id'], 'the census holds no printed block for it'))
                continue
            row = P.rows[block.row]
            hit, reason = place(found, block.page + 1, row.y, section, q, letter)
        if hit is None:
            refused.append((card['id'], reason))
            continue
        tag = tags.get(hit['n'])
        if tag is None:
            refused.append((card['id'], f'anchor n={hit["n"]} is not tagged in the Atlas'))
            continue
        topics = [tag.get('primary'), tag.get('secondary')]
        out[card['id']] = {'fileid': fileid, 'n': hit['n'], 'label': hit['label'],
                           'atlasTopics': [t for t in topics if t],
                           'cardTopicInAtlas': card['topicId'] in topics}
    return out, refused


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--cards', default=os.path.join(ROOT, 'scripts', 'markbank',
                                                    'authored', 'spanish.json'))
    args = ap.parse_args()
    with open(args.cards, encoding='utf-8') as fh:
        cards = json.load(fh)
    out, refused = resolve(cards)
    off = [cid for cid, v in out.items() if not v['cardTopicInAtlas']]
    print(f'{len(out)}/{len(cards)} cards resolved to an Atlas question; '
          f'{len(refused)} not; {len(off)} whose Mark Bank topic is not among '
          f'its Atlas question\'s tags')
    for cid, reason in refused:
        print(f'   NO ATLAS  {cid}: {reason}')
    for cid in off:
        v = out[cid]
        print(f'   TOPIC     {cid}: n={v["n"]} {v["atlasTopics"]}')
    if args.write:
        data = {
            '_comment': ('GENERATED by scripts/markbank/authoring/es_atlas.py --write. '
                         'Every Spanish card and the Topic Atlas question it is filed '
                         'under (test/spanishCardAtlas.test.ts). "gaps": cards whose '
                         'paper has no Atlas question of their own yet; "topicResidue": '
                         'cards whose Atlas question is tagged under a topic other than '
                         'the card\'s. Both are 2021-2025 Atlas faults that predate this '
                         'map and may only shrink.'),
            'cards': {cid: {'fileid': v['fileid'], 'n': v['n']}
                      for cid, v in sorted(out.items())},
            'gaps': {cid: reason for cid, reason in sorted(refused)},
            'topicResidue': sorted(off),
        }
        with open(OUT, 'w', encoding='utf-8') as fh:
            json.dump(data, fh, ensure_ascii=False, indent=1)
            fh.write('\n')
        print(f'wrote {OUT}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
