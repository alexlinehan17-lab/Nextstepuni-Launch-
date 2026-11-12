"""Original-source Russian 2018 Higher; the conflicting essay stays unpriced."""
import hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts/markbank/authoring'))
import fitz
from ru_review_2015_ol import question_text,source_split
from ru_review_2026_hl import squash,between
from ru_paper import bag,score
METADATA={'paper': {'pages': 16, 'sha256': 'd6687ec578dd821b52da934b60d69713a76c9d22bfe2740bc57572f335a35da7'}, 'aural': {'pages': 8, 'sha256': '4168e975614c8d0dcdcf5399c36e2b28e91413519faf87f828974ce1043baf79'}, 'scheme': {'pages': 20, 'sha256': '3a850731dfc2acd40b0df080a8910776105b541dee97dadaa94c353331a5360a'}}

def source_records():
    metadata=METADATA
    docs = {}
    for kind, relative in [('paper', 'papers/2018-hl-000-paper.pdf'),
                           ('aural', 'papers/2018-hl-A00-paper.pdf'),
                           ('scheme', 'schemes/2018-hl.pdf')]:
        path = ROOT / 'examiner-reports/russian' / relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == metadata[kind]['sha256']
        docs[kind] = fitz.open(path)
    Q, A, S = docs['paper'], docs['aural'], docs['scheme']

    def page(doc, n, right=False):
        # Preserve low-page guidance. In this pinned scheme the extracted
        # standalone page number precedes the page's body; remove only it.
        rect = fitz.Rect(295, 30, 580, 793) if right else fitz.Rect(20, 30, 580, 793)
        text = doc[n-1].get_text(clip=rect, sort=False).replace('\uf0b7', '•').replace('\xa0', ' ')
        if doc is S:text=re.sub(r'^\s*'+str(n-2)+r'\s*\n','',text,count=1)
        return re.sub(r'^[^\n]*Lch\s+\d+\s+de\s+\d+[^\n]*Page\s+\d+\s+of\s+\d+[^\n]*\n?', '', text, flags=re.M)

    norm = lambda t: re.sub(r'[^\w]', '', t.casefold())

    def numbered_blocks(text):
        heads=list(re.finditer(r'^\s*(\d)\.\s*(?:(iv|i{1,3})\.?\s*)?(?=[A-Z“])',text,re.M))
        return [(int(h.group(1)),h.group(2),text[h.end():heads[n+1].start() if n+1<len(heads) else len(text)]) for n,h in enumerate(heads)]

    def record(unit, item, roman, question, qp, body, sp, total, **extra):
        component = 'aural' if unit in ('L1', 'L2', 'L3', 'L4') else 'paper'
        assert any(norm(question) in norm(' '.join(page(docs[component], p, right=right) for p in qp))
                   for right in (False, True)), (unit, item, roman, question)
        return dict(id='ru-2018-hl-' + unit.lower() + (f'-{item}' if item is not None else '') + (f'-{roman}' if roman else ''),
                    unit=unit, item=item, roman=roman, question=question, questionPages=qp,
                    component=component, publishedSourceBlock=squash(body), schemePages=sp,
                    publishedTotal=total, **extra)

    cards = []
    source='\n'.join(page(S,p) for p in (4,5)).split('Q.1.2.')[0]
    blocks=numbered_blocks(source)
    asks=[(i,r,question_text(q),p) for p in (3,4) for i,r,q in numbered_blocks(page(Q,p,True))]
    assert len(blocks)==len(asks)==9
    totals=[2,2,6,6,4,4,6,8,2]
    for (i,r,b),(qi,qr,q,p),total in zip(blocks,asks,totals):
        assert (i,r)==(qi,qr)
        price=re.search(r'(\d)\s*x\s*2\s*=\s*(\d)',b)
        assert price and int(price.group(2))==total
        cue,body=b[:price.start()],b[price.start():]
        assert score(bag(q),bag(cue))>.75,(q,cue)
        cards.append(record('C1',i,r,q,[p],body,[4,5],total))
    assert sum(c['publishedTotal'] for c in cards)==40

    summary_source='\n'.join(page(S,p) for p in (6,7)).split('Q.2.2.')[0]
    blocks=numbered_blocks(summary_source)
    assert len(blocks)==4
    for i,r,b in blocks:
        p={1:6,2:7,3:8,4:9}[i]
        q=question_text(page(Q,p,True).split(f'Section {i}',1)[1])
        price=re.search(r'\(4 x 2\)\s*\+2=10',b);assert price
        cue,body=b[:price.start()],b[price.start():]
        assert score(bag(q),bag(cue))>.75,(q,cue)
        cards.append(record('C2',i,None,q,[p],body,[6,7],10,
                            scoring=dict(detail=2,detailQuota=4,discretionaryMaximum=2,incompleteDiscretionaryMaximum=1),
                            reviewNote='Original2018 rubric omits a general1-mark partial-detail rule. Names require category or translation; bare Russian name without category receives0.',
                            pending='Summary4 cannot receive2 discretionary marks unless sequence understood; actual cap flag required.' if i==4 else ''))

    q='Supply the infinitive '+squash(between(page(Q,5,True),'Supply the infinitive'))
    q=q[:q.index('of the text.')+len('of the text.')]
    b='Q.1.2. '+between(page(S,5),'Q.1.2.')
    rows=[[squash(v or '') for v in row] for row in S[4].find_tables().tables[0].extract()]
    assert len(rows)==10
    cards.append(record('LA1',None,None,q,[5],b,[5],10,answerRows=rows,scoring=dict(choose=5,available=9,perInfinitive=2),reviewNote='Preserve each supplied aspect; pool includes imperfective and perfective verbs.'))
    q='Find ten words '+question_text(between(page(Q,9,True),'Find ten words'))
    q=q[:q.index('in Russian.')+len('in Russian.')]
    b='Q.2.2. '+between(page(S,7),'Q.2.2.')
    cards.append(record('LA2',None,None,q,[9],b,[7],10,scoring=dict(words=10,perWord=1),reviewNote='Any case/number; full two-column pool retained; given example певец excluded.'))
    q='Read the following brief news items. '+squash(between(page(Q,10,True),'Read the following brief news items.'))
    q=q[:q.index('(20 marks)')+len('(20 marks)')]
    rows=[[squash(v or '') for v in row] for row in S[7].find_tables().tables[0].extract()]
    assert [re.findall(r'\d+',r[0]) for r in rows]==[['9'],['7'],['1','2'],['10'],['3'],['6','10'],['5'],['2'],['8'],['4']]
    cards.append(record('SD',None,None,q,[10],page(S,8),[8],20,answerRows=rows,scoring=dict(correctAnswers=10,perAnswer=2)))
    q='Read through the following text. '+squash(between(page(Q,11,True),'Read through the following text.'))
    q=q[:q.index('(30 marks)')+len('(30 marks)')]
    cards.append(record('GR',None,None,q,[11],page(S,9),[9],30,sourcePages=[11,12],scoring=dict(correctForms=15,perForm=2),reviewNote='Phrase школьных занятий contains two priced forms inside one gap. Latin letters and wrong tense earn0 per printed rule.'))
    q='Write a short essay '+squash(between(page(Q,13,True),'Write a short essay'))
    q=q[:q.index('(30 marks)')+len('(30 marks)')]
    cards.append(record('SE',None,None,q,[13],'\n'.join(page(S,p) for p in (10,11)),[10,11],30,fullQuestionPage=page(Q,13),pending='Unresolved Lower A contradiction: prose9–14 versus bracket/table9–11,12–14,15–16. No adjudication. All five topics retained.'))
    q='Write a piece '+question_text(page(Q,14,True).split('Write a piece',1)[1])
    cards.append(record('GW',None,None,q,[14],'\n'.join(page(S,p) for p in (12,13,14)),[12,13,14],40,pending='Shared conditional Lower A range7–12; all three writing choices retained.'))
    assert len(cards)==19 and sum(c['publishedTotal'] for c in cards)==220

    source='\n'.join(page(S,p) for p in (15,16,17))
    heads=list(re.finditer(r'^\s*Section (IV|III|II|I|1)\b[^\n]*$',source,re.M|re.I))
    assert len(heads)==4
    counts=[[1,1,2,2,2,2],[2,1,1,4,2],[1,1,3,3,2],[2,2,3,3]]
    starts=[['A sofa','3pm/','Ivanova','30%','4pm train','Student/she'],
            ['1992 +','She knew only','The role suits','elite ballet','7 years old'],
            ['4 days','40,000 visitors','(They will be able','15 interactives','Taste/own'],
            ['(She is one','it was difficult','Mainly she does','Loves Ireland']]
    topics=[['russian-0-9']*6,['russian-0-4','russian-0-3','russian-0-4','russian-0-3','russian-0-1'],['russian-0-7']*5,['russian-0-4','russian-0-4','russian-0-4','russian-2-3']]
    for n,h in enumerate(heads):
        section=n+1;b=source[h.end():heads[n+1].start() if n+1<len(heads) else len(source)]
        blocks=numbered_blocks(b)
        asks=[(i,r,question_text(q)) for i,r,q in numbered_blocks(page(A,section+1,True))]
        assert len(blocks)==len(asks)==len(counts[n]),(section,len(blocks),len(asks))
        for (i,r,b),(qi,qr,q),count,start,topic in zip(blocks,asks,counts[n],starts[n],topics[n]):
            assert (i,r)==(qi,qr)
            cue,body=source_split(b,start)
            assert score(bag(q),bag(cue))>.75,(q,cue)
            sp=[15,16] if section==1 else [16] if section==2 else [17]
            cards.append(record(f'L{section}',i,r,q,[section+1],body,sp,count*2,detailQuota=count,topicId=topic,
                                pending='Generalp15 expressly permits combined half-details; preserve specific husband/she going round Dublin example at2, no marks for museums, no invented2 perhalf.' if (section,i,r)==(4,1,'ii') else ''))
    assert len(cards)==39 and sum(c['publishedTotal'] for c in cards)==300
    assert len({c['id'] for c in cards})==39
    for c in cards:assert norm(c['publishedSourceBlock']) in norm('\n'.join(page(S,p) for p in c['schemePages'])),c['id']
    draft=dict(status='Source-only draft; not runtime cards or a completed sitting',sources=metadata,
               independentTasks=39,writtenTasks=19,listeningTasks=20,printedExamTotal=300,sourceLeafTotal=300,
               generalWrittenGuidance=squash(page(S,3)),comprehensionGuidance=squash(page(S,4).split('1.i.')[0]),
               summaryGuidance=squash(summary_source[:re.search(r'^\s*1\.\s+[A-Z]',summary_source,re.M).start()]),
               listeningGuidance=squash(source[:heads[0].start()]),tasks=cards)
    return docs,draft


