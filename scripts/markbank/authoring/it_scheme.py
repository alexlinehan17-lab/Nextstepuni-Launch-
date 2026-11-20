#!/usr/bin/env python3
"""Italian marking schemes — the priced answer, and the lesser answers under it.

    python3 scripts/markbank/authoring/it_scheme.py 2024 hl --full
    python3 scripts/markbank/authoring/it_scheme.py --audit

What this document is
---------------------
An Italian scheme is four documents stapled together and only two of them are
answers a card can carry:

    LISTENING COMPREHENSION TEST 80 MARKS      <- priced, but the ask is heard
      Section A  16 marks (8x2)                   multiple choice; the right box
      1. (a) a birthday party                     is BOLD in the PDF and the
         (b) an end of exam party                 boldness does not survive the
      SECTION B  Dialogue 1 - 2 - 3               text layer at Higher at all
    SECTION A READING COMPREHENSION (60 marks) <- priced answers
      1. (a) 5 marks
      È una campagna italiana (1m) che ha l'obiettivo … (2m), entro il 2030 (2m).
      ≈≈≈                                       <- the lesser-answer separator
      Nata nel 2020 2m
    SECTION B  (60 marks)                      <- priced answers at both levels
    Section C WRITING (100 marks)              <- BAND GRIDS, no answer

The grammar, and the one rule that reads it
-------------------------------------------
**The head tariff is the FIRST "N marks" printed in an ask's block, and what
comes before it in that block is either a directive or the answer itself.**
That one rule reads every shape the ten sittings print, and they print five:

    1. (a) 5 marks                    Higher: tariff alone, answer below
    (b) Any two of 5 marks (3+2)      a directive, then the options below
    2. (a) 700 2 marks                Ordinary: the answer is ON the head
    3. The beach has all the …
       … assist people 6 marks (2+2+2)   the head runs over two printed lines
    Question 5 … 16 marks (8x2 marks) a matching task, answered a) 7  b) 3 …

Reading the marker alone cannot do it, because the Ordinary scheme prints its
answer on the marker's own line; reading the line alone cannot do it either,
because that answer wraps. The block, cut at the markers and searched for its
first tariff, does both.

WHAT THE SPLIT MEANS DEPENDS ON THE DIRECTIVE
---------------------------------------------
"(3+2)" beside "Any two of 5 marks" is two answers at three and two. The same
"(4+1)" beside a bare "5 marks" is ONE answer whose two halves are worth four
and one — 2024 Higher B1 1(a) prints "Non sapeva dov'era la sua aula (4m) ma si
è perso (1m)" as a single sentence. So the split is only ever read as a count
of answers where the scheme printed a directive saying how many it wants, and
the directive is what sets `claim`. Without one, the ask has a single stated
answer worth the total, and where the scheme lists several unlabelled lines
under a bare tariff this refuses rather than deciding for the SEC how many of
them a candidate needed.

THE LESSER ANSWERS ARE NOT ANSWERS
----------------------------------
Both levels print, under the full-mark answer, the shorter forms that earn part
of the marks. Higher separates them with a row of "≈"; Ordinary wraps each in
parentheses and ends it with its mark: "(Best friend +/- extra information 4
marks)". They are kept, and disclosed on the card as a note with the marks the
scheme prints, because `RowKind` has no kind for a rung worth less than the row
above it and the type says why: add it together with its renderer, not before.
"""
import argparse
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

SUBJECT = 'italian'


def schemes_dir(subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'schemes')


# ------------------------------------------------------------- the units ----
# The listening test, which both levels head this way and which the paper sets
# in a separate booklet. 2025 Higher parenthesises its own total.
UNIT_L = re.compile(r'^LISTENING\s+COMPREHENSION\s+TEST\b', re.I)
# The reading comprehension. Higher sets one and prices it on this line;
# Ordinary sets two and prices them on "Question 1 …" heads beneath it.
UNIT_A = re.compile(r'^SECTION\s+A\s+READING\s+COMPREHENSION\b', re.I)
# Higher's Section B is one of three routes a candidate chooses between, and
# the scheme heads each: the unseen passage, the prescribed novel (itself A or
# B) and the essay. Ordinary's is five publicity pieces.
# 2026 heads the section "SECTION B Literary Passage (60 marks)" and its routes
# "B 1. Unseen passage" and "B 2. Prescribed novel".
UNIT_B_HL = re.compile(r'^SECTION\s+B\s+Unseen\s+Literary\s+Passage\b'
                       r'|^B\s*1\.?\s*Unseen\s+passage\b'
                       # 2015-2017: "SECTION B (60 marks)" over "Unseen Literary
                       # Passage", or "Unseen Literary Passage <title>"
                       r'|^Unseen\s+Literary\s+Passage\b', re.I)
UNIT_B2_HL = re.compile(r'^B\s*2\.?\s*Literary\s+passage\s+from\s+[Pp]rescribed\s+novel\b'
                        r'|^B\s*2\.?\s*Prescribed\s+novel\b', re.I)
UNIT_B3_HL = re.compile(r'^B\s*3\.?\s*Essay\s+on\s+prescribed\s+text\b', re.I)
UNIT_B_OL = re.compile(r'^SECTION\s+B\s*:?\s*PUBLICITY\b', re.I)
UNIT_C = re.compile(r'^Section\s+C\s+WRITING\b', re.I)
# Everything from here is the band grid, the modified scheme and the CD script
# — the transcript of the recording, printed in the ANSWER document.
APPENDIX = re.compile(r'^APPENDIX\b|^Script\s+for\s+Listening', re.I)

# A numbered question inside a unit that restarts its numbering: Ordinary's two
# reading comprehensions and its five publicity pieces. The title and the marks
# may both be on this line, or the title may be here and the marks on the next.
QUESTION_HEAD = re.compile(r'^Question\s+(\d)\b\s*(.*)$')
# The Higher prescribed-novel routes: "A." and "B." on a line of their own,
# each naming its novel. 2021 heads them "A. Marcovaldo (Italo Calvino)".
NOVEL_ROUTE = re.compile(r'^([AB])\s*[.)]\s*(\S.*)$')
# The listening test's own sections. Section A is the multiple choice; the rest
# is three dialogues, which the scheme heads by name.
LISTEN_A = re.compile(r'^\(?\s*(?:Section\s+A?\s*)?\(?\s*(\d{1,3})\s*marks?\s*\(?\s*8\s*[xX×]\s*(\d)', re.I)
LISTEN_SECTION_B = re.compile(r'^SECTION\s+B\b\s*(\d{1,3})?\s*marks?', re.I)
# "Dialogue 3 Interview with …", or in Italian "Dialogo 3 Intervista a …"
# (2018 Higher).
DIALOGUE = re.compile(r'^Dialog(?:ue|o)\s+(\d)\b\s*(.*)$', re.I)

# ------------------------------------------------------------- the block ----
# A printed marker opening an ask. "1.", "1. (a)", "(b)", "a)" — the last of
# which is how the matching task labels its eight items.
NUM_MARK = re.compile(r'^(\d{1,2})\s*\.\s*(?:\(\s*([a-h])\s*\)\s*)?(.*)$', re.S)
LETTER_MARK = re.compile(r'^\(\s*([a-h])\s*\)\s*(.*)$', re.S)
MATCH_MARK = re.compile(r'^([a-h])\s*\)\s*(.*)$', re.S)

# The tariff, wherever in the block it is first printed. The split may be a sum
# ("(3+3+3)"), a product ("(8x2 marks)") or absent.
TARIFF = re.compile(
    r'(\d{1,3})\s*marks?\b\s*(?:\(\s*([\d\s+xX×]+?)\s*(?:marks?\s*)?\))?', re.I)

# How many answers the scheme says it wants. It says so in words, never in
# digits, and always before the tariff: "Any two of", "Three of:", "One of",
# "Any three actions of the following", "Any one of the following two".
COUNT_WORD = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}
# A directive printed WITH the split beside it: "Three of (5+5+5+5)".
DIRECTIVE_SPLIT = re.compile(
    r'^(?:any\s+)?(one|two|three|four|five)\s+of\s*:?\s*'
    r'\(\s*(\d{1,2}(?:\s*\+\s*\d{1,2})+)\s*\)\s*$', re.I)
DIRECTIVE_PREFIX = re.compile(
    r'^(?:any\s+)?(one|two|three|four|five)\s+of\s*:\s*', re.I)
DIRECTIVE = re.compile(
    r'^(?:any\s+)?(one|two|three|four|five)\b[a-z\s’\']*\bof\b'
    r'(?:\s+the\s+(?:following|folloiwing)(?:\s+two)?)?\s*:?\s*$', re.I)

# The row of tildes Higher prints between the full answer and the shorter forms
# that earn part of the marks. 2021 sets four, 2024 three.
LADDER = re.compile(r'^[≈~]{2,}\s*')
# An Ordinary lesser answer: wholly parenthesised, and ending in its own mark.
# The closing bracket is not reliable — the SEC prints "(He is an artist / He
# started doing art in Turin (Torino)) 1 mark)" — so the test is the opening
# bracket plus a trailing mark, not balance.
PAREN_RUNG = re.compile(r'^\(.*\b\d{1,2}\s*marks?\b\.?\s*\)?\s*$', re.I)
# The mark printed at the end of a line, WITH an optional closing bracket: what
# _rung strips off a lesser answer to read its value.
TRAILING_MARK = re.compile(r'\b(\d{1,2})\s*(?:m|marks?)\.?\s*\)?\s*$', re.I)
# Every mark printed inside brackets, with or without its "m": "(3m)", "(2)".
# Where an answer carries SEVERAL of these it is one answer split into halves;
# where it carries exactly one, at its end, it is a lesser answer worth that.
BRACKET_MARK = re.compile(r'\(\s*(\d{1,2})\s*(?:m|marks?)?\s*\)', re.I)
# The split the SEC sometimes prints beside the FIRST answer instead of on the
# head: 2021 Higher B1 2(a) heads "Two of 5 marks" and prints "(3+2)" at the
# end of the first of its six options.
INLINE_SPLIT = re.compile(r'\(\s*(\d{1,2}(?:\s*\+\s*\d{1,2})+)\s*\)\s*$')
# The mark printed at the end of a line with NO bracket around it, which is the
# only shape a lesser answer takes at Higher: "Nata nel 2020 2m", "guitto 1m".
#
# The bracket is the whole distinction and it cost four answers on one ask
# before it was made. An Italian answer carries its own INTERNAL split in
# brackets — 2021 Higher A 1(a) prints "Basta cliccare sul pulsante "dona" e
# "ricevi" (3m) per donare o ricevere un PC/tablet gratuito (2m)" — and reading
# that trailing "(2m)" as the line's own value demoted all four of that ask's
# full answers to one-mark fragments. A bracketed mark is part of the answer; a
# bare one is what the answer is worth.
BARE_MARK = re.compile(r'(?<![(\d])\b(\d{1,2})\s*(?:m|marks?)\.?\s*$', re.I)

