# AI Governance Schedule

NextStepUni Learning Lab — AI feature inventory and EU AI Act risk position

Document status: DRAFT for legal review
Prepared by: NextStepUni Ltd
Date: 2026-04-29
Source code reviewed: commit `0ac6be4` on branch `main`

---

## 1. Scope and headline finding

This Schedule documents every feature of the application that is, could reasonably be characterised as, or has been *described as* an AI feature. It is written for PwC's Risk/Legal team and assumes familiarity with the EU AI Act risk-tier framework (prohibited / high-risk / limited-risk / minimal-risk) and Annex III (high-risk use cases, including education).

**Headline finding.** The current production build of the application contains **no large-language-model integration and no machine-learning inference of any kind**. This finding has been independently re-verified including a search of git history; the audit trail is recorded in `compliance/GEMINI_AUDIT.md` (2026-04-29).

In summary:

- No Gemini SDK (`@google/genai`, `GoogleGenerativeAI`, `generateContent`) has ever been present in this repository's git history. Verified by `git log -S` across all branches.
- No LLM SDK is declared in `package.json` or present in `package-lock.json`.
- A `define:` block in `vite.config.ts` did historically expose `GEMINI_API_KEY` to the client bundle (added in the initial commit `fc3db43`, 2026-02-07, as part of the original Google AI Studio scaffold). It was removed in commit `063d574` on 2026-04-06 with the explicit changelog entry "Gemini API key leak removed from vite.config". This was a security remediation, not a feature removal — there was no Gemini-using code to remove.
- The previous mentions of `GEMINI_API_KEY` in `README.md:18` and `CLAUDE.md:22` were corrected on 2026-04-29 (the same date as the present update); both files now point to `compliance/GEMINI_AUDIT.md` for the authoritative position.

**Position for PwC**: there is no live AI integration today. Forward-looking governance for any future integration is captured in Section 6.

The features in this Schedule are therefore either (a) *deterministic* algorithms that may be perceived as AI by a lay observer, or (b) *forward-looking* placeholders for capability that the Processor may build in Year 2.

---

## 2. Feature: Future Finder (CAO course recommendation)

**Source**: `components/futureFinderAlgorithm.ts` (lines 1–532), `components/FutureFinder.tsx`.

### 2.1 Student-facing purpose

A self-directed assessment that ranks Irish higher-education courses (CAO-listed undergraduate degrees, PLC programmes, apprenticeships) against the student's stated interests, values, predicted Leaving Cert points and willingness to relocate. Output is a ranked list with explanations, intended to support a conversation with a Guidance Counsellor.

### 2.2 Model used and vendor

None. The feature is a deterministic weighted-scoring algorithm authored in-house. No external API is called for inference. No model weights are loaded. There is no vendor.

### 2.3 Inputs

The student-supplied `FutureFinderAnswers` interface (futureFinderAlgorithm.ts:11–36):

```
interface FutureFinderAnswers {
  interestTags: string[]            // up to 5 from a fixed list of 15 interests
  scenarioChoices: string[]         // 2–3 job-scenario picks from a fixed set
  salaryImportance: number          // 1–5 slider
  jobSecurityImportance: number     // 1–5 slider
  helpingOthersImportance: number   // 1–5 slider
  workStyleTags: string[]           // 2–3 from a fixed list
  teamPreference: 'team' | 'solo' | 'mix'
  studyDuration: string[]           // '1' | '2' | '3' | '4+'
  willingToRelocate: boolean
  preferredRegions: string[]        // up to 3 Irish regions
  estimatedPoints: number           // computed from the student's mock results
}
```

No free-text input reaches the algorithm. No directly identifying data (name, school, age) is fed to the algorithm; the scoring function is purely on these attributes.

### 2.4 Outputs and how they are used

The algorithm returns a ranked array of `CourseRecommendation` objects, each with:

- the course identifier,
- the composite score (0–100),
- a breakdown across the three weighted dimensions (interest 45%, values 30%, feasibility 25%),
- a list of human-readable "reasons" derived from which input tags matched which course tags.

The output is rendered directly to the student in the FutureFinder component. There is no human-in-the-loop review.

