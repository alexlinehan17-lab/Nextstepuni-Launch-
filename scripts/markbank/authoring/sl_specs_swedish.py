#!/usr/bin/env python3
"""Reviewed specs for the Swedish classic examination (small-languages lane).

One entry per printed ask with no live card; see sl_lib.py for the selector
language. Line numbers are lines of examiner-reports/swedish/schemes/<year>-hl.md.
Drafted by Opus helpers on the Bulgarian, Romanian, Dutch and Maltese models, integrated
and gated by the lane lead.
"""
from sl_lib import (R, S, SR, J, L, PL, PC, QP, QL, Run, pre, prerun, PP, SP, PY, RX, PaperP, PARTP, REM,  # noqa: F401
                    one, shown, graded, crit, examples, quote, unprinted, part, NoScheme, Unpriced)
from pl_listen_lib import Join  # noqa: F401
from sl_lib import paper_run, MARKER, clean_question, PRICE_WORD  # noqa: F401,E402
_MARKER, _clean = MARKER, clean_question  # (names the 2013 draft imported)

SPECS = {}


def both(*notes):
    """Several printed notes on one row, in order."""
    return lambda doc: ' '.join(n(doc) for n in notes)


def specs(year):
    return SPECS.get(year, [])


# ====================================================================== 2010
# ====================================================================== 2010
# ================================================================ 2010 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I1, I2, I3, I4, I5, I6, II1, III1. No live card (the old reader excluded the
# whole sitting: "the scheme prices no ask at the address the paper prints").
# Paper (rendered pp2-4): the rule "Läs texten noga ... Alla svar måste vara
# skrivna på svenska." (p2 y103-117); the article "Är målet i livet att hitta
# en partner?" runs pp2-3 (title p2 y157, source "Dagens Nyheter den 9 februari
# 2009" y176, paragraphs 1-8 to the byline "Thomas Lerner" p3 y492); "Del I" +
# "(Totalt 30)" (p3 y547); Q1 "1. Ersätt ordet med ett annat som betyder samma
# sak." + "(5*1 poäng)" (y575, the price a cell at x436), then five UNLETTERED
# bullets "• livslånga (stycke 2)" ... "• värker (stycke 8)" (y603-661); Q2 two
# lines, "(3+2 poäng)" at the end of the second (y703); Q3 "(5 poäng)" (p3
# y745); Q4-Q6 on p4, "(5 poäng)" each; "Del II" + "(30 poäng)" (p4 y292);
# "Del III" + "(40 poäng)" (p4 y437), the instruction (y465-479) and two
# UNNUMBERED titles, "Förväntar vi oss för mycket av livet nu för tiden?"
# (y520) / "eller" (y548, bold) / "Ingen människa är en ö" (y578).
# CENSUS (for the lead): the census keys Part III as ONE ask, III1, whose text
# runs both titles together ("... nu för tiden? eller Ingen människa är en ö").
# The paper prints two titles, a choice of one: III2 "Ingen människa är en ö"
# (p4 x54 y578) is MISSED. III1 is carded below on title 1 only; III2 is not
# drafted (no census ask). Once the census adds it, the same spec serves:
# R('III2', [unprinted(_part3_note_2010)], question=QP(4, ESSAY_2010, 'Ingen människa')).
# PRICES:
# - I1: "(5*1 poäng)" on Q1's head (census tariff (5, 1, 5): PP() reads 5). The
#   paper prints a mark PER EXPRESSION (5 x 1): five one() rows at the 1 read
#   from that printed cell (PaperP: "1 poäng"), adding to the card's 5. The
#   census keys Q1 whole (the bullets carry no letter), so the card is the
#   parent key 'I1' (Danish 2015's shape: one card, a row per expression at its
#   printed 1). The scheme prints the same "(5*1 poäng)" (line 16).
# - I2: the census reads no price; the paper PRINTS "(3+2 poäng)" at the end of
#   the question's second line (p3 y703; rendered, right margin). Two
#   expressions, priced 3 and 2 in the order the question names them: "haft
#   ett gott öga till henne" 3, "dyka upp" 2; the card's 5 is the printed
#   terms added (_Split: PaperP's mark-word reader takes only the "2 poäng").
#   The scheme prints the same "(3+2 poäng)" (line 24). Not a remainder, not 10i.
# - I3-I6: "(5 poäng)" each (PP).
# - II1: the part head's "(30 poäng)" (PARTP); scheme "Del II (30 poäng)" (57).
# - III1: the part head's "(40 poäng)" (PARTP); scheme "Del III (40 poäng)" (64).
# WHAT THE SCHEME PRINTS (rendered scheme pp2-3 = printed pages 1-2; p4 a blank
# coloured cover):
# - Q1 (16-22): the instruction reprinted as "Ersätt uttrycket med ett som
#   betyder samma sak." (the paper: "Ersätt ordet med ett annat ..."; quoted,
#   10f), then a)-e), each the expression in bold, its paragraph, and "Rätta
#   svar: ..." in italics on the same line (d) wraps, 20-21). Paired by WORDS:
#   the scheme's a)-e) are the paper's five bullets in order.
# - Q2 (23-27): the question reprinted in other words ("... och uttrycket
#   ”dyka upp” (båda uttryck finns i stycke 8) med ett som betyder samma sak.",
#   quoted, 10f), then one italic line per expression, "Möjliga svar till
#   ”haft ett gott öga till”: gillat, ..." (25) and "Möjliga svar till ”dyka
#   upp”: infinna sig, ..." (26-27).
# - Q3 (28 reprint): one italic paragraph, 29-31, "Möjliga svar, baserade på
#   stycke 7: Förr var en parrelation ...".
# - Q4 (32-34 reprint, reworded: "Vad tror du Kurt numi menar med detta
#   citat?"; quoted, 10f): one italic paragraph, 35-37.
# - Q5 (38-39 reprint): one italic paragraph, 40-43, "Möjliga svar: Just det
#   osäkra ...".
# - Q6 (48-50 reprint, p3): one italic paragraph, 51-56, "Abiturenten bör kunna
#   diskutera ... Ett godkänt svar kännetecknas av djup, ...".
# - Part II (57-61 reprint the head and the task): one italic descriptive line,
#   62-63, "En klart och tydligt skriven uppsats som väl håller sig till ämnet,
#   med tydlig disposition, klart syfte och godtagbara formuleringar."
# - Part III (64-67 reprint the head and both titles, "Eller" between them):
#   the SAME descriptive line once under both titles, 68-69. Nothing per title.
# - Criteria (p3 foot, 70-76): "Anmärkning: I del I och II kommer följande
#   kriterier att vägas in i betygsättningen:" -- for Parts I AND II, not Part
#   III -- then four criteria WITH percentages, "– 30%" (71), "– 30%" (72-73),
#   "– 30%" (74-75), "– 10%" (76): 100 %.
# SHAPES:
# - I1: five one() rows at 1, each led by its paper bullet's word.
# - I2: two one() rows, 3 and 2, each led by its expression as the paper
#   prints it.
# - I3-I6: one printed paragraph each -> one claimable row at 5.
# - II1: graded (10b), 30/30/30/10 % of 30 = 9/9/9/3; head the descriptive line
#   (62-63, Slovakian 2010's shape); the criteria's lead quoted.
# - III1: one generic line printed once under both titles (a descriptive line)
#   and criteria stated for Parts I and II only: R4 (unprinted) at the paper's
#   40, the note quoting both.
# JUDGEMENT CALLS:
# - I2's 3/2 split read in the order the question names the expressions (the
#   scheme answers them in the same order). If the lead reads "(3+2)" as
#   unattached: shown rows, whole=True on the 5.
# - I6 is one claimable row: one printed paragraph (the brief's rule), though
#   it reads as a requirement ("Abiturenten bör kunna diskutera ..."). If the
#   lead prefers self-assessment: shown, whole=True on the 5.
# - Answer labels ("Rätta svar:", "Möjliga svar till ”...”:", "Möjliga svar,
#   baserade på stycke 7:", "Möjliga svar:") are cut off the rows; the Part I
#   heads that say where the answer comes from are quoted on the row.
# - Criteria read as NOT covering Part III ("I del I och II", rendered p3;
#   Bulgarian/Slovakian precedent). Alternative if the lead reads them
#   paper-wide: III1 graded(L(68, 69), PARTP(), CRIT_2010) (12/12/12/4).
# - I1's question: the stem and the five bullet lines, one per line (QL), the
#   bullets kept as printed. I2's: its two printed lines, the "(3+2 poäng)"
#   cut off the second (the census keeps it: clean_question does not read a
#   split price).
# - II1/III1 questions from the paper's own lines (the census glues the part
#   head's "(30 poäng)"/"(40 poäng)" in front and runs III1 into title 2).
# - Reading text pp2-3 (rendered: title p2 y157, the text to the byline p3
#   y492; questions from p3 y547): pages=(2, 3) on Part I and II1.
# GLYPHS: none. å ä ö read cleanly in every line used (paper and scheme;
# "livslånga", "outtömlig", "ängslan", "betygsättningen" checked on the
# render). Printed as such (render), SEC typing, lifted as printed: the
# scheme's "Kurt numi" (33, for the paper's "Kurt Nurmi"), "a) ... eviga," with
# its trailing comma (17).

import re as _re


class _Split:
    """A split price the paper prints in one bracket, "(3+2 poäng)", on the
    printed line on `page` opening with `opening`: term k (0, 1) or, with
    k=None, the printed terms added (the question's total)."""
    def __init__(self, page, opening, k=None):
        self.page, self.opening, self.k = page, opening, k

    def read(self, doc):
        t = PL(self.page, self.opening).text(doc)
        m = _re.search(r'\((\d{1,2})\s*\+\s*(\d{1,2})\s*poäng\)', t)
        if not m:
            raise ValueError(f'paper p{self.page} {self.opening!r} prints no split price: {t!r}')
        terms = [int(m.group(1)), int(m.group(2))]
        return 1, (sum(terms) if self.k is None else terms[self.k]), m.group(0)


def _q(*sels):
    """A question cut from printed paper lines: each line (or cut) in order,
    its own marker taken off, joined by a space."""
    from sl_lib import MARKER, clean_question
    return lambda d, _census=None: clean_question(' '.join(MARKER.sub('', s.text(d), count=1) for s in sels))


def _bullet_2010(opening):
    """The word a Q1 bullet prints before its paragraph reference."""
    return PC(3, opening, after='• ', before=' (stycke')


REPRINT = 'The scheme reprints this question as'
Q1P_2010 = PaperP(3, '(5*1 poäng)')
Q2_2010 = 'och ”dyka upp”'
CRIT_2010 = crit(71, (72, 73), (74, 75), 76)
LEAD_2010 = quote(S(70, after='Anmärkning: '), lead='The scheme prints')
ESSAY_2010 = Run('Skriv en uppsats på ungefär 300', 'ämnena nedan.')


def _part3_note_2010(d):
    # (second reader: the criteria block is printed under the titles too, so not "only")
    return (f'Under the two titles the scheme prints “{L(68, 69).text(d)}” and its criteria note, which names '
            f'parts I and II only: “{S(70, after="Anmärkning: ").text(d)}” It prints no answer for this part.')


SPECS[2010] = [
    R('I1', [one(S(17, after='Rätta svar: '), Q1P_2010, lead=_bullet_2010('• livslånga')),
             one(S(18, after='Rätta svar: '), Q1P_2010, lead=_bullet_2010('• outtömlig')),
             one(S(19, after='Rätta svar: '), Q1P_2010, lead=_bullet_2010('• oron')),
             one(L(20, 21, after='Rätta svar: '), Q1P_2010, lead=_bullet_2010('• grubbla')),
             one(S(22, after='Rätta svar: '), Q1P_2010, lead=_bullet_2010('• värker'))],
      rownote=quote(S(16, before=' (5*1'), lead='The scheme reprints the instruction as'),
      question=QL(3, '1. Ersätt ordet med ett annat', '• livslånga', '• outtömlig', '• oron', '• grubbla',
                  '• värker'),
      pages=(2, 3)),
    R('I2', [one(S(25, after='”: '), _Split(3, Q2_2010, 0),
                 lead=PC(3, '2. Ersätt uttrycket', after='uttrycket ”', before='”')),
             one(L(26, 27, after='”: '), _Split(3, Q2_2010, 1), lead=PC(3, Q2_2010, after='och ”', before='”'))],
      total=_Split(3, Q2_2010),
      rownote=quote(L(23, 24, after='2. ', before=' (3+2'), lead=REPRINT),
      question=_q(PL(3, '2. Ersätt uttrycket'), PC(3, Q2_2010, before=' (3+2')), pages=(2, 3)),
    R('I3', [one(L(29, 31, after='stycke 7: '), PP())],
      rownote=quote(S(29, before=' Förr'), lead='The scheme heads its answer'), pages=(2, 3)),
    R('I4', [one(L(35, 37, after='stycke 7: '), PP())],
      rownote=both(quote(L(32, 33, after='4. '), lead=REPRINT),
                   quote(S(35, before=' de högt'), lead='It heads its answer')), pages=(2, 3)),
    R('I5', [one(L(40, 43, after='Möjliga svar: '), PP())], pages=(2, 3)),
    R('I6', [one(L(51, 56), PP())], pages=(2, 3)),
    R('II1', [graded(L(62, 63), PARTP(), CRIT_2010)], rownote=LEAD_2010,
      question=QP(4, Run('”I dag ska förhållandet', 'är det lätt att få'),
                  Run('Skriv en uppsats på ungefär 100', 'hur du ser på')), pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2010)],
      question=QP(4, ESSAY_2010, 'Förväntar vi oss')),
]

