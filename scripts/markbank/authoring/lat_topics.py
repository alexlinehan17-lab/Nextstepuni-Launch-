#!/usr/bin/env python3
"""Latin — which part of the course an ask belongs to, read off the paper.

The taxonomy is the canonical one in curriculum.ts, and the strand these cards
tag against is `latin-3`, "Legacy Written Paper — Task Types". That is not a
convenience: Latin's specification was redeveloped, and its Strands 1 and 2 —
"Latin Language" and "Literature in Context" — describe a course assessed by a
capstone text and a research study that the SEC has not yet examined. Every
paper in the corpus, 2021 to 2025, is the LEGACY written paper, and the legacy
strand's seven task types are that paper's five questions:

    latin-3-0  Composition — Translation into Latin              Q1 Section A
    latin-3-1  Unseen Comprehension — Prose Passage with Questions Q1 Section B
    latin-3-2  Unseen Translation into English (Prose & Verse)    Q2
    latin-3-3  Prescribed Prose Text — Translation & Questions    Q3, prose route
    latin-3-4  Prescribed Poetry — Virgil's Aeneid                Q3, verse route
    latin-3-5  Grammar, Accidence & Scansion                      Q4
    latin-3-6  Roman History & Civilisation Essays                Q5

Question 3's two routes are one prose text and one verse text, and which is
which changes every year — 2021 Higher sets Livy against Virgil's Aeneid II,
2023 Higher Cicero against Aeneid I. So the route is classified by the AUTHOR
the paper prints under its own passage, never by the letter.
"""
import re

STRAND = 'latin-3'

COMPOSITION = 'latin-3-0'
COMPREHENSION = 'latin-3-1'
UNSEEN = 'latin-3-2'
PRESCRIBED_PROSE = 'latin-3-3'
PRESCRIBED_VERSE = 'latin-3-4'
GRAMMAR = 'latin-3-5'
CIVILISATION = 'latin-3-6'

# The authors the corpus sets, split as the syllabus splits them. Read off the
# credit the paper prints under its own passage.
VERSE = ('Virgil', 'Ovid', 'Catullus', 'Horace', 'Lucretius', 'Juvenal',
         'Martial', 'Propertius', 'Tibullus')
PROSE = ('Livy', 'Cicero', 'Caesar', 'Sallust', 'Pliny', 'Tacitus', 'Nepos',
         'Suetonius', 'Seneca')
AUTHOR = re.compile(r'\b(' + '|'.join(VERSE + PROSE) + r')\b')


def author_of(text):
    """The author the paper credits this passage to, or None."""
    found = AUTHOR.findall(text or '')
    return found[-1] if found else None


def topic_for(q, route_kind, route_text=''):
    """The syllabus task type this printed ask belongs to.

    `route_text` is the whole of the route the ask sits in, because Question
    3's classification lives in the author credit under the route's TRANSLATE
    passage rather than in the question the card is made from: "Comment on
    Livy's skill as a storyteller as displayed in Book XXX" names its author,
    but "What features of Book VI are typical of an epic poem?" does not.
    """
    if q == 1:
        return (COMPOSITION if route_kind == 'translate-into-latin'
                else COMPREHENSION)
    if q == 2:
        return UNSEEN
    if q == 3:
        author = author_of(route_text)
        if author in VERSE:
            return PRESCRIBED_VERSE
        if author in PROSE:
            return PRESCRIBED_PROSE
        return None
    if q == 4:
        return GRAMMAR
    return CIVILISATION


# A stable, level-independent identity for the thing an ask is ABOUT, so a
# Higher card and the Ordinary card asking the same thing share a student's
# work when they drop level. Latin's Ordinary and Higher papers set the same
# prescribed books in the same year, and often the same question of them.
STOP = {'the', 'a', 'an', 'of', 'in', 'and', 'or', 'to', 'from', 'on', 'with',
        'your', 'you', 'was', 'were', 'is', 'are', 'did', 'do', 'does', 'how',
        'what', 'why', 'who', 'which', 'that', 'this', 'these', 'those',
        'for', 'by', 'at', 'as', 'it', 'his', 'her', 'their', 'its', 'any',
        'two', 'three', 'one', 'following', 'answer', 'give', 'write',
        'notes', 'note', 'account', 'describe', 'discuss', 'comment',
        'explain', 'outline', 'view', 'brief', 'briefly', 'opinion', 'book',
        'name', 'names', 'state', 'about', 'own', 'above', 'below', 'passage',
        'reference', 'answers', 'question', 'questions', 'be', 'been', 'has',
        'have', 'had', 'not', 'but', 'they', 'them', 'he', 'she', 'we'}


def concept_for(text):
    words = [w for w in re.findall(r"[A-Za-z][A-Za-z'’-]+", (text or '').lower())
             if w not in STOP and len(w) > 2]
    return 'lat-' + '-'.join(sorted(set(words))[:4]) if words else 'lat-general'
