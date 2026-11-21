#!/usr/bin/env python3
"""Reviewed specs for the Maltese classic examination (small-languages lane).

One entry per printed ask with no live card; see sl_lib.py for the selector
language. Line numbers are lines of examiner-reports/maltese/schemes/<year>-hl.md.
Drafted by an Opus helper on the Romanian and Dutch models, integrated and gated
by the lane lead.
"""
from sl_lib import (R, S, SR, J, L, PL, PC, QP, QL, Run, pre, prerun, PP, SP, PY, RX, PaperP, PARTP,  # noqa: F401
                    one, shown, graded, crit, examples, quote, unprinted, part, NoScheme)
from pl_listen_lib import Join  # noqa: F401

SPECS = {}


def both(*notes):
    """Several printed notes on one row, in order."""
    return lambda doc: ' '.join(n(doc) for n in notes)


# ================================================================ 2018 HL ===
# Drafted (small-languages lane, 20 Nov): the 10 asks with no live card.
# Live: I2, I3, I6. Open: I1a-e (I1ċ), I4, I5. Excluded: II1, III1, III2.
# Paper (rendered pp2-4): Taqsima I "30 marka" (p2, no brackets); Q1 prints
# "( 5 × 1 marka)" beside its head line (p3 y617, a cell of its own) over five
# expressions a) b) ċ) d) e): a price per expression, so Q1 is carded letter by
# letter at 1 each. The census reads NO price for I1a-e (tariff None), so each
# is priced from that printed cell (PaperP), card total included. Q2-Q6 "(5
# marki)" each (Q4's on p4 y194, read by the census). Taqsima II "(30 marka)",
# Taqsima III "(40 marka)" (p4, PARTP), two titles joined by "jew".
# Scheme (rendered pp3-6): p3 "Taqsima I", Q1 reprints each expression with its
# answer in bold on the line below (a)-e) in the paper's order and words): one
# row each at 1. Above Q4's answer the scheme prints "(It-tweġibiet
# għall-mistoqsijiet 4, 5, 6 jeħtieġu r-rispons tal-kandidat. It-tweġibiet hawn
# taħt huma eżempji.)" (the answers to 4, 5, 6 need the candidate's own
# response; those below are examples): Q4 and Q5 are therefore shown, priced
# as a whole (10a), that line quoted. Q5 prints two answers split by " / ": two
# shown rows. p4 ends after Q6; p5 is BLANK and p6 is the back cover
# (rendered): the scheme prints NOTHING for Taqsima II or III, not even the
# tasks, so II1, III1, III2 take R4 at the paper's 30 and 40 with that said.
# Judgement calls:
# - Rows cut to the bold answer line only (the Romanian model), not
#   "expression: answer" as the live cards of other sittings print.
# - Q5's second answer wraps "għall-" / "kunċett": joined with no space (the
#   article hyphen), via _Wrapped below (provenance unaffected: normalise drops
#   spaces and hyphens).
# - The scheme reprints Q5 as "jiċċaqalqu" (paper "jiċċaqilqu"): spelling only,
#   not quoted.
# - Live I6 is a single 5-mark point row although the same "examples" line
#   covers Q6; not touched here, flagged for the lead.
# - Reading text pp2-3 (title "Fruntieri" p2 y165 to the source line p3 y577;
#   questions from p3 y604), as the live 2018 cards.
# No glyph problems.
import re as _re
from pl_listen_lib import Join as _Join


class _Wrapped(_Join):
    """Printed lines joined as the SEC wrapped them: a line broken right after
    a word's hyphen (the Maltese article, "għall-" / "kunċett") runs on into
    the next with no space; any other break is a space."""
    def text(self, doc):
        out = ''
        for p in self.parts:
            t = p.text(doc)
            out = f'{out}{t}' if _re.search(r'\w[-‐/]$', out) else (f'{out} {t}' if out else t)
        return _re.sub(r'\s+', ' ', out).strip()


def LH(a, b=None, after=None, before=None):
    """Scheme lines a..b as L() cuts them, joined as _Wrapped joins them."""
    if b is None or b == a:
        return S(a, after=after, before=before)
    return _Wrapped(*([S(a, after=after)] + [S(n) for n in range(a + 1, b)] + [S(b, before=before)]))


