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
# (2015-2016) a table of ONE column, the full scale alone ("12 CATEGORY
# DESCRIPTION" / "0 – 3 Length/relevance of response inadequate" / … / "12").
SCALE_ONE_HEAD = re.compile(r'^(\d{1,2})\s+CATEGORY DESCRIPTION$')
SCALE_ONE = re.compile(rf'^{RANGE}(?:\s+(.*))?$')


def _lines(S, start, stop):
    return [x for x in (_readable(l.strip()) for l in S.lines[start:stop]
                        if l.strip() and not PAGE.match(l.strip())) if x]


# 2014 Ordinary sets a few words in a font whose text layer is shifted into
# control characters: ",FK\x03KHLȕH\x03\x11\x11.. Ich bin ... Jahre alt." for
# "Ich heiße .. Ich bin …". Those words cannot be lifted; the line keeps only
# the words after them, as printed.
SHIFTED = re.compile(r'^.*[\x00-\x08\x0b-\x1f][\s.]*')


def _readable(line):
    return SHIFTED.sub('', line).strip() if SHIFTED.match(line) else line


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
    # 2021 Higher prints the "N.B. Take a global view …" line above the
    # table as well as below it: the table ends at the one after its first
    # category.
    # (2014 sets the ranges at the head of the category's first line: "0 – 2
    # 0 – 4 Vocabulary very inadequate …".)
    first = _find(S, r'^(?:[\d\s–-]+\s)?Vocabulary', start)
    # It ends at the N.B. under it, or (deferred 2022, which prints that N.B.
    # above the table only) at whatever the scheme prints next.
    stops = [_find(S, rx, first) for rx in (
        r'^N\.B\. Take a global view', r'^SCHRIFTLICHE PRODUKTION', r'^Marking Written Expression',
        r'^Reasonable Accommodations', r'^LISTENING COMPREHENSION', r'^TEXT\s+(?:I{1,3}|[123])\b')]
    stop = min((x for x in stops if x is not None), default=None)
    single = _single_column(S, start, stop)
    if single is not None:
        return single
    lines = _lines(S, start + 1, stop)
    cats = []
    for line in lines:
        m = SCALE_ROW.match(line)
        if line.startswith('Vocabulary') or (m and (m.group(5) or '').startswith('Vocabulary')):
            cats.append({'lines': [], 'one': None, 'two': None})
        if not cats:
            continue
        if m and cats[-1]['one'] is None:
            cats[-1]['one'] = (int(m.group(1)), int(m.group(2) or m.group(1)))
            cats[-1]['two'] = (int(m.group(3)), int(m.group(4) or m.group(3)))
            # The range column cuts the descriptor where it is printed
            # ("… Verb" / "4 – 6 forms/tense …"): the words either side are
            # kept apart, as the scheme's text has them.
            cats[-1]['lines'].append(None)
            if m.group(5) and not re.fullmatch(r'\*+', m.group(5).strip()):
                cats[-1]['lines'].append(m.group(5).strip())
            continue
        if re.fullmatch(r'\*+', line):
            # (deferred 2022) the asterisk row the scheme sets between a
            # category's upper and lower descriptors: a rule, not words.
            cats[-1]['lines'].append(None)
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


