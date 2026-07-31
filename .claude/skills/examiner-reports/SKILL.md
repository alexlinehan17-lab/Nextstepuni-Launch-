---
name: examiner-reports
description: How to use the SEC Chief Examiner Report and marking-scheme library in /examiner-reports/. Read before writing common-pitfalls content, commonTraps arrays, topAnswerIncludes insights, subject exam-strategy preambles or trap patterns, and before adding a new report.
---

## Examiner reports library

`/examiner-reports/` holds State Examinations Commission Chief Examiner Reports and marking-scheme commentaries, structured per subject and year:

```
examiner-reports/
├── README.md
├── <subject>/
│   ├── <year>-chief-examiner.pdf      (original PDF, kebab-case subject slug)
│   ├── <year>-chief-examiner.md       (markdown extraction)
│   └── <year>-insights.md             (structured summary — schema below)
```

Multi-year syntheses use `<start-year>-<end-year>-` as the prefix (e.g. `2019-2022-chief-examiner.pdf`).

### Insights file schema

```
# [Subject] [Year] — Examiner Insights

## Source
Report type, year, level(s), original filename, renamed filename, brief
context if relevant (e.g. syllabus changes, cohort shifts).

## Common errors by question type
Broken down by paper section. For each question/area:
- Specific errors examiners flagged (with page refs)
- What separated higher-grade answers from lower-grade ones
- Direct examiner phrasing quoted where useful (with page refs)
Where the report distinguishes between Higher and Ordinary in its
commentary, preserve that distinction.

## Strategic / structural observations
Timing, question choice, rubric handling, anything about exam strategy.

## Misconceptions
Factual or conceptual errors the report flags as widespread.

## Quotable lines
2-3 examiner quotes that would land well in student-facing content
(with page refs).
```

### When to consult the library

When generating any of the following kinds of student-facing content, **read the relevant `<subject>/<year>-insights.md` file first**:

- "Common pitfalls" or "where students lose marks" sections
- `commonTraps` arrays in `data/examQuestions/<subject>.ts` entries
- `topAnswerIncludes` insights for new questions
- Subject strategy preambles in `data/examStrategy/<subject>.ts`
- Trap pattern descriptions in `data/examStrategy/trapPatterns.ts`

The insights file is the curated synthesis. The `<year>-chief-examiner.md` is there for deeper context or for pulling quotes the insights file didn't surface — read it when the insights file points at a section but doesn't quote the exact phrasing you need.

### Adding a new report

1. Drop the PDF into `/tmp/examiner-reports-batch/` (or `~/Downloads/` if staging is informal).
2. Read the cover page to determine subject, year(s), levels.
3. Move into `examiner-reports/<subject>/`, renamed to the canonical filename.
4. Convert to markdown (PyPDF2 if `pdftotext` is unavailable — see prior session for the conversion script pattern).
5. Author the insights file against the schema above.
6. Update `examiner-reports/README.md` index.

### Source types

The library holds two source types per subject/year:

- `<year>-chief-examiner.{pdf,md}` — SEC Chief Examiner's Report
- `<year>-marking-scheme.{pdf,md}` — SEC marking scheme

Both are examiner-authored and citable. Marking schemes are particularly useful for per-question rules ("Max X SRPs if…", "Apply a *", indicative material lists). Cite as `Marking scheme YYYY` inline.
