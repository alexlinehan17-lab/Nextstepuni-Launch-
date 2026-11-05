#!/usr/bin/env python3
"""Author every Technology part the scheme states and prices.

    python3 scripts/markbank/authoring/tech_all.py --report    # counts, refusals
    python3 scripts/markbank/authoring/tech_all.py > scripts/markbank/authored/technology.json

Census-driven, like Engineering and Computer Science: 809 asks is far too many
to enumerate by hand, and every card is the scheme's own text against the
paper's own ask.

WHAT THE PAIRING RESTS ON. Law 4 refuses a join made on the (question, letter,
roman) key alone, and this subject does not need one. The scheme REPRINTS the
question above its answer, so each priced part carries a cue in the question's
own words, and `tech_scheme.cue_score` scores that cue against the paper's ask
for the address the scheme printed. `--report` prints the confirmation rate per
sitting; a part whose cue contradicts its address is refused rather than
carded. Where the scheme prints no cue at all -- it sometimes goes straight to
the answer, "1(c) (i) CAD: Computer aided drawing/drafting" -- the address is
all there is, and those are counted and named separately so the number is
visible rather than assumed.

WHAT THE TARIFF MEANS. The scheme prints one of three shapes and each maps to
one deck convention. None is inferred:

  "(6 marks, 2 + 4)"  over (i) and (ii)   the split names what each part is
                                          worth: (i) 2, (ii) 4 -> a card each,
                                          at its own printed mark.
  "(6 marks, 2+2+2)"  over no parts       the question is one ask with three
                                          named answers -> one card, one row
                                          per answer, at the split's marks.
  "(6 marks)"                             one card at six, rows carrying no
                                          mark of their own (questionTotal).

A split whose term count does not match what the block prints is NOT divided:
the card states the total the scheme prints and claims nothing in between.

REFUSALS, each a named bucket `--report` counts with a real example.
"""
import argparse
import collections
import json
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

import cardlint                                              # noqa: E402
import paper_census as PC                                    # noqa: E402
from tech_scheme import TechScheme, cue_score, normalise as SCHEME_NORM, _words as SCHEME_WORDS  # noqa: E402
from tech_topics import topic_for, topic_for_option, TOPIC_OVERRIDES  # noqa: E402
import tech_crops as TC                                      # noqa: E402

SUBJECT = 'technology'
MAX_ROWS = 16
# Mirrors MAX_LONG_OPTION_ROWS / MAX_OPTION_ROWS in optionCap.mjs.
CAP = {'A': 8, 'B': 16, 'C': 16}

LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}

# A scheme line that states no answer. Each of these shipped as a card's whole
# answer in some other subject before it was gated.
# A bare "Any two:" is the examiner saying how many of the lines below to
# credit. "Any two, solar, wind, etc." is not: it NAMES them, and the count is
# only its opening words. Dropping both cost seven parts their whole answer.
NOT_A_POINT = re.compile(
    r'^(?:any (?:other|valid|two|three|one|four)(?:\s+of\s+the\s+following)?'
    r'\s*[:.\u2013-]?'
    r'|accept(?:able)?\b.{0,30}'
    r'|award\b|allow\b|note:|marks? awarded'
    r'|suggested\b.{0,20}'
    r'|or\b|and\b|etc\.?'
    # The choice rubric between parts: "Answer 2(c) or 2(d)".
    r'|answer\s+\d\([a-d]\)\s+(?:and|or)\s+\d\([a-d]\)'
    r'|[^.?!]{0,28}:)\s*$', re.I)

# A scheme line that is nothing but a bulleted label: "• Rehabilitation from
# injury:".
BULLET_LABEL = re.compile(r'^[\u2022\u25aa\u25cf\u25e6]\s*[^:\u2022]{2,60}:$')

# The examiner's closing remark on a list -- "Suggested elements, other
# viable answers accepted." under 2026 Higher Q11's three -- is not a fourth
# element. It is dropped only where other points stand: where it is the
# scheme's ONLY line (2021 Higher Q13: "Any valid view of the assembled
# console is accepted.") it is what earns the marks, and stays.
ACCEPTED_NOTE = re.compile(r'^(?:suggested|any)\b.{0,80}\baccepted\.?\s*$', re.I)

# A worked calculation states an answer without ever using a word: "F x 0.5 M
# = 50 N x 0.8 M", "1000 ohm". The letters-only test threw away every line of
# the arithmetic on eleven parts, and then refused the part for stating
# nothing.
CALCULATION = re.compile(r'\d.*[=\u2248]|[=\u2248].*\d'
                         # An algebraic step with no figure in it: "F x D =
                         # Effort x D" above "250 x 50 = Effort x 250" (2026
                         # Higher 9(i)) is a step of the working, not prose
                         # that wraps onto the line below.
                         r'|^[A-Z][A-Za-z.]*(?:\s*[x\u00d7/+\-]\s*[A-Za-z.]+)+\s*='
                         # Both ohm signs: the SEC's text layer gives U+2126 OHM SIGN in one
                         # scheme and U+03A9 GREEK CAPITAL OMEGA in another, and
                         # "1000 ohm" is the whole answer to 2022 Ordinary Option 2(a)(i).
                         r'|\d\s*(?:[\u03a9\u2126\u00b5]|ohms?|[VWANJ]|Hz|kHz|mA|kW|RPM)\b')

# The running footer, and the page number the extractor leaves welded to a
# marking point's last line.
# Only the footer's own form -- "Leaving Certificate Examination 2026",
# "Leaving Certificate, 2020" -- never the words inside an ask: 2023 Ordinary
# Q10 ends "...a design portfolio for Leaving Certificate Technology." and was
# cut to "...portfolio for".
FOOTER = re.compile(
    r'\s*\d{0,3}\s*Leaving Certificate(?:\s+Examination)?,?\s*20\d\d\b.*$'
    # The 2021 Ordinary booklet's hidden footer tag, printed white at the foot of
    # pages 3 and 5 and read onto the end of Q12's ask.
    r'|\s*page\s+running\s*$'
    r'|\s*Technology\s*[-–—]\s*(?:Higher|Ordinary)\s+Level.*$'
    r'|\s*Please turn over\b.*$|\s*Do not write on this page\b.*$'
    # The facing page's own notice, read onto the last question of the
    # booklet (2017 Higher Q15).
    r'|\s*Blank Page\s*$'
    # The 2010-2018 Sections B/C booklet's page footer, "Page 7 of 9".
    r'|\s*Page\s+\d+\s+of\s+\d+\s*$', re.I)

# A cue too short to identify anything: "Modification:", "Calculation:".
# An ask that names its subject only by pointing back at the stimulus:
# "Name the machine.", "State two safety precautions ... using this machine."
# Dropping the stem under one of these leaves a question nobody can answer,
# which is a different thing from dropping context nobody needs.
LEANS_ON_STEM = re.compile(
    r'\b(?:this|these|the)\s+(?:machine|tool|mechanism|device|component|image'
    r'|graphic|photograph|product|item|object|system|diagram|circuit|sign'
    r'|structure|symbol|material|screen|table|chart|graph|drawing|sketch'
    r'|assembly|arrangement|layout)\b', re.I)

# An ask that stops mid-phrase: the reader lost the rest of the sentence.
CUT_SHORT = re.compile(
    r'\b(?:in|of|the|and|to|on|for|with|at|a|an|as|by|from|that|which|when'
    r'|is|are|be|its|their|this|these)\s*$', re.I)

# The answerbook's fill-in label left at the end of an ask once the labels
# printed inside the picture have come off: "...circuit shown. Calculation:".
# Only after a closed sentence -- "Explain each of the following in relation
# to DFA:" is the question's own colon.
TRAILING_LABEL = re.compile(r'(?<=[.?!])\s+[A-Z][a-z]{2,}:\s*$')

# A figure's caption, filed as a stem by the walker because it is printed
# between a part's head and its romans: "cable carousel cable loaded into
# carousel". A stimulus is a sentence; a caption closes nothing and is short.
CAPTION = re.compile(r'^(?:\S+\s+){0,7}\S*[^.?!:]$')


def flattened_table(text):
    """A table's cells read as prose: no sentence, half the tokens short."""
    words = text.split()
    if len(words) < 8 or re.search(r'[.?!]', text):
        return False
    # A lead-in that closes on its colon is a sentence, however long: "Analyse
    # the environmental impact of manually soldering a circuit as part of a
    # technology project in terms of:" (2016 Higher Q7) is no table.
    if text.rstrip().endswith(':') and sum(1 for w in words if re.fullmatch(r'[a-z]{2,}', w)) >= 0.6 * len(words):
        return False
    # Twelve words with no sentence among them is a table (the 2024 Higher
    # resistor colour code), however long its cells.
    return len(words) >= 12 or sum(1 for w in words if len(w) <= 3) >= 0.5 * len(words)

