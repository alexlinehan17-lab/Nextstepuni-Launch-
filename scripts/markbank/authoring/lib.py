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

class _EngSource:
    """eng_scheme.EngScheme behind the interface Author expects of a scheme.

    The Engineering scheme is read off the page, but the build's provenance
    gate reads the MARKDOWN extraction, so verify() is answered by the
    markdown as it is for every other subject: a claim lifted from the PDF has
    to appear in the document the gate checks against.
    """

    def __init__(self, scheme, md):
        self._scheme, self._md = scheme, md
        self.path = md.path

    def points(self, q, letter=None, roman=None):
        # Everything at this key and beneath it, because that is what the key's
        # tariff prices. `use` indexes into THIS list, so the author and the
        # card must be reading the same one.
        return self._scheme.points_under(q, letter, roman)

    def marks(self, q, letter=None, roman=None):
        t = self._scheme.tariff(q, letter, roman)
        return [str(t)] if t else []

    def verify(self, claims):
        return self._md.verify(claims)

    def paths(self):
        return list(self._scheme.body())


PAPER_TERMINAL = re.compile(r'[.?!]$')
# The page's own furniture, swept into a question block by the reader. A bare
# "Figure 3" at the end is the CAPTION of the picture printed beside the ask,
# not part of it; "Section B Long Questions 76 marks" is the banner of the
# section that starts underneath; and "This question continues on the next
# page" is an instruction to the candidate about the paper.
CONTINUES = re.compile(r'\s*This question continues on the next page\.?', re.I)
# A run of bare capitals on the end of an ask: the arrows printed on the
# picture beside it, swept into the block. 2022 Ordinary Q4(b) comes out as
# "Describe the purpose of any three of the following in manual metal arc
# welding: A B" -- A and B label the oxy-acetylene torch drawn above, for the
# part before it. Taken off only where what remains ends on the COLON that
# hands the ask to the children, which is the same self-check the furniture
# strip below uses, and only two parts in the subject satisfy it.
CALLOUT_TAIL = re.compile(r'(?:\s+[A-Z])+\s*$')
# What makes a line an instruction rather than a list item. Used to tell a
# roman that ASKS something from one that is only a term in a list.
COMMAND = re.compile(
    r'\b(?:answer|briefly|calculate|compare|complete|define|describe'
    r'|determine|differentiate|discuss|distinguish|draw|explain|give'
    r'|identify|indicate|label|list|name|outline|select|sketch|state'
    r'|suggest)\b', re.I)
TRAILING_FURNITURE = re.compile(
    r'(?:\s*(?:Figures?|Figs?\.?)\s*\d+[a-z]?)+\s*$'
    r'|\s*Section\s+[A-C]\b[^.]{0,60}?\d{1,3}\s*marks?\s*$'
    # The LETTERS printed under the pictures the ask names, swept onto the end
    # of it: 2023 OL Q5(a)(i) reads "Name the three plastic manufacturing
    # processes shown at A, B and C." on the page, with A, B and C set under
    # the three drawings beneath it, and the reader returns "... at A, B and
    # C. A B C". Bare capitals with nothing between them are never a sentence,
    # and the self-check below keeps the strip to the ones that leave a
    # finished question behind. Case-sensitive inside the case-insensitive
    # pattern, because a lower-case letter on a diagram is a quantity and a
    # question may well end on one.
    r'|(?-i:(?:\s+[A-H]){2,})\s*$', re.I)

# Which subjects get the question-text handling below. It is deliberately an
# ALLOWLIST rather than a default. The work it does -- taking the page's
# furniture off the end of an ask, joining a cue's children across letters as
# well as romans -- was written for Engineering and would silently rewrite the
# question text on every Biology, Chemistry and Physics card already shipped.
# A subject joins this list when its deck has been regenerated and diffed.
QUESTION_CLEANING = ('engineering',)


def _without_furniture(text):
    """The question with the page's furniture off its end, or None.

    Self-checking, the same way the table cut is: the strip is taken only
    where what remains still ends like a sentence. That is what separates a
    caption swept onto the end of the ask from a question that genuinely ends
    by naming a figure.
    """
    q = ' '.join(CONTINUES.sub(' ', text).split())
    for _ in range(4):
        stripped = TRAILING_FURNITURE.sub('', q).strip()
        if stripped == q:
            break
        q = stripped
    q = ' '.join(q.split())
    if q == ' '.join(text.split()) or len(q) < 25 or len(q.split()) < 5:
        return None
    return q if PAPER_TERMINAL.search(q) else None


