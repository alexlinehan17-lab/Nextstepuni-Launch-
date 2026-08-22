"""Economics binding of the shared authoring helpers.

The general helpers, and the reasoning behind each guard in them, are in
markbank_authoring.py. This file is what is true of Economics and nothing else.

Economics is the first subject authored against a specification the papers were
actually sat on: the NCCA specification of 2019, first examined 2021, so the
whole 2021-2025 corpus sits on one syllabus with nothing to straddle.

Option text is always SLICED from the scheme markdown, never retyped: the build's
provenance gate requires every marking point to appear in its own scheme, and both
historical scheme corruptions in this repo entered through hand transcription.
"""
import re

from econ_refs import CORRECTIONS
from markbank_authoring import (  # noqa: F401  (re-exported for the econ_*.py scripts)
    VALID_KINDS, anyN, block, heads, make_audit, make_card, make_emit, make_load,
    make_semis, point, tidy,
)

MAX_OPTIONS = 14          # optionCapFor('B') in scripts/markbank/optionCap.mjs


# A segment that is not a marking point. The provenance gate cannot catch these
# -- they ARE in the scheme -- but a running page footer or a note to the
# examiner rendered as a student-facing option is worse than a missing option.
#
# Economics sets its page number as "17 | P a g e", one letter-spaced word, so
# the footer survives tidy() as "P a g e" in the middle of a slice.
JUNK = re.compile(
    r'^(?:[•\-–—\s]*$'                                  # bullets / dashes only
    r'|Accept\b'                                        # note to the examiner
    r'|.*(?:P a g e|Leaving Certificate|Marking Scheme|Coimisiún|Economics – ))',
    re.IGNORECASE)

# "17 | P a g e" is the running footer, letter-spaced, and it survives tidy() in
# the MIDDLE of a slice rather than at its edges — a marking point sliced across
# a page break otherwise carries the footer into what a student is shown. The
# provenance gate cannot object: the footer really is in the scheme.
FOOTER = re.compile(r'\s*\d+\s*\|\s*P\s*a\s*g\s*e\s*')

# The extractor lifts every marks cell into angle brackets, and the SEC prints
# the SECOND cell of a descending tariff partway into the first response rather
# than beside the question: "...with a rising ⟨1 @ 4⟩ population the demand...".
# comparableScheme() strips these from the scheme, so a claim that keeps one can
# never match — and it would put "⟨1 @ 4⟩" in front of a student besides.
MARKS_CELL = re.compile(r'\s*⟨[^⟩]*⟩\s*')

# The same tariff spelled out in words. The SEC prints it beside the QUESTION
# rather than in the marks column, so flattening the page drops it into the
# middle of whatever response happens to be printed alongside — four shipped
# options read "...this may encourage 2nd @ 4 people to move". Stripped
# everywhere rather than only at the start of a response, which is all
# bullets() used to do. comparableScheme() strips it from the scheme too, as an
# added form, so a claim without it still traces.
ORDINAL_TARIFF = re.compile(r'\s*\b\d+\s*(?:st|nd|rd|th)\s*[@x]\s*\d+\b\s*', re.I)


def defurnish(s):
    """One slice with the page furniture the scheme's own comparison ignores."""
    return tidy(ORDINAL_TARIFF.sub(' ', MARKS_CELL.sub(' ', FOOTER.sub(' ', s))))


# Where the examiner stops answering one part and starts the next. heads() runs
# its LAST block to the end of the chunk, so if the chunk is bounded even
# slightly loosely that block swallows whatever follows — one option reached
# 9,047 characters and ended in the instructions of a later question. The
# provenance gate cannot object: the text really is in the scheme, contiguously.
NEXT_PART = re.compile(
    r'\((?:i{1,3}|iv|v|vi{1,3}|[a-c])\)\s'      # (i) (ii) (a) (b)
    r'|Question\s+\d+'
    r'|Suggested responses'
    r'|Must have a MINIMUM'                      # an instruction to the examiner
    r'|(?:Higher|Ordinary) Level Economics')     # the running header


def as_option(s):
    """One marking point, stopped where the next part of the paper begins."""
    text = defurnish(s)
    cut = NEXT_PART.search(text)
    return tidy(text[:cut.start()]) if cut else text


def bullets(chunk, drop_prefix=None):
    """The scheme's bullet-listed responses, in scheme order.

    Ordinary Level sets its possible responses as a bullet list where Higher
    Level runs them together under bold headings, and it spells the descending
    tariff out in words beside them — "1st @ 8", "2nd @ 4" — rather than in the
    marks column. Both are the same shape underneath.
    """
    t = defurnish(chunk)
    if drop_prefix and t.startswith(drop_prefix):
        t = t[len(drop_prefix):]
    out = []
    for x in re.split(r'\s*•\s*', t):
        x = as_option(re.sub(r'^\s*\d+(?:st|nd|rd|th)\s*@\s*\d+\s*', '', tidy(x)))
        if len(x) < 12 or JUNK.match(x):
            continue
        out.append(x)
    return out


_load = make_load('economics')

# Every appender adds its own marked block to the end of the scheme markdown, and
# each repeats the answers the primary extraction already carries. Slicing across
# that boundary makes every anchor ambiguous for reasons that have nothing to do
# with the paper — and the second copy is table cells, in the wrong order.
APPENDED = '<!-- markbank:'


def load(year, level):
    """The scheme's PRIMARY extraction, without the appended blocks.

    The appended blocks exist for the provenance gate, which searches the whole
    file. Authoring slices only from what the extractor read off the page.
    """
    raw = _load(year, level)
    cut = raw.find(APPENDED)
    return raw if cut < 0 else raw[:cut]
semis = make_semis(JUNK)
_card = make_card('economics', default_section='B')


def card(cid, *a, **kw):
    """An Economics card, with its citation corrected where the id misnames it.

    See econ_refs.py: nineteen ids count the wrong question, and the citation
    rather than the id is what gets fixed.
    """
    c = _card(cid, *a, **kw)
    c['questionRef'] = CORRECTIONS.get(cid, c['questionRef'])
    return c
audit = make_audit(MAX_OPTIONS)
emit = make_emit(audit)
