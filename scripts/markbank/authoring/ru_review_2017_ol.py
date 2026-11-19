"""Russian 2017 Ordinary: 51 asks from pinned originals.
The listening source conflict follows Alex’s explicit 18 November approval.
"""
from pathlib import Path
import hashlib,json,re,sys
import fitz
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts/markbank/authoring'))
from ru_review_2011_ol import roman_blocks,numbered_blocks
from ru_review_2015_ol import question_text,source_split
from ru_review_2026_hl import squash,between
from ru_paper import bag,score
METADATA={'paper': {'pages': 20, 'sha256': '2b705ed6fdff983ac7effe1b4d3737fdaca5a1cd893f19b8b58946f544d713f6'}, 'aural': {'pages': 8, 'sha256': '98fbb84beb3eb52c85dc18ccca198dfb964a2b7727444aa42634a041f3bcdd61'}, 'scheme': {'pages': 16, 'sha256': '27ccb0243cfcc6e793f3abfff15dab61fe0d7b2a575a624629770bf1d1fa447f'}}

def source_records():
    docs={}
    for kind,relative in [('paper','papers/2017-ol-000-paper.pdf'),('aural','papers/2017-ol-A00-paper.pdf'),('scheme','schemes/2017-ol.pdf')]:
        path=ROOT/'examiner-reports/russian'/relative
        assert hashlib.sha256(path.read_bytes()).hexdigest()==METADATA[kind]['sha256']
        docs[kind]=fitz.open(path);assert len(docs[kind])==METADATA[kind]['pages']
    Q,A,S=docs['paper'],docs['aural'],docs['scheme']
    def page(doc,n,right=False):
        # Keep every answer block. Remove only the exact printed page number
        # bound to its own footer geometry on the visually reviewed original.
        if doc is S:
            native=doc[n-1];blocks=[b for b in native.get_text('blocks') if b[6]==0]
            footer=[b for b in blocks if b[4].strip()==str(n-2) and b[1]>native.rect.height-65]
            assert len(footer)==1,(n,footer)
            text=''.join(b[4] for b in blocks if b is not footer[0])
        else:
            text=doc[n-1].get_text(clip=fitz.Rect(295 if right else 20,30,580,793),sort=False)
        return text.replace('\uf0b7','•').replace('\xa0',' ')
    norm=lambda text:re.sub(r'[^\w]','',text.casefold())
    records=[]
    def record(unit,item,roman,question,qp,body,sp,total,**extra):
        component='aural' if unit in ('L1','L2','L3','L4') else 'paper'
        assert any(norm(question) in norm(' '.join(page(docs[component],p,right) for p in qp)) for right in (False,True)),(unit,item,roman,question)
        assert norm(body) in norm(' '.join(page(S,p) for p in sp)),(unit,item,roman,body)
        c=dict(id='ru-2017-ol-'+unit.lower()+(f'-{item}' if item is not None else '')+(f'-{roman}' if roman else ''),unit=unit,item=item,roman=roman,question=question,questionPages=qp,component=component,publishedSourceBlock=squash(body),schemePages=sp,publishedTotal=total,**extra)
        records.append(c);return c
    for unit,sp,qps,counts,firsts in [
        ('IR1',4,[3,4],[1,2,1,1,1,2,2,2],['2013','(house = )','Three','stove','carpentry','post office','ecologically','fishing']),
        ('IR2',5,[6,7],[2,1,2,2,2,1,2],['schoolchildren','False','1. research','political','1. text','(1) October','name and contact'])]:
        body=re.split(r'Language [Aa]wareness',page(S,sp))[0]
        blocks=roman_blocks(body)
        asks=[]
        for p in qps:
            asks.extend((r,question_text(q),p) for r,q in roman_blocks(re.split(r'Language [Aa]wareness',page(Q,p,True))[0]))
        assert len(blocks)==len(asks)==len(counts),(unit,blocks,asks)
        for (r,b),(qr,q,qp),count,start in zip(blocks,asks,counts,firsts):
            assert r==qr
            cue,pool=source_split(b,start)
            options=[]
            if (unit,r)==('IR2','ii'):
                q=q.split('box below.',1)[0]+'box below.'
                assert squash(cue).startswith(q.split(' Tick the appropriate box below.')[0]),(q,cue)
                full=page(Q,qp)
                for option in ('True','False'):
                    assert re.search(r'(?<![A-Za-z])'+option+r'(?![A-Za-z])',full)
                options=['True','False']
            else:
                assert score(bag(q),bag(cue))>.7,(unit,r,q,cue)
            price=re.search(r'\((\d+)\)',cue);assert price and int(price.group(1))==count*2,(unit,r,cue)
            record(unit,None,r,q,[qp],pool,[sp],count*2,printedTariff=price.group(),printedDetailQuota=count,questionOptions=options)
    blocks=numbered_blocks(page(S,8))
    asks=[(i,r,question_text(q),p) for p in [12,13] for i,r,q in numbered_blocks(page(Q,p,True))]
    counts=[2,1,2,5,1,2,1,1,1,1,1,2]
    starts=['often met','4 months','They had argued','Bimka','standing','looking/searching','Is it black?','to her home','Andrei','he was feeling','that it wasn’t','didn’t want']
    assert len(blocks)==len(asks)==len(counts)==12,(blocks,asks)
    for (i,r,b),(qi,qr,q,p),count,start in zip(blocks,asks,counts,starts):
        assert (i,r)==(qi,qr)
        cue,pool=source_split(b,start);assert score(bag(q),bag(cue))>.7,(q,cue)
        record('CD',i,r,q,[p],pool,[8],count*2,printedDetailQuota=count)
    assert len(records)==27 and sum(r['publishedTotal'] for r in records)==88
    q='Write out '+question_text(between(page(Q,4,True),'Write out','script.'))+' script.'
    record('LA1',None,None,q,[4],between(page(S,4),'Language Awareness'),[4],6,sourceNote='Global six, half-mark per malformed letter, no repeat penalty and round up. No separate phrase allocations.')
    q='The following adjective '+question_text(between(page(Q,7,True),'The following adjective','множественное число:'))+' множественное число:'
    # Exact end cue and original table binding are checked after native inspection.
    record('LA2',None,None,q,[7],between(page(S,5),'Language awareness'),[5],6,sourceNote='Six explicit one-mark answers.')
    q='Match the following names '+question_text(between(page(Q,8,True),'Match the following names','the list of goods.'))+' the list of goods.'
    record('MM',1,None,q,[8],page(S,6),[6],40,sourceNote='Ten explicit four-mark answers; preserve printed Q1.')
    q='Read through '+question_text(between(page(Q,9,True),'Read through','appropriate form.'))+' appropriate form.'
    record('SD',None,None,q,[9],page(S,7),[7],20,sourcePages=[9,10],sourceNote='Both dialogues; ten explicit two-mark answers; unnumbered printed task.')
    q='Write 3'+question_text(between(page(Q,14,True),'Write 3','essay titles.'))+' essay titles.'
    record('SA',None,None,q,[14],page(S,9),[9],30,fullQuestionPage=page(Q,14),sourceNote='Two of five complete choices; three facts each at4/full or2/partial and coherence3.')
    q='Write 6'+question_text(between(page(Q,15,True),'Write 6','IN RUSSIAN.'))+' IN RUSSIAN.'
    record('EW',None,None,q,[15],page(S,10)+'\n'+page(S,11),[10,11],30,sourcePageBlocks=[squash(page(S,10)),squash(page(S,11))],fullQuestionPage=page(Q,15),sourceNote='All three choices; manual aggregate content2/detail to12, expression12, coherence6.')
    assert len(records)==33 and sum(r['publishedTotal'] for r in records)==220
    listening=page(S,12)+'\n'+page(S,13)
    heads=list(re.finditer(r'^\s*Section (1|II|III|IV)\s*$',listening,re.M));assert len(heads)==4
    firsts=[['Irish dance','16th of May','13th of February','Ciara','Boxer'],['America/USA','Spain','Sports','Learn/ improve'],['Swimming','At the age','Drawing','Austria'],['October','At (the age','(Received)','Russian (equivalent','Left the Russian']]
    for n,h in enumerate(heads):
        section=n+1;body=listening[h.end():heads[n+1].start() if n+1<len(heads) else len(listening)]
        blocks=numbered_blocks(body);asks=[(i,r,question_text(q)) for i,r,q in numbered_blocks(page(A,section+1,True))]
        assert len(blocks)==len(asks)==len(firsts[n]),(section,blocks,asks)
        for (i,r,b),(qi,qr,q),start in zip(blocks,asks,firsts[n]):
            assert (i,r)==(qi,qr),(section,i,r,qi,qr)
            cue,pool=source_split(b,start);assert score(bag(q),bag(cue))>.7,(q,cue)
            record(f'L{section}',i,r,q,[section+1],pool,[12,13] if section==2 else [12 if section==1 else 13],None,sharedAward=f'L{section}-section25',sourceNote='Literal two-mark guidance conflicts with section totals and explicit three-mark clauses. The separate approval record authorises five per requested detail; publishedTotal stays unset because five is inferred.')
    assert len(records)==51 and len({r['id'] for r in records})==51
    return docs,dict(status='Original hashes and native bindings checked; approved listening inference retained separately from printed source values',sources=METADATA,independentTasks=51,writtenTasks=33,listeningTasks=18,printedWrittenTotal=220,printedListeningTotal=100,generalWrittenGuidance=squash(page(S,3)),ir1Guidance=squash('Allocate 2 marks '+between(page(S,4),'Allocate 2 marks','i.')),ir2Guidance=squash('Allocate 2 marks '+between(page(S,5),'Allocate 2 marks','i.')),comprehensionGuidance=squash(page(S,8).split('1.i.')[0]),listeningGuidance=squash(listening[:heads[0].start()]),tasks=records)


