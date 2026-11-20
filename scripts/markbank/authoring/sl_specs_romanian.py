#!/usr/bin/env python3
"""Reviewed specs for the Romanian classic examination (small-languages lane).

One entry per printed ask; see sl_lib.py for the selector language. Line
numbers are lines of examiner-reports/romanian/schemes/<year>-hl.md.
"""
from sl_lib import (R, S, SR, J, L, PL, PC, QP, QL, Run, pre, prerun, PP, SP, PY, RX, PaperP, PARTP,  # noqa: F401
                    one, shown, graded, crit, examples, quote, unprinted, part, NoScheme)
from pl_listen_lib import Join  # noqa: F401

SPECS = {}


def both(*notes):
    """Several printed notes on one row, in order."""
    return lambda doc: ' '.join(n(doc) for n in notes)


def bullets(*spans):
    """Shown rows, one per printed bullet: each a span (a, b) of wrapped lines."""
    return [shown(L(a, b, after='• ')) if isinstance(a, int) else a
            for a, b in ((sp, sp) if isinstance(sp, int) else sp for sp in spans)]


# ================================================================ 2010 HL ===
# Paper p3: Q1 "(5x1 puncte)" over five expressions; the scheme answers them as
# five unlettered bullets in the paper's order (each matches its expression's
# words: docu-, edu-, infotainment, plan de marketing, obiectivitate), priced
# "(5 puncte)" for the question. Q2-Q6 "(5 puncte)" each over points with no
# split: shown, priced as a whole (10a); Q3 is one explanation. Q2's first
# bullet is one sentence the SEC bulleted line by line (rendered p2): joined.
# Parts II (30) and III (40) on the four criteria the scheme prints for both
# (p4), 30/30/30/10 % (10b).
CRIT_2010 = crit((94, 95), (96, 97), (98, 99), 100)
SPECS[2010] = [
    R('I1a', [one(L(20, 21, after='• '), PP())]),
    R('I1b', [one(L(22, 23, after='• '), PP())]),
    R('I1c', [one(L(24, 25, after='• '), PP())]),
    R('I1d', [one(L(26, 27, after='• '), PP())]),
    R('I1e', [one(L(28, 29, after='• '), PP())]),
    R('I2', [shown(J(S(32, after='• '), S(33, after='• '), S(34, after='• '))), shown(L(35, 37, after='• ')),
             shown(L(38, 41, after='• '))], whole=True),
    R('I3', [one(L(44, 47), PP())],
      rownote=quote(S(43, after='3. '), lead='The scheme heads its answer with the quotation in its own words '
                                                  '(the paper prints "anormal")')),
    R('I4', [shown(S(55, after='• '), lead=S(54)), shown(S(56, after='• '), lead=S(54)),
             shown(L(57, 58, after='• '), lead=S(54)), shown(S(60, after='• '), lead=S(59)),
             shown(S(61, after='• '), lead=S(59)), shown(L(62, 63, after='• '), lead=S(59))], whole=True,
      rownote=quote(S(53, after='4. '), lead='The scheme heads it')),
    R('I5', bullets((67, 69), (70, 72), (73, 74)), whole=True,
      rownote=quote(L(65, 66, after='5. '), lead='The scheme heads it')),
    R('I6', bullets((78, 80), 81, (82, 83), (84, 85), 86), whole=True,
      rownote=quote(L(76, 77, after='6. '), lead='The scheme heads it')),
    R('II1', [graded(L(102, 105), PARTP(), CRIT_2010)],
      rownote=quote(S(93), lead='The scheme prints')),
    R('III1', [graded(L(107, 108), PARTP(), CRIT_2010)], source='text',
      rownote=quote(S(93), lead='The scheme prints'),
      question=QP(4, 'Scrieţi un comentariu de aproximativ 300', '1. “Informaţia')),
    R('III2', [graded(L(107, 108), PARTP(), CRIT_2010)],
      rownote=quote(S(93), lead='The scheme prints'),
      question=QP(4, 'Scrieţi un comentariu de aproximativ 300', '2. Nimeni')),
]


# ================================================================ 2011 HL ===
# Paper p4: PARTEA I "(30/100)", Q1 "(5 x 1 punct)" over five expressions a)-e);
# Q2-Q6 "(5 puncte)" each; PARTEA II "(30/100)"; PARTEA III "(40/100)", two
# titles joined by "SAU". The census's 13 asks are the paper's 13.
# Scheme (rendered pp3-5): Q1 answers the five expressions as five unlettered
# bullets in the paper's order, priced "(5 puncte)" for the question. Paired by
# order because each gloss's wording matches its expression: elita intelectuală
# / "mai aleşi intelectuali", s-a insinuat / "s-a strecurat", iscodesc /
# "cercetează ... să afle un secret", mediul academic / "societate de învăţaţi",
# a învigorat limba / "dă vigoare ... limbii". Q2 is one printed list (no
# bullets): one row at the printed price. Q3-Q6 print two or three bullets
# with no split: shown, priced as a whole (10a), each under the scheme's own
# heading. Parts II (30) and III (40) are marked on the four criteria printed
# on p4 (30/30/30/10 %, whole numbers of both totals: 10b), each part under its
# own descriptive line (p5). Under Part II the scheme also prints four bullets
# of content: quoted as examples, not a checklist. Printed error (10f): the
# scheme names the professor "Andrei Bulai", the paper "Alfred Bulai" (p4).
CRIT_2011 = crit((74, 75), (76, 77), (78, 79), 80)


def _head(a, b=None, after=None):
    return quote(L(a, b, after=after), lead='The scheme heads it')


def _bulai(d):
    paper = J(PC(4, 'Referindu-vă la text (p.5)', after='Profesorului '),
              PC(4, 'Bulai “Astea', before=' “Astea')).text(d)
    scheme = S(90, after='profesorul ', before=' relativizează').text(d)
    return f'The scheme names the speaker “{scheme}”; the paper prints “{paper}”.'


ESSAY_2011 = 'Scrieţi un comentariu de aproximativ 300'
SPECS[2011] = [
    R('I1a', [one(S(22, after='• '), PP())]),
    R('I1b', [one(S(23, after='• '), PP())]),
    R('I1c', [one(S(24, after='• '), PP())]),
    R('I1d', [one(S(25, after='• '), PP())]),
    R('I1e', [one(S(26, after='• '), PP())]),
    R('I2', [one(L(29, 31), PP())], rownote=_head(28, after='2. ')),
    R('I3', bullets(34, 35), whole=True, rownote=_head(33, after='3. ')),
    R('I4', bullets((39, 40), 41, (42, 43)), whole=True, rownote=_head(37, 38, after='4. ')),
    R('I5', bullets((51, 55), (56, 57)), whole=True, rownote=_head(49, 50, after='5. ')),
    R('I6', bullets((60, 63), (64, 66), (67, 70)), whole=True, rownote=_head(59, after='6. ')),
    R('II1', [graded(L(86, 89), PARTP(), CRIT_2011)],
      rownote=both(quote(S(73), lead='The scheme prints'),
                   examples(None, L(90, 93, after='• '), L(94, 95, after='• '), L(96, 98, after='• '),
                            L(99, 103, after='• ')),
                   _bulai)),
    R('III1', [graded(L(105, 106), PARTP(), CRIT_2011)],
      rownote=quote(S(73), lead='The scheme prints'),
      question=QP(4, ESSAY_2011, Run('1. În zilele noastre', 'simplificate.'))),
    R('III2', [graded(L(105, 106), PARTP(), CRIT_2011)],
      rownote=quote(S(73), lead='The scheme prints'),
      question=QP(4, ESSAY_2011, Run('2. ”Majoritatea', '(al 16-lea'))),
]
# The census reads the reading text as p4 (the questions page); the passage is
# printed on pp2-3 (rendered: title "DE CE VORBIM ÎN ENGLEZĂ?" on p2,
# paragraphs 1-8 over pp2-3, questions from p4).
for _s in SPECS[2011]:
    _s.pages = (2, 3)


