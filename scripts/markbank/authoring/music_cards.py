#!/usr/bin/env python3
"""Music: every sitting, 2010-2026, Higher and Ordinary, June and deferred (music lane).

    python3 scripts/markbank/authoring/music_cards.py
    python3 scripts/markbank/authoring/music_cards.py --check <reading file> [<crops dir>]   (one sitting, writes nothing)

Writes scripts/markbank/authored/music.json (the cards), authored/music-census.json
(every printed ask, the denominator) and components/MarkBank/figures-music.json
(the crops). 2025 Higher comes from music_2025.py (the approved prototype,
emitted exactly as before); every other sitting from its reading file
authored/music-review/<year>-<hl|ol>[-deferred].json, one ask per entry, read
page by page off the booklets and the scheme (format: the music lane's
REVIEW-FORMAT.md).

Lift, never write: every question line is checked against the booklet's text
layer (or, for a booklet with no text layer, against its page images' OCR in
music-review/ocr/), every answer, rule and band line against the scheme's text
(PDF text layer and the committed .md). A line found in neither stops the run.
A card's heading is checked against the Topic Atlas: the card's topic must sit
under a heading its printed question is filed under.

The treatments are the approved prototype's (Alex, 18 Nov): printed answers as
claimable rows; example lists as "any N" menus; a rule with no answer as
UNPRINTED_ANSWER on the rule's marks, the rule quoted; notation answers as a
crop of the scheme's print beside its words; band-marked asks on the scheme's
bands (the grid languages use); Composing Section B's counted lines on the
counted grid line; every listening card plays the SEC recording.
"""
import glob
import hashlib
import json
import os
import re
import sys
import unicodedata

import fitz

import music_2025

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
REVIEW_DIR = os.path.join(ROOT, 'scripts/markbank/authored/music-review')
OUT = os.path.join(ROOT, 'scripts/markbank/authored/music.json')
CENSUS = os.path.join(ROOT, 'scripts/markbank/authored/music-census.json')
FIG_DIR = os.path.join(ROOT, 'public/exam-figures/music/markbank')
FIG_MANIFEST = os.path.join(ROOT, 'components/MarkBank/figures-music.json')
PAPERS_DIR = os.path.join(ROOT, 'examiner-reports/music/papers')
SCHEMES_DIR = os.path.join(ROOT, 'examiner-reports/music/schemes')
CORPUS = os.path.join(ROOT, 'paper-trail-corpus')
TAGS = os.path.join(ROOT, 'scripts/paper-trail/topic-tags/tags/music.json')
HEADINGS = os.path.join(ROOT, 'data/examTopics/music-runtime.json')
UNPRINTED = 'The scheme prints no answer for this part.'
NOTATION_NOTE = 'The scheme prints its answer in music notation: its print is shown on this card.'
COMPONENT = {'composing': '006', 'elective': '007', 'listening': '008'}
BOOKLET = {'composing': 'Composing', 'elective': 'Elective', 'listening': 'Listening'}
LVL = {'higher': 'hl', 'ordinary': 'ol'}
LEVEL_WORD = {'higher': 'Higher Level', 'ordinary': 'Ordinary Level'}


def norm(text):
    # A printed flat or sharp sign reaches the text layer as the music font's
    # "b" / "#": compare a card's ♭ with that "b" (♯ and "#" both drop out below).
    text = unicodedata.normalize('NFKC', (text or '').replace('♭', 'b')).lower()
    text = re.sub('[‐-―]', '-', text)
    return re.sub(r'[^a-z0-9Ā-ſ]+', '', text)


MUSIC_FONTS = ('Opus', 'Rousseau', 'Maestro', 'Petrucci', 'Sonata', 'Bravura')
SIGN = {'b': '♭', '#': '♯'}


