#!/usr/bin/env python3
"""2012 Ordinary Russian: independent 23-written/19-listening source census."""
import hashlib
import json
import re
import fitz
from ru_paper import RuPaper, bag, score
from ru_review_2026_hl import ROOT, squash, between, as_points, mark_range, save_reviewed, bullets
from ru_review_2013_ol import base as previous_base, page_text, pool
from ru_review_2015_ol import roman_blocks, numbered_blocks, question_text, source_split
from ru_review_2018_ol import criterion

FILES={
 'paper':('papers/2012-ol-000-paper.pdf','b6aba8df1ea656cf4efa1f1189ebfe6fb204c30969bc0a8d0645ddc3aadc9d61'),
 'aural':('papers/2012-ol-A00-paper.pdf','45db827722fbc93fcea8970edde10c6e30cd8011d343a33ffc2caedaf25d4fa6'),
 'scheme':('schemes/2012-ol.pdf','8dfb1ad867bbb88bbbaf13a5608bd0c0c9c94eae8a792f6f4104e13cb17d0071'),
}

def opened_sources():
 docs={}
 for key,(relative,digest) in FILES.items():
  path=ROOT/'examiner-reports/russian'/relative
  assert hashlib.sha256(path.read_bytes()).hexdigest()==digest
  docs[key]=fitz.open(path)
 return docs

def base(unit,text,total,pages,scheme_pages,item=None,roman=None):
 c=previous_base(unit,text,total,pages,scheme_pages,item,roman)
 c['id']=c['id'].replace('2013','2012');c['year']=2012
 c['questionRef']=c['questionRef'].replace('2013','2012')
 c['sourceMaterial']['title']=c['sourceMaterial']['title'].replace('2013','2012')
 return c

def writing_card(c,requirements,criteria,note=''):
 c.pop('rows');c.pop('tariffModel');c['kind']='rubric'
 c['rubric']={'system':'language-writing','taskRequirements':requirements,'criteria':criteria,'markingGuideNote':note}
 return c

def written_guidance(c,general):
 c['review']['guidancePages']=[3]
 c['rubric']['taskRequirements']=[general,'Do not penalise answers supplied in Russian.','Where a candidate uses the same information in response to two or more questions, accept the first answer only.']
 c['rubric']['markingGuideNote']='Answer in English or Irish unless the task specifies otherwise. The scheme explicitly accepts Russian answers. Do not claim the same information again in another question.'
 return c

