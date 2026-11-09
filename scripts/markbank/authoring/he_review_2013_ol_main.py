#!/usr/bin/env python3
"""2013 Ordinary original-source selections after the independent 48-page sweep."""
import hashlib,json,re,sys
import fitz
from he_review_2011_hl_main import ROOT,tidy,criterion,select,named,point,menu,semis,region,body_bottom,text,clean,without_number,examples,chosen,a_regions,WHOLE_NOTE
from he_review_2011_hl_main import card as prior_card
PAPER='paper-trail-corpus/exampapers/2013/LC098GLP000EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2013/LC098GLP000EV.pdf'
HASHES={PAPER:'4e08ed9a0032d4e91f1e46110e82960b8e8c50dd0b192d47b697224c0c9a0d7e',SCHEME:'d52c45073f9ac1867280624c21467101b3be27f3a674dc216f8211db9dc7c98c'}
REVIEW='scripts/markbank/authoring/home-economics/2013-ol-main-review.json'
def documents():
 for p,h in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 return {k:fitz.open(ROOT/p) for k,p in [('paper',PAPER),('scheme',SCHEME)]}
def card(key,section,ref,topic,prompt,stem,marks,rows,page,notation='',**extra):
 c=prior_card(key,section,ref,topic,prompt,stem,marks,rows,page,notation,**extra)
 c.update(id='he-2013-ol-'+key,year=2013,level='ordinary',questionRef='2013 OL Section '+section+' '+ref)
 c['sourceMaterial']['attribution']='SEC Home Economics 2013 Ordinary Level examination paper — © State Examinations Commission.'
 return c
def write_section(section,cards,review):
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text());ids={c['id'] for c in cards};assert len(ids)==len(cards)
 p.write_text(json.dumps([c for c in data if c['id'] not in ids]+cards,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text())
 if r['status']=='independent-source-census-complete-authoring-pending':r['status']='source-review-in-progress'
 r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],section=section,marks=c['totalMarks'],questionRef=c['questionRef'],topicId=c['topicId']) for c in cards];r['section'+section+'Review']=review;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
def transcript():
 d=documents()['scheme'];full='# SEC Home Economics 2013 Ordinary marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+p.get_text(sort=True) for i,p in enumerate(d))
 # Whole-page extraction interleaves the protein table's columns. Preserve
 # the raw transcript and append independent, coordinate-bounded cell reads.
 for pn in [4,5,7]:
  for i,t in enumerate(d[pn-1].find_tables().tables,1):
   full+=f'\n\n## Physical page {pn}, original table {i}, cell reading order\n\n'+'\n'.join(' | '.join(row).rstrip() for row in table_rows(t,d[pn-1]))
 (ROOT/'examiner-reports/home-economics/schemes/2013-ol.md').write_text(full.rstrip()+'\n')
def table_rows(table,page):
 return [[tidy(page.get_text(clip=fitz.Rect(cell),sort=True)) if cell else '' for cell in row.cells] for row in table.rows]