def music_signs(pdf):
    """Where the text layer types a flat or sharp in a music font (OpusTextStd's "b" is
    drawn as ♭, Rousseau's "#" as ♯): the line as the text layer spells it, a few
    characters either side of the letter and its sign, whitespace collapsed. A card
    string that spells one of these with the plain letter has dropped the printed
    sign (2025 HL Composing Q4 "Eb major" for the printed E♭ major)."""
    out = set()
    for page in fitz.open(pdf):
        for block in page.get_text('rawdict')['blocks']:
            for line in block.get('lines', []):
                chars = [(c['c'], span['font']) for span in line['spans'] for c in span['chars']]
                text = ''.join(c for c, _ in chars)
                for i, (c, font) in enumerate(chars):
                    if c in SIGN and i and chars[i - 1][0] in 'ABCDEFG' and any(f in font for f in MUSIC_FONTS) \
                            and not any(f in chars[i - 1][1] for f in MUSIC_FONTS):
                        left = re.sub(r'\s+', ' ', text[max(0, i - 7):i])
                        right = re.sub(r'\s+', ' ', text[i + 1:i + 7])
                        out.add((left, c, right))
    return out


def dropped_sign(text, signs):
    flat = re.sub(r'\s+', ' ', text or '')
    for left, c, right in signs:
        core = left[-2:] + c + right[:4]
        if core in flat:
            return f'{left}{SIGN[c]}{right}'
    return None


def recordings(year, deferred):
    """The two SEC sound files of a year's listening test (SOURCES.md), by file number."""
    if year <= 2011:
        ids = ('LC067ZLP100EV.mp3', 'LC067ZLP200EV.mp3')
    elif year <= 2021:
        ids = ('LC067ZLP117EV.mp3', 'LC067ZLP217EV.mp3')
    else:
        ids = ('LC067ZLP045EV.mp3', 'LC067ZLP046EV.mp3')
    view = 'deferredexams' if deferred else 'exampapers'
    return {n + 1: (f, f'https://www.examinations.ie/archive/{view}/{year}/{f}') for n, f in enumerate(ids)}