"""Unpublished builder components; import only after original selectors pass."""
from ru_review_2015_ol import base as previous_base
from ru_review_2026_hl import as_points
from ru_review_2018_ol import criterion

def source_card(r):
    pages={'IR1':[2,3,4],'LA1':[2,3,4],'IR2':[5,6,7],'LA2':[5,6,7],'CD':[11,12,13],'SD':[9,10]}.get(r['unit'],r['questionPages'])
    c=previous_base(r['unit'],r['question'],r['publishedTotal'],pages,r['schemePages'],r['item'],r['roman'])
    for key in ('id','questionRef'):c[key]=c[key].replace('2015','2017')
    c['year']=2017;c['sourceMaterial']['title']=c['sourceMaterial']['title'].replace('2015','2017')
    c['review']['questionPages']=r['questionPages'];c['review']['reviewedAt']='2026-11-18'
    if r.get('questionOptions'):
        c['questionText']+='\n\n'+' / '.join(r['questionOptions'])
        c['review']['questionOptions']=r['questionOptions']
    return c

def writing_card(c,criteria,requirements,note):
    c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
    c['rubric']={'system':'language-writing','criteria':criteria,'taskRequirements':requirements,'markingGuideNote':note}
    return c



def answer_pool(body):
    return [squash(x).rstrip('.') for x in body.split('+') if squash(x)]


