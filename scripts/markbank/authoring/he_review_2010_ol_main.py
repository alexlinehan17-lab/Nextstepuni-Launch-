#!/usr/bin/env python3
"""2010 Ordinary source selections, anchored to an independent full-page census."""
from pathlib import Path
from copy import deepcopy
import hashlib,json,re,sys
import fitz
from he_review_2010_hl_main import ROOT,tidy,criterion,select,named,point,menu,semis,region
from he_review_2010_hl_main import a_regions as higher_a_regions
from he_review_2010_hl_main import card as higher_card
PAPER='paper-trail-corpus/exampapers/2010/LC098GLP000EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2010/LC098GLP000EV.pdf'
HASHES={PAPER:'2d1345c5b86465c9cc40c45d04d141bd3bd9c7c3b02e0f0ca31dfb832b79bfdd',SCHEME:'bcd30296678dc76bcccd09b70d783d3e295721e6d7e60192e11c156c79808200'}
REVIEW='scripts/markbank/authoring/home-economics/2010-ol-main-review.json'
def documents():
 for p,h in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 return {k:fitz.open(ROOT/p) for k,p in [('paper',PAPER),('scheme',SCHEME)]}
def body_bottom(page):
 footers=[]
 for block in page.get_text('dict')['blocks']:
  for line in block.get('lines',[]):
   label=tidy(''.join(span['text'] for span in line['spans']))
   if line['bbox'][1]>770 and re.fullmatch(r'(?:\d{1,2}|Page \d+ of \d+)',label):footers.append(line['bbox'][1]-2)
 return min([790]+footers)
def text(doc,n):return tidy(doc[n-1].get_text(clip=fitz.Rect(0,20,doc[n-1].rect.width,body_bottom(doc[n-1])),sort=True))
def a_regions(doc,pages):
 regions=higher_a_regions(doc,pages)
 for r in regions.values():
  if r['rect'][3]==770:r['rect'][3]=body_bottom(doc[r['page']-1])
 return regions
def clean(s):return tidy(re.sub(r'_{2,}|\((?:i|ii|iii|iv)\)|\(6\)','',s))
def without_number(s):return re.sub(r'^\d+\.\s*','',s)
def examples(s):return re.sub(r'^e\.g\.\s*','',re.sub(r'\s*etc\.?\s*$','',s)).strip()
def chosen(s,words):
 return [select(s,w,include=True)[:len(w)] for w in words]
def card(key,section,ref,topic,prompt,stem,marks,rows,page,notation,**extra):
 c=higher_card(key,section,ref,topic,prompt,stem,marks,rows,page,notation,**extra)
 c.update(id='he-2010-ol-'+key,level='ordinary',questionRef='2010 OL Section '+section+' '+ref)
 c['sourceMaterial']['attribution']='SEC Home Economics 2010 Ordinary Level examination paper — © State Examinations Commission.'
 return c
def write_section(section,cards,review):
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text());ids={c['id'] for c in cards};assert len(ids)==len(cards)
 p.write_text(json.dumps([c for c in data if c['id'] not in ids]+cards,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text())
 if r['status']=='independent-source-census-complete-authoring-pending':r['status']='source-review-in-progress'
 r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],section=section,marks=c['totalMarks'],questionRef=c['questionRef'],topicId=c['topicId']) for c in cards];r['section'+section+'Review']=review;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
