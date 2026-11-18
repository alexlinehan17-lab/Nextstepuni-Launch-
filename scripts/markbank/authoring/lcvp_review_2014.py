#!/usr/bin/env python3
"""Hash-bound selectors following the independent 50-page 2014 visual sweep."""
import hashlib
import json
import re
import sys
import fitz
from lcvp_review_2026 import ROOT, tidy, select, point, criterion
from lcvp_review_2024 import split_raw
from lcvp_review_2022 import page_raw
from lcvp_review_2018 import choice_row, response_row, before_rate, models
from lcvp_review_2017 import paper_raw, header_body, component_rows
from lcvp_identity import concept_id

REVIEW = ROOT / 'scripts/markbank/authoring/lcvp/2014-cl-main-review.json'
PAPER = 'paper-trail-corpus/exampapers/2014/LC462CLP000EV.pdf'
CASE = 'paper-trail-corpus/exampapers/2014/LC462CLP016EV.pdf'
SCHEME = 'paper-trail-corpus/markingschemes/2014/LC462CLP000EV.pdf'
HASHES = {PAPER: '0ab57a643775584bec9477d433825260b70cfbd9e39b007a56d678cbaf209d37',
          CASE: 'a0e783d3a0b2e1d9d241088edd78223d7346fc4e10866214f0de45cdf5848ff2',
          SCHEME: 'eb92d0d5926e3af0053800e7ae1c911a4ee6403a201078e1b85d47fbe60b27f8'}
VIDEO_URL = 'https://www.examinations.ie/archive/exampapers/2014/LC462CLP031EV.mp4'


def documents():
    for path, expected in HASHES.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
    return fitz.open(ROOT / PAPER), fitz.open(ROOT / SCHEME)


def key(section, q, letter=None, roman=None):
    return section, q, letter, roman


def scheme_parts(doc):
    sections = split_raw('\n'.join(page_raw(doc, n) for n in range(4, 15)),
                         r'^\s*Section ([ABC])\s+', list('ABC'))
    out = {}
    for section, value in sections.items():
        questions = split_raw(value, r'^\s*Q\.?\s*(\d+)\s*',
            [str(n) for n in range(1, {'A': 8, 'B': 3, 'C': 6}[section] + 1)])
        for q, block in questions.items():
            q = int(q)
            if section == 'A' or (section == 'B' and q == 1):
                out[key(section, q)] = block
            elif section == 'B':
                heading, body = header_body(block)
                for roman, part in split_raw(body, r'^\s*\((i{1,3})\)\s*', ['i', 'ii']).items():
                    out[key(section, q, None, roman)] = heading + '\n' + part
            else:
                for letter, part in split_raw(block, r'^\s*\(([abcd])\)\s*', list('abcd')).items():
                    if (q, letter) in [(5, 'c'), (5, 'd')]:
                        heading, body = header_body(part)
                        for roman, answer in split_raw(body, r'^\s*\((i{1,2})\)\s*', ['i', 'ii']).items():
                            out[key(section, q, letter, roman)] = heading + '\n' + answer
                    else:
                        out[key(section, q, letter)] = part
    assert len(out) == 39
    return out


PAGES = {key('A', q): [p] for q, p in enumerate([3, 3, 3, 4, 4, 5, 6, 7], 1)}
PAGES[key('A', 5)] = [4, 5]
PAGES[key('B', 1)] = [9]
PAGES.update({key('B', q, None, roman): [8 + q, 9 + q]
              for q in [2, 3] for roman in (['i', 'ii'])})
PAGES.update({key('C', q, letter): [14 + (q - 1) * 3 + {'a': 0, 'b': 0, 'c': 1, 'd': 2}[letter]]
              for q in range(1, 7) for letter in 'abcd'})
for q, letter in [(5, 'c'), (5, 'd')]:
    pages = PAGES.pop(key('C', q, letter))
    PAGES.update({key('C', q, letter, roman): pages for roman in ['i', 'ii']})


