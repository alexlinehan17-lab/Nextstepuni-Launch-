"""Russian 2011 Higher source authoring; unsupported numeric cases remain open."""
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

METADATA = {'paper': {'pages': 16, 'sha256': '282f90bd9437359bb15917f4254fbd1e2c79b07912d7211abc7272c0be0429d9'}, 'aural': {'pages': 8, 'sha256': 'd914563a421a1aeb5dcadcd0a70e5d0e0c4c2c538075452df12be1445645ee1d'}, 'scheme': {'pages': 24, 'sha256': '0e0ba4dc7e9bffee7675b899d8380ed4102c50d5c0c84ffb7decf39362e5979e'}}

def source_records():
    docs = {}
    for kind, relative in [('paper', 'papers/2011-hl-000-paper.pdf'),
                           ('aural', 'papers/2011-hl-A00-paper.pdf'),
                           ('scheme', 'schemes/2011-hl.pdf')]:
        path = ROOT / 'examiner-reports/russian' / relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == METADATA[kind]['sha256']
        docs[kind] = fitz.open(path)
    Q, A, S = docs['paper'], docs['aural'], docs['scheme']

    def page(doc, n, right=False):
        # The scheme has content to y771 and a footer beginning at y771: remove
        # the actual footer line instead of clipping away low printed guidance.
        rect = fitz.Rect(295, 30, 580, 793) if right else fitz.Rect(20, 30, 580, 793)
        if doc is Q and n in (7,10):
            # These two original pages repeat boundary glyphs at the same physical
            # location across text spans. Retain one identical glyph at that location;
            # distinct consecutive letters remain distinct. Originals are untouched.
            chars=[]
            for block in doc[n-1].get_text('rawdict',clip=rect)['blocks']:
                for line in block.get('lines',[]):
                    for span in line.get('spans',[]):
                        for char in span['chars']:
                            if not any(char['c']==old['c'] and max(abs(a-b) for a,b in zip(char['bbox'],old['bbox']))<.2 for old in chars):
                                chars.append(char)
            lines=[]
            for char in sorted(chars,key=lambda c:(c['origin'][1],c['origin'][0])):
                match=next((line for y,line in lines if abs(y-char['origin'][1])<.2),None)
                if match is None:lines.append((char['origin'][1],[char]))
                else:match.append(char)
            text='\n'.join(''.join(c['c'] for c in sorted(line,key=lambda c:c['origin'][0])) for _,line in lines)
        else:text = doc[n-1].get_text(clip=rect, sort=False)
        text=text.replace('\uf0b7', '•').replace('\xa0', ' ')
        return re.sub(r'^[^\n]*Lch\s+\d+\s+de\s+\d+[^\n]*Page\s+\d+\s+of\s+\d+[^\n]*\n?', '', text, flags=re.M)

    norm = lambda t: re.sub(r'[^\w]', '', t.casefold())

    def numbered_blocks(text):
        heads=list(re.finditer(r'^\s*(\d)\.\s*(?:(iv|i{1,3})\.?\s*)?(?=[A-Z“])',text,re.M))
        return [(int(h.group(1)),h.group(2),text[h.end():heads[n+1].start() if n+1<len(heads) else len(text)]) for n,h in enumerate(heads)]

    def record(unit, item, roman, question, qp, body, sp, total, **extra):
        component = 'aural' if unit in ('L1', 'L2', 'L3', 'L4') else 'paper'
        assert any(norm(question) in norm(' '.join(page(docs[component], p, right=right) for p in qp))
                   for right in (False, True)), (unit, item, roman, question)
        return dict(id='ru-2011-hl-' + unit.lower() + (f'-{item}' if item is not None else '') + (f'-{roman}' if roman else ''),
                    unit=unit, item=item, roman=roman, question=question, questionPages=qp,
                    component=component, publishedSourceBlock=squash(body), schemePages=sp,
                    publishedTotal=total, **extra)

    cards = []
    source='\n'.join(page(S,p) for p in (5,6))
    blocks=numbered_blocks(source)
    asks=[(i,r,question_text(q),p) for p in (3,4) for i,r,q in numbered_blocks(page(Q,p,True).split('Language awareness')[0])]
    assert len(blocks)==len(asks)==8
    totals=[4,6,6,6,4,6,2,2]
    for (i,r,b),(qi,qr,q,p),total in zip(blocks,asks,totals):
        assert (i,r)==(qi,qr)
        price=re.search(r'(\d)\s*x\s*2\s*=\s*(\d)',b)
        assert price and int(price.group(2))==total
        cue,body=b[:price.start()],b[price.start():]
        assert score(bag(q),bag(cue))>.75,(q,cue)
        cards.append(record('C1',i,r,q,[p],body,[5,6],total))
    assert sum(c['publishedTotal'] for c in cards)==36

    summary_source='\n'.join(page(S,p) for p in (8,9))
    heads=list(re.finditer(r'^\s*Section ([1-4])\s*$',summary_source,re.M))
    assert len(heads)==4
    for n,h in enumerate(heads):
        i=n+1;p=[6,7,8,9][n]
        raw=page(Q,p,True)
        q=question_text(raw.split(f'Section {i}',1)[1])
        b=summary_source[h.end():heads[n+1].start() if n+1<len(heads) else len(summary_source)]
        cue,body=source_split(b,'main points:' if i==1 else 'Main points:')
        assert score(bag(q),bag(cue))>.75,(q,cue)
        cards.append(record('C2',i,None,q,[p],body,[8,9],None,sharedAward='C2-summary-collective45',
                            pending='Collective45 is printed; five details2 plus1 or2 discretionary does not assign11/12/11/11. Exact general rule retained; numeric allocation unresolved.'))

    q='Verbs: '+question_text(between(page(Q,4,True),'Verbs:'))
    b='Verbs: '+between(page(S,7),'Verbs:','Cultural awareness:')
    cards.append(record('LA1',None,None,q,[4],b,[7],6,scoring=dict(correctInfinitives=6,perInfinitive=1),
                        reviewNote='Accepted нравиться; no-credit example нравится. Source invalid forms поити/нравится/забывать retained exactly.'))
    q='Cultural awareness: '+question_text(between(page(Q,5,True),'Cultural awareness:'))
    b='Cultural awareness: '+between(page(S,7),'Cultural awareness:')
    cards.append(record('CA1',None,None,q,[5],b,[7],8,scoring=dict(topics=2,detailsPerTopic=2,perDetail=2),reviewNote='Both/either language accepted.'))
    q='Match the words, '+squash(between(page(Q,9,True),'Match the words,','FOCAIL'))
    rows=[[squash(v or '') for v in row] for row in S[9].find_tables().tables[0].extract()]
    assert [r[0] for r in rows]==['4','2','5','1','3']
    cards.append(record('LA2',None,None,q,[9],page(S,10),[10],5,answerRows=rows,scoring=dict(correctAnswers=5,perAnswer=1)))
    q='Read through '+squash(between(page(Q,10,True),'Read through'))
    q=q[:q.index('(20 marks)')+len('(20 marks)')]
    rows=[[squash(v or '') for v in row] for row in S[10].find_tables().tables[0].extract()]
    assert len(rows)==10
    assert [re.search(r'\d+',r[0]).group() for r in rows]==['6','4','7','8','1','2','10','3','9','5']
    cards.append(record('SD',None,None,q,[10],page(S,11),[11],20,sourcePages=[10,11],answerRows=rows,scoring=dict(correctAnswers=10,perAnswer=2),reviewNote='Published one-mark row alternatives retained; no inferred unique-use rule.'))
    q='Read through the following TWO texts. '+squash(between(page(Q,12,True),'Read through the following TWO texts.'))
    q=q[:q.index('substitute words.')+len('substitute words.')]
    cards.append(record('GR',None,None,q,[12],page(S,12),[12],30,scoring=dict(correctForms=15,perForm=2),reviewNote='Two texts, one30-mark task; incorrect capitalization earns0, not later-year half marks.'))
    q='Write a short essay '+squash(between(page(Q,13,True),'Write a short essay'))
    q=q[:q.index('(30 marks)')+len('(30 marks)')]
    cards.append(record('SE',None,None,q,[13],'\n'.join(page(S,p) for p in (13,14)),[13,14],30,fullQuestionPage=page(Q,13),pending='Shared conditional Lower A range9–14; all seven topics retained.'))
    q='Write a piece '+question_text(page(Q,14,True).split('Write a piece',1)[1])
    cards.append(record('GW',None,None,q,[14],'\n'.join(page(S,p) for p in (15,16,17)),[15,16,17],40,
                        pending='Shared conditional Lower A range7–12 with overlapping9–11/11–12. Adapted discussion details earn2; directly copied comprehension text0. Four full choices retained.'))
    assert len(cards)==19 and sum(c['publishedTotal'] or 0 for c in cards)==175

    source='\n'.join(page(S,p) for p in range(18,23))
    heads=list(re.finditer(r'^\s*SECTION (IV|III|II|I)\b[^\n]*$',source,re.M))
    assert len(heads)==4
    counts=[[2,2,3,1,2],[2,2,2,2,2],[3,2,1,4],[2,1,2,2,2,1]]
    topics=[['russian-0-7','russian-0-7','russian-0-4','russian-0-7','russian-0-7'],
            ['russian-2-3']*5,['russian-0-9']*4,
            ['russian-0-1','russian-0-4','russian-0-5','russian-0-4','russian-0-4','russian-0-6']]
    for n,h in enumerate(heads):
        section=n+1;b=source[h.end():heads[n+1].start() if n+1<len(heads) else len(source)]
        blocks=numbered_blocks(b)
        asks=[(i,r,question_text(q)) for i,r,q in numbered_blocks(page(A,section+1,True))]
        assert len(blocks)==len(asks)==len(counts[n]),(section,len(blocks),len(asks))
        for (i,r,b),(qi,qr,q),count,topic in zip(blocks,asks,counts[n],topics[n]):
            assert (i,r)==(qi,qr)
            m=re.search(r'(?:ONE|TWO|THREE|FOUR) OF:',b);assert m
            cue,body=b[:m.start()],b[m.start():]
            assert score(bag(q),bag(cue))>.7,(q,cue)
            sp=[18,19] if section==1 else [20] if section==2 else [21] if section==3 else [22]
            cards.append(record(f'L{section}',i,r,q,[section+1],body,sp,count*2,detailQuota=count,topicId=topic,
                                reviewNote='Date/date/place components retained under explicit two-detail quota; no inferred one-date plus one-place restriction.' if (section,i,r)==(4,1,'i') else ''))
    assert len(cards)==39 and sum(c['publishedTotal'] or 0 for c in cards)+45==300
    assert len({c['id'] for c in cards})==39
    for c in cards:
        assert norm(c['publishedSourceBlock']) in norm('\n'.join(page(S,p) for p in c['schemePages'])),c['id']
    draft=dict(status='Source-only draft; not runtime cards or a completed sitting',sources=METADATA,
               independentTasks=39,writtenTasks=19,listeningTasks=20,printedExamTotal=300,pricedTasksTotal=255,
               sharedAwards=[dict(id='C2-summary-collective45',publishedTotal=45,tasks=[f'ru-2011-hl-c2-{i}' for i in range(1,5)],schemePages=[8,9],
                                 pending='Five details2 plus1 or2 discretion and collective45 do not establish separate task maxima. No11/12/11/11 allocation.')],
               aggregateDiscrepancy='Paper reading40 versus scheme36; paper summary40 versus scheme45. Preserve original section and leaf totals.',
               generalWrittenGuidance=squash('\n'.join(page(S,p) for p in (3,4))),
               comprehensionGuidance=squash(page(S,5).split('1. i')[0]),
               summaryGuidance=squash(summary_source[:re.search(r'^\s*Section 1',summary_source,re.M).start()]),
               listeningGuidance=squash(source[:heads[0].start()]),tasks=cards)
    return docs,draft


