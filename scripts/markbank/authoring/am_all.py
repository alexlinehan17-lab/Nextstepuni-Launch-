#!/usr/bin/env python3
"""Author every Applied Mathematics ask the paper prints and the scheme prices.

    python3 scripts/markbank/authoring/am_all.py --report
    python3 scripts/markbank/authoring/am_all.py > scripts/markbank/authored/applied-maths.json

WHAT ONE CARD IS
----------------
One priced ask. Its question comes from the PAPER (paper.py, read span-aware
through mathtext so exponents and indices survive), its steps from the SCHEME
(am_scheme.py), and the tariff is the mark the SEC printed against each step.
Nothing is apportioned: a 20-mark ask is 20 because the scheme prints four
fives inside it.

THE TARIFF SHAPE
----------------
The same shape Mathematics ships, for the same reason. A worked solution is not
a menu of alternatives and it is not a list to recall in full: it is a ladder,
and what a student banks is how far up it they got. `anyN` with
`perOptionSteps` is the card model's own name for that — the options are the
scheme's own printed steps, in the order it sets them, and each carries the
mark the SEC printed beside it.

WHY A CARD SOMETIMES CITES THE PART RATHER THAN THE ROMAN
---------------------------------------------------------
The old syllabus (2021-2022) prints its part markers in the middle of the
working, and where a fraction's bar swallows one the reader cannot say which
of a part's romans a step belongs to. Guessing would put (i)'s working under
(ii) — a wrong citation, which is worse than a coarse one. So where the
reader's romans do not account for exactly the romans the PAPER prints under a
part, the part is carded whole: one card citing "Q3(a)", holding every step the
scheme printed for it, in order. reconcile.py counts that as covering the
romans beneath it, which is true — the ask is in the bank, inside that card.

REFUSALS
--------
Every one is a named bucket, counted and exampled by --report:
  * the scheme answers the ask with a DRAWING — its steps are priced but the
    page prints no words for them, only the diagram it awards them for;
  * the scheme prices a step whose words the card cannot show (a part-drawn
    ask: some steps are working, some are the diagram);
  * the paper prints no text the card can carry for the ask;
  * a step cannot be traced back to the scheme markdown the build checks
    against;
  * the ask has more priced steps than one card may show;
  * the ask points at printed matter the card cannot carry — what is left of
    this bucket once am_question_figures.py has cut the diagram and bound it.
    111 asks were refused here before that pass existed; two are, now;
  * the ask names lettered parts the scheme never decodes. A crop alone does
    not answer "the parts labelled A, B and C": the build wants the letters
    decoded as well, and there is nothing in these schemes to lift a decode
    from;
  * a printed character did not survive the paper's font, tested exactly as
    the build tests it, so the count here and the count in the deck agree.
"""
import argparse
import collections
import json
import os
import re
import unicodedata
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

import am_scheme                                              # noqa: E402
import am_topics                                              # noqa: E402
import mathtext                                               # noqa: E402
import paper as PP                                            # noqa: E402
from markbank_authoring import anyN, make_audit, make_card     # noqa: E402
import cardlint                                                # noqa: E402

SUBJECT = 'applied-maths'
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
YEARS = (2021, 2022, 2023, 2024, 2025)
LEVELS = ('hl', 'ol')
MAX_STEPS_SHOWN = 16          # MAX_LONG_OPTION_ROWS in types/markBank.ts

_card = make_card(SUBJECT, default_section='B')
audit = make_audit(MAX_STEPS_SHOWN)

# The picture each ask points at, cut from the paper by am_question_figures.py
# and published through the manifest by bind-figures.mjs. A card that CARRIES
# the diagram is no longer pointing at printed matter it cannot show, so this
# is read before the figure gate below. Nothing here is a path: the sidecar
# names a KEY, and the build resolves it against the manifest, confirms the
# file is on disk and that its bytes still hash to what the inspecting agent
# saw. Both historical figure corruptions in this repo came in through a
# hand-transcribed path.
QFIGS = os.path.join(ROOT, 'scripts', 'markbank', 'authored',
                     f'{SUBJECT}-question-figures.json')
FIGURES = (json.load(open(QFIGS, encoding='utf-8'))
           if os.path.exists(QFIGS) else {})
MANIFEST = os.path.join(ROOT, 'components', 'MarkBank', 'figures.json')
_INSPECTED = (set(json.load(open(MANIFEST, encoding='utf-8')))
              if os.path.exists(MANIFEST) else set())

