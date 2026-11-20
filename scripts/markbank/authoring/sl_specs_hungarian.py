#!/usr/bin/env python3
"""Reviewed specs for the Hungarian classic examination (small-languages lane).

One entry per printed ask with no live card; see sl_lib.py for the selector
language. Line numbers are lines of examiner-reports/hungarian/schemes/<year>-hl.md.
Drafted by Opus helpers on the Bulgarian, Romanian, Dutch and Maltese models, integrated
and gated by the lane lead.
"""
from sl_lib import (R, S, SR, J, L, PL, PC, QP, QL, Run, pre, prerun, PP, SP, PY, RX, PaperP, PARTP, REM,  # noqa: F401
                    one, shown, graded, crit, examples, quote, unprinted, part, NoScheme, Unpriced)
from pl_listen_lib import Join  # noqa: F401

SPECS = {}


def both(*notes):
    """Several printed notes on one row, in order."""
    return lambda doc: ' '.join(n(doc) for n in notes)


# ================================================================ 2010 HL ===
# Carded by the lead (20 Nov). Live: Part I. Paper p4: II. RÉSZ "(30 pont / 100
# pont)" (y70), the commentary on one sentence; III. RÉSZ "(40 pont / 100 pont)"
# (y217), two titles ("1. lehetőség" / "vagy" / "2. lehetőség"). Scheme p3-4:
# "A II. és III. részben elérhető pontok az alábbi szempontok szerint oszlanak
# meg:" (103) and the four criteria at 30/30/30/10 % (104-110): both parts
# graded (10b). Part II's head is its requirement line (77), its "Lehetséges
# irányok:" (78) quoted as examples; Part III's head is its own line (94), each
# title's "Egyéni válasz körülbelül 300 szóban." left to the head. The labels
# "1. lehetőség" / "2. lehetőség" are not part of the titles.
CRIT_2010 = crit((104, 105), (106, 107), (108, 109), 110)
LEAD_2010 = quote(S(103), lead='The scheme prints')
SPECS[2010] = [
    R('II1', [graded(S(77), PARTP(), CRIT_2010)],
      rownote=both(LEAD_2010, examples(S(78), L(79, 80, after='• '), L(81, 82, after='• '), L(83, 84, after='• '),
                                       S(85, after='• '), S(86, after='• '), S(87, after='• '))),
      question=QP(4, 'A szöveg alapján kommentáld', 'Pénzt kell költeni'), pages=(2, 3)),
    R('III1', [graded(S(94), PARTP(), CRIT_2010)], rownote=LEAD_2010,
      question=QP(4, 'A két téma közül', 'Reklámok: hiszünk')),
    R('III2', [graded(S(94), PARTP(), CRIT_2010)], rownote=LEAD_2010,
      question=QP(4, 'A két téma közül', Run('„Senki sem', '(J. Donne'))),
]


def specs(year):
    return SPECS.get(year, [])