from ru_review_2026_hl import base as common_base,as_points,save_reviewed,mark_range
from ru_review_2017_hl import options,named_group,band

def base(*args,**kwargs):
    c=common_base(*args,**kwargs)
    for key in ('id','questionRef'):c[key]=c[key].replace('2026','2011')
    c['year']=2011;c['sourceMaterial']['title']=c['sourceMaterial']['title'].replace('2026','2011');return c

def source_card(r):
    pages=r.get('sourcePages') or ([2,3,4] if r['unit']=='C1' else [6,7,8,9] if r['unit'] in ('C2','LA2') else r['questionPages'])
    c=base(r['unit'],r['question'],r['publishedTotal'],pages,r['schemePages'],r['item'],r['roman']);c['review']['questionPages']=r['questionPages'];return c

def reading(source):
    result=[]
    for r in source['tasks']:
        if r['unit']!='C1':continue
        key=(r['item'],r['roman']);body=r['publishedSourceBlock'];count=r['publishedTotal']//2
        c=source_card(r)
        if key==(1,'i'):
            c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
            c['rubric']={'system':'language-points','count':1,
                'alternativeSets':[{'id':'meeting-response','label':'Full statement or one detail about each person','sourceText':body,'schemePages':[5]}],
                'groups':[
                    {'id':'both-walking','label':'Both walking — complete published answer','alternativeSet':'meeting-response','answerCount':1,
                     'rows':[{'id':'full','text':'Misha and Lena/they are both (out) walking','marks':4}]},
                    {'id':'one-each','label':'One distinct detail about each person','alternativeSet':'meeting-response','rows':[],
                     'criteria':[{'id':person,'label':f'Detail about {person.title()}','maxMarks':2,'permittedMarks':[0,2],'guidance':[body]} for person in ('misha','lena')]}],
                'taskRequirements':[source['comprehensionGuidance'],body],
                'markingGuideNote':'Choose the full four-mark statement or one published two-mark detail about each person. The individual route must include BOTH Misha and Lena. No partial mark is specified for this task, and the routes cannot be combined.'}
        elif key in [(1,'ii'),(3,'i')]:
            c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
            c['rubric']={'system':'language-points','count':count,'groups':[
                {'id':f'detail-{n}','label':f'Distinct detail {n}','rows':[],
                 'criteria':[{'id':f'detail-{n}','label':f'Distinct detail {n}','maxMarks':2,'permittedMarks':[0,1,2],'guidance':[body]}]} for n in range(1,count+1)],
                'taskRequirements':[source['comprehensionGuidance'],body],
                'markingGuideNote':'Assess distinct actual details against the complete full, named partial and zero-credit pool. One mark requires a printed partial; no general partial tariff or unique full/partial pairing is inferred.'}
        else:
            pool=body.split('assign two marks:',1)[1].split('no marks:',1)[0].strip()
            c=as_points(c,options(pool),count)
            c['rubric']['taskRequirements']=[source['comprehensionGuidance'],body]
            if key==(2,'ii'):
                first=c['rubric']['groups'][0];assert first['rows'][0]['text']=='fantasy/science fiction [if not assigned in 2.i.]'
                first['rows']=[];first.pop('answerCount',None)
                first['criteria']=[{'id':'fantasy-credit','label':'Fantasy/science-fiction detail','maxMarks':2,'permittedMarks':[0,2],
                    'guidance':['fantasy/science fiction [if not assigned in 2.i.]'],
                    'limits':[{'id':'already-credited','maxMarks':0,'when':{'any':[{'flag':'fantasy-already-credited','prompt':'This fantasy/science-fiction detail already earned marks in Question 2(i).'}]},'guidance':['fantasy/science fiction [if not assigned in 2.i.]']}]}]
                c['rubric']['markingGuideNote']='The fantasy/science-fiction detail earns credit here only if it was not already credited in Question 2(i). Use the explicit condition for that repeated detail; the remaining distinct accepted facts keep their own published credit.'
        c['rubric']['markingGuideNote']+=' Source heading discrepancy: the paper gives 40 reading marks, while the eight scheme reading allocations total 36; language and cultural awareness add 14 to the scheme’s 50. The original task allocations are retained.'
        c['review']['guidancePages']=[5];result.append(c)
    assert len(result)==8 and sum(c['totalMarks'] for c in result)==36
    return result


