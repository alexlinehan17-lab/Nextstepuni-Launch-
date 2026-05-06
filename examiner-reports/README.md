# Examiner Reports Library

Reference library of State Examinations Commission Chief Examiner Reports
and marking-scheme commentaries. Used as the source-of-truth for "where
students lose marks" / "common pitfalls" content in the Exam Strategiser
(and any other student-facing content that needs examiner backing).

## What lives here

For each subject (`english/`, `maths/`, `business/`, …) and each report year:

- `<year>-chief-examiner.pdf` — original SEC PDF, untouched
- `<year>-chief-examiner.md` — markdown extraction of the PDF (formatting
  approximate; rely on the PDF for definitive rendering)
- `<year>-insights.md` — structured summary against the schema in
  `/CLAUDE.md` § "Examiner reports library"

For multi-year syntheses, the prefix is `<start-year>-<end-year>-` (e.g.
`2019-2022-chief-examiner.pdf`).

## Index

| Subject | Year | Source type | Levels | Original filename | Status |
|---|---|---|---|---|---|
| Maths | 2015 | Chief Examiner | Higher / Ordinary / Foundation | `CHEIFEXAMINERREPORTMATHEMATICS.pdf` | PDF + MD + insights |
| Business | 2015 | Chief Examiner | Higher / Ordinary | `CHIEFEXAMINERREPORTBUSINESS.pdf` | PDF + MD + insights |
| Business | 2025 | Marking scheme | Higher | `BUSINESS HL MARK SCHEME 2025.pdf` | PDF + MD + insights |

_Last updated: 2026-05-06_

## Adding a new report

1. Drop the PDF into `/tmp/examiner-reports-batch/`.
2. Run the conversion pipeline (see `/CLAUDE.md` § "Examiner reports library"
   for the schema and process).
3. Update this index with the new entry.

## Schema reminder — `<year>-insights.md`

```
# [Subject] [Year] — Examiner Insights
## Source
- Report type, year, level, original filename
## Common errors by question type
- Per question type / paper section: errors flagged + what separates
  higher-grade answers from lower-grade ones, with quoted examiner
  phrasing and page refs
## Strategic / structural observations
- Timing, question choice, rubric handling, exam strategy
## Misconceptions
- Factual or conceptual errors flagged as widespread
## Quotable lines
- 2–3 examiner quotes that would land well in student-facing content
  (with page refs)
```

The schema rewards quoted examiner phrasing with page references — those
are the hooks that let downstream content cite the source authoritatively.
