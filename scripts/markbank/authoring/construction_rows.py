#!/usr/bin/env python3
"""The components a Construction Studies criterion row is priced in, as parts.

    python3 scripts/markbank/authoring/construction_rows.py [--write]

A theory-paper criterion row often prices its item in named components on
the row's own line — "Design feature 1 (2 for point, 4 for discussion)",
"Scale - 4 marks Drafting - 4 marks", "Material 1 - identify (2 marks), adv
(1 mark), disadv (1 mark)" — and the card offered one mark strip for the
whole row, so a student who had the point but not the discussion could not
say so. Alex's rule (2026-10-23): what the scheme prices is a row with its
marks on it. A complete-question card may hold at most five rows per task,
so the components are not more rows: they are `parts` of the row (types/
markBank.ts MarkRowPart), each placed on its own marks, and the row's claim
is their sum. The row's id, text, marks and steps stay as the paper
validators pin them.

The pass adds no words. Each part is the component as the row prints it
("point", "discussion", "Scale", "identify"), its marks are the printed
price, and its steps are the ladder the row's note prints for it ("each
excellent 4, good 3, fair 2") or every mark up to its price. A row whose
prices do not add up to it is left alone.

Every card it changes is recorded the way the Construction review ledger
requires (construction_corrections.py): a card corrected in place keeps its
correction record and gains the hash it had until now under
`supersededSha256`, with `correctedSha256` moved to the new hash; a card
without one gains a `revisions` entry linking the two hashes. Complete-
question cards mirror their tasks' rows, parts included. The pass changes
nothing on a second run.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from construction_corrections import card_hash  # noqa: E402

R = Path(__file__).resolve().parents[3]
AUTHORED = R / 'scripts/markbank/authored'
REASON = ('Components the row prices by name ("2 for point, 4 for discussion") are parts of the row, '
          'each placed on its own marks; the row itself, its marks and its steps are unchanged.')

# "Design feature 1 (2 for point, 4 for discussion)", "Strategy 1: (2 for point, 4 for discussion)",
# "Ventilation point 1 (4 for notes, 4 for sketches)", also printed without its opening bracket.
FOR_PAIR = re.compile(r'^(?P<head>.*?)\s*[-–:]?\s*\(?\s*(?P<a>\d+)\s*(?:marks?\s*)?for\s+(?P<an>[a-z]+)\s*,\s*(?P<b>\d+)\s*(?:marks?\s*)?for\s+(?P<bn>[a-z]+)\s*\)?\s*$', re.I)
# "Advancement 1 (note 4 marks, sketch 4 marks)", "Advantage 1 (point 3 marks, discussion 3 marks)"
NAMED_PAIR = re.compile(r'^(?P<head>.*?)\s*[-–:]?\s*\(\s*(?P<an>[a-z]+)\s+(?P<a>\d+)\s*marks?\s*,\s*(?P<bn>[a-z]+)\s+(?P<b>\d+)\s*marks?\s*\)\s*$', re.I)
# "Scale - 4 marks Drafting - 4 marks", "Scale 4 marks: Drafting 4 marks:"
SCALE = re.compile(r'^(?P<an>Scale)\s*[-–:]?\s*(?P<a>\d+)\s*marks?\s*[:,]?\s*(?P<bn>Drafting)\s*[-–:]?\s*(?P<b>\d+)\s*marks?\s*:?\s*$', re.I)
# "Material 1 - identify (2 marks), adv (1 mark), disadv (1 mark)"
TRIPLE = re.compile(r'^(?P<head>.+?)\s*[-–]\s*(?P<an>identify)\s*\(\s*(?P<a>\d+)\s*marks?\s*\),\s*(?P<bn>adv)\s*\(\s*(?P<b>\d+)\s*marks?\s*\),\s*(?P<cn>disadv)\s*\(\s*(?P<c>\d+)\s*marks?\s*\)\s*$', re.I)
# "Design detail 1 - note 8 marks, sketch 8 marks", "Design consideration 1 Note 3 marks & sketch 3 marks"
NOTE_SKETCH = re.compile(r'^(?P<head>.+?)\s*[-–]?\s*(?P<an>notes?)\s*(?P<a>\d+)\s*marks?\s*[,&]\s*(?P<bn>sketch(?:es)?)\s*(?P<b>\d+)\s*marks?\s*$', re.I)
# "Damp proof material 1 (specification 3 marks) (advantages 3 marks)"
SPEC = re.compile(r'^(?P<head>.+?)\s*\(\s*(?P<an>specification)\s*(?P<a>\d+)\s*marks?\s*\)\s*\(\s*(?P<bn>advantages)\s*(?P<b>\d+)\s*marks?\s*\)\s*$', re.I)
# "Cable size (2) and colour (3)", "Reinforcement (2) + dimensions (2)"
BRACKETED = re.compile(r'^(?P<an>[A-Za-z][A-Za-z ]*?)\s*\(\s*(?P<a>\d+)\s*\)\s*(?:and|\+)\s*(?P<bn>[a-z][a-z ]*?)\s*\(\s*(?P<b>\d+)\s*\)\s*$', re.I)
# "Discussion (point 1) - 2 marks for point, 4 marks for discussion"
MARKS_FOR = re.compile(r'^(?P<head>.+?\(point\s*\d+\))\s*-\s*(?P<a>\d+)\s*marks?\s*for\s*(?P<an>point),\s*(?P<b>\d+)\s*marks?\s*for\s*(?P<bn>discussion)\s*$', re.I)
SHAPES = (FOR_PAIR, NAMED_PAIR, SCALE, TRIPLE, NOTE_SKETCH, SPEC, BRACKETED, MARKS_FOR)
# "each excellent 4, good 3, fair 2": the ladder every component is placed on.
LADDER = re.compile(r'each\s+excellent\s+(\d+)\s*,\s*good\s+(\d+)\s*,\s*fair\s+(\d+)', re.I)


def slug(word):
    return re.sub(r'[^a-z0-9]+', '-', word.lower()).strip('-')


def components(row):
    """[(printed word, marks)] the row prices by name, or None."""
    text = ' '.join(row['verbatim'].split())
    for shape in SHAPES:
        m = shape.match(text)
        if not m:
            continue
        g = m.groupdict()
        found = [(g['an'], int(g['a'])), (g['bn'], int(g['b']))]
        if 'cn' in g:
            found.append((g['cn'], int(g['c'])))
        if sum(marks for _, marks in found) != row['marks']:
            return None
        if len({slug(word) for word, _ in found}) != len(found):
            return None
        return found
    return None


def steps_for(marks, note):
    m = LADDER.search(note or '')
    if m:
        ladder = sorted({int(x) for x in m.groups()} | {0})
        if ladder[-1] == marks:
            return ladder
    return list(range(marks + 1))


def with_parts(row):
    """The row with its parts, or the row itself when it prices no components."""
    if row.get('kind') != 'criterion' or row.get('parts') or not row.get('permittedMarks'):
        return row
    found = components(row)
    if not found:
        return row
    row['parts'] = [{'id': slug(word), 'verbatim': word, 'marks': marks, 'permittedMarks': steps_for(marks, row.get('contextNote'))}
                    for word, marks in found]
    return row


def record(review, card_id, before, after):
    """The ledger entry that links the card's hashes, extended when one exists."""
    if before == after:
        return
    for fix in review.get('corrections', []) + review.get('revisions', []):
        if fix['cardId'] == card_id:
            assert fix['correctedSha256'] == before, (card_id, 'ledger does not hold the current hash')
            fix.setdefault('supersededSha256', []).append(before)
            fix['correctedSha256'] = after
            return
    review.setdefault('revisions', []).append({'cardId': card_id, 'priorSha256': before, 'correctedSha256': after, 'reason': REASON})


