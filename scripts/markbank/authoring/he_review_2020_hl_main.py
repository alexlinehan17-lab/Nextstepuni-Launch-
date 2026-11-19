#!/usr/bin/env python3
"""2020 Higher original-source selections after the independent 90-page sweep."""
import hashlib,json,re,sys
import fitz
from he_review_2011_hl_main import ROOT,tidy,criterion,select,named,point,menu,semis,region,body_bottom,text,clean,without_number,examples,chosen,a_regions,WHOLE_NOTE
from he_review_2011_hl_main import card as prior_card
PAPER_A='paper-trail-corpus/exampapers/2020/LC098ALP014EV.pdf'
PAPER_BC='paper-trail-corpus/exampapers/2020/LC098ALP039EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2020/LC098ALP000EV.pdf'
HASHES={'paper-trail-corpus/exampapers/2020/LC098ALP014EV.pdf': '209d36fc7f5c38698bc1192d71ce5a0d93338022f91b4c58f7c9dcc287c69580', 'paper-trail-corpus/exampapers/2020/LC098ALP039EV.pdf': '7452e4edb380755ddc2d6a92b0c0e06e039283956945f6339fd90845c15d8d7b', 'paper-trail-corpus/markingschemes/2020/LC098ALP000EV.pdf': 'dd443f95fd1de761fe1305598d00ee89649ca13c90cdf878da260a74942d2395'}
REVIEW='scripts/markbank/authoring/home-economics/2020-hl-main-review.json'
def documents():
 for p,h in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 return {k:fitz.open(ROOT/p) for k,p in [('a',PAPER_A),('bc',PAPER_BC),('scheme',SCHEME)]}
def card(key,section,ref,topic,prompt,stem,marks,rows,page,notation='',**extra):
 c=prior_card(key,section,ref,topic,prompt,stem,marks,rows,page,notation,**extra)
 c.update(id='he-2020-hl-'+key,year=2020,level='higher',questionRef='2020 HL Section '+section+' '+ref)
 c['sourceMaterial']['attribution']='SEC Home Economics 2020 Higher Level examination paper — © State Examinations Commission.'
 return c
def write_section(section,cards,review):
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text());ids={c['id'] for c in cards};assert len(ids)==len(cards)
 p.write_text(json.dumps([c for c in data if c['id'] not in ids]+cards,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text())
 if r['status']=='independent-source-census-complete-authoring-pending':r['status']='source-review-in-progress'
 r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],section=section,marks=c['totalMarks'],questionRef=c['questionRef'],topicId=c['topicId']) for c in cards];r['section'+section+'Review']=review;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
def transcript():
 d=documents()['scheme'];full='# SEC Home Economics 2020 Higher marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+p.get_text(sort=True) for i,p in enumerate(d))
 # Whole-page extraction interleaves the original tables's columns. Preserve
 # the raw transcript and append independent, coordinate-bounded cell reads.
 for pn in [5,6,7,13,14]:
  for i,t in enumerate(d[pn-1].find_tables().tables,1):
   full+=f'\n\n## Physical page {pn}, original table {i}, cell reading order\n\n'+'\n'.join(' | '.join(row).rstrip() for row in table_rows(t,d[pn-1]))
 full+='\n\n## Physical page 7, original symbol answer boxes\n\n'+'\n\n'.join(symbol_models(d[6]))
 (ROOT/'examiner-reports/home-economics/schemes/2020-hl.md').write_text(full.rstrip()+'\n')
def body_bottom(page):
 # The redesigned 2020 paper includes page/running boxes above its page
 # number. Exclude every actual footer line, keeping full source content.
 footers=[]
 for block in page.get_text('dict')['blocks']:
  for line in block.get('lines',[]):
   label=tidy(''.join(span['text'] for span in line['spans']))
   footer=bool(re.fullmatch(r'(?:\[?\d{1,2}\]?|Page \d+ of \d+|page|running|previous)',label)) or (label.startswith('Leaving Certificate') and label.endswith('2020')) or (label.startswith('Home Economics') and 'Higher' in label) or label.startswith(('Section A and answerbook','Sections B and C'))
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
def symbol_models(page):
 blocks=[b for b in page.get_text('blocks') if tidy(b[4]).startswith(('Green dot is','Plastic packaging made'))]
 assert len(blocks)==2,blocks
 return [tidy(b[4]) for b in sorted(blocks,key=lambda b:b[1])]
