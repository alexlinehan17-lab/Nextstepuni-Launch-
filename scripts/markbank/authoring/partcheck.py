#!/usr/bin/env python3
"""Coverage measured on the question a card asks, not the reference it cites.

    python3 scripts/markbank/authoring/partcheck.py                 # every subject
    python3 scripts/markbank/authoring/partcheck.py business        # one
    python3 scripts/markbank/authoring/partcheck.py business --list # and the open parts

Why this exists
---------------
coverage.py compares a card's citation against the paper's part path, counting
in the paper's own absolute numbering. Three subjects number their questions per
section instead — Business cites "2023 OL Section 2 Q4(A)", Home Economics cites
"2023 HL Section C E2 Q1(a)(i)", Economics restarts at Q11 after a Section A
ending at Q8 — so their Question 4 is not the paper's Question 4 and the
comparison fails on nearly every card. Business read 56% covered and Home
Economics 44% while their own subject tooling reported them all but closed.

The question text does not have this problem. Every card carries the wording the
paper prints, so comparing that against the part's own text settles coverage
without knowing anything about how a subject numbers its sections. It is also
the stronger check: a citation can be wrong — nineteen shipped cards cited the
wrong question and a gate had to be written to find them — while the text a
student reads is the card.

A part counts as covered when some card of the same year and level asks it. The
comparison is on letters and digits only, so punctuation, ligatures and the
paper's own spacing cannot separate two copies of one question, and it matches
on a leading run rather than the whole string, because a card may trim a part
mark or a run-on sentence off the end of what the parser returned.

Cards whose text was typed rather than lifted — the deck predates the rule — can
miss, so the reference test is kept as well and a part is covered if EITHER
finds it. The two together are what makes the number worth acting on.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from align import align_ordered                             # noqa: E402
import coverage as C                                        # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
AUTHORED = os.path.join(ROOT, 'scripts/markbank/authored')

# Below this a question is too short to identify: "Starch", "Protein", "Lipid"
# are three different parts of one Biology question and share no useful prefix.
FLOOR = 40
LEAD = 60

# A subject whose parts this tool cannot pair, and what to use instead. Economics
# is set as an answer booklet whose parts are reconstructed from the markers
# printed in it, which is what econ_auto does and what align_ordered cannot: ask
# it for 2024 HL Q15(b)(iii) and it offers a mark cell reading "Valid
# information 8". Any figure printed here for Economics would be measuring the
# pairing, not the coverage.
DEFER = {'economics': 'econ_todo.py <year> <level> <section> — reports 0 uncarded '
                      'parts on all ten papers'}


def squash(text):
    return re.sub(r'[^a-z0-9]+', '', (text or '').lower())


def asked(subject):
    """Every question text a card asks, keyed by (year, level)."""
    out = {}
    for card in json.load(open(os.path.join(AUTHORED, f'{subject}.json'))):
        level = 'hl' if str(card.get('level', '')).lower().startswith('h') else 'ol'
        key = (int(card['year']), level)
        out.setdefault(key, []).append(squash(card.get('questionText')))
    return out


def covered_by_text(text, texts):
    a = squash(text)
    if len(a) < FLOOR:
        return False
    return any(a[:LEAD] in b or b[:LEAD] in a for b in texts if len(b) >= FLOOR)


def report(subject, show=False):
    if subject in DEFER:
        print(f'{subject:<22} not measured here — use {DEFER[subject]}')
        return 0, 0
    by_ref = C.covered(subject)
    by_text = asked(subject)
    total = open_ = ref_only = text_only = 0
    for year in range(2021, 2026):
        for level in ('hl', 'ol'):
            try:
                P, S, pairs, positional = align_ordered(subject, year, level)
            except Exception:
                continue
            texts = by_text.get((year, level), [])
            for skey, (pkey, _) in {**positional, **pairs}.items():
                if not S.points(*skey):
                    continue
                q, letter, roman = pkey
                total += 1
                hit_ref = False
                for letters, romans in by_ref.get((year, level, q), ()):
                    if not letters and not romans:
                        hit_ref = letter is None and roman is None
                    else:
                        hit_ref = ((letter is None or not letters or letter in letters)
                                   and (roman is None or not romans or roman in romans))
                    if hit_ref:
                        break
                hit_text = covered_by_text(P.text(*pkey), texts)
                if hit_ref and not hit_text:
                    ref_only += 1
                if hit_text and not hit_ref:
                    text_only += 1
                if hit_ref or hit_text:
                    continue
                open_ += 1
                if show:
                    print(f'-- {year} {level.upper()} {P.ref(pkey)}  scheme={skey}')
                    print(f'   Q: {(P.text(*pkey) or "(no paper text)")[:170]}')
                    for pt in S.points(*skey)[:4]:
                        print(f'   * {pt[:150]}')
    pct = 100 - (open_ * 100 // total) if total else 0
    print(f'{subject:<22} {total:>5} parts   {total - open_:>5} covered   {open_:>5} open   '
          f'{pct:>3}%   (reference only {ref_only}, text only {text_only})')
    return total, open_


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    show = '--list' in sys.argv
    targets = args or C.SUBJECTS
    t = o = 0
    for s in targets:
        a, b = report(s, show and len(targets) == 1)
        t += a
        o += b
    if len(targets) > 1:
        print(f'\n{"TOTAL":<22} {t:>5} parts   {t - o:>5} covered   {o:>5} open')
