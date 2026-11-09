"""Russian 2016 Higher source-bound authoring preparation; not yet published."""
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

METADATA = {'paper': {'pages': 16, 'sha256': '37d0b278496335fe827bea49c8f89ccc1c77baa706815493557379e4466012d4'}, 'aural': {'pages': 8, 'sha256': '34402a6c1c8c769f9383e5c93d1c71b5b3e2fac9703ca8045ccb4c89491a623b'}, 'scheme': {'pages': 20, 'sha256': 'ec7771b35c2c806b9e0f2cc8a35626cd3a8e85a9c991afc8089f4319decc19e4'}}

def source_records():
    docs = {}
    for kind, relative in [('paper', 'papers/2016-hl-000-paper.pdf'),
                           ('aural', 'papers/2016-hl-A00-paper.pdf'),
                           ('scheme', 'schemes/2016-hl.pdf')]:
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
        return dict(id='ru-2016-hl-' + unit.lower() + (f'-{item}' if item is not None else '') + (f'-{roman}' if roman else ''),
                    unit=unit, item=item, roman=roman, question=question, questionPages=qp,
                    component=component, publishedSourceBlock=squash(body), schemePages=sp,
                    publishedTotal=total, **extra)

    cards = []
    source = '\n'.join(page(S, p) for p in (4, 5)).split('Language awareness')[0]
    blocks = numbered_blocks(source)
    asks = [(i,r,question_text(q),p) for p in (3,4) for i,r,q in numbered_blocks(page(Q,p,True))]
    assert len(blocks) == len(asks) == 9
    totals = [2,6,6,2,4,4,6,6,4]
    for (i,r,b),(qi,qr,q,p),total in zip(blocks,asks,totals):
        assert (i,r)==(qi,qr)
        price = re.search(r'(\d)\s*x\s*2\s*=\s*(\d)',b)
        assert price and int(price.group(2))==total
        cue,body=b[:price.start()],b[price.start():]
        assert score(bag(q),bag(cue))>.75,(q,cue)
        cards.append(record('C1',i,r,q,[p],body,[4,5],total))
    assert sum(c['publishedTotal'] for c in cards)==40

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
                            reviewNote='Summary4 must have an actual zero-discretion control for failing to understand they returned one week later.' if i==4 else ''))

    q='Supply the nominative singular form '+squash(between(page(Q,5,True),'Supply the nominative singular form')).split('1.')[0].strip()
    b='Supply the nominative singular form '+between(page(S,5),'Supply the nominative singular form')
    cards.append(record('LA1',None,None,q,[5],b,[5],10,fullQuestionPage=page(Q,5),
                        scoring=dict(chosenPhrases=5,availablePhrases=6,perAdjective=1,perNoun=1),
                        reviewNote='The paper explicitly chooses five of six; preserve separately claimable adjective/noun marks.'))
    text=page(Q,9,True)
    q='Semantic field / '+squash(between(text,'Semantic field /','Q.2.3.'))
    b='Q.2.2. '+between(page(S,7),'Q.2.2.','Q.2.3.')
    cards.append(record('LA2',None,'i',q,[9],b,[7],5,printedAddress='Q.2.2',scoring=dict(correctWords=5,perWord=1)))
    q='Verbs: '+question_text(between(text,'Verbs:'))
    b='Q.2.3. '+between(page(S,7),'Q.2.3.')
    cards.append(record('LA2',None,'ii',q,[9],b,[7],5,printedAddress='Q.2.3',scoring=dict(correctInfinitives=5,perInfinitive=1)))
    q='Read the following information '+squash(between(page(Q,10,True),'Read the following information'))
    q=q[:q.index('(20 marks)')+len('(20 marks)')]
    table=S[7].find_tables().tables[0].extract()
    rows=[[squash(v or '') for v in row] for row in table]
    assert [r[0] for r in rows]==['1','8','5','7','9','4','10','3','6','2'],rows
    cards.append(record('SD',None,None,q,[10],page(S,8),[8],20,answerRows=rows,scoring=dict(correctAnswers=10,perAnswer=2)))
    q='Read through the following text. '+squash(between(page(Q,11,True),'Read through the following text.'))
    q=q[:q.index('substitute words.')+len('substitute words.')]
    cards.append(record('GR',None,None,q,[11],page(S,9),[9],30,scoring=dict(correctForms=15,perForm=2),
                        reviewNote='All15 forms confirmed in full-size original scheme p9, including времени. Preserve мной/мною and пароходе/пароходах.'))
    q='Write a short essay '+squash(between(page(Q,12,True),'Write a short essay'))
    q=q[:q.index('essay title.')+len('essay title.')]
    cards.append(record('SE',None,None,q,[12],'\n'.join(page(S,p) for p in (10,11)),[10,11],30,fullQuestionPage=page(Q,12),
                        sourceNote='Source Lower A range9–14; all five topic choices preserved.'))
    q='Write a piece '+question_text(between(page(Q,13,True),'Write a piece'))
    cards.append(record('GW',None,None,q,[13],'\n'.join(page(S,p) for p in (12,13,14)),[12,13,14],40,
                        sourceNote='Source Lower A range7–12; all three writing choices and letterA–F retained.'))
    assert len(cards)==20 and sum(c['publishedTotal'] for c in cards)==220

    source='\n'.join(page(S,p) for p in (15,16,17))
    heads=list(re.finditer(r'^\s*Section (1|II|III|IV)\s*$',source,re.M))
    assert len(heads)==4
    counts=[[3,3,2,1,1],[1,1,5,3],[1,1,1,3,3,1],[3,2,2,1,2]]
    starts=[['Zhu-zhu +','Singer song-writer','(quality of )','Russian Imperial','(Live) music'],
            ['To bring together','Boys +','Sporting activities','Timetable:'],
            ['7 (years old)','(She was/at) 16','music ','Was (walking)','Hip hop','Emigrate'],
            ['Was born','(after leaving school)','Got his first','(In 2006)','He left education']]
    topics=[['russian-0-7','russian-0-5','russian-0-7','russian-0-7','russian-0-7'],
            ['russian-0-3','russian-0-3','russian-0-5','russian-0-9'],
            ['russian-0-5','russian-0-5','russian-0-5','russian-0-8','russian-0-5','russian-0-6'],
            ['russian-0-1','russian-0-3','russian-0-7','russian-0-4','russian-0-4']]
    for n,h in enumerate(heads):
        section=n+1;b=source[h.end():heads[n+1].start() if n+1<len(heads) else len(source)]
        blocks=numbered_blocks(b);asks=[(i,r,question_text(q)) for i,r,q in numbered_blocks(page(A,section+1,True))]
        assert len(blocks)==len(asks)==len(counts[n])
        for (i,r,b),(qi,qr,q),count,start,topic in zip(blocks,asks,counts[n],starts[n],topics[n]):
            assert (i,r)==(qi,qr)
            cue,body=source_split(b,start);assert score(bag(q),bag(cue))>.8,(q,cue)
            sp=[15,16] if section==1 else [16] if section==2 else [16,17] if section==3 else [17]
            cards.append(record(f'L{section}',i,r,q,[section+1],body,sp,count*2,detailQuota=count,topicId=topic,
                                reviewNote='Retain cross-question accepted pools exactly where source expressly permits them; no inferred cross-question expansion.'))
    assert len(cards)==40 and sum(c['publishedTotal'] for c in cards)==300
    assert len({c['id'] for c in cards})==40
    norm=lambda t:re.sub(r'[^\w]','',t.casefold())
    for c in cards:
        assert norm(c['publishedSourceBlock']) in norm('\n'.join(page(S,p) for p in c['schemePages'])),c['id']
    draft=dict(status='Source-only draft; not runtime cards or a completed sitting',sources=METADATA,
               independentTasks=40,writtenTasks=20,listeningTasks=20,generalWrittenGuidance=squash(page(S,3)),
               comprehensionGuidance=squash(page(S,4).split('1.i.')[0]),
               summaryGuidance=squash(summary_source.split('1. Why')[0]),
               listeningGuidance=squash(source[:heads[0].start()]),tasks=cards)
    return docs, draft

