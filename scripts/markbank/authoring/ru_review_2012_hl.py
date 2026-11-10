"""Russian 2012 Higher source authoring; unsupported numeric cases remain open."""
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

METADATA = {'paper': {'pages': 16, 'sha256': 'b7757711e6c73bd6f4d7648501364cb252d771bce02177a4c52893137c6ff04a'}, 'aural': {'pages': 8, 'sha256': '6391789ba2e09bca4df17e74473f2355d32c0fa11516b9e824bebb82aad8efad'}, 'scheme': {'pages': 28, 'sha256': 'eb369d55edcd65c40ace69eac2206c44ba545ddd0118658364537e5f9ac2e4fe'}}

def source_records():
    docs = {}
    for kind, relative in [('paper', 'papers/2012-hl-000-paper.pdf'),
                           ('aural', 'papers/2012-hl-A00-paper.pdf'),
                           ('scheme', 'schemes/2012-hl.pdf')]:
        path = ROOT / 'examiner-reports/russian' / relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == METADATA[kind]['sha256']
        docs[kind] = fitz.open(path)
    Q, A, S = docs['paper'], docs['aural'], docs['scheme']

    def page(doc, n, right=False):
        # The scheme has content to y771 and a footer beginning at y771: remove
        # the actual footer line instead of clipping away low printed guidance.
        rect = fitz.Rect(295, 30, 580, 793) if right else fitz.Rect(20, 30, 580, 793)
        text = doc[n-1].get_text(clip=rect, sort=False).replace('\uf0b7', '•').replace('\xa0', ' ')
        return re.sub(r'^[^\n]*Lch\s+\d+\s+de\s+\d+[^\n]*Page\s+\d+\s+of\s+\d+[^\n]*\n?', '', text, flags=re.M)

    norm = lambda t: re.sub(r'[^\w]', '', t.casefold())

    def numbered_blocks(text):
        heads=list(re.finditer(r'^\s*(\d)\.\s*(?:(iv|i{1,3})\.?\s*)?(?=[A-Z“])',text,re.M))
        return [(int(h.group(1)),h.group(2),text[h.end():heads[n+1].start() if n+1<len(heads) else len(text)]) for n,h in enumerate(heads)]

    def record(unit, item, roman, question, qp, body, sp, total, **extra):
        component = 'aural' if unit in ('L1', 'L2', 'L3', 'L4') else 'paper'
        assert any(norm(question) in norm(' '.join(page(docs[component], p, right=right) for p in qp))
                   for right in (False, True)), (unit, item, roman, question)
        return dict(id='ru-2012-hl-' + unit.lower() + (f'-{item}' if item is not None else '') + (f'-{roman}' if roman else ''),
                    unit=unit, item=item, roman=roman, question=question, questionPages=qp,
                    component=component, publishedSourceBlock=squash(body), schemePages=sp,
                    publishedTotal=total, **extra)

    cards = []
    source = '\n'.join(page(S, p) for p in (5, 6, 7)).split('Language awareness')[0]
    blocks = numbered_blocks(source)
    asks = [(i,r,question_text(q),p) for p in (3,4)
            for i,r,q in numbered_blocks(page(Q,p,True).split('Language awareness')[0])]
    assert len(blocks) == len(asks) == 8
    totals = [4,6,4,6,4,4,6,8]
    starts = ['assign two marks:', '3 x 2 = 6', '2 x 2 = 4', 'COMPULSORY:', '2 x 2 = 4', '2 x 2 = 4', '3 x 2 = 6', '4 x 2 =8']
    for (i,r,b),(qi,qr,q,p),total,start in zip(blocks,asks,totals,starts):
        assert (i,r)==(qi,qr)
        price = re.search(r'(\d)\s*x\s*(\d)\s*=\s*(\d)', b)
        assert price and int(price.group(3))==total
        cue,body = source_split(b,start)
        assert score(bag(q),bag(cue))>.75,(q,cue)
        cards.append(record('C1',i,r,q,[p],body,[5,6,7],total,
                            pending='Printed two-detail instruction and 2 x 2 = 6 conflict; compulsory mother-feeling reference retained.' if (i,r)==(2,'ii') else ''))
    assert sum(c['publishedTotal'] for c in cards)==42

    summary_source='\n'.join(page(S,p) for p in (9,10)).split('Language awareness')[0]
    blocks=numbered_blocks(summary_source)
    summary_starts=[(6,'Elena visited Cairo'),(6,'Give four details about what Elena'),
                    (7,'Give four details about the exhibits'),(7,'How did Elena spend')]
    assert len(blocks)==4
    for (i,r,b),(p,start) in zip(blocks,summary_starts):
        q=question_text(start+page(Q,p).split(start,1)[1].split('_',1)[0])
        cue,body=source_split(b,'Compulsory:' if i==3 else 'Main points:')
        cue=cue.replace('arrived in','visited').replace('4 details','four details')
        assert score(bag(q),bag(cue))>.75,(q,cue)
        cards.append(record('C2',i,None,q,[p],body,[9,10],10,
                            sourceScoringRoutes=[dict(detail=2,detailQuota=4,discretionaryMaximum=2),dict(detail=2,detailQuota=5,discretionaryMaximum=0)],
                            pending='Preserve alternative four-detail plus discretion OR five-detail routes; accepts Russian. Summary3 requires exhibits and importance.'))

    q='In the paragraph below '+squash(between(page(Q,4,True),'In the paragraph below','(6 marks)'))+' (6 marks)'
    b='Language awareness '+between('\n'.join(page(S,p) for p in (7,8)),'Language awareness','1.3.')
    prompts=['Give an example of a noun in the accusative case','Give an example of a noun in the prepositional case.','Give an example of a noun in the instrumental case']
    for prompt in prompts: assert norm(prompt) in norm(page(Q,4))
    cards.append(record('LA1',None,None,q,[4],b,[7],6,printedPrompts=prompts,
                        scoring=dict(correctExamples=3,perExample=2),pending='No published exemplar pool; source accepts nominative or requested case; instrumental одним earns1.'))
    q='Select two of the words '+question_text(between(page(Q,5,True),'Select two of the words'))
    b='1.3. '+between('\n'.join(page(S,p) for p in (7,8)),'1.3.')
    cards.append(record('CA1',None,None,q,[5],b,[7,8],4,scoring=dict(topics=2,detailsPerTopic=2,perDetail=1),reviewNote='Source accepts answers in both/either language.'))
    q='In the text find five words '+question_text(between(page(Q,8,True),'In the text find five words','1.'))
    b='Q.2.2. '+between(page(S,10),'Q.2.2.','Q.2.3.')
    cards.append(record('LA2',1,None,q,[8],b,[10],5,scoring=dict(correctWords=5,perWord=1),pending='No exemplar pool printed; nouns/verbs/adjectives and text/dictionary forms allowed; movement on foot excluded.'))
    q=('Verbs: '+question_text(between(page(Q,8,True),'Verbs:'))).split('1.',1)[0].strip()
    infinitive_prompts=['хотели','нашли','лежали','казался','стояла']
    assert all(norm(word) in norm(page(Q,8)) for word in infinitive_prompts)
    b='Verbs: '+between(page(S,11),'Verbs:','Q.3')
    cards.append(record('LA2',2,None,q,[8],b,[11],5,printedVerbs=infinitive_prompts,scoring=dict(correctInfinitives=5,perInfinitive=1)))
    q='The following questions '+squash(between(page(Q,9,True),'The following questions'))
    q=q[:q.index('(20 marks)')+len('(20 marks)')]
    rows=[]
    for p in (11,12): rows.extend([[squash(v or '') for v in row] for row in S[p-1].find_tables().tables[0].extract()])
    # The final line of answer9 continues onto the next scheme page.
    assert len(rows)==11 and rows[9][0]==''
    rows[8][1]+=' '+rows[9][1];rows.pop(9)
    assert [re.findall(r'\d+',r[0]) for r in rows]==[['4','6','9'],['8'],['4','6','9'],['7'],['10'],['5'],['4','6','9'],['2'],['1'],['3']],rows
    b='Q.3 '+between(page(S,11),'Q.3')+'\n'+page(S,12)
    cards.append(record('SD',None,None,q,[9],b,[11,12],20,sourcePages=[9,10],answerRows=rows,scoring=dict(correctAnswers=10,perAnswer=2),reviewNote='Do not penalize the same number twice; no unique-use constraint.'))
    q='Read through the following text. '+squash(between(page(Q,11,True),'Read through the following text.'))
    q=q[:q.index('substitute words.')+len('substitute words.')]
    cards.append(record('GR',None,None,q,[11],page(S,13),[13],30,scoring=dict(correctForms=15,perForm=2)))
    q='Write a short essay '+squash(between(page(Q,12,True),'Write a short essay'))
    q=q[:q.index('(30 marks)')+len('(30 marks)')]
    cards.append(record('SE',None,None,q,[12],'\n'.join(page(S,p) for p in (14,15)),[14,15],30,fullQuestionPage=page(Q,12),
                        pending='Shared conditional Lower A range9–14; all six topic choices retained.'))
    q='Write a piece '+question_text(page(Q,13,True).split('Write a piece',1)[1])
    cards.append(record('GW',None,None,q,[13],'\n'.join(page(S,p) for p in (16,17,18,19)),[16,17,18,19],40,
                        pending='Shared conditional Lower A range7–12; source middle9–11 overlaps11–12 and differs from prose9/10. All four choices preserved; holiday tense differs between paper and scheme.'))
    assert len(cards)==20 and sum(c['publishedTotal'] for c in cards)==222

    source='\n'.join(page(S,p) for p in range(20,27))
    heads=list(re.finditer(r'^\s*SECTION (IV|III|II|I)\b[^\n]*$',source,re.M))
    assert len(heads)==4
    counts=[[2,2,2,2,2],[2,3,2,3],[1,2,2,2,1,2],[2,2,2,2,2]]
    starts=[['64th festival','450 excursions','Festival will open','Lived and worked','Several million people'],
            ['25th of April','First album was','Formed in 1999','Assign 2 marks'],
            ['Tipperary','She started late','7 years','RTE Concert','Lack of time','Traditional +'],
            ['Played violin','Chooses the path','Wrote songs','Evening Jazz','Left medicine']]
    topics=[['russian-0-7','russian-0-7','russian-0-7','russian-0-4','russian-2-12'],
            ['russian-0-7','russian-0-4','russian-0-4','russian-0-7'],
            ['russian-0-2','russian-0-1','russian-0-3','russian-0-4','russian-0-4','russian-0-5'],
            ['russian-0-5','russian-0-3','russian-0-5','russian-0-3','russian-0-4']]
    for n,h in enumerate(heads):
        section=n+1;b=source[h.end():heads[n+1].start() if n+1<len(heads) else len(source)]
        blocks=numbered_blocks(b)
        asks=[(i,r,question_text(q)) for i,r,q in numbered_blocks(page(A,section+1,True))]
        assert len(blocks)==len(asks)==len(counts[n]),section
        for (i,r,b),(qi,qr,q),count,start,topic in zip(blocks,asks,counts[n],starts[n],topics[n]):
            assert (i,r)==(qi,qr)
            cue,body=source_split(b,start)
            assert score(bag(q),bag(cue.replace('Máiréad','Mairéad').replace('Mairead','Mairéad').replace('greatest','biggest')))>.65,(q,cue)
            sp=[21,22,23] if section==1 else [24] if section==2 else [25] if section==3 else [26]
            cards.append(record(f'L{section}',i,r,q,[section+1],body,sp,count*2,detailQuota=count,topicId=topic,
                                pending='Explicit category compensation: venue/time/price2 each; one category1 permits another3. No invented atom tariffs.' if (section,i)==(2,4) else ''))
    assert len(cards)==40 and sum(c['publishedTotal'] for c in cards)==302
    assert len({c['id'] for c in cards})==40
    for c in cards:
        assert norm(c['publishedSourceBlock']) in norm('\n'.join(page(S,p) for p in c['schemePages'])),c['id']
    draft=dict(status='Source-only draft; not runtime cards or a completed sitting',sources=METADATA,
               independentTasks=40,writtenTasks=20,listeningTasks=20,printedExamTotal=300,sourceLeafTotal=302,
               aggregateDiscrepancy='C1Q2ii explicitly prints2x2=6 although the question asks two details; reading leaf42 versus heading40, unresolved.',
               generalWrittenGuidance=squash('\n'.join(page(S,p) for p in (3,4))),
               comprehensionGuidance=squash('\n'.join(page(S,p) for p in (5,)).split('1.i.')[0]),
               summaryGuidance=squash(summary_source[:re.search(r'^\s*1\.\s+[A-Z]',summary_source,re.M).start()]),
               listeningGuidance=squash(source[:heads[0].start()]),tasks=cards)
    return docs,draft

