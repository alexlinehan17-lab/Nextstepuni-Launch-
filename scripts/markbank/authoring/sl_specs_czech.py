#!/usr/bin/env python3
"""Reviewed specs for the Czech classic examination (small-languages lane).

One entry per printed ask with no live card; see sl_lib.py for the selector
language. Line numbers are lines of examiner-reports/czech/schemes/<year>-hl.md.
Drafted by Opus helpers on the Bulgarian, Romanian, Dutch and Maltese models, integrated
and gated by the lane lead.
"""
from sl_lib import (R, S, SR, J, L, PL, PC, QP, QL, Run, pre, prerun, PP, SP, PY, RX, PaperP, PARTP, REM,  # noqa: F401
                    one, shown, graded, crit, examples, quote, unprinted, part, NoScheme)
from pl_listen_lib import Join  # noqa: F401

SPECS = {}


def both(*notes):
    """Several printed notes on one row, in order."""
    return lambda doc: ' '.join(n(doc) for n in notes)


# ================================================================ 2010 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, cs-2010-hl-i-1); not
# touched.
# Paper (rendered pp2-4): "Část 1 [30 bodů]" (p2 y235) over the reading text
# "Mazej ze školy" (p2 y259, eight numbered paragraphs to "(upraveno podle
# www.respekt.cz)" p3 y490); questions from p3 y539: Q1 "[5 bodů]" over a)-e)
# (live); Q2-Q6 "[5 bodů]" each; "Část 2 [30 bodů]" (p4 y209), the commentary,
# ONE task with no number; "Část 3 [40 bodů]" (p4 y365), the instruction and
# two titles "1."/"2.".
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - I2 "[5 bodů]" at the end of the question's last line (p3 y682,
#   "Vysvětlete na základě textu. [5 bodů]"): PaperP.
# - I3 "[5 bodů]" at the end of "základě textu. [5 bodů]" (p3 y722): PaperP.
# - I4 "[5 bodů]" at the end of "Co tuto situaci činí tak absurdní? [5 bodů]"
#   (p3 y761): PaperP.
# - I5 "[5 bodů]" on a line of its own under the question (p4 x467 y106).
#   PY cannot read it (its cell pattern takes "bodu"/"bod", not "bodů": PY(4,
#   106) returns 0 cells); it is the only line of p4 opening "[5 bodů]", so
#   PaperP(4, '[5 bodů]') reads the printed cell itself.
# - I6 "[5 bodů]" at the end of the question's own line (p4 y131): PaperP.
# - II: the part head "Část 2 [30 bodů]" (PARTP); III1/III2: "Část 3 [40
#   bodů]" (PARTP). The scheme prints the same totals on its own heads (68, 78).
# WHAT THE SCHEME PRINTS (rendered scheme pp2-3; answers in a smaller type):
# - Q2 (25-26 reprint the question, "[5 bodů]"): one paragraph, 27-31 ("Přístup
#   ke vzdělání nebyl svobodný. ... podepisoval petice apod.").
# - Q3 (32-33): one paragraph, 34-37.
# - Q4 (38-39): one paragraph, 40-43.
# - Q5 (44-46): one paragraph, 47-49.
# - Q6 (54-55, p3): one paragraph, 56-60.
#   No bullet, no split, no mark inside any of them: model answers (10a).
# - Criteria (p3, 61-67, between Part I and Part II): "Poznámka: V částech 2 a
#   3 jsou odpovědi posuzovány podle následujích kritérií:" -- for Parts 2 AND
#   3 -- then 1. "– 30 %." (62), 2. "– 30 %." (63-64), 3. "– 30 %." (65-66,
#   the percentage wrapped onto its own line), 4. "– 10 %." (67): all four
#   printed, 100 %.
# - Part II (68-72 reprint the head and the task): the descriptive line
#   "Správný, plynulý komentář o minimálně 100 slovech." (73, normal type),
#   then one paragraph of content in the smaller type (74-77, "Bubliny jsou
#   něco velmi lehkého ...").
# - Part III (78-81 reprint the head, the instruction and both titles): one
#   descriptive line only (82-83, "Jasně psaná kompozice, ...").
# SHAPES:
# - I2-I6: each one model paragraph, shown, whole=True on the paper's printed
#   5 (10a; the brief: never an exclusion, never split where the scheme does
#   not split).
# - II: graded on the four criteria (10b): 30/30/30/10 % of the paper's 30 =
#   9 / 9 / 9 / 3. Head: the part's own descriptive line (73). The criteria's
#   lead quoted (it names the parts they serve) and the content paragraph
#   quoted as examples, not a checklist (10a).
# - III1/III2: graded (10b): 30/30/30/10 % of 40 = 12 / 12 / 12 / 4; head the
#   part's descriptive line (82-83); the criteria's lead quoted.
# JUDGEMENT CALLS:
# - I2-I6 shown (self-assessed), not one(): each is a model paragraph the
#   scheme prices only as a whole (brief: 10a, whole=True). Bulgarian 2013 I6
#   and 2015 I2-I6 claim such a paragraph as one row; the brief for Czech
#   settles the other way.
# - Part II is keyed 'II' (cited "Section II") as the census keys it; its
#   question is the census's text (checked against p4: the quotation and the
#   task, no price).
# - Part III questions: the instruction and the title, cut from p4 (the census
#   gives the bare title).
# - Reading text: pp2-3 (rendered). The live Q1 card's sourceMaterial.pages
#   [2, 3] AGREE with the render.
# GLYPHS: none (no character outside Czech letters and punctuation in either
# text layer). Printed as such on the render, lifted as printed: "následujích"
# (61, the criteria's lead, for "následujících"), "souvislousti" (42, Q4's
# row), "lehkého lehkého" (74, a doubled word in Part II's content), "a a
# vhodnou" (63, a doubled word in criterion 2).

CRIT_2010 = crit(62, (63, 64), (65, 66), 67)
LEAD_2010 = quote(S(61, after='Poznámka: '), lead='The scheme prints')
ESSAY_2010 = 'Napište esej'

SPECS[2010] = [
    R('I2', [shown(L(27, 31))], whole=True, total=PaperP(3, 'Vysvětlete na základě textu.'), pages=(2, 3)),
    R('I3', [shown(L(34, 37))], whole=True, total=PaperP(3, 'základě textu.'), pages=(2, 3)),
    R('I4', [shown(L(40, 43))], whole=True, total=PaperP(3, 'Co tuto situaci'), pages=(2, 3)),
    R('I5', [shown(L(47, 49))], whole=True, total=PaperP(4, '[5 bodů]'), pages=(2, 3)),
    R('I6', [shown(L(56, 60))], whole=True, total=PaperP(4, '6. Autor popisuje'), pages=(2, 3)),
    R('II', [graded(S(73), PARTP(), CRIT_2010)],
      rownote=both(LEAD_2010, examples(None, L(74, 77))), pages=(2, 3)),
    R('III1', [graded(L(82, 83), PARTP(), CRIT_2010)], rownote=LEAD_2010,
      question=QP(4, ESSAY_2010, '1. Svoboda')),
    R('III2', [graded(L(82, 83), PARTP(), CRIT_2010)], rownote=LEAD_2010,
      question=QP(4, ESSAY_2010, '2. Nikdo')),
]


# ================================================================ 2011 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, cs-2011-hl-i-1); not
# touched.
# Paper (rendered pp2-4): an italic lead-in and "Část 1 [30 bodů]" on p2, the
# reading text "Smlouva s rodiči" from p2 to its byline "Jan-Michal Mleziva
# (nar. 1965), učitel" / "(upraveno podle Rodina a škola 8/2010)" (p3
# y495-519); questions from p3 y562: Q1 "[5 bodů]" over a)-e) (live); Q2-Q6
# "[5 bodů]" each; "Část 2 [30 bodů]" (p4 y270), the commentary, ONE task with
# no number; "Část 3 [40 bodů]" (p4 y394), the instruction and two titles.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - I2 and I3: the paper prints each "[5 bodů]" on a line of its own under the
#   question (p3 x480 y693 and p3 x480 y748; rendered p3, right margin). Two
#   lines of p3 open "[5 bodů]", so PaperP cannot single either out, and PY
#   cannot read the cell (its cell pattern takes "bodu"/"bod", not "bodů").
#   Priced from the scheme's own printed "[5 bodů]" on the question's reprint
#   (RX: line 29 "mysli. [5 bodů]", line 35 "na základě textu. [5 bodů]"),
#   the same 5 the paper prints. If the lead adds "bodů" to PY's cell pattern,
#   these become PY(3, 693) and PY(3, 748).
# - I4 "[5 bodů]" on a line of its own (p4 x480 y77), the only line of p4
#   opening "[5 bodů]": PaperP(4, '[5 bodů]').
# - I5 "[5 bodů]" at the end of "názor na toto tvrzení. [5 bodů]" (p4 y131),
#   I6 at the end of "rodiče. [5 bodů]" (p4 y200): PaperP.
# - II: "Část 2 [30 bodů]" (PARTP); III1/III2: "Část 3 [40 bodů]" (PARTP).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5; answers in italics):
# - Q2 (28-29 reprint): one paragraph, 30-32. Q3 (33-35): one paragraph,
#   36-40. Q4 (41-42): one paragraph, 43-50. Q5 (55-57, p4): one paragraph,
#   58-64. Q6 (65-67): one paragraph, 68-71. No split, no mark inside any:
#   model answers (10a).
# - Criteria (p4, 72-78): "Poznámka: V částech 2 a 3 jsou odpovědi posuzovány
#   podle následujících kritérií:" -- Parts 2 AND 3 -- then "– 30%." (73),
#   "– 30%." (74-75), "– 30%." (76-77, wrapped), "– 10%." (78): 100 %.
# - Part II (79-82 reprint the head and the task): the bold descriptive line
#   "Správný, plynulý komentář o minimálně 100 slovech." (83), then one italic
#   paragraph of content (84-87, "Souhlas, nesouhlas. Dříve měli učitelé ...").
# - Part III (p5, 92-93 the head and the instruction): the bold descriptive
#   line "Jasně psaná kompozice, ..." (94-95) printed ABOVE the two titles
#   (96-98).
# SHAPES:
# - I2-I6: each one model paragraph, shown, whole=True on the printed 5 (10a).
# - II: graded (10b), 9 / 9 / 9 / 3 of 30; head the descriptive line (83);
#   the criteria's lead quoted; the paragraph quoted as examples (10a).
# - III1/III2: graded (10b), 12 / 12 / 12 / 4 of 40; head the descriptive
#   line (94-95); the criteria's lead quoted.
# JUDGEMENT CALLS:
# - I2/I3 priced from the scheme (RX), not the paper: the paper's cells are
#   printed but not readable by the selectors this branch has (see PRICES).
# - Part III title 2 is the quotation and its attribution line (p4 y476-490),
#   joined.
# - Reading text: pp2-3 (rendered). The live Q1 card's sourceMaterial.pages
#   [2, 3] AGREE with the render.
# GLYPHS: none in either text layer. Printed as such (rendered), lifted as
# printed: "ústě" (44, Q4's row; for "úctě"), "vykovává" (61, Q5's row).

CRIT_2011 = crit(73, (74, 75), (76, 77), 78)
LEAD_2011 = quote(S(72, after='Poznámka: '), lead='The scheme prints')
ESSAY_2011 = 'Napište esej'
BODU = r'\[(\d+) bodů\]'

SPECS[2011] = [
    R('I2', [shown(L(30, 32))], whole=True, total=RX(29, BODU), pages=(2, 3)),
    R('I3', [shown(L(36, 40))], whole=True, total=RX(35, BODU), pages=(2, 3)),
    R('I4', [shown(L(43, 50))], whole=True, total=PaperP(4, '[5 bodů]'), pages=(2, 3)),
    R('I5', [shown(L(58, 64))], whole=True, total=PaperP(4, 'názor na toto tvrzení.'), pages=(2, 3)),
    R('I6', [shown(L(68, 71))], whole=True, total=PaperP(4, 'rodiče.'), pages=(2, 3)),
    R('II', [graded(S(83), PARTP(), CRIT_2011)],
      rownote=both(LEAD_2011, examples(None, L(84, 87))), pages=(2, 3)),
    R('III1', [graded(L(94, 95), PARTP(), CRIT_2011)], rownote=LEAD_2011,
      question=QP(4, ESSAY_2011, '1. Učení')),
    R('III2', [graded(L(94, 95), PARTP(), CRIT_2011)], rownote=LEAD_2011,
      question=QP(4, ESSAY_2011, '2. „Většina', '(Abraham Lincoln')),
]


