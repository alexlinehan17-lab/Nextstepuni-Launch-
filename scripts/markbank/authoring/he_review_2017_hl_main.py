#!/usr/bin/env python3
"""2017 Higher original-source selections after the independent 52-page sweep."""
import hashlib,json,re,sys
import fitz
from he_review_2011_hl_main import ROOT,tidy,criterion,select,named,point,menu,semis,region,body_bottom,text,clean,without_number,examples,chosen,a_regions,WHOLE_NOTE
from he_review_2011_hl_main import card as prior_card
PAPER='paper-trail-corpus/exampapers/2017/LC098ALP000EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2017/LC098ALP000EV.pdf'
HASHES={PAPER:'b6d772120643fe1d8dd51a7704a37b57d216cc1beebe2fb3b987bd6d3ffc702e',SCHEME:'ebdd081ae16bce2f3d4579652be79629d468be5ff0ab6444fc5893ee8459675c'}
REVIEW='scripts/markbank/authoring/home-economics/2017-hl-main-review.json'
def documents():
 for p,h in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 return {k:fitz.open(ROOT/p) for k,p in [('paper',PAPER),('scheme',SCHEME)]}
def card(key,section,ref,topic,prompt,stem,marks,rows,page,notation='',**extra):
 c=prior_card(key,section,ref,topic,prompt,stem,marks,rows,page,notation,**extra)
 c.update(id='he-2017-hl-'+key,year=2017,level='higher',questionRef='2017 HL Section '+section+' '+ref)
 c['sourceMaterial']['attribution']='SEC Home Economics 2017 Higher Level examination paper — © State Examinations Commission.'
 return c
def write_section(section,cards,review):
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text());ids={c['id'] for c in cards};assert len(ids)==len(cards)
 p.write_text(json.dumps([c for c in data if c['id'] not in ids]+cards,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text())
 if r['status']=='independent-source-census-complete-authoring-pending':r['status']='source-review-in-progress'
 r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],section=section,marks=c['totalMarks'],questionRef=c['questionRef'],topicId=c['topicId']) for c in cards];r['section'+section+'Review']=review;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
def transcript():
 d=documents()['scheme'];full='# SEC Home Economics 2017 Higher marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+p.get_text(sort=True) for i,p in enumerate(d))
 # Whole-page extraction interleaves the original tables's columns. Preserve
 # the raw transcript and append independent, coordinate-bounded cell reads.
 for pn in [5,6,9,14,23]:
  for i,t in enumerate(d[pn-1].find_tables().tables,1):
   full+=f'\n\n## Physical page {pn}, original table {i}, cell reading order\n\n'+'\n'.join(' | '.join(row).rstrip() for row in table_rows(t,d[pn-1]))
 (ROOT/'examiner-reports/home-economics/schemes/2017-hl.md').write_text(full.rstrip()+'\n')
