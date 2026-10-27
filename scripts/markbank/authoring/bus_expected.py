#!/usr/bin/env python3
"""The expected responses a Business scheme prints for each card, lifted as rows.

    python3 scripts/markbank/authoring/bus_expected.py [--write] [--report]

Every Business rubric card cites the scheme pages its allocation was read from
(`rubric.schemePages`: the tariff table first, then the "Possible Responses" or
"Support Notes" page). The card showed those pages as a crop and its buttons as
"Component 1 / Component 2", so the student could see the marks but not, on the
card itself, what the scheme wanted. Alex (2026-10-27): "all business questions
do carry a scheme answer" — so this reads each card's cited response pages and
lifts the block the scheme prints for that question part into
`rubric.expected`, one item per printed response ("(i) …", "• …", a heading
with the prose under it), cut from the scheme's own lines and never retyped.

How a block is found, and only found:
  * the part marker the scheme prints — "(B)", "2 (B)", "B (ii)", "10. (i)",
    a Section 1 question number — on a cited page, else on the page before or
    the three after (a block can start on the page before the one cited);
  * it runs to the next marker of the same level; a sub-part "(ii)" is cut
    inside its part;
  * the question the scheme echoes above its responses is dropped, so are the
    page furniture (footers, table heads, the marks column's "⟨8m⟩" tokens)
    and the page number a text layer welds onto a page's last line.

Where the scheme prints the part's marker but no response under it (a ratio
name whose workings follow in a table), where no marker can be found, or where
the block runs past 3,000 characters (a whole question rather than a part),
the card is left for review and listed, with its cited pages, in
scripts/markbank/authored/business-expected-review.json. Nothing is typed in
its place.

Re-running changes nothing: `expected` is a function of the scheme text.
"""
import json
import collections
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
AUTHORED = os.path.join(ROOT, 'components/MarkBank/cards/business/rubric-authored.json')
REVIEW = os.path.join(ROOT, 'scripts/markbank/authored/business-expected-review.json')
SCHEMES = os.path.join(ROOT, 'examiner-reports/business/schemes')
MAX_BLOCK = 3000
INLINE_FOOT = re.compile(r'\s*(?:LC Business \d{4} \((?:OL|HL)\)|Bus\.? ?\d{4} ?\((?:OL|HL)\) ?\d+|Page \d+ of \d+|Leaving Certificate(?: \d{4})?\s*[–-]\s*(?:Higher|Ordinary) Level(?: \d{4})?)\s*(?:⟨\d{1,2}⟩)?\s*')
_pages = {}

FOOT=re.compile(r'^\s*(?:Page \d+ of \d+|Bus\.? ?\d{4} ?\((?:OL|HL)\) ?\d+|LC Business \d{4} \((?:OL|HL)\)|Leaving Certificate\b.*|\d{1,2}\s*marks?|⟨\d+⟩|\d{1,2})\s*$')
def pages(year, level):
    key=(year,level)
    if key not in _pages:
        txt=open(os.path.join(SCHEMES, f'{year}-{"hl" if level == "higher" else "ol"}.md'), encoding='utf-8').read()
        parts=re.split(r'^## Page (\d+)\s*$', txt, flags=re.M)
        out={}
        for i in range(1,len(parts),2):
            # a text layer sets some running footers with no-break spaces: read them as spaces
            ls=[l.replace('\xa0', ' ').rstrip() for l in parts[i+1].splitlines() if l.strip()]
            # the page number a text layer welds onto a page's last line, before the footer test reads it
            if ls: ls[-1]=re.sub(r'\s*⟨\d{1,2}⟩\s*$', '', ls[-1])
            # a running footer the text layer set on a line of its own, or welded onto a line of content
            ls=[INLINE_FOOT.sub(' ', l).strip() for l in ls]
            ls=[l for l in ls if l and not FOOT.match(l)]
            out[int(parts[i])]=ls
        _pages[key]=out
    return _pages[key]
REF=re.compile(r'^(\d{4}) (HL|OL) Section (\d) (?:Q(\d+)|(ABQ))(?:\s*\(([A-Ea-e])\))?(?:\s*\((i|ii|iii|iv|v|vi)\))?')
def parse_ref(ref):
    m=REF.match(ref)
    if not m: return None
    year, lv, sec, q, abq, part, roman = m.groups()
    return dict(q=int(q) if q else 0, part=(part.upper() if part else None), roman=roman)
QPFX=r'(?:Q(?:uestion)?\.?\s*)?(?:{q}\s*[.)]?\s*)?'
def part_marker(line, q, part):
    # "(B) Outline", "2 (B)", "2. (B)", "Q2 (B)", "B (ii) …", "(b)", "B. Outline"
    return re.match(rf'^\s*{QPFX.format(q=q)}(?:\(\s*[{part}{part.lower()}]\s*\)|{part}\s*(?=\(|\.\s|\))|{part}\s+(?=[\'"‘“A-Z]))', line) is not None
