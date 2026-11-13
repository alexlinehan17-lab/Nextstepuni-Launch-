#!/usr/bin/env python3
"""German reading and grammar asks, read address by address from the paper.

    python3 scripts/markbank/authoring/de_written.py 2022 hl deferred   # read one sitting

de_scheme.py reads the June schemes of 2021-2026, whose questions are headed
"Frage 1: (14 marks: (a) …)" and whose answers are numbered. The deferred
2022 Higher scheme is set the other way: "1. (20 marks: 6, 4, 6, 4)" over
lettered parts, bullets ("•", "*") for answers, a part split printed only as
"(6 marks: (i) 4 marks (ii) 2 marks)" with no "(i)" over the first ask, and
grammar answered on the line under each sentence ("sein (2) Imperfekt (2)
Singular (1)"). Those are the listening scheme's shapes, so this reads each
census ask (the PAPER's address) with de_listen's row reader: the rows are
the scheme's words, and every ask adds to the tariff the scheme prints on
it, or it is refused with the reason.

Where the scheme numbers an ask otherwise than the paper prints it, the
paper's address wins and the card says so (SCHEME_ADDRESS): 2022 Higher
deferred TEXT I, the paper's Q3(b) and Q3(c), the scheme's "(b) (i)" and
"(ii)".
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from de_paper import DePaper                                     # noqa: E402
from de_scheme import (DeScheme, UNIT_LV, UNIT_AG, UNIT_AT, UNIT_SP,  # noqa: E402
                       UNIT_LISTEN, GUIDANCE, TEXT_NUM, head_total, _language_of,
                       MATCH_KEY, MATCH_PAIR)
import de_listen as L                                            # noqa: E402

PAGE = re.compile(r'^(?:##\s*Page\s*\d+\s*$|\d{1,3}\s*$)')
Q_HEAD = re.compile(r'^(?:(?:Frage|Question|Ceist)\s*(\d{1,2})\s*:?|(\d{1,2})\s*\.)\s*'
                    r'(\(?\s*(?:\d{1,3}|[A-Z][a-z]+)\s*marks?\b.*)$', re.I)
L_HEAD = re.compile(r'^\(\s*([a-h])\s*\)\s*(.*)$')
R_HEAD = re.compile(r'^\(\s*(i{1,3}|iv|v)\s*\)\s*(.*)$', re.I)
WORDS = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7,
         'eight': 8, 'nine': 9, 'ten': 10, 'twelve': 12}

# The scheme's address -> the paper's, where the two number one ask apart.
SCHEME_ADDRESS = {
    (2022, 'hl', 'deferred'): {('T1', 3, 'b', 'i'): ('T1', 3, 'b', None),
                               ('T1', 3, 'b', 'ii'): ('T1', 3, 'c', None)},
}


def _total(clause):
    """"(6 marks: …)" 6; "(Four marks: 2 x 2 marks)" 4."""
    got = head_total(clause)
    if got is not None:
        return got
    m = re.match(r'^\s*\(?\s*([A-Z][a-z]+)\s*marks?\b', clause or '', re.I)
    return WORDS.get(m.group(1).lower()) if m else None


def _units(S):
    """{unit: [lines]} for the reading units, each to the next unit head."""
    out, unit = {}, None
    for line in S.lines:
        s = line.strip()
        m = UNIT_LV.match(s)
        if m:
            unit = f'T{TEXT_NUM[m.group(1).lower()]}'
            out[unit] = []
            continue
        if UNIT_AG.match(s) or UNIT_AT.match(s) or UNIT_SP.match(s) or UNIT_LISTEN.match(s) \
                or GUIDANCE.match(s):
            unit = None
            continue
        if unit:
            out[unit].append(s)
    return out


def leaves(year, level, sitting, keys):
    """{paper key: Leaf} for the census's reading keys."""
    S = DeScheme(year, level, 'german', sitting)
    remap = SCHEME_ADDRESS.get((year, level, sitting), {})
    out = {}
    for unit, lines in _units(S).items():
        heads = [(i, int(m.group(1) or m.group(2)), m.group(3))
                 for i, s in enumerate(lines) if (m := Q_HEAD.match(s))]
        for n, (i, q, clause) in enumerate(heads):
            end = heads[n + 1][0] if n + 1 < len(heads) else len(lines)
            block = [s for s in lines[i + 1:end] if s and not PAGE.match(s)]
            _question(unit, q, clause, block, keys, remap, out)
    return out


