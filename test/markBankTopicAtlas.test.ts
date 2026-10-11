import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { describe, expect, it } from 'vitest';
import { loadCards } from '../components/MarkBank/deck';
import { browseTopicIdsForQuestion, questionsForTopics, topicsForPaper } from '../components/PaperTrail/topics';
import { examTopicDefinition } from '../data/examTopics/registry';
import type { SecCard } from '../types/markBank';
import type { PaperLang } from '../types/paperTrail';

interface AtlasReview {
  subjectId: string;
  year: number;
  level: SecCard['level'];
  lang: PaperLang;
  paperKey: string;
  authoringReview: string;
  sourceHashes: Record<string, string>;
  allocationReview?: string;
  expectedRuntimeCards?: number;
  questions: Array<{ n: string; fileid: string; topicIds: string[] }>;
  cards: Array<{ cardId: string; markBankTopicId: string; questionNumber: string; atlasTopicIds: string[] }>;
  unchangedCards?: AtlasReview['cards'];
}
function cardsInReviewScope(deck: SecCard[], review: AtlasReview) {
  return deck.filter(c => c.year === review.year);
}
const directory = path.resolve('scripts/markbank/atlas-reviews');
const reviews: AtlasReview[] = fs.readdirSync(directory).filter(name => name.endsWith('.json'))
  .map(name => JSON.parse(fs.readFileSync(path.join(directory, name), 'utf8')));

// This suite does not mutate the Atlas corpus. Reuse the actual reverse-query
// result for identical subject/topic pairs, while checking every card's exact
// source identity below (including every constituent topic of finite routes).
const topicQuestionCache = new Map<string, ReturnType<typeof questionsForTopics>>();
function reviewedTopicQuestions(subjectId: string, topicId: string) {
  const key = JSON.stringify([subjectId, topicId]);
  let questions = topicQuestionCache.get(key);
  if (!questions) {
    questions = questionsForTopics(subjectId, [topicId]);
    topicQuestionCache.set(key, questions);
  }
  return questions;
}

function verifyCard(card: SecCard, binding: AtlasReview['cards'][number], review: AtlasReview) {
  expect([card.subjectId, card.year, card.level]).toEqual([review.subjectId, review.year, review.level]);
  expect(card.topicId).toBe(binding.markBankTopicId);
  // Preserve the explicitly reviewed cross-specification topic bridge. A broad
  // unit match cannot choose among immunity, hormones and plant responses.
  expect(card.questionRef.match(/\bQ\s*(\d+)/i)?.[1]).toBe(binding.questionNumber);
  const question = review.questions.find(q => q.n === binding.questionNumber);
  expect(question, `Missing source identity for ${card.id}`).toBeDefined();
  const fileid = card.paperFileid.replace(/\.pdf$/i, '') + '.pdf';
  expect(fileid).toBe(question!.fileid);
  const paper = topicsForPaper(card.subjectId, card.year, card.level, review.lang, fileid);
  const printed = paper?.q.find(q => q.n === binding.questionNumber);
  expect(printed, `${card.id}: missing printed question in Atlas`).toBeDefined();
  expect(binding.atlasTopicIds.length).toBeGreaterThan(0);
  const actualTopics = browseTopicIdsForQuestion(paper!, printed!);
  for (const topicId of binding.atlasTopicIds) {
    expect(examTopicDefinition(topicId)?.level).toBe(card.level);
    expect(question!.topicIds).toContain(topicId);
    expect(actualTopics, `${card.id}: missing Atlas topic ${topicId}`).toContain(topicId);
    expect(reviewedTopicQuestions(card.subjectId, topicId)).toContainEqual({
      subjectId: card.subjectId, year: card.year, level: card.level,
      lang: review.lang, paperKey: review.paperKey, fileid, n: binding.questionNumber,
    });
  }
}

describe('paired Mark Bank / Topic Atlas source reviews', () => {
  it('has an explicit active review rather than passing over an empty directory', () => {
    expect(reviews.length).toBeGreaterThan(0);
  });
  for (const review of reviews) {
    describe(`${review.subjectId} ${review.year} ${review.level}`, () => {
      it('pins original sources and has no duplicate bindings or question identities', () => {
        expect(Object.keys(review.sourceHashes).length).toBeGreaterThan(0);
        for (const [file, hash] of Object.entries(review.sourceHashes)) {
          expect(createHash('sha256').update(fs.readFileSync(file)).digest('hex')).toBe(hash);
        }
        const bindings = [...review.cards, ...(review.unchangedCards ?? [])];
        expect(new Set(bindings.map(c => c.cardId)).size).toBe(bindings.length);
        expect(new Set(review.questions.map(q => q.n)).size).toBe(review.questions.length);
        for (const q of review.questions) {
          const anchor = JSON.parse(fs.readFileSync(`public/paper-anchors/${review.year}/${q.fileid}.json`, 'utf8'));
          expect(anchor.paperOnly).toBe(1);
          expect(anchor.q.some((item: { n: string }) => item.n === q.n)).toBe(true);
        }
      });
      it('keeps every reviewed card reachable under each required Atlas topic', async () => {
        const deck = await loadCards(review.subjectId, review.level);
        const byId = new Map(deck.map(card => [card.id, card]));
        const bindings = [...review.cards, ...(review.unchangedCards ?? [])];
        if (review.expectedRuntimeCards !== undefined) {
          expect(bindings).toHaveLength(review.expectedRuntimeCards);
          expect(bindings.map(b => b.cardId).sort()).toEqual(cardsInReviewScope(deck, review).map(c => c.id).sort());
        }
        if (review.allocationReview) {
          const ledger = JSON.parse(fs.readFileSync(review.allocationReview, 'utf8'));
          expect(bindings).toHaveLength(ledger.expectedRuntimeCards);
          expect(bindings.map(b => b.cardId).sort()).toEqual(cardsInReviewScope(deck, review).map(c => c.id).sort());
        }
        const bindingsById = new Map(bindings.map(binding => [binding.cardId, binding]));
        for (const binding of bindings) {
          const card = byId.get(binding.cardId);
          expect(card, `Reviewed card disappeared: ${binding.cardId}`).toBeDefined();
          verifyCard(card!, binding, review);
          if ('taskGroups' in card! && card.taskGroups) {
            for (const group of card.taskGroups) {
              const child = bindingsById.get(group.sourceCardId!);
              expect(child, `Missing constituent topic bridge: ${group.sourceCardId}`).toBeDefined();
              expect(binding.atlasTopicIds).toEqual(expect.arrayContaining(child!.atlasTopicIds));
            }
          }
        }
      });
      it('rejects a wrong booklet, question number or unrelated topic', async () => {
        const deck = await loadCards(review.subjectId, review.level);
        const binding = review.cards[0];
        const card = deck.find(c => c.id === binding.cardId)!;
        expect(() => verifyCard({ ...card, paperFileid: 'wrong-booklet' }, binding, review)).toThrow();
        expect(() => verifyCard(card, { ...binding, questionNumber: '999' }, review)).toThrow();
        expect(() => verifyCard(card, { ...binding, atlasTopicIds: ['unrelated-topic'] }, review)).toThrow();
      });
    });
  }

});
