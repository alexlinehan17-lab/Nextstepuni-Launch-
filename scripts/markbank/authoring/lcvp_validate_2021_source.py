#!/usr/bin/env python3
"""Explicit original-source authoring gate; runtime tests need no local corpus."""
import hashlib
import json
import re
from paper_census import census_lcvp, leaves_of, continuity_flags
from lcvp_review_2021 import ROOT, REVIEW, VIDEO_URL, documents, build, skill_quality_pools, comparison_pairs, email_source, questionnaire_source, page_raw, tidy
from lcvp_identity import ORIGINAL_CONCEPT_IDS


def verify():
    review=json.loads(REVIEW.read_text())
    for record in review['sources']:
        assert hashlib.sha256((ROOT/record['path']).read_bytes()).hexdigest()==record['sha256']
    paper,scheme=documents();assert len(paper)==40 and len(scheme)==24
    expected={('A',q,None,None) for q in [1,2,3,4,5,7]}
    expected.update(('A',q,None,r) for q in [6,8] for r in ['i','ii'])
    expected.update(('B',1,None,r) for r in ['i','ii','iii','iv'])
    expected.update(('B',q,None,r) for q in [2,3] for r in ['i','ii'])
    split={(1,'d'),(2,'a'),(5,'d')}
    expected.update(('C',q,l,None) for q in range(1,8) for l in 'abcd' if(q,l) not in split)
    expected.update(('C',q,l,r) for q,l in split for r in ['i','ii'])
    parts,texts,files,marks,stems=census_lcvp('lcvp',2021,'cl');actual=set(leaves_of(parts))
    assert len(expected)==review['manualOriginalLeaves']==49 and expected==actual,(expected-actual,actual-expected)
    assert sum(marks.values())==review['offeredPracticeMarks']==230 and review['candidateWrittenMarks']==130
    assert not continuity_flags(parts,texts,'lcvp')
    cards,_=build();assert len(cards)==review['manualPricedTasks']==45 and sum(c['totalMarks'] for c in cards)==230
    assert [sum(c['section']==s for c in cards) for s in 'ABC']==[10,5,30]
    assert all(c['tariffModel']['kind']=='fixed' for c in cards)
    for c in cards:
        if c['id'] in ORIGINAL_CONCEPT_IDS:assert c['conceptId']==ORIGINAL_CONCEPT_IDS[c['id']]
    by={c['id'].removeprefix('lcvp-2021-cl-'):c for c in cards}
    assert [len(v) for v in skill_quality_pools(scheme)]==[8,8]
    assert by['a6i']['questionText'] in by['a6ii']['stem']
    assert [r['marks'] for r in by['a6i']['rows']]==[2,2]
    assert len(by['b1']['rows'][0]['parts'])==3
    assert all(name in by['b1']['rows'][0]['contextNote'] for name in ['Market research:','To invest:','Diversification:','Unique selling point:'])
    assert 'Situated in a historic town' in by['b2ii']['rows'][0]['contextNote']
    assert by['b3i']['totalMarks']==4 and all([p['marks'] for p in r['parts']]==[1,1] for r in by['b3i']['rows'])
    assert [r['marks'] for r in by['c2a']['rows']]==[2,2]
    model,labels,summary=email_source(scheme)
    assert labels==['To: email address','Subject line','Salutation','Introduction','Reason for email','Closing']
    assert model in by['c2b']['rows'][0]['contextNote'] and 'Summary of marks' not in model
    assert [len(r['group']['options']) for r in by['c3b']['rows']]==[6,9]
    assert [r['marks'] for r in by['c3c']['rows']]==[1,1,1,5]
    questionnaire = questionnaire_source(scheme)
    assert questionnaire in by['c3c']['rows'][3]['contextNote']
    assert 'Q.1 Male' in questionnaire and 'Q.2 What age are you? 12-15' in questionnaire
    assert 'Q.6 What facilities' in questionnaire and 'Q.7 Are you willing' in questionnaire
    assert by['c4a']['rows'][0]['verbatim']=='mix of people' and by['c4a']['rows'][0]['marks']==2
    pairs=comparison_pairs(scheme);assert len(pairs)==10 and pairs[6][0].endswith('long term') and pairs[6][1].endswith('short term')
    assert pairs[8][1].endswith('Has') and pairs[9][1]=='set holidays/hours of work'
    for name in ['Communication skills','Time management skills','Decision-making skills','Creative skills']:
        assert name in by['c5c']['rows'][0]['contextNote']
    assert by['c6a']['rows'][0]['permittedMarks']==[0,2,4]
    pattern=re.compile(r'\b(?:choose|choice|one of|any\s+(?:one|two|three|four|five|\d+)|either|both|which one|which option|which of|compulsory)\b',re.I)
    directives={n:pattern.findall(tidy(page_raw(paper,n))) for n in range(1,41)}
    directives={n:v for n,v in directives.items() if v}
    # Exact source hash and original page review classify these explicit paths.
    assert directives == {2: ['any three', 'any four'], 6: ['Which of'],
                          9: ['any three', 'any four'], 10: ['both'],
                          15: ['any three', 'any four']}, directives
    media=json.loads((ROOT/'scripts/markbank/authoring/lcvp/media-inventory-20261110.json').read_text())
    video=next(v for v in media if v['year']==2021 and v['sitting']=='main')
    assert video['officialDownloadUrl']==VIDEO_URL and video['headers']['content-type']=='video/quicktime'
    assert bytes.fromhex(video['prefixHex'])[4:12]==b'ftypqt  '
    assert all(c['videoMaterial']['canonicalUrl']==VIDEO_URL for c in cards if c['section']=='A')
    return dict(year=2021,sitting='main',sourceHashes='verified',sourcePages=[40,24,2],manualLeaves=49,rawLeaves=len(actual),tasks=45,marks=230,candidateWrittenMarks=130,
        leafKeys=sorted([list(k) for k in actual],key=str),continuityFlags=[],numericHolds=[],classifiedSelectionDirectives=directives,
        originalVideo='Official listing, headers and QuickTime prefix verified; no whole-file hash or native playback claim',nativePlayback='pending root release QA',
        reconciliation='All66 original pages viewed before parser/cards. Original B1 four roman options form ONE choose-three task; C2(a) two leaves form ONE same-employer/reasons profile, hence49→45. Questionnaire Q1–Q8 are embedded answer examples, not top-level scheme questions. All40 original IDs/concepts retained; five omissions restored and B3(i) matching-way allocation restored2→4.')


if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False,indent=2))