# The asks the census missed (paper_census ADDED_ASKS, the lead), from the drafter's ready specs above.
SPECS[2010].append(R('III2', [unprinted(_part3_note_2010)], question=QP(4, ESSAY_2010, 'Ingen människa')))


# ====================================================================== 2011
# ====================================================================== 2011
# ================================================================ 2011 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# I1, II1, III1. Live: I2-I6 (5 cards); not touched (audited: see
# swedish-live-faults-2010-2016.json).
# Paper (rendered pp2-4): the rule "Läs texten noga ... Alla svar måste vara
# skrivna på svenska." (p2 y68-81); the article "Var femte man utan nära vän"
# runs pp2-3 (title p2 y104, paragraphs 1-12 to the source line "Maria Carling
# i Svenska Dagbladet den 21 november 2007" p3 y312); "Del I" + "(Totalt 30)"
# (p3 y351); Q1 (p3 y376-508): "1. Ersätt de understrukna orden med andra som
# betyder samma sak." + "(4+2 poäng)" (a cell at x476), four UNLETTERED word
# lines "Garv (stycke 2)" ... "Driver med (stycke 10)", a second instruction
# "Ersätt de följande understrukna uttrycken med andra som betyder samma sak:"
# (y457), then "”landar man mjukare” (stycke 6)" / "och" / "”när det gäller”
# (stycke 11)"; Q2 "(4 poäng)", Q3-Q6 "(5 poäng)"; "Del II" + "(30 poäng)" (p3
# y725); p4 "Del III" + "(40 poäng)" (y64), the instruction (y96) and two
# UNNUMBERED titles "Hur står sig mediernas skildring av vänskap jämfört med
# verkligheten?" (y121) / "eller" (y147) / "”De flesta människor är ungefär så
# lyckliga som de bestämt sig för att vara.”" (y172) with its attribution line
# "Abraham Lincoln [USA:s 16:e president, 1809-1865]" (y185).
# CENSUS (for the lead): Part III is keyed as ONE ask, III1, whose text runs
# both titles together. The paper prints two titles, a choice of one: III2
# "”De flesta människor är ungefär så lyckliga som de bestämt sig för att
# vara.”" + "Abraham Lincoln [USA:s 16:e president, 1809-1865]" (p4 x50
# y172-185) is MISSED. III1 is carded below on title 1 only. Once the census
# adds III2: R('III2', [unprinted(_part3_note_2011)],
# question=QP(4, ESSAY_2011, '”De flesta', 'Abraham Lincoln')).
# PRICES:
# - I1: the census reads no price; the paper PRINTS "(4+2 poäng)" on Q1's head
#   (p3 x476 y376; rendered, bold): 4 for the four words, 2 for the two
#   expressions, 6 in all (Del I's 30 less Q2's 4 and Q3-Q6's 20). No mark per
#   word or per expression is printed (the scheme prints the same "(4+2
#   poäng)", line 18): Q1 is carded whole at the parent key, its six answers
#   shown, priced as a whole on the printed terms added (_Split), as Romanian
#   2010-2019 card a Q1 priced only on its head.
# - II1: the part head's "(30 poäng)" (PARTP); scheme "Del II (30 poäng)" (85).
# - III1: the part head's "(40 poäng)" (PARTP); scheme "Del III (40 poäng)" (96).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3; pp2, 6-8
# blank):
# - Q1 (18-34): the instruction reprinted as "1. Ersätt ordet med ett annat som
#   betyder samma sak." and the second as "Ersätt följande uttryck med andra
#   som betyder samma sak:" (27) -- both reworded (quoted, 10f); each word or
#   expression on a line of its own with its paragraph and a colon, then "Rätt
#   svar:" (roman) and the accepted alternatives in italics: Garv 20, Bortåt 22,
#   Omhuldande 24, Driver med 26, ”landar man mjukare” 29-30, "och" (31, bold),
#   ”när det gäller” 33-34.
# - Criteria (p5 top, 77-84, between Q6 and Part II): "Anmärkning:" / "I del I
#   och II kommer följande kriterier att vägas in i betygssättningen:" -- for
#   Parts I AND II, not Part III -- then four criteria WITH percentages, "– 30%"
#   (79), "– 30%." (80-81), "– 30%." (82-83), "– 10%." (84): 100 %.
# - Part II (85-87 reprint the head and the task): one italic paragraph,
#   88-95, "Möjliga svar: (stycke 4,5,6)Rubriken antyder att vänner i framtiden
#   ... anföra exempel som stöd för sin tes." No descriptive line.
# - Part III (96-102): the head, the instruction and both titles reprinted
#   (title 2 with "- Abraham Lincoln [...]"), and NOTHING else.
# SHAPES:
# - I1: six shown rows (one per word or expression, each led by it as the
#   paper prints it), whole=True on the paper's 4+2 = 6 (questionTotal).
# - II1: graded (10b), 30/30/30/10 % of 30 = 9/9/9/3; head the criteria's own
#   lead (78; no descriptive line printed for the part, Finnish 2012's shape);
#   the "Möjliga svar:" paragraph quoted as an example, not a checklist (10a).
# - III1: nothing printed for the part and criteria stated for Parts I and II
#   only: R4 (unprinted) at the paper's 40, the note saying so (ruling 4).
# JUDGEMENT CALLS:
# - I1 whole, not one() at 1 each: "(4+2 poäng)" prices the two groups, not
#   each word (four words for 4, two expressions for 2 reads as 1 each, but no
#   1 is printed). If the lead reads it as a per-expression price, the six
#   rows become one(sel, 1) adding to 6 (a reader returning 1 per row would be
#   needed: no 1 is printed to read).
# - The "och" printed between the two expressions (paper p3 y495; scheme 31)
#   is a joiner, not an answer: kept in the question (QL keeps its own line),
#   left out of the rows.
# - "Rätt svar:" (roman; the answers italic, rendered p3) is a label: cut off
#   every row. "(stycke 4,5,6)" in II1's example is set in the paragraph's own
#   italics and stays in the quote as printed.
# - Criteria read as NOT covering Part III ("I del I och II", rendered p5).
#   Alternative if the lead reads them paper-wide: III1 graded(S(78), PARTP(),
#   CRIT_2011) (12/12/12/4).
# - II1's question is the census text (its "(30 poäng)" taken off by
#   clean_question), checked against p3 y745-758; the paper sets "Vänskapen är
#   framtidens relation" in italics.
# - Reading text pp2-3 (rendered: title p2 y104, the text to the source line p3
#   y312; Del I from p3 y351): pages=(2, 3) on I1 and II1. The live 2011 cards
#   carry sourceMaterial.pages [3] (flagged, P).
# GLYPHS: none. å ä ö read cleanly in every line used ("Bortåt", "beskyddande",
# "vårdande", "betygssättningen"; render checked). The scheme's "betygssättningen"
# (78) is printed with a double s (2010 prints "betygsättningen"): as printed.

import re as _re


class _Split:
    """A split price the paper prints in one bracket, "(4+2 poäng)", on the
    printed line on `page` opening with `opening`: term k (0, 1) or, with
    k=None, the printed terms added (the question's total)."""
    def __init__(self, page, opening, k=None):
        self.page, self.opening, self.k = page, opening, k

    def read(self, doc):
        t = PL(self.page, self.opening).text(doc)
        m = _re.search(r'\((\d{1,2})\s*\+\s*(\d{1,2})\s*poäng\)', t)
        if not m:
            raise ValueError(f'paper p{self.page} {self.opening!r} prints no split price: {t!r}')
        terms = [int(m.group(1)), int(m.group(2))]
        return 1, (sum(terms) if self.k is None else terms[self.k]), m.group(0)


def _word_2011(opening):
    """A Q1 word as the paper prints it, before its paragraph reference."""
    return PC(3, opening, before=' (stycke')


def _quoted_2011(opening):
    """A Q1 expression as the paper prints it, inside its quotation marks."""
    return PC(3, opening, after='”', before='”')


CRIT_2011 = crit(79, (80, 81), (82, 83), 84)
HEAD_2011 = S(78)
ESSAY_2011 = 'Skriv en uppsats på ungefär 300'


def _part3_note_2011(d):
    return (f'Under “{S(96, before=" (40").text(d)}” the scheme reprints only the instruction and the two titles; '
            f'it prints no answer, no content and no criteria for this part. Its criteria are printed for parts '
            f'I and II only: “{S(78).text(d)}”')


SPECS[2011] = [
    R('I1', [shown(S(20, after='Rätt svar: '), lead=_word_2011('Garv (stycke 2)')),
             shown(S(22, after='Rätt svar: '), lead=_word_2011('Bortåt (stycke 3)')),
             shown(S(24, after='Rätt svar: '), lead=_word_2011('Omhuldande (stycke 6)')),
             shown(S(26, after='Rätt svar: '), lead=_word_2011('Driver med (stycke 10)')),
             shown(L(29, 30, after='Rätt svar: '), lead=_quoted_2011('”landar man mjukare”')),
             shown(L(33, 34, after='Rätt svar: '), lead=_quoted_2011('”när det gäller”'))],
      whole=True, total=_Split(3, '(4+2 poäng)'),
      rownote=quote(S(18, after='1. ', before=' (4+2'), S(27),
                    lead='The scheme reprints the two instructions as'),
      question=QL(3, '1. Ersätt de understrukna orden', 'Garv (stycke 2)', 'Bortåt (stycke 3)',
                  'Omhuldande (stycke 6)', 'Driver med (stycke 10)', 'Ersätt de följande understrukna',
                  '”landar man mjukare”', 'och', '”när det gäller”'),
      pages=(2, 3)),
    R('II1', [graded(HEAD_2011, PARTP(), CRIT_2011)],
      rownote=examples(S(88, before=' (stycke'), L(88, 95, after='Möjliga svar: ')),
      pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2011)],
      question=QP(4, ESSAY_2011, 'Hur står sig')),
]

# The asks the census missed (paper_census ADDED_ASKS, the lead), from the drafter's ready specs above.
SPECS[2011].append(R('III2', [unprinted(_part3_note_2011)], question=QP(4, ESSAY_2011, '”De flesta', 'Abraham Lincoln')))


# ====================================================================== 2012
# ====================================================================== 2012
# ================================================================ 2012 HL ===
# Drafted (small-languages lane, 20 Nov): the two open asks of this sitting,
# II1, III1. Live: I1, I2-I6 (6 cards); not touched (audited: see
# swedish-live-faults-2010-2016.json).
# Paper (rendered pp2-4): the rule (p2 y119-133); the article "Övning i 10 000
# timmar slår medfödd begåvning" runs pp2-3 (title p2 y152, paragraphs 1)-16)
# to the source lines "Artikeln är baserad på ... i Svenska Dagbladet den 20
# oktober 2011" p3 y595-607); "Del I" + "(Totalt 30 poäng)" (p3 y647), Q1 on
# p3, Q2-Q6 on p4; "Del II" + "(Totalt 30 poäng)" (p4 y452), the quotation
# (y494-508) and the task (y549); "Del III" + "(Totalt 40 poäng)" (p4 y632), the
# instruction (y660-673) and two UNNUMBERED titles "Arbetet är sin egen
# belöning" (y701) / "eller" (y729) / "I vårt moderna samhälle handlar allt om
# här och nu" (y756).
# CENSUS (for the lead): Part III is keyed as ONE ask, III1, whose text runs
# both titles together ("Arbetet är sin egen belöning eller I vårt moderna
# samhälle ..."). The paper prints two titles, a choice of one: III2 "I vårt
# moderna samhälle handlar allt om här och nu" (p4 x57 y756) is MISSED. III1 is
# carded below on title 1 only. Once the census adds III2:
# R('III2', [unprinted(_part3_note_2012)], question=QP(4, ESSAY_2012, 'I vårt moderna')).
# PRICES: II1 the part head's "(Totalt 30 poäng)" (PARTP), III1 "(Totalt 40
# poäng)" (PARTP); the scheme heads the parts "Del II (30 poäng)" (86) and
# "Del III (40 poäng)" (101), the same totals.
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = unnumbered; p2, p6-7 blank):
# - Criteria (p5 top, 78-85, between Q6's answer and Part II): "Anmärkning:" /
#   "I del I och II kommer följande kriterier att vägas in i
#   betygssättningen:" -- for Parts I AND II, not Part III -- then four
#   criteria WITH percentages, "– 30%" (80), "– 30%" (81-82), "– 30%" (83-84),
#   "– 10%" (85): 100 %.
# - Part II (86-88 reprint the head and the quotation, without the paper's
#   "(...)" and with a capital "Med"; the task line is not reprinted): one
#   italic paragraph, 89-100, "Citatet visar på vikten av beslutsamhet, flit
#   och dedikation. ... att prestera allt bättre?" (no heading, no marks).
# - Part III (101-106): the head, the instruction and both titles reprinted,
#   NOTHING else.
# SHAPES:
# - II1: graded (10b), 30/30/30/10 % of 30 = 9/9/9/3; head the criteria's own
#   lead (79; no descriptive line printed for the part); the paragraph quoted
#   as an example, not a checklist (10a).
# - III1: nothing printed for the part and criteria stated for Parts I and II
#   only: R4 (unprinted) at the paper's 40.
# JUDGEMENT CALLS:
# - Criteria read as NOT covering Part III ("I del I och II", rendered p5).
#   Alternative: III1 graded(S(79), PARTP(), CRIT_2012) (12/12/12/4).
# - II1's question is the census text (its "(Totalt 30 poäng)" taken off by
#   clean_question), checked against p4 y494-549. The scheme's reprint of the
#   quotation differs in punctuation and case only: not quoted.
# - The paragraph prints "räckhåll?." (93; rendered: as printed) and is quoted
#   as printed.
# - Reading text pp2-3 (rendered: title p2 y152, the text to the source lines p3
#   y607; Del I from p3 y647): II1 carries pages=(2, 3). The live 2012 cards
#   carry sourceMaterial.pages [3] (flagged, P).
# GLYPHS: none. å ä ö read cleanly in the lines used ("dedikation",
# "räckhåll", "betygssättningen"; render checked).

