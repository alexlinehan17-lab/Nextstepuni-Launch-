#!/usr/bin/env python3
"""Reviewed specs for the Slovenian classic examination (small-languages lane).

One entry per printed ask with no live card; see sl_lib.py for the selector
language. Line numbers are lines of examiner-reports/slovenian/schemes/<year>-hl.md.
Drafted by Opus helpers on the Bulgarian, Romanian, Dutch and Maltese models, integrated
and gated by the lane lead.
"""
from sl_lib import (R, S, SR, J, L, PL, PC, QP, QL, Run, pre, prerun, PP, SP, PY, RX, PaperP, PARTP, REM,  # noqa: F401
                    one, shown, graded, crit, examples, quote, unprinted, part, NoScheme, Unpriced)
from pl_listen_lib import Join  # noqa: F401
from sl_lib import paper_run, MARKER, clean_question  # noqa: F401,E402

SPECS = {}


def both(*notes):
    """Several printed notes on one row, in order."""
    return lambda doc: ' '.join(n(doc) for n in notes)


def specs(year):
    return SPECS.get(year, [])


# ====================================================================== 2018
# ================================================================ 2018 HL ===
# Drafted (small-languages lane, 20 Nov): the open asks of this sitting, I1a-e
# (carded WHOLE at the parent key 'I1', see PRICES), II1, III1, III2. Live:
# I2-I6 (5 cards); not touched (audited: slovenian-live-faults-2018-2024.json).
# Paper (rendered PDF pp2-4; the booklet prints "2"/"3" on PDF pp3/4): the rule
# "Pazljivo preberite ... odgovori, ki morajo biti v slovenskem jeziku, ..."
# (p2 y95-124); the text "Julijske Alpe med prestižnimi imeni" runs p2 y154 to
# its byline "(Prirejeno po: Brane Maselj , Nedelo, ...)" p3 y731 (paragraphs
# 1-10); p4 prints only the questions. Part heads: "1. DE" (sic: the paper
# prints "DE", rendered p4 y65) "(30 točk)"; "2. DEL" "(30 točk)" (p4 y461);
# "3. DEL" "(40 točk)" (p4 y565).
# PRICES:
# - Q1: the paper prints ONE price, "(5 točk)", at the right of Q1's stem line
#   (p4 y87, rendered: bold, same line as "S svojimi besedami (na podlagi
#   teksta) pojasnite naslednje pojme:"). The bracketed numbers after the five
#   expressions, a) "(3)" b) "(9)" c) "(3)" d) "(2)" e) "(4)", are PARAGRAPH
#   numbers of the text, not marks: they add to 21, not 5, and each names the
#   paragraph that prints the word (gneče, para 3; razvoja, para 9; muzej
#   čebelarstva, para 3; družabnih omrežjih, para 2; kulturno dediščino, para
#   4; rendered pp2-3). The census reads them as tariffs (see CENSUS). Q1 is
#   priced only as a whole and the scheme answers each expression: carded
#   whole at the parent key, R('I1', 5 shown rows, whole=True), at the paper's
#   5 (PY(4, 87): the cell "(5 točk)"), as Romanian 2010-2019. The scheme
#   prints the same "(5 točk)" (line 138).
# - II1: the part head's "(30 točk)" (PARTP). The SCHEME heads the part "2. DEL
#   (40 točk)" (line 212, rendered scheme p7): paper and scheme disagree; the
#   paper's 30 stands and the scheme's head is quoted on the card (10f).
# - III1/III2: the part head's "(40 točk)" (PARTP); the scheme the same (237).
# WHAT THE SCHEME PRINTS (rendered scheme pp5-8):
# - Q1 (137-152): the stem with "(5 točk)", then each expression reprinted in
#   the scheme's own words, "a) Razložite besedo »gneča«. (3)" (139, 142, 145,
#   147, 150, bold-less, with the paragraph numbers), each over ONE italic gloss
#   paragraph: a) 140-141, b) 143-144, c) 146, d) 148-149, e) 151-152. Letters
#   agree with the paper's (same five words, same order).
# - Part II (212-215 reprint the head and the task): "Na primer:" (216, plain)
#   over FIVE dash paragraphs of indicative content, 217-221, 222-224, 225-226,
#   227-229, 230-232 (italic, each opening "- "), no per-point marks, no
#   criteria.
# - Part III (237-245): the head, the instruction and both titles reprinted;
#   nothing under them (rendered scheme p8 is otherwise blank; pp9-10 blank).
#   No criteria for any part anywhere in this scheme.
# SHAPES:
# - I1: whole at the parent key, one shown row per expression (the gloss),
#   each row led by the paper's expression (cut inside its printed quotation
#   marks: "For “gneča”"); questionTotal at the paper's 5.
# - II1: the five dash paragraphs shown, whole=True on the paper's 30 (10a:
#   indicative content under the scheme's own heading "Na primer:", quoted in
#   the rownote, never in a row), plus the scheme's "(40 točk)" head quoted.
# - III1/III2: R4 (unprinted) at the paper's 40, the note saying what the
#   scheme prints.
# JUDGEMENT CALLS:
# - I1 question: the stem and the five expression lines as printed, one per
#   line, KEEPING each expression's paragraph number ("a) »gneča« (3)"): it is
#   printed words, not a price (QL would strip a bare "(3)" at a line end as a
#   tariff). If the lead prefers the QL shape, use
#   QL(4, 'S svojimi besedami (na podlagi teksta)', 'a) »gneča«', 'b) ”razvoj«',
#   'c) “čebelarstvo”', 'd) ”družabno', 'e) ”kulturna').
# - I1: the scheme rewords each expression line ("Razložite besedo ..."): the
#   paper's words stand, the scheme's five reprints quoted (10f), cut before
#   their paragraph numbers.
# - I1a's gloss carries a usage example in the same paragraph ("Pred novo
#   trgovino je bila velika gneča, ..."): one printed paragraph, kept whole.
# - II1's question: the census text with its "(30 točk)" taken out
#   (clean_question): "Na podlagi prebranega besedila komentirajte naslednjo
#   misel (minimalno 100 besed). ”Izkušnje ... spremenijo sistem.”" as printed.
# - III1: the scheme reprints title 1 as "... prekletstvo današnje ekonomije."
#   where the paper prints "... prekletstvo razvijajoče se ekonomije.": the
#   paper wins on the question, the scheme's words quoted (10f). Title 2: the
#   scheme's "” Ali" differs by a space only, not quoted.
# - Reading text: PDF pp2-3 (rendered). The live I2-I6 cards carry pages [4]
#   (the questions page): flagged (class P).
# GLYPHS: none. The text layers of paper and scheme carry č š ž as drawn
#   (checked against the renders); no stray code points.


