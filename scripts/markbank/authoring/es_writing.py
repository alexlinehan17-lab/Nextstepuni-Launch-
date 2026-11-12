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
from itertools import groupby

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

from es_scheme import schemes_dir, X_BULLETS, GLYPHS as SCHEME_GLYPHS  # noqa: E402

# ---------------------------------------------------------------- the paper -
# 2019 Ordinary sets the footer of its Section B page with every word twice:
# "Leaving Leaving Certificate Certificate Examination Examination 2019 2019 8",
# "Spanish Spanish – Written – Written – Ordinary – Ordinary Level Level", under
# the page's number on a row of its own ("8").
FURNITURE = re.compile(
    r'^(?:Leaving Certificate Examination,?\s*\d{4}|Spanish\s*[–-]|_{6,}|\.{6,}|'
    r'Do not write on this page|There is no examination material|'
    r'Leaving Leaving Certificate Certificate Examination|Spanish Spanish\s*[–-]|'
    r'\d{1,2}$)', re.I)
# Where a task's own lines end: the "OR" between alternatives, a section head,
# an answer-page pointer, or the end matter. (The next task or question head
# ends it too; those are found by position, below.)
# "OR" is a line of its own: matched case-insensitively it ended a dialogue at
# "organisation and a very important part of Irish culture" (2023 Higher).
# 2018 Higher heads its answer page "BELOW WRITE YOUR ANSWER TO SECTION A, …".
TASK_END = re.compile(
    r'^(?:OR\s*$|SECTION\s+[A-C]\b|Section\s+[A-C]\s|Copyright notice|Acknowledgements|'
    r'PLEASE WRITE|(?:BELOW\s+)?WRITE YOUR ANSWER|Write your answer|This is space for extra work)')
# A line that starts a new line of the task as printed: a dialogue turn
# ("Begoña:", "Tú:"), a bullet or dash point, or a bracketed aside.
NEW_LINE = re.compile(r'^(?:[A-ZÁÉÍÓÚÑ][\wáéíóúñ]{0,15}(?: [A-ZÁÉÍÓÚÑ][\wáéíóúñ]{0,15})?:\s|[•−–‐\-]\s|\()')
MARKS = re.compile(r'\s*\(\s*\d{1,3}\s*marks?\s*\)\s*', re.I)
# A question's head: "Question 2", "Q 2.", "2." at the start of a line.
QHEAD = re.compile(r'^(?:(?:Question|Q)\s*\.?\s*(\d)\b\.?|(\d)\s*\.(?=\s|\())\s*', re.I)
# A lettered alternative, with or without its question's number in front:
# "(a) …", "Q 1 (a) …", "Question 1 (a) …", "1. (b) …".
LETTERED = re.compile(r'^(?:(?:Question|Q)\s*\.?\s*(\d)\s*\.?\s*|(\d)\s*\.\s*)?\(\s*([a-c])\s*\)\s*(.*)$', re.I)
# The Symbol-font bullet and dash some booklets print, read by glyph: U+F0B7
# is the Symbol bullet, U+F02D the Symbol minus.
GLYPHS = {'\uf0b7': '•', '\uf02d': '−'}


def _text(t):
    for k, v in GLYPHS.items():
        t = t.replace(k, v)
    return ' '.join(t.split())


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


def _summary(rest):
    """A lettered line that only NAMES an alternative ("Question 1 (b) Letter
    OR", "2. (a) Diary Entry or (b) Note. (25 marks)") rather than setting it."""
    rest = MARKS.sub(' ', rest).strip()
    if not rest:
        return False      # "(b)" alone on its line: the task follows (2016 Ordinary)
    return (len(rest.split()) <= 4 or re.search(r'\bOR$', rest)
            or re.search(r'\(\s*[a-c]\s*\)', rest) is not None)


