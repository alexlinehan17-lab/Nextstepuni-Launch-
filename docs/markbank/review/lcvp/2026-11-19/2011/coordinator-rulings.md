# Third reader decisions, 19 November 2026 (Link Modules and Russian)

Claude, as third reader for the Claude coordinator, settled every split and filing difference in the eight packets
Codex filed. Each decision was made from the printed paper page and the scheme page, not by averaging or majority.
Decisions sit beside each packet's input as `third-reader-decision.json` (same item ids; fields id, decision, reason,
agreesWith). For Russian there is no `third-reader-input.json`; the file sits beside `adjudication.json`. No card,
branch or worktree was changed and no SEC request was made.

"A" is the first or root reader, "B" the second reader. For Russian, "A" is the existing filing (PR R's
`russian.json`) and "B" is Codex's independent proposal.

## Counts

| Packet | Items | Agree A | Agree B | Both readers already agreed | Neither |
|---|---|---|---|---|---|
| Link Modules 2010 (`lcvp-2010-independent`) | 7 (5 filings, 2 splits) | 3 | 4 | 0 | 0 |
| Link Modules 2011 (`lcvp-2011-independent`) | 10 filings | 2 | 8 | 0 | 0 |
| Link Modules 2012 (`lcvp-2012-independent`) | 5 filings | 3 | 2 | 0 | 0 |
| Link Modules 2013 (`lcvp-2013-source-reading`) | 5 (4 filings, 1 split question) | 1 | 3 | 1 | 0 |
| Link Modules 2014 (`lcvp-release`) | 10 filings | 2 | 8 | 0 | 0 |
| Link Modules 2022 deferred | 17 (12 filings, 4 splits, 1 split check) | 8 | 8 | 1 | 0 |
| Link Modules 2023 deferred | 8 (6 filings, 2 split checks) | 2 | 4 | 2 | 0 |
| Russian (`russian-independent-category`) | 15 filings | 2 | 12 | 1 | 0 |
| **Total** | **77** | **23** | **49** | **5** | **0** |

What the split decisions do to each sitting's number of asks:
- **2010:** B2(i) becomes two cards (County Enterprise Board 3 marks, County Council 3 marks). C3(a) becomes three cards
  (CV, referees, equal opportunities employer, 2 marks each). That gives 48 asks, the root reader's count.
- **2013:** C5(d) ("State and explain three types of advertising") stays one 6-mark card. The count stays at 41.
- **2022 deferred:**
  - B3(i) is confirmed as two cards (one positive effect, one negative effect, 2 marks each).
  - C6(c) splits 4 + 4 (state four sources, then how each was relevant). It prints two separate instructions.
  - B3(ii), C3(c) and C7(c) stay whole. Each is a single "identify and explain" or "identify and describe" instruction.
  - That gives **48 asks**, one more than the root's 47 and three fewer than the second reader's 51. The offered marks
    are unchanged.
- **2023 deferred:** B2(ii) is confirmed as 3 + 3 and C6(b) as 2 + 2 (skills, qualities). The count stays at 50.

## Rules applied the same way in every Link Modules packet

1. **Splitting (R7).** An item gets its own card when the paper names it or prints it as its own instruction, and
   the scheme gives it its own marks. Examples: "one positive and one negative"; two named organisations; three
   underlined terms; "State four sources. Outline how each was relevant." A single "identify and explain N" or
   "state and explain N" instruction stays one card: its (1+1) is the inside of each answer point. A printed choice
   ("explain three of the following") is always one card.
2. **Audio Visual and Case Study** are exam-section headings.
   - An ask keeps one of them when the scheme's answers are recall of the recording or the printed case. Examples:
     why Michael won't emigrate; how Aoife prepared.
   - An ask that tests Link Module content goes under that content heading, even inside Section A or B. This follows
     the model lane's own earlier third readings (2015 A5, 2021 A7, 2022 B1).
3. **An ask is filed with its activity.** Evaluating or planning a specific activity goes under that activity's unit:
   - a visit-out to a business: Local Business Enterprises;
   - a voluntary organisation's visit-in: Local Voluntary/Community Enterprises;
   - the class enterprise: An Enterprise Activity.

   This matches the live 2015 to 2026 filings. Where a live card asks nearly the same thing, the same heading was used.