class Sitting:
    def __init__(self, path):
        self.path = path
        self.data = json.load(open(path, encoding='utf-8'))
        d = self.data
        self.year, self.level, self.deferred = d['year'], d['level'], bool(d.get('deferred'))
        self.lvl = LVL[self.level]
        self.tag = f'{self.lvl}-deferred' if self.deferred else self.lvl
        self.LV = self.lvl.upper()
        self.ref_suffix = ' — Deferred sitting' if self.deferred else ''
        self.papers = {}
        self.paper_text = {}
        self.ocr_text = {}
        for kind, comp in COMPONENT.items():
            path = self.paper_path(kind)
            if path and os.path.exists(path):
                self.papers[kind] = path
                self.paper_text[kind] = norm(''.join(p.get_text() for p in fitz.open(path)))
                ocr = os.path.join(REVIEW_DIR, 'ocr', f'{self.year}-{self.tag}-{comp}.json')
                if os.path.exists(ocr):
                    self.ocr_text[kind] = norm(' '.join(json.load(open(ocr, encoding='utf-8')).values()))
        self.scheme_pdf = self.scheme_path()
        md = os.path.join(SCHEMES_DIR, f'{self.year}-{self.tag}.md')
        text = ''.join(p.get_text() for p in fitz.open(self.scheme_pdf))
        if os.path.exists(md):
            text += open(md, encoding='utf-8').read()
        self.scheme_text = norm(text)
        self.scheme_signs = music_signs(self.scheme_pdf)
        self.paper_signs = {kind: music_signs(path) for kind, path in self.papers.items()}
        self.attr_paper = (f'SEC Leaving Certificate Music {self.year} {LEVEL_WORD[self.level]} '
                           f'{"deferred " if self.deferred else ""}examination paper — © State Examinations Commission')
        self.attr_scheme = (f'SEC Leaving Certificate Music {self.year} {LEVEL_WORD[self.level]} marking scheme'
                            f'{", deferred examination" if self.deferred else ""} — © State Examinations Commission')

    def paper_path(self, kind):
        comp = COMPONENT[kind]
        if self.deferred:
            return os.path.join(CORPUS, 'deferredexams', str(self.year), f'LC067{"A" if self.level == "higher" else "G"}LP{comp}EV.pdf')
        return os.path.join(PAPERS_DIR, f'{self.year}-{self.lvl}-{comp}-paper.pdf')

    def scheme_path(self):
        if self.deferred:
            files = sorted(glob.glob(os.path.join(CORPUS, 'deferredmarkingschemes', str(self.year), 'LC067*EV.pdf')))
            return files[0]
        return os.path.join(SCHEMES_DIR, f'{self.year}-{self.lvl}.pdf')

    def fileid(self, kind):
        return f'LC067{"A" if self.level == "higher" else "G"}LP{COMPONENT[kind]}EV.pdf'

    # ------------------------------------------------------------ gates ----
    def scheme(self, text):
        if not text or norm(text) not in self.scheme_text:
            raise SystemExit(f'{self.year} {self.tag}: not in the scheme: {text!r}')
        printed = dropped_sign(text, self.scheme_signs)
        if printed:
            raise SystemExit(f'{self.year} {self.tag}: the scheme prints a music-font sign here ({printed!r}): {text!r}')
        return text

    def paper(self, kind, text):
        # A line no text layer or OCR reading can carry (a printed superscript,
        # "Use the form AA¹BB¹.") is accepted only as the reading file records it:
        # read off a render of the page by the lane lead, with page, box and reader.
        if any(r['booklet'] == kind and r['text'] == text for r in self.data.get('readFromPage', [])):
            return text
        t = norm(text)
        if not t or (t not in self.paper_text.get(kind, '') and t not in self.ocr_text.get(kind, '')):
            raise SystemExit(f'{self.year} {self.tag}: not in the {kind} booklet: {text!r}')
        printed = dropped_sign(text, self.paper_signs.get(kind, set()))
        if printed:
            raise SystemExit(f'{self.year} {self.tag}: the {kind} booklet prints a music-font sign here ({printed!r}): {text!r}')
        return text

    def quote(self, lines):
        return 'The scheme reads: ' + ' '.join(f'“{self.scheme(l)}”' for l in lines)

    # -------------------------------------------------------- addresses ----
    def card_id(self, a):
        kind, addr = a['paper'], a['address']
        base = f'mus-{self.year}-{self.tag}'
        if kind == 'listening':
            # 2018 numbers its parts afresh under each excerpt: "Q1 Excerpt 2(i)".
            m = re.fullmatch(r'Q(\d)(?: ([AB]))?(?: Excerpt (\d))?((?:\([a-z]+\))*)', addr)
            if not m:
                raise SystemExit(f'listening address {addr!r}')
            parts = re.findall(r'\(([a-z]+)\)', m.group(4))
            excerpt = f'x{m.group(3)}' if m.group(3) else ''
            return '-'.join(x for x in [f'{base}-l', f'q{m.group(1)}', (m.group(2) or '').lower(), excerpt, *parts] if x)
        if kind == 'composing':
            # Ordinary Level prints two melodies under one question, "Answer (a) and (b)".
            m = re.fullmatch(r'Section ([AB]) Q(\d)((?:\([a-z]+\))*)', addr)
            if not m:
                raise SystemExit(f'composing address {addr!r}')
            parts = re.findall(r'\(([a-z]+)\)', m.group(3))
            return '-'.join([f'{base}-c-{m.group(1).lower()}-q{m.group(2)}', *parts])
        return f'{base}-e-' + addr.lower().replace('(', '-').replace(')', '')

    def ref(self, a):
        return f'{self.year} {self.LV} {BOOKLET[a["paper"]]} {a["address"]}{self.ref_suffix}'

    def question_number(self, a):
        """The printed question number the Topic Atlas files this ask under."""
        if a['paper'] == 'elective':
            return '1'
        return re.search(r'Q(\d)', a['address']).group(1)


# ----------------------------------------------------------------- crops ----
MANIFEST = {}


