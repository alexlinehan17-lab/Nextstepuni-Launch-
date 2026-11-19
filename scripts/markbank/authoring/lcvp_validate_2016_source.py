#!/usr/bin/env python3
"""Mandatory original-PDF gate, separate from portable checkout runtime tests."""
import hashlib
import json
import re
import fitz
from paper_census import census_lcvp, leaves_of, continuity_flags
from lcvp_review_2016 import ROOT, REVIEW, CASE, VIDEO_URL, PAGES, documents, build, question, scheme_parts, contrast_models, tidy


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
    assert [len(paper), len(case), len(scheme)] == [32, 2, 20]
    def case_text(value):
        value = value[value.index('GLENOR COMMUNITY PROJECT'):]
        return tidy(re.sub(r'Page\s+8\s+of\s+32', '', value.replace('-\n', '-')))
    assert case_text(paper[7].get_text(sort=True)) == case_text(case[1].get_text(sort=True))
    manual = {address(row['key']) for row in review['manualPaperLeaves']}
    assert len(manual) == review['manualOriginalLeaves'] == 40
    tasks = {address(row['key']) for row in review['pricedTaskLedger']}
    assert len(tasks) == review['manualPricedTasks'] == 39
    assert manual - tasks == {address('B2ai'), address('B2aii')}
    assert tasks - manual == {address('B2a')}
    parts, texts, files, marks, stems = census_lcvp('lcvp', 2016, 'cl')
    assert set(leaves_of(parts)) == manual
    assert not continuity_flags(parts, texts, 'lcvp')
    assert sum(marks.values()) == review['rawReaderAudit']['capturedTariffSum'] == 44
    cards, _ = build()
    assert len(cards) == 39 and sum(c['totalMarks'] for c in cards) == 210
    assert [sum(c['section'] == s for c in cards) for s in 'ABC'] == [8, 5, 26]
    by = {c['id'].removeprefix('lcvp-2016-cl-'): c for c in cards}
    assert {s: c['totalMarks'] for s, c in by.items()} == {r['key'].lower(): r['marks'] for r in review['pricedTaskLedger']}
    assert review['candidateWrittenMarks'] == 160
    assert review['originalMarkBankCards'] == 0 and review['previousAuthoredCards'] == 436
    assert len(review['originalAtlasMemberships']['existingRuntimeIds']) == 17
    assert by['a1']['rows'][0]['verbatim'] == 'TechMed Pro is a company which manufactures medical devices.'
    assert [len(by[s]['rows'][0]['group']['options']) for s in ['a2', 'a3', 'a5', 'a6', 'a7', 'a8', 'b1']] == [3, 2, 3, 7, 4, 6, 12]
    assert by['a5']['rows'][0]['group']['perOption'] == 2 and '0/2' in by['a5']['rows'][0]['contextNote']
    assert by['a7']['rows'][0]['group']['options'] == contrast_models(scheme)
    assert by['a7']['rows'][0]['group']['claimMax'] == 3
    assert all(len(pair.split(' — ')) == 2 for pair in contrast_models(scheme))
    assert contrast_models(scheme)[-1].endswith('Facilities creativity')
    assert 'both positive and negative' in by['a8']['rows'][0]['contextNote']
    case_stem = by['b1']['stem']
    assert len(case_stem) > 3500
    for card in cards:
        if card['section'] == 'B':
            assert card['stem'].startswith(case_stem)
            assert 'mobile catering' in card['stem'] and 'Ratlow Forest Park' in card['stem'] and 'Rathlow Park' in card['stem']
            assert card['stem'].count('Tree Top') == 1
            assert card['sourceMaterial']['pages'] == [8]
    assert by['b1']['questionText'] in by['b2a']['stem']
    assert '(i)' in by['b2a']['questionText'] and '(ii)' in by['b2a']['questionText']
    assert len([r for r in by['b2a']['rows'] if r['id'].startswith('contribution-')]) == 8
    assert len([r for r in by['b2a']['rows'] if r['id'].startswith('benefit-')]) == 9
    assert '(If not linked; mark both and disallow the lower mark)' in by['b2a']['rows'][0]['contextNote']
    assert by['b3b']['rows'][0]['marks'] == 1 and len(by['b3b']['rows'][1]['group']['options']) == 11
    assert by['b3b']['rows'][1]['group']['claimMax'] == 5
    assert [p['permittedMarks'] for p in by['c1aii']['rows'][0]['parts']] == [[0, 2], [0, 2]]
    assert all(v in by['c1b']['rows'][0]['contextNote'] for v in ['Future-focused', 'Self-confident', 'List is not exhaustive'])
    assert 'Advertising the enterprise' in by['c2b']['rows'][0]['contextNote']
    assert 'No repetition of points' in by['c2d']['rows'][0]['contextNote']
    assert [r['verbatim'] for r in by['c3d']['rows']] == ['Career Aspirations', 'Future Studies', 'What has been learned can be applied to work in the: Home', 'School', 'Community']
    for suffix, total in [('b2a', 6), ('c3d', 9)]:
        card = by[suffix]
        assert card['tariffModel']['kind'] == 'questionTotal' and card['totalMarks'] == total
        assert all(r['marks'] is None and not any(k in r for k in ['parts', 'group', 'permittedMarks']) for r in card['rows'])
        assert 'Numeric scoring held' in card['rows'][0]['contextNote']
    for suffix in ['c4a', 'c4b', 'c4c', 'c4d']:
        assert by[suffix]['sourceMaterial']['pages'] == [23]
        assert 'chocopersonnel@eircom.net' in by[suffix]['stem']
        assert '06 June, 2016' in by[suffix]['stem'] and '400' not in by[suffix]['stem']
    for row in by['c4b']['rows']:
        assert [p['permittedMarks'] for p in row['parts']] == [[0, 2], [0, 1]]
        assert all(v + ':' in row['contextNote'] for v in ['Interpersonal skills', 'Covering letter', 'References', 'Personnel Manager'])
    assert [len(r['group']['options']) for r in by['c4d']['rows']] == [6, 4, 6]
    assert all(r['group']['perOptionSteps'] == [2, 1] and r['group']['claimMax'] == 2 for r in by['c4d']['rows'])
    assert [r['marks'] for r in by['c5b']['rows']] == [1, 6, 1]
    assert len(by['c5b']['rows'][1]['group']['options']) == 7
    assert [by[s]['totalMarks'] for s in ['c5di', 'c5dii']] == [2, 6]
    assert [r['marks'] for r in by['c6a']['rows']] == [1, 3]
    assert [p['marks'] for p in by['c6a']['rows'][1]['parts']] == [2, 1]
    assert 'Business owner has links' in by['c6b']['rows'][0]['contextNote']
    assert all([p['permittedMarks'] for p in r['parts']] == [[0, 2], [0, 1]] for r in by['c6d']['rows'])
    assert 'Safe Pass' in by['c6d']['rows'][0]['contextNote']
    for letter in 'bcd':
        assert by['c6a']['questionText'] in by['c6' + letter]['stem']
    held = [c for c in cards if c['tariffModel']['kind'] == 'questionTotal']
    assert len(held) == 2 and sum(c['totalMarks'] for c in held) == review['heldWholeTaskMarks'] == 15
    priced = [c for c in cards if c not in held]
    assert sum(c['totalMarks'] for c in priced) == review['pricedMarks'] == 195
    for card in priced:
        assert sum(row['marks'] for row in card['rows']) == card['totalMarks'], card['id']
    blocks = scheme_parts(scheme)
    alignment = []
    for task in PAGES:
        words = set(re.findall(r'[a-z]+', question(paper, task).lower())) - {'the', 'a', 'of', 'to', 'in', 'and', 'is', 'for', 'you', 'your'}
        source_words = set(re.findall(r'[a-z]+', blocks[task].lower()))
        fraction = len(words & source_words) / len(words)
        assert fraction >= .75, (task, fraction, question(paper, task))
        alignment.append(dict(key=list(task), wordingRecall=round(fraction, 4)))
    for card in cards:
        assert not re.search(r'Office|Only|Page \d+ of 32|\b1 2\b', card['questionText'] + ' ' + card['stem']), card['id']
    media = json.loads((ROOT / 'scripts/markbank/authoring/lcvp/media-inventory-20261110.json').read_text())
    video = next(v for v in media if v['year'] == 2016 and v['sitting'] == 'main')
    assert video['officialDownloadUrl'] == VIDEO_URL and video['headers']['content-type'] == 'video/mp4'
    assert bytes.fromhex(video['prefixHex'])[4:12] == b'ftypisom'
    assert all(c['videoMaterial']['canonicalUrl'] == VIDEO_URL and c['additionalSourceMaterials'][0]['pages'] == [2] for c in cards if c['section'] == 'A')
    return dict(year=2016, sitting='main', sourceHashes='verified', sourcePages=[32, 2, 20], manualLeaves=40, rawLeaves=40,
        rawCapturedTariffSum=44, rawTariffLimitation='Older after-answer-space/continuation layout; independent original ledger governs 210 offered marks.',
        tasks=39, marks=210, candidateWrittenMarks=160, pricedMarks=195, heldWholeTaskMarks=15, continuityFlags=[],
        originalMarkBankCards=0, previousAuthoredCards=436, originalAtlasIdentities=17, caseBookletMatchesPaper=True,
        authoredSubsetSha256=hashlib.sha256(json.dumps(cards, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
        wordingAlignment=alignment, originalVideo='Official MP4 listing/headers/prefix verified; no full-file hash or playback claim',
        scope='All 54 original pages independently reviewed first. 40 printed leaves form 39 whole tasks; full case/ad, all alternatives and literal tariffs retained. B2(a) and C3(d) remain unresolved confidence reviews.')


if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
