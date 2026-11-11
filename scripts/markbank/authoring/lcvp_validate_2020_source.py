#!/usr/bin/env python3
"""Mandatory raw-source gate, separate from portable checkout runtime tests."""
import hashlib
import json
import re
from paper_census import census_lcvp,leaves_of,continuity_flags
from lcvp_review_2020 import ROOT,REVIEW,VIDEO_URL,SPLIT_C,documents,build,scheme_parts,question,PAGES,promotion_pairs,qualities,page_raw,tidy
from lcvp_identity import ORIGINAL_CONCEPT_IDS


def verify():
    review=json.loads(REVIEW.read_text())
    for record in review['sources']:assert hashlib.sha256((ROOT/record['path']).read_bytes()).hexdigest()==record['sha256']
    paper,scheme=documents();assert len(paper)==36 and len(scheme)==22
    expected={('A',q,None,None) for q in range(1,6)}
    expected.update(('A',q,None,r) for q in [6,7,8] for r in ['i','ii'])
    expected.update(('B',1,None,r) for r in ['i','ii','iii','iv'])
    expected.update(('B',q,None,r) for q in [2,3] for r in ['i','ii'])
    expected.update(('C',q,l,None) for q in range(1,7) for l in 'abcd' if (q,l) not in SPLIT_C)
    expected.update(('C',q,l,r) for q,l in SPLIT_C for r in ['i','ii'])
    assert len(expected)==review['manualOriginalLeaves']==49
    parts,texts,files,marks,stems=census_lcvp('lcvp',2020,'cl');actual=set(leaves_of(parts))
    # Raw reader retains the complete two-column B1 parent, not four separate leaves.
    collapsed={('B',1,None,r) for r in ['i','ii','iii','iv']}
    raw_expected=(expected-collapsed)|{('B',1,None,None)}
    assert len(actual)==46 and actual==raw_expected,(raw_expected-actual,actual-raw_expected)
    b1=question(paper,('B',1,None,None))
    assert set(re.findall(r'\((i|ii|iii|iv)\)\s+([a-z ]+?)(?=\s*\(|$)',b1))=={('i','mentor'),('ii','bookkeeping'),('iii','sole trader'),('iv','upskill')},b1
    assert sum(marks.values())==review['offeredPracticeMarks']==210 and review['candidateWrittenMarks']==160
    assert not continuity_flags(parts,texts,'lcvp')
    cards,_=build();assert len(cards)==review['manualPricedTasks']==46 and sum(c['totalMarks'] for c in cards)==210
    assert [sum(c['section']==s for c in cards) for s in 'ABC']==[11,5,30]
    by={c['id'].removeprefix('lcvp-2020-cl-'):c for c in cards}
    assert len([c for c in cards if c['id'] in ORIGINAL_CONCEPT_IDS])==43
    for c in cards:
        if c['id'] in ORIGINAL_CONCEPT_IDS:assert c['conceptId']==ORIGINAL_CONCEPT_IDS[c['id']]
    held=[c for c in cards if c['tariffModel']['kind']=='questionTotal']
    assert {c['id'] for c in held}=={'lcvp-2020-cl-c3a','lcvp-2020-cl-c5ai'}
    assert all(r['marks'] is None and 'parts' not in r and 'group' not in r for c in held for r in c['rows'])
    assert [len(by[k]['rows']) for k in ['c3a','c5ai']]==[8,7]
    assert all(t in by['c3a']['rows'][0]['contextNote'] for t in ['Four valid points','2 x 2 mark (1+1)'])
    assert all(t in by['c5ai']['rows'][0]['contextNote'] for t in ['Three points','2 x 1 mark'])
    assert sum(c['totalMarks'] for c in held)==6
    assert len(by['a1']['rows'][0]['group']['options'])==2
    assert 'Save the Bees Committee' in by['a1']['rows'][0]['group']['options'][1]
    assert len(by['b1']['rows'][0]['parts'])==3
    assert all(label in by['b1']['rows'][0]['contextNote'] for label in ['Mentor:','Bookkeeping:','Sole trader:','Upskill:'])
    pairs=promotion_pairs(scheme);assert len(pairs)==10
    assert pairs[5][0]=='Visit trade shows' and pairs[5][1].endswith('get information.')
    assert pairs[8][0]=='Local sponsorship' and pairs[8][1].endswith('support his business.')
    assert len(qualities(scheme))==8
    assert all(term in by['c1a']['rows'][0]['contextNote'] for term in ['Problem Solving:','Flexible Working Hours:','Referees:','Equal Opportunities Employer:'])
    assert 'problem solving' in by['c1a']['stem'] and 'hr@manraytechnologies.ie' in by['c1a']['stem']
    assert by['c2b']['rows'][0]['group']['perOption']==2
    assert 'advantages AND disadvantages' in by['c2c']['rows'][0]['contextNote']
    assert [r['marks'] for r in by['c4ai']['rows']]==[1,1]
    assert all(r['parts'][1]['permittedMarks']==[0,2] for r in by['c4d']['rows'])
    assert [r['marks'] for r in by['c5c']['rows']]==[1,1,1,1,3,1]
    assert [by[k]['totalMarks'] for k in ['c6di','c6dii']]==[6,3]
    assert by['c6di']['questionText'] in by['c6dii']['stem']
    assert all(name in by['c6dii']['rows'][0]['contextNote'] for name in ['Marketing/Market Research:','Finance:','Staff/Personnel/HR:','Production:','Location/Premises:'])
    blocks=scheme_parts(scheme)
    alignment=[]
    for key in PAGES:
        words=set(re.findall(r'[a-z]+',question(paper,key).lower()))-{'the','a','of','to','in','and','is','for','you','your'}
        source_words=set(re.findall(r'[a-z]+',blocks[key].lower()))
        fraction=len(words&source_words)/len(words)
        assert fraction>=.6,(key,fraction,question(paper,key),blocks[key][:220])
        alignment.append(dict(key=list(key),wordingRecall=round(fraction,4)))
    pattern=re.compile(r'\b(?:choose|choice|one of|any\s+(?:one|two|three|four|five|\d+)|either|both|which one|which option|which of|compulsory|(?:two|three) of (?:the|these))\b',re.I)
    directives={n:pattern.findall(tidy(page_raw(paper,n))) for n in range(1,37)};directives={n:v for n,v in directives.items() if v}
    # This exact source-hash-bound classification must match every selection directive.
    assert directives=={2:['any four'],10:['three of the'],12:['three of the'],14:['any four','two of the'],15:['choice'],16:['two of the'],25:['choice']},directives
    media=json.loads((ROOT/'scripts/markbank/authoring/lcvp/media-inventory-20261110.json').read_text())
    video=next(v for v in media if v['year']==2020 and v['sitting']=='main')
    assert video['officialDownloadUrl']==VIDEO_URL and video['headers']['content-type']=='video/mp4'
    assert bytes.fromhex(video['prefixHex'])[4:12]==b'ftypmp42'
    assert all(c['videoMaterial']['canonicalUrl']==VIDEO_URL for c in cards if c['section']=='A')
    return dict(year=2020,sitting='main',sourceHashes='verified',sourcePages=[36,22],manualLeaves=49,rawLeaves=46,tasks=46,marks=210,candidateWrittenMarks=160,
        rawReaderClassification=review['rawCensusClassification'],manualLeafKeys=sorted([list(k) for k in expected],key=str),continuityFlags=[],numericHolds=['C3(a)4','C5(a)(i)2'],
        pricedMarks=204,heldWholeTaskMarks=6,wordingAlignment=alignment,classifiedSelectionDirectives=directives,
        originalVideo='Official listing, MP4 headers and ISO base-media prefix verified; no whole-file hash or native playback claim',nativePlayback='pending root release QA',
        reconciliation='All58 original pages independently viewed. Four B1 roman options are one choose-three task; raw reader collapses these options as a whole parent, hence manual49 vs raw46/task46. All43 original IDs/concepts retained; C5(c)/C6(d)(i)/C6(d)(ii) restored and C4(a)(i) career1+benefit1 corrected. Both quota/allocation conflicts remain whole-task confidence-only, source completeness does not imply resolved scoring.')


if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False,indent=2))
