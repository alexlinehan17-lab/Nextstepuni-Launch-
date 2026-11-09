#!/usr/bin/env python3
"""2015 Ordinary Russian: 35 written + 19 listening tasks, original sources.

The three separately numbered/priced matching exercises remain separate tasks.
Half-mark handwriting and classification allocations use existing fixed criteria.
"""
import hashlib
import json
import re
import fitz
from ru_paper import RuPaper, bag, score
from ru_review_2026_hl import ROOT, squash, page_text as original_page_text, between, bullets, base as higher_base, as_points, mark_range, save_reviewed
from ru_review_2018_ol import criterion

FILES = {
    'paper': ('papers/2015-ol-000-paper.pdf', '6ac6846e912d21fb2bb26784c390da98e538e0ca6ec40aabfd43acf23025cd1f'),
    'aural': ('papers/2015-ol-A00-paper.pdf', 'aef9d92ffb824252084ce34575e43d03ebe224d7840c9c5f27ca3f7732e24064'),
    'scheme': ('schemes/2015-ol.pdf', '6dab67571e6bf05778257e96590973615860ba212d718eb19742c73cfdf5ef88'),
}

def page_text(doc, page, box=None):
    return original_page_text(doc, page, box or (20, 30, 580, 793)).replace('\uf0b7', '•')

def draw_text(doc, page):
    return doc[page-1].get_text(clip=fitz.Rect(20,30,580,793), sort=False).replace('\uf0b7','•')

def opened_sources():
    docs={}
    for key,(relative,digest) in FILES.items():
        path=ROOT/'examiner-reports/russian'/relative
        assert hashlib.sha256(path.read_bytes()).hexdigest()==digest
        docs[key]=fitz.open(path)
    return docs

def base(unit,text,total,pages,scheme_pages,item=None,roman=None):
    c=higher_base(unit,text,total,pages,scheme_pages,item,roman)
    c['id']=c['id'].replace('2026','2015').replace('-hl-','-ol-')
    c['year']=2015;c['level']='ordinary'
    c['questionRef']=f'2015 OL Section {unit}'+(f' Q{item}' if item is not None else '')
    if roman:c['questionRef']+=(' Q' if item is None else '')+f'({roman})'
    c['sourceMaterial']['title']=f'2015 Ordinary Russian — {unit}'
    return c

def roman_blocks(text):
    heads=list(re.finditer(r'^\s*(ix|viii|vii|vi|iv|v|i{1,3})\.\s+',text,re.M))
    return [(h.group(1),text[h.end():heads[n+1].start() if n+1<len(heads) else len(text)]) for n,h in enumerate(heads)]

def numbered_blocks(text):
    heads=list(re.finditer(r'^\s*(\d)\.\s*(?:(iv|i{1,3})\.\s*)?(?=[A-Z])',text,re.M))
    return [(int(h.group(1)),h.group(2),text[h.end():heads[n+1].start() if n+1<len(heads) else len(text)]) for n,h in enumerate(heads)]

def question_text(text):
    return squash(text.split('_')[0])

def source_split(block, first_answer):
    assert first_answer in block, (first_answer, block)
    cue, rest = block.split(first_answer, 1)
    return squash(cue), first_answer + rest


def named_pools(card, pools):
    # Explicit question asks one answer from each named dimension.
    card['rubric']['groups']=[{'id':gid,'label':label,'answerCount':1,'rows':[
        {'id':f'option-{n}','text':answer,'marks':2,'steps':[0,1,2]} for n,answer in enumerate(answers,1)]}
        for gid,label,answers in pools]
    card['rubric']['count']=len(pools)
    return card

