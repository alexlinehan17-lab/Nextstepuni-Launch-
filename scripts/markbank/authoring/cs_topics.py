#!/usr/bin/env python3
"""File a Computer Science part under a syllabus topic from its wording.

    python3 scripts/markbank/authoring/cs_topics.py        # unmatched report

Every term below is lifted from the specification's own "Students learn about"
column, which is the list of things the document says students must learn under
each heading. Nothing here is invented vocabulary: "Sorting: Simple sort, Insert
sort, Bubble sort, Quicksort" sits against S2 Algorithms in the specification,
"CPU: ALU, Registers, Program counter, Memory" and "Basic electronics: voltage,
current, resistors, capacitors, transistors" against S2 Computer systems, and
"8-bit ASCII / Non-Roman character sets / Unicode: UTF-8, Emojis" against S2
Data.

Most specific match wins. Anything unmatched is REPORTED, never filed under a
default — a wrong shelf sends a student to revise the wrong thing, and a gap
only asks a person to look. There are no existing Computer Science cards to
score this against, so unlike chem_topics it carries no measured accuracy: it
is a first pass over a fresh subject and every card it suggests for is read.
"""
import collections
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

RULES = [
    # ── Strand 2: the five core concepts, most specific ────────────────────
    # 2.13 puts the BINARY NUMBER SYSTEM and conversion between binary,
    # hexadecimal and decimal under Computer systems, not under Data; 2.15 puts
    # the web protocols there too ("Web infrastructure - Computer Network
    # Protocols: HTTP, TCP, IP, VOIP"). Data is 2.16-2.18: data types, ASCII
    # and Unicode, information systems.
    ('cs-2-3', 11, r'\b(logic gate|and gate|or gate|nand|nor|xor\b|truth table|'
                   r'\bcpu\b|\balu\b|register|program counter|main memory|\bram\b|'
                   r'\brom\b|cache|fetch[- ]decode|von neumann|transistor|'
                   r'resistor|capacitor|voltage|current|circuit|binary adder|'
                   r'operating system|hardware component|'
                   r'binary(?: number| format| digit)?|hexadecimal|denary|'
                   r'\bbits?\b|\bbytes?\b|base 2|base 16|'
                   r'\bhttps?\b|\btcp\b|\bip\b|\bvoip\b|protocol|'
                   r'world wide web|\bwww\b|client[- ]server|the internet|'
                   r'network|packet|router|bandwidth|latency|'
                   r'digital and analogue|analogue input)\b'),
    ('cs-2-2', 11, r'\b(bubble sort|insert(?:ion)? sort|simple sort|quicksort|'
                   r'linear search|binary search|pseudo ?code|algorithm|'
                   r'recursi\w+|iteration|\bloop\b|selection|conditional|'
                   r'complexity|big[- ]o\b|efficiency of|flowchart|procedure|'
                   r'function call|'
                   # 2.7 "implement algorithms using a programming language":
                   # a question about a printed program is a question about the
                   # algorithm it implements.
                   r'python|program(?:me)?\b|\bcode\b|variable|'
                   r'output of the following|what is the output|'
                   r'pseudocode|subroutine|parameter|\bwhile\b|\bfor loop\b)\b'),
    ('cs-2-4', 11, r'\b(data type|boolean|integer|\breal\b|\bchar\b|\bstring\b|'
                   r'\barray\b|\bascii\b|unicode|utf-8|character set|emoji|'
                   r'encode|decode|two.s complement|database|\bsql\b|'
                   r'record|field|continuous and discrete|information system)\b'),
    ('cs-2-5', 11, r'\b(unit test|function test|system test|debug\w*|'
                   r'syntax error|semantic error|logic error|runtime error|'
                   r'test case|test plan|validat\w+|verif\w+|'
                   r'stages? in software testing)\b'),
    ('cs-2-1', 10, r'\b(abstraction|modular design|module\b|abstract model|'
                   r'decompos\w+|pattern recognition|generalis\w+|'
                   r'wholes and parts)\b'),
    # ── Strand 1 ───────────────────────────────────────────────────────────
    ('cs-1-2', 10, r'\b(ethic\w*|society|social (?:media|impact)|privacy|'
                   r'turing machine|the internet|machine learning|'
                   r'artificial intelligence|\bai\b|user interface|usability|'
                   r'universal design|adaptive technology|accessib\w+|'
                   r'careers?|digital divide|cyber ?security|data protection|'
                   r'\bgdpr\b|quantum comput\w+|cloud comput\w+|edge comput\w+)\b'),
    ('cs-1-3', 9, r'\b(design process|iterative design|staged design|'
                  r'assign\w* roles|work(?:ing)? in a team|collaborat\w+|'
                  r'stakeholder|end users?|requirements?|version control|'
                  r'project management|prototyp\w+|reflect\w* on the design)\b'),
    ('cs-1-1', 8, r'\b(computational thinking|problem solving|logical thinking|'
                  r'algorithmic thinking|heuristic|simulation|modelling|'
                  r'automat\w+|systematic (?:process|approach))\b'),
    # ── Strand 3: the four applied learning tasks ──────────────────────────
    ('cs-3-4', 10, r'\b(embedded system|microprocessor|micro:?bit|arduino|'
                   r'sensor|actuator|analogue input|digital (?:input|output)|'
                   r'\bgpio\b)\b'),
    ('cs-3-1', 9, r'\b(website|web page|\bhtml\b|\bcss\b|javascript|'
                  r'relational database|web design|hyperlink|browser)\b'),
    ('cs-3-2', 9, r'\b(analytics|data set|visualis\w+|chart|graph of the data|'
                  r'trend|correlat\w+|statistic\w*)\b'),
    ('cs-3-3', 9, r'\b(agent[- ]based|emergent behaviour|scenario|'
                  r'simulat\w+ (?:model|the)|model that)\b'),
]
COMPILED = [(t, w, re.compile(p, re.I)) for t, w, p in RULES]


