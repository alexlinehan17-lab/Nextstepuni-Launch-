#!/usr/bin/env python3
"""2014 Ordinary original-source selections after the independent 48-page sweep."""
import hashlib,json,re,sys
import fitz
from he_review_2011_hl_main import ROOT,tidy,criterion,select,named,point,menu,semis,region,body_bottom,text,clean,without_number,examples,chosen,a_regions,WHOLE_NOTE
from he_review_2011_hl_main import card as prior_card
PAPER='paper-trail-corpus/exampapers/2014/LC098GLP000EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2014/LC098GLP000EV.pdf'
HASHES={PAPER:'42e680a67b38aa3c7c13b7cc73c1feb32c0230e81cd9ac67fd51a37a394b2df6',SCHEME:'755b7743b1dc19b8dca4d37ef254c34e5ac3a3ba7b6c17a8c0f66165f4bba044'}
REVIEW='scripts/markbank/authoring/home-economics/2014-ol-main-review.json'
def documents():
 for p,h in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 return {k:fitz.open(ROOT/p) for k,p in [('paper',PAPER),('scheme',SCHEME)]}
def card(key,section,ref,topic,prompt,stem,marks,rows,page,notation='',**extra):
 c=prior_card(key,section,ref,topic,prompt,stem,marks,rows,page,notation,**extra)
 c.update(id='he-2014-ol-'+key,year=2014,level='ordinary',questionRef='2014 OL Section '+section+' '+ref)
 c['sourceMaterial']['attribution']='SEC Home Economics 2014 Ordinary Level examination paper — © State Examinations Commission.'
 return c
def write_section(section,cards,review):
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text());ids={c['id'] for c in cards};assert len(ids)==len(cards)
 p.write_text(json.dumps([c for c in data if c['id'] not in ids]+cards,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text())
 if r['status']=='independent-source-census-complete-authoring-pending':r['status']='source-review-in-progress'
 r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],section=section,marks=c['totalMarks'],questionRef=c['questionRef'],topicId=c['topicId']) for c in cards];r['section'+section+'Review']=review;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
def transcript():
 d=documents()['scheme'];full='# SEC Home Economics 2014 Ordinary marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+p.get_text(sort=True) for i,p in enumerate(d))
 # Whole-page extraction interleaves the protein table's columns. Preserve
 # the raw transcript and append independent, coordinate-bounded cell reads.
 for pn in [4,5,6,7,8,10,11]:
  for i,t in enumerate(d[pn-1].find_tables().tables,1):
   full+=f'\n\n## Physical page {pn}, original table {i}, cell reading order\n\n'+'\n'.join(' | '.join(row).rstrip() for row in table_rows(t,d[pn-1]))
 (ROOT/'examiner-reports/home-economics/schemes/2014-ol.md').write_text(full.rstrip()+'\n')
def table_rows(table,page):
 return [[tidy(page.get_text(clip=fitz.Rect(cell),sort=True)) if cell else '' for cell in row.cells] for row in table.rows]
