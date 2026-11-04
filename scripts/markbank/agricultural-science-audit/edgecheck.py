"""Flag crop edges that cut through ink: for each region of a module's REGIONS, compare the ink
of the first/last pixel row with the emptiest row within +-0.012.
usage: python3 scripts/markbank/agricultural-science-audit/edgecheck.py <module> <paper.pdf> <scheme.pdf>"""
import importlib, sys
sys.path.insert(0, 'scripts/markbank/agricultural-science-audit')
sys.path.insert(0, 'scripts/markbank/authoring')
import regions as R
mod = importlib.import_module(sys.argv[1])
paper, scheme = sys.argv[2], sys.argv[3]
seen = set()
for ref, (pp, sp) in mod.REGIONS.items():
    for pdf, pieces, side in ((paper, pp, 'paper'), (scheme, sp, 'scheme')):
        for piece in pieces:
            p = piece['p']; a, b = piece['r'][1], piece['r'][3]
            key = (side, p, a, b)
            if key in seen: continue
            seen.add(key)
            rows = R._ink_rows(pdf, p); h = len(rows)
            for edge, y in (('top', a), ('bottom', b)):
                r = min(h - 1, int(round(y * h)))
                lo, hi = max(0, r - 20), min(h - 1, r + 20)
                base = min(rows[lo:hi + 1])
                if rows[r] > base + 3:
                    print(f'{ref:32s} {side:6s} p{p} {edge:6s} y={y} ink={rows[r]} base={base}')
