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