Q1P_2018 = PaperP(3, '( 5 × 1 marka)')
EXAMPLES_2018 = L(70, 71)
NOTHING_2018 = 'The scheme prints answers for Part I only and nothing for this part.'
ESSAY_2018 = 'Agħżel mistoqsija waħda'
SPECS[2018] = [
    R('I1a', [one(S(50), Q1P_2018)], total=Q1P_2018),
    R('I1b', [one(S(52), Q1P_2018)], total=Q1P_2018),
    R('I1ċ', [one(S(54), Q1P_2018)], total=Q1P_2018),
    R('I1d', [one(S(56), Q1P_2018)], total=Q1P_2018),
    R('I1e', [one(S(58), Q1P_2018)], total=Q1P_2018),
    R('I4', [shown(LH(72, 74))], whole=True,
      rownote=quote(EXAMPLES_2018, lead='The scheme prints above this answer')),
    R('I5', [shown(LH(80, 81, before=' / ')), shown(LH(81, 82, after='/ '))], whole=True,
      rownote=quote(EXAMPLES_2018, lead='The scheme prints above its answer to Question 4')),
    R('II1', [unprinted(NOTHING_2018)]),
    R('III1', [unprinted(NOTHING_2018)],
      question=QP(4, ESSAY_2018, Run('1. Nistgħu', 'tgħix bla fruntieri?'))),
    R('III2', [unprinted(NOTHING_2018)],
      question=QP(4, ESSAY_2018, Run('2. ”L-ilbies', 'tiegħek f’komponiment'))),
]
for _s in SPECS[2018]:
    if _re.match(r'^(I|II)\d', _s.key):
        _s.pages = (2, 3)


# ================================================================ 2019 HL ===
# Drafted (small-languages lane, 20 Nov): the 7 asks with no live card.
# Live: I1a-e (I1ċ). Open: I2, I3, I4, I5. Excluded: II1, III1, III2.
# Paper (rendered pp2-4): L-Ewwel Taqsima "30 marka"; Q1 "(5 × 1 marka)" beside
# e) (live). Then SIX questions at "(5 marki)" each, but the paper numbers only
# five of them: the first question on p4 (y65, "X’tgħallem dwar l-aspett fiżiku
# tal-isport David Stellini mingħand l-għalliem tiegħu u kif ħa tagħlima
# għall-ħajja minn dan?", "(5 marki)" at y80) is printed with NO number, and the
# next ones are numbered 2. to 5. Part I reaches its printed 30 only with it
# (Q1 5 + this 5 + Q2-Q5 4 x 5). The census reads the numbered ones as I2-I5
# and has NO ask for the unnumbered one.
# Scheme (rendered pp3-4): numbers the six questions 1-6, reprinting each with
# the paper's words: its 2 is the paper's unnumbered question, its 3-6 are the
# paper's 2-5. Paired by WORDS, not number: census I2 "Kif jara r-rwol" =
# scheme 3; I3 "Essenzjalment" = 4; I4 "Nitkellmu" = 5; I5 "Sina Buġeja" = 6.
# THIS is the census flag "scheme Q6 with no paper ask": the scheme's 6 is the
# paper's 5, and the paper's unnumbered question is the ask with no census key.
# NOT CARDED (needs a census key first; lead's call): the unnumbered question.
# Its spec, ready once the census gives it a key:
#   R('<key>', [one(LH(55, 59, before=' (P2)'), PY(4, 80))], total=PY(4, 80),
#     question=QP(4, Run('X’tgħallem dwar', 'tagħlima għall-ħajja')),
#     rownote=quote(S(59, after='mill-esperjenza. '), lead='The scheme ends its answer with'))
# Shapes: scheme 3 and 4 print one model paragraph each -> one row at 5 (as the
# live 2018 Q2/Q3 and Romanian 2012 Q5). Scheme 5 prints three bullets with no
# split, scheme 6 four bullets under "Xi punti li jistgħu jissemmew:" (some
# points that may be mentioned) -> shown, priced as a whole (10a).
# Taqsima II: the exclusion says the scheme prints nothing; it is WRONG. Under
# the reprinted task (p4) the scheme prints "Xi punti li jistgħu jissemmew:" and
# six bold-italic paragraphs of points, no marks: shown under the paper's 30
# (10a; as Dutch 2015 Deel 2). Taqsima III: the two titles reprinted as the
# paper prints them and nothing under them (p4; p5 blank): R4 at the paper's 40.
# The paper prints no instruction over Part III's titles (only "It-Tielet
# Taqsima (40 marka)").
# Judgement calls:
# - Scheme 3 and 2 end their paragraph with "(P3)" / "(P2)" (the paragraph of
#   the text the answer rests on): cut from the row, quoted in the note.
# - Scheme 5 reprints the paper's "spjega kif l-isport jista’ jgħin biex
#   jiġġieled kontra l-korruzzjoni" as "... jikkumbati kontra l-korruzzjoni":
#   a word changed, so the paper wins and the scheme's line is quoted (10f).
#   Spelling-only differences not quoted: "jbiegħdhom" (paper "jbegħedhom"),
#   Part II "l-impossibli" / "f-din" (paper "l-impossibbli" / "f’din").
# - Lines broken after an article hyphen ("l-" / "importanti", "it-" / "tip")
#   are joined with no space (_Wrapped).
# - Reading text pp2-3 (David Stellini's article p2, Sina Bugeja's p3 to the
#   source line y574), as the live 2019 cards.
# No glyph problems.
import re as _re
from pl_listen_lib import Join as _Join