CRIT_2012 = crit(80, (81, 82), (83, 84), 85)
HEAD_2012 = S(79)
ESSAY_2012 = Run('Skriv en uppsats på ungefär 300', 'nedan.')


def _part3_note_2012(d):
    return (f'Under “{S(101, before=" (40").text(d)}” the scheme reprints only the instruction and the two titles; '
            f'it prints no answer, no content and no criteria for this part. Its criteria are printed for parts '
            f'I and II only: “{S(79).text(d)}”')


SPECS[2012] = [
    R('II1', [graded(HEAD_2012, PARTP(), CRIT_2012)],
      rownote=examples(None, L(89, 100)), pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2012)],
      question=QP(4, ESSAY_2012, 'Arbetet är sin')),
]

# The asks the census missed (paper_census ADDED_ASKS, the lead), from the drafter's ready specs above.
SPECS[2012].append(R('III2', [unprinted(_part3_note_2012)], question=QP(4, ESSAY_2012, 'I vårt moderna')))


# ====================================================================== 2013
# ====================================================================== 2013
# ================================================================ 2013 HL ===
# Drafted (small-languages lane, 20 Nov): the seven open asks of this sitting,
# I1a-e, II1, III1. Live: I2-I6 (5 cards); not touched (audited: see
# swedish-live-faults-2010-2016.json).
# Paper (rendered pp2-4): the rule (p2 y93-109); the article "Rätt låt i
# högtalarna – vår tids huskur" runs pp2-3 (title p2 y135, unnumbered
# paragraphs to the source line "Baserad på artikeln ... i Svenska Dagbladet den
# 2 juli 2012" p3 y247); "Del I" + "(Totalt 30 poäng)" (p3 y348); Q1 "1. Ersätt
# orden eller uttrycken med andra som betyder samma sak." + "(5poäng)" (y398,
# the price a cell at x476), then (a)-(e), ONE expression per printed line
# (raw spans and render: (a) "från vaggan till graven" y417, (b) "navigerar"
# y429, (c) "föreställning" y442, (d) "över huvud taget" y455, (e) "nedstämda"
# y467); Q2-Q6 "(5poäng)" each on p3; p4 "Del II" + "(Totalt 30 poäng)" (y72);
# "Del III" + "(Totalt 40 poäng)" (y295), the instruction (y341-355) and two
# UNNUMBERED titles: "Diskutera åsikten som uttrycks i William Shakespeares
# pjäs Köpmannen från Venedig:" with five verse lines (y383-493) / "eller:"
# (y548) / "Att följa sina drömmar – en bitterljuv resa" (y603).
# CENSUS (for the lead):
# - Q1 MIS-KEYED: eu_paper joins each expression line with the next (12-13 pt
#   lower, inside its cell tolerance), so the census reads (a) "från vaggan
#   till graven navigerar", (b) "föreställning", (c) "över huvud taget", (d)
#   "nedstämda", (e) "" -- every letter from (b) carries the NEXT letter's
#   word and (e) none. The printed pairing (render, p3 x100-136 y417-467) is
#   a) från vaggan till graven, b) navigerar, c) föreställning, d) över huvud
#   taget, e) nedstämda, and the scheme answers them in that order (48-57).
#   Each question below is cut from the reader's own lines at the printed word
#   (PC), and its conceptId taken from that question (concept='question').
# - Part III is keyed as ONE ask, III1, whose text runs both titles together.
#   The paper prints two titles, a choice of one: III2 "Att följa sina drömmar
#   – en bitterljuv resa" (p4 x71 y603) is MISSED. III1 is carded on title 1
#   only. Once the census adds III2: R('III2', [unprinted(_part3_note_2013)],
#   question=QP(4, ESSAY_2013, 'Att följa sina')).
# PRICES:
# - I1a-e: the paper prints ONE price, "(5poäng)", on Q1's head; the SCHEME
#   prints a mark per expression, "(1*5 poäng)" (line 47, rendered p3: bold,
#   right). Carded per letter at that printed 1 (RX), five letters adding to
#   the paper's 5 (the census walks the same 1 down: tariff (1, 1, 1)).
# - II1: the part head's "(Totalt 30 poäng)" (PARTP); scheme "Del II (30
#   poäng)" (106).
# - III1: the part head's "(Totalt 40 poäng)" (PARTP); scheme "Del III (Totalt
#   40 poäng)" (122).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-6 = unnumbered; p2 the SEC's
# standard note, pp7-8 blank):
# - Q1 (47-57): the instruction reprinted as the paper prints it with "(1*5
#   poäng)"; each expression on a line of its own, "(stycke 1) från vaggan
#   till graven" (bold), then "Rätt svar:" (roman) and the accepted
#   alternatives in italics: a) 49, b) 51, c) 53, d) 55, e) 57.
# - Criteria (p5, 98-105, between Q6's answer and Part II): "Anmärkning:" / "I
#   del I och II kommer följande kriterier att vägas in i betygssättningen:" --
#   Parts I AND II, not Part III -- then "– 30%" (100), "– 30%." (101-102),
#   "– 30%." (103-104), "– 10%." (105): 100 %.
# - Part II (106-109 reprint the head, the quotation with "(stycke 1)" added,
#   and the task): one paragraph, 110-118, "Möjliga svar:" (roman) "Musiken
#   finns i dag med oss hela tiden. ... upplevelse eller epok." (italics).
# - Part III (p6, 122-131): the head, the instruction and both titles
#   reprinted (the verse set in four lines, not five), NOTHING else.
# SHAPES:
# - I1a-e: one(gloss) each at the scheme's printed 1.
# - II1: graded (10b), 9/9/9/3 of 30; head the criteria's own lead (99; no
#   descriptive line printed for the part); the "Möjliga svar:" paragraph
#   quoted as an example, not a checklist (10a).
# - III1: nothing printed for the part, criteria stated for Parts I and II
#   only: R4 (unprinted) at the paper's 40.
# JUDGEMENT CALLS:
# - I1 per letter (the census keys a)-e) and the scheme prints "1*5"), not
#   whole at the parent key.
# - "Rätt svar:" is a label (roman, the answers italic): cut off every row.
# - Criteria read as NOT covering Part III (rendered p5). Alternative: III1
#   graded(S(99), PARTP(), CRIT_2013) (12/12/12/4).
# - II1's question is the census text (its "(Totalt 30 poäng)" taken off by
#   clean_question), checked against p4 y112-162. The scheme's reprint adds
#   "(stycke 1)" after the quotation: a paragraph reference, not a rewording;
#   not quoted.
# - III1's question: the instruction, the lead line and the five verse lines
#   as printed (Run), the "eller:" and title 2 left out.
# - Reading text pp2-3 (rendered: title p2 y135, the text to the source line p3
#   y247; Del I from p3 y348): pages=(2, 3) on I1a-e and II1. The live 2013
#   cards carry sourceMaterial.pages [3] (flagged, P).
# GLYPHS: none. å ä ö é read cleanly in the lines used ("nedstämda",
# "föreställning", "idé", "bedrövade"; render and raw spans checked).



def _q(*sels):
    """A question cut from printed paper lines: each line (or cut) in order,
    its own marker taken off, joined by a space."""
    return lambda d, _census=None: _clean(' '.join(_MARKER.sub('', s.text(d), count=1) for s in sels))


STEM_2013 = PL(3, '1. Ersätt orden eller uttrycken')
Q1P_2013 = RX(47, r'\((\d)\*\d poäng\)')
CRIT_2013 = crit(100, (101, 102), (103, 104), 105)
HEAD_2013 = S(99)
ESSAY_2013 = Run('Skriv en uppsats på ungefär 300', 'nedan.')


def _part3_note_2013(d):
    return (f'Under “{S(122, before=" (Totalt").text(d)}” the scheme reprints only the instruction and the two '
            f'titles; it prints no answer, no content and no criteria for this part. Its criteria are printed for '
            f'parts I and II only: “{S(99).text(d)}”')


SPECS[2013] = [
    R('I1a', [one(S(49, after='Rätt svar: '), Q1P_2013)], total=Q1P_2013, concept='question',
      question=_q(STEM_2013, PC(3, '(a) från vaggan', after='(a) ', before=' navigerar')), pages=(2, 3)),
    R('I1b', [one(S(51, after='Rätt svar: '), Q1P_2013)], total=Q1P_2013, concept='question',
      question=_q(STEM_2013, PC(3, '(a) från vaggan', after='graven ')), pages=(2, 3)),
    R('I1c', [one(S(53, after='Rätt svar: '), Q1P_2013)], total=Q1P_2013, concept='question',
      question=_q(STEM_2013, PC(3, '(b) föreställning', after='(b) ')), pages=(2, 3)),
    R('I1d', [one(S(55, after='Rätt svar: '), Q1P_2013)], total=Q1P_2013, concept='question',
      question=_q(STEM_2013, PC(3, '(c) över huvud', after='(c) ')), pages=(2, 3)),
    R('I1e', [one(S(57, after='Rätt svar: '), Q1P_2013)], total=Q1P_2013, concept='question',
      question=_q(STEM_2013, PC(3, '(d) nedstämda', after='(d) ')), pages=(2, 3)),
    R('II1', [graded(HEAD_2013, PARTP(), CRIT_2013)],
      rownote=examples(S(110, before=' Musiken'), L(110, 118, after='Möjliga svar: ')), pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2013)],
      question=QP(4, ESSAY_2013, Run('Diskutera åsikten', 'Tro ingen sådan'))),
]

# The asks the census missed (paper_census ADDED_ASKS, the lead), from the drafter's ready specs above.
SPECS[2013].append(R('III2', [unprinted(_part3_note_2013)], question=QP(4, ESSAY_2013, 'Att följa sina')))


# ====================================================================== 2014
# ====================================================================== 2014
# ================================================================ 2014 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched (audited: see
# swedish-live-faults-2010-2016.json).
# Paper (rendered pp2-4): the rule (p2 y60-78) and "(Totalt 100 poäng)" (p2
# y101); the article (no title printed) runs pp2-3, from "Varje natt händer
# det." (p2 y122) to the source line "Ur artikeln ”Forskningen ger nya
# ledtrådar till drömmens gåta” av Anna Lagerblad i Svenska Dagbladet den 15
# april 2013" (p3 y441); "Del I" + "(30 poäng)" (p3 y535), Q1 on p3, Q2-Q6 on
# p4; "Del II" + "(30 poäng)" (p4 y419), the task (y444-475); "Del III" + "(40
# poäng)" (p4 y550), the instruction (y575-591) and two titles NUMBERED "1."
# (y616, attribution "Aristoteles" y631) / "Eller" (y662) / "2." (y693,
# attribution "Ralph Waldo Emerson" y720).
# CENSUS: III1 and III2 keyed as printed (the census glues the "Eller" printed
# between the titles onto III1's text: the questions below are cut from the
# paper's lines).
# PRICES: II1 the part head's "(30 poäng)" (PARTP), III1/III2 "(40 poäng)"
# (PARTP); the scheme prints "Del II (30 poäng)" (91) and "Del III (40 poäng)"
# (102), the same totals.
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4 = printed pages 2-3; p2 the
# SEC's standard note, pp5-6 blank):
# - Part II (91-94 reprint the head and the task, without its closing full
#   stop): ONE paragraph, 95-101, "Förslag till lösningar:" (roman, a heading)
#   then "Drömmar är högst personliga ... allenarådande förklaringsmodell."
#   (italics). No marks inside it.
# - Part III (102-109): the head, the instruction and both titles with their
#   attributions reprinted (without the paper's "1." / "2."), NOTHING else.
# - NO criteria anywhere in this scheme (rendered pp3-4: no "Anmärkning", no
#   percentages; every other 2010-2016 scheme prints them).
# SHAPES:
# - II1: a model paragraph for the commentary, no criteria: shown, priced as a
#   whole on the paper's 30 (10a, questionTotal), its heading "Förslag till
#   lösningar:" quoted on the row.
# - III1/III2: nothing printed for the part: R4 (unprinted) at the paper's 40,
#   the note saying what the scheme does print (ruling 4).
# JUDGEMENT CALLS:
# - II1's paragraph is one shown row (one printed paragraph, rendered p4), not
#   split into sentences.
# - III1/III2: the instruction (its two printed lines) plus the title and its
#   attribution line, the "1." / "2." taken off as markers (ruling B cites them
#   Section III Q1/Q2).
# - Reading text pp2-3 (rendered: the text from p2 y122 to the source line p3
#   y441; Del I from p3 y535): II1 carries pages=(2, 3). The live 2014 cards
#   carry sourceMaterial.pages [3] (flagged, P).
# GLYPHS: none. å ä ö read cleanly in the lines used ("Förslag",
# "allenarådande", "vakendröm"; render checked). "Arbiturenten" (99-100) is
# the SEC's own spelling (rendered p4), lifted as printed.

ESSAY_2014 = Run('Skriv en uppsats på minst 300', 'nedan.')


def _part3_note_2014(d):
    return (f'Under “{S(102, before=" (40").text(d)}” the scheme reprints only the instruction and the two titles '
            f'with their attributions; it prints no answer, no content and no criteria for this part (this '
            f'sitting\'s scheme prints no criteria at all).')


