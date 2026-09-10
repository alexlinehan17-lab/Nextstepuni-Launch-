#!/usr/bin/env python3
"""Where a non-curricular EU language card is filed, and in which language its
answer must be written.

The syllabus taxonomy already exists — curriculum.ts holds each subject's
strands and deck.ts publishes them — so nothing here invents a topic. The
strand that matters is the paper's own task types, and a card is filed by the
task it was printed as:

    portuguese-2-0  Reading Comprehension — one text, open questions (Parte I)
    portuguese-2-2  Commentary (~300 words, the classic paper's second part)
    portuguese-2-3  Reading Comprehension — two texts (Parte A, from 2022)
    portuguese-2-4  Written Production (Parte B, from 2022)
    portuguese-2-5  Listening Comprehension Test (its own booklet, from 2022)

Only the two reading topics take cards. The written production is answered by
a content-and-language band grid, and the listening asks by a recording no
card can carry.

THE ANSWER LANGUAGE IS PART OF THE ASK
--------------------------------------
One reading comprehension is set in TWO languages and priced in both. 2024
Higher asks Question 1 (a) to (f) in Portuguese and then heads its next page
"Answer questions (g) – (i) in English according to the text." The scheme
prices the difference on its own first page:

    "Answers given in the wrong language e.g. answers in Irish/English when
    Portuguese is required or answers in Portuguese when Irish/English is
    required — 50% of the Marks."

So the language is read PER ASK, from the language the ask itself is printed
in, and it rides on the card. A card that does not say which language is
wanted halves a right answer.
"""
import re

# The published topic ids, from curriculum.ts. Named here so a change to the
# canonical file is a one-line change, and so nothing in this directory
# invents an id the deck does not hold.
TOPICS = {
    'portuguese': {
        'classic_reading': 'portuguese-2-0',
        'classic_essay': 'portuguese-2-2',
        'reading': 'portuguese-2-3',
        'writing': 'portuguese-2-4',
        'aural': 'portuguese-2-5',
    },
}


def topic_for(subject, era, section):
    """The task type this ask belongs to, from the era and the section."""
    table = TOPICS[subject]
    if (section or '').startswith('L'):
        return table['aural']
    if era == 'classic':
        return (table['classic_reading'] if section == 'I'
                else table['classic_essay'])
    return table['writing'] if section == 'B' else table['reading']


LANGUAGE_NAME = {'portuguese': 'Portuguese'}
ENGLISH_OR_IRISH = 'English or Irish'

# Function words that belong to one language and not the other. Counted rather
# than pattern-matched on a single word, because a Portuguese ask quotes
# English ("TikTok", "Projeto Tamar") and an English ask quotes Portuguese
# names constantly.
TARGET_WORDS = {
    'portuguese': {
        'que', 'qual', 'quais', 'quem', 'onde', 'quando', 'porque', 'por',
        'razão', 'razões', 'como', 'descreva', 'indique', 'explique', 'dê',
        'detalhes', 'encontre', 'complete', 'preencha', 'escreva', 'diga',
        'assinale', 'numere', 'texto', 'parágrafo', 'parágrafos', 'suas',
        'seus', 'sobre', 'segundo', 'acordo', 'palavras', 'expressões',
        'significado', 'não', 'uma', 'para', 'com', 'dos', 'das', 'aconteceu',
        'era', 'está', 'são', 'foi', 'projeto', 'autor', 'narrador',
    },
}
EN_WORDS = {
    'what', 'why', 'how', 'when', 'where', 'who', 'which', 'give', 'name',
    'describe', 'explain', 'list', 'indicate', 'tick', 'the', 'and', 'of',
    'about', 'details', 'detail', 'based', 'according', 'did', 'does', 'do',
    'was', 'were', 'is', 'are', 'has', 'have', 'complete', 'underline',
    'number', 'fill', 'answer', 'happened', 'author', 'text', 'paragraph',
}
WORD = re.compile(r"[^\W\d_]+", re.UNICODE)


def answer_language(subject, text):
    """The subject's own language, or English/Irish — read from the ask."""
    words = {w.lower() for w in WORD.findall(text or '')}
    target = len(words & TARGET_WORDS[subject])
    english = len(words & EN_WORDS)
    if english > target:
        return ENGLISH_OR_IRISH
    return LANGUAGE_NAME[subject]


def language_note(subject, language):
    """The instruction a card carries so a right answer is not half-marked."""
    name = LANGUAGE_NAME[subject]
    if language == name:
        return (f'The examination prints this question in {name} and it is '
                f'answered in {name.upper()}. The scheme awards half marks '
                f'for an answer given in the wrong language.')
    return (f'The examination prints this question in English and it is '
            f'answered in English or in Irish, not in {name}. The scheme '
            f'awards half marks for an answer given in the wrong language.')


STOP = {'the', 'a', 'an', 'of', 'in', 'to', 'and', 'for', 'is', 'are', 'was',
        'were', 'what', 'which', 'how', 'why', 'who', 'when', 'where', 'you',
        'your', 'their', 'they', 'she', 'her', 'his', 'him', 'one', 'two',
        'three', 'four', 'five', 'each', 'any', 'give', 'name', 'state',
        'describe', 'explain', 'mention', 'write', 'details', 'detail',
        'about', 'from', 'that', 'this', 'with', 'does', 'did', 'do', 'has',
        'have', 'had', 'can', 'could', 'would', 'will', 'according',
        'que', 'qual', 'quais', 'como', 'para', 'com', 'dos', 'das', 'uma',
        'por', 'razao', 'razoes', 'texto', 'paragrafo', 'paragrafos', 'sobre',
        'segundo', 'acordo', 'nao', 'sao', 'esta', 'este', 'seus', 'suas',
        'detalhes', 'indique', 'descreva', 'explique', 'encontre'}

FOLD = str.maketrans('áàâãäéèêëíìîïóòôõöúùûüçñýÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇÑ',
                     'aaaaaeeeeiiiiooooouuuucnyAAAAAEEEEIIIIOOOOOUUUUCN')


def concept_for(text, fallback='ask'):
    """A level-independent slug for what the ask is about, from its own words.

    Shared by a Higher card and its Ordinary sibling where both papers ask the
    same thing. Derived from the ask, never typed — and ASCII-folded, because
    a concept id is a key compared across levels and years, and leaving ã in
    it makes two spellings of the same concept two concepts.
    """
    folded = (text or '').lower().translate(FOLD)
    words = re.findall(r"[a-z0-9']+", folded)
    keep = [w for w in words if w not in STOP and len(w) > 2][:6]
    return '-'.join(keep) or fallback
