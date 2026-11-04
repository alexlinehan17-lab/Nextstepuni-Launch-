#!/usr/bin/env python3
"""Where a Japanese card is filed, and which language its answer must be in.

The syllabus taxonomy already exists — curriculum.ts holds the Japanese
strands and curriculumRegistry.ts publishes them — so nothing here invents a
topic. It only says which published task type an ask belongs to, and it reads
that from the part the PAPER prints it in, because this paper's parts ARE its
task types: a kanji section, a grammar section, a translation, a comprehension.

THE ANSWER LANGUAGE IS PART OF THE ASK, AND IT CHANGES INSIDE ONE QUESTION
-------------------------------------------------------------------------
問題2 at Higher sets its first two items in Irish and English and heads them
"Freagair i nGaeilge / Answer in English", then sets its third in Japanese and
heads it "Freagair i Seapáinis / Answer in Japanese" — one comprehension,
two answer languages, and the scheme prices the difference: "Half marks if
answered in Japanese", "(1/2 marks if answered in Japanese)". A card that does
not say which language is wanted marks a right answer wrong, so every card
carries it, read from the language the question is actually printed in.

The kanji sections are the sharpest case, because BOTH directions are set in
one part: "Write the meaning of any FIVE of the following Kanji in English"
and, underneath it, "Write the reading of any FIVE of the following Kanji in
Hiragana". Same kanji, same part, opposite answers.
"""
import re

# Published topic ids, from curriculum.ts via curriculumRegistry.ts. Named here
# so a change to either is a one-line change, and so nothing in this directory
# invents an id the registry does not hold.
EVERYDAY = 'japanese-5-0'      # menus, guides, websites
LETTERS_BLOGS = 'japanese-5-1'  # letters, emails, blogs, diaries
ARTICLES = 'japanese-5-2'      # articles and interviews
TRANSLATION = 'japanese-5-3'
KANJI = 'japanese-5-4'
GRAMMAR = 'japanese-5-5'
CULTURE = 'japanese-5-6'
PERSONAL_WRITING = 'japanese-5-7'

KANJI_HEAD = re.compile(r'\bKanji\b', re.I)
GRAMMAR_HEAD = re.compile(r'GRAMADACH|GRAMMAR|p[áa]irteagal|particle'
                          r'|fhoirm|form of each verb|plain form|negative',
                          re.I)
TRANSLATE_HEAD = re.compile(r'Aistrigh|Translate', re.I)
CULTURE_HEAD = re.compile(r'chult[úu]r|shocha[íi]|culture and society', re.I)


def topic_for(question, rubric):
    """The published topic id for one ask, from the part's own instruction.

    The instruction is what the SEC printed above the ask, so a part that says
    "Write the meaning of any FIVE of the following Kanji" is a kanji task
    whatever question it sits under — which matters, because 問題2 and 問題3
    both set one and the syllabus files them in the same place.
    """
    text = rubric or ''
    if KANJI_HEAD.search(text):
        return KANJI
    if GRAMMAR_HEAD.search(text):
        return GRAMMAR
    if TRANSLATE_HEAD.search(text):
        return TRANSLATION
    if CULTURE_HEAD.search(text):
        return CULTURE
    # The three reading comprehensions, by what the SEC sets each year: 問題1
    # is a web page or a printed guide, 問題2 an article or interview, 問題3 a
    # letter, e-mail, blog or diary. Stable across all ten sittings on disk.
    return {1: EVERYDAY, 2: ARTICLES, 3: LETTERS_BLOGS}.get(question, EVERYDAY)


JAPANESE = 'Japanese'
ENGLISH_OR_IRISH = 'English or Irish'
HIRAGANA = 'hiragana'

