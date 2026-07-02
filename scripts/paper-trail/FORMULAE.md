# Paper Trail — Formulae & Tables quick-jump

**Status:** built, gated OFF (`FORMULAE_BOOKLET_LIVE = false`). Ships nothing until
the founder uploads the booklet + flips the flag. Needs the Mac + gcloud (Storage
is `allow write: if false`).

## What it is

Inside the viewer, booklet subjects (Maths, Applied Maths, Physics, Chemistry,
Physics & Chemistry, Biology, Engineering, Construction Studies, Ag Science) get a
**Formulae & Tables** entry in the Tools menu. It opens a sheet of the booklet's
sections; tapping one opens the booklet PDF at that page (`#page=N`).

Section labels + subject mapping are committed in `data/paperTrailFormulae.ts`.
Page numbers are **not** hard-coded there — printed page ≠ PDF page, and a wrong
jump reads as a bug. Pages come from a sidecar generated from the *actual*
uploaded PDF. A section with no page entry just opens the booklet at the front, so
a partial/absent index degrades gracefully.

## To turn it on (founder, on the Mac)

```bash
# a) Get the SEC "Formulae and Tables" booklet PDF (public, examinations.ie) →
#    paper-trail-corpus/formulae/formulae-and-tables.pdf

# b) Build the page-index sidecar from the real PDF. Easiest: read the booklet's
#    own bookmarks/contents and map each section id (see FORMULAE_SECTIONS ids in
#    data/paperTrailFormulae.ts) to its 1-based PDF page. Write:
#      { "algebra": 9, "geometry": 12, "trigonometry": 15, ... }
#    to  paper-trail-corpus/formulae/formulae-and-tables.index.json
#    (only include sections you've confirmed; omit the rest.)

# c) Upload both to Storage at the paths the app expects:
python3 - <<'PY'
import os
rows=[
  ("paper-trail-corpus/formulae/formulae-and-tables.pdf",
   "formulae/formulae-and-tables.pdf"),
  ("paper-trail-corpus/formulae/formulae-and-tables.index.json",
   "formulae/formulae-and-tables.index.json"),
]
os.makedirs("scripts/paper-trail/out", exist_ok=True)
open("scripts/paper-trail/out/formulae-upload.tsv","w").write(
  "\n".join(f"{a}\t{b}" for a,b in rows)+"\n")
print("wrote formulae-upload.tsv")
PY
python3 scripts/paper-trail/upload_answers.py scripts/paper-trail/out/formulae-upload.tsv

# d) Flip the flag + commit:
#    data/paperTrailFormulae.ts →  export const FORMULAE_BOOKLET_LIVE = true;
git commit -am "Paper Trail: light Formulae & Tables quick-jump"
```

Verify one section jumps to the right page before flipping the flag — the index
is the only part that can be wrong, and the flag is the only thing gating a live
button.

## Section ids

The stable ids the sidecar is keyed by live in `FORMULAE_SECTIONS`
(`data/paperTrailFormulae.ts`): `algebra`, `geometry`, `trigonometry`,
`differentiation`, `integration`, `sequences-series`, `financial-maths`,
`area-volume`, `statistics`, `physical-constants`, `mechanics`, `electricity`,
`waves-optics`, `periodic-table`, `reduction-potentials`, `thermodynamic-data`.
Add more by extending that list (label + subject mapping) and the sidecar.
