#!/usr/bin/env python3
"""Author every History ask the papers print and the schemes answer.

    python3 scripts/markbank/authoring/hist_all.py --report
    python3 scripts/markbank/authoring/hist_all.py > scripts/markbank/authored/history.json
    python3 scripts/markbank/authoring/hist_all.py --exclusions   # rewrite the ledger

Census-driven. Twenty papers — ten Later Modern and ten Early Modern, 2021-2025
at both levels — print 1,430 asks between them, and this walks that census
rather than choosing what to card.

WHAT IS CARDED, AND WHAT IS EXCLUDED
------------------------------------
History is the first subject in this bank where most of the paper cannot be
carded, and the reason is printed in the scheme rather than deduced.

*Carded.* The Documents-Based Question, and Ordinary Level's Part A. The
comprehension parts get a flat tariff list — "(a) To fight desegregation/
maintain segregation 5M" — and Part A gets five one-line answers at (6) apiece.
The comparison and criticism parts get the examiner's own model answer, priced
once on the ask with no per-point split.

*Excluded.* Every essay: Higher Level's Sections 2 and 3, Ordinary Level's
parts B and C, and the documents question's contextualisation part. The whole
scheme entry for one of those is a ceiling — "1. Max. CM = 60 Max. OE = 40" —
and there is nothing under it to lift. Each gets an entry in
exclusions/history.json carrying that printed line as its evidence, written by
--exclusions from the scheme itself so it cannot drift from what the SEC
prints.

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
from align import bag, score                                  # noqa: E402

YEARS = (2021, 2022, 2023, 2024, 2025)
LEVELS = ('hl', 'ol')
FIELD_KEYS = ('lm', 'em')
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
EXCLUSIONS = os.path.join(DIR, 'exclusions', 'history.json')

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

    for year in YEARS:
        for level in LEVELS:
            for field in FIELD_KEYS:
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

                    if ask.kind == 'banded':
                        exclusions.append({
                            'ref': ref,
                            'reason': ('the scheme prints a marking ceiling '
                                       'for this ask and no answer content'),
                            'schemeEvidence': ask.evidence,
                        })
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
        rows = sum(len(c['rows']) for c in cards)
        fixed = sum(1 for c in cards if c['tariffModel']['kind'] == 'fixed')
        print(f'{rows} marking rows; {fixed} fixed-tariff card(s), '
              f'{len(cards) - fixed} questionTotal')
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
