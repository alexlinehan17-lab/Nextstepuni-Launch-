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
two more readings follow, in order:
  * a hand-checked slice (scripts/markbank/authored/business-expected-slices.json):
    the page region the responses sit in, named by eye for a part the scheme
    prints no marker for; the words are still the page's own (expected_slice);
  * the page geometry (expected_geo, stage B): PyMuPDF word positions, so a
    table's rows, a tick's column, a drawn ring's option, a True/False column
    and a matching grid read as rows; a page whose text layer names glyphs by
    mangled code points is rebuilt character by character through glyph_ids.py.
What none of them can lift is listed, with its cited pages and every
reading's reason, in scripts/markbank/authored/business-expected-review.json;
a slice entry marked `excluded` records the page evidence for a card that
holds nothing to lift (an image, a drawn chart). Nothing is typed in its place.

Re-running changes nothing: `expected` is a function of the scheme pages.
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
# a line ending in one of these was cut mid-phrase; its tail is on the next line
ASK_TAIL={'in','of','the','a','an','to','for','and','or','by','on','at','with','from','as','into','each','its','their','this','that','which','between','under','over','such'}


def echoes(line, qn):
    n = norm(line)
    return bool(n) and (n[:25] in qn or n[:40] in qn)


# The scheme reprints the ask over its responses: an imperative line at the top of a block is the question, not an answer.
ASK = re.compile(r'^(?:Outline|Explain|Describe|Illustrate|Discuss|Evaluate|Define|State|Name|List|Calculate|Identify|Distinguish|Analyse|Draft|Complete|Indicate|Choose|Write|Give|Suggest|Compare|Contrast|Show|Match|Tick|Circle|Provide|Read|Using|What|Which|Why|How)\b.*(?:\?|\.|:|\d\s*marks?)\s*$')


# "B (ctd)", "A (ctd)": the scheme's continuation note at a page break.
CTD = re.compile(r'^\s*\(?[A-E]\)?\s*\(ctd\.?\)\s*$', re.I)
# A marker repeated on a line of its own: "1 (C) (ii)", "7 C", "(a)".
BARE_MARKER = re.compile(r'^\s*(?:\d{1,2}\s*[.)]?\s*)?(?:\(?\s*[A-Ea-e]\s*\)?\s*)?(?:\(\s*(?:i|ii|iii|iv|v|vi)\s*\)\s*)?:?\s*$')


def is_head(text):
    return bool(text) and len(text.split()) <= 6 and not re.search(r'[.;,]["”’]?$', text) \
        and not ITEM.match(text) and not re.search(r'\d', text) and text[0].isupper() \
        and text.count('”') <= text.count('“')   # "Europe and Asia.”" closes the quotation the line above opened


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
        _page_text[(year, level, 'raw')] = norm(unicodedata.normalize('NFKC', raw))
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
AMBIG_TICK={'9','P'}   # a digit or letter in the text layer: a tick only left of the marks column
def is_tick(tok, x0, ws=None, cols=()):
    if tok not in TICK or x0<=0.3: return False
    if tok not in AMBIG_TICK or x0<0.8: return True
    # '9' or 'P' in the marks column: a tick when a statement runs up to it, or when a tick column of the table is there
    if ws is not None and sum(1 for w in ws if re.search('[A-Za-z]{2}', w[3]) and w[0]<x0-0.05)>=2: return True
    return any(abs(x0-c)<0.02 for c in cols)
def tick_cols(texts):   # the x of every tick a statement establishes
    return [x0 for l,t in texts for x0,_,_,tok in l['ws'] if is_tick(tok, x0, l['ws'])]
GEO_FOOT=re.compile(r'^(?:Page \d+ of \d+|LC Business|Leaving Certificate|Bus\.?\s*\d{4})', re.I)
# a tick, arrow or check the marks column sets from a symbol font: a private-use glyph, not a word
PUA=re.compile('[\ue000-\uf8ff]')
KEEP_PUA=set(GLYPHMAP)|set(BULLET_GLYPHS)|TICK
# the marks column's cells, wherever the text layer set them: "(5+5)", "3+3+2+2", "10(5+5)", "2@5(2+3)", "(15m+5m)", "(2 x 5m)",
# "(2m + 2m)" split into its tokens, and a "+" or "m" the layer left on its own
MARKS_TOKEN=re.compile(r'^(?:\(?\d{1,2}\s*m?(?:\s*[+,]\s*\d{1,2}\s*m?)+\)?|\(\d{1,2}m\)|\d{1,2}\(\d{1,2}(?:\+\d{1,2})*\)|\d{1,2}@\d{1,2}m?(?:\([^)]*\))?|\d{1,2}m|\(\d{1,2}\s*[x×]\s*\d{1,2}m?\))$')
sys.path.insert(0, os.path.join(ROOT, 'scripts', 'markbank'))
import glyph_ids as _glyph_ids
_GLYPH_TABLE=_glyph_ids.load_table()
def page_words(page):
    """The page's words. Where the text layer names a glyph with a mangled code point the repair map does not
    know (2016 OL's Calibri2 subset reports U+FFFD, "ǆĂŵƉůĞƐ" for "Examples"), the words are rebuilt from
    the page's rawdict characters, each read by its glyph id through glyph_ids.py — the table the scheme
    extractor and repair_scheme_glyphs.py read; nothing is mapped by hand."""
    ws=page.get_text('words')
    if not any(MANGLED.search(w[4]) and any(MANGLED.match(ch) and not PUA.match(ch) and ch not in GLYPHMAP for ch in w[4]) for w in ws): return ws
    origin=_glyph_ids.page_glyphs(page); unnamed=_glyph_ids.page_unnamed(page); out=[]
    for blk in page.get_text('rawdict')['blocks']:
        for line in blk.get('lines', []):
            cur=[]
            def flush():
                if cur:
                    x0=min(c[1][0] for c in cur); y0=min(c[1][1] for c in cur); x1=max(c[1][2] for c in cur); y1=max(c[1][3] for c in cur)
                    out.append((x0,y0,x1,y1,''.join(c[0] for c in cur),0,0,0)); cur.clear()
            for sp in line.get('spans', []):
                size=sp.get('size', 10)
                for ch in sp['chars']:
                    text=_glyph_ids.repair_char(ch, origin, _GLYPH_TABLE, unnamed)
                    if text.isspace() or (cur and ch['bbox'][0]-cur[-1][1][2]>0.25*size):
                        flush()
                        if text.isspace(): continue
                    cur.append((text, ch['bbox']))
            flush()
    return out
def _figure_only(ws):
    if len(ws)>=3 and all(re.fullmatch(r'\d{1,2}\.?', t) for *_,t in ws): return False   # a matching grid's numbers, or a row of marks
    return all(re.fullmatch(r'[€$(\[]?[-–]?\d[\d,.·]*%?[)\]]?[❶-❿]?|\(?\d{1,2}m(?:arks?)?\)?|\(?(?:i|ii|iii|iv|v|vi)\)?|[A-D]|[=:+\-–x×/•◆●]', t) for *_,t in ws)
def _bare_marker(ws): return len(ws)<=2 and all(re.fullmatch(r'\(?(?:\d{1,2}|[A-Ea-e]|i{1,3}|iv|vi?)[.)]?', t) for *_,t in ws)
def _same_line(a, b):
    if any(x0<bx1-0.002 and x1>bx0+0.002 for x0,_,x1,_ in a for bx0,_,bx1,_ in b): return False   # overlapping words are two lines
    if all(t in TICK for *_,t in a) or all(t in TICK for *_,t in b): return False   # a tick on its own line ticks the statement nearest it
    gap=max(min(w[0] for w in b)-max(w[2] for w in a), min(w[0] for w in a)-max(w[2] for w in b))
    return _figure_only(a) or _figure_only(b) or _bare_marker(a) or _bare_marker(b) or (gap<0.03 and min(len(a),len(b))<=3)