from ru_review_2026_hl import base as common_base,as_points,save_reviewed,mark_range
from ru_review_2017_hl import options,named_group,band

def base(*args,**kwargs):
    c=common_base(*args,**kwargs)
    for key in ('id','questionRef'):c[key]=c[key].replace('2026','2012')
    c['year']=2012;c['sourceMaterial']['title']=c['sourceMaterial']['title'].replace('2026','2012');return c

def source_card(r):
    pages=r.get('sourcePages') or ([2,3,4] if r['unit']=='C1' else [6,7,8] if r['unit'] in ('C2','LA2') else r['questionPages'])
    c=base(r['unit'],r['question'],r['publishedTotal'],pages,r['schemePages'],r['item'],r['roman']);c['review']['questionPages']=r['questionPages'];return c

def reading(source):
    result=[]
    for r in source['tasks']:
        if r['unit']!='C1' or (r['item'],r['roman'])==(2,'ii'):continue
        key=(r['item'],r['roman']);body=r['publishedSourceBlock'];count=r['publishedTotal']//2
        c=source_card(r);c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
        c['rubric']={'system':'language-points','count':count,'groups':[
            {'id':f'detail-{n}','label':f'Distinct detail {n}','rows':[],
             'criteria':[{'id':f'detail-{n}','label':f'Distinct detail {n}','maxMarks':2,'permittedMarks':[0,1,2],'guidance':[body]}]} for n in range(1,count+1)],
            'taskRequirements':[source['comprehensionGuidance'],body],
            'markingGuideNote':'Assess each different actual detail once against the complete published full, partial and zero-credit guidance. Do not infer a unique full/partial association from list position or count a paraphrase as a second fact.'}
        if key==(1,'i'):
            c['rubric']['markingGuideNote']+=' The scheme lists “(other) furniture” among full-credit details and “furniture” as a one-mark partial. Both literal instructions remain above; the generic word alone must not automatically receive two marks.'
        elif key==(1,'ii'):
            rule='Answers must refer to how both girls felt. Candidates who reply in relation to one cannot obtain full marks.'
            assert rule in body
            c['rubric']['allocationCap']={'maxMarks':6,'sourceText':'3 x 2 = 6','schemePages':[5],
                'limits':[{'id':'missing-both-girls','maxMarks':5,'when':{'flag':'missing-both-girls','prompt':'The response refers to only one girl’s feelings.'},'sourceText':rule,'schemePages':[5]}]}
            c['rubric']['markingGuideNote']+=' Include the feelings of BOTH girls. The source prohibits full marks for a response about only one girl. On this whole-mark scale, the derived upper limit is therefore five out of six; five is not a printed award or a fixed one-mark deduction. Lower earned totals and zero remain unchanged.'
        c['review']['guidancePages']=[5];result.append(c)
    assert len(result)==7 and sum(c['totalMarks'] for c in result)==36
    return result

