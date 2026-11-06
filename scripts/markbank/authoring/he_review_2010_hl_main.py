#!/usr/bin/env python3
"""Source-selected 2010 Higher Home Economics. Never infer unprinted tariffs."""
from pathlib import Path
from copy import deepcopy
import hashlib,json,re,sys
import fitz
from he_review_2023_hl import ROOT,tidy,criterion
PAPER='paper-trail-corpus/exampapers/2010/LC098ALP000EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2010/LC098ALP000EV.pdf'
HASHES={PAPER:'80a5625b3ef38cc0dbd0337e68dfe34dccba86bea005133aa0b7576ba3270df3',SCHEME:'c18db92c5e9645dd372a558edf73e71c524d3333d47cdca72bcf9b84c5e61bcb'}
REVIEW='scripts/markbank/authoring/home-economics/2010-hl-main-review.json'
WHOLE_NOTE='The scheme prints 6 marks for the complete question, with no per-answer allocation or partial-credit ladder. Check the complete response; no separate answer marks have been inferred.'

def documents():
 for path,expected in HASHES.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected,path
 return {k:fitz.open(ROOT/v) for k,v in [('paper',PAPER),('scheme',SCHEME)]}

def text(doc,n):return tidy(doc[n-1].get_text(clip=fitz.Rect(0,20,doc[n-1].rect.width,770),sort=True))
def select(s,start,end=None,include=False):
 assert s.count(start)==1,(start,s[:150]);t=s.split(start,1)[1]
 if end is not None:assert end in t,end;t=t.split(end,1)[0]
 return (start+t if include else t).strip()
def named(s,labels):
 out=[]
 for i,label in enumerate(labels):out.append(select(s,label,labels[i+1] if i+1<len(labels) else None,True))
 return out
def point(key,value,marks=None,note=''):
 d=dict(id=key,kind='point',verbatim=tidy(value),marks=marks)
 if note:d['contextNote']=note
 return d
def menu(key,label,count,per,options,note=''):
 assert count<=len(options)<=25,(key,count,len(options));return dict(id=key,kind='anyN',verbatim=label,marks=count*per,openList=True,group=dict(claimMax=count,perOption=per,options=options),contextNote=note)
def semis(s):return [t.strip() for t in re.sub(r'\s*etc\.?\s*$','',s).split(';') if t.strip()]
def card(key,section,ref,topic,prompt,stem,marks,rows,page,notation=None,**extra):
 c=dict(id='he-2010-hl-'+key,subjectId='home-economics',topicId='home-economics-'+topic,conceptId=key,level='higher',year=2010,section=section,questionRef='2010 HL Section '+section+' '+ref,questionText=prompt,stem=stem,figureKey='',labelKey=[],totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation or ''),rows=rows,sourceMaterial=dict(kind='source-question',label='OFFICIAL QUESTION',title='Source and question',pages=[page],attribution='SEC Home Economics 2010 Higher Level examination paper — © State Examinations Commission.',presentationNote='Open the original examination page to review this task in context.'))
 c.update(extra);return c

def a_regions(doc,pages):
 out={}
 for n in pages:
  p=doc[n-1];starts=sorted((int(w[4][:-1]),w[1]-3) for w in p.get_text('words') if re.fullmatch(r'\d+\.',w[4]) and 54<w[0]<60 and w[1]<760)
  for i,(number,top) in enumerate(starts):
   bottom=starts[i+1][1] if i+1<len(starts) else 770
   out[number]=dict(page=n,rect=[45,top,p.rect.width-35,bottom])
 assert list(out)==list(range(1,13)),out.keys()
 return out

