/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "Career Paths" — a card deck that shows Leaving Cert students what real
 * careers actually involve: what you do, what they pay (Irish €), how you get
 * there (CAO / PLC / apprenticeship / professional exams), the skills you need
 * and the honest pros & cons. Each card links to the real CAO courses that lead
 * there — the same courses the Future Finder produces as results — so the deck
 * doubles as the "explore your matches" surface from the Future Finder results.
 *
 * Same immersive "colour world" register as How They Did It: each career field
 * owns a bold colour, one idea per screen, less text + more wow. Content is
 * source-grounded (Irish salary + route data) and verified.
 */

export type CareerField =
  | 'health'
  | 'animals'
  | 'tech'
  | 'engineering'
  | 'law'
  | 'psychology'
  | 'business'
  | 'education'
  | 'design'
  | 'science'
  | 'trades'
  | 'creative';

/** Irish salary band in € thousands (typical, not outliers). */
export interface SalaryBand {
  /** Rounded typical early-career full-time gross base pay, € thousands. */
  startK: number;
  /** Rounded typical experienced gross base pay, € thousands. */
  experiencedK: number;
  /** One short context line, e.g. "public pay scale" or "varies by firm". */
  note: string;
  /** How confidently the figures can be compared with a conventional salary. */
  basis?: 'public-scale' | 'market-estimate' | 'mixed-income';
}

/** One way in from the Leaving Cert. */
export interface EducationRoute {
  /** e.g. "CAO degree · Level 8", "Apprenticeship", "PLC → degree". */
  label: string;
  /** One short line of detail. */
  detail: string;
}

/**
 * "A Day in the Life" — a mistake-first decision moment from the real job.
 * The student makes the call, often picks the tempting-but-wrong option, sees
 * the realistic consequence, then the experienced-practitioner fix. Vicarious
 * mastery rehearsal (Bandura 1997 — the strongest mover of self-efficacy).
 * Each moment cites a real professional standard; paraphrased under the
 * 15-word verbatim threshold, decision-support not drama.
 */
export interface ShiftMoment {
  /** The dilemma, set in the real day-to-day. */
  setup: string;
  /** 2–3 choices; exactly one is correct. */
  options: string[];
  /** Index of the correct choice. */
  correctIndex: number;
  /** Index of the intuitive-but-wrong choice (the one most will reach for). */
  temptingIndex: number;
  /** Realistic outcome of the tempting-wrong choice. */
  consequence: string;
  /** The experienced-practitioner reasoning. */
  fix: string;
  /** Professional body / guidance the fix is grounded in. */
  source: string;
}
export interface DayInLife { moments: ShiftMoment[]; }

export interface CareerCard {
  id: string;
  title: string;
  field: CareerField;
  /** Emoji glyph (legacy data shape; the UI renders a line icon, not this). */
  emoji: string;
  /** Optional per-card icon key (see immersiveDeck/deckGlyphs CAREER_ICONS) — a
   *  distinct line icon while keeping the field's colour world. Falls back to the
   *  field icon when omitted. */
  iconKey?: string;
  /** Optional custom image for the card icon, path relative to /public
   *  (e.g. "career-icons/nurse.png"). Rendered in place of the line icon; falls
   *  back to the line icon if the image is missing. */
  image?: string;
  /** A short identity / "what it's really like" line (≤10 words). */
  tagline: string;
  /** Day-to-day, 2-3 short bullets. */
  whatYouDo: string[];
  /** Irish pay band. */
  salary: SalaryBand;
  /** 1-3 routes in from the LC. */
  routes: EducationRoute[];
  /** 4-6 concrete role skills. */
  skills: string[];
  /** 3 honest upsides. */
  pros: string[];
  /** 3 honest downsides. */
  cons: string[];
  /**
   * Exact `careerPaths` strings used in CAO_COURSES (futureFinderData) that map
   * to this career. Drives (a) the "courses that lead here" list, computed at
   * runtime, and (b) "jump to your matches" from the Future Finder results.
   */
  matchStrings: string[];
  /** Source citations for the salary + route claims. */
  sources: string[];
  /** Optional mistake-first decision sim ("A Day in the Life"). Per-card + optional:
   *  careers without one show the standard 4-beat walkthrough unchanged. */
  dayInLife?: DayInLife;
}

/** Persisted under progress/{uid}.careerPaths (additive-merge namespace). */
export interface CareerPathsState {
  /** Career ids opened. */
  seenIds: string[];
  /** Career ids saved / shortlisted. */
  savedIds: string[];
  /** Per-career "could I see myself doing this?" self-rating (1–5) from the sim. */
  shiftRatings?: Record<string, number>;
  updatedAt: string;
}
