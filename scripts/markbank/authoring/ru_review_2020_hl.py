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
    records.append(record('SE',None,None,q,[12],'\n'.join(page(S,p) for p in (12,13,14)),[12,13,14],30,fullQuestionPage=page(Q,12),sourcePageBlocks=[squash(page(S,p)) for p in (12,13,14)],reviewNote='Alex approved one or two marks for soft-sign errors; all five choices and original C10/E20 remain.'))
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
            records.append(record(f'L{section}',qi,qr,q,[section+1],pool,[section+16],None,printedDetailQuota=count,topicId=topic,reviewNote=note,sharedAward=f'L{section}-section20',reviewNoteAllocation='Alex approved two per requested detail; explicit luggage1+1 and pet1 awards are retained.'))
    assert len(records)==42 and len({r['id'] for r in records})==42
    return docs,dict(status='Unpublished source-only proposal',sources=METADATA,independentTasks=42,writtenTasks=20,listeningTasks=22,printedExamTotal=300,printedWrittenTotal=220,pricedWrittenTotal=220,confidenceWrittenPrintedTotal=0,generalWrittenGuidance=squash(page(S,3)),comprehensionGuidance=squash(comprehension[:re.search(r'^\s*1\.\s*\(i\)',comprehension,re.M).start()]),summaryGuidance=squash(summary[:re.search(r'^\s*1\.\s*[A-Z]',summary,re.M).start()]),listeningGuidance=squash(source[:heads[0].start()]),tasks=records)


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
    for physical in (13,14):
        tables=docs['scheme'][physical-1].find_tables().tables;assert len(tables)==1
        for printed,description in tables[0].extract():
            if printed=='Mark':continue
            normal.append(band(re.split(r'lower [AE]',printed)[0].strip(),description))
            lower.append(band(printed.split('lower E')[-1].strip(),description))
            if 'lower A' in printed:accuracy.append(band(between(printed,'lower A','lower E'),description))
    assert [x['marks'] for x in normal]==[[18,19,20],[14,15,16,17],[10,11,12,13],[6,7,8,9],[1,2,3,4,5],[0]]
    assert [x['marks'] for x in lower]==[[12,13,14],[10,11],[7,8,9],[4,5,6],[1,2,3],[0]]
    assert [x['marks'] for x in accuracy]==[[13,14],[11,12],[9,10]]
    c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
    blocks=r['sourcePageBlocks'];assert len(blocks)==3 and squash(' '.join(blocks))==body
    c['rubric']={'system':'language-writing','taskRequirements':blocks,
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
    c['review']['allocationApproval']='reviews/russian-2020-hl-sec-20261118/allocation-approval.json'
    return no_printed_answer(c,r['schemePages'])


def no_printed_answer(c,pages):
    fixed='The scheme prints no answer for this part.'
    if not c['rubric']['markingGuideNote'].startswith(fixed):c['rubric']['markingGuideNote']=fixed+' '+c['rubric']['markingGuideNote']
    c['review']['reviewedAt']='2026-11-19'
    c['review']['noPrintedAnswer']={'fixedLine':fixed,'schemePages':pages,'evidence':'scripts/markbank/authoring/reviews/russian-2020-hl-sec-20261118/archive-recheck.json'}
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
    c['rubric']['markingGuideNote']='Choose five distinct accepted source entries, in any case or number as explicitly permitted. A complete multiword entry is one response, each has one mark. The original paper labels this Q.1.3; the scheme labels it Q.2.2. Both refer to the first travel/cruise passage.'
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
    c['rubric']['markingGuideNote']='The eleven bracketed prompts contain fifteen word forms with separate marks: four prompts supply two words each. Each form receives the published two marks; зимой /зимою is one alternative response. Apply the exact zero-credit spelling/transcription and wrong-tense rules. The original instructions preserve singular or plural as supplied.'
    result.append(c)
    assert len(result)==5 and sum(c['totalMarks'] for c in result)==70
    return result


def allocation_approval():
    folder=ROOT/'scripts/markbank/authoring/reviews/russian-2020-hl-sec-20261118'
    proposal_path=folder/'allocation-proposal.json'
    approval=json.loads((folder/'allocation-approval.json').read_text())
    assert approval['listeningAnswer']=='Approve the proposed listening allocations'
    assert approval['writingAnswer']=='One or two marks'
    assert hashlib.sha256(proposal_path.read_bytes()).hexdigest()==approval['proposalSha256']
    return json.loads(proposal_path.read_text())


def listening(source):
    proposal=allocation_approval()
    approved={r['id']:r for r in proposal['listening']['cards'] if r['year']==2020}
    records=[r for r in source['tasks'] if r['component']=='aural']
    assert len(approved)==len(records)==22
    audio=next(row['source'] for row in json.loads((ROOT/'data/russianAudio.json').read_text()) if row['year']==2020)
    result=[]
    for r in records:
        a=approved[r['id']]
        assert a['question']==r['question'] and a['sourceAnswers']==r['publishedSourceBlock']
        count=a['proposedDetails'];assert a['proposedMaximum']==2*count
        body=r['publishedSourceBlock']
        # Keep named partial and zero-credit clauses as source guidance. Each
        # partial shares its full answer's existing mutually exclusive group.
        if r['id']=='ru-2020-hl-l1-2':
            assert body=='• One suitcase (1 mark) and a bag/purse (1 mark)'
            c=as_points(source_card({**r,'publishedTotal':2}),['One suitcase','a bag/purse'],2)
            for g in c['rubric']['groups']:g['rows'][0]['marks']=1
        elif r['id']=='ru-2020-hl-l4-3-ii':
            answers=[squash(x) for x in body.split('•')[1:]]
            assert answers==["Dog called ‘Rada’ / happy / joy",'Cat called Steve','Dog: 1 mark','Cat: 1 mark']
            c=as_points(source_card({**r,'publishedTotal':2}),answers[:2],1,partials={0:['Dog'],1:['Cat']})
        else:
            answers=[squash(x) for x in body.split('•')[1:] if squash(x)]
            c=as_points(source_card({**r,'publishedTotal':a['proposedMaximum']}),answers,count)
        c['rubric']['taskRequirements']=[source['listeningGuidance'],body]
        c['rubric']['markingGuideNote']='Two marks per complete requested detail are inferred from the paper’s 20-mark section totals and approved on 18 November 2026; two is not printed as a general per-detail award in this scheme. The printed one-mark and zero-mark instructions remain in force. Select distinct details up to the number requested.'
        c['rubric']['markingGuideNote']+=' The booklet front says 50 minutes and its back says 40 minutes; both original statements are retained.'
        if r['reviewNote']:c['rubric']['markingGuideNote']+=' Source numbering: '+r['reviewNote']
        c['review']['allocationApproval']='reviews/russian-2020-hl-sec-20261118/allocation-approval.json'
        c['review']['approvedInference']={'marksPerRequestedDetail':2,'requestedDetails':count,'printedSectionTotal':20}
        if r['id']=='ru-2020-hl-l1-2':
            c['rubric']['markingGuideNote']='The scheme gives one mark for a suitcase and one mark for a bag/purse. These two marks are explicitly printed; no allocation is inferred for this answer.'
            c['review'].pop('approvedInference');c['review']['explicitAllocation']=[1,1]
        c['review']['reviewedAt']='2026-11-19';c['review']['guidancePages']=[17]
        c['topicId']=r['topicId'];c['additionalTopicIds']=['russian-1-0']
        c['sourceMaterial']['kind']='source-question'
        c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
        c['audioMaterial']=audio;result.append(c)
    assert len(result)==22 and sum(c['totalMarks'] for c in result)==80
    assert all(sum(c['totalMarks'] for c in result if c['section']==f'L{section}')==20 for section in range(1,5))
    return result



def source_language_rules(cards,source):
    rule='Language of answer:'+between(source['generalWrittenGuidance'],'Language of answer:','Quality of English:')
    exception=re.search(r'Discretionary marks \(as opposed to content marks\) may be awarded.*?answers\)\.',source['summaryGuidance']).group()
    for c in cards:
        if c['section'] not in ('C1','C2','LA1','GR','GW','SE'):continue
        c['answerLanguageRule']={'otherLanguageMultiplier':0,'sourceText':squash(rule),'schemePages':[3]}
        if c['section'] in ('C1','C2'):
            c['rubric']['markingGuideNote']+=' Answer in English or Irish, as permitted by the original bilingual paper.'
            c['rubric']['taskRequirements'].append('Quality of English:'+between(source['generalWrittenGuidance'],'Quality of English:','Marking:'))
        if c['section']=='C2':
            c['answerLanguageRule']['manualCriterionExceptions']={'criterionIds':['summary-skills'],'sourceText':exception,'schemePages':[7]}


def build():
    docs,source=source_records()
    try:
        cards=reading(source)+summaries(source)+language_and_matching(docs,source)+[no_printed_answer(writing(docs,source),[15,16]),cultural_writing(docs,source)]+listening(source)
        source_language_rules(cards,source)
        assert len(cards)==len({c['id'] for c in cards})==42
        assert sum(c['totalMarks'] for c in cards)==300
        assert sum(c['totalMarks'] for c in cards if c.get('kind')=='rubric')==300
        assert sum(bool(c.get('answerLanguageRule')) for c in cards)==18
        from ru_live_listening_ids import preserve_live_listening_ids
        return preserve_live_listening_ids(cards)
    finally:
        for document in docs.values():document.close()


if __name__=='__main__':
    # Retain the released section ID on its first separately marked question.
    save_reviewed(build())
    (ROOT/'examiner-reports/russian/schemes/2020-hl.md').write_text(raw_scheme_text())