4. **Printed choices spanning several units** follow READING.md rule 6: the two headings that cover most options,
   flagged CHOICE SPANS (2013 B1, 2022 deferred B1).

## Not settled, or needing someone else

- **Russian `ru-2015-hl-l3-3`** is one card covering two printed parts with a shared 8-mark cap. Codex asked to show
  each part under its own heading.
  - Taken alone, part 3(i) (boxing in Ireland and Georgia) would be Leisure Pursuits, not Relations With Ireland.
  - The model allows at most two headings, and listening cards already use one for "Learning From Target-Language
    Material".
  - Showing each part under its own heading is a model or shared-code question for the coordinator. Until then the
    card stays filed as Work plus that listening heading. The shared cap stays: no 2/6 split was invented.
- **Russian live cards.** 11 of the Russian decisions move the displayed heading of a card that is live today. Each
  needs Alex's approval before it changes (the stop rule). The Link Modules asks are all new cards, so they need no
  approval.

## Inconsistencies found that the coordinator should settle subject-wide (not part of any packet)

- **Section A recall in the newer readings.** In the 2010 to 2013 and deferred readings, both readers agreed to file
  several pure-recall Section A asks under content headings. Examples: 2010 A1 under Career Investigation; 2011 A1 to
  A6 all under Local Voluntary/Community Enterprises. 2014 and 2015 to 2026 file recall under Audio Visual. These were
  agreed, not disputed, so I did not change them. They should be read once against rule 2 above.
- **Live Section A and B filings were never read.** Of the live 2015 to 2026 filings, 101 of 103 Section A asks sit
  under Audio Visual and 65 of 72 Section B asks under Case Study. These are defaults from the evidence (code `xa`).
  Under R9 many of them test content: the live Section B "explain three of the following terms" cards are one example.
- **Market research** is filed under Enterprise Skills in the new sittings (2013 Q5(b), 2022 deferred Q7(a)-(b),
  which both readers agreed, and 2014 B2(i) here). The live 2015, 2019 and 2026 market-research cards are under An
  Enterprise Activity. One heading should be chosen for the whole subject.
- **Per-option cards for term choices.** BRIEF rule 5 would allow a card per option when the options sit under
  different topics (2013 B1, 2022 deferred B1). I kept each as one card. If the coordinator wants per-option cards,
  the live term-choice cards should change at the same time.
- **Russian twins.** Similar asks outside the 15 are now filed differently from their twins:
  - `ru-2017-hl-l1-2` (Higher Bloomsday) is under Events in People's Lives, while its Ordinary twin now goes under
    Relations With Ireland.
  - `ru-2011-hl-l4-3` (Higher, cast of Annie) is under Work, while its Ordinary twin goes under Leisure Pursuits.

## Coordinator rulings on the open points (19 Nov 2026, ~19:40 UTC)
1. The 11 Russian decisions that move a live card's heading need no separate approval: Alex approved the single Mark
   Bank / Topic Atlas model on 18 Nov, including re-filing live cards part by part (the rollout has already moved 2,622
   parts). Ids, conceptIds, marks and rows do not change.
2. `ru-2015-hl-l3-3` (two printed parts sharing one 8-mark cap): keep the interim filing (Work plus the listening
   heading), no invented split. A third heading is not added to the model; revisit in the Phase 4 split sweep.
3. Link Modules, subject-wide: Audio Visual and Case Study headings only where the ask is recall of the recording or
   the printed case; anything testing module content goes under its content heading (the third reader's rule, already
   used by the model lane's earlier third readings). The live 2015-2026 Section A/B filings that were assigned from
   evidence and never read are re-read under this rule by the model lane in PR R, with a second reading on every move.
4. Market research is filed under An Enterprise Activity (the unit whose activity it plans or evaluates), matching the
   live cards and the "planning or evaluating an activity" rule; the new sittings follow this.
5. "Explain three of the following terms" stays one card (a printed choice, R7). Live cards stay as they are.
6. Russian twins: `ru-2017-hl-l1-2` and `ru-2011-hl-l4-3` take the same heading as the decided Ordinary ask they
   repeat (same ask, same heading).
Codex: treat the third-reader decisions plus these rulings as final for your LCVP and Russian batches.