def _q1_2018(d, _q):
    """The stem and the five expression lines as printed (each with its
    paragraph number)."""
    stem = clean_question(PL(4, 'S svojimi besedami (na podlagi teksta)').text(d))
    items = [PL(4, o).text(d) for o in ('a) »gneča«', 'b) ”razvoj«', 'c) “čebelarstvo”', 'd) ”družabno',
                                        'e) ”kulturna')]
    return '\n'.join([stem] + items)


def _reprints_2018(d):
    return ('The scheme reprints the five expressions as '
            + '; '.join(f'“{S(n, after=f"{l}) ", before=f" ({p})").text(d)}”'
                        for n, l, p in ((139, 'a', 3), (142, 'b', 9), (145, 'c', 3), (147, 'd', 2), (150, 'e', 4)))
            + '.')


def _part2_head_2018(d):
    return (f'The scheme heads this part “{S(212).text(d)}”; the paper prints “{PY(4, 461).read(d)[2]}” on the '
            f'part\'s head, and the paper\'s price stands.')


def _essay_2018(d):
    return ('The scheme reprints the part\'s head, the instruction and the two titles, and prints nothing '
            'under them: no answer, no criteria and no split of the part\'s marks.')


ESSAY_2018 = 'Napišite esej'
SPECS[2018] = [
    R('I1', [shown(L(140, 141), lead=PC(4, 'a) »gneča«', after='a) »', before='« (3)')),
             shown(L(143, 144), lead=PC(4, 'b) ”razvoj«', after='b) ”', before='« (9)')),
             shown(S(146), lead=PC(4, 'c) “čebelarstvo”', after='c) “', before='” (3)')),
             shown(L(148, 149), lead=PC(4, 'd) ”družabno', after='d) ”', before='« (2)')),
             shown(L(151, 152), lead=PC(4, 'e) ”kulturna', after='e) ”', before='” (4)'))],
      whole=True, total=PY(4, 87), question=_q1_2018, rownote=_reprints_2018, pages=(2, 3)),
    R('II1', [shown(L(217, 221)), shown(L(222, 224)), shown(L(225, 226)), shown(L(227, 229)),
              shown(L(230, 232))], whole=True,
      rownote=both(quote(S(216), lead='The scheme heads its points'), _part2_head_2018), pages=(2, 3)),
    R('III1', [unprinted(both(_essay_2018,
                              quote(S(239, after='1. '), lead='It reprints this title as')))],
      question=QP(4, ESSAY_2018, '1. ”Mediji', Run('Prosimo, izrazite', 'uporabe družbenih'))),
    R('III2', [unprinted(_essay_2018)],
      question=QP(4, ESSAY_2018, '2. ”Ali obleka', Run('Do katere mere', 'besedami.'))),
]