def _task_b5(rows, qheads, lo, hi):
    """Higher Section B Q5: its head ("5. Escribe en ESPAÑOL tu opinión …
    sobre una de las siguientes" / "afirmaciones. (50 marks)") is the stem,
    and the statements under it, with the "O" printed between them, are the
    task, lettered or not."""
    head = qheads.get(5)
    if head is None:
        raise ValueError('no Section B Question 5 head')
    stem = [rows[head][2][QHEAD.match(rows[head][2]).end():]]
    k = head + 1
    if not MARKS.search(rows[head][2]):
        while k < hi and rows[k][1] > rows[head][1] + 5 and not LETTERED.match(rows[k][2]) \
                and not TASK_END.match(rows[k][2]):
            stem.append(rows[k][2])
            k += 1
            if MARKS.search(rows[k - 1][2]):
                break
    lines, pages = [], []
    for j in range(k, hi):
        pno, _x, t = rows[j]
        if FURNITURE.match(t):
            continue
        if (TASK_END.match(t) and t != 'O') or (QHEAD.match(t) and not LETTERED.match(t)):
            break
        t = MARKS.sub(' ', t).strip()
        if t:
            lines.append(t)
            if pno + 1 not in pages:
                pages.append(pno + 1)
    stem = ' '.join(' '.join(MARKS.sub(' ', b) for b in stem).split())
    return {'question': '\n'.join(lines), 'stem': stem, 'pages': pages}


# A paper that letters an alternative other than its own head names it: 2010
# Higher Section C Q2 is headed "2. Answer either (a) DIARY ENTRY or (b) NOTE."
# and prints the note as "(c) You are in Salamanca …". The census reads it as
# (b), as the head does.
PRINTED_LETTERS = {(2010, 'hl', 'C', 2): {'c': 'b'}}


