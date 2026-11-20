#!/usr/bin/env python3
"""The spec runtime for the CLASSIC examination of the small non-curricular
languages (small-languages lane, 20 Nov 2026; PLAN-2026-11-18 queue 5).

Every one of these subjects sets the same paper in its own language: Part I, a
text and six questions (Question 1 five expressions at one mark each, Questions
2-6 five marks each); Part II, a commentary (30 marks; dropped in 2021-2022);
Part III, an essay on one of two titles (40 marks). The tariff is printed on
the QUESTION PAPER, beside each ask and on each part's head; the scheme prints
the answers, and for Parts II and III either four percentage criteria
(30/30/30/10 %), a model text, or nothing at all.

A sitting's cards are written as SPECS (sl_specs_<subject>.py), one per printed
ask, in the selector language of pl_listen_lib: `S(n)` is line n of the
scheme's .md (the text build-deck's provenance check reads), cut at printed
anchors; `PL(page, opening)` a printed line of the question paper. Every
string a card shows is cut from a document; every mark is read from the
paper's own printed price. This file turns specs into cards and checks that
each card adds up to the price the paper prints for its ask.

Shapes (CARD-STANDARD sections 2, 3, 10a, 10b, 10i; coordinator rulings of
20 Nov):
* one stated answer             -> a point row at the ask's printed price;
* answers priced by the scheme  -> point rows at those prices, adding up to
                                   the paper's price;
* a model or several points the
  scheme prices only as a whole -> `questionTotal`, the lines shown, never
                                   claimed (10a);
* percentage criteria           -> one graded criterion row, each criterion a
                                   part at its whole-number share (10b);
* nothing printed               -> the printed total and UNPRINTED_ANSWER (R4);
* no scheme published           -> NO_SCHEME_PUBLISHED, unscored (R4).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

import eu_paper                                                     # noqa: E402
from eu_paper import EuPaper, cfg                                    # noqa: E402
from eu_all import card_id, question_ref, source_material           # noqa: E402
from eu_topics import (topic_for, concept_for, answer_language,      # noqa: E402
                       language_note, ONE_LANGUAGE, LANGUAGE_NAME)
import lt_all                                                       # noqa: E402
import lt_topics                                                    # noqa: E402

# The subjects whose census walks the paper with lt_paper.LtPaper (Latvian and
# Czech never left the old examination; paper_census.SUBJECTS 'walker': 'lt').
LT_SUBJECTS = {'latvian', 'czech'}
# Modern Greek's census walks the paper with mgr_paper.MgrPaper (groups, not parts).
MGR_SUBJECTS = {'modern-greek'}
SUBJECT_NAME = {**LANGUAGE_NAME, **lt_topics.LANGUAGE, 'modern-greek': 'Modern Greek'}
import eu_topics as _eu_topics                                      # noqa: E402
TARGET_WORDS_KNOWN = set(_eu_topics.TARGET_WORDS)
from pl_listen_lib import (S, J, PL, one, menu, shown, graded,      # noqa: E402,F401
                           components, Graded, Shown, One, Menu, Sel, Join)
from pl_listen_specs import build_rows                               # noqa: E402
import pl_listen_specs as _pls                                      # noqa: E402

_one_line_percent = _pls.percent_of


def _percent_of(doc, n):
    """pl_listen_lib.percent_of, also reading a percentage the SEC wrapped:
    "... – 30" ending one scheme line and "%." opening the next (Czech 2015
    criterion 3). Only that shape; anything else still refuses."""
    try:
        return _one_line_percent(doc, n)
    except ValueError:
        line, prev = doc['scheme'][n - 1], doc['scheme'][n - 2] if n > 1 else ''
        m = re.search(r'(\d{1,3})\s*$', prev)
        if re.match(r'\s*%', line) and m:
            return int(m.group(1))
        raise


_pls.percent_of = _percent_of   # the graded-row builder this lane uses (sl_lib only)

UNPRINTED_ANSWER = 'The scheme prints no answer for this part.'
NO_SCHEME_PUBLISHED = 'The SEC published no marking scheme for this paper.'
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LANE = 'small-languages lane, 20 Nov 2026'

# Section, question, letter: 'I1a', 'I2', 'II1', 'III2'. The letter is the
# subject's own (Maltese c-dot, Bulgarian Cyrillic), so any one letter.
KEY = re.compile(r'^(III|II|I)(\d{1,2})(\w)?$')


# A question the paper prints with NO number, keyed by the census's ADDED_ASKS
# ("I1A": Maltese 2019's unnumbered question between Q1 and Q2).
ADDED_KEY = re.compile(r'^(III|II|I)(\d{1,2}[A-Z])$')


# Modern Greek: the census's own section token, "S1Q2" (group 1, question 2),
# "S2" (group 2, one unnumbered task), "SIIQ1" (2021's part II).
MGR_KEY = re.compile(r'^S(I{1,3}|[123])(?:Q(\d{1,2}))?$')


def parse_key(text):
    m = MGR_KEY.match(text)
    if m:
        return (m.group(1), int(m.group(2)) if m.group(2) else None, None, None)
    m = ADDED_KEY.match(text)
    if m:
        return (m.group(1), m.group(2), None, None)
    if text in ('I', 'II', 'III'):
        # a part that prints one task and no number (Czech "Část 2": the
        # commentary), cited "Section II" as the census keys it
        return (text, None, None, None)
    m = KEY.match(text)
    if not m:
        raise ValueError(f'not a classic key: {text!r}')
    return (m.group(1), int(m.group(2)), m.group(3), None)


def scheme_lines(subject, year, level='hl'):
    path = os.path.join(ROOT, 'examiner-reports', subject, 'schemes', f'{year}-{level}.md')
    with open(path, encoding='utf-8') as fh:
        return fh.read().split('\n')


# ----------------------------------------------------------------- prices ---
# eu_paper's mark words, with the Czech and Latvian forms the lt papers print
# ("[5 bodů]", "(5 punktu)", "1 punkts") and Ukrainian ("(5 балів)", "(5 × 1 бал)"), each before its shorter stem so the
# alternation does not stop at "bod" / "punkt" (Czech drafter, 20 Nov).
MARK_WORD = r'bodů|punktu|punkts|балів|бали|бал|' + eu_paper.MARK_WORD
# The papers' price words plus the bare "p" some sittings print ("(1 p)",
# "(5 p)", Dutch 2017), which the census's own tariff reader does not take.
PRICE_WORD = MARK_WORD + r'|p\.?'
P_PRICE = re.compile(r'[(\[]\s*(\d{1,2})\s*p\.?\s*[)\]]')


class AskPrice:
    """The price the paper prints for the ask itself (eu_paper's reading of
    its right-hand margin): (count, per, notation). With `key` ("I2", "I1а"),
    the price the paper prints for THAT ask of the same sitting (the other
    asks a remainder subtracts; REM)."""
    def __init__(self, key=None):
        self.key = key

    def read(self, doc):
        ask = doc['ask']
        if self.key:
            want = parse_key(self.key)
            ask = next((a for a in doc['P'].all_asks() if a.key == want), None)
            if ask is None:
                raise ValueError(f'the census prints no ask {self.key}')
        if not ask.tariff:
            found = P_PRICE.findall(f'{ask.text} {ask.margin_price}')
            if len(found) == 1:
                return 1, int(found[0]), f'({found[0]} p)'
            raise ValueError(f'{ask.key}: the paper prints no price for this ask')
        count, per, total = ask.tariff
        if per is None:
            return 1, total, ask.notation
        return (1, total, ask.notation) if count * per == total else (count, per, ask.notation)


def PP(key=None):
    return AskPrice(key)


class SchemePrice:
    """A price printed on scheme line n, "2 punten", "(5 bodů)": the k-th."""
    def __init__(self, n, k=0, count=1):
        self.n, self.k, self.count = n, k, count

    def read(self, doc):
        line = doc['scheme'][self.n - 1].replace('\xa0', ' ')
        found = list(re.finditer(r'(\d{1,2})\s*(?:' + MARK_WORD + r')\b', line, re.I))
        if len(found) <= self.k:
            raise ValueError(f'scheme line {self.n} prints no price #{self.k}: {line!r}')
        m = found[self.k]
        return self.count, int(m.group(1)), m.group(0)


def SP(n, k=0):
    return SchemePrice(n, k)


class PaperPrice:
    """A price printed on a QUESTION PAPER line: the line on `page` opening
    with `opening`, its k-th bracketed or worded price."""
    def __init__(self, page, opening, k=-1):
        self.page, self.opening, self.k = page, opening, k

    def read(self, doc):
        text = PL(self.page, self.opening).text(doc)
        found = list(re.finditer(r'(\d{1,3})\s*(?:' + MARK_WORD + r')', text, re.I)) or \
            list(re.finditer(r'[(\[]\s*(\d{1,3})\s*(?:/\s*\d{1,3})?\s*[)\]]', text))
        if not found:
            raise ValueError(f'paper p{self.page} {self.opening!r} prints no price: {text!r}')
        m = found[self.k]
        return 1, int(m.group(1)), m.group(0)


def PaperP(page, opening, k=-1):
    return PaperPrice(page, opening, k)


class PartPrice:
    """The total the paper prints on the head of the ask's own PART, "Deel 2
    (30 punten)", "ČASŤ III (40/100)" (eu_paper._part_head_tariff)."""
    def read(self, doc):
        ask, P = doc['ask'], doc['P']
        if hasattr(P, 'part_total'):
            total, head = P.part_total(ask.section)
            return 1, total, f'{head} ({total})'
        part_pat = re.compile(cfg(P.subject, 'classic_part'), re.I)
        part_map = cfg(P.subject, 'classic_part_map') or {}
        got = set()
        for head, (total, _of) in P._part_totals().items():
            pm = part_pat.match(head) or part_pat.match(re.sub(r'\s+', '', head))
            token = next(g for g in pm.groups() if g).lower()
            if (part_map.get(token) or eu_paper._part_token(token)) == ask.section:
                got.add((total, head))
        if not got:
            # The total printed on the head's OWN line, "PARTEA II (30/100)",
            # which _part_head_tariff (a cell to the right) does not read.
            own = re.compile(r'[(\[]\s*(?:[^\W\d_]+\.?\s+){0,2}?(\d{1,3})\s*(?:' + PRICE_WORD
                             + r')?\s*(?:/\s*\d{1,3}\s*(?:' + MARK_WORD + r')?\s*)?[)\]]\s*$', re.I)
            for line in P.lines:
                pm = part_pat.match(line.text) or part_pat.match(re.sub(r'\s+', '', line.text))
                m = own.search(line.text)
                if pm and m:
                    token = next(g for g in pm.groups() if g).lower()
                    if (part_map.get(token) or eu_paper._part_token(token)) == ask.section:
                        got.add((int(m.group(1)), line.text))
        totals = {t for t, _h in got}
        if len(totals) != 1:
            raise ValueError(f'{ask.key}: part heads print {sorted(got)}')
        total, head = next(iter(got))
        return 1, total, f'{head} ({total})'


