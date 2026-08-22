#!/usr/bin/env python3
"""Every part of a paper that has responses to card and no card citing it.

    python3 scripts/markbank/authoring/econ_todo.py 2025 higher B
    python3 scripts/markbank/authoring/econ_todo.py 2025 higher B --wide

Coverage is measured against the CITATION, not the card id: a part is carded if
some card cites its question and its part path, or a deeper path of it. That is
what makes the count trustworthy, because the citation is the thing the paper
itself can confirm — see econ_refcheck.py.

Prints the reference the QUESTION PAPER gives each part, so what is copied into
the script is what the paper says, not what the scheme's running order implies.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper
from econ_excluded import EXCLUDED  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
REF = re.compile(r'^(\d{4})\s+(HL|OL)(\s+Section A)?\s+Q(\d{1,2})((?:\([a-z]+\))*)')
# A part whose marks are for arithmetic or for drawing is not a menu.
NOT_A_MENU = re.compile(
    r'\b(calculate|complete the|show all your workings|show your workings|using the formula'
    r'|plot|draw the|illustrate|indicate (by|with|using)|tick)\b', re.I)


def key(ref):
    m = REF.match(ref or '')
    return m and (m.group(1), m.group(2), bool(m.group(3)), m.group(4), m.group(5))


def main():
    year, level, section = int(sys.argv[1]), sys.argv[2], sys.argv[3].upper()
    # econ_parts tests `level == 'higher'`, so an 'hl' passed straight through
    # is not higher and not ordinary — it silently fell through to the Ordinary
    # scheme, and this tool reported the same gaps for both levels.
    level = {'hl': 'higher', 'ol': 'ordinary'}.get(level, level)
    wide = '--wide' in sys.argv
    cards = json.load(open(os.path.join(ROOT, 'scripts/markbank/authored/economics.json')))
    carded = {k for k in (key(c['questionRef']) for c in cards) if k}

    P = Paper(year, level, section)
    n = 0
    skipped = []
    for p in P.parts:
        if len(p['options']) < 2:
            continue
        ref = P.cite(p)
        k = key(ref)
        if k and any(c[:4] == k[:4] and (c[4] == k[4] or c[4].startswith(k[4])
                                         or k[4].startswith(c[4])) for c in carded):
            continue
        # A part recorded in econ_excluded is a decision, not a gap. Listing it
        # argues for work already considered and declined, and invites carding a
        # part the deck deliberately left alone.
        if ref in EXCLUDED:
            skipped.append((ref, EXCLUDED[ref]))
            continue
        n += 1
        tar = ('+'.join(map(str, p['steps'])) if p['steps'] else
               f"{p['claim']}@{p['per']}" if p['claim'] else '/'.join(p['cells'])[:12])
        flag = '  [not a menu?]' if NOT_A_MENU.search(p['question']) else ''
        print(f"\n{ref or '(unplaced)'}  [{tar}]  {len(p['options'])} options{flag}")
        # The part PATH is reconstructed from markers in an answer booklet and is
        # a suggestion, not a verdict — so a part can be reported uncarded when a
        # card on the same question already covers it under a path one roman
        # numeral away. Show what is already carded on this question and let a
        # person decide; econ_all.py refuses the duplicate id either way.
        if k:
            near = [c for c in cards
                    if (kk := key(c['questionRef'])) and kk[:4] == k[:4] and kk[4] != k[4]]
            for c in near:
                print(f"    already on this question: {c['questionRef']} — "
                      f"{c['questionText'][:74]}")
        print(f"    Q: {p['question'][:150]}")
        for o in p['options']:
            print(f"     · {o[:220 if wide else 110]}")
    for ref, why in skipped:
        print(f'  left alone: {ref} — {why}')
    print(f'\n{n} uncarded part(s) with listed responses in {year} {level} '
          f'Section {section}' + (f'; {len(skipped)} deliberately left alone'
                                  if skipped else ''))


if __name__ == '__main__':
    main()