def crop(pdf, page, box, key, alt, attribution, solution=False):
    doc = fitz.open(pdf)
    pg = doc[page - 1]
    W, H = pg.rect.width, pg.rect.height
    clip = fitz.Rect(box[0] * W, box[1] * H, box[2] * W, box[3] * H)
    os.makedirs(FIG_DIR, exist_ok=True)
    path = os.path.join(FIG_DIR, f'{key}.png')
    pg.get_pixmap(dpi=200, clip=clip).save(path)
    md5 = hashlib.md5(open(path, 'rb').read()).hexdigest()
    if key in MANIFEST:
        raise SystemExit(f'two crops named {key}')
    MANIFEST[key] = {'src': f'/exam-figures/music/markbank/{key}.png', 'md5': md5,
                     'alt': alt, 'attribution': attribution, **({'solution': True} if solution else {})}
    return key


# ---------------------------------------------------------------- topics ----
class Atlas:
    def __init__(self):
        self.tags = {}
        for e in json.load(open(TAGS, encoding='utf-8')):
            if e['lang'] != 'ev':
                continue
            for q in e['q']:
                self.tags[(e['year'], e['level'], e['fileid'], q['n'])] = [x for x in (q.get('primary'), q.get('secondary')) if x]
        runtime = json.load(open(HEADINGS, encoding='utf-8'))
        groups = {g[0]: g[1] for g in runtime['groups']}
        self.headings = {}  # (levelKey, curriculum id) -> heading ids
        for t in runtime['topics']:
            for cid in t[5]:
                self.headings.setdefault((t[6], cid), set()).add(t[0])
        self.groups = groups

    def check(self, s, a, topic):
        """The card's topic must sit under a heading its printed question is filed under."""
        if s.deferred:
            return  # the Atlas files deferred papers once they are tagged; checked when they are
        key = (s.year, s.level, s.fileid(a['paper']), s.question_number(a))
        filed = self.tags.get(key)
        if filed is None:
            raise SystemExit(f'{s.ref(a)}: no Topic Atlas question {key}')
        lk = 'h' if s.level == 'higher' else 'o'
        mine = self.headings.get((lk, topic), set())
        theirs = set().union(*(self.headings.get((lk, t), set()) for t in filed))
        if not mine & theirs:
            raise SystemExit(f'{s.ref(a)}: topic {topic} shares no heading with the Atlas question ({filed})')


# ------------------------------------------------------------------ rows ----
def build_rows(s, a):
    rows = []
    for i, spec in enumerate(a['rows']):
        rid = f'r-{i + 1}'
        t = spec['type']
        note = []
        if spec.get('quote'):
            note.append(s.quote(spec['quote']))
        if spec.get('printedAnswer'):
            note.append(NOTATION_NOTE)
        if t == 'point':
            row = {'id': rid, 'kind': 'point', 'verbatim': s.scheme(spec['text']), 'marks': spec['marks']}
        elif t == 'ask':
            # The answer is printed in notation (shown as the scheme's crop): the
            # row names the ask in the paper's own words.
            row = {'id': rid, 'kind': 'point', 'verbatim': s.paper(a['paper'], spec['text']), 'marks': spec['marks'], 'ask': True}
        elif t == 'criterion':
            row = {'id': rid, 'kind': 'criterion', 'verbatim': s.scheme(spec['text']), 'marks': spec['marks']}
            if spec.get('steps'):
                row['permittedMarks'] = spec['steps']
        elif t == 'rule':
            top = spec['marks']
            steps = spec.get('steps') or list(range(0, int(top) + 1))
            row = {'id': rid, 'kind': 'criterion', 'verbatim': UNPRINTED, 'marks': top,
                   'permittedMarks': steps, 'unprinted': True}
        elif t == 'menu':
            options = []
            for o in spec['options']:
                for half in o.split(' — '):
                    s.scheme(half)
                options.append(o)
            row = {'id': rid, 'kind': 'anyN', 'verbatim': spec['label'], 'marks': None, 'openList': bool(spec.get('open')),
                   'group': {'claimMax': spec['claim'], 'perOption': spec['per'], 'options': options}}
        else:
            raise SystemExit(f'{s.ref(a)}: row type {t!r}')
        if note:
            row['contextNote'] = ' '.join(note)
        rows.append(row)
    return rows


