# Evidence Dossier — Cognitive Load

**Module:** `cognitive-load-protocol` (`components/TheCognitiveLoadModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what peer-reviewed literature supports; every DOI
verified via CrossRef. References surface via inline `Cite` markers + the module-wide
**References** button; data in `data/references/cognitiveLoad.ts`.

**Outcome:** Strong, canonical Cognitive Load Theory content — maps cleanly to Sweller's
framework. One specific figure ("30–50% better") reframed; everything else verified.

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| miller1956 | Miller (1956). The magical number seven, plus or minus two. *Psychological Review*. | [10.1037/h0043158](https://doi.org/10.1037/h0043158) |
| cowan2001 | Cowan (2001). The magical number 4 in short-term memory. *Behavioral and Brain Sciences*. | [10.1017/s0140525x01003922](https://doi.org/10.1017/s0140525x01003922) |
| sweller1988 | Sweller (1988). Cognitive load during problem solving. *Cognitive Science*. | [10.1207/s15516709cog1202_4](https://doi.org/10.1207/s15516709cog1202_4) |
| sweller1998 | Sweller, van Merriënboer & Paas (1998). Cognitive architecture and instructional design. *Educational Psychology Review*. | [10.1023/a:1022193728205](https://doi.org/10.1023/a:1022193728205) |
| chandlersweller1992 | Chandler & Sweller (1992). The split-attention effect. *British J. of Educational Psychology*. | [10.1111/j.2044-8279.1992.tb01017.x](https://doi.org/10.1111/j.2044-8279.1992.tb01017.x) |
| kalyuga2003 | Kalyuga, Ayres, Chandler & Sweller (2003). The expertise reversal effect. *Educational Psychologist*. | [10.1207/s15326985ep3801_4](https://doi.org/10.1207/s15326985ep3801_4) |

---

## Claim-by-claim record

- **§1 The Bottleneck** — Earlier estimates put short-term memory at ~7 items
  (**miller1956**); modern work puts working-memory capacity at ~4 (**cowan2001**).
  Exceeding capacity causes overload that degrades learning (**sweller1988**). Verified.
  Digit-span demo is illustrative (and labels ~4 as the average, consistent with cowan2001).
- **§2 Three Kinds of Brain Drain** — Intrinsic (built-in difficulty), extraneous (wasted
  effort), and germane (actual learning) load — the three-component model
  (**sweller1998**). Verified.
- **§3 Split Attention** — Physically separating a diagram from its explanation forces
  integration that consumes working memory; co-locating them improves learning — the
  split-attention effect (**chandlersweller1992**). Verified; "30–50%" reframed (CL-001).
- **§4 Expertise Reversal** — Supports (worked examples, guidance) that help novices can
  hinder more advanced learners — the expertise-reversal effect (**kalyuga2003**).
  Verified.
- **§5 Managing Your Load** — Cut extraneous load (distractions), chunk intrinsic load,
  spend freed capacity on germane processing; remove non-essentials and keep text+images
  together (**sweller1998**; split-attention/contiguity, **chandlersweller1992**).
  Verified.

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| CL-001 | § 3 | "performed 30 to 50% better" → "learned substantially better" | Split-attention effect is real (chandlersweller1992) but the specific 30–50% range is not a single verifiable figure. |

## Citation-order audit (2026-07-21)
A full-site sweep verified the invariant that inline citation numbers ascend by first
appearance on every render path. The Essentials path violated it: the §1 simplified
branch omitted the ~7-item historical estimate, so its first visible marker was ².
Fixed by adding the miller1956-backed sentence ("Scientists once thought ~7… the real
number is about 4") to the Essentials branch — the same two-claim structure the full
path already carries (miller1956 for ~7, cowan2001 for ~4). No numbering changed; both
paths now read 1,2,3… in order.
