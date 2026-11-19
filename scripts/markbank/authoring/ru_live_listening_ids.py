"""Keep the eight listening IDs that became live in the coordinator release."""
import json
from pathlib import Path

BINDINGS = json.loads((Path(__file__).parent / 'reviews/russian-after-release-20261119/listening-identities.json').read_text())

def live_id(identifier):
    return BINDINGS.get(identifier, {}).get('id', identifier)

def preserve_live_listening_ids(cards):
    for card in cards:
        binding = BINDINGS.get(card['id'])
        if binding:
            card['review']['atlasQuestionKey'] = card['id'].split('-', 3)[3]
            card['id'] = binding['id']
            card['conceptId'] = binding['conceptId']
    assert len({card['id'] for card in cards}) == len(cards)
    return cards
