#!/usr/bin/env python3
"""Exam question papers, any subject — the printed wording, lifted.

Nothing in this module composes question text. Every string it returns is a
slice of examiner-reports/<subject>/papers/<year>-<level>[-<component>]-paper.pdf
as pymupdf reads it, with page furniture removed and whitespace collapsed.

That distinction is the reason the module exists. The marking scheme prints a
compressed cue for the examiner — "Identify the following plants" — while the
paper prints what the candidate actually read: "Identify each of the following
plants." Only the second belongs on a card, and only the paper has it.

    P = Paper('agricultural-science', 2021, 'hl')
    P.text(1, 'a')          -> 'Identify each of the following plants.'
    P.text(2, 'b', 'iii')   -> 'Identify one way the student could improve ...'
    P.stem(13, 'a')         -> the stimulus prose printed above the parts

Why blocks and not lines
------------------------
Reading the pages as lines drags a neighbouring column into the question: on
2021 HL Q6 the tick-box options 'Ribosome / Mitochondria / Chloroplast' land
inside part (iii), and on Q15(b)(ii) an entire graph axis does. pymupdf's block
segmentation keeps a part marker and its own text together in one block and
leaves the option list, the table and the ruled answer boxes as separate blocks,
so walking blocks rather than lines removes that whole class of contamination.

A part occasionally runs across two blocks, which shows up as text that stops
without terminal punctuation. Continuation handles exactly that case and stops
as soon as the sentence closes, so it cannot swallow a table.
"""
import os
import re

import pymupdf

# The SEC typesets "configuration" with a single ﬁ glyph and "ti" with Ɵ, and a
# card must not carry them. The table is read out of schemeText.mjs rather than
# restated, so it cannot drift from the fold the rest of the pipeline applies.
def _ligatures():
    js = os.path.join(ROOT_DIR, 'scripts', 'markbank', 'schemeText.mjs')
    with open(js, encoding='utf-8') as fh:
        for line in fh:
            if 'LIGATURES = {' in line:
                body = line.split('{', 1)[1].rsplit('}', 1)[0]
                return {k.strip().strip("'"): v.strip().strip("'")
                        for k, v in (pair.split(':', 1)
                                     for pair in body.split(',') if ':' in pair)}
    return {}


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
LIGATURES = _ligatures()
LIG_RE = re.compile('[' + ''.join(re.escape(c) for c in LIGATURES) + ']') if LIGATURES else None


def unligature(text):
    if not text or LIG_RE is None:
        return text
    return LIG_RE.sub(lambda m: LIGATURES[m.group(0)], text)

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
def papers_dir(subject):
    return os.path.join(ROOT, 'examiner-reports', subject, 'papers')

# Subjects head their questions differently and both forms have to be read:
# Agricultural Science and Economics print "Question 4", Chemistry and Physics
# print "4." straight into the text. The bare form is anchored on a following
# capital or bracket so it cannot match a numbered answer line or a figure.
# A section rubric and the first question head can be set in one block, and the
# head is then invisible because QHEAD anchors at the start. Chemistry 2021 HL
# lost Questions 1 and 4 that way, Physics 2021 HL lost 1 and 6, Business and
# Home Economics lost Question 1 — whole questions, not parts. The head is only
# taken when a full stop ends the rubric immediately before it, so that a rubric
# reading "one question from questions 2, 3, 4 and 5." does not hand back a 5.
# A question head can also sit part-way down a block, behind the tail of the
# question before it: on page 8 of 2021 Higher Level Chemistry, "7. (a) Define
# an acid" runs on from the end of Question 6(d) inside one block, and splitting
# on part markers alone stranded the "7." at the end of Question 6. The head must
# follow a closed sentence AND introduce a part, which is what separates it from
# a figure caption or a numbered line; the caller then requires the number to be
# one the paper is actually due.
# Either spelling of a question head. Maths writes "Question 1" where the
# science papers write "1.", and the rubric sentence above it is set in the
# same block -- "Answer any four questions from this section. Question 1" --
# so a head only recognised at the start of a block was invisible. Every
# Q1 in the Maths corpus was lost that way, and with it its parts.
QHEAD_AHEAD = r'(?=\d{1,2}\.\s+[A-Z(]|Question\s+\d{1,2}\b)'
INLINE_QHEAD = re.compile(r'(?<=[.)?:])\s+' + QHEAD_AHEAD)