BULLET = re.compile(r'^[•●▪■]\s*')
# A heading the scheme itself marks as one: a trailing colon ("Narrator:"),
# the count it requires ("Four points are required"), the instruction over the
# novel ask's points ("The candidate must refer both to the passage and to the
# novel as a whole") and the halves of that ask ("Points from the passage").
SCHEME_HEAD = re.compile(
    r':\s*$'
    r'|\b(?:points?|elements?)\s+(?:is|are)\s+required\b'
    r'|^(?:the\s+)?candidates?\s+must\s+refer\b'
    r'|^(?:points?\s+)?from\s+the\s+(?:passage|novel|text)\b', re.I)
# The word printed between two alternative answers.
SEPARATOR = re.compile(r'^(?:OR|NÓ)$')
# A line that finishes what it says: a full stop, a closing bracket or quote,
# or the marks it earns.
COMPLETE = re.compile(r'(?:[.?!;:)\]”"’]|\b\d{1,2}\s*(?:m|marks?))\s*$', re.I)
# A section's own head printed above its first passage ("SECTION B (60
# marks)"): the end of the last block of the section before it, never part of
# an answer (2016 and 2017 Higher hung it on A Q5 as a lesser answer worth 60).
SECTION_LINE = re.compile(r'^SECTION\s+[A-C]\b[^()]*\(?\s*\d{1,3}\s*marks?\s*\)?\s*$', re.I)
# An examiner's instruction printed where a heading would be: what the answer
# must contain ("Four points are required", "The candidate must refer both to
# the passage and to the novel as a whole", "NB= Either:", "Any suitable
# points from the novel. For example:", a starred footnote). Never a group's
# name and never an answer: it is quoted in the row's note.
INSTRUCTION = re.compile(r'\b(?:points?|elements?)\s+(?:is|are)\s+required\b'
                         r'|^(?:the\s+)?candidates?\s+must\s+refer\b'
                         r'|^N\.?\s?B\.?\s*[=:]|^any\s+suitable\s+points\b|\bfor\s+example:?\s*$'
                         # a starred footnote, not a starred answer ("*To
                         # educate family members" is an answer; "*Educate can
                         # only be used once" is the footnote it points to)
                         r'|^\*\s*\(|^\*.*\b(?:only|if|must|marks?|allocated|reference)\b'
                         r'|\bcan\s+only\s+be\s+used\b'
                         r'|^incorrect\b.*\bminus\s+\d', re.I)
# The paper's instruction echoed on the scheme's head line: "Give four
# details", "One point for Nicole one point for Aurora", "Details: Two of:".
ECHO = re.compile(r'^give\s+(?:one|two|three|four|five)\b|\bpoints?\s+for\b'
                  r'|\b(?:one|two|three|four|five)\s+of\s*[.:]?\s*$', re.I)
# A count printed before the first answer on the head line: "One of Chef/cook".
LEAD_COUNT = re.compile(r'^(?:any\s+)?(?:one|two|three|four|five)\s+of\b\s*:?\s*', re.I)
# A condition the scheme prints after one answer: "(2 elements required)".
REQUIRED = re.compile(r'\s*\(\s*(?:\d|one|two|three|four)\s+elements?\s+required\s*\)\s*$', re.I)
# Characters the extraction leaves where the scheme printed a tick or a cross.
STRAY = re.compile(r'\s*¬`?\s*$')
# A line held aside that is neither a heading nor an answer: the examiner's
# condition ("If only point", "(This answer can be used only with …)") or an
# elements scale ("5 elements 6 marks").
ASIDE = re.compile(r'^\(.*\)\.?$|^if\b|^\d+\s+(?:to\s+\d+\s+)?elements?\b', re.I)
# A lesser answer whose opening bracket the SEC left off: "She makes/reels/
# videos 1 mark)", "Temperature 3 mark)".
# A heading that prices its own points: 2025 Higher A Q5 prints "Etta Polico:
# Any two of 5 marks (3+2)" inside its twenty marks.
PRICED_HEAD = re.compile(r'^([^:]{2,40}):\s*(?:any\s+)?(one|two|three|four|five)\s+of\s*:?\s*'
                         r'(\d{1,2})\s*marks?\s*\(\s*(\d{1,2}(?:\s*\+\s*\d{1,2})+)\s*\)\s*$', re.I)
CLOSED_RUNG = re.compile(r'^\(?(.*?\S)\s*(\d{1,2})\s*marks?\s*\)\s*$', re.I)
NOTE = re.compile(
    # Not "Candidates must have" over "Minimum 10 years' experience": that is
    # the advertisement's own wording, and the answer (2022 Ordinary B1 Q4).
    r'^(?:Note\s*:|N\.?B\.?\b|Penalise|Candidates?\s+(?:will|may|must)\b(?!\s+have\b)'
    r'|All\s+candidates\s+awarded\b|These?\s+last\s+two\s+lesser\b'
    r'|This\s+lesser\s+answer\b|Where\s+(?:a|the|marks)\b|Marks\s+awarded\b'
    r'|For\s+good\s+points\b|Use\s+the\s+descriptors\b|Evidence\s+is\s+needed\b'
    r'|The\s+candidates?\s+must\b|Accept\b|Allow\b'
    # "The answer 'She provides (online) books and resources' can only be
    # awarded marks once, either in part (a) or in part (b)" is an examiner's
    # instruction, and it shipped as a claimable four-mark answer.
    r'|The\s+answer\b|This\s+answer\b)', re.I)
PAGE = re.compile(r'^(?:##\s*Page\s*\d+\s*$|\d{1,3}\s*$)')
# A line that is nothing but a bracketed mark, which is the tail of a wrapped
# answer rather than an answer of its own.
MARK_ONLY = re.compile(r'\(\s*\d{1,2}\s*(?:m|marks?)\s*\)')
# A line holding a bracketed NUMBER with no "m" beside it — "(1)" — which the
# SEC prints as the tail of an answer's own split. It is DROPPED rather than
# joined, because schemeText.mjs drops it too: its LABEL_ONLY rule reads
# "(1)" as a part label and takes it out of the text a marking point is
# searched in, so a card that kept it could not be traced to the scheme it was
# lifted from. "(1m)" is not a label and stays.
BARE_BRACKET_NUM = re.compile(r'^\(\s*\d{1,2}\s*\)$')
# A line that OPENS with a bracketed mark, which is the tail of the answer
# printed above it rather than an answer of its own.
MARK_OPENS = re.compile(r'^\(\s*\d{1,2}\s*(?:m|marks?)?\s*\)')
# A line that states the ask's SPLIT and nothing else. The twenty-mark summary
# ask at the end of a Higher comprehension prints it under its head rather than
# on it — "5. Five points are required 20 marks" then "(5+5+5+5)" — and read as
# an answer it is a marking point made of four digits.
SPLIT_ONLY = re.compile(r'^\(?\s*(\d{1,2}(?:\s*\+\s*\d{1,2})+)\s*\)?\s*$')
# The band the same ask sometimes prints beneath its split: "3 points
# (0,1,3,5)*" is the scale it may score, not an answer.
BAND_LINE = re.compile(r'^\d{1,2}\s+points?\b|^\(\s*0\s*,', re.I)

# One priced line the SEC wrapped onto a second line that opens with a
# capital, which no wrap rule may join without joining separate answers
# everywhere: the two printed lines, joined exactly here.
WRAPS = {
    # 2018 Higher Dialogue 3 prints Q8's tariff on the line ABOVE its number,
    # "4 marks" over "8. His family (1) for at least (1m) two (1) weeks(1)
    # (1+1+1+1)", where the reader hangs it on Q7 as a second heading: the
    # printed tariff is set back on Q8's own line, no word changed.
    (2018, 'hl'): [('4 marks\n8. His family (1) for at least (1m) two (1) weeks(1) (1+1+1+1)',
                    '8. His family (1) for at least (1m) two (1) weeks(1) 4 marks (1+1+1+1)')],
    # 2017 Higher B1 the same: "4 marks" over "1. (a)".
    (2017, 'hl'): [('4 marks\n1. (a)\nSua madre era scomparsa', '1. (a) 4 marks\nSua madre era scomparsa')],
    # 2016 Higher B1 the same: "6marks (3+3)" over "1. (a)".
    (2016, 'hl'): [('6marks (3+3)\n1. (a)\n', '1. (a) 6 marks (3+3)\n')],
    # 2018 Ordinary B Question 4, ask 3 prices two prizes on two lines, "2nd
    # prize … 3 marks" and "3rd prize A book (1m) written your favourite" /
    # "Writer/ of your choice (1m) 2 marks"; the question's 10 marks need both.
    (2018, 'ol'): [('3rd prize A book (1m) written your favourite\nWriter/ of your choice (1m) 2 marks',
                    '3rd prize A book (1m) written your favourite Writer/ of your choice (1m) 2 marks')],
}

# SEC misprints, keyed by the sitting, never repaired by a heuristic.
MISPRINTS = {
    # 2022 Ordinary prices the first ask of its second publicity piece
    # "1. Three of: 6 (2+2+2)" — the word "marks" is not printed, and it is
    # the only tariff in the ten sittings that omits it. Section B Question 2
    # prices itself 18 and its asks 6 + 2 + 6 + 4, so the 6 is marks; the
    # repair says so rather than teaching the reader to read a bare number
    # beside a bracket as a tariff, which would find one in every answer that
    # ends in a date.
    (2022, 'ol'): [('1. Three of: 6 (2+2+2)', '1. Three of: 6 marks (2+2+2)')],
    # 2026 Higher prices Dialogue 3 Q7 "Any two of: 4 (2+2) marks", the word
    # after the split instead of before it; the dialogue's other seven asks
    # and its printed total (32) say the 4 is marks.
    (2026, 'hl'): [('7. Any two of: 4 (2+2) marks', '7. Any two of: 4 marks (2+2)')],
    # 2018 Ordinary prints Question 1's second ask "2 Any two of: 4 marks
    # (2+2)" with no stop after its number; the paper sets six asks and the
    # question's printed 40 marks need this ask's 4.
    (2018, 'ol'): [('2 Any two of: 4 marks (2+2)', '2. Any two of: 4 marks (2+2)')],
    # 2017 Ordinary prices Dialogue 3 Q4 "4 mharc" (the Irish word) and Q7
    # "6 (4+2)" with no word at all; the dialogue's other six asks and its
    # printed 36 marks say both are marks.
    (2017, 'ol'): [('4. Two required 4 mharc (3+1)', '4. Two required 4 marks (3+1)'),
                   ('7. Two required 6 (4+2)', '7. Two required 6 marks (4+2)')],
}


