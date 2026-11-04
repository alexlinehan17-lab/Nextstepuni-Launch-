"""Read a page whose text layer is cut into overlapping vertical strips.

The 2011 Ordinary Business paper's page 11 (Question 8, Brady's Hotel) was
typeset as narrow vertical strips, each overlapping the next by one
character. get_text() returns it as 125 word-fragment blocks ('Exp', 'Out',
'Ma'), so a reader finds no part marker and no ask: the census lost the whole
question and the selection scan saw "wo of the fiv" instead of "two of the
five levels".

Two signals, the cheap one first. The fragments make short text lines: that
page has 140 lines of twelve characters or fewer, no other Business paper
page more than 50. The decisive signal is the overlap itself, the same
character printed again at a strip edge on one baseline: that page has 100
such overlaps, no other Business paper page more than six. strip_lines()
rebuilds the page in reading order from character positions (baseline, then
x), dropping the duplicated overlap character; its output was checked line by
line against the rendered page.
"""

SHORT_LINES = 100
STRIP_OVERLAPS = 20


def _chars(page):
    chars = []
    for block in page.get_text('rawdict')['blocks']:
        for line in block.get('lines', []):
            for span in line['spans']:
                for ch in span['chars']:
                    chars.append((ch['origin'][1], ch['origin'][0], ch['bbox'][2], ch['c']))
    return chars


def strip_cut(page, text=None):
    """True when the page's text layer is cut into overlapping strips."""
    text = page.get_text() if text is None else text
    if sum(1 for line in text.split('\n') if line.strip() and len(line.strip()) <= 12) < SHORT_LINES:
        return False
    seen = sorted((round(y), x, x1, c) for y, x, x1, c in _chars(page) if c.strip())
    overlaps = sum(1 for a, b in zip(seen, seen[1:])
                   if a[0] == b[0] and a[3] == b[3] and b[1] < a[2] - 0.5)
    return overlaps >= STRIP_OVERLAPS


def strip_lines(page):
    """The page's printed lines in reading order, rebuilt from its characters."""
    rows = []
    for y, x, x1, c in _chars(page):
        row = next((r for r in rows if abs(r[0] - y) < 1.5), None)
        if row is None:
            row = [y, []]
            rows.append(row)
        row[1].append((x, x1, c))
    out = []
    for _, chars in sorted(rows):
        text, last = [], None
        for x, x1, c in sorted(chars):
            if last and c == last[2] and (abs(x - last[0]) < 1.0 or (c != ' ' and x < last[1] - 0.5)):
                continue  # the same character again where two strips overlap
            if last and c != ' ' and text and text[-1] != ' ' and x - last[1] > 2.5:
                text.append(' ')
            text.append(c)
            last = (x, x1, c)
        out.append(''.join(text).strip())
    return out


def page_text(page):
    """get_text() for an ordinary page; the rebuilt lines for a strip-cut one."""
    text = page.get_text()
    return '\n'.join(strip_lines(page)) if strip_cut(page, text) else text
