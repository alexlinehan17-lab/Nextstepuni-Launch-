"""Russian 2017 Higher: independently counted original-paper selectors and scoring."""
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

METADATA = {'paper': {'pages': 16, 'sha256': 'f25024625e703cada8bdaf6f3acb2713be820b6d5e9e5ce640087fdcbcd65815'}, 'aural': {'pages': 8, 'sha256': 'd704a57c8d5b3bded04a8c0da5f3ebacbbea06968dcdb2db2c14f164d1ca262b'}, 'scheme': {'pages': 20, 'sha256': '4436cf9e87767e3d7092bedbb38ad8818b731d232565d2d0fca1976621e95abd'}}

def source_records():
    docs = {}
    for kind, relative in [('paper', 'papers/2017-hl-000-paper.pdf'),
                           ('aural', 'papers/2017-hl-A00-paper.pdf'),
                           ('scheme', 'schemes/2017-hl.pdf')]:
        path = ROOT / 'examiner-reports/russian' / relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == METADATA[kind]['sha256']
        docs[kind] = fitz.open(path)
    Q, A, S = docs['paper'], docs['aural'], docs['scheme']

    def page(doc, n, right=False):
        return doc[n-1].get_text(clip=fitz.Rect(295, 30, 580, 793) if right else fitz.Rect(20, 30, 580, 775), sort=False).replace('\uf0b7', '•').replace('\xa0', ' ')

    def record(unit, item, roman, question, qp, body, sp, total, **extra):
        component = 'aural' if unit in ('L1', 'L2', 'L3', 'L4') else 'paper'
        norm = lambda t: re.sub(r'[^\w]', '', t.casefold())
        assert norm(question) in norm(' '.join(page(docs[component], p, right=True) for p in qp)), (unit, item, roman, question)
        return dict(id='ru-2017-hl-' + unit.lower() + (f'-{item}' if item is not None else '') + (f'-{roman}' if roman else ''),
                    unit=unit, item=item, roman=roman, question=question, questionPages=qp,
                    component=component, publishedSourceBlock=squash(body), schemePages=sp,
                    publishedTotal=total, **extra)

    cards = []
    source = '\n'.join(page(S, p) for p in (4, 5)).split('Q.1.2')[0]
    blocks = numbered_blocks(source)
    asks = [(i, r, question_text(q), p) for p in (2, 3, 4) for i, r, q in numbered_blocks(page(Q, p, True))]
    assert len(blocks) == len(asks) == 10, (blocks, asks)
    starts = ['Candidates are required', 'usual time', 'when he was squeezing', 'gas company', 'engineer +',
              'Candidates are required', '(large) python', 'Candidates are required', 'zoo employees', '(free) ticket']
    totals = [4, 6, 2, 2, 6, 8, 4, 4, 2, 2]
    for (i, r, b), (qi, qr, q, p), start, total in zip(blocks, asks, starts, totals):
        assert (i, r) == (qi, qr)
        cue, body = source_split(b, start)
        assert score(bag(q), bag(cue)) > .8, (q, cue)
        cards.append(record('C1', i, r, q, [p], body, [4, 5], total))
    assert sum(c['publishedTotal'] for c in cards) == 40

    summary_source = '\n'.join(page(S, p) for p in (6, 7)).split('Q.2.2')[0]
    summary_heads = list(re.finditer(r'^\s*Section\s+([1-4])\s*$', summary_source, re.M))
    summary_asks = []
    for p in (7, 8):
        t = page(Q, p, True).split('Q.2.2')[0]
        heads = list(re.finditer(r'^\s*Section\s+([1-4])\s*$', t, re.M))
        summary_asks.extend((int(h.group(1)), question_text(t[h.end():heads[n+1].start() if n+1 < len(heads) else len(t)]), p)
                            for n, h in enumerate(heads))
    assert len(summary_heads) == len(summary_asks) == 4, (summary_heads, summary_asks)
    for n, (h, (i, q, p)) in enumerate(zip(summary_heads, summary_asks)):
        assert int(h.group(1)) == i
        b = summary_source[h.end():summary_heads[n+1].start() if n+1 < len(summary_heads) else len(summary_source)]
        cue, body = source_split(b, 'primary details:')
        assert score(bag(q), bag(cue)) > .8
        cards.append(record('C2', i, None, q, [p], body, [6, 7], 10,
                            scoring=dict(detail=2, contentMaximum=8, discretionaryMaximum=2,
                                         partialDetail=1, incompleteDiscretionaryMaximum=1)))

    # All ten original case prompts stay visible. The scheme explicitly awards
    # two per correct response capped at ten; the paper does not say choose five.
    q = 'Indicate the case ' + squash(between(page(Q, 5, True), 'Indicate the case', 'Tuiseal/'))
    q = q[:q.index('Russian)')+len('Russian)')]
    assert q.endswith('Russian)'), repr(q)
    b = 'Indicate the case' + between(page(S, 5), 'Indicate the case')
    table = S[4].find_tables().tables[0].extract()
    rows = [[squash(v or '') for v in row] for row in table[1:]]
    assert len(rows) == 10 and all(r[0] == str(i) for i, r in enumerate(rows, 1)), rows
    cards.append(record('LA1', None, None, q, [5], b, [5], 10,
                        answerRows=rows, scoring=dict(perCorrectAnswer=2, globalMaximum=10),
                        reviewNote='All ten prompts are required. Original paper has no choose-five instruction. Japanese worker independently confirmed both originals. Irish, English and Russian answers are explicitly permitted.'))
    q = 'Find ten words ' + squash(between(page(Q, 8, True), 'Find ten words')).split('6.')[0].strip()
    b = 'Find ten words' + between(page(S, 7), 'Find ten words')
    pool_text = b[b.index('(по)слушать'):]
    words = [squash(w) for w in pool_text.split(',')]
    assert len(words) == 34, words
    cards.append(record('LA2', None, None, q, [8], b, [7], 10,
                        acceptedWords=words, scoring=dict(perCorrectAnswer=1, globalMaximum=10),
                        reviewNote='All 34 separately printed entries preserved, including (по)слушать and послушать. Source accepts any case/form and does not penalise spelling, but excludes the given концерт example and words outside the text.'))
    q = 'Read the following information ' + squash(between(page(Q, 9, True), 'Read the following information'))
    q = q[:q.index('(20 marks)')+len('(20 marks)')]
    table = S[7].find_tables().tables[0].extract()
    rows = [[squash(v or '') for v in row] for row in table]
    assert [r[-1] for r in rows] == ['6','5','2','8','7','1','10','9','3','4'], rows
    cards.append(record('SD', None, None, q, [9], page(S, 8), [8], 20, answerRows=rows,
                        scoring=dict(perCorrectAnswer=2, requiredAnswers=10)))
    q = 'Read through the following text. ' + squash(between(page(Q, 10, True), 'Read through the following text.'))
    q = q[:q.index('(30 marks)')+len('(30 marks)')]
    cards.append(record('GR', None, None, q, [10], page(S, 9), [9], 30,
                        scoring=dict(perCorrectForm=2, requiredForms=15),
                        reviewNote='Retain source singular урокe acceptance and литературным rejection; original general plural-form explanation is part of visible task guidance.'))

    q = 'Write a short essay ' + squash(between(page(Q, 11, True), 'Write a short essay'))
    q = q[:q.index('(30 marks)')+len('(30 marks)')]
    cards.append(record('SE', None, None, q, [11], '\n'.join(page(S, p) for p in (10, 11)), [10, 11], 30,
                        fullQuestionPage=page(Q, 11),
                        pending='Shared conditional Lower A allowed range9–14 with bands9–10/11–12/13–14; no runtime draft until supported.'))
    q = 'Write a piece' + between(page(Q, 12, True), 'Write a piece')
    q = question_text(q)
    cards.append(record('GW', None, None, q, [12], '\n'.join(page(S, p) for p in (12, 13, 14)), [12, 13, 14], 40,
                        pending='Shared conditional Lower A allowed range7–12 with bands7–8/9–10/11–12; no runtime draft until supported.'))
    assert len(cards) == 20 and sum(c['publishedTotal'] for c in cards) == 220

    source = '\n'.join(page(S, p) for p in (15, 16, 17))
    heads = list(re.finditer(r'^\s*Section (1|II|III|IV)\s*$', source, re.M))
    assert len(heads) == 4
    counts = [[2,2,3,3], [1,2,1,2,4], [2,1,4,2,1], [2,2,2,2,2]]
    starts = [
        ['Irish dance studio', '(Thursday) 16th', 'Chess tournament', 'Boxer +'],
        ['International/summer', 'America/USA', '8 participants', 'One detail must', '(Interest) clubs'],
        ['Swimming +', 'At the age of', 'Drawing +', 'Assign one mark', 'Sasha’s grandmother'],
        ['October +', 'Started school', 'Received Government', '(in 2007)', 'goes from country']]
    topics = [
        ['russian-0-5','russian-0-7','russian-0-7','russian-0-5'],
        ['russian-0-3','russian-0-3','russian-0-3','russian-0-7','russian-0-5'],
        ['russian-0-5','russian-0-5','russian-0-5','russian-0-8','russian-0-1'],
        ['russian-0-7','russian-0-3','russian-0-3','russian-2-11','russian-2-2']]
    for n, h in enumerate(heads):
        section = n+1
        b = source[h.end():heads[n+1].start() if n+1 < len(heads) else len(source)]
        blocks = numbered_blocks(b)
        asks = [(i,r,question_text(q)) for i,r,q in numbered_blocks(page(A, section+1, True))]
        assert len(blocks) == len(asks) == len(counts[n])
        for (i,r,b),(qi,qr,q),count,start,topic in zip(blocks, asks, counts[n], starts[n], topics[n]):
            assert (i,r)==(qi,qr) or (section,i,r,qi,qr)==(4,1,None,1,'i')
            cue, body = source_split(b, start)
            assert score(bag(q), bag(cue)) > .8, (q,cue)
            total = 4 if (section,i,r)==(3,3,'i') else count*2
            sp = [15] if section==1 else [16] if section in (2,3) else [17]
            cards.append(record(f'L{section}', qi, qr, q, [section+1], body, sp, total,
                                topicId=topic, detailQuota=count,
                                reviewNote='Country task explicitly awards1 for each country and1 for its detail, for two countries.' if (section,i,r)==(3,3,'i') else ''))
    assert len(cards) == 39 and sum(c['publishedTotal'] for c in cards) == 300
    assert len({c['id'] for c in cards}) == 39
    draft = dict(status='Source-only draft; not runtime cards or a completed sitting', sources=METADATA,
                 independentTasks=39, writtenTasks=20, listeningTasks=19,
                 generalWrittenGuidance=squash(page(S,3)),
                 comprehensionGuidance=squash(source_split('\n'.join(page(S,p) for p in (4,5)), 'Q.1.1')[0]),
                 summaryGuidance=squash(summary_source[:summary_heads[0].start()]),
                 listeningGuidance=squash(source[:heads[0].start()]), tasks=cards)
    return docs, draft