def summaries(source):
    result=[];general=source['summaryGuidance']
    incomplete=between(general,'If a candidate fails','OR –')
    incomplete='If a candidate fails'+incomplete
    alternatives=general[general.index('Award 2 marks for each of 4 details'):]
    for r in source['tasks']:
        if r['unit']!='C2':continue
        c=source_card(r);c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
        body=r['publishedSourceBlock']
        groups=[]
        for route,count,label in [('standard',4,'Four details plus discretionary marks'),('five-details',5,'Five details without discretionary marks')]:
            criteria=[{'id':f'{route}-detail-{n}','label':f'Distinct detail {n}','maxMarks':2,'permittedMarks':[0,1,2],
                       'guidance':[body,general]} for n in range(1,count+1)]
            if route=='standard':
                criteria.append({'id':'standard-discretion','label':'Discretionary marks','maxMarks':2,'permittedMarks':[0,1,2],
                                 'guidance':[general],
                                 'limits':[{'id':'standard-incomplete','maxMarks':1,'when':{'any':[{'flag':'standard-incomplete','prompt':incomplete}]},'guidance':[incomplete]}]})
            groups.append({'id':route,'label':label,'alternativeSet':'summary-route','rows':[],'criteria':criteria})
        c['rubric']={'system':'language-points','count':1,'groups':groups,
                    'alternativeSets':[{'id':'summary-route','label':'Printed alternative scoring routes','sourceText':alternatives,'schemePages':[9]}],
                    'taskRequirements':[general,body],
                    'markingGuideNote':'Choose one of the two complete printed routes. Four distinct details can earn eight content marks plus two discretionary marks; alternatively, five distinct details can earn ten without discretion. Do not combine the routes or count the same actual detail twice. The partial mark follows the printed intelligibility rule, including the question-specific partial where present. Russian answers are explicitly not penalised.'}
        if r['item']==3:
            c['rubric']['markingGuideNote']+=' Refer to BOTH the exhibits and their importance. The source provides no separate numeric allocation per category; its incomplete-response limit applies to discretion in the four-detail route.'
        c['review']['guidancePages']=[9];result.append(c)
    assert len(result)==4
    return result

