#!/usr/bin/env python3
"""Publish reviewed deferred Physics question/answer anchors and topic tags.

Only sittings with a completed Mark Bank source review can enter the Atlas.
Raw SEC archive basenames stay distinct from virtual indexed deferred IDs.
The page ranges below were checked against every source page, independently
of the Mark Bank task ledger. Never infer them from card counts.
"""
from pathlib import Path
import hashlib
import json
import sys
import fitz
import physics

ROOT = Path(__file__).resolve().parents[2]
REVIEWED = {
    '2022-hl-deferred': {
        'paperPages': [2, 2, 3, 3, 4, 5, 6, 7, 8, 8, 9, 10, 12, 13],
        'schemePages': [(4,4),(5,5),(6,6),(7,7),(8,8),(9,10),(11,11),
                        (12,12),(13,13),(14,14),(15,15),(16,17),(18,18),(19,22)],
        'tags': [('physics-0-3',),('physics-2-2',),('physics-5-1',),
                 ('physics-5-10',),('physics-6-11',),('physics-0-8','physics-7-9'),
                 ('physics-0-0','physics-0-2'),('physics-3-2','physics-0-11'),
                 ('physics-6-16','physics-6-17'),('physics-7-0','physics-7-2'),
                 ('physics-6-11',),('physics-7-9','physics-6-15'),
                 ('physics-6-9','physics-6-13'),('physics-0-12','physics-7-5')],
    },
}


def generate():
    audit = json.loads((ROOT/'scripts/markbank/authored/physics-review-audit.json').read_text())
    tags_path = ROOT/'scripts/paper-trail/topic-tags/tags/physics.json'
    old_tags = json.loads(tags_path.read_text())
    papers = [p for p in old_tags if not p['fileid'].endswith('-deferred.pdf')]
    wanted = [str(n) for n in range(1,15)]
    for key, geometry in REVIEWED.items():
        review = audit['sittings'].get(key)
        if review is None: continue
        assert review['status']=='reviewed' and review['sitting']=='deferred', key
        year, level, _ = key.split('-')
        year = int(year)
        raw_fileid = f"LC021{'A' if level=='hl' else 'G'}LP000EV.pdf"
        fileid = raw_fileid.replace('.pdf','-deferred.pdf')
        for kind,folder in [('paper','deferredexams'),('scheme','deferredmarkingschemes')]:
            source=review['sources'][kind]
            path=ROOT/f'paper-trail-corpus/{folder}/{year}/{raw_fileid}'
            assert source['fileid']==raw_fileid and source['path']==str(path.relative_to(ROOT)), key
            assert hashlib.sha256(path.read_bytes()).hexdigest()==source['sha256'], key
            with fitz.open(path) as doc: assert len(doc)==source['pages']
        path=ROOT/review['sources']['paper']['path']
        with fitz.open(path) as doc:
            anchors,tail=physics.paper_anchors(doc,path,wanted,physics.load_anchor_mapper())
        assert [a['page'] for a in anchors]==geometry['paperPages'], key
        assert tail==(14,1.0), (key,tail)
        anchor_map,_=physics.hosted_map(fileid,year,anchors,tail)
        answers={'v':1,'paperFileid':fileid,'schemeFileid':fileid,'component':'000',
                 'band':[1,review['sources']['scheme']['pages']+1],
                 'copyright':physics.COPYRIGHT,'q':[]}
        for anchor,(first,last) in zip(anchor_map['q'],geometry['schemePages']):
            answers['q'].append({
                'n':anchor['n'],'pP':anchor['pP'],'pY':anchor['pY'],
                'endP':anchor['endP'],'endY':anchor['endY'],
                'region':[{'p':p,'r':[0,0.06,1,0.93]} for p in range(first,last+1)],
                'mode':'crop','conf':1.0,
            })
        for folder,data in [('public/paper-anchors',anchor_map),
                            ('scripts/paper-trail/answers',answers),
                            ('public/paper-answers',answers)]:
            target=ROOT/f'{folder}/{year}/{fileid}.json'
            target.parent.mkdir(parents=True,exist_ok=True)
            if target.exists(): assert json.loads(target.read_text())==data, target
            target.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
        papers.append({'subjectId':'physics','level':'higher' if level=='hl' else 'ordinary',
                       'lang':'ev','year':year,'fileid':fileid,'paperKey':'single',
                       'q':[{'n':str(i+1),'primary':nodes[0],
                             **({'secondary':nodes[1]} if len(nodes)>1 else {})}
                            for i,nodes in enumerate(geometry['tags'])]})
    # An unrecognised existing deferred sitting must never disappear on rerun.
    live={(p['year'],p['level'],p['fileid']) for p in papers}
    assert all((p['year'],p['level'],p['fileid']) in live for p in old_tags)
    tags_path.write_text(json.dumps(papers,ensure_ascii=False,indent=1)+'\n')
    print(f'Physics Atlas: {len(papers)} paper variants; reviewed deferred sources retained separately.')

if __name__=='__main__': generate()