def any_part_marker(line, q):
    return (re.match(rf'^\s*{QPFX.format(q=q)}(?:\(\s*[A-Ea-e]\s*\)|[A-E]\s*(?=\(|\.\s|\))|[A-E]\s+(?=[\'"‘“A-Z]))', line) is not None
            or re.match(r'^\s*Question\s+\d+\b', line, re.I) is not None or re.match(r'^\s*SECTION\s+\d', line) is not None
            or re.match(r'^\s*\d{1,2}\s*[.)]?\s*\(\s*[A-E]\s*\)', line) is not None)
RPFX=r'(?:\d+\s*[.)]?\s*)?(?:\(?\s*[A-E]\s*\)?\s*)?'
def roman_marker(line, roman):
    return re.match(rf'^\s*{RPFX}\(\s*{roman}\s*\)', line, re.I) is not None
def any_roman_marker(line):
    return re.match(rf'^\s*{RPFX}\(\s*(?:i|ii|iii|iv|v|vi)\s*\)', line, re.I) is not None
def s1_marker(line, q):
    return (re.match(rf'^\s*{q}\s*[.)]\s', line) is not None or re.match(rf'^\s*Q(?:uestion)?\.?\s*{q}\b', line, re.I) is not None
            or re.match(rf'^\s*{q}\s+(?=[A-Z(•“‘]|\d\s+\d)', line) is not None)
def any_s1_next(line, q):
    if TABLEHEAD_LINE.match(line): return True
    m=re.match(r'^\s*(?:Q(?:uestion)?\.?\s*)?(\d{1,2})\s*[.)]?(?:\s+(?=[A-Z(•“‘]|\d\s+\d)|\s*$)', line)
    return m is not None and int(m.group(1))>q and int(m.group(1))<=q+3
TABLEHEAD_LINE = re.compile(r'^\s*Question\s+Possible\s+Responses?\s+(?:Max|Marks)', re.I)
def _locate(card):
    info=parse_ref(card['questionRef'])
    if not info: return None, 'unparsed ref', None
    P=pages(card['year'], card['level'])
    cited=card['rubric']['schemePages']
    resp=cited[1:] if len(cited)>1 else cited
    # widen one page either side: a block can start on the page before or run onto the next
    span=list(range(min(resp)-1, max(resp)+4))
    lines=[]; origin=[]
    for pg in span:
        for l in P.get(pg, []): lines.append(l); origin.append(pg)
    if not lines: return None, 'no page text', None
    q, part, roman = info['q'], info['part'], info['roman']
    sec=card['section']
    # prefer a marker ON a cited page; fall back to the widened span
    def find(pred, prefer):
        for i,l in enumerate(lines):
            if origin[i] in prefer and pred(l): return i
        for i,l in enumerate(lines):
            if pred(l): return i
        return None
    if sec=='1' and part:
        qs=find(lambda l: s1_marker(l,q), set(resp))
        if qs is None:
            # the page prints the parts without their question number: fall through to the part search
            sec='fallthrough'
    if sec=='1' and part:
        qe=len(lines)
        for j in range(qs+1,len(lines)):
            if any_s1_next(lines[j], q) or re.match(r'^\s*SECTION\s+\d', lines[j]): qe=j; break
        sub=lines[qs:qe]
        ps=None
        for i,l in enumerate(sub):
            if part_marker(l,q,part) or (i==0 and re.search(rf'\(\s*{part}\s*\)', l, re.I)): ps=i; break
        if ps is None: return None, 's1 part marker', None
        pe=len(sub)
        for j in range(ps+1,len(sub)):
            if any_part_marker(sub[j],q) and not part_marker(sub[j],q,part): pe=j; break
        block=sub[ps:pe]
        if roman:
            rs=None
            for i,l in enumerate(block):
                if roman_marker(l,roman) or (i==0 and re.search(rf'\(\s*{roman}\s*\)', l)): rs=i; break
            if rs is None: return None, 'roman marker', None
            re_=len(block)
            for j in range(rs+1,len(block)):
                if any_roman_marker(block[j]) and not roman_marker(block[j],roman): re_=j; break
            block=block[rs:re_]
        text='\n'.join(block)
        if len(text)<12: return None, 'tiny block', None
        return block, 'ok', origin[qs+ps], qe < len(lines)
    if sec=='1' and not part:
        start=find(lambda l: s1_marker(l,q), set(resp))
        if start is None: return None, 's1 marker', None
        end=len(lines)
        for j in range(start+1,len(lines)):
            if any_s1_next(lines[j], q) or re.match(r'^\s*SECTION\s+\d', lines[j]) or re.match(r'^\s*Question\s+\d+\b', lines[j], re.I): end=j; break
        block=lines[start:end]
    elif part:
        start=find(lambda l: part_marker(l,q,part), set(resp))
        if start is None and roman:
            rs=find(lambda l: roman_marker(l,roman), set(resp))
            if rs is not None and origin[rs] in set(resp):
                end=len(lines)
                for j in range(rs+1,len(lines)):
                    if (any_roman_marker(lines[j]) and not roman_marker(lines[j],roman)) or any_part_marker(lines[j],q): end=j; break
                block=lines[rs:end]
                return (block, 'ok', origin[rs], end < len(lines)) if len('\n'.join(block))>=12 else (None, 'tiny block', None)
        if start is None: return None, 'part marker', None
        end=len(lines)
        for j in range(start+1,len(lines)):
            if any_part_marker(lines[j],q) and not part_marker(lines[j],q,part): end=j; break
        block=lines[start:end]
    else:
        return None, 'no part (whole question)', None
    if roman:
        rs=None
        for i,l in enumerate(block):
            if roman_marker(l,roman) or (i==0 and re.search(rf'\(\s*{roman}\s*\)', l)): rs=i; break
        if rs is None: return None, 'roman marker', None
        re_=len(block)
        for j in range(rs+1,len(block)):
            if any_roman_marker(block[j]) and not roman_marker(block[j],roman): re_=j; break
        block=block[rs:re_]
    text='\n'.join(block)
    if len(text)<12: return None, 'tiny block', None
    return block, 'ok', origin[start], end < len(lines)