def _single_column(S, start, stop):
    """A one-column expression table, (None, [bands], N.B., at), or None.

    2015 prints the full scale alone, with no lower one: "12 CATEGORY
    DESCRIPTION", then each category's range beside the descriptor line it
    is printed level with. Its first category is the one line "0 – 3
    Length/relevance of response inadequate", with no "Vocabulary …" to open
    it, and its last range is a bare "12", which only the page break after
    it tells apart from a page number."""
    raw = [l.strip() for l in S.lines[start + 1:stop]]
    at = next((k for k, l in enumerate(raw) if SCALE_ONE_HEAD.match(l)), None)
    if at is None or any(SCALE_ROW.match(l) for l in raw):
        return None
    top = int(SCALE_ONE_HEAD.match(raw[at]).group(1))
    rest = [l for l in raw[at + 1:] if l]
    cats = []
    for k, line in enumerate(rest):
        if re.match(r'^##\s*Page\s*\d+\s*$', line):
            continue
        after = rest[k + 1] if k + 1 < len(rest) else '## Page'
        if re.fullmatch(r'\d{1,3}', line) and after.startswith('## Page'):
            continue                  # the page's own number
        m = SCALE_ONE.match(line)
        if m and int(m.group(2) or m.group(1)) <= top:
            if not cats or cats[-1]['two'] is not None:
                cats.append({'lines': [], 'two': None})
            cats[-1]['two'] = (int(m.group(1)), int(m.group(2) or m.group(1)))
            cats[-1]['lines'].append(None)
            if m.group(3):
                cats[-1]['lines'].append(m.group(3).strip())
            continue
        if line.startswith('Vocabulary'):
            cats.append({'lines': [], 'two': None})
        if cats:
            cats[-1]['lines'].append(line)
    bands = []
    for n, c in enumerate(cats, start=1):
        assert c['two'], (S.year, S.level, c)
        bands.append({'label': f'Category {n}', 'marks': list(range(c['two'][0], c['two'][1] + 1)),
                      'guidance': _join(c['lines'])})
    assert bands and bands[-1]['marks'][-1] == top, (S.year, S.level, bands)
    # 2015's Äußerung prints the N.B. above the table, Schriftliche
    # Produktion's below it.
    nb = ' '.join(_lines(S, stop, stop + 3)) if stop is not None else ''
    nb = re.match(r'^(N\.B\. Take a global view.*?categor(?:y|ies)[^.]*\.)', nb)
    if nb is None:
        above = _find(S, r'^N\.B\. Take a global view', start)
        if above is not None and above < start + 1 + at:
            nb = re.match(r'^(N\.B\. Take a global view.*?categor(?:y|ies)[^.]*\.)',
                          ' '.join(_lines(S, above, above + 3)))
    return None, bands, (nb.group(1) if nb else None), start


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


CONTENT_13 = re.compile(r'^Content = 13 \(A = \d; B = \d; C = \d; Dis\. 2\)')


def theme_grid(S, letter):
    """The content points of Äußerung option (a) or (b): its head lines, and
    [(id, label, marks, [printed lines])] for A, B, C and Dis."""
    # 2015 heads (b) "Content = 13 (A = 4; B = 4; C = 3; Dis. 2)" over points
    # it prices A (3), B (4), C (4): the points are read as printed.
    starts = [i for i, l in enumerate(S.lines) if CONTENT_13.match(l.strip())]
    at = starts['ab'.index(letter)]
    end = _find(S, r'^Dis\.:? 2 marks', at)       # "Dis.: 2 marks" (2018)
    lines = _lines(S, at, end + 1)
    head, points, cur = [], [], None
    for line in lines:
        m = re.match(r'^([ABC])[.:]? \((\d)(?: marks)?\)$', line)
        if m:
            cur = {'id': m.group(1).lower(), 'label': m.group(1), 'marks': int(m.group(2)), 'lines': []}
            points.append(cur)
            continue
        if re.match(r'^Dis\.:? 2 marks', line):
            points.append({'id': 'dis', 'label': 'Dis.', 'marks': 2, 'lines': [line]})
            cur = None
            continue
        (cur['lines'] if cur else head).append(line)
    assert [p['marks'] for p in points] == [3, 4, 4, 2], (S.year, S.level, letter, points)
    return head, points


