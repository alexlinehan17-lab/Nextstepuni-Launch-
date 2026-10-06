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

## Approved module review — 5–6 October 2026

- Never use emojis. Use the established hand-drawn artwork, paper/charcoal
  surfaces and orange accent. Scaffolding Your Focus and its A small beginning
  prompt use the regular thinker sitting on the orange star, not a timer.
- Controls must look clickable before hover. Selected answers need strong
  orange, mint or coral faces with contrasting text in both themes. Keep locked
  answers readable and triage choice/progress dots visible on selected fills.
- Keep compact citation bubbles and their animation. Definitions stay compact,
  bounded by the viewport, and only one remains open at a time.
- Preserve the bridge animation, Thought Reframer circular switches, Kobra OTP,
  flip interaction, flat orange activity ring, repeated-plan confirmation,
  segmented study-session bar and blocked/interleaved schedule layout.
- Bars use outlined tracks and coloured fills with aligned labels. Chart axes
  and ticks use quiet type sized for the rendered chart, including phones.
  Keep scales, units/context, grids and source data. Scale labels stay outside
  rotating balance illustrations; ring scores are centred geometrically.
- Correct Driver vs Passenger placements after the full sort. Backwards
  planning supports mouse, touch, keyboard and visible move controls.
- Yet examples describe skills that naturally accept "yet". Show instructions
  once, separately from the exercise. Bring Program Your Destination closer
  to A small beginning; centre the weekly location planner.
- Reuse onboarding current/target grades. Remove the duplicate CAO input
  calculator, Build Your WRAP exercise/section and the support-advice block.
- Breathing instructions sit outside the animated ring with a separate Begin
  button and clear timing.
- Defer subject Mastering exercises. This review includes general active recall,
  spacing and interleaving exercises explicitly reviewed by Alex.
- Research figures must retain primary-source context. Roediger & Karpicke
  (2006), Experiment 2 reports independent group averages of 40% and 61% of
  passage ideas recalled after one week: four reading periods versus one
  reading period plus three recall tests. Reading lasted 5 minutes per period;
  tests lasted 10 minutes. Do not describe these as equal study time.
- New instructions from Alex supersede these recorded decisions.
