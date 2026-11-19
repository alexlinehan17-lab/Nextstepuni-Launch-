#!/usr/bin/env python3
"""2016 Ordinary original-source selections after the independent 48-page sweep."""
import hashlib,json,re,sys
import fitz
from he_review_2011_hl_main import ROOT,tidy,criterion,select,named,point,menu,semis,region,body_bottom,text,clean,without_number,examples,chosen,a_regions,WHOLE_NOTE
from he_review_2011_hl_main import card as prior_card
PAPER='paper-trail-corpus/exampapers/2016/LC098GLP000EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2016/LC098GLP000EV.pdf'
HASHES={PAPER:'23c89d7a9e410e4df2ceff7ea713dda2160513c7619d0ce76bbf71ad534f59a3',SCHEME:'18c3106ebc93d5d23dbe807fd53c5337e31acebea0bf7e6ea3c385c391da55cc'}
REVIEW='scripts/markbank/authoring/home-economics/2016-ol-main-review.json'
def documents():
 for p,h in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 return {k:fitz.open(ROOT/p) for k,p in [('paper',PAPER),('scheme',SCHEME)]}
def card(key,section,ref,topic,prompt,stem,marks,rows,page,notation='',**extra):
 c=prior_card(key,section,ref,topic,prompt,stem,marks,rows,page,notation,**extra)
 c.update(id='he-2016-ol-'+key,year=2016,level='ordinary',questionRef='2016 OL Section '+section+' '+ref)
 c['sourceMaterial']['attribution']='SEC Home Economics 2016 Ordinary Level examination paper — © State Examinations Commission.'
 return c
def write_section(section,cards,review):
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text());ids={c['id'] for c in cards};assert len(ids)==len(cards)
 p.write_text(json.dumps([c for c in data if c['id'] not in ids]+cards,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text())
 if r['status']=='independent-source-census-complete-authoring-pending':r['status']='source-review-in-progress'
 r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],section=section,marks=c['totalMarks'],questionRef=c['questionRef'],topicId=c['topicId']) for c in cards];r['section'+section+'Review']=review;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
def transcript():
 d=documents()['scheme'];full='# SEC Home Economics 2016 Ordinary marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+p.get_text(sort=True) for i,p in enumerate(d))
 # Whole-page extraction interleaves the original tables's columns. Preserve
 # the raw transcript and append independent, coordinate-bounded cell reads.
 for pn in [4,5,6,7,8,10]:
  for i,t in enumerate(d[pn-1].find_tables().tables,1):
   full+=f'\n\n## Physical page {pn}, original table {i}, cell reading order\n\n'+'\n'.join(' | '.join(row).rstrip() for row in table_rows(t,d[pn-1]))
 (ROOT/'examiner-reports/home-economics/schemes/2016-ol.md').write_text(full.rstrip()+'\n')
def body_bottom(page):
 # The 2016 scheme uses bracketed printed page numbers. Keep full page content
 # through the last table border but exclude the actual bottom footer.
 footers=[]
 for block in page.get_text('dict')['blocks']:
  for line in block.get('lines',[]):
   label=tidy(''.join(span['text'] for span in line['spans']))
   if line['bbox'][1]>page.rect.height*.82 and re.fullmatch(r'(?:\[?\d{1,2}\]?|Page \d+ of \d+)',label):footers.append(line['bbox'][1]-2)
 return min(footers) if footers else page.rect.height-20
def text(doc,n):
 # Original visible degree symbols extract as a detached combining ring.
 return tidy(doc[n-1].get_text(clip=fitz.Rect(0,20,doc[n-1].rect.width,body_bottom(doc[n-1])),sort=True)).replace('\u030a','°').replace('\uf0b7','•')
def table_rows(table,page):
 return [[tidy(page.get_text(clip=fitz.Rect(cell),sort=True)).replace('\u030a','°').replace('\uf0b7','•') if cell else '' for cell in row.cells] for row in table.rows]