def language_and_matching(docs,source):
    result=[]
    for r in source['tasks']:
        unit=r['unit'];body=r['publishedSourceBlock']
        if unit not in ('LA1','CA1','LA2','SD'):continue
        c=source_card(r)
        if unit=='LA1':
            c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
            c['questionText']+='\n\n'+'\n'.join(r['printedPrompts'])
            c['rubric']={'system':'language-writing','criteria':[
                {'id':case,'label':prompt,'maxMarks':2,'permittedMarks':[0,1,2] if case=='instrumental' else [0,2],'guidance':[body]}
                for case,prompt in zip(('accusative','prepositional','instrumental'),r['printedPrompts'])],
                'taskRequirements':[body],
                'markingGuideNote':'Supply three examples from the original paragraph. The source permits the nominative form or requested case and explicitly gives one mark for одним in the instrumental task. It provides no full-credit exemplar pool; no example nouns are invented.'}
        elif unit=='CA1':
            topics=[squash(x) for x in re.split(r'\s[1-4]\.\s+',body)[1:]];assert topics==['электричка','дача','Арбат','метро']
            c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
            c['rubric']={'system':'language-points','count':2,'groups':[
                {'id':f'topic-{n}','label':topic,'rows':[],
                 'criteria':[{'id':f'topic-{n}-detail-{j}','label':f'Distinct detail {j}','maxMarks':1,'permittedMarks':[0,1],'guidance':['assign 1 mark for each relevant detail;']} for j in (1,2)]} for n,topic in enumerate(topics,1)],
                'taskRequirements':[body],
                'markingGuideNote':'Choose two of the four original topics and give two distinct details for each. The English column asks for English; the Irish column asks for Irish. The scheme additionally says “Accept answers in both/either language” without naming the pair. That literal exception is retained; no additional named language list or automatic penalty is inferred.'}
        elif unit=='LA2' and r['item']==1:
            c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
            c['rubric']={'system':'language-writing','criteria':[{'id':f'word-{n}','label':f'Different word {n}','maxMarks':1,'permittedMarks':[0,1],'guidance':[body]} for n in range(1,6)],
                'taskRequirements':[body],
                'markingGuideNote':'Assess five different words from the original passage. Nouns, verbs and adjectives are allowed in the text or dictionary form, but references to movement on foot receive no marks. The scheme prints no exemplar list; no words are invented.'}
        elif unit=='LA2':
            entries=[squash(x) for x in re.split(r'\s[1-5]\.\s+',body)[1:]];assert len(entries)==5
            pairs=[tuple(re.split(r'\s*[-–]\s*',entry,1)) for entry in entries]
            assert [prompt for prompt,answer in pairs]==r['printedVerbs']
            c['questionText']+='\n\n'+'\n'.join(f'{n}. {word}' for n,word in enumerate(r['printedVerbs'],1))
            answers=[answer.split(' (',1)[0] for prompt,answer in pairs]
            assert answers==['хотеть','найти','лежать','казаться','стоять']
            c=as_points(c,answers,5)
            for g,(prompt,answer) in zip(c['rubric']['groups'],pairs):g['label']=prompt;g['rows'][0]['marks']=1
            c['rubric']['taskRequirements']=[body.split('1.',1)[0],'penalise for наити instead of найти']
        else:
            rows=r['answerRows'];c=as_points(c,[numbers for numbers,text in rows],10)
            for g,(numbers,text) in zip(c['rubric']['groups'],rows):
                g['label']=text;g['rows']=[{'id':f'option-{n}','text':number,'marks':2} for n,number in enumerate(re.findall(r'\d+',numbers),1)]
            c['rubric']['taskRequirements']=[body.split('4 /',1)[0]]
            c['rubric']['markingGuideNote']='Each row retains all original accepted numbers. The source explicitly permits using the same number twice; do not impose a unique-use restriction or pair rows into invented complete routes.'
        result.append(c)
    assert len(result)==5
    return result

