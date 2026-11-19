#!/usr/bin/env python3
"""2014 Higher electives: source exceptions, choices, profiles and complete continuations."""
from copy import deepcopy
from he_review_2014_hl_main import *
def build():
 d=documents();p={n:re.sub(r'(\d)\.\s+\(([abc])\)',r'\1.(\2)',text(d['paper'],n+8)) for n in [1,2,3]};s={n:text(d['scheme'],n) for n in range(19,28)};cards=[]
 def part(n,letter):
  v=select(p[n],f'{n}.({letter})',f'{n}.({chr(ord(letter)+1)})' if f'{n}.({chr(ord(letter)+1)})' in p[n] else None)
  return re.sub(r'\s+(?:and|or)\s*$','',v).strip()
 def prompt(n,letter,roman):
  v=part(n,letter)
  if roman:v=select(v,f'({roman})');v=re.split(r'\((?:i|ii|iii)\)',v,1)[0]
  return re.sub(r'\s*\(\d+\)\s*$','',v).strip().replace('\uf0b7','•')
 def add(n,letter,roman,topic,marks,rows,notation,**extra):
  v=part(n,letter);stem=v.split('(i)',1)[0].strip() if roman else ''
  c=card(f'sc-q{n}{letter}{roman or ""}','C',f'E{n} Q{n}({letter})'+(f'({roman})' if roman else ''),topic,prompt(n,letter,roman),stem,marks,rows,n+8,notation,**extra);cards.append(c);return c
 def guide(page,token,end=None,include=False):return select(s[page],token,end,include)
 def judged(n,letter,roman,topic,count,per,label,guidance,**extra):return add(n,letter,roman,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} points × {per}',**extra)
 insulation=guide(19,'Attic/roof:','(ii)');insulation='Attic/roof: '+insulation;areas=chosen(insulation,['Attic/roof','Wall insulation','Floor insulation','External insulation','Window/door insulation','Hot water cylinder/pipes']);rows=[];groups=[]
 for i in [1,2,3]:
  rows.extend([menu(f'area-{i}','Area',1,2,areas,'Choose THREE different areas in total.'),criterion(f'method-{i}','method of insulation',1,[0,2],'One method suitable for the SAME area. Full original source: '+insulation),criterion(f'principle-{i}','underlying principle',1,[0,4],'Explain the principle of the SAME method. Full original source: '+insulation)])
  groups.append(dict(sourceCardId=f'he-2014-hl-sc-q1ai-area-{i}',label=f'Area {i}',marks=8,rowIds=[f'area-{i}',f'method-{i}',f'principle-{i}']))
 add(1,'a','i','3-6',24,rows,'3 areas × (area 2 + method 2 + principle 4)',taskGroups=groups)
 energy='Source - Solar power'+guide(19,'Source - Solar power')+' '+s[20].split('(iii)',1)[0]
 allowance='The original scheme explicitly accepts NON-RENEWABLE sources too because the English and Irish versions of the paper differ. Its printed models cover five renewable sources; no non-renewable model is supplied.'
 heads=['Source - Solar power','Source - Hydropower','Source - Wind power','Source - Bio energy','Source - Geothermal'];names=['Solar power','Hydropower','Wind power','Bio energy','Geothermal'];variants=[]
 for i,(name,body) in enumerate(zip(names,named(energy,heads)),1):
  variants.append(dict(id=f'source-{i}',label=name,rows=[point('name',name,2,allowance),criterion('source','source',1,[0,3],allowance+' Use the SAME energy source. Original model: '+body),criterion('evaluation','advantages / disadvantages',2,[0,3],allowance+' Two points about the SAME source. Original model: '+body),criterion('sustainability','sustainability',1,[0,3],allowance+' One point about the SAME source. Original model: '+body)]))
 variants.append(dict(id='another-source',label='Another source, including non-renewable',rows=[criterion('name','Name',1,[0,2],allowance),criterion('source','source',1,[0,3],allowance+' Identify the source of the SAME named energy.'),criterion('evaluation','advantages / disadvantages',2,[0,3],allowance+' Two points for the SAME source.'),criterion('sustainability','sustainability',1,[0,3],allowance+' One point for the SAME source.')]))
 add(1,'a','ii','3-6',14,deepcopy(variants[0]['rows']),'Name 2 + source 3 + evaluation 2×3 + sustainability 3',answerVariants=variants,figureKey='home-economics-2014-hl-sc-q1aii-allowance')
 judged(1,'a','iii','3-6',3,4,'Building Energy Rating',re.sub(r'\s+and$','',guide(20,'3 points @ 4 marks each','1. (b')))
 judged(1,'b','i','3-4',4,4,'factors',guide(20,'4 factors @ 4 marks each','(ii)'))
 wall=guide(20,'Paint',include=True)+' '+s[21].split('1.(c)',1)[0];wall=re.sub(r'\s+or$','',wall);options=chosen(wall,['Water-based paint','Specialised paint','General purpose wall paper','Washable wall paper','Embossed Wall paper','Wood chip','wood panelling','ceramic tiles']);rows=[];groups=[]
 for i in [1,2]:
  rows.extend([menu(f'name-{i}','Name',1,1,options,'Choose TWO DIFFERENT wall finishes in total.'),criterion(f'description-{i}','Description',1,[0,2],'Describe the SAME finish. Complete original source: '+wall),criterion(f'properties-{i}','Properties',2,[0,2],'Two properties of the SAME finish. The source names wood panelling/ceramic tiles without separate models; no missing details have been invented. Original source: '+wall)])
  groups.append(dict(sourceCardId=f'he-2014-hl-sc-q1bii-finish-{i}',label=f'Finish {i}',marks=7,rowIds=[f'name-{i}',f'description-{i}',f'properties-{i}']))
 add(1,'b','ii','3-4',14,rows,'2 finishes × (name 1 + description 2 + properties 2×2)',taskGroups=groups)
 judged(1,'c','i','3-3',3,5,'comparative costs',select(select(s[21],'1.(c)','(ii)'),'3 points @ 5 marks each'))
 judged(1,'c','ii','3-3',3,5,'private rented accommodation',select(select(s[21],'(ii)'),'3 points @ 5 marks each'))
 heads=['Comfort','Aesthetic appeal','Current fashion trends'];add(2,'a','i','3-8',15,[criterion(f'heading-{i}',head,1,[0,5],body) for i,(head,body) in enumerate(zip(heads,named(guide(22,'3 points @ 5 marks each','(ii)'),heads)),1)],'3 required headings × 5',questionFigureKey='home-economics-2014-hl-sc-q2-dress',questionFigureIncludesPrompt=False)
 design=guide(22,'2 elements @ 5 marks each')+' '+s[23].split('2.(b)',1)[0];design=re.sub(r'\s+and$','',design)
 judged(2,'a','ii','3-8',2,5,'elements',design)
 construction=guide(23,'Name = 3marks, 2 points @ 3 marks each','(ii)');variants=[]
 for i,(name,body) in enumerate(zip(['Weaving','Knitting'],named(construction,['Weaving-','Knitting -'])),1):variants.append(dict(id=f'technique-{i}',label=name,rows=[point('name',name,3),criterion('description','description',2,[0,3],'Two description points for the SAME fabric construction technique. Original model: '+body)]))
 variants.append(dict(id='another-technique',label='Another suitable construction technique',rows=[criterion('name','Name',1,[0,3],'One technique suitable for cotton fabric.'),criterion('description','description',2,[0,3],'Two matching description points. The scheme models weaving and knitting only; no further model is supplied.')]))
 add(2,'b','i','3-7',9,deepcopy(variants[0]['rows']),'Name 3 + description 2×3',answerVariants=variants)
 finish=re.sub(r'\s+or$','',select(select(s[23],'(ii)'),'2 points @ 3 marks each'))
 c=judged(2,'b','ii','3-7',2,3,'functional fabric finish',finish);c['rows'][0]['contextNote']='Choose ONE finish and give TWO details about that SAME finish; no name mark is printed. Some source examples have fewer than two developed details; no missing details have been invented. '+c['rows'][0]['contextNote']
 judged(2,'c','i','3-8',3,3,'challenges',guide(24,'3 points @ 3 marks each','(ii)'))
 designer=guide(24,'Name = 2 marks, 1 point @ 4 marks');names=chosen(designer,['John Rocha','Philip Treacy','Lainey Keogh','Paul Costelloe','Louise Kennedy','Sybill Connolly']);note='The source lists these names and generic work examples, without a full model for each designer. Apply the work point to the SAME chosen designer; no name/work pairing has been invented. '
 add(2,'c','ii','3-8',6,[menu('name','Name',1,2,names,note),criterion('work','promoting Irish fashion',1,[0,4],note+'Original source: '+designer)],'Name 2 + work 4')
 judged(3,'a','i','3-10',4,5,'adult and second chance education',select(select(s[25],'(i)','(ii)'),'4 points @ 5 marks each'))
 judged(3,'a','ii','3-10',4,5,'considerations',select(select(s[25],'(ii)','(iii)'),'4 points @ 5 marks each'))
 initiative=guide(25,'Name: 4 marks, 2 points @ 3 marks each')+' '+s[26].split('3.(b)',1)[0];initiative=re.sub(r'\s+and$','',initiative);names=chosen(initiative,['The National Adult Learning Council (NALC)','Aontas','VTOS','Bluebrick','Springboard','Youthreach','Solas','PLC courses','BTEA','Community Education Schemes','HEAR','DARE'])
 add(3,'a','iii','3-10',10,[menu('name','Name',1,4,names,'Choose ONE contemporary initiative in this historical 2014 exam.'),criterion('details','details',2,[0,3],'Two points about the SAME chosen initiative. Complete original 2014 source: '+initiative)],'Name 4 + details 2×3')
 change=select(s[26],'3.(b)');heads=['Changing attitudes to marriage –','Traditional roles within the family –','Impact of modern communications technology –'];rows=[]
 for i,(head,body) in enumerate(zip(heads,named(change,heads)),1):
  body=re.split(r'•|\(10\)|2 points @ 5 marks each',body,1)[0];body=re.sub(r'\s+or$','',body);rows.append(criterion(f'heading-{i}',head.rstrip(' –'),2,[0,5],body))
 add(3,'b',None,'3-11',30,rows,'3 required headings × 2 points × 5')
 judged(3,'c','i','3-11',3,6,'voluntary work',guide(27,'3 points @ 6 marks each','(ii)'))
 judged(3,'c','ii','3-11',3,4,'benefits',guide(27,'3 benefits @ 4 marks each'))
 assert len(cards)==19 and sum(c['totalMarks'] for c in cards)==275,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('C',cards,dict(tasks=19,marks=275,selectionDecisions='Three linked insulation profiles, explicit non-renewable allowance and full renewable variants. Two wall finishes retain name1/description2/properties4. Original dress, all design elements, construction variants, one-finish quota and visible incomplete model guidance. Complete educational initiative continuation and coherent three-heading family change account.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