def _split_terms(raw):
    """[3, 3, 3] for "(3+3+3)", [2]*8 for "(8x2)", or None where none printed."""
    if not raw:
        return None
    text = raw.strip()
    m = re.fullmatch(r'(\d{1,2})\s*[xX×]\s*(\d{1,2})', text)
    if m:
        return [int(m.group(2))] * int(m.group(1))
    if re.fullmatch(r'\d{1,2}(?:\s*\+\s*\d{1,2})*', text):
        return [int(x) for x in re.findall(r'\d{1,2}', text)]
    return None


class Part:
    """One priced component of an ask.

    Most asks have exactly one. A handful print two, because the SEC prices
    two halves of one printed question separately — 2024 Higher B1 Q5 sets
    "Kreshnik 15 marks (5+5+5)" over its own bullets and then "Andrea efforts
    5 marks" over more, and the twenty marks the paper prints for that ask are
    those two added. Reading only the first left the section five short of its
    own printed total, which is exactly what the checksum is for.
    """

    __slots__ = ('total', 'split', 'claim', 'directive', 'stated', 'label',
                 'answers', 'rungs', 'notation', 'seq', 'lead', 'confirmed',
                 'groups', 'asides', 'prices', 'components', 'stem', 'notes',
                 'inline', 'fullnames')

    @property
    def counted(self):
        """Whether the scheme PRINTED how many answers it wants."""
        return self.directive is not None

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))

    @property
    def per(self):
        """Descending per-answer values, or None where none is printed.

        The split is only ever a COUNT of answers where a directive said how
        many were wanted, or where its terms are equal and the scheme lists
        more answers than terms. "(4+1)" beside a bare "5 marks" over one
        printed sentence is one answer in two halves, not two answers.
        """
        if self.claim is None:
            return None
        if self.split and len(self.split) == self.claim:
            return self.split
        if self.total is not None and self.claim and self.total % self.claim == 0:
            return [self.total // self.claim] * self.claim
        return None

    def __repr__(self):
        return f'<Part {self.total} claim={self.claim} {len(self.answers or [])} ans>'


class Ask:
    """One printed ask, exactly as the scheme prices it."""

    __slots__ = ('unit', 'section', 'item', 'letter', 'parts', 'total',
                 'notes', 'line', 'fault', 'notation')

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))

    @property
    def key(self):
        return (self.section, self.item, self.letter, None)

    @property
    def head(self):
        return self.parts[0] if self.parts else None

    def __repr__(self):
        return (f'<Ask {self.section} {self.item}{self.letter or ""} '
                f'{self.total} marks in {len(self.parts or [])} part(s)>')