def reading(source):
    cards=[]
    for r in source['tasks']:
        unit=r['unit'];key=(unit,r['item'],r['roman']);body=r['publishedSourceBlock']
        if unit not in ('IR1','IR2','CD'):continue
        general=source['ir1Guidance' if unit=='IR1' else 'ir2Guidance' if unit=='IR2' else 'comprehensionGuidance']
        count=r['publishedTotal']//2
        if key==('IR1',None,'ii'):
            ordinary,complete=body.split('Assign full marks:')
            answers=answer_pool(ordinary);complete=squash(complete)
            assert len(answers)==4 and complete=='good in the hot and cold'
            c=as_points(source_card(r),[],1)
            c['rubric']['alternativeSets']=[{'id':'climate-answer','label':'Two details or the complete hot-and-cold answer','sourceText':body,'schemePages':[4]}]
            c['rubric']['groups']=[
                {'id':'two-details','label':'Two distinct details','alternativeSet':'climate-answer','answerCount':2,'rows':[{'id':f'detail-{i}','text':a,'marks':2,'steps':[0,1,2]} for i,a in enumerate(answers,1)]},
                {'id':'complete-answer','label':'Complete answer','alternativeSet':'climate-answer','answerCount':1,'rows':[{'id':'hot-and-cold','text':complete,'marks':4}]}]
            c['rubric']['markingGuideNote']='Choose the two-detail route or the scheme’s complete hot-and-cold answer. The complete answer earns all four marks.'
        elif key==('IR2',None,'iii'):
            categories=re.findall(r'([1-5])\.\s*(.*?)(?=\s+[1-5]\.\s|$)',body)
            assert len(categories)==5
            c=as_points(source_card(r),[squash(a) for _,a in categories],2,steps=[0,1,2])
            c['rubric']['markingGuideNote']='Choose two different categories and give one detail about each. The scheme gives two marks for a complete category response and one for a partially correct response.'
        elif key==('IR2',None,'vi'):
            c=as_points(source_card(r),[body],1,steps=[0,1,2])
            c['rubric']['markingGuideNote']='Assess the complete begin-and-end answer out of two. The bracketed (1) gives the optional day of the month. Use the scheme’s general partial-answer rule when assessing an incomplete response.'
        elif key==('IR2',None,'iv'):
            full,partial=body.split('Assign 1 mark:');answers=answer_pool(full);partial=squash(partial)
            assert answers[:2]==['political propaganda','religious propaganda'] and partial=='propaganda'
            c=as_points(source_card(r),answers[2:],2,steps=[0,1,2])
            c['rubric']['alternativeSets']=[{'id':'propaganda','label':'Specific or partial propaganda answer','sourceText':body,'schemePages':[5]}]
            c['rubric']['groups']=[
                {'id':'specific-propaganda','label':'Specific propaganda details','alternativeSet':'propaganda','answerCount':2,'rows':[{'id':f'specific-{i}','text':a,'marks':2,'steps':[0,1,2]} for i,a in enumerate(answers[:2],1)]},
                {'id':'partial-propaganda','label':'Partial propaganda detail','alternativeSet':'propaganda','answerCount':1,'rows':[{'id':'propaganda','text':partial,'marks':1}]},
                *c['rubric']['groups']]
            c['rubric']['allocationCap']={'maxMarks':4,'answerCount':2,'sourceText':general,'schemePages':[5]}
            c['rubric']['markingGuideNote']='Give two distinct details. A generic propaganda answer earns the printed one mark; do not claim it again for a detail already counted as political or religious propaganda.'
        else:
            partial=[]
            m=re.search(r'(?i)assign (?:one|1) mark:',body)
            if m:full,partial=body[:m.start()],answer_pool(body[m.end():])
            else:full=body
            if key==('IR2',None,'v'):
                full=re.sub(r'^\s*1\.\s*','',full)
                full=re.sub(r'\s+2\.\s+', ' + ', full)
            answers=answer_pool(full)
            c=as_points(source_card(r),answers+partial,count,steps=[0,1,2])
            for g in c['rubric']['groups'][len(answers):]:
                g['rows'][0]['marks']=1;g['rows'][0].pop('steps',None)
            c['rubric']['markingGuideNote']='Choose distinct details up to the number requested. The scheme gives two marks for a complete idea and one for a partially correct idea.'
            if key==('IR1',None,'vii'):
                assert len(answers)==15 and partial==['snow','little sun','wintery']
                # Full and partial descriptions of one weather feature are
                # alternatives within one detail, not two independent credits.
                c['rubric']['groups']=c['rubric']['groups'][:len(answers)]
                for prefix,answer in [('fresh/clean/white snow','snow'),('sunny','little sun'),('cold winters','wintery')]:
                    groups=[g for g in c['rubric']['groups'] if g['rows'][0]['text'].startswith(prefix)]
                    assert len(groups)==1
                    groups[0]['rows'].append({'id':'named-partial','text':answer,'marks':1})
                c['rubric']['markingGuideNote']+=' Claim cold winters or hot summers only if that detail was not already rewarded in question ii. Full and partial descriptions of the same weather feature share one detail.'
        c['rubric']['taskRequirements']=[general,body,source['generalWrittenGuidance']]
        c['review']['guidancePages']=[3,4 if unit=='IR1' else 5 if unit=='IR2' else 8]
        cards.append(c)
    assert len(cards)==27 and sum(c['totalMarks'] for c in cards)==88
    return cards