def a_build():
 d=documents();pr=a_regions(d['a'],range(3,7));sr=a_regions(d['scheme'],range(5,9))
 p={n:without_number(region(d['a'],r)) for n,r in pr.items()};s={n:without_number(region(d['scheme'],r)) for n,r in sr.items()};rows={}
 grid=[[v for v in row if v] for row in table_rows(d['scheme'][4].find_tables().tables[0],d['scheme'][4])];assert len(grid)==4 and all(len(row)==3 for row in grid[1:]),grid
 rows[1]=[];groups=[]
 for i,(label,formula,samples) in enumerate(grid[1:],1):
  opts=[x.strip(' .') for x in samples.split(',') if x.strip(' .')]
  rows[1]+=[point(f'formula-{i}',label+' — '+formula,1),menu(f'example-{i}',label+' — Example',1,1,opts,'Choose ONE example from the SAME required carbohydrate class.')]
  groups.append(dict(sourceCardId=f'he-2020-hl-sa-q1-class-{i}',label=label,marks=2,rowIds=[f'formula-{i}',f'example-{i}']))
 body=select(s[2],'1 reference to nutritionally aware, 1 reference to health conscious');models=named(body,['(i)','(ii)'])
 rows[2]=[criterion('nutrition','nutritionally aware',1,[0,2,3],'ONE required reference to nutritional awareness. '+models[0]),criterion('health','health conscious',1,[0,2,3],'ONE required reference to health consciousness. '+models[1])]
 for n,label,count,steps,token in [(3,'functions',2,[0,2,3],'(graded 3:2:0)'),(5,'functions',2,[0,2,3],'(graded 3:2:0)'),(7,'points',3,[0,1,2],'(graded 2:1:0)')]:
  guide=re.sub(r'\((?:i|ii)\)\s*','',select(s[n],token));rows[n]=[criterion('points',label,count,steps,f'Give ANY {count} distinct points across the complete original pool; answer lines do not impose category quotas. '+guide)]
 grid=[[v for v in row if v] for row in table_rows(d['scheme'][5].find_tables().tables[0],d['scheme'][5])];assert len(grid)==4 and all(len(row)==2 for row in grid),grid
 rows[4]=[criterion(f'vitamin-{i}',condition,1,[0,2],'Name ONE vitamin for this required condition. Original 2020 source alternatives are retained exactly: '+vitamins) for i,(condition,vitamins) in enumerate(grid[1:],1)]
 def required(n,labels):
  body=re.sub(r'\((?:i|ii)\)\s*','',select(s[n],'(graded 3:2:0)'))
  return [criterion(f'term-{i}',label.rstrip(':'),1,[0,2,3],model) for i,(label,model) in enumerate(zip(labels,named(body,labels)),1)]
 rows[6]=required(6,['Extractives:','Marinating:'])
 grid=table_rows(d['scheme'][6].find_tables().tables[0],d['scheme'][6]);assert len(grid)==3 and grid[0][0]=='Class/Type',grid
 rows[8]=[];sweet_groups=[]
 for i,(label,samples) in enumerate(grid[1:],1):
  opts=[x.strip(' .') for x in samples.split(',') if x.strip(' .')]
  rows[8]+=[point(f'class-{i}',label,2),menu(f'sample-{i}','Example',1,1,opts,'Give ONE example matching the SAME sweetener class: '+label+'.')]
  sweet_groups.append(dict(sourceCardId=f'he-2020-hl-sa-q8-class-{i}',label=label,marks=3,rowIds=[f'class-{i}',f'sample-{i}']))
 # Read the original two answer cells by geometry, avoiding image-caption
 # interleaving in the full-page text layer.
 cells=symbol_models(d['scheme'][6])
 rows[9]=[criterion(f'symbol-{i}',label,1,[0,2,3],model) for i,(label,model) in enumerate(zip(['Green dot','Plastic packaging made from polyethylene terephthalate (PET)'],cells),1)]
 rows[10]=required(10,['Enzymes:','Surfactants:'])
 rows[11]=required(11,['Fixed rate:','Variable rate:'])
 rows[11][1]['contextNote']='Explain the requested variable rate. The source also prints loan-to-value and tracker notes, retained here as supplementary guidance without extra required claims. '+rows[11][1]['contextNote']
 rows[12]=required(12,['Product placement:','Loyalty schemes:'])
 topics={1:'0-6',2:'0-1',3:'0-7',4:'0-8',5:'0-11',6:'0-3',7:'0-9',8:'0-11',9:'1-5',10:'1-4',11:'1-1',12:'1-2'};cards=[]
 for n in range(1,13):
  prompt=clean(p[n]);extra={}
  if n in [1,4,8,9]:
   end={1:'Chemical Formula',4:'Health Condition',8:'Class/Type',9:'(www.repak.ie)'}[n];assert end in prompt,(n,prompt);prompt=prompt.split(end,1)[0].strip();extra.update(questionFigureKey=f'home-economics-2020-hl-sa-q{n}',questionFigureIncludesPrompt=True)
  if n==1:extra['taskGroups']=groups
  if n==8:extra['taskGroups']=sweet_groups
  cards.append(card(f'sa-q{n}','A',f'Q{n}',topics[n],prompt,'',6,rows[n],pr[n]['page'],'Original component allocations and exact partial-credit ladders',**extra))
 assert len(cards)==12 and sum(c['totalMarks'] for c in cards)==72
 return cards
if __name__=='__main__':
 cards=a_build()
 if '--write' in sys.argv:transcript();write_section('A',cards,dict(tasks=12,marks=72,tariffDecision='All required formula/example cells, nutrition/health category quota, complete vitamin/sweetener/symbol pools, exact original partial steps and required paired terms. Original extra mortgage guidance remains supplementary.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