def summaries(docs,source):
    records=[r for r in source['tasks'] if r['unit']=='C2'];assert len(records)==4
    general=source['summaryGuidance'];incomplete=general[general.index('If a candidate fails'):]
    instruction='Write a summary in English of the content of each Section as instructed.'
    norm=lambda t:re.sub(r'[^\w]','',t.casefold())
    assert norm(instruction) in norm(docs['paper'][5].get_text())
    question=instruction+'\n\n'+'\n\n'.join(f'Section {r["item"]}\n{r["question"]}' for r in records)
    c=base('C2',question,45,[6,7,8,9],[8,9]);c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
    c['questionRef']='2011 HL Section C2 — Summary Sections 1–4'
    c['review']['questionPages']=[6,7,8,9]
    c['review']['coveredQuestionRefs']=[f'2011 HL Section C2 Q{r["item"]}' for r in records]
    c['review']['atlasQuestions']=[{'n':f'c2-{r["item"]}','questionRef':f'2011 HL Section C2 Q{r["item"]}',
                                 'questionText':r['question'],'questionPages':r['questionPages'],'schemePages':r['schemePages']} for r in records]
    criteria=[]
    for r in records:
        n=r['item'];body=r['publishedSourceBlock']
        criteria.extend([
            {'id':f'section-{n}-content','label':f'Section {n} content (manual assessment)','maxMarks':10,'permittedMarks':list(range(11)),
             'guidance':[general,body]},
            {'id':f'section-{n}-discretion','label':f'Section {n} discretionary marks','maxMarks':2,'permittedMarks':[0,1,2],
             'guidance':[general],
             'limits':[{'id':f'section-{n}-incomplete','maxMarks':0,
                        'when':{'any':[{'flag':'incomplete-summary-response','prompt':incomplete}]},'guidance':[incomplete]}]},
        ])
    c['rubric']={'system':'language-points','count':1,
                'groups':[{'id':'complete-response','label':'Assess the complete four-section response','rows':[],'criteria':criteria}],
                'allocationCap':{'maxMarks':45,'sourceText':'Summary writing 45 marks','schemePages':[8]},
                'taskRequirements':[general],
                'markingGuideNote':'The original paper gives 40 marks for summary writing; the final marking scheme gives 45 for the complete section. This joint task retains all four original questions and the final scheme’s collective maximum, without assigning a fixed 11/12 split to individual sections. Assess each section’s content manually against its complete published pool and five-distinct-details rule, including Section 2’s all-four-category requirement and two-mark subject-list maximum, and Section 3’s two-boy-sport limit and one-mark leisure details up to four. The numerical controls record your manual assessment; they do not count or classify individual details. Normal discretion is one, or two for a particularly well-answered question. If the response fails to answer all required sections/subsections, select the printed condition to withhold all discretionary marks.'}
    return [c]