RUBRIC_HEAD = re.compile(
    r'^(?:(?:SECTION|Section)\s+[A-D]\b'
    # 'Answer five questions', 'Answer any four questions', and Economics'
    # 'Answer 5 out of 6 questions.' — the last was unmatched, so the head
    # welded behind it was invisible and six sittings lost Q11 onward.
    r'|Answer\s+(?:any\s+)?[\w\-]+(?:\s+out\s+of\s+[\w\-]+)?\s+questions?\b)'
    # The full stop is optional: Economics prints 'Answer 3 out of 6
    # questions Question 11' with no punctuation at all, and demanding the
    # stop left six sittings' Question 11 welded invisible. Minimal
    # matching stops at the FIRST head-shaped token, and the lookahead
    # still refuses the bare '5' of 'questions 2, 3, 4 and 5.'
    r'.*?\.?\s+' + QHEAD_AHEAD, re.S)

# The '\d.' head may be followed by an opening quote: Construction Studies'
# 2019-2025 alternative Q10 opens with a quotation.
QHEAD = re.compile('^(?:Question\\s+(\\d{1,2})\\b|(\\d{1,2})\\.\\s+(?=[A-Z(\\d"\u201c\u2018]))')
MARKER = re.compile(r'^\(([a-z]{1,4})\)\s*')
# Letters run past (h): Chemistry's Q4 runs to (l) and Physics' lettered-choice
# questions to (l) as well — every part after (h) was invisible and 61 shipped
# cards orphaned against a census that had never seen their asks. 'i' is NOT in
# the letter class: alone it is a roman first, and only the (h)-context rule in
# Paper.__init__ may upgrade it. Romans run past (viii): Biology prints (ix),
# Physics (ix)-(xii), and the old alternation topped out at viii so '(ix)'
# could never split a block or key a part.
LETTER = re.compile(r'[a-hj-l]')
ROMAN = re.compile(r'i{1,3}|iv|vi{0,3}|ix|xi{0,3}')
RUBRIC = re.compile(r'^Answer (either|any|all)\b')
# A part marker orphaned at the very end of a block: pymupdf glues a marker
# whose content follows on the next line to the TAIL of the previous block —
# "...gene and allele. (ii)" — and the marker then vanishes, its children
# glued to the sibling before it. Seven Biology flags and two silent losses.
# Guarded by the punctuation before it, so "...shown in part (iii)" mid-prose
# is never stripped.
TRAILING_MARKER = re.compile(
    r'[.?!:]\s+(\((?:[a-hj-l]|i{1,3}|iv|vi{0,3}|ix|xi{0,3})\))\s*$')
# A cross-reference that lands at a block start — "(b) (iii) above." — reads
# as a real letter+roman marker and re-files the tail of the current ask into
# an earlier leaf. 25 instances across eight Biology papers.
CROSSREF = re.compile(
    r'^\([a-hj-l]\)\s*\([ivx]{1,4}\)\s*(?:\d\.\s*)?(?:above\b|,)')
# Misprints in the SEC's own papers, applied by (subject, year, level). No
# numbering heuristic can catch these: 2023 HL Biology prints a bold "16."
# where "(b)" belongs inside Question 15, which filed Q15(b) under a fake Q16
# and merged the real Q16 into it.
MISPRINTS = {
    ('biology', 2023, 'hl'): [
        ('16. (i) Draw a large diagram', lambda t: '(b) ' + t[4:]),
    ],
}
# Chemistry prints 'Leaving Certificate Examination, 2021' (comma), Physics
# 'Leaving Certificate, 2021' — the strict form let footers leak into leaf
# text.
PAGE_FURNITURE = re.compile(
    r'^(?:Leaving Certificate(?:\s+Examination)?[,\s]+\d{4}'
    r'|There is no examination material on this page'
    r'|Do not hand this up)')
# Answer-booklet scaffolding: a numbered answer line, or a short fill-in label
# ending in a colon ('Named crop:', 'Symptoms:'). Verified across all ten
# papers: 294 such lines occur and not one is the opening line of a part.
FURNITURE = re.compile(r'^(\d{1,2}\.|[^.?!]{1,34}:)$')
TERMINAL = re.compile(r'[.?!]$')
# Biology, Chemistry and Physics set several parts inside one block, so a marker
# turns up mid-text: "(ii) How did the student make the temperature 0 °C?".
# Anchored on a following capital or bracket, which keeps "(15)" and "(a)" of a
# chemical name out of it.
# The lookahead accepts what a part can actually open with: a capital, a
# bracket, a digit ('(vi) 90 g of...'), a quote, or a mathematical-alphanumeric
# glyph — Chemistry 2022 OL Q10(a) opens '(vi) 𝐇...' and the [A-Z(] class lost
# the part.
INLINE_MARKER = re.compile(
    r'\s(?=\((?:[a-hj-l]|i{1,3}|iv|vi{0,3}|ix|xi{0,3})\)'
    '\s+[A-Z(0-9"\u201c\u2018\'\u0391-\u03a9\U0001d400-\U0001d7ff])')