# ====================================================================== 2011
# ================================================================ 2011 HL ===
# Drafted (small-languages lane, 20 Nov): the four open asks of this sitting,
# I1a, II1, III1, III2. Live: I1b-e, I2-I6 (9 cards); not touched here (see the
# live audit, hungarian-live-faults-2010-2018.json).
# Paper (rendered pp2-4): rule p2 y78 ("Válaszolj érthetően magyarul az I., II.
# és III. részben feltett kérdésekre!"); reading text "Nemzetközi tizenegy -
# Foci és identitás" p2 y107 to the byline "Vajna Tamás, Weyer Béla, HVG 2010.,
# adaptáció" p3 y327 (paragraphs 1-4 on p2, 5-6 on p3); "I. RÉSZ (30 pont / 100
# pont)" p3 y373; Q1 a)-e) each "(1 pont)" at the right margin; Q2-Q6 "(5
# pont)"; "II. RÉSZ (30 pont / 100 pont)" p4 y79; "III. RÉSZ (40 pont / 100
# pont)" p4 y247, two titles "1. lehetőség" / "vagy" / "2. lehetőség".
# PRICES:
# - I1a: the census reads no price (tariff None): the text layer welds the
#   question number and a)'s margin price into one line "1. (1 pont)" (p3 x74
#   y429), with "a, Magyarázd meg ..." a separate cell at x108 on the same y.
#   Rendered p3: "(1 pont)" sits at the right margin on a)'s own line, as for
#   b)-e). Priced from that printed line (PaperP); the scheme prints the same
#   "(1 pont)" on its reprint of a) (line 19). Not a remainder, not 10i.
# - II1: the part head's "(30 pont / 100 pont)" (PARTP); III1/III2: "(40 pont /
#   100 pont)" (PARTP).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5):
# - Q1 a) (19 reprints the expression with "(1 pont)"): one italic gloss,
#   lines 20-22, "A 4. bekezdésben található szó saját szavaiddal kifejezve: a
#   „morális” szó azt jelenti, hogy erkölcsös, erkölcsi. Azon normák alapján
#   élő, amelyeket társadalmi szinten helyesnek tartunk." One stated answer: one
#   row at the paper's "(1 pont)", lead kept as the live b)-e) keep theirs.
# - Criteria (p4, under Q6, before Part II): "A II. és III. részben elérhető
#   pontok az alábbi szempontok szerint oszlanak meg:" (72) and the four
#   criteria at 30/30/30/10 % (73-78), stated for Parts II and III: both graded
#   (10b), 9/9/9/3 of 30 and 12/12/12/4 of 40, as the lead's 2010.
# - Part II (79-83 reprint the part head and the task): the requirement line
#   "A minimum 100 szóban tisztán, érthetően kifejtett saját vélemény." (88) is
#   the graded row's head; "Lehetséges irányok:" (89) and the list under it
#   (rendered p5: italic, two bold-italic sub-heads "a) Németország a pozitív
#   példa:" / "b) Franciaország a negatív példa:" with five and four bullets,
#   and "c) Saját szavakkal kifejtett vélemény") quoted as examples, every
#   printed line in order, sub-heads included.
# - Part III (114-124): "Tisztán, érthetően és világosan megírt esszé." (116),
#   the graded rows' head; each title reprinted with "Egyéni válasz minimum 300
#   szóban." (119, 124), left to the head as in 2010.
# SHAPES: I1a one(); II1, III1, III2 graded(head, PARTP(), CRIT_2011).
# JUDGEMENT CALLS:
# - Reading text pp2-3 (rendered); pages=(2, 3) on I1a and II1. The live I1b-e
#   and I2-I6 carry [3]: flagged in the live audit.
# - II1's question is cut from the paper's own lines (the census glues the
#   part head's "(30 pont / 100 pont) Kommentár" in front); the instruction line
#   kept, as the lead's 2010.
# - III1/III2: the instruction line plus the title, the labels "1. lehetőség"
#   / "2. lehetőség" left out, as the lead's 2010; title 2 keeps its printed
#   attribution line "(Abraham Lincoln, ...)".
# GLYPHS: none in the lines used (á é í ó ö ő ú ü ű read clean, render checked).
CRIT_2011 = crit(73, (74, 75), (76, 77), 78)
LEAD_2011 = quote(S(72), lead='The scheme prints')
SPECS[2011] = [
    R('I1a', [one(L(20, 22), PaperP(3, '1. (1 pont)'))], total=PaperP(3, '1. (1 pont)'), pages=(2, 3)),
    R('II1', [graded(S(88), PARTP(), CRIT_2011)],
      rownote=both(LEAD_2011, examples(S(89), S(90), L(91, 93), L(94, 97), L(98, 100), L(101, 102),
                                       L(103, 104), S(105), L(106, 107), S(108), L(109, 110), L(111, 112),
                                       S(113))),
      question=QP(4, 'A szöveg alapján kommentáld', Run('Kommentáld, hogyan', 'véleményedet!')), pages=(2, 3)),
    R('III1', [graded(S(116), PARTP(), CRIT_2011)], rownote=LEAD_2011,
      question=QP(4, 'A két téma közül', 'A diverzitás')),
    R('III2', [graded(S(116), PARTP(), CRIT_2011)], rownote=LEAD_2011,
      question=QP(4, 'A két téma közül', Run('„A legtöbben', '(Abraham Lincoln'))),
]