# ================================================================ 2012 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, cs-2012-hl-i-1); not
# touched.
# Paper (rendered pp2-4): the rule and the reading text "Jak mluví ženy a jak
# muži?" in ten numbered paragraphs over pp2-3, to its byline "(Václav
# Cvrček, jazykovědec)" / "(upraveno podle aktualne.cz)" (p3, foot); p4 opens
# "Část 1 [30 bodů]" (p4 y98) over the questions: Q1 "[5 bodů]" over a)-e)
# (live); Q2-Q6 "[5 bodů]" each; "Část 2 [30 bodů]" (p4 y531), the commentary,
# ONE task with no number; "Část 3 [40 bodů]" (p4 y658), the instruction and
# two titles.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - I2 and I5: the paper prints each "[5 bodů]" on a line of its own under the
#   question (p4 x455 y287 and p4 x455 y429; rendered p4, right margin). Two
#   lines of p4 open "[5 bodů]", so PaperP cannot single either out, and PY
#   cannot read the cell (its pattern takes "bodu"/"bod", not "bodů"). Priced
#   from the scheme's printed "[5 bodů]" on the question's reprint (RX: line 28,
#   a line of its own; line 45 "... na celý text. [5 bodů]"), the same 5 the
#   paper prints. With "bodů" in PY's pattern: PY(4, 287), PY(4, 429).
# - I3 "jazyka? [5 bodů]" (p4 y325), I4 "Na základě textu vysvětlete rizika
#   ... [5 bodů]" (p4 y364), I6 "napište krátký text odkazující k textu. [5
#   bodů]" (p4 y481): the price at the end of the question's last line, PaperP.
# - II: "Část 2 [30 bodů]" (PARTP; the scheme prints "[30 bodů]" beside its
#   descriptive line, 76); III1/III2: "Část 3 [40 bodů]" (PARTP; scheme 80).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4; answers in a smaller type):
# - Q2 (27-28 reprint): one paragraph, 29-32. Q3 (33-34): one paragraph,
#   35-36. Q4 (37-38): one paragraph, 39-42. Q5 (43-45): one paragraph, 46-51.
#   Q6 (52-54, p3): one paragraph on p4, 58-63. No split, no mark inside any:
#   model answers (10a).
# - Criteria (p4, 64-70): "Poznámka: V částech 2 a 3 jsou odpovědi posuzovány
#   podle následujících kritérií:" -- Parts 2 AND 3 -- then "– 30 %." (65),
#   "– 30 %." (66-67), "– 30 %." (68-69), "– 10 %." (70): 100 %.
# - Part II (71-75 reprint the head and the task): the descriptive line
#   "Správný, plynulý komentář o minimálně 100 slovech." with "[30 bodů]" set
#   in its right-hand cell (76), then one paragraph of content in the smaller
#   type (77-79, "Souhlas, nesouhlas. Mohou jazyk ...", three questions).
# - Part III (80-83 reprint the head, the instruction and both titles): one
#   descriptive line only (84-85, "Jasně psaná kompozice, ...").
# SHAPES:
# - I2-I6: each one model paragraph, shown, whole=True on the printed 5 (10a).
# - II: graded (10b), 9 / 9 / 9 / 3 of 30; head the descriptive line (76, cut
#   before its "[30 bodů]"); the criteria's lead quoted; the paragraph quoted as
#   examples (10a).
# - III1/III2: graded (10b), 12 / 12 / 12 / 4 of 40; head the descriptive line
#   (84-85); the criteria's lead quoted.
# JUDGEMENT CALLS:
# - I2/I5 priced from the scheme (RX), not the paper (see PRICES).
# - Reading text: pp2-3 (rendered: p2 opens with the rule and the title, the
#   text runs to the byline at the foot of p3; p4 holds only the questions).
#   The live Q1 card's sourceMaterial.pages [2, 3] AGREE with the render.
# GLYPHS: none in either text layer. Lifted as printed: the scheme's straight
# quotation marks in Q5's row ("vyčistit", "popisnice", "munjovoz", 47-49);
# "s kamarádi" (40, Q4's row), "požití" (78, Part II's content).

CRIT_2012 = crit(65, (66, 67), (68, 69), 70)
LEAD_2012 = quote(S(64, after='Poznámka: '), lead='The scheme prints')
ESSAY_2012 = 'Napište esej'
BODU = r'\[(\d+) bodů\]'

SPECS[2012] = [
    R('I2', [shown(L(29, 32))], whole=True, total=RX(28, BODU), pages=(2, 3)),
    R('I3', [shown(L(35, 36))], whole=True, total=PaperP(4, 'jazyka?'), pages=(2, 3)),
    R('I4', [shown(L(39, 42))], whole=True, total=PaperP(4, 'Na základě textu vysvětlete rizika'),
      pages=(2, 3)),
    R('I5', [shown(L(46, 51))], whole=True, total=RX(45, BODU), pages=(2, 3)),
    R('I6', [shown(L(58, 63))], whole=True, total=PaperP(4, 'napište krátký text'), pages=(2, 3)),
    R('II', [graded(S(76, before=' [30'), PARTP(), CRIT_2012)],
      rownote=both(LEAD_2012, examples(None, L(77, 79))), pages=(2, 3)),
    R('III1', [graded(L(84, 85), PARTP(), CRIT_2012)], rownote=LEAD_2012,
      question=QP(4, ESSAY_2012, '1. Stereotypy')),
    R('III2', [graded(L(84, 85), PARTP(), CRIT_2012)], rownote=LEAD_2012,
      question=QP(4, ESSAY_2012, '2. V naší')),
]


# ================================================================ 2013 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, cs-2013-hl-i-1); not
# touched.
# Paper (rendered pp2-4): the rule and "Část 1 [30 bodů]" (p2 y190) over the
# reading text "Bez mámy se neobejdu", eight numbered paragraphs over pp2-3 to
# "(Zuzana Dastychová, upraveno podle časopisu Instinkt)" (p3 y651); p4 holds
# the questions: Q1 "[5 bodů]" over a)-e) (live); Q2-Q6 "[5 bodů]" each;
# "Část 2 [30 bodů]" (p4 y470), the commentary, ONE task with no number;
# "Část 3 [40 bodů]" (p4 y626), the instruction and two titles.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply): every
# Q2-Q6 prints "[5 bodů]" in the right-hand cell of the question's own last
# line (rendered p4), read with PaperP: Q2 "2. Popište ..." (y234), Q3 "3.
# Vysvětlete ..." (y260), Q4 "rozdíly ve vnímání ..." (y299), Q5 "Myslíte si,
# ..." (y339), Q6 "s rodiči, včetně ..." (y392). II: "Část 2 [30 bodů]"
# (PARTP); III1/III2: "Část 3 [40 bodů]" (PARTP). The scheme prints the same
# "[5 bodů]" on each reprint, "[30 bodů]" (102) and "[40 bodů]" (109).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4; answers in a smaller type):
# - Q2 (58): one paragraph, 59-61. Q3 (62): one paragraph, 63-65. Q4 (66-67):
#   one paragraph, 68-71. Q5 (72-73): one paragraph, 74-78. Q6 (82-84, p4): one
#   paragraph, 85-90. No split, no mark inside any: model answers (10a).
# - Criteria (p4, 91-97): "Poznámka: V částech 2 a 3 jsou odpovědi posuzovány
#   podle následujících kritérií:" -- Parts 2 AND 3 -- then "– 30 %." (92),
#   "– 30 %." (93-94), "– 30 %." (95-96), "– 10 %." (97): 100 %.
# - Part II (98-102 reprint the head and the task, "[30 bodů]"): NO
#   descriptive line this sitting; one paragraph of content in the smaller
#   type (103-108, "Souhlas, nesouhlas. Dítě by nemělo být přívěškem ...").
# - Part III (109-112 reprint the head, the instruction and both titles): one
#   descriptive line only (113-114, "Jasně psaná kompozice, ...").
# SHAPES:
# - I2-I6: each one model paragraph, shown, whole=True on the printed 5 (10a).
# - II: graded (10b), 9 / 9 / 9 / 3 of 30. With no descriptive line, the head
#   is the criteria's own lead (91, cut after "Poznámka: "), as Dutch 2010
#   heads its Part II; the paragraph quoted as examples (10a).
# - III1/III2: graded (10b), 12 / 12 / 12 / 4 of 40; head the descriptive line
#   (113-114); the criteria's lead quoted.
# JUDGEMENT CALLS:
# - Q3: the paper prints "důvody mamánkovsví" (rendered p4 at 200 dpi: the
#   SEC's typing, a letter short); the scheme reprints it "mamánkovství" (62).
#   The paper wins on the question (10f); the scheme's reprint is quoted on the
#   row's note.
# - Reading text: pp2-3 (rendered). The live Q1 card's sourceMaterial.pages
#   [2, 3] AGREE with the render. (The live Q1 card's c) is a scheme matter
#   outside this draft: the scheme reprints "pokerovém stole světa", the paper
#   "pokerovém stole tohoto světa".)
# GLYPHS: none in either text layer (no character outside Czech letters and
# punctuation); the rows match the rendered scheme pp3-4.

CRIT_2013 = crit(92, (93, 94), (95, 96), 97)
LEAD_2013 = quote(S(91, after='Poznámka: '), lead='The scheme prints')
ESSAY_2013 = 'Napište esej'

SPECS[2013] = [
    R('I2', [shown(L(59, 61))], whole=True, total=PaperP(4, '2. Popište'), pages=(2, 3)),
    R('I3', [shown(L(63, 65))], whole=True, total=PaperP(4, '3. Vysvětlete'), pages=(2, 3),
      rownote=quote(S(62, after='3. ', before=' [5'), lead='The scheme reprints this question as')),
    R('I4', [shown(L(68, 71))], whole=True, total=PaperP(4, 'rozdíly ve vnímání'), pages=(2, 3)),
    R('I5', [shown(L(74, 78))], whole=True, total=PaperP(4, 'Myslíte si'), pages=(2, 3)),
    R('I6', [shown(L(85, 90))], whole=True, total=PaperP(4, 's rodiči, včetně'), pages=(2, 3)),
    R('II', [graded(S(91, after='Poznámka: '), PARTP(), CRIT_2013)],
      rownote=examples(None, L(103, 108)), pages=(2, 3)),
    R('III1', [graded(L(113, 114), PARTP(), CRIT_2013)], rownote=LEAD_2013,
      question=QP(4, ESSAY_2013, '1. Opičí')),
    R('III2', [graded(L(113, 114), PARTP(), CRIT_2013)], rownote=LEAD_2013,
      question=QP(4, ESSAY_2013, '2. Jít')),
]


# ================================================================ 2014 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, cs-2014-hl-i-1); not
# touched.
# Paper (rendered pp2-4): "ČESKÝ JAZYK 2014", the rule and "Část 1 [30 bodů]"
# (p2 y191) over the reading text "Jmenují se Emma Smetana, či Petra Svoboda.
# Proč to té češtině dělají?" (an italic lead-in, then ten numbered
# paragraphs over pp2-3 to "(Kristina Komůrková, upraveno podle idnes.cz)", p3
# y609); Q1 "[5 bodů]" over a)-e) on p3 (live); Q2-Q6 on p4, "[5 bodů]" each;
# "Část 2 [30 bodů]" (p4 y417), the commentary, ONE task with no number; "Část
# 3 [40 bodů]" (p4 y584), the instruction and two titles.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply): every
# Q2-Q6 prints "[5 bodů]" in the right-hand cell of the question's own last
# line (rendered p4), read with PaperP: Q2 "2. Jaký ..." (y78), Q3 "3. Jaké
# ..." (y119), Q4 "4. Popište ..." (y161), Q5 "s jazyky uvedenými ..." (y216),
# Q6 "svůj souhlas nebo nesouhlas ..." (y299). II: "Část 2 [30 bodů]"
# (PARTP); III1/III2: "Část 3 [40 bodů]" (PARTP). The scheme prints the same
# "[5 bodů]", "[30 bodů]" (105) and "[40 bodů]" (111).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4; answers in a smaller type):
# - Q2 (61): ONE sentence, 62-63 ("Ženské příjmení v češtině má ve většině
#   případů na konci přidanou koncovku -ová, např. Novák / Nováková.").
# - Q3 (64): one paragraph, 65-69. Q4 (70): one paragraph, 71-74. Q5 (75-76):
#   one paragraph, 77-83. Q6 (87-90, p4): one paragraph, 91-93. No split, no
#   mark inside any: model answers (10a).
# - Criteria (p4, 94-100): "Poznámka: V částech 2 a 3 jsou odpovědi posuzovány
#   podle následujících kritérií:" -- Parts 2 AND 3 -- then "– 30 %." (95),
#   "– 30 %." (96-97), "– 30 %." (98-99), "– 10 %." (100): 100 %.
# - Part II (101-105 reprint the head and the task, "[30 bodů]"): NO
#   descriptive line; one paragraph of content (106-110, "Souhlas, nesouhlas.
#   Toto tvrzení velmi silně souvisí s historií naší země, ...").
# - Part III (111-115 reprint the head, the instruction and both titles): one
#   descriptive line only (116-117, "Jasně psaná kompozice, ...").
# SHAPES:
# - I2: ONE stated answer (a single fact, one sentence): one(row) at the
#   paper's 5, claimable.
# - I3-I6: each one model paragraph, shown, whole=True on the printed 5 (10a).
# - II: graded (10b), 9 / 9 / 9 / 3 of 30; head the criteria's own lead (94,
#   no descriptive line this sitting; as 2013 and Dutch 2010); the paragraph
#   quoted as examples (10a).
# - III1/III2: graded (10b), 12 / 12 / 12 / 4 of 40; head the descriptive line
#   (116-117); the criteria's lead quoted.
# JUDGEMENT CALLS:
# - I2 one() (claimable) rather than shown: the scheme states one fact, not a
#   model paragraph. If the lead prefers every Czech Part I answer
#   self-assessed, flip to shown, whole=True.
# - I2's row runs over a line break after a spaced slash ("Novák /" on 62,
#   "Nováková." on 63; rendered p3). L()/J() glue a line ending "/" to the
#   next with no space ("Novák /Nováková."), so the two lines are joined by
#   the small Spaced helper below with the printed space. If the lead would
#   rather not carry a helper, L(62, 63) builds the card with the space lost.
# - Part II (10f): the paper prints only the quotation and "Napište komentář
#   (minimum 100 slov), ve kterém vysvětlíte svůj názor na toto tvrzení." (p4
#   y485); the scheme's reprint adds "Vysvětlete, proč si toto autorka myslí, a
#   napište komentář ..." (104-105). The paper wins on the question; the
#   scheme's reprint quoted on the row's note.
# - Part III title 1 (10f): the paper prints "Z vlastní zkušenosti - myslíte,
#   že nastal konečně čas změnit pravidla českého pravopisu?" (p4 y643-657);
#   the scheme reprints "Nastal čas změnit pravidla českého pravopisu?" (113).
#   The paper's title is the question; the scheme's words quoted.
# - The scheme's reprints of Q4 ("jaká je postoj", paper "jaký je postoj") and
#   Q6 (word order "křehkou ženu přivlastňuje") differ from the paper in
#   question text only; not quoted (no row depends on them).
# - Reading text: pp2-3 (rendered). The live Q1 card's sourceMaterial.pages
#   [2, 3] AGREE with the render.
# GLYPHS: none in either text layer; the rows match the rendered scheme.

class Spaced:
    """Two cuts the SEC wrapped at a spaced slash ("např. Novák /" over
    "Nováková."), joined with the printed space: Join glues a line that ends
    in "/" to the next ("sport centres/" over "schools"), which would print
    "Novák /Nováková"."""
    def __init__(self, *parts):
        self.parts = parts

    def text(self, doc):
        return ' '.join(p.text(doc) for p in self.parts)


CRIT_2014 = crit(95, (96, 97), (98, 99), 100)
LEAD_2014 = quote(S(94, after='Poznámka: '), lead='The scheme prints')
ESSAY_2014 = 'Napište esej'

