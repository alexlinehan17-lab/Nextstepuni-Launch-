#!/usr/bin/env python3
"""2018 Ordinary original-source selections after the independent 44-page sweep."""
import hashlib,json,re,sys
import fitz
from he_review_2011_hl_main import ROOT,tidy,criterion,select,named,point,menu,semis,region,body_bottom,text,clean,without_number,examples,chosen,a_regions,WHOLE_NOTE
from he_review_2011_hl_main import card as prior_card
PAPER='paper-trail-corpus/exampapers/2018/LC098GLP000EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2018/LC098GLP000EV.pdf'
HASHES={PAPER:'8d04d3858090b7db4c13222c2e806d11b719b40783c428bc3490e010ab5902c9',SCHEME:'a4bd923c2c0e8b37427b4ff7a99a23347f5eefc9e829631a1b28d3e0371a79fd'}
REVIEW='scripts/markbank/authoring/home-economics/2018-ol-main-review.json'
def documents():
 for p,h in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 return {k:fitz.open(ROOT/p) for k,p in [('paper',PAPER),('scheme',SCHEME)]}
def card(key,section,ref,topic,prompt,stem,marks,rows,page,notation='',**extra):
 c=prior_card(key,section,ref,topic,prompt,stem,marks,rows,page,notation,**extra)
 c.update(id='he-2018-ol-'+key,year=2018,level='ordinary',questionRef='2018 OL Section '+section+' '+ref)
 c['sourceMaterial']['attribution']='SEC Home Economics 2018 Ordinary Level examination paper — © State Examinations Commission.'
 return c
def write_section(section,cards,review):
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text());ids={c['id'] for c in cards};assert len(ids)==len(cards)
 p.write_text(json.dumps([c for c in data if c['id'] not in ids]+cards,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text())
 if r['status']=='independent-source-census-complete-authoring-pending':r['status']='source-review-in-progress'
 r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],section=section,marks=c['totalMarks'],questionRef=c['questionRef'],topicId=c['topicId']) for c in cards];r['section'+section+'Review']=review;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
def transcript():
 d=documents()['scheme'];full='# SEC Home Economics 2018 Ordinary marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+p.get_text(sort=True) for i,p in enumerate(d))
 # Whole-page extraction interleaves the original tables's columns. Preserve
 # the raw transcript and append independent, coordinate-bounded cell reads.
 for pn in [4,5,6,8]:
  for i,t in enumerate(d[pn-1].find_tables().tables,1):
   full+=f'\n\n## Physical page {pn}, original table {i}, cell reading order\n\n'+'\n'.join(' | '.join(row).rstrip() for row in table_rows(t,d[pn-1]))
 (ROOT/'examiner-reports/home-economics/schemes/2018-ol.md').write_text(full.rstrip()+'\n')