MIN_CUE_WORDS = 4
# How much of the scheme's cue the paper's ask must hold before the pairing
# counts as confirmed by wording rather than by address.
CUE_FLOOR = 0.5


def clean(text):
    text = FOOTER.sub('', ' '.join((text or '').split())).strip()
    # A stray backtick the 2019 Higher scheme sets after 4(b)(iii)'s last
    # line of working ("= €570,000 `"): it is no character of the answer.
    text = re.sub(r'\s+`$', '', text)
    return ' '.join(text.split())


# The answerbook's ruled writing lines, and the fill-in label that heads each
# of them. Technology prints them INSIDE the question block -- "State the
# meaning of each colour code. Red colour-coded sign: ______ Yellow
# colour-coded sign: ______" -- so they arrive as part of the ask.
BLANK_RULE = re.compile(r'[_\u2581\u00b7.]{3,}')
FILL_LABEL = re.compile(r'\s*[^.?!:]{1,40}:\s*$')


def clean_ask(text):
    """The printed question, with the answerbook's blank lines taken off.

    Not cosmetic. The labels above those blanks repeat the answer's own
    headings, so a scheme line stating the answer -- "Red colour-coded sign:
    Prohibition" -- reads as a REPRINT of the question and the whole answer
    was thrown away with it. Five Ordinary questions lost every marking point
    they had that way.
    """
    raw = text or ''
    text = clean(BLANK_RULE.sub(' ', raw))
    # The choice rubric that follows an either/or part -- the paper prints
    # "Answer 5(c) or 5(d)" above them and a standalone "OR" between them, and
    # the trailing one welds onto the end of (c)'s last ask. Fifteen cards
    # ended "... on the presentation box. OR".
    text = re.sub(r'\s+OR\s*$', '', text)

    # Only where the answerbook's ruled lines were actually there. A trailing
    # colon is ALSO how a question introduces its own bullet list -- "Explain
    # each of the following in relation to DFA:" -- and stripping that left
    # the word "Explain" as the whole question on two cards, which the build
    # then dropped as too short to stand alone.
    if not BLANK_RULE.search(raw):
        return text
    while True:
        m = FILL_LABEL.search(text)
        # A label follows the sentence it belongs under, or the label before
        # it. Anything else is the question's own words.
        if not m or m.start() == 0 \
                or not re.search(r'[.?!:]\s*$', text[:m.start()]):
            return text
        text = text[:m.start()].strip()


NUMBER = re.compile(r'\d[\d,.]*\d|\d')


def _tokens(text):
    return re.findall(r"[a-z0-9']+", (text or '').lower())


def split_cue(lines, ask):
    """(the question the scheme reprinted, the marking points under it).

    The scheme sets the ask again above its answer, at the same indent, so
    nothing in the geometry separates them -- the paper's own wording does,
    which is the argument lib.py's _TableSource makes for Chemistry. This
    consumes the paper's ask WORD BY WORD, in order: a scheme line is part of
    the reprint only while its words carry on through the ask from where the
    line before it stopped, and the reprint is over the moment the ask is
    used up.

    Bag-of-words overlap is not enough, and the difference is not cosmetic. A
    calculation's answer reuses the question's own nouns -- "Total energy =
    (50 watts/hour x 4 hours) x 0.15 = 30 watt/hour" against "Calculate the
    total energy a solar panel generates in 4 hours..." -- so every word of it
    is "in the ask" and thirty-nine parts had their whole answer thrown away
    as a reprint. Reading in order stops at the full stop instead.
    """
    ask_words = _tokens(ask)
    ask_nums = {n.replace(',', '') for n in NUMBER.findall(ask or '')}
    cue, points, at = [], list(lines), 0
    while points and at < len(ask_words):
        line_words = _tokens(points[0])
        if not line_words:
            cue.append(points.pop(0))
            continue
        # A line that takes one of the ask's figures and brings a new one is
        # an answer, not the reprint: "A document of 196 KB 196,000 bytes."
        # (2016 Higher 12(ii)) under the ask's "A document of 196 KB".
        line_nums = {n.replace(',', '') for n in NUMBER.findall(points[0])}
        if line_nums & ask_nums and line_nums - ask_nums:
            break
        # ...and a numbered answer list opens with "1." above a "2.": the
        # scheme's ORDER of the ask's own items ("1. 100 kilobyte" over
        # "2. 1 gigabyte", 2016 Higher 12(i)), not the reprint.
        if re.match(r'1\.\s', points[0]) and len(points) > 1 and re.match(r'2\.\s', points[1]):
            break
        pos, matched = at, 0
        for word in line_words:
            window = ask_words[pos:pos + 12]
            if word in window:
                pos += window.index(word) + 1
                matched += 1
        if pos > at and matched >= max(2, int(0.6 * len(line_words))):
            cue.append(points.pop(0))
            at = pos
        elif cue and not re.search(r'[.?!:]$', cue[-1]) \
                and points[0][:1].islower():
            # The reprint wraps and paraphrases: 2026 Ordinary 4(b)(iii)
            # reprints "...at stage 4" / "of a products life cycle." where
            # the paper says "in the lifecycle of a product". A line that
            # opens in lower case under an unclosed cue line is the cue's
            # own sentence going on, never an answer.
            cue.append(points.pop(0))
        else:
            break
    if not points and cue:
        # The reprint consumed every line, which no priced block is: the
        # last line is the answer, however many of the ask's words it
        # reuses. 2026 Higher 4(b)(iii) answers "Determine the control state
        # of this process" with "The control state is in control.", and
        # read as a reprint the part had no marking point at all. The
        # caller is told which line this was, so the repeat filter does
        # not throw it away a second time for the same reason.
        points = [cue.pop()]
        BACKED_OFF.append(points[0])
    return ' '.join(cue), points


BACKED_OFF = []


def strip_ask_label(point, ask):
    """A row that opens with the ask's own label is the scheme naming the
    part before answering it: "Edit images: Limited ability to edit images"
    under the ask "Edit images:" (2020 Higher 6(iii)), "cookie: Data sent from
    a website..." under "Explain the terms: cookie" (12(i)). The label comes
    off when it is the whole ask, or the ask's closing words, and an answer
    follows it on the line."""
    m = re.match(r'([^:]{1,40}):\s+(\S.*)$', point)
    if not m:
        return point
    label = ' '.join(m.group(1).split()).lower()
    bare = ' '.join((ask or '').rstrip(': ').split()).lower()
    # The whole ask, or what follows its last colon ("Explain the terms:
    # cookie"); never a heading the ask merely ends with ("...Man, Machine,
    # Method." keeps its "Method:" row distinct from the other two).
    if bare == label or re.search(r':\s*' + re.escape(label) + r'$', bare):
        # ...unless the ask closes on a RUN of labels ("Explain the terms:
        # CAM: CNC:"): stripping the last would leave one row labelled and
        # its sibling not.
        if re.search(r':\s*[^:]{1,40}:\s*' + re.escape(label) + r'$', bare):
            return point
        return m.group(2)
    return point


def question_label(covered):
    """The roman labels a card cites, as the scheme prints them beside them."""
    return ' '.join(k[3] or '' for k in covered)


