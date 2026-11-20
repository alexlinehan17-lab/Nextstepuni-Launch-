#!/usr/bin/env python3
"""The Portuguese written tasks (Section B, 2022 on) as rubric cards on the
French grid shape, as Polish's are (pl_writing.py). Portuguese-only.

    python3 scripts/markbank/authoring/pt_writing.py cards 2024 hl

Every string is lifted: the task from the paper's own lines (PL / PLk), the
grid from the scheme's .md (criterion heads, band names, descriptors), each
band's marks read from the range the scheme prints in the band (the k-th
"11 – 15" in its lines, k naming the column: "Q. 3 and 4" or "Q. 5"). The
only words that are the app's are practiceNotes (markingGuideNote stays empty:
build-deck traces it to the scheme).

Sittings and their grids:
* 2024: one table, "Content and Communication" and "Language", bands TOP /
  MIDDLE / BOTTOM, two columns of ranges (Q. 3 and 4: 15; Q. 5: 10). The
  Ordinary grid prints one column, headed "Q.3 and 4" although its tasks are
  Questions 4 and 5 (disclosed in markingGuideNote).
* 2025, 2026: the same bands with a Full Scale and a Lower Scale switched by
  word count -- held for the shared lower-scale change (coordinator, 19 Nov).
* 2022, 2023: a grid per question, three criteria (Content 4, Communication
  13, Language 13) whose bands are named only by their printed ranges, and a
  Content ladder that prints no 0 -- held (see languages-q3/STATUS.md).
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from pt_lib import S, PL, scheme_doc                               # noqa: E402
from eu_paper import EuPaper, read_lines                          # noqa: E402
from eu_topics import topic_for, concept_for                      # noqa: E402
from paper_census import key_label                                # noqa: E402

SUBJECT = 'portuguese'
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}
RANGE = re.compile(r'(?<![\d.])(\d{1,2})\s*[–‐-]\s*(\d{1,2})(?![\d.])')
BULLET = re.compile(r'^\s*[••]\s*')


class PLk:
    """The k-th line (0-based) on paper page `page` that opens with `opening`:
    for a bullet the booklet prints under each of (a), (b) and (c)."""
    def __init__(self, page, opening, k, after=None):
        self.page, self.opening, self.k, self.after = page, opening, k, after

    def text(self, doc):
        hits = [t for p, t in doc['paper'] if p == self.page and t.startswith(self.opening)]
        if len(hits) <= self.k:
            raise ValueError(f'paper p{self.page}: {len(hits)} lines open {self.opening!r}, want #{self.k}')
        t = re.sub(r'\s+', ' ', hits[self.k]).strip()
        if self.after is not None:
            t = t.split(self.after, 1)[1].strip()
        return t


class Band:
    """A band: its printed name (scheme line), the scheme lines of its
    descriptors, and which printed range in them is this column's."""
    def __init__(self, name_line, first, last, col=0):
        self.name_line, self.first, self.last, self.col = name_line, first, last, col

    def read(self, doc):
        name = S(self.name_line).text(doc)
        lines = [doc['scheme'][n - 1].replace('\xa0', ' ') for n in range(self.first, self.last + 1)]
        ranges = [m for line in lines for m in RANGE.finditer(line)]
        if len(ranges) <= self.col:
            raise ValueError(f'band {name!r} (lines {self.first}-{self.last}) prints no range #{self.col}')
        lo, hi = int(ranges[self.col].group(1)), int(ranges[self.col].group(2))
        guidance = []
        for line in lines:
            text = re.sub(r'\s+', ' ', RANGE.sub(' ', line)).strip()
            # A dash the range columns leave behind ("... of the task 0 – 3– 0 – 2",
            # 2025 Higher p10) is the cells', not the descriptor's.
            text = re.sub(r'\s*[–‐-]$', '', text).strip()
            if not text:
                continue
            if BULLET.match(text) or not guidance:
                guidance.append(BULLET.sub('', text))
            else:
                guidance[-1] = f'{guidance[-1]} {text}'
        return {'label': name, 'marks': list(range(lo, hi + 1)), 'guidance': guidance}


class Crit:
    def __init__(self, cid, label, bands):
        self.cid, self.label, self.bands = cid, label, bands

    def read(self, doc):
        bands = [b.read(doc) for b in self.bands]
        top = max(m for b in bands for m in b['marks'])
        return {'id': self.cid, 'label': self.label.text(doc), 'maxMarks': top,
                'permittedMarks': list(range(top + 1)), 'guidance': [],
                'bands': sorted(bands, key=lambda b: -b['marks'][0])}


