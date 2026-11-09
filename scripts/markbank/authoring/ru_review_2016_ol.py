"""Russian 2016 Ordinary original-source authoring, with exact answer/footer bounds."""
import hashlib,json,re,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[3]
# When moved into scripts/markbank/authoring, ROOT is the worktree.
sys.path.insert(0,str(ROOT/'scripts/markbank/authoring'))
from ru_review_2011_ol import roman_blocks as original_roman_blocks,numbered_blocks
from ru_review_2015_ol import question_text,source_split
from ru_review_2026_hl import squash,between
from ru_paper import bag,score
METADATA={'paper':{'pages':20,'sha256':'c664fa1ab4abdf8fc3eaec74dbde93201a196141aba9deb2b04744d3d048c7f8'},'aural':{'pages':8,'sha256':'b40b68b3174a9a4191343d4b01a7dc257730fc3df790c5f48a00b65e6dfe7ee4'},'scheme':{'pages':16,'sha256':'4242b1be879b2ff9973f75aabf3135478afe1e59b098d2c694ff581d1ce84616'}}

def roman_blocks(text):
    return original_roman_blocks(re.sub(r'(?m)^(\s*(?:ix|viii|vii|vi|iv|v|i{1,3}))\s+\.',r'\1.',text))

def source_records():
    docs={}
    for kind,relative in [('paper','papers/2016-ol-000-paper.pdf'),('aural','papers/2016-ol-A00-paper.pdf'),('scheme','schemes/2016-ol.pdf')]:
        p=ROOT/'examiner-reports/russian'/relative
        assert hashlib.sha256(p.read_bytes()).hexdigest()==METADATA[kind]['sha256']
        docs[kind]=fitz.open(p)
    Q,A,S=docs['paper'],docs['aural'],docs['scheme']
    def page(doc,n,right=False):
        # Answer4 on scheme p3 extends to y785.90; footer1 starts y795.09.
        return doc[n-1].get_text(clip=fitz.Rect(295 if right else 20,30,580,793),sort=False).replace('\x02','•').replace('\uf0b7','•').replace('\xa0',' ')
    cards=[]
    def record(unit,item,roman,q,qp,body,sp,total,**extra):
        component='aural' if unit.startswith('L') and unit in ('L1','L2','L3','L4') else 'paper'
        norm=lambda t:re.sub(r'[^\w]','',t.casefold())
        assert norm(q) in norm(' '.join(page(docs[component],p,True) for p in qp)),(unit,item,roman,q)
        c=dict(id='ru-2016-ol-'+unit.lower()+(f'-{item}' if item is not None else '')+(f'-{roman}' if roman else ''),unit=unit,item=item,roman=roman,question=q,questionPages=qp,component=component,publishedSourceBlock=squash(body),schemePages=sp,publishedTotal=total,**extra)
        cards.append(c);return c
    ir1='\n'.join(page(S,p) for p in (3,4)).split('Text 2 (30 marks)')[0]
    assert ir1.split('How many days a week do students attend classes?')[1].lstrip().startswith('4')
    ir2=between(page(S,4),'ANSWER IN ENGLISH unless indicated otherwise.')
    for unit,source,askpages,sp,counts,starts in [
        ('IR1',ir1,(3,4),[3,4],[None,1,2,2,1,1,1,1,1],[None,'Monday','Minimum: 3','Minimum: 5','4','138 euro','20 euro','228 euro','45 euro']),
        ('IR2',ir2,(6,7),[4],[3,1,1,2,2,2,2],['Basketball','2000','3','Step aerobics','Big pool:','8am','Evening swim'])]:
        blocks=roman_blocks(source);asks=[]
        for p in askpages:
            asks.extend((r,question_text(q),p) for r,q in roman_blocks(page(Q,p,True).split('Language awareness')[0]))
        assert len(blocks)==len(asks)==len(counts),(unit,blocks,asks)
        for (roman,b),(qr,q,qp),count,start in zip(blocks,asks,counts,starts):
            assert roman==qr
            if unit=='IR2':q=q[:re.search(r'\(Section \d\)',q).end()]
            if count is None:continue
            cue,body=source_split(b,start);assert score(bag(re.sub(r'\(Section \d+\)','',q)),bag(cue))>.70,(unit,roman,q,cue)
            record(unit,None,roman,q,[qp],body,sp,count*2)
    source='\n'.join(page(S,p) for p in (8,9)).split('SECTION II')[0];source=between(source,'D.')
    blocks=numbered_blocks(source);asks=[(i,r,question_text(q),p) for p in (12,13) for i,r,q in numbered_blocks(page(Q,p,True))]
    counts=[1,2,2,2,2,1,2,2,1,2,1,1,1]
    assert len(blocks)==len(asks)==len(counts)==13
    for (i,r,b),(qi,qr,q,p),count in zip(blocks,asks,counts):
        assert(i,r)==(qi,qr);m=re.search(r'\(\d+\s*marks\)',b);assert m,b
        cue,body=b[:m.start()],b[m.end():];assert score(bag(re.sub(r'\(Section \d+\)','',q)),bag(cue))>.70,(q,cue)
        record('CD',i,r,q,[p],body,[8,9],count*2)
    assert len(cards)==28 and sum(c['publishedTotal'] for c in cards)==86
    q='The advertisement '+squash(between(page(Q,3,True),'The advertisement','provided.'))+' provided.'
    table=S[2].find_tables().tables[0].extract()[1:];assert len(table)==3
    record('LA1',None,None,q,[3],'Assign a maximum of 10 marks. '+between(page(S,3),'Assign a maximum of 10 marks.','Answer the remaining questions'),[3],10,answerRows=table,originalQuestionLabels=[r[0] for r in table],scoring=dict(perPhrase=3,joining=1,incorrectLetterDeduction=.5))
    q='Indicate whether '+question_text(between(page(Q,7,True),'Indicate whether')).split('plural (множественное число).')[0]+'plural (множественное число).'
    record('LA2',None,None,q,[7],page(S,5),[5],4,scoring=dict(perAnswer=1,correctAnswers=4))
    q='Match the following '+squash(between(page(Q,8,True),'Match the following','r / Subject headings'))
    tables=S[5].find_tables().tables;assert len(tables)==2 and len(tables[1].extract())==20
    record('MM',None,None,q,[8],page(S,6),[6],40,answerRows=tables[1].extract(),headingRows=tables[0].extract(),scoring=dict(perAnswer=2,correctAnswers=20))
    q='Give the missing '+question_text(between(page(Q,9,True),'Give the missing','appropriate form.'))+' appropriate form.'
    record('SD',None,None,q,[9],page(S,7)+'\n'+page(S,8).split('D.')[0],[7,8],20,sourcePages=[9,10],sourceNote='All three interviews required. Only whole-exercise20 printed; ten gaps do not establish a per-gap tariff. Question4 in first interview is already filled, not a gap.')
    q='Write 3 '+squash(between(page(Q,14,True),'Write 3','textual coherence.'))+' textual coherence.'
    table=Q[13].find_tables().tables[0].extract();assert len(table)==5
    record('SA',None,None,q,[14],between(page(S,9),'A. Short answers: cultural awareness'),[9],30,choiceRows=table,scoring=dict(chosenTopics=2,contentPerTopic=12,coherencePerTopic=3))
    q='Write 6 '+squash(between(page(Q,15,True),'Write 6','IN RUSSIAN.'))+' IN RUSSIAN.'
    table=Q[14].find_tables().tables[0].extract();assert len(table)==3
    record('EW',None,None,q,[15],page(S,10)+'\n'+page(S,11),[10,11],30,choiceRows=table,scoring=dict(content=12,expression=12,coherence=6))
    assert len(cards)==34 and sum(c['publishedTotal'] for c in cards)==220
    source='\n'.join(page(S,p) for p in (12,13,14));heads=list(re.finditer(r'^\s*Section (1|II|III|IV)\s*$',source,re.M));assert len(heads)==4
    counts=[[1,1,1,1,1,1,1,1,1,2,2],[1,2,4,2,1,1,1],[1,1,1,1,1,2,1,3,2],[1]*12]
    starts=[['Moscow','(End of)','All Russian','Songwriter/','Russia +','Send an email','3','Aviva','Hundred','16th','Live music'],['Russian school','Boys & girls','Football','10am','75 euro','Food/lunch','Phone number'],['Diana','19','At (the age','(elder)','Music/','In winter','Moscow','Hip hop','Immigrate'],['19th','football','To be','music','(after leaving','16','2005','Became','2007','Eurovision','Too busy','He managed']]
    for n,h in enumerate(heads):
        section=n+1;b=source[h.end():heads[n+1].start() if n+1<len(heads) else len(source)];blocks=numbered_blocks(b)
        asks=[(i,r,question_text(q),p) for p in ([2,3] if section==1 else [4] if section==2 else [5] if section==3 else [6,7]) for i,r,q in numbered_blocks(page(A,p,True))]
        assert len(blocks)==len(asks)==len(counts[n]),(section,blocks,asks)
        for (i,r,b),(qi,qr,q,qp),count,start in zip(blocks,asks,counts[n],starts[n]):
            assert (i,r)==(qi,qr);cue,body=source_split(b,start)
            assert score(bag(q),bag(cue))>.75,(q,cue)
            record(f'L{section}',i,r,q,[qp],body,[12 if section==1 else 13 if section<4 else 14],count*2)
    assert len(cards)==73 and sum(c['publishedTotal'] for c in cards)==320
    return docs,dict(sources=METADATA,status='Source selectors only; 34 written and 39 listening tasks, 220+100=320 marks',tasks=cards)

