#!/usr/bin/env python3
"""Author every History ask the papers print and the schemes answer.

    python3 scripts/markbank/authoring/hist_all.py --report
    python3 scripts/markbank/authoring/hist_all.py > scripts/markbank/authored/history.json
    python3 scripts/markbank/authoring/hist_all.py --exclusions   # rewrite the ledger

Census-driven. It walks every ask each carded paper prints (PAPERS: 2021-2026
at both levels and in both fields, then back a paper at a time from 2020, the
one year the SEC set Later Modern alone) rather than choosing what to card.

WHAT IS CARDED, AND WHAT IS EXCLUDED
------------------------------------
History is the first subject in this bank where most of the paper cannot be
carded, and the reason is printed in the scheme rather than deduced.

*Carded.* The Documents-Based Question, and Ordinary Level's Part A. The
comprehension parts get a flat tariff list — "(a) To fight desegregation/
maintain segregation 5M" — and Part A gets five one-line answers at (6) apiece.
The comparison and criticism parts get the examiner's own model answer, priced
once on the ask with no per-point split.

*Excluded, until carded as essays.* Every essay: Higher Level's Sections 2
and 3, Ordinary Level's parts B and C, and the documents question's
contextualisation part. The whole scheme entry for one of those is a ceiling —
"1. Max. CM = 60 Max. OE = 40" — and there is no answer under it to lift. Each
still gets an entry in exclusions/history.json carrying that printed line as
its evidence, written by --exclusions from the scheme itself so it cannot
drift from what the SEC prints — except on a paper in ESSAY_PAPERS.

*Essay cards.* Alex's rule (2026-10-28) is that every printed ask is a card,
and an essay is marked by paragraph, which the scheme DOES print: a Cumulative
Mark built from a band ladder paragraph by paragraph up to a printed maximum,
and an Overall Evaluation on one band, each with its descriptors, plus the
question's own NOTE ("TWO elements … If only ONE, Max. CM = 50"). On a paper
in ESSAY_PAPERS every such ask is a `history-essay` rubric card carrying that
apparatus verbatim (hist_scheme.paragraph_marking) and no model answer, which
the scheme does not print. Papers join ESSAY_PAPERS one at a time, as each is
reviewed in the browser.

THE TWO TARIFF MODELS, BOTH READ
--------------------------------
`fixed` where the scheme prints the part's own marks and answers it in one
line: comprehension (5M at Higher, 8M at Ordinary) and Part A (6). One row,
carrying those marks, which reconcile against the total exactly.

`questionTotal` where the scheme prints ONE total for the ask and then lists
candidate points without dividing the marks between them — every comparison and
criticism part. Rows carry `marks: null`, which is what that model means. A
per-point value here would be the sixth guessed tariff in this bank.

LAW 4, WITHOUT A REPRINTED QUESTION
-----------------------------------
The scheme does not reprint the question it is marking, so align.py's cue join
has nothing to score. Two other joins are available and both are used:

  * the TOPIC TITLE. Both documents print it — "Ireland: Topic 1 / Ireland and
    the Union, 1815-1870" — and it is the level at which a mis-numbering would
    do real damage, moving thirteen asks at once. Every topic on every paper is
    scored against every topic in its own scheme, and must pick its own.
  * the TARIFF. The marks the PAPER prints for a unit must equal what the
    SCHEME prices under it: A (30 marks) against five answers at (6); B (30)
    against "Max CM = 20 marks Max OE = 10 marks"; each Higher essay's (100)
    against "Max. CM = 60 Max. OE = 40"; the documents question's (20) against
    four parts at 5M. Every one of the 1,430 is checked and reported.
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

from hist_paper import HistPaper, FIELDS                      # noqa: E402
from hist_scheme import HistScheme, GRID_WORDS                # noqa: E402
from hist_topics import topic_for, concept_for, TITLES        # noqa: E402
from hist_rows import split_priced                           # noqa: E402
from align import bag, score                                  # noqa: E402

LEVELS = ('hl', 'ol')
FIELD_KEYS = ('lm', 'em')
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
EXCLUSIONS = os.path.join(DIR, 'exclusions', 'history.json')

# The papers whose essays and contextualisation part are carded as
# `history-essay` rubric cards rather than excluded. 2025 Higher Later Modern
# is the prototype (lane batch 1, 4 Nov 2026); the rest follow once it has
# been reviewed.
ESSAY_PAPERS = {
    (2019, 'hl', 'em'),
    (2019, 'hl', 'lm'),
    (2019, 'ol', 'em'),
    (2019, 'ol', 'lm'),
    (2020, 'hl', 'lm'),
    (2020, 'ol', 'lm'),
    (2021, 'hl', 'em'),
    (2021, 'hl', 'lm'),
    (2021, 'ol', 'em'),
    (2021, 'ol', 'lm'),
    (2022, 'hl', 'em'),
    (2022, 'hl', 'lm'),
    (2022, 'ol', 'em'),
    (2022, 'ol', 'lm'),
    (2023, 'hl', 'em'),
    (2023, 'hl', 'lm'),
    (2023, 'ol', 'em'),
    (2023, 'ol', 'lm'),
    (2024, 'hl', 'em'),
    (2024, 'hl', 'lm'),
    (2024, 'ol', 'em'),
    (2024, 'ol', 'lm'),
    (2025, 'hl', 'em'),
    (2025, 'hl', 'lm'),
    (2025, 'ol', 'em'),
    (2025, 'ol', 'lm'),
    (2026, 'hl', 'em'),
    (2026, 'hl', 'lm'),
    (2026, 'ol', 'em'),
    (2026, 'ol', 'lm'),
}
# The papers carded. A paper is carded whole, essays included, so these are
# the essay papers; each joins one at a time, as it is read and reviewed
# (2021-2026 in lane batches 1-2, then back from 2020).
PAPERS = sorted(ESSAY_PAPERS, key=lambda p: (p[0], p[1], FIELD_KEYS.index(p[2])))

# NextStepUni's own guidance under the panel, never presented as the SEC's,
# for each way the scheme marks: (CM mode, prints an OE).
ESSAY_GUIDE = {
    ('paragraph', True): ('Place each paragraph you wrote, in the order you '
                          'wrote it, on the one band that fits it. The CM '
                          'stops at its maximum, so a paragraph past it counts '
                          '0m. Then place your whole answer on one OE band.'),
    ('core-statement', True): ('Count the Core Statements you completed and '
                               'place an incomplete last one if you wrote one. '
                               'The CM stops at its maximum, so a Core Statement '
                               'past it counts 0m. Then place your whole answer '
                               'on one OE band.'),
    ('core-statement', False): ('Count the Core Statements you completed and '
                                'place an incomplete last one if you wrote one. '
                                'The CM stops at its maximum, so a Core '
                                'Statement past it counts 0m.'),
}

# The floor a topic-title pairing has to clear. The two documents print the
# same title, so a real pair scores near 1.0; the floor is where a pair would
# be resting on the key alone, which Law 4 forbids.
TITLE_FLOOR = 0.60

# The scheme's own words for "this list is not exhaustive". Where the examiner
# says it, every row of that ask is openList, which is the card model's field
# for it and what turns on the session's "I wrote a different valid point".
OPEN_LIST = re.compile(
    r'\b(?:may include|could include|might include|such as the following'
    r'|points could include|etc\.)', re.I)

UNIT_RE = re.compile(r'^(?:(\d) Topic (\d)(?: ([ABC]))?|Extra A|1)$')


def unit_parts(unit):
    """('2', 3, 'A') for "2 Topic 3 A"; ('1', None, None) for the DBQ."""
    if unit == '1':
        return '1', None, None
    if unit == 'Extra A':
        return None, None, 'A'
    m = UNIT_RE.match(unit)
    return m.group(1), int(m.group(2)), m.group(3)


def slug(unit):
    if unit == '1':
        return 's1'
    if unit == 'Extra A':
        return 'extra-a'
    section, topic, part = unit_parts(unit)
    return f's{section}t{topic}' + (part.lower() if part else '')


def card_id(year, level, field, key):
    unit, q, letter, roman = key
    bits = ['hist', str(year), level, field, slug(unit)]
    if q is not None:
        bits.append(f'q{q}')
    if letter:
        bits[-1] += letter
    if roman:
        bits[-1] += roman
    return '-'.join(bits)


def question_ref(year, level, field, key):
    unit, q, letter, roman = key
    ref = f'{year} {level.upper()} {FIELDS[field]} Section {unit}'
    if q is None and letter is None and roman is None:
        return ref
    ref += ' Q' + ('' if q is None else str(q))
    if letter:
        ref += f'({letter})'
    if roman:
        ref += f'({roman})'
    return ref


def source_material(P, year, level, field, unit, pages, title, label):
    return {
        'kind': 'source-text',
        'label': label,
        'title': title,
        'pages': pages,
        'attribution': (f'SEC History {year} '
                        f'{"Higher" if level == "hl" else "Ordinary"} Level '
                        f'examination paper, {FIELDS[field]} — '
                        '© State Examinations Commission.'),
        'presentationNote': ('Read the exact source as it appeared in the '
                             'examination paper, then answer the question '
                             'above.'),
    }


def _bands(bands):
    return [{k: b[k] for k in ('label', 'marks', 'printed', 'descriptor') if k in b}
            for b in bands]


def _alternatives(text):
    """The four printed alternatives of a part B or C, or None.

    "1. The Tithe War. 2. William Dargan. ..." -- numbered 1 to 4 in print
    order. The 2022 Ordinary Later Modern paper prints its Europe Topic 4
    part B's second alternative as "2 The 1973 oil crisis." (no full stop on
    the page), so the stop is optional for the NEXT number in the run when a
    capital follows; the text is kept exactly as printed.
    """
    starts, pos = [], 0
    for k in range(1, 5):
        m = re.compile(rf'(?:^|\s)({k})\.?\s+(?=[A-Z\u201c"\u2018\'(])').search(text, pos)
        if not m:
            return None
        starts.append(m.start(1))
        pos = m.end()
    return [text[a:(starts[i + 1] if i + 1 < len(starts) else len(text))].strip()
            for i, a in enumerate(starts)]


def essay_card(P, S, year, level, field, key, ask, section, topic_id, ref):
    """One `history-essay` rubric card, or the reason it cannot be made."""
    unit = key[0]
    part = unit.rsplit(' ', 1)[-1] if level == 'ol' and unit != '1' else None
    question = P.asks[key]
    if level == 'hl':
        marking = S.paragraph_marking('q4' if unit == '1' else 'essay')
        cm, oe = marking['cm'], marking['oe']
        rubric_cm = {
            'mode': 'paragraph',
            'max': cm['max'],
            'definition': cm['definition'],
            'paragraphLead': cm['paragraphLead'],
            'paragraphKinds': cm['paragraphKinds'],
            'bands': _bands(cm['bands']),
            'directions': cm['directions'],
        }
        if unit != '1' and (ask.cm_max, ask.oe_max) != (cm['max'], oe['max']):
            return 'the essay ceiling disagrees with the paragraph-marking maximum'
    else:
        marking = S.core_statement_marking('q4' if unit == '1' else part)
        cm, oe = marking['cm'], marking['oe']
        rubric_cm = {
            'mode': 'core-statement',
            'max': cm['max'],
            # Q4 prints no CM definition of its own; its "Here, in question 4 of
            # the DBQ, the examiner will be looking to award 5 marks each to
            # four Core Statements ..." is what the CM is, there.
            'definition': (cm.get('definition')
                           or next(g for g in marking['schemeGuidance'] if g.startswith('Here, in question 4'))),
            'statementLead': cm['statementLead'],
            'statementKinds': cm['statementKinds'],
            'procedureLead': cm['procedureLead'],
            'procedure': cm['procedure'],
            'perStatement': cm['perStatement'],
            'incomplete': cm['incomplete'],
            'directions': cm['directions'],
        }
        if unit != '1' and (ask.cm_max, ask.oe_max) != (cm['max'], oe['max']):
            return "the part's ceiling disagrees with the Core Statement maxima"
    total = cm['max'] + (oe['max'] if oe else 0)
    printed = P.marks.get(key)
    if ask.total != total or (printed is not None and printed != total):
        return 'the paper, the scheme and the CM + OE maxima disagree'
    if ask.note is not None:
        if not ask.note_caps or not all(0 < top < cm['max'] for _when, top in ask.note_caps):
            return "the question's NOTE prints no CM ceiling below the maximum"
        rubric_cm['elementRule'] = {'note': ask.note,
                                    'caps': [{'when': when, 'max': top} for when, top in ask.note_caps]}
    guidance = [g for g in marking['schemeGuidance'] if g != rubric_cm['definition']]
    rubric = {'system': 'history-essay', 'schemeGuidance': guidance, 'cm': rubric_cm}
    if oe:
        rubric_oe = {'max': oe['max']}
        for name in ('definition', 'lead'):
            if name in oe:
                rubric_oe[name] = oe[name]
        rubric_oe['bands'] = _bands(oe['bands'])
        if 'directionsLead' in oe:
            rubric_oe['directionsLead'] = oe['directionsLead']
        rubric_oe['directions'] = oe['directions']
        rubric['oe'] = rubric_oe
    rubric['schemePages'] = sorted(set(marking['pages']) | ({ask.page} if ask.page else set()))
    rubric['markingGuideNote'] = ESSAY_GUIDE[rubric_cm['mode'], bool(oe)]
    if part in ('B', 'C'):
        # One card for the printed choice: the instruction the paper prints
        # over it, and its four alternatives each on its own line, as printed.
        instruction = P.instructions.get(unit)
        items = _alternatives(question)
        if not instruction or not items:
            return 'the printed choice and its instruction could not be read whole'
        question = '\n'.join([instruction, *items])
    card = {
        'id': card_id(year, level, field, key),
        'subjectId': 'history',
        'kind': 'rubric',
        'level': LEVEL_WORD[level],
        'year': year,
        'section': section,
        'topicId': topic_id,
        'conceptId': concept_for(P.asks[key]),
        'questionRef': ref,
        'questionText': question,
        'totalMarks': total,
        'rubric': rubric,
        'notes': (f'{FIELDS[field]} field of study. The scheme prints '
                  f'{ask.evidence[:60]!r} for this ask and no model answer.'),
    }
    stem = (f'Case study: {P.case_title}' if unit == '1' and P.case_title
            else P.topic_titles.get(unit.rsplit(' ', 1)[0] if part else unit))
    if stem and len(stem) >= 20:
        card['stem'] = stem
    return card


# A part the scheme prices only by its split, printing no answer: 2021
# Ordinary Later Modern Q3(b) is exactly "One opinion = 5M / Explanation = 5M
# / Max = 10M". Each priced component is a claimable row in the scheme's own
# words, and the row says the scheme prints no answer for it.
PRICED_COMPONENT = re.compile(r'([A-Z][A-Za-z \u2019\'-]{1,40}?)\s*=\s*(\d{1,3})M\b')
TARIFF_CEILING = re.compile(r'\bMax\.?\s*=\s*(\d{1,3})M\b')
NO_PRINTED_ANSWER = 'The scheme prints no answer here: any correct one earns the marks.'
TARIFF_WORDING = re.compile(r'^(?:ONE|TWO|THREE|[Oo]ne valid|[Tt]wo valid|[Aa]ny valid)\b(?![^.]*\.\s*\S)')


def split_card(P, year, level, field, key, ask, section, topic_id, ref):
    """A documents part the scheme prices component by component, answering
    each: one row per component at its printed marks (hist_scheme
    `_answered_split`). A component answered under its own line keeps that
    line, price and all, as the row's note."""
    question = P.asks[key]
    rows = []
    for i, (label, point, note) in enumerate(ask.points, start=1):
        row = {'id': f'r-{i}', 'kind': 'point', 'verbatim': point,
               'marks': ask.components[i - 1][1]}
        if note:
            row['contextNote'] = note
        rows.append(row)
    card = {
        'id': card_id(year, level, field, key),
        'subjectId': 'history',
        'level': LEVEL_WORD[level],
        'year': year,
        'section': section,
        'topicId': topic_id,
        'conceptId': concept_for(question),
        'questionRef': ref,
        'questionText': question,
        'tariffModel': {'kind': 'fixed'},
        'totalMarks': ask.total,
        'rows': rows,
        'notes': (f'{FIELDS[field]} field of study. The scheme prints '
                  f'{ask.notation!r} for this ask: each component at its '
                  f'printed marks.'),
    }
    if P.case_title:
        card['stem'] = f'Case study: {P.case_title}'
    card['sourceMaterial'] = source_material(
        P, year, level, field, '1', P.document_pages, 'The documents', 'OFFICIAL DOCUMENTS')
    return card


