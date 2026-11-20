"""Biology 2025 Higher Level, deferred sitting: the reviewed task ledger, kept as data.

The ledger itself is scripts/markbank/authored/biology-deferred-ledgers/2025-hl.json (bio_review_json.py
reads it); its "doc" is this sitting's method note.
"""
from bio_review_json import load

globals().update(load('2025-hl'))
