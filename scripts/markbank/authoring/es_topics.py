#!/usr/bin/env python3
"""Where a Spanish card is filed, and which language its answer must be in.

The syllabus taxonomy already exists — curriculum.ts holds the Spanish strands
and curriculumRegistry.ts publishes them as `spanish:current` — so nothing here
invents a topic. It only decides which of the published topics an ask belongs
to, and it does so from what the PAPER prints.

WHICH TEXT IS WHICH
-------------------
The paper names each of its own reading tasks:

    Higher Section A  "1. (a) Prescribed Literature: Gabriel García Márquez:
                      Relato de un náufrago."          -> the set text
                      "Question 1 (b) Journalistic Text."   -> journalism
                      "QUESTION 2 … Answer (a) AND (b)"     -> two short items
    Higher Section B  the article on the loose sheet         -> journalism
    Ordinary Section A  five comprehensions                  -> Comprehension (OL)

All ten Higher sittings set the same prescribed text, and the paper says so on
its own head, so nothing is inferred: the head is read.

THE ANSWER LANGUAGE IS PART OF THE ASK
--------------------------------------
Spanish sets some questions in Spanish and some in English, and the paper
directs which language the answer must be in — "Escribe en ESPAÑOL…", "Explain
in ENGLISH…", "Read about Harry Styles in Madrid and answer the questions in
English." The scheme enforces it on its own section heads: "Questions must be
answered in the language indicated on the examination paper for full marks",
and at Ordinary with the penalty spelled out — "If the entire question is
answered in the incorrect language, mark as per marking scheme and award 50% of
the marks achieved."

A card that does not say which language is wanted marks a right answer wrong,
so every card carries it. It is read where the paper DIRECTS it — on the
question's own head first, then the section's instruction — and only where
neither names a language, from the ask itself and then from the language the
ask is printed in. Reading the ask first gets it backwards: "Why is it not
necessary to understand the lyrics of a song in Spanish?" is answered in
English, under a head that says so.
"""
import re
import unicodedata

# The published topic ids, from curriculum.ts via curriculumRegistry.ts. Named
# here so a change to either is a one-line change, and so nothing in this
# directory invents an id the registry does not hold.
JOURNALISTIC = 'spanish-5-0'
SHORT_TEXTS = 'spanish-5-1'
OL_COMPREHENSION = 'spanish-5-2'
# The four prescribed literature texts the syllabus lists. The paper names the
# one it has set on its own head, and only one of the four has ever been set in
# the 2021-2025 corpus; the others stay here so a later sitting is filed
# correctly rather than under whichever text happens to be first.
LITERATURE = {
    'medall': 'spanish-7-0',        # El medallón perdido (Ana Alcolea)
    'naufrago': 'spanish-7-1',      # Relato de un náufrago (García Márquez)
    'said': 'spanish-7-2',          # La aventura de Saíd
    'gurb': 'spanish-7-3',          # Sin noticias de Gurb
}


def _fold(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', (text or '').lower())
                   if not unicodedata.combining(c))


def topic_for(level, section, head):
    """The published topic id for one printed ask.

    `head` is the paper's own head for the text — the prescribed-literature
    line, the journalistic-text line or the comprehension's introduction.
    """
    if level == 'ol':
        return OL_COMPREHENSION
    if section == 'A1a':
        folded = _fold(head)
        for needle, topic in LITERATURE.items():
            if needle in folded:
                return topic
        # No card is filed under a text the paper did not name: the caller
        # refuses rather than guessing which of the four was set.
        return None
    if section == 'A2':
        return SHORT_TEXTS
    return JOURNALISTIC


# What the paper says the answer must be written in. The tokens are the
# paper's own: it prints the language in CAPITALS where it directs one, and
# spells it out in the running instruction where it does not.
SAYS_SPANISH = re.compile(
    r'\bESPA[ÑN]OL\b|\bin Spanish\b|\ben espa[ñn]ol\b|\bSpanish\b(?=[^.]*\bwrite)', re.I)
SAYS_ENGLISH = re.compile(r'\bENGLISH\b|\bin English\b|\ben ingl[ée]s\b', re.I)

