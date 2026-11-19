#!/usr/bin/env python3
"""Reviewed specs for the Portuguese cards the shared generator does not make
right: every listening ask, and the reading asks eu_all refuses or shapes
wrongly. Portuguese-only, on the Polish pattern (pl_listen_specs.py).

    python3 scripts/markbank/authoring/pt_specs.py draft 2026 hl     # census asks beside the scheme
    python3 scripts/markbank/authoring/pt_specs.py cards 2026 hl     # what the specs build

Each entry names the census address the card answers and says, by SELECTORS
(pt_lib), which scheme lines are its answers and which printed price pays it.
Nothing is typed: the question is the census's reading of the paper or the
listening booklet (eu_paper), with booklet lines a question prints below
itself appended by PL(page, opening); the answers and prices are cuts of the
scheme's .md. A reading card keeps every field eu_all would give it (id, topic,
concept, stem, the reading text's pages) and takes its rows from the spec.

Checked as it builds: every census listening ask of the sitting gets exactly
one card; each card adds up to the price its spec names; each Parte adds up to
the total the scheme prints on its head ("Parte A Diálogo ⟨20 Marks⟩").
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

from pt_lib import (S, J, B, T, T2, AnyOf, CELL, PL, Sel, one, menu, alt, stepped, shown, rest,   # noqa: E402,F401
                    pairs, scheme_doc, build_rows, SCHEMES)
from eu_paper import EuPaper, read_lines                          # noqa: E402
from eu_topics import (topic_for, concept_for, answer_language,    # noqa: E402
                       language_note, ENGLISH_OR_IRISH)
from paper_census import key_label                                # noqa: E402

SUBJECT = 'portuguese'
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}
# A listening ask's roman follows its number ("LD4i" is Q4(i)), and where the
# booklet also letters it, the letter and a dash come first ("LC3a-i" is
# Q3(a)(i)); a reading ask's roman follows a dash ("A1b-ii").
KEY = re.compile(r'^(L[A-E])(\d{1,2})(?:([a-h])-)?(i{1,3}|iv|vi{0,3})?$'
                 r'|^(A|B)(\d{1,2})([a-l])?(?:-(i{1,3}|iv|vi{0,3}))?$')
AUDIO = os.path.join(ROOT, 'data', 'portugueseAudio.json')
PARTE = re.compile(r'^Parte\s+([A-E])\b')
NUMBERED = re.compile(r'^\(\d{1,2}\)')
# "Parte A Diálogo ⟨20 Marks⟩", "Parte B Anúncio 20 marks", and 2025 Higher's
# bare "Parte B Entrevista 20".
SECTION_TOTAL = re.compile(r'^Parte?\s+([A-E])\b.*?(\d{1,3})\s*(?:marks?\b|\u27e9|$)', re.I)
# A rule the booklet prints after the last words of a question: furniture.
# (The census already leaves out the "1." "2." "3." answer lines, and a
# question may itself end in a number: "porta de embarque número 7.")
TRAILING = re.compile(r'(?:\s+_{3,})+\s*$')


def parse_key(spec_key):
    m = KEY.match(spec_key)
    if not m:
        raise ValueError(f'bad key {spec_key!r}')
    g = m.groups()
    sec, q, letter, roman = g[:4] if g[0] else g[4:]
    return (sec, int(q), letter or None, roman or None)


def card_id(year, level, key):
    section, q, letter, roman = key
    return '-'.join(['por', str(year), level, section.lower(), str(q)]
                    + ([letter] if letter else []) + ([roman] if roman else []))


class C:
    """One card: the census address, its rows, the price it must add up to."""
    def __init__(self, key, rows, total=None, note=None, rownote=None, extra=(), whole=False,
                 question=None):
        self.key, self.rows, self.total, self.note = key, rows, total, note
        self.rownote, self.extra, self.whole = rownote, extra, whole
        # Where the census's reading of the ask is cut short (a true/false
        # table read as its first statement): the question as the paper prints
        # it, line by line, PL / PLc selectors joined.
        self.question = question


class PaperCut:
    """The paper's printed line on `page` that opens with `opening`, cut at
    printed anchors (the question letter "(h) " off the front)."""
    def __init__(self, page, opening, after=None, before=None):
        self.line, self.after, self.before = PL(page, opening), after, before

    def text(self, doc):
        t = self.line.text(doc)
        if self.after is not None:
            if self.after not in t:
                raise ValueError(f'paper: {self.after!r} not in {t!r}')
            t = t.split(self.after, 1)[1]
        if self.before is not None:
            if self.before not in t:
                raise ValueError(f'paper: {self.before!r} not in {t!r}')
            t = t.split(self.before, 1)[0]
        return t.strip()


def PLc(page, opening, after=None, before=None):
    return PaperCut(page, opening, after, before)


class Verdict(Sel):
    """The column a true/false tick stands in, read from the scheme PDF: the
    heading word ("Verdadeiro", "Falso") whose printed span holds the tick
    set on the same row as the statement on scheme line n."""
    def __init__(self, n, page):
        super().__init__('scheme', n)
        self.page = page

    def text(self, doc):
        import fitz
        pdf = fitz.open(os.path.join(SCHEMES, f'{doc["year"]}-{doc["level"]}.pdf'))
        words = pdf[self.page - 1].get_text('words')
        statement = re.sub(r'\s*✓\s*$', '', doc['scheme'][self.n - 1]).strip()
        first = statement.split()[0]
        rows = [w for w in words if w[4] == first and w[0] < 200]
        hits = []
        for r in rows:
            line = ' '.join(x[4] for x in sorted(words, key=lambda x: x[0])
                            if abs(x[1] - r[1]) < 3 and x[0] < 300)
            if line.startswith(statement) or statement.startswith(line):
                hits.append(r)
        if len(hits) != 1:
            raise ValueError(f'scheme p{self.page}: {len(hits)} rows read {statement!r}')
        y = hits[0][1]
        # The column heads: the nearest row of them printed above this one.
        heads = [w for w in words if w[4] in ('Verdadeiro', 'Falso', 'True', 'False') and w[1] < y]
        if not heads:
            raise ValueError(f'scheme p{self.page}: no column heads above {statement!r}')
        top = max(w[1] for w in heads)
        heads = {w[4]: (w[0], w[2]) for w in heads if abs(w[1] - top) < 3}
        # The tick nearest this row by vertical centre, which must be nearer it
        # than any other row the table prints (a tick sits a few points lower
        # than its row's text: 2025 Ordinary p6 and p8).
        mid = lambda w: (w[1] + w[3]) / 2                              # noqa: E731
        row_mid = mid(hits[0])
        ticks = sorted((w for w in words if w[4] in ('\uf0fc', '\u2713', '\u2714')
                        and abs(mid(w) - row_mid) < 14), key=lambda w: abs(mid(w) - row_mid))
        if not ticks:
            raise ValueError(f'scheme p{self.page}: no tick beside {statement!r}')
        others = [mid(w) for w in words if w is not hits[0] and abs(w[0] - hits[0][0]) < 3
                  and abs(mid(w) - row_mid) > 3]
        if any(abs(o - mid(ticks[0])) < abs(row_mid - mid(ticks[0])) for o in others):
            raise ValueError(f'scheme p{self.page}: the tick nearest {statement!r} is nearer another row')
        ticks = ticks[:1]
        cx = (ticks[0][0] + ticks[0][2]) / 2
        col = [h for h, (x0, x1) in heads.items() if x0 - 10 <= cx <= x1 + 10]
        if len(col) != 1:
            raise ValueError(f'scheme p{self.page}: tick at x={cx:.0f} under {col} for {statement!r}')
        return col[0]


def V(n, page):
    return Verdict(n, page)


class InlineVerdict(Sel):
    """A tick set in the box AFTER its label on the same row ("True False ✓",
    2025 Higher Q2(j)(i)): the label printed immediately left of the tick, on
    scheme line n's row of page `page`."""
    def __init__(self, n, page):
        super().__init__('scheme', n)
        self.page = page

    def text(self, doc):
        import fitz
        pdf = fitz.open(os.path.join(SCHEMES, f'{doc["year"]}-{doc["level"]}.pdf'))
        words = pdf[self.page - 1].get_text('words')
        heads = [w for w in words if w[4] in ('Verdadeiro', 'Falso', 'True', 'False')]
        # A tick, or the checked box the 2024 schemes draw (U+F0FE; U+F063 is
        # the empty box beside the other label).
        ticks = [w for w in words if w[4] in ('\uf0fc', '\uf0fe', '✓', '✔')]
        found = []
        for t in ticks:
            row = [h for h in heads if abs(h[1] - t[1]) < 8 and h[2] <= t[0]]
            if len(row) >= 2:
                found.append(max(row, key=lambda h: h[2])[4])
        if len(found) != 1:
            raise ValueError(f'scheme p{self.page}: {len(found)} inline ticks after a label: {found}')
        line = doc['scheme'][self.n - 1]
        if found[0] not in line:
            raise ValueError(f'scheme line {self.n} does not print {found[0]!r}: {line!r}')
        return found[0]