def body_bottom(page):
 # The redesigned 2018 paper includes page/running boxes above its page
 # number. Exclude every actual footer line, keeping full source content.
 footers=[]
 for block in page.get_text('dict')['blocks']:
  for line in block.get('lines',[]):
   label=tidy(''.join(span['text'] for span in line['spans']))
   footer=bool(re.fullmatch(r'(?:\[?\d{1,2}\]?|Page \d+ of \d+|page|running)',label)) or (label.startswith('Leaving Certificate') and label.endswith('2018')) or (label.startswith('Home Economics') and 'Ordinary Level' in label)
   if line['bbox'][1]>page.rect.height*.82 and footer:footers.append(line['bbox'][1]-2)
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
   assert bool(yes)!=bool(no);assert (yes or no)=='9'
   result.append(point(f'statement-{i}',statement+' — '+grid[0][1 if yes else 2],note='The original visible tick position determines True/False; its text-layer glyph extracts as9.'))
  return result
 rows[1]=truth(table_rows(d['scheme'][3].find_tables().tables[0],d['scheme'][3]))
 full=select(s[2],'The primary function',include=True);rows[2]=[point(f'blank-{i}',v,note='Fill the three blanks in their original order. Complete original source: '+full) for i,v in enumerate(chosen(full,['vitamin K','Vitamin B','folic acid']),1)]
 rows[3]=[point(f'way-{i}',v,note='Outline ANY TWO effects of finance using the full original source pool; no fixed higher/lower-income quota.') for i,v in enumerate(named(select(s[3],'(6)'),['(i)','(ii)']),1)]
 rows[4]=[point(f'pair-{i}',food+' — '+source) for i,(food,source) in enumerate(table_rows(d['scheme'][4].find_tables().tables[0],d['scheme'][4])[1:],1)]
 rows[5]=[point(f'problem-{i}',v,note='Identify ANY THREE problems across all original answer lines; no one-per-line quota.') for i,v in enumerate(named(select(s[5],'(6)'),['(i)','(ii)','(iii)']),1)]
 rows[6]=[point(f'heading-{i}',v,note='Explain this required heading. Original2018 source wording and temperatures retained.') for i,v in enumerate(named(select(s[6],'(6)'),['Food storage:','Personal hygiene:','Reheating procedures:']),1)]
 rows[7]=truth(table_rows(d['scheme'][5].find_tables().tables[0],d['scheme'][5]))
 full=select(s[8],'Cheese and yoghurt',include=True);rows[8]=[point(f'blank-{i}',v,note='The original scheme accepts Enzymes/yeast for the second blank. Retain both alternatives even though yeast also completes the third statement.' if i==2 else '') for i,v in enumerate(named(full,['Cheese and yoghurt','Enzymes/yeast','The biological raising agent']),1)]
 rows[9]=[point(f'step-{i}',v,note='Outline ANY THREE budget-planning steps across all original answer lines.') for i,v in enumerate(named(select(s[9],'(6)'),['(i)','(ii)','(iii)']),1)]
 rows[10]=[point(f'credit-{i}',v) for i,v in enumerate(named(select(s[10],'Advantage:','Name two types',True),['Advantage:','Disadvantage:']),1)]+[point(f'type-{i}',v,note='Also name ANY TWO car-credit types across both complete original source pools.') for i,v in enumerate(named(select(s[10],'Name two types of credit available to consumers when buying a car.'),['(i)','(ii)']),1)]
 rows[11]=[point('symbol-1',select(s[11],'Hot Iron','Drip dry',True)),point('symbol-2',select(s[11],'Drip dry',include=True))]
 rows[12]=[point(f'way-{i}',v,note='State ANY THREE ways technology increases efficiency from all original source lines; no one-per-line quota.') for i,v in enumerate(named(select(s[12],'(6)'),['(i)','(ii)','(iii)']),1)]
 topics={1:'0-8',2:'0-8',3:'0-10',4:'0-7',5:'0-1',6:'0-4',7:'0-4',8:'0-4',9:'1-1',10:'1-1',11:'1-4',12:'1-3'};figures=[1,2,4,7,8,11];cards=[]
 for n in range(1,13):
  prompt=clean(p[n].split('(6)',1)[0]) if n in figures else clean(p[n]);prompt=prompt.replace('\uf0fc','✓');rows[n][0]['contextNote']=WHOLE_NOTE+(' '+rows[n][0]['contextNote'] if rows[n][0].get('contextNote') else '')
  c=card(f'sa-q{n}','A',f'Q{n}',topics[n],prompt,'',6,rows[n],pr[n]['page'],tariffModel=dict(kind='questionTotal'))
  if n in figures:c.update(questionFigureKey=f'home-economics-2018-ol-sa-q{n}',questionFigureIncludesPrompt=True)
  cards.append(c)
 assert len(cards)==12 and sum(c['totalMarks'] for c in cards)==72
 return cards
if __name__=='__main__':
 cards=a_build()
 if '--write' in sys.argv:transcript();write_section('A',cards,dict(tasks=12,marks=72,tariffDecision='Whole-six original tasks preserve all companion asks, complete truth/false tick positions, cloze alternatives including Enzymes/yeast, full safe-food guidance, credit comparison AND both car-credit names, both textile symbols and unrestricted answer-line pools. No invented per-answer allocation.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