# ====================================================================== 2012
# ================================================================ 2012 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (see the live
# audit, hungarian-live-faults-2010-2018.json).
# Paper (rendered pp2-4): rule p2 y78-94 ("Olvassa el a következő szöveget, és
# válaszoljon érthetően magyarul az I., II. és III. részben feltett
# kérdésekre!"), "(100 pont)" p2 y120; reading text "Köszbizalom" p2 y149 to
# the byline "Balázs Zsuzsanna, HVG, 2011/36. szám, adaptáció" p3 y309
# (paragraphs 1-5 on p2, the end of 5 and 6 on p3); "I. RÉSZ (30 pont / 100
# pont)" p3 y346; "II. RÉSZ (30 pont / 100 pont)" p4 y78; "III. RÉSZ (40 pont /
# 100 pont)" p4 y253, two titles printed "1." / "vagy" / "2." (no "lehetőség"
# labels on the paper; the scheme adds them, 128/132).
# PRICES: II1 the part head's "(30 pont / 100 pont)" (PARTP); III1/III2 "(40
# pont / 100 pont)" (PARTP). Nothing else is priced for these parts.
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5):
# - Criteria (p4, under Q6): "A II. és III. részben elérhető pontok az alábbi
#   szempontok" / "szerint oszlanak meg:" (89-90) and the four criteria at
#   30/30/30/10 % (91-97), for Parts II and III: both graded (10b).
# - Part II (101-105 reprint the head and the task): requirement line "A
#   minimum 100 szóban tisztán, érthetően kifejtett saját vélemény." (106), the
#   graded head; "Lehetséges irányok:" (107) and four dashed points (108-124),
#   quoted as examples.
# - Part III (125-134): "Tisztán, érthetően és világosan megírt esszé." (127),
#   the head; each title with "Egyéni válasz minimum 300 szóban." left to it.
# SHAPES: II1, III1, III2 graded(head, PARTP(), CRIT_2012).
# JUDGEMENT CALLS:
# - Reading text pp2-3 (rendered); pages=(2, 3) on II1. The live Part I cards
#   carry [3]: flagged in the live audit.
# - II1's question: the instruction line and the task cut from the paper's own
#   lines (the census glues "(30 pont / 100 pont) Kommentár" in front). The
#   paper prints the quotation opening „ [A] with a space after the mark: lifted
#   as printed.
# - III1/III2: the instruction line plus the title, its printed "1." / "2."
#   taken off as a marker (ruling B cites them Section III Q1/Q2).
# GLYPHS: none in the lines used.
CRIT_2012 = crit((91, 92), (93, 94), (95, 96), 97)
LEAD_2012 = quote(L(89, 90), lead='The scheme prints')
SPECS[2012] = [
    R('II1', [graded(S(106), PARTP(), CRIT_2012)],
      rownote=both(LEAD_2012, examples(S(107), L(108, 112), L(113, 115), L(116, 119), L(120, 124))),
      question=QP(4, 'A szöveg alapján kommentálja', Run('„ [A] viszonosság', '100 szóban!')), pages=(2, 3)),
    R('III1', [graded(S(127), PARTP(), CRIT_2012)], rownote=LEAD_2012,
      question=QP(4, 'A két téma közül', '1. Jobb tisztességben')),
    R('III2', [graded(S(127), PARTP(), CRIT_2012)], rownote=LEAD_2012,
      question=QP(4, 'A két téma közül', '2. Modern társadalmunkban')),
]