# What separates an ask from a list item is not its LENGTH. "Explain the term
# bioplastic." is 28 characters and is the whole question; "Ferdinand Porsche"
# is 17 and is one of three names under "Outline the contribution made by each
# of the following". Refusing everything short refused 256 leaves, among them
# every short imperative in the subject.
#
# The command word is the real signal, and it is DERIVED rather than invented:
# these are the words that open the 550 census leaves too long to be anything
# but an ask, minus the stems that came with them ("nominal", "the", "using"),
# plus sketch/label/indicate, which open one ask each and are imperative in
# the same way. "Select" is excluded -- it opens "Select any two from the
# following", which is a lead-in to options rather than an ask.
#
# It lives here rather than in eng_all because both modules decide the same
# question with it: eng_all, whether a census leaf is an ask at all; card(),
# whether a part can stand on its own or takes the cue printed above it.
COMMAND_WORD = re.compile(
    r'^(?:briefly|calculate|compare|define|describe|determine|differentiate'
    r'|discuss|distinguish|draw|explain|give|identify|indicate|label|list'
    r'|name|outline|sketch|state|suggest)\b', re.I)

# What is left of a question head once the reader has taken the number off it.
# Engineering prints "Question 1. (50 marks)", the head match stops at the
# number, and the remainder is handed to the stem.
STEM_HEAD = re.compile(r'^\s*\.?\s*\(\s*\d{1,3}\s*marks?\s*\)\s*', re.I)
# Six or more numbers in a row: the DATA a question works from, printed above
# it. "Load (kN) 22 44 66 80 89 100 110 Extension (mm) 0.1 0.2 ..." is the
# table the candidate plots and belongs on the card. Mirrors cardlint's
# INLINE_TABLE, which is what decides the same question at lint time.
STEM_TABLE = re.compile(r'(?:\b\d[\d.,/]*\b[^\w]{0,4}){6,}')


# What follows a cue's colon, when the cue is the whole printed ask and the
# options are printed as parts of their own beneath it.
CUE_TAIL = re.compile(r'^(.*:)\s+([^:.?!]+)$', re.S)


def _without_caption(text):
    """The ask with a caption swept onto the end of its cue taken off.

    A cue's COLON is where the printed ask stops: the paper prints the options
    below it as parts of their own. Anything after the colon with no sentence
    in it is the caption of the artwork printed between the cue and its
    options, and the block reader swept it in:

        "... answer each of the following: A B C"        <- the furnace labels
        "... any two of the alloys listed below:            <- the wheelchair's
             rotary handrail seat cover frame"                 own callouts

    Five parts in the whole subject match, and all five are that. The guards
    are what keep a real ask out: a tail that opens with a command word is the
    next question, a tail with a marker in it is the options themselves
    printed inline, and a tail with terminal punctuation is a sentence.

    Returns None where nothing is taken, like _without_furniture.
    """
    m = CUE_TAIL.match(' '.join((text or '').split()))
    if not m:
        return None
    head, tail = m.group(1).strip(), m.group(2).strip()
    if len(tail.split()) > 8 or '(' in tail or COMMAND_WORD.match(tail):
        return None
    return head if len(head.split()) >= 5 else None


def _clean_stem(text):
    """The stimulus prose, with the page's furniture off it — or '' if none.

    Two faults, both of them the reader's and both visible on every Engineering
    deck. The head remnant above reached 227 cards, 148 of which carried a stem
    of ". (50 marks)" and nothing else. And a PART-level stem is often the
    caption of the picture printed beside the part ABOVE it: "chain and
    sprocket" stood over "Name two forms of renewable energy", "tool A" over
    "State one example of a ferrous metal", and the paper's running header --
    "Leaving Certificate - Higher Level ... Thursday 10 June Morning" -- over
    two more.

    What separates stimulus from furniture is the same test the figure rule
    already uses: a real stem is a SENTENCE or a cue and closes on punctuation,
    a caption closes on nothing. A table of numbers is the exception, because
    it is the data the ask works from and the card has to carry it.

    Engineering only, through QUESTION_CLEANING: every other subject's deck was
    generated before this existed and would be silently rewritten by it.
    """
    t = ' '.join(STEM_HEAD.sub('', text or '').split())
    if not t:
        return ''
    if re.search(r'[.?!:]$', t) or STEM_TABLE.search(t):
        return t
    return ''


