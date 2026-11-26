/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Sentence case for a short label shown on screen ("Keep My Options Open" ->
 * "Keep my options open"), the system's rule for words a student reads
 * (tokens.md, "Type"). Display only: the stored value is never changed.
 * The first word keeps its capital; "I" (and "I'm", "I'd") and acronyms
 * written in capitals ("CAO", "PLC") stay as they are.
 */
export function sentenceCase(label: string): string {
  return label
    .split(' ')
    .map((word, index) => {
      if (index === 0) return word.charAt(0).toLocaleUpperCase() + word.slice(1);
      if (/^I(['’][a-z]+)?$/.test(word)) return word;
      if (word.length > 1 && /^[A-Z0-9&]+[.,;:!?]?$/.test(word)) return word;
      return word.toLocaleLowerCase();
    })
    .join(' ');
}
