#!/usr/bin/env python3
"""2015 Ordinary original-source selections after the independent 48-page sweep."""
import hashlib,json,re,sys
import fitz
from he_review_2011_hl_main import ROOT,tidy,criterion,select,named,point,menu,semis,region,body_bottom,text,clean,without_number,examples,chosen,a_regions,WHOLE_NOTE
from he_review_2011_hl_main import card as prior_card
PAPER='paper-trail-corpus/exampapers/2015/LC098GLP000EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2015/LC098GLP000EV.pdf'
HASHES={PAPER:'e0aa871c86189030c12b785043448cb825fc6d3b2c2378bce9b59a0817e9f0f0',SCHEME:'1f24cb97ca1b4b1a6d68455ac4286339ffbe442cca28f839b700a1cdcb5727f1'}
REVIEW='scripts/markbank/authoring/home-economics/2015-ol-main-review.json'
def documents():
 for p,h in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 return {k:fitz.open(ROOT/p) for k,p in [('paper',PAPER),('scheme',SCHEME)]}
def card(key,section,ref,topic,prompt,stem,marks,rows,page,notation='',**extra):
 c=prior_card(key,section,ref,topic,prompt,stem,marks,rows,page,notation,**extra)
 c.update(id='he-2015-ol-'+key,year=2015,level='ordinary',questionRef='2015 OL Section '+section+' '+ref)
 c['sourceMaterial']['attribution']='SEC Home Economics 2015 Ordinary Level examination paper — © State Examinations Commission.'
 return c
def write_section(section,cards,review):
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text());ids={c['id'] for c in cards};assert len(ids)==len(cards)
 p.write_text(json.dumps([c for c in data if c['id'] not in ids]+cards,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text())
 if r['status']=='independent-source-census-complete-authoring-pending':r['status']='source-review-in-progress'
 r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],section=section,marks=c['totalMarks'],questionRef=c['questionRef'],topicId=c['topicId']) for c in cards];r['section'+section+'Review']=review;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
def transcript():
 d=documents()['scheme'];full='# SEC Home Economics 2015 Ordinary marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+p.get_text(sort=True) for i,p in enumerate(d))
 # Whole-page extraction interleaves the original tables's columns. Preserve
 # the raw transcript and append independent, coordinate-bounded cell reads.
 for pn in [4,5,7,9,17]:
  for i,t in enumerate(d[pn-1].find_tables().tables,1):
   full+=f'\n\n## Physical page {pn}, original table {i}, cell reading order\n\n'+'\n'.join(' | '.join(row).rstrip() for row in table_rows(t,d[pn-1]))
 (ROOT/'examiner-reports/home-economics/schemes/2015-ol.md').write_text(full.rstrip()+'\n')
def text(doc,n):
 # Original visible degree symbols extract as a detached combining ring.
 return tidy(doc[n-1].get_text(clip=fitz.Rect(0,20,doc[n-1].rect.width,body_bottom(doc[n-1])),sort=True)).replace('\u030a','°').replace('\uf0b7','•')
def table_rows(table,page):
 return [[tidy(page.get_text(clip=fitz.Rect(cell),sort=True)).replace('\u030a','°').replace('\uf0b7','•') if cell else '' for cell in row.cells] for row in table.rows]
def a_regions(doc,pages):
 out={}
 for n in pages:
  page=doc[n-1];starts=sorted((int(w[4][:-1]),w[1]-3) for w in page.get_text('words') if re.fullmatch(r'\d+\.',w[4]) and 40<w[0]<85 and w[1]<760)
  for i,(q,top) in enumerate(starts):out[q]=dict(page=n,rect=[35,top,page.rect.width-25,starts[i+1][1] if i+1<len(starts) else body_bottom(page)])
 assert list(out)==list(range(1,13)),out.keys()
 return out