# ====================================================================== 2019
# ================================================================ 2019 HL ===
# Drafted (small-languages lane, 20 Nov): every ask of this sitting, I1a-e,
# I2-I6, II1, III1, III2 (13 cards). No live card in this sitting.
# Paper (rendered PDF pp2-4; the booklet's page numbers agree with the PDF's):
# the rule "Pazljivo preberite ... odgovori, ki morajo biti v slovenskem
# jeziku, ..." (p2 y80-109); the text "Volite Ivana Cankarja!" runs p2 y146 to
# its byline "(Prirejeno po: Peter Kolšek, Delo, 28. april 2018.)" p3 y576
# (paragraphs 1-9). Part heads: "1. DEL" "(30 točk)" (p3 y619); "2. DEL"
# "(30 točk)" (p4 y446); "3. DEL" "(40 točk)" (p4 y592).
# PRICES:
# - Part I: the paper prints NO mark for any ask of the part, only the part's
#   "(30 točk)" (rendered p3 y619): Q1 "1. S svojimi besedami ... pojme:" over
#   a)-e) (p3 y649-756) and Q2-Q6 (p4 y109-358) carry no bracketed or worded
#   number at all (rendered p3, p4: the right margin is empty beside every
#   ask). The scheme prints none either: its "1. DEL (30 točk)" (line 46) and
#   nothing beside Q1 or any letter or Q2-Q6 (rendered scheme pp3-4).
#   Ten unpriced asks sharing the part's printed 30: CARD-STANDARD 10i, never
#   split. Each its own card, the scheme's answer as shown rows with no marks,
#   unpricedSection = the part's printed name "1. DEL" and its 30
#   (Unpriced(PL(3, '1. DEL'), PARTP())). Not REM (ten asks, not one).
# - II1: the part head's "(30 točk)" (PARTP); the scheme the same (113).
# - III1/III2: the part head's "(40 točk)" (PARTP); the scheme the same (128).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5):
# - Q1 (47-60): the stem, then each expression reprinted in the scheme's own
#   words, bold ("a) Razložite besedo ”šotor”." 48, 51, 53, 56, 59), each over
#   its italic gloss: a) 49-50, b) 52, c) 54-55, d) TWO glosses, one per word
#   of the phrase, "Domiseln: ..." (57) and "Pikanten: ..." (58), e) 60. Letters
#   and words agree with the paper's.
# - Q2 (63 reprint): the bold heading "Odgovor je možno najti v 2., 3. in 4.
#   odstavku:" (64), three italic lines, each starting at the margin, each a
#   sentence of the text (65-66, 67-68, 69-70), then "Npr: Enajstega decembra
#   ... Ivana Cankarja." (71) after a gap.
# - Q3 (76-77 reprint): italic heading "Odgovor je možno najti v 2. in 3.
#   odstavku." (78), one paragraph 79-80.
# - Q4 (81-82 reprint): italic heading "Odgovor je možno najti v odstavku 2, 3,
#   4 in 5." (83), one italic paragraph 84-89 and a plain line "Slovenci še
#   vedno nimamo filma o Cankarju." (90) on a line of its own.
# - Q5 (91-92 reprint): italic heading "Možni odgovori:" (93), one list of
#   themes (94-95).
# - Q6 (96-98 reprint): three paragraphs, 99-104, 105-106, 107-108 (each opens
#   at the margin after a line that ends short).
# - Part II (113-116 reprint the head and the task): ONE model paragraph
#   (117-127, italic), no heading, no criteria.
# - Part III (128-136): the head, "Napišite esej (minimalno 300 besed)." and
#   both titles reprinted; nothing under them (rendered scheme p5; pp6-7 blank).
#   No criteria for any part anywhere in this scheme.
# SHAPES:
# - I1a-e, I2-I6: 10i (Unpriced), one shown row per printed gloss, line or
#   paragraph; each heading ("Odgovor je možno najti ...", "Možni odgovori:",
#   "Npr:") quoted in the rownote, never in a row.
# - II1: the model paragraph shown, whole=True on the paper's 30 (10a).
# - III1/III2: R4 (unprinted) at the paper's 40, the note saying what the
#   scheme prints.
# JUDGEMENT CALLS:
# - Q1 per letter (10i), not whole at 'I1': no price is printed for Q1 at all
#   (neither per expression nor for the question), so the Romanian whole-Q1
#   shape (one printed price over a-e) does not apply; each letter is its own
#   printed ask with its own gloss.
# - I1d: two shown rows, the scheme's two glosses, each kept with its printed
#   headword ("Domiseln:", "Pikanten:"): the headword names which word the
#   gloss explains; it is not a heading over the answer.
# - Q1: the scheme rewords each expression line ("Razložite besedo ...", lower
#   case): the paper's words stand, the scheme's reprint quoted (10f).
# - Q2: the last line's "Npr:" is a heading (quoted in the rownote); the row
#   is cut after it. The three passage sentences are three printed lines, each
#   opening at the margin: three rows.
# - Q4: line 87 prints "(5)" inside the answer ("... status narodnega junaka
#   (5)."): a paragraph number, lifted as printed.
# - Q5: one shown row (one printed list), not split at the commas.
# - II1, III1, III2: questions cut from the paper's own lines (the census glues
#   "(30 točk)" in front of II1 and "ali" after III1). III1 keeps the printed
#   attribution "(Ivan Cankar)".
# - Part III: the scheme's instruction omits the paper's "Izberite enega
#   izmed danih naslovov.": not a title, not quoted.
# - Reading text: PDF pp2-3 (rendered); no live cards in this sitting.
# GLYPHS: none. č š ž read as drawn in both text layers (checked on the
#   renders); no stray code points.