MARK = re.compile(r'\s*⟨([^⟩]*)⟩')
# "(20 marks)", "(3 marks)": the part's tariff printed in the text, not a response.
MARKS_CELL = re.compile(r'\s*\(\s*\d{1,3}\s*marks?\s*\)')
HEADMARK = re.compile(r'^\s*(?:Q(?:uestion)?\.?\s*)?(?:\d{1,2}\s*[.)]?\s*)?(?:\(?\s*[A-Ea-e]\s*\)\s*|[A-E]\s+(?=[A-Z‘\'"]))?(?:\(\s*(?:i|ii|iii|iv|v|vi)\s*\)\s*)?')
ITEM = re.compile(r'^\s*(?:\((?:i|ii|iii|iv|v|vi|vii|viii|ix|x)\)|[•●▪■➢\-–]|\d{1,2}\s*[.)](?=\s)|[A-H]\s*[.)](?=\s)|\((?:[a-h])\))\s*')
TABLEHEAD = re.compile(r'^(Question\s+Possible\s+Responses?\s+(?:Max|Marks)|mark|Mark|Support Notes|SECTION\s+\d|PART\s+\d\s*:?|QUESTION\s+\d|Possible Responses\s+Marks)\s*$', re.I)


# What a broken subset font leaves in a text layer; businessGlyphs.test refuses a card that carries one.
MANGLED = re.compile('[\u0100-\u1fff\ue000-\uf8ff\ufb00-\ufb4f\ufffd\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')


def locate(card):
    """(block, reason, page, bounded): bounded says the block ends at a found marker, not at the end of the pages read."""
    found = _locate(card)
    return found if len(found) == 4 else (*found, False)


def norm(s):
    return re.sub(r'[^a-z0-9]+', '', s.lower())


def clean(card, block):
    """The block's lines without the marks column, the furniture and the echoed question."""
    out = []
    for line in block:
        text = MARKS_CELL.sub('', MARK.sub('', line)).strip()
        if text and not TABLEHEAD.match(text) and not CTD.match(text) and not BARE_MARKER.match(text):
            out.append(text)
    if not out:
        return []
    out[0] = HEADMARK.sub('', out[0], count=1).strip()
    out = [t for t in out if t]
    qn = norm(card['questionText'])
    while out and (echoes(out[0], qn) or asks(out[0])):
        echo = out.pop(0)
        # the echo's wrapped continuation, where the line stopped mid-sentence: lines that start lower-case
        while out and out[0][:1].islower() and not re.search(r'[.?!:]$', echo):
            echo = out.pop(0)
    kept = []
    for text in out:
        if asks(text):
            kept.append(BOUNDARY)
            continue
        kept.append(unicodedata.normalize('NFKC', text))
    return kept


def asks(line):
    """Whether a line is the scheme reprinting an ask, with or without its "(ii)" marker."""
    bare = HEADMARK.sub('', line, count=1).strip()
    return bool(ASK.match(bare)) and len(bare.split()) <= 30


