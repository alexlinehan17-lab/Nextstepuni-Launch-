"""usage: python3 scripts/markbank/agricultural-science-audit/render_edition.py <year> <fileid> <outdir> — page PNGs + text for paper and scheme."""
import fitz, sys, hashlib
from pathlib import Path
year, fileid, out = sys.argv[1], sys.argv[2], Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)
for kind in ('exampapers', 'markingschemes'):
    path = Path(f'paper-trail-corpus/{kind}/{year}/{fileid}')
    print(kind, hashlib.sha256(path.read_bytes()).hexdigest(), end=' ')
    with fitz.open(path) as d, open(out / f'{kind}.txt', 'w') as t:
        print(len(d))
        for i, p in enumerate(d):
            p.get_pixmap(matrix=fitz.Matrix(1.4, 1.4)).save(out / f'{kind}-{i+1:02d}.png')
            t.write(f'=== PAGE {i+1} ===\n' + p.get_text())
