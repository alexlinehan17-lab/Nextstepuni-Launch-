# Evidence Dossier — Coursework Companion

**Tool:** Coursework Companion (`components/CourseworkCompanion/CourseworkCompanion.tsx`,
registered in `components/InnovationZone.tsx` as tool id `coursework-companion`)
**Data:** `data/courseworkCompanion/index.ts` (types in `types.ts`)
**Review date:** 2026-07-11

## What it is

A browser for the coursework, project and practical components of Leaving Cert
subjects: pick a subject → see each component — what it is, the printed marking
criteria with their marks, the grading table where one is printed, and the exact
filed SEC marking scheme every fact comes from.

## Governing rule (same accreditation line as the rest of the app)

> Every marks figure, criterion, grade band and printed note is stated ONLY
> where the filed SEC marking scheme prints it. No percentage weighting,
> deadline, brief detail or component total is stated unless a filed SEC
> document states it — even when the printed criteria happen to sum to a round
> number, an unprinted total is never asserted (`totalMarks: null`). A subject
> whose filed scheme carries no coursework criteria is simply absent.

## Source of truth — AUTHORED-BUT-STRICTLY-CITED (the Oral Trainer register)

Unlike Answer Architect and Definition Drill (pure projections of the Marking
Lens corpus), there is no machine-readable coursework corpus to project from —
the written-paper corpus contains no coursework briefs. Coursework Companion is
therefore authored in the proven register of the Oral Trainer
(`data/oralExam/irish.ts` / `compliance/evidence/oral-trainer.md`): a small,
per-fact-cited dataset extracted from the filed SEC marking schemes in
`/examiner-reports/`, one verified subject at a time. Each component records:

- `source` — the named filed scheme + year, SEC-attributed;
- `filed` — the in-repo document path (the re-verification trail, checked by the
  gate to exist);
- `sourceUrl` — the SEC exam material archive
  (`https://www.examinations.ie/exammaterialarchive/`), where every cited scheme
  is published.

The internal `syllabusMeta.ts` overlay (which lists coursework components with
approximate weightings) was used ONLY as a checklist of what to go verify —
none of its uncited figures were copied. Extraction was performed per subject
directly from the filed scheme, with an explicit instruction set forbidding
inference; the extraction records are the basis of the claim-by-claim table
below.

## Coverage (launch) — claim-by-claim record

| Subject | Component | Total | Criteria | Filed source |
|---|---|---|---|---|
| Home Economics | Food Studies Practical Coursework | 160 (grading table) | Investigation 32, Prep & Planning 8, Implementation 28, Evaluation 12 (= 80 per assignment; "2 assignments for 2025" printed) | `home-economics/2025-marking-scheme.md` |
| Agricultural Science | Individual Investigative Study | — (no total printed) | 20 + 25 + 35 + 10 + 10 across five banded sections; word ranges printed | `agricultural-science/2024-marking-scheme.md` |
| Construction Studies | Practical Coursework (Form A) | 150 | Planning 40, Report 35, Manipulative Skills 40, Completion 35 (printed "Total 150"; scheme notes breakdowns may vary by year) | `construction-studies/2025-marking-scheme.md` |
| Construction Studies | Practical Test (Common Level) | 150 | Assembly 14, Marking Out 51, eight per-joint processing criteria (sum to printed "Grand Total 150"); hand-tools rule + 50% machinery penalty printed | `construction-studies/2025-marking-scheme.md` |
| DCG | Student Assignment (Higher Level) | — (total row blank on the printed sheet) | Seven printed criteria (30/20/35/15/25/10/25); page-excess deduction row printed with no amount | `dcg/2025-marking-scheme.md` |
| Engineering | Practical Examination | 100 ("100 Marks (× 1.5 = 150 Total)" printed) | Five 20-mark sections (test-piece + four part groups); Day 1/2/3 grids identical in structure | `engineering/2025-marking-scheme.md` |
| Art | Practical Coursework & Invigilated Practical | — (printed separately: 250 = 50%, 100 = 20%) | Per-artefact criteria: Investigation 10, Primary sources 25, Development 40, Realised artefact 90, Areas of practice 10; Low/Moderate/High banding printed | `art/2024-visual-studies-marking-scheme.md` |
| Geography | Geographical Investigation | — (no total printed) | Introduction 5, Planning 5, Gathering 40, Results/Conclusions/Evaluation 30, Organisation & Presentation 20; section-locked marking printed | `geography/2025-marking-scheme.md` |

**8 components across 7 subjects.** Honest omissions:
- **LCVP** — its filed scheme covers the written paper only (no portfolio
  criteria printed), so it is absent rather than padded from uncited sources.
- **Engineering Technology Project** — the filed scheme carries no project
  criteria (practical examination only), so only the practical is shown.
- The language **orals** are covered by the existing Oral Trainer and are not
  duplicated here.

## Year-cycling note

Coursework arrangements can change year to year (Home Economics' printed "2
assignments for 2025 as a result of adjustments" is itself an example, and the
Construction scheme prints that breakdowns "may vary for any given year"). Each
entry cites its exact scheme year; when a newer scheme is filed, the entry is
re-verified against it, exactly as the Oral Trainer's prescribed-material set is
year-cycled.

## Machine-checked integrity (`test/courseworkCompanion.test.ts`, every CI run)

1. Non-empty; ids unique; subject counts reconcile.
2. **THE ACCREDITATION GATE** — every component carries an SEC-attributed
   `source` naming a filed scheme + year, a resolvable SEC archive `sourceUrl`,
   and a `filed` path in `examiner-reports/` that actually exists on disk.
3. **Marks reconcile** — where a printed total exists and the criteria are the
   complete printed breakdown, they sum exactly; null totals confirm no
   invented figure.
4. Every criterion carries a name, positive marks and a what-it-rewards line.

`test/courseworkCompanion.smoke.test.tsx` renders the tool: the picker lists
real subjects; drilling into one shows component cards with SEC attribution and
the printed criteria behind a toggle.

## Design

Follows the module visual system (CLAUDE.md): accent orange for the brand, the
marks badges and the criteria callouts (tint + accent left-border); neutral
bordered chips for the printed grading table; the source line in label text with
a link to the SEC archive. No dynamic Tailwind class construction. Client-side
only; no persistence.