BOUNDARY = '\x00'


def echoes(line, qn):
    n = norm(line)
    return bool(n) and (n[:25] in qn or n[:40] in qn)


# The scheme reprints the ask over its responses: an imperative line at the top of a block is the question, not an answer.
ASK = re.compile(r'^(?:Outline|Explain|Describe|Illustrate|Discuss|Evaluate|Define|State|Name|List|Calculate|Identify|Distinguish|Analyse|Draft|Complete|Indicate|Choose|Write|Give|Suggest|Compare|Contrast|Show|Match|Tick|Read|Using|What|Which|Why|How)\b.*(?:\?|\.|:|\d\s*marks?)\s*$')


# "B (ctd)", "A (ctd)": the scheme's continuation note at a page break.
CTD = re.compile(r'^\s*\(?[A-E]\)?\s*\(ctd\.?\)\s*$', re.I)
# A marker repeated on a line of its own: "1 (C) (ii)", "7 C", "(a)".
BARE_MARKER = re.compile(r'^\s*(?:\d{1,2}\s*[.)]?\s*)?(?:\(?\s*[A-Ea-e]\s*\)?\s*)?(?:\(\s*(?:i|ii|iii|iv|v|vi)\s*\)\s*)?:?\s*$')


def is_head(text):
    return bool(text) and len(text.split()) <= 6 and not re.search(r'[.;,]$', text) \
        and not ITEM.match(text) and not re.search(r'\d', text) and text[0].isupper()


def split_items(lines):
    """One item per printed response: a marker line, or a heading with its prose."""
    items = []
    fresh = False
    for text in lines:
        if text == BOUNDARY:
            fresh = True
            continue
        text = re.sub(r'^\s*\d{1,2}\s+[A-E]\s+(?=[A-Z])', '', text)
        if fresh and not ITEM.match(text) and not is_head(text):
            items.append({'text': text, 'detail': []})
            fresh = False
            continue
        fresh = False
        if ITEM.match(text):
            body = ITEM.sub('', text, count=1).strip()
            if not body:
                fresh = True
                continue
            items.append({'text': body, 'detail': []})
        elif is_head(text) and (not items or items[-1]['detail'] or items[-1].get('head') or not items[-1].get('head')):
            items.append({'text': text, 'detail': [], 'head': True})
        elif items:
            last = items[-1]
            if last.get('head') or last['detail'] or len(last['text']) > 160 or re.search(r'[.;:]$', last['text']):
                last['detail'].append(text)
            else:
                last['text'] += ' ' + text
        else:
            items.append({'text': text, 'detail': []})
    out = []
    for n, item in enumerate(items, 1):
        row = {'id': f'e{n}', 'text': item['text']}
        if item['detail']:
            row['detail'] = item['detail']
        out.append(row)
    return out


_page_text = {}


def page_text(year, level):
    """The whole scheme as the gate normalises it: no page heads, footers, marks cells or marks column."""
    key = (year, level)
    if key not in _page_text:
        raw = open(os.path.join(SCHEMES, f'{year}-{"hl" if level == "higher" else "ol"}.md'), encoding='utf-8').read()
        lines = []
        for line in raw.replace('\xa0', ' ').splitlines():
            if re.match(r'^## Page \d+\s*$', line):
                continue
            line = MARKS_CELL.sub('', MARK.sub('', INLINE_FOOT.sub(' ', line))).strip()
            if line and not FOOT.match(line):
                lines.append(line)
        _page_text[key] = norm(unicodedata.normalize('NFKC', ' '.join(lines)))
    return _page_text[key]


def under_parent(card, roman):
    """The sub-part's responses where the scheme lists every sub-question first and answers them after.

    Cut from the SECOND print of the sub-part's marker ("(i) Net Profit Margin = …" after
    "(i) Net profit margin;") to the next sub-part's; where the scheme answers the
    sub-questions with one list instead, the whole list below the questions.
    """
    parent = dict(card)
    parent['questionRef'] = re.sub(r'\s*\((?:i|ii|iii|iv|v|vi)\)\s*$', '', card['questionRef'])
    block, why, page, bounded = locate(parent)
    if not block:
        return None, None
    marks = [i for i, line in enumerate(block) if roman_marker(line, roman) or (i == 0 and re.search(rf'\(\s*{roman}\s*\)', line))]
    if len(marks) >= 2:
        start = marks[1]
        end = next((j for j in range(start + 1, len(block)) if any_roman_marker(block[j]) and not roman_marker(block[j], roman)), len(block))
        return block[start:end], page
    return block, page


