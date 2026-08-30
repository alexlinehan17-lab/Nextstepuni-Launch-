#!/usr/bin/env python3
"""Give a card that POINTS AT printed matter the crop of it.

    python3 scripts/markbank/attach-question-figures.py            # report
    python3 scripts/markbank/attach-question-figures.py --write

A card that says "From your diagram above, explain how excess demand occurs"
or "Name the stage of mitosis shown in the diagram" cannot be answered by
someone who cannot see the diagram. 544 cards across the eleven decks read
that way, and for most of them the SEC's own crop was already published in
components/MarkBank/figures.json against the same question — bound to a
sibling card, or extracted and never used.

This attaches it as the QUESTION-side figure, which is the slot the deck
already has for exactly this: "the SEC's own print of the ask and its setup,
shown before the reveal. Unlike an answer figure it may legitimately be shared
context across sibling cards, so it skips the one-crop-one-card rule; and it
must never be a solution crop, which would print the answer in the question
area."

Done as one pass over the authored files rather than inside forty subject
authors, because the rule is the same everywhere and the fault is the same
everywhere: the crop existed and nothing joined it to the card.

WHAT IT WILL NOT DO:

  * attach a SOLUTION crop -- that prints the answer above the question;
  * attach to a card that already carries a figure of its own;
  * attach a crop from a different question. The join is card to card WITHIN
    one question: if a sibling part already carries a crop, this part may
    share it, because a stimulus printed once at the head of a question
    belongs to every part under it. Economics 2021 HL Q13(a)(i) carries the
    PlayStation 5 supply-and-demand axes and (a)(ii) says "From your diagram
    above" with nothing above it.

    The manifest's own questionRef is not usable for this: it is EMPTY on that
    figure and on many others, so a lookup keyed on it finds nothing. What a
    card carries is recorded on the card;
  * invent a crop. Where none is published the card is REPORTED, not altered,
    and the subject needs a figure pass before those cards can be honest.
"""
import argparse
import collections
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AUTHORED = os.path.join(ROOT, 'scripts', 'markbank', 'authored')
MANIFEST = os.path.join(ROOT, 'components', 'MarkBank', 'figures.json')

# A reference to something PRINTED that the card would have to show. Not every
# mention of a diagram: "draw a diagram of the heart" asks the student to make
# one and needs nothing shown, which is why the pointer words -- above, below,
# shown, opposite -- are required rather than the noun alone.
POINTS_AT = re.compile(
    r'\b(?:from your |in your |the )?(?:diagram|graph|chart|sketch|figure|fig\.?'
    r'|table|photograph|photo|image|picture|drawing|flowchart|map|extract'
    r'|passage|text|cartoon|label(?:led)?)\b[^.]{0,40}?'
    r'\b(?:above|below|shown|opposite|following|provided|supplied|attached)\b'
    r'|\b(?:above|below|opposite|shown)\b[^.]{0,20}\b(?:diagram|graph|table|figure)\b'
    r'|\bfrom (?:your|the) (?:diagram|graph|table|figure)\b'
    r'|\btick\b[^.]{0,30}\b(?:box|table|column)\b'
    r'|\brefer(?:ring)? to the (?:diagram|graph|table|figure|extract|passage)\b',
    re.I)
PART = re.compile(r'\s*\([a-z]\)(?:\([ivxlc]+\))?\s*$', re.I)
ROMAN = re.compile(r'\s*\([ivxlc]+\)\s*$', re.I)


def refs_above(ref):
    """The card's own ref, then each shallower ref it sits inside."""
    out = [ref]
    prev = None
    while out[-1] != prev:
        prev = out[-1]
        nxt = ROMAN.sub('', prev).strip()
        if nxt == prev:
            nxt = PART.sub('', prev).strip()
        if nxt != prev and nxt:
            out.append(nxt)
    return out


