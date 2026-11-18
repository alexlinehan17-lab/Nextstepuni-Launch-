"""Russian 2021 Higher: pinned originals, complete source tasks and literal rules."""
from pathlib import Path
import hashlib,json,re,sys
import fitz
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts/markbank/authoring'))
from ru_review_2015_ol import question_text,source_split
from ru_review_2026_hl import squash,between
from ru_paper import bag,score
METADATA={'paper': {'pages': 16, 'sha256': 'cc1ccca7e039ac3d38af858cdf842bd549c42183c392684f368e67cc952cca22'}, 'aural': {'pages': 8, 'sha256': 'b635aff4288709c732cc1cdc18e891ab13517d8ee21643f8578ff363266b5bf4'}, 'scheme': {'pages': 28, 'sha256': '7339c36919457d79424b100fb782372daf99d8c790dbe26ca5d69900779d3b41'}}

def summary_tariff(document, number):
    """Bind the printed right-margin tariff to its own numbered source region.

    The PDF content stream emits some tariffs before the next heading. Geometry,
    rather than extraction order, establishes the original question association.
    """
    assert number in (1,2,3,4)
    physical={1:7,2:8,3:8,4:9}[number]
    page=document[physical-1];words=page.get_text('words')
    heads=[w for w in words if w[0]<90 and w[4] in ('1.','2.','3.','4.')]
    selected=[w for w in heads if w[4]==f'{number}.'];assert len(selected)==1
    heading=selected[0]
    later=[w[1] for w in heads if w[1]>heading[1]]
    bottom=min(later) if later else page.rect.height
    tens=[w for w in words if w[0]>450 and w[4]=='10' and heading[1]-1<=w[1]<bottom]
    assert len(tens)==1,(number,tens)
    ten=tens[0]
    labels=[w for w in words if w[4]=='marks' and abs(w[1]-ten[1])<1 and 0<w[0]-ten[2]<10]
    assert len(labels)==1,(number,labels)
    return {'text':'10 marks','schemePage':physical,'questionNumber':number,
            'headingBox':list(heading[:4]),'tariffBoxes':[list(ten[:4]),list(labels[0][:4])]}