# ----------------------------------------------------------------- cards ----
def source_for(s, a, title):
    kind = a['paper']
    label = {'listening': 'LISTENING (CORE)' if s.level == 'higher' else 'LISTENING',
             'composing': f'COMPOSING · SECTION {a["address"][8]}' if kind == 'composing' else '',
             'elective': 'LISTENING ELECTIVE'}[kind]
    src = {'kind': 'source-text', 'label': label, 'title': title, 'pages': a['pages'],
           'attribution': f'{s.attr_paper}.', 'sourceLabel': BOOKLET[kind],
           'presentationNote': a.get('presentationNote') or {
               'listening': 'The question as the listening booklet prints it. Play the recording, then answer.',
               'composing': 'The question and its printed opening, exactly as the composing booklet sets them.',
               'elective': 'The questions exactly as the elective booklet prints them, about your own chosen topic.'}[kind]}
    if a.get('crop'):
        src['regions'] = [{'p': a['page'], 'r': a['crop']}]
    return src


def question_text(s, a):
    """The ask's words, each piece checked against the booklet (the title and
    bullets of a composing question are checked one by one)."""
    text = a['questionText']
    for line in text.split('\n'):
        for piece in line.split(' • '):
            s.paper(a['paper'], piece)
    return text


def printed_block(s, kind, text):
    """A lead-in or excerpt line, each printed line checked against the booklet
    on its own: the lines of the block, its bullets, and each numbered lyric line
    ("Line 4 Galileo, ..."), label and words together. A reading of a page in
    bands can repeat or reorder whole lines at a band edge, never a line's words."""
    if any(r['booklet'] == kind and r['text'] == text for r in s.data.get('readFromPage', [])):
        return text
    for line in text.split('\n'):
        for piece in re.split(r' (?=Line \d+ )', line.removeprefix('• ')):
            s.paper(kind, piece)
    return text


def figure_keys(s, a, card, cid):
    short = cid[len(f'mus-{s.year}-{s.tag}-'):]
    stem = f'music-{s.year}-{s.LV}{"-deferred" if s.deferred else ""}'
    fig = a.get('figure')
    if fig:
        card['questionFigureKey'] = crop(s.papers[a['paper']], fig['page'], fig['box'], f'{stem}-{short}-score',
                                         f'{fig["what"]}, printed with {BOOKLET[a["paper"]]} {a["address"]} in the {s.year} '
                                         f'{LEVEL_WORD[s.level]} {"deferred " if s.deferred else ""}paper, as the SEC set it.',
                                         s.attr_paper)
        card['questionFigureIncludesPrompt'] = bool(fig.get('includesPrompt'))
    sc = a.get('schemeCrop')
    if sc:
        card['figureKey'] = crop(s.scheme_pdf, sc['page'], sc['box'], f'{stem}-scheme-p{sc["page"]}-{short}',
                                 f'The marking scheme’s printed answer for {BOOKLET[a["paper"]]} {a["address"]}: {sc["what"]}, '
                                 f'cropped from page {sc["page"]} of the scheme.', s.attr_scheme, solution=True)


