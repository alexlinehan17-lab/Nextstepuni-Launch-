#!/usr/bin/env python3
"""Spanish written production: the printed task and the scheme's marking grid.

    python3 scripts/markbank/authoring/es_writing.py 2026 hl     # print both

Higher Section B Q5 (the opinion piece on the article's theme), Higher Section
C (dialogue or letter, then diary or note) and Ordinary Section B (letter, then
note or diary) are answered by writing, and the scheme marks them on a GRID:
Content/Communication and Language bands at Higher Q5, a per-turn or per-point
ladder everywhere else. There is no answer to tick, so these are rubric cards
in the French writing shape (types/markBank.ts FrenchRubric), which the
coordinator approved for Spanish on 11 Nov 2026.

LIFTED, NEVER WRITTEN
---------------------
The task is the paper's own lines (EsPaper.rows), set out as printed: a
dialogue turn or a bullet point starts a line; a wrapped line joins the one it
continues. Every string of the grid is a line, or a run of consecutive lines,
of the scheme's own text layer (examiner-reports/spanish/schemes/<sitting>.md);
build-deck.mjs traces each one back into the scheme and drops the card if any
does not. The only words that are NextStepUni's are the criterion labels
("Turn 1", "Point 1" — the scheme says "Mark each 'turn' individually" and
"There are five points to be made") and the practice notes, which the panel
prints under its own NextStepUni label.
"""
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

from es_scheme import schemes_dir                               # noqa: E402

# ---------------------------------------------------------------- the paper -
FURNITURE = re.compile(
    r'^(?:Leaving Certificate Examination \d{4}|Spanish\s*[–-]|_{6,}|\.{6,}|'
    r'Do not write on this page|There is no examination material)', re.I)
# Where a task's own lines end: the "OR" between alternatives, the next
# lettered alternative or question, a section head, an answer-page pointer, or
# the end matter.
TASK_END = re.compile(
    r'^(?:OR|Question\s+\d|Q\s*\.?\s*\d|\d\s*\.\s|\(\s*[a-c]\s*\)\s|SECTION\s+[A-C]\b|'
    r'Section\s+[A-C]\s|Copyright notice|Acknowledgements|PLEASE WRITE|WRITE YOUR ANSWER|'
    r'Write your answer|This is space for extra work)', re.I)
# A line that starts a new line of the task as printed: a dialogue turn
# ("Begoña:", "Tú:"), a bullet or dash point, or a bracketed aside.
NEW_LINE = re.compile(r'^(?:[A-ZÁÉÍÓÚÑ][\wáéíóúñ]{0,15}:\s|[•−–\-]\s|\()')
MARKS = re.compile(r'\s*\(\s*\d{1,3}\s*marks?\s*\)\s*', re.I)
HEAD = re.compile(r'^(?:Question\s*(\d)\b\.?|Q\s*\.?\s*(\d)\s*\.?|(\d)\s*\.)\s*', re.I)
LETTER = re.compile(r'^(?:Q\s*\.?\s*\d\s*\.?\s*)?\(\s*([a-c])\s*\)\s*', re.I)


def _set_out(lines):
    """Join wrapped lines; keep a printed line break where the paper starts a
    new turn, point or aside."""
    out = []
    for text in lines:
        if out and not NEW_LINE.match(text):
            out[-1] = f'{out[-1]} {text}'
        else:
            out.append(text)
    return [' '.join(line.split()) for line in out]


