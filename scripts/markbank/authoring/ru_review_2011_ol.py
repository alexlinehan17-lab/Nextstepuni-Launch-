#!/usr/bin/env python3
"""2011 Ordinary Russian: independent 26-written/16-listening source census."""
import hashlib
import json
import re
import fitz
from ru_paper import bag, score
from ru_review_2026_hl import ROOT, squash, between, as_points, mark_range, save_reviewed, bullets
from ru_review_2013_ol import base as previous_base, pool
from ru_review_2015_ol import page_text as extract_page, question_text, source_split
from ru_review_2012_ol import writing_card
from ru_review_2018_ol import criterion

FILES={
 'paper':('papers/2011-ol-000-paper.pdf','66f722cae32f9fe493d4b0c6fc5c3ace6127e75d0ea70e588f14bd3af9c338b7'),
 'aural':('papers/2011-ol-A00-paper.pdf','714fb158cd3dbeeb8c556fb529881376db8154a1c6615ad8a3c8a4f4da8bb8ed'),
 'scheme':('schemes/2011-ol.pdf','e4160e18369177d720c75bfba145a13289b352affa583db0881a37b058df1716'),
}

def opened_sources():
 docs={}
 for key,(relative,digest) in FILES.items():
  path=ROOT/'examiner-reports/russian'/relative
  assert hashlib.sha256(path.read_bytes()).hexdigest()==digest
  docs[key]=fitz.open(path)
 return docs

def page_text(doc,page,box=None):
 # Letter-size scheme: final CD answer ends at731.4; first footer starts733.3.
 return extract_page(doc,page,box or ((20,30,592,732) if '/schemes/' in doc.name else (20,30,580,793)))

def base(unit,text,total,pages,scheme_pages,item=None,roman=None):
 c=previous_base(unit,text,total,pages,scheme_pages,item,roman)
 c['id']=c['id'].replace('2013','2011');c['year']=2011
 c['questionRef']=c['questionRef'].replace('2013','2011')
 c['sourceMaterial']['title']=c['sourceMaterial']['title'].replace('2013','2011')
 return c

def roman_blocks(text):
 heads=list(re.finditer(r'^\s*(ix|viii|vii|vi|iv|v|i{1,3})(?:\.\s*|\s+)(?=[A-Z])',text,re.M|re.I))
 return [(h.group(1).lower(),text[h.end():heads[n+1].start() if n+1<len(heads) else len(text)]) for n,h in enumerate(heads)]

def numbered_blocks(text):
 heads=list(re.finditer(r'^\s*(\d)\.\s*(?:(iv|i{1,3})\.?\s*)?(?=[A-Z])',text,re.M))
 return [(int(h.group(1)),h.group(2),text[h.end():heads[n+1].start() if n+1<len(heads) else len(text)]) for n,h in enumerate(heads)]

def written_guidance(c,general):
 c['review']['guidancePages']=[3]
 requirements=[general,'Do not penalise answers supplied in Russian.','Where a candidate uses the same information in response to two or more questions, accept the first answer only.']
 note='Answer in English or Irish. The scheme explicitly accepts Russian answers. Do not claim the same information again in another question.'
 if 'rubric' in c:c['rubric']['taskRequirements']=requirements;c['rubric']['markingGuideNote']=note
 else:c['rows'][0]['contextNote']=' '.join(requirements)+' '+note
 return c

