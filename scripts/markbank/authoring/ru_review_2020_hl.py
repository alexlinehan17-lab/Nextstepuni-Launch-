"""Source-reviewed Russian 2020 Higher, derived from three pinned originals."""
import hashlib,json,re,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts/markbank/authoring'))
from ru_review_2015_ol import question_text,source_split
from ru_review_2026_hl import squash,between
from ru_paper import bag,score
METADATA={'paper': {'pages': 16,
           'sha256': '29eb6fbdfe4d43b0f85912a87ba9589710417a5e39794c630f0ff70949c37251'},
 'aural': {'pages': 8,
           'sha256': 'd9394291088173c4590d88db20bb6c5380dec243a2c50cebc37ea12c4d53e3a8'},
 'scheme': {'pages': 27,
            'sha256': '7ac8daeec37224d7082fe61f3e6a6bf5c6c99429580bc25bfa5efd2ff888d55f'}}

def summary_tariff(document, number):
    """Bind the printed right-margin tariff to its own numbered source region.

    The PDF content stream emits some tariffs before the next heading. Geometry,
    rather than extraction order, establishes the original question association.
    """
    assert number in (1,2,3,4)
    physical=7 if number==1 else 8
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
    for kind,relative in [('paper','papers/2020-hl-000-paper.pdf'),('aural','papers/2020-hl-A00-paper.pdf'),('scheme','schemes/2020-hl.pdf')]:
        path=ROOT/'examiner-reports/russian'/relative
        assert hashlib.sha256(path.read_bytes()).hexdigest()==METADATA[kind]['sha256']
        docs[kind]=fitz.open(path);assert len(docs[kind])==METADATA[kind]['pages']
    Q,A,S=docs['paper'],docs['aural'],docs['scheme']
    def page(doc,n,right=False):
        rect=fitz.Rect(295,30,580,793) if right else fitz.Rect(20,30,580,793)
        text=doc[n-1].get_text(clip=rect,sort=False).replace('\uf0b7','•').replace('\xa0',' ')
        # This source prints physical p3 as page2; source-specific exact leading
        # standalone footer removal requires the mandatory original regression.
        if doc is S:text=re.sub(r'^\s*'+str(n-1)+r'\s*\n','',text,count=1)
        return text
    norm=lambda text:re.sub(r'[^\w]','',text.casefold())
    def numbered(text):
        heads=list(re.finditer(r'^\s*(\d)\.\s*(?:\(?((?:iv|i{1,3}))\)?\.?\s*)?(?=[A-Z“])',text,re.M))
        return [(int(h.group(1)),h.group(2),text[h.end():heads[i+1].start() if i+1<len(heads) else len(text)]) for i,h in enumerate(heads)]
    def record(unit,item,roman,question,qp,body,sp,total,**extra):
        component='aural' if unit in ('L1','L2','L3','L4') else 'paper'
        assert any(norm(question) in norm(' '.join(page(docs[component],p,right) for p in qp)) for right in (False,True)),(unit,item,roman,question)
        assert norm(body) in norm(' '.join(page(S,p) for p in sp)),(unit,item,roman,body)
        return dict(id='ru-2020-hl-'+unit.lower()+(f'-{item}' if item is not None else '')+(f'-{roman}' if roman else ''),unit=unit,item=item,roman=roman,question=question,questionPages=qp,component=component,publishedSourceBlock=squash(body),schemePages=sp,publishedTotal=total,**extra)
    records=[]
    comprehension='\n'.join(page(S,p) for p in (4,5))
    blocks=numbered(comprehension)
    asks=[(i,r,question_text(q),p) for p in (3,4) for i,r,q in numbered(page(Q,p,True))]
    assert len(blocks)==len(asks)==9
    for (i,r,b),(qi,qr,q,p),total in zip(blocks,asks,[6,6,4,6,4,6,4,2,2]):
        assert (i,r)==(qi,qr)
        price=re.search(r'(\d)\s*x\s*2\s*marks',b);assert price
        assert int(price.group(1))*2==total
        cue,body=b[:price.start()],b[price.start():]
        assert score(bag(q),bag(cue))>.7,(q,cue)
        records.append(record('C1',i,r,q,[p],body,[4,5],total))
    assert sum(r['publishedTotal'] for r in records)==40
    q='Supply the infinitive/dictionary form '+squash(between(page(Q,5,True),'Supply the infinitive/dictionary form'))
    q=q[:q.index('verbs from the text.')+len('verbs from the text.')]
    language=page(S,6)
    body='Q. 1.2'+between(language,'Q. 1.2','Q. 2.2')
    records.append(record('LA1',1,None,q,[5],body,[6],5,sourceNumberingNote='Paper and scheme Q.1.2.'))
    q='Semantic field/'+squash(between(page(Q,5,True),'Semantic field/'))
    q=q[:q.index('them in Russian.')+len('them in Russian.')]
    body='Q. 2.2'+between(language,'Q. 2.2')
    records.append(record('LA1',2,None,q,[5],body,[6],5,sourceNumberingNote='Paper Q.1.3 versus scheme Q.2.2. Both refer to the first cruise passage travel semantic field; do not move it to the summary passage.'))
    summary='\n'.join(page(S,p) for p in (7,8))
    blocks=numbered(summary);assert len(blocks)==4
    for i,r,b in blocks:
        qp={1:6,2:7,3:8,4:8}[i]
        paper_asks=[(n,rr,question_text(q)) for n,rr,q in numbered(page(Q,qp,True))]
        matches=[q for n,rr,q in paper_asks if n==i and rr is None];assert len(matches)==1,(i,paper_asks)
        q=matches[0]
        tariff=summary_tariff(S,i)
        b=re.sub(r'^\s*10\s+marks\s*$', '', b, flags=re.M)
        cue,body=source_split(b,'Main points:')
        assert score(bag(q),bag(cue))>.75,(q,cue)
        records.append(record('C2',i,None,q,[qp],body,[7,8],10,printedTariffSource=tariff['text'],printedTariffEvidence=tariff,scoring={'detail':2,'detailQuota':4,'partialDetail':1,'discretionaryMaximum':2,'incompleteDiscretionaryMaximum':1}))
    q='Indicate the case '+squash(between(page(Q,9,True),'Indicate the case'))
    q=q[:q.index('Russian.)')+len('Russian.)')]
    records.append(record('LA2',None,None,q,[9],page(S,9),[9],10,reviewNote='Ten noun phrases at1; Irish/English/Russian explicitly allowed. Phrase translations in English explicitly0.'))
    q='Read the following paragraphs '+squash(between(page(Q,10,True),'Read the following paragraphs'))
    q=q[:q.index('headings provided.')+len('headings provided.')]
    rows=[[squash(v or '') for v in row] for row in S[9].find_tables().tables[0].extract()]
    assert [re.findall(r'\d+',r[0]) for r in rows]==[[str(i)] for i in [8,3,5,7,9,6,4,1,2,10]],rows
    records.append(record('SD',None,None,q,[10],page(S,10),[10],20,answerRows=rows))
    q='Read through the following text. '+question_text(between(page(Q,11,True),'Read through the following text.'))
    q=q[:q.index('substitute words.')+len('substitute words.')]
    records.append(record('GR',None,None,q,[11],page(S,11),[11],30,reviewNote='Eleven bracketed original prompts with15 underlined accepted forms, including four two-word phrases. зимой/зимою is one printed alternative response. Bold source spans yield the15 accepted forms; the original underlining was independently visually reviewed.'))
    q='Write a short essay '+squash(between(page(Q,12,True),'Write a short essay'))
    q=q[:q.index('essay title.')+len('essay title.')]
    records.append(record('SE',None,None,q,[12],'\n'.join(page(S,p) for p in (12,13,14)),[12,13,14],30,fullQuestionPage=page(Q,12),sourcePageBlocks=[squash(page(S,p)) for p in (12,13,14)],pending='Complete confidence task; ambiguous literalDeduct1/2marks. Five choices, full C10/E20 and guidance.'))
    q='Write a piece '+question_text(between(page(Q,13,True),'Write a piece'))
    records.append(record('GW',None,None,q,[13],'\n'.join(page(S,p) for p in (15,16)),[15,16],40,pending='Three choices,C15/E15/TC10,LowerA7–12 with9–11/11–12 overlap kept literal,explicit2softsign.'))
    assert len(records)==20 and sum(r['publishedTotal'] for r in records)==220
    source='\n'.join(page(S,p) for p in (17,18,19,20))
    heads=list(re.finditer(r'^\s*SECTION (IV|III|II|I)\b[^\n]*$',source,re.M));assert len(heads)==4
    counts=[[2,None,2,2,2,None],[2,None,2,2,2,1],[2,2,2,2,2],[3,2,2,2,1]]
    topics=[['russian-0-9','russian-0-8','russian-0-2','russian-0-9','russian-0-3','russian-0-8'],['russian-0-5','russian-0-5','russian-0-11','russian-0-6','russian-0-5','russian-0-5'],['russian-0-8','russian-0-9','russian-0-9','russian-0-9','russian-0-9'],['russian-0-7','russian-0-5','russian-0-4','russian-0-5','russian-0-1']]
    for n,h in enumerate(heads):
        section=n+1;body=source[h.end():heads[n+1].start() if n+1<len(heads) else len(source)]
        blocks=numbered(body);asks=[(i,r,question_text(q)) for i,r,q in numbered(page(A,section+1,True))]
        assert len(blocks)==len(asks)==len(counts[n]),(section,len(blocks),len(asks))
        for (i,r,b),(qi,qr,q),count,topic in zip(blocks,asks,counts[n],topics[n]):
            note=''
            if (section,i,r)==(2,1,None):
                assert (qi,qr)==(1,'i');note='English booklet1(i), Irish and scheme1.'
            elif (section,i,r)==(2,3,'i'):
                assert (qi,qr)==(3,None);note='Paper3, scheme3(i), same future-hopes prompt.'
            else:assert (i,r)==(qi,qr),(section,i,r,qi,qr)
            cue,pool=source_split(b,'•');assert score(bag(q),bag(cue))>.75,(q,cue)
            records.append(record(f'L{section}',qi,qr,q,[section+1],pool,[section+16],None,printedDetailQuota=count,topicId=topic,reviewNote=note,sharedAward=f'L{section}-section20',pending='Whole20confidence, full per-answer tariffs absent; luggage1+1 and petsbare1 remain exact visible evidence.'))
    assert len(records)==42 and len({r['id'] for r in records})==42
    return docs,dict(status='Unpublished source-only proposal',sources=METADATA,independentTasks=42,writtenTasks=20,listeningTasks=22,printedExamTotal=300,printedWrittenTotal=220,pricedWrittenTotal=190,confidenceWrittenPrintedTotal=30,generalWrittenGuidance=squash(page(S,3)),comprehensionGuidance=squash(comprehension[:re.search(r'^\s*1\.\s*\(i\)',comprehension,re.M).start()]),summaryGuidance=squash(summary[:re.search(r'^\s*1\.\s*[A-Z]',summary,re.M).start()]),listeningGuidance=squash(source[:heads[0].start()]),tasks=records)