"""Source-bound 2017 writing grids; preparation only until the sitting is gated."""
import re
from ru_review_2026_hl import squash, between, mark_range


def band(price, description):
    return {'label':squash(price),'marks':mark_range(price),'guidance':[squash(description)]}


def writing(docs, source, base):
    S=docs['scheme']; result=[]
    for unit,sp,table_page in [('SE',10,11),('GW',12,13)]:
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
            accuracy=[band(price,description) for price,description in tables[1].extract()[1:]]
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
        annotation=squash(between(expression,'Put a square box' if is_essay else 'Put square box','Penalise students'))
        annotation=('Put a square box' if is_essay else 'Put square box')+' '+annotation
        accommodations=S[table_page-1].get_text().split('Reasonable Accommodations:',1)[1]
        accommodations=accommodations.split('Add the marks',1)[0] if is_essay else accommodations.split('Lower A',1)[0]
        accommodations='Reasonable Accommodations: '+squash(accommodations)
        criteria.append({'id':'expression','label':'Language + expression (E)','maxMarks':maximum,'permittedMarks':list(range(maximum+1)),'guidance':[global_view,annotation,accommodations],'bands':normal,'limits':limits})
        if not is_essay:
            coherence=[band(price,description) for price,description in S[13].find_tables().tables[0].extract()[1:]]
            criteria.append({'id':'coherence','label':'Textual coherence (TC)','maxMarks':10,'permittedMarks':list(range(11)),'guidance':[],'bands':coherence})
        criteria.append({'id':'soft-sign-penalty','label':'Soft sign penalty','kind':'deduction','deductFrom':'expression','maxMarks':1,'permittedMarks':[0,1],'guidance':[soft]})
        c['rubric']={'system':'language-writing','taskRequirements':[],'markingGuideNote':'','criteria':criteria}
        result.append(c)
    return result