class _Wrapped(_Join):
    """Printed lines joined as the SEC wrapped them: a line broken right after
    a word's hyphen (the Maltese article, "l-" / "importanti") runs on into the
    next with no space; any other break is a space."""
    def text(self, doc):
        out = ''
        for p in self.parts:
            t = p.text(doc)
            out = f'{out}{t}' if _re.search(r'\w[-‐/]$', out) else (f'{out} {t}' if out else t)
        return _re.sub(r'\s+', ' ', out).strip()


def LH(a, b=None, after=None, before=None):
    """Scheme lines a..b as L() cuts them, joined as _Wrapped joins them."""
    if b is None or b == a:
        return S(a, after=after, before=before)
    return _Wrapped(*([S(a, after=after)] + [S(n) for n in range(a + 1, b)] + [S(b, before=before)]))


def QW(page, *openings):
    """The question cut from the paper's own lines (each opening names one),
    joined as _Wrapped joins them, its number taken off: the census joins a
    line broken after "għaż-" with a space ("għaż- żewġ")."""
    from sl_lib import MARKER as _M, clean_question as _cq
    return lambda doc, _q: _cq(_M.sub('', _Wrapped(*[PL(page, o) for o in openings]).text(doc), count=1))


def _numbered(n):
    return (f'The scheme numbers this question {n}: the paper prints its second question (top of p4) '
            f'with no number and numbers this one {n - 1}.')


# The unnumbered question (coordinator ruling A, 20 Nov): a census leaf of its
# own (paper_census.ADDED_ASKS), cited "Section I Q1A", priced from the paper's
# "(5 marki)" cell beside its last line (p4 y80); the note in plain words, as
# ruled.
UNNUMBERED_2019 = ('The paper prints this question without a number, between Questions 1 and 2; '
                   'the marking scheme calls it Question 2.')
SPECS[2019] = [
    R('I1A', [one(LH(55, 59, before=' (P2)'), PY(4, 80))], total=PY(4, 80),
      note='The paper prints this question with no number; the census keys it Section I Q1A (ADDED_ASKS).',
      question=QP(4, Run('X’tgħallem dwar', 'tagħlima għall-ħajja')),
      rownote=both(lambda d: UNNUMBERED_2019,
                   quote(S(59, after='mill-esperjenza. '), lead='The scheme ends its answer with'))),
    R('I2', [one(LH(61, 64, before=' (P3)'), PP())], note=_numbered(3),
      rownote=quote(S(64, after='mal-ħajja. '), lead='The scheme ends its answer with')),
    R('I3', [one(LH(67, 70), PP())], note=_numbered(4)),
    R('I4', [shown(S(76)), shown(S(77)), shown(S(78))], whole=True, note=_numbered(5),
      rownote=quote(LH(74, 75, before=' (5 marki)'), lead='The scheme reprints the last line of the question as')),
    R('I5', [shown(LH(87, 88)), shown(LH(89, 90)), shown(S(91)), shown(LH(92, 93))], whole=True,
      note=_numbered(6), rownote=quote(S(86), lead='The scheme heads its points'),
      question=QW(4, '5. Sina Buġeja', 'sforz li bih', 'żewġ artikli')),
    R('II1', [shown(LH(99, 100)), shown(LH(101, 102)), shown(S(103)), shown(S(104)), shown(LH(105, 106)),
              shown(LH(107, 108))], whole=True,
      rownote=quote(S(98), lead='The scheme heads its points'),
      question=QW(4, '“Imma l-isport', 'Minn dak li qrajt', 'ħajja f’madwar')),
    R('III1', [unprinted('The scheme reprints the two titles and prints nothing under them.')],
      question=QP(4, Run('1. ‘L-ewwel jien', 'l-opinjoni tiegħek'))),
    R('III2', [unprinted('The scheme reprints the two titles and prints nothing under them.')],
      question=QP(4, Run('2. X’taħseb dwar is-sena', 'f’komponiment ta madwar'))),
]
for _s in SPECS[2019]:
    if _re.match(r'^(I|II)\d', _s.key):
        _s.pages = (2, 3)


