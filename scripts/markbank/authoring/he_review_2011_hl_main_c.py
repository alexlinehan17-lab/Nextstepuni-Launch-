#!/usr/bin/env python3
"""2011 Higher electives: required headings, open choices and printed source omissions."""
from copy import deepcopy
from he_review_2011_hl_main import *
def build():
 d=documents();p={n:text(d['paper'],n+8) for n in [1,2,3]};s={n:text(d['scheme'],n) for n in range(14,20)};cards=[]
 def part(n,letter):
  v=select(p[n],f'{n}.({letter})',f'{n}.({chr(ord(letter)+1)})' if f'{n}.({chr(ord(letter)+1)})' in p[n] else None)
  return re.sub(r'\s+(?:and|or)\s*$','',v).strip()
 def add(n,letter,roman,topic,marks,rows,notation,**extra):
  v=part(n,letter);prompt=select(v,f'({roman})') if roman else v
  prompt=re.split(r'\((?:i|ii|iii)\)',prompt,1)[0] if roman else prompt
  prompt=re.sub(r'\s*\(\d+\)\s*$','',prompt).strip().replace('\uf0b7','•')
  stem=v.split('(i)',1)[0].strip() if '(i)' in v else ''
  c=card(f'sc-q{n}{letter}{roman or ""}','C',f'E{n} Q{n}({letter})'+(f'({roman})' if roman else ''),topic,prompt,stem,marks,rows,n+8,notation,**extra);cards.append(c);return c
 def guide(page,token,end=None):return select(s[page],token,end)
 def judged(n,letter,roman,topic,count,per,label,guidance,**extra):
  return add(n,letter,roman,topic,count*per,[criterion('points',label,count,[0,per],'Distinct source points at the printed value; no smaller marking steps are published. Complete source guidance: '+guidance)],f'{count} points @ {per}',**extra)
 def pool(n,letter,roman,topic,count,per,options,**extra):
  return add(n,letter,roman,topic,count*per,[menu('points','Published answer points',count,per,options)],f'{count} points @ {per}',**extra)
 housing=guide(14,'3 points @ 8 marks each','(ii)');pool(1,'a','i','3-3',3,8,[v.strip() for v in housing.split('x ') if v.strip()])
 planning=guide(14,'4 points @ 3 marks each','(iii)');judged(1,'a','ii','3-3',4,3,'procedures',planning)
 legislation=re.sub(r'\s+and$','',guide(14,'2 points @ 5 marks each'));labels=['National House Building Guarantee Scheme (Homebond)','Building Regulations Act 1991'];variants=[]
 for label,body in zip(labels,named(legislation,[v+' –' for v in labels])):
  variants.append(dict(id='homebond' if label==labels[0] else 'building-regulations',label=label,rows=[point('name',label,4),criterion('details','details',2,[0,5],'Two details of this same choice. Historical 2011 scheme example: '+body)]))
 variants.append(dict(id='another-valid-choice',label='Another valid choice',rows=[criterion('name','Name legislation',1,[0,4],'Use the examination’s 2011 context. No further source model has been invented.'),criterion('details','details',2,[0,5],'Two details for the same choice, five marks each.')]))
 add(1,'a','iii','3-3',14,deepcopy(variants[0]['rows']),'Name 4 + details 2 × 5',answerVariants=variants)
 energy=d['scheme'][14].find_tables().tables[0].extract();variants=[]
 for i,(source,advantages,sustainability) in enumerate(energy[1:],1):
  label=['Electricity','Oil','Gas','Solid fuel – coal','Solid fuel – turf/peat'][i-1]
  variants.append(dict(id=f'source-{i}',label=label,rows=[criterion('source','source',1,[0,3],'Account of this SAME energy source. Original table: '+tidy(source)),criterion('advantages','advantages/disadvantages',2,[0,4],'Two points for this SAME source. Some word endings are visibly clipped at table borders in the original scheme; the printed text is retained without inventing missing letters. Source: '+tidy(advantages).replace('CO than 2','CO2 than')),criterion('sustainability','sustainability',1,[0,4],'For this SAME energy source. Original table wording retained, including visibly clipped word endings: '+tidy(sustainability))]))
 variants.append(dict(id='another-source',label='Another valid non-renewable source',rows=[criterion('source','source',1,[0,3],'One non-renewable source, with an account of its source; no additional model is printed.'),criterion('advantages','advantages/disadvantages',2,[0,4],'Two points for the same energy source.'),criterion('sustainability','sustainability',1,[0,4],'One point about this same source.')]))
 add(1,'b','i','3-6',15,deepcopy(variants[0]['rows']),'Source 3 + advantages/disadvantages 2 × 4 + sustainability 4',answerVariants=variants)
 saving=re.sub(r'\s+or$','',guide(16,'3 points @ 5 marks each','1.(c)'));pool(1,'b','ii','3-6',3,5,named(saving,['Solar systems –','Large windows','Windows –','Insulation','Heating -','BER -','Timber framed','Sensor lighting','Cavity walls']))
 lighting=guide(16,'3 points @ 4 marks each','(ii)');pool(1,'c','i','3-5',3,4,[v.strip() for v in lighting.split('x ') if v.strip()])
 properties=guide(16,'3 points @ 6 marks each');pool(1,'c','ii','3-5',3,6,named(properties,['Reflected –','Refracted –','Diffused –','Absorbed –','Dispersed –']))
 add(2,'a','i','3-8',10,[criterion('sketch','Sketch',1,[0,4],'One sketch of the selected school-uniform outfit, four marks as printed. The scheme supplies no model sketch or smaller steps.'),criterion('description','Description',1,[0,6],'Describe that SAME outfit, six marks as printed. The scheme supplies no model description or smaller steps.')],'Sketch 4 + description 6')
 design=guide(17,'Principles of design i.e.','Suitability for purpose');purpose=re.sub(r'\s+and$','',guide(17,'Suitability for purpose -','2.(b)'))
 c=add(2,'a','ii','3-8',15,[criterion('design','principles of design',3,[0,3],'Explain how three principles apply to the SAME outfit sketched in (i), rather than merely naming principles. Source examples: '+design),criterion('purpose','suitable for purpose',2,[0,3],'Two points showing why that SAME outfit is suitable. Source examples: '+purpose)],'3 applied principles × 3 + 2 suitability points × 3')
 c['stem']+='\n\n'+select(part(2,'a'),'(i)','(ii)')
 missing='The original marking scheme prints the task and tariffs but supplies no model answer for this natural-fabric profile. Judge the stated criterion for ONE chosen fabric; no answer or extra partial-credit step has been invented.'
 add(2,'b',None,'3-7',15,[criterion('production','fibre production',3,[0,2],missing),criterion('properties','fibre properties',2,[0,2],missing),criterion('burning-test','identification of fibres using the burning test',1,[0,5],missing)],'Production 3 × 2 + properties 2 × 2 + burning test 5')
 pool(2,'c','i','3-8',3,1,semis(guide(17,'3 points @ 1 marks each','(ii)')))
 trends=guide(17,'3 points @ 4 marks each');add(2,'c','ii','3-8',12,[point(f'factor-{i}',v,4) for i,v in enumerate(named(trends,['Fashion trends –','Lifestyle –','Cost –']),1)],'3 required factors × 4')
 pool(3,'a','i','3-10',4,6,semis(examples(guide(18,'4 points @ 6 marks each','(ii)'))))
 pool(3,'a','ii','3-10',4,4,semis(examples(guide(18,'4 points @ 4 marks each','(iii)'))))
 initiatives=re.sub(r'\s+and$','',examples(guide(18,'2 points @ 4 marks each','3.(b)')))
 names=['Distance Learning Courses','Open University courses','BTEA','“Cost of Education Allowance”','Free fees and maintenance grants','Higher Education Access Route (HEAR)','Scholarships','Supplementary Admission Route (DARE)','Fás apprenticeships','PLC courses','Level 7 courses HETAC']
 add(3,'a','iii','3-10',10,[menu('name','Name',1,2,chosen(initiatives,names)),criterion('details','details',2,[0,4],'Two details of the SAME selected initiative. The historical 2011 names and guidance are retained as printed. Complete source guidance: '+initiatives)],'Name 2 + details 2 × 4')
 pool(3,'b','i','3-11',4,5,semis(examples(guide(18,'4 points @ 5 marks each'))))
 unemployment=re.sub(r'\s+or$','',examples(guide(19,'2 points @ 5 marks each','3.(c)'))) if s[19].count('2 points @ 5 marks each')==1 else re.sub(r'\s+or$','',examples(select(s[19].split('3.(c)',1)[0],'2 points @ 5 marks each')))
 pool(3,'b','ii','3-9',2,5,semis(unemployment))
 pool(3,'c','i','3-11',4,5,semis(examples(guide(19,'4 points @ 5 marks each','(ii)'))))
 protection=select(s[19].rsplit('(ii)',1)[1],'2 points @ 5 marks each');pool(3,'c','ii','3-9',2,5,named(examples(protection),['improved working conditions','National Minimum wage Act','Equality Act 2004','Organisation of Working Time Act 1997','Legal entitlements','Protection of Young Person']))
 assert len(cards)==19 and sum(c['totalMarks'] for c in cards)==275,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('C',cards,dict(tasks=19,marks=275,selectionDecisions='Required profiles and same-outfit sketch/description remain whole. School-uniform principles and suitability refer back to the chosen outfit. Natural-fabric source omission explicitly visible in every row. Energy-source variants keep the corresponding whole source table cells and disclose original clipped word endings; no fabricated completion. Full continued social-studies source on scheme19 included.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