def grammar_forms(document):
    spans=[span for block in document[10].get_text('dict')['blocks'] if 'lines' in block
           for line in block['lines'] for span in line['spans']
           if span['bbox'][1]>190 and span['flags']&16]
    assert len(spans)==12 and {span['font'] for span in spans}=={'Calibri,Bold'}
    forms=[]
    for span in spans:
        text=span['text'].strip().rstrip('.')
        forms.extend([text] if '/' in text else text.split())
    assert forms==['Мою','бабушку','многодетной','семье','лыжах','среднюю','Моего','дедушку','восьми','главным','помощником','дому','зимой /зимою','природе','края'],forms
    return forms


from ru_review_2026_hl import base as common_base, as_points, save_reviewed


def base(*args, **kwargs):
    c=common_base(*args, **kwargs)
    for key in ('id','questionRef'):c[key]=c[key].replace('2026','2020')
    c['year']=2020;c['sourceMaterial']['title']=c['sourceMaterial']['title'].replace('2026','2020')
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


def summaries(source):
    result=[];general=source['summaryGuidance']
    incomplete=re.search(r'If a candidate fails.*?discretionary mark can be awarded\)',general).group()
    for r in source['tasks']:
        if r['unit']!='C2':continue
        c=manual_details(r,4,[0,1,2],[general,r['publishedSourceBlock']],
            'Assess four distinct details manually against the complete published pool. One mark applies only to a partial detail intelligible to a monolingual English speaker, under the printed general rule. Discretionary marks remain separate from content.')
        if r['printedTariffSource'] not in r['publishedSourceBlock']:
            c['rubric']['taskRequirements'].append(r['printedTariffSource'])
        c['rubric']['criteria']=[{'id':'summary-skills','label':'Discretionary marks','maxMarks':2,'permittedMarks':[0,1,2],'guidance':[general],
            'limits':[{'id':'incomplete-response','maxMarks':1,'when':{'any':[{'flag':'incomplete-response','prompt':incomplete}]},'guidance':[incomplete]}]}]
        c['review']['guidancePages']=[7];result.append(c)
    assert len(result)==4 and sum(c['totalMarks'] for c in result)==40
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
    tables=docs['scheme'][15].find_tables().tables;assert len(tables)==3
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