class ItScheme:
    """One published Italian marking scheme, read as a list of asks."""

    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = os.path.join(schemes_dir(subject), f'{year}-{level}.md')
        with open(self.path, encoding='utf-8') as fh:
            raw = fh.read()
        for old, new in list(MISPRINTS.get((year, level), ())) + list(WRAPS.get((year, level), ())):
            assert old in raw, f'{year} {level}: misprint {old!r} is not in the scheme'
            raw = raw.replace(old, new)
        self.lines = [l.rstrip() for l in raw.split('\n')]
        self.asks = []
        self.refused = []
        self.section_totals = {}       # section token -> the tariff it prints
        self.titles = {}               # section token -> the passage it marks
        self._read()

    # -- segmentation -------------------------------------------------------
    def _sections(self):
        """[(section token, first line, last line)] over the whole file.

        The scheme's own heads, in the order it prints them. Everything from
        APPENDIX is the band grid, the modified scheme and the CD script.
        """
        marks = []
        stop = len(self.lines)
        for i, line in enumerate(self.lines):
            s = line.strip()
            if APPENDIX.match(s):
                stop = i
                break
        unit = None
        for i, line in enumerate(self.lines[:stop]):
            s = line.strip()
            if UNIT_L.match(s):
                unit = 'L'
                marks.append((i, 'L', 'LA', None))
                continue
            if UNIT_A.match(s):
                unit = 'A'
                total = self._marks_on(i)
                marks.append((i, 'A', 'A' if self.level == 'hl' else None, total))
                continue
            if UNIT_B_HL.match(s):
                unit = 'B'
                marks.append((i, 'B', 'B1', self._marks_on(i)))
                continue
            if UNIT_B2_HL.match(s):
                unit = 'B'
                marks.append((i, 'B', 'B2', self._marks_on(i)))
                continue
            if UNIT_B3_HL.match(s):
                unit = 'B'
                marks.append((i, 'B', 'B3', self._marks_on(i)))
                continue
            if UNIT_B_OL.match(s):
                unit = 'B'
                marks.append((i, 'B', None, self._marks_on(i)))
                continue
            if UNIT_C.match(s):
                unit = 'C'
                marks.append((i, 'C', 'C', self._marks_on(i)))
                continue
            if unit == 'L':
                m = LISTEN_SECTION_B.match(s)
                if m:
                    marks.append((i, 'L', 'LB', None))
                    continue
                m = DIALOGUE.match(s)
                if m:
                    marks.append((i, 'L', f'LB{m.group(1)}', self._marks_on(i)))
                    continue
                continue
            if unit in ('A', 'B') and self.level == 'ol':
                m = QUESTION_HEAD.match(s)
                if m:
                    token = f'{unit}{m.group(1)}'
                    marks.append((i, unit, token, self._marks_on(i, look=2)))
                    self.titles[token] = ' '.join(m.group(2).split())
                    continue
            if unit == 'B' and self.level == 'hl':
                m = NOVEL_ROUTE.match(s)
                if m and marks and marks[-1][2] and marks[-1][2].startswith('B2'):
                    token = f'B2{m.group(1)}'
                    marks.append((i, 'B', token, None))
                    self.titles[token] = ' '.join(m.group(2).split())
                    continue
        out = []
        for n, (i, unit, token, total) in enumerate(marks):
            end = marks[n + 1][0] if n + 1 < len(marks) else stop
            if token is None:
                continue           # a unit head whose questions carry the keys
            out.append((token, unit, i, end, total))
        # The Higher prescribed-novel section offers two novels and the scheme
        # labels the SECOND "B." while leaving the first unlabelled in three of
        # the five sittings — 2024 heads it "B 2. Literary passage from
        # prescribed novel (60 marks)" and names the novel on the next line.
        # An unlabelled first route beside a labelled second one is route A.
        tokens = {row[0] for row in out}
        if 'B2B' in tokens and 'B2' in tokens:
            out = [(('B2A' if t == 'B2' else t), u, i, e, tot)
                   for t, u, i, e, tot in out]
        # Both prescribed-novel routes are worth what the section prints on its
        # own head — a candidate answers ONE of them — and the scheme prints
        # that figure once, over route A. Route B's head names its novel only.
        by_token = {t: tot for t, _u, _i, _e, tot in out}
        if by_token.get('B2B') is None and by_token.get('B2A') is not None:
            out = [(t, u, i, e, (by_token['B2A'] if t == 'B2B' else tot))
                   for t, u, i, e, tot in out]
        return out

    def _marks_on(self, i, look=1):
        """The tariff printed on this head line, or on the next `look` lines."""
        for j in range(i, min(i + 1 + look, len(self.lines))):
            m = re.search(r'(\d{1,3})\s*marks?\b', self.lines[j], re.I)
            if m:
                return int(m.group(1))
        return None

    # -- the walk -----------------------------------------------------------
    def _read(self):
        for token, unit, start, end, total in self._sections():
            if total is not None:
                self.section_totals[token] = total
            if unit in ('L', 'C') or (token == 'B3' and self.level == 'hl'):
                # The listening test, Section C and the Higher essay on the
                # prescribed text are all priced by a BAND GRID rather than by
                # an answer — the essay's own head says so: "Use the
                # descriptors in Appendix 1". They are counted from the paper
                # and excluded with that evidence; see it_all.py.
                #
                # Level-guarded on purpose: "B3" at ORDINARY is the third
                # publicity piece, an ask with four priced answers, and
                # skipping it by token alone lost a whole advertisement from
                # four of the five Ordinary sittings.
                continue
            self._read_asks(token, unit, start + 1, end,
                            self._split_on(start))
        self._checksum()

    def _split_on(self, i):
        """The split printed on a section head — "16 marks (8x2 marks)".

        The matching task is the one ask family that prices nothing on its own
        markers: the scheme answers it "a) 7  b) 3 …" and states what each is
        worth once, on the question's own head. Without it every matching item
        carries no tariff at all and the section censuses sixteen marks against
        a sum of zero.
        """
        # Two lines, for the same reason _marks_on reads two: 2021 Ordinary
        # heads its fourth publicity piece "Question 4" and prints the title
        # and the tariff on the line beneath, where every other sitting prints
        # both on the head. Reading one line left that matching task with no
        # tariff at all.
        for j in range(i, min(i + 3, len(self.lines))):
            m = TARIFF.search(self.lines[j])
            if m:
                return _split_terms(m.group(2))
        return None

    def _read_asks(self, token, unit, start, end, section_split=None):
        """Every ask this section prices, cut into blocks at its markers."""
        heads = []
        item = None
        for i in range(start, end):
            s = self.lines[i].strip()
            if not s or PAGE.match(s):
                continue
            m = NUM_MARK.match(s)
            if m:
                item = int(m.group(1))
                heads.append((i, item, m.group(2), m.group(3)))
                continue
            m = LETTER_MARK.match(s)
            if m and item is not None:
                # NOT guarded by PAREN_RUNG. "(b) One of 5 marks" opens an ask
                # and also looks exactly like an Ordinary lesser answer — it
                # starts with a bracket and ends with a mark — so guarding it
                # threw away every lettered ask at Higher: 2021 censused five
                # asks in a section that prices nine. What separates the two is
                # the bracket's CONTENT: a part label is one letter a-h and
                # nothing else, while a lesser answer is a sentence, and
                # LETTER_MARK already requires the former.
                heads.append((i, item, m.group(1), m.group(2)))
                continue
            m = MATCH_MARK.match(s)
            if m and (re.fullmatch(r'\d{1,2}', m.group(2).strip())
                      # 2018 Ordinary prints the point's words after its
                      # number ("a) 3 Do not share your password"); only in a
                      # section whose head prices equal items ("(8x2 marks)").
                      or (re.match(r'\d{1,2}\s+\S', m.group(2).strip()) and section_split
                          and len(section_split) > 1 and len(set(section_split)) == 1)):
                # The matching task: "a) 7" — the marker is a bare letter and
                # the answer is the number of the point it refers to.
                heads.append((i, None, m.group(1), m.group(2)))
                continue
        blocks = []
        for n, (i, item, letter, rest) in enumerate(heads):
            stop = heads[n + 1][0] if n + 1 < len(heads) else end
            blocks.append([i, item, letter,
                           ([rest] if rest.strip() else [])
                           + [l.strip() for l in self.lines[i + 1:stop]]])
        blocks = _transplant(blocks)
        for i, item, letter, lines in blocks:
            ask = self._parse(token, unit, item, letter, i, lines, section_split)
            if not isinstance(ask, str) and ask is not None:
                # The same block, cut the other way. See _join: which cut is
                # right is settled by the scheme's own printed count, so both
                # are made and _recut chooses per component.
                alt = self._parse(token, unit, item, letter, i, lines,
                                  section_split, mode='list')
                if not isinstance(alt, str) and alt is not None:
                    _recut(ask, alt)
            if ask is None:
                # A marker printed on a line of its own, whose own lettered
                # parts are the asks: 2025 Higher A sets "2." alone above
                # "(a) 5 marks". It is not an ask and it is not a fault.
                continue
            if isinstance(ask, str):
                self.refused.append(((token, item, letter, i), ask))
            else:
                self.asks.append(ask)

    def _parse(self, token, unit, item, letter, line_no, block,
               section_split=None, mode='wrap'):
        """One block, cut into the components the scheme prices separately."""
        # The matching task states its answer on the marker's own line and
        # prices every item on the section head: "16 marks (8x2 marks)". Read
        # from the RAW block, before the join: its whole answer is a single
        # digit, and _join drops a line that is nothing but one — that is what
        # a printed page number looks like, and dropping those is what keeps
        # "10" and "## Page 11" out of the middle of an answer that runs across
        # a page break. Read after the join, all forty matching asks vanished.
        if item is None:
            answer = next((l.strip() for l in block if l.strip()), '')
            if not answer:
                return None
            per = section_split[0] if section_split else None
            part = Part(total=per, split=None, claim=None, directive=None,
                        stated=answer, label=None, answers=[answer], rungs=[],
                        notation='matching')
            return Ask(unit=unit, section=token, item=None, letter=letter,
                       parts=[part], total=per, notes=[], line=line_no,
                       fault=None, notation='matching')

        lines = _join(block, mode)
        if not lines:
            return None       # a bare "3." whose own lettered parts are the asks

        head = None
        for n, text in enumerate(lines):
            m = TARIFF.search(text)
            if m and not PAREN_RUNG.match(text):
                head = (n, m)
                break
        if head is None:
            return 'the scheme prints no tariff for this ask'
        n, m = head
        before = ' '.join((' '.join(lines[:n]) + ' ' + lines[n][:m.start()]).split())
        rest_lines = ([lines[n][m.end():].strip()]
                      if lines[n][m.end():].strip() else []) + lines[n + 1:]

        notes = []
        parts = [_open_part(before, m)]
        in_ladder = False
        in_note = False
        for at, text in enumerate(rest_lines):
            t = text.strip()
            if not t or PAGE.match(t):
                continue
            if LADDER.match(t):
                in_ladder = True
                continue
            if NOTE.match(t):
                notes.append(t)
                in_note = True
                continue
            if in_note and t[:1].islower() and not BULLET.match(t):
                # The examiner's instruction, wrapped. "These last two lesser
                # answers will be awarded" / "marks if they are the only
                # answers given" is one sentence, and its second half shipped
                # as a claimable answer until the note was allowed to run on.
                notes.append(t)
                continue
            in_note = False
            if PAREN_RUNG.match(t):
                parts[-1].rungs.append(_rung(t))
                continue
            ds = DIRECTIVE_SPLIT.match(t)
            if ds and not parts[-1].answers:
                parts[-1].claim = COUNT_WORD[ds.group(1).lower()]
                parts[-1].directive = t
                terms = [int(x) for x in re.findall(r'\d{1,2}', ds.group(2))]
                if parts[-1].split is None and sum(terms) == parts[-1].total:
                    parts[-1].split = terms
                continue
            d = DIRECTIVE.match(t)
            if d:
                # A directive is never an answer, wherever it is printed. 2021
                # Higher A Q5 sets a second "Two of" halfway down its block,
                # over the points for the second half of the ask, and read as
                # an answer it shipped "Two of" as a claimable marking point.
                if not parts[-1].answers:
                    parts[-1].claim = COUNT_WORD[d.group(1).lower()]
                    parts[-1].directive = t
                else:
                    notes.append(t)
                continue
            m3 = SPLIT_ONLY.match(t)
            if m3:
                terms = [int(x) for x in re.findall(r'\d{1,2}', m3.group(1))]
                if parts[-1].split is None and sum(terms) == parts[-1].total:
                    parts[-1].split = terms
                else:
                    notes.append(t)
                continue
            if BAND_LINE.match(t) and not parts[-1].answers:
                notes.append(t)
                continue
            if in_ladder and (BULLET.match(t) or (
                    not TRAILING_MARK.search(t) and not BRACKET_MARK.search(t)
                    and len(t.split()) <= 4
                    and at + 1 < len(rest_lines)
                    and (BULLET.match(rest_lines[at + 1].strip())
                         or DIRECTIVE.match(rest_lines[at + 1].strip())))):
                # The ladder ends where the next printed heading or bulleted
                # answer begins. 2017 Higher A Q5 prints its "Advantage"
                # points, a ladder of shorter answers, then "Disadvantage" over
                # three bulleted points and "Riccardo" points after another
                # ladder: read as one ladder, every one of those became a
                # lesser answer with no marks and the card lost both halves.
                in_ladder = False
            if in_ladder:
                parts[-1].rungs.append(_rung(t))
                continue
            # A SECOND priced head inside the block. It has to end the line and
            # be worth at least what one answer of the part above it is worth:
            # a line ending "2 marks" under a part paying three an answer is
            # the SEC's lesser answer printed without a tilde row over it, not
            # a new component. 2023 Ordinary A2 Q3(a) prints exactly that.
            m2 = TARIFF.search(t)
            if (m2 and parts[-1].stated and m2.end() >= len(t.rstrip())
                    and int(m2.group(1)) >= (parts[-1].split or [parts[-1].total])[0]):
                parts.append(_open_part(t[:m2.start()].strip(), m2))
                continue
            # The bullet is KEPT here and stripped in _settle, which needs it:
            # an unbulleted line inside a bulleted list is a heading, not an
            # answer.
            parts[-1].answers.append(t)

        for part in parts:
            _settle(part)
        if any(p.total is None for p in parts):
            return 'the scheme prints no tariff for one part of this ask'
        # Where the head merely NAMES what it is pricing, the ask is the sum of
        # its components; where the head prices the ask outright, a component
        # beneath it is a sub-total already inside that figure. 2024 Higher B1
        # Q5 heads "Kreshnik 15 marks" and adds "Andrea efforts 5 marks" to
        # reach the twenty the paper prints; 2025 Higher A Q5 heads "20 marks"
        # and prints "Etta Polico: Any two of 5 marks" inside it.
        total = (sum(p.total for p in parts) if parts[0].stated or parts[0].label
                 else parts[0].total)
        return Ask(unit=unit, section=token, item=item, letter=letter,
                   parts=parts, total=total, notes=notes, line=line_no,
                   fault=None, notation=m.group(0).strip())

    # -- the SEC's own arithmetic -------------------------------------------
    def _checksum(self):
        """Each section's item tariffs against the total it prints on its head.

        The only independent check this document offers on whether an ask was
        missed or a tariff mis-read: every reading section prints what it is
        worth, and the asks beneath it have to add up to it. Where they do not,
        every ask in that section is faulted — an unexplained disagreement
        means the reader may have lost one, and no tariff in it can be trusted.
        """
        for token, printed in self.section_totals.items():
            asks = [a for a in self.asks if a.section == token]
            if not asks or any(a.total is None for a in asks):
                continue
            got = sum(a.total for a in asks)
            if got == printed:
                continue
            for a in asks:
                a.fault = (f'section {token} prices its items {got} against its '
                           f'own printed {printed}, and the difference cannot '
                           f'be pinned on one ask')

    # -- lookups ------------------------------------------------------------
    def ref(self, ask):
        tail = f'Q{ask.item}' if ask.item is not None else 'Q'
        if ask.letter:
            tail += f'({ask.letter})'
        return f'{self.year} {self.level.upper()} Section {ask.section} {tail}'

    def reading(self):
        return [a for a in self.asks if a.unit in ('A', 'B')]

    def by_section(self, token):
        return [a for a in self.asks if a.section == token]


def _transplant(blocks):
    """The tariff printed on the ITEM line, above the letter it belongs to.

    The SEC prints a lettered ask two ways. Usually the letter carries its own
    tariff — "(b) Two of: 2 marks (1+1)". Twice in the corpus it prints the
    tariff on the item's own line and the letter under it:

        3. Two of 2 marks (1+1)          <- 2023 Ordinary Section B Q1
        (a) She worked in a
            small three-star Venetian hotel
        (b) Two of: 2 marks (1+1)

    Read literally that keys a tariff to an ask with no answer and an answer to
    an ask with no tariff, and the second is then refused for having no printed
    tariff — the "ask on the line below" bucket, exactly. The transplant moves
    the item head's lines onto the lettered ask BENEATH it, and only where the
    item head states nothing but a tariff and that letter prints none of its
    own, so it can never take a tariff off an ask that has one.
    """
    out = []
    n = 0
    while n < len(blocks):
        i, item, letter, lines = blocks[n]
        nxt = blocks[n + 1] if n + 1 < len(blocks) else None
        head_is_bare = (letter is None and item is not None
                        and len(_join(lines)) == 1
                        and TARIFF.search(lines[0]) is not None)
        # "prints none of its own" means none in its ANSWERS. A lesser answer
        # carries a mark of its own — "(Loudspeakers 1 mark)" — and counting
        # that as the ask's tariff left 2022 Ordinary Section B Q2(a) refused.
        next_is_letter = (nxt is not None and nxt[1] == item and nxt[2]
                          and not any(TARIFF.search(l) for l in nxt[3]
                                      if not PAREN_RUNG.match(l.strip())))
        if head_is_bare and next_is_letter:
            nxt[3] = lines + nxt[3]
            n += 1
            continue
        out.append(blocks[n])
        n += 1
    return out


