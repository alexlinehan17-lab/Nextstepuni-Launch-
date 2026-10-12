"""Consolidate one reviewed Construction Studies paper under the "choice is not a route" rule (2026-10-12).

When the student chooses which N of M printed items to answer, the paper now carries ONE card that
prints all M items and holds one anyN group over them, never a card per item or per combination.
This script swaps a paper's previously integrated reviewed cards for its regenerated draft:

- cards kept by ID are replaced in place (authored order preserved);
- cards no longer produced are WITHDRAWN and recorded in the reviewed file with the SHA-256 of the
  card withdrawn. Branch-only cards (never on main) simply go; a live pre-audit card consolidated
  into a surviving card is recorded with that card as its progress alias (aliasOf) and the alias is
  added to components/MarkBank/cardAliases.ts;
- new cards are appended; figures no longer referenced are removed from the manifest and public/;
- the reviewed file, the exact Atlas bridge and the test fixture follow the new card set.

Usage: python3 consolidate.py <paper>, where <paper> is one of PAPERS. Run once per paper; it
refuses to run when the paper is already consolidated.
"""
import hashlib
import importlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = HERE.parents[4]
AUTHORING = R / 'scripts/markbank/authoring'
sys.path.insert(0, str(AUTHORING))
import construction_corrections  # noqa: E402

DRAFTS = R / 'docs/markbank-audit/2026-09-28/drafts'
PAPERS = {
    '2026-ordinary': dict(validator='construction_2026_ordinary', draft=DRAFTS / 'construction-2026-ordinary/ordinary-2026-draft.json',
                          review='construction-studies-2026-ordinary-reviewed.json', bridge='construction-studies-2026-ordinary.json',
                          fixture='test/fixtures/construction2026Reviewed.ts', consts={'CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS': 'all'},
                          aliases={}),
    '2015-ordinary': dict(validator='construction_2015_ordinary', draft=DRAFTS / 'construction-2015-ordinary-q1-q9/ordinary-draft.json',
                          review='construction-studies-2015-ordinary-reviewed.json', bridge='construction-studies-2015-ordinary.json',
                          fixture='test/fixtures/construction2015Reviewed.ts', consts={'CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS': 'all'},
                          aliases={}),
    '2026-higher': dict(validator='construction_2026_higher', draft=DRAFTS / 'construction-2026-higher/higher-2026-draft.json',
                        review='construction-studies-2026-higher-reviewed.json', bridge='construction-studies-2026-higher.json',
                        fixture='test/fixtures/construction2026Reviewed.ts', consts={'CONSTRUCTION_2026_HIGHER_REVIEWED_IDS': 'all'},
                        aliases={}),
    '2025-higher': dict(validator='construction_2025_higher', draft=DRAFTS / 'construction-2025-higher/higher-2025-draft.json',
                        review='construction-studies-2025-higher-reviewed.json', bridge='construction-studies-2025-higher.json',
                        fixture='test/fixtures/construction2025Reviewed.ts',
                        consts={'CONSTRUCTION_2025_HIGHER_ADDED_IDS': 'added', 'CONSTRUCTION_2025_HIGHER_CORRECTED_IDS': 'corrected'},
                        aliases={'cons-2025-hl-q2-a-health-and-safety-officer': 'cons-2025-hl-q2-a-safety-training',
                                 'cons-2025-hl-q2-a-risk-assessment-audit': 'cons-2025-hl-q2-a-safety-training',
                                 'cons-2025-hl-q10-a-foundation-design': 'cons-2025-hl-q10-a-building-form'}),
}
RULE = ('Choice is not a route (coordinator rule, 2026-10-12): a printed choose-N-of-M is ONE card that prints all M items '
        'with one anyN group over them, never a card per item or per combination.')


def read(p):
    return json.loads(Path(p).read_text())


def save(p, d):
    Path(p).write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')


