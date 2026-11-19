#!/usr/bin/env python3
"""2011 Higher source selections following the independent 44-page visual census."""
import hashlib,json,re,sys
import fitz
from he_review_2010_hl_main import ROOT,tidy,criterion,select,named,point,menu,semis,region,WHOLE_NOTE
from he_review_2010_hl_main import card as prior_card
from he_review_2010_ol_main import clean,without_number,examples,chosen
PAPER='paper-trail-corpus/exampapers/2011/LC098ALP000EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2011/LC098ALP000EV.PDF'
HASHES={PAPER:'4acfe59d0dc12db9f1b745b2fd1f8d9dfeb9283e6aa2c44e41ccceb1071969c3',SCHEME:'9b34c478f6f8dd4e64ce212b8f537e490495754c8ecb21e1f0341b1cba89eb8d'}
REVIEW='scripts/markbank/authoring/home-economics/2011-hl-main-review.json'
def documents():
 for p,h in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 return {k:fitz.open(ROOT/p) for k,p in [('paper',PAPER),('scheme',SCHEME)]}
def body_bottom(page):
 # The 2011 scheme is 907pt tall. A fixed A4 crop would lose its final lines.
 footers=[]
 for block in page.get_text('dict')['blocks']:
  for line in block.get('lines',[]):
   label=tidy(''.join(span['text'] for span in line['spans']))
   if line['bbox'][1]>page.rect.height*.82 and re.fullmatch(r'(?:\d{1,2}|Page \d+ of \d+)',label):footers.append(line['bbox'][1]-2)
 return min(footers) if footers else page.rect.height-20
def text(doc,n):return tidy(doc[n-1].get_text(clip=fitz.Rect(0,20,doc[n-1].rect.width,body_bottom(doc[n-1])),sort=True))
def a_regions(doc,pages):
 out={}
 for n in pages:
  page=doc[n-1];starts=sorted((int(w[4][:-1]),w[1]-3) for w in page.get_text('words') if re.fullmatch(r'\d+\.',w[4]) and 50<w[0]<85 and w[1]<760)
  for i,(q,top) in enumerate(starts):out[q]=dict(page=n,rect=[45,top,page.rect.width-25,starts[i+1][1] if i+1<len(starts) else body_bottom(page)])
 assert list(out)==list(range(1,13)),out.keys()
 return out
def card(key,section,ref,topic,prompt,stem,marks,rows,page,notation='',**extra):
 c=prior_card(key,section,ref,topic,prompt,stem,marks,rows,page,notation,**extra)
 c.update(id='he-2011-hl-'+key,year=2011,questionRef='2011 HL Section '+section+' '+ref)
 c['sourceMaterial']['attribution']='SEC Home Economics 2011 Higher Level examination paper — © State Examinations Commission.'
 return c
def write_section(section,cards,review):
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text());ids={c['id'] for c in cards};assert len(ids)==len(cards)
 p.write_text(json.dumps([c for c in data if c['id'] not in ids]+cards,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text())
 if r['status']=='independent-source-census-complete-authoring-pending':r['status']='source-review-in-progress'
 r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],section=section,marks=c['totalMarks'],questionRef=c['questionRef'],topicId=c['topicId']) for c in cards];r['section'+section+'Review']=review;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
def transcript():
 d=documents()['scheme'];(ROOT/'examiner-reports/home-economics/schemes/2011-hl.md').write_text(('# SEC Home Economics 2011 Higher marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+p.get_text(sort=True) for i,p in enumerate(d))).rstrip()+'\n')
def a_build():
 d=documents();pr=a_regions(d['paper'],range(2,6));sr=a_regions(d['scheme'],range(4,7));p={n:without_number(region(d['paper'],r)) for n,r in pr.items()};s={n:without_number(region(d['scheme'],r)) for n,r in sr.items()};rows={}
 tables=d['scheme'][3].find_tables().tables;assert len(tables)==2
 rows[1]=[]
 for category,values,foods in tables[0].extract()[1:]:
  values=values.splitlines();foods=foods.splitlines();assert len(values)==len(foods)
  for v,f in zip(values,foods):rows[1].append(point(f'pair-{len(rows[1])+1}',tidy(category)+' — '+tidy(v)+' — '+tidy(f)))
 for n in [2,3,8,11]:
  body=select(s[n],'(6)');body=re.sub(r'\((?:i|ii|iii)\)\s*','; ',body).strip('; ')
  rows[n]=[point(f'answer-{i}',v) for i,v in enumerate(semis(body),1)]
 rows[4]=[point(f'food-{i}',tidy(food)+' — '+tidy(protein)) for i,(food,protein) in enumerate(tables[1].extract()[1:],1)]
 rows[5]=[point(f'loss-{i}',v) for i,v in enumerate(semis(select(s[5],'(6)')),1)]
 grid=d['scheme'][4].find_tables().tables[0].extract();assert grid[0][0]=='Antioxidants'
 rows[6]=[point(f'cell-{i}',tidy(grid[0][i]),note='Original antioxidant table, '+tidy(grid[0][i])+': '+tidy(grid[1][i])) for i in [1,2,3]]
 rows[7]=[point(f'method-{i}',v) for i,v in enumerate(named(select(s[7],'(6)'),['Hanging –','Mechanical breakdown –','Mincing','Tenderisers –','Marinating –','Slow moist methods']),1)]
 components=re.sub(r'\((?:i|ii|iii)\)','',select(s[9],'(6)','Give an example'))
 rows[9]=[point('components',tidy(components)),point('examples',select(s[9],'Meal planning',include=True))]
 rows[10]=[point('definition',select(s[10],'(6)','State two conditions'))]+[point(f'condition-{i}',v) for i,v in enumerate(semis(re.sub(r'\((?:i|ii)\)','; ',select(s[10],'State two conditions that must be fulfilled in order to qualify for FIS.')).strip('; ')),1)]
 rows[12]=[point('ce',select(s[12],'Goods comply','___',True)),point('insulation',select(s[12],'Appliance has','___',True))]
 topics={1:'0-6',2:'0-8',3:'0-8',4:'0-5',5:'0-3',6:'0-11',7:'0-3',8:'0-4',9:'1-0',10:'1-1',11:'1-1',12:'1-2'};cards=[]
 for n in range(1,13):
  prompt=clean(p[n].split('(6)',1)[0]) if n in [1,4,6,12] else clean(p[n])
  rows[n][0]['contextNote']=WHOLE_NOTE+(' '+rows[n][0]['contextNote'] if rows[n][0].get('contextNote') else '')
  if n in [10,11]:rows[n][0]['contextNote']+=' Historical 2011 scheme wording and conditions are retained for this examination task.'
  c=card(f'sa-q{n}','A',f'Q{n}',topics[n],prompt,'',6,rows[n],pr[n]['page'],tariffModel=dict(kind='questionTotal'))
  if n in [1,4,6,12]:c.update(questionFigureKey=f'home-economics-2011-hl-sa-q{n}',questionFigureIncludesPrompt=True)
  cards.append(c)
 assert len(cards)==12 and sum(c['totalMarks'] for c in cards)==72
 return cards
if __name__=='__main__':
 cards=a_build()
 if '--write' in sys.argv:transcript();write_section('A',cards,dict(tasks=12,marks=72,tariffDecision='Every question retains the published six-mark whole-question total. Unpriced answer rows and visible total-only guidance; no per-answer value or partial ladder invented. A9/A10 companion asks remain complete because the source gives no separate tariffs.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
