# Strategiser content migration — complete

All Exam Strategiser questions now use the per-prompt `debrief` +
question-level `biggestMistake` schema. The legacy flat
`topAnswerIncludes` / `commonTraps` / `markScheme` fields have been
removed from `types/examStrategiser.ts`, and the `LegacyDebrief`
rendering path has been deleted from `components/ExamStrategiser/stages/DebriefStage.tsx`.
The dev-only console warning that flagged legacy-format questions in
`QuestionPlayer.tsx` has also been removed.

Schema rules: `/CLAUDE.md` § "Strategiser content quality rules".

## Migration history

All 28 questions across 5 subjects migrated:

| Subject   | Questions | Final migration date |
|-----------|-----------|----------------------|
| business  | 4         | 2026-05-06           |
| maths     | 9         | 2026-05-19           |
| english   | 8         | 2026-05-20           |
| geography | 4         | 2026-05-20           |
| irish     | 1         | 2026-05-20           |

## Source citations

Each question's `commonWrongAnswer.source` and `biggestMistake.source`
cites the underlying examiner-authored material:

- **Maths questions** cite the 2015 Chief Examiner Report (the only
  Maths report currently in `/examiner-reports/`). The 2015 CER
  documents perennial OL failure patterns (algebra struggles,
  showing-work conventions, derivative confusion) that apply directly
  to the 2025 OL questions.
- **English, Geography, and Irish questions** cite the SEC marking
  scheme for the relevant year. The data was originally authored
  against the SEC paper + marking scheme per each file's header
  comment; the new schema preserves those citations and reshapes the
  insights into per-prompt strategic principles.
- **Irish placeholder** carries no marking-scheme citation because the
  question itself is a placeholder per the data-file header. The
  debrief content is preserved from the legacy fields; if real Irish
  questions are added later, their debriefs should cite the relevant
  SEC marking schemes.

## Adding new questions

Per `/CLAUDE.md` § "Strategiser content quality rules":

1. Read the relevant `/examiner-reports/<subject>/<year>-insights.md`
   first (or, if no insights file exists, the SEC marking scheme for
   the year).
2. For each predict prompt, author a `debrief` block:
   - `strategicPrinciple`: one short paragraph naming a specific error
     pattern, mark allocation rule, or examiner observation.
   - `commonWrongAnswer.answer`: the wrong answer students typically
     give.
   - `commonWrongAnswer.reason`: why they pick it, with an
     examiner-sourced citation in `source` where possible.
3. Author the question-level `biggestMistake` card:
   - `title`: short headline naming the failure mode.
   - `body`: 2-4 sentences citing the specific marking-scheme rule.
   - `source`: citation (year + type).
4. If an examiner-sourced insight isn't available for a particular
   point, omit `source` rather than filling with generic content.

Banned generic phrases live in `/CLAUDE.md` § "Strategiser content
quality rules" — reject drafts containing them.
