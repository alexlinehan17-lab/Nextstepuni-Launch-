"""Russian 2014 Higher authoring, bound to the original papers and scheme."""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts/markbank/authoring'))
import fitz
from ru_review_2011_ol import numbered_blocks
from ru_review_2015_ol import page_text, question_text, source_split
from ru_review_2026_hl import squash, between
from ru_paper import bag, score

METADATA = {'paper': {'pages': 16, 'sha256': '2260a53d30344848d06148108aac814aa7b99616d68dddec815ce79604877b91'}, 'aural': {'pages': 8, 'sha256': '3cf21d1f34576eda4ce0b6bc126152ea7f8b289c105cd5e7e711774bf10f1f66'}, 'scheme': {'pages': 20, 'sha256': 'fb5cfc36f2f64fc1a8fc068bbad392ff99eb2ff5792c37267dfcabc0d0ad1f48'}}

def source_records():
    docs = {}
    for kind, relative in [('paper', 'papers/2014-hl-000-paper.pdf'),
                           ('aural', 'papers/2014-hl-A00-paper.pdf'),
                           ('scheme', 'schemes/2014-hl.pdf')]:
        path = ROOT / 'examiner-reports/russian' / relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == METADATA[kind]['sha256']
        docs[kind] = fitz.open(path)
    Q, A, S = docs['paper'], docs['aural'], docs['scheme']

    def page(doc, n, right=False):
        return doc[n-1].get_text(clip=fitz.Rect(295, 30, 580, 793) if right else fitz.Rect(20, 30, 580, 775), sort=False).replace('\uf0b7', '•').replace('\x02', '•').replace('\xa0', ' ')

    def record(unit, item, roman, question, qp, body, sp, total, **extra):
        component = 'aural' if unit in ('L1', 'L2', 'L3', 'L4') else 'paper'
        norm = lambda t: re.sub(r'[^\w]', '', t.casefold())
        assert norm(question) in norm(' '.join(page(docs[component], p, right=True) for p in qp)), (unit, item, roman, question)
        return dict(id='ru-2014-hl-' + unit.lower() + (f'-{item}' if item is not None else '') + (f'-{roman}' if roman else ''),
                    unit=unit, item=item, roman=roman, question=question, questionPages=qp,
                    component=component, publishedSourceBlock=squash(body), schemePages=sp,
                    publishedTotal=total, **extra)

    cards = []
    source = '\n'.join(page(S, p) for p in (4, 5)).split('Q.1.2.')[0]
    blocks = numbered_blocks(source)
    asks = [(i,r,question_text(q),p) for p in (3,4) for i,r,q in numbered_blocks(page(Q,p,True))]
    assert len(blocks) == len(asks) == 8
    totals = [6,2,6,4,4,6,6,4]
    for (i,r,b),(qi,qr,q,p),total in zip(blocks,asks,totals):
        assert (i,r)==(qi,qr)
        price = re.search(r'(\d)\s*x\s*2\s*=\s*(\d)',b)
        assert price and int(price.group(2))==total
        cue,body=b[:price.start()],b[price.start():]
        assert score(bag(q),bag(cue))>.75,(q,cue)
        cards.append(record('C1',i,r,q,[p],body,[4,5],total))
    assert sum(c['publishedTotal'] for c in cards)==38

    summary_source='\n'.join(page(S,p) for p in (6,7)).split('Language awareness')[0]
    blocks=numbered_blocks(summary_source)
    asks=[]
    for p in (7,8):
        text=page(Q,p,True)
        heads=list(re.finditer(r'^\s*Section\s+([1-4])\s*$',text,re.M))
        asks.extend((int(h.group(1)),question_text(text[h.end():heads[n+1].start() if n+1<len(heads) else len(text)]),p)
                    for n,h in enumerate(heads))
    assert len(blocks)==len(asks)==4
    for (i,r,b),(qi,q,p) in zip(blocks,asks):
        assert i==qi and r is None
        cue,body=source_split(b,'Main points:')
        assert score(bag(q),bag(cue))>.75,(q,cue)
        cards.append(record('C2',i,None,q,[p],body,[6,7],10,
                            scoring=dict(detail=2,contentMaximum=8,discretionaryMaximum=2,partialDetail=1,incompleteDiscretionaryMaximum=1),
                            reviewNote='Summary2: source expressly says not to deduct discretion when Lucy/Serezha names are omitted.' if i==2 else ''))

    q='Supply the nominative singular form '+squash(between(page(Q,5,True),'Supply the nominative singular form','Q.1.3.')).split('1.')[0].strip()
    b='Supply the nominative singular form '+between(page(S,5),'Supply the nominative singular form','Q.1.3.')
    cards.append(record('LA1',None,None,q,[5],b,[5],6,fullQuestionPage=page(Q,5),scoring=dict(chosenPhrases=3,availablePhrases=6,perModifier=1,perNoun=1),reviewNote='Correct phrase translations explicitly receive full marks because original task did not specify answer language.'))
    q='Cultural awareness: '+question_text(between(page(Q,5,True),'Cultural awareness:'))
    b='Q.1.3. '+between(page(S,5),'Q.1.3.')
    cards.append(record('CA1',None,None,q,[5],b,[5],6,reviewNote='All three topic choices retained. English or Russian explicitly permitted; no invented factual exemplars.'))
    text=page(Q,9,True)
    q='In the text '+squash(between(text,'In the text','Q.2.3.'))
    b='Q.2.2. '+between(page(S,7),'Q.2.2.','Q.2.3.')
    cards.append(record('LA2',None,'i',q,[9],b,[7],5,printedAddress='Q.2.2',scoring=dict(correctWords=5,perWord=1)))
    q='Verbs: '+question_text(between(text,'Verbs:'))
    b='Q.2.3. '+between(page(S,7),'Q.2.3.')
    cards.append(record('LA2',None,'ii',q,[9],b,[7],5,printedAddress='Q.2.3',scoring=dict(correctInfinitives=5,perInfinitive=1)))
    q='Read the following information '+squash(between(page(Q,10,True),'Read the following information'))
    q=q[:q.index('(20 marks)')+len('(20 marks)')]
    table=S[7].find_tables().tables[0].extract()
    rows=[[squash(v or '') for v in row] for row in table]
    assert [re.findall(r'\d+',r[0]) for r in rows]==[['10','2'],['2','10'],['6'],['1','4'],['7'],['3','4'],['5'],['9'],['4','3','1'],['8']],rows
    cards.append(record('SD',None,None,q,[10],page(S,8),[8],20,answerRows=rows,scoring=dict(correctAnswers=10,perAnswer=2)))
    q='Read through the following text. '+squash(between(page(Q,11,True),'Read through the following text.'))
    q=q[:q.index('substitute words.')+len('substitute words.')]
    cards.append(record('GR',None,None,q,[11],page(S,9),[9],30,scoring=dict(correctForms=15,perForm=2),
                        sourcePages=[11,12],reviewNote='Fifteen forms continue across the two original paper pages; preserve all exact inflections.'))
    q='Write a short essay '+squash(between(page(Q,13,True),'Write a short essay'))
    q=q[:q.index('essay title.')+len('essay title.')]
    cards.append(record('SE',None,None,q,[13],'\n'.join(page(S,p) for p in (10,11)),[10,11],30,fullQuestionPage=page(Q,13),
                        pending='Shared conditional Lower A range9–14; all five topic choices preserved.'))
    q='Write a piece '+question_text(between(page(Q,14,True),'Write a piece'))
    cards.append(record('GW',None,None,q,[14],'\n'.join(page(S,p) for p in (12,13,14)),[12,13,14],40,
                        pending='Shared conditional Lower A range7–12; all three writing choices and their original category guides retained.'))
    assert len(cards)==20 and sum(c['publishedTotal'] for c in cards)==220

    source='\n'.join(page(S,p) for p in (15,16,17))
    heads=list(re.finditer(r'^\s*Section (1|II|III|IV):[^\n]*$',source,re.M))
    assert len(heads)==4
    counts=[[2,2,2,2,2],[2,3,2,3],[1,2,2,1,2,2],[2,2,1,3,2]]
    starts=[['Twenty volunteers','50% will stay','There are 3 guys','Last concert','He is 17'],
            ['bike rental','Website velobike.ru','Day/week/month','Fine of 15000'],
            ['To tell him','21 years old','Excellent organization','He’s happy','She brought them','He came for a week'],
            ['His father/','He attended','started when','At 18/','He was married']]
    topics=[['russian-2-3','russian-0-8','russian-2-3','russian-0-7','russian-0-5'],
            ['russian-0-9']*4,
            ['russian-2-3','russian-0-1','russian-0-7','russian-0-7','russian-2-3','russian-0-8'],
            ['russian-0-1','russian-0-3','russian-0-4','russian-0-4','russian-0-1']]
    for n,h in enumerate(heads):
        section=n+1;b=source[h.end():heads[n+1].start() if n+1<len(heads) else len(source)]
        blocks=numbered_blocks(b);asks=[(i,r,question_text(q)) for i,r,q in numbered_blocks(page(A,section+1,True))]
        assert len(blocks)==len(asks)==len(counts[n])
        for (i,r,b),(qi,qr,q),count,start,topic in zip(blocks,asks,counts[n],starts[n],topics[n]):
            assert (i,r)==(qi,qr)
            cue,body=source_split(b,start);assert score(bag(q),bag(cue))>.8,(q,cue)
            sp=[15,16] if section==1 else [16] if section==2 else [16,17] if section==3 else [17]
            cards.append(record(f'L{section}',i,r,q,[section+1],body,sp,count*2,detailQuota=count,topicId=topic,
                                reviewNote='L3Q4 source explicitly accepts details from other sections; no inferred other cross-question expansion.' if (section,i)==(3,4) else ''))
    assert len(cards)==40 and sum(c['publishedTotal'] for c in cards)==300
    assert len({c['id'] for c in cards})==40
    norm=lambda t:re.sub(r'[^\w]','',t.casefold())
    for c in cards:
        assert norm(c['publishedSourceBlock']) in norm('\n'.join(page(S,p) for p in c['schemePages'])),c['id']
    draft=dict(status='Source-only draft; not runtime cards or a completed sitting',sources=METADATA,
               independentTasks=40,writtenTasks=20,listeningTasks=20,generalWrittenGuidance=squash(page(S,3)),
               comprehensionGuidance=squash(page(S,4).split('1.i.')[0]),
               summaryGuidance=squash(summary_source[:re.search(r'^\s*1\.\s*[A-Z]',summary_source,re.M).start()]),
               listeningGuidance=squash(source[:heads[0].start()]),tasks=cards)
    return docs, draft

