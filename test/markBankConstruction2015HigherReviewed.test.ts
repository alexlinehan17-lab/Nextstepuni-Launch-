import fs from 'node:fs';
import { execFileSync } from 'node:child_process';
import { describe, expect, it } from 'vitest';
import { loadCards } from '../components/MarkBank/deck';
import { libraryTopicIds } from '../components/MarkBank/libraryGroups';
import { resolveCurriculumSpecification, findCanonicalTopic } from '../curriculumRegistry';
import { topicsForPaper, browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import type { SecCard, SecQuestionCard } from '../types/markBank';

const review = JSON.parse(fs.readFileSync('scripts/markbank/authored/construction-studies-2015-higher-reviewed.json', 'utf8')) as {
  tasks: Array<{card: Pick<SecQuestionCard, 'id' | 'rows' | 'totalMarks'> & {figureKey?: string; questionFigureKey: string}}>;
  bindings: Array<{cardId: string; canonicalTopicIds: string[]; atlasTopicIds: string[]; questionNumber: string}>;
};

describe('Construction Studies 2015 Higher source-reviewed Q1–Q10', () => {
  it('reconciles original marks, drawing crops, dependencies and selection directives', () => {
    const result = JSON.parse(execFileSync('python3', ['scripts/markbank/authoring/construction_2015_higher_q1_q2.py'], { encoding: 'utf8' }));
    expect(result).toEqual({tasks: 7, sourceFigures: 4, sourceSelectionCandidates: 15, paperComplete: false});
  });
  it('reconciles Q3–Q6 source boundaries, every finite route and original figures', () => {
    const result = JSON.parse(execFileSync('python3', ['scripts/markbank/authoring/construction_2015_higher_q3_q6.py'], { encoding: 'utf8' }));
    expect(result).toEqual({tasks: 56, sourceFigures: 19, wholeQuestionRoutes: 15, paperComplete: false});
  });
  it('reconciles Q7–Q10 routes, the alternative essay and source figures', () => {
    const result = JSON.parse(execFileSync('python3', ['scripts/markbank/authoring/construction_2015_higher_q7_q10.py'], { encoding: 'utf8' }));
    expect(result).toEqual({tasks: 39, sourceFigures: 12, wholeQuestionRoutes: 10, paperComplete: false});
  });
  it('preserves all previous authored cards unchanged, or corrected in place through a recorded later review', () => {
    const prior: SecCard[] = JSON.parse(fs.readFileSync('docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q1-q2/prior-authored-cards.json', 'utf8'));
    const authored: SecCard[] = JSON.parse(fs.readFileSync('scripts/markbank/authored/construction-studies.json', 'utf8'));
    const now = new Map(authored.map(c => [c.id, c]));
    // A later source review may correct a pre-audit card under its own ID; it records the
    // card it replaced (priorCorrectedCards) and the card that replaced it (its task).
    const corrected = new Map<string, {before: SecCard; after: SecCard}>();
    for (const name of fs.readdirSync('scripts/markbank/authored').filter(n => /^construction-studies-.*-reviewed\.json$/.test(n))) {
      const later = JSON.parse(fs.readFileSync(`scripts/markbank/authored/${name}`, 'utf8')) as {priorCorrectedCards?: string; tasks: Array<{correction?: boolean; card: SecCard}>};
      if (!later.priorCorrectedCards) continue;
      const before = new Map((JSON.parse(fs.readFileSync(later.priorCorrectedCards, 'utf8')) as SecCard[]).map(c => [c.id, c]));
      for (const t of later.tasks.filter(task => task.correction)) corrected.set(t.card.id, {before: before.get(t.card.id)!, after: t.card});
    }
    expect(prior).toHaveLength(505);
    for (const card of prior) {
      const fix = corrected.get(card.id);
      if (fix) {
        expect(fix.before).toEqual(card);
        expect(now.get(card.id)).toEqual(fix.after);
      } else expect(now.get(card.id)).toEqual(card);
    }
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
      expect(card.questionFigure?.src).toContain(`${source.questionFigureKey}.png`);
      if (source.figureKey) {
        expect(card.figure?.src).toContain(`${source.figureKey}.png`);
        expect(card.figure?.solution).toBe(true);
      }
      expect(libraryTopicIds(card).sort()).toEqual([...binding.canonicalTopicIds].sort());
      for (const topic of binding.canonicalTopicIds) expect(findCanonicalTopic(spec, topic)?.id).toBe(topic);
      const question = paper!.q.find(q => q.n === binding.questionNumber)!;
      expect(browseTopicIdsForQuestion(paper!, question)).toEqual(expect.arrayContaining(binding.atlasTopicIds));
    }
    for (const n of ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']) expect(paper!.q.filter(q => q.n === n)).toHaveLength(1);
  });
});