SPECS[2014] = [
    R('II1', [shown(L(95, 101, after='Förslag till lösningar: '))], whole=True,
      rownote=quote(S(95, before=' Drömmar'), lead='The scheme heads it'), pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2014)],
      question=QP(4, ESSAY_2014, '1. ”Hoppet', 'Aristoteles')),
    R('III2', [unprinted(_part3_note_2014)],
      question=QP(4, ESSAY_2014, '2. ”Fastän', 'Ralph Waldo')),
]


# ====================================================================== 2015
# ====================================================================== 2015
# ================================================================ 2015 HL ===
# Drafted (small-languages lane, 20 Nov): the two open asks of this sitting,
# II1, III1. Live: I1a-e, I2-I6 (10 cards); not touched (audited: see
# swedish-live-faults-2010-2016.json).
# Paper (rendered pp2-4): the rule "Läs texten noga ... All svar måste vara
# skrivna på svenska." (p2 y83-96; the paper prints "All", not "Alla") and
# "(Totalt 100 poäng)" (y112); the article "Skräck som terapi och frälsning"
# runs pp2-3 (title p2 y129, paragraphs 1-11 to the byline "Av Anna Arnman ur
# Forskning och Framsteg, 2008-03-01" p3 y278); "Del I" + "(Totalt 30 poäng)"
# (p3 y347), Q1-Q6 on p3; p4 "Del II" + "(30 poäng)" (y63), the quotation
# (y102) and the task (y125); "Del III" + "(40poäng)" (y193), the instruction
# (y238) and two UNNUMBERED titles "Vikten av att ta risker i livets alla
# skeenden." (y308) / "eller:" (y355) / "”Han är rikast som nöjer sig med
# minst.” (Sokrates)" (y401).
# CENSUS (for the lead): Part III is keyed as ONE ask, III1, whose text runs
# both titles together ("... skeenden. eller: ”Han är rikast ...” (Sokrates)").
# The paper prints two titles, a choice of one: III2 "”Han är rikast som nöjer
# sig med minst.” (Sokrates)" (p4 x57 y401) is MISSED. III1 is carded on title
# 1 only. Once the census adds III2: R('III2', [unprinted(_part3_note_2015)],
# question=QP(4, ESSAY_2015, '”Han är rikast')).
# PRICES: II1 the part head's "(30 poäng)" (PARTP), III1 "(40poäng)" (PARTP);
# the scheme heads the parts "Del II (Totalt 30 poäng)" (83) and "Del III
# (Totalt 40 poäng)" (92), the same totals.
# WHAT THE SCHEME PRINTS (rendered scheme pp3-4 = printed pages 2-3; p2 the
# SEC's standard note, pp5-6 blank):
# - Part II (83-85 reprint the head, the quotation and the task): ONE italic
#   paragraph, 86-91, opening with the heading "Till exempel:" ("For
#   example:"), "Kandidaten kan diskutera hur biografen tagit över kyrkans roll
#   ... relevansen i kandidatens personliga respons."
# - Part III (92-96): the head, the instruction and both titles reprinted,
#   nothing per title.
# - Criteria (p4, 97-104, printed AFTER Part III): "Anmärkning:" / "I del I och
#   II kommer följande kriterier att vägas in i betygssättningen:" -- Parts I
#   AND II, not Part III, though set under it -- then "– 30%" (99), "– 30%."
#   (100-101), "– 30%." (102-103), "– 10%." (104): 100 %.
# SHAPES:
# - II1: graded (10b), 9/9/9/3 of 30; head the criteria's own lead (98; no
#   descriptive line printed for the part); the "Till exempel:" paragraph
#   quoted under its own heading as an example, not a checklist (10a).
# - III1: nothing printed for the part, and the criteria (set under it) name
#   Parts I and II only: R4 (unprinted) at the paper's 40.
# JUDGEMENT CALLS:
# - The criteria are printed under Part III but name "del I och II": read as
#   NOT covering Part III, as every 2010-2016 sitting. Alternative: III1
#   graded(S(98), PARTP(), CRIT_2015) (12/12/12/4).
# - II1's question is the census text (its "(30 poäng)" taken off by
#   clean_question), checked against p4 y102-125.
# - III1's question: the instruction and title 1 from the paper's own lines
#   (the census runs on into "eller:" and title 2).
# - Reading text pp2-3 (rendered: title p2 y129, the text to the byline p3
#   y278; Del I from p3 y347): II1 carries pages=(2, 3). The live 2015 cards
#   carry sourceMaterial.pages [3] (flagged, P).
# GLYPHS: no wrong letters in the lines used (render checked: "sådant" (87)
# sets its "så" in a second font span, Cambria, and reads U+00E5 correctly).
# The scheme's header lines 4-11 ("&RLPLVL~QQD6FU~GXLWKH6WiLW" for
# "Coimisiún na Scrúduithe Stáit", "0DUNLQJ6FKHPH" for "Marking Scheme": ASCII
# letters read 29 code points low, '&' U+0026 for 'C' U+0043, '~' U+007E for
# 'ú') and the note heading (15, 35) are a shifted font map; cover and
# boilerplate only, no card uses them.

CRIT_2015 = crit(99, (100, 101), (102, 103), 104)
HEAD_2015 = S(98)
ESSAY_2015 = 'Skriv en uppsats på ungefär 300'


def _part3_note_2015(d):
    return (f'Under “{S(92, before=" (Totalt").text(d)}” the scheme reprints only the instruction and the two '
            f'titles; it prints no answer and no content for this part. Its criteria, printed under the titles, '
            f'name parts I and II only: “{S(98).text(d)}”')


SPECS[2015] = [
    R('II1', [graded(HEAD_2015, PARTP(), CRIT_2015)],
      rownote=examples(S(86, before=' Kandidaten'), L(86, 91, after='Till exempel: ')), pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2015)],
      question=QP(4, ESSAY_2015, 'Vikten av att')),
]

# The asks the census missed (paper_census ADDED_ASKS, the lead), from the drafter's ready specs above.
SPECS[2015].append(R('III2', [unprinted(_part3_note_2015)], question=QP(4, ESSAY_2015, '”Han är rikast')))


# ====================================================================== 2016
# ====================================================================== 2016
# ================================================================ 2016 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I1a, I2, I3, I4, I5, I6, II1, III1. No live card.
# Paper (rendered pp2-4): "PROV PÅ SVENSKA 2016" (p2 y78); the rule (p2
# y120-134); the article "Psykologiprofessor gör upp med självhjälpstrenden"
# runs pp2-3 (title p2 y163, paragraphs 1-15 to the source lines "Baserad på
# ”Psykologiprofessor gör upp med självhjälpstrenden, av Thomas Lerner i DN den"
# / "30 september 2015" p3 y462-474); "Del I" + "(Totalt 30 poäng)" (p3 y523);
# "1a." (a cell at x72) "Ersätt följande ord och uttryck med andra som betyder
# samma sak: (3 × 1 poäng)" (y572) over three UNLETTERED word lines
# "Profiterar på" / "Bitande" / "Återvändsgränd" (y621-659); "1b. Ersätt
# följande uttryck med ett annat som betyder samma sak:" + "(2 poäng)" (y703)
# over "Gå på magkänslan (stycke 2)" (y727); p4 Q2-Q6 "(5 poäng)" each; "Del
# II" + "(30 poäng)" (y436); "Del III" + "(40 poäng)" (y568), the instruction
# (y597-611) and two UNNUMBERED titles "Vi blir till i relationen till andra."
# (y640) / "Eller" (y669) / "”Världen kan vara ett ganska hemskt ställe om vi
# inte arbetar tillsammans för att skapa ett mer jämlikt, mer demokratiskt och
# mer hållbart samhälle.”" (y699-713) with "Fintan O'Toole, The Irish Times, 22
# februari 2016." (y727).
# CENSUS (for the lead):
# - Q1(b) is MISSED: the census keys only I1a (the "1a." head, tariff (3, 1,
#   3)); the paper prints a second part, "1b. Ersätt följande uttryck med ett
#   annat som betyder samma sak:" + "(2 poäng)" (p3 x72 y703, the price at
#   x441) over "Gå på magkänslan (stycke 2)" (p3 x100 y727). The scheme
#   answers it (51-53: "1b. ... (2 poäng)" / "Gå på magkänslan (stycke 2)" /
#   "Rätt svar: Agera instinkitivt, utan att reflektera"). Once the census adds
#   it: R('I1b', [one(S(53, after='Rätt svar: '), PP())], pages=(2, 3)), priced
#   from its own "(2 poäng)" (one printed answer at the printed 2).
# - Part III is keyed as ONE ask, III1, whose text runs both titles together.
#   III2 "”Världen kan vara ett ganska hemskt ställe ...”" + "Fintan O'Toole,
#   The Irish Times, 22 februari 2016." (p4 x72 y699-727) is MISSED. III1 is
#   carded on title 1 only. Once the census adds III2: R('III2',
#   [unprinted(_part3_note_2016)], question=QP(4, ESSAY_2016, Run('”Världen kan',
#   'jämlikt, mer'), 'Fintan O')).
# PRICES:
# - I1a: "(3 × 1 poäng)" (census tariff (3, 1, 3): PP() reads 3): a mark PER
#   WORD, so three one() rows at the 1 read from that printed line (PaperP: "1
#   poäng"), adding to 3. The scheme prints "(3*1 poäng)" (47).
# - I2-I6: "(5 poäng)" each (PP); the scheme prints the same.
# - II1: the part head's "(30 poäng)" (PARTP); scheme "Del II (30 poäng)" (131).
# - III1: the part head's "(40 poäng)" (PARTP); scheme "Del III" / "(40
#   poäng)" (154-155).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-6 = printed pages 1-4; p2 the
# SEC's standard note, pp7-8 blank):
# - Q1a (47-50): the head reprinted as the paper prints it with "(3*1 poäng)";
#   each word, then "Rätt svar:" and its answer on the same line.
# - Q2 (54-55 reprint): one paragraph, 56-57, "Rätt svar: Vi sover mindre ...".
# - Q3 (58-59 reprint, reworded: "... med positiv och negativ visualisering"
#   for the paper's "... positiv respektive negativ ..."; quoted, 10f): one
#   paragraph, 60-67, "Rätt svar hämtat ur stycke 12-14: Positiv visualisering
#   ...".
# - Q4 (68-69 reprint): one paragraph, 70-74, "Rätt svar baserat på stycke 3-8:
#   I dag krävs ...".
# - Q5 (79-80 reprint): a comment for Q5 AND Q6, "Inledande kommentar om
#   bedömningen av svaren till frågorna 5 och 6:" (81, bold italic) over
#   "Frågorna är så formulerade ... idéer som framförs i texten." (82-84);
#   then TWO paragraphs, "Möjliga svar: Coacher gör inget ... framstå som
#   modern." (85-89) and "Stoikerna förespråkar ... inte i stoicismen." (90-96).
# - Q6 (97-99 reprint): FOUR paragraphs, "Möjligt svar: En präst är ... god mot
#   andra." (100-106), "En psykoterapeut ... tjäna mer." (107-110), "För
#   coachen ... Detta är ren" / "business. ... uppnå dessa." (111-113 + 118-119,
#   over the page break), "Ett fullgott svar diskuterar pengarnas roll, ...
#   inför sig själva och andra." (120-122).
# - Criteria (p5, 123-130, after Q6): "Anmärkning:" / "I del I och II kommer
#   följande kriterier att vägas in i betygssättningen:" -- Parts I AND II, not
#   Part III -- then "– 30%" (125), "– 30%." (126-127), "– 30%." (128-129),
#   "– 10%." (130): 100 %.
# - Part II (131-134 reprint the head and the task): "Om kandidaten håller med
#   skulle ett möjligt svar inkludera ideer såsom:" (135) over six bullets
#   (136-141, the last "Etc."), "Om kandidaten inte håller med:" (142) over six
#   (143-149, the fifth wrapped 147-148, the last "Etc.").
# - Part III (p6, 154-162): the head, the instruction and both titles
#   reprinted, title 1 as "Vi blir till i mötet med andra." (the paper: "... i
#   relationen till andra."; quoted, 10f); nothing else.
# SHAPES:
# - I1a: three one() rows at 1, each led by its word as the paper prints it.
# - I2, I3, I4: one printed paragraph each -> one claimable row at 5.
# - I5 (two paragraphs) and I6 (four): shown rows, whole=True on the 5; the
#   comment for questions 5 and 6 and each "Möjliga/Möjligt svar:" heading
#   quoted on the row.
# - II1: graded (10b), 9/9/9/3 of 30; head the criteria's own lead (124; no
#   descriptive line printed for the part); both bullet lists quoted under
#   their own headings as examples, not a checklist (10a).
# - III1: nothing printed for the part, criteria stated for Parts I and II
#   only: R4 (unprinted) at the paper's 40; the scheme's reprint of the title
#   quoted (10f).
# JUDGEMENT CALLS:
# - Q6's fourth paragraph ("Ett fullgott svar diskuterar ...") states what a
#   full answer covers; printed in the answer's own italics under Q6 (rendered
#   p5): shown as a row, not moved to the note.
# - Q6's third paragraph joins its two halves across the page break (J), one
#   printed paragraph (rendered pp4-5).
# - "Rätt svar:" and the "Rätt svar hämtat/baserat ...:" / "Möjliga svar:"
#   heads are cut off the rows; the ones that cite paragraphs are quoted.
# - The two "Etc." bullets are printed bullets: quoted as printed.
# - Criteria read as NOT covering Part III (rendered p5). Alternative: III1
#   graded(S(124), PARTP(), CRIT_2016) (12/12/12/4).
# - I1a's question: the head line (its price taken off) and the three word
#   lines, one per line (QL); the "1a." cell is the address, not the words.
# - Reading text pp2-3 (rendered: title p2 y163, the text to the source lines p3
#   y474; Del I from p3 y523): pages=(2, 3) on Part I and II1.
# GLYPHS: none. å ä ö read cleanly in the lines used ("Återvändsgränd",
# "förändring", "befolkningsmönster"; render checked). SEC typing lifted as
# printed: "instinkitivt" (53, I1b's answer), "kandiaten" (82), "Desstom" (66),
# "ideer" (135).

