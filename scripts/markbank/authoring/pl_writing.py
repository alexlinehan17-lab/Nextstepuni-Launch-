#!/usr/bin/env python3
"""Polish written production on the scheme's own grid (FrenchRubric shape).

    python3 scripts/markbank/authoring/pl_writing.py 2026 hl     # print the cards

Treatment D (approved 18 Nov 2026): one marking-grid card per written task, the
live card German, French and Spanish use (de_writing.py is the precedent).

From 2022 the scheme marks every Część B task on ONE grid printed once for the
section: Content (C) and Expression (E), each in four bands at Higher ("Very
good", "Good", "Fair", "Weak") with a range for Questions 3 and 4 (15 marks)
and another for Question 5 (10 marks), and three bands at Ordinary (15 marks a
criterion for both questions). The grid is read from the scheme PDF's own
TABLE (pymupdf find_tables), because the flat text sets each band name halfway
down its descriptors; every band name, range and descriptor is the cell's own
words, and build-deck traces each one in the .md.

The task is read from the question paper: the lettered task, its bullet points
(set as a lone "•" glyph beside each point), up to the "lub" that separates it
from the next option. The instruction above the options ("Odpowiedz na pytanie
(a) lub (b), lub (c), używając około 200 słów.") is the card's stem: it carries
the word count. Image credits printed in the margin ("poster.pl") are not task
words and are left out; the page itself rides as the card's source.
"""
import json
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

import pl_paper                                                  # noqa: E402
from pl_topics import WRITTEN_PRODUCTION, concept_for            # noqa: E402
from paper_census import key_label                              # noqa: E402

LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}
LUB = re.compile(r'^(?:lub|LUB)$')
CREDIT = re.compile(r'^[\w.-]+\.(?:pl|ie|com|org|net|eu)$', re.I)
# 2023 sets its ranges with U+2010 HYPHEN ("15‐12").
RANGE = re.compile(r'(\d{1,2})\s*[-‐–]\s*(\d{1,2})')
SPEAKER = re.compile(r'^[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+:(?:\s|$)')
# Numbers under a row of photographs and the photographs' credits.
PHOTO_LABELS = re.compile(r'(?:\b\d{1,2}\.|[\w.-]+\.(?:pl|ie|com|org|net|eu|co\.uk)\b)')
# Right of this the page is the picture a Question 5 task sets beside it;
# every task's own words start at the left margin (x≈57) and its bullets at
# x≈85-128.
IMAGE_COLUMN = 290.0
INSTRUCTION = re.compile(r'^(?:Odpowiedz\b.*\b(?:słów|słowa)\b|Wykonaj\b.*\bzadanie\b)')
TASK_GAP = 45.0
# Tasks set on a printed table of pictures: the task's words stop at the
# table's first row label, and the table itself is read on the page the
# card carries. 2024 Ordinary Q5(a) (paper p20): rows Wygląd / Miejsce
# zamieszkania / Wiek, Lubi, Nie lubi, each a row of photographs.
TABLE_STARTS = {(2024, 'ol', 5, 'a'): 'Wygląd'}


def scheme_pdf(year, level):
    return os.path.join(ROOT, 'examiner-reports', 'polish', 'schemes', f'{year}-{level}.pdf')


def scheme_md(year, level):
    with open(os.path.join(ROOT, 'examiner-reports', 'polish', 'schemes',
                           f'{year}-{level}.md'), encoding='utf-8') as fh:
        return fh.read().split('\n')


# ------------------------------------------------------------- the grid ---
def _cell(text):
    return re.sub(r'\s+', ' ', (text or '').replace('\n', ' ')).strip()


def _descriptors(cell):
    """The descriptor cell, one entry per printed point: bullets at Higher,
    one point a line at Ordinary."""
    # 2023 prints its bullets as the Symbol font's private-use U+F0B7.
    raw = (cell or '').replace('\uf0b7', '•')
    if '•' in raw:
        return [_cell(p) for p in raw.split('•') if _cell(p)]
    return [_cell(p) for p in raw.split('\n') if _cell(p)]