def point_card(s, a, atlas):
    cid = s.card_id(a)
    q = int(s.question_number(a))
    question = question_text(s, a)
    topic = a['topicId']
    atlas.check(s, a, topic)
    card = {'id': cid, 'subjectId': 'music', 'level': s.level, 'year': s.year,
            'section': {'listening': 'L', 'composing': 'A', 'elective': 'E'}[a['paper']],
            'topicId': topic, 'conceptId': music_2025.concept(a.get('conceptText') or question), 'questionRef': s.ref(a),
            'questionText': question, 'totalMarks': a['marks'],
            'sourceMaterial': source_for(s, a, f'{BOOKLET[a["paper"]]} — Question {q}')}
    stem = ' '.join(printed_block(s, a['paper'], x) for x in [a.get('questionContext'), a.get('excerptLine')] if x)
    if stem:
        card['stem'] = stem
    if a.get('needsRecording'):
        n = a.get('soundFile') or (1 if q <= 4 else 2)
        fileid, url = recordings(s.year, s.deferred)[n]
        card['audioMaterial'] = {
            'kind': 'source-audio',
            'label': f'Question {q} · {(a.get("excerptLine") or "").split(",")[0]}'.strip(' ·'),
            'title': f'{s.year} Music · {"Deferred " if s.deferred else ""}Listening test (Higher and Ordinary)'
                     if not s.deferred else f'{s.year} Music · Deferred listening test (Higher)',
            'playbackUrl': url, 'secFileid': fileid, 'canonicalUrl': url,
            'attribution': '© State Examinations Commission.',
            'presentationNote': f'The SEC publishes this test as two sound files. This is Sound File {n} of 2. '
                                'Use the player to move to the question and replay the excerpt.'}
    card['rows'] = build_rows(s, a)
    card['tariffModel'] = {'kind': 'fixed'}
    figure_keys(s, a, card, cid)
    if any(r.get('printedAnswer') or r['type'] == 'ask' for r in a['rows']) and not a.get('schemeCrop'):
        raise SystemExit(f'{s.ref(a)}: an answer printed in notation needs the scheme crop')
    return card


def grid_criteria(s, spec):
    out = []
    for k in spec['criteria']:
        crit = {'id': k['id'], 'label': s.scheme(k['label']), 'maxMarks': k['max']}
        if k.get('counted'):
            rate, items = k['counted']['rate'], k['counted']['items']
            crit['permittedMarks'] = [i * rate for i in range(items + 1)]
            crit['guidance'] = [s.scheme(g) for g in k.get('guidance', [])]
            crit['counted'] = {'rate': rate, 'items': items}
        else:
            top = k['max']
            # A band line whose printed top is a half mark (2018 HL Composing Q4's
            # bass quality, "8 – 9.5" beside 0.5 x 21 = 10.5): every whole mark
            # below it and the printed top, as the bands print them.
            ladder = list(range(int(top) + 1)) + ([top] if top != int(top) else [])
            crit['permittedMarks'] = ladder
            crit['guidance'] = [s.scheme(g) for g in k.get('guidance', [])]
            if not k.get('bands'):
                # "Up to 3 marks for quality ... (3 x 4)": placed on its marks, no descriptors printed.
                out.append(crit)
                continue
            bands = []
            for b in k['bands']:
                marks = b['marks']
                if isinstance(marks, str):
                    nums = [float(n) for n in re.findall(r'\d+(?:\.\d+)?', marks)]
                    marks = [m for m in ladder if min(nums) <= m <= max(nums)]
                bands.append({'label': s.scheme(b['label']), 'marks': marks,
                              'guidance': [s.scheme(g) for g in b.get('guidance', [])]})
            crit['bands'] = bands
        out.append(crit)
    return out


def grid_card(s, a, atlas, cid=None, ref=None, question=None):
    cid = cid or s.card_id(a)
    q = s.question_number(a)
    question = question or question_text(s, a)
    spec = a['grid']
    topic = a['topicId']
    atlas.check(s, a, topic)
    section = {'listening': 'L', 'elective': 'E'}.get(a['paper']) or a['address'][8]
    title = (f'Section {section} — Question {q}' if a['paper'] == 'composing'
             else 'Listening elective — Questions' if a['paper'] == 'elective'
             else f'Question {q} {a["address"].split(" ")[1][0]}' if ' ' in a['address'] else f'Question {q}')
    card = {'id': cid, 'kind': 'rubric', 'subjectId': 'music', 'level': s.level, 'year': s.year,
            'section': section, 'topicId': topic, 'conceptId': music_2025.concept(a.get('conceptText') or question),
            'questionRef': ref or s.ref(a), 'questionText': question, 'totalMarks': a['marks'],
            'schemePages': spec['schemePages'],
            'rubric': {'system': 'french', 'taskRequirements': [s.scheme(x) for x in spec.get('taskRequirements', [])],
                       'criteria': grid_criteria(s, spec),
                       'markingGuideNote': s.scheme(spec['markingGuideNote'])},
            'sourceMaterial': source_for(s, a, title)}
    if spec.get('stem'):
        # A stem may carry several printed lines of the block (Q5's lead-in, then
        # "B Answer one of the following:"): each line is checked on its own.
        card['stem'] = '\n'.join(s.paper(a['paper'], x) for x in spec['stem'].split('\n'))
    if a.get('schemeCrop'):
        # The scheme's own print held back to the reveal: a composing question's
        # table of accepted chords, box by box, which a grid cannot carry.
        figure_keys(s, dict(a, figure=None), card, cid)
    if sum(k['maxMarks'] for k in card['rubric']['criteria']) != a['marks']:
        raise SystemExit(f'{card["questionRef"]}: criteria do not make {a["marks"]}')
    return card


