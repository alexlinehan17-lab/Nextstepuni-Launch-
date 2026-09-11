#!/usr/bin/env python3
"""Mandarin Chinese — where a card is filed, and what language its answer is in.

The taxonomy already exists in curriculum.ts and its fourth strand names this
paper's own task types, one for one:

    mandarin-chinese-3-0  Reading — Notices, Signs, Timetables & Maps
    mandarin-chinese-3-1  Reading — Nursery Rhymes & Poems
    mandarin-chinese-3-2  Reading — Descriptive & Narrative Passages
    mandarin-chinese-3-3  Reading — Emails, Messages, Diaries & Social Media
    mandarin-chinese-3-4  Reading — Word–Picture Matching (OL)
    mandarin-chinese-3-5  Written Production (Section B)

The task type is read from the paper's OWN rubric above the passage — "Read the
following weather report", "Read the following text about two animals", "Read
the following email from Linda", "Match the following words and pictures" —
never guessed from the answers.

THE ANSWER LANGUAGE IS PART OF THE ASK, and in this subject it is not a
constant. The SEC states it per ASK, in the ask's own printed words: most
questions say nothing and are answered in English, and the ones that are not
say so on the line — "Answer in Chinese", "Answer this question in Chinese",
"Answer the questions in English". The paper's instruction page states the
form the Chinese must take, and that IS a constant across all ten sittings:

    "Where answers are required in Mandarin Chinese, simplified Chinese
     characters must be used."

so it rides on every card whose answer is in Chinese. Pinyin is not an
acceptable substitute and the SEC says so in its own Writing band grid, which
deducts for "substitutes of characters using other languages or means (e.g.,
pinyin, traditional characters, first language, other phonetic symbols …)".
"""
import re

NOTICES = 'mandarin-chinese-3-0'
POEMS = 'mandarin-chinese-3-1'
PASSAGES = 'mandarin-chinese-3-2'
CORRESPONDENCE = 'mandarin-chinese-3-3'
MATCHING = 'mandarin-chinese-3-4'
WRITTEN_PRODUCTION = 'mandarin-chinese-3-5'

# The SEC's own words for what a candidate is reading, in the order they are
# tested: the first that matches the question's printed rubric wins.
TASK = (
    (MATCHING, r'match the following|filling in the grid|match the words'),
    (POEMS, r'nursery rhyme|\bpoem\b|\brhyme\b|children’s song'),
    (CORRESPONDENCE, r'\bemail\b|\bletter\b|\bmessage\b|\bdiary\b|\bnotice\b'
                     r'|\bnote\b|\binvitation\b|social media|\bblog\b|\bpost\b'
                     r'|\bnewsletter\b|\bWeChat\b'),
    (NOTICES, r'\bposter\b|\bflyer\b|\btimetable\b|\bmap\b|\bsign\b'
              r'|\bweather report\b|\badvertisement\b|\bschedule\b|\bmenu\b'
              r'|\bticket\b|\bbrochure\b|\bleaflet\b|\bslide\b|\bform\b'
              r'|\bboard\b|\bplan\b'),
)


def topic_for(ask, stimulus=''):
    """The subtopic this printed ask belongs to, from the paper's own rubric."""
    if ask.kind != 'reading':
        return WRITTEN_PRODUCTION
    text = f'{stimulus} {ask.stem} {ask.text}'
    for topic, pattern in TASK:
        if re.search(pattern, text, re.I):
            return topic
    # A run of prose with no named genre is a descriptive or narrative passage,
    # which is what the SEC sets when it names nothing: "Read the following
    # text about two animals."
    return PASSAGES


CHINESE_ASK = re.compile(r'answer\s+(?:this\s+question\s+|the\s+question\s+)?'
                         r'in\s+(?:Mandarin\s+)?Chinese', re.I)
ENGLISH_ASK = re.compile(r'answer\s+(?:this\s+question\s+|the\s+questions?\s+)?'
                         r'in\s+English', re.I)

SIMPLIFIED = ('The paper states on its instruction page: "Where answers are '
              'required in Mandarin Chinese, simplified Chinese characters '
              'must be used."')


def answer_language(ask, stimulus=''):
    """'Chinese' or 'English', read from the ask's own printed words.

    Per ASK and never per subject: 2024 Higher answers Question 3(a), (b), (d)
    and (e) in English and Question 3(c) — "Chinese people gave a nickname to
    Jan-Ove Waldner. What is it? Answer in Chinese." — in Chinese, inside one
    comprehension. The ask's own line is read first and the question's rubric
    second, because the rubric states the default and the ask states the
    exception.
    """
    own = f'{ask.text}'
    if CHINESE_ASK.search(own):
        return 'Chinese'
    if ENGLISH_ASK.search(own):
        return 'English'
    head = f'{ask.stem} {stimulus}'
    if CHINESE_ASK.search(head):
        return 'Chinese'
    if ENGLISH_ASK.search(head):
        return 'English'
    return None


def language_note(language):
    if language == 'Chinese':
        return ('The examination requires this answer in Mandarin Chinese. '
                + SIMPLIFIED)
    if language == 'English':
        return 'The examination requires this answer in English.'
    return ''


# A stable identity for the thing an ask is ABOUT. The SEC sets fresh material
# every year, so two sittings rarely share a concept — the words of the ask
# itself make the key, with the question's own furniture removed.
STOP = {'the', 'and', 'for', 'are', 'was', 'were', 'this', 'that', 'with',
        'from', 'what', 'which', 'name', 'give', 'list', 'answer', 'answers',
        'question', 'questions', 'following', 'sentences', 'text', 'according',
        'mentioned', 'one', 'two', 'three', 'four', 'five', 'them', 'their',
        'you', 'your', 'english', 'chinese', 'indicate', 'whether', 'true',
        'false', 'ticking', 'boxes', 'above', 'below', 'does', 'did', 'will',
        'can', 'how', 'why', 'who', 'where', 'when', 'many', 'much', 'any',
        'blanks', 'table', 'column', 'characters', 'character', 'previous'}


def concept_for(text, fallback='man-general'):
    words = [w for w in re.findall(r"[a-z']{3,}", (text or '').lower())
             if w not in STOP]
    return 'man-' + '-'.join(sorted(set(words))[:3]) if words else fallback
