#!/usr/bin/env python3
"""Reviewed specs for the Croatian classic examination (small-languages lane).

One entry per printed ask with no live card; see sl_lib.py for the selector
language. Line numbers are lines of examiner-reports/croatian/schemes/<year>-hl.md.
Drafted by Opus helpers on the Bulgarian, Romanian, Dutch and Maltese models, integrated
and gated by the lane lead.
"""
from sl_lib import (R, S, SR, J, L, PL, PC, QP, QL, Run, pre, prerun, PP, SP, PY, RX, PaperP, PARTP, REM,  # noqa: F401
                    one, shown, graded, crit, examples, quote, unprinted, part, NoScheme)
from pl_listen_lib import Join  # noqa: F401

SPECS = {}


import re  # noqa: E402
from sl_lib import clean_question, MARKER  # noqa: E402


def _hr_says(lead, *sels):
    """A note quoting printed lines after a lead. A full stop follows the
    closing quotation mark only where the quotation does not already end in
    one (quote() always adds one: "tema.”."). The same helper is defined in
    each Croatian draft; keep one copy."""
    def note(d):
        body = ' '.join(f'“{s.text(d)}”' for s in sels)
        return f'{lead} {body}' + ('' if re.search(r'[.!?:][”“"’]*”$', body) else '.')
    return note


def _hr_q1(page, stem, *items):
    """Question 1 as printed: its stem (number and price taken off) and its
    five expression lines as the paper prints them, letter and paragraph
    number kept. QL cleans each expression line too, and its price strip takes
    a closing bare "(2)", here a paragraph number, for a price. The same helper
    is defined in each Croatian draft that needs it; keep one copy."""
    def question(doc, _census=None):
        lines = [PL(page, i).text(doc) for i in items]
        priced = [t for t in lines if re.search(r'\bbod', t)]
        if priced:
            raise ValueError(f'an expression line prints a price: {priced}')
        return '\n'.join([clean_question(MARKER.sub('', PL(page, stem).text(doc), count=1))] + lines)
    return question


def both(*notes):
    """Several printed notes on one row, in order."""
    return lambda doc: ' '.join(n(doc) for n in notes)


# ================================================================ 2014 HL ===
# Drafted (small-languages lane, 20 Nov): the open asks of this sitting, I1a-d,
# II1, III1, III2. Live: I1e, I2-I6 (6 cards); not touched.
# Paper (rendered pp2-4): the rule and the reading text "Lice i naličje
# hrvatskih medija ..." p2 y126-p3 y339 (source line "Prilagođeno prema: Božo
# Skoko ..." p3 y339); "I. DIO (30 bodova)" p3 y388; Q1 prints its stem over two
# lines and five expressions a)-e) in italics, each with its paragraph
# ("(2. odjeljak)"), and ONE "(5 bodova)" at the right of e)'s line (p3 y519);
# Q2-Q6 "(5 bodova)" each at the end of their own last line; "II. DIO (30
# bodova)" p4 y77 (three cells); "III. DIO (40 bodova)" p4 y254 ("DIO (40
# bodova)" one cell), instruction, two titles "1. tema:" / "2. tema:" in bold.
# PRICES:
# - Q1: the paper prices Question 1 only as a whole: "(5 bodova)" at the end of
#   its last line (e)), where Q2-Q6 print theirs; 6 x 5 = Part I's printed 30.
#   No per-expression price on paper or scheme (scheme line 55 reprints e) with
#   the same "(5 bodova)"). The census gives that price to e) alone (I1e
#   tariff 5) and reads none on the parent ask, so the card reads it from the
#   printed line (PaperP). Carded WHOLE at the parent key 'I1' (Romanian
#   2012-2018 precedent).
# - II1: "(30 bodova)", the cell on Part II's head (p4 y77). III1/III2: "DIO
#   (40 bodova)" (p4 y254). PARTP cannot read either: the census reads only
#   "I. DIO" (the numeral, the word and the price are three cells), so both are
#   read from the printed head (PaperP). The scheme prints the same 30 (129)
#   and 40 (144).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5; answers in bold):
# - Q1 (49-55 reprint the stem and the five expressions, "(5 bodova)"): then
#   five answers, each opening with its own letter: a) 56, b) 57-58, c) 59,
#   d) 60-61, e) 62-64. Paired by letter (the order and the letters agree with
#   the paper's). No split: shown, scored on the printed 5 (questionTotal).
# - Part II (128-132 reprint the head and the task): one bold paragraph,
#   133-143 ("Na temelju problema koje autor navodi, ..."), no heading, no
#   criteria. A model answer (10a): one shown row on the paper's 30.
# - Part III (144-149): the head, the instruction and the two titles
#   reprinted, nothing else (no answer, no criteria, no notes): R4
#   (unprinted) at the paper's 40, the note quoting the instruction.
# - No criteria or percentages anywhere in this scheme.
# SHAPES:
# - I1: shown rows, one per expression, whole=True on the paper's 5.
# - II1: one shown row, whole=True on the paper's 30.
# - III1/III2: unprinted at the paper's 40.
# JUDGEMENT CALLS:
# - CONFLICT WITH A LIVE CARD (for the lead): hrv-2014-hl-i-1-e is live at 5
#   marks with ONE claimable row joining all five answers a)-e) (lines 56-64,
#   letters included) and e)'s words as its question: it is in effect Q1 carded
#   whole under e)'s key. 'I1' below is what the brief's rule gives, but it
#   duplicates that card. Either keep I1 and retire/alias I1e (removing a live
#   card needs Alex), or drop I1 here and record I1a-d as covered by the live
#   I1e (its rows then need the live-card fix: one shown row per expression).
# - Q1's question is the paper's stem and its five lines, each with its letter
#   and paragraph, e)'s price taken off (QL).
# - II1 is shown, not claimed, although it is one paragraph: the scheme prints
#   it as a model for a 30-mark commentary with no points or marks (10a).
# - Part III title 1: the scheme reprints it as "Je li medijsku slobodu
#   izvještavanja moguće je pomiriti s odgovornošću? Raspravite o tome." (146-
#   147; paper: "... moguće pomiriti s odgovornošću?"): the paper wins on the
#   question, the scheme's words quoted on that card (10f). Title 2: same words.
# - III questions keep the paper's "1. tema:" / "2. tema:" labels
#   (keep_marker): taking the number off leaves "tema: Je li ...". Title 2 keeps
#   its attribution cell "R.W. Emerson".
# - Reading text: pp2-3 (rendered). The live 2014 cards carry
#   sourceMaterial.pages [3], which the render does not agree with (p2 holds
#   the rule, the title and paragraphs 1-5): (2, 3) here; flagged, not changed.
# GLYPHS: the scheme's reprint of c) (line 53) prints a control character,
# U+001F, between "p" and "d" ("obrisati p\x1fd nekim"; rendered p3 as an
# empty box, "p□d"); the .md drops it ("obrisati pd nekim"). Not used by any
# row or question here. The paper itself prints "navdenoga" (p2, the rule) and
# the scheme "zakonao medijima", "postiogli": the SEC's own typing, kept.


ESSAY_2014 = _hr_says('Under Part III the scheme reprints only the instruction and the two titles, with no '
                      'answer, criteria or notes:', S(145))
P3_2014 = PaperP(4, 'DIO (40 bodova)')
# Ruling 14 (coordinator, 20 Nov): the live hrv-2014-hl-i-1-e becomes the whole-Q1 card (it held all five
# glosses at Q1's printed 5); the I1 drafted here is dropped. Its spec, for the record: five shown rows
# S(56)/L(57,58)/S(59)/L(60,61)/L(62,64) after each letter, on PaperP(3, 'e) stvaranje idola').
SPECS[2014] = [
    R('II1', [shown(L(133, 143))], whole=True, total=PaperP(4, '(30 bodova)'), pages=(2, 3)),
    R('III1', [unprinted(both(ESSAY_2014, _hr_says('The scheme reprints this title as',
                                                   L(146, 147, after='tema: '))))],
      total=P3_2014,
      question=QP(4, 'Napišite raspravljački', '1. tema:', keep_marker=True)),
    R('III2', [unprinted(ESSAY_2014)], total=P3_2014,
      question=QP(4, 'Napišite raspravljački', Run('2. tema:', 'R.W. Emerson'), keep_marker=True)),
]