def question(doc, k):
    section, q, letter, roman = k
    value = paper_raw(doc, PAGES[k][0])
    if section in ['A', 'B']:
        value = re.split(r'^\s*Q\.\s*' + str(q) + r'\s+', value, maxsplit=1, flags=re.M)[1]
        value = re.split(r'^\s*Q\.\s*\d+\s+', value, maxsplit=1, flags=re.M)[0]
    if letter:
        value = re.split(r'^\s*\(' + letter + r'\)\s*', value, maxsplit=1, flags=re.M)[1]
        # C5(c)(ii) ends with the wrapped reference "part (a).". Only the
        # following printed letter can delimit this question, not that reference.
        if letter != 'd':
            following = 'abcd'['abcd'.index(letter) + 1]
            value = re.split(r'^\s*\(' + following + r'\)\s*', value, maxsplit=1, flags=re.M)[0]
    if roman:
        value = re.split(r'\(' + roman + r'\)\s*', value, maxsplit=1)[1]
        value = re.split(r'\(i{1,3}\)\s*', value, maxsplit=1)[0]
    value = tidy(re.sub(r'\b\d+\s+marks?\b', '', value, flags=re.I))
    return value


def contrast_models(scheme):
    """Six complete pairs inside the original C6(d) ruled table."""
    page = scheme[13]
    dividers = [item for drawing in page.get_drawings() for item in drawing['items']
                if item[0] == 'l' and abs(item[1].x - item[2].x) < .01
                and 280 < item[1].x < 290 and 625 < min(item[1].y, item[2].y)]
    assert len(dividers) == 8, len(dividers)  # header, six pairs, tariff
    assert len({round(item[1].x, 2) for item in dividers}) == 1
    split_x = dividers[0][1].x
    bounds = sorted((min(item[1].y, item[2].y), max(item[1].y, item[2].y)) for item in dividers)
    result = []
    for upper, lower in bounds[1:-1]:
        cells = []
        for left in [True, False]:
            pieces = []
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    spans = [s for s in line['spans'] if upper <= (s['bbox'][1] + s['bbox'][3]) / 2 <= lower
                             and bool((s['bbox'][0] + s['bbox'][2]) / 2 < split_x) == left]
                    if spans:
                        pieces.append((line['bbox'][1], line['bbox'][0], ''.join(s['text'] for s in spans)))
            cell = tidy(' '.join(value for _, _, value in sorted(pieces)))
            assert cell
            cells.append(cell)
        result.append(cells[0] + ' — ' + cells[1])
    assert len(result) == 6 and result[0].endswith('on a daily basis')
    return result


def case_study(paper):
    # Native order keeps five prose paragraphs separate from the adjacent pie
    # chart. Sorted text interleaves chart labels in the middle of sentences.
    native = paper[7].get_text(sort=False)
    text = native[native.index('COROBAWN SUMMER FESTIVAL'):]
    text, graph = text.split('Visiting\u00a0', 1)
    assert tidy(graph) == ('Family 6% Hiking/Hill Walking 38% Golf 24% Gathering Festival 32% '
                           'Reasons for Visiting Corobawn in 2013')
    assert 'The committee, representing the local community, is made up of ten enthusiastic' in tidy(text)
    # The original chart remains available on the same source page. This exact
    # label/value transcription also exposes its values before reveal.
    return tidy(text) + '\n\nReasons for Visiting Corobawn in 2013: Visiting Family 6%; Hiking/Hill Walking 38%; Golf 24%; Gathering Festival 32%.'


def source(pages, kind='source-question', title='Original question'):
    return dict(kind=kind, label='OFFICIAL SOURCE', title=title, pages=pages,
        attribution='SEC LCVP Link Modules 2014 Common Level — © State Examinations Commission.',
        presentationNote='Read the complete original source and question in context.')


