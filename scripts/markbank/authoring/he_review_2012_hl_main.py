#!/usr/bin/env python3
"""2012 Higher original-source selections after the independent 48-page sweep."""
import hashlib,json,re,sys
import fitz
from he_review_2011_hl_main import ROOT,tidy,criterion,select,named,point,menu,semis,region,body_bottom,text,clean,without_number,examples,chosen,a_regions,WHOLE_NOTE
from he_review_2011_hl_main import card as prior_card
PAPER='paper-trail-corpus/exampapers/2012/LC098ALP000EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2012/LC098ALP000EV.pdf'
HASHES={PAPER:'545d922fd61d92a465f64d68bfd95dd898cc7506e6710f1c679eb2d322da4d20',SCHEME:'522426f0c1258dfe6db2c0a41674482e911e906af28b0af771e2598523402dc8'}
REVIEW='scripts/markbank/authoring/home-economics/2012-hl-main-review.json'
def documents():
 for p,h in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 return {k:fitz.open(ROOT/p) for k,p in [('paper',PAPER),('scheme',SCHEME)]}
def card(key,section,ref,topic,prompt,stem,marks,rows,page,notation='',**extra):
 c=prior_card(key,section,ref,topic,prompt,stem,marks,rows,page,notation,**extra)
 c.update(id='he-2012-hl-'+key,year=2012,questionRef='2012 HL Section '+section+' '+ref)
 c['sourceMaterial']['attribution']='SEC Home Economics 2012 Higher Level examination paper — © State Examinations Commission.'
 return c
def write_section(section,cards,review):
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text());ids={c['id'] for c in cards};assert len(ids)==len(cards)
 p.write_text(json.dumps([c for c in data if c['id'] not in ids]+cards,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text())
 if r['status']=='independent-source-census-complete-authoring-pending':r['status']='source-review-in-progress'
 r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],section=section,marks=c['totalMarks'],questionRef=c['questionRef'],topicId=c['topicId']) for c in cards];r['section'+section+'Review']=review;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
def transcript():
 d=documents()['scheme'];(ROOT/'examiner-reports/home-economics/schemes/2012-hl.md').write_text(('# SEC Home Economics 2012 Higher marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+p.get_text(sort=True) for i,p in enumerate(d))).rstrip()+'\n')
def a_build():
 d=documents();pr=a_regions(d['paper'],range(2,6));sr=a_regions(d['scheme'],range(4,7));p={n:without_number(region(d['paper'],r)) for n,r in pr.items()};s={n:without_number(region(d['scheme'],r)) for n,r in sr.items()};rows={}
 functions=select(s[1],'(6)','List two');sources=select(s[1],'List two good dietary sources of sodium.')
 rows[1]=[point('functions',functions)]+[point(f'sources-{i}',v) for i,v in enumerate(named(sources,['(i)','(ii)']),1)]
 rows[2]=[point('ldl',select(s[2],'(i)','(ii)')),point('hdl',select(s[2],'(ii)'))]
 rows[3]=[point('explanation',select(s[3],'(6)'))]
 rows[4]=[point('meaning',select(s[4],'(i)','(ii)')),point('examples',select(s[4],'(ii)'))]
 tables=d['scheme'][4].find_tables().tables;assert len(tables)==2
 rows[5]=[point(f'food-{i}',tidy(label),note='Original table: Source — '+tidy(source)+'; Product — '+tidy(product)) for i,(label,source,product) in enumerate(tables[0].extract()[1:],1)]
 rows[6]=[point(f'method-{i}',tidy(label),note='Original cooking examples: '+tidy(value)) for i,(label,value) in enumerate(tables[1].extract()[1:],1)]
 rows[6][0]['contextNote']+=' The original scheme places Microwave cooking under Conduction; this preserves its printed classification.'
 rows[7]=[point(f'sector-{i}',v) for i,v in enumerate(named(select(s[7],'(6)'),['(i)','(ii)','(iii)']),1)]
 labelled=select(s[8],'A.','A B C',True)
 rows[8]=[point(f'label-{i}',v) for i,v in enumerate(named(labelled,['A.','B.','C.']),1)]
 for n in [9,10,11]:rows[n]=[point(f'answer-{i}',v) for i,v in enumerate(named(select(s[n],'(6)'),['(i)','(ii)']),1)]
 rows[12]=[point('meaning',select(s[12],'(6)','Name two'))]+[point(f'appliances-{i}',v) for i,v in enumerate(named(select(s[12],'Name two household appliances which carry an energy label.'),['(i)','(ii)']),1)]
 topics={1:'0-8',2:'0-7',3:'0-11',4:'0-9',5:'0-5',6:'0-3',7:'0-11',8:'0-4',9:'1-2',10:'1-1',11:'1-2',12:'1-3'};cards=[]
 for n in range(1,13):
  prompt=clean(p[n].split('(6)',1)[0]) if n in [5,6,8] else clean(p[n])
  rows[n][0]['contextNote']=WHOLE_NOTE+(' '+rows[n][0]['contextNote'] if rows[n][0].get('contextNote') else '')
  if n in [9,10,12]:rows[n][0]['contextNote']+=' Historical 2012 source wording is retained for this examination task.'
  c=card(f'sa-q{n}','A',f'Q{n}',topics[n],prompt,'',6,rows[n],pr[n]['page'],tariffModel=dict(kind='questionTotal'))
  if n in [5,6,8]:c.update(questionFigureKey=f'home-economics-2012-hl-sa-q{n}',questionFigureIncludesPrompt=True)
  if n==8:c['labelKey']=[dict(letter=letter,meaning=row['verbatim'].split('. ',1)[1],askedInThisQuestion=True) for letter,row in zip(['A','B','C'],rows[n])]
  cards.append(c)
 assert len(cards)==12 and sum(c['totalMarks'] for c in cards)==72
 return cards
if __name__=='__main__':
 cards=a_build()
 if '--write' in sys.argv:transcript();write_section('A',cards,dict(tasks=12,marks=72,tariffDecision='Published whole-question six-mark totals only. Full unpriced source rows plus visible total-only explanation; no per-answer split or partial ladder invented. All companion asks and original table/diagram inputs retained.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
