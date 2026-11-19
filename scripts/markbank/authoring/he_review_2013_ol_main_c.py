#!/usr/bin/env python3
"""2013 Ordinary electives: complete original profiles and required/flexible quotas."""
from copy import deepcopy
from he_review_2013_ol_main import *
def build():
 d=documents();p={n:re.sub(r'(\d)\.\s+\(([abc])\)',r'\1.(\2)',text(d['paper'],n+8)) for n in [1,2,3]};s={n:text(d['scheme'],n) for n in range(14,21)};cards=[]
 # The original visible page has one heading; its hidden layer repeats it.
 s[20]=s[20].replace('• young adults • young adults','• young adults')
 def part(n,letter):
  v=select(p[n],f'{n}.({letter})',f'{n}.({chr(ord(letter)+1)})' if f'{n}.({chr(ord(letter)+1)})' in p[n] else None)
  return re.sub(r'\s+(?:and|or)\s*$','',v).strip()
 def prompt(n,letter,roman):
  v=part(n,letter)
  if roman:v=select(v,f'({roman})');v=re.split(r'\((?:i|ii|iii|iv)\)',v,1)[0]
  return re.sub(r'\s*\(\d+\)\s*$','',v).strip().replace('\uf0b7','•')
 def add(n,letter,roman,topic,marks,rows,notation,**extra):
  v=part(n,letter);stem=v.split('(i)',1)[0].strip() if roman else ''
  c=card(f'sc-q{n}{letter}{roman or ""}','C',f'E{n} Q{n}({letter})'+(f'({roman})' if roman else ''),topic,prompt(n,letter,roman),stem,marks,rows,n+8,notation,**extra);cards.append(c);return c
 def guide(page,token,end=None):return select(s[page],token,end)
 def judged(n,letter,roman,topic,count,per,label,guidance,**extra):return add(n,letter,roman,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} points × {per}',**extra)
 areas=guide(14,'areas:','reasons:');reason=guide(14,'reasons:','(ii)');c=add(1,'a','i','3-6',12,[menu('areas','areas',2,4,chosen(areas,['walls','roof']),'The TWO original priority areas.'),criterion('reason','reasons',1,[0,4],'The source awards ONE reason at 4 marks, not a separate reason for each area. Source: '+reason)],'Two areas4 each + one reason4',questionFigureKey='home-economics-2013-ol-sc-q1-heat-loss',questionFigureIncludesPrompt=False);c['rows'][0]['openList']=False
 insulate=guide(14,'Description 2 points @ 4 marks');roof,walls=named(insulate,['• attic / roof','• walls.']);roof+=' Original label is fire blanket insulation; its accompanying description specifies glass/mineral fibre strips.';rows=[];groups=[]
 for key,label,body in [('roof','attic / roof',roof),('walls','walls',walls)]:
  rows.extend([criterion(f'{key}-name','Name',1,[0,4],'Name ONE appropriate method for '+label+'. Complete original models: '+body),criterion(f'{key}-description','Description',1,[0,4],'Describe the SAME method for '+label+'. Complete original models: '+body)]);groups.append(dict(sourceCardId=f'he-2013-ol-sc-q1aii-{key}',label=label,marks=8,rowIds=[f'{key}-name',f'{key}-description']))
 add(1,'a','ii','3-6',16,rows,'Roof and wall each name4 + description4',taskGroups=groups)
 judged(1,'a','iii','3-6',3,4,'advantages',guide(15,'3 advantages @ 4 marks each','(iv)'))
 judged(1,'a','iv','3-5',2,5,'thermostats',re.sub(r'\s+and$','',guide(15,'2 ways @ 5 marks each','1.(b)')))
 factors=guide(15,'(identify = 3 points @ 2 marks, 3 factors @ 4 marks)','(ii)');rows=[];groups=[]
 for i in [1,2,3]:
  rows.extend([criterion(f'identify-{i}','identify',1,[0,2],'Identify one of THREE DIFFERENT factors for kitchen wall finishes. Complete source: '+factors),criterion(f'discuss-{i}','factors',1,[0,4],'Discuss the SAME identified factor. Complete source: '+factors)]);groups.append(dict(sourceCardId=f'he-2013-ol-sc-q1bi-factor-{i}',label=f'Factor {i}',marks=6,rowIds=[f'identify-{i}',f'discuss-{i}']))
 add(1,'b','i','3-4',18,rows,'Three linked factors identify2/discuss4 each',taskGroups=groups)
 tiles=re.sub(r'\s+or$','',guide(15,'(1 advantage, 1 disadvantage + 1 other)','1.(c)'));advantages,disadvantages=named(tiles,['Advantages','Disadvantages']);add(1,'b','ii','3-4',12,[criterion('advantage','Advantages',1,[0,4],advantages),criterion('disadvantage','Disadvantages',1,[0,4],disadvantages),criterion('other','1 other',1,[0,4],'ONE additional distinct point from either heading, as printed. Complete source: '+tiles)],'One advantage4 + one disadvantage4 + one other4')
 judged(1,'c','i','3-3',3,4,'renting',select(select(s[15],'1.(c)'),'3 points @ 4 marks each'))
 judged(1,'c','ii','3-3',3,6,'considerations',guide(16,'3 points @ 6 marks each'))
 outfit=guide(17,'Sketch = 3 marks, description = 6 marks','(ii)');add(2,'a','i','3-8',9,[criterion('sketch','Sketch',1,[0,3],'Sketch ONE leisure/outdoor outfit. The source prints this tariff but NO model drawing. General original guidance: '+outfit),criterion('description','description',1,[0,6],'Describe the SAME outfit. The source provides generic qualities, not a complete named outfit: '+outfit)],'Sketch3 + description6')
 evaluation=re.sub(r'\s+and$','',guide(17,'(one reference to each heading)','2.(b)'));heads=['• function (use)','• fashion appeal','• cost','• care.'];bodies=named(evaluation,heads);c=add(2,'a','ii','3-8',16,[criterion(f'heading-{i}',h.removeprefix('• ').rstrip('.'),1,[0,4],'Evaluate the SAME outfit from part(i). Original heading guidance: '+re.sub(r'^\(16\)\s*','',body)) for i,(h,body) in enumerate(zip(heads,bodies),1)],'Four required evaluation headings × 4');c['stem']+='\n\n'+prompt(2,'a','i')
 production=guide(17,'• fibre production','• properties');properties=guide(17,'• properties');construction=re.sub(r'\s+or$','',guide(18,'• how fabric is constructed','2.(c)'));prod=named(production,['linen:','Cotton:','Wool:','Silk:']);props=named(properties,['Linen:','Cotton:','Wool:','Silk:']);variants=[]
 for i,(label,one,two) in enumerate(zip(['Linen','Cotton','Wool','Silk'],prod,props),1):variants.append(dict(id=f'fabric-{i}',label=label,rows=[criterion('production','fibre production',1,[0,5],'One account of this SAME natural fibre. Original model: '+one),criterion('properties','properties',1,[0,5],'Properties of the SAME chosen fabric. Original model: '+two),criterion('construction','how fabric is constructed',1,[0,5],'Construction of the SAME chosen fabric. Complete original construction models: '+construction)]))
 variants.append(dict(id='another-fabric',label='Another natural fabric',rows=[criterion('production','fibre production',1,[0,5],'Account of the SAME chosen natural fibre. The scheme models linen/cotton/wool/silk only; no further individual production model is printed.'),criterion('properties','properties',1,[0,5],'Properties of the SAME chosen fabric. No additional individual model is printed.'),criterion('construction','how fabric is constructed',1,[0,5],'Construction of the SAME chosen fabric. Original applicable models: '+construction)]))
 c=add(2,'b',None,'3-7',15,deepcopy(variants[0]['rows']),'Three required profile headings × 5; no separate name tariff',answerVariants=variants);original=part(2,'b');c['stem']=original.split('Give an account',1)[0].strip();c['questionText']='Give an account'+prompt(2,'b',None).split('Give an account',1)[1]
 judged(2,'c','i','3-8',3,3,'factors',guide(18,'3 factors @ 3 marks each','(ii)'))
 judged(2,'c','ii','3-8',3,2,'functions',guide(18,'3 functions @ 2 marks each'))
 development=guide(19,'4 points @ 6 marks each','(ii)');heads=['• physical development','• emotional development','• moral development','• intellectual development'];add(3,'a','i','3-10',24,[criterion(f'heading-{i}',head.removeprefix('• '),1,[0,6],body) for i,(head,body) in enumerate(zip(heads,named(development,heads)),1)],'Four required development headings × 6')
 judged(3,'a','ii','3-10',4,4,'factors',guide(19,'4 factors @ 4 marks each','(iii)'))
 preschool=re.sub(r'\s+and$','',guide(19,'2 points @ 5 marks each'));heads=['Early Childhood Care and Education (ECCE) Scheme','Early Start Project / Pre-School Programme'];variants=[dict(id=f'scheme-{i}',label=head,rows=[criterion('details','pre-school education',2,[0,5],'Two details about ONE chosen historical scheme; no separate name allocation is printed. Original model: '+body)]) for i,(head,body) in enumerate(zip(heads,named(preschool,heads)),1)];variants.append(dict(id='another-scheme',label='Another government pre-school scheme',rows=[criterion('details','pre-school education',2,[0,5],'Two matching details about ONE historical government scheme. No further model is printed in the 2013 source.')]))
 add(3,'a','iii','3-10',10,deepcopy(variants[0]['rows']),'Two details × 5; no separate name tariff',answerVariants=variants)
 unemployment=guide(20,'3 points @ 6 marks each','(ii)');young,families=named(unemployment,['• young adults','• families with young children.']);add(3,'b','i','3-9',18,[criterion('young','young adults',1,[0,6],young),criterion('families','families with young children',1,[0,6],families),criterion('other','negative effects',1,[0,6],'ONE further point across either group. The paper requires BOTH groups within THREE total source points; no two-per-group quota. Complete source: '+unemployment)],'Both required groups within three total points × 6')
 poverty=re.sub(r'\s+or$','',guide(20,'2 points @ 6 marks each','3.(c)'));heads=['Relative Poverty:','Absolute Poverty:'];add(3,'b','ii','3-9',12,[criterion(f'type-{i}',head[:-1],1,[0,6],body) for i,(head,body) in enumerate(zip(heads,named(poverty,heads)),1)],'Relative6 + absolute6')
 community=select(s[20],'3.(c)');judged(3,'c','i','3-11',3,5,'voluntary work',select(select(community,'(i)','(ii)'),'3 points @ 5 marks each'))
 impact=select(select(community,'(ii)'),'3 points @ 5 marks each');positive,negative=named(impact,['Positive:','Negative:']);add(3,'c','ii','3-11',15,[criterion('positive','Positive',1,[0,5],positive),criterion('negative','Negative',1,[0,5],negative),criterion('other','impact',1,[0,5],'ONE further point across either side. The paper requires BOTH positive and negative impacts within THREE total source points, not two per side. Complete source: '+impact)],'Both required sides within three total points × 5')
 assert len(cards)==20 and sum(c['totalMarks'] for c in cards)==275,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('C',cards,dict(tasks=20,marks=275,selectionDecisions='All required/flexible quotas retained. Paired roof/wall profiles8 each, one shared insulation reason4, factor2/4 pairs, outfit sketch3/description6 with no model drawing, complete natural-fabric variants and continued construction guidance. Historical pre-school details5+5 without name price; both required groups/sides within three total points.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
