import fs from 'node:fs';
import { execFileSync } from 'node:child_process';
import { describe, expect, it } from 'vitest';
import { loadCards } from '../components/MarkBank/deck';
import { libraryTopicIds } from '../components/MarkBank/libraryGroups';
import { resolveCurriculumSpecification, findCanonicalTopic } from '../curriculumRegistry';
import { topicsForPaper, browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import type { SecCard, SecQuestionCard } from '../types/markBank';
import { CONSTRUCTION_2025_HIGHER_ADDED_IDS, CONSTRUCTION_2025_HIGHER_CORRECTED_IDS } from './fixtures/construction2025Reviewed';

const review = JSON.parse(fs.readFileSync('scripts/markbank/authored/construction-studies-2025-higher-reviewed.json', 'utf8')) as {
  tasks: Array<{correction: boolean; card: Pick<SecQuestionCard, 'id' | 'rows' | 'totalMarks' | 'questionBonus' | 'stem' | 'sourceMaterial'> & {figureKey?: string; questionFigureKey: string}}>;
  bindings: Array<{cardId: string; canonicalTopicIds: string[]; atlasTopicIds: string[]; questionNumber: string}>;
  corrections: Array<{cardId: string; priorSha256: string; correctedSha256: string}>;
};

describe('Construction Studies 2025 Higher source-reviewed Q1–Q10 and alternative Q10', () => {
  it('reconciles original wording, tariffs, every finite route, figures, selection directives and corrections', () => {
    const result = JSON.parse(execFileSync('python3', ['scripts/markbank/authoring/construction_2025_higher.py'], { encoding: 'utf8' }));
    expect(result).toEqual({tasks: 73, addedTasks: 52, correctedTasks: 21, leafTasks: 42, wholeQuestionRoutes: 18,
      q2Routes: 3, q8Routes: 4, q10Routes: 3, sourceFigures: 37, paperComplete: true});
  });

  it('pins every reviewed card identity: the added tasks and routes, and the pre-audit IDs corrected in place', () => {
    expect(review.tasks.filter(t => !t.correction).map(t => t.card.id)).toEqual(CONSTRUCTION_2025_HIGHER_ADDED_IDS);
    expect(review.tasks.filter(t => t.correction).map(t => t.card.id)).toEqual(CONSTRUCTION_2025_HIGHER_CORRECTED_IDS);
    expect(review.corrections.map(c => c.cardId)).toEqual(CONSTRUCTION_2025_HIGHER_CORRECTED_IDS);
    expect(new Set([...CONSTRUCTION_2025_HIGHER_ADDED_IDS, ...CONSTRUCTION_2025_HIGHER_CORRECTED_IDS]).size).toBe(73);
    expect(CONSTRUCTION_2025_HIGHER_ADDED_IDS).toHaveLength(52);
    expect(CONSTRUCTION_2025_HIGHER_CORRECTED_IDS).toHaveLength(21);
    const ids = review.tasks.map(t => t.card.id);
    expect(ids.filter(id => id.startsWith('cons-2025-hl-q2-complete-'))).toHaveLength(3);
    expect(ids.filter(id => id.startsWith('cons-2025-hl-q8-complete-'))).toHaveLength(4);
    expect(ids.filter(id => id.startsWith('cons-2025-hl-q10-complete-'))).toHaveLength(3);
    expect(ids.filter(id => id.startsWith('cons-2025-hl-q10-alt-'))).toHaveLength(3);
  });

  it('keeps all 1,018 previous card IDs in place, corrects 21 under their own IDs and appends only the added tasks', () => {
    const prior = JSON.parse(fs.readFileSync('docs/markbank-audit/2026-09-28/drafts/construction-2025-higher/prior-authored-card-hashes.json', 'utf8')) as {count: number; cards: Record<string, string>};
    const authored: SecCard[] = JSON.parse(fs.readFileSync('scripts/markbank/authored/construction-studies.json', 'utf8'));
    expect(prior.count).toBe(1018);
    // Later consolidations withdraw cards only through a recorded withdrawal; every surviving prior ID keeps its order.
    const withdrawn = new Set(fs.readdirSync('scripts/markbank/authored').filter(n => /^construction-studies-.*-reviewed\.json$/.test(n))
      .flatMap(n => (JSON.parse(fs.readFileSync(`scripts/markbank/authored/${n}`, 'utf8')).withdrawn ?? []).map((w: {cardId: string}) => w.cardId)));
    const live = new Set(authored.map(c => c.id));
    const priorIds = Object.keys(prior.cards).filter(id => live.has(id));
    expect(Object.keys(prior.cards).filter(id => !live.has(id)).every(id => withdrawn.has(id))).toBe(true);
    expect(authored.slice(0, priorIds.length).map(c => c.id)).toEqual(priorIds);
    expect(authored.filter(c => CONSTRUCTION_2025_HIGHER_ADDED_IDS.includes(c.id)).map(c => c.id).sort()).toEqual([...CONSTRUCTION_2025_HIGHER_ADDED_IDS].sort());
    for (const fix of review.corrections) expect(prior.cards[fix.cardId]).toBe(fix.priorSha256);
    expect(new Set(authored.map(c => c.id)).size).toBe(authored.length);
  });

  it('ships all reviewed tasks, their source figures and exact topic bindings', async () => {
    const deck = await loadCards('construction-studies', 'higher');
    const cards = new Map(deck.map(c => [c.id, c]));
    const paper = topicsForPaper('construction-studies', 2025, 'higher', 'ev', 'LC029ALP000EV.pdf');
    const spec = resolveCurriculumSpecification('construction-studies', 2025)!;
    expect(spec.id).toBe('construction-studies:outgoing');
    expect(deck.filter(c => c.year === 2025).map(c => c.id).sort()).toEqual(review.tasks.map(t => t.card.id).sort());
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
      const question = paper!.q.find(q => q.n === binding.questionNumber)!;
      expect(browseTopicIdsForQuestion(paper!, question)).toEqual(expect.arrayContaining(binding.atlasTopicIds));
    }
    for (const n of ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']) expect(paper!.q.filter(q => q.n === n)).toHaveLength(1);
  });
});
