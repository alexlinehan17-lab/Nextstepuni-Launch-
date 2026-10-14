import { describe, expect, it } from 'vitest';
import { CARDS as higher } from '../components/MarkBank/cards/agricultural-science/higher';
import { CARDS as ordinary } from '../components/MarkBank/cards/agricultural-science/ordinary';
import review from '../scripts/markbank/authored/agricultural-science-reviewed-tasks.json';
import { isPointCard, tariffReconciles } from '../types/markBank';
import { marksClaimed } from '../components/MarkBank/SessionScreen';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import atlas from '../data/examTopics/agricultural-science-question-runtime.json';
import { examTopicIdsForQuestion } from '../data/examTopics/registry';
import { siblingsFor } from '../components/PaperTrail/topics';
import { preferredAnswersUrl } from '../components/PaperTrail/vaultResolve';
import { paperRegionFor } from '../components/PaperTrail/paperRegion';
import type { PaperAnswerMap } from '../types/paperTrail';
import { findCanonicalTopic, resolveCurriculumSpecification } from '../curriculumRegistry';
import { cardsForTopic } from '../components/MarkBank/deck';
import census from '../scripts/markbank/authored/agricultural-science-census.json';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';

const cards = [...higher, ...ordinary];
const get = (id: string) => {
  const card = cards.find(c => c.id === id);
  if (!card || !isPointCard(card)) throw new Error(`Missing reviewed point card ${id}`);
  return card;
};