def VI(n, page):
    return InlineVerdict(n, page)


def quoted(*sels):
    """A line the scheme prints over its answers, quoted for the student."""
    return lambda d: ' '.join(f'The scheme heads its answers “{x.text(d)}”.' for x in sels)


READING, LISTENING = {}, {}


# ------------------------------------------------------------- building ---
def _doc(year, level, P=None, aural=False):
    doc = scheme_doc(year, level)
    doc['year'], doc['level'] = year, level
    if P is not None:
        path = P.aural_path if aural else P.path
        doc['paper'] = [(l.page, l.text) for l in read_lines(path, P.furniture)]
    return doc


def _question(ask, spec, doc):
    if spec.question:
        return ' '.join(x.text(doc) for x in spec.question)
    q = TRAILING.sub('', ask.full_text).strip()
    if spec.extra:
        # Booklet lines are kept whole: a gap's rule is part of the question.
        q = ' '.join([q] + [x.text(doc).strip() for x in spec.extra])
    return q


def _check_total(spec, doc, total, where):
    if spec.total is not None:
        c, p, n = spec.total.read(doc)
        if c * p != total:
            raise ValueError(f'{where} {spec.key}: rows add to {total}, the scheme prints {n!r}')


def reading_cards(year, level):
    specs = READING.get((year, level), [])
    if not specs:
        return []
    P = EuPaper(year, level, SUBJECT)
    import eu_all
    asks = {a.key: a for a in P.all_asks()}
    doc = _doc(year, level, P)
    out = []
    for spec in specs:
        key = parse_key(spec.key)
        if key not in asks:
            raise ValueError(f'{year} {level} {spec.key}: the census prints no such ask')
        ask = asks[key]
        question = _question(ask, spec, doc)
        language = answer_language(SUBJECT, question)
        note = language_note(SUBJECT, language)
        if spec.rownote:
            note = f'{note} {spec.rownote(doc) if callable(spec.rownote) else spec.rownote}'
        rows, total = build_rows(doc, spec.rows, note, spec.key)
        if spec.whole:
            c, p, n = spec.total.read(doc)
            total = c * p
        else:
            _check_total(spec, doc, total, f'{year} {level}')
        card = {
            'id': card_id(year, level, key),
            'subjectId': SUBJECT,
            'level': LEVEL_WORD[level],
            'year': year,
            'section': key[0],
            'topicId': topic_for(SUBJECT, P.era, key[0], key[2]),
            'conceptId': concept_for(question),
            'questionRef': f'{year} {level.upper()} {key_label(key)}',
            'questionText': question,
            'tariffModel': {'kind': 'questionTotal' if spec.whole else 'fixed'},
            'totalMarks': total,
            'rows': rows,
            'notes': (f'The scheme prices this ask {total} {"mark" if total == 1 else "marks"}; '
                      f'the paper prints it on page {ask.page} of the question booklet.'
                      + (f' {spec.note}' if spec.note else '')),
        }
        lead = P.lead(ask.q)
        if lead and len(lead) >= 12:
            card['stem'] = lead
        source = eu_all.source_material(P, ask, SUBJECT, language, level, year)
        if source:
            card['sourceMaterial'] = source
        out.append(card)
    return out


def section_intro(doc):
    """{part: (title, the booklet's instruction under it)}, lifted."""
    out, part, buf = {}, None, []
    for page, text in doc['paper']:
        m = PARTE.match(text)
        if m:
            if part and part not in out:
                out[part] = buf
            part, buf = m.group(1), [text]
            continue
        if part and part not in out:
            if NUMBERED.match(text):
                out[part] = buf
                continue
            buf.append(text)
    if part and part not in out:
        out[part] = buf
    res = {}
    for k, v in out.items():
        title = [v[0]] + [t for t in v[1:] if not t.rstrip().endswith('.')]
        said = [t for t in v[1:] if t.rstrip().endswith('.')]
        res[k] = (' '.join(title), ' '.join(said))
    return res


def _listening_language(stem):
    if re.search(r'\bResponda\b.*\bem portugu[eê]s\b', stem):
        return 'Portuguese'
    if re.search(r'\bAnswer\b.*\bin English\b', stem):
        return ENGLISH_OR_IRISH
    raise ValueError(f'no answer language in {stem!r}')


# A booklet whose text layer hands back a wrong character for a ligature,
# fixed only where the printed page was rendered and read (as Polish's
# VERIFIED_FILE): 2024 Higher listening booklet p3, Parte A Q3, set in Calibri,
# prints "exercício físico" and its "fí" ligature reads back as U+0130 "İ"
# The 2024 Ordinary listening booklet p3, Parte A Q4, has the same font and
# fault twice: "beneİcios do exercício İsico" prints "benefícios do exercício
# físico". These are the only U+0130 in any Portuguese booklet (render
# checked 19 Nov 2026).
GLYPH_FIXES = {(2024, 'hl', 'aural'): {'\u0130': 'fí'},
               (2024, 'ol', 'aural'): {'\u0130': 'fí'}}


