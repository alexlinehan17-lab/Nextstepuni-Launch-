/** Presentation shared by the app reader and the public legal documents. */
import { PRIVACY_NOTICE, TERMS_OF_USE, type LegalDoc } from './legalContent';

export const LEGAL_DRAFT_NOTE = 'Draft under legal review. The wording may change before final publication.';

export const legalSections = (doc: LegalDoc) => doc === 'privacy' ? PRIVACY_NOTICE : TERMS_OF_USE;
export const legalSectionId = (doc: LegalDoc, index: number) => `${doc}-section-${index + 1}`;
export const legalSectionNumber = (index: number) => String(index + 1).padStart(2, '0');

export type LegalBlock = { type: 'paragraph'; text: string } | { type: 'list'; items: string[] };

/** Preserve copy order while giving consecutive bullet lines real list semantics. */
export function legalBlocks(lines: string[]): LegalBlock[] {
  const blocks: LegalBlock[] = [];
  for (const line of lines) {
    if (!line.startsWith('• ')) {
      blocks.push({ type: 'paragraph', text: line });
      continue;
    }
    const previous = blocks.at(-1);
    if (previous?.type === 'list') previous.items.push(line.slice(2));
    else blocks.push({ type: 'list', items: [line.slice(2)] });
  }
  return blocks;
}
