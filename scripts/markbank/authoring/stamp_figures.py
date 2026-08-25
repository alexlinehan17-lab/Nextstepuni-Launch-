"""Bind inspected figures to cards, by key, across every subject.

A card whose ask points at printed artwork — "the vernacular cottage shown",
"the diagram below shows how a ray of light travels" — is unanswerable without
it, and `cardlint.py` calls that a ghost-figure. The repair is always the same:
name a figure the manifest already holds (or one a figure pass has just
cropped and bind-figures has published) and let the build resolve it.

The mapping lives in `figure_bindings.json` as {card id: figure key}. Nothing
here writes a path: the build checks the key against the manifest, confirms the
file is on disk and that its bytes still hash to what the inspecting agent saw,
and refuses otherwise. Both historical figure corruptions in this repo entered
through a hand-transcribed path, so a key is all an authoring pass may name.

Re-runnable: authoring scripts rewrite their subject's JSON, which drops the
binding, so this is run after any regeneration.

  python3 stamp_figures.py            # every subject
  python3 stamp_figures.py physics    # one
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AUTHORED = os.path.join(HERE, '..', 'authored')
BINDINGS = os.path.join(HERE, 'figure_bindings.json')
# A lettered question needs its letters DECODED as well as its crop shown, and
# the decode is lifted from the scheme's own naming part. It lives beside the
# bindings for the same reason: an authoring script rewrites its subject's
# JSON and would otherwise drop it.
LABELS = os.path.join(HERE, 'label_keys.json')
MANIFEST = os.path.join(HERE, '..', '..', '..', 'components', 'MarkBank', 'figures.json')

SUBJECTS = ['maths', 'physics', 'biology', 'chemistry', 'economics', 'business',
            'home-economics', 'agricultural-science', 'construction-studies']


def main():
    subjects = sys.argv[1:] or SUBJECTS
    if not os.path.exists(BINDINGS):
        print('no figure_bindings.json — nothing to stamp')
        return 0
    with open(BINDINGS) as fh:
        bind = json.load(fh)
    labels = {}
    if os.path.exists(LABELS):
        with open(LABELS) as fh:
            labels = json.load(fh)
    with open(MANIFEST) as fh:
        manifest = json.load(fh)

    unknown_key = [c for c, k in bind.items() if k not in manifest]
    if unknown_key:
        print(f'REFUSING: {len(unknown_key)} binding(s) name a figure the '
              f'manifest has never inspected, e.g. {unknown_key[:3]}')
        return 1

    total, seen = 0, set()
    for subject in subjects:
        path = os.path.join(AUTHORED, f'{subject}.json')
        if not os.path.exists(path):
            continue
        with open(path) as fh:
            cards = json.load(fh)
        hit = 0
        for c in cards:
            key = bind.get(c['id'])
            if key and c.get('figureKey') != key:
                c['figureKey'] = key
                hit += 1
            if key:
                seen.add(c['id'])
            lk = labels.get(c['id'])
            if lk and c.get('labelKey') != lk:
                c['labelKey'] = lk
                hit += 1
        if hit:
            with open(path, 'w') as fh:
                json.dump(cards, fh, ensure_ascii=False, indent=1)
        total += hit
        if hit:
            print(f'{subject}: bound {hit} card(s)')
    # Only meaningful when every subject was stamped: stamping one subject
    # leaves every other subject's bindings "unseen", which reads as breakage
    # and is not.
    if len(subjects) == len(SUBJECTS):
        orphan = sorted(set(bind) - seen)
        if orphan:
            print(f'WARNING {len(orphan)} binding(s) name no live card: {orphan[:4]}')
    print(f'stamped {total} card(s) from {len(bind)} binding(s)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
