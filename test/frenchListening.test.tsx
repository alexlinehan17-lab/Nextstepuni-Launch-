import { fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import fs from 'node:fs';
import { FRENCH_LISTENING_CARDS as cards } from '../components/MarkBank/cards/french/listening';
import SessionScreen from '../components/MarkBank/SessionScreen';
import VaultQuestionCard from '../components/PaperTrail/VaultQuestionCard';
import { frenchAudioForPaper } from '../components/PaperTrail/frenchAudio';
import { listeningExerciseKey, visibleSessionExercises, resolveSessionQueue } from '../components/MarkBank/sessionPlanning';
import { tariffReconciles } from '../types/markBank';
import { topicsForPaper, browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { paperRegionFor } from '../components/PaperTrail/paperRegion';
import tasks from '../data/examTopics/french-reviewed-tasks.json';
import audio from '../data/frenchAudio.json';

vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));
const byId = (suffix: string, year = 2026) => cards.find(card => card.id === `fr-${year}-${suffix}`)!;
afterEach(() => vi.unstubAllGlobals());

describe('reviewed French listening tasks', () => {
  it('preserves every priced boundary and the published section totals', () => {
    expect(cards).toHaveLength(715);
    for (const year of [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]) for (const [level, expected] of [['higher', [12, 21, 18, 21, 8]], ['ordinary', [20, 20, 20, 20, 20]]] as const) {
      const group = cards.filter(card => card.level === level && card.year === year);
      expect(group).toHaveLength(level === 'higher' ? (year === 2010 ? 24 : [2011, 2012, 2013, 2014, 2015].includes(year) ? 23 : year === 2022 ? 20 : [2019, 2020, 2023, 2025].includes(year) ? 21 : 22) : 20);
      expect(['LA', 'LB', 'LC', 'LD', 'LE'].map(section => group.filter(card => card.section === section).reduce((sum, card) => sum + card.totalMarks, 0)))
        .toEqual(year === 2010 ? (level === 'higher' ? [16, 18, 17, 21, 8] : [20, 20, 16, 24, 20]) : level === 'higher' && year === 2015 ? [16, 21, 18, 21, 4] : level === 'higher' && year === 2012 ? [12, 18, 21, 21, 8] : expected);
    }
    expect(cards.filter(card => card.questionChoices)).toHaveLength(204);
    for (const card of cards) {
      expect(tariffReconciles(card), card.id).toBe(true);
      expect(card.stem, card.id).toBeTruthy();
      expect(card.audioMaterial.playbackUrl).toBe(audio.find(recording => recording.year === card.year)!.source.playbackUrl);
      expect(card.audioMaterial.secFileid).toBe(card.year === 2012 ? 'LC010ZLPO17EV.mp3' : card.year <= 2021 ? 'LC010ZLP017EV.mp3' : card.year === 2022 ? 'LC010CLP017BV.mp3' : 'LC010CLP017EV.mp3');
      if (card.questionChoices) {
        expect(card.questionChoices).toHaveLength(4);
        expect(card.rubric.criteria[0].permittedMarks).toEqual([0, card.totalMarks]);
      }
    }
  });
  it('applies the 2025 higher-segment rule only to its three named tasks', () => {
    const special = cards.filter(card => card.year === 2025 && card.rubric.taskRequirements.some(rule => rule.startsWith('Special rule')));
    expect(special.map(card => card.id)).toEqual([
      'fr-2025-hl-listening-la-q2', 'fr-2025-hl-listening-lc-q2', 'fr-2025-hl-listening-ld-q1',
    ]);
    expect(special.map(card => card.rubric.criteria[0].permittedMarks)).toEqual([[0, 6], [0, 2, 4, 6], [0, 2, 4, 6]]);
    for (const card of special) {
      expect(card.rubric.taskRequirements).toContain('Give 2 distinct details. Do not count the same information twice.');
      expect(card.rubric.taskRequirements.join(' ')).toContain('including when the other detail earns 0');
      expect(card.schemeCitation).toContain('general rules p.17');
    }
    expect(byId('hl-listening-ld-q3', 2025).rubric.criteria[0].permittedMarks).toEqual([0, 2, 3, 5, 6]);
    expect(byId('hl-listening-le-q2', 2025).rubric.criteria[0].permittedMarks).toEqual([0, 1, 2, 3, 4]);
    expect(byId('hl-listening-le-q3', 2025).rubric.answerGuide).toContain('Wrong person = -1 Mark');
    for (const suffix of ['ol-listening-la-q2b', 'ol-listening-ld-q1']) {
      const card = byId(suffix, 2025);
      expect(card.rubric.criteria[0].permittedMarks).toEqual([0, 3, 5]);
      expect(card.rubric.answerGuide).toContain('Any two of the following, award 5 Marks');
      expect(card.schemeCitation).toContain('general rules p.18');
    }
  });
  it('retains the 2024 split tariffs, weekday ladder and year-specific rules', () => {
    const meal = cards.filter(card => card.id.startsWith('fr-2024-hl-listening-lc-q2-'));
    expect(meal.map(card => [card.id, card.totalMarks])).toEqual([
      ['fr-2024-hl-listening-lc-q2-main-course', 3], ['fr-2024-hl-listening-lc-q2-dessert', 3],
    ]);
    expect(meal[0].questionText).toContain('Answer for: Main course.');
    expect(meal[1].questionText).toContain('Answer for: Dessert.');
    expect(meal[0].rubric.answerGuide).toEqual(['(Roast) duck (with honey) — 3 Marks']);
    expect(meal[1].rubric.answerGuide).toEqual(['(Exotic) fruit (salad) — 3 Marks']);
    expect(byId('hl-listening-la-q2', 2024).rubric.criteria[0].permittedMarks).toEqual([0, 1, 2, 3]);
    expect(byId('hl-listening-la-q2', 2024).rubric.answerGuide).toContain('One correct day plus one incorrect day = 1 Mark');
    expect(byId('hl-listening-lc-q1b', 2024).stem).toContain('Florence; the evening is Saturday evening');
    const special = cards.filter(card => card.year === 2024 && card.rubric.taskRequirements.some(rule => rule.startsWith('Special rule')));
    expect(special.map(card => [card.id, card.rubric.criteria[0].permittedMarks])).toEqual([
      ['fr-2024-hl-listening-la-q3', [0, 4, 6]], ['fr-2024-hl-listening-lb-q3', [0, 6]], ['fr-2024-hl-listening-ld-q1', [0, 2, 4, 6]],
    ]);
    expect(byId('ol-listening-ld-q1', 2024).rubric.taskRequirements.join(' ')).toContain('whole test or whole section');
    expect(byId('ol-listening-ld-q1', 2025).rubric.taskRequirements.join(' ')).not.toContain('whole section');
  });
  it('retains the complete partial-credit and required-detail rules', () => {
    expect(byId('hl-listening-la-q2').rubric.criteria[0].permittedMarks).toEqual([0, 2, 3, 5, 6]);
    expect(byId('hl-listening-ld-q2').rubric.criteria[0].permittedMarks).toEqual([0, 3, 6]);
    expect(byId('hl-listening-lb-q3b').rubric.answerGuide).toHaveLength(7);
    expect(byId('hl-listening-ld-q4a').rubric.answerGuide).toContain('Incorrect year = -1 Mark');
    expect(byId('ol-listening-la-q2b').rubric.answerGuide).toContain('Wrong verb + correct person — 3 Marks');
    expect(byId('ol-listening-le-q2a').rubric.criteria[0].permittedMarks).toEqual([0, 1, 5]);
    expect(byId('ol-listening-le-q2b').rubric.answerGuide).toEqual(['Gold — 5 Marks']);
    expect(byId('ol-listening-ld-q1').rubric.criteria[0].permittedMarks).toEqual([0, 3, 5]);
    expect(byId('ol-listening-lc-q1').questionText).toContain('school?');
    expect(byId('hl-listening-lb-q4b').stem).toContain('street food Marcelle ate in Turkey');
  });
  it('preserves the six 2023 higher-segment tasks and 25% aggregate penalty', () => {
    const special = cards.filter(card => card.year === 2023 && card.rubric.taskRequirements.some(rule => rule.startsWith('Special rule')));
    expect(special.map(card => [card.id, card.rubric.criteria[0].permittedMarks])).toEqual([
      ['fr-2023-hl-listening-la-q3', [0, 6]], ['fr-2023-hl-listening-lb-q2', [0, 4, 6]],
      ['fr-2023-hl-listening-lb-q3', [0, 2, 4, 6]], ['fr-2023-hl-listening-lc-q2', [0, 4, 6]],
      ['fr-2023-hl-listening-ld-q1', [0, 4, 6]], ['fr-2023-hl-listening-ld-q4', [0, 6]],
    ]);
    for (const card of cards.filter(card => card.year === 2023)) {
      expect(card.rubric.taskRequirements.join(' ')).toContain('25% deduction');
      expect(card.rubric.taskRequirements.join(' ')).toContain('whole test or whole section');
      expect(card.rubric.taskRequirements.join(' ')).not.toContain('50%');
    }
    expect(byId('hl-listening-lb-q3', 2023).rubric.taskRequirements.join(' ')).toContain('before applying the higher-segment rule');
    expect(byId('hl-listening-ld-q2a', 2023).rubric.criteria[0].permittedMarks).toEqual([0, 1, 2, 3]);
    expect(byId('hl-listening-lb-q4b', 2023).stem).toContain('accordion');
    expect(byId('ol-listening-la-q1b', 2023).stem).toContain('Grégoire’s area in Paris');
    expect(byId('ol-listening-le-q2b', 2023).rubric.criteria[0].permittedMarks).toEqual([0, 1, 3, 5]);
    expect(byId('ol-listening-le-q2b', 2023).rubric.answerGuide).toHaveLength(5);
  });
  it('uses the 2022 answer rule, special tariffs and actual printed scheme numbers', () => {
    const special = cards.filter(card => card.year === 2022 && card.rubric.taskRequirements.some(rule => rule.startsWith('Special rule')));
    expect(special.map(card => [card.id, card.rubric.criteria[0].permittedMarks])).toEqual([
      ['fr-2022-hl-listening-lb-q2', [0, 6]], ['fr-2022-hl-listening-lc-q2', [0, 6]], ['fr-2022-hl-listening-ld-q2', [0, 6]],
    ]);
    for (const card of cards.filter(card => card.year === 2022)) {
      expect(card.rubric.taskRequirements.join(' ')).toContain('25% deduction');
      if (card.level === 'higher') {
        expect(card.schemeCitation).toContain(`p.${card.schemeRegion!.p - 1}; general rules p.15`);
        expect(card.rubric.taskRequirements.join(' ')).toContain('opening questions until 25%');
      } else {
        expect(card.rubric.taskRequirements).toContain('If both a correct and incorrect answer are given, award 0 marks.');
        expect(card.rubric.taskRequirements.join(' ')).not.toContain('offering more than one');
      }
    }
    expect(byId('hl-listening-lc-q3', 2022).rubric.answerGuide).toContain('One correct fruit + one incorrect fruit = 2 Marks');
    expect(byId('hl-listening-ld-q1b', 2022).questionText).toContain('Amélie');
    expect(byId('ol-listening-lc-q2', 2022).questionText).toContain('Manu’s');
    expect(byId('ol-listening-lb-q3', 2022).rubric.answerGuide).toHaveLength(6);
    expect(byId('ol-listening-le-q2a', 2022).rubric.criteria[0].permittedMarks).toEqual([0, 3, 5]);
  });
  it('retains the 2021 three-mark MCQ and both pages of the complaint answer guide', () => {
    const mcq = byId('hl-listening-lb-q1', 2021);
    expect(mcq.questionChoices).toEqual(['worked as a stagehand', 'saw Luciano Pavarotti in a concert', 'sang in an opera', 'acted in several plays']);
    expect(mcq.totalMarks).toBe(3);
    expect(mcq.rubric.criteria[0].permittedMarks).toEqual([0, 3]);
    const complaint = byId('hl-listening-lc-q2a', 2021);
    expect(complaint.schemeCitation).toContain('pp.18,19; general rules p.16');
    expect(complaint.rubric.answerGuide).toHaveLength(7);
    expect(complaint.rubric.answerGuide).toContain('(He’s) loud — 2 Marks');
    expect(complaint.rubric.answerGuide).toContain('Does DIY morning till night / all the time (including Sundays) — 3 Marks');
    expect(byId('hl-listening-lb-q2a', 2021).rubric.criteria[0].permittedMarks).toEqual([0, 2, 3]);
    expect(byId('hl-listening-lb-q4', 2021).rubric.criteria[0].permittedMarks).toEqual([0, 1, 3, 4, 6]);
    expect(byId('hl-listening-ld-q2', 2021).rubric.criteria[0].permittedMarks).toEqual([0, 2, 3, 5, 6]);
    expect(cards.filter(card => card.year === 2021).every(card => !card.rubric.taskRequirements.some(rule => rule.startsWith('Special rule')))).toBe(true);
    expect(byId('hl-listening-le-q2b', 2021).stem).toContain('Pierre, named in Q2(a)');
    expect(byId('ol-listening-le-q2a', 2021).rubric.criteria[0].permittedMarks).toEqual([0, 3, 5]);
  });
  it('preserves 2020 page numbering, special scoring and the published ambiguity', () => {
    const special = cards.filter(card => card.year === 2020 && card.rubric.taskRequirements.some(rule => rule.startsWith('Special rule')));
    expect(special.map(card => [card.id, card.rubric.criteria[0].permittedMarks])).toEqual([
      ['fr-2020-hl-listening-la-q2', [0, 6]], ['fr-2020-hl-listening-lb-q2', [0, 4, 6]], ['fr-2020-hl-listening-lc-q2', [0, 4, 6]],
    ]);
    for (const card of cards.filter(card => card.year === 2020)) {
      const page = card.sourceMaterial!.pages[0];
      expect(card.sourceMaterial!.presentationNote).toContain(`printed page is ${page}; the PDF page is ${page}`);
    }
    expect(byId('hl-listening-ld-q4', 2020).rubric.criteria[0].permittedMarks).toEqual([0, 2, 3, 5, 6]);
    expect(byId('hl-listening-ld-q1', 2020).rubric.criteria[0].permittedMarks).toContain(1);
    expect(byId('hl-listening-le-q2b', 2020).rubric.criteria[0].permittedMarks).toEqual([0, 1, 2]);
    const ambiguous = byId('ol-listening-lb-q1', 2020);
    expect(ambiguous.rubric.answerGuide).toContain('Primary school teacher / worked in a primary school — 5 Marks');
    expect(ambiguous.rubric.answerGuide).toContain('Worked in a primary school — 3 Marks');
    expect(ambiguous.rubric.taskRequirements.join(' ')).toContain('at both 5 and 3 marks');
    expect(byId('hl-listening-lc-q3', 2020).stem).toContain('oral English classes');
  });
  it('preserves the 2019 Roman references, five/one split and level-specific general rules', () => {
    const tram = byId('hl-listening-ld-q3i', 2019);
    const job = byId('hl-listening-ld-q3ii', 2019);
    expect([tram.totalMarks, job.totalMarks]).toEqual([5, 1]);
    expect(tram.questionRef).toBe('2019 HL Section IV Q3(i)');
    expect(job.questionRef).toBe('2019 HL Section IV Q3(ii)');
    expect(job.audioMaterial.label).toBe('Section IV · listening');
    expect(job.audioMaterial.presentationNote).toContain('sections I–V');
    expect(job.sourceMaterial?.title).toContain('Section IV');
    expect(byId('hl-listening-lb-q3', 2019).rubric.criteria[0].permittedMarks).toEqual([0, 2, 3]);
    expect(byId('hl-listening-lc-q3', 2019).rubric.criteria[0].permittedMarks).toEqual([0, 3, 6]);
    const special = cards.filter(card => card.year === 2019 && card.rubric.taskRequirements.some(rule => rule.startsWith('Special rule')));
    expect(special.map(card => [card.id, card.rubric.criteria[0].permittedMarks])).toEqual([
      ['fr-2019-hl-listening-la-q3', [0, 4, 6]], ['fr-2019-hl-listening-lb-q1', [0, 6]],
      ['fr-2019-hl-listening-lb-q4', [0, 4, 6]], ['fr-2019-hl-listening-lc-q2', [0, 2, 4, 6]],
      ['fr-2019-hl-listening-ld-q2', [0, 4, 6]], ['fr-2019-hl-listening-ld-q4', [0, 4, 6]],
    ]);
    expect(byId('hl-listening-le-q3ii', 2019).stem).toContain('lottery winner');
    expect(byId('ol-listening-lc-q2', 2019).rubric.criteria[0].permittedMarks).toEqual([0, 1, 3, 5]);
    for (const card of cards.filter(card => card.year === 2019)) {
      if (card.level === 'ordinary') {
        expect(card.rubric.taskRequirements.join(' ')).not.toMatch(/%|offering more than one/);
        expect(card.rubric.taskRequirements).toContain('If both a correct and incorrect answer are given, award 0 marks.');
      } else expect(card.rubric.taskRequirements.join(' ')).toContain('25% deduction');
    }
  });
  it('splits the 2018 named parts while retaining combined responses and printed page citations', () => {
    const parts = cards.filter(card => card.id.startsWith('fr-2018-hl-listening-lc-q2-'));
    expect(parts.map(card => [card.id, card.totalMarks, card.rubric.criteria[0].permittedMarks])).toEqual([
      ['fr-2018-hl-listening-lc-q2-advantage', 3, [0, 1, 2, 3]],
      ['fr-2018-hl-listening-lc-q2-disadvantage', 3, [0, 1, 3]],
    ]);
    expect(parts[0].questionText).toContain('Answer for: Advantage.');
    expect(parts[1].questionText).toContain('Answer for: Disadvantage.');
    expect(parts[0].schemeCitation).toContain('p.23; general rules p.18');
    expect(parts[0].schemeRegion?.p).toBe(25);
    const dishes = byId('hl-listening-lb-q1', 2018);
    expect(dishes.totalMarks).toBe(3);
    expect(dishes.rubric.answerGuide).toHaveLength(8);
    expect(dishes.rubric.criteria[0].permittedMarks).toEqual([0, 1, 2, 3]);
    expect(byId('hl-listening-ld-q4', 2018).rubric.criteria[0].permittedMarks).toEqual([0, 1, 3, 4, 6]);
    expect(byId('hl-listening-lc-q3i', 2018).rubric.answerGuide).toContain('Any incorrect day included = 0 Marks');
    expect(byId('hl-listening-lc-q3ii', 2018).stem).toContain('grandparents');
    const cooks = byId('ol-listening-lb-q4', 2018);
    expect(cooks.rubric.criteria[0].permittedMarks).toEqual([0, 1, 5]);
    expect(cooks.rubric.answerGuide).toEqual(['They hadn’t a lot of experience — 5 Marks', 'They lacked experience — 1 Marks']);
    for (const card of cards.filter(card => card.year === 2018)) {
      expect(card.rubric.taskRequirements.join(' ')).not.toContain('Special rule');
      expect(card.schemeCitation).toContain(`p.${card.schemeRegion!.p - 2};`);
      if (card.level === 'ordinary') expect(card.rubric.taskRequirements.join(' ')).not.toContain('%');
    }
  });
  it('resolves every 2017 letter key and keeps the parents under their shared scoring rule', () => {
    const mcqs = cards.filter(card => card.year === 2017 && card.questionChoices);
    expect(mcqs.map(card => card.rubric.answerGuide)).toEqual([
      ['(c) funny — 5 Marks'], ['(d) having a snowball fight. — 5 Marks'], ['(b) Daniel’s family moved house. — 5 Marks'],
      ['(d) They are fed four times a day. — 5 Marks'], ['(a) She meets other farmers. — 5 Marks'],
      ['(b) He broke a back window. — 5 Marks'], ['(c) Under the stairs. — 5 Marks'],
      ['(a) A list of things to do. — 5 Marks'], ['(d) remove their shoes before entering a house. — 5 Marks'],
      ['(a) It will be raining. — 5 Marks'], ['(b) He punctured the tyres. — 5 Marks'], ['(c) A sofa. — 5 Marks'],
    ]);
    const special = cards.filter(card => card.year === 2017 && card.rubric.taskRequirements.some(rule => rule.startsWith('Special rule')));
    expect(special.map(card => card.id)).toEqual(['fr-2017-hl-listening-la-q2', 'fr-2017-hl-listening-lb-q2', 'fr-2017-hl-listening-lc-q2', 'fr-2017-hl-listening-ld-q2']);
    for (const card of special) expect(card.rubric.criteria[0].permittedMarks).toEqual([0, 2, 4, 6]);
    const parents = byId('hl-listening-lc-q2', 2017);
    expect(parents.totalMarks).toBe(6);
    expect(parents.stem).toContain('(a) Father and (b) Mother');
    expect(parents.rubric.taskRequirements.join(' ')).toContain('one answer for his father and one for his mother');
    expect(parents.rubric.answerGuide).toHaveLength(8);
    const subjects = byId('hl-listening-ld-q3ii', 2017);
    expect(subjects.totalMarks).toBe(3);
    expect(subjects.rubric.criteria[0].permittedMarks).toEqual([0, 2, 3]);
    expect(byId('hl-listening-lc-q3ii', 2017).rubric.criteria[0].permittedMarks).toEqual([0, 2, 3]);
    expect(byId('ol-listening-lc-q2', 2017).rubric.criteria[0].permittedMarks).toEqual([0, 1, 3, 5]);
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2017, fileid: 'LC010GLPA00EV.pdf' })?.playbackUrl).toContain('/2017/');
  });
  it('preserves the unusual 2010 one/four/seven/eight-mark allocations', () => {
    const special = cards.filter(card => card.year === 2010 && card.rubric.taskRequirements.some(rule => rule.startsWith('Special rule')));
    expect(special.map(card => [card.id, card.rubric.criteria[0].permittedMarks])).toEqual([
      ['fr-2010-hl-listening-lb-q2', [0, 2, 4, 6]], ['fr-2010-hl-listening-lb-q3', [0, 2, 4, 6]],
      ['fr-2010-hl-listening-ld-q2', [0, 8]], ['fr-2010-hl-listening-ld-q3', [0, 4, 6]],
    ]);
    for (const suffix of ['lb-q4i', 'lb-q4ii', 'lc-q3i', 'ld-q1']) expect(byId(`hl-listening-${suffix}`, 2010).totalMarks).toBe(1);
    expect(byId('hl-listening-lb-q4ii', 2010).rubric.answerGuide).toContain('Note: No penalty for incorrect number of years.');
    expect(byId('hl-listening-lc-q2i', 2010).rubric.criteria[0].permittedMarks).toEqual([0, 1, 2, 3]);
    expect(byId('hl-listening-lc-q2ii', 2010).rubric.answerGuide).toContain('* Or any other incorrect workplace.');
    expect(byId('ol-listening-la-q2ii', 2010).totalMarks).toBe(2);
    expect(byId('ol-listening-lb-q4', 2010).rubric.criteria[0].permittedMarks).toEqual([0, 1, 2]);
    expect(byId('ol-listening-lc-q2', 2010).rubric.criteria[0].permittedMarks).toEqual([0, 2, 3, 4]);
    expect(cards.filter(card => card.year === 2010 && card.questionChoices).map(card => card.rubric.answerGuide)).toEqual([
      ['(c) a surfing shop — 8 Marks'], ['(a) her parents make her do so — 5 Marks'], ['(b) he goes out in the evenings — 5 Marks'],
      ['(d) Castles of the Middle Ages. — 8 Marks'], ['(b) have to live with other members of the team — 5 Marks'],
      ['(d) The owner increased the rent. — 4 Marks'], ['(a) The floors. — 4 Marks'], ['(b) bottles of wine — 5 Marks'],
      ['(a) Refuse to buy an object. — 7 Marks'], ['(b) The Americans. — 7 Marks'],
      ['(b) The Minister for Health. — 5 Marks'], ['(c) The remote control. — 5 Marks'],
    ]);
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2010, fileid: 'LC010ALPA00EV.pdf' })?.playbackUrl).toContain('/2010/LC010ZLP017EV.mp3');
  });
  it('preserves the 2011 ten-percent rule, nested priced task and moon-landing deductions', () => {
    const special = cards.filter(card => card.year === 2011 && card.rubric.taskRequirements.some(rule => rule.startsWith('Special rule')));
    expect(special.map(card => [card.id, card.rubric.criteria[0].permittedMarks])).toEqual([
      ['fr-2011-hl-listening-la-q2', [0, 2, 4, 6]], ['fr-2011-hl-listening-lb-q2i', [0, 4, 6]],
      ['fr-2011-hl-listening-lb-q4', [0, 4, 6]], ['fr-2011-hl-listening-lc-q2', [0, 2, 4, 6]],
      ['fr-2011-hl-listening-ld-q3', [0, 2, 4, 6]],
    ]);
    expect(byId('hl-listening-lb-q2i', 2011).totalMarks).toBe(6);
    expect(byId('hl-listening-lb-q2ii', 2011).totalMarks).toBe(3);
    for (const card of cards.filter(card => card.year === 2011 && card.level === 'higher')) expect(card.rubric.taskRequirements.join(' ')).toContain('10% deduction');
    expect(byId('hl-listening-ld-q1ii', 2011).rubric.criteria[0].permittedMarks).toEqual([0, 2, 3]);
    expect(byId('hl-listening-ld-q2i', 2011).rubric.criteria[0].permittedMarks).toEqual([0, 1, 2, 3]);
    expect(byId('hl-listening-ld-q2i', 2011).rubric.answerGuide).toContain('Note: If words “when she saw” are omitted, minus 1 mark.');
    expect(byId('hl-listening-ld-q2i', 2011).rubric.answerGuide).toContain('If word “first” omitted, minus 1 mark.');
    expect(byId('hl-listening-la-q2', 2011).questionText).toContain('Roselyne');
    expect(byId('ol-listening-la-q2ii', 2011).questionText).toContain('Roselyn');
    expect(cards.filter(card => card.year === 2011 && card.questionChoices).map(card => card.rubric.answerGuide)).toEqual([
      ['(a) aggressive — 5 Marks'], ['(c) a night club — 5 Marks'], ['(d) In the mountains. — 5 Marks'],
      ['(b) English — 5 Marks'], ['(a) By phone. — 5 Marks'], ['(a) go back home — 5 Marks'],
      ['(a) angry — 5 Marks'], ['(b) pay for the repairs — 5 Marks'], ['(c) broke his arm — 5 Marks'],
      ['(b) At a press conference. — 5 Marks'], ['(d) 90 minutes. — 5 Marks'],
      ['(b) 2,400 travellers — 5 Marks'], ['(c) By the roadside. — 5 Marks'],
    ]);
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2011, fileid: 'LC010ALPA00EV.pdf' })?.playbackUrl).toContain('/2011/LC010ZLP017EV.mp3');
  });
  it('uses the 2012 twenty-percent rule, original audio filename and local injury deductions', () => {
    const special = cards.filter(card => card.year === 2012 && card.rubric.taskRequirements.some(rule => rule.startsWith('Special rule')));
    expect(special.map(card => [card.id, card.rubric.criteria[0].permittedMarks])).toEqual([
      ['fr-2012-hl-listening-la-q2', [0, 6]], ['fr-2012-hl-listening-lb-q2', [0, 4, 6]],
      ['fr-2012-hl-listening-lc-q2', [0, 2, 4, 6]], ['fr-2012-hl-listening-lc-q4', [0, 2, 4, 6]],
      ['fr-2012-hl-listening-ld-q3', [0, 2, 4, 6]],
    ]);
    for (const card of cards.filter(card => card.year === 2012 && card.level === 'higher')) {
      expect(card.rubric.taskRequirements.join(' ')).toContain('20% deduction');
      expect(card.rubric.taskRequirements.join(' ')).not.toContain('25%');
    }
    expect(byId('hl-listening-lb-q3ii', 2012).rubric.criteria[0].permittedMarks).toEqual([0, 1, 2, 3]);
    expect(byId('hl-listening-le-q3i', 2012).rubric.criteria[0].permittedMarks).toEqual([0, 1, 2]);
    expect(byId('hl-listening-le-q3ii', 2012).rubric.answerGuide).toContain('Note: Injured his leg, etc. = 1 mark.');
    expect(byId('hl-listening-le-q3ii', 2012).rubric.answerGuide).toContain('Broke his leg, etc. = 0 marks.');
    expect(cards.filter(card => card.year === 2012 && card.questionChoices).map(card => card.rubric.answerGuide)).toEqual([
      ['(b) for three weeks — 5 Marks'], ['(d) the mother was unpleasant. — 5 Marks'], ['(c) She used gestures. — 5 Marks'],
      ['(a) was not working enough at school — 5 Marks'], ['(d) spend time with their children. — 5 Marks'],
      ['(c) Chemistry — 5 Marks'], ['(a) Her guidance counsellor. — 5 Marks'], ['(b) physically difficult — 5 Marks'],
      ['(d) He published a book. — 5 Marks'], ['(c) He had frozen food in the boot. — 5 Marks'],
      ['(b) tell the truth — 5 Marks'], ['(b) 340 grammes. — 5 Marks'], ['(a) He injured his back. — 5 Marks'],
    ]);
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2012, fileid: 'LC010ALPA00EV.pdf' })?.playbackUrl).toContain('/2012/LC010ZLPO17EV.mp3');
  });
  it('preserves the 2013 independent pair, pronoun deductions and third Ordinary scheme page', () => {
    const special = cards.filter(card => card.year === 2013 && card.rubric.taskRequirements.some(rule => rule.startsWith('Special rule')));
    expect(special.map(card => [card.id, card.rubric.criteria[0].permittedMarks])).toEqual([
      ['fr-2013-hl-listening-la-q3', [0, 2, 4, 6]], ['fr-2013-hl-listening-lb-q4', [0, 2, 4, 6]],
      ['fr-2013-hl-listening-lc-q3', [0, 2, 4, 6]], ['fr-2013-hl-listening-ld-q4', [0, 4, 6]],
    ]);
    expect(byId('hl-listening-lb-q2', 2013).rubric.criteria[0].permittedMarks).toEqual([0, 1, 2, 3, 4, 5, 6]);
    expect(byId('hl-listening-lb-q3ii', 2013).rubric.answerGuide).toContain('If “They” offered instead of “He” / “Guy”, award 2 Marks.');
    expect(byId('hl-listening-lb-q4', 2013).rubric.answerGuide).toContain('He was (very) grateful to his neighbours for helping him / for saving animals — 3 Marks');
    expect(byId('hl-listening-lb-q4', 2013).rubric.answerGuide).toContain('He was (very) grateful — 1 Marks');
    expect(byId('hl-listening-lc-q1ii', 2013).rubric.answerGuide).toContain('Note: If two jobs offered, award 0 Marks.');
    expect(byId('ol-listening-le-q3', 2013).schemeRegion!.p).toBe(18);
    expect(byId('ol-listening-le-q3', 2013).schemeCitation).toContain('p.16; general rules p.14');
    expect(cards.filter(card => card.year === 2013 && card.questionChoices).map(card => card.rubric.answerGuide)).toEqual([
      ['(b) sold their car — 5 Marks'], ['(c) shy — 5 Marks'], ['(a) leave her friends — 5 Marks'],
      ['(a) the hours are long — 5 Marks'], ['(d) snowfalls. — 5 Marks'],
      ['(d) A civil servant. — 5 Marks'], ['(c) go hunting — 5 Marks'], ['(a) It broke a vase. — 5 Marks'],
      ['(b) a motorbike accident — 5 Marks'], ['(c) She cried on the podium. — 5 Marks'],
      ['(a) She gives talks in schools. — 5 Marks'], ['(b) China. — 5 Marks'], ['(c) 40,000. — 5 Marks'],
    ]);
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2013, fileid: 'LC010ALPA00EV.pdf' })?.playbackUrl).toContain('/2013/');
  });
  it('retains the 2014 grouped details, deductions and misnumbered Ordinary answers', () => {
    const special = cards.filter(card => card.year === 2014 && card.rubric.taskRequirements.some(rule => rule.startsWith('Special rule')));
    expect(special.map(card => [card.id, card.rubric.criteria[0].permittedMarks])).toEqual([
      ['fr-2014-hl-listening-la-q2', [0, 2, 4, 6]], ['fr-2014-hl-listening-lb-q2', [0, 2, 4, 6]],
      ['fr-2014-hl-listening-lb-q4', [0, 2, 4, 6]], ['fr-2014-hl-listening-lc-q2', [0, 2, 4, 6]],
      ['fr-2014-hl-listening-ld-q4', [0, 4, 6]],
    ]);
    expect(byId('hl-listening-la-q2', 2014).rubric.answerGuide).toContain('Two of (i.e. one from “Luggage” and one from “Late plane”)');
    expect(byId('hl-listening-lc-q1i', 2014).rubric.criteria[0].permittedMarks).toEqual([0, 1, 2, 3]);
    expect(byId('hl-listening-ld-q3i', 2014).rubric.answerGuide).toContain('(It’s) not affected by the recession / economic crisis — 0 Marks');
    expect(byId('ol-listening-lb-q1', 2014).rubric.answerGuide).toEqual(['Twenty-five years ago / 1989 — 5 Marks']);
    expect(byId('ol-listening-lb-q3', 2014).rubric.answerGuide).toEqual(['The water is (too / very) cold — 5 Marks', 'It’s (too / very) cold — 3 Marks']);
    expect(cards.filter(card => card.year === 2014 && card.questionChoices).map(card => card.rubric.answerGuide)).toEqual([
      ['(a) Brussels. — 5 Marks'], ['(b) Four hours. — 5 Marks'], ['(d) they had got on the wrong train. — 5 Marks'],
      ['(c) Watch the sunrise. — 5 Marks'], ['(b) Produce an album for children. — 5 Marks'],
      ['(b) a criminal gang — 5 Marks'], ['(d) it will be his first time on stage. — 5 Marks'],
      ['(c) Waiter. — 5 Marks'], ['(a) The rents are cheaper. — 5 Marks'], ['(b) The postal service. — 5 Marks'],
      ['(d) Because of a flood. — 5 Marks'], ['(c) In a rubbish bin. — 5 Marks'],
    ]);
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2014, fileid: 'LC010ALPA00EV.pdf' })?.playbackUrl).toContain('/2014/');
  });
  it('retains the 2015 eight-mark pair, one-mark news and coupled advantage/disadvantage', () => {
    const special = cards.filter(card => card.year === 2015 && card.rubric.taskRequirements.some(rule => rule.startsWith('Special rule')));
    expect(special.map(card => [card.id, card.rubric.criteria[0].permittedMarks])).toEqual([
      ['fr-2015-hl-listening-la-q2', [0, 8]], ['fr-2015-hl-listening-lb-q2', [0, 2, 4, 6]],
      ['fr-2015-hl-listening-lc-q2', [0, 4, 6]], ['fr-2015-hl-listening-ld-q1', [0, 2, 4, 6]],
      ['fr-2015-hl-listening-ld-q4', [0, 2, 4, 6]],
    ]);
    const pair = byId('hl-listening-ld-q4', 2015);
    expect(pair.questionText).toContain('(a) one advantage and (b) one disadvantage');
    expect(pair.rubric.answerGuide).toContain('(a)');
    expect(pair.rubric.answerGuide).toContain('(b)');
    expect(byId('hl-listening-la-q3', 2015).rubric.criteria[0].permittedMarks).toEqual([0, 2, 3, 4]);
    expect(byId('hl-listening-ld-q1', 2015).rubric.taskRequirements.join(' ')).toContain('before applying the higher-segment rule');
    for (const q of ['1', '2i', '2ii', '3']) expect(byId(`hl-listening-le-q${q}`, 2015).totalMarks).toBe(1);
    for (const suffix of ['lc-q1i', 'ld-q2', 'le-q2i', 'le-q3']) expect(byId(`ol-listening-${suffix}`, 2015).rubric.criteria[0].permittedMarks).toEqual([0, 4, 5]);
    expect(cards.filter(card => card.year === 2015 && card.questionChoices).map(card => card.rubric.answerGuide)).toEqual([
      ['(a) In a bakery. — 5 Marks'], ['(d) He walked home. — 5 Marks'], ['(d) Winter. — 5 Marks'],
      ['(b) She didn’t have a lot of success. — 5 Marks'], ['(a) She can swim in front of her house. — 5 Marks'],
      ['(a) Hairstyles. — 5 Marks'], ['(c) It must be easy to find in search engines. — 5 Marks'],
      ['(d) It’s on the sixth floor. — 5 Marks'], ['(d) Paris is an expensive city. — 5 Marks'],
      ['(c) fill up the fridge — 5 Marks'], ['(c) A parking spot. — 5 Marks'], ['(b) They were taken hostage. — 5 Marks'],
    ]);
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2015, fileid: 'LC010ALPA00EV.pdf' })?.playbackUrl).toContain('/2015/');
  });
  it('preserves the 2016 local deductions and all thirteen letter-key answers', () => {
    const special = cards.filter(card => card.year === 2016 && card.rubric.taskRequirements.some(rule => rule.startsWith('Special rule')));
    expect(special.map(card => [card.id, card.rubric.criteria[0].permittedMarks])).toEqual([
      ['fr-2016-hl-listening-la-q3', [0, 2, 4, 6]], ['fr-2016-hl-listening-lb-q3', [0, 4, 6]],
      ['fr-2016-hl-listening-lc-q2', [0, 4, 6]], ['fr-2016-hl-listening-ld-q1', [0, 2, 4, 6]],
      ['fr-2016-hl-listening-ld-q3', [0, 4, 6]],
    ]);
    expect(byId('hl-listening-lb-q4i', 2016).rubric.criteria[0].permittedMarks).toEqual([0, 1, 2, 3]);
    expect(byId('hl-listening-lb-q4i', 2016).rubric.answerGuide).toContain('Note: One correct month = 2 marks.');
    expect(byId('hl-listening-ld-q4', 2016).rubric.criteria[0].permittedMarks).toEqual([0, 1, 2, 3]);
    expect(byId('hl-listening-ld-q4', 2016).rubric.answerGuide).toContain('Note: One or two items of rubbish missing, minus 1 mark.');
    expect(byId('hl-listening-le-q3ii', 2016).questionText).toBe('Where exactly in Falaise was this object discovered?');
    expect(byId('hl-listening-le-q3ii', 2016).rubric.answerGuide).toContain('Note: Incorrect preposition (e.g. near) + city / town hall = 0 marks.');
    expect(cards.filter(card => card.year === 2016 && card.questionChoices).map(card => card.rubric.answerGuide)).toEqual([
      ['(a) In the mountains. — 5 Marks'], ['(d) The drums. — 5 Marks'], ['(b) He has a salary. — 5 Marks'],
      ['(c) He eats three hours beforehand. — 5 Marks'], ['(d) His daughter was born in September. — 5 Marks'],
      ['(d) Parking is impossible. — 5 Marks'], ['(b) The bedrooms are dirty. — 5 Marks'],
      ['(a) It only takes him five minutes. — 5 Marks'], ['(c) A microwave oven. — 5 Marks'], ['(b) Gloves. — 5 Marks'],
      ['(c) 28,000. — 5 Marks'], ['(b) a bomb — 5 Marks'], ['(c) The town hall. — 5 Marks'],
    ]);
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2016, fileid: 'LC010ALPA00EV.pdf' })?.playbackUrl).toContain('/2016/');
  });
  it('links each task to the aural booklet and its exact canonical Atlas topic', () => {
    for (const card of cards) {
      const task = tasks.find(task => task.cardId === card.id)!;
      expect(task.paperKey).toBe('aural');
      const paper = topicsForPaper('french', card.year, card.level, 'ev', task.fileid)!;
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === task.n)!)).toEqual(task.topicIds);
      expect(task.topicIds.flatMap(curriculumNodeIdsForExamTopic)).toContain(card.topicId);
      const map = JSON.parse(fs.readFileSync(`public/paper-anchors/${card.year}/${task.fileid}.json`, 'utf8'));
      expect(paperRegionFor(map.q, task.n, map.maxCropPages)?.map(region => region.p)).toEqual(task.pages);
      expect(card.sourceMaterial?.pages).toEqual(task.pages);
    }
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2026, fileid: 'LC010ALPA00BV.pdf' })).not.toBeNull();
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2026, fileid: 'LC010GLPA00BV.pdf' })).not.toBeNull();
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2026, fileid: 'LC010ALP000BV.pdf' })).toBeNull();
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2025, fileid: 'LC010ALPA00BV.pdf' })?.playbackUrl).toContain('/2025/');
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2025, fileid: 'LC010GLPA00BV.pdf' })?.playbackUrl).toContain('/2025/');
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2024, fileid: 'LC010ALPA00BV.pdf' })?.playbackUrl).toContain('/2024/');
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2024, fileid: 'LC010GLPA00BV.pdf' })?.playbackUrl).toContain('/2024/');
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2023, fileid: 'LC010ALPA00BV.pdf' })?.playbackUrl).toContain('/2023/');
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2023, fileid: 'LC010GLPA00BV.pdf' })?.playbackUrl).toContain('/2023/');
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2022, fileid: 'LC010ALPA00BV.pdf' })?.playbackUrl).toContain('/2022/LC010CLP017BV.mp3');
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2022, fileid: 'LC010GLPA00BV.pdf' })?.playbackUrl).toContain('/2022/LC010CLP017BV.mp3');
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2021, fileid: 'LC010ALPA00BV.pdf' })?.playbackUrl).toContain('/2021/LC010ZLP017EV.mp3');
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2021, fileid: 'LC010GLPA00BV.pdf' })?.playbackUrl).toContain('/2021/LC010ZLP017EV.mp3');
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2020, fileid: 'LC010ALPA00BV.pdf' })?.playbackUrl).toContain('/2020/LC010ZLP017EV.mp3');
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2020, fileid: 'LC010GLPA00BV.pdf' })?.playbackUrl).toContain('/2020/LC010ZLP017EV.mp3');
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2018, fileid: 'LC010ALPA00EV.pdf' })?.playbackUrl).toContain('/2018/');
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2018, fileid: 'LC010GLPA00EV.pdf' })?.playbackUrl).toContain('/2018/');
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2018, fileid: 'LC010ALPA00BV.pdf' })).toBeNull();
    expect(frenchAudioForPaper({ subjectId: 'french', year: 2009, fileid: 'LC010ALPA00EV.pdf' })).toBeNull();
  });
  it('keeps all independently assessed tasks reachable in a French session', () => {
    expect(cards.every(card => listeningExerciseKey(card) === null)).toBe(true);
    expect(visibleSessionExercises(cards)).toHaveLength(715);
    expect(resolveSessionQueue(cards, {}, Date.UTC(2026, 9, 7))).toHaveLength(12);
  });
  it('plays on the question side, selects an MCQ, and grades only the current task', () => {
    const first = byId('ol-listening-la-q1');
    const next = byId('ol-listening-la-q2a');
    const onGrade = vi.fn();
    const { baseElement } = render(<SessionScreen cards={[first, next]} subjectLabel="French" onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()} />);
    expect(baseElement.querySelector('audio')).toHaveAttribute('src', audio[0].source.playbackUrl);
    expect(screen.getAllByRole('radio')).toHaveLength(4);
    expect(screen.queryByText('Camping — 5 Marks')).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('radio', { name: 'camping' }));
    expect(screen.getByRole('radio', { name: 'camping' })).toBeChecked();
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    expect(screen.getByText('Camping — 5 Marks')).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText('Response mark'), { target: { value: '5' } });
    fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
    expect(onGrade).toHaveBeenCalledTimes(1);
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({ cardId: first.id, marksClaimed: 5, marksAvailable: 5 }));
    expect(screen.getByRole('radio', { name: 'bar' })).not.toBeChecked();
    expect(screen.queryByText('SEC French marking scheme')).not.toBeInTheDocument();
  });
  it('keeps the official playback and recovery link available in Topic Atlas', () => {
    vi.stubGlobal('IntersectionObserver', class {
      constructor(private callback: (entries: { isIntersecting: boolean }[]) => void) {}
      observe() { this.callback([{ isIntersecting: true }]); }
      disconnect() {}
    });
    const { container } = render(<VaultQuestionCard sibling={{ subjectId: 'french', level: 'ordinary', lang: 'ev', year: 2026, fileid: 'LC010GLPA00BV.pdf', paperKey: 'aural', n: 'LA-Q1' }} saved={false} onToggleReview={vi.fn()} onOpenInPaper={vi.fn()} />);
    const player = container.querySelector('audio')!;
    expect(player).toHaveAttribute('src', audio[0].source.playbackUrl);
    fireEvent.error(player);
    expect(screen.getByRole('link', { name: 'Open the SEC recording' })).toHaveAttribute('href', audio[0].source.canonicalUrl);
    expect(within(container).queryByText('Camping — 5 Marks')).not.toBeInTheDocument();
  });
});
