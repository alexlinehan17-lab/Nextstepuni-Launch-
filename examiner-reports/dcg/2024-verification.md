# DCG Examiner's Chair — Second-Year Verification (2024 vs 2025)

**Purpose.** `data/examinersChair/dcg.ts` teaches three load-bearing DCG marking
rules, each cited to the **SEC LC DCG HL marking scheme 2025**
(`examiner-reports/dcg/2025-marking-scheme.*`). This document checks whether
those rules are **stable across a second year** by cross-referencing the
independently retrieved **SEC LC DCG HL marking scheme 2024**.

## Source retrieved for this check

- SEC, *Leaving Certificate 2024 Marking Scheme — Higher Level — Design and
  Communication Graphics*.
- Retrieved 2026-07-06 from the educateplus.ie mirror
  `https://www.educateplus.ie/sites/default/files/storage/DCG%20HL.pdf`
  (cover page confirms "Leaving Certificate 2024 … Higher Level … Design and
  Communication Graphics"). Saved as `2024-marking-scheme.pdf`; text extracted
  with PyPDF2 to `2024-marking-scheme.md` (28 pages, `<!-- page N -->` markers;
  the drawing/solution pages 15–28 are images with no extractable text, same as
  the 2025 file).

**Retrieval succeeded** — this is a genuine second-source cross-year check, not a
logical-only fallback.

## What "stable" means here

The `dcg.ts` citations name specific 2025 question labels and PDF pages
(e.g. "p.4 … A-2"). Those coordinates are **intentionally 2025-specific** — the
SEC re-numbers questions and re-paginates every year. The load-bearing claim is
the **marking grammar**, not the coordinates. So the test is: does each rule's
marking convention recur in 2024, at whatever question it happens to land on?

## Rule-by-rule result

| # | Rule taught in `dcg.ts` | 2025 evidence (as cited) | 2024 evidence (this check) | Verdict |
|---|--------------------------|--------------------------|-----------------------------|---------|
| **DCG1** | Construction is marked **separately from — and usually above** — the finished curve; erasing construction forfeits the larger award. | Q A-2, PDF p.4: "(ii) Construction to locate points above the major axis … **8**" vs "(iv) Draw curve … **4**" (8 > 4). | Q B-2(b), PDF p.7: "(vii) Construction to determine points on ellipse … **8**" vs "(viii) Draw elliptical curve …(any = 1) … **3**" (8 > 3). Same pattern at C-4(a): "(iv) Locate points on the locus … **12**" vs "(v) Draw required epicycloid (any = 1) … **4**"; A-4 sphere construction; C-2. Construction consistently out-scores the curve, listed as its own granule. | **STABLE** |
| **DCG2** | Every question is decomposed into **named steps, each scored independently**; no all-or-nothing drawing parts — a partial attempt banks the steps it reaches. | Q A-1…C-5, PDF p.4–13: every part broken into (i),(ii),(iii)… each carrying its own mark. | Q A-1…C-5, PDF p.4–13: identical structure — every one of the 15 questions is split into individually-marked sub-steps (e.g. C-3 has (i)–(xvii); C-5 assembly marked component-by-component). No question is scored as a single lump. | **STABLE** |
| **DCG3** | The scheme awards a **standalone "use of appropriate method" mark**, separate from getting the final answer — so a correct method shown scores even if unfinished. | Q A-4, cited p.4: "Use of appropriate method to determine … **2**" granules, listed separately from the "Location of point"/"Draw" marks. | Q C-3(d), PDF p.11: "(xvi) **Use of appropriate method to determine** the inclination of leg to HP … **2**" listed *separately* from "(xvii) Determine and indicate the inclination of leg to HP … **3**". The method is scored on its own, ahead of the result. (Cf. also "(xi) Use of line joining B and D…" C-2.) | **STABLE** |

## Notes & minor observations (no action required)

- **Curve granularity reinforces DCG1.** The 2024 scheme repeatedly tags the
  final-curve step "(any = 1)" (e.g. B-2 viii, C-2 x, C-4 v). This means even a
  single correct portion of the drawn curve earns a mark — underscoring that the
  bulk of the award sits in the *construction*, exactly as DCG1 teaches. This is
  additional supporting evidence, not a contradiction.

- **The "worth twice" figure is example-bound, not a universal claim.** DCG1's
  grid `ruleNote` says "The construction is worth twice the finished curve" —
  but that describes the **authored** 8+4 scenario (`questionNote` flags the
  scenario as authored), which matches 2025 A-2's 8/4 exactly. The *general*
  claim actually asserted in the takeaway is softer — "it's usually worth more"
  — and that holds in 2024 (8 > 3, 12 > 4) as well as 2025 (8 > 4). No overreach.

- **Page-cite nuance in the source file (pre-existing, out of scope).** In the
  2025 PDF, question A-4 sits on PDF page 5 (printed "- 2 -"), whereas DCG3 cites
  it as "p.4". A-2 (DCG1) genuinely is on PDF page 4. This is an intra-2025
  pagination nit in the existing citation, unrelated to cross-year stability, and
  the task scope forbids editing `dcg.ts`; flagged here for the record only.

## Confidence

**High.** All three load-bearing rules reproduce in the independently retrieved
2024 HL scheme, at different question numbers/pages (as expected), with the exact
same marking grammar. The rules describe the standing SEC DCG marking system, not
a one-year artefact.

## Conclusion

**All rules stable.** No reframe of `data/examinersChair/dcg.ts` is warranted.
The 2025 citations remain correct *as 2025 citations*; the conventions they cite
are corroborated by the 2024 scheme.