def body_bottom(page):
 # The 2017 scheme uses bracketed printed page numbers. Keep full page content
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
 full=select(s[1],'(6)');essential,other=named(full,['Essential amino acids','Non-essential amino acids']);rows[1]=[point('essential',essential,note='Explain essential amino acids and give ONE matching example from the complete original pool.'),point('nonessential',other,note='Explain non-essential amino acids and give ONE matching example from the complete original pool.')]
 rows[2]=[point('effect',select(s[2],'(6)','Give two culinary examples'))]+[point(f'example-{i}',v,note='Choose ANY TWO examples across both original answer lines; no one-per-line restriction.') for i,v in enumerate(named(select(s[2],'Give two culinary examples of gelatinisation.'),['(i)','(ii)']),1)]
 rows[3]=[point('role',select(s[3],'(6)'))]
 t5=d['scheme'][4].find_tables().tables;t6=d['scheme'][5].find_tables().tables;assert len(t5)==len(t6)==2
 rows[4]=[point(f'heading-{i}',a+' — '+b) for i,(a,b) in enumerate(table_rows(t5[0],d['scheme'][4]),1)]
 rows[5]=[point(f'packaging-{i}',v) for i,v in enumerate(named(select(s[5],'(6)'),['Modified atmosphere packaging','Biodegradable packaging']),1)]
 grid=table_rows(t5[1],d['scheme'][4])[1:]+table_rows(t6[0],d['scheme'][5]);assert len(grid)==5
 rows[6]=[point(f'bacterium-{i}',name,note='Choose ANY TWO different bacteria. For EACH give its matching description/characteristic AND habitat. Complete original paired model: '+name+' — Description / characteristic: '+description+' Habitat: '+habitat) for i,(name,description,habitat) in enumerate(grid,1)]
 rows[6].append(point('other-bacteria',select(text(d['scheme'],6),'Clostridium Welchii;','7.',True),note='The original scheme names Clostridium Welchii and Campylobacter without description/habitat models. No model has been invented. Keep all headings about each SAME selected bacterium.'))
 rows[7]=[point('fermentation',select(s[7],'(6)','yeast +'),note='The complete original chemical equation is retained in the source image.')]+[point(f'product-{i}',v,note='Choose ANY TWO by-products across both original source lines.') for i,v in enumerate(named(select(s[7],'Name two by-products of fermentation.'),['(i)','(ii)']),1)]
 grid=table_rows(t6[1],d['scheme'][5]);assert len(grid)==2;rows[8]=[point(f'cell-{i}',grid[0][i]+' — '+grid[1][i]) for i in [1,2,3]]
 rows[9]=[point('stages',select(s[9],'(6)','Give two examples'))]+[point(f'example-{i}',v,note='Choose ANY TWO family-life examples from both source lines; no one-per-line quota.') for i,v in enumerate(named(select(s[9],'Give two examples of family life which require management skills.'),['(i)','(ii)']),1)]
 rows[10]=[point(f'insurance-{i}',v) for i,v in enumerate(named(select(s[10],'(6)'),['Insurance premium','Insurance policy']),1)]
 rows[11]=[point(f'payment-{i}',v,note='Name ANY THREE social welfare payments across the full pool. Do not require a pension or one choice from each source line. Historical 2017 names retained.') for i,v in enumerate(named(select(s[11],'(6)'),['(i)','(ii)','(iii)']),1)]
 rows[12]=[point(f'protection-{i}',v,note='Historical consumer legislation named in the 2017 paper; original complete source guidance retained.') for i,v in enumerate(named(select(s[12],'(6)'),['(i)','(ii)']),1)]
 topics={1:'0-5',2:'0-6',3:'0-4',4:'0-8',5:'0-11',6:'0-4',7:'0-4',8:'0-9',9:'1-0',10:'1-1',11:'1-1',12:'1-2'};cards=[]
 for n in range(1,13):
  prompt=clean(p[n].split('(6)',1)[0]) if n in [4,6,8] else clean(p[n]);rows[n][0]['contextNote']=WHOLE_NOTE+(' '+rows[n][0]['contextNote'] if rows[n][0].get('contextNote') else '')
  c=card(f'sa-q{n}','A',f'Q{n}',topics[n],prompt,'',6,rows[n],pr[n]['page'],tariffModel=dict(kind='questionTotal'))
  if n in [4,6,8]:c.update(questionFigureKey=f'home-economics-2017-hl-sa-q{n}',questionFigureIncludesPrompt=True)
  if n==7:c['figureKey']='home-economics-2017-hl-sa-q7-equation'
  cards.append(c)
 assert len(cards)==12 and sum(c['totalMarks'] for c in cards)==72
 return cards
if __name__=='__main__':
 cards=a_build()
 if '--write' in sys.argv:transcript();write_section('A',cards,dict(tasks=12,marks=72,tariffDecision='All 12 original whole-six tariffs retain unpriced source guidance and all companion asks; no invented per-answer steps. Five full bacteria profiles and two name-only alternatives, complete original fermentation equation, unrestricted example/payment pools and historical source wording retained.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
