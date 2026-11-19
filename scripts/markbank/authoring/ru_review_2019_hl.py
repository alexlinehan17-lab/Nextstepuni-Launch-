"""Russian 2019 Higher: 44 printed asks with source-backed, approved allocations."""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts/markbank/authoring'))
import fitz
from ru_review_2015_ol import question_text, source_split
from ru_review_2026_hl import squash, between
from ru_paper import bag, score

METADATA={'paper': {'pages': 16, 'sha256': '539997eea0823aaf3f93224cc764ec9904cb57ef8afbe3de2048c413e153ecc8'}, 'aural': {'pages': 8, 'sha256': 'b2353a68203d0fd57e2e1d1f78ece5b024db3f251308502c599100b990e2662e'}, 'scheme': {'pages': 24, 'sha256': 'ea686213de8d50b2b3d44fbb18b9d95226b181d01602e6540f09331f74eb5216'}}

def source_records():
    metadata=METADATA
    docs = {}
    for kind, relative in [('paper', 'papers/2019-hl-000-paper.pdf'),
                           ('aural', 'papers/2019-hl-A00-paper.pdf'),
                           ('scheme', 'schemes/2019-hl.pdf')]:
        path = ROOT / 'examiner-reports/russian' / relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == metadata[kind]['sha256']
        docs[kind] = fitz.open(path)
    Q, A, S = docs['paper'], docs['aural'], docs['scheme']

    def page(doc, n, right=False):
        # Retain complete low-page content and remove only the pinned standalone
        # page-number line that precedes this scheme’s extracted body.
        rect = fitz.Rect(295, 30, 580, 793) if right else fitz.Rect(20, 30, 580, 793)
        text = doc[n-1].get_text(clip=rect, sort=False).replace('\uf0b7', '•').replace('\xa0', ' ')
        if doc is S:text=re.sub(r'^\s*'+str(n)+r'\s*\n','',text,count=1)
        return re.sub(r'^[^\n]*Lch\s+\d+\s+de\s+\d+[^\n]*Page\s+\d+\s+of\s+\d+[^\n]*\n?', '', text, flags=re.M)

    norm = lambda t: re.sub(r'[^\w]', '', t.casefold())

    def numbered_blocks(text):
        heads=list(re.finditer(r'^\s*(\d)\.\s*(?:\(?((?:iv|i{1,3}))\)?\.?\s*)?(?=[A-Z“])',text,re.M))
        return [(int(h.group(1)),h.group(2),text[h.end():heads[n+1].start() if n+1<len(heads) else len(text)]) for n,h in enumerate(heads)]

    def record(unit, item, roman, question, qp, body, sp, total, **extra):
        component = 'aural' if unit in ('L1', 'L2', 'L3', 'L4') else 'paper'
        assert any(norm(question) in norm(' '.join(page(docs[component], p, right=right) for p in qp))
                   for right in (False, True)), (unit, item, roman, question)
        return dict(id='ru-2019-hl-' + unit.lower() + (f'-{item}' if item is not None else '') + (f'-{roman}' if roman else ''),
                    unit=unit, item=item, roman=roman, question=question, questionPages=qp,
                    component=component, publishedSourceBlock=squash(body), schemePages=sp,
                    publishedTotal=total, **extra)

    cards = []
    source='\n'.join(page(S,p) for p in (4,5)).split('Language awareness')[0]
    blocks=numbered_blocks(source)
    asks=[(i,r,question_text(q),p) for p in (3,4) for i,r,q in numbered_blocks(page(Q,p,True))]
    assert len(blocks)==len(asks)==8
    totals=[4,8,4,4,2,4,6,6]
    for (i,r,b),(qi,qr,q,p),total in zip(blocks,asks,totals):
        assert (i,r)==(qi,qr)
        price=re.search(r'(?:(\d)\s*x\s*)?2\s*marks',b);assert price
        assert int(price.group(1) or 1)*2==total
        cue,body=b[:price.start()],b[price.start():]
        assert score(bag(q),bag(cue))>.75,(q,cue)
        cards.append(record('C1',i,r,q,[p],body,[4,5],total))
    assert sum(c['publishedTotal'] for c in cards)==38

    summary_source=between('\n'.join(page(S,p) for p in (6,7)),'Q.2 Summary writing','Language awareness')
    blocks=numbered_blocks(summary_source)
    assert len(blocks)==4
    for i,r,b in blocks:
        p={1:6,2:7,3:8,4:8}[i]
        q=question_text(page(Q,p,True).split(f'Section {i}',1)[1])
        cue,body=source_split(b,'10 marks')
        assert score(bag(q),bag(cue))>.75,(q,cue)
        cards.append(record('C2',i,None,q,[p],body,[6,7],10,
                            scoring=dict(detail=2,detailQuota=4,discretionaryMaximum=2,partialDetail=1,incompleteDiscretionaryMaximum=1)))

    q='Indicate the case '+question_text(between(page(Q,5,True),'Indicate the case','Q. 1.3'))
    b='Language awareness '+between(page(S,5),'Language awareness')
    rows=[[squash(v or '') for v in row] for row in S[4].find_tables().tables[0].extract()]
    cards.append(record('LA1',None,None,q,[5],b,[5],6,answerRows=rows,scoring=dict(phrases=6,perPhrase=1),reviewNote='Irish/English/Russian explicitly permitted.'))
    q='Select one of the topics '+question_text(between(page(Q,5,True),'Select one of the topics'))
    b='Cultural awareness '+between(page(S,6),'Cultural awareness','Q.2 Summary writing')
    cards.append(record('CA1',None,None,q,[5],b,[6],6,scoring=dict(topics=1,details=3,perDetail=2),reviewNote='English/Russian permitted; preserve Irish paper route.'))
    q='Verbs: '+question_text(between(page(Q,9,True),'Verbs:','Q.2.3'))
    b='Q.2.2. '+between(page(S,7),'Q.2.2.')
    cards.append(record('LA2',1,None,q,[9],b,[7],5,scoring=dict(correctInfinitives=5,perInfinitive=1),reviewNote='English translations expressly0.'))
    q='Semantic field/'+question_text(between(page(Q,9,True),'Semantic field/','1.'))
    b='Q.2.3. '+between(page(S,8),'Q.2.3.','Q.3 Structuring')
    cards.append(record('LA2',2,None,q,[9],b,[8],5,scoring=dict(words=5,perWord=1)))
    q='Read the following news items. '+squash(between(page(Q,10,True),'Read the following news items.'))
    q=q[:q.index('(20 marks)')+len('(20 marks)')]
    rows=[[squash(v or '') for v in row] for row in S[7].find_tables().tables[0].extract()]
    assert [re.findall(r'\d+',r[0]) for r in rows]==[['6'],['3'],['4'],['1'],['10'],['9'],['5'],['7'],['2','8'],['8','2']]
    b='Q.3 Structuring '+between(page(S,8),'Q.3 Structuring')
    cards.append(record('SD',None,None,q,[10],b,[8],20,answerRows=rows,scoring=dict(correctAnswers=10,perAnswer=2)))
    q='Read through the following text. '+squash(between(page(Q,11,True),'Read through the following text.'))
    q=q[:q.index('substitute words.')+len('substitute words.')]
    cards.append(record('GR',None,None,q,[11],page(S,9),[9],30,scoring=dict(correctForms=15,perForm=2),reviewNote='13 gaps include two adjective/noun pairs; preserve15 separately priced forms and both complete phrases.'))
    q='Write a short essay '+squash(between(page(Q,12,True),'Write a short essay'))
    q=q[:q.index('essay title.')+len('essay title.')]
    cards.append(record('SE',None,None,q,[12],'Q.2. Cultural Awareness '+between(page(S,9),'Q.2. Cultural Awareness')+'\n'+'\n'.join(page(S,p) for p in (10,11)),[9,10,11],30,fullQuestionPage=page(Q,12),reviewNote='Alex approved one or two soft-sign marks on 18 November; original wording retained.'))
    q='Write a piece '+question_text(page(Q,13,True).split('Write a piece',1)[1])
    cards.append(record('GW',None,None,q,[13],'\n'.join(page(S,p) for p in (12,13)),[12,13],40,pending='Conditional Lower A7–12; source middle9–11 overlaps11–12 and differs from prose9/10. Three complete choices.'))
    assert len(cards)==20 and sum(c['publishedTotal'] for c in cards)==220

    source='\n'.join(page(S,p) for p in (14,15,16,17))
    heads=list(re.finditer(r'^\s*SECTION (IV|III|II|I)\b[^\n]*$',source,re.M));assert len(heads)==4
    counts=[[2,1,1,2,2,1,1],[2,2,1,2,1,2],[None,2,2,1,3],[2,2,1,2,2,1]]
    topics=[['russian-0-9','russian-0-3','russian-0-3','russian-0-9','russian-0-5','russian-0-9','russian-0-9'],
            ['russian-0-5','russian-0-7','russian-0-5','russian-0-4','russian-0-5','russian-0-8'],
            ['russian-0-7']*5,['russian-0-1','russian-0-4','russian-0-5','russian-0-3','russian-0-4','russian-0-4']]
    for n,h in enumerate(heads):
        section=n+1;b=source[h.end():heads[n+1].start() if n+1<len(heads) else len(source)]
        blocks=numbered_blocks(b)
        asks=[(i,r,question_text(q)) for i,r,q in numbered_blocks(page(A,section+1,True))]
        assert len(blocks)==len(asks)==len(counts[n]),(section,len(blocks),len(asks))
        for (i,r,b),(qi,qr,q),count,topic in zip(blocks,asks,counts[n],topics[n]):
            note=''
            if (section,i,r)==(1,5,'i'):
                assert (qi,qr)==(5,'ii');note='English booklet prints5(ii) twice; Irish and scheme disambiguate destination5(i), passengers5(ii).'
            elif (section,i,r)==(2,1,None):
                assert (qi,qr)==(1,'i');note='English booklet 1(i); Irish and scheme 1. Preserve both original forms.'
            elif (section,i,r)==(4,1,'ii'):
                assert (qi,qr)==(1,'ii');note='English booklet and scheme 1(ii); Irish column prints 2(ii) beside the same part-time-job question. Both original forms are retained.'
            else:assert (i,r)==(qi,qr)
            cue,body=source_split(b,'•')
            assert score(bag(q),bag(cue))>.75,(q,cue)
            # No full-answer tariff is printed anywhere in this listening scheme.
            cards.append(record(f'L{section}',i,'i' if (section,i,r)==(2,1,None) else r,q,[section+1],body,[section+13],None,
                                printedDetailQuota=count,topicId=topic,sharedAward=f'L{section}-section20',reviewNote=note,
                                reviewNoteAllocation='Alex approved two marks per requested detail on 18 November; preserve explicit partial and zero instructions.'))
    assert len(cards)==44 and sum(c['publishedTotal'] or 0 for c in cards)==220
    assert len({c['id'] for c in cards})==44
    for c in cards:assert norm(c['publishedSourceBlock']) in norm('\n'.join(page(S,p) for p in c['schemePages'])),c['id']
    draft=dict(status='Source-only draft; not runtime cards or a completed sitting',sources=metadata,
               independentTasks=44,writtenTasks=20,listeningTasks=24,printedExamTotal=300,pricedWrittenTotal=220,
               sharedAwards=[dict(id=f'L{i}-section20',publishedTotal=20,schemePages=[i+13],pending='No full per-answer tariff printed.') for i in range(1,5)],
               generalWrittenGuidance=squash(page(S,3)),comprehensionGuidance=squash(re.split(r'^\s*1\.\s+Give two reasons',page(S,4),maxsplit=1,flags=re.M)[0]),
               summaryGuidance=squash(summary_source[:re.search(r'^\s*1\.\s+[A-Z]',summary_source,re.M).start()]),
               listeningGuidance=squash(source[:heads[0].start()]),tasks=cards)
    return docs,draft


