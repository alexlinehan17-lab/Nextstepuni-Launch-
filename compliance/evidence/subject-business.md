# Evidence Dossier — Mastering Business (subject module)

**Module:** `subject-business-protocol` (data-driven via `components/SubjectModule.tsx`;
content in `subjectContentBusiness.ts` under key `business`)
**Group:** B (subject-specific) — grounded in official SEC sources, **not**
peer-reviewed psychology journals.
**Review date:** 2026-06-26
**Reviewer:** Pre-accreditation review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what a real, locatable source supports. For this
module the sources are the in-repo SEC Business HL 2025 marking scheme and the in-repo
2015 Business Chief Examiner's Report. Sources surface via inline `{{cite:N}}` markers
(rendered as `<Cite/>`) + the module-wide **References** button; data in
`data/references/subjectBusiness.ts`.

**Infra note.** This is the first accredited *data-driven* subject module. Citation
support was added to the shared subject-module pipeline: `SubjectModuleContent` gained an
optional `references` field, and `SubjectModule.renderParagraph` now parses a
`{{cite:N}}` marker into an inline `<Cite n={N}/>` (alongside the existing `**bold**` and
`[[highlight]]` markers). The same mechanism is reusable for the remaining subject
modules.

**Corrections — this module had factual errors fixed against the 2025 marking scheme.**
See the table below; all are also logged in `data/cutContent.ts`.

---

## Verified sources

| # | Source | Kind | Locator |
|---|--------|------|---------|
| 1 | SEC Business Higher Level 2025 marking scheme — paper structure, section weightings, ABQ Name/Explain/Link requirement, per-part mark allocations | official | in-repo `examiner-reports/business/2025-marking-scheme.pdf` (verified directly) |
| 2 | SEC Business 2015 Chief Examiner's Report — developed vs one-word answers, action words, answering the question asked | official | in-repo `examiner-reports/business/2015-chief-examiner.pdf` (verified directly) |

---

## Claim-by-claim record

- **§1 How Business Actually Works** — Single 3-hour, 400-mark paper, three sections
  (**markingScheme2025**). Section 1 = 80 marks, **answer 8 questions at 10 marks each**
  (corrected — see BUS-001). Section 2 ABQ = 80 marks, sub-parts A/B/C, drawn from
  **Units 2-4** (corrected — see BUS-002); direct text linking required, no link mark
  without relevant theory (verified in the scheme). Section 3 = 240 marks, 4 questions ×
  60 marks, at least one from Part 1 and one from Part 2 (part-constraint added —
  BUS-003).
- **§2 What the Examiner Rewards** — SEE / SEEE answer structure mirrors the scheme's
  "Name, Explain, Example" mark allocation (**markingScheme2025**). ABQ
  State/Explain/**Link** — the scheme requires a direct quote/phrase per part and awards
  no link without theory (**markingScheme2025**). Action words and depth-over-breadth
  grounded in the Chief Examiner's developed-answer guidance (**chiefExaminer2015**).
  Invented per-part mark figures ("10-15 / 20-25 marks") and the "three vs six points"
  specifics were removed (BUS-004).
- **§3 Where Your Marks Are** — Section 3 240 marks/60%; ABQ 80 marks/20% on Units 2-4;
  Section 1 **8 × 10 marks** (corrected) (**markingScheme2025**). High-frequency topic
  list (motivation theories, 4 Ps, etc.) is a hedged past-paper observation and carries
  no citation.
- **§4 What Costs You Marks** — ABQ link requirement (**markingScheme2025**); action
  words and developed-answer depth (**chiefExaminer2015**). Timing advice is practical.
- **§5 How to Study Business** — Using the marking schemes to learn mark allocation
  (**markingScheme2025**); the Units-2-4 priority bullet corrected (BUS-002). Concept
  bank / timed ABQ practice are practical study advice.
- **§6 Your Business Action Plan** — Practical plan; the concept-bank unit reference
  corrected to Units 2-4 (BUS-002), marking-scheme study cited (**markingScheme2025**).

---

## Corrections & reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Corrected | Reason |
|----|---------|----------------------|--------|
| BUS-001 | §1, §3 | "10 out of 15 questions, each worth 8 marks" / "Ten questions at 8 marks each" → "8 short questions, each worth 10 marks" / "Eight questions at 10 marks each" | The 2025 marking scheme states Section 1 is "Answer 8 questions. Each question carries 10 marks." The original count and per-question marks were both wrong. |
| BUS-002 | §1, §3, §5, §6 | ABQ "Units 3, 4, and 5 (Management, HR, Enterprise, Marketing)" → "Units 2, 3, and 4 (Enterprise, Management, Human Resources)" | The 2025 scheme labels the ABQ "Units 2, 3 & 4"; the 2025 ABQ covered enterprise, management control and HRM (no marketing). Unit numbers and topic set corrected to the scheme. |
| BUS-003 | §1 | "You choose 4 from 7 questions" → "You answer 4 questions … at least one from Part 1 and one from Part 2" | Added the Section 3 part-selection constraint stated in the scheme; "4 questions × 60 marks" was already correct. |
| BUS-004 | §2 | "Part (a) … 10-15 marks, part (b) … 20-25 marks" and "three well-developed points score higher than six shallow ones" → generic, number-free phrasing | The specific per-part mark figures and the 3-vs-6 ratio were invented; reframed to the verifiable developed-answer principle from the Chief Examiner report. |

## Outstanding for accreditation
The high-frequency topic list (§3) is a reasonable past-paper observation but is not
backed by a counted analysis; if a topic-frequency table is wanted as evidence, build it
from the last 10 years of papers and cite it. ABQ unit coverage can shift year to year —
the module now states the 2025 set explicitly rather than implying a fixed set.