def region(doc,r):return tidy(doc[r['page']-1].get_text(clip=fitz.Rect(r['rect']),sort=True))
def strip_number(s):return re.sub(r'^\d+\.\s*','',s)
def clean_question(s):return tidy(re.sub(r'\((?:i|ii|iii)\)|_{2,}|\(6\)','',strip_number(s)))
def a_build():
 d=documents();pr=a_regions(d['paper'],range(2,6));sr=a_regions(d['scheme'],range(4,7));p={n:region(d['paper'],r) for n,r in pr.items()};s={n:strip_number(region(d['scheme'],r)) for n,r in sr.items()};rows={}
 t=d['scheme'][3].find_tables().tables
 assert len(t)==2
 grid=t[0].extract();assert tidy(grid[1][2])=='Trypsin'
 rows[1]=[point(f'cell-{i}',tidy(grid[0][i])+' — '+tidy(grid[1][i])) for i in [2,3,4]]
 pairs=t[1].extract()[1];left,right=[v.splitlines() for v in pairs];assert len(left)==len(right)==10
 rows[2]=[point(f'pair-{i}',tidy(a)+' — '+tidy(b)) for i,(a,b) in enumerate(zip(left,right),1)]
 for n in [3,4,8,10,11]:
  body=select(s[n],'(6)');body=re.sub(r'\((?:i|ii|iii)\)\s*','; ',body).strip('; ')
  if n==10:body=body.replace(',',';')
  rows[n]=[point(f'answer-{i}',v) for i,v in enumerate(semis(body),1)]
 rows[5]=[point('lactic',select(s[5],'(i)','(ii)')),point('rennet',select(s[5],'(ii)'))]
 pastries=tidy(re.sub(r'\((?:i|ii)\)','',select(s[6],'(6)','State one difference')))
 rows[6]=[point(f'type-{i}',v.strip()) for i,v in enumerate(pastries.split(','),1)]+[point('comparison',select(s[6],'Accept differences',include=True))]
 table=d['scheme'][4].find_tables().tables[0].extract()
 rows[7]=[point(f'agent-{i}',tidy(a)+' — '+tidy(b)) for i,(a,b) in enumerate(table[1:],1)]
 rows[9]=[point('refrigerant',select(s[9],'Refrigerant','Condenser',True)),point('condenser',select(s[9],'Condenser',include=True))]
 first=select(s[12],'Packaging suppliers','(ii)',True).replace('Green Dot','').strip();second=select(s[12],'Products that',include=True).replace('Eco Label','').strip()
 rows[12]=[point('green-dot','Green Dot — '+first),point('eco-label','Eco Label — '+second)]
 topics={1:'0-5',2:'0-6',3:'0-8',4:'0-1',5:'0-9',6:'0-3',7:'0-11',8:'0-4',9:'1-3',10:'1-4',11:'1-2',12:'1-5'}
 out=[]
 for n in range(1,13):
  prompt=clean_question(p[n]);
  if n in [1,2,7]:prompt=clean_question(p[n].split('(6)',1)[0])
  if n==12:prompt=clean_question(p[n].split('(6)',1)[0])
  rows[n][0]['contextNote']=WHOLE_NOTE
  c=card(f'sa-q{n}','A',f'Q{n}',topics[n],prompt,'',6,rows[n],pr[n]['page'],tariffModel=dict(kind='questionTotal'))
  if n in [1,2,7,12]:c.update(questionFigureKey=f'home-economics-2010-hl-sa-q{n}',questionFigureIncludesPrompt=True)
  if n==11:c['rows'][0]['contextNote']+=' This is the historical legislation named in the 2010 paper.'
  out.append(c)
 return out

def write_section(section,cards,review):
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text());ids={c['id'] for c in cards};before=[c for c in data if c['id'] not in ids]
 assert len(ids)==len(cards)
 p.write_text(json.dumps(before+cards,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW
 r=json.loads(p.read_text()) if p.exists() else dict(schemaVersion=1,year=2010,level='higher',sitting='main',language='ev',status='source-review-in-progress',sources={k:dict(sha256=v,pages=12 if k==PAPER else 33) for k,v in HASHES.items()},visualSweep=dict(paper='All twelve pages reviewed: cover/instructions1; SectionA2–5; B6–8; C9–11; blank12.',scheme='All thirty-three pages reviewed: cover1,blank2,guidance3,A4–6,B7–12,C13–19,blank20,separate coursework21–32,backcover33.'),expectedTasks=50,expectedSectionTasks=dict(A=12,B=18,C=20),sourceQuestionGroups=20,offeredPracticeMarks=627,tasks=[])
 r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],section=section,marks=c['totalMarks'],questionRef=c['questionRef'],topicId=c['topicId']) for c in cards];r['section'+section+'Review']=review
 p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')

def transcript():
 d=documents()['scheme'];(ROOT/'examiner-reports/home-economics/schemes/2010-hl.md').write_text(('# SEC Home Economics 2010 Higher marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+p.get_text(sort=True) for i,p in enumerate(d))).rstrip()+'\n')

if __name__=='__main__':
 cards=a_build();assert len(cards)==12 and sum(c['totalMarks'] for c in cards)==72
 if '--write' in sys.argv:
  transcript();write_section('A',cards,dict(tasks=12,marks=72,tariffDecision='Whole-question six-mark tariffs only; all answer rows unpriced. No inferred partial ladder or per-item value.',selectionDecisions='Each printed question is one card: A2 three property/use pairs, A6 two pastry names plus dependent comparison, A7 two of three named agents. Full source options retained without fan-out.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
