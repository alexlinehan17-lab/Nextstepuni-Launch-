#!/usr/bin/env python3
"""Paper-anchored Irish asks: every printed ask of a 2022-onward Irish paper, read from the SEC paper's own text
layer, never from the cards.

The Irish lane's counter (measured every main sitting 2010-2026, 4 Nov 2026) returns how many asks a paper prints;
this is the same reader with each ask's printed address kept, so a census can list them. Used for the deferred
sittings (paper_census.census_irish_deferred). Paper 1 (2022 on): the listening segments (Fógra, Comhrá, Píosa a
hAon/Dó/Trí; An Chéad/Dara Mír) and every titled composition the candidate may write on. Paper 2: the reading
comprehensions' lettered parts, then each literature option's parts (an option printed without parts is one ask).

usage: irish_paper_asks.py PDF 1|2   (prints the asks as JSON)
"""
from __future__ import annotations
import json
import re
import sys

SEG = re.compile(r'^(?:F[ÓO]GRA|COMHR[ÁA]|P[ÍI]OSA)\s+A\s+(?:hAON|D[ÓO]|TR[ÍI])\b|^An (?:Chéad|Dara) M[ií]r\b', re.I)
NUM = re.compile(r'^(\d{1,2})(?:\.(?:\s+(.*))?|\s+(?=\([a-h]\)\s)(.*))$')
LET = re.compile(r'^\(([a-h])\)(?:\s+(.*))?$')
ROM = re.compile(r'^\((i|ii|iii|iv|v|vi)\)(?:\s+(.*))?$')
BLANK = re.compile(r'^[_\s.…‐-]*$')
LIT_OPTION = re.compile(r'^([234][A-F])\.?(?:\s|$)')
PRICE = re.compile(r'\(\d+\s*m?h?arc\)')


def num_rest(m):
    return m.group(2) if m.group(2) is not None else m.group(3)


def marker(t):
    m = NUM.match(t)
    if m:
        return m.group(1)
    m = LET.match(t) or ROM.match(t)
    return f'({m.group(1)})' if m else ''


def lines_of(path):
    import fitz
    out = []
    for i, page in enumerate(fitz.open(path)):
        for raw in page.get_text(sort=True).split('\n'):
            t = ' '.join(raw.replace('‐', '-').split())
            if t:
                out.append((i + 1, t))
    return out


def has_text(lines, k, inline):
    """A marker carries a prompt when it has words on its line or on the next non-empty line."""
    if inline and re.search(r'[A-Za-zÁÉÍÓÚáéíóú]{2}', inline) and not BLANK.match(inline):
        return True
    for j in range(k + 1, min(k + 3, len(lines))):
        t = lines[j][1]
        if BLANK.match(t):
            return False
        if NUM.match(t) or LET.match(t) or ROM.match(t) or SEG.match(t):
            return False
        return bool(re.search(r'[A-Za-zÁÉÍÓÚáéíóú]{3}', t))
    return False


def marker_nodes(lines, letter_roman=False):
    """(level, carries a prompt, line) for every number / letter / roman marker, in print order. With letter_roman
    (the reading questions), a letter and its first roman printed on one line ("(a) (i) …") are two markers."""
    nodes = []
    for k, (_, t) in enumerate(lines):
        m = NUM.match(t)
        if m and num_rest(m) and (LET.match(num_rest(m)) or ROM.match(num_rest(m))):
            nodes.append((0, False, t))      # "1. (a) Cé a sheol …": a number and its first part on one line
            t = num_rest(m)
        m2 = LET.match(t)
        if letter_roman and m2 and m2.group(2) and ROM.match(m2.group(2)):
            nodes.append((1, False, t))
            t = m2.group(2)
        for rx, lvl in ((NUM, 0), (LET, 1), (ROM, 2)):
            m = rx.match(t)
            if m:
                nodes.append((lvl, has_text(lines, k, (num_rest(m) if rx is NUM else m.group(2)) or ''), t))
                break
    return nodes


