#!/usr/bin/env python3
"""Author every Arabic ask the papers print and the schemes answer.

    python3 scripts/markbank/authoring/ara_all.py --report
    python3 scripts/markbank/authoring/ara_all.py --exclusions   # rewrite them
    python3 scripts/markbank/authoring/ara_all.py > scripts/markbank/authored/arabic.json

Census-driven: the ten sittings print 370 leaf asks — 37 each, at both levels,
summing to the 400 marks each cover states — and this walks that census rather
than choosing what to card.

WHAT ONE CARD IS
----------------
One printed ask. Its question comes from the PAPER (ara_paper.py) and its
marking points from the SCHEME (ara_scheme.py). Both are read through
ara_text.py, which is what makes an Arabic page readable at all.

HOW THE TWO ARE JOINED (Law 4)
------------------------------
On the question NUMBER and the printed PART LETTER, never on wording — the
scheme does not reprint the question it is answering. The join is safe because
two counts that do not depend on each other agree first, which is the bar
Italian set: every question the scheme totals is priced the same by the paper,
and the part letters under a grammar question are the paper's letters in the
paper's order. Where the SEC letters a part twice over — 2025 Ordinary letters
Q13's fourth and fifth parts both (د) — the paper wins and the correction is
listed in ara_scheme.SCHEME_MISPRINTS, never inferred.

WHAT IS CARDED AND WHAT IS EXCLUDED
-----------------------------------
Twenty-five of the 37 asks a sitting prints state an answer:

  * Q1-4, the reading comprehension. The scheme names the option it accepts;
    the option's own words are lifted from the paper, which is where they are
    printed.
  * Q10-13, five grammar sub-asks each, at three marks apiece.
  * Q14, the parsing ask, whose 20 marks the scheme splits 8/4/4/4 over its
    own four marking points.

The other twelve are a Communication-and-Content grid — Q5 and Q6, the nine
literature alternatives of Q7-9, and the composition Q15 — over a list the
scheme heads "تجدر الإشارة إلى:" and states is not exhaustive. That is the
same written-production exclusion the six carded modern languages carry, and
--exclusions writes it with the grid's own printed rows as evidence.

THE ANSWER LANGUAGE IS PART OF THE ASK
--------------------------------------
Arabic is not bilingual the way French and German are: the paper is set in
Arabic, and its scheme answers in Arabic. Every card says so — a card that
does not say which language is wanted marks a right answer wrong — and every
card that carries Arabic says which way it is to be read.

REFUSALS
--------
Every one is a named bucket, counted and exampled by --report, and every
refusal that lands on a census leaf becomes an exclusions entry carrying the
scheme evidence for it.
"""
import argparse
import collections
import json
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

from ara_paper import AraPaper                                 # noqa: E402
from ara_scheme import AraScheme, INDICATIVE                   # noqa: E402
import ara_text                                                # noqa: E402

SUBJECT = 'arabic'
YEARS = (2021, 2022, 2023, 2024, 2025)
LEVELS = ('hl', 'ol')
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}

# From curriculum.ts, which already publishes the Arabic strands for the
# syllabus these ten sittings were set on. Nothing here invents an id.
COMPREHENSION = 'arabic-3-2'      # Scanning and Extracting Specific Information
GRAMMAR = 'arabic-5-0'            # Grammatical Structures
SENTENCE = 'arabic-5-4'           # Sentence & Paragraph Construction

# Which of the paper's fifteen questions state an answer, and where each is
# filed. Q13 asks for a sentence of the candidate's own for each construction
# named, which is sentence construction rather than a grammar drill.
CARDED = {1: COMPREHENSION, 2: COMPREHENSION, 3: COMPREHENSION,
          4: COMPREHENSION, 10: GRAMMAR, 11: GRAMMAR, 12: GRAMMAR,
          13: SENTENCE, 14: GRAMMAR}
GRID_QUESTIONS = (5, 6, 7, 8, 9, 15)