class ScaledCrit:
    """A criterion printed with two range columns, Full Scale and Lower Scale
    (2025-2026): the full bands from the first range of each band, the lower
    scale's from the second, and the scale switched on by the printed word
    count alone ("If the answer is too short (less than 140 words), mark
    questions 3 and 4 out of 20 marks (lower scale)"): contentCriteria [] and
    no threshold (FrenchLowerScale). `bands` are (name line, first, last)."""
    def __init__(self, cid, label, bands, rule, words_under):
        self.cid, self.label, self.bands = cid, label, bands
        self.rule, self.words_under = rule, words_under

    def read(self, doc):
        full = Crit(self.cid, self.label, [Band(*b, 0) for b in self.bands]).read(doc)
        lower = sorted((Band(*b, 1).read(doc) for b in self.bands), key=lambda b: -b['marks'][0])
        top = max(m for b in lower for m in b['marks'])
        rule = re.sub(r'\s+', ' ', self.rule.text(doc)).strip()
        if f'less than {self.words_under} words' not in rule:
            raise ValueError(f'{self.cid}: the rule does not print the word count {self.words_under}: {rule!r}')
        full['lowerScale'] = {'label': 'Lower', 'maxMarks': top, 'permittedMarks': list(range(top + 1)),
                              'bands': lower, 'contentCriteria': [], 'wordsUnder': self.words_under,
                              'rule': rule}
        return full


ANGLE = re.compile('\u27e8([^\u27e9]*)\u27e9')
CELL_RANGE = re.compile(r'^(\d{1,2})(?:\s*[–‐-]\s*(\d{1,2}))?(?:\s*marks?)?$', re.I)
EMOJI = re.compile('[\U0001F300-\U0001FAFF]')


def _cells(doc, n):
    return [m.group(1).strip() for m in ANGLE.finditer(doc['raw'][n - 1])]


def _items(lines):
    """A band's descriptors: a new one at each bullet; where the band prints
    no bullets, at each line that opens with a capital (a line opening in
    lower case or "(" continues the one above: the SEC wrapped it)."""
    bulleted = any(BULLET.match(t) for t in lines)
    out = []
    for t in lines:
        t = re.sub(r'\s+', ' ', t).strip()
        if not t:
            continue
        new = bool(BULLET.match(t)) if bulleted else not re.match(r'^[a-z(]', t)
        if new or not out:
            out.append(BULLET.sub('', t))
        else:
            # A word the SEC hyphenated over the break ("noun-" / "adjective")
            # joins without a space.
            out[-1] = f'{out[-1]}{t}' if out[-1].endswith('-') else f'{out[-1]} {t}'
    return out


class RangeBand:
    """A band the scheme names by nothing but the range printed in its marks
    cell ("⟨10 - 13⟩" over "⟨marks⟩", 2022-2023): that range is its label and
    its marks; its descriptors are the lines first..last."""
    def __init__(self, first, last):
        self.first, self.last = first, last

    def read(self, doc):
        lines = [TEXT_RANGE.sub(' ', doc['scheme'][k - 1]) for k in range(self.first, self.last + 1)]
        for n in range(self.first, self.last + 1):
            for c in _cells(doc, n):
                m = CELL_RANGE.match(c)
                if m:
                    lo = int(m.group(1)); hi = int(m.group(2) or m.group(1))
                    label = re.sub(r'\s*marks?$', '', c, flags=re.I).strip()
                    return {'label': label, 'marks': list(range(lo, hi + 1)), 'guidance': _items(lines)}
        # Or the range printed in the text itself ("... although 5 - 9 marks",
        # 2023 Ordinary), taken out of the descriptor it sits in.
        for n in range(self.first, self.last + 1):
            m = TEXT_RANGE.search(doc['scheme'][n - 1])
            if m:
                lo, hi = int(m.group(1)), int(m.group(2))
                return {'label': f'{m.group(1)} - {m.group(2)}', 'marks': list(range(lo, hi + 1)),
                        'guidance': _items(lines)}
        raise ValueError(f'lines {self.first}-{self.last}: no printed range')


class RangeCrit:
    """A criterion of the 2022-2023 grids: its printed head, its printed
    maximum (the cell "⟨13⟩" on line max_line), and its bands, which must
    cover 0 to the maximum once (else see RungCrit)."""
    def __init__(self, cid, label, max_line, bands):
        self.cid, self.label, self.max_line, self.bands = cid, label, max_line, bands

    def read(self, doc):
        top = _printed_max(doc, self.max_line)
        bands = sorted((b.read(doc) for b in self.bands), key=lambda b: -b['marks'][0])
        marks = sorted(m for b in bands for m in b['marks'])
        if marks != list(range(top + 1)):
            raise ValueError(f'{self.label.text(doc)}: printed ranges {marks} do not cover 0-{top} once')
        return {'id': self.cid, 'label': self.label.text(doc), 'maxMarks': top,
                'permittedMarks': list(range(top + 1)), 'guidance': [], 'bands': bands}


