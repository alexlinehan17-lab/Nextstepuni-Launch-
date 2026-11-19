/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Open the Mark Bank on exactly the cards a Topic Atlas question names ("Practise these parts in the Mark Bank",
 * atlasModel.markBankLinkForCards). Reads the boot-time URL snapshot once, like vaultDeepLink; never touches history.
 * Only a subject in the single model is honoured, and MarkBank.tsx keeps only cards its own deck holds.
 */
import { getBootParam } from '../../utils/bootParams';
import { isModelSubject } from '../PaperTrail/atlasModel';

let consumed = false;

export interface MarkBankCardLink { subjectId: string; level: string; cardIds: string[] }

export function consumeInitialMarkBankCards(): MarkBankCardLink | null {
  if (consumed) return null;
  consumed = true;
  if (getBootParam('tool') !== 'mark-bank') return null;
  const subjectId = getBootParam('mbsubject') ?? '';
  const level = getBootParam('mblevel') ?? '';
  const cardIds = (getBootParam('cards') ?? '').split(',').map(id => id.trim()).filter(Boolean).slice(0, 60);
  // Only a subject in the single model, at a real level; MarkBank.tsx then keeps only cards its deck holds.
  if (!isModelSubject(subjectId) || !['higher', 'ordinary', 'foundation', 'common'].includes(level) || !cardIds.length) return null;
  return { subjectId, level, cardIds };
}

/** Reset the once-guard: test-only. */
export function __resetMarkBankDeepLinkForTest(): void { consumed = false; }
