"""Extract an SEC Mathematics scheme PDF to the provenance gate's markdown: page text, then block order.

Pure extraction (pymupdf get_text per page, the bank's own glyph fold, then the
block-ordered text append-scheme-blocks.py writes). Nothing is typed by hand.
    python3 scripts/markbank/authoring/maths/make_scheme_md.py <year> <hl|ol>   (run from the repository root)
"""
import importlib.util, sys, os
import pymupdf
year, lv = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location('asb', 'scripts/markbank/authoring/append-scheme-blocks.py')
asb = importlib.util.module_from_spec(spec); spec.loader.exec_module(asb)
pdf = f'paper-trail-corpus/markingschemes/{year}/{"LC003ALP000EV" if lv == "hl" else "LC003GLP000EV"}.pdf'
out = f'examiner-reports/maths/schemes/{year}-{lv}.md'
assert not os.path.exists(out), out
with pymupdf.open(pdf) as doc:
    pages = [f'## Page {n + 1}\n\n{doc[n].get_text()}' for n in range(doc.page_count)]
text = asb.fold('\n'.join(pages)).rstrip('\n')
blocks = asb.fold(asb.block_text(pdf))
open(out, 'w', encoding='utf-8').write(f'{text}\n\n{asb.MARK}\n\n{blocks}\n')
print(out, len(text.splitlines()), 'page lines +', len(blocks.splitlines()), 'block lines')