class RungCrit:
    """A criterion whose printed rungs do not cover 0 to its maximum (2023
    Higher Q4 Content: 4, 3, 2, 1 marks and no 0). Lead ruling 19 Nov 2026:
    no bands; placed 0 to the maximum; the rungs verbatim in its guidance,
    one line per rung with its mark as printed. A rung the SEC wrapped past
    its marks cell is its text and then its mark, the order that traces."""
    def __init__(self, cid, label, max_line, rungs):
        self.cid, self.label, self.max_line, self.rungs = cid, label, max_line, rungs

    def read(self, doc):
        top = _printed_max(doc, self.max_line)
        guidance = []
        for first, last in self.rungs:
            # The rung's printed items: one per bullet (2022: "• Commented
            # ..." and "• Date format ..."), or the whole rung where it prints
            # none; each with the lines it spans.
            bulleted = any(BULLET.match(doc['scheme'][n - 1].strip()) for n in range(first, last + 1))
            items = []
            for n in range(first, last + 1):
                t = re.sub(r'\s+', ' ', doc['scheme'][n - 1]).strip()
                if not t:
                    continue
                if not items or (bulleted and BULLET.match(t)):
                    items.append([BULLET.sub('', t), n, n])
                else:
                    items[-1][0] = f'{items[-1][0]}{t}' if items[-1][0].endswith('-') else f'{items[-1][0]} {t}'
                    items[-1][2] = n
            where = [(n, c) for n in range(first, last + 1) for c in _cells(doc, n) if CELL_RANGE.match(c)]
            if len(where) != 1:
                raise ValueError(f'rung {first}-{last}: {len(where)} mark cells')
            n, cell = where[0]
            # The item the mark belongs to: the one whose lines hold its cell,
            # or the one it follows on a line of its own.
            owner = next((i for i, it in enumerate(items) if it[1] <= n <= it[2]), None)
            if owner is None:
                owner = max(i for i, it in enumerate(items) if it[2] < n)
            for i, (text, a, b) in enumerate(items):
                if i != owner:
                    guidance.append(text)
                elif n >= b:
                    guidance.append(f'{text} {cell}')      # contiguous in reading order
                else:
                    guidance += [text, cell]               # wrapped past its cell
        return {'id': self.cid, 'label': self.label.text(doc), 'maxMarks': top,
                'permittedMarks': list(range(top + 1)), 'guidance': guidance}


TEXT_RANGE = re.compile(r'(?<![\d.])(\d{1,2})\s*[–‐-]\s*(\d{1,2})\s*marks?\b', re.I)


def _printed_max(doc, n):
    nums = [int(m.group(1)) for c in _cells(doc, n) for m in [re.fullmatch(r'(\d{1,2})(?:\s*marks?)?', c, re.I)] if m]
    if len(nums) != 1:
        raise ValueError(f'scheme line {n}: {len(nums)} maximum cells')
    return nums[0]


class Celled:
    """Scheme lines read with their marks cells in place ("Did not follow the
    requested structure/format. -1 mark"), the order the scheme prints."""
    def __init__(self, *ns):
        self.ns = ns

    def text(self, doc):
        return re.sub(r'\s+', ' ', ' '.join(ANGLE.sub(r'\1', doc['raw'][n - 1]) for n in self.ns)).strip()


class Emoji:
    """A paper line whose emoji the page prints in outline: each lifted with
    U+FE0E (text presentation), as the Polish card's was (coordinator, 19 Nov)."""
    def __init__(self, sel):
        self.sel = sel

    def text(self, doc):
        return EMOJI.sub(lambda m: m.group(0) + '\ufe0e', self.sel.text(doc))


class Task:
    """One question's three options: the grid that marks them and, per
    option, the paper lines that print it."""
    def __init__(self, q, page, stem, options, criteria, requirements, scheme_pages, note=''):
        self.q, self.page, self.stem, self.options = q, page, stem, options
        self.criteria, self.requirements, self.scheme_pages, self.note = criteria, requirements, scheme_pages, note


SPECS = {}


def _doc(year, level):
    P = EuPaper(year, level, SUBJECT)
    doc = scheme_doc(year, level)
    # Unfiltered: a task line may open with words the furniture filter takes
    # for a page header ("Leaving Certificate. O texto deve incluir os
    # tópicos:", 2023 Higher Q4(c)). Lines are only ever picked by opening.
    doc['paper'] = [(l.page, l.text) for l in read_lines(P.path, None)]
    return P, doc


def cards(year, level):
    tasks = SPECS.get((year, level))
    if tasks is None:
        raise KeyError(f'no written-task spec for {year} {level}')
    P, doc = _doc(year, level)
    asks = {a.key: a for a in P.writing_asks()}
    out, seen = [], set()
    for t in tasks:
        criteria = [c.read(doc) for c in t.criteria]
        total = sum(c['maxMarks'] for c in criteria)
        for letter, (page, lines) in t.options.items():
            key = ('B', t.q, letter, None)
            if key not in asks:
                raise ValueError(f'{year} {level} Q{t.q}({letter}): the census prints no such ask')
            seen.add(key)
            question = ' '.join(x.text(doc) for x in lines)
            out.append({
                'id': f'por-{year}-{level}-b-{t.q}-{letter}',
                'kind': 'rubric',
                'subjectId': SUBJECT,
                'level': LEVEL_WORD[level],
                'year': year,
                'section': 'B',
                'topicId': topic_for(SUBJECT, P.era, 'B'),
                'conceptId': concept_for(question),
                'questionRef': f'{year} {level.upper()} {key_label(key)}',
                'questionText': question,
                'stem': ' '.join(x.text(doc) for x in t.stem),
                'totalMarks': total,
                'rubric': {
                    'system': 'french',
                    'taskRequirements': [x.text(doc) for x in t.requirements],
                    'criteria': [dict(c) for c in criteria],
                    'markingGuideNote': '',
                    # NextStepUni's own words, under the app's label (a note on
                    # the printed grid's own heading goes here too: the gate
                    # traces markingGuideNote to the scheme).
                    'practiceNotes': ['Write your answer in Portuguese, then place it on the published '
                                      'grid: content and communication first, then language.']
                                     + ([t.note] if t.note else []),
                },
                'schemePages': list(t.scheme_pages),
                'sourceMaterial': {
                    'kind': 'source-text',
                    'label': f'QUESTÃO {t.q}',
                    'title': f'Questão {t.q} ({letter}) — answer in Portuguese',
                    'pages': [page],
                    'attribution': (f'SEC Portuguese {year} {LEVEL_TITLE[level]} Level examination '
                                    f'paper — © State Examinations Commission.'),
                    'presentationNote': 'The task exactly as the examination printed it.',
                },
            })
    missing = sorted(set(asks) - seen, key=str)
    if missing:
        raise ValueError(f'{year} {level}: no card for {[key_label(k) for k in missing]}')
    return out