def PARTP():
    return PartPrice()


# ------------------------------------------------------------- extra rows ---
class Unprinted:
    """The scheme gives no answer for this ask (R4): one criterion row reading
    UNPRINTED_ANSWER at the printed total. `says` is what the scheme prints
    instead, quoted in the row's note (a callable of the documents)."""
    def __init__(self, says=None):
        self.says = says


def unprinted(says=None):
    return Unprinted(says)


class Part:
    """One printed sub-task of an ask, priced on its own ("(2 punten)" ...
    "(3 punten)" under one question): a criterion row whose words are the
    scheme's reprint of the sub-task, placed 0 to its printed price, and a
    note (callable of the documents) with what the scheme prints for it."""
    def __init__(self, label, price, says=None):
        self.label, self.price, self.says = label, price, says


def part(label, price, says=None):
    return Part(label, price, says)


class RegexPrice:
    """A price read from scheme line n with a pattern whose group 1 is the
    marks: "(2 p)", "2 p.", "[5 bodů]"."""
    def __init__(self, n, pattern, src='scheme'):
        self.n, self.pattern, self.src = n, pattern, src

    def read(self, doc):
        line = doc[self.src][self.n - 1].replace('\xa0', ' ')
        m = re.search(self.pattern, line)
        if not m:
            raise ValueError(f'{self.src} line {self.n} does not print {self.pattern!r}: {line!r}')
        return 1, int(m.group(1)), m.group(0)


def RX(n, pattern):
    return RegexPrice(n, pattern)