SPECS[2014] = [
    R('I2', [one(Spaced(S(62), S(63)), PaperP(4, '2. Jaký'))], total=PaperP(4, '2. Jaký'), pages=(2, 3)),
    R('I3', [shown(L(65, 69))], whole=True, total=PaperP(4, '3. Jaké'), pages=(2, 3)),
    R('I4', [shown(L(71, 74))], whole=True, total=PaperP(4, '4. Popište'), pages=(2, 3)),
    R('I5', [shown(L(77, 83))], whole=True, total=PaperP(4, 's jazyky uvedenými'), pages=(2, 3)),
    R('I6', [shown(L(91, 93))], whole=True, total=PaperP(4, 'svůj souhlas'), pages=(2, 3)),
    R('II', [graded(S(94, after='Poznámka: '), PARTP(), CRIT_2014)],
      rownote=both(examples(None, L(106, 110)),
                   quote(L(102, 105, before=' [30'), lead='The scheme reprints the task as')),
      pages=(2, 3)),
    R('III1', [graded(L(116, 117), PARTP(), CRIT_2014)],
      rownote=both(LEAD_2014, quote(S(113, after='1. '), lead='The scheme reprints this title as')),
      question=QP(4, ESSAY_2014, Run('1. Z vlastní', 'pravopisu?'))),
    R('III2', [graded(L(116, 117), PARTP(), CRIT_2014)], rownote=LEAD_2014,
      question=QP(4, ESSAY_2014, Run('2. I když', 's sebou.'))),
]


# ================================================================ 2015 HL ===
# Drafted (small-languages lane, 20 Nov): every ask of this sitting, Q1 carded
# whole at the parent key I1 (its listed asks I1a-I1e), I2-I6, II, III1, III2.
# No live 2015 card.
# Paper (rendered pp2-4): "ČESKÝ JAZYK 2015", the rule and "Část 1 [30 bodů]"
# (p2 y191) over the reading text "Děti úplňku", eleven numbered paragraphs
# over pp2-3 to "(Petr Třešňák, upraveno podle respekt.ihned.cz)" (p3 y740);
# p4 holds the questions: Q1 "1. Vysvětlete vlastními slovy: [5 bodů]" (p4
# y78) over a)-e), NO mark beside any expression (rendered p4: the five
# expressions indented, nothing in the right margin); Q2-Q6 "[5 bodů]" each;
# "Část 2 [30 bodů]" (p4 y510), the commentary, ONE task with no number; "Část
# 3 [40 bodů]" (p4 y642), the instruction and two titles.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - I1: "[5 bodů]" for the question as a whole, on its stem line (p4 y78):
#   PaperP. The paper prints no per-expression mark and the scheme none either
#   (50: "1. Vysvětlete vlastními slovy: [5 bodů]", then a)-e) unpriced). So Q1
#   is carded WHOLE at the parent key I1, the five glosses as shown rows on the
#   paper's 5, as the live Czech Q1 cards of 2010-2014, 2016, 2017 are (brief;
#   Romanian 2010-2019). Not 10i: the paper prints Q1's own total.
# - Q2-Q6: "[5 bodů]" in the right-hand cell of the question's own last line
#   (rendered p4), PaperP: Q2 "2. Vysvětlete ..." (y216), Q3 "3. Popište ..."
#   (y258), Q4 "zdravotnická a sociální zařízení." (y320), Q5 "„A nelze
#   vyloučit ..." (y382), Q6 "6. Vysvětlete ..." (y430).
# - II: "Část 2 [30 bodů]" (PARTP); III1/III2: "Část 3 [40 bodů]" (PARTP). The
#   scheme prints the same totals on its heads (103, 111).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4; the .md repaired from glyph
# ids, checked against the render word by word for every line used):
# - Q1 (50): a) to e), each the expression, a colon (a, b) or a hyphen (c-e),
#   and its gloss: a) 51-52, b) 53-54, c) 55, d) 56-57, e) 58-59.
# - Q2 (60): ONE sentence, 61-62 ("Mezi tajuplné a nevysvětlené otázky kolem
#   autismu patří fakt, že záchvaty často propukají kolem úplňku měsíce.").
# - Q3 (63): one paragraph, 64-70. Q4 (71-72): one paragraph, 73-78.
# - Q5 (79-80): one paragraph, 81-87, then a line of its own (88, "Vlastní
#   interpretace tohoto trvrzení, vlastními slovy.": rendered p3, flush left
#   under the short last line "může klamat.").
# - Q6 (93, p4): a requirement only, one paragraph 94-95 ("Úkolem je vlastními
#   slovy vysvětlit, jestli se případně chápání autismu změnilo, ...").
# - Criteria (p4, 96-102): "Poznámka: V částech 2 a 3 jsou odpovědi posuzovány
#   podle následujících kritérií:" -- Parts 2 AND 3 -- then "– 30 %." (97),
#   "– 30 %." (98-99), "– 30" / "%." (100-101, the sign wrapped alone), "– 10
#   %." (102): 100 %.
# - Part II (103-105 reprint the head and the task): one paragraph of content
#   (106-109, "Souhlas, nesouhlas. I nemocný člověk, ..."), then a line of its
#   own, "Vlastními slovy, bez opsání frází z textu." (110).
# - Part III (111-114 reprint the head, the instruction and both titles): one
#   descriptive line only (115-116, "Jasně psaná kompozice, ...").
# SHAPES:
# - I1: questionTotal on the paper's 5, five shown rows (one gloss each, cut
#   after the expression and its colon or hyphen), each led by the PAPER's
#   expression.
# - I2: ONE stated answer (one fact, one sentence): one row at the paper's 5,
#   claimable (as 2014 I2).
# - I3, I4: one model paragraph each, shown, whole=True on the printed 5 (10a).
# - I5: the model paragraph and the scheme's own requirement line, two shown
#   rows (the scheme sets them apart), whole=True on the printed 5.
# - I6: the requirement-only answer shown, whole=True on the printed 5
#   (requirement-only answers are shown and self-assessed; Dutch 2011 Q5).
# - II, III1, III2: the right shape is graded (10b: 30/30/30/10 % of 30 and of
#   40 are whole numbers), BUT the shared reader cannot take it this sitting:
#   criterion 3 prints its percentage wrapped over two lines, "... jasně a
#   plynule – 30" (100) / "%." (101) (rendered p4: the sign alone on the next
#   line), and percent_of reads ONE line for "N %" (graded() raises "scheme
#   line 101 prints 0 percentages"). So SPECS below carries the shape that
#   builds today: the four criteria, with their printed percentages, as shown
#   rows on the paper's printed total (questionTotal 30 / 40; ruling F's shape,
#   10b's "show the percentages and score on the printed total"), the part's
#   own line and the criteria's lead quoted on the note. The graded entries
#   are written out in the block "PREFERRED" at the end of this file: swap
#   them in once percent_of reads a percentage wrapped over a crit span's
#   lines (a shared-code change for the lead; 9 / 9 / 9 / 3 and 12 / 12 / 12
#   / 4).
# JUDGEMENT CALLS:
# - Q1 c) (10f): the paper prints "„dostat do širšího povědomí“" (p4 y137);
#   the scheme reprints "„dostat se do širšího povědomí“" (55). The row is led
#   by the paper's words; the scheme's reprint is quoted on the first row's
#   note.
# - Q1's question is the paper's stem and its five expressions, each on its
#   own line with its printed letter (QL's shape), as the lane's whole-Q1
#   cards are built (Romanian 2012-2016); the live Czech Q1 cards (built by
#   lt_all) set them inline as "(a) petice (b) ...". The stem is cut before
#   its "[5 bodů]" by a small callable (_q1_2015): clean_question does not take
#   "bodů" as a price word, so QL itself would keep the price in the question.
# - I2 one() (claimable): see 2014 I2.
# - Part II's own line: the scheme prints no "Správný, plynulý komentář ..."
#   line this sitting; its requirement line (110) is the part's own line (the
#   graded head in PREFERRED; quoted on the note in SPECS). 2013 and 2014,
#   which print neither, are headed by the criteria's lead.
# - Reading text: pp2-3 (rendered). No live 2015 card to compare.
# GLYPHS: the repaired .md matches the render in every line used (no
# character outside Czech letters and punctuation; Č / ý, the pair the raw
# layer confuses, checked word by word in 45-117). Printed as such on the
# render (200 dpi crops of p3), SEC typing, lifted as printed: "smylsu" (53),
# "sitace" (58), "autististy", "nekdy", "prípad", "vytvočit", "sparavována"
# (73-77), "protže", "agličtinou", "ostaními", "nedopovídal" (81-84),
# "trvrzení" (88).

ESSAY_2015 = 'Napište esej'
CRIT_2015 = crit(97, (98, 99), (100, 101), 102)
LEAD_2015 = quote(S(96, after='Poznámka: '), lead='The scheme prints')
Q1P_2015 = PaperP(4, '1. Vysvětlete vlastními slovy:')
# The four criteria as printed, each with its percentage (shown rows).
CRIT_LINES_2015 = [S(97), L(98, 99), L(100, 101), S(102)]


def _crit_note_2015(d):
    return (f'Under “Poznámka:” the scheme prints “{S(96, after="Poznámka: ").text(d)}” and four criteria '
            'with their percentages, 30 / 30 / 30 / 10 %; the part is scored on its printed total.')


def _q1c_2015(d):
    return (f'The scheme reprints expression c) as “{S(55, after="c) ", before=" - ").text(d)}”; the paper prints '
            f'“{PC(4, "c) „dostat", after="c) ").text(d)}”.')


def _q1_2015(d, _census=None):
    """QL's shape (the stem, then each expression on its own line with its
    printed letter), the stem cut before its "[5 bodů]": clean_question does
    not take "bodů" for a price word, so QL would keep it."""
    stem = PC(4, '1. Vysvětlete vlastními slovy:', after='1. ', before=' [5').text(d)
    items = [PL(4, o).text(d) for o in ('a) rituál', 'b) stereotypní', 'c) „dostat', 'd) „obávaná', 'e) „pud')]
    return '\n'.join([stem] + items)


SPECS[2015] = [
    R('I1', [shown(L(51, 52, after='a) rituál: '), lead=PC(4, 'a) rituál', after='a) ')),
             shown(L(53, 54, after='b) stereotypní: '), lead=PC(4, 'b) stereotypní', after='b) ')),
             shown(S(55, after='povědomí“ - '), lead=PC(4, 'c) „dostat', after='c) ')),
             shown(L(56, 57, after='legenda“ - '), lead=PC(4, 'd) „obávaná', after='d) ')),
             shown(L(58, 59, after='sebezáchovy“ - '), lead=PC(4, 'e) „pud', after='e) '))],
      whole=True, total=Q1P_2015, rownote=_q1c_2015,
      question=_q1_2015,
      pages=(2, 3)),
    R('I2', [one(L(61, 62), PaperP(4, '2. Vysvětlete'))], total=PaperP(4, '2. Vysvětlete'), pages=(2, 3)),
    R('I3', [shown(L(64, 70))], whole=True, total=PaperP(4, '3. Popište'), pages=(2, 3)),
    R('I4', [shown(L(73, 78))], whole=True, total=PaperP(4, 'zdravotnická a sociální'), pages=(2, 3)),
    R('I5', [shown(L(81, 87)), shown(S(88))], whole=True, total=PaperP(4, '„A nelze vyloučit'),
      pages=(2, 3)),
    R('I6', [shown(L(94, 95))], whole=True, total=PaperP(4, '6. Vysvětlete'), pages=(2, 3)),
    R('II', [shown(c) for c in CRIT_LINES_2015], whole=True, total=PARTP(),
      rownote=both(quote(S(110), lead='The scheme heads it'), _crit_note_2015,
                   examples(None, L(106, 109))), pages=(2, 3)),
    R('III1', [shown(c) for c in CRIT_LINES_2015], whole=True, total=PARTP(),
      rownote=both(quote(L(115, 116), lead='The scheme heads it'), _crit_note_2015),
      question=QP(4, ESSAY_2015, '1. „Láska')),
    R('III2', [shown(c) for c in CRIT_LINES_2015], whole=True, total=PARTP(),
      rownote=both(quote(L(115, 116), lead='The scheme heads it'), _crit_note_2015),
      question=QP(4, ESSAY_2015, '2. „Člověk')),
]

# PREFERRED, in force (lead, 20 Nov): sl_lib now reads the percentage the
# scheme wraps over lines 100-101 ("– 30" / "%."), so Parts II and III are
# graded on the four criteria (9/9/9/3 of 30, 12/12/12/4 of 40) as 2010-2017.
SPECS[2015][-3:] = [
    R('II', [graded(S(110), PARTP(), CRIT_2015)],
      rownote=both(LEAD_2015, examples(None, L(106, 109))), pages=(2, 3)),
    R('III1', [graded(L(115, 116), PARTP(), CRIT_2015)], rownote=LEAD_2015,
      question=QP(4, ESSAY_2015, '1. „Láska')),
    R('III2', [graded(L(115, 116), PARTP(), CRIT_2015)], rownote=LEAD_2015,
      question=QP(4, ESSAY_2015, '2. „Člověk')),
]