# ================================================================ 2024 HL ===
# Scheme .md lines 219-266 (page 10): one table, two columns of ranges
# (Q. 3 and 4 | Q. 5). Paper pages 11 (Q3, three pictures), 13 (Q4), 15 (Q5).
def _grid_2024_hl(col):
    return [Crit('content', S(221, before=' Q. 3'),
                 [Band(222, 223, 228, col), Band(229, 230, 235, col), Band(236, 237, 242, col)]),
            Crit('language', S(243, before=' Q. 3'),
                 [Band(244, 245, 250, col), Band(251, 252, 258, col), Band(259, 260, 266, col)])]


_REQ_2024_HL = [S(69)]
SPECS[(2024, 'hl')] = [
    Task(3, 11, [PL(11, 'Observe as imagens')],
         {x: (11, [PL(11, 'Escreva um texto em português, com cerca de 200'),
                   PL(11, '• Que mensagem'), PL(11, '• A sua opinião')]) for x in 'abc'},
         _grid_2024_hl(0), _REQ_2024_HL, [10]),
    Task(4, 13, [PL(13, 'Escolha uma opção'), PL(13, 'Escreva cerca de 200'), PL(13, 'Você foi convidado')],
         {x: (13, [PLk(13, f'({x})', 0, after=f'({x}) '), PLk(13, 'Inclua os seguintes', i)]
                  + [PLk(13, '•', 4 * i + j) for j in range(4)]) for i, x in enumerate('abc')},
         _grid_2024_hl(0), _REQ_2024_HL, [10]),
    Task(5, 15, [PL(15, 'Escolha uma opção'), PL(15, 'Escreva um e')],
         {x: (15, [PLk(15, f'({x})', 0, after=f'({x}) ')] + [PLk(15, '•', 4 * i + j) for j in range(4)])
          for i, x in enumerate('abc')},
         _grid_2024_hl(1), _REQ_2024_HL, [10]),
]


# ================================================================ 2024 OL ===
# Scheme .md lines 203-250 (page 9): one column of ranges, headed "Q.3 and 4"
# though the Ordinary written tasks are Questions 4 and 5 (Parte B, 60 pontos).
def _grid_2024_ol():
    return [Crit('content', S(205, before=' Q.3'),
                 [Band(206, 207, 212), Band(213, 214, 219), Band(220, 221, 226)]),
            Crit('language', S(227, before=' Q. 3'),
                 [Band(228, 229, 234), Band(235, 236, 242), Band(243, 244, 250)])]


_NOTE_2024_OL = ('The scheme heads this grid “Q.3 and 4”; on the Ordinary Level paper the written '
                 'tasks are Questions 4 and 5, each marked out of 30 on it.')
SPECS[(2024, 'ol')] = [
    Task(4, 11, [PL(11, 'Escolha uma opção'), PL(11, 'Escreva um texto em português com cerca de 100')],
         {'a': (11, [PLk(11, '(a)', 0, after='(a) ')] + [PLk(11, '•', j) for j in range(3)]),
          'b': (12, [PLk(12, '(b)', 0, after='(b) ')] + [PLk(12, '•', j) for j in range(3)]),
          'c': (13, [PLk(13, '(c)', 0, after='(c) ')] + [PLk(13, '•', j) for j in range(3)])},
         _grid_2024_ol(), [S(70)], [9], note=_NOTE_2024_OL),
    Task(5, 14, [PLk(14, 'Questão 5', 0, after='Questão 5'), PL(14, 'Escreva um texto em português com cerca de 100')],
         {x: (14, [PL(14, 'Inclua os tópicos'), PL(14, '•Que mensagem'), PL(14, '•A sua opinião')])
          for x in 'abc'},
         _grid_2024_ol(), [S(70)], [9], note=_NOTE_2024_OL),
]


# ================================================================ 2023 HL ===
# Scheme .md lines 268-433 (pages 10-13): a grid per question, Content /
# Communication / Language, each band named only by the range in its marks
# cell. Q4's Content prints rungs 4, 3, 2, 1 and no 0: RungCrit (lead ruling).
# Part B's own rules (lines 269-274) are every card's taskRequirements.
from pt_lib import J, Sel                                          # noqa: E402

