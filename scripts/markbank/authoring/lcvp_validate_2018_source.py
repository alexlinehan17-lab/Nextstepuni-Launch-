#!/usr/bin/env python3
"""Explicit original-PDF authoring gate, separate from portable runtime tests."""
import hashlib
import json
import re
from paper_census import census_lcvp, leaves_of, continuity_flags
from lcvp_identity import ORIGINAL_CONCEPT_IDS
from lcvp_review_2018 import ROOT, REVIEW, VIDEO_URL, PAGES, ADDED_IDS, documents, build, question, scheme_parts


def key(value):
    match = re.fullmatch(r'([ABC])(\d+)([abcd]?)(iv|i{1,3})?', value)
    assert match, value
    section, number, letter, roman = match.groups()
    return section, int(number), letter or None, roman


def verify():
    review = json.loads(REVIEW.read_text())
    for record in review['sources']:
        assert hashlib.sha256((ROOT / record['path']).read_bytes()).hexdigest() == record['sha256']
    paper, scheme = documents()
    assert [len(paper), len(scheme)] == [36, 20]
    manual = {key(row['key']) for row in review['manualPaperLeaves']}
    assert len(manual) == review['manualOriginalLeaves'] == 43
    parts, texts, files, marks, stems = census_lcvp('lcvp', 2018, 'cl')
    assert set(leaves_of(parts)) == manual
    assert sum(marks.values()) == review['offeredPracticeMarks'] == 210
    assert not continuity_flags(parts, texts, 'lcvp')
    assert review['candidateWrittenMarks'] == 160
    cards, _ = build()
    assert len(cards) == review['manualPricedTasks'] == 40
    assert sum(c['totalMarks'] for c in cards) == 210
    assert [sum(c['section'] == s for c in cards) for s in 'ABC'] == [8, 5, 27]
    by = {c['id'].removeprefix('lcvp-2018-cl-'): c for c in cards}
    original = [c for c in cards if c['id'] in ORIGINAL_CONCEPT_IDS]
    assert len(original) == 32
    for card in original:
        assert card['conceptId'] == ORIGINAL_CONCEPT_IDS[card['id']]
    assert {c['id'] for c in cards} - {c['id'] for c in original} == ADDED_IDS
    assert sum(c['totalMarks'] for c in cards if c['id'] in ADDED_IDS) == 45
    ledger = {row['key'].lower(): row['marks'] for row in review['pricedTaskLedger']}
    assert {suffix: c['totalMarks'] for suffix, c in by.items()} == ledger
    assert [by[s]['totalMarks'] for s in ['c1bi', 'c1bii']] == [2, 2]
    for suffix in ['c1bi', 'c1bii']:
        assert 'Describe two examples of enterprise in action in each of the following.' in by[suffix]['stem']
    assert [by[s]['rows'][0]['group']['options'] for s in ['a2']] == [['Price', 'Promotion', 'Place']]
    assert by['a4']['rows'][0]['group']['perOption'] == 2
    assert by['a4']['rows'][0]['group']['claimMax'] == 2
    assert len(by['a4']['rows'][0]['group']['options']) == 3
    assert [r['marks'] for r in by['a8']['rows']] == [2, 4]
    assert len(by['a8']['rows'][0]['group']['options']) == 2
    assert len(by['a8']['rows'][1]['parts']) == 2
    assert 'creating hyperlinks' in by['a8']['rows'][1]['contextNote']
    assert by['b1']['rows'][0]['group']['claimMax'] == 3
    assert len(by['b1']['rows'][0]['group']['options']) == 4
    assert 'Corporate Social Responsibility' in by['b1']['questionText']
    assert [r['marks'] for r in by['b2i']['rows']] == [4, 4]
    assert [len(r['group']['options']) for r in by['b2i']['rows']] == [6, 6]
    assert len(by['b2ii']['rows'][0]['group']['options']) == 9
    assert [r['marks'] for r in by['b3i']['rows']] == [2, 2, 2]
    for row in by['b3i']['rows']:
        assert len(row['parts']) == 2 and all(p['permittedMarks'] == [0, 1] for p in row['parts'])
        assert 'group' not in row
    assert 'A minimum of 2 in each area' in by['b3i']['rows'][0]['contextNote']
    assert 'credited only once' in by['b3i']['rows'][0]['contextNote']
    assert '2+4, 3+3 or 4+2' in by['b3i']['rows'][2]['contextNote']
    assert by['b3ii']['rows'][0]['group']['perOption'] == 2
    assert len(by['b3ii']['rows'][0]['group']['options']) == 8
    assert by['c1a']['rows'][0]['parts'][0]['permittedMarks'] == [0, 2]
    assert [len(by[s]['rows'][0]['group']['options']) for s in ['c1bi', 'c1bii']] == [6, 5]
    assert len(by['c1c']['rows']) == 2
    for row in by['c1c']['rows']:
        assert [p['marks'] for p in row['parts']] == [1, 3]
    for name in ['Local Enterprise Office/LEO/CEB', 'Enterprise Ireland', 'Local Area Partnerships', 'ETB’s/SOLAS/FAS', 'Leader Plus', 'Teagasc', 'Udaras Na Gaeltacha', 'Failte Ireland', 'IDA Ireland', 'Intertrade Ireland', 'Bord Bia', 'Glas']:
        assert name in by['c1c']['rows'][0]['contextNote'], name
    assert [len(r['group']['options']) for r in by['c1d']['rows']] == [8, 8, 4]
    assert [r['marks'] for r in by['c2a']['rows']] == [1, 2]
    assert by['c2bii']['rows'][0]['group']['perOptionSteps'] == [2, 1]
    assert len(by['c2bii']['rows'][0]['group']['options']) == 5
    assert by['c2bi']['questionText'] in by['c2bii']['stem']
    assert 'ONE' in by['c2bii']['rows'][0]['contextNote']
    assert [r['marks'] for r in by['c2d']['rows']] == [4, 4]
    assert '2 routes to same profession' in by['c2d']['rows'][1]['verbatim']
    assert [r['marks'] for r in by['c3b']['rows']] == [2, 2, 2, 2]
    assert '1 specific point to tidy towns' in by['c3b']['rows'][0]['contextNote']
    assert 'No marks for headings' in by['c3b']['rows'][0]['contextNote']
    assert 'No repetition of points' in by['c3b']['rows'][0]['contextNote']
    assert len(by['c4ai']['rows'][0]['group']['options']) == 8
    assert by['c4ai']['rows'][0]['group']['options'][-1] == 'FORÁS'
    assert [r['marks'] for r in by['c4c']['rows']] == [3, 3]
    assert [len(r['group']['options']) for r in by['c4c']['rows']] == [6, 7]
    assert by['c5a']['rows'][0]['group']['perOption'] == 2
    assert by['c5a']['stem'] == 'You are part of your LCVP class committee to plan upcoming activities.'
    assert [r['verbatim'] for r in by['c6b']['rows']] == ['A combination of', 'Product', 'Price', 'Place', 'Promotion', 'to achieve goals, sell a product/service']
    assert [r['marks'] for r in by['c6b']['rows']] == [1] * 6
    held = [c for c in cards if c['tariffModel']['kind'] == 'questionTotal']
    assert [c['id'] for c in held] == ['lcvp-2018-cl-c6c']
    assert held[0]['totalMarks'] == 8
    assert [r['verbatim'] for r in held[0]['rows']] == ['Market research/target market', 'Product/Packaging/USP/design', 'Price', 'Place', 'Promotion']
    for row in held[0]['rows']:
        assert row['marks'] is None and 'parts' not in row and 'group' not in row
    for text in ['2 points under each heading', 'No marks for headings', '4@2(1+1)', 'confidence review only']:
        assert text in held[0]['rows'][0]['contextNote']
    for card in cards:
        assert not re.search(r'\bExaminer\b|\bpage running\b|\bonly\b', card['questionText'] + ' ' + card['stem']), card['id']
        if card not in held:
            assert sum(row['marks'] for row in card['rows']) == card['totalMarks'], card['id']
    blocks = scheme_parts(scheme)
    alignment = []
    for task in PAGES:
        words = set(re.findall(r'[a-z]+', question(paper, task).lower())) - {'the', 'a', 'of', 'to', 'in', 'and', 'is', 'for', 'you', 'your'}
        source_words = set(re.findall(r'[a-z]+', blocks[task].lower()))
        fraction = len(words & source_words) / len(words)
        assert fraction >= .55, (task, fraction, question(paper, task))
        alignment.append(dict(key=list(task), wordingRecall=round(fraction, 4)))
    media = json.loads((ROOT / 'scripts/markbank/authoring/lcvp/media-inventory-20261110.json').read_text())
    video = next(v for v in media if v['year'] == 2018 and v['sitting'] == 'main')
    assert video['officialDownloadUrl'] == VIDEO_URL and video['headers']['content-type'] == 'video/mp4'
    assert bytes.fromhex(video['prefixHex'])[4:12] == b'ftypmp42'
    assert all(c['videoMaterial']['canonicalUrl'] == VIDEO_URL for c in cards if c['section'] == 'A')
    return dict(year=2018, sitting='main', sourceHashes='verified', sourcePages=[36, 20], manualLeaves=43, rawLeaves=43,
        tasks=40, marks=210, candidateWrittenMarks=160, pricedMarks=202, heldWholeTaskMarks=8, continuityFlags=[],
        originalIdsAndConceptsRetained=32, restoredIds=sorted(ADDED_IDS),
        authoredSubsetSha256=hashlib.sha256(json.dumps(cards, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
        wordingAlignment=alignment, originalVideo='Official MP4 listing/headers/prefix verified; no whole-file hash or playback claim',
        scope='All 56 original pages independently reviewed before parser/legacy audit. B1 four printed options remain one choose-three task; C1bi/C1bii remain separate source-priced original roman identities with full parent context. C6c eight marks held whole-task confidence-only; all five headings and conflicting instructions retained.')


if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