def a_regions(doc,pages):
 out={}
 for n in pages:
  page=doc[n-1];starts=sorted((int(w[4][:-1]),w[1]-3) for w in page.get_text('words') if re.fullmatch(r'\d+\.',w[4]) and 25<w[0]<85 and w[1]<760)
  for i,(q,top) in enumerate(starts):out[q]=dict(page=n,rect=[20,top,page.rect.width-25,starts[i+1][1] if i+1<len(starts) else body_bottom(page)])
 assert list(out)==list(range(1,13)),out.keys()
 return out
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
 rows[2]=[point(f'carbohydrate-{i}',kind+' — '+sources,note='Give ONE dietary source of this required carbohydrate.') for i,(kind,sources) in enumerate(table_rows(tables[1],d['scheme'][3])[1:],1)]
 rows[3]=[point(f'function-{i}',v,note='Choose ANY TWO functions across both source lists.') for i,v in enumerate(named(select(s[3],'(6)','Name two good dietary sources of Vitamin A.'),['(i)','(ii)']),1)]+[point(f'source-{i}',v,note='Choose ANY TWO dietary sources across both original retinol/beta-carotene pools; no one-per-source-line quota.') for i,v in enumerate(named(select(s[3],'Name two good dietary sources of Vitamin A.'),['(i)','(ii)']),1)]
 rows[4]=[point(f'factor-{i}',v,note='Choose ANY THREE factors from the complete source pool across all three answer lines.') for i,v in enumerate(named(select(s[4],'(6)'),['(i)','(ii)','(iii)']),1)]
 rows[5]=[point(f'nutrient-{i}',v,note='Choose ANY TWO nutrients across both original lists.') for i,v in enumerate(named(select(s[5],'(6)','State one lifestyle change'),['(i)','(ii)']),1)]+[point('lifestyle',select(s[5],'State one lifestyle change that would improve bone health.'),note='Give ONE lifestyle change from the complete original source pool.')]
 model=select(s[6],'In the production',include=True);rows[6]=[point(f'blank-{i}',v,note='Fill the three blanks in their original order. Complete original source sentence: '+model if i==1 else '') for i,v in enumerate(chosen(model,['lactic acid','rennin','curds']),1)]
 tables=d['scheme'][4].find_tables().tables;assert len(tables)==1;rows[7]=truth(table_rows(tables[0],d['scheme'][4]))
 tables=d['scheme'][5].find_tables().tables;assert len(tables)==1;rows[8]=[point(f'class-{i}',kind+' — '+first+' '+second,note='Give ANY TWO examples for EACH of the THREE required classes. Both original example columns form one complete pool; no forced one-per-column quota.') for i,(kind,first,second) in enumerate(table_rows(tables[0],d['scheme'][5])[1:],1)]
 rows[9]=[point('definition',select(s[9],'(6)','Name two compulsory deductions'))]+[point(f'deduction-{i}',v,note='Choose ANY TWO compulsory deductions from the full PAYE/PRSI/USC pool; no compulsory USC choice. Original historical 2016 wording retained.') for i,v in enumerate(named(select(s[9],'Name two compulsory deductions taken from gross pay.'),['(i)','(ii)']),1)]
 rows[10]=[point(f'symbol-{i}',v) for i,v in enumerate(chosen(s[10],['hand wash only','do not bleach']),1)]
 tables=d['scheme'][6].find_tables().tables;assert len(tables)==1;grid=table_rows(tables[0],d['scheme'][6]);rows[11]=[]
 for i,(appliance,element,motor) in enumerate(grid[1:],1):
  assert bool(element)!=bool(motor),(appliance,element,motor)
  rows[11].append(point(f'appliance-{i}',appliance+' — '+grid[0][1 if element else 2]))
 rows[12]=[point(f'source-{i}',v,note='Choose ANY TWO renewable energy sources across both original lists.') for i,v in enumerate(named(select(s[12],'(6)','Explain the benefit'),['(i)','(ii)']),1)]+[point('benefit',select(s[12],'Explain the benefit of renewable energy to the environment.'),note='Explain the environmental benefit using the complete original source guidance.')]
 topics={1:'0-5',2:'0-6',3:'0-8',4:'0-1',5:'0-8',6:'0-9',7:'0-11',8:'0-9',9:'1-1',10:'1-4',11:'1-3',12:'1-5'};figures=[1,2,6,7,8,10,11];cards=[]
 for n in range(1,13):
  prompt=clean(p[n].split('(6)',1)[0]) if n in figures else clean(p[n]);prompt=prompt.replace('\uf0fc','✓')
  rows[n][0]['contextNote']=WHOLE_NOTE+(' '+rows[n][0]['contextNote'] if rows[n][0].get('contextNote') else '')
  c=card(f'sa-q{n}','A',f'Q{n}',topics[n],prompt,'',6,rows[n],pr[n]['page'],tariffModel=dict(kind='questionTotal'))
  if n in figures:c.update(questionFigureKey=f'home-economics-2016-ol-sa-q{n}',questionFigureIncludesPrompt=True)
  cards.append(c)
 assert len(cards)==12 and sum(c['totalMarks'] for c in cards)==72
 return cards
if __name__=='__main__':
 cards=a_build()
 if '--write' in sys.argv:transcript();write_section('A',cards,dict(tasks=12,marks=72,tariffDecision='All twelve whole-six tariffs retain unpriced full source rows, every companion ask, complete cloze/true-false/category/appliance tables and care symbols. No one-per-answer-line quotas or inferred per-row marks.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
