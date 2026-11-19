#!/usr/bin/env python3
"""Mandatory local original-source gate, deliberately separate from CI tests."""
import hashlib
import json
from paper_census import census_lcvp, leaves_of, continuity_flags
from lcvp_review_2026 import ROOT, REVIEW, documents, build


def verify():
    review = json.loads(REVIEW.read_text())
    for record in review['sources']:
        assert hashlib.sha256((ROOT / record['path']).read_bytes()).hexdigest() == record['sha256'], record['path']
    video = ROOT / 'tmp/pdfs/lcvp-review/2026-main/LC462CLP031EV.mov'
    assert video.stat().st_size == review['video']['bytes']
    digest = hashlib.sha256()
    with video.open('rb') as original:
        while chunk := original.read(1024 * 1024):
            digest.update(chunk)
    assert digest.hexdigest() == review['video']['sha256'], video
    paper, scheme = documents()
    assert len(paper) == 40 and len(scheme) == 22
    expected = {('A', q, None, None) for q in range(1, 9)}
    expected.add(('B', 1, None, None))
    expected.update(('B', q, None, r) for q in [2, 3] for r in ['i', 'ii', 'iii'])
    expected.update(('C', q, letter, None) for q in range(1, 8) for letter in 'abcd'
                    if (q, letter) not in [(5, 'a'), (7, 'b')])
    expected.update(('C', q, letter, r) for q, letter in [(5, 'a'), (7, 'b')] for r in ['i', 'ii'])
    parts, texts, files, marks, stems = census_lcvp('lcvp', 2026, 'cl')
    actual = set(leaves_of(parts))
    assert len(expected) == review['manualOriginalLeaves'] == 45
    assert expected == actual, dict(missing=list(expected - actual), unexpected=list(actual - expected))
    assert sum(marks.values()) == review['offeredPracticeMarks'] == 235
    cards, _ = build()
    assert len(cards) == review['manualPricedTasks'] == 44
    assert sum(c['totalMarks'] for c in cards) == 235
    assert [sum(c['section'] == s for c in cards) for s in 'ABC'] == [8, 7, 29]
    assert all(c['questionText'] for c in cards)
    by_id = {c['id']: c for c in cards}
    assert by_id['lcvp-2026-cl-a8']['questionText'] == 'Describe the factors that contribute to the success of a business.'
    assert by_id['lcvp-2026-cl-c5a']['questionText'].count('(i)') == 1
    assert by_id['lcvp-2026-cl-c5a']['questionText'].count('(ii)') == 1
    holds = [c['id'] for c in cards if c['tariffModel']['kind'] == 'questionTotal']
    assert holds == ['lcvp-2026-cl-a2', 'lcvp-2026-cl-c5d']
    assert all(r['marks'] is None for cid in holds for r in by_id[cid]['rows'])
    return dict(year=2026, sitting='main', sourceHashes='verified', sourcePages=[40, 22, 2],
        manualLeaves=45, rawLeaves=len(actual), tasks=44, marks=235,
        originalVideoHash='verified', nativePlayback='pending root release QA',
        leafKeys=sorted([list(k) for k in actual], key=str), numericHolds=holds,
        continuityFlags=continuity_flags(parts, texts, 'lcvp'),
        reconciliation='Manual census predates parser/card review. C5(a) keeps two original leaves as one coherent career/qualification task. The two numeric holds retain every source task/model; these are not coverage exclusions.')


if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
