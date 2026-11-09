#!/usr/bin/env python3
"""2010 Ordinary Russian: independent 24-written/18-listening source census."""
import hashlib
import json
import re
import fitz
from ru_paper import bag, score
from ru_review_2026_hl import ROOT, squash, between, as_points, mark_range, save_reviewed
from ru_review_2013_ol import base as previous_base, pool
from ru_review_2015_ol import page_text, question_text, source_split
from ru_review_2011_ol import roman_blocks, numbered_blocks, written_guidance
from ru_review_2012_ol import writing_card
from ru_review_2018_ol import criterion
from ru_source_text import open_scheme

FILES={
 'paper':('papers/2010-ol-000-paper.pdf','8a4c29e76ab591c9d406b8cb3fcd57f57cbf7f4b178e32ea6c26614f1ac5502d'),
 'aural':('papers/2010-ol-A00-paper.pdf','0fb3329b722ebca3bcd74cd30fac7df55ed2b5ba7ab4d267d19a2af60f021844'),
 'scheme':('schemes/2010-ol.pdf','a9fa632484624a15aab956313b463260948d60ae1deaeb4f6344ef4dff2da67e'),
}

def opened_sources():
 docs={}
 for key,(relative,digest) in FILES.items():
  path=ROOT/'examiner-reports/russian'/relative
  assert hashlib.sha256(path.read_bytes()).hexdigest()==digest
  docs[key]=open_scheme(2010,'ol') if key=='scheme' else fitz.open(path)
 return docs

def base(unit,text,total,pages,scheme_pages,item=None,roman=None):
 c=previous_base(unit,text,total,pages,scheme_pages,item,roman)
 c['id']=c['id'].replace('2013','2010');c['year']=2010
 c['questionRef']=c['questionRef'].replace('2013','2010')
 c['sourceMaterial']['title']=c['sourceMaterial']['title'].replace('2013','2010')
 return c

def club_blocks(text):
 heads=list(re.finditer(r'^\s*(iv|iii|ii|i)(?:\.(?:([abc])\.)?|\s+)\s*',text,re.M))
 return [(h.group(1),h.group(2),text[h.end():heads[n+1].start() if n+1<len(heads) else len(text)]) for n,h in enumerate(heads)]

def reading(docs):
 S,Q,cards=docs['scheme'],docs['paper'],[]
 source=page_text(S,4).split('Language awareness')[0]
 general='Allocate 2 marks '+squash(between(source,'Allocate 2 marks','i. Give'))
 blocks=roman_blocks(source);asks=[]
 for p in [3,4]:asks.extend((r,question_text(q),p) for r,q in roman_blocks(page_text(Q,p,(300,30,580,793)).split('Language awareness')[0]))
 assert len(blocks)==len(asks)==7
 for (roman,b),(qr,question,qp),count,n,first in zip(blocks,asks,[2,2,2,2,2,1,2],[4,9,9,10,7,4,7],['10km','beautiful','dining room','3-5 bed','hot/cold','3 times','500m']):
  assert roman==qr
  cue,rest=source_split(b,first);assert score(bag(question),bag(cue))>.65,(question,cue)
  price=re.search(r'(\d+) marks',cue);assert price and int(price.group(1))==count*2
  answers=pool(rest);assert len(answers)==n,(roman,answers)
  c=as_points(base('IR1',question,count*2,[2,3,4],[4],roman=roman),answers,count,steps=[0,1,2]);written_guidance(c,general);c['review']['questionPages']=[qp];cards.append(c)
 blocks=club_blocks(page_text(S,5).split('Language awareness')[0]);asks=club_blocks(page_text(Q,7,(300,30,580,695)))
 assert [(r,a) for r,a,_ in blocks]==[(r,a) for r,a,_ in asks]==[('i',None),('ii','a'),('ii','b'),('ii','c'),('iii',None),('iv',None)]
 for (roman,letter,b),(_,_,q) in zip(blocks,asks):
  question=squash(q) if roman=='i' else squash(re.sub(r'_+','',q)) if roman=='iii' else question_text(q)
  if roman=='i':answers=['club','Moscow','Europe'];count=3
  elif roman=='ii':answers=[{'a':'2000 people','b':'3000 people','c':'10,000 people'}[letter]];count=1
  elif roman=='iv':answers=pool(b.split('Give two details.')[1]);count=2
  else:answers=[];count=5
  c=as_points(base('IR2',question,count*2,[6,7],[5],roman=roman),answers,count,steps=[0,1,2])
  if letter:c['id']+='-'+letter;c['questionRef']+='('+letter+')'
  if roman=='i':
   for g,label in zip(c['rubric']['groups'],['Type of venue','City','Wider region']):g['label']=label
  if roman=='iii':
   heads=list(re.finditer(r'(First|Second|Third|Fourth|Fifth) floor:\s*',b));assert len(heads)==5
   groups=[]
   for n,h in enumerate(heads):
    options=pool(b[h.end():heads[n+1].start() if n+1<len(heads) else len(b)]);assert len(options)==[4,4,5,5,3][n]
    groups.append({'id':f'floor-{n+1}','label':h.group(1)+' floor','answerCount':1,'rows':[{'id':f'option-{i}','text':a,'marks':2,'steps':[0,1,2]} for i,a in enumerate(options,1)]})
   c['rubric']['groups']=groups
  written_guidance(c,general);c['review']['questionPages']=[7]
  if roman=='iii':c['rubric']['markingGuideNote']+=' Give one detail for each of the five named floors; several details from one floor cannot replace another floor.'
  cards.append(c)
 blocks=numbered_blocks(page_text(S,8));asks=numbered_blocks(page_text(Q,13,(300,30,580,793)))
 assert len(blocks)==len(asks)==5
 for (item,roman,b),(qi,qr,q),count,n,first in zip(blocks,asks,[2,3,5,5,5],[5,11,15,18,14],['to earn','began in','legal +','national park','worked as']):
  assert (item,roman)==(qi,qr)
  question=question_text(q);cue,rest=source_split(b,first);assert score(bag(question),bag(cue))>.65,(question,cue)
  answers=pool(rest);assert len(answers)==n,(item,answers)
  c=as_points(base('CD',question,count*2,[12,13],[8],item,roman),answers,count,steps=[0,1,2]);written_guidance(c,'Allocate 2 marks for each correct idea/concept (each idea/concept separated by +) and 1 mark for a partially correct idea/concept [unless otherwise stated].');c['review']['questionPages']=[13];cards.append(c)
 assert len(cards)==18 and sum(c['totalMarks'] for c in cards)==92
 return cards

