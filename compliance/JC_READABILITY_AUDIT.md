# Junior Cycle vs Leaving Cert — content complexity audit (2026-07)

**Goal (owner):** content shown to 1st–3rd years (Junior Cycle, ages ~12–15) must
be **much simpler** than content shown to 4th years / Leaving Cert.

**Method:** the 39 Learning-Lab modules tagged `curriculum: 'both'` (shown to JC)
were read in full and scored 1–5 for reading level (1 = easy at 12; 3 = fine at
15–16+; 5 = university register), alongside a 6-module senior-only baseline.

## Key finding

Before this change, a module tagged `'both'` rendered the **identical full-register
prose** to a 12-year-old 1st year and an 18-year-old LC student — the module
interface has no year-group input. The senior-only baseline averages **2.3**
(range 2–3); the JC-visible set averaged **~2.7 and spiked to 4**. So JC students
were frequently shown text **harder** than the platform gives its oldest users —
the inverse of the goal. What makes senior modules "senior" is topic (CAO, points,
orals, marking schemes), not prose; the JC modules' problem is (a) reading level
and (b) embedded senior content.

## What shipped in this change

1. **Junior Cycle auto-enables Essentials Mode** (`hooks/useEssentialsMode.ts`).
   Essentials is a pre-existing simpler/shorter prose variant that 38 of the 39
   JC modules already ship; it was previously an opt-in setting unrelated to age.
   JC students (`curriculumLevel === 'junior'`) now always get it; seniors keep
   the opt-in toggle (`components/SettingsModal.tsx` shows it locked-on for JC).
   This lowers JC reading level below the senior register by construction for
   every Essentials-aware module.

