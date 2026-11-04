#!/usr/bin/env python3
"""Where a Polish card is filed, and which language its answer must be in.

The syllabus taxonomy already exists — curriculum.ts holds the Polish strands
and deck.ts publishes them — so nothing here invents a topic. Its fourth
strand, "Written Paper — Task Types", names the paper's own two eras one for
one, which is why a card is filed by the examination it was printed in:

    polish-3-0  Reading Comprehension — Text with Open Questions (Część I)
    polish-3-1  Reading — Matching, Multiple-Choice & True/False Tasks
                (Czytanie, New Format)
    polish-3-2  Essay — Wypracowanie (~300 Words)
    polish-3-3  Written Production (Część B Pisanie, New Format)

Only the two reading topics take cards. The essay and the written production
are answered by a content-and-expression grid, and the aural component
(polish-2-1) by a recording no card can carry.

THE ANSWER LANGUAGE IS PART OF THE ASK
--------------------------------------
One Polish reading comprehension is set in TWO languages and priced in both.
2023 Higher Question 1 asks (a) to (d) in Polish and then heads its next page
"Answer questions (e) – (h) in English." The scheme prices the difference on
its own first page:

    "Answers given in the wrong language e.g. answers in Irish/English when
    Polish is required or answers in Polish when Irish/English is required –
    award 50% of the marks."

So the language is read PER ASK, from the language the ask itself is printed
in, and it rides on the card. A card that does not say which language is
wanted halves a right answer.
"""
import re

# The published topic ids, from curriculum.ts. Named here so a change to the
# canonical file is a one-line change, and so nothing in this directory
# invents an id the deck does not hold.
OPEN_QUESTIONS = 'polish-3-0'
NEW_FORMAT_READING = 'polish-3-1'
ESSAY = 'polish-3-2'
WRITTEN_PRODUCTION = 'polish-3-3'
AURAL = 'polish-2-1'


def topic_for(year, section):
    """The task type this ask belongs to, from the era and the section.

    2021 and earlier is the OLD examination: one text, six open questions
    (Część I) and one essay (Część II). 2022 onward is the rebuilt paper:
    Section A Czytanie and Section B Pisanie.
    """
    if year <= 2021:
        return ESSAY if section == 'II' else OPEN_QUESTIONS
    if (section or '').startswith('L'):
        return AURAL
    return WRITTEN_PRODUCTION if section == 'B' else NEW_FORMAT_READING


POLISH = 'Polish'
ENGLISH_OR_IRISH = 'English or Irish'

# Function words that belong to one language and not the other. Counted rather
# than pattern-matched on a single word, because a Polish ask quotes English
# ("Instagram", "gap year") and an English ask quotes Polish names constantly.
PL_WORDS = {
    'jak', 'jakie', 'jaki', 'jaka', 'czy', 'co', 'dlaczego', 'kiedy', 'gdzie',
    'ile', 'kto', 'podaj', 'wymień', 'wypisz', 'uzupełnij', 'wyjaśnij',
    'zaznacz', 'napisz', 'dopasuj', 'określ', 'zacytuj', 'na', 'nie', 'się',
    'jest', 'oraz', 'przy', 'szczegóły', 'informacje', 'przykłady', 'tekstu',
    'akapit', 'akapicie', 'poniższe', 'swoje', 'tabeli', 'tabelę', 'wskaż',
}
EN_WORDS = {
    'what', 'why', 'how', 'when', 'where', 'who', 'which', 'give', 'name',
    'describe', 'explain', 'list', 'indicate', 'tick', 'the', 'and', 'of',
    'about', 'details', 'detail', 'based', 'according', 'did', 'does', 'do',
    'was', 'were', 'is', 'are', 'has', 'have', 'complete', 'underline',
}
WORD = re.compile(r"[^\W\d_]+", re.UNICODE)


def answer_language(text):
    """'Polish' or 'English or Irish' — read from the ask, never from a number."""
    words = {w.lower() for w in WORD.findall(text or '')}
    pl, en = len(words & PL_WORDS), len(words & EN_WORDS)
    if en > pl:
        return ENGLISH_OR_IRISH
    return POLISH


def language_note(language):
    """The instruction a card carries so a right answer is not half-marked."""
    if language == POLISH:
        return ('The examination prints this question in Polish and it is '
                'answered in POLISH. The scheme awards half marks for an '
                'answer given in the wrong language.')
    return ('The examination prints this question in English and it is '
            'answered in English or in Irish, not in Polish. The scheme '
            'awards half marks for an answer given in the wrong language.')


STOP = {'the', 'a', 'an', 'of', 'in', 'to', 'and', 'for', 'is', 'are', 'was',
        'were', 'what', 'which', 'how', 'why', 'who', 'when', 'where', 'you',
        'your', 'their', 'they', 'she', 'her', 'his', 'him', 'one', 'two',
        'three', 'four', 'five', 'each', 'any', 'give', 'name', 'state',
        'describe', 'explain', 'mention', 'write', 'details', 'detail',
        'about', 'from', 'that', 'this', 'with', 'does', 'did', 'do', 'has',
        'have', 'had', 'can', 'could', 'would', 'will', 'according',
        'podaj', 'jakie', 'czego', 'wymien', 'wymień', 'akapit', 'akapity',
        'szczegoly', 'szczegóły', 'jest', 'nie', 'sie', 'się', 'tekstu'}


PL_FOLD = str.maketrans('ąćęłńóśźżĄĆĘŁŃÓŚŹŻ', 'acelnoszzACELNOSZZ')


def concept_for(text, fallback='ask'):
    """A level-independent slug for what the ask is about, from its own words.

    Shared by a Higher card and its Ordinary sibling where both papers ask the
    same thing — which Polish does more than most, because the two levels are
    set on the SAME texts in the same year. Derived from the ask, never typed.
    """
    # ASCII-folded: a concept id is a key, not prose, and it is compared
    # across levels and years. Leaving ł and ż in it makes two spellings of the
    # same concept two concepts the moment one document loses a diacritic.
    folded = (text or '').lower().translate(PL_FOLD)
    words = re.findall(r"[a-z0-9']+", folded)
    keep = [w for w in words if w not in STOP and len(w) > 2][:6]
    return '-'.join(keep) or fallback
