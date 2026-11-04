/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The instruction words the Leaving Certificate exam-language papers print,
 * language by language, each with the English a teacher would give for it.
 * Only these words are glossed: the rest of an exam-language question stays
 * exactly as printed, because translating it could give away a vocabulary
 * answer. Generated from each language's own cards and checked by a second
 * reader (scripts/markbank/waysin/exam-lexicons.json).
 */

export interface ExamCommand {
  /** The printed form, lower case. */
  surface: string;
  /** The gloss key in the key-parts lexicon. */
  key: string;
  /** The plain English instruction, 1–4 words. */
  english: string;
  /** "start": begins its sentence (after a lead phrase); "anywhere": a question word. */
  position: 'start' | 'anywhere';
}

export interface ExamLexicon {
  commands: ExamCommand[];
  counts: Record<string, number>;
  conditions: Array<{ surface: string; english: string; kind: string }>;
  details: Array<{ surface: string; english: string }>;
  locatorWords: string[];
}

// Filled once each language's lexicon has been checked by a second reader.
export const EXAM_LEXICONS: Record<string, ExamLexicon> = {};