# ================================================================ 2022 HL ===
# Drafted (small-languages lane, 20 Nov): all 12 asks (no live card).
# Open: I2-I6. Excluded: I1a-e (I1ċ), II1, II2.
# Paper (rendered pp2-4): two parts only, "Massimu 70 marka". L‐Ewwel Taqsima
# "(30 marka)" (p2): the reading text "Inwessgħu t-toroq għall-ugwaljanza"
# (Josianne Cutajar) runs from p2 to p4 y141 (the last paragraph, byline and
# source on p4, then two URLs), so pages=(2, 3, 4). Q1 "(1 × 5 marki)" beside
# its head line over a) oqsma, b) ħemda, ċ) żżomm, d) antikwati, e) ħidmietna
# (the census reads 1 each); Q2-Q6 "(5 marki)" each. The census reads NO price
# for Q5 and only the first of its two printed lines: Q5's "(5 marki)" is the
# cell at p4 y497 (PY), and the question is cut from the paper (the italic
# quotation, then "Spjega kif ..."). It‐Tieni Taqsima "(40 marka)" is the
# essay: instruction "Ikteb komponiment (minimu ta' 300 kelma) dwar wieħed minn
# dawn it‐titli:", titles 1. and 2. joined by "jew".
# Scheme (rendered pp3-5): "SKEMA TA’ MARKI - 2022", Taqsima I answers a
# DIFFERENT TEXT: its Q1 explains tajt titwila, battala, burdati, l‐għan,
# il‐qofol; its Q2-Q6 ask about a teacher alone in a quarantine classroom
# ("Għaliex qiegħed waħdu fil‐klassi l‐awtur?", "‘L‐Klassi tal‐Kwarantina’").
# None of its Part I matches the paper. Its Taqsima II "(40 marka)" reprints
# an instruction in other words and the paper's two titles, and prints nothing
# under them (p4; p5 blank).
# COORDINATOR RULING (20 Nov), applied exactly: each of the 11 Part I asks is
# carded at the paper's printed marks with unprinted(...), its note the
# ruling's sentence, the five words cut from scheme lines 50-54 (S(n, after=
# letter, before=colon)); they print the scheme's own U+2010 hyphen
# ("l‐għan", "il‐qofol"). Part II carded normally: R4 at the paper's 40, the
# scheme's instruction quoted because its words differ from the paper's (10f).
# Judgement calls:
# - No `pages` on Part II: a two-part sitting's Part II is the essay (no text).
# - Title 1 wraps "s‐" / "soluzzjoni" on the paper: cut from the paper's lines
#   and joined with no space (QW); the census reads "s‐ soluzzjoni".
# - LEFT AS THE TEXT LAYER GIVES IT: Q5's "mhux in‐ nisa biss" and Q6's
#   "il‐ konlużjoni" (each one text-layer line with the break's space inside;
#   cannot be cut without typing). Flagged for the lead.
# No glyph problems (U+2010 HYPHEN throughout paper and scheme is a real
# hyphen).
import re as _re
from pl_listen_lib import Join as _Join


def _wrap_texts(texts):
    out = ''
    for t in texts:
        out = f'{out}{t}' if _re.search(r'\w[-‐/]$', out) else (f'{out} {t}' if out else t)
    return _re.sub(r'\s+', ' ', out).strip()


class _Wrapped(_Join):
    """Printed lines joined as the SEC wrapped them: a line broken right after
    a word's hyphen (the Maltese article, "s‐" / "soluzzjoni") runs on into
    the next with no space; any other break is a space."""
    def text(self, doc):
        return _wrap_texts([p.text(doc) for p in self.parts])


def QW(page, *openings):
    """The question cut from the paper's own lines (each opening names one),
    each line's own number taken off, joined as _Wrapped joins them."""
    from sl_lib import MARKER as _M, JOINER as _JN, clean_question as _cq
    return lambda doc, _q: _cq(_wrap_texts([_JN.sub('', _M.sub('', PL(page, o).text(doc), count=1))
                                            for o in openings]))


def _other_text_2022(d):
    words = ', '.join(S(n, after=f'{k}) ', before=':').text(d)
                      for n, k in zip(range(50, 55), 'abcde'))
    return (f'The marking scheme the SEC published for 2022 answers a different text in Part I (its Question 1 '
            f'explains {words}), so it gives no answer for this question.')


OTHER_2022 = unprinted(_other_text_2022)
ESSAY_2022 = 'Ikteb komponiment'


def _essay_2022(d):
    return (f'The scheme reprints the instruction as “{S(88).text(d)}” and the two titles, and prints nothing '
            f'under them.')


SPECS[2022] = [
    R('I1a', [OTHER_2022]),
    R('I1b', [OTHER_2022]),
    R('I1ċ', [OTHER_2022]),
    R('I1d', [OTHER_2022]),
    R('I1e', [OTHER_2022]),
    R('I2', [OTHER_2022]),
    R('I3', [OTHER_2022]),
    R('I4', [OTHER_2022]),
    R('I5', [OTHER_2022], total=PY(4, 497),
      question=QP(4, '5. Dan hu', Run('Spjega kif it‐tibdil', 'għajnuna għall‐ħaddiema'))),
    R('I6', [OTHER_2022]),
    R('II1', [unprinted(_essay_2022)],
      question=QW(4, ESSAY_2022, '1. Għaliex il‐bniedem', 'soluzzjoni? Jew', 'Iddiskuti l‐opinjoni')),
    R('II2', [unprinted(_essay_2022)], question=QP(4, ESSAY_2022, '2. Kif Tissawwar')),
]
for _s in SPECS[2022]:
    if _re.match(r'^I\d', _s.key):
        _s.pages = (2, 3, 4)