class PaperLinePrice:
    """A price printed on the question paper as a line of its own at
    (page, y): the question's total set under its sub-task prices."""
    def __init__(self, page, y):
        self.page, self.y = page, y

    def read(self, doc):
        cell = re.compile(r'^[(\[]\s*(\d{1,3})\s*(?:' + PRICE_WORD + r')\s*[)\]]$', re.I)
        hits = [l for l in doc['lines'] if l.page == self.page and abs(l.y - self.y) < 2
                and cell.match(l.text.strip())]
        if len(hits) != 1:
            raise ValueError(f'paper p{self.page} y{self.y}: {len(hits)} price cells')
        m = cell.match(hits[0].text.strip())
        if not m:
            raise ValueError(f'paper p{self.page} y{self.y} prints no price: {hits[0].text!r}')
        return 1, int(m.group(1)), m.group(0)


def PY(page, y):
    return PaperLinePrice(page, y)


class Remainder:
    """CARD-STANDARD 10i, clarification of 20 Nov: a SINGLE ask with no
    printed mark whose mark is fixed by printed figures takes the printed
    total of its part (or question) less the printed marks of every other ask
    under it. `total` and each of `others` are price readers of PRINTED
    figures; `note(doc)` states the sum on the row. Two or more unpriced asks
    sharing a remainder are 10i proper (never split): not this class."""
    def __init__(self, total, *others):
        if not others:
            raise ValueError('a remainder needs the printed marks of the other asks')
        self.total, self.others = total, others

    def _sum(self, doc):
        _c, t, tn = self.total.read(doc)
        rest = sum(c * p for c, p, _n in (o.read(doc) for o in self.others))
        if not 0 < t - rest <= t:
            raise ValueError(f'remainder {t} - {rest} is not a mark')
        return t, tn, rest

    def read(self, doc):
        t, tn, rest = self._sum(doc)
        return 1, t - rest, f'{t} - {rest}'

    def note(self, doc):
        t, tn, rest = self._sum(doc)
        return (f'Neither the paper nor the scheme prints a mark for this question. The paper prints '
                f'{t} marks for the part ("{tn}") and {rest} for its other questions, so this one '
                f'carries the remaining {t - rest} ({t} - {rest} = {t - rest}).')


def REM(total, *others):
    return Remainder(total, *others)


class R:
    """One card: the paper's address, its rows, the price it must add up to,
    and the notes. `whole` = `questionTotal` (rows shown, not claimed)."""
    def __init__(self, key, rows, total=None, whole=False, note=None, rownote=None,
                 question=None, source=True, stem=None, pages=None):
        self.key, self.rows, self.total, self.whole = key, rows, total, whole
        self.note, self.rownote, self.question = note, rownote, question
        self.source, self.stem = source, stem
        # The question paper's pages that print the reading text, where the
        # census's own reading of them is wrong (checked on the render).
        self.pages = pages


class NoScheme:
    """A sitting whose scheme the SEC never published: every ask is carded
    with the paper's price and NO_SCHEME_PUBLISHED, unscored (R4)."""
    def __init__(self, key, total=None, question=None, pages=None):
        self.key, self.total, self.question, self.pages = key, total, question, pages


# ------------------------------------------------------------- questions ---
# A printed price inside a question's words. Worded prices go wherever they
# stand, "(1 punt)", "(maksimum 30 point)", "(30/100)"; a BARE number in
# brackets only at the start or end of the text, because inside it a bracketed
# number is a paragraph reference: "(alinea 7)", "davateljica(2)".
_WORDED = (r'[(\[]\s*(?:[^\W\d_]+\.?\s+){0,2}?\d{1,3}\s*(?:[x×*]\s*\d{1,2}\s*)?'
           r'(?:' + PRICE_WORD + r')\.?\s*(?:/\s*\d{1,3}\s*(?:' + MARK_WORD + r')?\s*)?[)\]]')
_BARE = r'[(\[]\s*\d{1,3}\s*(?:[x×*]\s*\d{1,2}\s*)?(?:/\s*\d{1,3}\s*)?[)\]]'
TARIFF_WORDED = re.compile(r'\s*' + _WORDED, re.I)
TARIFF_EDGE = re.compile(r'^\s*' + _BARE + r'\s*|\s*' + _BARE + r'\s*$')


def clean_question(text):
    """The ask's words with every printed price taken out (a card never shows
    its own tariff in the question)."""
    t = TARIFF_WORDED.sub(' ', text)
    t = TARIFF_EDGE.sub(' ', t)
    # A word the SEC broke at a line end after its hyphen (U+2010, the Maltese
    # article: "in‐" / "nisa") comes back from the line reader with a space
    # inside it; the printed word has none (second reader, 20 Nov).
    t = re.sub(r'(?<=\w)\u2010 (?=\w)', '\u2010', t)
    return re.sub(r'\s+', ' ', t).strip()


def paper_run(doc, page, first, last=None):
    """Printed paper lines on `page` from the one opening with `first` to the
    one opening with `last` (inclusive), joined: a prompt the census does not
    attach to its ask."""
    lines = [t for p, t in doc['paper'] if p == page]
    starts = [i for i, t in enumerate(lines) if t.startswith(first)]
    if len(starts) != 1:
        raise ValueError(f'paper p{page}: {len(starts)} lines open {first!r}')
    i = starts[0]
    if last is None:
        return re.sub(r'\s+', ' ', lines[i]).strip()
    ends = [j for j, t in enumerate(lines) if j >= i and t.startswith(last)]
    if not ends:
        raise ValueError(f'paper p{page}: no line opens {last!r} after {first!r}')
    return re.sub(r'\s+', ' ', ' '.join(lines[i:ends[0] + 1])).strip()


# A part's own printed marker at the start of a paper line: "c: ", "a) ", "1) ",
# "2. ", "(b) ". Taken off a line a card quotes as its question.
MARKER = re.compile(r'^(?:\(?\d{1,2}\s*[.)]|\(?[^\W\d_]\s*[):.,]|\([^\W\d_]\))\s+')
# The word joining two printed essay titles ("of", "or", "SAU", "ELLER", "ili"),
# left at the end of the first title's line.
JOINER = re.compile(r'\s+(?:of|or|ou|sau|eller|ili|alebo|vagy|tai|või|vai|nebo|ali|jew|или|або|ή|ή)\s*$',
                    re.I)