def topic_for(text):
    """(topic id, the phrase that decided it) — or (None, None)."""
    best = (0, None, None)
    for tid, weight, rx in COMPILED:
        m = rx.search(text or '')
        if m and weight > best[0]:
            best = (weight, tid, m.group(0))
    return best[1], best[2]


def concept_for(text, fallback='part'):
    """A slug for the card's concept, from the ask's own first words."""
    words = re.findall(r"[a-z0-9']+", (text or '').lower())
    stop = {'the', 'a', 'an', 'of', 'in', 'to', 'and', 'for', 'is', 'are', 'was',
            'were', 'this', 'that', 'with', 'from', 'by', 'on', 'at', 'as', 'it',
            'what', 'which', 'state', 'give', 'name', 'write', 'explain'}
    keep = [w for w in words if w not in stop][:6]
    return '-'.join(keep) or fallback


def main():
    """What the rules cannot file, so the gaps are visible rather than guessed."""
    sys.path.insert(0, DIR)
    import paper as PP                                       # noqa: E402
    import reconcile as R                                    # noqa: E402
    from paper_census import census_subject                  # noqa: E402
    idx = R.leaf_index(census_subject('computer-science'))
    papers, hit, miss = {}, collections.Counter(), []
    for (yr, lv, _), leaves in sorted(idx.items()):
        P = papers.setdefault((yr, lv), PP.Paper('computer-science', yr, lv))
        for leaf in leaves:
            q, letter, roman = leaf[1], leaf[2], leaf[3]
            try:
                ask = P.text(q, letter, roman) or ''
            except Exception:                                # noqa: BLE001
                ask = ''
            tid, _ = topic_for(ask)
            if tid:
                hit[tid] += 1
            else:
                miss.append(f'{yr} {lv} Q{q}: {" ".join(ask.split())[:70]}')
    total = sum(hit.values()) + len(miss)
    print(f'{total} asks: {sum(hit.values())} filed, {len(miss)} unmatched')
    for tid, n in sorted(hit.items()):
        print(f'   {tid}  {n}')
    print('\nunmatched (first 20):')
    for m in miss[:20]:
        print(f'   {m}')


if __name__ == '__main__':
    main()