def _open_part(before, m):
    """A component from its printed head: the tariff, and what precedes it."""
    total = int(m.group(1))
    split = _split_terms(m.group(2))
    claim = directive = stated = None
    d = DIRECTIVE.match(before)
    if d:
        claim = COUNT_WORD[d.group(1).lower()]
        directive = before
    elif before:
        stated = before
    return Part(total=total, split=split, claim=claim, directive=directive,
                stated=stated, label=None, answers=[], rungs=[],
                notation=m.group(0).strip())


def _settle(part):
    """Sort a component's printed lines into answers, lesser answers and a claim.

    Three things are decided here, all from what the scheme prints.

    **Which lines are answers.** The SEC prints a lesser answer under its full
    answer with the mark it earns — "Si costruisce una reputazione (2m)",
    "guitto 1m", "Non avrebbe seguaci (3)" — and it prints the INTERNAL split
    of a full answer the same way: "Basta cliccare sul pulsante 'dona' e
    'ricevi' (3m) per donare o ricevere un PC/tablet gratuito (2m)". What
    separates them is WHERE the marks fall. A line carrying exactly one mark,
    at its end, worth less than the ask pays for one answer, is a lesser
    answer; a line carrying a mark anywhere else is a full answer showing how
    its own halves divide. Reading every trailing mark as the line's value
    demoted all four full answers of 2021 Higher A 1(a) to fragments.

    **What one answer is worth.** The split is usually printed on the head and
    sometimes at the end of the FIRST answer — 2021 Higher B1 2(a) heads "Two
    of 5 marks" and prints "(3+2)" after its first option — and the second is
    read only when its terms are as many as the directive asks for and add up
    to the head total. Where neither is printed and the total does not divide
    by the count, the ask is refused rather than priced.

    **How many answers are wanted.** The scheme states it — "Any two of",
    "Three of:" — or the split says it, where the split's terms are equal and
    it lists more answers than terms. Where it says neither and lists several
    answers, ONE of them answers the ask, which is the reading the scheme's own
    front matter states: "the answers given on the marking scheme are not
    intended to be exhaustive and therefore should not be considered as the
    only possible answers that may be accepted. Alternative expressions,
    phrases and words which convey a similar meaning … are also acceptable",
    and "In a question where a number of elements are required and not
    provided, marks will be deducted" — a number of elements is REQUIRED where
    the scheme prints one, and this scheme prints one whenever it wants more
    than a single answer.
    """
    per = (part.split or [part.total])[0]
    # One answer's whole worth: the total where an unequal split says how one
    # answer divides, else one share.
    whole = part.total if part.split and len(set(part.split)) > 1 else per
    kept, demoted = [], []
    for a in part.answers:
        body = INLINE_SPLIT.sub('', a).strip()
        marks = list(BRACKET_MARK.finditer(body))
        bare = BARE_MARK.search(body)
        if bare and int(bare.group(1)) < per and not body.startswith('('):
            demoted.append(_rung(a))
        elif (kept and len(marks) == 1 and marks[0].end() >= len(body.rstrip())
              and _completes(kept[-1], int(marks[0].group(1)), whole)):
            # The wrapped tail of the full answer above, not a lesser answer:
            # 2025 Higher B2B 2(a) prints "Il fatto che stesse per attaccare
            # uno del partito di Rosello (3) e voleva coinvolgere" and then
            # "Rosello stesso (2)" under a "5 marks (3+2)" head. The line above
            # stops short of one answer's worth by exactly this line's mark,
            # with its own mark mid-line, so this line finishes it.
            kept[-1] = f'{kept[-1].rstrip()} {a.strip()}'
        elif (len(marks) == 1 and marks[0].end() >= len(body.rstrip())
              and int(marks[0].group(1)) < per):
            demoted.append(_rung(body[:marks[0].start()] + ' '
                                + str(marks[0].group(1)) + 'm'))
        else:
            kept.append(a)
    part.answers, part.rungs = kept, part.rungs + demoted
    # The directive printed at the FRONT of the first answer instead of on a
    # line of its own: 2024 Higher A 3(b) prices "(b) 5 marks (3+2)" and
    # answers it "Two of: campagna, iniziativa, istituzione, …".
    if part.answers:
        d = DIRECTIVE_PREFIX.match(part.answers[0])
        if d:
            part.claim = part.claim or COUNT_WORD[d.group(1).lower()]
            part.directive = part.directive or d.group(0).strip()
            part.answers[0] = part.answers[0][d.end():].strip()
            part.answers = [a for a in part.answers if a]
    # A comma list the SEC broke across printed lines. Every line but the last
    # ends in a comma, which is what a list does and what a menu of separate
    # answers never does — a menu's lines end in words.
    if len(part.answers) > 1 and all(a.rstrip().endswith(',')
                                     for a in part.answers[:-1]):
        part.answers = [' '.join(part.answers)]
    if part.stated and not part.answers:
        part.answers = [part.stated]
    elif part.stated and part.answers:
        part.label, part.stated = part.stated, None
        part.lead = part.label
    # The split printed beside the first answer rather than on the head.
    if part.claim and part.claim > 1 and not part.split and part.answers:
        at_end = INLINE_SPLIT.search(part.answers[0])
        m = at_end or re.search(
            r'\(\s*(\d{1,2}(?:\s*\+\s*\d{1,2})+)\s*\)', part.answers[0])
        if m:
            terms = [int(x) for x in re.findall(r'\d{1,2}', m.group(1))]
            if len(terms) == part.claim and sum(terms) == part.total:
                part.split = terms
                # Taken OUT of the answer only where the SEC printed it at the
                # end. 2022 Higher A 2(b) sets "(3+2)" in the MIDDLE of its
                # first answer, and cutting it there leaves a sentence the
                # scheme prints nowhere: the provenance gate found no such
                # marking point, and rightly.
                if at_end:
                    part.answers[0] = part.answers[0][:m.start()].strip()
    # An equal split IS the count, wherever the scheme prints as many answers as
    # it has terms. "(3+3)" over two answers is two answers at three, not one
    # answer in two halves — 2023 Higher B1 3(a) prices "6 marks (3+3)" over
    # "Offrono vitto e alloggio" and "Avrebbe tempo per studiare", which are
    # two separate reasons. An UNEQUAL split is left alone: "(4+1)" is how one
    # answer divides.
    if (part.claim is None and part.split and len(part.split) > 1
            and len(set(part.split)) == 1
            and len(part.answers) >= len(part.split)):
        part.claim = len(part.split)
    # A claim the scheme answers on ONE printed line, as a comma list. 2021
    # Higher A 4(a) sets "Five of 5 marks" over "(Nativi) digitali, grafica,
    # sito, social, digitalizzazione, computer, componenti (1+1+1+1+1)" — seven
    # accepted words, five of them wanted, all on one line. Split only where
    # the line is a LIST: no sentence punctuation, and at least as many items
    # as the claim, so an answer that happens to contain a comma is left whole.
    if part.claim and part.claim > 1 and len(part.answers) == 1:
        one = part.answers[0]
        body = re.sub(r'\([^)]*\)', '', one)
        items = [x.strip(' .') for x in body.split(',')]
        items = [x for x in items if x]
        if len(items) >= part.claim and not re.search(r'[.?!]\s', body) \
                and all(len(x.split()) <= 4 for x in items):
            part.answers = items
    # A HEADING the SEC prints over a run of points, which is not an answer: the
    # twenty-mark summary ask names the person each half is about — "Guido",
    # "Leo", "Serendippo", "Advantage" — and left in the list each is a
    # claimable option worth five marks for writing down a name.
    #
    # Narrow on purpose. Short lines ARE answers elsewhere: 2022 Higher A 2(a)
    # answers "find three prepositions" with "Della", "del", "all'", "al". What
    # separates them is what FOLLOWS — a heading is followed by the sentences
    # it heads, a one-word answer by more one-word answers — so a line of three
    # words or fewer is only dropped when the line under it runs to eight or
    # more.
    # A heading that carries the ask's split with it: 2021 Higher A Q5 prints
    # "Advantage (5+5+5+5)" over the points for the first half of its answer.
    if part.answers:
        m = INLINE_SPLIT.search(part.answers[0])
        if m and len(part.answers[0][:m.start()].split()) <= 3:
            terms = [int(x) for x in re.findall(r'\d{1,2}', m.group(1))]
            if sum(terms) == part.total and part.split is None:
                part.split = terms
            part.answers[0] = part.answers[0][:m.start()].strip()
    # Lines shaped like a HEADING. Two shapes were read as headings and taken
    # out of the answers: a line without a bullet inside a bulleted list (2023
    # Higher B2A Q5 sets "Leo's view of il Sognatore" over its bulleted
    # points), and a line of three words or fewer over a line of eight or more
    # ("Advantage" over its points). Most lines of either shape are ANSWERS:
    # "Cars are speeding", "He is Italian", "It reduces stress" were each
    # taken out of their option lists, and the wrapped tail of a bulleted
    # answer ("Teschio" under "… thousand times worse than") with them.
    #
    # So a heading is only what the SCHEME marks as one (SCHEME_HEAD: a
    # trailing colon, "Four points are required", "The candidate must refer
    # …", "From the passage") or what the PAPER's own question prints, and the
    # paper is not read here: a line of either shape is held aside as a
    # CANDIDATE and confirm_headings() settles it once the card builder has
    # the question. What part.answers and part.label hold until then is what
    # they always held, so every count read before the question is known
    # (_recut, _lead, the claim below) is unchanged.
    seq = []        # [kind, text, wrapped]: 'ans', 'head' (scheme-marked), 'cand'
    for a in part.answers:
        t = BULLET.sub('', a)
        if SEPARATOR.match(t):
            continue        # "OR" between two alternative answers is neither
        kind = 'head' if (not BULLET.match(a) and SCHEME_HEAD.search(t)) else 'ans'
        m = INLINE_SPLIT.search(t) if kind == 'head' else None
        if m:
            # The split printed on a heading further down the list: 2018 and
            # 2019 Higher B2A Q5 print "Points from the passage (5+5+5+5)"
            # under "The candidate must refer both …", four answers at five.
            terms = [int(x) for x in re.findall(r'\d{1,2}', m.group(1))]
            t = t[:m.start()].strip()
            if part.split is None and sum(terms) == part.total:
                part.split = terms
                if part.claim is None and len(set(terms)) == 1:
                    part.claim = len(terms)
        seq.append([kind, t, False, bool(BULLET.match(a))])
    body = [e for e in seq if e[0] == 'ans']
    marked = [e[3] for e in body]
    if any(marked) and not all(marked) and sum(marked) >= (part.claim or 1):
        chain = []      # whether each line belongs to a bulleted answer
        for k, e in enumerate(seq):
            if e[0] == 'ans' and not e[3]:
                above = seq[k - 1] if k else None
                e[0] = 'cand'
                # The tail of the answer above it, not a line of its own: it
                # opens in lower case or on a figure ("30, who share a passion
                # …"), or the line above stops on a function word, a comma or
                # a solidus, or it sits under a BULLETED answer, whose bullet
                # it continues ("… thousand times worse than" / "Teschio";
                # "… has a son / called Mario." / "She lives in Naples"),
                # unless the paper prints it as a heading. An unbulleted line
                # under an unbulleted one that ends on a word is a line of its
                # own (2025 Higher A Q5's Serendippo points).
                parallel = above and e[1].split()[:2] == above[1].split()[:2] and len(e[1].split()) > 2
                # Never a bracket ("(A cycling event/For cycling" opens a
                # shorter answer) or a line priced on its own ("Standard
                # tickets cost €10 … 2 marks").
                own = e[1].startswith('(') or BARE_MARK.search(e[1])
                e[2] = bool(above and above[0] in ('ans', 'cand') and not parallel and not own and (
                    _opens_wrapped(e[1]) or CONTINUED.search(above[1])
                    or above[1].rstrip().endswith((',', '/', '-', '–'))
                    or chain[k - 1]))
            chain.append(bool(e[3] or (e[2] and chain and chain[-1])))
    body = [e for e in seq if e[0] == 'ans']
    heads = []
    for k, e in enumerate(body):
        nxt = body[k + 1][1] if k + 1 < len(body) else ''
        if (len(e[1].split()) <= 3 and len(nxt.split()) >= 8
                and not e[1].rstrip().endswith(('.', '?', '!'))):
            heads.append(e)
    if heads and len(body) - len(heads) >= (part.claim or 1):
        for e in heads:
            e[0] = 'cand'
    part.seq = [e[:4] for e in seq]
    part.answers = [e[1] for e in seq if e[0] == 'ans']
    aside = [e[1] for e in seq if e[0] != 'ans']
    if aside:
        part.label = part.label or ' / '.join(aside)[:120]
    # Nothing printed says how many, and more than one answer is stated: one of
    # them answers the ask. See the front matter quoted above.
    if part.claim is None and len(part.answers) > 1:
        part.claim = 1


