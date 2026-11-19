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
 d=documents();heads=b_heads(d['bc'],range(2,5));page,top=heads[2];p=d['bc'][page-1];end=heads[3][1];bottom=max(w[3] for w in p.get_text('words') if top<=w[1] and w[3]<end)+8;s=d['scheme'][13];sb=max(w[3] for w in s.get_text('words') if w[3]<760)+8
 return {BC:[dict(n='2',label='Section B · Q2',printOrder=2,pP=page,pY=[round(top/p.rect.height,6),round(bottom/p.rect.height,6)],endP=page,endY=round(bottom/p.rect.height,6),region=[dict(p=14,r=[0,round(35/s.rect.height,6),1,round(sb/s.rect.height,6)])],conf=1.0,mode='crop')]}


def apply():
 anchors=source_anchors()
 for file,questions in anchors.items():
  previous=read(f'scripts/paper-trail/answers/2025/{file}.json');merged=[q for q in previous['q'] if q['n']!='2']+questions;merged.sort(key=lambda q:int(q['n']));sidecar={**previous,'band':[1,44],'q':merged}
  for folder in ['scripts/paper-trail/answers','public/paper-answers']:write(f'{folder}/2025/{file}.json',sidecar)
  write(f'public/paper-anchors/2025/{file}.json',dict(v=1,paperOnly=1,paperFileid=file,schemeFileid='',component=sidecar['component'],band=[1,1],copyright=sidecar['copyright'],q=[{**{k:v for k,v in q.items() if k not in ('region','mode','conf')},'region':[dict(p=1)],'mode':'pagejump','conf':0.5} for q in merged]))
 crosswalk=read(f'data/examTopics/{SUBJECT}-curriculum-crosswalk.json');node_topics={}
 for topic,nodes in crosswalk.items():
  if '-higher-' in topic:
   for node in nodes:node_topics.setdefault(node,[]).append(topic)
 canonical={f:{q['n']:set() for q in qs} for f,qs in anchors.items()};mappings=[]
 deck=(ROOT/'components/MarkBank/cards/home-economics/higher.ts').read_text()
 for chunk in re.split(r'^\s*\.\.\.base,',deck,flags=re.M)[1:]:
  cid=re.search(r'\bid: "([^"]+)"',chunk).group(1)
  if not cid.startswith('he-2025-hl-sb-q2') or 'deferred' in cid:continue
  ref=re.search(r'questionRef: "([^"]+)"',chunk).group(1);match=re.search(r'Section ([ABC]) (?:E\d )?Q(\d+)',ref);assert match,(cid,ref)
  section,number=match.groups();file=A if section=='A' else BC;n=str(int(number)+(5 if section=='C' else 0));node=re.search(r'topicId: "([^"]+)"',chunk).group(1);assert node in node_topics
  canonical[file][n].add(node);mappings.append(dict(id=cid,fileid=file,n=n,topicId=node,atlasTopicIds=node_topics[node]))
 assert len(mappings) == 4 and all(nodes for groups in canonical.values() for nodes in groups.values()),len(mappings)
 topics={f:{n:{t for node in nodes for t in node_topics[node]} for n,nodes in groups.items()} for f,groups in canonical.items()}
 local_path=f'data/examTopics/{SUBJECT}-local-crosswalk.json';local=read(local_path)
 for association in local['associations']:
  if association['level']!='higher' or not association['heading'].startswith('2025 - Section B - Question 2') or 'Deferred' in association['heading']:continue
  match=re.search(r'Section ([ABC]) - Question (\d+)',association['heading']);assert match,association['heading'];section,number=match.groups();file=A if section=='A' else BC;n=str(int(number)+(5 if section=='C' else 0));assert n in topics[file]
  targets=[t for t in association.get('targets',[]) if t['lang']!='ev'];targets.append(dict(level='higher',lang='ev',year=2025,paperKey='single',fileid=file,n=n,label=f'Section {section} · Q{number}'));association['targets']=targets;association['resolution']='matched';association.pop('reason',None);topics[file][n].add(association['topicId'])
 tags_path=f'scripts/paper-trail/topic-tags/tags/{SUBJECT}.json';tags=read(tags_path)
 for file,groups in canonical.items():
  previous=next(p for p in tags if p['year']==2025 and p['fileid']==file);previous['q']=[q for q in previous['q'] if q['n']!='2']
  for n,nodes in groups.items():
   ordered=sorted(nodes);tag=dict(n=n,primary=ordered[0])
   if len(ordered)>1:tag['secondary']=ordered[1]
   previous['q'].append(tag)
 write(tags_path,tags,indent=1)
 runtime_path=f'data/examTopics/{SUBJECT}-question-runtime.json';runtime=read(runtime_path);runtime['questionMappings']=[r for r in runtime['questionMappings'] if not (r[:4]==['h','e',2025,'single'] and r[4] in anchors and r[5]=='2')]
 runtime['questionMappings'] += [['h','e',2025,'single',file,n,sorted(runtime['topicIds'].index(t) for t in ts)] for file,groups in topics.items() for n,ts in groups.items()];write(runtime_path,runtime)
 local['summary']['exactRuntimeQuestionMappings']=len(runtime['questionMappings']);local['summary']['localAnswerAnchoredPhysicalCards']=physical_question_count()
 matched=[a for a in local['associations'] if a['resolution']=='matched'];blocked=[a for a in local['associations'] if a['resolution']=='source-blocked'];local['summary'].update(matchedAssociations=len(matched),sourceBlockedAssociations=len(blocked),matchedLocalCardLinks=sum(len(a['targets']) for a in matched),sourceBlockedByReason={r:sum(a['reason']==r for a in blocked) for r in sorted({a['reason'] for a in blocked})})
 local['reviewedEnglish2025HigherB2']=dict(paperFileids=[A,BC],physicalQuestions=1,review=REVIEW,policy='Question B2 paper/scheme anchor reviewed; all four tasks mapped to canonical topics. Original paper lettering overrides scheme typo: cheese is (c), calcium is (b). All other question anchors preserved. B1/B3–B5/C task authoring remains pending; Irish editions untouched.',markBankMappings=mappings);write(local_path,local);print(f'2025 Higher: one source anchor; {len(mappings)} Mark Bank tasks mapped to canonical Atlas topics.')

if __name__=='__main__':apply()
