import { claimMatches, comparableScheme } from './schemeText.mjs';

/** Include every selectable route in the ordinary whole-scheme answer check. */
export const japaneseAnswerRows = card => [
  ...(card.rows ?? []),
  ...(card.answerVariants ?? []).flatMap(variant => variant.rows),
];

/** A selectable route must also bind to this task's reviewed physical pages. */
export function assertJapaneseVariantSources(card, selectors, unprintedAnswer) {
  if (!card.answerVariants?.length) return;
  const pages = card.sourceEvidence?.schemePages ?? [];
  const source = comparableScheme(selectors.filter(selector => selector.document === 'scheme'
    && pages.includes(selector.page)).map(selector => selector.text).join('\n'));
  for (const variant of card.answerVariants ?? []) {
    for (const row of variant.rows) {
      if (row.unprinted) {
        if (row.verbatim !== unprintedAnswer) throw new Error(`${card.id}/${variant.id}: unprinted route invents an answer`);
        continue;
      }
      const answers = row.kind === 'anyN' ? row.group.options : [row.verbatim];
      const unsupported = answers.filter(answer => !answer?.trim() || !claimMatches(source, answer));
      if (unsupported.length) throw new Error(`${card.id}/${variant.id}: variant answer is not bound to its task's reviewed scheme pages: ${JSON.stringify(unsupported)}`);
    }
  }
}
