# Build the Mark Bank audit report (HTML -> PDF). Run from the scratchpad.
import json, glob, os, re, html, sys
from PIL import Image

OUT = 'report'; IMG = OUT + '/img'
os.makedirs(IMG, exist_ok=True)
stats = json.load(open('stats.json')); feat = json.load(open('featured.json'))
tcount = json.load(open('textcounts.json')); pscale = json.load(open('phonescale.json'))
reviews = {json.load(open(f))['subject']: json.load(open(f)) for f in glob.glob('reviews/*.json')}
mans = {s: {c['n']: c for c in json.load(open(f'review/{s}/manifest.json'))['cards']} for s in reviews}
E = lambda t: html.escape(str(t or ''))

BIG = [s for s in reviews if len(mans[s]) >= 12]
SMALL = [s for s in reviews if s not in BIG]
T = lambda s: stats[s]['title']

def section_of(s):
    r = reviews[s]; sc = r['scores']
    diff = sum(1 for c in r['cards'] if c.get('other_questions_shown') == 'different-question')
    pc = (stats[s].get('pdfcheck') or {}).get('pct') or 0
    share = stats[s]['pctAttachedPage']
    if r['verdict'] == 'needs-work': return 2
    if (sc.get('attachments') or 5) <= 2: return 2
    if diff >= 3: return 2
    if pc >= 20 and share >= 30: return 2
    return 1

SEC = {s: section_of(s) for s in reviews}

# ---------------------------------------------------------------- images
def save_jpg(im, name, q=62):
    p = f'{IMG}/{name}.jpg'
    im.convert('RGB').save(p, 'JPEG', quality=q, optimize=True)
    return 'img/' + name + '.jpg'

def src_img(s, n, view, state):
    """view m|d, state q|a -> PIL image or None (true-to-screen capture, else the audit capture)."""
    p = f'feat/{s}__{n}__{view}_{state}.png'
    if os.path.exists(p): return Image.open(p)
    cid = mans[s][n]['id']; p = f'shots/all/{cid}__{view}_{state}.png'
    return Image.open(p) if os.path.exists(p) else None