def reading(docs,P):
 S,Q,cards=docs['scheme'],docs['paper'],[]
 general='Allocate 2 marks '+squash(between(page_text(S,4),'Allocate 2 marks','1. Кафе'))
 def bare_romans(text):
  hs=list(re.finditer(r'^\s*(iv|i{1,3})\s+',text,re.M))
  return [(h.group(1),text[h.end():hs[n+1].start() if n+1<len(hs) else len(text)]) for n,h in enumerate(hs)]
 asks=bare_romans(page_text(Q,4,(300,30,580,793)));blocks=bare_romans(page_text(S,4));assert len(asks)==len(blocks)==4
 for (roman,q),(sr,block),count,expected,first in zip(asks[:3],blocks[:3],[1,2,1],[6,6,1],['(people','international +','five (5)']):
  assert roman==sr
  question=question_text(q);cue,rest=source_split(block,first);assert score(bag(question),bag(cue))>.7
  price=re.search(r'(\d+) marks',rest);assert int(price.group(1))==count*2
  answers=pool(rest[:price.start()]);assert len(answers)==expected
  c=as_points(base('IR1',question,count*2,[2,3,4],[4],roman=roman),answers,count,steps=[0,1,2]);written_guidance(c,general)
  if roman=='ii':c['rubric']['taskRequirements'].append('no marks: kitchen food')
  cards.append(c)
 stem=question_text(asks[3][1].split('a)')[0])
 aq=question_text(asks[3][1].split('a)',1)[1]).split('Dish 1')[0].strip()
 remainder=page_text(Q,5,(300,30,580,793))
 qs={'a':aq,'b':question_text(between(remainder,'b)','c)')),'c':question_text(between(remainder,'c)','d)')),'d':question_text(between(remainder,'d)'))}
 source=blocks[3][1]
 rows=re.findall(r'^\s*([1-5])\s+([1-3])\s+(.+?)(?=^\s*[1-5]\s+[1-3]\s|\Z)',between(source,'Marking of handwriting:','b)'),re.M|re.S)
 assert len(rows)==5,rows
 dishbands=[{'label':a,'marks':[int(a)],'guidance':[squash(t)]} for a,_,t in rows]
 drinkbands=[{'label':str(n),'marks':[n],'guidance':[squash(t) for _,b,t in rows if int(b)==n]} for n in (3,2,1)]
 criteria={
  'a':[criterion('dish-1','Dish one',5,list(range(6)),[],dishbands),criterion('dish-2','Dish two',5,list(range(6)),[],dishbands),criterion('drink','Drink',3,list(range(4)),[],drinkbands)],
  'b':[criterion(f'dish-{dish}-ingredient-{n}',f'Dish {dish}: ingredient {n}',2,[0,1,2],['2 marks for each ingredient']) for dish in (1,2) for n in (1,2)],
  'c':[criterion('bill','Correct bill',4,[0,1,4],['4 marks for correct bill'])],
  'd':[criterion('vegetarian','Vegetarian dish',2,[0,1,2],['vegetarian dish'])],
 }
 for letter,total in [('a',13),('b',8),('c',4),('d',2)]:
  c=writing_card(base('IR1',stem+'\n\n'+qs[letter],total,[2,3,4,5],[4],roman='iv'),[],criteria[letter])
  c['id']+='-'+letter;c['questionRef']+='('+letter+')';written_guidance(c,general)
  c['rubric']['markingGuideNote']+=' The scheme gives criteria for your own menu choices and no worked example. Select two courses from different menu sections and one drink.'
  if letter=='a':
   c['rubric']['taskRequirements'].append('Marks are awarded for the quality of your handwriting, not for your choice of dish.')
   c['rubric']['markingGuideNote']+=' The two dish names carry 5 marks each and the drink name 3. No handwritten exemplar is supplied.'
   c['rubric']['markingGuideNote']+=' The scheme’s English Text 1 heading gives 35 marks while its Irish heading gives 30; the priced subparts and original paper total 35.'
  if letter=='c':c['rubric']['markingGuideNote']+=' Four marks are for a correct bill; the general one-mark partial-answer rule is retained. No per-item price allocation is inferred.'
  cards.append(c)
 blocks=roman_blocks(page_text(S,5).split('Language awareness')[0]);asks=roman_blocks(page_text(Q,7,(300,30,580,793)).split('Language awareness')[0]);assert len(blocks)==len(asks)==3
 for (roman,block),(qr,q),count,expected,first in zip(blocks,asks,[1,6,3],[3,20,8],['Russian-language','New Year','129 euro']):
  assert roman==qr
  question=question_text(q);cue,rest=source_split(block,first);assert score(bag(question),bag(cue))>.7
  price=re.search(r'(\d+) marks',rest);assert int(price.group(1))==count*2
  answers=pool(rest[:price.start()]);assert len(answers)==expected,(roman,answers)
  c=as_points(base('IR2',question,count*2,[6,7],[5],roman=roman),answers,count,steps=[0,1,2]);written_guidance(c,general)
  if roman=='ii':
   c['rubric']['taskRequirements'].append('one mark: hotel')
   c['rubric']['markingGuideNote']+=' Hotel alone is one partial detail, counted once within the six-detail quota. The scheme does not attach this note exclusively to either the named venue or the separate comfortable/stylish description.'
  cards.append(c)
 blocks=numbered_blocks(page_text(S,8));assert len(blocks)==8
 counts=[2,2,1,2,2,1,5,5];pools=[6,8,5,5,3,4,20,14]
 firsts=['name/ Lena','name/ Alexander','lives in Lugansk','works in university','works in TV','father’s parents','gets up early','student +']
 for (item,roman,block),count,expected,first in zip(blocks,counts,pools,firsts):
  b=next(b for b in P.blocks if b.unit=='CD' and b.side=='R' and b.item==item and (not roman or b.text.startswith(roman+'.')))
  question=re.sub(r'^[iv]+\.\s*','',b.text);cue,rest=source_split(block,first);assert score(bag(question),bag(cue))>.7
  price=re.search(r'(\d+) marks',rest);assert int(price.group(1))==count*2
  answers=pool(rest[:price.start()]);assert len(answers)==expected,(item,roman,answers)
  partials={0:['teaches in Institute']} if (item,roman)==(2,'i') else {2:['has a son']} if (item,roman)==(2,'ii') else None
  c=as_points(base('CD',question,count*2,[10,11,12],[8],item,roman),answers,count,partials,steps=[0,1,2]);written_guidance(c,'Allocate 2 marks for each correct idea/concept (each idea/concept separated by +) and 1 mark for a partially correct idea/concept [unless otherwise stated].')
  c['review']['questionPages']=[b.page+1];cards.append(c)
 assert len(cards)==18 and sum(c['totalMarks'] for c in cards)==95
 return cards

