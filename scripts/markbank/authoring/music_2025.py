#!/usr/bin/env python3
"""Music, 2025 Higher Level: the review pack 1 prototype (treatments lane).

    python3 scripts/markbank/authoring/music_cards.py   (writes authored/music.json with every sitting)

ONE sitting, all three booklets: Listening (core) LC067ALP008EV, Composing
LC067ALP006EV and the Listening elective LC067ALP007EV, against the one scheme
LC067ALP000EV. The census of printed asks (authored/music-census.json, written
here) comes from authored/music-2025-hl-review.json, an inventory read off
every page of the three booklets, each ask checked against the text layer.

What a card is, by how the scheme gives marks:
  * an answer the scheme prints (17 asks): a point card, one row per answer;
  * an example list ("For example ... Any valid answer"): an `anyN` menu,
    open where the scheme says the list is not complete;
  * a mark rule with no answer ("Up to 4m for a correct description ...
    Partially correct answer = 1m/2m/3m"): the UNPRINTED_ANSWER row at the
    rule's marks, on the printed partial steps, the rule quoted beside it;
  * an answer printed as NOTATION, or in a music font the text layer cannot
    carry (2/4, 9/8, the flat of E-flat major): the scheme's own print as a
    solution crop held back until the reveal, beside the scheme's own words;
  * a quality band (Q5 B, Composing Section A, the Listening elective): the
    scheme's printed bands on the marking grid the languages use ('french');
  * Composing Section B (bands PLUS half a mark per correct bass note, a mark
    per chord): the scheme's bands and, beside them, each rate line as a grid
    line that counts items at the printed rate (FrenchCriterion.counted,
    music_lib.harmony_criteria), approved by Alex on 18 Nov.
Every listening card plays the SEC's own sound file. The SEC publishes the
test as TWO files and prints nowhere which question is on which; by length,
Questions 1-4 (55 marks) sit in file 1 (about 50 minutes) and 5-6 in file 2
(about 42): that split is an inference to confirm by listening once.

Nothing here is typed from memory: question words come from the inventory
(gated against the paper's text layer again below), answers and rule lines
from the scheme's .md, and every quoted line is checked against it here.
"""
import hashlib
import json
import os
import re
import sys
import unicodedata

import fitz

import music_lib

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
YEAR, LEVEL = 2025, 'hl'
REVIEW = os.path.join(ROOT, 'scripts/markbank/authored/music-2025-hl-review.json')
CENSUS = os.path.join(ROOT, 'scripts/markbank/authored/music-census.json')
PAPERS = {'listening': '2025-hl-008-paper.pdf', 'composing': '2025-hl-006-paper.pdf',
          'elective': '2025-hl-007-paper.pdf'}
SCHEME_PDF = os.path.join(ROOT, 'examiner-reports/music/schemes/2025-hl.pdf')
SCHEME_MD = os.path.join(ROOT, 'examiner-reports/music/schemes/2025-hl.md')
FIG_DIR = os.path.join(ROOT, 'public/exam-figures/music/markbank')
FIG_MANIFEST = os.path.join(ROOT, 'components/MarkBank/figures-music.json')
UNPRINTED = 'The scheme prints no answer for this part.'
ATTR_PAPER = 'SEC Leaving Certificate Music 2025 Higher Level examination paper — © State Examinations Commission'
ATTR_SCHEME = 'SEC Leaving Certificate Music 2025 Higher Level marking scheme — © State Examinations Commission'
AUDIO = {
    1: ('LC067ZLP045EV.mp3', 'Sound File 1 of 2', 'about 50 minutes'),
    2: ('LC067ZLP046EV.mp3', 'Sound File 2 of 2', 'about 42 minutes'),
}


def norm(text):
    text = unicodedata.normalize('NFKC', text or '').lower()
    text = re.sub('[‐-―]', '-', text)
    return re.sub(r'[^a-z0-9Ā-ſ]+', '', text)


SCHEME = norm(open(SCHEME_MD, encoding='utf-8').read())
PAPER_TEXT = {k: norm(''.join(p.get_text() for p in fitz.open(os.path.join(
    ROOT, 'examiner-reports/music/papers', f)))) for k, f in PAPERS.items()}


def scheme(text):
    """A line the card quotes from the scheme: refused unless the scheme prints it."""
    if norm(text) not in SCHEME:
        raise SystemExit(f'not in the 2025 HL scheme: {text!r}')
    return text


