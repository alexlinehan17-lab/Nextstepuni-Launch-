#!/usr/bin/env python3
"""Where a History card is filed.

The syllabus's four FIELDS-and-areas are exactly the paper's own address, so
nothing here is inferred from wording:

    Early Modern  Section 2  ->  Early Modern field, Ireland 1494-1815
    Early Modern  Section 3  ->  Early Modern field, Europe and the wider world
    Later Modern  Section 2  ->  Later Modern field, Ireland 1815-1993
    Later Modern  Section 3  ->  Later Modern field, Europe and the wider world

and each field-and-area holds the six numbered TOPICS the paper heads its
questions with. A card's topic is READ off the paper, never matched, so there
is no "files under no syllabus topic" refusal bucket in this subject.

THE THREE UNITS THAT PRINT NO TOPIC NUMBER OF THEIR OWN

*The Documents-Based Question.* Section 1 prints its case study's topic under
its own heading — "Europe and the wider world: Topic 6 / The United States and
the world, 1945-1989" — so its cards file there.

*The extra Part A* that 2023-2025 Ordinary print for candidates following the
alternative instructions. The paper heads it with nothing at all. It does not
need a hand-written table: the extra Part A is on the topic the DBQ TOOK OUT of
Sections 2 and 3, which is why it exists — the alternative instructions let a
candidate answer three questions across two topics, and the extra unit restores
the topic the documents question removed. Six papers print one, and in all six
the extract is on the DBQ's own topic:

    2023 OL Later Modern   DBQ Ireland Topic 5   extra: Apprentice Boys of
                                                 Derry, Derry riots 1969
    2023 OL Early Modern   DBQ Ireland Topic 2   extra: the Nine Years' War
    2024 OL Later Modern   DBQ Europe Topic 3    extra: the Jarrow March, 1936
    2024 OL Early Modern   DBQ Europe Topic 1    extra: Henry VIII's divorce
    2025 OL Later Modern   DBQ Europe Topic 3    extra: working for Stalin
    2025 OL Early Modern   DBQ Europe Topic 1    extra: the New World, Seville

hist_all.py asserts the rule holds on every paper that prints one.
"""
import re

# The four field-and-area groups, and the six topics each holds, exactly as the
# canonical curriculum records them (curriculum.ts, groups history-0..history-3)
# and as the papers head them.
STRANDS = {
    ('em', '2'): ('hist-em-irl', 'Early Modern field — Ireland, 1494-1815'),
    ('em', '3'): ('hist-em-eur',
                  'Early Modern field — Europe and the wider world, 1492-1815'),
    ('lm', '2'): ('hist-lm-irl', 'Later Modern field — Ireland, 1815-1993'),
    ('lm', '3'): ('hist-lm-eur',
                  'Later Modern field — Europe and the wider world, 1815-1993'),
}

# The topic titles the papers print. Read off the corpus rather than typed, and
# asserted against both documents by hist_all.py.
TITLES = {
    'hist-em-irl': [
        'Reform and Reformation in Tudor Ireland, 1494-1558',
        'Rebellion and conquest in Elizabethan Ireland, 1558-1603',
        'Kingdom versus colony \u2013 the struggle for mastery in Ireland, 1603-1660',
        'Establishing a colonial ascendancy, 1660-1715',
        'Colony versus kingdom \u2013 tensions in mid-18th century Ireland, 1715-1770',
        'The end of the Irish kingdom and the establishment of the Union, 1770-1815',
    ],
    'hist-em-eur': [
        'Europe from Renaissance to Reformation, 1492-1567',
        'Religion and power: politics in the later 16th century, 1567-1609',
        'The eclipse of Old Europe, 1609-1660',
        'Europe in the age of Louis XIV, 1660-1715',
        'Establishing empires, 1715-1775',
        'Empires in revolution, 1775-1815',
    ],
    'hist-lm-irl': [
        'Ireland and the Union, 1815-1870',
        'Movements for political and social reform, 1870-1914',
        'The pursuit of sovereignty and the impact of partition, 1912-1949',
        'The Irish diaspora, 1840-1966',
        'Politics and society in Northern Ireland, 1949-1993',
        'Government, economy and society in the Republic of Ireland, 1949-1989',
    ],
    'hist-lm-eur': [
        'Nationalism and state formation in Europe, 1815-1871',
        'Nation states and international tensions, 1871-1920',
        'Dictatorship and democracy in Europe, 1920-1945',
        'Division and realignment in Europe, 1945-1992',
        'European retreat from empire and the aftermath, 1945-1990',
        'The United States and the world, 1945-1989',
    ],
}


def topic_for(field, section, number):
    """The topic id for a field, paper section and printed topic number."""
    strand = STRANDS.get((field, str(section)))
    if not strand or not 1 <= int(number) <= 6:
        return None
    return f'{strand[0]}-{int(number)}'


def strand_for(field, section):
    return STRANDS.get((field, str(section)))


STOP = {'the', 'a', 'an', 'of', 'in', 'to', 'and', 'for', 'is', 'are', 'was',
        'were', 'this', 'that', 'with', 'from', 'by', 'on', 'at', 'as', 'it',
        'what', 'which', 'how', 'why', 'you', 'your', 'their', 'they', 'one',
        'two', 'three', 'each', 'any', 'following', 'above', 'below', 'could',
        'can', 'may', 'might', 'would', 'have', 'has', 'had', 'be', 'been',
        'outline', 'explain', 'describe', 'examine', 'discuss', 'according',
        'compare', 'trace', 'assess', 'suggest', 'identify', 'document',
        'documents', 'briefly', 'extract', 'answer', 'give', 'state', 'name',
        'about', 'both', 'refer', 'referring', 'make', 'detailed', 'reference'}


def concept_for(text, fallback='ask'):
    """A level-independent slug for what the ask is about, from its own words.

    Shared by a Higher card and its Ordinary sibling where the two papers ask
    the same thing, which is what keeps a student's work when they drop level
    in spring. Derived from the ask, never typed.
    """
    words = re.findall(r"[a-z0-9']+", (text or '').lower())
    keep = [w for w in words if w not in STOP and len(w) > 2][:6]
    return '-'.join(keep) or fallback
