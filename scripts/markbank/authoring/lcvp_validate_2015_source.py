#!/usr/bin/env python3
"""Explicit mandatory original-source gate; normal runtime tests need no corpus."""
import hashlib
import json
import re
import fitz
from paper_census import census_lcvp, leaves_of, continuity_flags
from lcvp_review_2015 import ROOT, REVIEW, CASE, VIDEO_URL, PAGES, documents, build, question, scheme_parts, contrast_models, tidy


def address(value):
    match = re.fullmatch(r'([ABC])(\d+)([abcd]?)(i{0,3})', value)
    assert match, value
    section, number, letter, roman = match.groups()
    return section, int(number), letter or None, roman or None


def verify():
    review = json.loads(REVIEW.read_text())
    for record in review['sources']:
        assert hashlib.sha256((ROOT / record['path']).read_bytes()).hexdigest() == record['sha256']
    paper, scheme = documents()
    case = fitz.open(ROOT / CASE)
    assert [len(paper), len(case), len(scheme)] == [32, 2, 20]
    def case_text(value):
        value = value[value.index('Recruit Me Ltd'):]
        return tidy(re.sub(r'Page\s+8\s+of\s+32', '', value))
    assert case_text(paper[7].get_text(sort=True)) == case_text(case[1].get_text(sort=True))
    manual = {address(row['key']) for row in review['manualPaperLeaves']}
    tasks = {address(row['key']) for row in review['pricedTaskLedger']}
    assert len(manual) == review['manualOriginalLeaves'] == 43
    assert tasks == manual and len(tasks) == review['manualPricedTasks'] == 43
    parts, texts, _, marks, _ = census_lcvp('lcvp', 2015, 'cl')
    assert set(leaves_of(parts)) == manual
    assert not continuity_flags(parts, texts, 'lcvp')
    assert sum(marks.values()) == review['rawReaderAudit']['capturedTariffSum'] == 44
    cards, _ = build()
    assert len(cards) == 43 and sum(c['totalMarks'] for c in cards) == 210
    assert [sum(c['section'] == s for c in cards) for s in 'ABC'] == [8, 6, 29]
    by = {c['id'].removeprefix('lcvp-2015-cl-'): c for c in cards}
    assert {s: c['totalMarks'] for s, c in by.items()} == {r['key'].lower(): r['marks'] for r in review['pricedTaskLedger']}
    assert review['candidateWrittenMarks'] == 160 and review['paperPrintedTariffUnits'] == 35
    assert review['originalMarkBankCards'] == 0 and review['previousAuthoredCards'] == 475
    assert len(review['originalAtlasMemberships']['existingRuntimeIds']) == 10
    def pool(suffix, row=0):
        r = by[suffix]['rows'][row]
        if 'group' in r:
            return r['group']['options']
        return r['contextNote'].split('Complete original guidance: ', 1)[1].split(' | ')
    expected_pools = {'a2': 3, 'a4': 2, 'a5': 3, 'a6': 4, 'a8': 4, 'b1': 5, 'b2iii': 4, 'b3ii': 6,
        'c1b': 6, 'c1c': 6, 'c1d': 6, 'c2b': 6, 'c2c': 6, 'c2d': 8, 'c3a': 7, 'c3c': 6,
        'c3d': 5, 'c4aii': 9, 'c4b': 7, 'c4cii': 9, 'c4d': 6, 'c5bii': 7, 'c6a': 8, 'c6bii': 8, 'c6c': 9, 'c6d': 9}
    for suffix, count in expected_pools.items():
        assert len(pool(suffix)) == count, (suffix, pool(suffix))
    assert len(pool('a3', 1)) == 4 and [len(pool('a7', i)) for i in [0, 1]] == [4, 5]
    assert by['a3']['rows'][0]['marks'] == 1 and by['a3']['rows'][1]['group']['perOption'] == 2
    assert [r['group']['claimMax'] for r in by['a7']['rows']] == [1, 2]
    assert all(r['group']['perOption'] == 2 for r in by['a7']['rows'])
    for suffix in ['a4', 'a5', 'a6', 'b2iii']:
        assert by[suffix]['rows'][0]['group']['perOption'] == 2
        assert '0 marks' in by[suffix]['rows'][0]['contextNote']
    assert by['a2']['questionText'] == 'Why was this type of business suited to Sylvia?'
    assert 'no prescribed count of reasons' in by['a2']['rows'][0]['contextNote']
    assert all(t in pool('a8')[-1] for t in ['General management', 'Corporate Organisation', 'Finance', 'Business plan', 'Marketing', 'Website planning and design'])
    assert by['b1']['questionText'].count('•') == 5 and '\uf0b7' not in by['b1']['questionText']
    assert len(by['b1']['rows'][0]['parts']) == 3
    case_stem = by['b1']['stem']
    assert len(case_stem) > 3000
    for card in cards:
        if card['section'] == 'B':
            assert card['stem'].startswith(case_stem)
            assert all(t in card['stem'] for t in ['Robert', 'Maria', 'nominal rent', 'SWOT', 'Careers Programme'])
            assert card['sourceMaterial']['pages'] == [8]
    held = by['b2ii']
    assert held['questionText'] == 'Outline a corporate social responsibility policy implemented by Robert and Maria in Recruit Me Ltd.'
    assert held['totalMarks'] == 4 and held['tariffModel']['kind'] == 'questionTotal'
    assert len(held['rows']) == 2
    assert all(r['marks'] is None and not any(k in r for k in ['parts', 'group', 'permittedMarks']) for r in held['rows'])
    assert '2m (0/2)' in held['rows'][0]['verbatim'] and '2 @ 1m' in held['rows'][0]['verbatim']
    assert held['rows'][1]['verbatim'].startswith('They offer support to new start-up enterprises')
    assert held['rows'][1]['contextNote'].startswith('or — Complete second policy alternative.')
    assert all(t in held['rows'][1]['verbatim'] for t in ['fully serviced desks', 'printing, broadband & communications', 'legal and tax issues'])
    assert 'no printed internal allocation' in held['rows'][0]['contextNote']
    assert [p['permittedMarks'] for p in by['b2i']['rows'][0]['parts']] == [[0, 2], [0, 2]]
    assert [p['permittedMarks'] for p in by['b3i']['rows'][0]['parts']] == [[0, 2], [0, 2]]
    assert 'specific to the activity named in part (a)' in by['c1c']['rows'][0]['contextNote']
    assert all([p['verbatim'] for p in r['parts']] == ['Method', 'Explanation', 'Why'] for r in by['c1d']['rows'])
    assert pool('c1d')[-1].endswith('To measure the results against the aims/objectives.')
    assert pool('c2b') == contrast_models(scheme)
    assert contrast_models(scheme)[4] == 'Aim is to help others. — Aim is to produce a product/supply service.'
    assert contrast_models(scheme)[-1] == 'Benefits the community. — Benefits owners/investors'
    assert by['c2b']['questionText'] == 'Explain how a local voluntary body differs from a commercial business.'
    letter = by['c3b']['rows'][0]
    assert [p['marks'] for p in letter['parts']] == [1, 1, 1, 2, 1, 2, 2]
    assert all(p['permittedMarks'] == [0, p['marks']] for p in letter['parts'])
    assert letter['parts'][5]['verbatim'] == 'Closing paragraph (*CV enc)'
    assert '* compulsory item: CV enclosure' in letter['contextNote']
    assert '* compulsory item' in by['c4ci']['rows'][0]['contextNote']
    assert 'A written document*/between an employer and employee' in by['c4ci']['rows'][0]['contextNote']
    assert [r['marks'] for r in by['c5c']['rows']] == [3, 3]
    assert all([p['marks'] for p in r['parts']] == [1, 2] for r in by['c5c']['rows'])
    assert [r['marks'] for r in by['c5d']['rows']] == [6, 6]
    assert all(len(r['parts']) == 6 and all(p['marks'] == 1 for p in r['parts']) for r in by['c5d']['rows'])
    for suffix, labels in [('c6c', ['Statement', 'Disadvantage']), ('c6d', ['Method', 'Use'])]:
        assert len(by[suffix]['rows']) == 4
        assert all([p['verbatim'] for p in r['parts']] == labels for r in by[suffix]['rows'])
    assert 'Speadsheets' in pool('c6d')[6] and 'fianancial statements' in pool('c6d')[6]
    held_cards = [c for c in cards if c['tariffModel']['kind'] == 'questionTotal']
    assert held_cards == [held] and review['heldWholeTaskMarks'] == 4
    priced = [c for c in cards if c not in held_cards]
    assert sum(c['totalMarks'] for c in priced) == review['pricedMarks'] == 206
    for card in priced:
        assert sum(r['marks'] for r in card['rows']) == card['totalMarks'], card['id']
    blocks, alignment = scheme_parts(scheme), []
    for task in PAGES:
        words = set(re.findall(r'[a-z]+', question(paper, task).lower())) - {'the', 'a', 'of', 'to', 'in', 'and', 'is', 'for', 'you', 'your'}
        source_words = set(re.findall(r'[a-z]+', blocks[task].lower()))
        fraction = len(words & source_words) / len(words)
        assert fraction >= .75, (task, fraction, question(paper, task))
        alignment.append(dict(key=list(task), wordingRecall=round(fraction, 4)))
    for card in cards:
        assert not re.search(r'Office use|For Examiner|Page \d+ of 32|\uf0b7|\. \. 4', card['questionText'] + ' ' + card['stem']), card['id']
    media = json.loads((ROOT / 'scripts/markbank/authoring/lcvp/media-inventory-20261110.json').read_text())
    video = next(v for v in media if v['year'] == 2015 and v['sitting'] == 'main')
    assert video['officialDownloadUrl'] == VIDEO_URL and video['headers']['content-type'] == 'video/mp4'
    assert bytes.fromhex(video['prefixHex'])[4:12] == b'ftypisom'
    assert all(c['videoMaterial']['canonicalUrl'] == VIDEO_URL and c['additionalSourceMaterials'][0]['pages'] == [2] for c in cards if c['section'] == 'A')
    return dict(year=2015, sitting='main', sourceHashes='verified', sourcePages=[32, 2, 20], manualLeaves=43, rawLeaves=43,
        rawCapturedTariffSum=44, rawTariffLimitation='Older after-answer-space/continuation layout; independent original ledger governs 210 offered marks.',
        tasks=43, marks=210, candidateWrittenMarks=160, pricedMarks=206, heldWholeTaskMarks=4, continuityFlags=[],
        originalMarkBankCards=0, previousAuthoredCards=475, originalAtlasIdentities=17, originalRuntimeIdentities=10, caseBookletMatchesPaper=True,
        authoredSubsetSha256=hashlib.sha256(json.dumps(cards, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
        wordingAlignment=alignment, originalVideo='Official MP4 listing/headers/prefix verified; no full-file hash or playback claim',
        scope='All 54 original pages independently reviewed first. All 43 tasks/full models retained; B2(ii) keeps both policies as a whole confidence review. Source-bound table cells, bullets and answer-space artifacts checked.')


if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