def leaf_addresses(nodes, count_numbers=True):
    """The printed address ("1(a)", "2", "(b)(ii)") of every leaf ask: a marker with a prompt and no prompted child.
    A bare number counts where count_numbers (a listening question printed without parts); a letter always counts."""
    out = []
    path = ['', '', '', '']
    for i, (lvl, txt, t) in enumerate(nodes):
        path[lvl] = marker(t)
        path[lvl + 1:] = [''] * (3 - lvl)
        child = False
        for lvl2, txt2, _ in nodes[i + 1:]:
            if lvl2 <= lvl:
                break
            if txt2:
                child = True
                break
        if child:
            continue
        if count_numbers and (txt or lvl == 0):
            out.append(''.join(path[:lvl + 1]))
        elif not count_numbers and lvl > 0 and (txt or lvl == 1):
            out.append(''.join(path[:lvl + 1]))
    return out


def paper1_asks(path):
    """Listening segments and the titled compositions of a 2022-onward Paper 1."""
    lines = lines_of(path)
    pages = {}
    for p, t in lines:
        pages.setdefault(p, []).append(t)
    seg_pages = sorted({p for p, t in lines if SEG.match(t)})
    first, last = (seg_pages[0], seg_pages[-1]) if seg_pages else (1, 0)
    comp_pages = [p for p, ts in sorted(pages.items()) if p > last and re.search(r'ch?eapad', ' '.join(ts), re.I)
                  and re.search(r'\((?:a|i)\)', ' '.join(ts))]
    asks = []
    segment, body, main = None, [], ''

    def close():
        if segment is None:
            return
        nodes = marker_nodes(body)
        if any(lvl < 2 for lvl, _, _ in nodes):
            asks.extend(('Cluastuiscint', f'{segment} · {address}') for address in leaf_addresses(nodes))
            return
        # A grid ("Líon isteach an t-eolas … sa ghreille"): its printed prompts, joined across wrapped lines, each
        # ending in "?" or "."; answer lines dropped.
        kept = [t for _, t in body if not BLANK.match(t) and not ROM.match(t.split('_')[0].strip() or t)
                and not re.match(r'^\((?:i|ii|iii|iv)\)\s*_', t)]
        start = next((i for i, t in enumerate(kept) if re.search(r'gh?reille', t)), -1)
        text = ' '.join(kept[start + 1:]) if start >= 0 else ' '.join(kept)
        text = re.split(r'\b(?:Cuid|CUID) [ABC]\b|Scrúdú na hArdteist|Cloisfidh tú', text)[0]
        prompts = [x.strip() for x in re.split(r'(?<=[?.])\s+', text)
                   if re.search(r'[A-Za-zÁÉÍÓÚáéíóú]{3}', x) and re.search(r'[?.]$', x.strip())]
        asks.extend(('Cluastuiscint', f'{segment} · greille {n}') for n in range(1, len(prompts) + 1))

    for p, t in lines:
        if not first <= p <= last:
            continue
        if SEG.match(t):
            close()
            head = ' '.join(t.split()[:3]).title()
            # A conversation's second part ("An Dara Mír") is addressed under its conversation.
            main = head if not head.startswith('An ') else main
            segment, body = head if head == main else f'{main} · {head}', []
            continue
        if segment is not None:
            if re.match(r'^An Chéad Mh?ír$', t) and segment == main:
                segment = f'{main} · An Chéad Mhír'
            body.append((p, t))
    close()
    # Composition: every titled choice, addressed under its printed section ("A AISTE …", "B SCÉAL", …).
    section = ''
    for p, t in lines:
        if p not in comp_pages:
            continue
        m = re.match(r'^([A-D])\s+\S.*\b\d+\s*m?h?arc$', t)
        if m:
            section = m.group(1)
            continue
        found = leaf_addresses(marker_nodes([(p, t)]))
        asks.extend(('Ceapadóireacht', f'{section}{address}') for address in found)
    return asks


def literature_nodes(lines):
    """Letter and roman markers of one literature option, up to its last printed tariff (a poem reprinted after its
    questions carries its own numerals, and nothing after the last "(N marc)" is an ask). A roman that opens on a
    letter ("(i) (a) Cad a dhéanann an spailpín …", then "(b)", "(c)", "(d)") holds those letters as its own parts,
    until the next roman: the Ordinary An Spailpín Fánach sets its first question so."""
    priced = [k for k, (_, t) in enumerate(lines) if PRICE.search(t)]
    last = priced[-1] if priced else len(lines)
    out = []
    under_roman = False
    for k, (_, t) in enumerate(lines):
        if k > last:
            break
        if NUM.match(t):
            continue  # stanza and line numbers in printed poems
        m2 = LET.match(t)
        if m2 and m2.group(2) and ROM.match(m2.group(2)):
            out.append((1, False, t))
            t = m2.group(2)
        mr = ROM.match(t)
        if mr and mr.group(2) and LET.match(mr.group(2)):
            out.append((2, False, t))
            t = mr.group(2)
            under_roman = True
        elif mr:
            under_roman = False
        for rx, lvl in ((LET, 3 if under_roman else 1), (ROM, 2)):
            m = rx.match(t)
            if m:
                out.append((lvl, has_text(lines, k, m.group(2) or ''), t))
                break
    return out


