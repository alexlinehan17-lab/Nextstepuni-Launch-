"""Preserve original LCVP concept identifiers while source-reviewing tasks."""
import json
from pathlib import Path

_RECORD = json.loads((Path(__file__).parent / 'lcvp/original-concept-identities.json').read_text())
ORIGINAL_CONCEPT_IDS = _RECORD['conceptIds']
assert len(ORIGINAL_CONCEPT_IDS) == _RECORD['originalCardCount'] == 314


def concept_id(card_id, fallback):
    return ORIGINAL_CONCEPT_IDS.get(card_id, fallback)