def source_records():
    docs={}
    for kind,relative in [('paper','papers/2021-hl-000-paper.pdf'),('aural','papers/2021-hl-A00-paper.pdf'),('scheme','schemes/2021-hl.pdf')]:
        path=ROOT/'examiner-reports/russian'/relative
        assert hashlib.sha256(path.read_bytes()).hexdigest()==METADATA[kind]['sha256']
        docs[kind]=fitz.open(path);assert len(docs[kind])==METADATA[kind]['pages']
    Q,A,S=docs['paper'],docs['aural'],docs['scheme']
    def page(doc,n,right=False):
        rect=fitz.Rect(295,30,580,793) if right else fitz.Rect(20,30,580,793)
        text=doc[n-1].get_text(clip=rect,sort=False).replace('\uf0b7','•').replace('\xa0',' ')
        if doc is S:text=re.sub(r'^\s*'+str(n)+r'\s*\n','',text,count=1)
        return text
    norm=lambda text:re.sub(r'[^\w]','',text.casefold())
    def numbered(text):
        heads=list(re.finditer(r'^\s*(\d)\.\s*(?:\(?((?:iv|i{1,3}))\)?\.?\s*)?(?=[A-Z“])',text,re.M))
        return [(int(h.group(1)),h.group(2),text[h.end():heads[i+1].start() if i+1<len(heads) else len(text)]) for i,h in enumerate(heads)]
    def record(unit,item,roman,question,qp,body,sp,total,**extra):
        component='aural' if unit in ('L1','L2','L3','L4') else 'paper'
        assert any(norm(question) in norm(' '.join(page(docs[component],p,right) for p in qp)) for right in (False,True)),(unit,item,roman,question)
        assert norm(body) in norm(' '.join(page(S,p) for p in sp)),(unit,item,roman,body)
        return dict(id='ru-2021-hl-'+unit.lower()+(f'-{item}' if item is not None else '')+(f'-{roman}' if roman else ''),unit=unit,item=item,roman=roman,question=question,questionPages=qp,component=component,publishedSourceBlock=squash(body),schemePages=sp,publishedTotal=total,**extra)
    records=[]
    comprehension='\n'.join(page(S,p) for p in (4,5));blocks=numbered(comprehension)
    asks=[(i,r,question_text(q),p) for p in (3,4) for i,r,q in numbered(page(Q,p,True))]
    assert len(blocks)==len(asks)==9
    for (i,r,b),(qi,qr,q,p),total in zip(blocks,asks,[4,4,6,4,6,4,4,4,4]):
        assert (i,r)==(qi,qr)
        price=re.search(r'(\d)\s*x\s*2\s*marks',b);assert price and int(price.group(1))*2==total
        cue,body=b[:price.start()],b[price.start():]
        assert score(bag(q),bag(cue))>.7,(q,cue)
        records.append(record('C1',i,r,q,[p],body,[4,5],total,requiredNamedPools=['advantage','disadvantage'] if (i,r)==(3,'iii') else []))
    assert sum(r['publishedTotal'] for r in records)==40
    language=page(S,6)
    q='Indicate the case '+squash(between(page(Q,5,True),'Indicate the case')).split(':')[0]+':'
    body=language.split('\nOR\n')[0] if '\nOR\n' in language else language.split('OR')[0]
    records.append(record('LA1',None,None,q,[5],body,[6],10,reviewNote='Five source case responses at2; retain the original legacy identity.'))
    q='In the text find ten words '+squash(between(page(Q,5,True),'In the text find ten words'))
    q=q[:q.index('them in Russian.')+len('them in Russian.')]
    body='Q. 1.3'+between(language,'Q. 1.3')
    entries=[squash(entry) for entry in re.findall(r'^\s*\d+\.\s*([^\n]+)',body,re.M)];assert len(entries)==22 and entries[4]==entries[9]=='синтезатор',entries
    assert len(dict.fromkeys(entries))==21
    records.append(record('CA1',None,None,q,[5],body,[6],10,publishedEntries=entries,distinctOptions=list(dict.fromkeys(entries)),topicId='russian-2-0',additionalTopicIds=['russian-1-1','russian-0-5'],reviewNote='All22 literal entries retained; duplicate синтезатор at5/10 creates one claimable word only. Music content with original Cultural Awareness heading/identity retained. YouTube earns0 as printed.'))
    summary='\n'.join(page(S,p) for p in (7,8,9));blocks=numbered(summary);assert len(blocks)==4
    for i,r,b in blocks:
        qp={1:6,2:7,3:8,4:8}[i];sp={1:[7,8],2:[8],3:[8,9],4:[9]}[i]
        paper_asks=[(n,rr,question_text(q)) for n,rr,q in numbered(page(Q,qp,True))]
        matches=[q for n,rr,q in paper_asks if n==i and rr is None];assert len(matches)==1,(i,paper_asks)
        q=matches[0];tariff=summary_tariff(S,i)
        b=re.sub(r'^\s*10\s+marks\s*$', '', b, flags=re.M)
        cue,body=source_split(b,'Main points:')
        # The first source cue also prints the full-marks condition. Bind the
        # complete question verbatim, rather than dilute its match with that rule.
        assert norm(q) in norm(cue),(q,cue)
        clean_page=lambda n:re.sub(r'^\s*10\s+marks\s*$', '', page(S,n), flags=re.M)
        before=lambda text,n:re.split(r'^\s*'+str(n)+r'\.\s+(?=[A-Z])',text,maxsplit=1,flags=re.M)[0]
        if i==1:chunks=['Main points:'+between(clean_page(7),'Main points:'),before(clean_page(8),2)]
        elif i==3:chunks=['Main points:'+clean_page(8).rsplit('Main points:',1)[1],before(clean_page(9),4)]
        else:chunks=[body]
        assert squash(' '.join(chunks))==squash(body),(i,chunks,body)
        records.append(record('C2',i,None,q,[qp],body,sp,10,sourcePageBlocks=[squash(chunk) for chunk in chunks],printedTariffSource=tariff['text'],printedTariffEvidence=tariff,scoring={'detail':2,'detailQuota':4,'partialDetail':1,'discretionaryMaximum':2,'incompleteDiscretionaryMaximum':1},requiredFullMarksCondition=squash(between(b,'For full marks','Main points:')) if i==1 else None,reviewNote='Main/secondary continuation pages retained; partial1 means intelligible partial, not a universal secondary-detail tariff.'))
    language=page(S,10);qpage=page(Q,9,True)
    q='Supply the infinitive/dictionary '+squash(between(qpage,'Supply the infinitive/dictionary'))
    q=q[:q.index('verbs from the text.')+len('verbs from the text.')]
    body=language.split('OR')[0]
    records.append(record('LA2',None,'i',q,[9],body,[10],10,reviewNote='Both literal clauses preserved: Irish/English/Russian allowed, English phrase translations not credited. No automatic language multiplier or invented translations.'))
    q='Match the words, '+squash(between(qpage,'Match the words,'));q=q[:q.index('table entitled WORDS.')+len('table entitled WORDS.')]
    body='Q.2.2(ii)'+between(language,'Q.2.2(ii)')
    records.append(record('LA2',None,'ii',q,[9],body,[10],10,reviewNote='English Q.2.2(ii), Irish second task C.2.2(i) repeats first marker. Preserve one existing ru-2021-hl-la2-ii identity, no duplicate ask.'))
    q='Read the following paragraphs '+squash(between(page(Q,10,True),'Read the following paragraphs'))
    q=q[:q.index('left-hand column.')+len('left-hand column.')]
    records.append(record('SD',None,None,q,[10],page(S,11),[11],20,expectedAnswerOrder=[8,10,4,7,9,2,6,5,3,1]))
    q='Read through the following text. '+question_text(between(page(Q,11,True),'Read through the following text.'));q=q[:q.index('substitute words.')+len('substitute words.')]
    records.append(record('GR',None,None,q,[11],page(S,12),[12],30,reviewNote='Thirteen bracketed prompts/fifteen separately priced forms; first printed past/present pair remains one answer. Bold/underlined original spans need guarded extraction.'))
    q='Write a short essay '+squash(between(page(Q,12,True),'Write a short essay'));q=q[:q.index('essay title.')+len('essay title.')]
    records.append(record('SE',None,None,q,[12],'\n'.join(page(S,p) for p in (13,14,15)),[13,14,15],30,fullQuestionPage=page(Q,12),sourcePageBlocks=[squash(page(S,p)) for p in (13,14,15)],reviewNote='Printed content10/expression20 rubric. Five choices and every printed direction retained; literal Deduct1/2marks is shown without an inferred automatic deduction.'))
    q='Write a piece '+question_text(between(page(Q,13,True),'Write a piece'))
    records.append(record('GW',None,None,q,[13],'\n'.join(page(S,p) for p in (16,17,18)),[16,17,18],40,sourcePageBlocks=[squash(page(S,p)) for p in (16,17,18)],reviewNote='Six actual alternatives; C15/E15/TC10. Explicit deduction2. Literal overlapping LowerA table kept, no normalized descriptor boundary.'))
    assert len(records)==21 and sum(r['publishedTotal'] for r in records)==240
    source='\n'.join(page(S,p) for p in (19,20,21,22))
    counts=[[3,3,2,2],[2,1,2,1,2,2],[1,2,1,3,1,1],[2,2,3,3]]
    tariffs=[[2]*4,[2]*6,[2,2,4,2,2,2],[2]*4]
    question_pages=[[(2,1,None),(2,2,None),(2,3,None),(2,4,None)],[(3,1,'i'),(3,1,'ii'),(3,2,'i'),(3,2,'ii'),(3,3,None),(3,4,None)],[(4,1,'i'),(4,1,'ii'),(4,2,None),(5,3,'i'),(5,3,'ii'),(5,4,None)],[(6,1,'i'),(6,1,'ii'),(6,2,None),(7,3,None)]]
    for section in range(1,5):
        sp=section+18;body=page(S,sp);blocks=numbered(body)
        assert len(blocks)==len(counts[section-1]),(section,blocks)
        for (i,r,b),(qp,qi,qr),count,tariff in zip(blocks,question_pages[section-1],counts[section-1],tariffs[section-1]):
            assert (i,r)==(qi,qr)
            matches=[question_text(q) for n,rr,q in numbered(page(A,qp,True)) if (n,rr)==(i,r)];assert len(matches)==1,(section,i,r,matches)
            q=matches[0];price=re.search(r'(\d)\s*x\s*(\d)\s*marks',b);assert price and (int(price.group(1)),int(price.group(2)))==(count,tariff)
            cue=b[:price.start()];pool=b[price.start():]
            assert score(bag(q),bag(cue))>.6,(q,cue)
            records.append(record(f'L{section}',i,r,q,[qp],pool,[sp],count*tariff,printedDetailQuota=count,printedDetailMarks=tariff,reviewNote='Russian answers explicitly accepted; no inherited written-language penalty.'))
        assert sum(r['publishedTotal'] for r in records if r['unit']==f'L{section}')==20
    assert len(records)==41 and len({r['id'] for r in records})==41
    return docs,dict(status='Unpublished source proposal; parser not yet run or verified',sources=METADATA,independentTasks=41,writtenTasks=21,listeningTasks=20,allAlternativePracticeTotal=320,selectedExamTotal=250,selectedWrittenTotal=170,listeningTotal=80,generalWrittenGuidance=squash(page(S,3)),comprehensionGuidance=squash(comprehension[:re.search(r'^\s*1\.\s*\(i\)',comprehension,re.M).start()]),summaryGuidance=squash(summary[:re.search(r'^\s*1\.\s*[A-Z]',summary,re.M).start()]),listeningGuidance=squash(page(S,19).split('SECTION I')[0]),tasks=records)


