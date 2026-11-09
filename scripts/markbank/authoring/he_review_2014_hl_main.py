#!/usr/bin/env python3
"""2014 Higher original-source selections after the independent 52-page sweep."""
import hashlib,json,re,sys
import fitz
from he_review_2011_hl_main import ROOT,tidy,criterion,select,named,point,menu,semis,region,body_bottom,text,clean,without_number,examples,chosen,a_regions,WHOLE_NOTE
from he_review_2011_hl_main import card as prior_card
PAPER='paper-trail-corpus/exampapers/2014/LC098ALP000EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2014/LC098ALP000EV.pdf'
HASHES={PAPER:'520a2a2ab00814b34453c21b7dd78323d855b08c778513672244b96dc17a3ef6',SCHEME:'93331547487b86d251bd7bd632f6f06ed248f7a3f0165408a15b864f268f0706'}
REVIEW='scripts/markbank/authoring/home-economics/2014-hl-main-review.json'
def documents():
 for p,h in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 return {k:fitz.open(ROOT/p) for k,p in [('paper',PAPER),('scheme',SCHEME)]}
def card(key,section,ref,topic,prompt,stem,marks,rows,page,notation='',**extra):
 c=prior_card(key,section,ref,topic,prompt,stem,marks,rows,page,notation,**extra)
 c.update(id='he-2014-hl-'+key,year=2014,questionRef='2014 HL Section '+section+' '+ref)
 c['sourceMaterial']['attribution']='SEC Home Economics 2014 Higher Level examination paper — © State Examinations Commission.'
 return c
def write_section(section,cards,review):
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text());ids={c['id'] for c in cards};assert len(ids)==len(cards)
 p.write_text(json.dumps([c for c in data if c['id'] not in ids]+cards,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text())
 if r['status']=='independent-source-census-complete-authoring-pending':r['status']='source-review-in-progress'
 r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],section=section,marks=c['totalMarks'],questionRef=c['questionRef'],topicId=c['topicId']) for c in cards];r['section'+section+'Review']=review;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
def transcript():
 d=documents()['scheme'];full='# SEC Home Economics 2014 Higher marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+p.get_text(sort=True) for i,p in enumerate(d))
 # Whole-page extraction interleaves the protein table's columns. Preserve
 # the raw transcript and append independent, coordinate-bounded cell reads.
 for pn in [4,5,6,8,9,10,13]:
  for i,t in enumerate(d[pn-1].find_tables().tables,1):
   full+=f'\n\n## Physical page {pn}, original table {i}, cell reading order\n\n'+'\n'.join(' | '.join(row).rstrip() for row in table_rows(t,d[pn-1]))
 full+='\n\n## Physical page 19, embedded image note — manually transcribed after visual inspection\n\nDue to an inconsistency between the English and Irish versions of the examination paper, non-renewable sources of energy were also accepted.\n'
 (ROOT/'examiner-reports/home-economics/schemes/2014-hl.md').write_text(full.rstrip()+'\n')
def table_rows(table,page):
 return [[tidy(page.get_text(clip=fitz.Rect(cell),sort=True)) if cell else '' for cell in row.cells] for row in table.rows]
