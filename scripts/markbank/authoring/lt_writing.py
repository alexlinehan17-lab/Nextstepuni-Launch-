#!/usr/bin/env python3
"""The Lithuanian written tasks (Section B, 2023 on) as rubric cards on the
French grid shape, as Portuguese's are (pt_writing.py). Lithuanian only; the
languages-q3 lane adds them beside the 306 live cards (lt_q3_batch.py).

    python3 scripts/markbank/authoring/lt_writing.py 2026 hl

Every marking string is lifted from the scheme's .md above the column-runs
appendix (criterion heads, band names, descriptors, the communication lines),
and each band's marks are the range the scheme prints in the band. The task is
the paper's own text (lt_paper). The only words that are the app's are
practiceNotes. The shapes, ruled by the coordinator (Lithuanian stage 1, R2):

  Higher, Q3-Q5: one MARKING GRID, "Content and Communication" and
      "Language", bands TOP / MIDDLE / BOTTOM, two columns of ranges ("Q. 3
      and 4" at 15, "Q. 5" at 10): the k-th range in a band's lines is column
      k ("form 3", two trailing pairs).
  Ordinary, Q4: "4 Communicative tasks @ 4 marks each = 16 marks", scored
      per task where the option prints exactly four bullets ("Communication ·
      task N", 0-4, the two printed categories as bands), else one criterion
      on 16; and "Language: 14 marks" in three bands.
  Ordinary, Q5: the two lines the scheme prints, "First 3 tasks @ 2 marks
      each = 6 marks." (0-6) and "4 Communicative tasks @ 3 marks each = 12
      marks." (0-12), and "Language: 12 marks" in three bands.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

import lt_all  # noqa: E402
from lt_paper import LtPaper  # noqa: E402

SUBJECT = 'lithuanian'
SCHEMES = os.path.join(ROOT, 'examiner-reports', 'lithuanian', 'schemes')
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}
RANGE = re.compile(r'(?<![\d.])(\d{1,2})\s*[–‐-]\s*(\d{1,2})(?![\d.])')
BULLET = re.compile(r'^\s*[•]\s*')
BANDS = ('TOP', 'MIDDLE', 'BOTTOM')
PRACTICE = ('Write your answer in Lithuanian, then place it on the published grid: '
            'content and communication first, then language.')


class Refused(Exception):
    pass


def _norm(t):
    return re.sub(r'\s+', ' ', str(t)).strip()


class Scheme:
    """The scheme's own pages (above the column-runs appendix), each line with
    the page it is printed on."""
    def __init__(self, year, level):
        with open(os.path.join(SCHEMES, f'{year}-{level}.md'), encoding='utf-8') as fh:
            body = fh.read().split('<!-- markbank:column-runs -->')[0].split('\n')
        self.lines, self.pages, page, skip = [], [], 1, False
        for l in body:
            m = re.match(r'^## Page (\d+)', l)
            if m:
                page = int(m.group(1))
                skip = False
                continue
            if l.startswith('<!-- columns'):
                skip = True          # an extraction's columns block: until the next page
                continue
            if skip:
                continue
            self.lines.append(_norm(l))
            self.pages.append(page)

    def find(self, pattern, start=0, stop=None):
        rx = re.compile(pattern)
        for i in range(start, len(self.lines) if stop is None else stop):
            if rx.search(self.lines[i]):
                return i
        raise Refused(f'no scheme line matches {pattern!r} after line {start}')


def _band(S, name_i, end_i, col):
    """A band: its printed name, the descriptors under it, the col-th range."""
    lines = [l for l in S.lines[name_i + 1:end_i] if l and not re.fullmatch(r'\d{1,2}', l)]
    ranges = [m for l in lines for m in RANGE.finditer(l)]
    if len(ranges) <= col:
        raise Refused(f'band {S.lines[name_i]!r} prints no range #{col}')
    lo, hi = int(ranges[col].group(1)), int(ranges[col].group(2))
    guidance = []
    for l in lines:
        text = _norm(RANGE.sub(' ', l))
        if not text:
            continue
        if BULLET.match(text) or not guidance:
            guidance.append(BULLET.sub('', text))
        else:
            guidance[-1] = f'{guidance[-1]} {text}'
    return {'label': S.lines[name_i], 'marks': list(range(lo, hi + 1)), 'guidance': guidance}


def _banded(S, cid, label, head_i, stop_i, col):
    names = [S.find(rf'^{b}$', head_i, stop_i) for b in BANDS]
    bands = [_band(S, n, e, col) for n, e in zip(names, names[1:] + [stop_i])]
    top = max(m for b in bands for m in b['marks'])
    marks = sorted(m for b in bands for m in b['marks'])
    if marks != list(range(top + 1)):
        raise Refused(f'{label}: bands {[b["marks"] for b in bands]} do not cover 0 to {top} once')
    return {'id': cid, 'label': label, 'maxMarks': top, 'permittedMarks': list(range(top + 1)),
            'guidance': [], 'bands': bands}, names[0]


def _block_end(S, start):
    """The line after a band block: the next criterion head or task head."""
    for i in range(start, len(S.lines)):
        l = S.lines[i]
        if re.match(r'^(Q\. ?3 and 4|Language\b|Content and Communication|Communication:|Penkta užduotis|'
                    r'Listening Comprehension|APPENDIX|Section [A-E] \()', l):
            return i
    return len(S.lines)


def higher_grid(S, q):
    """Q3/Q4 read column 0 (15), Q5 column 1 (10)."""
    col = 0 if q in (3, 4) else 1
    g = S.find(r'^MARKING GRID$')
    cc = S.find(r'^Content and Communication', g)
    cc_top = S.find(r'^TOP$', cc)
    lang = S.find(r'^(Q\. ?3 and 4 Q\. ?5|Language)', cc_top + 1)
    if S.lines[lang].startswith('Q.'):
        lang = S.find(r'^Language', lang)
    content, _ = _banded(S, 'content', 'Content and Communication', cc, _block_end(S, S.find(r'^BOTTOM$', cc) + 1), col)
    lang_top = S.find(r'^TOP$', lang)
    language, _ = _banded(S, 'language', 'Language', lang, _block_end(S, S.find(r'^BOTTOM$', lang_top) + 1), col)
    heads = ' '.join(S.lines[g:cc_top])
    printed = [int(x) for x in re.findall(r'(\d+) marks', heads)]
    want = (15, 10)[col]
    if printed[:2] != [15, 10] or content['maxMarks'] != want or language['maxMarks'] != want:
        raise Refused(f'Q{q}: grid heads {printed}, bands {content["maxMarks"]}/{language["maxMarks"]}, want {want}')
    pages = sorted({S.pages[i] for i in range(g, _block_end(S, S.find(r'^BOTTOM$', lang_top) + 1))})
    return [content, language], [], pages


def _option_bullets(S, task_i, letter, stop_i):
    """The option's bullets as the scheme reprints them, or None where the
    scheme does not reprint the option (2023 Ordinary Q5 (b), (c))."""
    try:
        a = S.find(rf'^\({letter}\)\s', task_i, stop_i)
    except Refused:
        return None
    out = []
    for l in S.lines[a + 1:stop_i]:
        if re.match(r'^\([a-c]\)\s', l) or l.startswith('Communication'):
            break
        if BULLET.match(l):
            out.append(BULLET.sub('', l))
        elif out:
            out[-1] = f'{out[-1]} {l}'
    return out


def ordinary_grid(S, q, letter, paper_bullets):
    task = S.find(r'^Ketvirta užduotis' if q == 4 else r'^Penkta užduotis')
    comm = S.find(r'^Communication: ', task)
    lang_head = S.find(r'^Language: \d+ marks', comm)
    nb = S.find(r'^N\.B\. ', comm, lang_head)
    nb_text = _norm(' '.join(S.lines[nb:lang_head]))
    lang_top = S.find(r'^TOP$', lang_head)
    language, _ = _banded(S, 'language', 'Language', lang_head, _block_end(S, S.find(r'^BOTTOM$', lang_top) + 1), 0)
    printed_lang = int(re.search(r'Language: (\d+) marks', S.lines[lang_head]).group(1))
    if language['maxMarks'] != printed_lang:
        raise Refused(f'Q{q}: Language bands reach {language["maxMarks"]}, the head prints {printed_lang}')
    cats = [S.lines[i] for i in range(comm, nb) if S.lines[i].startswith(('1st Category', '2nd Category'))]
    def cat_bands(top):
        bands = []
        for c in cats:
            m = re.match(r'^(\d(?:st|nd) Category)\s+(\d)\s*[–‐-]\s*(\d)\s+(.+)$', c)
            if not m:
                raise Refused(f'unreadable category line {c!r}')
            bands.append({'label': m.group(1), 'marks': list(range(int(m.group(2)), int(m.group(3)) + 1)),
                          'guidance': [m.group(4)]})
        bands.sort(key=lambda b: -b['marks'][0])
        if sorted(m for b in bands for m in b['marks']) != list(range(top + 1)):
            raise Refused(f'categories {[b["marks"] for b in bands]} do not cover 0 to {top}')
        return bands
    per_task = [i for i in range(comm, nb) if S.lines[i] == '4 Communicative tasks @ 4 marks each = 16 marks.']
    if per_task:
        line = S.lines[per_task[0]]
        reprint = _option_bullets(S, task, letter, comm)
        if len(paper_bullets) == 4:
            # R2: scored per task where the option prints exactly four bullets,
            # on the French per-point shape (French "Communication · point N"):
            # the label is the app's, so the criterion carries no bands, and
            # its guidance quotes the scheme: its reprint of the bullet where
            # it prints one, the line pricing the tasks, and the two
            # categories as printed. cat_bands() holds the categories to
            # covering 0-4 once.
            cat_bands(4)
            comm_crits = [{'id': f'communication-{i}', 'label': f'Communication · task {i}', 'maxMarks': 4,
                           'permittedMarks': list(range(5)),
                           'guidance': ([reprint[i - 1]] if reprint else []) + [line] + cats}
                          for i in range(1, 5)]
        else:
            comm_crits = [{'id': 'communication', 'label': 'Communication', 'maxMarks': 16,
                           'permittedMarks': list(range(17)), 'guidance': [line] + cats}]
    else:
        first = S.lines[S.find(r'^First 3 tasks @ 2 marks each = 6 marks\.$', comm, nb)]
        four = S.lines[S.find(r'^4 Communicative tasks @ 3 marks each = 12 marks\.$', comm, nb)]
        comm_crits = [{'id': 'communication-first', 'label': first, 'maxMarks': 6,
                       'permittedMarks': list(range(7)), 'guidance': []},
                      {'id': 'communication-tasks', 'label': four, 'maxMarks': 12,
                       'permittedMarks': list(range(13)), 'guidance': cats}]
    head = S.lines[comm]
    printed_comm = int(re.search(r'Communication: (\d+) marks', head).group(1))
    if sum(c['maxMarks'] for c in comm_crits) != printed_comm:
        raise Refused(f'Q{q}: communication criteria sum to {sum(c["maxMarks"] for c in comm_crits)}, the head '
                      f'prints {printed_comm}')
    pages = sorted({S.pages[i] for i in range(comm, _block_end(S, S.find(r'^BOTTOM$', lang_top) + 1))})
    return comm_crits + [language], [nb_text], pages


def _paper_bullets(P, ask, want):
    """An option's bullets as the paper prints them, where the reader dropped
    them: some options set their bullets in a symbol font (U+F0B7). Read from
    the page's own text after the option's heading, up to the next option or
    the page's furniture, and held to the scheme's reprint of the same bullets."""
    import fitz
    page = _norm(fitz.open(P.path)[ask.page - 1].get_text())
    head = _norm(ask.text)
    k = page.find(head)
    if k < 0:
        raise Refused(f'{ask.key}: heading {head!r} not on paper page {ask.page}')
    rest = re.split(r'\sARBA\s|\s\([a-c]\)\s|\sDalis B\s', page[k + len(head):])[0]
    # the page's photo credits ("Nuotraukos iš www…", "Pixabay.com 15min.lt") are furniture
    rest = re.split(r'\sNuotraukos iš\s|\s(?=\S+\.(?:com|lt|net|org)\b)', ' ' + rest + ' ')[0]
    got = [_norm(b) for b in re.split('[\uf0b7•]', rest) if _norm(b)]
    # each paper bullet is the scheme's reprint of it, and the last may carry
    # the paper's own word count after it ("(apie 100 žodžių)")
    ok = len(got) == len(want) and all(
        g == w or (i == len(got) - 1 and re.fullmatch(re.escape(w) + r'\s*\(apie \d+ žodžių\)', g))
        for i, (g, w) in enumerate(zip(got, want)))
    if not ok:
        raise Refused(f'{ask.key}: paper bullets {got} are not the scheme\'s {want}')
    return got


def _task_pages(P, ask):
    """The paper pages an option is printed on: from its own page to where
    the next option begins (that page too, if the option runs onto it above
    the next "ARBA"), or for the last option, to the last page before the
    optional additional pages."""
    import fitz
    doc = fitz.open(P.path)
    def text(p):
        t = _norm(doc[p - 1].get_text())
        # the running head: "… 2026 16 Lithuanian – Ordinary Level" or "… 2026 Lithuanian – Higher Level 16"
        return re.sub(r'^Leaving Certificate Examination \d{4}(?: \d+)? Lithuanian – (?:Higher|Ordinary) Level(?: \d+)?\s*',
                      '', t)
    opts = sorted((a for a in P.all_asks() if a.section == 'B' and a.q == ask.q), key=lambda a: a.letter)
    nxt = next((a for a in opts if a.letter > ask.letter), None)
    if nxt is not None:
        if nxt.page == ask.page:
            return [ask.page]
        before = text(nxt.page).split(f'({nxt.letter})')[0]
        end = nxt.page if _norm(re.sub(r'\bARBA\b', '', before)) else nxt.page - 1
    else:
        end = ask.page
        while end + 1 <= len(doc) and text(end + 1) and not text(end + 1).startswith(
                ('Optional additional page', 'Copyright notice', 'Listening')):
            if ask.q != 5:
                break
            end += 1
    return list(range(ask.page, end + 1))


def _instruction(P, q):
    """The task's own instruction as the paper prints it between its title
    and option (a): "Atsakykite į (a) arba (b), arba (c). Parašykite apie 150
    žodžių." Empty where the paper prints none there."""
    import fitz
    first = min((a for a in P.all_asks() if a.section == 'B' and a.q == q), key=lambda a: a.letter)
    doc = fitz.open(P.path)
    for p in range(max(1, first.page - 1), first.page + 1):
        t = _norm(doc[p - 1].get_text())
        # through the instruction's own "(a) arba (b), arba (c)" to option (a)
        m = re.search(r'\w+ užduotis \(\d+ taškų\)\s*(.*?\(c\)\.?.*?)\s*\(a\)\s', t)
        if m:
            return _norm(m.group(1))
    return ''


