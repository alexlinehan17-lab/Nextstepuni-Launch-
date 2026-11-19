"""Russian 2010 Higher source authoring proposal; original source allocation retained."""
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

METADATA = {'paper': {'pages': 16, 'sha256': 'b31909e020b82ba2a6748f8b2ff59aa6bc5b0fc2c9351e7290d54c7e2215b475'}, 'aural': {'pages': 8, 'sha256': '98d9cd466281c69324f32e244a4734d9075c880d3d3850859dcc301120be03db'}, 'scheme': {'pages': 20, 'sha256': '15607f22c24d4502dee8d28cd319711c880d27d06eac33b1da96fa6554a0672c'}}

def source_records():
    docs = {}
    for kind, relative in [('paper', 'papers/2010-hl-000-paper.pdf'),
                           ('aural', 'papers/2010-hl-A00-paper.pdf'),
                           ('scheme', 'schemes/2010-hl.pdf')]:
        path = ROOT / 'examiner-reports/russian' / relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == METADATA[kind]['sha256']
        docs[kind] = fitz.open(path)
    from ru_2010_hl_fonts import open_repaired_scheme, scheme_page
    docs['scheme'].close(); docs['scheme'] = open_repaired_scheme()
    Q, A, S = docs['paper'], docs['aural'], docs['scheme']

    def page(doc, n, right=False):
        if doc is S:return scheme_page(doc,n)
        rect = fitz.Rect(295, 30, 580, 793) if right else fitz.Rect(20, 30, 580, 793)
        text = doc[n-1].get_text(clip=rect, sort=False).replace('\uf0b7', '•').replace('\xa0', ' ')
        return re.sub(r'^[^\n]*Lch\s+\d+\s+de\s+\d+[^\n]*Page\s+\d+\s+of\s+\d+[^\n]*\n?', '', text, flags=re.M)

    norm = lambda t: re.sub(r'[^\w]', '', t.casefold())

    def numbered_blocks(text):
        heads=list(re.finditer(r'^\s*(\d)\.\s*(?:(iv|i{1,3})\.?\s*)?(?=[A-Z“])',text,re.M))
        return [(int(h.group(1)),h.group(2),text[h.end():heads[n+1].start() if n+1<len(heads) else len(text)]) for n,h in enumerate(heads)]

    def record(unit, item, roman, question, qp, body, sp, total, **extra):
        component = 'aural' if unit in ('L1', 'L2', 'L3', 'L4') else 'paper'
        fragments=extra.get('questionFragments')
        if fragments:
            assert question==squash(' '.join(fragments))
            if (unit,item,roman,qp)==('LA1',None,None,[5]):
                assert len(fragments)==12 and sum(f.startswith('Give an example') for f in fragments)==6
                assert [f for f in fragments if re.fullmatch(r'Section [1-4]',f)]==['Section 1','Section 2','Section 3','Section 4']
            elif (unit,item,roman,qp)==('LA2',1,None,[9]):
                assert len(fragments)==9 and fragments[1]=='Sampla/Example:'
                assert fragments[2:]==['получила','получить','имеют','выбрались','поняла','создалось','стали']
                assert extra['printedVerbs']==fragments[4:]
            else:raise AssertionError((unit,item,roman,qp))
            assert all(norm(fragment) in norm(docs['paper'][qp[0]-1].get_text()) for fragment in fragments)
        else:
            assert any(norm(question) in norm(' '.join(page(docs[component], p, right=right) for p in qp))
                       for right in (False, True)), (unit, item, roman, question)
        return dict(id='ru-2010-hl-' + unit.lower() + (f'-{item}' if item is not None else '') + (f'-{roman}' if roman else ''),
                    unit=unit, item=item, roman=roman, question=question, questionPages=qp,
                    component=component, publishedSourceBlock=squash(body), schemePages=sp,
                    publishedTotal=total, **extra)

    cards = []
    source='\n'.join(page(S,p) for p in (4,5)).split('Language awareness')[0]
    blocks=numbered_blocks(source)
    asks=[(i,r,question_text(q),p) for p in (3,4) for i,r,q in numbered_blocks(page(Q,p,True))]
    assert len(blocks)==len(asks)==8
    totals=[6,2,4,2,2,2,6,14]
    for (i,r,b),(qi,qr,q,p),total in zip(blocks,asks,totals):
        assert (i,r)==(qi,qr)
        price=re.search(r'(\d)\s*x\s*2\s*[=+]\s*(\d+)',b)
        assert price and int(price.group(2))==total
        cue,body=b[:price.start()],b[price.start():]
        assert score(bag(q),bag(cue))>.75,(q,cue)
        cards.append(record('C1',i,r,q,[p],body,[4,5],total,
                            pending='Seven details, minimum two from each traditional/modern category; needs actual quota enforcement.' if i==5 else ''))
    assert sum(c['publishedTotal'] for c in cards)==38

    summary_source='\n'.join(page(S,p) for p in (7,8)).split('Language awareness')[0]
    blocks=numbered_blocks(summary_source)
    asks=[]
    for p in (7,8):
        raw=page(Q,p,True);heads=list(re.finditer(r'^\s*Section ([1-5])\s*$',raw,re.M))
        for n,h in enumerate(heads):
            asks.append((int(h.group(1)),question_text(raw[h.end():heads[n+1].start() if n+1<len(heads) else len(raw)]),p))
    assert len(blocks)==len(asks)==5
    for (i,r,b),(qi,q,p) in zip(blocks,asks):
        assert i==qi and r is None
        price=re.search(r'\(3 x 2\)\+2=8',b);assert price
        cue,body=b[:price.start()],b[price.start():]
        assert score(bag(q),bag(cue))>.75,(q,cue)
        cards.append(record('C2',i,None,q,[p],body,[7,8],8,
                            scoring=dict(detail=2,detailQuota=3,discretionaryMaximum=2,partialDetail=1,incompleteDiscretionaryMaximum=1),
                            reviewNote='Summary1 requires both visit origin and confusion; summary5 expressly accepts two details from Section4.'))

    prompts=[squash(p) for p in re.findall(r'Give an example[^_\n]+',page(Q,5))]
    assert len(prompts)==6
    lines=[line.strip() for line in Q[4].get_text().splitlines() if line.strip()]
    lines=lines[lines.index('Language awareness'):]
    fragments=[line for line in lines if line in ('Language awareness','(12 marks)') or re.fullmatch(r'Section [1-4]',line) or line.startswith('Give an example')]
    q=squash(' '.join(fragments))
    b='Language awareness '+between('\n'.join(page(S,p) for p in (5,6)),'Language awareness')
    cards.append(record('LA1',None,None,q,[5],b,[5,6],12,printedPrompts=prompts,questionFragments=fragments,
                        sourcePages=[2,5],scoring=dict(requestedExamples=6,perExample=2),pending='Source explicitly awards2 to everyone for absent plural-dative noun; preserve automatic award and no invented answer. English translations/dictionary forms accepted.'))
    raw='Give the infinitives '+re.split(r'2\.\s+Aimsigh',between(page(Q,9),'Give the infinitives'),maxsplit=1)[0]
    words=re.findall(r'^\s*([а-яё]+)\s*$',raw,re.M)
    assert words==['получила','получить','имеют','выбрались','поняла','создалось','стали']
    fragments=[squash(raw.split('Sampla/Example:',1)[0]),'Sampla/Example:',*words]
    q=squash(' '.join(fragments))
    b='1. Verb infinitives '+between(page(S,8),'1. Verb infinitives','2. Find five words')
    cards.append(record('LA2',1,None,q,[9],b,[8],5,questionFragments=fragments,printedVerbs=words[2:],scoring=dict(correctInfinitives=5,perInfinitive=1)))
    q='Find five words '+question_text(between(page(Q,9),'Find five words'))
    b='2. Find five words '+between(page(S,8),'2. Find five words')
    cards.append(record('LA2',2,None,q,[9],b,[8],5,scoring=dict(words=5,perWord=1),reviewNote='Original wording supplies no location; words beyond text allowed. Swimming accepted, sailing/boating excluded; printed pool is not exclusive.'))
    q='Read through '+squash(between(page(Q,10,True),'Read through'))
    q=q[:q.index('(20 marks)')+len('(20 marks)')]
    rows=[[squash(v or '') for v in row] for row in S[8].find_tables().tables[0].extract()]
    assert [r[0] for r in rows]==['7','8','3','5','1','4','2','10','9','6'],rows
    cards.append(record('SD',None,None,q,[10],page(S,9),[9],20,answerRows=rows,scoring=dict(correctAnswers=10,perAnswer=2)))
    q='Read through the following text. '+squash(between(page(Q,11,True),'Read through the following text.'))
    q=q[:q.index('substitute words.')+len('substitute words.')]
    cards.append(record('GR',None,None,q,[11],page(S,10),[10],30,sourcePages=[11,12],scoring=dict(correctForms=15,perForm=2),reviewNote='Wrong capitalization0; university singular/plural alternative retained.'))
    q='Write a short essay '+squash(between(page(Q,13,True),'Write a short essay'))
    q=q[:q.index('(30 marks)')+len('(30 marks)')]
    cards.append(record('SE',None,None,q,[13],'\n'.join(page(S,p) for p in (11,12)),[11,12],30,fullQuestionPage=page(Q,13),pending='Shared conditional Lower A range9–14; all eight Russian topic labels retained.'))
    q='Write a piece '+question_text(page(Q,14,True).split('Write a piece',1)[1])
    cards.append(record('GW',None,None,q,[14],'\n'.join(page(S,p) for p in (13,14,15)),[13,14,15],40,
                        pending='Shared conditional Lower A range7–12 with overlapping9–11/11–12. Seven choices retained; parenthesized additional information remains optional.'))
    assert len(cards)==20 and sum(c['publishedTotal'] for c in cards)==220

    source='\n'.join(page(S,p) for p in range(16,20))
    heads=list(re.finditer(r'^\s*SECTION (IV|III|II|I|1)\b[^\n]*$',source,re.M))
    assert len(heads)==4
    counts=[[2]*5,[3,2,2,2,1],[3,1,3,2,1],[4,4,2]]
    starts=[['President of Russian','Festival/competition','Longest/biggest','Buy an apartment'],
            ['Born in 1982','Original +','Had met a girl','English +','To study music'],
            ['Comparable to/','Sun (rays)','Business rooms','football +','150 million euro'],
            ['Collection of films','Cost is 3600','2 operators/twice']]
    topics=[['russian-0-2','russian-2-8','russian-0-7','russian-0-7','russian-0-6'],
            ['russian-0-3','russian-0-4','russian-0-8','russian-0-3','russian-0-6'],
            ['russian-0-5']*5,['russian-0-9']*3]
    for n,h in enumerate(heads):
        section=n+1;b=source[h.end():heads[n+1].start() if n+1<len(heads) else len(source)]
        blocks=numbered_blocks(b)
        asks=[(i,r,question_text(q)) for i,r,q in numbered_blocks(page(A,section+1,True))]
        assert len(asks)==len(counts[n]) and len(blocks)==len(asks)-(section==1),section
        expected=counts[n];section_topics=topics[n]
        if section==1:
            i,r,q=asks.pop(0);assert (i,r)==(1,None)
            cards.append(record('L1',1,'i',q,[2],'',[16],4,detailQuota=2,topicId=section_topics[0],
                                derivedTotalBasis=dict(detailCount=2,marksPerDetail=2,sourceText='Award two marks for each correct/relevant point.',schemePages=[16],questionPages=[2]),
                                missingAcceptedAnswerSource=True,pending='Original scheme starts at1(ii); no1(i) accepted answer printed. Do not borrow Ordinary answer. Booklet English labels1, Irish1(i).'))
            expected=expected[1:];section_topics=section_topics[1:]
        for (i,r,b),(qi,qr,q),count,start,topic in zip(blocks,asks,expected,starts[n],section_topics):
            assert (i,r)==(qi,qr)
            cue,body=source_split(b,start)
            assert score(bag(q),bag(cue))>.75,(q,cue)
            cards.append(record(f'L{section}',i,r,q,[section+1],body,[section+15],count*2,detailQuota=count,topicId=topic))
    assert len(cards)==38 and sum(c['publishedTotal'] for c in cards)==300
    assert len({c['id'] for c in cards})==38
    for c in cards:
        if not c['publishedSourceBlock']:
            assert c.get('missingAcceptedAnswerSource') is True
        else:assert norm(c['publishedSourceBlock']) in norm('\n'.join(page(S,p) for p in c['schemePages'])),c['id']
    draft=dict(status='Source-only draft; not runtime cards or a completed sitting',sources=METADATA,
               independentTasks=38,writtenTasks=20,listeningTasks=18,printedExamTotal=300,sourceLeafTotal=300,
               sourceLeafTotalIncludesDerivedMissingAnswerMarks=4,
               missingAcceptedAnswerTasks=['ru-2010-hl-l1-1-i'],
               aggregateDiscrepancy='Paper reading28 versus scheme leaves24. Source C1 reading24+culture14+language12=50.',
               generalWrittenGuidance=squash(page(S,3)),comprehensionGuidance=squash(page(S,4).split('1. Give')[0]),
               summaryGuidance=squash(summary_source[:re.search(r'^\s*1\.\s+[A-Z]',summary_source,re.M).start()]),
               listeningGuidance=squash(source[:heads[0].start()]),tasks=cards,
               fontRepair='In-memory Times glyph matching against original paper; two short Cambria spans visually transcribed from original scheme5/10 with consistent repeated glyphs. See repair_original_fonts.py; originals untouched.')
    return docs,draft