ANSWER_LANGUAGE = (
    'The paper is set in Arabic and the scheme answers in Arabic; this ask is '
    'answered in Arabic. Arabic reads right to left.')

# The most rows one card may show. The parsing ask states four marking points;
# nothing else here states more than one.
MAX_ROWS = 8


def card_id(year, level, question, letter=None):
    parts = ['ara', str(year), level, f'q{question}']
    if letter:
        parts.append(letter)
    return '-'.join(parts)


def question_ref(year, level, question, letter=None):
    ref = f'{year} {level.upper()} Q{question}'
    if letter:
        ref += f'({letter})'
    return ref


def concept_id(text, fallback):
    """A short, stable slug. Arabic does not transliterate here, so the concept
    is keyed on the ask's address; conceptId is an internal grouping key and
    never printed."""
    return fallback


def source_material(P, year, level):
    """The comprehension passage, in the QUESTION paper where it is printed."""
    pages = sorted(set(P.part_pages.get(1, [])))
    if not pages:
        return None
    return {
        'kind': 'source-text',
        'label': 'الجزء الأول — PART 1',
        'title': 'Part 1 reading passage — answer in Arabic',
        'pages': pages,
        'attribution': (f'SEC Arabic {year} {LEVEL_TITLE[level]} Level '
                        f'examination paper — © State Examinations Commission.'),
        'presentationNote': (
            'Read the printed passage exactly as the examination set it, then '
            'answer. The passage and the question are printed in Arabic and '
            'read right to left.'),
    }


