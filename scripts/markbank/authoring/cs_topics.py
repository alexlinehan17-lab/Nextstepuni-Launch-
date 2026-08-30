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
                   # "Operating system layers: Hardware, OS, Application, User"
                   # is the spec's own list against 2.11-2.13.
                   # 2.11 is "describe the different components within a
                   # computer and the function of those components". A solid
                   # state drive is such a component; the paper names it and
                   # the specification names the category.
                   r'hardware|software\b|firmware|peripheral|storage device|'
                   r'solid state drive|hard disk drive|\bssds?\b|\bhdds?\b|'
                   r'input device|output device|motherboard|clock speed|'
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
                   # 2.16 lists "array" among the data types. Indexing one and
                   # slicing one are how a program uses it, and the papers ask
                   # about both without ever using the word "array".
                   r'\barray\b|\bindex(?:es|ing)?\b|slice expression|'
                   r'\bascii\b|unicode|utf-8|character set|emoji|'
                   r'encode|decode|two.s complement|database|\bsql\b|'
                   # 2.18 is "collect, store and sort both continuous and
                   # discrete data" -- the paper asks about the two words one
                   # at a time ("either discrete data or continuous data"),
                   # which the joined phrase could never match.
                   r'record|field|discrete data|continuous data|'
                   r'continuous and discrete|information system)\b'),
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
                  # 1.20 is "collaborate and assign roles and responsibilities
                  # within a team to tackle a computing task" -- the paper puts
                  # a name on the role and asks about it.
                  r'project manage(?:ment|r)|team leader|'
                  r'prototyp\w+|reflect\w* on the design)\b'),
    # 1.4 "solve problems using skills of logic" and 1.5 "evaluate
    # alternative solutions to computational problems": a game-strategy
    # question is a logic problem, which is where the spec puts it.
    ('cs-1-1', 8, r'\b(computational thinking|problem solving|logical thinking|'
                  r'algorithmic thinking|heuristic|simulation|modelling|'
                  r'automat\w+|systematic (?:process|approach)|'
                  r'winning (?:position|move|strategy)|losing position|'
                  r'best move|strategy would you|deconstruct\w*|'
                  # 1.8: "evaluate the costs and benefits of the use of
                  # computing technology in automating processes".
                  r'automating processes|costs and benefits|'
                  r'alternative solution|trade[- ]?off)\b'),
    # ── Strand 3: the four applied learning tasks ──────────────────────────
    # The specification's own heading is "Embedded systems", plural, and 3.11
    # to 3.14 read "within an embedded system", "digital inputs and outputs",
    # "measure and store data returned from an analogue input", "design
    # automated applications using embedded systems". The singular-only
    # pattern could not match its own heading: "Describe two advantages of
    # embedded systems" filed under no topic at all.
    ('cs-3-4', 10, r'\b(embedded systems?|microprocessor|micro:?bit|arduino|'
                   r'sensors?|actuators?|analogue inputs?|'
                   r'digital (?:inputs?|outputs?)|automated applications?|'
                   r'\bgpio\b)\b'),
    # 3.2 is "create a basic relational database to store and retrieve a
    # variety of forms of data types", and the specification's own list for
    # this task is "File systems and relational databases". A foreign key is
    # the relation; a primary key is what it points at.
    ('cs-3-1', 9, r'\b(website|web page|\bhtml\b|\bcss\b|javascript|'
                  r'relational database|web design|hyperlink|browser|'
                  r'foreign key|primary key)\b'),
    ('cs-3-2', 9, r'\b(analytics|data set|visualis\w+|chart|graph of the data|'
                  r'trend|correlat\w+|statistic\w*)\b'),
    # 3.8 "develop a model that will allow different scenarios to be tested"
    # and 3.9 "analyse and interpret the outcome of simulations".
    ('cs-3-3', 9, r'\b(agent[- ]based|emergent behaviour|scenario|'
                  r'simulat\w+ (?:model|the)|model that|in the model|'
                  r'test in the model|outcome of the simulation)\b'),
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
