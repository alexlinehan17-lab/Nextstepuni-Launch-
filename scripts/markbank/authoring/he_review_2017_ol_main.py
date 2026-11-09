#!/usr/bin/env python3
"""2017 Ordinary original-source selections after the independent 44-page sweep."""
import hashlib,json,re,sys
import fitz
from he_review_2011_hl_main import ROOT,tidy,criterion,select,named,point,menu,semis,region,body_bottom,text,clean,without_number,examples,chosen,a_regions,WHOLE_NOTE
from he_review_2011_hl_main import card as prior_card
PAPER='paper-trail-corpus/exampapers/2017/LC098GLP000EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2017/LC098GLP000EV.pdf'
HASHES={PAPER:'b6a03df9bccb63758498c363de21dbafb0b76dc8c00ed118ccb892ec851fd7ce',SCHEME:'d11f346fc0a130b450444da8070ace4e386a6351034729825e3de5eb525fa737'}
REVIEW='scripts/markbank/authoring/home-economics/2017-ol-main-review.json'
def documents():
 for p,h in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 return {k:fitz.open(ROOT/p) for k,p in [('paper',PAPER),('scheme',SCHEME)]}
def card(key,section,ref,topic,prompt,stem,marks,rows,page,notation='',**extra):
 c=prior_card(key,section,ref,topic,prompt,stem,marks,rows,page,notation,**extra)
 c.update(id='he-2017-ol-'+key,year=2017,level='ordinary',questionRef='2017 OL Section '+section+' '+ref)
 c['sourceMaterial']['attribution']='SEC Home Economics 2017 Ordinary Level examination paper — © State Examinations Commission.'
 return c
def write_section(section,cards,review):
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text());ids={c['id'] for c in cards};assert len(ids)==len(cards)
 p.write_text(json.dumps([c for c in data if c['id'] not in ids]+cards,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text())
 if r['status']=='independent-source-census-complete-authoring-pending':r['status']='source-review-in-progress'
 r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],section=section,marks=c['totalMarks'],questionRef=c['questionRef'],topicId=c['topicId']) for c in cards];r['section'+section+'Review']=review;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
