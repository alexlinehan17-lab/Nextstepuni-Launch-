"""Apply a regenerated draft's wording revisions to an already-integrated Construction Studies paper.

Used when a reviewed paper's generator changes presentation only: wording (for example, retiring the
route-era note "every combination is kept" once a printed choice became one card) or a card's solution
figure (a one-card choice must still show every item's scheme drawings after reveal, so it takes a
composite crop). The card set, rows, tariffs and topics must be unchanged and earlier figures are kept
byte-identical; a new figure is installed in public/ with its manifest entry. Every changed card is
recorded, never silent:

- a card already corrected in place keeps its correction, now pointing at the revised card, with the
  hash it previously produced kept in supersededSha256 (so older prior sets still match it);
- any other changed card gets a hash-linked entry in the review's `revisions`, read by
  construction_corrections.recorded_corrections like a correction.

Usage: python3 revise.py <paper> "<reason>", where <paper> is a key of consolidate.PAPERS.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from consolidate import R, PAPERS, read, save, construction_corrections  # noqa: E402

ONLY = {'sourceMaterial', 'figureKey'}  # a revision may change presentation, nothing that is marked


def prior_digests():
    """Every digest any recorded prior set holds for each card."""
    out = {}
    for path in sorted((R / 'docs/markbank-audit/2026-09-28/drafts').glob('*/prior-authored-card-hashes.json')):
        for cid, digest in read(path)['cards'].items():
            out.setdefault(cid, set()).add(digest)
    return out


def main(key, reason):
    cfg = PAPERS[key]
    validator = __import__(cfg['validator'])
    review_path = R / 'scripts/markbank/authored' / cfg['review']
    authored_path = R / 'scripts/markbank/authored/construction-studies.json'
    old = read(review_path)
    draft = read(cfg['draft'])
    alts = draft.pop('newFigureAlts', {})
    old_figs = {f['key']: f for f in old['questionFigures']}
    new_figs = [f for f in draft['questionFigures'] if f['key'] not in old_figs]
    assert all(f in draft['questionFigures'] for f in old['questionFigures']), 'an earlier figure changed or was removed'
    assert set(alts) == {f['key'] for f in new_figs}, 'every new figure needs its alt text'
    manifest_path = R / 'components/MarkBank/figures-construction-studies.json'
    manifest = read(manifest_path)
    public = R / 'public/exam-figures/construction-studies/markbank'
    level = draft['level'].capitalize()
    for f in new_figs:
        src, dst = cfg['draft'].parent / f"{f['key']}.png", public / f"{f['key']}.png"
        assert f['key'] not in manifest and not dst.exists() and f['solution'] is True, f['key']
        dst.write_bytes(src.read_bytes())
        assert hashlib.sha256(dst.read_bytes()).hexdigest() == f['sha256'], f['key']
        manifest[f['key']] = dict(src='/' + str(dst.relative_to(R / 'public')), md5=hashlib.md5(dst.read_bytes()).hexdigest(), alt=alts[f['key']],
                                  attribution=f"SEC Leaving Certificate Construction Studies {draft['year']} {level} Level — © State Examinations Commission.",
                                  solution=True)
    save(manifest_path, manifest)
    validator.validate(draft, figure_dir=cfg.get('figure_dir', cfg['draft'].parent), integrated=None)
    assert [t['card']['id'] for t in draft['tasks']] == [t['card']['id'] for t in old['tasks']], 'card set changed: not a revision'
    assert draft['bindings'] == old['bindings']
    before = {t['card']['id']: t['card'] for t in old['tasks']}
    changed = [t['card']['id'] for t in draft['tasks'] if t['card'] != before[t['card']['id']]]
    assert changed, 'nothing to revise'
    for cid in changed:
        new = next(t['card'] for t in draft['tasks'] if t['card']['id'] == cid)
        assert {k for k in new.keys() | before[cid].keys() if new.get(k) != before[cid].get(k)} <= ONLY, cid

    authored = read(authored_path)
    by_id = {c['id']: c for c in authored}
    assert all(by_id[cid] == before[cid] for cid in before), 'authored deck out of step with the review'
    corrected = {f['cardId'] for f in draft.get('corrections', [])}
    seen = prior_digests()
    revisions = {r['cardId']: r for r in old.get('revisions', [])}
    for cid in changed:
        if cid in corrected:
            continue
        current = construction_corrections.card_hash(before[cid])
        new_hash = construction_corrections.card_hash(next(t['card'] for t in draft['tasks'] if t['card']['id'] == cid))
        prev = revisions.get(cid)
        if prev:
            revisions[cid] = dict(prev, correctedSha256=new_hash, reason=reason,
                                  supersededSha256=sorted(set(prev.get('supersededSha256', [])) | {prev['correctedSha256']}))
        else:
            # Every prior set must have seen this card only as it is now, or not at all.
            assert seen.get(cid, {current}) <= {current}, (cid, 'an older version is in a prior set')
            revisions[cid] = dict(cardId=cid, priorSha256=current, correctedSha256=new_hash, reason=reason)

    new_cards = {t['card']['id']: t['card'] for t in draft['tasks']}
    save(authored_path, [new_cards.get(c['id'], c) for c in authored])
    # A correction whose card is unchanged keeps its exact record; a revised one points at the revised card
    # and keeps the hash it previously produced (and any earlier ones) as superseded.
    earlier = {f['cardId']: f for f in old.get('corrections', [])}
    assert [f['cardId'] for f in draft.get('corrections', [])] == list(earlier)
    fixes = []
    for fix in draft.get('corrections', []):
        prev = earlier[fix['cardId']]
        assert prev['priorSha256'] == fix['priorSha256'] and prev['reason'] == fix['reason'], fix['cardId']
        fixes.append(prev if prev['correctedSha256'] == fix['correctedSha256'] else
                     dict(prev, correctedSha256=fix['correctedSha256'],
                          supersededSha256=sorted(set(prev.get('supersededSha256', [])) | {prev['correctedSha256']})))
    review = dict(old, tasks=draft['tasks'], questionFigures=draft['questionFigures'])
    if fixes:
        review['corrections'] = fixes
    if revisions:
        review['revisions'] = list(revisions.values())
    save(review_path, review)
    report = validator.validate(read(review_path))
    print(json.dumps(dict(paper=key, revisedCards=changed, newFigures=[f['key'] for f in new_figs], correctionsSuperseded=sorted(set(changed) & corrected),
                          revisions=len(revisions), validator=report)))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
