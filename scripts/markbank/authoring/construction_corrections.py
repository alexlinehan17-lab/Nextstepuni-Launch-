"""Hash-linked, in-place corrections of earlier Construction Studies cards.

A later source review may correct a pre-audit card in place, keeping its ID (student progress
is keyed on it). Each correction is recorded in that review's file with the SHA-256 of the card
it replaced and of the card that replaced it. A prior-card preservation check therefore accepts
a changed card only through such a recorded, hash-linked correction; every other prior card must
stay byte-identical.
"""
import hashlib
import json
from pathlib import Path

R = Path(__file__).resolve().parents[3]


def card_hash(card):
    return hashlib.sha256(json.dumps(card, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def recorded_corrections():
    out = {}
    for path in sorted((R / 'scripts/markbank/authored').glob('construction-studies-*-reviewed.json')):
        for fix in json.loads(path.read_text()).get('corrections', []):
            assert fix['cardId'] not in out, ('corrected twice', fix['cardId'])
            out[fix['cardId']] = fix
    return out


def assert_prior_cards_preserved(prior_hashes, by_id):
    """Every prior card is byte-identical, or replaced through its recorded correction."""
    fixes = recorded_corrections()
    for cid, digest in prior_hashes.items():
        actual = card_hash(by_id[cid])
        if actual != digest:
            fix = fixes.get(cid)
            assert fix and fix['priorSha256'] == digest and fix['correctedSha256'] == actual, cid