def paper2_asks(path):
    """Reading comprehensions' lettered parts, then each literature option's parts, of a 2022-onward Paper 2."""
    lines = lines_of(path)
    has_reading = any(re.search(r'L+[ÉE]+A+M+H+T+H+U+I+S+C+I+N+T', t, re.I) for p, t in lines if p > 3)
    alt_pages = [p for p, t in lines if re.search(r'\(A+l+t+\s*\d', t)]
    last_read = max(alt_pages) if alt_pages else 0
    if not has_reading:
        last_read = 0
    elif not alt_pages:
        starts = [p for k, (p, t) in enumerate(lines) if p > 3 and re.match(r'^(?:CEIST|Ceist)\s*2\b', t)
                  and any(re.search(r'PR[ÓO]S', lines[j][1], re.I) for j in range(k, min(k + 3, len(lines))))]
        last_read = (starts[0] - 1) if starts else 0
    reading = [(p, t) for p, t in lines if p <= last_read]
    literature = [(p, t) for p, t in lines if p > max(last_read, 1)]
    # Reading: only numbered questions with lettered parts (a passage's numbered paragraphs have none). Each
    # comprehension is addressed by its letter: Ordinary heads them "A – (50 marc)" or "A – 50 marc"; Higher prints
    # each one's questions under a "Ceisteanna" line, the first for A, the next for B.
    chunks, current, letter, seen = [], [], '', 0
    for line in reading:
        head = re.match(r'^([AB])\s*[–-]\s*\(?\d+\s*m?h?arc\)?$', line[1])
        if head or re.match(r'^Ceisteanna$', line[1]):
            chunks.append((letter, current))
            letter = head.group(1) if head else 'AB'[min(seen, 1)]
            seen += 0 if head else 1
            current = []
        current.append(line)
    chunks.append((letter, current))
    asks = []
    for prefix, chunk in chunks:
        nodes = marker_nodes(chunk, letter_roman=True)
        kept, i = [], 0
        while i < len(nodes):
            if nodes[i][0] == 0:
                j = i + 1
                while j < len(nodes) and nodes[j][0] > 0:
                    j += 1
                if any(n[0] == 1 for n in nodes[i + 1:j]):
                    kept += nodes[i:j]
                i = j
            else:
                i += 1
        asks.extend(('Léamhthuiscint', f'{prefix} {address}'.strip()) for address in leaf_addresses(kept, count_numbers=False))
    options, current, question = [], None, ''
    for p, t in literature:
        q = re.match(r'^(?:CEIST|Ceist)\s+([234])\b', t)
        if q:
            question = q.group(1)
        m = LIT_OPTION.match(t)
        # Some papers head an option "A – PRÓS AINMNITHE – (50 marc)" under its "CEIST 2": option 2A.
        lettered = re.match(r'^([A-F])\s*[–-]\s*(?:PR[ÓO]S|FIL[ÍI]OCHT|LITR[ÍI]OCHT)\b', t)
        if m or (lettered and question):
            current = {'head': m.group(1) if m else question + lettered.group(1), 'lines': []}
            options.append(current)
            continue
        if current is not None:
            current['lines'].append((p, t))
    for option in options:
        parts = leaf_addresses(literature_nodes(option['lines']), count_numbers=False)
        asks.extend(('Litríocht', f"{option['head']}{part}") for part in (parts or ['']))
    if not options:
        # No option heads in the text layer: the literature section is one tree of lettered parts.
        asks.extend(('Litríocht', part) for part in leaf_addresses(literature_nodes(literature), count_numbers=False))
    return asks


if __name__ == '__main__':
    path, component = sys.argv[1], sys.argv[2]
    found = paper1_asks(path) if component == '1' else paper2_asks(path)
    print(json.dumps(found, ensure_ascii=False, indent=1))
