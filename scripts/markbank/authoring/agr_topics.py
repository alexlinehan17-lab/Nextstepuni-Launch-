#!/usr/bin/env python3
"""Ancient Greek — which part of the course an ask belongs to, off the paper.

The taxonomy is the canonical one in curriculum.ts, and the strand these cards
tag against is `ancient-greek-4`, "Legacy Written Paper — Task Types". That is
not a convenience, and it is Latin's situation exactly: Ancient Greek's
specification was redeveloped, and its Strands 1 to 3 describe a course
assessed by a capstone text and a research study the SEC has not yet examined.
Every paper in the corpus, 2010 to 2024, is the LEGACY written paper, and the
legacy strand's six task types are that paper's four questions:

    ancient-greek-4-0  Composition — Translation into Greek        Q1 Section A
    ancient-greek-4-1  Unseen Comprehension — Prose with Questions Q1 Section B
    ancient-greek-4-2  Unseen Translation into English             Q2, and the
                       (Prose & Verse)                             OL Q1 and
                                                                   Q2(i)
    ancient-greek-4-3  Prescribed Prose Text — Translation &       Q3, the
                       Questions (e.g. Plato)                      Intellectual
                                                                   Revolution
                                                                   route
    ancient-greek-4-4  Prescribed Homer — Translation & Questions  Q3, the World
                                                                   of Heroes
                                                                   route
    ancient-greek-4-5  Greek History & Civilisation                Q4 (Higher),
                       (incl. Art & Architecture)                  Q3 (Ordinary)

Question 3's two routes are the syllabus's two PRESCRIBED COURSES, and which
letter carries which changes year to year: 2010 Higher sets A World of Heroes
as Section A and 2015 sets it as Section B. The paper names the course itself,
in capitals under the route's own translation passage —

    … δείσαντες τὸ ἐπὶ διαβολῇ ἐς δίκην καταπλεῦσαι.
                                      THE INTELLECTUAL REVOLUTION

— so the route is classified by that credit and never by the letter. The two
courses are not a prose/verse split and the subtopic names are read as their
headline authors: A World of Heroes is the Homer course (Iliad, with Herodotus
and Sophocles), and The Intellectual Revolution is the Plato course (with
Thucydides and Euripides). Where the paper credits an AUTHOR instead — its
unseen passages are signed XENOPHON, THUCYDIDES, SOPHOCLES, HOMER — the author
decides, by the course it belongs to.
"""
import re

STRAND = 'ancient-greek-4'

COMPOSITION = 'ancient-greek-4-0'
COMPREHENSION = 'ancient-greek-4-1'
UNSEEN = 'ancient-greek-4-2'
PLATO_COURSE = 'ancient-greek-4-3'      # Prescribed Prose Text (e.g. Plato)
HOMER_COURSE = 'ancient-greek-4-4'      # Prescribed Homer
CIVILISATION = 'ancient-greek-4-5'

# The credit the paper prints under a prescribed passage, and the course each
# belongs to. Both course names and both sets of authors are read off the page
# rather than inferred: the SEC signs its unseen passages with the author and
# its prescribed ones with the course.
HOMER = ('A WORLD OF HEROES', 'HOMER', 'HERODOTUS', 'SOPHOCLES')
PLATO = ('THE INTELLECTUAL REVOLUTION', 'PLATO', 'THUCYDIDES', 'EURIPIDES',
         'XENOPHON', 'DEMOSTHENES', 'LYSIAS', 'AESCHYLUS', 'ARISTOPHANES',
         'READING GREEK')
CREDIT = re.compile(r'\b(' + '|'.join(HOMER + PLATO) + r')\b')


def author_of(text):
    """The author the paper credits this passage to, or None."""
    found = CREDIT.findall((text or '').upper())
    return found[-1] if found else None


def topic_for(level, q, kind, route_text=''):
    """The syllabus task type this printed ask belongs to.

    `route_text` is the WHOLE of the route the ask sits in, because Question
    3's classification lives in the credit under the route's translation
    passage and not in the question a card is made from: "Outline the role
    played by Teiresias in the course of the play" names no author, and the
    passage three inches above it is credited to Sophocles.
    """
    if kind == 'translate-into-greek':
        return COMPOSITION
    if kind == 'comprehension':
        return COMPREHENSION
    if kind == 'translate-into-english':
        return UNSEEN
    last = 4 if level == 'hl' else 3
    if q == last:
        return CIVILISATION
    credit = author_of(route_text)
    if credit in HOMER:
        return HOMER_COURSE
    return PLATO_COURSE


# A stable, level-independent identity for the thing an ask is ABOUT, so a
# Higher card and the Ordinary card asking the same thing share a student's
# work when they drop level. Ancient Greek sets the same prescribed books and
# the same history topics at both levels in the same year, and often the same
# question of them: "Give an account of the Sicilian Expedition" is set at
# Ordinary in 2023 and "Explain why Alkibiades was recalled to Athens from the
# Sicilian Expedition" at Higher.
STOP = {'the', 'a', 'an', 'of', 'in', 'and', 'or', 'to', 'from', 'on', 'with',
        'your', 'you', 'was', 'were', 'is', 'are', 'did', 'do', 'does', 'how',
        'what', 'why', 'who', 'which', 'that', 'this', 'these', 'those',
        'for', 'by', 'at', 'as', 'it', 'his', 'her', 'their', 'its', 'any',
        'two', 'three', 'one', 'following', 'answer', 'give', 'write',
        'notes', 'note', 'account', 'describe', 'discuss', 'comment',
        'explain', 'outline', 'view', 'brief', 'briefly', 'opinion', 'book',
        'name', 'names', 'state', 'about', 'own', 'above', 'below', 'passage',
        'reference', 'answers', 'question', 'questions', 'be', 'been', 'has',
        'have', 'had', 'not', 'but', 'they', 'them', 'he', 'she', 'we',
        'short', 'main', 'features', 'each', 'ancient', 'greek', 'look',
        'looked', 'having', 'imagine', 'photographs', 'photograph'}


def concept_for(text):
    words = [w for w in re.findall(r"[A-Za-z][A-Za-z'’-]+",
                                   (text or '').lower())
             if w not in STOP and len(w) > 2]
    return 'agr-' + '-'.join(sorted(set(words))[:4]) if words else 'agr-general'