def reading(docs):
 S,Q,cards=docs['scheme'],docs['paper'],[]
 general='Allocate 2 marks '+squash(between(page_text(S,4),'Allocate 2 marks','i. When'))
 for unit,sp,pages,askpages,counts,expected,firsts in [
  ('IR1',4,[2,3,4],[3,4],[None,1,1,2,2,2,1,2,1],[6,4,1,6,6,5,2,4,1],['20.00','the banks','press conference','Drum master','Austria +','car +','comfortable','fast food','bracelet-visa']),
  ('IR2',5,[6,7],[7],[2,2,2,5],[7,7,9,9],['Open sea','Water tourism','Group excursions','European cuisine'])]:
  blocks=roman_blocks(page_text(S,sp).split('Language awareness')[0]);asks=[]
  for p in askpages:asks.extend((r,question_text(q),p) for r,q in roman_blocks(page_text(Q,p,(295,30,580,793)).split('Language awareness')[0]))
  assert len(blocks)==len(asks)==len(counts),(unit,blocks,asks)
  for (roman,b),(qr,question,qp),count,n,first in zip(blocks,asks,counts,expected,firsts):
   assert roman==qr
   cue,rest=source_split(b,first);assert score(bag(question),bag(cue))>.65,(question,cue)
   price=re.search(r'(\d+)\s*marks',b);assert price
   total=int(price.group(1));assert total==(count*2 if count else 6)
   answers=pool(re.sub(r'\d+\s*marks','',rest));assert len(answers)==n,(unit,roman,answers)
   c=base(unit,question,total,pages,[sp],roman=roman)
   if count:c=as_points(c,answers,count,steps=[0,1,2])
   else:
    c['kind']='question';c['tariffModel']={'kind':'questionTotal'}
    c['rows']=[{'id':f'detail-{i}','kind':'point','verbatim':answer,'marks':None} for i,answer in enumerate(answers,1)]
   written_guidance(c,general);c['review']['questionPages']=[qp]
   if not count:c['rows'][0]['contextNote']+=' Source allocation conflict: the scheme gives 6 marks for this question but prints six plus-separated start/end time, date and year entries under its general 2-marks-per-concept rule. All six entries and the published total are retained. No one-mark allocation or choose-three rule is inferred; numeric self-scoring is unavailable for this task.'
   cards.append(c)
 source=page_text(S,8);blocks=numbered_blocks(source)
 asks=numbered_blocks(page_text(Q,13,(295,30,580,793)))+numbered_blocks(page_text(Q,14,(295,30,580,793)))
 counts=[2,3,3,2,2,3,3,2];sizes=[3,7,8,8,3,8,9,5]
 firsts=['typical English','tiger +','after publication','David Heyman','Alan Radcliff and producer','Next day','Later Daniel','six films']
 assert len(blocks)==len(asks)==8,(blocks,asks)
 for (item,roman,b),(qi,qr,q),count,n,first in zip(blocks,asks,counts,sizes,firsts):
  assert item==qi and (roman==qr or (item,roman,qr)==(2,'i',None))
  question=question_text(q);cue,rest=source_split(b,first);assert score(bag(question),bag(cue))>.65,(question,cue)
  if 'one point for:' in rest:rest,partial=rest.split('one point for:');assert squash(partial)=='TV'
  answers=pool(rest);assert len(answers)==n,(item,roman,answers)
  c=as_points(base('CD',question,count*2,[12,13,14],[8],item,qr),answers,count,{2:['TV']} if item==1 and roman=='i' else None,steps=[0,1,2])
  written_guidance(c,'Allocate 2 marks for each correct idea/concept (each idea/concept separated by +) and 1 mark for a partially correct idea/concept [unless otherwise stated].')
  c['review']['questionPages']=[13 if item<3 else 14]
  if item==1 and roman=='i':c['rubric']['markingGuideNote']+=' The source passage places the mother’s casting work in television. The published one-point TV partial is kept with that family detail so it cannot be claimed in addition to the full answer.'
  if item==2:c['rubric']['markingGuideNote']+=' The booklet labels this question 2; the scheme labels it 2.i. The card follows the booklet.'
  cards.append(c)
 assert len(cards)==21 and sum(c['totalMarks'] for c in cards)==92
 return cards

def language_and_matching(docs):
 S,Q,cards=docs['scheme'],docs['paper'],[]
 question='In the text '+squash(between(page_text(Q,7,(295,30,580,793)),'In the text','A masculine word'))
 c=writing_card(base('LA2',question,8,[6,7],[5]),['Award two marks for each correct answer'],[criterion(f'word-{n}',label,2,[0,2],[]) for n,label in enumerate(['A masculine word','A feminine word','A plural word','A verb'],1)],'Find one example of each category in the original text. The scheme supplies no closed answer list or category-specific partial tariff.');cards.append(c)
 question='Match the following headings '+squash(between(page_text(Q,8,(295,30,580,140)),'Match the following headings'))
 table=S[5].find_tables().tables[0].extract();assert len(table)==10
 c=as_points(base('MM',question,40,[8,9],[6]),[squash(a)+' — '+squash(b) for a,b in table],10)
 for g in c['rubric']['groups']:g['rows'][0]['marks']=4
 c['rubric']['taskRequirements']=['FOUR marks per correct answer'];cards.append(c)
 question='Complete the interview '+squash(between(page_text(Q,10,(295,30,580,130)),'Complete the interview'))+'\n\nFocail'+between(page_text(Q,10),'Focail')+'\n\n'+page_text(Q,11)
 c=as_points(base('SD',question,20,[10,11],[7]),['как','кто','что','где','когда','сколько','где','какие','сколько','почему'],10)
 c['rubric']['taskRequirements']=['TWO marks per correct answer'];c['rubric']['markingGuideNote']='Complete all ten gaps across both pages. The concert question contains two gaps: где and когда in the printed scheme order.';cards.append(c)
 return cards

