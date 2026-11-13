#!/usr/bin/env python3
"""German written production on the scheme's own grid (FrenchRubric shape).

    python3 scripts/markbank/authoring/de_writing.py 2026 hl     # print the cards

Äußerung zum Thema (Higher, 25 marks) is marked "Content = 13 (A = 3; B = 4;
C = 4; Dis. 2)" and "Expression = 12", and the scheme prints a second, lower
expression scale beside the full one with the rule that switches to it: "If
the content mark is 8 or less, or the answer is too short (less than 60
words), mark expression out of 7". So a card's criteria are the content
points as printed (A, B, C, the discretionary marks) and Expression, whose
`lowerScale` carries the reduced scale, its bands and that rule verbatim.

Every string the card shows as the SEC's is lifted from the scheme's text
layer; the criterion labels for the bands ("Category 1") and the practice
notes are NextStepUni's, and the panel says so.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from de_paper import DePaper                       # noqa: E402
from de_scheme import DeScheme                     # noqa: E402

LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}
PAGE = re.compile(r'^(?:##\s*Page\s*\d+\s*$|\d{1,3}\s*$)')
RANGE = r'(\d{1,2})(?:\s*[–-]\s*(\d{1,2}))?'
# A row of the expression table: the lower range, the full range, then the
# descriptor's words ("0 – 2 0 – 3 verb forms/tense generally incorrect.").
SCALE_ROW = re.compile(rf'^{RANGE}\s+{RANGE}(?:\s+(.*))?$')


def _lines(S, start, stop):
    return [l.strip() for l in S.lines[start:stop] if l.strip() and not PAGE.match(l.strip())]


def _find(S, pattern, start=0):
    rx = re.compile(pattern, re.I)
    return next((i for i in range(start, len(S.lines)) if rx.search(S.lines[i].strip())), None)


def expression_scale(S, head, columns=2):
    """An expression table: ([column-1 bands], [column-2 bands], at).

    The table prints two ranges on one line of each category ("0 – 2 0 – 4
    position, very frequently wrong; …"): the reduced or Äußerung column
    first, the full one second. Each category opens with "Vocabulary …"."""
    start = _find(S, head)
    if start is None:
        return None
    stop = _find(S, r'^N\.B\. Take a global view', start)
    lines = _lines(S, start + 1, stop)
    cats = []
    for line in lines:
        if line.startswith('Vocabulary'):
            cats.append({'lines': [], 'one': None, 'two': None})
        if not cats:
            continue
        m = SCALE_ROW.match(line)
        if m and cats[-1]['one'] is None:
            cats[-1]['one'] = (int(m.group(1)), int(m.group(2) or m.group(1)))
            cats[-1]['two'] = (int(m.group(3)), int(m.group(4) or m.group(3)))
            # The range column cuts the descriptor where it is printed
            # ("… Verb" / "4 – 6 forms/tense …"): the words either side are
            # kept apart, as the scheme's text has them.
            cats[-1]['lines'].append(None)
            if m.group(5):
                cats[-1]['lines'].append(m.group(5).strip())
            continue
        cats[-1]['lines'].append(line)
    one, two = [], []
    for n, c in enumerate(cats, start=1):
        assert c['one'] and c['two'], (S.year, S.level, head, c)
        guidance = _join(c['lines'])
        one.append({'label': f'Category {n}', 'marks': list(range(c['one'][0], c['one'][1] + 1)),
                    'guidance': guidance})
        two.append({'label': f'Category {n}', 'marks': list(range(c['two'][0], c['two'][1] + 1)),
                    'guidance': guidance})
    nb = ' '.join(_lines(S, stop, stop + 3)) if stop is not None else ''
    nb = re.match(r'^(N\.B\. Take a global view.*?categor(?:y|ies)[^.]*\.)', nb)
    return one, two, (nb.group(1) if nb else None), start


def rule_text(S, start, pattern, until):
    """A printed rule, from its first words to the words that end it, joined
    across the scheme's own line breaks (the provenance gate compares text,
    not lines)."""
    at = _find(S, pattern, start)
    words = []
    for line in _lines(S, at, at + 4):
        words.append(line)
        m = re.search(until, ' '.join(words))
        if m:
            return ' '.join(words)[:m.end()].strip()
    raise AssertionError((S.year, S.level, pattern))


def _join(lines):
    """Descriptor lines as printed, a wrapped sentence joined: the scheme
    breaks "… word order, esp. verb position, very frequently wrong;" across
    lines mid-clause. Kept line by line where a line ends a clause, and never
    joined across a break (None) the range column makes."""
    out = []
    cut = False
    for line in lines:
        if line is None:
            cut = True
            continue
        if out and not cut and not re.search(r'[.;:]$', out[-1]):
            out[-1] = f'{out[-1]} {line}'
        else:
            out.append(line)
        cut = False
    return out


def theme_grid(S, letter):
    """The content points of Äußerung option (a) or (b): its head lines, and
    [(id, label, marks, [printed lines])] for A, B, C and Dis."""
    starts = [i for i, l in enumerate(S.lines) if re.match(r'^Content = 13 \(A = 3; B = 4; C = 4; Dis\. 2\)', l.strip())]
    at = starts['ab'.index(letter)]
    end = _find(S, r'^Dis\. 2 marks', at)
    lines = _lines(S, at, end + 1)
    head, points, cur = [], [], None
    for line in lines:
        m = re.match(r'^([ABC]):? \((\d) marks\)$', line)
        if m:
            cur = {'id': m.group(1).lower(), 'label': m.group(1), 'marks': int(m.group(2)), 'lines': []}
            points.append(cur)
            continue
        if line.startswith('Dis. 2 marks'):
            points.append({'id': 'dis', 'label': 'Dis.', 'marks': 2, 'lines': [line]})
            cur = None
            continue
        (cur['lines'] if cur else head).append(line)
    assert [p['marks'] for p in points] == [3, 4, 4, 2], (S.year, S.level, letter, points)
    return head, points


def task_text(P, unit, letter):
    """The task as the paper prints it, a bullet to a line."""
    rows = [r for r in P.alternatives if r[0] == unit and r[1] == letter]
    rows.sort(key=lambda r: (r[4] == 'R', len(' '.join(r[2]))), reverse=True)
    lines, page = rows[0][2], rows[0][3]
    if rows[0][4] == 'R' and len(' '.join(lines)) < 60:
        # The two columns fused on this page (2026 Higher p18: the English
        # "Your German friend, Karl/Karla, has" alone in its column, the rest
        # interleaved with the Irish): read the English column word by word.
        lines = _english_column(P.path, page, lines[0])
    out = []
    for raw in lines:
        t = ' '.join(raw.replace('\uf0b7', '•').split())
        if not t:
            continue
        title = len(out) == 1 and not re.search(r'[.?!:)]$', out[0]) and t[:1].isupper()
        if out and not t.startswith('•') and not re.search(r'[.?!:)]$', out[-1]) and not title:
            out[-1] = f'{out[-1]} {t}'
        else:
            out.append(t)
    return '\n'.join(out), page


def _english_column(path, page, first):
    """The English column of one written-paper page, from the line that opens
    the task to the line giving its length ("(Write approximately 160 words.)")."""
    import pymupdf
    with pymupdf.open(path) as doc:
        rows = []
        for x0, y0, x1, y1, word, *_ in doc[page - 1].get_text('words'):
            if x0 < 288 or not word.strip():
                continue
            mid = (y0 + y1) / 2
            for row in rows:
                if abs(row['mid'] - mid) <= 3:
                    row['w'].append((x0, word))
                    break
            else:
                rows.append({'mid': mid, 'w': [(x0, word)]})
    lines = [' '.join(w for _x, w in sorted(r['w'])) for r in sorted(rows, key=lambda r: r['mid'])]
    start = next(k for k, l in enumerate(lines) if first[:20] in l)
    out = []
    for line in lines[start:]:
        out.append(re.sub(r'^\(\s*[ab]\s*\)\s*', '', line) if not out else line)
        if re.search(r'words\.\)$|Wörter\)$', line):
            break
    return out


ORDINALS = ('First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth')
TAGS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))),
                    'scripts', 'paper-trail', 'topic-tags', 'tags', 'german.json')
PRACTICE = 'Write your answer in German, then place it on the published grid.'
PRACTICE_LOWER = 'Place the content first: which expression scale applies depends on it.'
PRACTICE_POINTS = ('You are marked on the points you chose; mark each one you wrote on its own '
                   'against the points the scheme lists.')


def _points(n, marks):
    return [{'id': f'point-{k}', 'label': f'{ORDINALS[k - 1]} point', 'maxMarks': marks,
             'permittedMarks': list(range(marks + 1)), 'guidance': []} for k in range(1, n + 1)]


def _criterion(cid, label, marks, guidance):
    return {'id': cid, 'label': label, 'maxMarks': marks,
            'permittedMarks': list(range(marks + 1)), 'guidance': guidance}


def _expression(maxm, bands, lower=None):
    k = _criterion('expression', 'Expression', maxm, [])
    k['bands'] = bands
    if lower:
        k['lowerScale'] = lower
    return k


def atlas_written(year, level):
    with open(TAGS, encoding='utf-8') as fh:
        papers = json.load(fh)
    fileid = f'LC011{"A" if level == "hl" else "G"}LP000{"BV" if year >= 2019 else "EV"}.pdf'
    for p in papers:
        if p['year'] == year and p['level'] == LEVEL_WORD[level] and p['lang'] == 'ev' and p['fileid'] == fileid:
            return {q['n']: q for q in p['q']}
    return {}


def _pages(P, unit, letter):
    """The task's own printed pages: Äußerung's two, a letter up to the
    picture task, the picture task and the page facing it."""
    unit_pages = P.unit_pages.get(unit, [])
    starts = {r[1]: r[3] for r in P.alternatives if r[0] == unit}
    if unit == 'AT':
        return unit_pages[:2]
    if letter == 'a':
        end = starts.get('b', starts['a'] + 1)
        return list(range(starts['a'], max(end, starts['a'] + 1)))
    return [p for p in (starts['b'], starts['b'] + 1) if p in unit_pages]


def _source(P, year, level, unit, letter, title):
    return {
        'kind': 'source-text',
        'label': 'ÄUSSERUNG ZUM THEMA' if unit == 'AT' else 'SCHRIFTLICHE PRODUKTION',
        'title': f'{title} ({letter}) — answer in German',
        'pages': _pages(P, unit, letter),
        'attribution': (f'SEC German {year} {LEVEL_TITLE[level]} Level examination '
                        f'paper — © State Examinations Commission.'),
        'presentationNote': 'The task exactly as the examination printed it.',
    }


def _block(S, start_pattern, end_pattern, after=0):
    a = _find(S, start_pattern, after)
    b = _find(S, end_pattern, a + 1)
    return a, b, _lines(S, a, b)


def _labelled(lines, label_rx):
    """[(label, marks, [lines])] for the lines a printed label opens:
    "A. (4)", "Op. (2)", "Cl. (2)", "A: (3 marks)", "A. (3) Say where …"."""
    out, head = [], []
    for line in lines:
        m = re.match(label_rx, line)
        if m:
            out.append([m.group(1), int(m.group(2)), [line]])
            continue
        (out[-1][2] if out else head).append(line)
    return head, out


def _rubric(requirements, criteria, note=''):
    return {'system': 'french', 'taskRequirements': requirements, 'criteria': criteria,
            'markingGuideNote': note}


def _card(year, level, unit, letter, total, rubric, text, source, topic, pages, concept_for,
          question_ref, practice):
    rubric['practiceNotes'] = practice
    assert sum(k['maxMarks'] for k in rubric['criteria']) == total, (year, level, unit, letter)
    return {
        'id': f'de-{year}-{level}-{unit.lower()}-{letter}',
        'kind': 'rubric', 'subjectId': 'german', 'level': LEVEL_WORD[level], 'year': year,
        'section': unit, 'topicId': topic, 'conceptId': concept_for(text),
        'questionRef': question_ref(year, level, unit, None, letter),
        'questionText': text, 'totalMarks': total, 'rubric': rubric,
        'schemePages': pages, 'sourceMaterial': source,
    }


def _page_span(S, a, b):
    pages = set()
    page = 1
    for n, line in enumerate(S.lines):
        m = re.match(r'^##\s*Page\s*(\d+)', line.strip())
        if m:
            page = int(m.group(1))
        if a <= n < b:
            pages.add(page)
    return sorted(pages)


# ------------------------------------------------------------- Higher -----
def higher_cards(year, card_id, question_ref, concept_for):
    P = DePaper(year, 'hl', 'german')
    S = DeScheme(year, 'hl', 'german')
    tags = atlas_written(year, 'hl')
    out = []
    # Äußerung zum Thema: A, B, C, Dis. as printed; Expression 12, Lower E 7.
    at_one, at_two, at_nb, at_at = expression_scale(S, r'^Marking Written Expression in [ÄA]u[ßs]{1,2}erung')
    at_rule = rule_text(S, at_at, r'^If the content mark is', r'out of \d+')
    for letter in 'ab':
        head, points = theme_grid(S, letter)
        criteria = [_criterion(p['id'], p['label'], p['marks'], p['lines']) for p in points]
        criteria.append(_expression(12, at_two, {
            'label': 'Lower E', 'maxMarks': 7, 'permittedMarks': list(range(8)), 'bands': at_one,
            'contentCriteria': [p['id'] for p in points], 'contentAtMost': 8, 'wordsUnder': 60,
            'rule': at_rule}))
        reqs = ['Content = 13 (A = 3; B = 4; C = 4; Dis. 2)', 'Expression = 12'] + _join(
            [l.lstrip('•\uf0b7 ').strip() for l in head if not re.match(r'^(Content|Expression) =', l)])
        if at_nb:
            reqs.append(at_nb)
        text, _page = task_text(P, 'AT', letter)
        starts = [i for i, l in enumerate(S.lines) if l.strip().startswith('Content = 13 (A = 3')]
        pages = sorted(set(_page_span(S, starts['ab'.index(letter)], starts['ab'.index(letter)] + 1)
                           + _page_span(S, at_at, at_at + 1)))
        out.append(_card(year, 'hl', 'AT', letter, 25, _rubric(reqs, criteria), text,
                         _source(P, year, 'hl', 'AT', letter, 'Äußerung zum Thema'),
                         tags[f'T-{letter.upper()}']['primary'], pages, concept_for, question_ref,
                         [PRACTICE, PRACTICE_LOWER]))
    # Schriftliche Produktion: (a) letter, any four of A-E; (b) photo, any
    # five of A-F; Op./Cl. on the letter, Dis. 5; Expression 25, Lower E 18.
    sp_one, sp_two, sp_nb, sp_at = expression_scale(S, r'^Marking Written Expression in Schriftliche')
    sp_rule = rule_text(S, sp_at, r'^If the content mark is', r'out of \d+')
    sp = _find(S, r'^SCHRIFTLICHE PRODUKTION \(50\)')
    a_at, b_at = _find(S, r'^\(a\) ', sp), _find(S, r'^\(b\) ', sp + 1)
    for letter, (lo, hi) in (('a', (a_at, b_at)), ('b', (b_at, sp_at))):
        lines = [l for l in _lines(S, lo, hi) if l not in ('OR',)]
        if letter == 'a':
            # (b)'s own note and its "Where a candidate …" line, printed
            # above "(b)", are not (a)'s.
            cut = next((k for k, l in enumerate(lines) if k > 0 and l.startswith('Note: Answer any')
                        and 'Dis.:' in ' '.join(lines[:k])), None)
            if cut is not None:
                lines = lines[:cut]
        if letter == 'b' and lo > 0:
            lead = [l for l in _lines(S, lo - 4, lo) if l.startswith('Note: Answer any') or l.startswith('Where a candidate')]
            lines = lead + lines
        head, labelled = _labelled(lines, r'^(Op|Cl|[A-F])\. \((\d)\)')
        dis = next(l for l in lines if l.startswith('Dis.:'))
        # 2023 prints (b)'s "Note: Answer any five …" above its "(b)" line,
        # so it closes (a)'s block: the task's own note is the first in its
        # block, or else the one printed just above it.
        want = re.search(r'Answer any (\w+) of the', ' '.join(head)) or re.search(
            r'Answer any (\w+) of the', ' '.join(_lines(S, lo - 4, lo)))
        n = {'four': 4, 'five': 5}[want.group(1).lower()]
        criteria, reqs = [], [l for l in head if not l.startswith('Dis.:')]
        for label, marks, block in labelled:
            block = [l for l in block if not l.startswith('Dis.:')]
            if label in ('Op', 'Cl'):
                criteria.append(_criterion(label.lower(), f'{label}.', marks, block))
            else:
                assert marks == 4, (year, letter, label)
                reqs.extend(block)
        points = [x for x in labelled if x[0] not in ('Op', 'Cl')]
        cl = [k for k in criteria if k['id'] == 'cl']
        criteria = [k for k in criteria if k['id'] == 'op'] + _points(n, 4) + cl + [
            _criterion('dis', 'Dis.', 5, [dis])]
        content = [k['id'] for k in criteria]
        criteria.append(_expression(25, sp_two, {
            'label': 'Lower E', 'maxMarks': 18, 'permittedMarks': list(range(19)), 'bands': sp_one,
            'contentCriteria': content, 'contentAtMost': 12, 'wordsUnder': 100, 'rule': sp_rule}))
        if sp_nb:
            reqs.append(sp_nb)
        text, _page = task_text(P, 'SP', letter)
        pages = sorted(set(_page_span(S, lo, hi) + _page_span(S, sp_at, sp_at + 1)))
        assert len(points) >= n, (year, letter, len(points), n)
        out.append(_card(year, 'hl', 'SP', letter, 50, _rubric(reqs, criteria), text,
                         _source(P, year, 'hl', 'SP', letter, 'Schriftliche Produktion'),
                         tags[f'P-{letter.upper()}']['primary'], pages, concept_for, question_ref,
                         [PRACTICE, PRACTICE_LOWER, PRACTICE_POINTS]))
    return out


# ----------------------------------------------------------- Ordinary -----
def ordinary_cards(year, card_id, question_ref, concept_for):
    P = DePaper(year, 'ol', 'german')
    S = DeScheme(year, 'ol', 'german')
    tags = atlas_written(year, 'ol')
    out = []
    # The one expression table: column one is Äußerung's 7 and Schriftliche
    # Produktion's "Lower Ex." 7, column two the full 10.
    one, two, nb, ex_at = expression_scale(S, r'^Guidelines for marking Expression in [ÄA]u[ßs]{1,2}erung')
    sp_rule = rule_text(S, ex_at, r'^N\.B\. If the content mark in the Schriftliche',
                        r'for expression\.')
    at = _find(S, r'^TEXT II: [ÄA]U[ßS]{1,2}ERUNG ZUM THEMA')
    a_at = _find(S, r'^\(a\) ', at)
    b_at = _find(S, r'^E-?Mail schreiben|^E-mail schreiben|^\(b\) ', a_at + 1)
    head_lines = _lines(S, at, a_at)
    # (a) the dialogue: one criterion per printed turn, "(A1)" … "(F2)", with
    # the prompt printed above it.
    lines = _lines(S, a_at, b_at)
    head, crit, prompt = [], [], []
    for line in lines:
        m = re.match(r'^\(([A-F])(\d)\)\s*(.*)$', line)
        if m:
            crit.append(_criterion(m.group(1).lower(), m.group(1), int(m.group(2)), prompt + [line]))
            prompt = []
        elif line.startswith('Sie:'):
            prompt.append(line)
        elif crit:
            crit[-1]['guidance'].append(line)
        else:
            head.append(line)
    closing = prompt
    reqs = head_lines[1:] + head + closing
    if nb:
        reqs.append(nb)
    criteria = crit + [_expression(7, one)]
    text, _p = task_text(P, 'AT', 'a')
    out.append(_card(year, 'ol', 'AT', 'a', 15, _rubric(reqs, criteria), text,
                     _source(P, year, 'ol', 'AT', 'a', 'Äußerung zum Thema'),
                     tags['T-A']['primary'], sorted(set(_page_span(S, a_at, b_at) + _page_span(S, ex_at, ex_at + 1))),
                     concept_for, question_ref, [PRACTICE]))
    # (b) the e-mail: one criterion per printed point, "A. (2) Introduce …".
    lines = _lines(S, b_at, ex_at)
    head, labelled = _labelled(lines, r'^([A-F])\. \((\d)\)')
    criteria = [_criterion(label.lower(), label, marks, block) for label, marks, block in labelled]
    criteria.append(_expression(7, one))
    reqs = head + ([nb] if nb else [])
    text, _p = task_text(P, 'AT', 'b')
    out.append(_card(year, 'ol', 'AT', 'b', 15, _rubric(reqs, criteria), text,
                     _source(P, year, 'ol', 'AT', 'b', 'Äußerung zum Thema'),
                     tags['T-B']['primary'], sorted(set(_page_span(S, b_at, ex_at) + _page_span(S, ex_at, ex_at + 1))),
                     concept_for, question_ref, [PRACTICE]))
    # Schriftliche Produktion: the fill-in phrases ("St.") are their own
    # claim card (coordinator ruling 2); the grid holds Content and Expression.
    sp = _find(S, r'^SCHRIFTLICHE PRODUKTION')
    a_at = _find(S, r'^\(a\) ', sp)
    b_at = _find(S, r'^\(b\) ', a_at + 1)
    end = _find(S, r'^LISTENING COMPREHENSION', b_at)
    for letter, (lo, hi) in (('a', (a_at, b_at)), ('b', (b_at, end))):
        lines = [l for l in _lines(S, lo, hi) if l != 'OR']
        st_at = next(k for k, l in enumerate(lines) if l.startswith('St.'))
        phrases = []
        k = st_at + 1
        while k < len(lines) and re.match(r'^[•\uf0b7●]\s*(.+?)\s*\((\d)\)\s*$', lines[k]):
            m = re.match(r'^[•\uf0b7●]\s*(.+?)\s*\((\d)\)\s*$', lines[k])
            phrases.append((m.group(1), int(m.group(2))))
            k += 1
        st_marks = int(re.match(r'^St\. \((\d)\)', lines[st_at]).group(1))
        assert sum(m for _p, m in phrases) == st_marks, (year, letter, phrases)
        rest = lines[:st_at] + lines[k:]
        ex_line = next((l for l in rest if l.startswith('Ex.')), None)
        if letter == 'a':
            head, labelled = _labelled([l for l in rest if not l.startswith('Ex.')], r'^(Cl|[A-F])\.? \((\d)\)')
            cl = [x for x in labelled if x[0] == 'Cl']
            points = [x for x in labelled if x[0] != 'Cl']
            content_total = 16
            n = (content_total - sum(x[1] for x in cl)) // points[0][1]
            assert all(x[1] == points[0][1] for x in points) and len(points) >= n
            criteria = _points(n, points[0][1]) + [_criterion('cl', 'Cl', x[1], x[2]) for x in cl]
            reqs = head + [l for x in points for l in x[2]] + ([ex_line] if ex_line else [])
        else:
            c_at = next(k for k, l in enumerate(rest) if re.match(r'^C \(12\)', l))
            guide = [l for l in rest[c_at:] if not l.startswith('Ex.')]
            criteria = [_criterion('content', 'C', 12, guide)]
            reqs = [l for l in rest[:c_at]] + ([ex_line] if ex_line else [])
        content = [k_['id'] for k_ in criteria]
        criteria.append(_expression(10, two, {
            'label': 'Lower Ex.', 'maxMarks': 7, 'permittedMarks': list(range(8)), 'bands': one,
            'contentCriteria': content, 'contentAtMost': 7, 'rule': sp_rule}))
        if nb:
            reqs.append(nb)
        text, _p = task_text(P, 'SP', letter)
        title = 'Schriftliche Produktion'
        pages = sorted(set(_page_span(S, lo, hi) + _page_span(S, ex_at, ex_at + 1)))
        topic = tags[f'P-{letter.upper()}']['primary']
        total = sum(k_['maxMarks'] for k_ in criteria)
        out.append(_card(year, 'ol', 'SP', letter, total, _rubric(reqs, criteria), text,
                         _source(P, year, 'ol', 'SP', letter, title), topic, pages, concept_for,
                         question_ref, [PRACTICE, PRACTICE_LOWER] + ([PRACTICE_POINTS] if letter == 'a' else [])))
        # The fill-in phrases: one claim row per phrase at its printed price.
        ask = re.search(r'(Firstly, complete[^.]*\.)', ' '.join(text.split('\n')))
        out.append({
            'id': f'de-{year}-ol-sp-{letter}-fill',
            'subjectId': 'german', 'level': 'ordinary', 'year': year, 'section': 'SP',
            'topicId': topic, 'conceptId': concept_for(ask.group(1) if ask else text),
            'questionRef': f'{question_ref(year, "ol", "SP", None, letter)} — the phrases in the box',
            'questionText': ask.group(1) if ask else text,
            'tariffModel': {'kind': 'fixed'}, 'totalMarks': st_marks,
            'rows': [{'id': f'r-{n_}', 'kind': 'point', 'verbatim': phrase, 'marks': m,
                      **({'contextNote': (f'The scheme prices the phrases on their own line: '
                                          f'“{lines[st_at]}”')} if n_ == 1 else {})}
                     for n_, (phrase, m) in enumerate(phrases, start=1)],
            'notes': (f'The scheme prices this part {st_marks} on its own line, apart from '
                      f'Content and Expression; the paper prints it inside task ({letter}).'),
            'sourceMaterial': _source(P, year, 'ol', 'SP', letter, title),
        })
    return out


def cards(year, level, card_id, question_ref, concept_for):
    return (higher_cards if level == 'hl' else ordinary_cards)(year, card_id, question_ref, concept_for)


def _page_of(S, text):
    page = 1
    for line in S.lines:
        m = re.match(r'^##\s*Page\s*(\d+)', line.strip())
        if m:
            page = int(m.group(1))
        if text[:40] in line:
            return page
    return page


if __name__ == '__main__':
    import de_all
    y, l = int(sys.argv[1]), sys.argv[2]
    for card in cards(y, l, de_all.card_id, de_all.question_ref, de_all.concept_for):
        r = card.get('rubric')
        if r:
            print(card['id'], card['totalMarks'], [(k['id'], k['maxMarks'], len(k['guidance']),
                  (k.get('lowerScale') or {}).get('maxMarks')) for k in r['criteria']], card['schemePages'],
                  card['sourceMaterial']['pages'], card['topicId'])
        else:
            print(card['id'], card['totalMarks'], [(x['verbatim'], x['marks']) for x in card['rows']])
