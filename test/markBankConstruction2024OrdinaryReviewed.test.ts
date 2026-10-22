import fs from 'node:fs';
import { execFileSync } from 'node:child_process';
import { describe, expect, it } from 'vitest';
import { hasConstructionSources } from './fixtures/constructionSources';
import { loadCards } from '../components/MarkBank/deck';
import { libraryTopicIds } from '../components/MarkBank/libraryGroups';
import { resolveCurriculumSpecification, findCanonicalTopic } from '../curriculumRegistry';
import { topicsForPaper, browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import type { SecCard, SecQuestionCard } from '../types/markBank';
import { CONSTRUCTION_2024_ORDINARY_ADDED_IDS, CONSTRUCTION_2024_ORDINARY_CORRECTED_IDS } from './fixtures/construction2024Reviewed';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';

const review = JSON.parse(fs.readFileSync('scripts/markbank/authored/construction-studies-2024-ordinary-reviewed.json', 'utf8')) as {
  tasks: Array<{correction: boolean; card: Pick<SecQuestionCard, 'id' | 'rows' | 'totalMarks' | 'questionBonus' | 'stem' | 'sourceMaterial'> & {figureKey?: string; questionFigureKey: string}}>;
  bindings: Array<{cardId: string; canonicalTopicIds: string[]; atlasTopicIds: string[]; questionNumber: string}>;
  corrections: Array<{cardId: string; priorSha256: string; correctedSha256: string}>;
};

describe('Construction Studies 2024 Ordinary source-reviewed Q1–Q9', () => {
  it.skipIf(!hasConstructionSources(2024, 'ordinary'))('reconciles original wording, tariffs, every finite route, figures, selection directives and corrections', () => {
    const result = JSON.parse(execFileSync('python3', ['scripts/markbank/authoring/construction_2024_ordinary.py'], { encoding: 'utf8' }));
    expect(result).toEqual({tasks: 30, addedTasks: 13, correctedTasks: 17, consolidatedLegacy: 8, leafTasks: 22, wholeQuestions: 9,
      q8AnyFiveOfNine: true, sourceFigures: 26, paperComplete: true});
  });

  it('pins every reviewed card identity: the added tasks, the pre-audit IDs corrected in place, and Q8 as one card', () => {
    expect(review.tasks.filter(t => !t.correction).map(t => t.card.id)).toEqual(CONSTRUCTION_2024_ORDINARY_ADDED_IDS);
    expect(review.tasks.filter(t => t.correction).map(t => t.card.id)).toEqual(CONSTRUCTION_2024_ORDINARY_CORRECTED_IDS);
    expect(review.corrections.map(c => c.cardId)).toEqual(CONSTRUCTION_2024_ORDINARY_CORRECTED_IDS);
    expect(new Set([...CONSTRUCTION_2024_ORDINARY_ADDED_IDS, ...CONSTRUCTION_2024_ORDINARY_CORRECTED_IDS]).size).toBe(30);
    expect(CONSTRUCTION_2024_ORDINARY_ADDED_IDS).toHaveLength(13);
    expect(CONSTRUCTION_2024_ORDINARY_CORRECTED_IDS).toHaveLength(17);
    const ids = review.tasks.map(t => t.card.id);
    // Choice is not a route: Q8 is one any-five card, kept under one pre-audit ID; the other eight alias to it.
    expect(ids.filter(id => id.startsWith('cons-2024-ol-q8'))).toEqual(['cons-2024-ol-q8-None-site-planning-notice']);
    const aliased = Object.entries(CARD_ID_ALIASES).filter(([id]) => id.startsWith('cons-2024-ol-q8'));
    expect(aliased).toHaveLength(8);
    for (const [, kept] of aliased) expect(kept).toBe('cons-2024-ol-q8-None-site-planning-notice');
  });

  it('keeps all 733 previous card IDs in place or withdrawn on record, corrects 17 under their own IDs and appends only the added tasks', () => {
    const prior = JSON.parse(fs.readFileSync('docs/markbank-audit/2026-09-28/drafts/construction-2024-ordinary/prior-authored-card-hashes.json', 'utf8')) as {count: number; cards: Record<string, string>};
    const authored: SecCard[] = JSON.parse(fs.readFileSync('scripts/markbank/authored/construction-studies.json', 'utf8'));
    expect(prior.count).toBe(733);
    // Later consolidations withdraw cards only through a recorded withdrawal; every surviving prior ID keeps its order.
    const withdrawn = new Set(fs.readdirSync('scripts/markbank/authored').filter(n => /^construction-studies-.*-reviewed\.json$/.test(n))
      .flatMap(n => (JSON.parse(fs.readFileSync(`scripts/markbank/authored/${n}`, 'utf8')).withdrawn ?? []).map((w: {cardId: string}) => w.cardId)));
    const live = new Set(authored.map(c => c.id));
    const priorIds = Object.keys(prior.cards).filter(id => live.has(id));
    expect(Object.keys(prior.cards).filter(id => !live.has(id)).every(id => withdrawn.has(id))).toBe(true);
    expect(authored.slice(0, priorIds.length).map(c => c.id)).toEqual(priorIds);
    expect(authored.filter(c => CONSTRUCTION_2024_ORDINARY_ADDED_IDS.includes(c.id)).map(c => c.id).sort()).toEqual([...CONSTRUCTION_2024_ORDINARY_ADDED_IDS].sort());
    for (const fix of review.corrections) expect(prior.cards[fix.cardId]).toBe(fix.priorSha256);
    expect(new Set(authored.map(c => c.id)).size).toBe(authored.length);
  });

  it('ships all reviewed tasks, their source figures and exact topic bindings', async () => {
    const deck = await loadCards('construction-studies', 'ordinary');
    const cards = new Map(deck.map(c => [c.id, c]));
    const paper = topicsForPaper('construction-studies', 2024, 'ordinary', 'ev', 'LC029GLP000EV.pdf');
    const spec = resolveCurriculumSpecification('construction-studies', 2024)!;
    expect(spec.id).toBe('construction-studies:outgoing');
    expect(deck.filter(c => c.year === 2024).map(c => c.id).sort()).toEqual(review.tasks.map(t => t.card.id).sort());
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