def paper(kind, text):
    if norm(text) not in PAPER_TEXT[kind]:
        raise SystemExit(f'not in the {kind} paper: {text!r}')
    return text


def quote(*lines):
    return 'The scheme reads: ' + ' '.join(f'“{scheme(l)}”' for l in lines)


# ------------------------------------------------------------- figures ----
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
    MANIFEST[key] = {'src': f'/exam-figures/music/markbank/{key}.png', 'md5': md5,
                     'alt': alt, 'attribution': attribution, **({'solution': True} if solution else {})}
    return key


# Where the scheme prints each notation or music-font answer, as page fractions,
# read off a render of the page (treatments/work/music/scheme-renders).
SCHEME_CROPS = {
    'Q1(g)': (14, [0.08, 0.085, 0.92, 0.32], 'the four missing notes printed on a treble stave, with the marking rule'),
    'Q2(c)': (15, [0.08, 0.285, 0.92, 0.41], 'the time signatures at X and Y, X printed in music notation, with "Allow 4/8"'),
    'Q3(a)': (16, [0.08, 0.205, 0.92, 0.41], 'the vocal line with a tick at each bar where the chord changes'),
    'Q5 A(d)': (18, [0.08, 0.385, 0.92, 0.52], 'the dance, its time signature in music notation, and the rhythm rule'),
    'Q6(d)': (21, [0.08, 0.13, 0.92, 0.24], 'the correct melody printed on a treble stave'),
    'Q6(e)': (21, [0.08, 0.235, 0.92, 0.285], 'the key, printed with a music-font flat sign'),
}


# ------------------------------------------------------------ listening ----
TOPIC_BY_Q = {1: 'music-2-15', 2: 'music-2-16', 3: 'music-2-14', 4: 'music-2-17', 6: 'music-2-7'}


def address_bits(address):
    m = re.match(r'Q(\d)\s*([AB])?\s*(\([a-z]+\))?(\([ivx]+\))?$', address)
    q, sec, letter, roman = int(m.group(1)), m.group(2), m.group(3), m.group(4)
    return q, sec, (letter or '').strip('()'), (roman or '').strip('()')


def listening_id(address):
    q, sec, letter, roman = address_bits(address)
    return '-'.join(x for x in ['mus-2025-hl-l', f'q{q}', (sec or '').lower(), letter, roman] if x)


def concept(text):
    words = sorted({w for w in re.findall(r"[a-z][a-z'’-]+", text.lower()) if len(w) > 3})
    return 'mus-' + '-'.join(words[:4])


def permitted(rule_marks, top):
    """The marks a rule-only answer can take: 0, the printed partial marks, full."""
    return sorted({0, top, *rule_marks})