# ====================================================================== 2013
# ================================================================ 2013 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (see the live
# audit, hungarian-live-faults-2010-2018.json).
# Paper (rendered pp2-4): rule p2 y64-78; reading text "Kikapcs - Tévét nem
# nézők. ..." p2 y107 to the byline "Dobszay János, HVG, 2012, adaptáció" p3
# y368 (paragraphs 1-6 on p2, the end of 6 and 7-8 on p3); "I. RÉSZ (30 pont /
# 100 pont)" p3 y478 (Q1 on p3, Q2-Q6 on p4); "II. RÉSZ (30 pont / 100 pont)"
# p4 y382; "III. RÉSZ (40 pont / 100 pont)" p4 y564, titles "1. lehetőség" /
# "vagy" / "2. lehetőség".
# PRICES: II1 "(30 pont / 100 pont)", III1/III2 "(40 pont / 100 pont)", each
# on its part head (PARTP). Nothing else is priced for these parts.
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5):
# - Criteria (p4, under Q6; set in a grey box): "A II. és III. részben elérhető
#   pontok az alábbi szempontok" / "szerint oszlanak meg:" (103-104) and the
#   four criteria at 30/30/30/10 % (105-111), for Parts II and III: graded.
# - Part II (112-117 reprint the head and the task): requirement line "A
#   minimum 100 szóban tisztán, érthetően kifejtett saját vélemény." (118), the
#   graded head; "Lehetséges irányok:" (119, foot of p4) and six dashed points
#   on p5 (124-140), quoted as examples. Line 136 ends "(5. bk)l": the stray l
#   is printed (rendered p5), lifted as printed.
# - Part III (141-150): "Tisztán, érthetően és világosan megírt esszé." (143),
#   the head.
# SHAPES: II1, III1, III2 graded(head, PARTP(), CRIT_2013).
# JUDGEMENT CALLS:
# - Reading text pp2-3 (rendered); pages=(2, 3) on II1. Live Part I cards carry
#   [3]: flagged in the live audit.
# - II1's question: the instruction line and the task from the paper's lines
#   (the scheme's reprint opens with an extra „ at 115; the paper's does not).
# - III1/III2: instruction line plus title, labels left out (2010 model).
# GLYPHS: none in the lines used.
CRIT_2013 = crit((105, 106), (107, 108), (109, 110), 111)
LEAD_2013 = quote(L(103, 104), lead='The scheme prints')
SPECS[2013] = [
    R('II1', [graded(S(118), PARTP(), CRIT_2013)],
      rownote=both(LEAD_2013, examples(S(119), L(124, 127), L(128, 132), L(133, 135), S(136), L(137, 138),
                                       L(139, 140))),
      question=QP(4, 'A szöveg alapján kommentálja', Run('A cikk alapján magyarázza', 'televízió”!')),
      pages=(2, 3)),
    R('III1', [graded(S(143), PARTP(), CRIT_2013)], rownote=LEAD_2013,
      question=QP(4, 'A két téma közül', '„[A] tévé nemcsak')),
    R('III2', [graded(S(143), PARTP(), CRIT_2013)], rownote=LEAD_2013,
      question=QP(4, 'A két téma közül', 'Álmaid követése')),
]


# ====================================================================== 2014
# ================================================================ 2014 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (see the live
# audit, hungarian-live-faults-2010-2018.json).
# Paper (rendered pp2-4): rule p2 y64-78; reading text "Szomszédságpolitika -
# Magyarok és a bevándorlás" p2 y105 to the byline "Dobszay János, HVG, 2013,
# adaptáció" p3 y357 (paragraphs 1-6 on p2, the end of 6 and 7 on p3); "I.
# RÉSZ (30 pont / 100 pont)" p3 y424 (Q1-Q4 on p3, Q5-Q6 on p4); "II. RÉSZ (30
# pont / 100 pont)" p4 y286; "III. RÉSZ (40 pont / 100 pont)" p4 y495, titles
# "1. lehetőség" / "vagy" / "2. lehetőség".
# PRICES: II1 "(30 pont / 100 pont)", III1/III2 "(40 pont / 100 pont)" on the
# part heads (PARTP). Nothing else is priced for these parts.
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5):
# - Criteria (p4, under Q6, grey box): "A II. és III. részben elérhető pontok
#   az alábbi szempontok szerint" / "oszlanak meg:" (110-111) and the four
#   criteria at 30/30/30/10 % (112-117), for Parts II and III: graded.
# - Part II (118-122 reprint the head and the task): requirement line (123),
#   the graded head; "Lehetséges irányok:" (124, foot of p4), then on p5 an
#   italic lead paragraph "Azért mondhatjuk, ... Budapestre, mert" (129-134)
#   and five dashed points (135-151), all quoted as examples, in order.
# - Part III (152-162): "Tisztán, érthetően és világosan megírt esszé." (154).
# SHAPES: II1, III1, III2 graded(head, PARTP(), CRIT_2014).
# JUDGEMENT CALLS:
# - Reading text pp2-3 (rendered); pages=(2, 3) on II1. Live Part I cards carry
#   [3]: flagged in the live audit.
# - II1's question: the paper's instruction (it ends "!" on the paper, ":" in
#   2011-2013) and the task, from the paper's own lines.
# - III2 keeps its printed attribution "- Ralph Waldo Emerson" (same line).
# GLYPHS: none in the lines used.
CRIT_2014 = crit(112, (113, 114), (115, 116), 117)
LEAD_2014 = quote(L(110, 111), lead='The scheme prints')
SPECS[2014] = [
    R('II1', [graded(S(123), PARTP(), CRIT_2014)],
      rownote=both(LEAD_2014, examples(S(124), L(129, 134), L(135, 137), L(138, 141), L(142, 143),
                                       L(144, 148), L(149, 151))),
      question=QP(4, 'A szöveg alapján kommentálja', Run('A cikk alapján magyarázza', 'valósult meg Szent')),
      pages=(2, 3)),
    R('III1', [graded(S(154), PARTP(), CRIT_2014)], rownote=LEAD_2014,
      question=QP(4, 'A két téma közül', 'A sokszínűség előnyei')),
    R('III2', [graded(S(154), PARTP(), CRIT_2014)], rownote=LEAD_2014,
      question=QP(4, 'A két téma közül', Run('„Beutazhatjuk', 'hordoznunk, különben'))),
]


