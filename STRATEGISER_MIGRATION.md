# Strategiser content migration

Tracks which questions still use the legacy schema (flat
`topAnswerIncludes` / `commonTraps`) versus the new per-prompt
`debrief` + question-level `biggestMistake` shape.

Schema rules: `/CLAUDE.md` § "Strategiser content quality rules".

In dev mode, loading a legacy-format question prints a console warning
naming the question id. Production console stays clean.

## Status

| ID                            | Subject   | Status | Migrated |
|-------------------------------|-----------|--------|----------|
| english-2025-p1-text1-qa-iii  | english   | legacy | —        |
| english-2025-p1-text2-qb      | english   | legacy | —        |
| english-2025-p1-composing-2   | english   | legacy | —        |
| english-2025-p1-composing-3   | english   | legacy | —        |
| english-2024-p1-text1-qa-i    | english   | legacy | —        |
| english-2024-p1-text1-qa-ii   | english   | legacy | —        |
| english-2024-p1-text2-qb      | english   | legacy | —        |
| english-2024-p1-composing-5   | english   | legacy | —        |
| irish-placeholder-2024-p2-q1  | irish     | legacy | —        |
| maths-placeholder-2024-p1-q1  | maths     | legacy | —        |
| maths-2025-ord-p1-q3          | maths     | legacy | —        |
| maths-2025-ord-p1-q4          | maths     | legacy | —        |
| maths-2025-ord-p1-q7          | maths     | legacy | —        |
| maths-2025-ord-p1-q8          | maths     | legacy | —        |
| maths-2025-ord-p2-q7          | maths     | legacy | —        |
| maths-2025-ord-p2-q8          | maths     | legacy | —        |
| maths-2025-ord-p2-q9          | maths     | legacy | —        |
| maths-2025-ord-p2-q10         | maths     | legacy | —        |
| geo-2025-hl-q1c               | geography | legacy | —        |
| geo-2025-hl-q2bi              | geography | legacy | —        |
| geo-2025-hl-q2c               | geography | legacy | —        |
| geo-2025-hl-q4b               | geography | legacy | —        |
| business-2025-hl-s1-q7        | business  | migrated | 2026-05-06 |
| business-2025-hl-s2-abq       | business  | migrated | 2026-05-06 |
| business-2025-hl-s3-q1        | business  | migrated | 2026-05-06 |
| business-2025-hl-s3-q8        | business  | migrated | 2026-05-06 |

_Last updated: 2026-05-06_

## Workflow per question

1. Pick a question to migrate.
2. Read `/examiner-reports/<subject>/` for citable insights — both
   chief-examiner reports and marking-scheme commentaries.
3. For each predict prompt, author a `debrief` block:
   - `strategicPrinciple`: one short line on what the prompt is testing.
   - `commonWrongAnswer`: the answer + reason students pick it +
     `source` citation (year + type) where possible.
4. Author the question-level `biggestMistake` card:
   - `title`: short headline.
   - `body`: 2-4 sentences.
   - `source` citation where possible.
5. Remove the question's `topAnswerIncludes`, `commonTraps`, `markScheme`.
6. Update this file: change status to `migrated`, set the migration date.

## Reminders

- Banned generic phrases live in `/CLAUDE.md` § "Strategiser content quality
  rules". Reject drafts containing them.
- If you can't find an examiner-sourced insight for a particular point,
  flag it (`source` omitted) rather than filling with generic content.
- Marking schemes are also examiner-authored — `Marking scheme YYYY` is a
  valid citation.
