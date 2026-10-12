/** Reviewed SEC Mathematics boundaries and placement, shared by both tools. */
import { readFileSync, readdirSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

export function mathematicsReviews() {
  const directory = new URL('./reviews/', import.meta.url);
  return readdirSync(directory).filter(name => name.endsWith('.json')).sort()
    .map(name => JSON.parse(readFileSync(new URL(name, directory), 'utf8')));
}

const reviewedCards = new Map();
for (const paper of mathematicsReviews()) {
  for (const card of paper.cards) {
    if (reviewedCards.has(card.id)) throw new Error(`Duplicate Mathematics review: ${card.id}`);
    reviewedCards.set(card.id, { paper, card });
  }
}

/** Only independent review records can supply an exact booklet identity. */
export function reviewedMathematicsSource(cardId) {
  const paper = reviewedCards.get(cardId)?.paper;
  return paper && {
    paperFileid: paper.paperFileid,
    schemeFileid: paper.schemeFileid,
    lang: paper.lang,
  };
}

/** Metadata-only correction: existing identities and answer content survive. */
export function applyMathematicsReview(authored) {
  const review = reviewedCards.get(authored.id);
  if (!review) return authored;
  const { paper, card } = review;
  if (authored.year !== paper.year || authored.level !== paper.level
      || authored.totalMarks !== card.totalMarks) {
    throw new Error(`${authored.id}: authored card disagrees with the reviewed SEC boundary`);
  }
  if (card.questionText !== undefined && (authored.questionText !== card.questionText
      || (authored.stem ?? '') !== (card.stem ?? ''))) {
    throw new Error(`${authored.id}: prompt disagrees with the independently reviewed text`);
  }
  // A–E: the SEC labels scales by their number of categories (2–6). The six-category
  // E scale appears on some adjusted papers (2021–2022), for example 2022 HL Paper 2 Q10(e).
  if (!/^[0-9]+[ABCDE]$/.test(card.scale)
      || card.permittedMarks.length !== 'ABCDE'.indexOf(card.scale.at(-1)) + 2
      || Number.parseInt(card.scale, 10) !== card.totalMarks
      || card.permittedMarks[0] !== 0
      || card.permittedMarks.at(-1) !== card.totalMarks
      || card.permittedMarks.some((mark, index, marks) => !Number.isInteger(mark)
        || (index > 0 && mark <= marks[index - 1]))
      || typeof paper.fullCreditMinusOne !== 'boolean'
      || !paper.generalNotesPages?.length
      || !card.schemePages?.length) {
    throw new Error(`${authored.id}: incomplete reviewed Mathematics scale`);
  }
  return {
    ...authored,
    topicId: card.topicId,
    qa: { gates: ['verbatim', 'tariff', 'figure'], humanReviewedBy: 'agent-verified', humanReviewedAt: paper.reviewedAt },
    mathematicsScale: {
      code: card.scale,
      marks: card.permittedMarks,
      fullCreditMinusOne: paper.fullCreditMinusOne,
      schemeFileid: paper.schemeFileid,
      schemePages: card.schemePages,
      generalNotesPages: paper.generalNotesPages,
    },
    sourceMaterial: {
      kind: 'source-question',
      label: 'OFFICIAL QUESTION PAGES',
      title: 'Question, diagrams and working space',
      pages: card.sourcePages,
      sourceFileid: paper.paperFileid,
      ...(card.measurementRequired ? { measurementRequired: true } : {}),
      attribution: `SEC Mathematics ${paper.year} ${({ higher: 'Higher', ordinary: 'Ordinary', foundation: 'Foundation' })[paper.level]} Level examination paper — © State Examinations Commission.`,
      presentationNote: 'Open the original question pages to inspect the notation, graphs, diagrams and any earlier parts needed for this task. Zoom in, then close the pages to return to your answer.',
    },
  };
}

/** Authoring requires the exact visually reviewed originals on disk. */
export function validateMathematicsReviewSources() {
  execFileSync('python3', [fileURLToPath(new URL('./audit.py', import.meta.url)), '--check-reviewed'], { stdio: 'inherit' });
}

/** A reviewed task must never disappear as a side effect of a build guard. */
export function assertReviewedMathematicsCards(outputIds, rejectionReasons = []) {
  const emitted = new Set(outputIds);
  const missing = [...reviewedCards.keys()].filter(id => !emitted.has(id));
  if (missing.length) {
    const reasons = rejectionReasons.filter(reason => missing.some(id => reason.startsWith(`${id}:`)));
    throw new Error(`Reviewed Mathematics tasks rejected by generation: ${missing.join(', ')}\n${reasons.join('\n')}`);
  }
}
