"""Choice is not a route (coordinator rule, 2026-10-12); one printed task is one card (decision 5, 2026-11-04).

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
import copy
import json
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
        return merge_printed_variants(data)
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
    return merge_printed_variants(dict(review=review, cards=kept))


VARIANT = re.compile(r'^(W-[45]B)-(.+)$')
ROGHA = '\n\nAn rogha don chárta seo: '
EXPANDED = re.compile(r'[^.]*(?:\bexpand|separate valid routes)[^.]*\.\s*', re.I)
VARIANT_POLICY = ('One printed task, one card (coordinator decision 5, 2026-11-04): where a Foundation writing task prints '
                  'a tick-box date, a job to choose or a recipient alternative inside ONE task, and every option carries '
                  'the same printed text and the same scheme marking, the task is one card. The options stay in the '
                  'printed text; no card adds a line choosing one.')


def merge_printed_variants(data):
    """Merge each W-4B/W-5B option group whose printed text and marking are identical into one card.

    The option cards differ only by the card-added line "An rogha don chárta seo: …" and the matching
    card-written requirement; everything printed and every criterion is the same, so the group is one
    printed task. Foundation is not on main: the option ids were never live and need no aliases.
    """
    cards = data['cards']
    groups = {}
    for card in cards:
        m = VARIANT.match(card.get('atlasQuestionId', ''))
        if m:
            groups.setdefault(m.group(1), []).append(card)
    if not groups:
        return data
    out, emitted, renamed, records = [], set(), {}, []
    for card in cards:
        m = VARIANT.match(card.get('atlasQuestionId', ''))
        if not m:
            out.append(card)
            continue
        key = m.group(1)
        if key in emitted:
            continue
        members = groups[key]
        assert len(members) >= 2, ('A single option is not a variant group', card['id'])
        assert all(ROGHA in mem['questionText'] for mem in members), ('Option line missing', key)
        printed = {mem['questionText'].split(ROGHA, 1)[0] for mem in members}
        assert len(printed) == 1, ('Option cards print different text', key)
        assert len({json.dumps(mem['criteria'], sort_keys=True, ensure_ascii=False) for mem in members}) == 1, ('Option cards are marked differently', key)
        varying = {'id', 'atlasQuestionId', 'questionRef', 'questionText', 'taskRequirements', 'markingGuideNote', 'conceptId', 'sourceMaterial'}
        for field in set().union(*members) - varying:
            assert len({json.dumps(mem.get(field), sort_keys=True, ensure_ascii=False) for mem in members}) == 1, ('Option cards differ in', key, field)
        # The source reader names the option in its label and title only; its pages and regions are one document.
        bare = lambda material: {k: v for k, v in (material or {}).items() if k not in ('label', 'title')}
        assert len({json.dumps(bare(mem.get('sourceMaterial')), sort_keys=True, ensure_ascii=False) for mem in members}) == 1, ('Option cards show different sources', key)
        suffixes = [VARIANT.match(mem['atlasQuestionId']).group(2) for mem in members]
        ids = [mem['id'][:-len('-' + suffix)] for mem, suffix in zip(members, suffixes)]
        assert all(mem['id'].endswith('-' + suffix) for mem, suffix in zip(members, suffixes)) and len(set(ids)) == 1, key
        refs = [mem['questionRef'].rsplit(' · ', 1) for mem in members]
        assert len({ref[0] for ref in refs}) == 1, key
        merged = copy.deepcopy(members[0])
        merged['id'] = ids[0]
        merged['atlasQuestionId'] = key
        merged['questionRef'] = refs[0][0]
        merged['questionText'] = printed.pop()
        if merged.get('sourceMaterial'):
            for field in ('label', 'title'):
                if len({mem['sourceMaterial'].get(field) for mem in members}) == 1:
                    continue  # the reader already names the whole task
                values = {mem['sourceMaterial'].get(field, '').rsplit(' · ', 1)[0] for mem in members}
                if merged['sourceMaterial'].get(field):
                    assert len(values) == 1 and all(mem['sourceMaterial'][field].endswith(' · ' + ref[1]) for mem, ref in zip(members, [m['questionRef'].rsplit(' · ', 1) for m in members])), (key, field)
                    merged['sourceMaterial'][field] = values.pop()
        merged['taskRequirements'] = [r for r in members[0]['taskRequirements'] if all(r in mem['taskRequirements'] for mem in members)]
        concepts = {mem['conceptId'] for mem in members}
        if len(concepts) > 1:
            merged['conceptId'] = members[0]['conceptId'].replace('-' + suffixes[0], '')
        options = [ref[1] for ref in refs]
        note = re.sub(r'\s+', ' ', EXPANDED.sub(' ', members[0]['markingGuideNote'])).strip()
        merged['markingGuideNote'] = (note + ' ' if note else '') + (
            f'The printed options ({", ".join(options)}) are a choice inside this one task, so one card carries the whole task.')
        out.append(merged)
        emitted.add(key)
        records.append(dict(cardId=merged['id'], atlasQuestionId=key, withdrawnOptionCardIds=[mem['id'] for mem in members], printedOptions=options))
        for mem in members:
            renamed[mem['id']] = merged['id']
    review = dict(data['review'])
    for field in ('atomicPracticeCardIds',):
        if field in review:
            seen = []
            for cid in review[field]:
                cid = renamed.get(cid, cid)
                if cid not in seen:
                    seen.append(cid)
            review[field] = seen
    review['variantPolicy'] = VARIANT_POLICY
    review['variantMerges'] = records
    return dict(review=review, cards=out)
