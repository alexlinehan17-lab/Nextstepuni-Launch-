"""Keep reviewed R4 notices when a Russian sitting is regenerated."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXED_LINE = 'The scheme prints no answer for this part.'


def annotate_no_answers(cards):
    path = ROOT / 'scripts/markbank/authoring/russian-no-answer.json'
    if not path.exists():
        return cards
    entries = json.loads(path.read_text())['cards']
    checked = {}
    for card in cards:
        entry = entries.get(card['id'])
        if entry is None:
            continue
        if entry.get('treatment') == 'unprinted-criterion':
            assert card['kind'] == 'question', card['id']
            assert card['tariffModel'] == {'kind': 'fixed'}, card['id']
            assert len(card['rows']) == 1, card['id']
            row = card['rows'][0]
            assert row['kind'] == 'criterion' and row['unprinted'] is True, card['id']
            assert row['verbatim'] == FIXED_LINE and row['marks'] == entry['printedMarks'], card['id']
        elif entry.get('treatment') == 'empty-points':
            assert card['kind'] == 'rubric', card['id']
            assert card['rubric']['system'] == 'language-points', card['id']
            assert all(not group['rows'] for group in card['rubric']['groups']), card['id']
        else:
            assert card['kind'] == 'rubric', card['id']
            assert card['rubric']['system'] == 'language-writing', card['id']
        assert card['totalMarks'] == entry['printedMarks'], card['id']
        assert card['review']['schemePages'] == entry['schemePages'], card['id']
        relative = entry['schemePath']
        if relative not in checked:
            checked[relative] = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert checked[relative] == entry['schemeSha256'], card['id']
        if card['kind'] == 'rubric':
            note = card['rubric'].get('markingGuideNote', '')
            if not note.startswith(FIXED_LINE):
                card['rubric']['markingGuideNote'] = FIXED_LINE + (' ' + note if note else '')
        card['review']['reviewedAt'] = entry['reviewedAt']
        card['review']['noPrintedAnswer'] = {
            'fixedLine': FIXED_LINE,
            'schemePages': entry['schemePages'],
            'evidence': entry['evidence'],
        }
    return cards
