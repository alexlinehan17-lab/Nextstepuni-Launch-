#!/usr/bin/env python3
"""Reviewed specs for the Bulgarian classic examination (small-languages lane).

One entry per printed ask with no live card; see sl_lib.py for the selector
language. Line numbers are lines of examiner-reports/bulgarian/schemes/<year>-hl.md.
Drafted by an Opus helper on the Romanian, Dutch and Maltese models, integrated
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
# Drafted (small-languages lane, 20 Nov): the four open asks of this sitting,
# I6, II1, III1, III2. Live: I1а-д, I2-I5 (9 cards); not touched.
# Paper (rendered pp2-4): "Въпроси (100 точки)" (p3 y494); "Първа част (30
# /100)" (p3 y525); Q1 "1 точка" beside each expression, Q2-Q6 "5 точки" each;
# "Втора част (30 /100)" (p4 y259) with "30 точки" on a line of its own under
# the task (p4 y408); "Трета част (40 /100)" (p4 y437), two titles joined by
# "или", "40 точки" under them (p4 y565).
# PRICES:
# - I6: the census reads no price (tariff None), but the paper PRINTS one: "5
#   точки" at the end of the question's own last line (p4 y216, "Съгласни ли
#   сте с автора? Аргументирайте мнението си. 5 точки"; rendered p4, right
#   margin, bold). Priced from that printed line (PaperP); the scheme prints
#   the same "5 точки" (line 72). Not a remainder, not 10i.
# - II1: the part head's "(30 /100)" (PARTP), the same 30 the paper prints
#   under the task ("30 точки", p4 y408) and the scheme on line 86.
# - III1/III2: the part head's "(40 /100)" (PARTP); "40 точки" p4 y565, scheme
#   line 108.
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4):
# - Q6 (lines 70-72 reprint the question with "5 точки"): one underlined dash,
#   lines 73-77, "Лична интерпретация – няколко разсъждения (или примерa) за
#   новите форми ... Отговорът може да засегне един или повече от
#   множеството възможни теми по въпроса." A requirement with example topics,
#   no split: shown, priced as a whole on the paper's 5 (questionTotal; Dutch
#   2011 Q5: a requirement-only answer is shown and self-assessed).
# - Part II (lines 78-86 reprint the task as the paper prints it): an
#   underlined descriptive line (91, "Лична интерпретация, ясни и
#   непротиворечиви идеи.") and one paragraph of indicative content (92-102,
#   "Кандидатът би могъл да развие темата, опирайки се на очевидното: ...").
# - Part III (103-108 reprint the instruction and both titles, "40 точки"):
#   one underlined descriptive line only (109-111, "- Умение за създаване на
#   цялостен, логически последователен (кохерентен и кохезивен) текст, ...").
# - Criteria (p4, "Бележки:", 112-124): "При оценяването на отговорите от
#   първите две части се прилагат следните критерии:" -- for the FIRST TWO
#   parts (Parts I and II), not Part III. Criteria 1-3 print "30%" each;
#   criterion 4 ("Конвенционални умения – ... книжовен език.", 123-124)
#   prints NO percentage (rendered p4: the line ends "книжовен език."). The
#   printed percentages add to 90 %, so graded() cannot apply (10b: never
#   round a tariff into existence; the missing 10 % is not printed).
# SHAPES:
# - I6: shown, whole=True, total = the paper's printed 5 (PaperP).
# - II1: the scheme prints indicative content (10a: answer content, never
#   the R4 line): the paragraph shown, priced as a whole on the paper's 30
#   (questionTotal); its descriptive line quoted as the head, and the four
#   criteria quoted with their printed percentages (10b, "otherwise show the
#   percentages and score on the printed total").
# - III1/III2: only a descriptive line, and the criteria are stated for the
#   first two parts only: R4 (unprinted) at the paper's 40, the note quoting
#   the descriptive line and the criteria's lead.
# JUDGEMENT CALLS:
# - Q6 shown (requirement), not one(): the dash prescribes "Лична
#   интерпретация" and names example topics ("Отговорът може да засегне един
#   или повече ..."), so it is not a stated answer to claim whole.
# - Part II's paragraph is one shown row (one printed paragraph, rendered p4).
# - II1's question is cut from the paper's own lines (the census runs on
#   into the "30 точки" printed under the task).
# - Part III's title 2: the scheme reprints it without the paper's full stop
#   ("Никой човек не е остров"): punctuation only, not quoted.
# - Reading text: pp2-3 (rendered: title "Младите владеят културните кодове
#   по-добре от старите" p2 y220, the text to its byline p3 y444; questions
#   from p3 y493). The live cards of this sitting carry no sourceMaterial
#   pages; set here from the render.
# GLYPHS: scheme line 73 prints "примерa" with a LATIN a (U+0061) as its last
# letter (rendered identically; the SEC's own typing, not a font map). Lifted
# as printed; flagged for the lead.

def _crit_note_2010(d):
    return (f'Under “{S(112).text(d)}” the scheme prints “{L(113, 114).text(d)}” '
            + ' '.join(f'“{L(a, b).text(d)}”' for a, b in ((115, 116), (117, 120), (121, 122), (123, 124)))
            + ' The fourth criterion prints no percentage, so the criteria are shown and the part is '
              'scored on its printed total.')


def _part3_note_2010(d):
    return (f'Under the two titles the scheme prints only “{L(109, 111, after="- ").text(d)}” Under '
            f'“{S(112).text(d)}” it prints its criteria for the first two parts only: “{L(113, 114).text(d)}”')


SPECS[2010] = [
    R('I6', [shown(L(73, 77, after='- '))], whole=True, total=PaperP(4, 'Съгласни ли сте с автора?'),
      pages=(2, 3)),
    R('II1', [shown(L(92, 102))], whole=True,
      rownote=both(quote(S(91), lead='The scheme heads it'), _crit_note_2010),
      question=QP(4, Run('„И за първи път', '(около 100 думи)')), pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2010)],
      question=QP(4, 'Напишете съчинение', '1. Отива си')),
    R('III2', [unprinted(_part3_note_2010)],
      question=QP(4, 'Напишете съчинение', '2. Никой')),
]


# ================================================================ 2011 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I1а-д, II1, III1, III2. Live: I2-I6 (5 cards); not touched.
# Paper (rendered pp2-4; this paper sets several bold and underlined runs with
# real space glyphs inside words, "Пъ рва час т", "В сич ки отговори", see
# GLYPHS): "Въпроси (100 точки)" (p3 y596); "Първа част (30 /100)" (p3 y629);
# Q1 prints its five expressions а)-д), each with "1 точка" at the right
# margin ON THE SAME LINE (p3 y678-731, rendered: bold, right-aligned); Q2-Q6
# "5 точки" each (p4); "Втора част (30/100)" (p4 y312) with "30 точки" beside
# "(около 100 думи)" (p4 y435); "Трета част (40/100)" (p4 y491), two titles
# joined by "или", "40 точки" under them (p4 y631).
# PRICES:
# - I1а-д: the census reads no price (tariff None) because each "1 точка" is
#   set on the expression's own text line; the paper PRINTS it for each
#   expression, so each is priced from its own printed line (PaperP). The
#   scheme prints the same "1 точка" beside each expression (lines 19, 21, 24,
#   28, 30). Not a remainder, not 10i.
# - II1: the part head's "(30/100)"; III1/III2: "(40/100)". PARTP cannot read
#   them: the census reads no part totals for this sitting (the letterspaced
#   heads "Вто ра час т", "Тре та час т" with the cell set apart at x494,
#   p4 y313/y492), so each is read from its printed head cell (PaperP, as
#   Romanian 2023 Part II).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5):
# - Q1 (rendered p3): each expression in bold with "1 точка", its gloss on
#   the line(s) below in plain type, no dash. Paired by WORDS, and the
#   scheme's letters agree with the paper's: а) реторика (20), б) лозунг
#   (22-23), в) традиция (25-27), г) размирици (29), д) догма (31-32). One
#   stated answer each: one row at the paper's "1 точка".
# - Part II (72-80 reprint the task as the paper prints it, "30 точки"): the
#   descriptive line "Лична интерпретация, ясни и непротиворечиви идеи." (81)
#   and one paragraph of indicative content (82-95, "Кандидатът би могъл да
#   развие темата, опирайки се на авторовата теза ...").
# - Part III (100-106 reprint the instruction and both titles, "40 точки"):
#   one descriptive line only (107-109, "Умение за създаване на цялостен,
#   логически последователен ... речеви умения.").
# - Criteria (p5, "Бележки:", 110-122): "При оценяването на отговорите от
#   първите две части се прилагат следните критерии:" -- the FIRST TWO parts
#   (I and II), not Part III. Criteria 1-3 "30%" each; criterion 4
#   ("Конвенционални умения – ...", 121-122) prints NO percentage (rendered
#   p5: ends "книжовен език."). 90 % printed: graded() cannot apply (10b).
# SHAPES:
# - I1а-д: one(gloss, PaperP) each.
# - II1: the paragraph shown, priced as a whole on the paper's 30 (10a,
#   questionTotal), descriptive line quoted as its head, the four criteria
#   quoted with their printed percentages (10b: shown, scored on the total).
# - III1/III2: only a descriptive line, criteria stated for the first two
#   parts only: R4 (unprinted) at the paper's 40, quoting both.
# JUDGEMENT CALLS:
# - Reading text: pp2-3 (rendered: title "Без интереса към чуждото културата
#   е невъзможна" p2, the text to its byline "Илия Траянов, ..." p3 y546;
#   questions from p3 y596). The live cards of this sitting (I2-I6) carry
#   sourceMaterial.pages [3], which the render does not agree with (p2 holds
#   the title and the first three paragraphs): set to (2, 3) here; the live
#   cards are flagged for the lead, not changed.
# - II1's question is cut from the paper's own lines (the census glues the
#   part head's "(30/100)" in front and "30 точки" after it).
# - Part III's instruction line prints "на една" as a bold underlined run
#   with real space glyphs inside it ("н а ед н а", content stream checked with
#   TEXT_INHIBIT_SPACES; visible gaps on the render). Lifted as printed, as
#   the lane already quotes this paper's rule sentence ("В сич ки отговори");
#   if the lead prefers, drop the instruction and card the title alone
#   (QP(4, '1. Другият')).
# GLYPHS: no mis-mapped glyphs in the lines used; the spaced runs above are
# printed spaces, not a font map. Scheme line 23 (I1б's gloss) prints
# "промeни" with a LATIN e (U+0065), rendered identically: the SEC's own
# typing, lifted as printed; flagged for the lead.

def _crit_note_2011(d):
    return (f'Under “{S(110).text(d)}” the scheme prints “{L(111, 112).text(d)}” '
            + ' '.join(f'“{L(a, b).text(d)}”' for a, b in ((113, 114), (115, 118), (119, 120), (121, 122)))
            + ' The fourth criterion prints no percentage, so the criteria are shown and the part is '
              'scored on its printed total.')


def _part3_note_2011(d):
    return (f'Under the two titles the scheme prints only “{L(107, 109).text(d)}” Under '
            f'“{S(110).text(d)}” it prints its criteria for the first two parts only: “{L(111, 112).text(d)}”')


ESSAY_2011 = 'Напишете съчинение'
P2_2011 = PaperP(4, '(30/100)')
P3_2011 = PaperP(4, '(40/100)')
SPECS[2011] = [
    R('I1а', [one(S(20), PaperP(3, 'а) реторика'))], total=PaperP(3, 'а) реторика'), pages=(2, 3)),
    R('I1б', [one(L(22, 23), PaperP(3, 'б) лозунг'))], total=PaperP(3, 'б) лозунг'), pages=(2, 3)),
    R('I1в', [one(L(25, 27), PaperP(3, 'в) традиция'))], total=PaperP(3, 'в) традиция'), pages=(2, 3)),
    R('I1г', [one(S(29), PaperP(3, 'г) размирици'))], total=PaperP(3, 'г) размирици'), pages=(2, 3)),
    R('I1д', [one(L(31, 32), PaperP(3, 'д) догма'))], total=PaperP(3, 'д) догма'), pages=(2, 3)),
    R('II1', [shown(L(82, 95))], whole=True, total=P2_2011,
      rownote=both(quote(S(81), lead='The scheme heads it'), _crit_note_2011),
      question=QP(4, Run('„Това е напълно', '(около 100 думи)')), pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2011)], total=P3_2011,
      question=QP(4, ESSAY_2011, '1. Другият')),
    R('III2', [unprinted(_part3_note_2011)], total=P3_2011,
      question=QP(4, ESSAY_2011, Run('2. „Повечето', 'Абрахам Линколн'))),
]


# ================================================================ 2012 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1а-д, I2-I6 (10 cards); not touched.
# Paper (rendered pp2-4): "Въпроси (100 точки)" (p3 y580); "Втора част
# (30/100)" on one line (p4 y366), "30 точки" under the task (p4 y520);
# "Трета част (40/100)" (p4 y567), two titles joined by "или", "40 точки"
# under them (p4 y703).
# PRICES: II1 the part head's "(30/100)", III1/III2 "(40/100)" (PARTP: each
# total printed on its head's own line); the scheme prints the same "30
# точки" (line 105) and "40 точки" (122).
# WHAT THE SCHEME PRINTS (rendered scheme p5):
# - Part II (97-105 reprint the task as the paper prints it): the underlined
#   descriptive line "Лична интерпретация, ясни и непротиворечиви идеи." (106)
#   and one paragraph of indicative content (107-116, "Кандидатът би могъл да
#   развие темата, опирайки се на авторовата теза ...").
# - Part III (117-122 reprint the instruction and both titles): one
#   underlined descriptive line only (123-125, "- Умение за създаване на
#   цялостен, логически последователен ... речеви умения.").
# - Criteria ("Бележки:", 126-136, rendered in italics): "При оценяването на
#   отговорите от първите две части се прилагат следните критерии:" -- the
#   FIRST TWO parts (I and II), not Part III. Criteria 1-3 "30%" each;
#   criterion 4 ("Конвенционални умения – ...", 135-136) prints NO
#   percentage (rendered: ends "книжовен език."). 90 % printed: graded()
#   cannot apply (10b).
# SHAPES:
# - II1: the paragraph shown, priced as a whole on the paper's 30 (10a,
#   questionTotal); descriptive line quoted as its head; the four criteria
#   quoted with their printed percentages (10b: shown, scored on the total).
# - III1/III2: only a descriptive line, criteria for the first two parts
#   only: R4 (unprinted) at the paper's 40, quoting both.
# JUDGEMENT CALLS:
# - II1's question is cut from the paper's own lines (the census runs on
#   into "30 точки").
# - Part III title 1: the scheme reprints it with a word the paper does not
#   print, "Дали има ли много светове около нас?" (paper "Дали има много
#   светове около нас?"): the paper wins on the question, the scheme's words
#   quoted on that card (10f).
# - Reading text: pp2-3 (rendered: title "България, която е отвън" p2 y192,
#   the text to its source lines p3 y502-518; questions from p3 y580). The
#   live cards carry no sourceMaterial pages.
# GLYPHS: none in the lines used.

def _crit_note_2012(d):
    return (f'Under “{S(126).text(d)}” the scheme prints “{S(127).text(d)}” '
            + ' '.join(f'“{L(a, b).text(d)}”' for a, b in ((128, 129), (130, 132), (133, 134), (135, 136)))
            + ' The fourth criterion prints no percentage, so the criteria are shown and the part is '
              'scored on its printed total.')


def _part3_note_2012(d):
    return (f'Under the two titles the scheme prints only “{L(123, 125, after="- ").text(d)}” Under '
            f'“{S(126).text(d)}” it prints its criteria for the first two parts only: “{S(127).text(d)}”')


ESSAY_2012 = 'Напишете съчинение'
SPECS[2012] = [
    R('II1', [shown(L(107, 116))], whole=True,
      rownote=both(quote(S(106), lead='The scheme heads it'), _crit_note_2012),
      question=QP(4, Run('„В съвременния свят', '(около 100 думи)')), pages=(2, 3)),
    R('III1', [unprinted(both(_part3_note_2012,
                              quote(S(119, after='1. '), lead='The scheme reprints this title as')))],
      question=QP(4, ESSAY_2012, '1. Дали има')),
    R('III2', [unprinted(_part3_note_2012)],
      question=QP(4, ESSAY_2012, '2. В съвременното')),
]


# ================================================================ 2013 HL ===
# Drafted (small-languages lane, 20 Nov): the four open asks of this sitting,
# I6, II1, III1, III2. Live: I1а-д, I2-I5 (9 cards); not touched.
# Paper (rendered pp2-4): "Въпроси (100 точки)" (p3 y619); "Първа част (30
# /100)" (p3 y652); Q1 "1 точка" beside each expression, Q2-Q6 "5 точки"
# each; "Втора част (30/100)" on one line (p4 y372), "30 точки" under the
# task (p4 y500); "Трета част (40/100)" (p4 y583), two titles joined by "или",
# "40 точки" under them (p4 y736).
# PRICES:
# - I6: the census reads no price (tariff None), but the paper PRINTS "5
#   точки" at the end of the question's last line (p4 y282, "(на
#   носталгиците или на прагматиците) вие причислявате автора? 5 точки";
#   rendered p4, right margin). Priced from that printed line (PaperP); the
#   scheme prints the same "5 точки" (line 118). Not a remainder, not 10i.
# - II1: the part head's "(30/100)" (PARTP); III1/III2: "(40/100)" (PARTP).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5; answers in italics):
# - Q6 (114-118 reprint the question with "5 точки"): one italic paragraph
#   opening with a dash, 119-133 ("– Трудно бихме причислили автора към една
#   от тези групи. ... за „бъдещето, което ни очаква”."). A model answer, no
#   split: one row at the paper's 5 (one printed paragraph = one row at the
#   printed price; Romanian 2012 Q5, 2020 Q6).
# - Part II (134-140 reprint the task with "30 точки"): the underlined
#   italic descriptive line "Лична интерпретация, ясни и непротиворечиви
#   идеи." (145, p5) and one paragraph of indicative content (146-152,
#   "Кандидатът би могъл да развие темата, опирайки се на авторовата теза
#   ...").
# - Part III (153-159 reprint the instruction and both titles, "40 точки"):
#   one underlined descriptive line only (160-161, "Умение за създаване на
#   цялостен, логически последователен ... речеви умения.").
# - Criteria ("Бележки:", 162-172, italics): "При оценяването на отговорите
#   от първите две части се прилагат следните критерии:" -- the FIRST TWO
#   parts (I and II), not Part III. Criteria 1-3 "30%" each; criterion 4
#   (171-172) prints NO percentage (rendered p5: ends "книжовен език.").
#   90 % printed: graded() cannot apply (10b).
# SHAPES:
# - I6: one row at the paper's printed 5 (PaperP).
# - II1: the paragraph shown, priced as a whole on the paper's 30 (10a,
#   questionTotal); descriptive line quoted as its head; the four criteria
#   quoted with their printed percentages (10b: shown, scored on the total).
# - III1/III2: only a descriptive line, criteria for the first two parts
#   only: R4 (unprinted) at the paper's 40, quoting both.
# JUDGEMENT CALLS:
# - I6 is one claimable row (a model answer about the author, one printed
#   paragraph), not shown: the live Part I cards of this sitting price their
#   one-paragraph answers the same way. If the lead prefers self-assessment
#   for an opinion-shaped ask, flip to shown, whole=True.
# - II1's question is cut from the paper's own lines (the census runs on
#   into "30 точки").
# - Part II: the scheme reprints the task with its own punctuation
#   ("носталгиците”, си казвате.”"): punctuation only, not quoted.
# - Part III title 2: the scheme reprints it as "Да преследваш мечтите си е
#   сладко и горчиво пътуване" (paper "... мечтите си – сладко и горчиво
#   пътуване"): the paper wins on the question, the scheme's words quoted on
#   that card (10f). Title 1: spacing only ("„ В"), not quoted.
# - Reading text: pp2-3 (rendered: title "За книгата и книжното" p2 y176, the
#   text to its source line p3 y458; questions from p3 y619). The live cards
#   carry no sourceMaterial pages.
# GLYPHS: none in the lines used.

def _crit_note_2013(d):
    return (f'Under “{S(162).text(d)}” the scheme prints “{S(163).text(d)}” '
            + ' '.join(f'“{L(a, b).text(d)}”' for a, b in ((164, 165), (166, 168), (169, 170), (171, 172)))
            + ' The fourth criterion prints no percentage, so the criteria are shown and the part is '
              'scored on its printed total.')


def _part3_note_2013(d):
    return (f'Under the two titles the scheme prints only “{L(160, 161).text(d)}” Under '
            f'“{S(162).text(d)}” it prints its criteria for the first two parts only: “{S(163).text(d)}”')


ESSAY_2013 = 'Напишете съчинение'
Q6P_2013 = PaperP(4, '(на носталгиците')
SPECS[2013] = [
    R('I6', [one(L(119, 133, after='– '), Q6P_2013)], total=Q6P_2013, pages=(2, 3)),
    R('II1', [shown(L(146, 152))], whole=True,
      rownote=both(quote(S(145), lead='The scheme heads it'), _crit_note_2013),
      question=QP(4, Run('„Сега обаче', '(около 100 думи)')), pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2013)],
      question=QP(4, ESSAY_2013, Run('1. „ В историята', 'нещо просто'))),
    R('III2', [unprinted(both(_part3_note_2013,
                              quote(S(158, after='2. '), lead='The scheme reprints this title as')))],
      question=QP(4, ESSAY_2013, '2. Да преследваш')),
]


# ================================================================ 2014 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1а-д, I2-I6 (10 cards); not touched.
# Paper (rendered pp2-4): the reading text on pp2-3, with an author's note
# under it on p3; "Въпроси (100 точки)" (p4 y90); "Втора част (30/100)" on
# one line (p4 y449), "30 точки" beside "(около 100 думи)" (p4 y534);
# "Трета част (40/100)" (p4 y561), two titles joined by "или", "40 точки"
# under them (p4 y711).
# PRICES: II1 the part head's "(30/100)", III1/III2 "(40/100)" (PARTP, each
# total on its head's own line); the scheme prints the same "30 точки" (123)
# and "40 точки" (161).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5; content in italics):
# - Part II (119-123 reprint the task, "30 точки"): the underlined
#   descriptive line "Лична интерпретация, ясни и непротиворечиви идеи."
#   (124), its own heading "Много възможности:" (125), then three paragraphs
#   of indicative content: 126-137 ("Кандидатът би могъл да се позове на
#   авторовата (малко неопределена) теза ..."), 138-142 ("Ще бъде предимство,
#   ако кандидатът ..."; opens on a new line after the short "... играта на
#   съдбата..."), and on p5 147-153 ("Кандидатът би могъл да се позове на
#   богата фразеология ...").
# - Part III (154-161 reprint the instruction and both titles as the paper
#   prints them): one underlined descriptive line only (162-163, "Умение за
#   създаване на цялостен, логически последователен ... речеви умения.").
# - Criteria ("Бележки:", 164-174, italics): "При оценяването на отговорите
#   от първите две части се прилагат следните критерии:" -- the FIRST TWO
#   parts (I and II), not Part III. Criteria 1-3 "30%" each; criterion 4
#   (173-174) prints NO percentage (rendered p5: ends "книжовен език.").
#   90 % printed: graded() cannot apply (10b).
# SHAPES:
# - II1: the three paragraphs shown, priced as a whole on the paper's 30
#   (10a, questionTotal), under the scheme's own heading "Много възможности:"
#   and its descriptive line (quoted); the four criteria quoted with their
#   printed percentages (10b: shown, scored on the total).
# - III1/III2: only a descriptive line, criteria for the first two parts
#   only: R4 (unprinted) at the paper's 40, quoting both.
# JUDGEMENT CALLS:
# - Part II, p5: "Една забавна и виртуозна възможност ..." (150) opens a line
#   after "... на нещо”..." with no indent and no gap (rendered p5); read as
#   the same paragraph as 147-149 (shown rows only; marks untouched).
# - II1's question is cut from the paper's own lines (the census runs on
#   into "30 точки").
# - Part II: the scheme's reprint of the task drops the closing quotation
#   mark ("... възможности?" for the paper's "... възможности?”"):
#   punctuation only, not quoted.
# - Reading text: pp2-3 (rendered: title "За неравенството" p2 y185, the text
#   to its source line p3 y565, an author's note under it; questions from p4
#   y90). The live cards carry no sourceMaterial pages.
# GLYPHS: the paper (and the scheme's reprint, line 120) prints the task's
# first word "Kак" with a LATIN K (U+004B; also in the passage, p3 y396),
# rendered identically: the SEC's own typing, lifted as printed into II1's
# question (the run's opening anchor carries the same Latin K). Flagged.

def _crit_note_2014(d):
    return (f'Under “{S(164).text(d)}” the scheme prints “{S(165).text(d)}” '
            + ' '.join(f'“{L(a, b).text(d)}”' for a, b in ((166, 167), (168, 170), (171, 172), (173, 174)))
            + ' The fourth criterion prints no percentage, so the criteria are shown and the part is '
              'scored on its printed total.')


def _part3_note_2014(d):
    return (f'Under the two titles the scheme prints only “{L(162, 163).text(d)}” Under '
            f'“{S(164).text(d)}” it prints its criteria for the first two parts only: “{S(165).text(d)}”')


ESSAY_2014 = 'Напишете съчинение'
SPECS[2014] = [
    R('II1', [shown(L(126, 137)), shown(L(138, 142)), shown(L(147, 153))], whole=True,
      rownote=both(quote(S(124), S(125), lead='The scheme heads it'), _crit_note_2014),
      question=QP(4, Run('„Kак да си помогнем', '(около 100 думи)')), pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2014)],
      question=QP(4, ESSAY_2014, Run('1. „ Най-голямата', 'надмогнеш неуспеха'))),
    R('III2', [unprinted(_part3_note_2014)],
      question=QP(4, ESSAY_2014, Run('2. „Дори', 'не ще я открием'))),
]


# ================================================================ 2015 HL ===
# Drafted (small-languages lane, 20 Nov): all thirteen asks of this sitting,
# I1а-д, I2-I6, II1, III1, III2 (all excluded before; no live 2015 cards).
# The scheme .md was repaired from glyph ids (it read "ɨɬɝɨɜɨɪɢ" for
# "отговори"); every line cut below was checked against the rendered scheme
# (pp3-5 at 190 dpi) and reads as printed.
# Paper (rendered pp2-4): the reading text "За приятелството" pp2-3;
# "Въпроси (100 точки)" (p4 y56); "Първа част (30 /100)" (p4 y89); Q1 prints
# "1 точка" as a cell beside each expression а)-д) (p4 y131-182); Q2-Q5 "5
# точки" each as a cell; Q6 "5 точки" at the END of its own last line (p4
# y436, "е този, който „хвърля мост през пропастта на това несъответствие”? 5
# точки"); "Втора част (30/100)" (p4 y466/467); "Трета част (40/100)" (p4
# y639/641), "Напишете съчинение (минимум 300 думи) на една от следните
# теми:", two titles joined by "или". No "30 точки"/"40 точки" under the tasks
# on the paper (the scheme prints them, lines 144, 165).
# CENSUS FLAGS, settled on the render:
# - "unpriced-ask" Q1(а)-(д) and "orphan-scheme-ask Section I Q1": the census's
#   scheme reader (eu_scheme) reads the scheme PDF, whose text layer is still
#   the glyph-broken one, so it finds Q1-Q6 by number and none of the Cyrillic
#   letters а)-д) (EuScheme(2015).reading() = I1..I6, no letters, no prices).
#   READ: the scheme prints Q1's stem (52) and under it, in bold, each
#   expression with "1 точка" at the right (а) привързаност 53, б) сигурност 55,
#   в) мистерия 57, г) отчуждение 59, д) морално право 63) and its gloss in
#   italics after a dash on the line(s) below. Paired by WORDS; the letters
#   agree with the paper's. The paper prints "1 точка" beside each (census
#   tariff (1, 1, 1): PP()).
# - "part-total: ... add to 25": the census reads no tariff for Q6 (its "5
#   точки" is on the question's own text line, not a cell). 5 x 1 + 5 x 5 =
#   30 with Q6's printed 5: the part closes. Q6 priced from that line
#   (PaperP); the scheme prints the same "5 точки" (118). Not a remainder, not
#   10i.
# PRICES: I1а-д PP() = 1 each; I2-I5 PP() = 5 each; I6 PaperP = 5; II1 the
# part head's "(30/100)" (PARTP); III1/III2 "(40/100)" (PARTP). The census
# reads all three part heads.
# WHAT THE SCHEME PRINTS (rendered pp3-5; questions bold, answers italic):
# - Q1: one gloss each after a dash: а) 54; б) 56; в) 58; г) 60-62; д) 64-69.
# - Q2 (70-72 reprint, "5 точки"): one paragraph after a dash, 73-80.
# - Q3 (81 reprint): one paragraph after a dash, 82-85.
# - Q4 (86-87 reprint): one paragraph after a hyphen, 88-92 and, over the
#   p3/p4 break, 97-101 (93-96 are the page number and head, left out).
# - Q5 (102-103 reprint): one paragraph after a hyphen, 104-115.
# - Q6 (116-118 reprint): one paragraph after a hyphen, 119-134.
# - Part II (135-144 reprint the head and the task, "(около 100 думи) 30
#   точки"): on p5 the underlined descriptive line "Лична интерпретация, ясни и
#   непротиворечиви идеи." (149), its own heading "Различни възможности за
#   отговор:" (150) and one paragraph of content (151-159).
# - Part III (160-165 reprint the head, the instruction, both titles, "40
#   точки"): one underlined descriptive line only (166-167, "Умение за
#   създаване на цялостен, ... речеви умения.").
# - Criteria ("Бележки:", 168-178, italics, p5): "При оценяването на
#   отговорите от първите две части се прилагат следните критерии:" -- the
#   FIRST TWO parts (I and II), not Part III. 1. 30 % (170-171), 2. 30 %
#   (172-174), 3. 30 % (175-176), 4. 10 % (177-178): all four printed
#   (rendered p5), 100 %.
# SHAPES:
# - I1а-д: one(gloss, PP()) each, the row cut after the dash.
# - I2-I6: one printed paragraph each = one row at the paper's 5 (as the
#   finished 2013 I6, 2021-2026 Part I), the row cut to the answer.
# - II1: graded on the four criteria (10b), 9 / 9 / 9 / 3 of the paper's 30;
#   head the part's descriptive line (149); the criteria's lead quoted and
#   the paragraph quoted under its own heading as examples (10a), as 2016.
# - III1/III2: only a descriptive line, criteria for the first two parts
#   only: R4 (unprinted) at the paper's 40, quoting both (as 2014, 2016).
# JUDGEMENT CALLS:
# - Q6's answer is one paragraph: line 125 "Това твърдение ..." continues
#   the paragraph (rendered p4, no gap, no indent).
# - The scheme's reprints of Q2-Q6 and of Part II's task match the paper's
#   words; Q2's reprint opens the inner quotation with “ for the paper's „:
#   punctuation only, not quoted.
# - Part III title 2: the scheme reprints it without the paper's "..."
#   ("с най-малко” (Сократ)" for "с най-малко...“ (Сократ)") and without the
#   space after „: punctuation only, not quoted.
# - Questions: I1-I6 and II1 are the census's text (II1's "(30/100)" taken
#   off); III1/III2 cut from the paper's lines, instruction first (the census
#   glues "или" to title 1).
# - Reading text pp2-3 (rendered: the rule and title "За приятелството" p2
#   y88-144, the text to the byline and author note on p3 y591-682; p4 opens
#   "Въпроси"). No live 2015 cards to compare.
# GLYPHS (repaired .md against the render): every word cut matches the
# rendered page. Three letters are LATIN in the .md: line 64 "e" (U+0065) in
# "моралното право e отнесено" (I1д's row) and line 121 "caмo" (Latin c, a,
# o around a Cyrillic м; I6's row). They were Latin in the ORIGINAL text layer
# too (rawdict: spans ' e ' and ' ca' 'ɦ' 'o ', where every Cyrillic letter
# came out as IPA), so they are Latin glyphs the SEC typed, rendered
# identically to е / само; not a repair fault. Lifted as printed, flagged.
# Also printed as such (rendered p4): line 126 "затов" (for "затова"), kept.

CRIT_2015 = crit((170, 171), (172, 174), (175, 176), (177, 178))
ESSAY_2015 = 'Напишете съчинение'
Q6P_2015 = PaperP(4, 'е този, който „хвърля')


def _part3_note_2015(d):
    return (f'Under the two titles the scheme prints only “{L(166, 167).text(d)}” Under '
            f'“{S(168).text(d)}” it prints its criteria for the first two parts only: “{S(169).text(d)}”')


SPECS[2015] = [
    R('I1а', [one(S(54), PP())], pages=(2, 3)),
    R('I1б', [one(S(56), PP())], pages=(2, 3)),
    R('I1в', [one(S(58), PP())], pages=(2, 3)),
    R('I1г', [one(L(60, 62), PP())], pages=(2, 3)),
    R('I1д', [one(L(64, 69), PP())], pages=(2, 3)),
    R('I2', [one(L(73, 80), PP())], pages=(2, 3)),
    R('I3', [one(L(82, 85), PP())], pages=(2, 3)),
    R('I4', [one(J(L(88, 92), L(97, 101)), PP())], pages=(2, 3)),
    R('I5', [one(L(104, 115), PP())], pages=(2, 3)),
    R('I6', [one(L(119, 134), Q6P_2015)], total=Q6P_2015, pages=(2, 3)),
    R('II1', [graded(S(149), PARTP(), CRIT_2015)],
      rownote=both(quote(S(169), lead='The scheme prints'), examples(S(150), L(151, 159))),
      pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2015)],
      question=QP(4, ESSAY_2015, '1. „ Който')),
    R('III2', [unprinted(_part3_note_2015)],
      question=QP(4, ESSAY_2015, '2. „ Най-богат')),
]


# ================================================================ 2016 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1а-д, I2-I6 (10 cards); not touched.
# Paper (rendered pp2-4): "Въпроси (100 точки)" (p3 y594); "Втора част" with
# "(30/100)" in the right-hand cell (p4 y281/283); "Трета част" with
# "(40/100)" (p4 y525/526), two titles joined by "или". Neither part prints
# "30 точки"/"40 точки" under its task this sitting: the head cells only.
# PRICES: II1 "(30/100)", III1/III2 "(40/100)" (PARTP; the census reads the
# three part heads, {'Първа част': (30, 100), 'Втора част': (30, 100),
# 'Трета част': (40, 100)}).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5; content in italics):
# - Part II (112-124 reprint the task, no price): the descriptive line
#   "Лична интерпретация, ясни и непротиворечиви идеи." (125), its own
#   heading "Различни възможности за отговор:" (126) and one paragraph of
#   indicative content (127-134, "Кандидатът би могъл да даде примери ...").
# - Part III (135-145 reprint the instruction and both titles, over the p4/p5
#   break): one descriptive line only (146-147, "Умение за създаване на
#   цялостен, логически последователен ... речеви умения.").
# - Criteria ("Бележки:", 148-158, italics, p5): "При оценяването на
#   отговорите от първите две части се прилагат следните критерии:" -- the
#   FIRST TWO parts (I and II), not Part III. 1. 30 % (150-151), 2. 30 %
#   (152-154), 3. 30 % (155-156), 4. 10 % (157-158): all four printed this
#   sitting, adding to 100 %.
# SHAPES:
# - II1: graded on the four criteria (10b): 30 % / 30 % / 30 % / 10 % of
#   the paper's 30 = 9 / 9 / 9 / 3, whole numbers. Head: the part's own
#   descriptive line (125, as Romanian 2010-2014 head their parts). The
#   criteria's lead is quoted (it names the parts they serve), and the
#   paragraph quoted under its own heading as examples, not a checklist
#   (10a).
# - III1/III2: only a descriptive line, and the criteria are printed for the
#   first two parts only: R4 (unprinted) at the paper's 40, the note quoting
#   the descriptive line and the criteria's lead.
# JUDGEMENT CALLS:
# - Part III is NOT graded although the same four criteria are printed
#   directly under it: the scheme's own lead limits them to "първите две
#   части" (brief, coordinator: read which parts the criteria serve).
# - The paper sets "питащия човек" and "питащият човек" in italics inside
#   Part II's quotation (the scheme in bold italics): emphasis carried from
#   the passage, not words the task points at; no stem.
# - Reading text: pp2-3 (rendered: title "Google като отговор" p2 y188, the
#   text to its source line p3 y459-473, an author's note under it;
#   questions from p3 y594). The live Part I cards of this sitting carry
#   sourceMaterial.pages [3], which the render does not agree with (p2
#   holds the title and the first paragraphs): (2, 3) here; the live cards
#   are flagged for the lead, not changed.
# GLYPHS: none in the lines used.

CRIT_2016 = crit((150, 151), (152, 154), (155, 156), (157, 158))
ESSAY_2016 = 'Напишете съчинение'


def _part3_note_2016(d):
    return (f'Under the two titles the scheme prints only “{L(146, 147).text(d)}” Under '
            f'“{S(148).text(d)}” it prints its criteria for the first two parts only: “{S(149).text(d)}”')


SPECS[2016] = [
    R('II1', [graded(S(125), PARTP(), CRIT_2016)],
      rownote=both(quote(S(149), lead='The scheme prints'), examples(S(126), L(127, 134))),
      pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2016)],
      question=QP(4, ESSAY_2016, '1. „Човекът')),
    R('III2', [unprinted(_part3_note_2016)],
      question=QP(4, ESSAY_2016, Run('2. „Светът', '(Финтан'))),
]


# ================================================================ 2017 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1а-д, I2-I6 (10 cards); not touched.
# Paper (rendered pp2-4): "Въпроси (100 точки)" (p3 y602); "Втора част" with
# "(30/100)" in the right-hand cell (p4 y341/342); "Трета част" with
# "(40/100)" (p4 y547/548), two titles joined by "или". No "30 точки"/"40
# точки" under the tasks this sitting: the head cells only.
# PRICES: II1 "(30/100)", III1/III2 "(40/100)" (PARTP; the census reads the
# three part heads).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-5; content in italics):
# - Part II (117-125 reprint the task as the paper prints it, no price): the
#   underlined descriptive line "Лична интерпретация, ясни и непротиворечиви
#   идеи." (126), then one paragraph of indicative content (127-136) that
#   opens with the words "Различни възможности за отговор." run into its
#   first line (2016 set the same words as a heading of their own) and ends
#   with an "Примерен цитат:" (Зиг Зиглар).
# - Part III (141-146): the instruction and title 1 reprinted; title 2 is
#   printed EMPTY, "2. „” ()" (146; rendered p5: the number, an empty pair of
#   quotation marks and an empty pair of brackets, nothing else). Then one
#   underlined descriptive line only (147-149, "Умение за създаване на
#   цялостен, логически последователен ... речеви умения.").
# - Criteria ("Бележки:", 150-162, italics): "При оценяването на отговорите
#   от първите две части се прилагат следните критерии:" -- the FIRST TWO
#   parts (I and II), not Part III. 1. 30 % (153-154), 2. 30 % (155-158),
#   3. 30 % (159-160), 4. 10 % (161-162): all four printed, 100 %.
# SHAPES:
# - II1: graded on the four criteria (10b): 9 / 9 / 9 / 3 of the paper's 30,
#   whole numbers. Head: the part's own descriptive line (126). The criteria's
#   lead quoted; the paragraph quoted as examples, not a checklist (10a).
# - III1/III2: only a descriptive line, criteria for the first two parts
#   only: R4 (unprinted) at the paper's 40, quoting both.
# JUDGEMENT CALLS:
# - Part II's paragraph is quoted whole, its opening words "Различни
#   възможности за отговор." included: they are set inside the paragraph's
#   first line, not as a heading of their own (rendered p4).
# - Part III title 2: the scheme's printed error, an empty reprint of the
#   title, is quoted on that card's note (10f: printed SEC errors go in the
#   first row's contextNote); the question is the paper's title.
# - Part III is NOT graded although the criteria are printed under it: the
#   scheme's own lead limits them to "първите две части".
# - Reading text: pp2-3 (rendered: title "Позитивното мислене" p2 y163, the
#   text to its source line p3 y507, an author's note under it; questions
#   from p3 y602). The live Part I cards of this sitting carry
#   sourceMaterial.pages [3], which the render does not agree with: (2, 3)
#   here; the live cards are flagged for the lead, not changed.
# GLYPHS: none in the lines used (the scheme's line 74 "ограниченo", a
# Latin o, is in Part I, not used here).

CRIT_2017 = crit((153, 154), (155, 158), (159, 160), (161, 162))
ESSAY_2017 = 'Напишете съчинение'


def _part3_note_2017(d):
    return (f'Under the two titles the scheme prints only “{L(147, 149).text(d)}” Under '
            f'“{S(150).text(d)}” it prints its criteria for the first two parts only: “{L(151, 152).text(d)}”')


def _empty_title_2017(d):
    return (f'The scheme reprints this title empty, as “{S(146).text(d)}”: the number, an empty pair of '
            f'quotation marks and empty brackets. The paper\'s title is the question.')


SPECS[2017] = [
    R('II1', [graded(S(126), PARTP(), CRIT_2017)],
      rownote=both(quote(L(151, 152), lead='The scheme prints'), examples(None, L(127, 136))),
      pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2017)],
      question=QP(4, ESSAY_2017, Run('1. „Ще обикна', 'мрака, защото'))),
    R('III2', [unprinted(both(_part3_note_2017, _empty_title_2017))],
      question=QP(4, ESSAY_2017, Run('2. „Моето мнение', 'в контекста на'))),
]


# ================================================================ 2018 HL ===
# Drafted (small-languages lane, 20 Nov): the 3 asks with no live card.
# Live: I1а-д, I2-I6. Open here: II1, III1, III2 (the old reader excluded them).
# Paper (rendered p4, booklet page 3): "Първа част (30 /100)"; "Втора част
# (30/100)" (p4 y420, on the head's own line: PARTP); "Трета част (40/100)"
# (p4 y562, PARTP). Part II prints a quotation from the text and "Какво е
# вашето мнение? Обяснете защо. (около 100 думи)"; Part III prints the
# instruction "Напишете съчинение (минимум 300 думи) на една от следните теми:"
# and two titles joined by "или".
# Scheme (rendered pp4-5):
# - Part II (lines 122-151): the task reprinted as the paper prints it, then an
#   underlined descriptive line "Лична интерпретация, ясни и непротиворечиви
#   идеи." (129) and one paragraph of possible directions (130-151, running
#   over the p4/p5 break: lines 132-135 are the page number and the page head,
#   left out of the join).
# - Part III (152-161): the instruction and both titles reprinted (bold), then
#   an underlined descriptive line "Умение за създаване на цялостен, ...
#   езикова компетентност и речеви умения." (159-161).
# - "Бележки:" (162-174): "При оценяването на отговорите от първите две части
#   се прилагат следните критерии:" then four criteria 30 % / 30 % / 30 % / 10 %.
#   READ: the criteria are stated for the FIRST TWO parts (Parts I and II), not
#   Part III, although the scheme sets them under Part III on p5.
# Shapes:
# - II1: graded on the four criteria at the paper's 30 (9/9/9/3, whole
#   numbers: 10b), the row headed by Part II's own descriptive line (129); the
#   criteria's lead line quoted, and the paragraph of directions quoted as
#   examples, not a checklist (10a).
# - III1, III2: the scheme states no criteria for Part III and prints only its
#   descriptive line: R4 at the paper's 40 (unprinted), the note quoting that
#   line and the criteria's lead (so the reader sees they are stated for the
#   first two parts only).
# Judgement calls:
# - The criteria's scope read as printed ("първите две части" = Parts I and
#   II). If the lead reads them as Parts II and III (Part I is point-marked),
#   III1/III2 become graded(L(159, 161), PARTP(), CRIT_2018) (12/12/12/4).
# - Title 1 prints "Сързан съм" on paper and scheme alike (the text's phrase is
#   "свързан съм"): kept as printed, not quoted (the same on both documents).
# - Questions: II1 is the census's text (its "(30/100)" taken off by
#   clean_question); III1/III2 are cut from the paper's lines with the
#   instruction before the title (the census glues "или" to title 1).
# - Reading text pp2-3 (rendered: title "Селфито – бягство от несигурността"
#   p2 y147, the text to the source line and author note on p3 y689; questions
#   on p4). The live 2018 cards carry pages [4] (the questions page): flagged
#   for the lead, not changed here.
# No glyph problems.

CRIT_2018 = crit((165, 166), (167, 170), (171, 172), (173, 174))
LEAD_2018 = L(163, 164)
ESSAY_2018 = 'Напишете съчинение (минимум 300 думи)'


def _essay_2018(d):
    return (f'Under Part III the scheme reprints the instruction and the two titles and prints only '
            f'“{L(159, 161).text(d)}” Its criteria are printed for the first two parts only: '
            f'“{LEAD_2018.text(d)}”')


SPECS[2018] = [
    R('II1', [graded(S(129), PARTP(), CRIT_2018)],
      rownote=both(quote(LEAD_2018, lead='The scheme prints'),
                   examples(None, J(L(130, 131), L(136, 151)))),
      pages=(2, 3)),
    R('III1', [unprinted(_essay_2018)],
      question=QP(4, ESSAY_2018, '1. Сързан съм')),
    R('III2', [unprinted(_essay_2018)],
      question=QP(4, ESSAY_2018, Run('2. Дрехите правят', 'за и против'))),
]


# ================================================================ 2019 HL ===
# Drafted (small-languages lane, 20 Nov): the 3 asks with no live card.
# Live: I1а-д, I2-I6. Open here: II1, III1, III2 (the old reader excluded them).
# Paper (rendered p4, booklet page 3): "Първа част (30 /100)"; "Втора част
# (30/100)" (p4 y506, on the head's own line: PARTP); "Трета част (40/100)"
# (p4 y601, PARTP). Part II prints "„Виртуалната реалност отнема
# свободата...”" and "Какво е вашето мнение? Обяснете защо. (около 100 думи)";
# Part III the instruction "Напишете съчинение (минимум 300 думи) на една от
# следните теми:" and two titles joined by "или".
# Scheme (rendered pp4-5), laid out as 2018:
# - Part II (lines 120-135, p4): the task reprinted as the paper prints it,
#   then the bold-italic descriptive line "Лична интерпретация, ясни и
#   непротиворечиви идеи." (123) and one paragraph of possible directions
#   (124-135, all on p4).
# - Part III (140-149, p5): the instruction and both titles reprinted (bold),
#   then the bold descriptive line "Умение за създаване на цялостен, ...
#   езикова компетентност и речеви умения." (147-149).
# - "Бележки:" (150-162, p5): "При оценяването на отговорите от първите две
#   части се прилагат следните критерии:" then four criteria 30 % / 30 % /
#   30 % / 10 %. READ: stated for the FIRST TWO parts (Parts I and II), not
#   Part III, although set on p5 under Part III.
# Shapes (as 2018):
# - II1: graded on the four criteria at the paper's 30 (9/9/9/3: 10b), headed
#   by Part II's own descriptive line (123); the criteria's lead quoted, the
#   paragraph of directions quoted as examples, not a checklist (10a).
# - III1, III2: no criteria stated for Part III, only its descriptive line: R4
#   at the paper's 40, the note quoting that line and the criteria's lead.
# Judgement calls:
# - Criteria scope read as printed ("първите две части"); if the lead reads
#   Parts II and III, III1/III2 become graded(L(147, 149), PARTP(), CRIT_2019)
#   (12/12/12/4).
# - The scheme's Part II paragraph prints "понятиeто" and "изрaзът" with Latin
#   e/a inside Cyrillic words (lines 127, 133; rendered p4 they look the same):
#   a printed mixed-script spelling in the .md text layer, left as it is; it is
#   only in the quoted examples note, never a row a student claims.
# - Questions: II1 the census's text ("(30/100)" taken off); III1/III2 cut
#   from the paper's lines, instruction first (the census glues "или" to
#   title 1).
# - Reading text pp2-3 (rendered: title "БЪДЕЩЕТО" p2, the text to the source
#   line and author note at the foot of p3; questions on p4). The live 2019
#   cards carry pages [4]: flagged for the lead, not changed here.
# No glyph problems beyond the two mixed-script letters above.

CRIT_2019 = crit((153, 154), (155, 158), (159, 160), (161, 162))
LEAD_2019 = L(151, 152)
ESSAY_2019 = 'Напишете съчинение (минимум 300 думи)'


def _essay_2019(d):
    return (f'Under Part III the scheme reprints the instruction and the two titles and prints only '
            f'“{L(147, 149).text(d)}” Its criteria are printed for the first two parts only: '
            f'“{LEAD_2019.text(d)}”')


SPECS[2019] = [
    R('II1', [graded(S(123), PARTP(), CRIT_2019)],
      rownote=both(quote(LEAD_2019, lead='The scheme prints'),
                   examples(None, L(124, 135))),
      pages=(2, 3)),
    R('III1', [unprinted(_essay_2019)],
      question=QP(4, ESSAY_2019, '1. Бъдещето е вече')),
    R('III2', [unprinted(_essay_2019)],
      question=QP(4, ESSAY_2019, Run('2. Една година почивка', 'и двете възможности'))),
]


# ================================================================ 2020 HL ===
# Drafted (small-languages lane, 20 Nov): the 3 asks with no live card.
# Live: I1а-д, I2-I6. Open here: II1, III1, III2 (the old reader excluded them).
# Paper (rendered pp3-4): "Първа част (30 /100)" (p3 y628); "Втора част
# (30/100)" (p4 y400, on the head's own line: PARTP); "Трета част (40/100)"
# (p4 y535, PARTP). Part II prints a quotation from the text and "Съгласни ли
# сте с автора? Обяснете защо. (около 100 думи)"; Part III the instruction
# "Напишете съчинение (минимум 300 думи) на една от следните теми:" and two
# titles joined by "или".
# Scheme (rendered pp4-5), laid out as 2018-2019:
# - Part II (lines 113-134): the task reprinted as the paper prints it, the
#   underlined-italic descriptive line "Лична интерпретация, ясни и
#   непротиворечиви идеи." (119) and one paragraph of possible directions
#   (120-129, running over the p4/p5 break to line 134; lines 130-133 are the
#   page number and head, left out of the join).
# - Part III (135-143, p5): instruction and both titles reprinted, then the
#   underlined descriptive line "Умение за създаване на цялостен, ...
#   речеви умения." (141-143).
# - "Бележки:" (144-157, p5): "При оценяването на отговорите от първите две
#   части се прилагат следните критерии:" then four criteria 30/30/30/10 %.
#   READ: stated for the FIRST TWO parts (Parts I and II), not Part III.
# Shapes (as 2018-2019):
# - II1: graded on the four criteria at the paper's 30 (9/9/9/3: 10b), headed
#   by Part II's own descriptive line (119); the criteria's lead quoted, the
#   paragraph quoted as examples, not a checklist (10a).
# - III1, III2: R4 at the paper's 40, the note quoting Part III's descriptive
#   line and the criteria's lead.
# Judgement calls:
# - Criteria scope read as printed; if the lead reads Parts II and III,
#   III1/III2 become graded(L(141, 143), PARTP(), CRIT_2020) (12/12/12/4).
# - Title 2: the scheme reprints it without the paper's quotation marks
#   (line 140): punctuation only, not quoted.
# - GLYPHS (reported, not repaired): the PAPER's title 2 is typed with Latin
#   letters inside Cyrillic words in the same Calibri font ("Приятелитe ми ca
#   моeтo семейство, членоветe нa ...": Latin e, c, a, e, o, e, a; rawdict,
#   p4 y676). They render identically to the Cyrillic letters (p4 rendered),
#   so they are what the SEC typed, not a mis-mapped glyph; the question text
#   carries them as the text layer gives them. Flagged for the lead (a
#   mixed-script check or search would trip on them). The scheme's reprint
#   (line 140) is all Cyrillic.
# - Questions: II1 the census's text ("(30/100)" taken off); III1/III2 cut
#   from the paper's lines, instruction first (the census glues "или" to
#   title 1). Title 1 keeps the paper's attribution line "(Андре Мороа,
#   Чувства и обичаи)".
# - Reading text pp2-3 (rendered: title "Благодатта на „частното”" p2, the text
#   to the author note on p3 y553; questions from p3 y586). The live 2020
#   cards carry pages [3]: flagged for the lead, not changed here.

CRIT_2020 = crit((147, 148), (149, 152), (153, 154), (155, 157))
LEAD_2020 = L(145, 146)
ESSAY_2020 = 'Напишете съчинение (минимум 300 думи)'


def _essay_2020(d):
    return (f'Under Part III the scheme reprints the instruction and the two titles and prints only '
            f'“{L(141, 143).text(d)}” Its criteria are printed for the first two parts only: '
            f'“{LEAD_2020.text(d)}”')


SPECS[2020] = [
    R('II1', [graded(S(119), PARTP(), CRIT_2020)],
      rownote=both(quote(LEAD_2020, lead='The scheme prints'),
                   examples(None, J(L(120, 129), S(134)))),
      pages=(2, 3)),
    R('III1', [unprinted(_essay_2020)],
      question=QP(4, ESSAY_2020, Run('1. „Без семейство', '(Андре Мороа'))),
    R('III2', [unprinted(_essay_2020)],
      question=QP(4, ESSAY_2020, '2. „Приятел')),
]


# ================================================================ 2021 HL ===
# Drafted (small-languages lane, 20 Nov): the 5 asks with no live card.
# Live: I1а-д, I2, I5. Open here: I3, I4, I6, II1, II2 (the old reader
# excluded them). Two parts: "Част първа" (30/70) and "Част втора (40/70)"
# (p4 y556, PARTP), the essay; keys II1/II2 are its two titles.
# PRICES: the exclusions say Q3, Q4 and Q6 print "no marks in [the] right-hand
# margin and the scheme prints none at all". BOTH ARE WRONG. The paper prints
# "5 точки" at the END OF THE QUESTION'S OWN LINE for each (rendered p4: Q3
# y297 "... Защо, според вас? 5 точки", Q4 y341 "... и защо? 5 точки", Q6 y472
# "... „политическа коректност”? 5 точки"; the census strips the price from
# the text but reads no tariff because it is not a cell of its own). The
# scheme prints "5 точки" too, on a line of its own under each reprinted
# question (lines 74, 81, 123). So each is priced from the paper's own line
# (PaperP(4, opening)), card total included. Not unpriced: no REM, no 10i.
# Scheme (rendered pp3-5):
# - Q3 (73-79): one paragraph of answer -> one row at 5.
# - Q4 (80-97): one paragraph running over the p3/p4 break (lines 88-91 are
#   the page number and head, left out of the join) -> one row at 5.
# - Q6 (120-135): one paragraph -> one row at 5.
#   (One printed paragraph = one row at the printed price: Romanian 2012 Q5,
#   2026 Q2; the live 2021 Q2/Q5 cards are one row at 5.)
# - Part II (140-148, p5): the instruction reprinted in other words, both
#   titles, the bold-italic descriptive line "Умение за създаване на
#   цялостен, ... компетентност и речеви умения." (146-148).
# - "Бележки:" (149-162): "При оценяването на отговорите от първите две части
#   се прилагат следните критерии:" (in a two-part sitting, Parts I and II:
#   the essay included) and the four criteria WITH NO PERCENTAGES and no marks
#   (rendered p5: the lines end "ясно и точно;", "определена логика", "ясен и
#   точен", "книжовен език"). The exclusion's "30%" evidence for 2018-2020 is
#   not on this scheme.
# Shapes:
# - I3, I4, I6: one row each at the paper's 5, the row cut to the answer
#   (after the scheme's dash; the reprinted question and price left out).
# - II1, II2: criteria named but no percentages, so 10b cannot give marks per
#   criterion: R4 at the paper's 40 (brief, ruling 4: "otherwise the printed
#   total plus the R4 line"), the note quoting the descriptive line, the
#   criteria's lead and the four criteria as printed.
# Judgement calls:
# - II1/II2 follow the brief's ruling 4 (unprinted), NOT Romanian 2021's model
#   (the four criteria as shown rows, questionTotal 40). Flip if the lead
#   prefers the Romanian shape: rows [shown(L(152, 153)), shown(L(154, 157)),
#   shown(L(158, 159)), shown(L(160, 162))], whole=True.
# - The scheme reprints the instruction as "Напишете съчинение (минимум 300
#   думи) на една от следните теми:" where the paper prints "Напишете есе
#   (минимум 300 думи) по една от следните теми:": the paper wins on the
#   question, the scheme's words quoted (10f).
# - Titles: the scheme reprints title 1 without its quotation marks and both
#   attributions in brackets ("(Иван Тургенев)" for the paper's "- Иван
#   Тургенев"): punctuation only, not quoted.
# - Q6's answer prints "цивилизоционен филтър" (the paper's text and question
#   print "цивилизационен"): the scheme's own spelling inside a row, kept as
#   printed (lifted, never corrected).
# - Q4's answer line 85 prints U+2010 as a dash ("и малцинства ‐ социални"):
#   kept as printed.
# - No `pages` on Part II: a two-part sitting's Part II is the essay.
#   Part I pages (2, 3), rendered: the text from p2 to the sources and author
#   note at the foot of p3; questions on p4. The live 2021 cards carry [2, 3].
# - The census glues "5 точки" inside live I2's question text ("Обяснете
#   значението 5 точки на тази поговорка."): live card, not touched here,
#   flagged for the lead.
# No glyph problems (U+2010 HYPHEN in the scheme's "по‐силна" etc. is a real
# hyphen).


def _p2021(opening):
    return PaperP(4, opening)


CRIT_LINES_2021 = (L(152, 153), L(154, 157), L(158, 159), L(160, 162))


def _essay_2021(d):
    crits = ' '.join(f'“{c.text(d)}”' for c in CRIT_LINES_2021)
    return (f'The scheme reprints the instruction as “{S(141).text(d)}” and the two titles, and prints '
            f'“{L(146, 148).text(d)}” Under “{S(149).text(d)}” it prints “{L(150, 151).text(d)}” and the '
            f'four criteria with no marks or percentages beside them: {crits}')


# Lead (20 Nov): the lane's shape for criteria printed with no percentages
# and stated for this part (Romanian 2021/2022): the four criteria as shown
# rows on the paper's 40 (questionTotal), their lead and the part's
# descriptive line quoted (raised with the coordinator as decision F).
def _crit_note_2021(d):
    return (f'Under the two titles the scheme prints “{L(146, 148).text(d)}” It then prints, with no marks or '
            f'percentages beside the criteria: “{L(150, 151).text(d)}” It reprints the instruction as “{S(141).text(d)}”')


ESSAY_2021 = 'Напишете есе (минимум 300 думи)'
SPECS[2021] = [
    R('I3', [one(L(75, 79), _p2021('3. В текста'))], total=_p2021('3. В текста'), pages=(2, 3)),
    R('I4', [one(J(L(82, 87), L(92, 97)), _p2021('4. С кои'))], total=_p2021('4. С кои'), pages=(2, 3)),
    R('I6', [one(L(124, 135), _p2021('възпитание” и не е ли'))], total=_p2021('възпитание” и не е ли'),
      pages=(2, 3)),
    R('II1', [shown(c) for c in CRIT_LINES_2021], whole=True, rownote=_crit_note_2021,
      question=QP(4, ESSAY_2021, '1. „Всеки човек')),
    R('II2', [shown(c) for c in CRIT_LINES_2021], whole=True, rownote=_crit_note_2021,
      question=QP(4, ESSAY_2021, Run('2. „Вие не можете', 'не харесвате'))),
]


# ================================================================ 2022 HL ===
# Drafted (small-languages lane, 20 Nov): the 4 asks with no live card.
# Live: I1а-д, I3, I4, I6. Open here: I2, I5, II1, II2 (the old reader
# excluded them). Two parts: "Първа част (30 /70)" (p2 y124) and "Втора част
# (40/70)" (p4 y528, PARTP), the essay; keys II1/II2 are its two titles.
# PRICES: the exclusions say Q2 and Q5 print no marks in the right-hand margin
# and the scheme none at all. BOTH ARE WRONG. The paper prints "5 точки" at
# the END OF THE QUESTION'S OWN LAST LINE (rendered p4: Q2 y263 "работата
# онлайн и каква е цената на този прогрес? 5 точки"; Q5 y395 "режим”?
# Обяснете за какво става въпрос? 5 точки"); the census reads no tariff
# because the price is not a cell of its own. The scheme prints "5 точки" too
# (line 68 at the end of the reprinted Q2, line 111 under Q5). Each is priced
# from the paper's own line (PaperP(4, opening)), card total included. Not
# unpriced: no REM, no 10i.
# Scheme (rendered pp3-5):
# - Q2 (67-76): one paragraph of answer after a dash -> one row at 5.
# - Q5 (109-117, p4): one paragraph (no dash) -> one row at 5.
#   (One printed paragraph = one row at the printed price: Romanian 2012 Q5,
#   2026 Q2; the live 2022 Q3/Q4/Q6 cards are one row at 5.)
# - Part II (142-150, p5): "Втора част" / "(40/70)", the instruction and both
#   titles reprinted as the paper prints them, then the descriptive line
#   "Умение за създаване на цялостен, ... компетентност и речеви умения."
#   (148-150).
# - "Бележки:" (151-162): "При оценяването на отговорите от първите две части
#   се прилагат следните критерии:" (a two-part sitting: Parts I and II, the
#   essay included) and four criteria WITH NO PERCENTAGES and no marks.
# Shapes:
# - I2, I5: one row each at the paper's 5, cut to the answer.
# - II1, II2: criteria named but no percentages (10b cannot give per-criterion
#   marks): R4 at the paper's 40 (brief, ruling 4), the note quoting the
#   descriptive line, the criteria's lead and the four criteria as printed.
# Judgement calls:
# - II1/II2 follow the brief's ruling 4 (unprinted), not Romanian 2022's
#   shown-criteria rows (flip as for 2021 if the lead prefers that shape).
# - Scheme Q1(г) prints "(присъжда се 1 точка на всeки кандидат)" (1 mark to
#   every candidate) beside "манифестация" (line 61): Q1 is live, not touched,
#   flagged for the lead (the live I1г card does not say so). That line also
#   carries a Latin "e" in "всeки".
# - Reading text pp2-3 (rendered: "Първа част" and the instruction p2 y124,
#   the text from p2 to the source line and author note at the foot of p3; p4
#   opens "Въпроси" and prints only questions). The live 2022 cards carry
#   [2, 3, 4]: the render does not agree, so (2, 3) here; flagged.
# - No `pages` on Part II (the essay of a two-part sitting).
# No glyph problems (U+2010 HYPHEN in "по‐производителен" etc. on paper and
# scheme is a real hyphen).

CRIT_LINES_2022 = (L(154, 155), L(156, 158), L(159, 160), L(161, 162))


def _essay_2022(d):
    crits = ' '.join(f'“{c.text(d)}”' for c in CRIT_LINES_2022)
    return (f'The scheme reprints the instruction and the two titles, and prints “{L(148, 150).text(d)}” '
            f'Under “{S(151).text(d)}” it prints “{L(152, 153).text(d)}” and the four criteria with no marks '
            f'or percentages beside them: {crits}')


Q2P_2022 = PaperP(4, 'работата онлайн и каква')
Q5P_2022 = PaperP(4, 'режим”? Обяснете')
# Lead (20 Nov): criteria as shown rows on the paper's 40, as 2021 (decision F).
def _crit_note_2022(d):
    return (f'Under the two titles the scheme prints “{L(148, 150).text(d)}” It then prints, with no marks or '
            f'percentages beside the criteria: “{L(152, 153).text(d)}”')


ESSAY_2022 = 'Напишете съчинение (минимум 300 думи)'
SPECS[2022] = [
    R('I2', [one(L(69, 76), Q2P_2022)], total=Q2P_2022, pages=(2, 3)),
    R('I5', [one(L(112, 117), Q5P_2022)], total=Q5P_2022, pages=(2, 3)),
    R('II1', [shown(c) for c in CRIT_LINES_2022], whole=True, rownote=_crit_note_2022,
      question=QP(4, ESSAY_2022, '1. „Изглежда')),
    R('II2', [shown(c) for c in CRIT_LINES_2022], whole=True, rownote=_crit_note_2022,
      question=QP(4, ESSAY_2022, '2. Какво прави')),
]


# ================================================================ 2023 HL ===
# Drafted (small-languages lane, 20 Nov): the 4 asks with no live card.
# Live: I1а-д, I3-I6. Open here: I2, II1, III1, III2 (the old reader excluded
# them).
# Paper (rendered p4): "Първа част (30/100)"; "Втора част (30/100)" (p4 y532,
# PARTP); "Трета част (40/100)" (p4 y629, PARTP); titles 1. and 2. joined by
# "или" under "Напишете съчинение (минимум 300 думи) на една от следните
# теми:".
# PRICE of Q2: the exclusion says the paper prints no marks in its right-hand
# margin and the scheme none at all. BOTH ARE WRONG. The paper prints "5
# точки" at the end of Q2's own last line (rendered p4 y306 "текста, защо
# мнението на Теслер е убедително? 5 точки"; the census reads no tariff as it
# is not a cell of its own), and the scheme prints "5 точки" at the end of its
# reprint (line 66). Priced from the paper's line (PaperP), card total
# included. Not unpriced: no REM, no 10i.
# Scheme (rendered pp3-5):
# - Q2 (65-70): one paragraph of answer after a dash -> one row at 5 (as the
#   live 2023 Q3-Q6, Romanian 2012 Q5).
# - Part II (140-151, p5): the task reprinted as the paper prints it, the
#   underlined-italic descriptive line "Лична интерпретация, ясни и
#   непротиворечиви идеи." (143), one paragraph of possible directions
#   (144-151).
# - Part III (152-159, p5): instruction and both titles reprinted, the
#   underlined descriptive line "Умение за създаване на цялостен, ...
#   компетентност и речеви умения." (157-159).
# - "Бележки:" (160-171): "При оценяването на отговорите от първите две части
#   се прилагат следните критерии:" and four criteria 30/30/30/10 %. READ:
#   stated for the FIRST TWO parts (Parts I and II), not Part III.
# Shapes (as 2018-2020):
# - I2: one row at the paper's 5, cut to the answer.
# - II1: graded on the four criteria at the paper's 30 (9/9/9/3: 10b), headed
#   by Part II's descriptive line (143); criteria lead quoted, the paragraph
#   quoted as examples, not a checklist (10a).
# - III1, III2: R4 at the paper's 40, the note quoting Part III's descriptive
#   line and the criteria's lead.
# Judgement calls:
# - Criteria scope read as printed; if the lead reads Parts II and III,
#   III1/III2 become graded(L(157, 159), PARTP(), CRIT_2023) (12/12/12/4).
# - Reading text pp2-3 (rendered: "Първа част" and the instruction p2 y122,
#   the text to the source line and author note on p3; p4 opens "Въпроси" and
#   prints only questions). The live 2023 cards carry [2, 3, 4]: the render
#   does not agree, so (2, 3) here; flagged.
# - Questions: II1 the census's text ("(30/100)" taken off); III1/III2 cut
#   from the paper's lines, instruction first (the census glues "или" to
#   title 1). Title 2 keeps the paper's attribution "(Иван Вазов)".
# No glyph problems (U+2010 HYPHEN in the scheme's "по‐добро" etc. is a real
# hyphen).

CRIT_2023 = crit((163, 164), (165, 167), (168, 169), (170, 171))
LEAD_2023 = L(161, 162)
ESSAY_2023 = 'Напишете съчинение (минимум 300 думи)'
Q2P_2023 = PaperP(4, 'текста, защо мнението')


def _essay_2023(d):
    return (f'Under Part III the scheme reprints the instruction and the two titles and prints only '
            f'“{L(157, 159).text(d)}” Its criteria are printed for the first two parts only: '
            f'“{LEAD_2023.text(d)}”')


SPECS[2023] = [
    R('I2', [one(L(67, 70), Q2P_2023)], total=Q2P_2023, pages=(2, 3)),
    R('II1', [graded(S(143), PARTP(), CRIT_2023)],
      rownote=both(quote(LEAD_2023, lead='The scheme prints'),
                   examples(None, L(144, 151))),
      pages=(2, 3)),
    R('III1', [unprinted(_essay_2023)],
      question=QP(4, ESSAY_2023, '1. „Вярата')),
    R('III2', [unprinted(_essay_2023)],
      question=QP(4, ESSAY_2023, '2. „Идеалът')),
]


# ================================================================ 2024 HL ===
# Drafted (small-languages lane, 20 Nov): the 3 asks with no live card.
# Live: I1а-д, I2-I6. Open here: II1, III1, III2 (the old reader excluded
# them).
# Paper (rendered p4): "Първа част (30/100)"; "Втора част (30/100)" (p4 y489,
# PARTP); "Трета част (40/100)" (p4 y604, PARTP); titles 1. and 2. joined by
# "или" under "Напишете съчинение (минимум 300 думи) на една от следните
# теми:".
# Scheme (rendered p5):
# - Part II (135-149): the task reprinted as the paper prints it, the
#   underlined-italic descriptive line "Лична интерпретация, ясни и
#   непротиворечиви идеи." (138), one paragraph of possible directions
#   (139-149).
# - Part III (150-158): instruction and both titles reprinted, the underlined
#   descriptive line "Умение за създаване на цялостен, ... речеви умения."
#   (157-158).
# - "Бележки:" (159-170): "При оценяването на отговорите от първите две части
#   се прилагат следните критерии:" and four criteria 30/30/30/10 %. READ:
#   stated for the FIRST TWO parts (Parts I and II), not Part III.
# Shapes (as 2018-2023):
# - II1: graded on the four criteria at the paper's 30 (9/9/9/3: 10b), headed
#   by Part II's descriptive line (138); criteria lead quoted, the paragraph
#   quoted as examples, not a checklist (10a).
# - III1, III2: R4 at the paper's 40, the note quoting Part III's descriptive
#   line and the criteria's lead.
# Judgement calls:
# - Criteria scope read as printed; if the lead reads Parts II and III,
#   III1/III2 become graded(L(157, 158), PARTP(), CRIT_2024) (12/12/12/4).
# - Criterion 2 is printed shorter than in 2018-2023 (it ends
#   "непротиворечиви – 30%;", line 166, with no "композицията ..."): lifted as
#   printed.
# - Reading text pp2-3 (rendered: "Първа част" and the instruction p2 y138,
#   the text to the source line and author note at the foot of p3; p4 opens
#   "Въпроси"). The live 2024 cards carry [2, 3, 4]: the render does not
#   agree, so (2, 3) here; flagged.
# - Questions: II1 the census's text ("(30/100)" taken off); III1/III2 cut
#   from the paper's lines, instruction first (the census glues "или" to
#   title 1).
# No glyph problems (U+2010 HYPHEN in "100‐150", "най‐голямо" etc. is a real
# hyphen).

CRIT_2024 = crit((162, 163), (164, 166), (167, 168), (169, 170))
LEAD_2024 = L(160, 161)
ESSAY_2024 = 'Напишете съчинение (минимум 300 думи)'


def _essay_2024(d):
    return (f'Under Part III the scheme reprints the instruction and the two titles and prints only '
            f'“{L(157, 158).text(d)}” Its criteria are printed for the first two parts only: '
            f'“{LEAD_2024.text(d)}”')


SPECS[2024] = [
    R('II1', [graded(S(138), PARTP(), CRIT_2024)],
      rownote=both(quote(LEAD_2024, lead='The scheme prints'),
                   examples(None, L(139, 149))),
      pages=(2, 3)),
    R('III1', [unprinted(_essay_2024)],
      question=QP(4, ESSAY_2024, Run('1. „Техническият', 'науката на съзнанието'))),
    R('III2', [unprinted(_essay_2024)],
      question=QP(4, ESSAY_2024, Run('2. „Най‐безнадеждното', 'да стига до своята'))),
]


# ================================================================ 2025 HL ===
# Drafted (small-languages lane, 20 Nov): the 7 asks with no live card.
# Live: I1а, I2-I6. Open here: I1б, I1в, I1г, I1д, II1, III1, III2.
# Paper (rendered p4): "Първа част (30/100)"; Q1 "Какво е значението на
# думите и на изразите в текста?" over а) просперитет, б) фолклор, в) вълшебна
# приказка, г) остроумие, д) обективно установено, "1 точка" beside each (the
# census reads 1 each: PP()); "Втора част (30/100)" (p4 y530, PARTP); "Трета
# част (40/100)" (p4 y627, PARTP), titles 1. and 2. joined by "или".
# Q1(б)-(д): the census flags "the scheme prices no ask that pairs with it".
# READ: the scheme letters its Q1 answers "а)" (Cyrillic, U+0430) then "b)",
# "c)", "d)", "e)" in LATIN (U+0062-0065; rawdict, Calibri,Bold, scheme p4),
# so the census's Cyrillic б/в/г/д find no partner. Paired by WORDS, each
# scheme head reprinting the paper's expression: "b) фолклор" (64) = б)
# фолклор; "c) вълшебна приказка" (66) = в); "d) остроумие" (69) = г); "e)
# обективно установено" (71) = д). Each prints "1 точка" and one gloss line
# under it (after a dash): one row each at the paper's 1 (PP()).
# Scheme (rendered pp4-6, p7-8 blank but for page numbers):
# - Part II (132-141, p6): the task reprinted with "(около 150 думи)" for the
#   paper's "(100 - 150 думи)", the bold-italic descriptive line "Лична
#   интерпретация, ясни и непротиворечиви идеи." (135) and one paragraph of
#   content (136-141), no marks.
# - Part III (142-150, p6): instruction and both titles reprinted, then the
#   italic descriptive line "Умение за създаване на цялостен, ... речеви
#   умения." (148-150).
# - NO "Бележки", NO criteria and NO percentages anywhere in this scheme (the
#   exclusions' "prints NOTHING under this task" is wrong for Part II, which
#   has a paragraph of content, and for Part III, which has its descriptive
#   line).
# Shapes:
# - I1б-д: one row each at 1 (the gloss, after the dash).
# - II1: the paragraph is the scheme's content for the part, under its own
#   heading (10a): one shown row, priced as a whole on the paper's 30
#   (questionTotal), the heading quoted (as Romanian 2025/2026 Part II).
# - III1, III2: only a descriptive line: R4 at the paper's 40, the note
#   quoting it.
# Judgement calls:
# - Q1: the scheme reprints the question as "Какво е значението на
#   подчертаните думи и изрази в текста?" (the UNDERLINED words) where the
#   paper asks about "думите и на изразите в текста" and sets them in BOLD in
#   the text (rendered p3 "обективно установено"): the paper wins, the
#   scheme's words quoted (10f).
# - Part II: the scheme's "(около 150 думи)" for the paper's "(100 - 150
#   думи)": the paper wins, the scheme's line quoted (10f).
# - Titles: the scheme sets « » where the paper sets „ “ / “ ”: punctuation
#   only, not quoted.
# - The paragraph prints "на бългаски" (line 140, for "български"): the
#   scheme's own spelling inside a shown row, kept as printed.
# - Reading text pp2-3 (rendered: "Първа част" and the instruction p2 y137,
#   the text to the source line and author note at the foot of p3; p4 opens
#   "Въпроси"). The live 2025 cards carry [2, 3, 4]: the render does not
#   agree, so (2, 3) here; flagged.
# - Questions: I1б-д and II1 are the census's text (II1's "(30/100)" taken
#   off); III1/III2 cut from the paper's lines, instruction first.
# GLYPHS: the scheme's Latin b/c/d/e letters (above) are printed Latin glyphs,
# not a mis-mapping; they are never cut into a row. (Line 80, live Q3, prints
# a Latin e in "Спорeд": not used here.)

Q1HEAD_2025 = quote(S(61, after='1. '), lead='The scheme reprints the question as')
ESSAY_2025 = 'Напишете съчинение (минимум 300 думи)'


def _essay_2025(d):
    return (f'Under Part III the scheme reprints the instruction and the two titles and prints only '
            f'“{L(148, 150).text(d)}” It prints no criteria and no split of the part\'s marks.')


SPECS[2025] = [
    R('I1б', [one(S(65), PP())], rownote=Q1HEAD_2025, pages=(2, 3)),
    R('I1в', [one(L(67, 68), PP())], rownote=Q1HEAD_2025, pages=(2, 3)),
    R('I1г', [one(S(70), PP())], rownote=Q1HEAD_2025, pages=(2, 3)),
    R('I1д', [one(S(72), PP())], rownote=Q1HEAD_2025, pages=(2, 3)),
    R('II1', [shown(L(136, 141))], whole=True,
      rownote=both(quote(S(135), lead='The scheme heads it'),
                   quote(S(134), lead='The scheme reprints the last line of the task as')),
      pages=(2, 3)),
    R('III1', [unprinted(_essay_2025)],
      question=QP(4, ESSAY_2025, '1. „Нищо не развива')),
    R('III2', [unprinted(_essay_2025)],
      question=QP(4, ESSAY_2025, Run('2. “Човек винаги', 'А те са вътре'))),
]


# ================================================================ 2026 HL ===
# Drafted (small-languages lane, 20 Nov): the 5 asks with no live card.
# Live: I1а-д, I2-I4. Open here: I5, I6, II1, III1, III2.
# Paper (rendered p4): "Първа част (30 /100)"; Q1-Q4 priced in the margin;
# "Втора част (30/100)" (p4 y516, PARTP); "Трета част (40/100)" (p4 y621,
# PARTP); titles 1. and 2. joined by "или" under "Напишете съчинение (минимум
# 300 думи) на една от следните теми:".
# PRICES of Q5 and Q6: the exclusions say the paper prints no marks in its
# right-hand margin and the scheme none at all. BOTH ARE WRONG. The paper
# prints "5 точки" at the END OF THE QUESTION'S OWN LAST LINE (rendered p4:
# Q5 y448 "устоявала над конюнктурата и временните страсти.» Защо, според
# автора? 5 точки"; Q6 y475 "6. В романа «1984» ... Защо? 5 точки"; the census
# reads no tariff as the price is not a cell of its own), and the scheme
# prints "5 точки" under each reprint (lines 117, 131). Each is priced from
# the paper's line (PaperP), card total included. Not unpriced: no REM, no
# 10i.
# Scheme (rendered pp4-6, p7-8 blank but for page numbers):
# - Q5 (115-125, p5): one paragraph after a dash; its second-last line breaks
#   after one word ("отнеме" / "време и ...", lines 124-125, rendered p5: the
#   same paragraph, no indent) -> one row at 5.
# - Q6 (130-136, p6): one paragraph -> one row at 5.
#   (One printed paragraph = one row at the printed price, as the live 2026
#   Q2-Q4 and Romanian 2026 Q2.)
# - Part II (137-154, p6): the task reprinted, the plain descriptive line
#   "Лична интерпретация, ясни и непротиворечиви идеи." (141) and one
#   paragraph of content after a dash (142-154), no marks.
# - Part III (155-163, p6): instruction and both titles reprinted, then the
#   descriptive line "Умение за създаване на цялостен, ... речеви умения."
#   (162-163).
# - NO "Бележки", NO criteria and NO percentages anywhere in this scheme.
# Shapes (as 2025):
# - I5, I6: one row each at the paper's 5, cut to the answer.
# - II1: the paragraph under the part's own heading (10a): one shown row,
#   priced as a whole on the paper's 30 (questionTotal), the heading quoted.
# - III1, III2: only a descriptive line: R4 at the paper's 40, the note
#   quoting it.
# Judgement calls:
# - Q5's answer prints "да се се е случило" (line 119, a doubled "се"): the
#   scheme's own words inside a row, kept as printed.
# - Part II: the scheme opens the quotation with „ and closes it with »
#   ("„В историческата наука ... гледна точка...»"), the paper « ... …»:
#   punctuation only, not quoted. Titles: „ ” for the paper's « »: likewise.
# - Reading text pp2-3 (rendered: title "Историята" p2 y153, the text to the
#   source line and author note on p3 y734; p4 opens "Въпроси"). The live 2026
#   cards carry [4] (the questions page): flagged for the lead, not changed.
# - Questions: I5, I6 and II1 are the census's text (II1's "(30/100)" taken
#   off); III1/III2 cut from the paper's lines, instruction first.
# GLYPHS (reported, not repaired): the PAPER's Q6 types "старитe" with a Latin
# e (U+0065) in the same Calibri font (rawdict p4 y475); it renders as the
# Cyrillic letter (rendered p4), so it is what the SEC typed, not a mis-mapped
# glyph. The question text carries it as the text layer gives it; the
# scheme's reprint (line 130) is all Cyrillic. Flagged for the lead.
# Aside (not carded): the cover's text layer (p1 y772) holds "Mathematics,
# Paper 1 – Higher Level", hidden under the cover's colour band (not visible
# on the render): a template leftover, nothing a card reads.

Q5P_2026 = PaperP(4, 'устоявала над конюнктурата')
Q6P_2026 = PaperP(4, '6. В романа')
ESSAY_2026 = 'Напишете съчинение (минимум 300 думи)'


def _essay_2026(d):
    return (f'Under Part III the scheme reprints the instruction and the two titles and prints only '
            f'“{L(162, 163).text(d)}” It prints no criteria and no split of the part\'s marks.')


SPECS[2026] = [
    R('I5', [one(L(118, 125), Q5P_2026)], total=Q5P_2026, pages=(2, 3)),
    R('I6', [one(L(132, 136), Q6P_2026)], total=Q6P_2026, pages=(2, 3)),
    R('II1', [shown(L(142, 154))], whole=True,
      rownote=quote(S(141), lead='The scheme heads it'), pages=(2, 3)),
    R('III1', [unprinted(_essay_2026)],
      question=QP(4, ESSAY_2026, Run('1. «Начинът', '(Б. Кауфман)'))),
    R('III2', [unprinted(_essay_2026)],
      question=QP(4, ESSAY_2026, Run('2. «Какво ще ни', '(Никола Вапцаров)'))),
]


def specs(year):
    return SPECS.get(year, [])
