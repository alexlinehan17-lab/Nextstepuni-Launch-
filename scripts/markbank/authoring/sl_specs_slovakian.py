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