from ru_review_2026_hl import base as common_base,as_points,save_reviewed,mark_range
from ru_review_2017_hl import options,named_group,band

def base(*args,**kwargs):
    c=common_base(*args,**kwargs)
    for key in ('id','questionRef'):c[key]=c[key].replace('2026','2010')
    c['year']=2010;c['sourceMaterial']['title']=c['sourceMaterial']['title'].replace('2026','2010');return c

def source_card(r):
    pages=r.get('sourcePages') or ([2,3,4] if r['unit'] in ('C1','CA1') else [6,7,8,9] if r['unit'] in ('C2','LA2') else r['questionPages'])
    c=base(r['unit'],r['question'],r['publishedTotal'],pages,r['schemePages'],r['item'],r['roman']);c['review']['questionPages']=r['questionPages'];return c

def reading(source):
    result=[]
    for r in source['tasks']:
        if r['unit']!='C1' or r['item']==5:continue
        body=r['publishedSourceBlock'];count=r['publishedTotal']//2;c=source_card(r)
        price=re.search(r'\d\s*x\s*2\s*[=+]\s*\d+',body);assert price
        pool=body[price.end():].strip()
        if 'assign one mark:' in pool:
            c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
            c['rubric']={'system':'language-points','count':count,'groups':[
                {'id':f'detail-{n}','label':f'Distinct detail {n}','rows':[],
                 'criteria':[{'id':f'detail-{n}','label':f'Distinct detail {n}','maxMarks':2,'permittedMarks':[0,1,2],'guidance':[body]}]} for n in range(1,count+1)],
                'taskRequirements':[source['comprehensionGuidance'],body],
                'markingGuideNote':'Assess each distinct response against the complete full, named partial and zero-credit guidance. One mark is available only for a printed partial. Do not infer a fixed full/partial pairing or count a paraphrase twice.'}
        else:
            c=as_points(c,options(pool),count);c['rubric']['taskRequirements']=[source['comprehensionGuidance'],body]
        c['rubric']['markingGuideNote']+=' The original paper gives 28 reading marks, while the seven scheme reading allocations total 24; cultural awareness adds 14 and language awareness adds 12 to the printed 50. The original task allocations are retained.'
        c['review']['guidancePages']=[4];result.append(c)
    assert len(result)==7 and sum(c['totalMarks'] for c in result)==24
    return result


