# Evidence Dossier — How Your Memory Works

**Module:** `cognitive-architecture-protocol` (`components/TheCognitiveArchitectureModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what peer-reviewed literature supports; every DOI
verified via CrossRef. References surface via inline `Cite` markers + the module-wide
**References** button; data in `data/references/howMemoryWorks.ts`.

**Outcome:** Foundational memory module; claims map to canonical findings. The two
specific numbers ("~4 chunks", "15–30 seconds") are well-evidenced and retained with
citations. One comparative claim was reframed (HMW-001).

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| atkinson1968 | Atkinson & Shiffrin (1968). Human memory: A proposed system and its control processes. *Psych. of Learning and Motivation*. | [10.1016/S0079-7421(08)60422-3](https://doi.org/10.1016/S0079-7421(08)60422-3) |
| miller1956 | Miller (1956). The magical number seven, plus or minus two. *Psychological Review*. | [10.1037/h0043158](https://doi.org/10.1037/h0043158) |
| cowan2001 | Cowan (2001). The magical number 4 in short-term memory. *Behavioral and Brain Sciences*. | [10.1017/s0140525x01003922](https://doi.org/10.1017/s0140525x01003922) |
| peterson1959 | Peterson & Peterson (1959). Short-term retention of individual verbal items. *JEP*. | [10.1037/h0049234](https://doi.org/10.1037/h0049234) |
| squire2004 | Squire (2004). Memory systems of the brain. *Neurobiology of Learning and Memory*. | [10.1016/j.nlm.2004.06.005](https://doi.org/10.1016/j.nlm.2004.06.005) |
| craik1972 | Craik & Lockhart (1972). Levels of processing. *J. Verbal Learning and Verbal Behavior*. | [10.1016/s0022-5371(72)80001-x](https://doi.org/10.1016/s0022-5371(72)80001-x) |
| diekelmann2010 | Diekelmann & Born (2010). The memory function of sleep. *Nature Reviews Neuroscience*. | [10.1038/nrn2762](https://doi.org/10.1038/nrn2762) |
| dunlosky2013 | Dunlosky et al. (2013). Improving students' learning with effective learning techniques. *PSPI*. | [10.1177/1529100612453266](https://doi.org/10.1177/1529100612453266) |
| lupien2009 | Lupien, McEwen, Gunnar & Heim (2009). Effects of stress throughout the lifespan on the brain, behaviour and cognition. *Nature Reviews Neuroscience*. | [10.1038/nrn2639](https://doi.org/10.1038/nrn2639) |

---

## Claim-by-claim record

- **§1 Three stores** — Sensory → short-term → long-term (the modal/multi-store model).
  **atkinson1968.** Verified.
- **§2 The bottleneck** — Short-term capacity is ~4 chunks for complex material
  (**cowan2001**; chunking concept **miller1956**); unrehearsed items decay within
  ~15–30 s (**peterson1959**). Verified; specific numbers retained as well-evidenced.
- **§3 Long-term organisation** — Distinct systems: fact (semantic), experience
  (episodic), skill (procedural). **squire2004.** Verified.
- **§4 Encoding** — Depth of processing: elaborative, meaning-based encoding produces
  more durable memory than shallow re-reading. **craik1972.** Verified. (The synaptic-
  strengthening aside is covered in depth in the Neuroplasticity module.)
- **§5 Sleep** — Memory consolidation occurs during sleep via hippocampal replay and
  transfer to neocortex. **diekelmann2010.** Verified.
- **§6 Action plan** — Practice testing and distributed (spaced) practice are rated
  **high**-utility by **dunlosky2013**; interleaving is rated **moderate**-utility in the
  same review (corrected after the verification pass — the earlier wording lumped
  interleaving into the high-utility tier the source does not place it in). Chronic stress /
  elevated cortisol impairs memory (**lupien2009**). Verified. Micro-commitment comparison
  reframed (HMW-001).

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| HMW-001 | § 6 | "bigger impact on your memory than an extra hour of cramming" → "protects the deep sleep your memory relies on…" | Direct quantitative comparison not established by any study; sleep's consolidation role is supported (diekelmann2010), the comparison is not. |
