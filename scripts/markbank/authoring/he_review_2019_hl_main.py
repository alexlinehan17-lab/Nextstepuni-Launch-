#!/usr/bin/env python3
"""2019 Higher original-source selections after the independent 48-page sweep."""
import hashlib,json,re,sys
import fitz
from he_review_2011_hl_main import ROOT,tidy,criterion,select,named,point,menu,semis,region,body_bottom,text,clean,without_number,examples,chosen,a_regions,WHOLE_NOTE
from he_review_2011_hl_main import card as prior_card
PAPER='paper-trail-corpus/exampapers/2019/LC098ALP000EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2019/LC098ALP000EV.pdf'
HASHES={PAPER:'60700cd2f6f12a62480dbf8d3263c04d8131fea98817d5d0a3148cb9b5ad5990',SCHEME:'c427e9c129a5c14f32444e68fc44b3b67fbe520f91b49f4da5d4a22413fd7699'}
REVIEW='scripts/markbank/authoring/home-economics/2019-hl-main-review.json'
def documents():
 for p,h in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 return {k:fitz.open(ROOT/p) for k,p in [('paper',PAPER),('scheme',SCHEME)]}
def card(key,section,ref,topic,prompt,stem,marks,rows,page,notation='',**extra):
 c=prior_card(key,section,ref,topic,prompt,stem,marks,rows,page,notation,**extra)
 c.update(id='he-2019-hl-'+key,year=2019,level='higher',questionRef='2019 HL Section '+section+' '+ref)
 c['sourceMaterial']['attribution']='SEC Home Economics 2019 Higher Level examination paper — © State Examinations Commission.'
 return c
def write_section(section,cards,review):
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text());ids={c['id'] for c in cards};assert len(ids)==len(cards)
 p.write_text(json.dumps([c for c in data if c['id'] not in ids]+cards,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text())
 if r['status']=='independent-source-census-complete-authoring-pending':r['status']='source-review-in-progress'
 r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],section=section,marks=c['totalMarks'],questionRef=c['questionRef'],topicId=c['topicId']) for c in cards];r['section'+section+'Review']=review;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
def transcript():
 d=documents()['scheme'];full='# SEC Home Economics 2019 Higher marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+p.get_text(sort=True) for i,p in enumerate(d))
 # Whole-page extraction interleaves the original tables's columns. Preserve
 # the raw transcript and append independent, coordinate-bounded cell reads.
 for pn in [4,13]:
  for i,t in enumerate(d[pn-1].find_tables().tables,1):
   full+=f'\n\n## Physical page {pn}, original table {i}, cell reading order\n\n'+'\n'.join(' | '.join(row).rstrip() for row in table_rows(t,d[pn-1]))
 (ROOT/'examiner-reports/home-economics/schemes/2019-hl.md').write_text(full.rstrip()+'\n')
def body_bottom(page):
 # The redesigned 2019 paper includes page/running boxes above its page
 # number. Exclude every actual footer line, keeping full source content.
 footers=[]
 for block in page.get_text('dict')['blocks']:
  for line in block.get('lines',[]):
   label=tidy(''.join(span['text'] for span in line['spans']))
   footer=bool(re.fullmatch(r'(?:\[?\d{1,2}\]?|Page \d+ of \d+|page|running|previous)',label)) or (label.startswith('Leaving Certificate') and label.endswith('2019')) or (label.startswith('Home Economics') and 'Higher Level' in label)
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
 def required(n,labels,steps):
  models=named(select(s[n],'(6)'),labels);out=[]
  for i,(label,model) in enumerate(zip(labels,models),1):
   guidance=re.sub(r'^'+re.escape(label)+r'\s*3\s*marks\s*\(graded [\d:]+\)\s*','',model)
   out.append(criterion(f'account-{i}',label,1,steps,guidance))
  return out
 rows[1]=required(1,['Hydrogenation','Plasticity'],[0,1,2,3])
 rows[4]=required(4,['Organic','Lecithin'],[0,2,3])
 rows[5]=required(5,['Cold smoking','Hot smoking'],[0,2,3])
 rows[6]=required(6,['Physical change','Chemical change'],[0,2,3])
 rows[8]=required(8,['Type1: Insulin dependent','Type 2: Non-insulin dependent'],[0,2,3])
 for row in rows[8]:row['contextNote']='The original 2019 scheme wording is reproduced for this examination task. '+row['contextNote']
 rows[10]=required(10,['Magnetron','Transformer'],[0,2,3])
 rows[10][1]['contextNote']='The original scheme describes the transformer as increasing voltage to a “higher frequency”; that source wording is reproduced here. '+rows[10][1]['contextNote']
 for n,label,count,steps,token in [(2,'Meal planning guidelines',3,[0,1,2],'(graded 2:1:0)'),(7,'Biological functions',3,[0,2],'(graded 2:0)'),(9,'Statutory bodies',3,[0,1,2],'(graded 2:1:0)'),(12,'points',2,[0,2,3],'(graded 3:2:0)')]:
  guide=re.sub(r'\((?:i|ii|iii)\)\s*','',select(s[n],token))
  rows[n]=[criterion('points',label,count,steps,f'Choose ANY {count} responses across the complete original pool; answer lines do not impose separate category quotas. '+guide)]
 grid=table_rows(d['scheme'][3].find_tables().tables[0],d['scheme'][3]);assert len(grid)==4
 rows[3]=[criterion(f'mineral-{i}',condition,1,[0,2],'Name ONE mineral for this required condition. Complete original alternatives: '+minerals) for i,(condition,minerals) in enumerate(grid[1:],1)]
 rows[11]=[]
 for i,full in enumerate(named(select(s[11],'(6)'),['Renewable resource','Non-renewable resource']),1):
  label=['Renewable resource','Non-renewable resource'][i-1]
  rows[11]+=[criterion(f'resource-{i}',label,1,[0,1,2],select(full,'(graded 2:1:0)','Example')),criterion(f'example-{i}','Example',1,[0,1],'Give ONE example matching '+label.lower()+'. Complete original pool: '+select(full,'(graded 1:0)'))]
 topics={1:'0-7',2:'0-1',3:'0-8',4:'0-9',5:'0-4',6:'0-3',7:'0-8',8:'0-1',9:'1-2',10:'1-3',11:'1-5',12:'1-5'};cards=[]
 for n in range(1,13):
  prompt=clean(p[n].split('(6)',1)[0]) if n==3 else clean(p[n])
  c=card(f'sa-q{n}','A',f'Q{n}',topics[n],prompt,'',6,rows[n],pr[n]['page'],'Original printed component allocations and partial-credit ladders')
  if n==3:c.update(questionFigureKey='home-economics-2019-hl-sa-q3',questionFigureIncludesPrompt=True)
  cards.append(c)
 assert len(cards)==12 and sum(c['totalMarks'] for c in cards)==72
 return cards
if __name__=='__main__':
 cards=a_build()
 if '--write' in sys.argv:transcript();write_section('A',cards,dict(tasks=12,marks=72,tariffDecision='Original component tariffs and exact partial-credit steps, unrestricted answer-line pools, all three mineral-condition matches, both resource definitions with matching examples. Original diabetes and transformer wording identified visibly.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