### 2.5 Data sent off-platform

None. The algorithm executes client-side. The student's saved answers and the computed result are persisted to Firestore `progress/{uid}` (specifically a Future Finder result blob), but no third party receives them.

### 2.6 Guardrails

- Inputs are constrained to fixed enumerations (no free text), eliminating prompt-injection-style attacks.
- The points-feasibility component uses a sigmoid that *discourages but does not eliminate* courses the student is unlikely to reach (futureFinderAlgorithm.ts:68–80), so the recommendation does not silently filter out aspirational options.
- The scoring function is deterministic and reviewable; it produces the same output for the same input.
- All recommended courses are drawn from `components/futureFinderData.ts`, a hand-curated set of CAO listings; the algorithm cannot fabricate a course.

### 2.7 Failure modes considered

- **Failure mode**: the student has no mock results, so `estimatedPoints` is 0. **Handling**: feasibility dimension treats this as "no data" and falls back to course-level priors rather than scoring 0. **TBC — Alex to confirm** the exact fallback in code; the Processor's intent is that no course is ever scored 0 purely because no points data exists.
- **Failure mode**: the student selects no interests. **Handling**: interest dimension contributes 0; the recommendation surfaces values-aligned courses.
- **Failure mode**: the student has unrealistic expectations (low effort, high salary, few subjects). **Handling**: the algorithm returns the closest available match plus a "reasons" string; it does not silently rank-order around the unattainable.

### 2.8 Logging and auditability

The full input vector and the full ranked output are persisted to `progress/{uid}` so a Guidance Counsellor can review them with the student. There is no separate audit log of *when* the algorithm was run.

### 2.9 EU AI Act classification

The Processor's position: this feature is **not** "AI" within the meaning of Article 3(1) of the EU AI Act. It is a deterministic rule-based system that does not infer from training data, does not adapt with use, and does not produce predictions, recommendations or decisions in the senses contemplated by the Act (Recital 12 of the AI Act explicitly excludes "systems based on rules defined solely by natural persons to automatically execute operations" from the AI definition).

If, contrary to that position, a regulator were to take the view that the feature falls within scope of the Act because it produces "recommendations" influencing access to education (Annex III, paragraph 3), the feature would arguably fall under Annex III(3)(a) — "AI systems intended to be used to determine access… of natural persons to educational and vocational training institutions" — and would therefore be **high-risk**. The Processor's mitigation against that interpretation is:

- the output is presented as one input to a conversation with a human Guidance Counsellor, not as a gating decision,
- the algorithm is fully transparent and explainable to the student (the "reasons" list),
- there is no opacity that prevents regulator inspection,
- inputs are student-volunteered.

**Reviewer note**: legal counsel should confirm the Processor's position that Recital 12 takes a deterministic algorithm out of AI Act scope. The structurally cautious approach is to apply Annex III obligations regardless.

### 2.10 Fallback if unavailable

Not applicable — the algorithm runs in the student's browser. The only failure mode is a JavaScript error, which the surrounding component catches and surfaces as a user-facing error message.

---

## 3. Feature: Spaced-repetition timetable (SM-2)

**Source**: `components/timetableAlgorithm.ts` (lines 1–729), `components/SpacedRepetitionTimetable.tsx`.

### 3.1 Student-facing purpose

Generates a personalised weekly study timetable across the student's Leaving Cert subjects, prioritising subjects and topics where confidence is low and exam impact is high. Adapts after each post-session debrief.

### 3.2 Model used and vendor

None. This is the SuperMemo SM-2 algorithm (Wozniak, 1987 — published, deterministic), augmented with a syllabus-efficiency weighting and a topic-mastery boost, all coded in-house. No machine learning. No vendor.

### 3.3 Inputs

- The student's `subjectProfile` (subjects, levels, target grades, exam start date, rest days, default block duration).
- Cumulative `studySessions` history (date, subject, session type, duration).
- `studyDebriefs` history (confidence before/after, perceived grade, free-text reflection — though only the confidence ratings feed the algorithm).
- `topicMastery.{subject}.{topic}` map (confidence per topic; SM-2 quality scores).

