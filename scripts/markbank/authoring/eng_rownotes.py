"""Engineering card notes a student must see, set on the row they qualify.

    python3 scripts/markbank/authoring/eng_rownotes.py   # every note this pass sets, by card

A card's `notes` never ship: build-deck.mjs strips them, and a question card
has no field to show one. Some of those notes are the author's record ("The
scheme prints '5'."); others tell the STUDENT something about the marking or
the printed page. Examples of the second kind:

  * Section B's "12 + 12 + 11": the third part answered earns 11.
  * Two (c)s set either side of an OR, and where the other branch's answers are.
  * "2 + 2" read as one property from each column.
  * A sentence the scheme prints that is on no row ("These methods will prevent
    the oxygen in the air attacking the metal surface.").
  * A misprint, a misnumbering or a word missing as printed.

Those notes are copied onto a row's `contextNote`, which every row renders
(SessionScreen: point, alternative, any-N group, whole-response, ask and
criterion rows alike). The card-level note stays as it is.

Which sentences go, and how they read:

* A sentence is the author's record, and stays off the card, when it only
  echoes a price ("The scheme prints '3 + 2', for (i) and (ii) in that
  order.", "Section A is 'Any ten @ 5 marks each'.") or describes the
  extraction (a table's head and cell joined). A price echo goes only where
  the card already shows that price.
* A sentence that READS the scheme ("read here as", "without saying which"),
  quotes scheme text no row carries, or reports the printed page goes on the
  card.
* Lane words become plain words. "carded at the letter" means answered on one
  card; "each branch a route" means both branches on this card, claimed one
  at a time. The words a note quotes from the paper or scheme are unchanged.
* The note sits on the row that holds a string it quotes, where exactly one
  row does ('Aiuminium', 'goggles'); otherwise on the first row.

Engineering only: eng_all.py runs this last, after eng_lists.
"""
import json
import os
import re
import sys

# A quoted tariff: digits, "Award", "Marks" or "@". A quoted SENTENCE (no
# digit) is scheme text and is not a price.
PRICE = r"'(?=[^']*(?:\d|Award|Marks|@))[^']*'"

# Sentences that READ the scheme, or quote it: always student-facing.
KEEP = re.compile(
    r"read here as|without saying|any one advantage|advantages and disadvantages"
    r"|opens:|adds|after the methods|[Ss]uggested|Alternative suggestions"
    r"|other feasible|two parts (?:here|at)|one here|its marks grid prints"
    r"|its grid prints|under the answer")

# Sentences that only echo a price, or describe the extraction.
PROVENANCE = [
    re.compile(rf"^The scheme prints {PRICE}(?:,? (?:and|or) (?:, for the OR, )?{PRICE})*"
               rf"(?:,? (?:under|for|beside|after) [^:;]*?)?(?:, (?:for|in) [^:;]*?)?\.$"),
    re.compile(rf"^The scheme prints {PRICE}(?: and, for the OR, {PRICE})?\.$"),
    re.compile(rf"^The scheme prints {PRICE}: each part answered earns \d+\.$"),
    re.compile(rf"^The scheme prints {PRICE}, \d+ for each part answered\.$"),
    re.compile(rf"^The scheme prints {PRICE}, \d+ marks\.$"),
    re.compile(rf"^The scheme prints {PRICE}(?:,)? \d+ for each process\.$"),
    re.compile(rf"^The scheme prints {PRICE} (?:under|for) [^.]*? and {PRICE} (?:under|for) [^.]*?\.$"),
    re.compile(rf"^The scheme prints {PRICE} \(under the box's heading '[^']*'\)\.$"),
    re.compile(rf"^The scheme prints {PRICE}, after '[^']*'$"),
    re.compile(rf"^The scheme prints (?:{PRICE}(?: and |, )?)+, for the (?:furnace|process|mechanism) "
               rf"(?:chosen|selected)\.$"),
    re.compile(rf"^The scheme prints {PRICE} for \(b\): each part answered earns \d+\.$"),
    re.compile(r"^The scheme prints '[^']*'(?: and '\d+'|, \d+ marks)\.$"),
    re.compile(r"^Section [AB] is ['\"][^'\"]*['\"]\.$"),
    re.compile(r"^Question \d+ is '[^']*'\.$"),
    re.compile(r"^Its table is headed .*"),
    re.compile(r"^The scheme answers in a table, .*"),
    re.compile(r"^The scheme's grid prints .*"),
    re.compile(r"^The scheme's marks grid prints .*"),
]

