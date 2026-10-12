import fs from 'node:fs';
import { execFileSync } from 'node:child_process';
import { describe, expect, it } from 'vitest';
import { loadCards } from '../components/MarkBank/deck';
import { libraryTopicIds } from '../components/MarkBank/libraryGroups';
import { resolveCurriculumSpecification, findCanonicalTopic } from '../curriculumRegistry';
import { topicsForPaper, browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import type { SecCard, SecQuestionCard } from '../types/markBank';
import { CONSTRUCTION_2025_ORDINARY_ADDED_IDS, CONSTRUCTION_2025_ORDINARY_CORRECTED_IDS } from './fixtures/construction2025Reviewed';

const review = JSON.parse(fs.readFileSync('scripts/markbank/authored/construction-studies-2025-ordinary-reviewed.json', 'utf8')) as {
  tasks: Array<{correction: boolean; card: Pick<SecQuestionCard, 'id' | 'rows' | 'totalMarks' | 'questionBonus' | 'stem' | 'sourceMaterial'> & {figureKey?: string; questionFigureKey: string}}>;
  bindings: Array<{cardId: string; canonicalTopicIds: string[]; atlasTopicIds: string[]; questionNumber: string}>;
  corrections: Array<{cardId: string; priorSha256: string; correctedSha256: string}>;
};

describe('Construction Studies 2025 Ordinary source-reviewed Q1–Q9', () => {
  it('reconciles original wording, tariffs, every finite route, figures, selection directives and corrections', () => {
    const result = JSON.parse(execFileSync('python3', ['scripts/markbank/authoring/construction_2025_ordinary.py'], { encoding: 'utf8' }));
    expect(result).toEqual({tasks: 35, addedTasks: 14, correctedTasks: 21, leafTasks: 25, wholeQuestions: 9,
      q8AnyFiveOfNine: true, sourceFigures: 25, paperComplete: true});
  });

  it('pins every reviewed card identity: the added tasks, and the pre-audit IDs corrected in place', () => {
    expect(review.tasks.filter(t => !t.correction).map(t => t.card.id)).toEqual(CONSTRUCTION_2025_ORDINARY_ADDED_IDS);
    expect(review.tasks.filter(t => t.correction).map(t => t.card.id)).toEqual(CONSTRUCTION_2025_ORDINARY_CORRECTED_IDS);
    expect(review.corrections.map(c => c.cardId)).toEqual(CONSTRUCTION_2025_ORDINARY_CORRECTED_IDS);
    expect(new Set([...CONSTRUCTION_2025_ORDINARY_ADDED_IDS, ...CONSTRUCTION_2025_ORDINARY_CORRECTED_IDS]).size).toBe(35);
    expect(CONSTRUCTION_2025_ORDINARY_ADDED_IDS).toHaveLength(14);
    expect(CONSTRUCTION_2025_ORDINARY_CORRECTED_IDS).toHaveLength(21);
    const ids = review.tasks.map(t => t.card.id);
    // Choice is not a route: Q8 is one any-five card over all nine printed terms.
    expect(ids.filter(id => id.startsWith('cons-2025-ol-q8'))).toEqual(['cons-2025-ol-q8']);
    expect(ids.filter(id => id.startsWith('cons-2025-ol-q6-a-'))).toHaveLength(3);
  });

  it('keeps all 1,070 previous card IDs in place, corrects 21 under their own IDs and appends only the added tasks', () => {
    const prior = JSON.parse(fs.readFileSync('docs/markbank-audit/2026-09-28/drafts/construction-2025-ordinary/prior-authored-card-hashes.json', 'utf8')) as {count: number; cards: Record<string, string>};
    const authored: SecCard[] = JSON.parse(fs.readFileSync('scripts/markbank/authored/construction-studies.json', 'utf8'));
    expect(prior.count).toBe(1070);
    expect(authored.slice(0, 1070).map(c => c.id)).toEqual(Object.keys(prior.cards));
    expect(authored.slice(1070, 1070 + CONSTRUCTION_2025_ORDINARY_ADDED_IDS.length).map(c => c.id)).toEqual(CONSTRUCTION_2025_ORDINARY_ADDED_IDS);
    for (const fix of review.corrections) expect(prior.cards[fix.cardId]).toBe(fix.priorSha256);
    expect(new Set(authored.map(c => c.id)).size).toBe(authored.length);
  });

  it('ships all reviewed tasks, their source figures and exact topic bindings', async () => {
    const deck = await loadCards('construction-studies', 'ordinary');
    const cards = new Map(deck.map(c => [c.id, c]));
    const paper = topicsForPaper('construction-studies', 2025, 'ordinary', 'ev', 'LC029GLP000EV.pdf');
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
    for (const n of ['1', '2', '3', '4', '5', '6', '7', '8', '9']) expect(paper!.q.filter(q => q.n === n)).toHaveLength(1);
  });
});
