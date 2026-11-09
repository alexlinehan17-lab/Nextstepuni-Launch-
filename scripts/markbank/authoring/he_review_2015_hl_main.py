#!/usr/bin/env python3
"""2015 Higher original-source selections after the independent 49-page sweep."""
import hashlib,json,re,sys
import fitz
from he_review_2011_hl_main import ROOT,tidy,criterion,select,named,point,menu,semis,region,body_bottom,text,clean,without_number,examples,chosen,a_regions,WHOLE_NOTE
from he_review_2011_hl_main import card as prior_card
PAPER='paper-trail-corpus/exampapers/2015/LC098ALP000EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2015/LC098ALP000EV.pdf'
HASHES={PAPER:'f983bc14638b99ad8c57e4c19dd44d2ff2037acf389b49d0c5cb0c25bcdd7047',SCHEME:'ed9467e251cfdf8084d1efc7dea7db47783b11c9a6f63fdcf7a87af0ae71bbdf'}
REVIEW='scripts/markbank/authoring/home-economics/2015-hl-main-review.json'
def documents():
 for p,h in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 return {k:fitz.open(ROOT/p) for k,p in [('paper',PAPER),('scheme',SCHEME)]}
def card(key,section,ref,topic,prompt,stem,marks,rows,page,notation='',**extra):
 c=prior_card(key,section,ref,topic,prompt,stem,marks,rows,page,notation,**extra)
 c.update(id='he-2015-hl-'+key,year=2015,level='higher',questionRef='2015 HL Section '+section+' '+ref)
 c['sourceMaterial']['attribution']='SEC Home Economics 2015 Higher Level examination paper — © State Examinations Commission.'
 return c
def write_section(section,cards,review):
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text());ids={c['id'] for c in cards};assert len(ids)==len(cards)
 p.write_text(json.dumps([c for c in data if c['id'] not in ids]+cards,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text())
 if r['status']=='independent-source-census-complete-authoring-pending':r['status']='source-review-in-progress'
 r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],section=section,marks=c['totalMarks'],questionRef=c['questionRef'],topicId=c['topicId']) for c in cards];r['section'+section+'Review']=review;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
def transcript():
 d=documents()['scheme'];full='# SEC Home Economics 2015 Higher marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+p.get_text(sort=True) for i,p in enumerate(d))
 # Whole-page extraction interleaves the carbohydrate table's columns. Preserve
 # the raw transcript and append independent, coordinate-bounded cell reads.
 for pn in [4,5,6,12,13,14,16]:
  for i,t in enumerate(d[pn-1].find_tables().tables,1):
   full+=f'\n\n## Physical page {pn}, original table {i}, cell reading order\n\n'+'\n'.join(' | '.join(row).rstrip() for row in table_rows(t,d[pn-1]))
 (ROOT/'examiner-reports/home-economics/schemes/2015-hl.md').write_text(full.rstrip()+'\n')
def text(doc,n):
 # Original visible degree symbols extract as a detached combining ring.
 return tidy(doc[n-1].get_text(clip=fitz.Rect(0,20,doc[n-1].rect.width,body_bottom(doc[n-1])),sort=True)).replace('\u030a','°')
def table_rows(table,page):
 return [[tidy(page.get_text(clip=fitz.Rect(cell),sort=True)).replace('\u030a','°') if cell else '' for cell in row.cells] for row in table.rows]
def a_regions(doc,pages):
 out={}
 for n in pages:
  page=doc[n-1];starts=sorted((int(w[4][:-1]),w[1]-3) for w in page.get_text('words') if re.fullmatch(r'\d+\.',w[4]) and 40<w[0]<85 and w[1]<760)
  for i,(q,top) in enumerate(starts):out[q]=dict(page=n,rect=[35,top,page.rect.width-25,starts[i+1][1] if i+1<len(starts) else body_bottom(page)])
 assert list(out)==list(range(1,13)),out.keys()
 return out
