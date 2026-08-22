"""Home Economics binding of the shared authoring helpers.

Everything general moved to markbank_authoring.py when Economics became the
second subject authored this way; this file is what is true of Home Economics
and nothing else. The names it exports are unchanged, so every he_*.py script
and test/markBankAuthoringToolkit.test.ts still see exactly the same API.

Option text is always SLICED from the scheme markdown, never retyped: the build's
provenance gate requires every marking point to appear in its own scheme, and both
historical scheme corruptions in this repo entered through hand transcription.
"""
import re

from markbank_authoring import (  # noqa: F401  (re-exported for the he_*.py scripts)
    VALID_KINDS, anyN, block, heads, make_audit, make_card, make_emit, make_load,
    make_semis, point, tidy,
)

MAX_OPTIONS = 14          # optionCapFor('B') in scripts/markbank/optionCap.mjs


# A segment that is not a marking point. The provenance gate cannot catch these
# -- they ARE in the scheme -- but a running page footer or a note to the
# examiner rendered as a student-facing option is worse than a missing option.
JUNK = re.compile(
    r'^(?:[•\-–—\s]*$'                   # bullets / dashes only
    r'|Accept\b'                                       # note to the examiner
    r'|.*(?:Leaving Certificate|Home Economics –|Coimisiún|Marcanna Breise))',
    re.IGNORECASE)

load = make_load('home-economics')
semis = make_semis(JUNK)
card = make_card('home-economics', default_section='B')
audit = make_audit(MAX_OPTIONS)
emit = make_emit(audit)