class PaperCut:
    """A cut of one printed paper line (the line on `page` opening with
    `opening`) at two printed anchors: words the paper marks (underlines,
    bold) for a question to point at."""
    def __init__(self, page, opening, after=None, before=None):
        self.page, self.opening, self.after, self.before = page, opening, after, before

    def text(self, doc):
        t = PL(self.page, self.opening).text(doc)
        if self.after is not None:
            if self.after not in t:
                raise ValueError(f'paper p{self.page}: anchor {self.after!r} not in {t!r}')
            t = t.split(self.after, 1)[1]
        if self.before is not None:
            if self.before not in t:
                raise ValueError(f'paper p{self.page}: anchor {self.before!r} not in {t!r}')
            t = t.split(self.before, 1)[0]
        return re.sub(r'\s+', ' ', t).strip()


def PC(page, opening, after=None, before=None):
    return PaperCut(page, opening, after, before)


class PaperQuestion:
    """A question cut from the paper's printed lines: each `opening` names
    the line on `page` that opens with it (a pair (page, opening) for a line
    on another page); the lines are joined, with each one's own part marker
    and a trailing title joiner taken off."""
    def __init__(self, page, openings, keep_marker=False):
        self.page, self.openings, self.keep_marker = page, openings, keep_marker

    def __call__(self, doc, _census=None):
        out = []
        for o in self.openings:
            if isinstance(o, Run):
                t = paper_run(doc, o.page or self.page, o.first, o.last)
            else:
                page, opening = (o if isinstance(o, tuple) else (self.page, o))
                t = PL(page, opening).text(doc)
            if not self.keep_marker:
                t = MARKER.sub('', t, count=1)
            out.append(JOINER.sub('', t))
        return clean_question(' '.join(out))


class Run:
    """A question line the SEC wrapped: from the printed line opening with
    `first` to the next one opening with `last`, joined."""
    def __init__(self, first, last, page=None):
        self.first, self.last, self.page = first, last, page


class ListQuestion:
    """A question that lists printed items under its stem: the stem's line
    (its number taken off) and each item's line with its own letter kept,
    "a) docutainment", one per line."""
    def __init__(self, page, stem, items):
        self.page, self.stem, self.items = page, stem, items

    def __call__(self, doc, _census=None):
        stem = PL(self.page, self.stem).text(doc) if not isinstance(self.stem, Run) else \
            paper_run(doc, self.stem.page or self.page, self.stem.first, self.stem.last)
        stem = clean_question(MARKER.sub('', stem, count=1))
        items = [clean_question(paper_run(doc, i.page or self.page, i.first, i.last) if isinstance(i, Run)
                                else (PL(*i) if isinstance(i, tuple) else PL(self.page, i)).text(doc))
                 for i in self.items]
        return '\n'.join([stem] + items)


def QL(page, stem, *items):
    return ListQuestion(page, stem, items)


def QP(page, *openings, keep_marker=False):
    return PaperQuestion(page, openings, keep_marker)


def pre(page, opening):
    """The census question with a printed lead-in line put before it: the
    instruction a lettered part answers ("Waarnaar verwijzen de volgende
    woorden?"), its marker taken off."""
    return lambda doc, q: clean_question(
        f'{MARKER.sub("", PL(page, opening).text(doc), count=1)} {JOINER.sub("", MARKER.sub("", q, count=1))}')


def prerun(page, first, last):
    """The census question with a printed instruction of several lines put
    before it (a run of the paper's lines, `first` to `last`)."""
    return lambda doc, q: clean_question(f'{paper_run(doc, page, first, last)} {q}')


class RawLine(Sel):
    """Scheme line n as printed, its opening dash or bullet KEPT: a wrapped
    sentence whose next printed line opens with a dash ("un tot" / "– corp,
    minte, suflet.", Romanian 2015), which the bullet strip would drop."""
    def text(self, doc):
        t = doc[self.src][self.n - 1].replace('\xa0', ' ')
        t = re.sub(r'\s+', ' ', t).strip()
        if not t:
            raise ValueError(f'{self.src} line {self.n} is empty')
        return t


def SR(n):
    return RawLine('scheme', n)


def L(a, b=None, after=None, before=None):
    """Scheme lines a..b joined (the SEC wrapped them), cut after `after` on
    the first and before `before` on the last."""
    if b is None or b == a:
        return S(a, after=after, before=before)
    parts = [S(a, after=after)] + [S(n) for n in range(a + 1, b)] + [S(b, before=before)]
    return J(*parts)


def crit(*spans):
    """The four printed criteria of Parts II and III: each a span (a, b) of
    scheme lines, the LAST line printing its percentage."""
    out = []
    for sp in spans:
        a, b = (sp, sp) if isinstance(sp, int) else sp
        out.append((L(a, b), b))
    return out


def examples(heading, *sels):
    """A model or indicative list the scheme prints under its own heading
    (CARD-STANDARD 10a), quoted word for word as examples, not a checklist."""
    def note(doc):
        head = heading.text(doc) if heading is not None else None
        body = '; '.join(f'“{s.text(doc)}”' for s in sels)
        if head:
            return f'Under the scheme\'s heading “{head}”, as examples, not a checklist: {body}.'
        return f'The scheme prints, as examples, not a checklist: {body}.'
    return note


def quote(*sels, lead='The scheme prints'):
    """What the scheme prints instead of an answer, quoted."""
    return lambda doc: f'{lead}: ' + ' '.join(f'“{s.text(doc)}”' for s in sels) + '.'


