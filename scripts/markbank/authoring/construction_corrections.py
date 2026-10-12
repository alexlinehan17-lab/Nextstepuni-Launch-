"""Hash-linked, in-place corrections and recorded withdrawals of earlier Construction Studies cards.

A later source review may correct a pre-audit card in place, keeping its ID (student progress
is keyed on it). Each correction is recorded in that review's file with the SHA-256 of the card it
replaced and of the card that replaced it.

A review may also withdraw a card. Two kinds are recorded, never silent:
- a branch-only card that never shipped (for example a per-combination route card retired by the
  "choice is not a route" rule), recorded with the SHA-256 of the card withdrawn;
- a live card consolidated into a surviving card, recorded with that card as its progress alias
  (aliasOf), which must also be listed in components/MarkBank/cardAliases.ts.

A prior-card preservation check therefore accepts a changed card only through a recorded,
hash-linked correction, and a missing card only through a recorded withdrawal; every other prior
card must stay byte-identical.
"""
import hashlib
import json
import re
from pathlib import Path

R = Path(__file__).resolve().parents[3]


def card_hash(card):
    return hashlib.sha256(json.dumps(card, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def _reviews():
    for path in sorted((R / 'scripts/markbank/authored').glob('construction-studies-*-reviewed.json')):
        yield json.loads(path.read_text())


def recorded_corrections():
    out = {}
    for review in _reviews():
        for fix in review.get('corrections', []):
            assert fix['cardId'] not in out, ('corrected twice', fix['cardId'])
            out[fix['cardId']] = fix
    return out


def recorded_withdrawals():
    out = {}
    for review in _reviews():
        for gone in review.get('withdrawn', []):
            assert gone['cardId'] not in out, ('withdrawn twice', gone['cardId'])
            assert gone['reason'].strip() and re.fullmatch(r'[0-9a-f]{64}', gone['priorSha256']), gone['cardId']
            out[gone['cardId']] = gone
    return out


def card_aliases():
    text = (R / 'components/MarkBank/cardAliases.ts').read_text()
    return dict(re.findall(r'^\s*"([^"]+)":\s*"([^"]+)",', text, re.M))


def assert_prior_cards_preserved(prior_hashes, by_id):
    """Every prior card is byte-identical, corrected through its record, or withdrawn through its record."""
    fixes, gone, aliases = recorded_corrections(), recorded_withdrawals(), card_aliases()
    for cid, digest in prior_hashes.items():
        if cid not in by_id:
            w = gone.get(cid)
            assert w and w['priorSha256'] == digest, ('missing without a recorded withdrawal', cid)
            if w.get('aliasOf'):
                assert w['aliasOf'] in by_id and aliases.get(cid) == w['aliasOf'], ('alias not live', cid)
            continue
        actual = card_hash(by_id[cid])
        if actual != digest:
            fix = fixes.get(cid)
            assert fix and fix['priorSha256'] == digest and fix['correctedSha256'] == actual, cid