def task(P, section, q, letter):
    """{question, stem, pages} for one writing ask, from the paper's rows.

    `stem` is what the paper prints over the alternatives (the question's head
    without its number and tariff: "Answer EITHER (a) DIALOGUE CONSTRUCTION or
    (b) LETTER WRITING"; in 2021 and 2022 the section's own "Answer ONE of the
    four parts …" and the parts it names); `question` the task itself, set out
    as printed.
    """
    rows = [(p, x, _text(t)) for p, x, t in P.rows]
    heads = [i for i, (_p, _x, t) in enumerate(rows)
             if re.match(rf'^(?:SECTION|Section)\s+{section}\b', t)]
    if not heads:
        raise ValueError(f'no Section {section} head on the paper')
    lo = heads[-1]
    hi = next((i for i in range(lo + 1, len(rows))
               if re.match(r'^(?:SECTION|Section)\s+[A-C]\b|^Copyright notice|^Acknowledgements', rows[i][2])),
              len(rows))
    # Walk the section: which question each line belongs to, and where each
    # alternative's task begins.
    qnum, tasks, qheads = None, [], {}
    for i in range(lo + 1, hi):
        t = rows[i][2]
        m = LETTERED.match(t)
        if m and (m.group(1) or m.group(2)):
            # A lettered line that names its question moves the walk on to
            # that question, even where it only lists the alternatives ("2.
            # (a) Diary Entry or (b) Note. (25 marks)", 2022 Higher).
            qnum = int(m.group(1) or m.group(2))
            # It is the question's own head where it names both alternatives
            # on one line; one line of a list of the section's parts ("Question
            # 1 (b) Letter OR", 2021 and 2022) is not.
            if _summary(m.group(4)) and re.search(r'\(\s*[a-c]\s*\)', m.group(4)):
                qheads.setdefault(qnum, i)
        if m and not _summary(m.group(4)):
            qq = int(m.group(1) or m.group(2) or 0) or qnum
            qnum = qq
            tok = m.group(3).lower()
            tok = PRINTED_LETTERS.get((P.year, P.level, section, qq), {}).get(tok, tok)
            tasks.append((qq, tok, i))
            continue
        h = QHEAD.match(t)
        if h and not m:
            qnum = int(h.group(1) or h.group(2))
            qheads.setdefault(qnum, i)
            if not letter and qnum == q and len(MARKS.sub(' ', t[h.end():]).split()) > 6 \
                    and not re.search(r'\b(?:Answer|Attempt)\b', t[h.end():]):
                # Ordinary 2020 sets the letter on its head line: "1. You are
                # planning to go to Spain after the exams. …"
                tasks.append((qnum, None, i))
    if section == 'B' and q == 5:
        return _task_b5(rows, qheads, lo, hi)
    if letter:
        found = [i for qq, ll, i in tasks if qq == q and ll == letter]
        if not found:
            raise ValueError(f'no ({letter}) under Section {section} Question {q}')
        start = found[-1]
        first_text = LETTERED.match(rows[start][2]).group(4)
    else:
        found = [i for qq, ll, i in tasks if qq == q and ll is None]
        head = qheads.get(q)
        if found:
            start = found[-1]
            first_text = rows[start][2][QHEAD.match(rows[start][2]).end():]
        elif head is not None:
            start, first_text = head, None
        else:
            raise ValueError(f'no Section {section} Question {q} head')
    # Where it stops: the next alternative's task, the next question's head,
    # or the end of the section's matter.
    later = [i for _q, _l, i in tasks if i > start]
    later += [i for qq, i in qheads.items() if i > start and qq != q]
    stop = min(later + [hi])
    lines, pages = [], []
    b5 = section == 'B' and q == 5
    for j in range(start, stop):
        pno, _x, t = rows[j]
        if j == start:
            t = first_text if first_text is not None else ''
            if first_text is None:
                pages.append(pno + 1)
        elif FURNITURE.match(t):
            continue
        elif TASK_END.match(t) and not (b5 and t == 'O'):
            break
        elif j == start + 1 and first_text is None and re.match(rf'^{q}\s*\.\s', t):
            # Ordinary 2023 repeats the number on the task's first line:
            # "Question 1 Letter / E‐mail (40 marks)" / "1. Your Spanish friend …"
            t = re.sub(rf'^{q}\s*\.\s*', '', t)
        elif b5 and QHEAD.match(t) and not LETTERED.match(t):
            break
        t = MARKS.sub(' ', t).strip()
        if t:
            lines.append(t)
            if pno + 1 not in pages:
                pages.append(pno + 1)
    # The stem: the question's head, without its number and tariff, and what
    # it prints before the first alternative; failing a head of its own, what
    # the section prints over its parts.
    first_task = min([i for qq, _l, i in tasks if qq == q] + [start])
    head = qheads.get(q)
    if head is not None and head <= first_task:
        h = QHEAD.match(rows[head][2])
        bits = [rows[head][2][h.end():]] + [rows[k][2] for k in range(head + 1, first_task)
                                            if not FURNITURE.match(rows[k][2])]
    else:
        bits = [rows[k][2] for k in range(lo + 1, first_task) if not FURNITURE.match(rows[k][2])
                and not (QHEAD.match(rows[k][2]) and not LETTERED.match(rows[k][2]))]
    if first_text is None and head == start:
        bits = [rows[head][2][QHEAD.match(rows[head][2]).end():]]
    elif first_text is not None and head == start:
        bits = []         # the head line IS the task's first line
    stem = ' '.join(MARKS.sub(' ', b).strip() for b in bits if b and MARKS.sub(' ', b).strip())
    stem = ' '.join(stem.split())
    if b5:
        question = '\n'.join(lines)
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
            # The scheme reader's own repairs of the text layer (es_scheme
            # GLYPHS), and a symbol-font bullet read as "x" dropped, as the
            # ladders of the other sittings print no bullet (2010 Ordinary
            # "x Full message unequivocally conveyed: 8 marks").
            for old, new in SCHEME_GLYPHS.get((year, level), ()):
                line = line.replace(old, new)
            if (year, level) in X_BULLETS:
                line = re.sub(r'^x (?=\S)', '', line)
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
# "1. CONTENT/COMMUNICATION 25 marks"; 2021 and 2022 print "25marks".
CRITERION = re.compile(r'^(\d)\.\s+([A-Z][A-Z/ ]+?)\s*(\d{1,2})\s*marks$')
CRITERION_UNPRICED = re.compile(r'^(\d)\.\s+(CONTENT/COMMUNICATION|LANGUAGE)\s*$')
# "(5 x 6m = 30 marks)"; 2017 prints "(5 x 6 = 30marks)".
TIMES = re.compile(r'\((\d)\s*x\s*(\d{1,2})\s*m?\s*=\s*(\d{1,3})\s*marks\)')
# 2010-2019 print it the other way round: "8 marks x 5 = 40 marks", "5 marks x 4 = 20".
OLD_TIMES = re.compile(r'^(\d{1,2})\s*marks?\s*[x×]\s*(\d)\s*=\s*(\d{1,3})\b', re.I)


