/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Necessary Knowledge tab — types shared across the tab's components and
 * its data files. All content here traces to /docs/leaving-cert-knowledge-
 * dossier.md, which itself is sourced from SEC marking schemes, Chief
 * Examiner Reports, and NCCA documents. Every entry below carries a
 * `source` reference back into the dossier.
 */

/** A pointer back into the dossier, so any claim is auditable. */
export interface DossierRef {
  /** Section identifier from the dossier — e.g. "A1", "B1", "D". */
  section: string;
  /** Approximate page in the markdown / source PDF. */
  page?: number;
  /** Optional line — the original source the dossier itself cites
   *  (e.g. "2013 Chief Examiner Report — English"). */
  cite?: string;
}

// ─── Command Word Decoder (E1) ──────────────────────────────────────────

export interface CommandWordEntry {
  word: string;
  /** What this command word actually demands. One sentence. */
  requiredAction: string;
  /** Typical mark range where this command appears. */
  typicalMarkRange: string;
  /** Structural template for the answer. */
  structuralTemplate: string;
  /** Specific common error from CERs / marking schemes for this word. */
  commonError: string;
  /** Optional aliases — words treated as equivalent (e.g. "Assess" → "Evaluate"). */
  aliases?: string[];
  source: DossierRef;
}

/** Modifiers are words that change the demand around a command word —
 *  "significant", "effective", "deeply embedded". The Purpose marks in
 *  English live in these. Dossier A1 p.3. */
export interface ModifierEntry {
  word: string;
  /** What this modifier signals about the demand. */
  signal: string;
  source: DossierRef;
}

// ─── Examiner Pet-Peeve Trainer (E12) ──────────────────────────────────

export interface ExaminerPetPeeve {
  id: string;
  subject: string;
  /** Paraphrased summary of the peeve. Never more than 15 words verbatim
   *  per source, per /CLAUDE.md content quality rules. */
  peeve: string;
  /** Year of the underlying Chief Examiner Report or marking scheme. */
  reportYear: number;
  /** A worked example of what triggers it. */
  example: string;
  /** The fix — one specific, actionable behaviour. */
  fix: string;
  source: DossierRef;
}

// ─── Marking Scheme Grammar Explainer (E2-cousin) ──────────────────────

export interface MarkingGrammarRule {
  title: string;
  body: string;
}

export interface SubjectMarkingGrammar {
  id: string;
  subjectLabel: string;
  /** Short narrative — the architecture of how this subject is marked. */
  architecture: string;
  rules: MarkingGrammarRule[];
  /** Optional worked example showing the marking applied. */
  workedExample?: { setup: string; outcome: string };
  source: DossierRef;
}

// ─── Time-Allocation Calculator (E3) ───────────────────────────────────

export interface SubjectTimingBreakdown {
  section: string;
  marks: number;
  minutes: number;
}

export interface SubjectTiming {
  id: string;
  subjectLabel: string;
  totalMarks: number;
  totalMinutes: number;
  /** Mock breakdown of how to spend the time across sections. */
  breakdown: SubjectTimingBreakdown[];
  source: DossierRef;
}

// ─── Quick-Check (used at end of every module) ─────────────────────────

export interface QuickCheckQuestion {
  id: string;
  prompt: string;
  options: string[];
  correctAnswer: string;
  /** Brief explanation shown after answering. */
  explanation: string;
}

// ─── Stage 2: SRP Identifier (E10) ──────────────────────────────────────

/** Examiner classification of a single sentence inside a long-question
 *  paragraph. Drives the heat-map and mark-provenance trail. */
export type SrpSentenceType =
  | 'srp'           // Counts — significant, relevant, develops the question
  | 'unsupported'   // Accurate but doesn't develop the question — 0 marks
  | 'waffle'        // Generic, padding, repeated — 0 marks
  | 'inaccurate';   // Factually wrong — 0 marks (and may signal errors)

export interface SrpSentence {
  id: string;
  text: string;
  type: SrpSentenceType;
  /** For SRPs: short label of the factor / process this sentence develops.
   *  Used in the diagnostic feedback ("missed SRPs cluster around X"). */
  developsFactor?: string;
  /** For non-SRPs: why this doesn't score. */
  reason?: string;
  /** A "buried" SRP follows a waffle sentence — examiners scan first
   *  sentences and may underweight a buried SRP. Used in feedback. */
  buried?: boolean;
}

export interface SrpSample {
  id: string;
  subject: 'geography' | 'history' | 'business';
  /** Subject-specific topic, e.g. "Coastal erosion — stack formation". */
  topicLabel: string;
  /** The question prompt the paragraph answers, paraphrased — never more
   *  than 15 words verbatim from any SEC paper, per /CLAUDE.md. */
  questionPrompt: string;
  /** Total marks available in the original question. Geography long-Q
   *  essays are typically 30 marks; an Option essay is 80. */
  marksAvailable: number;
  /** SRP cap implied by mark allocation — e.g. 30 marks → 15 SRPs. */
  srpCap: number;
  sentences: SrpSentence[];
  source: DossierRef;
}

// ─── Stage 2: Working-Shown Allocator (E9) ──────────────────────────────