def grid(year, level):
    """{'content': [...bands], 'expression': [...bands], 'pages': [...]}.

    A band is (label, [ranges], [descriptors]): one range per printed column,
    Q.3/Q.4 then Q.5 at Higher, one at Ordinary.
    """
    out, pages, current = {'content': [], 'expression': []}, [], None
    tables_seen = 0
    with pymupdf.open(scheme_pdf(year, level)) as doc:
        for pno, page in enumerate(doc, 1):
            for tb in page.find_tables().tables:
                rows = tb.extract()
                # A grid table, or a page's share of one: its first column
                # holds band names. 2025 Higher breaks both grids across
                # pages, and the first halves print no "Fair" or "Weak".
                if not any(re.match(r'^(?:Very good|Good|Fair|Weak)$', _cell(r[0])) for r in rows):
                    continue
                tables_seen += 1
                if pno not in pages:
                    pages.append(pno)
                header = ' '.join(_cell(c) for c in rows[0])
                if 'CONTENT' in header:
                    current = 'content'
                elif 'EXPRESSION' in header:
                    current = 'expression'
                elif level == 'ol':
                    # Ordinary prints two unheaded tables, Content's first:
                    # the head over each is the line "Content:"/"Expression:".
                    current = 'content' if tables_seen == 1 else 'expression'
                for r in rows:
                    label = _cell(r[0])
                    if not re.match(r'^(?:Very good|Good|Fair|Weak)$', label):
                        continue
                    ranges = [RANGE.search(_cell(c)) for c in r[1:-1]]
                    ranges = [(int(m.group(1)), int(m.group(2))) for m in ranges if m]
                    out[current].append((label, ranges, _descriptors(r[-1])))
    out['pages'] = pages
    return out


def band_marks(rng):
    hi, lo = max(rng), min(rng)
    return list(range(lo, hi + 1))


# ---------------------------------------------------------- the scheme's head ---
def requirements(year, level):
    """The scheme's own rules for Część B, each a printed point, from the .md.

    Read from the section head to the grid's own head ("Content (C)" /
    "Content:"); a bullet opens a point and a line without one continues it.
    """
    lines = scheme_md(year, level)
    # "SECTION B 80 marks" (2026 HL), "Część B: Pisanie", or the 2023/2024
    # pair "Część B Pisanie 80 punktów" over "Section B Writing 80 marks":
    # the rules start after the last heading line of the run.
    head = re.compile(r'^(?:SECTION B\b|Section B Writing\b|Cz[eę][sś][cć] B:? Pisanie)')
    norm = lambda l: re.sub(r'[ \xa0]+', ' ', l).strip()                     # noqa: E731
    start = next(i for i, l in enumerate(lines) if head.match(norm(l)))
    while start + 1 < len(lines) and head.match(norm(lines[start + 1])):
        start += 1
    out = []
    for l in lines[start + 1:]:
        # 2023 sets the section in no-break spaces.
        t = re.sub(r'[ \xa0]+', ' ', l).strip()
        if re.match(r'^Content\b', t):
            break
        if not t or re.match(r'^(?:##\s*Page\s*\d+|\d{1,3})$', t):
            continue
        if t.startswith('•'):
            out.append(t.lstrip('•').strip())
        elif out and not re.match(r'^(?:Zadanie|\(\d)', t) \
                and (not out[-1].endswith(('.', ')')) or re.match(r'^(?:AND|and|or)\b', t)):
            # A line the SEC wrapped: "Candidates are required to attempt:" /
            # "Either question" / "3(a) or 3(b) or 3(c), ..." is one point.
            out[-1] = f'{out[-1]} {t}'
        else:
            out.append(t)
    return out


# -------------------------------------------------------------- the task ---
def task_text(P, key):
    """The lettered task as printed: its words and its bullet points, up to
    the "lub" before the next option."""
    _s, q, letter, _r = key
    lines = P.lines
    head = None
    for i, line in enumerate(lines):
        qm = pl_paper.Q_HEAD.match(line.text)
        if qm:
            head = int(qm.group(1))
            continue
        if head == q and re.match(rf'^\(\s*{letter}\s*\)', line.text):
            start = i
            break
    else:
        raise ValueError(f'{P.year} {P.level} {key}: task not found on the paper')
    page = lines[start].page
    parts, bullet, last_y = [], False, None
    for line in lines[start:]:
        t = line.text
        if line is not lines[start]:
            if last_y is not None and line.y - last_y > TASK_GAP and not SPEAKER.match(t):
                # The task's words are set close together; what follows a
                # wider gap is the picture, map or table the task sets below
                # them ("16 września 2026, piątek" on the 2026 Ordinary map).
                # A printed dialogue leaves answer space between turns, so a
                # speaker's turn continues the task across it.
                break
            table = TABLE_STARTS.get((P.year, P.level, q, letter))
            if table and t.startswith(table):
                break
            if line.page != page or LUB.match(t) or pl_paper.Q_HEAD.match(t) \
                    or re.match(r'^\(\s*[a-h]\s*\)', t) \
                    or (pl_paper.FURNITURE.match(t) and len(t) < 60) \
                    or t.startswith(('Leaving Certificate', 'Polish –')):
                break
            if CREDIT.match(t) or not PHOTO_LABELS.sub('', t).strip():
                continue
            if line.x > IMAGE_COLUMN:
                # Printed in the picture's column: its caption or credit
                # ("Zdzisław Beksiński, Obraz AB79"), not the task's words.
                continue
        if t == '•':
            bullet = True
            last_y = line.y
            continue
        last_y = line.y
        if line is lines[start]:
            t = re.sub(r'^\(\s*[a-h]\s*\)\s*', '', t)
        if bullet:
            parts.append(f'• {t}')
            bullet = False
        elif parts and not SPEAKER.match(t):
            # A wrapped line belongs to the point or paragraph it continues;
            # only a bullet glyph or a speaker's turn in a printed dialogue
            # ("Jola: Cześć Marcelo! ...") opens a new one.
            parts[-1] = f'{parts[-1]} {t}'
        else:
            parts.append(t)
    # Ordinary sets some bullets inline ("punkty: • Poranny stres. • Droga do
    # szkoły."): each point on its own line, as the page lays it out.
    return '\n'.join(p.replace(' • ', '\n• ') for p in parts), page