def main():
    write = '--write' in sys.argv
    authored_path = AUTHORED / 'construction-studies.json'
    authored = json.loads(authored_path.read_text())
    by_id = {c['id']: c for c in authored}
    changed = []
    for path in sorted(AUTHORED.glob('construction-studies-*-reviewed.json')):
        review = json.loads(path.read_text())
        cards = {t['card']['id']: t['card'] for t in review['tasks']}
        before = {cid: card_hash(c) for cid, c in cards.items()}
        for card in cards.values():
            if 'taskGroups' in card:
                continue
            for row in card['rows']:
                with_parts(row)
        # A complete-question card mirrors its tasks' rows, parts included, under its own prefixes.
        for card in cards.values():
            for group in card.get('taskGroups', []):
                kid = cards[group['sourceCardId']]
                prefix = group['rowIds'][0][:len(group['rowIds'][0]) - len(kid['rows'][0]['id'])]
                for kid_row, row in zip(kid['rows'], [r for r in card['rows'] if r['id'] in group['rowIds']]):
                    assert row['id'] == prefix + kid_row['id'], (card['id'], row['id'])
                    if kid_row.get('parts'):
                        row['parts'] = json.loads(json.dumps(kid_row['parts']))
        for cid, card in cards.items():
            after = card_hash(card)
            if after != before[cid]:
                record(review, cid, before[cid], after)
                assert cid in by_id and {k: v for k, v in by_id[cid].items() if k != 'rows'} == {k: v for k, v in card.items() if k != 'rows'}, cid
                by_id[cid]['rows'] = card['rows']
                changed.append(cid)
        if write:
            path.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
    rows = sum(1 for c in authored for r in c['rows'] if r.get('parts'))
    print(f'{len(changed)} cards changed, {rows} rows carry parts', file=sys.stderr)
    if write:
        authored_path.write_text(json.dumps(authored, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