# A block holding nothing but figure labels ('A B C', 'A: B: C:'). It captions
# the artwork, so it belongs to the figure, not to the question's prose.
LABELS_ONLY = re.compile(r'^[A-H]\s*:?(\s+[A-H]\s*:?)*$')


def _blocks(path):
    """Every non-empty text block, in page then top-to-bottom, left-to-right order."""
    with pymupdf.open(path) as doc:
        pages = [sorted(doc[n].get_text('blocks'), key=lambda b: (round(b[1], 1), b[0]))
                 for n in range(doc.page_count)]
    for page in pages:
        for b in page:
            text = ' '.join(b[4].split())
            if text and not PAGE_FURNITURE.match(text):
                yield text


def _i_is_letter(blocks, index):
    """Is a lone "(i)" after "(h)" the ninth letter or the first roman?

    Decided by what follows: a "(j)" ahead of any "(ii)" means the letter run
    continues. Chemistry 2024 HL Q4 runs (a)-(l); Biology prints (h)(i)(ii)
    roman runs. Neither side can be a default without breaking the other.
    """
    for text in blocks[index + 1:index + 10]:
        t = text.strip()
        if re.match(r'^\(ii\)', t):
            return False
        if re.match(r'^\(j\)', t):
            return True
    return False


def _opens_a_question(blocks, index, open_letter=None):
    """Does a bare number here start a question, or label a graph?

    A question's first part is (a), or (i), or prose. So if the next part
    marker after this number is (d), the number is not a head and we are still
    inside the question that number belongs to. The graph in 2022 HL Paper 1
    Q7 labels its x-axis up to 8, and that "8" was read as Question 8 -- taking
    parts (d) to (g) of Question 7 with it. The neighbour test that catches an
    axis of several labels cannot catch a single one.

    And a roman next to a bare number while a LETTER is open is that letter's
    own numbering continuing, not a new question: three Maths papers had a
    stray figure label accepted as a head because "(i)" followed it, which
    created bare-roman leaves under a question that never printed them.
    """
    for text in blocks[index + 1:index + 7]:
        letter, roman, _ = _leading(text)
        if letter or roman:
            if roman and not letter and open_letter is not None:
                return False
            return letter in (None, 'a') and roman in (None, 'i')
    return True


def _leading(text):
    """Strip leading part markers. '(a) (i) Explain x' -> ('a', 'i', 'Explain x')."""
    letter = roman = None
    while True:
        m = MARKER.match(text)
        if not m:
            break
        tok = m.group(1)
        if LETTER.fullmatch(tok):
            letter, roman = tok, None
        elif ROMAN.fullmatch(tok):
            roman = tok
        else:
            break
        text = text[m.end():]
    return letter, roman, text