def grammar_forms(docs):
    paper=docs['paper'][10].get_text();paper=paper[paper.index('29 июня'):]
    solved=docs['scheme'][12].get_text();solved=solved[solved.index('29 июня'):]
    gaps=list(re.finditer(r'[.\u2026]+\s*\(([^)]+)\)',paper));assert len(gaps)==15
    fixed=lambda words:r'[^\w]*'.join(re.escape(word) for word in words)
    result=[]
    for n,gap in enumerate(gaps):
        before=paper[gaps[n-1].end() if n else 0:gap.start()];after=paper[gap.end():gaps[n+1].start() if n+1<len(gaps) else len(paper)]
        left=re.findall(r'\w+',before)[-3:];right=re.findall(r'\w+',after)[:3]
        pattern=fixed(left)+r'[^\w]+(\w+(?:\s*/\s*\w+)*)'+(r'[^\w]+'+fixed(right) if right else r'[^\w]*$')
        matches=re.findall(pattern,solved,re.I);assert len(matches)==1,(n,left,right,matches)
        result.append((gap[1],squash(matches[0])))
    assert [a for q,a in result]==['июля','поздравил/ поздравлял / поздравляет','надежду','университетом','научную','знаний','учителях','руках','страны','пожелал','университет','отличников','факультета','музыкальных','фоне']
    return result