# ------------------------------------------------------------------ cards ---
# How each subject's paper words its answer-language rule: a sentence that
# opens with the answer word (pattern 1) and names the language (pattern 2),
# read line by line from the paper (the passage itself may name the language:
# Dutch 2010-2014 are texts about Dutch). Read per sitting: the wording changes
# ("Alle antwoorden moeten worden geschreven in het Nederlands." 2021).
RULE_WORDS = {
    'dutch': (r'Alle antwoorden', r'Nederlands'),
    'romanian': (r'Toate r\S{1,2}spunsurile', r'rom[âa]n'),
    # Bulgarian 2011 prints the rule with spaces inside its words ("В сич ки
    # отговори ... бъл гарски език.", rendered p2 at 300 dpi): matched, and
    # quoted as printed.
    'bulgarian': (r'В ?сич ?ки отговори', r'бъл ?гарск'),
    # Croatian 2016 breaks "Svi" / "odgovori moraju biti na hrvatskome jeziku." over two
    # lines; 2014 words it "Odgovore napišite na hrvatskome jeziku, ...".
    'croatian': (r'Svi odgovori|Svi$|Odgovore napišite', r'hrvatsk'),
    'danish': (r'Alle (?:svar|spørgsmål|opgaver)', r'dansk'),
    'estonian': (r'K[õo]ikidele|Ülesannetele tuleb', r'eesti'),
    'finnish': (r'Vastaa', r'suome'),
    # Hungarian: "Válaszolj ..." (2010, 2011, 2020), "... válaszoljon ..." and "Minden
    # válaszát magyarul írja le!" (2021, 2022).
    'hungarian': (r'[Vv]álaszolj(?:on)?\b|Minden válaszát', r'magyar'),
    'slovakian': (r'[Oo]dpove', r'slovensk'),
    'slovenian': (r'[Oo]dgovor', r'sloven(?:sk|šč)'),
    'swedish': (r'Alla? svar', r'svensk'),
    'maltese': (r'[Ww]ieġeb|[Tt]weġibiet', r'[Mm]alti'),
    # Czech and Latvian print the rule on their own p2 (the lt walker's live
    # cards say only that the question is in the language; new cards quote it).
    'ukrainian': (r'відповід', r'українськ'),
    # "Οι απαντήσεις να δοθούν στα νέα Ελληνικά."; 2021 "Όλες οι απαντήσεις πρέπει να γραφούν ..."
    'modern-greek': (r'απαντήσεις', r'Ελληνικ|Νεοελληνικ'),
    'czech': (r'Všechny otázky', r'česk'),
    'latvian': (r'Visām atbildēm', r'latvisk'),
}
RULE_LINES = 3      # the rule's sentence ends within this many printed lines


# Text-layer repairs for a rule sentence, per sitting, each derived from glyph
# ids (never a hand map; memory markbank-glyph-repair):
# - Romanian 2013: the bold instruction font TimesNewRoman,Bold carries no
#   ToUnicode map, and get_text reads its glyph 1211 as U+04BB. The same font's
#   glyph 1211 reads U+1EB7 in the 2012 and 2014 papers (texttrace) and is
#   drawn as a with breve and dot below (rendered 2016 p2 at 300 dpi): the SEC
#   printed "rặspunsurile".
# - Romanian 2011: two glyphs of MicrosoftSansSerif that occur once each in the
#   whole Romanian corpus (no clean sighting to learn from), so settled by
#   cropping them at 400 dpi and looking (p4): glyph 1931, read U+020A, is drawn
#   as I with a circumflex ("În zilele noastre"); glyph 1440, read U+1E6D, as t
#   with a comma below ("fericiți").
TEXT_FIXES = {('romanian', 2011): {'\u020a': '\u00ce', '\u1e6d': '\u021b'}}
# - Paper maps derived from glyph ids by sl_glyphs.py (Romanian 2013: Times New
#   Roman with no ToUnicode map; each entry voted by the same glyph's clean
#   sightings across the corpus, or settled on a render): loaded as written.
for _path in sorted(__import__('glob').glob(os.path.join(HERE, 'glyphmap-*-*-paper.json'))):
    _subject, _year = os.path.basename(_path)[len('glyphmap-'):-len('-paper.json')].rsplit('-', 1)
    with open(_path, encoding='utf-8') as _fh:
        TEXT_FIXES.setdefault((_subject, int(_year)), {}).update(json.load(_fh))
RULE_FIXES = TEXT_FIXES


def fix_text(subject, year, text):
    for bad, good in TEXT_FIXES.get((subject, year), {}).items():
        text = text.replace(bad, good)
    return text
LATIN_SUBJECTS = {'dutch', 'romanian', 'hungarian', 'slovakian', 'swedish', 'estonian', 'finnish',
                  'croatian', 'danish', 'slovenian', 'maltese', 'czech', 'latvian'}


# A sentence ends at . ! ? followed by an upper-case letter, a line end or the
# text's end, or a bracket opening one ("... slovenščini. (Največ 100 točk)",
# Slovenian 2024); not at "I." in "az I., II. és III. részben" (Hungarian).
SENT_END = re.compile(r'[.!?](?=\s+[(\[]?[A-ZÀ-ÖØ-ÞĀ-Ž\u0400-\u042f\u0386-\u03ab]|\s*$)')


def rule_sentence(subject, doc):
    """(PDF page, sentence) of the paper's answer-language rule, cut from its
    own printed lines: from the start of the sentence holding the answer word
    to its end. A printed line that names the language and has no stop ends
    the sentence unless the next line runs on in lower case ("na hrvatskome" /
    "jeziku."; Romanian 2010 sets no stop before "Maximum 100 puncte")."""
    answer, lang = (re.compile(x) for x in RULE_WORDS[subject])
    for page in sorted({p for p, _t in doc['paper']}):
        lines = [re.sub(r'\s+', ' ', t).strip() for p, t in doc['paper'] if p == page]
        for i, line in enumerate(lines):
            # every answer word on the line: the rule may follow another use of
            # it ("... odpovedajte na otázky ... častiach. Odpovede napíšte po
            # slovensky ...", Slovakian)
            for m in answer.finditer(line):
                # the sentence's start: after the last sentence end before the
                # answer word, on this line or the one above it
                prev = lines[i - 1] if i else ''
                combined = f'{prev} {line}' if prev else line
                at = (len(prev) + 1 if prev else 0) + m.start()
                ends = [e.end() for e in SENT_END.finditer(combined[:at])]
                start = ends[-1] if ends else (len(prev) + 1 if prev else 0)
                # Cut, never re-joined: the printed spacing stands ("It‐tweġibiet",
                # where the answer word opens inside a hyphenated word; Maltese 2022).
                text = combined[start:].strip()
                lead = combined[start:at].strip()
                for nxt in lines[i + 1:i + RULE_LINES]:
                    stop = SENT_END.search(text, len(lead))
                    if stop:
                        break
                    # ... unless the next line runs on in lower case, or opens with a part's
                    # Roman numeral ("az I., II. és" / "III. részben", Hungarian)
                    if lang.search(text) and not re.match(r'[a-zà-öø-ÿā-ž\u0430-\u044f]|(?:I{1,3}|IV)\.\s', nxt):
                        break
                    text = f'{text} {nxt}'
                stop = SENT_END.search(text, len(lead))
                sent = text[:stop.end()] if stop else text
                if lang.search(sent):
                    for bad, good in RULE_FIXES.get((subject, doc['P'].year), {}).items():
                        sent = sent.replace(bad, good)
                    if subject in LATIN_SUBJECTS and re.search('[\u0400-\u04ff\ufffd]', sent):
                        raise ValueError(f'{subject} {doc["P"].year}: rule text carries an unrepaired glyph: {sent!r}')
                    return page, sent
    return None