def culture(source):
    from ru_topics import topic_for
    r=next(r for r in source['tasks'] if r['unit']=='C1' and r['item']==5)
    body=r['publishedSourceBlock']
    assert 'There should be seven details in total, a minimum of two details from each category.' in body
    partial='where reference is made to the language of the traditional folk/oral narrative but where there is no example/illustration'
    assert partial in body
    c=source_card(r);c['topicId']=topic_for('CA1')
    c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
    criteria=[]
    for category,count in [('traditional',2),('modern',2),('additional',3)]:
        for n in range(1,count+1):
            label=f'{category.title()} distinct detail {n}'
            if category=='additional':label+= ' (either category, not already credited)'
            criteria.append({'id':f'{category}-{n}','label':label,'maxMarks':2,
                             'permittedMarks':[0,2] if category=='modern' else [0,1,2],
                             'guidance':[body]})
    c['rubric']={'system':'language-writing','criteria':criteria,'taskRequirements':[body],
                'markingGuideNote':'Assess seven distinct details: two traditional, two modern and three additional details from either category. Reserve the first four slots for their named categories and never count the same fact twice. One mark is available only for the printed traditional narrative-language reference without an example or illustration; it is not a general partial tariff and is not tied to one particular full-credit example. This remains the original Question 5 within the comprehension, filed under cultural awareness.'}
    return [c]


