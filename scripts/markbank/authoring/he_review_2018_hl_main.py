#!/usr/bin/env python3
"""2018 Higher original-source selections after the independent 52-page sweep."""
import hashlib,json,re,sys
import fitz
from he_review_2011_hl_main import ROOT,tidy,criterion,select,named,point,menu,semis,region,body_bottom,text,clean,without_number,examples,chosen,a_regions,WHOLE_NOTE
from he_review_2011_hl_main import card as prior_card
PAPER='paper-trail-corpus/exampapers/2018/LC098ALP000EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2018/LC098ALP000EV.pdf'
HASHES={PAPER:'ee04fa824be50891a0f3dc3ca302824c0376f365a42af6ddd0ce4965a6e665a0',SCHEME:'33abfca7e608003644b9f6a5bb68a52d4d828c429f8a826329c609b7b296e333'}
REVIEW='scripts/markbank/authoring/home-economics/2018-hl-main-review.json'
def documents():
 for p,h in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 return {k:fitz.open(ROOT/p) for k,p in [('paper',PAPER),('scheme',SCHEME)]}
def card(key,section,ref,topic,prompt,stem,marks,rows,page,notation='',**extra):
 c=prior_card(key,section,ref,topic,prompt,stem,marks,rows,page,notation,**extra)
 c.update(id='he-2018-hl-'+key,year=2018,level='higher',questionRef='2018 HL Section '+section+' '+ref)
 c['sourceMaterial']['attribution']='SEC Home Economics 2018 Higher Level examination paper — © State Examinations Commission.'
 return c
def write_section(section,cards,review):
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text());ids={c['id'] for c in cards};assert len(ids)==len(cards)
 p.write_text(json.dumps([c for c in data if c['id'] not in ids]+cards,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text())
 if r['status']=='independent-source-census-complete-authoring-pending':r['status']='source-review-in-progress'
 r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],section=section,marks=c['totalMarks'],questionRef=c['questionRef'],topicId=c['topicId']) for c in cards];r['section'+section+'Review']=review;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
def transcript():
 d=documents()['scheme'];full='# SEC Home Economics 2018 Higher marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+p.get_text(sort=True) for i,p in enumerate(d))
 # Whole-page extraction interleaves the original tables's columns. Preserve
 # the raw transcript and append independent, coordinate-bounded cell reads.
 for pn in [4,5,6,8,13,14,18,19]:
  for i,t in enumerate(d[pn-1].find_tables().tables,1):
   full+=f'\n\n## Physical page {pn}, original table {i}, cell reading order\n\n'+'\n'.join(' | '.join(row).rstrip() for row in table_rows(t,d[pn-1]))
 (ROOT/'examiner-reports/home-economics/schemes/2018-hl.md').write_text(full.rstrip()+'\n')
