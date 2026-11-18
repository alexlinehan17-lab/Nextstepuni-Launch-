#!/usr/bin/env python3
"""2011 Ordinary source selections following the independent 44-page sweep."""
import hashlib,json,re,sys
import fitz
from paper import strip_set_lines
from he_review_2011_hl_main import ROOT,tidy,criterion,select,named,point,menu,semis,region,body_bottom,text,clean,without_number,examples,chosen
from he_review_2011_hl_main import card as higher_card
PAPER='paper-trail-corpus/exampapers/2011/LC098GLP000EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2011/LC098GLP000EV.PDF'
HASHES={PAPER:'603fecfd5aa5f7fe0c4ef963e05bc3001921e9ca1fbabc31362cf0bd1344c28a',SCHEME:'3abf73d93781c28a5b282a6d3094c3d4702b90c4d062def396ba1abd69bb0fd8'}
REVIEW='scripts/markbank/authoring/home-economics/2011-ol-main-review.json'
def documents():
 for p,h in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 return {k:fitz.open(ROOT/p) for k,p in [('paper',PAPER),('scheme',SCHEME)]}
def a_regions(doc,pages):
 out={}
 for n in pages:
  page=doc[n-1];starts=sorted((int(w[4][:-1]),w[1]-3) for w in page.get_text('words') if re.fullmatch(r'\d+\.',w[4]) and 50<w[0]<95 and w[1]<760)
  for i,(q,top) in enumerate(starts):out[q]=dict(page=n,rect=[45,top,page.rect.width-25,starts[i+1][1] if i+1<len(starts) else body_bottom(page)])
 assert list(out)==list(range(1,13)),out.keys()
 return out
def card(key,section,ref,topic,prompt,stem,marks,rows,page,notation='',**extra):
 c=higher_card(key,section,ref,topic,prompt,stem,marks,rows,page,notation,**extra)
 c.update(id='he-2011-ol-'+key,level='ordinary',questionRef='2011 OL Section '+section+' '+ref)
 c['sourceMaterial']['attribution']='SEC Home Economics 2011 Ordinary Level examination paper — © State Examinations Commission.'
 return c
def write_section(section,cards,review):
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text());ids={c['id'] for c in cards};assert len(ids)==len(cards)
 p.write_text(json.dumps([c for c in data if c['id'] not in ids]+cards,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text())
 if r['status']=='independent-source-census-complete-authoring-pending':r['status']='source-review-in-progress'
 r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],section=section,marks=c['totalMarks'],questionRef=c['questionRef'],topicId=c['topicId']) for c in cards];r['section'+section+'Review']=review;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
