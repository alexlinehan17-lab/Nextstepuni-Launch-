#!/usr/bin/env python3
"""2026 LCVP: original-page selections after the independent 64-page sweep.

This module adds this sitting only. It never reruns the legacy all-years parser.
The manual source/task ledger is independent of these selectors. Every prompt,
model and allocation below is selected from hash-locked original SEC PDFs.
"""
from pathlib import Path
import hashlib
import json
import re
import sys
import fitz

ROOT = Path(__file__).resolve().parents[3]
REVIEW = ROOT / 'scripts/markbank/authoring/lcvp/2026-cl-main-review.json'
PAPER = 'paper-trail-corpus/exampapers/2026/LC462CLP000EV.pdf'
SCHEME = 'paper-trail-corpus/markingschemes/2026/LC462CLP000EV.pdf'
HASHES = {PAPER: 'c1b319abcee8521b3c272f87b0230768a9e5082dc2526958b16df1203e35bd50',
          SCHEME: '49251a890b2998d216ed02dacf5edd657c0918984a19f09a4db4f5a7579efb4e'}
VIDEO_URL = 'https://www.examinations.ie/archive/exampapers/2026/LC462CLP031EV.mov'


def tidy(value):
    return ' '.join(value.split())


def select(value, start, end=None, include=False):
    assert value.count(start) == 1, (start, value[:120])
    tail = value.split(start, 1)[1]
    if end:
        assert end in tail, end
        tail = tail.split(end, 1)[0]
    return tidy((start if include else '') + tail)


def documents():
    for path, expected in HASHES.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
    return fitz.open(ROOT / PAPER), fitz.open(ROOT / SCHEME)


def page_text(doc, number):
    page = doc[number - 1]
    # Find the actual footer; do not truncate variable-height pages by guessing.
    cut = page.rect.height - 15
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            value = tidy(''.join(span['text'] for span in line['spans']))
            if line['bbox'][1] > page.rect.height * .82 and (
                re.fullmatch(r'\d{1,2}', value)
                or value.startswith('Leaving Certificate Vocational Programme')
                or value == 'Link Modules Examination'
            ):
                cut = min(cut, line['bbox'][1] - 2)
    return tidy(page.get_text(clip=fitz.Rect(0, 15, page.rect.width, cut), sort=True))


def numbered(value, expected):
    matches = list(re.finditer(r'(?<!\w)(\d+)\.\s+', value))
    assert [int(m[1]) for m in matches] == list(range(1, expected + 1)), (expected, value)
    return [tidy(value[m.end():matches[i + 1].start() if i + 1 < len(matches) else len(value)])
            for i, m in enumerate(matches)]


def split_heads(value, pattern, expected):
    matches = list(re.finditer(pattern, value))
    assert [m[1] for m in matches] == expected, (expected, [m[1] for m in matches])
    return {m[1]: tidy(value[m.end():matches[i + 1].start() if i + 1 < len(matches) else len(value)])
            for i, m in enumerate(matches)}


def scheme_parts(doc):
    source = ' '.join(page_text(doc, n) for n in range(4, 22))
    sections = split_heads(source, r'Section ([ABC])\s+', list('ABC'))
    out = {}
    for section, value in sections.items():
        questions = split_heads(value, r'Q\.\s*(\d+)\s+',
                                [str(n) for n in range(1, {'A': 8, 'B': 3, 'C': 7}[section] + 1)])
        for q, block in questions.items():
            if section == 'A' or (section == 'B' and q == '1'):
                out[(section, int(q), None, None)] = block
            elif section == 'B':
                for roman, part in split_heads(block, r'\((i{1,3})\)\s+', ['i', 'ii', 'iii']).items():
                    out[(section, int(q), None, roman)] = part
            else:
                letters = split_heads(block, r'\(([abcd])\)\s+', list('abcd'))
                for letter, part in letters.items():
                    if q == '7' and letter == 'b':
                        for roman, sub in split_heads(part, r'\((i{1,2})\)\s+', ['i', 'ii']).items():
                            out[(section, 7, letter, roman)] = sub
                    else:
                        out[(section, int(q), letter, None)] = part
    assert len(out) == 44
    return out


def point(key, value, marks=None, note=''):
    row = dict(id=key, kind='point', verbatim=tidy(value), marks=marks)
    if note:
        row['contextNote'] = note
    return row