def task(P, section, q, letter):
    """{question, stem, pages} for one writing ask, from the paper's rows.

    `stem` is the question's printed head without its tariff ("Answer EITHER
    (a) DIALOGUE CONSTRUCTION or (b) LETTER WRITING"); `question` the task
    itself as printed.
    """
    rows = P.rows
    want_head = lambda t: (HEAD.match(t) and int(next(g for g in HEAD.match(t).groups() if g)) == q)
    # The question's head: the last line before the task that names its
    # number. Higher Section B Q5 IS its head ("5. Escribe en ESPAÑOL …").
    sect_rows = [i for i, (_p, _x, t) in enumerate(rows)
                 if re.match(rf'^(?:SECTION|Section)\s+{section}\b', t)]
    if not sect_rows:
        raise ValueError(f'no Section {section} head on the paper')
    lo = sect_rows[-1]
    head = next((i for i in range(lo, len(rows)) if want_head(rows[i][2])), None)
    if head is None:
        raise ValueError(f'no Section {section} Question {q} head')
    start = head
    if letter:
        start = next((i for i in range(head, len(rows))
                      if LETTER.match(rows[i][2])
                      and LETTER.match(rows[i][2]).group(1).lower() == letter), None)
        if start is None:
            raise ValueError(f'no ({letter}) under Section {section} Question {q}')
    lines, pages = [], []
    head_text = MARKS.sub(' ', rows[head][2]).strip()
    # A head that wraps ("… sobre una de las siguientes" / "afirmaciones.
    # (50 marks)") continues on the next indented line, up to its tariff.
    i = head + 1
    if not MARKS.search(rows[head][2]):
        while i < len(rows) and i < start + (1 if start > head else 0) + 2 and not TASK_END.match(rows[i][2]) \
                and not LETTER.match(rows[i][2]) and rows[i][1] > rows[head][1] + 5:
            head_text = f'{head_text} {MARKS.sub(" ", rows[i][2]).strip()}'
            if MARKS.search(rows[i][2]):
                i += 1
                break
            i += 1
    head_text = HEAD.sub('', head_text).strip()
    if start == head:
        # The head is the task's instruction (Higher B Q5, Ordinary B Q1): the
        # task's own lines start after it.
        first = i
        stem = head_text
    else:
        first = start
        # Lines printed between the head and the first alternative belong to
        # the head: "Question 2 (20 marks)" / "Answer (a) or (b)."
        first_alt = next(k for k in range(i, start + 1) if LETTER.match(rows[k][2]))
        between = [MARKS.sub(' ', rows[k][2]).strip() for k in range(i, first_alt)
                   if not FURNITURE.match(rows[k][2])]
        stem = ' '.join([head_text] + [b for b in between if b]).strip()
    j = first
    while j < len(rows):
        pno, _x, text = rows[j]
        if j > first or start == head:
            # Higher B Q5's statements are its task: "(a) … O (b) … O (c) …".
            b5 = section == 'B' and q == 5
            if (TASK_END.match(text) and not (b5 and (text == 'O' or LETTER.match(text)))) \
                    or (b5 and re.match(r'^\d\s*\.\s', text)):
                if not (j == first and start != head):
                    break
        if FURNITURE.match(text):
            j += 1
            continue
        if j == first and start != head:
            text = LETTER.sub('', text)
        text = MARKS.sub(' ', text).strip()
        if text:
            lines.append(text)
            if pno + 1 not in pages:
                pages.append(pno + 1)
        j += 1
    if start == head and not (section == 'B' and q == 5):
        # Ordinary Q1's head may itself carry the opening of the task
        # ("1. You are planning to go to Spain after the exams. …").
        if len(stem.split()) > 6 and not re.search(r'\b(?:Answer|Attempt)\b', stem):
            lines.insert(0, stem)
            stem = ''
    if section == 'B' and q == 5:
        # The statements are a printed choice, "O" between each pair: one per line.
        question = '\n'.join(' '.join(t.split()) for t in lines)
    else:
        question = '\n'.join(_set_out(lines))
    return {'question': question, 'stem': stem, 'pages': pages}


# --------------------------------------------------------------- the scheme -
def scheme_lines(year, level):
    """[(page, line)] of the scheme's text layer, blank lines dropped."""
    path = os.path.join(schemes_dir(), f'{year}-{level}.md')
    out, page = [], 0
    with open(path, encoding='utf-8') as fh:
        for raw in fh:
            line = raw.rstrip('\n')
            m = re.match(r'^## Page (\d+)$', line)
            if m:
                page = int(m.group(1))
                continue
            s = ' '.join(line.split())
            if s:
                out.append((page, s))
    return out


PAGE_NO = re.compile(r'^\d{1,2}$')
RANGE_END = re.compile(r'\s*(\d{1,2})\s*[–-]\s*(\d{1,2})\s+marks$')
BAND = re.compile(r'^(TOP|MIDDLE|BOTTOM)$')
CRITERION = re.compile(r'^(\d)\.\s+([A-Z][A-Z/ ]+?)\s+(\d{1,2})\s+marks$')
TIMES = re.compile(r'\((\d)\s*x\s*(\d{1,2})\s*m\s*=\s*(\d{1,3})\s*marks\)')
# A ladder entry opens with its marks ("6 marks:", "4 - 5 marks:", "5 marks
# Communicative …") or closes with them ("… Verb(s) correct. 7 - 8 marks",
# "Full message unequivocally conveyed: 8 marks").
OPENS = re.compile(r'^(\d{1,2}(?:\s*-\s*\d{1,2})?)\s+marks?\b:?\s*(.*)$')
CLOSES = re.compile(r'^(.*?)[:\s]\s*(\d{1,2}(?:\s*-\s*\d{1,2})?)\s+marks?$')


