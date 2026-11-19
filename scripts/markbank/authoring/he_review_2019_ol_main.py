#!/usr/bin/env python3
"""2019 Ordinary original-source selections after the independent 48-page sweep."""
import hashlib,json,re,sys
import fitz
from he_review_2011_hl_main import ROOT,tidy,criterion,select,named,point,menu,semis,region,body_bottom,text,clean,without_number,examples,chosen,a_regions,WHOLE_NOTE
from he_review_2011_hl_main import card as prior_card
PAPER='paper-trail-corpus/exampapers/2019/LC098GLP000EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2019/LC098GLP000EV.pdf'
HASHES={PAPER:'d123a4b468df8896744d4c44bf30ebbb5af770087cb879e84e79de8d3e2cde3c',SCHEME:'8f99827fd5eb3027deeead7fa3630f4e37ee6939d9cae1eb195e0c4580ec4b0e'}
REVIEW='scripts/markbank/authoring/home-economics/2019-ol-main-review.json'
def documents():
 for p,h in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 return {k:fitz.open(ROOT/p) for k,p in [('paper',PAPER),('scheme',SCHEME)]}
def card(key,section,ref,topic,prompt,stem,marks,rows,page,notation='',**extra):
 c=prior_card(key,section,ref,topic,prompt,stem,marks,rows,page,notation,**extra)
 c.update(id='he-2019-ol-'+key,year=2019,level='ordinary',questionRef='2019 OL Section '+section+' '+ref)
 c['sourceMaterial']['attribution']='SEC Home Economics 2019 Ordinary Level examination paper — © State Examinations Commission.'
 return c
def write_section(section,cards,review):
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text());ids={c['id'] for c in cards};assert len(ids)==len(cards)
 p.write_text(json.dumps([c for c in data if c['id'] not in ids]+cards,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text())
 if r['status']=='independent-source-census-complete-authoring-pending':r['status']='source-review-in-progress'
 r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],section=section,marks=c['totalMarks'],questionRef=c['questionRef'],topicId=c['topicId']) for c in cards];r['section'+section+'Review']=review;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
def transcript():
 d=documents()['scheme'];full='# SEC Home Economics 2019 Ordinary marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+p.get_text(sort=True) for i,p in enumerate(d))
 # Whole-page extraction interleaves the original tables's columns. Preserve
 # the raw transcript and append independent, coordinate-bounded cell reads.
 for pn in [4,5,6,8,10]:
  for i,t in enumerate(d[pn-1].find_tables().tables,1):
   full+=f'\n\n## Physical page {pn}, original table {i}, cell reading order\n\n'+'\n'.join(' | '.join(row).rstrip() for row in table_rows(t,d[pn-1]))
 (ROOT/'examiner-reports/home-economics/schemes/2019-ol.md').write_text(full.rstrip()+'\n')
