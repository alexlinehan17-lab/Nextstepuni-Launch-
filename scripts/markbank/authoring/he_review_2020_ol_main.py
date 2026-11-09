#!/usr/bin/env python3
"""2020 Ordinary original-source selections after the independent 78-page sweep."""
import hashlib,json,re,sys
import fitz
from he_review_2011_hl_main import ROOT,tidy,criterion,select,named,point,menu,semis,region,body_bottom,text,clean,without_number,examples,chosen,a_regions,WHOLE_NOTE
from he_review_2011_hl_main import card as prior_card
PAPER_A='paper-trail-corpus/exampapers/2020/LC098GLP014EV.pdf'
PAPER_BC='paper-trail-corpus/exampapers/2020/LC098GLP039EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2020/LC098GLP000EV.pdf'
HASHES={'paper-trail-corpus/exampapers/2020/LC098GLP014EV.pdf': 'c25745702775fc93d7fc789b5d19aa39f38bfa45a94d3df875aef941154a37f0', 'paper-trail-corpus/exampapers/2020/LC098GLP039EV.pdf': '22863d489e51c88ec07912670032002f18e0d8a32013833d954766c82c08d013', 'paper-trail-corpus/markingschemes/2020/LC098GLP000EV.pdf': 'df16abbeb05005a72c051315b2addb88ffa08d5abcb890ff2ed5e83d53a411b7'}
REVIEW='scripts/markbank/authoring/home-economics/2020-ol-main-review.json'
def documents():
 for p,h in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 return {k:fitz.open(ROOT/p) for k,p in [('a',PAPER_A),('bc',PAPER_BC),('scheme',SCHEME)]}
def card(key,section,ref,topic,prompt,stem,marks,rows,page,notation='',**extra):
 c=prior_card(key,section,ref,topic,prompt,stem,marks,rows,page,notation,**extra)
 c.update(id='he-2020-ol-'+key,year=2020,level='ordinary',questionRef='2020 OL Section '+section+' '+ref)
 c['sourceMaterial']['attribution']='SEC Home Economics 2020 Ordinary Level examination paper — © State Examinations Commission.'
 return c
def write_section(section,cards,review):
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text());ids={c['id'] for c in cards};assert len(ids)==len(cards)
 p.write_text(json.dumps([c for c in data if c['id'] not in ids]+cards,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text())
 if r['status']=='independent-source-census-complete-authoring-pending':r['status']='source-review-in-progress'
 r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],section=section,marks=c['totalMarks'],questionRef=c['questionRef'],topicId=c['topicId']) for c in cards];r['section'+section+'Review']=review;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
def transcript():
 d=documents()['scheme'];full='# SEC Home Economics 2020 Ordinary marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+p.get_text(sort=True) for i,p in enumerate(d))
 for pn in [4,5,6,7,10]:
  for i,t in enumerate(d[pn-1].find_tables().tables,1):
   full+=f'\n\n## Physical page {pn}, original table {i}, cell reading order\n\n'+'\n'.join(' | '.join(row).rstrip() for row in table_rows(t,d[pn-1]))
 (ROOT/'examiner-reports/home-economics/schemes/2020-ol.md').write_text(full.rstrip()+'\n')