def instruction(P, q):
    """The line under "Pytanie 3" that says how to answer: (a) lub (b) lub (c),
    and how many words."""
    head = None
    for line in P.lines:
        qm = pl_paper.Q_HEAD.match(line.text)
        if qm:
            head = int(qm.group(1))
            continue
        if head == q and INSTRUCTION.match(line.text):
            return line.text
        if head == q and re.match(r'^\(\s*a\s*\)', line.text):
            return ''
    return ''


# -------------------------------------------------------------- the card ---
def cards(year, level):
    P = pl_paper.PlPaper(year, level)
    G = grid(year, level)
    reqs = requirements(year, level)
    # No-break spaces (2023) read as spaces; the zero rule may wrap (2024).
    md = [re.sub(r'[ \xa0]+', ' ', l) for l in scheme_md(year, level)]
    content_label = next((l.strip() for l in md if re.match(r'^Content\b', l.strip())), 'Content')
    content_label = 'Content (C)' if content_label.startswith('Content (C)') else 'Content'
    expression_label = 'Expression (E)' if any(l.strip().startswith('Expression (E)') for l in md) \
        else 'Expression'
    zero_rule = 'no marks will be awarded for expression' in ' '.join(l.strip() for l in md).lower()
    out = []
    for ask in P.writing_asks():
        key = ask.key
        q = key[1]
        col = 1 if (level == 'hl' and q == 5) else 0
        criteria = []
        for cid, label in (('content', content_label), ('expression', expression_label)):
            bands = []
            for blabel, ranges, desc in G[cid]:
                if len(ranges) <= col:
                    raise ValueError(f'{year} {level} {cid} {blabel}: no range for column {col}')
                bands.append({'label': blabel, 'marks': band_marks(ranges[col]), 'guidance': desc})
            top = max(m for b in bands for m in b['marks'])
            marks = sorted(m for b in bands for m in b['marks'])
            if marks != list(range(top + 1)):
                raise ValueError(f'{year} {level} Q{q} {cid}: bands cover {marks}, not 0-{top} once')
            crit = {'id': cid, 'label': label, 'maxMarks': top,
                    'permittedMarks': list(range(top + 1)), 'guidance': [], 'bands': bands}
            if cid == 'expression' and zero_rule:
                # "Where no marks are awarded for content (i.e. effort totally
                # irrelevant), no marks will be awarded for expression."
                crit['zeroWhenZero'] = 'content'
            criteria.append(crit)
        total = sum(c['maxMarks'] for c in criteria)
        text, page = task_text(P, key)
        stem = instruction(P, q)
        letter = key[2]
        card = {
            'id': '-'.join(['pl', str(year), level, 'b', str(q), letter]),
            'kind': 'rubric',
            'subjectId': 'polish',
            'level': LEVEL_WORD[level],
            'year': year,
            'section': 'B',
            'topicId': WRITTEN_PRODUCTION,
            'conceptId': concept_for(text),
            'questionRef': f'{year} {level.upper()} {key_label(key, "polish")}',
            'questionText': text,
            **({'stem': stem} if stem else {}),
            'totalMarks': total,
            'rubric': {
                'system': 'french',
                'taskRequirements': reqs,
                'criteria': criteria,
                'markingGuideNote': '',
                'practiceNotes': ['Write your answer in Polish, then place it on the '
                                  'published grid: content first, then expression.'],
            },
            'schemePages': G['pages'],
            'sourceMaterial': {
                'kind': 'source-text',
                'label': f'{"PYTANIE" if level == "hl" else "ZADANIE"} {q}',
                'title': f'{"Pytanie" if level == "hl" else "Zadanie"} {q} ({letter}) — answer in Polish',
                'pages': [page],
                'attribution': (f'SEC Polish {year} {LEVEL_TITLE[level]} Level examination '
                                f'paper — © State Examinations Commission.'),
                'presentationNote': 'The task exactly as the examination printed it.',
            },
        }
        out.append(card)
    return out


def main():
    year, level = int(sys.argv[1]), sys.argv[2]
    for c in cards(year, level):
        print(json.dumps(c, ensure_ascii=False, indent=1)[:2500])
    return 0


if __name__ == '__main__':
    sys.exit(main())