def body_bottom(page):
 # The redesigned 2019 paper includes page/running boxes above its page
 # number. Exclude every actual footer line, keeping full source content.
 footers=[]
 for block in page.get_text('dict')['blocks']:
  for line in block.get('lines',[]):
   label=tidy(''.join(span['text'] for span in line['spans']))
   footer=bool(re.fullmatch(r'(?:\[?\d{1,2}\]?|Page \d+ of \d+|page|running|previous)',label)) or (label.startswith('Leaving Certificate') and label.endswith('2019')) or (label.startswith('Home Economics') and 'Ordinary Level' in label)
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
   assert bool(yes)!=bool(no);assert (yes or no)=='\uf0fc'
   result.append(point(f'statement-{i}',statement+' — '+grid[0][1 if yes else 2],2,note='The original visible tick position determines the answer; each statement is 2 or 0 marks.'))
  return result
 rows[1]=truth(table_rows(d['scheme'][3].find_tables().tables[0],d['scheme'][3]))
 full=select(s[2],'A deficiency',include=True);rows[2]=[point(f'blank-{i}',v,2,note='Fill the three original blanks in order; each is 2 or 0 marks.') for i,v in enumerate(named(full,['A deficiency','Vitamin C','Vitamin A']),1)]
 definition=select(s[3],'Coagulation:','Name two different dishes');dishes=select(s[3],'Dishes:')
 rows[3]=[criterion('coagulation','Coagulation',1,[0,1,2],select(definition,'(graded 2:1:0)')),criterion('dishes','Dishes',2,[0,1,2],'Choose ANY TWO different dishes across both source lines; no one-per-line quota. '+re.sub(r'\((?:i|ii)\)\s*','',select(dishes,'(graded 2:1:0)')))]
 for n,label in [(4,'Changes in eating patterns'),(6,'Dietary guidelines')]:rows[n]=[criterion('points',label,3,[0,2],'Choose ANY THREE across the complete source pool; no forced answer-line quota. '+re.sub(r'\((?:i|ii|iii)\)\s*','',select(s[n],'(graded 2:0)')))]
 grid=table_rows(d['scheme'][4].find_tables().tables[0],d['scheme'][4]);assert len(grid)==7
 rows[5]=[criterion(f'class-{i}',grid[index][0],2,[0,1],'Name ANY TWO different fruits in this REQUIRED class. Complete original pool: '+re.sub(r'\b[12]\.\s*','',grid[index][1]+' '+grid[index+1][1])) for i,index in enumerate([1,3,5],1)]
 grid=table_rows(d['scheme'][5].find_tables().tables[0],d['scheme'][5]);assert len(grid)==3
 full=' | '.join('Types of pastry: '+types+' Suitable dishes: '+dishes for types,dishes in grid[1:])
 rows[7]=[criterion('types','Types of Pastry',2,[0,2],'Name TWO different pastry types. Both complete original grouped choice pools are retained: '+full),criterion('dishes','Dish',2,[0,1],'Give ONE suitable dish matching EACH of the SAME TWO selected pastry types. The original table groups several types and dishes; no one-to-one answer key has been invented. '+full)]
 rows[8]=truth(table_rows(d['scheme'][5].find_tables().tables[1],d['scheme'][5]))
 full=select(s[9],'Fabric conditioners',include=True);rows[9]=[point(f'blank-{i}',v,2,note='Fill the original blanks in order; each is 2 or 0 marks.') for i,v in enumerate(named(full,['Fabric conditioners','Wool fabric','Proban is']),1)]
 first=select(s[10],'Factors:','Name one saving scheme');rows[10]=[criterion('factors','Factors',2,[0,1,2],'Choose ANY TWO factors from the full pool: '+re.sub(r'\((?:i|ii)\)\s*','',select(first,'(graded 2:1:0)'))),criterion('scheme','Saving scheme',1,[0,1,2],'Name ONE savings scheme from the full original historical 2019 pool: '+select(select(s[10],'Saving scheme:'),'(graded 2:1:0)'))]
 full=select(s[11],'(graded 3:2:0)');rows[11]=[criterion(f'term-{i}',label,1,[0,2,3],select(model,label)) for i,(label,model) in enumerate(zip(['Gross Income','Net Income'],named(full,['(i) Gross Income','(ii) Net Income'])),1)]
 full=select(s[12],'(graded 3:2:0)');rows[12]=[criterion(f'symbol-{i}',label,1,[0,2,3],'Original 2019 source wording: '+model) for i,(label,model) in enumerate(zip(['Universal recycling symbol','European Union eco label'],named(full,['Universal recycling symbol;','European Union eco label;'])),1)]
 topics={1:'0-8',2:'0-8',3:'0-5',4:'0-10',5:'0-9',6:'0-1',7:'0-3',8:'0-3',9:'1-4',10:'1-1',11:'1-1',12:'1-5'};figures=[1,2,5,7,8,9,12];cards=[]
 for n in range(1,13):
  prompt=clean(p[n].split('(6)',1)[0]) if n in figures else clean(p[n]);prompt=prompt.replace('\uf0fc','✓')
  c=card(f'sa-q{n}','A',f'Q{n}',topics[n],prompt,'',6,rows[n],pr[n]['page'],'Original component allocations and printed partial-credit steps')
  if n in figures:c.update(questionFigureKey=f'home-economics-2019-ol-sa-q{n}',questionFigureIncludesPrompt=True)
  cards.append(c)
 assert len(cards)==12 and sum(c['totalMarks'] for c in cards)==72
 return cards
if __name__=='__main__':
 cards=a_build()
 if '--write' in sys.argv:transcript();write_section('A',cards,dict(tasks=12,marks=72,tariffDecision='Exact original component allocations and partial steps; both complete truth tables, cloze pools, two fruits per required class, coherent pastry/dish choices without an invented key, coagulation plus two dishes, saving factors plus scheme, and both income definitions/symbols.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