_REQ_2023_HL = [S(269), Celled(270, 271), J(S(272), S(273)), S(274)]
_Q3_TOPICS = {'a': ((12, 0), [('Olá, tudo bem?', 0), ('Tudo!', 0), ('Viste a nova série', 0),
                               ('Sim, vi. E foi', 0), ('Oh, que pena eu não ter podido', 0),
                               ('Podias contar-me', 0), ('Tens a certeza?', 0), ('Sim!!! Por favor!!!', 0)]),
              'b': ((12, 1), [('(b) Olá, tudo bem?', 0), ('Tudo!', 1), ('Leste o novo livro', 0),
                               ('Sim, li.', 0), ('Oh, que pena eu ainda', 0), ('Podias contar-me', 1),
                               ('Tens a certeza?', 1), ('Sim!!! Por favor!!!', 1)]),
              'c': ((13, 0), [('Olá, tudo bem?', 0), ('Tudo!', 0), ('Ontem viste', 0), ('Sim, vi.', 0),
                               ('Oh, que pena', 0), ('Qual é o teu desportista', 0)])}


def _chat(page, lines):
    return [Emoji(PLk(page, o, k, after='(b) ' if o.startswith('(b) ') else None)) for o, k in lines]


SPECS[(2023, 'hl')] = [
    Task(3, 12, [PL(12, 'Escolha uma opção'), PL(12, 'Continue a troca'), PL(12, 'Escreva cerca de 200')],
         {x: (page, _chat(page, lines)) for x, ((page, _k), lines) in _Q3_TOPICS.items()},
         [RangeCrit('content', S(277), 276, [RangeBand(278, 279), RangeBand(280, 281), RangeBand(282, 283)]),
          RangeCrit('communication', S(285), 284, [RangeBand(286, 290), RangeBand(291, 295), RangeBand(296, 300)]),
          RangeCrit('language', S(308), 307, [RangeBand(309, 314), RangeBand(315, 321), RangeBand(322, 328)])],
         _REQ_2023_HL, [10, 11]),
    Task(4, 15, [PL(15, 'Escolha uma opção'), PL(15, 'Escreva cerca de 200')],
         {'a': (15, [PLk(15, '(a)', 0, after='(a) ')] + [PLk(15, '•', j) for j in range(5)]),
          'b': (15, [PLk(15, '(b)', 0, after='(b) '), PL(15, 'chegou.')] + [PLk(15, '•', j) for j in range(5, 10)]),
          'c': (15, [PLk(15, '(c)', 0, after='(c) ')] + [PLk(15, '•', j) for j in range(10, 15)])},
         [RungCrit('content', S(336), 336, [(338, 338), (339, 339), (340, 340), (341, 342)]),
          RangeCrit('communication', S(343), 343, [RangeBand(345, 349), RangeBand(350, 354), RangeBand(355, 359)]),
          RangeCrit('language', S(360), 360, [RangeBand(362, 367), RangeBand(368, 374), RangeBand(375, 381)])],
         _REQ_2023_HL, [12]),
    Task(5, 17, [PL(17, 'Observe as imagens')],
         {x: (17, [PL(17, 'Escreva um texto em português, com cerca de 150'), PL(17, '• Que mensagem'),
                   PL(17, '• A sua opinião')]) for x in 'abc'},
         [RangeCrit('content', S(390), 389, [RangeBand(391, 392), RangeBand(393, 394)]),
          RangeCrit('communication', S(396), 395, [RangeBand(397, 401), RangeBand(402, 406), RangeBand(407, 411)]),
          RangeCrit('language', S(413), 412, [RangeBand(414, 419), RangeBand(420, 426), RangeBand(427, 433)])],
         _REQ_2023_HL, [13]),
]


# ================================================================ 2023 OL ===
# Scheme .md lines 235-349 (pages 10-12): Q4 and Q5 each Content 4 (rungs 4,
# 3, 2, 1 and no 0: RungCrit) / Communication 13 / Language 13, some ranges
# in marks cells and some in the text ("... although 5 - 9 marks").
_REQ_2023_OL = [S(236), Celled(237), J(S(238), S(239)), S(240)]
SPECS[(2023, 'ol')] = [
    Task(4, 12, [PL(12, 'Escreva em português, cerca de 100')],
         {'a': (12, [PLk(12, '(a)', 0, after='(a) '), PL(12, 'serviço. Escreva')]
                + [PLk(12, '•', j) for j in range(3)]),
          'b': (13, [PLk(13, '(b)', 0, after='(b) '), PL(13, 'enviadas para'), PL(13, 'serviço de apoio')]
                + [PLk(13, '•', j) for j in range(3)]),
          'c': (14, [PLk(14, '(c)', 0, after='(c) '), PL(14, 'contar a experiência')]
                + [PLk(14, '•', j) for j in range(3)])},
         [RungCrit('content', S(242), 242, [(243, 244), (245, 246), (247, 248), (249, 249)]),
          RangeCrit('communication', S(250), 250, [RangeBand(251, 256), RangeBand(257, 262), RangeBand(263, 268)]),
          RangeCrit('language', S(274), 274, [RangeBand(275, 280), RangeBand(281, 287), RangeBand(288, 294)])],
         _REQ_2023_OL, [10, 11]),
    Task(5, 15, [PL(15, 'Escreva em português, cerca de 100'), PL(15, 'Observe as imagens')],
         {x: (15, [PL(15, 'Escreva um texto onde'), PL(15, '• Escreva sobre'), PL(15, '• Dê a sua opinião')])
          for x in 'abc'},
         [RungCrit('content', S(296), 296, [(297, 298), (299, 300), (301, 302), (303, 304)]),
          RangeCrit('communication', S(310), 310, [RangeBand(311, 316), RangeBand(317, 322), RangeBand(323, 328)]),
          RangeCrit('language', S(329), 329, [RangeBand(330, 335), RangeBand(336, 342), RangeBand(343, 349)])],
         _REQ_2023_OL, [11, 12]),
]