def a_build():
 d=documents();pr=a_regions(d['paper'],range(2,6));sr=a_regions(d['scheme'],range(4,8));p={n:without_number(region(d['paper'],r)) for n,r in pr.items()};s={n:without_number(region(d['scheme'],r)) for n,r in sr.items()};rows={}
 tables=d['scheme'][3].find_tables().tables;assert len(tables)==2
 rows[1]=[point(f'fat-{i}',a+' — '+b) for i,(a,b) in enumerate(table_rows(tables[0],d['scheme'][3])[1:],1)]
 # Use the actual supplied word pool; show the solution's spelling mismatch.
 pool=select(s[2],'(6)','Vitamin A is necessary')
 answers=chosen(pool,['rhodopsin','night blindness','hypervitaminosis']);rows[2]=[point(f'blank-{i}',v) for i,v in enumerate(answers,1)];rows[2][2]['contextNote']='The printed word pool gives hypervitaminosis. The completed source line misspells that word as hypervitiminosis; the supplied word is retained here.'
 def truth(grid):
  result=[]
  for i,(statement,yes,no) in enumerate(grid[1:],1):
   assert bool(yes)!=bool(no),(statement,yes,no)
   result.append(point(f'statement-{i}',tidy(statement)+' — '+grid[0][1 if yes else 2]))
  return result
 rows[3]=truth(tables[1].extract())
 tables=d['scheme'][4].find_tables().tables;assert len(tables)==2;grid=table_rows(tables[0],d['scheme'][4]);rows[4]=[]
 for i,head in enumerate(grid[0]):
  body=' '.join(re.sub(r'^\d\.\s*','',r[i]) for r in grid[1:]);rows[4].append(point(f'method-{i}',head,note='Choose TWO examples for this method from the complete original list: '+body))
 rows[5]=[point(f'nutrient-{i}',v) for i,v in enumerate(chosen(select(s[5],'(6)','Name two heat treatments'),['protein','carbohydrate']),1)]+[point('treatments',clean(select(s[5],'Name two heat treatments applied to milk to extend its shelf life.')))]
 rows[6]=truth(tables[1].extract())
 rows[7]=[point(f'growth-{i}',v,note='Choose ANY TWO growth conditions across both printed source lines; no one-per-line quota.') for i,v in enumerate(named(select(s[7],'(6)','State one use'),['(i)','(ii)']),1)]+[point('use',select(s[7],'State one use of micro-organisms in food production.'))]
 rows[8]=[point('hand-wash',select(s[8],'Hand wash only',include=True)[:len('Hand wash only')]),point('tumble',select(s[8],'Do not tumble dry',include=True)[:len('Do not tumble dry')])]
 rows[9]=[point(f'income-{i}',v) for i,v in enumerate(named(select(s[9],'(6)'),['Gross Income:','Net Income:']),1)]
 rows[10]=[point('provider',select(s[10],'(6)','State two advantages')),point('advantages',clean(select(s[10],'State two advantages of private health insurance.')))]
 tables=d['scheme'][6].find_tables().tables;assert len(tables)==1;grid=table_rows(tables[0],d['scheme'][6]);rows[11]=[point('features',grid[1][0],note='Original accompanying use examples: '+grid[1][1]+' These are shared source lists: match each of TWO chosen features to an appropriate use; no extra individual pairings have been invented.'),point('rcd',grid[2][0],note='Original paired use: '+grid[2][1])]
 rows[12]=[point('techniques',clean(select(s[12],'(6)','How does merchandising'))),point('spending',select(s[12],'How does merchandising encourage consumer spending?'))]
 topics={1:'0-7',2:'0-8',3:'0-1',4:'0-3',5:'0-9',6:'0-3',7:'0-4',8:'1-4',9:'1-1',10:'1-1',11:'1-3',12:'1-2'};figures=[1,3,4,6,8,11];cards=[]
 for n in range(1,13):
  prompt=clean(p[n].split('(6)',1)[0]) if n in figures else clean(p[n]);rows[n][0]['contextNote']=WHOLE_NOTE+(' '+rows[n][0]['contextNote'] if rows[n][0].get('contextNote') else '')
  if n==2:prompt=clean(re.sub(r'_{2,}','[blank]',p[n]))
  prompt=prompt.replace('\uf0fc','✓')
  if n in [10]:rows[n][0]['contextNote']+=' Historical 2013 provider names and scheme wording retained.'
  c=card(f'sa-q{n}','A',f'Q{n}',topics[n],prompt,'',6,rows[n],pr[n]['page'],tariffModel=dict(kind='questionTotal'))
  if n in figures:c.update(questionFigureKey=f'home-economics-2013-ol-sa-q{n}',questionFigureIncludesPrompt=True)
  cards.append(c)
 assert len(cards)==12 and sum(c['totalMarks'] for c in cards)==72
 return cards
if __name__=='__main__':
 cards=a_build()
 if '--write' in sys.argv:transcript();write_section('A',cards,dict(tasks=12,marks=72,tariffDecision='All twelve original whole6 tariffs, complete companion prompts and full source guidance retained without inferred splits. Original A2 word-pool/answer spelling discrepancy visible; source safety-feature/use list associations preserved.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