def criterion(key, label, count, steps, guidance):
    totals = {0}
    for _ in range(count):
        totals = {a + b for a in totals for b in steps}
    row = dict(id=key, kind='criterion', verbatim=tidy(label), marks=count * steps[-1],
               permittedMarks=sorted(totals), contextNote=guidance)
    if count > 1:
        row['parts'] = [dict(id=f'response-{i}', verbatim=f'Response {i}', marks=steps[-1],
                             permittedMarks=steps) for i in range(1, count + 1)]
    return row


def model_pool(block, expected):
    models = numbered(block, expected)
    if re.fullmatch(r'Etc\.?', models[-1], re.I):
        return models[:-1], True
    return models, False


def menu(block, count, per, expected):
    models, open_list = model_pool(block, expected)
    return [dict(id='responses', kind='anyN', verbatim=block.split('1.', 1)[0].strip(),
                 marks=count * per, openList=True,
                 group=dict(claimMax=count, perOption=per, options=models),
                 contextNote=f'Choose any {count} distinct responses across the complete original pool. '
                 + f'Each response receives {per} or 0 marks; no unprinted partial step is inferred. '
                 + ('The source also prints “Etc.”; equivalent valid responses remain possible.' if open_list else ''))]


def partial(block, count, per, expected, extra=''):
    models, open_list = model_pool(block, expected)
    prefix = block.split('1.', 1)[0].strip()
    guide = f'Choose any {count} distinct responses across the full pool. Original allocation: {prefix} '
    guide += 'Each response follows the printed component ladder; do not count the same expansion twice. '
    guide += extra + ' Complete original guidance: ' + ' | '.join(f'{i}. {v}' for i, v in enumerate(models, 1))
    if open_list:
        guide += ' The source also prints “Etc.”.'
    return [criterion('responses', prefix, count, list(range(per + 1)), guide)]


PAGES = {('A', q, None, None): n for q, n in enumerate([4, 4, 4, 5, 5, 6, 7, 8], 1)}
PAGES.update({('B', 1, None, None): 10})
PAGES.update({('B', q, None, r): 9 + q for q in [2, 3] for r in ['i', 'ii', 'iii']})
PAGES.update({('C', q, letter, None): 16 + (q - 1) * 3 + {'a': 0, 'b': 0, 'c': 1, 'd': 2}[letter]
              for q in range(1, 8) for letter in 'abcd'})
PAGES.pop(('C', 7, 'b', None))
PAGES.update({('C', 7, 'b', r): 34 for r in ['i', 'ii']})


def question(doc, key):
    section, q, letter, roman = key
    value = page_text(doc, PAGES[key])
    if section in ['A', 'B']:
        value = re.split(r'Q\.\s*' + str(q) + r'\s+', value, maxsplit=1)[1]
        value = re.split(r'Q\.\s*\d+\s+', value, maxsplit=1)[0]
    else:
        value = select(value, '(' + letter + ')')
        value = re.split(r'\([abcd]\)\s+', value, maxsplit=1)[0]
    if roman:
        value = select(value, '(' + roman + ')')
        value = re.split(r'\(i{1,3}\)\s+', value, maxsplit=1)[0]
    value = re.sub(r'\(\d+\s+marks?\)', '', value)
    return tidy(value)


def source(pages, kind='source-question', title='Original question'):
    return dict(kind=kind, label='OFFICIAL SOURCE', title=title, pages=pages,
                attribution='SEC LCVP Link Modules 2026 Common Level — © State Examinations Commission.',
                presentationNote='Read the complete original source and question in context.')


