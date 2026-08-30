#!/usr/bin/env python3
"""Assemble Mark Bank cards, any subject, from the paper and the scheme.

The authoring scripts choose; this module refuses. What a caller supplies is
editorial — which part to card, which topic it belongs to, which of the
scheme's accepted answers to show, how the tariff is shaped. What a caller
cannot supply is the wording: question text comes from agsci_paper.Paper and
marking points come from agsci_scheme.Scheme, and card() will not accept a
string for either.

    A = Author('agricultural-science', 2021, 'hl')
    A.card(1, 'a', topic='agsci-1-1', concept='weed-identification',
           figure='agricultural-science-2021-HL-paper-p03-i0',
           labels={'A': 'Buttercup', 'B': 'Thistle', 'C': 'Dock (leaf)'})

It refuses, loudly and without writing anything, when:

  * the paper has no text for the part — nothing to ask;
  * the paper's text is suspect() and the caller has not passed
    checked='<why>' to say the page was opened and read;
  * any chosen marking point fails the build's own provenance gate;
  * the marks do not sum to the total the scheme prints.

Each refusal is a case where the alternative is a card that looks right and
is not, which is the only kind of defect this deck can actually ship.
"""
import re
import sys

from paper import Paper
from scheme import Scheme
from scheme_pdf import SchemePdf

ROMAN_ORDER = ['i', 'ii', 'iii', 'iv', 'v', 'vi']
# 'A = Buttercup', 'B: Graduated cylinder', 'C - Simmental'. The label is the
# paper's, the meaning is the scheme's, and deriving the pair from the marking
# point means neither is ever typed here.
LABELLED_POINT = re.compile(r'^([A-H])\s*[=:\u2010\u2013\u2014-]\s*(.+)$')


# Each deck already has an id convention and cards are keyed on it, so a new
# card has to be born under the same one rather than a tidier one.
ID_PREFIX = {
    'agricultural-science': 'agsci', 'biology': 'bio', 'business': 'bus',
    'chemistry': 'chem', 'economics': 'econ', 'home-economics': 'he',
    'physics': 'phys',
}


# Decks differ in how they join a part onto its question: agsci writes
# agsci-2021-hl-q3bi, biology writes bio-2025-hl-q1-a. Follow each deck's own.
DASHED = {'biology', 'chemistry'}
# Physics attaches the letter and dashes the roman: phys-2021-hl-q14c-v.
ROMAN_DASHED = {'physics'}


def part_id(subject, year, level, q, letter=None, roman=None, suffix=''):
    if subject in ROMAN_DASHED:
        tail = (letter or '') + (f'-{roman}' if roman else '')
    else:
        join = '-' if subject in DASHED else ''
        tail = ''.join(join + p for p in (letter, roman) if p)
    return (f'{ID_PREFIX[subject]}-{year}-{level}-q{q}{tail}'
            + (f'-{suffix}' if suffix else ''))


def part_ref(year, level, q, letter=None, roman=None):
    return (f'{year} {level.upper()} Q{q}'
            + (f'({letter})' if letter else '') + (f'({roman})' if roman else ''))


# A tariff, and nothing that merely looks like one. "[accept formula]" and
# "[accept covalent]" tell a student what else scores and stay on the card;
# "[H3O+]" is an answer. Only a bracket holding a mark expression comes off,
# plus the scheme's own "[accept partial answer for 3]", which is a tariff
# written out in words.
MARK_TAIL = re.compile(
    r'(?:\s*[\(\[]\s*\d+(?:\s*[×x+]\s*\d+)*\s*[\)\]]'
    r'|\s*\[\s*accept\s+partial\s+answer[^\]]*\])+\s*$', re.I)


def _unstar(text):
    """Drop the scheme's essential-answer asterisk from a marking point.

    It is an instruction to the examiner — award nothing for a near miss — not
    part of what a candidate writes. Agricultural Science prints it trailing
    ("Oilseed rape*") where the other subjects print it leading, and only the
    leading form was being removed.

    Cards that want the distinction on their face use the 'gate' row kind and say
    so in a note; this is for the ordinary case, where it is noise.
    """
    return text.strip().strip('*').strip()


class Refused(Exception):
    """A card that would have shipped wrong."""



