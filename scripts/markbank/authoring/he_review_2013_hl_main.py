#!/usr/bin/env python3
"""2013 Higher original-source selections after the independent 48-page sweep."""
import hashlib,json,re,sys
import fitz
from he_review_2011_hl_main import ROOT,tidy,criterion,select,named,point,menu,semis,region,body_bottom,text,clean,without_number,examples,chosen,a_regions,WHOLE_NOTE
from he_review_2011_hl_main import card as prior_card
PAPER='paper-trail-corpus/exampapers/2013/LC098ALP000EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2013/LC098ALP000EV.pdf'
HASHES={PAPER:'066d568cef0b12060037c81a0be9eab1bc9129cf9550f38a91166ba47509727d',SCHEME:'5ec2779ff9fd711f73e3db8216f6fad1405fc5c141929c8dcbedf6b3d97985d6'}
REVIEW='scripts/markbank/authoring/home-economics/2013-hl-main-review.json'
def documents():
 for p,h in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 return {k:fitz.open(ROOT/p) for k,p in [('paper',PAPER),('scheme',SCHEME)]}
def card(key,section,ref,topic,prompt,stem,marks,rows,page,notation='',**extra):
 c=prior_card(key,section,ref,topic,prompt,stem,marks,rows,page,notation,**extra)
 c.update(id='he-2013-hl-'+key,year=2013,questionRef='2013 HL Section '+section+' '+ref)
 c['sourceMaterial']['attribution']='SEC Home Economics 2013 Higher Level examination paper — © State Examinations Commission.'
 return c
def write_section(section,cards,review):
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text());ids={c['id'] for c in cards};assert len(ids)==len(cards)
 p.write_text(json.dumps([c for c in data if c['id'] not in ids]+cards,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text())
 if r['status']=='independent-source-census-complete-authoring-pending':r['status']='source-review-in-progress'
 r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],section=section,marks=c['totalMarks'],questionRef=c['questionRef'],topicId=c['topicId']) for c in cards];r['section'+section+'Review']=review;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
def transcript():
 d=documents()['scheme'];full='# SEC Home Economics 2013 Higher marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+p.get_text(sort=True) for i,p in enumerate(d))
 # Whole-page extraction interleaves the protein table's columns. Preserve
 # the raw transcript and append independent, coordinate-bounded cell reads.
 for pn in [4,5]:
  for i,t in enumerate(d[pn-1].find_tables().tables,1):
   full+=f'\n\n## Physical page {pn}, original table {i}, cell reading order\n\n'+'\n'.join(' | '.join(row) for row in table_rows(t,d[pn-1]))
 (ROOT/'examiner-reports/home-economics/schemes/2013-hl.md').write_text(full.rstrip()+'\n')
def table_rows(table,page):
 return [[tidy(page.get_text(clip=fitz.Rect(cell),sort=True)) if cell else '' for cell in row.cells] for row in table.rows]
def a_build():
 d=documents();pr=a_regions(d['paper'],range(2,6));sr=a_regions(d['scheme'],range(4,8));p={n:without_number(region(d['paper'],r)) for n,r in pr.items()};s={n:without_number(region(d['scheme'],r)) for n,r in sr.items()};rows={}
 tables=d['scheme'][3].find_tables().tables;assert len(tables)==2
 rows[1]=[point(f'type-{i}',a+' — '+b) for i,(a,b) in enumerate(table_rows(tables[0],d['scheme'][3])[1:],1)]
 rows[2]=[point(f'type-{i}',v) for i,v in enumerate(named(select(s[2],'(6)'),['(i)','(ii)']),1)]
 rows[3]=[point(f'vitamin-{i}',a+' — '+b) for i,(a,b) in enumerate(table_rows(tables[1],d['scheme'][3])[1:],1)]
 tables=d['scheme'][4].find_tables().tables;assert len(tables)==2
 rows[4]=[point(f'flour-{i}',tidy(a)+' — '+tidy(b)) for i,(a,b) in enumerate(tables[0].extract()[1:],1)]
 rows[4]+=[point('other-types',select(s[4],'Types:','Uses:'),note='The source prints these additional types and uses as separate lists, without pairing them. Match each chosen flour to an appropriate different use.'),point('other-uses',select(s[4],'Uses:'))]
 rows[5]=[point(f'spread-{i}',v) for i,v in enumerate(named(select(s[5],'(6)'),['Low-fat spreads','Functional dairy spreads']),1)]
 rows[6]=[point(f'contaminant-{i}',tidy(a),note='How contamination occurs — '+tidy(b)+' Possible effect on the body — '+tidy(c)) for i,(a,b,c) in enumerate(tables[1].extract()[1:],1)]
 freezing=select(s[7],'(6)');quick,slow=freezing.split('Slow freezing',1);rows[7]=[point('quick',quick),point('slow',slow)]
 rows[8]=[point(f'microorganism-{i}',v) for i,v in enumerate(named(select(s[8],'(6)'),['Aerobic micro-organisms:','Anaerobic micro-organisms:','Facultative micro-organisms:']),1)]
 rows[9]=[point(f'part-{i}',v) for i,v in enumerate(named(select(s[9],'(6)'),['Compressor:','Condenser:','Evaporator:']),1)]
 rows[10]=[point(f'organisation-{i}',v) for i,v in enumerate(named(select(s[10],'(6)'),['Consumer Association of Ireland (CAI)','Advertising Standards Authority of Ireland (ASAI)']),1)]
 rows[11]=[point(f'component-{i}',v) for i,v in enumerate(named(select(s[11],'(6)'),['Surfactants','Enzymes','Fluorescents']),1)]
 rows[12]=[point(f'profile-{i}',v) for i,v in enumerate(named(select(s[12],'(6)'),['Essential expenditure –','Discretionary expenditure –']),1)]
 topics={1:'0-5',2:'0-7',3:'0-8',4:'0-9',5:'0-9',6:'0-4',7:'0-3',8:'0-4',9:'1-3',10:'1-2',11:'1-4',12:'1-1'};cards=[]
 for n in range(1,13):
  prompt=clean(p[n].split('(6)',1)[0]) if n in [1,3,4,6] else clean(p[n]);rows[n][0]['contextNote']=WHOLE_NOTE+(' '+rows[n][0]['contextNote'] if rows[n][0].get('contextNote') else '')
  if n==11:rows[n][0]['contextNote']+=' Choose ANY TWO of the three printed components. All three original models are retained; do not require all three.'
  if n==10:rows[n][0]['contextNote']+=' Historical 2013 organisation names and roles are retained.'
  c=card(f'sa-q{n}','A',f'Q{n}',topics[n],prompt,'',6,rows[n],pr[n]['page'],tariffModel=dict(kind='questionTotal'))
  if n in [1,3,4,6]:c.update(questionFigureKey=f'home-economics-2013-hl-sa-q{n}',questionFigureIncludesPrompt=True)
  cards.append(c)
 assert len(cards)==12 and sum(c['totalMarks'] for c in cards)==72
 return cards
if __name__=='__main__':
 cards=a_build()
 if '--write' in sys.argv:transcript();write_section('A',cards,dict(tasks=12,marks=72,tariffDecision='Whole six-mark questions with complete unpriced source answer rows and visible total-only guidance. A11 choose2 of3 retained; paired flour/use, spread/example and expenditure/example prompts stay complete. No unprinted tariffs or inferred flour/use pairings.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
