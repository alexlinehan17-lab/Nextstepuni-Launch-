/** Attach a second physical edition only after its independent source review.
 * The Python review gate checks hashes, directives and exact route equivalence.
 * This check additionally ties those routes to the cards actually being built.
 */
import { resolvePaperFileid } from './paperIndex.mjs';

export function assertEconomicsReviewCoverage(builtIds, reviews) {
  const required = new Set(reviews.flatMap(review => review.questions.flatMap(
    question => question.tasks.map(task => task.cardId),
  )));
  const missing = [...required].filter(id => !builtIds.has(id));
  if (missing.length) {
    throw new Error(`Reviewed Economics tasks dropped during generation: ${missing.join(', ')}`);
  }
}

export function bindEconomicsEditions(cards, reviews) {
  const byId = new Map(cards.map(card => [card.id, card]));
  for (const review of reviews) {
    if (!review.equivalentTo) continue;
    if (review.lang !== 'iv' || review.equivalentTo.lang !== 'ev') {
      throw new Error('Unsupported reviewed Economics edition pairing');
    }
    for (const question of review.questions) {
      for (const task of question.tasks) {
        const card = byId.get(task.cardId);
        if (!card || card.year !== review.year || card.level !== review.level
            || card.totalMarks !== task.marks || card.topicId !== task.topicId
            || card.questionRef.match(/Q(\d+)/)?.[1] !== question.n
            || resolvePaperFileid('economics', card.year, card.level, card.section)
              !== review.equivalentTo.fileid) {
          throw new Error(`Reviewed edition does not match built card: ${task.cardId}`);
        }
        if (!card.sourceMaterial) {
          throw new Error(`Equivalent task lacks its primary source: ${task.cardId}`);
        }
        card.sourceMaterial.label = 'ENGLISH QUESTION PAGE';
        card.sourceMaterial.title = `English question ${question.n}`;
        card.additionalSourceMaterials = [...(card.additionalSourceMaterials ?? []), {
          kind: 'source-illustration',
          label: 'IRISH QUESTION PAGE',
          title: `Irish question ${question.n}`,
          pages: question.paperPages,
          sourceFileid: review.fileid,
          attribution: `SEC Economics ${review.year} ${review.level === 'higher' ? 'Higher' : 'Ordinary'} Level — Irish examination paper — © State Examinations Commission.`,
          presentationNote: 'Open the Irish edition of this question. Use the labels printed in that edition; the answer guidance explains any differences.',
        }];
        if (task.answerGuidance) {
          card.rows[0].contextNote = [card.rows[0].contextNote, task.answerGuidance]
            .filter(Boolean).join('\n\n');
        }
      }
    }
  }
}