# ================================================================ 2022 HL ===
# Scheme .md lines 234-421 (pages 11-16): a grid per question; Q3 and Q4's
# Content prints rungs 4, 3, 2, 1, each two bullets (the topics, then the
# date format), and no 0: RungCrit. Part B prints no rules of its own.
SPECS[(2022, 'hl')] = [
    Task(3, 9, [PL(9, 'Escreva em português, cerca de 150')],
         {'a': (9, [PLk(9, '(a)', 0, after='(a) '), PL(9, 'os jovens. Escreva')] + [PLk(9, '•', j) for j in range(4)]),
          'b': (9, [PLk(9, '(b)', 0, after='(b) '), PL(9, 'recomendando um filme')]
                + [PLk(9, '•', j) for j in range(4, 8)]),
          'c': (9, [PLk(9, '(c)', 0, after='(c) ')] + [PLk(9, '•', j) for j in range(8, 12)])},
         [RungCrit('content', S(236), 236, [(237, 239), (240, 242), (243, 245), (246, 248)]),
          RangeCrit('communication', S(249), 249, [RangeBand(250, 256), RangeBand(257, 263), RangeBand(268, 274)]),
          RangeCrit('language', S(275), 275, [RangeBand(276, 281), RangeBand(282, 289), RangeBand(290, 297)])],
         [], [11, 12]),
    Task(4, 11, [PL(11, 'Observe as imagens')],
         {x: (11, [PL(11, 'Escreva um texto em português, com cerca de 100'), PL(11, '• Que mensagem'),
                   PL(11, '• A sua opinião')]) for x in 'abc'},
         [RungCrit('content', S(303), 303, [(304, 306), (307, 309), (310, 312), (313, 315)]),
          RangeCrit('communication', S(316), 316, [RangeBand(317, 323), RangeBand(324, 330), RangeBand(335, 341)]),
          RangeCrit('language', S(342), 342, [RangeBand(343, 348), RangeBand(349, 356), RangeBand(357, 364)])],
         [], [13, 14]),
    Task(5, 13, [PL(13, 'Preencha um dos seguintes'), PL(13, 'Escreva cerca de 75')],
         {'a': (13, [PLk(13, '(a)', 0, after='(a) '), PL(13, 'Ficha de Inscrição'), PL(13, 'Nome:'),
                     PL(13, 'Data de Nascimento:'), PL(13, 'Peso:'), PL(13, 'Altura:'), PL(13, 'Endereço:'),
                     PL(13, 'Profissão:'), PL(13, 'Tipo de atividades'), PL(13, 'O que faz nos'), PL(13, 'Razões para')]),
          'b': (14, [PLk(14, '(b)', 0, after='(b) '), PL(14, 'Crítica de um Livro'), PL(14, 'Título:'), PL(14, 'Autor:'),
                     PL(14, 'Género:'), PL(14, 'Personagens:'), PL(14, 'Espaço:'), PL(14, 'Sumário:'),
                     PL(14, 'Parte preferida:'), PL(14, 'Por que razão'), PL(14, 'Classificação:')]),
          'c': (15, [PLk(15, '(c)', 0, after='(c) '), PL(15, 'Ficha de Inscrição'), PL(15, 'Nome:'),
                     PL(15, 'Data de Nascimento:'), PL(15, 'Interesses:'), PL(15, 'Alguém na sua'),
                     PL(15, 'Que instrumento'), PL(15, 'Há quanto tempo'), PL(15, 'Tipos de música'),
                     PL(15, 'Cantor ou grupo'), PL(15, 'O que quer aprender'), PL(15, 'Descreva o último')])},
         [RangeCrit('content', S(370), 370, [RangeBand(371, 371), RangeBand(372, 372)]),
          RangeCrit('communication', S(373), 373, [RangeBand(374, 380), RangeBand(381, 387), RangeBand(388, 394)]),
          RangeCrit('language', S(399), 399, [RangeBand(400, 405), RangeBand(406, 413), RangeBand(414, 421)])],
         [], [15, 16]),
]