from ru_review_2026_hl import base as common_base, as_points, save_reviewed

def base(*args, **kwargs):
    card=common_base(*args, **kwargs)
    for key in ('id','questionRef'):card[key]=card[key].replace('2026','2018')
    card['year']=2018
    card['sourceMaterial']['title']=card['sourceMaterial']['title'].replace('2026','2018')
    return card

def source_card(record):
    pages={'C1':[2,3,4],'LA1':[2,3,4,5],'C2':[6,7,8,9],'LA2':[6,7,8,9],'GR':[11,12]}.get(record['unit'],record['questionPages'])
    c=base(record['unit'],record['question'],record['publishedTotal'],pages,record['schemePages'],record['item'],record['roman'])
    c['review']['questionPages']=record['questionPages']
    return c

def manual_details(record,count,steps,guidance,note):
    c=as_points(source_card(record),[],count)
    c['rubric']['groups']=[{'id':f'detail-{i}','label':f'Manual distinct detail {i}','rows':[],
        'criteria':[{'id':f'detail-{i}-credit','label':f'Distinct detail {i}','maxMarks':2,'permittedMarks':steps,'guidance':[]}]} for i in range(1,count+1)]
    c['rubric']['taskRequirements']=guidance
    c['rubric']['markingGuideNote']=note
    return c

