# NextStepUni repository invariants

## Curriculum and Mark Bank

- Treat Curriculum Online/NCCA as the authority for curriculum content,
  hierarchy, specification transitions and assessment rules. Treat SEC papers
  and marking schemes as the authority for year-specific examination material.
- Resolve curriculum data through `curriculumRegistry.ts` using subject and
  examination year. Do not add a feature-local syllabus, strand or topic array.
- Store and join curriculum data with stable `specificationId` and canonical
  node IDs. Display names are labels/aliases, never durable identifiers.
- A curriculum migration must not delete, omit, overwrite or silently hide any
  Mark Bank card. Topic remapping changes card metadata only; card IDs and card
  content remain intact unless an independently verified correction is required.
- Run `test/markBankCardPreservation.test.ts`,
  `test/curriculumRegistry.test.ts`, and `test/markBankDeck.test.ts` after any
  curriculum, taxonomy, deck-generation or Mark Bank change.
- The preservation baseline may only be updated deliberately after confirming
  that every previous card still exists. A normal curriculum migration must not
  update the baseline merely to make a failing test pass.

## Exam-corpus completeness

- Never use the number of printed questions, generated cards, or a census made
  by the same parser as independent proof that a subject is complete. Before a
  completion claim, sweep every paper visually and cross-check each candidate
  card boundary against its marking scheme.
- The card unit is one independently selectable, separately practicable task at
  a published mark boundary—not necessarily one numbered question. Use the
  scheme's allocation to decide whether printed parts split or remain one
  holistic response.
- Expand every finite printed answer route. A closed choose-one pool of `n`
  options yields `n` cards; a closed choose-`k` pool yields `C(n, k)` cards.
  Derive these variants mechanically and pin their count, unique IDs, wording
  and tariff in tests.
- Apply selection analysis inside every split task, not just at the outer
  numbered-question level. The Art corpus previously handled separately marked
  parts and choose-one questions but missed the task-internal "any two of five"
  instruction in 2025 OL Q4(a), collapsing ten valid routes into one.
- Do not fan out required headings, illustrative example lists, open choices
  such as a named artist or work, or flexible wording such as `and/or`. Those
  remain one response unless the paper requires a fixed finite selection. Keep
  a reviewed, written reason beside any finite-looking pool that is deliberately
  not expanded.
- Scan raw extracted paper wording for selection directives such as `choose`,
  `one of`, `any N`, `either/or`, and `answer X of Y`; generation must fail when
  one is unclassified. A hand-written expansion map must also fail when its key
  no longer matches the source paper.
- When a task is split or expanded, carry all required stem context, source
  pages or illustrations, scheme criteria and marks into every resulting card.
  Alternative routes each retain the route tariff; their marks are never added
  together as though a candidate answered every alternative.
- Update coverage and preservation baselines only after the paper/scheme sweep,
  old-ID preservation check, zero-open/zero-orphan reconciliation, and targeted
  regression tests all pass.

## Design language

- Do not use the generic "AI callout" composition: a softly tinted rounded
  rectangle, decorative coloured side rail, stock icon and heading/body copy.
  It reads as generated filler and is not part of the NextStepUni brand.
- Do not add lightning, sparkle, rocket or similar stock icons merely to make
  explanatory copy feel more important. Icons must communicate a real control,
  state or subject; illustrative feature artwork follows the established
  hand-drawn icon system.
- Prefer editorial hierarchy on paper: an eyebrow, serif heading, concise copy,
  deliberate whitespace and a simple divider. Where containment is useful, use
  the established full charcoal or orange outline treatment rather than a
  decorative side stripe.
- Semantic warnings and errors may use colour when it communicates meaning, but
  they must not be styled as decorative feature banners.
- Never repeat the same label as both context and detail (for example, "Your
  current grades · your current grades"). Every phrase in a line must add new
  information.
