#!/usr/bin/env python3
"""2012 Higher B: original profiles, independent asks and explicit tariffs."""
from copy import deepcopy
from he_review_2012_hl_main import *
def build():
 d=documents();p={n:text(d['paper'],n) for n in range(6,9)};s={n:text(d['scheme'],n) for n in range(7,14)}
 q={1:select(p[6],'1.'),2:select(p[7],'2.','3.'),3:select(p[7],'3.'),4:select(p[8],'4.','5.'),5:select(p[8],'5.')};cards=[]
 def prompt(n,part):
  v=select(q[n],f'({part})',f'({chr(ord(part)+1)})' if f'({chr(ord(part)+1)})' in q[n] else None)
  return re.sub(r'\s*\(\d+\)\s*$','',v).replace('\uf0b7','•').strip()
 def add(n,part,topic,marks,rows,notation,**extra):
  c=card(f'sb-q{n}{part}','B',f'Q{n}({part})',topic,prompt(n,part),q[n].split('(a)',1)[0].strip(),marks,rows,6 if n==1 else 7 if n<=3 else 8,notation,**extra)
  if n==1:c['stem']=q[n].split('Age',1)[0].strip()
  cards.append(c);return c
 def guide(page,token,end=None):return select(s[page],token,end)
 def judged(n,part,topic,count,per,label,guidance,**extra):
  return add(n,part,topic,count*per,[criterion('points',label,count,[0,per],'Distinct points at the published value; no finer partial-credit steps are printed. Complete source guidance: '+guidance)],f'{count} points × {per}',**extra)
 reasons=guide(7,'Possible reasons:');rows=[];groups=[]
 for i,label in enumerate(['Bread/Cereals reference 1','Bread/Cereals reference 2','Fruit & Vegetables reference 1','Fruit & Vegetables reference 2'],1):
  rows.extend([criterion(f'analysis-{i}','simple analysis of table',1,[0,2],label+'. Two references to EACH of the two food groups are required, not four to one.'),criterion(f'elaboration-{i}','elaboration',1,[0,4],'Elaborate on the SAME analysis. Complete source guidance: '+reasons)])
  groups.append(dict(sourceCardId=f'he-2012-hl-sb-q1a-point-{i}',label=label,marks=6,rowIds=[f'analysis-{i}',f'elaboration-{i}']))
 add(1,'a','0-1',24,rows,'2 references per food group × (analysis 2 + elaboration 4)',taskGroups=groups,questionFigureKey='home-economics-2012-hl-sb-q1-servings',questionFigureIncludesPrompt=False)
 structure=guide(8,'Chemical structure','Disaccharide –',);structure='Chemical structure'+structure
 formation=guide(8,'Formation of disaccharides','Hydrolysis & Inversion',);formation='Formation of disaccharides'+formation
 hydrolysis=guide(8,'Hydrolysis & inversion –','(c)')
 add(1,'b','0-6',24,[criterion('structure','the chemical structure of a monosaccharide',1,[0,8],'The source gives eight marks for the structure, without per-atom allocations. Original chemical diagrams are retained below. Source: '+structure),criterion('formation','the formation of disaccharides',4,[0,2],'Complete original diagram and equation are shown below. The printed equation uses H20 while its diagram labels H₂O; both are retained as source material. Source: '+formation),criterion('hydrolysis','the hydrolysis of sugar to include inversion.',4,[0,2],hydrolysis)],'Structure 8 + formation 4 × 2 + hydrolysis/inversion 4 × 2',figureKey='home-economics-2012-hl-sb-q1b-carbohydrates')
 judged(1,'c','0-1',3,4,'balancing energy intake and energy output',guide(8,'3 points @ 4 marks each','(d)'))
 judged(1,'d','1-2',5,4,'trends in food shopping practices',guide(8,'5 points @ 4 marks each'))
 judged(2,'a','0-9',4,3,'options',guide(9,'4 points @ 3 marks each','(b)'))
 nutrition=guide(9,'5 points @ 4 marks each','(c)');nutrition=re.sub(r'^\(20\)\s*','',nutrition)
 judged(2,'b','0-9',5,4,'nutritional significance and the contribution to the diet','Choose EITHER fruit OR vegetables consistently. Both original source models are included; the historical nutritional statements are retained as marking guidance. '+nutrition)
 vitamin=guide(9,'(c)');headings=['biological functions','effects of deficiency','properties'];bodies=named(vitamin,['• '+h if '• '+h in vitamin else '\uf0b7 '+h for h in headings]);rows=[]
 for i,(heading,body) in enumerate(zip(headings,bodies),1):rows.append(criterion(f'heading-{i}',heading,3,[0,2],select(body,'(3 points @ 2 marks each)')))
 add(2,'c','0-8',18,rows,'3 required headings × 3 points × 2')
 safety=guide(10,'2 points under each heading','(b)');heads=['Storage –','Cooking & reheating –','Kitchen hygiene –'];add(3,'a','0-4',24,[criterion(f'heading-{i}',label[:-2],2,[0,4],body) for i,(label,body) in enumerate(zip(heads,named(safety,heads)),1)],'3 required headings × 2 points × 4')
 preservation=guide(10,'Methods – Jam/chutney making, bottling, drying','(c)');heads=['Jam/chutney making','Bottling –','Drying –'];names=['Jam/chutney making','Bottling','Drying'];variants=[]
 for i,(name,body) in enumerate(zip(names,named(preservation,heads)),1):variants.append(dict(id=f'source-{i}',label=name,rows=[point('name',name,4),criterion('principle','Principle involved',3,[0,4],'Three principle points for this SAME selected method. Complete source: '+body)]))
 variants.append(dict(id='another-method',label='Another valid method',rows=[criterion('name','Name method of preservation',1,[0,4],'Choose a valid method involving application of heat. The source lists jam/chutney making, bottling and drying.'),criterion('principle','Principle involved',3,[0,4],'Three matching principle points for that SAME method, at four marks each. No further model is printed.')]))
 add(3,'b','0-3',16,deepcopy(variants[0]['rows']),'Name 4 + principle 3 × 4',answerVariants=variants)
 judged(3,'c','0-4',2,5,'role of the Department of Agriculture, Food and the Marine',guide(10,'2 points @ 5 marks each'))
 housing=guide(11,'2 points under each heading','(b)');heads=['Economic factors –','Housing policy –','Trends –'];add(4,'a','3-3',24,[criterion(f'heading-{i}',label[:-2],2,[0,4],body) for i,(label,body) in enumerate(zip(heads,named(housing,heads)),1)],'3 required headings × 2 points × 4')
 mortgage=guide(11,'Annuity, Endowment, Pension linked, Interest only, Tracker, Current Account etc');heads=['Annuity –','Endowment –','Pension linked –','Interest only –','Tracker –','Current account –'];variants=[]
 for i,(label,body) in enumerate(zip(heads,named(mortgage,heads)),1):
  name=label[:-2];variants.append(dict(id=f'source-{i}',label=name,rows=[point('name',name,4),criterion('description','Description',2,[0,5],'Two description points for the SAME mortgage. Historical 2012 source: '+body)]))
 variants.append(dict(id='another-mortgage',label='Another valid mortgage',rows=[criterion('name','Name',1,[0,4],'One mortgage type. Source examples are Annuity, Endowment, Pension linked, Interest only, Tracker and Current account.'),criterion('description','Description',2,[0,5],'Two matching description points for that SAME mortgage. No additional source model is printed.')]))
 add(4,'b','1-1',14,deepcopy(variants[0]['rows']),'Name 4 + description 2 × 5',answerVariants=variants)
 housing=guide(12,'Tenant purchase scheme; shared ownership scheme; mortgage allowance scheme; affordable housing scheme');heads=['Tenant purchase scheme –','Mortgage allowance scheme –','Shared ownership scheme –','Affordable housing scheme –','Rental Accommodation Scheme (RAS 2004) –','Tenant Purchase of Apartments Scheme (TPAS 2012) –'];variants=[]
 for i,(label,body) in enumerate(zip(heads,named(housing,heads)),1):
  name=label[:-2];variants.append(dict(id=f'source-{i}',label=name,rows=[point('name',name,3),criterion('details','Details',3,[0,3],'Three details for the SAME scheme. Historical 2012 conditions: '+body)]))
 variants.append(dict(id='another-scheme',label='Another valid scheme',rows=[criterion('name','Name of scheme',1,[0,3],'One Local Authority housing scheme. The original scheme provides six models.'),criterion('details','Details',3,[0,3],'Three details matching that SAME housing scheme. No further source model is printed.')]))
 add(4,'c','3-3',12,deepcopy(variants[0]['rows']),'Name 3 + details 3 × 3',answerVariants=variants)
 judged(5,'a','2-0',4,3,'rights of children',guide(13,'4 points @ 3 marks each','(b)'))
 difficulties=guide(13,'Child –','(c)');child=select(difficulties,'shortage','Parent –',True);parent=select(difficulties,'Parent –','(some points');common='The source states that some points may be common to both child and parent.'
 for key,label,body in [('child','child',child),('parent','parent',parent)]:
  c=judged(5,'b','2-0',3,4,'difficulties',body+' '+common);c.update(id=f'he-2012-hl-sb-q5b-{key}',questionRef=f'2012 HL Section B Q5(b) — {label}',totalMarks=12)
  c['questionText']='Discuss each of the following: • '+prompt(5,'b').split('• ')[1 if key=='child' else 2].strip();c['questionText']=re.sub(r'\s+and\s*$','',c['questionText'])
 judged(5,'c','2-0',2,7,'Childcare Act, 1991',guide(13,'2 points @ 7 marks each').replace('(14)','').strip())
 assert len(cards)==17 and sum(c['totalMarks'] for c in cards)==280
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('B',cards,dict(tasks=17,marks=280,selectionDecisions='Independent B5(b) child/parent asks at12 each. Preserve required food-group and heading quotas, one carbohydrate profile with original diagrams, and chosen preservation/mortgage/housing-scheme dependencies with complete method-specific models.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
