import fs from 'node:fs';
import { execFileSync } from 'node:child_process';
import { describe, expect, it } from 'vitest';
import { loadCards } from '../components/MarkBank/deck';
import { libraryTopicIds } from '../components/MarkBank/libraryGroups';
import { resolveCurriculumSpecification, findCanonicalTopic } from '../curriculumRegistry';
import { topicsForPaper, browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import type { SecCard, SecQuestionCard } from '../types/markBank';
import { CONSTRUCTION_2015_HIGHER_REVIEWED_IDS } from './fixtures/construction2015Reviewed';

const review = JSON.parse(fs.readFileSync('scripts/markbank/authored/construction-studies-2015-higher-reviewed.json', 'utf8')) as {
  tasks: Array<{correction: boolean; card: Pick<SecQuestionCard, 'id' | 'rows' | 'totalMarks' | 'stem' | 'sourceMaterial'> & {figureKey?: string; questionFigureKey: string}}>;
  bindings: Array<{cardId: string; canonicalTopicIds: string[]; atlasTopicIds: string[]; questionNumber: string}>;
  corrections: Array<{cardId: string; priorSha256: string; correctedSha256: string}>;
  withdrawn: Array<{cardId: string; priorSha256: string; aliasOf?: string}>;
};

describe('Construction Studies 2015 Higher source-reviewed Q1–Q10 and alternative Q10', () => {
  it('reconciles lifted wording, tariffs, one card per printed choice, figures, selection directives and corrections', () => {
    const result = JSON.parse(execFileSync('python3', ['scripts/markbank/authoring/construction_2015_higher.py'], { encoding: 'utf8' }));
    expect(result).toEqual({tasks: 48, addedTasks: 11, correctedTasks: 37, withdrawnTasks: 65, leafTasks: 33, wholeQuestions: 11,
      anyNChoiceCards: 5, sourceFigures: 25, paperComplete: true});
  });

  it('pins every reviewed card identity: one card per printed choice and one complete card per question', () => {
    const ids = review.tasks.map(t => t.card.id);
    expect(ids).toEqual(CONSTRUCTION_2015_HIGHER_REVIEWED_IDS);
    expect(review.tasks.filter(t => t.correction).map(t => t.card.id)).toEqual(review.corrections.map(c => c.cardId));
    expect(review.corrections).toHaveLength(37);
    // Choice is not a route: the earlier per-item, per-option and per-combination route cards are gone.
    for (const part of ['q3-b', 'q4-a', 'q4-b', 'q6-b', 'q9-a', 'q10-a']) {
      expect(ids.filter(id => id === `cons-2015-hl-${part}` || id.startsWith(`cons-2015-hl-${part}-`))).toEqual([`cons-2015-hl-${part}`]);
    }
    expect(ids.filter(id => id.includes('-complete'))).toHaveLength(11);
    expect(ids.filter(id => id.startsWith('cons-2015-hl-q10-alt-'))).toHaveLength(4);
  });

  it('keeps every other card in place and withdraws the 65 earlier route cards only through recorded, hash-linked withdrawals', () => {
    const prior = JSON.parse(fs.readFileSync('docs/markbank-audit/2026-09-28/drafts/construction-2015-higher/prior-authored-card-hashes.json', 'utf8')) as {count: number; cards: Record<string, string>};
    const authored: SecCard[] = JSON.parse(fs.readFileSync('scripts/markbank/authored/construction-studies.json', 'utf8'));
    expect(prior.count).toBe(764);
    const live = new Set(authored.map(c => c.id));
    const gone = Object.keys(prior.cards).filter(id => !live.has(id));
    expect(gone.filter(id => id.startsWith('cons-2015-hl-'))).toHaveLength(65);
    const withdrawn = new Map(review.withdrawn.map(w => [w.cardId, w]));
    for (const id of gone.filter(id => id.startsWith('cons-2015-hl-'))) {
      expect(withdrawn.get(id)?.priorSha256).toBe(prior.cards[id]);
      expect(withdrawn.get(id)?.aliasOf).toBeUndefined();
    }
    const priorIds = Object.keys(prior.cards).filter(id => live.has(id));
    expect(authored.slice(0, priorIds.length).map(c => c.id)).toEqual(priorIds);
    for (const fix of review.corrections) expect(prior.cards[fix.cardId]).toBe(fix.priorSha256);
    expect(new Set(authored.map(c => c.id)).size).toBe(authored.length);
  });

  it('ships all reviewed tasks, their source figures and exact topic bindings', async () => {
    const deck = await loadCards('construction-studies', 'higher');
    const cards = new Map(deck.map(c => [c.id, c]));
    const paper = topicsForPaper('construction-studies', 2015, 'higher', 'ev', 'LC029ALP000EV.pdf');
    const spec = resolveCurriculumSpecification('construction-studies', 2015)!;
    expect(spec.id).toBe('construction-studies:outgoing');
    expect(deck.filter(c => c.year === 2015).map(c => c.id).sort()).toEqual(review.tasks.map(t => t.card.id).sort());
    for (const {card: source} of review.tasks) {
      const card = cards.get(source.id)!;
      if (card.kind !== 'question') throw new Error(`Expected a question card: ${card.id}`);
      const binding = review.bindings.find(b => b.cardId === card.id)!;
      expect(card.totalMarks).toBe(source.totalMarks);
      expect(card.rows).toEqual(source.rows);
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
      const question = paper!.q.find(q => q.n === binding.questionNumber)!;
      expect(browseTopicIdsForQuestion(paper!, question)).toEqual(expect.arrayContaining(binding.atlasTopicIds));
    }
    for (const n of ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']) expect(paper!.q.filter(q => q.n === n)).toHaveLength(1);
  });
});
