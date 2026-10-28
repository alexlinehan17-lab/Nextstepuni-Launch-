#!/usr/bin/env python3
"""2011 Higher Level Chemistry, carded part by part from the printed paper and scheme.

    python3 scripts/markbank/authoring/chem_2011_hl.py              # cards as JSON on stdout
    python3 scripts/markbank/authoring/chem_2011_hl.py --review     # the review ledger
    python3 scripts/markbank/authoring/chem_2011_hl.py --exclusions # [] -- nothing is excluded
    python3 scripts/markbank/authoring/chem_apply_print.py 2011 hl

No 2011 Higher card existed before the audit, so every card here is new. Every
question text, stem and lead-in is the PAPER's print of its part and every
marking point is the SCHEME's answer closed by its own mark cell; a calculation
is its first route's steps where the text layer carries them cleanly, and the
scheme's own print of the working (and of any other route) is the card's figure.

Reader (chem_print, gated to 2011 HL). The paper sets the heads of Questions 8,
10 and 11 in one run with their words ("8. Answer the questions below ..."), as
the 2013 Higher paper does, and Q11(c)'s choice as "Answer either part A or part
B."; unread, the paper reader found Questions 1-7 only and B's romans fell on A's
(OLD_OL_HEADS and PAPER_ALT_LETTERS joined). The scheme's running footer "ATAL
Chemistry Marking Scheme 2011" and its head "SECTION B" were filed as answers of
the part before them: dropped (the 2011 HL block of Printed). The census reads
Q11(c)'s alternatives the same way (paper_census.chemistry_choice_parts): 69 -> 73
asks, the paper's own.

Romans the paper sets inside one sentence are one census ask and a card per
scheme cell, each showing the sentence with a "For (i)."-style note: Q3(b),
Q5(a), Q5(c), Q7(b) and Q10(c)'s definitions; Q1(e), Q1(f), Q7(a) and Q9(b) set
their romans on lines of their own completing one sentence, and are carded the
same way. Where a letter prints a mark after each of several asks, or its asks
outrun a card's five rows, each run is a card cited with what it holds (Q1(b),
Q3(f), Q7(b), Q7(d), Q8(a), Q9(a), Q10(a), Q10(b), Q10(c), Q11(c)B). Asks the
paper sets before a letter's first roman are the letter's own card (Q10(b),
Q11(a), Q11(c)B); the ask set after Q9(b)(iii) is a card cited "— after (iii)".
Q4(k) and Q11(c) offer alternative parts A and B.

The scheme prices Q10(b)'s calculations under "CALC:" with no romans: (i)'s is
the first ("6.6 hours"), (ii)'s the second ("112.5 mg/100 ml blood"), read from
its own lines. The paper underlines words in Q2(a) ("fully labelled") and Q10(a)
("with and without"), which no text layer carries: those cards take the paper's
own print as their question, as do the parts whose equation the text layer
cannot carry (Q6(e)'s state symbols, Q9(a)'s drawn equilibrium arrow). Q9(b)'s
equation, its arrow drawn, is the paper's crop, its labels kept out of the text.

The scheme sets its fractions, square roots, log formulas and the Q8(a), Q9(a),
Q10(c) and Q11(c)B equations in Cambria Math glyphs the text layer maps into the
wrong Unicode blocks: those steps are rows lifted from the words around them,
each with a note saying what the scheme prints, and its own print is the card's
figure.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_print import Cards, Printed, Refused, anyN, display, make_audit, MAX_OPTIONS, point, read_lines, tidy  # noqa: E402

P = Printed(2011, 'hl', figures=True)
C = Cards(P)
FIG = 'chemistry-2011-HL-'
S = FIG + 'scheme-'
SPLIT = ('The scheme prices these points together as {} without saying which point earns which '
         'part, so no per-point value is shown.')


def k(*parts):
    q, letter, roman = (list(parts) + [None, None, None])[:3]
    return (q, letter, roman, None)


def ka(q, letter, roman, alt):
    return (q, letter, roman, alt)


def print_question(suffix):
    """The paper's own print of the part as the card's question."""
    C.cards[-1]['questionFigureKey'] = FIG + suffix


def shown(text, i=0):
    """An examiner's direction the student needs while self-marking, set on a
    row's note: a card's own notes are the author's record and never ship."""
    r = C.cards[-1]['rows'][i]
    r['contextNote'] = tidy(' '.join(x for x in (r.get('contextNote') or '', text) if x))


def cells(key):
    return [it.cell for it in P.items(key)]


def lift(rid, text, marks, note=''):
    return C.lifted(rid, display(text).strip(), marks, note)


def menu_row(rid, options, claim, note, per=None, steps=None, total=None):
    """An "any N" row: options lifted from the scheme, each refused unless the gate finds it."""
    opts = [C.lifted('x', display(o).strip(), None)['verbatim'] for o in options]
    if per is None:
        # Inside an orderedSplit: the whole is priced, the options are not.
        return {'id': rid, 'kind': 'anyN', 'verbatim': opts[0], 'marks': None, 'openList': True,
                'contextNote': note, 'group': {'claimMax': claim, 'options': opts}}
    return anyN(rid, opts[0], total, claim, per, opts, note, steps=steps)


_RAW = read_lines(P.scheme_path)


def raw(page, y0, y1, x0=0, x1=600):
    """The scheme's own printed lines inside a region, joined (a label or an
    examiner's note the cue reader splits off or welds to an answer)."""
    return tidy(' '.join(display(l.text) for l in _RAW if l.page == page and y0 <= l.y0 and l.y1 <= y1
                         and x0 <= l.x0 and l.x1 <= x1))


def rows(page, y0, y1, x0=0, x1=600):
    """The scheme's printed rows inside a region, each read left to right. A run
    set in a script ("•) /" after "(CH₃") starts a few points above the words of
    its row but ends with them: rows are told apart by where their runs END."""
    ls = [l for l in _RAW if l.page == page and y0 <= l.y0 and l.y1 <= y1 and x0 <= l.x0 and l.x1 <= x1]
    out = []
    for l in sorted(ls, key=lambda m: m.y1):
        if out and abs(out[-1][0] - l.y1) <= 3:
            out[-1][1].append(l)
        else:
            out.append([l.y1, [l]])
    return tidy(' '.join(display(m.text) for _y, grp in out for m in sorted(grp, key=lambda m: m.x0)))


def traced(text):
    """A string quoted from the scheme in a note, checked against the scheme."""
    if not P.traceable(text):
        raise Refused(f'"{text}" is not in the 2011 hl scheme')
    return text


def cut(text, at):
    """`text` split where `at` begins (the paper's print, cut between two asks
    it sets in one run)."""
    i = text.index(at)
    return text[:i].strip(), text[i:].strip()


def split_asides(text):
    """(the answer, its examiner's asides): the asides the scheme sets inside an
    answer's line lifted out."""
    from chem_print import INLINE_ASIDE
    asides = INLINE_ASIDE.findall(text)
    return tidy(INLINE_ASIDE.sub(' ', text)), [a.strip() for a in asides]


_q4 = P.items(k('4'))
assert len(_q4) == 1 and _q4[0].cell is None, _q4
Q4_NOTE = 'The scheme: "' + _q4[0].text + '"'
if not P.traceable(_q4[0].text):
    raise Refused('Q4 note is not in the scheme')

WITHDRAWN = {}
EXCLUDED = []

# ── Q1 Hypochlorite in bleach by an iodine/thiosulfate titration ─────────────
# The two equations (paper page 2, y 174-191 and 321-338) set each charge after
# its ion; set where the page prints them.
Q1_STEM = C.context(k('1', 'a'))
assert Q1_STEM.startswith('A chemist determined the concentration of a bleach solution') and \
    Q1_STEM.endswith('The following reaction took place in the conical flask. ClO – + 2I – + 2H⁺ → Cl – + I₂ + H₂O'), \
    Q1_STEM
Q1_STEM = P.rearranged(Q1_STEM, 'ClO – + 2I – + 2H⁺ → Cl – + I₂ + H₂O', 'ClO⁻ + 2I⁻ + 2H⁺ → Cl⁻ + I₂ + H₂O')
Q1_TITR = P.lead(k('1', 'b'))
assert Q1_TITR.startswith('The solution in the conical flask was next titrated') and \
    Q1_TITR.endswith('2S₂O₃ 2– + I₂ → S₄O₆ 2– + 2I –'), Q1_TITR
Q1_TITR = P.rearranged(Q1_TITR, '2S₂O₃ 2– + I₂ → S₄O₆ 2– + 2I –', '2S₂O₃²⁻ + I₂ → S₄O₆²⁻ + 2I⁻')
Q1_LATER = Q1_STEM + ' ' + Q1_TITR
# (a): DESCRIBE, "ANY FOUR: (4 × 3)" over five points (scheme page 5, y 84-185).
_any4 = raw(5, 172, 185, 440)
assert _any4 == 'ANY FOUR: (4 × 3)' and cells(k('1', 'a')) == ['[4 × 3]'], _any4
C.menu([k('1', 'a')], 'chem-4-1', 'diluting-a-sample-to-500-cm3', stem=Q1_STEM, note='"' + _any4 + '".')
# (b): COLOUR (3), printed (3); EXCESS (2 × 3), printed (6): a card each.
Q1B_COL, Q1B_EXC = cut(P.ask(k('1', 'b')), 'Give two reasons')
assert Q1B_COL.endswith('in the conical flask?') and Q1B_EXC == 'Give two reasons why excess potassium iodide was used.'
_q1b = P.items(k('1', 'b'))
assert [it.cell for it in _q1b] == ['[3]', '[2 × 3]'], _q1b
C.add([k('1', 'b')], 'chem-4-1', 'colour-of-iodine-released-from-the-bleach', [
    lift('r-1', _q1b[0].text, 3, 'COLOUR.')], qtext=Q1B_COL, stem=Q1_STEM, cid='q1-b-colour',
    ref_suffix='colour developed')