def transcript():
 d=documents()['scheme'];(ROOT/'examiner-reports/home-economics/schemes/2010-ol.md').write_text(('# SEC Home Economics 2010 Ordinary marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+p.get_text(sort=True) for i,p in enumerate(d))).rstrip()+'\n')
def a_build():
 d=documents();pr=a_regions(d['paper'],range(2,6));sr=a_regions(d['scheme'],range(4,8));p={n:without_number(region(d['paper'],r)) for n,r in pr.items()};s={n:clean(without_number(region(d['scheme'],r))) for n,r in sr.items()};cards=[]
 def add(n,topic,marks,rows,notation,suffix='',prompt=None,fig=False):
  c=card(f'sa-q{n}{suffix}','A',f'Q{n}'+(' — '+suffix[1:] if suffix else ''),topic,prompt or clean(p[n]),'',marks,rows,pr[n]['page'],notation)
  if fig:c.update(questionFigureKey=f'home-economics-2010-ol-sa-q{n}',questionFigureIncludesPrompt=True)
  cards.append(c);return c
 elements=select(s[1],'(6 @ 1 mark)','Give one source');words=chosen(elements,['carbon','hydrogen','oxygen','nitrogen','sulphur','iron','phosphorus'])
 add(1,'0-5',4,[point(f'element-{i}',v,1) for i,v in enumerate(words[:3],1)]+[menu('fourth','Fourth element',1,1,words[3:],'The source lists carbon, hydrogen and oxygen, then alternatives in the fourth answer slot.')],'4 elements × 1',prompt=clean(p[1].split('Give one source',1)[0]))
 animal=examples(select(s[1],'Animal','Plant (Vegetable)'));plant=examples(select(s[1],'Plant (Vegetable)'))
 add(1,'0-5',2,[menu('animal','Animal',1,1,[x.strip() for x in animal.split(',')]),menu('plant','Plant (Vegetable)',1,1,[x.strip() for x in plant.split(',')])],'2 sources × 1',suffix='-sources',prompt=clean(select(p[1],'Give one source',include=True)))
 lines=named(select(s[2],'liver energy cellulose'),['Glucose releases','Excess glucose','Cellulose stimulates'])
 add(2,'0-6',6,[point(f'blank-{i}',v,2) for i,v in enumerate(lines,1)],'3 answers × 2',fig=True)
 lipids=named(select(s[3],'(2 @ 3 marks)'),['Melting Point:','Smoke Point:','Flash Point:'])
 c=add(3,'0-7',6,[menu('properties','Two properties of lipids',2,3,lipids)],'2 properties × 3');c['rows'][0]['openList']=False
 table=d['scheme'][4].find_tables().tables[0].extract();assert len(table)==4 and table[0]==['Vitamins','True','False'],table
 tf=[]
 for i,row in enumerate(table[1:],1):
  assert bool(row[1])!=bool(row[2]);value=table[0][1 if row[1] else 2];tf.append(point(f'statement-{i}',tidy(row[0])+' — '+value,2))
 add(4,'0-8',6,tf,'3 statements × 2',fig=True)
 guidelines=select(s[5],'(3 @ 2 marks)');opts=named(guidelines,['eat balanced','increase intake','avoid fatty','reduce salt,','reduce sugar'])
 add(5,'0-1',6,[menu('guidelines','Nutritional guidelines',3,2,opts)],'3 guidelines × 2')
 departments=select(s[6],'(2 @ 1 mark)','List two career');names=['An Bord Bia','Teagasc','Forbairt','Department of Food & Agriculture','BIM','FSAI','Department of Health','Department of Communications, Marine & Natural Resources','HSE','IDA']
 add(6,'0-11',2,[menu('agencies','Government departments or agencies',2,1,chosen(departments,names))],'2 names × 1',prompt=clean(p[6].split('List two career',1)[0]))
 careers=examples(select(s[6],'(2 @ 2 marks)'));opts=chosen(careers,['chef','waiter','receptionist','food manufacturing','dietetics','home economics teacher','butcher','confectioner','baker','engineer','agricultural scientist/ science graduates','sales','health inspector'])
 add(6,'0-11',4,[menu('careers','Career opportunities',2,2,opts)],'2 careers × 2',suffix='-careers',prompt=clean(select(p[6],'List two career',include=True)))
 flour=select(s[7],'(6 @ 1 mark)');rows=[];groups=[]
 for i in range(1,4):
  rows.extend([criterion(f'flour-{i}','Type of flour',1,[0,1],'Choose a different type in each pair. Complete printed table: '+flour),criterion(f'use-{i}','Culinary use',1,[0,1],'One different culinary use matching this same flour. Complete printed table: '+flour)])
  groups.append(dict(sourceCardId=f'he-2010-ol-sa-q7-pair-{i}',label=f'Flour / use pair {i}',marks=2,rowIds=[f'flour-{i}',f'use-{i}']))
 c=add(7,'0-9',6,rows,'3 matching pairs × (name 1 + use 1)',fig=True);c['taskGroups']=groups
 table=d['scheme'][5].find_tables().tables[0].extract();assert len(table)==4,table
 add(8,'0-11',6,[point(f'additive-{i}',tidy(a)+' — '+tidy(b),2) for i,(a,b) in enumerate(table[1:],1)],'3 matches × 2',fig=True)
 purpose=examples(select(s[9].split('Identify and explain',1)[0],'(1 @ 3 marks)'))
 add(9,'1-2',3,[point('purpose',purpose,3)],'1 explanation × 3',prompt=clean(p[9].split('Identify and explain',1)[0]))
 symbol=select(s[9],'Harmful / Irritant',include=True)
 c=add(9,'1-2',3,[point('symbol',symbol,3,'Identification and explanation share one printed three-mark award; no split is published.')],'1 identification / explanation × 3',suffix='-symbol',prompt=clean(select(p[9],'Identify and explain',include=True)))
 c.update(questionFigureKey='home-economics-2010-ol-sa-q9-symbol',questionFigureIncludesPrompt=False)
 budget=examples(select(s[10],'(2 @ 2 marks)','What protection'));opts=named(budget,['helps to develop','spending and the use','areas of overspending','economies can be','financial security','encourages savings','sets a good'])
 add(10,'1-1',4,[menu('advantages','Advantages of a household budget',2,2,opts)],'2 advantages × 2',prompt=clean(p[10].split('What protection',1)[0]))
 assurance=examples(select(s[10],'(1 @ 2 marks)'));add(10,'1-1',2,[point('protection',assurance,2)],'1 explanation × 2',suffix='-assurance',prompt=clean(select(p[10],'What protection',include=True)))
 technology=examples(select(s[11],'(3 @ 2 marks)'));opts=named(technology,['workload is lightened','some appliances save','appliances have built','save time','tasks are performed','security technology','communication technology','improvements in energy'])
 add(11,'1-3',6,[menu('technology','Technological developments',3,2,opts)],'3 points × 2')
 payments=named(select(s[12],'(2 @ 3 marks)'),['Credit card:','Laser Card:','Direct Debit / Standing Order:'])
 c=add(12,'1-1',6,[menu('payments','Two payment methods',2,3,payments)],'2 explanations × 3');c['rows'][0]['openList']=False
 assert len(cards)==16 and sum(c['totalMarks'] for c in cards)==72
 return cards
if __name__=='__main__':
 cards=a_build()
 if '--write' in sys.argv:transcript();write_section('A',cards,dict(tasks=16,marks=72,selectionDecisions='A1,6,9,10 independent companion asks split only at their published tariffs. Printed choose-two pools retained. Flour names and dependent uses remain three paired groups. No invented partial-credit ladders.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