def _question(unit, q, clause, block, keys, remap, out):
    letters = [h for h in block if L_HEAD.match(h)]
    total = _total(clause)
    heads = []
    want = 'abcdefgh'
    for i, s in enumerate(block):
        m = L_HEAD.match(s)
        if m and m.group(1) == want[len(heads)] and _total(m.group(2)) is not None:
            heads.append((i, m.group(1), m.group(2)))
    if not heads:
        _leaf(unit, q, None, None, total, L._steps(clause), block, keys, remap, out)
        return
    for n, (i, letter, lclause) in enumerate(heads):
        end = heads[n + 1][0] if n + 1 < len(heads) else len(block)
        body = block[i + 1:end]
        romans = [k[3] for k in keys if k[:3] == (unit, q, letter) and k[3]] or [
            k[3] for k in remap if k[:3] == (unit, q, letter) and k[3]]
        if not romans:
            _leaf(unit, q, letter, None, _total(lclause), L._steps(lclause), body, keys, remap, out)
            continue
        totals, defaults = L.clause_split(lclause, romans)
        rheads, wanted = [], list(romans)
        if not any((m := R_HEAD.match(x)) and m.group(1).lower() == 'i' for x in body):
            wanted = wanted[1:]
        for k, s in enumerate(body):
            m = R_HEAD.match(s)
            if wanted and m and m.group(1).lower() == wanted[0]:
                rheads.append((k, wanted.pop(0), m.group(2)))
        if not rheads or rheads[0][1] != 'i':
            # No "(i)" over the first ask: it runs from the part's head to
            # "(ii)" (2022 Higher deferred TEXT I Q2(b)).
            rheads.insert(0, (-1, 'i', ''))
        for r, (k, roman, rest) in enumerate(rheads):
            stop = rheads[r + 1][0] if r + 1 < len(rheads) else len(body)
            rb = ([rest] if rest.strip() else []) + body[k + 1:stop]
            own = _total(rest)
            _leaf(unit, q, letter, roman, totals.get(roman) or own, defaults.get(roman) or L._steps(rest),
                  rb, keys, remap, out)
    del letters


def _leaf(unit, q, letter, roman, total, default, body, keys, remap, out):
    key = remap.get((unit, q, letter, roman), (unit, q, letter, roman))
    if key not in keys:
        return
    body = list(body)
    # The part's own tariff restated above its question ("(4 marks: 2 x 2
    # marks)") is its head, not a rate over answers.
    while body and re.match(r'^\(\s*(?:\d{1,3}|[A-Z][a-z]+)\s*marks?\s*[:)]', body[0]):
        default = default or L._steps(body[0])
        total = total or _total(body[0])
        body = body[1:]
    # A question wrapped across lines inside its own bracket ("(lines 79-" /
    # "89)") is one line.
    joined = []
    for s_ in body:
        if joined and joined[-1].count('(') > joined[-1].count(')'):
            joined[-1] = f'{joined[-1]} {s_}'
        else:
            joined.append(s_)
    body = joined
    # A tariff line of the part's own ("(4 marks: 2 x 2 marks)") opening the
    # body is its rate, not an answer.
    keyline = next((x for x in body if MATCH_KEY.match(x)), None)
    if keyline:
        # A matching question answered by its key alone: "2 f 3 a 4 b 5 c 6 e".
        out[key] = ('match', total, default, [f'{a} — {b}' for a, b in MATCH_PAIR.findall(keyline)])
        return
    out[key] = L.Leaf(part=unit, q=key[1], roman=key[3], total=total, lines=body,
                      default=default, rule='', line=0, q_total=None, q_split=None)


# The place in the text an ask is answered from closes it: "(Par. 6)".
ADDRESS_END = re.compile(r'\((?:Par\.|Alt|lines?|Zeilen?|Absatz|Abschnitt)[^)]*\)\s*$', re.I)


def _to_address(text):
    """The ask up to its address, where a lettered list printed after it is the
    next question's: the deferred 2022 Q3(b) "… (Par. 6)" ran on into Q4's
    sentence halves "a. bis er das Gemüse ernten kann. b. …", set in the same
    column on the page below."""
    lines = text.split('\n')
    for i, line in enumerate(lines[:-1]):
        if ADDRESS_END.search(line) and re.match(r'^[a-h]\.\s', lines[i + 1].strip()):
            return '\n'.join(lines[:i + 1])
    return text