# ================================================================ 2023 HL ===
# Drafted (small-languages lane, 20 Nov): the 6 asks with no live card.
# Live: I1a, I1b, I1ċ, I1e, I2-I4. Open: I5, I6. Excluded: I1d, II1, III1, III2.
# Paper (rendered pp2-4): L-Ewwel Taqsima "(30 marka)"; the reading text
# "Favur trasport sostenibbli għas-saħħa fiżika u mentali" (Lara Calleja) runs
# p2-p3 to its source line; questions on p4. Q1 "(5 × 1 marka)" on its head
# line over a) qraba, b) xhieda ta’ dan, c) stħarriġ, d) impjieg, e) għadna
# mjassra (letters a)-e) from 2023; the census keys c) as I1ċ). Q2-Q6 "(5
# marki)" each. "Taqsima II (30 marka)" and "Taqsima III (40 marka)" are each
# ONE text-layer line (head and price together), which PARTP's own-line reading
# takes. Part III: instruction "Agħżel mistoqsija waħda ..." and titles 1., 2.
# joined by "jew".
# Scheme (rendered pp3-4): "SKEMA TA’ TWEĠIBIET". Q1 prints five expressions,
# each "expression: gloss", paired with the paper BY WORDS: a) qraba, b) xhieda
# ta’ dan, c) stħarriġ, e) għadna mjassra match the paper (live). Its d) is
# "qofol: iċ‐ċentru/ l‐important/dak li jorbot u jħoll": the paper does not
# set "qofol" (it is not among the five bold words of the text, rendered p2-p3:
# qraba, xhieda ta’ dan, Stħarriġ, impjieg, għadna mjassra), and the scheme
# prints NO gloss for the paper's d) "impjieg". So I1d is R4 at the paper's 1,
# the scheme's d) quoted. (Not an extra expression this year: a substitution;
# the scheme still has five.)
# Q5: the scheme reprints the quotation, then "Iddeskrivi ... mill‐psikologu.
# X’tahseb dwar dan?" where the paper asks "Taqbel mal-opinjoni tal-psikologu?
# Agħti raġunijiet għalfejn taqbel jew ma taqbilx." (10f: the paper wins, the
# scheme's words quoted); under it one bullet describing the problems and
# "(l‐opinjoni tal‐istudent)" (the student's opinion) for the second half, no
# split: two shown rows, priced as a whole (10a).
# Q6: the scheme reprints the question in other words ("Għalfejn l‐awtriċi
# tagħżel li ttemm l‐artiklu b’żewġ mistoqsijiet?"; quoted, 10f) and prints
# three lines, one point each, no split: shown, priced as a whole.
# Taqsima II: the exclusion says nothing is printed; WRONG. Under the reprinted
# task the scheme prints "Firxa wiesgħa ta’ fatturi jikkontribwixxu; dawn
# il‐fatturi flimkien ma’ eżempji mill‐ħajja ta’ kuljum huma kollha validi."
# (what an answer may draw on, no marks): one shown row under the paper's 30
# (as Dutch 2011 Q5, requirement only). Taqsima III: instruction and the two
# titles reprinted as printed, nothing under them (p4; p5 blank): R4 at 40.
# Judgement calls:
# - Q5's second row is cut inside its printed brackets: "l‐opinjoni
#   tal‐istudent".
# - Q5 and Q6 questions are cut from the paper's lines (QW) because the census
#   joins "tal-" / "psikologu" and "mill-" / "karozzi" with a space.
# - Reading text pp2-3; the live 2023 cards carry pages [2, 3, 4] (the
#   census's reading). Flagged for the lead, not changed here.
# - "(5 × 1 marka)" on the paper, "(1 × 5 marki)" on the scheme: the paper's
#   price is used (1 each), as the live cards do.
# No glyph problems (U+2010 HYPHEN and U+00A0 in the scheme are printed text).
import re as _re
from pl_listen_lib import Join as _Join


def _wrap_texts(texts):
    out = ''
    for t in texts:
        out = f'{out}{t}' if _re.search(r'\w[-‐/]$', out) else (f'{out} {t}' if out else t)
    return _re.sub(r'\s+', ' ', out).strip()


class _Wrapped(_Join):
    """Printed lines joined as the SEC wrapped them: a line broken right after
    a word's hyphen runs on into the next with no space."""
    def text(self, doc):
        return _wrap_texts([p.text(doc) for p in self.parts])