def build():
    paper, scheme = documents()
    blocks = scheme_parts(scheme)
    rows, totals, topics = {}, {}, {}
    def put(key, mark, topic, value):
        rows[key], totals[key], topics[key] = value, mark, topic
    def a(n): return ('A', n, None, None)
    def b(n, r=None): return ('B', n, None, r)
    def c(n, l, r=None): return ('C', n, l, r)
    put(a(1), 1, '1-1', [point('business-name', select(blocks[a(1)], '1 mark'), 1)])
    models = numbered(blocks[a(2)], 3)
    put(a(2), 2, '1-1', [point(f'model-{i}', v, note=(
        'The source prints a total of 2 marks and these three models, but no response quota, '
        'component allocation or partial ladder. Numeric scoring is held; compare the complete response.'
        if i == 1 else '')) for i, v in enumerate(models, 1)])
    for n, count, per, expected in [(3, 3, 1, 5), (4, 2, 1, 4), (5, 2, 2, 6), (6, 3, 2, 5)]:
        put(a(n), count * per, '1-0' if n == 3 else '1-1', menu(blocks[a(n)], count, per, expected))
    for n, expected in [(7, 4), (8, 12)]:
        put(a(n), 6, '0-0' if n == 7 else '1-0', partial(blocks[a(n)], 3, 2, expected))
    put(b(1), 6, '1-2', partial(blocks[b(1)], 3, 2, 7,
        'The literal source “3m @ 2 (1+1)” is retained; the question asks for three sources and totals six.'))
    put(b(2, 'i'), 2, '1-2', menu(blocks[b(2, 'i')], 2, 1, 10))
    put(b(2, 'ii'), 6, '1-2', partial(blocks[b(2, 'ii')], 3, 2, 8))
    put(b(2, 'iii'), 4, '1-3', menu(blocks[b(2, 'iii')], 4, 1, 10))
    put(b(3, 'i'), 6, '1-2', menu(blocks[b(3, 'i')], 3, 2, 15))
    put(b(3, 'ii'), 4, '1-2', partial(blocks[b(3, 'ii')], 2, 2, 8))
    put(b(3, 'iii'), 2, '1-3', [criterion('action-plan-content', 'Construct an action plan', 2, [0, 1],
        'The source allocates 2@1m to content and explicitly states NO MARKS FOR HEADINGS. '
        'Two valid content points are claimable; selecting a heading alone earns no mark. '
        'The complete original scaffold is: ' + ' | '.join(numbered(blocks[b(3, 'iii')], 8))
        + '. No completed model action plan is printed; none has been invented.')])

    specifications = [
        (1, 'a', 2, 2, 4, False, '0-1'), (1, 'b', 2, 2, 6, True, '0-1'),
        (1, 'c', 4, 2, 10, True, '0-1'), (1, 'd', 3, 3, 7, True, '0-0'),
        (2, 'a', 2, 2, 15, False, '1-0'), (2, 'b', 2, 2, 8, True, '1-0'),
        (2, 'd', 4, 2, 8, True, '1-0'), (3, 'a', 2, 2, 10, False, '1-1'),
        (3, 'c', 3, 3, 11, True, '1-1'), (3, 'd', 4, 2, 9, True, '1-1'),
        (4, 'a', 2, 2, 8, False, '0-3'), (4, 'b', 2, 2, 7, True, '0-3'),
        (4, 'd', 3, 3, 5, True, '1-4'), (5, 'b', 2, 2, 8, True, '0-2'),
        (6, 'a', 2, 2, 4, False, '1-1'), (6, 'b', 4, 1, 17, False, '1-1'),
        (6, 'c', 4, 2, 8, True, '1-1'), (6, 'd', 3, 3, 8, True, '1-1'),
        (7, 'a', 4, 1, 9, False, '1-3'), (7, 'c', 3, 2, 6, True, '1-3'),
    ]
    for q, letter, count, per, expected, has_partial, topic in specifications:
        key = c(q, letter)
        put(key, count * per, topic, (partial if has_partial else menu)(blocks[key], count, per, expected))
    key = c(2, 'c')
    pool = numbered(blocks[key], 8)
    guidance = 'Choose THREE different barriers. Each response requires the barrier name (1) and how to overcome THAT barrier (1+1). No repetition of descriptions. Complete original paired profiles: ' + ' | '.join(pool)
    barrier_rows = []
    for i in range(1, 4):
        row = criterion(f'barrier-{i}', 'Name of barrier', 1, [0, 1, 2, 3], guidance if i == 1 else 'Use a different barrier and its matching solution. Name 1; explanation 0–2 on the printed 1+1 allocation.')
        row['parts'] = [dict(id='name', verbatim='Name of barrier', marks=1, permittedMarks=[0, 1]),
                        dict(id='overcome', verbatim='Description of how to overcome', marks=2, permittedMarks=[0, 1, 2])]
        barrier_rows.append(row)
    put(key, 9, '1-0', barrier_rows)
    key = c(3, 'b')
    model = select(blocks[key], 'An inclusive workplace', include=True)
    put(key, 4, '0-0', [criterion('definition', 'Mix of people', 1, [0, 1],
        'One opening concept: “Mix of people” OR “Not discriminated”, not both. Complete original guidance: ' + model),
        criterion('expansions', 'Everyone is equal/respected', 3, [0, 1],
        'THREE valid expansions of the same definition, 1 mark each; use the full original guidance above. The opening and expansions are different required components.')])
    key = c(4, 'c')
    allocation = select(blocks[key], 'Summary of marks:', 'Total')
    components = re.findall(r'(.*?)\s+1m', allocation)
    assert len(components) == 8, components
    put(key, 8, '0-3', [point(f'email-{i}', component, 1,
        'Required component of YOUR placement request email, 1 or 0 marks. The source prints this eight-component grid, not a model email; none is invented.' if i == 1 else '')
        for i, component in enumerate(components, 1)])
    key = c(5, 'a')
    put(key, 4, '0-2', [criterion('career', select(blocks[key], 'Any career mentioned', '(0/2m)', True), 1, [0, 2],
        'Choose your career. The next required row must name a valid qualification/training for THIS SAME career; no career combinations or invented models.'),
        criterion('qualification', select(blocks[key], 'One valid qualification/training', '(0/2m)', True), 1, [0, 2],
        'Required qualification/training matching the career named above; 2 or 0 marks.')])
    key = c(5, 'c')
    put(key, 9, '0-2', [criterion('experience-name', 'name the experience', 1, [0, 1],
        'Choose ONE out-of-school experience you actually used to investigate the SAME career. All original activity models: ' + ' | '.join(numbered(blocks[key], 7))),
        criterion('experience-explanation', 'Explain the experience', 1, [0, 1, 2],
        'Explain that SAME experience using the source’s 1m + 1m allocation.'),
        criterion('information-learned', '2 pieces of information', 2, [0, 1, 2, 3],
        'Two pieces learned from that SAME experience, 3 marks each (1+1+1). The source does not print a personal experience or learned-information model; none is invented.')])
    key = c(5, 'd')
    put(key, 8, '0-0', [point(f'training-profile-{i}', value, note=(
        'Numeric scoring held: the source prints a total of 8 marks, “Type of Training 2@2m (1+1)” and “2 Benefits 2@1m”. '
        'Those listed components total 6, not 8. Both allocations are preserved; no extra marks or revised per-benefit tariff are inferred. '
        'Compare TWO complete training/benefit profiles from the full pool; confidence only pending authoritative clarification.' if i == 1 else ''))
        for i, value in enumerate(numbered(blocks[key], 6), 1)])
    key = c(7, 'b', 'i')
    definition = select(blocks[key], 'Market research involves', include=True)
    put(key, 2, '1-3', [criterion('definition', definition, 2, [0, 1],
        'Original allocation 2@1m. Explain the term using two valid pieces of the complete source definition. Source emphasis identifies gathering, analysing and decisions; it does not create a three-part quota.')])
    key = c(7, 'b', 'ii')
    put(key, 4, '1-3', partial(blocks[key], 2, 2, 6))
    key = c(7, 'd')
    models = numbered(blocks[key], 9)
    put(key, 9, '1-3', [criterion('evaluation', 'Explain the methods you would use', 3, [0, 1, 2, 3],
        'Required selection: ONE group method, ONE personal method, and ONE other (group OR personal). Each receives 3@1, not three interchangeable responses with no category requirement. Complete original guidance: ' + ' | '.join(models))])
    rows[key][0]['parts'] = [dict(id=label, verbatim=title, marks=3, permittedMarks=[0, 1, 2, 3])
                           for label, title in [('group', 'Group method'), ('personal', 'Personal method'), ('other', 'Other group or personal method')]]
    assert set(rows) == set(blocks) == set(PAGES)
    case = select(page_text(paper, 9), 'Section B Case Study 30 marks')
    stems = {}
    for n in range(1, 8):
        stem = page_text(paper, 16 + (n - 1) * 3).split('(a)', 1)[0]
        stems[n] = tidy(re.sub(r'^Q\.\s*\d+\s+25\s+marks\s*', '', stem))
    cards = []
    for key in blocks:
        section, q, letter, roman = key
        suffix = section.lower() + str(q) + (letter or '') + (roman or '')
        ref = f'2026 CL Section {section} Q{q}' + (f'({letter})' if letter else '') + (f'({roman})' if roman else '')
        card = dict(id='lcvp-2026-cl-' + suffix, subjectId='lcvp', topicId='lcvp-link-modules-' + topics[key],
                    conceptId=suffix, level='common', year=2026, section=section, questionRef=ref,
                    questionText=question(paper, key), stem=stems[q] if section == 'C' else case if section == 'B' else '',
                    figureKey='', labelKey=[], totalMarks=totals[key], rows=rows[key],
                    tariffModel=dict(kind='questionTotal' if key in [a(2), c(5, 'd')] else 'fixed', notation='Original 2026 allocation; complete source guidance retained'),
                    sourceMaterial=source([PAGES[key]]))
        if section == 'A':
            card['videoMaterial'] = dict(kind='source-video', label='OFFICIAL VIDEO', title='2026 LCVP audiovisual examination',
                playbackUrl=VIDEO_URL, canonicalUrl=VIDEO_URL, secFileid='LC462CLP031EV.mov',
                attribution='State Examinations Commission — original 2026 Common Level English audiovisual recording.',
                presentationNote='Watch the original sequence with its sound before answering. The paper allows three minutes to read Section A, then the complete sequence, its three parts, and the complete sequence again. Use the original source link if embedded playback is unavailable.')
            card['additionalSourceMaterials'] = [source([3], title='Original audiovisual instructions')]
        elif section == 'B':
            card['sourceMaterial'] = source([9], 'source-text', 'Slí Abhaile — complete case study')
            card['additionalSourceMaterials'] = [source([PAGES[key]])]
        elif q == 1:
            card['additionalSourceMaterials'] = [source([16], 'source-text', 'Complete Beauty by Lola job advertisement')]
        elif q == 5 and letter == 'c':
            card['stem'] += ' ' + question(paper, c(5, 'a'))
            card['additionalSourceMaterials'] = [source([28], title='Original career and qualification context')]
        cards.append(card)
    assert len(cards) == 44 and sum(c['totalMarks'] for c in cards) == 235
    return cards, scheme