U1_2019 = Unpriced(PL(3, '1. DEL'), PARTP())


def _reprint_2019(n, letter):
    return quote(S(n, after=f'{letter}) '), lead='The scheme reprints this expression as')


def _q2_2019(d):
    return (f'The scheme heads its answer “{S(64).text(d)}” and sets its last line under '
            f'“{S(71, before=" Enajstega").text(d)}”.')


def _essay_2019(d):
    return ('The scheme reprints the part\'s head, the instruction and the two titles, and prints nothing '
            'under them: no answer, no criteria and no split of the part\'s marks.')


ESSAY_2019 = 'Napišite esej'
SPECS[2019] = [
    R('I1a', [shown(L(49, 50))], unpriced=U1_2019, rownote=_reprint_2019(48, 'a'), pages=(2, 3)),
    R('I1b', [shown(S(52))], unpriced=U1_2019, rownote=_reprint_2019(51, 'b'), pages=(2, 3)),
    R('I1c', [shown(L(54, 55))], unpriced=U1_2019, rownote=_reprint_2019(53, 'c'), pages=(2, 3)),
    R('I1d', [shown(S(57)), shown(S(58))], unpriced=U1_2019, rownote=_reprint_2019(56, 'd'), pages=(2, 3)),
    R('I1e', [shown(S(60))], unpriced=U1_2019, rownote=_reprint_2019(59, 'e'), pages=(2, 3)),
    R('I2', [shown(L(65, 66)), shown(L(67, 68)), shown(L(69, 70)), shown(S(71, after='Npr: '))],
      unpriced=U1_2019, rownote=_q2_2019, pages=(2, 3)),
    R('I3', [shown(L(79, 80))], unpriced=U1_2019,
      rownote=quote(S(78), lead='The scheme heads its answer'), pages=(2, 3)),
    R('I4', [shown(L(84, 89)), shown(S(90))], unpriced=U1_2019,
      rownote=quote(S(83), lead='The scheme heads its answer'), pages=(2, 3)),
    R('I5', [shown(L(94, 95))], unpriced=U1_2019,
      rownote=quote(S(93), lead='The scheme heads its answer'), pages=(2, 3)),
    R('I6', [shown(L(99, 104)), shown(L(105, 106)), shown(L(107, 108))], unpriced=U1_2019, pages=(2, 3)),
    R('II1', [shown(L(117, 127))], whole=True,
      question=QP(4, 'Na podlagi prebranega', Run('”Prvo je', 'se sprehajajo')), pages=(2, 3)),
    R('III1', [unprinted(_essay_2019)],
      question=QP(4, ESSAY_2019, Run('1. ”Če kdaj', 'se strnemo'), '(Ivan Cankar)')),
    R('III2', [unprinted(_essay_2019)],
      question=QP(4, ESSAY_2019, '2. Kakšna', 'Prosimo, argumentirajte')),
]