def _repair(year, level, booklet, text):
    for bad, good in GLYPH_FIXES.get((year, level, booklet), {}).items():
        text = text.replace(bad, good)
    return text


def _census_aural(year, level, P):
    """The listening asks as the census counts them: the walker's, with any
    ask it folds (paper_census.EU_FOLDED_ASKS) unfolded into the printed ones,
    each on the page of the ask it was folded into."""
    from types import SimpleNamespace
    import paper_census
    asks = {a.key: a for a in P.aural_asks()}
    fix = paper_census.EU_FOLDED_ASKS.get((SUBJECT, year, level))
    if not fix:
        return asks
    texts = paper_census.census_eu(SUBJECT, year, level)[1]
    page = asks[fix['folded'][0]].page
    for k in fix['folded']:
        asks.pop(k)
    for k in fix['asks']:
        asks[k] = SimpleNamespace(key=k, page=page, full_text=texts[k])
    return asks


def recording(year):
    with open(AUDIO, encoding='utf-8') as fh:
        return next(r for r in json.load(fh) if r['year'] == year)


def listening_cards(year, level):
    specs = LISTENING.get((year, level))
    if specs is None:
        raise KeyError(f'no listening spec for {year} {level}')
    P = EuPaper(year, level, SUBJECT)
    asks = _census_aural(year, level, P)
    doc = _doc(year, level, P, aural=True)
    intros = section_intro(doc)
    rec = recording(year)
    out, seen = [], set()
    for spec in specs:
        key = parse_key(spec.key)
        if key not in asks:
            raise ValueError(f'{year} {level} {spec.key}: the census prints no such ask')
        if key in seen:
            raise ValueError(f'{year} {level} {spec.key}: carded twice')
        seen.add(key)
        ask = asks[key]
        part = key[0][1]
        title, stem = intros[part]
        question = _repair(year, level, 'aural', _question(ask, spec, doc))
        language = _listening_language(stem)
        note = language_note(SUBJECT, language)
        if spec.rownote:
            note = f'{note} {spec.rownote(doc) if callable(spec.rownote) else spec.rownote}'
        rows, total = build_rows(doc, spec.rows, note, spec.key)
        if spec.whole:
            c, p, n = spec.total.read(doc)
            total = c * p
        else:
            _check_total(spec, doc, total, f'{year} {level}')
        suffix = (f'({key[2]})' if key[2] else '') + (f'({key[3]})' if key[3] else '')
        out.append({
            'id': card_id(year, level, key),
            'subjectId': SUBJECT,
            'level': LEVEL_WORD[level],
            'year': year,
            'section': key[0],
            'topicId': topic_for(SUBJECT, P.era, key[0]),
            'conceptId': concept_for(question),
            'questionRef': f'{year} {level.upper()} {key_label(key)}',
            'questionText': question,
            'tariffModel': {'kind': 'questionTotal' if spec.whole else 'fixed'},
            'totalMarks': total,
            'rows': rows,
            'notes': (f'The scheme prices this listening ask {total} '
                      f'{"mark" if total == 1 else "marks"}; the listening booklet prints it on '
                      f'page {ask.page}.' + (f' {spec.note}' if spec.note else '')),
            'stem': stem,
            'sourceMaterial': {
                'kind': 'source-text',
                'label': 'LISTENING COMPREHENSION',
                'title': f'{title} — Question {key[1]}{suffix}',
                'pages': [ask.page],
                'sourceLabel': 'Aural Paper',
                'attribution': (f'SEC Portuguese {year} {LEVEL_TITLE[level]} Level Listening '
                                f'Comprehension — © State Examinations Commission.'),
                'presentationNote': ('The question page of the listening booklet. '
                                     'Play the recording, then answer.'),
            },
            'audioMaterial': {**rec['source'], 'label': f'Parte {part} · listening'},
        })
    missing = sorted(set(asks) - seen, key=str)
    if missing:
        raise ValueError(f'{year} {level}: no card for {[key_label(k) for k in missing]}')
    printed, inside = {}, False
    for line in doc['raw']:
        t = line.strip()
        if t.startswith('Listening Comprehension'):
            inside = True
        if t.startswith('APPENDIX'):
            break
        m = SECTION_TOTAL.match(t) if inside else None
        if m and m.group(1) not in printed:
            printed[m.group(1)] = int(m.group(2))
    if set(printed) != {k[0][1] for k in asks}:
        raise ValueError(f'{year} {level}: Parte totals printed for {sorted(printed)}')
    for part, want in printed.items():
        got = sum(c['totalMarks'] for c in out if c['section'] == f'L{part}')
        if got != want:
            raise ValueError(f'{year} {level} Parte {part}: cards add to {got}, the scheme prints {want}')
    return out


# ================================================================ 2026 HL ===
# Scheme .md lines 92-226 (reading, pages 5-9) and 304-426 (listening, pages
# 12-16). Reading: Q1 and Q2 (a)-(f)/(e) in Portuguese, the rest in English.
# Listening: Partes A and B in Portuguese, C to E in English; each Parte 20.
READING[(2026, 'hl')] = [
    C('A1a', [menu([S(97), S(98)], T(97))]),
    # (e): two answers at "4 marks" (any 1) and a third the scheme prints as a
    # bullet of its own at "2 marks".
    C('A1e', [menu([J(S(126), S(127)), S(129)], T(127), [alt(S(130), T(130))])], total=T(127)),
    C('A1f', pairs(range(133, 138), 132, after=')'), total=T(132)),
    C('A1h', [stepped(S(146), T(146))]),
    C('A1j', [menu([S(158), S(159), S(160), S(161), S(162), J(S(163), S(164))], T(161))]),
    C('A2a', [stepped(J(S(172), S(173), S(174)), T(173))]),
    C('A2c', [stepped(S(182), T(182))]),
    C('A2d', [stepped(J(S(184), S(185)), T(185))]),
    C('A2f', [stepped(J(S(197), S(198)), T(197))]),
]

