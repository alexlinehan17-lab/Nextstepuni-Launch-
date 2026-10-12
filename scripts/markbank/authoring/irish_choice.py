"""Choice is not a route (coordinator rule, 2026-10-12).

When the candidate chooses which printed options to answer ("Freagair do rogha
dhá cheann …", "Freagair dhá cheist ar bith …", "(a) NÓ (b)"), no per-combination
card is published: sessions do not collapse route siblings, so every combination
would be a separate card. Each printed option keeps its own card with its own
scheme marking, and the printed choice instruction travels in that card's task
requirements. A scheme that marked a combination JOINTLY would instead need one
card with slot criteria; no Irish paper reviewed so far does (each option has its
own award), and `withdraw_combinations` refuses a combination whose criteria are
not exactly its members' criteria.
"""
from __future__ import annotations
import re

POLICY = ('Choice is not a route (2026-10-12): when the candidate chooses which printed options to answer, no per-combination '
          'cards are published. Each printed option keeps its own card with its own scheme marking, and the printed choice '
          'instruction is carried in that card’s task requirements. Selection decisions that describe pair or product '
          'expansions record how the paper was read; the expansions themselves are withdrawn.')


def choice_instruction(card):
    """The printed instruction a combination card quoted ahead of “An rogha don chárta seo”."""
    text = card['questionText'].split('\n\nAn rogha don chárta seo', 1)[0].strip()
    return re.sub(r'\s*\n+\s*', ' ', text)


def withdraw_combinations(data):
    """Drop every card with memberCardIds; carry its instruction into each member's task requirements."""
    cards = data['cards']
    combos = [c for c in cards if c.get('memberCardIds')]
    if not combos:
        return data
    kept = [c for c in cards if not c.get('memberCardIds')]
    by_id = {c['id']: c for c in kept}
    for combo in combos:
        members = [by_id[mid] for mid in combo['memberCardIds']]  # every option is published on its own
        # Jointly marked combinations would need slot criteria instead: refuse anything but a plain union.
        member_awards = sum(cr['maxMarks'] for m in members for cr in m['criteria'] if cr['kind'] == 'award')
        combo_awards = sum(cr['maxMarks'] for cr in combo['criteria'] if cr['kind'] == 'award')
        assert member_awards == combo_awards, ('Combination is not a plain union of its options', combo['id'])
        instruction = choice_instruction(combo)
        assert instruction and 'An rogha' not in instruction, combo['id']
        for member in members:
            member['taskRequirements'] = [instruction] + [r for r in member.get('taskRequirements', []) if r != instruction]
    review = dict(data['review'])
    review.pop('pairedRouteCardIds', None)
    if 'boundaries' in review:
        review['boundaries'] = (f'{len(kept)} individually marked task/option cards; {len(combos)} per-combination cards '
                                'withdrawn (choice is not a route).')
    review['choicePolicy'] = POLICY
    return dict(review=review, cards=kept)