def listening_rows(r):
    """The rows for one listening ask, by how the scheme gives its marks."""
    a = r['address']
    ans = r.get('schemeAnswers') or []
    # Rule-only asks: the scheme's rule, its partial marks, nothing to lift.
    RULES = {
        'Q1(h)': (['Up to 4m for a correct description of the texture of the music heard in the excerpt.',
                   'Partially correct answer = 1m/2m/3m'], [1, 2, 3]),
        'Q2(e)(ii)': (['Up to 3m for a description of the correct compositional technique identified with reference to the music in the excerpt',
                       'Partially correct description = 1m/2m'], [1, 2]),
        'Q3(d)': (['Up to 2m for describing how the words ‘for me’ are emphasized in the music towards the end of the excerpt.',
                   'Partially correct description = 1m'], [1]),
        'Q4(c)': (['Up to 2m for a description of a feature of Baroque music as heard in the excerpt',
                   'Partially correct answer = 1m'], [1]),
        'Q5 A(f)': (['Up to 4 marks for correct reference to the fusion in the excerpt',
                     'Partially correct answer = 1m/2m/3m'], [1, 2, 3]),
        'Q6(b)': (['Up to 3m for the quality of the description of the accompaniment in the excerpt.', 'Any valid answer',
                   'Partially correct answer = 1m/2m'], [1, 2]),
        'Q6(c)': (['Up to 3 marks for the quality of the description of the texture of the music in the excerpt.',
                   'A correct identification of the texture without a description = 1',
                   'Partially correct answer = 1m/2m'], [1, 2]),
    }
    if a in RULES:
        lines, partial = RULES[a]
        top = r['schemeMarks']
        return [{'id': 'r-1', 'kind': 'criterion', 'verbatim': UNPRINTED, 'marks': top,
                 'permittedMarks': permitted(partial, top), 'unprinted': True,
                 'contextNote': quote(*lines)}], {'kind': 'fixed'}
    # Example menus: "For example: ... Any valid answer".
    MENUS = {
        'Q1(e)': (2, 2, True, ['Up to 2m for each of two valid differences between the music in excerpt 1 and the music in excerpt 2',
                               'Answers must refer to both excerpts and the same point of difference for full marks.',
                               'Any valid difference', 'Partially correct difference = 1m'], 'Excerpt 1 — Excerpt 2'),
        'Q1(f)': (3, 2, True, ['Up to 2m each for identification of each of three features of the music in Excerpt 3',
                               'Any valid answer', 'Partially correct answer = 1m'], 'Features of the music in Excerpt 3'),
        'Q3(b)': (2, 1, True, ['1m each for identification of each of two features of the vocal music in lines 1 – 5 of the excerpt', 'Any valid answer'], 'Features of the vocal music'),
        'Q4(b)': (1, 2, True, ['Up to 2m for a correct identification of a feature of the music played by the continuo in the excerpt',
                               'Any valid answer', 'Partially correct answer = 1m'], 'A feature of the continuo'),
        'Q5 A(b)': (2, 1, True, ['1m for each of two features of sean-nós singing heard in the excerpt'], 'Features of sean-nós singing'),
        'Q5 A(e)': (2, 1, False, ['Any 2 correct instruments'], 'Instruments'),
        'Q6(g)': (2, 2, True, ['Up to 2m each for any two features of the vocal music in the excerpt.',
                               'Partially correct answer = 1m'], 'Features of the vocal music'),
        'Q6(h)': (2, 2, True, ['Up to 2m for each of two valid differences between the music in excerpt 4 and the music in excerpt 5',
                               'Answers must refer to both excerpts and the same point of difference for full marks.',
                               'Any valid answer', 'Partially correct answer = 1m'], 'Excerpt 4 — Excerpt 5'),
    }
    if a in MENUS:
        claim, per, open_list, lines, label = MENUS[a]
        # A difference is printed in two columns, one per excerpt: the
        # option names both halves, and each half is the scheme's own cell.
        options = [x['text'].replace(' | ', ' — ') for x in ans]
        options = [re.sub(r'Excerpt \d: ', '', o) for o in options]
        return [{'id': 'r-1', 'kind': 'anyN', 'verbatim': label, 'marks': None,
                 'openList': open_list, 'contextNote': quote(*lines),
                 'group': {'claimMax': claim, 'perOption': per, 'options': options}}], {'kind': 'fixed'}
    if a == 'Q3(c)':
        return [{'id': 'r-1', 'kind': 'anyN', 'verbatim': 'A recording technique', 'marks': None, 'openList': True,
                 'contextNote': quote('1m for correct identification of a recording technique used in the excerpt'),
                 'group': {'claimMax': 1, 'perOption': 1, 'options': [x['text'] for x in ans]}},
                {'id': 'r-2', 'kind': 'criterion', 'verbatim': UNPRINTED, 'marks': 2, 'permittedMarks': [0, 1, 2],
                 'unprinted': True,
                 'contextNote': quote('Up to 2m for a description of the recording technique identified with reference to the music in the excerpt',
                                      'Partially correct description = 1m')}], {'kind': 'fixed'}
    # Notation and music-font answers: the scheme's print beside its words.
    if a == 'Q1(g)':
        return [{'id': 'r-1', 'kind': 'criterion', 'verbatim': scheme('Mark the first four notes from left to right.'),
                 'marks': 4, 'permittedMarks': [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4],
                 'contextNote': quote('Pitch 1 X 4.', 'If the pitch is incorrect but the note moves in the correct direction from the preceding note allow 0.5')
                 + ' The scheme prints the four notes on a stave: its print is shown on this card.'}], {'kind': 'fixed'}
    if a == 'Q3(a)':
        return [{'id': 'r-1', 'kind': 'criterion',
                 'verbatim': scheme('1m for each chord change correctly identified in bars 2, 3 and 4'),
                 'marks': 3, 'permittedMarks': [0, 1, 2, 3],
                 'contextNote': 'The scheme marks the chord changes with ticks on the score: its print is shown on this card.'}], {'kind': 'fixed'}
    if a == 'Q2(c)':
        return [{'id': 'r-1', 'kind': 'criterion', 'verbatim': scheme('Correct time signature at X'), 'marks': 1,
                 'contextNote': 'The scheme prints this time signature in music notation: its print is shown on this card. '
                                + quote('Allow 4/8')},
                {'id': 'r-2', 'kind': 'point', 'verbatim': scheme('Correct time signature at Y = 5/8'), 'marks': 1}], {'kind': 'fixed'}
    if a == 'Q5 A(d)':
        return [{'id': 'r-1', 'kind': 'point', 'verbatim': scheme('Slip Jig'), 'marks': 1},
                {'id': 'r-2', 'kind': 'point', 'verbatim': 'Give its time signature', 'marks': 1, 'ask': True,
                 'contextNote': 'The scheme prints the time signature in music notation: its print is shown on this card.'},
                {'id': 'r-3', 'kind': 'criterion', 'verbatim': scheme('Any correct bar of slip jig rhythm'), 'marks': 2}], {'kind': 'fixed'}
    if a in ('Q6(d)', 'Q6(e)'):
        return [{'id': 'r-1', 'kind': 'point', 'verbatim': r['questionText'], 'marks': r['schemeMarks'], 'ask': True,
                 'contextNote': 'The scheme prints its answer in music notation: its print is shown on this card.'}], {'kind': 'fixed'}
    if a == 'Q2(e)(i)':
        return [{'id': 'r-1', 'kind': 'point', 'verbatim': scheme('canon'), 'marks': 1,
                 'contextNote': quote('1m for correct identification of the compositional technique, canon, used in the excerpt')}], {'kind': 'fixed'}
    if a == 'Q4(e)':
        return [{'id': 'r-1', 'kind': 'criterion', 'verbatim': scheme(ans[0]['text']), 'marks': 3,
                 'permittedMarks': [0, 1, 2, 3],
                 'contextNote': 'The scheme gives this “For example:”. '
                                + quote('Up to 3m for a description of Tierce de Picardie with reference to the music in the excerpt',
                                        'Partially correct answer = 1m/2m')}], {'kind': 'fixed'}
    if a == 'Q4(d)':
        return [{'id': f'r-{i + 1}', 'kind': 'point', 'verbatim': scheme(x['text']), 'marks': 0.5} for i, x in enumerate(ans)] , {'kind': 'fixed'}
    if r['markingShape'] == 'points':
        return [{'id': f'r-{i + 1}', 'kind': 'point', 'verbatim': scheme(x['text']), 'marks': x['marks']}
                for i, x in enumerate(ans)], {'kind': 'fixed'}
    raise SystemExit(f'no treatment for listening {a}')


