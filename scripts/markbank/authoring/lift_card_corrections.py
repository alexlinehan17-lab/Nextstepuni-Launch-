"""Lift corrected card text from the SEC papers, for card-corrections.json.

    python3 scripts/markbank/authoring/lift_card_corrections.py

Produced the 2026-09-15 corrections for econ-2025-hl-q14-a-iii-{agri,sport},
am-2021-ol-1-*, maths-2022-hl-p2-q10-c, maths-2024-hl-p1-q2-b and
bio-2022-ol-q6-*, then am-2021-ol-6-a-ii, am-2021-ol-7-a-ii, am-2022-ol-1-*,
am-2025-hl-2 and am-2025-hl-7-b-*, and prints them as JSON in
card-corrections.json's shape. Every string was then checked by independent
readers against the rendered page, with no difference found.

Every string written here is cut out of the paper PDF by the pipeline's own
readers and repaired with the pipeline's own glyph maps. Nothing is typed.
Each lift asserts what it expects to find, so a wrong page or block stops the
script instead of writing a wrong correction. Needs the papers (and the maths
and applied-maths schemes) fetched with fetch-corpus.py.
"""
import json
import os
import re
import sys
import unicodedata

AUTH = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(AUTH)))
sys.path.insert(0, AUTH)
sys.path.insert(0, os.path.join(ROOT, 'scripts/markbank'))
sys.argv = ['lift']

import fitz  # noqa: E402
from markbank_text import unligature  # noqa: E402
from derive_glyphs import LIGATURE as GLYPHS  # noqa: E402

ws = lambda s: re.sub(r'\s+', ' ', s.replace('\xa0', ' ')).strip()


def glyphs(s):
    for bad, good in GLYPHS.items():
        s = s.replace(bad, good)
    return unligature(s)


def blocks(pdf, page_no):
    page = fitz.open(pdf)[page_no - 1]
    return sorted(page.get_text('blocks'), key=lambda b: (round(b[1]), b[0]))


def block_with(bs, needle):
    hits = [b[4] for b in bs if needle in ws(b[4])]
    assert len(hits) == 1, (needle, len(hits))
    return hits[0]


out = {}


def correct(subject, cid, reason, **fields):
    out.setdefault(subject, {})[cid] = {'reason': reason, 'set': fields}


# --- Economics 2025 HL Q14(a)(iii) -------------------------------------------
pdf = os.path.join(ROOT, 'examiner-reports/economics/papers/2025-hl-paper.pdf')
bs = blocks(pdf, 26)
part = ws(glyphs(block_with(bs, 'Online shopping shows how advances in technology')))
assert part.startswith('(iii) '), part[:20]
part = part[len('(iii) '):]
cut = part.index('. ') + 1
context, ask = part[:cut], part[cut:].strip()
assert context.startswith('Online shopping shows') and ask.startswith('Outline one other way'), (context, ask)
assert '(✓)' in ask, ask
options = [ws(line) for line in block_with(bs, 'Sports and fitness').split('\n') if ws(line)]
assert options == ['Agriculture', 'Sports and fitness'], options
for cid, option in (('econ-2025-hl-q14-a-iii-agri', options[0]), ('econ-2025-hl-q14-a-iii-sport', options[1])):
    correct('economics', cid,
            'The authored question reworded the paper (it dropped "one other way" and the printed '
            'context the ask depends on). Restored word for word from the 2025 Higher Level paper, '
            'page 26, Q14(a)(iii): the context sentence as the stem, the ask and the tick '
            'instruction as the question, and this card\'s own printed sector option.',
            stem=context, questionText=f'{ask}\n{option}')

# --- Applied Maths 2021 OL Q1 --------------------------------------------------
import am_all  # noqa: E402
import am_scheme  # noqa: E402
import mathtext  # noqa: E402

A = am_all.Author(2021, 'ol')
raw = ws(A.P.stem(1, None) or '')
at = raw.index(' Calculate ')
car_raw, calc = raw[:at], raw[at + 1:at + 1 + len('Calculate')]
# The motorbike paragraph from its own printed block: the reader's stem runs on
# past it into the next question's diagram label ("100 m").
moto_raw = ws(block_with(blocks(os.path.join(ROOT, 'examiner-reports/applied-maths/papers/2021-ol-paper.pdf'), 2),
                         'Later, a motorbike passes P'))
