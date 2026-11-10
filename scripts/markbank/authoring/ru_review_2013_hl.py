"""Russian 2013 Higher source authoring; cultural allocation conflict remains open."""
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

METADATA = {'paper': {'pages': 16, 'sha256': '36835056dd0dbc40697f132b2a00484df1118ece3f364a8263992dc1a3c4dbc0'}, 'aural': {'pages': 8, 'sha256': '849f2d530c3a5d5cfc2667bff1f4b38be719483beab856f06d826b51b1640f02'}, 'scheme': {'pages': 20, 'sha256': 'b14c59425b38ee71743c5b59b119baad4071759692f069d143abc421b5ac4b6d'}}
FOOTER_BLOCK_BOUNDS = {3: (56.6376, 782.4505, 302.6097, 807.0616), 4: (56.6376, 782.4505, 302.6097, 807.0616), 5: (56.6376, 782.4505, 302.6097, 807.0616), 6: (84.0003, 785.9305, 305.7298, 810.5417), 7: (84.0003, 785.9305, 305.7298, 810.5417), 8: (84.0003, 785.9305, 305.7298, 810.5417), 9: (84.0003, 785.9305, 305.7298, 810.5417), 10: (84.0003, 785.9305, 305.7298, 810.5417), 11: (84.0003, 785.9305, 305.7298, 810.5417), 12: (84.0001, 785.9305, 308.13, 810.5417), 13: (84.0001, 785.9305, 308.13, 810.5417), 14: (84.0001, 785.9305, 308.13, 810.5417), 15: (84.0001, 785.9305, 308.13, 810.5417), 16: (84.0001, 785.9305, 308.13, 810.5417)}

def scheme_page(document,n):
    blocks=document[n-1].get_text('blocks',sort=False)
    footer=[b for b in blocks if b[4].strip()==str(n-2) and tuple(round(x,4) for x in b[:4])==FOOTER_BLOCK_BOUNDS[n]]
    assert len(footer)==1,(n,footer)
    return '\n'.join(b[4] for b in blocks if b is not footer[0])