def a_build():
 d=documents();pr=a_regions(d['paper'],range(2,6));sr=a_regions(d['scheme'],range(4,8));p={n:without_number(region(d['paper'],r)) for n,r in pr.items()};s={n:without_number(region(d['scheme'],r)) for n,r in sr.items()};rows={}
 rows[1]=[point('deamination',select(s[1],'(6)'))]
 tables=d['scheme'][3].find_tables().tables;assert len(tables)==1
 rows[2]=[point(f'class-{i}',a+' — '+b+' — '+c,note='Give ONE example and its matching food source for this required class. Full original table preserves all printed example/source associations.') for i,(a,b,c) in enumerate(table_rows(tables[0],d['scheme'][3])[1:],1)]
 rows[3]=[point(f'function-{i}',v,note='Choose ANY THREE functions across all original source lines, without a one-per-line quota.') for i,v in enumerate(named(select(s[3],'(6)'),['(i)','(ii)','(iii)']),1)]
 rows[4]=[point(f'term-{i}',v) for i,(head,v) in enumerate(zip(['Smoke point','Flash point'],named(select(s[4],'(6)'),['Smoke point','Flash point'])),1)]
 tables=d['scheme'][4].find_tables().tables;assert len(tables)==2
 rows[5]=[point(f'part-{i}',a+' — '+b,note='Original scheme: Accept relevant nutrient and its function.') for i,(a,b) in enumerate(table_rows(tables[0],d['scheme'][4])[1:],1)]
 rows[6]=[point(f'condition-{i}',v,note='Choose ANY THREE conditions across all original source lines, without a one-per-line quota.') for i,v in enumerate(named(select(s[6],'(6)'),['(i)','(ii)','(iii)']),1)]
 rows[7]=[point(f'class-{i}',a+' — '+b,note='Complete the TWO original table rows using any TWO classes and one matching example each. All SIX original classes remain available.') for i,(a,b) in enumerate(table_rows(tables[1],d['scheme'][4])[1:],1)]
 tables=d['scheme'][5].find_tables().tables;assert len(tables)==1
 rows[8]=[point(f'method-{i}',a+' — '+b,note='Choose ANY TWO of the THREE original treatments and explain each; do not answer all three for extra marks.') for i,(a,b) in enumerate(table_rows(tables[0],d['scheme'][5]),1)]
 rows[9]=[point('purpose',select(s[9],'(6)','List the three components of management.'))]+[point(f'component-{i}',v.rstrip('.')) for i,v in enumerate(named(select(s[9],'List the three components of management.'),['(i)','(ii)','(iii)']),1)]
 rows[10]=[point(f'side-{i}',v,note='Give ONE point for this required side.') for i,(head,v) in enumerate(zip(['Advantage','Disadvantage'],named(select(s[10],'(6)'),['Advantage','Disadvantage'])),1)]
 rows[11]=[point(f'part-{i}',v) for i,(head,v) in enumerate(zip(['Thermostat','Refrigerant'],named(select(s[11],'(6)'),['Thermostat','Refrigerant'])),1)];rows[11][0]['contextNote']='The original thermostat source says “disconnects the motor when the temperature rises”; this wording is retained as printed.'
 rows[12]=[point(f'function-{i}',v,note='Choose ANY TWO functions across both source lines. Historical 2015 agency wording retained.') for i,v in enumerate(named(select(s[12],'(6)'),['(i)','(ii)']),1)]
 topics={1:'0-5',2:'0-6',3:'0-8',4:'0-7',5:'0-9',6:'0-2',7:'0-3',8:'0-4',9:'1-0',10:'1-1',11:'1-3',12:'1-2'};figures=[2,5,7,8];cards=[]
 for n in range(1,13):
  prompt=clean(p[n].split('(6)',1)[0]) if n in figures else clean(p[n]);rows[n][0]['contextNote']=WHOLE_NOTE+(' '+rows[n][0]['contextNote'] if rows[n][0].get('contextNote') else '')
  c=card(f'sa-q{n}','A',f'Q{n}',topics[n],prompt,'',6,rows[n],pr[n]['page'],tariffModel=dict(kind='questionTotal'))
  if n in figures:c.update(questionFigureKey=f'home-economics-2015-hl-sa-q{n}',questionFigureIncludesPrompt=True)
  if n==2:c['figureKey']='home-economics-2015-hl-sa-q2-answer-table'
  cards.append(c)
 assert len(cards)==12 and sum(c['totalMarks'] for c in cards)==72
 return cards
if __name__=='__main__':
 cards=a_build()
 if '--write' in sys.argv:transcript();write_section('A',cards,dict(tasks=12,marks=72,tariffDecision='All twelve printed whole-six tariffs retain unpriced original responses and complete companion asks. All six sauce classes and three enzyme-control treatments remain available with choose-two guidance. Complete carbohydrate table associations retained, plus original source wording note for thermostat.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
