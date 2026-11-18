#!/usr/bin/env python3
"""2013 Ordinary Russian: independent 24-written/18-listening source census."""
import hashlib
import json
import re
import fitz
from ru_paper import RuPaper, bag, score
from ru_review_2026_hl import ROOT, squash, between, base as higher_base, as_points, mark_range, save_reviewed, bullets
from ru_review_2015_ol import page_text as extract_page, roman_blocks, numbered_blocks, question_text, source_split
from ru_review_2018_ol import criterion

FILES={
 'paper':('papers/2013-ol-000-paper.pdf','48a29fa96259ea535913e07fde760949d91f854dacb10ae8a90cdb0eb9b18a07'),
 'aural':('papers/2013-ol-A00-paper.pdf','3aa28cebff239c2f82bdbf2d82e085112eaf1b8d514d0931e1d1bd37b8d79de2'),
 'scheme':('schemes/2013-ol.pdf','0aafd6dfe0224a50fd53f45934ebb0e32e9241b05ba51c2854e8b712a792a0be'),
}

def page_text(doc,page,box=None):
 # The 2013 scheme footer starts at y782. Keep it out of answer pools and
 # rubric bands, including text continued onto the following page.
 return extract_page(doc,page,box or ((20,30,580,775) if '/schemes/' in doc.name else (20,30,580,793)))

def opened_sources():
 docs={}
 for key,(relative,digest) in FILES.items():
  path=ROOT/'examiner-reports/russian'/relative
  assert hashlib.sha256(path.read_bytes()).hexdigest()==digest
  docs[key]=fitz.open(path)
 return docs

def base(unit,text,total,pages,scheme_pages,item=None,roman=None):
 c=higher_base(unit,text,total,pages,scheme_pages,item,roman)
 c['id']=c['id'].replace('2026','2013').replace('-hl-','-ol-')
 c['year']=2013;c['level']='ordinary'
 c['questionRef']=f'2013 OL Section {unit}'+(f' Q{item}' if item is not None else '')
 if roman:c['questionRef']+=(' Q' if item is None else '')+f'({roman})'
 c['sourceMaterial']['title']=f'2013 Ordinary Russian — {unit}'
 return c

def pool(text):return [squash(a) for a in text.split('+') if squash(a)]