LISTENING[(2026, 'hl')] = [
    C('LA1', [stepped(S(307), T(307))]),
    C('LA2', [menu([S(309), S(310), S(312)], T(310))]),
    C('LA3', [stepped(J(S(314), S(315)), T(314))]),
    C('LA4', [stepped(J(S(317), S(318)), T(317))]),
    C('LA5', [stepped(J(S(321), S(322), S(323)), T(322))]),
    C('LA6', [one(S(325), T(325))]),
    C('LB1', [menu([S(332), S(333), S(334), S(336), S(337)], T(334))]),
    C('LB2', [menu([J(S(339), S(340)), J(S(341), S(342))], T(340))]),
    C('LB3', [stepped(J(S(344), S(345)), T(344))]),
    C('LB4', [stepped(S(347), T(347))]),
    C('LB5', [stepped(J(S(349), S(350), S(351), S(352)), T(350))]),
    C('LB6', [menu([S(354, before=', preços'), S(354, after='Horários, ', before=' e concursos'),
                    S(354, after='bilhetes e ')], T(354))]),
    C('LC1', [menu([S(362), S(363), S(365)], T(363))]),
    C('LC2', [stepped(J(S(367), S(368)), T(367))]),
    C('LC3', [stepped(J(S(370), S(371)), T(370))]),
    C('LC4', [menu([S(373, before=', secretary'), S(373, after='elderly, ', before=', sales'),
                    S(373, after='secretary, ', before=', customer'), S(373, after='assistant, ')],
                   T(373))]),
    C('LC5', [menu([S(375, before=', be positive'), S(375, after='calm, ', before=', focus'),
                    S(375, after='positive, ', before=' and be'),
                    J(S(375, after='kind and '), S(376))], T(375))]),
    C('LC6', [stepped(S(378), T(378))]),
    C('LD1', [menu([S(385), S(386)], T(386))]),
    C('LD2', [menu([S(388, before=', their'), S(388, after='speaks, ', before=' and cultural'),
                    S(388, after='humour and ', before=' 4 marks')], T(388))]),
    C('LD3', [stepped(S(390), T(390))]),
    C('LD4i', [stepped(S(393), T(393))]),
    C('LD4ii', [menu([S(395, before=', varied'), S(395, after='stories, ', before=', different'),
                      S(395, after='characters, ', before=' and type'),
                      S(395, after='accents and ')], T(395))]),
    C('LD5', [menu([J(S(398), S(399)), S(401)], T(399))]),
    C('LD6', [one(S(403), T(403))]),
    C('LE1', [menu([S(410), S(411)], T(410))]),
    C('LE2', [menu([S(413, before=', plastic'), S(413, after='cartons, ', before=', hot'),
                    S(413, after='bottles, ', before=' and markers'), S(413, after='glue and ')],
                   T(413))]),
    C('LE3', [stepped(S(415), T(415))]),
    C('LE4', [stepped(J(S(417), S(418)), T(418))]),
    C('LE5', [stepped(S(420), T(420))]),
    C('LE6i', [one(S(423), T(423))]),
    C('LE6ii', [stepped(S(425), T(425))]),
]


# ================================================================ 2026 OL ===
# Scheme .md lines 95-223 (reading, pages 5-9) and 263-385 (listening, pages
# 11-15). Listening: Partes A and B in Portuguese, C to E in English; each 24.
READING[(2026, 'ol')] = [
    C('A1c', [menu([J(S(109), S(110)), J(S(111), S(112))], T(110))]),
    C('A1e', pairs([118, 119, 121, 122], 120, after=')'), total=T(120)),
    C('A1f', [menu([S(130, before=', and'), S(131)], T(131))]),
    # (a): the scheme prints a second, shorter answer on its own line at
    # "2 marks", with no "ou" or "or": an answer of its own.
    C('A2a', [menu([S(154)], T(154), [alt(S(155), T(155))])]),
    C('A2d', [menu([S(164, before=', Dia'), S(164, after='Aniversários, ', before=' e chá'),
                    S(164, after='Mulheres e ')], T(164))]),
    C('A2e', [stepped(J(S(167), S(168)), T(167))]),
    C('A2f', pairs([170, 171, 173, 174], 172, after=')'), total=T(172)),
    C('A2i', [stepped(J(S(190), S(191)), T(190))]),
    C('A3c', [menu([S(211, before=' e '), S(211, after=' e ')], T(211))]),
    # (d): "6 marks" for the question and no split printed (CARD-STANDARD 5).
    C('A3d', [shown(S(213)), shown(S(214))], total=T(213), whole=True,
      note='The scheme prices the question as a whole and prints no split between its answers.'),
    C('A3e', [stepped(S(217), T(217))]),
]

LISTENING[(2026, 'ol')] = [
    # Fill-ins: one row per gap, each at the per-gap price, led by the
    # scheme's completed sentence.
    C('LA1', [one(S(266, after='está ', before=' porque'), T(266, each=True), lead=J(S(266), S(267))),
              one(S(266, after='problema ', before=' com'), T(266, each=True), lead=J(S(266), S(267)))],
      total=T(266), extra=(PL(3, 'O voo está'), PL(3, 'escadas do avião'))),
    C('LA2', [stepped(S(269), T(269))]),
    C('LA3', [menu([S(271, before=' / aniversário de 100'), S(271, after='família / ', before=' / aniversário da'),
                    S(271, after='anos / ', before=' / festa'), J(S(271, after='avó / '), S(272))],
                   T(271))]),
    C('LA4', [one(S(275, after='avó '), T(276, each=True), lead=S(275, before=' Brasil')),
              one(S(277, before=' Moçambique'), T(276, each=True), lead=S(277, after='Primos ')),
              one(S(278, before=' Guiné-Bissau'), T(276, each=True), lead=S(278, after='Tios '))],
      total=T(276)),
    C('LA5', [menu([S(280, before=', balcão'), S(280, after='informações, ', before=','), S(281)], T(281))]),
    C('LA6', [one(S(284, after='em ', before=' neste'), T(285, each=True), lead=S(284)),
              one(S(284, after='corredor da ', before='.'), T(285, each=True), lead=S(284)),
              one(S(285, after='na ', before=' à'), T(285, each=True), lead=S(285)),
              one(S(285, after='à ', before='.'), T(285, each=True), lead=S(285)),
              one(S(286, after='ao ', before=' da'), T(285, each=True), lead=S(286)),
              one(S(286, after='lado da ', before=' de embarque'), T(285, each=True), lead=S(286))],
      total=T(285), extra=(PL(3, 'Segues'), PL(3, 'Viras'), PL(3, 'Mesmo ao'))),
    C('LB1', [one(S(293, after='De ', before=' a '), T(293, each=True), lead=S(293)),
              one(S(293, after=' a ', before=' de'), T(293, each=True), lead=S(293)),
              one(S(293, after='23 de ', before='.'), T(293, each=True), lead=S(293))],
      total=T(293)),
    # True/false: the verdict is the column heading the tick stands under on
    # scheme p12, read by position (Verdict).
    C('LB2', [one(V(n, 12), T(295, each=True), lead=S(n, before=' ✓')) for n in range(298, 305)],
      total=T(295)),
    C('LB3', [menu([S(306, before=', pousadas'), S(306, after='Hotéis, ', before=', turismo'),
                    S(306, after='pousadas, ', before=', casas'), S(306, after='rural, ')], T(306))]),
    C('LB4', [menu([S(309, before=', transporte'), S(309, after='carro, ', before=', rede'),
                    S(309, after='público, ')], T(309))]),
    C('LB5', [menu([S(312, before='; preços'), S(312, after='Horários; ', before=' e concursos'),
                    S(312, after='bilhetes) e ')], T(312))]),
    C('LC1', [one(S(322, after='medicine '), T(320), lead=S(323))]),
    C('LC2', [stepped(J(S(326), S(327)), T(326))]),
    C('LC3', [menu([S(330, after='Childminder ', before=' ✓'), S(330, after='assistant ✓ ', before=' ✓')], T(329))],
      extra=(PL(5, 'Childminder'), PL(5, 'Sales assistant'), PL(5, 'Customer service'), PL(5, 'Waitress'))),
    C('LC4', [menu([S(332, before='; positive'), S(332, after='Calm; ', before='; responsible'),
                    S(332, after='(personality); ', before='; honest'), S(332, after='responsible; ', before='; patient'),
                    S(332, after='honest; ', before='; good'), J(S(332, after='patient; '), S(333, before='; punctual')),
                    S(333, after='listener; ', before='; team'), S(333, after='punctual; ', before='; she'),
                    J(S(333, after='player; '), S(335))], T(333))]),
    C('LC5', [stepped(J(S(337), S(338)), T(338))]),
    C('LD1', [menu([S(345, before=', comedy'), S(345, after='Humour, ', before=' and premieres'),
                    S(345, after='shows and ')], T(345))]),
    C('LD2', [menu([S(348, before=', Brazilian'), S(348, after='Angolan, ', before=' and'),
                    S(348, after='Brazilian and ')], T(348))]),
    C('LD3', [stepped(S(351), T(351))]),
    C('LD4', [menu([S(353, before=', several'), S(353, after='stories, ', before=', and'),
                    S(353, after='characters, and ')], T(353))]),
    C('LD5', [menu([S(356, before=' ✓'), S(359, before=' ✓')], T(355))],
      extra=(PL(6, 'The show was boring'), PL(6, 'They invited'), PL(6, 'They made new jokes'))),
    C('LE1', [menu([S(366, before=', create'), S(366, after='presentation, ', before=', a leaflet'),
                    S(366, after='posters, ', before=', and'), S(366, after='leaflet, and ')], T(366))]),
    C('LE2', [menu([S(370, before=' ✓ Glass'), S(370, after='Glass bottles ', before=' ✓ News')],
                   T(369))]),
    C('LE3', [stepped(S(372), T(372))]),
    C('LE4', [stepped(J(S(374), S(375)), T(374))]),
    C('LE5i', [one(S(378), T(378))]),
    C('LE5ii', [one(S(380), T(380))]),
    C('LE6i', [one(S(383), T(383))]),
    C('LE6ii', [stepped(S(385), T(385))]),
]


