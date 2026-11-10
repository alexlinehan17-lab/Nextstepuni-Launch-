#!/usr/bin/env python3
"""Mandatory local 2024 original-source gate, separate from portable tests."""
import hashlib
import json
import re
from paper_census import census_lcvp, leaves_of, continuity_flags
from lcvp_review_2024 import ROOT, REVIEW, VIDEO_URL, documents, build, table_cells, business_options, page_raw, tidy


def verify():
    review = json.loads(REVIEW.read_text())
    for record in review['sources']:
        assert hashlib.sha256((ROOT / record['path']).read_bytes()).hexdigest() == record['sha256'], record['path']
    paper, scheme = documents()
    assert len(paper) == 40 and len(scheme) == 16
    expected = {('A', q, None, None) for q in range(1, 9)}
    expected.add(('B', 1, None, None))
    expected.update(('B', q, None, r) for q, rs in [(2, ['i', 'ii']), (3, ['i', 'ii', 'iii'])] for r in rs)
    split = {(1, 'b'), (1, 'c'), (2, 'a'), (4, 'd'), (7, 'a')}
    expected.update(('C', q, letter, None) for q in range(1, 8) for letter in 'abcd' if (q, letter) not in split)
    expected.update(('C', q, letter, r) for q, letter in split for r in ['i', 'ii'])
    parts, texts, files, marks, stems = census_lcvp('lcvp', 2024, 'cl')
    actual = set(leaves_of(parts))
    assert len(expected) == review['manualOriginalLeaves'] == 47
    assert expected == actual, dict(missing=list(expected - actual), unexpected=list(actual - expected))
    assert sum(marks.values()) == review['offeredPracticeMarks'] == 235
    assert not continuity_flags(parts, texts, 'lcvp')
    cards, _ = build()
    assert len(cards) == review['manualPricedTasks'] == 45
    assert sum(c['totalMarks'] for c in cards) == 235
    assert [sum(c['section'] == s for c in cards) for s in 'ABC'] == [8, 6, 31]
    assert all(c['questionText'] for c in cards)
    by_id = {c['id']: c for c in cards}
    assert all(c['tariffModel']['kind'] == 'fixed' for c in cards)
    assert by_id['lcvp-2024-cl-c7aii']['questionRef'].endswith('Q7(a)')
    assert by_id['lcvp-2024-cl-c7aii']['conceptId'] == 'c7aii'
    assert by_id['lcvp-2024-cl-c7aii']['totalMarks'] == 4
    for cid in ['c2a', 'c7aii']:
        assert by_id['lcvp-2024-cl-' + cid]['questionText'].count('(i)') == 1
        assert by_id['lcvp-2024-cl-' + cid]['questionText'].count('(ii)') == 1
    for cid in ['a6', 'a7']:
        assert by_id['lcvp-2024-cl-' + cid]['rows'][0]['group']['perOption'] == 2
        assert 'expansion needed' in by_id['lcvp-2024-cl-' + cid]['rows'][0]['contextNote']
    assert by_id['lcvp-2024-cl-c3b']['rows'][0]['permittedMarks'] == [0, 2, 4, 6]
    assert 'compulsory point' in by_id['lcvp-2024-cl-c2b']['rows'][1]['verbatim'].lower()
    assert 'compulsory point' in by_id['lcvp-2024-cl-c4dii']['rows'][0]['verbatim'].lower()
    assert len([v for row in table_cells(scheme, 9) for v in row if v]) == 17
    assert len([v for row in table_cells(scheme, 12) for v in row if v]) == 18
    choices = business_options(scheme)
    assert [len(v.split('•')) - 1 for v in choices] == [6, 8]
    assert '€1 million' in choices[0] and 'baby products' in choices[1]
    issues = table_cells(scheme, 10)
    assert len(issues) == 9, issues
    assert 'Housing/homelessness' in issues[1][0] and 'council/politicians' in issues[1][1]
    assert 'Any other relevant point' in issues[-1][0]
    assert 'www.centralbank.ie, 2023' in tidy(page_raw(paper, 16))
    assert 'www.centralbank.ie, 2023' in tidy(page_raw(scheme, 6))
    pattern = re.compile(r'\b(?:choose|choice|one of|any\s+(?:one|two|three|four|five|\d+)|either|both|which one|which option|compulsory)\b', re.I)
    directives = {n: pattern.findall(tidy(page_raw(paper, n))) for n in range(1, 41)}
    directives = {n: v for n, v in directives.items() if v}
    # Page 2 specifies the three compulsory sections and C's four-of-seven
    # outer choice. B3(iii) is one two-option task with one shared grid. The
    # repeated "one of the 4Ps" sentence is information, not a candidate choice.
    assert directives == {2: ['Compulsory', 'Compulsory', 'Compulsory', 'any four'],
                          12: ['Which option', 'choice'], 14: ['one of'], 17: ['one of']}, directives
    assert review['manualOriginalLeaves'] != review['manualPricedTasks']
    media = json.loads((ROOT / 'scripts/markbank/authoring/lcvp/media-inventory-20261110.json').read_text())
    video = next(v for v in media if v['year'] == 2024 and v['sitting'] == 'main')
    assert video['officialDownloadUrl'] == VIDEO_URL
    assert video['headers']['content-type'] == 'video/quicktime'
    assert bytes.fromhex(video['prefixHex'])[4:12] == b'ftypqt  '
    assert all(c['videoMaterial']['canonicalUrl'] == VIDEO_URL for c in cards if c['section'] == 'A')
    return dict(year=2024, sitting='main', sourceHashes='verified', sourcePages=[40, 16, 2],
        manualLeaves=47, rawLeaves=len(actual), tasks=45, marks=235,
        leafKeys=sorted([list(k) for k in actual], key=str), numericHolds=[], continuityFlags=[],
        classifiedSelectionDirectives=directives,
        originalVideo='Official listing, response headers and QuickTime prefix verified; no full-file hash claimed',
        nativePlayback='pending root release QA',
        reconciliation='Independent manual census predates parser/card review. C2(a) and C7(a) each preserve their two related leaves as one coherent profile. All other separately priced original tasks remain separate. The old C7aii identity is retained for its restored whole activity/role task.')


if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