def cultural_confidence(source):
    r=next(r for r in source['tasks'] if r['unit']=='SE');c=source_card(r)
    choices='Напишите'+between(r['fullQuestionPage'],'Напишите').split('___')[0]
    assert all(f'{n}.' in choices for n in range(1,6));c['questionText']+='\n\n'+choices
    c['kind']='question';c['tariffModel']={'kind':'questionTotal'}
    # Complete original page slices retain every clause without silently
    # joining across the printed page-number blocks.
    blocks=r['sourcePageBlocks'];assert len(blocks)==3
    assert squash(' '.join(blocks))==r['publishedSourceBlock']
    c['rows']=[{'id':identifier,'kind':'point','marks':None,'verbatim':text}
        for identifier,text in zip(['published-choice','published-guidance','published-expression-grid'],blocks)]
    c['rows'][0]['contextNote']='Confidence review: the complete question is printed as 30 marks, content 10 plus expression 20. The scheme’s literal soft-sign instruction says “Deduct 1/2 marks” without establishing whether this is a half-mark or one-or-two marks. Neither interpretation is selected. Every original choice and scoring rule is retained, but this task does not calculate a numerical score.'
    return c


def raw_scheme_text():
    path=ROOT/'examiner-reports/russian/schemes/2020-hl.pdf'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==METADATA['scheme']['sha256']
    with fitz.open(path) as document:
        pages=[page.get_text() for page in document]
        raw='\n\n'.join(f'## Page {n+1}\n\n'+text for n,text in enumerate(pages))+'\n'
        # Retain every untouched page plus a labelled complete-page whitespace
        # rendering; the generic provenance comparator removes numeric-only lines.
        joined='\n\n'.join(f'### Joined original page {n+1}\n\n'+squash(text) for n,text in enumerate(pages))
        return raw+'\n# Original pages with line wraps joined\n\n'+joined+'\n'