def grammar_forms(document):
    spans=[span for block in document[11].get_text('dict')['blocks'] if 'lines' in block
           for line in block['lines'] for span in line['spans']
           if span['flags']&16 and re.search('[А-Яа-яЁё]',span['text'])]
    assert len(spans)==13 and {span['font'] for span in spans}=={'Calibri,Bold'}
    forms=[]
    for span in spans:
        text=span['text'].strip()
        forms.extend([text] if '/' in text else text.split())
    assert forms==['увлекалась/увлекается','искусством','получила','её','новым','учебном','заведении','могла','соревнованиях','международной','арене','кулинарией','любимому','друзьями','своей'],forms
    return forms


# Unpublished builder scaffold. Combine with source_records.py.proposal only
# after the original parser passes. No runtime/authored writes are invoked here.
from ru_review_2026_hl import base as common_base, as_points, save_reviewed


def base(*args, **kwargs):
    c=common_base(*args, **kwargs)
    for key in ('id','questionRef'):c[key]=c[key].replace('2026','2021')
    c['year']=2021;c['sourceMaterial']['title']=c['sourceMaterial']['title'].replace('2026','2021')
    return c


def source_card(r):
    pages={'C1':[2,3,4],'LA1':[2,3,4,5],'CA1':[2,3,4,5],'C2':[6,7,8],'LA2':[6,7,8,9],'GR':[11]}.get(r['unit'],r['questionPages'])
    c=base(r['unit'],r['question'],r['publishedTotal'],pages,r['schemePages'],r['item'],r['roman'])
    c['review']['questionPages']=r['questionPages'];return c


