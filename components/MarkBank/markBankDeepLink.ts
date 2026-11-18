/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Open the Mark Bank on exactly the cards a Topic Atlas question names ("Practise these parts in the Mark Bank",
 * atlasModel.markBankLinkForCards). Reads the boot-time URL snapshot once, like vaultDeepLink; never touches history.
 * Only cards with a topic record in the single model are honoured, so a link can only open real cards of one deck.
 */
import { getBootParam } from '../../utils/bootParams';
import { askRecord } from '../PaperTrail/atlasModel';

let consumed = false;

export interface MarkBankCardLink { subjectId: string; level: string; cardIds: string[] }

export function consumeInitialMarkBankCards(): MarkBankCardLink | null {
  if (consumed) return null;
  consumed = true;
  if (getBootParam('tool') !== 'mark-bank') return null;
  const ids = (getBootParam('cards') ?? '').split(',').map(id => id.trim()).filter(Boolean).slice(0, 60);
  const first = ids.map(askRecord).find(Boolean);
  if (!first) return null;
  const cardIds = ids.filter(id => { const r = askRecord(id); return r?.subjectId === first.subjectId && r.level === first.level; });
  return { subjectId: first.subjectId, level: first.level, cardIds };
}

/** Reset the once-guard: test-only. */
export function __resetMarkBankDeepLinkForTest(): void { consumed = false; }