# ================================================================ 2022 OL ===
# Scheme .md lines 234-358 (pages 13-16): Q4 and Q5 each Content 4 (rungs 4,
# 3, 2, 1 and no 0, each mark cell on a line of its own inside its rung) /
# Communication 13 / Language 13. Part B prints no rules of its own. Q4's
# stimuli (an e-mail, a blog page, an advert) are on the task's page.
SPECS[(2022, 'ol')] = [
    Task(4, 11, [PL(11, 'Escreva em português, cerca de 100')],
         {'a': (11, [PLk(11, '(a)', 0, after='(a) '), PL(11, 'seguintes pontos:')] + [PLk(11, '•', j) for j in range(3)]),
          'b': (12, [PLk(12, '(b)', 0, after='(b) ')] + [PLk(12, '•', j) for j in range(3)]),
          'c': (12, [PLk(12, '(c)', 0, after='(c) ')] + [PLk(12, '•', j) for j in range(3, 6)])},
         [RungCrit('content', S(236), 236, [(237, 239), (240, 242), (243, 245), (246, 246)]),
          RangeCrit('communication', S(247), 247, [RangeBand(248, 254), RangeBand(255, 261), RangeBand(262, 268)]),
          RangeCrit('language', S(273), 273, [RangeBand(274, 280), RangeBand(281, 287), RangeBand(288, 294)])],
         [], [13, 14]),
    Task(5, 13, [PL(13, 'Escreva em português, cerca de 100'), PL(13, 'Observe as imagens')],
         {x: (13, [PL(13, 'Escreva um texto onde'), PL(13, '• Que mensagem'), PL(13, '• A sua opinião')])
          for x in 'abc'},
         [RungCrit('content', S(300), 300, [(301, 303), (304, 306), (307, 309), (310, 310)]),
          RangeCrit('communication', S(311), 311, [RangeBand(312, 318), RangeBand(319, 325), RangeBand(326, 332)]),
          RangeCrit('language', S(337), 337, [RangeBand(338, 344), RangeBand(345, 351), RangeBand(352, 358)])],
         [], [15, 16]),
]


# ================================================================ 2025 HL ===
# Scheme .md: p9 lines 209-240 (Questions 3 and 4) and p10 lines 245-274
# (Question 5), each band printing its Full Scale and Lower Scale ranges; the
# lower scale is switched on by the word count alone (less than 140 words for
# Q3/Q4, 90 for Q5). No Section B rules are printed (the 2024 word-count
# penalty is gone). Paper p11 (Q3), p13 (Q4), p15 (Q5, three pictures).
def SK(n):
    """Scheme line n with its marks kept: a lower-scale rule is the scheme's
    sentence whole ("... out of 20 marks (lower scale)")."""
    return Sel('scheme', n, keep_tariff=True)


def _scaled(rule, words, cc, cc_bands, lang, lang_bands):
    return [ScaledCrit('content', S(cc), cc_bands, rule, words),
            ScaledCrit('language', S(lang), lang_bands, rule, words)]


def _grid_2025_hl_q34():
    return _scaled(J(SK(210), SK(211)), 140,
                   215, [(216, 217, 219), (220, 221, 223), (224, 225, 227)],
                   228, [(229, 230, 232), (233, 234, 236), (237, 238, 240)])


def _grid_2025_hl_q5():
    return _scaled(SK(245), 90,
                   249, [(250, 251, 253), (254, 255, 257), (258, 259, 261)],
                   262, [(263, 264, 266), (267, 268, 270), (271, 272, 274)])


def _options(page, inclua, per=3):
    """(a)-(c) printed on one page, each its heading, its "Inclua …" line and
    its `per` bullets."""
    return {x: (page, [PLk(page, f'({x})', 0, after=f'({x}) '), PLk(page, inclua, i)]
                + [PLk(page, '•', per * i + j) for j in range(per)]) for i, x in enumerate('abc')}


SPECS[(2025, 'hl')] = [
    Task(3, 11, [PL(11, 'Escolha uma opção'), PL(11, 'Escreva cerca de 200'), PL(11, 'Seu professor')],
         _options(11, 'Inclua os seguintes'), _grid_2025_hl_q34(), [], [9]),
    Task(4, 13, [PL(13, 'Escolha uma opção'), PL(13, 'Escreva um e'), PL(13, 'Você teve uma ideia')],
         _options(13, 'Inclua os seguintes'), _grid_2025_hl_q34(), [], [9]),
    Task(5, 15, [PL(15, 'Observe as imagens')],
         {x: (15, [PL(15, 'Escreva um texto em português, com cerca de 150'),
                   PL(15, '• Que mensagem'), PL(15, '• A sua opinião')]) for x in 'abc'},
         _grid_2025_hl_q5(), [], [10]),
]


# ================================================================ 2025 OL ===
# Scheme .md p11 lines 271-301: one grid for Questions 4 and 5, Full and Lower
# Scale (less than 60 words). Paper: Q4 (a) p12, (b) p13, (c) p14; Q5 p15
# (three pictures).
def _grid_2025_ol():
    return _scaled(J(SK(271), SK(272)), 60,
                   276, [(277, 278, 280), (281, 282, 284), (285, 286, 288)],
                   289, [(290, 291, 293), (294, 295, 297), (298, 299, 301)])