def _opens_wrapped(line):
    """A line opening in lower case or on a figure goes on from the one above."""
    return bool(re.match(r'[a-z\u00e0-\u00fc\d]', line))


def _printed_in(line, question, shaped=False):
    """Whether the paper's own question prints this heading: every word of it
    that is not a function word ("Advantage", "Riccardo", "Helena Geraci";
    "Difference" by its stem, "how they differ"), or most of them ("What we
    know about the letter at the end of the novel" over "What have we learned
    about the same letter by the end of the novel"). A line SHAPED like a
    heading (no bullet, over bulleted answers, no full stop) needs one:
    "Development/Implications for his investigation" over "How do these
    findings develop in the rest of the novel"."""
    words = [w for w in re.findall(r"[^\W\d_]+", line.lower())
             if len(w) > 1 and w not in CONTINUES]
    if not words:
        return False
    printed = set(re.findall(r"[^\W\d_]+", question.lower()))

    def hit(w):
        return (w in printed or f'{w}s' in printed or w.rstrip('s') in printed
                or (len(w) >= 6 and any(p.startswith(w[:6]) for p in printed)))
    hits = sum(1 for w in words if hit(w))
    if hits == len(words):
        return True
    if line.rstrip().endswith('.') or len(words) > 12:
        return False
    return hits * 2 >= len(words) or (shaped and hits >= 1)


def _run(seq, text, name):
    """How many answers in a row, from this one, open on "name:". A heading
    printed inside its answers labels a run of them; 2018 Higher B2B Q5
    alternates "Manno:" and "Roscio:" from answer to answer, which is a
    pairing, not two halves."""
    at = next(k for k, e in enumerate(seq) if e[1] == text)
    run = 0
    for kind, t, *_rest in seq[at:]:
        if kind != 'ans' or not t.startswith(f'{name}:'):
            break
        run += 1
    return run


def _balanced_outer(text):
    """Whether the first bracket of `text` closes at its end: "(Go on the
    internet /website=database)", not "(Era) una pianta verde"."""
    depth = 0
    for k, ch in enumerate(text):
        depth += ch == '('
        depth -= ch == ')'
        if depth == 0:
            return k == len(text) - 1
    return False


def _bracketed(part, text):
    """A bracketed line under the answers: a lesser answer with its marks
    ("(They were messing/playing 3 marks)*") becomes a lesser answer, and
    anything else, or the condition starred after it, the examiner's note."""
    m = re.match(r'^\((.*)\)\s*(\*.*)?$', text)
    inner, star = (m.group(1), m.group(2)) if m else (text, None)
    closed = re.match(r'^(.*\S)\s+(\d{1,2})\s*marks?\.?$', inner.strip(), re.I)
    if closed and int(closed.group(2)) < part.total:
        part.rungs.append((closed.group(1), int(closed.group(2))))
        if star and star.strip('* '):
            part.notes.append(f'§The scheme adds to the shorter answer “{closed.group(1)}”: “{star.strip()}”.')
        return
    part.asides.append(text if text.startswith('(') else f'({text})')


