#!/usr/bin/env python3
"""Reviewed specs for the Polish reading asks pl_all cannot read, one card each.

The rest of a sitting's reading cards come from pl_all.build(), which pairs the
paper's ask with the scheme's on their printed address. These are the asks it
refuses, read on the rendered page and set out by SELECTORS (pl_listen_lib):
every answer is a line of the scheme's .md cut at printed anchors, every price
the tariff the scheme prints for it, every question the census's reading of the
paper (plus, where the card needs them, the paper's own printed lines).

True/false verdicts are read from the TICK'S COLUMN on the rendered scheme page
(the .md keeps the tick and loses its column) and recorded with the page; the
verdict's word is cut from the table's own header row ("True False",
"Prawda Fałsz Marks").
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import pl_paper                                                  # noqa: E402
from pl_listen import scheme_lines                               # noqa: E402
from pl_listen_lib import S, J, T, TM, PL, W, one, menu, part, One  # noqa: E402,F401
from pl_listen_specs import build_rows                           # noqa: E402
from pl_topics import (topic_for, concept_for, answer_language,  # noqa: E402
                       language_note)
from pl_all import card_id, question_ref, source_material        # noqa: E402
from paper_census import key_label                              # noqa: E402

LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
KEY = re.compile(r'^A(\d{1,2})([a-l])(i{1,3}|iv|vi{0,3})?$')


class R:
    """One reading card: the census address, its rows, notes for the student
    (`rownote`, a callable of the documents or a string) and the reviewer's
    evidence (`note`)."""
    def __init__(self, key, rows, total=None, note=None, rownote=None, question=None,
                 extra_pages=()):
        self.key, self.rows, self.total, self.note = key, rows, total, note
        self.rownote, self.question = rownote, question
        # Paper pages the card needs beside its text's: a matching task's
        # pictures printed on a page of their own.
        self.extra_pages = extra_pages


def lifted(*sels):
    """A note quoting printed lines, for the student."""
    return lambda d: ' '.join(f'The scheme notes: “{s.text(d)}”.' for s in sels)


SPECS = {}

# ================================================================ 2026 HL ===
SPECS[(2026, 'hl')] = [
    # True/false, priced (1+1 m) on the head row. Rendered scheme p6: the
    # tick for (i) stands in the False column, for (ii) in the True column.
    R('A1ji', [one(S(187, after='True '), T(183, each=True))],
      rownote=lifted(S(185, raw=True), S(186, raw=True)),
      note='The tick stands in the False column (scheme p6, rendered).'),
    R('A1jii', [one(S(187, before=' False'), T(183, each=True))],
      rownote=lifted(S(185, raw=True), S(186, raw=True)),
      note='The tick stands in the True column (scheme p6, rendered).'),
    # "- pastor metodystów (2 m)" or "- pastor (1 m)": the shorter answer in
    # place of the full one, never beside it.
    R('A2aii', [one(S(201), T(201), [part(S(203), 0, T(203))])]),
]

# ================================================================ 2026 OL ===
SPECS[(2026, 'ol')] = [
    # "Podkreśl zdanie prawdziwe": the scheme prints the true sentence, by its
    # printed number, and prices the ask (4 marks).
    R('A1c', [one(S(105), T(106))]),
    # Multiple choice A-D: the scheme answers "C (2 marks)". The paper prints
    # the four options in the question itself.
    R('A2biii', [one(S(162), T(162))]),
    # A matching task: names 2-6 to portraits A-F (1. Agatka is the example).
    # The scheme sets its key as a table, numbers over letters ("1. 2. 3. 4.
    # 5. 6." / "E C F A B D", cells read by find_tables in that order) and
    # "2 marks" under each answer; each row is one name's letter, led by the
    # name as the paper prints it (p11). The portraits are on paper p11.
    R('A2c', [one(W(166, k - 1), T(167, k - 2), lead=PL(11, f'{k}. ')) for k in range(2, 7)],
      question=lambda d, q: '\n'.join([q] + [PL(11, f'{k}. ').text(d) for k in range(2, 7)]),
      extra_pages=(11,)),
]

# ================================================================ 2025 HL ===
SPECS[(2025, 'hl')] = [
    R('A2aii', [one(S(191), T(191), [part(S(193), 0, T(193))])]),
    # True/false, priced (2 x 1 m). Rendered scheme p7: (i) False, (ii) True.
    R('A2hi', [one(S(255, after='True '), T(251, each=True))],
      rownote=lifted(S(253, raw=True), S(254, raw=True)),
      note='The tick stands in the False column (scheme p7, rendered).'),
    R('A2hii', [one(S(255, before=' False'), T(251, each=True))],
      rownote=lifted(S(253, raw=True), S(254, raw=True)),
      note='The tick stands in the True column (scheme p7, rendered).'),
]

# ================================================================ 2025 OL ===
SPECS[(2025, 'ol')] = [
    # "Tick the three correct answers from the six boxes below": one card for
    # the printed question (CARD-STANDARD 10c), the scheme's three ticked boxes
    # as its rows at their printed 2 marks each. The six boxes are printed on
    # pages 5 and 6; each row names its box as the paper prints it.
    R('A1d', [one(S(113), T(113), lead=PL(5, 'A. ')),
              one(S(114), T(114), lead=PL(5, 'C. ')),
              one(S(115), T(115), lead=PL(6, 'F. '))],
      question=lambda d, q: '\n'.join(
          [re.sub(r'\s*✓\s*$', '', q)]
          + [PL(p, f'{x}. ').text(d) for p, x in ((5, 'A'), (5, 'B'), (5, 'C'),
                                                  (6, 'D'), (6, 'E'), (6, 'F'))])),
    # The answer is printed on the question's own row, before its price.
    R('A2bi', [one(S(148, after='ZHP? '), T(148))]),
    R('A2bii', [one(S(149, after='ZHP? '), T(149))]),
    # Rendered scheme p6: the (vi) tick stands in the Prawda column (x=406
    # under "Prawda" at x=392; "Fałsz" is at x=446). Priced in the Marks column.
    R('A2cvi', [one(S(152, before=' Fałsz'), TM(160))],
      note='The tick stands in the Prawda column (scheme p6, rendered).'),
]


def _marker_off(text):
    return re.sub(r'^\(\s*[a-l]\s*\)\s*', '', text)


# Question texts the census reads short or long, corrected with the paper's
# own lines (id -> f(documents, census question) -> question). Applied to the
# cards pl_all builds; the census itself is unchanged.
QFIX = {
    # The box of headings the task matches to parts 2-6, and its example, as
    # the paper prints them under the task (p9).
    'pl-2026-ol-a-2-a': lambda d, q: '\n'.join(
        [q, PL(9, 'W świecie bez internetu').text(d), PL(9, 'Pierwsze dobranocki').text(d),
         PL(9, 'Przykład:').text(d)]),
    # The text layer repeats the NEXT row's label beside this one ("miejsce
    # pierwszej styczności", p4 x=87), and the census appended it.
    'pl-2026-hl-a-1-a-i': lambda d, q: q.split(' miejsce pierwszej styczności')[0],
    # "Podkreślone wyrazy zastąp synonimami ..." heads the part, and the paper
    # prints each answer line opening with the underlined word ("dobrych –",
    # p5); the census keeps neither once the sentence runs past 60 characters,
    # and without them the card does not say which word to replace.
    'pl-2026-hl-a-1-e-i': lambda d, q: ' '.join(
        [_marker_off(PL(5, '(e) Podkreślone').text(d)), q, PL(5, 'dobrych').text(d)]),
    'pl-2026-hl-a-1-e-ii': lambda d, q: ' '.join([q, PL(5, 'uratował').text(d)]),
}


TF = {'true', 'false', 'prawda', 'fałsz'}


def with_instruction(card, ask):
    """A true/false row's card carries the table's printed instruction
    ("Indicate whether the following statements are true or false. ..."): the
    census keeps it only when the statement is short, and a statement alone
    does not say what to do with it."""
    rows = card.get('rows') or []
    if len(rows) == 1 and rows[0]['verbatim'].strip().lower() in TF and ask is not None \
            and ask.stem and not card['questionText'].startswith(ask.stem[:40]):
        card['questionText'] = f'{ask.stem} {card["questionText"]}'
    return card


def fix_question(card, year, level, doc=None, ask=None):
    with_instruction(card, ask)
    fix = QFIX.get(card['id'])
    if not fix:
        return card
    if doc is None:
        doc = {'scheme': scheme_lines(year, level),
               'paper': [(l.page, l.text) for l in pl_paper.PlPaper(year, level).lines]}
    card['questionText'] = fix(doc, card['questionText'])
    return card


def cards(year, level):
    specs = SPECS.get((year, level), [])
    doc = {'scheme': scheme_lines(year, level)}
    P = pl_paper.PlPaper(year, level)
    doc['paper'] = [(l.page, l.text) for l in P.lines]
    asks = {a.key: a for a in P.all_asks()}
    out = []
    for spec in specs:
        m = KEY.match(spec.key)
        key = ('A', int(m.group(1)), m.group(2), m.group(3))
        ask = asks[key]
        question = ask.full_text
        if spec.question:
            question = spec.question(doc, question)
        language = answer_language(question)
        note = language_note(language)
        if spec.rownote:
            note = f'{note} {spec.rownote(doc) if callable(spec.rownote) else spec.rownote}'
        rows, total = build_rows(doc, spec, note)
        if spec.total is not None:
            tc, tp, tn = spec.total.read(doc)
            if tc * tp != total:
                raise ValueError(f'{year} {level} {spec.key}: rows add to {total}, printed {tn!r}')
        card = {
            'id': card_id(year, level, key),
            'subjectId': 'polish',
            'level': LEVEL_WORD[level],
            'year': year,
            'section': 'A',
            'topicId': topic_for(year, 'A'),
            'conceptId': concept_for(question),
            'questionRef': question_ref(year, level, key),
            'questionText': question,
            'tariffModel': {'kind': 'fixed'},
            'totalMarks': total,
            'rows': rows,
            'notes': (f'Read on the rendered scheme and paper (languages-q3 lane, 19 Nov 2026); '
                      f'the paper prints this ask on page {ask.page} of the question booklet.'
                      + (f' {spec.note}' if spec.note else '')),
        }
        lead = P.lead(key[1])
        if lead and len(lead) >= 12:
            card['stem'] = lead
        source = source_material(P, ask, language, level, year)
        if source:
            for p in spec.extra_pages:
                if p not in source['pages']:
                    source['pages'].append(p)
            card['sourceMaterial'] = source
        with_instruction(card, ask)
        out.append(card)
    return out