def source_records():
    docs = {}
    for kind, relative in [('paper', 'papers/2013-hl-000-paper.pdf'),
                           ('aural', 'papers/2013-hl-A00-paper.pdf'),
                           ('scheme', 'schemes/2013-hl.pdf')]:
        path = ROOT / 'examiner-reports/russian' / relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == METADATA[kind]['sha256']
        docs[kind] = fitz.open(path)
    Q, A, S = docs['paper'], docs['aural'], docs['scheme']

    def page(doc, n, right=False):
        if doc is S:
            text=scheme_page(doc,n)
        else:
            text=doc[n-1].get_text(clip=fitz.Rect(295,30,580,793) if right else fitz.Rect(20,30,580,775),sort=False)
        return text.replace('\uf0b7','•').replace('\xa0',' ')

    def record(unit, item, roman, question, qp, body, sp, total, **extra):
        component = 'aural' if unit in ('L1', 'L2', 'L3', 'L4') else 'paper'
        norm = lambda t: re.sub(r'[^\w]', '', t.casefold())
        assert norm(question) in norm(' '.join(page(docs[component], p, right=True) for p in qp)), (unit, item, roman, question)
        return dict(id='ru-2013-hl-' + unit.lower() + (f'-{item}' if item is not None else '') + (f'-{roman}' if roman else ''),
                    unit=unit, item=item, roman=roman, question=question, questionPages=qp,
                    component=component, publishedSourceBlock=squash(body), schemePages=sp,
                    publishedTotal=total, **extra)

    cards = []
    source = '\n'.join(page(S, p) for p in (4, 5)).split('1.2. Language awareness')[0]
    blocks = numbered_blocks(source)
    asks = [(i,r,question_text(q),p) for p in (3,4) for i,r,q in numbered_blocks(page(Q,p,True))]
    assert len(blocks) == len(asks) == 10
    totals = [4,4,2,4,4,2,6,2,4,4]
    for (i,r,b),(qi,qr,q,p),total in zip(blocks,asks,totals):
        assert (i,r)==(qi,qr)
        price = re.search(r'(\d)\s*x\s*(\d)\s*=\s*(\d)',b)
        assert price and int(price.group(3))==total
        cue,body=b[:price.start()],b[price.start():]
        if (i,r)==(2,'i'):
            shared=next(block for item,roman,block in blocks if (item,roman)==(2,'ii'))
            shared_price=re.search(r'2\s*x\s*2\s*=\s*4',shared);assert shared_price
            body=shared[shared_price.start():]
        assert score(bag(q),bag(cue))>.75,(q,cue)
        cards.append(record('C1',i,r,q,[p],body,[4,5],total))
    assert sum(c['publishedTotal'] for c in cards)==36

    summary_source='\n'.join(page(S,p) for p in (6,7)).split('Language awareness')[0]
    blocks=numbered_blocks(summary_source)
    asks=[]
    for p in (6,7,8):
        text=page(Q,p,True)
        heads=list(re.finditer(r'^\s*Section\s+([1-4])\s*$',text,re.M))
        asks.extend((int(h.group(1)),question_text(text[h.end():heads[n+1].start() if n+1<len(heads) else len(text)]),p)
                    for n,h in enumerate(heads))
    assert len(blocks)==len(asks)==4
    for (i,r,b),(qi,q,p) in zip(blocks,asks):
        assert i==qi and r is None
        cue,body=source_split(b,'Main points')
        assert score(bag(q),bag(cue))>.75,(q,cue)
        cards.append(record('C2',i,None,q,[p],body,[6,7],10,
                            scoring=dict(detail=2,contentMaximum=8,discretionaryMaximum=2,partialDetail=1,incompleteDiscretionaryMaximum=1),
                            reviewNote='Summary2 requires at least one father and one mother detail; summary1 has a nested two-of collecting pool.'))

    q='Verbs: '+question_text(between(page(Q,5,True),'Verbs:','Cultural awareness:'))
    b='Verbs: '+between(page(S,5),'Verbs:','1.3.')
    cards.append(record('LA1',None,None,q,[5],b,[5],6,scoring=dict(correctInfinitives=6,perInfinitive=1)))
    q='Cultural awareness: '+question_text(between(page(Q,5,True),'Cultural awareness:'))
    b='1.3. '+between(page(S,5),'1.3.')
    cards.append(record('CA1',None,None,q,[5],b,[5],4,paperTotal=8,pending='Original paper says8; scheme explicitly1 per detail and2x2=4. Preserve contradiction, no silent doubling.'))
    q='Match the words, '+squash(between(page(Q,9,True),'Match the words,'));q=q[:q.index('entitled WORDS.')+len('entitled WORDS.')]
    b='Language awareness '+between(page(S,7),'Language awareness')
    rows=[[squash(v or '') for v in row] for row in S[6].find_tables().tables[0].extract()]
    assert len(rows)==5
    cards.append(record('LA2',None,None,q,[9],b,[7],10,answerRows=rows,scoring=dict(correctAnswers=5,perAnswer=2)))
    q='Read through the following questions '+squash(between(page(Q,10,True),'Read through the following questions'))
    q=q[:q.index('(20 marks)')+len('(20 marks)')]
    table=S[7].find_tables().tables[0].extract()
    rows=[[squash(v or '') for v in row] for row in table]
    assert [re.findall(r'\d+',r[0]) for r in rows]==[['9','1'],['7'],['10','8'],['6'],['3'],['5'],['4','2'],['2'],['1','9'],['8','10']],rows
    cards.append(record('SD',None,None,q,[10],page(S,8),[8],20,sourcePages=[10,11],answerRows=rows,scoring=dict(correctAnswers=10,perAnswer=2)))
    q='Read through the following text. '+squash(between(page(Q,12,True),'Read through the following text.'))
    q=q[:q.index('substitute words.')+len('substitute words.')]
    cards.append(record('GR',None,None,q,[12],page(S,9),[9],30,scoring=dict(correctForms=15,perForm=2),
                        reviewNote='Fifteen correct forms2 each; source half marks for capitalisation misuse, no marks for misspelling/transcription.'))
    q='Write a short essay '+squash(between(page(Q,13,True),'Write a short essay'))
    q=q[:q.index('essay title.')+len('essay title.')]
    cards.append(record('SE',None,None,q,[13],'\n'.join(page(S,p) for p in (10,11)),[10,11],30,fullQuestionPage=page(Q,13),
                        pending='Shared conditional Lower A range9–14; all seven topic choices preserved.'))
    assert page(Q,14,True).count('Write a piece')==2
    q='Write a piece '+question_text(page(Q,14,True).split('Write a piece',1)[1])
    cards.append(record('GW',None,None,q,[14],'\n'.join(page(S,p) for p in (12,13)),[12,13],40,
                        pending='Shared conditional Lower A range7–12; all three writing choices and their original category guides retained.'))
    assert len(cards)==21 and sum(c['publishedTotal'] for c in cards)==216

    source='\n'.join(page(S,p) for p in (14,15,16))
    heads=list(re.finditer(r'^\s*SECTION (IV|III|II|I)\b[^\n]*$',source,re.M))
    assert len(heads)==4
    counts=[[2,3,1,1,1,2],[3,4,3],[2,2,3,3],[2,2,2,1,1,2]]
    starts=[['Invested 7 million','Vladimir Yablokov','Heroism +','On a beach','In the garden','(Initiated by)'],
            ['Irish Film Festival','12.00-15.00','8-hour long'],
            ['Oral and written','Any amount','Results +','Site is visited'],
            ['Soviet/Russian','Father/ Vadim','Music was always','The Beatles','Architect /','Formed in 1969']]
    topics=[['russian-2-3','russian-0-7','russian-0-7','russian-0-8','russian-2-3','russian-2-3'],
            ['russian-2-3']*3,['russian-0-4']*4,
            ['russian-0-4','russian-0-1','russian-0-3','russian-0-5','russian-0-3','russian-0-4']]
    for n,h in enumerate(heads):
        section=n+1;b=source[h.end():heads[n+1].start() if n+1<len(heads) else len(source)]
        blocks=numbered_blocks(b)
        raw_asks=page(A,section+1,True)
        if section==4:raw_asks=A[4].get_text(clip=fitz.Rect(290,30,580,793)).replace('\xa0',' ')
        asks=[(i,r,question_text(q)) for i,r,q in numbered_blocks(raw_asks)]
        assert len(blocks)==len(asks)==len(counts[n])
        for (i,r,b),(qi,qr,q),count,start,topic in zip(blocks,asks,counts[n],starts[n],topics[n]):
            assert (i,r)==(qi,qr)
            cue,body=source_split(b,start);assert score(bag(q),bag(cue.replace('Andrey','Andrei').replace('web site','website')))>.75 or (section,i,r)==(2,1,None),(q,cue)
            sp=[14] if section==1 else [15] if section==2 else [15,16] if section==3 else [16]
            cards.append(record(f'L{section}',i,r,q,[section+1],body,sp,count*2,detailQuota=count,topicId=topic,
                                reviewNote='L2Q2 has blank published1-mark partial text; preserve missing-source note without inventing an answer.' if (section,i)==(2,2) else ''))
    assert len(cards)==40 and sum(c['publishedTotal'] for c in cards)==296
    assert len({c['id'] for c in cards})==40
    norm=lambda t:re.sub(r'[^\w]','',t.casefold())
    for c in cards:
        assert norm(c['publishedSourceBlock']) in norm('\n'.join(page(S,p) for p in c['schemePages'])),c['id']
    draft=dict(status='Source-only draft; not runtime cards or a completed sitting',sources=METADATA,
               independentTasks=40,writtenTasks=21,listeningTasks=19,printedExamTotal=300,sourceLeafTotal=296,aggregateDiscrepancy="CA1 paper8 versus scheme4; C1Q3ii re-review resolves prior tariff-conflict inference",generalWrittenGuidance=squash(page(S,3)),
               comprehensionGuidance=squash(page(S,4).split('1.i.')[0]),
               summaryGuidance=squash(summary_source[:re.search(r'^\s*1\.\s*[A-Z]',summary_source,re.M).start()]),
               listeningGuidance=squash(source[:heads[0].start()]),tasks=cards)
    return docs,draft

