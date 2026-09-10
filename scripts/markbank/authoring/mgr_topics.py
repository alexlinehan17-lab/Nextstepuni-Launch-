#!/usr/bin/env python3
"""Modern Greek — where a card is filed, and what language its answer is in.

The taxonomy already exists in curriculum.ts and names this paper's own two
halves, one for one:

    modern-greek-0-0  Vocabulary & expressions in context
    modern-greek-0-1  Comprehension & discussion of the set text
    modern-greek-1-0  Commentary / essay on the text theme

Only the two reading subtopics take cards. The commentary (ΟΜΑΔΑ 2η
ΣΧΟΛΙΑΣΜΟΣ) and the essay (ΟΜΑΔΑ 3η ΕΚΘΕΣΗ ΔΟΚΙΜΙΟ) are written production:
the scheme answers each with one indicative composition of its own and prices
nothing inside it, which is the same refusal the other nine languages make of
their writing tasks.

THE ANSWER LANGUAGE IS PART OF THE ASK — and here it is a subject constant,
which is worth saying because in a curricular language it is not. German
answers one comprehension in two languages and prices the difference; Modern
Greek prints one rubric over the whole paper and it never changes across the
sixteen sittings on disk:

    "Να απαντήσετε και στις 3 ομάδες ερωτήσεων.
     Οι απαντήσεις να δοθούν στα νέα Ελληνικά."

Answer all three groups of questions; the answers are to be given in MODERN
Greek. It rides on every card, read from the paper rather than assumed — a
sitting that stopped printing it would be caught by `answer_language`
returning nothing.
"""
import re

VOCABULARY = 'modern-greek-0-0'
COMPREHENSION = 'modern-greek-0-1'
WRITTEN_PRODUCTION = 'modern-greek-1-0'

GREEK_NAME = 'Modern Greek'
# The rubric that states it, in the two spellings the corpus prints:
# "στα νέα Ελληνικά" and 2011's "στα Νεοελληνικά".
RUBRIC = re.compile(r'απαντήσεις\s+να\s+δοθο[υύ]ν\s+στα\s+'
                    r'(?:ν[έε]α\s+Ελληνικ[άα]|Νεοελληνικ[άα])', re.I)


def answer_language(P):
    """The language the paper says its answers must be in, or None.

    Read from the paper's own printed rubric. None means the sitting did not
    print one, which is a fact about that paper and not a default to fill in.
    """
    return GREEK_NAME if RUBRIC.search(P.answer_language or '') else None


def language_note(language):
    return (f'The paper states that answers are to be given in {language}: '
            '"Οι απαντήσεις να δοθούν στα νέα Ελληνικά."'
            ) if language else ''


def topic_for(ask):
    """The subtopic this printed ask belongs to, from the group it sits in."""
    if ask.kind != 'reading':
        return WRITTEN_PRODUCTION
    return VOCABULARY if ask.items else COMPREHENSION


# A stable identity for the thing an ask is ABOUT. Modern Greek sets a fresh
# article every year, so two sittings rarely share a concept — but the vocabulary
# question is the same TASK every year and its cards should not all collapse
# into one concept either, so the words themselves make the key.
STOP = {'και', 'του', 'της', 'των', 'στο', 'στη', 'στην', 'στα', 'στις',
        'τους', 'την', 'τον', 'τα', 'το', 'η', 'ο', 'οι', 'που', 'με', 'σε',
        'για', 'από', 'ως', 'είναι', 'ήταν', 'να', 'δεν', 'θα', 'σας', 'σου',
        'μας', 'κατά', 'κάθε', 'ένα', 'μια', 'ποια', 'ποιο', 'ποιοι', 'πως',
        'πώς', 'γιατί', 'τι', 'αλλά', 'όπως', 'κείμενο', 'κειμένου',
        'σύμφωνα', 'διαβάσατε', 'άποψη', 'εξηγήστε', 'αναφέρετε', 'δικά',
        'λόγια', 'σημασία', 'παρακάτω', 'φράσεων', 'γραμμένες', 'έντονα',
        'γράμματα', 'δοσμένο', 'βασισμένοι', 'δική', 'επίσης'}


def concept_for(text):
    words = [w for w in re.findall(r'[Ͱ-Ͽ]{3,}', (text or '').lower())
             if w not in STOP]
    return 'mgr-' + '-'.join(sorted(set(words))[:3]) if words else 'mgr-general'
