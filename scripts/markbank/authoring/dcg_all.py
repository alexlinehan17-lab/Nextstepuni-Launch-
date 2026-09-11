#!/usr/bin/env python3
"""Author every Design & Communication Graphics part the scheme prices.

    python3 scripts/markbank/authoring/dcg_all.py --report   # counts, refusals
    python3 scripts/markbank/authoring/dcg_all.py > scripts/markbank/authored/dcg.json

WHAT A DCG CARD IS. The scheme prices one drawing as a numbered sequence of
CONSTRUCTION STEPS, each with its own mark:

    (b) Dihedral Angle between surfaces A and B                          (20)
      (iii) X1Y1 parallel to line of intersection ......................... 6
      (iv)  Projection of planes and line of intersection on new X1Y1 ..... 4
      (v)   New X2Y2 perpendicular to line of intersection ................ 5
      (vi)  Projection of planes as lines and indicating dihedral angle ... 5

So a card is the priced unit, its rows are those steps at those marks, and the
shape is Applied Maths': ONE bounded row holding the whole ordered sequence, so
a student ticks the steps they actually drew. Nothing is apportioned and
nothing is averaged -- every number on a card is printed in the scheme, and
`dcg_scheme` has already checked that the steps sum to the part and the parts
sum to the question's own "Total =".

WHAT THE PAIRING RESTS ON (Law 4). The paper and the scheme agree on the
QUESTION -- both print "B-2", "C-4" -- and that is the only join taken for
free. Below it the scheme numbers its own way: 2021 Ordinary B-3 prices the
paper's part (b) as two unlettered heads and then letters the paper's part (c)
"(b)". So a unit is paired to the paper's ask by an order-preserving alignment
scored on the WORDS the two documents share, with the letter used to confirm
rather than to decide. `--report` prints, per sitting, how many pairings were
confirmed by wording, how many by the letter alone, how many were forced (one
ask, or one unit), and how many rested on order alone -- those are refused.

REFUSALS are named buckets, counted with a real example by `--report`.
"""
import argparse
import collections
import functools
import json
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

import cardlint                                              # noqa: E402
import dcg_paper as DP                                       # noqa: E402
import dcg_topics as DT                                      # noqa: E402
import paper_census as PC                                    # noqa: E402
from dcg_scheme import (CUE_FLOOR, DcgScheme, cue_score,     # noqa: E402
                        has_scheme)
from markbank_authoring import anyN                          # noqa: E402

SUBJECT = 'dcg'
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TOKEN = {'higher': 'hl', 'ordinary': 'ol'}
# MAX_LONG_OPTION_ROWS in types/markBank.ts: the most options any one bounded
# row may show. A unit longer than this is split by the scheme's OWN named
# groups, which is the only division of it the SEC printed.
MAX_STEPS_SHOWN = 16

