"""Russian 2015 Higher: hash-bound original selectors and source-defined scoring."""
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

METADATA = {'paper': {'pages': 16, 'sha256': '119308b8b944f4a21dab09cf461ebb94c84cb4289458b38925634cc74ed45e66'}, 'aural': {'pages': 8, 'sha256': 'ffc5916d6a67988ce34ebc982b8d10c62e420e01593ae9c953008e0035439dbd'}, 'scheme': {'pages': 20, 'sha256': '210b81b664cfac3107aed4c750d839c70c82777d40b92c805f7f5db60d1c730c'}}

def source_records():
    docs = {}
    for kind, relative in [('paper', 'papers/2015-hl-000-paper.pdf'),
                           ('aural', 'papers/2015-hl-A00-paper.pdf'),
                           ('scheme', 'schemes/2015-hl.pdf')]:
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
        return dict(id='ru-2015-hl-' + unit.lower() + (f'-{item}' if item is not None else '') + (f'-{roman}' if roman else ''),
                    unit=unit, item=item, roman=roman, question=question, questionPages=qp,
                    component=component, publishedSourceBlock=squash(body), schemePages=sp,
                    publishedTotal=total, **extra)

    cards=[]
    source='\n'.join(page(S,p) for p in (4,5))
    blocks=numbered_blocks(source)
    asks=[(i,r,question_text(q),p) for p in (3,4) for i,r,q in numbered_blocks(page(Q,p,True))]
    assert len(blocks)==len(asks)==13
    totals=[4,4,4,4,2,2,2,4,4,2,2,2,4]
    for (i,r,b),(qi,qr,q,p),total in zip(blocks,asks,totals):
        assert (i,r)==(qi,qr)
        price=re.search(r'(\d)\s*x\s*2\s*=\s*(\d)',b)
        assert price and int(price.group(2))==total
        cue,body=b[:price.start()],b[price.start():]
        assert score(bag(re.sub(r"\(Section \d+\)", "", q)),bag(cue))>.75,(q,cue)
        cards.append(record('C1',i,r,q,[p],body,[4,5],total,
                            sourceNote='Source awards4 for either complete institute-admission explanation, versus2 per other detail, under global4. Source-bound four-mark cap is represented explicitly.' if (i,r)==(2,'i') else ''))
    assert sum(c['publishedTotal'] for c in cards)==40
    summary_source='\n'.join(page(S,p) for p in (7,8)).split('Language awareness')[0]
    blocks=numbered_blocks(summary_source);asks=[]
    for p in (7,8):
        text=page(Q,p,True);heads=list(re.finditer(r'^\s*Section\s+([1-4])\s*$',text,re.M))
        asks.extend((int(h.group(1)),question_text(text[h.end():heads[n+1].start() if n+1<len(heads) else len(text)]),p) for n,h in enumerate(heads))
    assert len(blocks)==len(asks)==4
    for (i,r,b),(qi,q,p) in zip(blocks,asks):
        assert i==qi and r is None
        cue,body=source_split(b,'Main points:');assert score(bag(re.sub(r"\(Section \d+\)", "", q)),bag(cue))>.75,(q,cue)
        cards.append(record('C2',i,None,q,[p],body,[7,8],10,scoring=dict(detail=2,contentMaximum=8,discretionaryMaximum=2,partialDetail=1,incompleteDiscretionaryMaximum=1)))

    q='Match the words, '+squash(between(page(Q,5,True),'Match the words,'));q=q[:q.index('entitled WORDS.')+len('entitled WORDS.')]
    rows=[[squash(v or '') for v in row] for row in S[5].find_tables().tables[0].extract()]
    assert len(rows)==5 and [r[1] for r in rows]==['ему','окончат','школьную','за','тренировки']
    cards.append(record('LA1',None,None,q,[5],page(S,6),[6],10,answerRows=rows,scoring=dict(correctAnswers=5,perAnswer=2)))
    text=page(Q,9,True)
    q='Verbs: '+question_text(between(text,'Verbs:','Q.2.3.'))
    b='Q.2.2. '+between(page(S,8),'Q.2.2.','Q.2.3.')
    cards.append(record('LA2',None,'i',q,[9],b,[8],5,printedAddress='Q.2.2',scoring=dict(correctInfinitives=5,perInfinitive=1),reviewNote='Keep explicit old-form придти acceptance and прийдти/прити rejections.'))
    q='In the first section '+question_text(between(text,'In the first section'))
    b='Q.2.3. '+between(page(S,8),'Q.2.3.')
    cards.append(record('LA2',None,'ii',q,[9],b,[8],5,printedAddress='Q.2.3',scoring=dict(correctWords=5,perWord=1)))
    q='Read the following information. '+squash(between(page(Q,10,True),'Read the following information.'));q=q[:q.index('(20 marks)')+len('(20 marks)')]
    rows=[[squash(v or '') for v in row] for row in S[8].find_tables().tables[0].extract()]
    assert [r[0] for r in rows]==['5','7','6','8','4','3','2','10','9','1'],rows
    cards.append(record('SD',None,None,q,[10],page(S,9),[9],20,sourcePages=[10,11],answerRows=rows,scoring=dict(correctAnswers=10,perAnswer=2)))
    q='Read through the following text. '+squash(between(page(Q,12,True),'Read through the following text.'));q=q[:q.index('substitute words.')+len('substitute words.')]
    cards.append(record('GR',None,None,q,[12],page(S,10),[10],30,scoring=dict(correctForms=15,perForm=2),reviewNote='Keep all printed verb alternatives; no imported forms.'))
    q='Write a short essay '+squash(between(page(Q,13,True),'Write a short essay'));q=q[:q.index('(30 marks)')+len('(30 marks)')]
    cards.append(record('SE',None,None,q,[13],'\n'.join(page(S,p) for p in (11,12)),[11,12],30,fullQuestionPage=page(Q,13),sourceNote='Shared conditional Lower A range9–14; keep all cultural topic choices.'))
    q='Write a piece '+question_text(between(page(Q,14,True),'Write a piece'))
    cards.append(record('GW',None,None,q,[14],'\n'.join(page(S,p) for p in (13,14)),[13,14],40,sourceNote='Shared Lower A range7–12; table9–11 overlaps11–12 and disagrees with prose9/10. No unprinted category mapping.'))
    assert len(cards)==24 and sum(c['publishedTotal'] for c in cards)==220

    source='\n'.join(page(S,p) for p in (15,16,17))
    heads=list(re.finditer(r'^\s*Section (1|II|III|IV)\s*$',source,re.M));assert len(heads)==4
    counts=[[2,2,2,2,2],[3,3,2,2],[2,2,None,None,2],[2,2,1,1,2,2]]
    starts=[['Manager/administrator','Airport announcement','Excursion +','Voicemail message','TV presenter'],
            ['Central Artists House','40 films','Comedians /comics','Mini-quest'],
            ['To take up post','Has been boxing','Similar character','Senior trainer','It’s difficult'],
            ['When she was 7','Applied to architectural','began work','Where her place','Lived in the country','Decided/ thought']]
    topics=[['russian-0-14']*5,['russian-2-3']*4,
            ['russian-0-4','russian-0-5','russian-2-3','russian-0-4','russian-0-1'],
            ['russian-0-3','russian-0-3','russian-0-6','russian-0-11','russian-0-1','russian-0-6']]
    announcement_instruction='Give two details '+squash(between(page(A,2,True),'Give two details','1.'))
    joint_rule='Section 3: '+squash(between(page(S,16),'Section 3:','3.i.'))
    for n,h in enumerate(heads):
        section=n+1;b=source[h.end():heads[n+1].start() if n+1<len(heads) else len(source)]
        if section==1:b='1. Announcement 1'+between(b,'1. Announcement 1')
        blocks=numbered_blocks(b);asks=[(i,r,question_text(q)) for i,r,q in numbered_blocks(page(A,section+1,True))]
        assert len(blocks)==len(asks)==len(counts[n]),(section,blocks,asks)
        for (i,r,b),(qi,qr,q),count,start,topic in zip(blocks,asks,counts[n],starts[n],topics[n]):
            assert (i,r)==(qi,qr)
            cue,body=source_split(b,start);assert score(bag(re.sub(r"\(Section \d+\)", "", q)),bag(cue))>.75,(q,cue)
            if section==3 and i==2:body=body.split('Section 3:')[0]
            c=record(f'L{section}',i,r,q,[section+1],body,[15 if section==1 else 16 if section in (2,3) else 17],count*2 if count is not None else None,topicId=topic)
            if section==1:c['taskInstruction']=announcement_instruction
            if section==3 and i==1:c['sourceNote']='Actual whole-question max3 unless the response mentions work/employment/boxing/trainer/position/post; source full maximum4.'
            if section==3 and i==3:c['sharedAward']='L3-Q3-joint';c['reviewNote']='Both original questions preserved; no individual question tariff invented.'
            cards.append(c)
    assert len(cards)==44 and sum(c['publishedTotal'] or 0 for c in cards)+8==300
    assert len({c['id'] for c in cards})==44
    norm=lambda t:re.sub(r'[^\w]','',t.casefold())
    for c in cards:assert norm(c['publishedSourceBlock']) in norm('\n'.join(page(S,p) for p in c['schemePages'])),c['id']
    draft=dict(status='Source-only draft; not runtime cards or a completed sitting',sources=METADATA,
               independentPrintedAsks=44,prospectivePracticeTasks=43,writtenTasks=24,listeningPrintedAsks=20,
               sharedAwards=[dict(id='L3-Q3-joint',taskIds=['ru-2015-hl-l3-3-i','ru-2015-hl-l3-3-ii'],total=8,detailQuota=4,sourceText=joint_rule,schemePages=[16])],
               generalWrittenGuidance=squash(page(S,3)),comprehensionGuidance=squash(page(S,4).split('1.i.')[0]),
               summaryGuidance=squash(summary_source[:re.search(r'^\s*1\.\s*[A-Z]',summary_source,re.M).start()]),listeningGuidance=squash(source[:heads[0].start()]),tasks=cards)
    return docs, draft