# The running header runs on into a part's text where the question ends near
# the foot of a page.
FURNITURE_TAIL = re.compile(
    r'\s*(Leaving Certificate\s*,?\s*\d{4}|Applied Mathematics\s*[–-]|Page\s+\d+\s+of)'
    r'[\s\S]*$', re.I)
# A whole step that names the WORK rather than doing it. "justification",
# printed alone in the solution column against five marks, is the SEC telling
# its examiners to look for reasoning — it is not reasoning, and a student who
# read it on a card would learn nothing they could write. 2023 Ordinary prints
# it twice, under Q5(b) ("Y" ⟨5⟩ / "justification" ⟨5⟩) and under Q10(v)
# ("C and D" ⟨5⟩ / "justification" ⟨5⟩), and both were refused for the wrong
# reason — that one letter "did not survive the scheme's font".
CONTENT_FREE = re.compile(r'^(as above|see above|or equivalent|etc\.?|'
                          r'accept any|other relevant|justification|'
                          r'justify)\W*$', re.I)
# A step the reader recovered as an unreadable smear: a run of replacement
# characters, or a line with no letter or digit in it at all. The provenance
# gate would refuse most of these anyway; refusing them here says WHY.
UNREADABLE = re.compile(r'[�]')
# The build's own broken-subset test, mirrored from BROKEN and REAL in
# build-deck.mjs. A card carrying one of these is DROPPED there, so the author
# has to refuse it here or its number and the deck's disagree: two asks the
# figure pass unblocked print their dot product with a glyph the font subset
# maps into the Malayalam block, and they came through as cards the build then
# threw away without the report ever saying so.
BROKEN_GLYPH = re.compile('[\u0100-\u1FFF\uE000-\uF8FF\uFB00-\uFB4F]')
REAL_SCRIPT = re.compile(
    '[\u0100-\u017F\u0218-\u021B\u02B0-\u02FF\u0302\u0305\u0307\u0308'
    '\u0370-\u03FF\u0400-\u04FF\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF'
    '\u1D62-\u1D6A\u1F00-\u1FFF]')


def broken_glyphs(text):
    return [c for c in BROKEN_GLYPH.findall(text or '')
            if not REAL_SCRIPT.match(c)]


# The three line shapes schemeText.mjs drops before it compares.
MARKS_ONLY = re.compile(r'^\s*\d+\s*(\(\s*\d+\s*\))?\s*$')
LABEL_ONLY = re.compile(r'^\s*\(?\s*([ivx]{1,4}|[a-z]|\d{1,2})\s*\)\s*$', re.I)
LEADING_LABEL = re.compile(r'^\s*\(\s*(?:[ivx]{1,4}|[a-z]|\d{1,2})\s*\)\s+(?=\S)', re.I)


def _squash(t):
    return re.sub(r'[^a-z0-9]+', '', mathtext.demangle(t or '').lower())


class Refused(Exception):
    pass


def card_id(year, level, key):
    q, letter, roman = key
    bits = ['am', str(year), level, str(q)]
    if letter:
        bits.append(letter)
    if roman:
        bits.append(roman)
    return '-'.join(bits)


# The printed marker, taken off the front of an ask. clean_like returns the
# question with the "(iii)" the page sets before it, and the card already names
# the part it cites in its own reference -- printed twice it reads as part of
# the question.
_LEADING_MARKER = re.compile(
    r'^\s*\(\s*(?:[a-z]|i{1,3}|iv|vi{0,3}|ix|xi{0,3})\s*\)\s*', re.I)


def _recovered(files, raw, repair):
    """clean_like's reading of `raw`, with the printed marker off the front.

    NO GUARD. One was tried here and withdrawn, and the reason is worth
    keeping. clean_like re-reads the PDF to recover what the text layer
    flattened, locating the fragment by its first occurrence, and where two
    asks open with the same words it finds the wrong one: 2021 Higher Q6(b)(i)
    is "Find the value of 𝜃" and it returns Question 1(b)(ii)'s "Find the value
    of f". That is a real defect and it is still here.

    The guard compared what clean_like returned against paper.py's own block
    and kept the block where they disagreed. It cannot work, because NEITHER
    candidate is reliably the better one -- both are garbled on different asks,
    and choosing between them by any similarity measure gets it wrong in both
    directions. Two ways it did:

      * 2023 Higher Q10(b)(ii). The paper prints "show that cos 𝜃 = (k−2)/3".
        paper.py's block loses the denominator -- "show that cos 𝜃 = 𝑘−2" --
        and clean_like has the fraction but out of order. Keeping the block
        asked a student to PROVE SOMETHING FALSE, which is worse than garbled.
      * 2022 Higher Q10(a). clean_like lifts the question number off the
        margin into the sentence and drops the equals from a differential
        equation; an ASCII-letter comparison caught that, and folding the
        Mathematical Alphanumeric letters -- which has to be done, or the
        guard destroys every recovered subscript -- stops catching it.

    So this returns what the subject shipped before: clean_like's reading,
    whatever it is. Choosing between two mangled readings is not a job for a
    similarity test; it needs the PAGE, and that is a separate piece of work.
    """
    if not raw:
        return ''
    return _LEADING_MARKER.sub(
        '', repair(mathtext.clean_like(files, raw))).strip()


