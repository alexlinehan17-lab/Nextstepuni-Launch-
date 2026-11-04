#!/usr/bin/env python3
"""Where a Lithuanian card is filed, and which language its answer must be in.

The syllabus taxonomy already exists — curriculum.ts holds the Lithuanian
strands and deck.ts publishes them — so nothing here invents a topic. Its third
strand, "Written Paper — Task Types", names the paper's own three eras one for
one, which is why a card is filed by the examination it was printed in:

    lithuanian-2-0  Reading Comprehension — Article with Open Questions
                    (I Dalis)
    lithuanian-2-1  Reading Comprehension — Narrative & Informational Texts
                    (Užduotys, New Format)
    lithuanian-2-2  Guided Commentary on the Text (II Dalis)
    lithuanian-2-3  Discursive Essay (Samprotavimo rašinys)
    lithuanian-2-4  Written Production (Section B, New Format)

Only the two reading topics take cards. The commentary and the essay are
answered by a model paragraph and a description of a good essay, the written
production by a marking grid, and the listening component (lithuanian-0-0) by a
recording no card can carry.

THE ANSWER LANGUAGE IS PART OF THE ASK
--------------------------------------
From 2022 one Lithuanian reading comprehension is set in TWO languages and
priced in both. 2024 Higher asks (a) to (i) in Lithuanian and then heads its
next ask "Answer question (j) in English." The scheme halves the marks for an
answer in the wrong one, on its own third page:

    "Answers given in the wrong language e.g. answers in Irish/English when
    Lithuanian is required or answers in Lithuanian when Irish/English is
    required – award 50% of the marks."

So the language is read PER ASK, from the language the ask itself is printed
in, and it rides on the card. A card that does not say which language is
wanted halves a right answer.

The rule is printed in the ten schemes from 2022 onward and in none of the
twelve before them, which is not an omission: the old examination is set
entirely in Lithuanian and asks nothing in English, so there is no wrong
language to award half marks for. The note a card carries says only what its
own sitting's scheme says.
"""
import re

# The published topic ids, from curriculum.ts. Named here so a change to the
# canonical file is a one-line change, and so nothing in this directory invents
# an id the deck does not hold.
TOPICS = {
    'lithuanian': {
        'open': 'lithuanian-2-0', 'new_reading': 'lithuanian-2-1',
        'commentary': 'lithuanian-2-2', 'essay': 'lithuanian-2-3',
        'production': 'lithuanian-2-4', 'aural': 'lithuanian-0-0',
    },
    # Latvian and Czech never left the old examination, so their taxonomy has
    # no "new format" topic at all — two subtopics of reading and one of
    # written production, which is exactly what their papers print.
    'latvian': {
        'open': 'latvian-0-1', 'vocab': 'latvian-0-0',
        'new_reading': 'latvian-0-1', 'commentary': 'latvian-1-0',
        'essay': 'latvian-1-0', 'production': 'latvian-1-0',
        'aural': 'latvian-0-1',
    },
    'czech': {
        'open': 'czech-0-1', 'vocab': 'czech-0-0',
        'new_reading': 'czech-0-1', 'commentary': 'czech-1-0',
        'essay': 'czech-1-0', 'production': 'czech-1-0',
        'aural': 'czech-0-1',
    },
}

# The old examination's Question 1 is a VOCABULARY task and nothing else — five
# expressions from the text, one taškas each, glossed in the scheme. Latvian
# and Czech name that its own subtopic; Lithuanian does not, and files it with
# the rest of I Dalis.
VOCAB_QUESTION = 1


# The examination was rebuilt in 2022 for LITHUANIAN and for nothing else.
# Latvian and Czech print the old paper in every year of the corpus, so the
# year says nothing about which taxonomy an ask belongs to — filed by year,
# ten of their thirty-four sittings were tagged to a "new format" topic their
# examination has never had.
REBUILT_IN_2022 = {'lithuanian'}


def topic_for(subject, year, section, q=None):
    """The task type this ask belongs to, from the era and the printed part."""
    ids = TOPICS[subject]
    if (section or '').startswith('L'):
        return ids['aural']
    if year >= 2022 and subject in REBUILT_IN_2022:
        return ids['production'] if section == 'B' else ids['new_reading']
    if section == 'I':
        if q == VOCAB_QUESTION and 'vocab' in ids:
            return ids['vocab']
        return ids['open']
    if section == 'III':
        return ids['essay']
    # II DALIS is the commentary in the three-part paper and the essay in the
    # two-part 2021 one, which drops the commentary altogether.
    return ids['essay'] if year == 2021 else ids['commentary']


LANGUAGE = {'lithuanian': 'Lithuanian', 'latvian': 'Latvian',
            'czech': 'Czech'}
ENGLISH_OR_IRISH = 'English or Irish'

