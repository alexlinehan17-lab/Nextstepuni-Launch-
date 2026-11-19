#!/usr/bin/env python3
"""2014 Ordinary Russian: 30 written + 20 listening tasks from original PDFs."""
import hashlib
import json
import re
import fitz
from ru_paper import bag, score
from ru_review_2026_hl import ROOT, squash, between, base as higher_base, as_points, mark_range, save_reviewed
from ru_review_2015_ol import page_text, draw_text, roman_blocks, numbered_blocks, question_text, source_split
from ru_review_2018_ol import criterion
from ru_source_text import open_scheme

FILES = {
 'paper': ('papers/2014-ol-000-paper.pdf','fa8c43f85b8c65aa24a0989c22213a548c729106057965052908d8a887107eef'),
 'aural': ('papers/2014-ol-A00-paper.pdf','1e2b3340b53b7ecd8f8e2deeb9ff5ed3b96914f41f3c77aafe21e13f37468720'),
 'scheme': ('schemes/2014-ol.pdf','b3186b37ad28e970e617c4c9fc3710628400da21c59a2dd18e51f444799e2d3c'),
}

def opened_sources():
 docs={}
 for key,(relative,digest) in FILES.items():
  path=ROOT/'examiner-reports/russian'/relative
  assert hashlib.sha256(path.read_bytes()).hexdigest()==digest
  docs[key]=open_scheme(2014,'ol') if key=='scheme' else fitz.open(path)
 return docs

def base(unit,text,total,pages,scheme_pages,item=None,roman=None):
 c=higher_base(unit,text,total,pages,scheme_pages,item,roman)
 c['id']=c['id'].replace('2026','2014').replace('-hl-','-ol-')
 c['year']=2014;c['level']='ordinary'
 c['questionRef']=f'2014 OL Section {unit}'+(f' Q{item}' if item is not None else '')
 if roman:c['questionRef']+=(' Q' if item is None else '')+f'({roman})'
 c['sourceMaterial']['title']=f'2014 Ordinary Russian — {unit}'
 return c

def pool(text):
 return [squash(a) for a in text.split('+') if squash(a)]

def reading(docs):
 S,Q,cards=docs['scheme'],docs['paper'],[]
 for unit,sp,pages,askpages,counts,pools in [
  ('IR1',4,[2,3,4,5],[4,5],[1,2,4,1,2,2],[3,8,16,6,11,8]),
  ('IR2',5,[6,7,8],[8],[1,2,2,3,1,1],[4,5,3,6,3,2])]:
  source=page_text(S,sp).split('Language awareness')[0];blocks=roman_blocks(source)
  asks=[]
  for p in askpages:asks.extend((r,question_text(q),p) for r,q in roman_blocks(page_text(Q,p,(300,30,580,793))))
  assert len(blocks)==len(asks)==len(counts),(unit,blocks,asks)
  general='Allocate 2 marks '+squash(between(source,'Allocate 2 marks','i.'))
  for (roman,block),(qr,question,qp),count,expected in zip(blocks,asks,counts,pools):
   assert roman==qr
   price=re.search(r'\((\d+)(?: marks)?\)',block);assert price,block
   cue=squash(block[:price.start()]);rest=block[price.end():].strip()
   assert int(price.group(1))==count*2
   assert score(bag(question),bag(cue))>.65,(question,cue)
   rest=re.sub(r'^(?:Two|Four) of:\s*','',rest)
   partial=[]
   if 'Assign one mark for:' in rest:rest,part=rest.split('Assign one mark for:');partial=pool(part)
   if 'Assign two marks for:' in rest:rest=rest.replace('Assign two marks for:','+')
   answers=pool(rest);assert len(answers)==expected,(unit,roman,answers)
   c=as_points(base(unit,question,count*2,pages,[sp],roman=roman),answers,count,steps=[0,1,2])
   # Unattached lesser answers remain an independent pool under the same quota.
   # The source does not associate them with one of several full-credit rows.
   for n,answer in enumerate(partial,1):c['rubric']['groups'].append({'id':f'partial-{n}','label':f'Published partial answer {n}','answerCount':1,'rows':[{'id':'partial','text':answer,'marks':1}]})
   c['review']['questionPages']=[qp];c['review']['guidancePages']=[3]
   c['rubric']['taskRequirements']=[general,'Do not penalise answers supplied in Russian.']
   c['rubric']['markingGuideNote']='Answer in English or Irish. The scheme explicitly accepts Russian answers.'
   cards.append(c)
 source=page_text(S,8);blocks=numbered_blocks(source)
 asks=[]
 for p in (14,15):asks.extend((q,r,question_text(t),p) for q,r,t in numbered_blocks(page_text(Q,p,(300,30,580,793))))
 counts=[2,2,2,1,2,2,2,1,1,2,2,1];pools=[4,4,5,1,4,4,4,1,1,4,2,3]
 assert len(blocks)==len(asks)==12
 general='Allocate 2 marks '+squash(between(source,'Allocate 2 marks','1.i.'))
 for (item,roman,block),(qi,qr,question,qp),count,expected in zip(blocks,asks,counts,pools):
  assert (item,roman)==(qi,qr)
  m=re.search(r'\((\d+) marks\)',block);assert m and int(m.group(1))==count*2
  cue=squash(block[:m.start()]);rest=block[m.end():]
  assert score(bag(question),bag(cue))>.65,(question,cue)
  # The printed clock time is one two-mark task. Keep its plus-linked whole
  # answer intact; no invented separate mark for either component.
  answers=[squash(rest)] if (item,roman)==(2,'i') else pool(rest)
  assert len(answers)==expected,(item,roman,answers)
  c=as_points(base('CD',question,count*2,[13,14,15],[8],item,roman),answers,count,steps=[0,1,2])
  c['review']['questionPages']=[qp];c['review']['guidancePages']=[3]
  c['rubric']['taskRequirements']=[general,'Do not penalise answers supplied in Russian.']
  c['rubric']['markingGuideNote']='Answer in English or Irish. The scheme explicitly accepts Russian answers.'
  if (item,roman)==(2,'i'):c['rubric']['markingGuideNote']+=' The complete printed time has a two-mark total; the general one-mark partial-answer rule applies.'
  cards.append(c)
 assert len(cards)==24 and sum(c['totalMarks'] for c in cards)==84
 return cards