def language_and_matching(docs,source):
    result=[]
    for r in source['tasks']:
        unit=r['unit'];body=r['publishedSourceBlock']
        if unit not in ('LA1','CA1','LA2','SD'):continue
        c=source_card(r)
        if unit=='LA1':
            pairs=re.findall(r'\b(?:i|ii|iii|iv|v|vi)\.\s+(\S+)\s+(\S+)',body)
            assert pairs==[('пошел','пойти'),('вижу','видеть'),('живет','жить'),('забыл','забыть'),('нравятся','нравиться'),('дружат','дружить')]
            assert all(q in docs['paper'][3].get_text() for q,a in pairs)
            c['questionText']+='\n\n'+'\n'.join(f'{n}. {q}' for n,(q,a) in enumerate(pairs,1))
            c=as_points(c,[a for q,a in pairs],6)
            for g,(q,a) in zip(c['rubric']['groups'],pairs):g['label']=q;g['rows'][0]['marks']=1
            c['rubric']['taskRequirements']=[body.split('i. пошел',1)[0]]
        elif unit=='CA1':
            c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
            c['rubric']={'system':'language-points','count':2,'groups':[
                {'id':f'topic-{n}','label':topic,'rows':[],
                 'criteria':[{'id':f'topic-{n}-detail-{j}','label':f'Distinct detail {j}','maxMarks':2,'permittedMarks':[0,2],'guidance':[body]} for j in (1,2)]} for n,topic in enumerate(('дача','двор','дом'),1)],
                'taskRequirements':[body],'markingGuideNote':'Choose two original topics and give two distinct details per topic. Each correct detail earns two marks; no partial tariff is printed. The literal both/either-language allowance is retained.'}
        elif unit=='LA2':
            rows=r['answerRows'];c=as_points(c,[a for a,q in rows],5)
            for g,(a,q) in zip(c['rubric']['groups'],rows):g['label']=q;g['rows'][0]['marks']=1
            c['rubric']['taskRequirements']=[body.split('4 них')[0]]
        else:
            rows=r['answerRows'];c=as_points(c,[a for a,q in rows],10)
            for g,(answers,prompt) in zip(c['rubric']['groups'],rows):
                g['label']=prompt;full=answers.split()[0];partial=re.findall(r'(\d+) = 1 mark',answers)
                g['rows']=[{'id':'full','text':full,'marks':2}]+[{'id':f'partial-{n}','text':a,'marks':1} for n,a in enumerate(partial,1)]
            c['rubric']['taskRequirements']=[body.split('6 5 = 1 mark')[0]]
            c['rubric']['markingGuideNote']='Each answer retains its exact full-credit number and any published one-mark alternatives within the same single-answer group. No unique-use restriction is inferred.'
        result.append(c)
    assert len(result)==4
    return result