# ================================================================ 2012 HL ===
# Paper (rendered pp3-4): PARTEA I "(30/100)"; Q1 prints its five expressions
# a)-e) and ONE "(5 puncte)" under e) for the question as a whole (no "5 x 1"
# as 2010 and 2011 print); Q2-Q6 "(5 puncte)" each, every price on a line of
# its own under the question; PARTEA II "(30/100)"; PARTEA III "(40/100)", two
# titles joined by "SAU". The census's 13 asks are the paper's 13, but it
# reads three prices wrongly: it gives Q1's "(5 puncte)" to e) alone, does not
# read Q4's (p4 y202), and opens Q5's text with Q4's "puncte)". Q4 and Q5 are
# priced from their own printed lines (PY) and Q5's question is cut from the
# paper.
# Scheme (rendered pp3-6): Q1 answers the five expressions as five unlettered
# dashes in the paper's order and prices "(5 puncte)" for the question. Paired
# by order because each gloss's wording matches its expression: "democratizarea
# totală a publicatului" / "publicarea articolelor ... a devenit accesibilă
# orcui"; "lectura este pozitiv conotată" / "Cititul este perceput ... bună şi
# nobilă"; "citesc cu nesaţ" / "nerăbdători şi dornici să citească";
# "predispuşi să-l facă praf" / "abordează textul cu intenţia de a-l critica";
# "o fervoare a demascării" / "O pasiune ... de a face public ... părţile
# ascunse". Neither paper nor scheme prices an expression on its own, so Q1(a)-
# (e) are CARDING-STANDARD 10i asks (never split the 5): they are NOT in SPECS
# below but in Q1 (carded at the question)_2012, each with its scheme answer as a shown row;
# `total=` there is the Q1 price to lift into unpricedSection.totalMarks, not
# the card's own total (10i: questionTotal, totalMarks 0). sl_lib in this
# worktree has no unpricedSection shape (d9181d7ef is not in HEAD).
# Q2, Q3, Q4 and Q6 print two to five dashes with no split: shown, priced as a
# whole (10a), each under the scheme's own heading. Q5 prints one paragraph:
# one row at the printed price. Q6's second dash runs over the page break
# (p4 "Avem cu toţii ..." to p5 "lectură bună şi una mai puţin bună."): joined.
# Parts II (30) and III (40) are marked on the four criteria printed on p5
# (30/30/30/10 %, whole numbers of both totals: 10b), each under its own
# descriptive line. Under Part II the scheme also prints three dashes of
# content: quoted as examples, not a checklist (the third runs over the p5/p6
# break; the second's "responsabi-"/"litate" is joined as printed).


def dashes(*spans):
    """Shown rows, one per printed dash: each a span (a, b) of wrapped lines."""
    return [shown(L(a, b, after='- ')) for a, b in ((sp, sp) if isinstance(sp, int) else sp for sp in spans)]


def _head(a, b=None, after=None):
    return quote(L(a, b, after=after), lead='The scheme heads it')


CRIT_2012 = crit((105, 106), (107, 108), (109, 110), 111)
ESSAY_2012 = Run('Scrieţi un comentariu de aproximativ 300', 'punctul vostru de vedere')
Q1P_2012 = PY(3, 771)
SPECS[2012] = [
    R('I2', dashes((38, 39), (40, 41), (42, 43), 44, (45, 47)), whole=True,
      rownote=_head(37, after='2. ')),
    R('I3', dashes((53, 55), (56, 57), (58, 61)), whole=True,
      rownote=_head(49, after='3. ')),
    R('I4', dashes((65, 70), (71, 73)), whole=True, total=PY(4, 202),
      rownote=_head(63, 64, after='4. ')),
    R('I5', [one(L(77, 83), PY(4, 308))], total=PY(4, 308),
      rownote=_head(75, 76, after='5. '),
      question=QP(4, '5. Explicaţi de ce este comparat', Run('“ Unele sînt', '(p.5)'))),
    R('I6', [shown(L(86, 88, after='- ')), shown(J(L(89, 92, after='- '), S(96))),
             shown(L(97, 101, after='- '))], whole=True,
      rownote=_head(85, after='6. ')),
    R('II1', [graded(L(113, 116), PARTP(), CRIT_2012)],
      rownote=both(quote(S(104), lead='The scheme prints'),
                   examples(None, L(117, 120, after='- '),
                            Join(L(121, 123, after='- '), L(124, 127), sep=''),
                            J(L(128, 134, after='- '), L(138, 139))))),
    R('III1', [graded(L(141, 142), PARTP(), CRIT_2012)],
      rownote=quote(S(104), lead='The scheme prints'),
      question=QP(4, ESSAY_2012, '1. Cuvântul scris')),
    R('III2', [graded(L(141, 142), PARTP(), CRIT_2012)],
      rownote=quote(S(104), lead='The scheme prints'),
      question=QP(4, ESSAY_2012, '2. În societatea modernă')),
]

# CARD-STANDARD 10i, not built by sl_lib here: see the comment above.

# The reading text is printed on pp2-3 (rendered: "Citind..." on p2, paragraphs
# 1-8 to Sever VOINESCU's byline on p3; questions from p3 y581).
SPECS[2012].insert(0, R('I1', [shown(L(22, 24, after='- ')), shown(S(25, after='- ')), shown(L(26, 28, after='- ')), shown(L(29, 32, after='- ')), shown(L(33, 35, after='- '))], whole=True, total=Q1P_2012,
      question=QL(3, Run('1. Explicaţi pe scurt cu', 'de context.'), 'a) democratizarea to', 'b) lectura este pozi', 'c) citesc cu nesaţ (', 'd) predispuşi să-l f', 'e) o fervoare a dema')))
for _s in SPECS[2012]:
    _s.pages = (2, 3)


# ================================================================ 2014 HL ===
# Paper (rendered pp3-4): PARTEA I "(30/100)"; Q1 asks for five words and
# expressions "scrise îngroşat în text" (bold in the passage, pp2-3; each is
# reprinted in italics in the question, so no stem is needed) and prints ONE
# "(5 puncte)" under e) for the question as a whole; Q2-Q6 "(5 puncte)" each;
# PARTEA a II-a "(30/100)"; PARTEA a III-a "(40/100)", two titles joined by
# "SAU". The census's 13 asks are the paper's 13; it gives Q1's "(5 puncte)"
# to e) alone.
# Scheme (rendered pp3-5): Q1 letters its answers a)-e), reprinting each
# expression above its dash (e) as "indiferenţă", the paper's "indiferenţa"),
# and prices "(5 puncte)" for the question: CARD-STANDARD 10i asks, NOT in
# SPECS but in Q1 (carded at the question)_2014 (see 2012). Q2-Q6 print three or four dashes
# each with no split: shown, priced as a whole (10a), under the scheme's own
# heading; Q3's third dash opens p4 (no line runs over the break); Q6's last
# dash ends in "(5 puncte)" on its own line of text, cut before it. Parts II
# (30) and III (40) are marked on the four criteria printed on p5 (30/30/30/10
# %, whole numbers: 10b), under each part's own descriptive line. Under Part II
# the scheme prints one dash and two undashed paragraphs at the same indent
# (rendered p5): quoted as examples, not a checklist. Paper and scheme
# disagree on Part III's first title (paper "în primul rând", scheme "înainte
# de toate"): the paper wins on the question, the scheme's words quoted (10f).


def dashes(*spans, mark='– '):
    """Shown rows, one per printed dash: each a span (a, b) of wrapped lines."""
    return [shown(L(a, b, after=mark)) for a, b in ((sp, sp) if isinstance(sp, int) else sp for sp in spans)]


def _head(a, b=None, after=None):
    return quote(L(a, b, after=after), lead='The scheme heads it')


CRIT_2014 = crit(149, (150, 151), (152, 153), 154)
NOTE_2014 = quote(L(147, 148), lead='The scheme prints')
ESSAY_2014 = Run('Scrieți un eseu', 'cuvinte):')
Q1P_2014 = PY(3, 582)
SPECS[2014] = [
    R('I2', dashes((68, 71), (72, 75), (76, 78)), whole=True, rownote=_head(67, after='2. ')),
    R('I3', dashes((81, 84), (85, 88), (93, 95)), whole=True, rownote=_head(80, after='3. ')),
    R('I4', dashes((99, 102), (103, 106), (107, 109)), whole=True, rownote=_head(97, 98, after='4. ')),
    R('I5', dashes((113, 116), (117, 118), (119, 121), (122, 124)), whole=True,
      rownote=_head(111, 112, after='5. ')),
    R('I6', dashes((127, 130), (131, 136), (137, 138)) + [shown(L(139, 141, after='– ', before=' (5 puncte)'))],
      whole=True, rownote=_head(126, after='6. ')),
    R('II1', [graded(L(156, 157), PARTP(), CRIT_2014)],
      rownote=both(NOTE_2014,
                   examples(None, L(158, 161, after='– '), L(162, 167), L(168, 173)))),
    R('III1', [graded(L(175, 176), PARTP(), CRIT_2014)],
      rownote=both(NOTE_2014,
                   quote(S(177, after='1 . '), lead='The scheme reprints this title as')),
      question=QP(4, ESSAY_2014, '1. Bogăția')),
    R('III2', [graded(L(175, 176), PARTP(), CRIT_2014)],
      rownote=NOTE_2014,
      question=QP(4, ESSAY_2014, '2. „Chiar')),
]

# CARD-STANDARD 10i, not built by sl_lib here (see 2012). The scheme letters
# each answer under its reprinted expression: a) line 51, b) 54, c) 56, d) 59,
# e) 63.