class Paper:
    """One paper, indexed by question number and part path."""

    def __init__(self, subject, year, level, component=None):
        level = {'higher': 'hl', 'ordinary': 'ol'}.get(level, level)
        self.subject, self.year, self.level = subject, year, level
        self.component = component
        # A sitting may be printed as several booklets — Biology sets Sections A
        # and B in one and Section C in another — and the question numbering
        # runs on across them, so every component is read in order as one paper.
        root = papers_dir(subject)
        # `component` reads ONE booklet. Merging is right where the numbering
        # runs on across booklets, which is what Biology does; Mathematics sets
        # two papers that both start at Question 1, so merging them collides
        # every question number in the year.
        want = rf'{year}-{level}-{component}-paper\.pdf' if component else \
            rf'{year}-{level}(-\d+)?-paper\.pdf'
        self.files = sorted(
            os.path.join(root, f) for f in os.listdir(root)
            if re.fullmatch(want, f))
        if not self.files:
            raise FileNotFoundError(f'no {year} {level} paper for {subject}')
        self.path = self.files[0]

        self.parts, self.stems = {}, {}
        q = letter = roman = None
        open_key = None          # the part a continuation block may extend
        or_pending = False       # a standalone OR announces a choice variant
        dot_heads = 0            # how many 'N.'-style heads were accepted
        qkind = {}               # q -> 'letter'|'roman': which marker opened it
        blocks = list(self._all_blocks())
        # A contents page lists "Question 12", "Question 13" and so on as bare
        # blocks with nothing under them. The second Biology booklet prints one,
        # and reading those as heads walked the parser up to 15 before the real
        # Question 11 arrived — so 11 to 15 were all rejected as going backwards
        # and four questions of that paper were unreachable. A real head is
        # never bare, and never has another bare head as its neighbour.
        bare = [i for i, t in enumerate(blocks)
                if re.fullmatch(r'Question\s+\d{1,2}|\d{1,2}\s+Question', t)]
        contents = {i for i in bare if i - 1 in bare or i + 1 in bare}
        # Same argument, one step further: a lone number standing beside other
        # lone numbers is a graph axis, not a head. The Argand diagram in 2021
        # OL Paper 1 Q2 labels its axes -5 to 7, and the "3" among those labels
        # was read as Question 3 -- which then swallowed Q2(b) and Q2(c) and
        # filed them under a question they have nothing to do with.
        lone = [i for i, t in enumerate(blocks)
                if re.fullmatch(r'[-\u2212]?\d{1,2}\.?', t.strip())]
        axis = {i for i in lone if i - 1 in lone or i + 1 in lone}

        for index, text in enumerate(blocks):
            if index in contents:
                continue
            # A standalone OR announces that the next head, though it repeats
            # the current question number, is a printed ALTERNATIVE the
            # student may choose instead — Construction Studies HL sets Q10
            # twice this way every year. The variant files under -q so its
            # parts never collide with the first printing's.
            if re.fullmatch(r'OR', text):
                or_pending = True
                continue
            if text.startswith('OR ') and QHEAD.match(text[3:]):
                or_pending, text = True, text[3:]
            # 2025 HL Economics letterspaces a head as 'Question 1 2' — two
            # digits, one question. QHEAD would happily read it as Question 1
            # and the forward guard would then discard it, so the joined
            # reading must come FIRST, taken only when the join is the next
            # question due and the split reading is not.
            sp = re.match(r'^Question\s+(\d)\s+(\d)\b', text)
            if sp and q is not None:
                joined_q = int(sp.group(1) + sp.group(2))
                if q < joined_q <= q + 3 and not q < int(sp.group(1)) <= q + 3:
                    text = f'Question {joined_q}' + text[sp.end():]
            m = QHEAD.match(text)
            if not m and q is not None:
                # Not every head is printed as "N." followed by a word. 2025 OL
                # Physics sets "12." in a block of its own with part (a) in the
                # next block, its Question 13 drops the full stop, and 2022 OL
                # Biology prints a bare "12". A lone number is normally the ruled
                # answer lines in an Agricultural Science booklet, so these forms
                # are only read as a head when the number is the very next
                # question due — no gap, no tolerance.
                loose = re.match(r'(\d{1,2})\.?(\s+|$)', text)
                # Only papers that head questions 'N.' earn loose bare-number
                # heads at all: Agricultural Science writes the literal
                # 'Question N' everywhere, and a stray '19' in a diagram was
                # its only bare number — accepted, it invented a Question 19.
                if loose and dot_heads and index not in axis \
                        and int(loose.group(1)) == q + 1 \
                        and _opens_a_question(blocks, index, letter):
                    text = f'{loose.group(1)}. {text[loose.end():]}'.strip()
                    m = QHEAD.match(text) or QHEAD.match(text + ' X')
            if not m:
                unrubriced = RUBRIC_HEAD.sub('', text, count=1)
                if unrubriced != text:
                    text = unrubriced
                    m = QHEAD.match(text)
            if m:
                found = int(m.group(1) or m.group(2))
                # Questions run forward, and a head that jumps too far ahead
                # is something else that looks like one. Three failures, all in
                # Biology: a numbered list inside 2025 OL Question 15 starts at
                # "2." and threw every part after it back under Question 2; the
                # 2021 HL experiment write-up numbers its own sub-questions 2 to
                # 4; and the second booklet of that paper opens with a contents
                # page reading "Question 14" to "Question 17", which claimed
                # those numbers before the real heads reached them and cost six
                # questions. Backwards is always wrong; the gap allows for a
                # question this parser missed and for a paper that resumes at 11
                # after a Section A ending at 8.
                variant = or_pending and q is not None and found == abs(q)
                if q is not None and not (q < found <= q + 3) and not variant:
                    pass
                else:
                    if m.group(2):
                        dot_heads += 1
                    q = -found if variant else found
                    or_pending = False
                    letter, roman, open_key = None, None, None
                    self.stems.setdefault((q, None), [])
                    rest = text[m.end():].strip()
                    if rest and _leading(rest)[:2] != (None, None):
                        # "7. (a) Define an acid ..." — the head is welded to its
                        # own first part, and filing that as stimulus prose loses
                        # the part: 2021 HL Chemistry read Question 7(a) as stem
                        # and then hung (i) and (ii) off no letter at all.
                        text = rest
                    else:
                        if rest and not RUBRIC.match(rest):
                            self.stems[(q, None)].append(rest)
                        continue
            if q is None:
                continue
            if RUBRIC.match(text):
                continue

            if CROSSREF.match(text):
                # "(b) (iii) above." is the tail of the CURRENT ask referring
                # back, not a marker — reading it as one re-filed the rest of
                # the sentence into an earlier leaf.
                if open_key:
                    self.parts[open_key].append(text)
                else:
                    self.stems.setdefault((q, letter), []).append(text)
                continue

            found_letter, found_roman, rest = _leading(text)
            if found_roman == 'i' and not found_letter and letter == 'h' \
                    and _i_is_letter(blocks, index):
                # Not gated on (h) being roman-free: Physics 2025 HL Q6 sets
                # romans UNDER (h) and then continues the letter run at (i) —
                # the (j) ahead already decides, and demanding a roman-free (h)
                # silently dropped four printed asks.
                # After (h), a lone (i) is the ninth LETTER when the run goes
                # on to (j) — Chemistry's Q4 runs (a) to (l) — and the first
                # roman when it does not. The blocks ahead decide.
                found_letter, found_roman = 'i', None
            if found_letter and letter is not None and found_letter > letter \
                    and ord(found_letter) - ord(letter) > 1 \
                    and found_letter not in ('j', 'k', 'l'):
                # Letters arrive in order. A jump — (g) landing while (b) is
                # open — is a unit in a table ("Average Daily Gain (ADG) (g)"),
                # and keying it filed two years' worth of Agricultural Science
                # asks under a letter the paper never printed.
                if open_key:
                    self.parts[open_key].append(f'({found_letter}) {rest}')
                else:
                    self.stems.setdefault((q, letter), []).append(
                        f'({found_letter}) {rest}')
                continue
            if found_letter in ('j', 'k', 'l') and letter != (
                    'i' if found_letter == 'j'
                    else chr(ord(found_letter) - 1)):
                # The high letters only ever CONTINUE a run: (k) out of
                # nowhere is Construction Studies' thermal-conductivity
                # symbol, not part (k) — extending the alphabet without this
                # guard invented a phantom Q5(k) in all ten HL papers.
                if open_key:
                    self.parts[open_key].append(f'({found_letter}) {rest}')
                else:
                    self.stems.setdefault((q, letter), []).append(
                        f'({found_letter}) {rest}')
                continue
            if found_letter or found_roman:
                if qkind.get(q) is None:
                    qkind[q] = 'letter' if found_letter else 'roman'
                if qkind.get(q) == 'roman' and found_letter and not found_roman:
                    # A roman-major question (Physics: parts are (i)..(x))
                    # enumerates WITHIN a part as (a), (b) — those are lines
                    # of the current ask, not new top-level parts, and keying
                    # them invented letter leaves the paper never printed.
                    if open_key:
                        self.parts[open_key].append(f'({found_letter}) {rest}')
                    else:
                        self.stems.setdefault((q, None), []).append(
                            f'({found_letter}) {rest}')
                    continue
                if found_letter:
                    letter, roman = found_letter, found_roman
                else:
                    roman = found_roman
                key = (q, letter, roman)
                self.parts.setdefault(key, [])
                if rest:
                    self.parts[key].append(rest)
                # A part that opens a group ('(a)' with prose but no roman yet)
                # doubles as the stem for the romans beneath it.
                open_key = key
                continue

            if FURNITURE.match(text):
                open_key = None
                continue

            joined = ' '.join(self.parts[open_key]) if open_key else ''
            # Sealed by a full stop only when there are words to seal: a bare
            # given like "g′(5) = 6." is a premise, not a closed ask, and
            # sealing on it filed the real instruction into the stem.
            sealed = TERMINAL.search(joined) and re.search(r'[A-Za-z]{3,}', joined)
            if open_key and not sealed:
                self.parts[open_key].append(text)      # continuation
                continue

            if letter is None:
                self.stems.setdefault((q, None), []).append(text)
            else:
                self.stems.setdefault((q, letter), []).append(text)
            open_key = None

        self._adopt_unlettered()

    def _all_blocks(self):
        """Blocks, split where a block sets several parts at once.

        The number that heads a question stays welded to the first piece.
        Splitting "9. (a) (i) What is meant by enzyme denaturation?" at its
        first marker leaves "9." alone, and a lone "9." cannot be told from the
        booklet's numbered answer lines — which is how Biology lost questions 8
        to 15 and, when a lone number was allowed to head a question, how
        Agricultural Science lost the parts underneath every ruled answer box.
        """
        fixes = MISPRINTS.get((self.subject, self.year, self.level), [])
        carry = ''
        for path in self.files:
            for block in _blocks(path):
              # A choice question prints its alternative welded on after a
              # standalone OR — Construction Studies HL sets Q10 twice this
              # way — and the second head must stand alone to be read at all.
              for text in re.split('\\s+(?=OR\\s+\\d{1,2}\\.\\s+[A-Z("\u201c\u2018])', block):
               for text in INLINE_QHEAD.split(text):
                text = text.strip()
                if not text:
                    continue
                head = re.match(r'(\d{1,2}\.)\s+(?=\()', text)
                prefix = ''
                if head:
                    prefix, text = head.group(1) + ' ', text[head.end():]
                pieces = [p.strip() for p in INLINE_MARKER.split(text) if p.strip()]
                for i, piece in enumerate(pieces):
                    piece = (prefix + piece) if i == 0 else piece
                    if carry:
                        piece, carry = f'{carry} {piece}', ''
                    for prefix_txt, fix in fixes:
                        if piece.startswith(prefix_txt):
                            piece = fix(piece)
                    t = TRAILING_MARKER.search(piece)
                    if t:
                        carry = t.group(1)
                        piece = piece[:t.start(1)].rstrip()
                    if piece:
                        yield piece
        if carry:
            yield carry

    def _adopt_unlettered(self):
        """A question with no (a) or (i) IS a part, and was being lost.

        Short-answer sections ask the whole question outright — "1. State two
        causes of protein denaturation and give one example in each case." —
        with no marker anywhere in it. Parts were only ever recorded when a
        marker was seen, so every such question fell into the stem and vanished
        from paths(). Home Economics lost seven of its fourteen questions that
        way, all the odd-numbered ones, which are its Section A.
        """
        for (qnum, letter), lines in list(self.stems.items()):
            if letter is not None or not lines:
                continue
            if any(k[0] == qnum for k in self.parts):
                continue                      # the question has lettered parts
            self.parts[(qnum, None, None)] = list(lines)

    @staticmethod
    def _flat(lines):
        return unligature(' '.join(' '.join(lines).split())) or None

    @staticmethod
    def _prose(lines):
        return [l for l in lines if not LABELS_ONLY.match(l)]

    def text(self, qnum, letter=None, roman=None):
        """The printed wording of one part, verbatim. None if the part is absent."""
        got = self.parts.get((qnum, letter, roman))
        return self._flat(got) if got is not None else None

    def stem(self, qnum, letter=None):
        """Stimulus prose printed above the parts, verbatim."""
        return self._flat(self._prose(self.stems.get((qnum, letter)) or []))

    def paths(self):
        return sorted(self.parts, key=lambda k: (k[0], k[1] or '', k[2] or ''))

    def suspect(self, qnum, letter=None, roman=None):
        """True when this part's text needs human eyes before it becomes a card.

        Question text is normally sentences, so text that stops without terminal
        punctuation is the signal that block segmentation cut it short or pulled
        in a neighbour. It is only a signal, not a verdict: of the 41 parts it
        flags across the ten papers, most are legitimately unpunctuated — a
        true/false statement, a word bank, a match-the-item list, a fill-in-the-
        blank, or a question ending in a colon above its sub-headings. The
        authoring layer refuses to card a flagged part until the caller has
        looked at the page and said so.
        """
        t = self.text(qnum, letter, roman)
        return not t or not TERMINAL.search(t)

    @staticmethod
    def ref(key):
        q, letter, roman = key
        return f'Q{q}' + (f'({letter})' if letter else '') + (f'({roman})' if roman else '')


if __name__ == '__main__':
    import sys
    P = Paper(sys.argv[1], int(sys.argv[2]), sys.argv[3])
    for key in P.paths():
        print(f'{P.ref(key):<14} {(P.text(*key) or "")}')