def lines_of(year,fid,p):
    page=doc(year,fid)[p-1]; W,H=page.rect.width,page.rect.height; rows=collections.defaultdict(list)
    for w in page_words(page): rows[round(w[1]/3)].append((w[0]/W,w[1]/H,w[2]/W,w[4]))
    out=[]
    for k in sorted(rows):
        ws=sorted(rows[k], key=lambda w:w[0]); text=' '.join(t for *_,t in ws)
        if GEO_FOOT.match(text): continue
        # a table's figure set a point or two off its label's baseline ("PAYE (20% of €30,000)" / "6000"), a part marker beside its
        # statement, or words continuing a line in a smaller face ("[county/region/country etc.]") are the same line; two columns
        # that happen to share a baseline, and a note in the far margin, are not
        if out and ws[0][1]-out[-1]['y']<0.0045 and _same_line(out[-1]['ws'], ws):
            merged=sorted(out[-1]['ws']+ws, key=lambda w:w[0]); out[-1]={'p':p,'y':min(out[-1]['y'],ws[0][1]),'x':merged[0][0],'ws':merged}; continue
        out.append({'p':p,'y':ws[0][1],'x':ws[0][0],'ws':ws})
    return out
ROMAN=re.compile(r'^\(?(i|ii|iii|iv|v|vi)\)?$')
# "A Merger is…", "A Franchise is…": the article, not the part marker, when a verb follows the noun
VERBISH={'is','are','was','were','means','refers','involves','occurs','sells','provides','gives','takes','allows','uses','has','can','will','may','describes','happens','exists','applies','includes','consists','relates','shows','states','sets'}
def marker_kind(ws, info):
    """Which marker a line starts with: ('q', n) | ('part', letter, q) | ('roman', r, letter, q) | None. Tolerant of split tokens.
    A question number sits at the left margin; a part letter may be indented to 0.2 (0.3 in parentheses, as a workings
    table's "(a)"), a roman to 0.35. "5(D)" is a number welded to its part; a bare letter on a line of its own is a part."""
    toks=[t for *_,t in ws[:4]]; x=ws[0][0]
    t0=toks[0] if toks else ''
    m=re.match(r'^(\d{1,2})\(([A-Ea-e])\)$', t0)
    if m and x<=0.2: return ('part', m.group(2).upper(), int(m.group(1)))
    m=re.match(r'^(\d{1,2})[.)]?$', t0)
    if m:
        if x>0.2: return None
        rest=toks[1:]
        if rest and re.match(r'^\(?[A-Ea-e]\)?$', rest[0]):
            letter=rest[0].strip('()').upper()
            if len(rest)>1 and ROMAN.match(rest[1]): return ('roman', rest[1].strip('()'), letter, int(m.group(1)))
            return ('part', letter, int(m.group(1)))
        if rest and re.match(r'^\((i|ii|iii|iv|v|vi)\)$', rest[0]): return ('roman', rest[0].strip('()'), None, int(m.group(1)))
        # "9." at the margin of an Ordinary Level support-notes page sits at 0.15–0.17
        return ('q', int(m.group(1))) if (x<0.15 or (x<0.17 and t0.endswith('.') and len(rest)>=3 and rest[0][:1].isupper())) else None
    m=re.match(r'^\(?([A-Ea-e])\)?$', t0)
    if m:
        paren=t0.startswith('(') or t0.endswith(')')
        if x>(0.3 if paren else 0.2): return None
        toks=[t0]+[t for t in toks[1:] if not MARKS_TOKEN.match(t)]   # "B 3@10(4+2+4)": the letter and its marks cell
        if len(toks)>1 and ROMAN.match(toks[1]): return ('roman', toks[1].strip('()'), m.group(1).upper(), None)
        if len(toks)==1 or paren: return ('part', m.group(1).upper(), None)
        if toks[1][:1].isupper():
            if t0=='A' and len(toks)>2 and toks[2].lower() in VERBISH: return None
            return ('part', m.group(1).upper(), None)
        return None
    m=ROMAN.match(t0)
    if m and x<0.35: return ('roman', m.group(1), None, None)
    return None
def same_marker(a, b):
    """Two markers naming the same part: "(B)" and "3 (B)", "(C) (ii)" and "(ii)"."""
    if not a or not b or a[0]!=b[0]: return False
    if a[0]=='q': return a[1]==b[1]
    if a[0]=='part': return a[1]==b[1] and (a[2] is None or b[2] is None or a[2]==b[2])
    return a[1]==b[1] and (a[2] is None or b[2] is None or a[2]==b[2]) and (a[3] is None or b[3] is None or a[3]==b[3])
