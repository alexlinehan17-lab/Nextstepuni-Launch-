#!/usr/bin/env python3
"""
dv_apply.py — Diagram Vault extraction, stage 3 (apply verified figures).

Reads the agent-verified JSON (stage 2), copies each accepted crop into
public/exam-figures/<subject>/, and (re)writes data/diagramVault/figures/
<subject>.ts as a list of `nf({...})` entries. The integrity gate then covers
them (file exists + SEC source + unique id).

Usage:
  python3 tools/dv_apply.py <subjectId> <verified.json> [<verified2.json> ...]
"""
import sys, os, json, shutil, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ident(subject):
    return re.sub(r'[^A-Za-z0-9]', '_', subject).upper()


def js(v):
    if v is None:
        return 'null'
    if isinstance(v, (int, float)):
        return str(v)
    return json.dumps(v, ensure_ascii=False)


def main():
    subject = sys.argv[1]
    files = sys.argv[2:]
    fig_dir = os.path.join(REPO, 'public', 'exam-figures', subject)
    os.makedirs(fig_dir, exist_ok=True)

    entries = []
    seen_src = set()
    used_names = set()
    for jf in files:
        for e in json.load(open(jf)):
            crop = e['crop']
            if not os.path.exists(crop):
                print(f'  MISS crop {crop}'); continue
            name = e['filename']
            if not name.endswith('.png'):
                name += '.png'
            base = name[:-4]
            k = 2
            while name in used_names:
                name = f'{base}-{k}.png'; k += 1
            used_names.add(name)
            dest = os.path.join(fig_dir, name)
            shutil.copyfile(crop, dest)
            src = f'/exam-figures/{subject}/{name}'
            if src in seen_src:
                continue
            seen_src.add(src)
            entries.append({
                'subjectId': e['subjectId'], 'subjectLabel': e['subjectLabel'],
                'topicLabel': e.get('topicLabel'), 'level': e.get('level'),
                'year': e.get('year'), 'questionRef': e.get('questionRef'),
                'src': src, 'alt': e['alt'], 'source': e['source'],
            })

    entries.sort(key=lambda x: (-(x.get('year') or 0), x['src']))
    lines = [
        '/**',
        ' * @license',
        ' * SPDX-License-Identifier: Apache-2.0',
        ' *',
        f' * Diagram Vault — {subject} figures extracted from SEC question papers. Written by',
        ' * tools/dv_apply.py from agent-verified crops; do not hand-edit (re-run apply).',
        ' */',
        '',
        "import { nf } from '../nf';",
        "import type { DiagramEntry } from '../index';",
        '',
        f'export const {ident(subject)}_FIGURES: DiagramEntry[] = [',
    ]
    for e in entries:
        lines.append('  nf({')
        lines.append(f"    subjectId: {js(e['subjectId'])}, subjectLabel: {js(e['subjectLabel'])},")
        lines.append(f"    level: {js(e['level'])}, year: {js(e['year'])},")
        lines.append(f"    topicLabel: {js(e['topicLabel'])}, questionRef: {js(e['questionRef'])},")
        lines.append(f"    src: {js(e['src'])},")
        lines.append(f"    alt: {js(e['alt'])},")
        lines.append(f"    source: {js(e['source'])},")
        lines.append('  }),')
    lines.append('];')
    out = os.path.join(REPO, 'data', 'diagramVault', 'figures', f'{subject}.ts')
    with open(out, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    print(f'{len(entries)} figures -> {out} (+ {len(used_names)} PNGs in public/exam-figures/{subject}/)')


if __name__ == '__main__':
    main()