def grammar_forms(docs):
    paper=docs['paper'][11].get_text();paper=paper[paper.index('Настя'):]
    solved=docs['scheme'][11].get_text();solved=solved[solved.index('Настя'):]
    gaps=list(re.finditer(r'[.\u2026]+\s*\(([^)]+)\)',paper));assert len(gaps)==15
    fixed=lambda words:r'[^\w]*'.join(re.escape(word) for word in words)
    result=[]
    for n,gap in enumerate(gaps):
        before=paper[gaps[n-1].end() if n else 0:gap.start()];after=paper[gap.end():gaps[n+1].start() if n+1<len(gaps) else len(paper)]
        left=re.findall(r'\w+',before)[-3:];right=re.findall(r'\w+',after)[:3]
        pattern=fixed(left)+r'[^\w]+(\w+(?:\s*/\s*\w+)*)'+(r'[^\w]+'+fixed(right) if right else r'[^\w]*$')
        matches=re.findall(pattern,solved,re.I);assert len(matches)==1,(n,left,right,matches)
        result.append((gap[1],squash(matches[0])))
    assert [a for q,a in result]==['родилась','художественную','плаванием','студии','фильмах','профессиональной','вуза/ВУЗа','августа','маршруту','Амстердаме','завтракали','могу','центра','велосипеде','ночным']
    return result