# The reading text is printed on pp2-3 (rendered: paragraphs to paragraph 8
# and Maria IORDĂNESCU's byline on p3; questions from p3 "ÎNTREBĂRI").
SPECS[2014].insert(0, R('I1', [shown(L(52, 53, after='– ')), shown(S(55, after='– ')), shown(L(57, 58, after='– ')), shown(L(60, 62, after='– ')), shown(L(64, 65, after='– '))], whole=True, total=Q1P_2014,
      question=QL(3, '1. Explicați următoarele cuvin', 'a) locuri incredibil', 'b) patrimoniu cultur', 'c) a imita', 'd) păreri proaspete', 'e) indiferența')))
for _s in SPECS[2014]:
    _s.pages = (2, 3)


# ================================================================ 2016 HL ===
# Paper (rendered pp3-4): PARTEA I "(30/100)"; Q1 asks for five words and
# expressions "scrise îngroșat în text" (each reprinted in the question) and
# prints ONE "(5 puncte)" under e) for the question as a whole; Q2-Q6 "(5
# puncte)" each; PARTEA a II-a "(30/100)"; PARTEA a III-a "(40/100)", two
# titles joined by "SAU". The census's 13 asks are the paper's 13; it gives
# Q1's "(5 puncte)" to e) alone.
# Scheme (rendered pp3-6): Q1 letters its answers a)-e), each after its
# expression and a dash on the same line, and prices "(5 puncte)" for the
# question: CARD-STANDARD 10i asks, NOT in SPECS but in Q1 (carded at the question)_2016 (see
# 2012). Q2-Q5: the scheme reprints each question in italics under its
# heading, then three or four dashes with no split: shown, priced as a whole
# (10a), under the heading; Q5's first dash runs over the p4/p5 break
# ("poate" / "însemna"): joined. Q6 prints two indented paragraphs of model
# answer (rendered p5) under its reprinted question: shown, priced as a whole.
# Parts II (30) and III (40) are marked on the four criteria printed on p5
# (30/30/30/10 %, whole numbers: 10b). Part II prints no descriptive line of
# its own: its head is the scheme's line introducing the criteria (as 2015,
# and Dutch 2010-2011); under it the scheme reprints the task (as the paper
# prints it) and two paragraphs of model commentary, quoted as examples, not
# a checklist. Part III is headed by its own descriptive line (rendered p6).


def dashes(*spans, mark='- '):
    """Shown rows, one per printed dash: each a span (a, b) of wrapped lines."""
    return [shown(L(a, b, after=mark)) for a, b in ((sp, sp) if isinstance(sp, int) else sp for sp in spans)]


def _head(a, b=None, after=None):
    return quote(L(a, b, after=after), lead='The scheme heads it')


CRIT_2016 = crit(160, (161, 162), (163, 164), 165)
NOTE_2016 = quote(L(158, 159), lead='The scheme prints')
ESSAY_2016 = Run('Scrieți un eseu', 'cuvinte):')
Q1P_2016 = PY(3, 653)
SPECS[2016] = [
    R('I2', dashes((67, 70), (71, 75), (76, 79)), whole=True, rownote=_head(65, after='2. ')),
    R('I3', dashes((88, 91), (92, 95), (96, 97)), whole=True, rownote=_head(85, after='3. ')),
    R('I4', dashes((103, 107), (108, 110), (111, 115), (116, 118)), whole=True,
      rownote=_head(99, 100, after='4. ')),
    R('I5', [shown(J(L(124, 125, after='- '), L(130, 132)))] + dashes((133, 134), (135, 138)), whole=True,
      rownote=_head(120, 121, after='5. ')),
    R('I6', [shown(L(143, 147)), shown(L(148, 155))], whole=True, rownote=_head(140, after='6. ')),
    R('II1', [graded(L(158, 159), PARTP(), CRIT_2016)],
      rownote=examples(None, L(174, 183), L(184, 187))),
    R('III1', [graded(L(189, 190), PARTP(), CRIT_2016)], rownote=NOTE_2016,
      question=QP(4, ESSAY_2016, Run('1 . „Cu cât', 'între noi.'))),
    R('III2', [graded(L(189, 190), PARTP(), CRIT_2016)], rownote=NOTE_2016,
      question=QP(4, ESSAY_2016, Run('2. „Lumea', 'democratică și'))),
]

# CARD-STANDARD 10i, not built by sl_lib here (see 2012). Each answer is cut
# after the dash that follows its expression on the scheme's own line.

# The reading text is printed on pp2-3 (questions from p3 PARTEA I, y451).
SPECS[2016].insert(0, R('I1', [shown(L(51, 54, after=' – ')), shown(L(55, 56, after=' – ')), shown(L(57, 58, after=' – ')), shown(L(59, 60, after=' – ')), shown(L(61, 63, after=' – '))], whole=True, total=Q1P_2016,
      question=QL(3, Run('1. Explicați pe scurt ur', 'perifraze și ținând cont'), 'a) oamenii de valoar', 'b) pseudo-vedete', 'c) trăncăneală', 'd) decăderea moravur', 'e) criza de încreder')))
for _s in SPECS[2016]:
    _s.pages = (2, 3)


# ================================================================ 2013 HL ===
# GLYPHS FIRST: this sitting's scheme .md and the paper's own text layer print
# Romanian letters as other code points ("܊" for ţ/ț, "܈" for ş/ș, "Ġ" and "а"
# for ţ, "ú" and "Ю" for ş, "һ" for ă, "Ӽ" for Ă; 78 scheme lines, 40 paper
# lines, the questions included). The rendered pages print the right letters.
# Every card below would show the wrong ones until the .md and the paper's text
# are glyph-repaired (map derived from glyph ids, never by hand). The specs are
# written on the current line numbers; no anchor or opening below holds a
# mangled character, so they survive an in-place repair.
# Paper (rendered pp3-4): PARTEA I "(30/100)"; Q1 prints its five expressions
# a)-e), each with "(paragraful N)", and ONE "(5 puncte)" under e) for the
# question as a whole; Q2-Q6 "(5 puncte)" each on lines of their own; PARTEA a
# II-a "(30/100)"; PARTEA a III-a "(40/100)", two titles joined by "SAU". The
# census's 13 asks are the paper's 13; it gives Q1's "(5 puncte)" to e) alone.
# Scheme (rendered pp3-5): Q1 LETTERS its answers a)-e), reprinting each
# expression above its dash, and prices "(5 puncte)" for the question. No
# expression is priced on its own by paper or scheme, so Q1(a)-(e) are
# CARD-STANDARD 10i asks: NOT in SPECS but in Q1 (carded at the question)_2013 (see 2012).
# Q2-Q6 print three or four dashes each with no split: shown, priced as a
# whole (10a), under the scheme's own heading; Q6's third dash runs over the
# p4/p5 break ("în" / "neînţelegere."): joined. Parts II (30) and III (40) are
# marked on the four criteria printed on p5 (30/30/30/10 %, whole numbers:
# 10b), under each part's own descriptive line; under Part II the scheme also
# prints three dashes of content, quoted as examples, not a checklist.


def dashes(*spans, mark='– '):
    """Shown rows, one per printed dash: each a span (a, b) of wrapped lines."""
    return [shown(L(a, b, after=mark)) for a, b in ((sp, sp) if isinstance(sp, int) else sp for sp in spans)]


def _head(a, b=None, after=None):
    return quote(L(a, b, after=after), lead='The scheme heads it')


CRIT_2013 = crit(147, (148, 149), (150, 151), 152)
ESSAY_2013 = Run('Scrie', 'cuvinte):')
Q1P_2013 = PY(3, 583)
SPECS[2013] = [
    R('I2', dashes((72, 73), (74, 76), (77, 79)), whole=True, rownote=_head(71, after='2. ')),
    R('I3', dashes(82, (83, 85), (91, 93), (94, 96)), whole=True, rownote=_head(81, after='3. ')),
    R('I4', dashes((100, 103), (104, 107), (108, 110)), whole=True, rownote=_head(98, 99, after='4. ')),
    R('I5', dashes((114, 115), (116, 119), (120, 122), (123, 125)), whole=True,
      rownote=_head(112, 113, after='5. ')),
    R('I6', dashes((128, 131), (132, 133)) + [shown(J(L(134, 135, after='– '), L(141, 142)))], whole=True,
      rownote=_head(127, after='6. ')),
    R('II1', [graded(L(154, 157), PARTP(), CRIT_2013)],
      rownote=both(quote(L(145, 146), lead='The scheme prints'),
                   examples(None, L(158, 163, after='– '), L(164, 165, after='– '), L(166, 170, after='– ')))),
    R('III1', [graded(L(172, 173), PARTP(), CRIT_2013)],
      rownote=quote(L(145, 146), lead='The scheme prints'),
      question=QP(4, ESSAY_2013, '1. Cultura')),
    R('III2', [graded(L(172, 173), PARTP(), CRIT_2013)],
      rownote=quote(L(145, 146), lead='The scheme prints'),
      question=QP(4, ESSAY_2013, '2. Să-')),
]

