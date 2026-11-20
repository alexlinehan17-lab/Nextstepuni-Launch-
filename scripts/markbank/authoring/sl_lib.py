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
from pl_listen_lib import (S, J, PL, one, menu, shown, graded,      # noqa: E402,F401
                           components, Graded, Shown, One, Menu, Sel, Join)
from pl_listen_specs import build_rows                               # noqa: E402

UNPRINTED_ANSWER = 'The scheme prints no answer for this part.'
NO_SCHEME_PUBLISHED = 'The SEC published no marking scheme for this paper.'
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LANE = 'small-languages lane, 20 Nov 2026'

# Section, question, letter: 'I1a', 'I2', 'II1', 'III2'. The letter is the
# subject's own (Maltese c-dot, Bulgarian Cyrillic), so any one letter.
KEY = re.compile(r'^(III|II|I)(\d{1,2})(\w)?$')


def parse_key(text):
    m = KEY.match(text)
    if not m:
        raise ValueError(f'not a classic key: {text!r}')
    return (m.group(1), int(m.group(2)), m.group(3), None)


def scheme_lines(subject, year, level='hl'):
    path = os.path.join(ROOT, 'examiner-reports', subject, 'schemes', f'{year}-{level}.md')
    with open(path, encoding='utf-8') as fh:
        return fh.read().split('\n')


# ----------------------------------------------------------------- prices ---
MARK_WORD = eu_paper.MARK_WORD
# The papers' price words plus the bare "p" some sittings print ("(1 p)",
# "(5 p)", Dutch 2017), which the census's own tariff reader does not take.
PRICE_WORD = MARK_WORD + r'|p\.?'
P_PRICE = re.compile(r'[(\[]\s*(\d{1,2})\s*p\.?\s*[)\]]')


class AskPrice:
    """The price the paper prints for the ask itself (eu_paper's reading of
    its right-hand margin): (count, per, notation)."""
    def read(self, doc):
        ask = doc['ask']
        if not ask.tariff:
            found = P_PRICE.findall(f'{ask.text} {ask.margin_price}')
            if len(found) == 1:
                return 1, int(found[0]), f'({found[0]} p)'
            raise ValueError(f'{ask.key}: the paper prints no price for this ask')
        count, per, total = ask.tariff
        if per is None:
            return 1, total, ask.notation
        return (1, total, ask.notation) if count * per == total else (count, per, ask.notation)


def PP():
    return AskPrice()


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
        part_pat = re.compile(cfg(P.subject, 'classic_part'), re.I)
        part_map = cfg(P.subject, 'classic_part_map') or {}
        got = set()
        for head, (total, _of) in P._part_totals().items():
            pm = part_pat.match(head) or part_pat.match(re.sub(r'\s+', '', head))
            token = next(g for g in pm.groups() if g).lower()
            if (part_map.get(token) or eu_paper._part_token(token)) == ask.section:
                got.add((total, head))
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
# The words each paper's answer-language rule opens with, where they are not
# the first two words of eu_topics.ONE_LANGUAGE's (2025-era) sentence.
RULE_OPENING = {}


def rule_note(subject, doc, language):
    """The answer-language note, quoting the rule as THIS paper prints it.

    eu_topics.language_note quotes one sitting's sentence for every sitting
    and says it is printed "on its own first page", which is the cover in these
    booklets (second reader, 20 Nov: Dutch prints it on p2, p3 or p4, worded
    three ways). Here the sentence is cut from the paper's own text, from its
    opening words to its full stop, and its page named."""
    rule = ONE_LANGUAGE.get(subject)
    if not rule:
        return language_note(subject, language)
    opening = RULE_OPENING.get(subject) or ' '.join(rule.split()[:2])
    hits = []
    for page in sorted({p for p, _t in doc['paper']}):
        text = re.sub(r'\s+', ' ', ' '.join(t for p, t in doc['paper'] if p == page))
        i = text.find(opening)
        if i >= 0:
            j = text.find('.', i)
            hits.append((page, text[i:j + 1] if j > i else text[i:]))
    if len(hits) != 1:
        raise ValueError(f'{subject}: the paper prints {len(hits)} answer-language rules: {hits}')
    page, sentence = hits[0]
    return (f'The examination requires every answer in {LANGUAGE_NAME[subject].upper()}. '
            f'The paper prints the rule on page {page}: "{sentence}"')


