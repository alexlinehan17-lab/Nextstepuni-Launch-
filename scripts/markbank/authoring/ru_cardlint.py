"""Apply the unchanged card lint rules to the complete served Russian overlay.

The generic authored-file loader reads only the legacy manifest. This entry
point follows withReviewedCards' stable-ID replacement and append order, so
new source-reviewed tasks cannot silently fall outside the lint gate.
"""
import json
from pathlib import Path
import cardlint

ROOT = Path(__file__).resolve().parents[3]


def russian_cards():
    originals = json.loads((ROOT / 'scripts/markbank/authored/russian.json').read_text())
    reviewed = json.loads((ROOT / 'components/MarkBank/cards/russian/reviewed.json').read_text())
    original_ids = {card['id'] for card in originals}
    by_id = {card['id']: card for card in reviewed}
    assert len(original_ids) == len(originals), 'Duplicate original Russian identity'
    assert len(by_id) == len(reviewed), 'Duplicate reviewed Russian identity'
    for card in reviewed:
        assert card['subjectId'] == 'russian', card['id']
        if card['id'] in original_ids:
            assert 'reviewed-card-correction' in card['qa']['gates'], card['id']
    cards = [by_id.get(card['id'], card) for card in originals]
    cards += [card for card in reviewed if card['id'] not in original_ids]
    assert len({card['id'] for card in cards}) == len(cards)
    assert original_ids <= {card['id'] for card in cards}
    return cards


def main():
    cardlint.DECK_LOADERS['russian'] = russian_cards
    findings = cardlint.lint('russian')
    print(f"Actual Russian runtime overlay: {cardlint.READ_COUNTS['russian']} cards; {len(findings)} findings")
    for subject, identifier, category, detail in findings:
        print(f'{subject}: {identifier}: {category}: {detail}')
    if findings:
        raise SystemExit(1)
    print('clean')


if __name__ == '__main__':
    main()
