"""Print a first-draft REGIONS table for a legacy paper's transcribed census refs.

    python3 scripts/markbank/agricultural-science-audit/draft_regions.py <year> <fileid> <census.txt>

census.txt holds the independent census rows (ref|marks|paperPage|schemePage|cue). The draft
is pasted into the review module and every crop is then rendered and inspected; a ref the
numbering cannot place is printed as a TODO for a hand-set region.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from regions import spans, task_regions  # noqa: E402

year, fileid, census = sys.argv[1:4]
paper = spans(f'paper-trail-corpus/exampapers/{year}/{fileid}')
scheme = spans(f'paper-trail-corpus/markingschemes/{year}/{fileid}')


def merge(regions):
    out = []
    for r in regions:
        if out and out[-1]['p'] == r['p'] and r['r'][1] - out[-1]['r'][3] <= 0.005:
            out[-1] = dict(p=r['p'], r=[0, out[-1]['r'][1], 1, max(out[-1]['r'][3], r['r'][3])])
        else:
            out.append(r)
    return out


def fmt(regions):
    regions = merge(regions)
    return 'P(' + ', '.join(f"({r['p']}, {r['r'][1]:.3f}, {r['r'][3]:.3f})" for r in regions) + ')'


for line in open(census).read().strip().splitlines():
    ref = line.split('|')[0]
    base = ref.split(' — ')[0]
    try:
        pp, sp = task_regions(paper, base), task_regions(scheme, base)
        print(f"    '{ref}': ({fmt(pp)}, {fmt(sp)}),")
    except KeyError as missing:
        print(f"    # TODO {ref}: no printed marker {missing}")