def _sentences(lines):
    """Consecutive printed lines joined into the sentences they wrap."""
    out = []
    for s in lines:
        if out and not re.search(r'[.:)]$', out[-1]) and not s.startswith(('•', '-', '–')):
            out[-1] = f'{out[-1]} {s}'
        else:
            out.append(s)
    return out


def _span(lines, start, stop):
    """Lines from the first matching `start` up to (not including) `stop`."""
    i = next(k for k, (_p, s) in enumerate(lines) if start(s))
    j = next((k for k in range(i + 1, len(lines)) if stop(lines[k][1])), len(lines))
    return i, j


def grid_b5(year, level):
    """Higher Section B Q5: Content/Communication and Language, three bands each."""
    L = scheme_lines(year, level)
    i, j = _span(L, lambda s: re.match(r'^Section B:?\s+Question 5\b', s),
                 lambda s: s.startswith('SECTION C'))
    block = L[i:j]
    pages = sorted({p for p, _s in block})
    criteria, notes, cur, band, desc = [], [], None, None, []
    in_note = False
    for _p, s in block[1:]:
        if PAGE_NO.match(s):
            continue
        if in_note:
            notes.append(s)
            continue
        if s.rstrip(':') in ('Note', 'NOTE', 'N.B.'):
            in_note = True
            continue
        m = CRITERION.match(s)
        if m:
            label = m.group(2).strip().title().replace('/C', '/C')
            cur = {'id': 'content' if m.group(1) == '1' else 'language',
                   'label': '/'.join(w.capitalize() for w in m.group(2).strip().split('/')),
                   'maxMarks': int(m.group(3)), 'guidance': [], 'bands': []}
            cur['permittedMarks'] = list(range(cur['maxMarks'] + 1))
            criteria.append(cur)
            continue
        if BAND.match(s):
            band, desc = s.capitalize(), []
            continue
        if band is None:
            continue
        r = RANGE_END.search(s)
        if r:
            body = s[:r.start()].strip()
            if body:
                desc.append(body)
            lo, hi = int(r.group(1)), int(r.group(2))
            cur['bands'].append({'label': band, 'marks': list(range(lo, hi + 1)),
                                 'guidance': desc})
            band, desc = None, []
        else:
            desc.append(s)
    return {'criteria': criteria, 'requirements': _sentences(notes), 'pages': pages,
            'lines': [s for _p, s in block]}


def _ladder(lines):
    """A per-turn/per-point ladder, one entry per printed mark value, each the
    printed lines that make it up joined."""
    out = []
    for s in lines:
        if OPENS.match(s) or (out and re.search(r'marks?$', out[-1]) and not OPENS.match(out[-1])):
            out.append(s)
        elif out:
            out[-1] = f'{out[-1]} {s}'
        else:
            out.append(s)
    return out