from ru_review_2026_hl import base as common_base, as_points, save_reviewed, mark_range
from ru_review_2017_hl import named_group, options, band

def base(*args, **kwargs):
    c=common_base(*args,**kwargs)
    for f in ('id','questionRef'):c[f]=c[f].replace('2026','2016')
    c['year']=2016;c['sourceMaterial']['title']=c['sourceMaterial']['title'].replace('2026','2016')
    return c

def source_card(record):
    pages=[2,3,4] if record['unit']=='C1' else [6,7,8,9] if record['unit']=='LA2' else [6,7,8] if record['unit']=='C2' else record['questionPages']
    c=base(record['unit'],record['question'],record['publishedTotal'],pages,record['schemePages'],record['item'],record['roman'])
    c['review']['questionPages']=record['questionPages']
    return c
def writing(docs, source, base):
    S=docs['scheme']; result=[]
    for unit,sp,table_page in [('SE',10,11),('GW',13,13)]:
        record=next(c for c in source['tasks'] if c['unit']==unit)
        text=S[sp-1].get_text()
        content=between(text,'1. Communication/content (C)','2. Expression (E):')
        expression=between(text,'2. Expression (E):')
        lower_e=squash(re.search(r'If the content mark.*?indicate this\.',expression,re.S).group())
        lower_a=squash(re.search(r'If the expression is very fluent.*?indicate this\.',expression,re.S).group())
        soft=squash(re.search(r'Penalise students.*?\(– 1\)\.',expression,re.S).group())
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
            accuracy=[band(price,description) for price,description in S[13].find_tables().tables[0].extract()[1:]]
            assert [b['marks'] for b in accuracy]==[[11,12],[9,10],[7,8]]
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
            title=squash(re.search(r'Candidates are required.*?overall content score\.',content,re.S).group())
            criteria.append({'id':'title-penalty','label':'Essay title penalty','kind':'deduction','deductFrom':'content','maxMarks':1,'permittedMarks':[0,1],'guidance':[title]})
        limits=[{'id':'lower-e','scaleLabel':'Lower E','maxMarks':14 if is_essay else 10,'when':{'any':[{'criterionIds':['content'],'atMost':5 if is_essay else 7,**({'ignoreDeductions':True} if is_essay else {})},{'length':'words','below':25 if is_essay else 60}]},'bands':lower,'guidance':[lower_e]},
                {'id':'lower-a','scaleLabel':'Lower A','minMarks':9 if is_essay else 7,'maxMarks':14 if is_essay else 12,'when':{'any':[{'flag':'lower-a','prompt':lower_a}]},'bands':accuracy,'guidance':[lower_a]}]
        if is_essay:
            no_content=squash(re.search(r'Answers which.*?no marks for\s+language\.',content,re.S).group())
            limits.append({'id':'no-content','maxMarks':0,'when':{'any':[{'criterionIds':['content'],'atMost':0,'ignoreDeductions':True}]},'guidance':[no_content]})
        global_view=squash(expression[:expression.index('If the content mark')]).rstrip('•\uf0b7 ').strip()
        annotation=squash(between(expression,'Put square box','Penalise students'))
        annotation=('Put square box')+' '+annotation
        accommodations=between(source['generalWrittenGuidance'],'Waivers:','Language issues')
        accommodations='Waivers: '+accommodations
        criteria.append({'id':'expression','label':'Language + expression (E)','maxMarks':maximum,'permittedMarks':list(range(maximum+1)),'guidance':[global_view,annotation,accommodations],'bands':normal,'limits':limits})
        if not is_essay:
            coherence=[band(price,description) for price,description in S[13].find_tables().tables[1].extract()[1:]]
            criteria.append({'id':'coherence','label':'Textual coherence (TC)','maxMarks':10,'permittedMarks':list(range(11)),'guidance':[],'bands':coherence})
        criteria.append({'id':'soft-sign-penalty','label':'Soft sign penalty','kind':'deduction','deductFrom':'expression','maxMarks':1,'permittedMarks':[0,1],'guidance':[soft]})
        c['rubric']={'system':'language-writing','taskRequirements':[],'markingGuideNote':'','criteria':criteria}
        c['review']['guidancePages']=[3]
        result.append(c)
    return result