/** A single step in the marker's annotated working. As the student
 *  reveals each step, marks accrue (or are deducted via a slip/blunder). */
export interface WorkingStep {
  id: string;
  /** Short label shown on the step card — e.g. "Write the formula". */
  label: string;
  /** The actual maths/working displayed in the answer scaffold. */
  contentLines: string[];
  /** Marks awarded for this step (positive). */
  marksEarned: number;
  /** Penalties applied here (negative). Keys: 'slip' | 'blunder' | 'misread'. */
  penalty?: { kind: 'slip' | 'blunder' | 'misread'; amount: number; reason: string };
  /** Examiner-voice annotation. */
  annotation: string;
}

/** A pre-defined "answer path" — what a real exam script might look like.
 *  Used for the rewind / what-if comparison feature. */
export interface WorkingAnswerPath {
  id: 'blank' | 'formula-only' | 'formula-sub' | 'full-with-slip' | 'full-correct';
  label: string;
  /** Step IDs (from the question's `steps`) included in this path. */
  includedStepIds: string[];
  /** Final score under this path. */
  finalScore: number;
  /** Why a real student would land here. */
  characterisation: string;
}

export interface WorkingQuestion {
  id: string;
  subject: 'maths' | 'chemistry' | 'physics' | 'accounting';
  /** Subject-specific topic. */
  topicLabel: string;
  /** Question prompt, paraphrased. */
  questionPrompt: string;
  /** Total marks. */
  marksAvailable: number;
  /** The published partial-credit scale (for Maths-style rubrics). */
  scaleLabel?: string;
  steps: WorkingStep[];
  paths: WorkingAnswerPath[];
  source: DossierRef;
}

// ─── Stage 2: Sanity-Check Trainer (E6) ────────────────────────────────

/** The four sanity checks that catch absurd answers in quantitative
 *  subjects, per dossier § C1. */
export type SanityCheck = 'order-of-magnitude' | 'units' | 'sign' | 'substitute-back';

export interface SanityCandidate {
  id: string;
  /** The candidate answer text. */
  text: string;
  /** Whether this candidate is correct. */
  correct: boolean;
  /** If wrong: which check would have caught it. */
  catchingCheck?: SanityCheck;
  /** Short explanation of why the answer is absurd, with a real-world anchor. */
  absurdityExplanation?: string;
}

export interface SanityCheckQuestion {
  id: string;
  subject: 'maths' | 'chemistry' | 'physics' | 'biology';
  topicLabel: string;
  questionPrompt: string;
  candidates: SanityCandidate[];
  source: DossierRef;
}

// ─── Stage 2: Spot the Trap (E4) ───────────────────────────────────────

export type TrapCategory =
  | 'modifier'           // English: "significant", "effective", "deeply"
  | 'plural-singular'    // Maths: "values" (plural) vs "value"
  | 'command-switch'     // Inside a sub-part the command word changes
  | 'definition-keyphrase' // Sciences: missing key phrase in a definition
  | 'state-symbol'       // Chemistry: state symbols required
  | 'process-vs-landform' // Geography: process question answered as landform
  | 'named-example'      // Geography option: missing named example
  | 'tense-disguise'     // Languages: time-word with non-matching tense
  | 'in-terms-of'        // Maths: "in terms of x" forces algebraic form
  | 'date-precision';    // History DBQ: date precision required

export interface TrapCard {
  id: string;
  subject: string;
  category: TrapCategory;
  /** Short subject + paper hint, e.g. "Maths HL Paper 1". */
  paperLabel: string;
  /** The question text — paraphrased, never more than 15 words verbatim
   *  from any SEC paper. */
  questionText: string;
  /** Index range in `questionText` of the trap term to underline. */
  trapSpans: { start: number; end: number }[];
  /** Short label — what the trap is. */
  trapLabel: string;
  /** Why students miss it. */
  whyStudentsMiss: string;
  /** What the marking-scheme cost is. */
  consequence: string;
  /** Approximate share of the question's marks at risk. */
  marksAtRiskPct: number;
  source: DossierRef;
}

// ─── Stage 2: Sub-task Ceiling Visualiser (E5) ─────────────────────────

export interface CeilingScenario {
  id: string;
  /** Subject + question type label. */
  scenarioLabel: string;
  /** The marking-scheme rule that creates the cap. */
  capRuleLabel: string;
  /** Apparent quality (out of 100) — what a generous reader would award. */
  apparentQuality: number;
  /** Marks the student expects. */
  studentExpectation: number;
  /** Marks the student actually gets after the cap fires. */
  actualScore: number;
  /** The cap itself (often equal to actualScore but can differ). */
  capLevel: number;
  /** A 4-6 sentence "answer body". The cap-trigger sentence is flagged. */
  answerSentences: { id: string; text: string; isCapTrigger?: boolean }[];
  /** What the student should have done at the cap-trigger moment. */
  counterfactual: {
    actionLabel: string;
    actionDetail: string;
    /** Marks they would have earned with the counterfactual. */
    liftedScore: number;
  };
  /** Optional cross-link to another knowledge module. */
  crossLink?: { moduleId: string; moduleLabel: string };
  source: DossierRef;
}