def confirm_headings(part, question):
    """Settle the lines _settle held aside as possible headings, now the
    question is known: a heading the scheme marks, or one the paper prints,
    heads the answers under it; any other such line is an ANSWER again, or
    the wrapped tail of the bulleted answer above it. Idempotent."""
    if part.confirmed:
        return
    part.confirmed = True
    part.asides, part.prices, part.notes, part.inline, part.fullnames = [], {}, [], set(), {}
    if not part.seq:
        return
    live = set(part.answers)
    restored = False
    out, heads, groups = [], [], [[None, [], None]]
    # The head line's own words: a heading ("From the passage" in 2018
    # Higher B2B Q5's "Candidate must refer both to the passage and to the
    # text as a whole From the passage 20 marks"), or an instruction only.
    if part.lead and not part.stem and not re.search(r'[^\W\d_]', part.lead):
        part.lead = None        # "6. (a) . 2 marks": nothing printed but the stop
    if part.lead and not part.stem and re.match(r'^(?:one|two|three|four|five)\s+required\b', part.lead, re.I):
        part.lead = None        # "4. Two required 4 marks (3+1)": the count, read from the split
    lead_restored = False
    if part.lead and not part.stem:
        first = re.search(r'(?:points?\s+)?from\s+the\s+(?:passage|novel|text)\b.*$', part.lead, re.I)
        if first:
            groups[0][0] = first.group(0)
            rest = part.lead[:first.start()].strip()
            if rest:
                part.notes.append(rest)
            part.lead = None
        elif INSTRUCTION.search(part.lead) or ECHO.search(part.lead):
            part.notes.append(part.lead)
            part.lead = None
        elif LEAD_COUNT.match(part.lead):
            # "One of Chef/cook 3 marks": the count, then the first answer.
            first_answer = STRAY.sub('', part.lead[LEAD_COUNT.match(part.lead).end():]).strip(' `')
            part.lead = None
            if len(first_answer) > 1:
                live.add(first_answer)
                part.seq = [['ans', first_answer, False, False]] + list(part.seq)
                restored = lead_restored = True
        elif not _printed_in(part.lead, question):
            # The head line's own words are the first ANSWER, not a heading:
            # "1. (a) Rest 8 marks (3+3+2)" over "Dance" and "Food"; "4.
            # January (1), February (1), March (1) and April (1) 4 marks".
            live.add(part.lead)
            part.seq = [['ans', part.lead, False, False]] + list(part.seq)
            part.lead = None
            restored = lead_restored = True
    # A bracket opened on one held-aside line and closed on the next is one
    # line: "(Get information/discounts/much" / "More 1 mark)".
    seq = []
    for e in part.seq:
        if (seq and e[0] == 'cand' and seq[-1][0] == 'cand'
                and seq[-1][1].count('(') > seq[-1][1].count(')')):
            seq[-1] = ['cand', f'{seq[-1][1]} {e[1]}', False, seq[-1][3]]
            continue
        seq.append(list(e))
    last = None             # 'ans', 'head' or 'note': what a wrapped line goes on from
    parent = None           # a heading over headings ("Bruno's Mother:" over "Passage:")
    in_nb = False
    pending = None          # a bracket still open
    for at, (kind, text, wrapped, bulleted) in enumerate(seq):
        printed = text
        text = STRAY.sub('', text)
        if pending is not None:
            # The rest of a bracket opened on an earlier line.
            pending = f'{pending} {text}'
            if pending.count('(') <= pending.count(')'):
                _bracketed(part, pending)
                pending = None
            continue
        # The lines under "NB= Either:" are the rule it states, not answers.
        if in_nb and kind in ('ans', 'cand') and (bulleted or wrapped or text.startswith('*')):
            part.notes[-1] += ('; ' if bulleted else ' ') + text
            continue
        in_nb = False
        if re.match(r'^\d\s*pts?\s+from\b', text, re.I):
            # The rule under "NB= Either:" (2017 Higher B2A Q5): "3 pts from
            # passage + 1 pt from novel", one line each.
            if last == 'rule':
                part.notes[-1] += f'; {text}'
            else:
                part.notes.append(text)
            last = 'rule'
            continue
        if ((kind in ('head', 'cand') or not bulleted) and INSTRUCTION.search(text)) \
                or (kind in ('head', 'cand') and ECHO.search(text)):
            half = re.match(r'^((?:points?\s+)?from\s+the\s+(?:passage|novel|text))\s+(\S.*)$', text, re.I)
            if half:
                # "From the passage The candidate must refer both to the
                # passage and to the text as a whole": the half it heads, and
                # the instruction printed after it.
                part.notes.append(half.group(2))
                text, kind = half.group(1), 'head'
            else:
                part.notes.append(text.rstrip())
                in_nb = bool(re.match(r'^N\.?\s?B', text))
                last = 'note'
                continue
        if (text.startswith('(') and not bulleted and text.count('(') > text.count(')')
                and not BRACKET_MARK.search(text)):
            pending = text              # "(A cycling event/For cycling" over "(enthusiasts) 4 marks)"
            continue
        if kind == 'cand':
            closed = CLOSED_RUNG.match(text)
            if closed and int(closed.group(2)) < part.total:
                part.rungs.append((closed.group(1), int(closed.group(2))))
                continue
            if ASIDE.search(text):
                part.asides.append(text)
                continue
            priced = PRICED_HEAD.match(text)
            if priced:
                name = priced.group(1).strip()
                terms = [int(x) for x in re.findall(r'\d{1,2}', priced.group(4))]
                part.prices[name] = (COUNT_WORD[priced.group(2).lower()], int(priced.group(3)), terms, text)
                heads.append(name)
                groups.append([name, [], parent])
                last = 'head'
                continue
        # The stem every answer completes, when it is the only such line:
        # "They can" over "spend time together", "hug a tree" …; "She lived:"
        # over "in a small town", "in the west of Ireland" …
        if kind in ('cand', 'head') and at == 0 and not part.lead:
            after = [e[1] for e in seq[1:] if (e[0] == 'ans' or (e[0] == 'cand' and _opens_wrapped(e[1])))
                     and not e[1].startswith('(') and not CLOSED_RUNG.match(e[1])]
            others = [e for e in seq[1:] if e[0] in ('cand', 'head')
                      and not CLOSED_RUNG.match(e[1]) and not ASIDE.search(e[1])
                      and not e[1].startswith('(') and not INSTRUCTION.search(e[1])
                      and not _opens_wrapped(e[1])]
            if (after and not others and len(after) >= (part.claim or 1)
                    and text[:1].isupper() and all(_opens_wrapped(a) for a in after)):
                part.lead = text.rstrip(': ').strip()
                part.stem = True
                continue
        # What the paper prints is a heading whatever its shape: the line above
        # "Disadvantage" in the scheme is a ladder of lesser answers, so in
        # the list it sits under an answer that does not end in a full stop.
        shaped = (not bulleted and at + 1 < len(seq)
                  and seq[at + 1][3] and seq[at + 1][0] == 'ans')
        if kind == 'head' or (kind == 'cand' and _printed_in(text, question, shaped)):
            if last == 'head' and groups[-1][0] and not groups[-1][1]:
                parent = groups.pop()[0]        # a heading over the headings under it
            heads.append(text)
            groups.append([text, [], parent])
            last = 'head'
            continue
        # A heading printed INSIDE each of a run of answers: 2017 Higher A Q5
        # sets "Riccardo: he is not very interested in art, …" for every point
        # on the second half of its ask. The answers keep their words; the
        # run is a group of its own.
        inline = re.match(r'^([^:]{2,30}):\s', text) if kind == 'ans' else None
        if (inline and text in live and groups[-1][0] != inline.group(1)
                and _run(seq, text, inline.group(1)) >= 2
                and _printed_in(inline.group(1), question)):
            heads.append(inline.group(1))
            groups.append([inline.group(1), [], parent])
            part.inline.add(inline.group(1))
        # The tail of the answer above it: flagged when _settle read it, or the
        # answer above left a bracket open ("… Albanian name (1m) (meaning" /
        # "“mountain wind”)").
        if kind == 'cand' and last == 'ans' and (wrapped or out[-1].count('(') > out[-1].count(')')):
            out[-1] = f'{out[-1]} {text}'
            groups[-1][1][-1] = out[-1]
            continue
        if kind == 'ans' and printed not in live:
            continue        # taken off by _lead: the stem every option completes
        closed = CLOSED_RUNG.match(text) if (kind == 'ans' and not text.startswith('(')
                                             and text.count(')') > text.count('(')) else None
        if closed:
            # A shorter answer printed without its opening bracket ("The
            # seaside 1 mark)"); at the full price it is another full answer
            # ("Quadruple rooms in a hostel/ A hostel with kitchen facilities 4
            # marks)").
            if int(closed.group(2)) < part.total:
                part.rungs.append((closed.group(1), int(closed.group(2))))
                continue
            text = closed.group(1)
            restored = True
        if text.startswith('(') and (kind == 'ans' or not bulleted):
            if text.count('(') > text.count(')') and not BRACKET_MARK.search(text):
                # "(The answers “For six months after purchase” … will only be
                # acceptable as an answer in" / "Question 4. if not used …)".
                pending = text
                continue
            whole = re.match(r'^(\(.*\))\s*(\*.*)?$', text)
            if whole and whole.group(1).count('(') == whole.group(1).count(')') \
                    and _balanced_outer(whole.group(1)):
                _bracketed(part, text)
                continue
        if (last == 'ans' and out[-1].count('(') > out[-1].count(')')
                and text.count(')') > text.count('(')):
            # One answer the SEC bulleted twice: "She doesn't spend too much
            # time (less than 30" / "• minutes) creating the stories".
            out[-1] = f'{out[-1]} {text}'
            groups[-1][1][-1] = out[-1]
            whole = out[-1]
            if whole.startswith('(') and whole.endswith(')'):
                # The joined line is a bracket of its own: a lesser answer
                # with its marks ("(She took / Irish (cultural) classes 2
                # marks)") or the examiner's condition.
                out.pop()
                groups[-1][1].pop()
                closed = CLOSED_RUNG.match(whole)
                if closed:
                    part.rungs.append((closed.group(1), int(closed.group(2))))
                else:
                    part.asides.append(whole)
                last = 'ans' if out else None
            continue
        if kind == 'cand':
            # A restored answer printed with its own price ("Standard tickets
            # cost €10 and concession tickets cost €9 2 marks").
            priced = re.match(r'^(.*\S)\s+(\d{1,2})\s*marks?\s*$', text)
            if priced and int(priced.group(2)) == (part.split or [part.total])[0]:
                text = priced.group(1)
            restored = True
        required = REQUIRED.search(text)
        if required:
            # "You can spend (500€) on cultural events … (2 elements required)":
            # the condition is the examiner's, quoted in the note.
            cond = required.group(0).strip()
            text = text[:required.start()].rstrip()
            words = ' '.join(text.split()[:6])
            part.notes.append(f'§The scheme prints “{cond}” after the answer beginning “{words}”.')
        out.append(text)
        groups[-1][1].append(text)
        last = 'ans'
    # An answer a repair set after the read (it_more's UNWELD) was never in
    # the printed sequence: it stays where the repair put it.
    seen = {e[1] for e in part.seq if e[0] == 'ans'}
    for a in part.answers:
        if a not in seen:
            out.append(a)
            groups[-1][1].append(a)
    if not out and part.lead and not heads:
        # What was read as the head line's heading was the answer: 2025
        # Ordinary A1 3(b) prices "20 to 30 years old/Young people 2 marks"
        # and prints only a lesser answer under it.
        out, part.lead = [part.lead], None
        groups[0][1].append(out[0])
    if pending is not None:
        part.asides.append(pending)
    prices_each = [sum(int(m.group(1)) for m in BRACKET_MARK.finditer(a)) for a in out]
    uniform = (len(out) > 1 and all(prices_each) and len(set(prices_each)) == 1
               and part.total % prices_each[0] == 0 and part.total > prices_each[0])
    if uniform and not part.counted and not part.split and restored:
        # Every answer printed with the same price, "It's (very) flexible
        # (2m)", "He can work (1) from home (1m)" …: separate answers, as many
        # wanted as the total holds; and a line at that price the reader took
        # for a shorter answer is one of them ("He never feels alone (2m)").
        v = prices_each[0]
        part.claim = part.total // v
        back = [t for t, m in part.rungs if m == v]
        part.rungs = [(t, m) for t, m in part.rungs if m != v]
        out.extend(back)
        groups[-1][1].extend(back)
    if lead_restored and len(out) > 1 and groups[0][1][:2] == out[:2] and not uniform:
        a, b = out[0], out[1]
        share = (part.split[0] if part.split and len(set(part.split)) == 1 else part.total)
        priced = sum(int(m.group(1)) for m in BRACKET_MARK.finditer(a))
        more = sum(int(m.group(1)) for m in BRACKET_MARK.finditer(b))
        if (a.rstrip().endswith((',', '/', '-', '–')) or CONTINUED.search(a) or _opens_wrapped(b)
                or (priced and priced < share and priced + more == share)):
            # The head line's answer runs on to the next line: "30% off on all
            # books (in the collection)," / "until the 13th of November"; "The
            # (percentage) increase (1) in cyclists (2)" / "since 2011 (2)".
            out[:2] = [f'{a} {b}']
            groups[0][1][:2] = [out[0]]
    part.answers = out
    if not part.counted and len(out) == 1:
        part.claim = None       # one answer left: a point, not a choice of one
    if (not part.counted and restored and part.split and len(set(part.split)) == 1
            and len(part.split) > 1 and len(out) >= len(part.split) and sum(part.split) == part.total):
        part.claim = len(part.split)    # "4 marks (2+2)" over two answers: both
    # One answer the scheme cuts by an unequal split, read whole once its
    # first half is no longer taken for a heading: 2026 Higher B2B 4(a)
    # "5 marks (4+1)" over "Per riconoscerli" / "Così che quando tornano …".
    part.components = bool(restored and not part.counted and part.split
                           and len(set(part.split)) > 1 and len(part.split) == len(out)
                           and sum(part.split) == part.total and not heads
                           and not any(BRACKET_MARK.search(a) for a in out))
    # A group is named by its parent heading where it has one ("Bruno's
    # Mother:" over "Passage:" and "Novel:"); the sub-heading goes in the note.
    named = []
    for name, answers, par in groups:
        if not answers:
            continue
        label = par or name
        if label:
            full = label.rstrip(': ').strip()
            label = re.sub(r'\s*\((?:[^)\s]+\s+){3,}[^)]*\)\s*$', '', full).strip() or full
            part.fullnames.setdefault(label, full)
            if par and name:
                part.fullnames[label] = full
        if named and named[-1][0] == label and par:
            named[-1][1].extend(answers)
        else:
            named.append([label, list(answers)])
    headed = [g for g in named if g[0]]
    # One heading the scheme marks, over the second run of answers only: 2025
    # Higher B2A Q5 prints its passage points under "The candidate must refer
    # both …" and its novel points under "Points from the novel:".
    lone = (len(headed) == 1 and named[0][0] is None
            and any(e[0] == 'head' and e[1].rstrip(': ').strip().startswith(headed[0][0]) for e in seq))
    part.groups = named if (len(headed) > 1 or lone) else None
    sub = [n for n, _a, p in groups if p and n and _a]
    if sub:
        part.notes.append('§Under each heading the scheme prints its points under '
                          + ' and '.join(f'“{x.rstrip(": ")}”' for x in dict.fromkeys(sub)) + '.')
    heads = [h for h in heads if h]
    part.label = ' / '.join(([part.lead] if part.lead else []) + [g[0] for g in headed]) or None
    if part.groups:
        # A hyphen the SEC sets as a bullet under a heading ("- Manno: …").
        unhyphen = lambda a: a[1:].strip() if re.match(r'^-\s+\S', a) else a
        part.answers = [unhyphen(a) for a in part.answers]
        for g in part.groups:
            g[1] = [unhyphen(a) for a in g[1]]
    if part.claim is None and len(part.answers) > 1:
        part.claim = 1