# CARD-STANDARD 10i, not built by sl_lib here (see 2012). The scheme letters
# each answer under its reprinted expression: a) line 51, b) 55, c) 58, d) 62,
# e) 67.

# The reading text is printed on pp2-3 (rendered: "Absurdul de zi cu zi.
# Comunicarea" on p2, to Sever VOINESCU's byline on p3 y340).
SPECS[2013].insert(0, R('I1', [shown(L(52, 54, after='– ')), shown(L(56, 57, after='– ')), shown(L(59, 61, after='– ')), shown(L(63, 66, after='– ')), shown(L(68, 69, after='– '))], whole=True, total=Q1P_2013,
      question=QL(3, Run('1. Explicați pe scurt ur', 'contextul în care apar:'), Run('a) lume complet absu', '(paragraful 1)'), 'b) jalnice clişee al', Run('c) se dau bani grei', '(paragraful 3)'), Run('d) propagandă falsă', '(paragraful 4)'), Run('e) cronică neputință', '(paragraful 4)'))))
for _s in SPECS[2013]:
    _s.pages = (2, 3)


# ================================================================ 2015 HL ===
# GLYPHS FIRST: this sitting's scheme .md prints Romanian letters as other code
# points on 86 lines ("܊" for ţ/ț, "܈" for ş/ș, "Ġ" and "а" for ţ, "ú" and
# "Ю" for ş, "Ӽ" for Ă; pp1-2 are a shifted font, not used here). The rendered
# scheme prints the right letters. Every scheme cut below would show the wrong
# ones until the .md is glyph-repaired (map derived from glyph ids, never by
# hand). The paper's questions are clean. No anchor below holds a mangled
# character, so the specs survive an in-place repair.
# Paper (rendered pp3-4): PARTEA I "(30/100)"; Q1 asks for five words and
# expressions "scrise îngroşat în text" (each reprinted in the question) and
# prints ONE "(5 puncte)" under e) for the question as a whole; Q2-Q6 "(5
# puncte)" each; PARTEA a II-a "(30/100)"; PARTEA a III-a "(40/100)", two
# titles joined by "SAU". The census's 13 asks are the paper's 13; it gives
# Q1's "(5 puncte)" to e) alone.
# Scheme (rendered pp3-6): Q1 letters its answers a)-e), each after its
# expression and a dash on the same line, and prices "(5 puncte)" for the
# question: CARD-STANDARD 10i asks, NOT in SPECS but in Q1 (carded at the question)_2015 (see
# 2012). Q2-Q6: the scheme reprints each question in italics under its
# heading, then two to four dashes with no split: shown, priced as a whole
# (10a), under the heading; Q5's first dash runs over the p4/p5 break
# ("praful" / "s-ar putea"): joined. Parts II (30) and III (40) are marked on
# the four criteria printed on p5 (30/30/30/10 %, whole numbers: 10b). Part II
# prints no descriptive line of its own (2010-2014 print "Comentarea
# citatului ..."): its head is the scheme's line introducing the criteria, as
# Dutch 2010 and 2011 (S(57), S(89)). Under it the scheme reprints the task
# without the paper's "doar" ("Soylent hrăneşte corpul", paper "hrăneşte doar
# corpul"): the paper wins on the question, the scheme's words quoted (10f);
# then four unheaded paragraphs, quoted as examples, not a checklist. LIBRARY
# LIMIT: the first paragraph wraps onto line 165, which opens with a printed
# dash ("un tot" / "– corp, minte, suflet"); Sel's bullet strip drops it, so
# the quote reads "un tot corp, minte, suflet". Part III is headed by its own
# descriptive line (rendered p6).


def dashes(*spans, mark='- '):
    """Shown rows, one per printed dash: each a span (a, b) of wrapped lines."""
    return [shown(L(a, b, after=mark)) for a, b in ((sp, sp) if isinstance(sp, int) else sp for sp in spans)]


def _head(a, b=None, after=None):
    return quote(L(a, b, after=after), lead='The scheme heads it')


CRIT_2015 = crit(151, (152, 153), (154, 155), 156)
NOTE_2015 = quote(L(149, 150), lead='The scheme prints')
ESSAY_2015 = Run('Scrieţi un eseu', 'cuvinte):')
Q1P_2015 = PY(3, 529)
SPECS[2015] = [
    R('I2', dashes((69, 72), (73, 76), (77, 78)), whole=True, rownote=_head(66, after='2. ')),
    R('I3', dashes((87, 90), (91, 94), (95, 96), (97, 98)), whole=True, rownote=_head(84, after='3. ')),
    R('I4', dashes((104, 107), (108, 109), (110, 112)), whole=True, rownote=_head(100, 101, after='4. ')),
    R('I5', [shown(J(L(118, 120, after='- '), L(125, 126)))] + dashes((127, 130), (131, 132)), whole=True,
      rownote=_head(114, 115, after='5. ')),
    R('I6', dashes((137, 141), (142, 146)), whole=True, rownote=_head(134, after='6. ')),
    R('II1', [graded(L(149, 150), PARTP(), CRIT_2015)],
      rownote=both(quote(L(162, 163), lead='The scheme reprints the task as'),
                   examples(None, J(S(164), SR(165), S(166), S(167)), L(168, 171), L(172, 173), L(174, 175)))),
    R('III1', [graded(L(177, 178), PARTP(), CRIT_2015)], rownote=NOTE_2015,
      question=QP(4, ESSAY_2015, Run('1 . „Oamenii', 'simtă că trăiesc'))),
    R('III2', [graded(L(177, 178), PARTP(), CRIT_2015)], rownote=NOTE_2015,
      question=QP(4, ESSAY_2015, '2. „ Cei care')),
]

# CARD-STANDARD 10i, not built by sl_lib here (see 2012). Each answer is cut
# after the dash that follows its expression on the scheme's own line.

# The reading text is printed on pp2-3 (rendered; questions from p3 PARTEA I).
SPECS[2015].insert(0, R('I1', [shown(L(53, 55, after=' – ')), shown(L(56, 57, after=' – ')), shown(L(58, 59, after=' – ')), shown(L(60, 61, after=' – ')), shown(L(62, 64, after=' – '))], whole=True, total=Q1P_2015,
      question=QL(3, '1. Explicaţi pe scurt următoar', 'a) trebuincioasă', 'b) mâncare minune', 'c) pământ suprapopul', 'd) ideea va prinde', Run('e) viaţă excepţional', '(5 puncte)'))))
for _s in SPECS[2015]:
    _s.pages = (2, 3)


# ================================================================ 2017 HL ===
# Paper (rendered pp3-4): PARTEA I "(30/100)"; Q1 asks for five words and
# expressions "scrise îngroșat în text" (each reprinted in italics in the
# question) and prints ONE "(5 puncte)" beside e) (p3 y722, the cell at x496)
# for the question as a whole, no "5 x 1"; Q2-Q6 "(5 puncte)" each; PARTEA a
# II-a "(30/100)"; PARTEA a III-a "(40/100)", two titles joined by "SAU". The
# census's 13 asks are the paper's 13; it gives Q1's "(5 puncte)" to e) alone,
# so Q1 is carded at the QUESTION ('I1', questionTotal, as 2012/2014/2016).
# Scheme (rendered pp3-7): Q1 letters its answers a)-e), each after its
# expression and " – " on the same line, and prints "(5 puncte)" once for the
# question (line 65): five shown rows, cut after the dash. Q2-Q6: the scheme
# heads each question with its own descriptive line, reprints the question in
# italics, then prints dashes (Q2, Q3, Q5) or paragraphs (Q4, Q6) with no split,
# "(5 puncte)" under the lot: shown, priced as a whole (10a), under the
# heading. Q5's third dash opens p6 (no line runs over the break).
# Judgement calls:
# - Q5's first dash prints an appositive en dash at the start of a wrapped line
#   (line 127 "– de cât mai mulți tineri,așadar.", rendered p5). The selector
#   strips a leading dash from every line, so the row reads "... ca tine de
#   cât mai mulți tineri,așadar." without it (provenance unaffected: normalise
#   drops punctuation). Flagged for the lead.
# - The scheme reprints Q3 and Q4 in other words than the paper ("aleg un
#   limbaj" for the paper's "aleg limbajul"; "este spre bine sau spre rău" for
#   "reprezintă un lucru pozitiv sau unul negativ"): the paper wins on the
#   question, the scheme's reprint quoted in the note (10f).
# - Parts II (30) and III (40) are marked on the four criteria printed on p6
#   under "Notă:" (30/30/30/10 %, whole numbers of both totals: 10b). Part II
#   prints no descriptive line of its own: its head is the scheme's line
#   introducing the criteria (lines 155-156, as 2016); under it the scheme
#   reprints the task as the paper prints it and one paragraph of model answer
#   (171-178), quoted as examples, not a checklist. Part III is headed by its
#   own descriptive line (180-181).
# - The scheme reprints Part III's second title in other words ("să fie
#   prețuite în mod egal." / "Comentează" for the paper's "să aibă aceeași
#   importanță." / "Comentați"): the paper wins, the scheme's words quoted.
# - Reading text: pp2-3 (rendered: title "Ce știm, de fapt, despre România?"
#   on p2, paragraphs 1-5 to the byline on p3; questions from p3 y521).
# No glyph problems: the rule line prints U+1EB7 ("rặspunsurile", fine).

