#!/usr/bin/env python3
"""Independent 2015 Ordinary inventory after a complete forty-page visual sweep."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
    ('paper', 'examiner-reports/japanese/papers/2015-ol-000-paper.pdf', 'f879d2104da262a0d71d0b35fe4e8b96663005919a79de7e985437311ddbaae4'),
    ('aural', 'examiner-reports/japanese/papers/2015-ol-A00-paper.pdf', '4182135287021fe369c51c80cdb12a9c1d87b8bcbdf6b859995a005c6d72ca91'),
    ('scheme', 'examiner-reports/japanese/schemes/2015-ol.pdf', 'a61a77888865f54df92faadfbde180cf052ab549a5f17a255856961808da22e8'),
]
TASKS = []


def task(section, q, marks, paper_page, scheme_pages, atlas, roman=None):
    component = 'aural' if section.startswith('L') else 'paper'
    TASKS.append({'key': [section, q, None, roman], 'marks': marks, 'component': component,
                  'paperPages': [paper_page], 'schemePages': scheme_pages,
                  'atlas': {'fileid': f'LC058GLP{"A00" if component == "aural" else "000"}EV.pdf', 'questionNumber': str(atlas)}})


def build():
    for q, marks in [(1, 10), (2, 10), (3, 4), (5, 2)]:
        task('1', q, marks, 3, [5], q)
    for roman in ['i', 'ii']:
        task('1', 4, 2, 3, [5], 4, roman)
    for q, marks in [(1, 6), (2, 4), (3, 2)]:
        task('2A', q, marks, 5, [6], q + 5)
    task('2B', None, 15, 5, [6], 9)
    task('2C', None, 10, 6, [7], 10)
    task('2D', None, 4, 7, [7], 19)
    for q in [1, 2]:
        task('3A', q, 4, 9, [8], q + 10)
    for roman in ['i', 'ii', 'iii', 'iv']:
        task('3A', 3, 3, 9, [8], 13, roman)
    for roman in ['i', 'ii', 'iii']:
        task('3A', 4, 3, 9, [8], 14, roman)
    for q in [1, 2]:
        task('3B', q, 10, 10, [9], q + 14)
    task('4', None, 30, 11, [10], 17)
    task('5', None, 50, 12, [10, 11], 18)
    for q, marks in [(1, [2, 4, 4]), (2, [2, 4, 4]), (3, [4, 4])]:
        for roman, value in zip(['i', 'ii', 'iii'], marks):
            task('LA', q, value, 2, [3], q, roman)
    for q, count, atlas in [(1, 3, 7), (2, 2, 8), (3, 1, 9)]:
        for roman in ['i', 'ii', 'iii'][:count]:
            task('LB', q, 4, 3, [3], atlas, roman)
    for q, atlas in [(1, 10), (2, 11)]:
        for roman in ['i', 'ii', 'iii']:
            task('LC', q, 4, 4, [4], atlas, roman)
    for q, atlas in [(1, 12), (2, 13), (3, 14), (4, 4), (5, 5), (6, 6)]:
        task('LD', q, 4, 5, [4], atlas)
    assert len(TASKS) == 51
    totals = {name: sum(t['marks'] for t in TASKS if condition(t)) for name, condition in [
        ('reading', lambda t: t['key'][0][0] in '123'), ('writing', lambda t: t['key'][0][0] in '45'),
        ('listening', lambda t: t['component'] == 'aural'), ('total', lambda t: True)]}
    assert totals == {'reading': 120, 'writing': 80, 'listening': 100, 'total': 300}, totals
    sources = []
    for component, path, sha256 in SOURCES:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha256
        sources.append({'component': component, 'path': path, 'sha256': sha256})
    return {'subjectId': 'japanese', 'year': 2015, 'level': 'ol', 'reviewedAt': '2026-11-09',
            'method': 'Independent full visual sweep of all sixteen written, eight aural and sixteen scheme physical pages before authoring. Required pools and profile fields remain whole; independent separately priced comprehension responses retain their source boundaries.',
            'sources': sources, 'tasks': TASKS, 'checksums': totals,
            'candidateMaximum': {'written': 200, 'listening': 100, 'total': 300, 'writingChoice': 'All five written questions required; Q4 all ten cloze blanks with each bank word used once; Q5 any five of seven independent responses.'},
            'pageRoles': {
                'paper': dict(zip(map(str, range(1, 17)), [
                    'cover: written200, all five questions required',
                    'Q1 full Senseinavi webpage: eight links, teacher profile, likes, four lesson prices and day off',
                    'Q1 all five required links and five profile fields; choose-two hobbies; two independent prices and day-off task',
                    'Q2 full J-pop posts by Ronan, Marie and Paul, pictures, underline cues and vocabulary',
                    'Q2A required three-artist matching, two countries and one leader detail; Q2B all five truth/Japanese-evidence pairs',
                    'Q2C all ten kanji meanings with all Irish/English distractors and given example',
                    'Q2D open culture prompt: other examples of Japanese pop culture',
                    'Q3 both complete emails between Dara and Hina, dates, addresses, underlined expressions and vocabulary',
                    'Q3A required Dara/Hina interests, four separate multiple choices and three Japanese answers',
                    'Q3B all five present forms and all five particle selections with examples and underline cues',
                    'Q4 ten required cloze blanks, complete bank, given example and each-word-once instruction',
                    'Q5 seven weekend/place prompts, answer any five, full vocabulary',
                    'explicit blank', 'explicit blank', 'explicit blank', 'explicit blank back cover'])),
                'aural': dict(zip(map(str, range(1, 9)), [
                    'cover: listening100, answer all questions in English',
                    'A three speeches: eight tasks with complete multiple-choice options',
                    'B three radio items: six tasks, all distractors and phone grid with four missing digits',
                    'C two campus/hospital conversations: six tasks with all distractors',
                    'D friends conversation: six tasks with all distractors',
                    'explicit blank', 'explicit blank', 'explicit blank back cover'])),
                'scheme': dict(zip(map(str, range(1, 17)), [
                    'cover', 'general examiner guidance',
                    'listening general Japanese/romaji/script half credit; all A28 and B24 tariffs, whole phone4',
                    'all C24 and D24 tariffs; C2i full4/feels-sick2 partial',
                    'general reading inappropriate-language half credit; all Q1 tariffs, surname1/given-name1 and whole required pools',
                    'Q2A matching6, countries4 with Japan1 partial, leader2; all five truth1/quote2 pairs15',
                    'Q2C ten meanings1each; Q2D any two unprinted culture points2each',
                    'Q3A explicit two-part interest allocations4each, four multiple choices3each and three Japanese answers3each',
                    'Q3B two five-item pools2each',
                    'Q4 ten cloze blanks3each with unused-elsewhere alternatives; Q5 any five of seven C5/E5 and full content bands',
                    'Q5 full expression bands and per-response Ecap3 when own C<=3',
                    'transcript A and B1/B2', 'transcript B3 and C', 'C end and full D transcript',
                    'explicit blank', 'back cover'])),
            },
            'sourceDiscrepancies': [
                {'task': '3A4(i)', 'paperPages': [8, 9], 'schemePages': [8], 'description': 'The scheme prints (ちょっと) むじかしいです。 while the original email prints むずかしいですね。 Both original spellings remain visible; no new penalty is inferred.'},
                {'task': 'Q4', 'paperPages': [11], 'schemePages': [10], 'description': 'The original bank prints 日本りょうり, scheme blank(i) 日本りようり and blank(iv) alternate 日本料理. One exact local bank binding preserves all spellings visibly and enforces the printed each-word-once condition; no global normalization.'},
                {'task': 'Q5(v)', 'paperPages': [12], 'schemePages': [10, 11], 'description': 'The scheme repeats the question with どうやった; the paper prints どうやって. The original paper question and common C5/E5 rubric remain; no invented correction or penalty.'},
            ],
            'choiceBoundaries': [
                'Q1 links: all five required at2each, example unpriced. Teacher profile stays one10-mark task: surname1/given-name1 plus four2-mark fields. Hobbies choose two of three2each; prices are independently printed2 each; day off2.',
                'Q2A1 all three artist/person matches2each stay one6-mark task. Countries choose two full details2each, with Japan1 as a separately named partial country. Leader choose one of four2each. Five required truth1/evidence2 pairs, all ten kanji1each and culture any two unprinted points2each each remain one complete task.',
                'Q3A1 explicitly prices Judo2 plus Aikido/rugby2; A2 Kendo2 plus badminton/shopping2. Preserve those source component allocations, not an invented generic choose-two pool. Four multiple-choice tasks3each and three Japanese tasks3each. Both required grammar pools have five answers2each.',
                'Q4 all ten cloze blanks3each stay one card. Each word used once. Exact source exceptions: school at blanki; loves/Japanese food at blankiv; by bus at blankviii, each only if unused elsewhere. The bank spelling 日本りょうり and source alternate 日本料理 are pinned and visibly retained as the same local bank token; no global spelling normalization.',
                'Q5 any five of seven independent responses, each content5/expression5, with complete printed bands and own expression capped3 where own content<=3. No inherited whole-essay writing rule.',
                'Listening has26 separately priced tasks: A8/B6/C6/D6 and28/24/24/24 marks. All MCQ distractors retained. Phone03-6576-8180 has one whole4-mark tariff with four blanks; no per-digit tariff is inferred. C2i full alternatives4/feels-sick2 share one response, never added together.',
                'General reading half credit is printed on the reading heading and applies to all23 reading tasks. Listening names Japanese/romaji/script. No extraneous-material or writing language penalty is published here.',
                'All19 written and14 aural Atlas question numbers, labels and regions retained. Verified scheme bounds17to16 only. No old cards/aliases are removed and no exclusions count as completion.',
            ]}


if __name__ == '__main__':
    result = build()
    (Path(__file__).parent / 'reviews/japanese-2015-ol-census.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(TASKS)} independently counted tasks; {result["checksums"]}')
