/** Emit Atlas's exact-booklet placement from independently reviewed tasks. */
import { readFileSync, writeFileSync } from 'node:fs';
import { mathematicsReviews, validateMathematicsReviewSources } from './review.mjs';

const target = new URL('../../../data/examTopics/mathematics-reviewed-question-runtime.json', import.meta.url);
const taxonomy = JSON.parse(readFileSync(new URL('../../../data/examTopics/mathematics-runtime.json', import.meta.url), 'utf8'));
const topicIds = taxonomy.topics.map(topic => topic[0]);
validateMathematicsReviewSources();
const mappings = [];
for (const paper of mathematicsReviews()) {
  const questions = new Map();
  for (const card of paper.cards) {
    const numbers = [...new Set(card.printedParts.map(part => part.match(/^Q(\d+)/)?.[1]))];
    if (numbers.some(number => !number)) throw new Error(`${card.id}: missing printed question number`);
    const indexes = card.examTopicIds.map(id => {
      const index = topicIds.indexOf(id);
      if (index < 0) throw new Error(`${card.id}: unknown Atlas topic ${id}`);
      return index;
    });
    for (const number of numbers) {
      questions.set(number, [...new Set([...(questions.get(number) ?? []), ...indexes])].sort((a, b) => a - b));
    }
  }
  for (const [number, indexes] of questions) {
    mappings.push([
      { higher: 'h', ordinary: 'o', foundation: 'f' }[paper.level],
      paper.lang === 'ev' ? 'e' : 'i', paper.year, paper.paperKey,
      paper.paperFileid, number, indexes,
    ]);
  }
}
const rendered = JSON.stringify({ schemaVersion: 1, subjectId: 'mathematics', topicIds, questionMappings: mappings }) + '\n';
if (process.argv.includes('--check')) {
  if (readFileSync(target, 'utf8') !== rendered) throw new Error('Mathematics reviewed Atlas mappings are stale');
} else writeFileSync(target, rendered);
console.log(`${mappings.length} reviewed Mathematics question placements`);
