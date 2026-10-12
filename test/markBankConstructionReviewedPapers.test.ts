/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import fs from 'node:fs';
import { execFileSync } from 'node:child_process';
import { describe, expect, it } from 'vitest';
import { loadCards } from '../components/MarkBank/deck';
import { libraryTopicIds } from '../components/MarkBank/libraryGroups';
import { resolveCurriculumSpecification, findCanonicalTopic } from '../curriculumRegistry';
import { topicsForPaper, browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import type { SecCard, SecQuestionCard } from '../types/markBank';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import { CONSTRUCTION_REVIEWED_PAPERS } from './fixtures/constructionReviewedPapers';

const FILEID = { higher: 'LC029ALP000EV.pdf', ordinary: 'LC029GLP000EV.pdf' } as const;

describe('Construction Studies papers reviewed on the shared engine', () => {
  it('lists the reviewed papers', () => {
    expect(CONSTRUCTION_REVIEWED_PAPERS.length).toBeGreaterThan(0);
  });
});

for (const paper of CONSTRUCTION_REVIEWED_PAPERS) {
  const name = `${paper.year} ${paper.level}`;
  const review = JSON.parse(fs.readFileSync(`scripts/markbank/authored/construction-studies-${paper.year}-${paper.level}-reviewed.json`, 'utf8')) as {
    tasks: Array<{correction: boolean; card: Pick<SecQuestionCard, 'id' | 'rows' | 'totalMarks' | 'questionBonus' | 'stem' | 'sourceMaterial'> & {figureKey?: string; questionFigureKey: string}}>;
    bindings: Array<{cardId: string; canonicalTopicIds: string[]; atlasTopicIds: string[]; questionNumber: string}>;
    corrections: Array<{cardId: string; priorSha256: string}>;
    withdrawn?: Array<{cardId: string; aliasOf: string}>;
  };

  describe(`Construction Studies ${name} source-reviewed theory`, () => {
    it('reconciles original wording, tariffs, routes, figures, selection directives and corrections', () => {
      const result = JSON.parse(execFileSync('python3', [paper.validator], { encoding: 'utf8' }));
      expect(result).toEqual(paper.result);
    });

    it('pins every reviewed card identity, one card per printed choice and the progress aliases of withdrawn cards', () => {
      expect(review.tasks.filter(t => !t.correction).map(t => t.card.id)).toEqual(paper.addedIds);
      expect(review.tasks.filter(t => t.correction).map(t => t.card.id)).toEqual(paper.correctedIds);
      expect(review.corrections.map(c => c.cardId)).toEqual(paper.correctedIds);
      const ids = review.tasks.map(t => t.card.id);
      for (const id of paper.choiceCardIds) expect(ids.filter(x => x === id || x.startsWith(`${id}-`))).toEqual([id]);
      expect((review.withdrawn ?? []).map(w => w.cardId)).toEqual(paper.withdrawnIds);
      for (const w of review.withdrawn ?? []) {
        expect(CARD_ID_ALIASES[w.cardId]).toBe(w.aliasOf);
        expect(ids).toContain(w.aliasOf);
      }
    });

    it('keeps every earlier card ID in place or withdrawn on record and appends only the added tasks', () => {
      const prior = JSON.parse(fs.readFileSync(`docs/markbank-audit/2026-09-28/drafts/construction-${paper.year}-${paper.level}/prior-authored-card-hashes.json`, 'utf8')) as {count: number; cards: Record<string, string>};
      const authored: SecCard[] = JSON.parse(fs.readFileSync('scripts/markbank/authored/construction-studies.json', 'utf8'));
      expect(prior.count).toBe(paper.priorCount);
      const withdrawn = new Set(fs.readdirSync('scripts/markbank/authored').filter(n => /^construction-studies-.*-reviewed\.json$/.test(n))
        .flatMap(n => (JSON.parse(fs.readFileSync(`scripts/markbank/authored/${n}`, 'utf8')).withdrawn ?? []).map((w: {cardId: string}) => w.cardId)));
      const live = new Set(authored.map(c => c.id));
      const priorIds = Object.keys(prior.cards).filter(id => live.has(id));
      expect(Object.keys(prior.cards).filter(id => !live.has(id)).every(id => withdrawn.has(id))).toBe(true);
      expect(authored.slice(0, priorIds.length).map(c => c.id)).toEqual(priorIds);
      expect(authored.filter(c => paper.addedIds.includes(c.id)).map(c => c.id).sort()).toEqual([...paper.addedIds].sort());
      for (const fix of review.corrections) expect(prior.cards[fix.cardId]).toBe(fix.priorSha256);
      expect(new Set(authored.map(c => c.id)).size).toBe(authored.length);
    });

    it('ships all reviewed tasks, their source figures and exact topic bindings', async () => {
      const deck = await loadCards('construction-studies', paper.level);
      const cards = new Map(deck.map(c => [c.id, c]));
      const atlas = topicsForPaper('construction-studies', paper.year, paper.level, 'ev', FILEID[paper.level]);
      const spec = resolveCurriculumSpecification('construction-studies', paper.year)!;
      expect(spec.id).toBe('construction-studies:outgoing');
      expect(deck.filter(c => c.year === paper.year).map(c => c.id).sort()).toEqual(review.tasks.map(t => t.card.id).sort());
      for (const {card: source} of review.tasks) {
        const card = cards.get(source.id)!;
        if (card.kind !== 'question') throw new Error(`Expected a question card: ${card.id}`);
        const binding = review.bindings.find(b => b.cardId === card.id)!;
        expect(card.totalMarks).toBe(source.totalMarks);
        expect(card.rows).toEqual(source.rows);
        expect(card.questionBonus).toEqual(source.questionBonus);
        expect(card.stem).toBe(source.stem || undefined);
        expect(card.sourceMaterial?.label).toBe(source.sourceMaterial?.label);
        expect(card.questionFigure?.src).toContain(`${source.questionFigureKey}.png`);
        if (source.figureKey) {
          expect(card.figure?.src).toContain(`${source.figureKey}.png`);
          expect(card.figure?.solution).toBe(true);
        } else {
          expect(card.figure).toBeUndefined();
        }
        expect(libraryTopicIds(card).sort()).toEqual([...binding.canonicalTopicIds].sort());
        for (const topic of binding.canonicalTopicIds) expect(findCanonicalTopic(spec, topic)?.id).toBe(topic);
        const question = atlas!.q.find(q => q.n === binding.questionNumber)!;
        expect(browseTopicIdsForQuestion(atlas!, question)).toEqual(expect.arrayContaining(binding.atlasTopicIds));
      }
      const questions = paper.level === 'higher' ? 10 : 9;
      for (let n = 1; n <= questions; n += 1) expect(atlas!.q.filter(q => q.n === String(n))).toHaveLength(1);
    });
  });
}