def reading(docs,P):
    S,Q,cards=docs['scheme'],docs['paper'],[]
    for unit,sp,pages,askpages,counts,pools in [
        ('IR1',4,[2,3,4],[3,4],[3,1,1,1,1,2,1,1,1],[6,2,2,2,1,3,2,5,1]),
        ('IR2',5,[6,7],[7],[3,1,1,1,1,3,1,1],[5,4,1,1,1,9,3,1])]:
        source=draw_text(S,sp).split('Language awareness')[0]
        blocks=roman_blocks(source)
        asks=[]
        for p in askpages:asks.extend((r,question_text(q),p) for r,q in roman_blocks(page_text(Q,p,(300,30,580,793))))
        assert len(blocks)==len(asks)==len(counts),(unit,blocks,asks)
        general='Allocate 2 marks '+squash(between(source,'Allocate 2 marks','ANSWER IN ENGLISH'))
        for (roman,block),(qr,question,qp),count,pool in zip(blocks,asks,counts,pools):
            assert roman==qr
            firsts={'IR1':['cycling','Famous Russian','Russia +','Three +','4th November','14th November','Presents','Phone +','Free/'],'IR2':['Food  +','Cleaning/','5 people','4 \n','2 rooms','(dining) table','(individual) parking','10500']}
            cue,rest=source_split(block,firsts[unit][[r for r,_ in blocks].index(roman)])
            assert score(bag(question.split(' a. ')[0]),bag(cue))>.65,(question,cue)
            answers=[squash(a) for a in re.split(r'\s+\+\s*',rest) if squash(a)]
            assert len(answers)==pool,(unit,roman,answers)
            c=as_points(base(unit,question,count*2,pages,[sp],roman=roman),answers,count,steps=[0,1,2])
            c['review']['questionPages']=[qp];c['review']['guidancePages']=[3]
            c['rubric']['taskRequirements']=[general,'Do not penalise answers supplied in Russian.']
            c['rubric']['markingGuideNote']='Answer in English or Irish. The scheme explicitly accepts Russian answers.'
            if unit=='IR1' and roman=='vi':named_pools(c,[('when','When',[answers[0]]),('where','Where',answers[1:])])
            cards.append(c)
    source=draw_text(S,8);blocks=numbered_blocks(source)
    counts=[1,3,2,2,2,1,1,2,2,4];pools=[1,3,4,4,4,1,1,4,4,7]
    assert len(blocks)==10
    general='Allocate 2 marks '+squash(between(source,'Allocate 2 marks','1.i.'))
    for (item,roman,block),count,pool in zip(blocks,counts,pools):
        m=re.search(r'\(\d+ marks\)',block);assert m,block
        cue=squash(block[:m.start()]);rest=block[m.end():]
        b=next(b for b in P.blocks if b.unit=='CD' and b.item==item and b.side=='R' and b.text.startswith(roman+'.'))
        question=re.sub(r'^i+\.\s*','',b.text)
        assert score(bag(question.split(' a. ')[0]),bag(cue))>.65,(question,cue)
        answers=[squash(a) for a in rest.split('+') if squash(a)]
        assert len(answers)==pool,(item,roman,answers)
        c=as_points(base('CD',question,count*2,[14,15,16],[8],item,roman),answers,count,steps=[0,1,2])
        c['review']['questionPages']=[b.page+1];c['review']['guidancePages']=[3]
        c['rubric']['taskRequirements']=[general,'Do not penalise answers supplied in Russian.']
        c['rubric']['markingGuideNote']='Answer in English or Irish. The scheme explicitly accepts Russian answers.'
        if (item,roman)==(2,'i'):named_pools(c,[('where','Where',[answers[0]]),('discussion','What Lena discusses',answers[1:])])
        cards.append(c)
    assert len(cards)==27 and sum(c['totalMarks'] for c in cards)==88
    return cards