describe('Agricultural Science reviewed additions (full audit still in progress)', () => {
  it('matches the independent source census exactly, including option addresses, routes and published marks', () => {
    for (const paper of census.papers) {
      const actual = paper.lang === 'iv'
        ? atlas.translatedMarkBankCards.filter(join => join.year === paper.year && join.fileid === paper.paperFileid)
            .map(join => ({ questionRef:get(join.cardId).questionRef, totalMarks:join.marksPerRoute }))
        : cards.filter(card => card.year === paper.year && card.level === paper.level);
      const expected = paper.baseTasks.flatMap(task => task.routes.map(ref => ({ ref, marks:task.marksPerResponse })));
      expect(actual.map(card => card.questionRef).sort()).toEqual(expected.map(task => task.ref).sort());
      for (const task of expected) {
        expect(actual.find(card => card.questionRef === task.ref)?.totalMarks,task.ref).toBe(task.marks);
      }
    }
    expect(census.status).toBe('in-progress');
    expect(census.editionStatus).toHaveLength(68);
    expect(census.editionStatus.filter(edition => edition.independentCensus === 'open')).toHaveLength(42);
    expect(census.questionMarkChecks.filter(check => check.sourceException)).toHaveLength(2);
  });

  it('keeps the three-of-four udder labels on one card at the published three-mark tariff', () => {
    expect(cards.filter(c => c.questionRef.startsWith('2023 HL Q18(a)(i)'))).toHaveLength(1);
    const card = get('agsci-2023-hl-q18ai');
    expect(card.totalMarks).toBe(3);
    expect(card.sourceMaterial?.pages).toEqual([37]);
    expect(card.questionText).toBe('Label any three parts of the structure of the udder.');
    expect(card.rows[0].group?.options).toHaveLength(4);
    expect(card.rows[0].group?.options[1]).toBe('Median suspensory ligament');
    expect(card.rows[0].group?.claimMax).toBe(3);
    expect(tariffReconciles(card)).toBe(true);
    expect(marksClaimed(card, {}, { labels: [0, 1, 3] })).toBe(3);
  });

  it('keeps both ram reason pools on one card with the complete 3+1 marking menu', () => {
    expect(cards.filter(c => c.questionRef.startsWith('2022 OL Q2(b)(ii)'))).toHaveLength(1);
    const card = get('agsci-2022-ol-q2bii');
    expect(card.rows[0].group?.options).toHaveLength(9);
    expect(card.rows[0].group?.options).toContain('easy lambing');
    expect(card.rows[0].group?.options).toContain('excellent conformation');
    expect(card.rows[0].contextNote).toContain('Breed F reasons');
    expect(card.stem).not.toContain('Practice choice');
    expect(card.totalMarks).toBe(4);
    expect(card.rows[0].group?.perOptionSteps).toEqual([3, 1]);
    expect(card.sourceMaterial?.pages).toEqual([5]);
    expect(tariffReconciles(card)).toBe(true);
    expect(marksClaimed(card, {}, { reasons: [0] })).toBe(3);
    expect(marksClaimed(card, {}, { reasons: [0, 1] })).toBe(4);
  });

  it('retains partial credit for the two correct warning symbols', () => {
    const card = get('agsci-2025-ol-q8b');
    expect(card.rows[0].group?.options).toEqual(['2', '3']);
    expect(card.rows[0].group?.perOptionSteps).toEqual([3, 2]);
    expect(card.sourceMaterial?.pages).toEqual([9]);
    expect(tariffReconciles(card)).toBe(true);
    expect(marksClaimed(card, {}, { 'warning-signs': [0] })).toBe(3);
    expect(marksClaimed(card, {}, { 'warning-signs': [1] })).toBe(3);
    expect(marksClaimed(card, {}, { 'warning-signs': [0, 1] })).toBe(5);
  });

  it('retains the field photograph and the actual four-mark sketch criterion', () => {
    const card = get('agsci-2022-ol-q13bi');
    expect(card.topicId).toBe('agsci-2-3');
    expect(card.sourceMaterial?.pages).toEqual([22]);
    expect(card.rows).toEqual([{ id: 'sampling-pattern', kind: 'criterion', verbatim: 'W shape on photograph', marks: 4 }]);
  });

  it('ships every reviewed route with a source page and a reconciled tariff', () => {
    for (const task of review.tasks) {
      for (const id of task.cardIds) {
        const card = get(id);
        expect(card.totalMarks).toBe(task.marksPerRoute);
        expect(card.sourceMaterial?.pages).toContain(task.paperPage);
        expect(tariffReconciles(card)).toBe(true);
      }
    }
  });

  it('preserves both 2010 Q3 options and all 55 independently reviewed legacy tasks', () => {
    const legacy = cards.filter(card => card.year === 2010 && card.level === 'higher');
    expect(legacy).toHaveLength(55);
    expect(legacy.filter(card => card.questionRef.includes('Q3 Option One'))).toHaveLength(6);
    expect(legacy.filter(card => card.questionRef.includes('Q3 Option Two'))).toHaveLength(6);
    // Hoose or grass tetany: one card whose two disease routes are mutually exclusive rows.
    const disease = get('agsci-2010-hl-q3o2b');
    expect(disease.totalMarks).toBe(12);
    expect(disease.rows.map(row => row.route)).toEqual(['Hoose', 'Hoose', 'Hoose', 'grass-tetany', 'grass-tetany', 'grass-tetany']);
    expect(tariffReconciles(disease)).toBe(true);
    expect(marksClaimed(disease, { 'r-1': 'yes', 'r-2': 'yes', 'r-3': 'yes' })).toBe(12);
    expect(marksClaimed(disease, { 'r-1': 'yes', 'r-4': 'yes' })).toBe(4);
    for (const card of legacy) {
      const specification = resolveCurriculumSpecification(card.subjectId, card.year)!;
      expect(card.specificationId).toBe(specification.id);
      expect(card.specVersion).toBe(specification.id);
      expect(card.specificationId).toBe('agricultural-science:legacy-current');
      expect(card.curriculumNodeIds?.length).toBeGreaterThan(0);
      for (const id of card.curriculumNodeIds!) expect(findCanonicalTopic(specification, id)).toBeDefined();
    }
  });

  it('keeps both 2010 three-of-four choices on one card that lists every printed item', () => {
    for (const [question, ref, total, rows, answer] of [['q7a', 'Q7(a)', 12, 4, 3], ['q8c', 'Q8(c)', 24, 8, 6]] as const) {
      expect(cards.filter(card => card.questionRef.startsWith(`2010 HL ${ref}`))).toHaveLength(1);
      const card = get(`agsci-2010-hl-${question}`);
      expect(card.questionRef).toBe(`2010 HL ${ref}`);
      expect(card.totalMarks).toBe(total);
      expect(card.rows).toHaveLength(rows);
      expect(card.tariffModel).toEqual({ kind: 'bestNofParts', answer, ofParts: rows, perPart: 4 });
      expect(card.rows.every(row => row.group?.claimMax === 2 && row.group?.perOption === 2)).toBe(true);
      expect(tariffReconciles(card)).toBe(true);
      expect(card.stem ?? '').not.toContain('Practice choice');
    }
  });

  it('retains the 85 Ordinary tasks and the published totals, including the English Q12 discrepancy', () => {
    const legacy = ordinary.filter(card => card.year === 2010);
    expect(legacy).toHaveLength(85);
    const totals: Record<string, number> = {};
    for (const card of legacy) {
      const question = card.questionRef.match(/Q(\d+)/)![1];
      totals[question] = (totals[question] ?? 0) + card.totalMarks;
      const specification = resolveCurriculumSpecification(card.subjectId, card.year)!;
      expect(card.specificationId).toBe(specification.id);
      for (const id of card.curriculumNodeIds!) expect(findCanonicalTopic(specification, id)).toBeDefined();
    }
    // Q12 contains all four alternatives, not a candidate's two-part exam
    // total. Its English part (d) prints 28 marks despite the paper's 30.
    expect(totals).toEqual({ 1:20, 2:20, 3:20, 4:20, 5:20, 6:20, 7:20, 8:60, 9:60, 10:60, 11:60, 12:118, 13:60 });
    expect(get('agsci-2010-ol-q12aiii').tariffModel.kind).toBe('questionTotal');
    expect(get('agsci-2010-ol-q12aiii').rows[0].marks).toBeNull();
    expect(get('agsci-2010-ol-q12aiii').rows[0].contextNote).toContain('Any three points');
    expect(get('agsci-2010-ol-q12dii').totalMarks).toBe(18);
    expect(get('agsci-2010-ol-q12dii').rows[0].contextNote).toContain('28');
  });

  it('retains all 67 2011 Higher tasks and separates shared genetic-cross marks from the three outcomes', () => {
    const legacy = higher.filter(card => card.year === 2011);
    expect(legacy).toHaveLength(67);
    const cross = get('agsci-2011-hl-q7b-cross');
    expect(cross.totalMarks).toBe(12);
    expect(cross.figure?.solution).toBe(true);
    expect(marksClaimed(cross, {'r-1':'yes','r-2':'yes'}, {'r-3':[0,1,2,3],'r-4':[0,1,2,3]})).toBe(12);
    for (const key of ['i','ii','iii']) expect(get(`agsci-2011-hl-q7b${key}`).totalMarks).toBe(4);
    expect(get('agsci-2011-hl-q7bi').rows[0].verbatim).toBe('12/16');
    expect(get('agsci-2011-hl-q7bii').rows[0].verbatim).toBe('4/16');
    expect(get('agsci-2011-hl-q7biii').rows[0].verbatim).toBe('3/16');
    // Any three of four comparison pairs: one card, eight member answers, the best six at 4.
    expect(legacy.filter(card => card.questionRef.startsWith('2011 HL Q8(c)'))).toHaveLength(1);
    const pairs = get('agsci-2011-hl-q8c');
    expect(pairs.totalMarks).toBe(24);
    expect(pairs.rows).toHaveLength(1);
    expect(pairs.rows[0].group?.options).toHaveLength(8);
    expect(pairs.rows[0].group?.claimMax).toBe(6);
    expect(marksClaimed(pairs, {}, { 'r-1': [0, 1, 2, 3, 6, 7] })).toBe(24);
    expect(marksClaimed(pairs, {}, { 'r-1': [0, 1] })).toBe(8);
  });

  it('keeps the heart image under circulatory physiology and preserves the cereal drawing’s partial award', () => {
    for (const part of ['i','ii','iii']) {
      const card = get(`agsci-2011-hl-q5b${part}`);
      expect(card.kind).toBe('diagram');
      expect(card.topicId).toBe('agsci-4-1');
      expect(card.figure?.solution).not.toBe(true);
      const task = review.tasks.find(task => task.cardIds.includes(card.id))!;
      expect(task.examTopicIds).toEqual(['agricultural-science-higher-animal-physiology-circulatory-system']);
    }
    const drawing = get('agsci-2011-hl-q6c');
    expect(drawing.tariffModel.kind).toBe('questionTotal');
    expect(drawing.totalMarks).toBe(8);
    expect(drawing.rows.every(row => row.marks === null)).toBe(true);
    expect(drawing.rows[0].contextNote).toContain('4, 2 or 0');
    expect(drawing.rows[1].contextNote).toContain('up to four');
  });

  it('preserves minimum coverage in 2011 germination and establishment without fixing the eight marks to one topic', () => {
    const card = get('agsci-2011-hl-q1e');
    expect(card.answerVariants).toHaveLength(4);
    for (const variant of card.answerVariants!) {
      const effective = {...card,rows:variant.rows};
      const claims = Object.fromEntries(variant.rows.map(row => [row.id,Array.from({length:row.group!.claimMax},(_,i)=>i)]));
      expect(marksClaimed(effective,{},claims)).toBe(10);
      for (const row of variant.rows) expect(marksClaimed(effective,{},{[row.id]:claims[row.id]})).toBeLessThan(10);
    }
  });

  it('awards the first correct immunity and vegetative-propagation point three marks in either order', () => {
    for (const id of ['agsci-2011-hl-q1c','agsci-2011-hl-q1j']) {
      const card = get(id);
      expect(card.rows).toHaveLength(2);
      for (const row of card.rows) {
        expect(marksClaimed(card,{},{[row.id]:[0]})).toBe(3);
        expect(marksClaimed(card,{},{[row.id]:[1]})).toBe(3);
        expect(marksClaimed(card,{},{[row.id]:[1,0]})).toBe(5);
      }
    }
    const yeast = get('agsci-2011-hl-q9a');
    expect(yeast.tariffModel.kind).toBe('questionTotal');
    expect(yeast.totalMarks).toBe(12);
    expect(yeast.rows[0].contextNote).toContain('At least one point must concern brewing');
  });

  it('scores the unusual Ordinary tariffs in the order the scheme prints', () => {
    const tf = get('agsci-2010-ol-q7');
    const expected = [0,1,2,3,4,5,8,11,14,17,20];
    for (let n = 0; n <= 10; n++) {
      expect(marksClaimed(tf, {}, { 'r-1': Array.from({ length:n }, (_,i) => 9-i) })).toBe(expected[n]);
    }
    const plants = get('agsci-2010-ol-q5');
    expect(marksClaimed(plants, {}, { 'r-1':[1,2,3,4,5,6] })).toBe(18);
    expect(marksClaimed(plants, {}, { 'r-1':[0,1,2,3,4,5,6] })).toBe(20);
    const sand = get('agsci-2010-ol-q1b');
    const effective = { ...sand, rows:sand.answerVariants!.find(v => v.id === 'sand')!.rows };
    expect(marksClaimed(effective, { 'r-1':'yes' }, { 'r-3':[4] })).toBe(9);
    expect(marksClaimed(effective, { 'r-1':'yes', 'r-2':'yes' }, { 'r-3':[4] })).toBe(12);
  });

  it('keeps Ordinary source diagrams, complete genetic crosses and open method menus', () => {
    for (const id of ['q6a','q10ai','q10bi','q13cii']) {
      const card = get(`agsci-2010-ol-${id}`);
      expect(card.kind).toBe('diagram');
      expect(card.figure?.solution).not.toBe(true);
      if (card.kind !== 'diagram') throw new Error('Expected a diagram card');
      expect(card.labelKey.length).toBe(id === 'q13cii' ? 2 : 3);
      expect(readFileSync(resolve(__dirname, `../public${card.figure!.src}`)).length).toBeGreaterThan(1000);
    }
    expect(get('agsci-2010-ol-q13bi').totalMarks).toBe(12);
    expect(get('agsci-2010-ol-q13bii').totalMarks).toBe(21);
    expect(get('agsci-2010-ol-q13bii').sourceMaterial?.pages).toEqual([10,11]);
    expect(get('agsci-2010-ol-q8c').answerVariants).toHaveLength(6);
    expect(get('agsci-2010-ol-q3a').rows[0].group?.options).toEqual(['Friesian','Jersey','Simmental']);
  });

  it('keeps 2011 Ordinary pooled tariffs whole and caps the two open dispersal answers', () => {
    const year = ordinary.filter(card => card.year === 2011);
    expect(year).toHaveLength(81);
    const tariffs = [[7,7,2,1,1,1,1], [7,7,2,2,1,1], [7,7,2,2,2], [6,6,2,2,1,1,1,1]];
    for (const [index, steps] of tariffs.entries()) {
      const card = get(`agsci-2011-ol-q${index + 1}`);
      expect(card.totalMarks).toBe(20);
      expect(card.rows[0].group?.perOptionSteps).toEqual(steps);
      let total = 0;
      for (let n = 1; n <= steps.length; n++) {
        total += steps[n - 1];
        expect(marksClaimed(card, {}, { 'r-1': Array.from({ length:n }, (_,i) => i) })).toBe(total);
      }
    }
    const bean = get('agsci-2011-ol-q1');
    expect(bean.answerVariants).toHaveLength(6);
    const pairs = bean.answerVariants!.map(variant => variant.rows[0].group!.options.slice(-2));
    expect(new Set(pairs.map(pair => [...pair].sort().join('|'))).size).toBe(6);
    for (const variant of bean.answerVariants!) {
      expect(variant.rows[0].group?.options).toHaveLength(7);
      expect(tariffReconciles({ ...bean, rows:variant.rows })).toBe(true);
    }
  });

  it('preserves the 2011 barley asterisks without charging twice for repeated gametes or phenotypes', () => {
    expect(get('agsci-2011-ol-q13b-f1').totalMarks).toBe(8);
    const f2 = get('agsci-2011-ol-q13b-f2');
    expect(f2.totalMarks).toBe(22);
    const points = Object.fromEntries(f2.rows.filter(row => !row.group).map(row => [row.id,'yes' as const]));
    const groups = Object.fromEntries(f2.rows.filter(row => row.group).map(row => [row.id,Array.from({length:row.group!.claimMax},(_,i)=>i)]));
    expect(marksClaimed(f2, points, groups)).toBe(22);
    expect(f2.rows[0].group?.options).toEqual(['Ss','Ss']);
    expect(f2.rows[2].group?.options).toEqual(['SS','Ss','Ss','ss']);
    expect(marksClaimed(f2, {}, { 'r-3':[1,2] })).toBe(4);
    expect(f2.rows[0].contextNote).toContain('only one parent');
    expect(['i','ii','iii'].map(part => get(`agsci-2011-ol-q13c${part}`).totalMarks)).toEqual([2,3,4]);
  });

  it('keeps open examples as marking menus and retains judgement-based experimental criteria', () => {
    expect(get('agsci-2011-ol-q11b').answerVariants).toHaveLength(2);
    expect(get('agsci-2011-ol-q11ciii').answerVariants?.map(variant => variant.id)).toEqual(['barley','potatoes']);
    for (const [id, marks] of [['q12a-system',15],['q12a-enzyme',15],['q12cii',12]] as const) {
      const card = get(`agsci-2011-ol-${id}`);
      expect(card.totalMarks).toBe(marks);
      expect(card.tariffModel.kind).toBe('questionTotal');
      expect(card.rows.every(row => row.kind === 'criterion' && row.marks === null)).toBe(true);
    }
    for (const sample of ['a','b','c']) {
      const card = get(`agsci-2011-ol-q10d-${sample}`);
      expect(card.totalMarks).toBe(4);
      expect(card.figure?.src).toContain('soil-triangle');
      expect(card.stem).toContain('Soil C: 60%, 25%, 15%');
    }
  });


  it('keeps both 2012 three-of-four choices on one card without summing alternatives', () => {
    for (const [key, ref] of [['q7a', 'Q7(a)'], ['q8c', 'Q8(c)']] as const) {
      expect(higher.filter(card => card.questionRef.startsWith(`2012 HL ${ref}`))).toHaveLength(1);
      const card = get(`agsci-2012-hl-${key}`);
      expect(card.questionText).toContain('three');
      expect(card.stem ?? '').not.toContain('Practice choice');
      const task = review.tasks.find(task => task.cardIds.includes(card.id))!;
      expect(task.selection).toMatchObject({ kind: 'closed', choose: 3, pooled: true });
      expect(tariffReconciles(card)).toBe(true);
    }
    const terms = get('agsci-2012-hl-q7a');
    expect(terms.totalMarks).toBe(12);
    expect(terms.rows[0].group?.options).toHaveLength(4);
    expect(marksClaimed(terms, {}, { 'r-1': [0, 1, 3] })).toBe(12);
    expect(marksClaimed(terms, {}, { 'r-1': [0, 1, 2, 3] })).toBe(12);
    const pairs = get('agsci-2012-hl-q8c');
    expect(pairs.totalMarks).toBe(24);
    expect(pairs.rows).toHaveLength(8);
    expect(pairs.tariffModel).toEqual({ kind: 'bestNofParts', answer: 6, ofParts: 8, perPart: 4 });
  });

  it('preserves the 2012 pooled first-correct scales and repeated answer fields', () => {
    const tissues = get('agsci-2012-hl-q1d');
    for (let n=0;n<=6;n++) {
      expect(marksClaimed(tissues,{}, {'r-1':Array.from({length:n},(_,i)=>i)})).toBe([0,2,4,6,8,9,10][n]);
    }
    const meiosis = get('agsci-2012-hl-q1h');
    expect(meiosis.rows[0].group?.options).toHaveLength(3);
    expect(marksClaimed(meiosis,{}, {'r-1':[2]})).toBe(4);
    expect(marksClaimed(meiosis,{}, {'r-1':[0,1,2]})).toBe(10);
    const tramlines = get('agsci-2012-hl-q1f');
    expect(tramlines.answerVariants).toHaveLength(6);
    for (const variant of tramlines.answerVariants!) {
      const effective = {...tramlines,rows:variant.rows};
      expect(variant.rows[0].group?.options).toHaveLength(3);
      expect(marksClaimed(effective,{}, {'r-1':[2]})).toBe(4);
      expect(marksClaimed(effective,{}, {'r-1':[0,1,2]})).toBe(10);
    }
  });

  it('keeps partial drawing bands and the full nitrogen pool under manual marking', () => {
    for (const [key,total] of [['q1aii',6],['q2aii',10],['q3o1a',11],['q6ai',10],['q8a',24]] as const) {
      const card = get(`agsci-2012-hl-${key}`);
      expect(card.tariffModel.kind).toBe('questionTotal');
      expect(card.totalMarks).toBe(total);
      expect(card.rows.every(row => row.kind === 'criterion' && row.marks === null)).toBe(true);
    }
    expect(get('agsci-2012-hl-q2aii').rows[0].contextNote).toContain('4, 2 or 0');
    expect(get('agsci-2012-hl-q6ai').rows[1].contextNote).toContain('6, 3 or 0');
    expect(get('agsci-2012-hl-q8a').rows[1].verbatim).toContain('addition of artificial fertilisers');
    for (const key of ['q6ai','q6aii','q7bii']) expect(get(`agsci-2012-hl-${key}`).figure?.solution).toBe(true);
  });

  it('does not award extra marks for the repeated heterozygous oat offspring', () => {
    const card = get('agsci-2012-hl-q7bii');
    expect(card.rows.map(row => row.marks)).toEqual([2,2,3,3]);
    expect(card.rows[2].group?.options).toEqual(['BB','BE','EE']);
    expect(card.rows[3].group?.options).toEqual(['500mm (BB)','650mm (BE)','800mm (EE)']);
    expect(marksClaimed(card,{'r-1':'yes','r-2':'yes'}, {'r-3':[0,1,2],'r-4':[0,1,2]})).toBe(10);
    expect(marksClaimed(card,{}, {'r-3':[1],'r-4':[1]})).toBe(2);
    expect(card.stem).toContain('500 mm');
    expect(card.stem).toContain('800 mm');
    expect(card.rows[0].contextNote).toContain('F2');
  });

  it('retains open answer context and distinguishes source defects from scoring', () => {
    expect(get('agsci-2012-hl-q3o1bii').stem).toContain('First list four factors');
    expect(get('agsci-2012-hl-q3o2biii').stem).toContain('two breeds');
    expect(get('agsci-2012-hl-q2b').answerVariants).toHaveLength(3);
    expect(get('agsci-2012-hl-q7c').answerVariants).toHaveLength(7);
    expect(get('agsci-2012-hl-q3o1cii').answerVariants?.every(v=>v.rows[0].verbatim.includes('37°C'))).toBe(true);
    const map:PaperAnswerMap=JSON.parse(readFileSync(resolve(__dirname,'../public/paper-answers/2012/LC024ALP000EV.pdf.json'),'utf8'));
    expect(map.q.find(q=>q.n==='4')?.schemeNote).toContain('yellow-orange precipitate');
    expect(map.q.find(q=>q.n==='5')?.schemeNote).toContain('Earthing-up');
    expect(map.q.find(q=>q.n==='8')?.schemeNote).toContain('moisture content');
    const tissues=review.tasks.find(task=>task.cardIds.includes('agsci-2012-hl-q1d'))!;
    expect(tissues.examTopicIds).toContain('agricultural-science-higher-animal-physiology-respiratory-system');
  });

  it('records edition-specific defects beside the unchanged original schemes', () => {
    expect(review.paperReviews).toHaveLength(29);
    for (const paper of review.paperReviews) {
      expect(paper.wholePaperVisualReview).toBe('reviewed');
      expect(paper.selectionDirectives.every(cue => cue.classification !== 'pending')).toBe(true);
    }
    const readMap = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(resolve(__dirname, `../public/paper-answers/2010/${fileid}.json`),'utf8'));
    expect(readMap('LC024ALP000IV.pdf').q.find(q => q.n === '7')?.schemeNote).toContain('D/d');
    const irish = readMap('LC024GLP000IV.pdf');
    expect(irish.q.find(q => q.n === '6')?.schemeNote).toContain('Clóraplast');
    expect(irish.q.find(q => q.n === '9')?.schemeNote).toContain('62');
    expect(irish.q.find(q => q.n === '13')?.schemeNote).toContain('C/c');
    expect(readMap('LC024GLP000EV.pdf').q.find(q => q.n === '12')?.schemeNote).toContain('28');
    for (const fileid of ['LC024ALP000IV.pdf','LC024GLP000IV.pdf']) {
      expect(preferredAnswersUrl('agricultural-science',2010,fileid,'old-storage')).toBe(`/paper-answers/2010/${fileid}.json`);
    }
    const irish2011: PaperAnswerMap = JSON.parse(readFileSync(resolve(__dirname, '../public/paper-answers/2011/LC024ALP000IV.pdf.json'),'utf8'));
    expect(irish2011.q.find(q => q.n === '1')?.schemeNote).toContain('2.5–3.5');
    expect(irish2011.q.find(q => q.n === '6')?.schemeNote).toContain('high protein');
    expect(irish2011.q.find(q => q.n === '7')?.schemeNote).toContain('CcFf');
    expect(preferredAnswersUrl('agricultural-science',2011,'LC024ALP000IV.pdf','old-storage')).toBe('/paper-answers/2011/LC024ALP000IV.pdf.json');
  });

  it('publishes every printed 2026 Higher item choice as one card', () => {
    const year = higher.filter(card => card.year === 2026);
    expect(year).toHaveLength(91);
    const pools: Array<[string, string, number, number, number]> = [
      ['q2b', 'Q2(b)', 4, 3, 10], ['q7', 'Q7', 6, 4, 10], ['q10a', 'Q10(a)', 3, 2, 5], ['q18ciii', 'Q18(c)(iii)', 5, 1, 3],
    ];
    for (const [key, ref, options, claim, marks] of pools) {
      expect(year.filter(card => card.questionRef === `2026 HL ${ref}`), key).toHaveLength(1);
      const card = get(`agsci-2026-hl-${key}`);
      expect(card.totalMarks).toBe(marks);
      expect(card.rows).toHaveLength(1);
      expect(card.rows[0].group?.options, key).toHaveLength(options);
      expect(card.rows[0].group?.claimMax, key).toBe(claim);
      expect(card.stem ?? '').not.toContain('Practice choice');
      expect(tariffReconciles(card)).toBe(true);
      expect(review.tasks.find(task => task.cardIds.includes(card.id))!.selection).toMatchObject({ kind: 'closed', pooled: true });
    }
    const benefits = get('agsci-2026-hl-q7');
    expect(benefits.rows[0].group?.perOptionSteps).toEqual([5, 3, 1, 1]);
    expect(marksClaimed(benefits, {}, { 'r-1': [3] })).toBe(5);
    expect(marksClaimed(benefits, {}, { 'r-1': [0, 1, 2, 5] })).toBe(10);
    // Method A or B: one card; naming a method commits its route.
    const sowing = get('agsci-2026-hl-q14ci');
    expect(sowing.totalMarks).toBe(9);
    expect(sowing.rows.map(row => row.route)).toEqual(['A', 'A', 'B', 'B']);
    expect(tariffReconciles(sowing)).toBe(true);
    expect(marksClaimed(sowing, { 'r-1': 'yes' }, { 'r-2': [0, 1] })).toBe(9);
    expect(marksClaimed(sowing, { 'r-1': 'yes', 'r-3': 'yes' }, {})).toBe(3);
    // Section A questions total 10 and Section B 50 for every candidate.
    const units = census.questionMarkChecks.filter(check => check.year === 2026 && check.level === 'higher');
    expect(units).toHaveLength(18);
    for (const check of units) expect(check.candidateTotalsFromScheme).toEqual([Number(check.question.slice(1)) <= 12 ? 10 : 50]);
  });

  it('keeps 2026 Higher drawings, graph and fertility comparisons under the published manual totals', () => {
    for (const [key, total] of [['q8b', 5], ['q13ci', 12], ['q15bi', 10], ['q17aiv', 11]] as const) {
      const card = get(`agsci-2026-hl-${key}`);
      expect(card.tariffModel.kind).toBe('questionTotal');
      expect(card.totalMarks).toBe(total);
      expect(card.rows.every(row => row.kind === 'criterion' && row.marks === null)).toBe(true);
    }
    expect(get('agsci-2026-hl-q15bi').figure?.solution).toBe(true);
    expect(get('agsci-2026-hl-q17aiv').rows[0].contextNote).toContain('4+4+3');
    expect(get('agsci-2026-hl-q11bi').rows[0].contextNote).toContain('floor space alone');
    const map: PaperAnswerMap = JSON.parse(readFileSync(resolve(__dirname, '../public/paper-answers/2026/LC024ALP000EV.pdf.json'), 'utf8'));
    expect(map.q.find(q => q.n === '11')?.schemeNote).toContain('feed space');
    expect(map.q.find(q => q.n === '17')?.schemeNote).toContain('4+4+3');
    expect(preferredAnswersUrl('agricultural-science', 2026, 'LC024ALP000EV.pdf', 'old-storage')).toBe('/paper-answers/2026/LC024ALP000EV.pdf.json');
    const flocculation = get('agsci-2026-hl-q13biii');
    expect(flocculation.totalMarks).toBe(16);
    expect(flocculation.rows[0].contextNote).toContain('Compulsory');
    expect(marksClaimed(flocculation, { 'r-1': 'yes' }, { 'r-2': [0, 1, 2] })).toBe(16);
    const minerals = get('agsci-2026-hl-q4c');
    expect(minerals.answerVariants?.map(variant => variant.id)).toEqual(['magnesium', 'phosphorus', 'selenium']);
    expect(get('agsci-2026-hl-q16av').answerVariants?.map(variant => variant.id)).toEqual(['no', 'yes']);
    for (const card of higher.filter(card => card.year === 2026)) {
      const specification = resolveCurriculumSpecification(card.subjectId, card.year)!;
      expect(card.specificationId).toBe(specification.id);
      expect(card.curriculumNodeIds?.[0]).toBe(card.topicId);
      for (const id of card.curriculumNodeIds!) expect(findCanonicalTopic(specification, id)).toBeDefined();
    }
  });

  it('publishes every printed 2026 Ordinary item choice as one card and keeps answer-identification ticks whole', () => {
    const year = ordinary.filter(card => card.year === 2026);
    expect(year).toHaveLength(85);
    const pools: Array<[string, number, number, number]> = [
      ['q1a', 4, 3, 6], ['q4a', 3, 2, 6], ['q4b', 9, 1, 2], ['q5a', 4, 3, 7], ['q9a', 5, 3, 10],
      ['q9bi', 3, 2, 5], ['q10a', 3, 2, 6], ['q14ai', 4, 3, 6], ['q18bii', 4, 3, 9],
    ];
    for (const [key, options, claim, marks] of pools) {
      const card = get(`agsci-2026-ol-${key}`);
      expect(year.filter(candidate => candidate.questionRef.split(' — ')[0] === card.questionRef), key).toHaveLength(1);
      expect(card.totalMarks, card.id).toBe(marks);
      expect(card.rows[0].group?.options, key).toHaveLength(options);
      expect(card.rows[0].group?.claimMax, key).toBe(claim);
      expect(card.stem ?? '').not.toContain('Practice choice');
      expect(tariffReconciles(card)).toBe(true);
      expect(review.tasks.find(task => task.cardIds.includes(card.id))!.selection).toMatchObject({ kind: 'closed', pooled: true });
    }
    const cattle = get('agsci-2026-ol-q5a');
    expect(cattle.rows[0].group?.perOptionSteps).toEqual([1, 2, 4]);
    expect(marksClaimed(cattle, {}, { 'r-1': [2] })).toBe(1);
    expect(marksClaimed(cattle, {}, { 'r-1': [0, 1, 3] })).toBe(7);
    const organic = get('agsci-2026-ol-q6');
    expect(organic.rows[0].group?.perOptionSteps).toEqual([1, 1, 2, 2, 4]);
    expect(marksClaimed(organic, {}, { 'r-1': [0, 1, 2, 3, 4] })).toBe(10);
    for (const id of ['q2a', 'q11a', 'q14aiii', 'q15bi', 'q16aii', 'q16ci', 'q16di', 'q17ai']) {
      const card = get(`agsci-2026-ol-${id}`);
      expect(card.rows).toHaveLength(1);
      expect(review.tasks.find(task => task.cardIds.includes(card.id))!.selection.kind).toBe('none');
    }
    for (const id of ['q4a', 'q11b', 'q12bi', 'q18bii']) {
      const card = ordinary.find(candidate => candidate.id === `agsci-2026-ol-${id}`)!;
      expect(card.kind, id).toBe('diagram');
      if (card.kind !== 'diagram') throw new Error('Expected a diagram card');
      expect(card.figure?.solution).not.toBe(true);
    }
    for (const id of ['q3bi', 'q14bi']) expect(get(`agsci-2026-ol-${id}`).figure?.solution).toBe(true);
    const units = census.questionMarkChecks.filter(check => check.year === 2026 && check.level === 'ordinary');
    expect(units).toHaveLength(18);
    for (const check of units) expect(check.candidateTotalsFromScheme).toEqual([Number(check.question.slice(1)) <= 12 ? 10 : 50]);
  });

  it('keeps 2026 Ordinary drawings, graph and calculation under the published awards', () => {
    for (const [key, total] of [['q12ai', 4], ['q14ci', 10], ['q18bi', 9]] as const) {
      const card = get(`agsci-2026-ol-${key}`);
      expect(card.tariffModel.kind).toBe('questionTotal');
      expect(card.totalMarks).toBe(total);
    }
    expect(get('agsci-2026-ol-q17c').totalMarks).toBe(22);
    expect(get('agsci-2026-ol-q16dii').rows.map(row => row.marks)).toEqual([2, 4]);
    const map: PaperAnswerMap = JSON.parse(readFileSync(resolve(__dirname, '../public/paper-answers/2026/LC024GLP000EV.pdf.json'), 'utf8'));
    expect(map.q.find(q => q.n === '11')?.schemeNote).toContain('(b)');
    expect(map.q.find(q => q.n === '13')?.schemeNote).toContain('part (ii)');
    expect(preferredAnswersUrl('agricultural-science', 2026, 'LC024GLP000EV.pdf', 'old-storage')).toBe('/paper-answers/2026/LC024GLP000EV.pdf.json');
    for (const card of ordinary.filter(card => card.year === 2026)) {
      const specification = resolveCurriculumSpecification(card.subjectId, card.year)!;
      expect(card.specificationId).toBe(specification.id);
      expect(card.curriculumNodeIds?.[0]).toBe(card.topicId);
      for (const id of card.curriculumNodeIds!) expect(findCanonicalTopic(specification, id)).toBeDefined();
    }
  });

  it('reconciles all 88 original 2025 Higher cards and publishes every printed item choice as one card', () => {
    const year = higher.filter(card => card.year === 2025);
    expect(year).toHaveLength(89);
    const tasks = review.tasks.filter(task => task.questionRef.startsWith('2025 HL'));
    expect(tasks).toHaveLength(89);
    const states = tasks.map(task => (task as { originalCard?: string }).originalCard);
    expect(states.filter(state => state === 'unchanged')).toHaveLength(81);
    expect(states.filter(state => state === 'corrected-in-place')).toHaveLength(3);
    expect(states.filter(state => state === 'added')).toHaveLength(5);
    expect(year.filter(card => card.questionRef.includes(' — '))).toHaveLength(0);
    for (const [key, marks] of [['q2a', 10], ['q2bii', 2], ['q6b', 4], ['q7b', 5], ['q12a', 10], ['q15b', 3]] as const) {
      const card = get(`agsci-2025-hl-${key}`);
      expect(card.totalMarks, key).toBe(marks);
      expect(tariffReconciles(card), key).toBe(true);
      expect(review.tasks.find(task => task.cardIds.includes(card.id))!.selection).toMatchObject({ kind: 'closed', pooled: true });
    }
    // Q12 is one any-four-of-five card; the other four prompt IDs are progress aliases of it.
    const q12 = get('agsci-2025-hl-q12a');
    expect(q12.questionRef).toBe('2025 HL Q12');
    expect(q12.rows[0].group?.options).toHaveLength(5);
    expect(q12.rows[0].group?.perOptionSteps).toEqual([4, 4, 1, 1]);
    expect(q12.rows[0].group?.options[2]).toContain('Close to surface to maximise photosynthesis');
    expect(marksClaimed(q12, {}, { 'r-1': [0, 1, 2, 4] })).toBe(10);
    expect(marksClaimed(q12, {}, { 'r-1': [3] })).toBe(4);
    expect((review as { withdrawnCardIds: Record<string, string> }).withdrawnCardIds).toMatchObject({
      'agsci-2025-hl-q12b': 'agsci-2025-hl-q12a', 'agsci-2025-hl-q12c': 'agsci-2025-hl-q12a',
      'agsci-2025-hl-q12d': 'agsci-2025-hl-q12a', 'agsci-2025-hl-q12e': 'agsci-2025-hl-q12a',
    });
    for (const key of ['b', 'c', 'd', 'e']) expect(year.some(card => card.id === `agsci-2025-hl-q12${key}`)).toBe(false);
    const plants = get('agsci-2025-hl-q15b');
    expect(plants.rows[0].group?.options).toEqual(['A: Cleavers', 'B: Chicory', 'C: Silverweed', 'D: Oilseed rape']);
    expect(higher.find(card => card.id === 'agsci-2025-hl-q15b')!.kind).toBe('diagram');
    const capillarity = get('agsci-2025-hl-q14bi');
    expect(capillarity.totalMarks).toBe(17);
    expect(marksClaimed(capillarity, { 'r-2': 'yes' }, { 'r-1': [0, 1, 2, 3] })).toBe(17);
    expect(get('agsci-2025-hl-q15c').answerVariants).toHaveLength(3);
    for (const variant of get('agsci-2025-hl-q15c').answerVariants!) {
      expect(tariffReconciles({ ...get('agsci-2025-hl-q15c'), rows: variant.rows })).toBe(true);
    }
    const units = census.questionMarkChecks.filter(check => check.year === 2025 && check.level === 'higher');
    expect(units).toHaveLength(18);
    for (const check of units) expect(check.candidateTotalsFromScheme).toEqual([Number(check.question.slice(1)) <= 12 ? 10 : 50]);
    const map: PaperAnswerMap = JSON.parse(readFileSync(resolve(__dirname, '../public/paper-answers/2025/LC024ALP000EV.pdf.json'), 'utf8'));
    expect(map.q.find(q => q.n === '14')?.schemeNote).toContain('17');
  });

  it('reconciles the original 2025 Ordinary cards, splits the fused Q9(b) parts and publishes each item choice as one card', () => {
    const year = ordinary.filter(card => card.year === 2025);
    expect(year).toHaveLength(91);
    // 90 tasks from this review plus the earlier reviewed Q8(b) correction.
    const tasks = review.tasks.filter(task => task.questionRef.startsWith('2025 OL'));
    expect(tasks).toHaveLength(91);
    const states = tasks.map(task => (task as { originalCard?: string }).originalCard);
    expect(states.filter(state => state === 'unchanged')).toHaveLength(68);
    expect(states.filter(state => state === 'corrected-in-place')).toHaveLength(3);
    expect(states.filter(state => state === 'added')).toHaveLength(19);
    for (const [key, ref, options, claim, marks] of [['q1ai', 'Q1(a)(i)', 4, 3, 6], ['q7a', 'Q7(a)', 4, 3, 6], ['q14ciii', 'Q14(c)(iii)', 3, 2, 8]] as const) {
      expect(year.filter(card => card.questionRef.startsWith(`2025 OL ${ref}`)), ref).toHaveLength(1);
      const card = get(`agsci-2025-ol-${key}`);
      expect(card.totalMarks).toBe(marks);
      expect(card.rows[0].group?.options).toHaveLength(options);
      expect(card.rows[0].group?.claimMax).toBe(claim);
      expect(tariffReconciles(card)).toBe(true);
    }
    expect(get('agsci-2025-ol-q1ai').questionRef).toBe('2025 OL Q1(a)(i)');
    expect(get('agsci-2025-ol-q9bi-ii').questionRef).toBe('2025 OL Q9(b)(i)');
    expect(get('agsci-2025-ol-q9bi-ii').totalMarks).toBe(3);
    expect(get('agsci-2025-ol-q9biii-iv').questionRef).toBe('2025 OL Q9(b)(iii)');
    expect(get('agsci-2025-ol-q9bii').totalMarks).toBe(2);
    expect(get('agsci-2025-ol-q14a-ii').answerVariants?.map(variant => variant.id)).toEqual(['potatoes', 'barley', 'kale']);
    expect(get('agsci-2025-ol-q17d').answerVariants?.map(variant => variant.id)).toEqual(['beef', 'dairy', 'sheep']);
    for (const variant of get('agsci-2025-ol-q17d').answerVariants!) {
      expect(tariffReconciles({ ...get('agsci-2025-ol-q17d'), rows: variant.rows })).toBe(true);
    }
    const units = census.questionMarkChecks.filter(check => check.year === 2025 && check.level === 'ordinary');
    expect(units).toHaveLength(18);
    for (const check of units) expect(check.candidateTotalsFromScheme).toEqual([Number(check.question.slice(1)) <= 12 ? 10 : 50]);
  });

  it('reconciles all 72 original 2024 Higher cards, keeps each item choice on one card and discloses the Q18 total', () => {
    const year = higher.filter(card => card.year === 2024);
    expect(year).toHaveLength(81);
    const tasks = review.tasks.filter(task => task.questionRef.startsWith('2024 HL'));
    expect(tasks).toHaveLength(81);
    const states = tasks.map(task => (task as { originalCard?: string }).originalCard);
    expect(states.filter(state => state === 'unchanged')).toHaveLength(63);
    expect(states.filter(state => state === 'corrected-in-place')).toHaveLength(9);
    expect(states.filter(state => state === 'added')).toHaveLength(9);
    expect(year.filter(card => card.questionRef.includes(' — '))).toHaveLength(0);
    for (const [key, marks] of [['q2ai', 4], ['q6a', 10], ['q6bii', 4], ['q15aiii', 4]] as const) {
      const card = get(`agsci-2024-hl-${key}`);
      expect(card.totalMarks, key).toBe(marks);
      expect(tariffReconciles(card), key).toBe(true);
      expect(review.tasks.find(task => task.cardIds.includes(card.id))!.selection).toMatchObject({ kind: 'closed', pooled: true });
    }
    const breeds = get('agsci-2024-hl-q2ai');
    expect(breeds.rows[0].group?.options).toEqual(['A: Landrace', 'B: Blue Leicester', 'C: Simmental']);
    expect(marksClaimed(breeds, {}, { 'r-1': [1, 2] })).toBe(4);
    const sheep = get('agsci-2024-hl-q6a');
    expect(sheep.questionRef).toBe('2024 HL Q6(a)');
    expect(sheep.rows.map(row => row.group?.options.length)).toEqual([4, 4]);
    expect(marksClaimed(sheep, {}, { 'r-1': [2, 3], 'r-2': [2, 3] })).toBe(10);
    // A named factor alone earns its 5; any two printed dominant features earn 6+2.
    expect(marksClaimed(get('agsci-2024-hl-q17a'), {}, { 'r-1': [2] })).toBe(5);
    expect(marksClaimed(get('agsci-2024-hl-q18aiii'), {}, { 'r-1': [2] })).toBe(6);
    expect(marksClaimed(get('agsci-2024-hl-q18aiii'), {}, { 'r-1': [2, 5] })).toBe(8);
    for (const id of ['agsci-2024-hl-q2ai', 'agsci-2024-hl-q5a', 'agsci-2024-hl-q9bi', 'agsci-2024-hl-q13aii', 'agsci-2024-hl-q18aii']) {
      expect(higher.find(card => card.id === id)!.kind, id).toBe('diagram');
    }
    expect(get('agsci-2024-hl-q16bi').rows[0].accepts).toContain('valid comparison with Sample 2 or Sample 3');
    const units = census.questionMarkChecks.filter(check => check.year === 2024 && check.level === 'higher');
    expect(units).toHaveLength(18);
    for (const check of units) {
      const expected = check.question === 'Q18' ? 54 : Number(check.question.slice(1)) <= 12 ? 10 : 50;
      expect(check.candidateTotalsFromScheme, check.question).toEqual([expected]);
    }
    expect(units.find(check => check.question === 'Q18')!.sourceException).toContain('54');
    const map: PaperAnswerMap = JSON.parse(readFileSync(resolve(__dirname, '../public/paper-answers/2024/LC024ALP000EV.pdf.json'), 'utf8'));
    expect(map.q.find(q => q.n === '18')?.schemeNote).toContain('54');
  });

  it('reconciles all 77 original 2024 Ordinary cards and adds the five missing parts', () => {
    const year = ordinary.filter(card => card.year === 2024);
    expect(year).toHaveLength(82);
    const tasks = review.tasks.filter(task => task.questionRef.startsWith('2024 OL'));
    expect(tasks).toHaveLength(82);
    const states = tasks.map(task => (task as { originalCard?: string }).originalCard);
    expect(states.filter(state => state === 'unchanged')).toHaveLength(74);
    expect(states.filter(state => state === 'corrected-in-place')).toHaveLength(3);
    expect(states.filter(state => state === 'added')).toHaveLength(5);
    for (const key of ['q5a', 'q6ai', 'q6aii', 'q7a', 'q13aii']) {
      expect(review.tasks.find(task => task.cardIds.includes(`agsci-2024-ol-${key}`))!.selection).toMatchObject({ kind: 'closed', pooled: true });
    }
    // Tick and X answers: the paper crop asks, the scheme crop answers after reveal.
    for (const id of ['agsci-2024-ol-q1a', 'agsci-2024-ol-q14aii']) {
      const card = ordinary.find(candidate => candidate.id === id)!;
      expect(card.kind === 'diagram' || card.kind === 'question').toBe(true);
      expect((card as { questionFigure?: { src: string } }).questionFigure?.src, id).toContain('agsci-2024-ol-paper-');
      expect((card as { figure?: { solution?: boolean } }).figure?.solution, id).toBe(true);
    }
    expect(get('agsci-2024-ol-q13biii').rows[0].verbatim).toBe('B');
    expect(get('agsci-2024-ol-q14bi').rows[0].verbatim).toBe('B');
    expect(get('agsci-2024-ol-q11aii').rows[0].verbatim).toBe('A');
    const ways = get('agsci-2024-ol-q14cii');
    expect(ways.rows.map(row => row.group?.options.length)).toEqual([6, 6]);
    expect(marksClaimed(ways, {}, { 'r-1': [0, 1] })).toBe(4);
    expect(marksClaimed(ways, {}, { 'r-1': [0, 1], 'r-2': [0, 1] })).toBe(8);
    const hay = get('agsci-2024-ol-q14d');
    expect(hay.rows).toHaveLength(6);
    expect(marksClaimed(hay, { 'r-1': 'yes' })).toBe(2);
    expect(get('agsci-2024-ol-q2biii').stem).not.toContain('Single file race');
    const units = census.questionMarkChecks.filter(check => check.year === 2024 && check.level === 'ordinary');
    expect(units).toHaveLength(18);
    for (const check of units) expect(check.candidateTotalsFromScheme, check.question).toEqual([Number(check.question.slice(1)) <= 12 ? 10 : 50]);
  });

  it('reconciles all 81 original 2023 Higher cards and adds the three missing parts', () => {
    const year = higher.filter(card => card.year === 2023);
    expect(year).toHaveLength(85);
    const tasks = review.tasks.filter(task => task.questionRef.startsWith('2023 HL'));
    expect(tasks).toHaveLength(85);
    const states = tasks.map(task => (task as { originalCard?: string }).originalCard);
    expect(states.filter(state => state === 'unchanged')).toHaveLength(57);
    expect(states.filter(state => state === 'corrected-in-place')).toHaveLength(24);
    expect(states.filter(state => state === 'added')).toHaveLength(4);
    for (const key of ['q2a', 'q2b', 'q4a', 'q13bii', 'q17biii', 'q17c', 'q18ai']) {
      expect(review.tasks.find(task => task.cardIds.includes(`agsci-2023-hl-${key}`))!.selection).toMatchObject({ kind: 'closed', pooled: true });
    }
    // Printed item choices list every item on one card.
    const stages = get('agsci-2023-hl-q2a');
    expect(stages.rows).toHaveLength(1);
    expect(stages.rows[0].group?.options).toHaveLength(3);
    expect(marksClaimed(stages, {}, { 'r-1': [1, 2] })).toBe(6);
    const treatments = get('agsci-2023-hl-q4a');
    expect(treatments.rows[0].group?.options).toHaveLength(4);
    expect(marksClaimed(treatments, {}, { 'r-1': [1, 2, 3] })).toBe(6);
    // Pools list every published point; descending tariffs pay their steps.
    expect(get('agsci-2023-hl-q13dii').rows[0].group?.options).toHaveLength(9);
    expect(marksClaimed(get('agsci-2023-hl-q13dii'), {}, { 'r-1': [4, 6] })).toBe(6);
    expect(get('agsci-2023-hl-q14ci').rows[0].group?.options).toContain('repeat (at least 10 times)');
    const factors = get('agsci-2023-hl-q13ai');
    expect(factors.totalMarks).toBe(14);
    expect(marksClaimed(factors, {}, { 'r-1': [0, 5, 1] })).toBe(12);
    const milk = get('agsci-2023-hl-q18bii');
    expect(marksClaimed(milk, {}, { 'r-1': [0, 2, 3] })).toBe(9);
    expect(marksClaimed(milk, {}, { 'r-1': [0, 2, 3], 'r-2': [0, 2, 3] })).toBe(18);
    // Alternative methods are answer variants, each reaching the full tariff alone.
    for (const [id, routes] of [['agsci-2023-hl-q13c', ['laboratory', 'field']], ['agsci-2023-hl-q15a', ['hand', 'sediment', 'sieve']]] as const) {
      const card = get(id);
      const variants = (card as { answerVariants?: Array<{ id: string; rows: typeof card.rows }> }).answerVariants ?? [];
      expect(variants.map(variant => variant.id), id).toEqual(routes);
      for (const variant of variants) expect(tariffReconciles({ ...card, rows: variant.rows }), `${id} ${variant.id}`).toBe(true);
    }
    // Added parts carry the paper's own table and photographs.
    expect(get('agsci-2023-hl-q7a').totalMarks).toBe(10);
    expect(get('agsci-2023-hl-q7a').figure?.src).toContain('agsci-2023-hl-paper-goat-cow-table');
    expect(get('agsci-2023-hl-q7b').rows[0].group?.perOptionSteps).toEqual([3, 3, 2, 2]);
    expect(get('agsci-2023-hl-q18av').rows.map(row => row.verbatim)).toEqual(['1 A', '2 D', '3 B', '4 C']);
    for (const id of ['agsci-2023-hl-q8c', 'agsci-2023-hl-q15cii', 'agsci-2023-hl-q16aii']) {
      expect(get(id).stem, id).not.toMatch(/\b0 Control|7000 Cumulaitve|50 Current farm/);
      expect(get(id).figure?.src, id).toBeTruthy();
    }
    const units = census.questionMarkChecks.filter(check => check.year === 2023 && check.level === 'higher');
    expect(units).toHaveLength(18);
    for (const check of units) expect(check.candidateTotalsFromScheme, check.question).toEqual([Number(check.question.slice(1)) <= 12 ? 10 : 50]);
  });

  it('reconciles all 76 original 2023 Ordinary cards and adds the five missing parts', () => {
    const year = ordinary.filter(card => card.year === 2023);
    expect(year).toHaveLength(81);
    const tasks = review.tasks.filter(task => task.questionRef.startsWith('2023 OL'));
    expect(tasks).toHaveLength(81);
    const states = tasks.map(task => (task as { originalCard?: string }).originalCard);
    expect(states.filter(state => state === 'unchanged')).toHaveLength(57);
    expect(states.filter(state => state === 'corrected-in-place')).toHaveLength(19);
    expect(states.filter(state => state === 'added')).toHaveLength(5);
    for (const key of ['q1a', 'q2a', 'q16ai', 'q18biii']) {
      expect(review.tasks.find(task => task.cardIds.includes(`agsci-2023-ol-${key}`))!.selection).toMatchObject({ kind: 'closed', pooled: true });
    }
    const breeds = get('agsci-2023-ol-q2a');
    expect(breeds.rows[0].group?.options).toHaveLength(5);
    expect(marksClaimed(breeds, {}, { 'r-1': [3, 4] })).toBe(5);
    expect((breeds as { labelKey?: Array<{ letter: string }> }).labelKey?.map(label => label.letter)).toEqual(['A', 'B', 'C', 'D', 'E']);
    // First-correct awards are no longer pinned to one printed position.
    for (const id of ['agsci-2023-ol-q4', 'agsci-2023-ol-q8a', 'agsci-2023-ol-q9b-iii', 'agsci-2023-ol-q13aii', 'agsci-2023-ol-q15b']) {
      expect(get(id).tariffModel.kind, id).toBe('orderedSplit');
      expect(get(id).rows.every(row => row.marks === null), id).toBe(true);
    }
    // The fused Q10(b) card keeps (i); (ii) and (iii) are their own cards.
    expect(get('agsci-2023-ol-q10b-i-iii').questionRef).toBe('2023 OL Q10(b)(i)');
    expect(cards.filter(card => card.questionRef.startsWith('2023 OL Q10(b)(ii)'))).toHaveLength(1);
    expect(get('agsci-2023-ol-q10biii').rows[0].verbatim).toBe('Bull 1');
    const milk = get('agsci-2023-ol-q16ai');
    const variants = (milk as { answerVariants?: Array<{ id: string; rows: typeof milk.rows }> }).answerVariants ?? [];
    expect(variants.map(variant => variant.id)).toEqual(['resazurin', 'tbc']);
    for (const variant of variants) expect(tariffReconciles({ ...milk, rows: variant.rows }), variant.id).toBe(true);
    expect(get('agsci-2023-ol-q11').tariffModel.kind).toBe('questionTotal');
    expect(get('agsci-2023-ol-q14biv').totalMarks).toBe(12);
    expect(get('agsci-2023-ol-q7a').figure?.src).toContain('agsci-2023-ol-paper-ewe-mothering');
    expect(get('agsci-2023-ol-q15aii').figure?.src).toContain('agsci-2023-ol-paper-compacted-soil');
    for (const id of ['agsci-2023-ol-q1b', 'agsci-2023-ol-q6aiii', 'agsci-2023-ol-q10bii', 'agsci-2023-ol-q13bii', 'agsci-2023-ol-q14bi', 'agsci-2023-ol-q15aii', 'agsci-2023-ol-q15b']) {
      expect(get(id).stem, id).not.toMatch(/pH probe Universal|Silage % Dry Matter|Bull 1 Bull 2|Grass production relative|^W X$|Soil particle Water|Parent Material Or/);
    }
    const units = census.questionMarkChecks.filter(check => check.year === 2023 && check.level === 'ordinary');
    expect(units).toHaveLength(18);
    for (const check of units) expect(check.candidateTotalsFromScheme, check.question).toEqual([Number(check.question.slice(1)) <= 12 ? 10 : 50]);
    expect(units.find(check => check.question === 'Q15')!.rule).toBe('(a) with either (b) or (c)');
  });

  it('reconciles all 96 original 2022 Higher cards and adds the five missing parts', () => {
    const year = higher.filter(card => card.year === 2022);
    expect(year).toHaveLength(101);
    const tasks = review.tasks.filter(task => task.questionRef.startsWith('2022 HL'));
    expect(tasks).toHaveLength(101);
    const states = tasks.map(task => (task as { originalCard?: string }).originalCard);
    expect(states.filter(state => state === 'unchanged')).toHaveLength(89);
    expect(states.filter(state => state === 'corrected-in-place')).toHaveLength(7);
    expect(states.filter(state => state === 'added')).toHaveLength(5);
    for (const key of ['q2a', 'q10b', 'q10c', 'q13aiii', 'q15ai', 'q18aii']) {
      expect(review.tasks.find(task => task.cardIds.includes(`agsci-2022-hl-${key}`))!.selection).toMatchObject({ kind: 'closed', pooled: true });
    }
    // Named-crop and named-animal answers are routes, never one mixed pool.
    const variantsOf = (id: string) => (get(id) as { answerVariants?: Array<{ id: string; rows: ReturnType<typeof get>['rows'] }> }).answerVariants ?? [];
    expect(variantsOf('agsci-2022-hl-q10b').map(variant => variant.id)).toEqual(['kale', 'miscanthus', 'osr']);
    expect(variantsOf('agsci-2022-hl-q10c').map(variant => variant.id)).toEqual(['kale', 'miscanthus', 'osr']);
    expect(variantsOf('agsci-2022-hl-q15ai')).toHaveLength(5);
    for (const id of ['agsci-2022-hl-q10b', 'agsci-2022-hl-q10c', 'agsci-2022-hl-q15ai']) {
      for (const variant of variantsOf(id)) expect(tariffReconciles({ ...get(id), rows: variant.rows }), `${id} ${variant.id}`).toBe(true);
    }
    expect(get('agsci-2022-hl-q2b').rows[0].group?.options).toHaveLength(11);
    expect(get('agsci-2022-hl-q16ci').totalMarks).toBe(11);
    expect(get('agsci-2022-hl-q17bii').rows[1].verbatim).toContain('to those of both parents');
    // Added: the drawn calf stomach, the growth stage, the seed comparison, the airflow arrows and the weed advice.
    expect(get('agsci-2022-hl-q9ai').tariffModel.kind).toBe('questionTotal');
    expect(get('agsci-2022-hl-q13aiv').rows[0].verbatim).toBe('Reproductive stage');
    expect(get('agsci-2022-hl-q13biii').rows[0].group?.options).toHaveLength(12);
    const airflow = get('agsci-2022-hl-q14cii');
    expect((airflow as { questionFigure?: { src: string } }).questionFigure?.src).toContain('agsci-2022-hl-paper-calf-shed-airflow');
    expect((airflow as { figure?: { solution?: boolean } }).figure?.solution).toBe(true);
    expect(get('agsci-2022-hl-q18bii').rows[0].group?.options).toHaveLength(9);
    const units = census.questionMarkChecks.filter(check => check.year === 2022 && check.level === 'higher');
    expect(units).toHaveLength(18);
    for (const check of units) expect(check.candidateTotalsFromScheme, check.question).toEqual([Number(check.question.slice(1)) <= 12 ? 10 : 50]);
  });

  it('reconciles all 95 original 2022 Ordinary cards, folds Q4(b) into one card and adds the six missing parts', () => {
    const year = ordinary.filter(card => card.year === 2022);
    expect(year).toHaveLength(98);
    const tasks = review.tasks.filter(task => task.questionRef.startsWith('2022 OL'));
    expect(tasks).toHaveLength(98);
    const states = tasks.map(task => (task as { originalCard?: string }).originalCard);
    expect(states.filter(state => state === 'unchanged')).toHaveLength(71);
    expect(states.filter(state => state === 'corrected-in-place')).toHaveLength(19);
    expect(states.filter(state => state === 'added')).toHaveLength(6);
    for (const key of ['q2ai', 'q3a', 'q7aiii', 'q12a']) {
      expect(review.tasks.find(task => task.cardIds.includes(`agsci-2022-ol-${key}`))!.selection).toMatchObject({ kind: 'closed', pooled: true });
    }
    // The five per-statement Q4(b) cards are withdrawn into the table card and read through aliases.
    for (const key of ['i', 'ii', 'iii', 'iv', 'v']) {
      expect(year.some(card => card.id === `agsci-2022-ol-q4b${key}`)).toBe(false);
      expect(CARD_ID_ALIASES[`agsci-2022-ol-q4b${key}`]).toBe('agsci-2022-ol-q4b');
      expect((review as { withdrawnCardIds: Record<string, string> }).withdrawnCardIds[`agsci-2022-ol-q4b${key}`]).toBe('agsci-2022-ol-q4b');
    }
    expect(get('agsci-2022-ol-q4b').rows).toHaveLength(5);
    expect(get('agsci-2022-ol-q4b').totalMarks).toBe(10);
    // The indicator and meter methods, and each named nutrient, are answer routes.
    const variantsOf = (id: string) => (get(id) as { answerVariants?: Array<{ id: string; rows: ReturnType<typeof get>['rows'] }> }).answerVariants ?? [];
    expect(variantsOf('agsci-2022-ol-q3a').map(variant => variant.id)).toEqual(['indicator', 'meter']);
    expect(variantsOf('agsci-2022-ol-q7aiii').map(variant => variant.id)).toEqual(['nitrogen', 'phosphorus', 'potassium', 'sulphur', 'calcium', 'magnesium']);
    for (const id of ['agsci-2022-ol-q3a', 'agsci-2022-ol-q7aiii']) {
      for (const variant of variantsOf(id)) expect(tariffReconciles({ ...get(id), rows: variant.rows }), `${id} ${variant.id}`).toBe(true);
    }
    expect(get('agsci-2022-ol-q14civ').totalMarks).toBe(11);
    expect(get('agsci-2022-ol-q5a').rows[1].verbatim).toContain('produce calf or lamb');
    // Added: silage tests, soil-forming factors, the grazing diagram, the shaded graph and the two nitrogen calculations.
    expect(get('agsci-2022-ol-q15aii').tariffModel.kind).toBe('questionTotal');
    expect(get('agsci-2022-ol-q15aii').totalMarks).toBe(19);
    expect(get('agsci-2022-ol-q16aii').figure?.src).toContain('agsci-2022-ol-paper-grass-growth-curve');
    for (const id of ['agsci-2022-ol-q10a', 'agsci-2022-ol-q12a', 'agsci-2022-ol-q17bi', 'agsci-2022-ol-q17biii']) {
      expect(tariffReconciles(get(id)), id).toBe(true);
    }
    const units = census.questionMarkChecks.filter(check => check.year === 2022 && check.level === 'ordinary');
    expect(units).toHaveLength(18);
    for (const check of units) expect(check.candidateTotalsFromScheme, check.question).toEqual([Number(check.question.slice(1)) <= 12 ? 10 : 50]);
    expect(units.find(check => check.question === 'Q13')!.rule).toBe('(a) with either (b) or (c)');
    expect(units.find(check => check.question === 'Q16')!.rule).toBe('both (a) and (b) with either (c) or (d)');
  });

  it('reconciles all 101 original 2021 Higher cards and adds the five missing tasks', () => {
    const year = higher.filter(card => card.year === 2021);
    expect(year).toHaveLength(106);
    const tasks = review.tasks.filter(task => task.questionRef.startsWith('2021 HL'));
    expect(tasks).toHaveLength(106);
    const states = tasks.map(task => (task as { originalCard?: string }).originalCard);
    expect(states.filter(state => state === 'unchanged')).toHaveLength(71);
    expect(states.filter(state => state === 'corrected-in-place')).toHaveLength(30);
    expect(states.filter(state => state === 'added')).toHaveLength(5);
    // Named crops, disorders, systems, species, tests and preservation pools are answer routes, never one mixed pool.
    const variantsOf = (id: string) => (get(id) as { answerVariants?: Array<{ id: string; rows: ReturnType<typeof get>['rows'] }> }).answerVariants ?? [];
    for (const [key, ids] of [['q5a', ['kale', 'osr', 'miscanthus']], ['q5b', ['kale', 'osr', 'miscanthus']], ['q5c', ['kale', 'osr', 'miscanthus']],
      ['q11bii', ['bloat', 'acidosis']], ['q14a-housing', ['dairy', 'beef', 'lamb']], ['q14a-nutrition', ['dairy', 'beef', 'lamb']],
      ['q14a-production-targets', ['dairy', 'beef', 'lamb']], ['q14bii', ['pig', 'poultry', 'horse']], ['q15bii', ['solution-1', 'solution-2']],
      ['q16b', ['resazurin', 'total-bacterial-count']], ['q18a-crop-preservation', ['grain', 'potatoes', 'grass']]] as const) {
      const id = `agsci-2021-hl-${key}`;
      expect(variantsOf(id).map(variant => variant.id), id).toEqual(ids);
      expect(review.tasks.find(task => task.cardIds.includes(id))!.selection).toMatchObject({ kind: 'closed', pooled: true });
      for (const variant of variantsOf(id)) expect(tariffReconciles({ ...get(id), rows: variant.rows }), `${id} ${variant.id}`).toBe(true);
    }
    expect(get('agsci-2021-hl-q1b').tariffModel.kind).toBe('orderedSplit');
    expect(get('agsci-2021-hl-q17biv').rows.map(row => row.group?.perOption)).toEqual([1, 3]);
    expect(get('agsci-2021-hl-q16ai').tariffModel.kind).toBe('questionTotal');
    for (const id of ['agsci-2021-hl-q14cii', 'agsci-2021-hl-q14ciii', 'agsci-2021-hl-q15ai', 'agsci-2021-hl-q15aii']) {
      expect(get(id).rows.some(row => row.verbatim.includes(' — ')), id).toBe(false);
    }
    for (const id of ['agsci-2021-hl-q15bi', 'agsci-2021-hl-q15bii', 'agsci-2021-hl-q15biii', 'agsci-2021-hl-q15biv']) {
      expect(get(id).figure?.src, id).toContain('agsci-2021-hl-paper-organic-fertiliser-dm-graph');
    }
    expect(get('agsci-2021-hl-q10c').figure?.src).toContain('agsci-2021-hl-paper-sheep-milk-pie');
    expect(get('agsci-2021-hl-q17bi').figure?.src).toContain('agsci-2021-hl-paper-reference-soil-index');
    const units = census.questionMarkChecks.filter(check => check.year === 2021 && check.level === 'higher');
    expect(units).toHaveLength(18);
    for (const check of units) expect(check.candidateTotalsFromScheme, check.question).toEqual([Number(check.question.slice(1)) <= 12 ? 10 : 50]);
    expect(units.find(check => check.question === 'Q13')!.rule).toBe('(a) with either (b) or (c)');
  });

  it('reconciles all 111 original 2021 Ordinary cards and adds the two missing parts', () => {
    const year = ordinary.filter(card => card.year === 2021);
    expect(year).toHaveLength(113);
    const tasks = review.tasks.filter(task => task.questionRef.startsWith('2021 OL'));
    expect(tasks).toHaveLength(113);
    const states = tasks.map(task => (task as { originalCard?: string }).originalCard);
    expect(states.filter(state => state === 'unchanged')).toHaveLength(77);
    expect(states.filter(state => state === 'corrected-in-place')).toHaveLength(34);
    expect(states.filter(state => state === 'added')).toHaveLength(2);
    const variantsOf = (id: string) => (get(id) as { answerVariants?: Array<{ id: string; rows: ReturnType<typeof get>['rows'] }> }).answerVariants ?? [];
    for (const [key, ids] of [['q12b', ['landrace', 'large-white', 'rhode-island-red', 'irish-sport-horse']],
      ['q14b-iii', ['temperature', 'amount', 'sterile', 'timing']], ['q14b-iv', ['resazurin', 'tbc']],
      ['q16c-v', ['compaction', 'germination', 'disease']], ['q18b-iii', ['conformation', 'polled', 'smaller-calves']]] as const) {
      const id = `agsci-2021-ol-${key}`;
      expect(variantsOf(id).map(variant => variant.id), id).toEqual(ids);
      expect(review.tasks.find(task => task.cardIds.includes(id))!.selection).toMatchObject({ kind: 'closed', pooled: true });
      for (const variant of variantsOf(id)) expect(tariffReconciles({ ...get(id), rows: variant.rows }), `${id} ${variant.id}`).toBe(true);
    }
    // Q18(a)(i) carries the scheme's "Named crop 2", so Question 18 totals 50.
    expect(get('agsci-2021-ol-q18a-i-seedbed').totalMarks).toBe(9);
    expect(get('agsci-2021-ol-q4c').rows[0].group?.perOptionSteps).toEqual([3, 1]);
    expect(get('agsci-2021-ol-q11b-iv').figure?.src).toContain('agricultural-science-2021-OL-paper-p15-i0');
    expect(get('agsci-2021-ol-q18b-iii').figure?.src).toContain('agricultural-science-2021-OL-paper-p34-i0');
    // The census reader no longer files Q17(b)(ii)/(iii) under (a): the two former orphans are covered.
    for (const key of ['q17b-ii', 'q17b-iii']) expect(review.tasks.find(task => task.cardIds.includes(`agsci-2021-ol-${key}`))!.questionRef).toMatch(/Q17\(b\)/);
    const units = census.questionMarkChecks.filter(check => check.year === 2021 && check.level === 'ordinary');
    expect(units).toHaveLength(18);
    for (const check of units) expect(check.candidateTotalsFromScheme, check.question).toEqual([Number(check.question.slice(1)) <= 12 ? 10 : 50]);
    expect(units.find(check => check.question === 'Q18')!.rule).toBe('both (a) and (b) with either (c) or (d)');
  });

  it('authors every 2020 Higher task from the paper and scheme', () => {
    const year = higher.filter(card => card.year === 2020);
    expect(year).toHaveLength(60);
    const tasks = review.tasks.filter(task => task.questionRef.startsWith('2020 HL'));
    expect(tasks).toHaveLength(60);
    expect(tasks.every(task => (task as { originalCard?: string }).originalCard === 'added')).toBe(true);
    for (const card of year) {
      expect(tariffReconciles(card), card.id).toBe(true);
      // Examined on the pre-2021 specification: the nodes resolve by exam year.
      const specification = resolveCurriculumSpecification(card.subjectId, card.year)!;
      expect(card.specificationId).toBe(specification.id);
      for (const id of card.curriculumNodeIds!) expect(findCanonicalTopic(specification, id), `${card.id} ${id}`).toBeDefined();
    }
    // Q4(b) names one animal enzyme: the scheme marks catalase and amylase as separate methods.
    const enzyme = get('agsci-2020-hl-q4b');
    expect(enzyme.answerVariants?.map(variant => variant.id)).toEqual(['catalase', 'amylase']);
    for (const variant of enzyme.answerVariants!) expect(tariffReconciles({ ...enzyme, rows: variant.rows }), variant.id).toBe(true);
    // Q8(c): any three of the four pairs is one card; each member of a chosen pair carries 2 + 2.
    expect(cards.filter(card => card.questionRef.startsWith('2020 HL Q8(c)'))).toHaveLength(1);
    const pairs = get('agsci-2020-hl-q8c');
    expect(pairs.totalMarks).toBe(24);
    expect(pairs.tariffModel).toEqual({ kind: 'bestNofParts', answer: 6, ofParts: 8, perPart: 4 });
    expect(review.tasks.find(task => task.cardIds.includes(pairs.id))!.selection).toMatchObject({ kind: 'closed', choose: 3, pooled: true });
    // Q1(e) prints 2(3) + 2(2): the first two correct locations earn 3, whichever two they are.
    const locations = get('agsci-2020-hl-q1e');
    expect(locations.rows[0].group?.perOptionSteps).toEqual([3, 3, 2, 2]);
    expect(marksClaimed(locations, {}, { 'r-1': [2, 3] })).toBe(6);
    expect(marksClaimed(locations, {}, { 'r-1': [0, 1, 2, 3] })).toBe(10);
    const units = census.questionMarkChecks.filter(check => check.year === 2020 && check.level === 'higher');
    expect(units).toHaveLength(10);
    for (const check of units) expect(check.candidateTotalsFromScheme, check.question).toEqual([check.question === 'Q1' ? 60 : 48]);
  });

  it('authors every 2020 Ordinary task, keeping each shared scale whole', () => {
    const year = ordinary.filter(card => card.year === 2020);
    expect(year).toHaveLength(52);
    const tasks = review.tasks.filter(task => task.questionRef.startsWith('2020 OL'));
    expect(tasks).toHaveLength(52);
    expect(tasks.every(task => (task as { originalCard?: string }).originalCard === 'added')).toBe(true);
    for (const card of year) {
      expect(tariffReconciles(card), card.id).toBe(true);
      const specification = resolveCurriculumSpecification(card.subjectId, card.year)!;
      expect(card.specificationId).toBe(specification.id);
      for (const id of card.curriculumNodeIds!) expect(findCanonicalTopic(specification, id), `${card.id} ${id}`).toBeDefined();
    }
    // A scale the scheme prints across several parts ("4 + 8(2)") is one card whose
    // rows carry no marks of their own: the first correct answers earn the higher award.
    const shared: Array<[string, string, number]> = [['q2', '4 + 8(2)', 20], ['q5', '4(4) + 2(2)', 20], ['q6', '2(4) + 6(2)', 20], ['q11c', '4 + 4(3)', 16],
      ['q12a', '3(4) + 4(2)', 20], ['q12b', '2(4) + 6(2)', 20], ['q12c', '2(4) + 2(2) + 8(1)', 20], ['q13a', '2(6) + 6(3)', 30], ['q13b', '2(5) + 5(4)', 30], ['q13c', '2(6) + 6(3)', 30]];
    for (const [key, notation, total] of shared) {
      const card = get(`agsci-2020-ol-${key}`);
      expect(card.tariffModel, key).toEqual({ kind: 'orderedSplit', notation });
      expect(card.totalMarks, key).toBe(total);
      expect(card.rows.every(row => row.marks === null), key).toBe(true);
    }
    // Winter or spring barley: one card, the two columns as mutually exclusive routes.
    expect(new Set(get('agsci-2020-ol-q13b').rows.map(row => row.route).filter(Boolean))).toEqual(new Set(['winter-barley', 'spring-barley']));
    for (const [key, routes] of [['q1b', ['sieve', 'feel', 'sedimentation']], ['q8c', ['colour', 'smell', 'squeeze', 'ph', 'taste', 'feel']], ['q9aiii', ['indicator', 'meter']]] as const) {
      const card = get(`agsci-2020-ol-${key}`);
      expect(card.answerVariants?.map(variant => variant.id), key).toEqual(routes);
      for (const variant of card.answerVariants!) expect(tariffReconciles({ ...card, rows: variant.rows }), `${key} ${variant.id}`).toBe(true);
    }
    // Every lettered diagram ships with its crop and a decoded label key.
    for (const [key, letters] of [['q4', 'ABCDEF'], ['q6', 'ABCDE'], ['q12b', 'ABC'], ['q12c', 'ABCDE']] as const) {
      const card = get(`agsci-2020-ol-${key}`);
      expect(card.figure?.src, key).toContain(`agsci-2020-ol-paper-`);
      expect((card as { labelKey?: Array<{ letter: string }> }).labelKey?.map(label => label.letter).join(''), key).toBe(letters);
    }
    const units = census.questionMarkChecks.filter(check => check.year === 2020 && check.level === 'ordinary');
    expect(units).toHaveLength(13);
    for (const check of units) expect(check.candidateTotalsFromScheme, check.question).toEqual([Number(check.question.slice(1)) <= 7 ? 20 : 60]);
    expect(units.find(check => check.question === 'Q13')!.choose).toBe(2);
  });

  it('authors every 2019 Higher task, keeping each Question 1 scale whole', () => {
    const year = higher.filter(card => card.year === 2019);
    expect(year).toHaveLength(61);
    const tasks = review.tasks.filter(task => task.questionRef.startsWith('2019 HL'));
    expect(tasks).toHaveLength(61);
    expect(tasks.every(task => (task as { originalCard?: string }).originalCard === 'added')).toBe(true);
    for (const card of year) {
      expect(tariffReconciles(card), card.id).toBe(true);
      const specification = resolveCurriculumSpecification(card.subjectId, card.year)!;
      expect(card.specificationId).toBe(specification.id);
      for (const id of card.curriculumNodeIds!) expect(findCanonicalTopic(specification, id), `${card.id} ${id}`).toBeDefined();
    }
    // A Question 1 scale printed across (i) and (ii) is one orderedSplit card; one pool keeps its steps.
    for (const [key, notation] of [['q1c', '4 + 1 + 5'], ['q1e', '4 + 1 + 5'], ['q1f', '4 + 1 + 1 + 4'], ['q6c', '4(2) + 4(1)']] as const)
      expect(get(`agsci-2019-hl-${key}`).tariffModel, key).toEqual({ kind: 'orderedSplit', notation });
    expect(get('agsci-2019-hl-q1a').rows[0].group?.perOptionSteps).toEqual([4, 1, 5]);
    expect(marksClaimed(get('agsci-2019-hl-q1a'), {}, { 'r-1': [2] })).toBe(4);
    for (const [key, count] of [['q2bii', 10], ['q3o1bii', 8], ['q4a', 2]] as const)
      expect(get(`agsci-2019-hl-${key}`).answerVariants, key).toHaveLength(count);
    const pairs = get('agsci-2019-hl-q8c');
    expect(pairs.tariffModel).toEqual({ kind: 'bestNofParts', answer: 6, ofParts: 8, perPart: 4 });
    expect(review.tasks.find(task => task.cardIds.includes(pairs.id))!.selection).toMatchObject({ kind: 'closed', choose: 3, pooled: true });
    const units = census.questionMarkChecks.filter(check => check.year === 2019 && check.level === 'higher');
    expect(units).toHaveLength(10);
    for (const check of units) expect(check.candidateTotalsFromScheme, check.question).toEqual([check.question === 'Q1' ? 60 : 48]);
  });

  it('authors every 2019 Ordinary task, keeping each shared scale whole', () => {
    const year = ordinary.filter(card => card.year === 2019);
    expect(year).toHaveLength(54);
    const tasks = review.tasks.filter(task => task.questionRef.startsWith('2019 OL'));
    expect(tasks).toHaveLength(54);
    expect(tasks.every(task => (task as { originalCard?: string }).originalCard === 'added')).toBe(true);
    for (const card of year) {
      expect(tariffReconciles(card), card.id).toBe(true);
      const specification = resolveCurriculumSpecification(card.subjectId, card.year)!;
      expect(card.specificationId).toBe(specification.id);
      for (const id of card.curriculumNodeIds!) expect(findCanonicalTopic(specification, id), `${card.id} ${id}`).toBeDefined();
    }
    for (const [key, notation, total] of [['q1', '2(4) + 6(2)', 20], ['q5', '2(4) + 6(2)', 20], ['q7', '3(4) + 4(2)', 20], ['q9c', '4(3) + 2 + 1', 15],
      ['q10a', '4 + 2(3)', 10], ['q13a', '7(4) + 2', 30], ['q13b', '5(4) + 5(2)', 30], ['q13d', '6 + 8(3)', 30]] as const) {
      const card = get(`agsci-2019-ol-${key}`);
      expect(card.tariffModel, key).toEqual({ kind: 'orderedSplit', notation });
      expect(card.totalMarks, key).toBe(total);
    }
    // Q13(d)(iv): the three demonstrations are mutually exclusive routes on the Q13(d) card.
    expect(new Set(get('agsci-2019-ol-q13d').rows.map(row => row.route).filter(Boolean))).toEqual(new Set(['bag', 'potometer', 'celery']));
    for (const [key, routes] of [['q8c', ['hill', 'lowland']], ['q11b', ['sandy', 'clay']], ['q12c', ['resazurin', 'agar']]] as const)
      expect(get(`agsci-2019-ol-${key}`).answerVariants?.map(variant => variant.id), key).toEqual(routes);
    // The 5 printed level with (iv)'s heading belongs to (iii): Q13(c) totals 10 + 5 + 5 + 10.
    expect(['q13ci', 'q13cii', 'q13ciii', 'q13civ'].map(key => get(`agsci-2019-ol-${key}`).totalMarks)).toEqual([10, 5, 5, 10]);
    for (const [key, letters] of [['q2', 'ABCDEF'], ['q5', 'ABC'], ['q13b', 'ABCD']] as const)
      expect((get(`agsci-2019-ol-${key}`) as { labelKey?: Array<{ letter: string }> }).labelKey?.map(label => label.letter).join(''), key).toBe(letters);
    const units = census.questionMarkChecks.filter(check => check.year === 2019 && check.level === 'ordinary');
    expect(units).toHaveLength(13);
    for (const check of units) expect(check.candidateTotalsFromScheme, check.question).toEqual([Number(check.question.slice(1)) <= 7 ? 20 : 60]);
  });

  it('authors every 2018 Higher task from the paper and scheme', () => {
    const year = higher.filter(card => card.year === 2018);
    expect(year).toHaveLength(57);
    const tasks = review.tasks.filter(task => task.questionRef.startsWith('2018 HL'));
    expect(tasks).toHaveLength(57);
    expect(tasks.every(task => (task as { originalCard?: string }).originalCard === 'added')).toBe(true);
    for (const card of year) {
      expect(tariffReconciles(card), card.id).toBe(true);
      const specification = resolveCurriculumSpecification(card.subjectId, card.year)!;
      expect(card.specificationId).toBe(specification.id);
      for (const id of card.curriculumNodeIds!) expect(findCanonicalTopic(specification, id), `${card.id} ${id}`).toBeDefined();
    }
    for (const [key, notation] of [['q1a', '4 + 3 + 3'], ['q1c', '2(3) + 2(2)'], ['q1d', '4 + 3 + 3'], ['q5c', '4(3) + 2(2)']] as const)
      expect(get(`agsci-2018-hl-${key}`).tariffModel, key).toEqual({ kind: 'orderedSplit', notation });
    expect(get('agsci-2018-hl-q3o2b').answerVariants?.map(variant => variant.id)).toEqual(['barley', 'wheat', 'oats', 'maize']);
    expect(get('agsci-2018-hl-q4c').answerVariants?.map(variant => variant.id)).toEqual(['amylase', 'catalase']);
    expect(get('agsci-2018-hl-q8c').tariffModel).toEqual({ kind: 'bestNofParts', answer: 6, ofParts: 8, perPart: 4 });
    // Q7(b): the matching ratio is one 4, 2, 0 award, so the cross totals 18.
    expect(get('agsci-2018-hl-q7b').totalMarks).toBe(18);
    const units = census.questionMarkChecks.filter(check => check.year === 2018 && check.level === 'higher');
    expect(units).toHaveLength(10);
    for (const check of units) expect(check.candidateTotalsFromScheme, check.question).toEqual([check.question === 'Q1' ? 60 : 48]);
  });

  it('authors every 2018 Ordinary task, keeping each Section One scale whole', () => {
    const year = ordinary.filter(card => card.year === 2018);
    expect(year).toHaveLength(60);
    const tasks = review.tasks.filter(task => task.questionRef.startsWith('2018 OL'));
    expect(tasks).toHaveLength(60);
    expect(tasks.every(task => (task as { originalCard?: string }).originalCard === 'added')).toBe(true);
    for (const card of year) {
      expect(tariffReconciles(card), card.id).toBe(true);
      const specification = resolveCurriculumSpecification(card.subjectId, card.year)!;
      expect(card.specificationId).toBe(specification.id);
      for (const id of card.curriculumNodeIds!) expect(findCanonicalTopic(specification, id), `${card.id} ${id}`).toBeDefined();
    }
    // Every Section One question prints one scale across all its parts.
    for (const [key, notation] of [['q1', '10 + 6 + 4(1)'], ['q2', '10 + 6 + 4(1)'], ['q3', '8 + 7 + 5(1)'], ['q4', '12 + 8(1)'], ['q6', '8 + 6 + 3(2)'], ['q7', '8 + 6 + 3(2)'],
      ['q11a', '2(4) + 4(2)']] as const)
      expect(get(`agsci-2018-ol-${key}`).tariffModel, key).toEqual({ kind: 'orderedSplit', notation });
    expect(get('agsci-2018-ol-q5').rows[0].group?.perOptionSteps).toEqual([3, 3, 3, 3, 3, 1, 1, 1, 1, 1]);
    // The paper prints a second "(a)" where the scheme has (b): the census reads it as (b).
    const q13 = census.papers.find(paper => paper.year === 2018 && paper.level === 'ordinary')!.baseTasks.map(task => task.ref);
    expect(q13).toContain('2018 OL Q13(b)(iv)');
    expect(get('agsci-2018-ol-q13div').answerVariants?.map(variant => variant.id)).toEqual(['pig', 'sheep', 'sheep-alternative']);
    // Part (b) of Q8 totals 24: (ii) takes the 4 printed on (iii)'s heading line.
    expect(['q8bi', 'q8bii', 'q8biii'].map(key => get(`agsci-2018-ol-${key}`).totalMarks)).toEqual([12, 8, 4]);
    const units = census.questionMarkChecks.filter(check => check.year === 2018 && check.level === 'ordinary');
    expect(units).toHaveLength(13);
    for (const check of units) expect(check.candidateTotalsFromScheme, check.question).toEqual([Number(check.question.slice(1)) <= 7 ? 20 : 60]);
  });

  it('authors every 2017 Higher task from the paper and scheme', () => {
    const year = higher.filter(card => card.year === 2017);
    expect(year).toHaveLength(58);
    const tasks = review.tasks.filter(task => task.questionRef.startsWith('2017 HL'));
    expect(tasks).toHaveLength(58);
    expect(tasks.every(task => (task as { originalCard?: string }).originalCard === 'added')).toBe(true);
    for (const card of year) {
      expect(tariffReconciles(card), card.id).toBe(true);
      const specification = resolveCurriculumSpecification(card.subjectId, card.year)!;
      expect(card.specificationId).toBe(specification.id);
      for (const id of card.curriculumNodeIds!) expect(findCanonicalTopic(specification, id), `${card.id} ${id}`).toBeDefined();
    }
    for (const [key, notation] of [['q1a', '2(4) + 2(1)'], ['q1b', '2(4) + 2(1)'], ['q1c', '2(4) + 2(1)'], ['q1h', '6 + 3 + 1'], ['q1i', '2(4) + 2(1)']] as const)
      expect(get(`agsci-2017-hl-${key}`).tariffModel, key).toEqual({ kind: 'orderedSplit', notation });
    expect(get('agsci-2017-hl-q1g').rows[0].group?.perOptionSteps).toEqual([6, 4]);
    for (const [key, count] of [['q3o2b', 4], ['q4a', 2], ['q4b', 4], ['q5aii', 7]] as const)
      expect(get(`agsci-2017-hl-${key}`).answerVariants, key).toHaveLength(count);
    expect(get('agsci-2017-hl-q8c').tariffModel).toEqual({ kind: 'bestNofParts', answer: 6, ofParts: 8, perPart: 4 });
    const units = census.questionMarkChecks.filter(check => check.year === 2017 && check.level === 'higher');
    expect(units).toHaveLength(10);
    for (const check of units) expect(check.candidateTotalsFromScheme, check.question).toEqual([check.question === 'Q1' ? 60 : 48]);
  });

  it('authors every 2017 Ordinary task from the paper and scheme', () => {
    const year = ordinary.filter(card => card.year === 2017);
    expect(year).toHaveLength(71);
    const tasks = review.tasks.filter(task => task.questionRef.startsWith('2017 OL'));
    expect(tasks).toHaveLength(71);
    expect(tasks.every(task => (task as { originalCard?: string }).originalCard === 'added')).toBe(true);
    for (const card of year) {
      expect(tariffReconciles(card), card.id).toBe(true);
      const specification = resolveCurriculumSpecification(card.subjectId, card.year)!;
      expect(card.specificationId).toBe(specification.id);
      for (const id of card.curriculumNodeIds!) expect(findCanonicalTopic(specification, id), `${card.id} ${id}`).toBeDefined();
    }
    // Section One: a scale across several parts is one orderedSplit card; one pool keeps its steps.
    for (const [key, notation] of [['q1', '2(7) + 6(1)'], ['q5', '2(5) + 5(2)'], ['q6', '5(3) + 5(1)']] as const)
      expect(get(`agsci-2017-ol-${key}`).tariffModel, key).toEqual({ kind: 'orderedSplit', notation });
    for (const key of ['q4', 'q7']) expect(get(`agsci-2017-ol-${key}`).rows[0].group?.perOptionSteps, key).toEqual([7, 7, 2, 2, 2]);
    expect(get('agsci-2017-ol-q11c').answerVariants?.map(variant => variant.id)).toEqual(['indicator', 'meter']);
    // The four pollution situations carry their own 2(3) each.
    expect(review.tasks.filter(task => task.questionRef.startsWith('2017 OL Q13(c)(ii)'))).toHaveLength(4);
    for (const [key, letters] of [['q2', 'ABCDEF'], ['q6', 'WXYZ'], ['q8di', 'ABCD']] as const)
      expect((get(`agsci-2017-ol-${key}`) as { labelKey?: Array<{ letter: string }> }).labelKey?.map(label => label.letter).join(''), key).toBe(letters);
    const units = census.questionMarkChecks.filter(check => check.year === 2017 && check.level === 'ordinary');
    expect(units).toHaveLength(13);
    for (const check of units) expect(check.candidateTotalsFromScheme, check.question).toEqual([Number(check.question.slice(1)) <= 7 ? 20 : 60]);
  });

  it('refuses Agricultural Science route siblings that differ only in which printed items were chosen', () => {
    // A printed any-N-of-M choice is ONE practice card (coordinator rule,
    // 2026-10-12). Siblings sharing a question address are allowed only for
    // separately marked required parts, never for an item choice.
    const closed = new Set(review.tasks.filter(task => task.selection.kind === 'closed').map(task => task.questionRef.split(' — ')[0]));
    const byBase = new Map<string, string[]>();
    for (const card of cards) {
      const base = card.questionRef.split(' — ')[0];
      byBase.set(base, [...(byBase.get(base) ?? []), card.id]);
      expect(card.id, card.id).not.toMatch(/-route-/);
      expect(`${card.stem ?? ''} ${card.questionText}`, card.id).not.toMatch(/Practice choice/);
    }
    const taskFor = (id: string) => review.tasks.find(task => task.cardIds.includes(id))!;
    for (const task of review.tasks.filter(task => task.selection.kind === 'closed')) {
      expect(task.cardIds, task.questionRef).toHaveLength(1);
      expect(task.questionRef, task.questionRef).not.toContain(' — ');
      expect((task.selection as { pooled?: boolean }).pooled, task.questionRef).toBe(true);
      // Any sibling at the same address must be a separately marked required
      // part (for example a definition beside the disease choice), never an
      // item of this printed choice.
      const options = ((task.selection as { options?: string[] }).options ?? []).map(option => option.toLowerCase());
      for (const id of byBase.get(task.questionRef) ?? []) {
        if (id === task.cardIds[0]) continue;
        const sibling = cards.find(card => card.id === id)!;
        expect(taskFor(id).selection.kind, id).not.toBe('closed');
        expect(options, id).not.toContain(sibling.questionRef.split(' — ')[1]?.toLowerCase());
      }
    }
    expect(closed.size).toBeGreaterThanOrEqual(35);
    for (const paper of census.papers) {
      for (const task of paper.baseTasks) expect(task.routes, task.ref).toHaveLength(1);
    }
  });

  it('awards 2010 first-correct marks independently of the named instrument', () => {
    const card = get('agsci-2010-hl-q1e');
    for (const first of [0, 1, 2]) expect(marksClaimed(card, {}, { 'r-1': [first] })).toBe(6);
    expect(marksClaimed(card, {}, { 'r-1': [1, 2] })).toBe(8);
    expect(marksClaimed(card, {}, { 'r-1': [0, 1, 2] })).toBe(10);
  });

  it('keeps the minimum ewe/ram and fasting/hanging coverage in every marking allocation', () => {
    for (const [id, allocations] of [['agsci-2010-hl-q8a', 3], ['agsci-2010-hl-q9a', 2]] as const) {
      const card = get(id);
      expect(card.answerVariants).toHaveLength(allocations);
      for (const variant of card.answerVariants!) {
        expect(variant.rows).toHaveLength(2);
        expect(variant.rows.every(row => row.group!.claimMax >= 1)).toBe(true);
        const effective = { ...card, rows: variant.rows };
        expect(tariffReconciles(effective)).toBe(true);
        const claims = Object.fromEntries(variant.rows.map(row => [row.id, Array.from({ length: row.group!.claimMax }, (_, i) => i)]));
        expect(marksClaimed(effective, {}, claims)).toBe(card.totalMarks);
        expect(marksClaimed(effective, {}, { 'r-1': claims['r-1'] })).toBeLessThan(card.totalMarks);
      }
    }
  });

  it('requires the compulsory nitrogen-fixation point for full marks without inventing a zero-score gate', () => {
    const card = get('agsci-2010-hl-q6cii');
    expect(marksClaimed(card, { 'r-1': 'yes' }, {})).toBe(3);
    expect(marksClaimed(card, {}, { 'r-2': [0] })).toBe(3);
    expect(marksClaimed(card, { 'r-1': 'yes' }, { 'r-2': [0] })).toBe(6);
  });

  it('keeps mixed comparisons discoverable under each assessed current topic without duplicating cards', () => {
    const card = get('agsci-2010-hl-q8c');
    for (const topic of ['agsci-4-3-1', 'agsci-3-3-2', 'agsci-4-3-3']) {
      expect(cardsForTopic(topic, cards).filter(candidate => candidate.id === card.id)).toHaveLength(1);
      expect(findCanonicalTopic(resolveCurriculumSpecification('agricultural-science', 2026)!, topic)).toBeDefined();
    }
  });

  it('keeps complete legacy method menus and official drawing solutions', () => {
    expect(get('agsci-2010-hl-q4a').answerVariants).toHaveLength(3);
    expect(get('agsci-2010-hl-q4d').answerVariants).toHaveLength(2);
    expect(get('agsci-2010-hl-q5aii').rows[0].group?.options).toHaveLength(17);
    for (const id of ['agsci-2010-hl-q1b', 'agsci-2010-hl-q7bii']) {
      const card = get(id);
      expect(card.figure?.solution).toBe(true);
      expect(card.figure?.alt).toBeTruthy();
      expect(readFileSync(resolve(__dirname, `../public${card.figure!.src}`)).length).toBeGreaterThan(1000);
    }
  });

  it('makes each reviewed Mark Bank task directly browsable in Atlas under its reviewed topic', () => {
    expect(atlas.markBankCards).toHaveLength(1920);
    for (const join of atlas.markBankCards) {
      const card = get(join.cardId);
      const task = review.tasks.find(task => task.cardIds.includes(join.cardId))!;
      const ids = examTopicIdsForQuestion('agricultural-science', card.level, card.year, 'main', join.n, 'single', 'ev', join.fileid);
      expect(ids).toEqual(task.examTopicIds);
      for (const topic of ids) {
        expect(siblingsFor('agricultural-science', topic).some(sibling =>
          sibling.year === join.year && sibling.fileid === join.fileid && sibling.n === join.n)).toBe(true);
      }
      const path = `/paper-answers/${join.year}/${join.fileid}.json`;
      expect(preferredAnswersUrl('agricultural-science', join.year, join.fileid, 'stale-storage')).toBe(path);
      const map = JSON.parse(readFileSync(resolve(__dirname, `../public${path}`), 'utf8'));
      const anchor = map.q.find((q: { n: string }) => q.n === join.n);
      expect(anchor.paperRegion[0].p).toBe(task.paperPage);
      expect(anchor.region[0].p).toBe(task.schemePage);
      if ('paperRegions' in task) expect(anchor.paperRegion).toEqual(task.paperRegions);
      if ('schemeRegions' in task) expect(anchor.region).toEqual(task.schemeRegions);
      expect(anchor.mode).toBe('crop');
      expect(anchor.parentN).toBe(card.questionRef.match(/Q(\d+)/)?.[1]);
    }
  });

  it('finds all 288 translated tasks under the same topics and practice identities', () => {
    expect(atlas.translatedMarkBankCards).toHaveLength(288);
    for (const join of atlas.translatedMarkBankCards) {
      const card = get(join.cardId);
      const english = atlas.markBankCards.find(candidate => candidate.cardId === join.cardId)!;
      const task = review.tasks.find(candidate => candidate.cardIds.includes(join.cardId))!;
      expect(join.n).toBe(english.n);
      const ids = examTopicIdsForQuestion('agricultural-science', card.level, join.year, 'main', join.n, 'single', 'iv', join.fileid);
      expect(ids).toEqual(task.examTopicIds);
      for (const topic of ids) {
        expect(siblingsFor('agricultural-science', topic).some(sibling =>
          sibling.lang === 'iv' && sibling.year === join.year && sibling.fileid === join.fileid && sibling.n === join.n)).toBe(true);
      }
      const map = JSON.parse(readFileSync(resolve(__dirname, `../public/paper-answers/${join.year}/${join.fileid}.json`), 'utf8')) as PaperAnswerMap;
      const anchor = map.q.find(question => question.n === join.n)!;
      expect(anchor.parentN).toBe(card.questionRef.match(/Q(\d+)/)?.[1]);
      expect(anchor.paperRegion?.length).toBeGreaterThan(0);
      expect(anchor.region.length).toBeGreaterThan(0);
      // Edition-specific tariffs must not overwrite the English Mark Bank.
      const differs = ['agsci-2010-ol-q9f', 'agsci-2010-ol-q12dii'].includes(join.cardId);
      expect(join.marksPerRoute).toBe(differs ? 20 : card.totalMarks);
      if (differs) {
        expect(card.totalMarks).toBe(18);
        expect(anchor.schemeNote).toContain('4 + 4 + 6 + 6');
      }
    }
  });

  it('does not shorten whole-question crops when independently selectable parts are appended', () => {
    for (const join of [...atlas.markBankCards, ...atlas.translatedMarkBankCards]) {
      const map = JSON.parse(readFileSync(resolve(__dirname, `../public/paper-answers/${join.year}/${join.fileid}.json`), 'utf8')) as PaperAnswerMap;
      const old = map.q.filter(question => !question.parentN);
      for (const question of old) {
        expect(paperRegionFor(map.q, question.n), `${join.year} ${join.fileid} Q${question.n}`).toEqual(paperRegionFor(old, question.n));
      }
    }
  });
});