CRIT_2017 = crit(157, (158, 159), (160, 161), 162)
NOTE_2017 = quote(L(155, 156), lead='The scheme prints')
ESSAY_2017 = 'Scrieți un eseu de aproximativ 300'
Q1P_2017 = PY(3, 722)


def _reprint_2017(a, b=None, after=None):
    return quote(L(a, b, after=after), lead='The scheme reprints the question as')


SPECS[2017] = [
    R('I1', [shown(L(51, 53, after=' – ')), shown(L(54, 55, after=' – ')), shown(L(56, 59, after=' – ')),
             shown(L(60, 62, after=' – ')), shown(L(63, 64, after=' – '))], whole=True, total=Q1P_2017,
      question=QL(3, Run('1. Explicați pe scurt', 'ținând cont de contextul'), 'a) lumea în schimbare',
                  'b) prăpădește', 'c) știri derutante', 'd) tradiție', 'e) autenticitate')),
    R('I2', dashes((72, 76), (77, 78), (79, 81), mark='- '), whole=True, rownote=_head(66, after='2. ')),
    R('I3', dashes((86, 88), (89, 92), (93, 96), mark='- '), whole=True,
      rownote=both(_head(83, after='3. '), _reprint_2017(84, 85))),
    R('I4', [shown(L(108, 113)), shown(L(114, 117))], whole=True,
      rownote=both(_head(98, 99, after='4. '), _reprint_2017(104, 107))),
    R('I5', [shown(J(L(123, 126, after='- '), SR(127)))] + dashes((128, 131), (136, 138), mark='- '), whole=True,
      rownote=_head(119, 120, after='5. ')),
    R('I6', [shown(L(143, 146)), shown(L(147, 152))], whole=True, rownote=_head(140, after='6. ')),
    R('II1', [graded(L(155, 156), PARTP(), CRIT_2017)],
      rownote=examples(None, L(171, 178))),
    R('III1', [graded(L(180, 181), PARTP(), CRIT_2017)], rownote=NOTE_2017,
      question=QP(4, ESSAY_2017, Run('1 . „ Oricâtă', 'Prof. Dr. Psihiatru'))),
    R('III2', [graded(L(180, 181), PARTP(), CRIT_2017)],
      rownote=both(NOTE_2017, quote(L(186, 188, after='2. '), lead='The scheme reprints this title as')),
      question=QP(4, ESSAY_2017, Run('2. „Părerea', 'acest punct de vedere'))),
]
for _s in SPECS[2017]:
    _s.pages = (2, 3)


# ================================================================ 2018 HL ===
# Paper (rendered pp3-4): PARTEA I "(30/100)"; Q1 asks for five words and
# expressions "scrise îngroșat în text" (each reprinted in italics) and prints
# ONE "(5 puncte)" on a line of its own under e) (p3 y599) for the question as
# a whole, no "5 x 1"; Q2-Q6 "(5 puncte)" each; PARTEA a II-a "(30/100)";
# PARTEA a III-a "(40/100)", titles a. and b. joined by "SAU". The census's 13
# asks are the paper's 13; it gives Q1's "(5 puncte)" to e) alone, so Q1 is
# carded at the QUESTION ('I1', questionTotal, as 2012/2014/2016).
# Scheme (rendered pp3-7): Q1 letters its answers a)-e), each after its
# expression and " – " on the same line, "(5 puncte)" once for the question
# (line 65): five shown rows. Q2-Q6: the scheme heads each question with its
# own descriptive line, reprints it in italics, then prints three or four
# indented paragraphs of model answer with no split, "(5 puncte)" under the
# lot: shown, priced as a whole (10a), under the heading.
# Judgement calls:
# - Q2's first paragraph runs over the p3/p4 break ("într-o" / "astfel de lume
#   virtuală"): joined.
# - Q6's first paragraph: p5's last line ("unele prin importanța lor, ...
#   stupiditatea lor.") is set justified to the margin and p6 opens
#   "Curiozitatea ne împinge ..." at the same indent as its own continuation
#   lines, so it is read as one paragraph running over the break: joined.
#   (Shown rows only; the split does not touch the marks.)
# - The scheme reprints Q3 as "... utilizatorilor rețelelor sociale?" (paper
#   "rețelelor de socializare?") and Part II without the paper's "regăsită în
#   text" ("Comentați această afirmație, exprimandu-va ..."): the paper wins on
#   the question, the scheme's reprint quoted (10f).
# - Parts II (30) and III (40) are marked on the four criteria printed on p6
#   under "Notă:" (30/30/30/10 %, whole numbers: 10b). Part II has no
#   descriptive line of its own: its head is the line introducing the criteria
#   (150, as 2016/2017); under its reprinted task the scheme prints two
#   paragraphs of model commentary (160-169), quoted as examples, not a
#   checklist. Part III is headed by its own descriptive line (175-176); its
#   two titles are reprinted as the paper prints them.
# - Reading text: pp2-3 (rendered: title "Am un prieten care nu se poate
#   dezlipi de telefon" on p2, paragraphs 1-6 and the byline on p3; questions
#   from p3 y306).
# No glyph problems (U+1EB7 in the rule line is printed and fine).

CRIT_2018 = crit(151, (152, 153), (154, 155), 156)
NOTE_2018 = quote(S(150), lead='The scheme prints')
ESSAY_2018 = 'Scrieți un eseu pornind'
Q1P_2018 = PY(3, 599)


def _reprint_2018(a, b=None, after=None, lead='The scheme reprints the question as'):
    return quote(L(a, b, after=after), lead=lead)


SPECS[2018] = [
    R('I1', [shown(L(52, 53, after=' – ')), shown(L(54, 55, after=' – ')), shown(L(56, 59, after=' – ')),
             shown(L(60, 61, after=' – ')), shown(L(62, 64, after=' – '))], whole=True, total=Q1P_2018,
      question=QL(3, Run('1. Explicați pe scurt', 'perifraze și ținând cont'), 'a) introvertire',
                  'b) lumea virtuală', 'c) preferăm să ne', 'd) să pozeze', 'e) nevoia de a evada')),
    R('I2', [shown(J(L(69, 70), L(75, 78))), shown(L(79, 81)), shown(L(82, 84))], whole=True,
      rownote=_head(66, after='2. ')),
    R('I3', [shown(L(88, 90)), shown(L(91, 93)), shown(L(94, 95))], whole=True,
      rownote=both(_head(86, after='3. '), _reprint_2018(87))),
    R('I4', [shown(L(101, 104)), shown(L(109, 110)), shown(L(111, 113))], whole=True,
      rownote=_head(97, 98, after='4. ')),
    R('I5', [shown(L(119, 121)), shown(L(122, 123)), shown(L(124, 126)), shown(L(127, 129))], whole=True,
      rownote=_head(115, 116, after='5. ')),
    R('I6', [shown(J(L(135, 136), L(141, 142))), shown(L(143, 144)), shown(L(145, 147))], whole=True,
      rownote=_head(131, after='6. ')),
    R('II1', [graded(S(150), PARTP(), CRIT_2018)],
      rownote=both(_reprint_2018(158, 159, lead='The scheme reprints the task as'),
                   examples(None, L(160, 161), L(162, 169)))),
    R('III1', [graded(L(175, 176), PARTP(), CRIT_2018)], rownote=NOTE_2018,
      question=QP(4, ESSAY_2018, 'a. Există limite')),
    R('III2', [graded(L(175, 176), PARTP(), CRIT_2018)], rownote=NOTE_2018,
      question=QP(4, ESSAY_2018, Run('b. „Nu haina', 'ideea cuprinsă'))),
]
for _s in SPECS[2018]:
    _s.pages = (2, 3)


