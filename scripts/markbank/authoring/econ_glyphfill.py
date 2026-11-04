#!/usr/bin/env python3
"""Fill glyphs a scheme PDF draws but whose ToUnicode entry is a space.

    python3 scripts/markbank/authoring/econ_glyphfill.py 2026 hl          # report
    python3 scripts/markbank/authoring/econ_glyphfill.py 2026 hl --write  # append

The 2026 Economics schemes embed a Calibri subset whose ToUnicode map sends a
handful of glyphs to U+0020. The page draws "GDP was €153.4 billion"; the text
layer reads "G P was €15 .4 billion". Nothing downstream can see the fault:
it is not a strange character, it is a space, so a card sliced from the
extraction would ship "Ireland's G P" with every gate green.

The repair is DERIVED, never typed (see markbank-glyph-repair). A font that
keeps its original glyph ids spells most of them correctly most of the time,
so each glyph id's character is learned from the sightings that agree, across
several SEC PDFs, and only ids that agree overwhelmingly are used. A drawn
glyph is filled only when its id's learned character is not a space.

`--write` APPENDS the filled text of every affected block to the scheme
markdown under a marker, replacing an earlier copy. Every original line stays,
so a claim that traced before still traces; a claim lifted from the filled
text now traces too, against characters the SEC printed. `fills()` gives the
authoring scripts the same line-level repairs, so the text they slice can be
filled identically.
"""
import collections
import os
import sys

import fitz

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
CORPUS = os.path.join(ROOT, 'paper-trail-corpus')
MARK = '<!-- markbank:glyph-fill -->'
END = '<!-- /markbank:glyph-fill -->'
# The fonts that keep Calibri's own glyph ids, recognised by their space: id 3.
SPACE_GID = 3
MIN_SIGHTINGS = 10
MIN_AGREEMENT = 0.98
MIN_LINE = 15


def _learning_set(year):
    names = []
    for kind in ('markingschemes', 'exampapers'):
        folder = os.path.join(CORPUS, kind, str(year))
        if os.path.isdir(folder):
            names += [os.path.join(folder, f) for f in sorted(os.listdir(folder))
                      if f.startswith('LC034') and f.endswith('EV.pdf')]
    return names


def learn(pdfs):
    """(font, gid) -> character, from spans that use the original glyph ids."""
    seen = collections.defaultdict(collections.Counter)
    for path in pdfs:
        with fitz.open(path) as doc:
            for page in doc:
                for tr in page.get_texttrace():
                    if not any(c[0] == 32 and c[1] == SPACE_GID for c in tr['chars']):
                        continue
                    for c in tr['chars']:
                        if c[0] > 0:
                            seen[(tr['font'], c[1])][chr(c[0])] += 1
    out = {}
    for key, counts in seen.items():
        # The space sightings ARE the fault being repaired, so agreement is
        # measured among the sightings that drew a real character.
        drawn = collections.Counter({c: n for c, n in counts.items() if c != ' '})
        if not drawn:
            continue
        ch, n = drawn.most_common(1)[0]
        if n >= MIN_SIGHTINGS and n / sum(drawn.values()) >= MIN_AGREEMENT:
            out[key] = ch
    return out


def _original_ids(tr, learned):
    """Whether a drawn span uses the original glyph ids the map was learned on.

    Either it draws its ordinary spaces with id 3, or every real character in
    it agrees with the learned map (a short run such as "€23,333m" has no
    space of its own to recognise it by).
    """
    if any(c[0] == 32 and c[1] == SPACE_GID for c in tr['chars']):
        return True
    drawn = [c for c in tr['chars'] if c[0] > 32]
    return bool(drawn) and all(learned.get((tr['font'], c[1])) == chr(c[0]) for c in drawn)