def language_and_matching(docs):
 S,Q,cards=docs['scheme'],docs['paper'],[]
 instruction=squash('Write out'+between(page_text(Q,5,(300,450,580,550)),'Write out'))
 target=squash(page_text(Q,5,(20,570,580,590)))
 assert target=='«Орлёнок» — детский центр для детей и подростков 11-16 лет (учащихся 6-10 классов).'
 c=base('LA1',instruction+'\n\n'+target,6,[5],[4]);c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
 c['rubric']={'system':'language-writing','taskRequirements':['Write out the following sentence in cursive/handwritten Cyrillic script. (6 marks)'],
  'criteria':[criterion('formation','Letter formation',3,[0,1,2,3],[]),criterion('transcription','Accurate transcription',3,[0,1,2,3],[])],
  'markingGuideNote':instruction+' The original paper supplies this 3 + 3 allocation. The scheme provides no handwritten exemplar.'}
 c['review']['paperGuidancePages']=[5];cards.append(c)
 question='Sort the following '+squash(between(page_text(Q,9,(300,30,580,130)),'Sort the following'))
 c=base('LA2',question,10,[9],[5]);c['kind']='question';c['tariffModel']={'kind':'questionTotal'}
 for col,label in [((20,590,100,760),'Nouns'),((100,590,250,760),'Adjectives')]:
  # Extract the source's two spatial columns independently, not alternating
  # words from an unreliable flattened table.
  words=[squash(t) for t in page_text(S,5,col).splitlines() if re.search('[А-Яа-яЁё]',t)]
  assert len(words)==5,(label,words)
  for n,word in enumerate(words,1):c['rows'].append({'id':f'{label.lower()}-{n}','kind':'point','verbatim':word,'marks':None,'contextNote':label})
 c['rows'][0]['contextNote']+='. The scheme gives 10 marks for the complete classification exercise and no per-word allocation. Individual answers can be reviewed; numeric self-scoring is unavailable for this task.'
 cards.append(c)
 question='Complete the table '+squash(between(page_text(Q,10,(300,30,580,150)),'Complete the table'))
 table=S[5].find_tables().tables[0].extract();assert len(table)==11 and table[4][2]=='Стать пилотом'
 table=table[:4]+table[5:];c=base('MM',question,40,[10],[6]);c['kind']='question'
 variants=[]
 for route in ('normal','swapped'):
  answers=[squash(r[2]) for r in table]
  if route=='swapped':answers[-2:]=answers[-2:][::-1]
  rows=[{'id':f'match-{n}','kind':'point','verbatim':answer,'marks':4,'contextNote':squash(row[0])+' '+squash(row[1])} for n,(row,answer) in enumerate(zip(table,answers),1)]
  rows[0]['contextNote']+='. 4 marks for each correct answer. The completed example “Стать пилотом” is not scored.'
  rows[-2]['contextNote']+='. The scheme labels the last answers “10/11” and “11/10”; select one complete accepted route.'
  variants.append({'id':route,'label':'Profession then position' if route=='normal' else 'Position then profession','rows':rows})
 c['rows']=variants[0]['rows'];c['answerVariants']=variants
 c['taskGroups']=[{'sourceCardId':f"{c['id']}-field-{n}",'label':squash(row[1]),'marks':4,'rowIds':[f'match-{n}']} for n,row in enumerate(table,1)]
 cards.append(c)
 instruction='In the following interviews '+squash(between(page_text(Q,11,(300,30,580,125)),'In the following interviews'))
 question=instruction+'\n\n'+'Интервью'+between(page_text(Q,11),'Интервью')+'\n\n'+page_text(Q,12)
 c=as_points(base('SD',question,20,[11,12],[7]),['Сколько','Когда','Кто','Чья','Где','как','чем','Чего','сколько','Какие'],10,{2:['Сколько']})
 c['rubric']['taskRequirements']=['In the following interviews supply the missing question words. Select your answers from the list supplied below. (2 marks per answer)']
 c['rubric']['markingGuideNote']='Complete both interviews. In the first interview, gap 3 accepts “Кто” for 2 marks or “Сколько” for 1 mark.'
 cards.append(c)
 assert len(cards)==4 and sum(c['totalMarks'] for c in cards)==76
 return cards

