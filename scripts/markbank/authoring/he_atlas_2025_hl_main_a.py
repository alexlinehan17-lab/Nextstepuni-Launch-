#!/usr/bin/env python3
"""Reviewed 2025 Higher main paper/scheme anchors and canonical card mappings."""
import json
import re
from he_review_2025_hl_main import ROOT, REVIEW, documents
from he_review_2023_hl_deferred import a_regions
from he_atlas_2022_deferred import b_heads
from he_atlas_2023_hl import read, write, physical_question_count
SUBJECT='home-economics-s-and-s'
A='LC098ALP014EV.pdf';BC='LC098ALP039EV.pdf'


def source_anchors():
 d=documents();pr=a_regions(d['a'],range(3,8),740);sr=a_regions(d['scheme'],range(6,11),780)
 def norm(region,doc):
  p=doc[region['page']-1];x0,y0,x1,y1=region['rect'];return [round(x0/p.rect.width,6),round(y0/p.rect.height,6),round(x1/p.rect.width,6),round(y1/p.rect.height,6)]
 qa=[]
 for n in range(1,15):
  p,s=pr[n],sr[n];r=norm(p,d['a']);qa.append(dict(n=str(n),label=f'Section A · Q{n}',printOrder=n,pP=p['page'],pY=[r[1],r[3]],endP=p['page'],endY=r[3],region=[dict(p=s['page'],r=norm(s,d['scheme']))],conf=1.0,mode='crop'))
 return {A:qa}


def apply():
 anchors=source_anchors()
 for file,questions in anchors.items():
  sidecar=dict(v=1,paperFileid=file,schemeFileid='LC098ALP000EV.pdf',component='014' if file==A else '039',band=[1,44],copyright='© State Examinations Commission',q=questions)
  for folder in ['scripts/paper-trail/answers','public/paper-answers']:write(f'{folder}/2025/{file}.json',sidecar)
  write(f'public/paper-anchors/2025/{file}.json',dict(v=1,paperOnly=1,paperFileid=file,schemeFileid='',component=sidecar['component'],band=[1,1],copyright=sidecar['copyright'],q=[{**{k:v for k,v in q.items() if k not in ('region','mode','conf')},'region':[dict(p=1)],'mode':'pagejump','conf':0.5} for q in questions]))
 crosswalk=read(f'data/examTopics/{SUBJECT}-curriculum-crosswalk.json');node_topics={}
 for topic,nodes in crosswalk.items():
  if '-higher-' in topic:
   for node in nodes:node_topics.setdefault(node,[]).append(topic)
 canonical={f:{q['n']:set() for q in qs} for f,qs in anchors.items()};mappings=[]
 deck=(ROOT/'components/MarkBank/cards/home-economics/higher.ts').read_text()
 for chunk in re.split(r'^\s*\.\.\.base,',deck,flags=re.M)[1:]:
  cid=re.search(r'\bid: "([^"]+)"',chunk).group(1)
  if not cid.startswith('he-2025-hl-sa-') or 'deferred' in cid:continue
  ref=re.search(r'questionRef: "([^"]+)"',chunk).group(1);match=re.search(r'Section ([ABC]) (?:E\d )?Q(\d+)',ref);assert match,(cid,ref)
  section,number=match.groups();file=A if section=='A' else BC;n=str(int(number)+(5 if section=='C' else 0));node=re.search(r'topicId: "([^"]+)"',chunk).group(1);assert node in node_topics
  canonical[file][n].add(node);mappings.append(dict(id=cid,fileid=file,n=n,topicId=node,atlasTopicIds=node_topics[node]))
 assert len(mappings) == 15 and all(nodes for groups in canonical.values() for nodes in groups.values()),len(mappings)
 topics={f:{n:{t for node in nodes for t in node_topics[node]} for n,nodes in groups.items()} for f,groups in canonical.items()}
 local_path=f'data/examTopics/{SUBJECT}-local-crosswalk.json';local=read(local_path)
 for association in local['associations']:
  if association['level']!='higher' or not association['heading'].startswith('2025 - Section A ') or 'Deferred' in association['heading']:continue
  match=re.search(r'Section ([ABC]) - Question (\d+)',association['heading']);assert match,association['heading'];section,number=match.groups();file=A if section=='A' else BC;n=str(int(number)+(5 if section=='C' else 0));assert n in topics[file]
  targets=[t for t in association.get('targets',[]) if t['lang']!='ev'];targets.append(dict(level='higher',lang='ev',year=2025,paperKey='single',fileid=file,n=n,label=f'Section {section} · Q{number}'));association['targets']=targets;association['resolution']='matched';association.pop('reason',None);topics[file][n].add(association['topicId'])
 tags_path=f'scripts/paper-trail/topic-tags/tags/{SUBJECT}.json';tags=read(tags_path)
 for file,groups in canonical.items():
  previous=next(p for p in tags if p['year']==2025 and p['fileid']==file);previous['q']=[]
  for n,nodes in groups.items():
   ordered=sorted(nodes);tag=dict(n=n,primary=ordered[0])
   if len(ordered)>1:tag['secondary']=ordered[1]
   previous['q'].append(tag)
 write(tags_path,tags,indent=1)
 runtime_path=f'data/examTopics/{SUBJECT}-question-runtime.json';runtime=read(runtime_path);runtime['questionMappings']=[r for r in runtime['questionMappings'] if not (r[:4]==['h','e',2025,'single'] and r[4] in anchors)]
 runtime['questionMappings'] += [['h','e',2025,'single',file,n,sorted(runtime['topicIds'].index(t) for t in ts)] for file,groups in topics.items() for n,ts in groups.items()];write(runtime_path,runtime)
 local['summary']['exactRuntimeQuestionMappings']=len(runtime['questionMappings']);local['summary']['localAnswerAnchoredPhysicalCards']=physical_question_count()
 matched=[a for a in local['associations'] if a['resolution']=='matched'];blocked=[a for a in local['associations'] if a['resolution']=='source-blocked'];local['summary'].update(matchedAssociations=len(matched),sourceBlockedAssociations=len(blocked),matchedLocalCardLinks=sum(len(a['targets']) for a in matched),sourceBlockedByReason={r:sum(a['reason']==r for a in blocked) for r in sorted({a['reason'] for a in blocked})})
 local['reviewedEnglish2025HigherA']=dict(paperFileids=[A,BC],physicalQuestions=14,review=REVIEW,policy='All 14 English Section A paper/scheme anchors reviewed; all 15 reviewed tasks mapped to canonical topics. B/C source authoring remains pending; Irish editions untouched.',markBankMappings=mappings);write(local_path,local);print(f'2025 Higher: 14 source anchors; {len(mappings)} Mark Bank tasks mapped to canonical Atlas topics.')

if __name__=='__main__':apply()