def grid_c(year, level, q, letter):
    """Higher Section C: a per-turn (dialogue) or per-point ladder."""
    L = scheme_lines(year, level)
    i, j = _span(L, lambda s: s.startswith('SECTION C'),
                 lambda s: s.startswith('APPENDIX') or s.startswith('LISTENING COMPREHENSION'))
    block = [(p, s) for p, s in L[i:j] if not PAGE_NO.match(s)]
    texts = [s for _p, s in block]
    # The section's own guidelines, printed once above Question 1.
    g0 = next(k for k, s in enumerate(texts) if s.startswith('Guidelines for Section C'))
    g1 = next(k for k, s in enumerate(texts) if re.match(r'^Question 1\b', s))
    guidelines = _sentences(texts[g0 + 1:g1])
    # Question 1's own direction ("When marking this question … broadly
    # adhered to") precedes its options.
    want = re.compile(rf'^Question {q}\s*\(\s*{letter}\s*\)')
    o0 = next(k for k, s in enumerate(texts) if want.match(s))
    o1 = next(k for k in range(o0 + 1, len(texts))
              if texts[k] == 'OR' or texts[k].startswith('Criteria for'))
    option = [texts[o0]] + _sentences(texts[o0 + 1:o1])
    direction = []
    if q == 1:
        d0 = next(k for k, s in enumerate(texts) if re.match(r'^Question 1\s*[.:]\s*When marking', s))
        # The one sentence, however many lines it wraps over.
        direction = _sentences(texts[d0:d0 + 3])[:1]
    c0 = next(k for k in range(o0, len(texts)) if texts[k].startswith(f'Criteria for Question {q}'))
    c1 = next((k for k in range(c0 + 1, len(texts))
               if re.match(r'^Question \d\s*\(', texts[k]) or texts[k].startswith('APPENDIX')), len(texts))
    criteria_head = texts[c0:c0 + 2]
    ladder = _ladder(texts[c0 + 2:c1])
    times = next((TIMES.search(s) for s in option if TIMES.search(s)), None)
    if not times:
        raise ValueError(f'{year} {level} C Q{q}({letter}): no "(n x m = total)" tariff')
    n, per, total = int(times.group(1)), int(times.group(2)), int(times.group(3))
    pages = sorted({p for p, s in block if s in texts[o0:c1] or s in texts[g0:g1]})
    return {'n': n, 'per': per, 'total': total, 'option': option, 'direction': direction,
            'guidelines': guidelines, 'criteriaHead': criteria_head, 'ladder': ladder,
            'pages': pages}


def grid_ol_b(year, level, q, letter):
    """Ordinary Section B: a per-point ladder for the letter, then the note or diary."""
    L = scheme_lines(year, level)
    i, j = _span(L, lambda s: s.startswith('SECTION B'),
                 lambda s: s.startswith('LISTENING') or s.startswith('APPENDIX'))
    block = [(p, s) for p, s in L[i:j] if not PAGE_NO.match(s)]
    texts = [s for _p, s in block]
    head = re.compile(r'^Q\.?\s*1\.' if q == 1 else r'^Q\.?\s*2\.')
    o0 = next(k for k, s in enumerate(texts) if head.match(s))
    o1 = next((k for k in range(o0 + 1, len(texts)) if re.match(r'^Q\.?\s*2\.', texts[k])), len(texts)) \
        if q == 1 else len(texts)
    part = texts[o0 + 1:o1]
    t = next(k for k, s in enumerate(part) if TIMES.search(s))
    lead = _sentences(part[:t + 1])
    ladder = _ladder(part[t + 1:])
    times = TIMES.search(part[t])
    n, per, total = int(times.group(1)), int(times.group(2)), int(times.group(3))
    pages = sorted({p for p, s in block if s in texts[o0:o1]})
    return {'n': n, 'per': per, 'total': total, 'head': texts[o0], 'lead': lead,
            'ladder': ladder, 'section': _sentences(texts[1:next(k for k, s in enumerate(texts) if head.match(s) or re.match(r'^Q\.?\s*1\.', s))]),
            'pages': pages}


def main():
    year, level = int(sys.argv[1]), sys.argv[2]
    from es_paper import EsPaper
    P = EsPaper(year, level)
    asks = ([('B', 5, None), ('C', 1, 'a'), ('C', 1, 'b'), ('C', 2, 'a'), ('C', 2, 'b')]
            if level == 'hl' else [('B', 1, None), ('B', 2, 'a'), ('B', 2, 'b')])
    for section, q, letter in asks:
        t = task(P, section, q, letter)
        print(f'=== {section} Q{q}{f"({letter})" if letter else ""} pages {t["pages"]}')
        print(f'STEM: {t["stem"]}')
        print(t['question'])
        if level == 'hl' and section == 'B':
            g = grid_b5(year, level)
        elif level == 'hl':
            g = grid_c(year, level, q, letter)
        else:
            g = grid_ol_b(year, level, q, letter)
        import json
        for k, v in g.items():
            if k == 'lines':
                continue
            if k == 'criteria':
                for c in v:
                    print(f'  CRIT {c["id"]} {c["label"]!r} /{c["maxMarks"]}')
                    for b in c['bands']:
                        print(f'     {b["label"]} {b["marks"][0]}-{b["marks"][-1]}: {b["guidance"]}')
            elif isinstance(v, list) and v and isinstance(v[0], str):
                print(f'  {k}:')
                for x in v:
                    print(f'     | {x}')
            else:
                print(f'  {k}: {v}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
