#!/usr/bin/env python3
"""Mandatory original-source gate; portable runtime tests do not need the PDFs."""
import hashlib
import json
import re
from paper_census import census_lcvp, leaves_of, continuity_flags
from lcvp_review_2017 import ROOT, REVIEW, VIDEO_URL, PAGES, documents, build, question, scheme_parts, contrast_models, scheme_page_text, tidy


def key(value):
    match = re.fullmatch(r'([ABC])(\d+)([abcd]?)', value)
    assert match, value
    section, number, letter = match.groups()
    return section, int(number), letter or None, None


def verify():
    review = json.loads(REVIEW.read_text())
    for record in review['sources']:
        assert hashlib.sha256((ROOT / record['path']).read_bytes()).hexdigest() == record['sha256']
    paper, scheme = documents()
    assert [len(paper), len(scheme)] == [32, 16]
    manual = {key(row['key']) for row in review['manualPaperLeaves']}
    assert len(manual) == review['manualOriginalLeaves'] == review['manualPricedTasks'] == 38
    parts, texts, files, marks, stems = census_lcvp('lcvp', 2017, 'cl')
    assert set(leaves_of(parts)) == manual
    assert not continuity_flags(parts, texts, 'lcvp')
    # The independent ledger, not this incomplete paper-layout tariff map,
    # determines marks. All 38 task addresses are nevertheless present.
    assert sum(marks.values()) == review['rawReaderAudit']['capturedTariffSum'] == 44
    assert review['offeredPracticeMarks'] == 210 and review['candidateWrittenMarks'] == 160
    cards, _ = build()
    assert len(cards) == 38 and sum(c['totalMarks'] for c in cards) == 210
    assert [sum(c['section'] == s for c in cards) for s in 'ABC'] == [8, 6, 24]
    by = {c['id'].removeprefix('lcvp-2017-cl-'): c for c in cards}
    assert {s: c['totalMarks'] for s, c in by.items()} == {r['key'].lower(): r['marks'] for r in review['pricedTaskLedger']}
    assert review['originalMarkBankCards'] == 0
    assert len(review['originalAtlasMemberships']['existingRuntimeIds']) == 17
    assert by['a2']['rows'][0]['verbatim'] == 'Mixed Bag Gaming'
    assert by['a2']['rows'][0]['marks'] == 2 and 'permittedMarks' not in by['a2']['rows'][0]
    assert by['a3']['questionText'] == 'Why does Emily like to take on work experience students?'
    assert by['a3']['rows'][0]['group']['perOptionSteps'] == [2, 1]
    assert len(by['a3']['rows'][0]['group']['options']) == 3
    assert [r['marks'] for r in by['a5']['rows']] == [1, 3]
    assert by['a5']['rows'][0]['verbatim'] == 'YES/NO'
    assert len(by['a5']['rows'][1]['group']['options']) == 5
    assert len(by['a6']['rows'][0]['group']['options']) == 6
    assert len(by['a7']['rows'][0]['group']['options']) == 7
    assert len(by['a8']['rows'][0]['group']['options']) == 6
    for c in cards:
        if c['section'] == 'B':
            assert c['stem'] == by['b1']['stem'] and len(c['stem']) > 3500
            assert 'Amy graduated from college with a languages degree' in c['stem']
            assert 'future business success.' in c['stem']
            assert c['sourceMaterial']['pages'] == [8]
    assert [by[s]['totalMarks'] for s in ['b2a', 'b2b', 'b2c', 'b3a', 'b3b']] == [2, 6, 4, 2, 10]
    assert by['b2b']['rows'][0]['group']['perOption'] == 2
    assert len(by['b2b']['rows'][0]['group']['options']) == 9
    assert by['b3a']['rows'][0]['group']['options'] == contrast_models(scheme)
    assert len(contrast_models(scheme)) == 10
    assert all(len(v.split(' — ')) == 2 and all(v.split(' — ')) for v in contrast_models(scheme))
    assert 'ENTREPRENEUR — EMPLOYEE' in by['b3a']['rows'][0]['contextNote']
    table_source = tidy(scheme_page_text(scheme, 8))
    assert scheme_page_text(scheme, 8) == scheme[7].get_text(sort=False)
    assert all(tidy(cell) in table_source for pair in contrast_models(scheme) for cell in pair.split(' — ')), 'Every original wrapped cell must remain contiguous in the source transcript'
    assert [r['marks'] for r in by['c1a']['rows']] == [2, 2]
    assert [r['marks'] for r in by['c1b']['rows']] == [2, 2]
    assert by['c1b']['sourceMaterial']['pages'] == [14, 15]
    for number in [1, 4]:
        for letter in 'bcd':
            assert by[f'c{number}a']['questionText'] in by[f'c{number}{letter}']['stem']
    for suffix in ['c1d', 'c2c']:
        assert len(by[suffix]['rows']) == 3
        assert all([p['permittedMarks'] for p in row['parts']] == [[0, 1], [0, 2]] for row in by[suffix]['rows'])
        assert all('1+2(0/2)' in row['contextNote'] for row in by[suffix]['rows'])
    assert [r['marks'] for r in by['c2d']['rows']] == [3, 3, 2]
    assert [[p['marks'] for p in r['parts']] for r in by['c2d']['rows']] == [[1, 2], [1, 2], [1, 1]]
    assert 'Word of mouth' in by['c3d']['rows'][0]['contextNote']
    assert 'Communication/interpersonal skills are improved.' in by['c4d']['rows'][0]['contextNote']
    letter = by['c4c']['rows'][0]
    assert letter['marks'] == 10 and len(letter['parts']) == 10
    assert all(p['marks'] == 1 and p['permittedMarks'] == [0, 1] for p in letter['parts'])
    assert {p['verbatim'] for p in letter['parts']} == {'Own address & Business address', 'Date', 'Opening & closing salutation', 'Introduction', 'Request for permission to visit', 'Date of visit', 'Closing', 'Layout/neatness', 'Spelling', 'Grammar/paragraphs/punctuation'}
    assert 'Team-player' in by['c5d']['rows'][0]['contextNote']
    assert [r['marks'] for r in by['c6b']['rows']] == [2, 2, 2]
    for row in by['c6b']['rows']:
        assert [p['permittedMarks'] for p in row['parts']] == [[0, 1], [0, 1]]
        assert 'group' not in row
        for heading in ['Aims/Objectives', 'Research Methods', 'Analysis of Research', 'Action Steps', 'Schedule of Time', 'Schedule of Costs', 'Evaluation Methods']:
            assert heading in row['contextNote']
        assert 'no marks for headings' in row['contextNote']
    assert [r['marks'] for r in by['c6d']['rows']] == [3, 3, 3]
    for row in by['c6d']['rows']:
        assert [p['marks'] for p in row['parts']] == [1, 1, 1]
        assert [p['verbatim'] for p in row['parts']] == ['Method', 'Statement 1', 'Statement 2']
        assert 'Method +2 statements' in row['contextNote']
    for card in cards:
        assert card['tariffModel']['kind'] == 'fixed'
        assert sum(row['marks'] for row in card['rows']) == card['totalMarks'], card['id']
        assert not re.search(r'Office|Only|Page \d+ of 32|\b1 2\b', card['questionText'] + ' ' + card['stem']), card['id']
    blocks = scheme_parts(scheme)
    alignment = []
    for task in PAGES:
        words = set(re.findall(r'[a-z]+', question(paper, task).lower())) - {'the', 'a', 'of', 'to', 'in', 'and', 'is', 'for', 'you', 'your'}
        source_words = set(re.findall(r'[a-z]+', blocks[task].lower()))
        fraction = len(words & source_words) / len(words)
        assert fraction >= .55, (task, fraction, question(paper, task))
        alignment.append(dict(key=list(task), wordingRecall=round(fraction, 4)))
    media = json.loads((ROOT / 'scripts/markbank/authoring/lcvp/media-inventory-20261110.json').read_text())
    video = next(v for v in media if v['year'] == 2017 and v['sitting'] == 'main')
    assert video['officialDownloadUrl'] == VIDEO_URL and video['headers']['content-type'] == 'video/mp4'
    assert bytes.fromhex(video['prefixHex'])[4:12] == b'ftypmp42'
    assert all(c['videoMaterial']['canonicalUrl'] == VIDEO_URL for c in cards if c['section'] == 'A')
    return dict(year=2017, sitting='main', sourceHashes='verified', sourcePages=[32, 16], manualLeaves=38, rawLeaves=38,
        rawCapturedTariffSum=44, rawTariffLimitation='Tariffs after answer spaces/continuations are omitted by the generic reader; independent original ledger governs.',
        tasks=38, marks=210, candidateWrittenMarks=160, pricedMarks=210, heldWholeTaskMarks=0, continuityFlags=[],
        originalMarkBankCards=0, originalAtlasIdentities=17,
        authoredSubsetSha256=hashlib.sha256(json.dumps(cards, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
        wordingAlignment=alignment, originalVideo='Official MP4 listing/headers/prefix verified; no full-file hash or playback claim',
        scope='All 48 original pages independently reviewed before parser/legacy audit. Full Amy case, all ten paired contrasts, cross-page answer pools, unequal response tariffs and all three open plan headings retained.')


if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
