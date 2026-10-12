"""Lift French SEC wording from the printed page, never from a typed copy.

Every string a card shows under the SEC's name comes from here. A typed or
parsed string is only a locator: it finds its span on the page, and the card
shows the page's own characters for that span. Matching ignores what the text
layer cannot reproduce reliably (whitespace, punctuation, dot leaders, list
markers, letter case); the returned text keeps everything the page prints.

Display normalisation is limited to the text layer itself:
- Symbol-font glyphs that have no portable character are mapped to the glyph
  the page shows (a bullet, a tick, a dash, an asterisk);
- whitespace is collapsed, a word broken at a printed hyphen across two lines
  is rejoined, and a superscript ordinal split from its number ("4 th") is
  rejoined;
- the dot leader between an answer and its marks is shown as " — ".
"""
from functools import lru_cache
from pathlib import Path
import re

import fitz

# Symbol/Wingdings private-use glyphs as the page draws them.
GLYPHS = {
    '': '•',   # Symbol bullet
    '': '•',   # Wingdings square bullet
    '': '✓',   # Wingdings tick
    '': '-',   # Symbol minus, used as the printed answer dash
    '': '*',   # Symbol asterisk, the older partial-credit mark
    '': '➢',   # Wingdings arrowhead marker
}
MARKER = r'[•●▪■\-–−*∗➢]'
# "5 Mar": the 2025 Ordinary scheme (p.19) prints its Fish tariff cut short.
MARKS = r'\d+(?:\s*\+\s*\d+)?\s*[Mm]ar(?:ks?)?\b'
# The only printed aside between an answer and its marks: which option it is.
OPTION = r'\s*\([^()]*\b(?:options?|answers?|réponse)\)'
# A dot leader as the schemes set it: two or more dots or ellipses run on
# from the answer, or dots set off by a space ("l'anglais . 5 Marks"). A
# single stop or ellipsis on the answer's last word is the answer's own.
LEADER = r'\s*[.…]{2,}[. …]*\s*|\s+[.…][. …]*\s*'


def clean(text):
    for glyph, char in GLYPHS.items():
        text = text.replace(glyph, char)
    text = re.sub(r'(\w[‐-])[ \t]*\n\s*(?=\w)', r'\1', text)   # printed hyphen at a line break
    text = re.sub(r'_{3,}', ' ', text)                              # printed answer lines
    text = ' '.join(text.split()).replace('(✓ )', '(✓)')          # the tick glyph's own advance
    return re.sub(r'(\d) (st|nd|rd|th)\b', r'\1\2', text)


@lru_cache(maxsize=None)
def _doc(path):
    return fitz.open(path)


# Pages whose text layer repeats glyphs across clipping tiles; their words are
# rebuilt from glyph coordinates (fr_pdf_words) and offered as a reading order.
TILED = {('2011-ol-000-paper.pdf', 2), ('2011-ol-000-paper.pdf', 4), ('2011-ol-000-paper.pdf', 6),
         ('2011-ol-000-paper.pdf', 8), ('2011-hl-000-paper.pdf', 10), ('2011-hl-000-paper.pdf', 12)}


@lru_cache(maxsize=None)
def page_texts(path, page, aliases=()):
    """The page's text in each reading order the layer offers, cleaned.

    `aliases` are reviewed bullet glyphs (e.g. the 2014 Higher scheme's "x")
    that the page draws as a bullet."""
    pg = _doc(str(path))[page - 1]
    w, h = pg.rect.width, pg.rect.height
    raw = [pg.get_text(), pg.get_text(sort=True),
           pg.get_text(clip=fitz.Rect(w / 2, 0, w, h)), pg.get_text(clip=fitz.Rect(w / 2, 0, w, h), sort=True)]
    if (Path(path).name, page) in TILED:
        from fr_pdf_words import fragmented_words
        raw.append(' '.join(word[4] for word in fragmented_words(pg)))
    else:
        raw.append('')
    out = []
    for text in raw:
        for glyph in aliases:
            text = re.sub(rf'(?m)^(\s*){re.escape(glyph)}(?=\s)', r'\1•', text)
        out.append(clean(text))
    return tuple(out)


@lru_cache(maxsize=4096)
def skeleton(text):
    chars, index = [], []
    for i, ch in enumerate(text):
        if ch.isalnum():
            chars.append(ch.lower())
            index.append(i)
    return ''.join(chars), tuple(index)


def display(span):
    """The printed span as shown: the leader before a mark figure becomes " — "."""
    return re.sub(rf'(?:{LEADER})(?={MARKS})', ' — ', span).strip()


