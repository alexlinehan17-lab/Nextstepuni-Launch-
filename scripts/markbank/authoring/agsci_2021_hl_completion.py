#!/usr/bin/env python3
"""Final provenance-checked Agricultural Science 2021 HL cards."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author  # noqa: E402

A = Author(2021, 'hl')

A.card(14, 'a', topic='agsci-4-3-2', concept='liquid-and-creamery-milk-systems',
       source='pdf', join=[(6, 3), (11, 9), (16, 17, 18, 19)], marks=[6, 6, 6],
       tariff='orderedSplit', notation='3 × (4+2)',
       context='Each row reads Liquid milk first, then Creamery milk.',
       notes='The official scheme presents this as a two-column comparison; joined '
             'rows preserve the printed left-to-right pairing without inventing '
             'a separate mark value for either cell.')

A.card(15, 'b', 'ii', topic='agsci-3-2', concept='calculating-milk-composition-change',
       source='pdf', use=[4, 6], marks=[3, 2], notation='3+2',
       figure='agricultural-science-2021-HL-paper-p33-art-q15b')

A.card(16, 'a', 'i', topic='agsci-1-3', concept='comparing-farm-gross-margins',
       source='pdf', join=[(4, 5, 7), (9,)], marks=[4, 2], notation='4+2',
       figure='agricultural-science-2021-HL-paper-p35-i1',
       notes='The first scheme row retains the linked calculations and totals; the '
             'second gives the resulting higher-price comparison.')

A.emit()
