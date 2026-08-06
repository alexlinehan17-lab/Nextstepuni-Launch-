"""
Mark Bank — where each question begins in a converted marking scheme.

One implementation, because two already drifted once: build-deck.mjs and the deck
test each kept their own copy of the provenance comparison, and when the build
learned to ignore page markers and the test did not, four correct cards were
reported as untraceable by the very check that had just accepted them.

Subjects do not head their questions alike, and a reader built for one silently
returns the wrong region for another rather than failing:

    Question 4            Business Section 3; Home Economics Sections B and C
    4 (A) Explain…        Business support notes
    4. State two…         Home Economics Section A short questions
    4.(a) 'Fats are…'     Home Economics Section C electives

The Home Economics slicer, asked for Section A Question 3, was handing back
Section B's Question 3 — a plausible-looking slice of the wrong question, which
is the worst thing a pre-slicer can do.
"""

import re

# Every shape a question head takes, in the order they must be tried: the
# elective form "4.(a)" has to be tested before the short form "4." or the dot
# swallows it.
# A heading, not a sentence ABOUT a question. Every rubric block carries
# "Question 1 is worth 80 marks.", and matching it set the reader into the long
# sections before Section A's answers began, losing Section A entirely. But a
# heading DOES carry trailing text — "Question 1 Max", "Question 4 - Core - 80
# marks" — so the trailing text cannot simply be forbidden: rejecting it took
# Business from full coverage to none. What separates them is the verb.
LONG_Q = re.compile(r"^\s*Question\s+(\d{1,2})\b(?![^\n]*\b(?:is|are)\s+worth\b)", re.I)
ELECTIVE_Q = re.compile(r"^\s*(\d{1,2})\.\s*\(([a-h])\)")
NOTES_Q = re.compile(r"^\s*(\d{1,2})\s*\(([A-Ha-h])\)")
SHORT_Q = re.compile(r"^\s*(\d{1,2})\.\s+(\S)")

ELECTIVE = re.compile(r"^\s*Elective\s+\d", re.I)
SECTION = re.compile(r"^\s*Section\s+([A-C1-3])\s*(\d+\s*(or\s*\d+\s*)?marks?)?\s*$", re.I)


def question_heads(lines):
    """Every (section, question, line index) a question starts at.

    Sections are inferred from question SHAPE, not from headings: every scheme
    prints a rubric block naming all its sections a few lines apart, so reading
    headings in order flips into the last one before a single answer of the
    first. An Elective heading is the exception — it genuinely opens Section C.
    """
    heads, section, seen_long = [], None, False
    for i, raw in enumerate(lines):
        line = raw.rstrip()
        if SECTION.match(line):
            continue
        if ELECTIVE.match(line):
            section = "C"
            continue
        if (m := LONG_Q.match(line)):
            if section != "C":
                section = "B"
            seen_long = True
            heads.append((section, m.group(1), i))
            continue
        if (m := ELECTIVE_Q.match(line)):
            heads.append((section or "C", m.group(1), i))
            continue
        if (m := NOTES_Q.match(line)):
            heads.append((section or "B", m.group(1), i))
            continue
        if (m := SHORT_Q.match(line)):
            # A short question only heads Section A, and Section A comes first.
            if not seen_long and section is None:
                heads.append(("A", m.group(1), i))
    return heads


# Subjects name their sections differently — Business numbers them 1/2/3, the
# sciences and Home Economics letter them A/B/C — while the shapes above only
# reveal whether a question is SHORT or LONG. Compare by kind, not by label, or
# a Business request for section "3" matches nothing and returns an empty slice.
SHORT_SECTIONS = {"1", "A"}


def _same_kind(inferred, requested):
    if not inferred or not requested:
        return True
    return (inferred.upper() in SHORT_SECTIONS) == (requested.upper() in SHORT_SECTIONS)


def blocks_for(lines, section, question):
    """(start, end) for every block belonging to one question.

    Exact section first, kind only as a fallback. Kind alone is too coarse where
    a paper has two long sections — asking Home Economics for Section C returned
    Section B's questions, since both are "long" — while exact alone is too
    strict for Business, whose sections are numbered where the shapes infer
    letters.
    """
    heads = question_heads(lines)

    def gather(match):
        out = []
        for idx, (sec, q, start) in enumerate(heads):
            if q != str(question) or not match(sec):
                continue
            end = heads[idx + 1][2] if idx + 1 < len(heads) else len(lines)
            out.append((start, end))
        return out

    if section:
        exact = gather(lambda sec: bool(sec) and sec.upper() == section.upper())
        if exact:
            return exact
    return gather(lambda sec: _same_kind(sec, section))