def LH(a, b=None, after=None, before=None):
    """Scheme lines a..b as L() cuts them, joined as _Wrapped joins them."""
    if b is None or b == a:
        return S(a, after=after, before=before)
    return _Wrapped(*([S(a, after=after)] + [S(n) for n in range(a + 1, b)] + [S(b, before=before)]))


def QW(page, *openings):
    """The question cut from the paper's own lines (each opening names one),
    each line's own number taken off, joined as _Wrapped joins them."""
    from sl_lib import MARKER as _M, JOINER as _JN, clean_question as _cq
    return lambda doc, _q: _cq(_wrap_texts([_JN.sub('', _M.sub('', PL(page, o).text(doc), count=1))
                                            for o in openings]))


ESSAY_2023 = 'Agħżel mistoqsija waħda'
NOTHING_2023 = 'The scheme reprints the instruction and the two titles and prints nothing under them.'
SPECS[2023] = [
    R('I1d', [unprinted(lambda d: f'At d) the scheme answers an expression the paper does not set, '
                                  f'“{S(51, after="d) ").text(d)}”, and prints no answer for this one.')]),
    R('I5', [shown(LH(84, 86, before=' (l‐opinjoni')), shown(S(86, after='frustrazzjoni. (', before=')'))],
      whole=True,
      rownote=quote(S(82, after='psikologu. '), lead='The scheme reprints the second half of the question as'),
      question=QW(4, '5. “...il-psikologu', 'qegħdin jesperjenzaw', 'Iddeskrivi fi kliemek', 'psikologu? Agħti')),
    R('I6', [shown(S(88)), shown(S(89)), shown(S(90))], whole=True,
      rownote=quote(S(87, after='6. ', before=' (5 marki)'), lead='The scheme reprints the question as'),
      question=QW(4, '6. Għalfejn l-awtriċi', 'karozzi? Tmiem')),
    R('II1', [shown(L(94, 95))], whole=True),
    R('III1', [unprinted(NOTHING_2023)], question=QP(4, ESSAY_2023, '1. Kemm huma')),
    R('III2', [unprinted(NOTHING_2023)], question=QP(4, ESSAY_2023, '2. “Il-mistoqsija')),
]
for _s in SPECS[2023]:
    if _re.match(r'^(I|II)\d', _s.key):
        _s.pages = (2, 3)


# ================================================================ 2024 HL ===
# Drafted (small-languages lane, 20 Nov): the 8 asks with no live card.
# Live: I1a, I1ċ, I2, I5, I6. Open: I3. Excluded: I1b, I1d, I1e, I4, II1, III1,
# III2.
# Paper (rendered pp2-4): L-Ewwel Taqsima "(30 marka)"; the reading text "Minn
# xibka mormija fil-baħar għal libsa fil-Malta Fashion Week" (Anthea Cachia)
# runs p2-p3; questions on p4. Q1 "(5 × 1 marki)" beside its head line over a)
# mdorrija, b) nisslet, c) tħażżiż, d) l-isfida, e) il-ħidma (the five bold
# words of the text, rendered p2-p3); Q2-Q6 "(5 marki)" each. Taqsima II "(30
# marka)", Taqsima III "(40 marka)" (PARTP), titles 1., 2. joined by "jew".
# Scheme (rendered pp3-4): Q1 prints five "expression: gloss" lines a)-e) and
# "(1 × 5 marki)" after e). It sets an EXTRA expression at d), "jibqa’
# mistgħaġeb" (in the text, p3, but not bold and not asked), so from d) on its
# gloss belongs to the paper's expression before it. Paired BY WORDS:
#   paper a) mdorrija  = scheme a) (live)
#   paper b) nisslet   = scheme b) "nislet" (one s: the same word, spelling
#                        only) -> I1b one row at 1 (the exclusion read the
#                        spelling as a different expression)
#   paper c) tħażżiż   = scheme c) (live)
#   paper d) l-isfida  = scheme e) "l‐isfida: prova li trid tegħlibha" -> I1d
#                        one row at 1, the lettering said in the note
#   paper e) il-ħidma  = NO gloss -> I1e R4 at the paper's 1, the scheme's
#                        extra d) quoted.
# Q3: one model paragraph, "(5 marki)" at its end -> one row at 5 (as live Q2).
# Q4: five "*" points, "(5 marki)" under them, no split -> shown, priced as a
# whole (10a; live Q5 and Q6 of this sitting are single 5-mark rows over the
# same kind of list: not touched, flagged).
# Taqsima II "(30 marka)": the exclusion says nothing is printed; WRONG. Under
# the reprinted question the scheme prints six bullets of points, no marks:
# shown under the paper's 30 (10a). Taqsima III: the instruction and the two
# titles reprinted as the paper prints them, nothing under them: R4 at 40.
# GLYPHS FIRST (Q4, the exclusion's reason): the scheme's font is a subset
# Calibri (CNODJA+Calibri, Type0 Identity-H) whose ligature glyphs carry no
# ToUnicode entry (PyMuPDF reads each as U+FFFD: glyph 414, 415, 425, 427).
# The .md reads glyphs 415, 425, 427 correctly ("ti", "tt", ...: "tikkolabora",
# "tqatta’", "buttuni", "plastik" all match the render) but glyph 414, which
# occurs ONCE in the scheme (p3, Q4's first point), as U+019E LATIN SMALL
# LETTER N WITH LONG RIGHT LEG "ƞ". Rendered at 400 dpi it is drawn as the
# "tf" ligature: the line prints "* Ikollħa tfittex materjal li tista’ tużah"
# (the "ħ" in "Ikollħa" is printed so, an SEC typo, not a glyph fault). The
# .md line 64 reads "* Ikollħa ƞittex materjal li tista’ tużah". No other
# line of this scheme carries an unexpected code point. NOT hand-mapped: the
# I4 spec below is written on the current line numbers with no anchor on the
# bad character, so it survives an in-place repair; until line 64 is repaired
# (glyph 414 -> "tf", one sighting, settled on the render as Romanian 2011's
# once-only glyphs were) its first row shows "ƞittex". HOLD I4 until then.
# Judgement calls:
# - Spelling-only differences in the scheme's reprints, not quoted: Q3
#   "tiddisinnja" (paper "tiddisinja"); Q4 "X’hinuma", "tiddisinnja",
#   "sostenibli" (paper "X’inhuma", "tiddisinja", "sostenibbli").
# - Reading text pp2-3; the live 2024 cards carry pages [2, 3, 4] (census).
# - The "*" bullets are cut after the asterisk (the selector's bullet strip
#   does not take "*").
import re as _re
from pl_listen_lib import Join as _Join