REPRINT = 'The scheme reprints this question as'
Q1A_P = PaperP(3, 'Ersätt följande ord och uttryck med')
CRIT_2016 = crit(125, (126, 127), (128, 129), 130)
HEAD_2016 = S(124)
ESSAY_2016 = Run('Skriv en uppsats på ungefär 300', 'nedan.')
Q56_2016 = quote(S(81), L(82, 84), lead='The scheme prints, for questions 5 and 6')


def _part3_note_2016(d):
    return (f'Under “{S(154).text(d)}” the scheme reprints only the instruction and the two titles; it prints no '
            f'answer, no content and no criteria for this part. Its criteria are printed for parts I and II only: '
            f'“{S(124).text(d)}”')


SPECS[2016] = [
    R('I1a', [one(S(48, after='Rätt svar: '), Q1A_P, lead=PL(3, 'Profiterar på')),
              one(S(49, after='Rätt svar: '), Q1A_P, lead=PL(3, 'Bitande')),
              one(S(50, after='Rätt svar: '), Q1A_P, lead=PL(3, 'Återvändsgränd'))],
      question=QL(3, 'Ersätt följande ord och uttryck med', 'Profiterar på', 'Bitande', 'Återvändsgränd'),
      pages=(2, 3)),
    R('I2', [one(L(56, 57, after='Rätt svar: '), PP())], pages=(2, 3)),
    R('I3', [one(L(60, 67, after='stycke 12-14: '), PP())],
      rownote=both(quote(L(58, 59, after='3. ', before=' (5 poäng)'), lead=REPRINT),
                   quote(S(60, before=' Positiv'), lead='It heads its answer')), pages=(2, 3)),
    R('I4', [one(L(70, 74, after='stycke 3-8: '), PP())],
      rownote=quote(S(70, before=' I dag'), lead='The scheme heads its answer'), pages=(2, 3)),
    R('I5', [shown(L(85, 89, after='Möjliga svar: ')), shown(L(90, 96))], whole=True,
      rownote=both(Q56_2016, quote(S(85, before=' Coacher'), lead='It heads its answer')), pages=(2, 3)),
    R('I6', [shown(L(100, 106, after='Möjligt svar: ')), shown(L(107, 110)), shown(J(L(111, 113), L(118, 119))),
             shown(L(120, 122))], whole=True,
      rownote=both(Q56_2016, quote(S(100, before=' En präst'), lead='It heads its answer')), pages=(2, 3)),
    R('II1', [graded(HEAD_2016, PARTP(), CRIT_2016)],
      rownote=both(examples(S(135), S(136), S(137), S(138), S(139), S(140), S(141)),
                   examples(S(142), S(143), S(144), S(145), S(146), L(147, 148), S(149))),
      pages=(2, 3)),
    R('III1', [unprinted(both(_part3_note_2016, quote(S(158), lead='It reprints this title as')))],
      question=QP(4, ESSAY_2016, 'Vi blir till i')),
]

# The asks the census missed (paper_census ADDED_ASKS, the lead), from the drafter's ready specs above.
SPECS[2016].insert(1, R('I1b', [one(S(53, after='Rätt svar: '), PaperP(3, '(2 poäng)'))], total=PaperP(3, '(2 poäng)'),
                        question=lambda d, _c=None: clean_question(PC(3, '1b. Ersätt', after='1b. ').text(d) + ' '
                                                                    + PL(3, 'Gå på magkänslan').text(d)),
                        concept='question', pages=(2, 3)))
SPECS[2016].append(R('III2', [unprinted(_part3_note_2016)],
                     question=QP(4, ESSAY_2016, Run('”Världen kan', 'jämlikt, mer'), 'Fintan O')))


# ====================================================================== 2017
# ====================================================================== 2017
# ================================================================ 2017 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched (audited:
# swedish-live-faults-2017-2026.json).
# Paper (rendered PDF pp2-4; the booklet prints "3"/"4" on PDF pp3/4): the rule
# "Läs texten noga ... Alla svar måste vara skrivna på svenska." (p2 y65-81);
# the article "Svenskfödd forskare ska rädda oss från onda maskiner" runs p2
# y148 to its source lines "Ur Svenskfödd forskare ... den 15 februari 2016" p3
# y389-418; "Del I" + "(30 poäng)" (p3 y513), Q1-Q3 on p3, Q4-Q6 on p4; "Del
# II" + "(30 poäng)" (p4 y329), the commentary on a quotation (y352-392); "Del
# III" + "(40 poäng)" (p4 y487), the instruction (y511-527) and two titles
# numbered "1." (y574) / "Eller" (y625) / "2." (y672-702).
# PRICES:
# - II1: the part head's "(30 poäng)" (PARTP; the census reads all three part
#   totals this sitting); the scheme "Del II (30 poäng)" (100).
# - III1/III2: the part head's "(40 poäng)" (PARTP); the scheme the same (124).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3; p2 the
# SEC's standard note; pp6-7 blank):
# - Part II (100-103): the head, the task REWORDED ("Skriv en uppsats på 100
#   ord där du uttrycker dina tankar om detta citat." for the paper's
#   "Kommentera detta citat och uttryck dina tankar med ungefär 100 ord.") and
#   the quotation; then "Till exempel:" (104, plain) over six italic
#   "Kandidaten kan diskutera ..." paragraphs, 105-106, 107-109, 114-115,
#   116-117, 118-119, 120-122 (110-113 are the page number and page break),
#   and one italic closing line, "Vad som dessutom kommer att bedömas är
#   relevansen i kandidatens personliga respons." (123).
# - Part III (124-131): the head, the instruction and both titles reprinted
#   (title 2 reworded: "Min åsikt ... lika högt." / "Skriv en uppsats där du
#   bemöter den här uppfattningen ..." for the paper's "“Min åsikt ... lika
#   högt”. / Bemöt den här uppfattningen ..."); nothing under them.
# - Criteria (p5, 132-139, printed AFTER Part III's titles): "Anmärkning:" /
#   "I del I och II kommer följande kriterier att vägas in i
#   betygssättningen:" -- Parts I AND II, not Part III -- then four criteria
#   WITH PERCENTAGES: "– 30%." (134), "– 30%." (135-136), "– 30 %." (137-138),
#   "– 10%." (139): 100 %.
# SHAPES:
# - II1: graded (10b), 30/30/30/10 % of the paper's 30 = 9 / 9 / 9 / 3; head
#   the criteria's own lead (133; no descriptive line is printed for the part);
#   the six paragraphs quoted under the scheme's own "Till exempel:" as
#   examples, not a checklist (10a), the closing line and the reworded task
#   quoted (10f).
# - III1/III2: nothing printed for this part, and the criteria are stated for
#   parts I and II only: R4 (unprinted) at the paper's 40, the note saying
#   what the scheme prints; III2's note also quotes the reworded title (10f).
# JUDGEMENT CALLS:
# - Criteria read as NOT covering Part III: the scheme names "del I och II"
#   although it prints the block after Part III (the sibling 2010-2016 drafts
#   read the same words the same way). Alternative: III1/III2
#   graded(HEAD_2017, PARTP(), CRIT_2017) (12/12/12/4).
# - II1's closing line (123) is a marking note, not an example: quoted on its
#   own after the examples.
# - II1's question: the instruction line and the two printed lines of the
#   quotation (the census glues "(30 poäng)" in front of it).
# - III2's question: the quotation and its task line, both printed as title 2.
# - Reading text pp2-3 (rendered): II1 carries pages=(2, 3). The live 2017
#   cards carry [3] (flagged, P).
# GLYPHS: none. å ä ö read as drawn in every line used (render checked);
# "‐" (U+2010) in the paper's time line is the SEC's hyphen.

CRIT_2017 = crit(134, (135, 136), (137, 138), 139)
HEAD_2017 = S(133)
ESSAY_2017 = Run('Skriv en uppsats på ungefär 300', 'nedan.')


def _part3_note_2017(d):
    return (f'Under “{S(124).text(d)}” the scheme reprints only the instruction and the two titles; it prints no '
            f'answer, no content and no criteria for this part. Its criteria, printed after the titles, are '
            f'stated for parts I and II only: “{S(133).text(d)}”')


SPECS[2017] = [
    R('II1', [graded(HEAD_2017, PARTP(), CRIT_2017)],
      rownote=both(examples(S(104), L(105, 106), L(107, 109), L(114, 115), L(116, 117), L(118, 119), L(120, 122)),
                   quote(S(123), lead='It adds'),
                   quote(S(101), lead='It reprints the task as')),
      question=QP(4, 'Kommentera detta citat', Run('”En superintelligens', 'sapiens uppstod')), pages=(2, 3)),
    R('III1', [unprinted(_part3_note_2017)],
      question=QP(4, ESSAY_2017, '1. Ett liv fyllt')),
    R('III2', [unprinted(both(_part3_note_2017, quote(L(129, 131), lead='It reprints this title as')))],
      question=QP(4, ESSAY_2017, Run('2. “Min åsikt', 'användandet av social'))),
]


# ====================================================================== 2018
# ====================================================================== 2018
# ================================================================ 2018 HL ===
# Drafted (small-languages lane, 20 Nov): the eight open asks of this sitting,
# I1a-e, II1, III1, III2. Live: I2-I6 (5 cards); not touched (audited:
# swedish-live-faults-2017-2026.json).
# Paper (rendered PDF pp2-4; the booklet prints "2" on PDF p3, one less than
# the PDF): the rule "Läs texten noga ... Alla svar måste vara skrivna på
# svenska." (p2 y65-80); the article "Forskare om nätet: Som att lämna barn
# ensamma i bar" runs p2 y109 to its source lines "Ur artikel ... den 29
# januari 2017" / "Texten har redigerats ..." p3 y539-563; "Del I" + "(30
# poäng)" (p3 y591); Q1 is printed WITHOUT a number: the stem "Förklara dessa
# ord och uttryck såsom de används i texten." (p3 y621, bold) with "(5×1
# poäng)" at its right (x468), over "(a) betraktades" ... "(e) ägnar"
# (y649-733); Q2-Q6 on p4, "(5 poäng)" each; "Del II" + "(30 poäng)" (p4
# y431); "Del III" + "(40 poäng)" (p4 y578), the instruction and two titles
# "1." (y651) / "Eller" / "2." (y724).
# PRICES:
# - I1a-e: the paper prints "(5×1 poäng)" on Q1's stem line (p3 x468 y621,
#   rendered): ONE MARK FOR EACH EXPRESSION. Carded per letter at 1, read with
#   PaperP(3, '(5×1') (its worded "1 poäng"). The scheme prices Q1 "(5
#   poäng)" as a whole (48): the totals agree. The census reads NO tariff here
#   (it welds the cell into each letter's text, "(5×1 poäng) betraktades"),
#   and the exclusions' "neither document states a tariff" is wrong (CENSUS).
# - II1: the part head's "(30 poäng)" (PARTP); the scheme the same (101).
# - III1/III2: the part head's "(40 poäng)" (PARTP); the scheme the same (117).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3):
# - Q1 (48-54): the stem as the paper prints it (with "1." and "(5 poäng)"),
#   then each expression reprinted, a hyphen-minus, and its glosses in italics
#   on the same line: (a) 49, (b) 50, (c) 51-52 (one gloss list wrapped), (d)
#   53, (e) 54. Letters and words agree with the paper's.
# - Part II (101-103 reprint the head, the task and the quotation): ONE model
#   paragraph explaining the quotation, "Sonia Livingstone uttrycker
#   besvikelse: ... och kommersiellt." (104-108), and one descriptive paragraph,
#   "Kandidaten kommenterar citatet ... som stöd för sitt resonemang."
#   (109-110 + 115-116, over the page break).
# - Part III (117-122): the head, the instruction and both titles reprinted;
#   nothing under them.
# - Criteria (p5, 123-129, after Part III): "Anmärkning:" / "I del II och III
#   kommer följande kriterier att vägas in i betygssättningen:" -- Parts II AND
#   III -- then THREE criteria WITH PERCENTAGES: "– 30%." (125), "– 30%."
#   (126-127), "– 40 %." (128-129): 100 %. No "Formalia" criterion this year
#   (rendered p5: nothing after criterion 3).
# SHAPES:
# - I1a-e: one(gloss after the hyphen, PaperP) each, total the same reader.
# - II1: graded (10b), 30/30/40 % of 30 = 9 / 9 / 12; head the criteria's own
#   lead (124); the model paragraph quoted as an example and the descriptive
#   paragraph quoted after it (10a).
# - III1/III2: graded (10b), 30/30/40 % of 40 = 12 / 12 / 16; the same head.
# JUDGEMENT CALLS:
# - Three criteria, not four: the brief's graded shape names "all four
#   criteria"; this scheme prints three, with whole-number percentages adding
#   to 100 and whole-number marks on both totals, so 10b applies as printed.
#   If the lead reads "four" strictly: ruling F (the three criteria as shown
#   rows on the printed total, whole=True).
# - Q1 questions: the stem and the expression's own printed line (QP strips
#   its "(a)"); conceptId from the census text ("betraktades" etc., clean).
# - I1c: the gloss list wraps over two scheme lines (51-52), joined with a
#   space as printed ("... negativt som är gömt/ dolt, ...").
# - II1's question: the instruction line and the quotation as the paper prints
#   it (it ends "(…)." with no closing quotation mark; the scheme's reprint
#   adds one: punctuation only, not quoted).
# - III1's title prints "någon‐ Drottning Kristina" (U+2010, then a space;
#   rendered p4 y651) where the scheme prints a hyphen-minus: punctuation
#   only. QP cannot lift it: clean_question deletes a space after U+2010
#   between two word characters (the Maltese line-break rule), which would
#   print "någon‐Drottning". _iii1_2018 joins the same printed lines (the
#   instruction run and the title, its "1." taken off) without that rule; the
#   lead may prefer to narrow the rule in sl_lib instead.
# - Reading text pp2-3 (rendered): I1a-e and II1 carry pages=(2, 3). The live
#   2018 cards carry [3] (flagged, P).
# GLYPHS: none. å ä ö read as drawn in every line used; "×" (U+00D7) in "(5×1
# poäng)" is the printed sign.