def tariff_only_card(P, year, level, field, key, ask, section, topic_id, ref):
    """A point card for a part priced by its split alone, or the reason it cannot be made."""
    evidence = ask.evidence
    ceiling = TARIFF_CEILING.search(evidence)
    parts = [(name.strip(), int(m)) for name, m in PRICED_COMPONENT.findall(evidence)
             if not name.strip().lower().startswith('max')]
    if not ceiling or not parts or sum(m for _n, m in parts) != int(ceiling.group(1)):
        return "the part's printed split does not add up to its ceiling"
    question = P.asks[key]
    card = {
        'id': card_id(year, level, field, key),
        'subjectId': 'history',
        'level': LEVEL_WORD[level],
        'year': year,
        'section': section,
        'topicId': topic_id,
        'conceptId': concept_for(question),
        'questionRef': ref,
        'questionText': question,
        'tariffModel': {'kind': 'fixed'},
        'totalMarks': int(ceiling.group(1)),
        'rows': [{'id': f'r-{i}', 'kind': 'criterion', 'verbatim': name, 'marks': marks,
                  'contextNote': NO_PRINTED_ANSWER}
                 for i, (name, marks) in enumerate(parts, start=1)],
        'notes': (f'{FIELDS[field]} field of study. The scheme prints '
                  f'{evidence!r} for this ask: a price for each component and no answer.'),
    }
    if P.case_title:
        card['stem'] = f'Case study: {P.case_title}'
    card['sourceMaterial'] = source_material(
        P, year, level, field, '1', P.document_pages, 'The documents', 'OFFICIAL DOCUMENTS')
    return card