_exc = [display(x).strip() for x in _q1b[1].text.split('//')]
assert len(_exc) == 2 and _exc[1] == 'to keep the iodine in solution', _exc
C.add([k('1', 'b')], 'chem-4-1', 'why-potassium-iodide-is-in-excess', [
    lift('r-1', _exc[0], 3, 'EXCESS. The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _exc[1], 3)], qtext=Q1B_EXC, stem=Q1_STEM + ' ' + Q1B_COL, cid='q1-b-excess',
    ref_suffix='excess potassium iodide')
C.fixed([k('1', 'c')], 'chem-4-1', 'a-white-tile-under-the-titration-flask', stem=Q1_LATER)
C.fixed([k('1', 'd')], 'chem-4-1', 'starch-indicator-for-the-thiosulfate-titration', stem=Q1_LATER,
        row_notes={0: 'INDICATOR.', 1: 'CHANGE.'})
# (e): the paper sets (i) and (ii) on lines of their own (page 2, y 400 and 413)
# completing one sentence. (i): the answer (9), worked in a box as fractions the
# text layer reads in the wrong glyphs (6) and "X = 0.0322 / 0.032" (3), its X
# among them; (ii): the answer (3) and the one step that earns it.
Q1E = P.ask(k('1', 'e')) + ' (i) ' + P.ask(k('1', 'e', 'i')) + ' (ii) ' + P.ask(k('1', 'e', 'ii'))
assert Q1E == ('Calculate the concentration of NaClO in moles per litre in (i) the diluted bleach, (ii) the '
               'original bleach.'), Q1E
_q1e1 = P.items(k('1', 'e', 'i'))
assert [it.cell for it in _q1e1] == ['[9]', '[6]', '[3]'] and display(_q1e1[0].text) == '0.0322 / 0.032 M', _q1e1
C.add([k('1', 'e', 'i')], 'chem-4-1', 'concentration-of-hypochlorite-in-the-diluted-bleach', [
    lift('r-1', _q1e1[0].text, 9, 'For (i). The scheme prices the answer (9) and works it in a box: (25 × X) over 1 = '
         '(16.1 × 0.1) over 2, set as fractions, (6), then X = 0.0322 / 0.032 (3); its own print is shown with the '
         'answer.')], qtext=Q1E, stem=Q1_LATER, figure=S + 'q1e-i')
_q1e2 = P.items(k('1', 'e', 'ii'))
assert [(it.cell, display(it.text)) for it in _q1e2] == [('[3]', '0.644 / 0.64 M'),
                                                          ('[3]', '0.0322 / 0.032 ×20 = 0.644 / 0.64')], _q1e2
C.add([k('1', 'e', 'ii')], 'chem-4-1', 'concentration-of-hypochlorite-in-the-original-bleach', [
    lift('r-1', _q1e2[0].text, 3, 'For (ii). The scheme gives the answer, priced (3), and the one step that earns it: '
         '"' + traced('0.0322 / 0.032 × 20 = 0.644 / 0.64') + '" (3).')], qtext=Q1E, stem=Q1_LATER)
# (f): the same, (i) and (ii) on lines of their own (page 2, y 444 and 457). The
# answer lines price (i) (3) and (ii) (5), as the outline does ("(f) Original: (i) 3,
# (ii) 5." scheme page 4, y 137), and the paper's (8); the boxes under them print (5)
# beside (i)'s working and (3) beside (ii)'s (scheme page 5, y 604 and 701), quoted.
Q1F = P.ask(k('1', 'f')) + ' (i) ' + P.ask(k('1', 'f', 'i')) + ' (ii) ' + P.ask(k('1', 'f', 'ii'))
assert Q1F == 'What was the concentration of NaClO in the original bleach (i) in grams per litre, (ii) as a % (w/v)?', Q1F
_outline = traced(raw(4, 136, 150, 60))
assert _outline == '(e) Calculate: (i) 9, (ii) 3; (f) Original: (i) 3, (ii) 5.', _outline
_q1f1 = P.items(k('1', 'f', 'i'))
assert [(it.cell, display(it.text)) for it in _q1f1] == [
    ('[3]', '47.6 – 48.0 g l⁻¹'), ('[5]', '0.644 / 0.64 × 74.5* = 47.978 / 47.98 / 48 / 47.68 / 47.7'),
    (None, '*Addition must be shown for error to be treated as a slip')], _q1f1
_slip = traced(display(_q1f1[2].text))
_ar = traced('[Use of Ar values from table is acceptable]')
C.add([k('1', 'f', 'i')], 'chem-4-1', 'hypochlorite-in-grams-per-litre', [
    lift('r-1', _q1f1[0].text, 3, 'For (i). The scheme prices the answer (3), as its outline does ("(f) Original: (i) 3, '
         '(ii) 5."), and works it in a box: "' + display(_q1f1[1].text) + ' (5)". It adds: "' + _slip + '" ' + _ar)],
    qtext=Q1F, stem=Q1_LATER)
_q1f2 = P.items(k('1', 'f', 'ii'))
assert [(it.cell, display(it.text)) for it in _q1f2] == [
    ('[5]', '4.76 – 4.80 % (w/v)'), ('[3]', '47.978 ÷ 10 = 4.7978 / 4.798 / 4.8 / 4.768 / 4.77')], _q1f2
C.add([k('1', 'f', 'ii')], 'chem-4-1', 'hypochlorite-as-a-percentage-w-v', [
    lift('r-1', _q1f2[0].text, 5, 'For (ii). The scheme prices the answer (5), as its outline does, and works it in a '
         'box: "' + display(_q1f2[1].text) + ' (3)".')], qtext=Q1F, stem=Q1_LATER)

# ── Q2 Reflux and steam distillation ─────────────────────────────────────────
# (a): IDENTIFY (6); DRAW, "ANY FOUR: (4 × 3)" over five points beside the scheme's
# drawing (page 6, x 410-538, crop 'scheme-q2a'); WHAT (6); HOW, "ANY ONE: (6)"; the
# paper prints (30) once. It underlines "fully labelled" (page 2, y 529): its own
# print is the question.
_q2a = P.items(k('2', 'a'))
assert [it.cell for it in _q2a] == ['[6]', '[4 × 3]', '[6]', '[6]'], _q2a
_draw = _q2a[1].options()
_any4 = raw(6, 256, 269, 430)
_one = raw(6, 418, 431, 450)
assert len(_draw) == 5 and _any4 == 'ANY FOUR: (4 × 3)' and _one == 'ANY ONE: (6)', (_draw, _any4, _one)
_how = _q2a[3].options()
assert len(_how) == 5 and _how[0].startswith('allowed enough time'), _how
C.add([k('2', 'a')], 'chem-4-2', 'refluxing-a-reaction-mixture', [
    lift('r-1', _q2a[0].text, 6, 'IDENTIFY.'),
    menu_row('r-2', _draw, 4, 'DRAW: any four of these, (3) each: "' + _any4 + '". The scheme draws the apparatus beside '
             'them, labelled, shown with the answer. It adds: ' + ' '.join(a for a in _q2a[1].asides
                                                                          if not a.startswith('[any')),
             per=3, total=12),
    lift('r-3', _q2a[2].text, 6, 'WHAT.'),
    menu_row('r-4', _how, 1, 'HOW: any one of these, (6): "' + _one + '". The scheme adds: ' + _q2a[3].asides[1],
             per=6, total=6)], total=30, figure=S + 'q2a')
print_question('paper-q2a-print')
# (b): the steam distillation apparatus (paper page 2, x 372-534, crop 'paper-q2b').
Q2B = FIG + 'paper-q2b'
Q2B_STEM = C.context(k('2', 'b', 'i'))
assert Q2B_STEM == 'The diagram shows an apparatus suitable for steam distillation.', Q2B_STEM
C.fixed([k('2', 'b', 'i')], 'chem-u2', 'a-natural-product-from-steam-distillation', figure=Q2B)
C.fixed([k('2', 'b', 'ii')], 'chem-u2', 'appearance-of-a-steam-distillate', figure=Q2B)
C.fixed([k('2', 'b', 'iii')], 'chem-u2', 'what-distils-across-with-the-natural-product', figure=Q2B)
# (iv): IDEN "feature" (3) and "explanation" (3), from the scheme's table of two
# features and their explanations (page 6, y 647-706), matched.
_q2b4 = P.items(k('2', 'b', 'iv'))
assert [(it.cell, display(it.text)) for it in _q2b4][:2] == [('[3]', 'feature'), ('[3]', 'explanation')] and \
    _q2b4[2].asides == ['[Feature and explanation must be matched]'], _q2b4
_feat = [rows(6, 664, 689, 130, 232), rows(6, 694, 707, 130, 232)]
_expl = [rows(6, 664, 689, 232, 450), rows(6, 694, 707, 232, 450)]
assert _feat == ['Safety tube / steam tube', 'Air-tight seals'] and \
    _expl == ['Releases pressure / releases steam / preventing explosion',
              'No steam escapes / preventing burns (scalds)'], (_feat, _expl)
C.add([k('2', 'b', 'iv')], 'chem-u2', 'a-safety-feature-of-the-steam-distillation-apparatus', [
    menu_row('r-1', _feat, 1, 'IDEN: "feature" (3), one of the two in the scheme\'s table.', per=3, total=3),
    menu_row('r-2', _expl, 1, '"explanation" (3): the one the table sets beside the feature named. The scheme adds: '
             + _q2b4[2].asides[0], per=3, total=3)], total=6, figure=Q2B)

# ── Q3 Recrystallising benzoic acid ──────────────────────────────────────────
# The five stages are drawn (paper page 3, y 113-532, crop 'paper-q3'), their labels
# ("Stage 1", "Dissolving", "A", "B", ...) read as the picture's.
Q3 = FIG + 'paper-q3'
Q3_STEM = C.context(k('3', 'a'))
assert Q3_STEM.startswith('Organic solids are frequently purified by recrystallization.') and \
    Q3_STEM.endswith('the recrystallization of the impure benzoic acid from water.'), Q3_STEM
# (a), (c): the cues "STAGE 1:" and "STAGE 3:" carry a number the cue reader does not
# take for a cue, and are read as the answers' words: set apart here.
_q3a = P.items(k('3', 'a'))
assert [it.cell for it in _q3a] == ['[5]'] and display(_q3a[0].text).startswith('STAGE 1: crystals in'), _q3a
C.add([k('3', 'a')], 'chem-u2', 'dissolving-in-the-minimum-of-hot-water', [
    lift('r-1', display(_q3a[0].text)[len('STAGE 1: '):], 5, 'STAGE 1.')], figure=Q3)
# (b): the paper sets (i) and (ii) inside one sentence (page 3, y 590); the scheme
# prices (i) (3) and (ii) (3): a card each.
Q3B = P.ask(k('3', 'b'))
assert Q3B == 'What solid was collected (i) at A, (ii) at B?', Q3B
# The letters the ask names are decoded by the scheme's own answers ("charcoal / C /
# insoluble solid" at A, "pure ... benzoic acid" at B): the label key, asked in both.
_at = [display(P.items(k('3', 'b', r))[0].text) for r in ('i', 'ii')]
assert _at == ['charcoal / C / insoluble solid', 'pure (purified, recrystallized) benzoic acid'], _at
Q3B_KEY = [{'letter': 'A', 'meaning': _at[0], 'askedInThisQuestion': True},
           {'letter': 'B', 'meaning': _at[1], 'askedInThisQuestion': True}]
C.fixed([k('3', 'b', 'i')], 'chem-u2', 'the-solid-collected-at-a', qtext=Q3B, stem=Q3_STEM, figure=Q3,
        row_notes={0: 'For (i).'}, label_key=Q3B_KEY)
C.fixed([k('3', 'b', 'ii')], 'chem-u2', 'the-solid-collected-at-b', qtext=Q3B, stem=Q3_STEM, figure=Q3,
        row_notes={0: 'For (ii).'}, label_key=Q3B_KEY)
_q3c = P.items(k('3', 'c'))
assert [it.cell for it in _q3c] == ['[6]'] and display(_q3c[0].text).startswith('STAGE 3: further cooling'), _q3c
C.add([k('3', 'c')], 'chem-u2', 'cooling-further-for-the-maximum-yield', [
    lift('r-1', display(_q3c[0].text)[len('STAGE 3: '):], 6, 'STAGE 3. The scheme adds: ' + ' '.join(_q3c[0].asides))],
    figure=Q3)
C.fixed([k('3', 'd')], 'chem-u2', 'separating-benzoic-acid-from-salt-by-solubility', figure=Q3)
C.fixed([k('3', 'e')], 'chem-u2', 'drying-the-crystals', figure=Q3)
# (f): DESCRIBE (4 × 3), four points, then the footnote to "paraffin*" and a note on
# the diagram (scheme page 7, y 398-556); DIFFER (2 × 3). The paper prints (18) once;
# six rows outrun a card: a card each, cited with what it holds. The footnote is read
# welded to DIFFER's first row.
Q3F_DESC, Q3F_DIFF = cut(P.ask(k('3', 'f')), 'How would you')
_q3f = P.items(k('3', 'f'))
assert [it.cell for it in _q3f] == ['[4 × 3]', '[2 × 3]'], _q3f
_mp = [display(x).strip() for x in _q3f[0].text.split('//')]
_star = '*Or other suitable liquid (not water)'
_diff = display(_q3f[1].text)
assert len(_mp) == 4 and _mp[2].startswith('heated in liquid paraffin*') and _diff.startswith(_star + ' '), (_mp, _diff)
_diff = [x.strip() for x in _diff[len(_star):].split('//')]
assert len(_diff) == 2 and _q3f[1].asides == ['[Absence of diagram with at least one label: deduct 3 marks.]'], _diff
C.add([k('3', 'f')], 'chem-u2', 'measuring-a-melting-point', [
    lift('r-1', _mp[0], 3, 'DESCRIBE. The scheme prices these points (4 × 3), one each.'),
    lift('r-2', _mp[1], 3),
    lift('r-3', _mp[2], 3, 'The scheme adds: "' + traced(_star) + '"'),
    lift('r-4', _mp[3], 3, 'The scheme adds: ' + _q3f[1].asides[0])],
    qtext=Q3F_DESC, stem=Q3_STEM, figure=Q3, cid='q3-f-describe', ref_suffix='measuring the melting points')
C.add([k('3', 'f')], 'chem-u2', 'melting-points-of-impure-and-pure-benzoic-acid', [
    lift('r-1', _diff[0], 3, 'DIFFER. The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _diff[1], 3)],
    qtext=Q3F_DIFF, stem=Q3_STEM, figure=Q3, cid='q3-f-differ', ref_suffix='how the values differ')
C.fixed([k('3', 'g')], 'chem-u3', 'a-use-of-benzoic-acid', stem=Q3_STEM)

# ── Q4 Eight of eleven short items ───────────────────────────────────────────
C.menu([k('4', 'a')], 'chem-1-2', 'properties-of-cathode-rays', notes=Q4_NOTE,
       note='"' + traced('ANY TWO: (2 × 3)') + '".')
C.fixed([k('4', 'b')], 'chem-2-3', 'avogadros-law', notes=Q4_NOTE)
C.fixed([k('4', 'c')], 'chem-2-2', 'shapes-of-an-ab2-molecule', notes=Q4_NOTE)
C.fixed([k('4', 'd')], 'chem-1-4', 'the-mole', notes=Q4_NOTE)
# (e): the answer (6), then a box (scheme page 8, y 362-418): the first step (3), set
# as fractions the text layer reads apart ("2.00 over 2.10 = 120 over 18x / 2 over
# 120 : 2.1 over 18 :") and then in words, and the answer (3).
_q4e = P.items(k('4', 'e'))
assert [(it.cell, display(it.text)) for it in _q4e][0] == ('[6]', 'x = 7') and cells(k('4', 'e')) == ['[6]', '[3]'], _q4e
_box = raw(8, 370, 396, 254)
assert _box == '18 : MgSO₄.xH₂O = 246 / water = 126 (3) => x = 7 (3)', _box
C.add([k('4', 'e')], 'chem-1-4', 'water-of-crystallisation-in-magnesium-sulfate', [
    lift('r-1', 'MgSO₄.xH₂O = 246 / water = 126', 3, 'The scheme gives the answer, x = 7, priced (6), then works it in '
         'a box, two steps (3) each. Before this step it sets two others as fractions: 2.00 over 2.10 = 120 over 18x, '
         'and 2 over 120 : 2.1 over 18; its own print is shown with the answer.'),
    lift('r-2', '=> x = 7', 3, 'The scheme adds: ' + ' '.join(_q4e[1].asides))],
    notes=Q4_NOTE, figure=S + 'q4e')
# (f): the equation, priced "FORMULAS // BALANCING: (2 × 3)" (scheme page 8, y 426). The
# paper sets the charge of "Cu²⁺" after the ion (page 4, y 254).
_q4f = P.items(k('4', 'f'))
_cu = display(_q4f[0].text)
assert [it.cell for it in _q4f] == ['[2 × 3]'] and _cu == '3Cu²⁺ + 2Al → 3Cu + 2Al³⁺ FORMULAS // BALANCING:', _q4f
_fb = raw(8, 425, 439, 370)
assert _fb == 'FORMULAS // BALANCING: (2 × 3)', _fb
C.add([k('4', 'f')], 'chem-3-5', 'aluminium-displacing-copper', [
    lift('r-1', _cu[:-len(' FORMULAS // BALANCING:')], 6, 'EQUAT: "' + _fb + '".')], notes=Q4_NOTE,
    qtext=P.rearranged(P.ask(k('4', 'f')), 'Cu 2+ + Al →', 'Cu²⁺ + Al →'))
C.menu([k('4', 'g')], 'chem-4-3', 'removing-all-hardness-from-water', notes=Q4_NOTE,
       note='"' + traced('ANY TWO: (2 × 3)') + '".')
C.fixed([k('4', 'h')], 'chem-3-2', 'activation-energy', notes=Q4_NOTE)
# (i): WHAT, "ANY TWO: (2 × 3)" of six; the examiner's note "Accept 'uniform chemical
# type' for 'sim. chem. properties.'" is set in bold on the list's last row (scheme
# page 8, y 584) and read as words of the last option: lifted out.
_q4i = P.items(k('4', 'i'))
_hom = [display(x).strip() for x in _q4i[0].text.split('//')]
_acc = 'Accept ‘uniform chemical type’ for ‘sim. chem. properties.’'
assert [it.cell for it in _q4i] == ['[2 × 3]'] and len(_hom) == 6 and _hom[5].endswith(' ' + _acc), _hom
_hom[5] = _hom[5][:-len(' ' + _acc)]
C.add([k('4', 'i')], 'chem-2-4', 'a-homologous-series', [
    menu_row('r-1', _hom, 2, 'Any two of these, (3) each: "' + traced('ANY TWO: (2 × 3)') + '". The scheme adds: "'
             + traced(_acc) + '"', per=3, total=6)], total=6, notes=Q4_NOTE)
C.fixed([k('4', 'j')], 'chem-u2', 'the-principle-of-chromatography', notes=Q4_NOTE)
C.fixed([ka('4', 'k', None, 'A')], 'chem-2-1', 'how-metallic-crystals-conduct', notes=Q4_NOTE)
C.fixed([ka('4', 'k', None, 'B')], 'chem-4-3', 'the-greenhouse-factor', notes=Q4_NOTE,
        qtext=P.ask(ka('4', 'k', None, 'B'), upto='in the atmosphere?'))

# ── Q5 The periodic table ────────────────────────────────────────────────────
# (a): the paper sets (i) and (ii) inside one sentence (page 4, y 498); the scheme
# prices (i) (5) and (ii) (2 × 3): a card each.
Q5A = P.ask(k('5', 'a'))
assert Q5A == 'Define (i) atomic number, (ii) relative atomic mass.', Q5A
C.fixed([k('5', 'a', 'i')], 'chem-1-2', 'atomic-number', qtext=Q5A, stem='', row_notes={0: 'For (i).'})
C.fixed([k('5', 'a', 'ii')], 'chem-1-2', 'relative-atomic-mass', qtext=Q5A, stem='', row_notes={0: 'For (ii).'})
# (b): BASIS (2 × 3), SPACES (3), REVER (3); the paper prints (12) once, at the end of
# its last line ("Explain why he did this.(12)", page 4, y 623), read with the ask.
# Mendeleev's portrait (page 4, x 447-533, crop 'paper-q5b').
Q5B = P.ask(k('5', 'b'))
assert Q5B.startswith('Sixty-two elements were known') and Q5B.endswith('Explain why he did this.(12)'), Q5B
C.fixed([k('5', 'b')], 'chem-1-3', 'mendeleevs-periodic-table', qtext=Q5B[:-len('(12)')], figure=FIG + 'paper-q5b',
        row_notes={0: 'BASIS.', 2: 'SPACES.', 3: 'REVER.'})
# (c): the paper sets (i) and (ii) inside one sentence (page 4, y 673); the scheme
# prices (i) (6) and (ii) (3): a card each.
Q5C_STEM, Q5C = cut(P.ask(k('5', 'c')), 'Explain why')
assert Q5C == ('Explain why (i) the alkali metals are all reactive, (ii) the reactivity of the alkali metals increases '
               'down the group.'), Q5C
C.fixed([k('5', 'c', 'i')], 'chem-1-3', 'why-the-alkali-metals-are-reactive', qtext=Q5C, stem=Q5C_STEM,
        row_notes={0: 'For (i).'})
C.fixed([k('5', 'c', 'ii')], 'chem-1-3', 'reactivity-down-the-alkali-metals', qtext=Q5C, stem=Q5C_STEM,
        row_notes={0: 'For (ii).'})
# (d)(i): DEFINE (2 × 3), two points, or after "or" a second wording of two points
# (scheme page 9, y 490-578).
_w1 = [x.strip() for x in rows(9, 489, 528, 170, 478).split('//')]
_w2 = [x.strip() for x in rows(9, 551, 578, 170, 470).split('//')]
assert raw(9, 533, 547, 220, 260) == 'or' and len(_w1) == 2 and _w2 == [
    'space occupied by electron', 'described by solution of Schrödinger equation'] and \
    cells(k('5', 'd', 'i')) == ['[2 × 3]', '[2 × 3]'], (_w1, _w2)
C.add([k('5', 'd', 'i')], 'chem-1-2', 'atomic-orbital', [
    menu_row('r-1', [_w1[0], _w2[0]], 1, 'One of these wordings, the scheme setting the second after "or"; it prices the '
             'two points of each (2 × 3), one each.', per=3, total=3),
    menu_row('r-2', [_w1[1], _w2[1]], 1, 'And the second point of that same wording, (3).', per=3, total=3)], total=6)
# (ii): WRITE (6); the note under it sets p's x, y and z as subscripts and its 2s as
# superscripts the text layer reads apart (scheme page 9, y 608-622): quoted as far
# as it reads, its own print shown with the answer.
_q5d2 = P.items(k('5', 'd', 'ii'))
assert [it.cell for it in _q5d2] == ['[6]', None] and \
    display(_q5d2[0].text) == '1s²2s²2p⁶3s²3p⁶4s²3d⁵ / [Ar]4s²3d⁵ / 1s²2s²2p⁶3s²3p⁶3d⁵4s² / [Ar]3d⁵4s²', _q5d2
C.add([k('5', 'd', 'ii')], 'chem-1-2', 'electron-configuration-of-manganese', [
    lift('r-1', _q5d2[0].text, 6, 'The scheme adds a note accepting the p orbitals written out with their subscripts '
         'and superscripts for p⁶, and "' + traced('accept subscripts.]')[:-1] + '"; its own print is shown with the '
         'answer.')], figure=S + 'q5d-ii')
# (iii): WHAT (6); the page sets the x of "3dx" as a subscript (scheme page 9, y 631),
# which the text layer reads on the line: set where the page prints it.
_q5d3 = P.items(k('5', 'd', 'iii'))
_3d = display(_q5d3[0].text)
assert [it.cell for it in _q5d3] == ['[6]'] and _3d.endswith('(All end in 3dx)'), _q5d3
C.add([k('5', 'd', 'iii')], 'chem-1-2', 'what-scandium-to-zinc-have-in-common', [
    lift('r-1', _3d[:-len('3dx)')] + '3dₓ)', 6, 'The scheme adds: ' + ' '.join(_q5d3[0].asides))])

# ── Q6 Crude oil and hydrogen ────────────────────────────────────────────────
Q6_STEM = C.context(k('6', 'a'))
assert Q6_STEM.startswith('Over 20% of the crude oil refined at Whitegate') and \
    Q6_STEM.endswith('and diesel derived from vegetable oil.'), Q6_STEM
C.fixed([k('6', 'a')], 'chem-2-4', 'what-crude-oil-is-made-of')
# (b): DESC (4 × 3), four points, beside the scheme's drawing of a fractionating column
# (page 10, x 378-528, crop 'scheme-q6b'); USE (3).
C.fixed([k('6', 'b')], 'chem-2-4', 'fractional-distillation-of-crude-oil', figure=S + 'q6b',
        row_notes={0: 'DESC. The scheme draws a fractionating column beside these points, labelled, shown with the '
                      'answer.', 4: 'USE.'})
C.fixed([k('6', 'c')], 'chem-2-4', 'catalytic-cracking', row_notes={0: 'WHAT.', 2: 'WHY.'})
C.fixed([k('6', 'd', 'i')], 'chem-2-4', 'hydrogen-from-water-on-a-large-scale')
C.fixed([k('6', 'd', 'ii')], 'chem-2-4', 'a-drawback-of-hydrogen-as-a-fuel')
# (e): CALC (12): three equations (3) each and their sum under a rule (3); then after
# "Equations not required" the sums of heats of formation (scheme page 10, y 548-702).
# The paper's equation sets state symbols the text layer reads apart ("CH₄ _((g))"):
# its own print is the question.
_q6e = P.items(k('6', 'e'))
_last = display(_q6e[4].text)
assert [it.cell for it in _q6e] == ['[12]'] + ['[3]'] * 7 and _last.startswith('______') and \
    _last.endswith(' CH₄ + H₂O → CO + 3H₂ ΔH = 205.6 kJ'), _q6e
C.route([k('6', 'e')], 'chem-3-1', 'heat-of-the-steam-reforming-reaction', figure=S + 'q6e',
        fixes={_last: 'CH₄ + H₂O → CO + 3H₂ ΔH = 205.6 kJ'},
        notes='After "Equations not required" the scheme works it from the sums of heats of formation instead, '
              'pricing each term it uses (3).')
shown('The scheme gives the answer as "ΔH = 205.6 kJ mol⁻¹" (12). After "Equations not required" it works it from the '
      'sums of heats of formation instead, pricing each term (3); its own print of both is shown with the answer.')
print_question('paper-q6e-print')

# ── Q7 Strong and weak acids ─────────────────────────────────────────────────
Q7_STEM = C.context(k('7', 'a'))
assert Q7_STEM == 'Sulfuric acid is a strong dibasic acid. The formula HA represents a weak monobasic acid.', Q7_STEM
# (a): the paper sets (i) and (ii) on a line of their own (page 5, y 420) completing
# one sentence; the scheme prices each (2 × 3): a card each. Each examiner's note
# is set under the row it qualifies (scheme page 11, y 71 and 109).
Q7A = P.ask(k('7', 'a')) + ' (i) ' + P.ask(k('7', 'a', 'i')) + ' (ii) ' + P.ask(k('7', 'a', 'ii'))
assert Q7A == ('How do strong acids differ from weak acids in their behaviour in water according to (i) the Arrhenius '
               'theory, (ii) the Brønsted-Lowry theory?'), Q7A
_q7a1 = P.items(k('7', 'a', 'i'))
_arr = [display(x).strip() for x in _q7a1[0].text.split('//')]
assert [it.cell for it in _q7a1] == ['[2 × 3]'] and len(_arr) == 2 and len(_q7a1[0].asides) == 2, _q7a1
C.add([k('7', 'a', 'i')], 'chem-3-4', 'strong-and-weak-acids-in-the-arrhenius-theory', [
    lift('r-1', _arr[0], 3, 'For (i). The scheme prices these points (2 × 3), one each, and adds: ' + _q7a1[0].asides[0]),
    lift('r-2', _arr[1], 3, 'The scheme adds: ' + _q7a1[0].asides[1])], qtext=Q7A, stem=Q7_STEM)
C.fixed([k('7', 'a', 'ii')], 'chem-3-4', 'strong-and-weak-acids-in-the-bronsted-lowry-theory', qtext=Q7A, stem=Q7_STEM,
        row_notes={0: 'For (ii).'})
# (b): the paper sets (i) and (ii) inside one sentence (page 5, y 442), then "Which of
# these conjugate bases is the stronger? Explain."; the scheme prices (i) (3), (ii)
# (3), WHICH (3) and EXPL (3): a card for each roman, and one for the ask after them.
Q7B, Q7B_WHICH = cut(P.ask(k('7', 'b')), 'Which of these')
assert Q7B == 'What is the conjugate base of (i) sulfuric acid, (ii) the weak acid HA?' and \
    Q7B_WHICH == 'Which of these conjugate bases is the stronger? Explain.', (Q7B, Q7B_WHICH)
_q7b1 = P.items(k('7', 'b', 'i'))
assert [(it.cell, display(it.text)) for it in _q7b1] == [('[3]', 'sulfuric acid: HSO₄¯')], _q7b1
C.add([k('7', 'b', 'i')], 'chem-3-4', 'conjugate-base-of-sulfuric-acid', [
    lift('r-1', 'HSO₄¯', 3, 'For (i): the scheme sets it after "sulfuric acid:".')], qtext=Q7B, stem=Q7_STEM)
_q7b2 = P.items(k('7', 'b', 'ii'))
assert [(it.cell, display(it.text)) for it in _q7b2][:2] == [('[3]', 'A¯'), ('[3]', 'A¯ / conjugate base of weak acid')] \
    and cells(k('7', 'b', 'ii')) == ['[3]'] * 3 and raw(11, 213, 228, 110, 160) == 'HA:', _q7b2
C.add([k('7', 'b', 'ii')], 'chem-3-4', 'conjugate-base-of-a-weak-acid', [
    lift('r-1', 'A¯', 3, 'For (ii): the scheme sets it after "HA:".')], qtext=Q7B, stem=Q7_STEM)
C.add([k('7', 'b')], 'chem-3-4', 'the-stronger-conjugate-base', [
    lift('r-1', _q7b2[1].text, 3, 'WHICH.'), lift('r-2', _q7b2[2].text, 3, 'EXPL.')],
    qtext=Q7B_WHICH, stem=Q7_STEM + ' ' + Q7B, cid='q7-b-stronger', ref_suffix='after (ii), the stronger base')
# (c): EXPL (6), the equation; the examiner's note under it prices an incomplete one
# (2 × 3) (scheme page 11, y 341-372), quoted.
_q7c = P.items(k('7', 'c'))
assert [(it.cell, display(it.text)) for it in _q7c] == [
    ('[6]', 'HSO₄¯ + H₂O → SO₄ 2– + H₃O⁺'),
    (None, '[If incomplete, mark as: HSO₄¯→ SO₄ 2– // H₂O → H₃O⁺ (2 × 3)]')], _q7c
C.add([k('7', 'c')], 'chem-3-4', 'the-hydrogensulfate-ion-as-an-acid', [
    lift('r-1', 'HSO₄¯ + H₂O → SO₄²⁻ + H₃O⁺', 6, 'The scheme adds: "' + traced(
        '[If incomplete, mark as: HSO₄¯→ SO₄²⁻ // H₂O → H₃O⁺ (2 × 3)]') + '"')], stem=Q7_STEM)
# (d): DEF (6), printed (6): the words, then after "/" the log formulas in glyphs the
# text layer misreads (scheme page 11, y 419-444). CALC (9) and CONC (5), printed
# (14) together: the first route's three steps (3) each, the pH worked after "or" from
# a square root in two boxes, then CONC's two steps (3) and (2) (y 455-731).
Q7D_DEF, Q7D_CALC = cut(P.ask(k('7', 'd')), 'Calculate the pH')
assert Q7D_DEF == 'Define pH.' and Q7D_CALC.endswith('that has the same pH?'), Q7D_CALC
_q7d = P.items(k('7', 'd'))
assert [it.cell for it in _q7d] == ['[6]', '[9]', '[3]', '[3]', '[3]', '[5]', '[3]', '[2]'], _q7d
_ph = raw(11, 393, 407, 115)
assert _ph == 'minus log (negative log) to base 10 of hydrogen (hydronium) ion concentration /', _ph
C.add([k('7', 'd')], 'chem-3-4', 'definition-of-ph', [
    lift('r-1', _ph.rstrip('/ '), 6, 'After "/" the scheme gives it as formulas: minus log₁₀ of [H⁺] or of [H₃O⁺], or '
         'log₁₀ of 1 over [H⁺] or over [H₃O⁺], set as fractions; its own print is shown with the answer.')],
    qtext=Q7D_DEF, stem='', figure=S + 'q7d-def', cid='q7-d-define', ref_suffix='pH defined')
_ka = raw(11, 480, 500, 215, 405).split(' / ')
_h = rows(11, 510, 526, 150, 320)
_p = rows(11, 536, 552, 150, 290)
_c1, _c2 = raw(11, 696, 712, 120, 420), raw(11, 716, 731, 120, 420)
_conc = raw(11, 673, 688, 80, 400)
assert _ka[1:] == ['[H⁺]² = 1.26 × 10⁻⁵'] and _ka[0].endswith('= 6.3 × 10⁻⁵') and _h == '⇒ [H⁺] = 3.5 × 10⁻³' and \
    _p == '⇒ pH = 2.45' and _c1.startswith('[H⁺] / inv. log') and _c2.startswith('⇒ M =') and \
    _conc == 'CONC: 1.75 × 10⁻³ – 1.77 × 10⁻³', (_ka, _h, _p, _c1, _c2, _conc)
C.add([k('7', 'd')], 'chem-3-4', 'ph-of-a-weak-acid-and-a-strong-acid-of-the-same-ph', [
    lift('r-1', _ka[1], 3, 'CALC: the scheme gives the answer, "pH = 2.45", priced (9), then three steps (3) each. It '
         'opens "Ka =" [H⁺][A⁻] over [HA], or [H⁺]² over 0.2, set as fractions, "= 6.3 × 10⁻⁵ /" then this; after '
         '"or" it works the pH from the square root of Ka[M] in two boxes. Its own print is shown with the answer.'),
    lift('r-2', _h, 3),
    lift('r-3', _p, 3),
    lift('r-4', _c1, 3, 'CONC: the scheme gives the answer, "' + _conc[len('CONC: '):] + '", priced (5), then two '
         'steps, (3) and (2).'),
    lift('r-5', _c2, 2)],
    qtext=Q7D_CALC, stem=Q7_STEM, figure=S + 'q7d-calc', cid='q7-d-calc',
    ref_suffix='the pH and the sulfuric acid concentration')

# ── Q8 Methane, ethene and benzene ───────────────────────────────────────────
# The question's opening "Answer the questions below about methane ..." is set as an
# instruction, which C.context leaves out; it names the three compounds: the stem.
Q8_STEM = P.ask(k('8'))
assert Q8_STEM.startswith('Answer the questions below about methane (a saturated hydrocarbon)'), Q8_STEM
Q8A_MECH, Q8A_EVID = cut(P.ask(k('8', 'a')), 'State three')
assert Q8A_MECH == 'Describe the mechanism of the monochlorination of methane.', Q8A_MECH
# (a): DESC "ANY FOUR: (4 × 3)" over five points, each step's words then after "/"
# its equations in glyphs the text layer misreads (scheme page 12, y 58-273); a
# script run "•)" starts above its row: read row by row.
_mech = [raw(12, 58, 77, 185, 525) + ' ' + raw(12, 79, 95, 185, 330).split(' / ')[0],
         rows(12, 96, 131.5, 185, 525).rstrip('/ '),
         rows(12, 142, 177, 185, 525).rstrip('/ '),
         raw(12, 195, 209, 185).rstrip('/ '),
         raw(12, 220, 234, 185, 450).rstrip('/ ')]
assert _mech[0].endswith('free radicals (Cl•) by ultraviolet (uv) light') and \
    _mech[1].endswith('and a methyl radical (CH₃ •)') and _mech[2].endswith('and a chlorine radical (Cl•)') and \
    _mech[3:] == ['chain reaction occurs', 'combination of remaining radicals to form molecules'], _mech
_stage = [raw(12, 62, 77, 60, 185), raw(12, 101, 115, 110, 185), raw(12, 220, 234, 110, 185)]
_any4 = raw(12, 259, 273, 450)
assert _stage == ['(a) DESC: initiation:', 'propagation:', 'termination:'] and _any4 == 'ANY FOUR: (4 × 3)', _stage
C.add([k('8', 'a')], 'chem-4-2', 'free-radical-chlorination-of-methane', [
    menu_row('r-1', _mech, 4, 'DESC: any four of these, (3) each: "' + _any4 + '". The scheme sets the first under '
             '"initiation:", the next three under "propagation:" and the last under "termination:", and after each "/" '
             'gives the step as equations; its own print is shown with the answer.', per=3, total=12)],
    total=12, qtext=Q8A_MECH, stem=Q8_STEM, figure=S + 'q8a', cid='q8-a-mechanism', ref_suffix='the mechanism')
# STATE: "three × [piece of evidence // corresponding explanation] 3 × (2 × 3)", from
# the scheme's table of seven pieces of evidence and their explanations (page 12, y
# 322-513), matched.
_state = raw(12, 297, 311, 180)
assert _state == 'three × [piece of evidence // corresponding explanation] 3 × (2 × 3)', _state
_bands = ((342, 374.5), (374.5, 395.5), (394, 418), (417, 438), (438, 470), (468, 491), (489, 513))
_ev = [rows(12, a, b, 100, 255) for a, b in _bands]
_ex = [rows(12, a, b, 255, 525) for a, b in _bands]
_tail = ' [not given from termination above]'
assert len(_ev) == 7 and _ev[0] == 'promoted by uv at room temp' and _ev[6] == 'HCl produced' and \
    _ex[2].endswith(_tail) and _ex[6] == 'shows Cl• produced / proves Cl• attacks CH₄', (_ev, _ex)
_ex[2] = _ex[2][:-len(_tail)]
# "{tetra-" ends its row and "methyl (tetraethyl) lead}" opens the next (page 12, y 417-438):
# the word broken at its hyphen, joined.
assert _ev[3] == 'add source of free radicals {tetra- methyl (tetraethyl) lead}', _ev[3]
_ev[3] = _ev[3].replace('{tetra- methyl', '{tetra-methyl')
_match = traced(raw(12, 524, 539, 160))
assert _match == '*Piece of evidence and explanation must be matched', _match
C.add([k('8', 'a')], 'chem-4-2', 'evidence-for-the-free-radical-mechanism', [
    menu_row('r-1', _ev, 3, 'STATE: "' + _state + '": three pieces of evidence from the scheme\'s table, (3) each.',
             per=3, total=9),
    menu_row('r-2', _ex, 3, 'And the explanation the table sets beside each piece of evidence named, (3) each. The '
             'scheme adds, beside the explanation of "ethane formed":' + _tail + ' and under the table: "' + _match + '"',
             per=3, total=9)],
    total=18, qtext=Q8A_EVID, stem=Q8_STEM + ' ' + Q8A_MECH, figure=S + 'q8a-evidence', cid='q8-a-evidence',
    ref_suffix='evidence for the mechanism')
C.fixed([k('8', 'b', 'i')], 'chem-4-2', 'type-of-reaction-from-ethanol-to-ethene')
# (b)(ii): BROKEN and FORMED, priced together (6 + 3).
_q8b2 = P.items(k('8', 'b', 'ii'))
_bf = _q8b2[0].points()
assert [it.cell for it in _q8b2] == ['[6 + 3]'] and _bf == ['C – H and C – O',
                                                            'C = C and O – H / C to C π (pi) bond and O – H'], _q8b2
C.add([k('8', 'b', 'ii')], 'chem-4-2', 'bonds-broken-and-formed-making-ethene', [
    lift('r-1', _bf[0], None, 'BROKEN. The scheme prices its two points (6 + 3).'),
    lift('r-2', _bf[1], None, 'FORMED.')],
    kind='orderedSplit', notation='[6 + 3]', total=9, notes=SPLIT.format('[6 + 3]'))
# (c): DESCRIBE (3 + 3 + 2), three points, or after "or" a second set of three, each
# priced (3 + 3 + 2) (scheme page 12, y 627-741).
_q8c = P.items(k('8', 'c'))
assert [it.cell for it in _q8c] == ['[3 + 3 + 2]', '[3 + 3 + 2]'], _q8c
_b1 = [display(x).strip() for x in _q8c[0].text.split('//')]
_b2 = [display(x).strip() for x in _q8c[1].text.split('//')]
_b13, _b1a = split_asides(_b1[2])
assert len(_b1) == 3 and len(_b2) == 3 and _b1a == ['[Accept correct description]'], (_b1, _b2)
C.add([k('8', 'c')], 'chem-2-1', 'bonding-in-benzene', [
    menu_row('r-1', [_b1[0], _b2[0]], 1, 'One of these, the scheme setting the second set of points after "or"; it '
             'prices the three points of each (3 + 3 + 2).'),
    menu_row('r-2', [_b1[1], _b2[1]], 1, 'And the second point of that same set.'),
    menu_row('r-3', [_b13, _b2[2]], 1, 'And the third point of that same set. The scheme adds, after the first: '
             + _b1a[0])],
    kind='orderedSplit', notation='[3 + 3 + 2]', total=8, notes=SPLIT.format('[3 + 3 + 2]'), stem=Q8_STEM)

# ── Q9 Equilibria ────────────────────────────────────────────────────────────
# (a): the equation draws its equilibrium arrow (paper page 6, y 72-85), read as a
# picture's ('q9a-equation'); the cards' questions are the paper's print of it.
# WRITE (5), printed (5): the scheme sets the expression as a fraction in glyphs the
# text layer misreads (scheme page 13, y 68-90), so the row is the paper's ask and
# the scheme's print its answer. CALC (18), printed (18): the answer, then two routes
# side by side, four steps each (y 104-289): the rows are the first route's.
Q9A_LEAD, _r = cut(P.ask(k('9', 'a')), 'Write the equilibrium')
Q9A_WRITE, Q9A_CALC = cut(_r, 'Calculate the equilibrium')
assert Q9A_LEAD.endswith('described by the following balanced equation, is established.') and \
    Q9A_WRITE == 'Write the equilibrium constant (Kc) expression for this reaction.' and \
    Q9A_CALC.endswith('The value of Kc at this temperature is 0.0185.'), (Q9A_LEAD, Q9A_WRITE, Q9A_CALC)
_q9a = P.items(k('9', 'a'))
assert [it.cell for it in _q9a][:2] == ['[5]', '[18]'] and display(_q9a[1].text) == '0.044 – 0.045 mol l⁻¹', _q9a
C.add([k('9', 'a')], 'chem-3-3', 'kc-expression-for-hydrogen-iodide', [
    C.mark_ask(point('r-1', Q9A_WRITE, 5, 'The scheme answers with the expression set as a fraction, shown with the '
                     'answer.'))],
    qtext=Q9A_WRITE, stem=Q9A_LEAD, figure=S + 'q9a-write', cid='q9-a-expression', ref_suffix='Kc expression')
print_question('paper-q9a-write-print')
_eq = rows(13, 195, 209, 80, 300)
_frac = rows(13, 225, 238, 155, 260)
_x = rows(13, 252, 266, 120, 260)
_conc9 = rows(13, 274, 290, 80, 270)
_let = raw(13, 126, 139, 80, 305)
assert _eq == 'Equil: (5 – 2x) mol x mol x mol (3)' and _frac == '= 0.0185' and _x == 'x = 0.53 – 0.54 mol' and \
    _conc9 == 'Conc: 0.53 ÷ 12 = 0.044 – 0.045 mol l⁻¹' and \
    _let == 'Let x = number of moles of hydrogen at equilibrium', (_eq, _frac, _x, _conc9, _let)
C.add([k('9', 'a')], 'chem-3-3', 'equilibrium-concentration-of-hydrogen-from-kc', [
    lift('r-1', _eq[:-len(' (3)')], 3, 'The scheme gives the answer, "0.044 – 0.045 mol l⁻¹", priced (18), then two '
         'routes side by side, four steps each: these are the first, under "' + _let + '"; the second works in '
         'concentrations. Its own print of both is shown with the answer.'),
    lift('r-2', _frac, 6, 'The scheme prints x² over [5 – 2x]², set as a fraction, then this.'),
    lift('r-3', _x, 6),
    lift('r-4', _conc9, 3)],
    qtext=Q9A_CALC, stem=Q9A_LEAD, figure=S + 'q9a-calc', cid='q9-a-calculation',
    ref_suffix='equilibrium concentration of hydrogen')
print_question('paper-q9a-calc-print')
# (b): the equation, its arrow drawn and its colours labelled under it (paper page 6,
# y 166-196, crop 'paper-q9b'). (i)-(iii) complete the sentence "Explain", on lines of
# their own (y 243-300); the ask after (iii) is a card of its own.
Q9B = FIG + 'paper-q9b'
Q9B_STEM = P.ask(k('9', 'b'))
assert Q9B_STEM.endswith('Test tube D was kept as a reference. Explain'), Q9B_STEM
Q9B_STEM = Q9B_STEM[:-len(' Explain')]
Q9B_III, Q9B_C = cut(P.ask(k('9', 'b', 'iii')), 'When test tube C')
Q9B_SENT = 'Explain (i) ' + P.ask(k('9', 'b', 'i')) + ' (ii) ' + P.ask(k('9', 'b', 'ii')) + ' (iii) ' + Q9B_III
assert Q9B_SENT.endswith('(iii) the colour that appeared when a few drops of concentrated hydrochloric acid were added '
                         'to test tube B.') and Q9B_C.endswith('Justify your answer.'), (Q9B_SENT, Q9B_C)
C.menu([k('9', 'b', 'i')], 'chem-3-3', 'the-lilac-colour-of-the-cobalt-equilibrium', qtext=Q9B_SENT, stem=Q9B_STEM,
       figure=Q9B, note='For (i). "' + traced('ANY TWO: (2 × 3)') + '".')
C.fixed([k('9', 'b', 'ii')], 'chem-3-3', 'adding-water-to-the-cobalt-equilibrium', qtext=Q9B_SENT, stem=Q9B_STEM,
        figure=Q9B, row_notes={0: 'For (ii).'})
_q9b3 = P.items(k('9', 'b', 'iii'))
assert [it.cell for it in _q9b3] == ['[2 × 3]', '[3]', '[6]'], _q9b3
_blue = [display(x).strip() for x in _q9b3[0].text.split('//')]
assert _blue[0] == 'blue' and len(_blue) == 2, _blue
C.add([k('9', 'b', 'iii')], 'chem-3-3', 'adding-acid-to-the-cobalt-equilibrium', [
    lift('r-1', _blue[0], 3, 'For (iii). The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _blue[1], 3)], qtext=Q9B_SENT, stem=Q9B_STEM, figure=Q9B)
C.add([k('9', 'b')], 'chem-3-3', 'cooling-the-cobalt-equilibrium', [
    lift('r-1', _q9b3[1].text, 3, 'IS.'), lift('r-2', _q9b3[2].text, 6, 'JUSTIFY.')],
    qtext=Q9B_C, stem=Q9B_STEM, figure=Q9B, cid='q9-b-cooling', ref_suffix='after (iii), test tube C in ice')

# ── Q10 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a): the paper prints (5) after "Define ...", (12) after "Suggest ... Describe ..."
# and (8) after "Draw ...": a card each. DEFINE (5): two wordings, then after "/" a
# third set as a fraction in glyphs the text layer misreads (scheme page 14, y 52-92),
# read as words of SUGGEST; its own lines are read here.
Q10A = P.ask(k('10', 'a'))
Q10A_DEF, _r = cut(Q10A, 'There is a slow')
Q10A_LEAD, _r = cut(_r, 'Suggest the type')
Q10A_CAT, Q10A_DRAW = cut(_r, 'Draw a clearly')
assert Q10A_DEF == 'Define the rate of a chemical reaction.' and Q10A_LEAD.endswith('catalyst is added.') and \
    Q10A_DRAW.endswith('with and without the catalyst.'), Q10A
_q10a = P.items(k('10', 'a'))
assert [it.cell for it in _q10a] == ['[5]', '[6]', '[6]', '[3]', '[5]'], _q10a
_rate = raw(14, 51, 66, 140)
_sug = raw(14, 101, 116, 140, 400)
assert _rate == 'change in concentration per unit time / rate of change of concentration /' and \
    _sug == 'heterogeneous (not ‘hetero’) / surface / adsorption', (_rate, _sug)
C.add([k('10', 'a')], 'chem-3-2', 'rate-of-a-chemical-reaction', [
    lift('r-1', _rate.rstrip('/ '), 5, 'After "/" the scheme sets "change in concentration" over "time" as a fraction; '
         'its own print is shown with the answer.')],
    qtext=Q10A_DEF, stem='', figure=S + 'q10a-define', cid='q10-a-rate', ref_suffix='rate defined')
C.add([k('10', 'a')], 'chem-3-2', 'surface-catalysis-by-platinum', [
    lift('r-1', _sug, 6, 'SUGGEST.'),
    lift('r-2', _q10a[2].text, 6, 'DESCRIBE. The scheme adds: ' + ' '.join(_q10a[2].asides))],
    qtext=Q10A_CAT, stem=Q10A_LEAD, cid='q10-a-catalysis', ref_suffix='the catalysis')
# DRAW (3) and (5), beside the scheme's drawing of the two profiles (page 14, x 405-487,
# crop 'scheme-q10a-draw'). The paper underlines "and" (page 6, y 470): its own print
# is the question.
C.add([k('10', 'a')], 'chem-3-2', 'reaction-profiles-with-and-without-a-catalyst', [
    lift('r-1', display(_q10a[3].text).rstrip('/ '), 3, 'DRAW. The scheme draws the two profiles beside its points, '
         'shown with the answer.'),
    lift('r-2', _q10a[4].text, 5)],
    qtext=Q10A_DRAW, stem=Q10A_LEAD, figure=S + 'q10a-draw', cid='q10-a-profile', ref_suffix='reaction profile')
print_question('paper-q10a-draw-print')
# (b): WRITE (4, 3), printed (7); NAME (3), printed (3); the scheme reads the cell of
# WRITE, "FORMULAS // BALANCING: (4, 3)", as words of the answer and welds NAME to it
# (scheme page 14, y 307-342): its own lines are read here. CALC: the scheme sets
# (i)'s calculation (9) and (ii)'s (6) under one cue with no romans (y 354-491).
Q10B = P.ask(k('10', 'b'))
Q10B_GLU, _r = cut(Q10B, 'Write a balanced')
Q10B_WRITE, _r = cut(_r, 'When a person')
Q10B_RATE, Q10B_NAME = cut(_r, 'Name the primary')
Q10B_LEAD = P.lead(k('10', 'b'))
assert Q10B_WRITE == 'Write a balanced chemical equation for this fermentation reaction.' and \
    Q10B_NAME == 'Name the primary metabolite of ethanol in the human liver.' and \
    Q10B_LEAD == 'A woman drank two 175 ml standard glasses of wine labelled 12.5% (v/v).', (Q10B, Q10B_LEAD)
_ferm, _fb10, _ald = raw(14, 306, 321, 140, 340), raw(14, 306, 321, 400), raw(14, 328, 342, 140, 300)
assert _ferm == 'C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂' and _fb10 == 'FORMULAS // BALANCING: (4, 3)' and \
    _ald == 'ethanal (acetaldehyde)' and raw(14, 328, 342, 500) == '(3)', (_ferm, _fb10, _ald)
C.add([k('10', 'b')], 'chem-4-2', 'equation-for-fermenting-glucose', [
    lift('r-1', _ferm, 7, 'WRITE: "' + _fb10 + '".')],
    qtext=Q10B_WRITE, stem=Q10B_GLU, cid='q10-b-equation', ref_suffix='fermentation equation')
C.add([k('10', 'b')], 'chem-4-2', 'the-liver-metabolite-of-ethanol', [lift('r-1', _ald, 3, 'NAME.')],
      qtext=Q10B_NAME, stem=Q10B_GLU + ' ' + Q10B_RATE, cid='q10-b-metabolite', ref_suffix='the primary metabolite')
_q10b = [(it.cell, display(it.text)) for it in P.items(k('10', 'b'))]
assert _q10b[1:] == [('[9]', '6.6 hours'), ('[3]', '12.5 % of 350 ml = 43.75 ml ethanol'), ('[3]', '43.75 × 0.8 = 35 g'),
                     ('[3]', '35 ÷ 5.3 = 6.6 hours'), ('[6]', '112.5 mg/100 ml blood'),
                     ('[3]', '90 % of 35 g = 31.5 g ethanol'), ('[3]', '31.5 g in 28 l = 112.5 mg/100 ml')], _q10b
_pen = P.items(k('10', 'b'))[-1].asides
assert _pen == ['[Penalty of 3 marks if calculated using man’s rate]'], _pen
Q10B_WINE = Q10B_GLU + ' ' + Q10B_RATE + ' ' + Q10B_LEAD
C.add([k('10', 'b', 'i')], 'chem-1-4', 'time-for-the-liver-to-process-two-glasses-of-wine', [
    lift('r-1', _q10b[2][1], 3, 'The scheme gives the answer, "6.6 hours", priced (9), then three steps (3) each, '
         'under "CALC:" with no "(i)".'),
    lift('r-2', _q10b[3][1], 3),
    lift('r-3', _q10b[4][1], 3)], stem=Q10B_WINE)
C.add([k('10', 'b', 'ii')], 'chem-1-4', 'maximum-blood-ethanol-concentration', [
    lift('r-1', _q10b[6][1], 3, 'The scheme gives the answer, "112.5 mg/100 ml blood", priced (6), then two steps (3) '
         'each, after (i)\'s with no "(ii)".'),
    lift('r-2', _q10b[7][1], 3, 'The scheme adds: ' + _pen[0])], stem=Q10B_WINE)
# (c): the paper prints (5), (8), (6) and (6) after four asks; the second sets (i) and
# (ii) inside one sentence. WHAT (3 + 2); DEFINE (i) (3 + 2), two wordings, the second
# after "or", and (ii) (3); WRITE (2 × 3), the nuclear equation in glyphs the text
# layer misreads (scheme page 14, y 696-714), so the row is the paper's ask and the
# scheme's print its answer; EXPL (6), read welded to WRITE's glyphs: its own line.
Q10C = P.ask(k('10', 'c'))
Q10C_ISO, _r = cut(Q10C, 'Define (i)')
Q10C_DEF, _r = cut(_r, 'Carbon–14 decays')
Q10C_BETA, Q10C_SHOE = cut(_r, 'The world')
assert Q10C_ISO == 'What are isotopes?' and Q10C_DEF == 'Define (i) radioactivity, (ii) radioisotope.' and \
    Q10C_BETA.endswith('describe beta-decay of the carbon–14 nucleus.') and Q10C_SHOE.endswith('the shoe was made.'), Q10C
_q10c = P.items(k('10', 'c'))
_iso = [display(x).strip() for x in _q10c[0].text.split('//')]
assert [it.cell for it in _q10c] == ['[3 + 2]'] and len(_iso) == 2, _q10c
C.add([k('10', 'c')], 'chem-1-2', 'isotopes', [
    lift('r-1', _iso[0], None, 'WHAT. The scheme prices its two points (3 + 2).'), lift('r-2', _iso[1], None)],
    kind='orderedSplit', notation='[3 + 2]', total=5, notes=SPLIT.format('[3 + 2]'), qtext=Q10C_ISO, stem='',
    cid='q10-c-isotopes', ref_suffix='isotopes')
_q10c1 = P.items(k('10', 'c', 'i'))
_d1 = [display(x).strip() for x in _q10c1[0].text.split('//')]
_d2 = [display(x).strip() for x in _q10c1[1].text.split('//')]
assert [it.cell for it in _q10c1] == ['[3 + 2]', '[3 + 2]'] and len(_d1) == 2 and len(_d2) == 2 and \
    raw(14, 608, 622, 220, 260) == 'or', (_d1, _d2)
C.add([k('10', 'c', 'i')], 'chem-1-2', 'radioactivity', [
    menu_row('r-1', [_d1[0], _d2[0]], 1, 'For (i). One of these wordings, the scheme setting the second after "or"; it '
             'prices the two points of each (3 + 2).'),
    menu_row('r-2', [_d1[1], _d2[1]], 1, 'And the second point of that same wording.')],
    kind='orderedSplit', notation='[3 + 2]', total=5, notes=SPLIT.format('[3 + 2]'), qtext=Q10C_DEF, stem='')
_q10c2 = P.items(k('10', 'c', 'ii'))
assert [it.cell for it in _q10c2] == ['[3]', '[2 × 3]', '[6]'] and _q10c2[2].asides == ['[Accept β for e]'], _q10c2
C.add([k('10', 'c', 'ii')], 'chem-1-2', 'radioisotope', [lift('r-1', _q10c2[0].text, 3, 'For (ii).')],
      qtext=Q10C_DEF, stem='')
Q10C_BETA_ASK = cut(Q10C_BETA, 'Write a balanced')[1]
C.add([k('10', 'c')], 'chem-1-2', 'beta-decay-of-carbon-14', [
    C.mark_ask(point('r-1', Q10C_BETA_ASK, 6, 'The scheme answers with the nuclear equation, its mass and atomic numbers '
                     'set above and below each symbol, and prices it (2 × 3); its own print is shown with the answer. '
                     'It adds: ' + _q10c2[2].asides[0]))],
    qtext=Q10C_BETA, stem='', figure=S + 'q10c-write', cid='q10-c-beta-decay', ref_suffix='beta-decay equation')
_c14 = raw(14, 740, 754, 140, 400)
assert _c14 == 'carbon–14 decayed (changed to nitrogen)', _c14
C.add([k('10', 'c')], 'chem-1-2', 'radiocarbon-and-the-oldest-shoe', [lift('r-1', _c14, 6, 'EXPL.')],
      qtext=Q10C_SHOE, stem='', figure=FIG + 'paper-q10c', cid='q10-c-shoe', ref_suffix='the shoe leather')

# ── Q11 Any two of (a), (b), (c) ─────────────────────────────────────────────
# (a): BOD (4 + 3); (i) DESC and (ii) EXPL each price three points (6 + 3): any two.
C.ordered([k('11', 'a')], 'chem-4-3', 'biochemical-oxygen-demand', stem='')
Q11A_LEAD = P.lead(k('11', 'a'))
assert Q11A_LEAD == 'The BOD of a raw sewage sample was 350 ppm and the BOD of the same sample after treatment was ' \
                    'about 25 ppm.', Q11A_LEAD
_q11a1 = P.items(k('11', 'a', 'i'))
_prim = [display(x).strip() for x in _q11a1[0].text.split('//')]
assert [it.cell for it in _q11a1] == ['[6 + 3]'] and len(_prim) == 3, _q11a1
C.add([k('11', 'a', 'i')], 'chem-4-3', 'primary-sewage-treatment', [
    menu_row('r-1', _prim, 2, 'Any two of these, the first (6), the second (3): the scheme lists three points and '
             'prices them "(6 + 3)".', per=6, steps=[6, 3], total=9)], total=9, stem=Q11A_LEAD)
_q11a2 = P.items(k('11', 'a', 'ii'))
_sec = [display(x).strip() for x in _q11a2[0].text.split('//')]
assert [it.cell for it in _q11a2] == ['[6 + 3]', None] and len(_sec) == 3, _q11a2
_ox = traced(display(_q11a2[1].text))
assert _ox == '*Marks can only be given once for ‘oxidation.’', _ox
C.add([k('11', 'a', 'ii')], 'chem-4-3', 'secondary-sewage-treatment', [
    menu_row('r-1', _sec, 2, 'Any two of these, the first (6), the second (3): the scheme lists three points and '
             'prices them "(6 + 3)". It adds: "' + _ox + '"', per=6, steps=[6, 3], total=9)], total=9, stem=Q11A_LEAD)
# (b): (i) DIST (4 + 3); (ii) WHY (2 × 3); (iii) SHOW (2 × 3) and DESC (2 × 3), two
# points or after "or" a second pair, printed (12) once.
C.ordered([k('11', 'b', 'i')], 'chem-2-1', 'ionic-and-polar-covalent-bonding')
C.fixed([k('11', 'b', 'ii')], 'chem-2-1', 'why-ionic-substances-conduct-when-molten')
_q11b3 = P.items(k('11', 'b', 'iii'))
assert [it.cell for it in _q11b3] == ['[2 × 3]'] * 3 and raw(15, 596, 610, 200, 230) == 'or', _q11b3
_show = [display(x).strip() for x in _q11b3[0].text.split('//')]
_dsc1 = [display(x).strip() for x in _q11b3[1].text.split('//')]
_dsc2 = [display(x).strip() for x in _q11b3[2].text.split('//')]
assert len(_show) == len(_dsc1) == len(_dsc2) == 2, (_show, _dsc1, _dsc2)
C.add([k('11', 'b', 'iii')], 'chem-2-2', 'polar-bonds-in-ammonia-and-its-solubility', [
    lift('r-1', _show[0], 3, 'SHOW. The scheme prices these points (2 × 3), one each.'),
    lift('r-2', _show[1], 3),
    menu_row('r-3', [_dsc1[0], _dsc2[0]], 1, 'DESC: one of these, (3), the scheme setting the second pair after "or"; '
             'it prices the two points of each (2 × 3), one each.', per=3, total=3),
    menu_row('r-4', [_dsc1[1], _dsc2[1]], 1, 'And the second point of that same pair, (3).', per=3, total=3)],
    total=12)
# (c)A: Teflon. Roy Plunkett's portrait (paper page 7, x 432-510, crop 'paper-q11c-a').
Q11CA = FIG + 'paper-q11c-a'
C.fixed([ka('11', 'c', 'i', 'A')], 'chem-4-2', 'the-monomer-of-teflon', figure=Q11CA)
C.fixed([ka('11', 'c', 'ii', 'A')], 'chem-4-2', 'how-teflon-is-polymerised', figure=Q11CA)
# (iii): DRAW (6): the two units drawn in full (scheme page 16, x 150-228), then after
# "/" as formulas.
_qa3 = P.items(ka('11', 'c', 'iii', 'A'))
assert [(it.cell, display(it.text)) for it in _qa3] == [('[6]', '/ – CF₂ – CF₂ – CF₂ – CF₂ – [End bonds not reqd.]')], _qa3
C.add([ka('11', 'c', 'iii', 'A')], 'chem-4-2', 'repeating-units-of-teflon', [
    lift('r-1', '– CF₂ – CF₂ – CF₂ – CF₂ –', 6, 'Or the two units drawn in full, as the scheme draws them before "/", '
         'shown with the answer. It adds: [End bonds not reqd.]')], figure=S + 'q11c-a-iii')
# (iv): GIVE "first property // use of first // second property // use of second (4 ×
# 3)", from the scheme's table of five properties and their uses (page 16, y 200-337).
_give = raw(16, 180, 195, 70, 440)
assert _give == '(iv) GIVE: first property // use of first // second property // use of second', _give
_tb = ((217, 242), (247, 260), (265, 290), (294, 319), (324, 337))
_prop = [rows(16, a, b, 120, 290) for a, b in _tb]
_use = list(dict.fromkeys(rows(16, a, b, 295, 480) for a, b in _tb))
assert _prop == ['Inert (unreactive, stable)', 'Temperature tolerant', 'Hydrophobic (repellent, non-stick)',
                 'Corrosion resistant', 'Low friction'] and len(_use) == 4, (_prop, _use)
C.add([ka('11', 'c', 'iv', 'A')], 'chem-4-2', 'properties-and-uses-of-teflon', [
    menu_row('r-1', _prop, 2, 'GIVE: "' + _give[len('(iv) GIVE: '):] + ' (4 × 3)": two properties from the scheme\'s '
             'table, (3) each.', per=3, total=6),
    menu_row('r-2', _use, 2, 'And the use the table sets beside each property named, (3) each.', per=3, total=6)],
    total=12, figure=S + 'q11c-a-iv')
# (c)B: ozone. OUTLINE (4 + 3), the words of each point then after "/" its equation
# in glyphs the text layer misreads (scheme page 16, y 387-449); WHY (3): a card each,
# the paper asking them in two sentences under one mark (10).
Q11CB_OUT, Q11CB_WHY = cut(P.ask(ka('11', 'c', None, 'B')), 'Why is ozone')
Q11CB_LEAD = P.lead(ka('11', 'c', None, 'B'))
assert Q11CB_OUT.endswith('ozone gas in the stratosphere.') and Q11CB_LEAD.startswith('The destruction of the ozone'), \
    (Q11CB_OUT, Q11CB_LEAD)
_qb = P.items(ka('11', 'c', None, 'B'))
assert [it.cell for it in _qb] == ['[4 + 3]', '[3]'], _qb
_o1 = raw(16, 386, 400, 140) + ' ' + raw(16, 402, 418, 140, 270).split(' / ')[0]
_o2 = raw(16, 421, 435, 140).rstrip('/ ')
assert _o1 == 'decomposition of oxygen molecule into oxygen atoms (radicals) by high-energy ultraviolet (uv) light' and \
    _o2 == 'reaction of oxygen atom (radical) with oxygen molecule forming ozone', (_o1, _o2)
C.add([ka('11', 'c', None, 'B')], 'chem-4-3', 'how-ozone-forms-in-the-stratosphere', [
    lift('r-1', _o1, None, 'OUTLINE. The scheme prices its two points (4 + 3), and after "/" gives each as an '
         'equation; its own print is shown with the answer.'),
    lift('r-2', _o2, None)],
    kind='orderedSplit', notation='[4 + 3]', total=7, notes=SPLIT.format('[4 + 3]'), qtext=Q11CB_OUT, stem='',
    figure=S + 'q11c-b', cid='q11-c-b-outline', ref_suffix='ozone in the stratosphere')
C.add([ka('11', 'c', None, 'B')], 'chem-4-3', 'why-ozone-does-not-form-low-down', [
    lift('r-1', _qb[1].text, 3, 'WHY.')],
    qtext=Q11CB_WHY, stem=Q11CB_OUT, cid='q11-c-b-why', ref_suffix='ozone in the lower atmosphere')
C.fixed([ka('11', 'c', 'i', 'B')], 'chem-4-3', 'what-cfcs-are', stem=Q11CB_LEAD)
C.fixed([ka('11', 'c', 'ii', 'B')], 'chem-4-3', 'why-cfcs-last-in-the-lower-atmosphere', stem=Q11CB_LEAD)
C.fixed([ka('11', 'c', 'iii', 'B')], 'chem-4-3', 'a-former-use-of-cfcs', stem=Q11CB_LEAD)
C.fixed([ka('11', 'c', 'iv', 'B')], 'chem-4-3', 'the-oxide-that-destroys-ozone', stem=Q11CB_LEAD,
        row_notes={0: 'NAME.', 1: 'GIVE.'})


# A charge the scheme sets as a macron ("Cl¯", "HSO₄¯", "A¯") is shown as the minus it
# prints; a script run the text layer sets apart from what it closes ("(CH₃ •)") is
# shown as the page sets it. The gate reads both alike, checked again here.
def _clean(t):
    t2 = re.sub(r'(?<=[A-Za-z₀-₉)\]])¯', '⁻', t)
    t2 = re.sub(r'([₀-₉]) •', r'\1•', t2)
    if t2 != t and not P.traceable(t2):
        raise Refused(f'"{t2}" is not in the 2011 hl scheme')
    return t2


for _c in C.cards:
    for _r in _c['rows']:
        if not _r.get('ask'):
            _r['verbatim'] = _clean(_r['verbatim'])
        if _r.get('contextNote'):
            _r['contextNote'] = re.sub(r'(?<=[A-Za-z₀-₉)\]])¯', '⁻', _r['contextNote'])
        if _r.get('group'):
            _r['group']['options'] = [_clean(o) for o in _r['group']['options']]
            _r['verbatim'] = _r['group']['options'][0]

# A note quoted from the scheme in the reader's script notation ("A_(r)") is shown
# as the page sets it.
for _c in C.cards:
    for _r in _c['rows']:
        if '_(' in (_r.get('contextNote') or '') or '^(' in (_r.get('contextNote') or ''):
            _r['contextNote'] = display(_r['contextNote'])
            assert '_(' not in _r['contextNote'] and '^(' not in _r['contextNote'], _r


# ── review ───────────────────────────────────────────────────────────────────
def printed():
    """Every letter's printed marks: the paper sets one mark after a letter's
    last part, or several, one after each run of asks."""
    out = {}
    for key, last in P.marks.items():
        if not key[1]:
            continue
        at = [m for s in P.pseg if s.key[:2] == key[:2] for _n, m in s.marks_at]
        out[key[:2]] = sum(at) if at else last
    # Three marks print in one run with the words before them, and the reader keeps
    # them with the ask, not as marks after a run: Q5(b)'s "(12)" ("Explain why he did
    # this.(12)", paper page 4, y 623; asserted on Q5B above), Q10(b)'s "(7)" ("... this
    # fermentation reaction. (7)", page 6, y 511) and Q11(c)B(iv)'s first "(3)" ("... in
    # the stratosphere. (3)", page 7, y 691).
    assert ('5', 'b') not in out
    out[('5', 'b')] = 12
    assert [m for s in P.pseg if s.key[:2] == ('10', 'b') for _n, m in s.marks_at] == [3, 15], P.pseg
    out[('10', 'b')] += 7
    assert P.pseg_of(ka('11', 'c', 'iv', 'B')).marks_at[-1][1] == 3 and out[('11', 'c')] == 47, out
    out[('11', 'c')] += 3
    return out


def review():
    out = []
    for c in C.cards:
        out.append(f"{c['id']} | {c['questionRef']} | {c['totalMarks']} "
                   f"{c['tariffModel']['kind']} {c['tariffModel'].get('notation', '')} | {c['topicId']}")
    out.append('')
    for key, reason in EXCLUDED:
        out.append(f'EXCLUDED {C.ref([key])}: {reason}')
    got = {}
    for c in C.cards:
        key = tuple(c['keys'][0][:2])
        if key[0] != '4':
            got[key] = got.get(key, 0) + c['totalMarks']
    marks = printed()
    for key in sorted(set(got) | set(marks), key=lambda kv: (int(kv[0]), kv[1] or '')):
        if key == ('4', None):
            continue
        line = f'Q{key[0]}({key[1]}) printed {marks.get(key)}, carded {got.get(key)}'
        if key == ('11', 'c'):
            line += ' (A and B are alternatives, 25 each; the paper prints each one\'s marks, 2 x 25)'
        out.append(line)
    q4 = [c for c in C.cards if c['keys'][0][0] == '4']
    out.append(f'Q4 printed 50 for eight of eleven items, six each and one more to the best two; '
               f'carded {len(q4)} cards, (a)-(j) and (k) as A and B, {sorted({c["totalMarks"] for c in q4})} each')
    for key, ask, s in dict.fromkeys(P.inexact):
        out.append(f'PAPER≠REPRINT {key}: paper "{ask}" / scheme "{s}"')
    return '\n'.join(out)


def exclusions():
    return []


if __name__ == '__main__':
    problems = make_audit(MAX_OPTIONS)(C.cards)
    for p in problems:
        print('AUDIT', p, file=sys.stderr)
    if '--exclusions' in sys.argv:
        print(json.dumps(exclusions(), ensure_ascii=False, indent=1))
    elif '--review' in sys.argv:
        print(review())
    else:
        print(json.dumps(C.finish(), ensure_ascii=False, indent=1))
    sys.exit(1 if problems else 0)
