#!/usr/bin/env python3
"""Italian written tasks (Section C) and Higher essays (B3) as marking-grid cards.

    python3 scripts/markbank/authoring/it_writing.py 2026 hl     # print one sitting's cards

Review pack 1, treatment D: one marking-grid card per printed written task, on
the grid the live French, German and Spanish writing cards use (rubric system
'french'). Every criterion, every guidance line and every band is a line of
the scheme, lifted verbatim and asserted present in the scheme .md before it is
used; the question is the paper's own printed lines. The only words that are
the app's own are `markingGuideNote`.

A printed choice is one card (R7): Higher C1's five prompts "(a)-(e)", of which
a candidate answers three, are one card cited "Section C Q1(a)–(e)". A task the
scheme prices by fields or by order, not by a grid (Ordinary C2's form and C3's
sequence), is a point card, built here too.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

from fr_paper import _rows                                       # noqa: E402
import it_paper as IP                                            # noqa: E402
from it_scheme import schemes_dir                                # noqa: E402
from it_topics import ITALIAN_WORDS, ENGLISH_IRISH_WORDS         # noqa: E402

LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}
TOPIC = {('hl', 1): 'italian-6-0', ('hl', 2): 'italian-6-1', ('hl', 3): 'italian-6-2',
         ('ol', 1): 'italian-6-3', ('ol', 2): 'italian-6-4', ('ol', 3): 'italian-6-5'}
ESSAY_TOPIC = 'italian-5-2'
NOTE = ('Place your answer on each criterion the scheme prints. Every band, '
        'point and rule here is the SEC marking scheme\'s own wording.')
RANGE = re.compile(r'^(\d{1,2})\s*[-–]\s*(\d{1,2})\s+(.*)$')


def flat(s):
    return ' '.join(str(s).split())


class Scheme:
    def __init__(self, year, level):
        self.path = os.path.join(schemes_dir(), f'{year}-{level}.md')
        raw = open(self.path, encoding='utf-8').read()
        self.lines, self.page_of, page = [], [], 1
        for l in raw.split('\n'):
            m = re.match(r'^## Page (\d+)', l)
            if m:
                page = int(m.group(1))
                continue
            if l.strip() and not re.fullmatch(r'\d{1,3}', l.strip()):
                self.lines.append(l.strip())
                self.page_of.append(page)
        self.flat = flat(' '.join(self.lines))

    def pages(self, i, j):
        return sorted(set(self.page_of[i:j + 1]))

    def at(self, pattern, start=0):
        rx = re.compile(pattern, re.I)
        for i in range(start, len(self.lines)):
            if rx.search(self.lines[i]):
                return i
        raise AssertionError(f'{self.path}: no line matches {pattern!r}')

    def span(self, start_pat, stop_pat, start=0, include_start=True):
        i = self.at(start_pat, start)
        j = self.at(stop_pat, i + 1)
        return self.lines[i if include_start else i + 1:j]

    def check(self, *strings):
        for s in strings:
            assert flat(s) in self.flat, f'{self.path}: {s!r} is not in the scheme'


def bands_from(lines, pick=0):
    """[(lo, hi, [descriptor lines])] from "7 - 10 Idiomatic Italian, …" lines.

    A descriptor that wraps continues on the next line; a range line opens a
    band. `pick` chooses the column where a line prints two ranges ("13 – 15
    21 – 25": essays, then letter).
    """
    out = []
    for l in lines:
        two = re.match(r'^(\d{1,2})\s*[-–]\s*(\d{1,2})\s+(\d{1,2})\s*[-–]\s*(\d{1,2})\s*$', l)
        if two:
            raw = re.findall(r'\d{1,2}\s*[-–]\s*\d{1,2}', l)[pick]
            lo, hi = (two.group(1), two.group(2)) if pick == 0 else (two.group(3), two.group(4))
            out.append([int(lo), int(hi), [], raw])
            continue
        m = RANGE.match(l)
        if m:
            raw = re.match(r'^\d{1,2}\s*[-–]\s*\d{1,2}', l).group(0)
            out.append([int(m.group(1)), int(m.group(2)), [m.group(3)], raw])
            continue
        if out and not re.match(r'^(Essays|N\.B\.|Language|_{3,})', l):
            out[-1][2].append(l)
    return out


def criterion(cid, label, maxm, guidance, bands=None, lower=None):
    c = {'id': cid, 'label': label, 'maxMarks': maxm,
         'permittedMarks': list(range(maxm + 1)), 'guidance': guidance}
    if bands:
        # The band's label is its range exactly as the scheme prints it.
        c['bands'] = [{'label': raw, 'marks': list(range(lo, hi + 1)), 'guidance': g}
                      for lo, hi, g, raw in sorted(bands, key=lambda b: b[0])]
    # The scheme's lower language scale: its printed rule caps the criterion
    # (out of 5 or 7; at Ordinary no language marks) while content is at or
    # under the printed figure. It prints no bands of its own.
    if lower:
        c['lowerScale'] = lower
    return c


def lower_scale(maxm, rule, at_most):
    return {'label': 'Lower', 'maxMarks': maxm,
            'permittedMarks': list(range(maxm + 1)), 'bands': [],
            'contentCriteria': ['content'], 'contentAtMost': at_most, 'rule': rule}


# ------------------------------------------------------------- the paper ---
IRISH = re.compile(r'\b(?:agus|na|an|ar|do|le|go|nó|Freagair|Scr[íi]obh|Roghnaigh|Aiste|'
                   r'marc|Scr[íi]bhneoireacht|l[ée]amhthuiscint|sliocht|faoi|Threoir|'
                   r'Fhoirmi[úu]il|Litir|Comhr[áa]|Neamhfhoirmi[úu]il|ceist|cheist|D[ée]an|s[íi]os)\b', re.I)
PAGE_FURNITURE = re.compile(r'^(?:Leaving Certificate|Italian\s*[—–-]|Iod[áa]ilis\s*[—–-]|Scr[úu]d[úu]'
                            r'|Lch\s+\d|Page\s+\d|\d{1,3}$|_+$)', re.I)


# Where the last task ends: the back pages that follow it (extra-work pages,
# acknowledgements, the copyright notice, a blank page, the back cover).
TASK_END = re.compile(r'^(?:You may use this page for extra work|Make sure to label extra work'
                      r'|Acknowledgements?$|Admhálacha|Admháil|Copyright notice|Fógra Cóipchirt'
                      r'|Leathanach Bán|Blank Page)', re.I)


def paper_task(year, level, item, english_only=False):
    """The printed task: the English rubric and the Italian task, in page order.

    Irish lines are left out (the task itself is set in Italian; the rubric is
    kept in English). A head the converter welds to its Irish twin — "Aiste
    faoi Threoir. (25 marc) 2. Guided Composition." — still opens the task.
    """
    P = IP.ItPaper(year, level)
    marked = P.pages.get('C', [])
    # every page from Section C's first to the end: a task may run onto a page
    # that prints no marker of its own (2026 Ordinary's dialogue, page 17)
    with IP.pymupdf.open(P.path) as doc:
        pages = list(range(marked[0], doc.page_count + 1)) if marked else []
    lines, page_of, on = [], None, False
    opens = re.compile(rf'(?:^|\s){item}\s*\.\s')
    closes = re.compile(rf'(?:^|\s){item + 1}\s*\.\s')
    for page in pages:
        for _p, groups in _rows(P.path, page - 1, page):
            for x, side, text in groups:
                s = IP._clean(text)
                if not s or PAGE_FURNITURE.match(s):
                    continue
                s = s.replace('\uf0b7', '•')
                if on and lines and TASK_END.match(s):
                    return lines, page_of
                # "NÓ / OR" between the two options of a choice is not task text.
                if on and re.fullmatch(r'NÓ\s*/\s*OR', s):
                    continue
                # A page with no column bound of its own reads every group as
                # 'L'; the English column is the right half of the sheet.
                if x >= 0.45 * P.width:
                    side = 'R'
                if on and closes.search(s + ' '):
                    return lines, page_of
                if not on and opens.search(s + ' '):
                    on, page_of = True, page
                    heads = [m.start(1) for m in re.finditer(rf'(?:^|\s)({item}\s*\.\s)', s + ' ')]
                    if heads and heads[-1] > 0:
                        # "Aiste faoi Threoir. (25 marc) 2. Guided Composition.
                        # (25 marks) Déan cur síos …": keep the English head,
                        # up to the Irish that follows it.
                        tail = s[heads[-1]:]
                        cut = IRISH.search(tail, 3)
                        lines.append(tail[:cut.start()].strip() if cut else tail)
                        continue
                if not on:
                    continue
                if side != 'R' and english_only:
                    continue
                if side != 'R':
                    welded = [m.start(1) for m in re.finditer(rf'(?:^|\s)({item}\s*\.\s+[A-Z])', s)]
                    if welded and welded[-1] > 0:
                        tail = s[welded[-1]:]
                        cut = IRISH.search(tail, 3)
                        lines.append(tail[:cut.start()].strip() if cut else tail)
                        continue
                    # An English instruction welded after its Irish twin in
                    # one group: "Déan cur síos ar an gcaoi ar eagraigh tú
                    # imeacht Describe how you organised a charity event."
                    # (2025 Higher C2) - the English sentence is kept.
                    en = re.search(r'\s((?:Describe|Write|Use|Using|Imagine|Choose|Answer|Tell|Explain)'
                                   r'\b[^.?!]*[.?!])\s*$', s)
                    if en and IRISH.search(s[:en.start()]):
                        lines.append(en.group(1))
                        continue
                    it = len(ITALIAN_WORDS.findall(s))
                    marked = bool(re.match(r'^(?:\([a-e]\)|•)', s))
                    irish = bool(IRISH.search(s)) and it < 2
                    # Inside a lettered task the page is the Italian task at
                    # full width: a short line with no listed Italian word
                    # ("Scrivete a:", "Via Nicotera 1,", "00195 Roma.", 2016)
                    # is the task's own, kept unless it reads as Irish.
                    in_task = any(re.match(r'^\([a-e]\)', l) for l in lines)
                    # The guided composition's ideas, "Notte prima esami –
                    # andare a letto presto – …", run on to a second line
                    # ("godersi vacanze.", 2019): a dash-separated list, or the
                    # line after one that ends on a dash, is the task's own.
                    if not IRISH.search(s) and lines and (
                            re.search(r'\s[–-]\s*$', lines[-1]) or (' – ' in s and ' – ' in lines[-1])):
                        in_task = True
                    if irish or not (it or marked or (in_task and not IRISH.search(s))):
                        continue
                if not lines or lines[-1] != s:
                    lines.append(s)
    return lines, page_of


def join_lines(lines):
    """The printed task as paragraphs: a line the paper wrapped is joined to
    the line it continues; a new item ("(a)", "•", "3.") or a line after a
    full stop, question mark, colon or closing bracket starts a new line."""
    out = []
    for l in lines:
        starts = re.match(r'^(?:\([a-e]\)|•|\d{1,2}\.|[A-Z]\.\s|\(\d+ marks?\))', l)
        if out and (out[-1].endswith(',') or not starts) and not re.search(r'[.?!:)]$', out[-1]):
            out[-1] = f'{out[-1]} {l}'
        else:
            out.append(l)
    return out


def english_column(year, level, item):
    """The English column of a bilingual writing page, read WORD by word.

    The row reader welds an Irish line and the English line beside it into
    one group when the gutter between them is narrow (2025 Ordinary page 16:
    "In both (a) and (b), write on any four of the" vanished into the Irish),
    so the column is cut at the page's own midline word by word instead.
    Returns (lines, page) from the item's head to the next item's.
    """
    P = IP.ItPaper(year, level)
    marked = P.pages.get('C', [])
    lines, page_of, on = [], None, False
    with IP.pymupdf.open(P.path) as doc:
        for pno in range(marked[0] - 1, doc.page_count) if marked else []:
            page = doc[pno]
            mid = page.rect.width * 0.47
            rows = {}
            for x0, y0, x1, y1, w, *_ in page.get_text('words'):
                if x0 < mid:
                    continue
                key = round((y0 + y1) / 2 / 3)
                rows.setdefault(key, []).append((x0, w))
            for key in sorted(rows):
                text = IP._clean(' '.join(w for _x, w in sorted(rows[key])))
                if not text or PAGE_FURNITURE.match(text):
                    continue
                if on and re.match(rf'^{item + 1}\s*\.', text):
                    return lines, page_of
                if not on and re.match(rf'^{item}\s*\.', text):
                    on, page_of = True, pno + 1
                if on:
                    lines.append(text.replace('\uf0b7', '•'))
    return lines, page_of


EN_WORDS = re.compile(r'\b(?:the|and|of|in|to|your|you|any|following|write|choose|answer|'
                      r'form|below|same|should|not|be|used|twice|questions?|ideas|plan|'
                      r'weekend|correct|order|both|four|six|eight|seven|nine|some|have|'
                      r'parts|details|personal|without|using|fill|is|are|going|for|a|an|'
                      r'with|this|line|begin|letter|dialogue|informal|writing|marks?)\b', re.I)


def english_sentences(year, level, item):
    """The paper's English instruction for a task, as whole printed sentences.

    Read off the page text of the task's pages, cut into sentences, and kept
    where a sentence is English and nothing else (an Irish or an Italian word
    in it means the converter welded two columns): every sentence kept is a
    run of words the page prints in that order.
    """
    lines, page = english_column(year, level, item)
    P = IP.ItPaper(year, level)
    with IP.pymupdf.open(P.path) as doc:
        text = ' '.join(doc[p - 1].get_text() for p in range(page, min(page + 2, doc.page_count + 1)))
    text = flat(IP._clean(text))
    m = re.search(rf'(?:^|\s){item}\s*\.\s', text)
    stop = re.search(rf'\s{item + 1}\s*\.\s', text[m.end():]) if m else None
    body = text[m.start():m.end() + (stop.start() if stop else len(text))] if m else text
    out = []
    for sent in re.split(r'(?<=[.?!:])\s+', body):
        sent = sent.strip()
        words = re.findall(r'[A-Za-zÀ-ÿ’\']+', sent)
        if not words:
            continue
        en = len(EN_WORDS.findall(sent))
        if IRISH.search(sent):
            continue
        if en >= max(2, len(words) * 0.3) or re.fullmatch(r'\(\d+ marks\)|\(max \d+ marks\)', sent):
            if not out or out[-1] != sent:
                out.append(sent)
    return out, page


def split_choice(lines):
    """{'a': lines, 'b': lines} for a task printed as "(a)" or "(b)"."""
    # The label may share its row with the task's first line ("(a) Avete
    # deciso …", 2015-2016): it is cut off onto a line of its own.
    if '(a)' not in lines or '(b)' not in lines:
        cut = []
        for l in lines:
            m = re.match(r'^\(([ab])\)\s+(\S.*)$', l)
            cut += ([f'({m.group(1)})', m.group(2)] if m else [l])
        lines = cut
    try:
        ia = lines.index('(a)')
        ib = lines.index('(b)')
    except ValueError:
        return None
    head = lines[:ia]
    return {'a': head + lines[ia:ib], 'b': head + lines[ib:]}


def source(year, level, page):
    return {'kind': 'source-text', 'label': 'SECTION C', 'title': 'Writing',
            'pages': [page],
            'attribution': (f'SEC Italian {year} {LEVEL_TITLE[level]} Level examination '
                            'paper — © State Examinations Commission.'),
            'presentationNote': 'The task as the examination paper prints it.'}


def rubric_card(year, level, item, letter, ref_letters, crit, reqs, text, page, total,
                topic=None, section='C', note='Use the descriptors in Appendix 2', pages=None):
    ref = f'{year} {level.upper()} Section {section} Q{item}'
    if ref_letters:
        ref += f'({ref_letters[0]})' + (f'–({ref_letters[-1]})' if len(ref_letters) > 1 else '')
    cid = f'it-{year}-{level}-{section.lower()}-{item}' + (f'-{letter}' if letter else '')
    assert sum(c['maxMarks'] for c in crit) == total, (ref, [c['maxMarks'] for c in crit], total)
    return {
        'id': cid, 'kind': 'rubric', 'subjectId': 'italian', 'level': LEVEL_WORD[level],
        'year': year, 'section': section, 'topicId': topic or TOPIC[(level, item)],
        'conceptId': re.sub(r'[^a-z0-9]+', '-', flat(text)[:60].lower()).strip('-')[:48],
        'questionRef': ref, 'questionText': text, 'totalMarks': total,
        'rubric': {'system': 'french', 'taskRequirements': reqs, 'criteria': crit,
                   'markingGuideNote': note},
        'schemePages': pages or [],
        'sourceMaterial': source(year, level, page),
    }


# ------------------------------------------------------------- Higher -----
def higher(year):
    S = Scheme(year, 'hl')
    c0 = S.at(r'^Section C WRITING')
    rule5 = flat(' '.join(S.span(r'^In C1 and C2 where', r'^In C3 where', c0)))
    rule7 = flat(' '.join(S.span(r'^In C3 where', r'^1\.\s*Composition', c0)))
    S.check(rule5, rule7)
    a2 = S.at(r'^APP?ENDIX 2')
    a2_end = S.at(r'^APPENDIX 3|^Italian Leaving', a2)
    cpages = sorted(set(S.pages(c0, S.at(r'^APPENDIX 1', c0) - 1)) | set(S.pages(a2, a2_end - 1)))
    # "Language (essays) out of 10" (2025-2026) or "Language (essays)" (2023-2024)
    lang10 = bands_from(S.span(r'^Language \(essays\)', r'^Language \(letter\)', a2,
                               include_start=False))
    lang15 = bands_from(S.span(r'^Language \(letter\)', r'^APPENDIX 3|^Italian Leaving', a2,
                               include_start=False))
    content_lines = S.span(r'^CONTENT AND COMMUNICATION DESCRIPTORS', r'^N\.B\.', a2,
                           include_start=False)
    c_essay = bands_from(content_lines, 0)
    c_letter = bands_from(content_lines, 1)
    out = []
    # C1: one card for the printed choice of prompts
    i1 = S.at(r'^1\.\s*Composition linked', c0)
    g1 = S.span(r'^Content and communication 15 marks', r'^Language 10 marks', i1)
    t1, p1 = paper_task(year, 'hl', 1)
    letters = [l for item, l, _t, _p in IP.ItPaper(year, 'hl').writing_asks() if item == 1 and l]
    out.append(rubric_card(year, 'hl', 1, 'a', letters, [
        criterion('content', 'Content and communication', 15, g1, c_essay),
        criterion('language', 'Language', 10, ['Use the descriptors in Appendix 2'], lang10,
                  lower_scale(5, rule5, 7))],
        [S.lines[i1], rule5], '\n'.join(join_lines(t1)), p1, 25, pages=cpages))
    # C2
    i2 = S.at(r'^2\.\s*Guided composition', c0)
    g2 = S.span(r'^Candidates must not', r'^3\.\s*Formal', i2)
    t2, p2 = paper_task(year, 'hl', 2)
    out.append(rubric_card(year, 'hl', 2, None, [], [
        criterion('content', 'Content and communication', 15, g2, c_essay),
        criterion('language', 'Language', 10, ['Use the descriptors in Appendix 2'], lang10,
                  lower_scale(5, rule5, 7))],
        [S.lines[i2], rule5], '\n'.join(join_lines(t2)), p2, 25, pages=cpages))
    # C3 (a) and (b)
    i3 = S.at(r'^3\.\s*Formal Writing', c0)
    i3_end = S.at(r'^APPENDIX 1', i3)
    if not any(re.match(r'^(?:Format 10 marks|Date 1 mark)', l) for l in S.lines[i3:i3_end]):
        # 2017 prints no format line at all (see c3_unpriced).
        out += c3_unpriced(S, year, i3, i3_end, rule7, cpages)
    else:
        try:
            fmt = S.span(r'^Date 1 mark', r'^Use the descriptors in Appendix 2', i3)
            general = S.span(r'Correct register', r'^. Format$|^● Format$|^• Format$', i3)
        except AssertionError:
            # 2023-2024 print no breakdown of the format marks: the criterion's
            # guidance is its own printed line.
            fmt = [S.lines[S.at(r'^Format 10 marks', i3)]]
            general = S.span(r'Correct register', r'^Format 10 marks', i3)
        t3, p3 = paper_task(year, 'hl', 3)
        for letter, nxt in (('a', r'^\(?b[.)]\s*The following'), ('b', r'^Points for the composition|^APPENDIX 1')):
            pts = S.span(rf'^\(?{letter}[.)]\s*The following points', nxt, i3)
            task = (split_choice(t3) or {}).get(letter)
            assert task, f'{year} HL C3: the task does not print "(a)" and "(b)" on lines of their own'
            out.append(rubric_card(year, 'hl', 3, letter, [letter], [
                criterion('format', 'Format', 10, fmt),
                criterion('content', 'Content and communication', 25, general + pts, c_letter),
                criterion('language', 'Language', 15, ['Use the descriptors in Appendix 2'], lang15,
                          lower_scale(7, rule7, 12))],
                [S.lines[i3], rule7], '\n'.join(join_lines(task)), p3, 50, pages=cpages))
    # B3 essays
    a1 = S.at(r'^APPENDIX 1')
    a1_end = S.at(r'^APP?ENDIX 2', a1)
    # The essay grid's bands start at 6 ("6 - 23 marks"), so they cannot be the
    # 0-60 placement scale; they are shown, verbatim, as its guidance.
    guide = [l for l in S.lines[S.at(r'^\(\d+\s*-\s*\d+\s*marks\)', a1):a1_end]
             if not re.fullmatch(r'_+', l)]
    P = IP.ItPaper(year, 'hl')
    b3 = S.at(r'^B\s*3\.?\s*Essay on prescribed text')
    for route, item, text, page in P.essay_asks():
        card = rubric_card(year, 'hl', item, None, [],
                           [criterion('essay', 'Essay', 60, guide)],
                           [S.lines[b3], 'Use the descriptors in Appendix 1'], text, page, 60,
                           topic=ESSAY_TOPIC, section=f'B3{route}',
                           note='Use the descriptors in Appendix 1', pages=S.pages(a1, a1_end - 1))
        card['id'] = f'it-{year}-hl-b3{route.lower()}-{item}'
        card['section'] = 'B'
        out.append(card)
    return out


def c3_unpriced(S, year, i3, i3_end, rule7, cpages):
    """Higher C3 where the scheme prices less than the task's printed marks.

    2017 heads the task "3. Formal Writing 50 marks" and prices only "Content
    and communication 25 marks" and "Language 15 marks"; the format line every
    neighbouring year prints ("Format 10 marks") is not there, and is never
    borrowed from another year. Ruling (coordinator, 19 Nov): the printed 50,
    self-assessed, with the scheme's printed lines as its criteria and both the
    head and the priced lines quoted.
    """
    def lines(a, b):
        return [re.sub(r'^[•●]\s*', '', l).strip() for l in S.span(a, b, i3)
                if l.strip() and not re.match(r'^(?:\d+|## Page \d+)$', l.strip())]
    head = S.lines[i3]
    content = S.lines[S.at(r'^Content and communication 25 marks', i3)]
    language = S.lines[S.at(r'^Language 15 marks', i3)]
    general = lines(r'Correct register', r'^Content and communication 25 marks')
    t3, p3 = paper_task(year, 'hl', 3)
    out = []
    for letter, nxt in (('a', r'^\(?b[.)]\s*The following'), ('b', r'^APPENDIX 1')):
        # the points, without their "(a) The following points to be covered" head
        pts = lines(rf'^\(?{letter}[.)]\s*The following points', nxt)[1:]
        task = (split_choice(t3) or {}).get(letter)
        assert task and pts, f'{year} HL C3({letter}): task or points not read'
        texts = general + [content, language] + pts
        S.check(head, rule7, *texts)
        rows = [{'id': f'r-{k}', 'kind': 'criterion', 'verbatim': t, 'marks': None}
                for k, t in enumerate(texts, start=1)]
        rows[0]['contextNote'] = (
            f'The scheme heads this task "{head}" and prices "{content}" and "{language}", '
            '40 of the 50 marks; it prints no line for the other 10, so judge your letter '
            f'against the total. It also prints: "{rule7}"')
        text = '\n'.join(join_lines(task))
        out.append({
            'id': f'it-{year}-hl-c-3-{letter}', 'subjectId': 'italian', 'level': 'higher',
            'year': year, 'section': 'C', 'topicId': TOPIC[('hl', 3)],
            'conceptId': re.sub(r'[^a-z0-9]+', '-', flat(text)[:60].lower()).strip('-')[:48],
            'questionRef': f'{year} HL Section C Q3({letter})', 'questionText': text,
            'tariffModel': {'kind': 'questionTotal'}, 'totalMarks': 50, 'rows': rows,
            'notes': f'The scheme prices this task on pages {", ".join(map(str, cpages))}.',
            'sourceMaterial': source(year, 'hl', p3),
        })
    return out


# Where the scheme's order task does not match the paper's, said on the card
# (the first row's contextNote), never corrected: 2026 Ordinary's scheme heads
# Question 3 "Francesca has a very busy weekend ahead" (the 2025 title) and
# names Anna in its lines; the paper sets Leo's weekend.
ORDER_MISMATCH = {
    2026: (' The scheme heads this question "Francesca has a very busy weekend ahead" '
           'and names Anna in its lines, where the paper names Leo: the lines are shown '
           'as the scheme prints them.'),
}


# ------------------------------------------------------------- Ordinary ---
def ordinary(year):
    S = Scheme(year, 'ol')
    c0 = S.at(r'^Section C Writing')
    opages = S.pages(c0, S.at(r'^APPENDIX 1', c0) - 1)
    out = []
    # The Ordinary writing pages set Irish, English and the Italian task in a
    # layout a row reader welds; the card carries the paper's English
    # instruction and the page itself (its source) shows the task as printed.
    t1, p1 = english_sentences(year, 'ol', 1)
    if not t1:
        # 2019 and earlier print the choice with no full stop ("1. Informal
        # Writing (30 marks) / Choose (a) Informal Letter / or / (b) Dialogue"):
        # the English column's head, up to where the first option's own task
        # begins (its second "(a)").
        col, p1 = english_column(year, 'ol', 1)
        seen = [k for k, l in enumerate(col) if l.startswith('(a)')]
        t1 = col[:seen[1]] if len(seen) > 1 else col[:4]
    head = join_lines(t1)
    choice = {'a': head, 'b': head}
    for letter, head, stop in (('a', r'^\(a\)\s*E-mail/Letter', r'^OR$'),
                               ('b', r'^\(b\)\s*Dialogue', r'^Question 2 FORM')):
        i = S.at(head, c0)
        block = S.span(head, stop, c0)
        fmt_end = next(k for k, l in enumerate(block) if re.search(r'7 marks \(2\+2\+2\+1\)', l))
        fmt = block[1:fmt_end + 1]
        ci = next(k for k, l in enumerate(block) if l.startswith('Content and communication'))
        li = next(k for k, l in enumerate(block) if l.startswith('Language'))
        content = block[ci:li]
        lang = block[li + 1:]
        rule_at = next(k for k, l in enumerate(lang) if l.startswith('Where marks for content'))
        rule = flat(' '.join(lang[rule_at:rule_at + 2]))
        S.check(rule)
        bands = bands_from(lang[:rule_at])
        task = choice.get(letter)
        assert task, f'{year} OL C1: no "({letter})" on a line of its own'
        out.append(rubric_card(year, 'ol', 1, letter, [letter], [
            criterion('format', fmt[0] if len(fmt) == 1 else 'Format', 7, fmt),
            criterion('content', 'Content and communication', 16, content),
            criterion('language', re.sub(r'\s+7 marks$', '', block[li].split(':')[0].replace(' 7 marks (2+2+2+1)', '')),
                      7, [block[li]], bands, lower_scale(0, rule, 7))],
            [S.lines[S.at(r'^Question 1 30 marks', c0)], block[0], rule], '\n'.join(join_lines(task)), p1, 30,
            note=S.lines[S.at(r'^Question 1 30 marks', c0)], pages=opages))
    # C2 form-filling: two boxes, each priced by its best N answers
    i2 = S.at(r'^Question 2 FORM-FILLING', c0)
    # It ends where Question 3 begins: "3. <title>" or "Question 3" (2019,
    # 2022), never inside Question 3's own numbered lines.
    q2 = S.span(r'^Question 2 FORM-FILLING', r'^(?:3\.\s|Question 3\b)', c0)
    ia = next((k for k, l in enumerate(q2) if l.startswith('Box A')), None)
    t2, p2 = english_sentences(year, 'ol', 2)
    # The task's opening sentence ("You are going to volunteer in an animal
    # shelter.", 2022), broken by its Irish twin in the page's running text,
    # is taken from the English column where the sentences above lost it.
    col2, _p = english_column(year, 'ol', 2)
    w = next((k for k, l in enumerate(col2) if l.startswith('Without using')), None)
    if w:
        head2 = re.sub(r'^2\s*\.\s*', '', flat(' '.join(col2[:w])))
        if head2 and head2 not in flat(' '.join(t2)):
            t2 = [head2] + t2
    if ia is not None:
        ib = next(k for k, l in enumerate(q2) if l.startswith('Box B'))
        out.append(rubric_card(year, 'ol', 2, None, [], [
            criterion('box-a', 'Box A', 8, q2[ia:ib]),
            criterion('box-b', 'Box B', 14, q2[ib:])],
            q2[:ia], '\n'.join(join_lines(t2)), p2, 22, note=q2[0], pages=opages))
    else:
        # 2019 and earlier price each field of the form on its own line
        # ("Nazionalità 2 marks", "Qualità 4 marks (2+2)"): one criterion per
        # printed field, labelled with the field's name as printed.
        crit, first = [], None
        for k, l in enumerate(q2[1:], 1):
            m = re.match(r'^(.+?)\s+(\d+)\s+marks?\b', l)
            if not m:
                continue
            first = k if first is None else first
            cid = 'field-' + re.sub(r'[^a-z0-9]+', '-', m.group(1).lower()).strip('-')
            crit.append(criterion(cid, m.group(1), int(m.group(2)), [l]))
        assert crit and len({c['id'] for c in crit}) == len(crit), f'{year} OL C2: fields'
        out.append(rubric_card(year, 'ol', 2, None, [], crit, q2[:first],
                               '\n'.join(join_lines(t2)), p2, 22, note=q2[0], pages=opages))
    # C3 the sequence: eight lines in the printed order, one mark each
    # Its head is "3. Francesca has a very busy weekend ahead (8x1 mark)"
    # (2025-2026), "3. Andrea's school schedule 8 marks" over "(8x1 mark)"
    # (2021) or "Question 3" over the title (2022): the eight lines follow.
    q3 = S.span(r'^(?:Question 3\b|3\.\s)', r'^APPENDIX 1', S.at(r'^Question 2 FORM', c0))
    rows, cur = [], None
    # An examiner's instruction printed in capitals in brackets under the
    # lines (2016: "(IF THE LAST PIECE OF THE SEQUENCE IS IN THE EIGHT SPOT
    # AWARD THE MARK)") is quoted on the card, never read as part of a line.
    caps, in_caps = [], False
    for l in q3[1:]:
        if in_caps or re.match(r"^\([A-Z][A-Z ,'’-]{8,}", l):
            caps.append(l)
            in_caps = not l.rstrip().endswith(')')
            continue
        # 2016 prints its first line "1 Mi alzo …" with no stop after the 1.
        m = re.match(r'^(\d)\.\s*(.*)$', l) or (not rows and re.match(r'^(1)\s+(\S.*)$', l))
        if m:
            cur = [int(m.group(1)), m.group(2)]
            rows.append(cur)
        elif cur and not re.match(r'^\(?\d+x\d', l):
            cur[1] = f'{cur[1]} {l}'
    if not rows:
        # 2017 and earlier print the eight lines unnumbered, one to a line,
        # under the head: the order is the order printed.
        body = [l for l in q3[1:] if l.strip() and not re.match(r'^(?:\d+|## Page \d+|\(?\d+x\d.*)$', l.strip())]
        rows = [[k + 1, l.strip()] for k, l in enumerate(body)]
    assert [r[0] for r in rows] == list(range(1, 9)), (year, [r[0] for r in rows])
    for _n, t in rows:
        S.check(t)
    if caps:
        S.check(' '.join(caps))
    # The eight sentences to order are set in two columns on the page, which a
    # row reader welds together; the card carries the paper's English
    # instruction - the English column, read word by word, from the question's
    # head to "… in the correct order." - and the page itself (its source)
    # shows the line to begin with and the eight sentences as printed. Read
    # off the page's running text instead, a sentence broken by its Irish
    # twin beside it was dropped ("She writes in her diary, but the details
    # got mixed up.", 2025).
    col, p3 = english_column(year, 'ol', 3)
    # A head with "(8 marks)" on the line beneath it is a title ("3. Daily
    # routine"), its own line; one that runs on ("3. A new Italian restaurant
    # is opening in" / "Killarney. (8 marks)") is the first sentence.
    title = (len(col) > 1 and col[1].strip() == '(8 marks)') or col[0].rstrip().endswith('(8 marks)')
    col = [re.sub(r'\s*\(8 marks\)\s*', ' ', re.sub(r'^3\s*\.\s*', '', l)).strip() for l in col]
    col = [l for l in col if l]
    t3 = ([col[0]] + join_lines(col[1:])) if title else join_lines(col)
    order = next((k for k, l in enumerate(t3) if re.search(r'in the correct order\.\s*$', l)), None)
    assert order is not None, f'{year} OL C3: no "in the correct order." line'
    t3 = t3[:order + 1]
    out.append({
        'id': f'it-{year}-ol-c-3', 'subjectId': 'italian', 'level': 'ordinary', 'year': year,
        'section': 'C', 'topicId': TOPIC[('ol', 3)],
        'conceptId': re.sub(r'[^a-z0-9]+', '-', flat(' '.join(t3))[:60].lower()).strip('-')[:48],
        'questionRef': f'{year} OL Section C Q3', 'questionText': '\n'.join(t3),
        'tariffModel': {'kind': 'fixed'}, 'totalMarks': 8,
        # One menu row of the eight printed lines, a mark for each in its place
        # ("8x1 mark"): a fixed card shows at most six rows.
        'rows': [{'id': 'r-1', 'kind': 'anyN',
                  'verbatim': 'The answers the scheme accepts in full', 'marks': None,
                  'group': {'claimMax': 8, 'perOption': 1,
                            'options': [f'{n}. {flat(t)}' for n, t in rows]}}],
        'notes': f'The scheme prices the sequence "{q3[0]}": one mark for each line in its place.',
        'sourceMaterial': dict(source(year, 'ol', p3), presentationNote=(
            'The task as the examination paper prints it, with the eight sentences '
            'to put in order.')),
    })
    out[-1]['rows'][0]['contextNote'] = ('The scheme prints the order line by line; each line '
                                         'in its place is one mark.' + ORDER_MISMATCH.get(year, '')
                                         + (f' The scheme adds: "{flat(" ".join(caps))}".' if caps else ''))
    return out


def main():
    import json
    year, level = int(sys.argv[1]), sys.argv[2]
    cards = higher(year) if level == 'hl' else ordinary(year)
    print(json.dumps(cards, ensure_ascii=False, indent=1)[:6000])
    print(len(cards), 'cards')


if __name__ == '__main__':
    main()