def reading(source):
    result=[]
    for r in source['tasks']:
        if r['unit']!='C1':continue
        body=r['publishedSourceBlock'];key=(r['item'],r['roman'])
        if key in ((3,'i'),(3,'ii'),(4,'i')):
            steps=[0,1,2] if key in ((3,'i'),(4,'i')) else [0,2]
            note='Manually assess each distinct detail against the complete published pool. A detail earns credit once; no unprinted partial-to-full association is enforced.'
            if key in ((3,'i'),(4,'i')):note+=' The one-mark option applies only to the literal partial wording printed in this question.'
            if key==(3,'ii'):note+=' The separate Anna sentence remains in its original source position; no missing separator or relocation is inferred.'
            c=manual_details(r,r['publishedTotal']//2,steps,[source['comprehensionGuidance'],body],note)
        else:
            full=body.split('assign two marks:',1)[1]
            rejected=''
            if 'assign no marks:' in full:full,rejected=full.split('assign no marks:',1)
            # Cross-section permission remains part of the visible literal pool.
            # It is not silently converted into an independently priced phrase.
            if 'Accept details from Section 4' in full:
                c=manual_details(r,r['publishedTotal']//2,[0,2],[source['comprehensionGuidance'],body],
                    'Manually assess two distinct details, including the exact cross-section allowance printed by the scheme. Do not reuse the same information for multiple awards.')
            else:
                answers=[squash(x) for x in full.split('+') if squash(x)]
                c=as_points(source_card(r),answers,r['publishedTotal']//2)
                c['rubric']['taskRequirements']=[source['comprehensionGuidance']]+(['assign no marks: '+squash(rejected)] if rejected else [])
        c['review']['guidancePages']=[4]
        result.append(c)
    assert len(result)==9 and sum(c['totalMarks'] for c in result)==40
    return result

def summaries(source):
    result=[];general=source['summaryGuidance']
    incomplete=re.search(r'If a candidate fails.*?discretionary mark\)',general).group()
    for r in source['tasks']:
        if r['unit']!='C2':continue
        c=manual_details(r,4,[0,2],[general,r['publishedSourceBlock']],
            'Manual assessment: use four distinct details under the printed content rule. The complete main-point and secondary-detail guidance remains above. This sitting does not print a general one-mark partial-content tariff.')
        limits=[{'id':'incomplete-response','maxMarks':1,'when':{'any':[{'flag':'incomplete-response','prompt':incomplete}]},'guidance':[incomplete]}]
        if r['item']==4:
            sequence=re.search(r'Do not give 2 bonus marks.*?understood\.',r['publishedSourceBlock']).group()
            limits.append({'id':'sequence-not-understood','maxMarks':1,'when':{'any':[{'flag':'sequence-not-understood','prompt':sequence}]},'guidance':[sequence]})
            c['rubric']['markingGuideNote']+=' Source discrepancy: original paper page 8 prints www.scherbackov.ru; scheme page 7 prints www.scherbakov.ru. Both original spellings are retained without adjudicating the website.'
        c['rubric']['criteria']=[{'id':'summary-skills','label':'Discretionary marks','maxMarks':2,'permittedMarks':[0,1,2],'guidance':[general],'limits':limits}]
        if r['item']==2:
            # The sentence continues across physical pages 6–7. Keep both
            # literal slices, without joining through the printed footer.
            first,last=r['publishedSourceBlock'].split('people who understand/ listen',1)
            c['rubric']['taskRequirements']=[general,first,'people who understand/ listen'+last]
        c['review']['guidancePages']=[6]
        result.append(c)
    assert len(result)==4 and sum(c['totalMarks'] for c in result)==40
    return result

def listening(source):
    result=[]
    audio=next(row['source'] for row in json.loads((ROOT/'data/russianAudio.json').read_text()) if row['year']==2018)
    for r in source['tasks']:
        if not re.fullmatch(r'L[1-4]',r['unit']):continue
        c=manual_details(r,r['detailQuota'],[0,2],[source['listeningGuidance'],r['publishedSourceBlock']],
            'Manual assessment: apply the printed two-mark point rule to distinct responses. The source also permits a combination of half-details from two segments to earn one two-mark award. Do not price each half separately or reuse the same evidence in another slot. No one-mark atom tariff is inferred.')
        if r['id']=='ru-2018-hl-l4-1-ii':
            c['rubric']['markingGuideNote']+=' The exact published example gives two marks for the husband and Tatyana going round Dublin, and no marks for museums. Assess that combined response once; it does not fill both two-mark slots.'
        c['review']['guidancePages']=[15]
        c['topicId']=r['topicId'];c['additionalTopicIds']=['russian-1-0']
        c['sourceMaterial']['kind']='source-question'
        c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
        c['audioMaterial']=audio
        result.append(c)
    assert len(result)==20 and sum(c['totalMarks'] for c in result)==80
    return result

def grammar_forms(document):
    page=document[8]
    chars=[char for block in page.get_text('rawdict')['blocks'] if 'lines' in block
           for line in block['lines'] for span in line['spans'] for char in span['chars']]
    underlines=[drawing['rect'] for drawing in page.get_drawings()
                if drawing['rect'].y0>260 and drawing['rect'].height<2 and drawing['rect'].width>5]
    answers=[]
    for box in underlines:
        # Select the original characters on the underline's baseline, rather
        # than a tall clip that can include text from the preceding line.
        selected=[char for char in chars if box.y0-5 <= char['origin'][1] <= box.y0+1
                  and box.x0-1 <= (char['bbox'][0]+char['bbox'][2])/2 <= box.x1+1]
        text=squash(''.join(char['c'] for char in selected)).strip('.,')
        assert text,(list(box),selected)
        answers.extend(text.split())
    assert len(underlines)==14 and len(answers)==15,answers
    assert answers[5:7]==['школьных','занятий'],answers
    return answers


def language_and_matching(docs,source):
    records={r['unit']:r for r in source['tasks'] if r['unit'] in ('LA1','LA2','SD','GR')}
    result=[]
    r=records['LA1'];rows=r['answerRows'][1:];assert len(rows)==9
    c=as_points(source_card(r),[row[0]+' — '+row[-1] for row in rows],5)
    c['rubric']['taskRequirements']=[r['publishedSourceBlock'].split('связывают',1)[0]]
    c['rubric']['markingGuideNote']='Choose five of the nine supplied verbs. Preserve the supplied aspect and the published no-credit alternatives; no additional award is available for the printed example.'
    result.append(c)
    r=records['LA2']
    pool='альбом'+between(docs['scheme'][6].get_text(),'альбом')
    words=[squash(word).rstrip('.') for word in re.split(r'[,\n]',pool) if squash(word)]
    assert len(words)==29,words
    assert words[7:9]==['записать','звезда'] and words[-1]=='эстрадная (музыка)',words
    c=as_points(source_card(r),words,10)
    for group in c['rubric']['groups']:group['rows'][0]['marks']=1
    c['rubric']['taskRequirements']=[r['publishedSourceBlock'].split('альбом',1)[0]]
    c['rubric']['markingGuideNote']='Choose ten different accepted words. Each printed slash or parenthesis entry is one option; do not claim the same supplied word twice. The printed example is not an additional answer in this pool.'
    result.append(c)
    r=records['SD'];rows=r['answerRows'];assert len(rows)==10
    c=as_points(source_card(r),[row[0]+' — '+row[1] for row in rows],10)
    c['rubric']['taskRequirements']=['2 marks for each correct answer 10 x 2 = 20']
    c['rubric']['markingGuideNote']='The answers follow the ten original news items from top to bottom. Each printed slash pair is an alternative for that item; no rule requiring each section number to be used once is added.'
    result.append(c)
    r=records['GR'];answers=grammar_forms(docs['scheme'])
    c=as_points(source_card(r),answers,15)
    c['rubric']['taskRequirements']=['TWO marks per correct form 15 x 2 = 30',
        'In this exercise'+between(r['publishedSourceBlock'],'In this exercise','Мой день')]
    c['rubric']['markingGuideNote']='Assess all fifteen correct forms in the complete exercise. The printed prompt школьные занятия contains two words: школьных and занятий each use one two-mark form slot. No one-mark partial award is printed.'
    result.append(c)
    assert len(result)==4 and sum(c['totalMarks'] for c in result)==70
    return result


def writing(docs,source):
    from ru_review_2017_hl import band
    r=next(r for r in source['tasks'] if r['unit']=='GW')
    c=source_card(r);c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
    body=r['publishedSourceBlock']
    content=between(body,'1. Communication/content (C)','2. Expression (E):')
    expression=between(body,'2. Expression (E):','Lower E Ex 10')
    lower_e=re.search(r'If the content mark.*?indicate this\.',expression).group()
    lower_a=re.search(r'If the expression is very fluent.*?indicate this\.',expression).group()
    soft=re.search(r'Penalise students.*?\(–1 or – 2\)\.',expression).group()
    normal=[];lower=[]
    tables=docs['scheme'][13].find_tables().tables;assert len(tables)==3
    for low,full,description in tables[0].extract()[1:]:
        normal.append(band(full,description));lower.append(band(low,description))
    accuracy=[band(price,description) for price,description in tables[1].extract()[1:]]
    assert [b['marks'] for b in accuracy]==[[11,12],[9,10],[7,8]]
    coherence=[band(price,description) for price,description in tables[2].extract()[1:]]
    limits=[{'id':'lower-e','scaleLabel':'Lower E','maxMarks':10,
             'when':{'any':[{'criterionIds':['content'],'atMost':7},{'length':'words','below':60}]},
             'guidance':[lower_e],'bands':lower},
            {'id':'lower-a','scaleLabel':'Lower A','minMarks':7,'maxMarks':12,
             'when':{'any':[{'flag':'lower-a','prompt':lower_a}]},'guidance':[lower_a],'bands':accuracy}]
    prompts,tariffs=body.split('1. Communication/content (C)',1)[0].split('Communication + content',1)
    c['rubric']={'system':'language-writing','taskRequirements':[prompts,'Communication + content'+tariffs,source['generalWrittenGuidance'].split('Language issues',1)[0]],
        'markingGuideNote':'Manually assess the selected response against all its original categories, including at least one detail from each required category. The scheme supplies one mark per content detail, without a fixed per-category split. Lower A and Lower E retain their own source tables; no descriptor conversion or minimum award is inferred.',
        'criteria':[{'id':'content','label':'Communication/content (C)','maxMarks':15,'permittedMarks':list(range(16)),'guidance':[squash(content)]},
                    {'id':'expression','label':'Language + expression (E)','maxMarks':15,'permittedMarks':list(range(16)),
                     'guidance':[squash(expression)],'bands':normal,'limits':limits},
                    {'id':'coherence','label':'Textual coherence (TC)','maxMarks':10,'permittedMarks':list(range(11)),
                     'guidance':['3. Textual coherence:'+between(body,'3. Textual coherence:','Mark Textual coherence')],'bands':coherence},
                    {'id':'soft-sign-penalty','label':'Soft sign penalty','kind':'deduction','deductFrom':'expression','maxMarks':2,'permittedMarks':[0,1,2],'guidance':[soft]}]}
    c['review']['guidancePages']=[3]
    return c


def cultural_confidence(source):
    r=next(r for r in source['tasks'] if r['unit']=='SE')
    c=source_card(r)
    choices='Напишите'+between(r['fullQuestionPage'],'Напишите').split('___')[0]
    assert all(f'{n}.' in choices for n in range(1,6))
    c['questionText']+='\n\n'+choices
    c['kind']='question';c['tariffModel']={'kind':'questionTotal'}
    instruction,table=r['publishedSourceBlock'].split('Mark Language: lexis, accuracy, fluency',1)
    c['rows']=[{'id':'published-guidance','kind':'point','marks':None,'verbatim':instruction,
        'contextNote':'Confidence review: the whole question is printed as 30 marks, with content 10 and expression 20. Its Lower A instruction says between 9 and 14, but the same instruction and table include 15–16. Both original versions and every other scoring instruction are retained. No Lower A ceiling is selected and this card does not calculate a numerical score. All five original choices, the 50-word Russian response, five factual details and title remain required as printed.'}]
    c['rows'].append({'id':'published-expression-grid','kind':'point','marks':None,'verbatim':'Mark Language: lexis, accuracy, fluency'+table})
    return c


def source_language_rules(cards,source):
    rule='Language of answer:'+between(source['generalWrittenGuidance'],'Language of answer:','Quality of English:')
    exception=re.search(r'Discretionary marks \(as opposed to content marks\) may be awarded.*?answers\)\.',source['summaryGuidance']).group()
    for c in cards:
        if c['section'] not in ('C1','C2','LA1','LA2','GR','GW'):continue
        c['answerLanguageRule']={'otherLanguageMultiplier':0,'sourceText':squash(rule),'schemePages':[3]}
        if c['section'] in ('C1','C2'):
            c['rubric']['markingGuideNote']+=' Answer in English or Irish, as permitted by the original bilingual paper.'
        if c['section']=='C2':
            c['answerLanguageRule']['manualCriterionExceptions']={'criterionIds':['summary-skills'],'sourceText':exception,'schemePages':[6]}


def build():
    docs,source=source_records()
    try:
        cards=reading(source)+summaries(source)+language_and_matching(docs,source)+[writing(docs,source),cultural_confidence(source)]+listening(source)
        source_language_rules(cards,source)
        assert len(cards)==len({c['id'] for c in cards})==39
        assert sum(c['totalMarks'] for c in cards)==300
        assert sum(c['totalMarks'] for c in cards if c['section']!='SE')==270
        assert sum(bool(c.get('answerLanguageRule')) for c in cards)==17
        return cards
    finally:
        for document in docs.values():document.close()


def raw_scheme_text():
    path=ROOT/'examiner-reports/russian/schemes/2018-hl.pdf'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==METADATA['scheme']['sha256']
    with fitz.open(path) as document:
        pages=[page.get_text() for page in document]
        raw='\n\n'.join(f'## Page {n+1}\n\n'+text for n,text in enumerate(pages))+'\n'
        # The shared provenance comparator removes standalone numeric lines.
        # Preserve a second original-page form with only line wraps joined, so
        # complete quoted grids retain their printed marks without any new text.
        joined='\n\n'.join(f'### Joined original page {n+1}\n\n'+squash(text) for n,text in enumerate(pages))
        return raw+'\n# Original pages with line wraps joined\n\n'+joined+'\n'


if __name__=='__main__':
    save_reviewed(build())
    (ROOT/'examiner-reports/russian/schemes/2018-hl.md').write_text(raw_scheme_text())