def a_build():
 d=documents();pr=a_regions(d['paper'],range(2,6));sr=a_regions(d['scheme'],range(4,8));p={n:without_number(region(d['paper'],r)) for n,r in pr.items()};s={n:without_number(region(d['scheme'],r)) for n,r in sr.items()};rows={}
 def truth(grid):
  result=[]
  for i,(statement,yes,no) in enumerate(grid[1:],1):
   assert bool(yes)!=bool(no),(statement,yes,no)
   result.append(point(f'statement-{i}',tidy(statement)+' — '+grid[0][1 if yes else 2]))
  return result
 tables=d['scheme'][3].find_tables().tables;assert len(tables)==2
 rows[1]=truth(table_rows(tables[0],d['scheme'][3]))
 rows[2]=[point(f'class-{i}',re.sub(r'^\d\.\s*','',a)+' — '+re.sub(r'^\d\.\s*','',b),note='One example of this required vitamin class.') for i,(a,b) in enumerate(table_rows(tables[1],d['scheme'][3])[1:],1)]
 rows[3]=[point(f'function-{i}',v,note='Choose ANY TWO biological functions across the complete source guidance.') for i,v in enumerate(named(select(s[3],'(6)','Name two good dietary sources of iron.'),['(i)','(ii)']),1)]+[point(f'source-{i}',v,note='Choose ANY TWO dietary sources across both printed lists.') for i,v in enumerate(named(select(s[3],'Name two good dietary sources of iron.'),['(i)','(ii)']),1)]
 tables=d['scheme'][4].find_tables().tables;assert len(tables)==2;rows[4]=truth(table_rows(tables[0],d['scheme'][4]))
 grid=table_rows(tables[1],d['scheme'][4]);assert [i for i,x in enumerate(grid[1]) if x]==[1];rows[5]=[point('nutrient',grid[0][1])]+[point(f'effect-{i}',v,note='Choose ANY TWO cooking effects from both source lines.') for i,v in enumerate(named(select(s[5],'List two effects of cooking on cheese.'),['(i)','(ii)']),1)]
 pool=select(s[6],'(6)','mincing helps');rows[6]=[point(f'blank-{i}',v) for i,v in enumerate(chosen(pool,['mincing','collagen','denaturation']),1)]
 rows[7]=[point(f'change-{i}',v,note='Choose ANY THREE changes from all printed source guidance; no one-per-line quota.') for i,v in enumerate(named(select(s[7],'(6)'),['(i)','(ii)','(iii)']),1)]
 rows[8]=[point('definition',select(s[8],'(6)','Give two examples'))]+[point(f'example-{i}',v,note='Choose ANY TWO examples across both source lists.') for i,v in enumerate(named(select(s[8],'Give two examples of added value foods sold in supermarkets.'),['(i)','(ii)']),1)]
 tables=d['scheme'][5].find_tables().tables;assert len(tables)==1;rows[9]=[point(f'part-{i}',a+' — '+b) for i,(a,b) in enumerate(table_rows(tables[0],d['scheme'][5])[1:],1)]
 rows[10]=[point('definition',select(s[10],'(6)','Give two examples'))]+[point(f'use-{i}',v,note='Choose ANY TWO uses across both printed source lists.') for i,v in enumerate(named(select(s[10],'Give two examples of how PAYE contributions are used by the government.'),['(i)','(ii)']),1)]
 tables=d['scheme'][6].find_tables().tables;assert len(tables)==1;grid=table_rows(tables[0],d['scheme'][6]);rows[11]=[point('natural',grid[0][0]+' — '+grid[1][0],note='Choose ONE natural fibre.'),point('synthetic',grid[0][1]+' — '+grid[1][1],note='Choose ONE synthetic fibre.'),point('reason',select(s[11],'Explain why natural fibres are commonly used in household textiles.'))]
 rows[12]=[point(f'body-{i}',v,note='Choose ONE body from this required category. Original historical 2014 classification retained.') for i,v in enumerate(named(select(s[12],'(6)'),['Statutory body:','Voluntary body / agency:']),1)]
 topics={1:'0-7',2:'0-8',3:'0-8',4:'0-1',5:'0-9',6:'0-3',7:'0-1',8:'0-11',9:'1-3',10:'1-1',11:'1-4',12:'1-2'};figures=[1,2,4,5,9,11];cards=[]
 for n in range(1,13):
  prompt=clean(p[n].split('(6)',1)[0]) if n in figures else clean(p[n]);rows[n][0]['contextNote']=WHOLE_NOTE+(' '+rows[n][0]['contextNote'] if rows[n][0].get('contextNote') else '')
  if n==6:prompt=clean(re.sub(r'_{2,}','[blank]',p[n]))
  if n in [5,11]:prompt=clean(p[n])
  prompt=prompt.replace('\uf0fc','✓')
  c=card(f'sa-q{n}','A',f'Q{n}',topics[n],prompt,'',6,rows[n],pr[n]['page'],tariffModel=dict(kind='questionTotal'))
  if n in figures:c.update(questionFigureKey=f'home-economics-2014-ol-sa-q{n}',questionFigureIncludesPrompt=True)
  cards.append(c)
 assert len(cards)==12 and sum(c['totalMarks'] for c in cards)==72
 return cards
if __name__=='__main__':
 cards=a_build()
 if '--write' in sys.argv:transcript();write_section('A',cards,dict(tasks=12,marks=72,tariffDecision='Twelve printed whole-six questions retain all unpriced source answers, complete companion prompts and original pools. No invented per-answer marks or one-per-source-line quota. Vitamin/iron, cheese tick/effects, PAYE/use and fibre/reason companions intact; three meat blanks preserved.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