All of this is data the student has either entered or generated through legitimate use of the app.

### 3.4 Outputs and how they are used

A weekly timetable: an array of `{ dayOfWeek, blockIndex, subjectName, sessionType, suggestedTopics }` blocks. The block can be opened, started, completed or skipped by the student. The output is shown directly; no human-in-the-loop review.

### 3.5 Data sent off-platform

None. The algorithm runs client-side; the resulting timetable is persisted to `progress/{uid}` for cross-device continuity.

### 3.6 Guardrails

- Per-day block cap (3–4 weekdays, 4–6 weekends; timetableAlgorithm.ts ~line 263 onward).
- Per-week hour cap (10–22 hours depending on weeks-until-exam) so the algorithm cannot generate a punitive schedule.
- Log-scale compression on subject priorities to prevent any one subject monopolising the timetable.
- Ease factor floor of 1.3 (timetableAlgorithm.ts:21–99) so a "difficult" subject does not collapse into daily review.

### 3.7 Failure modes considered

- **Failure mode**: student debrief confidence drops on every session. **Handling**: SM-2 resets the interval to 1 day; the timetable rebalances toward that subject without piling on it (log compression).
- **Failure mode**: examStartDate is in the past. **Handling**: TBC — Alex to confirm the algorithm's behaviour when the exam window has elapsed; the Processor's intent is that the timetable becomes a maintenance/revision schedule rather than crashing.
- **Failure mode**: the student has zero subjects. **Handling**: the timetable is empty; the surrounding UI prompts the student to complete subject onboarding.

### 3.8 Logging and auditability

Each generated timetable is persisted; the inputs that produced it are recoverable from the same `progress/{uid}` document. There is no separate audit log of generation events.

### 3.9 EU AI Act classification

Same position as Section 2.9: deterministic, rule-based, transparent, not AI within the Act's definition. If a regulator disagreed, the feature does not gate access to education or assess natural persons; it sequences a personal study plan. The strongest argument for Annex III applicability is paragraph 3(b) — "AI systems intended… to evaluate learning outcomes" — but the feature does not evaluate learning outcomes, it sequences study time. The Processor's position: **out of scope**.

### 3.10 Fallback if unavailable

Client-side only. The algorithm's failure surfaces as a UI error; the underlying study modules and content remain accessible.

---

## 4. Feature: Subject-priority and recommendation hooks (`useRecommendation`, `smartRecommendation`)

**Source**: `hooks/useRecommendation.ts`.

### 4.1 Student-facing purpose

Presents a "what to do next" suggestion on the home dashboard — typically the next study block on the timetable, or a module the student has not opened recently.

### 4.2 Model and vendor

None. The hook is a series of conditional rules over Firestore-held progress state.

### 4.3–4.10

Inputs: same `progress/{uid}` data already discussed; outputs: a single `SmartRecommendation` object surfaced in the home view; no off-platform data movement; deterministic; not in EU AI Act scope; client-side only.

---

## 5. Feature: Reflection quality scoring

**Source**: `components/ReflectionModal.tsx` (lines 38–61, prompts at 73–81).

### 5.1 Student-facing purpose

After a study block, the student writes a short reflection. The application scores the reflection ("brief", "thoughtful", "deep") and awards points accordingly.

### 5.2 Model and vendor

None. The scoring is heuristic: word count, presence of growth-mindset language tokens, presence of concrete-detail markers. No ML, no LLM, no vendor.

### 5.3 Inputs

The reflection text the student types (free text, may contain Article 9-adjacent content — see DPIA Section 1.4).

### 5.4 Outputs and how they are used

A tier label and a points award. The reflection text itself is stored to `progress/{uid}.studyDebriefs` for the student's own review and for GC visibility.

### 5.5 Data sent off-platform

None. The reflection is processed and stored within Firestore only.

### 5.6 Guardrails

- The scorer cannot reject a reflection or hide it; every reflection earns at least the lowest tier.
- The scorer cannot label reflections by mental-health content — there is no sentiment analysis, no health classifier.

### 5.7 Failure modes

