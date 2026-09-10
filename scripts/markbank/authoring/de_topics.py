#!/usr/bin/env python3
"""Where a German card is filed, and which language its answer must be in.

The syllabus taxonomy already exists — curriculum.ts holds the German strands
and curriculumRegistry.ts publishes them as `german:current` — so nothing here
invents a topic. It only decides which published topic an ask belongs to, and
it does so from what the PAPER prints.

WHICH TEXT IS WHICH
-------------------
Every German reading comprehension closes with its own source credit, and the
credit says what kind of text it is:

    TEXT I   "Nach: Arno Geiger: Das glückliche Geheimnis"     a book
             "Nach: Caroline Wahl, 22 Bahnen"                  a novel
    TEXT II  "Quellen: taz.de / sueddeutsche.de / welt.de"     journalism
    TEXT III "Nach: zeit.de / sportalpen.com / br.de"          journalism

An author and a title on TEXT I in all ten sittings; web and magazine sources
on TEXT II and TEXT III in all ten. So the classification is read from the
credit — a credit naming a DOMAIN is journalism, one naming a person is a
literary extract — and where the credit cannot be read the position decides,
which the credits themselves confirm: TEXT I is the literary one.

THE ANSWER LANGUAGE IS PART OF THE ASK, AND IT IS NOT A SUBJECT CONSTANT
------------------------------------------------------------------------
The paper prints the instruction itself, above the questions it governs and in
both of its own languages: "Lesen Sie Text I. Beantworten Sie Frage 1 (a), (b)
und (c) auf Deutsch." then "Freagair Ceist 2, 3 agus 4 i nGaeilge." / "Answer
Questions 2, 3 and 4 in English." So ONE comprehension is answered in two
different languages, and the scheme prices the difference: "Answers in language
not specified = half marks" at Higher, "Where all answers are in German: Award
half marks only if manipulation of relevant information is attempted" at
Ordinary. A card that does not say which language is wanted marks a right
answer wrong, so every card carries it — read from the language the question is
printed in, which is what de_scheme._language_of decides and what the paper's
own instruction line confirms.
"""
import re

# The published topic ids, from curriculum.ts via curriculumRegistry.ts. Named
# here so a change to either is a one-line change, and so nothing in this
# directory invents an id the registry does not hold.
JOURNALISTIC = 'german-6-0'      # Comprehension — Magazine / Newspaper Text
LITERARY = 'german-6-1'          # Comprehension — Novel / Short Story
GRAMMAR = 'german-3-4'           # Applied Grammar (Angewandte Grammatik)
WRITTEN = 'german-3-3'           # Written Production
LISTENING = 'german-3-1'         # Listening Comprehension (Hörverständnis)

# The source credit the paper prints at the foot of a passage.
CREDIT = re.compile(r'^\s*(?:Nach|Quellen?|Aus|Adaptiert)\s*:\s*(.+)$', re.I)
# A credit that names a website or a magazine rather than an author.
DOMAIN = re.compile(r'https?://|\bwww\.|\.(?:de|ch|at|com|net|org|eu)\b'
                    r'|\bmagazin\b|\bZEIT ?Campus\b', re.I)


def topic_for(unit, credit):
    """The published topic id for one unit of the paper."""
    if unit == 'AG':
        return GRAMMAR
    if unit in ('AT', 'SP'):
        return WRITTEN
    if unit.startswith('L'):
        return LISTENING
    if credit:
        return JOURNALISTIC if DOMAIN.search(credit) else LITERARY
    # No readable credit — 2022 and 2024 Higher set theirs across two printed
    # lines. The position decides, and the eighteen credits that ARE readable
    # agree with it in every sitting: TEXT I is the literary extract.
    return LITERARY if unit == 'T1' else JOURNALISTIC


TEXT_TITLE = {
    'T1': 'TEXT I: LESEVERSTÄNDNIS',
    'T2': 'TEXT II: LESEVERSTÄNDNIS',
    'T3': 'TEXT III: LESEVERSTÄNDNIS',
    'AG': 'ANGEWANDTE GRAMMATIK',
    'AT': 'ÄUSSERUNG ZUM THEMA',
    'SP': 'SCHRIFTLICHE PRODUKTION',
}


def language_note(language):
    """The instruction a card carries so a right answer is not marked wrong."""
    if language == 'German':
        return ('This question is printed in German and must be answered in '
                'German; the marking scheme halves the marks for an answer '
                'given in the language not specified.')
    return ('This question is printed in Irish and in English and must be '
            'answered in Irish or English; the marking scheme halves the marks '
            'for an answer given in the language not specified.')


STOP = {'the', 'a', 'an', 'of', 'in', 'to', 'and', 'for', 'is', 'are', 'was',
        'what', 'which', 'how', 'why', 'you', 'your', 'their', 'they', 'one',
        'two', 'three', 'each', 'any', 'give', 'name', 'state', 'identify',
        'mention', 'write', 'details', 'detail', 'der', 'die', 'das', 'des',
        'dem', 'den', 'ein', 'eine', 'einen', 'einem', 'eines', 'und', 'ist',
        'sind', 'sie', 'was', 'wie', 'warum', 'wer', 'wo', 'geben', 'nennen',
        'beschreiben', 'schreiben', 'erklaren', 'section', 'roinn', 'par',
        'lines', 'line', 'zeile', 'abschnitt'}


def concept_for(text, fallback='ask'):
    """A level-independent slug for what the ask is about, from its own words.

    Shared by a Higher card and its Ordinary sibling where both papers ask the
    same thing, which is what keeps a student's work when they drop level in
    spring. Derived from the ask, never typed.
    """
    words = re.findall(r"[a-z0-9']+", (text or '').lower())
    keep = [w for w in words if w not in STOP and len(w) > 2][:6]
    return '-'.join(keep) or fallback