# Lane words, as plain words. Applied in order; quoted words never match.
PLAIN = [
    (r", so they are one card, each branch a route\.",
     ", so both branches are on this card: claim the rows for the branch you answered."),
    (r", so each roman is one card, each branch a route\.",
     ", so this card holds this part of both branches: claim the rows for the branch you "
     "answered."),
    (r"; priced differently, each branch is carded on its own\.",
     "; priced differently, each branch has its own cards."),
    (r", so each branch is a card of its own\.", ", so each branch has its own cards."),
    (r"are carded together at the letter", "are answered together on one card"),
    (r"answered at the letter for (\d+)", r"answered as one part for \1"),
    (r"for 16, answered at the letter", "for 16, answered as one part"),
    (r"carded at the letter", "answered on one card"),
    (r"are carded apart", "each have a card of their own"),
    (r"one card for each (symbol|component) (drawn|photographed) and captioned \(i\)-\(iii\)",
     r"each \1 \2 and captioned (i)-(iii) on a card of its own"),
    (r"\(iv\) is carded on its own\.", "(iv) has a card of its own."),
    (r"the card carries", "this card shows"),
    (r"a part earns answered first or second; answered third it earns",
     "a part earns answered first or second; a part answered third earns"),
    (r"two parts here, one at", "two parts on this card, one at"),
    (r"two parts at \((i)\), one here", r"two parts at (\1), one on this card"),
    (r"the chip at C is one paragraph, carried whole", "its answer on the chip at C is one paragraph, shown whole"),
    (r"^It (numbers|spells) ", r"The scheme \1 "),
    (r"^Its (second )?sentence ", r"The scheme's \1sentence "),
    (r"^The scheme prints (?:{p})(?:,? [^':]*?)?,? and (opens|adds)".format(p=PRICE), r"The scheme \1"),
    (r"^The scheme prints (?:{p}), and after the methods:".format(p=PRICE),
     "After the methods, the scheme prints:"),
    (r"^The scheme prints (?:{p}),? and '(?![^']*(?:\d|Award|Marks|@))".format(p=PRICE),
     "The scheme prints '"),
]

# A note the rules above would read wrongly, set by hand. None keeps a card's
# note off the card. Text here is ours, around words lifted from the page.
OVERRIDES = {
    # The paper asks how XR could benefit the environment; the scheme's list is
    # examples of XR, under its own lead-in.
    'eng-2023-hl-deferred-q2-a-ii':
        "The scheme answers with examples of extended reality, under the heading "
        "'Examples of Extended Reality include:'",
    # The lift itself is the author's record; what the student needs is that
    # the note is the scheme's own.
    'eng-2014-hl-q1-h': "The scheme's note on Marie Curie is shown as printed.",
    # Price splits the rows already show, row by row.
    'eng-2010-hl-q2-a-ii': None,   # 'Purpose 4', 'Operation 6': rows at 4 and 6
    'eng-2015-hl-q4-a': None,      # names and descriptions: rows at 4 each
    'eng-2015-hl-q6-c-i': None,    # structure and property: rows at 2 each
}


def sentences(text):
    """Split at '. X' or '; X' outside quotes ('…', "…", “…”)."""
    out, cur, quote = [], '', None
    closing = {"'": "'", '"': '"', '“': '”'}
    i = 0
    while i < len(text):
        ch = text[i]
        prev = text[i - 1] if i else ' '
        nxt = text[i + 1] if i + 1 < len(text) else ' '
        if quote is None and ch in closing and prev in ' (:':
            quote = closing[ch]
        elif quote is not None and ch == quote and (nxt in ' .,;:)' or i + 1 == len(text)):
            quote = None
        cur += ch
        after = text[i + 2:i + 4]
        opens = after[:1].isupper() or (after[:1] in '\'"\u201c' and after[1:2].isupper())
        if quote is None and ch in '.;' and nxt == ' ' and opens:
            out.append(cur.strip())
            cur = ''
            i += 1
        i += 1
    if cur.strip():
        out.append(cur.strip())
    return out


def plain(sentence):
    for pat, rep in PLAIN:
        sentence = re.sub(pat, rep, sentence)
    return sentence


def student_note(card):
    """The part of a card's note a student must see, in plain words, or None."""
    if card['id'] in OVERRIDES:
        return OVERRIDES[card['id']]
    keep = []
    for s in sentences(card.get('notes') or ''):
        if not KEEP.search(s) and any(p.match(s) for p in PROVENANCE):
            continue
        keep.append(plain(s))
    return ' '.join(keep) or None


def _row_text(row):
    parts = [row.get('verbatim') or '']
    parts += row.get('accepts') or []
    parts += (row.get('group') or {}).get('options') or []
    return ' '.join(parts)


def row_for(card, note):
    """The row a note is about: the one row holding a string it quotes."""
    rows = card['rows']
    for quoted in re.findall(r"'([^']{4,})'|\"([^\"]{4,})\"", note):
        quoted = quoted[0] or quoted[1]
        hits = [i for i, r in enumerate(rows) if quoted in _row_text(r)]
        if len(hits) == 1:
            return hits[0]
    return 0


ROUTES = ' Both branches are on this card: claim the rows for the branch you answered.'


def with_routes(card, note):
    """An OR card whose rows carry both branches says how to claim them."""
    if 'either side of an OR' in note and 'claim the rows' not in note \
            and any(r.get('route') for r in card['rows']):
        return note + ROUTES
    return note


def promote(cards):
    """Set each card's student-facing note on its row. Returns {card id: note}."""
    set_ = {}
    for card in cards:
        note = student_note(card)
        if not note or not card.get('rows'):
            continue
        note = with_routes(card, note)
        row = card['rows'][row_for(card, note)]
        have = (row.get('contextNote') or '').strip()
        if note in have:
            continue
        row['contextNote'] = f'{have} {note}'.strip()
        set_[card['id']] = note
    return set_


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, '..', 'authored', 'engineering.json')
    cards = json.load(open(sys.argv[1] if len(sys.argv) > 1 else path, encoding='utf-8'))
    shown = {}
    for card in cards:
        note = student_note(card)
        if note:
            shown.setdefault(with_routes(card, note), []).append(card['id'])
    for note, ids in sorted(shown.items(), key=lambda kv: kv[1][0]):
        print(f'{len(ids)} {", ".join(ids)}\n    {note}')
    print(f'{sum(len(v) for v in shown.values())} cards, {len(shown)} notes', file=sys.stderr)
