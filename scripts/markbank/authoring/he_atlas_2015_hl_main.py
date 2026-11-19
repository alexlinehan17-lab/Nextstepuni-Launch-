#!/usr/bin/env python3
"""Reviewed 2015 combined booklet: retain all twenty original Atlas identities."""
import re,fitz
from he_review_2015_hl_main import ROOT, REVIEW, documents, a_regions, body_bottom
from he_atlas_2023_hl import read, write, physical_question_count
SUBJECT='home-economics-s-and-s'
FILE='LC098ALP000EV.pdf'

def source_anchors():
 d=documents();paper,scheme=d['paper'],d['scheme'];pr=a_regions(paper,range(2,6));sr=a_regions(scheme,range(4,8));questions=[]
 def norm(region,doc):
  p=doc[region['page']-1];x0,y0,x1,y1=region['rect'];return [round(x0/p.rect.width,6),round(y0/p.rect.height,6),round(x1/p.rect.width,6),round(y1/p.rect.height,6)]
 for n in range(1,13):
  p,s=pr[n],sr[n];r=norm(p,paper);questions.append(dict(n=str(n),label=f'Section A · Q{n}',printOrder=n,pP=p['page'],pY=[r[1],r[3]],endP=p['page'],endY=r[3],region=[dict(p=s['page'],r=norm(s,scheme))],conf=1.0,mode='crop'))
 def heads(doc,pages):
  out={}
  for page in pages:
   for w in doc[page-1].get_text('words'):
    if re.fullmatch(r'[1-5]\.?',w[4]) and 40<w[0]<80:out[int(w[4].rstrip('.'))]=(page,w[1]-3)
  assert sorted(out)==[1,2,3,4,5];return out
 ph,sh=heads(paper,range(6,9)),heads(scheme,range(8,16))
 for n in range(1,6):
  page,top=ph[n];p=paper[page-1];paper_bottom=ph[n+1][1] if n<5 and ph[n+1][0]==page else body_bottom(p)
  start,upper=sh[n];end=sh[n+1][0] if n<5 else 15;regions=[]
  for sn in range(start,end+1):
   s=scheme[sn-1];st=upper if sn==start else 20;bottom=sh[n+1][1] if n<5 and sn==end else body_bottom(s)
   if bottom>st and s.get_text(clip=fitz.Rect(0,st,s.rect.width,bottom)).strip():regions.append(dict(p=sn,r=[0,round(st/s.rect.height,6),1,round(bottom/s.rect.height,6)]))
  questions.append(dict(n=str(n+12),label=f'Section B · Q{n}',printOrder=n+12,pP=page,pY=[round(top/p.rect.height,6),round(paper_bottom/p.rect.height,6)],endP=page,endY=round(paper_bottom/p.rect.height,6),region=regions,conf=1.0,mode='crop'))
 for n,pages in [(1,range(16,19)),(2,range(19,21)),(3,range(21,24))]:
  page=n+8;p=paper[page-1];regions=[dict(p=sn,r=[0,round(20/scheme[sn-1].rect.height,6),1,round(body_bottom(scheme[sn-1])/scheme[sn-1].rect.height,6)]) for sn in pages]
  questions.append(dict(n=str(n+17),label=f'Section C · Q{n}',printOrder=n+17,pP=page,pY=[round(20/p.rect.height,6),round(body_bottom(p)/p.rect.height,6)],endP=page,endY=round(body_bottom(p)/p.rect.height,6),region=regions,conf=1.0,mode='crop'))
 return questions