def summaries(source):
    result=[];general=source['summaryGuidance']
    incomplete=re.search(r'If a candidate fails.*?discretionary mark can be awarded\)',general).group()
    for r in source['tasks']:
        if r['unit']!='C2':continue
        # Heading text is not an accepted answer, including the unpunctuated
        # Secondary details heading after Sveta's previous-papers answer.
        pool_source=re.sub(r'Secondary details:?\s*','',r['publishedSourceBlock'])
        pool=[squash(item) for item in pool_source.split('•')[1:]]
        assert len(pool)=={1:13,2:11,3:15,4:13}[r['item']]
        assert len(set(pool))==len(pool)
        c=as_points(source_card(r),pool,4,steps=[0,1,2])
        c['rubric']['taskRequirements']=[general,*r['sourcePageBlocks']]
        c['rubric']['markingGuideNote']='Choose up to four distinct accepted details. Each printed answer has its own claimable row. One mark applies only to a partial detail intelligible to a monolingual English speaker, under the printed general rule. Discretionary marks remain separate from content.'
        if r['printedTariffSource'] not in r['publishedSourceBlock']:
            c['rubric']['taskRequirements'].append(r['printedTariffSource'])
        c['rubric']['criteria']=[{'id':'summary-skills','label':'Discretionary marks','maxMarks':2,'permittedMarks':[0,1,2],'guidance':[general],
            'limits':[{'id':'incomplete-response','maxMarks':1,'when':{'any':[{'flag':'incomplete-response','prompt':incomplete}]},'guidance':[incomplete]}]}]
        if r['item']==1:
            exact='For full marks '+r['requiredFullMarksCondition']
            c['rubric']['taskRequirements'].append(exact)
            c['rubric']['criteria'][0]['limits'].append({'id':'missing-certain-or-uncertain','maxMarks':1,
                'when':{'any':[{'flag':'missing-certain-or-uncertain','prompt':'The response omits a certain aspect or an uncertain aspect required by the original question.'}]},
                'guidance':[exact,incomplete]})
            c['rubric']['markingGuideNote']+=' The source requires at least one certain and one uncertain aspect for full marks. Manually flag an omitted aspect to apply the printed incomplete-response discretionary cap; no fixed content-category allocation is invented.'
        c['rubric']['markingGuideNote']+=' The original Q2.1 heading prints 50 marks in both columns, while the same directions print 40 marks. The scheme explicitly assigns 40 to the four summaries, at ten marks each; both original paper labels are retained without an extra award.'
        c['review']['guidancePages']=[7];result.append(c)
    assert len(result)==4 and sum(c['totalMarks'] for c in result)==40
    return result