from ru_review_2026_hl import base as common_base, as_points, save_reviewed

def base(*args, **kwargs):
    card=common_base(*args, **kwargs)
    for field in ('id','questionRef'):card[field]=card[field].replace('2026','2017')
    card['year']=2017
    card['sourceMaterial']['title']=card['sourceMaterial']['title'].replace('2026','2017')
    return card

def source_card(record):
    pages=[2,3,4] if record['unit']=='C1' else [6,7,8] if record['unit'] in ('C2','LA2') else record['questionPages']
    card=base(record['unit'],record['question'],record['publishedTotal'],pages,record['schemePages'],record['item'],record['roman'])
    card['review']['questionPages']=record['questionPages']
    return card

def options(text):
    return [squash(x) for x in text.split('+') if squash(x)]

def named_group(id,label,answers,quota=1,marks=2,partials=()):
    return {'id':id,'label':label,'answerCount':quota,'rows':[{'id':f'full-{i}','text':x,'marks':marks} for i,x in enumerate(answers,1)]+[{'id':f'partial-{i}','text':x,'marks':1} for i,x in enumerate(partials,1)]}


def reading(source):
    cards=[]
    for record in source['tasks']:
        if record['unit']!='C1':continue
        key=(record['item'],record['roman']);body=record['publishedSourceBlock']
        card=as_points(source_card(record),[],record['publishedTotal']//2)
        if key==(1,None):
            reaction=between(body,'reaction:','(2) when it changed:')
            changed=between(body,'when it changed:','(2) Assign 1 mark:')
            partial=between(body,'Assign 1 mark:')
            card['rubric']['groups']=[named_group('reaction','First reaction',options(reaction)),named_group('changed','When the attitude changed',[squash(changed)],partials=[squash(partial)])]
        elif key==(3,'ii'):
            first=between(body,'policeman 1:','(4) policeman 2:')
            second=between(body,'policeman 2:').removesuffix('(4)').strip()
            card['rubric']['count']=2
            card['rubric']['groups']=[named_group('policeman-1','Policeman 1',options(first),2),named_group('policeman-2','Policeman 2',options(second),2)]
            assert [len(g['rows']) for g in card['rubric']['groups']]==[4,3]
        elif key==(4,'ii'):
            where=between(body,'where:','(2) what:');what=between(body,'what:','(2) Assign 1 mark:')
            partial=between(body,'Assign 1 mark:','Assign no marks:')
            card['rubric']['groups']=[named_group('where','Where',options(where),partials=options(partial)),named_group('what','What',[squash(what)])]
            card['rubric']['taskRequirements']=['Assign no marks: '+squash(between(body,'Assign no marks:'))]
        else:
            rejected=''
            if 'Assign no marks:' in body:body,rejected=body.split('Assign no marks:',1)
            partial=''
            if 'Assign 1 mark:' in body:body,partial=body.split('Assign 1 mark:',1)
            body=re.sub(r'\s*\(\d+\)\s*$','',body).strip()
            answers=options(body);partial_answers=options(partial)
            if key==(2,'i'):
                assert len(answers)==7 and len(partial_answers)==4
                card=as_points(source_card(record),answers,3,{6:partial_answers})
            elif key==(3,'i'):
                assert len(answers)==6 and partial_answers==['briefcase']
                card=as_points(source_card(record),answers,3,{5:partial_answers})
            else:
                if key==(4,'i'):
                    assert len(answers)==4 and '// two animals//' in answers[1]
                    answers[1]=answers[1].replace('// two animals//','').strip()
                card=as_points(source_card(record),answers,record['publishedTotal']//2)
                for i,partial_answer in enumerate(partial_answers,1):
                    card['rubric']['groups'].append(named_group(f'partial-{i}','Published partial answer',[partial_answer],marks=1))
            if key==(4,'i'):
                card['rubric']['markingGuideNote']='Published pool: '+record['publishedSourceBlock']+' Apply the printed synthesis guidance to a response expressing both animal concepts. The general two-animals wording is retained without a separate priced row.'
            if rejected:card['rubric']['taskRequirements']=['Assign no marks: '+squash(rejected)]
        card['rubric']['taskRequirements'].insert(0,source['comprehensionGuidance'])
        if key in [(1,None),(3,'ii'),(4,'ii')]:
            card['rubric']['taskRequirements'].append(squash(body.split(':',1)[0])+':')
        card['review']['guidancePages']=[4]
        cards.append(card)
    assert len(cards)==10 and sum(c['totalMarks'] for c in cards)==40
    return cards


def language_and_matching(docs,source):
    records={r['unit']:r for r in source['tasks'] if r['unit'] in ('LA1','LA2','SD','GR')}
    cards=[]
    r=records['LA1'];rows=r['answerRows'];assert len(rows)==10
    c=as_points(source_card(r),[row[1]+' — '+row[2] for row in rows],10)
    cap='Give two marks'+between(r['publishedSourceBlock'],'Give two marks','Accept any answer')
    c['rubric']['allocationCap']={'maxMarks':10,'sourceText':squash(cap),'schemePages':[5]}
    c['rubric']['taskRequirements']=['Accept any answer'+between(r['publishedSourceBlock'],'Accept any answer','1 (напечатать)')]
    c['rubric']['markingGuideNote']='All ten printed prompts remain required. The published award is 2 marks per correct answer, capped at 10 overall; the paper does not give a choose-five instruction.'
    cards.append(c)
    r=records['LA2'];answers=r['acceptedWords'];assert len(answers)==34
    c=as_points(source_card(r),answers,10)
    for g in c['rubric']['groups']:g['rows'][0]['marks']=1
    # The optional prefix and the repeated prefixed entry refer to the one
    # supplied passage word. Both published entries remain visible, one credit.
    passage=' '.join(docs['paper'][page-1].get_text() for page in (6,7,8))
    assert len(re.findall(r'(?<![А-Яа-яЁё])послушать(?![А-Яа-яЁё])',passage))==1
    assert not re.search(r'(?<![А-Яа-яЁё])слушать(?![А-Яа-яЁё])',passage)
    first=answers.index('(по)слушать');duplicate=answers.index('послушать')
    c['rubric']['groups'][first]['label']='One passage word: accepted forms'
    c['rubric']['groups'][first]['rows'].append({'id':'prefixed-form','text':answers[duplicate],'marks':1})
    c['rubric']['groups'].pop(duplicate)
    assert len(c['rubric']['groups'])==33 and sum(len(g['rows']) for g in c['rubric']['groups'])==34
    c['rubric']['markingGuideNote']='The scheme prints both (по)слушать and послушать. The original passage on page 6 contains one supplied word, послушать. Both printed entries are retained as accepted forms of that one passage word; claim its one mark once.'
    c['review']['paperAnswerSources']=[{'text':'послушать','pages':[6],'schemeAcceptance':'Accept words in any case/form; do not penalise spelling mistakes.'}]
    guidance=between(r['publishedSourceBlock'],'Give one mark','(по)слушать')
    c['rubric']['taskRequirements']=['Give one mark'+guidance]
    cards.append(c)
    r=records['SD'];rows=r['answerRows'];assert len(rows)==10
    c=as_points(source_card(r),[row[1]+' — '+row[2] for row in rows],10)
    c['rubric']['taskRequirements']=['2 marks for each correct answer']
    c['rubric']['markingGuideNote']='Answers follow the descriptions from top to bottom in the original table.'
    cards.append(c)
    r=records['GR'];page=docs['scheme'][8];underlined=[]
    for drawing in page.get_drawings():
        box=drawing['rect']
        if box.y0>260 and box.height<2:
            text=page.get_text('text',clip=fitz.Rect(box.x0-1,box.y0-16,box.x1+1,box.y1+2))
            underlined.append(squash(text).strip('.,'))
    assert len(underlined)==17,underlined
    groups=[];exceptions=[]
    for word in underlined:
        if word.startswith('(accept '):
            groups[-1]['rows'].append({'id':'accepted-singular','text':word[len('(accept '):-1],'marks':2})
            exceptions.append(word)
        elif word.startswith('(do not accept '):exceptions.append(word)
        else:groups.append(named_group(f'form-{len(groups)+1}',f'Form {len(groups)+1}',[word]))
    assert len(groups)==15 and sum(len(g['rows']) for g in groups)==16
    c=as_points(source_card(r),[],15);c['rubric']['groups']=groups
    c['rubric']['taskRequirements']=['TWO marks per correct form: 15 x 2 = 30','In this exercise'+between(r['publishedSourceBlock'],'In this exercise','Десять лет')]+exceptions
    c['rubric']['markingGuideNote']='The scheme accepts the indicated singular lesson form but rejects the singular literary adjective where agreement is required. Its full plural-form explanation is retained above.'
    cards.append(c)
    assert len(cards)==4 and sum(c['totalMarks'] for c in cards)==70
    return cards


def listening(docs,source):
    cards=[]
    audio=next(r['source'] for r in json.loads((ROOT/'data/russianAudio.json').read_text()) if r['year']==2017)
    for record in source['tasks']:
        if record['unit'] not in ('L1','L2','L3','L4'):continue
        key=(record['unit'],record['item'],record['roman']);body=record['publishedSourceBlock'];extra=[]
        if key==('L3',3,'i'):
            rule,body=source_split(body,'Austria -')
            pairs=[re.split(r'\s+[–-]\s+',part,maxsplit=1) for part in options(body)]
            assert len(pairs)==4 and all(len(pair)==2 for pair in pairs),pairs
            c=source_card(record);c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
            c['rubric']={'system':'language-writing','criteria':[{'id':id,'label':label,'maxMarks':1,'permittedMarks':[0,1],'guidance':[]} for id,label in [('first-country','First country'),('first-detail','Detail about the first country'),('second-country','Second different country'),('second-detail','Detail about the second country')]],'taskRequirements':[],
                'markingGuideNote':'The scheme groups China/Vietnam in one printed row. It does not clarify whether both may be used as the two country responses. That combination remains unresolved; the controls preserve the published one-mark country and one-mark detail allocation without automatically accepting or rejecting the combination.'}
            extra=[squash(rule)]+options(body)
        elif key==('L2',3,'i'):
            rule,body=source_split(body,'Costa Brava')
            full,partial=body.split('Assign 1 mark:',1);answers=options(full)
            assert len(answers)==5
            c=as_points(source_card(record),[],2)
            c['rubric']['groups']=[named_group('location','Location',answers[:2]),named_group('date','Date',answers[2:],partials=options(partial))]
            extra=[squash(rule)]
        else:
            rejected=''
            if 'Assign no marks:' in body:body,rejected=body.split('Assign no marks:',1)
            full_credit=''
            if 'Assign 2 marks:' in body:body,full_credit=body.split('Assign 2 marks:',1)
            parts=re.split(r'Assign (?:1 mark:|one mark for:)',body,maxsplit=1)
            answers=options(parts[0]);partial=re.sub(r'\s*\(1\)\s*$','',parts[1]).strip() if len(parts)>1 else ''
            partials=options(partial)
            mapping={}
            if key==('L1',1,None):
                assert len(answers)==10 and len(partials)==2
                mapping={5:partials}
            elif key==('L1',2,None):
                assert len(answers)==9 and len(partials)==2
                mapping={0:[partials[0]],4:[partials[1]]}
            elif key==('L2',1,None):mapping={0:partials}
            elif key==('L3',1,'ii'):mapping={4:partials}
            elif key==('L4',1,'i'):
                assert partial=='10th + incorrect month'
                mapping={0:[partial]}
            elif key==('L4',1,'ii'):
                assert len(answers)==9 and len(partials)==3
                mapping={3:[partials[0]],5:[partials[1]],6:[partials[2]]}
            else:assert not partial,(key,partial)
            c=as_points(source_card(record),answers,record['detailQuota'],mapping)
            if full_credit:
                assert key==('L3',1,'i') and answers[1]=='judo'
                c['rubric']['groups'][1]['rows'].append({'id':'accepted-spelling','text':squash(full_credit),'marks':2})
            if rejected:extra.append('Assign no marks: '+squash(rejected))
            if key==('L4',1,'i'):
                c['rubric']['markingGuideNote']='The complete published partial “10th + incorrect month” earns one mark within the month detail. It cannot add to correct October credit. The year and place remain separate details under the two-detail quota.'
        c['rubric']['taskRequirements']=[source['listeningGuidance']]+extra
        c['review']['guidancePages']=[15]
        c['topicId']=record['topicId'];c['additionalTopicIds']=['russian-1-0']
        c['sourceMaterial']['kind']='source-question'
        c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
        c['audioMaterial']=audio
        cards.append(c)
    assert len(cards)==19 and sum(c['totalMarks'] for c in cards)==80
    return cards


def summaries(source):
    cards=[]
    general=source['summaryGuidance']
    incomplete='If a candidate fails'+between(general,'If a candidate fails','Where a candidate supplies')
    incomplete=squash(incomplete)
    for record in source['tasks']:
        if record['unit']!='C2':continue
        body=record['publishedSourceBlock'];secondary=[]
        match=re.search(r'secondary details?:',body,re.I)
        if match:body,secondary=body[:match.start()],options(body[match.end():])
        main=between(body,'primary details:')
        special=None
        if record['item']==4:
            special=re.search(r'everyone was joining in / \[.*?\]',main).group()
            main=main.replace(special,'__SOURCE_ROUTE__')
        primary=options(main)
        primary=[x for x in primary if x!='__SOURCE_ROUTE__']
        c=as_points(source_card(record),primary+secondary,4,steps=[0,1,2],labels=['Primary detail']*len(primary)+['Secondary detail']*len(secondary))
        c['rubric']['taskRequirements']=[general]
        c['rubric']['criteria']=[{'id':'summary-skills','label':'Discretionary marks','maxMarks':2,'permittedMarks':[0,1,2],'guidance':[general],
            'limits':[{'id':'incomplete-response','maxMarks':1,'when':{'any':[{'flag':'incomplete-response','prompt':incomplete}]},'guidance':[incomplete]}]}]
        if special:
            specific=options(between(special,'following:',']'));assert len(specific)==4
            alternative='crowd-joining'
            c['rubric']['alternativeSets']=[{'id':alternative,'label':'How the crowd joined in','sourceText':special,'schemePages':[7]}]
            general_group=named_group('crowd-general','General description',[special.split(' / ')[0]])
            specific_group=named_group('crowd-specific','Specific crowd actions',specific,2)
            for group in [general_group,specific_group]:
                group['alternativeSet']=alternative
                for row in group['rows']:row['steps']=[0,1,2]
            c['rubric']['groups'].extend([general_group,specific_group])
            cap='Award 2 marks'+between(general,'Award 2 marks','AND 2 discretionary marks')
            c['rubric']['allocationCap']={'maxMarks':8,'answerCount':4,'sourceText':squash(cap),'schemePages':[6]}
        cards.append(c)
    assert len(cards)==4 and sum(c['totalMarks'] for c in cards)==40
    return cards


def attach_source_language_rule(cards,docs,source):
    rule='Language of answer:'+between(source['generalWrittenGuidance'],'Language of answer:','Quality of English:')
    rule=squash(rule)
    assert 'award NO marks' in rule and 'listening comprehension' in rule
    for c in cards:
        if c['section'] not in ('C1','C2','LA2','GR','SE','GW'):continue
        c['answerLanguageRule']={'otherLanguageMultiplier':0,'sourceText':rule,'schemePages':[3]}
        if c['section'] in ('C1','C2'):
            c['rubric']['markingGuideNote']=(c['rubric']['markingGuideNote']+' Answer in English or Irish. Both languages are permitted by the original bilingual paper.').strip()


def build():
    docs,source=source_records()
    cards=reading(source)+summaries(source)+language_and_matching(docs,source)+writing(docs,source,base)+listening(docs,source)
    attach_source_language_rule(cards,docs,source)
    assert len(cards)==39 and len({c['id'] for c in cards})==39
    assert sum(c['totalMarks'] for c in cards)==300
    assert sum(bool(c.get('answerLanguageRule')) for c in cards)==18
    for d in docs.values():d.close()
    return cards


if __name__=='__main__':save_reviewed(build())