def expected_for(card):
    """(expected, None) or (None, reason) for one authored card."""
    block, why, page, bounded = locate(card)
    if not block:
        return None, why
    # A block that runs to the end of the pages read, not to a marker, and is this long is a whole question's responses.
    if not bounded and len('\n'.join(block)) > MAX_BLOCK:
        return None, 'unbounded block over 3000 characters: a whole question, not this part'
    lines = clean(card, block)
    if not lines:
        info = parse_ref(card['questionRef'])
        if info and info['roman']:
            block, page = under_parent(card, info['roman'])
            lines = clean(card, block) if block else []
    if not lines:
        return None, 'the scheme prints the marker and the question but no response under it on the cited page'
    joined = ' '.join(lines)
    if MANGLED.search(joined):
        return None, 'text layer glyph damage on the cited page'
    letters = sum(ch.isalpha() for ch in joined)
    digits = sum(ch.isdigit() for ch in joined)
    if letters < 0.5 * len(joined.replace(' ', '')) or '✓' in joined:
        return None, 'table layout lost in the text layer'
    if len(lines) > 4 and digits > 0.25 * (letters + digits):
        return None, 'workings table flattened by the text layer'
    items = split_items(lines)
    corpus = page_text(card['year'], card['level'])
    for item in items:
        for piece in [item['text'], *item.get('detail', [])]:
            if norm(piece) not in corpus:
                return None, 'an item is not one slice of the page text: a table or diagram the text layer reordered'
    return {'page': page, 'items': items}, None



# ---------------------------------------------------------------- stage B: the page's own geometry ----
# What the markdown text layer lost — a table's rows, a tick under a column, a marker printed as separate
# tokens, "True"/"False" in a right-hand column — the page's word positions still hold. For a card the text
# reading leaves for review, the cited pages are read with PyMuPDF as word lines (words grouped by baseline,
# ordered by x): the marker is found on the cited response pages first (the tariff page is never a response
# page), the block runs to the next marker of the same level, to a line echoing a sibling card's question, or
# to the page's end; each line is an item — a table line stands alone, a tick names the column header above
# it, "True"/"False" at the right names its statement, a numbers row over a letters row pairs them — and the
# rest is split as the text reading splits it. Every word of every item is a word the page prints (checked
# against the page's own text); the glyph map and NFKC make the printed letters. A tick table whose ticks are
# drawn rather than typed, a marker the page does not print, or a block with no readable response stays in the
# review file with its reason.
import fitz
SIBLINGS = collections.defaultdict(list)
GLYPHMAP = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'glyphmap.json')))
BULLET_GLYPHS = {'\uf0b7': '•', '\uf0a7': '•', '\uf0d8': '•', '\uf076': '•', '\uf0fc': '✓', '\uf0a8': '✓'}
def repaired(text):
    return unicodedata.normalize('NFKC', ''.join(GLYPHMAP.get(ch, BULLET_GLYPHS.get(ch, ch)) for ch in text))
_docs = {}
def doc(year, fid):
    if (year, fid) not in _docs:
        _docs[(year, fid)] = fitz.open(os.path.join(ROOT, 'paper-trail-corpus', 'markingschemes', str(year), f'{fid}.pdf'))
    return _docs[(year, fid)]


docs={}
def doc(year,fid):
    if (year,fid) not in docs: docs[(year,fid)]=fitz.open(f'paper-trail-corpus/markingschemes/{year}/{fid}.pdf')
    return docs[(year,fid)]
TICK={'9','ü','✓','þ','√','P','',''}
GEO_FOOT=re.compile(r'^(?:Page \d+ of \d+|LC Business|Leaving Certificate|Bus\.?\s*\d{4})', re.I)
def lines_of(year,fid,p):
    page=doc(year,fid)[p-1]; W,H=page.rect.width,page.rect.height; rows=collections.defaultdict(list)
    for w in page.get_text('words'): rows[round(w[1]/3)].append((w[0]/W,w[1]/H,w[2]/W,w[4]))
    out=[]
    for k in sorted(rows):
        ws=sorted(rows[k], key=lambda w:w[0]); text=' '.join(t for *_,t in ws)
        if GEO_FOOT.match(text): continue
        out.append({'p':p,'y':ws[0][1],'x':ws[0][0],'ws':ws})
    return out
