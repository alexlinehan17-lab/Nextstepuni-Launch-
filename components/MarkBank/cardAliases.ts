/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Stable progress aliases for cards consolidated after the paper-level audit.
 * Most rows come from scripts/markbank/card-corrections.json; the rest are
 * re-citations, where an author stopped emitting an id because the citation on
 * it was wrong. Those cannot live in the corrections file, which refuses an
 * entry for a card its generator no longer emits. Either way old review memory
 * is read by the surviving canonical card and is never silently discarded.
 */
export const CARD_ID_ALIASES: Readonly<Record<string, string>> = {
  // Re-citation. "am-2021-hl-2" cited the whole of 2021 Higher Question 2
  // while holding only its (a)(i) and (a)(ii) — Q2(b), the other 25 marks, was
  // already a separate card. It cited the question that way because the SCHEME
  // heads those two romans "(i)" and "(ii)" with no part letter, so the author
  // could not match them to the paper's Q2(a) and fell back to carding the
  // question whole. They are now am-2021-hl-2-a-i and am-2021-hl-2-a-ii;
  // progress follows the first of them.
  "am-2021-hl-2": "am-2021-hl-2-a-i",
  "chem-2023-ol-q10-a-iii-iv-fig": "chem-2023-ol-q10-a-iii-iv",
  "chem-2023-ol-q6-b-i-iv": "chem-2023-ol-q6-b",
  "english-2022-ol-p1-t2-a-iii-a": "english-2022-ol-p1-t1-a-iii-a",
  "english-2022-ol-p1-t2-a-iii-b": "english-2022-ol-p1-t1-a-iii-b",
  "english-2022-ol-p1-t3-a-iii-a": "english-2022-ol-p1-t1-a-iii-a",
  "english-2022-ol-p1-t3-a-iii-b": "english-2022-ol-p1-t1-a-iii-b",
  "english-2023-ol-p1-t2-a-iii-a": "english-2023-ol-p1-t1-a-iii-a",
  "english-2023-ol-p1-t3-a-iii-a": "english-2023-ol-p1-t1-a-iii-a",
  "english-2024-ol-p1-t2-a-iii-a": "english-2024-ol-p1-t1-a-iii-a",
  "english-2024-ol-p1-t3-a-iii-a": "english-2024-ol-p1-t1-a-iii-a",
  "english-2025-ol-p1-t2-a-iii-b": "english-2025-ol-p1-t1-a-iii-b",
  "english-2025-ol-p1-t3-a-iii-b": "english-2025-ol-p1-t1-a-iii-b",
  "he-2023-hl-sc-q2b-cotton-polyester": "he-2023-hl-sc-q2b-wool-nylon",
  "he-2023-hl-sc-q4aii-braising": "he-2023-hl-sc-q4aii-boiling",
  "he-2023-hl-sc-q4aii-frying": "he-2023-hl-sc-q4aii-boiling",
  "he-2023-hl-sc-q4aii-grilling-barbecuing": "he-2023-hl-sc-q4aii-boiling",
  "he-2023-hl-sc-q4aii-poaching": "he-2023-hl-sc-q4aii-boiling",
  "he-2023-hl-sc-q4aii-pressure-cooking": "he-2023-hl-sc-q4aii-boiling",
  "he-2023-hl-sc-q4aii-roasting": "he-2023-hl-sc-q4aii-boiling",
  "he-2023-hl-sc-q4aii-steaming": "he-2023-hl-sc-q4aii-boiling",
  "he-2023-hl-sc-q4aii-stewing": "he-2023-hl-sc-q4aii-boiling",
  "he-2023-hl-sc-q4aiii-metal": "he-2023-hl-sc-q4aiii-glass",
  "he-2023-hl-sc-q4aiii-paper": "he-2023-hl-sc-q4aiii-glass",
  "he-2023-hl-sc-q4aiii-plastic": "he-2023-hl-sc-q4aiii-glass",
  "he-2024-hl-sc-q2b-cotton": "he-2024-hl-sc-q2b-wool",
  "he-2024-hl-sc-q2b-linen": "he-2024-hl-sc-q2b-wool",
  "he-2024-hl-sc-q2b-silk": "he-2024-hl-sc-q2b-wool",
  "he-2024-ol-sc-q2b-cotton": "he-2024-ol-sc-q2b-linen",
  "he-2024-ol-sc-q2b-silk": "he-2024-ol-sc-q2b-linen",
  "he-2024-ol-sc-q2b-wool": "he-2024-ol-sc-q2b-linen",
  "he-2024-ol-sc-q4aii-condensed": "he-2024-ol-sc-q4aii-pasteurisation",
  "he-2024-ol-sc-q4aii-evaporated": "he-2024-ol-sc-q4aii-pasteurisation",
  "he-2024-ol-sc-q4aii-sterilisation": "he-2024-ol-sc-q4aii-pasteurisation",
  "he-2024-ol-sc-q4aii-uht": "he-2024-ol-sc-q4aii-pasteurisation"
};