def body_bottom(page):
 # The redesigned 2020 paper includes page/running boxes above its page
 # number. Exclude every actual footer line, keeping full source content.
 footers=[]
 for block in page.get_text('dict')['blocks']:
  for line in block.get('lines',[]):
   label=tidy(''.join(span['text'] for span in line['spans']))
   footer=bool(re.fullmatch(r'(?:\[?\d{1,2}\]?|Page \d+ of \d+|page|running|previous)',label)) or (label.startswith('Leaving Certificate') and label.endswith('2020')) or (label.startswith('Home Economics') and 'Ordinary' in label) or label.startswith(('Section A and answerbook','Sections B and C'))
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
 d=documents();pr=a_regions(d['a'],range(3,7));sr=a_regions(d['scheme'],range(4,8))
 p={n:without_number(region(d['a'],r)) for n,r in pr.items()};s={n:without_number(region(d['scheme'],r)) for n,r in sr.items()};rows={};cards=[]
 def truth(page,table):
  # Decorative grid lines create spurious empty columns. Read each original
  # statement row by geometry and match its visible tick to the header centre.
  words=page.get_text('words');head=table.rows[0];top=min(c[1] for c in head.cells if c);bottom=max(c[3] for c in head.cells if c)
  headers={w[4]:(w[0]+w[2])/2 for w in words if w[4] in ['True','False'] and top<=w[1]<bottom};assert set(headers)=={'True','False'},headers
  out=[]
  for i,row in enumerate(table.rows[1:],1):
   low=min(c[1] for c in row.cells if c);high=max(c[3] for c in row.cells if c)
   content=table_rows(table,page)[i];statement=next(v for v in content if v and v!='\uf0fc')
   ticks=[w for w in words if w[4]=='\uf0fc' and low<=w[1]<high];assert len(ticks)==1,ticks
   x=(ticks[0][0]+ticks[0][2])/2;answer=min(headers,key=lambda h:abs(headers[h]-x))
   out.append(point(f'statement-{i}',statement+' — '+answer,2,note='The original visible tick position determines the answer; each statement is 2 or 0 marks.'))
  return out
 rows[1]=truth(d['scheme'][3],d['scheme'][3].find_tables().tables[0])
 body=re.sub(r'\((?:i|ii)\)\s*','',select(s[2],'(graded 3:2:0)'))
 rows[2]=[criterion(f'term-{i}',label.rstrip(':'),1,[0,2,3],model) for i,(label,model) in enumerate(zip(['Smoke point:','Flash point:'],named(body,['Smoke point:','Flash point:'])),1)]
 body=select(s[3],'Milk is',include=True)
 rows[3]=[point(f'blank-{i}',v,2,note='Fill the three original blanks in order, using the printed word pool; each is 2 or 0 marks.') for i,v in enumerate(named(body,['Milk is','The process','Spray drying']),1)]
 grid=[[v for v in row if v] for row in table_rows(d['scheme'][4].find_tables().tables[0],d['scheme'][4])];assert len(grid)==3,grid
 full=' | '.join('Culinary uses: '+a+' Food/dish: '+b for a,b in grid[1:])
 rows[4]=[criterion('uses','Culinary uses of eggs',2,[0,1],'Name ANY TWO different uses. Preserve the complete original grouped table; no one-per-row quota or invented one-to-one key. '+full),criterion('dishes','Food/dish',2,[0,2],'Give ONE matching food/dish for EACH of the SAME TWO selected uses. Complete grouped source pool: '+full)]
 rows[5]=truth(d['scheme'][4],d['scheme'][4].find_tables().tables[1])
 grid=[[v for v in row if v] for row in table_rows(d['scheme'][5].find_tables().tables[0],d['scheme'][5])];assert len(grid)==4,grid
 rows[7]=[criterion(f'effect-{i}',condition,1,[0,2],'Give an effect for this REQUIRED dietary condition. Full original guidance: '+guide) for i,(condition,guide) in enumerate(grid[1:],1)]
 rows[9]=truth(d['scheme'][5],d['scheme'][5].find_tables().tables[-1])
 rows[11]=[criterion('factors','Factors',3,[0,1,2],'Choose ANY THREE distinct factors across the complete pool; no answer-line quotas. '+re.sub(r'\((?:i|ii|iii)\)\s*','',select(s[11],'(graded 2:1:0)')))]
 # The two text boxes are the exact original labels beside the source symbols.
 labels=['Line dry','Do not dry clean']
 assert all(label in s[12] for label in labels)
 rows[12]=[criterion(f'symbol-{i}',label,1,[0,2,3],'Original source answer: '+label+'.') for i,label in enumerate(labels,1)]
 topics={1:'0-6',2:'0-7',3:'0-9',4:'0-3',5:'0-3',6:'0-11',7:'0-1',8:'0-11',9:'1-1',10:'1-2',11:'3-3',12:'1-4'}
 for n in range(1,13):
  if n in [6,8,10]:
   split={6:'Name two food additives',8:'List two career opportunities',10:'Name one method'}[n];prompts=[clean(p[n].split(split,1)[0]),clean(split+p[n].split(split,1)[1])]
   if n==6:
    first=select(s[n],'(graded 2:1:0)','Name two food additives');second=select(select(s[n],'Name two food additives'),'(graded 2:0)')
    tasks=[('definition',2,[criterion('definition','Food additive',1,[0,1,2],first)]),('additives',4,[criterion('additives','Food additives',2,[0,2],'ANY TWO different additives across the complete original pool: '+re.sub(r'\((?:i|ii)\)\s*','',second))])]
   elif n==8:
    first=select(s[n],'(graded 2:0)','List two career opportunities');second=select(s[n],'(graded 1:0)')
    tasks=[('foods',4,[criterion('foods','Foods exported from Ireland',2,[0,2],'ANY TWO different foods across the complete pool: '+re.sub(r'\((?:i|ii)\)\s*','',first))]),('careers',2,[criterion('careers','Career opportunities',2,[0,1],'ANY TWO different careers across the complete pool: '+re.sub(r'\((?:i|ii)\)\s*','',second))])]
   else:
    first=select(s[n],'(graded 2:1:0)','Name one method');second=select(s[n],'(graded 2:0)')
    tasks=[('advantages',4,[criterion('advantages','Advantages',2,[0,1,2],'ANY TWO different advantages across both source lines: '+re.sub(r'\((?:i|ii)\)\s*','',first))]),('payment',2,[criterion('payment','method',1,[0,2],second)])]
   for prompt,(suffix,marks,rs) in zip(prompts,tasks):cards.append(card(f'sa-q{n}-{suffix}','A',f'Q{n} — {suffix}',topics[n],prompt,'',marks,rs,pr[n]['page'],'Separately printed and priced companion ask; exact original steps'))
   continue
  prompt=clean(p[n]).replace('\uf0fc','✓');extra={}
  if n in [1,3,4,5,7,9,12]:
   stop={1:'True',3:'spray drying',4:'Culinary use',5:'True',7:'Effect on',9:'True',12:'(www.goodhousekeeping.com)'}[n]
   if stop in prompt:prompt=prompt.split(stop,1)[0].strip()
   extra.update(questionFigureKey=f'home-economics-2020-ol-sa-q{n}',questionFigureIncludesPrompt=True)
  cards.append(card(f'sa-q{n}','A',f'Q{n}',topics[n],prompt,'',6,rows[n],pr[n]['page'],'Original component allocations and exact partial-credit ladders',**extra))
 assert len(cards)==15 and sum(c['totalMarks'] for c in cards)==72
 return cards
if __name__=='__main__':
 cards=a_build()
 if '--write' in sys.argv:transcript();write_section('A',cards,dict(tasks=15,marks=72,tariffDecision='All required named definitions and exact original partial ladders, complete truth/cloze/effect/symbol inputs, coherent egg use/dish selections without invented pairing keys, and three separately printed and priced companion asks.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