# ================================================================ 2015 HL ===
# Drafted (small-languages lane, 20 Nov): the open asks of this sitting, I1a-e,
# II1, III1, III2. Live: I2-I6 (5 cards); not touched.
# GLYPHS FIRST: this sitting's scheme .md carries the Georgia fonts' broken
# ToUnicode map: U+00FE "þ" where the render prints č, U+00FC "ü" for ć, U+00FF
# "ÿ" for đ, U+00FD "ý" for Č, U+0108 "Ĉ" for Đ (91 lines; rendered scheme
# pp3-6 print the right letters, e.g. p3 "Sigurno ćemo dobiti jedinicu", "sačuvan",
# "uzbuđenje"). The paper's text layer is clean. Rows below that carry them:
# I1b (126 "saþuvan"), I1d (130 "üemo", "mimoiüi"), I1e (133-134 "Ushiüenje,
# uzbuÿenje", "neþega", "þime üemo", "uþiniti"), II1 (190-199, e.g.
# "meÿudruštvenih", "postiüi", "þije", "osjeüaju", "vrtiüu", "djeþjeg"), and the
# quoted notes (187 "rijeþima", "reþenicu"; 201 "sljedeüih"). NOT repaired here
# (never a hand map): repair_scheme_glyphs.py --check REFUSES this file (its
# MANGLED class, U+0100-U+1FFF, takes the real č ć š ž Š for mangled and does
# not cover U+00FC-U+00FF), so the .md needs a glyph-id repair the lane's tool
# cannot do yet before these cards ship. The specs are written on the current
# line numbers and no anchor holds a mangled letter, so an in-place repair
# keeps them valid. (The live 2015 cards I2-I6 already carry these letters.)
# Paper (rendered pp2-4): rule, "I. dio [30 bodova]" and the author's note p2;
# the text "VOĐA IZ ŠKOLSKOG ZAHODA" p2 y338 to its source line p3 y477; Q1
# p3 y560 "1. Objasnite svojima riječima sljedeće pojmove: [5 bodova]", five
# expressions a)-e) each with its paragraph number "(2)", no price of their
# own; Q2-Q6 "[5 bodova]" each (p4); "II. dio [30 bodova]" p4 y515 (numeral and
# "dio [30 bodova]" two cells); "III. dio [40 bodova]" p4 y664, instruction and
# two titles.
# PRICES:
# - Q1: "[5 bodova]" on the stem's own line, for the question as a whole (5 +
#   5 x 5 = Part I's 30). The census "walked" it down to 1 per expression
#   (I1a-e tariff (1, 1, 1)); the paper prints no per-expression price and the
#   scheme none either (122 reprints the stem with "[5 bodova]"). Carded WHOLE
#   at 'I1' on the parent ask's printed price (PP(): the census reads
#   "[5 bodova]" there).
# - II1 "dio [30 bodova]", III1/III2 "dio [40 bodova]" (PaperP: the census reads
#   no part heads this sitting). The scheme prints the same (185, 200).
# WHAT THE SCHEME PRINTS (rendered pp3-6; answers in italics):
# - Q1: each expression reprinted on its own line with its paragraph number,
#   its answer on the line(s) below: a) 124, b) 126, c) 128, d) 130-131,
#   e) 133-134. Letters agree with the paper's. No split: shown on the 5.
# - Part II (185-188 reprint the head and the task): the italic heading "Na
#   primjer" (189) and one italic paragraph, 190-199 ("Pravda opisuje idealno
#   stanje ..."). No criteria: a model (10a), shown on the paper's 30 under
#   its heading.
# - Part III (200-203): the head, the instruction and the two titles, nothing
#   else: R4 (unprinted) at 40, the note quoting the instruction.
# JUDGEMENT CALLS:
# - Q1's question keeps each expression's paragraph number as printed
#   ("a) kompleksnih (2)"): QL's price strip would take a closing bare "(2)"
#   for a price, so the expression lines are taken as printed (_hr_q1, which
#   refuses a line with a price word). Live 2016/2018 Q1 cards drop the number.
# - The paper prints Part II's task with a misprint, "vlastitim triječima"
#   (rendered p4); the scheme reprints "vlastitim riječima". The paper's words
#   stand in the question; the misprint and the scheme's reprint are quoted
#   on the row (10f).
# - Part III title 2: the scheme sets "~ Sokrat" for the paper's "(Sokrat)":
#   punctuation only, not quoted. Title 1: the same words (mangled letters only).
# - Reading text pp2-3 (rendered). The live 2015 cards carry [2, 3]: agree.


def _misprint_2015(d):
    return (f'The paper prints the task with “{PC(4, "vlastitim", before=",").text(d)}”, a misprint; the '
            f'scheme reprints it as “{S(187, before=",").text(d)}”.')


P2_2015 = PaperP(4, 'dio [30')
P3_2015 = PaperP(4, 'dio [40')
ESSAY_2015 = _hr_says('Under Part III the scheme reprints only the instruction and the two titles, with no '
                      'answer, criteria or notes:', S(201))
SPECS[2015] = [
    R('I1', [shown(S(124)), shown(S(126)), shown(S(128)), shown(L(130, 131)), shown(L(133, 134))],
      whole=True,
      note=('The paper prices Question 1 only as a whole, "[5 bodova]" on its stem; the scheme answers '
            'each expression and prints no split.'),
      question=_hr_q1(3, '1. Objasnite', 'a) kompleksnih', 'b) pohranjen', 'c) dvolične', 'd) „Jedinice',
                      'e) „pravednički'),
      pages=(2, 3)),
    R('II1', [shown(L(190, 199))], whole=True, total=P2_2015,
      rownote=both(_hr_says('The scheme heads it', S(189)), _misprint_2015),
      pages=(2, 3)),
    R('III1', [unprinted(ESSAY_2015)], total=P3_2015,
      question=QP(4, 'Napišite esej', '1. „Vođe')),
    R('III2', [unprinted(ESSAY_2015)], total=P3_2015,
      question=QP(4, 'Napišite esej', '2. „Najbogatiji')),
]


# ================================================================ 2016 HL ===
# Drafted (small-languages lane, 20 Nov): the open asks of this sitting, II1,
# III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched.
# Paper (rendered pp2-4): rule p2 y118-147; the text "ŽIVOT NA KOTAČIMA" p2
# y195 to its source line p3 y721; questions p4; "II. dio [30 bodova]" p4 y525
# (numeral and "dio [30 bodova]" two cells), a quotation from the text and
# "Komentirajte, vlastitim riječima (minimalno 100 riječi), ovu misao.";
# "III. dio [40 bodova]" p4 y658, instruction and two titles.
# PRICES: II1 "dio [30 bodova]", III1/III2 "dio [40 bodova]" (PaperP: the census
# reads no part heads this sitting). The scheme prints the same (117, 147).
# WHAT THE SCHEME PRINTS (rendered pp4-5; content in italics):
# - Part II (117-121, p4): the head and the task reprinted, then on p5 the
#   italic heading "Na primjer:" (126) and five italic paragraphs, each opening
#   a new line after a short last line (rendered p5): 127-131, 132-133,
#   134-139, 140-142, 143-146. No criteria: a model (10a), one shown row per
#   printed paragraph, scored on the paper's 30.
# - Part III (147-152): the head, instruction and two titles reprinted,
#   nothing else: R4 (unprinted) at 40, the note quoting the instruction.
# JUDGEMENT CALLS:
# - Part II: the scheme reprints a DIFFERENT quotation from the one the paper
#   sets: scheme 118-120 "„„Komfor nije stvar materijalnog obilja, nego
#   zadovoljstva unutarnje sigurnosti. [...] Nakon zadovoljenja osnovnih
#   materijalnih potreba, najvažniji je unutarnji doživljaj života.”" (a
#   doubled „„ as printed), paper p4 "„Kvaliteta života nije istoznačnica s
#   kvantitetom – novca, stvari ili prostora. [...] Komfor nije stvar ...
#   sigurnosti.”". The paper wins on the question; the scheme's reprint is
#   quoted on the row (10f). The model paragraphs answer the shared idea.
# - Part III titles: punctuation only between paper and scheme (title 1 "”. –"
#   / "” –"; title 2 "”." / "” –"), not quoted.
# - Reading text pp2-3 (rendered). The live 2016 cards carry [2, 3]: agree.
# GLYPHS: none in the lines used.


