#!/usr/bin/env python3
"""Where a Religious Education card is filed.

Unlike every other subject in this bank, Religious Education needs no keyword
matcher to shelve a card. The syllabus's units ARE the paper's sections, and
the paper prints the section over every ask: Section C is World Religions on
all ten papers in the corpus. So the topic is READ, not inferred, and there is
no "files under no syllabus topic" refusal bucket in this subject at all.

The section titles below are the papers' own, normalised to one casing — the
SEC sets them in capitals in 2021 and in title case afterwards, and prints
"The Bible: Literature and Sacred Text" and "...Sacred Texts" in different
years for the same section.
"""
import re

SECTIONS = {
    'A': 'The Search for Meaning and Values',
    'B': 'Christianity: Origins and Contemporary Expressions',
    'C': 'World Religions',
    'D': 'Moral Decision-Making',
    'E': 'Religion and Gender',
    'F': 'Issues of Justice and Peace',
    'G': 'Worship, Prayer and Ritual',
    'H': 'The Bible: Literature and Sacred Text',
    'I': 'Religion: The Irish Experience',
    'J': 'Religion and Science',
}

# Which unit of the syllabus each section belongs to, as the papers head them.
UNITS = {
    1: ['A'],
    2: ['B', 'C', 'D'],
    3: ['E', 'F', 'G', 'H', 'I', 'J'],
}


def topic_for(section):
    """The topic id for a paper section. Every ask has one; none can be missed."""
    if section not in SECTIONS:
        return None
    return f're-{section.lower()}'


STOP = {'the', 'a', 'an', 'of', 'in', 'to', 'and', 'for', 'is', 'are', 'was',
        'were', 'this', 'that', 'with', 'from', 'by', 'on', 'at', 'as', 'it',
        'what', 'which', 'how', 'why', 'you', 'your', 'their', 'they', 'one',
        'two', 'three', 'each', 'any', 'following', 'above', 'below', 'could',
        'can', 'may', 'might', 'would', 'have', 'has', 'had', 'be', 'been',
        'outline', 'explain', 'describe', 'examine', 'discuss', 'profile',
        'compare', 'trace', 'assess', 'suggest', 'identify', 'imagine',
        'using', 'used', 'name', 'give', 'state', 'list', 'about'}


def concept_for(text, fallback='ask'):
    """A level-independent slug for what the ask is about, from its own words.

    Shared by an HL card and its OL sibling where the two papers ask the same
    thing, which is what keeps a student's work when they drop level in
    spring. Derived from the ask, never typed.
    """
    words = re.findall(r"[a-z0-9']+", (text or '').lower())
    keep = [w for w in words if w not in STOP and len(w) > 2][:6]
    return '-'.join(keep) or fallback
