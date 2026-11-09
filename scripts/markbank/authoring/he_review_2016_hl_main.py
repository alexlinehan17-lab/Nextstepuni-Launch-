#!/usr/bin/env python3
"""2016 Higher original-source selections after the independent 52-page sweep."""
import hashlib,json,re,sys
import fitz
from he_review_2011_hl_main import ROOT,tidy,criterion,select,named,point,menu,semis,region,body_bottom,text,clean,without_number,examples,chosen,a_regions,WHOLE_NOTE
from he_review_2011_hl_main import card as prior_card
PAPER='paper-trail-corpus/exampapers/2016/LC098ALP000EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2016/LC098ALP000EV.pdf'
HASHES={PAPER:'eed9c2b03c01e4036bd52faddd45555384a12610eb90efd4291300eab9faa51b',SCHEME:'3be6624649c45c3c1dbe76b68189c55f2a90a8c40cc42478a3d633ea3a63641b'}
REVIEW='scripts/markbank/authoring/home-economics/2016-hl-main-review.json'
def documents():
 for p,h in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 return {k:fitz.open(ROOT/p) for k,p in [('paper',PAPER),('scheme',SCHEME)]}
def card(key,section,ref,topic,prompt,stem,marks,rows,page,notation='',**extra):
 c=prior_card(key,section,ref,topic,prompt,stem,marks,rows,page,notation,**extra)
 c.update(id='he-2016-hl-'+key,year=2016,level='higher',questionRef='2016 HL Section '+section+' '+ref)
 c['sourceMaterial']['attribution']='SEC Home Economics 2016 Higher Level examination paper — © State Examinations Commission.'
 return c
def write_section(section,cards,review):
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text());ids={c['id'] for c in cards};assert len(ids)==len(cards)
 p.write_text(json.dumps([c for c in data if c['id'] not in ids]+cards,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text())
 if r['status']=='independent-source-census-complete-authoring-pending':r['status']='source-review-in-progress'
 r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],section=section,marks=c['totalMarks'],questionRef=c['questionRef'],topicId=c['topicId']) for c in cards];r['section'+section+'Review']=review;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
