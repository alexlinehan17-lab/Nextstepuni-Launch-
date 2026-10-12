import fs from 'node:fs';
import { execFileSync } from 'node:child_process';
import { describe, expect, it } from 'vitest';
import { loadCards } from '../components/MarkBank/deck';
import { libraryTopicIds } from '../components/MarkBank/libraryGroups';
import { resolveCurriculumSpecification, findCanonicalTopic } from '../curriculumRegistry';
import { topicsForPaper, browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import type { SecCard, SecQuestionCard } from '../types/markBank';
import { CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS } from './fixtures/construction2026Reviewed';

const review = JSON.parse(fs.readFileSync('scripts/markbank/authored/construction-studies-2026-ordinary-reviewed.json', 'utf8')) as {
  tasks: Array<{card: Pick<SecQuestionCard, 'id' | 'rows' | 'totalMarks' | 'questionBonus'> & {figureKey?: string; questionFigureKey: string}}>;
  bindings: Array<{cardId: string; canonicalTopicIds: string[]; atlasTopicIds: string[]; questionNumber: string}>;
};

describe('Construction Studies 2026 Ordinary source-reviewed Q1–Q9', () => {
  it('reconciles original wording, tariffs, every finite route, figures and selection directives', () => {
    const result = JSON.parse(execFileSync('python3', ['scripts/markbank/authoring/construction_2026_ordinary.py'], { encoding: 'utf8' }));
    expect(result).toEqual({tasks: 32, leafTasks: 23, wholeQuestions: 9, q8AnyFiveOfNine: true, sourceFigures: 25, paperComplete: true});
  });

  it('pins every reviewed card identity; the Q8 choice is one any-five card, not a route per combination', () => {
    expect(review.tasks.map(t => t.card.id)).toEqual(CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS);
    expect(new Set(CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS).size).toBe(32);
    expect(CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS.filter(id => id.startsWith('cons-2026-ol-q8'))).toEqual(['cons-2026-ol-q8']);
  });

  it('keeps all 852 previous authored card positions and adds only the reviewed tasks', () => {
    const prior = JSON.parse(fs.readFileSync('docs/markbank-audit/2026-09-28/drafts/construction-2026-ordinary/prior-authored-card-hashes.json', 'utf8')) as {count: number; cards: Record<string, string>};
    const authored: SecCard[] = JSON.parse(fs.readFileSync('scripts/markbank/authored/construction-studies.json', 'utf8'));
    expect(prior.count).toBe(852);
    // Later consolidations withdraw cards only through a recorded withdrawal; every surviving prior ID keeps its order.
    const withdrawn = new Set(fs.readdirSync('scripts/markbank/authored').filter(n => /^construction-studies-.*-reviewed\.json$/.test(n))
      .flatMap(n => (JSON.parse(fs.readFileSync(`scripts/markbank/authored/${n}`, 'utf8')).withdrawn ?? []).map((w: {cardId: string}) => w.cardId)));
    const live = new Set(authored.map(c => c.id));
    const priorIds = Object.keys(prior.cards).filter(id => live.has(id));
    expect(Object.keys(prior.cards).filter(id => !live.has(id)).every(id => withdrawn.has(id))).toBe(true);
    expect(authored.slice(0, priorIds.length).map(c => c.id)).toEqual(priorIds);
    expect(authored.filter(c => CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS.includes(c.id)).map(c => c.id).sort()).toEqual([...CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS].sort());
    expect(new Set(authored.map(c => c.id)).size).toBe(authored.length);
  });

  it('ships all reviewed tasks, their source figures and exact topic bindings', async () => {
    const deck = await loadCards('construction-studies', 'ordinary');
    const cards = new Map(deck.map(c => [c.id, c]));
    const paper = topicsForPaper('construction-studies', 2026, 'ordinary', 'ev', 'LC029GLP000EV.pdf');
    const spec = resolveCurriculumSpecification('construction-studies', 2026)!;
    expect(spec.id).toBe('construction-studies:outgoing');
    expect(deck.filter(c => c.year === 2026).map(c => c.id).sort()).toEqual(review.tasks.map(t => t.card.id).sort());
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