def block_candidates(card):
    """Every block the card's marker opens, in the order to try them, each with whether a marker bounded it. A block that
    is only the question's echo yields nothing, and the responses follow under the marker printed again ("(ii) Calculate…"
    then "5 B (ii) Current Ratio"); the same part printed again ("3 (B) No/Maybe") continues one block; a sub-question the
    scheme echoes before answering ("(ii) Profit at forecast output;") does not end its sibling's block."""
    info=parse_ref(card['questionRef'])
    if not info: return [],'unparsed ref'
    rub=card['rubric']; fid=rub['schemeFileid']; year=card['year']
    cited=rub['schemePages']; n=len(doc(year,fid))
    resp=sorted(set(cited[1:])) or sorted(set(cited))
    pages=[p for p in range(max(1,min(resp)-1), min(n,max(resp)+3)+1) if p!=cited[0] or len(cited)==1]
    lines=[l for p in pages for l in lines_of(year,fid,p)]
    rank={p:(0 if p in resp else 1 if p<min(resp) else 2) for p in pages}
    q=info['q']; part=info.get('part'); roman=info.get('roman')
    want_level='roman' if roman else ('part' if part else 'q')
    marks=[marker_kind(l['ws'], info) for l in lines]
    qn=norm(card['questionText'])
    texts=[item_text(l['ws'], strip_marker=True) for l in lines]
    def hit(mk):
        return bool(mk) and ((want_level=='q' and ((mk[0]=='q' and mk[1]==q) or (mk[0]=='roman' and mk[3]==q and mk[1]=='i') or (mk[0]=='part' and mk[2]==q and mk[1]=='A'))) or
            (want_level=='part' and mk[0]=='part' and mk[1].upper()==str(part).upper() and (mk[2] in (None,q))) or
            (want_level=='roman' and mk[0]=='roman' and mk[1]==roman and (mk[2] in (None,str(part).upper())) and (mk[3] in (None,q))))
    def vagueness(mk):   # 0 when the marker names the card's part and question, more as it leaves them out
        return sum(1 for v in (mk[2:] if mk[0]=='roman' else mk[2:] if mk[0]=='part' else ()) if v is None)
    def q_of(mk): return None if not mk else (mk[1] if mk[0]=='q' else mk[2] if mk[0]=='part' else mk[3])
    def opens_parent(mk):
        if not mk: return False
        if part: return mk[0]=='part' and mk[1].upper()==str(part).upper() and q_of(mk) in (None,q)
        return q_of(mk)==q
    spans=[]
    for i,mk in enumerate(marks):
        if want_level=='roman' and opens_parent(mk):
            end=next((j for j in range(i+1,len(lines)) if marks[j] and ((part and marks[j][0] in ('part','q') and not (marks[j][0]=='part' and marks[j][1].upper()==str(part).upper())) or (not part and q_of(marks[j]) not in (None,q)))), len(lines))
            spans.append((i,end))
    inside=lambda i: 0 if any(a<=i<b for a,b in spans) else 1
    candidates=sorted((rank[l['p']], inside(i), vagueness(marks[i]), i) for i,l in enumerate(lines) if hit(marks[i]))
    if want_level=='roman': candidates=[c for c in candidates if c[0]<2]   # a sub-part's marker on a later page is another question's
    candidates=[(r,i) for r,_,_,i in candidates]
    if want_level=='q':
        # a question number sits at the page's own margin; "5. When a company's equity…" in a True/False list sits inside it
        margin={}
        for i,l in enumerate(lines):
            if marks[i] and marks[i][0]=='q': margin[l['p']]=min(margin.get(l['p'],1), l['x'])
        candidates=[c for c in candidates if lines[c[1]]['x']<=margin[lines[c[1]]['p']]+0.02]
    if not candidates: return [], f'{want_level} marker not found'
    def no_response_before(j, start):   # every line between the marker and j is the question's reprint, an ask, or short
        return all(len(norm(texts[k]))<12 or echoes(texts[k], qn) or asks(texts[k]) for k in range(start+1, j))
    def ends(j, start_mk, start):
        mk=marks[j]
        if not mk: return False
        if same_marker(mk, start_mk) and want_level!='q': return False
        own_q=mk[2] if mk[0]=='part' else mk[3] if mk[0]=='roman' else mk[1]
        if own_q is not None and own_q!=q: return True
        if mk[0]=='roman' and len(norm(texts[j]))>=12 and (echoes(texts[j], qn) or (asks(texts[j]) and no_response_before(j, start))): return False
        if want_level=='roman' and mk[0]=='part' and mk[1].upper()==str(part).upper() and (mk[2] in (None,q)): return False   # "C Market segmentation…": the part restated over its sub-part's responses
        return mk[0]==want_level or (want_level=='roman' and mk[0] in ('part','q')) or (want_level=='part' and mk[0]=='q')
    blocks=[]
    for _,start in candidates:
        if any(b[0]<=start<b[1] for b in blocks): continue
        end=len(lines); bounded=(max(pages)==n)
        for j in range(start+1,len(lines)):
            if ends(j, marks[start], start): end=j; bounded=True; break
            if (re.match(r'^(?:SECTION|PART)\s+\d|^Applied Business Question|^Section \d Applied Business', texts[j], re.I) or (want_level=='q' and TABLEHEAD_LINE.match(texts[j]))) and j>start+1: end=j; bounded=True; break
            if j-start>=2 and lines[j]['x']<0.2:
                nn=norm(texts[j])
                if len(nn)>=25 and not echoes(texts[j], qn) and any(cid!=card['id'] and nn[:25] in sq for cid,sq in SIBLINGS[(card['year'],card['level'])]): end=j; bounded=True; break
        blocks.append((start,end,bounded))
    out=[]
    own_ask=sub_asks(card)[0] if want_level=='roman' else None
    for start,end,bounded in blocks:
        block=lines[start:end]
        if own_ask:
            others_=sub_asks(card)[1]
            restated=[i for i,l in enumerate(block) if i>0 and len(norm(item_text(l['ws'], strip_marker=True)))>=20 and norm(item_text(l['ws'], strip_marker=True))[:32] in norm(own_ask) and not any(norm(item_text(l['ws'], strip_marker=True))[:32] in norm(o) for o in others_)]
            if restated: block=block[restated[-1]:]
        # a line the layout set on the marker's own baseline, a hair above it: "– €30,000" over "(ii) 270,000 240,000 =", the "FC …" row beside a bare "(b)"
        if start>0 and lines[start-1]['p']==lines[start]['p'] and abs(lines[start-1]['y']-lines[start]['y'])<0.004 and not marks[start-1] \
                and (BARE_MARKER.match(item_text(lines[start]['ws'], strip_marker=False)) or (want_level=='roman' and re.search(r'\d', texts[start-1]))):
            block=[lines[start-1]]+block
        first=item_text(block[0]['ws'], strip_marker=True); fn=norm(first)
        if len(fn)>=25 and not echoes(first, qn) and any(cid!=card['id'] and fn[:25] in sq for cid,sq in SIBLINGS[(card['year'],card['level'])]):
            continue
        out.append((block, bounded))
    if not out: return [], 'the marker found opens another part'
    return out, None
_by_id={}
def sub_asks(card):
    """The card's own sub-question and its siblings', as the paper words them ("(ii) State whether it is a surplus or a deficit.")."""
    info=parse_ref(card['questionRef']); own=None; others=[]
    pat=re.compile(r'\((i|ii|iii|iv|v|vi|[a-e])\)\s*(.+?)(?=\s*\((?:i|ii|iii|iv|v|vi|[a-e])\)|$)', re.S)
    def asks_of(text): return {m.group(1): ' '.join(m.group(2).split()) for m in pat.finditer(text)}
    mine=asks_of(card['questionText'])
    key=info.get('roman') or (info.get('part') or '').lower()
    own=mine.get(key)
    parent=re.sub(r'\s*\((?:i|ii|iii|iv|v|vi)\)\s*$', '', card['questionRef']) if info.get('roman') else re.sub(r'\s*\([A-Ea-e]\)\s*$', '', card['questionRef'])
    for cid,_ in SIBLINGS[(card['year'],card['level'])]:
        if cid==card['id']: continue
        sib=_by_id.get(cid)
        if not sib: continue
        sparent=re.sub(r'\s*\((?:i|ii|iii|iv|v|vi)\)\s*$', '', sib['questionRef']) if info.get('roman') else re.sub(r'\s*\([A-Ea-e]\)\s*$', '', sib['questionRef'])
        if sparent!=parent: continue
        sinfo=parse_ref(sib['questionRef']); skey=sinfo.get('roman') or (sinfo.get('part') or '').lower()
        sask=asks_of(sib['questionText']).get(skey)
        if sask and sask!=own: others.append(sask)
    return own, others
def parent_slice(card):
    """A sub-part whose marker the scheme never prints: its lines inside the parent part's block, from the line that
    echoes the card's own ask (the parent's marker for a first sub-part) to the line that echoes a sibling's."""
    info=parse_ref(card['questionRef'])
    if not info or not (info.get('roman') or info.get('part')): return None,'no parent'
    own,others=sub_asks(card)
    if not own and not others: return None,'the paper does not word the sub-questions apart'
    parent=dict(card)
    parent['questionRef']=re.sub(r'\s*\((?:i|ii|iii|iv|v|vi)\)\s*$', '', card['questionRef']) if info.get('roman') else re.sub(r'\s*\([A-Ea-e]\)\s*$', '', card['questionRef'])
    # the parent's ask is every sibling's ask together: a sibling's lead-in over the shared marker is not another part
    sibs=[_by_id[cid] for cid,_ in SIBLINGS[(card['year'],card['level'])] if cid in _by_id and cid!=card['id']
          and (re.sub(r'\s*\((?:i|ii|iii|iv|v|vi)\)\s*$', '', _by_id[cid]['questionRef']) if info.get('roman') else re.sub(r'\s*\([A-Ea-e]\)\s*$', '', _by_id[cid]['questionRef']))==parent['questionRef']]
    parent['questionText']=' '.join([card['questionText']]+[x['questionText'] for x in sibs])
    parent['id']=card['id']
    cands,why=block_candidates(parent)
    if not cands: return None, f'parent {why}'
    def echo_of(line, ask):
        if not ask: return False
        t=item_text(line['ws'], strip_marker=True); n=norm(t); a=norm(ask)
        if len(n)>=12 and (n[:20] in a or a[:20] in n): return True
        ws=re.findall(r'[a-z]{4,}', t.lower())
        return 2<=len(ws)<=4 and all(w in a for w in ws) and len(t.split())<=5
    first=(info.get('roman')=='i') or ((info.get('part') or '').upper()=='A')
    for block,bounded in cands:
        starts=[i for i,l in enumerate(block) if i>0 and echo_of(l, own) and not any(echo_of(l,o) for o in others)]
        start=starts[0] if starts else (0 if first else None)
        if start is None: continue
        end=next((j for j in range(start+1,len(block)) if any(echo_of(block[j],o) for o in others)), len(block))
        if end-start<=0: continue
        return (block[start:end], bounded), None
    return None, 'the parent block has no line echoing the sub-question'