# Native page/table checks bind the language, matching and writing cards.

from ru_review_2026_hl import mark_range


def no_printed_answer(c,pages):
    c['rubric']['markingGuideNote']='The scheme prints no answer for this part. '+c['rubric']['markingGuideNote']
    c['review']['noPrintedAnswer']={'fixedLine':'The scheme prints no answer for this part.','schemePages':pages,'evidence':'reviews/russian-2017-ol-sec-20261118/archive-recheck.json'}
    return c


def language_and_matching(docs,source):
    result=[]
    for r in source['tasks']:
        unit=r['unit'];body=r['publishedSourceBlock']
        if unit not in ('LA1','LA2','MM','SD'):continue
        c=source_card(r)
        if unit=='LA1':
            phrases=['дом в горах Алтая','стиральная комната','прекрасное место для отдыха']
            for phrase in phrases:
                assert squash(phrase) in squash(docs['paper'][3].get_text())
                assert phrase in body
            c['questionText']+='\n\n'+'\n'.join(phrases)
            c=writing_card(c,[criterion('cursive','Handwritten/cursive script',6,list(range(7)),[body])],[body],
                'Assess all three handwritten phrases together. Deduct half a mark for each incorrectly formed letter, do not deduct again for repeated errors, and round the remaining mark up to the next whole number. The scheme gives six marks for the complete exercise.')
            no_printed_answer(c,[4])
        elif unit=='LA2':
            pairs=re.findall(r'([А-Яа-яЁё]+(?:\s+[А-Яа-яЁё]+)*)\s+(feminine singular|masculine singular|neuter singular|plural)',body)
            assert len(pairs)==6,pairs
            c=as_points(c,[squash(a)+' — '+b for a,b in pairs],6)
            for g in c['rubric']['groups']:g['rows'][0]['marks']=1
            c['rubric']['taskRequirements']=[body]
            c['rubric']['markingGuideNote']='Claim one mark for each correct gender or number classification.'
        elif unit=='MM':
            tables=docs['scheme'][5].find_tables().tables
            rows=[row for table in tables for row in table.extract() if len(row)==2 and str(row[0]).strip().isdigit()]
            assert [int(row[0]) for row in rows]==[10,3,2,4,5,6,1,9,8,7],rows
            c=as_points(c,[squash(str(a))+' — '+squash(b) for a,b in rows],10)
            for g in c['rubric']['groups']:g['rows'][0]['marks']=4
            c['rubric']['taskRequirements']=[body]
            c['rubric']['markingGuideNote']='Match all ten descriptions to the numbered departments. The scheme gives four marks for each correct match.'
        else:
            # These are the inserted forms in the two completed dialogues, not
            # their word-bank order. The underlined positions were visually checked on the fresh SEC copy.
            answers=['Чем','Как','Что','Какие','кем','Чем','Что','Когда','Где','какое']
            completed=squash(docs['scheme'][6].get_text())
            contexts=['Чем вы сейчас занимаетесь?','Как проводите свободное время?','Что вы любите носить?','Какие цвета предпочитаете?','С кем вы покупаете одежду?','Чем я могу Вам помочь?','Что Вы хотите узнать?','Когда начинаются курсы русского языка?','Где будут занятия?','А в какое время начинаются занятия?']
            assert all(x in completed for x in contexts)
            c=as_points(c,answers,10,labels=[f'Group {"A" if i<5 else "B"}, gap {i%5+1}' for i in range(10)])
            c['rubric']['taskRequirements']=[body]
            c['rubric']['markingGuideNote']='Complete both dialogues. The scheme gives two marks for each of the ten missing words. The rows follow the gaps in the original paper.'
        result.append(c)
    assert len(result)==4 and sum(c['totalMarks'] for c in result)==72
    return result