def writing(docs):
 S,Q,cards=docs['scheme'],docs['paper'],[]
 instructions='Write 3 '+squash(between(page_text(Q,16,(300,30,580,195)),'Write 3'))
 options=page_text(Q,16,(405,198,580,396));assert len(numbered_blocks(options))==5
 question=instructions+'\n\n'+options
 source=page_text(S,9);content=squash(between(source,'Content of each answer','Textual coherence')).removeprefix('12 ').strip()
 coherence=between(source,'Textual coherence')
 bands=[{'label':n,'marks':[int(n)],'guidance':[squash(t)]} for n,t in re.findall(r'^\s*([0-3])\s+(.+?)(?=^\s*[0-3]\s|\Z)',coherence,re.M|re.S) if not squash(t).startswith('Allocate')];assert len(bands)==4
 c=base('SA',question,30,[16],[9]);c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
 c['rubric']={'system':'language-writing','taskRequirements':['Write 3 – 5 sentences on TWO of the following topics in Russian or English. Each answer should contain three factual details. Marks are awarded for relevant content and textual coherence.','The quality of the English/Russian will only be an assessment factor insofar as it impedes communication.'],'criteria':[criterion(f'{choice}-content',f'{label}: content',12,list(range(0,13,2)),[content]) if part=='content' else criterion(f'{choice}-coherence',f'{label}: textual coherence',3,[0,1,2,3],[],bands) for choice,label in [('first','First chosen topic'),('second','Second chosen topic')] for part in ['content','coherence']],'markingGuideNote':''}
 cards.append(c)
 table=Q[16].find_tables().tables[0].extract();assert len(table)==5
 instruction='Write 6 '+squash(between(page_text(Q,17,(300,30,580,120)),'Write 6'))
 question=instruction+'\n\n'+'\n\n'.join('\n• '.join(squash(p) for p in re.split(r'[\uf0b7•]',row[2])) for row in table)
 source=page_text(S,11);table=S[10].find_tables().tables[0].extract()
 full=[{'label':squash(r[0]),'marks':mark_range(squash(r[0])),'guidance':[squash(r[1])]} for r in table[1:]]
 coherence=between(source,'Allocate 6 marks for textual coherence:')
 bands=[{'label':n,'marks':mark_range(n),'guidance':[squash(t)]} for n,t in re.findall(r'^\s*(\d(?:-\d)?)\s+(.+?)(?=^\s*\d(?:-\d)?\s|\Z)',coherence,re.M|re.S)];assert len(bands)==5
 c=base('EW',question,30,[17],[10,11]);c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
 extra=[]
 for item,_,block in numbered_blocks(page_text(S,10)):
  pieces=[squash(t).rstrip(' +') for t in re.split(r'^\s*x\s*',block,flags=re.M)[1:]]
  assert pieces,(item,block)
  extra.append(f'Choice {item}: '+'; '.join(pieces)+'.')
 c['rubric']={'system':'language-writing','taskRequirements':['Write 6 – 10 sentences on one of the following topics in Russian.','No marks are awarded for additional information/content.'],'criteria':[criterion('content','Communication + content',12,list(range(0,13,2)),['2 points for content details up to maximum of 12']),criterion('expression','Language + expression',12,list(range(13)),[],full),criterion('coherence','Textual coherence',6,list(range(7)),[],bands)],'markingGuideNote':'\n'.join(extra)}
 cards.append(c)
 return cards