def language_and_matching(docs):
 S,Q,cards=docs['scheme'],docs['paper'],[]
 question='In the Russian text '+squash(between(page_text(Q,4,(300,30,580,793)),'In the Russian text','A masculine word'))
 c=writing_card(base('LA1',question,4,[2,3,4],[4]),['ONE mark per correct answer. Do not penalise students who supply appropriate words in English.'],[criterion(f'word-{n}',label,1,[0,1],[]) for n,label in enumerate(['A masculine word','A feminine word','A neuter word','A verb'],1)],'Find one example of each category. The scheme explicitly accepts appropriate English words and supplies no closed answer list.');cards.append(c)
 question='Find four words '+squash(between(page_text(Q,7),'Find four words')).split('_')[0].strip()
 answers=[squash(a) for a in between(page_text(S,5),'Award ONE marks for each correct answer.').splitlines() if squash(a)];assert len(answers)==7
 c=as_points(base('LA2',question,4,[6,7],[5]),answers,4)
 for g in c['rubric']['groups']:g['rows'][0]['marks']=1
 c['rubric']['taskRequirements']=['Award ONE marks for each correct answer.'];cards.append(c)
 question='Match the following textbook covers '+squash(between(page_text(Q,8,(300,30,580,160)),'Match the following textbook covers'))
 source=page_text(S,6);heads=list(re.finditer(r'^\s*(\d{1,2})\s+(?=[А-Я])',source,re.M));assert len(heads)==10
 answers=[h.group(1)+' — '+squash(source[h.end():heads[n+1].start() if n+1<len(heads) else len(source)]) for n,h in enumerate(heads)]
 c=as_points(base('MM',question,40,[8,9],[6]),answers,10)
 for g in c['rubric']['groups']:g['rows'][0]['marks']=4
 c['rubric']['taskRequirements']=['FOUR marks per correct answer'];cards.append(c)
 question='Complete the interview '+squash(between(page_text(Q,10,(300,30,580,145)),'Complete the interview'))+'\n\nFocail'+between(page_text(Q,10),'Focail')
 c=as_points(base('SD',question,20,[10],[7]),['каком','чем','Какое','Почему','Как','Как','Кто','Когда','как','где'],10)
 c['rubric']['taskRequirements']=['TWO marks per correct answer'];c['rubric']['markingGuideNote']='Complete all ten gaps. Numbered exchange 6 contains two gaps, Как and Кто.';cards.append(c)
 return cards