ROMAN_ORDER = {r: i for i, r in enumerate(
    ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii'])}


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
        # Tolerated, not required: a parser that cannot open a subject must
        # not stop the subject being authored. Engineering's schemes are among
        # those SchemePdf raises on.
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
        elif subject == 'engineering':
            # Engineering's scheme is read off the page by eng_scheme, and the
            # adapter above puts it behind the interface Author expects.
            from eng_scheme import EngScheme
            self.scheme_table = _EngSource(EngScheme(year, level), self.scheme)
        self.cards = []

    def _source(self, source):
        if source == 'table':
            if self.scheme_table is None:
                raise Refused(f'source="table" has no reader for {self.subject}')
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
             question_figure=None,
             labels=None, notes=None, stem=True, checked=None, suffix='',
             row_kind='point', notation=None, spread=False, context=None,
             omit=(), source='md', card_id=None, from_run=None, from_runs=None,
             tick=None, first_sentence=False, ladder=None):
        ref = part_ref(self.year, self.level, q, letter, roman)

        clean = self.subject in QUESTION_CLEANING
        question = self.paper.text(q, letter, roman)
        if not clean and not question:
            raise Refused(f'{ref}: the paper has no text for this part')

        # A part that is only a CUE hands its ask to the romans beneath it:
        # 2021 OL Chemistry Q9(c) reads "From your graph find" and (i) and (ii)
        # complete the sentence. A card citing the parent has to carry what the
        # parent actually asks, so the children are joined onto it -- still the
        # paper's own words, in the paper's own order. Only where the part
        # cannot stand on its own; a part with a real question of its own keeps
        # it, and a card citing a CHILD is untouched.
        # For a cleaning subject the empty check runs AFTER this, not before:
        # a question that states nothing of its own is exactly the case that
        # needs its children, and the widened key takes lettered parts as well
        # as romans. Both are Engineering's; every other subject keeps the
        # narrow rule it was authored against.
        # A ROMAN that is only a list ITEM needs the instruction printed above
        # it. 2022 HL Q5(c) reads "Select any two from (i), (ii) or (iii)
        # below and explain:" and its (i) is "The impact of a dislocation in
        # crystal structures." -- a noun phrase, with no verb anywhere. On a
        # card of its own that is not a question, and the deck shipping today
        # carries the joined form: this is the rule those cards were generated
        # with on markbank/maths-review-2, restored with them.
        if clean and roman is not None and question:
            _own = ' '.join(question.split())
            if not COMMAND.match(_own):
                try:
                    _up = ' '.join((self.paper.text(q, letter, None)
                                    or '').split())
                except Exception:                            # noqa: BLE001
                    _up = ''
                if _up.endswith(':') and COMMAND.search(_up):
                    question = f'{_up} {_own}'

        # LENGTH is a proxy for "cannot stand on its own", and on these papers
        # it is the wrong one. "Explain any two of the following processes:" is
        # 43 characters and states no processes; "Describe how to carry out
        # each of the following heat treatment processes:" is 73 and states no
        # processes either. Both close on a COLON, which is the paper saying
        # outright that the list comes next -- and it is the same colon
        # Paper.suspect() flags the part for. So a cleaning subject reads the
        # punctuation instead of the character count, and the flag then answers
        # itself below, exactly as the joined_kids rule already intends. The
        # colon is not always the last character: 2025 HL Q9(b) reads "Answer
        # any three of the following: inspection robot", the lead-in with the
        # first item already run onto it.
        #
        # Read only for a cleaning subject, because every other deck was
        # authored against the length test and widening it would rewrite the
        # question text on cards already shipped.
        cue = ' '.join((question or '').split())
        # Two things come off the end BEFORE the join, not after, because a cue
        # whose colon has something stuck to it does not look like a cue and
        # the join then never fires: a caption swept in from the page, and a
        # run of bare capitals that label the picture beside the ask -- 2022
        # Ordinary Q4(b) comes out as "...in manual metal arc welding: A B",
        # where A and B label the torch drawn above, for the part before it.
        # Each is taken only where what remains still ends on the colon, which
        # is the same self-check the furniture strip uses.
        furniture_removed = False
        if clean and roman is None:
            trimmed = _without_caption(cue)
            if trimmed:
                question, cue, furniture_removed = trimmed, trimmed, True
            _t = CALLOUT_TAIL.sub('', cue)
            if _t != cue and _t.endswith(':'):
                question, cue, furniture_removed = _t, _t, True
        joined_kids = False
        # A question that does not end like a SENTENCE has not finished being
        # asked — which is the same thing paper.suspect() flags it for — so
        # the terminal test subsumes the colon and covers the shapes that end
        # on neither: "Explain any three of the following furnace-related
        # terms:", and the drawbacks question that runs two sentences before
        # its colon.
        hands_over = len(cue) < 40 or (
            clean and (cue.endswith(':')
                       or re.search(r'\bfollowing\s*:', cue)
                       or not PAPER_TERMINAL.search(cue)))
        if roman is None and hands_over:
            if clean:
                kids = [k for k in self.paper.parts
                        if k[0] == q
                        and (k[1] == letter if letter
                             else k[1] is not None or k[2])
                        and (k[1], k[2]) != (letter, roman)]
            else:
                kids = [k for k in self.paper.parts
                        if k[0] == q and k[1] == letter and k[2]]
            if kids:
                kids.sort(key=lambda k: ((k[1] or '') if clean else '',
                                         ROMAN_ORDER.get(k[2], 99)))
                if clean:
                    tail = ' '.join(
                        f'({k[2] or k[1]}) {(self.paper.text(*k) or "").strip()}'
                        for k in kids)
                else:
                    tail = ' '.join(
                        f'({k[2]}) {(self.paper.text(*k) or "").strip()}'
                        for k in kids)
                if tail.strip():
                    question = f'{(question or "").rstrip()} {tail}'.strip()
                    joined_kids = True
        elif clean and roman is not None and cue and not COMMAND_WORD.match(cue):
            # And the mirror of it. "Select any two from (i), (ii) or (iii)
            # below and explain the difference between the terms in each:" is
            # the ask; (iii) is "Upper critical temperature (UCT) and lower
            # critical temperature (LCT)." and asks nothing on its own. A card
            # citing the ROMAN has to carry the cue above it or it shows the
            # student two terms and no instruction.
            #
            # What decides it is the command word, not the length, and the
            # shipped deck is the evidence: of the 116 roman cards whose parent
            # closes on a colon, this rule agrees with 115 -- every child that
            # opens with a command word stands alone in the deck, and every
            # child that does not carries its parent's cue. The one exception
            # is a card whose text an OR-branch merge had already garbled.
            above = ' '.join((self.paper.text(q, letter, None) or '').split())
            if above.endswith(':'):
                question = f'{above} {cue}'
                joined_kids = True

        # The page's own furniture, taken back off the end of the ask.
        if clean and question:
            without = _without_furniture(question)
            if without:
                question, furniture_removed = without, True

        if clean and not question:
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
        # The flag is raised on what the paper BLOCK held. Where the children
        # have been joined on, or the furniture taken off, the text the card
        # carries is a different string and answers the flag on its own terms:
        # a part that reads "Answer any three of the following:" is flagged for
        # stopping on a colon, and once its three children are joined it ends
        # in a full stop like any other question.
        flagged = self.paper.suspect(q, letter, roman)
        if flagged and (furniture_removed or joined_kids) \
                and PAPER_TERMINAL.search(question.strip()):
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
        # The same shape for a different reason. The scheme prices the QUESTION
        # and states its points without saying how those marks divide across
        # its parts, so no row has a value of its own.
        if tariff == 'questionTotal':
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

        if tariff == 'questionTotal':
            # There is nothing to sum, so the total has to be given: it is the
            # tariff the paper prints on the question.
            if total is None:
                raise Refused(f'{ref}: a questionTotal card must be given the '
                              f'total the paper prints')
            computed = total
        elif ladder is not None:
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
            if text and self.subject in QUESTION_CLEANING:
                text = _clean_stem(text)
            if text:
                card['stem'] = text
        if notes:
            card['notes'] = notes
        if figure:
            card['figureKey'] = figure
        # The SEC's own print of the ask and its setup, shown BEFORE the
        # reveal. It is the right slot for a stimulus printed once and asked
        # about by several parts -- one hybrid vehicle diagram over (d)(i) and
        # (d)(ii) -- which the answer slot's one-crop-one-card rule is there
        # to forbid, and which would otherwise appear only once the student
        # has already answered.
        if question_figure:
            card['questionFigureKey'] = question_figure
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
