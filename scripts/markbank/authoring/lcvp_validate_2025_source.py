#!/usr/bin/env python3
"""Mandatory local original-PDF gate; portable runtime tests do not invoke it."""
import hashlib
import json
import re
from paper_census import census_lcvp, leaves_of, continuity_flags
from lcvp_review_2025 import ROOT, REVIEW, VIDEO_URL, documents, build, challenge_cells, page_text


def verify():
    review = json.loads(REVIEW.read_text())
    for record in review['sources']:
        assert hashlib.sha256((ROOT / record['path']).read_bytes()).hexdigest() == record['sha256'], record['path']
    paper, scheme = documents()
    assert len(paper) == 40 and len(scheme) == 20
    expected = {('A', q, None, None) for q in range(1, 9) if q != 6}
    expected.update(('A', 6, None, r) for r in ['i', 'ii'])
    expected.add(('B', 1, None, None))
    expected.update(('B', q, None, r) for q in [2, 3] for r in ['i', 'ii', 'iii'])
    expected.update(('C', q, letter, None) for q in range(1, 8) for letter in 'abcd'
                    if (q, letter) not in [(2, 'a'), (7, 'a')])
    expected.update(('C', q, 'a', r) for q in [2, 7] for r in ['i', 'ii'])
    parts, texts, files, marks, stems = census_lcvp('lcvp', 2025, 'cl')
    actual = set(leaves_of(parts))
    assert len(expected) == review['manualOriginalLeaves'] == 46
    assert expected == actual, dict(missing=list(expected - actual), unexpected=list(actual - expected))
    assert sum(marks.values()) == review['offeredPracticeMarks'] == 235
    assert not continuity_flags(parts, texts, 'lcvp')
    cards, _ = build()
    assert len(cards) == review['manualPricedTasks'] == 45
    assert sum(c['totalMarks'] for c in cards) == 235
    assert [sum(c['section'] == s for c in cards) for s in 'ABC'] == [9, 7, 29]
    assert all(c['questionText'] for c in cards)
    by_id = {c['id']: c for c in cards}
    assert by_id['lcvp-2025-cl-a6i']['questionText'] == 'What resources are needed for the presentation?'
    assert by_id['lcvp-2025-cl-c2a']['questionText'].count('(i)') == 1
    assert by_id['lcvp-2025-cl-c2a']['questionText'].count('(ii)') == 1
    holds = [c['id'] for c in cards if c['tariffModel']['kind'] == 'questionTotal']
    assert holds == ['lcvp-2025-cl-b1']
    assert all(r['marks'] is None for cid in holds for r in by_id[cid]['rows'])
    assert by_id['lcvp-2025-cl-a2']['rows'][0]['permittedMarks'] == [0, 2]
    cells = challenge_cells(scheme)
    names = ['Funding', 'Staffing', 'Location', 'Competition', 'Brexit/ U.S. Tariffs',
             'Increasing Business Costs', 'Customer relations', 'Technology']
    endings = ['make workers redundant', 'necessary skills', 'services option', 'other countries',
               'locally where possible', 'more efficient', 'good customer service', 'stay informed']
    assert all(v.startswith(n) and v.endswith(e) for v, n, e in zip(cells, names, endings))

    # Fail on new selection wording, including repeated overview and contextual
    # open choices. These classifications follow the independent visual sweep.
    pattern = re.compile(r'\b(?:choose|choice|one of|any\s+(?:one|two|three|four|five|\d+)|either|both|which one|one specific|two advantages and two disadvantages)\b', re.I)
    directives = {n: pattern.findall(page_text(paper, n)) for n in range(1, 41)}
    directives = {n: v for n, v in directives.items() if v}
    assert directives == {2: ['any four'], 11: ['which one'], 12: ['one specific'],
        14: ['any four', 'choice', 'choice'], 15: ['choice', 'two advantages and two disadvantages'],
        19: ['choice'], 20: ['choice'], 28: ['choice'], 32: ['two advantages and two disadvantages']}, directives
    media = json.loads((ROOT / 'scripts/markbank/authoring/lcvp/media-inventory-20261110.json').read_text())
    video = next(v for v in media if v['year'] == 2025 and v['sitting'] == 'main')
    assert video['officialDownloadUrl'] == VIDEO_URL
    assert video['headers']['content-type'] == 'video/quicktime'
    assert video['headers']['content-range'].endswith('/506475995')
    assert bytes.fromhex(video['prefixHex'])[4:12] == b'ftypqt  '
    assert all(c['videoMaterial']['canonicalUrl'] == VIDEO_URL for c in cards if c['section'] == 'A')
    return dict(year=2025, sitting='main', sourceHashes='verified', sourcePages=[40, 20, 2],
        manualLeaves=46, rawLeaves=len(actual), tasks=45, marks=235,
        leafKeys=sorted([list(k) for k in actual], key=str), numericHolds=holds,
        continuityFlags=[], classifiedSelectionDirectives=directives,
        originalVideo='Official listing, response headers and QuickTime prefix verified; no full-file hash claimed',
        nativePlayback='pending root release QA',
        reconciliation='Manual census predates parser/card review. C2(a) preserves two subject/explanation leaves as one coherent task. A6(i)/(ii) and C7(a)(i)/(ii) remain separately priced tasks. All source tasks are present; the B1 numeric allocation hold is not a coverage exclusion.')


if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