def reading(docs,P):
 S,Q,cards=docs['scheme'],docs['paper'],[]
 general='Allocate 2 marks '+squash(between(page_text(S,4),'Allocate 2 marks','Answer the following'))
 question='What kind '+squash(between(page_text(Q,3,(300,30,580,793)),'What kind','(16 marks)'))+' (16 marks)'
 table=S[3].find_tables().tables[0].extract();assert len(table)==9
 c=as_points(base('IR1',question,16,[2,3],[4],roman='i'),[squash(r[0])+' — '+squash(r[2]) for r in table[1:]],8,steps=[0,1,2])
 c['rubric']['taskRequirements']=[general,squash(table[0][1]),squash(table[0][2])]
 c['rubric']['markingGuideNote']='The original paper requests handwriting and translation. The scheme discounts the handwriting column and awards 2 marks per English translation/equivalent supplied in either answer column; no handwriting mark is inferred.'
 cards.append(c)
 raw=page_text(Q,4,(300,30,580,793));stem='If you were organising '+squash(between(raw,'If you were organising','ii.a'))
 for letter,end,answer in [('a','ii.b','Кавказский дворик / ЛиВуар'),('b','iii','Кавказский дворик')]:
  question=stem+'\n\n'+question_text(between(raw,'ii.'+letter,end))
  c=as_points(base('IR1',question,2,[2,3,4],[4],roman='ii'),[answer],1,steps=[0,1,2]);c['id']+='-'+letter;c['questionRef']+='('+letter+')'
  c['review']['questionPages']=[4];c['rubric']['taskRequirements']=[general];cards.append(c)
 question='Complete the following '+squash(between(raw,'Complete the following'))
 c=base('IR1',question,8,[4],[5],roman='iii');c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
 table=S[4].find_tables().tables[0].extract();assert len(table)==8
 requirement=squash('Complete the following'+between(page_text(S,5),'Complete the following','1.'))
 c['rubric']={'system':'language-writing','taskRequirements':[requirement],'criteria':[criterion(f'line-{n}',squash(row[0]),1,[0,1],[]) for n,row in enumerate(table,1)],'markingGuideNote':'The scheme awards one mark for each completed form line and supplies no personal example answers. Answer in Russian or English; do not supply real contact information. The original booklet and the scheme phrase some field labels differently.'}
 cards.append(c)
 asks=roman_blocks(page_text(Q,7,(300,30,580,793)).split('Language awareness')[0]);assert len(asks)==2
 for roman,block in asks:
  question=question_text(block)
  c=as_points(base('IR2',question,2 if roman=='i' else 20,[6,7],[5] if roman=='i' else [5,6],roman=roman),['(not far from centre of ) Dublin','Donnybrook'],1,steps=[0,1,2])
  c['review']['questionPages']=[7];c['rubric']['taskRequirements']=[general]
  if roman=='ii':
   # Extract nine named source pools by page layout. Embedded // stays within
   # its printed plus-delimited unit; it never creates extra priced details.
   source='Group 1 '+between(page_text(S,5),'Group 1')+'\nGroup 5 '+between(page_text(S,6),'Group 5','3. Select')
   heads=list(re.finditer(r'Group\s+(\d)\s+',source));assert len(heads)==9
   groups=[]
   for i,h in enumerate(heads):
    answers=pool(source[h.end():heads[i+1].start() if i+1<len(heads) else len(source)])
    assert len(answers)==[4,4,5,3,4,5,5,6,5][i],(i,answers)
    groups.append({'id':f'group-{h.group(1)}','label':f'Group {h.group(1)}','answerCount':2,'rows':[{'id':f'detail-{n}','text':answer,'marks':2,'steps':[0,1,2]} for n,answer in enumerate(answers,1)]})
   c['rubric']['groups']=groups;c['rubric']['count']=5
   c['rubric']['taskRequirements'].append('The advertisement identifies nine groups of learners. Select any five groups; give two details about each group. (2 marks per detail x 2 details per group x 5 groups = 20 marks)')
   c['rubric']['markingGuideNote']='Choose five learner groups and two details in each. The source’s embedded // wording is retained within its printed plus-delimited detail; it does not create an additional answer slot.'
  cards.append(c)
 source='\n'.join(page_text(S,p) for p in (8,9)).split('SECTION II')[0]
 sections=re.split(r'Section\s+[1-4]\s*\(5 x 2\)',source)[1:];assert len(sections)==4
 firsts=[['Evgeniy:','One of:','a volleyball','One of:'],['Three of:','Liverpool'],['Three of:','Three of:'],['One of:','One of:','Two of:','One of:']]
 counts=[[2,1,1,1],[3,2],[3,2],[1,1,2,1]];pools=[[2,3,1,3],[12,2],[4,6],[3,3,6,2]]
 for section,text in enumerate(sections,1):
  blocks=numbered_blocks(text);assert len(blocks)==len(counts[section-1]),(section,blocks)
  for n,((item,_,block),first,count,expected) in enumerate(zip(blocks,firsts[section-1],counts[section-1],pools[section-1])):
   roman=['i','ii','iii','iv'][item-1]
   b=next(b for b in P.blocks if b.unit=='CD' and b.item==section and b.side=='R' and b.text.startswith(roman+'.'))
   question=re.sub(r'^[iv]+\.\s*','',b.text);cue,rest=source_split(block,first)
   assert score(bag(question),bag(cue))>.65,(question,cue)
   price=re.search(r'\((\d+) x 2 = (\d+)\)',cue);assert price and int(price.group(1))==count and int(price.group(2))==count*2,(cue,count)
   rest=re.sub(r'^(?:One|Two|Three) of:\s*','',rest)
   partial=None
   if '1 mark for:' in rest:rest,partial=rest.split('1 mark for:');partial=squash(partial)
   if 'Assign one mark for a mention of football.' in rest:rest=rest.split('Assign one mark')[0];partial='football'
   answers=[squash(a) for a in rest.splitlines() if squash(a)] if (section,item)==(1,1) else pool(rest)
   assert len(answers)==expected,(section,item,answers)
   c=as_points(base('CD',question,count*2,[11,12,13],[8] if section<3 else [8,9] if section==3 else [9],section,roman),answers,count,steps=[0,1,2])
   c['review']['questionPages']=[b.page+1];c['review']['guidancePages']=[8]
   c['rubric']['taskRequirements']=['Allocate 2 marks for each correct idea/concept (each idea/concept separated by +) and 1 mark for a partially correct idea/concept [unless otherwise stated].']
   if partial:c['rubric']['groups'][0]['rows'].append({'id':'partial','text':partial,'marks':1})
   if (section,item)==(3,2):c['rubric']['markingGuideNote']='Source discrepancy: the booklet asks for two benefits and the scheme prices the task at 2 x 2 = 4 marks on page 8. The continued answer list on page 9 starts “Three of”. The two-answer quota and four-mark total are retained.'
   cards.append(c)
 assert len(cards)==18 and sum(c['totalMarks'] for c in cards)==90
 return cards