from ru_review_2026_hl import base as common_base,as_points,save_reviewed,mark_range
from ru_review_2017_hl import options,named_group,band

def base(*args,**kwargs):
    c=common_base(*args,**kwargs)
    for key in ('id','questionRef'):c[key]=c[key].replace('2026','2013')
    c['year']=2013;c['sourceMaterial']['title']=c['sourceMaterial']['title'].replace('2026','2013');return c

def source_card(r):
    pages=r.get('sourcePages') or ([2,3,4] if r['unit']=='C1' else [6,7,8,9] if r['unit']=='LA2' else [6,7,8] if r['unit']=='C2' else r['questionPages'])
    c=base(r['unit'],r['question'],r['publishedTotal'],pages,r['schemePages'],r['item'],r['roman']);c['review']['questionPages']=r['questionPages'];return c

def reading(source):
    result=[]
    for r in source['tasks']:
        if r['unit']!='C1':continue
        body=r['publishedSourceBlock'];key=(r['item'],r['roman']);count=r['publishedTotal']//2
        if 'assign one mark:' in body:
            # Pool-level partial wording does not identify a unique full-answer
            # association. Independent placements preserve the published scale.
            c=source_card(r);c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
            c['rubric']={'system':'language-writing','criteria':[{'id':f'detail-{n}','label':f'Distinct detail {n}','maxMarks':2,'permittedMarks':[0,1,2],'guidance':[body]} for n in range(1,count+1)],
                         'taskRequirements':[],
                         'markingGuideNote':'Assess each different actual detail once against the complete printed full and partial pools. Do not count a paraphrase twice or infer an exclusive full/partial pairing merely from list position.'}
        else:c=as_points(source_card(r),options(between(body,'assign two marks:')),count)
        c['rubric']['taskRequirements']=[source['comprehensionGuidance'],body]
        if key==(3,'ii'):
            c['rubric']['markingGuideNote']+=' The question requires details about TWO PLACES. Both originals give six marks and the scheme assigns two per full detail; three distinct response slots preserve this allocation. Cover both places; the source supplies no per-place split or numeric incomplete-place cap.'
        if key in ((2,'i'),(2,'ii')):
            c['rubric']['markingGuideNote']+=' Both questions accept the same complete published pool. Apply the original repeated-information rule across the two responses: reward the best answer once, without claiming the same detail again in the other question.'
        c['review']['guidancePages']=[4];result.append(c)
    assert len(result)==10 and sum(c['totalMarks'] for c in result)==36
    return result