# ----------------------------------------------------------------- build ----
def crops_overlapping(s):
    """Pairs of asks whose scheme crops overlap on one page: each pair is LOOKED
    at, because a crop must never show another ask's answer (2026 HL Q1(e)'s crop
    once carried Q1(f)'s notes at Y, and Q1(f)'s the time signature at X)."""
    crops = [(a['address'], a['schemeCrop']) for a in s.data['asks'] if a.get('schemeCrop')]
    out = []
    for i, (n1, c1) in enumerate(crops):
        for n2, c2 in crops[i + 1:]:
            a, b = c1['box'], c2['box']
            if c1['page'] == c2['page'] and min(a[2], b[2]) - max(a[0], b[0]) > 0.005 \
                    and min(a[3], b[3]) - max(a[1], b[1]) > 0.005:
                out.append((n1, n2, c1['page']))
    return out


def build_sitting(s, atlas):
    cards, census, covers = [], {}, {}
    shared = {}
    for a in s.data['asks']:
        cid = s.card_id(a)
        census.setdefault(a['paper'], []).append({'id': cid, 'questionRef': s.ref(a)})
        if a.get('sharedCard'):
            shared.setdefault(a['sharedCard'], []).append(a)
            continue
        cards.append(grid_card(s, a, atlas) if a.get('grid') else point_card(s, a, atlas))
    # Asks the scheme marks together (the Listening elective's shared band):
    # one card, its question every ask's printed words, covering them all.
    for name, asks in shared.items():
        lead = asks[0]
        question = ' '.join(f'{x.get("label", "")} {question_text(s, x)}'.strip() for x in asks)
        cid = f'mus-{s.year}-{s.tag}-{name}'
        first, last = asks[0]['address'], asks[-1]['address']
        base = first.split('(')[0]
        span = f'{first}–{last[len(base):]}' if last.startswith(base + '(') else f'{first}–{last}'
        ref = f'{s.year} {s.LV} {BOOKLET[lead["paper"]]} {span}{s.ref_suffix}'
        lead = dict(lead, pages=sorted({p for x in asks for p in x['pages']}), crop=None)
        cards.append(grid_card(s, lead, atlas, cid=cid, ref=ref, question=question))
        covers[cid] = [s.card_id(x) for x in asks]
    papers = []
    for kind in ('listening', 'composing', 'elective'):
        asks = census.get(kind, [])
        if asks:
            name = BOOKLET[kind] + (' — Deferred' if s.deferred else '')
            papers.append({'year': s.year, 'level': s.level, 'paper': name, 'expectedAsks': len(asks), 'asks': asks})
    return cards, papers, covers


