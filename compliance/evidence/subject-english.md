<!--
 @license
 SPDX-License-Identifier: Apache-2.0
-->

# Evidence Dossier — Mastering English (subject module)

**Module:** `subject-english` (data-driven via `components/SubjectModule.tsx`;
content in `subjectContentLanguages.ts` under key `english`)
**Group:** B (subject-specific) — grounded in official SEC sources, **not**
peer-reviewed psychology journals.
**Review date:** 2026-07-18
**Reviewer:** Pre-accreditation review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what a real, locatable source supports. For this
module the sources are the in-repo SEC English HL 2025 marking scheme and the in-repo
2013 English Chief Examiner's Report (the most recent for LC English). Sources surface
via inline `{{cite:N}}` markers (rendered as `<Cite/>`) + the module-wide **References**
button; data in `data/references/subjectEnglish.ts`. The 2024 HL scheme serves as a
second-year stability check (`examiner-reports/english/2024-verification.md` confirms
the PCLM weightings, primacy-of-P, and section structures are stable across 2024/2025,
and the 2025 OL scheme confirms the same PCLM machinery at Ordinary Level).

**Corrections — this module had factual errors fixed against the 2025 marking scheme,
and strategy advice reversed where it contradicted the Chief Examiner's Report.**
See the table below; all are also logged in `data/cutContent.ts`.

---

## Verified sources

| # | Source | Kind | Locator |
|---|--------|------|---------|
| 1 | SEC English Higher Level 2025 marking scheme — PCLM criteria + 30/30/30/10 weightings and primacy-of-P (p.3), Paper 1 QA/QB structure and same-text prohibition (p.4), Composition theme/texts-as-resource rule (p.13), Single Text 60 (pp.21–22), Comparative 70 + 2025 modes (p.32), Poetry 70 = Unseen 20 + Prescribed 50, both compulsory (p.42), unseen-poetry marking stance (p.42), Language descriptors (Appendix 1, p.50) | official | in-repo `examiner-reports/english/2025-marking-scheme.pdf` (verified directly; distilled in `2025-insights.md`) |
| 2 | SEC English 2013 Chief Examiner's Report — loss of task focus (p.18), banks-of-knowledge caveat (pp.11, 20), formulaic comparative warning (pp.8, 19–20), section averages incl. Comparative weakest / Unseen Poem lowest element (p.7), compulsory-section omissions (pp.8–9, 21), brief-in-the-extreme compositions + genre control (pp.15–16), link-and-cross-reference praise for studied poetry (p.9), overly-literal-reading warning (p.14) | official | in-repo `examiner-reports/english/2013-chief-examiner.pdf` (verified directly; distilled in `2013-insights.md`) |

**Uncited logistical facts.** The paper durations (P1 2h50, P2 3h20) are printed on the
examination papers themselves (mirrored in the app's Paper Trail corpus) and are not
stated in the marking schemes, so they carry no citation. They are stable, publicly
verifiable exam-timetable facts.

---

## Claim-by-claim record

- **§1 How English Actually Works** — Two papers × 200 = 400 marks (**scheme2025**).
  Paper 1: Comprehending 100 = QA 50 (one text) + QB 50 (functional task, different
  text), same-text prohibition; Composition 100, single theme, paper texts usable as a
  resource (**scheme2025**, corrected — ENG-001). Paper 2: Single Text 60; Comparative
  70 with the 2025 modes named; Poetry 70 = Unseen Poem 20 + Prescribed Poetry 50, both
  compulsory (**scheme2025**, corrected — ENG-002). 50/50 paper balance (**scheme2025**).
  Comparative highlight reframed to the examiner's weakest-section finding (ENG-004).
- **§2 What the Examiner Rewards** — PCLM criterion names and 30/30/30/10 weightings
  (**scheme2025**, corrected — ENG-003); primacy-of-P rule (**scheme2025**); Coherence
  descriptors (continuity of argument, sequencing, management of ideas) and Language
  descriptors ("lively interesting phrasing, energy, style") quoted from Appendix 1
  (**scheme2025**). Genre-matching and question-engagement framing supported by the
  criteria descriptors; superlatives softened (ENG-007).
- **§3 Where Your Marks Are** — Composition 100 = 25% (**scheme2025**). Comparative +
  Poetry = 35% (**scheme2025**); formulaic-comparative advice REVERSED to the
  examiner's warning, with the "quality of evidence… significant discriminator" quote
  (**chiefExaminer2013**, ENG-004). Unseen Poem 20 marks, lowest-scoring element,
  compulsory-omission warning (**chiefExaminer2013**); no-single-correct-reading stance
  (**scheme2025**); Prescribed Poetry 50 + link-and-cross-reference praise
  (**chiefExaminer2013**). Section I QA/QB description (**scheme2025**, corrected —
  ENG-001) with the overly-literal-reading warning (**chiefExaminer2013**).
- **§4 What Costs You Marks** — Task-focus and banks-of-knowledge (**chiefExaminer2013**,
  softened — ENG-007). Omission/timing quote (**chiefExaminer2013**); the 55/70/70
  minute split is explicitly framed as an example plan (practical advice, uncited).
  Brief-in-the-extreme + genre-control quotes replace the invented 7–9-paragraph and
  1,000+-word figures (**chiefExaminer2013**, ENG-005). Authentic-voice claim re-anchored
  to the Language descriptor (**scheme2025**).
- **§5 How to Study English** — Timed practice, one-page summaries, quote counts:
  practical study advice (uncited). Comparison grid retained with an anti-formula
  caution (**chiefExaminer2013**). "TPCASLT" branded method replaced with a routine
  built from the scheme's unseen-poetry marking stance, quoted (**scheme2025**,
  ENG-006).