def summaries(source):
    """Five published three-detail summaries; source-specific manual discretion."""
    result=[];general=source['summaryGuidance']
    incomplete=general[general.index('If a candidate fails'):]
    for record in source['tasks']:
        if record['unit']!='C2':continue
        body=record['publishedSourceBlock'];card=source_card(record)
        if record['item'] in (1,5):
            # Question1 requires both questions, without a numeric split between
            # them. Question5 has a pool-level partial and expressly accepts
            # details from Section4. Manual distinct responses avoid inventing
            # a fixed category allocation or an exclusive partial association.
            card.pop('rows');card.pop('tariffModel');card['kind']='rubric'
            card['rubric']={'system':'language-points','count':3,'groups':[
                {'id':f'detail-{n}','label':f'Distinct detail {n} — manual assessment','rows':[],
                 'criteria':[{'id':f'detail-{n}','label':f'Distinct detail {n}','maxMarks':2,
                              'permittedMarks':[0,1,2],'guidance':[body,general]}]}
                for n in (1,2,3)],'taskRequirements':[general,body],
                'markingGuideNote':'Assess three distinct actual details against the complete printed full, partial and no-credit guidance. Do not count a paraphrase twice. Assess the meaning of each response manually using the printed guidance.'}
            if record['item']==1:
                card['rubric']['markingGuideNote']+=' The response must address BOTH how the visit came about and the cause of confusion. The scheme gives no separate mark allocation to these two questions. Apply the printed incomplete-response discretionary limit if a required question is unanswered.'
            else:
                card['rubric']['markingGuideNote']+=' The scheme expressly accepts the two named details from Section4. Assess the named one-mark wording as a partial response. A complete and partial version of the same actual detail earns credit once.'
        else:
            pool=re.sub(r'^\(3 x 2\)\+2=8\s*','',body)
            assert pool!=body,record['id']
            pool=pool.split('Assign no mark for:',1)[0].strip()
            card=as_points(card,options(pool),3,steps=[0,1,2])
            card['rubric']['taskRequirements']=[general,body]
            card['rubric']['markingGuideNote']='Assess each distinct source detail once. Each printed plus-separated concept remains available within the three-detail quota; slash wordings stay together as alternatives. One mark follows the original intelligible-partial-detail rule.'
        card['rubric']['criteria']=[{'id':'summary-skills','label':'Discretionary marks','maxMarks':2,
            'permittedMarks':[0,1,2],'guidance':[general],
            'limits':[{'id':'incomplete-response','maxMarks':1,'when':{'any':[{'flag':'incomplete-response','prompt':incomplete}]},'guidance':[incomplete]}]}]
        card['review']['guidancePages']=[7];result.append(card)
    assert len(result)==5 and sum(card['totalMarks'] for card in result)==40
    return result


