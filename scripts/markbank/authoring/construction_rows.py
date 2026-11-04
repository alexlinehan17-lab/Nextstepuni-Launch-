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
("point", "discussion", "Scale", "identify") — or, where the row's text
names the item alone and its note carries the scheme's split before its
examples ("Guideline 1" / "Notes 6 and sketches 6. Such as: …"), the
component as the note prints it — its marks are the printed price, and its
steps are the ladder the row's note prints for it ("each excellent 4, good
3, fair 2") or every mark up to its price. A row whose prices do not add
up to it is left alone.

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
import construction_paper as cp  # noqa: E402

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
# A row whose text names the item alone ("Guideline 1", "Safety training") and whose note carries the
# scheme's split before its examples: "Notes 6 and sketches 6. Such as: …", "Point 2 and discussion 4. Such as: …",
# "For this distinct design feature, award notes 4 and a relevant freehand sketch 4".
NOTE_PAIR = re.compile(r'\b(?P<an>notes?|points?|sketch(?:es)?|discussion)\s*(?P<a>\d+)\s*(?:marks?)?\s*(?:and|,|&|\+)\s*(?:a\s+relevant\s+freehand\s+|a\s+)?(?P<bn>notes?|sketch(?:es)?|discussion|points?)\s*(?P<b>\d+)\b', re.I)
EXAMPLES = re.compile(r'\b(?:Such as|Menu|e\.g\.|For example)\b', re.I)
# The note's first sentence prices two components by name, bracketed or bare, before its examples:
# "The distribution board drawn (4) and annotated (1)", "Advantage 1 (3) and disadvantage 1 (3) of …",
# "Sketches showing the inner leaf (5) and its insulation (5)", "Type 3 and thickness 3",
# "The flashing (DPC) at the window head 2 and the insulation above the window head 2".
NOTE_BRACKETED = re.compile(r'^(?:The\s+|Both\s+)?(?P<an>[A-Za-z][^()]*?)\s*\(\s*(?P<a>\d+)\s*\)\s*(?:and|\+|,)\s*(?:the\s+|a\s+|its\s+)?(?P<bn>[A-Za-z][^()]*?)\s*\(\s*(?P<b>\d+)\s*\)', re.I)
NOTE_BARE = re.compile(r'^(?:The\s+)?(?P<an>[A-Za-z].+?)\s+(?P<a>\d+)\s+and\s+(?:the\s+|a\s+|its\s+)?(?P<bn>[A-Za-z].+?)\s+(?P<b>\d+)\s*[.,;]?$')
# "Award 4 marks for a relevant point and 6 for its developed discussion, total 10."
NOTE_FOR = re.compile(r'\b(?P<a>\d+)\s*(?:marks?\s*)?for\s+(?:a\s+|an\s+|the\s+|its\s+)?(?P<an>[a-z][a-z -]*?)\s+and\s+(?P<b>\d+)\s*(?:marks?\s*)?for\s+(?:a\s+|an\s+|the\s+|its\s+)?(?P<bn>[a-z][a-z -]*?)(?=\s*[,.;]|$)', re.I)
# "Correct tabulation 2, wood 3, insulation 3, external and internal surfaces 2, total resistance 2, U-value 3 (1 for the formula)."
NOTE_LIST_ITEM = re.compile(r'^(?P<n>[A-Za-z][^,]*?)\s+(?P<m>\d+)(?:\s*\([^)]*\))?\.?$')
# "each excellent 4, good 3, fair 2": the ladder every component is placed on.
LADDER = re.compile(r'each\s+excellent\s+(\d+)\s*,\s*good\s+(\d+)\s*,\s*fair\s+(\d+)', re.I)


def slug(word):
    return re.sub(r'[^a-z0-9]+', '-', word.lower()).strip('-')


STOP = {'with', 'from', 'that', 'this', 'into', 'each', 'other', 'their', 'very', 'than', 'then', 'when', 'where', 'which', 'also', 'kept'}
FUNCTION = {'and', 'or', 'of', 'the', 'a', 'an', 'on', 'in', 'to', 'its', 'for', 'with', 'at', 'by', 'from'}
# A participle after the noun it qualifies ("distribution board drawn") is not the phrase's head.
PARTICIPLE = {'drawn', 'annotated', 'shown', 'named', 'sketched', 'labelled', 'identified', 'located', 'justified', 'stated',
              'described', 'explained', 'selected', 'listed', 'given', 'outlined', 'discussed'}


def head(tokens):
    """The phrase's head word: its last alphabetic token, skipping a trailing participle and any formula or units."""
    alpha = [t for t in tokens if re.fullmatch(r'[A-Za-z][A-Za-z-]{2,}', t)]
    while len(alpha) > 1 and alpha[-1].lower() in PARTICIPLE:
        alpha.pop()
    return alpha[-1].lower() if alpha else None