def reading(source):
    result=[]
    for r in source['tasks']:
        if r['unit']!='C1':continue
        pool=r['publishedSourceBlock'].split('•')[1:]
        count=r['publishedTotal']//2
        assert len(pool)>=count
        c=as_points(source_card(r),[squash(item) for item in pool],count)
        c['rubric']['taskRequirements']=[source['comprehensionGuidance']]
        c['rubric']['markingGuideNote']='Assess distinct accepted details against the complete printed pool. Preserve each slash alternative as one response. The source gives two marks per correct detail; no unprinted one-mark partial or semantic exclusion is inferred. Apply the printed general rule on information repeated across questions manually, keeping the answer that earns the most marks.'
        c['review']['guidancePages']=[4]
        result.append(c)
    assert len(result)==9 and sum(c['totalMarks'] for c in result)==40
    return result


def language_and_matching(docs,source):
    result=[]
    records={r['id'].replace('ru-2020-hl-',''):r for r in source['tasks'] if r['unit'] in ('LA1','LA2','SD','GR')}
    r=records['la1-1']
    pool=r['publishedSourceBlock'].rsplit('infinitive (инфинитив)',1)[1]
    pairs=re.findall(r'(?<![\w.])[1-5]\s+(\S+)\s+(\S+)',pool)
    assert pairs==[('планируют','планировать'),('надели','надеть'),('наслаждались','наслаждаться'),('отправились','отправиться'),('иди','идти')],pairs
    c=as_points(source_card(r),[a+' — '+b for a,b in pairs],5)
    for g in c['rubric']['groups']:g['rows'][0]['marks']=1
    c['rubric']['taskRequirements']=[r['publishedSourceBlock'].rsplit('infinitive (инфинитив)',1)[0]]
    c['rubric']['markingGuideNote']='Supply all five original infinitives, preserving the aspect of each supplied verb under the exact source direction. Paper and scheme identify this task as Q.1.2.'
    result.append(c)
    r=records['la1-2']
    pool=r['publishedSourceBlock'].split('5 x 1 = 5',1)[1]
    words=[squash(word).rstrip('.') for word in pool.split(',')]
    assert len(words)==18 and len(set(words))==18,words
    c=as_points(source_card(r),words,5)
    for g in c['rubric']['groups']:g['rows'][0]['marks']=1
    c['rubric']['taskRequirements']=[r['publishedSourceBlock'].split('Путешествовать',1)[0]]
    c['rubric']['markingGuideNote']='Choose five distinct accepted source entries, in any case or number as explicitly permitted. A complete multiword entry is one response, not separately priced words. The original paper labels this Q.1.3; the scheme labels it Q.2.2. Both refer to the first travel/cruise passage.'
    result.append(c)
    r=records['la2']
    entries=re.findall(r'(?<![\w.])(?:10|[1-9])\.\s*(.*?)(?=\s+(?:10|[1-9])\.\s|$)',r['publishedSourceBlock'])
    assert len(entries)==10 and sum('предожный' in entry for entry in entries)==2,entries
    c=as_points(source_card(r),entries,10)
    for g in c['rubric']['groups']:g['rows'][0]['marks']=1
    c['rubric']['taskRequirements']=[r['publishedSourceBlock'].split('1. (знакомили)',1)[0]]
    c['rubric']['markingGuideNote']='All ten original noun phrases are required. Case names may be supplied in Irish, English or Russian; English translations of the phrases receive no marks under the separate printed rule. The two printed предожный spellings are retained literally, without replacing the original acceptance wording.'
    result.append(c)
    r=records['sd'];rows=r['answerRows'];assert len(rows)==10
    c=as_points(source_card(r),[row[0]+' — '+row[1] for row in rows],10)
    c['rubric']['taskRequirements']=[r['publishedSourceBlock'].split('8 Расширьте',1)[0]]
    c['rubric']['markingGuideNote']='Match each of the ten original paragraphs to its printed heading. Keep the answers in the original paragraph order.'
    result.append(c)
    r=records['gr'];answers=grammar_forms(docs['scheme'])
    c=as_points(source_card(r),answers,15)
    c['rubric']['taskRequirements']=[r['publishedSourceBlock'].split('Мою бабушку',1)[0]]
    c['rubric']['markingGuideNote']='The eleven bracketed prompts contain fifteen separately priced word forms: four prompts supply two words each. Each form receives the published two marks; зимой /зимою is one alternative response. Apply the exact zero-credit spelling/transcription and wrong-tense rules. The original instructions preserve singular or plural as supplied.'
    result.append(c)
    assert len(result)==5 and sum(c['totalMarks'] for c in result)==70
    return result


