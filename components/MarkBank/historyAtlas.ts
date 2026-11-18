/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Which Topic Atlas question a History card belongs to, read off its citation.
 *
 * The Atlas tags a History paper by the units it PRINTS: the documents
 * question's four parts ("1" to "4"), and each topic block of Sections 2 and 3
 * as one question — "I1" to "I6" for Ireland, "E1" to "E6" for Europe and the
 * wider world — because a candidate answers inside one block, and its four
 * essays (or its Ordinary Level parts A, B and C) all sit under that block's
 * syllabus topic. The 2023-2025 Ordinary papers' extra Part A is "ALT".
 *
 * So a History card's own Atlas question is its block's: "Section 2 Topic 1
 * Q3" resolves to "I1", "Section 3 Topic 5 B" to "E5", "Section 1 Q4(a)" to
 * "4". The two fields of study are separate papers and separate Atlas
 * subjects: an Early Modern citation resolves under "history-early-modern".
 */
import type { SecCard } from '../../types/markBank';

export interface HistoryAtlasAddress {
  subjectId: 'history' | 'history-early-modern';
  fileid: string;
  n: string;
}

export function historyAtlasQuestion(card: Pick<SecCard, 'questionRef' | 'paperFileid'>): HistoryAtlasAddress | null {
  if (!card.paperFileid) return null;
  const ref = card.questionRef;
  const subjectId = /\bEarly Modern\b/.test(ref) ? 'history-early-modern' : 'history';
  const fileid = `${card.paperFileid.replace(/\.pdf$/i, '')}.pdf`;
  const dbq = /\bSection 1 Q(\d)\b/.exec(ref);
  if (dbq) return { subjectId, fileid, n: dbq[1] };
  const block = /\bSection ([23]) Topic (\d)\b/.exec(ref);
  if (block) return { subjectId, fileid, n: `${block[1] === '2' ? 'I' : 'E'}${block[2]}` };
  if (/\bSection Extra A\b/.test(ref)) return { subjectId, fileid, n: 'ALT' };
  return null;
}
