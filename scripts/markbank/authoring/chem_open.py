#!/usr/bin/env python3
"""Chemistry parts the deck had not carded, lifted through chem_scheme.

    python3 scripts/markbank/authoring/chem_open.py            # emit JSON
    python3 scripts/markbank/authoring/chem_open.py --report   # what was skipped

reconcile listed 123 open asks after the census was corrected. Every one of
them was read here beside its scheme answer, and this file carries the ones
that pass three tests at once:

  * the PAPER states the ask on its own, without pointing at a printed
    reaction scheme, table or graph the card would have to carry and does not,
  * the SCHEME states an answer in words the text layer recovers intact, and
  * the scheme prints a tariff that can be read one way only (chem_scheme's
    tariff(), which refuses rather than guesses).

The topic on each card was assigned BY HAND. chem_topics.py suggests one and
is measured at 54% against the cards already in the deck, which is not good
enough to file by: whether a part is about the EXPERIMENT or about the
CHEMISTRY IN it is a judgement its wording does not carry. Every topic below
was chosen by reading the ask.

What is deliberately NOT here, and why, so a later pass can pick it up:

  drawings          Q asks for a structure, a dot-and-cross diagram or a
                    completed nuclear equation. The scheme answers with
                    artwork and the text layer returns its scattered labels --
                    "H H H H H H" for a benzene ring, "/ 86 84 2 222 218 4"
                    for an alpha decay. These are croppable as solution
                    figures, which is how Economics carded its worked
                    calculations, and they belong to a figure pass.
  scheme-referenced Q names a conversion or a curve lettered on a figure at
                    the head of its question -- "Identify the elimination
                    reaction in the scheme", "of the first four alkanes". The
                    answer ("D") means nothing without the figure bound.
  no printed tariff 24 parts whose answer is plain but whose marks are only
                    printed against the group. NEVER GUESS A TARIFF.
  font-mangled      the 2023 equation font maps several glyphs to one
                    codepoint; see markbank glyph repair.

2022 HL Q4(b) was carded here and then taken out. Its answer is clean and
priced at 6, but the ask opens "The diagram shows the origin of one of the
lines in the Balmer series", and no crop of that diagram exists -- the only
two figures extracted from the page carry Q4(f)'s diamond and Q4(k)'s
skeletal formula. card lint caught it as a ghost figure, which is what that
check is for.

2025 OL Q8(a)(iii) and (iv) were carded here and then taken out again. Both
answers are clean and priced -- "polyethene", "ethanal / CH₃CHO" -- but
chem_2025_ol.py had already refused them, and its reason still holds: the ask
points at the reaction scheme at the head of Q8, the only crops of that page
are marked truncated, and a card that asks a student to read a diagram it
cannot show is worse than no card. It belongs to the same figure pass.

Emitted per sitting by the chem_<year>_<level>_open.py wrappers, which is the
filename merge.py looks for.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author, Refused  # noqa: E402

# (year, level) -> [(q, letter, roman, topic, concept, note)]
# The note goes in the card's contextNote where the ask needs one to stand on
# its own; None where the paper's wording is already self-contained.
GRAPH = ('The paper sets Q3(b)(i) to (iii) as a numbered list under one cue: '
         '(i) ends "Plot a graph ... From your graph", and (ii) and (iii) '
         'complete that sentence. Page 5 of the 2022 Ordinary Level paper '
         'prints this part exactly as the card carries it.')

WORK = {
    (2021, 'ol'): [
        (8, 'b', 'ii', 'chem-2-4', 'substances-added-to-ethene-in-two-addition-reactions',
         None,
         'The paper prints "A and B are two other addition reactions of ethene." '
         'as part of the ask; the reactions are named in the scheme printed above '
         'it and the card needs no figure to be answerable.'),
        (11, 'a', 'iii', 'chem-1-2', 'metal-with-the-same-occupied-energy-levels-as-boron',
         None, None),
        (11, 'b', 'iii', 'chem-3-3', 'principle-named-when-an-equilibrium-is-disturbed',
         None, None),
    ],
    (2022, 'hl'): [
        (5, 'd', 'i', 'chem-1-2', 'definition-of-radioactivity', None, None),
        (5, 'd', 'iii', 'chem-1-2', 'why-lead-cannot-be-changed-to-gold-chemically',
         None,
         'The paper sets this as one sentence ending "(12)", which is the mark '
         'for the group. Page 9 of the 2022 Higher Level paper prints it as the '
         'card carries it.'),
        (9, 'd', 'i', 'chem-3-4', 'volume-of-naoh-that-neutralised-solution-a', None, None),
        (9, 'd', 'ii', 'chem-3-4', 'molar-concentrations-of-four-titrated-solutions',
         None, None),
        (11, 'a', 'vi', 'chem-3-5', 'reducing-agent-in-a-manganese-bismuth-reaction',
         'The unbalanced equation for the reaction is set out at the head of '
         'Q11(a) on the paper.',
         'The trailing "(25)" is the mark for the whole of Q11(a). Page 17 of '
         'the 2022 Higher Level paper prints the ask as the card carries it.'),
    ],
    (2022, 'ol'): [
        (3, 'b', 'ii', 'chem-3-2', 'time-to-collect-50-cm3-of-oxygen',
         'Part (i) sets the cue this ask completes: "Plot a graph (on graph '
         'paper) of volume of O2 (y-axis) versus time. From your graph".',
         GRAPH),
        (3, 'b', 'iii', 'chem-3-2', 'average-rate-of-reaction-over-the-first-25-minutes',
         'Part (i) sets the cue this ask completes: "Plot a graph (on graph '
         'paper) of volume of O2 (y-axis) versus time. From your graph".',
         GRAPH),
        (9, 'b', 'iii', 'chem-3-5', 'reducing-agent-in-a-redox-reaction',
         'The redox equation is printed above the ask in Q9(b).',
         'The trailing "(12)" is the mark for the group. Page 13 of the 2022 '
         'Ordinary Level paper prints the ask as the card carries it.'),
        (10, 'c', 'iii', 'chem-1-4', 'number-of-molecules-in-a-quantity-of-oxygen',
         None, None),
        (11, 'c', 'ii', 'chem-4-3', 'purpose-of-the-glass-wool-plug-in-column-chromatography',
         'C is the column chromatography apparatus of Q11(c).', None),
        (11, 'c', 'iii', 'chem-4-3', 'stationary-phase-in-a-chromatographic-separation',
         'The scheme answers for each of the three separations a candidate may '
         'have drawn: P paper, T thin-layer, C column.', None),
        (11, 'c', 'iv', 'chem-4-3', 'direction-the-mobile-phase-moves',
         'The scheme answers for each of the three separations a candidate may '
         'have drawn: P paper, T thin-layer, C column.', None),
        (11, 'c', 'vi', 'chem-4-3', 'component-carried-fastest-by-the-mobile-phase',
         'The scheme answers for each of the three separations a candidate may '
         'have drawn: P paper, T thin-layer, C column.', None),
        (11, 'c', 'vii', 'chem-4-3',
         'result-when-every-component-is-insoluble-in-the-mobile-phase',
         'The scheme answers for each of the three separations a candidate may '
         'have drawn: P paper, T thin-layer, C column.',
         'The trailing "(25)" is the mark for the whole of Q11(c). Page 19 of '
         'the 2022 Ordinary Level paper prints the ask as the card carries it.'),
    ],
    (2021, 'ol', 'FIG'): [
        (5, 'd', 'ii', 'chem-2-1', 'dot-and-cross-diagram-for-an-oxygen-molecule',
         'The scheme accepts either a shell diagram or a Lewis structure; both '
         'are printed side by side in its own answer.',
         'The paper prints the whole ask on one line including its own '
         'parenthetical, "(Electrons in the first main energy levels need not '
         'be shown.)". Page 12 of the 2021 Ordinary Level paper carries it as '
         'the card does.',
         'chemistry-2021-OL-scheme-q5d-ii'),
    ],
    (2024, 'hl', 'FIG'): [
        (5, 'b', 'vi', 'chem-1-2', 'shape-of-a-p-orbital', None,
         'The trailing "(29)" is the mark for the whole of Q5(b). Page 9 of '
         'the 2024 Higher Level paper prints the ask as the card carries it.',
         'chemistry-2024-HL-scheme-q5b-vi'),
    ],
    (2024, 'ol'): [
        (10, 'a', 'iii', 'chem-1-4', 'molecular-formula-from-a-relative-molecular-mass',
         None, None),
    ],
    # ── parts unlocked by the figure pass ─────────────────────────────────
    # Each of these points at something printed. chem_question_figures.py
    # cropped it from the paper and it is bound to the card, so the ask can be
    # answered from what the card shows.
    (2022, 'hl', 'FIGPASS'): [
        (4, 'b', None, 'chem-1-2', 'why-a-photon-is-emitted-in-the-balmer-series',
         None, None, 'chemistry-2022-HL-paper-q4-fig0'),
    ],
    (2022, 'ol', 'FIGPASS'): [
        (6, 'c', 'ii', 'chem-2-4', 'identifying-the-aromatic-hydrocarbons-in-a-table',
         'A to E are the five structures drawn in the table at the head of Q6.',
         'The block ends "(12) H H B C C H H" -- the group mark followed by '
         'atom labels the text layer lifted out of the drawn structures beside '
         'it. Page 7 of the 2022 Ordinary Level paper prints the ask itself as '
         'the card carries it.',
         'chemistry-2022-OL-paper-q6-fig0'),
    ],
    (2023, 'hl', 'FIGPASS'): [
        (8, 'a', 'ii', 'chem-2-4', 'identifying-the-elimination-reaction-in-a-scheme',
         None,
         'The trailing "(8)" is the mark for the whole of Q8(a). Page 9 of the '
         '2023 Higher Level paper prints the ask as the card carries it.',
         'chemistry-2023-HL-paper-q8-fig0'),
        (8, 'c', 'ii', 'chem-2-2', 'geometry-change-when-ethene-is-polymerised',
         None,
         'The trailing "(12)" is the mark for the whole of Q8(c). Page 9 of the '
         '2023 Higher Level paper prints the ask as the card carries it.',
         'chemistry-2023-HL-paper-q8-fig0'),
        (8, 'd', 'i', 'chem-2-4', 'inorganic-product-of-a-free-radical-substitution',
         None, None, 'chemistry-2023-HL-paper-q8-fig0'),
        (8, 'd', 'ii', 'chem-2-4', 'significance-of-traces-of-butane-in-a-substitution',
         None,
         'The trailing "(6)" is the mark for the whole of Q8(d). Page 9 of the '
         '2023 Higher Level paper prints the ask as the card carries it.',
         'chemistry-2023-HL-paper-q8-fig0'),
        (8, 'e', 'i', 'chem-2-2', 'which-graph-shows-the-boiling-points-of-the-alkanes',
         'Q8(e) sets the cue these asks complete: "Deduce which of A, B, C or '
         'D is a graph of the boiling points".',
         'The paper sets (i) and (ii) as a two-item list under that one cue, so '
         'each begins in lower case. Page 9 of the 2023 Higher Level paper '
         'prints this part exactly as the card carries it.',
         'chemistry-2023-HL-paper-q8-fig1'),
        (8, 'e', 'ii', 'chem-2-2', 'which-graph-shows-the-boiling-points-of-the-aldehydes',
         'Q8(e) sets the cue these asks complete: "Deduce which of A, B, C or '
         'D is a graph of the boiling points".',
         'The paper sets (i) and (ii) as a two-item list under that one cue, so '
         'each begins in lower case. Page 9 of the 2023 Higher Level paper '
         'prints this part exactly as the card carries it.',
         'chemistry-2023-HL-paper-q8-fig1'),
        (8, 'e', 'iii', 'chem-2-2', 'why-boiling-point-rises-with-carbon-number',
         None,
         'The paper runs (iii) on into the lead-in for (iv) and (v), "Account '
         'for the significant difference in the boiling points". Page 9 of the '
         '2023 Higher Level paper prints both sentences under (iii) as the '
         'card carries them.',
         'chemistry-2023-HL-paper-q8-fig1'),
    ],
    (2025, 'ol', 'FIGPASS'): [
        (8, 'a', 'iii', 'chem-2-4', 'name-of-the-polymer-formed-from-ethene',
         'P is the polymer drawn at the foot of the Q8 reaction scheme, shown '
         'as two repeating units.',
         'The scheme is now cropped and bound, which is what chem_2025_ol.py '
         'was waiting on when it refused this part.',
         'chemistry-2025-OL-paper-q8-fig0'),
        (8, 'a', 'iv', 'chem-2-4', 'carbonyl-compound-in-a-reaction-scheme',
         None,
         'The trailing "(18)" is the mark for the whole of Q8(a), and the '
         'scheme the ask points at is now bound to the card.',
         'chemistry-2025-OL-paper-q8-fig0'),
    ],
    (2023, 'ol'): [
        (3, 'a', 'ii', 'chem-4-3', 'determining-the-concentration-of-dissolved-solids',
         None, None),
    ],
}


def scattered(points):
    """Artwork the text layer has broken up, rather than an answer in words.

    The signal is MANY very short marking points, and only that. Two other
    tests were tried and both rejected real answers:

      * the proportion of DIGITS -- but "20.0 cm³" and "1.0 × 10²³ molecules
        O₂" are mostly numeric and are exactly what the scheme prints;
      * a token REPEATED four times or more -- which is the shape of a drawn
        structure's labels ("H H H H H H"), and also the shape of the answer
        to 2022 HL Q4(b), where "electron" opens all three alternatives, and
        of "A: 1.0 M B: 0.5 M C: 1.0 M D: 1.0 M", where the unit repeats.

    A drawn structure or a completed equation arrives as a column of
    fragments -- "222", "Rn →", "218", "Po + He", "4" -- and it is their
    shortness, not their content, that gives them away.

    The guard is here as well as in the selection
    because a part boundary can move: 2022 HL Q5(d)(i) is "Define
    radioactivity", and the nuclear equation belonging to (d)(ii) underneath
    it has no marker line of its own to close (d)(i) on.
    """
    if not points:
        return True
    return sum(1 for p in points if len(p.strip()) <= 6) >= 3


def emit(only=None):
    """(cards, refusals) for one sitting, or for every sitting when None."""
    cards, refused = [], []
    for sitting, items in sorted(WORK.items(), key=lambda kv: kv[0][:2]):
        year, level = sitting[0], sitting[1]
        if only and (year, level) != only:
            continue
        A = Author('chemistry', year, level)
        table = A._source('table')
        for item in items:
            q, letter, roman, topic, concept, note, checked = item[:7]
            figure = item[7] if len(item) > 7 else None
            rows = table.points(q, letter, roman)
            tariff = table.tariff(q, letter, roman, rows=len(rows))
            keep = list(range(len(rows)))
            try:
                if not rows:
                    raise Refused('the scheme states nothing at this key')
                if not tariff:
                    raise Refused('the scheme prints no tariff that reads one way')
                # A SOLUTION crop is the scheme's own drawing and is itself
                # the answer, so the card's rows are the criteria printed
                # beside it. A QUESTION crop is the paper's diagram and is the
                # stimulus, so the rows are the ordinary answer -- which is
                # often a single letter read off that diagram ("D").
                if figure and '-scheme-' in figure:
                    # On a card carrying the scheme's own DRAWING, the drawing
                    # is the answer and the rows are the CRITERIA printed
                    # beside it. The picture's own scattered labels are not
                    # criteria: 2021 OL Q5(d)(ii) returns "x x", "/", "O", "O"
                    # before it returns "two bond pairs shown". Keep only what
                    # reads as a sentence.
                    keep = [i for i, r in enumerate(rows) if len(r.split()) >= 3]
                    rows = [rows[i] for i in keep]
                    if not rows:
                        raise Refused('the scheme states no criteria for the '
                                      'drawing, so there is nothing to claim')
                elif scattered(rows) and not figure:
                    raise Refused('the answer is artwork the text layer scattered')
                # One mark per marking point. The scheme prints the split
                # itself where it can -- "A: bromine (3)", "B: hydrogen
                # chloride (3)" -- and where it prints only the total, that
                # total over the printed COUNT of points is the one division
                # the rules allow. Anything that does not divide is refused.
                if len(rows) == 1:
                    marks = [tariff]
                elif tariff % len(rows) == 0:
                    marks = [tariff // len(rows)] * len(rows)
                else:
                    raise Refused(f'tariff {tariff} does not divide over '
                                  f'{len(rows)} marking point(s)')
                A.card(q, letter, roman, topic=topic, concept=concept,
                       source='table', use=keep,
                       marks=marks, tariff='fixed', context=note,
                       checked=checked, figure=figure)
            except Refused as exc:
                refused.append(f'{year} {level.upper()} Q{q}'
                               + (f'({letter})' if letter else '')
                               + (f'({roman})' if roman else '') + f': {exc}')
        cards.extend(A.cards)
    return cards, refused


def main():
    report = '--report' in sys.argv
    cards, refused = emit()
    if report:
        print(f'{len(cards)} card(s) emitted, {len(refused)} refused')
        for r in refused:
            print(f'   REFUSED {r}')
        return 0
    for r in refused:
        print(f'REFUSED {r}', file=sys.stderr)
    print(json.dumps(cards, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