# ====================================================================== 2022
# ================================================================ 2022 HL ===
# The SEC published no marking scheme for 2022 (SOURCES.md; nothing under
# examiner-reports/slovenian/schemes/ for 2022). Every open ask is carded with
# the paper's own price and the fixed line NO_SCHEME_PUBLISHED, unscored (R4;
# the lead's Danish 2010 shape). Drafted (small-languages lane, 20 Nov): I1a-e,
# I2-I6, II1 (11 cards). No live card in this sitting.
# Paper (rendered PDF pp2-4; the booklet's page numbers agree with the PDF's):
# a TWO-part sitting. "Odgovorite na vprašanja v obeh delih." / "Vsi odgovori
# morajo biti v slovenščini." / "(Največ 70 točk)" (p2 y65-112); "1. DEL" "(30
# točk)" (p2 y152); the text "V hribe k sebi (in zase)" runs p2 y230 to its
# source line "(Prirejeno po: Andreja Frankovič, https://www.mladinska-knjiga.si
# ..., julij 2019)" p3 y624; Q1 on p3 y661-773, Q2-Q6 on p4; "2. DEL" "(40
# točk)" (p4 y461), the essay: "Napišite esej (minimalno 300 besed). Izberite
# enega izmed danih naslovov." (p4 y532), title 1 "»Turizem – blagoslov ali
# prekletstvo?«" with its prompt "Ali se vam zdi ... v njeni lepoti?" (p4
# y580-609), "ALI" (p4 y646), title 2 "Kako se razvije pravo prijateljstvo."
# (p4 y690). Neither title is numbered.
# PRICES:
# - I1a-e: the paper prints "(5 × 1 )" as a cell at the right of e)'s line (p3
#   y773, rendered): ONE MARK FOR EACH EXPRESSION. Carded per letter at 1. The
#   reader: PaperP and PY read only a worded price or a single bracketed number,
#   and PP()'s notation is the census's own description ("(5 × 1 ) on the head
#   of Q1, walked down to its 5 parts"), which NoScheme's note would quote as if
#   printed. _per_each(3, 773) reads the printed cell "(5 × 1 )" at (p3, y773)
#   and returns its per-expression 1 with the cell as printed (see JUDGEMENT).
# - I2-I6: "(5)" at the right of each question's last line (p4 y126, 189, 252,
#   315, 395): PP() (the census reads each).
# - II1 (the essay): the part head's "(40 točk)" (PARTP).
# SHAPES: NoScheme for every ask; Part I with pages=(2, 3). II1 is the essay of
# a two-part sitting (filed as Part III; no reading text attached).
# JUDGEMENT CALLS:
# - Q1 per letter at 1 (the paper prints a mark per expression), not whole at
#   'I1'.
# - _per_each is a draft-local price reader (eight lines, below). If the lead
#   prefers sl_lib names only, drop total= on the five Q1 specs: PP() reads the
#   same 1, and the NoScheme note then quotes the census's description.
# - II1: the census keys ONE ask over both titles (its text runs "»Turizem ...
#   lepoti? ALI Kako se razvije pravo prijateljstvo."). The two titles are two
#   printed asks (the 2023 paper of the same design numbers them 1./2. and the
#   census keys III1/III2): II1 is carded with the paper's FIRST title only
#   (instruction + "»Turizem – blagoslov ali prekletstvo?«" + its prompt);
#   title 2 (p4 y690) has no census key and is reported under CENSUS, not
#   drafted around. If the lead keys the part as one ask instead, use the
#   census question (drop question=).
# - I6: the census question reads as printed ("»Ne osvojimo gore, pač pa sami
#   sebe.« Na podlagi besedila, ..."): the quotation opens the question on
#   the paper (p4 y379).
# - Reading text: PDF pp2-3 (rendered).
# GLYPHS: none. The text layer carries č š ž as drawn; "‐" (U+2010) in the
#   source line and in "družbeno‐ekonomskih"/"60‐letnici" is the SEC's own
#   hyphen character (drawn as a hyphen), not a mangled letter.
import re  # noqa: E402


