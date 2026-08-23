#!/usr/bin/env python3
"""Authoring for Mathematics.

A card is one part of one paper:

  question   the paper's own wording, read span-aware so exponents survive
             (mathtext.clean_like) -- "4x^3 - 12x^2", not "4x3 - 12x2"
  rows       the Marking Notes: the numbered steps where the scheme gives them,
             otherwise its Low/Mid/High Partial Credit descriptors
  tariff     the partial-credit ladder, "Scale 15D (0, 4, 7, 10, 15)"

The ladder maps exactly onto perOptionSteps, which is what the first n options
claimed are worth: the increments of (0, 4, 7, 10, 15) are 4, 3, 3, 5, so one
step earns 4, two earn 7, three earn 10 and all four earn 15. Nothing is
derived -- every number is printed on the page.

The model solution is NOT text. Extraction scrambles it, so it belongs on the
card as a cropped image; see maths_figures.py.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mathtext                                              # noqa: E402
import maths_scheme                                          # noqa: E402
import paper as PP                                           # noqa: E402
from markbank_authoring import anyN, make_audit, make_card, make_emit  # noqa: E402

SUBJECT = 'maths'
_card = make_card(SUBJECT, default_section='B')
MAX_OPTIONS_SHOWN = 14
audit = make_audit(MAX_OPTIONS_SHOWN)
emit = make_emit(audit)
COMPONENT = {1: '100', 2: '200'}

# The running header runs on into a part's text where the question ends near
# the foot of a page: "... (2x+ 5√x-7 ) Leaving Certificate 2025 5 Mathematics,
# Paper 1". It is not part of the question and looks like a mistake on a card.
FURNITURE_TAIL = re.compile(
    r'\s*(Leaving Certificate\s+\d{4}|Mathematics,?\s*Paper|Page\s+\d+\s+of)'
    r'[\s\S]*$', re.I)

CONTENT_FREE = re.compile(r'^(work of merit|any valid|as above|see above|'
                          r'accept any|other relevant)\W*$', re.I)


class Refused(Exception):
    pass


def _squash(t):
    return re.sub(r'[^a-z0-9]+', '', (t or '').lower())


class Author:
    LEVELS = {'hl': 'higher', 'ol': 'ordinary'}

    def __init__(self, year, level):
        self.year, self.level = year, level
        self.deck_level = self.LEVELS[level]
        self.S = maths_scheme.Scheme(year, level)
        self.P = {n: PP.Paper(SUBJECT, year, level, component=c)
                  for n, c in COMPONENT.items()}
        self.cards = []
        self._used = set()

    def question(self, key):
        """The paper's wording for this unit.

        A unit may be marked at a coarser grain than the paper sets it -- the
        scheme prices Q2(b) once where the paper asks (b)(i), (b)(ii) and
        (b)(iii) -- so where the exact part is not in the paper, the parts
        underneath it are joined. That is still the paper's own words.
        """
        paper, q, letter, roman = key[0], key[1], key[2], key[3]
        P = self.P[paper]
        exact = [k for k in P.parts
                 if k[0] == q and k[1] == letter and k[2] == roman]
        if not exact and roman is None:
            exact = [k for k in P.parts if k[0] == q and k[1] == letter]
        if not exact:
            return ''
        exact.sort(key=lambda k: (k[1] or '', k[2] or ''))
        joined = ' '.join((P.text(*k) or '').strip() for k in exact)
        return mathtext.clean_like(P.files, joined)

    def ref(self, key):
        paper, q, letter, roman = key[0], key[1], key[2], key[3]
        tail = f'Q{q}'
        if letter:
            tail += f'({letter})'
        if roman:
            tail += f'({roman})'
        return f'{self.year} {self.level.upper()} Paper {paper} {tail}'

    def card(self, key, *, cid, topic, concept, notes='', stem='', figure_key=''):
        if cid in self._used:
            raise Refused(f'{cid}: already emitted')
        qtext = FURNITURE_TAIL.sub('', self.question(key)).strip(' .;,')
        if len(_squash(qtext)) < 15:
            raise Refused(f'{self.ref(key)}: no question text in the paper')
        total, ladder = self.S.tariff(key)
        if not total or not ladder or len(ladder) < 2:
            raise Refused(f'{self.ref(key)}: the scheme prints no ladder for this part')
        rows = [(lab, txt) for lab, txt in self.S.answer_rows(key)
                if txt and not CONTENT_FREE.match(txt) and len(_squash(txt)) > 6]
        if not rows:
            raise Refused(f'{self.ref(key)}: the marking notes state nothing liftable')
        if len(rows) > MAX_OPTIONS_SHOWN:
            raise Refused(f'{self.ref(key)}: {len(rows)} rows, past the '
                          f'{MAX_OPTIONS_SHOWN} a row may show')
        # The ladder's rungs are cumulative; perOptionSteps wants the increments.
        rungs = [v for v in ladder if v]
        steps = [rungs[0]] + [b - a for a, b in zip(rungs, rungs[1:])]
        if sum(steps) != total or any(s < 0 for s in steps):
            raise Refused(f'{self.ref(key)}: ladder {ladder} does not make {total}')
        claim = min(len(rows), len(steps))
        steps = steps[:claim]
        if sum(steps) != total:
            # Fewer marking points than rungs: give the last row the remainder,
            # which is what the scale does -- the top rung is full credit.
            steps[-1] += total - sum(steps)
        # The option is the scheme's own text and nothing else. Joining the
        # rung's heading to it -- "Low Partial Credit — Finds one relevant
        # probability" -- is a string the scheme never printed, and the
        # provenance gate is right to refuse it. The headings go in the note,
        # in order, so a student still knows which rung is which.
        options = [txt for _, txt in rows]
        rung_note = ' Marked in order: ' + '; '.join(lab for lab, _ in rows) + '.'
        note = ('The scheme marks this on a sliding scale: '
                + ', '.join(f'{n} for {v}' for n, v in
                            zip(('nothing', 'one part', 'two parts', 'three parts',
                                 'four parts', 'five parts'), ladder)) + '.')
        row = anyN(f'{cid}-r1', options[0], total, claim, steps[0], options,
                   note + rung_note,
                   steps=steps if len(set(steps)) > 1 else None)
        self.cards.append(_card(
            cid, self.year, self.deck_level, topic, concept, self.ref(key), qtext,
            f'Scale ({", ".join(str(v) for v in ladder)})', total, [row], notes,
            stem=stem, tariff_kind='fixed', figure_key=figure_key))
        self._used.add(cid)
        return self.cards[-1]

    def emit(self):
        emit(self.cards)


if __name__ == '__main__':
    A = Author(int(sys.argv[1]), sys.argv[2])
    ok = bad = 0
    for key in A.S.parts():
        try:
            c = A.card(key, cid=f'probe-{key}', topic='t', concept='c')
            ok += 1
            if ok <= 4:
                g = c['rows'][0]['group']
                print(f'{c["questionRef"]:<28} {c["totalMarks"]:>3}m  '
                      f'{g["claimMax"]}x steps={g.get("perOptionSteps")}')
                print(f'    Q: {c["questionText"][:78]}')
                for o in g['options'][:3]:
                    print(f'    - {o[:74]}')
        except Refused as e:
            bad += 1
            if bad <= 4:
                print(f'  REFUSED {str(e)[:88]}')
    print(f'\n{ok} cardable, {bad} refused of {len(A.S.parts())}')