P3_2016 = PaperP(4, 'dio [40')
ESSAY_2016 = _hr_says('Under Part III the scheme reprints only the instruction and the two titles, with no '
                      'answer, criteria or notes:', S(148))
SPECS[2016] = [
    R('II1', [shown(L(127, 131)), shown(L(132, 133)), shown(L(134, 139)), shown(L(140, 142)),
              shown(L(143, 146))],
      whole=True, total=PaperP(4, 'dio [30'),
      rownote=both(_hr_says('The scheme heads it', S(126)),
                   _hr_says('The scheme reprints the task with a different quotation from the one the '
                            'paper sets:', L(118, 120))),
      pages=(2, 3)),
    R('III1', [unprinted(ESSAY_2016)], total=P3_2016,
      question=QP(4, 'Napišite esej', '1. „Usvojite')),
    R('III2', [unprinted(ESSAY_2016)], total=P3_2016,
      question=QP(4, 'Napišite esej', Run('2. „Svijet', '- Fintan'))),
]


# ================================================================ 2017 HL ===
# Drafted (small-languages lane, 20 Nov): the open asks of this sitting, I1a-e,
# II1, III1, III2. Live: I2-I6 (5 cards); not touched.
# Paper (rendered pp2-4): rule p2 y104-133; the text "Društvene mreže - život za
# tuđi pogled?" p2 y165, paragraphs 1-11 on pp2-3, paragraph 12 and the source
# line "(prilagođeno prema: Ozren Podnar, www.sensaklub.hr)" at the TOP of p4
# (y64-115); "I. dio [30 bodova]" p4 y142; Q1 p4 y170 "1. Objasnite svojima
# riječima sljedeće pojmove: [5 bodova]", five expressions a)-e) each with its
# paragraph number "(1)", no price of their own; Q2-Q6 "[5 bodova]" each;
# "II. dio [30 bodova]" p4 y574 (two cells); "III. dio [40 bodova]" p4 y652,
# instruction and two titles.
# PRICES:
# - Q1: "[5 bodova]" on the stem's own line, for the question as a whole (5 +
#   5 x 5 = Part I's 30). The census walked it down to 1 per expression; the
#   paper and the scheme (142) print no per-expression price. Carded WHOLE at
#   'I1' on the parent ask's printed price (PP(), "[5 bodova]").
# - II1 "dio [30 bodova]", III1/III2 "dio [40 bodova]" (PaperP: the census reads
#   no part heads). The scheme prints the same (221, 243).
# WHAT THE SCHEME PRINTS (rendered pp3-7): the scheme reprints the whole
# reading text (50-141) before the answers.
# - Q1 (142 reprints the stem, "[5 bodova]"): each expression and its
#   paragraph number with the answer on the same line, running on: a) 143,
#   b) 144, c) 145-146, d) 147-148, e) 149-150; cut after the paragraph
#   number. Letters agree with the paper's. No split: shown on the 5.
# - Part II (221-224 reprint the head and the task): the italic heading "Na
#   primjer:" (225) and six italic dashes, 226-227, 228-230, 231-232, 233-235,
#   236-240, 241-242 (rendered p7). No criteria: shown, one row per dash, on
#   the paper's 30 (10a).
# - Part III (243-248): the head, instruction and two titles reprinted,
#   nothing else: R4 (unprinted) at 40, quoting the instruction.
# JUDGEMENT CALLS:
# - Q1's question keeps each expression's paragraph number as printed (see
#   _hr_q1; QL's price strip would take "(1)" for a price).
# - Part III title 2: the scheme reprints it with a word the paper does not
#   print, "Moje je mišljenje je jednako dobro ..." (246; paper "Moje je
#   mišljenje jednako dobro ..."): the paper wins on the question, the
#   scheme's words quoted on that card (10f). Title 1: the same.
# - Reading text pp2-4: the text runs onto p4 (paragraph 12 and the source
#   line, rendered). The live 2017 cards carry NO sourceMaterial at all:
#   flagged for the lead, not changed. pages=(2, 3, 4) here.
# GLYPHS: none in the lines used.


P3_2017 = PaperP(4, 'dio [40')
ESSAY_2017 = _hr_says('Under Part III the scheme reprints only the instruction and the two titles, with no '
                      'answer, criteria or notes:', S(244))
SPECS[2017] = [
    R('I1', [shown(S(143, after='(1) ')), shown(S(144, after='(5) ')), shown(L(145, 146, after='(12) ')),
             shown(L(147, 148, after='(2) ')), shown(L(149, 150, after='(6) '))],
      whole=True,
      note=('The paper prices Question 1 only as a whole, "[5 bodova]" on its stem; the scheme answers '
            'each expression and prints no split.'),
      question=_hr_q1(4, '1. Objasnite', 'a) suparnice', 'b) potištenost', 'c) utočište', 'd)', 'e)'),
      pages=(2, 3, 4)),
    R('II1', [shown(L(226, 227)), shown(L(228, 230)), shown(L(231, 232)), shown(L(233, 235)),
              shown(L(236, 240)), shown(L(241, 242))],
      whole=True, total=PaperP(4, 'dio [30'),
      rownote=_hr_says('The scheme heads it', S(225)),
      pages=(2, 3, 4)),
    R('III1', [unprinted(ESSAY_2017)], total=P3_2017,
      question=QP(4, 'Napišite esej', '1. „Tko sam')),
    R('III2', [unprinted(both(ESSAY_2017, _hr_says('The scheme reprints this title as',
                                                   L(246, 248, after='2. '))))],
      total=P3_2017,
      question=QP(4, 'Napišite esej', Run('2. „Moje', 'medija.'))),
]


# ================================================================ 2018 HL ===
# Drafted (small-languages lane, 20 Nov): the open asks of this sitting, II1,
# III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched.
# Paper (rendered pp2-4; the booklet numbers PDF p3 as its page 2): rule and
# "I. dio [30 bodova]" p2; the text from p2 to its source line "(prilagođeno
# prema: Gabrijela Radanović ...)" p3 y620; Q1 at the foot of p3; Q2-Q6 p4;
# "II. dio [30 bodova]" p4 y443 (numeral, "dio" and "[30 bodova]" three
# cells), a quotation from paragraph 7 and "Komentirajte, vlastitim riječima
# (minimalno 100 riječi), ovu misao."; "III. dio [40 bodova]" p4 y600,
# instruction, two titles joined by "ili".
# PRICES: II1 "[30 bodova]", III1/III2 "[40 bodova]", each a cell on its part's
# head (PaperP: the census reads no part heads beyond Part I). The scheme
# prints the same (144, 176).
# WHAT THE SCHEME PRINTS (rendered pp5-6; content in italics):
# - Part II (144-148 reprint the head and the task): the italic heading "Na
#   primjer:" (149) and four italic dashes, 150-152, 153-159 and, over the p5/p6
#   break (160-163 are the page number and head, left out), 164-170 and
#   171-175. No criteria: shown, one row per dash, on the paper's 30 (10a).
# - Part III (176-181): the head, instruction and two titles reprinted,
#   nothing else: R4 (unprinted) at 40, quoting the instruction.
# JUDGEMENT CALLS:
# - Part III title 2: the scheme reprints it with other words, "Do koje je
#   mjere moguće reći da se o ljudima može donijeti ispravna prosudba na
#   temelju odjeće koju nose?" (179-181; paper "... da se ljude može ispravno
#   prosuditi na temelju odjeće koju nose?"): the paper wins on the question,
#   the scheme's words quoted on that card (10f). Title 1: the same words.
# - Part II: the scheme's reprint of the task closes the quotation with “ for
#   the paper's ”: punctuation only, not quoted.
# - Reading text pp2-3 (rendered). The live 2018 cards carry [2, 3]: agree.
# GLYPHS: none in the lines used.