def graphic_fragments(points):
    """Whether these "points" are a drawing the extractor read the words off.

    A flowchart's boxes come through as "Start", "Power on", "Toner empty
    Fuser temp. Wait correct", "Yes Yes" -- eleven rows a student would be
    asked to tick, not one of which states anything. What separates them from
    prose is that they are short AND they never close a sentence.
    """
    if len(points) < 4:
        return False
    # Two exceptions, both found by reading the twenty parts this first
    # refused. A WORKED CALCULATION is short and unpunctuated line by line
    # ("Series: R2 + R3 = 8k + 4k = 12k") and states its answer in every one
    # of them. And a BULLETED list is the scheme's own enumeration of accepted
    # answers, however tersely each is written.
    if sum(1 for p in points if CALCULATION.search(p)) >= 2:
        return False
    bullets = [p for p in points
               if p.lstrip().startswith(('\u2022', '-', '\u2013'))]
    # A bulleted list is an exception only when the list is what this part
    # holds. Three bullets among twelve fragments is the QUESTION's own
    # sequence, reprinted above a flowchart -- "the capsule is inserted N On?"
    # is one of the paper's bullets with a flowchart's decision box welded to
    # it, and the exception let three such cards through.
    if len(bullets) >= 2 and len(bullets) >= 0.6 * len(points):
        return False
    # ...and so is a NUMBERED one, "1. Marking out of parts." / "2. Drilling."
    # (2018 Ordinary Q9's four steps, priced "(4x2 marks)").
    numbered = [p for p in points if re.match(r'\d\.\s+\S', p.lstrip())]
    if len(numbered) >= 2 and len(numbered) >= 0.6 * len(points):
        return False
    # "People: Unskilled, in-experienced" -- a heading and its answer on one
    # line, three of them under 2026 Higher Q11's fishbone. Short, never
    # closed, and each one states something.
    # 2019 Ordinary 2(c)(i) gives the Deming stages with a DASH for the colon --
    # "Plan– identify problems", "Study- consider/examine the findings" -- the
    # same heading-and-answer line.
    # ...and an abbreviation spelled out, "EST - Earliest Start Time", "X -
    # EFT - Earliest Finish Time" (2014 Higher Q6's critical-path terms).
    labelled = [p for p in points
                if re.match(r'^[A-Z][A-Za-z /-]{1,24}:\s+\S', p)
                or re.match(r'^[A-Z][a-z]{1,24}\s?[\u2013\u2014-]\s+[a-z]', p)
                or re.match(r'^(?:[A-Z]\s[\u2013\u2014-]\s)?[A-Z]{2,6}\s[\u2013\u2014-]\s+[A-Z][a-z]+\s', p)]
    if len(labelled) >= 0.5 * len(points):
        return False
    short = [p for p in points if len(p) < 46]
    # A question mark closes a flowchart's decision box, not a sentence --
    # "N On?", "Large coffee?" -- and counting those as closed let three
    # flowchart cards through. Only a full stop on a line long enough to be a
    # sentence counts.
    closed = [p for p in points if p.rstrip().endswith(('.', '!')) and len(p) >= 30]
    return len(short) >= 0.7 * len(points) and len(closed) <= 0.25 * len(points)


# The examiner's own lead-in to an answer, which names nothing: it stays
# off the row (cardable drops it on its own line, as before).
EXAMINER_LEAD = re.compile(
    r'^(?:calculations?|suggestions?|suggested (?:solutions?|answers?)|such as'
    r'|modifications?|alternative solutions? acceptable|answers?|notes?|e\.g\.'
    r'|any (?:one|two|three|four)(?:\s+\w+)?|possible answers?|sample answers?)\s*:$', re.I)


def reflow(points, scheme_norm=''):
    """Put a marking point back together where the PDF broke it across lines.

    The scheme sets its answers as running prose and the extractor emits one
    line per printed line, so "Ergonomics is the science of designing and
    arranging objects, equipment, and / environments in a way that optimises
    human performance" arrived as two marking points and shipped as two rows a
    student is asked to tick separately. A line that does not close a sentence,
    or whose successor opens in lower case, is the same point continuing.
    """
    out = []
    for line in points:
        text = clean(line)
        if not text:
            continue
        if out and '=' in text and len(text) >= 6 and out[-1].rstrip().endswith(text.rstrip()):
            # A worked answer that opens by restating the formula the line
            # above ends with -- the ask's "Note: hFE = Ic / Ib", then the
            # scheme's "hFE = Ic / Ib" / "= 0.05 / 0.00025" (2014 Higher
            # Q5(ii)) -- starts its own point. Joined, the answer rode on the
            # reprint and was thrown away with it.
            out.append(text)
            continue
        if out:
            prev = out[-1]
            opens_lower = text[:1].islower() or text[:1] in ',;)'
            unclosed = not re.search(r'[.?!:;\u2022]$', prev)
            # "Web/content scraping:" above "gathers data or content from
            # websites..." is one point with its heading, not a heading the
            # filter below throws away and an answer that then names nothing.
            if prev.endswith(':') and opens_lower and not CALCULATION.search(text):
                unclosed = True
            # A bare heading -- "Product layout:", "Parallel:", "Method:" --
            # is the name of the point under it, not a point: it joins the
            # line below whatever case that opens in (2026 Higher 4(d)'s
            # three layouts, 2025 Higher 12). Longer and it is a sentence.
            heading = (prev.endswith(':') and len(prev) <= 40
                       and not re.search(r'[.?!]', prev) and not CALCULATION.search(text)
                       and not EXAMINER_LEAD.match(prev)
                       # A bulleted label is a heading at any length: the
                       # short-colon rule below would otherwise throw away
                       # "• Rehabilitation from injury:" (28 characters) as
                       # no point while "• Professional athletics and
                       # sports:" (35) joined its answer -- 2019 Higher 3(a)
                       # shipped its first row without its lead.
                       and (BULLET_LABEL.match(prev) or not NOT_A_POINT.match(prev)))
            if heading:
                joined = f'{prev} {text}'
                if not scheme_norm or SCHEME_NORM(joined) in scheme_norm:
                    out[-1] = joined
                    continue
            # A bullet, a heading and a new sentence all start their own point.
            # A worked calculation never closes a line and starts every
            # step with a figure, so the rule above read 2026 Higher 9(i)'s
            # five steps as one point. Two calculation lines stay two.
            steps = bool(CALCULATION.search(prev) and CALCULATION.search(text)
                         and not opens_lower
                         and not re.match(r'[=+\u00d7\u2212\u2013-]|x\s', text))
            # A line that stops on an article or a preposition is a sentence
            # the PDF broke, whatever the next line opens with: 2019 Higher
            # 2(d)(i) breaks "...and hence an" / "EMF is induced...", and the
            # capital split one answer into two rows, the first cut mid-phrase.
            dangling = unclosed and bool(CUT_SHORT.search(prev)
                                         or re.search(r'\b(?:e\.g|i\.e)\.,?$', prev))
            # A numbered answer, and a term with its dash-led gloss -- "video
            # output- with increased data-transfer speeds...", "charging - can
            # carry more power" (2019 Ordinary 3(b)(ii)) -- open points of their
            # own, whatever case they start in.
            # ("1: Mark out shape...", 2011 Ordinary Q10, numbers its steps
            # with a colon.)
            num = re.match(r'(\d)[.:]\s', text)
            own_point = bool((num and re.match(rf'{int(num.group(1)) - 1}[.:]\s', prev))
                             # the dash set hard against the term, or one word
                             # and a spaced hyphen: a dash with space before it
                             # is the sentence's own ("inserted when cool – it").
                             or re.match(r'[a-z][a-z ]{1,30}?[a-z][\u2013\u2014]\s+[a-z]', text)
                             or re.match(r'[a-z]+\s-\s+[a-z]', text))
            if unclosed and not steps and not own_point and (opens_lower or dangling or not re.match(
                    r'[A-Z\u2022\u2013-]', text)):
                joined = f'{prev} {text}'
                # And only where the JOIN is what the scheme prints. The two
                # lines are adjacent in the block, not always in the file --
                # a footer or a rubric can sit between them -- and a join
                # across one is a sentence the SEC never wrote. The build's
                # provenance gate caught three; asking it here means the card
                # keeps its rows instead of being dropped whole.
                if not scheme_norm or SCHEME_NORM(joined) in scheme_norm:
                    out[-1] = joined
                    continue
        out.append(text)
    return out


def cardable(points, scheme_norm=''):
    out = []
    for p in reflow(points, scheme_norm):
        t = clean(p)
        # A cell of a table the extractor flattened -- "12000", "(EUR)" --
        # states no answer, and the provenance gate rightly refuses it. One
        # WORD is enough to be an answer, though: "Transistor." is the whole
        # of 2024 Higher Q4(i), and demanding two threw it away.
        if len(t) < 4 or NOT_A_POINT.match(t) \
                or not (re.search(r'[A-Za-z]{3,}', t) or CALCULATION.search(t)):
            continue
        out.append(t)
    return out


def keeps_stem(stem, question):
    """Whether the stimulus above a part is worth showing on its card."""
    text = clean(stem)
    if not text or cardlint.label_junk(text):
        return False
    if len(text) < 20:
        return False
    # The stem repeats the ask on a whole-question leaf: the census hands the
    # same sentence back as both, and printing it twice looks like a defect.
    if text.rstrip('.') in (question or '').rstrip('.'):
        return False
    # Or the other way about: a whole-question stem that is the ask with the
    # answerbook's labels after it ("...State the meaning of each colour
    # code. Red colour-coded sign: Yellow colour-coded sign:").
    if question and question.rstrip('.') in text:
        return False
    return True


def leaf_key(section, q, letter, roman):
    return (section, q, letter, roman)


def ref_for(year, level, section, q, letter, roman):
    return (f'{year} {level.upper()} Section {section} Q{q}'
            + (f'({letter})' if letter else '')
            + (f'({roman})' if roman else ''))


def card_id(year, level, section, q, letter, roman):
    return (f'tech-{year}-{level}-{section.lower()}{q}'
            + (letter or '') + (f'-{roman}' if roman else ''))


