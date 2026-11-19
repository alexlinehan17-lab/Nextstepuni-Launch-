#!/usr/bin/env python3
"""Review all 27 Ordinary Section C tasks against every source continuation."""
from copy import deepcopy
import json,sys
from he_review_2021_ol_main import documents,page_text,originals,save_batch,criterion,named_sections


def build():
 d=documents();s={n:page_text(d['scheme'],n) for n in range(15,26)};old=originals();fixes={}
 def body(n,start,end=None):
  assert start in s[n],(n,start)
  t=s[n].split(start,1)[1];assert end is None or end in t,(n,end)
  return (t.split(end,1)[0] if end else t).strip()
 def put(key,marks,notation,rows,**extra):
  fixes['he-2021-ol-sc-'+key]=dict(reason='Full 2021 Ordinary C review: all required headings, complete original images and continued scheme guidance, exact published partial credit.',set=dict(totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,**extra))
 def points(key,marks,count,steps,text,label='points',**extra):
  grade=':'.join(str(n) for n in reversed(steps));put(key,marks,f'{count} points × {steps[-1]} ({grade})',[criterion('points',label,count,steps,f'{count} distinct points, each graded {grade}. Complete historical guidance: '+text)],**extra)
 def headings(key,labels,values,count,steps,extra_note='',**extra):
  grade=':'.join(str(n) for n in reversed(steps));put(key,len(labels)*count*steps[-1],f'{len(labels)} required headings × {count} points × {steps[-1]} ({grade})',[criterion(f'heading-{i}',label,count,steps,f'{count} points under this required heading, each graded {grade}. '+extra_note+'Complete guidance: '+text) for i,(label,text) in enumerate(zip(labels,values),1)],**extra)
 image=dict(questionFigureKey='home-economics-2021-ol-sc-q1a-heat-loss',questionFigureIncludesPrompt=False,stem='The diagram below shows the average heat loss for a family home.')
 points('q1ai',20,4,[0,3,5],body(15,'4 advantages @ 5 marks each (graded 5:3:0)','(ii)'),label='advantages',**image)
 parts=named_sections(body(15,'Description: 3 marks (graded 3:0)').replace('(www.ors.ie)',''),['(a) attic:','(b) walls:','(c) windows:']);rows=[]
 for i,(label,text) in enumerate(zip(['Attic','Walls','Windows'],parts),1):
  rows += [criterion(f'name-{i}',label+' — method',1,[0,2],'Name a method for this required location, graded 2:0. Complete location-specific guidance: '+text),criterion(f'description-{i}',label+' — description',1,[0,3],'Describe the same method for this location, graded 3:0; no intermediate marks. Use the full guidance above.')]
 put('q1aii',15,'3 locations × (name 2 (2:0) + description 3 (3:0))',rows,taskGroups=[dict(sourceCardId=f'he-2021-ol-sc-q1aii-location-{i}',label=name,marks=5,rowIds=[f'name-{i}',f'description-{i}']) for i,name in enumerate(['Attic','Walls','Windows'],1)],**image)
 points('q1aiii',15,3,[0,3,5],'Solar output and savings depend on the installation and conditions; the historical 80% example is not a guaranteed reduction. '+body(16,'3 points @ 5 marks each (graded 5:3:0)','and 1.(b)'),label='points',**image)
 home=body(16,'1 advantage + 1 disadvantage + 1 other point','(ii)');values=named_sections(home,['Advantages:','Disadvantages:'])
 put('q1bi',12,'1 advantage + 1 disadvantage + 1 other, each 4 (4:2:0)',[criterion('advantage','Advantage',1,[0,2,4],'One advantage, graded 4:2:0. Historical examples, not guarantees about prices, grants or investment returns. '+values[0]),criterion('disadvantage','Disadvantage',1,[0,2,4],'One disadvantage, graded 4:2:0. '+values[1]),criterion('other','other',1,[0,2,4],'One further distinct advantage or disadvantage, graded 4:2:0. Use the complete guidance above.')])
 points('q1bii',18,3,[0,3,6],body(16,'3 points @ 6 marks each (graded 6:3:0)'),label='points')
 points('q1ci',15,3,[0,3,5],body(17,'3 factors @ 5 marks each (graded 5:3:0)','(ii)'),label='factors')
 points('q1cii',15,3,[0,3,5],s[17].rsplit('3 factors @ 5 marks each (graded 5:3:0)',1)[1].strip(),label='factors')
 outfits=named_sections(body(18,'(18 marks)','(ii)'),['Woman:','Man:']);outfit_parts=[named_sections(t,['shape:','comfort:','design features:']) for t in outfits]
 image=dict(questionFigureKey='home-economics-2021-ol-sc-q2a-occasion-wear',questionFigureIncludesPrompt=False,stem='‘Fashions fade, style is eternal.’ (Yves Saint Laurent)')
 headings('q2ai',['Shape','Comfort','Design features'],['Dress: '+outfit_parts[0][i]+' Suit: '+outfit_parts[1][i] for i in range(3)],2,[0,2,3],questionText='Comment on the suitability of the occasion wear shown above.\nRefer to:\n(a) shape    (b) comfort    (c) design features.',**image)
 accessories=body(18,'1 accessory @ 3 marks (graded 3:0), 1 reason @ 4 marks (graded 4:2:0)')
 put('q2aii',7,'Accessory 3 (3:0); reason 4 (4:2:0)',[criterion('accessory','Accessory',1,[0,3],'Name one accessory for either pictured outfit, graded 3:0. Complete published examples for both outfits: '+accessories),criterion('reason','Reason',1,[0,2,4],'Give one reason for the same accessory and outfit, graded 4:2:0. Use the complete guidance above.')],questionText='Suggest one accessory you could add to enhance either of the above outfits.\nGive one reason for your choice.',**image)
 construction=body(19,'Fabric construction technique:','Properties:');properties=named_sections(body(19,'Properties:','(ii)'),['Linen:','Cotton:','Wool:','Silk:']);variants=[]
 for key,name,text in zip(['linen','cotton','wool','silk','another'],['Linen','Cotton','Wool','Silk','Another natural fabric'],properties+['The paper permits another natural fabric. Give accurate properties of your named fabric; the scheme does not print another model.']):
  variants.append(dict(id=key,label=name,rows=[criterion('construction','Construction',1,[0,2,3],'One construction point, graded 3:2:0. Describe a technique that applies to the natural fabric you chose; naming it earns no separate marks. All printed construction guidance: '+construction),criterion('properties','properties',2,[0,2,3],'Two properties of the same chosen fabric, each graded 3:2:0. Complete guidance: '+text)]))
 put('q2bi',9,'Construction 3 + 2 properties × 3, each 3:2:0',deepcopy(variants[0]['rows']),answerVariants=variants)
 points('q2bii',6,2,[0,2,3],body(19,'2 advantages @ 3 marks each (graded 3:2:0)','or 2.(c)'),label='advantages')
 values=[body(19,'(a) Function:','(b) Money available:'),body(19,'(b) Money available:','(c) Cultural influences:'),body(19,'(c) Cultural influences:')]
 headings('q2ci',['Function','Money available','Cultural influences'],[v.split('(graded 3:2:0)',1)[1].strip() for v in values],1,[0,2,3])
 points('q2cii',6,2,[0,2,3],body(20,'2 contributions @ 3 marks each (graded 3:2:0)'),label='contributions')
 values=named_sections(body(21,'(18 marks)','(ii)'),['Physical development:','Emotional development:','Intellectual development:'])
 headings('q3ai',['Physical development','Emotional development','Intellectual development'],values,2,[0,2,3])
 points('q3aii',20,4,[0,3,5],body(21,'4 factors @ 5 marks each (graded 5:3:0)','(iii)'),label='factors')
 points('q3aiii',12,3,[0,2,4],body(21,'3 benefits @ 4 marks each (graded 4:2:0)'),label='benefits')
 points('q3bi',15,3,[0,3,5],body(22,'3 reasons @ 5 marks each (graded 5:3:0)','(ii)'),label='reasons')
 values=named_sections(body(22,'(15 marks)',None).split('(15 marks)',1)[1].split('or 3.(c)',1)[0],['Cost:','Occupation:','Age:'])
 headings('q3bii',['Cost','Occupation','Age'],values,1,[0,3,5],extra_note='These are possible influences, not assumptions about everyone in a group. ')
 values=named_sections(body(22,'(18 marks)')+' '+s[23].split('(ii)',1)[0],['Young individuals:','The family:','Society:'])
 headings('q3ci',['Young individuals','The family','Society'],values,2,[0,2,3],extra_note='Treat these historical examples as possible effects, not inevitable outcomes or judgements about unemployed people. ')
 support=body(23,'Name: 4 marks (graded 4:0), 2 details @ 4 marks each (graded 4:2:0)')
 put('q3cii',12,'Name 4 (4:0); 2 details × 4 (4:2:0)',[criterion('name','Voluntary organisation',1,[0,4],'Name one organisation, graded 4:0. Complete source examples and general support activities: '+support),criterion('details','details',2,[0,2,4],'Two accurate details about the same named organisation, each graded 4:2:0. The general activity list does not imply every organisation provides every listed service.')])
 values=named_sections(body(24,'2 references to nutritive value, 2 references to dietetic value, plus 1 other','(ii)'),['Nutritive value:','Dietetic Value:'])
 put('q4ai',20,'5 points × 4 (4:2:0): 2 nutritive, 2 dietetic, 1 other',[criterion('nutritive','Nutritive value',2,[0,2,4],'Two nutritive points, each graded 4:2:0. The source’s biological-value figure does not mean eggs are 100% protein. Complete guidance: '+values[0]),criterion('dietetic','Dietetic Value',2,[0,2,4],'Two dietetic points, each graded 4:2:0. Complete guidance: '+values[1]),criterion('other','other',1,[0,2,4],'One further distinct point under either heading, graded 4:2:0. Use the complete guidance above.')])
 headings('q4aii',['Ways of including eggs','Effects of heat'],[body(24,'3 ways @ 3 marks each (graded 3:2:0)','3 effects @'),body(24,'3 effects @ 3 marks each (graded 3:2:0)','(iii)')],3,[0,2,3],questionText='Outline:\n• different ways of including eggs in the diet\n• the effects of heat on eggs.')
 points('q4aiii',12,3,[0,2,4],'Local origin or small scale does not guarantee better nutrition; these are perceived qualities/examples in the historical scheme. '+body(24,'3 reasons @ 4 marks each (graded 4:2:0)'),label='reasons')
 values=named_sections(body(25,'(15 marks)','(ii)'),['Household income:','Discount offers:','Shopper loyalty schemes:'])
 headings('q4bi',['Household income','Discount offers','Shopper loyalty schemes'],values,1,[0,3,5])
 values=named_sections(body(25,'1 advantage, 1 disadvantage, plus 1 other','or 4.(c)'),['Advantages:','Disadvantages:'])
 put('q4bii',15,'1 advantage + 1 disadvantage + 1 other, each 5 (5:3:0)',[criterion('advantage','Advantage',1,[0,3,5],'One advantage, graded 5:3:0. '+values[0]),criterion('disadvantage','Disadvantage',1,[0,3,5],'One disadvantage, graded 5:3:0. '+values[1]),criterion('other','other',1,[0,3,5],'One further distinct advantage or disadvantage, graded 5:3:0. Use all guidance above.')])
 points('q4ci',15,3,[0,3,5],body(25,'3 factors @ 5 marks each (graded 5:3:0)','(ii)'),label='factors')
 points('q4cii',15,3,[0,3,5],body(25,'3 aspects @ 5 marks each (graded 5:3:0)'),label='aspects')
 assert len(fixes)==27 and sum(f['set']['totalMarks'] for f in fixes.values())==385
 return fixes,[]


def write():
 fixes,added=build();save_batch('C',fixes,added,dict(tasks=27,marks=385,selectionDecisions='Keep all required headings and dependent name/detail pairs whole. Solar advantages and/or disadvantages is flexible wording, not a finite choice. Natural-fabric profiles remain one open task with four full model routes and another-valid-fabric route. Clothing-accessory choice retains both original outfits. C4(a)(ii) is one outlined response under required headings; B3(b)(i)/(ii) are separately numbered independent tasks. Continuations retained for trendsetters and unemployment effects.',checked='2026-11-01'));print('2021 Ordinary C: 27 reviewed tasks, 385 offered marks.')

if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