def source_language_rules(cards,source):
    general=source['generalWrittenGuidance']
    rule='Language of answer:'+between(general,'Language of answer:','1. The examiner')
    clause=re.search(r'Discretionary marks may be awarded[\s\S]*?answers\)\.',source['summaryGuidance'])
    assert clause
    for card in cards:
        if card['section'] not in ('C1','C2','LA2','GR','SE','GW'):continue
        card['answerLanguageRule']={'otherLanguageMultiplier':0,'sourceText':squash(rule),'schemePages':[3]}
        if card['section'] in ('C1','C2'):
            card['rubric']['markingGuideNote']+=' Answer in English or Irish as directed by the original bilingual paper.'
        if card['section']=='C2':
            card['answerLanguageRule']['manualCriterionExceptions']={
                'criterionIds':['summary-skills'],'sourceText':clause.group(),'schemePages':[7]}


"""Temporary source proposal: no runtime publication or original-source gate claimed."""


def language_and_matching(docs, source):
    result=[]
    for r in source['tasks']:
        unit=r['unit'];body=r['publishedSourceBlock']
        if unit not in ('LA2','SD'):continue
        c=source_card(r)
        if unit=='LA2' and r['item']==1:
            printed=r['printedVerbs']
            pairs=re.findall(r'([а-яё]+)\s+([а-яё]+)',body.split('5 x 1 + 5',1)[1])
            assert pairs==[('имеют','иметь'),('выбрались','выбраться'),('поняла','понять'),('создалось','создаться'),('стали','стать')]
            assert [q for q,a in pairs]==printed
            assert all(q in c['questionText'] for q in printed)
            assert 'Sampla/Example: получила получить' in c['questionText']
            c=as_points(c,[answer for prompt,answer in pairs],5)
            for g,(prompt,answer) in zip(c['rubric']['groups'],pairs):
                g['label']=prompt;g['rows'][0]['marks']=1
            c['rubric']['taskRequirements']=[body.split('имеют',1)[0]]
            c['rubric']['markingGuideNote']='The printed worked example is retained with the question. Assess only the five requested verb forms, at one mark for each correct infinitive.'
        elif unit=='LA2':
            c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
            c['rubric']={'system':'language-points','count':5,'groups':[
                {'id':f'word-{n}','label':f'Different word {n}','rows':[],
                 'criteria':[{'id':f'word-{n}','label':f'Different word {n}','maxMarks':1,'permittedMarks':[0,1],'guidance':[body]}]}
                for n in range(1,6)],
                'taskRequirements':[body],
                'markingGuideNote':'Assess five different Russian words manually against the printed swimming rule. The scheme explains that the question does not specify a passage to search; its printed words are examples, not an exclusive list. Sailing or boating words receive no credit. No additional exemplar answers are supplied.'}
        else:
            rows=r['answerRows'];assert [number for number,text in rows]==['7','8','3','5','1','4','2','10','9','6']
            c=as_points(c,[number for number,text in rows],10)
            for g,(number,prompt) in zip(c['rubric']['groups'],rows):g['label']=prompt
            c['rubric']['taskRequirements']=[body.split('7 В детском лагере',1)[0]]
            c['rubric']['markingGuideNote']='Each original answer paragraph retains its published matching question number and two-mark award. The complete ten questions and ten answer paragraphs remain in the original source.'
        result.append(c)
    assert len(result)==3 and sum(c['totalMarks'] for c in result)==30
    return result


def grammar_pairs(paper, solved):
    paper=paper[paper.index('Как поступить'):]
    solved=solved[solved.index('Как поступить'):]
    # A single sentence-ending full stop after (30 - 34 недели) is not a gap.
    gaps=list(re.finditer(r'\(([^)\n]+)\)\s*[.\u2026]{2,}',paper));assert len(gaps)==15
    fixed=lambda words:r'[^\w]*'.join(re.escape(word) for word in words)
    result=[]
    for n,gap in enumerate(gaps):
        before=paper[gaps[n-1].end() if n else 0:gap.start()]
        left=re.findall(r'\w+',before)[-3:]
        matches=re.findall(fixed(left)+r'[^\w]+(\w+(?:\s*/\s*\w+)*)',solved,re.I)
        assert len(matches)==1,(n,left,matches)
        result.append((gap[1],squash(matches[0])))
    assert [a for q,a in result]==['университете','заведением','экзаменов','языку','школы','образования','могут','январе','существует','месяцев','университета/университетов','молодым','организаций','сайте','центра']
    return result