# ================================================================ 2025 HL ===
# Live: 18 reading cards (eu_all). New here: the three reading asks it refused,
# and the listening test (scheme .md lines 279-411, pages 11-15; each Parte 20,
# Parte B's head printing a bare "20"). Written tasks held (lower scale).
READING[(2025, 'hl')] = [
    C('A1b-ii', [menu([S(106, before=' Vão'), S(106, after='família. '), S(107)], T(106))]),
    # A numbering task: one row per printed piece of information, each led by
    # it, its answer the part the scheme numbers it with.
    C('A1i', [one(S(n, before=' ' + w), T(142, each=True), lead=S(n, after=f'Part {k} '))
              for n, k, w in [(143, 4, 'New'), (144, 3, 'Online'), (145, 1, 'Like'), (146, 2, 'Unexpected')]],
      total=T(142), extra=(PL(7, 'New perspectives'), PL(7, 'Online friendship'),
                           PL(7, 'Like grandmother'), PL(7, 'Unexpected news'))),
    # True/false: the tick stands in the box after "False" (scheme p8).
    C('A2j-i', [one(VI(202, 8), T(202))]),
]

LISTENING[(2025, 'hl')] = [
    C('LA1', [stepped(S(282), T(282))]),
    C('LA2', [stepped(S(284), T(284))]),
    C('LA3', [menu([S(286), S(287), S(288), S(290), S(291)], T(288))]),
    C('LA4', [stepped(S(293), T(293))]),
    C('LA5', [stepped(J(S(295), S(296)), T(296))]),
    C('LA6', [one(S(298), T(298))]),
    C('LB1', [stepped(J(S(306), S(307)), T(306))]),
    C('LB2', [stepped(S(309), T(309))]),
    C('LB3', [stepped(S(312), T(312))]),
    # "4 marks" for the question and no split printed (CARD-STANDARD 5).
    C('LB4', [shown(S(314)), shown(S(316))], total=T(315), whole=True,
      note='The scheme prices the question as a whole and prints no split between its answers.'),
    C('LB5', [menu([S(318), S(319), S(320), S(321), J(S(322), S(323))], T(320))]),
    C('LC1', [stepped(J(S(330), S(331)), T(330))]),
    C('LC2', [one(S(333), T(333))]),
    C('LC3', [menu([S(335), S(336), S(337), S(338), S(339)], T(337))]),
    C('LC4', [stepped(J(S(341), S(342)), T(341))]),
    C('LC5', [stepped(S(344), T(344))]),
    C('LC6', [menu([S(346), S(347), S(348), S(350), S(351)], T(348))]),
    # The table: every cell is asked (the booklet prints only its two heads).
    C('LD1', [one(S(n, before=' ' + w), T(358, each=True), lead=S(359, before=' How long'))
              if half == 0 else
              one(S(n, after=w0 + ' '), T(358, each=True), lead=S(359, after='there? '))
              for n, w, w0 in [(360, 'Half', 'Train'), (361, '20', 'Metro'), (362, '10', 'Walking')]
              for half in (0, 1)], total=T(358)),
    C('LD2', [stepped(S(364), T(364))]),
    # Three answers at the full 4 marks: the first priced "4 marks: 2 x 2
    # marks", the other two "4 marks". One is claimed.
    C('LD3', [menu([S(366), S(367), S(368)], T(367))],
      rownote=lambda d: (f'The scheme prices “{S(366).text(d)}” “{T(366).read(d)[2]}” and each '
                         f'of the other two “{T(367).read(d)[2]}”.')),
    C('LD4', [menu([S(370), S(371), S(372), S(373), S(374)], T(372))]),
    C('LD5', [one(S(376), T(376))]),
    C('LD6', [stepped(S(378), T(378))]),
    C('LE1', [menu([S(387), S(388), S(389)], T(388))], rownote=quoted(S(386))),
    C('LE2', [stepped(J(S(391), S(392)), T(391))]),
    C('LE3', [menu([S(394), S(395), S(396), S(398), S(399)], T(396))]),
    C('LE4', [menu([S(402), S(403), S(404), S(405), S(406)], T(403))], rownote=quoted(S(401))),
    C('LE5', [stepped(B(J(S(408), S(409)), S(410), S(411)), T(409))]),
]