P3_2018 = PaperP(4, '[40 bodova]')
ESSAY_2018 = _hr_says('Under Part III the scheme reprints only the instruction and the two titles, with no '
                      'answer, criteria or notes:', S(177))
SPECS[2018] = [
    R('II1', [shown(L(150, 152)), shown(L(153, 159)), shown(L(164, 170)), shown(L(171, 175))],
      whole=True, total=PaperP(4, '[30 bodova]'),
      rownote=_hr_says('The scheme heads it', S(149)),
      pages=(2, 3)),
    R('III1', [unprinted(ESSAY_2018)], total=P3_2018,
      question=QP(4, 'Napišite esej', '1. „Nisu svi')),
    R('III2', [unprinted(both(ESSAY_2018, _hr_says('The scheme reprints this title as',
                                                   L(179, 181, after='2. '))))],
      total=P3_2018,
      question=QP(4, 'Napišite esej', Run('2. „Odijelo', 'argumente za i protiv'))),
]


# ================================================================ 2019 HL ===
# Drafted (small-languages lane, 20 Nov): the open asks of this sitting, II1,
# III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched.
# Paper (rendered pp2-4): rule and "I. dio [30 bodova]" p2; the text
# "EPIDEMIJA AMNEZIJE I NESTANAK ZABORAVA" p2 y169, "Scenarij A" p2, "Scenarij
# B" p3, to the source line "(prilagođeno prema: Iva Biondić, Storybook, Jesen
# 3/2018)" p3 y735; Q1-Q6 p4; "II. dio [30 bodova]" p4 y488 (three cells), a
# quotation from the film and the task; "III. dio [40 bodova]" p4 y636,
# instruction, two titles with "Ili" between them on a line of its own.
# PRICES: II1 "[30 bodova]", III1/III2 "[40 bodova]", cells on the part heads
# (PaperP: the census reads only Part I's head). The scheme prints the same
# totals (159, 187) under the wrong part numbers (below).
# WHAT THE SCHEME PRINTS (rendered pp5-6; content in italics):
# - Part II (159-166 reprint the head and the task): the italic heading "Na
#   primjer:" (167) and two italic dashes, 168-173 continued over the p5/p6
#   break (174-177 are the page number and head, left out) at 178-182, and
#   183-186. No criteria: shown, one row per dash, on the paper's 30 (10a).
# - Part III (187-192): the head, instruction and two titles reprinted,
#   nothing else: R4 (unprinted) at 40, quoting the instruction.
# JUDGEMENT CALLS:
# - The scheme MISNUMBERS both parts: it heads Part II "I. dio [30 bodova]"
#   (159) and Part III "II. dio [40 bodova]" (187) (rendered p5, p6), after
#   Part I's answers. The paper's parts, tasks and totals pair them
#   unambiguously (the same task words, 30 and 40); the paper wins, and the
#   scheme's heads are quoted on each card (10f: a printed SEC error).
# - Part II's first dash runs over the page break: joined (J) across the page
#   furniture.
# - III questions: instruction and title cut from the paper's lines; the "Ili"
#   between the titles is a line of its own and is left out.
# - Reading text pp2-3 (rendered). The live 2019 cards carry pages [2], which
#   the render does not agree with (p3 holds paragraphs 4-9 and the source
#   line): (2, 3) here; flagged, not changed.
# GLYPHS: none in the lines used.


def _misnumbered_2019(n, part):
    return lambda d: (f'The scheme misnumbers this part: it heads it “{S(n).text(d)}”, where the paper '
                      f'prints it as Part {part}.')


P3_2019 = PaperP(4, '[40 bodova]')
ESSAY_2019 = both(_misnumbered_2019(187, 'III'),
                  _hr_says('Under it the scheme reprints only the instruction and the two titles, with no '
                           'answer, criteria or notes:', S(188)))
SPECS[2019] = [
    R('II1', [shown(J(L(168, 173), L(178, 182))), shown(L(183, 186))],
      whole=True, total=PaperP(4, '[30 bodova]'),
      rownote=both(_hr_says('The scheme heads it', S(167)), _misnumbered_2019(159, 'II')),
      pages=(2, 3)),
    R('III1', [unprinted(ESSAY_2019)], total=P3_2019,
      question=QP(4, 'Napišite esej', '1. „Znaš')),
    R('III2', [unprinted(ESSAY_2019)], total=P3_2019,
      question=QP(4, 'Napišite esej', Run('2. „Odlazak', 'vremena?'))),
]


# ================================================================ 2020 HL ===
# Drafted (small-languages lane, 20 Nov): the open asks of this sitting, I1a-e,
# II1, III1, III2. Live: I2-I6 (5 cards); not touched.
# Paper (rendered pp2-4): rule and "I. dio [30 bodova]" p2 y106-162; the text
# "U potrazi za srećom" p2 y191 to the byline "Pavao Pavličić (kolumna ...)" p3
# y572; Q1 p3 y606 "1. Objasnite svojima riječima sljedeće pojmove:" with
# "[5 bodova]" as a cell at its right (x476), five expressions a)-e) each with
# its paragraph "(2. odlomak)", no price of their own; Q2-Q6 "[5 bodova]" each
# (p4); "II. dio [30 bodova]" p4 y395 (three cells); "III. dio [40 bodova]" p4
# y547, instruction and two titles.
# PRICES:
# - Q1: "[5 bodova]" beside the stem, for the question as a whole (5 + 5 x 5 =
#   Part I's 30). The census walked it down to 1 per expression; the paper and
#   the scheme (118) print no per-expression price. Carded WHOLE at 'I1' on
#   the parent ask's printed price (PP(), "[5 bodova]").
# - II1 "[30 bodova]", III1/III2 "[40 bodova]" (PaperP: the census reads only
#   Part I's head). The scheme prints the same, heading the parts "2. dio" and
#   "3. dio" (187, 200).
# WHAT THE SCHEME PRINTS (rendered pp5-6; answers in italics): the scheme
# reprints the whole reading text (50-117) first.
# - Q1 (118 reprints the stem, "[5 bodova]"): each expression with its
#   paragraph number "(2)" and the answer on the same line, running on:
#   a) 119-120, b) 121, c) 126-127, d) 128-129, e) 130-131 (the p4/p5 break,
#   122-125, falls between b) and c)); cut after the paragraph number. Letters
#   agree with the paper's. No split: shown on the 5.
# - Part II (187-190 reprint the head and the task): one italic paragraph,
#   191-199 ("Autor time želi reći ..."), no heading, no criteria: a model
#   (10a), one shown row on the paper's 30.
# - Part III (200-204): the head, instruction and two titles reprinted,
#   nothing else: R4 (unprinted) at 40, quoting the instruction.
# JUDGEMENT CALLS:
# - Part II: the scheme reprints the task as "U 11. odlomku autor zaključuje:
#   ..." (188) for the paper's "U jedanaestome odlomku autor zaključuje: ...":
#   the same sense, other words; the paper wins, the scheme's line quoted
#   (10f). Part III title 2 drops the paper's full stop: punctuation only.
# - Q1's question is the paper's stem and its five lines (QL; the paragraph
#   references "(2. odlomak)" survive its price strip). The scheme numbers them
#   "(2)" where the paper prints "(2. odlomak)": not quoted.
# - Reading text pp2-3 (rendered). The live 2020 cards carry [2, 3]: agree.
# GLYPHS: none in the lines used.


P3_2020 = PaperP(4, '[40 bodova]')
ESSAY_2020 = _hr_says('Under Part III the scheme reprints only the instruction and the two titles, with no '
                      'answer, criteria or notes:', S(201))