# The furniture of the extra-work pages that close the Higher booklet (2022-
# 2026), read on as if it were the last task's: "Spás le haghaidh obair
# bhreise. / Lipéadaigh aon obair bhreise … / This is space for extra work.
# Label any such extra work clearly with the question number and part."
EXTRA_WORK = re.compile(r'^(?:Spás le haghaidh obair bhreise|This is space for extra work)', re.I)


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
    # The length the task asks for closes it; read a point above the
    # bullet's last line beside it, it is put back at the end: "(100
    # Wörter)" / "Was würden Sie nie online kaufen? …" (2016 Higher).
    count = [k for k, raw in enumerate(lines) if re.fullmatch(r'\s*\(\d{2,3} Wörter\)\s*', raw)]
    if (len(count) == 1 and count[0] == len(lines) - 2
            and re.search(r'[.?!]\s*$', lines[-1]) and not lines[-1].lstrip().startswith(('•', '\uf0b7'))):
        lines = lines[:count[0]] + [lines[-1], lines[count[0]]]
    out = []
    for raw in lines:
        t = ' '.join(raw.replace('\uf0b7', '•').split())
        if not t:
            continue
        if EXTRA_WORK.match(t):
            break                    # the booklet's extra-work pages, never the task
        if re.fullmatch(r'[_\s]+', t):
            continue                 # the ruled lines the answer is written on (2020)
        # A title is a few words ("Europas Jugend trifft sich in Straßburg");
        # a longer first line is a sentence wrapped: "You and a couple of
        # friends want to travel to" / "Austria next year." (2015 Ordinary).
        title = (len(out) == 1 and not re.search(r'[.?!:)/]$', out[0]) and t[:1].isupper()
                 and len(out[0].split()) <= 7)
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
    skipping = False
    for line in lines[start:]:
        # The box and the letter's gapped opening between the instruction and
        # its bullets are read here only in their right-hand halves ("viel
        # ______ .", 2016 Ordinary): they are on the page carried with the
        # card, and the task resumes at its first bullet.
        if skipping and not re.match(r'^[•\uf0b7]', line):
            continue
        skipping = False
        # The Irish column's last "/" can sit past the gutter, ahead of the
        # English marker: "/ (a) You are writing a letter …" (2016 Ordinary).
        out.append(re.sub(r'^(?:/\s*)?\(\s*[ab]\s*\)\s*', '', line) if not out else line)
        # … and the page foot shares the last printed row: "• Write a
        # suitable closing sentence Page 16 of 20".
        out[-1] = re.sub(r'\s*Page \d+ of \d+\s*$', '', out[-1])
        if re.search(r'words\.\)$|Wörter\)$', line):
            break
        if re.search(r'\bwords\.$', out[-1]):
            skipping = True
    return [x for x in out if x]


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