class _TableSource:
    """chem_scheme.ChemScheme behind the interface Author expects of a scheme.

    Only points() differs: the 2024 and 2025 Chemistry schemes REPRINT the ask
    above its answer, at the same indent, so nothing in the geometry separates
    them. The paper's own wording does, and it is passed in here so the split
    is confirmed by a second document rather than guessed from layout.
    """

    def __init__(self, scheme, paper, md):
        self._scheme, self._paper, self._md = scheme, paper, md
        # The build's provenance gate reads the MARKDOWN scheme, so that is
        # what a claim lifted from the PDF has to be checked against -- and it
        # is the right check: text the two documents disagree about should not
        # ship. normalise() folds super and subscript digits, so "20.0 cm³"
        # matches the markdown's "20.0 cm3".
        self.path = md.path

    def points(self, q, letter=None, roman=None):
        try:
            ask = self._paper.text(q, letter, roman) or ''
        except Exception:                                    # noqa: BLE001
            ask = ''
        return self._scheme.marking_points(q, letter, roman, ask=ask)

    def marks(self, q, letter=None, roman=None):
        return self._scheme.marks(q, letter, roman)

    def asides(self, q, letter=None, roman=None):
        return self._scheme.asides(q, letter, roman)

    def tariff(self, q, letter=None, roman=None, rows=None):
        return self._scheme.tariff(q, letter, roman, rows=rows)

    def verify(self, claims):
        return self._md.verify(claims)

    def paths(self):
        return self._scheme.parts()

