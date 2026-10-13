"""Reviewer's tools for the Biology paper-by-paper review (bio_review.py).

None of these write to the bank; they are how a reviewer reads the PDFs and
checks a ledger before `bio_review.py <year> <level> --write`.

  python3 bio_tools.py dump PDF FIRST-LAST          printed lines, page by page (the lifter's own text)
  python3 bio_tools.py lines PDF PAGE Y0 Y1         line boxes in PDF points, for crop rectangles
  python3 bio_tools.py images PDF PAGE [PAGE ...]   image blocks and drawing extents per page
  python3 bio_tools.py sheet PDF NAME FIRST-LAST COLS ZOOM   contact sheet of rendered pages
  python3 bio_tools.py scan YEAR LEVEL              selection directives, in SELECTION_SCAN order
  python3 bio_tools.py existing YEAR LEVEL          the sitting's authored cards before review
  python3 bio_tools.py cards YEAR LEVEL             the cards a ledger builds (check only)
  python3 bio_tools.py pointers YEAR LEVEL          cards whose text points at a printed figure but carry none
  python3 bio_tools.py crops YEAR LEVEL [KEY ...]   render the ledger's crops
  python3 bio_tools.py montage [KEY ...]            four crops to a sheet, for viewing
  python3 bio_tools.py topics YEAR LEVEL [ADDS] [--replace]
                                                    write a sitting's Topic Atlas entries: the reference
                                                    topics per question plus ADDS ("5:24-immunity;8:...",
                                                    "-topic" drops a wrong reference topic); refuses to
                                                    change a level already mapped unless --replace
  python3 bio_tools.py identity [YEAR-LEVEL ...]    re-run --write for every reviewed sitting (except those
                                                    named) and report whether the bank comes back byte-identical

Output (sheets, crops, montages) goes to $BIO_REVIEW_OUT, default
<tmpdir>/bio-review. Run from anywhere; paths resolve from this file.
"""
import importlib
import json
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
OUT = os.environ.get('BIO_REVIEW_OUT', os.path.join(tempfile.gettempdir(), 'bio-review'))


def _pdf(path):
    return path if os.path.isabs(path) else os.path.join(ROOT, path)


def _pages(spec):
    a, _, b = spec.partition('-')
    return range(int(a), int(b or a) + 1)


def _ledger(year, level):
    return importlib.import_module(f'bio_review_{year}_{level}')


def cmd_dump(path, pages):
    import bio_review_lib as B
    src = B.Src(_pdf(path), 'x')
    for p in _pages(pages):
        if p not in src.lines:
            break
        print(f'===== p{p}')
        for i, line in enumerate(src.lines[p]):
            print(f'{i:3d}| {line}')


def cmd_lines(path, page, y0, y1):
    import fitz
    pg = fitz.open(_pdf(path))[int(page) - 1]
    for b in pg.get_text('dict')['blocks']:
        for ln in b.get('lines', []):
            x0, ly0, x1, ly1 = ln['bbox']
            if ly1 >= float(y0) and ly0 <= float(y1):
                text = ''.join(s['text'] for s in ln['spans']).strip()
                if text:
                    print(f'{x0:5.0f}{ly0:5.0f}{x1:5.0f}{ly1:5.0f}  {text[:80]}')


def cmd_images(path, *pages):
    import fitz
    doc = fitz.open(_pdf(path))
    for p in pages:
        pg = doc[int(p) - 1]
        ims = [[round(v) for v in b['bbox']] for b in pg.get_text('dict')['blocks'] if b['type'] == 1]
        big = [d['rect'] for d in pg.get_drawings() if d['rect'].width > 3 and d['rect'].height > 3]
        print(f'p{p} images {ims}')
        if big:
            u = fitz.Rect(big[0])
            for r in big:
                u |= r
            print(f'    drawings {len(big)} union {[round(v) for v in u]}')


