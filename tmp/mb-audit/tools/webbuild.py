# Turn report/report.html into a commentable web page: web/index.html + web/img/*
import re, os, shutil, json
from bs4 import BeautifulSoup

src = open('report/report.html', encoding='utf-8').read()
soup = BeautifulSoup(src, 'html.parser')
body = soup.body
slug = lambda t: re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')[:60]

def mark(el, cid, label):
    el['data-cid'] = cid; el['data-label'] = label

mark_count = 0
# front-matter findings
for i, f in enumerate(body.select('div.find')):
    t = f.h4.get_text(' ', strip=True); t = re.sub(r'^\d+\s*', '', t)
    mark(f, f'summary-finding-{i + 1}', f'Summary, finding {i + 1}: {t}')
# subjects, their issues and examples
for sec in body.select('section.subj'):
    name = sec.h3.get_text(strip=True); s = slug(name)
    sec['id'] = 'sub-' + s
    head = soup.new_tag('div'); head['class'] = 'subhead'
    sec.h3.wrap(head)
    mark(head, s, f'{name} (whole subject)')
    for k, iss in enumerate(sec.select('div.issue')):
        t = iss.h4.get_text(' ', strip=True); t = re.sub(r'^(high|medium|low)\s*', '', t, flags=re.I)
        mark(iss, f'{s}-issue-{k + 1}', f'{name}, issue {t}')
    for k, ex in enumerate(sec.select('div.ex')):
        b = ex.find('b'); t = b.get_text(' ', strip=True) if b else ''
        mark(ex, f'{s}-example-{k + 1}', f'{name}, example card {t}')
    for k, ul in enumerate(sec.select('ul.small')):
        mark(ul, f'{s}-small-fixes', f'{name}, small fixes list')
# section 3 and 4
part = None
for el in list(body.children):
    if getattr(el, 'name', None) == 'h1' and 'part' in (el.get('class') or []):
        part = el.get('id')
    if part == 's3' and getattr(el, 'name', None) == 'h2':
        t = el.get_text(' ', strip=True); n = re.match(r'(\d+)', t)
        mark(el, f'phone-{n.group(1) if n else slug(t)}', f'Desktop versus phone, {t}')
for tr in body.select('table.plain tr'):
    n = tr.find('td', class_='n')
    if n and tr.find_parent('section') is None and tr.find('b'):
        mark(tr, f'plan-fix-{n.get_text(strip=True)}', f'Fix plan, step {n.get_text(strip=True)}: {tr.find("b").get_text(strip=True)}')
for h in body.select('h1.part'):
    mark(h, 'section-' + h.get('id', slug(h.get_text())), 'Section: ' + h.get_text(' ', strip=True))
board = body.select_one('table.board')
if board:
    wrap = soup.new_tag('div'); wrap['class'] = 'scroll'; board.wrap(wrap)
for t in body.select('table.plain'):
    if 'scroll' not in (t.parent.get('class') or []):
        w = soup.new_tag('div'); w['class'] = 'scroll'; t.wrap(w)
# link board rows to subjects
ids = {sec.h3.get_text(strip=True): sec['id'] for sec in body.select('section.subj')}
for tr in body.select('table.board tbody tr'):
    td = tr.find('td'); name = td.get_text(strip=True)
    if name in ids:
        a = soup.new_tag('a', href='#' + ids[name]); a.string = name; td.clear(); td.append(a)
for img in body.find_all('img'): img['loading'] = 'lazy'

inner = body.decode_contents()
n_marks = len(re.findall(r'data-cid=', inner))

CSS = open('web.css').read(); JS = open('web.js').read()
doc = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mark Bank audit</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&family=Source+Serif+4:wght@600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>
<header class="bar"><div class="bar-in"><strong>Mark Bank audit</strong><nav><a href="#s1">Works</a><a href="#s2">Needs work</a><a href="#s3">Phone</a><a href="#s4">Fix plan</a></nav>
<span class="grow"></span><span id="count" class="count">0 comments</span><button type="button" id="copyAll" class="btn primary">Copy all comments</button></div></header>
<main>
<div class="howto" data-cid="general" data-label="General comment on the whole report"><b>How to comment.</b> Tap <span class="pill">Comment</span> beside any subject, issue, example or fix. Your comments are saved as you go. When you are done, tap <b>Copy all comments</b> at the top and paste the result into the Claude Code session, or just tell Claude to read your comments.</div>
{inner}
</main>
<div id="sheet" class="sheet" hidden><div class="sheet-in"><h4>All comments</h4><p class="note" id="sheetMsg"></p><textarea id="sheetText" readonly rows="14"></textarea><div class="row"><button type="button" class="btn" id="sheetClose">Close</button><button type="button" class="btn primary" id="sheetCopy">Copy</button></div></div></div>
<script>{JS}</script>
</body></html>'''
os.makedirs('web/img', exist_ok=True)
open('web/index.html', 'w', encoding='utf-8').write(doc)
used = set(re.findall(r'src="img/([^"]+)"', doc))
for f in os.listdir('web/img'):
    if f not in used: os.remove('web/img/' + f)
for f in used: shutil.copy('report/img/' + f, 'web/img/' + f)
print('marks', n_marks, 'images', len(used), 'html KB', len(doc) // 1024)