SPECS[2020] = [
    R('I1', [shown(L(119, 120, after='(2) ')), shown(S(121, after='(6) ')), shown(L(126, 127, after='(3) ')),
             shown(L(128, 129, after='(5) ')), shown(L(130, 131, after='(7) '))],
      whole=True,
      note=('The paper prices Question 1 only as a whole, "[5 bodova]" beside its stem; the scheme answers '
            'each expression and prints no split.'),
      question=QL(3, '1. Objasnite', 'a) cupka', 'b) nelogično', 'c) „vedro', 'd) „prebirati', 'e) „poljuljati'),
      pages=(2, 3)),
    R('II1', [shown(L(191, 199))], whole=True, total=PaperP(4, '[30 bodova]'),
      rownote=_hr_says('The scheme reprints the task as', S(188)),
      pages=(2, 3)),
    R('III1', [unprinted(ESSAY_2020)], total=P3_2020,
      question=QP(4, 'Napišite esej', '1. „Vječna')),
    R('III2', [unprinted(ESSAY_2020)], total=P3_2020,
      question=QP(4, 'Napišite esej', '2. Sreća')),
]


# ================================================================ 2021 HL ===
# Drafted (small-languages lane, 20 Nov): the 2 asks with no live card.
# Live: I1a-e, I2-I6 (10 cards); not touched. Open here: II1, II2, the two
# essay titles. Two parts: "I. dio" "(30 bodova)" (p2 y136) and "II. dio"
# "(40 bodova)" (p4 y597, PARTP), the essay; "Ukupna ocjena [70 bodova]"
# (p2 y106). Rule: "Svi odgovori moraju biti na hrvatskome jeziku." (p2 y80).
# PRICES: II1/II2 the part head's "(40 bodova)" (PARTP; the census reads
# 'II. dio': 40). The scheme prints "II. dio [40 bodova]" (line 141). No
# other price on the titles (rendered p4: none beside either title).
# WHAT THE SCHEME PRINTS (rendered scheme p5; pp6-7 blank):
# - "II. dio [40 bodova]" (141), the instruction reprinted as "Napišite esej
#   (minimalno 300 riječi) o jednoj od sljedećih tema:" (142), both titles
#   (143-146), then ONE starred descriptive line: "*učenici trebaju napisati
#   esej (minimalno 300 riječi) u kojem će pokazati da razumiju značenje
#   zadane/odabrane teme" (147-148). No criteria, no percentages, no content,
#   no split anywhere in the scheme (the exclusion's "NOTHING beyond the SEC's
#   own wording and the titles" misses the starred line).
# SHAPES:
# - II1, II2: only a descriptive line for the part -> R4 (unprinted) at the
#   paper's 40, the note quoting the starred line (brief ruling 4).
# JUDGEMENT CALLS:
# - The starred line read as a descriptive line, not indicative content: it
#   states what the essay must show (that the candidate understands the
#   title), names no content.
# - The scheme's instruction "(minimalno 300 riječi)" for the paper's "(od
#   najmanje 300 riječi)": the paper wins on the question, the scheme's words
#   quoted (10f).
# - Title 2: the scheme sets ”...čujete.” (Greta Thunberg) where the paper
#   sets „...čujete” - Greta Thunberg: punctuation only, not quoted.
# - Questions cut from the paper's lines, instruction first (the census glues
#   "ili" to title 1 and gives no instruction).
# - No `pages` on Part II: a two-part sitting's Part II is the essay (sl_lib
#   attaches no reading text to it).
# LIVE PAGES: the reading text runs pp2-3 (rendered: title "ČOVJEK I DRVO" p2
#   y209, paragraphs 1-6 and the footnote on p2, paragraphs 7-14 and the
#   source line "(prilagođeno prema: ... kolovoz 2019.)" on p3 y733; questions
#   on p4). The live 2021 cards carry [2]: the render does not agree, (2, 3)
#   is right; flagged for the lead.
# LIVE CARDS (not mine; flagged for the lead): the five live Q1 cards
#   (hrv-2021-hl-i-1-a..e) carry the paper's p2 FOOTNOTE as their question
#   ("Tvrtka Zrinjevac projektira, uređuje i održava ... u Zagrebu. očaravaju")
#   in place of the instruction "Objasnite svojima riječima sljedeće pojmove:"
#   (p4 y91). The census still glues that footnote to I1a-e. Their rows are
#   the scheme's glosses (lines 48-54): right.
# GLYPHS: none (č ć đ š ž read cleanly on paper and scheme; the scheme's U+2010
#   HYPHEN before "Ralph Waldo Emerson" is a printed hyphen).


def _essay_2021(d):
    return (f'Under Part II the scheme reprints the instruction as “{S(142).text(d)}” and the two titles, and '
            f'prints only “{L(147, 148).text(d)}”. It prints no criteria and no split of the part\'s marks.')


ESSAY_2021 = 'Napišite esej (od najmanje 300'
SPECS[2021] = [
    R('II1', [unprinted(_essay_2021)],
      question=QP(4, ESSAY_2021, '1. „Svaki zid')),
    R('II2', [unprinted(_essay_2021)],
      question=QP(4, ESSAY_2021, Run('2. „Ne možete', '- Greta Thunberg'))),
]


# ================================================================ 2022 HL ===
# Drafted (small-languages lane, 20 Nov): the 7 asks with no live card.
# Live: I2-I6 (5 cards); not touched. Open here: I1a-e, II1, II2. Two parts:
# "I. dio" "(30 bodova)" (p2 y136) and "II. dio" "(40 bodova)" (p4 y601,
# PARTP), the essay; "Ukupna ocjena [70 bodova]" (p2 y92). Rule: "Svi
# odgovori moraju biti na hrvatskome jeziku." (p2 y92).
# PRICES:
# - I1a-e: the paper prints "[5 × 1 bod]" at the right of Q1's head line
#   (p4 y65, rendered: "1. Objasnite svojima riječima sljedeće pojmove:
#   [5 × 1 bod]") -- a price per expression, five at 1 mark, adding to 5.
#   The census walks it down to each letter (tariff 1 each): PP(). Per letter,
#   as the live 2021, 2024-2026 Q1 cards. The scheme prints the same "[5 × 1
#   bod]" (line 137).
# - II1/II2: the part head's "(40 bodova)" (PARTP); the scheme prints "II. dio
#   (40 bodova)" (223). No other price on the titles (rendered p4).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-7; pp8-9 blank):
# - pp3-4 (46-132) reprint the paper's rule, Part I head and the whole reading
#   text; p5 (137-145) Q1: each letter reprints the paper's expression and its
#   paragraph number, then the answer on the same line (italic for a, b, c, e;
#   roman for d), one gloss each, synonyms joined by commas and semicolons.
#   The exclusions' "the scheme prices no ask that pairs with it" is wrong:
#   the letters a)-e) pair one to one with the paper's, expression for
#   expression.
# - Part II (p7, 223-227): the head, the instruction and both titles
#   reprinted, and NOTHING under them (no descriptive line, no criteria, no
#   content; rendered p7 is otherwise blank).
# SHAPES:
# - I1a-e: one stated answer each -> one(row cut after the reprinted
#   expression and its paragraph number, PP()) at 1.
# - II1, II2: nothing printed for the part -> R4 (unprinted) at the paper's 40,
#   the note saying what the scheme does print (brief ruling 4).
# JUDGEMENT CALLS:
# - Q1 questions are the census's text (instruction + expression), matching the
#   live 2024-2026 Q1 cards; the census drops the paragraph number the paper
#   prints after each expression ("(2)", "(6)", ...) as it does on the live
#   cards. The paper sets the word to explain in BOLD inside a) "dobrovoljna
#   davateljica" and c) "neizmjerno zahvalan" (rendered p4: "dobrovoljna",
#   "neizmjerno" bold); the question text cannot carry the bold. Flagged, not
#   changed (the scheme's answers gloss a) "dobrovoljna" and c) the whole
#   phrase).
# - Q1(e)'s answer prints three glosses including "koji pripada starom rodu"
#   (masculine, after the feminine "ona koja ..."): lifted as printed.
# - Title 2: the scheme sets "„Kako se gradi istinsko prijateljstvo?" (an
#   opening „, never closed) where the paper prints no quotation marks:
#   punctuation only, not quoted.
# - Questions II1/II2 cut from the paper's lines, instruction first (the census
#   glues "Ili" to title 1 and gives no instruction).
# - No `pages` on Part II (a two-part sitting's Part II is the essay).
# LIVE PAGES: the reading text runs pp2-3 (rendered: title "ŽIVOT PIŠE ROMANE"
#   p2 y209, paragraphs 1-6 on p2, 7-13 and the source line "(prilagođeno
#   prema: Lada Novak Starčević, Jutarnji list, prosinac 2021.)" on p3 y758;
#   questions on p4). The live 2022 cards carry [2, 3]: they agree.
# LIVE CARDS (not mine; flagged for the lead, "Live-card answer fixes"
#   ruling): ALL FIVE live cards hrv-2022-hl-i-2..6 carry rows lifted from the
#   scheme's REPRINT of the reading text (pp3-4), not from its answers: I2 the
#   text's paragraph 2 ("postala je dobrovoljna davateljica krvi ...", line 55),
#   I3 paragraph 3 (61-), I4 paragraph 4 (65-), I5 paragraph 5 (71-), I6
#   paragraph 6 (80-). The scheme's answers are I2 148-155, I3 158-167, I4
#   170-176 (scheme p5), I5 184-194, I6 "Na primjer:" 199 and four dashes
#   200-218 (scheme p6). Every one of these live cards shows a wrong answer.
# GLYPHS: none (č ć đ š ž read cleanly; U+2010 HYPHEN in the paper's and the
#   scheme's "Kliničko‐bolničkog" is a printed hyphen, not used here).

