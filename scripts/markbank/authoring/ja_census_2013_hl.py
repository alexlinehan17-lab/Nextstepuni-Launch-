#!/usr/bin/env python3
"""Independent 2013 Higher inventory after all 44 original pages were swept."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
    ('paper', 'examiner-reports/japanese/papers/2013-hl-000-paper.pdf', '0ffbc8bb2997bcf7cc45501f37740d7ac630ed94cf5043951eef0d37b8c9ed30'),
    ('aural', 'examiner-reports/japanese/papers/2013-hl-A00-paper.pdf', 'f305723a4a90896b32c16db110d32a97e49bad1157e37b4357705951239ac94e'),
    ('scheme', 'examiner-reports/japanese/schemes/2013-hl.pdf', '23b16facde93e13a8a83aa590ac970e6e6776ae6df84c39347288ad65a32a887'),
]
TASKS = []


def task(section, q, marks, pp, sp, atlas, roman=None):
    component = 'aural' if section.startswith('L') else 'paper'
    TASKS.append({'key': [section, q, None, roman], 'marks': marks, 'component': component,
                  'paperPages': [pp], 'schemePages': sp,
                  'atlas': {'fileid': f'LC058ALP{"A00" if component == "aural" else "000"}EV.pdf', 'questionNumber': str(atlas)}})


def build():
    task('1AA', None, 10, 3, [6], 1)
    task('1AB', 1, 6, 3, [6], 1)
    for roman in ['i', 'ii', 'iii']: task('1AB', 2, 2, 3, [6], 1, roman)
    task('1B', None, 10, 4, [6], 1)
    task('2A', 1, 11, 6, [7], 2)
    for roman in ['i', 'ii', 'iii']: task('2A', 2, 2, 6, [7], 2, roman)
    # The paper repeats 2 for this whole discussion after its separate 2(i–iii).
    task('2A', 2, 8, 6, [7, 8], 2)
    task('2B', None, 10, 7, [8], 6)
    for q, marks, page in [(1, 10, 7), (2, 5, 8), (3, 5, 8)]: task('2C', q, marks, page, [8], 7)
    for q, values in [(1, [4, 4]), (2, [3, 4, 3])]:
        for roman, marks in zip(['i', 'ii', 'iii'], values): task('3A', q, marks, 10, [9], 3, roman)
    task('3A', 3, 5, 10, [9], 3)
    for q in [1, 2]: task('3B', q, 5, 11, [9], 8)
    task('4', None, 40, 12, [10, 11], 4)
    task('5', None, 60, 15, [12, 13], 5)
    task('LA', None, 20, 2, [3], 1)
    task('LB', 1, 8, 3, [3], 2)
    for roman, marks in [('i', 2), ('ii', 4), ('iii', 2), ('iv', 2)]: task('LB', 2, marks, 3, [3], 2, roman)
    for q, values in [(1, [2, 4]), (2, [2, 2, 3, 3]), (3, [2, 4])]:
        for roman, marks in zip(['i', 'ii', 'iii', 'iv'], values): task('LC', q, marks, 4, [4], 3, roman)
    task('LD', None, 20, 5, [5], 4)
    assert len(TASKS) == 40
    totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
        ('reading', lambda t: t['key'][0][0] in '123'), ('writing', lambda t: t['key'][0][0] in '45'),
        ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
    assert totals == {'reading': 120, 'writing': 100, 'listening': 80, 'total': 300}
    sources = []
    for component, path, sha256 in SOURCES:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha256
        sources.append({'component': component, 'path': path, 'sha256': sha256})
    return {'subjectId': 'japanese', 'year': 2013, 'level': 'hl', 'reviewedAt': '2026-11-10',
        'method': 'Independent complete visual sweep of twenty written, eight aural and sixteen scheme physical pages before authoring. Required finite pools stay whole; separately prompted comprehension answers retain their printed boundaries. Both printed writing choices share a grid and one topic and remain one card each.',
        'sources': sources, 'tasks': TASKS, 'checksums': totals,
        'candidateMaximum': {'written': 220, 'listening': 80, 'total': 300, 'writingChoice': 'Q4 choose(a) or(b); Q5 choose(a) or(b), then any four of that option\'s six headings.'},
        'pageRoles': {
            'paper': dict(zip(map(str, range(1, 21)), [
                'cover: written220, answer all five questions',
                'Q1 PartA complete fashion-week webpage, nine events, locations, dates, notices and vocabulary',
                'Q1 PartA innerA five required Japanese events; innerB three required venue details and three separately prompted comprehension questions',
                'Q1 PartB complete designer profile, photograph, categories and five-blank English biography',
                'Q2 complete four accommodation reviews with photographs, ratings, prices and vocabulary',
                'Q2A complete accommodation table with given cells; Japanese2(i–iii); separately printed repeated2 discussion about both hotels',
                'Q2B five required kanji reading/meaning pairs with full choices/example; Q2C1 ten required particles in seven sentences',
                'Q2C2 five required negatives and Q2C3 five te forms, both with complete examples',
                'Q3 full Evan/Mika emails with underlines, names and vocabulary',
                'Q3A six separately prompted English comprehension responses',
                'Q3B five required meanings and five required hiragana readings, with examples',
                'Q4 choose job speech or college speech, same40-mark grid, approximately200characters',
                'Q4 answer grid', 'Q4 continued answer grid',
                'Q5 choose family-holiday email or home-holiday email, each anyfour of six headings, approximately320characters',
                'Q5 answer grid', 'Q5 continued answer grid', 'continued answer grid', 'explicit blank', 'explicit blank back cover'])),
            'aural': dict(zip(map(str, range(1, 9)), [
                'cover: listening80, all responses in English',
                'A required four-person weather/plans/items table; third printed nameTom differs from schemeHaru',
                'B four health suggestions and four separately numbered pool-promotion tasks; phone prefilled06 and seven blanks',
                'C eight separately numbered comprehension tasks, including descending-detail pools and required turn-right direction',
                'D complete nine-field interview table with given nameKentaSuzuki',
                'explicit blank', 'explicit blank', 'explicit blank back cover'])),
            'scheme': dict(zip(map(str, range(1, 17)), [
                'official cover', 'published-scheme general marking notice',
                'general listening language rule, A20 and B18 with exact full/partial tariffs; phone misnumbered(v)',
                'C22 complete answer pools and mixed direction allocation',
                'D20 nine-field table with unequal hobby tariffs, spelling/place/restaurant partials',
                'reading120; Q1A/B32; romanised katakana acceptance; Japanese-language half rules scoped to innerB and PartB',
                'Q2 table11, Japanese6 with extraneous-material condition, discussion8 and hostel pool',
                'capsule-hotel pool; Q2 kanji10 and grammar20',
                'Q3 comprehension23 and kanji10 with exact partials; last two reading rows misnumbered(vi)/(vii)',
                'Q4 alternatives share C18 plus discretionary2 and E20; exact global awards',
                'Q4 expression bands and strictC<10 / characters<150 lower-scale condition',
                'Q5 alternatives share anyfour×6 plus local4/global2 discretionary and E30; both complete six-heading pools',
                'Q5 expression bands and strictC<15 / characters<200 lower-scale condition',
                'explicit blank', 'explicit blank', 'blank back cover'])),
        },
        'choiceBoundaries': [
            'Required Q1 event, venue and biography pools stay whole; no example earns marks.',
            'Required Q2 accommodation table and kanji/grammar pools stay whole; given table cells are unpriced.',
            'Q2 discussion is one four-detail pool. Both hotels must be referenced; no printed one-per-polarity restriction or numeric omission penalty is invented.',
            'Q4 two scenarios share one40-mark writing grid and topic; one task retains both prompts.',
            'Q5 choose one scenario then anyfour of its six headings, one60-mark task; no cross-scenario combinations or duplicate cards.',
            'Both listening tables remain whole required pools. B1 allfour health suggestions is one8-mark question.',
            'Listening anytwo pools preserve distinct concepts, descending2+1 tariffs and compound turn-right2 plus anytwo×1.',
        ],
        'sourceDiscrepancies': [
            'Q1 PartA has nested A/B subheadings; canonical sections1AA/1AB preserve the printed hierarchy.',
            'Q2A repeats2 for the discussion after Japanese2(i–iii); preserve both source prompts and printed references.',
            'Listening third conversation is Tom in the paper and Haru in the scheme; retain both literal names and disclose the difference.',
            'Listening phone is paperB2(iv) and scheme(v); paper identity retained, whole2-mark tariff unchanged.',
            'Q3B2 last two hiragana items are paper(iv)/(v), scheme(vi)/(vii); whole five-answer pool retained.',
            'Q2 Japanese pool prints２時間オープン while the original passage prints24時間オープン; both original literals independently verified and disclosed, without normalization.',
            'Q1 biography accepts Grand prix as an alternative to Jean Paul(1) Gaultier(1), total2; preserve the printed routes without adding them.',
        ],
        'atlasSourceSpans': {'written1': [2, 3, 4], 'written2': [5, 6, 7, 8], 'written3': [9, 10, 11],
                             'written4': [12, 13, 14], 'written5': [15, 16, 17, 18],
                             'written6': [7], 'written7': [7, 8], 'written8': [11]},
    }


if __name__ == '__main__':
    data = build()
    target = Path(__file__).parent / 'reviews/japanese-2013-hl-census.json'
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(TASKS)} independently counted tasks; {data["checksums"]}')