def writing(docs,source):
    result=[]
    raw_page=lambda n: docs['scheme'][n-1].get_text(sort=False)
    for r in source['tasks']:
        unit=r['unit'];body=r['publishedSourceBlock']
        if unit not in ('SA','EW'):continue
        c=source_card(r);page=14 if unit=='SA' else 15
        tables=docs['paper'][page-1].find_tables().tables
        assert len(tables)==1,(page,len(tables))
        choices=tables[0].extract();assert len(choices)==(5 if unit=='SA' else 3)
        assert all(len(row)==3 for row in choices)
        c['questionText']+='\n\n'+'\n\n'.join(squash(cell) for row in choices for cell in row[1:])
        if unit=='SA':
            content=squash(between(body,'Content of each answer','Textual coherence')).removeprefix('12 ').strip()
            coherent=raw_page(9).split('Textual coherence',1)[1]
            bands=[{'label':mark,'marks':[int(mark)],'guidance':[squash(text)]} for mark,text in re.findall(r'^\s*([0-3])\s+(.+?)(?=^\s*[0-3]\s|\Z)',coherent,re.M|re.S) if not squash(text).startswith('Allocate')]
            assert len(bands)==4,bands
            criteria=[]
            for ident,label in [('first','First chosen topic'),('second','Second chosen topic')]:
                criteria.extend([criterion(ident+'-content',label+': content',12,list(range(0,13,2)),[content]),criterion(ident+'-coherence',label+': textual coherence',3,[0,1,2,3],[],bands)])
            c=writing_card(c,criteria,[body],
                'Choose two topics. For each response, the scheme gives four marks for each of three complete factual details, or two for a partially correct detail, and up to three marks for textual coherence.')
            no_printed_answer(c,[9])
        else:
            tables=docs['scheme'][10].find_tables().tables
            expression=[{'label':squash(mark),'marks':mark_range(squash(mark)),'guidance':[squash(text)]} for mark,text in tables[0].extract()[1:]]
            assert len(expression)==6
            coherent=raw_page(11).split('Allocate 6 marks for textual coherence:',1)[1]
            bands=[{'label':mark,'marks':mark_range(mark),'guidance':[squash(text)]} for mark,text in re.findall(r'^\s*(6|4-5|2-3|1|0)\s+(.+?)(?=^\s*(?:6|4-5|2-3|1|0)\s|\Z)',coherent,re.M|re.S)]
            assert len(bands)==5,bands
            c=writing_card(c,[criterion('content','Communication/content',12,list(range(0,13,2)),['Content: 2 points for content details up to maximum of 12']),criterion('expression','Expression',12,list(range(13)),[],expression),criterion('coherence','Textual coherence',6,list(range(7)),[],bands)],r.get('sourcePageBlocks',[body]),
                'Choose one prompt and assess its complete response. The scheme gives two marks per content detail, up to twelve, twelve for expression and six for textual coherence. No marks are awarded for additional information or content.')
            no_printed_answer(c,[10,11])
        result.append(c)
    assert len(result)==2 and sum(c['totalMarks'] for c in result)==60
    return result


