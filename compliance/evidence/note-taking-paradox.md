# Evidence Dossier — The Note-Taking Paradox

**Module:** `note-taking-paradox-protocol` (`components/TheNoteTakingParadoxModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what peer-reviewed literature supports; every DOI
verified via CrossRef. References surface via inline `Cite` markers + the module-wide
**References** button; data in `data/references/noteTakingParadox.ts`.

**Outcome:** Two reframes — the "pen is mightier" study (overstated given failed
replications) and an unverifiable "30–40%" figure. The robust core (generative/encoding
note-taking beats verbatim copying; self-testing; concept maps for relational content)
is retained with citations.

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| mueller2014 | Mueller & Oppenheimer (2014). The pen is mightier than the keyboard. *Psychological Science*. | [10.1177/0956797614524581](https://doi.org/10.1177/0956797614524581) |
| kiewra1989 | Kiewra (1989). A review of note-taking: The encoding-storage paradigm and beyond. *Educational Psychology Review*. | [10.1007/bf01326640](https://doi.org/10.1007/bf01326640) |
| craik1972 | Craik & Lockhart (1972). Levels of processing. *J. Verbal Learning and Verbal Behavior*. | [10.1016/s0022-5371(72)80001-x](https://doi.org/10.1016/s0022-5371(72)80001-x) |
| rk2006 | Roediger & Karpicke (2006). Test-enhanced learning. *Psychological Science*. | [10.1111/j.1467-9280.2006.01693.x](https://doi.org/10.1111/j.1467-9280.2006.01693.x) |
| nesbit2006 | Nesbit & Adesope (2006). Learning with concept and knowledge maps: A meta-analysis. *Review of Educational Research*. | [10.3102/00346543076003413](https://doi.org/10.3102/00346543076003413) |

---

## Claim-by-claim record

- **§1 The Transcription Trap** — Verbatim transcription produces shallower learning than
  selective, in-your-own-words note-taking. **mueller2014** (with the replication caveat
  now stated in-text). Verified after reframe (NTP-001). The dual-chart is illustrative.
- **§2 Notes That Actually Work** — Generative note-taking (paraphrase, summarise,
  connect) aids learning via deeper encoding (**kiewra1989**, encoding hypothesis;
  **craik1972**, depth of processing). Verified; "30–40%" reframed (NTP-002).
- **§3 The Cornell System** — A structured layout that builds paraphrasing + cue-based
  **self-testing** into notes; the cue-cover-and-recall step is retrieval practice
  (**rk2006**). Cornell itself is a practical method. Verified.
- **§4 Mapping vs Listing** — Concept maps tend to outperform plain lists for relational
  understanding (**nesbit2006**, meta-analysis; modest effect — wording softened from
  "consistently beat" to "tend to outperform" to match the effect size). Linear notes
  suit sequential content. Verified.
- **§5 Building Your System** — Organised notes + active review/self-testing
  (**rk2006**). 24-hour cue/summary pass adds generation + spacing. Verified.

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| NTP-001 | § 1 | "handwriters crushed it" → "came out ahead" + replication caveat | Mueller & Oppenheimer (2014) is real but failed to replicate (handwriting-vs-laptop conceptual advantage); robust mechanism is verbatim-vs-generative. |
| NTP-002 | § 2 | "outperform … by 30-40%" → "tend to outperform" | Specific figure unverifiable; generative-encoding benefit supported qualitatively (kiewra1989, craik1972). |

*Minor accuracy refinement (not a separate cut entry): §4 "concept maps consistently beat
lists" → "tend to outperform", to match the modest meta-analytic effect in nesbit2006.*