def grammar(docs,source):
    r=next(r for r in source['tasks'] if r['unit']=='GR');pairs=grammar_forms(docs)
    c=as_points(source_card(r),[a for q,a in pairs],15)
    for n,(g,(q,a)) in enumerate(zip(c['rubric']['groups'],pairs),1):g['label']=f'{n}. {q}'
    c['rubric']['taskRequirements']=[r['publishedSourceBlock'].split('Настя')[0]]
    c['rubric']['markingGuideNote']='Both complete original texts share fifteen forms and one thirty-mark award. The source explicitly gives zero for inappropriate upper/lower case, misspelling or transcription errors. Both printed вуза/ВУЗа variants remain accepted; no text-specific subtotal or partial mark is invented.'
    return [c]


def writing(docs, source, base):
    S=docs['scheme']; result=[]
    for unit,sp,table_page in [('SE',13,14),('GW',15,17)]:
        record=next(c for c in source['tasks'] if c['unit']==unit)
        text='\n'.join(re.sub(r'^.*Lch\s+\d+\s+de\s+\d+.*Page\s+\d+\s+of\s+\d+.*$', '', S[n-1].get_text(sort=True), flags=re.M) for n in ([13] if unit=='SE' else [15,16]))
        expression_heading='2. Expression (E):' if unit=='SE' else '2. Expression (E)'
        content=between(text,'1. Communication/content (C)',expression_heading)
        expression=between(text,expression_heading)
        lower_e=squash(re.search(r'If the content mark.*?indicate\s+this\.',expression,re.S).group())
        lower_a=squash(re.search(r'If the expression is very fluent.*?indicate\s+this\.',expression,re.S).group())
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
        accommodations='Reasonable Accommodation: '+between(source['generalWrittenGuidance'],'Reasonable Accommodation:','Marking:')
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
            guide=text
            instructions=between(guide,'1. FACEBOOK','2. Expression (E):')
            instructions='1. FACEBOOK '+instructions
            c['rubric']['taskRequirements']=[squash(instructions),squash(re.search(r'If a candidate answers.*?one\(s\)\.',guide,re.S).group())]
            c['rubric']['markingGuideNote']+=' The discussion choice has its own printed exception: material copied directly from the second comprehension receives zero content marks; adapted or summarised details receive two content marks each, within the same fifteen-mark content maximum. Apply that source rule manually against the full guide; no exemplar content is invented.'
        result.append(c)
    return result