def listening_card(r):
    a = r['address']
    q, sec, letter, roman = address_bits(a)
    topic = TOPIC_BY_Q.get(q) or ('music-2-2' if sec == 'A' else 'music-2-13')
    file_no = 1 if q <= 4 else 2
    fileid, which, length = AUDIO[file_no]
    question = paper('listening', r['questionText'])
    stem = ' '.join(x for x in [r.get('questionContext'), r.get('excerptLine')] if x)
    card = {
        'id': listening_id(a), 'subjectId': 'music', 'level': 'higher', 'year': YEAR,
        'section': 'L', 'topicId': topic, 'conceptId': concept(question),
        'questionRef': f'2025 HL Listening {a}', 'questionText': question,
        'totalMarks': r['schemeMarks'],
        'sourceMaterial': {
            'kind': 'source-text', 'label': 'LISTENING (CORE)', 'title': f'Listening — Question {q}',
            'pages': r['pages'], 'regions': [{'p': p, 'r': r['crop']} for p in r['pages'][:1]],
            'attribution': f'{ATTR_PAPER}.', 'sourceLabel': 'Listening',
            'presentationNote': 'The question as the listening booklet prints it. Play the recording, then answer.'},
    }
    if stem:
        card['stem'] = stem
    if r.get('needsRecording'):
        card['audioMaterial'] = {
            'kind': 'source-audio', 'label': f'Question {q} · {(r.get("excerptLine") or "").split(",")[0]}'.strip(' ·'),
            'title': '2025 Music · Listening test (Higher and Ordinary)',
            'playbackUrl': f'https://www.examinations.ie/archive/exampapers/2025/{fileid}',
            'secFileid': fileid,
            'canonicalUrl': f'https://www.examinations.ie/archive/exampapers/2025/{fileid}',
            'attribution': '© State Examinations Commission.',
            'presentationNote': f'The SEC publishes this test as two sound files. This is {which} ({length}). '
                                'Use the player to move to the question and replay the excerpt.'}
    rows, tariff = listening_rows(r)
    card['rows'], card['tariffModel'] = rows, tariff
    if r.get('needsFigure') and r.get('figureCrop'):
        card['questionFigureKey'] = crop(os.path.join(ROOT, 'examiner-reports/music/papers', PAPERS['listening']),
                                         r['page'], r['figureCrop'], f'music-2025-HL-L-{listening_id(a)[12:]}-score',
                                         f'The outline score printed with Listening {a} in the 2025 Higher Level paper, as the SEC set it.',
                                         ATTR_PAPER)
        card['questionFigureIncludesPrompt'] = False
    if a in SCHEME_CROPS:
        page, box, what = SCHEME_CROPS[a]
        card['figureKey'] = crop(SCHEME_PDF, page, box, f'music-2025-HL-scheme-p{page}-{listening_id(a)[12:]}',
                                 f'The marking scheme’s printed answer for Listening {a}: {what}, cropped from page {page} of the scheme.',
                                 ATTR_SCHEME, solution=True)
    return card