def write(cards, scheme):
    path = ROOT / 'scripts/markbank/authored/lcvp.json'
    old = json.loads(path.read_text())
    ids = {c['id'] for c in cards}
    preserved = [c for c in old if c['id'] not in ids]
    assert len(preserved) == 314, len(preserved)
    path.write_text(json.dumps(preserved + cards, ensure_ascii=False, indent=1) + '\n')
    transcript = '# SEC LCVP 2026 Common Level written marking scheme\n\n'
    transcript += '\n\n'.join(f'## Physical page {i + 1}\n\n' + p.get_text(sort=True) for i, p in enumerate(scheme))
    (ROOT / 'examiner-reports/lcvp/schemes/2026-cl.md').write_text(transcript.rstrip() + '\n')
    review = json.loads(REVIEW.read_text())
    review['status'] = 'source-authored; independent-sweep-complete; two-numeric-scoring-holds'
    review['tasks'] = [dict(id=c['id'], questionRef=c['questionRef'], marks=c['totalMarks'], topicId=c['topicId']) for c in cards]
    review['heldNumericScoring'] = ['lcvp-2026-cl-a2', 'lcvp-2026-cl-c5d']
    review['scoringScope'] = dict(printedOfferedMarks=235, pricedTaskMarks=225,
        heldWholeTaskMarks=10, heldTasks=2,
        distinction='All 44 source tasks are retained. Two tasks worth 10 printed marks use confidence-only review; their numerical splits are unresolved. These holds are not missing/excluded source tasks or a release-readiness claim.')
    review['selectionPolicy'] = {
        'outerSectionC': 'Answer any four of seven. Retain seven independently selectable questions because their topics and priced structures differ; no four-question combination cards.',
        'internalChoices': 'All ordinary open-response and numbered model pools remain whole tasks. Numbered scheme examples are not a mandate to create one card per example or combination.',
        'C5a': 'The required career and matching qualification are two original leaves in one coherent four-mark profile. Preserve both exact prompts and independently claimable 0/2 rows.',
        'C5c': 'One personal activity with its explanation and two pieces learned remains one nine-mark task; all seven illustrative source activities retained, no invented personal model.',
        'C5d': 'Two complete training/benefit profiles from all six source examples; no cross-product of training and benefits. Numeric allocation conflict explicitly held.',
        'C7d': 'Three required responses: one group, one personal and one other group/personal. Preserve distinct claim slots and all nine source models.',
        'B3iii': 'Eight printed action-plan headings are a scaffold, not paid answer options; source explicitly forbids marks for headings. Two content points at one mark each.'}
    REVIEW.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    cards, scheme = build()
    if '--write' in sys.argv:
        write(cards, scheme)
    else:
        print(json.dumps(cards, ensure_ascii=False, indent=2))