- **§6 Your English Action Plan** — Practical plan; PCLM self-assessment highlight
  updated to the corrected criterion names and weighting (per §2 corrections).

---

## Corrections & reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Corrected | Reason |
|----|---------|----------------------|--------|
| ENG-001 (`subject-english-001`) | §1, §3 | "two comprehension texts (Question A, worth 50 marks each — you do both)" → QA (50, comprehension) + QB (50, functional writing) on different texts, same-text prohibition | 2025 scheme p.4: Section I is QA on one text + QB on a *different* text; QB is functional writing, not a second comprehension QA. |
| ENG-002 (`subject-english-002`) | §1, §3, §4 | "Unseen Poetry … comparison with a second poem — 70 marks" (incl. the invented 20/30/20 split) → Poetry 70 = Unseen Poem 20 + Prescribed Poetry 50, both compulsory | 2025 scheme p.42. The two-poem comparison structure does not exist; 50 of the 70 marks are on studied poets. |
| ENG-003 (`subject-english-003`) | §2 | "Each criterion carries roughly equal weight" → 30/30/30/10 + primacy-of-P; criterion names corrected | 2025 scheme p.3 (confirmed stable in 2024 HL and 2025 OL schemes). |
| ENG-004 (`subject-english-004`) | §1, §3 | "the Comparative is highly formulaic … consistently score well" / "often the highest-scoring section" → weakest-scoring section; formulaic approaches hinder; evidence quality discriminates | 2013 CE report pp.7–8, 18–20 directly contradict the original advice. |
| ENG-005 (`subject-english-005`) | §4 | "seven to nine substantial paragraphs" / "1,000+ words" → the report's qualitative brevity/development principle + genre control | Figures invented; report supports the principle only (pp.15–16). |
| ENG-006 (`subject-english-006`) | §5 | "TPCASLT method" → reading routine grounded in the scheme's unseen-poetry stance | Branded method not locatable in any SEC source; scheme p.42 quoted instead. |
| ENG-007 (`subject-english-007`) | §2, §4 | "the most common reason students lose marks…" / "Every year, the Chief Examiner's Report says…" → softened, attributed to the 2013 report's actual statements | No SEC ranking verifies "most common"; only one (2013) CE report exists for LC English. |

## Outstanding for accreditation

- The 2013 Chief Examiner's Report remains the most recent for LC English; its cohort
  statistics (section averages) predate the 2017 grading-scale change. The module quotes
  its qualitative findings and uses its averages only for relative ordering (weakest
  section, lowest element), which is the reading the report itself gives.
- The comparative modes are stated as the 2025 set ("in 2025 the modes were…") rather
  than implied to be fixed — mode line-ups rotate year to year.
- Paper durations are uncited logistical facts (see note above); if a citable source is
  wanted, the exam papers in the Paper Trail corpus state them on their covers.