from ru_review_2026_hl import base as common_base, as_points, save_reviewed


def base(*args, **kwargs):
    c=common_base(*args, **kwargs)
    for key in ('id','questionRef'):c[key]=c[key].replace('2026','2019')
    c['year']=2019;c['sourceMaterial']['title']=c['sourceMaterial']['title'].replace('2026','2019')
    return c


def source_card(r):
    pages={'C1':[2,3,4],'LA1':[2,3,4,5],'C2':[6,7,8],'LA2':[6,7,8,9],'GR':[11]}.get(r['unit'],r['questionPages'])
    c=base(r['unit'],r['question'],r['publishedTotal'],pages,r['schemePages'],r['item'],r['roman'])
    c['review']['questionPages']=r['questionPages'];return c


def manual_details(r,count,steps,guidance,note):
    c=as_points(source_card(r),[],count)
    c['rubric']['groups']=[{'id':f'detail-{i}','label':f'Manual distinct detail {i}','rows':[],
        'criteria':[{'id':f'detail-{i}-credit','label':f'Distinct detail {i}','maxMarks':2,'permittedMarks':steps,'guidance':[]}]} for i in range(1,count+1)]
    c['rubric']['taskRequirements']=guidance;c['rubric']['markingGuideNote']=note
    return c


def reading(source):
    result=[];records=[r for r in source['tasks'] if r['unit']=='C1']
    first=next(r for r in records if (r['item'],r['roman'])==(2,'i'))
    second=next(r for r in records if (r['item'],r['roman'])==(2,'ii'))
    no_repeat='Accept information relating to university preparations'+first['publishedSourceBlock'].split('Accept information relating to university preparations',1)[1]
    for r in records:
        body=r['publishedSourceBlock'];key=(r['item'],r['roman'])
        if key in ((2,'i'),(2,'ii')):
            c=manual_details(r,r['publishedTotal']//2,[0,2],
                [source['comprehensionGuidance'],first['publishedSourceBlock'],second['publishedSourceBlock']],
                'Assess distinct details manually against the complete accepted pools and the source rule on repeated information. No automatic cross-question state is inferred.')
            if key==(2,'ii'):
                for i,g in enumerate(c['rubric']['groups'],1):
                    g['criteria'][0]['limits']=[{'id':f'detail-{i}-already-credited','maxMarks':0,
                        'when':{'any':[{'flag':f'detail-{i}-already-credited','prompt':f'This detail was already credited in Question 2(i).'}]},
                        'guidance':[no_repeat]}]
                c['rubric']['markingGuideNote']+=' Set the already-credited condition only for the particular repeated detail. The other response remains independent. Follow the printed general instruction to accept the response giving the most marks; a condition does not move or alter the other card’s stored score.'
        else:
            pool=body.split('•')[1:];assert len(pool)>=r['publishedTotal']//2
            rejected=''
            if 'Assign no marks:' in pool[-1]:pool[-1],rejected=pool[-1].split('Assign no marks:',1)
            c=as_points(source_card(r),[squash(item) for item in pool],r['publishedTotal']//2)
            c['rubric']['taskRequirements']=[source['comprehensionGuidance']]+(['Assign no marks: '+squash(rejected)] if rejected else [])
        c['review']['guidancePages']=[4];result.append(c)
    assert len(result)==8 and sum(c['totalMarks'] for c in result)==38
    return result


def summaries(source):
    result=[];general=source['summaryGuidance']
    incomplete=re.search(r'If a candidate fails.*?discretionary mark can be awarded\)',general).group()
    for r in source['tasks']:
        if r['unit']!='C2':continue
        c=manual_details(r,4,[0,1,2],[general,r['publishedSourceBlock']],
            'Assess four distinct details manually against the complete published pool. One mark applies only to a partial detail intelligible to a monolingual English speaker, under the printed general rule. Discretionary marks remain separate from content.')
        c['rubric']['criteria']=[{'id':'summary-skills','label':'Discretionary marks','maxMarks':2,'permittedMarks':[0,1,2],'guidance':[general],
            'limits':[{'id':'incomplete-response','maxMarks':1,'when':{'any':[{'flag':'incomplete-response','prompt':incomplete}]},'guidance':[incomplete]}]}]
        c['review']['guidancePages']=[6];result.append(c)
    assert len(result)==4 and sum(c['totalMarks'] for c in result)==40
    return result


def allocation_approval():
    folder=ROOT/'scripts/markbank/authoring/reviews/russian-2019-hl-sec-20261118'
    proposal_path=folder/'allocation-proposal.json'
    approval=json.loads((folder/'allocation-approval.json').read_text())
    assert approval['listeningAnswer']=='Approve the proposed listening allocations'
    assert approval['writingAnswer']=='One or two marks'
    assert hashlib.sha256(proposal_path.read_bytes()).hexdigest()==approval['proposalSha256']
    return json.loads(proposal_path.read_text())


def listening(source):
    proposal=allocation_approval()
    approved={r['id']:r for r in proposal['listening']['cards'] if r['year']==2019}
    records=[r for r in source['tasks'] if r['component']=='aural']
    assert len(approved)==len(records)==24
    audio=next(row['source'] for row in json.loads((ROOT/'data/russianAudio.json').read_text()) if row['year']==2019)
    result=[]
    for r in records:
        a=approved[r['id']]
        assert a['question']==r['question'] and a['sourceAnswers']==r['publishedSourceBlock']
        count=a['proposedDetails'];assert a['proposedMaximum']==2*count
        body=r['publishedSourceBlock']
        # Keep named partial and zero-credit clauses as source guidance. Each
        # partial shares its full answer's existing mutually exclusive group.
        pool=re.split(r'(?:Assign|Award) (?:one mark|no marks)',body)[0]
        answers=[squash(x) for x in pool.split('•')[1:] if squash(x)]
        partials={}
        if r['id']=='ru-2019-hl-l1-5-i':
            assert answers==['Train station'];partials={0:['station']}
        elif r['id']=='ru-2019-hl-l2-3-ii':
            assert answers==['Ice skating','ceramics'];partials={0:['skating']}
        elif r['id']=='ru-2019-hl-l3-1-i':
            assert answers==['The Mill Theatre / Dundrum theatre / Dublin theatre','21st and 22nd July']
            partials={0:['Dublin/Dundrum']}
        c=as_points(source_card({**r,'publishedTotal':a['proposedMaximum']}),answers,count,partials=partials)
        if r['id']=='ru-2019-hl-l3-1-i':
            # The printed general partial-detail rule also applies to the date;
            # the date stays one response, with no invented partial wording.
            c['rubric']['groups'][1]['rows'][0]['steps']=[0,1,2]
        c['rubric']['taskRequirements']=[source['listeningGuidance'],body]
        c['rubric']['markingGuideNote']='Two marks per complete requested detail are inferred from the paper’s 20-mark section totals and approved on 18 November 2026; two is not printed as a general per-detail award in this scheme. The printed one-mark and zero-mark instructions remain in force. Select distinct details up to the number requested.'
        if r['reviewNote']:c['rubric']['markingGuideNote']+=' Source numbering: '+r['reviewNote']
        c['review']['allocationApproval']='reviews/russian-2019-hl-sec-20261118/allocation-approval.json'
        c['review']['approvedInference']={'marksPerRequestedDetail':2,'requestedDetails':count,'printedSectionTotal':20}
        c['review']['reviewedAt']='2026-11-19';c['review']['guidancePages']=[14]
        c['topicId']=r['topicId'];c['additionalTopicIds']=['russian-1-0']
        c['sourceMaterial']['kind']='source-question'
        c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
        c['audioMaterial']=audio;result.append(c)
    assert len(result)==24 and sum(c['totalMarks'] for c in result)==80
    assert all(sum(c['totalMarks'] for c in result if c['section']==f'L{section}')==20 for section in range(1,5))
    return result



def writing(docs,source):
    from ru_review_2017_hl import band
    r=next(r for r in source['tasks'] if r['unit']=='GW');c=source_card(r)
    c.pop('rows');c.pop('tariffModel');c['kind']='rubric';body=r['publishedSourceBlock']
    content=between(body,'1. Communication/content (C)','2. Expression (E):')
    expression=between(body,'2. Expression (E):','Lower E Ex 10')
    lower_e=re.search(r'If the content mark.*?indicate this\.',expression).group()
    lower_a=re.search(r'If the expression is very fluent.*?indicate this\.',expression).group()
    soft=re.search(r'Deduct 2 marks.*?infinitives\.',expression).group()
    tables=docs['scheme'][12].find_tables().tables;assert len(tables)==3
    normal=[];lower=[]
    for low,full,description in tables[0].extract()[1:]:
        normal.append(band(full,description));lower.append(band(low,description))
    printed_accuracy=[band(price,description) for price,description in tables[1].extract()[1:]]
    assert [b['marks'] for b in printed_accuracy]==[[11,12],[9,10,11],[7,8]]
    accuracy_literal='Lower A Expression'+between(body,'Lower A Expression','3. Textual coherence:')
    coherence=[band(price,description) for price,description in tables[2].extract()[1:]]
    limits=[{'id':'lower-e','scaleLabel':'Lower E','maxMarks':10,
        'when':{'any':[{'criterionIds':['content'],'atMost':7},{'length':'words','below':60}]},'guidance':[lower_e],'bands':lower},
        {'id':'lower-a','scaleLabel':'Lower A','minMarks':7,'maxMarks':12,
         'when':{'any':[{'flag':'lower-a','prompt':lower_a}]},'guidance':[lower_a,accuracy_literal]}]
    prompts,tariffs=body.split('1. Communication/content (C)',1)[0].split('Communication + content',1)
    c['rubric']={'system':'language-writing',
        'taskRequirements':[prompts,'Communication + content'+tariffs,source['generalWrittenGuidance'].split('Language issues',1)[0]],
        'markingGuideNote':'Manually assess the selected complete response against every original requirement. The source gives one mark per content detail and requires at least one from each specified category, without fixed category totals. Lower A permits 7–12, but its prose middle range 9/10 and table 9–11 disagree at 11, overlapping the table’s 11–12 range. Both exact versions remain visible; no descriptor is reassigned, no precedence is inferred and the range does not automatically award its minimum.',
        'criteria':[{'id':'content','label':'Communication/content (C)','maxMarks':15,'permittedMarks':list(range(16)),'guidance':[squash(content)]},
            {'id':'expression','label':'Language + expression (E)','maxMarks':15,'permittedMarks':list(range(16)),
             'guidance':[squash(expression)],'bands':normal,'limits':limits},
            {'id':'coherence','label':'Textual coherence (TC)','maxMarks':10,'permittedMarks':list(range(11)),
             'guidance':['3. Textual coherence:'+between(body,'3. Textual coherence:','Mark Textual coherence')],'bands':coherence},
            {'id':'soft-sign-penalty','label':'Soft sign penalty','kind':'deduction','deductFrom':'expression','maxMarks':2,'permittedMarks':[0,2],'guidance':[soft]}]}
    c['review']['guidancePages']=[3];return c


def cultural_writing(docs,source):
    from ru_review_2017_hl import band
    allocation_approval()
    r=next(r for r in source['tasks'] if r['unit']=='SE');c=source_card(r)
    choices='Напишите'+between(r['fullQuestionPage'],'Напишите').split('___')[0]
    assert all(f'{n}.' in choices for n in range(1,6));c['questionText']+='\n\n'+choices
    body=r['publishedSourceBlock']
    content=between(body,'Communication/content (C)','2. Expression (E)')
    expression=between(body,'2. Expression (E)','Mark Language:')
    bullets=[squash(x) for x in content.split('•')[1:]];assert len(bullets)==6
    title=next(x for x in bullets if 'ONE penalty mark' in x)
    no_content=next(x for x in bullets if 'no marks for language' in x)
    lower_e=re.search(r'If the content mark.*?indicate this\.',expression).group()
    lower_a=re.search(r'If the expression is very fluent.*?indicate this\.',expression).group()
    soft=re.search(r'Deduct 1/2 marks.*?infinitives',expression).group()
    normal=[];lower=[];accuracy=[]
    tables=docs['scheme'][10].find_tables().tables;assert len(tables)==1
    for printed,description in tables[0].extract():
        if printed=='Mark':continue
        normal.append(band(re.split(r'lower [AE]',printed)[0].strip(),description))
        lower.append(band(printed.split('lower E')[-1].strip(),description))
        if 'lower A' in printed:accuracy.append(band(between(printed,'lower A','lower E'),description))
    assert [x['marks'] for x in normal]==[[18,19,20],[14,15,16,17],[10,11,12,13],[6,7,8,9],[1,2,3,4,5],[0]]
    assert [x['marks'] for x in lower]==[[12,13,14],[10,11],[7,8,9],[4,5,6],[1,2,3],[0]]
    assert [x['marks'] for x in accuracy]==[[13,14],[11,12],[9,10]]
    c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
    prompt,rest=body.split('1. Content 10 marks',1)
    instruction,table=('1. Content 10 marks'+rest).split('Mark Language: lexis, accuracy, fluency',1)
    c['rubric']={'system':'language-writing','taskRequirements':[prompt,instruction,'Mark Language: lexis, accuracy, fluency'+table],
        'markingGuideNote':'The scheme prints no answer for this part. Assess the selected essay using the printed content and expression grid. The direction “Deduct 1/2 marks” means one or two marks under Alex’s 18 November approval; its original wording is retained.',
        'criteria':[
            {'id':'content','label':'Communication/content (C)','maxMarks':10,'permittedMarks':[0,2,4,6,8,10],'guidance':bullets},
            {'id':'title-penalty','label':'Essay title penalty','kind':'deduction','deductFrom':'content','maxMarks':1,'permittedMarks':[0,1],'guidance':[title]},
            {'id':'expression','label':'Language/expression (E)','maxMarks':20,'permittedMarks':list(range(21)),
             'guidance':[squash(expression)],'bands':normal,'limits':[
                {'id':'lower-e','scaleLabel':'Lower E','maxMarks':14,'when':{'any':[{'criterionIds':['content'],'atMost':5,'ignoreDeductions':True},{'length':'words','below':25}]},'guidance':[lower_e],'bands':lower},
                {'id':'lower-a','scaleLabel':'Lower A','minMarks':9,'maxMarks':14,'when':{'any':[{'flag':'lower-a','prompt':lower_a}]},'guidance':[lower_a],'bands':accuracy},
                {'id':'no-content','maxMarks':0,'when':{'any':[{'criterionIds':['content'],'atMost':0,'ignoreDeductions':True}]},'guidance':[no_content]}]},
            {'id':'soft-sign-penalty','label':'Soft sign penalty','kind':'deduction','deductFrom':'expression','maxMarks':2,'permittedMarks':[0,1,2],'guidance':[soft]}]}
    c['review']['allocationApproval']='reviews/russian-2019-hl-sec-20261118/allocation-approval.json'
    return no_printed_answer(c,r['schemePages'])


def no_printed_answer(c,pages):
    fixed='The scheme prints no answer for this part.'
    if not c['rubric']['markingGuideNote'].startswith(fixed):c['rubric']['markingGuideNote']=fixed+' '+c['rubric']['markingGuideNote']
    c['review']['reviewedAt']='2026-11-19'
    c['review']['noPrintedAnswer']={'fixedLine':fixed,'schemePages':pages,'evidence':'scripts/markbank/authoring/reviews/russian-2019-hl-sec-20261118/archive-recheck.json'}
    return c



def source_language_rules(cards,source):
    rule='Language of answer:'+between(source['generalWrittenGuidance'],'Language of answer:','Quality of English:')
    exception=re.search(r'Discretionary marks \(as opposed to content marks\) may be awarded.*?answers\)\.',source['summaryGuidance']).group()
    for c in cards:
        if c['section'] not in ('C1','C2','LA2','GR','GW','SE'):continue
        c['answerLanguageRule']={'otherLanguageMultiplier':0,'sourceText':squash(rule),'schemePages':[3]}
        if c['section'] in ('C1','C2'):
            c['rubric']['markingGuideNote']+=' Answer in English or Irish, as permitted by the original bilingual paper.'
        if c['section']=='C2':
            c['answerLanguageRule']['manualCriterionExceptions']={'criterionIds':['summary-skills'],'sourceText':exception,'schemePages':[6]}



def grammar_forms(document):
    spans=[span for block in document[8].get_text('dict')['blocks'] if 'lines' in block
           for line in block['lines'] for span in line['spans'] if span['color'] in {12582912,13506590}]
    # Both red colours are independently observed on the pinned original p9.
    assert {span['color'] for span in spans}=={12582912,13506590}
    assert spans
    words=[word.strip('.,') for span in spans for word in span['text'].split() if word.strip('.,')]
    assert len(words)==15,words
    assert words[1]=='пошла/шла',words
    return words


def language_and_matching(docs,source):
    result=[];records={r['id'].replace('ru-2019-hl-',''):r for r in source['tasks'] if r['unit'] in ('LA1','CA1','LA2','SD','GR')}
    r=records['la1'];rows=r['answerRows'][3:];assert len(rows)==6
    assert [row[0] for row in rows]==[str(n) for n in range(1,7)]
    c=as_points(source_card(r),[row[1]+' — '+row[2] for row in rows],6)
    for g in c['rubric']['groups']:g['rows'][0]['marks']=1
    c['rubric']['taskRequirements']=[r['publishedSourceBlock'].split('Example /',1)[0]]
    c['rubric']['markingGuideNote']='All six original noun phrases are required. Answers may be written in Irish, English or Russian. The printed example is not an additional claimable answer.'
    result.append(c)
    r=records['ca1'];topics=re.findall(r'\b[1-3]\.\s*(.*?)(?=\s+[1-3]\.|$)',r['publishedSourceBlock']);assert len(topics)==3,topics
    c=as_points(source_card(r),[],1)
    c['rubric']['groups']=[{'id':f'topic-{n}','label':topic,'rows':[],
        'criteria':[{'id':f'topic-{n}-detail-{k}','label':f'Distinct detail {k}','maxMarks':2,'permittedMarks':[0,2],
                     'guidance':[r['publishedSourceBlock']]} for k in range(1,4)]} for n,topic in enumerate(topics,1)]
    c['rubric']['taskRequirements']=[r['publishedSourceBlock']]
    c['rubric']['markingGuideNote']='Select one of the three original topics and assess three distinct relevant details. The scheme does not print an exemplar factual pool. English or Russian is explicitly permitted; retain the Irish column of the original paper without imposing an automatic language penalty.'
    no_printed_answer(c,[6])
    result.append(c)
    r=records['la2-1'];pairs=re.findall(r'(?<![\w.])[1-5]\.\s*(\S+)\s+(\S+)',r['publishedSourceBlock']);assert len(pairs)==5,pairs
    c=as_points(source_card(r),[a+' — '+b for a,b in pairs],5)
    for g in c['rubric']['groups']:g['rows'][0]['marks']=1
    c['rubric']['taskRequirements']=[r['publishedSourceBlock'].split('1. беспокоилась',1)[0]]
    c['rubric']['markingGuideNote']='Supply all five original infinitives. English translations receive no marks under the explicit source rule.'
    result.append(c)
    r=records['la2-2'];pool=r['publishedSourceBlock'].split('5 x 1 mark',1)[1]
    words=[squash(word).rstrip('.') for word in pool.split(',')];assert len(words)==15,words
    c=as_points(source_card(r),words,5)
    for g in c['rubric']['groups']:g['rows'][0]['marks']=1
    c['rubric']['taskRequirements']=[r['publishedSourceBlock'].split('домашние дела',1)[0]]
    c['rubric']['markingGuideNote']='Select five distinct source entries. Each complete printed multiword entry is one accepted response, each has one mark.'
    result.append(c)
    r=records['sd'];rows=r['answerRows'];assert len(rows)==10
    c=as_points(source_card(r),[row[0]+' — '+row[1] for row in rows],10)
    c['rubric']['taskRequirements']=[r['publishedSourceBlock'].split('6 Традиция',1)[0]]
    c['rubric']['markingGuideNote']='The ten answers follow the original news items in order. Preserve each printed slash alternative; no additional rule requiring unique section numbers is inferred.'
    result.append(c)
    r=records['gr'];answers=grammar_forms(docs['scheme'])
    c=as_points(source_card(r),answers,15)
    c['rubric']['taskRequirements']=[r['publishedSourceBlock'].split('Оксана родилась',1)[0]]
    c['rubric']['markingGuideNote']='The thirteen original gaps contain fifteen forms with separate marks. Each word of the complete adjective/noun phrases receives the printed two-mark form allocation; the published пошла/шла alternatives are one response. Apply the exact spelling/transcription and wrong-tense zero rules.'
    result.append(c)
    assert len(result)==6 and sum(c['totalMarks'] for c in result)==72
    return result


def build():
    docs,source=source_records()
    try:
        cards=reading(source)+summaries(source)+language_and_matching(docs,source)+[no_printed_answer(writing(docs,source),[12,13]),cultural_writing(docs,source)]+listening(source)
        source_language_rules(cards,source)
        assert len(cards)==len({c['id'] for c in cards})==44
        assert sum(c['totalMarks'] for c in cards)==300
        assert sum(c['totalMarks'] for c in cards if c.get('kind')=='rubric')==300
        assert sum(bool(c.get('answerLanguageRule')) for c in cards)==17
        return cards
    finally:
        for document in docs.values():document.close()


def raw_scheme_text():
    path=ROOT/'examiner-reports/russian/schemes/2019-hl.pdf'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==METADATA['scheme']['sha256']
    with fitz.open(path) as document:
        pages=[page.get_text() for page in document]
        raw='\n\n'.join(f'## Page {n+1}\n\n'+text for n,text in enumerate(pages))+'\n'
        # Retain every untouched page plus a labelled complete-page whitespace
        # rendering; the generic provenance comparator removes numeric-only lines.
        joined='\n\n'.join(f'### Joined original page {n+1}\n\n'+squash(text) for n,text in enumerate(pages))
        return raw+'\n# Original pages with line wraps joined\n\n'+joined+'\n'


if __name__=='__main__':
    cards=build()
    # These four never-live section placeholders are replaced by their 24
    # original asks. Keep the retired records in the review evidence.
    output=ROOT/'scripts/markbank/authored/russian-reviewed.json'
    previous=json.loads(output.read_text())
    retired={f'ru-2019-hl-l{n}' for n in range(1,5)}
    removed=[c for c in previous if c['id'] in retired]
    if removed:
        assert len(removed)==4
        evidence=ROOT/'scripts/markbank/authoring/reviews/russian-2019-hl-sec-20261118/retired-section-cards.json'
        if evidence.exists():assert json.loads(evidence.read_text())==removed
        else:evidence.write_text(json.dumps(removed,indent=2,ensure_ascii=False)+'\n')
        output.write_text(json.dumps([c for c in previous if c['id'] not in retired],indent=2,ensure_ascii=False)+'\n')
    save_reviewed(cards)
    (ROOT/'examiner-reports/russian/schemes/2019-hl.md').write_text(raw_scheme_text())