def a_build():
 d=documents();pr=a_regions(d['paper'],range(2,6));sr=a_regions(d['scheme'],range(4,8));p={n:without_number(region(d['paper'],r)) for n,r in pr.items()};s={n:without_number(region(d['scheme'],r)) for n,r in sr.items()};rows={}
 rows[1]=[point(f'property-{i}',v) for i,v in enumerate(named(select(s[1],'(6)'),['Caramelisation','Crystallisation']),1)]
 rows[1][1]['contextNote']='The original crystallisation model literally says “if over 65% of jam is added”. That printed wording is retained; no substitute ingredient has been invented.'
 tables=d['scheme'][3].find_tables().tables;assert len(tables)==1;grid=table_rows(tables[0],d['scheme'][3]);rows[2]=[point(f'cell-{i}',grid[0][i]+' — '+grid[1][i],note='For the Small Intestine row.') for i in [1,2,3]]
 rows[3]=[point(f'iron-{i}',v) for i,v in enumerate(named(select(s[3],'(6)'),['Haem iron','Non-haem iron']),1)]
 rows[4]=[point('definition',select(s[4],'(6)','Give two factors'))]+[point(f'factor-{i}',v,note='Choose ANY TWO factors across the complete source lists; no one-per-line quota.') for i,v in enumerate(named(select(s[4],'Give two factors that determine a person’s basal metabolic rate.'),['(i)','(ii)']),1)]
 functions=select(s[5],'Function');rows[5]=[point(f'agency-{i}',v,note='Choose ONE named agency and explain its own primary function. Historical 2014 source wording retained.') for i,v in enumerate(named(functions,['Teagasc –','BIM –','An Bord Bia -','The Food Safety Authority of Ireland (FSAI)']),1)]
 tables=d['scheme'][4].find_tables().tables;assert len(tables)==1;rows[6]=[point(f'cheese-{i}',a+' — '+b,note='Complete THREE classification/example pairs using the original blank table. All five source classes remain available; no requirement to use all five.') for i,(a,b) in enumerate(table_rows(tables[0],d['scheme'][4])[1:],1)]
 rows[7]=[point('definition',select(s[7],'(6)','Outline two health benefits'))]+[point(f'benefit-{i}',v,note='Choose ANY TWO benefits from the complete source lists.') for i,v in enumerate(named(select(s[7],'Outline two health benefits of including functional foods in the diet.'),['(i)','(ii)']),1)]
 tables=d['scheme'][5].find_tables().tables;assert len(tables)==1;rows[8]=[point(f'organism-{i}',a+' — '+b) for i,(a,b) in enumerate(table_rows(tables[0],d['scheme'][5])[1:],1)]
 rows[9]=[point('definition',select(s[9],'(6)','Name two PRSI benefits.'))]+[point(f'benefit-{i}',v,note='Choose ANY TWO benefits from the complete historical 2014 source lists.') for i,v in enumerate(named(select(s[9],'Name two PRSI benefits.'),['(i)','(ii)']),1)]
 rows[10]=[point(f'feature-{i}',v) for i,v in enumerate(semis(select(s[10],'(6)')),1)]
 rows[11]=[point('finish',select(s[11],'(6)','Outline two effects'))]+[point(f'effect-{i}',v,note='Choose ANY TWO effects for the chosen finish; original source models retained.') for i,v in enumerate(named(select(s[11],'Outline two effects of this finish.'),['(i)','(ii)']),1)]
 rows[12]=[point(f'point-{i}',v,note='Give ANY TWO points from the complete source lists.') for i,v in enumerate(named(select(s[12],'(6)'),['(i)','(ii)']),1)]
 topics={1:'0-6',2:'0-7',3:'0-8',4:'0-1',5:'0-11',6:'0-9',7:'0-1',8:'0-4',9:'1-1',10:'3-3',11:'1-4',12:'1-5'};figures=[2,6,8];cards=[]
 for n in range(1,13):
  prompt=clean(p[n].split('(6)',1)[0]) if n in figures else clean(p[n]);rows[n][0]['contextNote']=WHOLE_NOTE+(' '+rows[n][0]['contextNote'] if rows[n][0].get('contextNote') else '')
  if n==10:rows[n][0]['contextNote']+=' Give TWO features. The original historical 2014 policy guidance is retained.'
  c=card(f'sa-q{n}','A',f'Q{n}',topics[n],prompt,'',6,rows[n],pr[n]['page'],tariffModel=dict(kind='questionTotal'))
  if n in figures:c.update(questionFigureKey=f'home-economics-2014-hl-sa-q{n}',questionFigureIncludesPrompt=True)
  cards.append(c)
 assert len(cards)==12 and sum(c['totalMarks'] for c in cards)==72
 return cards
if __name__=='__main__':
 cards=a_build()
 if '--write' in sys.argv:transcript();write_section('A',cards,dict(tasks=12,marks=72,tariffDecision='All twelve printed whole-six tariffs and complete companion prompts retained with unpriced source rows and visible guidance. Three cheese pairs from all five source classes; all other original pools retained. Original crystallisation wording visible, no invented correction.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