def grammar(docs,source):
    r=next(r for r in source['tasks'] if r['unit']=='GR')
    pairs=grammar_pairs('\n'.join(docs['paper'][n-1].get_text() for n in (11,12)),docs['scheme'][9].get_text())
    c=as_points(source_card(r),[answer for prompt,answer in pairs],15)
    for n,(g,(prompt,answer)) in enumerate(zip(c['rubric']['groups'],pairs),1):g['label']=f'{n}. {prompt}'
    c['rubric']['taskRequirements']=[r['publishedSourceBlock'].split('Как поступить')[0]]
    c['rubric']['markingGuideNote']='Each of the fifteen original gaps earns two marks for a correct accepted form. Misspelling, transcription and inappropriate upper/lower case receive zero as printed. The two университет prompts retain their context-specific forms, including the singular/plural alternative in the later gap. No capitalization partial mark is supplied this year.'
    return [c]


"""Temporary 2010 writing proposal; tables and original-source gates still pending."""


def source_table(doc, page, columns, tokens):
    found=[]
    for table in doc[page-1].find_tables().tables:
        rows=table.extract()
        if rows and len(rows[0])==columns and all(token in squash(' '.join(x or '' for x in rows[0])) for token in tokens):found.append(rows)
    assert len(found)==1,(page,columns,tokens,len(found))
    return found[0]