# ====================================================================== 2015
# ================================================================ 2015 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (see the live
# audit, hungarian-live-faults-2010-2018.json).
# (Was HOLD, resolved by the lead: the .md repaired from glyph ids by sl_glyphs.py
# hungarian, 280 -> ő, 294 -> ű, 293 -> Ű, derived by vote; line numbers unchanged.)
# The 2015 scheme's text layer is mangled in the bold/italic
# Times New Roman runs (TimesNewRoman,Bold / TimesNewRoman,Italic): it reads
# U+0118 (Ę) where the render shows ő (U+0151), U+0126 (Ħ) where it shows ű
# (U+0171), U+0125 (ĥ) where it shows Ű (U+0170) (rendered scheme p3 at 130
# dpi: "MAGYAR NYELVŰ MEGOLDÓKULCS" read "NYELVĥ" at 49; "következő" read
# "következĘ" at 51; p4/p5 "megfelelĘ", "egyszerĦek"). Every line these cards
# lift that carries ő/ű comes out mangled: the criteria lead 99 ("elérhetĘ"),
# criterion 2 (103, "megfelelĘ"), criterion 3 (105-106, "megfelelĘen",
# "összefüggĘen"), the Part II head 112 and the Part III head 141
# ("érthetĘen"), and examples 118-136 ("döntĘ", "szépségérĘl", "szereplĘket",
# "egyszerĦek", "beszĦkítenek", "elsĘsorban", "köszönhetĘen", "elĘtt"). Not
# hand-mapped (brief): needs a scheme glyph map derived from glyph ids (as
# glyphmap-polish-2015-hl.json) applied to the .md before these cards build.
# The specs below are otherwise final. The live 2015 cards I1a, I1b, I3, I5, I6
# already carry U+0118 (flagged in the live audit).
# Paper (rendered pp2-4; its text layer is clean): rule p2 y79-93; reading text
# "A bőség zavaros - ..." p2 y121 to the byline "Illényi Balázs, HVG, 2014,
# adaptáció" p3 y453 (paragraphs 1-4 on p2, 5-7 on p3); "I. RÉSZ (30 pont / 100
# pont)" p3 y482; "II. RÉSZ (30 pont / 100 pont)" p4 y260; "III. RÉSZ (40 pont
# / 100 pont)" p4 y454, titles "1. lehetőség" / "vagy" / "2. lehetőség".
# PRICES: II1 "(30 pont / 100 pont)", III1/III2 "(40 pont / 100 pont)" on the
# part heads (PARTP). Nothing else is priced for these parts.
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5):
# - Criteria (p4, under Q6): "A II. és III. részben elérhetĘ pontok az alábbi
#   szempontok" / "szerint oszlanak meg:" (99-100) and the four criteria at
#   30/30/30/10 % (101-107), for Parts II and III: graded.
# - Part II (108-111 reprint the head and the task): requirement line (112),
#   the graded head; "Lehetséges irányok:" (113), a lead sentence "Azért
#   mondhatjuk, hogy „ a képek elfogyasztják a valóságot”, mert:" (114) and
#   five dashed points (115-138), quoted as examples in order.
# - Part III (139-149): "Tisztán, érthetĘen és világosan megírt esszé." (141).
# SHAPES: II1, III1, III2 graded(head, PARTP(), CRIT_2015).
# JUDGEMENT CALLS:
# - Reading text pp2-3 (rendered); pages=(2, 3) on II1. Live Part I cards carry
#   [3]: flagged in the live audit.
# - III1: the paper opens the title with an English-style “ (U+201C), the
#   scheme reprints it with no quotation marks (143-144): the paper's printing
#   is the question (10f).
CRIT_2015 = crit((101, 102), (103, 104), (105, 106), 107)
LEAD_2015 = quote(L(99, 100), lead='The scheme prints')
SPECS[2015] = [
    R('II1', [graded(S(112), PARTP(), CRIT_2015)],
      rownote=both(LEAD_2015, examples(S(113), S(114), L(115, 117), L(118, 122), L(127, 132), L(133, 136),
                                       L(137, 138))),
      question=QP(4, 'A szöveg alapján kommentálja', '„ [A] képek'), pages=(2, 3)),
    R('III1', [graded(S(141), PARTP(), CRIT_2015)], rownote=LEAD_2015,
      question=QP(4, 'A két téma közül', Run('“Minden, amit', 'vagyok tőle.”'))),
    R('III2', [graded(S(141), PARTP(), CRIT_2015)], rownote=LEAD_2015,
      question=QP(4, 'A két téma közül', 'Az a leggazdagabb')),
]