# ================================================================ 2019 HL ===
# Paper (rendered pp3-4): PARTEA I "(30/100)"; Q1 asks for five words and
# expressions "scrise îngroșat în text" and prints "(5 × 1 punct)" beside e)
# (p3 y572): a price per expression, so Q1 is carded letter by letter (I1a-e,
# one row at 1 mark each, as 2010/2011). Q2-Q6 "(5 puncte)" each (Q2's on its
# own question line); PARTEA a II-a "(30/100)"; PARTEA a III-a "(40/100)",
# titles a. and b. joined by "SAU". The census's 13 asks are the paper's 13 and
# it reads every price as printed.
# Scheme (rendered pp3-7): Q1 letters its answers a)-e), each after its
# expression and " – " on the same line, "(5 puncte)" once for the question:
# each answer one row at the paper's "(5 × 1 punct)". Q2-Q6: the scheme heads
# each question with its own descriptive line, reprints it in italics, then
# prints two or three indented paragraphs of model answer with no split,
# "(5 puncte)" under the lot: shown, priced as a whole (10a), under the
# heading. Paragraph breaks read on the render (first-line indents; Q3's second
# paragraph is set flush left, p4, but opens on a new line after a short one).
# Judgement calls:
# - Spelling-only differences in the scheme's reprints, left in this comment
#   and not quoted (as 2014's "indiferenţă"): Q2 "Șeherazadei" (paper
#   "Șeherezadei"); Q6 "propria experiența" (paper "experiență"); Part III a.
#   reprinted without diacritics ("Toti acei ce au acces la o biblioteca, la
#   carti ...") and with a straight opening quote.
# - Part III b.: the scheme reprints the title with words the paper does not
#   print ("Răspundeți la această întrebare într-un eseu de aproximativ 300 de
#   cuvinte, ..."): the paper wins on the question, the scheme's words quoted.
# - Parts II (30) and III (40) are marked on the four criteria printed on p6
#   under "Notă:" (30/30/30/10 %, whole numbers: 10b). Part II has no
#   descriptive line of its own: its head is the line introducing the criteria
#   (154-155, as 2016-2018); under its reprinted task (167-171, as the paper
#   prints it) the scheme prints two dashes of content (172-181), quoted as
#   examples, not a checklist. Part III is headed by its own descriptive line
#   (183-184).
# - Reading text: pp2-3 (title "Deținuții evadează în lectură" on p2, the text
#   to its source line on p3 y310; questions from p3 y353).
# No glyph problems.

CRIT_2019 = crit(156, (157, 158), (159, 160), 161)
NOTE_2019 = quote(L(154, 155), lead='The scheme prints')
ESSAY_2019 = Run('Scrieți un eseu pornind', 'cuvinte):')
SPECS[2019] = [
    R('I1a', [one(L(52, 54, after=' – '), PP())]),
    R('I1b', [one(L(55, 57, after=' – '), PP())]),
    R('I1c', [one(L(58, 61, after=' – '), PP())]),
    R('I1d', [one(L(62, 65, after=' – '), PP())]),
    R('I1e', [one(L(66, 68, after=' – '), PP())]),
    R('I2', [shown(L(76, 78)), shown(L(79, 81)), shown(L(82, 84))], whole=True,
      rownote=_head(70, after='2. ')),
    R('I3', [shown(L(89, 95)), shown(L(96, 98))], whole=True, rownote=_head(86, after='3. ')),
    R('I4', [shown(L(108, 113)), shown(L(114, 115))], whole=True, rownote=_head(100, 101, after='4. ')),
    R('I5', [shown(L(122, 129)), shown(L(130, 133))], whole=True, rownote=_head(117, 118, after='5. ')),
    R('I6', [shown(L(142, 144)), shown(L(145, 151))], whole=True, rownote=_head(139, after='6. ')),
    R('II1', [graded(L(154, 155), PARTP(), CRIT_2019)],
      rownote=examples(None, L(172, 175, after='- '), L(176, 181, after='- '))),
    R('III1', [graded(L(183, 184), PARTP(), CRIT_2019)], rownote=NOTE_2019,
      question=QP(4, ESSAY_2019, Run('a. Comentați următoarea', 'repede.” (Mircea'))),
    R('III2', [graded(L(183, 184), PARTP(), CRIT_2019)],
      rownote=both(NOTE_2019, quote(L(191, 194, after='b. '), lead='The scheme reprints this title as')),
      question=QP(4, ESSAY_2019, Run('b. Luarea unui an', 'sugerate.'))),
]
for _s in SPECS[2019]:
    _s.pages = (2, 3)


# ================================================================ 2020 HL ===
# Paper (rendered pp3-4): PARTEA I (its "(30/100)" set on a line below the
# head, p3 y490); Q1 is ONE question with no lettered parts ("Găsiţi cinci
# cuvinte sau expresii care definesc cuvântul „conflict“ în primele patru
# paragrafe ale textului.", "(5 puncte)" under it, no "5 x 1"): so the paper
# prints 9 asks, not 13, and the census's 9 are the paper's 9 (Q1-Q6, Part
# II, Part III titles 1 and 2). Q1-Q6 "(5 puncte)" each; PARTEA a II-a
# "(30/100)"; PARTEA a III-a "(40/100)", two titles joined by "SAU".
# Scheme (rendered pp3-7): each question under the scheme's own heading
# (which here restates the task), then model answer paragraphs, "(5 puncte)"
# under the lot, no split. Shapes, following this file's precedents (2011 Q2,
# 2012 Q5: one printed paragraph = one row at the printed price; 2016 Q6:
# several paragraphs = shown, priced as a whole, 10a):
# - Q1: one paragraph naming the definitions -> one row at 5. JUDGEMENT CALL:
#   the ask wants five words and the paragraph lists them with no per-item
#   price; if the lead prefers self-assessment here, flip to shown, whole=True.
# - Q2 (three paragraphs, one per motive), Q3 (two), Q4 (three), Q5 (two):
#   shown, priced as a whole. Paragraphs read on the render: each opens on a
#   new line after a short one (Q2, Q4) or after a gap (Q3, Q5).
# - Q4's first paragraph wraps "într-" / "adevăr" at its hyphen (lines 93-94):
#   joined with no space, as 2012's "responsabi-"/"litate".
# - Q6: one paragraph running over the p5/p6 break -> one row at 5, joined.
# - The scheme reprints only the title's question under Q5 ("Este conflictul
#   dintre generații o falsă problemă?"), not the paper's wording around it:
#   not a disagreement, not quoted.
# - Parts II (30) and III (40) on the four criteria the scheme prints under
#   "Indicații:" (p6): a) 30 %, b) 30 %, c) 30 %, d) 10 % (other criteria
#   from 2017-2019: "Înțelegerea cerințelor și coerența răspunsurilor",
#   "Eficiența limbajului", "Organizarea clară a argumentelor", grammar);
#   whole numbers of both totals (10b). Part II has no descriptive line of
#   its own: its head is the line introducing the criteria (142-143); under
#   the reprinted task the scheme prints one paragraph of model commentary
#   (152-161), quoted as examples, not a checklist. Part III is headed by its
#   own descriptive lines (167-169).
# - Part III: the paper asks for "un comentariu (de aproximativ 300 de
#   cuvinte)"; the scheme reprints the instruction as "Scrieți un eseu de
#   aproximativ 300 de cuvinte, ...": the paper wins, the scheme's words
#   quoted. The census attaches "SAU" to title 1: the question is cut from the
#   paper's own lines.
# - Reading text: pp2-3 (title "CONFLICTUL ÎNTRE GENERAŢII – O FALSĂ
#   PROBLEMĂ?" on p2, paragraphs 1-9 to "Adaptat din: Cotidianul" on p3).
# GLYPHS (reported, not repaired): the scheme sets the part numbers as Unicode
# Roman numerals in MS Gothic (rendered as Roman numerals, so printed, not a
# mis-mapped glyph): line 49 "Partea Ⅰ" U+2160; line 142 "Partea a Ⅱ-a și
# Partea a Ⅲ-a" U+2161, U+2162 (this line is the Part II head and is quoted on
# the Part III cards); line 148 U+2161; line 166 U+2162.

CRIT_2020 = crit(144, 145, 146, 147)
NOTE_2020 = quote(L(142, 143), lead='The scheme prints')
ESSAY_2020 = 'Scrieţi un comentariu'
ESSAYNOTE_2020 = quote(L(170, 171), lead='The scheme reprints the instruction as')
SPECS[2020] = [
    # Q1 asks for five words or expressions and the scheme answers in one
    # unpriced paragraph: shown, self-assessed on the printed 5 (a single row
    # could only be claimed whole or not at all).
    R('I1', [shown(L(52, 55))], whole=True, rownote=_head(51, after='1. ')),
    R('I2', [shown(L(59, 61)), shown(L(62, 65)), shown(L(66, 68))], whole=True,
      rownote=_head(57, 58, after='2. ')),
    R('I3', [shown(L(76, 85)), shown(L(86, 88))], whole=True, rownote=_head(74, 75, after='3. ')),
    R('I4', [shown(Join(L(91, 93), S(94), sep='')), shown(L(95, 98)), shown(L(99, 100))], whole=True,
      rownote=_head(90, after='4. ')),
    R('I5', [shown(L(109, 113)), shown(L(114, 121))], whole=True, rownote=_head(106, 107, after='5. ')),
    R('I6', [one(J(L(126, 132), L(137, 139)), PP())], rownote=_head(123, 124, after='6. ')),
    R('II1', [graded(L(142, 143), PARTP(), CRIT_2020)],
      rownote=examples(None, L(152, 161))),
    R('III1', [graded(L(167, 169), PARTP(), CRIT_2020)], rownote=both(NOTE_2020, ESSAYNOTE_2020),
      question=QP(4, ESSAY_2020, '1. Luptăm')),
    R('III2', [graded(L(167, 169), PARTP(), CRIT_2020)], rownote=both(NOTE_2020, ESSAYNOTE_2020),
      question=QP(4, ESSAY_2020, '2. Credeţi că')),
]
for _s in SPECS[2020]:
    _s.pages = (2, 3)


