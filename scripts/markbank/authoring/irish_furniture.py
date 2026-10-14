#!/usr/bin/env python3
"""Boxed page headings that the scheme PDFs' text layer stores inside answer-key text.

Each SEC scheme page prints its section heading in a box ("Ceist 3 FILÍOCHT 30 marc",
"A – (50 marc)" …). The text layer stores that box after the page body, so a key lifted
across a page boundary can carry it. These headings are not marking content. They are
removed by EXACT string match only: the list below is pinned (test/irishSchemeFurniture.test.ts),
every entry is a heading that ends in its printed mark total, and no partial match, prefix
or pattern is ever removed, so no answer wording can be stripped by this rule.
"""
from __future__ import annotations
import re

HEADINGS = (
    # Higher Paper 2 literature boxes (2022 prints the Ceist box with brackets, 2024–2026 without).
    'FILÍOCHT AINMNITHE nó FILÍOCHT ROGHNACH 30 marc',
    'PRÓS AINMNITHE nó PRÓS ROGHNACH 30 marc',
    'Ceist 2 PRÓS 30 marc',
    'Ceist 3 FILÍOCHT 30 marc',
    'Ceist 2 PRÓS (30 marc)',
    'Ceist 3 FILÍOCHT (30 marc)',
    # Ordinary Paper 1 composition box.
    'Cuid II An Cheapadóireacht 100 marc',
    # Ordinary Paper 2 reading passage boxes (2024 bracketed, 2025 plain).
    'A – (50 marc)',
    'B – (50 marc)',
    'A – 50 marc',
    'B – 50 marc',
)
_PATTERN = re.compile('|'.join(r'\s*' + re.escape(h) + r'(?=\s|$)\s*' for h in sorted(HEADINGS, key=len, reverse=True)))


def strip_text(text):
    """Remove every exact heading occurrence; return (text, count)."""
    count = 0

    def gap(match):
        nonlocal count
        count += 1
        start, end = match.start() == 0, match.end() == len(match.string)
        return '' if (start or end) else ' '
    return _PATTERN.sub(gap, text), count


def strip_card(card):
    """Strip headings from every guidance string of one card in place; return the number removed."""
    removed = 0
    for criterion in card['criteria']:
        cleaned = []
        for text in criterion['guidance']:
            text, n = strip_text(text)
            removed += n
            cleaned.append(text)
        criterion['guidance'] = cleaned
    return removed