def a_build():
 d=documents();pr=a_regions(d['paper'],range(2,6));sr=a_regions(d['scheme'],range(4,7));p={n:without_number(region(d['paper'],r)) for n,r in pr.items()};s={n:without_number(region(d['scheme'],r)) for n,r in sr.items()};rows={}
 def truth(grid):
  result=[]
  for i,(statement,yes,no) in enumerate(grid[1:],1):
   assert bool(yes)!=bool(no),(statement,yes,no)
   result.append(point(f'statement-{i}',tidy(statement)+' — '+grid[0][1 if yes else 2]))
  return result
 tables=d['scheme'][3].find_tables().tables;assert len(tables)==1
 rows[1]=truth(table_rows(tables[0],d['scheme'][3]))
 rows[2]=[point(f'blank-{i}',v) for i,v in enumerate(chosen(select(s[2],'(6)','Heat causes'),['coagulate','maillard reaction','opaque']),1)]
 rows[3]=[point(f'way-{i}',v,note='Choose ANY TWO ways from the complete original source pool; no one-per-line quota.') for i,v in enumerate(named(select(s[3],'(6)'),['(i)','(ii)']),1)]
 rows[4]=[point(f'function-{i}',v,note='Choose ANY TWO functions across both source lists.') for i,v in enumerate(named(select(s[4],'(6)','Name two good dietary sources of Vitamin C.'),['(i)','(ii)']),1)]+[point(f'source-{i}',v,note='Choose ANY TWO dietary sources across the complete fruit and vegetable lists.') for i,v in enumerate(named(select(s[4],'Name two good dietary sources of Vitamin C.'),['(i)','(ii)']),1)]
 rows[5]=[point(f'change-{i}',v,note='Choose ANY THREE lifestyle changes across all original source lines; no one-per-line quota.') for i,v in enumerate(named(select(s[5],'(6)'),['(i)','(ii)','(iii)']),1)]
 tables=d['scheme'][4].find_tables().tables;assert len(tables)==2
 rows[6]=truth(table_rows(tables[0],d['scheme'][4]))
 rows[7]=[point(f'class-{i}',a+' — '+b) for i,(a,b) in enumerate(table_rows(tables[1],d['scheme'][4])[1:],1)]
 rows[8]=[point(f'quality-{i}',v,note='Choose ANY TWO qualities across both source lists.') for i,v in enumerate(named(select(s[8],'(6)','Name two materials used to package food.'),['(i)','(ii)']),1)]+[point(f'material-{i}',v,note='Choose ANY TWO materials across both original source lists.') for i,v in enumerate(named(select(s[8],'Name two materials used to package food.'),['(i)','(ii)']),1)]
 rows[9]=[point(f'blank-{i}',v) for i,v in enumerate(chosen(select(s[9],'(6)','Flame retardant finishes reduce'),['flammability','Proban','self-extinguish']),1)]
 rows[10]=[point(f'type-{i}',v,note='Choose ANY TWO types of credit across both original lists.') for i,v in enumerate(named(select(s[10],'(6)','State the main advantage'),['(i)','(ii)']),1)]+[point('advantage',select(s[10],'State the main advantage of one of the types of credit named.'),note='ONE advantage must match ONE of the TWO credit types named. Original historical 2015 terms retained.')]
 rows[11]=[point('explanation',select(s[11],'(6)','Name one shopper loyalty scheme.')),point('scheme',select(s[11],'Name one shopper loyalty scheme.'),note='Name ONE scheme from the original open list.')]
 rows[12]=[point(f'right-{i}',v,note='Choose ANY TWO rights across both source lists.') for i,v in enumerate(named(select(s[12],'(6)','State the function'),['(i)','(ii)']),1)]+[point('function',select(s[12],'State the function of the Small Claims Procedure.'),note='Original historical 2015 limit and procedure retained for this examination task.')]
 topics={1:'0-8',2:'0-5',3:'0-10',4:'0-8',5:'0-1',6:'0-4',7:'0-9',8:'0-11',9:'1-4',10:'1-1',11:'1-2',12:'1-2'};figures=[1,6,7];cards=[]
 for n in range(1,13):
  prompt=clean(p[n].split('(6)',1)[0]) if n in figures else clean(p[n]);rows[n][0]['contextNote']=WHOLE_NOTE+(' '+rows[n][0]['contextNote'] if rows[n][0].get('contextNote') else '')
  if n in [2,9]:prompt=clean(re.sub(r'_{2,}','[blank]',p[n]))
  prompt=prompt.replace('\uf0fc','✓').replace('[blank]of','[blank] of')
  c=card(f'sa-q{n}','A',f'Q{n}',topics[n],prompt,'',6,rows[n],pr[n]['page'],tariffModel=dict(kind='questionTotal'))
  if n in figures:c.update(questionFigureKey=f'home-economics-2015-ol-sa-q{n}',questionFigureIncludesPrompt=True)
  cards.append(c)
 assert len(cards)==12 and sum(c['totalMarks'] for c in cards)==72
 return cards
if __name__=='__main__':
 cards=a_build()
 if '--write' in sys.argv:transcript();write_section('A',cards,dict(tasks=12,marks=72,tariffDecision='All12 whole-six tariffs retain unpriced source answers. Complete VitaminC functions/sources, packaging qualities/materials, credit/advantage, loyalty/name and rights/SmallClaims companion asks; two fixed true-false grids and closed cheese matching retained. No invented per-answer price or one-per-source-line quota.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