def marker_kind(ws, info):
    """Which marker a line starts with: ('q', n) | ('part', letter) | ('roman', r) | None. Tolerant of split tokens."""
    toks=[t for *_,t in ws[:4]]; x=ws[0][0]
    if x>0.2: return None
    t0=toks[0] if toks else ''
    m=re.match(r'^(\d{1,2})[.)]?$', t0)
    if m:
        # "1 A i …", "2 (B)", "10. (i)"
        rest=toks[1:]
        if rest and re.match(r'^\(?[A-Ea-e]\)?$', rest[0]):
            letter=rest[0].strip('()').upper()
            if len(rest)>1 and re.match(r'^\(?(i|ii|iii|iv|v|vi)\)?$', rest[1]): return ('roman', rest[1].strip('()'), letter, int(m.group(1)))
            return ('part', letter, int(m.group(1)))
        if rest and re.match(r'^\((i|ii|iii|iv|v|vi)\)$', rest[0]): return ('roman', rest[0].strip('()'), None, int(m.group(1)))
        return ('q', int(m.group(1))) if x<0.15 else None
    m=re.match(r'^\(?([A-Ea-e])\)?$', t0)
    if m and (len(t0)>1 or (len(toks)>1 and toks[1][:1].isupper()) or (len(toks)>1 and re.match(r'^\((i|ii|iii|iv|v|vi)\)$', toks[1]))):
        if len(toks)>1 and re.match(r'^\(?(i|ii|iii|iv|v|vi)\)?$', toks[1]): return ('roman', toks[1].strip('()'), m.group(1).upper(), None)
        return ('part', m.group(1).upper(), None)
    m=re.match(r'^\(?(i|ii|iii|iv|v|vi)\)?$', t0)
    if m and x<0.2: return ('roman', m.group(1), None, None)
    return None
def block_for(card):
    info=parse_ref(card['questionRef'])
    if not info: return None,'unparsed ref'
    rub=card['rubric']; fid=rub['schemeFileid']; year=card['year']
    cited=rub['schemePages']; n=len(doc(year,fid))
    # the first cited page is the tariff table; the responses are on the pages after it (and may start a page early)
    resp=sorted(set(cited[1:])) or sorted(set(cited))
    pages=[p for p in range(max(1,min(resp)-1), min(n,max(resp)+3)+1) if p!=cited[0] or len(cited)==1]
    lines=[l for p in pages for l in lines_of(year,fid,p)]
    # the marker is looked for on the cited pages first, then the page before, then the pages after
    rank={p:(0 if p in resp else 1 if p<min(resp) else 2) for p in pages}
    q=info['q']; part=info.get('part'); roman=info.get('roman'); section=info.get('section')
    want_level='roman' if roman else ('part' if part else 'q')
    start=None; candidates=[]
    for i,l in enumerate(lines):
        mk=marker_kind(l['ws'], info)
        if not mk: continue
        hit=(want_level=='q' and mk[0]=='q' and mk[1]==q) or \
            (want_level=='part' and mk[0]=='part' and mk[1].upper()==str(part).upper() and (mk[2] in (None,q))) or \
            (want_level=='roman' and mk[0]=='roman' and mk[1]==roman and (mk[2] in (None,str(part).upper())) and (mk[3] in (None,q)))
        if hit: candidates.append((rank[l['p']], i))
    if not candidates: return None,f'{want_level} marker not found'
    start=min(candidates)[1]
    end=len(lines); qn=norm(card['questionText'])
    for j in range(start+1,len(lines)):
        mk=marker_kind(lines[j]['ws'], info)
        if mk and (mk[0]==want_level or (want_level=='roman' and mk[0] in ('part','q')) or (want_level=='part' and mk[0]=='q')):
            end=j; break
        if j-start>=2 and lines[j]['x']<0.2:
            t=item_text(lines[j]['ws'], strip_marker=True); n=norm(t)
            if len(n)>=25 and not echoes(t, qn) and any(cid!=card['id'] and n[:25] in sq for cid,sq in SIBLINGS[(card['year'],card['level'])]): end=j; break
    block=lines[start:end]
    # a sub-part listed first and answered after: its marker printed a second time opens the responses
    if want_level=='roman' and len(block)<=2:
        later=[j for j in range(end, len(lines)) if (marker_kind(lines[j]['ws'], info) or (None,))[0]=='roman' and marker_kind(lines[j]['ws'], info)[1]==roman]
        if later:
            s2=later[0]; e2=len(lines)
            for j in range(s2+1,len(lines)):
                mk=marker_kind(lines[j]['ws'], info)
                if mk and mk[0] in ('roman','part','q'): e2=j; break
            block=lines[s2:e2]
    return block, None
