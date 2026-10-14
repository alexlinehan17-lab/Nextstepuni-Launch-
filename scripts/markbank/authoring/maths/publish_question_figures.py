"""Publish inspected printed-question crops for whole Mathematics sittings.

    python3 scripts/markbank/authoring/maths/publish_question_figures.py 2020 2019 2018 2017
    python3 scripts/markbank/authoring/maths/publish_question_figures.py 2016-hl-p1      (one paper)

maths_question_figures.py writes each crop to exam-papers/maths/figures/<year>-<lv>/
and records it in scripts/markbank/authored/maths-question-figures-catalogue.json.
After every crop of a sitting has been opened and checked, this copies the crops
to public/exam-figures/maths/markbank/ and enters them in
components/MarkBank/figures.json in exactly the shape bind-figures.mjs writes.

The entries are inserted textually rather than by rewriting the whole object:
figures.json mixes escaped and raw Unicode from earlier writers, and a full
rewrite would restyle thousands of unrelated lines in a file every subject
shares (the same reason scheme_row_figures.py --publish inserts textually).

A name already published with the same bytes is left alone; a name already
published with DIFFERENT bytes is refused, and so is a crop whose bytes are
already published under another name.
"""
import hashlib
import json
import os
import shutil
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
CATALOGUE = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'maths-question-figures-catalogue.json')
MANIFEST = os.path.join(ROOT, 'components', 'MarkBank', 'figures.json')
DEST = os.path.join(ROOT, 'public', 'exam-figures', 'maths', 'markbank')


def main(years):
    raw = open(MANIFEST, encoding='utf-8').read()
    manifest = json.loads(raw)
    by_md5 = {v['md5']: k for k, v in manifest.items()}
    added, kept = [], 0
    for e in json.load(open(CATALOGUE)):
        name = e['file'][:-4]
        parts = name.split('-')            # maths-<year>-<LV>-ask-p<N>-...
        paper = f'{parts[1]}-{parts[2].lower()}-{parts[4]}'
        if parts[3] != 'ask' or not (parts[1] in years or paper in years):
            continue
        year, lv = parts[1], parts[2].lower()
        assert e['kind'] == 'figure' and not e['truncated'], name
        src = os.path.join(ROOT, 'exam-papers', 'maths', 'figures', f'{year}-{lv}', e['file'])
        md5 = hashlib.md5(open(src, 'rb').read()).hexdigest()
        if name in manifest:
            if manifest[name]['md5'] != md5:
                raise SystemExit(f'{name}: already published with different bytes')
            kept += 1
            continue
        if md5 in by_md5:
            raise SystemExit(f'{name}: identical bytes to {by_md5[md5]}')
        by_md5[md5] = name
        shutil.copyfile(src, os.path.join(DEST, e['file']))
        word = 'Higher' if lv == 'hl' else 'Ordinary'
        added.append((name, {
            'src': f'/exam-figures/maths/markbank/{e["file"]}', 'md5': md5, 'alt': e['description'],
            'lettersVisible': [], 'labelMeanings': [], 'questionRef': e.get('questionRef', ''),
            'year': int(year), 'level': 'higher' if lv == 'hl' else 'ordinary',
            'attribution': f'SEC Leaving Certificate Mathematics {year} {word} Level — © State Examinations Commission',
        }))
    if added:
        tail = raw.rstrip()
        assert tail.endswith('}\n}'), 'unexpected manifest ending'
        block = ''.join(',\n ' + json.dumps(k, ensure_ascii=False) + ': '
                        + json.dumps(v, ensure_ascii=False, indent=1).replace('\n', '\n ')
                        for k, v in added)
        out = tail[:-2] + block + '\n}\n'
        assert json.loads(out) == {**manifest, **dict(added)}
        open(MANIFEST, 'w', encoding='utf-8').write(out)
    print(f'published {len(added)} question crops; {kept} already published unchanged')


if __name__ == '__main__':
    main(set(sys.argv[1:]))
