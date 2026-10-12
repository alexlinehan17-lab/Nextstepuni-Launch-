import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { CARDS as ALL_CARDS } from '../components/MarkBank/cards/irish/foundation';
import authored from '../components/MarkBank/cards/irish/foundation-authored.json';
import { builtDecks, cardsForTopic, loadCards } from '../components/MarkBank/deck';
import { levelsForSubject } from '../components/MarkBank/levels';
import { readChoice, writeChoice } from '../components/MarkBank/store';
import { combinedListeningAssessment, irishMarks, irishScoreId, listeningQuestionGroups } from '../components/MarkBank/SessionScreen';
import { examTopicIdsForQuestion, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { resolveCurriculumSpecification } from '../curriculumRegistry';
import { tariffReconciles } from '../types/markBank';

const CARDS = ALL_CARDS.filter(c => c.year === 2025);

describe('reviewed 2025 Irish Foundation tasks', () => {
  it('loads and remembers Foundation without changing other subjects’ available levels', async () => {
    expect(await loadCards('irish', 'foundation')).toHaveLength(1003);
    expect(builtDecks()).toContainEqual({ subjectId: 'irish', level: 'foundation', label: 'Irish Foundation' });
    expect(levelsForSubject('irish', 2025)).toEqual(['higher', 'ordinary', 'foundation']);
    expect(levelsForSubject('biology', 2025)).toEqual(['higher', 'ordinary']);
    writeChoice('foundation-review', { subjectId: 'irish', level: 'foundation' });
    expect(readChoice('foundation-review')).toEqual({ subjectId: 'irish', level: 'foundation' });
  });

  it('keeps every reviewed task at its published boundary and on the canonical curriculum', () => {
    expect(CARDS).toHaveLength(60);
    expect(new Set(CARDS.map(c => c.id)).size).toBe(60);
    for (const card of CARDS) {
      expect(tariffReconciles(card), card.id).toBe(true);
      expect(card.specVersion).toBe(resolveCurriculumSpecification('irish', 2025)!.id);
      expect(card.sourceMaterial?.pages.length, card.id).toBeGreaterThan(0);
      expect(card.schemeRegion?.schemeFileid).toBe('LC001BLP000IV.pdf');
    }
    expect(CARDS.filter(c => /-r-1-\d+$/.test(c.id))).toHaveLength(10);
    expect(CARDS.filter(c => /-r-[23][abc]-\d+$/.test(c.id))).toHaveLength(30);
    expect(CARDS.filter(c => /-r-2[abc]-\d+$/.test(c.id)).every(c => c.totalMarks === 5)).toBe(true);
    expect(CARDS.filter(c => /-r-3[abc]-\d+$/.test(c.id)).every(c => c.totalMarks === 6)).toBe(true);
  });

  it('publishes each passage part and writing option once, carrying the printed choose-two instruction', () => {
    // Choice is not a route: no per-combination cards for “dhá cheann de (a), (b), (c)” or “dhá cheist ar bith”.
    expect(CARDS.filter(c => /-r-[23]-[abc]{2}$|-w-[45][ab]-[45][ab]/.test(c.id))).toEqual([]);
    for (const question of [2, 3]) {
      const parts = CARDS.filter(c => new RegExp(`-r-${question}[abc]-\\d+$`).test(c.id));
      expect(parts).toHaveLength(15);
      for (const part of parts) {
        if (part.rubric.system !== 'irish') throw new Error('Wrong rubric');
        expect(part.rubric.taskRequirements[0], part.id).toBe(`Ceist ${question} Freagair do rogha dhá cheann de (a), (b), (c) anseo thíos.`);
      }
    }
    const forms = CARDS.filter(c => /-w-4b-(16|5|10)-/.test(c.id));
    expect(forms).toHaveLength(3);
    expect(forms.map(c => c.questionText.split('An rogha don chárta seo: ')[1]))
      .toEqual(['16 Aibreán.', '5 Bealtaine.', '10 Meitheamh.']);
    for (const form of forms) {
      expect(form.totalMarks).toBe(45);
      expect(form.questionText).toContain('Nuala Seoighe');
      expect(form.questionText).toContain('timpeall 40 focal');
      expect(form.sourceMaterial?.pages).toEqual([15]);
    }
    const writing = CARDS.filter(c => /-w-[45][ab](-|$)/.test(c.id));
    expect(writing).toHaveLength(6);
    for (const option of writing) {
      if (option.rubric.system !== 'irish') throw new Error('Wrong rubric');
      expect(option.rubric.taskRequirements[0], option.id).toBe('Freagair dhá cheist ar bith as na ceithre cinn seo a leanas: 4 (a), 4 (b), 5 (a) nó 5 (b).');
    }
    expect(cardsForTopic('irish-9-0', CARDS)).toContain(forms[0]);
  });

  it('never lets a short story deduct marks from its language award', () => {
    const card = CARDS.find(c => c.id === 'irish-2025-fl-w-5a')!;
    if (card.rubric.system !== 'irish') throw new Error('Wrong rubric');
    const scores = Object.fromEntries(card.rubric.criteria.map(c => [irishScoreId(c.id), c.kind === 'award' ? c.maxMarks : 0]));
    expect(irishMarks(card, scores)).toBe(45);
    scores['irish:cumarsaid'] = 0;
    scores['irish:length'] = 4;
    expect(irishMarks(card, scores)).toBe(11); // the length deduction reduces communication only; 11 language marks stay.
  });

  it('keeps all listening pictures and choices with the official Foundation recording', () => {
    const listening = CARDS.filter(c => Boolean(c.audioMaterial)) as Parameters<typeof combinedListeningAssessment>[0];
    expect(listening).toHaveLength(14);
    const combined = combinedListeningAssessment(listening);
    expect(combined.totalMarks).toBe(120);
    expect(combined.sourceMaterial?.pages).toEqual([3, 4, 5]);
    expect(combined.audioMaterial.secFileid).toBe('LC001BLP017IV.mp3');
    const prompts = listening.flatMap(c => listeningQuestionGroups(c.questionText).flatMap(g => g.prompts));
    expect(prompts).toHaveLength(14);
    expect(prompts.find(p => p.label === '7(a)')?.text).toContain('55%\n70%\n80%');
    expect(combined.questionText).not.toContain('Tá tarracóir mór nua againn');
  });

  it('joins every card to a correctly tagged Atlas entry with all source and scheme pages', () => {
    const map = JSON.parse(readFileSync('public/paper-answers/2025/LC001BLP000IV.pdf.json', 'utf8'));
    expect(map.paperOnly).toBeUndefined();
    for (const card of authored.cards) {
      const ids = examTopicIdsForQuestion('irish', 'foundation', 2025, 'main', card.atlasQuestionId, 'single', 'iv', 'LC001BLP000IV.pdf');
      expect(ids.length, card.id).toBeGreaterThan(0);
      const canonical = ids.flatMap(curriculumNodeIdsForExamTopic);
      expect(canonical, card.id).toContain(card.topicId);
      const anchor = map.q.find((q: { n: string }) => q.n === card.atlasQuestionId);
      expect(anchor.paperRegion.map((r: { p: number }) => r.p), card.id).toEqual(card.sourceMaterial.pages);
      expect(anchor.region.map((r: { p: number }) => r.p), card.id).toEqual(card.schemePages);
      if ('audioMaterial' in card) expect(anchor.audioMaterial).toEqual(card.audioMaterial);
    }
    expect(examTopicIdsForQuestion('irish', 'foundation', 2025, 'main', 'W-4B', 'single', 'iv', 'LC001BLP000IV.pdf'))
      .toEqual(['irish-foundation-fill-in-a-form']);
    expect(examTopicIdsForQuestion('irish', 'foundation', 2025, 'main', 'R-2C', 'single', 'iv', 'LC001BLP000IV.pdf'))
      .toEqual(['irish-foundation-reading-extract']);
  });
});