def printed_page(path, pdf_page):
    """The page number the booklet itself prints on PDF page `pdf_page`, where
    it prints one: the number in the top or bottom margin (within 100 points of
    the edge; Bulgarian 2012/2014/2016 set it 97 points up) that follows the
    booklet's own offset from the PDF (most booklets 0; Dutch 2018's cover is
    unnumbered, so -1), voted over every page so a paragraph number set in the
    margin is not taken for it."""
    import collections
    import fitz
    doc = fitz.open(path)
    cands = []
    for page in doc:
        h, nums = page.rect.height, set()
        for b in page.get_text('dict')['blocks']:
            for ln in b.get('lines', []):
                t = ''.join(sp['text'] for sp in ln['spans']).strip()
                if re.fullmatch(r'\d{1,2}', t) and (ln['bbox'][1] < 100 or ln['bbox'][1] > h - 100):
                    nums.add(int(t))
        cands.append(nums)
    votes = collections.Counter(n - (i + 1) for i, nums in enumerate(cands) for n in nums)
    if not votes:
        return None
    offset = votes.most_common(1)[0][0]
    want = pdf_page + offset
    return want if want in cands[pdf_page - 1] else None


def rule_note(subject, doc, language):
    """The answer-language note, quoting the rule as THIS paper prints it,
    with the page number the booklet prints (coordinator, 20 Nov: wording and
    page as printed). eu_topics.language_note quotes one sitting's sentence for
    every sitting and says it is printed "on its own first page", the cover."""
    if subject not in ONE_LANGUAGE and subject not in RULE_WORDS:
        return language_note(subject, language)
    found = rule_sentence(subject, doc)
    if found is None and subject in LT_SUBJECTS:
        # Latvian 2024 and 2025 print no answer-language rule at all ("Atbildiet
        # uz jautājumiem!" only): the lt walker's own note, which claims none.
        return lt_topics.language_note(subject, SUBJECT_NAME[subject], doc['P'].year)
    if found is None:
        raise ValueError(f'{subject}: the paper prints no answer-language rule')
    page = printed_page(doc['P'].path, found[0])
    where = f'on page {page}' if page else 'above its questions'
    return (f'The examination requires every answer in {SUBJECT_NAME[subject].upper()}. '
            f'The paper prints the rule {where}: "{found[1]}"')


def part_head(P, section):
    """The part's own printed head ("Deel 2: commentaar")."""
    if hasattr(P, 'part_head'):
        return P.part_head(section)
    part_pat = re.compile(cfg(P.subject, 'classic_part'), re.I)
    part_map = cfg(P.subject, 'classic_part_map') or {}
    tail = cfg(P.subject, 'classic_part_tail')
    heads = []
    for line in P.lines:
        pm = part_pat.match(line.text) or part_pat.match(re.sub(r'\s+', '', line.text))
        if not pm and tail and re.fullmatch(r'(?:I{1,3}|[123])\s*\.?', line.text.strip()):
            # The numeral set as a cell of its own, "II." + "dio [30 bodova]"
            # (Croatian 2015-2020): eu_paper's classic_part_tail joins them, as
            # the census does.
            nxt = sorted((l for l in P.lines if l.page == line.page and abs(l.y - line.y) < 2 and l.x > line.x),
                         key=lambda l: l.x)
            if nxt and re.match(tail, nxt[0].text.strip(), re.I):
                pm = part_pat.match(f'{line.text.strip()} {nxt[0].text.strip()}')
        if pm:
            token = next(g for g in pm.groups() if g).lower()
            if (part_map.get(token) or eu_paper._part_token(token)) == section:
                # The head's second half set as a cell of its own on the same
                # line, "Deel 2:" + "Commentaar" (Dutch 2023), price cells aside.
                cells = [l.text for l in P.lines if l.page == line.page and abs(l.y - line.y) < 2
                         and l.x > line.x and not TARIFF_EDGE.fullmatch(l.text.strip())
                         and not TARIFF_WORDED.fullmatch(' ' + l.text.strip())
                         # an unbracketed total, "30 marka" (Maltese 2019 p2)
                         and not re.fullmatch(r'\d{1,3}\s*(?:' + MARK_WORD + r')', l.text.strip(), re.I)]
                heads.append(' '.join([line.text] + cells))
    return heads[-1] if heads else None


def essay_part(section, two_part):
    """The part an ask is answered as: a two-part sitting's Part II is its essay."""
    return 'III' if two_part and section == 'II' else section


def default_price(key):
    """Part I prices each ask beside it; Parts II and III print one total on
    the part's own head."""
    return PP() if key[0] == 'I' else PARTP()