class _PerEach:
    """The per-expression mark of a printed "(N × M )" cell on the question
    paper at (page, y): M marks for each of N expressions."""
    def __init__(self, page, y):
        self.page, self.y = page, y

    def read(self, doc):
        cell = re.compile(r'^\(\s*(\d{1,2})\s*[×x]\s*(\d{1,2})\s*\)$')
        hits = [l for l in doc['lines'] if l.page == self.page and abs(l.y - self.y) < 2
                and cell.match(l.text.strip())]
        if len(hits) != 1:
            raise ValueError(f'paper p{self.page} y{self.y}: {len(hits)} "(N × M)" cells')
        m = cell.match(hits[0].text.strip())
        return 1, int(m.group(2)), hits[0].text.strip()


def _per_each(page, y):
    return _PerEach(page, y)


Q1P_2022 = _per_each(3, 773)
SPECS[2022] = [
    NoScheme('I1a', total=Q1P_2022, pages=(2, 3)),
    NoScheme('I1b', total=Q1P_2022, pages=(2, 3)),
    NoScheme('I1c', total=Q1P_2022, pages=(2, 3)),
    NoScheme('I1d', total=Q1P_2022, pages=(2, 3)),
    NoScheme('I1e', total=Q1P_2022, pages=(2, 3)),
    NoScheme('I2', pages=(2, 3)),
    NoScheme('I3', pages=(2, 3)),
    NoScheme('I4', pages=(2, 3)),
    NoScheme('I5', pages=(2, 3)),
    NoScheme('I6', pages=(2, 3)),
    NoScheme('II1', total=PARTP(),
             question=QP(4, 'Napišite esej', '»Turizem', Run('Ali se vam zdi', 'za to, da mi'))),
    # Title 2 (census ADDED_ASKS: printed on its own line after "ALI", p4 y690; the walker kept no ask for it)
    NoScheme('II2', total=PARTP(), question=QP(4, 'Napišite esej', 'Kako se razvije pravo')),
]