def _wrap_texts(texts):
    out = ''
    for t in texts:
        out = f'{out}{t}' if _re.search(r'\w[-‐/]$', out) else (f'{out} {t}' if out else t)
    return _re.sub(r'\s+', ' ', out).strip()


class _Wrapped(_Join):
    """Printed lines joined as the SEC wrapped them: a line broken right after
    a word's hyphen runs on into the next with no space."""
    def text(self, doc):
        return _wrap_texts([p.text(doc) for p in self.parts])


def LH(a, b=None, after=None, before=None):
    """Scheme lines a..b as L() cuts them, joined as _Wrapped joins them."""
    if b is None or b == a:
        return S(a, after=after, before=before)
    return _Wrapped(*([S(a, after=after)] + [S(n) for n in range(a + 1, b)] + [S(b, before=before)]))


def _extra_d_2024(d):
    return f'“{S(52, after="d) ", before=":").text(d)}”'


ESSAY_2024 = 'Agħżel mistoqsija waħda'
NOTHING_2024 = 'The scheme reprints the instruction and the two titles and prints nothing under them.'
SPECS[2024] = [
    R('I1b', [one(S(50, after='nislet: '), PP())]),
    R('I1d', [one(S(53, after='l‐isfida: ', before=' (1 × 5 marki)'), PP())],
      note='The scheme letters this expression e) (p3): its d) is an expression the paper does not set.',
      rownote=lambda d: (f'The scheme answers this expression at its e); its d) is {_extra_d_2024(d)}, which the '
                         f'paper does not set.')),
    R('I1e', [unprinted(lambda d: (f'The scheme sets at its d) an expression the paper does not set, '
                                   f'{_extra_d_2024(d)}, answers the paper’s d) at its e), and prints no answer '
                                   f'for this one.'))]),
    R('I3', [one(LH(59, 61, before=' (5 marki)'), PP())]),
    # HOLD until scheme line 64 is glyph-repaired (see GLYPHS FIRST above).
    R('I4', [shown(S(n, after='*')) for n in range(64, 69)], whole=True),
    R('II1', [shown(S(n)) for n in range(87, 93)], whole=True),
    R('III1', [unprinted(NOTHING_2024)],
      question=QP(4, ESSAY_2024, Run('1. “Min jitwieled', 'importanti li nsibu'))),
    R('III2', [unprinted(NOTHING_2024)],
      question=QP(4, ESSAY_2024, Run('2. “Aqta’ fjura', 'mill-poeżija ta’'))),
]
for _s in SPECS[2024]:
    if _re.match(r'^(I|II)\d', _s.key):
        _s.pages = (2, 3)


