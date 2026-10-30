"""Render exact, reviewed question/solution rectangles, then publish inspected crops.

Usage: python3 .../reviewed_presentation.py review_2025_ol_p1_deferred [--publish]
The source hashes and every rectangle live beside the paper declaration.
Preview is read-only; publication requires a recorded visual inspection.
"""
import hashlib, importlib, json, shutil, sys
from pathlib import Path
import fitz
from PIL import Image, ImageDraw
from legacy_presentation_figures import render
sys.path.insert(0, 'scripts/markbank/mathematics')
from sources import source_path

BASE = Path(__file__).resolve().parent


def main(name, publish=False):
    paper = importlib.import_module(name).p
    plan = json.loads((BASE / (name.removeprefix('review_').replace('_', '-') + '-presentation.json')).read_text())
    cards = {c['id']: c for c in paper.cards}
    assert set(cards) == set(plan['tasks']), 'presentation does not cover the reviewed task list'
    docs = {}
    for kind, fileid in [('question', paper.paper_file), ('solution', paper.scheme_file)]:
        path = source_path(paper.year, fileid, 'paper' if kind == 'question' else 'scheme', paper.sitting)
        assert hashlib.sha256(path.read_bytes()).hexdigest() == plan[kind + 'Sha256'], 'source changed'
        docs[kind] = fitz.open(path)
    out = Path('tmp/pdfs') / (name + '-crops')
    out.mkdir(parents=True, exist_ok=True)
    records = {}
    for kind in docs:
        sheets, columns = [], [[], []]
        heights = [0, 0]
        for cid, c in cards.items():
            regions = plan['tasks'][cid][kind]
            rects = [dict(page=p, x0=x0, top=y0, x1=x1, bottom=y1) for p,x0,y0,x1,y1 in regions]
            im = render(docs[kind], rects, 200)
            key = c['questionFigureKey' if kind == 'question' else 'figureKey']
            path = out / f'{key}.png'
            im.save(path)
            records[key] = dict(src=f'/exam-figures/maths/markbank/{key}.png',
                md5=hashlib.md5(path.read_bytes()).hexdigest(),
                alt=('The question as printed on the paper — ' + ' '.join(filter(None, [c.get('stem'), c['questionText']])))
                    if kind == 'question' else f"Original SEC worked solution and complete marking guidance for {paper.ref} {', '.join(c['printedParts'])}.",
                year=paper.year, level=paper.level,
                attribution=f'SEC Leaving Certificate Mathematics {paper.year} {paper.level.title()} Level, deferred examination — © State Examinations Commission')
            if kind == 'solution': records[key]['solution'] = True
            w=760; h=round(im.height*w/im.width)
            col=0 if heights[0]<=heights[1] else 1
            if heights[col]+h+35>2300 and any(columns):
                sheets.append(columns);columns=[[],[]];heights=[0,0];col=0
            columns[col].append((cid,im.resize((w,h))));heights[col]+=h+35
        if any(columns): sheets.append(columns)
        for n,cols in enumerate(sheets,1):
            sheet=Image.new('RGB',(1580,max(sum(im.height+35 for _,im in col) for col in cols)+20),'#eee')
            draw=ImageDraw.Draw(sheet)
            for x,col in enumerate(cols):
                y=10
                for cid,im in col:
                    draw.text((x*790+10,y),cid,fill='black');sheet.paste(im,(x*790+10,y+25));y+=im.height+35
            sheet.save(out/f'{kind}-qa-{n:02}.jpg',quality=92)
        print(kind,len(cards),'crops',len(sheets),'inspection sheets')
    if publish:
        assert plan.get('inspectedAt') and plan.get('inspectionNote'), 'inspect every crop before publication'
        manifest=Path('components/MarkBank/figures.json');data=json.loads(manifest.read_text())
        for key,record in records.items():
            destination=Path('public') / record['src'].lstrip('/')
            destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(out/f'{key}.png',destination)
            data[key]=record
        manifest.write_text(json.dumps(data,ensure_ascii=False,indent=1)+'\n')
        print('Published',len(records),'inspected source crops')


if __name__=='__main__': main(sys.argv[1], '--publish' in sys.argv)