# ====================================================================== 2023
# ================================================================ 2023 HL ===
# Drafted (small-languages lane, 20 Nov): the four open asks of this sitting,
# I1e, II1, III1, III2. Live: I1a-d, I2-I6 (9 cards); not touched (audited:
# slovenian-live-faults-2018-2024.json).
# Paper (rendered PDF pp2-4; the booklet's page numbers agree with the PDF's):
# "Odgovorite na vprašanja v vseh delih." / "Vsi odgovori morajo biti v
# slovenščini." "(Največ 100 točk)" (p2 y65-97); "1. DEL" "(30 točk)" (p2
# y136); the text "Rastline v ljudski medicini na Slovenskem" runs p2 y176 to
# its notes and source "(Prirejeno po: Vlasta Mlakar, ... pridobljeno septembra
# 2022)" p3 y705-718; p4 prints only the questions: Q1 a)-e) with "(5 × 1)" at
# the right of e)'s line (p4 y152); Q2-Q6 "(5)" each; "2. DEL" "(30 točk)" (p4
# y489); "3. DEL" "(40 točk)" (p4 y588), titles "1." and "2." joined by "ALI".
# PRICES:
# - I1e: "(5 × 1)" = one mark for each expression (p4 y152): 1 (PP(); the census
#   walks the cell down to each letter, as for the live a-d). The scheme prints
#   the same "(5 × 1)" under e) (line 136).
# - II1: the part head's "(30 točk)" (PARTP); the scheme the same (184).
# - III1/III2: the part head's "(40 točk)" (PARTP); the scheme the same (201).
# WHAT THE SCHEME PRINTS (rendered scheme pp5-7):
# - Q1 (130-136): each expression as the paper prints it, then " – " and its
#   gloss on the same line; e) "“Ustno izročilo”.  – Kar se z ustnim
#   sporočanjem širi in ohranja iz roda v rod." (135).
# - Part II (184-186 reprint the head and the task): "Na primer:" (187,
#   underlined), then THREE paragraphs of model commentary: 188-189 ("Ljudje že
#   od nekdaj ... kvalitetno življenje.", p4, last line short), 194-197 ("V
#   preteklosti ... oblike zdravljenja.", p5), 198-200 ("Vse to pa izhaja ...
#   in stresom.", opening at the margin after the short "zdravljenja.").
# - Part III (201-208): the head, the instruction and both titles reprinted
#   (without their "1."/"2."), "ALI" between; nothing under them (rendered
#   scheme p7; pp8-9 blank). No criteria for any part anywhere in this scheme.
# SHAPES:
# - I1e: one(gloss, PP()) at the paper's 1 (one stated answer).
# - II1: the three paragraphs shown, whole=True on the paper's 30 (10a), the
#   scheme's heading "Na primer:" quoted in the rownote.
# - III1/III2: R4 (unprinted) at the paper's 40.
# JUDGEMENT CALLS:
# - I1e question: the census text runs on into the instruction printed under
#   Q1 ("“Ustno izročilo”. S svojimi besedami odgovorite na naslednja
#   vprašanja; ...") and lacks Q1's stem (see CENSUS). Cut from the paper's own
#   lines: QP(4, '1. S svojimi', 'e) “Ustno'), the live a-d's form ("S svojimi
#   besedami ... pojme: “Zdravnik”."). Its conceptId is still derived from the
#   census's welded text (sl_lib reads ask.text); concept='question' would give
#   the stem's words instead. Left to the lead (fixing the census text fixes
#   both).
# - II1: three rows, not one: the scheme sets three paragraphs (rendered).
# - III1/III2: questions cut from the paper's lines (the census leaves "ALI"
#   on III1). III2's attribution "(N. Zaplotnik)" is joined to its title by
#   Run: as a line of its own QP would take "(N." for a part marker and cut it.
#   Titles reprinted as printed (bar the numbers): nothing quoted.
# - Reading text: PDF pp2-3 (rendered), including the two footnotes
#   ("*bukovnik", "**manifestacija") under the text on p3. The live cards'
#   pages [2, 3] agree.
# GLYPHS: none. The scheme's text layer sets its words in no-break spaces
#   (U+00A0, read as spaces by S()); "‐" (U+2010) in "kultno‐magične",
#   "(100‐150 besed)" is the SEC's own hyphen character. č š ž read as drawn.

def _essay_2023(d):
    return ('The scheme reprints the part\'s head, the instruction and the two titles, and prints nothing '
            'under them: no answer, no criteria and no split of the part\'s marks.')


ESSAY_2023 = 'Napišite esej'
SPECS[2023] = [
    # conceptId from the printed question (the census welds the instruction under Q1 onto e)'s text)
    R('I1e', [one(S(135, after='– '), PP())], question=QP(4, '1. S svojimi', 'e) “Ustno'), pages=(2, 3),
      concept='question'),
    R('II1', [shown(L(188, 189)), shown(L(194, 197)), shown(L(198, 200))], whole=True,
      rownote=quote(S(187), lead='The scheme heads its answer'), pages=(2, 3)),
    R('III1', [unprinted(_essay_2023)],
      question=QP(4, ESSAY_2023, Run('1. »Zdrav duh', 'načinu življenja?'))),
    R('III2', [unprinted(_essay_2023)],
      question=QP(4, ESSAY_2023, Run('2. »Kdor išče', '(N. Zaplotnik)'))),
]