def question_ref(year, level, key):
    q, letter, roman = key
    ref = f'{year} {level.upper()} Q{q}'
    if letter:
        ref += f'({letter})'
    if roman:
        ref += f'({roman})'
    return ref


class Author:
    def __init__(self, year, level, census_text=None):
        self.year, self.level = year, level
        self.paper_text = am_scheme._paper_index(year, level)
        self.S = am_scheme.AmScheme(year, level, paper_text=self.paper_text)
        self.P = PP.Paper(SUBJECT, year, level)
        # {key: the paper's words for that leaf} as the CENSUS reads them.
        # paper.py blocks a paper out on its printed markers, and this paper
        # sets the first of a run inside the sentence that introduces it —
        # "Find (i) the speeds of P and Q immediately after the collision" is
        # one line, with (i) in the middle of it — so (i) gets no block of its
        # own and the card had no question to ask. The census already recovers
        # those: complete_leading_romans() splits the parent's own text on its
        # printed romans, which is the same paper, the same words, read at the
        # grain the page prints them. Used only where paper.py has nothing.
        self.census_text = census_text or {}
        self._flat = None

    # -- the scheme markdown, as the build's provenance gate reads it --------
    def _scheme_flat(self):
        """The scheme as the build's provenance gate reads it.

        Mirrors schemeText.mjs comparableScheme(): the extractor's page
        markers, the lines that are nothing but a mark, and the lines that are
        nothing but a part label all come out — a part label printed on its own
        row sits BETWEEN two lines of one step, and leaving it in made a step
        the scheme plainly prints look untraceable. Both of the gate's forms
        are searched, the second with a leading label stripped from each line.
        """
        if self._flat is None:
            path = os.path.join(ROOT, 'examiner-reports', SUBJECT, 'schemes',
                                f'{self.year}-{self.level}.md')
            raw = open(path, encoding='utf-8').read()
            keep = [l for l in raw.split('\n')
                    if not re.match(r'^##\s*Page\s*\d+\s*$', l)
                    and not MARKS_ONLY.match(l) and not LABEL_ONLY.match(l)]
            self._flat = (_squash(' '.join(keep)),
                          _squash(' '.join(LEADING_LABEL.sub('', l)
                                           for l in keep)))
        return self._flat

    def traceable(self, text):
        sq = _squash(text)
        return any(sq in form for form in self._scheme_flat())

    # -- the paper's own wording --------------------------------------------
    def question(self, key):
        """The paper's wording for this ask, joined where the card is coarser.

        A card that cites a PART holds every roman under it, so its question is
        every roman's wording in the order the paper prints them — the paper's
        own words either way.
        """
        q, letter, roman = key
        exact = [k for k in self.P.parts
                 if k[0] == q and k[1] == letter and (roman is None or k[2] == roman)]
        if not exact and roman is None:
            exact = [k for k in self.P.parts if k[0] == q and k[1] == letter]
        if not exact and letter is None:
            exact = [k for k in self.P.parts if k[0] == q]
        if not exact:
            # The census read this leaf out of its parent's own sentence.
            lifted = (self.census_text.get(key) or '').strip()
            return _recovered(self.P.files, lifted, am_scheme.repair)
        # In PRINTING order, which puts a part's own opening paragraph before
        # the romans under it. _rank() scores an unknown roman 99, and a key
        # with no roman at all was taking that score — so 2021 Ordinary Q5(b)
        # read "the velocity of the ball immediately after it hits the floor /
        # the value of h. / A ball is dropped from a height of 11.25 m...",
        # asking for the answer before saying what the question was.
        exact.sort(key=lambda k: (k[1] or '',
                                  -1 if k[2] is None else am_scheme._rank(k[2])))
        # Repaired BLOCK BY BLOCK, then joined — the same way maths_lib does
        # it, and for the same reason. clean_like locates one fragment at a
        # time: it finds the longest prefix the document spells and returns a
        # window as long as the whole fragment starting there. Handed a JOIN of
        # blocks that the paper prints with its own markers and command word
        # between them ("Calculate  (i) ...  (ii) ..."), the window pays for
        # those out of its budget and runs off one end or the other. 2021
        # Ordinary Q5(b) lost its second ask, "the value of h", off the tail;
        # before the sort above was fixed the same window ran the other way and
        # brought the whole of Question 6 back with it.
        #
        # Repaired again on the way out. paper.py repairs the blocks it hands
        # back, but clean_like re-reads the PDF itself to recover the
        # exponents, and its own table is the SHARED one — so this subject's
        # own glyphs came back unrepaired in the question text while the same
        # characters were repaired in the scheme's.
        pieces = []
        for k in exact:
            raw = (self.P.text(*k) or '').strip()
            if not raw:
                continue
            pieces.append(_recovered(self.P.files, raw, am_scheme.repair))
        return ' '.join(' '.join(pieces).split())

    def stem(self, key):
        """The paper's setup above the ask — the context it leans on."""
        q, letter, roman = key
        raws = []
        # The letter's OWN opening prose. Applied Maths sets a part as
        # "(a) A ball is thrown vertically downwards from the top of a
        # building of height h m. ... Find (i) the value of h", and paper.py
        # files that paragraph as the text of (a) rather than as a stem — so
        # reading stems alone left "the value of h" standing on its own with
        # nothing to say what h is.
        if roman is not None and letter is not None:
            raws.append((self.P.text(q, letter, None) or '').strip())
        elif roman is not None:
            raws.append((self.P.text(q, None, None) or '').strip())
        for src in ((q, None), (q, letter) if letter else None):
            if not src:
                continue
            raws.append((self.P.stem(*src) or '').strip())
        pieces = []
        for raw in raws:
            if len(_squash(raw)) >= 15:
                # Cut at the running header, exactly as the ASK is cut. The
                # trim was only ever applied to the question, and a stem that
                # ran over a page break carried the header and everything the
                # reader picked up after it: 41 of this deck's 280 cards showed
                # a student "... 6 m Q 10 Leaving Certificate, 2023 Applied
                # Mathematics – Higher Level Draw a diagram to show the
                # external forces acting on seat A.", and four of them carried
                # the paper's copyright notice or its "Do not hand this up."
                pieces.append(FURNITURE_TAIL.sub('', am_scheme.repair(
                    mathtext.clean_like(self.P.files, raw))).strip())
        text = ' '.join(dict.fromkeys(p for p in pieces if p))
        return text if len(_squash(text)) >= 15 else ''

    def drawn_quote(self, units):
        """Everything the scheme prints in this ask's band, and where.

        The evidence for an exclusion has to be a quotation, and an ask whose
        whole answer is a drawing has no prose to quote — so what is quoted is
        the drawing's own printed matter: every row the page sets between this
        leaf's head and its tariff, at the coordinate it is printed at, with
        the ones inside drawn or raster ink named as such. A reader can put the
        page beside this list and check it.

        Read back off the PAGE rather than off the walk. The walk drops a row
        of the old syllabus's reprint before it ever asks whether the row is
        inside ink, so the units of 2021 and 2022 carry almost none of their
        own labels — and an exclusion whose evidence is "the band prints no
        text at all" is an assertion, not a quotation.
        """
        out = []
        for u in units:
            page = self.S.doc[u.page]
            boxes = am_scheme.ink(page)
            lo = (u.y0 if u.y0 is not None else 0) - 2
            # Down to the NEXT leaf's head, not to this one's last tariff. The
            # scheme prints the mark level with the leaf's head and the drawing
            # BELOW both — 2022 Ordinary Q7(a)(i) sets its "(i)" at y=326 and
            # its "(10)" at y=340, with the whole loaded beam from y=350 down —
            # so a band that stops at the tariff quotes nothing at all.
            later = [o.y0 for o in self.S.units.values()
                     if o.page == u.page and o.y0 is not None and o.y0 > lo + 4]
            hi = min(later) - 4 if later else page.rect.height - am_scheme.FOOTER_BAND
            for y, x0, x1, t in self.S.rows(page):
                if not t or not (lo <= y <= hi) or x0 >= self.S.cut:
                    continue
                # A head is a head by WHERE it is printed, not by its shape.
                # "5g" and "3g" — the weights hanging off a pulley diagram —
                # parse as "question 5, part g", and a shape test dropped both
                # labels of 2021 Ordinary Q4(a)(i) out of its own evidence.
                if am_scheme.MARKER_ONLY.match(t) or am_scheme.FURNITURE.match(t):
                    continue
                if abs(x0 - self.S.head_x) <= 3 and (
                        am_scheme.NEW_HEAD.match(t)
                        or am_scheme.OLD_HEAD.match(t)):
                    continue
                inside = any(bx0 - 4 <= x0 <= bx1 + 4 and by0 - 4 <= y <= by1 + 4
                             for bx0, by0, bx1, by1 in boxes)
                out.append(f'p.{u.page + 1} y={y:.1f} x={x0:.1f} {t!r}'
                           + (' [inside the drawing]' if inside else ''))
        if not out:
            raster = [i['bbox'] for u in units
                      for i in self.S.doc[u.page].get_image_info()]
            if raster:
                return ('the band carries no text whatever: the answer is a '
                        'placed RASTER image, at '
                        + '; '.join(f'({b[0]:.0f},{b[1]:.0f})-({b[2]:.0f},'
                                    f'{b[3]:.0f})' for b in raster[:4])
                        + ', so there is not even a label to lift')
            return ('the band prints no text at all between the head and the '
                    'tariff: the drawing is the only thing on it')
        more = f' … and {len(out) - 14} more' if len(out) > 14 else ''
        return ('every row the band prints, in order: '
                + '; '.join(out[:14]) + more)

    # -- one card ------------------------------------------------------------
    def card(self, key, units, refs):
        ref = question_ref(self.year, self.level, key)
        steps = [(t, m) for u in units for t, m in u.groups]
        total = sum(m for _, m in steps)
        if not total:
            raise Refused(('the scheme prints no mark for this ask', ref))
        # THE SCHEME'S OWN ARITHMETIC HAS TO CLOSE. Each part carries the total
        # the SEC printed for it in brackets, and where the steps this reader
        # priced do not add up to that total, it has not read the part -- it
        # has read some of it, and a card built on that claims a tariff the
        # scheme never gave the answer it shows.
        #
        # Both shapes are the same underlying fault, the scheme's REPRINT of
        # the question read as a priced step:
        #   2022 Higher Q6(b) is priced (25) and came back as ONE five-mark
        #     step reading "A particle is attached to one end of a light
        #     inextensible..." -- the paper's own question, offered as a
        #     five-mark answer to a twenty-five-mark part.
        #   2021 Ordinary Q6(b)(ii) is priced (30) and came back as four steps
        #     summing to 25, the first of them ten marks of "A uniform
        #     triangular lamina in the shape of an isosceles triangle...".
        #
        # Refused rather than shipped short: never guess a tariff, and a
        # tariff that does not match the marks beside the answer is a guess.
        #
        # Only where the card COVERS the whole part. part_total is the part's
        # own figure and the scheme hangs it on the LAST sub-part of the run --
        # 2021 Higher Q1(a) is (i) at 15 and (ii) at 10, and the (25) sits on
        # (ii) -- so measuring one roman's steps against it condemns every
        # correctly split part in the subject. It cost 38 good cards before
        # this line was added.
        #
        # 50 is the whole QUESTION's total on this paper, and where it turns up
        # against a part key the reader has picked up the question's closing
        # figure rather than the part's -- no evidence about the part, so no
        # claim is made on it.
        printed = {u.part_total for u in units
                   if getattr(u, 'part_total', None) and u.part_total != 50}
        if key[2] is None and len(printed) == 1:
            want = printed.pop()
            if want != total:
                page = min(u.page for u in units) + 1
                raise Refused((
                    'the priced steps do not add up to the total the scheme '
                    'prints for this part', ref,
                    f'{self.year} {self.level.upper()} scheme p.{page}, '
                    f'{ref.split()[-1]}: the SEC prints ({want}) for this '
                    f'part and the steps read here come to {total} — '
                    f'{len(steps)} step(s) at '
                    f'{", ".join(str(m) for _, m in steps)}. Part of what the '
                    f'scheme states has not been read, so the card would '
                    f'claim a tariff the answer it shows was never given.'))
        if all(not t for t, _ in steps):
            page = min(u.page for u in units) + 1
            marks = ', '.join(str(m) for _, m in steps)
            asked = ' '.join(f'{self.stem(key)} {self.question(key)}'.split())[:120]
            raise Refused(('the scheme answers this ask with a drawing', ref,
                           f'{self.year} {self.level.upper()} scheme p.{page}, '
                           f'{ref.split()[-1]}: the scheme prints the mark(s) '
                           f'{marks} against this ask and no line of working '
                           f'at all — everything printed under the head is the '
                           f'drawing and the labels on it, which is what the '
                           f'mark is awarded for. The paper asks: {asked!r}',
                           self.drawn_quote(units)))
        if any(not t for t, _ in steps):
            drawn = sum(m for t, m in steps if not t)
            raise Refused((f'the scheme awards {drawn} of these marks for a '
                           f'diagram it draws rather than states', ref))
        rows = [(t.strip(), m) for t, m in steps
                if not CONTENT_FREE.match(t.strip())]
        if len(rows) != len(steps):
            empty = next(t.strip() for t, _ in steps
                         if CONTENT_FREE.match(t.strip()))
            page = min(u.page for u in units) + 1
            priced = next(m for t, m in steps if CONTENT_FREE.match(t.strip()))
            raise Refused(('a priced step states nothing liftable', ref,
                           f'{self.year} {self.level.upper()} scheme p.{page}, '
                           f'{ref.split()[-1]}: the scheme prices a step at '
                           f'{priced} and states it as {empty!r}, which names '
                           f'the work instead of doing it. The whole of this '
                           f'ask, as the scheme prints it, is: '
                           + '; '.join(f'{t.strip()!r} ⟨{m}⟩'
                                       for t, m in steps)))
        bad = [t for t, _ in rows if UNREADABLE.search(t) or len(_squash(t)) < 2]
        if bad:
            raise Refused(('a priced step did not survive the scheme\'s font',
                           f'{ref}: {bad[0][:60]!r}'))
        # An unbalanced bracket is a splice casualty. The scheme sets
        # "F = mr w^2 = 4 x 2 x (5pi/3)^2" with the fraction stacked, and where
        # the reader loses one side of it the step reads "4 x 2 x ( = 219.3 N"
        # — arithmetic that does not close, which is not what the SEC printed
        # and is worse than nothing in front of a student.
        torn = [t for t, _ in rows
                if t.count('(') != t.count(')') or t.count('{') != t.count('}')]
        if torn:
            raise Refused(('a priced step lost half of a stacked expression',
                           f'{ref}: {torn[0][:60]!r}'))
        # A step whose words the PAPER prints is the scheme's reprint of the
        # question, not its answer to it — the reader's boundary between the
        # two slipped. Shipping it would put the question in front of a student
        # as a marking point.
        paper = self.paper_text.get(None) or ''
        echo = [t for t, _ in rows
                if len(_squash(t)) >= 25 and _squash(t) in paper]
        if echo:
            raise Refused(('a priced step is the scheme\'s reprint of the '
                           'question, not its answer',
                           f'{ref}: {echo[0][:60]!r}'))
        if len(rows) > MAX_STEPS_SHOWN:
            raise Refused((f'more than {MAX_STEPS_SHOWN} priced steps', ref))
        untraceable = [t for t, _ in rows if not self.traceable(t)]
        if untraceable:
            raise Refused(('a priced step cannot be traced to the scheme',
                           f'{ref}: {untraceable[0][:60]!r}'))

        qtext = FURNITURE_TAIL.sub('', self.question(key)).strip(' .;,')
        # The paper prints the part marker with the ask, and the card already
        # says which part it is in its citation — "(iii) Solve the difference
        # equation" reads as if a step were missing above it.
        qtext = LEADING_LABEL.sub('', qtext)
        stem = self.stem(key)
        if stem and _squash(stem) in _squash(qtext):
            stem = ''
        joined = ' '.join(f'{stem} {qtext}'.split())
        # Judged on the ask AND its stem. A roman here is often three words —
        # "the value of h" — and unanswerable alone; what makes it a question
        # is the paragraph above it, which the card carries as its stem and
        # the session prints above the ask. Measuring the roman by itself
        # refused twenty-six asks whose wording is on the page in full.
        if len(_squash(joined)) < 12 and len(joined) < 24:
            raise Refused(('the paper prints no text for this ask', ref))
        # The ASK itself still has to be there. A card whose whole question is
        # its stem asks the student nothing, and the build drops it — better to
        # say so here than to lose it silently at the gate.
        if len(_squash(qtext)) < 8:
            raise Refused(('the paper prints only the setup for this ask, no '
                           'question of its own', ref))
        # The crop, if this ask has one. A key the manifest has never inspected
        # is treated as no figure at all rather than shipped: the build would
        # drop the card, and a refusal here says why.
        figure = FIGURES.get(card_id(self.year, self.level, key), '')
        if figure and figure not in _INSPECTED:
            figure = ''
        wrecked = broken_glyphs(joined) or broken_glyphs(
            ' '.join(t for t, _ in rows))
        if wrecked:
            raise Refused(('a printed character did not survive the paper\'s '
                           'font', f'{ref}: '
                           f'U+{ord(wrecked[0]):04X} in {joined[:48]!r}'))
        if cardlint.NAMES_LETTERS.search(joined):
            # A lettered ask needs its letters DECODED as well as shown, and
            # the decode has to be lifted from somewhere. These schemes name a
            # point in their working, not in a key, so there is nothing to lift
            # and the build would drop the card even with the crop bound.
            raise Refused(('the ask names lettered parts the scheme never '
                           'decodes', ref))
        if not figure and (cardlint.FIG_REF.search(joined)
                           and not cardlint.SELF_WORK.search(joined)
                           and not cardlint.NO_DEPENDENCY.search(joined)):
            raise Refused(('the ask points at printed matter the card cannot '
                           'carry', ref))

        topic, matched = am_topics.topic_for(
            f'{joined} ' + ' '.join(t for t, _ in rows))
        marks = [m for _, m in rows]
        options = [t for t, _ in rows]
        scales = [s for u in units for s in u.scales]
        note = ('The scheme prices this ask step by step: '
                + ', '.join(str(m) for m in marks)
                + f' — {total} marks in all, in the order the scheme sets them out.')
        if scales:
            note += (' Marked on a systemic-error scale: the scheme prints '
                     + '; '.join(f'({s})' for s in scales)
                     + ', which is what the work is worth with one error, two, '
                       'and so on down to a valid attempt.')
        note += (' Penalties are subtractive: a mathematical error costs 3, a '
                 'slip or a misreading 1.')
        row = anyN(f'{card_id(self.year, self.level, key)}-r1', options[0],
                   total, len(options), marks[0], options, note,
                   steps=marks if len(set(marks)) > 1 else None)
        card = _card(card_id(self.year, self.level, key), self.year,
                     LEVEL_WORD[self.level], topic,
                     am_topics.concept_for(qtext), ref, qtext,
                     'step marks', total, [row],
                     notes=f'Cited from the {self.year} '
                           f'{LEVEL_WORD[self.level]} paper.',
                     stem=stem, tariff_kind='fixed', figure_key=figure)
        return card, matched