# ------------------------------------------------------------------ pairing
def pair(units, leaves, texts):
    """[(unit, [leaf keys])] — the scheme's units against the paper's asks.

    Where BOTH documents letter the same parts in the same order -- 339 of the
    corpus's 396 questions -- the letters are two documents agreeing on the
    address, and that is the pairing. Nothing is inferred and nothing can
    drift: 2025 Ordinary A-2 letters "Locate points", "Draw curve" and "Focal
    points" against asks that letter (a), (b), (c), and scored on wording
    alone the first unit's words fit the THIRD ask just as well as its own.

    Where they do not agree, an order-preserving alignment scored on the words
    the two documents share: a unit may cover several asks, several units may
    divide one ask, but neither document's order is ever crossed.
    """
    m, n = len(units), len(leaves)
    if not m or not n:
        return []
    paper_letters = []
    for key in leaves:
        if key[2] and key[2] not in paper_letters:
            paper_letters.append(key[2])
    if m == len(paper_letters) and [u.letter for u in units] == paper_letters:
        return [(u, [k for k in leaves if k[2] == u.letter]) for u in units]

    # Every pairing the alignment makes has to PAY for itself. Scored on the
    # wording alone, spreading one unit over two asks always scores more than
    # placing it on one, because it adds another term -- 2025 Ordinary C-2's
    # "End view of Hyperbolic Paraboloid" was paired with the paper's (b) AND
    # its (c) for exactly that reason. So each pairing is charged CUE_FLOOR,
    # the same bar a pairing has to clear to count as confirmed at all, and a
    # pairing that does not clear it makes the alignment worse rather than
    # better. The LETTER is deliberately not scored here: this alignment only
    # runs where the two documents letter DIFFERENTLY, and there the scheme's
    # letter is the thing that is wrong.
    def fit(i, j):
        return cue_score(units[i].title, texts.get(leaves[j], '')) - CUE_FLOOR

    @functools.lru_cache(maxsize=None)
    def best(i, j):
        if i == m - 1:
            return sum(fit(i, k) for k in range(j, n)), 'down'
        if j == n - 1:
            return sum(fit(k, j) for k in range(i, m)), 'right'
        here = fit(i, j)
        # Ties are the rule rather than the exception here -- a unit that
        # matches nothing scores zero against every ask -- so the tie-break is
        # stated rather than left to whichever label sorts first. Advancing
        # BOTH is preferred: it is the reading where the two documents divide
        # the question the same way, which is what they do in 339 of the
        # corpus's 396 questions. Picked by string order instead, the 2025
        # Ordinary A-2 scheme's "Draw curve" was paired with "Locate the focal
        # points".
        options = [
            (here + best(i + 1, j + 1)[0], 2, 'diag'),
            (here + best(i + 1, j)[0], 1, 'right'),
            (here + best(i, j + 1)[0], 0, 'down'),
        ]
        value, _rank, move = max(options)
        return value, move

    out = collections.defaultdict(list)
    i = j = 0
    while True:
        out[i].append(leaves[j])
        if i == m - 1 and j == n - 1:
            break
        if i == m - 1:
            j += 1
            continue
        if j == n - 1:
            i += 1
            continue
        move = best(i, j)[1]
        if move == 'diag':
            i, j = i + 1, j + 1
        elif move == 'right':
            i += 1
        else:
            j += 1
    return [(units[k], out[k]) for k in range(m)]


# --------------------------------------------------------------- citations
def ref_for(year, level, section, q, covered, all_leaves):
    """The paper's own address for what one card holds."""
    head = f'{year} {level.upper()} Section {section} Q{q}'
    siblings = [k for k in all_leaves if k[0] == section and k[1] == q]
    if len(covered) == len(siblings):
        return head
    letters = []
    for key in covered:
        if key[2] and key[2] not in letters:
            letters.append(key[2])
    if not letters:
        return head
    if len(letters) > 1:
        return head + '(' + ')('.join(letters[:1]) + ')' + ''.join(
            f', ({x})' for x in letters[1:])
    letter = letters[0]
    under = [k for k in siblings if k[2] == letter]
    romans = [k[3] for k in covered if k[3]]
    if len(covered) == len(under) or not romans:
        return f'{head}({letter})'
    return (f'{head}({letter})(' + romans[0] + ')'
            + ''.join(f', ({r})' for r in romans[1:]))


# The parts list an assembly question prints beside its drawing. It is a
# TABLE -- "Part | Name | Qty." over ten rows -- and the text layer hands it
# back as one run of column cells: "Part Name Qty. Sliding Plunger End Cutter
# End Cap Handle Link Arm". The crop carries the table as the SEC set it; on
# the card it is a wall of two-word fragments after the ask has finished.
PARTS_LIST = re.compile(r'\s*\bPart\s+Name\s+Qty\.?.*$', re.I | re.S)


def _squash(text):
    return re.sub(r'[^a-z0-9]+', '', (text or '').lower())