# The language an ask is written in, where it directs neither. Content words
# only: "de", "la" and "the" carry no evidence, and a Spanish ask quoting an
# English proper noun is still a Spanish ask.
SPANISH_WORDS = re.compile(
    r'\b(?:qu[ée]|c[óo]mo|por\s+qu[ée]|cu[áa]l(?:es)?|cu[áa]nt[oa]s?|d[óo]nde'
    r'|escribe|busca|explica|menciona|indica|seg[úu]n|relevez|texto|palabras'
    r'|frases|sentido|siguientes|art[íi]culo|p[áa]rrafo|opini[óo]n|sobre'
    r'|que|los|las|una?|del?|para|con|sus?|est[áa]|dice|hay)\b', re.I)
ENGLISH_WORDS = re.compile(
    r'\b(?:what|how|why|which|who|where|when|write|explain|give|name|mention'
    r'|according|details?|full|text|phrases|following|meaning|context|answer'
    r'|says?|said|does|did|is|are|the|of|about|in|to|and)\b', re.I)


def answer_language(question, stem='', instruction=''):
    """'Spanish' or 'English' — read from where the paper actually directs it.

    The DIRECTION is printed on the question's own head, not inside the ask:
    "Answer the following questions in ENGLISH." governs "Why is it not
    necessary to understand the lyrics of a song in Spanish?", and reading the
    ask first made that card demand its answer in Spanish — the exact way a
    card marks a right answer wrong. So the stem is read first, then the
    section's instruction, and the ask's own words only where neither of those
    names a language (Higher Section A's Q.3 carries its own: "Give three
    details in English from the extract").

    Where nothing names one, the language the ask and its head are PRINTED in
    decides. The section instruction is deliberately left out of that count:
    Higher Section B introduces itself in English — "The questions refer to the
    text on the loose sheet provided separately" — above a question set in
    Spanish and answered in Spanish.
    """
    for text in (stem, instruction, question):
        if not text:
            continue
        es, en = SAYS_SPANISH.search(text), SAYS_ENGLISH.search(text)
        if es and en:
            # Both named in one instruction — "Explain in ENGLISH the meaning
            # of the following Spanish phrases" — so the FIRST is the direction
            # and the second names the text being quoted.
            return 'Spanish' if es.start() < en.start() else 'English'
        if es:
            return 'Spanish'
        if en:
            return 'English'
    joined = f'{question} {stem}'
    return ('Spanish' if len(SPANISH_WORDS.findall(joined))
            >= len(ENGLISH_WORDS.findall(joined)) else 'English')


def language_note(language, rule):
    """The instruction a card carries so a right answer is not marked wrong.

    The scheme's own sentence is quoted rather than paraphrased, because the
    two levels state different penalties and the Ordinary one is specific: half
    marks for a whole question in the wrong language, and none at all for a
    sub-part.
    """
    said = (f' The marking scheme states: “{rule}”' if rule else '')
    return (f'The examination paper directs that this question be answered in '
            f'{language}.{said}')


STOP = {'the', 'a', 'an', 'of', 'in', 'to', 'and', 'for', 'is', 'are', 'was',
        'what', 'which', 'how', 'why', 'you', 'your', 'their', 'they', 'one',
        'two', 'three', 'each', 'any', 'give', 'name', 'state', 'identify',
        'mention', 'write', 'que', 'qui', 'quel', 'est', 'los', 'las', 'una',
        'del', 'para', 'con', 'sus', 'esta', 'este', 'sobre', 'texto', 'para',
        'section', 'roinn', 'escribe', 'busca', 'explica', 'seg', 'por',
        'para', 'full', 'details', 'detail', 'about', 'says', 'said',
        # The paper's own pointer into the text — "(lines 1-10)", "(para 3)",
        # "(párrafo 5)" — addresses the passage, not the concept.
        'lines', 'line', 'para', 'parrafo', 'paragraph'}


def concept_for(text, fallback='ask'):
    """A level-independent slug for what the ask is about, from its own words.

    Shared by a Higher card and its Ordinary sibling where both papers ask the
    same thing, which is what keeps a student's work when they drop level in
    spring. Derived from the ask, never typed.
    """
    words = re.findall(r"[a-z0-9']+", _fold(text))
    keep = [w for w in words if w not in STOP and len(w) > 2][:6]
    return '-'.join(keep) or fallback