def rows_for(points, marks, total, cap=MAX_ROWS, single_ask=True):
    """(rows, tariff model) for one card, or None to refuse.

    `marks` is the printed split for this card's own answers, when the scheme
    printed one that fits. Otherwise the card states the total and divides
    nothing -- the rule that has cost this bank five incidents when broken.
    """
    points = points[:min(cap, MAX_ROWS)]
    if marks is None and len(points) == 1 and single_ask:
        # One stated answer for a priced part: the part's tariff IS that row's
        # mark. Nothing is divided, so nothing is guessed.
        marks = [total]
    if marks and len(marks) == len(points):
        rows = [{'id': f'r-{i}', 'kind': 'point', 'verbatim': p, 'marks': m,
                 'openList': True}
                for i, (p, m) in enumerate(zip(points, marks), start=1)]
        return rows, {'kind': 'fixed'}
    rows = [{'id': f'r-{i}', 'kind': 'point', 'verbatim': p, 'marks': None,
             'openList': True}
            for i, p in enumerate(points, start=1)]
    return rows, {'kind': 'questionTotal'}


ROMAN_ORDER = ['i', 'ii', 'iii', 'iv', 'v']


def block_units(block, leaves, year, level):
    """The cards this priced block should become.

    One per roman where the printed split has a term for each of them -- the
    ordinary case, and the one that gives a student a card per ask. Otherwise
    ONE card for the whole block, citing every leaf under it and stating the
    block's own printed total. That second shape is not a fallback for
    convenience; it is what "never guess a tariff" requires when the split
    names more parts than the scheme printed markers for. 2022 Higher
    Question 13 prices "(6 marks, 2 + 2 + 2)" over (i) and (ii), because (ii)
    itself asks for two things, and no reading of that says what (i) is worth.

    Each unit is (roman or None, the scheme lines, this unit's tariff, the
    census leaf keys it covers).
    """
    section, q, letter = block.section, block.q, block.letter
    romans = block.romans()
    # Per-roman cards need the PAPER to print those romans too. Where it does
    # not -- 2021 Higher Question 8 is one ask on the page and two in the
    # scheme -- the whole-block card is the honest shape: it covers the leaf
    # the paper actually prints instead of citing two the paper does not.
    paper = sorted((k[3] for k in leaves
                    if k[0] == section and k[1] == q and k[2] == letter and k[3]),
                   key=lambda r: ROMAN_ORDER.index(r) if r in ROMAN_ORDER else 99)
    remap = {}
    if romans and paper and len(romans) == len(paper) and set(romans) != set(paper):
        # The scheme misprints a roman -- 2024 Higher 3(d) heads its two
        # parts "(i)" and "(iii)" for the paper's (i) and (ii) -- and the
        # block prints as many as the paper does: read them in printed order.
        remap = dict(zip(romans, paper))
    # A roman the scheme omits altogether -- no head, no answer (2016 Ordinary
    # 1(a)(ii)) -- while its split still prices it: tech_crops.UNPRINTED
    # names it, and the split is read over the paper's romans in order.
    missing = [r for r in paper if r not in romans
               and (year, level, section, q, letter, r) in TC.UNPRINTED]
    if romans and missing and not remap and set(romans) | set(missing) == set(paper) \
            and len(block.terms) == len(paper):
        return [(r, block.part_lines(r) if r in romans else [], block.terms[i],
                 [(section, q, letter, r)]) for i, r in enumerate(paper)]
    if romans and all(block.marks_for(r) is not None for r in romans) \
            and all((section, q, letter, remap.get(r, r)) in leaves for r in romans):
        out = []
        for roman in romans:
            out.append((remap.get(roman, roman), block.part_lines(roman), block.marks_for(roman),
                        [(section, q, letter, remap.get(roman, roman))]))
        return out
    # Whole block. Its leaves are whatever the PAPER prints under this
    # address -- the scheme's own roman markers are not to be trusted here,
    # which is half of why this shape exists.
    covered = sorted(
        (k for k in leaves
         if k[0] == section and k[1] == q and k[2] == letter),
        key=lambda k: ROMAN_ORDER.index(k[3]) if k[3] in ROMAN_ORDER else -1)
    if not covered:
        covered = [(section, q, letter, None)]
    return [(None, [t for _, t in block.lines], block.total, covered)]


def joined_ask(covered, leaves):
    """The paper's own wording for every leaf one card covers, in order."""
    if len(covered) == 1:
        return clean_ask(leaves.get(covered[0], ''))
    parts = []
    for key in covered:
        text = clean_ask(leaves.get(key, ''))
        if text:
            parts.append(f'({key[3]}) {text}' if key[3] else text)
    return ' '.join(parts)


def joined_ref(year, level, covered):
    section, q, letter = covered[0][0], covered[0][1], covered[0][2]
    head = (f'{year} {level.upper()} Section {section} Q{q}'
            + (f'({letter})' if letter else ''))
    romans = [k[3] for k in covered if k[3]]
    if not romans:
        return head
    return head + '(' + ')('.join(romans[:1]) + ')' + ''.join(
        f', ({r})' for r in romans[1:])


ARTICLE = re.compile(r'\b(?:the|a|an)\b', re.I)

# A quality band the scheme prints for a part: "(Very good sketch - 8 marks
# Fair sketch - 4 marks)", "(Very good description- 6 marks Fair description- 4
# marks)", or the bare ladder "(8,6,4,2 Marks)". It prices the answer in steps,
# and the fair price must be claimable (Alex): the row takes every printed
# value, with zero, and the band itself, lifted, as its note.
BAND_NOTE = re.compile(
    r'\(\s*very good\b[^()]*?\d{1,2}\s*marks?\b[^()]*?\bfair\b[^()]*?\d{1,2}\s*marks?\s*\)', re.I)
BAND_LADDER = re.compile(r'\(\s*(\d{1,2}(?:\s*,\s*\d{1,2}){2,})\s*marks?\s*\)', re.I)


def band_steps(text):
    """The marks a printed band permits, with zero, ascending; [] if none."""
    text = (text or '').strip()
    if BAND_NOTE.fullmatch(text):
        found = [int(n) for n in re.findall(r'(\d{1,2})\s*marks?\b', text, re.I)]
    elif BAND_LADDER.fullmatch(text):
        found = [int(n) for n in re.findall(r'\d{1,2}', text)]
    else:
        return []
    return sorted({0, *found}) if found else []



def _manifest():
    path = os.path.join(ROOT, 'components', 'MarkBank', 'figures.json')
    if not os.path.exists(path):
        return {}
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def figure_index():
    """The inspected crops, keyed by the part they were cut FOR.

    A crop is cut once for a (section, question, letter) and every roman under
    it shows the same picture, because the paper prints it once. Read from the
    manifest bind-figures.mjs wrote, so a crop that was never inspected is not
    in here to be bound.
    """
    figs = {}
    for key, rec in _manifest().items():
        parsed = TC.parse_key(key)
        if parsed and '-paper-' in key and not rec.get('solution'):
            figs[parsed] = key
    for alias, key in TC.FIGURE_SHARED.items():
        parsed = TC.parse_key(alias)
        if parsed and key in _manifest():
            figs[parsed] = key
    return figs


def solution_index():
    """The scheme's own drawn answers, keyed by the part each answers.

    Published by tech_figures.py --publish from tech_crops.SOLUTIONS, each
    marked solution: true, which the session screen holds back until the
    student has answered. Bound as the card's figureKey, so the reveal shows
    the examiner's drawing beside the rows -- or, where the scheme prints no
    words at all, beside the ask itself as the one row.
    """
    figs = {}
    for key, rec in _manifest().items():
        parsed = TC.parse_key(key)
        if parsed and '-scheme-' in key and rec.get('solution'):
            figs[parsed] = key
    for alias, key in TC.SOLUTION_SHARED.items():
        parsed = TC.parse_key(alias)
        if parsed and key in _manifest():
            figs[parsed] = key
    return figs


def stem_pieces(section, q, letter, roman, texts, stems, whole_letter=False):
    """The stimulus printed above a part, in the order the paper prints it.

    The question's own introduction, then the lettered part's head sentence
    ("The decorative wood-fired outdoor pizza oven shown, is made from cast
    iron."), then whatever the walker filed as that part's stem. The head
    sentence is the census's text for the letter itself, which is not a leaf
    where romans follow it and so never reached a card: 171 long-question
    cards opened mid-sentence ("in Co. Louth, consisting of...") for want of
    it.
    """
    pieces = []
    if letter:
        pieces.append(stems.get((section, q, None)) or '')
    # ...and the same head above a card that covers every roman of its
    # letter (2010-2014, priced only by letter): "The cruise ship Costa
    # Concordia ran aground..." is 2014 Ordinary 2(a)'s stimulus.
    if letter and (roman or whole_letter):
        pieces.append(texts.get((section, q, letter, None), ''))
    pieces.append(stems.get((section, q, letter)) or '')
    out = []
    for piece in pieces:
        piece = clean(piece)
        if piece and piece not in out:
            out.append(piece)
    return out