def check(path, crops_to):
    """Build ONE sitting in memory and report it; writes nothing but its crops (to `crops_to`)."""
    global FIG_DIR
    FIG_DIR = crops_to
    s = Sitting(path)
    cards, papers, covers = build_sitting(s, Atlas())
    for p in papers:
        print(f"{p['paper']}: {p['expectedAsks']} asks")
    marks = {}
    for c in cards:
        marks[c['section']] = marks.get(c['section'], 0) + c['totalMarks']
    print(f'{len(cards)} cards; marks by section (every option of a choice counted): {marks}')
    for c in cards:
        rows = c.get('rows') or c['rubric']['criteria']
        print(f"  {c['id']:34} {c['totalMarks']:>5}  {c['topicId']:12} {len(rows)} rows/criteria"
              f"{'  audio ' + c['audioMaterial']['secFileid'] if c.get('audioMaterial') else ''}"
              f"{'  fig' if c.get('questionFigureKey') else ''}{'  scheme-crop' if c.get('figureKey') else ''}")
    # Marks against the paper's own printed question totals ("Question 1 (25 marks)").
    printed = {}
    if 'listening' in s.papers:
        text = '\n'.join(p.get_text() for p in fitz.open(s.papers['listening']))
        ocr = os.path.join(REVIEW_DIR, 'ocr', f'{s.year}-{s.tag}-008.json')
        if os.path.exists(ocr):
            text += '\n' + '\n'.join(json.load(open(ocr, encoding='utf-8')).values())
        # "Question 1 (25 marks)", or before 2021 a bare "(25)" beside the question number.
        for m in re.finditer(r'Question\s+(\d)\s*[\s\S]{0,40}?\((\d+)(?:\s*marks)?\)', text):
            printed.setdefault(int(m.group(1)), int(m.group(2)))
    sums = {}
    for a in s.data['asks']:
        if a['paper'] != 'listening':
            continue
        q = int(s.question_number(a))
        choice = re.match(r'Q\d B\(', a['address'])
        key = (q, 'B' if choice else '')
        sums.setdefault(q, {}).setdefault(key, []).append(a['marks'])
    for q in sorted(set(printed) | set(sums)):
        got = sum(max(v) if k[1] == 'B' else sum(v) for k, v in sums.get(q, {}).items())
        flag = '' if printed.get(q) == got else '   <-- CHECK'
        print(f'  Listening Q{q}: paper prints {printed.get(q)}, asks give {got}{flag}')
    for r in s.data.get('readFromPage', []):
        print(f"  READ FROM PAGE ({r['booklet']} p{r['page']}, {r['readBy']}): {r['text']}")
    for n1, n2, page in crops_overlapping(s):
        print(f'  LOOK: the scheme crops of {n1} and {n2} overlap on page {page}: neither may show the other\'s answer')
    print(f'crops written to {crops_to}')


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--check':
        return check(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else '/private/tmp/music-check-crops')
    atlas = Atlas()
    cards, census, manifest = music_2025.build()
    MANIFEST.update(manifest)
    # Only the sittings listed in landed.json are built: a reading file still
    # being written beside them never reaches the deck by accident.
    landed = json.load(open(os.path.join(REVIEW_DIR, 'landed.json'), encoding='utf-8'))
    for tag in landed:
        s = Sitting(os.path.join(REVIEW_DIR, f'{tag}.json'))
        got, papers, covers = build_sitting(s, atlas)
        cards += got
        census['papers'] += papers
        census['covers'].update(covers)
        print(f'{s.year} {s.tag}: {len(got)} cards for {sum(p["expectedAsks"] for p in papers)} asks', file=sys.stderr)
    ids = [c['id'] for c in cards]
    if len(ids) != len(set(ids)):
        raise SystemExit('two cards share an id')
    census['note'] = ('Every numbered ask each sitting\'s booklets print, read page by page: 2025 Higher from '
                      'authored/music-2025-hl-review.json, every other sitting from authored/music-review/. Unnumbered, '
                      'unmarked "Preparatory work" tasks sit inside their question.')
    json.dump(census, open(CENSUS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(CENSUS, 'a').write('\n')
    json.dump(MANIFEST, open(FIG_MANIFEST, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(FIG_MANIFEST, 'a').write('\n')
    json.dump(cards, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(OUT, 'a').write('\n')
    print(f'{len(cards)} cards in all', file=sys.stderr)


if __name__ == '__main__':
    main()