def language_and_matching(docs):
 S,Q,cards=docs['scheme'],docs['paper'],[]
 question='Give three phrases '+squash(between(page_text(Q,5,(300,30,580,180)),'Give three phrases','(6 marks)'))+' (6 marks)'
 guidance=squash('Award full marks'+between(page_text(S,5),'Award full marks','Example/пример'))
 c=base('LA1',question,6,[2,3,5],[5]);c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
 c['rubric']={'system':'language-writing','taskRequirements':[guidance,'You may not use the example.'],'criteria':[criterion(g,g.title()+' phrase',2,[0,1,2],[guidance]) for g in ['masculine','feminine','neuter']],'markingGuideNote':'The printed example банкетный зал cannot be used. The scheme accepts another correct-gender noun phrase whether or not it occurs in the passage; no closed phrase list is imposed.'};cards.append(c)
 question='Select two '+squash(between(page_text(Q,7,(300,550,580,690)),'Select two','(4 marks)'))+' (4 marks)'
 pairs=[('школа','дошкольный'),('русский','русскоговорящий'),('работать','работа'),('сын','усыновленный'),('готовить','подготовительный'),('знать','знание')]
 c=as_points(base('LA2',question,4,[6,7],[6]),[a+' — '+b for a,b in pairs],2);c['rubric']['taskRequirements']=['Select two of the words listed below. In the text find a word with the same stem: (2 marks x 2 = 4 marks)'];cards.append(c)
 question='Match the following interviews '+squash(between(page_text(Q,8,(300,30,580,125)),'Match the following interviews'))
 table=S[5].find_tables().tables[0].extract();assert len(table)==8
 c=as_points(base('MM',question,40,[8,9],[6]),[squash(r[0])+' — '+squash(r[1]) for r in table],8)
 for g in c['rubric']['groups']:g['rows'][0]['marks']=5
 c['rubric']['taskRequirements']=['Match the following interviews with the following interview titles. Insert the number of the appropriate interview in the table listing the titles. (5 marks for each correct answer)'];cards.append(c)
 question='Give the missing '+squash(between(page_text(Q,10,(300,30,580,110)),'Give the missing'))+'\n\n'+'Focail'+between(page_text(Q,10),'Focail')
 answers=['Как','сколько','где','Какую','Какая/ Кто','Что','Кто','чем','Где','Что']
 c=as_points(base('SD',question,20,[10],[7]),answers,10)
 c['rubric']['taskRequirements']=['Supply the missing question in the following interview with Laura. Select your answers from the list supplied below. (2 marks per answer)']
 c['rubric']['markingGuideNote']='Complete all ten printed gaps. The first numbered exchange contains three gaps. Exchange 3 accepts either Какая or Кто.';cards.append(c)
 return cards


def writing(docs):
 S,Q,cards=docs['scheme'],docs['paper'],[]
 raw=page_text(Q,14,(300,30,580,470));question=question_text('Write 3'+between(raw,'Write 3'))
 source=page_text(S,10);content=squash(between(source,'Content of each answer','Textual coherence')).removeprefix('12 ').strip()
 coherence=between(source,'Textual coherence')
 bands=[{'label':n,'marks':[int(n)],'guidance':[squash(t)]} for n,t in re.findall(r'^\s*([0-3])\s+(.+?)(?=^\s*[0-3]\s|\Z)',coherence,re.M|re.S) if not squash(t).startswith('Allocate')];assert len(bands)==4
 c=base('SA',question,30,[14],[9,10]);c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
 c['rubric']={'system':'language-writing','taskRequirements':['Write 3-5 sentences on TWO of the following topics in Russian or English. Each answer should contain three factual details. Marks are awarded for relevant content and textual coherence.','The quality of the English/Russian will only be an assessment factor insofar as it impedes communication.'],'criteria':[criterion(f'{choice}-content',f'{label}: content',12,list(range(0,13,2)),[content]) if part=='content' else criterion(f'{choice}-coherence',f'{label}: textual coherence',3,[0,1,2,3],[],bands) for choice,label in [('first','First chosen topic'),('second','Second chosen topic')] for part in ['content','coherence']],'markingGuideNote':''};cards.append(c)
 question='Write 6 '+between(page_text(Q,15,(300,30,580,793)),'Write 6')+'\n\n'+page_text(Q,16,(300,30,580,420))
 source=page_text(S,12);table=S[11].find_tables().tables[0].extract()
 full=[{'label':squash(r[0]),'marks':mark_range(squash(r[0])),'guidance':[squash(r[1])]} for r in table[1:]]
 coherence=between(source,'Allocate 6 marks for textual coherence:')
 bands=[{'label':n,'marks':mark_range(n),'guidance':[squash(t)]} for n,t in re.findall(r'^\s*(\d(?:-\d)?)\s+(.+?)(?=^\s*\d(?:-\d)?\s|\Z)',coherence,re.M|re.S)];assert len(bands)==5
 c=base('EW',question,30,[15,16],[11,12]);c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
 c['rubric']={'system':'language-writing','taskRequirements':['Write 6-10 sentences on one of the following topics IN RUSSIAN.','No marks are awarded for additional information/content.'],'criteria':[criterion('content','Communication + content',12,list(range(0,13,2)),['2 points for content details up to maximum of 12']),criterion('expression','Language + expression',12,list(range(13)),[],full),criterion('coherence','Textual coherence',6,list(range(7)),[],bands)],'markingGuideNote':''};cards.append(c)
 return cards


