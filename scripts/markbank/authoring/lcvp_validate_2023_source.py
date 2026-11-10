#!/usr/bin/env python3
"""Mandatory original-source gate, separate from portable runtime tests."""
import hashlib
import json
import re
from paper_census import census_lcvp, leaves_of, continuity_flags
from lcvp_review_2023 import ROOT, REVIEW, VIDEO_URL, documents, build, research_cells, page_raw, tidy


def verify():
    review = json.loads(REVIEW.read_text())
    for record in review['sources']:
        assert hashlib.sha256((ROOT / record['path']).read_bytes()).hexdigest() == record['sha256']
    paper, scheme = documents()
    assert len(paper) == 40 and len(scheme) == 24
    expected = {('A', q, None, None) for q in range(1, 9)}
    expected.add(('B', 1, None, None))
    expected.update(('B', q, None, r) for q, rs in [(2, ['i', 'ii']), (3, ['i', 'ii', 'iii'])] for r in rs)
    expected.update(('C', q, letter, None) for q in range(1, 8) for letter in 'abcd' if (q, letter) != (5, 'c'))
    expected.update(('C', 5, 'c', r) for r in ['i', 'ii'])
    parts, texts, files, marks, stems = census_lcvp('lcvp', 2023, 'cl')
    actual = set(leaves_of(parts))
    assert len(expected) == review['manualOriginalLeaves'] == 43
    assert expected == actual, dict(missing=list(expected - actual), unexpected=list(actual - expected))
    assert sum(marks.values()) == review['offeredPracticeMarks'] == 235
    assert not continuity_flags(parts, texts, 'lcvp')
    cards, _ = build()
    assert len(cards) == review['manualPricedTasks'] == 43
    assert sum(c['totalMarks'] for c in cards) == 235
    assert [sum(c['section'] == s for c in cards) for s in 'ABC'] == [8, 6, 29]
    by_id = {c['id'].removeprefix('lcvp-2023-cl-'): c for c in cards}
    held = by_id['a6']
    assert held['tariffModel']['kind'] == 'questionTotal' and held['totalMarks'] == 6
    assert len(held['rows']) == 9 and all(r['marks'] is None for r in held['rows'])
    assert 'Award 6 marks to all candidates' in held['rows'][0]['verbatim']
    assert 'Part 2 rather than for Part 3.' in held['rows'][0]['verbatim']
    assert 'Three valid reasons 2 x 3 marks (0/3)' in held['rows'][0]['verbatim']
    assert sum(c['totalMarks'] for c in cards if c['tariffModel']['kind'] == 'fixed') == 229
    assert all(c['tariffModel']['kind'] == 'fixed' for c in cards if c != held)
    cells = research_cells(scheme)
    assert cells[0] == ['Primary/Field', 'Secondary/Desk']
    assert '7. Postal surveys' in cells[1][0] and '4. Press releases etc.' in cells[1][1]
    assert 'Publications/census' not in cells[1][0] and 'Postal surveys' not in cells[1][1]
    for suffix, required in [('b2ii', ['Advantages', 'Disadvantages']), ('c1d', ['Business', 'Consumers'])]:
        assert [r['verbatim'] for r in by_id[suffix]['rows'][:2]] == required
        assert len(by_id[suffix]['rows']) == 3
    assert len(by_id['c4c']['rows']) == 4
    assert all(len(r['parts']) == 2 and r['marks'] == 2 for r in by_id['c4c']['rows'])
    assert all('NO marks for headings' in r['contextNote'] for r in by_id['c4c']['rows'])
    assert [r['marks'] for r in by_id['c5ci']['rows']] == [1, 1, 1]
    assert [r['marks'] for r in by_id['c7b']['rows']] == [1, 6]
    pattern = re.compile(r'\b(?:choose|choice|one of|any\s+(?:one|two|three|four|five|\d+)|either|both|which one|which option|compulsory)\b', re.I)
    directives = {n: pattern.findall(tidy(page_raw(paper, n))) for n in range(1, 41)}
    directives = {n: v for n, v in directives.items() if v}
    assert directives == {2: ['Compulsory', 'Compulsory', 'Compulsory', 'any four'], 9: ['One of', 'one of'], 15: ['both'], 31: ['both']}, directives
    media = json.loads((ROOT / 'scripts/markbank/authoring/lcvp/media-inventory-20261110.json').read_text())
    video = next(v for v in media if v['year'] == 2023 and v['sitting'] == 'main')
    assert video['officialDownloadUrl'] == VIDEO_URL
    assert video['headers']['content-type'] == 'video/quicktime'
    assert bytes.fromhex(video['prefixHex'])[4:12] == b'ftypqt  '
    assert all(c['videoMaterial']['canonicalUrl'] == VIDEO_URL for c in cards if c['section'] == 'A')
    return dict(year=2023, sitting='main', sourceHashes='verified', sourcePages=[40, 24, 2],
        manualLeaves=43, rawLeaves=len(actual), tasks=43, marks=235, explicitlyPricedPracticeMarks=229,
        leafKeys=sorted([list(k) for k in actual], key=str), continuityFlags=[],
        heldPracticeScoring=[dict(task='A6', printedMarks=6, reason='Explicit all-candidates historical award, confidence-only practice; eight original models and full notice retained')],
        classifiedSelectionDirectives=directives,
        originalVideo='Official listing, headers and QuickTime prefix verified; no full-file hash claimed',
        nativePlayback='pending root release QA',
        reconciliation='Independent 66-page visual census predates parser/card inspection. All43 separately priced tasks preserved, including both3-mark C5(c) leaves. C6(a) and C7(b) restored without altering any41 prior identities. Historical universal award is separate from missing-task or release-completeness claims.')


if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