# ====================================================================== 2016
# ================================================================ 2016 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (see the live
# audit, hungarian-live-faults-2010-2018.json).
# Paper (rendered pp2-4): rule p2 y79-93; reading text "Nem egyedülálló
# helyzetek - ..." p2 y121 to the byline "Lindner András: HVG, 2015,
# adaptáció" p3 y480 (paragraphs 1-3 on p2, the end of 3 and 4-5 on p3; the
# footnote "1 Paradoxon: ..." p3 y764 belongs to paragraph 4); "I. RÉSZ (30
# pont / 100 pont)" p3 y557 (Q1 on p3, Q2-Q6 on p4); "II. RÉSZ (30 pont / 100
# pont)" p4 y343; "III. RÉSZ (40 pont / 100 pont)" p4 y525, titles "1.
# lehetőség" / "vagy" / "2. lehetőség".
# PRICES: II1 "(30 pont / 100 pont)", III1/III2 "(40 pont / 100 pont)" on the
# part heads (PARTP). Nothing else is priced for these parts.
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5):
# - Criteria (p4, under Q6, grey box): "A II. és III. részben elérhető pontok
#   az alábbi szempontok" / "szerint oszlanak meg:" (105-106) and the four
#   criteria at 30/30/30/10 % (107-113), for Parts II and III: graded. (The
#   exclusions file calls these "percentages of qualities ... no answer": the
#   criteria are exactly what 10b grades on.)
# - Part II (114-119 reprint the head and the task): requirement line "A
#   minimum 100, maximum 150 szóban tisztán, érthetően kifejtett saját
#   vélemény." (120), the graded head; "Lehetséges irányok:" (121), a lead "A
#   szerző arra utal az alábbi mondatával, hogy:" (122) and six dashed points
#   on p5 (127-147), quoted as examples in order.
# - Part III (148-160): "Tisztán, érthetően és világosan megírt esszé." (150).
# SHAPES: II1, III1, III2 graded(head, PARTP(), CRIT_2016).
# JUDGEMENT CALLS:
# - Reading text pp2-3 (rendered); pages=(2, 3) on II1. Live Part I cards carry
#   [3]: flagged in the live audit.
# - II1's question: the paper's instruction (two lines, its word limit "(min.
#   100, max. 150 szóban)" inside it, no colon; the scheme's reprint adds one)
#   and the quoted sentence, from the paper's own lines.
# - III2 keeps its printed attribution line "Fintan O'Toole, The Irish Times,
#   2016. február. 22.02.2016." as the paper prints it (rendered p4; the scheme
#   prints "2016. február. 22." only).
# GLYPHS: none in the lines used.
CRIT_2016 = crit((107, 108), (109, 110), (111, 112), 113)
LEAD_2016 = quote(L(105, 106), lead='The scheme prints')
SPECS[2016] = [
    R('II1', [graded(S(120), PARTP(), CRIT_2016)],
      rownote=both(LEAD_2016, examples(S(121), S(122), L(127, 129), L(130, 131), L(132, 134), L(135, 139),
                                       L(140, 144), L(145, 147))),
      question=QP(4, Run('A szöveg alapján kommentálja', 'véve, hogy'), Run('„Az egyik', 'nincs igazi')),
      pages=(2, 3)),
    R('III1', [graded(S(150), PARTP(), CRIT_2016)], rownote=LEAD_2016,
      question=QP(4, 'A két téma közül', Run('“[H]a egyszer', 'soha.”'))),
    R('III2', [graded(S(150), PARTP(), CRIT_2016)], rownote=LEAD_2016,
      question=QP(4, 'A két téma közül', Run('A világ elég rossz', 'Fintan O'))),
]