def language_and_matching(docs):
 S,Q,cards=docs['scheme'],docs['paper'],[]
 question='In the AVOR advertisement '+squash(between(page_text(Q,7,(300,550,580,793)),'In the AVOR advertisement')).split('A masculine word')[0].strip()
 names=['A masculine word','A feminine word','A neuter word','A plural word','A verb']
 c=writing_card(base('LA2',question,5,[6,7],[5]),['Award one marks for each correct answer'],[criterion(f'word-{n}',name,1,[0,1],[]) for n,name in enumerate(names,1)],'Find one example of each category in the original AVOR advertisement. The scheme supplies no closed answer list.');cards.append(c)
 question='Match the following sections/links '+squash(between(page_text(Q,8,(280,30,580,125)),'Match the following sections/links'))
 table=S[5].find_tables().tables[0].extract();assert len(table)==10
 accepted=[re.split(r'\s+(?=\d\s*/)',squash(r[0]).split('half marks:')[0].strip()) for r in table]
 assert [len(a) for a in accepted]==[1,1,1,1,1,1,2,1,2,1]
 answers=[a[0] for a in accepted]
 c=as_points(base('MM',question,40,[8],[6]),answers,10,labels=[squash(r[1]) for r in table])
 for g in c['rubric']['groups']:g['rows'][0]['marks']=4
 for g,alternatives in zip(c['rubric']['groups'],accepted):
  for n,answer in enumerate(alternatives[1:],1):g['rows'].append({'id':f'alternative-{n}','text':answer,'marks':4})
 c['rubric']['groups'][5]['rows'].append({'id':'partial','text':'6 / история','marks':2})
 c['rubric']['taskRequirements']=['Assign FOUR marks per correct answer'];c['rubric']['markingGuideNote']='The museum headline accepts 2 / выставки for 4 marks or 6 / история for 2. The eco-houses and Buddhist-new-year headlines each retain both printed full-credit alternatives.';cards.append(c)
 question='Complete the interview '+squash(between(page_text(Q,9,(300,30,580,125)),'Complete the interview'))+'\n\n'+'Focail'+between(page_text(Q,9),'Focail')
 c=as_points(base('SD',question,20,[9],[7]),['Когда','Почему','Как (/когда)','Куда','Кто','Сколько','какие','Как','Где','какую'],10,{0:['Сколько'],3:['Где'],8:['Куда']})
 c['rubric']['taskRequirements']=['TWO marks per correct answer'];c['rubric']['markingGuideNote']='Complete all ten gaps. The source gives one-mark alternatives Сколько for gap 1, Где for gap 4 and Куда for gap 9. Gap 3 accepts Как or когда.';cards.append(c)
 return cards

def writing(docs):
 S,Q,cards=docs['scheme'],docs['paper'],[]
 question=question_text('Write 3'+between(page_text(Q,13,(300,30,580,410)),'Write 3'))
 source=page_text(S,9);content=squash(between(source,'Content of each answer','Textual coherence')).removeprefix('12 ').strip()
 coherence=between(source,'Textual coherence');bands=[{'label':n,'marks':[int(n)],'guidance':[squash(t)]} for n,t in re.findall(r'^\s*([0-3])\s+(.+?)(?=^\s*[0-3]\s|\Z)',coherence,re.M|re.S) if not squash(t).startswith('Allocate')];assert len(bands)==4
 c=writing_card(base('SA',question,30,[13],[9]),['Write 3-5 sentences on TWO of the following topics in Russian or English. Each answer should contain three factual details. Marks are awarded for relevant content and textual coherence.','The quality of the English/Russian will only be an assessment factor insofar as it impedes communication.'],[criterion(f'{choice}-content',f'{label}: content',12,list(range(0,13,2)),[content]) if part=='content' else criterion(f'{choice}-coherence',f'{label}: textual coherence',3,[0,1,2,3],[],bands) for choice,label in [('first','First chosen topic'),('second','Second chosen topic')] for part in ['content','coherence']]);cards.append(c)
 question='Write 6'+between(page_text(Q,14,(300,30,580,560)),'Write 6')
 table=S[9].find_tables().tables[0].extract();full=[{'label':squash(r[0]),'marks':mark_range(squash(r[0])),'guidance':[squash(r[1])]} for r in table[1:]]
 coherence=between(page_text(S,11),'Allocate 6 marks for textual coherence:');bands=[{'label':n,'marks':mark_range(n),'guidance':[squash(t)]} for n,t in re.findall(r'^\s*(\d(?:-\d)?)\s+(.+?)(?=^\s*\d(?:-\d)?\s|\Z)',coherence,re.M|re.S)];assert len(bands)==5
 c=writing_card(base('EW',question,30,[14],[10,11]),['Write 6-10 sentences on one of the following topics IN RUSSIAN.','No marks are awarded for additional information/content.'],[criterion('content','Communication + content',12,list(range(0,13,2)),['2 points for content details up to maximum of 12']),criterion('expression','Language + expression',12,list(range(13)),[],full),criterion('coherence','Textual coherence',6,list(range(7)),[],bands)]);cards.append(c)
 return cards