# ====================================================================== 2024
# ================================================================ 2024 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# I1e, II1, III1. Live: I1a-d, I2-I6 (9 cards); not touched (audited:
# slovenian-live-faults-2018-2024.json).
# Paper (rendered PDF pp2-4; the booklet's page numbers agree with the PDF's):
# "Odgovorite na vprašanja v vseh delih. Vsi odgovori morajo biti v
# slovenščini. (Največ 100 točk)" (p2 y65); "1. DEL" "(30 točk)" (p2 y94); the
# text "Pitje kave po slovensko" runs p2 y128 to its sources "(Prirejeno po:
# https://www.delo.si/... pridobljeno septembra 2023)" p3 y489-545; Q1 on p3
# y602-718, "(5 × 1)" at the right of e)'s line (p3 y718); Q2-Q6 "(5)" each
# (p4); "2. DEL" "(30 točk)" (p4 y459); "3. DEL" "(40 točk)" (p4 y587), two
# UNNUMBERED titles joined by "ALI" (p4 y652-740).
# PRICES:
# - I1e: "(5 × 1)" = one mark for each expression (p3 y718): 1 (PP(); the census
#   walks the cell down to each letter). The scheme prints "(5x1)" (line 135).
# - II1: the part head's "(30 točk)" (PARTP); the scheme the same (188).
# - III1: the part head's "(40 točk)" (PARTP); the scheme the same (204).
# WHAT THE SCHEME PRINTS (rendered scheme pp5-7):
# - Q1 (128-135): the five expressions in ANOTHER ORDER than the paper's:
#   scheme a) “Kavopivec” b) “Žvečiti” c) “Pašnik” d) “Geografska lega” e)
#   “Odtegnitveni simptomi” (paper a) Pašnik, b) Žvečiti, c) Kavopivec, d), e)
#   the same). Each gloss follows its expression on the same line; e) runs
#   133-134. Paired by WORDS: e) is e) on both.
# - Part II (188-190 reprint the head and the task): "Na primer:" (191,
#   italic, p6 foot), then ONE model paragraph (196-203, p7).
# - Part III (204-211): the head, the instruction and both titles reprinted,
#   "ALI" between; nothing under them (rendered scheme p7; pp8-9 blank). No
#   criteria for any part anywhere in this scheme.
# SHAPES:
# - I1e: one(gloss, PP()) at the paper's 1, the gloss cut after the scheme's
#   reprint of the expression.
# - II1: the model paragraph shown, whole=True on the paper's 30 (10a), the
#   heading "Na primer:" quoted in the rownote.
# - III1: R4 (unprinted) at the paper's 40.
# JUDGEMENT CALLS:
# - III1: the census keys ONE ask over both titles (its text runs "»Socializacija
#   ... pri srcu? ALI »Vsak človek je enkratna stvaritev.« (P. Bibič)"). The two
#   titles are two printed asks (2023 numbers them 1./2. and the census keys
#   III1/III2): III1 is carded with the paper's FIRST title only; title 2
#   (p4 y740) has no census key and is reported under CENSUS, not drafted
#   around. If the lead keys the part as one ask, drop question= (the census
#   text, its "(40 točk)" taken out).
# - Q1 order: the scheme's re-lettering is the cause of the live a/c swap (see
#   the live audit); e) is unaffected.
# - Reading text: PDF pp2-3 (rendered). The live cards' pages [2, 3] agree.
# GLYPHS: none. The scheme's text layer sets its words in no-break spaces
#   (U+00A0, read as spaces by S()); "‐" (U+2010) in the source URLs is the
#   SEC's own hyphen character. č š ž read as drawn.

def _essay_2024(d):
    return ('The scheme reprints the part\'s head, the instruction and the two titles, and prints nothing '
            'under them: no answer, no criteria and no split of the part\'s marks.')


SPECS[2024] = [
    R('I1e', [one(L(133, 134, after='“Odtegnitveni simptomi”. '), PP())], pages=(2, 3)),
    R('II1', [shown(L(196, 203))], whole=True,
      rownote=quote(S(191), lead='The scheme heads its answer'), pages=(2, 3)),
    R('III1', [unprinted(_essay_2024)],
      question=QP(4, 'Napišite esej', Run('»Socializacija', 'družino'))),
    # Title 2 (census ADDED_ASKS: printed on its own line after "ALI", p4 y740; the walker kept no ask for it)
    R('III2', [unprinted(_essay_2024)], question=QP(4, 'Napišite esej', '»Vsak človek')),
]