def listening(source):
    result=[]
    manifest=json.loads((ROOT/'scripts/markbank/authoring/russian-joint-tasks.json').read_text())
    audio=next(row['source'] for row in json.loads((ROOT/'data/russianAudio.json').read_text()) if row['year']==2020)
    for section in range(1,5):
        records=[r for r in source['tasks'] if r['unit']==f'L{section}']
        expected=next(task for task in manifest['tasks'] if task['id']==f'ru-2020-hl-l{section}')
        prompts=[f'{r["item"]}'+(f'({r["roman"]})' if r['roman'] else '')+'. '+r['question'] for r in records]
        c=base(f'L{section}','\n\n'.join(prompts),20,expected['paperPages'],expected['schemePages'])
        c['questionRef']=expected['questionRef'];c['kind']='question';c['tariffModel']={'kind':'questionTotal'}
        c['review']['questionPages']=expected['paperPages'];c['review']['guidancePages']=[17]
        c['review']['coveredQuestionRefs']=[f'2020 HL Section L{section} Q'+str(r['item'])+(f'({r["roman"]})' if r['roman'] else '') for r in records]
        c['review']['atlasQuestions']=[{'n':r['id'].replace('ru-2020-hl-',''),'questionRef':ref,
            'questionText':r['question'],'questionPages':r['questionPages'],'schemePages':r['schemePages'],
            'topicId':r['topicId'],'additionalTopicIds':['russian-1-0']} for r,ref in zip(records,c['review']['coveredQuestionRefs'])]
        note='Confidence review of the complete printed 20-mark section. The scheme does not provide complete full-answer allocations for its questions. All original prompts and accepted pools remain available, with no equal tariff or numerical score inferred.'
        if section==1:note+=' The luggage answer explicitly gives one mark for a suitcase and one for a bag/purse. Those known prices remain visible below; they do not establish an 18-mark remainder or allocations for the other questions.'
        if section==4:note+=' The published bare Dog and Cat one-mark partials remain visible; they do not establish the absent full-answer tariffs.'
        note+=' The original booklet front says 50 minutes while its back says 40 minutes; both source statements are retained without selecting one as a correction.'
        c['rows']=[{'id':'general-listening-guidance','kind':'point','marks':None,'verbatim':source['listeningGuidance'],'contextNote':note}]
        for r in records:
            c['rows'].append({'id':r['id'].replace('ru-2020-hl-',''),'kind':'point','marks':None,
                'verbatim':r['publishedSourceBlock'],'contextNote':r['question']+(' Source numbering: '+r['reviewNote'] if r['reviewNote'] else '')})
        topics=list(dict.fromkeys([r['topicId'] for r in records]+['russian-1-0']))
        c['topicId']=topics[0];c['additionalTopicIds']=topics[1:]
        c['sourceMaterial']['kind']='source-question'
        c['sourceMaterial']['presentationNote']='Listen to the official recording and answer all the original questions in this section. The transcript is not shown before answering.'
        c['audioMaterial']=audio;result.append(c)
    assert len(result)==4 and sum(len(c['review']['coveredQuestionRefs']) for c in result)==22
    return result


