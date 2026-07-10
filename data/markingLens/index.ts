/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Marking Lens — registry + lookup. Per-subject lens files register here; the
 * Topic Vault card looks a question up by its sibling key. Grows subject by
 * subject exactly like the topic tags did (authored ONLY from filed schemes —
 * see types.ts for the honesty rules and test/markingLens.test.ts for the
 * machine-checked integrity gates).
 */

import { type QuestionLens, type SubjectLens } from './types';
import BUSINESS_LENS from './business';

export const MARKING_LENS: SubjectLens[] = [
  BUSINESS_LENS,
];

const key = (subjectId: string, year: number, level: string, lang: string, fileid: string, n: string) =>
  `${subjectId}|${year}|${level}|${lang}|${fileid}|${n}`;

const byKey = new Map<string, QuestionLens>();
for (const s of MARKING_LENS) {
  for (const e of s.entries) {
    byKey.set(key(s.subjectId, e.year, e.level, e.lang, e.fileid, e.n), e);
  }
}

/** The lens for one vault question, or null when none is authored yet. */
export function lensFor(t: {
  subjectId: string; year: number; level: string; lang: string; fileid: string; n: string;
}): QuestionLens | null {
  return byKey.get(key(t.subjectId, t.year, t.level, t.lang, t.fileid, t.n)) ?? null;
}

export type { QuestionLens, LensPart, LensPitfall, SubjectLens } from './types';