def summaries(source):
    result=[];general=source['summaryGuidance'];incomplete=general[general.index('If a candidate fails'):]
    for r in source['tasks']:
        if r['unit']!='C2':continue
        body=r['publishedSourceBlock'];special=''
        if 'Do not award full marks' in body:body,special=body.split('Do not award full marks',1);special='Do not award full marks'+special
        primary,secondary=body.split('Secondary details:',1)
        primary=options(primary.split(':',1)[1]);secondary=options(secondary)
        c=as_points(source_card(r),primary+secondary,4,steps=[0,1,2],labels=['Main point']*len(primary)+['Secondary detail']*len(secondary))
        if r['item']==1:
            group=next(g for g in c['rubric']['groups'] if g['rows'][0]['text'].startswith('TWO OF:'))
            collection=group['rows'][0]['text'];assert collection.endswith('coins, money, films')
            entries=collection.split('TWO OF:',1)[1].strip().rsplit(', ',3);assert len(entries)==4
            group['label']='Examples of collections — at most two distinct examples';group['answerCount']=2
            group['rows']=[{'id':f'example-{n}','text':text,'marks':2,'steps':[0,1,2]} for n,text in enumerate(entries,1)]
            c['rubric']['allocationCap']={'maxMarks':8,'answerCount':4,'sourceText':'Award 2 marks for each of 4 details (up to 8 marks)','schemePages':[6]}
            c['rubric']['markingGuideNote']='Choose up to two collection examples within the four-detail content maximum. In the stamps row, the published postage wording earns one mark and marks earns zero; do not claim postage and stamps separately. Other intelligible partial details follow the general one-mark rule.'
        elif r['item']==2:
            c['rubric']['groups']=[{'id':f'detail-{n}','label':f'Distinct detail {n}','rows':[],
                'criteria':[{'id':f'detail-{n}','label':f'Distinct detail {n}','maxMarks':2,'permittedMarks':[0,1,2],'guidance':[body,special]}]} for n in (1,2,3,4)]
            c['rubric']['markingGuideNote']='Include at least one detail about the mother AND one about the father, as expressly required. Assess four distinct actual details, with the complete published restrictions above. The source does not give separate numeric allocations to the parents. Apply the incomplete-response discretionary limit if a required section is omitted; do not infer a further content cap.'
        c['rubric']['criteria']=[{'id':'summary-skills','label':'Discretionary marks','maxMarks':2,'permittedMarks':[0,1,2],'guidance':[general],
            'limits':[{'id':'incomplete-response','maxMarks':1,'when':{'any':[{'flag':'incomplete-response','prompt':incomplete}]},'guidance':[incomplete]}]}]
        c['rubric']['taskRequirements']=[general]+([special] if special else [])
        result.append(c)
    assert len(result)==4
    return result