from ru_review_2015_ol import base as old_base, page_text
from ru_review_2026_hl import as_points,save_reviewed,mark_range
from ru_review_2018_ol import criterion

def source_card(r):
    pages=r.get('sourcePages') or ([2,3,4] if r['unit'] in ('IR1','LA1') else [5,6,7] if r['unit']=='IR2' else [11,12,13] if r['unit']=='CD' else r['questionPages'])
    c=old_base(r['unit'],r['question'],r['publishedTotal'],pages,r['schemePages'],r['item'],r['roman'])
    for key in ('id','questionRef'):c[key]=c[key].replace('2015','2016')
    c['year']=2016;c['sourceMaterial']['title']=c['sourceMaterial']['title'].replace('2015','2016');c['review']['questionPages']=r['questionPages']
    return c

def pool(body):return [squash(x) for x in body.split('+') if squash(x)]

def written_guidance(c,general):
    c['review']['guidancePages']=[3]
    note='Answer in English or Irish. Marking scheme page 3: Do not penalise answers supplied in Russian.'
    if c['kind']=='rubric':
        c['rubric']['taskRequirements']=[general,'Do not penalise answers supplied in Russian.']+c['rubric']['taskRequirements']
        c['rubric']['markingGuideNote']=(c['rubric']['markingGuideNote']+' '+note).strip()
    else:
        for variant in c.get('answerVariants',[]):variant['rows'][0]['contextNote']=general+' '+note
        c['rows'][0]['contextNote']=general+' '+note
    return c