def apply():
 anchors=source_anchors();old=read(f'scripts/paper-trail/answers/2015/{FILE}.json');assert [q['n'] for q in old['q']]==[q['n'] for q in anchors]
 sidecar=dict(v=1,paperFileid=FILE,schemeFileid='LC098ALP000EV.pdf',component='',band=[1,38],copyright='© State Examinations Commission',q=anchors)
 for folder in ['scripts/paper-trail/answers','public/paper-answers']:write(f'{folder}/2015/{FILE}.json',sidecar)
 write(f'public/paper-anchors/2015/{FILE}.json',dict(v=1,paperOnly=1,paperFileid=FILE,schemeFileid='',component='000',band=[1,1],copyright=sidecar['copyright'],q=[{**{k:v for k,v in q.items() if k not in ('region','mode','conf')},'region':[dict(p=1)],'mode':'pagejump','conf':0.5} for q in anchors]))
 crosswalk=read(f'data/examTopics/{SUBJECT}-curriculum-crosswalk.json');node_topics={}
 for topic,nodes in crosswalk.items():
  if '-higher-' in topic:
   for node in nodes:node_topics.setdefault(node,[]).append(topic)
 canonical={q['n']:set() for q in anchors};mappings=[]
 for chunk in re.split(r'^\s*\.\.\.base,',(ROOT/'components/MarkBank/cards/home-economics/higher.ts').read_text(),flags=re.M)[1:]:
  cid=re.search(r'\bid: "([^"]+)"',chunk).group(1)
  if not cid.startswith('he-2015-hl-'):continue
  ref=re.search(r'questionRef: "([^"]+)"',chunk).group(1);m=re.search(r'Section ([ABC]) (?:E\d )?Q(\d+)',ref);assert m,(cid,ref)
  section,number=m.groups();n=str(int(number)+{'A':0,'B':12,'C':17}[section]);node=re.search(r'topicId: "([^"]+)"',chunk).group(1);assert node in node_topics
  canonical[n].add(node);mappings.append(dict(id=cid,fileid=FILE,n=n,topicId=node,atlasTopicIds=node_topics[node]))
 assert len(mappings)==48 and all(canonical.values())
 topics={n:{t for node in nodes for t in node_topics[node]} for n,nodes in canonical.items()}
 local_path=f'data/examTopics/{SUBJECT}-local-crosswalk.json';local=read(local_path)
 for a in local['associations']:
  if a['level']!='higher' or not a['heading'].startswith('2015 '):continue
  m=re.search(r'Section ([ABC]) - Question (\d+)',a['heading']);assert m,a['heading'];section,number=m.groups();n=str(int(number)+{'A':0,'B':12,'C':17}[section]);assert n in topics
  a['targets']=[t for t in a.get('targets',[]) if t['lang']!='ev']+[dict(level='higher',lang='ev',year=2015,paperKey='single',fileid=FILE,n=n,label=f'Section {section} · Q{number}')];a['resolution']='matched';a.pop('reason',None);topics[n].add(a['topicId'])
 tags_path=f'scripts/paper-trail/topic-tags/tags/{SUBJECT}.json';tags=read(tags_path);tag=next((p for p in tags if p['year']==2015 and p['fileid']==FILE),None)
 if tag is None:tag=dict(subjectId=SUBJECT,level='higher',lang='ev',year=2015,fileid=FILE,paperKey='single');tags.append(tag)
 tag['q']=[]
 for n,nodes in canonical.items():
  ordered=sorted(nodes);q=dict(n=n,primary=ordered[0])
  if len(ordered)>1:q['secondary']=ordered[1]
  tag['q'].append(q)
 write(tags_path,tags,indent=1)
 runtime_path=f'data/examTopics/{SUBJECT}-question-runtime.json';runtime=read(runtime_path);runtime['questionMappings']=[r for r in runtime['questionMappings'] if r[:5]!=['h','e',2015,'single',FILE]]
 runtime['questionMappings'] += [['h','e',2015,'single',FILE,n,sorted(runtime['topicIds'].index(t) for t in ts)] for n,ts in topics.items()];write(runtime_path,runtime)
 matched=[a for a in local['associations'] if a['resolution']=='matched'];blocked=[a for a in local['associations'] if a['resolution']=='source-blocked'];local['summary'].update(exactRuntimeQuestionMappings=len(runtime['questionMappings']),localAnswerAnchoredPhysicalCards=physical_question_count(),matchedAssociations=len(matched),sourceBlockedAssociations=len(blocked),matchedLocalCardLinks=sum(len(a['targets']) for a in matched),sourceBlockedByReason={r:sum(a['reason']==r for a in blocked) for r in sorted({a['reason'] for a in blocked})})
 local['reviewedEnglish2015Higher']=dict(paperFileid=FILE,physicalQuestions=20,review=REVIEW,policy='Original identities1–20 retained: A1–12, B13–17, C18–20. Original English paper/scheme boundaries visually reviewed; separate coursework excluded from written-answer crops. Irish editions untouched.',markBankMappings=mappings);write(local_path,local)
 print('2015 Higher: all20 original Atlas identities preserved; all48 tasks mapped to canonical topics.')

if __name__=='__main__':apply()