PAGES_2022 = (2, 3)
SPECS[2022] = [
    R('I1a', [one(L(138, 139, after='davateljica(2) '), PP())], pages=PAGES_2022),
    R('I1b', [one(S(140, after='ugrožen (6) '), PP())], pages=PAGES_2022),
    R('I1c', [one(S(141, after='zahvalan (12) '), PP())], pages=PAGES_2022),
    R('I1d', [one(L(142, 143, after='neizvjesnosti (13) '), PP())], pages=PAGES_2022),
    R('I1e', [one(L(144, 145, after='plemenita (13) '), PP())], pages=PAGES_2022),
    R('II1', [unprinted('The scheme reprints the part\'s head, the instruction and the two titles, and '
                        'prints nothing under them: no criteria and no split of the '
                        'part\'s marks.')],
      question=QP(4, 'Napišite esej (od najmanje', '1. „Ništa nije')),
    R('II2', [unprinted('The scheme reprints the part\'s head, the instruction and the two titles, and '
                        'prints nothing under them: no criteria and no split of the '
                        'part\'s marks.')],
      question=QP(4, 'Napišite esej (od najmanje', '2. Kako se gradi')),
]


# ================================================================ 2023 HL ===
# Drafted (small-languages lane, 20 Nov): the 9 asks with no live card.
# Live: I2, I4, I5, I6 (4 cards); not touched (but see LIVE CARDS below).
# Open here: I1a-e, I3, II1, III1, III2.
# Paper (rendered pp2-4): "Ukupna ocjena [100 bodova]" (p2 y65); the rule
# "Svi odgovori moraju biti na hrvatskome jeziku." ends the instruction (p2
# y124); "I. dio" "(30 bodova)" (p2 y153); reading text p2 y200 to the source
# line p3 y629; Q1 p3 y669-780 with "[5 × 1 bod]" at the right of e) (p3
# y780); Q2-Q6 "[5 bodova]" each on a line of their own (p4); "II. dio" "(30
# bodova)" (p4 y468); "III. dio" "(40 bodova)" (p4 y599); titles 1. and 2.
# joined by "ili".
# PRICES:
# - I1a-e: "[5 × 1 bod]" (p3 y780): a price per expression, five at 1 mark
#   (the census walks it down, tariff 1 each): PP(). Per letter, as the live
#   2021 and 2024-2026 Q1 cards.
# - I3: "[5 bodova]" on its own line under Q3 (p4 y153; census tariff 5): PP().
#   The scheme prints "[5 bodova]" too (line 149).
# - II1: the part head's "(30 bodova)" (PARTP; census 'II. dio': 30).
# - III1/III2: the part head's "(40 bodova)" (PARTP).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-7; pp8-9 blank):
# - pp3-4 (46-124) reprint the rule and the whole reading text, with its OWN
#   paragraph numbers (it numbers "5. Robert Waldinger ..." the paper's
#   paragraph 4, "6. Studija je pokazala ..." the paper's 5, and skips 4 and
#   9).
# - Q1 (p4, 125-133): the scheme's letters set the paper's expressions in
#   ANOTHER ORDER, each with the scheme's own paragraph number, then the
#   answer: a) potomaka (3); b) površne veze (6); c) suočiti se (3); d)
#   osjećaju blagostanja (6); e) „sudionici su bili podvrgnuti skeniranjima
#   mozga” (3) and "[5 × 1 bod]" at the end of e)'s second line (133).
#   Paired by WORDS with the paper's a) potomaka (3), b) „sudionici ...” (3),
#   c) suočiti (3), d) površne veze (5), e) osjećaju blagostanja (5):
#   paper a = scheme a (126); b = scheme e (132-133); c = scheme c (129);
#   d = scheme b (127-128); e = scheme d (130-131). This reordering is why the
#   exclusions say "the scheme prices no ask that pairs with it": wrong, every
#   expression has its answer.
# - Q3 (p5, 147-156): the question reprinted word for word as the paper prints
#   it, "[5 bodova]" (149), then one paragraph of answer (150-156). The
#   exclusion's "no ask that pairs with it" is wrong (the census seems to have
#   paired "3." with the scheme's reprint of the text's paragraph "3. Studija
#   je uključivala ...", line 64).
# - Part II (p6-7, 215-230): "II. dio (30 bodova)", the task reprinted with
#   "(minimalno 100 riječi) iscrpno argumentirajte" for the paper's "(100 -
#   150 riječi) argumentirajte", then "Na primjer:" (219) and ONE model
#   paragraph after a dash (220-224, running over the p6/p7 break to 229-230;
#   lines 225-227 are the page number and head, left out of the join). No
#   criteria, no percentages, no marks.
# - Part III (p7, 231-235): the head, the instruction and both titles
#   reprinted as the paper prints them, and NOTHING under them.
# SHAPES:
# - I1a-e: one stated answer each -> one(gloss cut after the scheme's
#   expression and paragraph number, PP()) at 1, the scheme's own letter and
#   head quoted in the row note (10f: the scheme's order differs).
# - I3: one paragraph -> one row at 5 (as the live 2023 cards and Bulgarian).
# - II1: the model paragraph under the scheme's own heading "Na primjer:"
#   (10a): one shown row, priced as a whole on the paper's 30 (questionTotal),
#   the heading and the scheme's reprint of the task quoted.
# - III1, III2: nothing printed -> R4 (unprinted) at the paper's 40.
# JUDGEMENT CALLS:
# - Q1 paired by the expressions' own words (as Bulgarian 2025 Q1), never by
#   letter. The scheme's "(6)" for d) and e) against the paper's "(5)" follows
#   the scheme's own renumbered reprint of the text: not an answer, quoted in
#   the row note with the scheme's head.
# - Q1(c): the scheme reprints the paper's "suočiti" as "suočiti se": quoted
#   in the note (10f), the paper's word stays the question.
# - Q1(a) answer prints "od mekoga" (rendered p4: "mekoga", presumably for
#   "nekoga"); Q3's answer prints "upravljnju" (151) and Part II's model
#   "sučimo" (223) and "osbnost" (230): the scheme's own spellings inside rows,
#   kept as printed (lifted, never corrected).
# - Q1 questions are the census's text (instruction + expression; the
#   paragraph number dropped as on the live Q1 cards). The paper sets the word
#   to explain in BOLD inside b) "podvrgnuti", d) "površne" and e)
#   "blagostanja" (rendered p3); the question text cannot carry the bold.
# - Questions: I3 and II1 the census's text (II1's "(30 bodova)" taken off);
#   III1/III2 cut from the paper's lines, instruction first.
# LIVE PAGES: the reading text runs pp2-3 (rendered: title p2 y200 to the
#   source line "(prilagođeno prema: Nenad Jarić Dauenhauer, index.hr, siječanj
#   2023.)" p3 y629; Q1 under it on p3). The live 2023 cards carry [2, 3]:
#   they agree.
# LIVE CARDS (not mine; flagged for the lead, "Live-card answer fixes" ruling):
# - hrv-2023-hl-i-2: its row is the scheme's REPRINT of the reading text's
#   paragraph 2 (lines 57-63, "Jedan je od ključnih zaključaka studije ..."),
#   not the scheme's Q2 answer, which is lines 141-146 ("Harvardska studija o
#   razvoju odraslih započela je 1930‐ih ...", scheme p5). Wrong answer.
# - hrv-2023-hl-i-6: its row is the scheme's reprinted Q6 QUESTION (195-197,
#   "Nakon što ste pročitali cijeli tekst ..."), not an answer; and that
#   question is not the paper's Q6 (the paper asks "U 8. odlomku voditelj
#   harvardskog istraživanja tvrdi kako „nitko nije stalno sretan”. Što dr.
#   Waldinger želi reći ovom tvrdnjom?", p4 y379). The scheme's three answers
#   (199-214) answer its own question. A printed SEC error for 10f.
# - hrv-2023-hl-i-5: its row opens with the scheme's heading "Na primjer:".
# GLYPHS: title 2 prints "zvijezdaǃ" with U+01C3 LATIN LETTER RETROFLEX CLICK
#   where the render shows "!" (paper p4 y745 and scheme p7, both Calibri; the
#   texttrace gives glyph id 1766, a different glyph from Calibri's "!", so it
#   is the character the SEC typed, not a mis-mapped glyph). Left in the
#   question as the text layer gives it; flagged for the lead (no hand map).