def reading(docs,source):
    result=[];general='Allocate 2 marks '+squash(between(page_text(docs['scheme'],3),'Allocate 2 marks','ANSWER IN ENGLISH'))
    for r in source['tasks']:
        unit=r['unit'];key=(r['item'],r['roman']);body=r['publishedSourceBlock']
        if unit not in ('IR1','IR2','CD'):continue
        if unit=='IR2' and r['roman']=='v':
            c=source_card(r);c['kind']='question';variants=[]
            for ident,label,start,end in [('big','Big pool','Big pool:','kids’ pool:'),('kids','kids’ pool','kids’ pool:',None)]:
                answers=pool(between(body,start,end));assert len(answers)==2
                rows=[{'id':f'dimension-{n}','kind':'criterion','verbatim':answer,'marks':2,'permittedMarks':[0,1,2]} for n,answer in enumerate(answers,1)]
                variants.append({'id':ident,'label':label,'rows':rows})
            c['answerVariants']=variants;c['rows']=variants[0]['rows']
            written_guidance(c,general)
            for variant in variants:variant['rows'][0]['contextNote']+=' Choose one pool and give both of its dimensions. Changing the pool resets the selected dimensions; do not combine dimensions from different pools.'
        else:
            partial=[]
            if 'Assign one mark' in body:body,partial=body.split('Assign one mark',1);partial=pool(partial.removeprefix(' for:').removeprefix(':'))
            mapping={}
            if unit=='IR2' and r['roman']=='iv':mapping={3:partial};assert partial==['dance']
            if unit=='CD' and key==(2,'i'):mapping={1:partial};assert partial==['4th class/form']
            if unit=='CD' and key==(1,'i'):
                answers=pool(between(body,'assign one mark for each of:'))
                c=as_points(source_card(r),answers,2)
                for g in c['rubric']['groups']:g['rows'][0]['marks']=1
                c['rubric']['taskRequirements']=[body]
            elif unit=='IR2' and r['roman']=='vii':
                # Original printed cost table has four choices; each whole
                # named cost stays intact rather than splitting number/unit.
                answers=[squash(x) for x in ['Evening swim 265 (roubles)','Swimming lesson 550 (roubles)','Training session during the day time 125 (roubles)','Rental of the main sports hall (whole space) 2190 (roubles an hour)']]
                c=as_points(source_card(r),answers,2,steps=[0,1,2])
                c['questionText']+='\n\n'+'\n'.join(squash(row[1]) for row in docs['paper'][6].find_tables().tables[0].extract())
            else:c=as_points(source_card(r),pool(body),r['publishedTotal']//2,mapping,steps=[0,1,2])
            written_guidance(c,general)
            if unit=='CD' and key==(2,'i'):
                c['rubric']['markingGuideNote']+=' The two-sisters detail may be claimed only if it was not already rewarded in Q1(i). Assess that source condition before placing this detail.'
        result.append(c)
    assert len(result)==28 and sum(c['totalMarks'] for c in result)==86
    return result

def writing_card(c,criteria,requirements=None,note=''):
    c.pop('rows');c.pop('tariffModel');c['kind']='rubric';c['rubric']={'system':'language-writing','criteria':criteria,'taskRequirements':requirements or [],'markingGuideNote':note};return c

def language_and_matching(docs,source):
    result=[];S=docs['scheme']
    for r in source['tasks']:
        unit=r['unit']
        if unit not in ('LA1','LA2','MM','SD'):continue
        c=source_card(r)
        if unit=='LA1':
            rule=between(r['publishedSourceBlock'],'Assign a maximum of 10 marks.','Cursive script')
            rule='Assign a maximum of 10 marks. '+squash(rule)
            joining=squash(re.search(r'Where candidates.*?joining letters together\.',rule).group())
            criteria=[criterion(f'phrase-{n}',squash(label),3,[n/2 for n in range(7)],[squash(answer)]) for n,(label,answer) in enumerate(r['answerRows'],1)]
            criteria.append(criterion('joining','Joining letters together',1,[0,1],[joining]))
            criteria[-1]['limits']=[{'id':'missing-initial-loop','maxMarks':0,'when':{'any':[{'flag':'missing-initial-loop','prompt':joining}]},'guidance':[joining]}]
            c=writing_card(c,criteria,[rule],'The published exemplars are typeset, not handwriting samples. Assess the written letter forms in half-mark steps for each of the three phrases; do not deduct again for repeated errors. The one joining mark is global, not one per phrase.')
            c['questionText']+='\n\n'+'\n'.join(r['originalQuestionLabels'])
        elif unit=='LA2':
            answers=['спортивный комплекс — singular (единственное число)','рабочие дни — plural (множественное число)','индивидуальные занятия — plural (множественное число)','спортивное сооружение — singular (единственное число)']
            c=as_points(c,answers,4)
            for g in c['rubric']['groups']:g['rows'][0]['marks']=1
            c['rubric']['taskRequirements']=['Language awareness (4 marks: assign 1 mark for each correct answer)']
        elif unit=='MM':
            c=as_points(c,[squash(answer)+' — '+squash(number) for number,answer in r['answerRows']],20)
            c['rubric']['taskRequirements']=['B. Mix and Match (40 marks: assign 2 marks for each correct answer)']
        else:
            c['kind']='question';c['tariffModel']={'kind':'questionTotal'}
            answers=['Kак','сколько','скольки/ скольких','где','Kак','Кто','Kакие','Kогда','Чья','Сколько']
            c['rows']=[{'id':f'gap-{n}','kind':'point','verbatim':answer,'marks':None} for n,answer in enumerate(answers,1)]
            c['rows'][0]['contextNote']='Complete all three interviews. The scheme publishes 20 marks for the whole exercise and no per-gap allocations. All ten missing-word answers are retained here; numeric self-scoring is unavailable. Question 4 in the first interview is already complete in the original paper and is not an additional gap.'
        result.append(c)
    assert len(result)==4 and sum(c['totalMarks'] for c in result)==74
    return result

def writing(docs,source):
    result=[];S,Q=docs['scheme'],docs['paper']
    for r in source['tasks']:
        if r['unit'] not in ('SA','EW'):continue
        c=source_card(r);c['questionText']+='\n\n'+'\n\n'.join('\n• '.join(squash(x) for x in re.split(r'[\uf0b7•]',cell)) for row in r['choiceRows'] for cell in row[1:])
        if r['unit']=='SA':
            text=page_text(S,9);content=squash(between(text,'Content of each answer','Textual coherence')).removeprefix('12 ').strip()
            coherence=between(text,'Textual coherence')
            bands=[{'label':n,'marks':[int(n)],'guidance':[squash(t)]} for n,t in re.findall(r'^\s*([0-3])\s+(.+?)(?=^\s*[0-3]\s|\Z)',coherence,re.M|re.S) if not squash(t).startswith('Allocate')];assert len(bands)==4
            criteria=[criterion(f'{choice}-content',f'{label}: content',12,list(range(0,13,2)),[content]) if part=='content' else criterion(f'{choice}-coherence',f'{label}: textual coherence',3,[0,1,2,3],[],bands) for choice,label in [('first','First chosen topic'),('second','Second chosen topic')] for part in ['content','coherence']]
            c=writing_card(c,criteria,['Write 3-5 sentences on TWO of the following topics in Russian or English. Each answer should contain three factual details. Marks are awarded for relevant content and textual coherence.','The quality of the English/Russian will only be an assessment factor insofar as it impedes communication.'],'Choose two topics. Each has three content details at four marks full or two marks partial, plus three marks for coherence; there is no published model essay.')
        else:
            text=page_text(S,11);table=S[10].find_tables().tables[0].extract()
            bands=[{'label':squash(price),'marks':mark_range(squash(price)),'guidance':[squash(description)]} for price,description in table[1:]];assert len(bands)==6
            coherent=between(text,'Allocate 6 marks for textual coherence:')
            coherence=[{'label':n,'marks':mark_range(n),'guidance':[squash(t)]} for n,t in re.findall(r'^\s*(\d(?:-\d)?)\s+(.+?)(?=^\s*\d(?:-\d)?\s|\Z)',coherent,re.M|re.S)];assert len(coherence)==5
            c=writing_card(c,[criterion('content','Communication + content',12,list(range(0,13,2)),['2 points for content details up to maximum of 12']),criterion('expression','Language + expression',12,list(range(13)),[],bands),criterion('coherence','Textual coherence',6,list(range(7)),[],coherence)],[squash(text[:text.index('2 points for content')]),'Write 6-10 sentences on one of the following topics IN RUSSIAN.'],'Use the original required information/functions for the chosen prompt. No marks for additional content and no model answer or later-year expression cap is invented.')
        result.append(c)
    return result

def listening(docs,source):
    result=[];S=docs['scheme'];general=between(page_text(S,12),'General:','Section 1')
    requirements=[squash(x) for x in re.split(r'[\x02\uf0b7•]',general) if squash(x)]
    audio=next(row['source'] for row in json.loads((ROOT/'data/russianAudio.json').read_text()) if row['year']==2016)
    topics={1:['russian-0-2','russian-0-7','russian-2-3','russian-0-4','russian-0-8','russian-0-9','russian-2-3','russian-0-2','russian-2-3','russian-0-7','russian-0-5'],2:['russian-0-3','russian-0-3','russian-0-5','russian-0-3','russian-0-9','russian-0-9','russian-0-14'],3:['russian-0-7','russian-0-7','russian-0-5','russian-0-5','russian-0-5','russian-0-5','russian-0-8','russian-0-5','russian-0-6'],4:['russian-0-7','russian-0-5','russian-0-6','russian-0-4','russian-0-3','russian-0-4','russian-0-7','russian-0-4','russian-0-7','russian-2-8','russian-0-4','russian-0-4']}
    for r in source['tasks']:
        if r['unit'] not in ('L1','L2','L3','L4'):continue
        section=int(r['unit'][1]);key=(r['item'],r['roman']);body=r['publishedSourceBlock'];partial=[]
        m=re.search('(?:assign|Assign) one mark:',body)
        if m:body,partial=body[:m.start()],pool(body[m.end():])
        answers=pool(body);mapping={}
        if section==1 and key==(4,'i'):mapping={0:[partial[0]],1:[partial[1]]};assert partial==['October','castle']
        if section==4 and key==(4,'i'):mapping={1:[partial[0]],2:[partial[1]]};assert partial==['New Russian','worldwide']
        c=as_points(source_card(r),answers,r['publishedTotal']//2,mapping)
        c['rubric']['taskRequirements']=requirements
        c['review']['guidancePages']=[12]
        if section==1 and key==(4,'i'):
            c['rubric']['groups'][0]['label']='When';c['rubric']['groups'][1]['label']='Where'
        if section==4 and key==(4,'ii'):c['rubric']['markingGuideNote']='The actor detail may be claimed only if it was not already rewarded in Q1(iii) or Q3(i). Assess this condition before placing that answer.'
        index=sum(c0['section']==r['unit'] for c0 in result);c['topicId']=topics[section][index];c['additionalTopicIds']=['russian-1-0']
        c['sourceMaterial']['kind']='source-question';c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.';c['audioMaterial']=audio
        result.append(c)
    assert len(result)==39 and sum(c['totalMarks'] for c in result)==100
    return result

def build():
    docs,source=source_records()
    cards=reading(docs,source)+language_and_matching(docs,source)+writing(docs,source)+listening(docs,source)
    assert len(cards)==len({c['id'] for c in cards})==73 and sum(c['totalMarks'] for c in cards)==320
    for doc in docs.values():doc.close()
    return cards

if __name__=='__main__':save_reviewed(build())