def cmd_sheet(path, name, pages, cols, zoom):
    import fitz
    doc = fitz.open(_pdf(path))
    ps = list(_pages(pages))
    pix = [doc[p - 1].get_pixmap(matrix=fitz.Matrix(float(zoom), float(zoom))) for p in ps]
    w0, h0 = pix[0].width, pix[0].height
    cols = int(cols)
    rows = (len(pix) + cols - 1) // cols
    canvas = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, cols * (w0 + 6), rows * (h0 + 6)), False)
    canvas.clear_with(200)
    for i, p in enumerate(pix):
        p2 = fitz.Pixmap(fitz.csRGB, p) if p.alpha or p.colorspace.n != 3 else p
        p2.set_origin((i % cols) * (w0 + 6), (i // cols) * (h0 + 6))
        canvas.copy(p2, p2.irect)
    os.makedirs(OUT, exist_ok=True)
    out = os.path.join(OUT, f'{name}.png')
    canvas.save(out)
    print(out)


def cmd_scan(year, level):
    import bio_review as R
    import bio_review_lib as B
    L = _ledger(int(year), level)
    n = 0
    for doc, ps in L.SCAN_PAGES.items():
        src = B.Src(os.path.join(ROOT, L.SOURCES[doc]['path']), doc)
        for p in ps:
            t = src.page_text(p)
            for m in R.SCAN.finditer(t):
                print(f"{n:3d} {doc} p{p} {m.group(0).lower()!r:24} ...{t[max(0, m.start() - 55):m.end() + 45]}...")
                n += 1


def cmd_existing(year, level):
    tag = f'bio-{year}-{level}'
    authored = json.load(open(os.path.join(ROOT, 'scripts/markbank/authored/biology.json')))
    cards = authored['cards'] if isinstance(authored, dict) else authored
    deck = open(os.path.join(ROOT, 'components/MarkBank/cards/biology',
                             ('higher' if level == 'hl' else 'ordinary') + '.ts')).read()
    shipped = set(re.findall(rf'^\s*id: "({tag}[^"]*)"', deck, re.M))
    bind = json.load(open(os.path.join(ROOT, 'scripts/markbank/card-source-bindings.json'))).get('biology', {})
    corr = json.load(open(os.path.join(ROOT, 'scripts/markbank/card-corrections.json'))).get('biology', {})
    n = 0
    for c in cards:
        if not c['id'].startswith(tag + '-'):
            continue
        n += 1
        flags = ['SHIP' if c['id'] in shipped else 'NOSHIP'] + (['BIND'] if c['id'] in bind else []) \
            + (['CORR'] if c['id'] in corr else [])
        rows = ' || '.join(f"{r.get('kind')}:{r.get('marks')}:{str(r.get('verbatim', ''))[:50]}" for r in c['rows'])
        print(f"{c['id']} [{' '.join(flags)}] {c['questionRef']} | {c['totalMarks']} | "
              f"{json.dumps(c.get('tariffModel'))} | {c['topicId']} | sec {c.get('section')} | "
              f"fig={c.get('figureKey')} | {c['questionText'][:90]!r}\n     {rows[:300]}")
    print(f'{n} authored, {len(shipped)} shipped')
    for k, v in bind.items():
        if k.startswith(tag + '-'):
            print('BIND', k, v)
    for k, v in corr.items():
        if k.startswith(tag + '-'):
            print('CORR', k, json.dumps(v)[:200])


def _build(year, level):
    import bio_review as R
    L = _ledger(int(year), level)
    return L, R.build(L, int(year), level)


def cmd_cards(year, level):
    _, (_, cards, _, checks) = _build(year, level)
    for c in cards:
        print('=' * 100)
        print(c['id'], '|', c['questionRef'], '|', c['topicId'], c['conceptId'], '|', c['totalMarks'], '|',
              c.get('figureKey'), '|', c.get('questionFigureKey'))
        if c.get('stem'):
            print('STEM:', c['stem'])
        print('Q:', c['questionText'])
        for r in c['rows']:
            extra = ''
            if r.get('group'):
                extra = f" claim={r['group']['claimMax']} per={r['group']['perOption']} opts={r['group']['options']}"
            print(f"  [{r['kind']}:{r['marks']}] {r['verbatim']}{extra}"
                  + (f"  NOTE: {r['contextNote']}" if r.get('contextNote') else '')
                  + (' OPEN' if r.get('openList') else ''))
        if c.get('labelKey'):
            print('  LABELS:', c['labelKey'])
        print('  NOTES:', c['notes'])
    for h in checks.get('excluded', []):
        print('HELD', h)


POINTS_AT_PRINT = re.compile(r'\b(the|this) (diagram|image|photograph|graph|table|food web|picture)s?\b'
                             r'|\bdata table\b|\bword equation\b|\bpedigree chart\b|\bthe one shown\b', re.I)


def cmd_pointers(year, level):
    _, (_, cards, _, _) = _build(year, level)
    for c in cards:
        text = f"{c.get('stem') or ''} {c['questionText']}"
        m = POINTS_AT_PRINT.search(text)
        if m and not (c.get('figureKey') or c.get('questionFigureKey') or c.get('sourceMaterial')):
            print('NEEDS FIG', c['id'], m.group(0))


def cmd_crops(year, level, *only):
    import bio_review as R
    L = _ledger(int(year), level)
    _, recs = R.figures(L, R.Lifter(L), int(year), level, False)
    d = os.path.join(OUT, 'crops')
    os.makedirs(d, exist_ok=True)
    for k, png in recs:
        if only and not any(o in k for o in only):
            continue
        open(os.path.join(d, f'{k}.png'), 'wb').write(png)
        print(k, len(png))


def cmd_montage(*names):
    import glob
    import fitz
    d = os.path.join(OUT, 'crops')
    files = sorted(glob.glob(os.path.join(d, '*.png')))
    if names:
        files = [f for f in files if any(n in f for n in names)]
    for gi in range(0, len(files), 4):
        grp = files[gi:gi + 4]
        pix = [fitz.Pixmap(f) for f in grp]
        scaled = [(p, min(1.0, 680 / p.width, 600 / p.height)) for p in pix]
        rows = [scaled[0:2], scaled[2:4]]
        height = sum(max((int(p.height * s) for p, s in r), default=0) + 30 for r in rows)
        doc = fitz.open()
        page = doc.new_page(width=1400, height=height)
        y = 0
        for r in rows:
            x = rh = 0
            for p, s in r:
                w, h = int(p.width * s), int(p.height * s)
                page.draw_rect(fitz.Rect(x, y + 20, x + w, y + 20 + h), color=(0.6, 0.6, 0.6), width=0.5)
                page.insert_image(fitz.Rect(x, y + 20, x + w, y + 20 + h), pixmap=p)
                page.insert_text((x + 2, y + 14), os.path.basename(grp[pix.index(p)]), fontsize=11)
                x += 700
                rh = max(rh, h)
            y += rh + 30
        out = os.path.join(OUT, f'montage-{gi // 4}.png')
        page.get_pixmap().save(out)
        print(out)


def cmd_topics(year, level, adds='', *flags):
    """data/examTopics/biology-<year>-exam-topic-map.json: each question of the
    sitting keeps every topic the reference snapshot (data/examTopics/biology.json
    headings) gives it and gains ADDS, written "q:topic,topic;q:topic" with
    topics named without their "biology-<level>-new-course-" prefix; "-topic"
    drops a reference topic the reviewed tasks show is wrong. A level already in
    the file is left alone unless the result matches it or --replace is given,
    so a reviewed map is never silently rebuilt."""
    from collections import defaultdict
    if adds == '--replace':
        adds, flags = '', ('--replace',) + flags
    year = int(year)
    word = {'hl': 'higher', 'ol': 'ordinary'}.get(level, level)
    full = lambda t: t if t.startswith('biology-') else f'biology-{word}-new-course-{t}'
    extra, drop = {}, {}
    for part in filter(None, adds.split(';')):
        q, ts = part.split(':')
        ts = ts.split(',')
        extra[int(q)] = [full(t) for t in ts if not t.startswith('-')]
        drop[int(q)] = {full(t[1:]) for t in ts if t.startswith('-')}
    ref_doc = json.load(open(os.path.join(ROOT, 'data/examTopics/biology.json')))
    cw = json.load(open(os.path.join(ROOT, 'data/examTopics/biology-curriculum-crosswalk.json')))
    ref = defaultdict(list)
    for var in (f'{word}-new-course', f'{word}-old-course'):
        for t in ref_doc['variants'][var]['topics']:
            for h in t.get('officialQuestionHeadings', []):
                m = re.search(r'Question\s+(\d+)', h) if h.startswith(f'{year} ') else None
                if m and t['id'] not in ref[int(m.group(1))]:
                    ref[int(m.group(1))].append(t['id'])
    path = os.path.join(ROOT, f'data/examTopics/biology-{year}-exam-topic-map.json')
    doc = json.load(open(path)) if os.path.exists(path) else {
        'schemaVersion': 1, 'subjectId': 'biology', 'year': year, 'authority': 'State Examinations Commission',
        'scope': 'Top-level question-to-reference-topic mapping reviewed directly from the official English paper '
                 'booklets and marking schemes, task by task (scripts/markbank/authoring/bio_review_'
                 f'{year}_<level>.py). Each question keeps every topic the factual reference snapshot already gave '
                 'it and gains the topics its reviewed tasks need.', 'questions': {}}
    before = {k: v for k, v in doc['questions'].items() if k.startswith(f'{word}|')}
    for q in range(1, 18):
        for t in extra.get(q, []):
            if t not in cw:
                raise SystemExit(f'{t} is not in the curriculum crosswalk')
        for t in drop.get(q, set()) - set(ref[q]):
            raise SystemExit(f'Q{q}: {t} is not a reference topic, so there is nothing to drop')
        kept = [t for t in ref[q] if t not in drop.get(q, set())]
        doc['questions'][f'{word}|{q}'] = kept + [t for t in extra.get(q, []) if t not in kept]
        print(q, sorted({n for t in doc['questions'][f'{word}|{q}'] for n in cw.get(t, []) if n.startswith('bio-')}))
    after = {k: v for k, v in doc['questions'].items() if k.startswith(f'{word}|')}
    if before and before != after and '--replace' not in flags:
        for k in sorted(set(before) | set(after), key=lambda k: int(k.split('|')[1])):
            if before.get(k) != after.get(k):
                print(f'  {k}: mapped {before.get(k)} -> would be {after.get(k)}')
        raise SystemExit(f'{year} {word} is already mapped and this would change it; pass --replace to rewrite it')
    head = {k: v for k, v in doc.items() if k != 'questions'}
    lines = ['{'] + [f'  {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)},' for k, v in head.items()]
    lines.append('  "questions": {')
    qs = list(doc['questions'].items())
    for i, (k, v) in enumerate(qs):
        lines.append(f'    {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}' + (',' if i < len(qs) - 1 else ''))
    lines += ['  }', '}']
    open(path, 'w').write('\n'.join(lines) + '\n')


def cmd_identity(*skip):
    """A reader or runner change must not move a reviewed sitting it was not
    made for: re-write every reviewed sitting and compare the bank's files."""
    import glob
    import hashlib
    import subprocess
    watched = ['scripts/markbank/authored/biology.json', 'scripts/markbank/authored/biology-review-audit.json',
               'components/MarkBank/figures-biology.json', 'scripts/markbank/card-corrections.json']

    def snapshot():
        files = watched + sorted(os.path.relpath(f, ROOT) for f in glob.glob(
            os.path.join(ROOT, 'public/exam-figures/biology/markbank/biology-20*.png')))
        return {f: hashlib.sha256(open(os.path.join(ROOT, f), 'rb').read()).hexdigest() for f in files}
    before = snapshot()
    sittings = sorted({re.match(r'bio_review_(\d{4})_(hl|ol)\.py', os.path.basename(f)).groups()
                       for f in glob.glob(os.path.join(HERE, 'bio_review_20??_??.py'))}, reverse=True)
    for year, level in sittings:
        if f'{year}-{level}' in skip:
            continue
        out = subprocess.run([sys.executable, os.path.join(HERE, 'bio_review.py'), year, level, '--write'],
                             capture_output=True, text=True)
        lines = out.stdout.strip().splitlines() or [out.stderr.strip()]
        print(f'{year} {level}:', ([l for l in lines if 'reviewed tasks' in l] or lines)[-1][:110])
    after = snapshot()
    moved = sorted(f for f in set(before) | set(after) if before.get(f) != after.get(f))
    print('byte-identical' if not moved else 'CHANGED: ' + ', '.join(moved))


COMMANDS = {k[4:]: v for k, v in globals().items() if k.startswith('cmd_')}

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(2)
    COMMANDS[sys.argv[1]](*sys.argv[2:])
    sys.stdout.flush()
    # PyMuPDF can crash in its exit-time cleanup after heavy page reads.
    os._exit(0)