def language_and_matching(docs,source):
    result=[]
    for r in source['tasks']:
        unit=r['unit'];body=r['publishedSourceBlock']
        if unit not in ('LA1','LA2','SD'):continue
        if unit=='LA1':
            words=body.rsplit('aspect.',1)[1].split();assert len(words)==12
            pairs=list(zip(words[::2],words[1::2]));c=as_points(source_card(r),[a for q,a in pairs],6)
            for g,(q,a) in zip(c['rubric']['groups'],pairs):g['label']=q;g['rows'][0]['marks']=1
            c['rubric']['taskRequirements']=[body.split(pairs[0][0],1)[0]]
        elif unit=='LA2':
            rows=r['answerRows'];c=as_points(source_card(r),[answer for answer,word in rows],5)
            for g,(answer,word) in zip(c['rubric']['groups'],rows):g['label']=word
            c['rubric']['taskRequirements']=['Give two marks for each correct answer.']
            c['rubric']['markingGuideNote']='The original scheme lists the number and the Irish, English and Russian word-class names. Any listed form identifies the same answer; do not award multiple marks for equivalent labels.'
        else:
            rows=r['answerRows'];c=as_points(source_card(r),[numbers for numbers,text in rows],10)
            for g,(numbers,text) in zip(c['rubric']['groups'],rows):
                g['label']=text;full= re.sub(r'\([^)]+\)','',numbers);partial=re.findall(r'\((\d+)\)',numbers)
                g['rows']=[{'id':f'full-{n}','text':number,'marks':2} for n,number in enumerate(re.findall(r'\d+',full),1)]
                g['rows'] += [{'id':f'partial-{n}','text':number,'marks':1} for n,number in enumerate(partial,1)]
            c['rubric']['taskRequirements']=['2 marks for each correct answer and 1 mark for answer supplied in brackets','10 x 2 = 20']
            c['rubric']['markingGuideNote']='Choose one number for each printed response. Every full-credit alternative and bracketed one-mark response remains in its original row. No extra one-use-only constraint across rows is supplied.'
        result.append(c)
    assert len(result)==3
    return result

