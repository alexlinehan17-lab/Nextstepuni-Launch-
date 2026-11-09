#!/usr/bin/env python3
"""2012 Ordinary original-source selections after the independent 44-page sweep."""
import hashlib,json,re,sys
import fitz
from he_review_2011_hl_main import ROOT,tidy,criterion,select,named,point,menu,semis,region,body_bottom,text,clean,without_number,examples,chosen,a_regions,WHOLE_NOTE
from he_review_2011_hl_main import card as prior_card
PAPER='paper-trail-corpus/exampapers/2012/LC098GLP000EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2012/LC098GLP000EV.pdf'
HASHES={PAPER:'c92998f0e2ff944108a0615022a899b910776248b2fe219317c6d08dadb5c4b1',SCHEME:'3f3fbde5c556d4d9d94935ffc2965da75ec01e1e59f59446dea64d5343529b50'}
REVIEW='scripts/markbank/authoring/home-economics/2012-ol-main-review.json'
def documents():
 for p,h in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 return {k:fitz.open(ROOT/p) for k,p in [('paper',PAPER),('scheme',SCHEME)]}
def card(key,section,ref,topic,prompt,stem,marks,rows,page,notation='',**extra):
 c=prior_card(key,section,ref,topic,prompt,stem,marks,rows,page,notation,**extra)
 c.update(id='he-2012-ol-'+key,year=2012,level='ordinary',questionRef='2012 OL Section '+section+' '+ref)
 c['sourceMaterial']['attribution']='SEC Home Economics 2012 Ordinary Level examination paper — © State Examinations Commission.'
 return c
def write_section(section,cards,review):
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text());ids={c['id'] for c in cards};assert len(ids)==len(cards)
 p.write_text(json.dumps([c for c in data if c['id'] not in ids]+cards,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text())
 if r['status']=='independent-source-census-complete-authoring-pending':r['status']='source-review-in-progress'
 r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],section=section,marks=c['totalMarks'],questionRef=c['questionRef'],topicId=c['topicId']) for c in cards];r['section'+section+'Review']=review;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