def manual_card(record,source,labels,maximum,permitted,guidance,note=''):
    c=source_card(record);c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
    c['rubric']={'system':'language-writing','criteria':[{'id':f'answer-{n}','label':label,'maxMarks':maximum,'permittedMarks':permitted,'guidance':[]} for n,label in enumerate(labels,1)],'taskRequirements':guidance,'markingGuideNote':note}
    return c


def reading(source):
    result=[]
    for r in source['tasks']:
        if r['unit']!='C1':continue
        key=(r['item'],r['roman']);body=r['publishedSourceBlock']
        if key==(1,'ii'):
            food=between(body,'What does Pavel eat?','why does he eat there?')
            reason=between(body,'why does he eat there?')
            food_pool=between(food,'maximum of 4:','assign one mark:')
            partial=between(food,'assign one mark:','assign no marks:')
            reasons=between(reason,'maximum of 4:')
            c=as_points(source_card(r),[],2)
            c['rubric']['groups']=[named_group('food','What Pavel eats',options(food_pool),2),named_group('reasons','Why he eats there',options(reasons),2)]
            main=c['rubric']['groups'][0]['rows'][2]
            assert main['text']=='main course/ second course/ second dish' and partial.strip()=='second meal'
            main['steps']=[0,1,2]
            c['rubric']['allocationCap']={'maxMarks':6,'answerCount':3,'sourceText':body,'schemePages':[4]}
            c['rubric']['markingGuideNote']='The one-mark step on the main-course row applies to the published partial “second meal”; its complete answer earns two. A complete and partial version of the same detail cannot earn both awards. Each named category is capped at two details, with three details overall.'
        elif key==(3,'i'):
            c=manual_card(r,source,['First distinct detail','Second distinct detail'],2,[0,1,2],[body],
                'The scheme lists the one-mark partials at question level without tying them to a particular full-credit snow activity. Use the exact published full and partial wording to place each distinct answer once; no exclusive partial-to-activity mapping is inferred.')
        else:
            rejected='';partial=''
            if 'assign no marks:' in body:body,rejected=body.split('assign no marks:',1)
            if 'assign one mark:' in body:body,partial=body.split('assign one mark:',1)
            full=between(body,'assign two marks:');answers=options(full);partials=options(partial)
            mapping={}
            if key==(1,'i'):
                assert len(answers)==3 and len(partials)==4
                mapping={1:partials[2:],2:partials[:2]}
            elif key==(1,'iii'):
                assert len(answers)==9 and partials==['looks at his collection'];mapping={3:partials}
            else:assert not partials,(key,partials)
            c=as_points(source_card(r),answers,r['publishedTotal']//2,mapping)
            c['rubric']['taskRequirements']=['assign no marks: '+rejected] if rejected else []
        c['rubric']['taskRequirements'].insert(0,source['comprehensionGuidance'])
        c['review']['guidancePages']=[4]
        result.append(c)
    assert len(result)==9 and sum(c['totalMarks'] for c in result)==40
    return result


def summaries(source,docs):
    result=[];general=source['summaryGuidance']
    incomplete=next(x for x in general.split('. ') if 'fails to answer all' in x)
    for r in source['tasks']:
        if r['unit']!='C2':continue
        body=r['publishedSourceBlock'];special=''
        if 'Do not assign discretionary marks' in body:body,special=body.split('Do not assign discretionary marks',1);special='Do not assign discretionary marks'+special
        primary,secondary=body.split('Secondary details:',1)
        answers=options(between(primary,'Main points:'))+options(secondary)
        c=as_points(source_card(r),answers,4,steps=[0,1,2])
        if r['item']==4:
            a=answers.index('friends were smoking');b=answers.index('smoking')
            passage=docs['paper'][6].get_text()
            assert passage.count('курили')==1
            group=c['rubric']['groups'][a];group['label']='One smoking event'
            group['rows'].append({'id':'other-published-wording','text':answers[b],'marks':2,'steps':[0,1,2]})
            c['rubric']['groups'].pop(b)
            c['rubric']['markingGuideNote']='The scheme prints both “friends were smoking” and “smoking”. They refer to the single smoking event in paragraph 4 on original paper page 7 (курили); both wordings are preserved and the event earns credit once.'
            c['review']['paperAnswerSources']=[{'text':'курили','pages':[7],'schemeAcceptance':'No marks for details not included in the source text.'}]
        limits=[{'id':'incomplete-response','maxMarks':1,'when':{'any':[{'flag':'incomplete-response','prompt':incomplete}]},'guidance':[incomplete]}]
        if special:limits.append({'id':'missed-return-delay','maxMarks':0,'when':{'any':[{'flag':'missed-return-delay','prompt':special}]},'guidance':[special]})
        c['rubric']['criteria']=[{'id':'summary-skills','label':'Discretionary marks','maxMarks':2,'permittedMarks':[0,1,2],'guidance':[general],'limits':limits}]
        c['rubric']['taskRequirements']=[general]
        result.append(c)
    assert len(result)==4
    return result

def language_and_matching(docs,source):
    result=[]
    for r in source['tasks']:
        if r['unit'] not in ('LA1','LA2','SD','GR'):continue
        body=r['publishedSourceBlock']
        if r['unit']=='LA1':
            entries=[squash(x) for x in re.split(r'\s[1-6]\.\s+',body)[1:]]
            assert len(entries)==12 and all(len(x.split())==2 for x in entries),entries
            c=as_points(source_card(r),[],5)
            c['rubric']['groups']=[named_group(f'phrase-{i+1}',entries[i],entries[6+i].split(),2,1) for i in range(6)]
            c['rubric']['taskRequirements']=[body[:body.index('1. выпускные')]]
        elif r['unit']=='LA2' and r['roman']=='i':
            pool=between(body,'5 x 1 = 5','Assign no marks')
            answers=[squash(x).rstrip('.') for x in pool.split(',')]
            assert len(answers)==16
            c=as_points(source_card(r),answers,5)
            for g in c['rubric']['groups']:g['rows'][0]['marks']=1
            c['rubric']['taskRequirements']=['Give one mark for each correct answer.','Assign no marks'+between(body,'Assign no marks')]
        elif r['unit']=='LA2':
            entries=[squash(x).split() for x in re.split(r'\s[1-5]\.\s+',body)[1:]]
            assert len(entries)==5 and all(len(x)==2 for x in entries),entries
            c=as_points(source_card(r),[x[1] for x in entries],5)
            for g,pair in zip(c['rubric']['groups'],entries):g['label']=pair[0];g['rows'][0]['marks']=1
            c['rubric']['taskRequirements']=['Do not assign any marks where candidates translate'+between(body,'Do not assign any marks where candidates translate','1. пошли')]
        elif r['unit']=='SD':
            rows=r['answerRows'];assert len(rows)==10
            c=as_points(source_card(r),[row[1]+' — '+row[0] for row in rows],10)
            c['rubric']['taskRequirements']=['2 marks for each correct answer']
        else:
            page=docs['scheme'][8];frames={}
            for drawing in page.get_drawings():
                box=drawing['rect']
                if box.y0>260 and box.height<1 and box.width>5:
                    frames.setdefault((round(box.x0,1),round(box.x1,1)),[]).append(round(box.y0,1))
            assert len(frames)==15 and all(len(y)==2 for y in frames.values())
            forms=[]
            for (left,right),ys in sorted(frames.items(),key=lambda item:(min(item[1]),item[0][0])):
                top,bottom=sorted(ys)
                assert 10<bottom-top<20
                forms.append(squash(page.get_text(clip=fitz.Rect(left-1,top-1,right+1,bottom+1))).rstrip('.,'))
            assert forms==['свою','мной/ мною','закончил','пароходе/пароходах','севере','переехал','музыке','музыкальной','детям','дедушкой','уезжают','появляется','времени','долгой','них'],forms
            c=as_points(source_card(r),[],15)
            c['rubric']['groups']=[named_group(f'form-{i+1}',f'Form {i+1}',[squash(x) for x in form.split('/')]) for i,form in enumerate(forms)]
            c['rubric']['taskRequirements']=['TWO marks per correct form 15 x 2 = 30','In this exercise'+between(body,'In this exercise','Здравствуйте')]
        result.append(c)
    assert len(result)==5 and sum(c['totalMarks'] for c in result)==70
    return result
def listening(docs,source):
    result=[];records={(r['unit'],r['item'],r['roman']):r for r in source['tasks'] if r['unit'].startswith('L') and r['unit'] in ('L1','L2','L3','L4')}
    audio=next(r['source'] for r in json.loads((ROOT/'data/russianAudio.json').read_text()) if r['year']==2016)
    full_credit='Award two marks for each correct/relevant point.'
    for key,r in records.items():
        body=r['publishedSourceBlock'];extra=[]
        if key==('L1',2,None):
            full,partial=body.split('Assign one mark:',1);first,remaining=full.split('+',1)
            c=as_points(source_card(r),[],3)
            c['rubric']['groups']=[named_group('singer-songwriter','Singer/songwriter detail',[squash(first)],partials=options(partial))]
            for i in range(1,4):
                c['rubric']['groups'].append({'id':f'other-detail-{i}','label':f'Other distinct detail {i}','rows':[],
                    'criteria':[{'id':f'other-detail-{i}-credit','label':f'Other distinct detail {i}','maxMarks':2,'permittedMarks':[0,2],'guidance':[full_credit]}]})
            extra=[body]
            c['rubric']['markingGuideNote']='Assess three distinct details in total. Singer/songwriter is one concept: the complete detail earns two marks or one printed partial earns one, once. Use the other slots for different full-credit details. The printed travel span uses “=” and repeats “USA” in festival and solo-concert context; the scheme does not resolve how those descriptions overlap. Its complete wording is retained above without an invented geography grouping, deduplication or automatic exclusivity.'
        elif key==('L2',2,None):
            general,sports,other=body.split('//')
            c=as_points(source_card(r),options(other),5)
            c['rubric']['alternativeSets']=[{'id':'sports','label':'General or specific sporting details','sourceText':body,'schemePages':[16]}]
            groups=[named_group('sports-general','Sporting activities',[squash(general)]),named_group('sports-specific','Named sporting activities',options(sports),4)]
            for g in groups:g['alternativeSet']='sports'
            c['rubric']['groups'].extend(groups)
            c['rubric']['allocationCap']={'maxMarks':10,'answerCount':5,'sourceText':r['question'],'schemePages':[16]}
            c['rubric']['markingGuideNote']='The slash layout gives a general sporting-activities route or the named-sports route. Keep the other listed activities independent; assess five distinct details overall.'
        elif key==('L2',3,None):
            time=between(body,'Timetable:','Location:');where=between(body,'Location:','Price:');price=between(body,'Price:','Assign no marks:')
            c=as_points(source_card(r),[],3)
            c['rubric']['groups']=[named_group('timetable','Timetable',[squash(time)]),named_group('location','Location',[squash(where)]),named_group('price','Price',options(price))]
            extra=[body]
            c['rubric']['markingGuideNote']='The question names location, price and timetable, and the scheme mirrors those three categories. Assess one detail in each category. This is a reviewed interpretation of the combined question and layout; the original price line retains its plus sign and is not rewritten as a printed either/or instruction.'
        elif key in [('L4',2,'i'),('L4',2,'ii')]:
            other=records[('L4',2,'ii' if key[-1]=='i' else 'i')]['publishedSourceBlock']
            c=manual_card(r,source,['First distinct detail','Second distinct detail'],2,[0,1,2] if key[-1]=='i' else [0,2],
                [body,other],
                'The scheme expressly permits details from the paired education/achievements question. Its complete original guidance is shown alongside this question’s own full and partial guidance. Assess each distinct detail once; no unprinted partial-to-full association is inferred.')
            if key[-1]=='ii':
                c['rubric']['markingGuideNote']+=' The one-mark partial “started doing music” is explicitly priced only in Q2(i). The source does not establish its tariff when transferred to Q2(ii); leave that cross-question partial unassessed here. The 0/2 controls apply to clear full-credit details, without converting that unresolved partial to either one or two marks.'
        else:
            cross='';rejected='';partial=''
            if 'Assign full marks' in body:body,cross=body.split('Assign full marks',1);cross='Assign full marks'+cross
            if 'Assign no marks:' in body:body,rejected=body.split('Assign no marks:',1)
            if 'Assign one mark:' in body:body,partial=body.split('Assign one mark:',1)
            answers=options(body);mapping={}
            if partial:
                pos={('L1',1,None):3,('L1',4,'i'):0,('L3',2,'i'):0,('L4',1,None):0}[key]
                mapping={pos:options(partial)}
            c=as_points(source_card(r),answers,r['detailQuota'],mapping)
            if key==('L1',4,'i'):
                for i,answer in enumerate(options(records[('L1',4,'ii')]['publishedSourceBlock']),1):c['rubric']['groups'].append(named_group(f'programme-{i}','Programme detail',[answer]))
            elif key==('L3',3,'ii'):
                c['rubric']['groups'].append({'id':'cross-section','label':'Another detail allowed by the source','rows':[],
                    'criteria':[{'id':'cross-section-credit','label':'Another accepted detail','maxMarks':2,'permittedMarks':[0,2],'guidance':[cross]}]})
                c['rubric']['markingGuideNote']='The additional response slot preserves the printed allowance for details from other sections. Assess it against that source allowance; no new model answer is invented.'
            if cross:extra.append(cross)
            if rejected:extra.append('Assign no marks: '+rejected)
        c['rubric']['taskRequirements']=[source['listeningGuidance']]+c['rubric']['taskRequirements']+extra
        c['review']['guidancePages']=[15]
        c['topicId']=r['topicId'];c['additionalTopicIds']=['russian-1-0']
        c['sourceMaterial']['kind']='source-question';c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
        c['audioMaterial']=audio;result.append(c)
    assert len(result)==20 and sum(c['totalMarks'] for c in result)==80
    return result


def source_language_rules(cards,source):
    rule='Language of answer:'+between(source['generalWrittenGuidance'],'Language of answer:','Quality of English:')
    for c in cards:
        if c['section'] not in ('C1','C2','LA1','LA2','GR','SE','GW'):continue
        c['answerLanguageRule']={'otherLanguageMultiplier':0,'sourceText':squash(rule),'schemePages':[3]}
        if c['section'] in ('C1','C2'):c['rubric']['markingGuideNote']+=' Answer in English or Irish. Both languages are permitted by the original bilingual paper.'


def build():
    docs,source=source_records()
    cards=reading(source)+summaries(source,docs)+language_and_matching(docs,source)+writing(docs,source,base)+listening(docs,source)
    source_language_rules(cards,source)
    assert len(cards)==40 and len({c['id'] for c in cards})==40
    assert sum(c['totalMarks'] for c in cards)==300
    assert sum(bool(c.get('answerLanguageRule')) for c in cards)==19
    for doc in docs.values():doc.close()
    return cards


if __name__=='__main__':save_reviewed(build())