# ====================================================================== 2017
# ================================================================ 2017 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (see the live
# audit, hungarian-live-faults-2010-2018.json).
# Paper (rendered pp2-4): rule p2 y65-80, "Az elérhető maximális pontszám 100
# pont" p2 y109; reading text "Perszonalizált világ" p2 y138 to the byline
# "Szauer Tamás: HVG, 2016, adaptáció" p3 y433 (paragraphs 1-4 on p2 with the
# footnote "1 A beépített okos szenzorok ..." p2 y767, 5-7 on p3); "I. RÉSZ (30
# pont / 100 pont)" p3 y533 (Q1 on p3, Q2-Q6 on p4); "II. RÉSZ (30 pont / 100
# pont)" p4 y343 with "Kommentár (min. 100, max. 150 szóban)" y373; "III. RÉSZ
# (40 pont / 100 pont)" p4 y519, titles "1. lehetőség" / "vagy" / "2.
# lehetőség".
# PRICES: II1 "(30 pont / 100 pont)", III1/III2 "(40 pont / 100 pont)" on the
# part heads (PARTP). Nothing else is priced for these parts.
# WHAT THE SCHEME PRINTS (rendered scheme pp4-6):
# - Criteria (p4, under Q6): "A II. és III. részben elérhető pontok az alábbi
#   szempontok" / "szerint oszlanak meg:" (112-113) and the four criteria at
#   30/30/30/10 % (114-120), for Parts II and III: graded.
# - Part II (p5; 125-129 reprint the head and the task): requirement line "A
#   minimum 100, maximum 150 szóban tisztán, érthetően kifejtett saját
#   vélemény." (130), the graded head; "Lehetséges irányok:" (131), a lead "A
#   szerző azért állítja, ... mert:" (132) and eight dashed points (133-157),
#   quoted as examples in order.
# - Part III (p6, 162-174): "Tisztán, érthetően és világosan megírt esszé."
#   (164).
# SHAPES: II1, III1, III2 graded(head, PARTP(), CRIT_2017).
# JUDGEMENT CALLS:
# - Reading text pp2-3 (rendered); pages=(2, 3) on II1. Live Part I cards carry
#   [3]: flagged in the live audit.
# - II1's question: the paper prints the word limit only on the task's own
#   head, "Kommentár (min. 100, max. 150 szóban)" (p4 y373), then the task
#   (y402-431). Both lifted (head line + task) so the card keeps the printed
#   word limit; the lead's 2010 lifts the instruction line that carries it.
# - III2: the title's two printed sentences, the instruction "Fejtse ki ..."
#   included (it is the title as printed, p4 y739-754).
# GLYPHS: none in the lines used.
CRIT_2017 = crit((114, 115), (116, 117), (118, 119), 120)
LEAD_2017 = quote(L(112, 113), lead='The scheme prints')
SPECS[2017] = [
    R('II1', [graded(S(130), PARTP(), CRIT_2017)],
      rownote=both(LEAD_2017, examples(S(131), S(132), S(133), L(134, 137), L(138, 139), L(140, 145),
                                       L(146, 150), L(151, 152), L(153, 155), L(156, 157))),
      question=QP(4, 'Kommentár (min.', Run('Kommentálja a szöveg', 'is szól”!')), pages=(2, 3)),
    R('III1', [graded(S(164), PARTP(), CRIT_2017)], rownote=LEAD_2017,
      question=QP(4, 'A két téma közül', Run('„Egy ponton', 'tegye meg!”'))),
    R('III2', [graded(S(164), PARTP(), CRIT_2017)], rownote=LEAD_2017,
      question=QP(4, 'A két téma közül', Run('„A véleményem', 'az álláspontot a modern'))),
]