def transcript():
 d=documents()['scheme'];(ROOT/'examiner-reports/home-economics/schemes/2012-ol.md').write_text(('# SEC Home Economics 2012 Ordinary marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+p.get_text(sort=True) for i,p in enumerate(d))).rstrip()+'\n')
def a_build():
 d=documents();pr=a_regions(d['paper'],range(2,6));sr=a_regions(d['scheme'],range(4,7));p={n:without_number(region(d['paper'],r)) for n,r in pr.items()};s={n:without_number(region(d['scheme'],r)) for n,r in sr.items()};rows={}
 table=d['scheme'][3].find_tables().tables[0].extract();assert len(table)==4
 rows[1]=[point(f'statement-{i}',tidy(row[0])+' — '+('True' if row[1] else 'False')) for i,row in enumerate(table[1:],1)]
 rows[2]=[point(f'blank-{i}',v) for i,v in enumerate(named(select(s[2],'insoluble, gelatinisation, hygroscopic'),['Starch can absorb','When starch is heated','Starch is insoluble']),1)]
 rows[3]=[point('functions',re.sub(r'\((?:i|ii|iii)\)\s*','',select(s[3],'(6)')))]
 rows[4]=[point('meaning',select(s[4],'(6)','List two'))]+[point(f'source-{i}',v) for i,v in enumerate(named(select(s[4],'List two sources of haem-iron.'),['(i)','(ii)']),1)]
 tables=d['scheme'][4].find_tables().tables;assert len(tables)==2
 rows[5]=[point(f'nutrient-{i}',tidy(n),note='Original food sources: '+tidy(a)+'; '+tidy(b)) for i,(n,a,b) in enumerate(tables[0].extract()[1:],1)]
 fruit=tables[1].extract();rows[6]=[point(f'class-{i}',tidy(a)+' — '+tidy(b)) for i,(a,b) in enumerate(fruit[1:4],1)]
 last_labels=fruit[4][0].splitlines();last_labels=[*last_labels[:2],tidy(' '.join(last_labels[2:]))];last_values=fruit[4][1].splitlines();assert len(last_labels)==len(last_values)==3
 rows[6]+=[point(f'class-{i+4}',a+' — '+b) for i,(a,b) in enumerate(zip(last_labels,last_values))]
 rows[7]=[point('meaning',select(s[7],'(6)','State two'))]+[point(f'disadvantage-{i}',v) for i,v in enumerate(named(select(s[7],'State two disadvantages of using additives in food.'),['(i)','(ii)']),1)]
 rows[8]=[point(f'reason-{i}',v) for i,v in enumerate(named(select(s[8],'(6)','Name two'),['(i)','(ii)']),1)]+[point(f'export-{i}',v) for i,v in enumerate(named(select(s[8],'Name two major Irish Food Exports.'),['(i)','(ii)']),1)]
 rows[9]=[point('meaning',select(s[9],'(6)','State two'))]+[point(f'benefit-{i}',v) for i,v in enumerate(named(select(s[9],'State two benefits of PRSI to the individual.'),['(i)','(ii)']),1)]
 tables=d['scheme'][5].find_tables().tables;assert len(tables)==2
 rows[10]=[point(f'property-{i}',tidy(a)) for i,(a,b) in enumerate(tables[0].extract()[1:],1) if b]
 energy=tables[1].extract();rows[11]=[point(f'energy-{i}',tidy(energy[0][i]),note='Original table examples: '+tidy(energy[1][i])) for i in [0,1]]
 rows[11][0]['contextNote']+=' The original scheme includes nuclear in the renewable cell and uranium in the non-renewable cell; the printed classification is preserved here.'
 rows[11]+=[point(f'method-{i}',v) for i,v in enumerate(named(select(s[11],'State two different methods of reducing energy consumption in the home.'),['(i)','(ii)']),1)]
 rows[12]=[point(f'factor-{i}',v) for i,v in enumerate(named(select(s[12],'(6)','Name one'),['(i)','(ii)']),1)]+[point('statutory-body',select(s[12],'Statutory Body',include=True))]
 topics={1:'0-5',2:'0-6',3:'0-1',4:'0-8',5:'0-1',6:'0-9',7:'0-11',8:'0-11',9:'1-1',10:'1-4',11:'1-5',12:'1-2'};cards=[]
 for n in range(1,13):
  prompt=clean(p[n].split('(6)',1)[0]) if n in [1,2,5,6,10] else clean(p[n]);prompt=prompt.replace('\uf0fc','✓')
  rows[n][0]['contextNote']=WHOLE_NOTE+(' '+rows[n][0]['contextNote'] if rows[n][0].get('contextNote') else '')
  if n==10:rows[n][0]['contextNote']+=' Choose THREE of the four properties ticked in the source; the complete six-option printed pool is shown above.'
  if n in [9,12]:rows[n][0]['contextNote']+=' Historical 2012 source names and conditions are retained for this examination.'
  c=card(f'sa-q{n}','A',f'Q{n}',topics[n],prompt,'',6,rows[n],pr[n]['page'],tariffModel=dict(kind='questionTotal'))
  if n in [1,2,5,6,10,11]:c.update(questionFigureKey=f'home-economics-2012-ol-sa-q{n}',questionFigureIncludesPrompt=True)
  cards.append(c)
 assert len(cards)==12 and sum(c['totalMarks'] for c in cards)==72
 return cards
if __name__=='__main__':
 cards=a_build()
 if '--write' in sys.argv:transcript();write_section('A',cards,dict(tasks=12,marks=72,tariffDecision='All twelve whole six-mark totals retained; full unpriced source answers and visible total-only explanation. Companion asks and table inputs retained, no invented granular tariffs.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