def _gid_at(page, learned):
    """Drawing origin -> (font, gid, unicode) for every glyph on the page."""
    at = {}
    for tr in page.get_texttrace():
        if not _original_ids(tr, learned):
            continue
        for c in tr['chars']:
            at[(round(c[2][0], 2), round(c[2][1], 2))] = (tr['font'], c[1], c[0])
    return at


def repaired_blocks(pdf, learned):
    """[(page, damaged line pairs, filled text)] for every page with damage.

    The whole page is re-read in block order, not only the damaged block, so
    a response that runs across several text blocks (a trend sentence and the
    explanation printed beneath it) stays contiguous in the appended copy.
    """
    out = []
    with fitz.open(pdf) as doc:
        for pno, page in enumerate(doc, 1):
            at = _gid_at(page, learned)
            page_pairs, page_text = [], []
            for block in page.get_text('rawdict')['blocks']:
                if block.get('type') != 0:
                    continue
                lines_fixed, pairs, damaged = [], [], False
                for line in block['lines']:
                    before, after = [], []
                    for span in line['spans']:
                        for ch in span['chars']:
                            c = ch['c']
                            fill = c
                            if c == ' ':
                                hit = at.get((round(ch['origin'][0], 2), round(ch['origin'][1], 2)))
                                if hit and (hit[0], hit[1]) in learned:
                                    fill = learned[(hit[0], hit[1])]
                            before.append(c)
                            after.append(fill)
                    b, a = ''.join(before), ''.join(after)
                    if a != b:
                        damaged = True
                        pairs.append((' '.join(b.split()), ' '.join(a.split())))
                    lines_fixed.append(' '.join(a.split()))
                page_pairs += pairs
                page_text.append(' '.join(x for x in lines_fixed if x))
            if page_pairs:
                out.append((pno, page_pairs, '\n'.join(t for t in page_text if t)))
    return out


_CACHE = {}


def fills(year, level):
    """Line-level (damaged, filled) pairs for one Economics scheme, longest first."""
    key = (year, level)
    if key not in _CACHE:
        fileid = 'LC034ALP000EV.pdf' if level in ('hl', 'higher') else 'LC034GLP000EV.pdf'
        pdf = os.path.join(CORPUS, 'markingschemes', str(year), fileid)
        learned = learn(_learning_set(year))
        pairs = {d: f for _, ps, _ in repaired_blocks(pdf, learned) for d, f in ps}
        _CACHE[key] = sorted(pairs.items(), key=lambda kv: -len(kv[0]))
    return _CACHE[key]


def fill(text, year, level):
    """Apply the derived line repairs to text sliced from the extraction."""
    for damaged, filled in fills(year, level):
        # Whole damaged lines only: a two-letter chart fragment ("E P") would
        # otherwise be "repaired" inside unrelated text.
        if len(damaged) >= MIN_LINE and damaged in text:
            text = text.replace(damaged, filled)
    return text


def main():
    year, level = int(sys.argv[1]), sys.argv[2]
    fileid = 'LC034ALP000EV.pdf' if level == 'hl' else 'LC034GLP000EV.pdf'
    pdf = os.path.join(CORPUS, 'markingschemes', str(year), fileid)
    learned = learn(_learning_set(year))
    blocks = repaired_blocks(pdf, learned)
    for pno, pairs, _ in blocks:
        for d, f in pairs:
            print(f'p{pno}: {d!r}\n    -> {f!r}')
    if '--write' not in sys.argv:
        return
    md = os.path.join(ROOT, 'examiner-reports', 'economics', 'schemes', f'{year}-{level}.md')
    text = open(md, encoding='utf-8').read()
    if MARK in text:
        head, _, rest = text.partition(MARK)
        text = head.rstrip('\n') + rest.partition(END)[2]
    body = '\n'.join(block for _, _, block in blocks)
    with open(md, 'w', encoding='utf-8') as fh:
        fh.write(f'{text.rstrip()}\n\n{MARK}\n{body}\n{END}\n')
    print(f'{md}: appended {len(blocks)} filled page(s)')


if __name__ == '__main__':
    main()
