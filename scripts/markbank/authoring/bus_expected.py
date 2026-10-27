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


def main():
    with open(AUTHORED, encoding='utf-8') as fh:
        data = json.load(fh)
    review = []
    lifted = 0
    for card in data['cards']:
        expected, why = expected_for(card)
        card['rubric'].pop('expected', None)
        if expected:
            card['rubric']['expected'] = expected
            lifted += 1
        else:
            review.append({'id': card['id'], 'questionRef': card['questionRef'], 'schemePages': card['rubric']['schemePages'], 'reason': why})
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
