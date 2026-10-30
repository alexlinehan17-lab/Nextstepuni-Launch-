"""Publish visually reviewed whole-question anchors for an exact Maths booklet.

Uses the same hashed source files and inspected plan as reviewed_presentation.
The rich map is hosted with the app as well as kept in the source sidecar store;
build-index.py reproduces answers:1 from that store's existing Maths QA profile.
"""
import hashlib
import importlib
import json
import sys
from pathlib import Path

import fitz

sys.path.insert(0, 'scripts/markbank/mathematics')
from sources import source_path

BASE = Path(__file__).resolve().parent


def publish(name):
    paper = importlib.import_module(name).p
    plan = json.loads((BASE / (name.removeprefix('review_').replace('_', '-') + '-presentation.json')).read_text())
    assert plan.get('inspectedAt') and plan.get('atlasInspectionNote'), 'Atlas boundaries need a visual review'
    assert set(plan['atlasQuestions']) == set(paper.printed_marks), 'Missing whole-question anchors'
    docs = {}
    for kind, fid in [('question', paper.paper_file), ('solution', paper.scheme_file)]:
        path = source_path(paper.year, fid, 'paper' if kind == 'question' else 'scheme', paper.sitting)
        assert hashlib.sha256(path.read_bytes()).hexdigest() == plan[kind+'Sha256'], 'Source changed'
        docs[kind] = fitz.open(path)

    def regions(kind, span):
        first, top, last, bottom = span
        doc = docs[kind]
        assert 1 <= first <= last <= len(doc)
        out = []
        for page in range(first, last+1):
            height = doc[page-1].rect.height
            y0, y1 = (top/height if page == first else 0), (bottom/height if page == last else 1)
            assert 0 <= y0 < y1 <= 1
            out.append({'p':page,'r':[0,round(y0,6),1,round(y1,6)]})
        return out

    qs = []
    for n, bounds in plan['atlasQuestions'].items():
        question, solution = regions('question',bounds['paper']), regions('solution',bounds['scheme'])
        qs.append(dict(n=n,label=f'Q{n}',pP=question[0]['p'],pY=[question[0]['r'][1],1],
                       endP=question[-1]['p'],endY=question[-1]['r'][3],
                       paperRegion=question,region=solution,mode='crop',conf=1.0))
    result = dict(v=1,paperFileid=paper.paper_file,schemeFileid=paper.scheme_file,
                  component=paper.paper_key[1:]+'00',band=[min(q['region'][0]['p'] for q in qs),max(q['region'][-1]['p'] for q in qs)+1],
                  copyright='© State Examinations Commission',q=qs)
    override = f'mathematics|{paper.year}|{paper.paper_file}'
    assert repr(override) in Path('components/PaperTrail/vaultResolve.ts').read_text(), 'Register the reviewed hosted map before exposing Atlas questions'
    content = json.dumps(result,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n'
    for root in ['scripts/paper-trail/answers','public/paper-answers']:
        path=Path(root)/str(paper.year)/(paper.paper_file+'.json')
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(content)
    index=Path('paperTrailData.ts')
    lines=index.read_text().splitlines(keepends=True)
    found=0
    for i,line in enumerate(lines):
        if f'"year": {paper.year}' not in line or f'"{paper.paper_file}"' not in line:
            continue
        entry=json.loads(line.strip().rstrip(','))
        for item in entry['papers']:
            if item['doc']['f'] == paper.paper_file:
                assert item['scheme']['f'] == paper.scheme_file
                assert (item.get('sitting') or entry.get('sitting','main')) == paper.sitting
                item['answers']=1
                found+=1
        lines[i]='    '+json.dumps(entry,ensure_ascii=False)+',\n'
    assert found == 1, 'No unique indexed booklet'
    index.write_text(''.join(lines))
    print(f'Published {len(qs)} verified Atlas question/answer maps for {override}')


if __name__=='__main__': publish(sys.argv[1])