def build_written():
    docs,source=source_records()
    try:
        cards=reading(source)+language_and_matching(docs,source)+writing(docs,source)
        assert len(cards)==len({c['id'] for c in cards})==33
        assert sum(c['totalMarks'] for c in cards)==220
        return cards
    finally:
        for doc in docs.values():doc.close()


def approved_listening(source):
    evidence=ROOT/'scripts/markbank/authoring/reviews/russian-2017-ol-sec-20261118'
    approval=json.loads((evidence/'listening-approval.json').read_text())
    proposal_path=evidence/'listening-allocation-proposal.json'
    assert approval['answer']=='Approve 5 marks per detail'
    assert hashlib.sha256(proposal_path.read_bytes()).hexdigest()==approval['proposalSha256']
    proposal=json.loads(proposal_path.read_text())
    assert proposal['conflict']['sectionTotals']==[25]*4
    assert proposal['conflict']['requestedDetailsPerSection']==[5]*4
    assert proposal['conflict']['generalLine'] in source['listeningGuidance']
    audio=next(r['source'] for r in json.loads((ROOT/'data/russianAudio.json').read_text()) if r['year']==2017)
    records=[r for r in source['tasks'] if r['component']=='aural']
    assert len(records)==len(proposal['cards'])==18
    topics=[['russian-0-5','russian-0-7','russian-0-7','russian-0-7','russian-0-5'],['russian-0-8','russian-0-8','russian-0-5','russian-0-3'],['russian-0-5','russian-0-5','russian-0-5','russian-0-8'],['russian-0-7','russian-0-3','russian-0-3','russian-2-11','russian-0-7']]
    pools=[6,9,10,5,8,15,2,5,1,3,2,7,5,3,1,9,3,8]
    partial_expected={'ru-2017-ol-l1-3-i':['34 (people)'],'ru-2017-ol-l1-4':['winner','Azerbaijan'],'ru-2017-ol-l2-2':['kids up to the age of …'],'ru-2017-ol-l2-3-ii':['friendship'],'ru-2017-ol-l4-3':['Facebook']}
    position={f'L{s}':0 for s in range(1,5)};cards=[]
    for r,pool,approved in zip(records,pools,proposal['cards']):
        count=approved['requestedDetails'];assert count in (1,2)
        assert r['item'] is not None
        part=str(r['item'])+(f"({r['roman']})" if r['roman'] else '')
        assert part==approved['part']
        assert approved['proposedMaximum']==count*5
        body=r['publishedSourceBlock'];match=re.search(r'Assign 3 marks(?: for)?:',body)
        full=body[:match.start()] if match else body
        partial=answer_pool(body[match.end():]) if match else []
        answers=answer_pool(full)
        assert len(answers)==pool,(r['id'],answers)
        assert partial==partial_expected.get(r['id'],[]),(r['id'],partial)
        c=as_points(source_card({**r,'publishedTotal':count*5}),answers+partial,count)
        for i,g in enumerate(c['rubric']['groups']):g['rows'][0]['marks']=5 if i<len(answers) else 3
        c['rubric']['taskRequirements']=[source['listeningGuidance'],*(body.split('Assign 3 marks:',1)[0:1]+['Assign 3 marks:'+body.split('Assign 3 marks:',1)[1]] if r['id']=='ru-2017-ol-l2-2' else [body])]
        c['rubric']['markingGuideNote']='Source conflict: the scheme says “Award two marks for each correct/relevant point.” It also prints 25 marks for each of four sections, with five requested details per section, and named three-mark answers. This card uses five marks per complete requested detail, inferred from the section totals and approved on 18 November 2026; five is not a printed per-detail award. The explicitly printed three-mark answers remain worth three. Select distinct details up to the number requested.'
        c['review']['allocationApproval']='reviews/russian-2017-ol-sec-20261118/listening-approval.json'
        c['review']['sourceConflict']={'printedGeneralMarksPerDetail':2,'printedSectionTotal':25,'requestedDetailsInSection':5,'approvedInferredMarksPerDetail':5,'explicitPartialMarks':3}
        c['review']['guidancePages']=[12]
        section=r['unit'];c['topicId']=topics[int(section[1:])-1][position[section]];position[section]+=1
        c['additionalTopicIds']=['russian-1-0']
        c['sourceMaterial']['kind']='source-question'
        c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
        c['audioMaterial']=audio
        cards.append(c)
    assert len(cards)==18 and sum(c['totalMarks'] for c in cards)==100
    assert all(sum(c['totalMarks'] for c in cards if c['section']==f'L{s}')==25 for s in range(1,5))
    return cards


def build():
    docs,source=source_records()
    try:
        cards=reading(source)+language_and_matching(docs,source)+writing(docs,source)+approved_listening(source)
        assert len(cards)==len({c['id'] for c in cards})==51
        assert sum(c['totalMarks'] for c in cards)==320
        return cards
    finally:
        for doc in docs.values():doc.close()

def raw_scheme_text():
    path=ROOT/'examiner-reports/russian/schemes/2017-ol.pdf'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==METADATA['scheme']['sha256']
    with fitz.open(path) as document:
        pages=[page.get_text() for page in document]
    raw='\n\n'.join(f'## Page {n+1}\n\n'+text for n,text in enumerate(pages))+'\n'
    joined='\n\n'.join(f'### Joined original page {n+1}\n\n'+squash(text) for n,text in enumerate(pages))
    return raw+'\n# Original pages with line wraps joined\n\n'+joined+'\n'

if __name__=='__main__':
    from ru_review_2026_hl import save_reviewed
    save_reviewed(build_written() if '--written-only' in sys.argv else build())
    (ROOT/'examiner-reports/russian/schemes/2017-ol.md').write_text(raw_scheme_text())