def reading(source):
    result=[]
    for r in source['tasks']:
        if r['unit']!='C1':continue
        pool=[squash(item) for item in r['publishedSourceBlock'].split('•')[1:]]
        count=r['publishedTotal']//2;assert len(pool)>=count
        c=as_points(source_card(r),pool,count)
        if r['requiredNamedPools']:
            assert r['requiredNamedPools']==['advantage','disadvantage'] and len(pool)==3
            c['rubric']['groups']=[
                {'id':'advantage','label':'One advantage','answerCount':1,'rows':[{'id':f'option-{n}','text':answer,'marks':2} for n,answer in enumerate(pool[1:],1)]},
                {'id':'disadvantage','label':'One disadvantage','answerCount':1,'rows':[{'id':'full','text':pool[0],'marks':2}]}]
            c['rubric']['count']=2
        if r['id']=='ru-2021-hl-c1-1-ii':
            assert len(pool)==4 and '11th grade' in pool[1] and 'Second last year' in pool[3]
            c['rubric']['groups']=[c['rubric']['groups'][0],
                {'id':'school-year','label':'School year — one source detail','answerCount':1,'rows':[
                    {'id':'final-year','text':pool[1],'marks':2},
                    {'id':'second-last-year','text':pool[3],'marks':2}]},c['rubric']['groups'][2]]
            c['rubric']['count']=2
        c['rubric']['taskRequirements']=[source['comprehensionGuidance']]
        c['rubric']['markingGuideNote']='Assess distinct accepted details using the published two marks per correct detail. Preserve each complete slash alternative. Apply the printed general cross-question duplicate-credit instruction manually. Where the original prompt requires one advantage and one disadvantage, each named slot accepts only its own category; two advantages cannot fill both slots.'
        if r['id']=='ru-2021-hl-c1-1-ii':c['rubric']['markingGuideNote']+=' The original passage supplies one school-year fact, 11-классницу. Both published school-year wordings remain available as alternatives for that same detail; selecting both earns two marks once. Age and city are separate details.'
        c['review']['guidancePages']=[4];result.append(c)
    assert len(result)==9 and sum(c['totalMarks'] for c in result)==40
    return result


def cultural_writing(docs,source):
    from ru_review_2017_hl import band
    r=next(r for r in source['tasks'] if r['unit']=='SE');c=source_card(r)
    choices='Напишите'+between(r['fullQuestionPage'],'Напишите').split('Teideal/Title:')[0]
    assert choices.count('•')==5
    c['questionText']+='\n\n'+choices
    blocks=r['sourcePageBlocks'];assert len(blocks)==3
    assert squash(' '.join(blocks))==r['publishedSourceBlock']
    body=r['publishedSourceBlock']
    content=between(body,'Communication/content (C)','2. Expression (E)')
    expression=between(body,'2. Expression (E)','Mark Language:')
    content_bullets=[squash(x) for x in content.split('•')[1:]]
    assert len(content_bullets)==6
    title=next(x for x in content_bullets if 'ONE penalty mark' in x)
    no_content=next(x for x in content_bullets if 'no marks for language' in x)
    lower_e=re.search(r'If the content mark.*?indicate this\.',expression).group()
    lower_a=re.search(r'If the expression is very fluent.*?indicate this\.',expression).group()
    soft=re.search(r'Deduct 1/2 marks.*?infinitives',expression).group()
    normal=[];lower=[];accuracy=[]
    for page_number in (14,15):
        tables=docs['scheme'][page_number-1].find_tables().tables
        assert len(tables)==1
        for price,description in tables[0].extract():
            if price=='Mark':continue
            full=re.split(r'lower [AE]',price)[0].strip()
            normal.append(band(full,description))
            low=price.split('lower E')[-1].strip()
            lower.append(band(low,description))
            if 'lower A' in price:
                accuracy.append(band(between(price,'lower A','lower E'),description))
    assert [x['marks'] for x in normal]==[[18,19,20],[14,15,16,17],[10,11,12,13],[6,7,8,9],[1,2,3,4,5],[0]]
    assert [x['marks'] for x in lower]==[[12,13,14],[10,11],[7,8,9],[4,5,6],[1,2,3],[0]]
    assert [x['marks'] for x in accuracy]==[[13,14],[11,12],[9,10]]
    c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
    c['rubric']={'system':'language-writing','taskRequirements':blocks,
        'markingGuideNote':'The scheme prints no answer for this part. Use its printed content and expression criteria to assess the selected essay. The soft-sign direction is printed as “Deduct 1/2 marks”; apply the published direction when selecting the expression mark. The app does not infer a separate deduction from that notation.',
        'criteria':[
            {'id':'content','label':'Communication/content (C)','maxMarks':10,
             'permittedMarks':[0,2,4,6,8,10],'guidance':content_bullets},
            {'id':'title-penalty','label':'Essay title penalty','kind':'deduction','deductFrom':'content',
             'maxMarks':1,'permittedMarks':[0,1],'guidance':[title]},
            {'id':'expression','label':'Language/expression (E)','maxMarks':20,
             'permittedMarks':list(range(21)),'guidance':[squash(expression)],'bands':normal,
             'limits':[
                 {'id':'lower-e','scaleLabel':'Lower E','maxMarks':14,
                  'when':{'any':[{'criterionIds':['content'],'atMost':5,'ignoreDeductions':True},
                                 {'length':'words','below':25}]},'guidance':[lower_e],'bands':lower},
                 {'id':'lower-a','scaleLabel':'Lower A','minMarks':9,'maxMarks':14,
                  'when':{'any':[{'flag':'lower-a','prompt':lower_a}]},'guidance':[lower_a],'bands':accuracy},
                 {'id':'no-content','maxMarks':0,
                  'when':{'any':[{'criterionIds':['content'],'atMost':0,'ignoreDeductions':True}]},
                  'guidance':[no_content]}]}]}
    c['review']['noPrintedAnswer']={'fixedLine':'The scheme prints no answer for this part.',
        'schemePages':[13,14,15],
        'evidence':'scripts/markbank/authoring/reviews/russian-2021-hl-sec-20261118/archive-recheck.json'}
    assert soft in c['rubric']['criteria'][-1]['guidance'][0]
    return c


