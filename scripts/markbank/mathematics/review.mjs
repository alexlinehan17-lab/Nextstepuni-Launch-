/** Reviewed SEC Mathematics boundaries and placement, shared by both tools. */
import { readFileSync, readdirSync } from 'node:fs';

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

/** Metadata-only correction: existing identities and answer content survive. */
export function applyMathematicsReview(authored) {
  const review = reviewedCards.get(authored.id);
  if (!review) return authored;
  const { paper, card } = review;
  if (authored.year !== paper.year || authored.level !== paper.level
      || authored.totalMarks !== card.totalMarks) {
    throw new Error(`${authored.id}: authored card disagrees with the reviewed SEC boundary`);
  }
  if (!/^[0-9]+[ABCD]$/.test(card.scale)
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