ASK_ROW_NOTE = ("The scheme answers this part with a drawing its text cannot "
                "carry; its own print is shown with the answer.")
# types/markBank.ts UNPRINTED_ANSWER: the one row a card may carry that is not
# a slice of the scheme, for a printed ask whose scheme prints no answer.
UNPRINTED_ANSWER = 'The scheme prints no answer for this part.'
# The note on a row the printed scheme leaves unfinished (tech_crops.SCHEME_BREAKS_OFF).
BREAKS_OFF_NOTE = 'The printed scheme breaks off here, mid-sentence.'
FALLBACK_TOPIC = 'tech-core-design'


def author(bind_figures=True):
    census = PC.census_subject(SUBJECT)
    # tech_figures.py calls this with the binding OFF, so that its worklist is
    # every part that points at printed matter -- not just the ones still
    # uncovered. A cropper whose candidate set shrinks as its own crops are
    # bound cannot reproduce what it published.
    figures = figure_index() if bind_figures else {}
    solutions = solution_index() if bind_figures else {}
    cards, refused, examples = [], collections.Counter(), collections.defaultdict(list)
    verdicts = []
    stats = []
    # Cards whose ask names no syllabus heading, filled from their question's
    # siblings once the sitting is read (every printed ask gets a card).
    unshelved = []
    shelved = collections.defaultdict(collections.Counter)

    for paper in census['papers']:
        year, level = paper['year'], paper['level']
        if not os.path.exists(os.path.join(
                ROOT, 'examiner-reports/technology/schemes', f'{year}-{level}.md')):
            # A sitting the census reads but whose scheme has not been
            # extracted yet is not carded at all: its asks stay OPEN in the
            # ledger, which is where an uncarded sitting belongs.
            continue
        # The full printed wording, not the census REPORT's copy of it: that
        # one is truncated to 160 characters for display, and a card built
        # from it ends a question mid-word. The keys are the same walk either
        # way, so the denominator is unchanged.
        keys, texts, _files = PC.census_sections(SUBJECT, year, level)
        leaves = {tuple(k): texts[k] for k in PC.leaves_of(keys)}
        assert set(leaves) == {tuple(l['key']) for l in paper['leaves']}, \
            f'{year} {level}: the authored leaf set is not the census leaf set'
        # census_subject has just walked this sitting, so its stimulus table is
        # the one belonging to these very leaves.
        stems = PC.SECTION_STEMS.get((SUBJECT, year, level), {})
        S = TechScheme(year, level)
        confirmed = cueless = contradicted = 0

        for block in S.priced():
            section, q, letter = block.section, block.q, block.letter
            # The lettering printed inside a drawing on this block's scheme
            # pages -- a solution crop's own labels, or a diagram the scheme
            # reprints beside its answer (tech_crops.py) -- comes off the
            # marking points it was welded to, by the printed row.
            for roman, lines, total, covered in block_units(block, leaves,
                                                            year, level):
                covered = [k for k in covered if k in leaves] or covered
                ask = clean_ask(joined_ask(covered, leaves))
                # tech_crops.ASK_FROM_STEM: a roman whose instruction is printed
                # after its data, below a picture, which the walker files as
                # the letter's stem (2017 Higher 4(b)(iii)'s "Calculate the
                # process capability index ... where: Cp = ...").
                stem_owner = TC.ASK_FROM_STEM.get((year, level, section, q, letter))
                letter_stem = clean(stems.get((section, q, letter)) or '')
                if stem_owner and stem_owner == roman:
                    ask = clean_ask(f'{ask} {letter_stem}')
                # tech_crops.STEM_TAIL_TO_ASK: an answer box's labels that ARE
                # the terms asked about ("Explain the terms: CAM: ____ CNC:
                # ____", 2017 Higher Q14(i)), filed by the walker at the end
                # of the question's stem. They join the one roman that asks
                # about them, and come off the stem every roman shows.
                tail_move = TC.STEM_TAIL_TO_ASK.get((year, level, section, q, letter))
                if tail_move and tail_move[0] == roman:
                    ask = clean_ask(f'{ask} {tail_move[1]}')
                ref = joined_ref(year, level, covered)

                def note(reason, ask_text=''):
                    verdicts.append({'year': year, 'level': level, 'ref': ref,
                                     'reason': reason})
                    refused[reason] += 1
                    if len(examples[reason]) < 80:
                        examples[reason].append(f'{ref}: {ask_text[:70]}')

                if not ask:
                    note('the paper prints no ask at this address')
                    continue

                # The SEC's own print of the picture the ask points at, and of
                # the answer the scheme draws. A question figure is cut once
                # per part and shared by the romans under it; a solution crop
                # belongs to the one unit it answers.
                figure = (figures.get((year, level, section, q, letter, roman))
                          or figures.get((year, level, section, q, letter, None)))
                solution = solutions.get((year, level, section, q, letter, roman))
                paper_labels = TC.paper_labels(year, level, figure) if figure else set()
                for key in TC.BY_EYE:
                    if TC.parse_key(key)[:5] == (year, level, section, q, letter):
                        paper_labels |= TC.paper_labels(year, level, key)
                paper_labels |= TC.ask_zone_words(year, level, section, q, letter, roman)
                # The lettering printed inside that picture, which the paper's
                # text layer welds onto the end of the ask: "...the circuit
                # shown. Calculation: 40 Ω 10 Ω 10 Ω V 12V". The crop carries
                # it; the question does not.
                # The ask as the paper's text layer gives it, lettering and all:
                # the scheme reprints the same picture, so a "point" that is
                # one of its labels ("1200 N") is found here and dropped.
                raw_ask = ask
                ask = TC.strip_labels(ask, paper_labels) or ask
                ask = TRAILING_LABEL.sub('', ask).strip()
                # The answer lines' own numbers, "1. ____ 2. ____", left after
                # the ask's last sentence once their rules are gone (2019
                # Ordinary Q3(ii), Q4(i), Q8, Q9).
                ask = re.sub(r'(?<=[.?!])(?<![Ff]ig\.)(?:\s+\d\.)+\s*$', '', ask)
                # ...and a run of them BETWEEN two asks of one unlettered
                # question, "...in cities. 1. 2. State two advantages..."
                # (2018 Ordinary Q2): a run of two or more, after a closed
                # sentence and before a capital, is the answer lines' numbers.
                ask = re.sub(r'(?<=[.?!])(?:\s+\d\.){2,}(?=\s+[A-Z(])', '', ask)
                # A tail the paper prints that no text layer reads in order:
                # tech_crops.ASK_TAILS, each looked at on its page.
                tail = TC.ASK_TAILS.get((year, level, section, q, letter, roman))
                if tail and ask.endswith(tail):
                    ask = ask[:-len(tail)].rstrip()
                # A picture's lone letter read after the ask's last sentence
                # ("...direction of arrow A. A"), whether or not its crop is
                # known: a question never ends in a capital on its own.
                ask = re.sub(r'(?<=[.?!])\s+[A-Z]\s*$', '', ask)
                # ...and a short tail of numbers, units or capitalised words
                # after the last sentence ("...for the display. 90 KG").
                ask = re.sub(r'(?<=[.?!])\s+(?:[A-Z0-9][^\s.?!,]*\s*){1,3}$', '', ask)
                # A roman that is a bare term under a lead-in that ends in a
                # colon -- "Explain the terms:" over "(i) cookie" -- carries the
                # lead-in, which is printed and is what the student is asked.
                if roman and len(ask.split()) <= 4 and not re.search(r'[.?!](?:\s|$)', ask):
                    lead_src = clean(stems.get((section, q, letter)) or stems.get((section, q, None)) or '')
                    lm = re.search(r'(?:^|[.?!]\s+)([A-Z][^.?!:]{3,60}:)\s*(?:\S+\s*){0,40}$', lead_src)
                    if lm:
                        ask = f'{lm.group(1)} {ask}'

                # tech_crops.ASK_STRIP: an answer box's own labels, set inside
                # the ask's text ("Value:", "Lowest: Highest:"), and a lead-in
                # the rule above misread, each measured on the page. Off the
                # raw ask too, which decides whether a row's label is the ask's.
                for pattern in TC.ASK_STRIP.get((year, level, section, q, letter, roman), ()):
                    ask = re.sub(pattern, '', ask).strip()
                    raw_ask = re.sub(pattern, '', raw_ask).strip()

                del BACKED_OFF[:]
                # A card covering every roman of its letter (2010-2014, priced
                # only by letter) is cued by the letter's head sentence too:
                # the scheme reprints it first ("Graphics A, B and C show
                # various power accessories.", 2013 Ordinary 2(a)), and read
                # against the romans alone that reprint scored as a mismatch.
                # Only where the romans alone do not cue it: read with the head
                # first, 2013 Higher 4(b)'s reprinted head walked on into its
                # first answer line.
                whole_letter = roman is None and len([k for k in covered if k[3]]) > 1
                letter_head = clean(texts.get((section, q, letter, None), '')) if whole_letter else ''
                cue, points = split_cue([clean(l) for l in lines], ask)
                score = cue_score(cue, ask)
                if letter_head and score < CUE_FLOOR \
                        and len(re.findall(r"[a-z']{3,}", cue.lower())) >= MIN_CUE_WORDS:
                    del BACKED_OFF[:]
                    cue_ask = f'{letter_head} {ask}'
                    cue, points = split_cue([clean(l) for l in lines], cue_ask)
                    score = cue_score(cue, cue_ask)
                backed_off = clean(BACKED_OFF[0]) if BACKED_OFF else None
                cue_words = len(re.findall(r"[a-z']{3,}", cue.lower()))
                if cue_words < MIN_CUE_WORDS:
                    # The part's own cue can be a single word -- 2021 Higher
                    # Q3 marks "'patched'" and "Anti-virus" -- but the BLOCK
                    # reprints the stimulus above them, and the paper prints
                    # the same stimulus as this question's stem. That is a
                    # second document agreeing on which question this is,
                    # which is what Law 4 asks for.
                    head = ' '.join(clean(t) for t in block.head_lines())
                    stem_text = (stems.get((section, q, letter))
                                 or stems.get((section, q, None)) or '')
                    if cue_score(head, stem_text) >= CUE_FLOOR \
                            and len(re.findall(r"[a-z']{3,}", head.lower())) \
                            >= MIN_CUE_WORDS:
                        cue, cue_words = head, MIN_CUE_WORDS
                        score = cue_score(head, stem_text)
                if cue_words >= MIN_CUE_WORDS:
                    if score >= CUE_FLOOR:
                        confirmed += 1
                    else:
                        contradicted += 1
                        note('the scheme cue does not match the paper ask here',
                             ask)
                        continue
                else:
                    cueless += 1
                    if not block.numbered and section == 'A':
                        # Position-numbered AND wordless: nothing but order
                        # supports the pairing, which Law 4 does not accept.
                        note('block number and pairing both rest on order alone',
                             ask)
                        continue

                question = clean(ask)

                def points_at_print(text):
                    return bool(cardlint.FIG_REF.search(text)
                                and not cardlint.SELF_WORK.search(text)
                                and not cardlint.INLINE_TABLE.search(text))

                # The picture first, before the answer is read: a part that
                # points at printed matter the card cannot carry is refused
                # here whatever its scheme says, so tech_figures.py's worklist
                # names every one of them.
                pieces = []
                lost_picture = not figure and points_at_print(question)
                # tech_crops.STEM_JOIN: a sentence's last words that the census
                # read as the letter's head because they open a line with a
                # part reference ("2(a) above."); they go back on the stem
                # sentence they end.
                rejoin = TC.STEM_JOIN.get((year, level, section, q, letter))
                for piece in stem_pieces(section, q, letter, roman, texts, stems, whole_letter):
                    if stem_owner and piece == letter_stem:
                        continue
                    if rejoin and piece.endswith(' ' + rejoin):
                        piece = piece[:-len(rejoin)].rstrip()
                    # The answerbook's ruled blanks and their fill-in labels
                    # ("Time: ____ People: ____"), which 2021 Ordinary Q6 prints
                    # between its stem and its romans.
                    piece = clean(BLANK_RULE.sub(' ', piece))
                    for pattern in TC.ASK_STRIP.get((year, level, section, q, letter, roman), ()):
                        piece = re.sub(pattern, '', piece).strip()
                    if tail_move and piece.endswith(tail_move[1]):
                        piece = piece[:-len(tail_move[1])].rstrip()
                    piece = re.sub(r'(?:\s*\b[A-Z][a-z]{1,12}:\s*)+$', '', piece).strip()
                    # The paper's "OR" between two optional parts closes the
                    # piece AFTER a picture's lettering (2016 Ordinary 4(c):
                    # "...Low Price High Price Low Quality OR"), and a trailing
                    # word that is not lettering stops the strip; it comes off first.
                    piece = re.sub(r'\s+OR\s*$', '', piece)
                    piece = TC.strip_labels(piece, paper_labels)
                    piece = TRAILING_LABEL.sub('', piece).strip()
                    piece = re.sub(r'\s+OR\s*$', '', piece)
                    if rejoin and piece and not re.search(r'[.?!:]$', piece):
                        piece = f'{piece} {rejoin}'
                    # The answer lines' numbers, as the ask loses them above.
                    piece = re.sub(r'(?<=[.?!])(?:\s+\d\.){2,}(?=\s+[A-Z])', '', piece)
                    piece = re.sub(r'(?<=[.?!])(?<![Ff]ig\.)(?:\s+\d\.)+\s*$', '', piece)
                    # A neighbouring figure's lone letter ("...in electronics. A")
                    # and a table the walker flattened ("Week 1 Week 2 ... Task D").
                    piece = re.sub(r'(?<=[.?!])\s+[A-Z]\s*$', '', piece)
                    # A caption that followed the stem's last sentence on the
                    # page ("...Technology workshops. Cylinder sail"): a run of
                    # up to four words that closes nothing.
                    piece = re.sub(r'(?<=[.?!])\s+(?:[A-Z]\S*\s+)(?:\S+\s+){0,2}\S*[^.?!:\s]\s*$', '', piece)
                    if not keeps_stem(piece, question) or CAPTION.match(piece) \
                            or flattened_table(piece):
                        continue
                    if not figure and points_at_print(piece):
                        if LEANS_ON_STEM.search(question):
                            lost_picture = True
                        # This PIECE of the stimulus points at a picture and
                        # the ask does not. "A 4K UHD interactive touch screen
                        # ... is shown" above "Explain the term UHD." -- the ask
                        # stands perfectly well on its own, and the sentence is
                        # context this card cannot show. The piece goes, not
                        # the card and not the rest of the stem: the cost data
                        # printed under "the Slant 3D headphone stand, shown
                        # here" is what 2022 Higher 4(b)(ii) is worked from.
                        continue
                    pieces.append(piece)
                if lost_picture:
                    note('points at printed matter the card cannot carry', question)
                    continue
                show_stem = ' '.join(pieces)
                lead = re.match(r'([^.?!]{4,60}:)\s', question or '')
                if lead and show_stem.rstrip().endswith(lead.group(1)):
                    # "Explain the terms:" printed once above the parts arrives
                    # at the end of the stem AND the head of each ask (2020
                    # Higher 12); the stem gives it up.
                    show_stem = show_stem.rstrip()[:-len(lead.group(1))].rstrip()
                if not total:
                    note('the scheme prints no tariff for this part', question)
                    continue

                raw = [TC.strip_scheme_line(clean(l), year, level, block.pages,
                                            keep_numbers=bool(CALCULATION.search(l)))
                       for l in points]
                points = cardable([t for t in raw if t], S.normalised)
                # A "point" that repeats the ask is the scheme naming the part
                # rather than answering it: 2021 Higher Q3 marks the term
                # "'patched'" and heads its answer with the term again, which
                # shipped as a row telling the student the question.
                # The paper's multiplication sign and the scheme's letter x are
                # one character for the reprint test ("1280 \u00d7 800" / "1280 x
                # 800", 2013 Higher 3(c)(ii)).
                bare = SCHEME_NORM(f'{raw_ask} {question_label(covered)}'.replace('\u00d7', 'x'))
                # The scheme reprints the stimulus too -- 2022 Higher Q9, Q13
                # and Q14 open their blocks with the paper's own sentence --
                # and a line that sits inside it is no answer either.
                bare_stem = SCHEME_NORM(' '.join(pieces))
                # ...and a whole SENTENCE of the stimulus at any length, closed
                # as the paper closes it: "Silicon is a semiconductor." (2014
                # Ordinary 2(a)), its stem's last sentence, set above (i).
                stem_sentences = {SCHEME_NORM(t) for t in
                                  re.split(r'(?<=[.?!])\s+', ' '.join(pieces)) if t}
                points = [p for p in points
                          if not (len(SCHEME_WORDS(p)) >= 5 and SCHEME_NORM(p) in bare_stem)
                          and not (p.rstrip().endswith(('.', '?', '!'))
                                   and len(p.split()) >= 3
                                   and SCHEME_NORM(p) in stem_sentences)
                          # The stimulus's given data reprinted whole, "Assume
                          # g = 9.81 m/s2" over 2019 Higher 11(i)'s working: a
                          # line that opens "Assume" gives, it does not answer.
                          and not (re.match(r'assume\b', p, re.I)
                                   and SCHEME_NORM(p) in SCHEME_NORM(f'{bare_stem} {raw_ask}'))]
                # At any length: 2022 Ordinary 2(b)(iii) reprints its ask in
                # 68 characters above the two-word answer "Suitable circuit.",
                # and a length exemption kept the reprint and lost the answer.
                # A numbered answer list ("1. 100 kilobyte", "2. 1 gigabyte",
                # "3. 1 terabyte.") is the scheme's ORDER of the ask's own
                # items (2016 Higher 12(i)), not a reprint of them.
                numbered_list = [p for p in points if re.match(r'\d\.\s', p)]
                numbered_list = numbered_list if (
                    len(numbered_list) >= 2 and re.match(r'1\.\s', numbered_list[0])) else []
                # Where each roman starts: a whole-block card's ask joins them
                # as "(i) Name ... (ii) Give ...", and a reprint of (ii)
                # opens as (ii) does, not as the ask's first word.
                ask_starts = {t[0] for t in (_tokens(seg) for seg in
                              re.split(r'\((?:i{1,3}|iv|v)\)', ask)) if t}
                unit_key = (year, level, section, q, letter, roman)
                kept = [p for p in points
                        if p in numbered_list
                        # A scheme heading that happens to reuse the ask's words
                        # and is a marking point, named on the scheme page
                        # (tech_crops.KEEP_LINES): 2013 Higher Q15's "Pictorial
                        # View" over "Two suitable graphic techniques".
                        or p in TC.KEEP_LINES.get(unit_key, ())
                        or (SCHEME_NORM(p.replace('\u00d7', 'x')) not in bare
                            # ...nor with an article dropped: 2015 Ordinary
                            # Q11 reprints "Explain what is meant by terms AC
                            # and DC." for the paper's "by the terms". Only a
                            # line that opens as one of the ask's romans does.
                            and not (_tokens(p)[:1] and _tokens(p)[0] in ask_starts
                                     and len(SCHEME_WORDS(p)) >= 4
                                     and SCHEME_NORM(ARTICLE.sub(' ', p))
                                     in SCHEME_NORM(ARTICLE.sub(' ', f'{raw_ask} {question_label(covered)}')))
                            # A reprint that paraphrases by a word -- "Find a
                            # value of R2" for the paper's "Find the value of
                            # R2" -- is still the question, not an answer.
                            # Measured in WORDS, not tokens: a worked line
                            # ("Mean: 2+3+...+4 = 48 = 4") has one word, which
                            # the ask also has, and scored as a reprint.
                            # ...and opening as the ask opens: "Batch production
                            # is most appropriate for this order" reuses every
                            # word of its ask and is the answer.
                            and not (len(SCHEME_WORDS(p)) >= 6
                                     and cue_score(p, ask) >= 0.85
                                     and _tokens(p)[:1]
                                     and _tokens(p)[0] in ask_starts)
                            # ...and the stimulus reprinted by a word -- "the
                            # frame structures of buildings" for the paper's
                            # "structure" (2016 Ordinary Q11).
                            and not (len(SCHEME_WORDS(p)) >= 6 and pieces
                                     and cue_score(p, ' '.join(pieces)) >= 0.85
                                     and _tokens(p)[:1] == _tokens(' '.join(pieces))[:1])
                            # ...and a lead-in that ends in a colon needs
                            # only most of its words in the ask: "Describe,
                            # with specific examples, each of the following
                            # potential sources of waste in business or in
                            # manufacturing:" is the scheme's own wording of
                            # the paper's "with reference to a specific example".
                            and not (p.rstrip().endswith(':')
                                     and len(SCHEME_WORDS(p)) >= 8
                                     and (cue_score(p, ask) >= 0.6
                                          # ...or in the stem, where the paper
                                          # set the lead-in above its romans:
                                          # 2016 Higher Q3's "Analyse ... using
                                          # the following headings:" for the
                                          # paper's "under the following".
                                          or cue_score(p, ' '.join(pieces)) >= 0.8)))
                        or p == backed_off]
                # A priced block answers: where every line reads as a reprint,
                # the last is the answer in the ask's own words. 2022 Ordinary
                # 2(b)(iii) asks for "a suitable circuit" and the scheme credits
                # "Suitable circuit." -- two words the ask contains. Unless the
                # last line merely finishes the line before it: 2026 Higher
                # 2(b)(ii)'s reprint wraps after "voltage", and "comparator."
                # is the end of the question, not a row.
                if not kept and len(points) >= 2 \
                        and SCHEME_NORM(f'{points[-2]} {points[-1]}') in bare:
                    points = []
                else:
                    points = kept or points[-1:]
                if len(points) > 1:
                    points = [p for p in points if not ACCEPTED_NOTE.match(p)]
                if backed_off and backed_off in points and cue \
                        and SCHEME_NORM(f'{cue} {backed_off}') in bare:
                    # The cue and the back-off line together are the ask: the
                    # reprint wrapped, and its last line is no answer whether
                    # or not a drawing is bound.
                    points = []
                if backed_off and solution and backed_off in points:
                    # The reprint consumed every line and the scheme's answer
                    # is its DRAWING (the crop is bound): the back-off line is
                    # the end of the question, not a row. 2023 Ordinary
                    # 1(b)(i)'s block is the paper's own bullets above a
                    # flowchart, and "rotating and the light bulb turns off."
                    # shipped as its 8-mark answer.
                    points = []
                points = [strip_ask_label(p, raw_ask) for p in points]
                # A quality band printed UNDER the answer, inside a part the
                # block's tariff prices (2015 Ordinary 5(c)(ii): "(Very good
                # description- 6 marks Fair description- 4 marks)" over the
                # steps of rotational moulding): not a row, and not dropped.
                # The answer is one criterion row on the band's steps, with
                # the band as its note.
                band_note, band_marks = None, []
                bands = [p for p in points if BAND_NOTE.fullmatch(p.strip())]
                if len(bands) == 1 and len(points) > 1:
                    found = band_steps(bands[0])
                    if found and found[-1] == total:
                        band_note, band_marks = bands[0].strip(), found
                        points = [p for p in points if p is not bands[0]]
                unprinted_note = TC.UNPRINTED.get((year, level, section, q, letter, roman))
                ask_row = bool(solution and solution in TC.ASK_ONLY) or bool(unprinted_note)
                if not ask_row and (not points or (
                        graphic_fragments(points)
                        and (year, level, section, q, letter, roman) not in TC.LISTED_STEPS)):
                    # The answer is a DRAWING: the text layer holds nothing,
                    # or the words read off a flowchart's boxes and a truth
                    # table's rows, not one of which states anything. Where
                    # the scheme's own print of that drawing has been cut and
                    # looked at (tech_crops.SOLUTIONS), the card shows it at
                    # the reveal, with the ask as its one row -- Chemistry's
                    # rule for its dot-and-cross diagrams. Otherwise the part
                    # is refused, and the refusal is the cropper's worklist.
                    if solution or (year, level, section, q, letter, roman) in TC.NO_DRAWING:
                        ask_row = True
                    elif not points:
                        note('the scheme states no marking point for this part', ask)
                        continue
                    else:
                        note('the scheme answers this part with a drawing the '
                             'text layer reads as fragments', ask)
                        continue

                marks = None
                if roman is None and block.terms \
                        and len(block.terms) == len(points) \
                        and sum(block.terms) == total:
                    marks = block.terms

                stem_text = stems.get((section, q, letter)) or stems.get((section, q, None)) or ''
                topic = (topic_for_option(q) if section == 'C'
                         else topic_for(question, stem_text,
                                        ' '.join(block.head_lines())))

                joined = f'{show_stem} {question}'
                label_key = []
                if cardlint.NAMES_LETTERS.search(joined) \
                        and not cardlint.INVITES_DRAWING.search(joined):
                    # A question naming labelled points needs those letters
                    # DECODED as well as shown, and the build drops a card that
                    # shows them without a label key. tech_crops.LABEL_KEYS
                    # holds the scheme's own words for each letter; a part
                    # with a picture and a key is carded, the rest refused.
                    decoded = TC.LABEL_KEYS.get((year, level, section, q, letter))
                    if figure and decoded:
                        label_key = [{'letter': d['letter'], 'meaning': d['meaning'],
                                      'askedInThisQuestion': True} for d in decoded]
                    else:
                        note('names a lettered part this author cannot decode', question)
                        continue
                if cardlint.SCHEME_LEAK.search(joined):
                    note('the paper text carries scheme metadata', question)
                    continue
                if len(question) < 16 and len(show_stem) < 20:
                    note('the ask is too short to stand on its own', question)
                    continue
                if CUT_SHORT.search(question) and not re.search(r'\b[A-Z]\w*\s+[A-Z]$', question):
                    # (A capital letter closing a name -- "Component A", 2017
                    # Higher Q3(i) -- is a label, not the article "a".)
                    # The paper text stops mid-phrase -- "A PIC, like the one
                    # mentioned in" -- which is the reader losing the rest of
                    # the sentence, not a question. paper.suspect() flags the
                    # same shape and the authoring layer refuses to card a
                    # flagged part; this is that rule, for the sections walker.
                    note('the paper text for this part is cut short', question)
                    continue

                if ask_row and not solution:
                    # tech_crops.NO_DRAWING: a sketch whose scheme prints no
                    # drawing, only the band it is marked on (2018 Ordinary
                    # Q7's empty answer box). Every printed ask gets a card;
                    # this one says the scheme prints no answer.
                    trimmed = 0
                    rows = [{'id': 'r-1', 'kind': 'criterion',
                             'verbatim': UNPRINTED_ANSWER, 'marks': total,
                             'contextNote': (unprinted_note
                                             or ('The scheme prints no drawing for this '
                                                 'part, only how the sketch is marked: '
                                                 f'{block.notation}')),
                             'unprinted': True}]
                    model = {'kind': 'fixed'}
                elif ask_row:
                    trimmed = 0
                    rows = [{'id': 'r-1', 'kind': 'point', 'verbatim': question,
                             'marks': total, 'openList': True,
                             'contextNote': ASK_ROW_NOTE, 'ask': True}]
                    model = {'kind': 'fixed'}
                elif band_note:
                    trimmed = 0
                    rows = [{'id': 'r-1', 'kind': 'criterion', 'verbatim': ' '.join(points),
                             'marks': total, 'permittedMarks': band_marks,
                             'contextNote': band_note}]
                    model = {'kind': 'fixed'}
                else:
                    trimmed = len(points) - min(len(points), CAP[section])
                    # A card covering several printed asks, priced only as a
                    # whole (2014 Higher 2(d): a drawn (i) and a worded (ii)
                    # at "(c) OR (d) - 14 marks"), never hands its total to a
                    # lone surviving row: that row answers one of the asks.
                    # ...nor does a lone row take a total split by a bare
                    # "(4+ 2)" (2011 Higher Q8: the WBS drawn, the method
                    # worded): the split says the row is one of two. (Bare
                    # splits only: the "(4+4 marks)" years were measured and
                    # carded the other way, and they stay as shipped.)
                    bare_split = bool(re.fullmatch(r'\(\s*\d{1,2}(?:\s*\+\s*\d{1,2})+\s*\)',
                                                   (block.notation or '').strip()))
                    rows, model = rows_for(points, marks, total, CAP[section],
                                           single_ask=len(covered) == 1
                                           and not (roman is None and bare_split
                                                    and len(block.terms) > 1))
                    shown = sum(r['marks'] or 0 for r in rows)
                    if model['kind'] == 'fixed' and shown != total:
                        note('the rows do not sum to the printed tariff', question)
                        continue
                steps = band_steps(block.notation)
                if steps and len(rows) == 1 and steps[-1] == total == rows[0]['marks'] \
                        and (rows[0].get('ask') or rows[0].get('unprinted')):
                    # A drawing priced by its quality band ("(Very good sketch -
                    # 8 marks Fair sketch - 4 marks)"): the one row is a
                    # criterion on the band's steps, so a fair sketch's 4 can
                    # be claimed. An unprinted row already quotes the band.
                    rows[0]['kind'] = 'criterion'
                    rows[0]['permittedMarks'] = steps
                    rows[0].pop('openList', None)
                    if rows[0].get('ask'):
                        rows[0]['contextNote'] = f'{block.notation.strip()} {ASK_ROW_NOTE}'
                cut = TC.SCHEME_BREAKS_OFF.get((year, level, section, q, letter, roman))
                if cut:
                    # The printed scheme stops mid-sentence: the row is lifted
                    # up to the break and says so, rather than finishing it.
                    hit = [r for r in rows if r['verbatim'].endswith(cut)]
                    if len(hit) != 1:
                        note('the scheme answer named as breaking off was not found', question)
                        continue
                    hit[0]['contextNote'] = BREAKS_OFF_NOTE
                if model['kind'] == 'questionTotal' and roman is None and block.terms \
                        and len([k for k in covered if k[3]]) > 1 and rows:
                    # A card for several printed asks whose scheme prints one
                    # split for them all ("(2+2+4 marks)" over two romans):
                    # the split is the scheme's, but which mark is for which
                    # part is not, so the card is assessed as a whole. The
                    # student sees why on the first row, since card-level
                    # notes never ship (build-deck strips them).
                    split = (f'The scheme prints {block.notation.strip()} for these '
                             'parts together and does not say which part each mark '
                             'is for, so they are assessed as a whole.')
                    rows[0]['contextNote'] = ' '.join(
                        t for t in (split, rows[0].get('contextNote')) if t)
                model = dict(model, notation=block.notation)

                note_text = (f'The scheme prints {block.notation!r} for '
                             f'{"this part" if roman else "this question"}.')
                if trimmed:
                    # Disclosed trimming, the skill's own remedy for a menu
                    # over the display cap: the student is told the list goes
                    # on rather than shown a list that quietly stops.
                    note_text += (f' The scheme lists {len(points)} accepted '
                                  f'answers; the first {len(rows)} are shown.')

                topic = TOPIC_OVERRIDES.get(card_id(year, level, section, q, letter, roman), topic)
                card = {
                    'id': card_id(year, level, section, q, letter, roman),
                    'topicId': topic,
                    'conceptId': (topic or '').replace('tech-', ''),
                    'level': LEVEL_WORD[level],
                    'year': year,
                    'subjectId': SUBJECT,
                    'section': section,
                    'questionRef': ref,
                    'questionText': question,
                    'stem': show_stem,
                    # The scheme's own drawn answer, held back until the reveal.
                    'figureKey': solution or '',
                    # The SEC's own print of the picture the ask points at,
                    # shown BEFORE the reveal. A question figure may be shared
                    # by the siblings under one part, which is right here: the
                    # paper prints the picture once for the whole question.
                    'questionFigureKey': figure or '',
                    # A Technology question figure is the PICTURE the ask names
                    # (a circuit, a lamp, a gate), never the printed ask itself:
                    # the session screen must keep the stem and the ask text
                    # visible beside it (SessionScreen printedQuestionReplacesText
                    # hides both unless includesPrompt is false).
                    **({'questionFigureIncludesPrompt': False} if figure else {}),
                    'labelKey': label_key,
                    'tariffModel': model,
                    'totalMarks': total,
                    'rows': rows,
                    'notes': note_text,
                }
                cards.append(card)
                shelf = (year, level, section, q)
                if topic:
                    shelved[shelf][topic] += 1
                else:
                    unshelved.append((card, shelf))

        stats.append((year, level, confirmed, cueless, contradicted))

    # An ask whose own words name no syllabus heading -- "Suggest two
    # industries that might use standards developed by the NSAI." -- sits on
    # the shelf its question's other parts sit on, since the paper sets each
    # long question in one context; failing that, under design, the area the
    # syllabus names first. A shelf is a place to find the card, not a claim
    # about what it says, and a card without one is a printed ask without a
    # card.
    for card, shelf in unshelved:
        topic = (shelved[shelf].most_common(1)[0][0] if shelved[shelf]
                 else FALLBACK_TOPIC)
        card['topicId'] = topic
        card['conceptId'] = topic.replace('tech-', '')

    return cards, refused, examples, verdicts, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--verdicts')
    args = ap.parse_args()

    cards, refused, examples, verdicts, stats = author()

    if args.verdicts:
        with open(args.verdicts, 'w', encoding='utf-8') as fh:
            json.dump(verdicts, fh, indent=1)
        print(f'wrote {args.verdicts}: {len(verdicts)} refusals')
    if args.report:
        census = PC.census_subject(SUBJECT)
        total = sum(p['leafCount'] for p in census['papers'])
        print(f'{len(cards)} card(s) against {total} census asks')
        print()
        print('PAIRING (Law 4): how each sitting\'s scheme parts were joined')
        for year, level, ok, cueless, bad in stats:
            n = ok + cueless + bad
            print(f'  {year} {level.upper()}: {ok:3} confirmed by wording, '
                  f'{cueless:3} address only (scheme prints no cue), '
                  f'{bad:3} refused for contradicting the address'
                  f'   [{100 * ok // max(n, 1)}% confirmed]')
        print()
        for reason, n in refused.most_common():
            print(f'  {n:4} REFUSED  {reason}')
            for e in examples[reason][:60 if args.all else 3]:
                print(f'            {e}')
        return 0
    print(json.dumps(cards, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
