#!/usr/bin/env python3
"""Chemistry 2024 HL — open parts carded through chem_scheme.

The work list, the hand-assigned topics and the reasons for everything left
out are in chem_open.py. This wrapper exists because merge.py discovers a
subject's scripts by the filename chem_<year>_<level>.py, one sitting each.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_open import emit  # noqa: E402

cards, refused = emit((2024, 'hl'))
for r in refused:
    print(f'REFUSED {r}', file=sys.stderr)
print(json.dumps(cards, ensure_ascii=False, indent=1))