def writing(docs):
 S,Q,cards=docs['scheme'],docs['paper'],[]
 question=question_text('Write 3'+between(page_text(Q,14,(300,30,580,793)),'Write 3'))
 source=page_text(S,9);content=squash(between(source,'Content of each answer','Textual coherence')).removeprefix('12 ').strip()
 coherence=between(source,'Textual coherence');bands=[{'label':n,'marks':[int(n)],'guidance':[squash(t)]} for n,t in re.findall(r'^\s*([0-3])\s+(.+?)(?=^\s*[0-3]\s|\Z)',coherence,re.M|re.S) if not squash(t).startswith('Allocate')];assert len(bands)==4
 c=writing_card(base('SA',question,30,[14],[9]),['Write 3-5 sentences on TWO of the following topics in Russian or English. Each answer should contain three FACTUAL details. Marks are awarded for relevant content and textual coherence.','The quality of the English/Russian will only be an assessment factor insofar as it impedes communication.'],[criterion(f'{choice}-content',f'{label}: content',12,list(range(0,13,2)),[content]) if part=='content' else criterion(f'{choice}-coherence',f'{label}: textual coherence',3,[0,1,2,3],[],bands) for choice,label in [('first','First chosen topic'),('second','Second chosen topic')] for part in ['content','coherence']]);cards.append(c)
 question=question_text('Write 6'+between(page_text(Q,15,(300,30,580,793)),'Write 6'))
 source=page_text(S,10);rule='ALL: '+squash(between(source,'ALL:','Allocate 6 marks for textual coherence:'))
 coherence=between(source,'Allocate 6 marks for textual coherence:');bands=[{'label':n,'marks':mark_range(n),'guidance':[squash(t)]} for n,t in re.findall(r'^\s*(\d(?:-\d)?)\s+(.+?)(?=^\s*\d(?:-\d)?\s|\Z)',coherence,re.M|re.S)];assert len(bands)==5
 c=writing_card(base('EW',question,30,[15],[10]),['Write 6-10 sentences on one of the following topics IN RUSSIAN.',rule], [criterion('content','Required function and information',12,list(range(13)),[rule]),criterion('expression','Manipulation of language',12,list(range(13)),[rule]),criterion('coherence','Textual coherence',6,list(range(7)),[],bands)],'The scheme prints 4 x 6 marks for each choice, with half of each available mark for the required function/information and half for language manipulation, plus 6 for coherence. These two 12-mark totals summarise that allocation; they do not create extra credit for additional material. No content/expression quality-band descriptors or a new four-slot mapping for the book review are supplied.');cards.append(c)
 return cards

def listening(docs):
 S,A,cards=docs['scheme'],docs['aural'],[]
 general=[squash(x) for x in re.split(r'^\s*x\s+',between(page_text(S,11),'General:','Award five'),flags=re.M)[1:]]+['Award five marks for each correct/relevant point.'];assert len(general)==6
 counts=[[1]*5,[1]*5,[1,2,1,1],[2,1,1,1]];sizes=[[1,6,1,1,4],[1]*5,[1,4,4,1],[6,1,5,5]]
 firsts=[['c)','President of','c)','a)','Buy an'],['b)','d)','a)','b)','a)'],['c)','Business rooms','football +','c)'],['Collection','c)','Name +','2 operators']]
 topics=[['russian-2-6','russian-2-8','russian-0-7','russian-0-7','russian-0-6'],['russian-0-4','russian-0-5','russian-0-8','russian-0-3','russian-0-6'],['russian-0-2','russian-0-5','russian-0-5','russian-0-9'],['russian-0-9']*4]
 audio=next(r['source'] for r in json.loads((ROOT/'data/russianAudio.json').read_text()) if r['year']==2010)
 for section in range(1,5):
  blocks=numbered_blocks(page_text(S,section+10));asks=numbered_blocks(page_text(A,section+1,(300,30,580,793)));assert len(blocks)==len(asks)==len(counts[section-1]),(section,blocks,asks)
  for n,((item,roman,b),(qi,qr,q),count,expected,first) in enumerate(zip(blocks,asks,counts[section-1],sizes[section-1],firsts[section-1])):
   assert (item,roman)==(qi,qr)
   question=question_text(q);cue,rest=source_split(b,first);assert score(bag(question.split(' a) ')[0]),bag(cue))>.6,(question,cue)
   partial=None
   if 'Assign 2 marks for:' in rest:rest,partial=rest.split('Assign 2 marks for:');partial=squash(partial);assert partial=='President'
   answers=pool(rest);assert len(answers)==expected,(section,item,roman,answers)
   c=as_points(base(f'L{section}',question,count*5,[section+1],[section+10],item,roman),answers,count)
   for i,g in enumerate(c['rubric']['groups'],1):
    g['rows'][0].update({'marks':5,'steps':[0,2.5,5]})
    g['label']=f'Answer {i} · Half credit only when the whole answer is in Russian'
   if partial:c['rubric']['groups'][0]['rows'].append({'id':'partial','text':partial,'marks':2,'steps':[0,1,2]})
   c['rubric']['taskRequirements']=general;c['review']['guidancePages']=[11]
   c['rubric']['markingGuideNote']='Use the half-credit step only when the entire answer is in Russian: 2.5 instead of 5 marks'+(', or 1 instead of 2 for the President-only partial' if partial else '')+'. Isolated Russian words or expressions do not reduce credit. The middle step is this language rule, not a general partial-content award.'
   c['topicId']=topics[section-1][n];c['additionalTopicIds']=['russian-1-0']
   c['sourceMaterial']['kind']='source-question';c['sourceMaterial']['presentationNote']='Listen to the official recording and answer the printed question. The transcript is not shown before answering.';c['audioMaterial']=audio;cards.append(c)
 assert len(cards)==18 and sum(c['totalMarks'] for c in cards)==100
 return cards

def build():
 docs=opened_sources();cards=reading(docs)+language_and_matching(docs)+writing(docs)+listening(docs)
 assert len(cards)==42 and sum(c['totalMarks'] for c in cards)==320
 old={c['id'] for c in json.loads((ROOT/'scripts/markbank/authored/russian.json').read_text())};assert not any(c['id'] in old for c in cards)
 return cards

if __name__=='__main__':save_reviewed(build())
