import { describe, expect, it } from 'vitest';
import fs from 'node:fs';
import { FRENCH_WRITING_CARDS as cards } from '../components/MarkBank/cards/french/writing';
import { CARDS as higher } from '../components/MarkBank/cards/french/higher';
import { CARDS as ordinary } from '../components/MarkBank/cards/french/ordinary';
import legacy from '../scripts/markbank/authored/french.json';
import tasks from '../data/examTopics/french-reviewed-tasks.json';
import sources from '../scripts/markbank/authoring/french-writing-sources.json';
import readingReview from '../scripts/markbank/authoring/french-reading-review.json';
import { tariffReconciles } from '../types/markBank';
import { examTopicIdsForQuestion, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { topicsForPaper, browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { paperRegionFor } from '../components/PaperTrail/paperRegion';
import { frenchMarks, frenchScoreId, FRENCH_ATTEMPT_ID } from '../components/MarkBank/frenchRubric';

const deck = [...higher, ...ordinary];
const correctedReadingIds = new Set(readingReview.papers.flatMap(paper => Object.values(paper.preservedCardIds ?? {})));

describe('reviewed 2010–2026 French writing tasks', () => {
  it('adds all 306 reviewed units while preserving the 260 existing identities', () => {
    expect(cards).toHaveLength(306);
    expect(cards.filter(card => card.level === 'higher')).toHaveLength(136);
    expect(cards.filter(card => card.level === 'ordinary')).toHaveLength(170);
    expect(deck).toHaveLength(2120);
    expect(new Set(deck.map(card => card.id)).size).toBe(deck.length);
    for (const old of legacy) {
      const live = deck.find(card => card.id === old.id)!;
      expect(live, old.id).toBeDefined();
      if (!correctedReadingIds.has(old.id)) {
        expect(live.questionText, old.id).toBe(old.questionText);
        expect(live.totalMarks, old.id).toBe(old.totalMarks);
      }
      const review = readingReview.papers.find(paper => Object.values(paper.preservedCardIds ?? {}).includes(old.id));
      const comprehension = old.questionRef.match(/Section A(\d)/)?.[1];
      const correction = comprehension && review && 'topicCorrections' in review
        ? (review.topicCorrections as Record<string, { topicId: string }> | undefined)?.[comprehension]
        : undefined;
      expect(live.topicId, old.id).toBe(correction?.topicId ?? old.topicId);
    }
  });

  it.each([2021, 2022, 2023, 2024, 2025, 2026].flatMap(year => ['B2A', 'B2B', 'B3A', 'B3B'].map(parent => [year, parent] as const)))('publishes %s %s as one card with every printed point', (year, parent) => {
    // The student chooses which three of the five printed points to include:
    // one card, never one card per combination.
    const variants = tasks.filter(task => task.parent === parent && task.level === 'ordinary' && task.year === year);
    expect(variants.map(task => task.n)).toEqual([parent]);
    const card = cards.find(card => card.id === variants[0].cardId)!;
    expect(card.id).toBe(`fr-${year}-ol-writing-${parent.toLowerCase()}`);
    expect(card.questionRef).toBe(`${year} OL Section B Q${parent[1]}(${parent[2].toLowerCase()})`);
    expect(card.totalMarks).toBe(30);
    const pool = sources.find(source => source.year === year)!.pools.find(pool => pool[0] === parent)!;
    const points = pool[4] as string[];
    const answers = pool[5] as string[];
    expect(card.questionText.match(/• /g)).toHaveLength(5);
    for (const point of points) expect(card.questionText).toContain(`• ${point}`);
    const instruction = card.rubric.taskRequirements.find(line => line.includes('three of the following'))!;
    expect(instruction, card.id).toBeDefined();
    expect(card.questionText.split('\n\n')[0]).toContain(instruction);
    const communication = card.rubric.criteria.filter(c => c.id.startsWith('communication-'));
    expect(communication.map(c => c.label)).toEqual(['first', 'second', 'third'].map(ordinal => `Communication · ${ordinal} point you chose`));
    for (const criterion of communication) {
      expect(criterion.guidance.slice(0, 5)).toEqual(points.map((point, index) => `${point} — ${answers[index]}`));
    }
    expect(card.rubric.criteria.at(-1)?.id).toBe('language');
    expect(card.rubric.practiceNotes![0]).toBe('Choose any three of the five printed points. Each Communication mark is for one point you chose; one point cannot earn two of them.');
  });

  it.each([2021, 2022, 2023, 2024, 2025, 2026])('keeps %s form fields and publishes its four printed questions as one choose-three card', year => {
    const form = tasks.filter(task => task.parent === 'B1B' && task.level === 'ordinary' && task.year === year);
    expect(form.filter(task => task.n.includes('-field-')).map(task => cards.find(card => card.id === task.cardId)!.totalMarks))
      .toEqual([2, 2, 2, 2, 2]);
    expect(form.filter(task => task.n.includes('-route-')).map(task => task.n)).toEqual(['B1B-route-6789']);
    const card = cards.find(card => card.id === `fr-${year}-ol-writing-b1b-route-6789`)!;
    expect(card.totalMarks).toBe(20);
    expect(card.questionText.match(/^[6-9]\. /gm)).toHaveLength(4);
    expect(card.rubric.criteria.map(c => [c.id, c.maxMarks])).toEqual([
      ['communication-first', 4], ['communication-second', 4], ['communication-third', 4], ['language', 8],
    ]);
    for (const criterion of card.rubric.criteria.slice(0, 3)) {
      expect(criterion.guidance.slice(0, 4)).toEqual(card.questionText.split('\n').filter(line => /^[6-9]\. /.test(line)));
    }
  });

  it('refuses route siblings: two cards of one printed task that differ only in the points they show', () => {
    // Same paper and question, the same rubric shape, the same printed stem:
    // the student's choice of points must be one card, not one per combination.
    const shape = (card: { totalMarks: number; rubric?: unknown }) => {
      const criteria = (card.rubric as { criteria?: { maxMarks: number; permittedMarks: number[] }[] } | undefined)?.criteria ?? [];
      return JSON.stringify([card.totalMarks, criteria.map(c => [c.maxMarks, c.permittedMarks])]);
    };
    const isPoint = (line: string) => /^(?:• |[6-9]\. )/.test(line);
    const siblings = (pool: typeof deck) => {
      const groups = new Map<string, typeof deck>();
      for (const card of pool) {
        const key = [card.paperFileid, card.questionRef.replace(/ · points [\d, ]+$/, ''), shape(card),
          (card.questionText ?? '').split('\n').filter(line => !isPoint(line)).join('\n')].join('|');
        groups.set(key, [...(groups.get(key) ?? []), card]);
      }
      return [...groups.values()].filter(group => group.length > 1
        && new Set(group.map(card => (card.questionText ?? '').split('\n').filter(isPoint).join('\n'))).size > 1);
    };
    expect(siblings(deck).map(group => group.map(card => card.id))).toEqual([]);
    // The guard does refuse the old layout: two routes of the 2021 message.
    const card = cards.find(card => card.id === 'fr-2021-ol-writing-b2a')!;
    const lines = card.questionText.split('\n');
    const route = (keep: number[], suffix: string) => ({
      ...card, id: `${card.id}-route-${suffix}`, questionRef: `${card.questionRef} · points ${keep.join(', ')}`,
      questionText: lines.filter(line => !isPoint(line) || keep.includes(lines.filter(isPoint).indexOf(line) + 1)).join('\n'),
    });
    expect(siblings([route([1, 2, 3], '123'), route([1, 2, 4], '124')])).toHaveLength(1);
  });

  it('uses complete published grids, source documents and the same exact topic in Atlas', () => {
    for (const card of cards) {
      expect(tariffReconciles(card), card.id).toBe(true);
      const task = tasks.find(task => task.cardId === card.id)!;
      expect(task, card.id).toBeDefined();
      const paper = topicsForPaper('french', card.year, card.level, 'ev', `${card.paperFileid}.pdf`)!;
      const question = paper.q.find(q => q.n === task.n)!;
      expect(question, card.id).toBeDefined();
      expect(browseTopicIdsForQuestion(paper, question), card.id).toEqual(task.topicIds);
      expect(examTopicIdsForQuestion('french', card.level, card.year, 'main', task.n, 'single', 'ev', task.fileid))
        .toEqual(task.topicIds);
      expect(task.topicIds.flatMap(curriculumNodeIdsForExamTopic), card.id).toContain(card.topicId);
      const map = JSON.parse(fs.readFileSync(`public/paper-anchors/${card.year}/${task.fileid}.json`, 'utf8'));
      expect(paperRegionFor(map.q, task.n, map.maxCropPages)?.map(region => region.p), card.id).toEqual(task.pages);
      expect(card.sourceMaterial?.pages.length, card.id).toBeGreaterThan(0);
      expect(card.schemeRegion?.p, card.id).toBeGreaterThan(0);
    }
  });

  it('lifts each year’s printed communication tariff line rather than one shared paraphrase', () => {
    // 2010–2021 schemes print "Two points" on every task; from 2022 the message and
    // postcard (B2A/B2B) print "Two parts" while the diary and letter keep "Two points".
    const seen = new Map<string, number>();
    for (const card of cards.filter(card => /-ol-writing-b[23][ab](?:-route-|$)/.test(card.id))) {
      const task = card.id.split('-writing-')[1].split('-route-')[0];
      const word = card.year >= 2022 && ['b2a', 'b2b'].includes(task) ? 'parts' : 'points';
      // Printed without a closing stop.
      const tariff = task === 'b3b' ? '4 marks (2 + 2)' : '5 marks (3 + 2)';
      for (const criterion of card.rubric.criteria.filter(c => c.id.startsWith('communication-'))) {
        expect(criterion.guidance.find(line => line.includes('required for'))).toBe(`Two ${word} required for ${tariff}`);
        seen.set(word, (seen.get(word) ?? 0) + 1);
      }
    }
    expect(Object.fromEntries(seen)).toEqual({ points: 174, parts: 30 });
  });

  it('keeps the 2015 email, boxed quotation and task-specific language descriptors', () => {
    const group = cards.filter(card => card.year === 2015);
    expect(group).toHaveLength(18);
    const email = group.find(card => card.id === 'fr-2015-hl-writing-b2b')!;
    expect(email.questionText.match(/• /g)).toHaveLength(3);
    expect(email.questionText).toContain('la cuisine, l’art, le cinéma');
    expect(email.questionText).toContain('Matthieu');
    const quote = group.find(card => card.id === 'fr-2015-hl-writing-b3b')!;
    expect(quote.questionText).toContain('Béatrice, 17 ans');
    expect(quote.questionText).toContain('ils apprécieraient la valeur de l’argent');
    expect(quote.questionText).toContain('Êtes-vous d’accord');
    const form = group.find(card => card.id === 'fr-2015-ol-writing-b1b-route-6789')!;
    expect(form.rubric.criteria.at(-1)?.bands?.[1].guidance).toContain('some sense of register');
    for (const parent of ['b2a', 'b2b', 'b3a']) {
      const task = group.find(card => card.id === `fr-2015-ol-writing-${parent}-route-123`)!;
      expect(task.rubric.criteria.at(-1)?.bands?.[1].guidance).toEqual([
        'reasonable to good range of vocabulary',
        'verb endings, tenses, agreements correct more often than incorrect',
        'at least half the words spelt correctly',
      ]);
    }
    const field = group.find(card => card.id === 'fr-2015-ol-writing-b1b-field-5')!;
    expect(field.rubric.criteria[0].guidance).toEqual(['Level of French – accept any level']);
    expect(field.rubric.taskRequirements).toEqual([]);
  });

  it('shows only SEC printed wording in the scheme panel and keeps our guidance in practice notes', () => {
    const written = /Assess how clearly|message not clear\. 3: message clear|^France not necessary in address\.$|^Write in French|^Answer in French|^Answer (?:all four|the three)|^Use the formal letter layout|Use the published descriptors|^Source discrepancy/;
    for (const card of cards) {
      const scheme = [...card.rubric.taskRequirements, ...card.rubric.criteria.flatMap(c => [...c.guidance, ...(c.bands ?? []).flatMap(b => b.guidance)])];
      for (const text of scheme) expect(text, card.id).not.toMatch(written);
      expect(card.rubric.markingGuideNote, card.id).toBe('');
      expect(card.rubric.practiceNotes?.at(-1), card.id).toBe('Use the published descriptors to place the response you wrote. The marks apply to this selected task; alternative routes are not added together.');
    }
    const byId = (id: string) => cards.find(card => card.id === id)!;
    const message = byId('fr-2014-ol-writing-b2a-route-123');
    expect(message.rubric.taskRequirements).toEqual(['Rédigez vos réponses en français.', 'Ignore layout.']);
    expect(message.rubric.criteria[0].guidance.slice(-2)).toEqual(['1st Category - message not clear.', '2nd Category - message clear.']);
    expect(byId('fr-2014-ol-writing-b3a-route-123').rubric.taskRequirements).toEqual(['Rédigez vos réponses en français.', 'No marks for layout.']);
    const letter = byId('fr-2014-ol-writing-b3b-route-123');
    expect(letter.rubric.criteria[0].guidance[0]).toBe('Top of page - 3 marks (France not necessary in address)');
    expect(letter.rubric.criteria.find(c => c.id === 'communication-1')!.guidance.slice(-2))
      .toEqual(['1st Category 0 - 1 - message not clear.', '2nd Category 2 - message clear.']);
    expect(letter.rubric.practiceNotes).toContain('Use the formal letter layout and the supplied addresses.');
    expect(byId('fr-2026-ol-writing-b1b-route-6789').rubric.taskRequirements)
      .toEqual(['Pour 6, 7, 8 et 9 : Choisissez trois questions et répondez par des phrases complètes.']);
    expect(byId('fr-2025-ol-writing-b1b-route-6789').rubric.taskRequirements)
      .toEqual(['Pour 6, 7, 8 et 9 : choisissez trois questions et répondez par des phrases complètes.']);
    expect(byId('fr-2026-ol-writing-b2a').rubric.practiceNotes![0]).toBe('Choose any three of the five printed points. Each Communication mark is for one point you chose; one point cannot earn two of them.');
    expect(byId('fr-2021-hl-writing-b4').rubric.criteria[0].guidance).toEqual(['Q. 4 No particular layout required']);
    expect(byId('fr-2026-hl-writing-b3').rubric.criteria[0].guidance).toEqual(['Q. 3 – no particular layout required']);
    expect(byId('fr-2014-hl-writing-b1a').rubric.taskRequirements).toEqual([]);
    expect(byId('fr-2014-hl-writing-b1a').rubric.practiceNotes![0]).toBe('Write your answer in French.');
  });

  it('reproduces each year’s printed wording: word-count line, diary instruction, grid case and letter notes', () => {
    for (const year of [2010, 2011, 2013, 2016, 2018, 2020]) {
      expect(cards.find(card => card.id === `fr-${year}-hl-writing-b2b`)!.questionText.endsWith('\n(about 75 words)')).toBe(true);
    }
    expect(cards.filter(card => card.questionText.includes('(about 75 words)'))).toHaveLength(6);
    for (const card of cards.filter(card => /-ol-writing-b3a(?:-route-|$)/.test(card.id))) {
      const instruction = card.year >= 2021 ? 'Note three of the following five points in French in your diary:'
        : card.year >= 2017 ? 'Note the following in French in your diary:' : 'Note the following in your diary:';
      expect(card.questionText.split('\n\n')[0].endsWith(` ${instruction}`), card.id).toBe(true);
      expect(card.questionText).not.toContain('Note the selected points');
    }
    const byId = (id: string) => cards.find(card => card.id === id)!;
    expect(byId('fr-2017-hl-writing-b1a').rubric.criteria[1].bands?.[0].guidance[0]).toBe('idiomatic French');
    expect(byId('fr-2016-hl-writing-b1a').rubric.criteria[1].bands?.[0].guidance[0]).toBe('Idiomatic French');
    expect(byId('fr-2013-ol-writing-b1b-route-6789').rubric.criteria.at(-1)?.bands?.[2].guidance)
      .toEqual(['Most verb endings, tenses, agreements incorrect', 'Most words misspelt', 'No sense of register']);
    expect(byId('fr-2015-ol-writing-b3b-route-123').rubric.criteria[0].guidance).toContain('Include “Irlande”. Accept “Ireland” / “Éire”.');
    expect(byId('fr-2026-ol-writing-b3b').rubric.criteria[0].guidance).toContain('Include Irlande, accept “Ireland” / “Éire”.');
    expect(byId('fr-2017-ol-writing-b2a-route-123').rubric.criteria[0].guidance[0]).toBe('You have a toothache / and you can’t eat');
  });

  it('keeps the 2010 page-specific tense note, form condition and cartoon board text', () => {
    const group = cards.filter(card => card.year === 2010);
    expect(group).toHaveLength(18);
    const message = group.find(card => card.id === 'fr-2010-ol-writing-b2a-route-123')!;
    // Scheme p11 prints "NB." where pp.9 and 12-14 print "N.B.".
    expect(message.rubric.criteria[0].guidance).toContain('NB. Correct tense required for full marks in Communication.');
    expect(group.find(card => card.id === 'fr-2010-ol-writing-b2b-route-123')!.rubric.criteria[0].guidance)
      .toContain('N.B. Correct tense required for full marks in Communication.');
    const form = group.find(card => card.id === 'fr-2010-ol-writing-b1b-route-6789')!;
    expect(form.rubric.criteria.find(c => c.id === 'communication-7')?.guidance).toContain('Two or more subjects required for full marks');
    const cartoon = group.find(card => card.id === 'fr-2010-hl-writing-b3a')!;
    expect(cartoon.questionText).toContain('Le « fast food » fait partie du style de vie');
    expect(cartoon.questionText).not.toContain('HAMBURGER');
    expect(cartoon.sourceMaterial?.kind).toBe('source-illustration');
    expect(group.find(card => card.id === 'fr-2010-hl-writing-b1a')!.additionalSourceMaterials?.[0].pages).toEqual([2, 3]);
    const letter = group.find(card => card.id === 'fr-2010-ol-writing-b3b-route-123')!;
    expect(letter.rubric.criteria.find(c => c.id === 'format-top')?.guidance)
      .toContain('Name and address of sender in top left corner – with name on first line, number & street on second line, etc.');
  });

  it('verifies the tiled 2011 Higher prompts against their rebuilt words and keeps the form conditions', () => {
    const group = cards.filter(card => card.year === 2011);
    expect(group).toHaveLength(18);
    const slogan = group.find(card => card.id === 'fr-2011-hl-writing-b3a')!;
    expect(slogan.questionText.split('\n\n')[0]).toBe('« Trop boire, c’est le cauchemar ! »');
    expect(slogan.sourceMaterial?.kind).toBe('source-illustration');
    const referees = group.find(card => card.id === 'fr-2011-hl-writing-b3b')!;
    expect(referees.questionText.split('\n\n')).toHaveLength(6);
    expect(referees.questionText).toContain('Guillaume, 20 ans');
    expect(referees.questionText).toContain('Nadine, 19 ans');
    // The raw text layer of these pages repeats glyphs ("Tro p boire"); none may reach a card.
    for (const card of group) expect(card.questionText, card.id).not.toMatch(/Tro p|cauch hemar|mo ots|Twitt ter/);
    expect(group.find(card => card.id === 'fr-2011-hl-writing-b4b')!.sourceMaterial?.kind).toBe('source-illustration');
    const email = group.find(card => card.id === 'fr-2011-hl-writing-b2b')!;
    expect(email.questionText.match(/^- /gm)).toHaveLength(5);
    expect(email.questionText).not.toContain('Ba mhaith');
    const form = group.find(card => card.id === 'fr-2011-ol-writing-b1b-route-6789')!;
    expect(form.rubric.criteria.find(c => c.id === 'communication-6')?.guidance).toContain('Two or more qualities required for full marks');
    expect(group.find(card => card.id === 'fr-2011-ol-writing-b1b-field-3')!.rubric.criteria[0].guidance)
      .toEqual(['Age – accept any appropriate age (“ans” needed for full marks)']);
    const diary = group.find(card => card.id === 'fr-2011-ol-writing-b3a-route-123')!;
    expect(diary.rubric.criteria.find(c => c.id === 'communication-3')?.guidance[0]).toBe('You hope to go the beach / with your cousin Martin on Sunday.');
    expect(diary.questionText).toContain('• You hope to go to the beach with your cousin Martin on Sunday.');
  });

  it('keeps the 2012 form-sentence condition, boxed quotation and earlier scheme layout', () => {
    const group = cards.filter(card => card.year === 2012);
    expect(group).toHaveLength(18);
    const form = group.find(card => card.id === 'fr-2012-ol-writing-b1b-route-6789')!;
    const tense = 'N.B. Correct tense required for full marks in Communication.';
    expect(form.rubric.criteria.find(c => c.id === 'communication-7')?.guidance).toEqual([
      'Quels sports pratiquez-vous ?', '1st Category 0 - 2 - message not clear.', '2nd Category 3 - message clear.',
      'Two or more sports required here for full marks', tense,
    ]);
    for (const id of ['communication-6', 'communication-8', 'communication-9']) {
      expect(form.rubric.criteria.find(c => c.id === id)?.guidance).not.toContain('Two or more sports required here for full marks');
    }
    expect(form.schemeCitation).toContain('p.9');
    const quote = group.find(card => card.id === 'fr-2012-hl-writing-b3b')!;
    expect(quote.questionText.split('\n\n').slice(1, 3)).toEqual(['Solange, 22 ans.', 'Donnez vos réactions.\n(75 mots environ)']);
    expect(quote.sourceMaterial?.kind).toBe('source-text');
    expect(group.find(card => card.id === 'fr-2012-hl-writing-b4a')!.sourceMaterial?.kind).toBe('source-illustration');
    const message = group.find(card => card.id === 'fr-2012-ol-writing-b2a-route-123')!;
    expect(message.questionText).toContain('• He will arrive tomorrow at half-past ten.');
    expect(message.schemeCitation).toContain('p.11');
    expect(message.rubric.criteria.at(-1)?.bands?.[1].guidance).not.toContain('some sense of register');
    expect(group.find(card => card.id === 'fr-2012-ol-writing-b3b-route-123')!.schemeCitation).toContain('pp.14, 17, 18');
  });

  it('keeps the 2013 bilingual message, illustrated prompts and scheme-specific form and letter rules', () => {
    const group = cards.filter(card => card.year === 2013);
    expect(group).toHaveLength(18);
    const message = group.find(card => card.id === 'fr-2013-hl-writing-b2b')!;
    // Printed in Irish then English: only the English rendering, all five points.
    expect(message.questionText.match(/^- /gm)).toHaveLength(5);
    expect(message.questionText).toContain('You are staying with a French family who have gone out for the day.');
    expect(message.questionText).not.toContain('teaghlach');
    expect(message.questionText).not.toContain('___');
    const cartoon = group.find(card => card.id === 'fr-2013-hl-writing-b4b')!;
    expect(cartoon.questionText).toBe('Le scandale de la viande de cheval !\n\nDonnez votre réaction.\n(75 mots environ)');
    for (const id of ['b3a', 'b3b', 'b4a', 'b4b']) {
      expect(group.find(card => card.id === `fr-2013-hl-writing-${id}`)!.sourceMaterial?.kind).toBe('source-illustration');
    }
    expect(group.find(card => card.id === 'fr-2013-ol-writing-b1b-field-5')!.rubric.criteria[0].guidance)
      .toEqual(['References to both brother(s) & sister(s) required here']);
    const letter = group.find(card => card.id === 'fr-2013-ol-writing-b3b-route-123')!;
    expect(letter.rubric.criteria.find(c => c.id === 'format-top')?.guidance)
      .toContain('[Note: Accept “Monsieur le Directeur” or “Madame la Directrice” in the address above]');
    expect(letter.schemeCitation).toContain('pp.15, 19, 20');
    const postcard = group.find(card => card.id === 'fr-2013-ol-writing-b2b-route-123')!;
    expect(postcard.rubric.criteria[0].guidance).toContain('N.B. Correct tense required for full marks in Communication.');
  });

  it('keeps the 2014 cartoon, boxed article and the printed tense rule on every Ordinary task', () => {
    const group = cards.filter(card => card.year === 2014);
    expect(group).toHaveLength(18);
    expect(group.filter(card => card.level === 'higher').map(card => card.totalMarks))
      .toEqual([40, 40, 30, 30, 30, 30, 30, 30]);
    const cartoon = group.find(card => card.id === 'fr-2014-hl-writing-b4b')!;
    // Only part of the cartoon lettering is in the text layer; never insert a fragment.
    expect(cartoon.questionText).toBe('Donnez vos réactions.\n(75 mots environ)');
    expect(cartoon.sourceMaterial?.kind).toBe('source-illustration');
    expect(cartoon.sourceMaterial?.pages).toEqual([12]);
    const boxed = group.find(card => card.id === 'fr-2014-hl-writing-b4a')!;
    expect(boxed.questionText.split('\n\n').slice(0, 3)).toEqual([
      'Les cigarettes tuent 6 millions de personnes par an',
      'Il y a une seule solution : interdire purement et simplement la cigarette !',
      'Le Point, le 15 mai, 2012',
    ]);
    expect(boxed.sourceMaterial?.kind).toBe('source-text');
    expect(group.find(card => card.id === 'fr-2014-hl-writing-b3a')!.sourceMaterial?.kind).toBe('source-illustration');
    expect(group.find(card => card.id === 'fr-2014-hl-writing-b1b')!.additionalSourceMaterials?.[0].pages).toEqual([4, 5]);
    expect(group.find(card => card.id === 'fr-2014-hl-writing-b2b')!.rubric.criteria[0].guidance)
      .toEqual(['Q. 2 (a) and (b) No particular layout required.']);
    const tense = 'N.B. Correct tense required for full marks in Communication.';
    for (const card of group.filter(card => card.id.includes('ol-writing-') && card.id.includes('-route-'))) {
      for (const criterion of card.rubric.criteria.filter(c => c.id.startsWith('communication-'))) {
        expect(criterion.guidance, card.id).toContain(tense);
      }
    }
    for (const card of cards.filter(card => card.year >= 2015)) {
      expect(card.rubric.criteria.flatMap(c => c.guidance), card.id).not.toContain(tense);
    }
    expect(group.find(card => card.id === 'fr-2014-ol-writing-b1b-field-2')!.rubric.criteria[0].guidance)
      .toEqual(['Christian Name – accept any reasonable Christian name']);
    for (const parent of ['b2a', 'b2b', 'b3a']) {
      const task = group.find(card => card.id === `fr-2014-ol-writing-${parent}-route-123`)!;
      expect(task.rubric.criteria.at(-1)?.bands?.[1].guidance).not.toContain('some sense of register');
    }
    const letter = group.find(card => card.id === 'fr-2014-ol-writing-b3b-route-123')!;
    expect(letter.questionText).toContain('You are Eamonn / Emma Ryan, 13 Orchard Place, Celbridge, Co. Kildare.');
    expect(letter.rubric.criteria.find(c => c.id === 'format-top')?.guidance)
      .toContain('City / town / village & date (Celbridge, le 11 juin 2014) in top right corner or underneath.');
    expect(letter.rubric.criteria.find(c => c.id === 'language')?.bands?.[1].guidance).toContain('some sense of register');
  });

  it('uses the distinct 2016 Higher formal-letter grid and preserves the form discrepancy', () => {
    const group = cards.filter(card => card.year === 2016);
    expect(group).toHaveLength(18);
    const letter = group.find(card => card.id === 'fr-2016-hl-writing-b2b')!;
    expect(letter.rubric.criteria.map(c => [c.id, c.maxMarks])).toEqual([
      ['format', 6], ['communication', 12], ['language', 12],
    ]);
    expect(letter.rubric.criteria[1].bands?.map(b => b.marks)).toEqual([
      [9, 10, 11, 12], [5, 6, 7, 8], [0, 1, 2, 3, 4],
    ]);
    expect(letter.questionText.match(/- /g)).toHaveLength(5);
    expect(letter.questionText).toContain('27, Bridge Street, Cashel');
    expect(letter.questionText).toContain('Minimum 18 ans');
    expect(letter.questionText).not.toContain('Scríobh');
    expect(letter.schemeCitation).toContain('PDF pages 14–15');
    expect(letter.rubric.criteria.flatMap(c => c.guidance).join(' ')).not.toContain('No particular layout');
    expect(letter.sourceMaterial?.kind).toBe('source-illustration');
    const field = group.find(card => card.id === 'fr-2016-ol-writing-b1b-field-5')!;
    expect(field.questionText).toContain('Niveau de français');
    expect(field.rubric.criteria[0].guidance).toEqual(['Years of study – accept any appropriate number']);
    // The discrepancy is our disclosure, so it sits in the app-labelled practice notes.
    expect(field.rubric.practiceNotes!.join(' ')).toContain('Source discrepancy');
    expect(field.rubric.taskRequirements).toEqual([]);
    expect(group.find(card => card.id === 'fr-2016-ol-writing-b1b-field-4')!.rubric.taskRequirements).toEqual([]);
    const ordinaryLetter = group.find(card => card.id === 'fr-2016-ol-writing-b3b-route-123')!;
    expect(ordinaryLetter.rubric.criteria[0].guidance).toContain('More than 3 mistakes - award 0.');
    expect(ordinaryLetter.rubric.criteria[0].guidance.join(' ')).toContain('Buncrana, le 15 juin 2016');
  });

  it('preserves the 2017 required responses and discloses the source address discrepancy', () => {
    const group = cards.filter(card => card.year === 2017);
    expect(group).toHaveLength(18);
    const email = group.find(card => card.id === 'fr-2017-hl-writing-b2b')!;
    expect(email.questionText.match(/• /g)).toHaveLength(4);
    expect(email.totalMarks).toBe(30);
    const boxed = group.find(card => card.id === 'fr-2017-hl-writing-b4a')!;
    expect(boxed.questionText).toContain('Brexit – l’Union européenne en crise');
    expect(boxed.questionText).toContain('Le 23 juin 2016');
    expect(boxed.questionText).toContain('pour l’Irlande ?');
    const cartoon = group.find(card => card.id === 'fr-2017-hl-writing-b4b')!;
    expect(cartoon.sourceMaterial?.kind).toBe('source-illustration');
    expect(cartoon.sourceMaterial?.pages).toEqual([12]);
    const form = group.find(card => card.id === 'fr-2017-ol-writing-b1b-route-6789')!;
    expect(form.rubric.criteria.map(c => c.maxMarks)).toEqual([3, 3, 3, 3, 8]);
    expect(form.questionText).toContain('avec ou sans animal ? Pourquoi ?');
    const letter = group.find(card => card.id === 'fr-2017-ol-writing-b3b-route-123')!;
    expect(letter.questionText).toContain('26 rue Pasterolli');
    expect(letter.rubric.practiceNotes!.join(' ')).toContain('appendix prints rue Pastorelli');
    expect(letter.rubric.taskRequirements).toEqual(['Rédigez vos réponses en français.']);
    expect(letter.schemeCitation).toContain('pp.17, 20, 21');
    for (const parent of ['b2a', 'b2b', 'b3a', 'b3b']) expect(group.filter(card => card.id.includes(`ol-writing-${parent}-route-`))).toHaveLength(1);
  });

  it('retains all 2018 application points and the full cartoon source', () => {
    const group = cards.filter(card => card.year === 2018);
    expect(group).toHaveLength(18);
    const email = group.find(card => card.id === 'fr-2018-hl-writing-b2b')!;
    expect(email.questionText.match(/• /g)).toHaveLength(5);
    expect(email.questionText).toContain('9,77 € par heure');
    expect(email.questionText).toContain('marine@jouffruit.fr');
    expect(email.questionText).not.toContain('Scríobh');
    expect(email.totalMarks).toBe(30);
    expect(email.sourceMaterial?.pages).toEqual([8]);
    const cartoon = group.find(card => card.id === 'fr-2018-hl-writing-b3b')!;
    expect(cartoon.questionText).toBe('Pensez-vous que les voitures sans conducteur sont une bonne idée ?\n(75 mots environ)');
    expect(cartoon.sourceMaterial?.kind).toBe('source-illustration');
    expect(cartoon.sourceMaterial?.pages).toEqual([10]);
    for (const suffix of ['a', 'b']) {
      const linked = group.find(card => card.id === `fr-2018-hl-writing-b1${suffix}`)!;
      expect(linked.additionalSourceMaterials?.[0].pages).toEqual(suffix === 'a' ? [2, 3] : [4, 5]);
      expect(linked.totalMarks).toBe(40);
    }
    const form = group.find(card => card.id === 'fr-2018-ol-writing-b1b-route-6789')!;
    expect(form.rubric.criteria.map(c => c.maxMarks)).toEqual([3, 3, 3, 3, 8]);
    expect(group.find(card => card.id === 'fr-2018-ol-writing-b1b-field-5')!.rubric.criteria[0].guidance[0]).toContain('1 language acceptable');
    for (const parent of ['b2a', 'b2b', 'b3a', 'b3b']) expect(group.filter(card => card.id.includes(`ol-writing-${parent}-route-`))).toHaveLength(1);
    expect(group.find(card => card.id === 'fr-2018-ol-writing-b3b-route-123')!.schemeCitation).toContain('pp.17, 21, 22');
  });

  it('keeps the 2019 required responses, cartoon and two-page formal-letter appendix', () => {
    const group = cards.filter(card => card.year === 2019);
    expect(group).toHaveLength(18);
    const form = group.find(card => card.id === 'fr-2019-ol-writing-b1b-route-6789')!;
    expect(form.rubric.criteria.map(c => c.maxMarks)).toEqual([3, 3, 3, 3, 8]);
    expect(form.questionText).toContain('échange de maison');
    expect(form.sourceMaterial?.pages).toEqual([11]);
    expect(form.rubric.criteria.at(-1)?.bands?.[2].guidance).toEqual([
      'most verb endings, tenses, agreements incorrect', 'most words misspelt', 'no sense of register',
    ]);
    for (const parent of ['b2a', 'b2b', 'b3a', 'b3b']) {
      const routes = group.filter(card => card.id.includes(`ol-writing-${parent}-route-`));
      expect(routes).toHaveLength(1);
      expect(routes[0].totalMarks).toBe(30);
      expect(routes[0].questionText.match(/• /g)).toHaveLength(3);
    }
    const letter = group.find(card => card.id === 'fr-2019-ol-writing-b3b-route-123')!;
    expect(letter.schemeCitation).toContain('pp.15, 18, 19');
    expect(letter.questionText).toContain('12 Mountain View, Clonmel');
    expect(letter.rubric.criteria[0].guidance.join(' ')).toContain('Clonmel, le 12 juin, 2019');
    const cartoon = group.find(card => card.id === 'fr-2019-hl-writing-b4b')!;
    expect(cartoon.sourceMaterial?.kind).toBe('source-illustration');
    expect(cartoon.sourceMaterial?.pages).toEqual([12]);
    const email = group.find(card => card.id === 'fr-2019-hl-writing-b2b')!;
    expect(email.questionText.match(/• /g)).toHaveLength(3);
    expect(email.questionText).toContain('vous le félicitez');
    expect(email.rubric.criteria[0].guidance).toContain('Q. 2 (a) and (b) No particular layout required.');
    expect(group.filter(card => card.level === 'higher').map(card => card.totalMarks)).toEqual([40, 40, 30, 30, 30, 30, 30, 30]);
  });

  it('keeps the 2020 fixed-response tasks at their own published boundaries', () => {
    const group = cards.filter(card => card.year === 2020);
    expect(group).toHaveLength(18);
    expect(group.filter(card => card.level === 'higher').map(card => card.totalMarks))
      .toEqual([40, 40, 30, 30, 30, 30, 30, 30]);
    const form = group.find(card => card.id === 'fr-2020-ol-writing-b1b-route-6789')!;
    expect(form.totalMarks).toBe(20);
    expect(form.rubric.criteria.map(criterion => criterion.maxMarks)).toEqual([3, 3, 3, 3, 8]);
    for (const parent of ['b2a', 'b2b', 'b3a', 'b3b']) {
      const fixed = group.filter(card => card.id.includes(`ol-writing-${parent}-route-`));
      expect(fixed).toHaveLength(1);
      expect(fixed[0].id).toBe(`fr-2020-ol-writing-${parent}-route-123`);
      expect(fixed[0].totalMarks).toBe(30);
      expect(fixed[0].questionText.match(/• /g)).toHaveLength(3);
    }
    const review = group.find(card => card.id === 'fr-2020-hl-writing-b2b')!;
    expect(review.questionText.match(/• /g)).toHaveLength(4);
    expect(review.questionText).toContain('Montmartre');
    expect(review.rubric.criteria[0].guidance).toContain('Q. 2 (a) and (b) No particular layout required.');
    expect(review.sourceMaterial?.pages).toEqual([10]);
    expect(review.sourceMaterial?.kind).toBe('source-illustration');
  });

  it('carries the referenced passages and the image-based writing prompts', () => {
    const byId = (id: string) => cards.find(card => card.id === id)!;
    expect(byId('fr-2025-hl-writing-b1a').additionalSourceMaterials?.[0].pages).toEqual([4, 5]);
    expect(byId('fr-2024-hl-writing-b1b').additionalSourceMaterials?.[0].pages).toEqual([4, 5]);
    expect(byId('fr-2025-hl-writing-b1b').additionalSourceMaterials?.[0].pages).toEqual([6, 7]);
    expect(byId('fr-2026-hl-writing-b1c').additionalSourceMaterials?.[0].pages).toEqual([6, 7]);
    const cartoon = byId('fr-2023-hl-writing-b5');
    expect(cartoon.sourceMaterial?.kind).toBe('source-illustration');
    expect(cartoon.sourceMaterial?.pages).toEqual([12]);
    expect(cartoon.questionText).toBe('Aller à la fac – comment survivre ?\n\nDonnez votre réaction.\n(75 mots environ)');
  });

  it('includes formal-letter appendix rules and that year’s language descriptors', () => {
    for (const card of cards.filter(card => /ol-writing-b3b(?:-route-|$)/.test(card.id))) {
      expect(card.rubric.criteria.find(c => c.id === 'language')?.requiresAttempt).toBe(true);
      expect(card.rubric.criteria.find(c => c.id === 'format-close')?.guidance)
        .toContain('Formal ending required.');
      expect(card.rubric.criteria.find(c => c.id === 'format-top')?.guidance)
        .toContain('2 mistakes - deduct 1 mark.');
    }
    const latest = cards.find(card => card.id === 'fr-2026-ol-writing-b2a')!;
    expect(latest.rubric.criteria.find(c => c.id === 'language')?.bands?.[2].guidance[0])
      .toBe('very limited to limited use of vocabulary of vocabulary');
  });

  it('uses the earlier Higher tariffs and only the language descriptors that year published', () => {
    for (const year of [2021, 2022]) {
      const group = cards.filter(card => card.year === year && card.level === 'higher');
      expect(group.map(card => card.totalMarks)).toEqual([40, 40, 40, 30, 30, 30, 30, 30]);
      expect(group[0].rubric.criteria.map(c => c.maxMarks)).toEqual([20, 20]);
      expect(group[3].rubric.criteria.map(c => c.maxMarks)).toEqual([15, 15]);
      expect(group[3].rubric.criteria[0].bands?.[0].marks).toEqual([11, 12, 13, 14, 15]);
    }
    const form = cards.find(card => card.id === 'fr-2021-ol-writing-b1b-route-6789')!;
    expect(form.rubric.criteria.at(-1)?.bands?.[2].guidance).toEqual([
      'most verb endings, tenses, agreements incorrect', 'most words misspelt', 'no sense of register',
    ]);
    const higher2022 = cards.find(card => card.id === 'fr-2022-hl-writing-b1a')!;
    expect(higher2022.schemeCitation).toContain('p.14 (PDF page 15)');
    expect(higher2022.schemeRegion?.p).toBe(15);
  });

  it('applies the form language gate without confusing an unclear answer with no attempt', () => {
    const card = cards.find(c => c.id === 'fr-2026-ol-writing-b1b-route-6789')!;
    expect(frenchMarks(card, { [frenchScoreId('language')]: 8 })).toBe(0);
    expect(frenchMarks(card, { [frenchScoreId('language')]: 8, [FRENCH_ATTEMPT_ID]: 1 })).toBe(8);
    expect(frenchMarks(card, { [frenchScoreId('language')]: 99, [FRENCH_ATTEMPT_ID]: 1 })).toBe(0);
    const full = Object.fromEntries(card.rubric.criteria.map(c => [frenchScoreId(c.id), c.maxMarks]));
    expect(frenchMarks(card, { ...full, [FRENCH_ATTEMPT_ID]: 1 })).toBe(20);
  });
});
