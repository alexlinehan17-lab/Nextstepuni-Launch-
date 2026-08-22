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
    'chemistry': 'chem', 'economics': 'econ', 'home-economics': 'hem',
    'physics': 'phys',
}


# Decks differ in how they join a part onto its question: agsci writes
# agsci-2021-hl-q3bi, biology writes bio-2025-hl-q1-a. Follow each deck's own.
DASHED = {'biology'}


def part_id(subject, year, level, q, letter=None, roman=None, suffix=''):
    join = '-' if subject in DASHED else ''
    tail = ''.join(join + p for p in (letter, roman) if p)
    return (f'{ID_PREFIX[subject]}-{year}-{level}-q{q}{tail}'
            + (f'-{suffix}' if suffix else ''))


def part_ref(year, level, q, letter=None, roman=None):
    return (f'{year} {level.upper()} Q{q}'
            + (f'({letter})' if letter else '') + (f'({roman})' if roman else ''))


class Refused(Exception):
    """A card that would have shipped wrong."""


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
        self.scheme_pdf = SchemePdf(subject, year, level)
        self.cards = []

    def _source(self, source):
        if source not in ('md', 'pdf'):
            raise Refused(f'unknown scheme source {source!r} — use "md" or "pdf"')
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
             omit=(), source='md', card_id=None, from_run=None, tick=None):
        ref = part_ref(self.year, self.level, q, letter, roman)

        question = self.paper.text(q, letter, roman)
        if not question:
            raise Refused(f'{ref}: the paper has no text for this part')
        if self.paper.suspect(q, letter, roman) and not checked:
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
        if from_run is not None:
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
                candidates = [' '.join(taken)]
            else:
                if token_index >= len(tokens):
                    raise Refused(f'{ref}: run {run[point_index]!r} has no token '
                                  f'{token_index}')
                candidates = [tokens[token_index]]
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