def block_for(card):
    cands,why=block_candidates(card)
    return (cands[0][0], None) if cands else (None, why)
def item_text(ws, strip_marker=True):
    toks=[(x0,t) for x0,_,_,t in ws]
    out=[]
    skip=False
    body=sum(1 for x0,t in toks if x0<0.6 and re.search('[A-Za-z]{2}', t))
    for k,(x0,t) in enumerate(toks):
        if skip: skip=False; continue
        if x0>=0.6 and re.fullmatch(r'\d{1,2}', t) and k+1<len(toks) and re.fullmatch(r'marks?', toks[k+1][1]): skip=True; continue
        # a marking label set in the far margin beside a line of prose ("Explain", "Example", "State", "Link"): a gap, then a word or three without a digit
        if x0>=0.78 and body>=4 and k>0 and x0-ws[k-1][2]>0.04 and all(re.fullmatch(r'[A-Za-z][A-Za-z.]*', t2) for _,t2 in toks[k:]) and len(toks)-k<=3: break
        t=''.join(ch for ch in t if not (PUA.match(ch) and ch not in KEEP_PUA))   # a stray marks-column glyph, never a bullet or tick
        if not t: continue
        if x0>=0.8 and (re.fullmatch(r'\d{1,3}|x|\d+m|\(\d+\)|\d{1,2}marks?', t) or t in ('Max','mark','marks','Marks')): continue       # the marks column
        if x0>=0.6 and MARKS_TOKEN.match(t): continue                    # "(5+5)", "3+3+2+2", "10(5+5)" beside a response
        if x0>=0.78 and (t in ('+','m') or re.fullmatch(r'\(\d{1,2}m?|\d{1,2}m?\)|marks?\)?', t)): continue   # a marks cell the layer split: "(2m" "+" "2m)", "(2" "marks)"
        if re.fullmatch(r'\(\d{1,2}m?\)', t) and x0>0.35: continue        # a line price "(1)", a marks cell "(1m)"
        t=re.sub(r'^\(\d{1,2}\)(?=\S)', '', t)                           # "(1)13,600"
        if re.fullmatch(r'⟨[^⟩]*⟩', t) or re.fullmatch(r'[`´‘’"“”]+', t): continue
        out.append(t)
    text=' '.join(out)
    if strip_marker: text=re.sub(r'^(?:\d{1,2}[.)]?\s+)?(?:\(?[A-Ea-e]\)?\s+)?(?:\(?(?:i|ii|iii|iv|v|vi)\)?\s+)?', '', text, count=1)
    return repaired(text).strip()
def expected_geo(card):
    """(expected, None) or (None, reason) from the cited pages' geometry; see the stage B note above."""
    cands,why=block_candidates(card)
    if not cands or why=='the marker found opens another part':
        found,pwhy=parent_slice(card)
        if found: cands=[found]
        elif not cands: return None, f'{why}; {pwhy}'
    last=None
    for block,bounded in cands:
        found,reason=_items_of(card, block, bounded)
        if found: return found,None
        last=reason
    return None,last
def tick_table(texts, headers, all_texts=None):
    """Items of a tick table: one per tick, the statement's lines around the tick and the column its x falls under.
    The header may wrap ("Take-"/"over", "Price"/"Skimming"): its lines are joined by column. Returns None when the
    block is not such a table."""
    cols_=tick_cols(texts)
    ticks=[(l['y'], x0) for l,t in texts for x0,_,_,tok in l['ws'] if is_tick(tok, x0, l['ws'], cols_)]
    if len(ticks)<2: return None
    # the header zone: the short capitalised lines over the first statement, however the layout wrapped them
    # ("Take- Fran- Strategic" / "Statement Merger" / "over chise Alliance"); a statement is longer, or ends a sentence
    hdr=[]
    for l,t in (all_texts or texts):
        toks=t.split()
        if any(is_tick(tok, x0, l['ws'], cols_) for x0,_,_,tok in l['ws']): break
        # an ask that carries the column words after its colon ("Indicate categories: Visible Invisible …"): capitalised words, right of the colon
        colon=next((k for k,w in enumerate(l['ws']) if w[3].endswith(':')), None)
        after=[w for w in l['ws'][colon+1:] if not MARKS_TOKEN.match(w[3]) and not re.fullmatch(r'\d{1,2}m?', w[3])] if colon is not None else []
        if len(after)>=2 and after[0][0]>0.45 and all(re.fullmatch(r'[A-Z][A-Za-z-]*', w[3]) for w in after):
            hdr.append(({**l, 'ws': after}, ' '.join(w[3] for w in after))); continue
        if asks(t): continue
        if not hdr and len(toks)>5: continue
        caps=sum(1 for tok in toks if tok[:1].isupper())
        hyphenated=any(tok.endswith('-') for _,ht in hdr for tok in ht.split())
        if len(toks)<=5 and all(len(tok)<=15 for tok in toks) and not re.search(r'[.;:?]$', t) and (caps>=2 or (hyphenated and caps>=1)):
            hdr.append((l,t)); continue
        if hdr: break
    if not hdr: return None
    # the header's columns: phrases of its first line, then later header lines joined by column
    def phrases_of(l):   # (centre, x0, text, x1) of each run of words the layout set together
        out=[]; cur=[]
        for x0,y0,x1,tok in l['ws']:
            if cur and x0-cur[-1][2]>0.02: out.append(cur); cur=[]
            cur.append((x0,y0,x1,tok))
        if cur: out.append(cur)
        return [((ph[0][0]+ph[-1][2])/2, ph[0][0], ' '.join(tk for *_,tk in ph), ph[-1][2]) for ph in out]
    hy=hdr[0][0]['y']; head_lines=[hdr[0]]
    for l,t in hdr[1:]:
        if abs(l['y']-hy)>0.03: break
        head_lines.append((l,t)); hy=l['y']
    # the columns are where the ticks fall; each takes the header words set over it, line by line ("Take-"/"over")
    xs=[]
    for _,x in sorted(ticks, key=lambda t:t[1]):
        if not xs or x-xs[-1]>0.04: xs.append(x)
    cols=[]
    for cx in xs:
        label=''
        for l,t in head_lines:
            near=[w for w in l['ws'] if abs((w[0]+w[2])/2-cx)<0.035 and re.search('[A-Za-z]', w[3]) and not BARE_MARKER.match(w[3])]
            if not near: continue
            ph=next((ph for ph in phrases_of(l) if ph[1]<=near[0][0]<=ph[3]), None)
            # the phrase is one column's label only if no other tick column runs through it ("Visible Invisible" over two columns)
            words=ph[2].split() if ph and ph[3]-ph[1]<=0.12 and not any(ph[1]<=x<=ph[3] for x in xs if abs(x-cx)>0.02) else [min(near, key=lambda w: abs((w[0]+w[2])/2-cx))[3]]
            words=[tok for tok in words if not BARE_MARKER.match(tok)]
            if words: label=(label.rstrip('-')+' '.join(words)) if label.endswith('-') else (label+' '+' '.join(words)).strip()
        if label: cols.append((cx,label))
    if len(cols)<2: return None
    # statement lines: text after the header, words left of the ticks
    body=[(l,t) for l,t in texts if id(l) not in headers and l['y']>hy]
    tick_ys=sorted(y for y,_ in ticks)
    # a statement runs to its full stop; the ticks say which statement a group of lines belongs to
    runs=[]; cur=[]
    for l,t in body:
        words=[tok for x0,_,_,tok in l['ws'] if not is_tick(tok, x0, l['ws'], cols_) and x0<0.6 and not MARKS_TOKEN.match(tok)]
        if cur and words and re.match(r'^\(?(?:i|ii|iii|iv|v|vi)\)$', words[0]): runs.append(cur); cur=[]   # "(ii) Debate and approve…" starts its own statement
        cur.append((l,words))
        if re.search(r'[.?!]$', ' '.join(words)): runs.append(cur); cur=[]
    if cur: runs.append(cur)
    def ticks_in(run):
        y0=run[0][0]['y']-0.004; y1=run[-1][0]['y']+0.004
        return [(y,x) for y,x in ticks if y0<=y<=y1]
    split=[]
    for run in runs:
        inside=sorted(ticks_in(run))
        while len(inside)>=2:
            # the second tick's statement starts at the first capitalised line nearer to it than to the first tick,
            # else at the wordy line nearest it
            wordy=[i for i in range(1,len(run)) if run[i][1]]
            starts=[i for i in wordy if (run[i][1][0][:1].isupper() or re.match(r'^\(?(?:i|ii|iii|iv|v|vi)\)$', run[i][1][0])) and abs(run[i][0]['y']-inside[1][0])<abs(run[i][0]['y']-inside[0][0])]
            cut=starts[0] if starts else (min(wordy, key=lambda i: abs(run[i][0]['y']-inside[1][0])) if wordy else None)
            if cut is None: break
            split.append(run[:cut]); run=run[cut:]; inside=sorted(ticks_in(run))
        split.append(run)
    items=[]; pending=[]
    for run in split:
        inside=ticks_in(run)
        if not inside: pending.extend(run); continue   # a header-less fragment joins the statement after it
        run=pending+run; pending=[]
        x=sorted(inside)[0][1]; pick=min(cols, key=lambda c: abs(c[0]-x))[1]
        text=' '.join(' '.join(words) for _,words in run if words).strip()
        if text: items.append({'text': repaired(f"{text} — {pick}"), 'detail': [], 'geo': 'tick'})
    return items if len(items)>=2 else None