def listening(docs):
 S,A,cards=docs['scheme'],docs['aural'],[]
 source='\n'.join(page_text(S,p) for p in (13,14))
 general=bullets(between(source,'General:','Award FIVE'))+['Award FIVE marks for each correct/relevant point.'];assert len(general)==6
 sections=re.split(r'Section\s+[1-4]\b',source)[1:];assert len(sections)==4
 # This year's scheme omits dots after some roman markers.
 def blocks(text):
  heads=list(re.finditer(r'^\s*(\d)\.\s*(?:(i{1,3})\.?\s*)?(?=[A-Z])',text,re.M))
  return [(int(h.group(1)),h.group(2),text[h.end():heads[n+1].start() if n+1<len(heads) else len(text)]) for n,h in enumerate(heads)]
 counts=[[1]*5,[1,1,2,1],[1,1,1,2],[1]*5]
 pools=[[1,1,3,1,1],[1,1,7,1],[4,2,7,20],[7,1,3,1,1]]
 firsts=[['(b) 7','(b) February','One of:','(c) Wicklow','(c) St.'],['b.','b.','Two of:','c.'],['One of:','One of:','One of:','Two of:'],['One of:','a.','One of:','d.','b.']]
 topics=[['russian-0-9','russian-0-9','russian-0-5','russian-0-7','russian-0-2'],['russian-0-5','russian-0-7','russian-0-5','russian-0-7'],['russian-0-4','russian-0-4','russian-0-4','russian-0-2'],['russian-0-4','russian-0-1','russian-0-5','russian-0-5','russian-0-3']]
 audio=next(r['source'] for r in json.loads((ROOT/'data/russianAudio.json').read_text()) if r['year']==2013)
 for section,text in enumerate(sections,1):
  answers_blocks=blocks(text);asks=blocks(page_text(A,section+1,(300,30,580,793)))
  assert len(answers_blocks)==len(asks)==len(counts[section-1]),(section,answers_blocks,asks)
  for n,((item,roman,block),(qi,qr,q),count,expected,first) in enumerate(zip(answers_blocks,asks,counts[section-1],pools[section-1],firsts[section-1])):
   assert (item,roman)==(qi,qr)
   question=question_text(q);cue,rest=source_split(block,first)
   if (section,item,roman)==(2,2,'ii'):
    assert question=='Apart from the parade, what forms of entertainment will there be? Give two details.'
    assert cue=='Give two details about the entertainment that will be available.'
   else:assert score(bag(question.split(' a. ')[0]),bag(cue))>.65,(question,cue)
   rest=re.sub(r'^(?:One|Two) of:\s*','',rest);answers=pool(rest);assert len(answers)==expected,(section,item,roman,answers)
   c=as_points(base(f'L{section}',question,count*5,[section+1],[13] if section==1 else [13,14] if section==2 else [14],item,roman),answers,count)
   for g in c['rubric']['groups']:g['rows'][0]['marks']=5
   c['rubric']['taskRequirements']=general;c['review']['guidancePages']=[13]
   c['topicId']=topics[section-1][n];c['additionalTopicIds']=['russian-1-0']
   c['sourceMaterial']['kind']='source-question';c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
   c['audioMaterial']=audio;cards.append(c)
 assert len(cards)==18 and sum(c['totalMarks'] for c in cards)==100
 return cards


def build():
 docs=opened_sources();cards=reading(docs,RuPaper(2013,'ol'))+language_and_matching(docs)+writing(docs)+listening(docs)
 assert len(cards)==42 and sum(c['totalMarks'] for c in cards)==320
 old={c['id'] for c in json.loads((ROOT/'scripts/markbank/authored/russian.json').read_text())};assert not any(c['id'] in old for c in cards)
 return cards

if __name__=='__main__':save_reviewed(build())