def grammar_forms(docs):
    paper=docs['paper'][11].get_text();paper=paper[paper.index('РАНЬШЕ И СЕЙЧАС'):]
    solved=scheme_page(docs['scheme'],9);solved=solved[solved.index('РАНЬШЕ И СЕЙЧАС'):]
    gaps=list(re.finditer(r'\(([^)]+)\)\s*[.\u2026]+\s*',paper));assert len(gaps)==15
    fixed=lambda words:r'[^\w]*'.join(re.escape(word) for word in words)
    result=[]
    for n,gap in enumerate(gaps):
        before=paper[gaps[n-1].end() if n else 0:gap.start()];after=paper[gap.end():gaps[n+1].start() if n+1<len(gaps) else len(paper)]
        left=re.findall(r'\w+',before)[-4:];right=re.findall(r'\w+',after)[:4]
        pattern=fixed(left)+r'[^\w]+(\w+)'+(r'[^\w]+'+fixed(right) if right else r'[^\w]*$')
        matches=re.findall(pattern,solved,re.I);assert len(matches)==1,(n,left,right,matches)
        result.append((gap[1],matches[0]))
    assert [a for q,a in result]==['Меня','родителями','Соединённых','жили','России','младшей','учусь','начальной','программистом','преподаёт','нас','ведёт','нам','этим','родственников']
    return result

def grammar(docs,source):
    r=next(r for r in source['tasks'] if r['unit']=='GR');pairs=grammar_forms(docs)
    c=as_points(source_card(r),[a for q,a in pairs],15,steps=[0,1,2])
    for n,(g,(q,a)) in enumerate(zip(c['rubric']['groups'],pairs),1):g['label']=f'{n}. {q}'
    c['rubric']['taskRequirements']=[r['publishedSourceBlock'].split('РАНЬШЕ И СЕЙЧАС')[0]]
    c['rubric']['markingGuideNote']='The one-mark placement is only the printed half-credit rule for inappropriate upper/lower case. Misspelt or incorrectly transcribed forms receive zero. The repeated мы prompts are separate original gaps with different exact answers, нас and нам.'
    return [c]

def writing(docs, source, base):
    S=docs['scheme']; result=[]
    for unit,sp,table_page in [('SE',10,11),('GW',12,13)]:
        record=next(c for c in source['tasks'] if c['unit']==unit)
        text=S[sp-1].get_text(sort=True)
        expression_heading='2. Expression (E):' if unit=='SE' else '2. Expression (E)'
        content=between(text,'1. Communication/content (C)',expression_heading)
        expression=between(text,expression_heading)
        lower_e=squash(re.search(r'If the content mark.*?indicate this\.',expression,re.S).group())
        lower_a=squash(re.search(r'If the expression is very fluent.*?indicate this\.',expression,re.S).group())
        soft=squash(re.search(r'Penalise students.*?\(– .*?\)\.',expression,re.S).group())
        normal=[];lower=[];accuracy=[];content_bands=[]
        tables=S[table_page-1].find_tables().tables
        if unit=='SE':
            for content_price,content_description,prices,description in tables[0].extract()[1:]:
                content_bands.append(band(content_price,content_description))
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
            assert all(f'{n}.' in choices for n in range(1,8))
        c=base(unit,question,record['publishedTotal'],record['questionPages'],record['schemePages'])
        c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
        criteria=[{'id':'content','label':'Communication/content (C)','maxMarks':10 if is_essay else 15,'permittedMarks':list(range(11 if is_essay else 16)),'guidance':[squash(content)]}]
        if is_essay:criteria[0]['bands']=content_bands
        if is_essay:
            title=squash(re.search(r'Candidates are required.*?overall\s+content score\.',content,re.S).group())
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
            c['rubric']['markingGuideNote']='Source descriptor conflict: the Lower A prose gives the middle pair as 9/10, but its table prints 9–11, overlapping the 11–12 row. Both exact versions remain above. The agreed numeric range is 7–12; no descriptor is trimmed or reassigned, and no minimum mark is automatically awarded. The choice-specific category letters and requirements are retained in the original guide; no equal per-category prices are invented.'
        if not is_essay:
            guide=scheme_page(S,12)
            instructions=guide[guide.index('1. Write an entry'):guide.index('Communication + content')]
            c['rubric']['taskRequirements']=[squash(instructions),squash(re.search(r'If a candidate answers.*?one\(s\)\.',guide,re.S).group())]
        result.append(c)
    return result