from ru_review_2026_hl import base as common_base,as_points,save_reviewed
from ru_review_2017_hl import named_group,options

def base(*args,**kwargs):
    c=common_base(*args,**kwargs)
    for key in ('id','questionRef'):c[key]=c[key].replace('2026','2014')
    c['year']=2014;c['sourceMaterial']['title']=c['sourceMaterial']['title'].replace('2026','2014');return c

def source_card(r):
    pages=r.get('sourcePages') or ([2,3,4] if r['unit']=='C1' else [6,7,8,9] if r['unit']=='LA2' else [6,7,8] if r['unit']=='C2' else r['questionPages'])
    c=base(r['unit'],r['question'],r['publishedTotal'],pages,r['schemePages'],r['item'],r['roman']);c['review']['questionPages']=r['questionPages'];return c

def reading(source):
    result=[]
    for r in source['tasks']:
        if r['unit']!='C1':continue
        key=(r['item'],r['roman']);body=r['publishedSourceBlock'];notes=[];rejected='';partial='';special=''
        for marker in ["Don't penalise",'Do not award marks']:
            if marker in body:body,note=body.split(marker,1);notes.append(marker+note)
        if 'assign no marks:' in body:body,rejected=body.split('assign no marks:',1)
        if 'assign one mark:' in body:body,partial=body.split('assign one mark:',1)
        if 'assign up to four marks' in body:body,special=body.split('assign up to four marks',1);special='assign up to four marks'+special
        full=between(body,'assign two marks:');answers=options(full);partials=options(partial)
        mapping={};independent=partials
        if key==(3,'i'):
            assert len(answers)==5 and len(partials)==2
            independent=[]
        c=as_points(source_card(r),answers,r['publishedTotal']//2,mapping)
        for n,p in enumerate(independent,1):c['rubric']['groups'].append(named_group(f'independent-partial-{n}','Published partial detail',[p],marks=1))
        if key==(1,'i'):
            # The one-mark evaluation is printed at pool level, without an
            # exclusive full-answer association. Three distinct response
            # slots retain the allocation without inventing that pairing.
            c['rubric']['groups']=[{'id':f'detail-{n}','label':f'Distinct detail {n}','rows':[],
                'criteria':[{'id':f'detail-{n}','label':f'Distinct detail {n}','maxMarks':2,'permittedMarks':[0,1,2],
                             'guidance':['assign two marks: '+full,'assign one mark: '+partial]}]} for n in (1,2,3)]
            c['rubric']['markingGuideNote']='Assess three distinct details against the complete printed pool. The one-mark evaluation is printed at question level. Do not count one detail twice merely because it is paraphrased, and do not infer a unique full/partial pairing from its position.'
        if special:
            assert key==(3,'i')
            rows=options(between(special,'of:'));assert rows==['neighbours didn’t drink','make jokes','talk','sing']
            groups=[{'id':f'neighbour-{n}','label':f'Neighbours did not: distinct detail {n}','rows':[],
                     'criteria':[{'id':f'neighbour-{n}','label':f'Neighbours did not: detail {n}','maxMarks':2,'permittedMarks':[0,2],'guidance':[special]}]} for n in (1,2)]
            groups += [{'id':f'other-{n}','label':f'Other distinct detail {n} — exclude the four neighbours-did-not actions','rows':[],
                        'criteria':[{'id':f'other-{n}','label':f'Other detail {n}, excluding the four neighbours-did-not actions','maxMarks':2,'permittedMarks':[0,1,2],
                                     'guidance':['assign two marks: '+full,'assign one mark: '+partial]}]} for n in (1,2,3)]
            c['rubric']['groups']=groups
            c['rubric']['allocationCap']={'maxMarks':6,'sourceText':'3 x 2 = 6','schemePages':[5]}
            c['rubric']['markingGuideNote']='Select at most three distinct answer slots; every selected slot must represent a different actual detail. Do not use the same neighbour action in both slots or repeat a fact in an Other slot. Use the two neighbours-did-not slots only for the four actions drinking, making jokes, talking and singing; these have a shared maximum of two details/four marks. Use the other slots for all remaining published full or partial details, including the separate sleep details. Both original source lines remain visible. The bad/boring partial association is not uniquely specified: assess the actual distinct response, without counting one evaluation twice as paraphrases or imposing a fixed pairing.'
            notes+=['assign two marks: '+full,special,'assign one mark: '+partial]
        c['rubric']['taskRequirements']=[source['comprehensionGuidance']]+notes
        if rejected:c['rubric']['taskRequirements'].append('assign no marks: '+rejected)
        c['rubric']['markingGuideNote']+=' Source allocation: the paper reading heading gives 40 marks, while the scheme explicitly assigns 38 to the reading questions and 12 to the two following tasks. These cards follow every printed local allocation without moving two marks between tasks.'
        c['review']['guidancePages']=[4]
        result.append(c)
    assert len(result)==8 and sum(c['totalMarks'] for c in result)==38
    return result

def summaries(source):
    result=[];general=source['summaryGuidance'];incomplete=next(x for x in general.split('. ') if 'fails to answer all' in x)
    for r in source['tasks']:
        if r['unit']!='C2':continue
        body=r['publishedSourceBlock'];special=''
        if 'Do not deduct a discretionary mark' in body:body,special=body.split('Do not deduct a discretionary mark',1);special='Do not deduct a discretionary mark'+special
        primary,secondary=body.split('Secondary details:',1);primary=options(between(primary,'Main points:'));secondary=options(secondary)
        c=as_points(source_card(r),primary+secondary,4,steps=[0,1,2],labels=['Main point']*len(primary)+['Secondary detail']*len(secondary))
        if r['item'] in (1,2):
            c['rubric']['groups']=[{'id':f'detail-{n}','label':f'Distinct detail {n}','rows':[],
                'criteria':[{'id':f'detail-{n}','label':f'Distinct detail {n}','maxMarks':2,'permittedMarks':[0,1,2],'guidance':[body]}]} for n in (1,2,3,4)]
            c['rubric']['markingGuideNote']='The main and secondary lists contain overlapping statements. Assess four distinct facts from the actual response; an identical fact printed in both lists earns once. Additional distinct facts remain eligible under the printed detail rule. No automatic pairing or extra credit is inferred from the two lists.'
        c['rubric']['criteria']=[{'id':'summary-skills','label':'Discretionary marks','maxMarks':2,'permittedMarks':[0,1,2],'guidance':[general],
            'limits':[{'id':'incomplete-response','maxMarks':1,'when':{'any':[{'flag':'incomplete-response','prompt':incomplete}]},'guidance':[incomplete]}]}]
        c['rubric']['taskRequirements']=[general]+([special] if special else [])
        if special:c['rubric']['markingGuideNote']+=' Omitting the names Lucy/Serezha alone does not reduce discretionary marks.'
        result.append(c)
    return result

def language_and_matching(docs,source):
    result=[]
    for r in source['tasks']:
        unit=r['unit'];body=r['publishedSourceBlock'];c=source_card(r)
        if unit not in ('LA1','CA1','LA2','SD'):continue
        if unit=='LA1':
            pairs=re.findall(r'\s[1-6]\.\s+(.+?)\s[-–]\s+(.+?)(?=\s[1-6]\.|$)',body);assert len(pairs)==6
            rule='Assign full marks '+squash(between(body,'Assign full marks','1.'))
            groups=[];sets=[]
            for n,(prompt,answer) in enumerate(pairs,1):
                modifier,noun=answer.split();sid=f'phrase-{n}'
                groups.append({'id':sid+'-russian','label':prompt+' — Russian form','alternativeSet':sid,'rows':[],
                               'criteria':[{'id':sid+'-modifier','label':'Modifier','maxMarks':1,'permittedMarks':[0,1],'guidance':[modifier]},
                                           {'id':sid+'-noun','label':'Noun','maxMarks':1,'permittedMarks':[0,1],'guidance':[noun]}]})
                groups.append({'id':sid+'-translation','label':prompt+' — correct translation','alternativeSet':sid,'rows':[],
                               'criteria':[{'id':sid+'-translation','label':'Correct translation of the complete phrase','maxMarks':2,'permittedMarks':[0,2],'guidance':[rule]}]})
                sets.append({'id':sid,'label':'Response type for '+prompt,'sourceText':rule,'schemePages':[5]})
            c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
            c['rubric']={'system':'language-points','count':3,'groups':groups,'alternativeSets':sets,
                         'taskRequirements':['Assign one mark for the noun and one mark for its modifier.',rule],
                         'markingGuideNote':'Choose three different phrases. For each, use one response type; do not claim both the Russian form and a translation of the same phrase. Correct translations receive full credit because the task does not specify a response language. The scheme supplies no translated model answers.'}
        elif unit=='CA1':
            c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
            c['rubric']={'system':'language-writing','criteria':[{'id':f'detail-{n}','label':f'Distinct factual detail {n}','maxMarks':2,'permittedMarks':[0,2],'guidance':['Award 2 marks per detail.']} for n in (1,2,3)],
                         'taskRequirements':[body,'Award 2 marks per detail.'],
                         'markingGuideNote':'Choose one of the three original cultural topics and supply three distinct details. English, Irish and Russian are permitted by the original bilingual paper. The detail rate is printed in the general Q1 guidance on scheme page4; its50-mark heading explicitly includes38+12, with this task and language awareness making up the12. No factual model answers or partial-detail tariff are supplied.'}
            c['review']['guidancePages']=[4]
        elif unit=='LA2' and r['roman']=='i':
            words=between(body,'5 x 1 = 5');answers=[squash(x) for x in words.split(',')];assert len(answers)==13
            c=as_points(c,answers,5)
            for g in c['rubric']['groups']:g['rows'][0]['marks']=1
            c['rubric']['taskRequirements']=['Accept words in any form (case, number).','Give one mark for each correct answer.']
        elif unit=='LA2':
            entries=re.split(r'\s[1-5]\.\s+',body)[1:];assert len(entries)==5
            pairs=[squash(x).split(' ',1) for x in entries]
            c=as_points(c,[answer for prompt,answer in pairs],5)
            for g,(prompt,answer) in zip(c['rubric']['groups'],pairs):g['label']=prompt;g['rows'][0]['marks']=1
            c['rubric']['taskRequirements']=['Do not assign any marks where candidates translate the verb into English.']
        else:
            rows=r['answerRows'];c=as_points(c,[squash(text)+' — '+squash(numbers) for numbers,text in rows],10)
            for n,(g,(numbers,text)) in enumerate(zip(c['rubric']['groups'],rows),1):
                g['label']=squash(text);g['rows']=[{'id':f'option-{j}','text':number,'marks':2} for j,number in enumerate(re.findall(r'\d+',numbers),1)]
            c['rubric']['taskRequirements']=['10 x 2 = 20']
            c['rubric']['markingGuideNote']='Each row retains every number accepted in the original scheme. Do not impose an additional one-use-only rule across rows that the scheme does not print.'
        result.append(c)
    assert len(result)==5
    return result

from ru_review_2026_hl import mark_range
from ru_review_2017_hl import band

def writing(docs, source, base):
    S=docs['scheme']; result=[]
    for unit,sp,table_page in [('SE',10,11),('GW',13,13)]:
        record=next(c for c in source['tasks'] if c['unit']==unit)
        text=S[sp-1].get_text(sort=True)
        expression_heading='2. Expression (E):' if unit=='SE' else '2. Expression (E)'
        content=between(text,'1. Communication/content (C)',expression_heading)
        expression=between(text,expression_heading)
        lower_e=squash(re.search(r'If the content mark.*?indicate this\.',expression,re.S).group())
        lower_a=squash(re.search(r'If the expression is very fluent.*?indicate this\.',expression,re.S).group())
        soft=squash(re.search(r'Penalise (?:students|candidates).*?\(– .*?\)\.',expression,re.S).group())
        normal=[];lower=[];accuracy=[]
        tables=S[table_page-1].find_tables().tables
        if unit=='SE':
            for prices,description in tables[0].extract()[1:]:
                prices=squash(prices)
                normal.append(band(prices.split('lower')[0],description))
                lower.append(band(prices.split('lower E')[-1] if 'lower E' in prices else prices,description))
                a=re.search(r'lower A (\d+-\d+)',prices)
                if a:accuracy.append(band(a.group(1),description))
            assert [b['marks'] for b in accuracy]==[[13,14],[11,12],[9,10]]
        else:
            for low,full,description in tables[0].extract()[1:]:
                normal.append(band(full,description));lower.append(band(low,description))
            accuracy_source=[(squash(price),squash(description)) for price,description in tables[1].extract()[1:]]
            assert [mark_range(price) for price,description in accuracy_source]==[[11,12],[9,10],[7,8]]
            accuracy=[band(price,description) for price,description in accuracy_source]
        is_essay=unit=='SE';maximum=20 if is_essay else 15
        question=record['question']
        if is_essay:
            choices=between(record['fullQuestionPage'],'Напишите').split('___')[0]
            question+='\n\nНапишите'+choices
            assert all(f'{n}.' in choices for n in range(1,6))
        c=base(unit,question,record['publishedTotal'],record['questionPages'],record['schemePages'])
        c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
        criteria=[{'id':'content','label':'Communication/content (C)','maxMarks':10 if is_essay else 15,'permittedMarks':list(range(11 if is_essay else 16)),'guidance':[squash(content)]}]
        if is_essay:
            title=squash(re.search(r'Candidates are required.*?overall\s+content score\.',content,re.S).group())
            criteria.append({'id':'title-penalty','label':'Essay title penalty','kind':'deduction','deductFrom':'content','maxMarks':1,'permittedMarks':[0,1],'guidance':[title]})
        limits=[{'id':'lower-e','scaleLabel':'Lower E','maxMarks':14 if is_essay else 10,'when':{'any':[{'criterionIds':['content'],'atMost':5 if is_essay else 7,**({'ignoreDeductions':True} if is_essay else {})},{'length':'words','below':25 if is_essay else 60}]},'bands':lower,'guidance':[lower_e]},
                {'id':'lower-a','scaleLabel':'Lower A','minMarks':9 if is_essay else 7,'maxMarks':14 if is_essay else 12,'when':{'any':[{'flag':'lower-a','prompt':lower_a}]},'bands':accuracy,'guidance':[lower_a]}]
        if is_essay:
            no_content=squash(re.search(r'Answers which.*?no marks for\s+language\.',content,re.S).group())
            limits.append({'id':'no-content','maxMarks':0,'when':{'any':[{'criterionIds':['content'],'atMost':0,'ignoreDeductions':True}]},'guidance':[no_content]})
        global_view=squash(expression[:expression.index('If the content mark')]).rstrip('•\uf0b7 ').strip()
        annotation=squash(between(expression,'Put square box','Penalise '))
        annotation=('Put square box')+' '+annotation
        accommodations=between(source['generalWrittenGuidance'],'Waivers:','Language issues')
        accommodations='Waivers: '+accommodations
        criteria.append({'id':'expression','label':'Language + expression (E)','maxMarks':maximum,'permittedMarks':list(range(maximum+1)),'guidance':[global_view,annotation,accommodations],'bands':normal,'limits':limits})
        if not is_essay:
            coherence=[band(price,description) for price,description in S[13].find_tables().tables[0].extract()[1:]]
            criteria.append({'id':'coherence','label':'Textual coherence (TC)','maxMarks':10,'permittedMarks':list(range(11)),'guidance':[],'bands':coherence})
        criteria.append({'id':'soft-sign-penalty','label':'Soft sign penalty','kind':'deduction','deductFrom':'expression','maxMarks':2,'permittedMarks':[0,1,2] if is_essay else [0,2],'guidance':[soft]})
        c['rubric']={'system':'language-writing','taskRequirements':[],'markingGuideNote':'','criteria':criteria}
        c['review']['guidancePages']=[3]
        if not is_essay:
            guide=page_text(S,12);heads=list(re.finditer(r'^\s*[1-3]\.\s+(?:LETTER|INTERVIEW|DISCUSSION)',guide,re.M));assert len(heads)==3
            end=guide.index('Communication + content')
            c['rubric']['taskRequirements']=[squash(guide[h.start():heads[n+1].start() if n+1<len(heads) else end]) for n,h in enumerate(heads)]
            c['rubric']['taskRequirements'].append(squash(re.search(r'If a candidate answers.*?one\(s\)\.',guide,re.S).group()))
            c['rubric']['markingGuideNote']='The scheme explicitly gives choice-specific category lists, retained above. Its later general minimum-category shorthand A–D / A–E / A–D(E,F,G) does not fully match those lists. Both versions remain visible; no per-category numeric split or automatic conversion is imposed. Follow every required point in the original chosen task.'
        result.append(c)
    return result

def grammar_forms(docs):
    paper='\n'.join(docs['paper'][p-1].get_text(clip=fitz.Rect(20,30,580,793),sort=False) for p in (11,12))
    paper=paper[paper.index('Я люблю отмечать'):]
    solved=docs['scheme'][8].get_text();solved=solved[solved.index('Я люблю отмечать'):]
    gaps=list(re.finditer(r'\(([^)]+)\)\s*[.\u2026]+\s*',paper));assert len(gaps)==15
    # The scheme edits unrelated connective prose (и -> При этом), so bind
    # each actual gap by its nearest fixed words instead of inventing a
    # whole-passage equality or silently changing the original question.
    fixed=lambda words:r'[^\w]*'.join(re.escape(word) for word in words)
    forms=[]
    for n,gap in enumerate(gaps):
        before=paper[gaps[n-1].end() if n else 0:gap.start()]
        after=paper[gap.end():gaps[n+1].start() if n+1<len(gaps) else len(paper)]
        left=re.findall(r'\w+',before)[-4:];right=re.findall(r'\w+',after)[:4]
        assert left and right,(n,left,right)
        matches=re.findall(fixed(left)+r'[^\w]+(\w+)[^\w]+'+fixed(right),solved,re.I)
        assert len(matches)==1,(n,left,right,matches)
        forms.append((gap[1],matches[0]))
    assert [answer for prompt,answer in forms]==['отмечают','рождения','был','дня','бабушек','придумывала','кремом','шоколадом','организовываю','моей','целую','Мне','люблю','выбирают','приятных']
    return forms

def grammar(docs,source):
    r=next(r for r in source['tasks'] if r['unit']=='GR');forms=grammar_forms(docs)
    c=as_points(source_card(r),[answer for prompt,answer in forms],15)
    for g,(prompt,answer) in zip(c['rubric']['groups'],forms):g['label']=prompt
    guide=r['publishedSourceBlock'].split('Я люблю отмечать')[0]
    c['rubric']['taskRequirements']=[guide]
    return [c]

def listening(docs,source):
    result=[]
    audio=next(r['source'] for r in json.loads((ROOT/'data/russianAudio.json').read_text()) if r['year']==2014)
    for r in source['tasks']:
        if r['unit'] not in ('L1','L2','L3','L4'):continue
        key=(r['unit'],r['item'],r['roman']);body=r['publishedSourceBlock'];pool=body;partial='';extra=[]
        if 'Assign one mark' in pool:pool,partial=pool.split('Assign one mark',1);partial='Assign one mark'+partial
        if 'Assign no marks:' in pool:pool,rejection=pool.split('Assign no marks:',1);extra.append('Assign no marks:'+rejection)
        if 'Assign full marks where' in pool:pool,acceptance=pool.split('Assign full marks where',1);extra.append('Assign full marks where'+acceptance)
        answers=options(pool);mapping={}
        if key==('L1',2,None):
            partials=options(partial.split('of:',1)[1]);assert len(partials)==len(answers)==5
            mapping={i:[answer] for i,answer in enumerate(partials)}
        elif key==('L2',1,None):
            assert answers[3]=='first 30 stations' and partial=='Assign one mark to: 30 offices'
            mapping={3:['30 offices']}
        elif key==('L4',1,None):
            assert 'great-grandfather (Surikov)' in answers[3]
            mapping={3:[partial.split(':',1)[1].strip()]}
        c=as_points(source_card(r),answers,r['detailQuota'],mapping)
        if key in (('L1',3,'i'),('L3',2,'i'),('L4',3,'i')):
            c.pop('rubric');c['rubric']={'system':'language-writing','criteria':[
                {'id':f'detail-{n}','label':f'Distinct detail {n}','maxMarks':2,'permittedMarks':[0,1,2],'guidance':[body]}
                for n in range(1,r['detailQuota']+1)],'taskRequirements':[],
                'markingGuideNote':'Assess each distinct response once against the complete published full and partial pools. Do not infer a unique full/partial association from list position, and do not count the same detail again as a paraphrase.'}
            if key==('L1',3,'i'):
                c['rubric']['markingGuideNote']+=' Source placement: the one-mark concert / May / 8:00 list is printed immediately below the band question, before the separate upcoming-event question. It is retained here exactly as published; the scheme does not explain this apparent mismatch.'
        elif key==('L3',4,None):
            assert len(extra)==1
            c['rubric']['groups'] += [{'id':f'other-section-{n}','label':f'Other-section distinct detail {n}','rows':[],
                'criteria':[{'id':f'other-section-{n}','label':f'Different detail from another section {n}','maxMarks':2,'permittedMarks':[0,2],'guidance':[extra[0]]}]} for n in (1,2)]
            c['rubric']['markingGuideNote']='The printed two-detail maximum includes the express allowance for details from other sections. Use an other-section slot only for a different actual detail, and do not repeat a detail already claimed from this list or in the other slot. No extra marks or invented partial tariff are added.'
        if partial:extra.append(partial)
        c['rubric']['taskRequirements']=[source['listeningGuidance']]+extra
        c['review']['guidancePages']=[15]
        c['topicId']=r['topicId'];c['additionalTopicIds']=['russian-1-0']
        c['sourceMaterial']['kind']='source-question';c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
        c['audioMaterial']=audio;result.append(c)
    assert len(result)==20 and sum(c['totalMarks'] for c in result)==80
    return result

def source_language_rules(cards,source):
    rule='Language of answer:'+between(source['generalWrittenGuidance'],'Language of answer:','Decoding the marking scheme:')
    for c in cards:
        if c['section'] not in ('C1','C2','LA2','GR','SE','GW'):continue
        c['answerLanguageRule']={'otherLanguageMultiplier':0,'sourceText':squash(rule),'schemePages':[3]}
        if c['section'] in ('C1','C2'):c['rubric']['markingGuideNote']+=' Answer in English or Irish. Both languages are permitted by the original bilingual paper.'

def build():
    docs,source=source_records()
    cards=reading(source)+summaries(source)+language_and_matching(docs,source)+grammar(docs,source)+writing(docs,source,base)+listening(docs,source)
    source_language_rules(cards,source)
    assert len(cards)==40 and len({c['id'] for c in cards})==40
    assert sum(c['totalMarks'] for c in cards)==300
    assert sum(bool(c.get('answerLanguageRule')) for c in cards)==17
    for doc in docs.values():doc.close()
    return cards

if __name__=='__main__':save_reviewed(build())