def cards(year, level, sitting, card_id, question_ref, concept_for, refuse, keys):
    """Reading cards for one sitting's census keys (T units)."""
    from de_all import reading_source, UNIT_NAME
    from de_topics import topic_for, language_note
    P = DePaper(year, level, 'german', sitting)
    keys = [tuple(k) for k in keys if k[0].startswith('T')]
    read = leaves(year, level, sitting, keys)
    remap = SCHEME_ADDRESS.get((year, level, sitting), {})
    moved = {v: k for k, v in remap.items()}
    out = []
    credit = {u: P.credit(u) for u in P.unit_pages if u.startswith('T')}
    for key in keys:
        unit, q, letter, roman = key
        ref = question_ref(year, level, unit, q, letter, roman)
        if sitting:
            ref = f'{ref} — Deferred sitting'
        leaf = read.get(key)
        hit = P.by_key(unit, q, letter, roman)
        if hit is None or leaf is None:
            refuse('the scheme prints no block for this ask', ref, f'{year} {level.upper()} {sitting or ""} scheme')
            continue
        text, page, _s = hit
        from de_all import instruction_only, clean_question
        # One line, as June's reading cards are; a matching task keeps its
        # instruction only (the table is on the pages the card carries).
        if not isinstance(leaf, tuple):
            text = _to_address(text)
        text = (instruction_only(text) if isinstance(leaf, tuple) else ' '.join(text.split()))
        text = clean_question(text.replace('\uf0b7', '•'))
        rows = None
        if isinstance(leaf, tuple):
            _kind, total, steps, pairs = leaf
            if not steps or len(pairs) != len(steps) or sum(steps) != total:
                refuse('the answer key does not match its printed tariff', ref, str(pairs))
                continue
            rows = [{'id': 'r-1', 'kind': 'anyN', 'verbatim': 'The answers the scheme accepts in full',
                     'marks': None, 'group': {'claimMax': len(steps), 'perOption': steps[0], 'options': pairs},
                     'contextNote': (language_note(_language_of(text, None)) + ' The scheme pays every one '
                                     'of these; none is optional. It prints only the key, so each pair is '
                                     'the number and the letter it prints.')}]
            leaf = L.Leaf(part=unit, q=q, roman=roman, total=total, lines=[], default=steps,
                          rule='', line=0, q_total=None, q_split=None)
        got = ([], []) if rows else L.leaf_rows(leaf, text)
        if isinstance(got, str):
            refuse(got, ref, f'{year} {level.upper()} {sitting or ""} scheme, {unit} Q{q}')
            continue
        items, general = got
        language = _language_of(text, None)
        if rows is None:
            rows = L.mark_rows(items, language_note(language), general)
        note = (f'The scheme prices this ask {leaf.total} marks; the paper prints it on page {page}'
                f' of the question booklet.')
        if key in moved:
            u, qq, ll, rr = moved[key]
            note += (f' The scheme numbers it {UNIT_NAME[u]} Q{qq}({ll})({rr}); the paper prints it '
                     f'as Q{q}({letter}), and the card keeps the paper\'s address.')
        card = {
            'id': card_id(year, level, unit, q, letter, roman).replace(
                f'de-{year}-{level}-', f'de-{year}-{level}-deferred-') if sitting else
            card_id(year, level, unit, q, letter, roman),
            'subjectId': 'german', 'level': {'hl': 'higher', 'ol': 'ordinary'}[level], 'year': year,
            'section': unit, 'topicId': topic_for(unit, credit.get(unit)),
            'conceptId': concept_for(text), 'questionRef': ref, 'questionText': text,
            'tariffModel': {'kind': 'fixed'}, 'totalMarks': leaf.total, 'rows': rows, 'notes': note,
        }
        src = reading_source(P, unit, language, level, year)
        if src:
            if sitting:
                src['attribution'] = src['attribution'].replace('examination paper', 'deferred examination paper')
            card['sourceMaterial'] = src
        out.append(card)
    return out


if __name__ == '__main__':
    import paper_census as pc
    import de_all
    y, l = int(sys.argv[1]), sys.argv[2]
    sitting = sys.argv[3] if len(sys.argv) > 3 else None
    paper = (pc.census_german_deferred()[0] if sitting else None)
    keys = [tuple(x['key']) for x in paper['leaves']]
    refused = []
    cs = cards(y, l, sitting, de_all.card_id, de_all.question_ref, de_all.concept_for,
               lambda *a: refused.append(a), keys)
    for c in cs:
        print(c['id'], c['totalMarks'], [(r['kind'], r.get('marks'), (r.get('group') or {}).get('claimMax'),
                                          len((r.get('group') or {}).get('options', []))) for r in c['rows']])
    for r in refused:
        print('REFUSED', r[1], '|', r[0])


# ------------------------------------------------------- applied grammar ----
GRAMMAR_ITEM = re.compile(r'^\(\s*(\d)\s*\)\s*(.*)$')
NB_PARTIAL = re.compile(r'\s*\(NB:?\s*(.+?)\s*[–-]\s*(\d)\s*marks?\)\s*$', re.I)