# Function words that belong to one language and not the other. Counted rather
# than pattern-matched on a single word, because a Lithuanian ask quotes
# English ("Instagram", "zero waste") and an English ask quotes Lithuanian
# names constantly.
LT_WORDS = {
    'kodėl', 'kokia', 'kokie', 'kokias', 'kokių', 'kokius', 'kas', 'kur',
    'kiek', 'ką', 'kaip', 'kada', 'kelintą', 'kelerių', 'kuris', 'kuri',
    'parašykite', 'raskite', 'paaiškinkite', 'išvardinkite', 'aptarkite',
    'pažymėkite', 'remdamiesi', 'atsakykite', 'nurašykite', 'įrašykite',
    'sudarykite', 'suderinkite', 'sunumeruokite', 'išrinkite', 'dalis',
    'tekste', 'tekstu', 'teksto', 'detales', 'detalę', 'apie', 'anot',
    'nuomone', 'yra', 'jūsų', 'savo',
}
LV_WORDS = {
    'kāpēc', 'kas', 'kur', 'cik', 'kā', 'kad', 'kāda', 'kādi', 'kādas',
    'uzrakstiet', 'atrodiet', 'paskaidrojiet', 'nosauciet', 'izskaidrojiet',
    'balstoties', 'tekstā', 'teksta', 'savu', 'jūsu', 'ir', 'pēc',
}
CS_WORDS = {
    'proč', 'kdo', 'kde', 'kolik', 'jak', 'kdy', 'jaký', 'jaká', 'jaké',
    'napište', 'najděte', 'vysvětlete', 'uveďte', 'popište', 'podle',
    'textu', 'textu', 'text', 'svůj', 'vaše', 'je', 'na',
}
NATIVE_WORDS = {'lithuanian': LT_WORDS, 'latvian': LV_WORDS, 'czech': CS_WORDS}
EN_WORDS = {
    'what', 'why', 'how', 'when', 'where', 'who', 'which', 'give', 'name',
    'describe', 'explain', 'list', 'indicate', 'tick', 'the', 'and', 'of',
    'about', 'details', 'detail', 'based', 'according', 'did', 'does', 'do',
    'was', 'were', 'is', 'are', 'has', 'have', 'complete', 'underline',
    'discuss', 'refer', 'support', 'answer', 'agree', 'benefits', 'words',
    'total', 'text', 'your',
}
WORD = re.compile(r"[^\W\d_]+", re.UNICODE)


def answer_language(subject, text):
    """The subject's own language or English/Irish — read from the ask."""
    words = {w.lower() for w in WORD.findall(text or '')}
    native = len(words & NATIVE_WORDS[subject])
    english = len(words & EN_WORDS)
    if english > native:
        return ENGLISH_OR_IRISH
    return LANGUAGE[subject]


def language_note(subject, language, year):
    """The instruction a card carries so a right answer is not half-marked.

    The half-marks sentence is quoted only for the sittings whose scheme prints
    it — 2022 onward. Before that the paper is set wholly in the subject's own
    language and its scheme states no language rule, so a card that claimed one
    would be putting a penalty in the SEC's mouth.
    """
    own = LANGUAGE[subject]
    # The half-marks rule is quoted only where the SEC prints it: the ten
    # Lithuanian schemes from 2022 on, and nowhere else. Latvian and Czech
    # print no language rule at all — their paper is set wholly in the
    # subject's own language and asks nothing in English — and a card that
    # claimed one would be putting a penalty in the SEC's mouth. Checked by
    # grep over the corpus: "wrong language" appears in ten of the fifty-six
    # schemes these three subjects publish, all of them Lithuanian.
    penalty = (' The scheme awards half marks for an answer given in the '
               'wrong language.'
               if year >= 2022 and subject in REBUILT_IN_2022 else '')
    if language == own:
        return (f'The examination prints this question in {own} and it is '
                f'answered in {own.upper()}.{penalty}')
    return (f'The examination prints this question in English and it is '
            f'answered in English or in Irish, not in {own}.{penalty}')


STOP = {'the', 'a', 'an', 'of', 'in', 'to', 'and', 'for', 'is', 'are', 'was',
        'were', 'what', 'which', 'how', 'why', 'who', 'when', 'where', 'you',
        'your', 'their', 'they', 'she', 'her', 'his', 'him', 'one', 'two',
        'three', 'four', 'five', 'each', 'any', 'give', 'name', 'state',
        'describe', 'explain', 'mention', 'write', 'details', 'detail',
        'about', 'from', 'that', 'this', 'with', 'does', 'did', 'do', 'has',
        'have', 'had', 'can', 'could', 'would', 'will', 'according',
        'parasykite', 'raskite', 'kokie', 'kokia', 'kodel', 'dalis', 'tekste',
        'tekstu', 'teksto', 'detales', 'detale', 'anot', 'apie', 'yra',
        'pazymekite', 'remdamiesi', 'atsakykite'}

FOLD = str.maketrans('ąčęėįšųūžĄČĘĖĮŠŲŪŽāēģīķļņĀĒĢĪĶĻŅáčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ',
                     'aceeisuuzACEEISUUZaegiklnAEGIKLNacdeeinorstuuyzACDEEINORSTUUYZ')


def concept_for(text, fallback='ask'):
    """A level-independent slug for what the ask is about, from its own words.

    Shared by a Higher card and its Ordinary sibling where both papers ask the
    same thing — which these languages do more than most, because the two
    levels are set in the same year on related texts. Derived from the ask,
    never typed, and ASCII-folded because a concept id is a key compared across
    levels and years, not prose.
    """
    folded = (text or '').lower().translate(FOLD)
    words = re.findall(r"[a-z0-9']+", folded)
    keep = [w for w in words if w not in STOP and len(w) > 2][:6]
    return '-'.join(keep) or fallback