def lift(words, scheme):
    """The longest run of the phrase's words the scheme prints, or None.

    A note may paraphrase the scheme's table ("its supports kept free of insulation" for "Tank supports free of
    insulation"); the part keeps only words the scheme prints (construction_paper.validate asserts this). The run
    must keep the phrase's head word, hold a content word, neither start nor end on a function word, and be two
    words or more unless the phrase itself was; a phrase
    whose head the scheme does not print ("external and internal surfaces" for "External surface / Internal
    surface") leaves its row alone. Nothing is added."""
    tokens = words.split()
    if cp.normalise(words) in scheme:
        return words
    top = head(tokens)
    # A single word is a weak match against a whole scheme ("surfaces" is printed somewhere in every paper):
    # only a phrase of one or two words may shrink to one.
    for size in range(len(tokens) - 1, 1 if len(tokens) > 2 else 0, -1):
        for start in range(0, len(tokens) - size + 1):
            run = tokens[start:start + size]
            if run[0].lower() in FUNCTION or run[-1].lower() in FUNCTION:
                continue
            if top not in [t.lower() for t in run]:
                continue
            content = [t for t in run if len(re.sub(r'[^A-Za-z]', '', t)) >= 4 and t.lower() not in STOP]
            span = ' '.join(run)
            if content and cp.normalise(span) in scheme:
                return span
    return None


def scheme_text(path):
    """The normalised scheme text for a reviewed-paper file, construction_paper's way."""
    year, level = re.search(r'construction-studies-(\d{4})-(higher|ordinary)-reviewed', path.name).groups()
    _, S = cp.sources(int(year), level)
    return cp.normalise(' '.join(cp.page_text(S, p) for p in range(1, cp.page_count(S) + 1)))


def components(row, scheme=None):
    """[(printed word, marks)] the row prices by name, or None. With a scheme, every word is one it prints."""
    found = _components(row)
    if not found or scheme is None:
        return found
    lifted = [(lift(word, scheme), marks) for word, marks in found]
    if any(word is None for word, _ in lifted) or len({slug(word) for word, _ in lifted}) != len(lifted):
        print(f"  left alone {row['id']}: {found}", file=sys.stderr)
        return None
    if lifted != found:
        print(f"  lifted {row['id']}: {found} -> {lifted}", file=sys.stderr)
    return lifted


def _components(row):
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
    allocation = EXAMPLES.split(row.get('contextNote') or '', 1)[0]
    m = NOTE_PAIR.search(allocation)
    if m:
        found = [(m.group('an'), int(m.group('a'))), (m.group('bn'), int(m.group('b')))]
        if sum(marks for _, marks in found) == row['marks'] and len({slug(word) for word, _ in found}) == 2:
            return found
    return note_components(allocation.strip(), row['marks'])


def phrase(words):
    """The component as the note names it: after any lead-in ("For the first wall selected in (b): …") and
    without a leading article or conjunction, so "The tank" is the part "tank"."""
    words = words.rsplit(':', 1)[-1].strip()
    return re.sub(r'^(?:the|a|an|both|and|its)\s+', '', words, flags=re.I).strip()


def note_components(allocation, marks):
    """[(printed phrase, marks)] the note's first sentence prices by name, summing to the row, or None."""
    sentence = re.split(r'(?<=[a-z)])\.\s', allocation, 1)[0].strip()
    for shape in (NOTE_BRACKETED, NOTE_FOR, NOTE_BARE):
        m = shape.search(sentence)
        if not m:
            continue
        found = [(phrase(m.group('an')), int(m.group('a'))), (phrase(m.group('bn')), int(m.group('b')))]
        if sum(x for _, x in found) == marks and len({slug(w) for w, _ in found}) == 2 and all(w for w, _ in found):
            return found
        return None
    pieces = [piece.strip() for piece in sentence.rstrip('.').split(',')]
    if len(pieces) >= 3:
        items = [NOTE_LIST_ITEM.match(piece) for piece in pieces]
        if all(items):
            found = [(phrase(m.group('n')), int(m.group('m'))) for m in items]
            if sum(x for _, x in found) == marks and len({slug(w) for w, _ in found}) == len(found):
                return found
    return None


def steps_for(marks, note):
    m = LADDER.search(note or '')
    if m:
        ladder = sorted({int(x) for x in m.groups()} | {0})
        if ladder[-1] == marks:
            return ladder
    return list(range(marks + 1))


def with_parts(row, scheme=None):
    """The row with its parts, or the row itself when it prices no components."""
    if row.get('kind') != 'criterion' or row.get('parts') or not row.get('permittedMarks'):
        return row
    found = components(row, scheme)
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
        scheme = scheme_text(path)
        for card in cards.values():
            if 'taskGroups' in card:
                continue
            for row in card['rows']:
                with_parts(row, scheme)
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