def body_bottom(page):
 # The redesigned 2018 paper includes page/running boxes above its page
 # number. Exclude every actual footer line, keeping full source content.
 footers=[]
 for block in page.get_text('dict')['blocks']:
  for line in block.get('lines',[]):
   label=tidy(''.join(span['text'] for span in line['spans']))
   footer=bool(re.fullmatch(r'(?:\[?\d{1,2}\]?|Page \d+ of \d+|page|running)',label)) or (label.startswith('Leaving Certificate') and label.endswith('2018')) or (label.startswith('Home Economics') and 'Higher Level' in label)
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
 t4=d['scheme'][3].find_tables().tables;assert len(t4)==1;grid=table_rows(t4[0],d['scheme'][3]);assert len(grid)==5
 rows[1]=[point('pancreas',' — '.join(grid[1]),note='Complete the required PANCREAS row with this coherent enzyme/substrate/product profile.')]
 for i,row in enumerate(grid[2:],1):
  rows[1].append(point(f'intestine-{i}',' — '.join(row[1:]),note='Choose ONE complete SMALL INTESTINE enzyme/substrate/product profile from the three original alternatives; do not mix cells between profiles.'+(' The original scheme prints Glucose / Fructose for Lactase / Lactose; the source wording is reproduced here.' if i==3 else '')))
 rows[2]=[point(f'function-{i}',v,note='Choose ANY THREE Vitamin C functions across all original answer lines; no compulsory collagen/immune-system split.') for i,v in enumerate(named(select(s[2],'(6)'),['(i)','(ii)','(iii)']),1)]
 rows[3]=[point(f'protein-{i}',v,note='Choose ANY TWO meat proteins across both complete source pools.') for i,v in enumerate(named(select(s[3],'(6)','Outline two effects of cooking'),['(i)','(ii)']),1)]+[point(f'effect-{i}',v,note='Choose ANY TWO cooking effects across both complete source pools.') for i,v in enumerate(named(select(s[3],'Outline two effects of cooking on protein in meat.'),['(i)','(ii)']),1)]
 rows[4]=[point(f'role-{i}',v,note='Outline the role of energy using the complete source guidance. Answer lines carry no separate allocation.') for i,v in enumerate(named(select(s[4],'(6)'),['(i)','(ii)','(iii)']),1)]
 rows[5]=[point('significance',select(s[5],'Food products','Name two products',True))]+[point(f'product-{i}',v,note='Choose ANY TWO labelled products across both original pools, after explaining the symbol.') for i,v in enumerate(named(select(s[5],'Name two products that use this symbol on their labelling.'),['(i)','(ii)']),1)]
 t5=d['scheme'][4].find_tables().tables;assert len(t5)==1
 rows[6]=[point(f'category-{i}',category+' — '+models,note='Give ONE different food/product for EACH required processed-food category; full original model pool retained.') for i,(category,models) in enumerate(table_rows(t5[0],d['scheme'][4])[1:],1)]
 rows[7]=[point(f'method-{i}',v) for i,v in enumerate(named(select(s[7],'(6)'),['Conduction:','Convection:']),1)]
 t6=d['scheme'][5].find_tables().tables;assert len(t6)==2
 rows[8]=[point(f'group-{i}',name+' — '+temperature,note='State the complete original optimum-growth temperature RANGE for this required group.') for i,(name,temperature) in enumerate(table_rows(t6[0],d['scheme'][5]),1)]
 rows[9]=[point(f'textile-{i}',name,note='Choose ANY TWO textiles, giving ONE property matching EACH selected textile. Complete original paired guidance: '+name+' — '+properties) for i,(name,properties) in enumerate(table_rows(t6[1],d['scheme'][5])[1:],1)]
 rows[9].append(point('finish',select(s[9],'Name one fire retardant finish used on household textiles.'),note='Also name ONE fire-retardant finish from the original source pool.'))
 rows[10]=[point(f'influence-{i}',v,note='Explain how advertising affects buying behaviour using the complete source guidance; no separate answer-line allocation is printed.') for i,v in enumerate(named(select(s[10],'(6)'),['(i)','(ii)']),1)]
 rows[11]=[point(f'advantage-{i}',v,note='Choose ANY TWO saving advantages across both original pools.') for i,v in enumerate(named(select(s[11],'(6)','Name two savings schemes'),['(i)','(ii)']),1)]+[point('schemes',select(s[11],'Name two savings schemes offered by financial institutions.'),note='Also name ANY TWO saving schemes from the complete original list.')]
 rows[12]=[point(f'tax-{i}',v,note='Original historical 2018 tax wording, thresholds and rates are preserved.') for i,v in enumerate(named(select(s[12],'(6)'),['Tax Credit:','USC:']),1)]
 topics={1:'0-6',2:'0-8',3:'0-9',4:'0-1',5:'0-1',6:'0-11',7:'0-3',8:'0-4',9:'1-4',10:'1-2',11:'1-1',12:'1-1'};figures=[1,5,6,8,9];cards=[]
 for n in range(1,13):
  prompt=clean(p[n].split('(6)',1)[0]) if n in [1,6,8] else clean(p[n]);rows[n][0]['contextNote']=WHOLE_NOTE+(' '+rows[n][0]['contextNote'] if rows[n][0].get('contextNote') else '')
  c=card(f'sa-q{n}','A',f'Q{n}',topics[n],prompt,'',6,rows[n],pr[n]['page'],tariffModel=dict(kind='questionTotal'))
  if n in figures:c.update(questionFigureKey=f'home-economics-2018-hl-sa-q{n}',questionFigureIncludesPrompt=True)
  cards.append(c)
 assert len(cards)==12 and sum(c['totalMarks'] for c in cards)==72
 return cards
if __name__=='__main__':
 cards=a_build()
 if '--write' in sys.argv:transcript();write_section('A',cards,dict(tasks=12,marks=72,tariffDecision='Whole-six questions retain all companion asks, coherent pancreatic/intestine profiles, the original lactase-product wording, full textile/property choices plus finish, original symbol and temperature ranges, unrestricted answer-line pools and historical tax wording. No invented per-answer allocation.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
