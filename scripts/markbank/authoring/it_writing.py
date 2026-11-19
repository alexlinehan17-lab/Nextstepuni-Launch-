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
    # The scheme's lower language scale prints a rule and no bands of its own,
    # so the rule is shown in the card's task requirements, never as a scale.
    return c


def lower_scale(maxm, rule, at_most):
    return {'label': f'Language out of {maxm}', 'maxMarks': maxm,
            'permittedMarks': list(range(maxm + 1)), 'bands': [],
            'contentCriteria': ['content'], 'contentAtMost': at_most, 'rule': rule}


# ------------------------------------------------------------- the paper ---
IRISH = re.compile(r'\b(?:agus|na|an|ar|do|le|go|nó|Freagair|Scr[íi]obh|Roghnaigh|Aiste|'
                   r'marc|Scr[íi]bhneoireacht|l[ée]amhthuiscint|sliocht|faoi|Threoir|'
                   r'Fhoirmi[úu]il|Litir|Comhr[áa]|Neamhfhoirmi[úu]il|ceist|cheist|D[ée]an|s[íi]os)\b', re.I)
PAGE_FURNITURE = re.compile(r'^(?:Leaving Certificate|Italian\s*[—–-]|Iod[áa]ilis\s*[—–-]|Scr[úu]d[úu]'
                            r'|Lch\s+\d|Page\s+\d|\d{1,3}$|_+$)', re.I)


def paper_task(year, level, item):
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
                if side != 'R':
                    welded = [m.start(1) for m in re.finditer(rf'(?:^|\s)({item}\s*\.\s+[A-Z])', s)]
                    if welded and welded[-1] > 0:
                        tail = s[welded[-1]:]
                        cut = IRISH.search(tail, 3)
                        lines.append(tail[:cut.start()].strip() if cut else tail)
                        continue
                    it = len(ITALIAN_WORDS.findall(s))
                    marked = bool(re.match(r'^(?:\([a-e]\)|•)', s))
                    irish = bool(IRISH.search(s)) and it < 2
                    if irish or not (it or marked):
                        continue
                if not lines or lines[-1] != s:
                    lines.append(s)
    return lines, page_of


def split_choice(lines):
    """{'a': lines, 'b': lines} for a task printed as "(a)" or "(b)"."""
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
    lang10 = bands_from(S.span(r'^Language \(essays\) out of 10', r'^Language \(letter\)', a2,
                               include_start=False))
    lang15 = bands_from(S.span(r'^Language \(letter\) out of 15', r'^APPENDIX 3|^Italian Leaving', a2,
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
        [S.lines[i1], rule5], '\n'.join(t1), p1, 25, pages=cpages))
    # C2
    i2 = S.at(r'^2\.\s*Guided composition', c0)
    g2 = S.span(r'^Candidates must not', r'^3\.\s*Formal', i2)
    t2, p2 = paper_task(year, 'hl', 2)
    out.append(rubric_card(year, 'hl', 2, None, [], [
        criterion('content', 'Content and communication', 15, g2, c_essay),
        criterion('language', 'Language', 10, ['Use the descriptors in Appendix 2'], lang10,
                  lower_scale(5, rule5, 7))],
        [S.lines[i2], rule5], '\n'.join(t2), p2, 25, pages=cpages))
    # C3 (a) and (b)
    i3 = S.at(r'^3\.\s*Formal Writing', c0)
    fmt = S.span(r'^Date 1 mark', r'^Use the descriptors in Appendix 2', i3)
    general = S.span(r'Correct register', r'^. Format$|^● Format$|^• Format$', i3)
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
            [S.lines[i3], rule7], '\n'.join(task), p3, 50, pages=cpages))
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


# ------------------------------------------------------------- Ordinary ---
def ordinary(year):
    S = Scheme(year, 'ol')
    c0 = S.at(r'^Section C Writing')
    opages = S.pages(c0, S.at(r'^APPENDIX 1', c0) - 1)
    out = []
    t1, p1 = paper_task(year, 'ol', 1)
    choice = split_choice(t1) or {}
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
            criterion('language', block[li].split(':')[0].replace(' 7 marks (2+2+2+1)', ''),
                      7, [block[li]], bands, lower_scale(0, rule, 7))],
            [S.lines[S.at(r'^Question 1 30 marks', c0)], block[0], rule], '\n'.join(task), p1, 30,
            note=S.lines[S.at(r'^Question 1 30 marks', c0)], pages=opages))
    # C2 form-filling: two boxes, each priced by its best N answers
    i2 = S.at(r'^Question 2 FORM-FILLING', c0)
    q2 = S.span(r'^Question 2 FORM-FILLING', r'^3\.\s', c0)
    ia = next(k for k, l in enumerate(q2) if l.startswith('Box A'))
    ib = next(k for k, l in enumerate(q2) if l.startswith('Box B'))
    t2, p2 = paper_task(year, 'ol', 2)
    out.append(rubric_card(year, 'ol', 2, None, [], [
        criterion('box-a', 'Box A', 8, q2[ia:ib]),
        criterion('box-b', 'Box B', 14, q2[ib:])],
        q2[:ia], '\n'.join(t2), p2, 22, note=q2[0], pages=opages))
    # C3 the sequence: eight lines in the printed order, one mark each
    q3 = S.span(r'^3\.\s.*\(8x1 mark', r'^APPENDIX 1', c0)
    rows, cur = [], None
    for l in q3[1:]:
        m = re.match(r'^(\d)\.\s*(.*)$', l)
        if m:
            cur = [int(m.group(1)), m.group(2)]
            rows.append(cur)
        elif cur:
            cur[1] = f'{cur[1]} {l}'
    assert [r[0] for r in rows] == list(range(1, 9)), (year, [r[0] for r in rows])
    for _n, t in rows:
        S.check(t)
    t3, p3 = paper_task(year, 'ol', 3)
    out.append({
        'id': f'it-{year}-ol-c-3', 'subjectId': 'italian', 'level': 'ordinary', 'year': year,
        'section': 'C', 'topicId': TOPIC[('ol', 3)],
        'conceptId': re.sub(r'[^a-z0-9]+', '-', flat(' '.join(t3))[:60].lower()).strip('-')[:48],
        'questionRef': f'{year} OL Section C Q3', 'questionText': '\n'.join(t3),
        'tariffModel': {'kind': 'fixed'}, 'totalMarks': 8,
        'rows': [{'id': f'r-{n}', 'kind': 'point', 'verbatim': f'{n}. {flat(t)}', 'marks': 1}
                 for n, t in rows],
        'notes': f'The scheme prices the sequence "{q3[0]}": one mark for each line in its place.',
        'sourceMaterial': source(year, 'ol', p3),
    })
    out[-1]['rows'][0]['contextNote'] = ('The scheme prints the order line by line; each line '
                                         'in its place is one mark.')
    return out


def main():
    import json
    year, level = int(sys.argv[1]), sys.argv[2]
    cards = higher(year) if level == 'hl' else ordinary(year)
    print(json.dumps(cards, ensure_ascii=False, indent=1)[:6000])
    print(len(cards), 'cards')


if __name__ == '__main__':
    main()
