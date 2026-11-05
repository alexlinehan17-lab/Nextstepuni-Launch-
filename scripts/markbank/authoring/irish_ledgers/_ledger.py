"""Shared finishing step for the Irish source-review ledger makers.

Each maker rebuilds one committed ledger (scripts/markbank/authored/irish-*-source-review.json)
from the official paper: it rescans every raw directive line and classifies it with the
decision rules recorded at review time. Two kinds of later record are kept explicitly so the
ledger stays byte-reproducible:

- AMENDMENTS: exact whole-string replacements made after the first review (for example the
  2026-10-12 "choice is not a route" rule and the film/play decision), applied in order.
- RECORDED: fields observed after review that cannot be derived from the paper (browser
  verification, verified audio) or lists rewritten wholesale.

`--check` rebuilds the ledger and fails unless it is byte-identical to the committed file.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
AUTHORED = REPO / 'scripts/markbank/authored'


def _amend(value, amendments):
    if isinstance(value, dict):
        return {k: _amend(v, amendments) for k, v in value.items()}
    if isinstance(value, list):
        return [_amend(v, amendments) for v in value]
    if isinstance(value, str):
        for old, new in amendments:
            if value == old:
                value = new
        return value
    return value


def render(ledger, amendments, recorded, key_order):
    data = _amend(ledger, amendments)
    data.update(recorded)
    assert set(data) == set(key_order), ('Ledger keys changed', set(data) ^ set(key_order))
    return json.dumps({k: data[k] for k in key_order}, ensure_ascii=False, indent=2) + '\n'


def finish(ledger, name, amendments, recorded, key_order, argv=None):
    argv = sys.argv[1:] if argv is None else argv
    target = AUTHORED / name
    content = render(ledger, amendments, recorded, key_order)
    if '--check' in argv:
        if not target.exists() or target.read_text() != content:
            raise SystemExit(f'STALE: {name} does not match its maker')
        print(f'OK {name}')
    else:
        target.write_text(content)
        print(f'wrote {name}')