# ================================================================ 2025 OL ===
# Live: 16 reading cards. New: the seven reading asks eu_all refused and the
# listening test (scheme .md lines 306-430, pages 12-16; heads "Part A" ...,
# each 24). Many prices are split over two lines: "⟨4 marks:⟩" / "⟨4 x 1
# mark⟩" (T2). Written tasks held (lower scale).
READING[(2025, 'ol')] = [
    # A numbering task: each event's printed position is its answer.
    C('A1d', pairs([113, 114, 115, 116], T2(114, 115, each=True), after='. '), total=T2(114, 115),
      extra=(PL(4, 'O trabalho parou'), PL(4, 'Os colegas ficaram'), PL(4, 'Senhor Google Pacheco desapareceu'))),
    # True/false: the verdict is the column the tick stands under (scheme p6).
    C('A1h', [one(V(145, 6), T2(142, 143, each=True), lead=S(145, before=' ✓')),
              one(V(146, 6), T2(142, 143, each=True), lead=J(S(146, before=' ✓'), S(147))),
              one(V(148, 6), T2(142, 143, each=True), lead=S(148, before=' ✓')),
              one(V(149, 6), T2(142, 143, each=True), lead=S(149, before=' ✓'))], total=T2(142, 143),
      question=(PL(5, 'True or False? Tick'), PLc(5, '(h)', after='(h) '),
                PL(5, 'The owner of the company travelled'), PL(5, 'The owner of the company had'),
                PL(5, 'with Google'), PL(5, 'Some colleagues'), PL(5, 'Everyone agreed'))),
    C('A2f-i', [one(V(n, 8), T2(188, 189, each=True), lead=S(n, before=' ✓')) for n in range(191, 195)],
      total=T2(188, 189),
      question=(PLc(8, '(f) True', after='(f) '), PLc(8, '(i) Tick', after='(i) '),
                PL(8, '1. Lucas'), PL(8, '2. Lucas'), PL(8, '3. Teresa'), PL(8, '4. There'))),
    C('A2f-ii', [menu([S(196), S(197)], T2(197, 198))],
      question=(PLc(8, '(f) True', after='(f) '), PL(8, '1. Lucas'), PL(8, '2. Lucas'),
                PL(8, '3. Teresa'), PL(8, '4. There'), PLc(8, '(ii) Number', after='(ii) '))),
    # Four numbered steps priced "6 marks: 6 x 1 mark" with no split between
    # them: one answer, placed on the printed steps. Quoted in the scheme's
    # own reading order, its step numbers included.
    C('A2g', [stepped(J(S(201), S(202), S(203), S(204), S(205), S(206)), T2(203, 204))]),
    # Two columns, "Any 3" each, under "12 marks: 6 x 2 marks".
    C('A3b', [menu([S(227), S(228), S(229), S(230)], AnyOf(T2(224, 225), 228), lead=S(226)),
              menu([S(232), S(233), S(234), S(235), S(236)], AnyOf(T2(224, 225), 233), lead=S(231))],
      total=T2(224, 225),
      question=(PLc(10, '(b) Preencha', after='(b) '), PL(10, 'Brasileiros em Portugal'),
                PL(10, 'Portugueses no Brasil'))),
]

LISTENING[(2025, 'ol')] = [
    C('LA1i', [one(S(310, after='Semana: '), T(310), lead=S(310, before=': domingo')),
               one(S(311, after='Data: '), T(311), lead=S(311, before=': 18'))],
      extra=(PL(3, 'Dia da semana'), PL(3, 'Data:'))),
    C('LA1ii', [one(S(313), T(313))]),
    C('LA2', [one(S(315, after='Peso: '), T2(316, 317, each=True), lead=S(315, before=': até')),
              one(S(316, after='1. '), T2(316, 317, each=True), lead=S(316, before=': 1.')),
              one(S(317, after='2. '), T2(316, 317, each=True), lead=S(316, before=': 1.')),
              one(S(318, after='Alimentação: '), T2(316, 317, each=True), lead=S(318, before=': vegetariano'))],
      total=T2(316, 317), extra=(PL(3, '2.'), PL(3, 'Alimentação'))),
    C('LA3', [one(S(320, after='estava ', before=', mas'), T2(320, 321, each=True), lead=J(S(320), S(321))),
              one(S(321, before=' e por isso'), T2(320, 321, each=True), lead=J(S(320), S(321))),
              one(S(321, after='por isso ', before='.'), T2(320, 321, each=True), lead=J(S(320), S(321)))],
      total=T2(320, 321), extra=(PL(3, 'As autoridades'), PL(3, 'mas'), PL(3, 'e por isso'))),
    C('LA4', [one(S(323), T2(323, 324))]),
    C('LB1', [one(S(331), T(331))]),
    C('LB2', [one(S(333), T(333))]),
    C('LB3', [stepped(S(335), T2(335, 336))]),
    # Two answers printed for "6 marks: 3 x 2 marks": each at 2, and the 2 the
    # scheme pays beyond them on the unprinted row (CARD-STANDARD 3).
    C('LB4', [one(S(338), T2(338, 339, each=True)), one(S(339), T2(338, 339, each=True)),
              rest(T2(338, 339), 2)], total=T2(338, 339)),
    C('LB5', [one(S(341), T(341))]),
    # The paper asks for two details and the scheme prints "(any 2)", but
    # prices the question "6 marks: 3 x 2 marks": the printed price is carded
    # (CARD-STANDARD 5) and the conflict quoted.
    C('LB6', [menu([S(343), S(344), S(345), J(S(346), S(347))], T2(344, 345))],
      rownote=lambda d: (f'The paper asks for two details and the scheme prints “(any 2)”, but it '
                         f'prices the question “{T2(344, 345).read(d)[2]}”; the printed price is carded.')),
    C('LC1', [one(S(354), T(354))]),
    C('LC2', [menu([S(356), S(357), S(358), S(359), S(360)], T2(357, 358))]),
    C('LC3', [menu([S(362), S(363), S(364), S(366)], T2(363, 364))]),
    C('LC4', [stepped(S(368), T2(368, 369))]),
    C('LC5', [menu([S(371), S(372), S(373), S(375)], T2(372, 373))]),
    # A second answer on a line of its own at "1 mark", no "or": an answer of
    # its own.
    C('LC6', [menu([S(377)], T(377), [alt(S(378), T(378))])]),
    C('LD1', [one(S(385), T(385))]),
    C('LD2', [menu([S(387), S(388), S(389), S(390)], T2(387, 388))]),
    C('LD3', [one(S(392), T(392))]),
    C('LD4', [menu([S(394), S(395)], T2(394, 395))]),
    C('LD5', [menu([S(397), S(398)], T2(397, 398))]),
    C('LD6', [one(S(400, before=' ✓'), T(400))], extra=(PL(6, 'True'), PL(6, 'False'))),
    C('LE1', [menu([S(407), S(408), S(409)], T2(407, 408))]),
    C('LE2', [menu([S(n) for n in range(411, 418)], T2(413, 414))]),
    C('LE3', [stepped(S(419), T2(419, 420))]),
    C('LE4i', [stepped(J(S(424), S(425)), T2(423, 425))]),
    C('LE4ii', [menu([S(427), S(428), S(429), S(430)], T2(428, 429))]),
]