def atlas_written(year, level, sitting=None):
    with open(TAGS, encoding='utf-8') as fh:
        papers = json.load(fh)
    fileid = f'LC011{"A" if level == "hl" else "G"}LP000{"BV" if year >= 2019 else "EV"}' \
             f'{"-deferred" if sitting else ""}.pdf'
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
def higher_cards(year, card_id, question_ref, concept_for, sitting=None):
    P = DePaper(year, 'hl', 'german', sitting)
    S = DeScheme(year, 'hl', 'german', sitting)
    tags = atlas_written(year, 'hl', sitting)
    out = []
    # Äußerung zum Thema: A, B, C, Dis. as printed; Expression 12, Lower E 7.
    at_one, at_two, at_nb, at_at = expression_scale(S, r'^Marking Written Expression in [ÄA]u[ßs]{1,2}erung')
    # (2015) a table of the full scale alone: no lower E, and no rule for it.
    at_rule = rule_text(S, at_at, r'^If the content mark is', r'out of \d+') if at_one else None
    for letter in 'ab':
        head, points = theme_grid(S, letter)
        criteria = [_criterion(p['id'], p['label'], p['marks'], p['lines']) for p in points]
        criteria.append(_expression(12, at_two, {
            'label': 'Lower E', 'maxMarks': 7, 'permittedMarks': list(range(8)), 'bands': at_one,
            'contentCriteria': [p['id'] for p in points], 'contentAtMost': 8, 'wordsUnder': 60,
            'rule': at_rule} if at_one else None))
        # A bullet opens an instruction of its own: an instruction printed
        # without a full stop ("• Award content marks first", 2019-2020) is
        # never joined to the bullet below it.
        reqs = ['Content = 13 (A = 3; B = 4; C = 4; Dis. 2)', 'Expression = 12'] + _join(
            [x for l in head if not re.match(r'^(Content|Expression) =', l)
             for x in ([None] if re.match(r'^[•\uf0b7]', l) else []) + [l.lstrip('•\uf0b7 ').strip()]])
        if at_nb:
            reqs.append(at_nb)
        text, _page = task_text(P, 'AT', letter)
        starts = [i for i, l in enumerate(S.lines) if CONTENT_13.match(l.strip())]
        pages = sorted(set(_page_span(S, starts['ab'.index(letter)], starts['ab'.index(letter)] + 1)
                           + _page_span(S, at_at, at_at + 1)))
        out.append(_card(year, 'hl', 'AT', letter, 25, _rubric(reqs, criteria), text,
                         _source(P, year, 'hl', 'AT', letter, 'Äußerung zum Thema'),
                         tags[f'T-{letter.upper()}']['primary'], pages, concept_for, question_ref,
                         [PRACTICE] + ([PRACTICE_LOWER] if at_one else [])))
    # Schriftliche Produktion: (a) letter, any four of A-E; (b) photo, any
    # five of A-F; Op./Cl. on the letter, Dis. 5; Expression 25, Lower E 18.
    sp_one, sp_two, sp_nb, sp_at = expression_scale(S, r'^Marking Written Expression in Schriftliche')
    sp_rule = rule_text(S, sp_at, r'^If the content mark is', r'out of \d+') if sp_one else None
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
        # The deferred 2022 photo task prints no "Answer any five …" but "mark
        # all and award marks for the best five".
        rx = r'Answer any (\w+) of the|for the best (\w+)\b'
        want = re.search(rx, ' '.join(head)) or re.search(rx, ' '.join(_lines(S, lo - 4, lo)))
        points = [x for x in labelled if x[0] not in ('Op', 'Cl')]
        # Until 2020 the candidate answered EVERY point: the scheme prints no
        # "Answer any four …" and its content adds up only with all of them
        # ("Content = 25 marks": Op. 2 + A-D 4 each + Cl. 2 + Dis. 5). Each
        # point is then a criterion of its own, as Op. and Cl. are.
        every = want is None
        n = len(points) if every else {'four': 4, 'five': 5}[(want.group(1) or want.group(2)).lower()]
        if every:
            # The content must add up with every point: "Content = 25 marks".
            assert sum(x[1] for x in labelled) + 5 == 25, (year, letter, labelled)
        criteria, reqs = [], [l for l in head if not l.startswith('Dis.:')]
        for label, marks, block in labelled:
            block = [l for l in block if not l.startswith('Dis.:')]
            if label in ('Op', 'Cl'):
                criteria.append(_criterion(label.lower(), f'{label}.', marks, block))
            else:
                # Where every point is answered, a point is priced as printed
                # (2015's photo task: A. (3) … E. (5)).
                assert every or marks == 4, (year, letter, label)
                if every:
                    criteria.append(_criterion(label.lower(), f'{label}.', marks, block))
                else:
                    reqs.extend(block)
        cl = [k for k in criteria if k['id'] == 'cl']
        chosen = ([k for k in criteria if k['id'] not in ('op', 'cl')] if every
                  else _points(n, 4))
        criteria = [k for k in criteria if k['id'] == 'op'] + chosen + cl + [
            _criterion('dis', 'Dis.', 5, [dis])]
        content = [k['id'] for k in criteria]
        criteria.append(_expression(25, sp_two, {
            'label': 'Lower E', 'maxMarks': 18, 'permittedMarks': list(range(19)), 'bands': sp_one,
            'contentCriteria': content, 'contentAtMost': 12, 'wordsUnder': 100, 'rule': sp_rule}
            if sp_one else None))
        if sp_nb:
            reqs.append(sp_nb)
        text, _page = task_text(P, 'SP', letter)
        pages = sorted(set(_page_span(S, lo, hi) + _page_span(S, sp_at, sp_at + 1)))
        assert len(points) >= n, (year, letter, len(points), n)
        out.append(_card(year, 'hl', 'SP', letter, 50, _rubric(reqs, criteria), text,
                         _source(P, year, 'hl', 'SP', letter, 'Schriftliche Produktion'),
                         tags[f'P-{letter.upper()}']['primary'], pages, concept_for, question_ref,
                         [PRACTICE] + ([PRACTICE_LOWER] if sp_one else [])
                         + ([] if every else [PRACTICE_POINTS])))
    return out


