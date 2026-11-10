#!/usr/bin/env python3
"""Independent 2014 Higher inventory after all 48 original pages were swept."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
    ('paper', 'examiner-reports/japanese/papers/2014-hl-000-paper.pdf', '59b71fcb93297410cf035d781222996745dd4b602cd8923f6af8728e825e53cf'),
    ('aural', 'examiner-reports/japanese/papers/2014-hl-A00-paper.pdf', 'e0c704274e1029a9e29c263027e4dd5b48a1708f3fd25cc1b6bd0c34c1e6dd3d'),
    ('scheme', 'examiner-reports/japanese/schemes/2014-hl.pdf', '5035dd9f744ba5e6fb9e19b75589787a53eb9035950d0480d1168dfe0e0654d0'),
]
TASKS = []


def task(section, q, marks, pp, sp, atlas, roman=None):
    component = 'aural' if section.startswith('L') else 'paper'
    TASKS.append({'key': [section, q, None, roman], 'marks': marks, 'component': component,
                  'paperPages': [pp], 'schemePages': sp,
                  'atlas': {'fileid': f'LC058ALP{"A00" if component == "aural" else "000"}EV.pdf', 'questionNumber': str(atlas)}})


def build():
    task('1A', 1, 6, 3, [6], 1)
    for q in [2, 3, 4, 5]:
        for roman in ['i', 'ii']:
            task('1A', q, 2, 3, [6], 1, roman)
    for q in range(1, 5): task('1B', q, 2, 4, [7], 2)
    task('2A', 1, 12, 7, [7], 3)
    for roman, page in [('i', 7), ('ii', 7), ('iii', 8), ('iv', 8)]: task('2A', 2, 2, 7, [page], 3, roman)
    for roman in ['i', 'ii', 'iii']: task('2A', 3, 2, 7, [8], 3, roman)
    task('2A', 4, 4, 7, [8], 3)
    for q in [1, 2]: task('2B', q, 5, 8, [8], 8)
    for q in [1, 2]: task('2C', q, 5, 9, [9], 9)
    for q, marks in [(1, [3, 2]), (2, [2, 2]), (3, [3, 2])]:
        for roman, value in zip(['i', 'ii'], marks): task('3A', q, value, 11, [9], 4, roman)
    for q in [1, 2]: task('3B', q, 3, 11, [10], 5)
    task('3C', None, 10, 12, [10], 10)
    task('3D', None, 10, 12, [10], 11)
    task('4', None, 40, 14, [11, 12], 6)
    task('5', None, 60, 16, [13, 14], 7)
    task('LA', None, 18, 2, [3], 1)
    for roman, value, page in [('i', 3, 3), ('ii', 4, 3), ('iii', 3, 3), ('iv', 3, 4)]: task('LB', 1, value, 3, [page], 2, roman)
    task('LB', 2, 6, 3, [4], 2)
    for roman in ['i', 'ii']: task('LB', 3, 3, 3, [4], 2, roman)
    for roman, value in [('i', 2), ('ii', 3), ('iii', 4), ('iv', 4)]: task('LC', 1, value, 4, [4], 3, roman)
    for roman in ['i', 'ii']: task('LC', 2, 3, 4, [4], 3, roman)
    for roman, value in [('i', 2), ('ii', 2), ('iii', 6), ('iv', 6), ('v', 2)]: task('LD', None, value, 5, [5], 4, roman)
    assert len(TASKS) == 57, len(TASKS)
    totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
        ('reading', lambda t: t['key'][0][0] in '123'), ('writing', lambda t: t['key'][0][0] in '45'),
        ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
    assert totals == {'reading': 120, 'writing': 100, 'listening': 80, 'total': 300}, totals
    sources = []
    for component, path, sha256 in SOURCES:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha256
        sources.append({'component': component, 'path': path, 'sha256': sha256})
    return {'subjectId': 'japanese', 'year': 2014, 'level': 'hl', 'reviewedAt': '2026-11-09',
            'method': 'Independent full visual sweep of every original physical page before authoring. Required pools and tables stay whole; original printed component tariffs, choices and partial credits determine the task boundaries.',
            'sources': sources, 'tasks': TASKS, 'checksums': totals,
            'candidateMaximum': {'written': 220, 'listening': 80, 'total': 300, 'writingChoice': 'All five questions required; Q4 Christmas OR birthday diary using one shared grid; Q5 any four of eight printed headings.'},
            'pageRoles': {
                'paper': dict(zip(map(str, range(1, 21)), [
                    'cover: written220, all five questions required',
                    'Q1A full twelve-link TV guide, NHK/Fuji timetable, all titles/times and vocabulary',
                    'Q1A all six links and eight separate time/language/cartoon/sport/team/coach tasks',
                    'Q1B three original tweets, authors/timestamps, four separate English prompts',
                    'explicit blank; printed footer erroneously says page5of5 but physical PDF has20 pages',
                    'Q2 full overseas profiles for Miyu/Hidemi/Makoto, photographs, underlined cues and vocabulary',
                    'Q2A required profile table with two given cells, four Japanese prompts, three English helping prompts and translation',
                    'Q2B required five meanings and separate five hiragana readings with examples',
                    'Q2C all five underlined past-tense forms and five context-dependent correct verb forms',
                    'Q3 full Eco ideas article with eco-toy, eco-car and Cool Biz sections, illustrations, underline cues and vocabulary',
                    'Q3A six English tasks; Q3B two Japanese tasks',
                    'Q3C all five reading/meaning pairs with distractors; Q3D ten particle blanks across six sentences',
                    'explicit blank',
                    'Q4 two diary alternatives each with three common prompts,200characters',
                    'Q4 answer grid',
                    'Q5 school speech, any four of eight headings,320characters',
                    'Q5 answer grid', 'Q5 answer grid', 'Q5 answer grid', 'explicit blank back cover'])),
                'aural': dict(zip(map(str, range(1, 9)), [
                    'cover: listening80, English answers required',
                    'A three holiday conversations, one required twelve-cell table',
                    'B Sky Tree four tasks including eight telephone blanks, Kenichi three-detail pool, two weather tasks',
                    'C job interview four tasks and restaurant two required order pools',
                    'D Maki/Maeve conversation, five required tasks and full original context',
                    'explicit blank', 'explicit blank', 'explicit blank back cover'])),
                'scheme': dict(zip(map(str, range(1, 21)), [
                    'cover', 'general examiner guidance',
                    'general listening Japanese/romaji/script half-credit; A18 table with descending enjoyment pools and cycle-only1; B1date1+1+1, SkyTree any2concepts2each with nested amenities threshold, directions2+1',
                    'B1phone whole3, B2Kenichi three-details2each and show-only1, B3weather descending2+1; Cjob13 includes experience2+1/restaurant1 partial, details and uniform choose2; restaurant orders two descending2+1 pools',
                    'D18: doctor2, cooking2, Japan-life choose2x3, school choose2x3, return-plans study-music1/college1',
                    'reading120, Q1A22: required links6, eight independent2-mark responses, coach first-name1/surname1',
                    'Q1B8 named Japanese half-credit, Olympic win1/winter1, jumps2/romaji1; Q2A table12 with explicit partials and two given cells; A2extraneous half-credit first two answers',
                    'Q2A2 remaining Japanese answers, A3three2-mark tasks with culture1/origami1 OR whole voluntary-work2, translation2+2; Q2B meanings/readings five1each',
                    'Q2C two required five1-mark grammar pools; Q3A14 full and partial alternatives, descending first task',
                    'Q3B two3-mark answers; Q3C five reading1/meaning1 pairs; Q3D ten1-mark particles',
                    'Q4 both diaries and shared C20/E20: three content6 and two discretionary for appropriate introduction/ending',
                    'Q4 full expression grids20/15, lower if C<10 or length<150; complete marking/error guidance',
                    'Q5 all eight source headings, four content6, discretionary opening/closing2 and chosen-heading1each; stale reference1to6 explicitly noted',
                    'Q5 full expression grids30/20, lower if C<15 or length<200; complete marking/error guidance',
                    'transcript A and startB1', 'transcript B1/B2/B3 and C1',
                    'transcript C2 and D first part', 'D final transcript', 'explicit blank', 'back cover'])),
            },
            'sourceDiscrepancies': [
                {'task': 'Q2A1', 'paperPages': [6, 7], 'schemePages': [7, 8], 'description': 'The scheme profile table labels Makoto Takashi, whereas the original profile, paper table and subsequent scheme answer identify Makoto Hayashi. Retain the original identity and disclose the scheme table typo.'},
                {'task': 'Q3C', 'paperPages': [12], 'schemePages': [10], 'description': 'Item iv is a.にんき in the paper but b.にんき in the scheme; item v is b.でんしゃ in the paper but a.でんしゃ in the scheme. The exact hiragana readings agree. Preserve both literal letter assignments visibly; no invented penalty.'},
                {'task': 'Q5', 'paperPages': [16], 'schemePages': [13], 'description': 'The paper and scheme each print all eight headings and choose any four. A stale scheme content line says headings1-6; retain all eight original headings and disclose the contradictory reference.'},
            ],
            'choiceBoundaries': [
                'Q1A six links remain one6-mark task; two times, language, cartoon, two sports, team and coach are eight independent2-mark tasks. Q1B four2-mark tasks include Olympic-win1/winter1 and jumps2/romaji1 partial.',
                'Q2 profile table remains one12-mark task with two unpriced given cells, date components and explicit1-mark partials. Four Japanese prompts2each, three helping prompts2each and translation2+2. Both kanji pools and both grammar pools are required complete five-item tasks.',
                'Q3A first response any2 descending2+1; remaining answers retain exact2/3-mark alternatives and source1-mark partials. Btwo3-mark Japanese tasks; reading/meaning pool all5x(1+1); particle pool all10x1 remains one task.',
                'Q4 both diary alternatives remain one40-mark card, each three content6 plus shared discretionary2 for introduction/ending and expression20; lowerE15 only when C<10 or length<150. Q5 any4of8 headings6each, discretionary1 per chosen heading plus shared introduction/conclusion2, expression30 lower20 if C<15 or length<200. No invented per-opening allocation.',
                'Listening A required whole18-mark table retains12cells, three descending2+1 enjoyment quotas, complete source alternatives and cycle-only1 partial without double credit. B1SkyTree any2conceptsx2: tallest/Guinness one concept, exact printed630metres, and amenities one concept requiring any2; one amenity has no priced partial. Full nested pool remains visible.',
                'Listening Bdate three1-mark components; directions2+1; phone03-5822-6405 whole3 with no invented digit split; Kenichi any3details2each and show-only1 partial; both weather pools descending2+1. Cexperience full work2/context1 or restaurant-only1, job/uniform any2x2, orders any2descending2+1. Dlife/school any2x3, return-plans1+1.',
                'Language penalty is printed on Q1B only for Japanese and globally on listening for Japanese/romaji/script. No global reading penalty appears. Extraneous-material half credit binds only the four Q2A2 answers. All penalties stay source-local.',
                'Preserve all eleven written and four aural Atlas question numbers/labels/regions, including original coarse whole-section anchors. Physical scheme bounds21to20 only; no invented anchors, aliases or exclusions.',
            ]}


if __name__ == '__main__':
    result = build()
    (Path(__file__).parent / 'reviews/japanese-2014-hl-census.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(TASKS)} independently counted tasks; {result["checksums"]}')