def grammar(docs,source):
    r=next(r for r in source['tasks'] if r['unit']=='GR');pairs=grammar_forms(docs)
    c=as_points(source_card(r),[a for q,a in pairs],15)
    for n,(g,(q,a)) in enumerate(zip(c['rubric']['groups'],pairs),1):g['label']=f'{n}. {q}'
    c['rubric']['taskRequirements']=[r['publishedSourceBlock'].split('29 июня')[0]]
    c['rubric']['markingGuideNote']='Each original gap earns two marks only for an accepted correct form. The source gives no capitalization partial mark this year. All three printed congratulation forms are accepted in the same gap, and the two университет prompts retain their separate context-bound forms.'
    return [c]

def writing(docs, source, base):
    S=docs['scheme']; result=[]
    for unit,sp,table_page in [('SE',14,15),('GW',16,18)]:
        record=next(c for c in source['tasks'] if c['unit']==unit)
        text='\n'.join(re.sub(r'^.*Lch\s+\d+\s+de\s+\d+.*Page\s+\d+\s+of\s+\d+.*$', '', S[n-1].get_text(sort=True), flags=re.M) for n in ([14] if unit=='SE' else [16,17]))
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
            assert all(f'{n}.' in choices for n in range(1,7))
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
            guide=text
            instructions=between(guide,'1. NARRATIVE','2. Expression (E):')
            instructions='1. NARRATIVE '+instructions
            c['rubric']['taskRequirements']=[squash(instructions),squash(re.search(r'If a candidate answers.*?one\(s\)\.',guide,re.S).group())]
            c['rubric']['markingGuideNote']+=' The holiday blog prompt uses present-tense requirements in the original paper but past-tense requirements in the scheme. Both original versions are retained; no tense instruction is silently substituted.'
        result.append(c)
    return result