# ---------------------------------------------------------------- grids ----
def grid_card(cid, ref, section, topic, question, marks, criterion, pages, source, stem=None, note=None):
    card = {'id': cid, 'kind': 'rubric', 'subjectId': 'music', 'level': 'higher', 'year': YEAR,
            'section': section, 'topicId': topic, 'conceptId': concept(question), 'questionRef': ref,
            'questionText': question, 'totalMarks': marks, 'schemePages': pages,
            'rubric': {'system': 'french', 'taskRequirements': [], 'criteria': [criterion],
                       'markingGuideNote': scheme(note or criterion['label'])},
            'sourceMaterial': source}
    if stem:
        card['stem'] = stem
    return card


def bands_from_table(page, first_label_only=False):
    """[(descriptor lines, [marks])] for one band table, high to low, as printed."""
    tab = fitz.open(SCHEME_PDF)[page - 1].find_tables().tables[0]
    out = []
    for row in tab.extract():
        cells = [c for c in row if c]
        # The elective's first row is Element 1, "Name of topic", which the
        # scheme gives no marks ("-"); its 100 is the table's total column.
        if any((c or '').strip() == 'Name of topic' for c in row):
            continue
        marks_cell = next((c for c in reversed(cells) if re.fullmatch(r'[\d\s–\-‐/\n]+', c or '') and re.search(r'\d', c)), None)
        desc = next((c for c in cells if '•' in c or re.search(r'[a-z]{4}', c or '')), None)
        if not marks_cell or not desc or 'Descriptors' in desc:
            continue
        nums = [int(n) for n in re.findall(r'\d+', marks_cell)]
        lines, current = [], ''
        for raw in desc.split('\n'):
            raw = raw.strip()
            if not raw:
                continue
            if raw.startswith('•'):
                if current:
                    lines.append(current)
                current = raw.lstrip('• ').strip()
            elif current and raw[:1].islower():
                current += ' ' + raw
            else:
                if current:
                    lines.append(current)
                current = raw
        if current:
            lines.append(current)
        out.append((lines, list(range(min(nums), max(nums) + 1))))
    return out


def composing_a(r):
    q = int(r['address'][-1])
    page = {1: 3, 2: 4, 3: 5}[q]
    bands = []
    extra = []
    for lines, marks in bands_from_table(page):
        if lines == ['No text inserted']:
            extra.append(scheme('No text inserted'))
            continue
        bands.append({'label': scheme(lines[0]), 'marks': marks, 'guidance': [scheme(l) for l in lines[1:]]})
    question = paper('composing', r['questionText'])
    criterion = {'id': 'melody', 'label': scheme('SECTION A – MELODY COMPOSITION (40 marks)'), 'maxMarks': 40,
                 'permittedMarks': list(range(41)), 'guidance': extra + ([scheme('No text inserted 0')] if False else []),
                 'bands': bands}
    source = {'kind': 'source-text', 'label': 'COMPOSING · SECTION A', 'title': f'Section A — Question {q}',
              'pages': r['pages'], 'attribution': f'{ATTR_PAPER}.', 'sourceLabel': 'Composing',
              'presentationNote': 'The question and its printed opening, exactly as the composing booklet sets them.'}
    return grid_card(f'mus-2025-hl-c-a-q{q}', f'2025 HL Composing Section A Q{q}', 'A',
                     {1: 'music-1-10', 2: 'music-1-11', 3: 'music-1-12'}[q], question, 40, criterion, [page], source,
                     stem=paper('composing', 'Answer one question only in this section.'))