def listening(docs):
 S,A,cards=docs['scheme'],docs['aural'],[]
 source='\n'.join(page_text(S,p) for p in (12,13))
 general=[squash(t) for t in re.split(r'^\s*x\s*',between(source,'General:','Award FIVE'),flags=re.M)[1:]]+['Award FIVE marks for each correct/relevant point.'];assert len(general)==6
 sections=re.split(r'SECTION\s+(?:IV|III|II|I)\b',source)[1:];assert len(sections)==4
 pools=[[1,1,1,1,1],[1,3,1,1,1],[9,4,9,4,4],[6,1,1,1,1]]
 firsts=[['c.','a.','d.','a.','a.'],['b.','Personal data','b.','b.','c.'],['From Briansk','A pack','Low sky','supplied skis','Go to a charity'],['Father','b.','c.','b.','d.']]
 topics=[['russian-0-10','russian-0-8','russian-0-8','russian-0-5','russian-0-5'],['russian-0-8','russian-0-14','russian-0-9','russian-0-9','russian-0-9'],['russian-0-7','russian-0-5','russian-0-2','russian-0-10','russian-0-6'],['russian-0-1','russian-0-3','russian-0-7','russian-0-5','russian-0-4']]
 audio=next(r['source'] for r in json.loads((ROOT/'data/russianAudio.json').read_text()) if r['year']==2014)
 for section,text in enumerate(sections,1):
  blocks=numbered_blocks(text);asks=numbered_blocks(page_text(A,section+1,(300,30,580,793)))
  assert len(blocks)==len(asks)==5,(section,blocks,asks)
  for n,((item,roman,block),(qi,qr,q),expected,first) in enumerate(zip(blocks,asks,pools[section-1],firsts[section-1])):
   assert (item,roman)==(qi,qr)
   question=question_text(q)
   cue,rest=source_split(block,first)
   assert score(bag(question.split(' a. ')[0]),bag(cue))>.65,(question,cue)
   partial=None
   if 'Award 3 marks for:' in rest:rest,partial=rest.split('Award 3 marks for:');partial=squash(partial)
   answers=pool(rest);assert len(answers)==expected,(section,item,roman,answers)
   c=as_points(base(f'L{section}',question,5,[section+1],[12 if section<3 else 13],item,roman),answers,1)
   for g in c['rubric']['groups']:g['rows'][0]['marks']=5
   if partial:c['rubric']['groups'][0]['rows'].append({'id':'partial','text':partial,'marks':3})
   c['rubric']['taskRequirements']=general;c['review']['guidancePages']=[12]
   c['topicId']=topics[section-1][n];c['additionalTopicIds']=['russian-1-0']
   c['sourceMaterial']['kind']='source-question';c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.'
   c['audioMaterial']=audio;cards.append(c)
 assert len(cards)==20 and sum(c['totalMarks'] for c in cards)==100
 return cards

def build():
 docs=opened_sources();cards=reading(docs)+language_and_matching(docs)+writing(docs)+listening(docs)
 assert len(cards)==50 and sum(c['totalMarks'] for c in cards)==320
 old={c['id'] for c in json.loads((ROOT/'scripts/markbank/authored/russian.json').read_text())};assert not any(c['id'] in old for c in cards)
 return cards

if __name__=='__main__':save_reviewed(build())