def writing(docs,source):
    result=[];S=docs['scheme']
    for unit in ('SE','GW'):
        r=next(r for r in source['tasks'] if r['unit']==unit);text=r['publishedSourceBlock'];essay=unit=='SE'
        content=between(text,'1. Communication/content (C)','2. Expression (E):')
        expression=between(text,'2. Expression (E):')
        lower_e=squash(re.search(r'If the content mark.*?indicate this\.',expression,re.S).group())
        lower_a=squash(re.search(r'If the expression is very fluent.*?indicate this\.',expression,re.S).group())
        soft=squash(re.search(r'Penalise students.*?\(– .*?\)\.',expression,re.S).group())
        normal=[];lower=[];accuracy=[];content_bands=[]
        if essay:
            rows=source_table(S,12,4,['Content','Language'])
            for content_price,content_description,prices,description in rows[1:]:
                content_bands.append(band(content_price,content_description));prices=squash(prices)
                normal.append(band(prices.split('lower')[0],description))
                lower.append(band(prices.split('lower E')[-1] if 'lower E' in prices else prices,description))
                a=re.search(r'lower A (\d+-\d+)',prices)
                if a:accuracy.append(band(a.group(1),description))
            assert [b['marks'] for b in accuracy]==[[13,14],[11,12],[9,10]]
        else:
            rows=source_table(S,14,3,['Lower E','Expression'])
            for low,full,description in rows[1:]:normal.append(band(full,description));lower.append(band(low,description))
            accuracy_source=[(squash(price),squash(description)) for price,description in source_table(S,15,2,['Lower A','Expression'])[1:]]
            assert [mark_range(price) for price,description in accuracy_source]==[[11,12],[9,10,11],[7,8]]
        question=r['question']
        if essay:
            choices=between(r['fullQuestionPage'],'Напишите').split('___')[0]
            assert len(re.findall(r'^\s*(?:viii|vii|vi|iv|v|iii|ii|i)\.\s*$',choices,re.M))==8
            question+='\n\nНапишите'+choices
        c=base(unit,question,r['publishedTotal'],r['questionPages'],r['schemePages']);c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
        criteria=[{'id':'content','label':'Communication/content (C)','maxMarks':10 if essay else 15,'permittedMarks':list(range(11 if essay else 16)),'guidance':[squash(content)]}]
        if essay:
            criteria[0]['bands']=content_bands
            title=squash(re.search(r'Candidates are required.*?overall content score\.',content,re.S).group())
            criteria.append({'id':'title-penalty','label':'Essay title penalty','kind':'deduction','deductFrom':'content','maxMarks':1,'permittedMarks':[0,1],'guidance':[title]})
        limits=[{'id':'lower-e','scaleLabel':'Lower E','maxMarks':14 if essay else 10,
                 'when':{'any':[{'criterionIds':['content'],'atMost':5 if essay else 7,**({'ignoreDeductions':True} if essay else {})},{'length':'words','below':25 if essay else 60}]},'bands':lower,'guidance':[lower_e]},
                {'id':'lower-a','scaleLabel':'Lower A','minMarks':9 if essay else 7,'maxMarks':14 if essay else 12,
                 'when':{'any':[{'flag':'lower-a','prompt':lower_a}]},'guidance':[lower_a]}]
        if essay:
            limits[1]['bands']=accuracy
            no_content=squash(re.search(r'Answers which.*?no marks for language\.',content,re.S).group())
            limits.append({'id':'no-content','maxMarks':0,'when':{'any':[{'criterionIds':['content'],'atMost':0,'ignoreDeductions':True}]},'guidance':[no_content]})
        else:limits[1]['guidance'] += [price+' '+description for price,description in accuracy_source]
        global_view=squash(expression[:expression.index('If the content mark')]).rstrip('•\uf0b7 ').strip()
        annotation='Put square box '+squash(between(expression,'Put square box','Penalise students'))
        accommodations='Waivers: '+between(source['generalWrittenGuidance'],'Waivers:','Language issues')
        maximum=20 if essay else 15
        criteria.append({'id':'expression','label':'Language + expression (E)','maxMarks':maximum,'permittedMarks':list(range(maximum+1)),
                         'guidance':[global_view,annotation,accommodations],'bands':normal,'limits':limits})
        if not essay:
            coherence=[band(price,description) for price,description in source_table(S,15,2,['Mark','Textual coherence'])[1:]]
            coherence_guidance='3. Textual coherence: '+between(text,'3. Textual coherence:','Mark Textual coherence')
            criteria.append({'id':'coherence','label':'Textual coherence (TC)','maxMarks':10,'permittedMarks':list(range(11)),'guidance':[squash(coherence_guidance)],'bands':coherence})
        criteria.append({'id':'soft-sign-penalty','label':'Soft sign penalty','kind':'deduction','deductFrom':'expression','maxMarks':2,'permittedMarks':[0,1,2] if essay else [0,2],'guidance':[soft]})
        c['rubric']={'system':'language-writing','criteria':criteria,'taskRequirements':[],'markingGuideNote':''};c['review']['guidancePages']=[3]
        if not essay:
            instructions='1. LETTER '+between(text,'1. LETTER','2. Expression (E):')
            best=squash(re.search(r'If a candidate answers.*?one\(s\)\.',text,re.S).group())
            brackets=source['generalWrittenGuidance'][source['generalWrittenGuidance'].index('Round brackets'):]
            c['rubric']['taskRequirements']=[squash(instructions),best,brackets]
            c['rubric']['markingGuideNote']='Assess the chosen response manually against its complete printed categories, one mark per content detail. Parenthesized additional-relevant-information categories retain the source’s general “valid but not essential” rule. The content paragraph itself says no marks for additional information/content; both original statements remain visible, without an invented category tariff or silently rewritten rule. Lower A has a descriptor conflict: the prose gives 9/10, while the table prints 9–11 and also 11–12. Both exact versions are retained. The numeric range remains 7–12; no descriptor is trimmed, no precedence is invented, and no minimum is automatically awarded.'
        result.append(c)
    assert len(result)==2 and sum(c['totalMarks'] for c in result)==70
    return result


"""Temporary listening proposal; native audio and original-source gates remain pending."""