def phone_cols(s, n, state='a', maxcols=3, colh=1560, w=500):
    im = src_img(s, n, 'm', state)
    if im is None: return [], 0
    k = w / im.width; im = im.resize((w, round(im.height * k)))
    ch = round(colh * w / 780) if im.width else colh
    ch = 1000
    out = []; total = -(-im.height // ch)
    for i in range(min(total, maxcols)):
        out.append(save_jpg(im.crop((0, i * ch, w, min(im.height, (i + 1) * ch))), f'{s}-{n}-m{state}{i}'))
    return out, total

def phone_first(s, n, w=500):
    im = src_img(s, n, 'm', 'q')
    if im is None: return None
    k = w / im.width; im = im.resize((w, round(im.height * k)))
    return save_jpg(im.crop((0, 0, w, min(im.height, round(844 * w / 390)))), f'{s}-{n}-mfirst')

def desktop(s, n, state='a', maxh=1150, w=1100):
    im = src_img(s, n, 'd', state)
    if im is None: return None, False
    k = w / im.width; im = im.resize((w, round(im.height * k)))
    cut = im.height > maxh
    return save_jpg(im.crop((0, 0, w, min(im.height, maxh))), f'{s}-{n}-d{state}'), cut

def attached(s, n):
    p = f'review/{s}/{n:02d}_attached_page.png'
    if not os.path.exists(p): return None
    im = Image.open(p); w, h = im.size
    # trim the dark backdrop around the reader
    im = im.crop((0, int(h * 0.19), w, int(h * 0.81))) if h >= 1400 else im
    im = im.resize((900, round(im.height * 900 / im.width)))
    return save_jpg(im, f'{s}-{n}-att')

def cardlabel(s, n):
    c = mans[s][n]
    return f"{E(c['questionRef'])} · {c['totalMarks']} marks · topic: {E(c['topic'])}"

# ---------------------------------------------------------------- pieces
def chips(s):
    st = stats[s]; r = reviews[s]; sc = r['scores']
    lv = '/'.join(l[0].upper() + 'L' for l in st['levels'])
    bits = [f"{st['cards']:,} cards", lv, f"{st['years'][0]}–{st['years'][1]}"]
    return ' · '.join(bits)

def scorebar(s):
    sc = reviews[s]['scores']; out = []
    for k, lab in (('question', 'Question'), ('attachments', 'Attachments'), ('scheme', 'Scheme'), ('phone', 'Phone'), ('desktop', 'Desktop')):
        v = sc.get(k)
        cls = 'na' if v is None else ('g' if v >= 4 else 'a' if v == 3 else 'r')
        out.append(f'<span class="sc {cls}"><b>{lab}</b> {"–" if v is None else str(v) + "/5"}</span>')
    return '<div class="scores">' + ''.join(out) + '</div>'

def numbers(s):
    st = stats[s]; tc = tcount[s]['counts']; out = []
    if st['pctAttachedPage']:
        crop = 'cropped to the question' if st['pctAttachedCropped'] >= 80 else 'whole printed pages, not cropped'
        out.append(f"{st['pctAttachedPage']}% of cards attach exam pages ({crop})")
    pc = st.get('pdfcheck')
    if pc and pc['cardsChecked'] and pc['pct'] and s not in LANGS and st['pctAttachedPage'] >= 10 and s != 'history':
        out.append(f"checked against {pc['cardsChecked']} real paper pages: a different question is printed on the page for {pc['pct']:.0f}%")
    if st['pctQuestionImage'] >= 15: out.append(f"{st['pctQuestionImage']}% of questions are shown as a picture of the paper")
    if tc.get('a_slash_list', 0) >= 20: out.append(f"{tc['a_slash_list']:,} cards have slash-joined answer lists")
    if tc.get('a_pipe_table', 0) >= 20: out.append(f"{tc['a_pipe_table']:,} schemes hold a table flattened into one line")
    if tc.get('q_over_900_chars', 0) >= 40: out.append(f"{tc['q_over_900_chars']:,} questions run past 900 characters of text")
    ps = pscale.get(s, {})
    if ps.get('phoneLenMax', 0) >= 4200: out.append(f"longest sampled card is about {ps['phoneLenMax'] / 844:.0f} phone screens")
    return ('<p class="nums">' + ' · '.join(out) + '.</p>') if out else ''

LANGS = {'irish', 'french', 'german', 'spanish', 'italian', 'japanese', 'russian', 'polish', 'portuguese'} | set()

DROP_SENT = re.compile(r'blank (band|gap)|empty band|large gap|white space|empty space (before|above|between)|opened as a blank|could not be (loaded|played)|dead (video|player)|did not load on card 7|Loading the step', re.I)
SCRUB = [(r' is the (strongest|cleanest|tidiest) of (these four|this group|the four subjects|the four)( on desktop| on the scheme side)?', r' is one of the cleaner subjects\3'),
         (r'one of the better-looking of this group', 'one of the better-looking subjects'), (r'among the cleaner subjects here', 'among the cleaner subjects'),
         (r'is the best layout in this batch', 'is one of the best layouts seen'), (r'is the cleanest scheme layout of the four subjects', 'is a very clean scheme layout')]
def clean(t, sentences=False):
    t = re.sub(r'\s+', ' ', str(t or '')).strip()
    if sentences:
        t = ' '.join(x for x in re.split(r'(?<=[.!?])\s+', t) if not DROP_SENT.search(x))
        for a, b in SCRUB: t = re.sub(a, b, t)
    return t

def example_block(s, g, compact=False):
    n = g['card']; h = [f'<div class="ex"><div class="keep"><p class="cap"><b>{cardlabel(s, n)}</b><br>{E(clean(g.get("why")))}</p>']
    cols, total = phone_cols(s, n, 'a', maxcols=3)
    row = []
    for i, c in enumerate(cols):
        row.append(f'<figure class="ph"><img src="{c}"><figcaption>Phone · {"the question, then the scheme after the reveal" if i == 0 else "continued"}</figcaption></figure>')
    h.append('<div class="phrow">' + ''.join(row) + '</div></div>')
    if not compact:
        d, cut = desktop(s, n, 'a', maxh=900)
        if d: h.append(f'<figure class="dk"><img src="{d}"><figcaption>Desktop · after reveal{" (top of the card)" if cut else ""}</figcaption></figure>')
    h.append('</div>')
    return ''.join(h)

def issue_block(s, i, idx, pictures=True):
    sev = i.get('severity', 'medium'); n = i.get('card')
    h = [f'<div class="issue"><h4><span class="sev {sev}">{sev}</span> {idx}. {E(clean(i["title"]))}</h4>']
    h.append(f'<p><b>What is wrong.</b> {E(clean(i["detail"], True))}</p>')
    h.append(f'<p class="fix"><b>How to fix it.</b> {E(clean(i["suggested_fix"]))}</p>')
    if n and pictures:
        kind = i.get('evidence_kind')
        if kind == 'attached':
            a = attached(s, n)
            if a: h.append(f'<figure class="dk att"><img src="{a}"><figcaption>What opens from the card for {cardlabel(s, n)}</figcaption></figure>')
        elif kind == 'desktop':
            d, cut = desktop(s, n, 'a', maxh=1000)
            if d: h.append(f'<figure class="dk"><img src="{d}"><figcaption>Desktop · {cardlabel(s, n)}</figcaption></figure>')
        else:
            cols, total = phone_cols(s, n, 'a', maxcols=3)
            if cols:
                h.append('<div class="phrow">' + ''.join(f'<figure class="ph"><img src="{c}"><figcaption>Phone · screen {k + 1} of {total}</figcaption></figure>' for k, c in enumerate(cols)) + f'</div><p class="capline">{cardlabel(s, n)}</p>')
    h.append('</div>')
    return ''.join(h)

EXTRA = json.load(open('extra_notes.json')) if os.path.exists('extra_notes.json') else {}
OVR = json.load(open('overrides.json')) if os.path.exists('overrides.json') else {}
for _s,_o in OVR.items():
    feat[_s]['issues']=[i for i in feat[_s]['issues'] if not any(d.lower() in i['title'].lower() for d in _o.get('drop',[]))]
    if _o.get('summary'): reviews[_s]['summary']=_o['summary']
    for k,v in (_o.get('scores') or {}).items(): reviews[_s]['scores'][k]=v

def subject_block(s):
    r = reviews[s]; f = feat[s]; sec = SEC[s]
    h = [f'<section class="subj {"big" if s in BIG else "sm"}"><h3>{E(T(s))}</h3><p class="meta">{chips(s)}</p>{scorebar(s)}']
    h.append(f'<p class="sum">{E(clean(r["summary"], True))}</p>{numbers(s)}')
    for note in EXTRA.get(s, []): h.append(f'<p class="verified"><b>Checked directly.</b> {note}</p>')
    big = s in BIG
    if sec == 1:
        h.append('<h5>How it looks</h5>')
        for k, g in enumerate(f['good'][: 2 if big else 1]): h.append(example_block(s, g, compact=(not big) or k == 1))
        iss = [i for i in f['issues']]
        if iss:
            h.append('<h5>Small fixes still worth making</h5><ul class="small">')
            for i in iss[:5]: h.append(f'<li><b>{E(clean(i["title"]))}.</b> {E(clean(i["suggested_fix"]))}</li>')
            h.append('</ul>')
    else:
        h.append('<h5>The issues, with evidence</h5>')
        for k, i in enumerate(f['issues'][: 4 if big else 2]): h.append(issue_block(s, i, k + 1, pictures=(k < 2 if big else k < 1)))
        more = [i for i in f['issues'][4 if big else 2:]]
        titles = [t for t in [clean(i['title']) for i in more] + f.get('more_issues', []) if not DROP_SENT.search(t) and not re.search(r'audio|video|recording', t, re.I)]
        if titles:
            h.append('<p class="also"><b>Also found:</b> ' + E('; '.join(titles)) + '.</p>')
        if f['good']:
            h.append('<h5>What already works here (the pattern to copy)</h5>')
            h.append(example_block(s, f['good'][0], compact=True))
    h.append('</section>')
    return ''.join(h)

# ---------------------------------------------------------------- order
ORDER1_BIG = [s for s in ['physics', 'biology', 'technology', 'engineering', 'computer-science', 'religious-education', 'spanish', 'polish', 'portuguese'] if SEC.get(s) == 1]
ORDER2_BIG = ['maths', 'applied-maths', 'construction-studies', 'dcg', 'chemistry', 'agricultural-science', 'economics', 'business', 'accounting', 'home-economics', 'lcvp', 'geography', 'history', 'politics-and-society', 'english', 'irish', 'french', 'german', 'italian', 'japanese', 'russian', 'art', 'music', 'physical-education', 'classical-studies']
big1 = ORDER1_BIG + sorted(s for s in BIG if SEC[s] == 1 and s not in ORDER1_BIG)
big2 = [s for s in ORDER2_BIG if SEC.get(s) == 2] + sorted(s for s in BIG if SEC[s] == 2 and s not in ORDER2_BIG)
small1 = sorted(s for s in SMALL if SEC[s] == 1); small2 = sorted(s for s in SMALL if SEC[s] == 2)

def table():
    rows = []
    for sec, group in ((1, big1 + small1), (2, big2 + small2)):
        for s in group:
            sc = reviews[s]['scores']
            def cell(k):
                v = sc.get(k); cls = 'na' if v is None else ('g' if v >= 4 else 'a' if v == 3 else 'r')
                return f'<td class="{cls}">{"–" if v is None else v}</td>'
            top = feat[s]['issues'][0]['title'] if feat[s]['issues'] else ''
            rows.append(f'<tr><td>{E(T(s))}</td><td>{stats[s]["cards"]:,}</td><td class="s{sec}">{"Works" if sec == 1 else "Needs work"}</td>{cell("question")}{cell("attachments")}{cell("scheme")}{cell("phone")}{cell("desktop")}<td class="top">{E(clean(top))}</td></tr>')
    return '<table class="board"><thead><tr><th>Subject</th><th>Cards</th><th>Verdict</th><th>Question</th><th>Attach.</th><th>Scheme</th><th>Phone</th><th>Desktop</th><th>Biggest thing to fix</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table>'

FRONT = open('front.html').read() if os.path.exists('front.html') else ''
PHONE = open('phone.html').read() if os.path.exists('phone.html') else ''
PLAN = open('plan.html').read() if os.path.exists('plan.html') else ''
CSS = open('report.css').read()

doc = ['<!doctype html><html><head><meta charset="utf-8"><title>Mark Bank audit</title><style>', CSS, '</style></head><body>']
doc.append(FRONT.replace('{{TABLE}}', table()).replace('{{N1}}', str(len(big1) + len(small1))).replace('{{N2}}', str(len(big2) + len(small2))))
doc.append(f'<h1 class="part" id="s1"><span>Section 1</span>Subjects that work</h1><p class="lead">These {len(big1) + len(small1)} subjects ask a clear question, show the right marking scheme for it, and attach nothing from another topic in the cards sampled. None is perfect: each has a short list of small fixes, set out under its examples. Scores are out of 5 from a card-by-card look at the sampled cards.</p>')
for s in big1: doc.append(subject_block(s))
if small1:
    doc.append('<h2 class="grp">Smaller language subjects that work</h2><p class="lead">These share one layout: a reading text attached as its own pages, a short question, and the scheme\'s answer points to tick. The attached pages held the right text and no other question in every card sampled.</p>')
    for s in small1: doc.append(subject_block(s))
doc.append(f'<h1 class="part" id="s2"><span>Section 2</span>Subjects that need work</h1><p class="lead">These {len(big2) + len(small2)} subjects have at least one problem a student would notice: another question shown beside the one asked, a question that cannot be read or answered from the card, or a marking scheme that is hard to follow or says nothing. Each issue has what is wrong, how to fix it, and a screenshot from the app.</p>')
for s in big2: doc.append(subject_block(s))
if small2:
    doc.append('<h2 class="grp">Smaller language subjects that need work</h2>')
    for s in small2: doc.append(subject_block(s))
doc.append(PHONE); doc.append(PLAN)
doc.append('</body></html>')
open(OUT + '/report.html', 'w').write('\n'.join(doc))
print('section1', len(big1), len(small1), 'section2', len(big2), len(small2))
print('big1', big1); print('big2', big2); print('small1', small1); print('small2', small2)
print('images', len(os.listdir(IMG)), 'MB', round(sum(os.path.getsize(f'{IMG}/{f}') for f in os.listdir(IMG)) / 1e6, 1))