def question_of(ref):
    """"2021 HL Q13(a)(ii)" -> "2021 HL Q13". The question a part sits in."""
    out = ref
    while True:
        nxt = PART.sub('', ROMAN.sub('', out)).strip()
        if nxt == out:
            return out
        out = nxt


def card_text(card):
    bits = [card.get('questionText') or '', card.get('stem') or '']
    return ' '.join(' '.join(bits).split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--from-catalogue',
                    help='a question_art.py catalogue: attach each crop to the '
                         'card it was cropped FOR, by id')
    ap.add_argument('subjects', nargs='*')
    args = ap.parse_args()

    manifest = json.load(open(MANIFEST, encoding='utf-8'))
    solution = {k for k, v in manifest.items() if v.get('solution')}

    # A crop cut FOR a named card, by question_art.py. Joined by id rather
    # than by ref, because that is what the cropper recorded and it cannot be
    # ambiguous.
    for_card = {}
    if args.from_catalogue:
        for entry in json.load(open(args.from_catalogue, encoding='utf-8')):
            key = entry['file'][:-4]
            if entry.get('cardId') and key in manifest:
                for_card[entry['cardId']] = key

    # The eleven files build-deck consumes. The authored directory also holds
    # working lists -- "-figures", "-held", "-skipped", "-script-ids" -- and
    # some of those are lists of strings rather than cards.
    DECKS = ['agricultural-science', 'biology', 'business', 'chemistry',
             'computer-science', 'construction-studies', 'economics',
             'engineering', 'home-economics', 'maths', 'physics']
    files = [f'{s}.json' for s in DECKS
             if not args.subjects or s in args.subjects]

    attached = collections.Counter()
    orphaned = collections.Counter()
    examples = collections.defaultdict(list)
    for name in files:
        subject = name[:-5]
        path = os.path.join(AUTHORED, name)
        cards = json.load(open(path, encoding='utf-8'))
        # What each QUESTION's cards already carry between them.
        by_question = collections.defaultdict(set)
        for card in cards:
            key = card.get('figureKey') or card.get('questionFigureKey')
            if key and key not in solution:
                by_question[question_of(card.get('questionRef') or '')].add(key)
        changed = 0
        for card in cards:
            if card.get('figureKey') or card.get('questionFigureKey'):
                continue
            text = card_text(card)
            if not POINTS_AT.search(text):
                continue
            if card['id'] in for_card:
                attached[subject] += 1
                changed += 1
                if args.write:
                    card['questionFigureKey'] = for_card[card['id']]
                continue
            siblings = by_question.get(question_of(card.get('questionRef') or ''))
            # ONE crop for the question is unambiguous. Where its parts carry
            # several, this card cannot choose between them and is left for a
            # figure pass to bind deliberately.
            found = next(iter(siblings)) if siblings and len(siblings) == 1 else None
            if found:
                attached[subject] += 1
                changed += 1
                if args.write:
                    card['questionFigureKey'] = found
            else:
                orphaned[subject] += 1
                if len(examples[subject]) < 3:
                    examples[subject].append(f'{card["id"]} — {text[:70]}')
        if args.write and changed:
            with open(path, 'w', encoding='utf-8') as fh:
                json.dump(cards, fh, ensure_ascii=False, indent=1)
                fh.write('\n')

    width = max((len(s) for s in set(attached) | set(orphaned)), default=10)
    print(f'{"subject":{width}}  {"attached":>9}  {"still bare":>10}')
    for subject in sorted(set(attached) | set(orphaned)):
        print(f'{subject:{width}}  {attached[subject]:>9}  {orphaned[subject]:>10}')
    print(f'{"TOTAL":{width}}  {sum(attached.values()):>9}  '
          f'{sum(orphaned.values()):>10}')
    if not args.write:
        print('\n(report only — pass --write to attach)')
    print('\nstill bare, by subject:')
    for subject in sorted(examples):
        print(f'  {subject}')
        for e in examples[subject]:
            print(f'     {e}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