# ----------------------------------------------------------- Ordinary -----
def ordinary_cards(year, card_id, question_ref, concept_for):
    P = DePaper(year, 'ol', 'german')
    S = DeScheme(year, 'ol', 'german')
    tags = atlas_written(year, 'ol')
    out = []
    # The one expression table: column one is Äußerung's 7 and Schriftliche
    # Produktion's "Lower Ex." 7, column two the full 10.
    # 2018 prints the head over three lines, "Guidelines for marking
    # Expression in:" / "Äußerung zum Thema (a) and (b)" / "Schriftliche …";
    # 2017 sets "Äuβerung" with a Greek beta.
    one, two, nb, ex_at = expression_scale(
        S, r'^Guidelines for marking Expression in(?:\s+[ÄA]u[ßsβ]{1,2}erung zum Thema|:\s*$'
           r'|\s+Schriftliche Produktion \(a\) and \(b\)$)')     # (the last, 2013)
    # "… (0-7) for expression." (2022-2026) or "… for expression and write
    # “Lower Ex.” to indicate this." (2021); 2014 capitalises "Expression".
    sp_rule = rule_text(S, ex_at, r'^N\.B\. If the content mark (?:in the Schriftliche|is \d)',
                        r'for [Ee]xpression(?:\.| and write .*?to indicate this\.)')
    at = _find(S, r'^TEXT II: [ÄA]U[ßS]{1,2}ERUNG ZUM THEMA')
    a_at = _find(S, r'^\(a\) ', at)
    # (2023 heads it "E-Mail (25-30 words) (15 marks)".)
    b_at = _find(S, r'^E-?Mail schreiben|^E-mail schreiben|^E-?Mail \(\d|^\(b\) ', a_at + 1)
    head_lines = _lines(S, at, a_at)
    # (a) the dialogue: one criterion per printed turn, "(A1)" … "(F2)", with
    # the prompt printed above it.
    # 2021 prints a short "Guidelines for marking expression in ÄUSSERUNG"
    # after each option and TEXT III's questions before the expression table:
    # an option's block ends at whichever comes first.
    def _end(after, limit):
        stop = _find(S, r'^(?:Guidelines for marking expression|TEXT III)', after + 1)
        return min(x for x in (stop, limit) if x is not None)
    a_end, b_end = _end(a_at, b_at), _end(b_at, ex_at)
    lines = _lines(S, a_at, a_end)
    head, crit, prompt = [], [], []
    for line in lines:
        if line == 'OR':
            continue                  # 2018 prints "OR" between (a) and the e-mail
        # "(A2) Jan Kammann: …", in 2018 "A 2: Dagi Bee: …" / "E 1 Mirko: …",
        # in 2017 "A: 2 Florian: …", in 2015 "E2: Julia: …", in 2014 "A. (2)
        # Kristina: …".
        m = (re.match(r'^\(([A-F])(\d)\)\s*(.*)$', line) or re.match(r'^([A-F]):? (\d)\b:?\s*(.*)$', line)
             or re.match(r'^([A-F])(\d):\s*(.*)$', line)
             or re.match(r'^([A-F])\.\s*\((\d)\)\s*(.*)$', line))     # "A. (2) Kristina: …" (2014)
        if m:
            crit.append(_criterion(m.group(1).lower(), m.group(1), int(m.group(2)), prompt + [line]))
            prompt = []
        elif line.startswith('Sie:'):
            prompt.append(line)
        elif prompt and line.startswith('N.B.'):
            # (2014 prints its "N.B. Bracket off irrelevant content …" under
            # the closing prompt: a requirement of the task, not the prompt's
            # second line.)
            head.append(line)
        elif prompt:
            # The prompt's own second line: "Sie: … Welche Kleidung soll man
            # auf ein Festival" / "mitnehmen?" (2017), "Sie: Herr Kammann, …" /
            # "Warum?" (2020).
            prompt[-1] = f'{prompt[-1]} {line}'
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
                     tags['T-A']['primary'], sorted(set(_page_span(S, a_at, a_end) + _page_span(S, ex_at, ex_at + 1))),
                     concept_for, question_ref, [PRACTICE]))
    # (b) the e-mail: one criterion per printed point, "A. (2) Introduce …".
    lines = _lines(S, b_at, b_end)
    # "A. (2) Introduce yourself …", or in 2016 "(A3) Give your personal details".
    head, labelled = _labelled(lines, r'^\(?([A-F])(?:\. \(|)(\d)\)')
    criteria = [_criterion(label.lower(), label, marks, block) for label, marks, block in labelled]
    criteria.append(_expression(7, one))
    reqs = head + ([nb] if nb else [])
    text, _p = task_text(P, 'AT', 'b')
    out.append(_card(year, 'ol', 'AT', 'b', 15, _rubric(reqs, criteria), text,
                     _source(P, year, 'ol', 'AT', 'b', 'Äußerung zum Thema'),
                     tags['T-B']['primary'], sorted(set(_page_span(S, b_at, b_end) + _page_span(S, ex_at, ex_at + 1))),
                     concept_for, question_ref, [PRACTICE]))
    # Schriftliche Produktion: the fill-in phrases ("St.") are their own
    # claim card (coordinator ruling 2); the grid holds Content and Expression.
    # The section head, priced — never "Schriftliche Produktion (a) and (b)"
    # inside the expression guidelines printed above it (2018).
    sp = _find(S, r'^SCHRIFTLICHE PRODUKTION\s*:?\s*\(?\d')
    a_at = _find(S, r'^\(a\) ', sp)
    b_at = _find(S, r'^\(b\) ', a_at + 1)
    # The listening test follows, or (2021, which prints it first) its
    # transcript, or the document ends.
    end = _find(S, r'^(?:LISTENING COMPREHENSION|Teil\s+(?:I|1)\b)', b_at) or len(S.lines)
    for letter, (lo, hi) in (('a', (a_at, b_at)), ('b', (b_at, end))):
        lines = [l for l in _lines(S, lo, hi) if l != 'OR']
        st_at = next(k for k, l in enumerate(lines) if l.startswith('St.'))
        phrases = []
        k = st_at + 1
        # 2014 prints "St. (5)" alone and its instruction on the line below:
        # "Complete the first paragraph by inserting … (5 x 1 mark)".
        st_line = lines[st_at]
        # (2013 prints its price on the line below: "St. (5) Complete the
        # first paragraph …" / "(5 x 1 mark)".)
        if k < len(lines) and (
                (re.fullmatch(r'St\. \(\d\)', st_line) and re.search(r'\(\d x 1\s*mark\)', lines[k]))
                or (not re.search(r'\(\d x 1\s*mark\)', st_line) and re.fullmatch(r'\(\d x 1\s*mark\)', lines[k]))):
            st_line = f'{st_line} {lines[k]}'
            k += 1
        # (2016's text layer carries its bullet as a control character, \x02;
        # 2014 sets a hyphen.)
        bullet = r'^(?:[•\uf0b7●\x02]|-(?=\s))\s*(.+?)\s*\((\d)\)\s*$'
        while k < len(lines) and re.match(bullet, lines[k]):
            m = re.match(bullet, lines[k])
            phrases.append((m.group(1), int(m.group(2))))
            k += 1
        st_marks = int(re.match(r'^St\. \((\d)\)', lines[st_at]).group(1))
        assert sum(m for _p, m in phrases) == st_marks, (year, letter, phrases)
        rest = lines[:st_at] + lines[k:]
        # "Ex. (10) Use the grid on Page 19 to calculate expression mark in
        # relation to" / "C (Content)" (2014): the line's own end, wrapped.
        # Or "Ex. (10)" alone over "Use the grid on Page 19 …" (2014 (b)).
        for j in range(len(rest) - 1):
            if ((rest[j].startswith('Ex.') and rest[j].endswith(' to') and rest[j + 1].startswith('C (Content)'))
                    or (re.fullmatch(r'Ex\. \(\d{1,2}\)', rest[j]) and rest[j + 1].startswith('Use the grid'))):
                rest = rest[:j] + [f'{rest[j]} {rest[j + 1]}'] + rest[j + 2:]
                break
        ex_line = next((l for l in rest if l.startswith('Ex.')), None)
        if letter == 'a':
            head, labelled = _labelled([l for l in rest if not l.startswith('Ex.')], r'^(C[lL]|[A-F])\.? \((\d)\)')
            labelled = [['Cl' if x[0] == 'CL' else x[0]] + x[1:] for x in labelled]   # "CL. (1)", 2017
            cl = [x for x in labelled if x[0] == 'Cl']
            points = [x for x in labelled if x[0] != 'Cl']
            # The content total the section prints, "(St. = 4, C = 16, Ex. =
            # 10)" (2021-2026) or "(St. = 5, C = 15, Ex. = 10)" (2019-2020).
            # 2022 prints the closing apart, "(St. = 4, C = 15, CL = 1, Ex. =
            # 10)": the content the grid holds is then C and CL together.
            # (2017 prints it under "(a) Letter": "(Start = 5, Content = 15,
            # Expression = 10)".)
            sp_head = ' '.join(_lines(S, sp, lo + 3))
            content_total = int(re.search(r'\bC(?:ontent)?\s*=\s*(\d+)', sp_head).group(1))
            cl_apart = re.search(r'\bCL\s*=\s*(\d+)', sp_head)
            content_total += int(cl_apart.group(1)) if cl_apart else 0
            # Until 2020 the candidate wrote EVERY point, priced as printed
            # ("A. (3)", "E. (4)"): no "answer any FIVE points" is printed and
            # the points and Cl. add to C exactly (2025 prints no "any five"
            # either, but its six points of 3 and Cl. 1 are 19 against C = 16:
            # a choice). Each point is then a criterion of its own.
            every = (not re.search(r'\bany\s+\w+\s+points?\b', ' '.join(head), re.I)
                     and sum(x[1] for x in points + cl) == content_total)
            if every:
                criteria = ([_criterion(x[0].lower(), x[0], x[1], x[2]) for x in points]
                            + [_criterion('cl', 'Cl', x[1], x[2]) for x in cl])
                assert sum(k_['maxMarks'] for k_ in criteria) == content_total, (year, letter)
                reqs = head + ([ex_line] if ex_line else [])
            else:
                n = (content_total - sum(x[1] for x in cl)) // points[0][1]
                assert all(x[1] == points[0][1] for x in points) and len(points) >= n
                criteria = _points(n, points[0][1]) + [_criterion('cl', 'Cl', x[1], x[2]) for x in cl]
                reqs = head + [l for x in points for l in x[2]] + ([ex_line] if ex_line else [])
        else:
            every = False
            c_at = next(k for k, l in enumerate(rest) if re.match(r'^C \(\d{1,2}\)', l))
            c_marks = int(re.match(r'^C \((\d{1,2})\)', rest[c_at]).group(1))
            guide = [l for l in rest[c_at:] if not l.startswith('Ex.')]
            criteria = [_criterion('content', 'C', c_marks, guide)]
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
                         question_ref, [PRACTICE, PRACTICE_LOWER] + ([PRACTICE_POINTS] if letter == 'a' and not every else [])))
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
                                          f'“{st_line}”')} if n_ == 1 else {})}
                     for n_, (phrase, m) in enumerate(phrases, start=1)],
            'notes': (f'The scheme prices this part {st_marks} on its own line, apart from '
                      f'Content and Expression; the paper prints it inside task ({letter}).'),
            'sourceMaterial': _source(P, year, 'ol', 'SP', letter, title),
        })
    return out


def cards(year, level, card_id, question_ref, concept_for, sitting=None):
    if not sitting:
        return (higher_cards if level == 'hl' else ordinary_cards)(year, card_id, question_ref, concept_for)
    # A deferred sitting's cards are "de-2022-hl-deferred-…", cited "… —
    # Deferred sitting", on the deferred booklet.
    out = higher_cards(year, card_id, lambda *a: f'{question_ref(*a)} — Deferred sitting',
                       concept_for, sitting)
    for card in out:
        card['id'] = card['id'].replace(f'de-{year}-{level}-', f'de-{year}-{level}-deferred-', 1)
        src = card['sourceMaterial']
        src['attribution'] = src['attribution'].replace('examination paper', 'deferred examination paper')
    return out


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
