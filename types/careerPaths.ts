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
  /** Typical starting full-time salary, € thousands. */
  startK: number;
  /** Typical experienced / senior salary, € thousands. */
  experiencedK: number;
  /** One short context line, e.g. "public pay scale" or "varies by firm". */
  note: string;
}

/** One way in from the Leaving Cert. */
export interface EducationRoute {
  /** e.g. "CAO degree · Level 8", "Apprenticeship", "PLC → degree". */
  label: string;
  /** One short line of detail. */
  detail: string;
}

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
}

/** Persisted under progress/{uid}.careerPaths (additive-merge namespace). */
export interface CareerPathsState {
  /** Career ids opened. */
  seenIds: string[];
  /** Career ids saved / shortlisted. */
  savedIds: string[];
  updatedAt: string;
}