def ask_text(covered, texts, parent):
    """The paper's own wording for every ask one card covers, in order."""
    parts = []
    for key in covered:
        text = ' '.join((texts.get(key) or '').split())
        if not text:
            continue
        parts.append(f'({key[3]}) {text}' if key[3] and len(covered) > 1
                     else text)
    joined = ' '.join(parts).strip()
    if not joined:
        joined = ' '.join((parent or '').split())
    return PARTS_LIST.sub('', joined).strip()


def card_id(year, level, section, q, covered, ordinal, many):
    letters = sorted({k[2] for k in covered if k[2]})
    tail = letters[0] if len(letters) == 1 else ''
    romans = sorted({k[3] for k in covered if k[3]})
    if len(romans) == 1 and len(letters) <= 1:
        tail += romans[0]
    base = f'dcg-{year}-{level}-{section.lower()}{q}{tail}'
    return f'{base}-{ordinal}' if many else base


# ----------------------------------------------------------------- figures
def figure_index():
    """The inspected question crops, keyed by the question they were cut FOR.

    One crop per QUESTION: the SEC prints the drawing once and every part of
    that question is answered from it. Read from the manifest a figure pass
    wrote, so a crop nobody has looked at is not in here to be bound.
    """
    figs = {}
    for name in ('figures.json', f'figures-{SUBJECT}.json'):
        path = os.path.join(ROOT, 'components', 'MarkBank', name)
        if not os.path.exists(path):
            continue
        with open(path, encoding='utf-8') as fh:
            manifest = json.load(fh)
        for key in manifest:
            m = re.fullmatch(r'dcg-(\d{4})-(HL|OL)-paper-sec([ABC])'
                             r'-q(\d)-art', key)
            if m:
                figs[(int(m.group(1)), m.group(2).lower(), m.group(3),
                      int(m.group(4)))] = key
    return figs


# ------------------------------------------------------------------ author
def repeats(unit):
    """Does this unit print the same step twice?

    The earthworks questions do, and so does every interpenetration priced by
    side: 2022 Ordinary B-2(b) prices "Projection from elevation", "Locate
    points in plan" and "Complete the plan" once for the ramp and again for
    the front cut. On one card that is three pairs of identical rows and a
    student cannot tell which is which -- but the SEC prints a HEADING over
    each set ("Interpenetration into ramp", "Front ramp cut"), so the card is
    cut where the scheme cut it instead.
    """
    texts = [s.text for s in unit.steps]
    return len(set(texts)) != len(texts)


def split_by_groups(unit):
    """A unit cut where the SEC's own headings cut it.

    Two units reach this. The assembly drawings are past the display cap --
    2021 Higher C-5 prices one sectional elevation in eighteen steps, under
    eight named component headings each carrying its own printed mark, "Main
    Body (14)", "Clamping Jaw (8)". And the earthworks and interpenetration
    questions price the SAME step once per section of the course, under a
    heading naming the section: "Earthworks between A and B (Level) –
    Embankment", "... – Cutting".

    The headings are the SEC's and so are the marks; where the heading carries
    no printed mark of its own the piece is worth the sum of the steps printed
    under it, which is arithmetic on printed numbers and not a tariff invented
    for it. Returns [(label, marks, [steps])] or None where there is nothing
    printed to split on.
    """
    groups = []
    for step in unit.steps:
        if not step.group:
            return None
        if not groups or groups[-1][0] != step.group:
            groups.append((step.group, []))
        groups[-1][1].append(step)
    if len(groups) < 2:
        return None
    out = []
    for label, steps in groups:
        if len(steps) > MAX_STEPS_SHOWN:
            return None
        out.append((label, sum(s.marks for s in steps), steps))
    return out