# ================================================================ 2024 HL ===
# Live: 21 reading cards. New: the two reading asks eu_all refused and the
# listening test (scheme .md lines 271-386, pages 11-15; heads "Part A" ...,
# each 20). The census unfolds Parte C Q3 into (a)(i)-(b)(ii) (paper_census
# EU_FOLDED_ASKS). Written tasks: pt_writing.py.
READING[(2024, 'hl')] = [
    # "What?" and "Why?" answered under one "6 marks: 3 x 2 marks".
    C('A1i', [stepped(J(S(153), S(155)), T(154))]),
    # A numbering task: each sentence's printed position, read from the cell
    # the scheme prints beside it ("⟨4⟩").
    C('A2j', [one(CELL(209), T(208, each=True), lead=S(209)),
              one(CELL(210), T(208, each=True), lead=S(210)),
              one(CELL(211), T(208, each=True), lead=J(S(211), S(212))),
              one(CELL(213), T(208, each=True), lead=S(213)),
              one(CELL(214), T(208, each=True), lead=S(214))], total=T(208),
      question=(PLc(10, '(j) Number', after='(j) '), PL(10, 'The Tamar project connects'),
                PL(10, 'Only a small'), PL(10, 'The Tamar project is one'), PL(10, 'initiatives.'),
                PL(10, 'The Tamar project is an'), PL(10, 'The Tamar project rescues'))),
]

LISTENING[(2024, 'hl')] = [
    C('LA1i', [stepped(S(275), T(275))]),
    C('LA1ii', [one(S(277), T(277))]),
    # Six printed answers set as one slash-separated list, "any 3".
    C('LA2', [menu([S(280, before=' / Os amigos'), S(280, after='pessoal / ', before=' / Os aparelhos'),
                    S(280, after='que fez / ', before=' /'), S(281, before=' / É perto'),
                    S(281, after='aulas / ', before=' / Não'), J(S(281, after='dela / '), S(283))], T(281))]),
    C('LA3', [menu([S(285, before=' / Melhorar'), S(285, after='forma / ', before=' / Ter'),
                    S(285, after='mental / ')], T(285))]),
    C('LA4', [one(S(287, after='Aula: '), T(287, each=True), lead=S(287, before=': Ioga')),
              one(S(288, after='Horário: '), T(287, each=True), lead=S(288, before=': 8'))], total=T(287)),
    C('LA5', [stepped(J(S(290), S(291)), T(291))]),
    C('LB1', [one(S(298, after='Cidade: '), T(298, each=True), lead=S(298, before=': Maputo')),
              one(S(299, after='Idade: '), T(298, each=True), lead=S(299, before=': seis'))], total=T(298)),
    C('LB2', [menu([S(302, before=', pintura'), S(302, after='Dança, ', before=', escrita'),
                    S(302, after='pintura, ', before=' e ritmos'), S(302, after='escrita e ')], T(302))]),
    # A four-gap sentence: one row per gap, led by the completed sentence.
    C('LB3', [one(S(305, after='década de ', before=', trabalhou'), T(305, each=True), lead=J(S(305), S(306))),
              one(S(305, after='(70), ', before=' como'), T(305, each=True), lead=J(S(305), S(306))),
              one(S(306, before=' na Cruz'), T(305, each=True), lead=J(S(305), S(306))),
              one(S(306, after='Cruz ', before='.'), T(305, each=True), lead=J(S(305), S(306)))],
      total=T(305)),
    C('LB4', [stepped(S(308), T(308))]),
    # Title and year priced together "4 marks: 4 x 1 mark", no split between
    # them: one answer on the printed steps.
    C('LB5', [stepped(B(S(310), S(311)), T(311))]),
    C('LB6', [one(S(313), T(313))]),
    C('LC1i', [one(S(320), T(320))], question=(PLc(5, '1. (i) Why', after='1. (i) '),)),
    # Two answers at the full 2 marks, the first split "2 x 1": one claimed.
    C('LC1ii', [menu([S(322), S(323)], T(323))], question=(PLc(5, '(ii) Why does', after='(ii) '),),
      rownote=lambda d: (f'The scheme prices “{S(322).text(d)}” “{T(322).read(d)[2]}” and '
                         f'“{S(323).text(d)}” “{T(323).read(d)[2]}”.')),
    C('LC2i', [one(S(325), T(325))], question=(PLc(5, '2. (i) Who', after='2. (i) '),)),
    C('LC2ii', [one(S(327), T(327))], question=(PLc(5, '(ii) How long', after='(ii) '),)),
    C('LC3a-i', [one(S(331), T(331))]),
    C('LC3a-ii', [menu([S(333, before=', dinner'), S(333, after='hotel, ', before=', live'),
                        S(333, after='dinner, ')], T(333))]),
    C('LC3b-i', [menu([S(336, before=' and traditional'), S(336, after='tour and ')], T(336))]),
    C('LC3b-ii', [one(S(338), T(338))]),
    C('LC4', [menu([S(340, before=', hotel'), S(340, after='Cruise, ', before=', trips'),
                    S(340, after='hotel, ', before=', visits'), S(340, after='trips, ', before=', meals'),
                    S(340, after='visits, ')], T(340))]),
    C('LC5', [stepped(S(343), T(343))]),
    C('LD1', [stepped(S(350), T(350))]),
    C('LD2i', [one(S(352), T(352))]),
    C('LD2ii', [menu([S(354, before=', corn'), S(354, after='skin, ', before=', bamboo'),
                      S(354, after='fibre, ', before=' and soy'), S(354, after='bamboo and ')], T(354))]),
    C('LD3i', [menu([S(357, before=', sustainability'), S(357, after='Transparency, ', before=' and'),
                     S(357, after='sustainability and ')], T(357))],
      question=(PLc(6, '3. (i) Name', after='3. (i) '),)),
    C('LD3ii', [menu([S(359, before=' and in'), S(359, after='Online and ')], T(359))],
      question=(PLc(6, '(ii) Where can', after='(ii) '),)),
    # The table: every cell the booklet leaves blank, "6 marks: 6 x 1 mark
    # (any 6)".
    C('LD4', [one(S(361, after='State: '), T(363, each=True), lead=S(361, after='Location ', before=': Mato')),
              one(S(362, after='Country: '), T(363, each=True), lead=S(362, before=': Brazil')),
              one(S(363, after='1. '), T(363, each=True), lead=S(364, before=' 2.')),
              one(S(364, after='2. '), T(363, each=True), lead=S(364, before=' 2.')),
              one(S(365, after='3. '), T(363, each=True), lead=S(364, before=' 2.')),
              one(S(366, after='Material '), T(363, each=True), lead=S(366, before=' Organic'))],
      total=T(363), extra=(PL(6, 'Location'), PL(6, 'State: Country:'), PL(6, 'Products'),
                           PL(6, 'Type of'), PL(6, 'Material'))),
    # "To help animals." at 1 mark under the fuller answer's "2 x 1": a
    # partial of the same point, quoted beside it.
    C('LE1i', [stepped(S(373), T(373))]),
    C('LE1ii', [stepped(S(375), T(375))],
      rownote=lambda d: f'The scheme also allows “{S(376).text(d)}” for {T(376).read(d)[1]} mark.'),
    C('LE2', [menu([S(378, before=', shelter'), S(378, after='Food, ', before=' and'),
                    S(378, after='shelter and ')], T(378))]),
    C('LE3', [menu([S(380, before=' and best'), S(380, after='superhero and ')], T(380))]),
    C('LE4', [one(S(382, after='Date: ', before=', 5th'), T(382, each=True), lead=S(382, before=': Friday')),
              one(S(382, after='Friday, ', before='.'), T(382, each=True), lead=S(382, before=': Friday')),
              one(S(383, after='From: ', before=' To:'), T(382, each=True), lead=S(383, before=': 7pm')),
              one(S(383, after='To: '), T(382, each=True), lead=S(383, after='19h ', before=': midnight'))],
      total=T(382), extra=(PL(7, 'Date:'), PL(7, 'From:'), PL(7, 'To:'))),
    C('LE5', [menu([S(386, before=', dance'), S(386, after='Music, ', before=', food'),
                    S(386, after='floor, ', before=' and drink'), S(386, after='food and ')], T(386))]),
]