def _times(s):
    """(n, per, total) from a printed tariff line, or None."""
    m = TIMES.search(s)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    m = OLD_TIMES.search(s)
    if m:
        return int(m.group(2)), int(m.group(1)), int(m.group(3))
    return None
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
    i, j = _span(L, lambda s: re.match(r'^Section B:?\s+Question 5\b', s, re.I),
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
        if re.match(r'^Note:\s+\S', s):
            # 2021 and 2022 print the note on its head's line: "Note: Where no
            # marks are awarded for Content 1, …"
            in_note = True
            notes.append(s[len('Note:'):].strip())
            continue
        m = CRITERION.match(s) or CRITERION_UNPRICED.match(s)
        if m:
            cur = {'id': 'content' if m.group(1) == '1' else 'language',
                   'label': '/'.join(w.capitalize() for w in m.group(2).strip().split('/')),
                   'maxMarks': int(m.group(3)) if m.lastindex >= 3 else None,
                   'guidance': [], 'bands': []}
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
    for c in criteria:
        if c['maxMarks'] is None:
            # 2014 heads its first criterion "1. CONTENT/COMMUNICATION" with no
            # total; its TOP band prints the top of the range, "18 – 25 marks".
            c['maxMarks'] = max(max(b['marks']) for b in c['bands'])
        c['permittedMarks'] = list(range(c['maxMarks'] + 1))
    requirements = _sentences(notes)
    # The scheme's own rule tying the two criteria: "Where no marks are awarded
    # for Content 1, (i.e. effort totally irrelevant), no marks will be awarded
    # for Language 2." (2021 and 2022 print "will be award"). Where it is
    # printed, Language is scored 0 while Content is 0 (FrenchCriterion.
    # zeroWhenZero), and the line itself stays on the card as printed.
    rule = next((r for r in requirements if ZERO_RULE.search(r)), None)
    if rule:
        for c in criteria:
            if c['id'] == 'language':
                c['zeroWhenZero'] = 'content'
    return {'criteria': criteria, 'requirements': requirements, 'pages': pages,
            'zeroRule': rule, 'lines': [s for _p, s in block]}


ZERO_RULE = re.compile(r'no marks are awarded for Content\b.*no marks will be award(?:ed)? for Language\b', re.I)


def _ladder(lines):
    """A per-turn/per-point ladder, one entry per PRINTED line (coordinator
    ruling, 12 Nov 2026). The 2020 Higher diary/note ladder prints "5 marks
    Communicative intention fulfilled" / "Good level of vocabulary" / "Verbs
    correct" with no full stops; joined, they ran on into one sentence the
    scheme never wrote, so each printed line stays a line and nothing is
    added to it."""
    return list(lines)


def grid_c(year, level, q, letter):
    """Higher Section C: a per-turn (dialogue) or per-point ladder.

    Read by region, because 2016-2026 lay the section out several ways: each
    alternative's own lines run from its head ("Question 1 (a) DIALOGUE
    CONSTRUCTION", "Q.1 (a) …") to the "OR", the next head or the ladder's
    head ("Criteria for Question 1 …", "Guidelines for Section C, Question 1
    (a) and (b):", "Criteria for awarding marks in Q.2 …"); the ladder and any
    "Note:" lines belong to the whole question; 2016 and 2017's letter notes
    ("1a) Letter/Email:" …) to the letter alone.
    """
    L = scheme_lines(year, level)
    i, j = _span(L, lambda s: s.startswith('SECTION C'),
                 lambda s: s.startswith('APPENDIX') or s.startswith('LISTENING COMPREHENSION'))
    block = []
    for p, s in L[i:j]:
        if PAGE_NO.match(s):
            continue
        # 2025 welds the criteria's head onto the line above it: "… need not
        # use the guidelines given. Criteria for Question 1 (a) DIALOGUE and
        # (b) LETTER". Cut it where the head begins.
        at = s.find('Criteria for Question')
        if at > 0:
            block += [(p, s[:at].rstrip()), (p, s[at:])]
        else:
            block.append((p, s))
    texts = [s for _p, s in block]
    OPT = re.compile(r'^(?:Question|Q\.?)\s*(\d)\s*\(\s*([a-c])\s*\)(?!\s*and\b)')
    CRIT = re.compile(r'^(?:Criteria for|Guidelines for Section C, Question)')
    LETTER_NOTES = re.compile(r'^(?:Extra Notes|1[ab]\)\s*Letter)')
    opts = [(k, int(m.group(1)), m.group(2).lower()) for k, s in enumerate(texts) if (m := OPT.match(s))]
    # The section's own guidelines, printed once above Question 1.
    g0 = next((k for k, s in enumerate(texts) if s.startswith('Guidelines for Section C')
               and not CRIT.match(s)), None)
    g1 = next(k for k, s in enumerate(texts) if re.match(r'^Question 1\b', s) or OPT.match(s))
    guidelines = _sentences(texts[(g0 + 1) if g0 is not None else 1:g1])
    o0 = next(k for k, qq, ll in opts if qq == q and ll == letter)
    r0 = min(k for k, qq, _l in opts if qq == q)
    # The question ends where the next one's first head is printed, its own
    # lead included ("Question 2(a) and (b): Five points. …", 2021, 2022).
    r1 = min([k for k, qq, _l in opts if qq > q] + [len(texts)]
             + [k for k, s in enumerate(texts) if k > r0 and re.match(rf'^(?:Question|Q\.?)\s*{q + 1}\b', s)])
    o1 = next((k for k in range(o0 + 1, r1) if texts[k] == 'OR' or CRIT.match(texts[k])
               or OPT.match(texts[k]) or re.match(r'^Note:', texts[k]) or LETTER_NOTES.match(texts[k])), r1)
    option = [texts[o0]] + _sentences(texts[o0 + 1:o1])
    direction = []
    if q == 1:
        d0 = next((k for k, s in enumerate(texts) if re.match(r'^Question 1\s*[.:]\s*When marking', s)), None)
        # The one sentence, however many lines it wraps over.
        if d0 is not None:
            direction = _sentences(texts[d0:d0 + 3])[:1]
    c0 = next((k for k in range(r0, r1) if CRIT.match(texts[k])), None)
    criteria_head, ladder = [], []
    if c0 is not None:
        criteria_head = texts[c0:c0 + 2] if re.match(r'^TOTAL MARKS', texts[c0 + 1]) else texts[c0:c0 + 1]
        c1 = next((k for k in range(c0 + len(criteria_head), r1) if re.match(r'^Note:', texts[k])
                   or LETTER_NOTES.match(texts[k])), r1)
        ladder = _ladder(texts[c0 + len(criteria_head):c1])
    # Notes printed for the whole question ("Note: In Q. 2 (a) and (b) …"),
    # and the letter's own notes.
    notes, in_letter = [], False
    for k in range(r0, r1):
        t = texts[k]
        if LETTER_NOTES.match(t):
            in_letter = True
        if in_letter:
            continue
        elif re.match(r'^Note:', t) and (c0 is None or not (c0 <= k < c0 + len(criteria_head) + len(ladder))):
            notes.append(t)
            # its wrapped continuation lines
            m = k + 1
            while m < r1 and not (texts[m] == 'OR' or CRIT.match(texts[m]) or OPT.match(texts[m])
                                  or re.match(r'^Note:', texts[m]) or LETTER_NOTES.match(texts[m])):
                notes.append(texts[m])
                m += 1
    notes = _sentences(notes)
    # The letter's own notes run from their head to the next question's head
    # or the section's end: 2017 prints them under Question 1, 2016 under
    # Question 2, after its notes ("Extra Notes:" / "1a) Letter/Email:" / …).
    letter_at = []
    if q == 1 and letter == 'b':
        k0 = next((k for k, t in enumerate(texts) if LETTER_NOTES.match(t)), None)
        if k0 is not None:
            k1 = next((k for k in range(k0 + 1, len(texts)) if OPT.match(texts[k])), len(texts))
            letter_at = list(range(k0, k1))
            notes += _sentences([texts[k] for k in letter_at])
    times = next((_times(s) for s in option if _times(s)), None)
    # Pages from the lines' own positions: the question's region and the
    # section's guidelines (a ladder line repeated under Question 2 is not
    # Question 1's page).
    pages = sorted({block[k][0] for k in [*range(r0, r1), *range(g0 or 0, g1), *letter_at]})
    l0 = next((k for k, s in enumerate(texts) if re.match(rf'^Question {q}\s*\(a\) and \(b\)', s)), None)
    lead = _sentences(texts[l0:next(k for k in range(l0, len(texts)) if texts[k] == 'OR')]) if l0 is not None else []
    out = {'option': option, 'direction': direction, 'guidelines': guidelines, 'lead': lead,
           'criteriaHead': criteria_head, 'ladder': ladder, 'notes': notes, 'pages': pages}
    if times:
        n, per, total = times
        return {**out, 'n': n, 'per': per, 'total': total}
    whole = re.search(r'\((\d{1,2})\s*marks\)', option[0])
    if any(re.search(r'\bglobal mark\b', s) for s in lead) and whole:
        # One mark for the whole piece, placed on the printed bands.
        return {**out, 'n': 1, 'per': int(whole.group(1)), 'total': int(whole.group(1)), 'global': True}
    raise ValueError(f'{year} {level} C Q{q}({letter}): no "(n x m = total)" tariff')


def grid_ol_b(year, level, q, letter):
    """Ordinary Section B: a per-point ladder for the letter, then the note or diary."""
    L = scheme_lines(year, level)
    i, j = _span(L, lambda s: s.startswith('SECTION B'),
                 lambda s: s.startswith('LISTENING') or s.startswith('APPENDIX'))
    block = [(p, s) for p, s in L[i:j] if not PAGE_NO.match(s)]
    texts = [s for _p, s in block]
    # "Q. 1. LETTER", "Q.2. (a) NOTE …"; 2016 prints "Q.2 (a) NOTE …".
    head = re.compile(r'^Q\.?\s*1\.' if q == 1 else r'^Q\.?\s*2\b\.?')
    o0 = next(k for k, s in enumerate(texts) if head.match(s))
    o1 = next((k for k in range(o0 + 1, len(texts)) if re.match(r'^Q\.?\s*2\b', texts[k])), len(texts)) \
        if q == 1 else len(texts)
    # 2019 closes the section with its "Reasonable Accommodations:" note, and
    # 2012 runs straight on into "Appendix One".
    o1 = next((k for k in range(o0 + 1, o1)
               if re.match(r'^(?:Reasonable Accommodations|Appendix\b)', texts[k], re.I)), o1)
    part = texts[o0 + 1:o1]
    t = next(k for k, s in enumerate(part) if _times(s))
    lead = _sentences(part[:t + 1])
    ladder = _ladder(part[t + 1:])
    n, per, total = _times(part[t])
    pages = sorted({p for p, s in block if s in texts[o0:o1]})
    # The section's own note, quoted a page at a time: 2010 prints "Candidates
    # must attempt 1. LETTER/E-MAIL and either" at the foot of p8 and "2. (a)
    # MESSAGE or 2 (b) DIARY ENTRY." at the head of p9, and its text layer sets
    # the page number between them with control characters ("7\x03"), so the
    # sentence joined across the page is not one the scheme's text holds.
    k1 = next(k for k, s in enumerate(texts) if head.match(s) or re.match(r'^Q\.?\s*1\.', s))
    section = [t for _p, run in groupby(block[1:k1], key=lambda ps: ps[0])
               for t in _sentences([s for _q, s in run])]
    return {'n': n, 'per': per, 'total': total, 'head': texts[o0], 'lead': lead,
            'ladder': ladder, 'section': section,
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