def author(bind_figures=True):
    census = PC.census_subject(SUBJECT)
    figures = figure_index() if bind_figures else {}
    cards, refused, examples = [], collections.Counter(), collections.defaultdict(list)
    verdicts, stats = [], []

    for paper in census['papers']:
        year, level = paper['year'], paper['level']
        P = DP.load(year, level, SUBJECT)
        leaves = {tuple(leaf['key']) for leaf in paper['leaves']}
        texts = {ask.key: ask.full_text for ask in P.asks()}
        assert set(texts) == leaves, \
            f'{year} {level}: the authored leaf set is not the census leaf set'
        if not has_scheme(year, level, SUBJECT):
            for key in sorted(leaves):
                refused['no marking scheme is published for this sitting'] += 1
            continue
        S = DcgScheme(year, level, SUBJECT)
        wording = letter_only = forced = order_only = 0

        for qkey in sorted(P.questions):
            section, q = qkey
            qq = P.questions[qkey]
            unit_list = S.questions[qkey].units if qkey in S.questions else []
            mine = sorted(k for k in leaves if k[0] == section and k[1] == q)
            if not unit_list:
                for key in mine:
                    ref = ref_for(year, level, section, q, [key], leaves)
                    refused['the scheme prices nothing under this question'] += 1
                    examples['the scheme prices nothing under this question'] \
                        .append(f'{ref}')
                continue
            pairing = pair(unit_list, mine, texts)
            per_address = collections.Counter(
                tuple(cov) for _u, cov in pairing)
            ordinal = collections.Counter()
            # Two units covering DIFFERENT spans of one question can still
            # land on the same id: a span crossing two letters is keyed by the
            # question alone. Counted over the whole question, so the suffix
            # is decided by how many cards the question makes and not by how
            # many share one address.
            bases = collections.Counter(
                card_id(year, level, section, q, cov, 1, False)
                for _u, cov in pairing)

            for index, (unit, covered) in enumerate(pairing, 1):
                ref = ref_for(year, level, section, q, covered, leaves)
                base = card_id(year, level, section, q, covered, 1, False)
                many = per_address[tuple(covered)] > 1
                ordinal[base] += 1
                cid = card_id(year, level, section, q, covered,
                              ordinal[base], bases[base] > 1)

                def note(reason, detail=''):
                    verdicts.append({'year': year, 'level': level, 'ref': ref,
                                     'reason': reason})
                    refused[reason] += 1
                    if len(examples[reason]) < 80:
                        examples[reason].append(f'{ref}: {detail[:80]}')

                # --- Law 4: how was this unit paired to the paper's ask?
                score = max(cue_score(unit.title, texts.get(k, ''))
                            for k in covered)
                if len(unit_list) == 1 or len(mine) == 1:
                    forced += 1
                elif score >= CUE_FLOOR:
                    wording += 1
                elif unit.letter and any(unit.letter == k[2] for k in covered):
                    letter_only += 1
                else:
                    order_only += 1
                    note('the pairing of this priced unit to a printed ask '
                         'rests on order alone', unit.title)
                    continue

                if not unit.steps:
                    note('the scheme prices this unit but states no step '
                         'under it', unit.title)
                    continue
                if not unit.marks:
                    note('the scheme prints no tariff for this unit',
                         unit.title)
                    continue

                question = ask_text(covered, texts,
                                    P.parent_text(section, q, covered[0][2]))
                if len(question) < 12:
                    note('the paper prints no ask at this address', unit.title)
                    continue

                pieces = [(None, unit.marks, unit.steps)]
                if len(unit.steps) > MAX_STEPS_SHOWN or repeats(unit):
                    split = split_by_groups(unit)
                    if not split:
                        note('the scheme states the same priced step twice, '
                             'or more than '
                             f'{MAX_STEPS_SHOWN} steps, and names no groups '
                             'to split them by', unit.title)
                        continue
                    pieces = split

                stem = ' '.join((qq['stem'] or '').split())
                # A question the paper asks WHOLE has no ask of its own: its
                # leaf text IS the stem, so the card would print the same
                # paragraph twice, once above the other.
                if stem and _squash(stem) in _squash(question):
                    stem = ''
                topic, why = DT.topic_for(section, qq['option'],
                                          ' '.join([stem, question, unit.title]
                                                   + [s.text for s in unit.steps]))
                if topic is None:
                    note('files under no syllabus heading', why)
                    continue
                figure = figures.get((year, level, section, q))
                if cardlint.NAMES_LETTERS.search(f'{stem} {question}') \
                        and not cardlint.INVITES_DRAWING.search(question):
                    note('names a lettered part this author cannot decode',
                         question)
                    continue
                if cardlint.SCHEME_LEAK.search(f'{stem} {question}'):
                    note('the paper text carries scheme metadata', question)
                    continue

                for piece_no, (label, marks, steps) in enumerate(pieces, 1):
                    options = [s.text for s in steps]
                    step_marks = [s.marks for s in steps]
                    if sum(step_marks) != marks:
                        note('the priced steps do not sum to the mark the '
                             'scheme prints for this unit', unit.title)
                        continue
                    if any(not o for o in options):
                        note('the scheme states no words for one of the '
                             'priced steps', unit.title)
                        continue
                    piece_ref = ref
                    piece_id = cid
                    title = label or unit.title
                    if label or many:
                        piece_ref = f'{ref} — {title}'
                    if label:
                        piece_id = f'{cid}-{piece_no}'
                    rows = [anyN(
                        f'{piece_id}-r1', options[0], marks, len(options),
                        step_marks[0], options,
                        'The scheme prices this drawing step by step: '
                        + ', '.join(str(m) for m in step_marks)
                        + f' — {marks} marks in all, in the order the scheme '
                          'sets them out.',
                        steps=step_marks if len(set(step_marks)) > 1 else None)]
                    cards.append({
                        'id': piece_id,
                        'topicId': topic,
                        'conceptId': DT.concept_for(topic),
                        'level': LEVEL_WORD[level],
                        'year': year,
                        'subjectId': SUBJECT,
                        'section': section,
                        'questionRef': piece_ref,
                        'questionText': question,
                        'stem': stem,
                        'figureKey': '',
                        'questionFigureKey': figure or '',
                        'labelKey': [],
                        'tariffModel': {'kind': 'fixed',
                                        'notation': f'({marks})'},
                        'totalMarks': marks,
                        'rows': rows,
                        'notes': (f'The scheme heads this {title!r} and prices '
                                  f'it at {marks}. '
                                  'Construction lines must be shown on all '
                                  'solutions, and the scheme notes that other '
                                  'valid solutions are acceptable and are '
                                  'marked accordingly.'),
                    })
        stats.append((year, level, wording, letter_only, forced, order_only))

    return cards, refused, examples, verdicts, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--verdicts')
    args = ap.parse_args()

    cards, refused, examples, verdicts, stats = author()

    if args.verdicts:
        with open(args.verdicts, 'w', encoding='utf-8') as fh:
            json.dump(verdicts, fh, indent=1)
        print(f'wrote {args.verdicts}: {len(verdicts)} refusals')
    if args.report:
        census = PC.census_subject(SUBJECT)
        total = sum(p['leafCount'] for p in census['papers'])
        print(f'{len(cards)} card(s) against {total} census asks')
        print()
        print("PAIRING (Law 4): how each sitting's priced units were joined")
        for year, level, w, lo, f, oo in stats:
            n = w + lo + f + oo
            print(f'  {year} {level.upper()}: {w:3} confirmed by wording, '
                  f'{lo:3} by the letter alone, {f:3} forced (one ask or one '
                  f'unit), {oo:3} refused for resting on order alone'
                  f'   [{100 * (w + f) // max(n, 1)}%]')
        print()
        for reason, n in refused.most_common():
            print(f'  {n:4} REFUSED  {reason}')
            for e in examples[reason][:80 if args.all else 3]:
                print(f'            {e}')
        return 0
    print(json.dumps(cards, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
