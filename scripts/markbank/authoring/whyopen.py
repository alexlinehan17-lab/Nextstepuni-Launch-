#!/usr/bin/env python3
"""Why is each open part open? The bucket, not the total.

    python3 scripts/markbank/authoring/whyopen.py                 # every subject
    python3 scripts/markbank/authoring/whyopen.py physics --list  # and the parts

partcheck.py says how many parts are uncarded. That number on its own is not
actionable and has twice been acted on wrongly: a bucket called "the answer is a
drawing" was written off whole, and it held 156 cardable parts behind 13 dead
ones. A percentage cannot tell you whether the remainder is work or a ceiling.

So every open part is sorted here, first match wins, into one of:

  mispair   the scheme block offered for this part answers a different
            question. align_ordered pairs positionally and hands a pendulum
            part the gold-foil marking points, so a part that looks authorable
            is most often this. Read both documents before believing it.
  mangled   the scheme's answer does not survive its own font, so there is no
            text to lift. The 2023 Chemistry equation font maps several glyphs
            to one codepoint and "118" extracts as six copies of MATHEMATICAL
            BOLD DIGIT ONE.
  drawing+  the question wants a drawing AND the scheme states what the drawing
            must contain. CARDABLE: the criteria are the answer, and the card
            asks what a student would draw and what earns each mark.
  drawing-  the question wants a drawing and the scheme states no criteria, only
            "apparatus, method, observation (3 x 3)". Nothing to put on a card.
  rubric    the scheme answers with a marking convention rather than an answer.
  figure    the question cannot be read without art the catalogue does not hold.
  notariff  the scheme prints no marks against this part, usually because it
            prices the whole question on a sliding scale. Use ladder=, or leave
            it — NEVER estimate the split. That has been the recurring error.
  author    none of the above. Read the pairing, then card it.

The buckets are ordered so the cheapest disqualifier is tested first: a part
whose text is mangled cannot be assessed for anything else.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from align import align_ordered                             # noqa: E402
import coverage as C                                        # noqa: E402
import partcheck as PC                                      # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
FIGURES = os.path.join(ROOT, 'components/MarkBank/figures.json')

ORDER = ['author', 'drawing+', 'figure', 'notariff', 'mispair', 'drawing-',
         'rubric', 'mangled']
CARDABLE = {'author', 'drawing+'}
WORK = {'figure', 'notariff'}

# Codepoints that mean the text layer has lost the answer rather than printed
# it: the Mathematical Alphanumeric block a formula font falls back into, and
# the Oriya block the degree sign and several digits land in.
# Plus the substitute glyphs a broken font subset leaves behind: 'Ɵ' standing
# in for the 'ti' ligature ("Derive an equaƟon"), and anything in the private
# use area, which is where a subsetted font dumps what it could not map.
MANGLED = re.compile(r'[\U0001D400-\U0001D7FF଀-୿ƟƜ\uE000-\uF8FF]')

DRAW = re.compile(r'\b(draw|sketch|plot|construct|complete the diagram|'
                  r'label the diagram)\b', re.I)

# A scheme line that prices the shape of an answer instead of stating one. The
# scheme reprints the question above its own answer, so this is tested against
# what is LEFT after that cue is stripped — anchoring it at the raw start missed
# every "Describe an experiment... apparatus [3] method [3] observation [3]".
RUBRIC = re.compile(r'^(?:\W|\d)*(apparatus|method|observation|procedure|'
                    r'diagram|labell?ed diagram|any (?:two|three|four|one|valid|'
                    r'correct|suitable|other)\b|'
                    r'\d+\s*[x×]\s*\d+|srps?\b|correct answer|'
                    r'named? example|suitable|as above|accept any|'
                    r'(?:two|three|four|one|each)\s+(?:items?|answers?|points?|'
                    r'reasons?|ways?|examples?|uses?|factors?)\b|'
                    r'answers? (?:that are )?separated|mutually)', re.I)

# Page furniture the scheme prints once and the block reader can hand to a part.
FURNITURE = re.compile(r'(double solidus|mutually exclusive|marking scheme|'
                       r'leaving certificate|page \d+ of|blank page|'
                       r'partial answer from|//|section [a-d] \(|'
                       r'answer (?:any |all )?\w+ questions?)', re.I)

# The question leans on art: it points at something, or names a label only a
# figure carries. Bare letter runs count — "Name A, B and C" is unanswerable
# without the diagram just as surely as "the part labelled A" is, and the build
# refuses a lettered part with no figure behind it.
NEEDS_ART = re.compile(r'\b(diagram|figure|graph|chart|table above|photograph|'
                       r'shown (?:above|below|in)|in the (?:diagram|figure|graph|'
                       r'photograph|table)|labell?ed\s+[A-Z]\b|marked\s+[A-Z]\b'
                       r'|[A-Z],\s*[A-Z]\s*(?:,|and)\s*[A-Z]\b)\b')

MARKED = re.compile(r'[\[(]\s*\d{1,3}\s*[\])]|\b\d{1,3}\s*m(?:ark)?s?\b', re.I)


def bound_figures():
    """Every (year, level, question) the figure manifest can already illustrate."""
    try:
        man = json.load(open(FIGURES))
    except Exception:
        return set()
    entries = man if isinstance(man, list) else man.get('figures', man.values())
    out = set()
    for f in entries:
        if not isinstance(f, dict):
            continue
        k = f.get('key') or f.get('figureKey') or ''
        m = re.search(r'(\d{4})-(HL|OL|hl|ol)', k)
        if m:
            out.add((int(m.group(1)), m.group(2).lower()))
    return out


BOUND = bound_figures()


def strip_cue(point, question):
    """Drop the question the scheme reprints above its own answer.

    Without this the rubric test never fires: the point reads 'Describe a
    laboratory experiment to demonstrate this principle. apparatus [3] method
    [2] observation [2]', which starts with a verb and looks like an answer.
    What the examiner actually awards is the three words at the end.
    """
    q = PC.squash(question)
    if len(q) < 20:
        return point
    # The reprinted cue is often the question's TAIL, not its head: the paper
    # sets a stem and then asks, and the scheme prints only the asking part.
    # So the point's own leading run is looked for anywhere in the question,
    # not just at its start — anchoring at the start left "Describe a
    # laboratory experiment to demonstrate this principle. apparatus [3]
    # method [2] observation [2]" reading as a stated answer.
    squashed, index = [], []
    for i, ch in enumerate(point):
        c = re.sub(r'[^a-z0-9]', '', ch.lower())
        if c:
            squashed.append(c)
            index.append(i)
    body = ''.join(squashed)
    cut = 0
    for n in range(min(len(body), 300), 24, -1):
        if body[:n] in q:
            cut = index[n - 1] + 1
            break
    return point[cut:].strip(' .:;-—') if cut else point.strip(' .:;-—')


MARK_VALUE = re.compile(r'[\[(]\s*(\d{1,3})(?:\s*[+×x]\s*(\d{1,3}))*\s*[\])]')
TARIFF = re.compile(r'\(\s*(\d{1,3})\s*\)\s*$')


def upto_tariff(points, question, marks):
    """Points up to this part's printed tariff; the rest belong to the next part.

    The block reader takes everything between two scheme headings, and where a
    part's answer is short that run keeps going into the following part. A
    half-life answer was appearing under "Name two other items that can cause
    dispersion of light", which made a part the scheme prices at "two items
    [4 + 3]" — no items named, nothing to card — look authorable.

    The printed tariff is the honest stopping point, and it is the same check
    lib.Author.card() already makes before it will emit a card.
    """
    total = marks if isinstance(marks, int) and marks > 0 else None
    if total is None:
        m = TARIFF.search((question or '').strip())
        total = int(m.group(1)) if m else None
    if not total:
        return points
    kept, run = [], 0
    for p in points:
        kept.append(p)
        for m in MARK_VALUE.finditer(p):
            run += sum(int(g) for g in m.groups() if g)
        if run >= total:
            break
    return kept


def mispaired(question, cue):
    """Does the scheme block answer a different question than the paper asks?"""
    a, b = PC.squash(question), PC.squash(cue)
    if len(a) < PC.FLOOR or len(b) < PC.FLOOR:
        return False
    if a[:40] in b or b[:40] in a or a[-40:] in b:
        return False
    import difflib
    return difflib.SequenceMatcher(None, a[:160], b[:160]).ratio() < 0.5


def classify(question, points, marks, year, level, cue=None):
    text = ' '.join(points)
    if MANGLED.search(text) or MANGLED.search(question or ''):
        return 'mangled'
    q = question or ''
    # Tested BEFORE anything about the points, because every bucket below
    # asserts "these marking points answer this question" and a mispaired block
    # makes that false. Ordering it after the drawing branch had every mispaired
    # drawing question reading as cardable — the Chemistry scheme offering
    # "DEFINE: electronegativity" under "Draw a dot and cross diagram for NH3".
    if cue and mispaired(q, cue):
        return 'mispair'
    residue = [strip_cue(p, q) for p in upto_tariff(points, q, marks)]
    stated = []
    for r in residue:
        t = r.strip()
        if RUBRIC.match(t) or FURNITURE.search(t):
            continue
        # A residue that opens like a question and shares no run with this
        # part's question is the NEXT part's cue, not this part's answer.
        if PC.CUE_IS_A_QUESTION.match(t) and PC.squash(t)[:40] not in PC.squash(q):
            continue
        bare = re.sub(r'[\[(]\s*\d+[^\])]*[\])]', '', t).strip()
        # Long prose carrying no marks at all is a stem the reader picked up,
        # not an answer — a scheme prices what it awards.
        if len(bare) > 90 and not MARK_VALUE.search(t):
            continue
        if len(bare) > 12:
            stated.append(r)
    if DRAW.search(question or ''):
        return 'drawing+' if stated else 'drawing-'
    if not stated:
        return 'rubric'
    if NEEDS_ART.search(question or '') and (year, level) not in BOUND:
        return 'figure'
    if not marks and not MARKED.search(text):
        return 'notariff'
    return 'author'


def report(subject, show=False):
    if subject in PC.DEFER:
        print(f'{subject:<22} not measured here — use {PC.DEFER[subject]}')
        return {}
    by_ref = C.covered(subject)
    by_text = PC.asked(subject)
    tally = {k: 0 for k in ORDER}
    for year in range(2021, 2026):
        for level in ('hl', 'ol'):
            try:
                P, S, pairs, positional = align_ordered(subject, year, level)
            except Exception:
                continue
            texts = by_text.get((year, level), [])
            paired = {**positional, **pairs}
            asks = {sk: PC.question_of(P, S, pk, sk) for sk, (pk, _) in paired.items()}
            shared = PC.unreadable(P, [(pk, asks[sk]) for sk, (pk, _) in paired.items()])
            for skey, (pkey, _) in paired.items():
                pts = S.points(*skey)
                if not pts:
                    continue
                if pkey in shared and not PC.CUE_IS_A_QUESTION.match((asks[skey] or '').strip()):
                    continue
                q, letter, roman = pkey
                hit_ref = False
                for letters, romans in by_ref.get((year, level, q), ()):
                    if not letters and not romans:
                        hit_ref = letter is None and roman is None
                    else:
                        hit_ref = ((letter is None or not letters or letter in letters)
                                   and (roman is None or not romans or roman in romans))
                    if hit_ref:
                        break
                if hit_ref or PC.covered_by_text(asks[skey], texts):
                    continue
                try:
                    marks = S.marks(*skey)
                except Exception:
                    marks = None
                cue = (S.cues or {}).get(skey) if hasattr(S, 'cues') else None
                b = classify(asks[skey], pts, marks, year, level, cue)
                tally[b] += 1
                if show:
                    print(f'-- [{b}] {year} {level.upper()} {P.ref(pkey)}')
                    print(f'   Q: {(asks[skey] or "(no paper text)")[:150]}')
                    print(f'   * {pts[0][:150]}')
    total = sum(tally.values())
    cells = '  '.join(f'{k} {tally[k]:>3}' for k in ORDER)
    print(f'{subject:<22} {total:>4} open   {cells}')
    return tally


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    show = '--list' in sys.argv
    targets = args or C.SUBJECTS
    grand = {k: 0 for k in ORDER}
    for s in targets:
        for k, v in (report(s, show and len(targets) == 1) or {}).items():
            grand[k] += v
    if len(targets) > 1:
        total = sum(grand.values())
        print(f'\n{"TOTAL":<22} {total:>4} open   '
              + '  '.join(f'{k} {grand[k]:>3}' for k in ORDER))
        card = sum(grand[k] for k in CARDABLE)
        work = sum(grand[k] for k in WORK)
        mis = grand['mispair']
        print(f'\n  cardable as they stand : {card}')
        print(f'  reachable with work    : {work}')
        print(f'  read the pairing first : {mis}')
        print(f'  ceiling                : {total - card - work - mis}')