Q1P_2018 = PaperP(3, '(5×1')
CRIT_2018 = crit(125, (126, 127), (128, 129))
HEAD_2018 = S(124)
ESSAY_2018 = Run('Skriv en uppsats på ungefär 300', 'nedan.')
STEM_2018 = 'Förklara dessa ord och uttryck'
II_NOTE_2018 = both(examples(None, L(104, 108)), quote(J(L(109, 110), L(115, 116)), lead='It adds'))




def _iii1_2018(d, _q):
    """The instruction and title 1 as printed (see JUDGEMENT CALLS)."""
    head = paper_run(d, 4, 'Skriv en uppsats på ungefär 300', 'nedan.')
    title = MARKER.sub('', PL(4, '1. Den som är god').text(d), count=1)
    return f'{head} {title}'


def _q1_2018(key, sel, opening):
    return R(key, [one(sel, Q1P_2018)], total=Q1P_2018, question=QP(3, STEM_2018, opening), pages=(2, 3))


SPECS[2018] = [
    _q1_2018('I1a', S(49, after='betraktades- '), '(a) betraktades'),
    _q1_2018('I1b', S(50, after='prylar- '), '(b) prylar'),
    _q1_2018('I1c', L(51, 52, after='vrår- '), '(c) dess mörkaste'),
    _q1_2018('I1d', S(53, after='lotsa- '), '(d) lotsa'),
    _q1_2018('I1e', S(54, after='ägnar- '), '(e) ägnar'),
    R('II1', [graded(HEAD_2018, PARTP(), CRIT_2018)], rownote=II_NOTE_2018,
      question=QP(4, 'Kommentera detta citat', '”Jag trodde att 2000'), pages=(2, 3)),
    R('III1', [graded(HEAD_2018, PARTP(), CRIT_2018)],
      question=_iii1_2018),
    R('III2', [graded(HEAD_2018, PARTP(), CRIT_2018)],
      question=QP(4, ESSAY_2018, '2. ”Kläderna')),
]


# ====================================================================== 2019
# ====================================================================== 2019
# ================================================================ 2019 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched (audited:
# swedish-live-faults-2017-2026.json).
# Paper (rendered PDF pp2-4): the rule (p2 y65-80); the article "Varnar för
# eufori: En hashtag förändrar inte samhället" runs p2 to its source lines "Ur
# artikeln ... den 11 februari 2018" / "Texten har redigerats ..." p3
# y430-454; "Del I" + "(30 poäng)" (p3 y526), Q1 "(5×1 poäng)" over (a)-(e) on
# p3, Q2-Q6 on p4; "Del II" + "(30 poäng)" (p4 y417), the commentary on a
# two-line quotation (y446-505); "Del III" + "(40 poäng)" (p4 y592), the
# instruction and two titles "1." (y666-680) / "Eller" / "2." (y739-754).
# PRICES:
# - II1: the head's "(30 poäng)" cell (p4 x468 y417); III1/III2: "(40 poäng)"
#   (p4 x468 y592). Both cells print "poäng" as "a" + U+0308 COMBINING
#   DIAERESIS (see GLYPHS), so neither the census (it reads only Part I's
#   total) nor PARTP/PY/PaperP reads them. Read with _PartCellNFC(page, y): PY's
#   own cell match after canonical composition (NFC). The scheme prints the
#   same totals, "Del II (30 poäng)" (113), "Del III (40 poäng)" (121), with the
#   same decomposed "ä".
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3):
# - Part II (113-116 reprint the head, the task and the quotation as the paper
#   prints them): one descriptive line, "Kandidaten för en diskussion kring
#   etik och teknik med utgångspunkt från digitaliseringen." (117, a line of
#   its own), then ONE model paragraph, "Zeynep Tufekci lyfter fram ... som
#   bygger systemen." (118-120).
# - Part III (121-128): the head, the instruction and both titles reprinted as
#   printed; nothing under them.
# - Criteria (p5, 129-135, after Part III): "Anmärkning:" / "I del II och III
#   kommer följande kriterier att vägas in i betygssättningen:" -- Parts II AND
#   III -- then THREE criteria WITH PERCENTAGES: "– 30%." (131), "– 30%."
#   (132-133), "– 40 %." (134-135): 100 %. No "Formalia" criterion (rendered).
# SHAPES:
# - II1: graded (10b), 30/30/40 % of 30 = 9 / 9 / 12; head the criteria's own
#   lead (130); the descriptive line and the model paragraph quoted (10a).
# - III1/III2: graded (10b), 30/30/40 % of 40 = 12 / 12 / 16; the same head.
# JUDGEMENT CALLS:
# - Three criteria, not four (as 2018): whole-number marks on both totals, so
#   10b as printed. Strict "four criteria" reading: ruling F instead.
# - _PartCellNFC is draft-local (twelve lines, below): NFC is Unicode's
#   canonical composition, not a hand map (the composed and decomposed forms
#   are the same text by definition). The lead may prefer an NFC step in
#   sl_lib's PY/PARTP (it would also give the census its Part II/III totals).
# - II1's conceptId from its printed question (concept='question'): the census
#   text opens with the decomposed "(30 poäng)", which clean_question cannot
#   strip, so the census-derived id would open "poa-".
# - Questions cut from the paper's own lines (the census glues "(30 poäng)" in
#   front of II1's task and "Eller" after III1's title).
# - Reading text pp2-3 (rendered): II1 carries pages=(2, 3). The live 2019
#   cards carry [3] (flagged, P). II1's sourceMaterial label comes out "DEL II
#   (30 POÄNG)": part_head keeps the decomposed price cell (it does not read
#   it as a price); cosmetic, for the lead.
# GLYPHS: no wrong letters. The part-total cells on the paper (p4 y417, y592)
# print "poäng" as Calibri,Bold glyph 258 (U+0061 "a") followed by glyph 523
# (U+0308 COMBINING DIAERESIS, drawn over it at x505.0), rendered "ä"; every
# other "ä" on the page is glyph 263 (U+00E4). The scheme's part heads (113,
# 121) carry the same pair. Canonically equivalent to "ä", not a mangled map.
import re  # noqa: E402
import unicodedata  # noqa: E402


class _PartCellNFC:
    """A part's total printed as a cell of its own on the question paper at
    (page, y), "(30 poäng)", read as PY reads it after Unicode canonical
    composition (the SEC set this cell's "ä" as "a" + U+0308)."""
    def __init__(self, page, y):
        self.page, self.y = page, y

    def read(self, doc):
        cell = re.compile(r'^[(\[]\s*(\d{1,3})\s*(?:' + PRICE_WORD + r')\s*[)\]]$', re.I)
        hits = [unicodedata.normalize('NFC', l.text.strip()) for l in doc['lines']
                if l.page == self.page and abs(l.y - self.y) < 2]
        hits = [t for t in hits if cell.match(t)]
        if len(hits) != 1:
            raise ValueError(f'paper p{self.page} y{self.y}: {len(hits)} price cells')
        return 1, int(cell.match(hits[0]).group(1)), hits[0]


II_P_2019 = _PartCellNFC(4, 417)
III_P_2019 = _PartCellNFC(4, 592)
CRIT_2019 = crit(131, (132, 133), (134, 135))
HEAD_2019 = S(130)
ESSAY_2019 = Run('Skriv en uppsats på ungefär 300', 'nedan.')

SPECS[2019] = [
    R('II1', [graded(HEAD_2019, II_P_2019, CRIT_2019)], total=II_P_2019,
      rownote=both(quote(S(117), lead='The scheme prints'), examples(None, L(118, 120))),
      question=QP(4, 'Kommentera detta citat', Run('”Teknikfolk', 'byggt blir bra')), pages=(2, 3),
      concept='question'),
    R('III1', [graded(HEAD_2019, III_P_2019, CRIT_2019)], total=III_P_2019,
      question=QP(4, ESSAY_2019, Run('1. ”Ibland måste', 'lort.”'))),
    R('III2', [graded(HEAD_2019, III_P_2019, CRIT_2019)], total=III_P_2019,
      question=QP(4, ESSAY_2019, Run('2. Är ett sabbatsår', 'Diskutera båda'))),
]


# ====================================================================== 2021
# ====================================================================== 2021
# ================================================================ 2021 HL ===
# Drafted (small-languages lane, 20 Nov): the two open asks of this sitting,
# II1, II2 (Part II, the essay of a two-part sitting). Live: I1a-e, I2-I6 (10
# cards); not touched (audited: swedish-live-faults-2017-2026.json).
# Paper (rendered PDF pp2-4): "Besvara båda delarna: Del I och Del II." / "Alla
# svar måste vara skrivna på svenska." / "(Totalt 70 poäng)" (p2 y65-94); "Del
# I" + "(30 poäng)" (p2 y138), the instruction (y166-181), the article "Fakta
# – inte fiktion – kan bryta Pisa-förbannelsen" p2 y224 to its byline and
# source lines p3 y534-572; Q1 "(5 × 1 poäng)" on p3, Q2-Q6 on p4; "Del II" +
# "(40 poäng)" (p4 y474), "Skriv en uppsats (minst 300 ord) om ett av följande
# ämnen:" (y516), title "1." (y560) with "- John Greenleaf Whittier" (y573),
# "eller" (y616), title "2." (y660) with "- Greta Thunberg" (y674).
# PRICES:
# - II1/II2: the head's "(40 poäng)" cell (p4 x468 y474), printed with "a" +
#   U+0308 (see GLYPHS): _PartCellNFC(4, 474) (PARTP fails: the census reads
#   only Part I's total). The scheme "Del II (40 poäng)" (102).
# WHAT THE SCHEME PRINTS (rendered scheme p5 = printed page 3):
# - Part II (102-109): the head, the instruction REWORDED ("Skriv en uppsats
#   på ungefär 300 ord där du redogör för dina tankar om ett av de två ämnena
#   nedan." for the paper's "Skriv en uppsats (minst 300 ord) om ett av
#   följande ämnen:"), both titles with their attributions and "Eller";
#   nothing under them.
# - Criteria (110-116, after the titles): "Anmärkning:" / "I del II och III
#   kommer följande kriterier att vägas in i betygssättningen:" then THREE
#   criteria with NO percentages and no marks: 112, 113-114, 115-116.
# SHAPES:
# - II1/II2: ruling F: the three criteria as shown rows on the paper's 40
#   (questionTotal, whole=True), their lead and the reworded instruction quoted.
# JUDGEMENT CALLS:
# - The criteria name "del II och III" in a TWO-part sitting: read as covering
#   this Part II (the essay; the scheme prints the block under it, and its
#   wording is the three-part years'). Alternative: R4 (unprinted) quoting it.
# - Titles: reprinted as printed (the scheme sets title 2's dash as U+2010):
#   punctuation only, not quoted.
# - Questions cut from the paper's own lines: the instruction, the title and
#   its attribution line.
# - No pages: a two-part sitting's Part II is the essay (filed as Part III).
# GLYPHS: no wrong letters. The "(40 poäng)" cell (p4 y474) prints "poäng" as
# "a" + U+0308 (Calibri,Bold glyph 258 + glyph 523, as 2019), rendered "ä";
# the scheme's head (102) the same. Canonically equivalent to U+00E4.
import re  # noqa: E402
import unicodedata  # noqa: E402


class _PartCellNFC:
    """A part's total printed as a cell of its own on the question paper at
    (page, y), "(30 poäng)", read as PY reads it after Unicode canonical
    composition (the SEC set this cell's "ä" as "a" + U+0308)."""
    def __init__(self, page, y):
        self.page, self.y = page, y

    def read(self, doc):
        cell = re.compile(r'^[(\[]\s*(\d{1,3})\s*(?:' + PRICE_WORD + r')\s*[)\]]$', re.I)
        hits = [unicodedata.normalize('NFC', l.text.strip()) for l in doc['lines']
                if l.page == self.page and abs(l.y - self.y) < 2]
        hits = [t for t in hits if cell.match(t)]
        if len(hits) != 1:
            raise ValueError(f'paper p{self.page} y{self.y}: {len(hits)} price cells')
        return 1, int(cell.match(hits[0]).group(1)), hits[0]


II_P_2021 = _PartCellNFC(4, 474)
CRIT_ROWS_2021 = [shown(S(112)), shown(L(113, 114)), shown(L(115, 116))]
ESSAY_2021 = 'Skriv en uppsats (minst 300 ord)'
NOTE_2021 = both(quote(S(111), lead='The scheme prints these criteria with no marks or percentages; their lead reads'),
                 quote(L(103, 104), lead='It reprints the instruction as'))

SPECS[2021] = [
    R('II1', CRIT_ROWS_2021, whole=True, total=II_P_2021, rownote=NOTE_2021,
      question=QP(4, ESSAY_2021, '1. "Det bästa', '- John Greenleaf')),
    R('II2', CRIT_ROWS_2021, whole=True, total=II_P_2021, rownote=NOTE_2021,
      question=QP(4, ESSAY_2021, '2. ”Du kan inte', '- Greta Thunberg')),
]


