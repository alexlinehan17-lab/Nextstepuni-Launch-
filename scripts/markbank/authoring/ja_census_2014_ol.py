#!/usr/bin/env python3
"""Independent 2014 Ordinary inventory after all forty original pages were swept."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
    ('paper', 'examiner-reports/japanese/papers/2014-ol-000-paper.pdf', '64eb767e0866b2605ea1cc2eaeb9cb1979e9ed5c2c7e5a4bb565e5306bde67c4'),
    ('aural', 'examiner-reports/japanese/papers/2014-ol-A00-paper.pdf', 'f6e50ff8e32cbd3081f71533d63bb266dc04ea97d18a1997d470ccf6ff6cad9f'),
    ('scheme', 'examiner-reports/japanese/schemes/2014-ol.pdf', '69355ed48177aeaec82eb22b281381acfe9cea433c3a39a8791b88c662472f9f'),
]
TASKS = []


def task(section, q, marks, pp, sp, atlas, roman=None):
    component = 'aural' if section.startswith('L') else 'paper'
    TASKS.append({'key': [section, q, None, roman], 'marks': marks, 'component': component,
                  'paperPages': [pp], 'schemePages': sp,
                  'atlas': {'fileid': f'LC058GLP{"A00" if component == "aural" else "000"}EV.pdf', 'questionNumber': str(atlas)}})


def build():
    task('1', 1, 10, 3, [5], 1)
    task('1', 2, 10, 3, [5], 2)
    for roman in ['i', 'ii']: task('1', 3, 4, 3, [5], 3, roman)
    task('1', 4, 2, 3, [5], 4)
    for roman in ['i', 'ii']: task('2A', 1, 3, 5, [6], 5, roman)
    task('2A', 2, 2, 5, [6], 6)
    task('2A', 3, 10, 5, [6], 7)
    task('2A', 4, 10, 5, [6], 7)
    task('2B', None, 10, 6, [7], 8)
    for q in [1, 2]: task('2C', q, 10, 7, [7], 9)
    task('2D', None, 3, 8, [7], 16)
    task('3', 1, 8, 11, [8], 10)
    for roman, value in [('i', 3), ('ii', 6)]: task('3', 2, value, 11, [8], 11, roman)
    for q, atlas in [(3, 12), (4, 13)]:
        for roman in ['i', 'ii', 'iii']: task('3', q, 2, 11, [8], atlas, roman)
    task('4', None, 30, 12, [9], 14)
    task('5', None, 50, 13, [9, 10], 15)
    for q, values in [(1, [2, 4, 4]), (2, [2, 4, 4]), (3, [4, 4])]:
        for roman, value in zip(['i', 'ii', 'iii'], values): task('LA', q, value, 2, [3], q, roman)
    for q, count, atlas in [(1, 3, 7), (2, 2, 8)]:
        for roman in ['i', 'ii', 'iii'][:count]: task('LB', q, 4, 3, [3], atlas, roman)
    task('LB', 3, 4, 3, [3], 9)
    for roman, value in [('i', 2), ('ii', 4), ('iii', 4), ('iv', 4), ('v', 4)]: task('LC', 1, value, 4, [4], 10, roman)
    for roman, value in [('i', 2), ('ii', 4)]: task('LC', 2, value, 4, [4], 11, roman)
    for q, atlas in [(1, 12), (2, 13), (3, 14), (4, 4), (5, 5), (6, 6)]: task('LD', q, 4, 5, [4], atlas)
    assert len(TASKS) == 52, len(TASKS)
    totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
        ('reading', lambda t: t['key'][0][0] in '123'), ('writing', lambda t: t['key'][0][0] in '45'),
        ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
    assert totals == {'reading': 120, 'writing': 80, 'listening': 100, 'total': 300}, totals
    sources = []
    for component, path, sha256 in SOURCES:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha256
        sources.append({'component': component, 'path': path, 'sha256': sha256})
    return {'subjectId': 'japanese', 'year': 2014, 'level': 'ol', 'reviewedAt': '2026-11-10',
        'method': 'Independent full visual sweep of sixteen written, eight aural and sixteen scheme physical pages before authoring. Complete required pools and explicit choices remain whole; each separately priced comprehension answer retains its source identity. Broken scheme text encoding must be recovered from original glyph evidence before publication.',
        'sources': sources, 'tasks': TASKS, 'checksums': totals,
        'candidateMaximum': {'written': 200, 'listening': 100, 'total': 300, 'writingChoice': 'All five written questions required; Q4 all ten blanks, Q5 any five of seven independent responses.'},
        'pageRoles': {
            'paper': dict(zip(map(str, range(1, 17)), [
                'cover: written200, all five questions required',
                'Q1 full Tokyo Zoo shop webpage, eight links, all toy prices, colours, goods, admission prices, hours and closing day',
                'Q1 five required links, five required toy prices, two colours, two katakana goods and closing day; language directions explicit',
                'Q2 complete oldest-people profile/table with names, dates, places, photographs, underlined cues and vocabulary',
                'Q2A two average ages, one truth decision, choose-two complete people profiles and all five truth/evidence pairs',
                'Q2B all ten meanings with complete English and Irish distractors and given example',
                'Q2C five required negative forms with underlines and five particle MCQs with example',
                'Q2D open culture prompt on reasons for Japanese longevity',
                'explicit blank',
                'Q3 complete four-person Japan GAA webpage with photographs, logo and vocabulary',
                'Q3 four required person/place matches, October detail, any two countries, three independent MCQs and three Japanese prompts',
                'Q4 complete email, ten required blanks, full eleven-token bank and given example',
                'Q5 all seven music prompts, answer any five, complete vocabulary and answer grids',
                'explicit blank', 'explicit blank', 'explicit blank back cover'])),
            'aural': dict(zip(map(str, range(1, 9)), [
                'cover: listening100, all questions in English',
                'A three holiday conversations, eight separately priced tasks with all distractors',
                'B three news items, six tasks; prefilled phone grid has four missing digits; weather item unnumbered withinQ3',
                'C interview five tasks and ordering two tasks, all distractors and explicit two-dish request',
                'D six tasks with all distractors and one open dislike response',
                'explicit blank', 'explicit blank', 'explicit blank back cover'])),
            'scheme': dict(zip(map(str, range(1, 17)), [
                'cover', 'general examiner guidance',
                'global listening romaji/Japanese-script half credit; A28/B24; phone4 at1permissingnumber, full source number',
                'C24: interview18, orders2+4, compound food details1+1 within any-two-dish quota; D24 with teachers/strict2 partial',
                'general reading inappropriate-language half credit; allQ1 tariffs, five links2each, five prices2each, colours2+2, katakana2+2, Monday2',
                'Q2A28: two ages3each, truth2, anytwo complete profiles5each (surname1/given1/date1/place2), five truth1/quote1 pairs',
                'Q2B10 required MCQ letters1each; C20 two required five-item pools2each; D3 one unprinted culture point2 plus discretionary1',
                'Q3 all29marks: required four matches2each, October3, countriesany2x3, threeMCQs2each and threeJapaneseanswers2each',
                'Q4 ten blanks3each; Q5 anyfive responses C5/E5, explicit C3+2 oniv/v, complete content bands and Ecap3 when ownC<4',
                'Q5 complete expression1/2-3/4-5 bands and global error/marking guidance',
                'complete A transcript', 'complete B transcript', 'complete C transcript', 'complete D transcript',
                'explicit blank', 'back cover'])),
        },
        'sourceDiscrepancies': [
            {'task': 'LB3', 'paperPages': [3], 'schemePages': [3], 'description': 'The scheme labels the single weather response (i), whereas the paper prints no subsidiary number. Preserve the original paper Q3 identity and complete wording.'},
            {'task': 'Q3.4(ii)', 'paperPages': [11], 'schemePages': [8], 'description': 'The original scheme question restatement visibly prints どこにすねいますか with ね, whereas the original paper prints どこにすんでいますか. Preserve the original paper prompt and the unchanged printed answer/tariff; disclose the literal scheme typo.'},
        ],
        'choiceBoundaries': [
            'Q1 five links and five toy prices stay whole required10-mark pools. Colours stay one4-mark response with two2-mark components; required two katakana goods stay one4-mark pool; closing day2 separately. Examples unpriced.',
            'Q2A two independent average ages3each and truth2; one choose-two-of-four complete profile task10, each profile surname1/given-name1/date-of-birth1/place2. Given Okawa example unpriced. Five truth/evidence pairs1+1 stay one required10-mark pool; alltenkanji and bothfivegrammar pools remain whole.',
            'Culture Q2D has no model answer: one source-guided unprinted criterion3 with separate point2/discretionary1 controls, not invented reasons or two points.',
            'Q3 four required matches stay one8-mark task; October3 and countriesany2of5x3 separate. ThreeMCQs and threeJapaneseanswers2each remain independent responses.',
            'Q4 alltenblanks3each stay one30-mark task with complete originalbank andexample; do not invent a once-only instruction absent from this paper. Q5 one50-mark task anyfiveofseven C5/E5; iv/v show explicit3+2 component maxima but the common content scale permits totals1,2,3-4,5 without specifying a per-component partial allocation. Keep manual whole-response C0-5 with both literal allocations and all bands visible. OwnEcap3 when owncontent<=3; allresponses remain independent.',
            'Listening27tasks: A8/B6/C7/D6 and28/24/24/24marks. Phone03-5822-6405 has four missingdigits8/4/0/5, onecard with four1-mark components from explicit1percorrectnumber. No additional whole-number credit.',
            'C2ii choose two dishes: tempura2; teriyaki1+salmon1; toufu1+salad1; sashimi/rawfish2 one alternative concept. Each compound dish counts one selected group and partial components remain independent. D5 anyonefull4 or teachers/strict2 in the same response, never additive.',
            'General reading half credit applies to all23reading tasks, listening namedromaji/Japanesescript to all27. No writing language penalty or extraneous-material rule is printed.',
            'Preserve all16written and14aural originalAtlas identities/labels/regions. Correct physicalschemebound17to16 only, no aliases or exclusions.',
        ]}


if __name__ == '__main__':
    result = build()
    (Path(__file__).parent / 'reviews/japanese-2014-ol-census.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(TASKS)} independently counted tasks; {result["checksums"]}')