class LtView:
    """A Latvian or Czech paper walked by lt_paper.LtPaper, the walker their
    census uses, seen through the EuPaper interface the card builder reads:
    the census's own keys, Part I's reading pages and leads by question
    number, and each part's head and printed share ("Část 1 [30 bodů]",
    "I daļa (30 punkti)"). lt asks print no per-ask tariff the walker reads:
    prices come from PaperP/PY/SP in the specs."""
    def __init__(self, year, level, subject):
        import lt_paper
        self._P = lt_paper.LtPaper(year, level, subject)
        self.year, self.level, self.subject, self.path = year, level, subject, self._P.path
        self.lines = self._P.lines
        self.text_pages = {}
        self._asks = [self._wrap(a) for a in self._P._asks]

    @staticmethod
    def _wrap(a):
        import types
        return types.SimpleNamespace(key=a.key, section=a.section, q=a.q, letter=a.letter, roman=a.roman,
                                     text=a.text, full_text=a.full_text, page=a.page,
                                     tariff=None, margin_price='', notation='')

    def all_asks(self):
        return [self._wrap(a) for a in self._P.all_asks()]

    def pages_for(self, *args):                 # (q) or lt_all's (section, q)
        q = args[-1]
        return self.text_pages.get(q) or self._P.pages_for('I', q)

    def lead(self, *args):
        return self._P.lead('I', args[-1])

    def _heads(self, section):
        import lt_paper
        out = []
        for line in self.lines:
            m = lt_paper.PART_OLD.match(line.text.strip())
            if m and lt_paper.part_token(m) == section:
                cells = [l.text for l in self.lines if l.page == line.page and abs(l.y - line.y) < 2 and l.x > line.x]
                out.append(' '.join([line.text] + cells))
        return out

    def part_head(self, section):
        heads = self._heads(section)
        if not heads:
            return None
        # the head's words, its printed share left off ("Část 1" of "Část 1 [30 bodů]")
        return re.sub(r'\s*[\(\[]\s*\d{2,3}[^\)\]]*[\)\]]\s*$', '', heads[-1]).strip()

    def part_total(self, section):
        import lt_paper
        got = set()
        for head in self._heads(section):
            m = lt_paper.LtPaper.PART_SHARE.search(head)
            if m:
                got.add((int(m.group(1)), head))
        if len({t for t, _h in got}) != 1:
            raise ValueError(f'{self.subject} {self.year} part {section}: heads print {sorted(got)}')
        return next(iter(got))


class MgrView:
    """A Modern Greek paper walked by mgr_paper.MgrPaper (its census's walker)
    seen through the EuPaper interface: the census keys ("1", 2) / ("2", None) /
    ("I", 1), each ask's own printed marks as its tariff, the article's pages,
    the group totals the paper prints, and positioned lines for PL/PC/PY."""
    def __init__(self, year, level, subject):
        import types
        import mgr_paper
        import pymupdf
        self._P = mgr_paper.MgrPaper(year, level, subject)
        self.year, self.level, self.subject, self.path = year, level, subject, self._P.path
        self.lines = []
        with pymupdf.open(self.path) as pdf:
            for pno, page in enumerate(pdf, 1):
                for block in page.get_text('dict')['blocks']:
                    for line in block.get('lines', []):
                        text = ''.join(sp['text'] for sp in line['spans'])
                        if text.strip():
                            x0, y0, x1, _y1 = line['bbox']
                            self.lines.append(eu_paper.Line(pno, x0, y0, x1, text))
        raw = self._P.asks()
        self._asks = [types.SimpleNamespace(
            key=a.key, section=a.section, q=a.q, letter=a.letter, roman=None, text=a.text,
            full_text=a.text, page=a.page, tariff=(1, a.marks, a.marks) if a.marks else None,
            margin_price='', notation=f'({a.marks})' if a.marks else '', kind=a.kind, items=a.items)
            for a in raw]
        self.text_pages = {}

    def all_asks(self):
        return list(self._asks)

    def pages_for(self, *args):
        return self.text_pages.get(args[-1]) or list(self._P.passage_pages)

    def lead(self, *args):
        return ''

    def part_head(self, section):
        return None

    def part_total(self, section):
        total = self._P.section_marks.get(section)
        if total is None:
            raise ValueError(f'modern-greek {self.year} section {section}: no printed total')
        return total, f'section {section}'


def documents(subject, year, level='hl', scheme=True):
    if subject in MGR_SUBJECTS:
        P = MgrView(year, level, subject)
    else:
        P = LtView(year, level, subject) if subject in LT_SUBJECTS else EuPaper(year, level, subject)
    doc = {'paper': [(l.page, fix_text(subject, year, l.text)) for l in P.lines], 'lines': P.lines, 'P': P,
           'scheme': scheme_lines(subject, year, level) if scheme else []}
    return P, doc


def _added_ask(subject, year, level, key, P):
    """An ask the paper prints with no number (paper_census.ADDED_ASKS), as
    the census lifts it, shaped like a walker's ask for the card builder."""
    import types
    import paper_census
    for spec in paper_census.ADDED_ASKS.get((subject, year, level), []):
        if tuple(spec['key']) == key:
            leaf, _marks = paper_census._added_leaf(subject, year, level, spec)
            return types.SimpleNamespace(key=key, section=key[0], q=key[1], letter=None, roman=None,
                                         page=spec['lines'][0], text=leaf['text'], full_text=leaf['text'],
                                         tariff=None, margin_price='', notation='')
    return None