2. **Three modules re-tagged `jcStatus: 'coming-soon'` for JC** (`courseData.ts`) —
   inherently senior or too hard even in Essentials:
   - `mental-modelling-protocol` — built entirely on LC **DCG** (Traces of a
     Plane, Interpenetration, FCC/BCC); DCG doesn't exist at JC (JC has Graphics).
   - `effective-struggle-protocol` — university-register throughout (ZPD,
     retrieval/storage strength, metacognitive calibration); Essentials fallback
     still denser than most modules' full text.
   - `strategic-advantage-protocol` — level-4 prose ("radical authorship",
     "resilient identity construction") + senior examples (mock points, "600
     points + UCC Scholarship").

Gates at time of change: typecheck 0 / lint 0 / 1766 tests / build — all clean.

## What Essentials Mode does NOT fix (remaining work — content, staged)

Essentials swaps the **reading prose** only. It does not touch **PersonalStory
testimonials, interactive-widget copy, or chart labels**, where most embedded
senior references live. These are shown to 1st years and should be reframed
(preferably a JC-audience variant of the copy, since these components are shared):

**Senior "PersonalStory" testimonials (highest-value fix — the clearest "not for
you" signal):** 6th/5th-Year + mocks stories in GrowthMindset (also "nearly 600
points and a UCC Scholarship"), TheScienceOfMakingMistakes, ExamCrisisManagement,
GameDay, DigitalDistraction, TheLearningRadar, TheNoteTakingParadox, TheCognitiveLoad,
TheContextEffect, AgencyArchitecture, ReverseEngineering.

**Senior number/CAO references in interactive copy:** SelfEfficacy RoleModelSelector
("625 points"; "failed their mocks … dream course").

**LC-only interactive content shown to JC (swap to a JC exercise):**
- MasteringInterleaving — the flagship ProblemTypeSpotter is LC HL calculus
  (differentiate y = sin(x²), chain/product rule).
- ElaborativeInterrogation — §5 Irish **Oral**, §4 Geography **SRPs**, calculus.
- ExamHallStrategies — the two flagship drills are an LC English HL paper
  (Comparative Study, cultural context/general vision, Unseen Poetry) + GDP =
  C+I+G+(X−M), Peig Sayers.
- CognitiveEndurance — AllostaticLoad chart labels "5th Year / 6th Year".
- TheAutodidactsEngine — writing loop uses PCLM (LC English marking) + Yeats
  "The Second Coming".
- Scattered calculus / HL-Maths examples: IllusionOfCompetence ("chain rule"),
  TheLearningRadar, TheCognitiveLoad, ReverseEngineering, ThePowerOfYet
  ("Honours Maths").

**Age-appropriateness (distinct from reading level):** ControllableVariables uses a
blood-alcohol-0.05% / "studying drunk" / drink-drive-limit analogy — built for an
audience that understands driving limits, not 12-year-olds.

**Unglossed jargon to translate for under-15s:** "SUDS"/"NAT" (CatastrophicThinking),
"Low-GI/High-GI" on GameDay food chips, "verbatim/generative" chart labels
(NoteTakingParadox), "metacognitic blind spots" (LearningRadar), "pomodoro"
(ImplementationProtocol), "EFT" button (HopeProtocol).

## Per-module verdict table (39 JC-visible modules)

Reading level 1–5; verdict OK-FOR-JC / BORDERLINE / TOO-HARD / MISTAGGED.
"Senior refs" = count of senior-only references (mocks, CAO/points, 5th/6th year,
LC-only subjects/formats) shown to JC.

| Module | Level | Senior refs | Verdict |
|---|---|---|---|
| StrategicAdvantage | 4 | 5 | TOO-HARD → re-tagged coming-soon |
| EffectiveStruggleAndGrowth | 4 | 2 | TOO-HARD → re-tagged coming-soon |
| MentalModelling | 3 | ~6 (DCG) | MISTAGGED → re-tagged coming-soon |
| ExamHallStrategies | 2 (drills LC) | ~10 | MISTAGGED (drills) — needs JC question bank |
| TheAutodidactsEngine | 3 | 1 (PCLM/Yeats) | BORDERLINE→MISTAGGED (writing loop) |
| ElaborativeInterrogation | 2 | 4 | BORDERLINE (LC oral/SRP/calculus sections) |
| SelfEfficacy | 3 | 2 (625 pts) | BORDERLINE |
| IllusionOfCompetence | 3 | 3 | BORDERLINE |
| HopeProtocol | 3 | 1 (+1) | BORDERLINE |
| AgencyArchitecture | 3 | 1 | BORDERLINE |
| CatastrophicThinking | 3 | 1 | BORDERLINE (SUDS/NAT jargon) |
| Procrastination | 3 | 1 soft | BORDERLINE (no Essentials variant) |
| TheGrammarOfGrit | 3 | 0 | BORDERLINE |
| EmotionalIntelligence | 3 | 0 | BORDERLINE (term density) |
| ThePraiseProtocol | 3 | 1 | BORDERLINE |
| TheLearningRadar | 3 | 3 | BORDERLINE |
| TheImplementationProtocol | 3 | 0 | BORDERLINE |
| TheNoteTakingParadox | 3 | 2 | BORDERLINE |
| ControllableVariables | 3 | BAC analogy | BORDERLINE (age-inappropriate analogy) |
| TheMyelinManual | 2.5 | 1 | BORDERLINE |
| ReverseEngineering | 2 | 5 | BORDERLINE |
| MasteringInterleaving | 2 | 2 (calculus drill) | BORDERLINE |
| TheCognitiveLoad | 2.5 | 3 | OK-FOR-JC (with fixes) |
| TheContextEffect | 2.5 | 2 | OK-FOR-JC (with fixes) |
| ExamCrisisManagement | 2 | 2 | OK-FOR-JC (fix story) |
| GameDay | 2 | 2 | OK-FOR-JC (fix story + GI) |
| GrowthMindset | 2.5 | 5 | OK-FOR-JC (fix founder story) |
| ThePowerOfYet | 2.5 | 2 | OK-FOR-JC (reframe examples) |
| TheScienceOfMakingMistakes | 3 | 2 (Junior Cert) | BORDERLINE |
| CognitiveEndurance | 2 | 2 (5th/6th yr labels) | BORDERLINE |
| MasteringSpacedRepetition | 2 | 0 | OK-FOR-JC (simplify §4 ratios) |
| MasteringActiveRecall | 2 | 0 | OK-FOR-JC |
| TheCognitiveArchitecture | 2 | 1 trivial | OK-FOR-JC |
| AffirmingValues | 2 | 1 | OK-FOR-JC |
| BestPossibleSelf | 2 | 0 | OK-FOR-JC |
| Neuroplasticity | 2 | 0 | OK-FOR-JC |
| DigitalDistraction | 1–2 | 1 | OK-FOR-JC |
| TheTeachingEffect | 2 | 0 | OK-FOR-JC |
| BimodalBrain | 1 | 0 | OK-FOR-JC (the model to aspire to) |

## Senior-only baseline (for calibration)

| Module | Level |
|---|---|
| points-optimization-protocol | 3 |
| agency-protocol | 2.5 |
| answer-engineering-protocol | 2.5 |
| leaving-cert-strategy-protocol | 2 |
| marking-scheme-decoder-protocol | 2 |
| reframing-progress-protocol | 2 |

Mean ≈ 2.3. House style is deliberately conversational with tooltipped jargon —
so JC content only needs to sit at/below this to satisfy the goal, which
auto-Essentials now delivers for the reading-level dimension.
