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
    expect(census.editionStatus.filter(edition => edition.independentCensus === 'open')).toHaveLength(62);
    expect(census.questionMarkChecks.filter(check => check.sourceException)).toHaveLength(1);
  });

  it('expands every three-of-four udder-labelling route at the published three-mark tariff', () => {
    const routes = cards.filter(c => c.id.startsWith('agsci-2023-hl-q18ai-route-'));
    expect(routes.map(c => c.id.split('-').at(-1)).sort()).toEqual(['abc', 'abd', 'acd', 'bcd']);
    for (const card of routes) {
      expect(card.totalMarks).toBe(3);
      expect(card.sourceMaterial?.pages).toEqual([37]);
      expect(card.questionText).toBe('Label any three parts of the structure of the udder.');
      expect(tariffReconciles(card)).toBe(true);
    }
    expect(get('agsci-2023-hl-q18ai-route-abc').rows[1].verbatim).toBe('Median suspensory ligament');
  });

  it('keeps the separate ram reason pools and their complete 3+1 marking menus', () => {
    const e = get('agsci-2022-ol-q2bii-route-e');
    const f = get('agsci-2022-ol-q2bii-route-f');
    expect(e.rows[0].group?.options).toHaveLength(8);
    expect(f.rows[0].group?.options).toHaveLength(5);
    expect(f.rows[0].group?.options).not.toContain('easy lambing');
    for (const card of [e, f]) {
      expect(card.totalMarks).toBe(4);
      expect(card.rows[0].group?.perOptionSteps).toEqual([3, 1]);
      expect(card.sourceMaterial?.pages).toEqual([5]);
      expect(tariffReconciles(card)).toBe(true);
      expect(marksClaimed(card, {}, { reasons: [0] })).toBe(3);
      expect(marksClaimed(card, {}, { reasons: [0, 1] })).toBe(4);
    }
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

  it('preserves both 2010 Q3 options and all 62 independently reviewed legacy tasks', () => {
    const legacy = cards.filter(card => card.year === 2010 && card.level === 'higher');
    expect(legacy).toHaveLength(62);
    expect(legacy.filter(card => card.questionRef.includes('Q3 Option One'))).toHaveLength(6);
    expect(legacy.filter(card => card.questionRef.includes('Q3 Option Two'))).toHaveLength(7);
    const diseaseRoutes = legacy.filter(card => card.id.startsWith('agsci-2010-hl-q3o2b-route-'));
    expect(diseaseRoutes.map(card => card.id).sort()).toEqual([
      'agsci-2010-hl-q3o2b-route-grass-tetany', 'agsci-2010-hl-q3o2b-route-hoose',
    ]);
    expect(diseaseRoutes.map(card => card.totalMarks)).toEqual([12, 12]);
    for (const card of legacy) {
      const specification = resolveCurriculumSpecification(card.subjectId, card.year)!;
      expect(card.specificationId).toBe(specification.id);
      expect(card.specVersion).toBe(specification.id);
      expect(card.specificationId).toBe('agricultural-science:legacy-current');
      expect(card.curriculumNodeIds?.length).toBeGreaterThan(0);
      for (const id of card.curriculumNodeIds!) expect(findCanonicalTopic(specification, id)).toBeDefined();
    }
  });

  it('expands both 2010 three-of-four tasks with their complete wording and tariffs', () => {
    const combinations = ['i-ii-iii', 'i-ii-iv', 'i-iii-iv', 'ii-iii-iv'];
    for (const [question, marks, rowCount] of [['q7a', 12, 3], ['q8c', 24, 6]] as const) {
      const routes = cards.filter(card => card.id.startsWith(`agsci-2010-hl-${question}-route-`));
      expect(routes.map(card => card.id.split('-route-')[1])).toEqual(combinations);
      expect(new Set(routes.map(card => card.questionText)).size).toBe(1);
      for (const candidate of routes) {
        const card = get(candidate.id);
        expect(card.totalMarks).toBe(marks);
        expect(card.rows).toHaveLength(rowCount);
        const claims = Object.fromEntries(card.rows.map(row => [row.id, [0, 1]]));
        expect(marksClaimed(card, {}, claims)).toBe(marks);
      }
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

  it('retains all 70 2011 Higher routes and separates shared genetic-cross marks from the three outcomes', () => {
    const legacy = higher.filter(card => card.year === 2011);
    expect(legacy).toHaveLength(70);
    const cross = get('agsci-2011-hl-q7b-cross');
    expect(cross.totalMarks).toBe(12);
    expect(cross.figure?.solution).toBe(true);
    expect(marksClaimed(cross, {'r-1':'yes','r-2':'yes'}, {'r-3':[0,1,2,3],'r-4':[0,1,2,3]})).toBe(12);
    for (const key of ['i','ii','iii']) expect(get(`agsci-2011-hl-q7b${key}`).totalMarks).toBe(4);
    expect(get('agsci-2011-hl-q7bi').rows[0].verbatim).toBe('12/16');
    expect(get('agsci-2011-hl-q7bii').rows[0].verbatim).toBe('4/16');
    expect(get('agsci-2011-hl-q7biii').rows[0].verbatim).toBe('3/16');
    const routes = legacy.filter(card => card.id.startsWith('agsci-2011-hl-q8c-route-'));
    expect(routes.map(card => card.id.split('-route-')[1])).toEqual(['i-ii-iii','i-ii-iv','i-iii-iv','ii-iii-iv']);
    for (const candidate of routes) {
      const card = get(candidate.id);
      expect(card.totalMarks).toBe(24);
      expect(card.rows).toHaveLength(6);
      expect(marksClaimed(card,Object.fromEntries(card.rows.map(row => [row.id,'yes'])),{})).toBe(24);
    }
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


  it('expands both 2012 three-of-four pools without summing alternative-route tariffs', () => {
    for (const [prefix,total,rows] of [['q7a',12,3],['q8c',24,6]] as const) {
      const routes = higher.filter(card => card.id.startsWith(`agsci-2012-hl-${prefix}-route-`));
      expect(routes.map(card => card.id.split('-route-')[1])).toEqual(['i-ii-iii','i-ii-iv','i-iii-iv','ii-iii-iv']);
      for (const candidate of routes) {
        const card = get(candidate.id);
        expect(card.totalMarks).toBe(total);
        expect(card.rows).toHaveLength(rows);
        expect(card.questionText).toContain('three');
        expect(card.stem).toContain('Practice choice:');
        const task = review.tasks.find(task => task.cardIds.includes(card.id))!;
        expect(task.selection.kind).toBe('closed');
        if (prefix === 'q8c') {
          const claims = Object.fromEntries(card.rows.map(row => [row.id,[0,1]]));
          expect(marksClaimed(card,{},claims)).toBe(24);
          expect(marksClaimed(card,{},Object.fromEntries(card.rows.map(row => [row.id,[0]])))).toBe(12);
        } else {
          expect(marksClaimed(card,Object.fromEntries(card.rows.map(row => [row.id,'yes'])),{})).toBe(12);
        }
      }
    }
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
    expect(review.paperReviews).toHaveLength(9);
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
    const card = get('agsci-2010-hl-q8c-route-i-ii-iv');
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
    expect(atlas.markBankCards).toHaveLength(368);
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

  it('finds all 298 translated tasks under the same topics and practice identities', () => {
    expect(atlas.translatedMarkBankCards).toHaveLength(298);
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
