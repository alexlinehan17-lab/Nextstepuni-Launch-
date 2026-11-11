#!/usr/bin/env python3
"""Take a drawing's lettering out of a Technology scheme's .md, by printed row.

    python3 scripts/markbank/authoring/tech_mdclean.py            # report
    python3 scripts/markbank/authoring/tech_mdclean.py --write    # rewrite the .md files

The scheme sets a flowchart, a circuit or a lever beside its answer prose, and
the extractor reads the two as one row: "Effort = 50 N Fulcrum", "A limit
switch at the top of the Yes". tech_all.py takes the lettering off the marking
points it builds, but the build's provenance gate reads the .md, so a point
whose two halves are separated in the .md by a flowchart's words could never be
joined back into the sentence the scheme prints -- 2025 Higher 1(b)(iii) read
as five fragments and was refused as a drawing.

So the lettering comes out of the .md itself, here, before anything reads it.
The region is a rectangle a person measured on the rendered page
(tech_crops.LABEL_ZONES, and every tech_crops.SOLUTIONS crop); the row is the
one the extractor assembled; the lines inside the rectangle are the drawing's
own and come off, the prose beside them stays word for word. A tariff line is
never touched: it bounds the block.
"""
import argparse
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
import tech_crops as TC                                      # noqa: E402
import tech_degrees as TD                                    # noqa: E402
from tech_scheme import TARIFF, BAND                         # noqa: E402

PAGE_MARK = re.compile(r'^##\s*Page\s*(\d+)\s*$')


def sittings():
    out = set(TC.LABEL_ZONES)
    for key in TC.SOLUTIONS:
        p = TC.parse_key(key)
        out.add((p[0], p[1]))
    return sorted(out)


def clean(year, level):
    """(new text, [(page, old line, new line)])."""
    md = os.path.join(TC.SCHEMES, f'{year}-{level}.md')
    if not os.path.exists(md):
        return None, []
    pdf = TC.scheme_path(year, level)
    out, changes, page = [], [], 0
    with open(md, encoding='utf-8') as fh:
        for raw in fh.read().split('\n'):
            pm = PAGE_MARK.match(raw)
            if pm:
                page = int(pm.group(1)) - 1
                out.append(raw)
                continue
            # tech_crops.MD_LINE_FIX: a drawing's lettering the row rule
            # cannot place (rotated, or welded onto prose), a tariff printed
            # beside an answer's first line, a head set on its neighbour's
            # line -- each one named, and each one only moves or removes.
            fixed = raw
            for pattern, repl in TC.MD_LINE_FIX.get((year, level), ()):
                fixed = re.sub(pattern, repl, fixed)
            if fixed != raw:
                changes.append((page + 1, raw.strip(), fixed.strip()))
                for part in fixed.split('\n'):
                    if part.strip():
                        out.append(part)
                continue
            text = raw.strip()
            rects = TC.scheme_zones(year, level, page) if text else []
            if not rects or TARIFF.search(text) or BAND.search(text) \
                    or text in TC.MD_KEEP.get((year, level, page), ()):
                out.append(raw)
                continue
            got = TC.strip_row_labels(text, pdf, page, rects)
            if got is None or got == text:
                out.append(raw)
                continue
            # The fixes once more on the stripped line, so a run over an
            # already-cleaned .md does what a run over the raw one did.
            for pattern, repl in TC.MD_LINE_FIX.get((year, level), ()):
                got = re.sub(pattern, repl, got)
            changes.append((page + 1, text, got))
            if got:
                out.extend(part for part in got.split('\n') if part.strip())
    # tech_degrees: the scheme's raised "o" degree signs, each proven from the
    # PDF's spans on that page, written as the degree sign the page prints.
    proven = TD.scheme_proofs(year, level)
    if proven:
        # Never more of one form on a page than the page proves.
        page, seen = 0, {}
        for line in out:
            pm = PAGE_MARK.match(line)
            if pm:
                page = int(pm.group(1)) - 1
            elif page in proven:
                for key in proven[page]:
                    seen[(page, key)] = seen.get((page, key), 0) + len(TD.pattern(*key).findall(line))
        for (pg, key), n in seen.items():
            if n > proven[pg][key]:
                raise SystemExit(f'tech_mdclean: {year} {level} page {pg + 1}: {n} x {key[0]}o, {proven[pg][key]} proven')
        page = 0
        for i, line in enumerate(out):
            pm = PAGE_MARK.match(line)
            if pm:
                page = int(pm.group(1)) - 1
                continue
            if page in proven:
                got, n = TD.repair(line, proven[page])
                if n:
                    changes.append((page + 1, line.strip(), got.strip()))
                    out[i] = got
    return '\n'.join(out), changes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    total = 0
    cleaned = set(sittings())
    for name in sorted(os.listdir(TC.SCHEMES)):
        m = re.fullmatch(r'(\d{4})-(hl|ol)\.md', name)
        if m and (int(m.group(1)), m.group(2)) not in cleaned \
                and TD.scheme_proofs(int(m.group(1)), m.group(2)):
            raise SystemExit(f'tech_mdclean: {name} prints degree signs but is not a cleaned sitting')
    for year, level in sittings():
        new, changes = clean(year, level)
        if new is None:
            continue
        total += len(changes)
        print(f'{year} {level.upper()}: {len(changes)} line(s) {"rewritten" if args.write else "to rewrite"}')
        for page, old, got in changes[:40]:
            print(f'   p{page}: {old[:60]!r} -> {got[:60]!r}')
        if args.write and changes:
            with open(os.path.join(TC.SCHEMES, f'{year}-{level}.md'), 'w', encoding='utf-8') as fh:
                fh.write(new)
    print(f'{total} line(s) in all')
    return 0


if __name__ == '__main__':
    sys.exit(main())