def _spans(text, typed, marks=None):
    """Every printed span of `text` that `typed` locates."""
    body = typed
    if marks is None:
        found = re.search(rf'(?:\s—\s|\s=\s|\s)({MARKS})\.?$', typed)
        if found:
            body, marks = typed[:found.start()], found[1]
    target, _ = skeleton(re.sub(rf'^{MARKER}\s*', '', body))
    if not target:
        return []
    skel, index = skeleton(text)
    spans = []
    start = skel.find(target)
    while start >= 0:
        a, b = index[start], index[start + len(target) - 1] + 1
        if (a == 0 or not text[a - 1].isalnum()) and (b == len(text) or not text[b].isalnum()):
            # Printed punctuation that opens or closes the located words.
            while a > 0 and (text[a - 1] in '(«“‘[€$£¿¡' or (text[a - 2:a] == '« ')):
                a -= 2 if text[a - 2:a] == '« ' else 1
            # French sets ? ! : ; » € % apart with a space, and the scheme
            # prints signs alone in brackets ("80 (%)", "(?)").
            spaced = '?!:;»%' + ('.' if re.search(r'\s\.$', body.rstrip()) else '')
            tail = re.match(rf'(?:\s?[{re.escape(spaced)}]|\s?€(?!\s?\d)|\s?\([^\w()]*\)|[^\w\s(«“‘\[€$£])+', text[b:])
            if tail:
                # Closing punctuation as printed, stopping where a dot leader
                # starts. A stop the leader runs straight on from ("10 a.m……")
                # stays with the word when the locator ends with it.
                kept = re.match(r'(.*?)(?:[.…]{2,}.*)?$', tail[0])[1]
                if not kept and tail[0].startswith('.') and body.rstrip().endswith('.'):
                    kept = '.'
                b += len(kept)
            if marks:
                number = re.match(r'\d+(?:\s*\+\s*\d+)?', marks)[0].replace(' ', '')
                ext = re.match(rf'((?:{OPTION})?)([. …]*|\s*=\s*)({MARKS})\.?', text[b:])
                if not ext or re.match(r'\d+(?:\s*\+\s*\d+)?', ext[3])[0].replace(' ', '') != number:
                    start = skel.find(target, start + 1)
                    continue
                b += ext.end()
            marker = re.search(rf'(?:^|\s)({MARKER})\s*$', text[:a])
            shown = (marker[1] + ' ' if marker else '') + display(text[a:b])
            spans.append(shown)
        start = skel.find(target, start + 1)
    return spans


def lift(groups, typed, marks=None, what=''):
    """The one printed form of `typed`.

    `groups` holds the candidate pages once per reading order, best first; the
    first order that locates the words decides (the sorted order, for example,
    lifts a superscript ordinal off its number)."""
    for texts in groups:
        shown = []
        for text in texts:
            shown += _spans(text, typed, marks)
        unique = list(dict.fromkeys(shown))
        if len(unique) > 1:
            # The same words printed twice, once as a marked answer line and
            # once inside other text: keep the reading the locator names.
            marked = bool(re.match(rf'{MARKER}\s*\S', typed))
            same = [s for s in unique if bool(re.match(rf'{MARKER}\s', s)) == marked]
            unique = same or unique
        if len(unique) > 1:
            exact = [s for s in unique if re.sub(rf'^{MARKER}\s+', '', s) == re.sub(rf'^{MARKER}\s+', '', typed)]
            unique = exact or unique
        if unique:
            assert len(unique) == 1, (what, typed, unique)
            return unique[0]
    raise AssertionError((what, typed, 'not printed on the cited pages'))


def try_lift(texts, typed, marks=None):
    try:
        return lift(texts, typed, marks)
    except AssertionError:
        return None


def doc_texts(path, pages, aliases=()):
    """The cited pages grouped by reading order, best order first."""
    texts = [page_texts(str(path), p, tuple(aliases)) for p in pages]
    return [[t[i] for t in texts] for i in range(len(texts[0]))]


def printed(path, pattern, pages=None, what=''):
    """The one printed sentence matching `pattern`, and the first page it is on.

    Reading orders are tried best first; the first that finds the pattern
    must find exactly one wording."""
    doc = _doc(str(path))
    pages = list(pages or range(1, len(doc) + 1))
    for order in range(len(page_texts(str(path), pages[0]))):
        found = {}
        for page in pages:
            for m in re.finditer(pattern, page_texts(str(path), page)[order]):
                found.setdefault(m.group(0), set()).add(page)
        if found:
            assert len(found) == 1, (what, str(path), pattern, found)
            text, where = found.popitem()
            return text, min(where)
    raise AssertionError((what, str(path), pattern, 'not printed'))


HEADING = rf'(?:Either|One|Any|Two|Three)\b[^.…:]{{0,40}}?:?(?:{LEADER}|\s+)(?:{MARKS})'


def heading_before(groups, typed, what=''):
    """The printed line that carries the marks for a list of answers which
    print none of their own ("Either of the following: ...... 5 marks")."""
    body = re.sub(rf'(?:\s—\s|\s=\s|\s)({MARKS})\.?$', '', typed)
    target, _ = skeleton(re.sub(rf'^{MARKER}\s*', '', body))
    for texts in groups:
        found = set()
        for text in texts:
            skel, index = skeleton(text)
            start = skel.find(target)
            while start >= 0:
                a = index[start]
                window = text[max(0, a - 300):a]
                heads = list(re.finditer(HEADING, window))
                if heads and re.fullmatch(rf'\s*(?:{MARKER})?\s*', window[heads[-1].end():]):
                    found.add(display(heads[-1].group(0)))
                start = skel.find(target, start + 1)
        if found:
            assert len(found) == 1, (what, typed, found)
            return found.pop()
    raise AssertionError((what, typed, 'no printed marks heading'))