# ====================================================================== 2022
# ====================================================================== 2022
# ================================================================ 2022 HL ===
# Drafted (small-languages lane, 20 Nov): the two open asks of this sitting,
# II1, II2 (Part II, the essay of a two-part sitting). Live: I1a-e, I2-I6 (10
# cards); not touched (audited: swedish-live-faults-2017-2026.json).
# Paper (rendered PDF pp2-4): the rule (p2 y51-66) and "(Totalt 70 poäng)"
# (y80); the article "Naturen har blivit svenskarnas kyrka" runs p2 y110 to
# its source lines p3 y621-633; "Del I" + "(30 poäng)" (p3 y661), Q1 "(5 × 1
# poäng)" on p3, Q2-Q6 on p4; "Del II" + "(40 poäng)" (p4 y505), "Skriv en
# uppsats på ungefär 300 ord där du redogör för dina tankar om ett av de två
# ämnena" / "nedan." (y577-592), title "1." (y635), "Eller" (y680), title "2."
# (y709).
# PRICES:
# - II1/II2: the head's "(40 poäng)" cell (p4 x468 y505), printed with "a" +
#   U+0308 (see GLYPHS): _PartCellNFC(4, 505). The scheme "Del II (40 poäng)"
#   (100).
# WHAT THE SCHEME PRINTS (rendered scheme p5 = printed page 3):
# - Part II (100-105): the head, the instruction and both titles as printed
#   (title 1 without its closing full stop) and "eller"; nothing under them.
# - Criteria (106-112, after the titles): "Anmärkning:" / "Följande kriterier
#   vägs in i betygssättningen:" (no part named) then THREE criteria with NO
#   percentages and no marks: 108, 109-110, 111-112; then "(Totalt 70 poäng)"
#   (113).
# SHAPES:
# - II1/II2: ruling F: the three criteria as shown rows on the paper's 40
#   (questionTotal, whole=True), their lead quoted.
# JUDGEMENT CALLS:
# - The criteria name no part and are printed under the essay, the only
#   written part: read as covering it. Alternative: R4 (unprinted) quoting it.
# - Questions cut from the paper's own lines (the census leaves "Eller" off
#   only because it is a cell of its own; the instruction is not in its text).
# - No pages: a two-part sitting's Part II is the essay (filed as Part III).
# GLYPHS: no wrong letters. The "(40 poäng)" cell (p4 y505) prints "poäng" as
# "a" + U+0308, rendered "ä" (as 2019); the scheme's head (100) the same.
import re  # noqa: E402
import unicodedata  # noqa: E402


class _PartCellNFC:
    """A part's total printed as a cell of its own on the question paper at
    (page, y), "(30 poäng)", read as PY reads it after Unicode canonical
    composition (the SEC set this cell's "ä" as "a" + U+0308)."""
    def __init__(self, page, y):
        self.page, self.y = page, y

    def read(self, doc):
        cell = re.compile(r'^[(\[]\s*(\d{1,3})\s*(?:' + PRICE_WORD + r')\s*[)\]]$', re.I)
        hits = [unicodedata.normalize('NFC', l.text.strip()) for l in doc['lines']
                if l.page == self.page and abs(l.y - self.y) < 2]
        hits = [t for t in hits if cell.match(t)]
        if len(hits) != 1:
            raise ValueError(f'paper p{self.page} y{self.y}: {len(hits)} price cells')
        return 1, int(cell.match(hits[0]).group(1)), hits[0]


II_P_2022 = _PartCellNFC(4, 505)
CRIT_ROWS_2022 = [shown(S(108)), shown(L(109, 110)), shown(L(111, 112))]
ESSAY_2022 = Run('Skriv en uppsats på ungefär 300', 'nedan.')
NOTE_2022 = quote(S(107), lead='The scheme prints these criteria with no marks or percentages; their lead reads')

SPECS[2022] = [
    R('II1', CRIT_ROWS_2022, whole=True, total=II_P_2022, rownote=NOTE_2022,
      question=QP(4, ESSAY_2022, '1. “Djuren')),
    R('II2', CRIT_ROWS_2022, whole=True, total=II_P_2022, rownote=NOTE_2022,
      question=QP(4, ESSAY_2022, '2. Hur sann')),
]


# ====================================================================== 2023
# ====================================================================== 2023
# ================================================================ 2023 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched (audited:
# swedish-live-faults-2017-2026.json).
# Paper (rendered PDF pp2-4): the rule (p2 y51-66) and "(Totalt 100 poäng)"
# (y80); the article "Svenska kyrkan ber om ursäkt för övergrepp mot samerna.
# Men hur bearbetar vi det som skett?" runs p2 y110 to its source lines "- Ur
# artikeln ... den 19 februari 2022." / "Texten har redigerats ..." p3
# y504-528; "Del I" + "(30 poäng)" (p3 y583), Q1 "(5 × 1 poäng)" on p3, Q2-Q6
# on p4; "Del II" + "(30 poäng)" (p4 y432), "Kommentera detta citat och
# uttryck dina tankar med 100 - 150 ord:" (y461) and the quotation (y505-520);
# "Del III" + "(40 poäng)" (p4 y593), the instruction (y622-637), title "1."
# (y681), "eller" (y725), title "2." (y754).
# PRICES:
# - II1: the head's "(30 poäng)" cell (p4 x454 y432); III1/III2: "(40 poäng)"
#   (p4 x454 y593). Both print "poäng" with "a" + U+0308 (see GLYPHS):
#   _PartCellNFC. The scheme "Del II (30 poäng)" (104), "Del III (40 poäng)"
#   (114).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3):
# - Part II (104-107): the head, the task REWORDED ("... med ungefär 100 ord:"
#   for the paper's "... med 100 - 150 ord:") and the quotation; then ONE
#   paragraph of indicative content, "Kandidaten kan föra en diskussion kring
#   ... vad han eller hon inte tror går i arv." (108-113).
# - Part III (114-121): the head, the instruction and both titles reprinted
#   (attributions on lines of their own); nothing under them.
# - Criteria (p5, 122-129, after Part III): "Anmärkning:" / "I del I och II
#   kommer följande kriterier att vägas in i betygssättningen:" -- Parts I AND
#   II, not Part III -- then four criteria WITH PERCENTAGES: "– 30%." (124),
#   "– 30%." (125-126), "– 30 %." (127-128), "– 10%." (129): 100 %.
# SHAPES:
# - II1: graded (10b), 9 / 9 / 9 / 3 of 30; head the criteria's own lead
#   (123); the content paragraph quoted as an example (10a) and the reworded
#   task quoted (10f).
# - III1/III2: nothing printed for this part, criteria stated for parts I and
#   II only: R4 (unprinted) at the paper's 40, the note saying what the scheme
#   prints.
# JUDGEMENT CALLS:
# - Criteria read as NOT covering Part III ("I del I och II", as 2017 and the
#   sibling 2010-2016 drafts). Alternative: III1/III2 graded(HEAD_2023,
#   III_P_2023, CRIT_2023) (12/12/12/4).
# - II1's conceptId from its printed question (concept='question'): the census
#   text opens with the decomposed "(30 poäng)", which clean_question cannot
#   strip, so the census-derived id would open "poa-".
# - Questions cut from the paper's own lines (the census glues "(30 poäng)" in
#   front of II1's task).
# - Reading text pp2-3 (rendered): II1 carries pages=(2, 3). The live 2023
#   cards carry [3] (flagged, P). II1's sourceMaterial label comes out "DEL II
#   (30 POÄNG)" (part_head keeps the decomposed price cell): cosmetic.
# GLYPHS: no wrong letters. The part-total cells (p4 y432, y593) print
# "poäng" as "a" + U+0308 COMBINING DIAERESIS (glyph 523, here a span of its
# own in Calibri at x491.0), rendered "ä"; elsewhere "ä" is glyph 263
# (U+00E4). The scheme's part heads (104, 114) the same. The scheme sets its
# words in no-break spaces (U+00A0, read as spaces by S()).
import re  # noqa: E402
import unicodedata  # noqa: E402


class _PartCellNFC:
    """A part's total printed as a cell of its own on the question paper at
    (page, y), "(30 poäng)", read as PY reads it after Unicode canonical
    composition (the SEC set this cell's "ä" as "a" + U+0308)."""
    def __init__(self, page, y):
        self.page, self.y = page, y

    def read(self, doc):
        cell = re.compile(r'^[(\[]\s*(\d{1,3})\s*(?:' + PRICE_WORD + r')\s*[)\]]$', re.I)
        hits = [unicodedata.normalize('NFC', l.text.strip()) for l in doc['lines']
                if l.page == self.page and abs(l.y - self.y) < 2]
        hits = [t for t in hits if cell.match(t)]
        if len(hits) != 1:
            raise ValueError(f'paper p{self.page} y{self.y}: {len(hits)} price cells')
        return 1, int(cell.match(hits[0]).group(1)), hits[0]


II_P_2023 = _PartCellNFC(4, 432)
III_P_2023 = _PartCellNFC(4, 593)
CRIT_2023 = crit(124, (125, 126), (127, 128), 129)
HEAD_2023 = S(123)
ESSAY_2023 = Run('Skriv en uppsats på ungefär 300', 'nedan.')


def _part3_note_2023(d):
    return (f'Under “{S(114).text(d)}” the scheme reprints only the instruction and the two titles; it prints no '
            f'answer, no content and no criteria for this part. Its criteria, printed after the titles, are '
            f'stated for parts I and II only: “{S(123).text(d)}”')


SPECS[2023] = [
    R('II1', [graded(HEAD_2023, II_P_2023, CRIT_2023)], total=II_P_2023,
      rownote=both(examples(None, L(108, 113)), quote(S(105), lead='It reprints the task as')),
      question=QP(4, 'Kommentera detta citat', Run('”–När jag började', 'jag egentligen')), pages=(2, 3),
      concept='question'),
    R('III1', [unprinted(_part3_note_2023)], total=III_P_2023,
      question=QP(4, ESSAY_2023, '1. ”Utan förlåtelse')),
    R('III2', [unprinted(_part3_note_2023)], total=III_P_2023,
      question=QP(4, ESSAY_2023, '2. ”En hungrig')),
]


# ====================================================================== 2024
# ====================================================================== 2024
# ================================================================ 2024 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched (audited:
# swedish-live-faults-2017-2026.json).
# Paper (rendered PDF pp2-4): the rule (p2 y65-80) and "(Totalt 100 poäng)"
# (y94); an introduction (p2 y124-168) and the article by Lars Trägårdh to its
# source lines "Ur artikeln ”Lagar genomsyras av värderingar” ..." p3
# y475-505; "Del I" + "(30 poäng)" (p3 y563), Q1 "(5 × 1 poäng)" on p3, Q2-Q6
# on p4; "Del II" + "(30 poäng)" (p4 y417), "Kommentera detta citat och
# uttryck dina tankar med 100 - 150 ord:" (y446) and the quotation (y475);
# "Del III" + "(40 poäng)" (p4 y549), the instruction (y578-592), title "1."
# (y635), "eller" (y680), title "2." (y724).
# PRICES:
# - II1: the head's "(30 poäng)" cell (p4 x454 y417); III1/III2: "(40 poäng)"
#   (p4 x454 y549). Both print "poäng" with "a" + U+0308 (see GLYPHS):
#   _PartCellNFC. The scheme "Del II (30 poäng)" (96), "Del III (40 poäng)"
#   (108).
# WHAT THE SCHEME PRINTS (rendered scheme pp3-5 = printed pages 1-3):
# - Part II (96-98): the head, the task REWORDED ("... med ungefär 100 ord:"
#   for the paper's "... med 100 - 150 ord:") and the quotation reprinted
#   differently ("”att ”dela svensk kultur”( är) inte på något sätt oviktig
#   ..." for the paper's "”... att ”dela svensk kultur” [är] inte på något sätt
#   oviktigt ..."); then three printed paragraphs, each set off by space
#   (rendered p4): "Kandidaten utgår från citatet och uttrycker tydligt sin
#   åsikt/ sina åsikter." (99), "Kandidaten kan diskutera vad hen tycker är
#   svensk kultur och vad begreppet svensk betyder." (100), "Kandidaten kan
#   utgå från sig själv ... som Lars Trägårdh refererar till." (101-103).
# - Part III (108-115): the head, the instruction and both titles reprinted
#   (attributions on lines of their own, without brackets); nothing under them.
# - Criteria (p5, 116-122, after Part III): "Följande kriterier vägs in i
#   betygssättningen:" -- NO part named -- then four criteria WITH
#   PERCENTAGES: "– 30%." (117), "– 30%." (118-119), "– 30 %." (120-121), "–
#   10%." (122): 100 %.
# SHAPES:
# - II1: graded (10b), 9 / 9 / 9 / 3 of 30; head the criteria's own lead
#   (116); the first paragraph quoted as the scheme's descriptive line, the
#   other two as examples (10a); the reworded task and quotation quoted (10f).
# - III1/III2: graded (10b), 12 / 12 / 12 / 4 of 40; the same head.
# JUDGEMENT CALLS:
# - Criteria read as covering Parts II AND III: this year's lead names no part
#   ("Följande kriterier vägs in i betygssättningen:"), unlike 2017/2023's "I
#   del I och II". If the lead reads an unnamed block as the essay's only:
#   II1 becomes [shown(S(100)), shown(L(101, 103))], whole=True on 30 with
#   S(99) quoted (10a).
# - II1's conceptId from its printed question (concept='question'): the census
#   text opens with the decomposed "(30 poäng)", which clean_question cannot
#   strip, so the census-derived id would open "poa-".
# - Questions cut from the paper's own lines (the census glues "(30 poäng)" in
#   front of II1's task).
# - Reading text pp2-3 (rendered): II1 carries pages=(2, 3). The live 2024
#   cards carry [3] (flagged, P). II1's sourceMaterial label comes out "DEL II
#   (30 POÄNG)": cosmetic.
# GLYPHS: no wrong letters. The part-total cells (p4 y417, y549) print
# "poäng" as "a" + U+0308, rendered "ä" (as 2019, 2023); the scheme's heads
# (96, 108) the same. The scheme sets its words in no-break spaces.
import re  # noqa: E402
import unicodedata  # noqa: E402