# ================================================================ 2016 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, cs-2016-hl-i-1); not
# touched.
# Paper (rendered pp2-4): "ČESKÝ JAZYK 2016", the rule and "Část 1 [30 bodů]"
# (p2 y203) over the reading text "Recept od čtyř režisérů. Jak vyrobit
# legendární pohádku?", eleven numbered paragraphs running over pp2-3 INTO p4
# (paragraph 11, p4 y174, to "(Jiří Göth, upraveno podle lidovky.cz)", p4
# y252; a footnote on Švejk at the foot of p3); questions from p4 y282: Q1
# "[5 bodů]" over a)-e) (live); Q2-Q6 "[5 bodů]" each; "Část 2 [30 bodů]" (p4
# y584), the commentary, ONE task with no number; "Část 3 [40 bodů]" (p4
# y666), the instruction and two titles.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q2-Q5: "[5 bodů]" at the end of the question's own last line (rendered
#   p4), PaperP: Q2 "tím má na mysli." (y392), Q3 "3. Popište ..." (y420), Q4
#   "příliš uspět nedá“." (y462), Q5 "tak populární." (y504).
# - Q6: "[5 bodů]" on a line of its own (p4 x475 y545), the only line of p4
#   opening "[5 bodů]": PaperP(4, '[5 bodů]') (PY cannot read "bodů").
# - II: "Část 2 [30 bodů]" (PARTP); III1/III2: "Část 3 [40 bodů]" (PARTP).
#   The scheme prints the same totals on its heads (103, 114).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5; answers in a smaller type):
# - Q2 (57-58 reprint): one paragraph, 59-62. Q3 (63-64): one paragraph,
#   65-68. Q4 (69-70): one paragraph, 71-76. Q5 (81-82, p4): one paragraph,
#   83-91. No split, no mark inside any: model answers (10a).
# - Q6 (92-93): a requirement only, one paragraph 94-96 ("Úkolem je vlastními
#   slovy vysvětlit, proč nelze klasickou pohádku považovat za
#   „Teletubbies“, ...").
# - Criteria (p4, 97-102): "Poznámka: V částech 2 a 3 jsou odpovědi posuzovány
#   podle následujících kritérií:" -- Parts 2 AND 3 -- then "– 30 %." (98),
#   "– 30 %." (99-100), "– 30%." (101), "– 10 %." (102): 100 %.
# - Part II (103-105 reprint the head and the task): one paragraph of content
#   (106-108, "Kompilace názorů čtyř úspěšných režisérů, ..."), then a line of
#   its own, "Vlastními slovy, bez opsání frází z textu." (109).
# - Part III (p5, 114-119 reprint the head, the instruction and both titles):
#   one descriptive line only (120-121, "Jasně psaná kompozice, ...").
# SHAPES:
# - I2-I5: each one model paragraph, shown, whole=True on the printed 5 (10a).
# - I6: the requirement-only answer shown, whole=True on the printed 5.
# - II: graded (10b), 9 / 9 / 9 / 3 of 30; head the part's own requirement
#   line (109; no "Správný, plynulý komentář" line this sitting, as 2015); the
#   criteria's lead quoted; the paragraph quoted as examples (10a).
# - III1/III2: graded (10b), 12 / 12 / 12 / 4 of 40; head the descriptive line
#   (120-121); the criteria's lead quoted.
# JUDGEMENT CALLS:
# - The scheme's reprints of Q3 (ends "?", the paper ".") and Q4 ("že s
#   „originalitou", the paper "že „s originalitou") differ in punctuation
#   only; not quoted.
# - Part III title 2 is the two printed lines and the attribution (p4
#   y731-758), joined.
# - Reading text: pp2-4 (rendered: paragraph 11 and the byline are on p4, above
#   the questions). The live Q1 card's sourceMaterial.pages [2, 3, 4] AGREE
#   with the render.
# GLYPHS: none in either text layer; the rows match the rendered scheme.
# Lifted as printed: "něaký" (66, Q3's row), "ušišlaná" (85, Q5's row).

CRIT_2016 = crit(98, (99, 100), 101, 102)
LEAD_2016 = quote(S(97, after='Poznámka: '), lead='The scheme prints')
ESSAY_2016 = 'Napište esej'

SPECS[2016] = [
    R('I2', [shown(L(59, 62))], whole=True, total=PaperP(4, 'tím má na mysli.'), pages=(2, 3, 4)),
    R('I3', [shown(L(65, 68))], whole=True, total=PaperP(4, '3. Popište'), pages=(2, 3, 4)),
    R('I4', [shown(L(71, 76))], whole=True, total=PaperP(4, 'příliš uspět'), pages=(2, 3, 4)),
    R('I5', [shown(L(83, 91))], whole=True, total=PaperP(4, 'tak populární.'), pages=(2, 3, 4)),
    R('I6', [shown(L(94, 96))], whole=True, total=PaperP(4, '[5 bodů]'), pages=(2, 3, 4)),
    R('II', [graded(S(109), PARTP(), CRIT_2016)],
      rownote=both(LEAD_2016, examples(None, L(106, 108))), pages=(2, 3, 4)),
    R('III1', [graded(L(120, 121), PARTP(), CRIT_2016)], rownote=LEAD_2016,
      question=QP(4, ESSAY_2016, '1. Jestliže')),
    R('III2', [graded(L(120, 121), PARTP(), CRIT_2016)], rownote=LEAD_2016,
      question=QP(4, ESSAY_2016, Run('2. Svět', '(Fintan'))),
]


# ================================================================ 2017 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, cs-2017-hl-i-1); not
# touched.
# Paper (rendered pp2-4): the rule and "Část 1 [30 bodů]" (p2 y156) over the
# reading text "Nemyslím, tedy jsem" (unnumbered paragraphs) over pp2-3 to
# "(Linda Kholová, upraveno podle časopisu Instinkt)" (p3 y771); p4 holds the
# questions: Q1 "[5 bodů]" over a)-e) (live); Q2-Q6 "[5 bodů]" each; "Část 2
# [30 bodů]" (p4 y528), the commentary, ONE task with no number; "Část 3 [40
# bodů]" (p4 y636), the instruction and two titles.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply): every
# Q2-Q6 prints "[5 bodů]" in the right-hand cell of the question's own last
# line (rendered p4), PaperP: Q2 "2. Vysvětlete ..." (y235), Q3 "3. Popište
# ..." (y279), Q4 "workholismus. ..." (y345), Q5 "5. Proč ..." (y389), Q6
# "sobě.“ (odst. 1) ..." (y455). II: "Část 2 [30 bodů]" (PARTP); III1/III2:
# "Část 3 [40 bodů]" (PARTP). The scheme prints the same totals (107, 114).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4):
# - Q2 (63): one paragraph, 64-67. Q3 (68): one paragraph, 69-71. Q5 (89):
#   one paragraph, 90-94. No split, no mark inside: model answers (10a).
# - Q4 (72-73): one paragraph running over the p3/p4 break, 74-82 and 87-88
#   ("... Otázka k diskuzi" / "je, zda je to tak správně, ... Prostor pro
#   vlastní názor."; 83-85 are the page number and the page head, left out).
# - Q6 (95-96): a requirement only, one paragraph 97-100 ("Úkolem je vlastními
#   slovy vysvětlit, proč mohou být informace tak mocnou zbraní ...").
# - Criteria (p4, 101-106): "Poznámka: V částech 2 a 3 jsou odpovědi posuzovány
#   podle následujících kritérií:" -- Parts 2 AND 3 -- then "– 30 %." (102),
#   "– 30 %." (103-104), "– 30 %." (105), "– 10 %." (106): 100 %.
# - Part II (107-109 reprint the head and the task): one block, 110-112 ("Vlastní
#   názor na uvedené tvrzení, lze vyjádřit souhlas i nesouhlas, ... Cokoliv, co
#   se vymkne kontrole, ...") and its last line "Vlastními slovy, bez opsání
#   frází z textu." (113, a sentence on a line of its own).
# - Part III (114-120 reprint the head, the instruction and both titles): one
#   descriptive line only (121-122, "Jasně psaná kompozice, ...").
# SHAPES:
# - I2-I5: each one model paragraph, shown, whole=True on the printed 5 (10a).
# - I6: the requirement-only answer shown, whole=True on the printed 5.
# - II: graded (10b), 9 / 9 / 9 / 3 of 30; head the part's own requirement
#   line (113, as 2015 and 2016); the criteria's lead quoted; 110-112 quoted
#   as examples (10a).
# - III1/III2: graded (10b), 12 / 12 / 12 / 4 of 40; head the descriptive line
#   (121-122); the criteria's lead quoted.
# JUDGEMENT CALLS:
# - Q5: the scheme's reprint doubles a word ("Proč je pro náš mozek dostat
#   důležité dostat se ...", 89); Part III title 1's reprint prints "doobu"
#   (117) for the paper's "dobu"; Part II's reprint "100–150" for the paper's
#   "100-150". Reprints of the question only, the paper's words stand; not
#   quoted (no row depends on them). The lead may quote 89 on I5 under 10f.
# - Q4's row joins 74-82 and 87-88 (one paragraph over the page break).
# - Part III titles cut from the paper's wrapped lines (title 1 p4 y684-714,
#   title 2 y742-772).
# - Reading text: pp2-3 (rendered). The live Q1 card's sourceMaterial.pages
#   [2, 3] AGREE with the render.
# GLYPHS: none in either text layer; the rows match the rendered scheme.
# Lifted as printed: "využívajíci" (65, Q2's row), "jestě" (70, Q3's row),
# "činnosti pro činnost" and "pamět" (91-93, Q5's row).

CRIT_2017 = crit(102, (103, 104), 105, 106)
LEAD_2017 = quote(S(101, after='Poznámka: '), lead='The scheme prints')
ESSAY_2017 = 'Napište esej'

SPECS[2017] = [
    R('I2', [shown(L(64, 67))], whole=True, total=PaperP(4, '2. Vysvětlete'), pages=(2, 3)),
    R('I3', [shown(L(69, 71))], whole=True, total=PaperP(4, '3. Popište'), pages=(2, 3)),
    R('I4', [shown(J(L(74, 82), L(87, 88)))], whole=True, total=PaperP(4, 'workholismus.'), pages=(2, 3)),
    R('I5', [shown(L(90, 94))], whole=True, total=PaperP(4, '5. Proč'), pages=(2, 3)),
    R('I6', [shown(L(97, 100))], whole=True, total=PaperP(4, 'sobě.“'), pages=(2, 3)),
    R('II', [graded(S(113), PARTP(), CRIT_2017)],
      rownote=both(LEAD_2017, examples(None, L(110, 112))), pages=(2, 3)),
    R('III1', [graded(L(121, 122), PARTP(), CRIT_2017)], rownote=LEAD_2017,
      question=QP(4, ESSAY_2017, Run('1. Filozof', 'vlastní názor.'))),
    R('III2', [graded(L(121, 122), PARTP(), CRIT_2017)], rownote=LEAD_2017,
      question=QP(4, ESSAY_2017, Run('2. „Můj názor', 'média.'))),
]


# ================================================================ 2018 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, cs-2018-hl-i-1); not
# touched.
# Paper (rendered pp2-4): "ČESKÝ JAZYK 2018", the rule and "Část 1 [30 bodů]"
# (p2 y183) over the reading text "Vkus není jen o trendech. Má blízko k umění a
# dá se rozvíjet" (unnumbered paragraphs) over pp2-3 to "(Jana Syslová,
# upraveno podle idnes.cz)" (p3 y544); Q1 "1. Vysvětlete vlastními slovy: [5
# bodů]" over a)-e) on p3 (live); Q2-Q6 on p4, "[5 bodů]" each; "Část 2 [30
# bodů]" (p4 y382), the commentary, ONE task with no number; "Část 3 [40
# bodů]" (p4 y511), the instruction and two titles; a footnote at the foot of
# p4 (y718-741) glossing "udržitelnost", called from Q3.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q2, Q3, Q4, Q5: "[5 bodů]" at the end of the question's own last line
#   (rendered p4), PaperP: Q2 "2. Vysvětlete ..." (y65), Q3 "odstavec).
#   Domníváte ..." (y124), Q4 "textu. [5 bodů]" (y182), Q5 "5. Na základě ..."
#   (y226).
# - Q6: "[5 bodů]" on a line of its own (p4 x461 y285), the only line of p4
#   opening "[5 bodů]": PaperP(4, '[5 bodů]') (as 2016 Q6).
# - II: "Část 2 [30 bodů]" (PARTP); III1/III2: "Část 3 [40 bodů]" (PARTP).
#   The scheme prints the same "[5 bodů]" on each of Q2-Q6, "[30 bodů]" (124)
#   and "Část 3 [40 bodů]" (128).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5):
# - Q2 (64): one paragraph, 65-70 ("Podle definice je vkus schopnost posoudit
#   krásu, ..."). Q5 (97): one paragraph, 98-104. No split, no mark inside:
#   model answers (10a).
# - Q3 (71-73): one paragraph, 74-80, then a line of its own, "Prostor pro
#   vlastní názor." (81; rendered p3: set on its own line under "prostředí a
#   budoucí generace.").
# - Q4 (86-87, p4): one paragraph, 88-94, then two lines of their own, 95-96
#   ("Čím to je, že období socialismu ovlivnilo lidi ... Vždyť principálně se
#   jedná o politické zřízení."; rendered p4: a new line under "módou více
#   experimentovat.").
# - Q6 (105-106): a requirement only, one paragraph 107-109 ("Úkolem je
#   vlastními slovy vysvětlit svůj názor na toto tvrzení, ...").
# - Criteria (p4, 110-116): "Poznámka: V částech 2 a 3 jsou odpovědi posuzovány
#   podle následujících kritérií:" -- Parts 2 AND 3 -- then "– 30 %." (111),
#   "– 30 %." (112-113), "– 30" / "%." (114-115, the sign wrapped alone;
#   rendered p4), "– 10 %." (116): 100 %.
# - Part II (p5, 121-124 reprint the head and the task, "[30 bodů]"): one
#   paragraph of content (125-126, "Vlastní názor na uvedené tvrzení, lze
#   vyjádřit souhlas i nesouhlas, pomocí argumentů z textu i vlastní
#   zkušenosti."), then a line of its own, "Vlastními slovy, bez opsání frází z
#   textu." (127).
# - Part III (128-134 reprint the head, the instruction and both titles): one
#   descriptive line only (135-136, "Jasně psaná kompozice, ...").
# SHAPES:
# - I2, I5: each one model paragraph, shown, whole=True on the printed 5 (10a).
# - I3, I4: the model paragraph and the line(s) the scheme sets apart under it,
#   two shown rows each (as 2015 I5), whole=True on the printed 5.
# - I6: the requirement-only answer shown, whole=True on the printed 5.
# - II: graded (10b), 9 / 9 / 9 / 3 of 30; head the part's own requirement
#   line (127, as 2015-2017); the criteria's lead quoted; 125-126 quoted as
#   examples (10a).
# - III1/III2: graded (10b), 12 / 12 / 12 / 4 of 40; head the descriptive line
#   (135-136); the criteria's lead quoted.
# JUDGEMENT CALLS:
# - Criterion 3's percentage is wrapped ("– 30" / "%.", 114-115): read by the
#   lead's percent_of (UPDATE); crit span (114, 115).
# - Q3's question: the paper prints a superscript footnote mark on
#   "udržitelnost¹" (rendered p4 y109); the text layer reads it as a plain "1"
#   ("udržitelnost1 módy"). The question is cut around the mark from the same
#   printed line (QP cannot drop a mark inside a line), so it reads
#   "udržitelnost módy". The footnote itself (p4 y718-741) is not carded; if
#   the lead wants it on the card, it is the paper's own printed gloss of the
#   word and could ride as the card's stem (not done here).
# - Part III (10f): the paper prints "Napište esej (minimum 300 slov) na jedno
#   z následujících témat:" (p4 y532); the scheme reprints it with ", s
#   použitím argumentů proti a pro vyjádřete vlastní názor:" (129-130). The
#   paper's words are the question; the scheme's reprint quoted on the row.
# - The scheme's reprints of Q2 ("na základě text", the paper "textu") and of
#   Part II ("100–150", the paper "100-150") differ from the paper in question
#   text only; not quoted (no row depends on them).
# - Reading text: pp2-3 (rendered). The live Q1 card's sourceMaterial.pages
#   [2, 3] AGREE with the render.
# GLYPHS: none in either text layer; the rows match the rendered scheme.
# Lifted as printed: "nějaký dílo" (98, Q5's row), "i vkusu se dá" (104).