assert car_raw.startswith('The points P and Q lie 1 km apart') and car_raw.endswith('rest at Q.'), car_raw[-40:]
assert moto_raw.startswith('Later, a motorbike') and moto_raw.endswith('P to Q.'), moto_raw[-40:]
render = lambda piece: am_all.FURNITURE_TAIL.sub('', am_scheme.repair(mathtext.clean_like(A.P.files, piece))).strip()
car, moto = render(car_raw), render(moto_raw)
assert '^(–1)' in car and 'one minute' in moto, (car, moto)
for roman in ('i', 'ii', 'iii', 'iv'):
    correct('applied-maths', f'am-2021-ol-1-{roman}',
            'The stem ran every sibling ask into one sentence and dropped the end of the motorbike '
            'paragraph. Rebuilt from the 2021 Ordinary Level paper, page 2, Question 1, block by '
            'block through the same span-aware reader: the car scenario and the printed '
            '"Calculate" that governs (i)-(iv).',
            stem=f'{car} {calc}')
for roman in ('v', 'vi'):
    correct('applied-maths', f'am-2021-ol-1-{roman}',
            'The stem ran every sibling ask into one sentence and cut the motorbike paragraph off '
            'before "It continues at this speed until it passes Q. The motorbike takes one minute '
            'to travel from P to Q.", which (v) and (vi) depend on. Rebuilt from the 2021 Ordinary '
            'Level paper, page 2, Question 1, block by block through the same span-aware reader.',
            stem=f'{car} {moto}')

# --- Maths 2022 HL Paper 2 Q10(c) ----------------------------------------------
import maths_lib  # noqa: E402

M22 = maths_lib.Author(2022, 'hl')
P2 = M22.P[2]
pdf = os.path.join(ROOT, 'examiner-reports/maths/papers/2022-hl-200-paper.pdf')
bs = blocks(pdf, 29)
ask_raw = ws(block_with(bs, 'Find the probability that at most'))
context = M22.question((2, 10, 'c', None))
assert context.startswith('20 relay teams') and context.endswith('0∙1.'), context
ask = ws(mathtext.clean_like(P2.files, ask_raw))
assert ask.startswith('Find the probability that at most') and ask.endswith('4 decimal places.'), ask
correct('maths', 'maths-2022-hl-p2-q10-c',
        'The question stopped after the printed context and lost the ask set in its own block '
        'beneath it. Restored from the 2022 Higher Level Paper 2, page 29, Q10(c), each block read '
        'through the same span-aware reader and joined in printed order.',
        questionText=f'{context} {ask}')