ROMAN_ORDER = {r: i for i, r in enumerate(
    ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii'])}



class _CsSource:
    """cs_scheme.CsScheme behind the interface Author expects of a scheme.

    points() returns the scheme's marking points with the credit BANDS already
    removed -- "Very good explanation - clear understanding demonstrated" is
    the rubric, and a card built from it would tell a student how they were
    graded rather than what the answer was.
    """

    def __init__(self, scheme, md):
        self._scheme, self._md = scheme, md
        # The build's provenance gate reads the MARKDOWN scheme, so a claim
        # lifted from the PDF is checked against that.
        self.path = md.path

    def points(self, q, letter=None, roman=None):
        own = self._scheme.points(q, letter, roman)
        if own or letter is not None or roman is not None:
            return own
        # A whole-question key whose answers are printed under its PARTS.
        # Computer Science prices Section A at the question ("5 marks") and
        # then states the answer under (a) and (b), so a card citing the
        # question has to gather what its parts hold. Still the scheme's own
        # text, in the scheme's own order.
        out = []
        for k in self._scheme.parts():
            if k[0] == q and (k[1] is not None or k[2] is not None):
                out.extend(self._scheme.points(*k))
        return out

    def marks(self, q, letter=None, roman=None):
        t = self._scheme.tariff(q, letter, roman)
        return [t] if t else []

    def tariff(self, q, letter=None, roman=None):
        return self._scheme.tariff(q, letter, roman)

    def bands(self, q, letter=None, roman=None):
        return self._scheme.bands(q, letter, roman)

    def verify(self, claims):
        return self._md.verify(claims)

    def paths(self):
        return self._scheme.parts()

PAPER_TERMINAL = re.compile(r'[.?!]$')


def _without_listing(question, lines, strict=False):
    """The question text with the crop's own lines removed.

    A PROGRAM is a contiguous run of monospaced lines and occurs once, so the
    first place its opening line is found is where it starts. A TABLE's labels
    are ordinary words that also appear in the question's own sentence --
    "shown in Figure 7", "in Column A" -- so cutting at the first match left
    "Complete the truth table for the AND logic gate, shown in". Strict mode
    is for those: it tries every place the first label occurs, wants a run of
    at least three labels, and accepts a cut only when what remains still ends
    like a sentence. Where nothing satisfies that, it declines and the part
    stays flagged for a person to look at.
    """
    q = ' '.join(question.split())
    toks = [' '.join(t.split()) for t in lines]
    toks = [t for t in toks if len(t) >= 3]
    if not toks:
        return None
    starts = []
    at = q.find(toks[0])
    while at > 0:
        starts.append(at)
        if not strict:
            break
        at = q.find(toks[0], at + 1)
    for lo in starts:
        out = _cut(q, toks, lo, strict)
        if out:
            return out
    return None


def _cut(q, toks, lo, strict):
    cur = lo + len(toks[0])
    run = 1
    for t in toks[1:]:
        i = q.find(t, cur)
        # 14 characters of slack: a blank line in the listing shows up as its
        # bare line numbers ("3 4") between two lines of code.
        if i < 0 or i - cur > 14:
            continue
        cur = i + len(t)
        run += 1
    if strict and run < 3:
        return None
    head = re.sub(r'[\s\d]+$', '', q[:lo].rstrip())
    tail = re.sub(r'^[\s\d]+', '', q[cur:].lstrip())
    out = ' '.join(f'{head} {tail}'.split())
    # What is left has to still be a question. 2023 HL Q3 matched a crop line
    # against the fourth character of its text and the "removal" reduced the
    # whole ask to "(a)". Taking the listing out may shorten a question; it
    # may not empty it.
    if len(out) < 25 or len(out.split()) < 5:
        return None
    if strict and not PAPER_TERMINAL.search(out):
        return None
    return out


class Author:
    def __init__(self, subject, year, level):
        level = {'higher': 'hl', 'ordinary': 'ol'}.get(level, level)
        self.subject = subject
        self.year, self.level = year, level
        self.long_level = 'higher' if level == 'hl' else 'ordinary'
        self.paper = Paper(subject, year, level)
        self.scheme = Scheme(subject, year, level)
        # The PDF-backed parser, for parts the flattened markdown mangles. See
        # agsci_scheme_pdf: neither parser dominates, so the choice is per part.
        # Tolerated, not required: SchemePdf raises UnboundLocalError on the
        # Computer Science schemes, and that subject reads its own table
        # through cs_scheme instead. A parser that cannot open a subject must
        # not stop the subject being authored.
        try:
            self.scheme_pdf = SchemePdf(subject, year, level)
        except Exception:                                    # noqa: BLE001
            self.scheme_pdf = None
        # Chemistry's schemes are a five-column table that neither generic
        # parser reads correctly. chem_scheme keys the table the way the PAPER
        # numbers it and reads its super/subscripts from the baseline, which is
        # what an ion charge depends on. Offered as source='table'.
        self.scheme_table = None
        if subject == 'chemistry':
            from chem_scheme import ChemScheme
            self.scheme_table = _TableSource(ChemScheme(year, level),
                                             self.paper, self.scheme)
        elif subject == 'computer-science':
            from cs_scheme import CsScheme
            self.scheme_table = _CsSource(CsScheme(year, level), self.scheme)
        self.cards = []

    def _source(self, source):
        if source == 'table':
            if self.scheme_table is None:
                raise Refused('source="table" is Chemistry only')
            return self.scheme_table
        if source not in ('md', 'pdf'):
            raise Refused(f'unknown scheme source {source!r} — use "md", "pdf" '
                          f'or "table"')
        return self.scheme_pdf if source == 'pdf' else self.scheme

    # -- the scheme's offer, for deciding what to card -----------------------
    def offer(self, q, letter=None, roman=None, source='md'):
        """What the two documents hold for this part. Printing aid, not a card."""
        scheme = self._source(source)
        pts = scheme.points(q, letter, roman)
        ok, _ = scheme.verify(pts)
        ok = set(ok)
        # Indexed over EVERY candidate, traceable or not, because card()'s `use`
        # indexes the same list. Numbering only the traceable ones would silently
        # shift every index past the first untraceable point.
        return {
            'ref': part_ref(self.year, self.level, q, letter, roman),
            'question': self.paper.text(q, letter, roman),
            'suspect': self.paper.suspect(q, letter, roman),
            'stem': self.paper.stem(q, letter) or self.paper.stem(q),
            'marks': scheme.marks(q, letter, roman) or self.scheme.marks(q, letter, roman),
            'points': [(i, p, p in ok) for i, p in enumerate(pts)],
            'usable': sum(1 for p in pts if p in ok),
        }

    def card(self, q, letter=None, roman=None, *, topic, concept,
             use=None, marks=None, tariff='fixed', total=None, figure=None,
             labels=None, notes=None, stem=True, checked=None, suffix='',
             row_kind='point', notation=None, spread=False, context=None,
             omit=(), source='md', card_id=None, from_run=None, from_runs=None,
             tick=None, first_sentence=False, ladder=None, listing=(),
             printed=()):
        ref = part_ref(self.year, self.level, q, letter, roman)

        question = self.paper.text(q, letter, roman)

        # A part that is only a CUE hands its ask to the romans beneath it:
        # 2021 OL Chemistry Q9(c) reads "From your graph find" and (i) and (ii)
        # complete the sentence. A card citing the parent has to carry what the
        # parent actually asks, so the children are joined onto it -- still the
        # paper's own words, in the paper's own order. Only where the part
        # cannot stand on its own; a part with a real question of its own keeps
        # it, and a card citing a CHILD is untouched.
        # Tested BEFORE the empty check, not after: a question that states
        # nothing of its own is exactly the case that needs its children.
        # Computer Science prices Section A at the question and prints the ask
        # only under (a) and (b), so the parent's own text is empty and a card
        # citing the question was refused for having no question text at all.
        if roman is None and len(' '.join((question or '').split())) < 40:
            kids = [k for k in self.paper.parts
                    if k[0] == q
                    and (k[1] == letter if letter else k[1] is not None or k[2])
                    and (k[1], k[2]) != (letter, roman)]
            if kids:
                kids.sort(key=lambda k: (k[1] or '', ROMAN_ORDER.get(k[2], 99)))
                tail = ' '.join(
                    f'({k[2] or k[1]}) {(self.paper.text(*k) or "").strip()}'
                    for k in kids)
                if tail.strip():
                    question = f'{(question or "").rstrip()} {tail}'.strip()

        # A PROGRAM the crop carries, taken back out of the question text.
        # Computer Science prints its listings inside the question block, and
        # the text layer returns them run into the prose: "What is the output
        # of the following piece of Python code? 1 x = 3 2 print("x is", x)".
        # Where a figure carries that listing, the card's question is the ask
        # without it -- the paper's own words either side, nothing rewritten,
        # and the code shown as the paper set it rather than as a text layer
        # mangled it. The lines are matched IN ORDER from the first one found,
        # so a fragment that also occurs in the prose cannot start the cut.
        listing_removed = False
        if listing and question:
            without = _without_listing(question, listing)
            if without:
                question, listing_removed = without, True
        if printed and question:
            without = _without_listing(question, printed, strict=True)
            if without:
                question, listing_removed = without, True

        if not question:
            raise Refused(f'{ref}: the paper has no text for this part')

        # Where a paper sets two questions side by side, the block segmentation
        # welds the neighbour's text onto this one: 2023 OL Q2(c) comes out as
        # "Data always involves numbers. Three bases together are known as a
        # ………". The statement is the first sentence — but rather than trust
        # that, the trimmed text has to appear in the marking scheme, which
        # prints these statements as well. A second document confirming it is
        # what separates a trim from a guess, so an unconfirmed one is refused.
        if first_sentence:
            trimmed = re.split(r'(?<=[.?!])\s+', question)[0].strip()
            with open(self.scheme.path, encoding='utf-8', errors='ignore') as fh:
                scheme_text = ' '.join(fh.read().split()).lower()
            if trimmed.rstrip('.').lower() not in scheme_text:
                raise Refused(f'{ref}: first sentence {trimmed[:60]!r} does not appear '
                              f'in the scheme, so the trim is unconfirmed')
            question = trimmed

        # The flag is raised on what the paper block held; a scheme-confirmed
        # trim answers it, so the check runs on the text the card will carry.
        # The flag is raised on what the paper BLOCK held. Where the crop has
        # taken the listing back out, the text the card carries is a different
        # string, and it answers the flag on its own terms if it now ends in a
        # full stop: what made it look truncated was the program running off
        # its end.
        flagged = self.paper.suspect(q, letter, roman)
        if flagged and listing_removed and PAPER_TERMINAL.search(question.strip()):
            flagged = False
        if not first_sentence and flagged and not checked:
            raise Refused(
                f'{ref}: question text is flagged and unreviewed — {question!r}. '
                f'Open the page; if it is right, pass checked="<why>".')

        scheme = self._source(source)

        # A tick in a True/False column is an answer the text layer does not
        # carry: the glyph leaves an empty block behind, so no parser can read
        # it and the marking points for the NEXT question get attributed here
        # instead. The answer is read off the rendered scheme page and named
        # here, which is the same standing as reading a figure — the scheme
        # states it, just graphically. Both words appear in the scheme's own
        # column headings, so the provenance gate still checks it, and the note
        # says on the card's face where the answer came from.
        if tick is not None:
            if tick not in ('True', 'False'):
                raise Refused(f'{ref}: tick must be "True" or "False", not {tick!r}')
            if not notes:
                raise Refused(f'{ref}: a tick-read answer needs a note saying so')
            candidates = [tick]
            use = [0]
            scheme = self.scheme_pdf

        # Some parts have their answers printed as one positional run against
        # the parent, because the scheme set them as a table: 2022 OL Q4(b) has
        # five true/false statements and prints "False True True False False"
        # once, with the roman markers in a neighbouring cell. from_run names
        # the parent part, which of its points holds the run, and which token in
        # that run belongs to this part. A slice takes a span of words instead
        # of one, for the commoner case where the scheme's answer simply runs on
        # from the tail of its own question cue — "Explain the underlined term.
        # Produce many offspring". The words are still lifted from the scheme;
        # only where the cue stops and the answer starts is read off the page.
        # Several marking points can share one line of the scheme: 2024 HL
        # Physics prints "slope formula [3] R = 7.03 Ω [2]" as a single point,
        # which is two rows on a card. from_runs takes a slice per row.
        if from_runs is not None:
            if from_run is not None:
                raise Refused(f'{ref}: pass from_run or from_runs, not both')
            candidates = []
            for parent, point_index, token_index in from_runs:
                run = scheme.points(*parent)
                if point_index >= len(run):
                    raise Refused(f'{ref}: parent {parent} has no point {point_index}')
                taken = run[point_index].split()[token_index]
                if not taken:
                    raise Refused(f'{ref}: run {run[point_index]!r} yields nothing '
                                  f'for {token_index}')
                candidates.append(_unstar(' '.join(taken)))
            use = list(range(len(candidates))) if use is None else use
        elif from_run is not None:
            parent, point_index, token_index = from_run
            run = scheme.points(*parent)
            if point_index >= len(run):
                raise Refused(f'{ref}: parent {parent} has no point {point_index}')
            tokens = run[point_index].split()
            if isinstance(token_index, slice):
                taken = tokens[token_index]
                if not taken:
                    raise Refused(f'{ref}: run {run[point_index]!r} yields nothing '
                                  f'for {token_index}')
                # The scheme marks an essential answer with a leading asterisk;
                # it is an annotation to the examiner, not part of the answer,
                # and no card in any deck carries one.
                candidates = [_unstar(' '.join(taken))]
            else:
                if token_index >= len(tokens):
                    raise Refused(f'{ref}: run {run[point_index]!r} has no token '
                                  f'{token_index}')
                candidates = [_unstar(tokens[token_index])]
            use = [0] if use is None else use
        elif tick is None:
            candidates = scheme.points(q, letter, roman)
        if not candidates:
            raise Refused(f'{ref}: the scheme has no marking points for this part')
        # An entry in `use` may be an index, or a list of indices meaning "this
        # answer, and the scheme's alternatives for it" — which becomes one alt
        # row carrying its accepts, not several rows worth marks each.
        picks = list(range(len(candidates))) if use is None else list(use)
        groups = [[candidates[i] for i in (p if isinstance(p, (list, tuple)) else [p])]
                  for p in picks]
        # The PDF scheme leaves the tariff inline — "d indicated (3)", "hot
        # cathode [6] [accept partial answer for 3]" — while the markdown one
        # keeps it in a column of its own. A card carries the answer and its
        # marks separately, and no card in any deck has ever shown a tariff
        # inside its answer text, so the annotation comes off here rather than
        # every caller slicing it away by hand. Only a bracket whose whole
        # content is a mark expression is taken, which is what keeps the "(m2)"
        # in "area = 4.52 × 10–6 (m2)" where it belongs.
        groups = [[MARK_TAIL.sub('', c).strip() or c for c in g] for g in groups]
        chosen = [g[0] for g in groups]
        if not chosen:
            raise Refused(f'{ref}: no marking points chosen')

        ok, bad = scheme.verify(chosen)
        if bad:
            raise Refused(f'{ref}: {len(bad)} marking point(s) do not trace to the '
                          f'scheme: {bad[0][:90]!r}')

        # Marks come from whichever parser found them: the PDF one keeps table
        # cells intact but often leaves the right-aligned tariff in a block of
        # its own that belongs to a neighbouring part.
        # A sliding scale is not a per-part mark. Biology's Ordinary Level
        # Section A prints one ladder for a whole question — "Q1 (a)-(e) Number
        # of correct responses 1 2 3 4 5 / Mark 7 14 16 18 20" — so no part of it
        # has a mark of its own. The deck's shape for that is a row carrying no
        # mark, the ladder written into the notation, and totalMarks set to what
        # the first correct response is worth. `ladder` says so explicitly, so
        # that a part with no printed tariff is never quietly given one.
        if ladder is not None:
            if not notation:
                raise Refused(f'{ref}: ladder needs a notation giving the scale')
            marks = [None] * len(chosen)

        scheme_marks = scheme.marks(q, letter, roman) or self.scheme.marks(q, letter, roman)
        if marks is None:
            numeric = [int(m) for m in scheme_marks if re.fullmatch(r'\d{1,2}', m)]
            if len(numeric) != len(chosen):
                raise Refused(
                    f'{ref}: the scheme prints marks {scheme_marks} but {len(chosen)} '
                    f'point(s) were chosen — pass marks=[...] to say how they split')
            marks = numeric
        if len(marks) != len(chosen):
            raise Refused(f'{ref}: {len(marks)} marks for {len(chosen)} points')

        if ladder is not None:
            computed = ladder
        else:
            computed = sum(marks)
            if total is not None and total != computed:
                raise Refused(f'{ref}: marks sum to {computed}, not the {total} given')

        # 'spread' is the 2(2) shape: the scheme prints more ways than the
        # question asks for, any of them scores, so every row carries the ones
        # the card did not put on its own line.
        shown = {c for g in groups for c in g}
        dropped = {candidates[i] for i in omit}
        spare = ([c for c in candidates if c not in shown and c not in dropped]
                 if spread else [])

        # An 'accepts' entry is answer text a student will read, but the build
        # gates only 'verbatim' — so nothing downstream would catch a bad one.
        # Gated here instead: an alternative that does not trace is dropped and
        # reported, rather than failing the card the way a bad verbatim does.
        extra = [c for g in groups for c in g[1:]] + spare
        if extra:
            fine, unusable = scheme.verify(extra)
            if unusable:
                print(f'  {ref}: dropped {len(unusable)} untraceable alternative(s)',
                      file=sys.stderr)
                fine = set(fine)
                groups = [[g[0]] + [c for c in g[1:] if c in fine] for g in groups]
                spare = [c for c in spare if c in fine]

        rows = []
        for i, (group, m) in enumerate(zip(groups, marks), start=1):
            row = {'id': f'r-{i}',
                   'kind': 'alt' if len(group) > 1 and not spread else row_kind,
                   'verbatim': group[0], 'marks': m}
            accepts = group[1:] + spare
            if accepts:
                row['accepts'] = accepts
            if i == 1 and context:
                row['contextNote'] = context
            rows.append(row)

        card = {
            'id': card_id or part_id(self.subject, self.year, self.level, q, letter, roman, suffix),
            'topicId': topic,
            'conceptId': concept,
            'level': self.long_level,
            'year': self.year,
            'subjectId': self.subject,
            'section': 'A' if q <= 12 else 'B',
            'questionRef': ref,
            'questionText': question,
            'tariffModel': ({'kind': tariff, 'notation': notation} if notation
                            else {'kind': tariff}),
            'totalMarks': computed,
            'rows': rows,
        }
        if stem:
            text = self.paper.stem(q, letter) or self.paper.stem(q)
            # The crop carries the listing here too. A shared stem is where a
            # printed table most often ends up -- 2021 OL Q15's stem came out
            # as "Figure 7 INPUTS OUTPUTS A B A OR B 0 0 0 1 1 0 1 1", which
            # card lint reports as label junk and a student reads as noise.
            if listing and text:
                text = _without_listing(text, listing) or text
            if printed and text:
                text = _without_listing(text, printed, strict=True) or text
            if text:
                card['stem'] = text
        if notes:
            card['notes'] = notes
        if figure:
            card['figureKey'] = figure
        if labels == 'auto':
            labels = {}
            for point in chosen:
                m = LABELLED_POINT.match(point)
                if m:
                    labels.setdefault(m.group(1), m.group(2).strip())
            if not labels:
                raise Refused(f'{ref}: labels="auto" but no marking point carries '
                              f'a label — pass the letters explicitly or drop it')
        if labels:
            card['labelKey'] = [
                {'letter': k, 'meaning': v, 'askedInThisQuestion': True}
                if isinstance(v, str) else dict(letter=k, **v)
                for k, v in labels.items()]
        self.cards.append(card)
        return card

    def emit(self):
        import json
        import sys
        json.dump(self.cards, sys.stdout, ensure_ascii=False, indent=1)
