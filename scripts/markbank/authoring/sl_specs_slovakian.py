#!/usr/bin/env python3
"""Reviewed specs for the Slovakian classic examination (small-languages lane).

One entry per printed ask with no live card; see sl_lib.py for the selector
language. Line numbers are lines of examiner-reports/slovakian/schemes/<year>-hl.md.
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


def specs(year):
    return SPECS.get(year, [])


# ====================================================================== 2010
# ================================================================ 2010 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (audited:
# see slovakian-live-faults-2010-2017.json).
# Paper (rendered pp2-4): the rule "Prečítajte si pozorne celý text ... Odpovede
# napíšte po slovensky ..." (p2 y126-140); the text "Láska k umeniu" runs pp2-3
# (title p2 y185, paragraphs 1-6 and the closing line to the byline "PETER
# PIŠŤANEK" p3 y273); "ČASŤ I: (30 bodov)" p3 y315, Q1 "(5 x 1 bod)" over a)-e),
# Q2-Q6 "(5 bodov)" each; p4: "ČASŤ II" + "(30 bodov)" (y121, the total right-
# aligned on the head's line; one text-layer line), the commentary; "ČASŤ III" +
# "(40 bodov)" (y273), the instruction and two titles "1. téma:" / "alebo" /
# "2. téma:".
# PRICES: II1 the part head's "(30 bodov)" (PARTP, read from the head's own
# line: the census prints no part totals for this sitting); III1/III2 "(40
# bodov)" (PARTP). The scheme heads its parts "ČASŤ II 30 bodov" (72) and
# "ČASŤ III 40 bodov" (90), the same totals.
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4 = printed pages 2-3):
# - Criteria (p3, bold "Poznámka:", 63-71, set between Q6's bullets and Part
#   II): "V 1. a 2. časti budú pri hodnotení brané do úvahy nasledovné
#   kritériá:" -- for Parts 1 AND 2 (I and II), NOT Part III -- then four
#   criteria, each with its percentage: "– 30 %" (65-66), "– 30%" (67-68),
#   "– 30%" (69-70), "– 10%" (71): 100 %.
# - Part II (72-75 reprint the head and the task as the paper prints it): the
#   descriptive line "Komentár obsahujúci najmenej 100 slov, ktorý jasne
#   preukáže porozumenie textu v podstatných bodoch." (76-77, normal type),
#   then seven italic bullets of content (78, 79, 80, 81-82, 83, 84, 85).
# - Part III (90-96 reprint the head, the instruction and both titles): one
#   paragraph under both titles, 97-99, "Zrozumiteľne napísaná slohová práca
#   obsahujúca najmenej 300 slov, ..." (a descriptive line, nothing per
#   title). The criteria are not stated for Part III.
# SHAPES:
# - II1: graded (10b), 30/30/30/10 % of the paper's 30 = 9 / 9 / 9 / 3. Head:
#   the descriptive line (76-77); the criteria's lead quoted (it names the
#   parts it serves); the seven bullets quoted as examples, not a checklist
#   (10a).
# - III1/III2: only a descriptive line printed once under both titles, and
#   the criteria stated for Parts 1 and 2 only: R4 (unprinted) at the paper's
#   40, the note quoting the descriptive line and the criteria's lead.
# JUDGEMENT CALLS:
# - The criteria's lead says "V 1. a 2. časti" (parts 1 and 2; rendered p3):
#   read as NOT covering Part III, as Bulgarian 2010-2014 read "първите две
#   части". If the lead reads the criteria as the paper-wide grid, III1/III2
#   become graded(L(97, 99), PARTP(), CRIT_2010) (12/12/12/4).
# - II1's question is the census text, checked against p4 (the instruction,
#   the bold statement and the task line, no price).
# - III1/III2: the instruction line plus the title; the labels "1. téma:" /
#   "2. téma:" are lines of their own and are left out (Hungarian model);
#   title 2 keeps its printed attribution "(John Donne)" (same line).
# - Reading text pp2-3 (rendered); II1 carries pages=(2, 3). The live 2010
#   cards carry NO sourceMaterial at all (flagged, P).
# GLYPHS: none. á ä č ď é í ĺ ľ ň ó ô ŕ š ť ú ý ž read cleanly in every line used
# (paper and scheme; "zločinu", "dôstojný", "príťažlivý", "ľudí" checked on the
# render).

CRIT_2010 = crit((65, 66), (67, 68), (69, 70), 71)
LEAD_2010 = quote(L(63, 64, after='Poznámka: '), lead='The scheme prints')
ESSAY_2010 = 'Napíšte esej'


def _part3_note_2010(d):
    return (f'Under the two titles the scheme prints only “{L(97, 99).text(d)}” Its criteria are printed for '
            f'parts 1 and 2 only: “{L(63, 64, after="Poznámka: ").text(d)}”')


SPECS[2010] = [
    R('II1', [graded(L(76, 77), PARTP(), CRIT_2010)],
      rownote=both(LEAD_2010, examples(None, S(78), S(79), S(80), L(81, 82), S(83), S(84), S(85))),
      question=QP(4, 'Napíšte komentár', 'Takýto druh', 'Komentujte, prečo'), pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2010)],
      question=QP(4, ESSAY_2010, 'Čím je alebo')),
    R('III2', [unprinted(_part3_note_2010)],
      question=QP(4, ESSAY_2010, '„Nikto nie je')),
]


# ====================================================================== 2011
# ================================================================ 2011 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (audited:
# see slovakian-live-faults-2010-2017.json).
# Paper (rendered pp2-4): the rule (p2 y136-149); the text "Betónové Slovensko"
# runs pp2-3 (title p2 y194, paragraphs 1-8 to the byline "Michal Feik, SME 9.
# júla 2010" p3 y423); "ČASŤ I: (30 bodov)" p3 y465 with Q1-Q6 on p3; p4:
# "ČASŤ II" + "(30 bodov)" (y78, the total a cell of its own at x467), the
# commentary; "ČASŤ III" + "(40 bodov)" (y230), the instruction and two titles
# "1. téma:" / "alebo" / "2. téma:", title 2 with its attribution line
# "Abraham Lincoln (16. prezident USA, 1809 – 1865)" (y464).
# PRICES: II1 "(30 bodov)", III1/III2 "(40 bodov)" on the part heads (PARTP;
# the census reads both totals this sitting). The scheme heads its parts
# "ČASŤ II 30 bodov" (59), "ČASŤ III 40 bodov" (74).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4 = printed pages 1-2):
# - Criteria (p4 top, bold "Poznámka:", 52-58): "V 1. a 2. časti budú pri
#   hodnotení brané do úvahy nasledovné kritériá:" -- Parts 1 AND 2, not Part
#   III -- then "– 30 %" (53), "– 30%" (54-55), "– 30%" (56-57), "– 10%" (58):
#   100 %.
# - Part II (59-62 reprint the head and the task): the descriptive line
#   "Komentár obsahujúci najmenej 100 slov, ktorý jasne preukáže porozumenie
#   textu v podstatných bodoch." (63-64), then eight italic bullets (65, 66,
#   67, 68, 69, 70, 71, 72-73).
# - Part III (74-81 reprint the head, the instruction and both titles, with
#   title 2's attribution): one paragraph under both titles, 82-83,
#   "Zrozumiteľne napísaná slohová práca ..." (descriptive line only).
# SHAPES:
# - II1: graded (10b), 9 / 9 / 9 / 3 of 30; head the descriptive line (63-64);
#   the criteria's lead quoted; the eight bullets quoted as examples (10a).
# - III1/III2: R4 (unprinted) at the paper's 40, the note quoting the
#   descriptive line and the criteria's lead (criteria for parts 1 and 2 only).
# JUDGEMENT CALLS:
# - Criteria read as not covering Part III ("V 1. a 2. časti", rendered p4),
#   as 2010. Alternative if the lead reads them paper-wide:
#   graded(L(82, 83), PARTP(), CRIT_2011).
# - II1's question is cut from the paper's own lines (the census glues the
#   head's "(30 bodov)" cell in front).
# - III2: the quotation and its attribution line, joined; the paper prints
#   "akí šťasní" (a letter short of "šťastní", rendered p4; the scheme's
#   reprint, line 80, prints it the same): lifted as printed.
# - Reading text pp2-3 (rendered); II1 carries pages=(2, 3). The live 2011
#   cards carry NO sourceMaterial (flagged, P).
# GLYPHS: none in the lines used (render checked).

CRIT_2011 = crit(53, (54, 55), (56, 57), 58)
LEAD_2011 = quote(S(52, after='Poznámka: '), lead='The scheme prints')
ESSAY_2011 = 'Napíšte esej'


def _part3_note_2011(d):
    return (f'Under the two titles the scheme prints only “{L(82, 83).text(d)}” Its criteria are printed for '
            f'parts 1 and 2 only: “{S(52, after="Poznámka: ").text(d)}”')


SPECS[2011] = [
    R('II1', [graded(L(63, 64), PARTP(), CRIT_2011)],
      rownote=both(LEAD_2011, examples(None, S(65), S(66), S(67), S(68), S(69), S(70), S(71), L(72, 73))),
      question=QP(4, 'Napíšte komentár', 'Dá sa porušovaním', 'Aké môžu byť'), pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2011)],
      question=QP(4, ESSAY_2011, 'Aká by mala byť')),
    R('III2', [unprinted(_part3_note_2011)],
      question=QP(4, ESSAY_2011, '„Ľudia sú', 'Abraham Lincoln')),
]


# ====================================================================== 2012
# ================================================================ 2012 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (audited:
# see slovakian-live-faults-2010-2017.json).
# Paper (rendered pp2-4): the rule (p2 y136-149); the text "Vidím to presne: O
# sto rokov budú teleporty" runs pp2-3 (title p2 y194, paragraphs 1-7 to the
# byline "Miro ŠIFRA, denník SME 17.1.2012" p3 y403); "ČASŤ I: (30 bodov)" p3
# y457 with Q1-Q6 on p3; p4: "ČASŤ II (30 bodov)" (y78, one text-layer line;
# the total right-aligned), the commentary on two quoted sentences (y119-188);
# "ČASŤ III (40 bodov)" (y271), the instruction and two titles "1. téma:" /
# "alebo" / "2. téma:".
# PRICES: II1 "(30 bodov)", III1/III2 "(40 bodov)", each on its head's own
# line (PARTP; the census prints no part totals this sitting). Scheme heads
# "ČASŤ II 30 bodov" (78), "ČASŤ III 40 bodov" (106).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5 = printed pages 3-4):
# - Criteria (p4, bold "Poznámka:", 70-77, under Q6's answer): "V 1. a 2.
#   časti budú pri hodnotení brané do úvahy nasledovné kritériá:" -- Parts 1
#   AND 2, not Part III -- then "– 30 %" (71-72), "– 30%" (73-74), "– 30%"
#   (75-76), "– 10%" (77): 100 %.
# - Part II (78-83 reprint the head and the task in bold): thirteen italic
#   dashed items, 84-85, 86, 87, 88 (p4) and 93-94, 95, 96-97, 98, 99, 100,
#   101, 102, 103 (p5), then, AFTER them, the descriptive line in normal type
#   "Komentár obsahujúci najmenej 100 slov, ktorý jasne preukáže porozumenie
#   textu v podstatných bodoch." (104-105).
# - Part III (106-112 reprint the head, the instruction and both titles): one
#   paragraph under both titles, 113-114, "Zrozumiteľne napísaná slohová práca
#   ..." (descriptive line only).
# SHAPES:
# - II1: graded (10b), 9 / 9 / 9 / 3 of 30; head the descriptive line (104-105,
#   printed after the items); the criteria's lead quoted; the thirteen items
#   quoted as examples, not a checklist (10a).
# - III1/III2: R4 (unprinted) at the paper's 40, quoting the descriptive line
#   and the criteria's lead (criteria for parts 1 and 2 only).
# JUDGEMENT CALLS:
# - Criteria read as not covering Part III, as 2010 (alternative:
#   graded(L(113, 114), PARTP(), CRIT_2012)).
# - II1's question: the instruction line and the four printed lines of the
#   task (p4 y119-188), from the paper. The scheme's reprint (79-83) differs
#   only in punctuation ("kamarátmi“." for the paper's "kamarátmi.“"): not
#   quoted.
# - III1: the scheme reprints title 1 with two commas the paper does not print
#   ("Ľudstvo závisí viac, ako si myslí, od svojich snov", 109; paper p4 y368
#   "Ľudstvo závisí viac ako si myslí od svojich snov"): punctuation only, not
#   quoted; the paper's words are the question.
# - Reading text pp2-3 (rendered); II1 carries pages=(2, 3). The live 2012
#   cards carry NO sourceMaterial (flagged, P).
# GLYPHS: none in the lines used (render checked).

CRIT_2012 = crit((71, 72), (73, 74), (75, 76), 77)
LEAD_2012 = quote(S(70, after='Poznámka: '), lead='The scheme prints')
ESSAY_2012 = 'Napíšte esej'


def _part3_note_2012(d):
    return (f'Under the two titles the scheme prints only “{L(113, 114).text(d)}” Its criteria are printed for '
            f'parts 1 and 2 only: “{S(70, after="Poznámka: ").text(d)}”')


SPECS[2012] = [
    R('II1', [graded(L(104, 105), PARTP(), CRIT_2012)],
      rownote=both(LEAD_2012, examples(None, L(84, 85), S(86), S(87), S(88), L(93, 94), S(95), L(96, 97),
                                       S(98), S(99), S(100), S(101), S(102), S(103))),
      question=QP(4, 'Napíšte komentár', Run('Predstavme si', 'preboha, nemuseli')), pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2012)],
      question=QP(4, ESSAY_2012, 'Ľudstvo závisí')),
    R('III2', [unprinted(_part3_note_2012)],
      question=QP(4, ESSAY_2012, 'V našej modernej')),
]


# ====================================================================== 2013
# ================================================================ 2013 HL ===
# Drafted (small-languages lane, 20 Nov): the four open asks of this sitting,
# I1e, II1, III1, III2. Live: I1a-d, I2-I6 (9 cards); not touched here
# (audited: see slovakian-live-faults-2010-2017.json).
# Paper (rendered pp2-4): the rule (p2 y137-151); the text "Byť najlepší" runs
# pp2-3 (title p2 y196, paragraphs 1-8 to the byline "Lucia Laczkó, Týždeň
# 8/2012" p3 y495); "ČASŤ I: (30 bodov)" p3 y536; Q1 "(5 × 1 bod)" (p3 y564)
# over a)-e) (y577-633), Q2-Q4 on p3, Q5-Q6 on p4, "(5 bodov)" each; p4: "ČASŤ
# II (30 bodov)" (y290, one text-layer line), the commentary on one sentence;
# "ČASŤ III (40 bodov)" (y483), the instruction and two titles "1. téma:" /
# "alebo" / "2. téma:".
# PRICES:
# - I1e: "(5 × 1 bod)" on Q1's head, five expressions at 1 each (PP: the
#   census walks the per-expression price down to e), tariff (1, 1, 1)). The
#   scheme heads Q1 "(1 x 5 bodov)" (49): the paper's per-expression price
#   stands (10f), the scheme's head quoted on the card.
# - II1 "(30 bodov)", III1/III2 "(40 bodov)" on the part heads (PARTP; the
#   census prints no part totals this sitting). Scheme heads "ČASŤ II 30
#   bodov" (102), "ČASŤ III 40 bodov" (122).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3):
# - Q1 (rendered p3, italic): each expression reprinted with its gloss after a
#   dash, lettered a) b) c) d) d) -- the fifth line (54) is a SECOND "d)":
#   "d) biť na poplach – upozorniť na vážnosť situácie". Its words are the
#   paper's e) "biť na poplach (odsek 6)" (p3 y633): paired by WORDS, so it is
#   e)'s answer. One stated answer: one row at the paper's 1.
# - Criteria (p4, bold "Poznámka:", 94-101, under Q6): "V 1. a 2. časti budú
#   pri hodnotení brané do úvahy nasledovné kritériá:" -- Parts 1 AND 2, not
#   Part III -- "– 30 %" (95-96), "– 30%" (97-98), "– 30%" (99-100), "– 10%"
#   (101): 100 %.
# - Part II (102-104): the scheme reprints the task as "Napíšte komentár
#   (najmenej 100 slov) na tému:" (103) where the paper prints "Napíšte
#   komentár nasledovnej vety z textu (najmenej 100 slov):" (p4 y332), and the
#   sentence (104); then the descriptive line "Komentár obsahujúci najmenej
#   100 slov, ktorý jasne preukáže porozumenie textu v podstatných bodoch."
#   (105-106, normal type) and ONE italic model paragraph, 107-117 ("Na ľuďoch
#   sú ľudské aj chyby. ... Ale aké by bolo potom ľudstvo?").
# - Part III (p5, 122-128 reprint the head, the instruction and both titles):
#   one paragraph under both titles, 129-130, "Zrozumiteľne napísaná slohová
#   práca ..." (descriptive line only).
# SHAPES:
# - I1e: one(gloss after the dash, PP()).
# - II1: graded (10b), 9 / 9 / 9 / 3 of 30; head the descriptive line
#   (105-106); the criteria's lead quoted; the model paragraph quoted as an
#   example, not a checklist (10a; Czech 2010-2013 Part II); the scheme's
#   reworded task quoted (10f).
# - III1/III2: R4 (unprinted) at the paper's 40, quoting the descriptive line
#   and the criteria's lead (criteria for parts 1 and 2 only).
# JUDGEMENT CALLS:
# - I1e: the scheme's misprinted second "d)" is the only line answering "biť na
#   poplach"; the live I1d row (slk-2013-hl-i-1-d) currently runs on into it
#   (flagged, A). The scheme's letter is quoted on the row's note (10f).
# - Criteria read as not covering Part III, as 2010 (alternative:
#   graded(L(129, 130), PARTP(), CRIT_2013)).
# - II1: the model paragraph goes to the note as an example, not a shown row:
#   the part is graded on its printed criteria (the lane's graded shape, Czech
#   2010-2013), so the paragraph is quoted under it.
# - II1's question: the instruction line and the sentence, cut from the paper.
# - Reading text pp2-3 (rendered); I1e and II1 carry pages=(2, 3). The live
#   2013 cards carry NO sourceMaterial (flagged, P).
# GLYPHS: none in the lines used (render checked).

CRIT_2013 = crit((95, 96), (97, 98), (99, 100), 101)
LEAD_2013 = quote(S(94, after='Poznámka: '), lead='The scheme prints')
ESSAY_2013 = 'Napíšte esej'


def _q1e_note_2013(d):
    return (f'The scheme heads Q1 “{S(49, after="výrazy: ", raw=True).text(d)}” and letters this expression '
            f'“{S(54, before=" – ").text(d)}”, a second d) after “{S(53, before=" – ").text(d)}”; the paper '
            f'prints it as e) and prices each expression “{PC(3, "1. Vysvetlite", after="výrazy: ").text(d)}”.')


def _part3_note_2013(d):
    return (f'Under the two titles the scheme prints only “{L(129, 130).text(d)}” Its criteria are printed for '
            f'parts 1 and 2 only: “{S(94, after="Poznámka: ").text(d)}”')


SPECS[2013] = [
    R('I1e', [one(S(54, after='– '), PP())], rownote=_q1e_note_2013, pages=(2, 3)),
    R('II1', [graded(L(105, 106), PARTP(), CRIT_2013)],
      rownote=both(LEAD_2013, quote(S(103), lead='The scheme reprints the task as'),
                   examples(None, L(107, 117))),
      question=QP(4, 'Napíšte komentár', 'Na ľuďoch sú'), pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2013)],
      question=QP(4, ESSAY_2013, 'Láska sa získava')),
    R('III2', [unprinted(_part3_note_2013)],
      question=QP(4, ESSAY_2013, 'Putovanie za')),
]


# ====================================================================== 2014
# ================================================================ 2014 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (audited:
# see slovakian-live-faults-2010-2017.json).
# Paper (rendered pp2-4): the rule (p2 y137-150); the text "Uštvaní prácou"
# runs pp2-3 (title p2 y197, paragraphs 1-8 to the byline "Martin Hanus, Lukáš
# Krivošík: Týžden 37/2013" p3 y761); p4: "ČASŤ I: (30 bodov)" (y79), Q1-Q6,
# two footnotes at the foot of p4 (y752-764) for Q4's "homo sapiens1" / "homo
# asapiens2"; "ČASŤ II (30 bodov)" (y397, one text-layer line), the
# commentary on a quotation; "ČASŤ III" + "(40 bodov)" (y507, the total a cell
# of its own), the instruction and two titles "1. téma:" / "alebo" / "2.
# téma:", title 2 with its attribution "Ralph Waldo Emerson" (y702).
# PRICES: II1 "(30 bodov)" (PARTP, from the head's own line; the census reads
# only Part III's total this sitting); III1/III2 "(40 bodov)" (PARTP). Scheme
# heads "ČASŤ II 30 bodov" (103), "ČASŤ III 40 bodov" (122).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5 = printed pages 3-4):
# - Criteria (p4, bold "Poznámka:", 95-102, under Q6): "V 1. a 2. časti budú
#   pri hodnotení brané do úvahy nasledovné kritériá:" -- Parts 1 AND 2, not
#   Part III -- "– 30 %" (96-97), "– 30%" (98-99), "– 30%" (100-101), "– 10%"
#   (102): 100 %.
# - Part II (103-106 reprint the head and the task as the paper prints it): NO
#   descriptive line this sitting; seven italic lines of content, each opening
#   a new line, no bullets (rendered p4): 107-108, 109, 110, 111, 112-113,
#   114-115, 116-117.
# - Part III (p5, 122-130 reprint the head, the instruction, both titles and
#   title 2's attribution): NOTHING else -- no descriptive line, no content,
#   no criteria for this part.
# SHAPES:
# - II1: graded (10b), 9 / 9 / 9 / 3 of 30. With no descriptive line, the
#   head is the criteria's own lead (95, cut after "Poznámka: "; Czech 2013,
#   Finnish 2012); the seven lines quoted as examples, not a checklist (10a).
# - III1/III2: nothing printed for this part: R4 (unprinted) at the paper's
#   40, the note saying what the scheme prints (the instruction and titles
#   only, criteria for parts 1 and 2).
# JUDGEMENT CALLS:
# - The seven content lines are quoted as seven items (each opens a new line,
#   rendered p4), wrapped lines joined.
# - II1's question: the instruction line and the two printed lines of the
#   quotation, from the paper.
# - III1: the census welds the joiner onto title 1 ("Práca – povinnosť a
#   poslanie alebo"); the title is cut from its own printed line.
# - III2: the two lines of the quotation and the attribution line, joined.
# - Reading text pp2-3 (rendered: title p2 y197, the text to its byline at the
#   foot of p3; p4 holds only the questions and Parts II-III); II1 carries
#   pages=(2, 3). The live 2014 cards carry NO sourceMaterial (flagged, P).
# GLYPHS: none in the lines used (render checked).

CRIT_2014 = crit((96, 97), (98, 99), (100, 101), 102)
HEAD_2014 = S(95, after='Poznámka: ')
ESSAY_2014 = 'Napíšte esej'


def _part3_note_2014(d):
    return (f'Under “{S(122, before=" 40 bodov").text(d)}” the scheme reprints only the instruction “{S(123).text(d)}” and the two '
            f'titles; it prints no answer, no content and no criteria for this part. Its criteria are printed for '
            f'parts 1 and 2 only: “{S(95, after="Poznámka: ").text(d)}”')


SPECS[2014] = [
    R('II1', [graded(HEAD_2014, PARTP(), CRIT_2014)],
      rownote=examples(None, L(107, 108), S(109), S(110), S(111), L(112, 113), L(114, 115), L(116, 117)),
      question=QP(4, 'Napíšte komentár', '„O čo sa', 'Dá sa ešte'), pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2014)],
      question=QP(4, ESSAY_2014, 'Práca – povinnosť')),
    R('III2', [unprinted(_part3_note_2014)],
      question=QP(4, ESSAY_2014, '„Aj keď', 'ináč ju', 'Ralph Waldo')),
]


# ====================================================================== 2015
# ================================================================ 2015 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (audited:
# see slovakian-live-faults-2010-2017.json).
# (Was HOLD, resolved by the lead: the .md repaired from glyph ids by sl_glyphs.py slovakian,
# 3870db7bf; line numbers unchanged.) The scheme's text layer was mangled. Scheme pp3-5 set Type0
# Times New Roman (regular, bold, italic) glyphs with no Unicode (texttrace
# U+FFFD); the .md reads them as Latin-1/Latin Extended-A stand-ins. Read
# against the render (scheme p3 at 150 dpi, "ČASŤ I", "mať kopec času",
# "s ľuďmi", "keď"; p4 at 100 dpi), by glyph id:
#   id 253 -> U+00FD "ý" (7x), drawn Č  ("ýASġ I" = "ČASŤ I", "ýlovek",
#             "ýakáme") -- COLLIDES with the real ý the same text prints
#             ("vlastnými", "slovami výrazy"): a character map cannot repair it;
#   id 254 -> U+00FE "þ" (32x), drawn č  ("þasu" = "času");
#   id 263 -> U+0107 "ć" (13x), drawn ď  ("Đućmi" = "ľuďmi", "keć" = "keď");
#   id 272 -> U+0110 "Đ" (37x), drawn ľ  ("veĐa" = "veľa");
#   id 289 -> U+0121 "ġ" (3x),  drawn Ť  ("ýASġ" = "ČASŤ");
#   id 290 -> U+0122 "Ģ" (61x), drawn ť  ("maĢ" = "mať").
# Not hand-mapped. The .md needs sl_glyphs' positional repair (as Czech 2015,
# whose "ýást" collides the same way): a 'slovakian' entry with docs {2015:
# ('scheme',)}, positional=True and the Slovak alphabet as real letters. The
# repair keeps every line and its length, so the line numbers below stand;
# until it lands, every row and note of this sitting would show the stand-ins.
# Dry run (20 Nov), never written to the repo: sl_glyphs.derive with such an
# entry settles all six ids from the corpus (253 Č, 254 č, 263 ď, 272 ľ, 289 Ť,
# 290 ť; nothing left unsettled) and positional() in check mode repairs 331
# glyphs (7 "ý"->Č, the real ý left; the cover's shifted ASCII too) with 0
# unresolved, 0 conflicts, 0 unaligned. On a scratch copy so repaired
# (drafts/sk2015fix/), these three specs build clean (draft_check with the
# scheme lines read from it). The ten live 2015 cards need the same repair
# (flagged, A: slovakian-live-faults-2010-2017.json).
# The paper's text layer is clean (census questions read "vybrať ľudí do
# záchranného člna"). The cover (p1-2 headings) is shifted ASCII
# ("&RLPLVL~QQD6FU~GXLWKH6WiLW"); no card uses it.
# Paper (rendered pp2-4): the rule (p2 y105-117); the text "Priateľstvo podľa
# Macka Pu" runs pp2-3 (title p2 y155, paragraphs 1-6 to the byline "Mirka
# Gúčiková: Týždeň 8/2014" p3 y178); "ČASŤ I: (30 bodov)" p3 y259 with Q1-Q6 on
# p3; p4: "ČASŤ II" + "(30 bodov)" (y64), the commentary on one sentence;
# "ČASŤ III" + "(40 bodov)" (y216), the instruction and two titles "1. téma:" /
# "Alebo" / "2. téma:", title 2 "... zo všetkých.“ (Sokrates)" on one line.
# PRICES: II1 "(30 bodov)", III1/III2 "(40 bodov)" on the part heads (PARTP;
# the census reads both). Scheme heads "ČASŤ II 30 bodov" (101), "ČASŤ III 40
# bodov" (126).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5 = printed pages 2-3):
# - Criteria (p4, bold "Poznámka:", 93-100): "V 1. a 2. časti budú pri
#   hodnotení brané do úvahy nasledovné kritériá:" -- Parts 1 AND 2, not
#   Part III -- "– 30 %" (94-95), "– 30%" (96-97), "– 30%" (98-99), "– 10%"
#   (100): 100 %.
# - Part II (101-103 reprint the head and the task): NO descriptive line;
#   "Napríklad:" (104, bold) over seventeen italic items, one per line, no
#   bullets, 105-121 (rendered p4).
# - Part III (p5, 126-132 reprint the head, the instruction and both titles,
#   title 2's attribution without the paper's brackets, "Sokrates"): NOTHING
#   else.
# SHAPES:
# - II1: graded (10b), 9 / 9 / 9 / 3 of 30; head the criteria's own lead (93,
#   cut after "Poznámka: "; no descriptive line, as 2014); the seventeen items
#   quoted under the scheme's own "Napríklad:" as examples, not a checklist
#   (10a).
# - III1/III2: nothing printed for this part: R4 (unprinted) at the paper's
#   40, the note saying what the scheme prints.
# JUDGEMENT CALLS:
# - Item 112 prints "Byťiniciatívny" with no space (rendered p4): as printed.
# - Criteria read as not covering Part III, as 2010.
# - II1's question: the instruction line and the quoted sentence, from the
#   paper (the census glues the head's "(30 bodov)" cell in front).
# - III2: title and "(Sokrates)" as the paper prints them on one line; the
#   scheme's bracketless "Sokrates" is punctuation only, not quoted.
# - Reading text pp2-3 (rendered); II1 carries pages=(2, 3). The live 2015
#   cards carry NO sourceMaterial (flagged, P).

CRIT_2015 = crit((94, 95), (96, 97), (98, 99), 100)
HEAD_2015 = S(93, after='Poznámka: ')
ESSAY_2015 = 'Napíšte esej'


def _part3_note_2015(d):
    return (f'Under “{S(126, before=" 40 bodov").text(d)}” the scheme reprints only the instruction “{S(127).text(d)}” and the two '
            f'titles; it prints no answer, no content and no criteria for this part. Its criteria are printed for '
            f'parts 1 and 2 only: “{S(93, after="Poznámka: ").text(d)}”')


SPECS[2015] = [
    R('II1', [graded(HEAD_2015, PARTP(), CRIT_2015)],
      rownote=examples(S(104), *[S(n) for n in range(105, 122)]),
      question=QP(4, 'Napíšte komentár', '„Ak chceme'), pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2015)],
      question=QP(4, ESSAY_2015, 'Magická sila')),
    R('III2', [unprinted(_part3_note_2015)],
      question=QP(4, ESSAY_2015, '„Človek, ktorý')),
]


# ====================================================================== 2016
# ================================================================ 2016 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (audited:
# see slovakian-live-faults-2010-2017.json).
# Paper (rendered pp2-4): the rule (p2 y135-149); the text "„Lepšie ako
# žobrať,“ hovoria chudobní, ktorí obliekajú svet" runs pp2-3 (title p2 y194,
# paragraphs 1-8 to the byline "Jarmila Štuková: Týždeň 42/2015" p3 y506);
# "ČASŤ I: (30 bodov)" p3 y561, Q1-Q2 on p3, Q3-Q6 on p4; p4: "ČASŤ II (30
# bodov)" (y395, one text-layer line), the commentary on a three-line
# statement (y451-478); "ČASŤ III" + "(40 bodov)" (y547, the total a cell of
# its own), the instruction and two titles "1. téma:" / "alebo" / "2. téma:",
# title 2 with its attribution "Fintan O´Toole: The Irish Times" / "22.
# februára 2016" (y753-764).
# PRICES: II1 "(30 bodov)" (PARTP, from the head's own line; the census reads
# only Part III's total this sitting); III1/III2 "(40 bodov)" (PARTP). Scheme
# heads "ČASŤ II 30 bodov" (119), "ČASŤ III 40 bodov" (141).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5 = printed pages 2-3):
# - Criteria (p4, bold "Poznámka:", 107-114, under Q6): "V 1. a 2. časti budú
#   pri hodnotení brané do úvahy nasledovné kritériá:" -- Parts 1 AND 2, not
#   Part III -- "– 30 %" (108-109), "– 30%" (110-111), "– 30%" (112-113),
#   "– 10%" (114): 100 %.
# - Part II (p5, 119-123 reprint the head and the statement): NO descriptive
#   line; "Napríklad:" (124, bold) over seven italic dashed items, 125-126,
#   127-128, 129-131, 132-133, 134-136, 137-138, 139-140.
# - Part III (141-150 reprint the head, the instruction, both titles and
#   title 2's attribution): NOTHING else.
# SHAPES:
# - II1: graded (10b), 9 / 9 / 9 / 3 of 30; head the criteria's own lead
#   (107, cut after "Poznámka: "); the seven items quoted under the scheme's
#   own "Napríklad:" as examples, not a checklist (10a).
# - III1/III2: nothing printed for this part: R4 (unprinted) at the paper's
#   40, the note saying what the scheme prints.
# JUDGEMENT CALLS:
# - Criteria read as not covering Part III, as 2010.
# - Printed as such (rendered p5), lifted as printed: "sme sme zarábali"
#   (125, a doubled word), "oblečnie" (131, 139).
# - II1's question: the instruction line and the three printed lines of the
#   statement, from the paper.
# - III1: the census welds the joiner onto title 1 ("... na svete. alebo");
#   the title is cut from its own printed line (the paper ends it with a full
#   stop, the scheme's reprint does not: punctuation only).
# - III2: the two lines of the statement and both attribution lines, joined
#   (keep_marker: QP would take the date's "22." for a part marker; no line of
#   this question prints one).
# - Reading text pp2-3 (rendered); II1 carries pages=(2, 3). The live 2016
#   cards carry NO sourceMaterial (flagged, P).
# GLYPHS: none in the lines used (render checked).

CRIT_2016 = crit((108, 109), (110, 111), (112, 113), 114)
HEAD_2016 = S(107, after='Poznámka: ')
ESSAY_2016 = 'Napíšte esej'


def _part3_note_2016(d):
    return (f'Under “{S(141, before=" 40 bodov").text(d)}” the scheme reprints only the instruction “{S(142).text(d)}” and the two '
            f'titles; it prints no answer, no content and no criteria for this part. Its criteria are printed for '
            f'parts 1 and 2 only: “{S(107, after="Poznámka: ").text(d)}”')


SPECS[2016] = [
    R('II1', [graded(HEAD_2016, PARTP(), CRIT_2016)],
      rownote=examples(S(124), L(125, 126), L(127, 128), L(129, 131), L(132, 133), L(134, 136), L(137, 138),
                       L(139, 140)),
      question=QP(4, 'Napíšte komentár', Run('Západná spoločnosť', 'zaobchádzanie s úbohými')), pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2016)],
      question=QP(4, ESSAY_2016, 'Ako sa dá prežiť')),
    R('III2', [unprinted(_part3_note_2016)],
      question=QP(4, ESSAY_2016, Run('Svet sa môže', 'demokratickejším'), 'Fintan O´Toole', '22. februára',
                  keep_marker=True)),
]


# ====================================================================== 2017
# ================================================================ 2017 HL ===
# Drafted (small-languages lane, 20 Nov): the four open asks of this sitting,
# I2, II1, III1, III2. Live: I1a-e, I3-I6 (9 cards); not touched here
# (audited: see slovakian-live-faults-2010-2017.json).
# Paper (rendered pp2-4): the rule (p2 y138-153); the text "Obrana čumenia z
# okna" runs pp2-3 (title p2 y197, paragraphs 1-10 to the byline "Sandra
# Tordová: Nota bene 03/2016" p3 y387; a footnote to "Silicon Valley1" at the
# foot of p3, y779); "ČASŤ I: (30 bodov)" p3 y430, Q1-Q3 on p3, Q4-Q6 on p4;
# p4: "ČASŤ II (30 bodov)" (y299, one text-layer line), the commentary on a
# quotation (y358-387); "ČASŤ III" + "(40 bodov)" (y461, the total a cell of
# its own), the instruction and two titles "1. téma:" / "alebo" / "2. téma:",
# title 2 a quotation and a task line (y666-680).
# PRICES:
# - I2: "(5 bodov)" on a line of its own under the question (p3 x482 y642);
#   the census reads it (tariff (1, 5, 5)): PP(). The scheme prints the same
#   "(5 bodov)" (56).
# - II1 "(30 bodov)" (PARTP, from the head's own line; the census reads only
#   Part III's total this sitting); III1/III2 "(40 bodov)" (PARTP). Scheme
#   heads "ČASŤ II 30 bodov" (115), "ČASŤ III 40 bodov" (134).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3):
# - Q2 (55-56 reprint the question in bold with "(5 bodov)", as "Na základe
#   textu a vysvetlite, ..." -- an "a" the paper does not print): ONE italic
#   paragraph, 57-62 ("Snívanie za bieleho dňa je tá časť dňa, ... nenáročná
#   športová aktivita."). No split, no marks inside.
# - Criteria (p4, bold "Poznámka:", 103-110, under Q6): "V 1. a 2. časti budú
#   pri hodnotení brané do úvahy nasledovné kritériá:" -- Parts 1 AND 2, not
#   Part III -- "– 30 %" (104-105), "– 30%" (106-107), "– 30%" (108-109),
#   "– 10%" (110): 100 %.
# - Part II (p5, 115-119 reprint the head and the quotation): NO descriptive
#   line; "Napríklad:" (120, bold) over nine italic items each opened by a
#   minus sign "−" (U+2212; rendered as a dash): 121, 122, 123, 124-125, 126,
#   127, 128-129, 130-131, 132-133.
# - Part III (134-142 reprint the head, the instruction and both titles):
#   NOTHING else. Title 2's task line is reprinted as "... a najmä na
#   používanie sociálnych médií." (141-142) where the paper prints "...
#   sociálnych sietí." (p4 y680).
# SHAPES:
# - I2: one printed answer paragraph for a priced short question: ONE
#   claimable row at the paper's 5 (one(sel, PP())); the scheme's reworded
#   reprint quoted on the row (10f).
# - II1: graded (10b), 9 / 9 / 9 / 3 of 30; head the criteria's own lead
#   (103, cut after "Poznámka: "); the nine items quoted under "Napríklad:" as
#   examples, not a checklist (10a).
# - III1/III2: nothing printed for this part: R4 (unprinted) at the paper's
#   40; III2's note also quotes the scheme's reworded reprint of its title.
# JUDGEMENT CALLS:
# - I2: the old exclusion ("does not hold this answer as one run") came from
#   joining the reprint to the answer; the answer alone (57-62) is one run.
# - Part II items: S() keeps the minus sign (its bullet strip takes "-", "–",
#   "—", "•", not U+2212), so each item is cut after "− ".
# - Printed as such (rendered p5), lifted as printed: "ľudmi" (121, for
#   "ľuďmi"), "rieiť" (132, for "riešiť"), the comma ending 131.
# - Criteria read as not covering Part III, as 2010.
# - II1's question: the instruction line and the three printed lines of the
#   quotation (it closes with "”", as printed).
# - III2: the quotation and the task line, both printed as title 2.
# - Reading text pp2-3 (rendered); I2 and II1 carry pages=(2, 3). The live
#   2017 cards carry NO sourceMaterial (flagged, P).
# GLYPHS: none in the lines used (render checked).

CRIT_2017 = crit((104, 105), (106, 107), (108, 109), 110)
HEAD_2017 = S(103, after='Poznámka: ')
ESSAY_2017 = 'Napíšte esej'
DASH_2017 = '− '


def _part3_note_2017(d):
    return (f'Under “{S(134, before=" 40 bodov").text(d)}” the scheme reprints only the instruction “{S(135).text(d)}” and the two '
            f'titles; it prints no answer, no content and no criteria for this part. Its criteria are printed for '
            f'parts 1 and 2 only: “{S(103, after="Poznámka: ").text(d)}”')


SPECS[2017] = [
    R('I2', [one(L(57, 62), PP())],
      rownote=quote(L(55, 56, after='2. ', before=' (5'), lead='The scheme reprints this question as'), pages=(2, 3)),
    R('II1', [graded(HEAD_2017, PARTP(), CRIT_2017)],
      rownote=examples(S(120), S(121, after=DASH_2017), S(122, after=DASH_2017), S(123, after=DASH_2017), L(124, 125, after=DASH_2017),
                       S(126, after=DASH_2017), S(127, after=DASH_2017), L(128, 129, after=DASH_2017), L(130, 131, after=DASH_2017),
                       L(132, 133, after=DASH_2017)),
      question=QP(4, 'Napíšte komentár', Run('„Nechodíme', 'hovoriť.')), pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2017)],
      question=QP(4, ESSAY_2017, 'Sme zasnívané')),
    R('III2', [unprinted(both(_part3_note_2017,
                              quote(L(140, 142), lead='The scheme reprints this title as')))],
      question=QP(4, ESSAY_2017, '„Môj názor', 'Premietni tento')),
]


# ====================================================================== 2018
# ================================================================ 2018 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I1a-e, II1, III1, III2. Live: I2-I6 (5 cards); not touched here (audited:
# see slovakian-live-faults-2018-2026.json).
# Paper (rendered pp2-4; renders slo-2018-sk-paper-p*.png): the rule "Prečítajte
# si pozorne celý text ... Odpovede napíšte po slovensky ..." (p2 y124-138);
# the text "Najnebezpečnejší text na facebooku napísal jeho zakladateľ" runs
# pp2-3 (title p2 y182, paragraphs 1-6 to the byline "Ondrej Podstupka, SME,
# 27. február 2017" p3 y370; two footnotes at the foot of p3, y738-755);
# "ČASŤ I:" + "(30 bodov)" p3 y413. Q1 is printed as a bare "1." (bold, p3
# y436) over five lettered expressions a)-e) (y451-518), each with its
# paragraph "(2. odsek)": NO instruction and NO price anywhere in Q1's block
# (rendered p3; text layer checked span by span). Q2-Q3 on p3, Q4-Q6 on p4,
# "(5 bodov)" each. p4: "ČASŤ II" + "(30 bodov)" (y369), the commentary;
# "ČASŤ III" + "(40 bodov)" (y501), the instruction and two titles "1. téma:" /
# "alebo" / "2. téma:".
# PRICES:
# - I1a-e: the paper prints no price for Q1 at all (its Part I prints 30, and
#   Q2-Q6 print 5 each). The SCHEME prices Q1 "(5 x 1 bod)" on its head (line
#   50): one mark per expression, read with SP(50) (the brief: else the
#   scheme's printed price). 5 x 1 = 30 - 25, so the paper's totals agree.
#   Not 10i and not REM: the scheme prints the per-expression mark.
# - II1 "(30 bodov)", III1/III2 "(40 bodov)": PARTP (the census reads all three
#   part heads). Scheme heads "ČASŤ II 30 bodov" (100), "ČASŤ III 40 bodov"
#   (119).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3):
# - Q1 (50): "1. Vysvetlite vlastnými slovami výrazy: (5 x 1 bod)", then a)-e)
#   (51-55), each reprinting the paper's expression (without its paragraph)
#   and the gloss after a dash ("–"; b) sets a hyphen-minus "svetonázor -
#   chápanie sveta", 52). Letters and words agree with the paper's a)-e).
# - Criteria (p4, bold "Poznámka:", 92-99, under Q6): "V 1. a 2. časti budú
#   pri hodnotení brané do úvahy nasledovné kritériá:" -- Parts 1 AND 2, not
#   Part III -- "– 30 %" (93-94), "– 30%" (95-96), "– 30%" (97-98), "– 10%"
#   (99): 100 %.
# - Part II (100-102 reprint the head and the task; the statement in quotes
#   with a full stop the paper does not print: punctuation only): NO
#   descriptive line; six italic dashed items, 103 (p4), 108-109, 110-112, 113,
#   114-115, 116-118 (p5; lines 104-107 are the page number and page break).
# - Part III (119-127 reprint the head, the instruction and both titles):
#   NOTHING else -- no descriptive line, no content, no criteria.
# SHAPES:
# - I1a-e: one(gloss after the dash, SP(50)) each, total SP(50).
# - II1: graded (10b), 30/30/30/10 % of the paper's 30 = 9 / 9 / 9 / 3; head
#   the criteria's own lead (92, cut after "Poznámka: "; no descriptive line,
#   as 2014-2017); the six items quoted as examples, not a checklist (10a).
# - III1/III2: nothing printed for this part: R4 (unprinted) at the paper's
#   40, the note saying what the scheme prints (criteria for parts 1 and 2).
# JUDGEMENT CALLS:
# - Q1 questions: the expression and its paragraph as the paper prints them on
#   the expression's own line (the paper prints no instruction; the scheme's
#   "Vysvetlite vlastnými slovami výrazy:" is quoted on the row's note, 10f).
#   CENSUS MIS-KEY (reported, not drafted around): eu_paper's line reader welds
#   each expression cell (x125) onto the letter cell 16.8 pt ABOVE it, so the
#   census reads "1. zmeniť tvár spoločnosti (2. odsek)" (p3 y442) as Q1's
#   stem and gives every letter its successor's expression: I1a "zmeniť tvár
#   spoločnosti (2. odsek) svetonázor (3. odsek)" ... I1e "zmeniť tvár
#   spoločnosti (2. odsek)" with nothing of its own. The raw spans set each
#   letter and its expression on ONE baseline (a) + "zmeniť tvár spoločnosti
#   (2. odsek)" y450.8; b) + "svetonázor (3. odsek)" y467.6; c) "asociál"
#   y484.5; d) "obuť celý svet" y501.4; e) "manifest (6. odsek)" y518.2). The
#   question is lifted from the welded line that carries the right words
#   (QP strips its "1." / letter), and conceptId is taken from the card's own
#   question (concept='question'; Danish 2024 precedent).
# - Criteria read as not covering Part III ("V 1. a 2. časti"), as 2010-2017.
#   If the lead reads them paper-wide: graded(HEAD_2018, PARTP(), CRIT_2018)
#   for III1/III2 (12/12/12/4).
# - II1's question: the instruction line and the statement, from the paper.
# - III2: the three printed lines of the title, joined.
# - Reading text pp2-3 (rendered); I1a-e and II1 carry pages=(2, 3). The live
#   2018 cards carry [3] (flagged, P).
# GLYPHS: none. á ä č ď é í ĺ ľ ň ó ô ŕ š ť ú ý ž read cleanly in every line
# used (paper and scheme, render checked: "zmeniť", "človek", "ľudí", "Šaty").

Q1P_2018 = SP(50)
CRIT_2018 = crit((93, 94), (95, 96), (97, 98), 99)
HEAD_2018 = S(92, after='Poznámka: ')
ESSAY_2018 = 'Napíšte esej'


def _q1_note_2018(d):
    return (f'The paper prints Question 1 as a bare “1.” over the five expressions, with no instruction and no '
            f'price; the scheme heads it “{S(50, after="1. ", before=" (5").text(d)}” and prices it '
            f'“{S(50, after=": ", raw=True).text(d)}”.')


def _part3_note_2018(d):
    return (f'Under “{S(119, before=" 40 bodov").text(d)}” the scheme reprints only the instruction “{S(120).text(d)}” and the two '
            f'titles; it prints no answer, no content and no criteria for this part. Its criteria are printed for '
            f'parts 1 and 2 only: “{S(92, after="Poznámka: ").text(d)}”')


def _q1_2018(key, line, dash, opening):
    return R(key, [one(S(line, after=dash), Q1P_2018)], total=Q1P_2018, rownote=_q1_note_2018,
             question=QP(3, opening), concept='question', pages=(2, 3))


SPECS[2018] = [
    _q1_2018('I1a', 51, '– ', '1. zmeniť'),
    _q1_2018('I1b', 52, '- ', 'a) svetonázor'),
    _q1_2018('I1c', 53, '– ', 'b) asociál'),
    _q1_2018('I1d', 54, '– ', 'c) obuť'),
    _q1_2018('I1e', 55, '– ', 'd) manifest'),
    R('II1', [graded(HEAD_2018, PARTP(), CRIT_2018)],
      rownote=examples(None, S(103), L(108, 109), L(110, 112), S(113), L(114, 115), L(116, 118)),
      question=QP(4, 'Napíšte komentár', 'Facebook je'), pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2018)],
      question=QP(4, ESSAY_2018, 'Sloboda slova')),
    R('III2', [unprinted(_part3_note_2018)],
      question=QP(4, ESSAY_2018, Run('Šaty robia', 'to svoj názor'))),
]


# ====================================================================== 2019
# ================================================================ 2019 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I1a-e, II1, III1, III2. Live: I2-I6 (5 cards); not touched here (audited:
# see slovakian-live-faults-2018-2026.json).
# Paper (rendered pp2-4; renders slo-2019-sk-paper-p*.png): the rule (p2
# y124-138); the text "Narodení v digitálnom veku" runs pp2-3 (title p2 y167,
# paragraphs 1-8 to the byline "Galina Lišháková, Nota bene 5/2018" p3 y431;
# a footnote "1 videoblog" at the foot of p3, y781); "ČASŤ I:" + "(30 bodov)"
# p3 y474. Q1 is printed as a bare "1." (bold, p3 y497) over five lettered
# expressions a)-e) (y512-600), each with its paragraph: NO instruction and NO
# price in Q1's block (rendered p3; spans checked). Q2 on p3, Q3-Q6 on p4,
# "(5 bodov)" each. p4: "ČASŤ II" + "(30 bodov)" (y335), the commentary on a
# three-line quotation (y409-438); "ČASŤ III" + "(40 bodov)" (y526), the
# instruction and two titles "1. téma:" / "alebo" / "2. téma:".
# PRICES:
# - I1a-e: the paper prints no price for Q1 (Part I 30, Q2-Q6 5 each). The
#   SCHEME prices Q1 "(5 x 1 bod)" on its head (line 50): one mark per
#   expression, SP(50). 5 x 1 = 30 - 25: the paper's totals agree.
# - II1 "(30 bodov)", III1/III2 "(40 bodov)": PARTP. Scheme heads "ČASŤ II 30
#   bodov" (104), "ČASŤ III 40 bodov" (127).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3):
# - Q1 (50): "1. Vysvetlite vlastnými slovami výrazy: (5 x 1 bod)", then a)-e)
#   (51-55): the gloss ONLY after each letter (italic, no reprint of the
#   expression). d)'s gloss carries its own dash: "nastal čas zmeny – všetko
#   sa zmenilo" (54) -- the whole line after "d) " is the answer (the paper's
#   d) is "nastal zlom"). Paired by letter: the order and the sense agree with
#   the paper's a)-e) (a) peniaze sa začali sypať = "zrazu začali zarábať veľa
#   peňazí", b) krstiť knihu = "slávnosť, pri ktorej sa kniha uvádza na trh",
#   c) smiešne sumy = "málo peňazí", e) učiť sa za pochodu = "priebežne sa
#   učiť, ...").
# - Criteria (p4, bold "Poznámka:", 96-103): "V 1. a 2. časti budú pri
#   hodnotení brané do úvahy nasledovné kritériá:" -- Parts 1 AND 2, not Part
#   III -- criterion 1 ends "– 30" with its "%" wrapped onto a line of its own
#   (97-98; sl_lib reads the wrapped percentage), "– 30%" (99-100), "– 30%"
#   (101-102), "– 10%" (103): 100 %.
# - Part II (104-108 reprint the head and the quotation as the paper prints
#   it): NO descriptive line; seven italic items, each opened by a minus sign
#   "−" (U+2212), all on p5: 113, 114-117, 118-119, 120, 121-122, 123-124,
#   125-126 (109-112 are the page number and page break).
# - Part III (127-136 reprint the head, the instruction and both titles):
#   NOTHING else.
# SHAPES:
# - I1a-e: one(gloss, SP(50)) each, total SP(50).
# - II1: graded (10b), 9 / 9 / 9 / 3 of 30; head the criteria's own lead (96,
#   cut after "Poznámka: "); the seven items quoted as examples (10a).
# - III1/III2: nothing printed for this part: R4 (unprinted) at the paper's 40.
# JUDGEMENT CALLS:
# - Q1 questions: the expression and its paragraph as printed (no instruction
#   on the paper; the scheme's quoted on the note). CENSUS MIS-KEY (reported):
#   the line reader welds a)'s expression (x125, y511.6) onto the "1." line
#   (y496.9) and leaves "a)" empty, so the census gives b)-e) a)'s expression
#   as a stem: I1b "peniaze sa začali sypať (1. odsek) krstiť knihu (3.
#   odsek)" ... I1e "... učiť sa za pochodu (7. odsek)" (I1a happens to read
#   right). Each question is lifted from its own printed line; conceptId from
#   the card's question (concept='question').
# - Part II items: S() keeps the minus sign (its bullet strip takes "-", "‐",
#   "–", "—", "•", not U+2212), so each item is cut after "− ".
# - Printed as such (rendered p5), lifted as printed: "n fb?" (120, for "na
#   fb"); item 2 (117) and items 3, 5, 6, 7 end with no full stop.
# - Criteria read as not covering Part III, as 2010-2018 (alternative:
#   graded(HEAD_2019, PARTP(), CRIT_2019) on III1/III2).
# - II1's question: the instruction line and the three printed lines of the
#   quotation, from the paper. III1/III2: each title's printed lines, joined.
# - Reading text pp2-3 (rendered); I1a-e and II1 carry pages=(2, 3). The live
#   2019 cards carry [3] (flagged, P).
# GLYPHS: none in the lines used (render checked).

Q1P_2019 = SP(50)
CRIT_2019 = crit((97, 98), (99, 100), (101, 102), 103)
HEAD_2019 = S(96, after='Poznámka: ')
ESSAY_2019 = 'Napíšte esej'
DASH_2019 = '− '


def _q1_note_2019(d):
    return (f'The paper prints Question 1 as a bare “1.” over the five expressions, with no instruction and no '
            f'price; the scheme heads it “{S(50, after="1. ", before=" (5").text(d)}” and prices it '
            f'“{S(50, after=": ", raw=True).text(d)}”.')


def _part3_note_2019(d):
    return (f'Under “{S(127, before=" 40 bodov").text(d)}” the scheme reprints only the instruction “{S(128).text(d)}” and the two '
            f'titles; it prints no answer, no content and no criteria for this part. Its criteria are printed for '
            f'parts 1 and 2 only: “{S(96, after="Poznámka: ").text(d)}”')


def _q1_2019(key, line, opening):
    return R(key, [one(S(line, after=f'{key[-1]}) '), Q1P_2019)], total=Q1P_2019, rownote=_q1_note_2019,
             question=QP(3, opening), concept='question', pages=(2, 3))


SPECS[2019] = [
    _q1_2019('I1a', 51, '1. peniaze'),
    _q1_2019('I1b', 52, 'b) krstiť'),
    _q1_2019('I1c', 53, 'c) smiešne'),
    _q1_2019('I1d', 54, 'd) nastal'),
    _q1_2019('I1e', 55, 'e) učiť'),
    R('II1', [graded(HEAD_2019, PARTP(), CRIT_2019)],
      rownote=examples(None, S(113, after=DASH_2019), L(114, 117, after=DASH_2019), L(118, 119, after=DASH_2019),
                       S(120, after=DASH_2019), L(121, 122, after=DASH_2019), L(123, 124, after=DASH_2019),
                       L(125, 126, after=DASH_2019)),
      question=QP(4, 'Napíšte komentár', Run('„Títo mladí', 'že zverejnením')), pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2019)],
      question=QP(4, ESSAY_2019, Run('Sme deti', 'Komentujte túto'))),
    R('III2', [unprinted(_part3_note_2019)],
      question=QP(4, ESSAY_2019, Run('Zobrať si', 'Vo svojej eseji'))),
]


# ====================================================================== 2021
# ================================================================ 2021 HL ===
# Drafted (small-languages lane, 20 Nov): the two open asks of this sitting,
# II1 and II2. Live: I1a-e, I2-I6 (10 cards); not touched here (audited: see
# slovakian-live-faults-2018-2026.json).
# TWO PARTS (the 2021 paper): "Odpovedajte na obidve časti: Prvá časť a Druhá
# časť." (p2 y65), "Celkové hodnotenie 70 bodov". "Prvá časť" + "(30 bodov)"
# (p2 y138), the text "Divadlo bez domova im dalo domov" pp2-3 (title p2 y226
# to the byline "Danka Sláviková, Týždeň 11/2020" p3 y401), Q1-Q6; "Druhá
# časť" + "(40 bodov)" (p4 y253) is the ESSAY: "Napíšte esej (najmenej 300
# slov) na jednu z nasledovných tém:" (y282), "1. téma:" (y340) over the title
# "Dať peniaze do klobúka alebo...?" (y399) and two lines "Uvažuj o rôznych
# formách ..." (y443-458); "alebo" (y516); "2. téma:" (y559) over "Nemôžeš si
# jednoducho vymyslieť svoje vlastné fakty len preto," / "lebo sa ti
# jednoducho nepáči to, čo počuješ.“" (y617-632) and "- Greta Thunberg" (x369
# y632). Essay titles printed "1."/"2.": cited Section II Q1/Q2 (ruling B; in a
# two-part sitting Part II is the essay).
# PRICES: II1/II2 "(40 bodov)" on Part II's head (PARTP: the census maps
# "Druhá časť" to II). The scheme heads it "ČASŤ II 40 bodov" (109).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3):
# - Criteria (p5 top, bold "Poznámka:", 101-108): "V 1. a 2. časti budú pri
#   hodnotení brané do úvahy nasledovné kritériá:" -- in this two-part sitting
#   Parts 1 AND 2 are the whole paper, so the criteria are stated for the
#   ESSAY too -- then the four criteria WITH NO PERCENTAGES and no marks
#   (rendered p5: they end "odpovedať", "spôsobom", "ucelene", "pravopis";
#   2018-2020's "– 30 %" ... "– 10%" are not printed this sitting).
# - Part II (109-119): the head, the instruction reprinted as "Napíšte esej
#   (asi 300 slov) na jednu z dvoch nasledovných tém:" (110; the paper prints
#   "(najmenej 300 slov) na jednu z nasledovných tém:"), both titles reprinted
#   (title 1's sub-lines as "Uvažujte o formách a o účinnosti pomoci – ..."
#   (113-114) for the paper's "Uvažuj o rôznych formách ..."; title 2 with
#   "Greta Thunberg" on its own line, no dash), NOTHING else: no answer, no
#   content, no descriptive line.
# SHAPES:
# - II1/II2: criteria printed for this part WITHOUT percentages: the four
#   criteria as shown rows on the paper's 40, questionTotal (coordinator
#   ruling F; Bulgarian 2021/2022, Romanian 2021/2022). Never a split of 40
#   per criterion (10b: no percentage printed). The criteria's lead quoted on
#   the first row's note, with the scheme's reworded instruction (10f).
# JUDGEMENT CALLS:
# - Which parts the criteria name: "V 1. a 2. časti" in a sitting of exactly
#   two parts reads as both parts, the essay included (as Bulgarian 2021). If
#   the lead reads it as Part I only, II1/II2 become unprinted (R4) at 40.
# - II1: the scheme's reworded sub-lines of title 1 ("Uvažujte o formách" for
#   the paper's "Uvažuj o rôznych formách") are quoted on that card (10f); the
#   paper's words are the question.
# - CENSUS MIS-KEY (reported): the census's II1 and II2 texts are only the
#   labels "1. téma:" (p4 y340) and "2. téma:" (p4 y559); the titles printed
#   below them (y399-458; y617-632 and the attribution x369 y632) are not
#   attached. The questions are cut from the paper's own lines, label left
#   out (Hungarian model, as 2010-2019), and conceptId is taken from the card's
#   question (concept='question'), not from "téma:".
# - II2: the paper prints the quotation with a closing „“” and no opening
#   mark, and the attribution "- Greta Thunberg" (hyphen): lifted as printed.
# - No pages on Part II: a two-part sitting's Part II is the essay. The live
#   2021 cards carry [2, 3] and agree with the render.
# GLYPHS: none in the lines used (render checked).

ESSAY_2021 = 'Napíšte esej'
CRIT_ROWS_2021 = (L(102, 103), L(104, 105), L(106, 107), S(108))


def _crit_note_2021(d):
    return (f'The scheme prints, with no marks or percentages beside the criteria: '
            f'“{S(101, after="Poznámka: ").text(d)}” Under the two titles it prints nothing else. It reprints the '
            f'instruction as “{S(110).text(d)}”')


def _crit_note_2021_t1(d):
    return (f'{_crit_note_2021(d)} and the lines under this title as “{L(113, 114).text(d)}”')


SPECS[2021] = [
    R('II1', [shown(c) for c in CRIT_ROWS_2021], whole=True, rownote=_crit_note_2021_t1,
      question=QP(4, ESSAY_2021, 'Dať peniaze', Run('Uvažuj o', 'pomoc alebo')), concept='question'),
    R('II2', [shown(c) for c in CRIT_ROWS_2021], whole=True, rownote=_crit_note_2021,
      question=QP(4, ESSAY_2021, Run('Nemôžeš si', 'lebo sa ti'), '- Greta'), concept='question'),
]


# ====================================================================== 2022
# ================================================================ 2022 HL ===
# Drafted (small-languages lane, 20 Nov): the two open asks of this sitting,
# II1 and II2. Live: I1a-e, I2-I6 (10 cards); not touched here (audited: see
# slovakian-live-faults-2018-2026.json).
# TWO PARTS (the 2022 paper): "Celkové hodnotenie [70 bodov]" (p2 y94); the
# rule "Prečítajte si pozorne celý text a odpovedajte na otázky v obidvoch
# častiach. Odpovede napíšte po slovensky ..." (p2 y124-138); the text "V
# zajatí konzumu" pp2-3 (title p2 y167 to the byline "Katarína Batková, Týždeň
# 12/2021" p3 y506); "ČASŤ I:" + "(30 bodov)" p3 y578, Q1 "(5 × 1)" (p3 y607)
# over a)-e), Q2-Q6 on p4; "ČASŤ II" + "(40 bodov)" (p4 y445) is the ESSAY:
# "Napíšte esej (asi 300 slov) na jednu z dvoch nasledovných tém:" (y504),
# "1. téma:" over "V dobe dostupných a lacných vecí" / "sa stávajú drahé a
# ťažko dostupné priateľské vzťahy" (y563-577), "alebo", "2. téma:" over "Ako
# vzniká pravé priateľstvo" (y680). Cited Section II Q1/Q2 (ruling B).
# PRICES: II1/II2 "(40 bodov)" on Part II's head (PARTP). Scheme head "ČASŤ II
# 40 bodov" (120).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3):
# - Criteria (p4, bold "Poznámka:", 108-115, under Q6's answer): "V 1. a 2.
#   časti budú pri hodnotení brané do úvahy nasledovné kritériá:" -- in this
#   two-part sitting the whole paper, the ESSAY included -- and the four
#   criteria WITH NO PERCENTAGES and no marks (rendered p4).
# - Part II (p5, 120-127): the head, the instruction and both titles reprinted
#   as the paper prints them (title 2 in quotation marks the paper does not
#   print: punctuation only), NOTHING else.
# SHAPES:
# - II1/II2: criteria printed for this part without percentages: the four
#   criteria as shown rows on the paper's 40, questionTotal (ruling F; as
#   2021). The criteria's lead quoted on the first row's note.
# JUDGEMENT CALLS:
# - "V 1. a 2. časti" read as both parts of this two-part sitting (as 2021).
#   If the lead reads it as Part I only, II1/II2 become unprinted (R4) at 40.
# - Questions: the instruction line and each title's printed lines, from the
#   paper (the census joins the label "1. téma:" / "2. téma:" in front).
# - No pages on Part II (the essay of a two-part sitting).
# GLYPHS: none in the lines used (render checked).

ESSAY_2022 = 'Napíšte esej'
CRIT_ROWS_2022 = (L(109, 110), L(111, 112), L(113, 114), S(115))


def _crit_note_2022(d):
    return (f'The scheme prints, with no marks or percentages beside the criteria: '
            f'“{S(108, after="Poznámka: ").text(d)}” Under “{S(120, before=" 40 bodov").text(d)}” it reprints only the '
            f'instruction and the two titles.')


SPECS[2022] = [
    R('II1', [shown(c) for c in CRIT_ROWS_2022], whole=True, rownote=_crit_note_2022,
      question=QP(4, ESSAY_2022, 'V dobe dostupných', 'sa stávajú drahé')),
    R('II2', [shown(c) for c in CRIT_ROWS_2022], whole=True, rownote=_crit_note_2022,
      question=QP(4, ESSAY_2022, 'Ako vzniká')),
]


# ====================================================================== 2023
# ================================================================ 2023 HL ===
# Drafted (small-languages lane, 20 Nov): the seven open asks of this sitting,
# I1a-d, II1, III1, III2. Live: I1e, I2-I6 (6 cards); not touched here
# (audited: see slovakian-live-faults-2018-2026.json).
# Paper (rendered pp2-4; renders slo-2023-sk-paper-p*.png): the rule (p2
# y124-138); the text "Aké bude Slovensko, ak všetci odídu do zahraničia" runs
# pp2-3 (title p2 y167, paragraphs 1-8 to the byline "Ria Gehrerová, DenníkN
# 35/2022" p3 y414); "ČASŤ I:" + "(30 bodov)" p3 y443; Q1 "1. Vysvetlite
# vlastnými slovami výrazy:" (bold, y472) over a)-e) (y500-588; each
# expression and its "(N. odsek)" two cells of one line) and ONE "(5 bodov)"
# on a line of its own under e) (x491 y611); Q2-Q3 on p3, Q4-Q6 on p4, "(5
# bodov)" each. p4: "ČASŤ II" + "(30 bodov)" (y331), "Napíšte komentár
# (najmenej 100 - 150 slov) na tému:" and the statement; "ČASŤ III" + "(40
# bodov)" (y463), the instruction and two titles "1. téma:" / "alebo" / "2.
# téma:", title 2 a two-line quotation and "Milan Rastislav Štefánik" (y726).
# PRICES:
# - I1a-d: the paper prints ONE price for Q1, "(5 bodov)" under e), for the
#   five expressions together (the census gives it to e) alone: I1e tariff
#   (1, 5, 5); I1a-d none). The SCHEME prices each expression "(5 x 1 bod)"
#   (line 50). One mark each: SP(50); 5 x 1 = the paper's 5, so paper and
#   scheme agree. Carded per letter at the scheme's per-expression price (the
#   brief's marks rule: else the scheme's printed price), not whole at 'I1'
#   (that shape is for a Q1 neither document splits; Romanian 2012-2017 and
#   Croatian print no per-expression price). The paper's single price and
#   the scheme's split are both quoted on each row.
# - II1 "(30 bodov)", III1/III2 "(40 bodov)": PARTP. Scheme heads "ČASŤ II 30
#   bodov" (114), "ČASŤ III 40 bodov" (134).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3):
# - Q1: "1." and "(5 x 1 bod)" (50), "Vysvetlite vlastnými slovami výrazy:"
#   (51), then a)-e) (52-57), each reprinting the paper's expression and the
#   gloss after " – ". Letters and words agree with the paper's.
# - Criteria (p4, bold "Poznámka:", 102-109): "V 1., 2. a 3. časti budú pri
#   hodnotení brané do úvahy nasledovné kritériá:" -- THIS sitting names
#   Parts 1, 2 AND 3 -- then "– 30 %" (103-104), "– 30%" (105-106), "– 30%"
#   (107-108), "– 10%" (109): 100 %.
# - Part II (p5, 114-116): the head, the task reprinted as "Napíšte komentár
#   najmenej 100 slov na tému:" (115; the paper prints "(najmenej 100 - 150
#   slov)") and the statement; NO descriptive line; then one italic model
#   commentary, 117-133: a lead "Existuje mnoho dôvodov, ... Niektoré z
#   týchto dôvodov sú:" (117-118), four paragraphs each opened by its own
#   label ("Motivácia a entuziazmus:" 119-121, "Dôvera investorov:" 122-124,
#   "Patriotizmus:" 125-127, "Inovácia a rozvoj:" 128-130) and a closing
#   paragraph "V konečnom dôsledku ..." (131-133).
# - Part III (134-142 reprint the head, the instruction and both titles):
#   nothing else of its own; the criteria above name it.
# SHAPES:
# - I1a-d: one(gloss after the dash, SP(50)) each, total SP(50).
# - II1: graded (10b), 9 / 9 / 9 / 3 of 30; head the criteria's own lead
#   (102, cut after "Poznámka: "; no descriptive line); the model's six
#   paragraphs quoted as examples, not a checklist (10a); the scheme's
#   reworded task quoted (10f).
# - III1/III2: GRADED, 30/30/30/10 % of the paper's 40 = 12 / 12 / 12 / 4
#   (whole numbers, 10b): the criteria's lead names "3. časti" this sitting
#   (the convention: if a later scheme names Part 3, grade Part III too and
#   say so). Head the criteria's lead; the note says the scheme prints nothing
#   else for the part.
# JUDGEMENT CALLS:
# - Q1 per letter, not whole: see PRICES. The live I1e (slk-2023-hl-i-1-e)
#   carries 5 marks for e)'s one gloss (the census's walk of Q1's single
#   price): flagged C (1).
# - Model paragraphs quoted whole, each label kept inside its paragraph (the
#   labels open the paragraph's own sentence; none is a heading on a line of
#   its own, rendered p5).
# - Q1 questions are the census's text (the paper's stem, the expression and
#   its paragraph, checked on the render).
# - II1's question: the instruction line and the statement, from the paper.
#   III2: the two lines of the quotation and the attribution line.
# - Reading text pp2-3 (rendered); I1a-d and II1 carry pages=(2, 3). The live
#   2023 cards carry [3] (flagged, P).
# GLYPHS: none in the lines used (the .md sets its scheme in no-break spaces;
# the selectors read them as spaces).

Q1P_2023 = SP(50)
CRIT_2023 = crit((103, 104), (105, 106), (107, 108), 109)
HEAD_2023 = S(102, after='Poznámka: ')
ESSAY_2023 = 'Napíšte esej'


def _q1_note_2023(d):
    return (f'The paper prints one price for Question 1, “{PY(3, 611).read(d)[2]}”, under e), for the five '
            f'expressions together; the scheme prices them “{S(50, after="1.", raw=True).text(d)}”.')


def _part3_note_2023(d):
    return (f'The scheme prints its criteria for parts 1, 2 and 3 (the line heading this row). Under '
            f'“{S(134, before=" 40 bodov").text(d)}” it reprints only the instruction “{S(135).text(d)}” and the two '
            f'titles; it prints no answer and no content for this part.')


def _q1_2023(key, line):
    return R(key, [one(S(line, after='– '), Q1P_2023)], total=Q1P_2023, rownote=_q1_note_2023, pages=(2, 3))


SPECS[2023] = [
    _q1_2023('I1a', 52),
    _q1_2023('I1b', 53),
    _q1_2023('I1c', 54),
    _q1_2023('I1d', 55),
    R('II1', [graded(HEAD_2023, PARTP(), CRIT_2023)],
      rownote=both(quote(S(115), lead='The scheme reprints the task as'),
                   examples(None, L(117, 118), L(119, 121), L(122, 124), L(125, 127), L(128, 130), L(131, 133))),
      question=QP(4, 'Napíšte komentár', '„Slovensko potrebuje'), pages=(2, 3)),
    R('III1', [graded(HEAD_2023, PARTP(), CRIT_2023)], rownote=_part3_note_2023,
      question=QP(4, ESSAY_2023, 'Pre uskutočnenie')),
    R('III2', [graded(HEAD_2023, PARTP(), CRIT_2023)], rownote=_part3_note_2023,
      question=QP(4, ESSAY_2023, Run('„Nemôžeme', 'na ktoré nemáme'), 'Milan Rastislav')),
]


# ====================================================================== 2024
# ================================================================ 2024 HL ===
# Drafted (small-languages lane, 20 Nov): the seven open asks of this sitting,
# I1a-d, II1, III1, III2. Live: I1e, I2-I6 (6 cards); not touched here
# (audited: see slovakian-live-faults-2018-2026.json).
# Paper (rendered pp2-4; renders slo-2024-sk-paper-p*.png): the rule (p2
# y124-138); the text "Nomofóbia sa nesmie stať tabu" runs pp2-3 (title p2
# y168, paragraphs 1-7 to the byline "Oliver Remiáš RTVS, 2. 11. 2023" p3
# y327); "ČASŤ I:" + "(30 bodov)" p3 y368; Q1 "1. Vysvetlite vlastnými slovami
# výrazy:" (bold, y397) over a)-e) (y425-493; expression and "(N. odsek)" two
# cells of one line) and ONE "(5 bodov)" at the right of e)'s line (x465
# y494); Q2-Q5 on p3, Q6 on p4, "(5 bodov)" each. p4: "ČASŤ II" + "(30
# bodov)" (y229), "Napíšte komentár (najmenej 100 - 150 slov) na tému:" and
# the statement; "ČASŤ III" + "(40 bodov)" (y390), the instruction and two
# titles "1. téma:" / "Alebo" / "2. téma:", title 2 a two-line quotation and
# "Marek Jílek (etický hacker)" (y666).
# PRICES:
# - I1a-d: the paper prints ONE price for Q1, "(5 bodov)" beside e), for the
#   five expressions together (the census gives it to e) alone). The SCHEME
#   prices each expression "(5 × 1 bod)" (line 50): one mark each, SP(50);
#   5 x 1 = the paper's 5. Per letter at the scheme's price (as 2023); both
#   prints quoted on each row.
# - II1 "(30 bodov)", III1/III2 "(40 bodov)": PARTP. Scheme heads "ČASŤ II 30
#   bodov" (107), "ČASŤ III 40 bodov" (125).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3):
# - Q1 (50-58): "1. Vysvetlite vlastnými slovami výrazy: (5 × 1 bod)", then
#   a)-e), each reprinting the expression and the gloss after " – " (c)
#   after a U+2010 hyphen, "kyberšikana ‐ online ..."). The scheme reprints
#   two expressions in other forms than the paper: b) "monitorovať" (paper
#   "monitoruje"), c) "kyberšikana" (paper "kyberšikanovanie"). Paired by
#   letter and sense (a)-e) agree in order).
# - Criteria (p4, bold "Poznámka:", 95-102): "V 1. a 2. časti budú pri
#   hodnotení brané do úvahy nasledovné kritériá:" -- Parts 1 AND 2, not Part
#   III -- "– 30 %" (96-97), "– 30%" (98-99), "– 30%" (100-101), "– 10%"
#   (102): 100 %.
# - Part II (p5, 107-109): the head, the task reprinted as "Napíšte komentár
#   (najmenej 100 slov) na tému:" (108; the paper prints "(najmenej 100 - 150
#   slov)") and the statement; NO descriptive line; eight italic items each
#   opened by "‐ " (U+2010): 110-112, 113-114, 115-116, 117, 118-119, 120-121,
#   122, 123-124.
# - Part III (125-133 reprint the head, the instruction and both titles):
#   NOTHING else.
# SHAPES:
# - I1a-d: one(gloss after the dash, SP(50)) each, total SP(50).
# - II1: graded (10b), 9 / 9 / 9 / 3 of 30; head the criteria's own lead (95,
#   cut after "Poznámka: "); the eight items quoted as examples (10a); the
#   scheme's reworded task quoted (10f).
# - III1/III2: nothing printed for this part and criteria stated for parts 1
#   and 2 only: R4 (unprinted) at the paper's 40 (2023 named part 3; 2024 does
#   not).
# JUDGEMENT CALLS:
# - Q1 per letter, not whole: as 2023. The live I1e (slk-2024-hl-i-1-e)
#   carries 5 marks for e)'s one gloss: flagged C (1).
# - b), c): the paper's expression stands in the question (census text, the
#   paper's words); the scheme's reworded reprint is quoted on the row (10f).
# - Criteria read as not covering Part III (alternative: graded(HEAD_2024,
#   PARTP(), CRIT_2024) on III1/III2, 12/12/12/4).
# - II1's question: the instruction line and the statement, from the paper.
#   III2: the two lines of the quotation and the attribution line.
# - Reading text pp2-3 (rendered); I1a-d and II1 carry pages=(2, 3). The live
#   2024 cards carry [3] (flagged, P).
# - The live I4's question prints "dospelmôžu" (no space): so the paper
#   prints it (rendered p3 y640), not a text-layer fault.
# - RENDERS (for the lead): drafts/png/slo-2024-scheme-p*.png (and other
#   slo-2018..2024 files) were overwritten at 20:32:48 by the Slovenian
#   helper's renders (same "slo-<year>-" prefix): they show SLOVENIAN pages.
#   This lane's Slovakian renders are slo-<year>-sk-*.png.
# GLYPHS: none in the lines used (U+2010 HYPHEN in "kyberšikana ‐ online" and
# the Part II items is a printed hyphen).

Q1P_2024 = SP(50)
CRIT_2024 = crit((96, 97), (98, 99), (100, 101), 102)
HEAD_2024 = S(95, after='Poznámka: ')
ESSAY_2024 = 'Napíšte esej'


def _q1_note_2024(d):
    return (f'The paper prints one price for Question 1, “{PY(3, 494).read(d)[2]}”, beside e), for the five '
            f'expressions together; the scheme prices them “{S(50, after=": ", raw=True).text(d)}”.')


def _q1_reprint_2024(n, letter, dash):
    def note(d):
        return (f'{_q1_note_2024(d)} The scheme reprints the expression as '
                f'“{S(n, after=f"{letter}) ", before=f" {dash}").text(d)}”.')
    return note


def _part3_note_2024(d):
    return (f'Under “{S(125, before=" 40 bodov").text(d)}” the scheme reprints only the instruction “{S(126).text(d)}” and the two '
            f'titles; it prints no answer, no content and no criteria for this part. Its criteria are printed for '
            f'parts 1 and 2 only: “{S(95, after="Poznámka: ").text(d)}”')


SPECS[2024] = [
    R('I1a', [one(L(51, 52, after='– '), Q1P_2024)], total=Q1P_2024, rownote=_q1_note_2024, pages=(2, 3)),
    R('I1b', [one(S(53, after='– '), Q1P_2024)], total=Q1P_2024, rownote=_q1_reprint_2024(53, 'b', '–'),
      pages=(2, 3)),
    R('I1c', [one(L(54, 55, after='‐ '), Q1P_2024)], total=Q1P_2024, rownote=_q1_reprint_2024(54, 'c', '‐'),
      pages=(2, 3)),
    R('I1d', [one(S(56, after='– '), Q1P_2024)], total=Q1P_2024, rownote=_q1_note_2024, pages=(2, 3)),
    R('II1', [graded(HEAD_2024, PARTP(), CRIT_2024)],
      rownote=both(quote(S(108), lead='The scheme reprints the task as'),
                   examples(None, L(110, 112), L(113, 114), L(115, 116), S(117), L(118, 119), L(120, 121), S(122),
                            L(123, 124))),
      question=QP(4, 'Napíšte komentár', '„Ten, kto'), pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2024)],
      question=QP(4, ESSAY_2024, 'Nech internet')),
    R('III2', [unprinted(_part3_note_2024)],
      question=QP(4, ESSAY_2024, Run('„Aj inteligentný', 'Svet je'), 'Marek Jílek')),
]


# ====================================================================== 2025
# ================================================================ 2025 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (audited:
# see slovakian-live-faults-2018-2026.json).
# Paper (rendered pp2-4; renders slo-2025-sk-paper-p*.png): the rule (p2
# y124-138); the text "Sledujete aj vy greenfluencerov?" / "Ak nie, možno by
# ste mali začať (už dnes)." runs pp2-3 (title p2 y168-182, paragraphs 1-7 to
# the byline "Martin Odkladal, Aktuality.sk, 24. 5. 2024" p3 y327); "ČASŤ I:"
# + "(30 bodov)" p3 y368, Q1-Q6 on p3. p4: "ČASŤ II" + "(30 bodov)" (y79),
# "Napíšte komentár od 100 do 150 slov na tému:" and a two-line statement
# (y152-167); "ČASŤ III" + "(40 bodov)" (y255), "Napíšte esej (najmenej 300
# slov) na jednu z dvoch nasledovných tém:", "1. téma:" / "alebo" / "2.
# téma:", title 2 a quotation over "Belo Kapolka" / "(spisovateľ a
# vysokohorský chatár)" (y502-514).
# PRICES: II1 "(30 bodov)", III1/III2 "(40 bodov)": PARTP. Scheme heads "ČASŤ
# II 30 bodov" (124), "ČASŤ III 40 bodov" (144).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-6 = printed pages 4-6; p3 the
# annotations table, pp7-8 blank but for page numbers):
# - NO "Poznámka", NO criteria and NO percentages anywhere in this scheme.
# - Part II (p6, 124-127 reprint the head, the task and the statement as the
#   paper prints them): one italic paragraph of content, 128-132 ("Sú ľudia,
#   pre ktorých ... len to musia robiť systematicky a, vedome."), ending with
#   the list's lead "Je to napríklad:" on its last line (132), then ten
#   italic dashed points, 133-143 (140-141 one point wrapped). No marks.
# - Part III (144-152 reprint the head, the instruction and both titles, title
#   2 with its attribution): NOTHING else.
# SHAPES:
# - II1: content printed with no per-point marks and no criteria: shown rows,
#   questionTotal on the paper's 30 (the lane convention; Bulgarian 2025/2026
#   Part II): the paragraph (cut before its list lead) and one row per dashed
#   point; the lead "Je to napríklad:" goes in the first row's note, never in
#   a row.
# - III1/III2: nothing printed for this part and no criteria anywhere: R4
#   (unprinted) at the paper's 40, the note saying what the scheme prints.
# JUDGEMENT CALLS:
# - The paragraph and the list are shown, not claimed: the scheme prints them
#   as content for a 30-mark commentary with no points, marks or criteria
#   (10a).
# - Printed as such (rendered p6), lifted as printed: "systematicky a,
#   vedome" (132), "covoiturage" (139), "sóda bicarbona" (140-141).
# - II1's question: the instruction line and the two printed lines of the
#   statement, from the paper. III2: the quotation, "Belo Kapolka" and the
#   bracketed line under it, joined.
# - Reading text pp2-3 (rendered); II1 carries pages=(2, 3). The live 2025
#   cards carry [3] (flagged, P).
# GLYPHS: none in the lines used (render checked; the paper's "hŕstku" prints
# ŕ U+0155, as the render shows).

ESSAY_2025 = 'Napíšte esej'


def _part2_note_2025(d):
    return (f'The scheme prints this paragraph and, under “{S(132, after="vedome. ").text(d)}”, the points below it, '
            f'with no marks and no criteria.')


def _part3_note_2025(d):
    return (f'Under “{S(144, before=" 40 bodov").text(d)}” the scheme reprints only the instruction “{S(145).text(d)}” and the two '
            f'titles; it prints no answer, no content and no criteria for this part, and no criteria anywhere in '
            f'this scheme.')


SPECS[2025] = [
    R('II1', [shown(L(128, 132, before=' Je to napríklad:')), shown(S(133)), shown(S(134)), shown(S(135)),
              shown(S(136)), shown(S(137)), shown(S(138)), shown(S(139)), shown(L(140, 141)), shown(S(142)),
              shown(S(143))], whole=True, rownote=_part2_note_2025,
      question=QP(4, 'Napíšte komentár', '„Tento svet', 'Potrebujeme milióny'), pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2025)],
      question=QP(4, ESSAY_2025, 'Svet, v ktorom')),
    R('III2', [unprinted(_part3_note_2025)],
      question=QP(4, ESSAY_2025, '„Objavovaním', 'Belo Kapolka', '(spisovateľ')),
]


# ====================================================================== 2026
# ================================================================ 2026 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched here (audited:
# see slovakian-live-faults-2018-2026.json).
# Paper (rendered pp2-4; renders slo-2026-sk-paper-p*.png): the rule (p2
# y124-138); the text "Chcete vedieť, či je huba jedovatá? Ochutnajte ju,
# radí umelá inteligencia." runs pp2-3 (title p2 y167, paragraphs 1-6 to the
# byline "Zuzana Vitková, DenníkN, uverejnené 26. septembra 2023" p3 y482);
# "ČASŤ I:" + "(30 bodov)" p3 y555, Q1 a bare "1." over a)-e) with "(5 × 1
# bodov)" beside e) (x454 y695); Q2-Q6 on p4 (Q5 printed "5 Uvažujte", no
# stop). p4: "ČASŤ II" + "(30 bodov)" (y407), "Napíšte komentár (100 – 150
# slov) v ktorom rozviniete tému:" and the statement (y465); "ČASŤ III" +
# "(40 bodov)" (y539), "Napíšte esej (najmenej 300 slov) na jednu z dvoch
# nasledovných tém:", "1. téma:" / "Alebo" / "2. téma:", title 2 a two-line
# quotation and "Tomáš Janovic" (x454 y736).
# PRICES: II1 "(30 bodov)", III1/III2 "(40 bodov)": PARTP. Scheme heads "ČASŤ
# II 30 bodov" (118), "ČASŤ III 40 bodov" (135).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-6 = printed pages 4-6; p3 the
# annotations table, pp7-8 blank but for page numbers):
# - NO "Poznámka", NO criteria and NO percentages anywhere in this scheme.
# - Part II (p6, 118-120): the head, the task reprinted as "Napíšte komentár
#   (najmenej 100 slov) na tému:" (119; the paper prints "(100 – 150 slov) v
#   ktorom rozviniete tému:") and the statement; then "Riziká sú napríklad
#   tieto:" (121, a heading line of its own) over six dashed points: 122-123,
#   124-125, 126-127, 128-129, 130-132, 133-134. No marks.
# - Part III (135-142): the head, the instruction reprinted as "Napíšte esej
#   (asi 300 slov) ..." (136; the paper prints "(najmenej 300 slov)") and both
#   titles: NOTHING else.
# SHAPES:
# - II1: points with no per-point marks and no criteria: one shown row per
#   dashed point, questionTotal on the paper's 30 (as 2025; Bulgarian
#   2025/2026); the heading "Riziká sú napríklad tieto:" in the first row's
#   note, never a row; the scheme's reworded task quoted (10f).
# - III1/III2: nothing printed for this part, no criteria anywhere: R4
#   (unprinted) at the paper's 40, the note quoting the scheme's reworded
#   instruction (10f).
# JUDGEMENT CALLS:
# - Point 2 prints "môžu sa zverejniť" (124; word order as printed): lifted.
# - II1's question: the instruction line and the statement, from the paper.
#   III1: the census welds the joiner "Alebo" onto title 1 ("...
#   inteligenciou? Alebo"); the title is cut from its own printed line.
#   III2: the two printed lines of the quotation and "Tomáš Janovic".
# - Reading text pp2-3 (rendered); II1 carries pages=(2, 3). The live 2026
#   cards carry [3] (flagged, P).
# GLYPHS: none in the lines used (render checked).

ESSAY_2026 = 'Napíšte esej'


def _part3_note_2026(d):
    return (f'Under “{S(135, before=" 40 bodov").text(d)}” the scheme reprints the instruction as “{S(136).text(d)}” and the two '
            f'titles; it prints no answer, no content and no criteria for this part, and no criteria anywhere in '
            f'this scheme.')


SPECS[2026] = [
    R('II1', [shown(L(122, 123)), shown(L(124, 125)), shown(L(126, 127)), shown(L(128, 129)), shown(L(130, 132)),
              shown(L(133, 134))], whole=True,
      rownote=both(quote(S(121), lead='The scheme heads these points'),
                   quote(S(119), lead='It reprints the task as')),
      question=QP(4, 'Napíšte komentár', '„Rastú aj'), pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2026)],
      question=QP(4, ESSAY_2026, 'Ľudská inteligencia')),
    R('III2', [unprinted(_part3_note_2026)],
      question=QP(4, ESSAY_2026, Run('„Život znamená', 'zmocnil.'), 'Tomáš Janovic')),
]