def source_language_rules(cards,source):
    rule='Language of answer:'+between(source['generalWrittenGuidance'],'Language of answer:','Quality of English:')
    exception=re.search(r'Discretionary marks \(as opposed to content marks\) may be awarded.*?answers\)\.',source['summaryGuidance']).group()
    for c in cards:
        if c['section'] not in ('C1','C2','LA1','GR','GW'):continue
        c['answerLanguageRule']={'otherLanguageMultiplier':0,'sourceText':squash(rule),'schemePages':[3]}
        if c['section'] in ('C1','C2'):
            c['rubric']['markingGuideNote']+=' Answer in English or Irish, as permitted by the original bilingual paper.'
            c['rubric']['taskRequirements'].append('Quality of English:'+between(source['generalWrittenGuidance'],'Quality of English:','Marking:'))
        if c['section']=='C2':
            c['answerLanguageRule']['manualCriterionExceptions']={'criterionIds':['summary-skills'],'sourceText':exception,'schemePages':[7]}


def build():
    docs,source=source_records()
    try:
        cards=reading(source)+summaries(source)+language_and_matching(docs,source)+[writing(docs,source),cultural_confidence(source)]+listening(source)
        source_language_rules(cards,source)
        assert len(cards)==len({c['id'] for c in cards})==24
        assert sum(c['totalMarks'] for c in cards)==300
        assert sum(c['totalMarks'] for c in cards if c.get('kind')=='rubric')==190
        assert sum(bool(c.get('answerLanguageRule')) for c in cards)==17
        return cards
    finally:
        for document in docs.values():document.close()


if __name__=='__main__':
    save_reviewed(build())
    (ROOT/'examiner-reports/russian/schemes/2020-hl.md').write_text(raw_scheme_text())
