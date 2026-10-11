import fs from 'node:fs';
import { execFileSync } from 'node:child_process';
import { describe, expect, it } from 'vitest';
import { loadCards } from '../components/MarkBank/deck';
import { libraryTopicIds } from '../components/MarkBank/libraryGroups';
import { resolveCurriculumSpecification, findCanonicalTopic } from '../curriculumRegistry';
import { topicsForPaper, browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import type { SecCard, SecQuestionCard } from '../types/markBank';
import { CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS } from './fixtures/construction2015Reviewed';

const review = JSON.parse(fs.readFileSync('scripts/markbank/authored/construction-studies-2015-ordinary-reviewed.json', 'utf8')) as {
  tasks: Array<{card: Pick<SecQuestionCard, 'id' | 'rows' | 'totalMarks' | 'questionBonus'> & {figureKey?: string; questionFigureKey: string}}>;
  bindings: Array<{cardId: string; canonicalTopicIds: string[]; atlasTopicIds: string[]; questionNumber: string}>;
};

describe('Construction Studies 2015 Ordinary source-reviewed Q1–Q9', () => {
  it('reconciles original wording, tariffs, every finite route, figures and selection directives', () => {
    const result = JSON.parse(execFileSync('python3', ['scripts/markbank/authoring/construction_2015_ordinary.py'], { encoding: 'utf8' }));
    expect(result).toEqual({tasks: 176, leafTasks: 37, wholeQuestionRoutes: 134, q8Routes: 126, sourceFigures: 35, sharedDrawingAllowances: 2, paperComplete: true});
  });

  it('pins every reviewed card identity, including all 126 choose-five Q8 routes', () => {
    expect(review.tasks.map(t => t.card.id)).toEqual(CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS);
    expect(new Set(CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS).size).toBe(176);
    expect(CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS.filter(id => id.startsWith('cons-2015-ol-q8-complete-'))).toHaveLength(126);
  });

  it('keeps all 607 previous authored cards and adds only the reviewed tasks', () => {
    const prior = JSON.parse(fs.readFileSync('docs/markbank-audit/2026-09-28/drafts/construction-2015-ordinary-q1-q9/prior-authored-card-hashes.json', 'utf8')) as {count: number; cards: Record<string, string>};
    const authored: SecCard[] = JSON.parse(fs.readFileSync('scripts/markbank/authored/construction-studies.json', 'utf8'));
    expect(prior.count).toBe(607);
    expect(authored.slice(0, 607).map(c => c.id)).toEqual(Object.keys(prior.cards));
    expect(authored.slice(607, 607 + CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS.length).map(c => c.id)).toEqual(CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS);
    expect(new Set(authored.map(c => c.id)).size).toBe(authored.length);
  });

  it('ships all reviewed tasks, their source figures and exact topic bindings', async () => {
    const deck = await loadCards('construction-studies', 'ordinary');
    const cards = new Map(deck.map(c => [c.id, c]));
    const paper = topicsForPaper('construction-studies', 2015, 'ordinary', 'ev', 'LC029GLP000EV.pdf');
    const spec = resolveCurriculumSpecification('construction-studies', 2015)!;
    expect(spec.id).toBe('construction-studies:outgoing');
    expect(deck.filter(c => c.year === 2015).map(c => c.id).sort()).toEqual(review.tasks.map(t => t.card.id).sort());
    for (const {card: source} of review.tasks) {
      const card = cards.get(source.id)!;
      if (card.kind !== 'question') throw new Error(`Expected a question card: ${card.id}`);
      const binding = review.bindings.find(b => b.cardId === card.id)!;
      expect(card.totalMarks).toBe(source.totalMarks);
      expect(card.rows).toEqual(source.rows);
      expect(card.questionBonus).toEqual(source.questionBonus);
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