def grammar_leaves(S):
    """{1|2: [(sentence, answer line)]} for a scheme that answers each printed
    sentence on the line under it ("(1) Das war kein Problem …" / "sein (2)
    Imperfekt (2) Singular (1)"), the deferred 2022 Higher layout."""
    start = next(i for i, l in enumerate(S.lines) if UNIT_AG.match(l.strip()))
    out, alt, cur = {}, None, None
    for line in S.lines[start + 1:]:
        s = line.strip()
        if not s or PAGE.match(s) or s.upper() in ('ODER', 'OR', 'NÓ/OR'):
            continue
        if UNIT_LV.match(s) or UNIT_AT.match(s) or UNIT_SP.match(s):
            break
        m = re.match(r'^([12])\s*\.\s', s)
        if m:
            alt = int(m.group(1))
            out[alt] = []
            cur = None
            continue
        m = GRAMMAR_ITEM.match(s)
        if m and alt:
            cur = [s, []]
            out[alt].append(cur)
            continue
        if cur is not None:
            cur[1].append(s)
    return {k: [(sent, ' '.join(ans)) for sent, ans in v] for k, v in out.items()}


def grammar_cards(year, level, sitting, card_id, question_ref, concept_for, refuse):
    from de_all import TEXT_TITLE, clean_question
    from de_topics import topic_for, language_note
    P = DePaper(year, level, 'german', sitting)
    S = DeScheme(year, level, 'german', sitting)
    total = S.unit_totals.get('AG')
    read = grammar_leaves(S)
    out = []
    for q, text, page in P.grammar_alternatives():
        ref = question_ref(year, level, 'AG', q, None) + (' — Deferred sitting' if sitting else '')
        items = read.get(q) or []
        rows = []
        for n, (sentence, answer) in enumerate(items, start=1):
            nb = NB_PARTIAL.search(answer)
            main = answer[:nb.start()].strip() if nb else answer
            parts = L._components(main)
            marks = sum(int(x) for x in re.findall(r'\((\d)\)', main))
            note = f'The sentence the scheme prints: {sentence}'
            if parts and sum(m for _w, m in parts) == marks:
                row = {'id': f'r-{n}', 'kind': 'criterion', 'verbatim': main, 'marks': marks,
                       'contextNote': note, 'permittedMarks': list(range(marks + 1)),
                       'parts': [{'id': f'p{k}', 'verbatim': w, 'marks': m, 'permittedMarks': list(range(m + 1))}
                                 for k, (w, m) in enumerate(parts, start=1)]}
            elif nb and int(nb.group(2)) < marks:
                row = {'id': f'r-{n}', 'kind': 'anyN', 'verbatim': 'The answers the scheme accepts in full',
                       'marks': None, 'contextNote': (f'{note} The scheme allows “{nb.group(1)}” for '
                                                      f'{nb.group(2)} marks, in place of the answer, never beside it.'),
                       'group': {'claimMax': 1, 'perOption': marks, 'options': [main, nb.group(1)],
                                 'optionMarks': [marks, int(nb.group(2))], 'optionOf': [None, 0]}}
            else:
                row = {'id': f'r-{n}', 'kind': 'point', 'verbatim': main, 'marks': marks, 'contextNote': note}
            rows.append(row)
        got = sum(r['marks'] if r['marks'] is not None else r['group']['perOption'] for r in rows)
        if not rows or total is None or got != total:
            refuse('the scheme prints no priced answers this reads for this alternative', ref,
                   f'{year} {level.upper()} scheme, ANGEWANDTE GRAMMATIK {q}: {got} of {total}')
            continue
        rows[0]['contextNote'] = ('Every gap is answered; the scheme prints the mark it pays on each. '
                                  + language_note('German') + ' ' + rows[0]['contextNote'])
        out.append({
            'id': f'de-{year}-{level}-deferred-ag-{q}' if sitting else card_id(year, level, 'AG', q, None, None),
            'subjectId': 'german', 'level': {'hl': 'higher', 'ol': 'ordinary'}[level], 'year': year,
            'section': 'AG', 'topicId': topic_for('AG', None),
            'conceptId': concept_for(text, 'applied-grammar'), 'questionRef': ref,
            'questionText': clean_question(text), 'tariffModel': {'kind': 'fixed'}, 'totalMarks': total,
            'rows': rows,
            'sourceMaterial': {
                'kind': 'source-text', 'label': TEXT_TITLE['AG'],
                'title': 'Angewandte Grammatik — the printed exercise', 'pages': [page],
                'attribution': (f'SEC German {year} {"Higher" if level == "hl" else "Ordinary"} Level '
                                f'{"deferred " if sitting else ""}examination paper — © State Examinations Commission.'),
                'presentationNote': 'Work from the sentences exactly as the examination printed them. '
                                    + language_note('German')},
            'notes': (f'The paper sets question 1 OR question 2 here and this is alternative {q}; the '
                      f'scheme prices it {total}, five sentences, each answered on the line under it.'),
        })
    return out