PAGES_2023 = (2, 3)


def _scheme_head_2023(n, head):
    """The scheme's own letter and head for this expression (line n, up to
    the answer), quoted: its order and paragraph numbers are not the paper's."""
    return quote(S(n, before=head), lead='The scheme sets the paper\'s expressions in another order and '
                                         'prints this answer under')


ESSAY_2023 = 'Napišite esej (od najmanje 300'


def _essay_2023(d):
    return ('The scheme reprints the part\'s head, the instruction and the two titles, and prints nothing '
            'under them: no criteria and no split of the part\'s marks.')


SPECS[2023] = [
    R('I1a', [one(S(126, after='potomaka (3) '), PP())], pages=PAGES_2023),
    R('I1b', [one(L(132, 133, after='mozga” (3) ', before=' [5 × 1 bod]'), PP())],
      rownote=_scheme_head_2023(132, ' učiniti koga'), pages=PAGES_2023),
    R('I1c', [one(S(129, after='suočiti se (3) '), PP())],
      rownote=_scheme_head_2023(129, ' susresti se'), pages=PAGES_2023),
    R('I1d', [one(L(127, 128, after='veze (6) '), PP())],
      rownote=_scheme_head_2023(127, ' veze koje'), pages=PAGES_2023),
    R('I1e', [one(L(130, 131, after='blagostanja (6) '), PP())],
      rownote=_scheme_head_2023(130, ' osjećaju obilja'), pages=PAGES_2023),
    R('I3', [one(L(150, 156), PP())], pages=PAGES_2023),
    R('II1', [shown(J(L(220, 224), L(229, 230)))], whole=True,
      rownote=both(quote(S(219), lead='The scheme heads it'),
                   quote(L(216, 218), lead='The scheme reprints the task as')),
      pages=PAGES_2023),
    R('III1', [unprinted(_essay_2023)],
      question=QP(4, ESSAY_2023, '1. „Sreću nam')),
    R('III2', [unprinted(_essay_2023)],
      question=QP(4, ESSAY_2023, '2. „Čovječe')),
]


# ================================================================ 2024 HL ===
# Drafted (small-languages lane, 20 Nov): the 3 asks with no live card.
# Live: I1a-e, I2-I6 (10 cards); not touched. Open here: II1, III1, III2.
# Paper (rendered pp2-4): "Ukupna ocjena [100 bodova]" (p2 y65); the rule ends
# the instruction (p2 y124); "I. dio" "(30 bodova)" (p2 y153); reading text p2
# y200 to the source line p3 y612; Q1 p3 y637; Q2-Q6 p4; "II. dio" "(30
# bodova)" (p4 y482); "III. dio" "(40 bodova)" (p4 y614); titles 1. and 2.
# joined by "ili", title 2's attribution on a line of its own (p4 y746).
# PRICES: II1 the part head's "(30 bodova)" (PARTP; census 'II. dio': 30);
# III1/III2 "(40 bodova)" (PARTP). The scheme prints the same heads (134,
# 150). No other price under either part (rendered p4).
# WHAT THE SCHEME PRINTS (rendered scheme p5; pp6-7 blank):
# - Part II (134-149): "II. dio (30 bodova)", the task reprinted as the paper
#   prints it, then the italic heading "Na primjer:" (138) and ONE model
#   paragraph (139-149). No criteria, no percentages, no marks.
# - Part III (150-155): the head, the instruction and both titles reprinted,
#   and NOTHING under them. Title 2 is reprinted in OTHER WORDS: "„Riječi
#   nisu dokaz. Tko osjeća, zna pokazati i djelima.“" (154) for the paper's
#   "„Riječi nisu dokazi. Tko osjeća, zna dokazati i djelima.”".
# SHAPES:
# - II1: the model paragraph under the scheme's own heading (10a): one shown
#   row, priced as a whole on the paper's 30 (questionTotal), the heading
#   quoted.
# - III1, III2: nothing printed -> R4 (unprinted) at the paper's 40.
# JUDGEMENT CALLS:
# - III2: the paper wins on the title, the scheme's reprint quoted in the note
#   (10f: "dokaz"/"pokazati" for the paper's "dokazi"/"dokazati").
# - Title 1: the scheme prints "Odijelo ne čini čovjeka." (no quotation marks,
#   a full stop) for the paper's "„Odijelo ne čini čovjeka”": punctuation
#   only, not quoted. The scheme's "Ili" for the paper's "ili": not quoted.
# - The model paragraph is set as one block after the heading (rendered p5,
#   no paragraph break): one shown row.
# - Questions: II1 the census's text ("(30 bodova)" taken off); III1/III2 cut
#   from the paper's lines, instruction first (the census glues "ili" to
#   title 1); title 2 joined to its attribution line.
# LIVE PAGES: the reading text runs pp2-3 (rendered: title "Brza moda – o čemu
#   ne razmišljamo dok kupujemo" p2 y200 to the source line "(prilagođeno
#   prema: Danijela Goreta, green.hr, lipanj 2023.)" p3 y612; Q1 under it on
#   p3). The live 2024 cards carry [2, 3]: they agree.
# GLYPHS: the scheme PDF's raw text layer (pp3-5) reads Calibri's "ti"
#   ligature as U+019F LATIN CAPITAL LETTER O WITH MIDDLE TILDE (60 times:
#   "eƟkeƟ", "pitaƟ") and its "ft" ligature as U+014C LATIN CAPITAL LETTER O
#   WITH MACRON (6 times: "jeŌine"); the render shows "ti"/"ft". The scheme .md
#   (what the rows and the provenance check read) already holds plain "ti"
#   and "ft" (lines 135, 140, 58: "etiketi", "pitati", "jeftinoj"; no U+019F
#   or U+014C anywhere in it), so no row carries a mangled letter. Reported,
#   not mapped. U+2010 HYPHEN in the scheme's "100 ‐ 150" (137) is a printed
#   hyphen, not cut into a row. No problem on the paper.

ESSAY_2024 = 'Napišite esej (od najmanje 300'


def _essay_2024(d):
    return ('The scheme reprints the part\'s head, the instruction and the two titles, and prints nothing '
            'under them: no criteria and no split of the part\'s marks.')