# ====================================================================== 2018
# ================================================================ 2018 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (see the live
# audit, hungarian-live-faults-2010-2018.json).
# Paper (rendered pp2-4): rule p2 y65-80; reading text "Jólétet mindenkinek!"
# p2 y109 to the byline "Weyer Béla: HVG, 2017, adaptáció" p3 y404
# (paragraphs 1-6 on p2, the end of 6 and 7-8 on p3); "I. RÉSZ (30 pont / 100
# pont)" p3 y489 (Q1 on p3, Q2-Q6 on p4); "II. RÉSZ (30 pont / 100 pont)" p4
# y329 with "Kommentár (min. 100, max. 150 szóban)" y358; "III. RÉSZ (40 pont /
# 100 pont)" p4 y475, titles "1. lehetőség" / "vagy" / "2. lehetőség".
# PRICES: II1 "(30 pont / 100 pont)", III1/III2 "(40 pont / 100 pont)" on the
# part heads (PARTP). Nothing else is priced for these parts.
# WHAT THE SCHEME PRINTS (rendered scheme pp4-6):
# - Criteria: the lead "A II. és III. részben elérhető pontok az alábbi
#   szempontok szerint oszlanak meg:" at the foot of p4 (124), the four
#   criteria at 30/30/30/10 % at the top of p5 (129-135), for Parts II and
#   III: graded.
# - Part II (p5; 136-140 reprint the head and the task): requirement line "A
#   minimum 100, maximum 150 szóban tisztán, érthetően kifejtett saját
#   vélemény." (141), the graded head; "Lehetséges irányok:" (142), a lead
#   "Azért nem minden úgy valósult meg, ... mert:" (143-145) and eight dashed
#   points (146-177; the sixth runs over the page break, 162-164 + 169-170),
#   quoted as examples in order.
# - Part III (p6, 178-191): "Tisztán, érthetően és világosan megírt esszé."
#   (180).
# SHAPES: II1, III1, III2 graded(head, PARTP(), CRIT_2018).
# JUDGEMENT CALLS:
# - Reading text pp2-3 (rendered); pages=(2, 3) on II1. Live Part I cards carry
#   [3]: flagged in the live audit.
# - II1's question: head line "Kommentár (min. 100, max. 150 szóban)" + the
#   task, as 2017 (the task itself also says "min. 100 szóban").
# - III1: the paper prints the title with no closing stop; the scheme's reprint
#   opens with a doubled „„ (182). The paper's is the question.
# - III2: the title's three printed sentences, the instruction included.
# GLYPHS: none in the lines used.
CRIT_2018 = crit((129, 130), (131, 132), (133, 134), 135)
LEAD_2018 = quote(S(124), lead='The scheme prints')
SPECS[2018] = [
    R('II1', [graded(S(141), PARTP(), CRIT_2018)],
      rownote=both(LEAD_2018, examples(S(142), L(143, 145), L(146, 149), L(150, 154), S(155), L(156, 161),
                                       J(L(162, 164), L(169, 170)), L(171, 172), L(173, 177))),
      question=QP(4, 'Kommentár (min.', Run('Kommentálja a szöveg', 'megjelent, mindenkinek')), pages=(2, 3)),
    R('III1', [graded(S(180), PARTP(), CRIT_2018)], rownote=LEAD_2018,
      question=QP(4, 'A két téma közül', Run('„Az ország csak', 'elveinek, ha a jelenleginél'))),
    R('III2', [graded(S(180), PARTP(), CRIT_2018)], rownote=LEAD_2018,
      question=QP(4, 'A két téma közül', Run('A ruha teszi', 'véleményét egy min.'))),
]