def item_text(ws, strip_marker=True):
    toks=[(x0,t) for x0,_,_,t in ws]
    out=[]
    for x0,t in toks:
        if x0>=0.8 and (re.fullmatch(r'\d{1,3}|x|\d+m|\(\d+\)', t) or t in ('Max','mark','marks','Marks')): continue       # the marks column
        if re.fullmatch(r'\(\d{1,2}\)', t) and x0>0.35: continue         # a line price "(1)"
        t=re.sub(r'^\(\d{1,2}\)(?=\S)', '', t)                           # "(1)13,600"
        if re.fullmatch(r'⟨[^⟩]*⟩', t): continue
        out.append(t)
    text=' '.join(out)
    if strip_marker: text=re.sub(r'^(?:\d{1,2}[.)]?\s+)?(?:\(?[A-Ea-e]\)?\s+)?(?:\(?(?:i|ii|iii|iv|v|vi)\)?\s+)?', '', text, count=1)
    return repaired(text).strip()
def expected_geo(card):
    """(expected, None) or (None, reason) from the cited pages' geometry; see the stage B note above."""
    block,why=block_for(card)
    if not block: return None,why
    page=block[0]['p']
    texts=[]
    for i,l in enumerate(block):
        t=item_text(l['ws'], strip_marker=(i==0))
        if not t or TABLEHEAD.match(t) or CTD.match(t) or BARE_MARKER.match(t) or re.match(r'^Question\s+Possible\s+Response', t) or re.fullmatch(r'\(?(?:i|ii|iii|iv|v|vi|[A-E])\)?', t) or re.match(r'^(?:Sample|Possible) responses? (?:may|could) include', t, re.I): continue
        texts.append((l,t))
    def is_header(l,t):
        return len(l['ws'])>=2 and all(len(tok)<=12 for *_,tok in l['ws']) and not re.search(r'[.;:]$', t) and sum(1 for *_,tok in l['ws'] if tok[:1].isupper())>=2 and l['ws'][0][0]>0.3 and not any(tok in TICK for *_,tok in l['ws'])
    headers={id(l) for l,t in texts if is_header(l,t)}
    qn=norm(card['questionText'])
    popped=0
    def asks_wrapped(k):
        t=item_text(texts[k][0]['ws'], strip_marker=True)
        if asks(t): return True
        if k+1<len(texts) and texts[k+1][1][:1].islower(): return asks((t+' '+texts[k+1][1]).rstrip()+'.') or asks(t.rstrip()+'.')
        return False
    cap=1 if any(tok.rstrip('.').lower() in ('true','false') and x0>0.65 for l,t in texts for x0,_,_,tok in l['ws']) else 2
    while texts and popped<cap and id(texts[0][0]) not in headers and (echoes(texts[0][1], qn) or asks_wrapped(0)):
        echo=texts.pop(0)[1]; popped+=1
        while texts and texts[0][1][:1].islower() and not re.search(r'[.?!:]$', echo): echo=texts.pop(0)[1]
    if not texts: return None,'no response under the marker'
    items=[]
    header=None
    pending_numbers=None
    for l,t in texts:
        toks=[tok for *_,tok in l['ws']]
        # a TRUE/FALSE answer at the right of a statement, on its line or the line after
        tf=[(x0,tok) for x0,_,_,tok in l['ws'] if tok.rstrip('.').lower() in ('true','false') and x0>0.65]
        if tf:
            stmt=' '.join(tok for x0,_,_,tok in l['ws'] if x0<=0.65)
            if stmt.strip():
                items.append({'text': f"{stmt.strip()} — {tf[0][1].rstrip('.')}", 'detail': [], 'geo': 'table'})
            elif items and ' — ' not in items[-1]['text']:
                items[-1]['text']+=f" — {tf[0][1].rstrip('.')}"; items[-1]['geo']='tf'
            continue
        if items and items[-1].get('geo')=='tf' and t[:1].islower():
            stmt,ans=items[-1]['text'].rsplit(' — ',1); items[-1]['text']=f"{stmt} {t} — {ans}"; continue
        # a matching grid: a line of numbers "1. 2. 3." over a line of letters "D A E"
        if len(toks)>=3 and all(re.fullmatch(r'\d{1,2}\.?', tok) for tok in toks):
            pending_numbers=[(x0,tok.rstrip('.')) for x0,_,_,tok in l['ws']]; continue
        if pending_numbers and len(toks)==len(pending_numbers) and all(re.fullmatch(r'[A-H]', tok) for tok in toks):
            for (x0,n),(x1,_,_,letter) in zip(pending_numbers, l['ws']): items.append({'text': f"{n} — {letter}", 'detail': [], 'geo': 'table'})
            pending_numbers=None; continue
        pending_numbers=None
        ticks=[x0 for x0,_,_,tok in l['ws'] if tok in TICK and x0>0.3]
        words=[(x0,tok) for x0,_,_,tok in l['ws'] if tok not in TICK]
        if ticks and header:
            label=' '.join(tok for x0,tok in words if x0<min(ticks)) or t
            picks=[min(header, key=lambda h: abs(h[0]-x))[1] for x in ticks]
            items.append({'text': f"{label} — {' / '.join(picks)}", 'detail': [], 'geo': 'tick'}); continue
        if id(l) in headers:
            phrases=[]; cur=[]
            for k,(x0,y0,x1,tok) in enumerate(l['ws']):
                if cur and x0-cur[-1][2]>0.02: phrases.append(cur); cur=[]
                cur.append((x0,y0,x1,tok))
            if cur: phrases.append(cur)
            header=[((ph[0][0]+ph[-1][2])/2, ' '.join(tk for *_,tk in ph)) for ph in phrases]
            items.append({'text': t, 'detail': [], 'geo': 'header'}); continue
        if asks(t) or asks(item_text(l['ws'], strip_marker=True)): items.append({'text': BOUNDARY, 'detail': []}); continue
        figs=sum(1 for *_,tok in l['ws'] if re.fullmatch(r'[€(]?\d[\d,.]*%?\)?', tok) and len(re.sub(r'\D','',tok))>=2)
        if figs>=1 and len(l['ws'])<=9: items.append({'text': t, 'detail': [], 'geo': 'table'}); continue
        if t.strip(): items.append({'text': t, 'detail': []})
    if header is not None and not any(it.get('geo')=='tick' for it in items): return None, 'tick table: the ticks are not in the text layer'
    # join continuation lines and split bulleted items as stage A does; tick rows stay whole
    out=[]; run=[]
    def flush_run():
        for o in split_items(run):
            if o['text'].strip() and o['text']!=BOUNDARY: out.append({k:v for k,v in o.items() if k!='id'})
        run.clear()
    for it in items:
        if it.get('geo')=='header': continue
        if it.get('geo') in ('table','tick','tf'):
            flush_run(); out.append({'text': it['text']})
        else: run.append(it['text'])
    flush_run()
    # a marks cell printed as a line, and a fragment the page break left mid-sentence at the top, are not responses
    out=[o for o in out if not re.fullmatch(r'\(\d{1,3}\s*marks?\)', o['text'].strip())]
    while out and out[0]['text'][:1].islower(): out.pop(0)
    out=[{'id':f'e{n}', **{k:v for k,v in o.items() if k!='id'}} for n,o in enumerate(out,1)]
    joined=' '.join(o['text']+' '+' '.join(o.get('detail',[])) for o in out)
    letters=sum(ch.isalpha() for ch in joined)
    if not out or letters<10: return None,'no readable response'
    # a page whose text layer dropped or shifted letters ("xplain", "Wz") is not readable either
    if MANGLED.search(joined) or re.search(r'\bxplain|:ob|Wz|h\^|\b[A-Za-z]*[\^|]\w', joined): return None,'text layer glyph damage on the page'
    if len(joined)>MAX_BLOCK: return None,'block over 3000 characters'
    # every word of every item is a word the page prints
    # every word of every item is a word the scheme's text layer prints, as the gate reads it (page_text)
    corpus=page_text(card['year'], card['level'])
    for o in out:
        for piece in [o['text'], *o.get('detail', [])]:
            for wd in piece.replace('—',' ').split():
                if norm(wd) and norm(wd) not in corpus: return None, f'word not in the scheme text: {wd}'
    return {'page':page,'items':out,'lifted':'geometry'}, None