def transcript():
 d=documents()['scheme'];full='# SEC Home Economics 2016 Higher marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+p.get_text(sort=True) for i,p in enumerate(d))
 # Whole-page extraction interleaves the original tables's columns. Preserve
 # the raw transcript and append independent, coordinate-bounded cell reads.
 for pn in [4,6,9,10,11]:
  for i,t in enumerate(d[pn-1].find_tables().tables,1):
   full+=f'\n\n## Physical page {pn}, original table {i}, cell reading order\n\n'+'\n'.join(' | '.join(row).rstrip() for row in table_rows(t,d[pn-1]))
 (ROOT/'examiner-reports/home-economics/schemes/2016-hl.md').write_text(full.rstrip()+'\n')
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
 d=documents();pr=a_regions(d['paper'],range(2,6));sr=a_regions(d['scheme'],range(4,9));p={n:without_number(region(d['paper'],r)) for n,r in pr.items()};s={n:without_number(region(d['scheme'],r)) for n,r in sr.items()};rows={}
 tables=d['scheme'][3].find_tables().tables;assert len(tables)==1
 rows[1]=[point(f'protein-{i}',a+' — '+b,note='Give ONE source for this required protein.') for i,(a,b) in enumerate(table_rows(tables[0],d['scheme'][3])[1:],1)]
 rows[2]=[point('function',select(s[2],'(6)','Name two different food sources'),note='Give ONE function from the full source pool.')]+[point(f'source-{i}',v,note='Choose ANY TWO different food sources across both source lines.') for i,v in enumerate(named(select(s[2],'Name two different food sources of omega 3 fatty acids.'),['(i)','(ii)']),1)]
 rows[3]=[point('fortification',select(s[3],'(6)','Name one fortified food / product')),point('product',select(s[3],'Fortified food / product -','Benefit:'),note='Name ONE fortified food/product.'),point('benefit',select(s[3],'Benefit:'),note='Explain a benefit of the SAME named product using the original source guidance.')]
 full=re.sub(r'\((?:i|ii|iii)\)\s*','',select(s[4],'(6)'));rows[4]=[point(f'function-{i}',v,note='Choose ANY THREE functions. The original sentence about development of brain, spinal cord and skeleton crosses printed answer lines; it remains intact.') for i,v in enumerate(semis(full),1)]
 rows[5]=[point(f'advantage-{i}',v,note='Choose ANY TWO advantages across both source lines.') for i,v in enumerate(named(select(s[5],'(6)','Other than tofu'),['(i)','(ii)']),1)]+[point(f'alternative-{i}',v,note='Choose ANY TWO protein alternatives other than tofu across both source lists. The original vegan list includes quorn; the printed source is retained.') for i,v in enumerate(named(select(s[5],'Other than tofu, name two protein alternatives that can be used in a vegan diet.'),['(i)','(ii)']),1)]
 heads=['Genetically modified food','Organic food / produce','Added-value food'];rows[6]=[point(f'type-{i}',v,note='Choose ANY TWO of the THREE printed categories. Original historical 2016 definitions and GM labelling threshold retained.') for i,v in enumerate(named(select(s[6],'(6)'),heads),1)]
 tables=d['scheme'][5].find_tables().tables;assert len(tables)==1;answers=table_rows(tables[0],d['scheme'][5])[0][1];rows[7]=[point(f'label-{i}',v) for i,v in enumerate(named(answers,['A =','B =','C =']),1)]
 hazard,control=named(select(s[8],'(6)'),['Hazard','Control measure']);rows[8]=[point('hazard',select(hazard,'Hazard','Example')),point('hazard-example',select(hazard,'Example'),note='Give ONE example matching a hazard.'),point('control',select(control,'Control measure','Example'),note='The original control-measure definition describes an area where a hazard could occur. This source wording is retained as printed, without an invented replacement.'),point('control-example',select(control,'Example'),note='Give ONE control-measure example from the complete original source pool.')]
 rows[9]=[point('purpose',select(s[9],'(6)','Name and describe one method'))]+[point(f'method-{i}',v,note='Name AND describe ONE method. The original scheme gives no model description for Focus groups; no description has been invented. Accept research by consumers and/or manufactures, as printed.') for i,v in enumerate(named(select(s[9],'Name and describe one method of consumer research.'),['Desk research:','Field research:','Focus groups:']),1)]
 rows[10]=[point(f'policy-{i}',v,note='Explain this required policy. Original historical 2016 wording retained.') for i,v in enumerate(named(select(s[10],'(6)'),['Life assurance:','Mortgage protection policy:']),1)]
 rows[11]=[point(f'property-{i}',v,note='Choose ANY TWO properties across both source lists.') for i,v in enumerate(named(select(s[11],'(6)','What information does the following label convey to the consumer?'),['(i)','(ii)']),1)]+[point('label',select(s[11],'Materials meet the requirements',include=True))]
 rows[12]=[point(f'heading-{i}',v,note='Use ONE pollution cause, its matching effect and a relevant reduction measure. Full original open guidance retained; do not mix unrelated profiles.') for i,v in enumerate(named(select(s[12],'(6)'),['Cause:','Effect:','Reduction measure:']),1)]
 topics={1:'0-5',2:'0-7',3:'0-11',4:'0-8',5:'0-5',6:'0-11',7:'0-4',8:'0-4',9:'1-2',10:'1-1',11:'1-4',12:'1-5'};figures=[1,7,11];cards=[]
 for n in range(1,13):
  prompt=clean(p[n].split('(6)',1)[0]) if n in [1,7] else clean(p[n]);rows[n][0]['contextNote']=WHOLE_NOTE+(' '+rows[n][0]['contextNote'] if rows[n][0].get('contextNote') else '')
  c=card(f'sa-q{n}','A',f'Q{n}',topics[n],prompt,'',6,rows[n],pr[n]['page'],tariffModel=dict(kind='questionTotal'))
  if n in figures:c.update(questionFigureKey=f'home-economics-2016-hl-sa-q{n}',questionFigureIncludesPrompt=True)
  if n==7:c['labelKey']=[dict(letter=letter,meaning=row['verbatim'].split(' = ',1)[1],askedInThisQuestion=True) for letter,row in zip(['A','B','C'],rows[n])]
  cards.append(c)
 assert len(cards)==12 and sum(c['totalMarks'] for c in cards)==72
 return cards
if __name__=='__main__':
 cards=a_build()
 if '--write' in sys.argv:transcript();write_section('A',cards,dict(tasks=12,marks=72,tariffDecision='All 12 whole-six tariffs retain unpriced full source guidance and every companion ask. Complete source pools, ANY TWO of THREE named food categories, both HACCP pairs and original source anomalies retained. Original folate sentence stays intact across answer lines.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