class _PartCellNFC:
    """A part's total printed as a cell of its own on the question paper at
    (page, y), "(30 poäng)", read as PY reads it after Unicode canonical
    composition (the SEC set this cell's "ä" as "a" + U+0308)."""
    def __init__(self, page, y):
        self.page, self.y = page, y

    def read(self, doc):
        cell = re.compile(r'^[(\[]\s*(\d{1,3})\s*(?:' + PRICE_WORD + r')\s*[)\]]$', re.I)
        hits = [unicodedata.normalize('NFC', l.text.strip()) for l in doc['lines']
                if l.page == self.page and abs(l.y - self.y) < 2]
        hits = [t for t in hits if cell.match(t)]
        if len(hits) != 1:
            raise ValueError(f'paper p{self.page} y{self.y}: {len(hits)} price cells')
        return 1, int(cell.match(hits[0]).group(1)), hits[0]


II_P_2024 = _PartCellNFC(4, 417)
III_P_2024 = _PartCellNFC(4, 549)
CRIT_2024 = crit(117, (118, 119), (120, 121), 122)
HEAD_2024 = S(116)
ESSAY_2024 = Run('Skriv en uppsats på ungefär 300', 'nedan.')

SPECS[2024] = [
    R('II1', [graded(HEAD_2024, II_P_2024, CRIT_2024)], total=II_P_2024,
      rownote=both(quote(S(99), lead='The scheme prints'), examples(None, S(100), L(101, 103)),
                   quote(S(97), S(98), lead='It reprints the task and the quotation as')),
      question=QP(4, 'Kommentera detta citat', '”... att ”dela'), pages=(2, 3),
      concept='question'),
    R('III1', [graded(HEAD_2024, III_P_2024, CRIT_2024)], total=III_P_2024,
      question=QP(4, ESSAY_2024, '1. ”Får man')),
    R('III2', [graded(HEAD_2024, III_P_2024, CRIT_2024)], total=III_P_2024,
      question=QP(4, ESSAY_2024, '2. ”Undvik krig')),
]


# ====================================================================== 2025
# ====================================================================== 2025
# ================================================================ 2025 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched (audited:
# swedish-live-faults-2017-2026.json).
# Paper (rendered PDF pp2-4): the rule (p2 y65-80) and "(Totalt 100 poäng)"
# (y94); the article "Därför blir protesterna allt hårdare" runs p2 y124 to its
# source lines "Ur artikeln ... forskning.se, 2023/06/13, ..." p3 y547-572;
# "Del I (30 poäng)" (p3 y629, one line), Q1 "(5 × 1 poäng)" on p3, Q2-Q6 on
# p4; "Del II" + "(30 poäng)" (p4 y431), "Kommentera detta citat och uttryck
# dina tankar med 100 - 150 ord:" (y461) and the quotation (y490); "Del III" +
# "(40 poäng)" (p4 y563), the instruction (y592-607), title "1." (y635-651)
# with "(Laleh)" (y664) and its footnote "*David och Goliat är en berättelse
# ..." (y691), "eller" (y719), title "2." (y749).
# PRICES:
# - II1: the head's "(30 poäng)" cell (p4 x454 y431); III1/III2: "(40 poäng)"
#   (p4 x454 y563). Both print "poäng" with "a" + U+0308 (see GLYPHS):
#   _PartCellNFC (the census reads no part total at all this sitting). The
#   scheme "Del II (30 poäng)" (118), "Del III (40 poäng)" (124).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-6 = printed pages 4-6; p3 the
# annotations table, pp7-8 blank):
# - Part II (118-120): the head, the task and the quotation as printed; then
#   one descriptive line, "Kandidaten utgår från citatet och uttrycker tydligt
#   sin åsikt/ sina åsikter." (121, a line of its own), and one paragraph,
#   "Kandidaten kan utgå från artikeln men hen kan också ta egna exempel. Hen
#   kan eventuellt göra en jämförelse med ett annat ämne hen tycker är
#   speciellt." (122-123).
# - Part III (124-133): the head, the instruction and both titles reprinted,
#   title 1's footnote included; nothing under them.
# - NO criteria anywhere in this scheme (rendered pp4-6).
# SHAPES:
# - II1: the paragraph shown, whole=True on the paper's 30 (10a, indicative
#   content), the descriptive line quoted (as Danish 2013's II1).
# - III1/III2: nothing printed: R4 (unprinted) at the paper's 40.
# JUDGEMENT CALLS:
# - II1's paragraph is thin indicative content (use the article or own
#   examples; compare with another topic): read as 10a content, not as a
#   second descriptive line. If the lead reads both lines as descriptive only:
#   R('II1', [unprinted(quote(S(121), L(122, 123)))], total=II_P_2025, ...).
# - III1's question: the instruction, the title's two printed lines, its
#   attribution "(Laleh)" and its footnote, all printed as title 1.
# - II1's conceptId from its printed question (concept='question'): the census
#   text opens with the decomposed "(30 poäng)", which clean_question cannot
#   strip, so the census-derived id would open "poa-".
# - Questions cut from the paper's own lines (the census glues "(30 poäng)" in
#   front of II1's task).
# - Reading text pp2-3 (rendered): II1 carries pages=(2, 3). The live 2025
#   cards carry NO sourceMaterial (flagged, P). II1's sourceMaterial label
#   comes out "DEL II (30 POÄNG)": cosmetic.
# GLYPHS: no wrong letters. The part-total cells (p4 y431, y563) print
# "poäng" as "a" + U+0308, rendered "ä" (as 2019); the scheme's heads (118,
# 124) the same.
import re  # noqa: E402
import unicodedata  # noqa: E402


class _PartCellNFC:
    """A part's total printed as a cell of its own on the question paper at
    (page, y), "(30 poäng)", read as PY reads it after Unicode canonical
    composition (the SEC set this cell's "ä" as "a" + U+0308)."""
    def __init__(self, page, y):
        self.page, self.y = page, y

    def read(self, doc):
        cell = re.compile(r'^[(\[]\s*(\d{1,3})\s*(?:' + PRICE_WORD + r')\s*[)\]]$', re.I)
        hits = [unicodedata.normalize('NFC', l.text.strip()) for l in doc['lines']
                if l.page == self.page and abs(l.y - self.y) < 2]
        hits = [t for t in hits if cell.match(t)]
        if len(hits) != 1:
            raise ValueError(f'paper p{self.page} y{self.y}: {len(hits)} price cells')
        return 1, int(cell.match(hits[0]).group(1)), hits[0]


II_P_2025 = _PartCellNFC(4, 431)
III_P_2025 = _PartCellNFC(4, 563)
ESSAY_2025 = Run('Skriv en uppsats på minst 300', 'nedan.')


def _part3_note_2025(d):
    return (f'Under “{S(124).text(d)}” the scheme reprints only the instruction and the two titles; it prints no '
            f'answer, no content and no criteria for this part (and no criteria anywhere in this scheme).')


SPECS[2025] = [
    R('II1', [shown(L(122, 123))], whole=True, total=II_P_2025,
      rownote=quote(S(121), lead='The scheme prints'),
      question=QP(4, 'Kommentera detta citat', '”Jag tycker att klimat'), pages=(2, 3),
      concept='question'),
    R('III1', [unprinted(_part3_note_2025)], total=III_P_2025,
      question=QP(4, ESSAY_2025, Run('1. ”Vi ska ta över', 'göra vattnet rent'), '(Laleh)', '*David och Goliat')),
    R('III2', [unprinted(_part3_note_2025)], total=III_P_2025,
      question=QP(4, ESSAY_2025, '2. ”Man säger')),
]


# ====================================================================== 2026
# ====================================================================== 2026
# ================================================================ 2026 HL ===
# Drafted (small-languages lane, 20 Nov): the three open asks of this sitting,
# II1, III1, III2. Live: I1a-e, I2-I6 (10 cards); not touched (audited:
# swedish-live-faults-2017-2026.json).
# Paper (rendered PDF pp2-4): the rule (p2 y65-80) and "(Totalt 100 poäng)"
# (y109); the article "Överraskande fynd på Bali – nomaderna är inga glidare"
# runs p2 y138 to its source lines "Ur artikeln ... Svenska Dagbladet, den 22"
# / "september 2023. ..." p3 y474-498; "Del I" + "(30 poäng)" (p3 y570), Q1
# "(5 × 1 poäng)" on p3, Q2-Q6 on p4; "Del II" + "(30 poäng)" (p4 y373),
# "Kommentera detta citat och uttryck dina tankar med 100 - 150 ord:" (y402)
# and the quotation (y446-461); "Del III" + "(40 poäng)" (p4 y534), the
# instruction "Skriv en uppsats på minst 300 ord ..." (y578-592), title "1."
# (y635), "eller" (y680), title "2." (y724-739).
# PRICES:
# - II1: the head's "(30 poäng)" cell (p4 x454 y373); III1/III2: "(40 poäng)"
#   (p4 x454 y534). Both print "poäng" with "a" + U+0308 (see GLYPHS):
#   _PartCellNFC. The scheme "Del II (30 poäng)" (125), "Del III (40 poäng)"
#   (134).
# WHAT THE SCHEME PRINTS (rendered scheme pp4-6 = printed pages 4-6; p3 the
# annotations table, pp7-8 blank):
# - Part II (125-128): the head, the task REWORDED ("... med ungefär 100 ord:"
#   for the paper's "... med 100 - 150 ord:") and the quotation; then ONE
#   paragraph of indicative content, "Kandidaten kan t.ex. utgå från egna
#   erfarenheter ... diskutera just ämnet digitala nomader." (129-133).
# - Part III (134-140): the head, the instruction REWORDED ("Skriv en uppsats
#   på ungefär 300 ord ..." for the paper's "... på minst 300 ord ...") and
#   both titles as printed; nothing under them.
# - NO criteria anywhere in this scheme (rendered pp4-6).
# SHAPES:
# - II1: the paragraph shown, whole=True on the paper's 30 (10a), the reworded
#   task quoted (10f).
# - III1/III2: nothing printed: R4 (unprinted) at the paper's 40, the reworded
#   instruction quoted (10f).
# JUDGEMENT CALLS:
# - II1: one row, not split at its sentences: the scheme prints one paragraph.
# - II1's conceptId from its printed question (concept='question'): the census
#   text opens with the decomposed "(30 poäng)", which clean_question cannot
#   strip, so the census-derived id would open "poa-".
# - Questions cut from the paper's own lines (the census glues "(30 poäng)" in
#   front of II1's task).
# - Reading text pp2-3 (rendered): II1 carries pages=(2, 3). The live 2026
#   cards carry [3] (flagged, P). II1's sourceMaterial label comes out "DEL II
#   (30 POÄNG)": cosmetic.
# GLYPHS: no wrong letters. The part-total cells (p4 y373, y534) print
# "poäng" as "a" + U+0308, rendered "ä" (as 2019); the scheme's heads (125,
# 134) the same.
import re  # noqa: E402
import unicodedata  # noqa: E402


class _PartCellNFC:
    """A part's total printed as a cell of its own on the question paper at
    (page, y), "(30 poäng)", read as PY reads it after Unicode canonical
    composition (the SEC set this cell's "ä" as "a" + U+0308)."""
    def __init__(self, page, y):
        self.page, self.y = page, y

    def read(self, doc):
        cell = re.compile(r'^[(\[]\s*(\d{1,3})\s*(?:' + PRICE_WORD + r')\s*[)\]]$', re.I)
        hits = [unicodedata.normalize('NFC', l.text.strip()) for l in doc['lines']
                if l.page == self.page and abs(l.y - self.y) < 2]
        hits = [t for t in hits if cell.match(t)]
        if len(hits) != 1:
            raise ValueError(f'paper p{self.page} y{self.y}: {len(hits)} price cells')
        return 1, int(cell.match(hits[0]).group(1)), hits[0]


II_P_2026 = _PartCellNFC(4, 373)
III_P_2026 = _PartCellNFC(4, 534)
ESSAY_2026 = Run('Skriv en uppsats på minst 300', 'nedan.')


def _part3_note_2026(d):
    return (f'Under “{S(134).text(d)}” the scheme reprints the instruction, as “{L(135, 136).text(d)}”, and the '
            f'two titles; it prints no answer, no content and no criteria for this part (and no criteria anywhere '
            f'in this scheme).')


SPECS[2026] = [
    R('II1', [shown(L(129, 133))], whole=True, total=II_P_2026,
      rownote=quote(S(126), lead='The scheme reprints the task as'),
      question=QP(4, 'Kommentera detta citat', Run('”De flesta teorier', 'geografiska plats')), pages=(2, 3),
      concept='question'),
    R('III1', [unprinted(_part3_note_2026)], total=III_P_2026,
      question=QP(4, ESSAY_2026, '1. ”Lust gör')),
    R('III2', [unprinted(_part3_note_2026)], total=III_P_2026,
      question=QP(4, ESSAY_2026, Run('2. ”Om kärleken', 'meningslöst av samma'))),
]