def plan(A, census_leaves):
    """[(key, [units], why)] — what to card, at the grain the reader earned.

    A part whose romans the reader accounted for exactly is carded roman by
    roman. A part where they do not agree with the PAPER is carded whole, and
    the card cites the part.
    """
    leaves = {(k[0], k[1], k[2]) for k in census_leaves}
    parts = collections.OrderedDict()
    for key, unit in A.S.units.items():
        parts.setdefault((key[0], key[1]), []).append((key, unit))
    out, coarse = [], 0
    for (q, letter), items in parts.items():
        want = {k for k in leaves if k[0] == q and k[1] == letter}
        got = {k for k, _ in items}
        if want and got == want:
            out.extend(((k, [u], 'exact') for k, u in items))
            continue
        if letter is None:
            # The scheme drops a part letter the PAPER prints. 2024 Ordinary
            # sets Q6 as "6(a)(i)...(iii)" and "6(b)"; its scheme heads the
            # three romans "6 (i)", "6 (ii)", "6 (iii)" with no letter at all,
            # so the reader's keys carry none and match no census leaf. Falling
            # through to the coarse grain then made ONE card for the whole of
            # Q6, and because (i) is answered by a drawn network the whole of
            # (ii) and (iii) went with it — two asks the scheme states in
            # words. The letter is not guessed: it is taken only when EXACTLY
            # ONE letter of this question in the paper has exactly the romans
            # the reader found, which is evidence and not a preference.
            romans = {k[2] for k, _ in items}
            named = [L for L in sorted({k[1] for k in leaves
                                        if k[0] == q and k[1]})
                     if {j[2] for j in leaves if j[0] == q and j[1] == L}
                     == romans]
            if len(named) == 1 and None not in romans:
                out.extend((((q, named[0], k[2]), [u], 'exact')
                            for k, u in items))
                continue
        # ONE unit cannot be ONE roman where the paper prints several. The
        # scheme reader keys a part it failed to split to the LAST roman it
        # saw, and that key is a real census leaf, so this branch carded it as
        # though it were exact: 2021 Higher Q9(b) came out citing (b)(iii) --
        # a five-mark ask -- while carrying all six of part (b)'s steps and
        # its running total of 30, with the paper's printed asks for (i) and
        # (ii) sitting inside the first marking point as though they were the
        # answer. 2021 Ordinary Q2(a)(iii) is the same shape at 30 against a
        # stated 15.
        #
        # The PAPER decides, as it decides everything here: `want` is what it
        # prints under this letter, and a lone unit against several printed
        # asks is a part the reader did not split, not a roman it read.
        if len(items) == 1 and items[0][0] in leaves and len(want) <= 1:
            out.append((items[0][0], [items[0][1]], 'exact'))
            continue
        out.append(((q, letter, None), [u for _, u in items], 'part'))
        coarse += 1
    return out, coarse


