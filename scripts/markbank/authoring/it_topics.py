#!/usr/bin/env python3
"""Where an Italian card is filed, and which language its answer must be in.

The syllabus taxonomy already exists — curriculum.ts holds the Italian strands
and curriculumRegistry.ts publishes them as `italian:current` — so nothing here
invents a topic. It only says which of the published reading-comprehension
task types an ask belongs to, and it does so from the section the PAPER prints
it in, because this paper's sections ARE those task types:

    Higher   Section A    journalistic passage          italian-5-0
             Section B1   literary passage (unseen)     italian-5-1
             Section B2   literary passage, prescribed  italian-5-2
    Ordinary Section A    two short passages            italian-5-3
             Section B    five publicity pieces         italian-5-4
             Section B    …of which the matching task   italian-6-5

THE ANSWER LANGUAGE IS PART OF THE ASK
--------------------------------------
Higher sets its reading questions in ITALIAN and directs that they be answered
in Italian — "Rispondete in italiano alle domande 1, 2, 3, 4" is printed at the
head of every one of its twenty question pages — and then sets the LAST ask of
each comprehension in Irish and again in English, directing the opposite:
"Freagair an cheist seo a leanas i nGaeilge / Answer the following question in
English". Ordinary sets every ask in Irish and English and is answered in one
of those; its scheme's answers are in English throughout.

A card that does not say which language is wanted marks a right answer wrong,
so every card carries it, read from the language the question is actually
printed in rather than from its number — and checked against the number, which
is what the numbering rule is for.
"""
import re

# The published topic ids, from curriculum.ts via curriculumRegistry.ts. Named
# here so a change to either is a one-line change, and so nothing in this
# directory invents an id the registry does not hold.
JOURNALISTIC = 'italian-5-0'
UNSEEN_LITERARY = 'italian-5-1'
PRESCRIBED = 'italian-5-2'
SHORT_PASSAGES = 'italian-5-3'
PUBLICITY = 'italian-5-4'
SEQUENCING = 'italian-6-5'

TOPICS = {
    'hl': {'A': JOURNALISTIC, 'B1': UNSEEN_LITERARY,
           'B2A': PRESCRIBED, 'B2B': PRESCRIBED},
    'ol': {'A1': SHORT_PASSAGES, 'A2': SHORT_PASSAGES,
           'B1': PUBLICITY, 'B2': PUBLICITY, 'B3': PUBLICITY,
           'B4': PUBLICITY, 'B5': PUBLICITY},
}


def topic_for(level, section, matching=False):
    """The published topic id for one ask."""
    if matching:
        # The Ordinary paper's put-them-in-order task, which the syllabus
        # names in its written-production strand rather than its reading one:
        # "Correct Order / Sequencing Task (OL)".
        return SEQUENCING
    return TOPICS[level].get(section, PUBLICITY if level == 'ol' else JOURNALISTIC)


# What the question is written in. An Italian ask uses Italian function words
# and an Irish/English one does not; the two sets share nothing, which is what
# makes the test safe on a one-line question.
ITALIAN_WORDS = re.compile(
    r"\b(?:che|cosa|perch[ée]|come|quale|quali|quanto|dite|spiegate|indicate"
    r"|trovate|riferendovi|secondo|nella|nel|della|del|dei|delle|con|vostre"
    r"|parole|sezione|significa|individuate|descrivete|ci[òo]|sono|il|la|le"
    r"|un|una|di|per|alla|all|questo|questa)\b", re.I)
ENGLISH_IRISH_WORDS = re.compile(
    r'\b(?:what|how|why|name|identify|give|write|mention|which|does|did|do'
    r'|answer|refer|according|says?|details?|points?|looking|following'
    r'|tabhair|cad|c[ée]n|freagair|ainmnigh|conas|luaigh|sonra[íi]?|pointe'
    r'|liostaigh|d[ée]an|cuir|nGaeilge|Ghaeilge)\b', re.I)

ITALIAN = 'Italian'
ENGLISH_OR_IRISH = 'English or Irish'


def answer_language(level, text):
    """'Italian' or 'English or Irish' — never a guess about a blank string."""
    if level == 'ol':
        # Every Ordinary ask is set in Irish and in English, and its scheme's
        # answers are in English. There is no Italian-answered ask at this
        # level, so nothing is read from the wording.
        return ENGLISH_OR_IRISH
    it = len(ITALIAN_WORDS.findall(text or ''))
    en = len(ENGLISH_IRISH_WORDS.findall(text or ''))
    return ITALIAN if it >= en else ENGLISH_OR_IRISH


def language_note(language):
    """The instruction a card carries so a right answer is not marked wrong."""
    if language == ITALIAN:
        return ('The examination paper prints this question in Italian and '
                'heads its page "Rispondete in italiano alle domande 1, 2, 3, '
                '4" — it must be answered in Italian.')
    return ('The examination paper prints this question in Irish and in '
            'English and directs that it be answered in one of those, not in '
            'Italian.')


STOP = {'the', 'a', 'an', 'of', 'in', 'to', 'and', 'for', 'is', 'are', 'was',
        'what', 'which', 'how', 'why', 'you', 'your', 'their', 'they', 'one',
        'two', 'three', 'each', 'any', 'give', 'name', 'state', 'identify',
        'mention', 'write', 'che', 'cosa', 'come', 'quale', 'quali', 'con',
        'del', 'della', 'dei', 'delle', 'nel', 'nella', 'per', 'alla', 'dite',
        'sono', 'una', 'uno', 'sezione', 'riferendovi', 'vostre', 'parole',
        'section', 'par', 'details', 'detail'}


def concept_for(text, fallback='ask'):
    """A level-independent slug for what the ask is about, from its own words.

    Shared by a Higher card and its Ordinary sibling where both papers ask the
    same thing, which is what keeps a student's work when they drop level in
    spring. Derived from the ask, never typed.
    """
    words = re.findall(r"[a-z0-9']+", (text or '').lower())
    keep = [w for w in words if w not in STOP and len(w) > 2][:6]
    return '-'.join(keep) or fallback