def transcript():
 d=documents()['scheme'];(ROOT/'examiner-reports/home-economics/schemes/2011-ol.md').write_text(('# SEC Home Economics 2011 Ordinary marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+p.get_text(sort=True) for i,p in enumerate(d))).rstrip()+'\n')
def a_build():
 d=documents();pr=a_regions(d['paper'],range(2,6));sr=a_regions(d['scheme'],range(4,8));p={n:without_number(region(d['paper'],r)) for n,r in pr.items()};s={n:without_number(region(d['scheme'],r)) for n,r in sr.items()};cards=[]
 # Three strip-set pages are reconstructed by original glyph positions.
 for n in [7,8,9]:
  r=pr[n];p[n]=without_number(tidy(' '.join(t for _,t in strip_set_lines(d['paper'][r['page']-1],clip=r['rect']))))
 def add(n,topic,marks,rows,notation,suffix='',prompt=None,figure=False):
  c=card(f'sa-q{n}{suffix}','A',f'Q{n}'+(' — '+suffix[1:] if suffix else ''),topic,(prompt or clean(p[n])).replace('\uf0fc','✓'),'',marks,rows,pr[n]['page'],notation)
  if figure:c.update(questionFigureKey=f'home-economics-2011-ol-sa-q{n}',questionFigureIncludesPrompt=True)
  cards.append(c);return c
 table=d['scheme'][3].find_tables().tables[0].extract();assert len(table)==4
 add(1,'0-6',6,[point(f'match-{i}',tidy(a)+' — '+tidy(b),2) for i,(a,b) in enumerate(table[1:],1)],'3 matches × 2',prompt=clean(p[1].split('(6)',1)[0]),figure=True)
 fibre=clean(select(s[2],'3 points @ 2 marks'));opts=[v.strip() for v in examples(fibre).split(',') if v.strip()]
 add(2,'0-6',6,[menu('ways','ways',3,2,opts)],'3 points × 2')
 cloze=named(select(s[3],'folic acid, thiamine, energy'),['Vitamin B1 is also','Vitamin B1 is necessary','A woman should'])
 add(3,'0-8',6,[point(f'blank-{i}',v,2) for i,v in enumerate(cloze,1)],'3 points × 2',prompt=clean(p[3].split('(6)',1)[0]),figure=True)
 tables=d['scheme'][4].find_tables().tables;assert len(tables)==3
 truth=tables[0].extract();assert all(bool(row[1]) and not row[2] for row in truth[1:])
 add(4,'0-1',6,[point(f'statement-{i}',tidy(row[0])+' — True',2) for i,row in enumerate(truth[1:],1)],'3 statements × 2',prompt=clean(p[4].split('(6)',1)[0]),figure=True)
 add(5,'0-3',6,[point(f'match-{i}',tidy(a)+' — '+tidy(b),2) for i,(a,b) in enumerate(tables[1].extract()[1:],1)],'3 matches × 2',prompt=clean(p[5].split('(6)',1)[0]),figure=True)
 raising=tables[2].extract();guide='; '.join(tidy(a)+' — '+tidy(b) for a,b in raising[1:]);principles=select(s[6],'1 point @ 1 mark')
 add(6,'0-3',6,[criterion('matches','Raising Agents',1,[0,5],'Complete all three named-dish matches. The source prices two answers at2 marks and one at1 (five total) but does not assign those prices to individual dishes. No per-food allocation or finer ladder has been invented; this criterion checks the complete five-mark table. Source: '+guide),menu('principle','underlying principle',1,1,named(principles,['Air:','Yeast:','Bread soda:']),'Explain ONE of the agents named in your table. No additional model for baking powder is supplied.')],'Table (2 × 2 + 1) + dependent principle 1',figure=True)
 storage=select(s[7],'2 points @ 3 marks');add(7,'0-4',6,[point(f'point-{i}',v,3) for i,v in enumerate(named(storage,['(i)','(ii)']),1)],'2 points × 3',prompt=clean(p[7]))
 pollution=select(s[8],'Effect: 2 @ 2 marks');rows=[];groups=[]
 for i in [1,2]:
  rows.extend([criterion(f'type-{i}','Type',1,[0,1],'Choose a different type in each pair. Complete source options and matching effects: '+pollution),criterion(f'effect-{i}','Effect',1,[0,2],'One effect of the SAME pollution type. Complete source guidance: '+pollution)])
  groups.append(dict(sourceCardId=f'he-2011-ol-sa-q8-pair-{i}',label=f'Pollution type / effect {i}',marks=3,rowIds=[f'type-{i}',f'effect-{i}']))
 c=add(8,'1-5',6,rows,'2 pairs × (type1 + effect2)',prompt=clean(p[8].split('(6)',1)[0]));c['taskGroups']=groups
 energy=select(s[9],'This enables consumers',include=True);add(9,'1-3',6,[criterion('benefits','benefit',2,[0,3],'Historical 2011 energy-label scale retained as printed. Source guidance: '+energy)],'2 points × 3',prompt=clean(p[9]),figure=True)
 names=select(s[10],'Name: Tesco','State one advantage');names='Tesco '+names;body=select(s[10],'State one advantage');adv=select(body,'Advantage :','Disadvantage:');dis=select(body,'Disadvantage:')
 add(10,'1-2',6,[menu('name','Name',1,2,[v.strip() for v in examples(names).split(',') if v.strip()]),criterion('advantage','Advantage',1,[0,2],'One advantage of this SAME loyalty scheme. Source: '+adv),criterion('disadvantage','Disadvantage',1,[0,2],'One disadvantage of this SAME loyalty scheme. Source: '+dis)],'Name2 + advantage2 + disadvantage2')
 names=examples(select(s[11],'1 point @ 2 marks','Give two different'));uses=examples(clean(select(s[11],'2 points @ 2 marks')))
 add(11,'1-4',2,[menu('finish','fire retardant finish',1,2,[v.strip() for v in names.split(',') if v.strip()])],'Name2',prompt=clean(p[11].split('Give two different',1)[0]))
 add(11,'1-4',4,[menu('uses','uses',2,2,chosen(uses,['children’s nightwear','protective work wear','upholstered furniture','military apparel']))],'2 uses × 2',suffix='-uses',prompt=clean(select(p[11],'Give two different',include=True)))
 essential=select(s[12],'Essential expenditure:','Discretionary expenditure:');discretionary=select(s[12],'Discretionary expenditure:');rows=[];groups=[]
 for key,label,body in [('essential','Essential expenditure',essential),('discretionary','Discretionary expenditure',discretionary)]:
  definition,example=body.split('Example:',1);rows += [point(key+'-explanation',label+': '+definition.strip(),2),menu(key+'-example','Example',1,1,[v.strip() for v in examples(example).split(',') if v.strip()])];groups.append(dict(sourceCardId='he-2011-ol-sa-q12-'+key,label=label,marks=3,rowIds=[key+'-explanation',key+'-example']))
 c=add(12,'1-1',6,rows,'2 explanations × 2 + 2 examples × 1');c['taskGroups']=groups
 assert len(cards)==13 and sum(c['totalMarks'] for c in cards)==72
 return cards
if __name__=='__main__':
 cards=a_build()
 if '--write' in sys.argv:transcript();write_section('A',cards,dict(tasks=13,marks=72,selectionDecisions='A11 independent name/uses tasks2+4; remaining required pairs and chosen-profile dependencies stay whole. A6 source gives2@2+1@1 without mapping prices to foods; visible whole-table criterion preserves this ambiguity and dependent principle1.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