def _items_of(card, block, bounded):
    """(expected, None) or (None, reason) for one block's lines."""
    page=block[0]['p']
    info=parse_ref(card['questionRef'])
    mi=next((i for i,l in enumerate(block[:2]) if marker_kind(l['ws'], info)), 0)
    start_mk=marker_kind(block[mi]['ws'], info)
    # a marks column inside a table: bare one- or two-digit integers ending three or more lines at one x right of 0.6
    lasts=[l['ws'][-1] for l in block if len(l['ws'])>1 and l['ws'][-1][0]>=0.6 and re.fullmatch(r'\d{1,2}', l['ws'][-1][3])]
    mark_x=[x for x,n in collections.Counter(round(w[0],2) for w in lasts).items() if n>=3]
    if mark_x: block=[{**l, 'ws':[w for w in l['ws'] if not (re.fullmatch(r'\d{1,2}', w[3]) and any(abs(w[0]-x)<=0.02 for x in mark_x))]} for l in block]
    texts=[]
    for i,l in enumerate(block):
        if not l['ws']: continue   # a line that was only its marks figure
        mk_=marker_kind(l['ws'], info)
        own=bool(mk_) and ((mk_[0]=='part' and str(mk_[1]).upper()==str(info.get('part') or '').upper() and mk_[2] in (None, info['q'])) or (mk_[0]=='q' and mk_[1]==info['q']))
        t=item_text(l['ws'], strip_marker=(i==mi or own or same_marker(mk_, start_mk)))
        if not t or TABLEHEAD.match(t) or CTD.match(t) or BARE_MARKER.match(t) or re.fullmatch(r'(?:\d{1,2}m for [A-Za-z ]+\.?\s*)+', t) or re.fullmatch(r'(?:€\s*)+', t) or re.fullmatch(r'NOTE:?', t) or re.match(r'^Own [Ff]igures\b', t) or re.match(r'^Must (?:have|show)\b', t) or re.search(r'\bonly other figure accepted\b', t, re.I) or (re.fullmatch(r'\d{1,2}(?: \d{1,2})*', t) and t.split()!=[str(n) for n in range(1,len(t.split())+1)]) or re.fullmatch(r'(?:END|Blank Page)', t) or (re.fullmatch(r'(?:19|20)\d{2}', t) and l['y']>0.85) or (all(x0>=0.75 for x0,*_ in l['ws']) and len(t.split())<=6 and (len(t.split())>=3 or all(x0>=0.8 for x0,*_ in l['ws'])) and not re.search(r'\d', t) and not any(tok in TICK for *_,tok in l['ws'])) or re.match(r'^Question\s+Possible\s+Response', t) or re.fullmatch(r'\(?(?:i|ii|iii|iv|v|vi|[A-E])\)?', t) or re.match(r'^(?:Sample|Possible) responses?\b.{0,20}\binclude', t, re.I): continue
        texts.append((l,t))
    cols_=tick_cols(texts)
    ticked=any(is_tick(tok, x0, l['ws'], cols_) for l,t in texts for x0,_,_,tok in l['ws'])
    first_tick_y=min([l['y'] for l,t in texts if any(is_tick(tok, x0, l['ws'], cols_) for x0,_,_,tok in l['ws'])] or [0])
    def is_header(l,t):
        toks=[tok for *_,tok in l['ws']]
        # a column header sits to the right; a tick table's may start at the statement column ("Statement Land Labour Capital Enterprise"),
        # but only above the first tick: a statement naming "Avonmore Foods plc and Waterford Foods" is not a header
        return ' / ' not in t and len(toks)>=2 and all(len(tok)<=15 for tok in toks) and not re.search(r'[.;:]$', t) and sum(1 for tok in toks if tok[:1].isupper())>=2 and (l['ws'][0][0]>0.3 or (ticked and l['y']<first_tick_y and len(toks)>=4 and sum(1 for tok in toks if tok[:1].isupper())>=4 and l['ws'][0][0]>0.15)) and not any(tok in TICK for tok in toks)
    headers={id(l) for l,t in texts if is_header(l,t)} if ticked else set()
    all_texts=list(texts)
    qn=norm(card['questionText'])
    popped=0
    def gapped(l):   # phrases on the line, split where the layout left a gap: a header line has several; the marker's own tokens are not phrases
        ws=[w for w in l['ws'] if not re.fullmatch(r'\(?(?:\d{1,2}|[A-Ea-e]|i{1,3}|iv|vi?)[.)]?', w[3])]
        n=1
        for a,b in zip(ws, ws[1:]):
            if b[0]-a[2]>0.02 and re.search('[A-Za-z]', b[3]): n+=1
        return n
    def inline_answer(t):
        # the ask with its answer on the same line: "State whether it is a surplus or deficit: Surplus", "Name one leadership style. Autocratic/Democratic/Laissez Faire"
        tail=re.search(r'^(.{12,}?[:.])\s*([^:]{1,40})$', t)
        if tail and len(tail.group(2).split())<=3 and asks(tail.group(1)) and not asks(tail.group(2)+'.') and tail.group(2).count('(')==tail.group(2).count(')') and tail.group(2).split()[-1].lower() not in ASK_TAIL: return tail.group(2)
        return None
    def answers_inline(t): return inline_answer(t) is not None
    def asks_wrapped(k):
        t=item_text(texts[k][0]['ws'], strip_marker=True)
        if answers_inline(t): return 0
        if asks(t): return 1
        if k+1<len(texts):
            nxt=texts[k+1][1]
            if nxt[:1].islower() and (asks((t+' '+nxt).rstrip()+'.') or asks(t.rstrip()+'.')): return 2
            # the ask's last words on a line of their own ("…affecting this sector in" / "Ireland.", "…extend a Product Life" / "Cycle."):
            # a short capitalised tail, after a line cut mid-phrase or whose tail the question itself prints
            if len(nxt.split())<=3 and re.search(r'[.?:]$', nxt) and not re.search(r'[.?!:]$', t) and asks(t+' '+nxt) \
                    and (t.split()[-1].lower().strip('‘’\'"') in ASK_TAIL or norm(nxt) in qn): return 2
        # the ask printed without its full stop ("Calculate the Profit at Forecast Output"): an imperative sharing its words with the question
        if not re.search(r'[.?!:]$', t) and len(t.split())<=12 and asks(t.rstrip()+'.') and len({w for w in re.findall(r'[a-z]{4,}', t.lower()) if w in qn})>=2: return 1
        return 0
    def offered(text):
        ql=card['questionText'].lower(); t=text.strip().rstrip('.,:')
        if asks(text) or not t: return False
        if '/' in t:   # "Saturation / Decline": each a word (or two) naming a stage the ask lists
            parts=[w.strip().lower() for w in t.split('/') if w.strip()]
            return 1<len(parts)<=4 and all(re.fullmatch(r'[a-z-]+(?: [a-z-]+)?', w) and re.search(r'\b'+re.escape(w)+r'\b', ql) for w in parts)
        if len(t.split())>2: return False
        w=re.escape(t.lower())
        return bool(re.search(r'\b'+w+r'\b[^.?]{0,24}\bor\b|\bor\b[^.?]{0,24}\b'+w+r'\b', ql))
    pair_words={'true','false'}|{w.lower() for m in re.finditer(r'(?:writ(?:e|ing)|plac(?:e|ing)|stat(?:e|ing)|indicat(?:e|ing))[^.?]{0,40}?\b([A-Z][a-z]+|[A-Z]{3,})\b\s+(?:[A-Za-z]+\s+)?or\s+\b([A-Z][a-z]+|[A-Z]{3,})\b', card['questionText']) for w in m.groups()}
    cap=1 if any(tok.rstrip('.').lower() in pair_words and x0>0.65 for l,t in texts for x0,_,_,tok in l['ws']) else 2
    cloze_q='___' in card['questionText'] or bool(re.search(r'\bcircle\b', card['questionText'], re.I))   # a cloze, or a circled option: the echoed sentences are the answers' lines
    cloze=lambda t: any(w not in card['questionText'] for w in re.findall(r'\b[A-Z]{4,}\b', t))   # a filled blank is capitalised; an acronym the ask prints is not
    while texts and popped<cap and id(texts[0][0]) not in headers and not cloze(texts[0][1]) and not offered(texts[0][1]) and not answers_inline(texts[0][1]) and ' / ' not in texts[0][1] and ((echoes(texts[0][1], qn) and not cloze_q and len(norm(texts[0][1]))>=12 and (len(texts[0][1].split())>=(5 if popped==0 else 8) or re.search(r'[.?!:;]$', texts[0][1]) or re.search(r'\d{2}', texts[0][1]) or gapped(texts[0][0])>=3 or (len(texts)>1 and texts[1][1][:1].islower()))) or asks_wrapped(0)):
        n=asks_wrapped(0) or 1
        echo=texts.pop(0)[1]; popped+=1
        for _ in range(n-1): echo=texts.pop(0)[1]
        while texts and not re.search(r'[.?!:]$', echo) and not re.match(r'^(?:i|ii|iii|iv|v|vi)[.)]\s', texts[0][1]) and ' / ' not in texts[0][1] and (texts[0][1][:1].islower() or (len(texts[0][1].split())<=3 and asks(echo+' '+texts[0][1])) or (echo.rstrip().endswith(('”','"')) and echoes(texts[0][1], qn) and len(texts[0][1].split())<=6) or (echoes(texts[0][1], qn) and not re.match(r'^\w+:', echo) and asks((echo+' '+texts[0][1]).rstrip('.')+'.'))): echo=texts.pop(0)[1]
    while texts and id(texts[0][0]) not in headers and re.match(r'^\(.*\)\.?$', texts[0][1]) and len(norm(texts[0][1]))>=15 and norm(texts[0][1]) in qn: texts.pop(0)
    if not texts: return None,'no response under the marker'
    ringed={}
    if re.search(r'\bcircle\b', card['questionText'], re.I):
        try:
            pg_=doc(card['year'], card['rubric']['schemeFileid'])[page-1]; W_,H_=pg_.rect.width,pg_.rect.height
            rings=[d['rect'] for d in pg_.get_drawings() if d.get('rect') is not None and 15<=d['rect'].width<=200 and 8<=d['rect'].height<=45 and any(it[0]=='c' for it in d.get('items',[]))]
            page_lines=[l for l,t in texts if l['p']==page]
            for r in rings:
                # a ring taller than a line overlaps the line above too: the words ringed are on the line its centre sits on
                cy=(r.y0+r.y1)/2/H_
                near=[l for l in page_lines if r.y0/H_-0.012<=l['y']<=r.y1/H_ and any(r.x0/W_-0.004<=x0 and x1<=r.x1/W_+0.004 for x0,_,x1,_ in l['ws'])]
                if not near: continue
                l=min(near, key=lambda l: abs(l['y']+0.006-cy))
                inside=[tok for x0,y0,x1,tok in l['ws'] if r.x0/W_-0.004<=x0 and x1<=r.x1/W_+0.004]
                while inside and inside[-1].lower().rstrip('.,') in ('in','a','an','the','of','to'): inside.pop()
                inside=[tok for tok in inside if tok not in ('/',) and not MARKS_TOKEN.match(tok)]
                if inside: ringed[id(l)]=repaired((ringed.get(id(l),'')+' '+' '.join(inside)).strip())
        except Exception:
            ringed={}
    items=[]
    header=None
    pending_numbers=None
    table=tick_table(texts, headers, all_texts)
    if table: items=table; texts=[]
    for l,t in texts:
        if inline_answer(t): t=inline_answer(t)
        toks=[tok for x0,_,_,tok in l['ws'] if not (x0>=0.6 and MARKS_TOKEN.match(tok))]
        # a TRUE/FALSE answer at the right of a statement, on its line or the line after
        tf=[(x0,tok) for x0,_,_,tok in l['ws'] if tok.rstrip('.').lower() in pair_words and x0>0.65]
        if tf:
            stmt=' '.join(tok for x0,_,_,tok in l['ws'] if x0<=0.65)
            if stmt.strip():
                # the statement's first line sits above the line that carries its answer
                if items and not items[-1].get('geo') and ' — ' not in items[-1]['text'] and items[-1]['text']!=BOUNDARY and not re.search(r'[.?!:]$', items[-1]['text']):
                    stmt=items.pop()['text']+' '+stmt
                items.append({'text': f"{stmt.strip()} — {tf[0][1].rstrip('.')}", 'detail': [], 'geo': 'tf'})
            elif items and ' — ' not in items[-1]['text'] and items[-1].get('geo') is None:
                items[-1]['text']+=f" — {tf[0][1].rstrip('.')}"; items[-1]['geo']='tf'
            else:
                items.append({'text': tf[0][1].rstrip('.'), 'detail': [], 'geo': 'tf-pending'})
            continue
        if items and items[-1].get('geo')=='tf-pending':
            items[-1]={'text': f"{t} — {items[-1]['text']}", 'detail': [], 'geo': 'tf'}; continue
        if items and items[-1].get('geo')=='tf' and (t[:1].islower() or not re.search(r'[.?!:]$', items[-1]['text'].rsplit(' — ',1)[0])) and not re.match(r'^\(?(?:i|ii|iii|iv|v|vi|\d{1,2})[.)]?\s', t):
            stmt,ans=items[-1]['text'].rsplit(' — ',1); items[-1]['text']=f"{stmt} {t} — {ans}"; continue
        # a matching grid: a line of numbers "1. 2. 3." over a line of letters "D A E"
        if len(toks)>=3 and all(re.fullmatch(r'\d{1,2}\.?', tok) for tok in toks):
            pending_numbers=[(x0,tok.rstrip('.')) for x0,_,_,tok in l['ws']]; continue
        if pending_numbers and len(toks)==len(pending_numbers) and all(re.fullmatch(r'[A-H]', tok) for tok in toks):
            if items and items[-1].get('geo') is None and items[-1]['text']!=BOUNDARY and len(items[-1]['text'].split())<=4 and not re.search(r'[.?!:]$', items[-1]['text']): items.pop()   # the grid's header line
            for (x0,n),(x1,_,_,letter) in zip(pending_numbers, l['ws']): items.append({'text': f"{n} — {letter}", 'detail': [], 'geo': 'table'})
            pending_numbers=None; continue
        pending_numbers=None
        ticks=[x0 for x0,_,_,tok in l['ws'] if is_tick(tok, x0, l['ws'], cols_)]
        words=[(x0,tok) for x0,_,_,tok in l['ws'] if not is_tick(tok, x0, l['ws'], cols_)]
        if ticks and not words and header is None:
            items.append({'text': '✓', 'detail': [], 'geo': 'lone-tick', 'y': l['y']}); continue
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
        if id(l) in ringed:
            # a statement wrapped over lines: the ring sits on one of them
            if items and (items[-1].get('geo')=='circled-wait' or (items[-1].get('geo') is None and items[-1]['text']!=BOUNDARY and not re.search(r'[.?!:]$', items[-1]['text']))): stmt=items.pop()['text']+' '+t
            else: stmt=t
            items.append({'text': f"{stmt.strip()} — {ringed[id(l)]}", 'detail': [], 'geo': 'circled'}); continue
        if ringed and items and items[-1].get('geo')=='circled' and t[:1].islower():
            stmt,ans=items[-1]['text'].rsplit(' — ',1); items[-1]['text']=f"{stmt} {t} — {ans}"; continue
        if ringed and not re.search(r'[.?!]$', t) and ' / ' in t:
            items.append({'text': t, 'detail': [], 'geo': 'circled-wait'}); continue
        if re.match(r'^(?:i|ii|iii|iv|v|vi)[.)]\s', t): items.append({'text': t, 'detail': [], 'geo': 'table'}); continue
        if asks(t) or asks(item_text(l['ws'], strip_marker=True)): items.append({'text': BOUNDARY, 'detail': []}); continue
        figs=sum(1 for tok in t.split() if re.fullmatch(r'[€(]?\d[\d,.·]*(?:[x×]\d[\d,.·]*)?%?\)?[◆•❶-❿*]?|\(\d[\d,.]*[-–]\d[\d,.]*\)[◆•❶-❿*]?', tok) and len(re.sub(r'\D','',tok))>=2)
        last_fig=bool(re.fullmatch(r'[€(]?\d[\d,.·]*%?\)?[◆•❶-❿*]?', toks[-1])) if toks else False
        if figs>=1 and len(l['ws'])<=9 and (figs>=2 or len(l['ws'])<=5 or last_fig or re.search(r'[=:%€]', t)) and not (t[:1].islower() and re.search(r'[.?!]["”’]?$', t)): items.append({'text': t, 'detail': [], 'geo': 'table', 'y': l['y']}); continue
        if t.strip(): items.append({'text': t, 'detail': [], 'y': l['y']})
    # a drawn answer: a chart or graph plotted on the page (small drawn glyphs, few printed lines) is not a list of rows
    try:
        pg=doc(card['year'], card['rubric']['schemeFileid'])[page-1]
        glyphs=sum(1 for d in pg.get_drawings() if d.get('rect') is not None and 3<d['rect'].width<20 and 3<d['rect'].height<20)
    except Exception:
        glyphs=0
    texty=[it for it in items if it.get('geo') not in ('header',) and it['text']!=BOUNDARY and (sum(ch.isalpha() for ch in it['text'])>=8 or ' — ' in it['text'] or sum(ch.isdigit() for ch in it['text'])>=3)]
    if glyphs>=5 and len(texty)<3: return None, 'the answer is a drawing: a chart or graph plotted on the page'
    try:
        H=pg.rect.height; ys=[l['y'] for l in block]
        imaged=any(r.y1/H>=min(ys) and r.y0/H<=max(ys)+0.05 and r.height>40 for r in pg.get_image_rects(pg.get_images()[0][0])) if pg.get_images() else False
        if pg.get_images() and not imaged:
            imaged=any(r.y1/H>=min(ys) and r.y0/H<=max(ys)+0.05 and r.height>40 for img in pg.get_images() for r in pg.get_image_rects(img[0]))
    except Exception:
        imaged=False
    if imaged and len(texty)<3: return None, 'the answer is an image on the page'
    if header is not None and any(is_tick(tok, x0, l['ws'], cols_) for l,t in texts for x0,_,_,tok in l['ws']) and not any(it.get('geo')=='tick' for it in items): return None, 'a tick table the geometry did not read'
    if re.search(r'\bcircle\b', card['questionText'], re.I) and sum(1 for l,t in texts if ' / ' in t)>=2 and not any(it.get('geo')=='circled' for it in items): return None, 'the answer is a circle the scheme drew around a printed option'
    if header is not None and not any(it.get('geo')=='tick' for it in items):
        items=[it for it in items if it.get('geo')!='header']   # a header line with no ticks under it was just a line of short words
    # join continuation lines and split bulleted items as stage A does; tick rows stay whole
    # a tick on a line of its own ticks the statement nearest it
    lone=[it for it in items if it.get('geo')=='lone-tick']
    if lone:
        others=[(k,it) for k,it in enumerate(items) if it.get('geo') in (None,'table') and it['text']!=BOUNDARY and 'y' in it]
        for tk in lone:
            near=min(others, key=lambda ki: abs(ki[1]['y']-tk['y']), default=None)
            if near and not near[1]['text'].startswith('✓'): near[1]['text']='✓ '+near[1]['text']
        items=[it for it in items if it.get('geo')!='lone-tick']
        items=[it for it in items if not (it.get('geo') is None and it['text']!=BOUNDARY and not it['text'].startswith('✓') and len(norm(it['text']))>=8 and norm(it['text']) in qn)]
    out=[]; run=[]
    def flush_run():
        for o in split_items(run):
            if o['text'].strip() and o['text']!=BOUNDARY: out.append({k:v for k,v in o.items() if k not in ('id','y')})
        run.clear()
    for it in items:
        if it.get('geo')=='header': continue
        if it.get('geo')=='circled-wait': it['geo']=None
        if it.get('geo') in ('table','tick','tf','circled'):
            flush_run(); out.append({'text': it['text'], 'geo': it['geo']})
        else: run.append(it['text'])
    flush_run()
    # a marks cell printed as a line, and a fragment the page break left mid-sentence at the top, are not responses
    out=[o for o in out if not re.fullmatch(r'\(\d{1,3}\s*marks?\)', o['text'].strip()) and re.search(r'[A-Za-z0-9]', o['text'])]
    out=[o for k,o in enumerate(out) if not (k>0 and out[k-1].get('geo')=='table' and not o.get('geo') and o['text'][:1].islower() and len(o['text'].split())<=5 and not re.search(r'\d', o['text']))]
    fragments=0
    while out and fragments<2 and not out[0].get('geo') and out[0]['text'][:1].islower() and not re.match(r'^(?:i|ii|iii|iv|v|vi|\d{1,2})[.)]\s', out[0]['text']): out.pop(0); fragments+=1
    out=[{k:v for k,v in o.items() if k!='geo'} for o in out]
    if len(out)==1 and len(texts)==1:
        ws=texts[0][0]['ws']; phrases=[]; cur=[]
        for x0,y0,x1,tok in ws:
            if cur and x0-cur[-1][2]>0.03: phrases.append(cur); cur=[]
            cur.append((x0,y0,x1,tok))
        if cur: phrases.append(cur)
        parts=[item_text(ph, strip_marker=True) for ph in phrases]; parts=[t for t in parts if t and not BARE_MARKER.match(t)]
        if len(parts)>=2 and all(len(t.split())>=2 and re.search(r'[A-Za-z]{3}', t) for t in parts) and not any(re.search(r'[.;:=]$', t) or re.fullmatch(r'[\d€,.()\s-]+', t) for t in parts): out=[{'text': t} for t in parts]
    out=[{'id':f'e{n}', **{k:v for k,v in o.items() if k!='id'}} for n,o in enumerate(out,1)]
    joined=' '.join(o['text']+' '+' '.join(o.get('detail',[])) for o in out)
    letters=sum(ch.isalpha() for ch in joined); digits=sum(ch.isdigit() for ch in joined)
    pairs=sum(1 for o in out if ' — ' in o['text'])
    if not out or (letters<10 and digits<6 and pairs<3 and not (len(out)<=2 and (digits>=1 or letters>=2))): return None,'no readable response'
    # a page whose text layer dropped or shifted letters ("xplain", "Wz") is not readable either
    if MANGLED.search(joined) or re.search(r'\bxplain|:ob|Wz|h\^|\b[A-Za-z]*[\^|]\w', joined): return None,'text layer glyph damage on the page'
    if len(joined)>(MAX_BLOCK if not bounded else 12000): return None,'block over 3000 characters' if not bounded else 'block over 12000 characters'
    # every word of every item is a word the page prints
    # every word of every item is a word the scheme's text layer prints, as the gate reads it (page_text)
    corpus=page_text(card['year'], card['level'])
    for o in out:
        for piece in [o['text'], *o.get('detail', [])]:
            for wd in piece.replace('—',' ').split():
                w=norm(wd)
                if w and w not in corpus and w not in _page_text[(card['year'], card['level'], 'raw')] \
                        and not any(w[:i] in corpus and w[i:] in corpus for i in range(3, len(w)-2)):   # a column label the layout hyphenated ("Take-"/"over")
                    return None, f'word not in the scheme text: {wd}'
    return {'page':page,'items':out,'lifted':'geometry'}, None