def listening(source):
    result=[]
    audio=next(row['source'] for row in json.loads((ROOT/'data/russianAudio.json').read_text()) if row['year']==2021)
    topics={'ru-2021-hl-l1-1': {'topicId': 'russian-0-8', 'additionalTopicIds': ['russian-1-0']}, 'ru-2021-hl-l1-2': {'topicId': 'russian-0-5', 'additionalTopicIds': ['russian-1-0']}, 'ru-2021-hl-l1-3': {'topicId': 'russian-0-9', 'additionalTopicIds': ['russian-1-0']}, 'ru-2021-hl-l1-4': {'topicId': 'russian-0-8', 'additionalTopicIds': ['russian-1-0']}, 'ru-2021-hl-l2-1-i': {'topicId': 'russian-0-5', 'additionalTopicIds': ['russian-1-0']}, 'ru-2021-hl-l2-1-ii': {'topicId': 'russian-0-5', 'additionalTopicIds': ['russian-1-0']}, 'ru-2021-hl-l2-2-i': {'topicId': 'russian-0-5', 'additionalTopicIds': ['russian-1-0']}, 'ru-2021-hl-l2-2-ii': {'topicId': 'russian-0-5', 'additionalTopicIds': ['russian-1-0']}, 'ru-2021-hl-l2-3': {'topicId': 'russian-0-11', 'additionalTopicIds': ['russian-1-0']}, 'ru-2021-hl-l2-4': {'topicId': 'russian-0-6', 'additionalTopicIds': ['russian-1-0']}, 'ru-2021-hl-l3-1-i': {'topicId': 'russian-0-8', 'additionalTopicIds': ['russian-1-0']}, 'ru-2021-hl-l3-1-ii': {'topicId': 'russian-0-9', 'additionalTopicIds': ['russian-1-0']}, 'ru-2021-hl-l3-2': {'topicId': 'russian-0-8', 'additionalTopicIds': ['russian-1-0']}, 'ru-2021-hl-l3-3-i': {'topicId': 'russian-0-2', 'additionalTopicIds': ['russian-1-0']}, 'ru-2021-hl-l3-3-ii': {'topicId': 'russian-2-6', 'additionalTopicIds': ['russian-1-0']}, 'ru-2021-hl-l3-4': {'topicId': 'russian-2-5', 'additionalTopicIds': ['russian-1-0']}, 'ru-2021-hl-l4-1-i': {'topicId': 'russian-0-3', 'additionalTopicIds': ['russian-1-0']}, 'ru-2021-hl-l4-1-ii': {'topicId': 'russian-0-10', 'additionalTopicIds': ['russian-1-0']}, 'ru-2021-hl-l4-2': {'topicId': 'russian-0-4', 'additionalTopicIds': ['russian-1-0']}, 'ru-2021-hl-l4-3': {'topicId': 'russian-0-10', 'additionalTopicIds': ['russian-1-0']}}
    for r in source['tasks']:
        if r['unit'] not in ('L1','L2','L3','L4'):continue
        pool=re.sub(r'^\(?\d\s*x\s*\d\s*marks\)?\s*','',r['publishedSourceBlock']).strip()
        if r['id']=='ru-2021-hl-l3-1-i':
            full=pool.split('1 mark for Boat')[0]
            answers=[squash(item) for item in full.split('•')[1:]];assert answers==['Rivers','Canals']
            c=as_points(source_card(r),answers+['Boat'],1)
            c['rubric']['groups'][-1]['rows'][0]['marks']=1
        elif r['id']=='ru-2021-hl-l4-1-i':
            answers=[squash(item) for item in pool.split('•')[1:]];assert len(answers)==4
            c=as_points(source_card(r),answers,2)
            group=c['rubric']['groups'][2]
            text=group['rows'][0]['text'];assert '(Economics on its own = 1 mark)' in text
            group['rows'][0]['text']=text.split('(Economics on its own = 1 mark)')[0].strip()
            group['answerCount']=1
            group['rows'].append({'id':'economics-only','text':'Economics','marks':1})
        else:
            answers=[squash(item) for item in pool.split('•')[1:]] if '•' in pool else [pool]
            assert len(answers)>=r['printedDetailQuota']
            c=as_points(source_card(r),answers,r['printedDetailQuota'])
            for group in c['rubric']['groups']:
                for row in group['rows']:row['marks']=r['printedDetailMarks']
        c['rubric']['taskRequirements']=[source['listeningGuidance'],r['publishedSourceBlock']]
        c['rubric']['markingGuideNote']='Use distinct accepted responses under the original quota and local tariff. Each printed plus-linked bullet remains one complete response; no unprinted one-mark component allocation is inferred. Russian answers and non-invalidating excess material are explicitly accepted.'
        if r['id']=='ru-2021-hl-l3-2':
            c['rubric']['markingGuideNote']+=' The original prompt asks for two details, while the marking scheme explicitly prints 1 x 4 marks and awards four marks for any reference to speaking English. One four-mark claim preserves that local tariff; it is not divided into invented two-mark parts.'
        c['review']['guidancePages']=[19]
        c['topicId']=topics[c['id']]['topicId'];c['additionalTopicIds']=topics[c['id']]['additionalTopicIds']
        c['sourceMaterial']['kind']='source-question'
        c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the original question. The transcript is not shown before answering.'
        c['audioMaterial']=audio;result.append(c)
    assert len(result)==20 and sum(c['totalMarks'] for c in result)==80
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
    tables=docs['scheme'][17].find_tables().tables;assert len(tables)==3
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
             'guidance':['3. Textual coherence:'+between(body,'3. Textual coherence:','Add the marks for communication/content')],'bands':coherence},
            {'id':'soft-sign-penalty','label':'Soft sign penalty','kind':'deduction','deductFrom':'expression','maxMarks':2,'permittedMarks':[0,2],'guidance':[soft]}]}
    c['review']['guidancePages']=[3];return c


