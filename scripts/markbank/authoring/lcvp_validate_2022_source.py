#!/usr/bin/env python3
"""Mandatory original-source gate; portable runtime tests use committed data."""
import hashlib
import json
import re
from paper_census import census_lcvp, leaves_of, continuity_flags
from lcvp_review_2022 import ROOT, REVIEW, VIDEO_URL, documents, build, comparison_cells, email_source, page_raw, tidy, csr_pools, scheme_parts


def verify():
    review = json.loads(REVIEW.read_text())
    for record in review['sources']:
        assert hashlib.sha256((ROOT / record['path']).read_bytes()).hexdigest() == record['sha256']
    paper, scheme = documents()
    assert len(paper) == 40 and len(scheme) == 23
    expected = {('A', q, None, None) for q in range(1, 9)}
    expected.add(('B', 1, None, None))
    expected.update(('B', q, None, r) for q in [2, 3] for r in ['i', 'ii', 'iii'])
    split = {(2, 'a'), (6, 'a'), (7, 'd')}
    expected.update(('C', q, letter, None) for q in range(1, 8) for letter in 'abcd' if (q, letter) not in split)
    expected.update(('C', q, letter, r) for q, letter in split for r in ['i', 'ii'])
    parts, texts, files, marks, stems = census_lcvp('lcvp', 2022, 'cl')
    actual = set(leaves_of(parts))
    assert len(expected) == review['manualOriginalLeaves'] == 46
    assert expected == actual, dict(missing=list(expected - actual), unexpected=list(actual - expected))
    assert sum(marks.values()) == review['offeredPracticeMarks'] == 230
    assert review['candidateWrittenMarks'] == 130
    assert not continuity_flags(parts, texts, 'lcvp')
    cards, _ = build()
    assert len(cards) == review['manualPricedTasks'] == 45
    assert sum(c['totalMarks'] for c in cards) == 230
    assert [sum(c['section'] == s for c in cards) for s in 'ABC'] == [8, 7, 30]
    assert all(c['tariffModel']['kind'] == 'fixed' for c in cards)
    by_id = {c['id'].removeprefix('lcvp-2022-cl-'): c for c in cards}
    assert by_id['a5']['rows'][0]['group']['claimMax'] == 4
    pools = csr_pools(scheme_parts(scheme, raw=True)[('A', 6, None, None)])
    assert [len(v) for v in pools.values()] == [7, 7, 6, 8]
    for name in pools:
        assert name in by_id['a6']['questionText'] and name in by_id['a6']['rows'][0]['contextNote']
    assert len(by_id['a6']['rows'][0]['parts']) == 6
    assert by_id['b2ii']['rows'][0]['group']['options'] == ['Website development and maintenance', 'Digital marketing', 'Product Promotion', 'Cyber Security']
    assert by_id['b2ii']['questionText'] in by_id['b2iii']['stem']
    assert len(by_id['b2iii']['rows']) == 4
    assert [r['marks'] for r in by_id['c1c']['rows']] == [2, 5, 1]
    assert 'Dec 2nd night of show' in by_id['c1c']['rows'][1]['contextNote']
    assert 'Evaluation of activity' in by_id['c1c']['rows'][1]['contextNote']
    assert '(i)' in by_id['c2a']['questionText'] and '(ii)' in by_id['c2a']['questionText']
    assert [r['marks'] for r in by_id['c2d']['rows']] == [4, 4, 1]
    assert [len(by_id['c2d']['rows'][i]['group']['options']) for i in [0, 1]] == [11, 9]
    assert '9 to 5.' in by_id['c2d']['rows'][0]['group']['options'][6]
    assert by_id['c3a']['rows'][0]['permittedMarks'] == [0, 2, 4]
    assert all([p['marks'] for p in row['parts']] == [2, 1] for row in by_id['c5d']['rows'])
    cells = comparison_cells(scheme)
    assert len(cells) == 7 and cells[0] == ['Voluntary Organisation', 'Commercial Business']
    assert cells[-1] == ['Benefits the community.', 'Benefits owners/investors.']
    model, labels, summary = email_source(scheme)
    assert labels == ['To: email address', 'Subject line', 'Salutation', 'Introduction', 'Reason for email', 'Availability', 'Concluding statement', 'Closing']
    assert [r['verbatim'] for r in by_id['c6c']['rows']] == labels
    assert model in by_id['c6c']['rows'][0]['contextNote']
    assert model.endswith('Rebecca O’Sullivan') and 'Summary of marks' not in model
    pattern = re.compile(r'\b(?:choose|choice|one of|any\s+(?:one|two|three|four|five|\d+)|either|both|which one|which option|which of|compulsory)\b', re.I)
    directives = {n: pattern.findall(tidy(page_raw(paper, n))) for n in range(1, 41)}
    directives = {n: v for n, v in directives.items() if v}
    assert directives == {2: ['any three', 'any four'], 6: ['which of'], 9: ['any three', 'any four'],
                          10: ['both'], 15: ['any three', 'any four'], 16: ['choice', 'choose'], 21: ['choice', 'choose']}, directives
    media = json.loads((ROOT / 'scripts/markbank/authoring/lcvp/media-inventory-20261110.json').read_text())
    video = next(v for v in media if v['year'] == 2022 and v['sitting'] == 'main')
    assert video['officialDownloadUrl'] == VIDEO_URL
    assert video['headers']['content-type'] == 'video/quicktime'
    assert bytes.fromhex(video['prefixHex'])[4:12] == b'ftypqt  '
    assert all(c['videoMaterial']['canonicalUrl'] == VIDEO_URL for c in cards if c['section'] == 'A')
    return dict(year=2022, sitting='main', sourceHashes='verified', sourcePages=[40, 23, 2],
        manualLeaves=46, rawLeaves=len(actual), tasks=45, marks=230, candidateWrittenMarks=130,
        leafKeys=sorted([list(k) for k in actual], key=str), continuityFlags=[], numericHolds=[],
        classifiedSelectionDirectives=directives,
        originalVideo='Official listing, headers and QuickTime prefix verified; no whole-file hash claimed',
        nativePlayback='pending root release QA',
        reconciliation='Independent65-page visual census predates parser/card review. C2(a) career and same-career duties form one coherent profile; all other separately priced tasks remain distinct. COVID route is A30+B25+threeC OR A30+fourC. All38 prior identities retained; seven omissions restored. Footer detection uses actual centred footer geometry, preserving the right-hand3x1m allocation and all four B2(ii) models. Numbered lists use original line boundaries where prose contains9to5.')


if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