def listening(docs):
 S,A,cards=docs['scheme'],docs['aural'],[]
 general=bullets(between(page_text(S,12),'General:','Award FIVE'))+['Award FIVE marks for each correct/relevant point.'];assert len(general)==6
 counts=[[1]*5,[1,1,1,2],[1]*5,[1]*5]
 pools=[[1,1,1,9,12],[1,1,1,7],[1,6,6,4,1],[1,1,1,5,1]]
 firsts=[['d.','d.','Estonia','First name:','Several million'],['b.','d.','c.','Limited parking'],['She started','Musical family','7 years','RTE','d.'],['b.','c.','a.','Evening Jazz','a.']]
 topics=[['russian-0-5','russian-0-7','russian-0-2','russian-0-7','russian-2-5'],['russian-0-7','russian-0-5','russian-0-2','russian-0-8'],['russian-0-7','russian-0-1','russian-0-3','russian-0-4','russian-0-5'],['russian-0-7','russian-0-3','russian-0-7','russian-0-3','russian-0-4']]
 audio=next(r['source'] for r in json.loads((ROOT/'data/russianAudio.json').read_text()) if r['year']==2012)
 for section in range(1,5):
  blocks=numbered_blocks(page_text(S,section+11));asks=numbered_blocks(page_text(A,section+1,(300,30,580,793)));assert len(blocks)==len(asks)==len(counts[section-1]),(section,blocks,asks)
  for n,((item,roman,b),(qi,qr,q),count,expected,first) in enumerate(zip(blocks,asks,counts[section-1],pools[section-1],firsts[section-1])):
   assert (item,roman)==(qi,qr)
   question=question_text(q);cue,rest=source_split(b,first);assert score(bag(question.split(' a. ')[0]),bag(cue))>.6,(question,cue)
   partial=None
   if 'Award 3 marks:' in rest:rest,partial=rest.split('Award 3 marks:');partial=squash(partial)
   answers=pool(rest);assert len(answers)==expected,(section,item,roman,answers)
   c=as_points(base(f'L{section}',question,count*5,[section+1],[section+11],item,roman),answers,count)
   for g in c['rubric']['groups']:g['rows'][0]['marks']=5
   if partial:c['rubric']['groups'].append({'id':'partial','label':'Published partial answer','answerCount':1,'rows':[{'id':'music','text':partial,'marks':3}]})
   c['rubric']['taskRequirements']=general;c['review']['guidancePages']=[12]
   c['topicId']=topics[section-1][n];c['additionalTopicIds']=['russian-1-0']
   c['sourceMaterial']['kind']='source-question';c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.';c['audioMaterial']=audio;cards.append(c)
 assert len(cards)==19 and sum(c['totalMarks'] for c in cards)==100
 return cards

def build():
 docs=opened_sources();cards=reading(docs,RuPaper(2012,'ol'))+language_and_matching(docs)+writing(docs)+listening(docs)
 assert len(cards)==42 and sum(c['totalMarks'] for c in cards)==320
 old={c['id'] for c in json.loads((ROOT/'scripts/markbank/authored/russian.json').read_text())};assert not any(c['id'] in old for c in cards)
 return cards

if __name__=='__main__':save_reviewed(build())