def part_head(P, section):
    """The part's own printed head ("Deel 2: commentaar")."""
    part_pat = re.compile(cfg(P.subject, 'classic_part'), re.I)
    part_map = cfg(P.subject, 'classic_part_map') or {}
    heads = []
    for line in P.lines:
        pm = part_pat.match(line.text) or part_pat.match(re.sub(r'\s+', '', line.text))
        if pm:
            token = next(g for g in pm.groups() if g).lower()
            if (part_map.get(token) or eu_paper._part_token(token)) == section:
                heads.append(line.text)
    return heads[-1] if heads else None


def essay_part(section, two_part):
    """The part an ask is answered as: a two-part sitting's Part II is its essay."""
    return 'III' if two_part and section == 'II' else section


def default_price(key):
    """Part I prices each ask beside it; Parts II and III print one total on
    the part's own head."""
    return PP() if key[0] == 'I' else PARTP()


def documents(subject, year, level='hl', scheme=True):
    P = EuPaper(year, level, subject)
    doc = {'paper': [(l.page, l.text) for l in P.lines], 'lines': P.lines, 'P': P,
           'scheme': scheme_lines(subject, year, level) if scheme else []}
    return P, doc


def cards(subject, year, specs, level='hl', scheme=True):
    P, doc = documents(subject, year, level, scheme)
    asks = {a.key: a for a in P.all_asks()}
    two_part = not any(k[0] == 'III' for k in asks)
    out, seen = [], set()
    for spec in specs:
        key = parse_key(spec.key)
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
        language = answer_language(subject, question)
        note = lang_note = rule_note(subject, doc, language)
        card = {
            'id': card_id(subject, year, level, key),
            'subjectId': subject,
            'level': LEVEL_WORD[level],
            'year': year,
            'section': key[0],
            # In a two-part sitting (2021, 2022) Part II IS the essay: filed
            # and shown as Part III's is.
            'topicId': topic_for(subject, 'classic', essay_part(key[0], two_part), key[2]),
            'conceptId': concept_for(question),
            'questionRef': question_ref(year, level, key),
            'questionText': question,
        }
        if isinstance(spec, NoScheme):
            _c, total, notation = (spec.total or default_price(key)).read(doc)
            card.update({
                'tariffModel': {'kind': 'questionTotal'}, 'totalMarks': total,
                'rows': [{'id': 'r-1', 'kind': 'criterion', 'verbatim': NO_SCHEME_PUBLISHED,
                          'marks': None, 'contextNote': note}],
                'noScheme': True,
                'notes': (f'Read on the rendered paper ({LANE}); the paper prints this ask on page '
                          f'{ask.page} of the question booklet and prices it "{notation}". The SEC '
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
                          f'on page {ask.page} of the question booklet.'
                          + (f' {spec.note}' if spec.note else '')),
            })
        if spec.stem if hasattr(spec, 'stem') else None:
            card['stem'] = spec.stem(doc) if callable(spec.stem) else spec.stem
        if getattr(spec, 'source', True) and essay_part(key[0], two_part) in ('I', 'II'):
            src = source_material(P, ask, subject, language, level, year)
            if src:
                src['presentationNote'] = ('Read the text exactly as the examination printed it, then '
                                           'answer. ' + lang_note)
                if getattr(spec, 'pages', None):
                    src['pages'] = list(spec.pages)
                if key[0] != 'I':
                    head = part_head(P, key[0])
                    if head:
                        src['label'] = clean_question(head).upper()[:60]
                card['sourceMaterial'] = src
        out.append(card)
    return out
