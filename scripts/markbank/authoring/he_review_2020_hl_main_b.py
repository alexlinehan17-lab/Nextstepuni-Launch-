#!/usr/bin/env python3
"""2020 Higher B: original choices, coherent profiles and exact allocations."""
from copy import deepcopy
from he_review_2020_hl_main import *
def build():
 d=documents();p={n:text(d['bc'],n) for n in range(2,5)};s={n:text(d['scheme'],n) for n in range(9,19)}
 q={1:p[2].rsplit('Question 1',1)[1].strip(),2:select(p[3],'Question 2','Question 3'),3:select(p[3],'Question 3'),4:select(p[4],'Question 4','Question 5'),5:select(p[4],'Question 5')};cards=[]
 def part(n,l):return select(q[n],f'({l})',f'({chr(ord(l)+1)})' if f'({chr(ord(l)+1)})' in q[n] else None)
 def add(n,l,topic,marks,rows,notation,**extra):
  prompt=re.sub(r'\s*\(\d+ marks\)\s*$','',part(n,l)).strip();stem=q[n].split('(a)',1)[0].strip()
  if n==1:
   stem=stem.split('Situations/Settings',1)[0].strip()
   if l!='a':stem=stem.split('The following table',1)[0].strip()
  c=card(f'sb-q{n}{l}','B',f'Q{n}({l})',topic,prompt,stem,marks,rows,2 if n==1 else 3 if n<=3 else 4,notation,**extra);cards.append(c);return c
 def guide(page,token,end=None,include=False):return select(s[page],token,end,include)
 def judged(n,l,topic,count,steps,label,guidance,**extra):return add(n,l,topic,count*steps[-1],[criterion('points',label,count,steps,guidance)],f'{count} points; original steps '+str(steps),**extra)
 judged(1,'a','0-1',5,[0,1,2,3,4],'reasons','Refer to FIVE different situations/settings from the complete ten-row original table. The source groups examples as difficult/not difficult, without fixed category quotas or a separate answer key for each situation. Complete original guidance: '+guide(9,'Difficult:',include=True),questionFigureKey='home-economics-2020-hl-sb-q1-portions',questionFigureIncludesPrompt=False)
 heads=['How a peptide bond is formed:','Essential and non-essential amino acids:','Supplementary value/complementary role:'];full=guide(10,heads[0],'(c)',True)
 add(1,'b','0-5',24,[criterion(f'heading-{i}',head.rstrip(':'),4,[0,1,2],model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)],'Three required protein headings, four points2 EACH')
 heads=['Gel formation:','Foam formation:'];full=guide(10,heads[0],include=True)
 add(1,'c','0-5',16,[criterion(f'property-{i}',head.rstrip(':'),4,[0,1,2],'Explain this REQUIRED property with culinary application. The source provides four points overall for each property, with no separate explanation/application allocation. '+model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)],'Two required protein properties, four points2 EACH')
 full=guide(11,'Shopping for food:',include=True);heads=['Shopping for food:','Eating at home:','Eating out:'];models=named(full,heads)
 add(1,'d','0-1',20,[criterion(f'category-{i}',head.rstrip(':'),1,[0,3,5],model) for i,(head,model) in enumerate(zip(heads,models),1)]+[criterion('other','1 other',1,[0,3,5],'ONE additional distinct strategy from any of the three required categories; no repeated credit. '+full)],'One shopping5 + one at home5 + one eating out5 + one other5')
 judged(2,'a','0-9',5,[0,1,2,3,4],'points',guide(12,'Protein:','(b)',True))
 full=guide(12,'Flour:','(c)',True);production=named(full.split('Packaging:',1)[0],['Flour:','Pasta:']);pack=select(full,'Packaging:','Labelling:',True);label=select(full,'Labelling:',include=True);variants=[]
 for i,name in enumerate(['Flour','Pasta','Another valid cereal product']):
  model=production[i] if i<2 else 'The paper leaves the cereal-product choice open. No further production model is printed or invented.'
  rows=[criterion('production','Production',6,[0,1,2],'Use ONE coherent '+name+' profile throughout. '+model),criterion('packaging','Packaging',1,[0,2,3],'Describe packaging appropriate to the SAME selected product. '+pack),criterion('labelling','Labelling',1,[0,2,3],'Describe labelling appropriate to the SAME selected product. '+label)]
  variants.append(dict(id=f'cereal-{i+1}',label=name,rows=rows))
 add(2,'b','0-9',18,deepcopy(variants[0]['rows']),'Production six2 + packaging3 + labelling3',answerVariants=variants)
 judged(2,'c','0-6',3,[0,2,4],'benefits',guide(12,'(graded 4:2:0)'))
 full=guide(13,'Preparation:','(b)',True);heads=['Preparation:','Storage:'];models=named(full,heads)
 add(3,'a','0-4',12,[criterion('preparation','Preparation',1,[0,2,3],models[0]),criterion('storage','Storage',1,[0,2,3],models[1]),criterion('other','2 other points',2,[0,2,3],'TWO additional distinct points from either category; no repeated credit. '+full)],'One preparation3 + one storage3 + two other3')
 grid=[]
 for pn in [13,14]:
  for t in d['scheme'][pn-1].find_tables().tables:
   rows=table_rows(t,d['scheme'][pn-1])
   grid.extend(row for row in rows if row[0].startswith(('Freezing:','Heat treatments:','Chemical preservation:','Dehydration:','Salting:')))
 assert len(grid)==5 and all(len(row)==3 for row in grid),grid
 profiles='\n\n'.join('Method: '+a+'\nUnderlying principle: '+b+'\nRisk of food spoilage: '+c for a,b,c in grid)
 rows=[];groups=[]
 for i in [1,2]:
  ids=[f'method-{i}',f'principle-{i}',f'risk-{i}'];rows += [criterion(ids[0],'Preservation method',2,[0,1,2],f'Describe method {i} of TWO DIFFERENT methods; retain the SAME method throughout its three criteria. Complete five paired original profiles (including all named submethods): '+profiles),criterion(ids[1],'Underlying principle',2,[0,1,2,3],f'Explain the principle for the SAME selected method {i}; use its matching original table column in the complete guidance above.'),criterion(ids[2],'Risk of food spoilage',1,[0,1,2,3],f'Explain a spoilage risk for the SAME selected method {i}; use its matching original table column in the complete guidance above.')];groups.append(dict(sourceCardId=f'he-2020-hl-sb-q3b-method-{i}',label=f'Preservation method {i}',marks=13,rowIds=ids))
 add(3,'b','0-4',26,rows,'TWO profiles each: method2×2 + principle2×3 + risk3',taskGroups=groups)
 heads=['Food Hygiene Regulations:','Food Information to Consumers (FIC) Regulation:','European Communities (Hygiene of Foodstuffs) Regulations:','Sale of Food and Drugs Acts:','Health Acts:'];full=guide(14,heads[0],include=True)+' '+s[15];models=named(full.split('An Bord Bia Act 1994;',1)[0],heads);labels=[h.rstrip(':') for h in heads]+['An Bord Bia Act 1994','Food Safety Authority of Ireland Act','Another valid Regulation/Act'];variants=[]
 for i,name in enumerate(labels):
  model=models[i] if i<5 else 'Accepted by name only in the source; no detail model is printed or invented.' if i<7 else 'The source leaves valid alternatives open; no further detail model is printed or invented.'
  variants.append(dict(id=f'law-{i+1}',label=name,rows=[criterion('name','Name of Act',1,[0,2,3,4],'Name ONE Regulation/Act consistently throughout. Original selected name: '+name),criterion('details','points',2,[0,2,3,4],'Two details about the SAME named Regulation/Act. The original historical 2020 legal account is retained. '+model)]))
 add(3,'c','0-4',12,deepcopy(variants[0]['rows']),'Name4 + two matching points4',answerVariants=variants)
 full=guide(16,'Name of household appliance',include=True);names=select(full,'(graded 2:0)','Selection criteria');selection=select(full,'Selection criteria','Sourcing consumer information');information=select(full,'Sourcing consumer information','Working principle');working=select(full,'Working principle','Guidelines for use');use=select(full,'Guidelines for use')
 add(4,'a','1-3',26,[criterion('name','Name of household appliance',1,[0,2],'Select ONE motorised appliance suitable for use in a kitchen, consistently throughout all five criteria. Complete original name pool: '+names),criterion('selection','Selection criteria',3,[0,1,2],'For the SAME selected appliance. '+selection),criterion('information','Sourcing consumer information',3,[0,1,2],'For the SAME selected appliance. '+information),criterion('working','Working principle',4,[0,1,2],'For the SAME selected appliance. Full refrigerator and food-processor models follow; other listed appliances are accepted by name, with no additional working model printed or invented. Labelled diagrams are accepted. '+working),criterion('use','Guidelines for use',2,[0,1,2],'For the SAME selected appliance. Full refrigerator and food-processor models follow; no additional use models are invented. '+use)],'Name2 + selection3×2 + information3×2 + working4×2 + use2×2')
 full=guide(17,'Choosing:','(c)',True);heads=['Choosing:','Using:','Disposing:'];add(4,'b','1-5',12,[criterion(f'category-{i}',head.rstrip(':'),1,[0,2,4],model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)],'ONE required choosing/using/disposing point4 EACH')
 judged(4,'c','1-2',3,[0,1,2,3,4],'points','Original historical account of the 1980 Act named in the paper: '+guide(17,'(graded 4:3:2:1:0)'))
 full=guide(18,'Post industrialisation:','(b)',True);models=named(full,['Post industrialisation:','The modern family:'])
 add(5,'a','2-0',20,[criterion('middle','middle of the century',2,[0,2,4],models[0]),criterion('present','present day',2,[0,2,4],'Present day means the original 2020 source context. '+models[1]),criterion('other','1 other',1,[0,2,4],'ONE additional distinct point from either era, without repeated credit. '+full)],'TWO mid-century4 + TWO present-day4 + ONE other4')
 heads=['Children’s/teenager’s roles and responsibilities:','Parent’s roles and responsibilities:','Grandparent’s roles and responsibilities:'];full=guide(18,heads[0],'(c)',True)
 add(5,'b','2-0',18,[criterion(f'group-{i}',head.rstrip(':'),1,[0,2,4,6],model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)],'ONE required reference6 to EACH family group')
 judged(5,'c','2-0',3,[0,2,4],'points',select(select(s[18],'(c)'),'(graded 4:2:0)'))
 assert len(cards)==16 and sum(c['totalMarks'] for c in cards)==280
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('B',cards,dict(tasks=16,marks=280,selectionDecisions='Full ten-row table, exact protein/portion quotas, coherent cereal choices, five complete preservation-table profiles in TWO selected-method slots, all legislation models and name-only alternatives, one coherent appliance profile with complete name pool, required environmental categories and historical family quotas.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
