#!/bin/bash
# usage: mkscheme.sh <year> <hl|ol> — build examiner-reports/agricultural-science/schemes/<year>-<lvl>.md from the PDF
# (extract, block-order append for THIS file only, column runs, table cells). Run from the worktree root.
set -e
Y=$1; L=$2; D=examiner-reports/agricultural-science/schemes
python3 scripts/markbank/extract-scheme.py $D/$Y-$L.pdf -o $D/$Y-$L.md 2>&1 | tail -1
python3 - "$D/$Y-$L.md" "$D/$Y-$L.pdf" <<'PY'
import sys,importlib.util
spec=importlib.util.spec_from_file_location('asb','scripts/markbank/authoring/append-scheme-blocks.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
md,pdf=sys.argv[1:3]
orig=open(md).read().split(m.MARK)[0].rstrip('\n')
app=m.fold(m.block_text(pdf))
open(md,'w').write(f'{orig}\n\n{m.MARK}\n\n{app}\n')
print('blocks',len(app.splitlines()))
PY
python3 scripts/markbank/append-scheme-columns.py agricultural-science $Y $L 2>&1 | tail -1
python3 scripts/markbank/append-scheme-tables.py agricultural-science $Y $L 2>&1 | tail -1
wc -l $D/$Y-$L.md