def main(key):
    cfg = PAPERS[key]
    validator = importlib.import_module(cfg['validator'])
    review_path = R / 'scripts/markbank/authored' / cfg['review']
    bridge_path = R / 'scripts/markbank/atlas-reviews' / cfg['bridge']
    authored_path = R / 'scripts/markbank/authored/construction-studies.json'
    manifest_path = R / 'components/MarkBank/figures-construction-studies.json'
    aliases_path = R / 'components/MarkBank/cardAliases.ts'
    public = R / 'public/exam-figures/construction-studies/markbank'
    old = read(review_path)
    assert 'consolidation' not in old, f'{key} is already consolidated'
    draft = read(cfg['draft'])
    validator.validate(draft, figure_dir=cfg['draft'].parent, integrated=None)

    authored = read(authored_path)
    by_id = {c['id']: c for c in authored}
    old_ids = [t['card']['id'] for t in old['tasks']]
    new_cards = {t['card']['id']: t['card'] for t in draft['tasks']}
    assert set(old_ids) <= set(by_id) and all(by_id[i] == t['card'] for i, t in zip(old_ids, old['tasks']))
    withdrawn_ids = [i for i in old_ids if i not in new_cards]
    assert set(cfg['aliases']) <= set(withdrawn_ids) and set(cfg['aliases'].values()) <= set(new_cards)
    previously = {w['cardId'] for w in old.get('withdrawn', [])}
    assert not previously & set(withdrawn_ids)
    withdrawn = [dict(cardId=i, priorSha256=construction_corrections.card_hash(by_id[i]), reason=RULE,
                      **({'aliasOf': cfg['aliases'][i]} if i in cfg['aliases'] else {})) for i in withdrawn_ids]

    gone = set(withdrawn_ids)
    merged = [new_cards.get(c['id'], c) for c in authored if c['id'] not in gone]
    merged += [c for i, c in new_cards.items() if i not in by_id]
    assert len({c['id'] for c in merged}) == len(merged)
    save(authored_path, merged)

    if cfg['aliases']:
        text = aliases_path.read_text()
        lines = ''.join(f'  "{o}": "{n}",\n' for o, n in cfg['aliases'].items())
        block = ('  /* 2026-10-12. Construction Studies: a printed choose-N-of-M is one card, not a card per item\n'
                 '   * (coordinator rule "choice is not a route"). These pre-audit per-item cards are consolidated\n'
                 '   * into the surviving card for the same printed part; progress goes to it. */\n' + lines)
        assert text.rstrip().endswith('};') and not any(f'"{o}"' in text for o in cfg['aliases'])
        aliases_path.write_text(text.rstrip()[:-2] + block + '};\n')

    manifest = read(manifest_path)
    old_figs = {f['key'] for f in old['questionFigures']}
    new_figs = {f['key']: f for f in draft['questionFigures']}
    for k in sorted(old_figs - set(new_figs)):
        dst = public / f'{k}.png'
        assert k in manifest and dst.exists(), k
        del manifest[k]
        dst.unlink()
    for k in new_figs:
        dst = public / f'{k}.png'
        assert k in manifest and dst.exists() and hashlib.sha256(dst.read_bytes()).hexdigest() == new_figs[k]['sha256'], k
    save(manifest_path, manifest)

    now = datetime.now(timezone.utc).isoformat()
    keep = {k: v for k, v in old.items() if k not in draft and k not in ('tasks', 'bindings', 'questionFigures', 'addedIds')}
    review = dict(draft, **keep)
    review['withdrawn'] = old.get('withdrawn', []) + withdrawn
    review['consolidation'] = dict(at=now, rule=RULE, withdrawnCards=len(withdrawn), aliasedCards=len(cfg['aliases']),
                                   tasksBefore=len(old_ids), tasksAfter=len(new_cards),
                                   removedFigures=sorted(old_figs - set(new_figs)))
    review['status'] = re.sub(r'\b\d+ source-reviewed tasks', f'{len(new_cards)} source-reviewed tasks', old['status'])
    save(review_path, review)

    bridge = read(bridge_path)
    bridge.update(expectedRuntimeCards=len(new_cards), cards=draft['bindings'],
                  questions=[dict(n=q['n'], fileid=q['fileid'],
                                  topicIds=sorted({t for b in draft['bindings'] if b['questionNumber'] == q['n'] for t in b['atlasTopicIds']}))
                             for q in bridge['questions']])
    bridge['reason'] = re.sub(r'\d+ source-reviewed tasks', f'{len(new_cards)} source-reviewed tasks', bridge['reason'])
    save(bridge_path, bridge)

    fixture = R / cfg['fixture']
    text = fixture.read_text()
    corrected = {t['card']['id'] for t in draft['tasks'] if t.get('correction')}
    for const, kind in cfg['consts'].items():
        ids = [t['card']['id'] for t in draft['tasks']
               if kind == 'all' or (kind == 'added') != (t['card']['id'] in corrected)]
        body = json.dumps(ids, indent=2).replace('"', "'")
        text, n = re.subn(rf'export const {const} = \[.*?\];', f'export const {const} = {body};', text, flags=re.S)
        assert n == 1, const
    fixture.write_text(text)
    report = validator.validate(read(review_path))
    if 'fullPaperReconciliation' in review:
        recon = {k: v for k, v in review['fullPaperReconciliation'].items() if k not in ('wholeQuestionRoutes', 'q8Routes')}
        review['fullPaperReconciliation'] = dict(recon, validator=report)
        save(review_path, review)
        assert validator.validate(read(review_path)) == report
    print(json.dumps(dict(paper=key, before=len(old_ids), after=len(new_cards), withdrawn=len(withdrawn),
                          aliased=len(cfg['aliases']), removedFigures=len(old_figs - set(new_figs)))))


if __name__ == '__main__':
    main(sys.argv[1])