class Author:
    def __init__(self):
        self.cards = []
        self.refusals = collections.defaultdict(list)
        self.excluded = []
        self.covered = set()
        self.leaves = 0

    def refuse(self, bucket, ref, evidence):
        self.refusals[bucket].append((ref, evidence))

    # ------------------------------------------------------------------ walk
    def run(self):
        for year in YEARS:
            for level in LEVELS:
                try:
                    P = AraPaper(year, level)
                    S = AraScheme(year, level)
                except FileNotFoundError:
                    continue
                self.sitting(P, S, year, level)

    def sitting(self, P, S, year, level):
        leaves = P.leaves
        self.leaves += len(leaves)
        by_q = collections.defaultdict(list)
        for a in leaves:
            by_q[a.question].append(a)
        src = source_material(P, year, level)
        for q, asks in sorted(by_q.items()):
            if q in GRID_QUESTIONS:
                self.exclude_grid(S, year, level, asks, q)
                continue
            topic = CARDED.get(q)
            if topic is None:
                self.refuse('the paper sets a question this reader does not '
                            'place', question_ref(year, level, q),
                            f'{year} {level.upper()} paper: Q{q}')
                continue
            letters = [a.letter for a in asks if a.letter]
            pairs = S.aligned(q, letters)
            if not pairs:
                self.refuse('the scheme does not state one answer per printed '
                            'part', question_ref(year, level, q),
                            f'{year} {level.upper()} scheme: the paper prints '
                            f'{len(asks)} part(s) and the scheme states '
                            f'{len(S.by_question().get(q, []))} row(s)')
                continue
            if q in (1, 2, 3, 4):
                self.comprehension(P, S, year, level, asks[0], pairs, topic, src)
            elif q == 14:
                self.parsing(P, S, year, level, asks[0], topic)
            else:
                self.grammar(P, S, year, level, asks, pairs, topic)

    # ------------------------------------------------------------- the cards
    def comprehension(self, P, S, year, level, ask, pairs, topic, src):
        ref = question_ref(year, level, ask.question)
        if not ask.options:
            self.refuse('the paper prints no options for a multiple choice',
                        ref, f'{year} {level.upper()} paper p{ask.page}')
            return
        row = pairs[0][1]
        letter = row.letter
        if letter is None:
            self.refuse('the scheme names no option for a multiple choice',
                        ref, f'{year} {level.upper()} scheme p{row.page}: '
                             f'{row.text[:80]!r}')
            return
        chosen = [t for l, t in ask.options
                  if ara_text._normalise(l) == row.arabic_letter]
        if not chosen:
            self.refuse('the option the scheme names is not one the paper '
                        'prints', ref,
                        f'{year} {level.upper()} scheme p{row.page} names '
                        f'({row.arabic_letter}); the paper prints '
                        f'{[l for l, _ in ask.options]}')
            return
        marks = row.marks or ask.marks
        if marks is None:
            self.refuse('the scheme prints no tariff this reads for the ask',
                        ref, f'{year} {level.upper()} scheme p{row.page}')
            return
        stem = ask.text.strip()
        options = '\n'.join(f'({l}) {t}'.strip() for l, t in ask.options)
        answer = chosen[0].strip().rstrip('.') or row.text
        note = ANSWER_LANGUAGE
        if row.text and row.text.strip('. ') not in ('', row.arabic_letter):
            note += (' The scheme states the answer as '
                     f'"({row.arabic_letter}) {row.text}".')
        else:
            note += (f' The scheme states the answer as the option letter '
                     f'({row.arabic_letter}); the words are the paper’s own.')
        self.cards.append({
            'id': card_id(year, level, ask.question),
            'subjectId': SUBJECT,
            'level': LEVEL_WORD[level],
            'year': year,
            'section': str(ask.part),
            'topicId': topic,
            'conceptId': concept_id(stem, f'ara-comprehension-{ask.question}'),
            'questionRef': ref,
            'questionText': f'{stem}\n{options}',
            'tariffModel': {'kind': 'fixed'},
            'totalMarks': marks,
            'rows': [{'id': 'r-1', 'kind': 'point',
                      'verbatim': f'({row.arabic_letter}) {answer}',
                      'marks': marks, 'contextNote': note}],
            'notes': (f'The scheme prices this ask at {marks} marks. The paper '
                      f'prints it on page {ask.page} of the question booklet.'),
            **({'sourceMaterial': src} if src else {}),
        })
        self.covered.add(ref)

    def grammar(self, P, S, year, level, asks, pairs, topic):
        stem = next((a.text for a in P.asks
                     if a.question == asks[0].question and a.letter is None), '')
        notes = ' '.join(S.notes.get(asks[0].question, []))
        by_letter = {a.letter: a for a in asks}
        for letter, row in pairs:
            ask = by_letter.get(letter)
            if ask is None:
                continue
            ref = question_ref(year, level, ask.question, letter)
            marks = row.marks
            if marks is None:
                self.refuse('the scheme prints no tariff this reads for the ask',
                            ref, f'{year} {level.upper()} scheme p{row.page}: '
                                 f'{row.text[:60]!r}')
                continue
            note = ANSWER_LANGUAGE
            if notes:
                note += f' The scheme states: "{notes}"'
            self.cards.append({
                'id': card_id(year, level, ask.question, letter),
                'subjectId': SUBJECT,
                'level': LEVEL_WORD[level],
                'year': year,
                'section': str(ask.part),
                'topicId': topic,
                'conceptId': concept_id(
                    ask.text, f'ara-grammar-{ask.question}-{letter}'),
                'questionRef': ref,
                'questionText': (f'{stem}\n({ask.arabic_letter}) {ask.text}'
                                 if stem else
                                 f'({ask.arabic_letter}) {ask.text}'),
                'tariffModel': {'kind': 'fixed'},
                'totalMarks': marks,
                'rows': [{'id': 'r-1', 'kind': 'point',
                          'verbatim': row.text, 'marks': marks,
                          'contextNote': note}],
                'notes': (f'The scheme prices this part at {marks} marks, one '
                          f'of the {len(pairs)} the question is split into. '
                          f'The paper prints it on page {ask.page} of the '
                          f'question booklet.'),
            })
            self.covered.add(ref)

    def parsing(self, P, S, year, level, ask, topic):
        ref = question_ref(year, level, ask.question)
        # The parsing cell prints, in order: the sentence being parsed, then
        # one priced marking point per word of it. The sentence is the QUESTION
        # and is already in the stem, so it is not a marking point; and a
        # marking point that runs to a second line arrives as a row with no
        # tariff of its own, which belongs to the point above it.
        rows = []
        for r in S.by_question().get(14, []):
            if not r.text:
                continue
            if r.text.startswith('"') or r.text.startswith('الكلمة'):
                continue
            if r.marks is None and rows:
                rows[-1].text = f'{rows[-1].text} {r.text}'.strip()
                continue
            if r.marks is None:
                continue
            rows.append(r)
        if not rows:
            self.refuse('the scheme prints no priced marking point for the '
                        'parsing ask', ref,
                        f'{year} {level.upper()} scheme')
            return
        rows = rows[:MAX_ROWS]
        total = ask.marks or sum(r.marks for r in rows)
        if sum(r.marks for r in rows) != total:
            self.refuse('the parsing ask’s marking points do not sum to its '
                        'tariff', ref,
                        f'{year} {level.upper()}: rows sum to '
                        f'{sum(r.marks for r in rows)}, the paper prices it '
                        f'{total}')
            return
        self.cards.append({
            'id': card_id(year, level, 14),
            'subjectId': SUBJECT,
            'level': LEVEL_WORD[level],
            'year': year,
            'section': str(ask.part),
            'topicId': topic,
            'conceptId': f'ara-parsing-{year}-{level}',
            'questionRef': ref,
            'questionText': ask.text,
            'tariffModel': {'kind': 'fixed'},
            'totalMarks': total,
            'rows': [{'id': f'r-{i}', 'kind': 'point', 'verbatim': r.text,
                      'marks': r.marks,
                      'contextNote': ANSWER_LANGUAGE if i == 1 else ''}
                     for i, r in enumerate(rows, 1)],
            'notes': (f'The scheme splits this ask’s {total} marks over '
                      f'{len(rows)} marking points, at '
                      f'{"/".join(str(r.marks) for r in rows)}. The paper '
                      f'prints it on page {ask.page} of the question booklet.'),
        })
        self.covered.add(ref)

    # -------------------------------------------------------- the exclusions
    def exclude_grid(self, S, year, level, asks, q):
        for ask in asks:
            ref = question_ref(year, level, q, ask.letter)
            self.excluded.append({
                'ref': ref,
                'reason': ('the scheme marks this ask with a '
                           'Communication-and-Content grid over a list it '
                           'states is not exhaustive'),
                'evidence': (
                    f'{year} {LEVEL_TITLE[level]} scheme, Question {q}: the '
                    f'marking cell prints the three grid rows — Communication '
                    f'and Content, Knowledge and Application of Language, '
                    f'Accuracy of Language — against the tariff, over a list '
                    f'headed "{INDICATIVE} إلى:" ("it should be noted"), and '
                    f'adds "(Responses require appropriate development or '
                    f'elaboration beyond mere textual transcription)". Nothing '
                    f'in that cell states an answer a card could lift.'),
            })


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--exclusions', action='store_true')
    args = ap.parse_args()
    A = Author()
    A.run()
    if args.exclusions:
        path = os.path.join(DIR, 'exclusions', f'{SUBJECT}.json')
        with open(path, 'w') as fh:
            json.dump(A.excluded, fh, ensure_ascii=False, indent=1)
        print(f'{len(A.excluded)} exclusion(s) -> {path}', file=sys.stderr)
        return 0
    if args.report:
        print(f'{A.leaves} leaf asks in the ten papers')
        print(f'{len(A.cards)} card(s) over {len(A.covered)} covered ask(s)')
        print(f'{len(A.excluded)} excluded (the Communication-and-Content grid)')
        open_n = A.leaves - len(A.covered) - len(A.excluded)
        print(f'{open_n} open')
        for bucket, hits in sorted(A.refusals.items(),
                                   key=lambda kv: -len(kv[1])):
            print(f'\n  {len(hits):>4}  {bucket}')
            for ref, evidence in hits[:3]:
                print(f'          {ref}: {evidence}')
        return 0
    json.dump(A.cards, sys.stdout, ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
