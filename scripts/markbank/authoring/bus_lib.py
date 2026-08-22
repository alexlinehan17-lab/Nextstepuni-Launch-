#!/usr/bin/env python3
"""Assemble Business cards from the marking scheme's own table.

    A = Author(2021, 'ol')
    A.card(2, 1, 'a', 'i', topic='business-2-11', concept='what-the-ccpc-is',
           use=[0], marks=[10])
    A.emit()

Where the wording comes from, and why it is not the paper
--------------------------------------------------------
Every other subject takes its question text from the question paper. Business
cannot: it prints its paper as an answerbook, interleaving question text with
ruled answer space, and the block parser returns page furniture for two thirds
of it. Sixty-six of its parts could not even be measured until bus_parts was
written.

The marking scheme prints the question itself, in the tariff table beside the
marks, and at Ordinary Level prints the answers underneath it in the same cell.
That table is a published State Examinations Commission document, so a card
built from it is still lifted rather than written — which is the rule that
matters. It is recorded on every card built this way, in the schemeCitation, so
nobody has to guess later which document a Business question was read from.

What it refuses
---------------
  * a part bus_parts did not find, or found with no question text;
  * a marking point that is not one of the lines the scheme printed under that
    part — the caller chooses by index, never by string;
  * marks that do not sum to the tariff the scheme printed for the part;
  * a question that still has its answer welded to it, which happens when the
    tariff sits on a continuation line rather than the first, because a card
    would otherwise show a student the answer inside the question.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bus_parts import parts, ref                            # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
SCHEMES = os.path.join(ROOT, 'examiner-reports/business/schemes')
CITATION = ('Question and marking points quoted from the SEC marking scheme, Business '
            '{year} {level} — © State Examinations Commission. Business prints its paper '
            'as an answerbook, so the scheme\'s own table is the published source for the '
            'question as well as for the answer.')


class Refused(Exception):
    pass


def _squash(text):
    return re.sub(r'[^a-z0-9]+', '', (text or '').lower())


class Author:
    def __init__(self, year, level):
        self.year, self.level = year, level
        self.cards = []
        self.parts = {}
        for p in parts(year, level):
            self.parts[(p['section'], p['question'], p['part'], p['roman'])] = p
        with open(os.path.join(SCHEMES, f'{year}-{level}.md'), encoding='utf-8') as fh:
            self.raw = _squash(fh.read())

    def card(self, section, q, part, roman=None, *, topic, concept, use, marks,
             notes=None, notation=None, row_kind='point', suffix='', words=None,
             extend=0, shared_tariff=False):
        key = (section, q, part, roman)
        p = self.parts.get(key)
        if p is None:
            raise Refused(f'{key}: bus_parts found no such part')
        r = ref(p, self.year, self.level)
        question = p['text'].strip()
        if extend:
            # The question wrapped past its own line and the rest of it landed
            # among the answer lines: 2021 OL Q4(E) reads 'Explain, giving two
            # reasons, why the advertisement shown is unlawful' on the tariff
            # line and 'under the Employment Equality Acts 1998-2015' on the
            # next. extend says how many of those lines finish the question.
            question = ' '.join([question] + [a.strip() for a in p['answers'][:extend]])
            # The answer list is deliberately NOT reindexed. An index in `use`
            # always means the line the scheme printed at that position, so
            # adding or changing an extend cannot silently move which lines a
            # card is quoting.
        if words is not None:
            question = ' '.join(question.split()[:words]).strip()
            if _squash(question) not in self.raw:
                raise Refused(f'{r}: the {words}-word question does not trace to '
                              f'the scheme: {question!r}')
        elif not p.get('clean', True):
            # The scheme set this part's tariff on a continuation line, so the
            # reader had no boundary and the text carries some of its own answer.
            # A card built from it would show the answer inside the question.
            listing = ' '.join(f'[{i}]{w}' for i, w in enumerate(question.split()))
            raise Refused(f'{r}: the tariff is not on the question\'s own line, so the '
                          f'text has answer welded on. Pass words=<n> to say where the '
                          f'question ends.\n      {listing[:400]}')
        if len(question) < 12:
            raise Refused(f'{r}: no question text')
        if not p['answers']:
            raise Refused(f'{r}: the scheme printed no answer lines under this part')

        # An entry in `use` is a line index, or a list of them where one marking
        # point wrapped over several lines — the scheme sets a bullet and its
        # continuation as two lines and they are one point.
        chosen = []
        for entry in use:
            idxs = entry if isinstance(entry, (list, tuple)) else [entry]
            for i in idxs:
                if i >= len(p['answers']):
                    raise Refused(f'{r}: no answer line {i} — the scheme printed '
                                  f'{len(p["answers"])}')
            joined = ' '.join(p['answers'][i].strip() for i in idxs)
            chosen.append((re.sub(r'\s+', ' ', joined).lstrip('•').strip(),
                           [p['answers'][i] for i in idxs]))
        if len(marks) != len(chosen):
            raise Refused(f'{r}: {len(marks)} marks for {len(chosen)} points')

        # The JOINED point has to trace, not merely each line of it. The build
        # runs its own provenance gate on the verbatim a card carries, and a
        # point joined across lines the tariff column sits between will not
        # trace there — checking line by line here just moved the rejection
        # later, to a card that had already been written. Where a point's lines
        # are not contiguous in the scheme, that point cannot be carded as one.
        chosen = [c for c, _ in chosen]
        for c in chosen:
            if _squash(c.lstrip('•').strip()) not in self.raw:
                raise Refused(f'{r}: {c[:60]!r} does not trace to the scheme — its '
                              f'lines are not contiguous there')

        tariff = [int(m) for m in p['marks'] if m.isdigit()]
        total = sum(marks)
        if shared_tariff:
            # One tariff can cover a part and the parts under it: 2021 OL
            # Q1(A) prints ⟨10m⟩ once and splits it 5 and 5 between (i) and
            # (ii). The sum check cannot apply, so the card has to say on its
            # face what the printed figure covers instead.
            if not notation:
                raise Refused(f'{r}: shared_tariff needs a notation saying what the '
                              f'printed tariff covers')
        elif tariff and total != tariff[0]:
            raise Refused(f'{r}: marks sum to {total}, but the scheme prints '
                          f'{tariff[0]} for this part')

        level = 'higher' if self.level == 'hl' else 'ordinary'
        qnum = f'q{q}' if q else 'abq'
        cid = (f'bus-{self.year}-{self.level}-s{section}-{qnum}'
               f'-{part}{"-" + roman if roman else ""}{suffix}')
        self.cards.append({
            'id': cid, 'topicId': topic, 'conceptId': concept, 'level': level,
            'year': self.year, 'subjectId': 'business', 'section': str(section),
            'questionRef': r, 'questionText': question,
            'schemeCitation': CITATION.format(
                year=self.year, level='Higher Level' if self.level == 'hl' else 'Ordinary Level'),
            'tariffModel': {'kind': 'fixed', **({'notation': notation} if notation else {})},
            'totalMarks': total,
            'rows': [{'id': f'r-{i + 1}', 'kind': row_kind, 'verbatim': c, 'marks': m}
                     for i, (c, m) in enumerate(zip(chosen, marks))],
            **({'notes': notes} if notes else {}),
        })
        return self.cards[-1]

    def emit(self):
        print(json.dumps(self.cards, ensure_ascii=False, indent=1))