The scorer can give a generous tier to a long but low-quality reflection. The Processor accepts this as a deliberate choice in favour of student goodwill.

### 5.8 Logging and auditability

Reflections are stored verbatim. Tier and points are recoverable from the saved record.

### 5.9 EU AI Act classification

Out of scope. The scorer is a rule-based heuristic.

### 5.10 Fallback

Client-side only. The reflection stores even if scoring fails.

---

## 6. Forward-looking: Gemini integration (currently absent)

The Processor anticipates that Year 2 may introduce LLM-backed features such as personalised feedback on student answers, content generation for new modules, or moderated chatbot tutoring. **None of this exists today.** Before any such feature is enabled, the following are mandatory:

- **EU AI Act re-assessment**: an LLM-backed feedback feature aimed at minors and informing study decisions is materially closer to Annex III(3)(b) ("AI systems intended… to evaluate learning outcomes") and likely to be **high-risk**.
- **Lawful basis re-confirmation**: parental consent must be re-confirmed because the processing has changed materially.
- **Sub-processor disclosure**: Google as a Gemini provider must be disclosed to schools as a sub-processor.
- **Prompt registry**: every prompt sent to the model must be reviewable and version-controlled in the repository (no in-flight prompt construction outside source control).
- **Output handling**: model output must not be presented to a student without (a) a system-prompted refusal policy for self-harm / harmful advice / personal data extraction, (b) a safety-classifier check before render, (c) a logging path so a Guidance Counsellor can audit what the model said.
- **Rate limits and cost controls**: per-user and per-school caps to prevent both abuse and runaway cost.
- **Region**: Gemini calls must be routed to an EEA endpoint where possible, and the resulting transfer position documented in DPA Schedule 6.
- **Human review for new content**: any model-generated module *content* (as distinct from per-student feedback) must pass human curriculum review before being added to `courseData.ts` / `moduleRegistry.ts`.

**Reviewer note**: this section is forward-looking only. Until Gemini is wired into the build, there is no obligation arising from it.

---

## 7. AI Feature Inventory — single-page summary

| Feature | Source file | "AI" in lay sense? | Model / vendor | Inference location | Off-platform data? | EU AI Act position | Status |
|---|---|---|---|---|---|---|---|
| Future Finder course recommendation | components/futureFinderAlgorithm.ts | Often perceived as AI | None — deterministic weighted scoring | Client-side | None | Recital 12: not AI. Cautious view: Annex III(3)(a) high-risk; mitigated by human GC step | Active |
| Spaced-repetition timetable (SM-2) | components/timetableAlgorithm.ts | Sometimes perceived as AI | None — SM-2 algorithm | Client-side | None | Out of scope | Active |
| Smart "what next" recommendation | hooks/useRecommendation.ts | No | None — rule-based | Client-side | None | Out of scope | Active |
| Reflection quality scoring | components/ReflectionModal.tsx | No | None — heuristic | Client-side | None | Out of scope | Active |
| Gemini-backed features | n/a | n/a | n/a | n/a | n/a | High-risk if reactivated; full review required first | **Not implemented. Documentation drift in README/CLAUDE.md corrected 2026-04-29; historical leaked-in-bundle config remediated 2026-04-06 in commit `063d574`. Audit: `compliance/GEMINI_AUDIT.md`.** |
| Any third-party LLM | n/a | n/a | n/a | n/a | n/a | n/a | Not implemented |
| Analytics / behavioural inference | n/a | n/a | n/a | n/a | n/a | n/a | Not implemented |

---

## 8. Document control

- Source code reviewed: commit `0ac6be4` on branch `main`.
- Verification method for "no LLM in build": initial exhaustive grep over `*.ts`, `*.tsx`, `*.json` for `gemini`, `@google/gen`, `GoogleGenerativeAI`, `GoogleGenAI`, `generateContent`, `Anthropic`, `OpenAI` (commit `0ac6be4`); independently re-verified 2026-04-29 with full git-log search across all branches — see `compliance/GEMINI_AUDIT.md`. README.md and CLAUDE.md drift mentions were corrected on the same date.
- Companion documents: DPIA.md, DPA_SCHEDULES.md, SUMMARY.md.
