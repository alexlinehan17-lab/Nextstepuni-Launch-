#!/usr/bin/env python3
"""Where a Russian card is filed, and which language its answer must be in.

The syllabus taxonomy already exists — curriculum.ts holds the Russian strands
and deck.ts publishes them — so nothing here invents a topic. Its fourth
strand, "Written Paper — Task Types", names the paper's own questions one for
one, which is why a card is filed by the QUESTION it was printed under:

    russian-3-0  Comprehension — Reading Text with Questions in English
    russian-3-1  Summary in English
    russian-3-2  Language Awareness Tasks
    russian-3-3  Structuring Discourse
    russian-3-4  Information Retrieval — Everyday Texts (OL)
    russian-3-5  Mix and Match (OL)
    russian-3-6  Short Answers — Cultural Awareness (OL)
    russian-3-7  Grammar & Language Use
    russian-3-8  Short Essay (~50 Words, HL)
    russian-3-9  Guided / Extended Writing

THE ANSWER LANGUAGE IS PART OF THE ASK
--------------------------------------
Every comprehension and retrieval ask is set in Irish and in English on the
same printed lines and directed to be answered in one of those — the paper
heads its question pages "FREAGAIR NA CEISTEANNA SEO A LEANAS i nGAEILGE /
ANSWER THE FOLLOWING QUESTIONS IN ENGLISH" — while the language-awareness
questions are answered in RUSSIAN, and the scheme prices the difference on its
own first page: "Language of answer: If an answer is supplied in the wrong
language: When it should be English: award NO marks (except in the listening
comprehension where there is no penalty for answering in the wrong language);
When it should be Russian: award NO marks."

A card that does not say which language is wanted marks a right answer wrong,
so every card carries it, read from the ask rather than from its number.
"""
import re

# The published topic ids, from curriculum.ts. Named here so a change to the
# canonical file is a one-line change, and so nothing in this directory
# invents an id the deck does not hold.
COMPREHENSION = 'russian-3-0'
SUMMARY = 'russian-3-1'
LANGUAGE_AWARENESS = 'russian-3-2'
STRUCTURING = 'russian-3-3'
RETRIEVAL = 'russian-3-4'
MIX_AND_MATCH = 'russian-3-5'
SHORT_ANSWERS = 'russian-3-6'
GRAMMAR = 'russian-3-7'
SHORT_ESSAY = 'russian-3-8'
GUIDED_WRITING = 'russian-3-9'
CULTURAL_AWARENESS = 'russian-2-0'

TOPICS = {
    'C1': COMPREHENSION, 'CD': COMPREHENSION, 'C2': SUMMARY,
    'LA1': LANGUAGE_AWARENESS, 'LA2': LANGUAGE_AWARENESS,
    'CA1': CULTURAL_AWARENESS, 'SD': STRUCTURING,
    'IR1': RETRIEVAL, 'IR2': RETRIEVAL, 'MM': MIX_AND_MATCH,
    'SA': SHORT_ANSWERS, 'GR': GRAMMAR, 'SE': SHORT_ESSAY,
    'GW': GUIDED_WRITING, 'EW': GUIDED_WRITING,
}


def topic_for(unit):
    return TOPICS[unit]


ENGLISH_OR_IRISH = 'English or Irish'
RUSSIAN = 'Russian'

# An ask answered in Russian says so, in the words the paper and the scheme
# both use: "list them in Russian", "Supply the infinitive/dictionary form",
# "Put the words in brackets into the correct form".
RUSSIAN_ANSWER = re.compile(
    r'\bin\s+Russian\b|\binfinitive\b|\bnominative\b|\bcorrect\s+form\b|'
    r'\bparts?\s+of\s+speech\b|\bcursive\b|\bhandwritten\b', re.I)


def answer_language(unit, text):
    """'Russian' or 'English or Irish' — read from the ask, never from a number.

    The comprehension and retrieval questions are the paper's own answer-in-
    English half and are never answered in Russian; the language-awareness
    tasks are answered in Russian unless the ask itself says otherwise
    ("Indicate the case of the nouns in bold. Award 2 marks for each correct
    answer, answers may be given in Irish, English or Russian").
    """
    if unit in READ_IN_ENGLISH:
        return ENGLISH_OR_IRISH
    if re.search(r'may be given in Irish, English or Russian', text or '', re.I):
        return ENGLISH_OR_IRISH
    return RUSSIAN if RUSSIAN_ANSWER.search(text or '') else ENGLISH_OR_IRISH


READ_IN_ENGLISH = {'C1', 'C2', 'CD', 'IR1', 'IR2'}


def language_note(language):
    """The instruction a card carries so a right answer is not marked wrong."""
    if language == RUSSIAN:
        return ('The examination paper prints this question in Irish and in '
                'English and directs that it be answered in RUSSIAN; the '
                'scheme awards no marks for an answer in the wrong language.')
    return ('The examination paper prints this question in Irish and in '
            'English and heads its page "ANSWER THE FOLLOWING QUESTIONS IN '
            'ENGLISH" — it is answered in English or in Irish, not in '
            'Russian.')


STOP = {'the', 'a', 'an', 'of', 'in', 'to', 'and', 'for', 'is', 'are', 'was',
        'were', 'what', 'which', 'how', 'why', 'who', 'when', 'where', 'you',
        'your', 'their', 'they', 'she', 'her', 'his', 'him', 'one', 'two',
        'three', 'four', 'five', 'each', 'any', 'give', 'name', 'state',
        'describe', 'explain', 'mention', 'write', 'details', 'detail',
        'about', 'from', 'that', 'this', 'with', 'does', 'did', 'do', 'has',
        'have', 'had', 'can', 'could', 'would', 'will', 'according'}


def concept_for(text, fallback='ask'):
    """A level-independent slug for what the ask is about, from its own words.

    Shared by a Higher card and its Ordinary sibling where both papers ask the
    same thing, which is what keeps a student's work when they drop level in
    spring. Derived from the ask, never typed.
    """
    words = re.findall(r"[a-z0-9']+", (text or '').lower())
    keep = [w for w in words if w not in STOP and len(w) > 2][:6]
    return '-'.join(keep) or fallback
