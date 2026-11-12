#!/usr/bin/env python3
"""Mandatory original-source gate; portable runtime tests do not need local PDFs."""
import hashlib
import json
import re
from paper_census import census_lcvp,leaves_of,continuity_flags
from lcvp_review_2019 import ROOT,REVIEW,VIDEO_URL,PAGES,documents,build,scheme_parts,question,work_skills,ict_uses,cv_headings,questionnaire_source
from lcvp_identity import ORIGINAL_CONCEPT_IDS
from lcvp_review_2026 import numbered


def verify():
    review=json.loads(REVIEW.read_text())
    for record in review['sources']:assert hashlib.sha256((ROOT/record['path']).read_bytes()).hexdigest()==record['sha256']
    paper,scheme=documents();assert [len(paper),len(scheme)]==[36,20]
    # Independently saved visual paper ledger, not inferred from generated cards.
    expected={('A',q,None,None) for q in [1,2,3,4,6,7,8]}
    expected.update(('A',5,None,r) for r in ['i','ii'])
    expected.add(('B',1,None,None))
    expected.update(('B',2,None,r) for r in ['i','ii','iii'])
    expected.update(('B',3,None,r) for r in ['i','ii'])
    split={(1,'d'),(2,'b'),(2,'d'),(3,'a'),(3,'d'),(5,'a')}
    expected.update(('C',q,l,None) for q in range(1,7) for l in 'abcd' if(q,l) not in split)
    expected.update(('C',q,l,r) for q,l in split for r in ['i','ii'])
    assert len(expected)==review['manualOriginalLeaves']==45
    parts,texts,files,marks,stems=census_lcvp('lcvp',2019,'cl');actual=set(leaves_of(parts))
    assert actual==expected,(expected-actual,actual-expected)
    assert sum(marks.values())==review['offeredPracticeMarks']==210 and review['candidateWrittenMarks']==160
    assert not continuity_flags(parts,texts,'lcvp')
    cards,_=build();assert len(cards)==review['manualPricedTasks']==45 and sum(c['totalMarks'] for c in cards)==210
    assert [sum(c['section']==s for c in cards) for s in 'ABC']==[9,6,30]
    by={c['id'].removeprefix('lcvp-2019-cl-'):c for c in cards}
    originals=[c for c in cards if c['id'] in ORIGINAL_CONCEPT_IDS];assert len(originals)==39
    for c in originals:assert c['conceptId']==ORIGINAL_CONCEPT_IDS[c['id']]
    assert [by[k]['totalMarks'] for k in ['b3ii','c3ai','c3aii','c4a','c5ai','c5d']]==[9,1,3,3,2,6]
    assert by['b3i']['totalMarks']==3 and [r['marks'] for r in by['b3i']['rows']]==[1,2]
    source_blocks=scheme_parts(scheme)
    for suffix,q,count,pool_count in [('a6',6,4,13),('a7',7,6,10)]:
        assert len(by[suffix]['rows'][0]['parts'])==count
        assert all(part['marks']==1 and part['permittedMarks']==[0,1] for part in by[suffix]['rows'][0]['parts'])
        assert by[suffix]['rows'][0]['marks']==count and 'group' not in by[suffix]['rows'][0]
        for model in numbered(source_blocks[('A',q,None,None)],pool_count):assert model in by[suffix]['rows'][0]['contextNote'],model
    assert cv_headings(scheme)==['Personal details','Skills/qualities','Education/qualifications','Work experience','Hobbies/interests','Achievements','Referees']
    assert by['c1a']['rows'][1]['group']['options']==cv_headings(scheme)
    held=[c for c in cards if c['tariffModel']['kind']=='questionTotal']
    assert [c['id'] for c in held]==['lcvp-2019-cl-c6b']
    assert all(r['marks'] is None and 'parts' not in r and 'group' not in r for c in held for r in c['rows'])
    assert len(by['c6b']['rows'])==8 and by['c6b']['rows'][-1]['verbatim']=='Etc.'
    assert all(s in by['c6b']['rows'][0]['contextNote'] for s in ['Two relevant answers','4 x 1 mark','confidence review only'])
    for c in cards:
        if c not in held:assert sum(r['marks'] for r in c['rows'])==c['totalMarks'],c['id']
    assert by['b3ii']['rows'][0]['parts'] and len(by['b3ii']['rows'][0]['parts'])==3
    assert by['b3ii']['rows'][0]['verbatim']=='Set it out under three headings.'
    assert all(part['marks']==3 and part['permittedMarks']==[0,1,2,3] for part in by['b3ii']['rows'][0]['parts'])
    for label in ['Product / service','Financial details','Management/People','Marketing']:
        assert label in by['b3ii']['rows'][0]['contextNote'],(label,by['b3ii'])
    assert 'MUST link' in by['b2iii']['rows'][0]['contextNote']
    assert 'SCHOOL BASED ACTIVITY/ENTERPRISE' in by['b3i']['rows'][0]['contextNote']
    assert all('One of the local schools is interested in using the land.' in by[s]['stem'] for s in ['b3i','b3ii'])
    model=questionnaire_source(scheme)
    for token in ['Q.1','Male','Female','Q.2','Yes','No','Q.3','Blue','Red','Grey','Q.4','Q.5','Full zip','No zip','Q.6*','pay for a hoodie']:
        assert token in model,token
    assert model.count('☐')==11,model
    assert [r['marks'] for r in by['c2c']['rows']]==[1,1,1,1,4]
    assert 'LAYOUT ONLY' in by['c2c']['rows'][0]['contextNote'] and 'finance' in by['c2c']['rows'][3]['verbatim']
    assert by['c2c']['rows'][-1]['parts'] and len(by['c2c']['rows'][-1]['parts'])==4
    assert by['c2c']['rows'][-1]['verbatim']=='questions'
    assert all(part['marks']==1 and part['permittedMarks']==[0,1] for part in by['c2c']['rows'][-1]['parts'])
    assert 'Repetition will not score' in by['c2dii']['rows'][0]['contextNote']
    assert by['c4b']['rows'][0]['group']['perOption']==2 and by['c4b']['rows'][0]['group']['claimMax']==4
    assert [r['marks'] for r in by['c3aii']['rows']]==[1,2]
    assert all(r['marks']==2 and [p['marks'] for p in r['parts']]==[1,1] for r in by['c5d']['rows'])
    skills=work_skills(scheme,scheme_parts(scheme)[('C',4,'d',None)]);uses=ict_uses(scheme)
    assert len(skills)==13 and skills[9:]==['Problem solving','Time management','Motivation','Etc.'],skills
    assert len(uses)==14 and uses[11]=='Production of portfolio items/reports/printing' and uses[-1]=='Etc',uses
    assert 'Provide free WiFi to attract customers' in by['c6c']['rows'][0]['contextNote']
    assert 'Negative/bad reviews of the business from customers/service/bad ratings' in by['c6d']['rows'][0]['contextNote']
    blocks=scheme_parts(scheme);alignment=[]
    for key in PAGES:
        words=set(re.findall(r'[a-z]+',question(paper,key).lower()))-{'the','a','of','to','in','and','is','for','you','your'}
        source_words=set(re.findall(r'[a-z]+',blocks[key].lower()));fraction=len(words&source_words)/len(words)
        difference=None
        if key==('C',6,'b',None):
            printed='Why are ICT skills necessary for an employee in today’s working environment?'
            scheme_prompt='Why are IT skills necessary for an employee?'
            assert question(paper,key)==printed and blocks[key].startswith(scheme_prompt+' Two relevant answers 4 x 1 mark')
            difference=dict(paperPage=31,schemePage=17,paperWording=printed,schemeWording=scheme_prompt,
                review='Exact original wording difference visually verified; task identity and contradictory allocation remain source-bound, no fuzzy match inferred.')
        else:assert fraction>=.55,(key,fraction,question(paper,key),blocks[key][:220])
        alignment.append(dict(key=list(key),wordingRecall=round(fraction,4),reviewedWordingDifference=difference))
    media=json.loads((ROOT/'scripts/markbank/authoring/lcvp/media-inventory-20261110.json').read_text())
    video=next(v for v in media if v['year']==2019 and v['sitting']=='main')
    assert video['officialDownloadUrl']==VIDEO_URL and video['headers']['content-type']=='video/mp4'
    assert bytes.fromhex(video['prefixHex'])[4:12]==b'ftypmp42'
    assert all(c['videoMaterial']['canonicalUrl']==VIDEO_URL for c in cards if c['section']=='A')
    return dict(year=2019,sitting='main',sourceHashes='verified',sourcePages=[36,20],manualLeaves=45,rawLeaves=45,tasks=45,marks=210,candidateWrittenMarks=160,
        authoredSubsetSha256=hashlib.sha256(json.dumps(cards,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        manualLeafKeys=sorted([list(k) for k in expected],key=str),continuityFlags=[],numericHolds=['C6(b)4'],pricedMarks=206,heldWholeTaskMarks=4,
        wordingAlignment=alignment,questionnaireFinance='Compulsory finance question within5; non-hoodie layout-only rule visible; entire6-question model retained',
        originalVideo='Official MP4 listing/headers/prefix verified, no whole-file hash or native playback claim',nativePlayback='pending coordinator release QA',
        reconciliation='All56 original pages independently viewed before parser/legacy inspection. All45 leaves form45 tasks. All39 original IDs/concepts retained; six omissions restored and B3(i) name1+reason2 corrected. C6(b) Two relevant answers vs4x1mark remains whole-task confidence-only; no tariff precedence inferred.')


if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False,indent=2))