def build():
    paper, scheme = documents()
    raw = scheme_parts(scheme)
    rows, totals, topics, concepts = {}, {}, {}, {}
    a = lambda q: key('A', q)
    b = lambda q, r=None: key('B', q, None, r)
    c = lambda q, l, r=None: key('C', q, l, r)
    def put(k, marks, topic, concept, value):
        rows[k], totals[k], topics[k], concepts[k] = value, marks, topic, concept
    def labelled(k):
        header, body = header_body(raw[k])
        if k[3]:
            header = split_raw(header, r'^\s*\((i{1,2})\)\s*', ['i', 'ii'])[k[3]]
        return tidy(re.sub(r'\b\d+\s+[Mm]arks?\b', '', header)), body
    def ordinary(k, topic, concept, count, per, expected, rate, binary=False, extra=''):
        label, body = labelled(k)
        pool = models(before_rate(body, rate), expected)
        if binary or per == 1:
            value = choice_row('responses', label, pool, count, per,
                f'Original {count} responses at {per} or 0 marks each. All alternatives remain. ' + extra)
        else:
            value = response_row('responses', label, pool, count, list(range(per + 1)),
                f'Original {count} responses, each {per} marks in printed 1-mark components. ' + extra)
        put(k, count * per, topic, concept, [value])
    def profiles(k, topic, concept, count, pool, names, marks, ladders, guidance):
        value = []
        for i in range(1, count + 1):
            value.append(dict(id=f'profile-{i}', kind='criterion', verbatim=labelled(k)[0],
                marks=sum(marks), permittedMarks=list(range(sum(marks) + 1)),
                parts=[dict(id=f'component-{j}', verbatim=name, marks=mark, permittedMarks=ladder)
                       for j, (name, mark, ladder) in enumerate(zip(names, marks, ladders), 1)],
                contextNote=f'Complete profile {i} of {count}. ' + guidance + ' Keep each response distinct and credit it only once. Complete original guidance: ' + ' | '.join(pool)))
        put(k, count * sum(marks), topic, concept, value)
    def binary_expansion(k, topic, concept, expected):
        label, body = labelled(k)
        pool = models(before_rate(body, r'3\s*@\s*3m'), expected)
        value = component_rows(label, pool, [[1, 2]] * 3,
            'Original 3@3m (1 + 2 (0/2)). The two-mark component is indivisible: 0 or 2, no 1-mark partial. No fixed semantic division beyond the printed components is inferred.')
        put(k, 9, topic, concept, value)

    _, body = labelled(a(1))
    put(a(1), 2, '1-3', 'student-social-enterprise-awards', [point('competition', tidy(before_rate(body, r'2m')), 2)])
    ordinary(a(2), '1-3', 'prior-enterprise-entrants-advice', 2, 1, 3, r'2\s*@\s*1m')
    ordinary(a(3), '1-0', 'enterprise-presentation-preparation', 2, 1, 4, r'2\s*@\s*1m')
    ordinary(a(4), '1-3', 'enterprise-project-funding', 4, 1, 5, r'4\s*@\s*1m')
    ordinary(a(5), '1-3', 'charity-shop-target-market', 4, 1, 6, r'4\s*@\s*1m')
    ordinary(a(6), '1-0', 'enterprise-planning-skills', 2, 2, 8, r'2\s*@\s*2\s*marks', binary=True)
    ordinary(a(7), '1-0', 'presentation-judges-feedback', 3, 2, 4, r'3\s*@\s*2\s*marks', binary=True)
    ordinary(a(8), '1-3', 'enterprise-project-evaluation', 6, 1, 6, r'6\s*@\s*1\s*mark',
        extra='Keep the full fourth model: review of career options + valid expansion in light of the role or experience. The skills model includes team, financial and marketing skills.')
    ordinary(b(1), '1-1', 'corobawn-visitor-reasons', 3, 2, 5, r'3\s*@\s*2m')
    ordinary(b(2, 'i'), '1-3', 'visitor-survey-reasons', 4, 2, 6, r'4\s*@\s*2m')
    ordinary(b(2, 'ii'), '1-1', 'local-business-promotion', 2, 2, 8, r'2\s*@\s*2\s*marks',
        extra='The third model includes both special promotions and niche products such as packed lunches for walkers.')
    ordinary(b(3, 'i'), '1-0', 'effective-festival-meetings', 4, 2, 8, r'4\s*@\s*2\s*marks')
    ordinary(b(3, 'ii'), '1-0', 'festival-conflict-resolution', 2, 2, 7, r'2\s*@\s*2\s*marks')

    _, body = labelled(c(1, 'a'))
    put(c(1, 'a'), 1, '0-2', 'investigated-career-title', [point('career', tidy(before_rate(body, r'1\s*mark')), 1)])
    ordinary(c(1, 'b'), '0-2', 'career-interview-preparation', 3, 2, 6, r'3\s*@\s*2m')
    _, body = labelled(c(1, 'c'))
    pool = models(before_rate(body, r'3\s*@\s*1m'), 2)
    profiles(c(1, 'c'), '0-2', 'career-qualities-skills-relevance', 3, pool,
        ['Quality/skill', 'Reason relevant to this career'], [1, 2], [[0, 1], [0, 1, 2]],
        'Original 3@1m for stating + 3@2m (1+1) for explaining. Must be relevant to the SAME career. Keep the two open source categories; no example or prescribed category mix is invented.')
    binary_expansion(c(1, 'd'), '0-2', 'career-research-method-evaluation', 7)
    label, body = labelled(c(2, 'a'))
    assert '1m for naming' in body and '1m for outline' in body
    profiles(c(2, 'a'), '1-1', 'visited-local-business', 1, [tidy(before_rate(body, r'1m for naming'))],
        ['Name', 'Outline'], [1, 1], [[0, 1], [0, 1]], 'One complete name-and-outline task; 1m for naming and 1m for outline.')
    ordinary(c(2, 'b'), '1-1', 'business-visit-student-benefits', 3, 2, 7, r'3\s*@\s*2m')
    _, body = labelled(c(2, 'c'))
    profiles(c(2, 'c'), '1-1', 'business-visit-subject-connections', 3, [tidy(before_rate(body, r'3\s*@\s*1m'))],
        ['Subject', 'Use in organisation/planning'], [1, 2], [[0, 1], [0, 1, 2]],
        'Original 3@1m naming + 3@2m (1+1) explanation. THREE subjects OTHER THAN Link Modules, each linked to the SAME visit. Mention particular knowledge/skills; no invented subjects.')
    ordinary(c(2, 'd'), '1-1', 'business-visit-host-preparation', 4, 2, 7, r'4\s*@\s*2m')
    label, body = labelled(c(3, 'a'))
    put(c(3, 'a'), 2, '0-0', 'upskilling-definition', [response_row('definition', label,
        [tidy(before_rate(body, r'\(1\s*\+\s*1\)'))], 2, [0, 1],
        'Original whole definition 2m (1+1). Preserve the complete definition without inventing a fixed semantic split.')])
    ordinary(c(3, 'b'), '0-0', 'worker-upskilling-reasons', 6, 1, 10, r'6\s*@\s*1m')
    ordinary(c(3, 'c'), '0-0', 'jobbridge-jobseeker-benefits', 4, 2, 7, r'4\s*@\s*2m',
        extra='Original historical JobBridge question and model guidance; retain the full quoted paper context.')
    binary_expansion(c(3, 'd'), '0-0', 'employer-effective-teamwork', 10)
    label, body = labelled(c(4, 'a'))
    heading, item_text = body.split('1m', 1)
    assert tidy(heading) == 'Heading' and '* Compulsory item' in item_text
    pool = models(before_rate(item_text, r'5\s*items\s*@\s*1m'), 7)
    assert pool[0] == 'Election of officers* (Chairperson/Managing Director/Secretary/Treasurer)'
    put(c(4, 'a'), 6, '1-3', 'mini-company-first-agenda', [point('heading', 'Heading', 1),
        point('election', pool[0], 1, '* Compulsory item: election of officers. Keep the complete source examples; no unprinted whole-question penalty is added.'),
        choice_row('other-items', label, pool[1:], 4, 1,
            'Original Heading 1m + 5 items@1m. Election of officers is compulsory and priced separately; choose four other distinct items from the full remaining pool. No repeated credit.')])
    ordinary(c(4, 'b'), '1-3', 'enterprise-action-plan-benefits', 4, 1, 8, r'4\s*@\s*1m')
    _, body = labelled(c(4, 'c'))
    profiles(c(4, 'c'), '1-3', 'mini-company-resources', 3, models(before_rate(body, r'3\s*@\s*2m'), 4),
        ['Resource', 'Explanation'], [1, 1], [[0, 1], [0, 1]],
        'Original three complete resource/reason profiles: 1m identifying resource + 1m explanation. Retain every nested example in all four source categories.')
    label, body = labelled(c(4, 'd'))
    definition, types = body.split('Types of Feedback.', 1)
    put(c(4, 'd'), 9, '1-3', 'enterprise-feedback-definition-types', [
        response_row('definition', label, [tidy(before_rate(definition, r'3\s*@\s*1m'))], 3, [0, 1],
            'One whole task: definition 3@1m plus three types 2m (1+1) each. No fixed semantic division of the full definition is invented.'),
        response_row('types', label, models(before_rate(types, r'3\s*@\s*2m'), 6), 3, [0, 1, 2],
            'Original types 3@2m (1+1). Preserve all six models and every continuation; no required positive/negative mix.')])
    _, body = labelled(c(5, 'a'))
    assert re.fullmatch(r'Name of group\s+1m\s+Outline of the type of work\s+2m\s*\(0/2\)', body.strip())
    profiles(c(5, 'a'), '1-2', 'local-voluntary-organisation', 1, ['Name of group', 'Outline of the type of work'],
        ['Name of group', 'Outline of the type of work'], [1, 2], [[0, 1], [0, 2]],
        'Original name 1m + outline 2m (0/2). Same voluntary group; no 1-mark partial for outline and no invented personal example.')
    ordinary(c(5, 'b'), '1-2', 'choosing-voluntary-organisation', 4, 1, 7, r'4\s*@\s*1m')
    label, body = labelled(c(5, 'c', 'i'))
    put(c(5, 'c', 'i'), 2, '1-2', 'voluntary-swot-benefits', [response_row('benefit', label,
        [tidy(before_rate(body, r'2\s*@\s*1m'))], 2, [0, 1], 'Original 2@1m. Preserve the full SWOT purpose/benefit statement; no fixed semantic split is inferred.')])
    label, body = labelled(c(5, 'c', 'ii'))
    model_text = body.split('No marks for headings', 1)[0]
    categories = split_raw(model_text, r'^\s*(Strengths|Weaknesses|Opportunities|Threats):\s*',
                           ['Strengths', 'Weaknesses', 'Opportunities', 'Threats'])
    swot = []
    for title, expected in [('Strengths', 4), ('Weaknesses', 3), ('Opportunities', 4), ('Threats', 3)]:
        pool = [tidy(line) for line in categories[title].splitlines() if line.strip()]
        assert len(pool) == expected
        swot.append(response_row(title.lower(), label, pool, 1, [0, 1, 2],
            title + ': A relevant statement for each. Original 4@2m (1+1), one complete statement under EACH category. No marks for headings. No repetition of points. Keep the same organisation named in part (a).'))
    put(c(5, 'c', 'ii'), 8, '1-2', 'voluntary-organisation-swot', swot)
    ordinary(c(5, 'd', 'i'), '1-2', 'business-support-voluntary-group', 2, 2, 4, r'2\s*@\s*2m')
    ordinary(c(5, 'd', 'ii'), '1-2', 'business-reasons-voluntary-support', 2, 2, 5, r'2\s*@\s*2m')
    label, body = labelled(c(6, 'a'))
    pool = [tidy(line) for line in before_rate(body, r'4\s*@\s*1m').splitlines() if line.strip()]
    assert len(pool) == 7 and pool[4] == 'Adaptible' and 'Each must be explained for the mark' in body
    put(c(6, 'a'), 4, '1-0', 'explained-entrepreneur-characteristics', [response_row('characteristics', label, pool, 4, [0, 1],
        'Original 4@1m each. Each must be explained for the mark. A bare trait name receives no mark; manually assess each complete distinct characteristic/explanation. All seven source traits remain; no explanation is invented.')])
    ordinary(c(6, 'b'), '1-0', 'entrepreneurs-society-benefits', 3, 2, 8, r'3\s*@\s*2m')
    _, body = labelled(c(6, 'c'))
    profiles(c(6, 'c'), '1-0', 'entrepreneur-startup-problems', 3, models(before_rate(body, r'3\s*@\s*1m'), 8),
        ['Heading', 'Expansion'], [1, 2], [[0, 1], [0, 1, 2]],
        'Original 3@1m (Heading) + 3@(1+1) expansion. Keep three complete problem/expansion profiles and all eight source models.')
    put(c(6, 'd'), 6, '1-0', 'entrepreneur-manager-role-comparison', [response_row('contrasts', labelled(c(6, 'd'))[0],
        contrast_models(scheme), 3, [0, 1, 2],
        'Original 3@2m (1+1). Each paired model reads Entrepreneur — Manager. Retain both complete cells for all six contrasts, including every wrapped line.')])
    assert set(rows) == set(raw) == set(PAGES) and len(rows) == 39
    assert sum(totals.values()) == 210
    case = case_study(paper)
    stems = {q: tidy(re.split(r'^Q\.\s*' + str(q) + r'\s+', paper_raw(paper, 14 + (q - 1) * 3), maxsplit=1, flags=re.M)[1].split('(a)', 1)[0]) for q in range(1, 7)}
    cards = []
    for k in raw:
        section, q, letter, roman = k
        suffix = section.lower() + str(q) + (letter or '') + (roman or '')
        card_id = 'lcvp-2014-cl-' + suffix
        ref = f'2014 CL Section {section} Q{q}' + (f'({letter})' if letter else '') + (f'({roman})' if roman else '')
        card = dict(id=card_id, subjectId='lcvp', topicId='lcvp-link-modules-' + topics[k],
            conceptId=concept_id(card_id, concepts[k]), level='common', year=2014, section=section,
            questionRef=ref, questionText=question(paper, k), stem=case if section == 'B' else stems[q] if section == 'C' else '',
            figureKey='', labelKey=[], totalMarks=totals[k], rows=rows[k],
            tariffModel=dict(kind='fixed', notation='Original 2014 marking scheme allocation.'), sourceMaterial=source(PAGES[k]))
        if section == 'C' and q in [1, 2, 5] and letter in 'bcd':
            card['stem'] += ' ' + question(paper, c(q, 'a'))
        if section == 'A':
            card['videoMaterial'] = dict(kind='source-video', label='OFFICIAL VIDEO', title='2014 LCVP audiovisual examination',
                playbackUrl=VIDEO_URL, canonicalUrl=VIDEO_URL, secFileid='LC462CLP031EV.mp4',
                attribution='State Examinations Commission — original 2014 Common Level English audiovisual recording.',
                presentationNote='Watch the original enterprise sequence with its sound before answering. Follow the printed viewing instructions. Use the original source link if embedded playback is unavailable.')
            card['additionalSourceMaterials'] = [source([2], title='Original audiovisual instructions')]
        elif section == 'B':
            card['sourceMaterial'] = source([8], 'source-text', 'Corobawn Summer Festival — complete case study and chart')
            card['sourceMaterial']['presentationNote'] += ' Read all five paragraphs and the original 2013 visitor-reasons pie chart. Population 4,000 and nearly 5,000 visitors are distinct figures.'
            card['additionalSourceMaterials'] = [source(PAGES[k])]
        cards.append(card)
    return cards, scheme