from sl_lib import clean_question  # noqa: E402

CRIT_2018 = crit(111, (112, 113), (114, 115), 116)
LEAD_2018 = quote(S(110, after='Poznámka: '), lead='The scheme prints')
ESSAY_2018 = 'Napište esej'
ESSAY_NOTE_2018 = both(LEAD_2018, quote(L(129, 130), lead='The scheme reprints the instruction as'))


def _q3_2018(d, _census=None):
    """Q3 as printed, cut around the footnote mark the text layer reads as a
    plain "1" after "udržitelnost" (p4 y109)."""
    return clean_question(J(PC(4, '3. V textu', after='3. ', before='1 módy'),
                            PC(4, '3. V textu', after='udržitelnost1'),
                            PL(4, 'odstavec).')).text(d))


SPECS[2018] = [
    R('I2', [shown(L(65, 70))], whole=True, total=PaperP(4, '2. Vysvětlete'), pages=(2, 3)),
    R('I3', [shown(L(74, 80)), shown(S(81))], whole=True, total=PaperP(4, 'odstavec).'),
      # second reader: the paper glosses "udržitelnost" in a footnote on the same page (p4 y718-741)
      rownote=lambda d: f'The paper glosses “udržitelnost” in a footnote: “{PC(4, "1 Udržitelnost", after="1 ").text(d)} '
                        f'{PL(4, "kompromitování schopnosti").text(d)} {PL(4, "společnost musí být").text(d)}”',
      question=_q3_2018, pages=(2, 3)),
    R('I4', [shown(L(88, 94)), shown(L(95, 96))], whole=True, total=PaperP(4, 'textu. [5'), pages=(2, 3)),
    R('I5', [shown(L(98, 104))], whole=True, total=PaperP(4, '5. Na základě'), pages=(2, 3)),
    R('I6', [shown(L(107, 109))], whole=True, total=PaperP(4, '[5 bodů]'), pages=(2, 3)),
    R('II', [graded(S(127), PARTP(), CRIT_2018)],
      rownote=both(LEAD_2018, examples(None, L(125, 126))), pages=(2, 3)),
    R('III1', [graded(L(135, 136), PARTP(), CRIT_2018)], rownote=ESSAY_NOTE_2018,
      question=QP(4, ESSAY_2018, Run('1. „Televize', 'Prodává'))),
    R('III2', [graded(L(135, 136), PARTP(), CRIT_2018)], rownote=ESSAY_NOTE_2018,
      question=QP(4, ESSAY_2018, Run('2. „Šaty', 'jeho oblečení?'))),
]


# ================================================================ 2019 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, cs-2019-hl-i-1); not
# touched.
# Paper (rendered pp2-4): "ČESKÝ JAZYK 2019", the rule and "Část 1 [30 bodů]"
# (p2 y168) over the reading text (urbex; headed paragraphs, among them "Zůstane
# jen fotka", p3 y527) over pp2-3 to "(Katka Havlíková, upraveno podle
# finmag.cz)" (p3 y742); p4 holds the questions: Q1 "1. Vysvětlete vlastními
# slovy: [5 bodů]" over a)-e) (live); Q2-Q6 "[5 bodů]" each; "Část 2 [30
# bodů]" (p4 y528), the commentary, ONE task with no number; "Část 3 [40
# bodů]" (p4 y631), the instruction and two titles.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q2, Q3, Q5, Q6: "[5 bodů]" at the end of the question's own last line
#   (rendered p4), PaperP: Q2 "2. Vysvětlete ..." (y223), Q3 "3. Vysvětlete
#   ..." (y270), Q5 "i společnost obecně." (y397), Q6 "toto tvrzení." (y460).
# - Q4: "[5 bodů]" on a line of its own (p4 x461 y334), the only line of p4
#   opening "[5 bodů]": PaperP(4, '[5 bodů]').
# - II: "Část 2 [30 bodů]" (PARTP); III1/III2: "Část 3 [40 bodů]" (PARTP).
#   The scheme prints the same "[5 bodů]" on each of Q2-Q6 and the same part
#   totals (105, 110).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4; answers in a smaller type):
# - Q2 (58): ONE sentence, 59-60, the definition ("Urbex je městský průzkum,
#   poznávání a dokumentace různých staveb, ... průzkum všeho, co vzniklo
#   lidskou rukou.").
# - Q3 (61-62): one paragraph, 63-65. No split, no mark inside: a model answer.
# - Q4 (66-67): 68-71, then 72-73 ("Zde je možnost se zamyslet i nad aspektem
#   udržitelnosti – ...") and 74-75 ("Dalším pohledem na urbex ..."), each
#   opening a new line (rendered p3). No mark inside.
# - Q5 (76-78): 79-82 (p3), then a second paragraph on p4, 87-90 ("Je nutno
#   přiznat, že urbex může mít i rizika ..."; 83-85 are the page number and
#   head), then a line of its own, "Prostor pro vlastní názor." (91).
# - Q6 (92-93): one paragraph 94-98, the requirement and model points in one
#   ("Úkolem je vlastními slovy vysvětlit svůj názor ... Vlastní vysvětlení:
#   vlastními slovy, bez opsání frází z textu.").
# - Criteria (p4, 99-104): "Poznámka: V částech 2 a 3 jsou odpovědi posuzovány
#   podle následujících kritérií:" -- Parts 2 AND 3 -- then "– 30 %." (100),
#   "– 30 %." (101-102), "– 30 %." (103), "– 10 %." (104): 100 %.
# - Part II (105-107 reprint the head and the task): one line of content
#   (108, "Vlastní názor na uvedené tvrzení, lze vyjádřit souhlas i
#   nesouhlas, ..."), then a line of its own, "Vlastními slovy, bez opsání
#   frází z textu." (109).
# - Part III (110-115 reprint the head, the instruction and both titles): one
#   descriptive line only (116-117, "Jasně psaná kompozice, ...").
# SHAPES:
# - I2: ONE stated answer (one definition, one sentence): one(row) at the
#   paper's 5, claimable (as the 2014 and 2015 I2 drafts).
# - I3: one model paragraph, shown, whole=True on the printed 5 (10a).
# - I4, I5: the model lines as the scheme sets them apart, one shown row each
#   (I4 three, I5 three), whole=True on the printed 5.
# - I6: the requirement-and-points paragraph shown, whole=True on the printed 5.
# - II: graded (10b), 9 / 9 / 9 / 3 of 30; head the part's own requirement
#   line (109, as 2015-2018); the criteria's lead quoted; 108 quoted as
#   examples (10a).
# - III1/III2: graded (10b), 12 / 12 / 12 / 4 of 40; head the descriptive line
#   (116-117); the criteria's lead quoted.
# JUDGEMENT CALLS:
# - I2 one() (claimable) rather than shown: the scheme states a single
#   definition, not a model paragraph. If the lead prefers every Czech Part I
#   answer self-assessed, flip to [shown(L(59, 60))], whole=True.
# - Part III (10f): the paper prints "Napište esej (minimum 300 slov) na jedno
#   z následujících témat:" (p4 y653); the scheme reprints it as "... témat: ,
#   s použitím argumentů pro a proti vyjádřete vlastní názor:" (111-112). The
#   paper's words are the question; the scheme's reprint quoted on the row.
# - The scheme's reprints of Part II ("100–150", the paper "100-150") and of
#   title 2 (the paper's second sentence set in brackets, lower case) differ
#   from the paper in punctuation only; not quoted.
# - Reading text: pp2-3 (rendered). The live Q1 card's sourceMaterial.pages
#   [2, 3] AGREE with the render.
# GLYPHS: none in either text layer; the rows match the rendered scheme.
# Lifted as printed (SEC typing, on the render): "výjímkou", "nekdo" (80-81,
# Q5's row), "sou velmi opatrní", "zazanamenávají", "zapomnutá" (96-97, Q6's
# row), "opuštěná místo mohou" (87-88).

CRIT_2019 = crit(100, (101, 102), 103, 104)
LEAD_2019 = quote(S(99, after='Poznámka: '), lead='The scheme prints')
ESSAY_2019 = 'Napište esej'
ESSAY_NOTE_2019 = both(LEAD_2019, quote(L(111, 112), lead='The scheme reprints the instruction as'))

SPECS[2019] = [
    R('I2', [one(L(59, 60), PaperP(4, '2. Vysvětlete'))], total=PaperP(4, '2. Vysvětlete'), pages=(2, 3)),
    R('I3', [shown(L(63, 65))], whole=True, total=PaperP(4, '3. Vysvětlete'), pages=(2, 3)),
    R('I4', [shown(L(68, 71)), shown(L(72, 73)), shown(L(74, 75))], whole=True,
      total=PaperP(4, '[5 bodů]'), pages=(2, 3)),
    R('I5', [shown(L(79, 82)), shown(L(87, 90)), shown(S(91))], whole=True,
      total=PaperP(4, 'i společnost obecně.'), pages=(2, 3)),
    R('I6', [shown(L(94, 98))], whole=True, total=PaperP(4, 'toto tvrzení.'), pages=(2, 3)),
    R('II', [graded(S(109), PARTP(), CRIT_2019)],
      rownote=both(LEAD_2019, examples(None, S(108))), pages=(2, 3)),
    R('III1', [graded(L(116, 117), PARTP(), CRIT_2019)], rownote=ESSAY_NOTE_2019,
      question=QP(4, ESSAY_2019, '1. „Návštěva')),
    R('III2', [graded(L(116, 117), PARTP(), CRIT_2019)], rownote=ESSAY_NOTE_2019,
      question=QP(4, ESSAY_2019, Run('2. Dát si', 'Vezměte ve svém'))),
]


# ================================================================ 2020 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, cs-2020-hl-i-1); not
# touched.
# Paper (rendered pp2-4): the rule and "Část 1 [30 bodů]" (p2 y148) over the
# reading text (clothing sizes) over pp2-3 to "(upraveno podle časopisu
# Instinkt)" (p3 y598); Q1 "1. Vysvětlete vlastními slovy: [5 bodů]" over
# a)-e) on p3 (live); Q2-Q6 on p4, "[5 bodů]" each; "Část 2 [30 bodů]" (p4
# y416), the commentary (a quotation, then the task), ONE task with no number;
# "Část 3 [40 bodů]" (p4 y595), the instruction and two titles.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q2: "[5 bodů]" on a line of its own (p4 x475 y102), the only line of p4
#   opening "[5 bodů]": PaperP(4, '[5 bodů]').
# - Q3-Q6: "[5 bodů]" at the end of the question's own last line (rendered
#   p4), PaperP: Q3 "tuto politiku?" (y145), Q4 "tato otázka považována ..."
#   (y202), Q5 "svůj vlastní názor ..." (y259), Q6 "třicátých let ..." (y316).
# - II: "Část 2 [30 bodů]" (PARTP); III1/III2: "Část 3 [40 bodů]" (PARTP).
#   The scheme prints the same "[5 bodů]" on each of Q2-Q6, "[30 bodů]" (108)
#   and "Část 3 [40 bodů]" (119).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5):
# - Q2 (58-59): one paragraph, 60-62. Q3 (63-64): one paragraph, 65-70. Q4
#   (71-72): one paragraph, 73-77. No split, no mark inside: model answers.
# - Q5 (82-83, p4): one paragraph, 84-89, then a line of its own, "Vlastní
#   názor: vlastními slovy, bez opisovaných frází z textu." (90; rendered p4).
# - Q6 (91-93): one paragraph, 94-96, then, after a blank line, "Vlastní
#   názor: vlastními slovy, bez opisování frází z textu." (97).
# - Criteria (p4, 98-103): "Poznámka: V částech 2 a 3 jsou odpovědi posuzovány
#   podle následujících kritérií:" -- Parts 2 AND 3 -- then "– 30 %." (99),
#   "– 30 %." (100-101), "– 30 %." (102), "– 10 %." (103): 100 %.
# - Part II (104-108 reprint the head, the quotation, the task and "[30
#   bodů]"): one paragraph of content (109-113, "Souhlas, nesouhlas. Mnoho
#   dívek a mladých žen má psychické problémy ..."), then a line of its own,
#   "Vlastní názor vlastními slovy, bez opisování frází z textu." (114).
# - Part III (p5, 119-122 reprint the head, the instruction and both titles):
#   one descriptive line only (123-124, "Jasně psaná kompozice, ...").
# SHAPES:
# - I2, I3, I4: each one model paragraph, shown, whole=True on the printed 5.
# - I5, I6: the model paragraph and the scheme's own requirement line under
#   it, two shown rows each (as 2015 I5), whole=True on the printed 5.
# - II: graded (10b), 9 / 9 / 9 / 3 of 30; head the part's own requirement
#   line (114); the criteria's lead quoted; 109-113 quoted as examples (10a).
# - III1/III2: graded (10b), 12 / 12 / 12 / 4 of 40; head the descriptive line
#   (123-124); the criteria's lead quoted.
# JUDGEMENT CALLS:
# - Q2's question is the census's text, which keeps the paper's printed "tex
#   tu" (rendered p4 y87: the SEC set a space inside "textu"; the scheme's
#   reprint, 58, prints "textu"). Lifted as printed, the paper's words being
#   the question; flagged for the lead (a crop or the scheme's spelling are the
#   alternatives).
# - III2 (10f): the paper prints "Lidé ukazují v době krize jak svoje
#   nejlepší tak i nejhorsi stranky." (rendered p4 y741: no háček or čárka on
#   "nejhorsi stranky"); the scheme reprints "... nejhorší stránky." (122).
#   The paper's title is the question; the scheme's reprint quoted on the row.
# - The scheme's reprint of Q6 sets U+2010 for the paper's "-" ("Jaký projekt
#   ‐ na základě textu ‐ ..."): question text only, not quoted.
# - Reading text: pp2-3 (rendered). The live Q1 card's sourceMaterial.pages
#   [2, 3] AGREE with the render.
# GLYPHS: none (the scheme's U+2010 HYPHEN in Q1's glosses and Q6's reprint is
# a real hyphen; its U+00A0 spaces are read as spaces). Lifted as printed:
# "být tak takhle hubený" (87, Q5's row), "aby ženy měli jistotu" (95-96).