def listening(docs,source):
    result=[];audio=next(r['source'] for r in json.loads((ROOT/'data/russianAudio.json').read_text()) if r['year']==2011)
    for r in source['tasks']:
        if r['unit'] not in ('L1','L2','L3','L4'):continue
        key=(r['unit'],r['item'],r['roman']);body=r['publishedSourceBlock'];count=r['detailQuota']
        if key in [('L4',2,None),('L4',4,'i')]:
            c=source_card(r);c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
            c['rubric']={'system':'language-points','count':count,'groups':[
                {'id':f'detail-{n}','label':f'Distinct detail {n}','rows':[],
                 'criteria':[{'id':f'detail-{n}','label':f'Distinct detail {n}','maxMarks':2,'permittedMarks':[0,1,2],'guidance':[body]}]} for n in range(1,count+1)],
                'taskRequirements':[body],'markingGuideNote':'Assess distinct actual answers against the complete printed full and named one-mark partial pool. Do not invent a unique full/partial association or award a paraphrase twice. One mark requires a published partial.'}
        else:
            pool=body.split('OF:',1)[1].strip();partial=''
            if 'Award one mark for:' in pool:pool,partial=pool.split('Award one mark for:',1)
            answers=options(pool);c=as_points(source_card(r),answers,count)
            if partial:
                index=1
                c['rubric']['groups'][index]['rows'].append({'id':'partial','text':partial.strip(),'marks':1})
                assert key in [('L1',1,None),('L3',2,'ii')]
            c['rubric']['taskRequirements']=[body]
        if key==('L4',1,'i'):
            c['rubric']['markingGuideNote']='The original question asks when and where. Its published TWO OF pool contains three separately printed components: 17th May, 1992 and in Moscow. The source does not impose an additional one-date/one-place quota; all three remain available under the printed two-detail limit.'
        c['rubric']['taskRequirements']=[source['listeningGuidance']]+c['rubric']['taskRequirements']
        c['review']['guidancePages']=[18];c['topicId']=r['topicId'];c['additionalTopicIds']=['russian-1-0']
        c['sourceMaterial']['kind']='source-question';c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
        c['audioMaterial']=audio;result.append(c)
    assert len(result)==20 and sum(c['totalMarks'] for c in result)==80
    return result

