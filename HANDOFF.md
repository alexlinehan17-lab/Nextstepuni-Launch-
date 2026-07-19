# Founder terminal to-do (things that need your Mac + credentials)

Some work is fully built and committed but can't go **live** from the CI/agent
environment because it needs write access to Firebase Storage (`allow write: if
false` — uploads go only through the gcloud pipeline) or a credentialed deploy.
Run these on your Mac where gcloud + the SEC harvest live. Newest at the top.

---

## ☐ 1. Paper Trail — light Wave 10 answer flags (Politics & Society + Classical Studies)

20 verified answer maps are committed; they just need uploading + the flag re-lit.

```bash
# a) upload the 20 new sidecars + re-sync the 1 drifted Italian map
python3 - <<'PY'
import os
rows=[]
for yr in os.listdir('scripts/paper-trail/answers'):
    d=f'scripts/paper-trail/answers/{yr}'
    if not (yr.isdigit() and os.path.isdir(d)): continue
    for fn in os.listdir(d):
        if fn.startswith(('LC568','LC008')):
            sid='politics-and-society' if fn.startswith('LC568') else 'classical-studies'
            rows.append(f"{d}/{fn}\tpapers/lc/{sid}/{yr}/answers/{fn[:-5]}.json")
rows.append("scripts/paper-trail/answers/2014/LC013ALP000IV.pdf.json\t"
            "papers/lc/italian/2014/answers/LC013ALP000IV.pdf.json")
os.makedirs('scripts/paper-trail/out', exist_ok=True)
open('scripts/paper-trail/out/wave10-upload.tsv','w').write('\n'.join(sorted(rows))+'\n')
print(len(rows),'rows')
PY
python3 scripts/paper-trail/upload_answers.py scripts/paper-trail/out/wave10-upload.tsv

# b) re-light the flags (regenerates paperTrailData.ts with answers:1)
python3 scripts/paper-trail/build-index.py
git add paperTrailData.ts && git commit -m "Paper Trail: light Wave 10 answer flags"
```

Details: `scripts/paper-trail/WAVE10.md`.

## ☐ 2. Paper Trail — mirror the Formulae & Tables booklet (feature: Formulae quick-jump)

The Formulae quick-jump feature is built and gated: the button only appears once
the booklet PDF + its page-index sidecar are in Storage AND
`FORMULAE_BOOKLET_LIVE` is flipped, so nothing dead ships. To turn it on:

```bash
# a) get the SEC "Formulae and Tables" booklet PDF (public) →
#    paper-trail-corpus/formulae/formulae-and-tables.pdf
# b) build the page-index sidecar (section id → PDF page) from the real PDF →
#    paper-trail-corpus/formulae/formulae-and-tables.index.json
# c) upload both (regenerate the TSV first — out/ is gitignored):
python3 scripts/paper-trail/upload_answers.py scripts/paper-trail/out/formulae-upload.tsv
# d) flip FORMULAE_BOOKLET_LIVE = true in data/paperTrailFormulae.ts, commit.
```

Full steps + section ids: **`scripts/paper-trail/FORMULAE.md`**.

## ☐ 3. Accreditation — supply more SEC reports (unblocks the subject modules)

35 subject modules are deferred pending each subject's SEC Chief Examiner report /
marking scheme. Drop PDFs into `examiner-reports/<subject>/` and I can accredit
them (this doesn't need a terminal — just the files in the repo). Priority:
English, Biology, Geography (big cohorts).

## ☐ 4. Accreditation — re-verify Points Optimization H1 rates

The per-subject H1-rate figures are labelled approximate (examinations.ie 403'd
the stats tables). When you can reach examinations.ie/statistics, confirm the
`SUBJECTS_DATA` numbers in `components/PointsOptimizationModule.tsx` against the
published tables and tell me any that drifted.

## ☐ 5. Accuracy — Mastering Home Economics exam structure is wrong (needs a sourced pass)

Flagged 2026-07-19 during the Innovation-Zone audit loop. The Home Economics
subject module (`subjectContentPractical.ts`, key `home-economics`, §1) misstates
the assessment structure and I did **not** correct it, because the in-repo scheme
only documents the written paper's internal marks — not the overall
written-vs-coursework split — and the governing rule forbids replacing wrong
figures with numbers I can't cite. What's verifiably wrong against the in-repo
**2025 HL marking scheme** (`examiner-reports/home-economics/2025-insights.md`):

- The module claims **three components** including a **"Food Practical Exam …
  worth roughly 35%"**. LC Home Economics has **no separate timed food-practical
  exam** — the practical element is the **Food Studies Coursework journal**
  (marked out of 160; `2025-marking-scheme.md` p.~1247, `2025-ol-insights.md` §8).
- The module says the written paper is **"~250 marks (~50%)"** with **two
  electives (Food Studies / Social Studies)**. The scheme says the written paper
  is **280 or 320 marks** (Section A 60 + Section B 180 + Section C 40/80) and
  Section C offers **four** options: Home Design & Management (80), Textiles
  Fashion & Design (40), Social Studies (80), or Core Q4 (80) — "Food Studies" is
  the coursework journal, **not** a written elective.

**To fix properly:** supply the SEC Home Economics subject specification (or the
2017 Chief Examiner's Report — examinations.ie 403'd it on 2026-07-06) stating the
official **written 80% / Food Studies coursework 20%** split, and I'll rewrite §1
to the correct structure, wire references, add the dossier, and log the
corrections in `data/cutContent.ts` — the same accreditation shape used for
English. Until then the module's structure section should be treated as unverified.
