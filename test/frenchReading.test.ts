import { describe, expect, it } from 'vitest';
import fs from 'node:fs';
import { FRENCH_READING_CARDS as cards } from '../components/MarkBank/cards/french/reading';
import { CARDS as higher } from '../components/MarkBank/cards/french/higher';
import { CARDS as ordinary } from '../components/MarkBank/cards/french/ordinary';
import tasks from '../data/examTopics/french-reviewed-tasks.json';
import { tariffReconciles } from '../types/markBank';
import { examTopicIdsForQuestion, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { topicsForPaper, browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { paperRegionFor } from '../components/PaperTrail/paperRegion';
import { frenchMarks, frenchRowScoreId } from '../components/MarkBank/frenchRubric';

const byId = (suffix: string) => cards.find(card => card.id === `fr-2026-${suffix}`)!;
const legacy = (suffix: string) => cards.find(card => card.id === `fr-2025-${suffix}`)!;
const card2010 = (suffix: string) => cards.find(card => card.id === `fr-2010-${suffix}`)!;
const card2011 = (suffix: string) => cards.find(card => card.id === `fr-2011-${suffix}`)!;
const card2012 = (suffix: string) => cards.find(card => card.id === `fr-2012-${suffix}`)!;
const card2013 = (suffix: string) => cards.find(card => card.id === `fr-2013-${suffix}`)!;
const card2014 = (suffix: string) => cards.find(card => card.id === `fr-2014-${suffix}`)!;
const card2015 = (suffix: string) => cards.find(card => card.id === `fr-2015-${suffix}`)!;
const card2016 = (suffix: string) => cards.find(card => card.id === `fr-2016-${suffix}`)!;
const card2017 = (suffix: string) => cards.find(card => card.id === `fr-2017-${suffix}`)!;
const card2018 = (suffix: string) => cards.find(card => card.id === `fr-2018-${suffix}`)!;
const card2019 = (suffix: string) => cards.find(card => card.id === `fr-2019-${suffix}`)!;
const card2020 = (suffix: string) => cards.find(card => card.id === `fr-2020-${suffix}`)!;
const card2021 = (suffix: string) => cards.find(card => card.id === `fr-2021-${suffix}`)!;
const card2022 = (suffix: string) => cards.find(card => card.id === `fr-2022-${suffix}`)!;
const card2023 = (suffix: string) => cards.find(card => card.id === `fr-2023-${suffix}`)!;
const card2024 = (suffix: string) => cards.find(card => card.id === `fr-2024-${suffix}`)!;
type ReadingCard = (typeof cards)[number];
// Which printed marker gives full credit is the scheme's own convention, as its
// lifted note states: a stroke (-) in the older Ordinary schemes, a bullet
// point (•) elsewhere; partial credit is an asterisk (*) or a dash.
const strokeConvention = (card: ReadingCard) => (card.rubric.markingGuideNote ?? '').startsWith('Please note that');
const fullCredit = (card: ReadingCard) => card.rubric.answerGuide!.filter(line => line.startsWith(strokeConvention(card) ? '- ' : '•'));
const partCredit = (card: ReadingCard) => card.rubric.answerGuide!.filter(line => line.startsWith(strokeConvention(card) ? '* ' : '–'));
const practice = (card: ReadingCard) => (card.rubric.practiceNotes ?? []).join(' ');

describe('visually reviewed French reading tasks', () => {
  it('retains every reviewed tariff boundary and all original cards', () => {
    expect(cards).toHaveLength(925);
    expect(cards.filter(card => card.level === 'higher')).toHaveLength(372);
    expect(cards.filter(card => card.level === 'ordinary')).toHaveLength(553);
    expect([...higher, ...ordinary]).toHaveLength(2120);
    expect(new Set([...higher, ...ordinary].map(card => card.id)).size).toBe(2120);
    for (const year of [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]) {
      for (const [level, counts, totals] of [
        ['higher', [2015, 2019].includes(year) ? [11, 10] : [11, 11], [60, 60]], ['ordinary', year === 2010 ? [5, 5, 7, 8] : year === 2011 ? [10, 9, 8, 8] : year === 2012 ? [9, 8, 9, 8] : year === 2013 ? [8, 8, 8, 9] : year === 2014 ? [8, 8, 8, 10] : year === 2015 ? [5, 5, 8, 8] : year === 2016 ? [8, 10, 8, 8] : year === 2018 ? [9, 8, 9, 8] : year === 2022 ? [9, 9, 8, 8] : [2021, 2024].includes(year) ? [8, 9, 8, 8] : [9, 8, 8, 8], [40, 40, 40, 40]],
      ] as const) {
        counts.forEach((count, index) => {
          const group = cards.filter(card => card.year === year && card.level === level && card.questionRef.includes(`Section A${index + 1} `));
          expect(group).toHaveLength(count);
          expect(group.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(totals[index]);
        });
      }
    }
  });

  it('retains 2010 uneven tariffs, jointly priced questions and the Q7 opinion language', () => {
    for (const [part, mark] of [['i', 5], ['ii', 2], ['iii', 2]] as const) expect(card2010(`hl-reading-a1-q2-${part}`).totalMarks).toBe(mark);
    expect(card2010('hl-reading-a1-q4').rubric.criteria[0].permittedMarks).toEqual([0, 1]);
    for (const [rc, count] of [[1, 16], [2, 17]]) {
      const card = card2010(`hl-reading-a${rc}-q6`);
      expect(card.totalMarks).toBe(12);
      expect(fullCredit(card)).toHaveLength(count);
    }
    expect(card2010('hl-reading-a1-q6').rubric.taskRequirements.join(' ')).not.toContain('higher segment score');
    expect(card2010('hl-reading-a2-q6').rubric.criteria[0].permittedMarks).toEqual([0, 2, 4, 6, 8, 10, 12]);
    expect(card2010('hl-reading-a2-q3-i').rubric.answerGuide!.join(' ')).toContain('ne laissant');
    for (const [rc, groups] of [[1, [[1, 2], [4, 5], [6, 7], [8, 9]]], [2, [[1, 2], [3, 4], [5, 6], [8, 9]]]] as const) {
      for (const group of groups) {
        const card = card2010(`ol-reading-a${rc}-q${group[0]}`);
        for (const q of group) expect(card.questionText).toMatch(new RegExp(`(^|\n)${q}\\. `));
        expect(card.rubric.criteria[0].permittedMarks).toEqual([0, 7, 8]);
        expect(card.rubric.taskRequirements).toContain('Two correct answers required for 8 marks (7 + 1).');
        expect(practice(card)).toContain('1 additional mark');
      }
    }
    const parents = card2010('ol-reading-a3-q3');
    expect(parents.questionText).toContain('(a) son père');
    expect(parents.questionText).toContain('(b) sa mère');
    expect(parents.totalMarks).toBe(8);
    expect(parents.rubric.taskRequirements).toContain('3.(a) & (b) 7 + 1 marks');
    expect(practice(parents)).toContain('1 additional mark');
    const opinion = card2010('ol-reading-a3-q7');
    expect(opinion.rubric.taskRequirements[0]).toBe('Aux questions posées en irlandais/anglais il faut répondre en irlandais ou en anglais.');
    expect(opinion.sourceMaterial!.title).toBe('Reading Comprehension 3');
    expect(opinion.rubric.taskRequirements).toContain('In Q.7, where no attempt is made at answering in English or Irish, a correct quote in French is to be awarded half marks.');
    expect(fullCredit(opinion)).toHaveLength(7);
    expect(fullCredit(card2010('ol-reading-a4-q8'))).toHaveLength(9);
    expect(card2010('ol-reading-a4-q1').rubric.taskRequirements).toContain('N.B. Penalise extraneous material to a maximum of 1 mark.');
    expect(partCredit(card2010('ol-reading-a3-q5'))).toHaveLength(4);
    expect(card2010('ol-reading-a3-q4').rubric.answerGuide!.join(' ')).toContain('One correct verb and one incorrect verb = 0');
    expect(cards.filter(card => card.year === 2010 && card.questionChoices)).toHaveLength(4);
  });

  it('restores 2011 tiled text and independently priced positive and negative answers', () => {
    expect(card2011('ol-reading-a3-q1').questionText).toBe('Dans quel mois de l’année organise-t-on la plupart de brocantes / vide-greniers ? (Section 1)');
    expect(card2011('ol-reading-a4-q2').questionText).toBe('Citez le mot qui décrit les sentiments de sa mère. (Section 1)');
    for (const [part, label, examples] of [['a', 'Positif', 6], ['b', 'Négatif', 4]] as const) {
      const card = card2011(`hl-reading-a1-q3-${part}`);
      expect(card.totalMarks).toBe(5);
      expect(card.questionText).toBe(`Pour Christine, son hébergement chez Gabrielle a des aspects à la fois positifs et négatifs. Donnez-en un exemple, dans chaque cas. (Section 3)\n\n(${part}) ${label} :`);
      expect(practice(card)).toContain('wrong category');
      expect(practice(card)).toContain('scheme heading');
      expect(fullCredit(card)).toHaveLength(examples);
      expect(card.rubric.answerGuide!.join(' ')).toContain('award 0 marks for that line');
      expect(tasks.find(task => task.cardId === card.id)?.parent).toBe('5');
    }
    for (const [rc, q] of [[2, 4], [3, 2], [4, 5]]) expect(card2011(`ol-reading-a${rc}-q${q}`).totalMarks).toBe(8);
    expect(partCredit(card2011('ol-reading-a4-q5'))).toHaveLength(2);
    for (const [rc, q] of [[3, 6], [4, 1], [4, 7]]) expect(card2011(`ol-reading-a${rc}-q${q}`).rubric.answerGuide!.join(' ')).toContain('Penalise attempt at manipulation by deducting 1 mark');
    expect(card2011('ol-reading-a4-q7').rubric.taskRequirements.join(' ')).not.toContain('a quotation is given');
    expect(card2011('hl-reading-a1-q5-i').rubric.criteria[0].permittedMarks).toEqual([0, 5]);
    expect(fullCredit(card2011('hl-reading-a1-q6'))).toHaveLength(10);
    expect(fullCredit(card2011('hl-reading-a2-q6'))).toHaveLength(10);
    for (const rc of [3, 4]) expect(fullCredit(card2011(`ol-reading-a${rc}-q8`))).toHaveLength(6);
    expect(cards.filter(card => card.year === 2011 && card.questionChoices)).toHaveLength(4);
  });

  it('retains 2012 named categories, coupled opinion scoring and the disclosed missing tariff', () => {
    for (const [rc, labels] of [[1, ['Male', 'Female']], [3, ['Mère', 'Père']]] as const) {
      for (const [index, part] of ['i', 'ii'].entries()) {
        const card = card2012(`ol-reading-a${rc}-q1-${part}`);
        expect(card.totalMarks).toBe(4);
        expect(card.questionText).toContain(labels[index]);
        expect(card.questionText).toContain('(Section 1)');
      }
    }
    expect(card2012('ol-reading-a1-q1-i').rubric.answerGuide!.join(' ')).not.toContain('makeup');
    expect(card2012('ol-reading-a3-q1-ii').rubric.answerGuide!.join(' ')).toContain('directeur 2 marks');
    for (const rc of [1, 2]) {
      const card = card2012(`hl-reading-a${rc}-q6`);
      expect(card.totalMarks).toBe(10);
      expect(card.rubric.taskRequirements).toContain('In Q.6, where less than full marks is achieved in either segment, the higher mark is to be awarded to each segment.');
      expect(practice(card)).toContain('twice the higher segment score');
      expect(card.rubric.criteria[0].permittedMarks).toEqual([0, 2, 4, 6, 8, 10]);
    }
    const paired = card2012('hl-reading-a2-q6');
    expect(paired.questionText).toContain('countryside and (ii) the restaurant');
    expect(paired.rubric.answerGuide).toContain('(i) Countryside');
    expect(paired.rubric.answerGuide).toContain('(ii) Restaurant');
    expect(fullCredit(card2012('hl-reading-a1-q6'))).toHaveLength(10);
    expect(card2012('hl-reading-a1-q2-ii').questionText).toContain('réseau RER');
    expect(card2012('ol-reading-a4-q2').questionText).toBe('Comment sont les résultats scolaires de Jenny ? (Section 1)');
    expect(practice(card2012('ol-reading-a2-q7'))).toContain('same applause point');
    const missing = card2012('ol-reading-a4-q7');
    expect(missing.totalMarks).toBe(4);
    expect(practice(missing)).toContain('without a mark figure');
    expect(practice(missing)).toContain('total 36');
    expect(cards.filter(card => card.year === 2012 && card.questionChoices)).toHaveLength(4);
    expect(fullCredit(card2012('ol-reading-a3-q8'))).toHaveLength(4);
    expect(fullCredit(card2012('ol-reading-a4-q8'))).toHaveLength(6);
  });

  it('preserves 2013 two-mark answers, required pairs and the two named opinion parts', () => {
    for (const q of [3, 6]) {
      const card = card2013(`ol-reading-a3-q${q}`);
      expect(card.totalMarks).toBe(2);
      expect(card.rubric.answerGuide!.join(' ')).toContain('1 mark');
    }
    const pair = card2013('ol-reading-a3-q1');
    expect(pair.totalMarks).toBe(8);
    expect(fullCredit(pair)).toHaveLength(2);
    expect(card2013('ol-reading-a4-q4').rubric.answerGuide!.at(-1)).toContain('3 marks');
    for (const [part, label] of [['i', 'Diane:'], ['ii', 'Mother:']]) {
      const card = card2013(`ol-reading-a4-q8-${part}`);
      expect(card.totalMarks).toBe(4);
      expect(card.questionText).toContain('Both Diane and her mother');
      expect(card.questionText).toContain(label);
      expect(card.questionText).toContain('Answer in English, giving TWO points and referring to the text.');
      expect(practice(card)).toContain('Give one supported point');
      expect(fullCredit(card)).toHaveLength(5);
      expect(card.rubric.answerGuide!.at(-1)).toBe('Award 2 marks if answer is partially correct.');
      expect(card.schemeRegion?.p).toBe(9);
    }
    expect(fullCredit(card2013('ol-reading-a3-q8'))).toHaveLength(9);
    expect(fullCredit(card2013('hl-reading-a1-q6'))).toHaveLength(11);
    expect(fullCredit(card2013('hl-reading-a2-q6'))).toHaveLength(6);
    expect(card2013('hl-reading-a2-q4-ii').questionText).toMatch(/^Selon la troisième section,/);
    expect(card2013('hl-reading-a2-q5-i').rubric.criteria[0].permittedMarks).toEqual([0, 5]);
    expect(card2013('hl-reading-a1-q2-i').rubric.answerGuide!.join(' ')).toContain('maximum penalty minus 2');
    expect(card2013('hl-reading-a1-q1-i').rubric.answerGuide!.join(' ')).toContain('only one month offered, minus 2');
    expect(cards.filter(card => card.year === 2013 && card.questionChoices)).toHaveLength(4);
    expect(cards.filter(card => card.year === 2013 && card.level === 'ordinary' && card.questionRef.includes('Section A2 ')).every(card => card.topicId === 'french-5-3')).toBe(true);
  });

  it('separates 2014 independent questions and named opinion parts with their full ladders', () => {
    const change = card2014('ol-reading-a4-q5-i');
    const books = card2014('ol-reading-a4-q5-ii');
    expect(change.questionText).toContain('Pourquoi Laurent');
    expect(books.questionText).toContain('aimait la lecture');
    expect(change.rubric.answerGuide!.join(' ')).not.toContain('bibliothèque');
    expect(books.rubric.answerGuide!.join(' ')).not.toContain('douche');
    expect(books.rubric.answerGuide!.at(-1)).toContain('1 mark');
    for (const [part, label, examples] of [['i', 'parents', 8], ['ii', 'sisters', 2]] as const) {
      const card = card2014(`ol-reading-a4-q8-${part}`);
      expect(card.totalMarks).toBe(4);
      expect(card.questionText).toContain('(i) Laurent’s parents, and (ii) his sisters, Céline and Marie?');
      expect(card.questionText.split('\n').at(-1)).toBe(`His ${label}:`);
      expect(card.questionText).toContain('Answer in English, giving TWO points and referring to the text.');
      expect(practice(card)).toContain('Give one supported point');
      expect(fullCredit(card)).toHaveLength(examples);
      expect(card.rubric.answerGuide!.at(-1)).toBe('Award 2 marks if answer is partially correct.');
      expect(card.schemeRegion?.p).toBe(9);
    }
    expect(card2014('ol-reading-a3-q2').totalMarks).toBe(8);
    expect(card2014('ol-reading-a3-q2').rubric.answerGuide!.join(' ')).toContain('indépendante');
    expect(card2014('ol-reading-a3-q2').rubric.answerGuide!.join(' ')).toContain('ambitieuse');
    expect(fullCredit(card2014('hl-reading-a1-q1-i'))).toHaveLength(2);
    expect(fullCredit(card2014('hl-reading-a1-q6'))).toHaveLength(16);
    expect(fullCredit(card2014('hl-reading-a2-q6'))).toHaveLength(11);
    expect(fullCredit(card2014('ol-reading-a3-q8'))).toHaveLength(12);
    expect(card2014('hl-reading-a2-q2-i').questionText).toMatch(/^Dans la deuxième section,/);
    expect(card2014('hl-reading-a2-q2-i').questionText).not.toContain('(Section 1)');
    expect(card2014('hl-reading-a2-q5-ii').rubric.criteria[0].permittedMarks).toEqual([0, 5]);
    expect(card2014('hl-reading-a2-q5-ii').rubric.answerGuide!.join(' ')).toContain('s’oppose');
    const circus = card2014('hl-reading-a1-q6');
    expect(circus.topicId).toBe('french-5-0');
    const task = tasks.find(task => task.cardId === circus.id)!;
    for (const n of [task.n, '11']) {
      expect(examTopicIdsForQuestion('french', 'higher', 2014, 'main', n, 'single', 'ev', task.fileid)).toEqual(['french-higher-newspapermagazine-comprehension']);
    }
    expect(cards.filter(card => card.year === 2014 && card.questionChoices)).toHaveLength(4);
  });

  it('keeps 2015 shared seven-plus-one tariffs with every numbered prompt', () => {
    for (const [rc, groups] of [[1, [[1], [2, 3], [4], [5, 6], [7]]], [2, [[1], [2, 3], [4, 5], [6, 7], [8, 9]]]] as const) {
      for (const group of groups) {
        const card = card2015(`ol-reading-a${rc}-q${group[0]}`);
        expect(card.totalMarks).toBe(8);
        expect(card.rubric.criteria[0].permittedMarks).toEqual([0, 7, 8]);
        expect(card.rubric.taskRequirements).toContain(rc === 1 ? 'Two correct answers needed for 8 marks (7+1).' : 'Two correct answers in each section needed for 8 marks (7+1).');
        expect(practice(card)).toContain('7 marks for one correct answer and 1 additional mark');
        expect(practice(card)).not.toContain('Each earns at most 4');
        if (group.length > 1) {
          for (const q of group) {
            expect(card.questionText).toMatch(new RegExp(`(^|\n)${q}\\. `));
            expect(card.rubric.answerGuide).not.toContain(`Question ${q}:`);
          }
          expect(tasks.find(task => task.cardId === card.id)?.label).toContain(`Q${group[0]} and Q${group[1]}`);
        }
      }
    }
    for (const id of ['ol-reading-a3-q4', 'ol-reading-a4-q5']) {
      expect(card2015(id).totalMarks).toBe(8);
      expect(card2015(id).rubric.taskRequirements.join(' ')).toContain('Any two of the following for 7+1 marks:');
      expect(practice(card2015(id))).toContain('7 marks for one correct answer');
    }
    for (const rc of [1, 2]) {
      const card = card2015(`hl-reading-a${rc}-q6`);
      expect(fullCredit(card)).toHaveLength(13);
      expect(card.rubric.taskRequirements.join(' ')).toContain('higher mark is to be awarded to each segment');
      expect(card.rubric.criteria[0].permittedMarks).toEqual([0, 2, 4, 6, 8, 10]);
    }
    expect(card2015('hl-reading-a2-q4-i').totalMarks).toBe(10);
    expect(practice(card2015('hl-reading-a2-q4-i'))).toContain('not an official correction');
    expect(card2015('hl-reading-a2-q2-ii').rubric.criteria[0].permittedMarks).toEqual([0, 5]);
    for (const [rc, count] of [[3, 9], [4, 10]]) {
      expect(fullCredit(card2015(`ol-reading-a${rc}-q8`))).toHaveLength(count);
      expect(practice(card2015(`ol-reading-a${rc}-q8`))).toContain('scheme says “Accept any one”');
    }
    expect(cards.filter(card => card.year === 2015 && card.questionChoices)).toHaveLength(4);
  });

  it('retains the 2016 instrument pair and restores the omitted source marker', () => {
    expect(card2016('hl-reading-a1-q6').questionText).toMatch(/^Do you think/);
    const pair = card2016('ol-reading-a3-q1');
    expect(pair.totalMarks).toBe(8);
    expect(pair.rubric.criteria[0].permittedMarks).toEqual([0, 1, 2, 3, 4, 5, 6, 7, 8]);
    expect(pair.rubric.taskRequirements.join(' ')).toContain('Penalise extraneous material');
    expect(pair.rubric.answerGuide).toHaveLength(4);
    expect(pair.rubric.answerGuide![0]).toContain('violon');
    expect(pair.rubric.answerGuide![2]).toContain('flûte');
    expect(card2016('ol-reading-a4-q1').rubric.answerGuide!.join(' ')).not.toContain('États-Unis');
    expect(card2016('ol-reading-a4-q2').rubric.answerGuide![0]).toContain('Il vient des États-Unis');
    expect(card2016('ol-reading-a4-q2').schemeRegion?.p).toBe(8);
    expect(card2016('hl-reading-a1-q2-ii').rubric.criteria[0].permittedMarks).toEqual([0, 5]);
    for (const [id, count] of [['hl-reading-a1-q6', 20], ['hl-reading-a2-q6', 13], ['ol-reading-a3-q8', 9], ['ol-reading-a4-q8', 9]] as const) {
      expect(fullCredit(card2016(id))).toHaveLength(count);
    }
    expect(cards.filter(card => card.year === 2016 && card.questionChoices)).toHaveLength(4);
    for (const card of cards.filter(card => card.year === 2016)) expect(card.questionText).not.toMatch(/_{3,}|[\uF000-\uF8FF]/);
    for (const [letter, name] of [['a', 'Microbe et Gasoil'], ['b', 'Le Garçon Invisible'], ['c', 'L’étudiante et M. Henri'], ['d', 'Le Tournoi']]) {
      expect(card2016(`ol-reading-a2-q1-${letter}`).rubric.answerGuide![0]).toContain(name);
    }
  });

  it('resolves 2017 lettered choices and preserves its complete opinion guidance', () => {
    expect(cards.filter(card => card.year === 2017 && card.questionChoices)).toHaveLength(4);
    for (const [id, option, letter, answer] of [
      ['hl-reading-a1-q3-ii', 0, 'a', 'installera des panneaux de signalisation supplémentaires'],
      ['hl-reading-a2-q2-i', 3, 'd', 'Camille pense que Tibor est un garçon sympa.'],
      ['ol-reading-a3-q7', 2, 'c', 'rend souvent visite aux enfants hospitalisés'],
      ['ol-reading-a4-q7', 3, 'd', 'il lui fait la bise deux fois.'],
    ] as const) {
      const card = card2017(id);
      expect(card.questionChoices).toHaveLength(4);
      expect(card.questionChoices![option]).toBe(answer);
      expect(card.rubric.answerGuide![0]).toMatch(new RegExp(`^(• |- )?\\(${letter}\\)( —)? ${card.totalMarks} [Mm]arks$`));
      expect(card.rubric.practiceNotes).toContain(`The scheme’s answer (${letter}) is this option on the paper: “${answer}”`);
    }
    for (const id of ['hl-reading-a1-q5-i', 'hl-reading-a2-q5-ii']) {
      expect(card2017(id).rubric.criteria[0].permittedMarks).toEqual([0, 5]);
    }
    for (const [id, count] of [['hl-reading-a1-q6', 14], ['hl-reading-a2-q6', 23], ['ol-reading-a3-q8', 5], ['ol-reading-a4-q8', 7]] as const) {
      expect(fullCredit(card2017(id))).toHaveLength(count);
    }
    const guide = card2017('hl-reading-a2-q6').rubric.answerGuide!;
    for (const heading of ['Other students not interested:', 'Other students interested:', 'Tibor not interested:', 'Tibor interested:']) expect(guide).toContain(heading);
    expect(guide[0]).toContain('other students exclusively');
    expect(card2017('ol-reading-a2-q3').rubric.criteria[0].permittedMarks).toEqual([0, 1, 2, 3, 4, 5, 6, 7, 8]);
    expect(card2017('ol-reading-a2-q7').rubric.criteria[0].permittedMarks).toEqual([0, 4, 8]);
    for (const card of cards.filter(card => card.year === 2017)) expect(card.questionText).not.toMatch(/_{3,}|[\uF000-\uF8FF]/);
    for (const [rc, parent] of [[1, '1'], [2, '6'], [3, '7'], [4, 'A4']] as const) {
      for (const card of cards.filter(card => card.year === 2017 && card.level === 'ordinary' && card.questionRef.includes(`Section A${rc} `))) {
        expect(tasks.find(task => task.cardId === card.id)?.parent).toBe(parent);
      }
    }
  });

  it('splits the two priced 2018 country responses with their shared stem and partial rules', () => {
    for (const [letter, country, answer] of [['i', 'Au Japon', 'persévérance'], ['ii', 'En France', 'coordination']]) {
      const card = card2018(`ol-reading-a3-q5-${letter}`);
      expect(card.totalMarks).toBe(4);
      expect(card.questionText).toContain('quelles sont les qualités nécessaires pour jouer à ces jeux');
      expect(card.questionText).toContain(country);
      expect(card.rubric.answerGuide).toHaveLength(3);
      expect(card.rubric.answerGuide![0]).toContain(answer);
      expect(card.rubric.answerGuide![1]).toContain('2 qualities 2 marks');
      expect(card.rubric.answerGuide![2]).toContain('1 quality 1 mark');
      expect(card.schemeRegion?.p).toBe(8);
      expect(tasks.find(task => task.cardId === card.id)?.parent).toBe('19');
    }
    expect(card2018('ol-reading-a3-q6').schemeRegion?.p).toBe(9);
    expect(card2018('hl-reading-a1-q3-ii').rubric.criteria[0].permittedMarks).toEqual([0, 5]);
    expect(card2018('hl-reading-a1-q3-ii').rubric.answerGuide!.join(' ')).toContain('Award 5 Marks or 0 Marks');
    expect(card2018('ol-reading-a2-q3').rubric.criteria[0].permittedMarks).toEqual([0, 1, 4, 5, 8]);
    expect(card2018('ol-reading-a2-q6').rubric.criteria[0].permittedMarks).toEqual([0, 2, 3, 4]);
    expect(practice(card2018('ol-reading-a4-q2'))).toContain('at both 4 and 2 marks');
    for (const [id, count] of [['hl-reading-a1-q6', 18], ['hl-reading-a2-q6', 19], ['ol-reading-a3-q8', 7], ['ol-reading-a4-q8', 6]] as const) {
      expect(fullCredit(card2018(id))).toHaveLength(count);
    }
    for (const rc of [3, 4]) {
      expect(card2018(`ol-reading-a${rc}-q8`).rubric.answerGuide!.join(' ')).toContain('Penalise incorrect gender');
    }
    expect(cards.filter(card => card.year === 2018 && card.questionChoices)).toHaveLength(4);
  });

  it('preserves 2019 Roman subparts, all opinion examples and the disclosed tariff conflict', () => {
    const pair = card2019('hl-reading-a2-q3-ii');
    expect(pair.totalMarks).toBe(10);
    expect(pair.questionText).toContain('Donnez deux raisons');
    expect(practice(pair)).toContain('heading prints 5 marks');
    expect(practice(pair)).toContain('not an official correction');
    expect(card2019('hl-reading-a2-q4').totalMarks).toBe(5);
    expect(card2019('hl-reading-a2-q4').rubric.answerGuide).toContain('Correct manipulation required.');
    expect(card2019('hl-reading-a2-q2-ii').rubric.answerGuide!.join(' ')).toContain('full sentence must be given');
    expect(card2019('hl-reading-a2-q5-i').rubric.answerGuide!.join(' ')).toContain('Any extraneous element = 0 Marks');
    expect(fullCredit(card2019('hl-reading-a1-q6'))).toHaveLength(19);
    expect(fullCredit(card2019('hl-reading-a2-q6'))).toHaveLength(30);
    for (const [id, parent] of [['hl-reading-a1-q6', '11'], ['hl-reading-a2-q1-i', '12'], ['hl-reading-a2-q6', '21']]) {
      expect(tasks.find(task => task.cardId === `fr-2019-${id}`)?.parent).toBe(parent);
    }
    for (const card of cards.filter(card => card.year === 2019)) {
      expect(card.questionText).not.toMatch(/_{3,}|[\uF000-\uF8FF]/);
      expect(card.schemeCitation).toContain('general rules p.3');
    }
  });

  it('keeps the 2019 Ordinary answer rates and partial-credit ladders', () => {
    for (const id of ['ol-reading-a1-q6', 'ol-reading-a2-q1', 'ol-reading-a2-q6', 'ol-reading-a3-q2', 'ol-reading-a4-q4']) {
      const card = card2019(id);
      expect(card.totalMarks).toBe(8);
      expect(practice(card)).toContain('2 distinct points. Each earns at most 4 marks');
    }
    expect(card2019('ol-reading-a2-q1').rubric.criteria[0].permittedMarks).toEqual([0, 2, 4, 6, 8]);
    expect(card2019('ol-reading-a2-q3').rubric.criteria[0].permittedMarks).toEqual([0, 1, 4]);
    expect(card2019('ol-reading-a2-q4').rubric.criteria[0].permittedMarks).toEqual([0, 1, 2, 3, 4]);
    expect(card2019('ol-reading-a2-q4').rubric.answerGuide).toHaveLength(7);
    expect(fullCredit(card2019('ol-reading-a3-q8'))).toHaveLength(5);
    expect(fullCredit(card2019('ol-reading-a4-q8'))).toHaveLength(15);
    for (const [letter, answer] of [['a', 'De joie coulent mes larmes'], ['b', 'Adam'], ['c', 'La Maison Abandonnée'], ['d', 'Le Grand Voyage de Figgy']]) {
      const card = card2019(`ol-reading-a1-q1-${letter}`);
      expect(card.totalMarks).toBe(4);
      expect(card.rubric.answerGuide!.join(' ')).toContain(answer);
      expect(tasks.find(task => task.cardId === card.id)?.parent).toBe('A1');
    }
    expect(cards.filter(card => card.year === 2019 && card.questionChoices)).toHaveLength(4);
    for (const [id, option, answer] of [
      ['hl-reading-a1-q2-ii', 1, 'les commerçants offrent des produits récents et périssables'],
      ['hl-reading-a2-q3-i', 3, 'a été accueillie chaleureusement par Justine'],
      ['ol-reading-a3-q7', 3, 'ne donne jamais son avis sur les histoires'],
      ['ol-reading-a4-q7', 0, 'est retournée à l’apartement'],
    ] as const) {
      expect(card2019(id).questionChoices?.[option]).toBe(answer);
    }
  });

  it('uses 2020’s two-mark and twelve-mark tasks with their full ladders', () => {
    for (const id of ['ol-reading-a2-q1', 'ol-reading-a2-q3']) {
      expect(card2020(id).totalMarks).toBe(2);
      expect(card2020(id).rubric.criteria[0].permittedMarks).toEqual([0, 2]);
    }
    const twelve = card2020('ol-reading-a2-q8');
    expect(twelve.totalMarks).toBe(12);
    expect(twelve.rubric.criteria[0].permittedMarks).toEqual([0, 3, 6, 9, 12]);
    expect(practice(twelve)).toContain('2 distinct points. Each earns at most 6 marks');
    expect(twelve.rubric.answerGuide!.join(' ')).toContain('clothes — 3 Marks');
    expect(card2020('ol-reading-a1-q2').rubric.criteria[0].permittedMarks).toEqual([0, 1, 2, 3, 4]);
    expect(card2020('ol-reading-a3-q6').totalMarks).toBe(4);
    expect(card2020('ol-reading-a3-q6').rubric.answerGuide!.join(' ')).toContain('ONE theme — 2 Marks');
    expect(card2020('hl-reading-a2-q5-b').rubric.answerGuide).toContain('Direct quotation required.');
    expect(card2020('hl-reading-a1-q5-a').rubric.answerGuide!.join(' ')).toContain('Any extraneous element = 0 Marks');
    expect(fullCredit(card2020('hl-reading-a1-q6'))).toHaveLength(19);
    expect(fullCredit(card2020('hl-reading-a2-q6'))).toHaveLength(22);
    expect(cards.filter(card => card.year === 2020 && card.questionChoices)).toHaveLength(4);
    for (const [letter, answer] of [['a', 'Antoine'], ['b', 'Maxime'], ['c', 'Shadi'], ['d', 'Richalda']]) {
      const card = card2020(`ol-reading-a1-q1-${letter}`);
      expect(card.totalMarks).toBe(4);
      expect(card.questionText).not.toContain('::');
      expect(card.rubric.answerGuide!.join(' ')).toContain(answer);
    }
  });

  it('discloses both 2020 tariff conflicts and files the magazine extracts consistently', () => {
    for (const [id, page] of [['ol-reading-a3-q5', 8], ['ol-reading-a4-q6', 10]] as const) {
      const card = card2020(id);
      expect(card.totalMarks).toBe(8);
      expect(card.schemeRegion?.p).toBe(page);
      expect(practice(card)).toContain('Source discrepancy: the heading prints 4 marks');
      expect(practice(card)).toContain('not an official correction');
    }
    for (const card of cards.filter(card => card.year === 2020 && card.level === 'ordinary' && /Section A[12] /.test(card.questionRef))) {
      const task = tasks.find(task => task.cardId === card.id)!;
      expect(card.topicId).toBe('french-5-3');
      for (const n of [task.n, task.parent]) {
        expect(examTopicIdsForQuestion('french', 'ordinary', 2020, 'main', n, 'single', 'ev', task.fileid))
          .toEqual(['french-ordinary-reading-comprehension-other-website-magazine-extracts']);
      }
    }
  });

  it('keeps 2022’s nine-question second comprehension and complete partial credit', () => {
    const old = JSON.parse(fs.readFileSync('scripts/markbank/authored/french.json', 'utf8'))
      .filter((card: { year: number; section: string }) => card.year === 2022 && card.section === 'A');
    expect(old).toHaveLength(53);
    for (const card of old) expect(cards.some(current => current.id === card.id)).toBe(true);
    for (const [id, parent] of [['ol-a2-9', '15'], ['ol-a3-1', '16'], ['ol-a4-1', '24']]) {
      expect(tasks.find(task => task.cardId === `fr-2022-${id}`)?.parent).toBe(parent);
    }
    expect(card2022('ol-a2-8').rubric.criteria[0].permittedMarks).toEqual([0, 1, 2, 4]);
    expect(card2022('ol-a3-3').rubric.answerGuide!.join(' ')).toContain('• (des) jeux video — 1 Mark');
    expect(card2022('ol-a3-4').totalMarks).toBe(4);
    expect(card2022('ol-a3-4').rubric.answerGuide!.join(' ')).toContain('gratin');
    expect(card2022('hl-a1-5-b').rubric.answerGuide!.join(' ')).toContain('(Whole sentence) = minus 2 Marks');
    expect(fullCredit(card2022('hl-a1-6'))).toHaveLength(15);
    expect(fullCredit(card2022('hl-a2-6'))).toHaveLength(16);
    for (const [id, answer] of [
      ['ol-a1-1-a', 'Benazir'], ['ol-reading-a1-q1-b', 'Samia'],
      ['ol-reading-a1-q1-c', 'Adil'], ['ol-reading-a1-q1-d', 'Joana'],
    ]) {
      expect(card2022(id).totalMarks).toBe(4);
      expect(card2022(id).rubric.answerGuide!.join(' ')).toContain(answer);
    }
    expect(cards.filter(card => card.year === 2022 && card.questionChoices)).toHaveLength(4);
  });

  it('restores 2021 full-credit Symbol-font bullets and all examiner notes', () => {
    const old = JSON.parse(fs.readFileSync('scripts/markbank/authored/french.json', 'utf8'))
      .filter((card: { year: number; section: string }) => card.year === 2021 && card.section === 'A');
    expect(old).toHaveLength(50);
    for (const card of old) expect(cards.some(current => current.id === card.id)).toBe(true);
    expect(card2021('hl-a1-1-a').rubric.answerGuide!.join(' ')).toContain('la fermeture des écoles');
    expect(fullCredit(card2021('hl-a1-1-a'))).toHaveLength(1);
    expect(card2021('hl-a1-2-a').rubric.answerGuide!.join(' ')).toContain('Full sentence is acceptable');
    expect(card2021('hl-a1-2-b').rubric.answerGuide!.join(' ')).toContain('Accept Present Tense');
    expect(card2021('hl-a2-2-a').rubric.answerGuide!.join(' ')).toContain('If on peut omitted, Minus 2 Marks');
    expect(card2021('hl-a2-4-a').rubric.answerGuide!.join(' ')).toContain('Any extraneous element = 0 Marks');
    expect(card2021('hl-a2-6').questionText).toMatch(/^The portrayal of two people/);
    expect(fullCredit(card2021('hl-a1-6'))).toHaveLength(18);
    expect(fullCredit(card2021('hl-a2-6'))).toHaveLength(27);
    expect(card2021('ol-a4-5').rubric.answerGuide!.join(' ')).toContain('Full sentence 2 Marks');
    for (const [id, answer] of [
      ['ol-a2-1-a', 'Djamila'], ['ol-reading-a2-q1-b', 'Loïc'],
      ['ol-reading-a2-q1-c', 'Anaïs'], ['ol-reading-a2-q1-d', 'Manu'],
    ]) {
      const card = card2021(id);
      expect(card.totalMarks).toBe(4);
      expect(card.rubric.answerGuide!.join(' ')).toContain(answer);
      expect(tasks.find(task => task.cardId === card.id)?.parent).toBe('9');
    }
    expect(cards.filter(card => card.year === 2021 && card.questionChoices)).toHaveLength(4);
  });

  it('restores the last two excluded 2021 tasks with the source discrepancy disclosed', () => {
    for (const [id, page, examples] of [['ol-reading-a3-q5', 8, 10], ['ol-reading-a4-q3', 10, 5]] as const) {
      const card = card2021(id);
      expect(card.totalMarks).toBe(8);
      expect(card.schemeRegion?.p).toBe(page);
      expect(practice(card)).toContain('Source discrepancy: the heading prints 4 marks');
      expect(practice(card)).toContain('not an official correction');
      expect(practice(card)).toContain('2 distinct points. Each earns at most 4 marks');
      expect(card.rubric.criteria[0].permittedMarks).toEqual([0, 1, 2, 3, 4, 5, 6, 7, 8]);
      expect(fullCredit(card)).toHaveLength(examples);
    }
    expect(JSON.parse(fs.readFileSync('scripts/markbank/authoring/exclusions/french.json', 'utf8'))).toEqual([]);
  });

  it('uses readable punctuation for PDF Symbol-font note markers', () => {
    for (const card of cards) {
      expect(card.rubric.answerGuide!.join(' '), card.id).not.toMatch(/[\uF000-\uF8FF]/);
    }
  });

  it('restores all 2023 guidance while preserving its 52 original reading identities', () => {
    const old = JSON.parse(fs.readFileSync('scripts/markbank/authored/french.json', 'utf8'))
      .filter((card: { year: number; section: string }) => card.year === 2023 && card.section === 'A');
    expect(old).toHaveLength(52);
    for (const card of old) expect(cards.some(current => current.id === card.id)).toBe(true);
    expect(card2023('hl-a1-6').questionText).toMatch(/^In the text, a strong case/);
    expect(fullCredit(card2023('hl-a1-6'))).toHaveLength(18);
    expect(fullCredit(card2023('hl-a2-6'))).toHaveLength(12);
    expect(card2023('hl-a1-4-a').totalMarks).toBe(5);
    expect(card2023('hl-a1-4-a').rubric.answerGuide!.join(' ')).toContain('One correct point = 4 Marks');
    expect(card2023('hl-a2-3-a').rubric.answerGuide!.join(' ')).toContain('Omission of ordinaires = minus 1 Mark');
    expect(card2023('hl-a2-5-b').rubric.answerGuide!.join(' ')).toContain('Inclusion of À voir');
    expect(card2023('ol-a3-6').rubric.answerGuide).toContain('- 1 item — 1 Mark');
    expect(card2023('ol-a1-6').rubric.criteria[0].permittedMarks).toEqual([0, 3, 4]);
    for (const [id, answer] of [
      ['ol-a1-1-a', 'Victor'], ['ol-reading-a1-q1-b', 'Nathan'],
      ['ol-reading-a1-q1-c', 'Aline'], ['ol-reading-a1-q1-d', 'Mathilde'],
    ]) {
      const card = card2023(id);
      expect(card.totalMarks).toBe(4);
      expect(card.rubric.criteria[0].permittedMarks).toEqual([0, 4]);
      expect(card.rubric.answerGuide!.join(' ')).toContain(answer);
    }
  });

  it('keeps all four 2023 single-choice tasks at their published tariffs', () => {
    for (const [id, answer, maximum] of [
      ['hl-a1-3-b', 'est conscient des frais de vacances', 5],
      ['hl-a2-2-a', 'rend des lettres à la poste après sa sieste', 5],
      ['ol-a3-7', 'tous les vêtements qu’elle dessine', 4],
      ['ol-a4-7', 'jouait au rugby avec ses voisins', 4],
    ] as const) {
      const card = card2023(id);
      expect(card.questionChoices).toHaveLength(4);
      expect(card.questionChoices).toContain(answer);
      expect(card.rubric.criteria[0].permittedMarks).toEqual([0, maximum]);
      expect(card.rubric.answerGuide!.join(' ')).toMatch(/more than one answer offered.*0 Marks/);
    }
  });

  it('corrects all four 2023 Ordinary passage types in both products', () => {
    for (const [rc, index, slug] of [
      [1, 3, 'other-website-magazine-extracts'], [2, 3, 'other-website-magazine-extracts'],
      [3, 2, 'interview'], [4, 1, 'book-extract'],
    ] as const) {
      const group = cards.filter(card => card.year === 2023 && card.level === 'ordinary' && card.questionRef.includes(`Section A${rc} `));
      expect(group.length).toBeGreaterThan(0);
      for (const card of group) {
        expect(card.topicId).toBe(`french-5-${index}`);
        const task = tasks.find(task => task.cardId === card.id)!;
        const ids = [`french-ordinary-reading-comprehension-${slug}`];
        expect(task.topicIds).toEqual(ids);
        for (const n of [task.n, task.parent]) {
          expect(examTopicIdsForQuestion('french', 'ordinary', 2023, 'main', n, 'single', 'ev', task.fileid)).toEqual(ids);
        }
      }
    }
  });

  it('restores all three excluded 2024 tasks with a visible source discrepancy', () => {
    for (const [id, answer, page] of [
      ['ol-reading-a2-q2', 'To be motivated', 7],
      ['ol-reading-a3-q7', 'Elle lit plus', 10],
      ['ol-reading-a4-q5', 'Il a fini ses devoirs avant le dîner', 12],
    ] as const) {
      const card = card2024(id);
      expect(card.totalMarks).toBe(8);
      expect(card.schemeRegion?.p).toBe(page);
      expect(practice(card)).toContain('Source discrepancy: the heading prints 4 marks');
      expect(practice(card)).toContain('not an official correction');
      expect(practice(card)).toContain('2 distinct points. Each earns at most 4 marks');
      expect(card.rubric.answerGuide!.join(' ')).toContain(answer);
    }
    expect(card2024('ol-reading-a2-q2').rubric.criteria[0].permittedMarks).toEqual([0, 2, 4, 6, 8]);
    expect(card2024('ol-a1-7').totalMarks).toBe(4);
    expect(practice(card2024('ol-a1-7'))).toContain('2 distinct points. Each earns at most 2 marks');
    expect(card2024('ol-a1-7').rubric.criteria[0].permittedMarks).toEqual([0, 1, 2, 3, 4]);
    const excluded = JSON.parse(fs.readFileSync('scripts/markbank/authoring/exclusions/french.json', 'utf8'));
    expect(excluded.some((entry: { ref: string }) => entry.ref.startsWith('2024 '))).toBe(false);
  });

  it('preserves 2024 identities and uses its actual archive numbering for the name matches', () => {
    const old = JSON.parse(fs.readFileSync('scripts/markbank/authored/french.json', 'utf8'))
      .filter((card: { year: number; section: string }) => card.year === 2024 && card.section === 'A');
    expect(old).toHaveLength(49);
    for (const card of old) expect(cards.some(current => current.id === card.id)).toBe(true);
    for (const [id, answer] of [
      ['ol-a2-1-a', 'Xavier'], ['ol-reading-a2-q1-b', 'Saïda'],
      ['ol-reading-a2-q1-c', 'Olivier'], ['ol-reading-a2-q1-d', 'Carmelle'],
    ]) {
      const card = card2024(id);
      expect(card.totalMarks).toBe(4);
      expect(card.rubric.answerGuide!.join(' ')).toContain(answer);
      expect(tasks.find(task => task.cardId === card.id)?.parent).toBe('9');
    }
    expect(tasks.find(task => task.cardId === 'fr-2024-ol-reading-a2-q2')?.parent).toBe('10');
    expect(card2024('ol-a3-1').topicId).toBe('french-5-3');
    expect(fullCredit(card2024('hl-a1-6'))).toHaveLength(19);
    expect(fullCredit(card2024('hl-a2-6'))).toHaveLength(18);
    expect(card2024('hl-a2-1-b').rubric.answerGuide!.join(' ')).toContain('Inclusion of Alors = minus 1 Mark');
    expect(cards.filter(card => card.year === 2024 && card.questionChoices)).toHaveLength(4);
  });

  it('corrects the 2025 tasks in place and splits each published name match', () => {
    const original = JSON.parse(fs.readFileSync('scripts/markbank/authored/french.json', 'utf8'))
      .filter((card: { year: number; section: string }) => card.year === 2025 && card.section === 'A');
    expect(original).toHaveLength(52);
    for (const old of original) {
      const corrected = cards.find(card => card.id === old.id)!;
      expect(corrected, old.id).toBeDefined();
      expect(corrected.conceptId).toBe(old.conceptId);
      expect(corrected.totalMarks).toBe(old.id === 'fr-2025-ol-a1-1-a' ? 4 : old.totalMarks);
      expect([...higher, ...ordinary].filter(card => card.id === old.id)).toHaveLength(1);
    }
    for (const [id, prompt, answer] of [
      ['ol-a1-1-a', 'buys clothes online', 'Marie'],
      ['ol-reading-a1-q1-b', 'says that we shouldn’t neglect fashion', 'Nadine'],
      ['ol-reading-a1-q1-c', 'thinks clothes express our creative side', 'Bruno'],
      ['ol-reading-a1-q1-d', 'thinks we should buy fewer clothes', 'Julien'],
    ]) {
      const card = legacy(id);
      expect(card.questionText).toBe(`Write the name of the person who\n\n${prompt}`);
      expect(card.totalMarks).toBe(4);
      expect(card.rubric.answerGuide).toEqual([`• ${prompt} – ${answer} — 4 Marks`]);
      expect(card.rubric.criteria[0].permittedMarks).toEqual([0, 4]);
    }
  });

  it('restores the full 2025 ladders, opinion evidence and unbulleted answer list', () => {
    const scout = legacy('hl-a1-6');
    expect(scout.questionText).toMatch(/^Scouting has become attractive/);
    expect(fullCredit(scout)).toHaveLength(22);
    expect(fullCredit(legacy('hl-a2-6'))).toHaveLength(16);
    expect(legacy('hl-a1-5-b').rubric.answerGuide!.filter(line => line.startsWith('-'))).toHaveLength(10);
    expect(legacy('ol-a4-5').rubric.answerGuide).toEqual([
      'Voir / (S’)amuser / Descendre / (Se) laisser / Porter / Ramer/ Être',
      'Note: Minus 1 mark for each extraneous element',
    ]);
    expect(legacy('ol-a2-3').rubric.answerGuide).toContain('- (Passion for) food — 1 Mark');
    expect(legacy('ol-a2-3').rubric.criteria[0].permittedMarks).toEqual([0, 1, 2, 4]);
    expect(legacy('ol-a3-2').totalMarks).toBe(4);
    expect(legacy('ol-a3-2').rubric.answerGuide).toHaveLength(3);
    expect(legacy('hl-a2-5-a').rubric.answerGuide).toContain('Correct manipulation required.');
  });

  it('preserves the four 2025 multiple-choice tasks without revealing answers', () => {
    for (const [id, answer, maximum] of [
      ['hl-a1-3-a', 'permet aux jeunes d’être dans la nature.', 5],
      ['hl-a2-3-b', 'lui a indiqué son logement', 5],
      ['ol-a3-6', 'fatigué', 4], ['ol-a4-7', 'sur une île', 4],
    ] as const) {
      const card = legacy(id);
      expect(card.questionChoices).toHaveLength(4);
      expect(card.questionChoices).toContain(answer);
      expect(card.questionText).not.toMatch(/correct|answer offered/);
      expect(card.rubric.criteria[0].permittedMarks).toEqual([0, maximum]);
      expect(card.rubric.answerGuide!.join(' ')).toMatch(/more than one answer offered.*0 Marks/);
    }
  });

  it('allows published excess-material deductions on Ordinary opinion responses', () => {
    for (const card of [legacy('ol-a3-8'), legacy('ol-a4-8'), byId('ol-reading-a3-q8'), byId('ol-reading-a4-q8')]) {
      expect(card.rubric.taskRequirements).toContain('Penalise extraneous material to a maximum of 2 marks.');
      expect(card.rubric.answerGuide![0]).toMatch(/Award 2 marks if answer is partially correct/i);
      expect(card.rubric.criteria[0].permittedMarks).toEqual([0, 1, 2, 3, 4, 5, 6, 7, 8]);
      // The points are rows now: one at its full mark and one at the partial mark the scheme prints.
      expect(frenchMarks(card, { [frenchRowScoreId('r1')]: 4, [frenchRowScoreId('r2')]: 2 })).toBe(6);
    }
  });

  it('files the 2025 Étienne novel extract under book extracts in both products', () => {
    const topicIds = ['french-ordinary-reading-comprehension-book-extract'];
    for (let item = 1; item <= 8; item += 1) {
      const card = legacy(`ol-a4-${item}`);
      expect(card.topicId).toBe('french-5-1');
      const task = tasks.find(task => task.cardId === card.id)!;
      expect(task.topicIds).toEqual(topicIds);
      for (const n of [task.n, task.parent]) {
        expect(examTopicIdsForQuestion('french', 'ordinary', 2025, 'main', n, 'single', 'ev', task.fileid)).toEqual(topicIds);
      }
    }
  });

  it('splits the four name-matching tasks without sharing their answers', () => {
    for (const [letter, prompt, answer] of [
      ['a', 'studying in England', 'Vanessa'], ['b', 'taking a year out', 'Léon'],
      ['c', 'doing an apprenticeship', 'Fatima'], ['d', 'buying a car', 'Yoann'],
    ]) {
      const card = byId(`ol-reading-a1-q1-${letter}`);
      expect(card.questionText).toBe(`Write the name of the person who talks about\n\n${prompt}`);
      expect(card.totalMarks).toBe(4);
      expect(card.rubric.answerGuide).toEqual([`• ${prompt} – ${answer} — 4 Marks`]);
      expect(card.rubric.criteria[0].permittedMarks).toEqual([0, 4]);
    }
  });

  it('keeps all four MCQ options and the scheme’s all-or-nothing rule', () => {
    for (const [suffix, answer, mark] of [
      ['hl-reading-a1-q4-b', 'les jeunes se sentent sous pression de voyager en avion', 5],
      ['hl-reading-a2-q5-b', 'va décider entre les deux candidats', 5],
      ['ol-reading-a3-q6', 'finir le Vendée Globe', 4],
      ['ol-reading-a4-q6', 'Son père', 4],
    ] as const) {
      const card = byId(suffix);
      expect(card.questionText.split('\n')).toHaveLength(5);
      expect(card.questionChoices).toEqual(card.questionText.split('\n').slice(1));
      expect(card.questionText).toContain(answer);
      expect(card.rubric.answerGuide?.join(' ')).toContain(answer);
      expect(card.rubric.answerGuide?.join(' ')).toMatch(/more than one answer offered.*0 Marks/);
      expect(card.rubric.criteria[0].permittedMarks).toEqual([0, mark]);
      expect(frenchMarks(card, { 'french:response': mark - 1 })).toBe(0);
    }
  });

  it('retains the full ladders, open opinion evidence and manipulation rules', () => {
    const ladder = byId('hl-reading-a2-q2-a').rubric.answerGuide!;
    expect(ladder.filter(line => line.startsWith('-'))).toHaveLength(16);
    expect(ladder.at(-1)).toContain('elle y est souvent allée en vacances');
    const opinion = byId('hl-reading-a1-q6');
    expect(fullCredit(opinion)).toHaveLength(20);
    expect(opinion.rubric.answerGuide).toContain('Agree:');
    expect(opinion.rubric.answerGuide).toContain('Disagree:');
    expect(practice(opinion)).toContain('2 distinct points');
    expect(byId('hl-reading-a2-q3-a').totalMarks).toBe(5);
    expect(byId('hl-reading-a2-q3-a').rubric.answerGuide).toContain('Correct manipulation required.');
    expect(byId('ol-reading-a1-q5').totalMarks).toBe(4);
    expect(byId('ol-reading-a1-q5').rubric.answerGuide).toHaveLength(3);
    expect(byId('ol-reading-a1-q4').rubric.answerGuide).toContain('An indication of the future tense in the second answer is required to gain marks.');
    expect(byId('ol-reading-a3-q8').rubric.answerGuide![0]).toContain('Award 2 marks if answer is partially correct.');
  });

  it('binds every task to its full passage, published scheme and exact Atlas topic', () => {
    for (const card of cards) {
      const task = tasks.find(task => task.cardId === card.id)!;
      const paper = topicsForPaper('french', card.year, card.level, 'ev', `${card.paperFileid}.pdf`)!;
      const question = paper.q.find(question => question.n === task.n)!;
      expect(tariffReconciles(card), card.id).toBe(true);
      expect(browseTopicIdsForQuestion(paper, question), card.id).toEqual(task.topicIds);
      expect(examTopicIdsForQuestion('french', card.level, card.year, 'main', task.n, 'single', 'ev', task.fileid)).toEqual(task.topicIds);
      expect(task.topicIds.flatMap(curriculumNodeIdsForExamTopic), card.id).toContain(card.topicId);
      const map = JSON.parse(fs.readFileSync(`public/paper-anchors/${card.year}/${task.fileid}.json`, 'utf8'));
      expect(paperRegionFor(map.q, task.n, map.maxCropPages)?.map(region => region.p), card.id).toEqual(task.pages);
      expect(card.sourceMaterial!.pages, card.id).toEqual(task.pages);
      expect(task.pages).toHaveLength(2);
      expect(card.rubric.answerGuide!.length, card.id).toBeGreaterThan(0);
    }
  });
});