def listening(docs,source):
    result=[];audio=next(r['source'] for r in json.loads((ROOT/'data/russianAudio.json').read_text()) if r['year']==2012)
    for r in source['tasks']:
        if r['unit'] not in ('L1','L2','L3','L4'):continue
        key=(r['unit'],r['item'],r['roman']);body=r['publishedSourceBlock'];count=r['publishedTotal']//2
        manual=key in [('L1',1,None),('L1',3,'i'),('L1',3,'ii'),('L2',1,None),('L2',2,None),('L2',3,None)]
        if key==('L2',4,None):
            c=source_card(r);c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
            rule=body[:body.index('Starts at')].strip()
            c['rubric']={'system':'language-points','count':3,'groups':[
                {'id':category,'label':category.title(),'answerCount':1,'rows':[{'id':'response','text':body,'marks':3,'steps':[0,1,2,3]}]} for category in ('venue','time','price')],
                'allocationCap':{'maxMarks':6,'sourceText':rule,'schemePages':[24],
                                 'categoryCompensation':{'normalMarks':2,'reducedMarks':1,'increasedMarks':3}},
                'taskRequirements':[body],
                'markingGuideNote':'Assess the three named categories against the complete original pool. The normal maximum is two per category. Three is available for a category only when another category receives exactly one, within six overall. No per-word or per-line allocation is inferred from the pool. The printed discount-ticket partial remains visible.'}
        elif manual:
            c=source_card(r);c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
            c['rubric']={'system':'language-points','count':count,'groups':[
                {'id':f'detail-{n}','label':f'Distinct response {n}','rows':[],
                 'criteria':[{'id':f'detail-{n}','label':f'Distinct response {n}','maxMarks':2,'permittedMarks':[0,1,2],'guidance':[body]}]} for n in range(1,count+1)],
                'taskRequirements':[body],
                'markingGuideNote':'Assess different actual responses against the full printed pool. One mark is available only for a named source partial, not a new general partial tariff. Do not award the full and partial versions of the same information twice. Every source zero-credit direction remains above.'}
            if key==('L2',2,None):
                c['rubric']['markingGuideNote']+=' Each bracketed award or documentary entry requires its stated two components for a full two-mark response; do not turn the inner words into separately priced full answers. The bare age is explicitly worth zero; the complete career-stage wording is retained.'
        else:
            c=as_points(source_card(r),options(body),count)
        c['rubric']['taskRequirements']=[source['listeningGuidance']]+c['rubric']['taskRequirements']
        c['rubric']['markingGuideNote']+=' The scheme’s general language rule explicitly exempts listening from wrong-language penalties.'
        c['review']['guidancePages']=[3,20];c['topicId']=r['topicId'];c['additionalTopicIds']=['russian-1-0']
        c['sourceMaterial']['kind']='source-question';c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
        c['audioMaterial']=audio;result.append(c)
    assert len(result)==20 and sum(c['totalMarks'] for c in result)==80
    return result

def source_language_rules(cards,source):
    rule='Language of answer: '+between(source['generalWrittenGuidance'],'Language of answer:','When it should be Russian: award NO marks')+' When it should be Russian: award NO marks'
    for c in cards:
        if c['section'] not in ('C1','LA1','LA2','GR','SE','GW'):continue
        c['answerLanguageRule']={'otherLanguageMultiplier':0,'sourceText':squash(rule),'schemePages':[3]}
        if c['section']=='C1':c['rubric']['markingGuideNote']+=' Answer in English or Irish. Both languages are permitted by the original bilingual paper.'


def split_original_page_quotes(cards):
    # These literal passages cross bilingual footer blocks in the original
    # PDF text stream. Keep contiguous source quotations on either side of
    # each verified page boundary; never remove words to make a claim pass.
    boundaries={
        'ru-2012-hl-c1-2-i':'assign two marks:',  # price on p5, pool on p6
        'ru-2012-hl-c2-2':'(the small) tomb/burial chamber',  # p9 to p10
        'ru-2012-hl-ca1':'2. дача',  # p7 to p8
        'ru-2012-hl-gw':'Interview someone you admire.',  # p16 to p17
    }
    def walk(value,marker):
        if isinstance(value,dict):
            for key,child in value.items():
                if key in ('guidance','taskRequirements'):
                    split=[]
                    for text in child:
                        if marker in text and text.index(marker)>0:
                            at=text.index(marker);parts=[text[:at].strip(),text[at:].strip()]
                            assert squash(' '.join(parts))==squash(text)
                            split.extend(parts)
                        else:split.append(text)
                    value[key]=split
                else:walk(child,marker)
        elif isinstance(value,list):
            for child in value:walk(child,marker)
    for card in cards:
        if card['id'] in boundaries:walk(card['rubric'],boundaries[card['id']])

def build():
    docs,source=source_records()
    cards=reading(source)+summaries(source)+language_and_matching(docs,source)+grammar(docs,source)+writing(docs,source,base)+listening(docs,source)
    source_language_rules(cards,source)
    split_original_page_quotes(cards)
    assert len(cards)==39 and len({c['id'] for c in cards})==39
    assert sum(c['totalMarks'] for c in cards)==296
    assert sum(bool(c.get('answerLanguageRule')) for c in cards)==13
    assert not any(c['id']=='ru-2012-hl-c1-2-ii' for c in cards)
    for doc in docs.values():doc.close()
    return cards

if __name__=='__main__':save_reviewed(build())
