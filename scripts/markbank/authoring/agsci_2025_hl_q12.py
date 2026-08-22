#!/usr/bin/env python3
"""Agricultural Science 2025 Higher Level Q12 — "outline one scientific reason".

Five prompts, any four to be answered, marked 2(4) + 2(1): two marks for each of
four, and two more. Each card carries the 2 its own prompt is worth.

Read from the scheme PDF. The markdown runs the cue into the first answer here,
and the scheme repeats each prompt before answering it, so the prompt is index 0
of every part and the answers follow it.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author  # noqa: E402

A = Author(2025, 'hl')
TARIFF = ('Q12 sets five prompts and asks for any four, marked 2(4) + 2(1) — two '
          'marks for each of four answered, and two more.')

A.card(12, 'a', topic='agsci-4-3-2', concept='why-progeny-test-dairy-cows',
       source='pdf', use=[2], marks=[2], notation='2(4) + 2(1)', notes=TARIFF)

A.card(12, 'b', topic='agsci-3-3-1', concept='why-buffer-zones-beside-waterways',
       source='pdf', use=[[1, 2, 3, 4]], marks=[2], notation='2(4) + 2(1)', notes=TARIFF)

A.card(12, 'c', topic='agsci-3-1', concept='why-chloroplasts-sit-in-the-palisade-layer',
       source='pdf', use=[1], marks=[2], notation='2(4) + 2(1)', notes=TARIFF)

A.card(12, 'd', topic='agsci-4-3-1', concept='why-cull-breeding-ewes',
       source='pdf', use=[1], marks=[2], notation='2(4) + 2(1)', notes=TARIFF)

A.card(12, 'e', topic='agsci-3-1', concept='why-water-moves-through-the-plant',
       source='pdf', use=[[1, 2, 3]], marks=[2], notation='2(4) + 2(1)', notes=TARIFF)

A.emit()
