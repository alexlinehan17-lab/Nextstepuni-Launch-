# Applied Mathematics — Examiner's Chair second-year verification (2023 vs cited 2024)

**Purpose.** `data/examinersChair/appliedmaths.ts` cites its marking rules to the **SEC LC Applied
Mathematics HL marking scheme 2024**. This document cross-checks each load-bearing rule against a
**different year's** scheme — the **2023 HL marking scheme** — to establish whether each rule is a
*standing convention* (year-stable) or a *year-specific detail*.

- **Cited (primary) source:** SEC LC Applied Mathematics HL marking scheme **2024** —
  `examiner-reports/applied-maths/2024-marking-scheme.{pdf,md}`
- **Second (verification) source:** SEC LC Applied Mathematics HL marking scheme **2023** —
  `examiner-reports/applied-maths/2023-marking-scheme.{pdf,md}`
  (downloaded this session from the educateplus.ie SEC mirror:
  `https://www.educateplus.ie/sites/default/files/storage/Applied%20Maths%202023%20HL.pdf`;
  cover page confirms "Coimisiún na Scrúduithe Stáit — Leaving Certificate 2023 — Marking Scheme —
  Higher Level — Applied Mathematics"). Retrieval date 2026-07-06.
- Both schemes are on the **revised Applied Mathematics specification** (first examined 2023), so the
  cross-year comparison stays within the current spec, as required.

Page references below are PDF page order (matching the `<!-- page N -->` markers in each `.md`).

---

## Load-bearing rules asserted by `appliedmaths.ts`

| # | Session | Rule as taught | Cite in `appliedmaths.ts` (2024) |
|---|---------|----------------|----------------------------------|
| R1 | AM1 (`am-blunder-slip`) | Subtractive penalty tariff: **blunder −3, slip −1, misreading −1**, applied down from full marks; a slip/misreading/omission that *oversimplifies* is upgraded to a blunder. "A blunder costs 3× a slip." | `p.3 (instruction 4, penalty tariff)`; takeaway/embodies → `p.3` |
| R2 | AM2 (`am-scale-floor`) | On a **systemic-error marking scale** a genuine attempt always banks a floor: a valid attempt banks the bottom rung and evident method with several errors still scores well above zero. Illustrated with a **30-mark scale = 27 / 24 / 16 / 8** (one error / two / more-than-two-with-method / valid attempt). | `p.3, p.13 (systemic-error marking scales)`; takeaways/embodies → `p.3` |
| R3 | AM3 (`am-name-method`) | **"Allow 3 marks for the name of a correct algorithm if no other work is presented"**, and omitting/mis-naming the algorithm where required is a specific **−3** ("Deduct 3 marks if the algorithm used is not correctly named"). | `p.6 (3 marks for naming a correct algorithm)`; takeaway/embodies → `p.6` |

---

## Rule-by-rule cross-year result

| Rule | Cited in `appliedmaths.ts` | Second source — 2023 scheme (page) | Verdict | Note |
|------|----------------------------|-------------------------------------|---------|------|
| **R1 — Penalty tariff (blunder −3 / slip −1 / misreading −1) + oversimplifying-slip upgrade** | 2024 scheme **p.3**, General Instruction **4** (tariff) and **5** (oversimplifying slip → treated as blunder) | 2023 scheme **p.3**, General Instructions **4 and 5** — text is **verbatim identical**: "mathematical error ('blunder') –3 / mathematical/numerical slip –1 / misreading (if not serious or leading to oversimplification) –1"; and "A misreading or slip or omission which oversimplifies the question may be regarded as equivalent to a mathematical error and is marked accordingly." | **STABLE** | Standing convention. Same wording, same page number (p.3, instructions 4 & 5) in both years. The AM1 arithmetic (10−1=9, 10−3=7) is a direct application of the tariff and carries over unchanged. |
| **R2 — Systemic-error scale: a valid attempt always banks a floor** (the taught principle) | 2024 scheme **p.3** (Instruction 6) + **p.13** (a real 30-mark scale item `[0/8/16/24/27]`) | 2023 scheme **p.3**, General Instruction **6**: every marking scale carries a **"valid attempt" bottom rung** and a graded ladder above it (20-mark → 17/14/8; 15-mark → 12/9/6; 10-mark → 7/4). Body scale items confirm the pattern: `[0/4/7]` (p.6), `[0/8/14/17]` (p.7, p.15), `[0/6/9/12]` (p.12). | **STABLE** | The *principle the module teaches* — "a genuine attempt is never worth zero; a valid attempt banks the bottom rung; evident method scores well above zero" — holds in every scale of both years. |
| **R2b — the *specific* 30-mark scale values 27 / 24 / 16 / 8, incl. the "more-than-two-errors → 16" rung** | 2024 scheme **p.3** (Instruction 6 lists a 30-mark scale) + **p.13** (30-mark item marked `[0/8/16/24/27]`) | **Not present in 2023.** The 2023 General Instructions (p.3, Instruction 6) list **only** 20-, 15- and 10-mark scales — there is **no 30-mark scale**. No 30-mark scale item appears anywhere in the 2023 body (bracket scales found: `[0/4/7]`, `[0/8/14/17]`, `[0/6/9/12]` only). Corroborating evidence that the exact rungs are year-variable: the **15-mark scale changed between years** — 2023 = **12/9/6** (three rungs) vs 2024 = **12/6** (two rungs). | **YEAR-SPECIFIC (correctly attributed)** | The 30-mark `27/24/16/8` ladder — and the distinctive "more than two errors but evidence of correct method → 16" rung the AM2 script leans on — is a **2024 detail**, not a standing convention. It is, however, **cited specifically to the 2024 scheme** and the scenario is explicitly labelled "authored for this exercise", so the citation is accurate and not overclaimed. No edit is *required*; see optional reframe below if a year-agnostic scenario is preferred. |
| **R3 — "3 marks for naming a correct algorithm; −3 for not correctly naming it"** | 2024 scheme **p.6** (item 1(b)(i)) | 2023 scheme **p.12** (item 7(a)(i), a 15-mark scale MST item) — **verbatim identical** both sentences: "Deduct 3 marks if the algorithm used is not correctly named." and "Allow 3 marks for the name of a correct algorithm if no other work is presented." | **STABLE** | Standing convention applied to the graph/network (MST) questions in both years. Only the page number differs (2024 p.6 vs 2023 p.12); the rule text is identical. |

---

## Conclusion

- **R1 (blunder/slip/misreading tariff + oversimplification upgrade): STABLE** — verbatim in both years' General Instructions (p.3, items 4–5).
- **R3 (name-of-algorithm ±3): STABLE** — verbatim in both years (2024 p.6 / 2023 p.12).
- **R2 (systemic-error scale floor): the taught rule is STABLE** — every scale in both years has a valid-attempt floor and a graded ladder. The *specific* 30-mark `27/24/16/8` figures used to illustrate it are a **2024-specific detail** (no 30-mark scale exists in 2023, and the 15-mark scale demonstrably changed rungs between years), but they are **cited specifically to the 2024 scheme** and framed as an authored scenario, so the file is not overclaiming a standing rule.

**Net:** all three *taught marking rules* are corroborated by the 2023 scheme. No `appliedmaths.ts`
rule is contradicted by the second year. The only year-variable element (R2's exact 30-mark ladder)
is already scoped to the 2024 scheme in the citation and to an authored scenario in the copy.

### Optional reframe (not required)

The specific 30-mark ladder in AM2 is correctly cited to 2024, so no change is mandatory. If the
maintainers prefer the AM2 scenario to be year-agnostic (so it reads as a standing convention rather
than a 2024 instance), swap the 30-mark illustration for the **10-mark scale**, which is identical in
both 2023 and 2024 (`7 / 4 / valid-attempt`), or keep the 30-mark example but retain the explicit
"2024" attribution it already carries. This is a presentational preference, not a correctness fix.