def _essay2_2024(d):
    return (f'{_essay_2024(d)} It reprints this title as “{L(154, 155, after="2. ").text(d)}”, where the '
            f'paper prints “{PC(4, "2. „Riječi nisu", after="2. ").text(d)}”.')


SPECS[2024] = [
    R('II1', [shown(L(139, 149))], whole=True,
      rownote=quote(S(138), lead='The scheme heads it'), pages=(2, 3)),
    R('III1', [unprinted(_essay_2024)],
      question=QP(4, ESSAY_2024, '1. „Odijelo')),
    R('III2', [unprinted(_essay2_2024)],
      question=QP(4, ESSAY_2024, Run('2. „Riječi nisu', '(Marija Jurić'))),
]


# ================================================================ 2025 HL ===
# Drafted (small-languages lane, 20 Nov): the 3 asks with no live card.
# Live: I1a-e, I2-I6 (10 cards); not touched. Open here: II1, III1, III2.
# Paper (rendered pp2-4): "Ukupna ocjena [100 bodova]" (p2 y65); the rule ends
# the instruction (p2 y124); "I. dio" "(30 bodova)" (p2 y153); reading text p2
# y182 to the source line p3 y603; Q1 p3 y640; Q2-Q6 p4; "II. dio" "(30
# bodova)" (p4 y461); "III. dio" "(40 bodova)" (p4 y607); titles 1. and 2.
# joined by "ili", each with its attribution at the right (p4 y694, y757).
# PRICES: II1 the part head's "(30 bodova)" (PARTP; census 'II. dio': 30);
# III1/III2 "(40 bodova)" (PARTP). The scheme prints the same heads (144,
# 165). No other price under either part (rendered p4).
# WHAT THE SCHEME PRINTS (rendered scheme p6; p3 is the annotations table,
# pp7-8 blank but for page numbers):
# - Part II (144-164): "II. dio (30 bodova)", the task reprinted as the paper
#   prints it, then the italic heading "Na primjer:" (148) and ONE model
#   answer after a dash (149-164). No criteria, no percentages, no marks.
# - Part III (165-171): the head, the instruction and both titles with their
#   attributions reprinted as the paper prints them (the scheme's "Ili" for
#   the paper's "ili"), and NOTHING under them.
# SHAPES:
# - II1: the model answer under the scheme's own heading (10a): one shown
#   row, priced as a whole on the paper's 30 (questionTotal), the heading
#   quoted.
# - III1, III2: nothing printed -> R4 (unprinted) at the paper's 40.
# JUDGEMENT CALLS:
# - The model answer is one dash, one block (rendered p6): one shown row.
#   It prints "priuštiti se što nam treba" (150, presumably "sve"): the
#   scheme's own words inside a shown row, kept as printed.
# - Questions: II1 the census's text ("(30 bodova)" taken off); III1/III2 cut
#   from the paper's lines, instruction first, each title joined to its
#   attribution (the census glues "ili" to title 1).
# LIVE PAGES: the reading text runs pp2-3 (rendered: title "Vjerovanje u Djeda
#   Božićnjaka djecu ne čini boljom, a šteti im" p2 y182 to the source line
#   "(prilagođeno prema: Nenad Jarić Dauenhauer, index.hr, prosinac 2024.)" p3
#   y603; Q1 under it on p3). The live 2025 cards carry [2, 3]: they agree.
# GLYPHS: none (č ć đ š ž read cleanly on paper and scheme).

ESSAY_2025 = 'Napišite esej (od najmanje 300'


def _essay_2025(d):
    return ('The scheme reprints the part\'s head, the instruction and the two titles with their attributions, '
            'and prints nothing under them: no criteria and no split of the part\'s marks.')


SPECS[2025] = [
    R('II1', [shown(L(149, 164))], whole=True,
      rownote=quote(S(148), lead='The scheme heads it'), pages=(2, 3)),
    R('III1', [unprinted(_essay_2025)],
      question=QP(4, ESSAY_2025, Run('1. „Laž je', 'Martin Luther'))),
    R('III2', [unprinted(_essay_2025)],
      question=QP(4, ESSAY_2025, Run('2. ”Nije najveća', 'Ivo Andrić'))),
]


# ================================================================ 2026 HL ===
# Drafted (small-languages lane, 20 Nov): the 3 asks with no live card.
# Live: I1a-e, I2-I6 (10 cards); not touched. Open here: II1, III1, III2.
# Paper (rendered pp2-4): "Ukupna ocjena [100 bodova]" (p2 y65); the rule ends
# the instruction (p2 y124); "I. dio" "(30 bodova)" (p2 y153); reading text p2
# y182 to the source line p3 y734; Q1-Q6 p4; "II. dio" "(30 bodova)" (p4
# y519); "III. dio" "(40 bodova)" (p4 y636); titles 1. and 2. joined by "Ili".
# PRICES: II1 the part head's "(30 bodova)" (PARTP; census 'II. dio': 30);
# III1/III2 "(40 bodova)" (PARTP). The scheme prints the same heads (172,
# 203). No other price under either part (rendered p4).
# WHAT THE SCHEME PRINTS (rendered scheme p7; p3 is the annotations table, p8
# blank but for its page number):
# - Part II (172-202): "II. dio (30 bodova)", the task reprinted in bold as the
#   paper prints it (the scheme's "(100–150 riječi)" for the paper's "(100 -
#   150 riječi)"), then the heading "Na primjer:" (178) and FOUR model answers,
#   each after its own dash and set apart by a blank line (179-186, 187-191,
#   192-197, 198-202). No criteria, no percentages, no marks.
# - Part III (203-208): the head, the instruction and both titles reprinted
#   (title 2 opened with „ where the paper sets ”), and NOTHING under them.
# SHAPES:
# - II1: the four model answers under the scheme's own heading (10a): four
#   shown rows, priced as a whole on the paper's 30 (questionTotal), the
#   heading quoted.
# - III1, III2: nothing printed -> R4 (unprinted) at the paper's 40.
# JUDGEMENT CALLS:
# - One shown row per printed dash (four, rendered p7), as Bulgarian/Romanian
#   model lists.
# - The scheme's "(100–150 riječi)" and title 2's „ for ”: punctuation only,
#   not quoted.
# - Model answers print "situacijma" (142, Q6, not used), "uljepšavatiti"
#   (202) and "raznima" (181): the scheme's own spellings inside shown rows,
#   kept as printed.
# - Questions: II1 the census's text ("(30 bodova)" taken off); III1/III2 cut
#   from the paper's lines, instruction first (title 1 is one line in the
#   text layer, p4 y695; the census glues nothing to it here, but cut
#   uniformly).
# LIVE PAGES: the reading text runs pp2-3 (rendered: title "„Najbolje je kad
#   kažu – napokon razumijem!“" p2 y182 to the source line "(prilagođeno
#   prema: Boris Vlašić, jutarnji.hr, veljača 2022.)" p3 y734; all questions
#   on p4). The live 2026 cards carry [2, 3]: they agree.
# GLYPHS: none (č ć đ š ž read cleanly). Aside: the paper's p4 text layer
#   holds the footer "Croatian" / "Duration: 3 hours" twice (x42 and x57,
#   y789-809); the render shows it once. Nothing a card reads.

ESSAY_2026 = 'Napišite esej (od najmanje 300'


def _essay_2026(d):
    return ('The scheme reprints the part\'s head, the instruction and the two titles, and prints nothing '
            'under them: no criteria and no split of the part\'s marks.')


SPECS[2026] = [
    R('II1', [shown(L(179, 186)), shown(L(187, 191)), shown(L(192, 197)), shown(L(198, 202))], whole=True,
      rownote=quote(S(178), lead='The scheme heads them'), pages=(2, 3)),
    R('III1', [unprinted(_essay_2026)],
      question=QP(4, ESSAY_2026, '1. Je li svijetu')),
    R('III2', [unprinted(_essay_2026)],
      question=QP(4, ESSAY_2026, '2. ”Život nam')),
]


def specs(year):
    return SPECS.get(year, [])