from ru_review_2026_hl import base as common_base, as_points, save_reviewed
from ru_review_2017_hl import named_group, options

def base(*args, **kwargs):
    c=common_base(*args,**kwargs)
    for field in ('id','questionRef'):c[field]=c[field].replace('2026','2015')
    c['year']=2015;c['sourceMaterial']['title']=c['sourceMaterial']['title'].replace('2026','2015')
    return c

def source_card(record):
    pages=record.get('sourcePages') or ([2,3,4] if record['unit']=='C1' else [6,7,8,9] if record['unit']=='LA2' else [6,7,8] if record['unit']=='C2' else record['questionPages'])
    c=base(record['unit'],record['question'],record['publishedTotal'],pages,record['schemePages'],record['item'],record['roman'])
    c['review']['questionPages']=record['questionPages']
    return c

def reading(source):
    result=[]
    for r in source['tasks']:
        if r['unit']!='C1':continue
        key=(r['item'],r['roman']);body=r['publishedSourceBlock'];rejected='';partial='';four=''
        if 'assign no marks:' in body:body,rejected=body.split('assign no marks:',1)
        if 'assign one mark:' in body:body,partial=body.split('assign one mark:',1)
        if 'assign four marks:' in body:body,four=body.split('assign four marks:',1)
        full=between(body,'assign two marks:');answers=options(full);partials=options(partial);mapping={}
        independent=[]
        if key==(1,'ii'):
            assert len(answers)==4 and len(partials)==8
            mapping={i:partials[2*i:2*i+2] for i in range(4)}
        elif key==(1,'iii'):
            assert len(answers)==5 and len(partials)==3
            mapping={1:partials[:2],3:[partials[2]]}
        elif key==(2,'ii'):
            assert len(answers)==4 and len(partials)==1;mapping={2:partials}
        elif key==(2,'i'):
            assert len(answers)==5 and len(partials)==4
            mapping={1:[partials[-1]]};independent=partials[:-1]
        elif partials:independent=partials
        c=as_points(source_card(r),answers,r['publishedTotal']//2,mapping)
        for i,p in enumerate(independent,1):c['rubric']['groups'].append(named_group(f'independent-partial-{i}','Published partial detail',[p],marks=1))
        if four:
            assert key==(2,'i') and len(options(four))==2
            c['rubric']['groups'].append(named_group('admission-explanation','Complete admission explanation',options(four),marks=4))
            c['rubric']['allocationCap']={'maxMarks':4,'sourceText':'2 x 2 = 4','schemePages':[4]}
            c['rubric']['markingGuideNote']='The scheme explicitly awards four marks for either complete admission explanation shown here. Either reaches the whole-question maximum of four; other details cannot add further credit. The other listed full details retain their published two-mark award.'
            c['rubric']['taskRequirements']=['assign four marks: '+four]
        if rejected:c['rubric']['taskRequirements'].append('assign no marks: '+rejected)
        c['rubric']['taskRequirements'].insert(0,source['comprehensionGuidance'])
        c['review']['guidancePages']=[4]
        result.append(c)
    assert len(result)==13 and sum(c['totalMarks'] for c in result)==40
    return result


def summaries(source):
    result=[];general=source['summaryGuidance']
    incomplete=next(x for x in general.split('. ') if 'fails to answer all' in x)
    for r in source['tasks']:
        if r['unit']!='C2':continue
        main,secondary=r['publishedSourceBlock'].split('Secondary details:',1)
        primary=options(between(main,'Main points:'));secondary=options(secondary)
        c=as_points(source_card(r),primary+secondary,4,steps=[0,1,2],labels=['Main point']*len(primary)+['Secondary detail']*len(secondary))
        c['rubric']['criteria']=[{'id':'summary-skills','label':'Discretionary marks','maxMarks':2,'permittedMarks':[0,1,2],'guidance':[general],
            'limits':[{'id':'incomplete-response','maxMarks':1,'when':{'any':[{'flag':'incomplete-response','prompt':incomplete}]},'guidance':[incomplete]}]}]
        c['rubric']['taskRequirements']=[general]
        result.append(c)
    assert len(result)==4
    return result

def grammar_forms(docs):
    paper=docs['paper'][11].get_text();paper=paper[paper.index('Необычный'):].strip()
    solved=docs['scheme'][9].get_text();solved=solved[solved.index('Необычный'):]
    gaps=list(re.finditer(r'\(([^)]+)\)\s*[.\u2026]+\s*',paper));assert len(gaps)==15
    normal=lambda text:re.sub(r'[^\w]','',text.casefold())
    fixed=lambda text:''.join(re.escape(c)+r'[^\w]*' for c in normal(text))
    pattern='';cursor=0
    for gap in gaps:pattern+=fixed(paper[cursor:gap.start()])+r'(.+?)';cursor=gap.end()
    pattern+=fixed(paper[cursor:]);match=re.search(pattern,solved,re.S|re.I);assert match
    forms=[squash(x).strip(' .,') for x in match.groups()]
    assert forms==['школу','педагогов','говорят / говорили / сказали','удивились','необычного','решил/ решал','меня','урокe','наc','новую','выигралa','дисциплинe','трудностями','уроков','замечательных'],forms
    return [(gap[1],answer) for gap,answer in zip(gaps,forms)]


def language_and_matching(docs,source):
    result=[]
    for r in source['tasks']:
        if r['unit'] not in ('LA1','LA2','SD','GR'):continue
        body=r['publishedSourceBlock']
        if r['unit']=='LA1':
            rows=r['answerRows'];assert len(rows)==5
            c=as_points(source_card(r),[row[1]+' — '+row[0] for row in rows],5)
            c['rubric']['taskRequirements']=['Give two marks for each correct answer.']
        elif r['unit']=='LA2' and r['roman']=='i':
            entries=[squash(x) for x in re.split(r'\s[1-5]\.\s+',body)[1:]]
            pairs=[x.split(' ',1) for x in entries];assert len(pairs)==5
            answers=[x[1].split(' (')[0] for x in pairs]
            assert answers==['учиться','знать','прийти','получить','решaть'],answers
            c=as_points(source_card(r),answers,5)
            for group,pair in zip(c['rubric']['groups'],pairs):group['label']=pair[0];group['rows'][0]['marks']=1
            c['rubric']['groups'][2]['rows'].append({'id':'old-form','text':'придти','marks':1})
            c['rubric']['taskRequirements']=['Do not assign any marks where candidates translate the verb into English.','(allow old form придти, but not прийдти or прити)']
        elif r['unit']=='LA2':
            pool=between(body,'5 x 1 = 5','Do not accept')
            answers=[squash(x).rstrip('.') for x in pool.split(',')];assert len(answers)==7
            c=as_points(source_card(r),answers,5)
            for group in c['rubric']['groups']:group['rows'][0]['marks']=1
            c['rubric']['taskRequirements']=['Accept words in any form (case, number)','Do not accept'+between(body,'Do not accept')]
        elif r['unit']=='SD':
            rows=r['answerRows'];assert len(rows)==10
            c=as_points(source_card(r),[row[1]+' — '+row[0] for row in rows],10)
            c['rubric']['taskRequirements']=['2 marks for each correct answer']
        else:
            forms=grammar_forms(docs);c=as_points(source_card(r),[],15)
            c['rubric']['groups']=[named_group(f'form-{i+1}',supplied,[squash(x) for x in answer.split('/')]) for i,(supplied,answer) in enumerate(forms)]
            c['rubric']['taskRequirements']=['TWO marks per correct form 15 x 2 = 30','In this exercise'+between(body,'In this exercise','Необычный')]
        result.append(c)
    assert len(result)==5 and sum(c['totalMarks'] for c in result)==70
    return result

from ru_review_2026_hl import squash, between, mark_range
from ru_review_2017_hl import band
import re

def writing(docs, source, base):
    S=docs['scheme']; result=[]
    for unit,sp,table_page in [('SE',11,12),('GW',13,14)]:
        record=next(c for c in source['tasks'] if c['unit']==unit)
        text=S[sp-1].get_text()
        expression_heading='2. Expression (E):' if unit=='SE' else '2. Expression (E)'
        content=between(text,'1. Communication/content (C)',expression_heading)
        expression=between(text,expression_heading)
        lower_e=squash(re.search(r'If the content mark.*?indicate this\.',expression,re.S).group())
        lower_a=squash(re.search(r'If the expression is very fluent.*?indicate this\.',expression,re.S).group())
        soft=squash(re.search(r'Penalise students.*?\(– .*?\)\.',expression,re.S).group())
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
            assert [mark_range(price) for price,description in accuracy_source]==[[11,12],[9,10,11],[7,8]]
            accuracy=[]
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
        if not is_essay:
            limits[1].pop('bands')
            limits[1]['guidance'] += [price+' '+description for price,description in accuracy_source]
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
            coherence=[band(price,description) for price,description in tables[2].extract()[1:]]
            criteria.append({'id':'coherence','label':'Textual coherence (TC)','maxMarks':10,'permittedMarks':list(range(11)),'guidance':[],'bands':coherence})
        criteria.append({'id':'soft-sign-penalty','label':'Soft sign penalty','kind':'deduction','deductFrom':'expression','maxMarks':2,'permittedMarks':[0,1,2] if is_essay else [0,2],'guidance':[soft]})
        c['rubric']={'system':'language-writing','taskRequirements':[],'markingGuideNote':'','criteria':criteria}
        c['review']['guidancePages']=[3]
        if not is_essay:
            c['rubric']['markingGuideNote']='Source descriptor conflict: the Lower A prose gives the middle pair as 9/10, but its table prints 9–11, overlapping the 11–12 row. Both exact versions remain above. The agreed numeric range is 7–12; no descriptor is trimmed or reassigned, and no minimum mark is automatically awarded. The scheme’s category letters are not assigned to the printed writing prompts; no per-category mapping or marks are invented.'
        result.append(c)
    return result

def listening(docs,source):
    result=[];records={(r['unit'],r['item'],r['roman']):r for r in source['tasks'] if r['unit'] in ('L1','L2','L3','L4')}
    audio=next(r['source'] for r in json.loads((ROOT/'data/russianAudio.json').read_text()) if r['year']==2015)
    for key,r in records.items():
        if key==('L3',3,'ii'):continue
        body=r['publishedSourceBlock'];extra=[]
        if key==('L3',3,'i'):
            second=records[('L3',3,'ii')];joint=source['sharedAwards'][0]
            combined={**r,'roman':None,'publishedTotal':joint['total'],'question':r['question']+'\n\n'+second['question']}
            c=as_points(source_card(combined),options(body)+options(second['publishedSourceBlock']),joint['detailQuota'])
            c['questionRef']='2015 HL Section L3 Q3(i), (ii)'
            c['review']['printedQuestionParts']=[r['question'],second['question']]
            extra=[joint['sourceText']]
            c['rubric']['markingGuideNote']='Both printed questions are practised together because the scheme assigns a single eight-mark maximum for up to four details across them. Their original one-detail and three-detail wording remains above; no separate two/six mark split or independent subquestion cap is invented.'
        elif key==('L3',1,None):
            pool,rule=body.split('In order to obtain full marks',1);rule='In order to obtain full marks'+rule
            first,conditional=rule.split('Where none of these',1);conditional='Where none of these'+conditional
            c=as_points(source_card(r),options(pool),2)
            c['rubric']['allocationCap']={'maxMarks':4,'sourceText':squash(first),'schemePages':[16],
                'limits':[{'id':'missing-employment-reference','maxMarks':3,
                    'when':{'flag':'missing-employment-reference','prompt':'No detail refers to work, employment, boxing, a trainer, a position or a post.'},
                    'sourceText':conditional,'schemePages':[16]}]}
            c['rubric']['markingGuideNote']='Assess whether either actual answer makes one of the stated references. Russian answers are permitted by the listening guidance. The flag does not inspect English keywords or infer the condition from selected answer labels; it applies the published whole-answer cap without changing the two-mark detail tariff.'
        elif key==('L3',2,None):
            c=source_card(r);c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
            c['rubric']={'system':'language-writing','criteria':[{'id':f'detail-{i}','label':f'Distinct detail {i}','maxMarks':2,'permittedMarks':[0,1,2],'guidance':[]} for i in (1,2)],
                'taskRequirements':[body],
                'markingGuideNote':'The one-mark “world championship” wording is printed at question level. Both full and partial guidance remain visible; place each distinct answer once without inventing an exclusive association to a particular full-credit achievement.'}
        else:
            c=as_points(source_card(r),options(body),r['publishedTotal']//2)
        if r.get('taskInstruction'):c['questionText']=r['taskInstruction']+'\n\n'+c['questionText']
        c['rubric']['taskRequirements']=[source['listeningGuidance']]+c['rubric']['taskRequirements']+extra
        c['review']['guidancePages']=[15]
        c['topicId']=r['topicId'];c['additionalTopicIds']=['russian-1-0']
        c['sourceMaterial']['kind']='source-question';c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
        c['audioMaterial']=audio;result.append(c)
    assert len(result)==19 and sum(c['totalMarks'] for c in result)==80
    return result


def source_language_rules(cards,source):
    rule='Language of answer:'+between(source['generalWrittenGuidance'],'Language of answer:','Quality of English:')
    for c in cards:
        if c['section'] not in ('C1','C2','LA2','GR','SE','GW'):continue
        c['answerLanguageRule']={'otherLanguageMultiplier':0,'sourceText':squash(rule),'schemePages':[3]}
        if c['section'] in ('C1','C2'):c['rubric']['markingGuideNote']+=' Answer in English or Irish. Both languages are permitted by the original bilingual paper.'

def build():
    docs,source=source_records()
    cards=reading(source)+summaries(source)+language_and_matching(docs,source)+writing(docs,source,base)+listening(docs,source)
    source_language_rules(cards,source)
    assert len(cards)==43 and len({c['id'] for c in cards})==43
    assert sum(c['totalMarks'] for c in cards)==300
    assert sum(bool(c.get('answerLanguageRule')) for c in cards)==22
    for doc in docs.values():doc.close()
    from ru_summary_language_rules import attach_reviewed_summary_language_exceptions
    return attach_reviewed_summary_language_exceptions(cards)

if __name__=='__main__':save_reviewed(build())