def language_and_matching(docs):
    S,Q,cards=docs['scheme'],docs['paper'],[]
    phrases=['Тематика конкурса','Возрастные группы','Справки']
    question='Write out '+squash(between(page_text(Q,5,(300,30,580,150)),'Write out','script.'))+' script.'+'\n\n'+'\n'.join(phrases)
    c=base('LA1',question,6,[5],[4]);c['kind']='question'
    c['rows']=[{'id':'handwriting','kind':'criterion','verbatim':'Deduct ½ mark for each letter incorrectly formed. Do not penalise for repeat errors.',
        'marks':6,'permittedMarks':[n/2 for n in range(13)],
        'contextNote':'Handwriting exercise: Write out the following headings in handwritten/cursive script. (6 marks) The source provides no handwritten exemplar. Apply the printed half-mark deductions across the complete exercise; no per-phrase allocation is inferred.'}]
    c['rows'] += [{'id':f'phrase-{n}','kind':'point','verbatim':p,'marks':None} for n,p in enumerate(phrases,1)]
    cards.append(c)
    raw=page_text(Q,8,(300,30,580,180));question='The following '+squash(between(raw,'The following','plural:'))+' plural:'
    table=S[4].find_tables().tables[0].extract()[1:];assert len(table)==6
    c=base('LA2',question,6,[8],[5]);c['kind']='question'
    partial=squash(between(draw_text(S,5),'Assign half the available marks'))
    partial='Assign half the available marks '+partial
    c['rows']=[{'id':f'phrase-{n}','kind':'criterion','verbatim':squash(a)+' — '+squash(b),'marks':1,
               'permittedMarks':[0,.5,1] if 'singular' in b else [0,1], 'contextNote':partial} for n,(a,b) in enumerate(table,1)]
    c['rows'][4]['contextNote']+=' Source discrepancy: the scheme prints “feminine singular / мужской род” for индивидуальная парковка. The English and Russian labels disagree; the published wording is retained here.'
    cards.append(c)
    for roman,page,box,total,table_index in [('i',9,(300,45,580,150),12,0),('ii',10,(300,30,580,150),16,1),('iii',10,(300,405,580,475),12,None)]:
        question=question_text(page_text(Q,page,box));question=re.sub(r'^i+\.\s*','',question)
        question=question.split('marks)')[0]+'marks)'
        assert question.startswith(('Match','Read')),question
        c=base('MM',question,total,[page],[6],roman=roman);c['kind']='question'
        if table_index is not None:
            table=S[5].find_tables().tables[table_index].extract()[1:]
            c['rows']=[{'id':f'match-{n}','kind':'point','verbatim':squash(a)+' — '+squash(b),'marks':4} for n,(a,b) in enumerate(table,1)]
        else:
            c['rows']=[{'id':f'match-{n}','kind':'point','verbatim':answer,'marks':4,'contextNote':'Assign full marks if candidates name the correct floor.'} for n,answer in enumerate(['B — на 2 этаж','A — на 3 этаж','B — на 6 этаж'],1)]
        if roman=='ii':c['rows'][2]['contextNote']='Source wording differs: the booklet’s heading c is “Сюрпризы погоды”; the scheme calls c “Погода ненормальная”. Both refer to text 2. The scheme also shortens heading a; its answer remains text 4.'
        cards.append(c)
    question=squash('Read through'+between(page_text(Q,11,(300,30,580,180)),'Read through','form.'))+' form.'
    question+='\n\n'+'Focail'+between(page_text(Q,11),'Focail')+'\n\n'+page_text(Q,12)
    answers=['когда','что','Какой','О чем','Как','Куда','Сколько','что','какой','когда']
    c=as_points(base('SD',question,20,[11,12],[7]),answers,10)
    c['rubric']['taskRequirements']=['Read through the following brief dialogues and insert words in the spaces provided. Select your answers from the lists supplied below. All the words are provided in the appropriate form. (10 x 2)']
    c['rubric']['markingGuideNote']='Complete both Group A and Group B. Each of the ten gaps is worth 2 marks.'
    cards.append(c)
    assert len(cards)==6 and sum(c['totalMarks'] for c in cards)==72
    return cards


def writing(docs):
    S,Q,cards=docs['scheme'],docs['paper'],[]
    raw=Q[16].get_text().replace('\u00a0',' ')
    instructions=squash('Write 3'+between(raw,'Write 3','1.'))
    table=Q[16].find_tables().tables[0].extract();assert len(table)==5
    question=instructions+'\n\n'+'\n'.join(squash(r[1])+' / '+squash(r[2]) for r in table)
    source=page_text(S,9);content=squash(between(source,'Content of each answer','Textual coherence')).removeprefix('12 ').strip()
    coherence=between(source,'Textual coherence')
    bands=[{'label':n,'marks':[int(n)],'guidance':[squash(t)]} for n,t in re.findall(r'^\s*([0-3])\s+(.+?)(?=^\s*[0-3]\s|\Z)',coherence,re.M|re.S) if not squash(t).startswith('Allocate')]
    assert len(bands)==4
    c=base('SA',question,30,[17],[9]);c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
    c['rubric']={'system':'language-writing','taskRequirements':['Write 3-5 sentences on TWO of the following topics in Russian or English. Each answer should contain three factual details. Marks are awarded for relevant content and textual coherence.','The quality of the English/Russian will only be an assessment factor insofar as it impedes communication.'],'criteria':[criterion(f'{choice}-content',f'{label}: content',12,list(range(0,13,2)),[content]) if part=='content' else criterion(f'{choice}-coherence',f'{label}: textual coherence',3,[0,1,2,3],[],bands) for choice,label in [('first','First chosen topic'),('second','Second chosen topic')] for part in ['content','coherence']],'markingGuideNote':''}
    cards.append(c)
    table=Q[17].find_tables().tables[0].extract();assert len(table)==3
    question='Write 6 '+squash(between(page_text(Q,18,(300,30,580,110)),'Write 6','IN RUSSIAN.'))+' IN RUSSIAN.'+'\n\n'+'\n\n'.join('\n• '.join(squash(p) for p in re.split(r'[\uf0b7•]',cell)) for row in table for cell in row[1:])
    source=page_text(S,11);table=S[10].find_tables().tables[0].extract()
    full=[{'label':squash(r[0]),'marks':mark_range(squash(r[0])),'guidance':[squash(r[1])]} for r in table[1:]]
    coherence=between(source,'Allocate 6 marks for textual coherence:')
    bands=[{'label':n,'marks':mark_range(n),'guidance':[squash(t)]} for n,t in re.findall(r'^\s*(\d(?:-\d)?)\s+(.+?)(?=^\s*\d(?:-\d)?\s|\Z)',coherence,re.M|re.S)];assert len(bands)==5
    c=base('EW',question,30,[18],[10,11]);c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
    c['rubric']={'system':'language-writing','taskRequirements':['Write 6-10 sentences on one of the following topics IN RUSSIAN.','No marks are awarded for additional information/content.','Opening/greeting','age','how you spent your birthday','signing off'],'criteria':[criterion('content','Communication + content',12,list(range(0,13,2)),['2 points for content details up to maximum of 12']),criterion('expression','Language + expression',12,list(range(13)),[],full),criterion('coherence','Textual coherence',6,list(range(7)),[],bands)],'markingGuideNote':'The opening/greeting, age, birthday account and signing-off guidance applies to the letter choice.'}
    cards.append(c)
    return cards