# ================================================================ 2024 OL ===
# Live: 22 reading cards. New: Q1(e) (true/false) and the listening test
# (scheme .md lines 255-363, pages 10-14; heads "Part A" ..., each 24). The
# 2024 scheme draws a checked box (U+F0FE) after the label it ticks.
READING[(2024, 'ol')] = [
    C('A1e', [one(VI(116, 5), T(116))]),
]

LISTENING[(2024, 'ol')] = [
    # A second answer on a line of its own at "2 marks", no "ou": an answer
    # of its own.
    C('LA1', [menu([S(258)], T(258), [alt(S(259), T(259))])]),
    C('LA2', [one(S(262), T(262))]),
    C('LA3', [menu([S(265), S(266), S(267), S(268)], T(266))]),
    C('LA4', [menu([S(270, before=' ✓'), S(272, before=' ✓')], T(271))],
      extra=(PL(3, 'Aumenta'), PL(3, 'Diminui'), PL(3, 'Melhora'), PL(3, 'Piora'))),
    C('LA5', [one(S(276, after='Marina: '), T(277, each=True), lead=S(276, before=': 7')),
              one(S(277, after='Pedro: '), T(277, each=True), lead=S(277, before=': 8'))],
      total=T(277), extra=(PL(3, 'Marina:'), PL(3, 'Pedro:'))),
    C('LA6', [one(S(279, after='Aula: ', before=' Horário'), T(279, each=True), lead=S(279, before=': Ioga')),
              one(S(279, after='Horário: ', before=' Sala'), T(279, each=True),
                  lead=S(279, after='Yoga ', before=': 8')),
              one(S(279, after='Sala: '), T(279, each=True), lead=S(279, after='8:30 ', before=': 3'))],
      total=T(279)),
    C('LB1', [one(S(286), T(286))]),
    C('LB2', [one(S(289), T(289))]),
    C('LB3', [one(VI(291, 11), T(291))]),
    C('LB4', [one(S(293, after='Alguns ', before=' depois'), T(293, each=True), lead=J(S(293), S(294))),
              one(S(293, after='depois, ', before=' seus'), T(293, each=True), lead=J(S(293), S(294))),
              one(S(293, after='seus ', before=' contos'), T(293, each=True), lead=J(S(293), S(294))),
              one(S(293, after='contos em '), T(293, each=True), lead=J(S(293), S(294)))],
      total=T(293), extra=(PL(4, 'Alguns'), PL(4, '___'))),
    C('LB5', [one(S(296), T(296))]),
    C('LB6', [one(S(298), T(298))]),
    C('LB7', [one(S(300), T(300))]),
    C('LC1', [one(S(310, before=' ✓'), T(308))]),
    C('LC2', [one(S(312, after='Who: ', before=' When'), T(312, each=True), lead=S(312, before=': Her')),
              one(S(312, after='When: '), T(312, each=True), lead=S(312, after='family. ', before=': Next'))],
      total=T(312), extra=(PL(5, 'Who:'), PL(5, 'When:'))),
    C('LC3', [one(VI(314, 12), T(314))]),
    C('LC4', [one(S(316), T(316))]),
    C('LC5', [menu([S(318), S(319), S(320), S(321), S(322)], T(319))]),
    C('LC6', [one(S(324), T(324))]),
    C('LD1', [one(S(331), T(331))]),
    C('LD2', [one(S(333), T(333))]),
    C('LD3', [one(S(336), T(336))]),
    C('LD4', [menu([S(338, before=', corn'), S(338, after='(skin), ', before=', bamboo'),
                    S(338, after='corn, ', before=' and soya'), S(338, after='bamboo and ')], T(338))]),
    C('LD5', [menu([S(341, before=' and women'), S(341, after='male and ')], T(341))]),
    # Five cells printed for "6 marks: 6 x 1 mark": each at 1, and the mark
    # the scheme pays beyond them on the unprinted row (CARD-STANDARD 3).
    C('LD6', [one(S(343, after='Country: '), T(345, each=True), lead=S(343, after='Location ', before=': Brazil')),
              one(S(344, after='1. '), T(345, each=True), lead=S(345, before=' 2.')),
              one(S(345, after='2. '), T(345, each=True), lead=S(345, before=' 2.')),
              one(J(S(346, after='3. '), S(347)), T(345, each=True), lead=S(345, before=' 2.')),
              one(S(348, after='Material '), T(345, each=True), lead=S(348, before=' Organic')),
              rest(T(345), 5)],
      total=T(345),
      question=(PLc(6, '6. Fill', after='6. '), PL(6, 'Country:'), PL(6, 'Products'),
                PL(6, 'Type of'), PL(6, 'Material'))),
    C('LE1', [one(VI(355, 14), T(355))]),
    C('LE2', [stepped(S(357), T(357))]),
    C('LE3', [menu([S(359, before=', shelter'), S(359, after='Food, ', before=' and'),
                    S(359, after='shelter and ')], T(359))]),
    C('LE4', [menu([S(361, before=' and villains'), S(361, after='Superheroes and ')], T(361))]),
    C('LE5', [menu([S(363, before=', dance'), S(363, after='Music, ', before=', food'),
                    S(363, after='floor, ', before=' and drink'), S(363, after='food and ')], T(363))]),
]


# ----------------------------------------------------------------- CLI ----
def _show(cards):
    for c in cards:
        print(f"== {c['questionRef']} [{c['totalMarks']}] {c['tariffModel']['kind']}")
        print(f"   Q: {c['questionText']}")
        for r in c['rows']:
            g = r.get('group')
            if g:
                om = g.get('optionMarks')
                print(f"   anyN {g['claimMax']} x {g['perOption']}" + (f" marks={om} of={g.get('optionOf')}" if om else '')
                      + ': ' + ' || '.join(g['options']))
            else:
                print(f"   {r['kind']} {r['marks']} {r.get('permittedMarks', '')}: {r['verbatim']}")
            if r.get('contextNote'):
                print(f"     note: {r['contextNote']}")


def main():
    cmd, year, level = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    if cmd == 'cards':
        _show(reading_cards(year, level) + listening_cards(year, level))
    elif cmd == 'draft':
        P = EuPaper(year, level, SUBJECT)
        for a in P.aural_asks():
            print(key_label(a.key), 'p', a.page, '|', a.full_text)


if __name__ == '__main__':
    main()