def transcript():
 d=documents()['scheme'];full='# SEC Home Economics 2017 Ordinary marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+p.get_text(sort=True) for i,p in enumerate(d))
 # Whole-page extraction interleaves the original tables's columns. Preserve
 # the raw transcript and append independent, coordinate-bounded cell reads.
 for pn in [4,5,6,7,10]:
  for i,t in enumerate(d[pn-1].find_tables().tables,1):
   full+=f'\n\n## Physical page {pn}, original table {i}, cell reading order\n\n'+'\n'.join(' | '.join(row).rstrip() for row in table_rows(t,d[pn-1]))
 (ROOT/'examiner-reports/home-economics/schemes/2017-ol.md').write_text(full.rstrip()+'\n')
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
 def truth(grid):
  result=[]
  for i,(statement,yes,no) in enumerate(grid[1:],1):
   assert bool(yes)!=bool(no),(statement,yes,no)
   result.append(point(f'statement-{i}',tidy(statement)+' — '+grid[0][1 if yes else 2]))
  return result
 t4=d['scheme'][3].find_tables().tables;assert len(t4)==2
 rows[1]=truth(table_rows(t4[0],d['scheme'][3]))
 rows[2]=[point(f'source-{i}',v,note='Choose ANY THREE fibre sources across all three original answer lines; no one-per-line quota.') for i,v in enumerate(named(select(s[2],'(6)'),['(i)','(ii)','(iii)']),1)]
 rows[3]=truth(table_rows(t4[1],d['scheme'][3]))
 rows[4]=[point(f'function-{i}',v,note='Choose ANY TWO functions across both original source lines.') for i,v in enumerate(named(select(s[4],'(6)','Name two good dietary sources of calcium.'),['(i)','(ii)']),1)]+[point(f'source-{i}',v,note='Choose ANY TWO calcium sources across both complete original pools.') for i,v in enumerate(named(select(s[4],'Name two good dietary sources of calcium.'),['(i)','(ii)']),1)]
 rows[5]=[point(f'guideline-{i}',v,note='Choose ANY THREE guidelines across all three original source lines; historical 2017 scheme wording retained.') for i,v in enumerate(named(select(s[5],'(6)'),['(i)','(ii)','(iii)']),1)]
 t5=d['scheme'][4].find_tables().tables;assert len(t5)==1
 rows[6]=[point(f'method-{i}',method+' — '+first+' '+second,note='For EACH required cooking method choose ANY TWO foods from the complete pool across both example columns; no one-per-column restriction.') for i,(method,first,second) in enumerate(table_rows(t5[0],d['scheme'][4])[1:],1)]
 complete=select(s[7],'The largest part',include=True)
 rows[7]=[point(f'blank-{i}',v,note='Fill the three blanks in their original order. Complete original source sentence: '+complete if i==1 else '') for i,v in enumerate(chosen(complete,['endosperm','staple','bran']),1)]
 t6=d['scheme'][5].find_tables().tables;assert len(t6)==1;rows[8]=truth(table_rows(t6[0],d['scheme'][5]))
 rows[9]=[point(f'protection-{i}',v,note='Choose ANY THREE protections across the full original pool; no requirement to select a guarantee point. Historical legislation wording retained.') for i,v in enumerate(named(select(s[9],'(6)'),['(i)','(ii)','(iii)']),1)]
 rows[10]=[point(f'factor-{i}',v,note='Choose ANY TWO factors across both complete source lines.') for i,v in enumerate(named(select(s[10],'(6)','Name two fabrics suitable for household textiles.'),['(i)','(ii)']),1)]+[point(f'fabric-{i}',v,note='Choose ANY TWO fabrics across both original source lines; no one-per-line quota.') for i,v in enumerate(named(select(s[10],'Name two fabrics suitable for household textiles.'),['(i)','(ii)']),1)]
 rows[11]=[point('benefit',select(s[11],'enables consumers',include=True).replace('(www.which.co.uk)','').strip(),note='Explain ONE benefit from the complete original scheme guidance. The question shows the original historical energy label.')]
 t7=d['scheme'][6].find_tables().tables;assert len(t7)==1
 rows[12]=[point(f'pollution-{i}',kind+' — '+model,note='Give ONE example for EACH of the three required pollution types.') for i,(kind,model) in enumerate(table_rows(t7[0],d['scheme'][6])[1:],1)]
 topics={1:'0-7',2:'0-6',3:'0-5',4:'0-8',5:'0-1',6:'0-3',7:'0-9',8:'0-11',9:'1-2',10:'1-4',11:'1-3',12:'1-5'};figures=[1,3,6,7,8,11,12];cards=[]
 for n in range(1,13):
  prompt=clean(p[n].split('(6)',1)[0]) if n in figures else clean(p[n]);prompt=prompt.replace('\uf0fc','✓');rows[n][0]['contextNote']=WHOLE_NOTE+(' '+rows[n][0]['contextNote'] if rows[n][0].get('contextNote') else '')
  c=card(f'sa-q{n}','A',f'Q{n}',topics[n],prompt,'',6,rows[n],pr[n]['page'],tariffModel=dict(kind='questionTotal'))
  if n in figures:c.update(questionFigureKey=f'home-economics-2017-ol-sa-q{n}',questionFigureIncludesPrompt=True)
  cards.append(c)
 assert len(cards)==12 and sum(c['totalMarks'] for c in cards)==72
 return cards
if __name__=='__main__':
 cards=a_build()
 if '--write' in sys.argv:transcript();write_section('A',cards,dict(tasks=12,marks=72,tariffDecision='All twelve whole-six tariffs preserve every companion ask, complete source pools and original tables/cloze/energy label, with unpriced source rows and no invented per-answer allocation.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