def listening(docs,source):
    result=[]
    audio=next(row['source'] for row in json.loads((ROOT/'data/russianAudio.json').read_text()) if row['year']==2010)
    for r in source['tasks']:
        if r['unit'] not in ('L1','L2','L3','L4'):continue
        key=(r['unit'],r['item'],r['roman']);body=r['publishedSourceBlock'];count=r['detailQuota']
        c=source_card(r)
        if r.get('missingAcceptedAnswerSource'):
            assert key==('L1',1,'i') and not body and count==2
            c['kind']='question';c['tariffModel']={'kind':'questionTotal'}
            c['rows']=[{'id':'published-guidance','kind':'point','verbatim':source['listeningGuidance'],'marks':None,
                'contextNote':'The original listening booklet asks for two details about Yaroslavl. Its English column labels this question 1, while its Irish column labels it 1(i); the scheme starts with the different visitors question 1(ii). No accepted city-answer pool is printed in the available original scheme. The recorded 4 is derived from two requested details and the general two-marks-per-detail rule; it is not a separately printed task total or an assessed score. Listen to the original recording and review your response; this card does not calculate a numerical score. No answers are borrowed from the Ordinary paper.'}]
        else:
            pieces=re.split(r'(?i)\s*award one mark:\s*',body);assert len(pieces)<=2
            pool=pieces[0].split('Award no marks:',1)[0].strip()
            answers=options(pool);c=as_points(c,answers,count)
            if len(pieces)==2:
                partial=pieces[1].strip()
                if key==('L1',1,'ii'):
                    assert answers[-1]=='1,5 million tourists (accept in excess of 1 million tourists)' and partial=='many tourists'
                    c['rubric']['groups'][-1]['rows'].append({'id':'partial','text':partial,'marks':1})
                elif key==('L1',3,None):
                    partials=options(partial)
                    assert answers[1]=='800m (long)' and partials[1]=='8?? M long'
                    assert answers[2]=='1.5 thousand people can sit on it/it can fit 1.5 thousand people on it'
                    assert partials[0]=='many/500/1000 people can sit on it at once'
                    for group_index,partial_index in ((1,1),(2,0)):
                        c['rubric']['groups'][group_index]['rows'].append({'id':'partial','text':partials[partial_index],'marks':1})
                elif key==('L1',4,None):
                    assert answers[-1]=='open a chain of shops (in St Petersburg)' and partial=='open a shop'
                    c['rubric']['groups'][-1]['rows'].append({'id':'partial','text':partial,'marks':1})
                elif key==('L3',3,'ii'):
                    assert answers==['150 million euro'] and partial=='million euro'
                    c['rubric']['groups'][0]['rows'].append({'id':'partial','text':partial,'marks':1})
                else:raise AssertionError(key)
                c['rubric']['markingGuideNote']='Each printed partial remains an alternative to the complete version of the same detail; it cannot earn additional credit alongside that full detail. All distinct details retain the question’s published quota.'
            if key==('L1',2,None):
                assert 'from ANY TWO OF:' in answers[3]
                c['rubric']['markingGuideNote']='The international/from-all-over-the-world alternative includes the exact requirement for any two named countries. That is one accepted detail under the question’s two-detail quota; the countries do not each earn two marks.'
            if key==('L1',3,None):c['rubric']['markingGuideNote']+=' The partial length is printed literally as “8?? M long”; no precise substitute number is supplied.'
            c['rubric']['taskRequirements']=[source['listeningGuidance'],body]
        c['review']['guidancePages']=[16];c['topicId']=r['topicId'];c['additionalTopicIds']=['russian-1-0']
        c['sourceMaterial']['kind']='source-question';c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
        c['audioMaterial']=audio
        assert 'answerLanguageRule' not in c
        result.append(c)
    assert len(result)==18 and sum(c['totalMarks'] for c in result)==80
    return result


def language_awareness_one(source):
    r=next(r for r in source['tasks'] if r['unit']=='LA1');body=r['publishedSourceBlock']
    allowance=body[body.index('Award full marks '):body.index('1. Section 1')]
    award='award 2 marks to all (there is no noun in the dative case)'
    assert award in body
    ids=['section1-feminine-instrumental','section1-feminine-dative','section2-reflexive','section2-dative-plural','section3-masculine-genitive','section4-feminine-accusative']
    sections=[1,1,2,2,3,4];criteria=[]
    for id,section,prompt in zip(ids,sections,r['printedPrompts']):
        criterion={'id':id,'label':f'Section {section} — {prompt}','maxMarks':2,'permittedMarks':[0,2],'guidance':[prompt,squash(allowance)]}
        if id=='section2-dative-plural':
            criterion['permittedMarks']=[2];criterion['guidance'].append(award)
            criterion['automaticAward']={'marks':2,'sourceText':award,'schemePages':[5]}
        criteria.append(criterion)
    c=source_card(r);c.pop('rows');c.pop('tariffModel');c['kind']='rubric';c['questionRef']='2010 HL Section LA1'
    c['rubric']={'system':'language-writing','criteria':criteria,'taskRequirements':[squash(allowance),award],
                'markingGuideNote':'Assess the other five examples manually using the printed guidance, including its English-translation and base/dictionary-form allowances. The plural-dative prompt carries the published two-mark award for all candidates, including a blank response. No noun is invented.'}
    return [c]


def split_original_page_quotes(cards):
    # Two original quotations cross verified footer blocks. Retain every word
    # as separately bound page slices instead of weakening source matching.
    boundaries={'ru-2010-hl-c2-3':'Assign no mark for:',
                'ru-2010-hl-gw':'A how you got there'}
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
    cards=reading(source)+culture(source)+summaries(source)+language_awareness_one(source)+language_and_matching(docs,source)+grammar(docs,source)+writing(docs,source)+listening(docs,source)
    source_language_rules(cards,source)
    split_original_page_quotes(cards)
    assert len(cards)==len({c['id'] for c in cards})==38
    assert sum(c['totalMarks'] for c in cards)==300
    city=next(c for c in cards if c['id']=='ru-2010-hl-l1-1-i')
    assert city['tariffModel']['kind']=='questionTotal' and all(row['marks'] is None for row in city['rows'])
    assert sum(c['totalMarks'] for c in cards if c is not city)==296
    assert 'answerLanguageRule' not in next(c for c in cards if c['section']=='LA1')
    for doc in docs.values():doc.close()
    return cards

if __name__=='__main__':save_reviewed(build())