SLICES=os.path.join(ROOT, 'scripts/markbank/authored/business-expected-slices.json')
def expected_slice(card):
    """(expected, None) or (None, reason) from a hand-checked slice of a cited page (business-expected-slices.json).

    A slice names the page region(s) the scheme printed a part's responses in when no marker or echo could
    say so: a ratio's rows on a shared baseline, an answer box beside a chart, a sub-part whose marker the
    scheme never printed. The words are the page's own, read as a marker's block is; the slice only says
    where. An entry marked excluded records why the page holds nothing to lift (an image, a drawn chart)."""
    if not os.path.exists(SLICES): return None,'no slice'
    spec=json.load(open(SLICES, encoding='utf-8')).get(card['id'])
    if not spec: return None,'no slice'
    if spec.get('excluded'): return None, f"excluded: {spec['why']}"
    fid=card['rubric']['schemeFileid']; block=[]
    for region in spec['regions']:
        p=region['page']; y0,y1=region['y']; x0,x1=region.get('x',[0,1])
        for l in lines_of(card['year'],fid,p):
            if not (y0<=l['y']<=y1 and x0<=l['x']<=x1): continue
            if any(item_text(l['ws'], strip_marker=False).startswith(sk) for sk in spec.get('skip', [])): continue   # a marking note the slice names
            ws=[w for w in l['ws'] if w[0]>=region.get('xmin',0)]
            if ws: block.append({**l, 'ws':ws})
    if not block: return None,'the slice holds no lines'
    if spec.get('mode')=='labels':
        # the marks column's own labels, wrapped word by word: one item per label ("Labels: Year No.empl")
        toks=[repaired(tok) for l in block for *_,tok in l['ws']]
        toks=[t for t in toks if not re.fullmatch(r'\d{1,2}|\d{1,2}\s*x\s*\d{1,2}m?|x|\d{1,2}m|[+=]', t)]
        joined=' '.join(toks)
        cuts=[]
        for label in spec['labels']:   # each label is the page's own words; the slice says where one label ends and the next begins
            at=joined.find(label, cuts[-1]+1 if cuts else 0)
            if at<0: return None, f'label not on the page: {label}'
            cuts.append(at)
        parts=[joined[a:b].strip() for a,b in zip(cuts, cuts[1:]+[len(joined)])]
        items=[{'id':f'e{n}','text':t} for n,t in enumerate(parts,1) if t.strip()]
        return {'page':block[0]['p'],'items':items,'lifted':'slice'}, None
    out,reason=_items_of(card, block, True)
    if not out: return None, reason
    return {**out, 'lifted':'slice'}, None
def main():
    with open(AUTHORED, encoding='utf-8') as fh:
        data = json.load(fh)
    review = []
    lifted = 0
    for card in data['cards']:
        SIBLINGS[(card['year'], card['level'])].append((card['id'], norm(card['questionText'])))
        _by_id[card['id']] = card   # parent_slice reads a sub-part's siblings by id
    geometry = 0
    sliced = 0
    for card in data['cards']:
        expected, why = expected_for(card)
        card['rubric'].pop('expected', None)
        if not expected:
            sl, sl_why = expected_slice(card)
            if sl:
                expected = sl
                sliced += 1
            elif sl_why != 'no slice':
                why = f'{why}; slice: {sl_why}'
            else:
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
    print(f'{geometry} of them from the page geometry, {sliced} from a hand-checked slice', file=sys.stderr)
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