def writing(docs):
 S,Q,cards=docs['scheme'],docs['paper'],[]
 question=question_text('Write 3'+between(page_text(Q,16,(290,30,580,390)),'Write 3'))
 source=page_text(S,9);content=squash(between(source,'Content of each answer','Textual coherence')).removeprefix('12 ').strip()
 coherence=between(source,'Textual coherence');bands=[{'label':n,'marks':[int(n)],'guidance':[squash(t)]} for n,t in re.findall(r'^\s*([0-3])\s+(.+?)(?=^\s*[0-3]\s|\Z)',coherence,re.M|re.S) if not squash(t).startswith('Allocate')];assert len(bands)==4
 c=writing_card(base('SA',question,30,[16],[9]),['Write 3-5 sentences on TWO of the following topics in Russian or English. Each answer should contain three FACTUAL details. Marks are awarded for relevant content and textual coherence.','The quality of the English/Russian will only be an assessment factor insofar as it impedes communication.'],[criterion(f'{choice}-content',f'{label}: content',12,list(range(0,13,2)),[content]) if part=='content' else criterion(f'{choice}-coherence',f'{label}: textual coherence',3,[0,1,2,3],[],bands) for choice,label in [('first','First chosen topic'),('second','Second chosen topic')] for part in ['content','coherence']]);cards.append(c)
 question=question_text('Write 6'+between(page_text(Q,17,(295,30,580,793)),'Write 6')).replace('\uf0b7','•')
 table=S[10].find_tables().tables[0].extract();full=[{'label':squash(r[0]),'marks':mark_range(squash(r[0])),'guidance':[squash(r[1])]} for r in table[1:]]
 coherence=between(page_text(S,11),'Allocate 6 marks for textual coherence:');bands=[{'label':n,'marks':mark_range(n),'guidance':[squash(t)]} for n,t in re.findall(r'^\s*(\d(?:-\d)?)\s+(.+?)(?=^\s*\d(?:-\d)?\s|\Z)',coherence,re.M|re.S)];assert len(bands)==5
 c=writing_card(base('EW',question,30,[17],[10,11]),['Write 6-10 sentences on one of the following topics IN RUSSIAN.','No marks are awarded for additional information/content.'],[criterion('content','Communication + content',12,list(range(0,13,2)),['2 points for content details up to maximum of 12']),criterion('expression','Language + expression',12,list(range(13)),[],full),criterion('coherence','Textual coherence',6,list(range(7)),[],bands)]);cards.append(c)
 return cards

def listening(docs):
 S,A,cards=docs['scheme'],docs['aural'],[]
 general=bullets(between(page_text(S,12),'General:','Award five'))+['Award five marks for each correct/relevant point.'];assert len(general)==6
 counts=[[1,2,1,1],[1]*5,[1,2,2],[2,1,1,1]]
 sizes=[[1,3,1,1],[1,5,1,3,10],[8,9,8],[3,9,1,1]]
 firsts=[['b)','Visit Louvre','b)','d)'],['a)','Russian students','c)','Bono','Good cuisine'],['Situated','5 times','Sports activities'],['17th','Started','b)','b)']]
 topics=[['russian-0-7','russian-0-8','russian-0-7','russian-2-3'],['russian-0-3','russian-0-3','russian-0-2','russian-2-3','russian-2-3'],['russian-0-5','russian-2-2','russian-0-5'],['russian-0-7','russian-0-5','russian-0-7','russian-0-6']]
 audio=next(r['source'] for r in json.loads((ROOT/'data/russianAudio.json').read_text()) if r['year']==2011)
 for section in range(1,5):
  blocks=numbered_blocks(page_text(S,section+11));asks=numbered_blocks(page_text(A,section+1,(295,30,580,793)));assert len(blocks)==len(asks)==len(counts[section-1]),(section,blocks,asks)
  for n,((item,roman,b),(qi,qr,q),count,expected,first) in enumerate(zip(blocks,asks,counts[section-1],sizes[section-1],firsts[section-1])):
   assert (item,roman)==(qi,qr)
   question=question_text(q);cue,rest=source_split(b,first);assert score(bag(question.split(' a) ')[0]),bag(cue))>.6,(question,cue)
   answers=pool(rest);assert len(answers)==expected,(section,item,roman,answers)
   c=as_points(base(f'L{section}',question,count*5,[section+1],[section+11],item,roman),answers,count)
   for g in c['rubric']['groups']:g['rows'][0]['marks']=5
   c['rubric']['taskRequirements']=general;c['review']['guidancePages']=[12]
   c['topicId']=topics[section-1][n];c['additionalTopicIds']=['russian-1-0']
   if section==4 and item==1:c['rubric']['markingGuideNote']='The question asks “when and where” and requests two details. The scheme prints 17th of May, 1992 and Moscow as three plus-separated details. All three are retained under the two-detail quota; no separate one-date/one-place restriction is printed.'
   c['sourceMaterial']['kind']='source-question';c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.';c['audioMaterial']=audio;cards.append(c)
 assert len(cards)==16 and sum(c['totalMarks'] for c in cards)==100
 return cards

def build():
 docs=opened_sources();cards=reading(docs)+language_and_matching(docs)+writing(docs)+listening(docs)
 assert len(cards)==42 and sum(c['totalMarks'] for c in cards)==320
 old={c['id'] for c in json.loads((ROOT/'scripts/markbank/authored/russian.json').read_text())};assert not any(c['id'] in old for c in cards)
 return cards

if __name__=='__main__':save_reviewed(build())
