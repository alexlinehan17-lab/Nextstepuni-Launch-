# Module accreditation — evidence dossiers & queue

Per-module evidence dossiers for the pre-accreditation review (DCU / Brian MacCraith).
Each `<module-slug>.md` records the verified peer-reviewed sources behind a module,
a claim-by-claim verification record, and any content reframed or cut.

**Governing rule:** only state/advise what peer-reviewed literature supports; never
attach a citation that can't be verified against a real, locatable paper; reframe or
cut anything unverifiable (logged in `data/cutContent.ts`). See `CLAUDE.md` →
"Module accreditation & evidence dossier".

**Independent verification pass (2026-06-26):** all 48 accredited modules were put through
a second, adversarial check — one reviewer per module re-confirmed each citation supports
its *specific* claim, with every issue independently re-tested. 297 cited claims checked,
26 modules fully clean, 13 genuine issues upheld and **all 13 resolved**. Full report:
`VERIFICATION-2026-06-26.md`. The in-app Accreditation Dossier page summarises it.

## Queue — Group A (psychology / learning-science, 37)

### 🎯 Learning Cheat Codes (15)
- [x] Mastering Active Recall — `active-recall.md`
- [x] Mastering Spaced Repetition — `spaced-repetition.md`
- [x] Mix It Up (Interleaving) — `interleaving.md`
- [x] Overcoming Illusions of Competence — `illusion-of-competence.md`
- [x] Using Feedback Loops — `feedback-loops.md`
- [x] How Your Memory Works — `how-memory-works.md`
- [x] Elaborative Interrogation — `elaborative-interrogation.md`
- [x] Cognitive Endurance — `cognitive-endurance.md`
- [x] Mental Modelling — `mental-modelling.md`
- [x] Focused vs Diffuse Mode — `bimodal-brain.md`
- [x] Creating Barriers for Digital Distractions — `digital-distraction.md`
- [x] The Learning Radar — `learning-radar.md`
- [x] The Note-Taking Paradox — `note-taking-paradox.md`
- [x] Cognitive Load — `cognitive-load.md`
- [x] The Context Effect — `context-effect.md`

### 🌱 Science of Growth (10)
- [x] Neuroplasticity — `neuroplasticity.md`
- [x] The Myelin Manual — `myelin-manual.md`
- [x] The Power of Praise — `praise-protocol.md`
- [x] Effective Struggle and Growth — `effective-struggle.md`
- [x] The Science of Making Mistakes — `science-of-mistakes.md`
- [x] The Power of "Yet" — `power-of-yet.md`
- [x] Using Controllable Variables to Grow — `controllable-variables.md`
- [x] Linking Study to Future Goals — `linking-study-future-goals.md`
- [x] The Growth Playbook — `growth-mindset.md`
- [x] The Teaching Effect — `teaching-effect.md`

### 🧠 Architecture / Mindset (13)
- [x] The Driver — `agency-protocol.md`
- [x] The Science of Hope — `hope-protocol.md`
- [x] Affirming Values — `affirming-values.md`
- [x] Best Possible Self — `best-possible-self.md`
- [x] The Grammar of Grit — `grammar-of-grit.md`
- [x] Controlling the Controllables — `agency-architecture.md`
- [x] Your Strategic Advantage — `strategic-advantage.md`
- [x] Self Efficacy — `self-efficacy.md`
- [x] Understanding Procrastination and Motivation — `procrastination.md`
- [x] Reframing Catastrophic Thoughts — `catastrophic-thinking.md`
- [x] Building Emotional Intelligence — `emotional-intelligence.md`
- [x] Reframing Progress — `reframing-progress.md`
- [x] The Implementation Playbook — `implementation-protocol.md`

## Group B — Subject & Exam (45)
Grounded in official Irish State exam / admissions documents (CAO points grid, SEC
marking schemes & Chief Examiner reports — `/examiner-reports/`), **not** psychology
journals. The references system supports these via `kind: 'official'` sources
(`data/references/types.ts`). Note: examinations.ie blocks automated fetches (403), so
subjects without an in-repo examiner report are flagged in their dossiers for a
follow-up sourcing pass.

### 🎯 Exam Zone (8)
- [x] The Points Playbook (Leaving Cert Strategy) — `leaving-cert-strategy.md`
- [x] Reverse Engineering the Exam — `reverse-engineering.md`
- [x] Exam Hall Strategies — `exam-hall-strategies.md`
- [x] Exam Crisis Management — `exam-crisis-management.md`
- [x] Game Day — `game-day.md`
- [x] Points Optimization — `points-optimization.md` (H1-rate figures labelled approximate; SEC stats re-verification pending site access)
- [x] Marking Scheme Decoder — `marking-scheme-decoder.md`
- [x] Answer Engineering — `answer-engineering.md`

### 📚 Subject-Specific (37) — per-subject SEC reports needed
Citation support is wired into the data-driven subject modules (`{{cite:N}}` marker in
`SubjectModule.tsx` + optional `references` on `SubjectModuleContent`). Accredited where
in-repo SEC reports exist; the rest are deferred pending subject Chief Examiner reports /
marking schemes in `/examiner-reports/`.

- [x] Business — `subject-business.md` (corrected 4 factual errors vs 2025 marking scheme)
- [x] Mathematics — `subject-mathematics.md` (corrected the 300-marks/two-section paper structure vs 2015 Chief Examiner report)
- [ ] Remaining 35 — awaiting per-subject SEC reports
