#!/usr/bin/env python3
"""
dv_prepare.py — Diagram Vault extraction, stage 1 (prepare candidates).

For a subject, download each tagged question paper from the (world-readable) SEC
corpus on Firebase Storage, detect candidate figure regions, and crop each to a
PNG in a scratch dir, writing a candidates.json manifest. Stage 2 is an agent
that VIEWS each crop and accepts/describes/attributes it (that is the gate — this
script only proposes).

Usage:
  python3 tools/dv_prepare.py <subjectId> <cycle> [--years 2022,2023] [--out DIR]
    cycle ∈ {lc, jc, lca}
"""
import sys, os, json, urllib.parse, urllib.request

sys.path.insert(0, os.path.dirname(__file__))
from detect_exam_figures import detect  # noqa: E402
import fitz  # noqa: E402

BUCKET = 'nextstepuni-app.firebasestorage.app'
TAGS = 'scripts/paper-trail/topic-tags/tags'


def paper_url(cycle, subject, year, fileid):
    path = f'papers/{cycle}/{subject}/{year}/paper/{fileid}'
    return f'https://firebasestorage.googleapis.com/v0/b/{BUCKET}/o/{urllib.parse.quote(path, safe="")}?alt=media'


def download(url, dest):
    req = urllib.request.Request(url, headers={'User-Agent': 'dv-prepare'})
    with urllib.request.urlopen(req, timeout=60) as r:
        if r.status != 200:
            return False
        data = r.read()
    if not data[:4] == b'%PDF':
        return False
    with open(dest, 'wb') as f:
        f.write(data)
    return True


def main():
    subject, cycle = sys.argv[1], sys.argv[2]
    years = None
    out = f'/tmp/dv/{subject}'
    if '--years' in sys.argv:
        years = set(int(y) for y in sys.argv[sys.argv.index('--years') + 1].split(','))
    if '--out' in sys.argv:
        out = sys.argv[sys.argv.index('--out') + 1]
    os.makedirs(out, exist_ok=True)

    tags = json.load(open(f'{TAGS}/{subject}.json'))
    # Unique papers (dedupe by fileid+year+level; EV only — IV is the same figures).
    seen = set()
    papers = []
    for t in tags:
        if t.get('lang') == 'iv':
            continue
        if years and t['year'] not in years:
            continue
        key = (t['year'], t['level'], t['fileid'])
        if key in seen:
            continue
        seen.add(key)
        papers.append(t)

    candidates = []
    for t in papers:
        url = paper_url(cycle, subject, t['year'], t['fileid'])
        # The SEC reuses the same fileid across years — key the cached PDF by
        # year+level+fileid so different sittings never collide (the bug that
        # scrambled the first biology wave).
        pdf = f'{out}/{t["year"]}-{t["level"][:3]}-{t["fileid"]}'
        if not os.path.exists(pdf):
            try:
                if not download(url, pdf):
                    print(f'  MISS {t["year"]} {t["level"]} {t["fileid"]} (not on storage)')
                    continue
            except Exception as e:
                print(f'  ERR  {t["year"]} {t["level"]} {t["fileid"]}: {e}')
                continue
        try:
            cands = detect(pdf)
        except Exception as e:
            print(f'  ERR detect {t["fileid"]}: {e}')
            continue
        doc = fitz.open(pdf)
        for i, c in enumerate(cands):
            # cand_id carries year+level so crops from different sittings that
            # share a fileid never overwrite each other.
            cid = f'{t["year"]}-{t["level"][:3]}-{t["fileid"][:-4]}-p{c["page"]}-{i}'
            png = f'{out}/crop-{cid}.png'
            page = doc[c['page'] - 1]
            pr = page.rect
            clip = fitz.Rect(pr.x0 + c['x0'] * pr.width, pr.y0 + c['y0'] * pr.height,
                             pr.x0 + c['x1'] * pr.width, pr.y0 + c['y1'] * pr.height)
            try:
                page.get_pixmap(clip=clip, dpi=200).save(png)
            except Exception:
                continue
            candidates.append({
                'cand_id': cid, 'subjectId': subject, 'year': t['year'], 'level': t['level'],
                'fileid': t['fileid'], 'page': c['page'], 'near': c['near'],
                'w': c['w'], 'h': c['h'], 'kind': c['kind'], 'crop': png,
            })
        print(f'  OK   {t["year"]} {t["level"]} {t["fileid"]}: {len(cands)} candidates')

    with open(f'{out}/candidates.json', 'w') as f:
        json.dump(candidates, f, indent=1)
    print(f'\n{len(candidates)} candidates across {len(papers)} papers -> {out}/candidates.json')


if __name__ == '__main__':
    main()
