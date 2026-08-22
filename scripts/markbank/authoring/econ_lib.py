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


def defurnish(s):
    """One slice with the running footer taken out of it."""
    return tidy(FOOTER.sub(' ', s))


load = make_load('economics')
semis = make_semis(JUNK)
card = make_card('economics', default_section='B')
audit = make_audit(MAX_OPTIONS)
emit = make_emit(audit)
