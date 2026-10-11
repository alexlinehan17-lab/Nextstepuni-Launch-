#!/usr/bin/env node
/** Build the library's canonical topic lookup from source-pinned card/Atlas reviews.
 * This changes navigation metadata only, never a card's ID, wording or marks.
 * A cross-topic task belongs to every reviewed constituent topic; it is not
 * assigned by a raw alias or by the whole printed question's broader union.
 */
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
export function buildConstructionLibraryTopics() {
  return buildReviewedLibraryTopics('construction-studies', 'cons-', 'construction-studies:outgoing');
}
function buildReviewedLibraryTopics(subjectId, topicPrefix = `${subjectId}-`, specificationId = `${subjectId}:legacy-current`) {
  // Canonical IDs may address an explicit section context as well as numbered outcomes.
  // This source-reviewed crosswalk is checked against curriculumRegistry by the Atlas tests.
  const crosswalk = JSON.parse(fs.readFileSync(path.join(root, `data/examTopics/${subjectId}-curriculum-crosswalk.json`), 'utf8'));
  const canonicalTopics = new Set(Object.values(crosswalk).flat());
  const subjectLabel = subjectId[0].toUpperCase() + subjectId.slice(1);
  const directory = path.join(root, 'scripts/markbank/atlas-reviews');
  const reviews = fs.readdirSync(directory).filter(name => name.startsWith(`${subjectId}-`) && name.endsWith('.json'))
    .map(name => JSON.parse(fs.readFileSync(path.join(directory, name), 'utf8')));
  const entries = {};
  const papers = [];
  for (const review of reviews) {
    if (review.sitting !== 'main') throw new Error('A deferred review needs a sitting-aware library intake');
    for (const [file,digest] of Object.entries(review.sourceHashes)) {
      if (createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex') !== digest) throw new Error(`Changed source: ${file}`);
    }
    const authored = JSON.parse(fs.readFileSync(path.join(root,review.authoringReview),'utf8'));
    const cards = new Map(authored.tasks.map(task => [task.card.id,task.card]));
    const bridge = new Map(review.cards.map(card => [card.cardId,card]));
    const topicsFor = (id,seen = new Set()) => {
      if (seen.has(id)) throw new Error(`Circular task group: ${id}`);
      const card=cards.get(id);
      const binding=bridge.get(id);
      if (!card || !binding || binding.markBankTopicId !== card.topicId) throw new Error(`Missing exact ${subjectLabel} topic bridge: ${id}`);
      if (!card.topicId.startsWith(topicPrefix)) throw new Error(`Not an outgoing ${subjectLabel} topic: ${id}`);
      if (!card.taskGroups) {
        const topics=binding.canonicalTopicIds ?? [card.topicId];
        if (!topics.includes(card.topicId) || new Set(topics).size !== topics.length
          || (topics.length > 1 && !binding.canonicalTopicReview?.trim())
          || topics.some(topic => !canonicalTopics.has(topic))) {
          throw new Error(`Invalid reviewed ${subjectLabel} topics: ${id}`);
        }
        return [...topics].sort();
      }
      const next = new Set([...seen,id]);
      const children=card.taskGroups.map(group => group.sourceCardId);
      const atlasUnion=[...new Set(children.flatMap(child => bridge.get(child)?.atlasTopicIds ?? []))].sort();
      if (JSON.stringify(atlasUnion)!==JSON.stringify([...binding.atlasTopicIds].sort())) throw new Error(`Composite Atlas union changed: ${id}`);
      return [...new Set(children.flatMap(child => topicsFor(child,next)))].sort();
    };
    for (const id of cards.keys()) {
      if (entries[id]) throw new Error(`Duplicate ${subjectLabel} library binding: ${id}`);
      entries[id]=topicsFor(id);
    }
    papers.push({year:review.year,level:review.level,cards:cards.size});
  }
  return {schemaVersion:1,subjectId,specificationId,
    provenance:'Source-pinned authoring and exact Atlas bridge. Complete routes inherit the union of their separately reviewed constituent canonical topics.',
    papers:papers.sort((a,b) => a.year-b.year || a.level.localeCompare(b.level)),
    cards:Object.fromEntries(Object.entries(entries).sort(([a],[b]) => a.localeCompare(b)))};
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const construction = JSON.stringify(buildConstructionLibraryTopics()) + '\n';
  const constructionOutput = path.join(root, 'data/markBank/construction-studies-library-topics.json');
  if (process.argv.includes('--check')) {
    if (fs.readFileSync(constructionOutput, 'utf8') !== construction) throw new Error('Construction Studies library topic index is stale');
  } else fs.writeFileSync(constructionOutput, construction);
  console.log(`Construction Studies library topic bindings: ${Object.keys(JSON.parse(construction).cards).length}`);
}