def composing_b(r):
    """Composing Section B: the scheme's bands PLUS lines counted at a printed
    rate ("0.5 mark per correct bass note ... (0.5 X 20)"), on the grid line
    that counts items (FrenchCriterion.counted), each line as printed."""
    q = int(r['address'][-1])
    page = {4: 6, 5: 7, 6: 8}[q]
    criteria = music_lib.harmony_criteria(SCHEME_PDF, page, q)
    for k in criteria:
        k['label'] = scheme(k['label'])
        k['guidance'] = [scheme(g) for g in k['guidance']]
        for b in k.get('bands', []):
            b['label'] = scheme(b['label'])
            b['guidance'] = [scheme(g) for g in b['guidance']]
    # The chord-progression rules print under Question 5's table, on its page.
    rules = []
    if q == 5:
        top = fitz.open(SCHEME_PDF)[page - 1].find_tables().tables[0].bbox[3]
        rules = [scheme(x) for x in music_lib.text_blocks_below(SCHEME_PDF, page, top)]
    # The title and each bullet are checked one by one: the page prints the
    # (unmarked) preparatory work between the title and the bullets.
    question = r['questionText']
    for piece in question.split(' • '):
        paper('composing', piece)
    source = {'kind': 'source-text', 'label': 'COMPOSING · SECTION B', 'title': f'Section B — Question {q}',
              'pages': r['pages'], 'attribution': f'{ATTR_PAPER}.', 'sourceLabel': 'Composing',
              'presentationNote': 'The question, its printed opening and the chords it gives, exactly as the composing booklet sets them.'}
    card = {'id': f'mus-2025-hl-c-b-q{q}', 'kind': 'rubric', 'subjectId': 'music', 'level': 'higher', 'year': YEAR,
            'section': 'B', 'topicId': {4: 'music-1-14', 5: 'music-1-13', 6: 'music-1-15'}[q],
            'conceptId': concept(question), 'questionRef': f'2025 HL Composing Section B Q{q}',
            'questionText': question, 'totalMarks': 60, 'schemePages': [page],
            'rubric': {'system': 'french', 'taskRequirements': rules, 'criteria': criteria,
                       'markingGuideNote': scheme('SECTION B – HARMONY (60 marks)')},
            'sourceMaterial': source,
            'stem': paper('composing', 'Answer one question only in this section.')}
    if sum(k['maxMarks'] for k in criteria) != 60:
        raise SystemExit(f'Composing B Q{q}: criteria make {sum(k["maxMarks"] for k in criteria)}, not 60')
    return card


def q5b(r):
    roman = re.search(r'\(([ivx]+)\)', r['address']).group(1)
    bands = []
    for b in r['schemeBands']:
        nums = [int(n) for n in re.findall(r'\d+', b['marks'])]
        bands.append({'label': scheme(b['marks']), 'marks': list(range(min(nums), max(nums) + 1)),
                      'guidance': [scheme(d) for d in b['descriptors']]})
    criterion = {'id': 'quality', 'label': scheme('Up to 10 marks for quality of answers and knowledge of topic chosen.'),
                 'maxMarks': 10, 'permittedMarks': list(range(11)), 'guidance': [], 'bands': bands}
    question = paper('listening', r['questionText'])
    source = {'kind': 'source-text', 'label': 'LISTENING (CORE) · QUESTION 5 B', 'title': 'Question 5 B',
              'pages': [r['page']], 'regions': [{'p': r['page'], 'r': r['crop']}], 'attribution': f'{ATTR_PAPER}.',
              'sourceLabel': 'Listening', 'presentationNote': 'The choice of questions as the listening booklet prints it.'}
    return grid_card(f'mus-2025-hl-l-q5-b-{roman}', f'2025 HL Listening Q5 B({roman})', 'L', 'music-2-13', question, 10,
                     criterion, [19], source, stem=paper('listening', 'Answer one of the following:'))