def listening(docs,source):
    result=[];audio=next(r['source'] for r in json.loads((ROOT/'data/russianAudio.json').read_text()) if r['year']==2013)
    for r in source['tasks']:
        if r['unit'] not in ('L1','L2','L3','L4'):continue
        key=(r['unit'],r['item'],r['roman']);body=r['publishedSourceBlock'];pool=body;extra=[];partial=''
        if 'Award one mark:' in pool:pool,partial=pool.split('Award one mark:',1)
        if pool.endswith('1 mark:'):
            assert key==('L2',2,None);pool=pool[:-len('1 mark:')].strip();extra=['1 mark:']
        answers=options(pool);c=as_points(source_card(r),answers,r['detailQuota'],{0:[partial.strip()]} if partial else {})
        if key==('L3',1,None):
            assert len(answers)==5
            c['rubric']['groups']=c['rubric']['groups'][:3]+[
                named_group('translator-requirement','Translators — one named requirement',['grammatical correctness','literacy','wide vocabulary']),
                named_group('interpreter-requirement','Interpreters — one named requirement',['clear articulation','etiquette','clothes'])]
            c['rubric']['taskRequirements']=[answers[3],answers[4]]
            c['rubric']['markingGuideNote']='Each printed ONE OF pool contributes one detail at most. Both share the question’s two-detail maximum with the other accepted statements.'
        elif key==('L3',4,None):
            countries=next(x for x in answers if x.startswith('ANY TWO OF:'))
            c['rubric']['groups']=[g for g in c['rubric']['groups'] if not g['rows'][0]['text'].startswith('ANY TWO OF:')]
            c['rubric']['groups'] += [{'id':f'country-{n}','label':f'Distinct country {n} from the printed country span','rows':[],
                'criteria':[{'id':f'country-{n}','label':f'Distinct country {n}','maxMarks':2,'permittedMarks':[0,2],'guidance':[countries]}]} for n in (1,2)]
            c['rubric']['markingGuideNote']='Use at most two different country details within the original three-detail question maximum. Each country belongs in one of the two reserved country slots and cannot be claimed twice. The complete printed country span, including “and other countries”, remains visible; no extra country slot or invented partial tariff is added.'
        elif key==('L2',2,None):
            c['rubric']['markingGuideNote']='The scheme prints a bare “1 mark:” line after this answer pool without supplying a partial answer. Every complete published detail remains available at two marks; no missing one-mark answer is invented.'
        c['rubric']['taskRequirements']=[source['listeningGuidance']]+c['rubric']['taskRequirements']+extra
        if partial:c['rubric']['taskRequirements'].append('Award one mark:'+partial)
        c['review']['guidancePages']=[14];c['topicId']=r['topicId'];c['additionalTopicIds']=['russian-1-0']
        c['sourceMaterial']['kind']='source-question';c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
        c['audioMaterial']=audio;result.append(c)
    assert len(result)==19 and sum(c['totalMarks'] for c in result)==80
    return result

def source_language_rules(cards,source):
    rule='Language of answer:'+between(source['generalWrittenGuidance'],'Language of answer:','Decoding the marking scheme:')
    for c in cards:
        if c['section'] not in ('C1','C2','LA1','GR','SE','GW'):continue
        c['answerLanguageRule']={'otherLanguageMultiplier':0,'sourceText':squash(rule),'schemePages':[3]}
        if c['section'] in ('C1','C2'):c['rubric']['markingGuideNote']+=' Answer in English or Irish. Both languages are permitted by the original bilingual paper.'

def build():
    docs,source=source_records()
    cards=reading(source)+summaries(source)+language_and_matching(docs,source)+grammar(docs,source)+writing(docs,source,base)+listening(docs,source)
    source_language_rules(cards,source)
    assert len(cards)==39 and len({c['id'] for c in cards})==39
    assert sum(c['totalMarks'] for c in cards)==292
    assert sum(bool(c.get('answerLanguageRule')) for c in cards)==18
    assert not any(c['id']=='ru-2013-hl-ca1' for c in cards)
    for doc in docs.values():doc.close()
    return cards

if __name__=='__main__':save_reviewed(build())