def listening(docs):
    S,A,cards=docs['scheme'],docs['aural'],[]
    source='\n'.join(draw_text(S,p) for p in (12,13,14))
    source=re.sub(r'(SECTION [IV]+) *\n',r'\1\n',source)
    general=bullets(between(source,'General:','Award FIVE'))+['Award FIVE marks for each correct/relevant point.'];assert len(general)==6
    sections=[between(source,'SECTION I\n','SECTION II\n'),between(source,'SECTION II\n','SECTION III\n'),between(source,'SECTION III\n','SECTION IV\n'),between(source,'SECTION IV\n')]
    counts=[[1]*5,[1]*5,[1]*5,[1,1,2,1]]
    pools=[[1,3,6,7,1],[5,6,10,7,5],[4,3,5,5,3],[4,12,11,1]]
    topics=[['russian-0-5','russian-0-8','russian-0-8','russian-0-14','russian-0-5'],['russian-0-7','russian-2-5','russian-2-5','russian-2-5','russian-0-5'],['russian-0-2','russian-0-4','russian-0-5','russian-0-4','russian-0-1'],['russian-0-3','russian-0-4','russian-0-1','russian-0-6']]
    audio=next(r['source'] for r in json.loads((ROOT/'data/russianAudio.json').read_text()) if r['year']==2015)
    for section,text in enumerate(sections,1):
        blocks=numbered_blocks(text);asks=numbered_blocks(page_text(A,section+1,(300,30,580,793)))
        assert len(blocks)==len(asks)==len(counts[section-1]),(section,blocks,asks)
        for n,((item,roman,block),(qi,qr,q),count,pool) in enumerate(zip(blocks,asks,counts[section-1],pools[section-1])):
            assert (item,roman)==(qi,qr)
            question=question_text(q)
            firsts=[['c. in a theatre','Air France','Pskov','Her mother is ill','a. on television'],['from 13th March','Stand-up','40 films','Comics','Mini-quest'],['Georgia','To take up post','Has been boxing','Senior trainer','Brother'],['She was 7','Applied to','Lived in','(decided)']]
            cue,rest=source_split(block,firsts[section-1][n])
            assert score(bag(question.split(' a. ')[0]),bag(cue))>.65,(question,cue)
            answers=[squash(a).rstrip(' .') for a in rest.split('+') if squash(a).strip('.')]
            assert len(answers)==pool,(section,item,roman,answers)
            c=as_points(base(f'L{section}',question,count*5,[section+1],[12 if section==1 else 13 if section<4 else 14],item,roman),answers,count)
            for g in c['rubric']['groups']:g['rows'][0]['marks']=5
            c['rubric']['taskRequirements']=general
            c['topicId']=topics[section-1][n];c['additionalTopicIds']=['russian-1-0']
            c['sourceMaterial']['kind']='source-question';c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
            c['audioMaterial']=audio;c['review']['guidancePages']=[12];cards.append(c)
    assert len(cards)==19 and sum(c['totalMarks'] for c in cards)==100
    return cards


def build():
    docs=opened_sources();cards=reading(docs,RuPaper(2015,'ol'))+language_and_matching(docs)+writing(docs)+listening(docs)
    assert len(cards)==54 and sum(c['totalMarks'] for c in cards)==320
    old={c['id'] for c in json.loads((ROOT/'scripts/markbank/authored/russian.json').read_text())};assert not any(c['id'] in old for c in cards)
    return cards

if __name__=='__main__':save_reviewed(build())
