#!/usr/bin/env python3
"""2011 Ordinary C: complete source guidance and unaltered elective choices."""
from he_review_2011_ol_main import *
from paper import strip_set_lines
def build():
 d=documents();p={n:re.sub(r'(\d)\.\s+\(([abc])\)',r'\1.(\2)',text(d['paper'],n+8)) for n in [1,2,3]};s={n:text(d['scheme'],n) for n in range(15,21)};cards=[]
 # The original page9 is strip-set; join original glyphs by baseline once.
 p[1]=tidy(' '.join(t for _,t in strip_set_lines(d['paper'][8]) if not t.startswith('Page ')))
 def part(n,letter):
  v=select(p[n],f'{n}.({letter})',f'{n}.({chr(ord(letter)+1)})' if f'{n}.({chr(ord(letter)+1)})' in p[n] else None)
  return re.sub(r'\s+(?:and|or)\s*$','',v).strip()
 def add(n,letter,roman,topic,marks,rows,notation,**extra):
  v=part(n,letter);prompt=select(v,f'({roman})');prompt=re.split(r'\((?:i|ii|iii)\)',prompt,1)[0];prompt=re.sub(r'\s*\(\d+\)\s*$','',prompt).strip().replace('\uf0b7','•')
  stem=v.split('(i)',1)[0].strip();c=card(f'sc-q{n}{letter}{roman}','C',f'E{n} Q{n}({letter})({roman})',topic,prompt,stem,marks,rows,n+8,notation,**extra)
  if n==1 and letter=='a':c.update(questionFigureKey='home-economics-2011-ol-sc-q1-houses',questionFigureIncludesPrompt=False)
  if n==3 and letter=='a':c['stem']=c['stem'].split('Poverty in Ireland 2008',1)[0].strip();c.update(questionFigureKey='home-economics-2011-ol-sc-q3-poverty',questionFigureIncludesPrompt=False)
  cards.append(c);return c
 def guide(page,token,end=None):return select(s[page],token,end)
 def judged(n,letter,roman,topic,count,per,label,guidance,**extra):
  return add(n,letter,roman,topic,count*per,[criterion('points',label,count,[0,per],'Distinct points at the source’s printed value, with no finer ladder invented. Complete source guidance: '+guidance)],f'{count} points × {per}',**extra)
 housing=guide(15,'Refer to:','(ii)');judged(1,'a','i','3-3',4,5,'factors','Address all three required headings: social, economic and environmental. Four points TOTAL; the source does not assign a quota to each heading. '+housing)
 judged(1,'a','ii','3-3',2,5,'housing requirements',guide(15,'2 @ 5 marks','(iii)'))
 renting=re.sub(r'\s+and$','',guide(15,'2 advantages @ 5 marks, 2 disadvantages @ 5 marks'));add(1,'a','iii','3-3',20,[criterion('advantages','advantages',2,[0,5],select(renting,'Advantages','Disadvantages')),criterion('disadvantages','disadvantages',2,[0,5],select(renting,'Disadvantages'))],'2 advantages × 5 + 2 disadvantages × 5')
 heating=guide(16,'x type of heating system','x fuel / energy source');fuel=guide(16,'x fuel / energy source','x method of heat transfer');transfer=guide(16,'x method of heat transfer','(ii)')
 add(1,'b','i','3-5',14,[criterion('type','type of heating system',1,[0,6],'Describe ONE selected system, not only its name. Source examples: '+select(heating,'6 marks')),criterion('fuel','fuel / energy source',1,[0,4],'A fuel/energy source for that SAME system. Source: '+select(fuel,'4 marks')),criterion('transfer','method of heat transfer',1,[0,4],'Heat transfer for that SAME system. Source: '+select(transfer,'4 marks'))],'Heating system6 + fuel4 + heat transfer4')
 controls=re.sub(r'\s+or$','',guide(16,'Explanation: 2 @ 4 marks','1.(c)'));rows=[];groups=[]
 for i in [1,2]:
  rows.extend([criterion(f'control-{i}','controls',1,[0,4],'Choose a different control in each pair. Source: '+controls),criterion(f'explanation-{i}','Explanation',1,[0,4],'How this SAME control ensures efficient energy use. The source gives no model explanation for its radiator-thermostat example. Full source: '+controls)])
  groups.append(dict(sourceCardId=f'he-2011-ol-sc-q1bii-pair-{i}',label=f'Heating control {i}',marks=8,rowIds=[f'control-{i}',f'explanation-{i}']))
 add(1,'b','ii','3-5',16,rows,'2 controls × 4 + 2 explanations × 4',taskGroups=groups)
 judged(1,'c','i','3-5',3,4,'artificial methods of ventilation',guide(16,'3 points @ 4 marks','(ii)'))
 ventilation=guide(16,'Underlying principle - 2 points @ 3 marks each');names=chosen(ventilation,['extractor fan','cooker hood','air conditioning']);add(1,'c','ii','3-5',18,[menu('name','Name',1,4,names),criterion('description','Description',2,[0,4],'Two description points for the SAME selected method. The source models an extractor fan and lists two alternatives. Full guidance: '+ventilation),criterion('principle','Underlying principle',2,[0,3],'Two principle points for that SAME method. Full source guidance: '+ventilation)],'Name4 + description2 × 4 + principle2 × 3')
 judged(2,'a','i','3-8',1,10,'Sketch',guide(17,'Sketch = 10 marks','(ii)'))
 fabric=guide(17,'Fabric:','2 reasons @ 3 marks');reasons=guide(17,'Reasons:','(iii)');c=add(2,'a','ii','3-7',9,[menu('fabric','Fabric',1,3,[v.strip() for v in examples(fabric).split(',') if v.strip()]),criterion('reasons','reasons',2,[0,3],'Two reasons for this SAME fabric in the outfit you designed. Complete source guidance: '+reasons)],'Fabric3 + 2 reasons × 3');c['stem']+='\n\n'+select(part(2,'a'),'(i)','(ii)')
 principles=re.sub(r'\s+and$','',guide(17,'Name – 3 marks Explain – 3 marks','2.(b)'));c=add(2,'a','iii','3-8',6,[menu('name','Name',1,3,chosen(principles,['Proportion','Balance','Emphasis','Repetition'])),criterion('explanation','Explain',1,[0,3],'Explain the SAME principle as shown on your own sketch. Full source examples: '+principles)],'Name3 + explanation3');c['stem']+='\n\n'+select(part(2,'a'),'(i)','(ii)')
 finishpart=select(s[17],'2.(b)');finishwhy=select(select(finishpart,'(i)','(ii)'),'2 reasons @ 3 marks');judged(2,'b','i','3-7',2,3,'fabric finishes',finishwhy)
 finishes=re.sub(r'\s+or$','',select(finishpart,'name - 3 marks description - 3 marks example of use - 3 marks'));add(2,'b','ii','3-7',9,[menu('name','name',1,3,chosen(finishes,['crease resistant','mercerising','waterproof','anti-static','stain resistant'])),criterion('description','description',1,[0,3],'Describe the SAME selected finish. Source: '+finishes),criterion('use','example of use',1,[0,3],'Sportswear use matching that SAME finish. Source: '+finishes)],'Name3 + description3 + matching use3')
 factors=guide(18,'3 factors @ 3 marks each','(ii)');heads=['x available money','x climate','x cultural influences.'];add(2,'c','i','3-8',9,[criterion(f'factor-{i}',head[2:],1,[0,3],body[2:]) for i,(head,body) in enumerate(zip(heads,named(factors,heads)),1)],'3 required factors × 3')
 judged(2,'c','ii','3-8',2,3,'media',guide(18,'2 points @ 3 marks'))
 definition=select(select(s[19],'(i)','(ii)'),'(6)');add(3,'a','i','3-9',6,[point('definition',definition,6,'The scheme prints one six-mark definition, without a finer ladder.')],'Definition6')
 poverty=guide(19,'4 reasons @ 6 marks','(iii)');judged(3,'a','ii','3-9',4,6,'reasons',poverty)
 groups=guide(19,'Social groups:','Effects of poverty:');effects=re.sub(r'\s+and$','',guide(19,'Effects of poverty:'))
 add(3,'a','iii','3-9',20,[menu('groups','Social groups',2,4,chosen(groups,['travellers and other minority groups','homeless people','refugees','people with alcohol, drug and gambling problems','children','lone-parent families','disabled','long term unemployed','elderly'])),criterion('effects','Effects of poverty',3,[0,4],'THREE effects TOTAL across the TWO groups named, not three for each group. Full historical source guidance: '+effects)],'2 groups × 4 + 3 effects TOTAL × 4')
 leisure=guide(20,'4 points @ 5 marks','(ii)');judged(3,'b','i','3-11',4,5,'leisure','Address both required headings: function of leisure and children’s physical development. Four points TOTAL; no per-heading allocation is printed. '+leisure)
 choices=re.sub(r'\s+or$','',guide(20,'2 factors @ 5 marks','3.(c)'));judged(3,'b','ii','3-11',2,5,'factors',choices)
 judged(3,'c','i','3-10',3,5,'factors',guide(20,'3 points @ 5 marks','(ii)'))
 judged(3,'c','ii','3-10',3,5,'benefits',guide(20,'3 benefits @ 5 marks'))
 assert len(cards)==21 and sum(c['totalMarks'] for c in cards)==275,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('C',cards,dict(tasks=21,marks=275,selectionDecisions='Keep all required headings and chosen-system/outfit dependencies. Four-point housing and leisure totals have no invented heading quotas. Poverty effects are three TOTAL across two groups. Full source-specified criteria and any omitted model details are visible.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