def scheme_page_text(scheme, number):
    return scheme[number - 1].get_text(sort=number != 14)


def write(cards, scheme):
    review = json.loads(REVIEW.read_text())
    proof = review['sourceVerification']['proof']
    digest = hashlib.sha256(json.dumps(cards, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    assert proof['tasks'] == review['manualPricedTasks'] == 39
    assert digest == proof['authoredSubsetSha256'], 'Refresh the mandatory original-source gate before writes'
    assert review['sourceVerification']['validatedAuthoringSha256'] == hashlib.sha256((ROOT / 'scripts/markbank/authoring/lcvp_review_2014.py').read_bytes()).hexdigest()
    path = ROOT / 'scripts/markbank/authored/lcvp.json'
    old = json.loads(path.read_text())
    preserved = [c for c in old if c['year'] != 2014]
    prior = [c for c in old if c['year'] == 2014]
    assert len(prior) in [0, 39] and len(preserved) == 518
    assert {c['id']: c['conceptId'] for c in prior}.items() <= {c['id']: c['conceptId'] for c in cards}.items()
    result, inserted = [], False
    for card in old:
        if card['year'] == 2014:
            if not inserted:
                result.extend(cards)
                inserted = True
        else:
            result.append(card)
    if not inserted:
        result.extend(cards)
    assert [c for c in result if c['year'] != 2014] == preserved
    path.write_text(json.dumps(result, ensure_ascii=False, indent=1) + '\n')
    pages = [f'## Physical page {n}\n\n' + scheme_page_text(scheme, n) for n in range(1, 17)]
    transcript = '# SEC LCVP 2014 Common Level written marking scheme\n\n' + '\n\n'.join(pages)
    (ROOT / 'examiner-reports/lcvp/schemes/2014-cl.md').write_text('\n'.join(line.rstrip() for line in transcript.splitlines()).rstrip() + '\n')
    review['status'] = 'source-authored; independent-sweep-complete; validation-pending'
    review['tasks'] = [dict(id=c['id'], questionRef=c['questionRef'], marks=c['totalMarks'], topicId=c['topicId']) for c in cards]
    REVIEW.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    cards, scheme = build()
    if '--write' in sys.argv:
        write(cards, scheme)
    else:
        print(json.dumps(cards, ensure_ascii=False, indent=2))