# ================================================================ 2025 HL ===
# Drafted (small-languages lane, 20 Nov): the 4 asks with no live card.
# Live: I1a-e (I1ċ), I2, I3, I4, I6. Open: I5. Excluded: II1, III1, III2.
# Paper (rendered pp2-4): the reading text (David Pace, on Xummiemu the
# hedgehog) runs p2-p3 to its source line (p3 y~490); L-Ewwel Taqsima "(30
# marka)" from p3; Q5 and Q6 on p4, "(5 marki)" each. Taqsima II "(30 marka)",
# Taqsima III "(40 marka)" (PARTP); Part III's instruction "Agħżel mistoqsija
# waħda minn din it-taqsima u ikteb mhux inqas minn 300 kelma." and titles 1.,
# 2. joined by "jew".
# Scheme (rendered pp5-6): Q5 reprints the quotation and the questions, then
# "Il-kandidati jridu jagħtu raġunijiet għalfejn jaħsbu iva jew le." (the
# candidates must give reasons why they think yes or no), then four italic
# bullets under "Iva" and three under "Le", no marks: shown, priced as a whole
# (10a), each row led by its printed head ("For “Iva”", as Romanian 2010 Q4).
# Taqsima II: the exclusion says nothing is printed; WRONG. Under the
# reprinted task the scheme prints "Il-kandidati jistgħu jagħtu l-opinjoni
# tagħhom billi jsemmu punti bħal:" and five bullets, no marks: shown under the
# paper's 30 (10a), that heading quoted. Taqsima III: the instruction and the
# two titles reprinted, nothing under them (p6; p7-p8 blank but for page
# numbers): R4 at the paper's 40.
# Judgement calls:
# - Q5: the scheme reprints the quotation as "... l-ambjent Malti jaħdmu
#   favurih u jistgħu jagħmlu differenza" (paper "... l-ambjent Malti u jaħdmu
#   favurih, huma jistgħu jagħmlu differenza."): words moved and dropped, so
#   the paper wins and the scheme's lines are quoted (10f). The paper's own
#   "Kif jistgħu agħmlu differenza?" (scheme "jagħmlu") is left as printed.
# - Part II: the scheme reprints the task's last line as "Ikkummenta dwar dan
#   f’madwar 100-150 kelma." (paper "... dan ikteb bejn 100-150 kelma."): quoted.
# - Part II's fourth point runs onto a line opening with a printed en dash
#   ("malajr" / "– infatti, ..."): that line is read raw (SR) so the dash stays.
# - Part III: the scheme reprints the instruction as "... ikteb madwar 300
#   kelma." where the paper prints "mhux inqas minn 300 kelma": quoted in the R4
#   note (10f).
# - Reading text pp2-3 (as the live 2025 cards).
# No glyph problems.
import re as _re
from pl_listen_lib import Join as _Join


def _wrap_texts(texts):
    out = ''
    for t in texts:
        out = f'{out}{t}' if _re.search(r'\w[-‐/]$', out) else (f'{out} {t}' if out else t)
    return _re.sub(r'\s+', ' ', out).strip()


class _Wrapped(_Join):
    """Printed lines joined as the SEC wrapped them: a line broken right after
    a word's hyphen runs on into the next with no space."""
    def text(self, doc):
        return _wrap_texts([p.text(doc) for p in self.parts])


def LH(a, b=None, after=None, before=None):
    """Scheme lines a..b as L() cuts them, joined as _Wrapped joins them."""
    if b is None or b == a:
        return S(a, after=after, before=before)
    return _Wrapped(*([S(a, after=after)] + [S(n) for n in range(a + 1, b)] + [S(b, before=before)]))


YES_2025, NO_2025 = S(91), S(97)
ESSAY_2025 = 'Agħżel mistoqsija waħda'


def _essay_2025(d):
    return (f'The scheme reprints the instruction as “{S(133).text(d)}” and the two titles, and prints nothing '
            f'under them.')


SPECS[2025] = [
    R('I5', [shown(S(92), lead=YES_2025), shown(S(93), lead=YES_2025), shown(LH(94, 95), lead=YES_2025),
             shown(S(96), lead=YES_2025),
             shown(S(98), lead=NO_2025), shown(LH(99, 100), lead=NO_2025), shown(S(101), lead=NO_2025)],
      whole=True,
      rownote=both(quote(S(90), lead='The scheme prints'),
                   quote(LH(86, 87, after='5. “', before='”'), lead='It reprints the quotation as'))),
    R('II1', [shown(LH(123, 124)), shown(LH(125, 126)), shown(S(127)), shown(J(S(128), SR(129))),
              shown(LH(130, 131))], whole=True,
      rownote=both(quote(S(122), lead='The scheme heads its points'),
                   quote(S(121), lead='It reprints the last line of the task as'))),
    R('III1', [unprinted(_essay_2025)], question=QP(4, ESSAY_2025, '1. X’jistgħu')),
    R('III2', [unprinted(_essay_2025)], question=QP(4, ESSAY_2025, Run('2. Bla flus', 'Tassew li'))),
]
for _s in SPECS[2025]:
    if _re.match(r'^(I|II)\d', _s.key):
        _s.pages = (2, 3)


def specs(year):
    return SPECS.get(year, [])