# Kana and kanji. A question set in Japanese is written in them and a question
# set in Irish or English is not, so the script itself answers which language
# the SEC is asking in — no word list needed, unlike the Latin-script
# languages where French had to score wording.
JA_SCRIPT = re.compile(r'[぀-ヿ㐀-鿿]')
# The instruction the SEC prints above an ask it wants answered in Japanese.
IN_JAPANESE = re.compile(r'i\s*Seap[áa]inis|in\s+Japanese', re.I)
IN_HIRAGANA = re.compile(r'in\s+Hiragana|in\s+Hiragana', re.I)


def answer_language(text, rubric=''):
    """'Japanese', 'hiragana' or 'English or Irish' — from what is printed.

    Read from the RUBRIC first, because the rubric is where the SEC states it,
    and from the script of the question only where the rubric is silent. The
    two agree everywhere they are both present in the corpus; the rubric wins
    because the kanji sections set their questions in Japanese and want them
    answered in English.
    """
    if IN_HIRAGANA.search(rubric or ''):
        return HIRAGANA
    if re.search(r'i\s*nGaeilge|in\s+English', rubric or '', re.I):
        return ENGLISH_OR_IRISH
    if IN_JAPANESE.search(rubric or ''):
        return JAPANESE
    return JAPANESE if JA_SCRIPT.search(text or '') else ENGLISH_OR_IRISH


def language_note(language, level):
    """The instruction a card carries so a right answer is not marked wrong.

    Stated, never QUOTED. An earlier draft put "Freagair i Seapáinis / Answer
    in Japanese" on every Japanese-answered card, including the particle and
    verb-form tasks, whose pages print no such heading — a quotation attributed
    to a paper that never printed it. What is quoted here is the half-marks
    penalty, which all ten schemes on disk do print, on the head of every
    component: "(1/2 marks if answered in Japanese, romaji or Japanese
    script)" at Ordinary, "Half marks if answered in Japanese" at Higher.
    """
    half = ('All ten schemes print a half-marks penalty for answering in the '
            'wrong language.')
    if language == JAPANESE:
        return ('Answer in Japanese: the examination paper sets this ask in '
                f'Japanese. {half}')
    if language == HIRAGANA:
        return ('Write the READING of the printed kanji, in hiragana, as the '
                'examination paper directs.')
    return ('Answer in Irish or English, not in Japanese: the examination '
            f'paper sets this ask in both of those. {half}')


# The bracket convention every card carrying Japanese discloses. The SEC prints
# furigana as a second layer of type above the kanji it glosses, which no
# single line of text can hold; ja_text.py folds each run in after the
# character it was centred over.
FURIGANA_NOTE = (
    'Where the examination paper prints a kana reading above a kanji '
    '(furigana), this card shows it in brackets after the kanji it belongs '
    'to — 秋葉原（あきはばら） — because a card is one line of text and the '
    'paper sets it on two.')

STOP = {'the', 'a', 'an', 'of', 'in', 'to', 'and', 'for', 'is', 'are', 'was',
        'what', 'which', 'how', 'why', 'you', 'your', 'their', 'they', 'one',
        'two', 'three', 'each', 'any', 'give', 'name', 'state', 'identify',
        'mention', 'write', 'list', 'does', 'did', 'do', 'from', 'about',
        'with', 'that', 'this', 'these', 'those', 'can', 'will', 'would',
        'section', 'details', 'detail', 'answer', 'following', 'cad', 'cen',
        'conas', 'tabhair', 'freagair', 'ainmnigh', 'luaigh', 'nGaeilge'}


def concept_for(text, fallback='ask'):
    """A level-independent slug for what the ask is about, from its own words.

    Shared by a Higher card and its Ordinary sibling where both papers ask the
    same thing, which is what keeps a student's work when they drop level in
    spring. Derived from the ask, never typed — and where the ask is set in
    Japanese there are no Latin words to derive it from, so the caller passes
    a fallback built from the address.
    """
    words = re.findall(r"[a-z0-9']+", (text or '').lower())
    keep = [w for w in words if w not in STOP and len(w) > 2][:6]
    return '-'.join(keep) or fallback