def build():
    cards = []
    exclusions = []
    refused = collections.Counter()
    examples = collections.defaultdict(list)
    title_pairs = []
    title_variants = []
    tariff_checks = {'agree': 0, 'disagree': []}
    extra_topic_checks = []

    def refuse(reason, ref):
        refused[reason] += 1
        examples[reason].append(ref)

    for year, level, field in PAPERS:
        if True:
            if True:
                P = HistPaper(year, level, field)
                S = HistScheme(year, level, field)

                # --- Law 4, join one: the topic title, on both documents.
                scheme_titles = [(u, bag(t))
                                 for u, t in S.topic_titles.items()]
                for unit, title in sorted(P.topic_titles.items()):
                    cue = bag(title)
                    ranked = sorted(((score(cue, sb), u)
                                     for u, sb in scheme_titles),
                                    key=lambda t: t[0], reverse=True)
                    best, best_unit = ranked[0] if ranked else (0.0, None)
                    own = next((s for s, u in ranked if u == unit), 0.0)
                    where = f'{year} {level} {field} {unit}'
                    if best_unit != unit or own < TITLE_FLOOR:
                        refuse('the scheme topic title matches another topic '
                               'better than its own',
                               f'{where} (own {own:.2f}, best {best:.2f})')
                        continue
                    title_pairs.append((where, own))
                    if (re.sub(r'[^a-z0-9]+', '', title.lower())
                            != re.sub(r'[^a-z0-9]+', '',
                                      S.topic_titles[unit].lower())):
                        title_variants.append(
                            f'{where}: paper {title!r}, '
                            f'scheme {S.topic_titles[unit]!r}')

                # --- the extra Part A files under the DBQ's own topic.
                if 'Extra A' in {k[0] for k in P.asks}:
                    extra_topic_checks.append(
                        (f'{year} {level} {field}', P.case_study))

                # --- Law 4, join two: the tariff, unit by unit.
                for unit, printed in sorted(P.unit_marks.items()):
                    section, topic, part = unit_parts(unit)
                    if part == 'A':
                        priced = sum(a.total or 0 for a in S.asks
                                     if a.key[0] == unit and a.total)
                    else:
                        ask = S.by_key.get((unit, None, None, None))
                        priced = ask.total if ask else None
                    if priced == printed:
                        tariff_checks['agree'] += 1
                    else:
                        tariff_checks['disagree'].append(
                            f'{year} {level} {field} {unit}: paper {printed}, '
                            f'scheme {priced}')
                for q, printed in sorted(
                        (k[1], v) for k, v in P.marks.items() if k[0] == '1'):
                    priced = sum(a.total or 0 for a in S.asks
                                 if a.key[0] == '1' and a.key[1] == q)
                    if priced == printed:
                        tariff_checks['agree'] += 1
                    else:
                        tariff_checks['disagree'].append(
                            f'{year} {level} {field} Section 1 Q{q}: '
                            f'paper {printed}, scheme {priced}')
                for key, printed in sorted(
                        ((k, v) for k, v in P.marks.items()
                         if k[0] != '1' and k[1] is not None),
                        key=lambda kv: str(kv[0])):
                    ask = S.by_key.get(key)
                    priced = ask.total if ask else None
                    if priced == printed:
                        tariff_checks['agree'] += 1
                    else:
                        tariff_checks['disagree'].append(
                            f'{year} {level} {field} {key}: paper {printed}, '
                            f'scheme {priced}')

                # --- one card, or one exclusion, per printed ask.
                for key in sorted(P.asks, key=lambda k: tuple(str(x) for x in k)):
                    ref = question_ref(year, level, field, key)
                    unit = key[0]
                    section, topic, part = unit_parts(unit)
                    ask = S.by_key.get(key)
                    if ask is None:
                        refuse('the scheme prices no ask at this address', ref)
                        continue

                    # The card's `section` is the paper's own section; the
                    # TOPIC it files under is a separate question. Section 1
                    # prints its case study's topic under its head, and the
                    # extra Part A of 2023-2025 Ordinary restores the topic the
                    # documents question took out of Sections 2 and 3 — so both
                    # take their topic from the documents question, while only
                    # the extra unit belongs to that topic's own section.
                    if unit in ('1', 'Extra A'):
                        if not P.case_study:
                            refuse('the ask sits under no syllabus topic', ref)
                            continue
                        topic_section, topic = P.case_study
                        section = '1' if unit == '1' else topic_section
                    else:
                        topic_section = section
                    if section is None or topic is None:
                        refuse('the ask sits under no syllabus topic', ref)
                        continue
                    topic_id = topic_for(field, topic_section, topic)
                    if not topic_id:
                        refuse('the ask sits under no syllabus topic', ref)
                        continue

                    if ask.kind == 'banded' and (year, level, field) in ESSAY_PAPERS:
                        # An essay is priced whole on its unit; a lettered
                        # documents part priced by its split alone is not.
                        if key[2]:
                            made = tariff_only_card(P, year, level, field, key, ask,
                                                    section, topic_id, ref)
                        else:
                            made = essay_card(P, S, year, level, field, key, ask,
                                              section, topic_id, ref)
                        if isinstance(made, str):
                            refuse(made, ref)
                        else:
                            cards.append(made)
                        continue
                    if ask.kind == 'banded':
                        exclusions.append({
                            'ref': ref,
                            'reason': ('the scheme prints a marking ceiling '
                                       'for this ask and no answer content'),
                            'schemeEvidence': ask.evidence,
                        })
                        continue

                    if ask.kind == 'split':
                        cards.append(split_card(P, year, level, field, key, ask,
                                                section, topic_id, ref))
                        continue

                    points = [(lab, p, n) for lab, p, n in ask.points
                              if not GRID_WORDS.search(p)]
                    if len(points) != len(ask.points):
                        refuse('a marking point carried band-grid wording', ref)
                        continue
                    if not points:
                        refuse('the scheme states no marking points for this '
                               'ask', ref)
                        continue
                    if ask.total is None:
                        refuse('the scheme prints no tariff for this ask', ref)
                        continue

                    question = P.asks[key]
                    open_list = bool(OPEN_LIST.search(' '.join(ask.notes)))
                    rows = []
                    single = len(points) == 1
                    for i, (label, point, note) in enumerate(points, start=1):
                        row = {
                            'id': f'r-{i}', 'kind': 'point',
                            'verbatim': point,
                            # A one-line answer carries the ask's own printed
                            # marks. A listed answer does not: the scheme
                            # prices the ask and divides nothing.
                            'marks': ask.total if single else None,
                        }
                        if open_list and not single:
                            row['openList'] = True
                        notes = [x for x in (label, note) if x]
                        if notes:
                            row['contextNote'] = ' — '.join(notes)
                        rows.append(row)

                    card = {
                        'id': card_id(year, level, field, key),
                        'subjectId': 'history',
                        'level': LEVEL_WORD[level],
                        'year': year,
                        'section': section,
                        'topicId': topic_id,
                        'conceptId': concept_for(question),
                        'questionRef': ref,
                        'questionText': question,
                        'tariffModel': ({'kind': 'fixed'} if single
                                        else {'kind': 'questionTotal'}),
                        'totalMarks': ask.total,
                        'rows': rows,
                        'notes': (
                            f'{FIELDS[field]} field of study. The scheme '
                            f'prints {ask.notation!r} for this ask'
                            + ('.' if single else
                               ' and divides it between no marking point, so '
                               'the rows carry no marks of their own.')),
                    }
                    stem = P.stems.get(unit)
                    if unit == '1' and P.case_title:
                        stem = f'Case study: {P.case_title}'
                    if stem and len(stem) >= 20:
                        card['stem'] = stem
                    pages = (P.document_pages if unit == '1'
                             else [P.unit_pages[unit]])
                    card['sourceMaterial'] = source_material(
                        P, year, level, field, unit, pages,
                        'The documents' if unit == '1' else 'The extract',
                        'OFFICIAL DOCUMENTS' if unit == '1'
                        else 'OFFICIAL EXTRACT')
                    # The marks the SEC prints inside a Part A line ("Sods
                    # (3M) and saplings (3M)") are rows, not one claim
                    # (hist_rows.py).
                    card = split_priced(card)
                    # A row that is the scheme pricing an answer it does not
                    # print ("ONE valid reason", "ONE decision of the Synod of
                    # Thurles") says so, in the bank's fixed words.
                    for row in card['rows']:
                        if TARIFF_WORDING.match(row['verbatim']):
                            row['contextNote'] = ' — '.join(
                                x for x in (row.get('contextNote'), NO_PRINTED_ANSWER) if x)
                    cards.append(card)
    return (cards, exclusions, refused, examples, title_pairs, tariff_checks,
            extra_topic_checks, title_variants)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--exclusions', action='store_true',
                    help='rewrite exclusions/history.json from the schemes')
    ap.add_argument('--all', action='store_true')
    args = ap.parse_args()
    (cards, exclusions, refused, examples, title_pairs, tariffs,
     extras, title_variants) = build()

    if args.exclusions:
        os.makedirs(os.path.dirname(EXCLUSIONS), exist_ok=True)
        with open(EXCLUSIONS, 'w', encoding='utf-8') as fh:
            json.dump(exclusions, fh, ensure_ascii=False, indent=1)
            fh.write('\n')
        print(f'{len(exclusions)} exclusion(s) written to {EXCLUSIONS}',
              file=sys.stderr)
        return 0

    if args.report:
        from paper_census import census_subject
        census = census_subject('history')
        total = sum(p['leafCount'] for p in census['papers'])
        accounted = len(cards) + len(exclusions)
        print(f'{len(cards)} card(s) + {len(exclusions)} exclusion(s) = '
              f'{accounted} of {total} paper asks '
              f'({100 * accounted / total:.1f}%)')
        points = [c for c in cards if c.get('kind') != 'rubric']
        rows = sum(len(c['rows']) for c in points)
        fixed = sum(1 for c in points if c['tariffModel']['kind'] == 'fixed')
        print(f'{rows} marking rows; {fixed} fixed-tariff card(s), '
              f'{len(points) - fixed} questionTotal; '
              f'{len(cards) - len(points)} essay rubric card(s)')
        worst = min(title_pairs, key=lambda t: t[1]) if title_pairs else None
        print(f'topic-title pairing: {len(title_pairs)} pairs, weakest '
              f'{worst[0]} at {worst[1]:.2f}' if worst else 'no pairs')
        print(f'topic titles printed differently on the two documents: '
              f'{len(title_variants)}')
        for v in title_variants[:40 if args.all else 4]:
            print(f'   VARIANT {v}')
        print(f'paper/scheme tariff agreement: {tariffs["agree"]} agree, '
              f'{len(tariffs["disagree"])} disagree')
        for d in tariffs['disagree'][:20]:
            print(f'   DISAGREE {d}')
        print(f'extra Part A units: {len(extras)}, each filed under its '
              f"paper's own documents-question topic")
        for where, case in extras:
            print(f'   {where}: Section {case[0]} Topic {case[1]}')
        by_topic = collections.Counter(c['topicId'] for c in cards)
        for tid, n in sorted(by_topic.items()):
            print(f'   {tid:16} {n}')
        for reason, n in refused.most_common():
            print(f'   {n:4} REFUSED  {reason}')
            for e in examples[reason][:200 if args.all else 3]:
                print(f'             {e}')
        return 0

    json.dump(cards, sys.stdout, ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
