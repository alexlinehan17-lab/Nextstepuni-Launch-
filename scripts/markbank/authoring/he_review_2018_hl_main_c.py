#!/usr/bin/env python3
"""2018 Higher electives: all paired floor/programme choices, exact published tariffs."""
from copy import deepcopy
from he_review_2018_hl_main import *
def build():
 d=documents();p={n:re.sub(r'(\d)\.\s+\(([abc])\)',r'\1.(\2)',text(d['paper'],n+8)) for n in [1,2,3]};s={n:text(d['scheme'],n) for n in range(17,26)};cards=[]
 def stripjoin(v):return re.sub(r'\s+(?:and|or)\s*$','',v).strip()
 def part(n,letter):return stripjoin(select(p[n],f'{n}.({letter})',f'{n}.({chr(ord(letter)+1)})' if f'{n}.({chr(ord(letter)+1)})' in p[n] else None))
 def prompt(n,letter,roman):
  v=part(n,letter)
  if roman:v=select(v,f'({roman})');v=re.split(r'\((?:i|ii|iii|iv)\)',v,1)[0]
  return re.sub(r'\s*\(\d+\)\s*$','',v).strip()
 def add(n,letter,roman,topic,marks,rows,notation,**extra):
  v=part(n,letter);stem=v.split('(i)',1)[0].strip() if roman else ''
  if n==2 and letter=='a':stem=stem.split('(Adored Vintage:',1)[0].strip()
  c=card(f'sc-q{n}{letter}{roman or ""}','C',f'E{n} Q{n}({letter})'+(f'({roman})' if roman else ''),topic,prompt(n,letter,roman),stem,marks,rows,n+8,notation,**extra);cards.append(c);return c
 def guide(page,token,end=None,include=False):return select(s[page],token,end,include)
 def judged(n,letter,roman,topic,count,per,label,guidance,**extra):return add(n,letter,roman,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} points × {per}',**extra)
 judged(1,'a','i','3-3',4,4,'housing requirements',guide(17,'4 points @ 4 marks each','(ii)'))
 full=guide(17,'private housing sector/owner occupied:',include=True);heads=['private housing sector/owner occupied:','private rental sector:'];add(1,'a','ii','3-3',18,[criterion(f'sector-{i}',head.rstrip(':'),3,[0,3],'Historical 2018 accommodation and legislative account. '+model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)],'BOTH housing sectors: three points3 each')
 c=judged(1,'a','iii','3-3',4,4,'house building standards',stripjoin(guide(18,'4 points @ 4 marks each','1.(b)')));c['rows'][0]['contextNote']='Discuss importance WITH REFERENCE TO regulation across four points. No separate importance/regulation quota is printed; historical 2018 source guidance retained. '+c['rows'][0]['contextNote']
 judged(1,'b','i','3-4',4,3,'factors',guide(18,'4 factors @ 3 marks each','(ii)'))
 first=table_rows(d['scheme'][17].find_tables().tables[0],d['scheme'][17])[1:];second=table_rows(d['scheme'][18].find_tables().tables[0],d['scheme'][18]);assert len(first)==3 and len(second)==5
 # The PDF table detector merges two visibly separate source rows. Split
 # only at the original text boundary, preserving each matching property pool.
 description,properties=second[0];descriptions=named(description,['Marble/travertine','Stone carpeting']);property_models=named(properties,['Cold underfoot;','Hard-wearing;']);models=first+list(zip(descriptions,property_models))+second[1:];assert len(models)==9
 full=' | '.join('Description: '+desc+' Properties: '+props for desc,props in models);full+=' '+stripjoin(guide(19,'Accept:',include=True));rows=[];groups=[]
 for i in range(1,4):
  rows += [criterion(f'description-{i}','Description',1,[0,4],f'Choose THREE different floor coverings. Give the description of selected covering {i}; the source gives no separate name tariff and no internal description split. Complete original paired models: '+full),criterion(f'properties-{i}','properties',2,[0,1],f'Two properties of the SAME selected covering {i}. Keep properties paired with its description. Cork, linoleum and concrete are accepted names only; no models are invented. '+full)]
  groups.append(dict(sourceCardId=f'he-2018-hl-sc-q1bii-floor-{i}',label=f'Floor covering {i}',marks=6,rowIds=[f'description-{i}',f'properties-{i}']))
 add(1,'b','ii','3-4',18,rows,'Three coverings×(description4 + two properties1)',taskGroups=groups)
 c=judged(1,'c','i','3-6',3,5,'sources of energy',select(s[20].split('(ii)',1)[0],'3 points @ 5 marks each'));c['rows'][0]['contextNote']='Identify/elaborate on ANY THREE sources AND discuss sustainability of EACH. Each complete source/sustainability account earns five marks; no required mix of energy-source types or internal mark split. All described and name-only alternatives remain available. '+c['rows'][0]['contextNote']
 c=judged(1,'c','ii','3-6',3,5,'emissions',select(guide(20,'(ii)'),'3 points @ 5 marks each'));c['rows'][0]['contextNote']='Give three accounts linking emissions to their environmental effects. No fixed climate/acid-rain/smog quota or separate emission/effect allocation is printed. '+c['rows'][0]['contextNote']
 judged(2,'a','i','3-8',3,5,'personality',guide(21,'3 points @ 5 marks each','(ii)'),questionFigureKey='home-economics-2018-hl-sc-q2-outfits',questionFigureIncludesPrompt=False)
 judged(2,'a','ii','3-8',2,5,'technological influences',stripjoin(guide(21,'2 points @ 5 marks each')))
 c=judged(2,'b','i','3-7',3,3,'natural fibres',select(s[22].split('(ii)',1)[0],'3 points @ 3 marks each'));c['rows'][0]['contextNote']='Classify fibres WITH examples and uses in each case across three points. The source does not allocate separate marks to class, example or use, or require three classes. '+c['rows'][0]['contextNote']
 c=judged(2,'b','ii','3-7',3,2,'burning test',stripjoin(select(select(s[22].split('2.(c)',1)[0],'(ii)'),'3 points @ 2 marks each')));c['rows'][0]['contextNote']='Explain identification by burning test AND give ONE example across three points. No separate example allocation or fixed flame/smell/ash quota is printed. '+c['rows'][0]['contextNote']
 judged(2,'c','i','3-8',3,3,'modification',select(guide(22,'2.(c)'),'3 points @ 3 marks each','(ii)'))
 full=guide(22,'Lengthen or shortening commercial pattern;',include=True);variants=[]
 for i,(label,start,end) in enumerate([('lengthen','lengthen -','reduce pattern -'),('shortening','reduce pattern -',None)],1):variants.append(dict(id=f'method-{i}',label=label,rows=[point('method',label,2),criterion('description','Description',2,[0,2],'Two description points for the SAME selected modification. '+select(full,start,end,True))]))
 variants.append(dict(id='other-method',label='Another valid modification method',rows=[criterion('method','Method',1,[0,2],'Choose ONE method consistently. The original scheme models lengthening and shortening; no additional model is invented.'),criterion('description','Description',2,[0,2],'Two points describing the SAME selected method; no additional source model is printed.')]))
 add(2,'c','ii','3-8',6,deepcopy(variants[0]['rows']),'Method2 + two description points2',answerVariants=variants)
 full=guide(23,'Junior Certificate:',include=True)+' '+guide(24,'work (60%);','(ii)',True);heads=['Junior Certificate:','Junior Cycle:','Transition Year Programme:','Leaving Certificate Programme:','LCVP:','LCA:'];programmes=named(full.split('Accept:',1)[0],heads);assert len(programmes)==6
 rows=[menu('names','Name',2,2,[head.rstrip(':') for head in heads]+['PLC courses'],'Choose ANY TWO different programmes. Historical 2018 names and programme descriptions retained.')];groups=[]
 for i in [1,2]:
  for key,label in [('curriculum','curriculum'),('assessment','assessment/examination systems')]:rows.append(criterion(f'{key}-{i}',label,1,[0,4],f'Give the {label} for the SAME programme {i} selected above. This is a whole four-mark criterion; no internal split is printed. All six complete original paired models, including LCVP across the page break: '+' | '.join(programmes)+' PLC courses are accepted by name only; no curriculum/assessment model is invented.'))
 add(3,'a','i','3-10',20,rows,'Two programmes×(name2 + curriculum4 + assessment4)')
 judged(3,'a','ii','3-10',3,5,'educational achievement',select(select(s[24],'(ii)','(iii)'),'3 points @ 5 marks each'))
 judged(3,'a','iii','3-10',3,5,'equality of opportunity',stripjoin(select(guide(24,'(iii)'),'3 points @ 5 marks each')))
 judged(3,'b','i','3-11',3,5,'community',guide(25,'Community:','(ii)',True))
 judged(3,'b','ii','3-11',3,5,'Volunteer',stripjoin(guide(25,'Volunteer:','3.(c)',True)))
 judged(3,'c','i','3-11',3,5,'value of leisure',select(select(s[25],'3.(c)','(ii)'),'3 points @ 5 marks each'))
 full=guide(25,'(1 reference to social, 1 reference to cultural + 1 other point)');heads=['Social:','Cultural Influences:'];add(3,'c','ii','3-11',15,[criterion(f'heading-{i}',head.rstrip(':'),1,[0,5],model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)]+[criterion('other','1 other point',1,[0,5],'One ADDITIONAL point from either required category. '+full)],'Social5 + cultural5 + one additional point5')
 assert len(cards)==20 and sum(c['totalMarks'] for c in cards)==275,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('C',cards,dict(tasks=20,marks=275,selectionDecisions='Both housing sectors, unrestricted importance/regulation points, nine full flooring profiles plus three name-only alternatives, linked energy/sustainability and emission/effect accounts, all four outfits, original unsplit fibre/burning-test tariffs, matching pattern methods and six complete programme models including the LCVP continuation plus PLC acceptance, and social/cultural/additional leisure quota.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