CRIT_2020 = crit(99, (100, 101), 102, 103)
LEAD_2020 = quote(S(98, after='Poznámka: '), lead='The scheme prints')
ESSAY_2020 = 'Napište esej'

SPECS[2020] = [
    R('I2', [shown(L(60, 62))], whole=True, total=PaperP(4, '[5 bodů]'), pages=(2, 3)),
    R('I3', [shown(L(65, 70))], whole=True, total=PaperP(4, 'tuto politiku?'), pages=(2, 3)),
    R('I4', [shown(L(73, 77))], whole=True, total=PaperP(4, 'tato otázka'), pages=(2, 3)),
    R('I5', [shown(L(84, 89)), shown(S(90))], whole=True, total=PaperP(4, 'svůj vlastní názor'), pages=(2, 3)),
    R('I6', [shown(L(94, 96)), shown(S(97))], whole=True, total=PaperP(4, 'třicátých let'), pages=(2, 3)),
    R('II', [graded(S(114), PARTP(), CRIT_2020)],
      rownote=both(LEAD_2020, examples(None, L(109, 113))), pages=(2, 3)),
    R('III1', [graded(L(123, 124), PARTP(), CRIT_2020)], rownote=LEAD_2020,
      question=QP(4, ESSAY_2020, '1. Móda')),
    R('III2', [graded(L(123, 124), PARTP(), CRIT_2020)],
      rownote=both(LEAD_2020, quote(S(122, after='2. '), lead='The scheme reprints this title as')),
      question=QP(4, ESSAY_2020, '2. Lidé')),
]


# ================================================================ 2021 HL ===
# Drafted (small-languages lane, 20 Nov): the seven open asks of this sitting,
# I2-I6, II1, II2. Live: I1 (Q1 carded whole, cs-2021-hl-i-1); not touched.
# TWO-PART sitting: "Celkové hodnocení [70 bodů]" (p2 y100); "Část 1 (30
# bodů)" (p2 y142) and "Část 2 (40 bodů)" (p4 y370), the essay; no
# commentary. Keys II1/II2 are the essay's two titles (ruling B), cited
# Section II Q1/Q2.
# Paper (rendered pp2-4): the reading text (old children's games, Alice
# Kavková) over pp2-3 to "(Lucie Zídková, upraveno podle lidovky.cz)" (p3
# y580); Q1 "1. Vysvětlete vlastními slovy: [5 bodů]" over a)-e) on p3 (live);
# Q2-Q6 on p4, "[5 bodů]" each; Part 2 the instruction and two titles
# separated by "nebo".
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q2, Q3, Q5: "[5 bodů]" at the end of the question's own last line
#   (rendered p4), PaperP: Q2 "2. Vysvětlete ..." (y94), Q3 "zmiňovaných v
#   textu." (y153), Q5 "z generace na generaci ..." (y256).
# - Q4 and Q6: "[5 bodů]" on a line of its own (p4 x496 y212 and x496 y314):
#   TWO lines of p4 open "[5 bodů]", so each is read at its own height, PY(4,
#   212) and PY(4, 314).
# - II1/II2: "Část 2 (40 bodů)" (PARTP, 40). The scheme prints "Část 2 [40
#   bodů]" (109).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5):
# - Q2 (60-61): one paragraph, 62-64. No split, no mark inside: a model answer.
# - Q3 (65-66): ONE sentence, 67-68 ("Ptá se na staré hry všude, kde přijde,,
#   například i při návštěvě restaurace, kde vyzývá ostatní hosty, aby s ní
#   tyto hry hráli.").
# - Q4 (69-70): one paragraph running over the p3/p4 break, 71-73 and 78-81
#   (74-76 are the page number and the page head, left out).
# - Q5 (82-84, p4): one paragraph, 85-89, then a line of its own, "Prostor pro
#   vlastní názor." (90; rendered p4).
# - Q6 (91-92): one paragraph, 93-97, then a line of its own, "Vlastní
#   vysvětlení: vlastními slovy, bez opsání frází z textu." (98; rendered p4).
# - Criteria (p4, 99-104): "Poznámka: V částech 2 a 3 jsou odpovědi posuzovány
#   podle následujících kritérií:" and the four criteria WITH NO PERCENTAGES
#   (rendered p4: the lines end "s odpovědí", "a cílevědomý", "jasně a
#   plynule", "gramatika, pravopis"; nothing after them).
# - Part 2 (p5, 109-114 reprint the head, the instruction and both titles):
#   one descriptive line only (115-116, "Jasně psaná kompozice, ...").
# SHAPES:
# - I2: one model paragraph, shown, whole=True on the printed 5 (10a).
# - I3: ONE stated answer (one fact, one sentence): one(row) at the paper's 5,
#   claimable (as the 2014 and 2015 I2 drafts).
# - I4: one model paragraph over a page break, shown, whole=True on the 5.
# - I5, I6: the model paragraph and the scheme's own line under it, two shown
#   rows each, whole=True on the printed 5.
# - II1/II2: criteria printed for the essay part WITHOUT percentages (ruling
#   F; Bulgarian 2021): the four criteria as shown rows on the paper's 40
#   (questionTotal); the criteria's lead, the part's descriptive line and the
#   scheme's reprint of the instruction quoted.
# JUDGEMENT CALLS:
# - The criteria's lead names "části 2 a 3" in a sitting with no Part 3: the
#   only part it can serve here is Part 2, the essay, so the criteria are
#   taken as printed for it (quoted as printed on the row).
# - I3 one() (claimable) rather than shown: the scheme states a single fact.
#   Flip to [shown(L(67, 68))], whole=True if the lead prefers.
# - Scheme self-contradiction (10f), not on any row: the scheme heads Part 1
#   "Část 1 [40 bodů]" (48) beside "Celkem – 70 bodů" (47) and "Část 2 [40
#   bodů]" (109); the paper prints "Část 1 (30 bodů)" and six questions at 5
#   (30). Part 1's total prices no card here (each question is priced on its
#   own line), so it is recorded here only; the lead may quote it on the Q2
#   card's note.
# - Part 2 (10f): the paper prints "Napište esej (minimálně 300 slov) na jedno
#   z následujících témat:" (p4 y411); the scheme reprints "Napište esej
#   (minimum 300 slov) na jedno z následujících témat, s použitím argumentů
#   pro a proti vyjádřete vlastní názor:" (110-111). The paper's words are the
#   question; the scheme's reprint quoted on the row. Title 2's attribution
#   ("- Greta Thunberg", the scheme "(Greta Thunberg)") differs in punctuation
#   only; not quoted.
# - No `pages` on II1/II2: a two-part sitting's Part 2 is the essay.
#   Part I pages (2, 3): the text from p2 to its byline at p3 y580, Q1 below it
#   on p3; Q2-Q6 on p4. The live Q1 card's sourceMaterial.pages [2, 3] AGREE
#   with the render.
# GLYPHS: none (U+00A0 spaces in the scheme read as spaces). Lifted as printed
# (on the render): "Archeologie je veda" and "Alice Kafková" (62-63, Q2's row;
# the paper prints "Kavková"), "kde přijde,," (67, Q3's row), "v současné
# době máme" after "Paradox spočívá v tom," (85).

ESSAY_2021 = 'Napište esej'
CRIT_LINES_2021 = [S(100), L(101, 102), S(103), S(104)]


def _crit_note_2021(d):
    return (f'The scheme prints “{L(115, 116).text(d)}” Under “Poznámka:” it prints '
            f'“{S(99, after="Poznámka: ").text(d)}” and the four criteria, with no marks or percentages beside '
            f'them; the part is scored on its printed total. It reprints the instruction as '
            f'“{L(110, 111).text(d)}”')


SPECS[2021] = [
    R('I2', [shown(L(62, 64))], whole=True, total=PaperP(4, '2. Vysvětlete'), pages=(2, 3)),
    R('I3', [one(L(67, 68), PaperP(4, 'zmiňovaných'))], total=PaperP(4, 'zmiňovaných'), pages=(2, 3)),
    R('I4', [shown(J(L(71, 73), L(78, 81)))], whole=True, total=PY(4, 212), pages=(2, 3)),
    R('I5', [shown(L(85, 89)), shown(S(90))], whole=True, total=PaperP(4, 'z generace'), pages=(2, 3)),
    R('I6', [shown(L(93, 97)), shown(S(98))], whole=True, total=PY(4, 314), pages=(2, 3)),
    R('II1', [shown(c) for c in CRIT_LINES_2021], whole=True, total=PARTP(), rownote=_crit_note_2021,
      question=QP(4, ESSAY_2021, '1. Kdo si')),
    R('II2', [shown(c) for c in CRIT_LINES_2021], whole=True, total=PARTP(), rownote=_crit_note_2021,
      question=QP(4, ESSAY_2021, '2. „Nemůžete')),
]


# ================================================================ 2022 HL ===
# Drafted (small-languages lane, 20 Nov): the seven open asks of this sitting,
# I2-I6, II1, II2. Live: I1 (Q1 carded whole, cs-2022-hl-i-1); not touched.
# TWO-PART sitting: "Celkové hodnocení [70 bodů]" (p2 y103); "Část 1 [30
# bodů]" (p2 y146) and "Část 2 [40 bodů]" (p4 y541), the ESSAY ("Napište esej
# (minimum 300 slov) ...", two titles separated by "nebo"); no commentary.
# The exclusions file calls II1/II2 a "commentary": wrong, both are essay
# titles (rendered p4). Keys II1/II2, cited Section II Q1/Q2 (ruling B).
# Paper (rendered pp2-4): the reading text (re-watching series; numbered
# paragraphs, "6. Co tedy hraje ..." at p3 y65) over pp2-3 to "(upraveno podle
# Denikn.cz)" (p3 y657); p4 holds the questions: Q1 "1. Vysvětlete vlastními
# slovy: [5 bodů]" over a)-e) (live); Q2-Q6 "[5 bodů]" each.
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q2, Q4, Q5, Q6: "[5 bodů]" at the end of the question's own last line
#   (rendered p4), PaperP: Q2 "2. Vysvětlete ..." (y227), Q4 "odpověď dává
#   autor ..." (y328), Q5 "vysvětlete svůj názor ..." (y382), Q6 "k postavám.“
#   (odstavec 10) [5 bodů]" (y446; the reader takes the "5 bodů", not the
#   paragraph number).
# - Q3: "[5 bodů]" on a line of its own (p4 x468 y285), the only line of p4
#   opening "[5 bodů]": PaperP(4, '[5 bodů]').
# - II1/II2: "Část 2 [40 bodů]" (PARTP, 40). The scheme prints the same (119).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5):
# - Q2 (63): ONE sentence, 64-65, the meaning ("Jedná se o návrat do bezpečí,
#   když žijeme v nejisté době ... co nám dává pocit jistoty.").
# - Q3 (66-68): one paragraph, 69-73, then a line of its own, "Možnost přidat
#   vlastní zkušenost: dětská kniha čtená pořád dokola, seriál v dětství
#   apod." (74-75).
# - Q4 (76-78; the reprint drops the opening „): one paragraph on p4, 83-89,
#   then "Souhlas – nesouhlas, vlastní názor, vlastní zkušenost." (90).
# - Q5 (91-93): one paragraph, 94-96, then "Prostor pro vlastní názor, vlastní
#   zkušenost., souhlas – nesouhlas." (97).
# - Q6 (98-99): one paragraph, 100-107, then "Vlastní vysvětlení: vlastními
#   slovy, bez opsání frází z textu. Vlastní zkušenost." (108).
# - Criteria (p4, 109-114): "Poznámka: V části 2 jsou odpovědi posuzovány podle
#   následujících kritérií:" -- Part 2, the essay, by name -- and the four
#   criteria WITH NO PERCENTAGES (rendered p4: nothing after "s odpovědí", "a
#   cílevědomý", "jasně a plynule", "gramatika, pravopis").
# - Part 2 (p5, 119-123 reprint the head, the instruction, both titles and
#   "nebo"): one descriptive line only (124-125, "Jasně psaná kompozice, ...").
# SHAPES:
# - I2: ONE stated answer (one meaning, one sentence): one(row) at the paper's
#   5, claimable (as the 2014 and 2015 I2 drafts).
# - I3-I6: the model paragraph and the scheme's own line under it, two shown
#   rows each, whole=True on the printed 5 (10a).
# - II1/II2: criteria printed for the essay part WITHOUT percentages (ruling
#   F; Bulgarian 2021): the four criteria as shown rows on the paper's 40
#   (questionTotal); the criteria's lead and the part's descriptive line
#   quoted.
# JUDGEMENT CALLS:
# - I2 one() (claimable) rather than shown: the scheme states a single
#   meaning. Flip to [shown(L(64, 65))], whole=True if the lead prefers.
# - Q2's question is the census's text, which keeps the paper's printed
#   "znamenená" (rendered p4 y227; the scheme's reprint, 63, prints "znamená").
#   Lifted as printed; flagged.
# - Q6's row (100-107) opens a bracket at "(často se hercům ..." (104) and
#   never closes it (rendered p4): lifted as printed.
# - Reading text: pp2-3 (rendered). No `pages` on II1/II2 (the essay). The live
#   Q1 card's sourceMaterial.pages [2, 3] AGREE with the render.
# GLYPHS: none ("Søren Kierkegaard", p2, is a real ø; U+00A0 spaces in the
# scheme read as spaces). Lifted as printed: "Velmi významem důvodem" (88, Q4's
# row), "vlastní zkušenost., souhlas" (97).

ESSAY_2022 = 'Napište esej'
CRIT_LINES_2022 = [S(110), L(111, 112), S(113), S(114)]


def _crit_note_2022(d):
    return (f'The scheme prints “{L(124, 125).text(d)}” Under “Poznámka:” it prints '
            f'“{S(109, after="Poznámka: ").text(d)}” and the four criteria, with no marks or percentages beside '
            f'them; the part is scored on its printed total.')