# --- Maths 2024 HL Paper 1 Q2(b) -----------------------------------------------
M24 = maths_lib.Author(2024, 'hl')
current = M24.question((1, 2, 'b', None))
assert current == 'Use de Moivre’s theorem to write (1 −√3 i) 9 in the form a+ b, where a, b∈ℝ.', current
page = fitz.open(os.path.join(ROOT, 'examiner-reports/maths/papers/2024-hl-100-paper.pdf'))[5]
line = [s for s in page.get_texttrace() if 'Cambria' in s['font'] and 428 < s['bbox'][1] < 452]
line.sort(key=lambda s: s['bbox'][0])
read = lambda s: ''.join(chr(c[0]) for c in s['chars'] if c[1] != -1)
# The exponent: the one span on this line set smaller and higher than the rest.
body = max(s['size'] for s in line)
small = [s for s in line if s['size'] < body * 0.8]
assert len(small) == 1 and read(small[0]) == '9', [read(s) for s in small]
exponent = read(small[0]).translate(str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹'))
# The form: the maths glyphs after "in the form", folded the way every maths
# card spells them. Glyph #1861 is the same glyph Q2(a) prints as i.
after = [s for s in line if s['bbox'][0] > small[0]['bbox'][0] and s['size'] == body]
form = ''.join(unicodedata.normalize('NFKC', read(s)) for s in after[:4])  # a | + | b | i
assert form == 'a+bi', form
fixed = current.replace(' 9 in', f'{exponent} in', 1).replace('a+ b,', f'{form[:2]} {form[2:]},', 1)
assert fixed != current and fixed.count('⁹') == 1 and 'a+ bi,' in fixed, fixed
correct('maths', 'maths-2024-hl-p1-q2-b',
        'The PDF text layer flattens the exponent and reads the i of "a + bi" as a second b. The '
        'glyph trace of the 2024 Higher Level Paper 1, page 6, Q2(b) prints a raised 9 after the '
        'bracket and glyph #1861 (the i of Q2(a)) after the b; this restores both and changes no '
        'word.',
        questionText=fixed)

# --- Biology 2022 OL Q6 ----------------------------------------------------------
pdf = os.path.join(ROOT, 'examiner-reports/biology/papers/2022-ol-038-paper.pdf')
bs = blocks(pdf, 7)
head = ws(glyphs(block_with(bs, 'State whether each of the following statements is true or false')))
assert head.startswith('6. '), head[:10]
head = head[len('6. '):]
assert '(✓)' in head and head.endswith('in each case.'), head
for letter in 'abcdefg':
    correct('biology', f'bio-2022-ol-q6-{letter}',
            'Each statement card showed the bare statement with no instruction. Restored the '
            'question\'s printed instruction from the 2022 Ordinary Level paper (Sections A and B), '
            'page 7, Question 6, as the stem shared by every statement.',
            stem=head)


# === 2026-09-15, second set: Applied Maths stems that carried other parts =====

AM_PAPERS = os.path.join(ROOT, 'examiner-reports/applied-maths/papers')
am_block = lambda year, level, page, needle: ws(block_with(blocks(os.path.join(AM_PAPERS, f'{year}-{level}-paper.pdf'), page), needle))
AM_REASON = ('The stem carried other parts’ asks or lost what this part depends on. Rebuilt from the {paper}, '
             'page {page}, {q}, block by block through the same span-aware reader{extra}.')

# --- 2021 OL Q6(a)(ii) and Q7(a)(ii): scenario, then the printed "Find" ---------
for cid, page, needle, label, q in (
        ('am-2021-ol-6-a-ii', 4, 'Particles of weight 3', '6. (a) ', 'Question 6(a)'),
        ('am-2021-ol-7-a-ii', 5, 'A uniform beam AB of length 5', '7. (a) ', 'Question 7(a)')):
    first = am_block(2021, 'ol', page, needle)
    assert first.startswith(label), first[:12]
    pieces = [first[len(label):]]
    if cid == 'am-2021-ol-6-a-ii':
        pieces.append(am_block(2021, 'ol', page, 'The co‐ordinates of the centre of gravity'))
    find = am_block(2021, 'ol', page, 'Find (i) the value of')
    assert find.startswith('Find '), find
    stem = ' '.join(render(p) for p in pieces) + ' ' + find[:len('Find')]
    correct('applied-maths', cid, AM_REASON.format(paper='2021 Ordinary Level paper', page=page, q=q,
            extra=': the setup and the printed "Find" that governs (i) and (ii)'), stem=stem)

# --- 2022 OL Q1: the car scenario; (vi) also the motorcycle paragraph ------------
# Read line by line (exponents marked by mathtext.line_text) rather than through
# clean_like: clean_like's window re-reads the page and sets the question number
# back into the middle of the first sentence -- "in a time 1. of 5 s", the very
# fault being corrected.
doc22 = fitz.open(os.path.join(AM_PAPERS, '2022-ol-paper.pdf'))


def block_lines(doc, page_no, needle):
    hits = []
    for b in doc[page_no - 1].get_text('dict')['blocks']:
        lines = [ws(mathtext.line_text(ln)) for ln in b.get('lines', [])]
        if needle in ' '.join(lines):
            hits.append(ws(am_scheme.repair(' '.join(t for t in lines if t))))
    assert len(hits) == 1, (needle, len(hits))
    return hits[0]


first = block_lines(doc22, 2, 'A car starts from rest at point P')
assert first.startswith('1. '), first[:6]
car = [first[len('1. '):], block_lines(doc22, 2, 'The total time for the journey from P to Q')]
moto = block_lines(doc22, 2, 'A motorcycle passes point P')
assert ' 1. ' not in car[0] and 'in a time of 5 s' in car[0] and '^(–1)' in car[0], car[0]
assert car[0].endswith('rest at point Q.') and car[1].endswith('35 s.') and moto.endswith('as the car.'), (car, moto)
for roman in ('ii', 'iii', 'iv', 'v'):
    correct('applied-maths', f'am-2022-ol-1-{roman}',
            AM_REASON.format(paper='2022 Ordinary Level paper', page=2, q='Question 1',
                             extra=': the car scenario, without the question number and the other parts’ asks'),
            stem=' '.join(car))
correct('applied-maths', 'am-2022-ol-1-vi',
        AM_REASON.format(paper='2022 Ordinary Level paper', page=2, q='Question 1',
                         extra=': the car scenario and the motorcycle paragraph (vi) depends on, which the old stem left out'),
        stem=' '.join(car + [moto]))

# --- 2025 HL: stacked fractions read by mathtext's fraction reader ------------------
A25 = am_all.Author(2025, 'hl')
render25 = lambda piece: am_all.FURNITURE_TAIL.sub('', am_scheme.repair(mathtext.clean_like(A25.P.files, piece))).strip()
doc25 = fitz.open(os.path.join(AM_PAPERS, '2025-hl-paper.pdf'))


def lines25(page_no):
    """[(y, x, text)] -- each printed line, exponents marked, in reading order."""
    out = []
    for b in doc25[page_no - 1].get_text('dict')['blocks']:
        for ln in b.get('lines', []):
            t = ws(mathtext.line_text(ln))
            if t:
                out.append((ln['bbox'][1], ln['bbox'][0], t))
    return out


def line25(page_no, start):
    hits = [t for _, _, t in lines25(page_no) if t.startswith(start)]
    assert len(hits) == 1, (page_no, start, hits)
    return hits[0]


def frac25(page_no, needle):
    hits = [ws(f[3]) for f in mathtext.fractions(doc25[page_no - 1]) if needle in f[3]]
    assert len(hits) == 1, (page_no, needle, hits)
    return hits[0]


# Q2: a whole-question card. Stem = the setup; question = every part in order.
setup = render25(am_block(2025, 'hl', 6, 'moves vertically upwards through the air'))
assert setup.startswith('A particle of mass') and setup.endswith('s₀ = 0.'), setup
p_i = frac25(6, 'chain rule')
assert p_i == '(i) Using the chain rule, show that a = v dv/ds.', p_i
p_ii = '(ii) ' + line25(6, 'Use calculus to derive')
model_head = line25(7, 'The model may be improved')
model_tail = frac25(7, 'air resistance as')
assert model_head.endswith('air resistance as') and model_tail.startswith('due to air resistance as '), (model_head, model_tail)
model = model_head + model_tail[len('due to air resistance as'):]
assert model.endswith('as 1/40 mv².'), model
p_iii_head = line25(7, '(iii) Show that the upward motion')
lhs = frac25(7, '392')
assert lhs == '2v/(v² + 392)', lhs
# The right-hand side's fraction, from the glyph trace: "1" then "20" in one span
# twice the line's height, the "20" set back under the "1" -- one over twenty.
stack = [t for t in doc25[6].get_texttrace() if ''.join(chr(c[0]) for c in t['chars'] if c[1] != -1) == '120']
assert len(stack) == 1, len(stack)
xs = [c[3][0] for c in stack[0]['chars'] if c[1] != -1]
assert xs[1] < xs[0] < xs[2] and stack[0]['bbox'][3] - stack[0]['bbox'][1] > 20, (xs, stack[0]['bbox'])
tail_line = line25(7, 'v² + 392 dv = −1')
assert tail_line == 'v² + 392 dv = −1' and line25(7, '20 ds') == '20 ds'
p_iii = f'{p_iii_head} {lhs} dv = −1/20 ds'
p_iv = line25(7, '(iv) Solve this differential equation')
p_v = '(v) ' + line25(8, 'Calculate the greatest height')
p_vi_head = frac25(9, 'By using')
rest = line25(9, 'dt solve a differential equation')
assert p_vi_head == '(vi) By using a = dv/dt solve a differential equation', p_vi_head
p_vi = p_vi_head + rest[len('dt solve a differential equation'):]
assert p_vi.endswith('relates v and t.'), p_vi
correct('applied-maths', 'am-2025-hl-2',
        'The question text flattened its fractions ("a=v dv ds", "−1 20 ds"), repeated (iv) and set (i) in the stem. '
        'Rebuilt from the 2025 Higher Level paper, pages 6-9, Question 2: the setup as the stem, and every part in '
        'printed order with each stacked fraction read by mathtext.fractions (the −1/20 from the glyph trace).',
        stem=setup, questionText=' '.join([p_i, p_ii, model, p_iii, p_iv, p_v, p_vi]))

# Q7(b): the setup for (i)-(ii); (iii) also the restitution coefficient printed above it.
setup7 = render25(ws(A25.P.text(7, 'b', None) or ''))
assert setup7.startswith('Chioma is throwing a basketball') and setup7.endswith('to the horizontal.'), setup7
coeff_head = line25(29, 'The coefficient of restitution between the basketball')
coeff_tail = frac25(29, 'and the wall is')
assert coeff_head.endswith('and the wall is') and coeff_tail == 'and the wall is 3/7.', (coeff_head, coeff_tail)
coeff = coeff_head + coeff_tail[len('and the wall is'):]
for roman in ('i', 'ii'):
    correct('applied-maths', f'am-2025-hl-7-b-{roman}',
            'The stem ended in a cut-off "is" and ran into part (iii). Rebuilt from the 2025 Higher Level paper, '
            'page 28, Question 7(b): the setup this part uses.', stem=setup7)
correct('applied-maths', 'am-2025-hl-7-b-iii',
        'The stem lost the coefficient of restitution (a stacked 3/7) and ran into this part’s own ask. Rebuilt '
        'from the 2025 Higher Level paper, pages 28-29, Question 7(b): the setup and the coefficient sentence printed '
        'above (iii), the fraction read by mathtext.fractions.', stem=f'{setup7} {coeff}')

json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
