#!/usr/bin/env python3
"""Reviewed specs for the Polish listening cards, one per printed ask.

    python3 scripts/markbank/authoring/pl_listen.py draft 2026 hl   # what a spec is written from
    python3 scripts/markbank/authoring/pl_listen.py cards 2026 hl   # what it builds

Each entry names the census address the card answers and says, by SELECTORS
(pl_listen_lib), which scheme lines are its answers and which printed tariff
prices it. Nothing here is typed text: a selector names a line of the scheme's
.md by number and, where the SEC set two cells on one line, cuts it at printed
anchors. The card's question is the census's reading of the booklet (pl_paper),
its stem the booklet's own instruction for the section, its source the booklet
page, and its audio the year's SEC recording (data/polishAudio.json).

A spec is checked as it builds: every census listening leaf of the sitting gets
exactly one card, every option is a cut of the scheme, and every card's rows add
up to the tariff the scheme prints for it.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

import pl_paper                                                  # noqa: E402
from pl_listen import scheme_lines, aural_lines, AUDIO           # noqa: E402
from pl_listen_lib import (S, J, T, TN, PL, one, menu, part,   # noqa: E402,F401
                           One, Menu, Sel)
from pl_topics import (AURAL, POLISH, ENGLISH_OR_IRISH,          # noqa: E402
                       language_note, answer_language, concept_for)
from paper_census import key_label                              # noqa: E402

LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}
KEY = re.compile(r'^L([A-F])(\d{1,2})([a-h])?(i{1,3}|iv|vi{0,3})?$')
# Printed matter that closes a question in the booklet and is not part of it:
# the true/false columns' headings and the answer lines' dashes.
TRAILING = re.compile(r'(?:\s+(?:True\s+False|Prawda\s+Fa[lł]sz|[–—-]))+\s*$')


def parse_key(spec_key):
    m = KEY.match(spec_key)
    if not m:
        raise ValueError(f'bad key {spec_key!r}')
    return (f'L{m.group(1)}', int(m.group(2)), m.group(3), m.group(4))


class C:
    """One card: the census address, its rows, the tariff that prices it."""
    def __init__(self, key, rows, total=None, note=None, rownote=None, extra=()):
        self.key, self.rows, self.total, self.note = key, rows, total, note
        # Booklet lines the census leaves off the question (a table's second
        # row, a true/false statement): PL(page, opening), appended in order.
        self.extra = extra
        # A conflict between two printed lines, quoted for the student on
        # every row (CARD-STANDARD 5): the printed total is carded.
        self.rownote = rownote


SPECS = {}


# ------------------------------------------------------------- building ---
def recording(year):
    with open(AUDIO, encoding='utf-8') as fh:
        return next(r for r in json.load(fh) if r['year'] == year)


def section_intro(year, level):
    """{part: (heading, the booklet's instruction under it)}, lifted."""
    lines = aural_lines(year, level)
    out, part, buf = {}, None, []
    for line in lines:
        m = pl_paper.AURAL_TAB.match(line.text)
        if m:
            if part and part not in out:
                out[part] = buf
            part, buf = m.group(1), [line.text]
            continue
        if part and part not in out:
            if pl_paper.NUMBERED.match(line.text):
                out[part] = buf
                continue
            buf.append(line.text)
    if part and part not in out:
        out[part] = buf
    return {k: (v[0], ITEM.sub('', ' '.join(v[1:])).strip()) for k, v in out.items()}


ITEM = re.compile(r'\s*\bItem\s+\d{1,2}\s*$')
ITEM_LINE = re.compile(r'^Item\s+\d{1,2}$')


def item_labels(year, level):
    """{(part, q): "Item 2"}: the news item a question is printed under.

    Część E prints "Item 1" ... "Item 4" over its questions, and at Ordinary
    an item can carry two questions, so the label is read per question from
    the booklet, never assumed one to one."""
    out, part, item = {}, None, None
    for line in aural_lines(year, level):
        m = pl_paper.AURAL_TAB.match(line.text)
        if m:
            part, item = m.group(1), None
            continue
        if ITEM_LINE.match(line.text):
            item = line.text
            continue
        nm = pl_paper.NUMBERED.match(line.text)
        if nm and part and item:
            out.setdefault((part, int(nm.group(1))), item)
    return out


def card_id(year, level, key):
    section, q, letter, roman = key
    return '-'.join(['pl', str(year), level, section.lower(), str(q)]
                    + ([letter] if letter else []) + ([roman] if roman else []))


def _language(stem, question):
    if re.search(r'Answer in Polish', stem):
        return POLISH
    if re.search(r'Answer in (?:English|Irish)', stem):
        return ENGLISH_OR_IRISH
    return answer_language(question)


def build_rows(doc, spec, note):
    rows, total = [], 0
    base_note = note
    for i, r in enumerate(spec.rows, 1):
        rid = f'r-{i}'
        note = (f'For “{r.lead.text(doc)}”: {base_note}' if getattr(r, 'lead', None)
                else base_note)
        if isinstance(r, One) and not r.alts:
            count, per, notation = r.tariff.read(doc)
            if count != 1:
                raise ValueError(f'{spec.key}: one answer priced {notation!r}')
            rows.append({'id': rid, 'kind': 'point', 'verbatim': r.sel.text(doc),
                         'marks': per, 'contextNote': note})
            total += per
            continue
        if isinstance(r, One):          # one answer with lower-paid alternatives
            options, partials, count = [r.sel], list(r.alts), 1
            count_, per, notation = r.tariff.read(doc)
            if count_ != 1:
                raise ValueError(f'{spec.key}: one answer priced {notation!r}')
        else:
            options, partials = list(r.options), list(r.partials)
            count, per, notation = r.tariff.read(doc)
        texts = [o.text(doc) for o in options]
        if len(texts) < count:
            raise ValueError(f'{spec.key}: {notation!r} prices {count} answers over {len(texts)} printed')
        group = {'claimMax': count, 'perOption': per, 'options': texts}
        extra = []
        if partials:
            marks, of = [per] * len(texts), [None] * len(texts)
            for sel, of_i, t in partials:
                pc, pp, pn = t.read(doc)
                if pc != 1 or pp >= per:
                    raise ValueError(f'{spec.key}: partial priced {pn!r} against {per}')
                ptext = sel.text(doc)
                group['options'].append(ptext)
                marks.append(pp)
                of.append(of_i)
                extra.append(f'The scheme allows “{ptext}” for {pp} '
                             f'{"mark" if pp == 1 else "marks"}, in place of '
                             f'“{texts[of_i]}”, never beside it.')
            group['optionMarks'], group['optionOf'] = marks, of
        rows.append({'id': rid, 'kind': 'anyN',
                     'verbatim': 'The answers the scheme accepts in full', 'marks': None,
                     'contextNote': ' '.join([note] + extra), 'group': group})
        total += count * per
    return rows, total


def cards(year, level):
    spec_list = SPECS.get((year, level))
    if spec_list is None:
        raise KeyError(f'no listening spec for {year} {level}')
    doc = {'scheme': scheme_lines(year, level),
           'paper': [(l.page, l.text) for l in aural_lines(year, level)]}
    P = pl_paper.PlPaper(year, level)
    asks = {a.key: a for a in P.aural_asks()}
    intros = section_intro(year, level)
    items = item_labels(year, level)
    rec = recording(year)
    want = set(asks)
    out, seen = [], set()
    for spec in spec_list:
        key = parse_key(spec.key)
        if key not in asks:
            raise ValueError(f'{year} {level} {spec.key}: the census prints no such ask')
        if key in seen:
            raise ValueError(f'{year} {level} {spec.key}: carded twice')
        seen.add(key)
        ask = asks[key]
        part = key[0][1]
        heading, stem = intros.get(part, (f'Część {part}', ''))
        if (part, key[1]) in items:
            stem = f'{stem} {items[(part, key[1])]}'
        question = TRAILING.sub('', ask.full_text).strip()
        if spec.extra:
            question = ' '.join([question] + [TRAILING.sub('', x.text(doc)).strip()
                                              for x in spec.extra])
        language = _language(stem, question)
        note = language_note(language)
        if spec.rownote:
            note = f'{note} {spec.rownote(doc) if callable(spec.rownote) else spec.rownote}'
        rows, total = build_rows(doc, spec, note)
        if spec.total is not None:
            tc, tp, tn = spec.total.read(doc)
            if tc * tp != total:
                raise ValueError(f'{year} {level} {spec.key}: rows add to {total}, '
                                 f'the scheme prints {tn!r}')
        suffix = (f'({key[2]})' if key[2] else '') + (f'({key[3]})' if key[3] else '')
        ref = f'{year} {level.upper()} {key_label(key, "polish")}'
        card = {
            'id': card_id(year, level, key),
            'subjectId': 'polish',
            'level': LEVEL_WORD[level],
            'year': year,
            'section': key[0],
            'topicId': AURAL,
            'conceptId': concept_for(question),
            'questionRef': ref,
            'questionText': question,
            'tariffModel': {'kind': 'fixed'},
            'totalMarks': total,
            'rows': rows,
            'notes': (f'The scheme prices this listening ask {total} '
                      f'{"mark" if total == 1 else "marks"}; the listening booklet '
                      f'prints it on page {ask.page}.' + (f' {spec.note}' if spec.note else '')),
            'stem': stem,
            'sourceMaterial': {
                'kind': 'source-text',
                'label': 'LISTENING COMPREHENSION TEST',
                'title': f'Część {part} — Question {key[1]}{suffix}',
                'pages': [ask.page],
                'sourceLabel': 'Aural Paper',
                'attribution': (f'SEC Polish {year} {LEVEL_TITLE[level]} Level Listening '
                                f'Comprehension Test — © State Examinations Commission.'),
                'presentationNote': ('The question page of the listening booklet. '
                                     'Play the recording, then answer.'),
            },
            'audioMaterial': {**rec['source'], 'label': f'Część {part} · listening'},
        }
        out.append(card)
    missing = sorted(want - seen, key=str)
    if missing:
        raise ValueError(f'{year} {level}: no card for {[key_label(k, "polish") for k in missing]}')
    # Each section's cards add up to the total the scheme prints on its head
    # ("Część B – Święto Palanta – 16 marks"): a row read at the wrong price
    # cannot hide inside a sitting that still adds up.
    printed = {}
    body = doc['scheme']
    if '<!-- markbank:column-runs -->' in body:
        body = body[:body.index('<!-- markbank:column-runs -->')]
    for line in body:
        m = SECTION_TOTAL.match(line.strip())
        if m and m.group(1) not in printed:
            printed[m.group(1)] = int(m.group(2))
    for part, want_total in printed.items():
        got = sum(c['totalMarks'] for c in out if c['section'] == f'L{part}')
        if got != want_total:
            raise ValueError(f'{year} {level} Część {part}: cards add to {got}, '
                             f'the scheme prints {want_total}')
    return out


SECTION_TOTAL = re.compile(
    r'^Cz[eę][sś][cć]\s+([A-E])\s*[–‐-].*?(?:[–‐-]\s*|\(\s*)(\d{1,3})\s*marks?\s*\)?$', re.I)


# ================================================================ 2026 HL ===
# Scheme .md lines 370-557 (pages 12-16). Część A and B answer in Polish, C to
# E in English, as each section's own instruction says. Section totals as
# printed: A 24, B 16, C 24, D 14, E 22 (= 100).
SPECS[(2026, 'hl')] = [
    C('LA1', [menu([S(373), S(374)], T(372), [part(S(376), 1, T(376))])]),
    C('LA2', [menu([S(379), S(380)], T(377), [part(S(382), 0, T(382))])]),
    # Two columns on one row: (a) the faults at x=56, (b) the strengths at
    # x=296 (scheme p12, read by position). (a)'s "-emocjonalna (1 m)" stands
    # in for "zbyt emocjonalna".
    C('LA3a', [menu([S(386, before=' - optymizm'), S(387, before=' - cieszy'),
                     S(388, before=' - cieszy'), S(389)], T(385, 0),
                    [part(S(391), 0, T(391))])]),
    C('LA3b', [menu([S(386, after='emocjonalna - '), S(387, after='impulsywna - '),
                     S(388, after='nastroju - ')], T(385, 2))]),
    C('LA4', [menu([S(n) for n in range(394, 404)], T(392))]),
    C('LA5', [one(S(405), T(404), [part(S(407), 0, T(407))])]),
    C('LA6', [menu([S(410), S(411)], T(409))]),
    C('LB1i', [one(J(S(418, after='Palanta? '), S(419)), T(419))]),
    C('LB1ii', [one(S(420, after='gry? '), T(420), [part(S(422), 0, T(422))])]),
    C('LB1iii', [one(S(423, after='palanta? '), T(423), [part(S(425), 0, T(425))])]),
    C('LB2', [menu([S(428), S(429), S(430)], T(427))]),
    C('LB3', [menu([S(n) for n in range(433, 437)], T(431))]),
    C('LB4', [one(S(438), T(437))]),
    C('LC1a', [one(S(441, after='movie. '), T(441))]),
    C('LC1b', [menu([J(S(443, after='(i) '), S(444)), S(445, after='(ii) '),
                     J(S(446, after='(iii) '), S(447)), S(448, after='(iv) '),
                     S(449, after='(v) '), S(450, after='(vi) '), S(451, after='(vii) ')],
                    T(442))]),
    C('LC1c', [menu([S(457, after='(i) '), S(458, after='(ii) ')], T(456))]),
    C('LC2', [one(S(460), T(459), [part(S(462), 0, T(462)), part(S(464), 0, T(464))])]),
    C('LC3', [menu([S(n) for n in range(467, 471)], T(466))]),
    C('LC4', [one(S(472, after='trumpeter. '), T(471))]),
    C('LC5', [menu([S(n) for n in range(475, 482)], T(474))]),
    C('LD1', [menu([S(n) for n in range(485, 489)], T(484))]),
    C('LD2', [one(S(490, after='only. '), T(489))]),
    C('LD3i', [menu([S(n) for n in range(497, 502)], T(492), [part(S(503), 2, T(503))])]),
    C('LD3ii', [menu([S(506), S(507)], T(505), [part(S(509), 0, T(509))])]),
    # The price after "or" covers the whole "or" group, as the SEC sets it on
    # the group's first or last line (rendered: 2025 HL p13, p16): each line is
    # a shorter answer standing in for the full one it shortens.
    C('LE1', [menu([S(n) for n in range(513, 519)], T(512),
                   [part(S(520), 0, T(520)), part(S(521), 1, T(520)),
                    part(S(522), 2, T(520))])]),
    C('LE2', [menu([S(n) for n in range(525, 530)], T(524),
                   [part(S(531), 0, T(531)), part(S(532), 3, T(531))])]),
    C('LE3', [menu([S(535), S(536)] + [S(n) for n in range(541, 547)], T(534))]),
    C('LE4', [menu([S(n) for n in range(550, 556)], T(549), [part(S(557), 4, T(557))])]),
]


def quoted(*sels):
    """A marking instruction the scheme prints over the answer ("All or
    nothing:"), quoted for the student."""
    return lambda d: ' '.join(f'The scheme notes: “{s.text(d)}”.' for s in sels)


def conflict(head, tariff, asked):
    """The CARD-STANDARD 5 note for a directive that disagrees with the price."""
    return lambda d: (f'The scheme heads its list “{head.text(d)}” and prices the '
                      f'question “{tariff.read(d)[2]}”; the printed price is carded'
                      f'{asked}.')


# ================================================================ 2026 OL ===
# Scheme .md lines 294-432 (pages 11-14). Ordinary prices every listening
# answer at 3 marks; Część A and B answer in Polish, C to E in English.
# Section totals as printed: A 24, B 21, C 27, D 21, E 27 (= 120).
SPECS[(2026, 'ol')] = [
    C('LA1', [one(S(297), T(296))]),
    C('LA2', [one(S(299), T(299))]),
    # (a) prints no price of its own; its 3 marks are the question head's
    # "(3 marks)", as (b) prints "(3 marks)" beside its own list.
    C('LA3a', [menu([S(n) for n in range(302, 306)], T(300))],
      note='The scheme prints (a)\'s price on the question\'s head row.'),
    C('LA3b', [menu([S(307), S(308)], T(306))]),
    C('LA4', [menu([S(n) for n in range(311, 319)], T(309))],
      rownote=conflict(S(310), T(309), ', as the paper asks for three details')),
    C('LA5', [one(S(320), T(319))]),
    C('LB1i', [one(S(327, after='(i) '), T(326, each=True))]),
    C('LB1ii', [one(S(328, after='(ii) ', before=' or '), T(326, each=True),
                    [part(S(328, after=' or '), 0, T(328))])]),
    C('LB1iii', [one(S(329, after='(iii) ', before=' or '), T(326, each=True),
                     [part(S(329, after='wędzenia kiełbasy or ', before=' (2 marks)'), 0, T(329, 0)),
                      part(S(329, after='(2 marks) or '), 0, T(329, 1))])]),
    C('LB2', [menu([S(331), S(332), S(333)], T(330))]),
    C('LB3', [one(S(335, before=' or'), T(334), [part(S(335, after=' or '), 0, T(335))])]),
    C('LB4', [menu([S(337, before=', '), S(337, after=', ')], T(336))]),
    C('LC1', [one(S(340), T(339))]),
    C('LC2', [menu([S(n) for n in range(342, 349)], T(341))]),
    C('LC3', [one(S(350), T(349))]),
    C('LC4', [menu([S(n) for n in range(353, 357)], T(352))]),
    C('LC5', [one(S(358, after='humour. '), T(357))]),
    C('LC6', [menu([S(365), S(366)], T(363))]),
    C('LD1', [one(S(369), T(368))]),
    C('LD2', [one(S(371), T(370))]),
    C('LD3', [one(S(373), T(372))]),
    C('LD4', [one(S(376, after='sightseeing. '), T(374))]),
    C('LD5', [menu([S(n) for n in range(379, 388)], T(377))]),
    C('LE1', [one(S(391), T(390))]),
    C('LE2', [one(S(393), T(392))]),
    C('LE3', [one(S(396), T(395))]),
    C('LE4', [menu([S(n) for n in range(403, 408)], T(401))]),
    C('LE5', [menu([S(n) for n in range(411, 421)], T(409))]),
    C('LE6', [one(S(423), T(422))]),
    C('LE7', [menu([S(427), S(428), S(429), S(430, before=' or '), S(431), S(432)], T(425),
                   [part(S(430, after=' or '), 3, T(430))])]),
]


# ================================================================ 2025 HL ===
# Scheme .md lines 363-533 (pages 12-16). Część A and B answer in Polish, C to
# E in English. Section totals as printed: A 24, B 18, D 14, E 20 (Część C's
# head prints no total on its own line).
SPECS[(2025, 'hl')] = [
    # One printed ask, a table of two rows: "Kiedy ...?" (2 m) and "Dlaczego
    # ...? Podaj 2 powody." Two of (2 x 2 m), the question priced (3 × 2m).
    C('LA1', [one(S(365, after='w Puszczy '), T(365), [part(S(367), 0, T(367))],
                  lead=J(S(365, before=' pod koniec'), S(366))),
              menu([J(S(369, after='(i) '), S(370)), S(373, after='(ii) '),
                    J(S(374, after='(iii) '), S(375))], T(368),
                   [part(S(372), 0, T(372))],
                   lead=J(S(368, before=' Two of'), S(369, before=' (i)')))],
      total=T(364)),
    C('LA2', [menu([S(n) for n in range(379, 384)], T(377))]),
    C('LA3', [menu([S(n) for n in range(386, 391)], T(385))]),
    C('LA4', [one(S(392, after='roku. '), T(392))]),
    C('LA5', [menu([S(395), S(396), S(397)], T(394))]),
    C('LA6', [one(S(399), T(398))]),
    C('LB1', [one(S(406), T(406), [part(S(408), 0, T(408))])]),
    # "(4 m)" for the whole answer; after "or", its two halves with "(2 m)"
    # (rendered, scheme p13).
    C('LB2i', [one(S(410), T(410), [part(S(412), 0, T(413)), part(S(413), 0, T(413))])]),
    C('LB2ii', [menu([S(n) for n in range(416, 420)], T(415))]),
    C('LB3', [menu([S(422), S(423), S(424)], T(421), [part(S(426), 0, T(426))])]),
    C('LB4', [menu([S(429), S(430), S(431)], T(428),
                   [part(S(433), 0, T(432, each=True)), part(S(434), 1, T(432, each=True)),
                    part(S(435), 2, T(432, each=True))])]),
    # A table of three rows, priced (6 m) over its four answers.
    C('LC1', [one(S(442, after='month – '), T(442), lead=S(442, before=' month')),
              one(S(443, after='year – '), T(443), lead=S(442, before=' month')),
              one(J(S(444, after='protest? '), S(445), S(446), S(447)), T(447),
                  lead=S(444, before=' university')),
              one(S(448, after='protest '), T(448), lead=J(S(448, before=' ten'), S(449)))],
      total=T(441)),
    C('LC2', [one(S(451, after='protest. '), T(451))]),
    C('LC3', [menu([S(n) for n in range(454, 463)], T(453))]),
    C('LC4i', [one(S(464), T(463))]),
    C('LC4ii', [menu([S(467), S(468), S(469)], T(465))]),
    C('LC5', [one(S(471), T(470), [part(S(473), 0, T(473))])]),
    C('LD1', [one(S(480), T(479))]),
    C('LD2', [one(S(482), T(481))]),
    C('LD3', [menu([S(n) for n in range(485, 489)], T(484))]),
    C('LD4', [one(S(490), T(489))]),
    C('LD5', [one(S(492), T(491), [part(S(494), 0, T(494))])]),
    C('LE1', [one(S(502, after='playing? '), T(502), lead=S(502, before=' Kenya')),
              one(S(503, after='match? '), T(503), [part(S(505), 0, T(505))],
                  lead=S(503, before=' Poland'))],
      total=T(501)),
    C('LE2', [menu([S(n) for n in range(509, 513)], T(508))]),
    C('LE3', [menu([S(n) for n in range(516, 524)], T(515))]),
    C('LE4', [menu([S(n) for n in range(527, 531)], T(525),
                   [part(S(532), 0, T(532)), part(S(533), 1, T(532))])]),
]


# ================================================================ 2025 OL ===
# Scheme .md lines 277-439 (pages 10-15). Część A and B answer in Polish, C to
# E in English. Section totals as printed: A 30, B 21, C 30, D 15, E 24 (= 120).
SPECS[(2025, 'ol')] = [
    # A table of two rows, each its own printed ask, priced (2 × 3 m).
    C('LA1i', [one(S(279, after='mieszka w '), T(278, each=True))]),
    C('LA1ii', [menu([J(S(282, after='puszczy? '), S(283)), S(284), J(S(285), S(286))],
                     T(278, each=True), [part(S(288), 0, T(288))])]),
    C('LA2', [menu([S(n) for n in range(291, 297)], T(290))]),
    C('LA3', [menu([S(n) for n in range(299, 303)], T(298))]),
    C('LA4', [menu([S(n) for n in range(305, 312)], T(303))]),
    C('LA5', [one(S(313), T(312))]),
    C('LB1', [one(S(320), T(319))]),
    C('LB2i', [one(S(322), T(321), [part(S(324), 0, T(324))])]),
    C('LB2ii', [menu([S(n) for n in range(328, 332)], T(327))]),
    C('LB3', [menu([S(334), S(335), S(336)], T(333), [part(S(338), 0, T(338))])]),
    C('LB4', [menu([S(341), S(342), S(343)], T(339))]),
    C('LC1', [one(S(350, after='protest '), T(350), lead=S(350, before=' Poznań')),
              one(S(351, after='protest '), T(351), [part(S(353), 0, T(353))],
                  lead=S(351, before=' December')),
              one(S(354, after='protest '), T(354), lead=S(354, before=' Ten'))],
      total=T(349)),
    C('LC2', [one(S(356, after='zostaje. '), T(355))]),
    C('LC3', [menu([S(n) for n in range(359, 368)], T(357))]),
    C('LC4', [one(S(370, before=' ✓'), T(368))]),
    C('LC5i', [one(S(375), T(374))]),
    C('LC5ii', [menu([S(378), S(379), S(384)], T(376))]),
    C('LD1', [one(S(387), T(386))]),
    C('LD2', [one(S(389), T(388))]),
    C('LD3', [one(S(391, after='available. '), T(391))]),
    C('LD4i', [one(S(393), T(392, each=True))]),
    C('LD4ii', [one(S(395), T(392, each=True))]),
    C('LE1', [one(S(403, after='playing? '), T(402, each=True), lead=S(403, before=' Kenya')),
              one(S(404, after='match? '), T(402, each=True), [part(S(406), 0, T(406))],
                  lead=S(404, before=' Poland'))],
      total=T(402)),
    C('LE2', [menu([S(n) for n in range(410, 415)], T(409))]),
    C('LE3', [menu([S(418), S(419), S(420), J(S(421), S(422)), S(423), S(424), S(425), S(430)],
                   T(417))]),
    C('LE4', [menu([S(n) for n in range(434, 440)], T(433))]),
]


# ================================================================ 2024 HL ===
# Scheme .md lines 358-518 (pages 12-16). Część A and B answer in Polish, C to
# E in English. Section totals as printed: A 24, B 16, C 22, D 16, E 22 (= 100).
SPECS[(2024, 'hl')] = [
    # A table of three rows, "(3 x 2m)": each row's answer printed beside it.
    C('LA1', [one(S(360, after='grany '), T(359, each=True), lead=S(360, before=' Kwadrat')),
              one(S(361, after='Miejscowość '), T(359, each=True), lead=S(361, before=' Warszawa')),
              one(S(362, after='Tytuł '), T(359, each=True), lead=S(362, before=' Promieniowanie'))],
      total=T(359)),
    C('LA2', [menu([S(n) for n in range(365, 375)], T(364))]),
    C('LA3', [one(S(376, after='nudna. '), T(375))], extra=(PL(3, 'Reżyser'),)),
    C('LA4', [menu([S(n) for n in range(379, 386)], T(378))]),
    C('LA5', [menu([S(n) for n in range(388, 392)], T(387))]),
    C('LA6', [one(S(393), T(392))]),
    C('LB1', [menu([S(n) for n in range(401, 405)], T(400))]),
    C('LB2', [menu([S(407), S(408)], T(405))]),
    C('LB3', [menu([S(n) for n in range(411, 415)], T(409))]),
    C('LB4', [menu([S(n) for n in range(417, 422)], T(415))]),
    C('LC1', [menu([S(n) for n in range(429, 432)], T(428))]),
    C('LC2', [one(S(433), T(432))]),
    C('LC3', [menu([S(n) for n in range(436, 442)], T(435))]),
    C('LC4', [menu([S(n) for n in range(444, 449)], T(443))]),
    C('LC5', [one(S(450), T(449))]),
    # A table of two rows, "(4 x 2m)" over both, "any two of:" over each.
    C('LD1', [menu([S(458, after='posters: '), S(459), S(460), S(461)], TN(456, 457),
                   lead=S(458, before=' - simple')),
              menu([S(463, after='created? '), S(464), S(465), S(466)], TN(456, 462),
                   lead=S(463, before=' - films'))],
      total=T(456), extra=(PL(6, 'For what were'),)),
    C('LD2', [one(S(468, after='artists. '), T(468))]),
    C('LD3', [menu([S(n) for n in range(471, 478)], T(470))]),
    # A table of three rows, "(3 x 2m)"; its third row takes "any one of:".
    C('LE1', [one(S(484, after='damaged? '), T(483, each=True), lead=S(484, before=' gas')),
              one(J(S(485, after='happen? '), S(486)), T(483, each=True),
                  lead=S(485, before=' (last)')),
              menu([S(488), S(489), S(490)], TN(483, 487), lead=S(487, before=' any one'))],
      total=T(483)),
    C('LE2', [menu([S(n) for n in range(493, 498)], T(492))]),
    C('LE3', [menu([S(n) for n in range(500, 508)], T(498))]),
    C('LE4', [menu([S(510, after='seaside '), S(511), S(512), S(513)], TN(508, 509),
                   lead=S(510, before=' - temperature')),
              menu([S(515, after='mountains '), S(516), S(517), S(518)], TN(508, 514),
                   lead=S(515, before=' - sunny'))],
      total=T(508), extra=(PL(7, 'at the seaside'), PL(7, 'in the mountains'))),
]


# ================================================================ 2024 OL ===
# Scheme .md lines 285-422 (pages 11-15). Część A and B answer in Polish, C to
# E in English. Section totals as printed: A 25, B 22, C 25, D 21, E 27 (= 120).
SPECS[(2024, 'ol')] = [
    C('LA1', [one(S(287, after='grany. '), T(286, each=True), lead=S(287, before=' Kwadrat')),
              one(S(288, after='bohaterka? '), T(286, each=True), lead=S(288, before=' Maria'))],
      total=T(286)),
    # Multiple choice: the scheme ticks the first of the four printed options.
    C('LA2', [one(S(291, before=' ✓'), T(289))],
      extra=(PL(3, 'Sztuka poświęcona'), PL(3, 'życiu i pracy'), PL(3, 'jedynie życiu'),
             PL(3, 'jedynie pracy noblistki'), PL(3, 'jedynie pracy naukowej'))),
    C('LA3', [menu([S(n) for n in range(294, 301)], T(293))]),
    C('LA4', [menu([S(n) for n in range(303, 307)], T(301))]),
    C('LA5', [menu([S(309), S(310)], T(307))]),
    C('LB1', [one(S(317), T(316))]),
    C('LB2', [menu([S(n) for n in range(320, 323)], T(319))]),
    C('LB3', [menu([S(325), S(326)], T(324))]),
    C('LB4', [menu([S(n) for n in range(329, 332)], T(328))]),
    C('LB5', [menu([S(n) for n in range(334, 340)], T(332))]),
    C('LC1', [menu([S(347), S(348)], T(346))]),
    C('LC2', [one(S(350), T(349))]),
    C('LC3', [one(S(352, after='Podsiadło. '), T(352))], extra=(PL(5, 'There are only'),)),
    C('LC4', [menu([S(n) for n in range(355, 361)], T(354))]),
    C('LC5', [menu([S(n) for n in range(363, 366)], T(362))]),
    C('LD1', [one(S(372, after='Poland. '), T(372))]),
    # A table of two rows, "(4 x 3 m)" over both, "any two of:" beside each.
    C('LD2', [menu([S(n) for n in range(375, 379)], TN(373, 374), lead=S(374, before=' any two')),
              menu([S(n) for n in range(380, 384)], TN(373, 379), lead=S(379, before=' any two'))],
      total=T(373), extra=(PL(6, 'For what were'),)),
    C('LD3', [menu([S(n) for n in range(386, 393)], T(385))]),
    C('LE1', [one(S(399, after='damaged? '), T(398, each=True), lead=S(399, before=' gas')),
              one(J(S(400, after='happen? '), S(401)), T(398, each=True),
                  lead=S(400, before=' (last)')),
              one(J(S(402, after='help? '), S(403)), T(398, each=True),
                  lead=S(402, before=' fire'))],
      total=T(398)),
    C('LE2', [menu([S(n) for n in range(406, 411)], T(405))]),
    C('LE3', [one(S(412), T(412))]),
    # "(2 x 3 m)": one answer for each of the two rows. The seaside row prints
    # "any one of:"; the mountains row prints its list with no directive.
    C('LE4', [menu([S(415), S(416), J(S(417), S(418))], T(413, each=True),
                   lead=S(414, before=' any one')),
              menu([S(419, after='mountains '), S(420), S(421), S(422)], T(413, each=True),
                   lead=S(419, before=' - sunny'))],
      total=T(413), extra=(PL(7, 'in the mountains'),)),
]


# ================================================================ 2023 HL ===
# Scheme .md lines 354-495 (pages 12-16). Część A and B answer in Polish, C to
# E in English. Section totals as printed: A 22, B 18, C 22, D 14, E 24 (= 100);
# A, B and D set their heads with U+2010 hyphens.
SPECS[(2023, 'hl')] = [
    C('LA1', [one(S(356), T(356))]),
    # "(2 x 2m)" over exactly two printed answers: both are asked for.
    C('LA2', [one(S(358), T(357, each=True)), one(J(S(359), S(360)), T(357, each=True))],
      total=T(357)),
    C('LA3', [one(S(363), T(362, each=True)), one(S(364), T(362, each=True))], total=T(362)),
    C('LA4i', [one(S(366, after='wykształcenie. '), T(365))]),
    C('LA4ii', [menu([S(369), S(370), S(371)], T(368))]),
    C('LA5', [menu([S(n) for n in range(374, 379)], T(373))]),
    C('LA6', [one(S(381), T(379))], rownote=quoted(S(380))),
    C('LB1', [menu([S(389), S(390), S(391)], T(388))]),
    C('LB2', [one(S(393, after='powstały? '), T(392, each=True), lead=S(393, before=' w celu')),
              one(S(394, after='Kiedy? '), T(392, each=True), lead=S(394, before=' po II'))],
      total=T(392)),
    C('LB3', [menu([S(n) for n in range(397, 404)], T(396))]),
    C('LB4', [one(S(405), T(404, each=True)), one(S(406), T(404, each=True))], total=T(404)),
    C('LC1', [menu([S(414), S(415)], T(413))]),
    C('LC2i', [one(S(418), T(417))], rownote=quoted(S(417))),
    C('LC2ii', [menu([S(n) for n in range(421, 425)], T(420))]),
    C('LC2iii', [one(S(426), T(425))]),
    C('LC3', [menu([S(n) for n in range(429, 440)], T(428))]),
    C('LC4', [one(S(441, after='Mrągowo. '), T(440))]),
    C('LC5', [one(S(443), T(443))]),
    C('LD1', [one(S(450, after='built? '), T(449, each=True), lead=S(450, before=' in 1970s')),
              one(S(451, after='is it? '), T(449, each=True), lead=S(451, before=' (almost)')),
              one(S(452, after='remind us of? '), T(449, each=True), lead=S(452, before=' a sea'))],
      total=T(449)),
    C('LD2', [menu([S(n) for n in range(455, 458)], T(454))]),
    C('LD3', [menu([S(n) for n in range(460, 463)], T(459))]),
    # Multiple choice: the scheme prints the ticked box's words.
    C('LE1', [one(S(470, before=' ✓'), T(470))],
      extra=(PL(7, 'in September'), PL(7, 'for the thirty'), PL(7, 'for Polish students'),
             PL(7, 'online only'))),
    C('LE2', [menu([S(n) for n in range(473, 481)], T(472))]),
    C('LE3', [one(S(482, after='type '), T(481, each=True), lead=S(482, before=' photo')),
              one(S(483, after='title '), T(481, each=True), lead=S(483, before=' “My')),
              one(S(484, after='prize '), T(481, each=True), lead=S(484, before=' 1 200'))],
      total=T(481)),
    C('LE4', [menu([S(n) for n in range(487, 491)], T(486))]),
    C('LE5', [menu([S(n) for n in range(493, 496)], T(492))]),
]