SPECS[2022] = [
    R('I2', [one(L(64, 65), PaperP(4, '2. Vysvětlete'))], total=PaperP(4, '2. Vysvětlete'), pages=(2, 3)),
    R('I3', [shown(L(69, 73)), shown(L(74, 75))], whole=True, total=PaperP(4, '[5 bodů]'), pages=(2, 3)),
    R('I4', [shown(L(83, 89)), shown(S(90))], whole=True, total=PaperP(4, 'odpověď dává'), pages=(2, 3)),
    R('I5', [shown(L(94, 96)), shown(S(97))], whole=True, total=PaperP(4, 'vysvětlete svůj'), pages=(2, 3)),
    R('I6', [shown(L(100, 107)), shown(S(108))], whole=True, total=PaperP(4, 'k postavám.'), pages=(2, 3)),
    R('II1', [shown(c) for c in CRIT_LINES_2022], whole=True, total=PARTP(), rownote=_crit_note_2022,
      question=QP(4, ESSAY_2022, '1. „…štěstí')),
    R('II2', [shown(c) for c in CRIT_LINES_2022], whole=True, total=PARTP(), rownote=_crit_note_2022,
      question=QP(4, ESSAY_2022, '2. Jak vzniká')),
]


# ================================================================ 2023 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, cs-2023-hl-i-1); not
# touched.
# Paper (rendered pp2-4): "Celkové hodnocení [100 bodů]", the rule and "Část 1
# [30 bodů]" (p2 y168) over the reading text (media education; numbered
# paragraphs, "6. Proč si mediální výchova ..." at p3 y64) over pp2-3 to
# "(upraveno podle www.forum24.cz)" (p3 y542); Q1 "1. Vysvětlete vlastními
# slovy: [5 bodů]" over a)-e) on p3 (live); Q2-Q6 on p4, "[5 bodů]" each;
# "Část 2 [30 bodů]" (p4 y428), the commentary, ONE task with no number;
# "Část 3 [40 bodů]" (p4 y553), the instruction and two titles separated by
# "nebo".
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q2, Q4, Q5: "[5 bodů]" at the end of the question's own last line
#   (rendered p4), PaperP: Q2 "2. Vysvětlete ..." (y65), Q4 "4. Na základě
#   ..." (y152), Q5 "problémy mohly být vyřešeny?" (y216).
# - Q3 and Q6: "[5 bodů]" on a line of its own (p4 x482 y129 and x482 y315):
#   TWO lines of p4 open "[5 bodů]", so each is read at its own height, PY(4,
#   129) and PY(4, 315).
# - II: "Část 2 [30 bodů]" (PARTP); III1/III2: "Část 3 [40 bodů]" (PARTP).
#   The scheme prints the same "[5 bodů]" on each of Q2-Q6 and the same part
#   totals (106, 111).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4; set in no-break spaces):
# - Q2 (63): one paragraph, 64-66 (what RVP stands for, then what the
#   programmes define). Q3 (67-68): one paragraph, 69-74. Q4 (75): one
#   paragraph, 76-80. No split, no mark inside: model answers (10a).
# - Q5 (85-87, p4): one paragraph, 88-91, then a line of its own, "Prostor pro
#   vlastní názor, vlastní zkušenost." (92).
# - Q6 (93-95; the reprint doubles "Napište vlastní názor na tvrzení z
#   textu:"): one paragraph, 96-98, then "Vlastní vysvětlení: vlastními slovy,
#   bez opsání frází z textu. Vlastní zkušenost." (99).
# - Criteria (p4, 100-105): "Poznámka: V částech 2 a 3 jsou odpovědi posuzovány
#   podle následujících kritérií:" -- Parts 2 AND 3 -- then "– 30 %." (101),
#   "– 30 %." (102-103), "– 30 %." (104), "– 10 %." (105): 100 %.
# - Part II (106-108 reprint the head and the task): one line of content
#   (109, "Vlastní názor na uvedené tvrzení, lze vyjádřit souhlas i
#   nesouhlas, ..."), then a line of its own, "Vlastními slovy, bez opsání
#   frází z textu." (110).
# - Part III (111-115 reprint the head, the instruction, both titles and
#   "Nebo"): one descriptive line only (116-117, "Jasně psaná kompozice,
#   ...").
# SHAPES:
# - I2, I3, I4: each one model paragraph, shown, whole=True on the printed 5.
# - I5, I6: the model paragraph and the scheme's own line under it, two shown
#   rows each, whole=True on the printed 5.
# - II: graded (10b), 9 / 9 / 9 / 3 of 30; head the part's own requirement
#   line (110); the criteria's lead quoted; 109 quoted as examples (10a).
# - III1/III2: graded (10b), 12 / 12 / 12 / 4 of 40; head the descriptive line
#   (116-117); the criteria's lead quoted.
# JUDGEMENT CALLS:
# - I2 shown, not one(): the answer is two statements (what the abbreviation
#   stands for, and what the programmes define), the question asks for both.
# - The scheme's reprints differ from the paper in question text only, not
#   quoted: Q6's doubled lead-in (93), title 1 set in quotation marks (113),
#   title 2 without its closing quotation mark (115), Part II's "100‐150"
#   (U+2010).
# - Reading text: pp2-3 (rendered). The live Q1 card's sourceMaterial.pages
#   [2, 3] AGREE with the render.
# GLYPHS: none (U+00A0 spaces read as spaces; U+2010 in "e‐mail" (47) and
# "100‐150" (107) is a real hyphen). Lifted as printed: "orientovat v
# mediálních obsazích" (77, Q4's row), "extremističtí populisté slibují" (97-98,
# Q6's row).

CRIT_2023 = crit(101, (102, 103), 104, 105)
LEAD_2023 = quote(S(100, after='Poznámka: '), lead='The scheme prints')
ESSAY_2023 = 'Napište esej'

SPECS[2023] = [
    R('I2', [shown(L(64, 66))], whole=True, total=PaperP(4, '2. Vysvětlete'), pages=(2, 3)),
    R('I3', [shown(L(69, 74))], whole=True, total=PY(4, 129), pages=(2, 3)),
    R('I4', [shown(L(76, 80))], whole=True, total=PaperP(4, '4. Na základě'), pages=(2, 3)),
    R('I5', [shown(L(88, 91)), shown(S(92))], whole=True, total=PaperP(4, 'problémy mohly'), pages=(2, 3)),
    R('I6', [shown(L(96, 98)), shown(S(99))], whole=True, total=PY(4, 315), pages=(2, 3)),
    R('II', [graded(S(110), PARTP(), CRIT_2023)],
      rownote=both(LEAD_2023, examples(None, S(109))), pages=(2, 3)),
    R('III1', [graded(L(116, 117), PARTP(), CRIT_2023)], rownote=LEAD_2023,
      question=QP(4, ESSAY_2023, '1. Vítězná')),
    R('III2', [graded(L(116, 117), PARTP(), CRIT_2023)], rownote=LEAD_2023,
      question=QP(4, ESSAY_2023, '2. „Pravda')),
]


# ================================================================ 2024 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, cs-2024-hl-i-1); not
# touched.
# Paper (rendered pp2-4): "Celkové hodnocení [100 bodů]", the rule and "Část 1
# [30 bodů]" (p2 y168) over the reading text (the Moon; numbered paragraphs,
# "6. Měsíc má vliv ..." at p3 y64) over pp2-3 to "(upraveno podle časopisu
# Téma)" (p3 y710); p4 holds the questions: Q1 "1. Vysvětlete vlastními slovy:
# [5 bodů]" over a)-e) (live); Q2-Q6 "[5 bodů]" each; "Část 2 [30 bodů]" (p4
# y520), the commentary, ONE task with no number; "Část 3 [40 bodů]" (p4
# y623), the instruction and two titles separated by "nebo".
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q2, Q4, Q5, Q6: "[5 bodů]" at the end of the question's own last line
#   (rendered p4), PaperP: Q2 "2. Vysvětlete ..." (y225), Q4 "specifický
#   příklad." (y343), Q5 "5. Vysvětlete ..." (y391), Q6 "od našich prapředků
#   ..." (y452).
# - Q3: "[5 bodů]" on a line of its own (p4 x482 y304), the only line of p4
#   opening "[5 bodů]": PaperP(4, '[5 bodů]').
# - II: "Část 2 [30 bodů]" (PARTP); III1/III2: "Část 3 [40 bodů]" (PARTP).
#   The scheme prints the same "[5 bodů]" after each answer and the same part
#   totals (97, 110).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4): this year the answer RUNS ON
# from the reprinted question on the same line, and "[5 bodů]" closes the
# answer (60, 66, 72, 80, 96). Each row is cut after the reprinted question's
# last words and before the price:
# - Q2 (56-60): one paragraph, from "Slunce se z jedné třetiny podílí ..." to
#   "... o „skočném“ přílivu."
# - Q3 (61-66): one paragraph, from "Měsíční fáze se dají dobře sledovat ..."
#   to "... to umožňovala."
# - Q4 (67-72): one paragraph, from "Během střídání přílivu a odlivu ..." to
#   "... střídání dne a noci."
# - Q5 (73-80): one paragraph, from "Lunární cyklus je jakýsi vnitřní
#   biologický režim ..." to "... jak to funguje."
# - Q6 (85-96, p4): one paragraph, from "Cirkadiánní rytmy jsou jakési vnitřní
#   biologické hodiny ..." to "... postupně přizpůsobí." (its own "– Zde je
#   možnost vyjádřit názor na toto zjištění." inside it).
# - NO criteria anywhere in this scheme (rendered pp3-6: no "Poznámka", no
#   percentages).
# - Part II (97-99 reprint the head and the task): "V odpovědi je možno zvážit
#   například následující body:" (100) over seven dashed points (101-107), then
#   "Vyjádřit vlastní názor na uvedené tvrzení, vlastními slovy, pomocí
#   argumentů z textu i vlastní zkušenosti." (108-109).
# - Part III (110-114): the head, the instruction, both titles and "nebo" --
#   and nothing under them (rendered p4: the page ends at title 2; pp5-6
#   blank).
# SHAPES:
# - I2-I6: each one model paragraph, shown, whole=True on the printed 5 (10a).
# - II: an indicative list the scheme heads "například" (for example), no mark
#   on any point, no criteria: the seven points and the requirement line as
#   shown rows on the paper's 30 (questionTotal; 10a, as Croatian 2026 II1),
#   the heading quoted and labelled as examples.
# - III1/III2: nothing printed for the part -> unprinted (ruling 4) at the
#   paper's 40, the note saying what the scheme does print.
# JUDGEMENT CALLS:
# - II: shown rows rather than unprinted: the scheme prints content for this
#   part (an indicative list), so 10a applies, not R4.
# - III1 (10f): the paper prints "Ztrácíme v našem digitálním světě kontakt s
#   přírodou?" (p4 y691); the scheme reprints "... digitalizovaném světě ..."
#   (112). The paper's title is the question; the scheme's reprint quoted.
# - The scheme's reprints of Q3 ("Měsíce, a uveďte", the paper "Měsíce a
#   uveďte") and Part II ("100‐150") differ in punctuation only; not quoted.
# - Reading text: pp2-3 (rendered). The live Q1 card's sourceMaterial.pages
#   [2, 3] AGREE with the render.
# GLYPHS: none (U+00A0 spaces read as spaces; U+2010 in the dashed points and
# "100‐150" is a real hyphen, taken off the points as their bullet). Lifted as
# printed: "více vyditelný" (64, Q3's row), "Naši prapředci byly" (88, Q6's
# row).

ESSAY_2024 = 'Napište esej'


def _points_2024(d):
    return (f'The scheme heads the points “{S(100).text(d)}” They are examples, not a checklist; '
            f'none carries a mark of its own, and the scheme prints no criteria for the part.')


def _essay_2024(d):
    return ('The scheme reprints the part\'s head, the instruction and the two titles, and prints nothing '
            'under them: no criteria, no descriptive line and no split of the part\'s marks.')


SPECS[2024] = [
    R('I2', [shown(L(56, 60, after='a odlivu. ', before=' [5'))], whole=True,
      total=PaperP(4, '2. Vysvětlete'), pages=(2, 3)),
    R('I3', [shown(L(62, 65, after='důležitá. '))], whole=True, total=PaperP(4, '[5 bodů]'), pages=(2, 3)),
    R('I4', [shown(L(68, 72, after='příklad. ', before=' [5'))], whole=True,
      total=PaperP(4, 'specifický příklad.'), pages=(2, 3)),
    R('I5', [shown(L(73, 80, after='náměsíčností. ', before=' [5'))], whole=True,
      total=PaperP(4, '5. Vysvětlete'), pages=(2, 3)),
    R('I6', [shown(L(86, 96, after='rytmy. ', before=' [5'))], whole=True,
      total=PaperP(4, 'od našich'), pages=(2, 3)),
    R('II', [shown(S(n)) for n in range(101, 108)] + [shown(L(108, 109))], whole=True, total=PARTP(),
      rownote=_points_2024, pages=(2, 3)),
    R('III1', [unprinted(both(_essay_2024, quote(S(112, after='1. '), lead='It reprints this title as')))],
      question=QP(4, ESSAY_2024, '1. Ztrácíme')),
    R('III2', [unprinted(_essay_2024)],
      question=QP(4, ESSAY_2024, '2. „Na světě')),
]


