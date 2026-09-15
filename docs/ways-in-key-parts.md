# Ways In — the key parts of a question

`components/WaysIn/keyParts.ts` turns a Mark Bank question into the parts a
teacher would point at before the student writes anything. The panel's first
stage, **Break it down**, shows them; **Plan** gives one space per part.

## What a part is

| Slot | What it holds | Example |
|---|---|---|
| Do | the command, with a one-line meaning of what it asks for | Discuss in detail — *Several developed points, with reasons or examples.* |
| Item | the printed item this part covers, when the paper prints a list | Commission |
| How many | the printed count | three functional requirements |
| About | what the answer is about; `…` joins words that resume after a limit | conditions … that are necessary for price discrimination to occur |
| Only counts if | the limits that decide what earns marks | using notes and freehand sketches |
| Given | values for a calculation | a half-life of 8 days |
| Use | supplied material, options to choose from, where to look | Fig. C-2 · (paragraph 6) |

## Rules nothing may break

- **Every slot is lifted.** Each value is a character range of the printed
  stem or question (`KPSpan.start/end`). Only the command's meaning is
  written by us. `test/waysInKeyParts.test.ts` checks this on every card.
- **Nothing hints at the answer.** A given about the very quantity being
  asked for is never attached; the marking scheme is never read.
- **Nothing printed is dropped.** A part or clause with an instruction the
  parser cannot read honestly is shown as printed (`as-printed`). A whole
  card in the exam language, or garbled, falls back to the printed question.

## Shapes it handles

- Lists after a colon, bullets, lines, `(i)…(iv)` parts under a lead-in and
  "the terms X and Y" give one part per item. "Any two of the following"
  keeps the list as options and plans two spaces.
- A lead-in's instruction and limits reach the parts after it ("Circle the
  correct option in each of the following statements", "Answer each of the
  following with reference to a European region (not in Ireland) that you
  have studied").
- Yes/no, either/or and quiz questions; the statement before "Do you agree?"
  or "Give details."; "Name two." after a question; "Give your answer in its
  simplest form" as a limit on the calculation before it.
- Plan rows come from the parts: one per item, heading or counted point.

## How it is measured

- `test/waysInKeyPartsGold.test.ts` scores the parser against 220
  hand-written breakdowns (`test/fixtures/waysInKeyPartsGold.json`) and
  fails if any slot drops below its floor.
- Changes were driven by students' readings: batches of 150 unseen cards,
  each judged good / ok / confusing / wrong, with every "wrong" put to a
  skeptical examiner before it counted. When changing the parser, check a
  fresh sample the same way; the gold set alone rewards matching a format.

## Card data it cannot fix

The breakdown only reads the card's own text. Faults found in the text
itself — a question paraphrased when split per option, a stem that lost its
`(i)/(ii)` labels, a question cut off before its ask, a flattened exponent —
have to be fixed in the card.