def source_language_rules(cards,source):
    rule='Language of answer: '+between(source['generalWrittenGuidance'],'Language of answer:','When it should be Russian: award NO marks')+' When it should be Russian: award NO marks'
    for c in cards:
        if c['section']=='C2':
            # The summary-specific discretion exception has no printed
            # wholly/mixed threshold. Retain both original rules for manual
            # assessment; an automatic zero must not override the exception.
            c['rubric']['taskRequirements'].insert(0,squash(rule))
            for criterion in c['rubric']['groups'][0]['criteria']:
                criterion['guidance'].insert(0,squash(rule))
            c['review']['guidancePages']=[3]
            c['rubric']['markingGuideNote']+=' Assess language manually for each section. Read the general no-marks instruction alongside the summary-specific discretion exception. The scheme gives no numerical or wholly/mixed-language threshold; do not automatically remove discretionary marks merely because Russian words appear. English or Irish is permitted by the original bilingual paper.'
            continue
        if c['section'] not in ('C1','LA1','GR','SE','GW'):continue
        c['answerLanguageRule']={'otherLanguageMultiplier':0,'sourceText':squash(rule),'schemePages':[3]}
        if c['section'] in ('C1','C2'):c['rubric']['markingGuideNote']+=' Answer in English or Irish, as allowed by the original bilingual paper.'



def split_original_page_quotes(cards):
    # Literal quotations cross bilingual footer text at two verified physical
    # page boundaries. Split the source slices, preserving every original word.
    boundaries={'ru-2011-hl-c2':'art + subjects in which',
                'ru-2011-hl-gw':'3. INTERVIEW'}
    def walk(value,marker):
        if isinstance(value,dict):
            for key,child in value.items():
                if key in ('guidance','taskRequirements'):
                    output=[]
                    for text in child:
                        if marker in text and text.index(marker)>0:
                            at=text.index(marker);parts=[text[:at].strip(),text[at:].strip()]
                            assert squash(' '.join(parts))==squash(text)
                            output.extend(parts)
                        else:output.append(text)
                    value[key]=output
                else:walk(child,marker)
        elif isinstance(value,list):
            for child in value:walk(child,marker)
    for card in cards:
        if card['id'] in boundaries:walk(card['rubric'],boundaries[card['id']])


def build():
    docs,source=source_records()
    cards=reading(source)+summaries(docs,source)+language_and_matching(docs,source)+grammar(docs,source)+writing(docs,source,base)+listening(docs,source)
    source_language_rules(cards,source)
    split_original_page_quotes(cards)
    assert len(cards)==36 and len({c['id'] for c in cards})==36
    assert sum(c['totalMarks'] for c in cards)==300
    assert sum(bool(c.get('answerLanguageRule')) for c in cards)==12
    assert not next(c for c in cards if c['id']=='ru-2011-hl-c2').get('answerLanguageRule')
    for doc in docs.values():doc.close()
    return cards

if __name__=='__main__':save_reviewed(build())
