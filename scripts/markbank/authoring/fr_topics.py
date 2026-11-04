#!/usr/bin/env python3
"""Where a French card is filed, and which language its answer must be in.

The syllabus taxonomy already exists — curriculum.ts holds the French strands
and curriculumRegistry.ts publishes them as `french:current` — so nothing here
invents a topic. It only decides which of the published reading-comprehension
topics an ask belongs to, and it does so from what the PAPER prints.

WHICH COMPREHENSION IS WHICH
----------------------------
The syllabus names four kinds of reading comprehension, and the paper's own
source credit says which one it has set:

    Higher Q.1   Le Figaro · La-Zep.fr · Aujourd'hui en France · France Inter
    Higher Q.2   LE GRAND SAUT 3 · Les chats éraflés · TROIS (Valérie Perrin)
                 · Le Choix du monde · La famille Martin

Journalism first, a novel second, in all five sittings. Ordinary sets four,
and its own English lead-in names the genre outright — "In this interview,
adapted from the magazine Phosphore…", "…is adapted from various websites" —
with the last of the four always the literary extract (Le Secret des Hurlants,
Le professeur de musique, Nuit blanche au musée, À plein tube !).

So the classification is read, in this order: the last comprehension of a
sitting is the literary one; otherwise the lead's own genre word; otherwise
journalism, which is what the remaining credits name.

THE ANSWER LANGUAGE IS PART OF THE ASK
--------------------------------------
Section A prints some questions in French and some in Irish and English, and
the paper directs that each be answered in the language it was set in — "Aux
autres questions en français, il faut répondre en français. Aux questions
posées en irlandais/anglais, il faut répondre en irlandais ou en anglais." The
scheme enforces it: "Answers given in the wrong language… -1 mark" at Higher,
"if answered through English / Irish – allow half marks only" at Ordinary. A
card that does not say which language is wanted marks a right answer wrong, so
every card carries it, read from the language the question is actually printed
in.
"""
import re

# The published topic ids, from curriculum.ts via curriculumRegistry.ts. Named
# here so a change to either is a one-line change, and so nothing in this
# directory invents an id the registry does not hold.
JOURNALISTIC = 'french-5-0'
LITERARY = 'french-5-1'
INTERVIEW = 'french-5-2'
WEBSITE = 'french-5-3'
CLOZE = 'french-6-6'

GENRE = [
    (re.compile(r'\binterview\b|\bagallamh\b', re.I), INTERVIEW),
    (re.compile(r'\bweb\s?sites?\b|\bshu[íi]omh|\bsu[íi]omh', re.I), WEBSITE),
]

# How many reading comprehensions each level sets. The last one is the literary
# extract at both levels, which the source credits confirm in all ten sittings.
LAST_RC = {'hl': 2, 'ol': 4}


def topic_for(level, rc, lead):
    """The published topic id for one reading comprehension."""
    if rc == LAST_RC.get(level):
        return LITERARY
    for pattern, topic in GENRE:
        if pattern.search(lead or ''):
            return topic
    return JOURNALISTIC


# What the question is written in. Read from the question's own words: the
# paper prints an ask either in French or in Irish and English, never in both
# on the card, and the answer language follows the question language.
FRENCH_WORDS = re.compile(
    r"\b(?:qu['’]est-ce|pourquoi|comment|relevez|trouvez|citez|donnez|quelle?s?"
    r"|dans|selon|d['’]apr[èe]s|est-ce|expliquez|nommez|identifiez|que|cette"
    r"|pense|montre|veut|vous|votre|des|les|une?)\b", re.I)
ENGLISH_WORDS = re.compile(
    r'\b(?:what|how|why|name|identify|give|write|mention|which|does|did|do'
    r'|agree|answer|refer|according|says?|two|one|detail|details|points?)\b',
    re.I)


def answer_language(text):
    """'French' or 'English or Irish' — never a guess about a blank string."""
    fr = len(FRENCH_WORDS.findall(text or ''))
    en = len(ENGLISH_WORDS.findall(text or ''))
    return 'French' if fr >= en else 'English or Irish'


def language_note(language):
    """The instruction a card carries so a right answer is not marked wrong."""
    if language == 'French':
        return ('This question is printed in French and must be answered in '
                'French; the marking scheme penalises an answer given in '
                'Irish or English.')
    return ('This question is printed in Irish and in English and must be '
            'answered in Irish or English; the marking scheme penalises an '
            'answer given in French.')


STOP = {'the', 'a', 'an', 'of', 'in', 'to', 'and', 'for', 'is', 'are', 'was',
        'what', 'which', 'how', 'why', 'you', 'your', 'their', 'they', 'one',
        'two', 'three', 'each', 'any', 'give', 'name', 'state', 'identify',
        'mention', 'write', 'que', 'qui', 'quel', 'quelle', 'est', 'ce', 'se',
        'dans', 'pour', 'par', 'sur', 'aux', 'avec', 'les', 'des', 'une', 'un',
        'section', 'roinn', 'relevez', 'trouvez', 'citez', 'donnez', 'comment',
        'pourquoi', 'selon'}


def concept_for(text, fallback='ask'):
    """A level-independent slug for what the ask is about, from its own words.

    Shared by a Higher card and its Ordinary sibling where both papers ask the
    same thing, which is what keeps a student's work when they drop level in
    spring. Derived from the ask, never typed.
    """
    words = re.findall(r"[a-z0-9']+", (text or '').lower())
    keep = [w for w in words if w not in STOP and len(w) > 2][:6]
    return '-'.join(keep) or fallback