def _completes(line, value, whole):
    """Whether `line` is a full answer cut short: its bracketed marks stop `value`
    short of one answer's worth, and the last of them sits mid-line."""
    body = INLINE_SPLIT.sub('', line).strip()
    marks = list(BRACKET_MARK.finditer(body))
    return bool(marks) and marks[-1].end() < len(body.rstrip()) \
        and sum(int(m.group(1)) for m in marks) + value == whole


def _recut(ask, alt):
    """Take the minimally-cut answers wherever the aggressive cut fell short.

    A component that states how many answers it wants is its own check on the
    cut: where the aggressive join leaves fewer answers than the directive asks
    for, the SEC was printing a list rather than wrapping a sentence, and the
    minimal cut is the one to keep. Where the counts agree, nothing moves.
    """
    if len(ask.parts) != len(alt.parts):
        return
    for part, other in zip(ask.parts, alt.parts):
        if not part.claim or len(part.answers) >= part.claim:
            continue
        if len(other.answers) < part.claim:
            continue
        part.answers, part.rungs = other.answers, other.rungs
        part.seq = other.seq
        part.lead = part.lead or other.lead
        part.label = part.label or other.label
        _lead(part)


def _lead(part):
    """A lead-in line the options each complete, moved off the option list.

    "1. (a) Three of: 9 marks" then "That the beaches have" then six lines
    starting "boardwalks on the sand". The first line is not an answer a
    candidate could give; it is the stem of all six. Left in the list it is a
    claimable option that says nothing, and prefixing it onto each option would
    put wording on the card that the scheme prints nowhere as one run — so it
    moves to the row's own label instead, where the provenance gate does not
    read it and a student still sees it.
    """
    if not part.claim or not part.answers:
        return
    first = part.answers[0]
    if len(part.answers) - 1 >= part.claim and CONTINUED.search(first) \
            and len(first.split()) <= 8:
        part.label = part.lead = first
        part.stem = True
        part.answers = part.answers[1:]


def _rung(text):
    """(text, marks) for a lesser answer — the mark taken off, never invented."""
    s = text.strip()
    m = TRAILING_MARK.search(s)
    marks = int(m.group(1)) if m else None
    body = s[:m.start()] if m else s
    body = body.strip().lstrip('(').strip()
    body = re.sub(r'[)\s]+$', '', body)
    return (' '.join(body.split()), marks)


# A printed line that stops mid-phrase, so the line under it finishes it. The
# test is the LAST WORD, against a closed list of function words in the two
# languages this scheme answers in, plus a line ending in a comma, a slash or a
# hyphen.
#
# A closed list rather than "short and lower case": 2023 Ordinary answers "Give
# two details about Samantha's personality" with "Willing to learn / Motivated
# / Loves her job / Enterprising", and "job" is three lower-case letters at the
# end of a finished answer. "un" is not.
CONTINUES = set("""
un uno una il lo la i gli le di del dello della dei degli delle
a al allo alla ai agli alle da dal dalla dallo dai in nel nella nelle nei
con col su sul sulla sui per tra fra e ed o che chi cui non si ci ne
come dove quando ma se sono ha hanno era erano essere fare
puo puoi possono deve devono
the of to and or for with is are was were that this these those their his her
its from on at by as be been has have had not but if so into about out up
can could may might must will would should do does did
throughout during until than towards within without
""".split())
# NOT the comma. The SEC ends an option with one — 2024 Ordinary answers "give
# three details" with "Like Ivy, she painted/drew from an early age," and four
# more lines just like it — and treating a trailing comma as a wrap welded all
# five into a single answer on a three-answer ask.
CONTINUED = re.compile(r"[/\u2013-]$|\b(?:" + '|'.join(sorted(CONTINUES)) + r")$", re.I)
# The wrap a MINIMAL join still makes: a line the SEC broke inside a word or
# inside a solidus list. Nothing about capitalisation, nothing about function
# words — just the two marks that cannot end a printed answer.
HARD_WRAP = re.compile(r'[/\u2013-]$')


def _join(lines, mode='wrap'):
    """Printed lines with the SEC's own wraps put back together.

    Two modes, because the SEC breaks a line for two different reasons and one
    rule cannot tell them apart from the text alone. The PDF cannot either: on
    2024 Ordinary page 8 its options and its wrapped continuations both start
    at x=115 and both stop far short of the measure, so there is no geometry to
    read and no right margin to test.

    `wrap` assumes a line opening in lower case, or sitting under a line that
    ended on a function word, finishes the line above it. That is right where
    the SEC wraps a long answer: "Basta cliccare sul pulsante “dona” e
    “ricevi” (3m) per donare o ricevere/richiedere un" / "PC/tablet gratuito
    (2m)" is one answer in two printed lines.

    `list` assumes almost nothing: only a line broken inside a word or inside a
    solidus list is a wrap. That is right where the SEC prints a menu in lower
    case — "That the beaches have" / "boardwalks on the sand" / "accessible
    toilet facilities" — which `wrap` welds into a single answer.

    Which one is right is decided by the scheme's OWN COUNT: `_settle` joins in
    `wrap`, and where that leaves fewer answers than the printed directive asks
    for, re-cuts in `list`. The directive is the arbiter here, the same way the
    printed section total is the arbiter of the tariffs.
    """
    out = []
    for raw in lines:
        s = raw.strip()
        # The extractor's page markers and the SEC's own page numbers are
        # dropped BEFORE joining, not after. Joined first, "10" and "## Page
        # 11" landed in the middle of the one 2021 Ordinary answer the SEC
        # printed across a page break, and no card could quote it.
        if SECTION_LINE.match(s):
            break           # the next section's head, and its front matter after it
        if not s or PAGE.match(s) or BARE_BRACKET_NUM.match(s):
            continue
        # A line holding nothing but a bracketed mark is the tail of the answer
        # above it — 2021 Higher A 3(b) sets its second half's "(3m)" on a line
        # of its own — and read as an answer it is a marking point with no
        # content at all.
        head = s.lstrip('(')[:1]
        # A line OPENING with a bracketed mark finishes the answer above it:
        # 2024 Higher A 1(a) sets "È una campagna italiana (1m) che ha
        # l'obiettivo di proteggere almeno il 30% del nostro mare" and
        # "(2m), entro il 2030 (2m)." as one answer over two printed lines.
        joins = bool(out) and bool(MARK_ONLY.fullmatch(s)
                                   or MARK_OPENS.match(s)
                                   or s.startswith('/')
                                   or HARD_WRAP.search(out[-1]))
        if mode == 'wrap' and out:
            joins = joins or head.islower() or bool(CONTINUED.search(out[-1]))
        # Never onto a line that is complete in itself: a bare directive ("Two
        # of" over the heading "Solutions"), or a lesser answer ending on its
        # own marks ("… 3m" over "she did not make a lot of friends 3m"); and
        # never a bracketed lesser answer onto the answer above it ("His team
        # mates all love her" over "(She (always) helps/supports him 2 marks)").
        # A bracketed shorter answer printed over two lines: "(A cycling
        # event/For cycling" / "(enthusiasts) 4 marks)".
        if out and out[-1].startswith('(') and out[-1].count('(') > out[-1].count(')'):
            joins = True
        if out and (DIRECTIVE.match(out[-1]) or BARE_MARK.search(out[-1])
                    or (PAREN_RUNG.match(s) and s.startswith('(') and s.rstrip().endswith(')')
                        and not out[-1].startswith('('))):
            joins = False
        if (out and joins and not LADDER.match(s) and not LADDER.match(out[-1])
                and not BULLET.match(s) and not PAGE.match(s)):
            out[-1] = f'{out[-1]} {s}'
            continue
        out.append(s)
    return out


# ------------------------------------------------------------------ audit ----
def audit(subject=SUBJECT, verbose=False):
    bad = 0
    for path in sorted(glob.glob(os.path.join(schemes_dir(subject), '*.md'))):
        stem = os.path.basename(path)[:-3]
        year, level = int(stem[:4]), stem[5:]
        S = ItScheme(year, level, subject)
        print(f'{stem}: {len(S.asks)} priced asks, {len(S.refused)} refused')
        for token in sorted({a.section for a in S.asks}):
            asks = S.by_section(token)
            printed = S.section_totals.get(token)
            got = sum(a.total for a in asks if a.total)
            flag = ''
            if printed is not None and any(a.total for a in asks) and got != printed:
                flag = '   <-- MISMATCH'
                bad += 1
            print(f'    {token:<4} {len(asks):>3} asks, heads sum {got:>3}, '
                  f'printed {printed}{flag}')
            if verbose:
                for a in asks:
                    print(f'        {S.ref(a):<34} {a.total:>3} in '
                          f'{len(a.parts)} part(s): '
                          + '; '.join(f'claim={p.claim} split={p.split} '
                                      f'{len(p.answers)} ans {len(p.rungs)} rung'
                                      for p in a.parts))
        for head, why in S.refused:
            print(f'    REFUSED {head}: {why}')
            bad += 1
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('--subject', default=SUBJECT)
    ap.add_argument('--audit', action='store_true')
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--full', action='store_true')
    ap.add_argument('--section')
    args = ap.parse_args()
    if args.audit or not args.year:
        return audit(args.subject, args.verbose)
    S = ItScheme(args.year, args.level, args.subject)
    print(f'{args.year} {args.level.upper()}: {len(S.asks)} asks; '
          f'section totals {S.section_totals}')
    for a in S.asks:
        if args.section and a.section != args.section:
            continue
        print(f'  {S.ref(a):<34} total={a.total}')
        for p in a.parts:
            print(f'      PART {p.notation!r} split={p.split} claim={p.claim} '
                  f'per={p.per} label={p.label!r}')
            if p.directive:
                print(f'      DIR  {p.directive}')
            if args.full:
                for ans in p.answers:
                    print(f'      *    {ans[:150]}')
                for text, marks in p.rungs:
                    print(f'      -    [{marks}] {text[:130]}')
        if args.full:
            for n in a.notes:
                print(f'      NOTE {n[:120]}')
    for head, why in S.refused:
        print(f'  REFUSED {head}: {why}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
