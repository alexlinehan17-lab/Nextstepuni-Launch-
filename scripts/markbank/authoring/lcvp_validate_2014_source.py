#!/usr/bin/env python3
"""Mandatory original-PDF gate, separate from portable runtime tests."""
import hashlib
import json
import re
import fitz
from paper_census import census_lcvp, leaves_of, continuity_flags
from lcvp_review_2014 import ROOT, REVIEW, CASE, VIDEO_URL, PAGES, documents, build, question, scheme_parts, contrast_models, tidy


def address(value):
    match = re.fullmatch(r'([ABC])(\d+)([abcd]?)(i{0,2})', value)
    assert match, value
    section, number, letter, roman = match.groups()
    return section, int(number), letter or None, roman or None


def verify():
    review = json.loads(REVIEW.read_text())
    for record in review['sources']:
        assert hashlib.sha256((ROOT / record['path']).read_bytes()).hexdigest() == record['sha256']
    paper, scheme = documents()
    case = fitz.open(ROOT / CASE)
    assert [len(paper), len(case), len(scheme)] == [32, 2, 16]
    def case_text(value):
        value = value[value.index('COROBAWN SUMMER FESTIVAL'):]
        return tidy(value)
    main_case, companion = case_text(paper[7].get_text(sort=False)), case_text(case[1].get_text(sort=False))
    assert main_case != companion
    # Precisely declared punctuation difference, not an assertion that these
    # separately hashed source documents are identical or interchangeable.
    assert main_case.replace('The committee, representing the local community,',
                             'The committee representing the local community') == companion
    assert review['caseBookletMatchesPaper'] is False
    manual = {address(row['key']) for row in review['manualPaperLeaves']}
    tasks = {address(row['key']) for row in review['pricedTaskLedger']}
    assert len(manual) == review['manualOriginalLeaves'] == 39
    assert tasks == manual and len(tasks) == review['manualPricedTasks'] == 39
    parts, texts, _, marks, _ = census_lcvp('lcvp', 2014, 'cl')
    assert set(leaves_of(parts)) == manual
    assert not continuity_flags(parts, texts, 'lcvp')
    assert sum(marks.values()) == review['rawReaderAudit']['capturedTariffSum'] == 44
    cards, _ = build()
    assert len(cards) == 39 and sum(c['totalMarks'] for c in cards) == 210
    assert [sum(c['section'] == s for c in cards) for s in 'ABC'] == [8, 5, 26]
    by = {c['id'].removeprefix('lcvp-2014-cl-'): c for c in cards}
    assert {s: c['totalMarks'] for s, c in by.items()} == {r['key'].lower(): r['marks'] for r in review['pricedTaskLedger']}
    assert review['candidateWrittenMarks'] == 160 and review['paperPrintedTariffUnits'] == 35
    assert review['originalMarkBankCards'] == 0 and review['previousAuthoredCards'] == 518
    assert len(review['originalAtlasMemberships']['existingRuntimeIds']) == 17
    def pool(suffix, row=0):
        r = by[suffix]['rows'][row]
        return r['group']['options'] if 'group' in r else r['contextNote'].split('Complete original guidance: ', 1)[1].split(' | ')
    expected = {'a2': 3, 'a3': 4, 'a4': 5, 'a5': 6, 'a6': 8, 'a7': 4, 'a8': 6,
        'b1': 5, 'b2i': 6, 'b2ii': 8, 'b3i': 8, 'b3ii': 7, 'c1b': 6, 'c1c': 2, 'c1d': 7,
        'c2b': 7, 'c2d': 7, 'c3b': 10, 'c3c': 7, 'c3d': 10, 'c4b': 8, 'c4c': 4,
        'c5b': 7, 'c5di': 4, 'c5dii': 5, 'c6a': 7, 'c6b': 8, 'c6c': 8, 'c6d': 6}
    for suffix, count in expected.items():
        assert len(pool(suffix)) == count, (suffix, pool(suffix))
    assert by['a1']['rows'][0]['verbatim'] == 'Student Social Enterprise Awards'
    assert by['a1']['rows'][0]['marks'] == 2
    for suffix, count in [('a6', 2), ('a7', 3)]:
        assert by[suffix]['rows'][0]['group']['claimMax'] == count
        assert by[suffix]['rows'][0]['group']['perOption'] == 2
    assert '€2,000' in pool('a4')[1] and 'career options + valid expansion' in pool('a8')[3]
    case_stem = by['b1']['stem']
    assert case_stem.split('\n\n')[0] == main_case.split(' Visiting Family 6%')[0]
    for card in cards:
        if card['section'] == 'B':
            assert card['stem'] == case_stem
            assert all(t in card['stem'] for t in ['population of 4,000', 'nearly 5,000 visitors', 'The committee, representing the local community,',
                'Great Western Greenway', 'Wild Atlantic Way', 'Exploring Your Roots in Corobawn',
                'Visiting Family 6%', 'Hiking/Hill Walking 38%', 'Golf 24%', 'Gathering Festival 32%'])
            assert card['sourceMaterial']['pages'] == [8]
    assert by['b1']['topicId'] == 'lcvp-link-modules-1-1'
    assert 'packed lunches for walkers' in pool('b2ii')[2]
    for suffix in ['c1c', 'c2c', 'c6c']:
        assert [r['marks'] for r in by[suffix]['rows']] == [3, 3, 3]
        assert all([p['marks'] for p in r['parts']] == [1, 2] for r in by[suffix]['rows'])
        assert all(r['parts'][1]['permittedMarks'] == [0, 1, 2] for r in by[suffix]['rows'])
    assert 'Must be relevant to the career.' in pool('c1c')[-1]
    assert 'OTHER THAN Link Modules' in by['c2c']['rows'][0]['contextNote']
    for suffix in ['c1d', 'c3d']:
        assert len(by[suffix]['rows']) == 3
        assert all([p['permittedMarks'] for p in r['parts']] == [[0, 1], [0, 2]] for r in by[suffix]['rows'])
    agenda = by['c4a']['rows']
    assert [r['marks'] for r in agenda] == [1, 1, 4]
    assert agenda[0]['verbatim'] == 'Heading'
    assert agenda[1]['verbatim'] == 'Election of officers* (Chairperson/Managing Director/Secretary/Treasurer)'
    assert '* Compulsory item' in agenda[1]['contextNote']
    assert len(agenda[2]['group']['options']) == 6 and agenda[2]['group']['claimMax'] == 4
    assert all([p['verbatim'] for p in r['parts']] == ['Resource', 'Explanation'] for r in by['c4c']['rows'])
    assert all(t in pool('c4c')[0] for t in ['Skilled team members', 'Teachers', 'Parents', 'General public'])
    assert [r['marks'] for r in by['c4d']['rows']] == [3, 6] and len(pool('c4d', 1)) == 6
    assert 'Brainstorming in the class' in pool('c4d', 1)[-1]
    assert [p['permittedMarks'] for p in by['c5a']['rows'][0]['parts']] == [[0, 1], [0, 2]]
    assert by['c5cii']['questionText'].endswith('referred to in part (a).')
    assert [r['id'] for r in by['c5cii']['rows']] == ['strengths', 'weaknesses', 'opportunities', 'threats']
    assert [len(pool('c5cii', i)) for i in range(4)] == [4, 3, 4, 3]
    assert all(r['marks'] == 2 and r['permittedMarks'] == [0, 1, 2] for r in by['c5cii']['rows'])
    assert all('No marks for headings. No repetition of points.' in r['contextNote'] for r in by['c5cii']['rows'])
    assert pool('c5cii', 3)[-1] == 'Immigration/no volunteers'
    assert pool('c6a')[4] == 'Adaptible'
    assert 'Each must be explained for the mark' in by['c6a']['rows'][0]['contextNote']
    assert [p['permittedMarks'] for p in by['c6a']['rows'][0]['parts']] == [[0, 1]] * 4
    assert pool('c6d') == contrast_models(scheme)
    assert pool('c6d')[0] == 'Comes up with an idea/sets up the business — Implements entrepeneur’s idea/runs the business on a daily basis'
    assert pool('c6d')[-1] == 'Long term planning — Implements short term plan'
    assert review['heldWholeTaskMarks'] == 0 and review['pricedMarks'] == 210
    for card in cards:
        assert card['tariffModel']['kind'] == 'fixed'
        assert sum(r['marks'] for r in card['rows']) == card['totalMarks'], card['id']
    blocks, alignment = scheme_parts(scheme), []
    for task in PAGES:
        words = set(re.findall(r'[a-z]+', question(paper, task).lower())) - {'the', 'a', 'of', 'to', 'in', 'and', 'is', 'for', 'you', 'your'}
        source_words = set(re.findall(r'[a-z]+', blocks[task].lower()))
        fraction = len(words & source_words) / len(words)
        assert fraction >= .75, (task, fraction, question(paper, task))
        alignment.append(dict(key=list(task), wordingRecall=round(fraction, 4)))
    for card in cards:
        assert not re.search(r'Office use|For Examiner|Page \d+ of 32|\uf0b7', card['questionText'] + ' ' + card['stem']), card['id']
    media = json.loads((ROOT / 'scripts/markbank/authoring/lcvp/media-inventory-20261110.json').read_text())
    video = next(v for v in media if v['year'] == 2014 and v['sitting'] == 'main')
    assert video['officialDownloadUrl'] == VIDEO_URL and video['headers']['content-type'] == 'video/mp4'
    assert bytes.fromhex(video['prefixHex'])[4:12] == b'ftypisom'
    assert all(c['videoMaterial']['canonicalUrl'] == VIDEO_URL and c['additionalSourceMaterials'][0]['pages'] == [2] for c in cards if c['section'] == 'A')
    return dict(year=2014, sitting='main', sourceHashes='verified', sourcePages=[32, 2, 16], manualLeaves=39, rawLeaves=39,
        rawCapturedTariffSum=44, rawTariffLimitation='Older after-answer-space/continuation layout; independent original ledger governs 210 offered marks.',
        tasks=39, marks=210, candidateWrittenMarks=160, pricedMarks=210, heldWholeTaskMarks=0, continuityFlags=[],
        originalMarkBankCards=0, previousAuthoredCards=518, originalAtlasIdentities=17, originalRuntimeIdentities=17,
        caseBookletMatchesPaper=False, caseBookletDifference='Exactly the two commas bracketing representing the local community in the main paper; main-paper punctuation retained.',
        authoredSubsetSha256=hashlib.sha256(json.dumps(cards, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
        wordingAlignment=alignment, originalVideo='Official MP4 listing/headers/prefix verified; no full-file hash or playback claim',
        scope='All 50 original pages independently reviewed first. All 39 tasks/full models retained. Source-bound paired table, complete case/chart, compulsory agenda item, required SWOT categories and explanation conditions checked.')


if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