# The refusals that are a claim about the SCHEME rather than about the reader,
# and so belong in the exclusions ledger. Each maps to the sentence the ledger
# carries as its reason; the evidence is raised with the refusal.
EXCLUDING = {
    'the scheme answers this ask with a drawing':
        'the scheme answers this ask with a drawing and states no marking '
        'point for it at all',
    'a priced step states nothing liftable':
        'the scheme prices a step of this ask against a word that names the '
        'work rather than stating it, so part of the tariff has no marking '
        'point behind it',
}


def build():
    cards = []
    drawings = []
    refused = collections.Counter()
    examples = collections.defaultdict(list)
    stats = collections.Counter()
    from paper_census import census_subject
    census = census_subject(SUBJECT)
    by_paper = {(p['year'], p['level']): [tuple(l['key']) for l in p['leaves']]
                for p in census['papers']}
    census_text = {(p['year'], p['level']):
                   {tuple(l['key']): l.get('text') or '' for l in p['leaves']}
                   for p in census['papers']}
    for year in YEARS:
        for level in LEVELS:
            A = Author(year, level, census_text=census_text[(year, level)])
            todo, coarse = plan(A, by_paper[(year, level)])
            stats['part-grain cards'] += coarse
            for key, units, _why in todo:
                try:
                    card, matched = A.card(key, units, by_paper[(year, level)])
                except Refused as e:
                    reason, where = e.args[0][:2]
                    parts = [p for p in e.args[0][2:] if p]
                    refused[reason] += 1
                    examples[reason].append(where)
                    if parts and reason in EXCLUDING:
                        drawings.append({'ref': where,
                                         'reason': EXCLUDING[reason],
                                         'evidence': ' — '.join(parts)})
                    continue
                if not matched:
                    stats['filed by the paper\'s own default topic'] += 1
                cards.append(card)
    return cards, refused, examples, stats, census, drawings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--exclusions', action='store_true',
                    help='write exclusions/applied-maths.json and stop')
    args = ap.parse_args()
    cards, refused, examples, stats, census, drawings = build()
    problems = audit(cards)
    if args.exclusions:
        path = os.path.join(DIR, 'exclusions', f'{SUBJECT}.json')
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(drawings, fh, ensure_ascii=False, indent=1)
            fh.write('\n')
        print(f'wrote {len(drawings)} exclusion(s) to {path}')
        return 0
    if args.report:
        total = sum(p['leafCount'] for p in census['papers'])
        print(f'{len(cards)} card(s) against {total} paper asks '
              f'({100 * len(cards) / total:.1f}% by count)')
        rows = sum(len(r['group']['options']) for c in cards for r in c['rows'])
        marks = sum(c['totalMarks'] for c in cards)
        print(f'{rows} priced steps, {marks} marks')
        for k, v in sorted(stats.items()):
            print(f'   {v:4} {k}')
        by_topic = collections.Counter(c['topicId'] for c in cards)
        for tid, n in sorted(by_topic.items()):
            print(f'   {n:4} {am_topics.TOPIC_NAME.get(tid, tid)}')
        for reason, n in refused.most_common():
            print(f'   {n:4} REFUSED  {reason}')
            for e in examples[reason][:60 if args.all else 3]:
                print(f'             {e}')
        for p in problems:
            print(f'   AUDIT {p}')
        return 0
    for p in problems:
        print('AUDIT', p, file=sys.stderr)
    json.dump(cards, sys.stdout, ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
