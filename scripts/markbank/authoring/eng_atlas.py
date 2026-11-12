#!/usr/bin/env python3
"""Bind every Engineering card of a sitting to its Topic Atlas question.

    python3 scripts/markbank/authoring/eng_atlas.py 2021 hl            # report
    python3 scripts/markbank/authoring/eng_atlas.py 2021 hl --write    # write the review

The Atlas files each printed QUESTION under topics from a factual reference
whose headings are part-level ("2021 - Question 1 - Part K"), and each of
those topics names the syllabus headings it covers (its curriculum nodes,
engineering-curriculum-crosswalk.json). A Mark Bank card is filed under one
syllabus heading. So a card resolves under the right Atlas topic when its
question is filed under a topic whose nodes include the card's heading -- and
where the reference files the card's own LETTER under such a topic, that one
is preferred.

Where no topic of the question covers the card's heading, nothing is guessed:
the sitting's eng_residue module says, card by card in ATLAS, which topic of
that level the content belongs to and why, and the crosswalk build adds it to
the question (build-engineering-exam-topic-crosswalk.mjs reads the review this
writes). The review is what test/markBankTopicAtlas.test.ts checks: every card
of the sitting is bound, every bound topic is the card's level, and the Atlas
really lists the card's question under it.
"""
import argparse
import collections
import datetime
import hashlib
import json
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

import eng_residue                                          # noqa: E402

FILEID = {'hl': 'LC027ALP000EV.pdf', 'ol': 'LC027GLP000EV.pdf'}
LEVEL = {'hl': 'higher', 'ol': 'ordinary'}


def load(path):
    with open(os.path.join(ROOT, path), encoding='utf-8') as fh:
        return json.load(fh)


def tail_letters(tail):
    """The part letters a reference heading's tail names: ' - Part A,B',
    ' - Part A-C', ' - Part C2' (the second printing of (c)), ' - Part (c) 1'."""
    t = (tail or '').replace(' - Part ', '', 1).strip()
    if not t:
        return set()
    head = re.split(r'\s+-\s+', t)[0]
    out = set()
    for m in re.finditer(r'\(?([A-Ma-m])\)?\s*-\s*\(?([A-Ma-m])\)?', head):
        a, b = m.group(1).lower(), m.group(2).lower()
        out |= {chr(c) for c in range(ord(a), ord(b) + 1)}
    for m in re.finditer(r'\(?\b([A-Ma-m])\b\)?', head):
        out.add(m.group(1).lower())
    return out


def deck_ids(level):
    path = os.path.join(ROOT, 'components/MarkBank/cards/engineering',
                        f'{LEVEL[level]}.ts')
    with open(path, encoding='utf-8') as fh:
        return set(re.findall(r'\bid: "(eng-[^"]+)"', fh.read()))