# ================================================================ 2026 HL ===
# Paper (rendered pp3-4): PARTEA I "(30/100)"; Q1 asks for five words and
# expressions "(redate îngroșat în text)" and prints "(5 × 1 punct)" beside e)
# (p3 y660): a price per expression, so Q1 is carded letter by letter (I1a-e,
# one row at 1 mark each, as 2010/2011/2019). Q2-Q6 "(5 puncte)" each; PARTEA
# a II-a "(30/100)"; PARTEA a III-a "(40/100)", titles 1. and 2. joined by
# "SAU". The census's 13 asks are the paper's 13 and it reads every price as
# printed.
# Scheme (rendered pp4-8): Q1 letters its answers a)-e), each after its bold
# expression and " – ", "(5 puncte)" once on the question's head line: each
# answer one row at the paper's "(5 × 1 punct)". Q2-Q6: the scheme reprints
# each question in bold with "(5 puncte)", then its own descriptive line,
# then model answer paragraphs (no indent; each opens on a new line after a
# short one), no split. Following this file's precedents (2012 Q5: one
# printed paragraph = one row at the printed price; 2016 Q6: several = shown,
# priced as a whole, 10a): Q2 (one paragraph) one row at 5; Q3 (two), Q4
# (three), Q5 (four), Q6 (four): shown, priced as a whole, under the heading.
# Q5's heading is followed by a second, plain reprint of the question (lines
# 124-126), not shown.
# Part II: NO criteria anywhere in this scheme (no "Notă", no percentages; p8
# is blank but for its page number). Under the reprinted task the scheme
# prints five dashes of content with no marks: shown under the paper's 30
# (10a; as Dutch 2015 Deel 2). Part III: the scheme reprints the instruction
# and the two titles and prints nothing under them (p7): R4 at the paper's 40.
# Judgement calls:
# - Q5's third paragraph prints an in-sentence dash at the start of a wrapped
#   line (line 139 "- nevoi ale personalului, ..."): the selector strips a
#   leading dash from every line, so the row reads "... raporturilor umane
#   nevoi ale personalului ..." without it. Flagged for the lead (as 2017 Q5).
# - Part II: the scheme reprints the task as "Discutați această temă" (paper
#   "Comentaţi această temă"): the paper wins, the scheme's words quoted.
# - Part III: the scheme reprints the instruction with "(a sau b)" where the
#   paper prints "(1. sau 2.)" (and itself numbers the titles 1. and 2.):
#   quoted in the R4 note (10f).
# - Reading text: pp2-3 (the article from p2 y168 to its source line on p3
#   y362; "CERINŢE" from p3 y463).
# No glyph problems.

SPECS[2026] = [
    R('I1a', [one(L(64, 66, after=' – '), PP())]),
    R('I1b', [one(L(67, 70, after=' – '), PP())]),
    R('I1c', [one(L(71, 73, after=' – '), PP())]),
    R('I1d', [one(L(74, 76, after=' – '), PP())]),
    R('I1e', [one(L(77, 78, after=' – '), PP())]),
    R('I2', [one(L(82, 88), PP())], rownote=_head(81)),
    R('I3', [shown(L(96, 99)), shown(L(100, 102))], whole=True, rownote=_head(95)),
    R('I4', [shown(S(108)), shown(L(109, 114)), shown(L(115, 117))], whole=True, rownote=_head(106, 107)),
    R('I5', [shown(L(131, 133)), shown(L(134, 137)), shown(J(S(138), SR(139), S(140))), shown(S(141))], whole=True,
      rownote=_head(122, 123)),
    R('I6', [shown(L(145, 147)), shown(L(148, 153)), shown(L(154, 160)), shown(S(161))], whole=True,
      rownote=_head(144)),
    R('II1', [shown(L(169, 170)), shown(L(171, 173)), shown(L(174, 175)), shown(L(176, 178)),
              shown(L(179, 180))], whole=True,
      rownote=quote(L(167, 168), lead='The scheme reprints the task as')),
    R('III1', [unprinted(lambda d: f'The scheme reprints the instruction as “{L(182, 183).text(d)}” and the two '
                                   f'titles, and prints nothing under them.')],
      question=QP(4, Run('Scrieți un eseu în care', 'de cuvinte):'), '1. Creierul uman')),
    R('III2', [unprinted(lambda d: f'The scheme reprints the instruction as “{L(182, 183).text(d)}” and the two '
                                   f'titles, and prints nothing under them.')],
      question=QP(4, Run('Scrieți un eseu în care', 'de cuvinte):'), Run('2. Când sclavul', '(Mihai Eminescu'))),
]
for _s in SPECS[2026]:
    _s.pages = (2, 3)


# ================================================================ 2021 HL ===
# Live: Part I (I1a-e, I2-I6, 10 cards). Drafted here: the two asks the old
# reader excluded, Part II's two essay titles (this sitting has no commentary;
# PARTEA a II-a is the essay, "(40/70)" on its head, p4 y497; the head prints a
# stray "`" after "II-a", read by the census as part of it).
# Scheme (rendered pp6-7): under "Notă:" (p6) the scheme names the four
# criteria for Part II and prints NO percentages and no marks beside them
# (rendered: the lines end "într-un mod clar", "structurat și logic", "ideile
# și opiniile", "de punctuație"). The exclusion's evidence quotes "— 30%" etc.
# for 2021: that text is not on this scheme (it is the 2023/2024 wording).
# Under Part II (p7) it prints its descriptive line, reprints the instruction
# and both titles, and prints nothing under them.
# Shape: graded() needs printed percentages, so it cannot apply. The scheme
# prints only what the candidate's own essay is judged on: the four criteria
# as shown rows, priced as a whole on the paper's 40 (questionTotal; 10b,
# "otherwise ... score on the printed total"), the descriptive line and the
# line introducing the criteria quoted in the note.
# Judgement calls:
# - Title b.: the scheme reprints "(Greta Thunberg)" where the paper prints
#   "- Greta Thunberg": punctuation only, not quoted.
# - No `pages`: in a two-part sitting Part II is the essay, so sl_lib attaches
#   no reading text to it (essay_part).
# No glyph problems (the scheme sets U+2010 HYPHEN in "II‐a", "într‐un";
# a real hyphen, normalised by the provenance check).


def _crit_note_2021(d):
    return (f'The scheme heads this part “{L(169, 170).text(d)}” and prints, with no marks or percentages '
            f'beside the criteria: “{S(157).text(d)}”')


CRIT_ROWS_2021 = [shown(S(158)), shown(L(159, 160)), shown(L(161, 162)), shown(S(163))]
ESSAY_2021 = 'Scrieți un eseu pornind'
SPECS[2021] = [
    R('II1', list(CRIT_ROWS_2021), whole=True, rownote=_crit_note_2021,
      question=QP(4, ESSAY_2021, Run('a. Plecând de la', 'Călătoria – o nevoie'))),
    R('II2', list(CRIT_ROWS_2021), whole=True, rownote=_crit_note_2021,
      question=QP(4, ESSAY_2021, 'b. Nu poți inventa')),
]


# ================================================================ 2022 HL ===
# Live: Part I (I1a-e, I2-I6, 10 cards). Drafted here: Part II's two essay
# titles (no commentary this sitting; PARTEA a II‐a "(40/70)", p4 y466).
# Scheme (pp6-7, as 2021): under "Notă:" the four criteria for Part II with NO
# percentages and no marks (lines 148-153; the exclusion's "— 30%" evidence is
# not on this scheme); under Part II its descriptive line (159-160), the
# instruction and both titles reprinted, nothing under them.
# Shape (as 2021): the four criteria as shown rows, priced as a whole on the
# paper's 40 (questionTotal; 10b), the descriptive line and the criteria's
# introducing line quoted in the note.
# Judgement calls:
# - The scheme reprints the instruction in other words ("una din cele două
#   idei exprimate mai jos: (aproximativ 300 de cuvinte):" for the paper's
#   "idei redate mai jos (aproximativ 300 de cuvinte):"): the paper wins, the
#   scheme's words quoted (10f).
# - Titles: the scheme spells "răzbi" (paper "rîzbi") and "adevărată ?"
#   (paper "adevarata", no question mark): spelling and punctuation only, not
#   quoted; the paper's words are the question.
# - No `pages`: Part II of a two-part sitting is the essay (no reading text).
# No glyph problems (U+2010 HYPHEN in "II‐a" on paper and scheme is a real
# hyphen).