def language_and_matching(docs,source):
    result=[]
    records={r['id'].replace('ru-2021-hl-',''):r for r in source['tasks'] if r['unit'] in ('LA1','CA1','LA2','SD','GR')}
    r=records['la1'];body=r['publishedSourceBlock'];pool=body.split('CASE',1)[1]
    pairs=re.findall(r'(?<![\w.])[1-5]\s+(.*?)(?=\s+[1-5]\s+\(|$)',pool)
    assert len(pairs)==5
    c=as_points(source_card(r),pairs,5);c['rubric']['taskRequirements']=[body.split('CASE',1)[0]]
    c['rubric']['markingGuideNote']='Name the case of each of the five original noun phrases. The published Russian and English case names are retained; no exclusive-language penalty is inferred.'
    result.append(c)
    r=records['ca1'];assert len(r['publishedEntries'])==22 and len(r['distinctOptions'])==21
    c=as_points(source_card(r),r['distinctOptions'],10)
    for group in c['rubric']['groups']:group['rows'][0]['marks']=1
    c['topicId']=r['topicId'];c['additionalTopicIds']=r['additionalTopicIds']
    c['rubric']['taskRequirements']=[r['publishedSourceBlock']]
    c['rubric']['markingGuideNote']='Choose ten distinct words from the original Music pool. The printed list repeats синтезатор at entries5 and10: both literal entries remain in the source guidance, but that one word can earn one mark once. Preserve the printed Cultural Awareness heading and identity alongside the music/meaning topic coverage. The source explicitly awards no mark for YouTube in English or Russian.'
    result.append(c)
    r=records['la2-i'];body=r['publishedSourceBlock']
    pairs=re.findall(r'(?<![\w.])[1-5]\.\s*(\S+)\s+(\S+)',body)
    assert pairs==[('понял','понять'),('хочу','хотеть'),('повлияли','повлиять'),('перешёл','перейти'),('сомневаюсь','сомневаться')]
    c=as_points(source_card(r),[a+' — '+b for a,b in pairs],5)
    c['rubric']['taskRequirements']=[body.split('1. понял',1)[0]]
    c['rubric']['markingGuideNote']='Supply the five printed infinitives. Both original clauses remain visible: answers may be in Irish, English or Russian, and English phrase translations receive no marks. No translated alternatives or automatic language penalty are inferred.'
    result.append(c)
    r=records['la2-ii'];body=r['publishedSourceBlock'];pool=body.split('FOCAIL / WORDS / СЛОВА',1)[1]
    pairs=re.findall(r'(\S+)\s+([1-5]\s*\([a-z]+\))',pool)
    assert pairs==[('выдохнул','5 (verb)'),('амбициозных','1 (adjective)'),('счастье','2 (noun)'),('по','3 (preposition)'),('мне','4 (pronoun)')]
    c=as_points(source_card(r),[a+' — '+b for a,b in pairs],5)
    c['rubric']['taskRequirements']=[body.split('FOCAIL / WORDS / СЛОВА',1)[0]]
    c['rubric']['markingGuideNote']='Match all five supplied words to the printed parts of speech. The second task is labelled Q.2.2(ii) in English and C.2.2(i) in Irish below OR, repeating the first Irish label. Both printed forms refer to this one task; the existing card identity is retained.'
    result.append(c)
    r=records['sd'];tables=docs['scheme'][10].find_tables().tables;assert len(tables)==1
    rows=[[squash(v or '') for v in row] for row in tables[0].extract()]
    assert [int(row[0]) for row in rows]==r['expectedAnswerOrder']
    c=as_points(source_card(r),[row[0]+' — '+row[1] for row in rows],10)
    c['rubric']['taskRequirements']=[r['publishedSourceBlock'].split('8 Маркетинговая',1)[0]]
    c['rubric']['markingGuideNote']='Match all ten original programme descriptions to their supplied genre numbers, in the printed paragraph order. Each correct match has the published two marks.'
    result.append(c)
    r=records['gr'];answers=grammar_forms(docs['scheme'])
    assert len(answers)==15
    c=as_points(source_card(r),answers,15)
    c['rubric']['taskRequirements']=[r['publishedSourceBlock'].split('В середине лета',1)[0]]
    c['rubric']['markingGuideNote']='Thirteen bracketed prompts supply fifteen separately priced forms. The first printed past/present pair is one accepted alternative for the same prompt, not two credits. Preserve both accepted forms alongside the exact general spelling/transcription and wrong-tense rules; no source answer is silently corrected.'
    result.append(c)
    assert len(result)==6 and sum(c['totalMarks'] for c in result)==90
    return result