def writing_cards(year, level):
    P = LtPaper(year, level, SUBJECT)
    S = Scheme(year, level)
    out, refused = [], []
    for ask in P.all_asks():
        if ask.section != 'B':
            continue
        key = ask.key
        try:
            question = _norm(ask.full_text)
            if level == 'ol':
                head = S.find(r'^Ketvirta užduotis' if ask.q == 4 else r'^Penkta užduotis')
                want = _option_bullets(S, head, ask.letter, S.find(r'^Communication: ', head))
                if want and question.count('•') != len(want):
                    question = _norm(question + ' ' + ' '.join(f'• {b}' for b in _paper_bullets(P, ask, want)))
                if '•' not in question:
                    # a form or a dialogue to fill: the reader carries on into the
                    # form's first label ("Jūsų vardas, pavardė"), which the page
                    # shows; the question is the instruction, to its last sentence
                    m = re.match(r'^(.*[.?!])\s+[^.?!()•]+$', question)
                    if m:
                        question = m.group(1)
            paper_bullets = [b for b in question.split('•')[1:]]
            if level == 'hl':
                criteria, reqs, pages = higher_grid(S, ask.q)
            else:
                criteria, reqs, pages = ordinary_grid(S, ask.q, ask.letter, paper_bullets)
            src_pages = _task_pages(P, ask)
        except Refused as e:
            refused.append((key, str(e)))
            continue
        lead = P.lead('B', ask.q)
        card = {
            'id': lt_all.card_id(SUBJECT, year, level, key),
            'kind': 'rubric',
            'subjectId': SUBJECT,
            'level': lt_all.LEVEL_WORD[level],
            'year': year,
            'section': 'B',
            'topicId': lt_all.topic_for(SUBJECT, year, 'B', ask.q),
            'conceptId': lt_all.concept_for(question),
            'questionRef': lt_all.question_ref(year, level, key),
            'questionText': question,
            'stem': _instruction(P, ask.q) or _norm(lead),
            'totalMarks': sum(c['maxMarks'] for c in criteria),
            'rubric': {
                'system': 'french',
                'taskRequirements': reqs,
                'criteria': criteria,
                'markingGuideNote': '',
                'practiceNotes': [PRACTICE],
            },
            'schemePages': pages,
            'sourceMaterial': {
                'kind': 'source-text',
                'label': _norm(lead).upper() if lead else f'QUESTION {ask.q}',
                'title': f'{_norm(lead) if lead else f"Question {ask.q}"} ({ask.letter}) — answer in Lithuanian',
                'pages': src_pages,
                'attribution': (f'SEC Lithuanian {year} {LEVEL_TITLE[level]} Level examination paper — '
                                f'© State Examinations Commission.'),
                'presentationNote': 'The task exactly as the examination printed it.',
            },
        }
        out.append(card)
    return out, refused


def main():
    year, level = int(sys.argv[1]), sys.argv[2]
    cards, refused = writing_cards(year, level)
    for c in cards:
        crit = c['rubric']['criteria']
        print(c['id'], c['totalMarks'], '|', c.get('stem', '')[:30], '|', c['questionText'][:100])
        print('      ', [(k['label'][:34], k['maxMarks'], [b['label'] + str(b['marks'][0]) + '-' + str(b['marks'][-1])
                                                          for b in k.get('bands', [])]) for k in crit])
        print('       pages', c['schemePages'], '| req', [r[:60] for r in c['rubric']['taskRequirements']],
              '| src p', c['sourceMaterial']['pages'])
    print(f'== {len(cards)} cards; {len(refused)} refused')
    for x in refused:
        print('   REFUSED', x)


if __name__ == '__main__':
    main()