def _crit_note_2022(d):
    return (f'The scheme heads this part “{L(159, 160).text(d)}” and prints, with no marks or percentages '
            f'beside the criteria: “{S(147).text(d)}” It reprints the instruction as “{L(161, 162).text(d)}”.')


CRIT_ROWS_2022 = [shown(S(148)), shown(L(149, 150)), shown(L(151, 152)), shown(S(153))]
ESSAY_2022 = Run('Scrieți un eseu în care', 'cuvinte):')
SPECS[2022] = [
    R('II1', list(CRIT_ROWS_2022), whole=True, rownote=_crit_note_2022,
      question=QP(4, ESSAY_2022, 'a. Mugurele vieții')),
    R('II2', list(CRIT_ROWS_2022), whole=True, rownote=_crit_note_2022,
      question=QP(4, ESSAY_2022, 'b. Cum se construiește')),
]


# ================================================================ 2023 HL ===
# Live: Part I (I1a-e, I2-I6, 10 cards). Drafted here: Part II (commentary)
# and Part III's two titles.
# Paper (p4): PARTEA a II-a with its "(30/100)" set on a line BELOW the head
# (y429 under y414), so the census reads no total for Part II and PARTP()
# fails: Part II is priced from that printed cell, PaperP(4, '(30/100)').
# PARTEA a III-a "(40/100)" on its head's line (PARTP). Titles 1 and 2 joined
# by "SAU" (the census attaches "SAU" to title 1: questions cut from the
# paper's own lines).
# Scheme (rendered pp6-7): under "Notă:" the four criteria for Parts II and
# III, 30/30/30/10 % (whole numbers of 30 and 40: 10b). Neither part prints a
# descriptive line of its own, so both are headed by the line introducing the
# criteria (161-162). Under Part II's reprinted task the scheme prints its own
# heading "Nota: Raspunsul care urmeaza este doar un exemplu sau o sugestie."
# and three paragraphs of model commentary: quoted under that heading, as
# examples, not a checklist (10a). Under Part III it reprints the instruction
# and the two titles and nothing else.
# Judgement calls:
# - Part III: the scheme reprints the instruction with "(a sau b)" where the
#   paper prints "(1 sau 2)" (and itself numbers the titles 1. and 2.):
#   quoted (10f).
# - Reading text: pp2-3 (title "Adolescenții față cu dezinformarea" p2 y131,
#   two adapted texts to the source line on p3 y504; ÎNTREBĂRI p3 y537). The
#   live Part I cards of 2022-2025 carry sourceMaterial pages [3] only (the
#   census's reading); flagged for the lead, not changed here.
# No glyph problems (U+2010 HYPHEN in the scheme's "II‐a" is a real hyphen).

CRIT_2023 = crit(163, (164, 165), (166, 167), 168)
P2_2023 = PaperP(4, '(30/100)')
ESSAY_2023 = Run('Scrieți un eseu în care', '300 de cuvinte):')
NOTE3_2023 = quote(L(187, 188), lead='The scheme reprints the instruction as')
SPECS[2023] = [
    R('II1', [graded(L(161, 162), P2_2023, CRIT_2023)], total=P2_2023,
      rownote=examples(S(177), L(178, 179), L(180, 182), L(183, 185)), pages=(2, 3)),
    R('III1', [graded(L(161, 162), PARTP(), CRIT_2023)], rownote=NOTE3_2023,
      question=QP(4, ESSAY_2023, Run('1. Citește.', '(Mihai Eminescu)'))),
    R('III2', [graded(L(161, 162), PARTP(), CRIT_2023)], rownote=NOTE3_2023,
      question=QP(4, ESSAY_2023, '2. Nu e bun')),
]


# ================================================================ 2024 HL ===
# Live: Part I (I1a-e, I2-I6, 10 cards). Drafted here: Part II (commentary)
# and Part III's two titles.
# Paper (p4): PARTEA a II-a "(30/100)", PARTEA a III-a "(40/100)", each on its
# head's line (PARTP); titles a. and b. joined by "SAU".
# Scheme (rendered pp7-8): under "Notă:" the four criteria for Parts II and
# III, 30/30/30/10 % (whole numbers of 30 and 40: 10b). Neither part prints a
# descriptive line of its own, so both are headed by the line introducing the
# criteria (171-172, as 2023). Under Part II's reprinted task the scheme
# prints five paragraphs of model commentary (no heading; each opens on a new
# line after a short one, rendered p7): quoted as examples, not a checklist
# (10a). Under Part III it reprints the instruction and the two titles as the
# paper prints them, and nothing else.
# Judgement calls:
# - Part II: the scheme reprints the last line of the task with a word the
#   paper does not print, "(aproximativ 100‐150 de cuvinte)" for the paper's
#   "(100-150 de cuvinte)": the paper wins, the scheme's line quoted (10f).
# - Reading text: pp2-3 (two texts: Adina Popescu's to its source line on p2
#   y728, Alina Pavelescu's on p3 to y195; ÎNTREBĂRI p3 y280).
# No glyph problems (U+2010 HYPHEN in the scheme is a real hyphen).

CRIT_2024 = crit(173, (174, 175), (176, 177), 178)
ESSAY_2024 = Run('Scrieți un eseu în care', '(aproximativ 300')
SPECS[2024] = [
    R('II1', [graded(L(171, 172), PARTP(), CRIT_2024)],
      rownote=both(quote(L(183, 184), lead='The scheme reprints the last line of the task as'),
                   examples(None, L(185, 187), L(188, 189), L(190, 191), L(192, 193), L(194, 198))),
      pages=(2, 3)),
    R('III1', [graded(L(171, 172), PARTP(), CRIT_2024)],
      question=QP(4, ESSAY_2024, Run('a. Nu supraviețuiesc', 'adaptabile.'))),
    R('III2', [graded(L(171, 172), PARTP(), CRIT_2024)],
      question=QP(4, ESSAY_2024, Run('b. Omul este', '(citat din romanul'))),
]


# ================================================================ 2025 HL ===
# Live: Part I (I1a-e, I2-I6, 10 cards). Drafted here: Part II (commentary)
# and Part III's two titles.
# Paper (p4): PARTEA a II-a "(30/100)", PARTEA a III-a "(40/100)" (PARTP);
# titles 1. and 2. joined by "SAU" (the census attaches "SAU" to title 1:
# questions cut from the paper's own lines).
# Scheme (rendered p7): NO criteria anywhere (no "Notă", no percentages; heads
# "PARTEA a II-a 30 de puncte", "PARTEA a III-a 40 de puncte"). Part II: the
# task reprinted in other words, then the paper's three pieces of advice each
# as a sub-heading with one or two bullets of content under it, no marks:
# shown under the paper's 30 (10a; as 2026 Part II, Dutch 2015 Deel 2), each
# bullet led by its advice ("For “„Trăiți momentul!“”", as 2010 Q4's leads).
# Part III: the instruction and the two titles reprinted as the paper prints
# them, nothing under them: R4 at the paper's 40.
# Judgement calls:
# - Part II: the scheme reprints the task as "... regăsim trei sfaturi de
#   ademenit fericirea. Alegeți unul dintre aceste sfaturi și discutați
#   importanța lui ..." (without the three quoted pieces of advice the paper
#   prints, "discutați" for the paper's "comentați"): the paper wins, the
#   scheme's words quoted (10f).
# - Title 1: the scheme prints "ceea ce faci . (Mahatma Gandhi)" (a space
#   before the stop): punctuation only, not quoted.
# - Reading text: pp2-3 (p2 y153 to the source line on p3; CERINȚE p3 y502).
# No glyph problems.

SPECS[2025] = [
    R('II1', [shown(L(176, 178), lead=S(175)), shown(L(179, 181), lead=S(175)),
              shown(L(183, 186), lead=S(182)), shown(L(187, 188), lead=S(182)),
              shown(L(190, 194), lead=S(189))], whole=True,
      rownote=quote(L(172, 174), lead='The scheme reprints the task as'), pages=(2, 3)),
    R('III1', [unprinted('The scheme reprints the instruction and the two titles and prints nothing under them.')],
      question=QP(4, Run('Scrieți un eseu în care', '(minimum 300'), Run('1. Fericirea apare', 'ceea ce faci.'))),
    R('III2', [unprinted('The scheme reprints the instruction and the two titles and prints nothing under them.')],
      question=QP(4, Run('Scrieți un eseu în care', '(minimum 300'), '2. Înțelepciunea')),
]


for _s in SPECS[2010]:
    _s.pages = (2, 3)


def specs(year):
    return SPECS.get(year, [])