def main():
    with open(AUTHORED, encoding='utf-8') as fh:
        data = json.load(fh)
    review = []
    lifted = 0
    for card in data['cards']:
        SIBLINGS[(card['year'], card['level'])].append((card['id'], norm(card['questionText'])))
    geometry = 0
    for card in data['cards']:
        expected, why = expected_for(card)
        card['rubric'].pop('expected', None)
        if not expected:
            geo, geo_why = expected_geo(card)
            if geo:
                expected = geo
                geometry += 1
            else:
                why = f'{why}; geometry: {geo_why}'
        if expected:
            card['rubric']['expected'] = expected
            lifted += 1
        else:
            review.append({'id': card['id'], 'questionRef': card['questionRef'], 'schemePages': card['rubric']['schemePages'], 'reason': why})
    print(f'{geometry} of them from the page geometry', file=sys.stderr)
    print(f'{lifted} cards lifted, {len(review)} left for review', file=sys.stderr)
    if '--report' in sys.argv:
        import collections
        print(collections.Counter(r['reason'] for r in review), file=sys.stderr)
    if '--write' in sys.argv:
        with open(AUTHORED, 'w', encoding='utf-8') as fh:
            json.dump(data, fh, ensure_ascii=False, indent=1)
            fh.write('\n')
        with open(REVIEW, 'w', encoding='utf-8') as fh:
            json.dump(review, fh, ensure_ascii=False, indent=1)
            fh.write('\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