SPECS[(2025, 'ol')] = [
    Task(4, 12, [PL(12, 'Escolha uma opção'), PL(12, 'Escreva um texto em português com cerca de 100')],
         {'a': (12, [PLk(12, '(a)', 0, after='(a) '), PL(12, 'Escreva um email')] + [PLk(12, '•', j) for j in range(3)]),
          'b': (13, [PLk(13, '(b)', 0, after='(b) '), PL(13, 'Escreva uma apresentação')]
                + [PLk(13, '•', j) for j in range(3)]),
          'c': (14, [PLk(14, '(c)', 0, after='(c) ')] + [PLk(14, '•', j) for j in range(3)])},
         _grid_2025_ol(), [], [11]),
    Task(5, 15, [PLk(15, 'Questão 5', 0, after='Questão 5 '), PL(15, 'Escreva um texto em português com cerca de 100')],
         {x: (15, [PL(15, 'Inclua os seguintes'), PL(15, '• Que mensagem'), PL(15, '• A sua opinião')])
          for x in 'abc'},
         _grid_2025_ol(), [], [11]),
]


# ================================================================ 2026 OL ===
# Scheme .md p10 lines 228-258: one grid for Questions 4 and 5, Full and Lower
# Scale (less than 60 words). Paper: Q4 (a) p12, (b) p13, (c) p14, each
# heading wrapped onto a second line; Q5 p15 (three pictures).
def _grid_2026_ol():
    return _scaled(J(SK(228), SK(229)), 60,
                   233, [(234, 235, 237), (238, 239, 241), (242, 243, 245)],
                   246, [(247, 248, 250), (251, 252, 254), (255, 256, 258)])


def _wrapped(page, x, cont):
    return (page, [PLk(page, f'({x})', 0, after=f'({x}) '), PL(page, cont), PL(page, 'Inclua as seguintes')]
            + [PLk(page, '•', j) for j in range(3)])


SPECS[(2026, 'ol')] = [
    Task(4, 12, [PL(12, 'Escolha uma opção'), PL(12, 'Escreva um texto em português com cerca de 100')],
         {'a': _wrapped(12, 'a', 'escolher um país'), 'b': _wrapped(13, 'b', 'foi a sua experiência'),
          'c': _wrapped(14, 'c', 'de reclamação')},
         _grid_2026_ol(), [], [10]),
    Task(5, 15, [PLk(15, 'Questão 5', 0, after='Questão 5 '), PL(15, 'Escreva um texto em português com cerca de 100')],
         {x: (15, [PL(15, 'Inclua os seguintes'), PL(15, '• Que mensagem'), PL(15, '• A sua opinião')])
          for x in 'abc'},
         _grid_2026_ol(), [], [10]),
]


# ================================================================ 2026 HL ===
# Scheme .md p10 lines 231-263 (Questions 3 and 4, less than 140 words) and
# p11 lines 268-299 (Question 5, less than 90). The Language bands print their
# range columns on the FIRST line of a wrapped bullet ("Verb endings, tenses,
# agreements (number, gender, etc.) 11 – 15 8 – 10" / "nearly always
# correct."): the descriptor reads whole, and traces through the grid gate's
# band-range form extended to a line's two trailing range pairs (lead ruling,
# 19 Nov 2026). Paper p11 (Q3), p13 (Q4), p15 (Q5, three pictures).
def _grid_2026_hl_q34():
    return _scaled(J(SK(231), SK(232)), 140,
                   235, [(236, 237, 239), (240, 241, 243), (244, 245, 247)],
                   248, [(249, 250, 253), (254, 255, 258), (259, 260, 263)])


def _grid_2026_hl_q5():
    return _scaled(SK(268), 90,
                   271, [(272, 273, 275), (276, 277, 279), (280, 281, 283)],
                   284, [(285, 286, 289), (290, 291, 294), (295, 296, 299)])


SPECS[(2026, 'hl')] = [
    Task(3, 11, [PL(11, 'Escolha uma opção'), PL(11, 'Escreva cerca de 200'), PL(11, 'Escreva um e')],
         _options(11, 'Inclua os seguintes'), _grid_2026_hl_q34(), [], [10]),
    Task(4, 13, [PL(13, 'Escolha uma opção'), PL(13, 'Escreva cerca de 200'), PL(13, 'Escreva um anúncio')],
         _options(13, 'Inclua os seguintes'), _grid_2026_hl_q34(), [], [10]),
    Task(5, 15, [PLk(15, 'Questão 5', 0, after='Questão 5 ')],
         {x: (15, [PL(15, 'Escreva um texto em português, com cerca de 150'),
                   PL(15, '• Que mensagem'), PL(15, '• A sua opinião')]) for x in 'abc'},
         _grid_2026_hl_q5(), [], [11]),
]


def main():
    import json
    cmd, year, level = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    if cmd == 'cards':
        for c in cards(year, level):
            print(f"== {c['questionRef']} [{c['totalMarks']}] p{c['sourceMaterial']['pages']} stem: {c['stem']}")
            print(f"   Q: {c['questionText']}")
        print(json.dumps(cards(year, level)[0]['rubric'], ensure_ascii=False, indent=1)[:3000])


if __name__ == '__main__':
    main()
