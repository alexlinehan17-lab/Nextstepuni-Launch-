"""Run the two scheme appenders for a Construction scheme whose cover the
appenders' own level check cannot read (upper-case cover, or a glyph-shifted
cover). The cover was checked by hand; the PDF hash was checked against the
corpus hash list. Only pdf_for is bypassed; the fold logic is the shipped one."""
import importlib.util, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]  # repository root
sys.path.insert(0, str(ROOT / 'scripts/markbank'))
def load(name):
    spec = importlib.util.spec_from_file_location(name.replace('-', '_'), ROOT / 'scripts/markbank' / f'{name}.py')
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
year, level = int(sys.argv[1]), sys.argv[2]
pdf = ROOT / 'examiner-reports/construction-studies/schemes' / f'{year}-{level}.pdf'
assert pdf.exists()
for name in ('append-scheme-columns', 'append-scheme-fractions'):
    m = load(name)
    m.pdf_for = lambda s, y, l, _p=pdf: _p
    m.apply('construction-studies', year, level)