def sha(path):
    with open(os.path.join(ROOT, path), 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('level', choices=('hl', 'ol'))
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    year, level = args.year, args.level
    lvl = LEVEL[level]

    reference = load('data/examTopics/engineering.json')
    crosswalk = load('data/examTopics/engineering-curriculum-crosswalk.json')
    topics = {}
    for variant, v in reference['variants'].items():
        for t in v['topics']:
            topics[t['id']] = dict(label=t['label'], variant=variant,
                                   level='higher' if variant.startswith('higher') else 'ordinary',
                                   course='new' if variant.endswith('new-course') else 'old',
                                   nodes=crosswalk[t['id']])
    by_label = {(t['level'], t['course'], t['label']): tid for tid, t in topics.items()}
    assoc = collections.defaultdict(list)          # n -> [(topic, letters)]
    for a in load('data/examTopics/engineering-local-crosswalk.json')['associations']:
        if a['resolution'] != 'matched':
            continue
        tg = a['target']
        if tg['year'] == year and tg['level'] == lvl and tg['lang'] == 'ev':
            assoc[tg['questionNumber']].append((a['topicId'], tail_letters(a.get('tail'))))

    mod = eng_residue.module(year, level)
    choices = getattr(mod, 'ATLAS', {}) if mod else {}
    live = deck_ids(level)
    cards = [c for c in load('scripts/markbank/authored/engineering.json')
             if c['year'] == year and c['level'] == lvl and c['id'] in live]
    unbuilt = sorted(i for i in live if i.startswith(f'eng-{year}-{level}-')
                     and i not in {c['id'] for c in cards})
    if unbuilt:
        raise SystemExit(f'deck holds cards the authored file does not: {unbuilt}')

    def resolve_topic(name):
        if name in topics:
            return name
        tid = by_label.get((lvl, 'old', name))
        if not tid:
            raise SystemExit(f'ATLAS names an unknown {lvl} outgoing topic {name!r}')
        return tid

    bindings, review, questions = [], [], collections.defaultdict(set)
    for c in sorted(cards, key=lambda c: c['id']):
        m = re.match(r'\d{4} [HO]L Q(\d+)(?:\(([a-m])\))?', c['questionRef'])
        n, letter = m.group(1), m.group(2)
        old = [(t, ls) for t, ls in assoc[n]
               if topics[t]['level'] == lvl and topics[t]['course'] == 'old']
        node = [t for t, _ in old if c['topicId'] in topics[t]['nodes']]
        part = [t for t, ls in old if letter and letter in ls]
        entry = {'cardId': c['id'], 'markBankTopicId': c['topicId'],
                 'questionNumber': n}
        if c['id'] in choices:
            ch = choices[c['id']]
            chosen = [resolve_topic(t) for t in ch['topics']]
            for tid in chosen:
                if topics[tid]['level'] != lvl:
                    raise SystemExit(f'{c["id"]}: {tid} is not a {lvl} topic')
            entry['atlasTopicIds'] = chosen
            entry['canonicalTopicReview'] = ch['note']
            added = [t for t in chosen if t not in {x for x, _ in old}]
            if added:
                entry['addedToQuestion'] = added
        elif node:
            entry['atlasTopicIds'] = sorted(set(t for t in node if t in part) or set(node))
        else:
            review.append((c, old, part))
            continue
        bindings.append(entry)
        questions[n] |= set(entry['atlasTopicIds'])

    print(f'{year} {level}: {len(cards)} cards, {len(bindings)} bound, '
          f'{len(review)} need an ATLAS choice')
    for c, old, part in review:
        print(f'  {c["id"]}  [{c["topicId"]}] {c["questionText"][:110]!r}')
        print(f'      question topics: ' + '; '.join(
            f'{topics[t]["label"]}{" *" if t in part else ""} {topics[t]["nodes"]}'
            for t, _ in old))
    if review or not args.write:
        return 1 if review else 0
    paper = f'paper-trail-corpus/exampapers/{year}/{FILEID[level]}'
    scheme = f'paper-trail-corpus/markingschemes/{year}/{FILEID[level]}'
    added = sum(1 for b in bindings if b.get('addedToQuestion'))
    out = {
        'schemaVersion': 1, 'subjectId': 'engineering', 'year': year, 'level': lvl,
        'lang': 'ev', 'sitting': 'main', 'paperKey': 'single',
        'reviewedAt': datetime.date.today().isoformat(),
        'authoringReview': f'scripts/markbank/authoring/eng_residue/y{year}_{level}.py',
        'sourceHashes': {paper: sha(paper), scheme: sha(scheme)},
        'expectedRuntimeCards': len(bindings),
        'reason': (f'{year} {lvl.capitalize()} main English written paper: every one of the '
                   f'{len(bindings)} Mark Bank cards bound to its printed question and to the '
                   f'Atlas topics whose syllabus headings include the card\'s own; {added} '
                   f'bound under a topic the reference did not give the question, each with '
                   f'its review.'),
        'questions': [{'n': n, 'fileid': FILEID[level], 'topicIds': sorted(questions[n])}
                      for n in sorted(questions, key=int)],
        'cards': bindings,
    }
    path = os.path.join(ROOT, 'scripts/markbank/atlas-reviews',
                        f'engineering-{year}-{lvl}.json')
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    print(f'wrote {os.path.relpath(path, ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