def cards(subject, year, specs, level='hl', scheme=True):
    P, doc = documents(subject, year, level, scheme)
    asks = {a.key: a for a in P.all_asks()}
    # A lettered question the paper prices only as a whole ("1. ... (5 puncte)"
    # over a) to e)) is carded at the question: its parent ask (R7, CARD-STANDARD
    # 2 "questionTotal"; Latvian and Czech Q1 are the precedent).
    parents = {a.key: a for a in P._asks if a.letter is None and a.roman is None
               and any(b.section == a.section and b.q == a.q and b.letter for b in P._asks)}
    two_part = not any(k[0] == 'III' for k in asks)
    out, seen = [], set()
    for spec in specs:
        key = parse_key(spec.key)
        if key not in asks and key in parents:
            asks[key] = parents[key]
        added = key not in asks and _added_ask(subject, year, level, key, P)
        if added:
            asks[key] = added
        if key not in asks:
            raise ValueError(f'{subject} {year} {spec.key}: the census prints no such ask')
        if key in seen:
            raise ValueError(f'{subject} {year} {spec.key}: carded twice')
        seen.add(key)
        ask = asks[key]
        doc['ask'] = ask
        question = clean_question(ask.full_text)
        if spec.question:
            question = spec.question(doc, question) if callable(spec.question) else spec.question
        question = fix_text(subject, year, question)
        lt = subject in LT_SUBJECTS
        mgr = subject in MGR_SUBJECTS
        if mgr:
            import mgr_all
            import mgr_topics
            language = mgr_topics.answer_language(P._P) or 'Modern Greek'
        else:
            language = (lt_topics.answer_language(subject, question) if lt else
                        # a subject whose paper prints a one-language rule that eu_topics has no
                        # word list for (Ukrainian: "... дайте відповіді українською мовою ...")
                        SUBJECT_NAME[subject] if subject in RULE_WORDS and subject not in ONE_LANGUAGE
                        and subject not in TARGET_WORDS_KNOWN else answer_language(subject, question))
        note = lang_note = rule_note(subject, doc, language)
        card = {
            'id': (mgr_all.card_id(year, level, key) if mgr
                   else (lt_all.card_id if lt else card_id)(subject, year, level, key).lower() if added
                   else f'{lt_all.ID_PREFIX[subject]}-{year}-{level}-{key[0].lower()}' if lt and key[1] is None
                   else (lt_all.card_id if lt else card_id)(subject, year, level, key)),
            'subjectId': subject,
            'level': LEVEL_WORD[level],
            'year': year,
            'section': key[0],
            # In a two-part sitting (2021, 2022) Part II IS the essay: filed
            # and shown as Part III's is.
            # A question carded whole over its lettered expressions is filed as
            # the expressions are (second reader, 20 Nov: Q1 sat under two topics).
            'topicId': (mgr_topics.topic_for(ask) if mgr else
                        lt_topics.topic_for(subject, year, key[0], key[1]) if subject in LT_SUBJECTS else
                        topic_for(subject, 'classic', essay_part(key[0], two_part),
                                  key[2] or ('*' if key in parents else None))),
            # From the ask's own printed words, not an instruction put before
            # them (2026 Q1(c)-(e) shared one; second reader, 20 Nov).
            'conceptId': (mgr_topics.concept_for if mgr else lt_topics.concept_for if subject in LT_SUBJECTS
                          else concept_for)(
                clean_question(MARKER.sub('', ask.text, count=1)) or question),
            'questionRef': (mgr_all.question_ref if mgr else lt_all.question_ref if lt else question_ref)(year, level, key),
            'questionText': question,
        }
        if isinstance(spec, NoScheme):
            _c, total, notation = (spec.total or default_price(key)).read(doc)
            card.update({
                'tariffModel': {'kind': 'questionTotal'}, 'totalMarks': total,
                'rows': [{'id': 'r-1', 'kind': 'criterion', 'verbatim': NO_SCHEME_PUBLISHED,
                          'marks': None, 'contextNote': note}],
                'noScheme': True,
                'notes': (f'Read on the rendered paper ({LANE}); the paper prints this ask on PDF page '
                          f'{ask.page} of the question paper and prices it "{notation}". The SEC '
                          f'published no marking scheme for this sitting (SOURCES.md: not in the 31 Aug '
                          f'2026 archive listing; live check 18 Nov 2026 = 404).'),
            })
        else:
            if spec.rownote:
                note = f'{note} {spec.rownote(doc) if callable(spec.rownote) else spec.rownote}'
            unp = [r for r in spec.rows if isinstance(r, Unprinted)]
            parts = [r for r in spec.rows if isinstance(r, Part)]
            if parts:
                if len(parts) != len(spec.rows):
                    raise ValueError(f'{spec.key}: a card of priced sub-tasks holds nothing else')
                rows, total = [], 0
                for i, r in enumerate(parts, 1):
                    _c, m, _n = r.price.read(doc)
                    says = r.says(doc) if callable(r.says) else r.says
                    ctx = ' '.join(x for x in [note if i == 1 else '', says] if x)
                    rows.append({'id': f'r-{i}', 'kind': 'criterion', 'verbatim': r.label.text(doc),
                                 'marks': m, 'permittedMarks': list(range(m + 1)),
                                 **({'contextNote': ctx} if ctx else {})})
                    total += m
                pc, pp, pn = (spec.total or default_price(key)).read(doc)
                if pc * pp != total:
                    raise ValueError(f'{subject} {year} {spec.key}: sub-tasks add to {total}, the paper prints {pn!r}')
            elif unp:
                if len(spec.rows) != 1:
                    raise ValueError(f'{spec.key}: UNPRINTED_ANSWER is the card\'s only row here')
                _c, total, _n = (spec.total or default_price(key)).read(doc)
                says = unp[0].says
                ctx = ' '.join(x for x in [note, says(doc) if callable(says) else says] if x)
                rows = [{'id': 'r-1', 'kind': 'criterion', 'verbatim': UNPRINTED_ANSWER,
                         'marks': total, 'permittedMarks': list(range(total + 1)),
                         'unprinted': True, **({'contextNote': ctx} if ctx else {})}]
            else:
                rows, total = build_rows(doc, spec, note)
                price = spec.total or default_price(key)
                pc, pp, pn = price.read(doc)
                if spec.whole:
                    if total != 0:
                        raise ValueError(f'{subject} {year} {spec.key}: a whole-question card shows rows only')
                    total = pc * pp
                elif pc * pp != total:
                    raise ValueError(f'{subject} {year} {spec.key}: rows add to {total}, '
                                     f'the paper prints {pn!r}')
            card.update({
                'tariffModel': {'kind': 'questionTotal' if spec.whole else 'fixed'},
                'totalMarks': total,
                'rows': rows,
                'notes': (f'Read on the rendered scheme and paper ({LANE}); the paper prints this ask '
                          f'on PDF page {ask.page} of the question paper.'
                          + (f' {spec.note}' if spec.note else '')),
            })
        if spec.stem if hasattr(spec, 'stem') else None:
            card['stem'] = spec.stem(doc) if callable(spec.stem) else spec.stem
        # The reading text travels with Parts I and II, and with an essay title
        # that cites a paragraph of it (source='text'; Romanian 2010 III "(p.6)").
        if getattr(spec, 'source', True) and (essay_part(key[0], two_part) in ('I', 'II')
                                              or getattr(spec, 'source', True) == 'text'):
            if getattr(spec, 'pages', None):
                # The spec's pages, read on the render, where the census attaches
                # none or the wrong ones (Romanian 2010 has none).
                P.text_pages[ask.q] = list(spec.pages)
            src = (mgr_all._source(P._P, year, level, language) if mgr
                   else lt_all.source_material(P, ask, language, level, year, subject) if lt
                   else source_material(P, ask, subject, language, level, year))
            if src:
                src['presentationNote'] = ('Read the text exactly as the examination printed it, then '
                                           'answer. ' + lang_note)
                if getattr(spec, 'pages', None):
                    src['pages'] = list(spec.pages)
                if key[0] != 'I' or added:
                    # Part II's own head; and the part head for an unnumbered
                    # question, which has no "Question N" of its own.
                    head = part_head(P, key[0])
                    if head:
                        src['label'] = clean_question(head).upper()[:60]
                card['sourceMaterial'] = src
        out.append(card)
    return out
