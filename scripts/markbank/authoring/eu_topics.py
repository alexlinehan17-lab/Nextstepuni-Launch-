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
        'classic_vocab': 'portuguese-2-0',
        'classic_reading': 'portuguese-2-0',
        'classic_essay': 'portuguese-2-2',
        'classic_essay2': 'portuguese-2-2',
        'reading': 'portuguese-2-3',
        'writing': 'portuguese-2-4',
        'aural': 'portuguese-2-5',
    },
    # Romanian and Dutch are classic-only, and their published taxonomies name
    # the classic paper's parts one for one already: a vocabulary question, a
    # set of comprehension questions, and the written production. Only the
    # third part — an essay on a quotation, set from 2023 — had to be added.
    'romanian': {
        'classic_vocab': 'romanian-0-0',
        'classic_reading': 'romanian-0-1',
        'classic_essay': 'romanian-1-0',
        'classic_essay2': 'romanian-1-1',
    },
    'dutch': {
        'classic_vocab': 'dutch-0-0',
        'classic_reading': 'dutch-0-1',
        'classic_essay': 'dutch-1-0',
        'classic_essay2': 'dutch-1-1',
    },
    # The nine remaining non-curricular EU languages are classic-only and
    # their published taxonomies name the classic paper's parts one for one:
    # a vocabulary question, a set of comprehension questions, the commentary
    # and — added with this wave, as Romanian's and Dutch's third part was —
    # the essay of Part III.
    'hungarian': {
        'classic_vocab': 'hungarian-0-0',
        'classic_reading': 'hungarian-0-1',
        'classic_essay': 'hungarian-1-0',
        'classic_essay2': 'hungarian-1-1',
    },
    'bulgarian': {
        'classic_vocab': 'bulgarian-0-0',
        'classic_reading': 'bulgarian-0-1',
        'classic_essay': 'bulgarian-1-0',
        'classic_essay2': 'bulgarian-1-1',
    },
    'slovakian': {
        'classic_vocab': 'slovakian-0-0',
        'classic_reading': 'slovakian-0-1',
        'classic_essay': 'slovakian-1-0',
        'classic_essay2': 'slovakian-1-1',
    },
    'swedish': {
        'classic_vocab': 'swedish-0-0',
        'classic_reading': 'swedish-0-1',
        'classic_essay': 'swedish-1-0',
        'classic_essay2': 'swedish-1-1',
    },
    'estonian': {
        'classic_vocab': 'estonian-0-0',
        'classic_reading': 'estonian-0-1',
        'classic_essay': 'estonian-1-0',
        'classic_essay2': 'estonian-1-1',
    },
    'finnish': {
        'classic_vocab': 'finnish-0-0',
        'classic_reading': 'finnish-0-1',
        'classic_essay': 'finnish-1-0',
        'classic_essay2': 'finnish-1-1',
    },
    'croatian': {
        'classic_vocab': 'croatian-0-0',
        'classic_reading': 'croatian-0-1',
        'classic_essay': 'croatian-1-0',
        'classic_essay2': 'croatian-1-1',
    },
    'danish': {
        'classic_vocab': 'danish-0-0',
        'classic_reading': 'danish-0-1',
        'classic_essay': 'danish-1-0',
        'classic_essay2': 'danish-1-1',
    },
    'slovenian': {
        'classic_vocab': 'slovenian-0-0',
        'classic_reading': 'slovenian-0-1',
        'classic_essay': 'slovenian-1-0',
        'classic_essay2': 'slovenian-1-1',
    },
}


def topic_for(subject, era, section, letter=None):
    """The task type this ask belongs to, from the era and the section."""
    table = TOPICS[subject]
    if (section or '').startswith('L'):
        return table['aural']
    if era == 'classic':
        if section == 'III':
            return table['classic_essay2']
        if section in ('II',):
            return table['classic_essay']
        return (table['classic_vocab'] if letter else table['classic_reading'])
    return table['writing'] if section == 'B' else table['reading']


LANGUAGE_NAME = {'portuguese': 'Portuguese', 'romanian': 'Romanian',
                 'dutch': 'Dutch',
                 'hungarian': 'Hungarian',
                 'bulgarian': 'Bulgarian',
                 'slovakian': 'Slovakian',
                 'swedish': 'Swedish',
                 'estonian': 'Estonian',
                 'finnish': 'Finnish',
                 'croatian': 'Croatian',
                 'danish': 'Danish',
                 'slovenian': 'Slovenian',
                 }
# A subject whose paper requires EVERY answer in the target language, in
# its own printed rubric — "Toate răspunsurile trebuie scrise în limba
# română", "Alle antwoorden moeten in het Nederlands gegeven worden". The
# language is then a fact about the PAPER and not about the ask, unlike
# Portuguese, which sets one comprehension in two languages and prices the
# difference.
ONE_LANGUAGE = {
    'romanian': 'Toate răspunsurile trebuie scrise în limba română.',
    'dutch': 'Alle antwoorden moeten in het Nederlands gegeven worden.',
    # All nine of the remaining non-curricular EU languages print the same
    # rule on the first page of their own booklet, in their own language.
    'hungarian': 'Válaszoljon érthetően magyarul az I., II. és III. részben feltett kérdésekre!',
    'bulgarian': 'Всички отговори трябва да бъдат написани на български език.',
    'slovakian': 'Všetky odpovede musia byť napísané po slovensky.',
    'swedish': 'Alla svar måste vara skrivna på svenska.',
    'estonian': 'Kõikidele ülesannetele tuleb vastata eesti keeles.',
    'finnish': 'Vastaa kaikkiin kolmeen tehtävään suomeksi.',
    'croatian': 'Svi odgovori moraju biti na hrvatskome jeziku.',
    'danish': 'Alle svar skal skrives på dansk.',
    'slovenian': 'Vsi odgovori morajo biti v slovenščini.',
}
ENGLISH_OR_IRISH = 'English or Irish'

# Function words that belong to one language and not the other. Counted rather
# than pattern-matched on a single word, because a Portuguese ask quotes
# English ("TikTok", "Projeto Tamar") and an English ask quotes Portuguese
# names constantly.
TARGET_WORDS = {
    'romanian': set(),
    'dutch': set(),
    'hungarian': set(),
    'bulgarian': set(),
    'slovakian': set(),
    'swedish': set(),
    'estonian': set(),
    'finnish': set(),
    'croatian': set(),
    'danish': set(),
    'slovenian': set(),

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
    if subject in ONE_LANGUAGE:
        return LANGUAGE_NAME[subject]
    words = {w.lower() for w in WORD.findall(text or '')}
    target = len(words & TARGET_WORDS[subject])
    english = len(words & EN_WORDS)
    if english > target:
        return ENGLISH_OR_IRISH
    return LANGUAGE_NAME[subject]


def language_note(subject, language):
    """The instruction a card carries so a right answer is not half-marked."""
    name = LANGUAGE_NAME[subject]
    if subject in ONE_LANGUAGE:
        return (f'The examination requires every answer in {name.upper()}. '
                f'The paper prints the rule on its own first page: '
                f'"{ONE_LANGUAGE[subject]}"')
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