# ================================================================ 2025 HL ===
# Drafted (small-languages lane, 20 Nov): every ask of this sitting, I1a-I1e,
# I2-I6, II, III1, III2. No live 2025 card.
# Paper (rendered pp2-4): "Celkové hodnocení [100 bodů]", the rule and "Část 1
# [30 bodů]" (p2 y190) over the reading text (financial literacy; numbered
# paragraphs 1-12, the Q1 expressions set in bold in it) over pp2-3 to
# "(Upraveno podle aktualne.cz)" (p3 y575, at the end of paragraph 12's last
# line); Q1 on p3 (y624): "1. Vysvětlete vlastními slovy:" over a)-e), and
# "[5 × 1 bod]" at the right-hand end of the e) line (p3 y740; rendered: the
# only price under Q1, set level with e)); Q2-Q6 on p4, "[5 bodů]" each; "Část
# 2 [30 bodů]" (p4 y423), the commentary, ONE task with no number; "Část 3 [40
# bodů]" (p4 y591), the instruction and two titles separated by "nebo".
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply):
# - Q1: "[5 × 1 bod]" = ONE MARK FOR EACH EXPRESSION, five expressions, 5 in
#   all: the paper prints a mark per expression, so Q1 is carded PER LETTER
#   (brief: "if the paper prints per-expression marks that add to the whole,
#   card per letter"), each at 1, read with PaperP(3, 'e) „vzdělávací') (the
#   reader takes the "1 bod"; the "5 ×" is the count). The scheme prints no
#   price for Q1 (59: "1. Vysvětlete vlastními slovy:" alone).
# - Q2, Q4, Q5, Q6: "[5 bodů]" at the end of the question's own last line
#   (rendered p4), PaperP: Q2 "2. Co je to ..." (y65), Q4 "důležitější než
#   ..." (y191), Q5 "předmětem? Uveďte ..." (y270), Q6 "propojeny." (y333).
# - Q3: "[5 bodů]" on a line of its own (p4 x454 y127), the only line of p4
#   opening "[5 bodů]": PaperP(4, '[5 bodů]').
# - II: "Část 2 [30 bodů]" (PARTP); III1/III2: "Část 3 [40 bodů]" (PARTP).
#   The scheme prints "[5 bodů]" on each of Q2-Q6 and the same part totals
#   (122, 126).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-6; p3 is the SEC's table of
# marking annotations):
# - Q1 (59): a) to e), each the expression in quotation marks, a dash and its
#   gloss: a) 60-62, b) 63-66, c) 67-68, d) 69-71, e) 72-73 (e) prints no
#   space before its dash: "„vzdělávací mezera“– nedostatek ...").
# - Q2 (74): one paragraph, 75-79 (what the "pink tax" is, then the article's
#   example). Q3 (80): one paragraph, 81-85. No split, no mark inside.
# - Q4 (90-92, p5): one paragraph, 93-95, then a line of its own, "Vyjádřete
#   vlastní názor, vlastní zkušenost." (96).
# - Q5 (97-100): one paragraph, 101-104, then a second (105-108, "Prostor pro
#   vlastní názor, vlastní zkušenost, souhlas (...) – nesouhlas (...).").
# - Q6 (109-110): "Body, které by neměly v odpovědi chybět:" (111) over five
#   dashed points (112-117), no mark on any.
# - NO criteria anywhere in this scheme (rendered pp3-8: no "Poznámka", no
#   percentages).
# - Part II (p6, 122-125): the head and the task reprinted, and NOTHING under
#   them (rendered p6: "Část 3" follows directly).
# - Part III (126-131 reprint the head, the instruction, both titles and
#   "nebo"): one descriptive line only (132-133, "Jasně psaná kompozice,
#   ...").
# SHAPES:
# - I1a-I1e: one stated answer each (the gloss, cut after the expression and
#   its dash) -> one(row) at the paper's 1, claimable; the paper's "[5 × 1
#   bod]" quoted on each row.
# - I2, I3: one model paragraph each, shown, whole=True on the printed 5 (10a).
# - I4, I5: the model paragraph and the scheme's own requirement paragraph,
#   two shown rows each, whole=True on the printed 5.
# - I6: the five points as shown rows, whole=True on the printed 5, their
#   heading quoted (the scheme gives no point a mark).
# - II: nothing printed for the part -> unprinted (ruling 4) at the paper's 30.
# - III1/III2: only a descriptive line -> unprinted (ruling 4) at the paper's
#   40, the descriptive line quoted.
# JUDGEMENT CALLS:
# - Q1 per letter, NOT whole at I1: the brief's own test ("[5 × 1 bod]" is a
#   printed mark for each expression). Note for the lead: 2026 prints the same
#   "[5 × 1 bod]" (p3 y633) and its scheme "[5 x 1 bod]" (60), yet the LIVE
#   2026 Q1 card (cs-2026-hl-i-1) is carded whole (questionTotal 5); the two
#   sittings now differ in shape.
# - I6: the scheme's heading says the points "should not be missing" from the
#   answer, so they are quoted as the scheme's own points (not labelled as
#   examples); still shown, not claimable, because no point carries a mark.
# - Q3's question is the PAPER's ("Na základě textu uveďte, jaký je hlavní cíl
#   ..."); the scheme reprints it shorter ("Jaký je hlavní cíl ...", 80).
#   Question text only; not quoted.
# - Part III titles: the scheme drops each title's closing quotation mark
#   (128, 130); punctuation only, not quoted.
# - Reading text: pp2-3 (rendered: the text from p2 y190 to the source line at
#   p3 y575; Q1 below it on p3). No live 2025 card to compare.
# GLYPHS: none in either text layer (Czech letters and punctuation only).
# Printed as such on the render (SEC typing), lifted as printed: "skupinu
# lidi" (67, c)), "vzdělávaní" (69, d), as the paper prints it), "ze jejich
# aktivita", "domu" (83-85, Q3's row), "Vetší", "prakticky život" (94-95, Q4's
# row), "ze to není", "duležité", "žadnou", "ve skole" (105-108, Q5's row),
# "Propojeni", "byt vyučován" (112-114, Q6's points).

ESSAY_2025 = 'Napište esej'
Q1P_2025 = PaperP(3, 'e) „vzdělávací')


def _q1_2025(d):
    return (f'The paper prices Question 1 “{PC(3, "e) „vzdělávací", after="mezera“ ").text(d)}”: one mark for '
            f'each of its five expressions.')


def _points_2025(d):
    return f'The scheme heads the points “{S(111).text(d)}” None carries a mark of its own.'


def _commentary_2025(d):
    return ('The scheme reprints the part\'s head and the task, and prints nothing under them: no answer, no '
            'criteria and no split of the part\'s marks.')


def _essay_2025(d):
    return (f'The scheme reprints the part\'s head, the instruction and the two titles; under them it prints only '
            f'“{L(132, 133).text(d)}” It prints no criteria and no split of the part\'s marks.')


SPECS[2025] = [
    R('I1a', [one(L(60, 62, after='„gramotnost“ – '), Q1P_2025)], total=Q1P_2025, rownote=_q1_2025, pages=(2, 3)),
    R('I1b', [one(L(63, 66, after='„kapesné“ – '), Q1P_2025)], total=Q1P_2025, rownote=_q1_2025, pages=(2, 3)),
    R('I1c', [one(L(67, 68, after='„koordinátor“ – '), Q1P_2025)], total=Q1P_2025, rownote=_q1_2025,
      pages=(2, 3)),
    R('I1d', [one(L(69, 71, after='vzdělávaní“ – '), Q1P_2025)], total=Q1P_2025, rownote=_q1_2025,
      pages=(2, 3)),
    R('I1e', [one(L(72, 73, after='mezera“– '), Q1P_2025)], total=Q1P_2025, rownote=_q1_2025, pages=(2, 3)),
    R('I2', [shown(L(75, 79))], whole=True, total=PaperP(4, '2. Co je to'), pages=(2, 3)),
    R('I3', [shown(L(81, 85))], whole=True, total=PaperP(4, '[5 bodů]'), pages=(2, 3),
      rownote=quote(S(80, after='3. ', before=' [5'), lead='The scheme reprints this question as')),
    R('I4', [shown(L(93, 95)), shown(S(96))], whole=True, total=PaperP(4, 'důležitější'), pages=(2, 3)),
    R('I5', [shown(L(101, 104)), shown(L(105, 108))], whole=True, total=PaperP(4, 'předmětem?'), pages=(2, 3)),
    R('I6', [shown(L(112, 113)), shown(S(114)), shown(S(115)), shown(S(116)), shown(S(117))], whole=True,
      total=PaperP(4, 'propojeny.'), rownote=_points_2025, pages=(2, 3)),
    R('II', [unprinted(_commentary_2025)], pages=(2, 3)),
    R('III1', [unprinted(_essay_2025)], question=QP(4, ESSAY_2025, '1. „Peníze')),
    R('III2', [unprinted(_essay_2025)], question=QP(4, ESSAY_2025, '2. „Všichni')),
]


# ================================================================ 2026 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I2-I6, II, III1, III2. Live: I1 (Q1 carded whole, cs-2026-hl-i-1); not
# touched.
# Paper (rendered pp2-4): "Celkové hodnocení [100 bodů]", the rule and "Část 1
# [30 bodů]" (p2 y168) over the reading text (Czech readers and books;
# numbered paragraphs, "6. Autoři zdůrazňují ..." at p3 y152) over pp2-3 to
# "(upraveno podle seznamzprávy.cz, Tomáš Svoboda)" (p3 y603, at the end of
# the last paragraph's line); Q1 "1. Vysvětlete vlastními slovy: [5 × 1 bod]"
# over a)-e) on p3 (live); Q2-Q6 on p4, "[5 bodů]" each; "Část 2 [30 bodů]"
# (p4 y392), the commentary, ONE task with no number; "Část 3 [40 bodů]" (p4
# y567), the instruction and two titles separated by "nebo".
# PRICES (the lt walker reads no per-ask price, so PP() cannot apply): every
# Q2-Q6 prints "[5 bodů]" at the end of the question's own last line
# (rendered p4), PaperP: Q2 "2. Jak se ..." (y65), Q3 "3. Vysvětlete ..."
# (y113), Q4 "základě textu. [5 bodů]" (y176), Q5 "tvrzením? Vysvětlete ..."
# (y240), Q6 "vlastní názor. [5 bodů]" (y303). II: "Část 2 [30 bodů]"
# (PARTP); III1/III2: "Část 3 [40 bodů]" (PARTP). The scheme prints the same
# "[5 bodů]" on each of Q2-Q6 and the same part totals (115, 122).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-6; p3 is the SEC's table of
# marking annotations):
# - Q2 (82): one paragraph, 83-85 (the statistics, the reason, the rise in
#   non-readers). Q3 (90, p5): one sentence, 91-92, three statements (deep
#   reading needs concentration; about 15 minutes to get into a book; many
#   lack the patience). Q4 (93-94): one paragraph, 95-100. No split, no mark
#   inside: model answers (10a).
# - Q5 (101-103): one paragraph, 104-105 ("Prostor pro vlastní názor za
#   použití argumentů z textu. Potřebujeme knihy ke svému životu? Nebo se
#   obejdeme bez nich a vystačíme si s internetem?").
# - Q6 (106-107): one paragraph, 108-110 ("Prostor pro vlastní názor na základě
#   informací z textu. ... Vlastní vysvětlení: vlastními slovy, bez opsání
#   frází z textu. Vlastní zkušenost.").
# - NO criteria anywhere in this scheme (rendered pp3-8: no "Poznámka", no
#   percentages).
# - Part II (p6, 115-118 reprint the head and the task): one paragraph of
#   content (119-120, "Vlastní názor na uvedené tvrzení, lze vyjádřit
#   souhlas i nesouhlas, pomocí argumentů z textu i vlastní zkušenosti."),
#   then a line of its own, "Vlastními slovy, bez opsání frází z textu."
#   (121).
# - Part III (122-126 reprint the head, the instruction, both titles and
#   "nebo"): one descriptive line only (127-128, "Jasně psaná kompozice,
#   ...").
# SHAPES:
# - I2-I6: each one model paragraph, shown, whole=True on the printed 5 (10a).
# - II: the scheme's content line and its requirement line, two shown rows on
#   the paper's 30 (questionTotal; 10a: content with no marks and no
#   criteria; as the requirement-only answers of Part I are shown).
# - III1/III2: only a descriptive line -> unprinted (ruling 4) at the paper's
#   40, the descriptive line quoted.
# JUDGEMENT CALLS:
# - I3 shown, not one(): one sentence, but three statements, not a single
#   fact.
# - II shown rather than unprinted: the scheme prints what the commentary
#   should do (119-121), as in 2015-2023 where the same lines sat beside the
#   criteria; with no criteria this year they are the part's only answer
#   content. If the lead reads them as a "descriptive line" (ruling 4), the
#   alternative is unprinted(quote(L(119, 121))).
# - Part II's question is the PAPER's ("... na toto tvrzení a vyjádřete vlastní
#   názor:", p4 y438); the scheme reprints it without "a vyjádřete vlastní
#   názor" (116). Question text only; not quoted.
# - III1: the paper prints "1. „Knihy jsou mrtvým materiálem, dokud v nás
#   neožijí. (Jiří Mahen)" with no closing quotation mark (rendered p4 y651);
#   the scheme the same (124). Lifted as printed.
# - Reading text: pp2-3 (rendered). The live Q1 card's sourceMaterial.pages
#   [2, 3] AGREE with the render.
# - Live-card note for the lead: the paper prices Q1 "[5 × 1 bod]" (p3 y633)
#   and the scheme "[5 x 1 bod]" (60) -- a mark per expression -- but the live
#   card cs-2026-hl-i-1 is carded whole (questionTotal 5). Not touched here;
#   2025's Q1 (same print) is drafted per letter.
# GLYPHS: none in either text layer (Czech letters and punctuation only).
# Lifted as printed: "sociální sítě jsou je služba" (64, live Q1 b)), "Internetem
# často jen srolujeme" (97, Q4's row), "elektronická media" (108, Q6's row).

ESSAY_2026 = 'Napište esej'


def _essay_2026(d):
    return (f'The scheme reprints the part\'s head, the instruction and the two titles; under them it prints only '
            f'“{L(127, 128).text(d)}” It prints no criteria and no split of the part\'s marks.')


def _commentary_2026(d):
    return ('The scheme prints no criteria for the part and no mark beside either line; it is scored on its printed total. '
            f'It reprints the task as “{S(116).text(d)}”')


SPECS[2026] = [
    R('I2', [shown(L(83, 85))], whole=True, total=PaperP(4, '2. Jak se'), pages=(2, 3)),
    R('I3', [shown(L(91, 92))], whole=True, total=PaperP(4, '3. Vysvětlete'), pages=(2, 3)),
    R('I4', [shown(L(95, 100))], whole=True, total=PaperP(4, 'základě textu.'), pages=(2, 3)),
    R('I5', [shown(L(104, 105))], whole=True, total=PaperP(4, 'tvrzením?'), pages=(2, 3)),
    R('I6', [shown(L(108, 110))], whole=True, total=PaperP(4, 'vlastní názor.'), pages=(2, 3)),
    R('II', [shown(L(119, 120)), shown(S(121))], whole=True, total=PARTP(), rownote=_commentary_2026,
      pages=(2, 3)),
    R('III1', [unprinted(_essay_2026)], question=QP(4, ESSAY_2026, '1. „Knihy')),
    R('III2', [unprinted(_essay_2026)], question=QP(4, ESSAY_2026, '2. „Vlastenectví')),
]


def specs(year):
    return SPECS.get(year, [])