def elective(rows):
    parts = []
    for r in rows:
        label = {'Q1': '1.', 'Q2': '2.', 'Q3': '3.', 'Q4(a)': '4. (a)', 'Q4(b)': '(b)'}[r['address']]
        parts.append(f"{label} {paper('elective', r['questionText'])}")
    bands = []
    for lines, marks in bands_from_table(23):
        if lines and lines[0] == 'Name of topic':
            continue
        bands.append({'label': scheme(lines[0]), 'marks': marks, 'guidance': [scheme(l) for l in lines[1:]]})
    criterion = {'id': 'elements-2-4', 'label': scheme('Listening – Higher level - Elective'), 'maxMarks': 100,
                 'permittedMarks': list(range(101)), 'guidance': [scheme('Name of topic -')], 'bands': bands}
    source = {'kind': 'source-text', 'label': 'LISTENING ELECTIVE', 'title': 'Listening elective — Questions 1 to 4',
              'pages': [2, 3], 'attribution': f'{ATTR_PAPER}.', 'sourceLabel': 'Elective',
              'presentationNote': 'The questions exactly as the elective booklet prints them, about your own chosen topic.'}
    return grid_card('mus-2025-hl-e-q1-q4', '2025 HL Elective Q1–Q4(b)', 'E', 'music-2-8', ' '.join(parts), 100,
                     criterion, [23], source, stem=paper('elective', 'Answer all questions.'))


# ---------------------------------------------------------------- build ----
def build():
    """(cards, census, figure manifest) for 2025 Higher; music_cards.py adds the other sittings."""
    review = json.load(open(REVIEW, encoding='utf-8'))
    numbered = [r for r in review if not r.get('unnumbered')]
    cards = []
    section_b = []
    census = {'papers': [], 'covers': {}}
    by_paper = {'Listening': [], 'Composing': [], 'Elective': []}
    for r in numbered:
        if r['paper'] == 'listening':
            cid = listening_id(r['address'])
            by_paper['Listening'].append({'id': cid, 'questionRef': f"2025 HL Listening {r['address']}"})
            cards.append(q5b(r) if r['markingShape'] == 'band' else listening_card(r))
        elif r['paper'] == 'composing':
            m = re.match(r'Section ([AB]) Q(\d)', r['address'])
            cid = f'mus-2025-hl-c-{m.group(1).lower()}-q{m.group(2)}'
            by_paper['Composing'].append({'id': cid, 'questionRef': f"2025 HL Composing {r['address']}"})
            if m.group(1) == 'A':
                cards.append(composing_a(r))
            else:
                section_b.append(composing_b(r))
        else:
            cid = 'mus-2025-hl-e-' + r['address'].lower().replace('(', '-').replace(')', '')
            by_paper['Elective'].append({'id': cid, 'questionRef': f"2025 HL Elective {r['address']}"})
    elective_rows = [r for r in numbered if r['paper'] == 'elective']
    cards.append(elective(elective_rows))
    # Composing Section B, carded on the counted grid line (19 Nov): after the
    # 46 cards that were live before it, so those are emitted exactly as they were.
    cards.extend(section_b)
    census['covers']['mus-2025-hl-e-q1-q4'] = [a['id'] for a in by_paper['Elective']]
    for name, asks in by_paper.items():
        census['papers'].append({'year': YEAR, 'level': 'higher', 'paper': name,
                                 'expectedAsks': len(asks), 'asks': asks})
    census['note'] = ('Every numbered ask the three 2025 Higher Level booklets print, read page by page '
                      '(authored/music-2025-hl-review.json). The three unnumbered "Preparatory work" tasks of '
                      'Composing Section B carry no marks and sit inside their question.')
    print(f'{len(cards)} cards for {sum(len(a) for a in by_paper.values())} asks', file=sys.stderr)
    return cards, census, MANIFEST


def main():
    cards, census, _ = build()
    json.dump(census, open(CENSUS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(CENSUS, 'a').write('\n')
    json.dump(MANIFEST, open(FIG_MANIFEST, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(FIG_MANIFEST, 'a').write('\n')
    json.dump(cards, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