def source_language_rules(cards,source):
    rule='Language of answer:'+between(source['generalWrittenGuidance'],'Language of answer:','Quality of English:')
    exception=re.search(r'Discretionary marks \(as opposed to content marks\) may be awarded.*?answers\)\.',source['summaryGuidance']).group()
    for c in cards:
        if c['section'] not in ('C1','C2','CA1','GR','GW'):continue
        c['answerLanguageRule']={'otherLanguageMultiplier':0,'sourceText':squash(rule),'schemePages':[3]}
        if c['section'] in ('C1','C2'):
            c['rubric']['markingGuideNote']+=' Answer in English or Irish, as explicitly permitted by the two original paper columns. Irish is not a disallowed answer language.'
            c['rubric']['taskRequirements'].append('Quality of English:'+between(source['generalWrittenGuidance'],'Quality of English:','Marking:'))
        if c['section']=='C2':
            c['answerLanguageRule']['manualCriterionExceptions']={'criterionIds':['summary-skills'],'sourceText':exception,'schemePages':[7]}


def build():
    docs,source=source_records()
    try:
        cards=reading(source)+summaries(source)+language_and_matching(docs,source)+[writing(docs,source),cultural_writing(docs,source)]+listening(source)
        source_language_rules(cards,source)
        old={c['id']:c for c in json.loads((ROOT/'scripts/markbank/authored/russian.json').read_text()) if c['year']==2021 and c['level']=='higher'}
        assert len(old)==17 and old.keys()<={c['id'] for c in cards}
        for c in cards:
            if c['id'] in old:
                c['review']['correctsExisting']=True
                c['conceptId']=old[c['id']]['conceptId']
        assert len(cards)==len({c['id'] for c in cards})==41
        assert sum(c['totalMarks'] for c in cards)==320
        assert sum(c['totalMarks'] for c in cards if c.get('kind')=='rubric')==320
        assert sum(bool(c.get('answerLanguageRule')) for c in cards)==16
        assert sum(c['review'].get('correctsExisting',False) for c in cards)==17
        return cards
    finally:
        for document in docs.values():document.close()


def raw_scheme_text():
    path=ROOT/'examiner-reports/russian/schemes/2021-hl.pdf'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==METADATA['scheme']['sha256']
    with fitz.open(path) as document:
        pages=[page.get_text() for page in document]
        raw='\n\n'.join(f'## Page {n+1}\n\n'+text for n,text in enumerate(pages))+'\n'
        # Retain every untouched page plus a labelled complete-page whitespace
        # rendering; the generic provenance comparator removes numeric-only lines.
        joined='\n\n'.join(f'### Joined original page {n+1}\n\n'+squash(text) for n,text in enumerate(pages))
        return raw+'\n# Original pages with line wraps joined\n\n'+joined+'\n'



if __name__=='__main__':
    save_reviewed(build())
    (ROOT/'examiner-reports/russian/schemes/2021-hl.md').write_text(raw_scheme_text())
