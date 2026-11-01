import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/higher';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2023/LC098ALP039EV.pdf.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { preferredAnswersUrl } from '../components/PaperTrail/vaultResolve';
import { paperRegionFor, schemeRegionFor } from '../components/PaperTrail/paperRegion';
import type { PaperAnswerMap } from '../types/paperTrail';

const get = (id: string) => {
  const card = CARDS.find(candidate => candidate.id === id);
  expect(card, id).toBeDefined();
  if (!card || card.kind !== 'question') throw new Error(`Missing point card: ${id}`);
  return card;
};

describe('2023 Higher Home Economics recovered tasks', () => {
  it('preserves the Social Studies minimum headings and paired scheme marks', () => {
    const work = get('he-2023-hl-sc-q3ai');
    expect(work.rows.map(r => r.marks)).toEqual([4, 4, 12]);
    expect(work.rows[2].parts?.map(p => p.permittedMarks)).toEqual(Array(3).fill([0, 2, 4]));
    const welfare = get('he-2023-hl-sc-q3bii');
    expect(welfare.rows.map(r => r.parts?.map(p => p.permittedMarks))).toEqual([
      [[0, 2, 3], [0, 2, 4]], [[0, 2, 3], [0, 2, 4]],
    ]);
    expect(welfare.rows[0].contextNote?.split('\n\n')).toHaveLength(9);
    expect(welfare.rows[0].contextNote).toContain('eases transition from rent to mortgage');
    expect(get('he-2023-hl-sc-q3ci').rows.map(r => r.permittedMarks)).toEqual(Array(3).fill([0, 3, 6]));
    expect(get('he-2023-hl-sc-q3cii').rows[0].contextNote).toContain('Published 2023 examination guidance');
    expect(get('he-2023-hl-sc-q3cii').rows[0].contextNote).toContain('€7.91');
  });

  it('keeps complete cooking and packaging choices within their existing live identities', () => {
    const cooking = get('he-2023-hl-sc-q4aii-boiling');
    expect(cooking.answerVariants).toHaveLength(10);
    expect(cooking.answerVariants?.find(v => v.id === 'frying')?.rows[2].contextNote).toContain('some loss of B group vitamins');
    for (const variant of cooking.answerVariants ?? []) {
      expect(variant.rows.map(r => r.marks)).toEqual([3, 9, 12]);
      expect(variant.rows[1].parts?.map(p => p.permittedMarks)).toEqual(Array(3).fill([0, 2, 3]));
      expect(variant.rows[2].parts?.map(p => p.permittedMarks)).toEqual(Array(4).fill([0, 2, 3]));
      expect(tariffReconciles({ ...cooking, rows: variant.rows })).toBe(true);
    }
    const packaging = get('he-2023-hl-sc-q4aiii-glass');
    expect(packaging.answerVariants?.map(v => v.id)).toEqual(['glass', 'metal', 'paper', 'plastic', 'another-material']);
    for (const variant of packaging.answerVariants ?? []) {
      expect(variant.rows.map(r => r.permittedMarks)).toEqual([[0, 2, 4], [0, 3, 5], [0, 3, 5]]);
      expect(tariffReconciles({ ...packaging, rows: variant.rows })).toBe(true);
    }
    expect(packaging.answerVariants?.find(v => v.id === 'plastic')?.rows[2].contextNote).toContain('limited and non-renewable resources');
    expect(get('he-2023-hl-sc-q4cii').rows[0].contextNote).toContain('incorporated grill browns food by radiation');
  });

  it('reconciles all 2023 Higher practice tasks after the full paper and scheme review', () => {
    const cards = CARDS.filter(c => c.year === 2023 && !c.questionRef.includes('Deferred'));
    expect(cards).toHaveLength(59);
    expect(cards.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(749);
    for (const card of cards) {
      if (card.kind !== 'question') throw new Error(card.id);
      expect(tariffReconciles(card), card.id).toBe(true);
      for (const variant of card.answerVariants ?? []) expect(tariffReconciles({ ...card, rows: variant.rows }), `${card.id}/${variant.id}`).toBe(true);
    }
  });

  it('keeps the graduation-ball outfit context with its fabric and principle tasks', () => {
    const sketch = get('he-2023-hl-sc-q2ai');
    expect(sketch.rows[0].permittedMarks).toEqual([0, 2, 4, 6]);
    expect(sketch.rows[1].parts?.map(p => p.permittedMarks)).toEqual(Array(3).fill([0, 1, 2]));
    const fabric = get('he-2023-hl-sc-q2aii');
    expect(fabric.questionText).toBe('Suggest a suitable fabric for the outfit and give a reason for your choice.');
    expect(fabric.stem).toContain('Sketch and describe an outfit to wear for your graduation ball.');
    expect(fabric.rows.map(r => r.permittedMarks)).toEqual([[0, 3], [0, 2, 3]]);
    const principle = get('he-2023-hl-sc-q2aiii');
    expect(principle.stem).toContain('graduation ball');
    expect(principle.answerVariants?.map(v => v.id)).toEqual(['balance', 'emphasis', 'proportion', 'rhythm', 'another-principle']);
    for (const variant of principle.answerVariants ?? []) {
      expect(variant.rows[1].permittedMarks).toEqual([0, 3, 5]);
      expect(tariffReconciles({ ...principle, rows: variant.rows })).toBe(true);
    }
  });

  it('keeps one blended-fabric profile with complete component production and the original progress identity', () => {
    const blend = get('he-2023-hl-sc-q2b-wool-nylon');
    expect(CARDS.some(c => c.id === 'he-2023-hl-sc-q2b-cotton-polyester')).toBe(false);
    expect(blend.answerVariants?.map(v => v.id)).toEqual(['wool-nylon', 'cotton-polyester', 'another-blend']);
    expect(blend.answerVariants?.[0].rows[0].contextNote).toContain('wool fleece is graded');
    expect(blend.answerVariants?.[1].rows[0].contextNote).toContain('filaments solidify when cooled');
    for (const variant of blend.answerVariants ?? []) {
      expect(variant.rows[0].parts?.map(p => p.permittedMarks)).toEqual(Array(3).fill([0, 2, 3]));
      expect(variant.rows[0].contextNote).toContain('warp and weft');
      expect(variant.rows[2].contextNote).toContain('bed linen');
      expect(tariffReconciles({ ...blend, rows: variant.rows })).toBe(true);
    }
    const vintage = get('he-2023-hl-sc-q2ci');
    expect(vintage.rows.map(r => r.verbatim)).toEqual(['pattern', 'influences', 'accessories']);
    expect(vintage.rows.map(r => r.permittedMarks)).toEqual(Array(3).fill([0, 2, 3]));
    const cards = ['ai', 'aii', 'aiii', 'b-wool-nylon', 'ci', 'cii'].map(part => get(`he-2023-hl-sc-q2${part}`));
    expect(cards.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(55);
    for (const card of cards) expect(tariffReconciles(card), card.id).toBe(true);
  });

  it('keeps paired Elective 1 answers and the complete original light-property table', () => {
    const rooms = get('he-2023-hl-sc-q1aii');
    expect(rooms.stem).toContain('help people make their home');
    expect(rooms.sourceMaterial?.pages).toEqual([5]);
    expect(rooms.rows.map(r => r.parts?.map(p => p.permittedMarks))).toEqual([
      [[0, 2], [0, 2, 4]], [[0, 2], [0, 2, 4]],
    ]);
    expect(rooms.rows[0].contextNote).toContain('17°C to 21°C');
    const light = get('he-2023-hl-sc-q1bi');
    expect(light.figure?.solution).toBe(true);
    expect(light.figure?.alt).toContain('Refracted:');
    expect(light.rows).toHaveLength(4);
    for (const row of light.rows) {
      expect(row.parts?.map(p => p.permittedMarks)).toEqual([[0, 2], [0, 1, 2], [0, 1]]);
      expect(row.contextNote).toContain('matching explanation and home example');
    }
  });

  it('retains Elective 1 required headings, lighting choices and every published tariff', () => {
    const design = get('he-2023-hl-sc-q1ai');
    expect(design.rows.map(r => r.marks)).toEqual([8, 8, 4]);
    expect(design.rows[0].contextNote).toContain('ergonomics');
    expect(design.rows[1].contextNote).toContain('repurpose');
    const housing = get('he-2023-hl-sc-q1ci');
    expect(housing.rows.map(r => r.permittedMarks)).toEqual(Array(3).fill([0, 2, 4, 6]));
    const lighting = get('he-2023-hl-sc-q1bii');
    expect(lighting.answerVariants?.map(v => v.id)).toEqual(['cfl', 'led', 'another-type']);
    for (const variant of lighting.answerVariants ?? []) {
      expect(variant.rows[0].permittedMarks).toEqual([0, 2, 4]);
      expect(variant.rows[1].parts?.map(p => p.permittedMarks)).toEqual([[0, 2, 3], [0, 2, 3]]);
      expect(tariffReconciles({ ...lighting, rows: variant.rows })).toBe(true);
    }
    const cards = ['ai', 'aii', 'aiii', 'bi', 'bii', 'ci', 'cii'].map(part => get(`he-2023-hl-sc-q1${part}`));
    expect(cards.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(110);
    expect(cards.slice(0, 3).reduce((sum, c) => sum + c.totalMarks, 0)).toBe(50);
    expect(cards.slice(3, 5).reduce((sum, c) => sum + c.totalMarks, 0)).toBe(30);
    expect(cards.slice(5).reduce((sum, c) => sum + c.totalMarks, 0)).toBe(30);
    for (const card of cards) expect(tariffReconciles(card), card.id).toBe(true);
  });

  it('retains the fish tariff, complete factor guidance and compulsory management headings', () => {
    const fish = get('he-2023-hl-sb-q2a');
    expect(fish.stem).toContain('recommend consuming 2-3 portions');
    expect(fish.rows[0].parts?.map(p => p.permittedMarks)).toEqual(Array(5).fill([0, 1, 2, 3, 4]));
    expect(fish.rows[0].contextNote).toContain('1 mark for the nutrient, 1 for its type and 2 for function');
    expect(get('he-2023-hl-sb-q2c').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 3, 6], [0, 3, 6]]);
    expect(get('he-2023-hl-sb-q3a').rows[0].contextNote).toContain('influencers; etc.');
    const management = get('he-2023-hl-sb-q4a');
    expect(management.rows.map(r => r.verbatim)).toEqual([
      'Stages in the life cycle of the family', 'Employment patterns', 'Values', 'one other',
    ]);
    expect(management.rows.map(r => r.permittedMarks)).toEqual(Array(4).fill([0, 3, 5]));
    expect(management.rows[0].contextNote).toContain('decreased agility');
    expect(management.rows[1].contextNote).toContain('one parent working abroad');
    expect(management.rows[3].contextNote).toContain('Do not score a point already used');
  });

  it('marks retail points individually with the two-per-technique instruction and retains all three family terms', () => {
    const retail = get('he-2023-hl-sb-q4b');
    expect(retail.rows).toHaveLength(1);
    expect(retail.rows[0].parts?.map(p => p.permittedMarks)).toEqual(Array(4).fill([0, 3, 5]));
    expect(retail.rows[0].contextNote).toContain('Count no more than two points under the same technique');
    expect(retail.rows[0].contextNote).toContain('select its best two');
    expect(retail.rows[0].contextNote?.split('\n\n')).toHaveLength(8);
    expect(retail.rows[0].contextNote).toContain('loyalty cards money off coupons');
    const terms = get('he-2023-hl-sb-q5b');
    expect(terms.questionText).toContain('• universality of the family • kinship • monogamy.');
    expect(terms.rows.map(r => r.permittedMarks)).toEqual(Array(3).fill([0, 3, 5]));
    expect(terms.rows[2].contextNote).toContain('only one partner at a time');
  });

  it('keeps the agent and legal-option choices as single cards with independently scored name and detail', () => {
    const agent = get('he-2023-hl-sb-q3c');
    expect(agent.answerVariants).toHaveLength(11);
    expect(agent.answerVariants?.at(-2)?.rows[1].contextNote).toContain('crushed during handling');
    for (const variant of agent.answerVariants ?? []) {
      expect(variant.rows.map(r => r.marks)).toEqual([4, 8]);
      expect(variant.rows[1].parts?.map(p => p.permittedMarks)).toEqual([[0, 4], [0, 4]]);
      expect(tariffReconciles({ ...agent, rows: variant.rows })).toBe(true);
    }
    const legal = get('he-2023-hl-sb-q5c');
    expect(legal.answerVariants?.map(v => v.id)).toEqual(['deed-of-separation', 'judicial-separation', 'legal-nullity', 'divorce', 'another-option']);
    for (const variant of legal.answerVariants ?? []) {
      expect(variant.rows[0].permittedMarks).toEqual([0, 2, 3]);
      expect(variant.rows[1].parts?.map(p => p.permittedMarks)).toEqual(Array(3).fill([0, 2, 4]));
      expect(tariffReconciles({ ...legal, rows: variant.rows })).toBe(true);
    }
    expect(legal.answerVariants?.[3].rows[1].contextNote).toContain('at least two of the previous three years');
    for (let q = 2; q <= 5; q++) {
      const cards = ['a', 'b', 'c'].map(part => get(`he-2023-hl-sb-q${q}${part}`));
      expect(cards.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(50);
      for (const card of cards) expect(tariffReconciles(card), card.id).toBe(true);
    }
  });

  it('keeps the complete iron chart on the question side and all seven scheme sources in the reveal', () => {
    const card = get('he-2023-hl-sb-q1a');
    expect(card.questionFigure?.includesPrompt).toBe(false);
    expect(card.questionFigure?.solution).not.toBe(true);
    expect(card.questionFigure?.alt).toContain('confectionery, biscuits and preserves 11%');
    expect(card.stem).toContain('Adequate micronutrient intake during the teenage years');
    expect(card.stem).toContain('National Teen Food Survey II Report 2021');
    expect(card.rows[0].parts).toHaveLength(4);
    expect(card.rows[0].parts?.every(p => JSON.stringify(p.permittedMarks) === '[0,1,2,3,4,5]')).toBe(true);
    const guidance = card.rows[0].contextNote!;
    expect(guidance.split('\n\n')).toHaveLength(8);
    expect(guidance).toContain('Grains, rice & pasta 10%');
    expect(guidance).toContain('Other 14%');
    expect(tariffReconciles(card)).toBe(true);
  });

  it('keeps the absorption mark ladder and all budget-shopping guidance', () => {
    expect(get('he-2023-hl-sb-q1b').rows[0].parts?.map(p => p.permittedMarks))
      .toEqual(Array(4).fill([0, 3, 4, 5]));
    const shopping = get('he-2023-hl-sb-q1d');
    expect(shopping.rows[0].parts?.map(p => p.permittedMarks)).toEqual(Array(5).fill([0, 2, 4]));
    expect(shopping.rows[0].contextNote).toContain('food pyramid');
    expect(shopping.rows[0].contextNote).toContain('awareness of food labelling');
    expect(shopping.rows[0].contextNote).toMatch(/budget constraints; etc\.$/);
    expect(['a', 'b', 'c', 'd'].reduce((sum, part) => sum + get(`he-2023-hl-sb-q1${part}`).totalMarks, 0)).toBe(80);
  });

  it('preserves Section A marks while splitting the two separately priced prompts', () => {
    const cards = CARDS.filter(c => /^2023 HL Section A /.test(c.questionRef) && !c.questionRef.includes('Deferred'));
    expect(cards).toHaveLength(16);
    expect(cards.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(84);
    expect(get('he-2023-hl-sa-q4').totalMarks).toBe(4);
    expect(get('he-2023-hl-sa-q4-factors').totalMarks).toBe(2);
    expect(get('he-2023-hl-sa-q8').totalMarks).toBe(2);
    expect(get('he-2023-hl-sa-q8-uses').totalMarks).toBe(4);
    expect(get('he-2023-hl-sa-q4').rows[0].verbatim).toBe('the minimum');
    for (const card of cards) expect(tariffReconciles(card), card.id).toBe(true);
  });

  it('offers the published partial credit and restores omitted guidance', () => {
    expect(get('he-2023-hl-sa-q14').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 2, 3], [0, 2, 3]]);
    expect(get('he-2023-hl-sa-q12').rows[0].contextNote).toContain('borrower knows the exact amount');
    expect(get('he-2023-hl-sa-q12').rows[1].contextNote).toContain('they pay less if interest rates fall');
    expect(get('he-2023-hl-sa-q7').rows[0].contextNote).toContain('chemical raising agents');
    expect(get('he-2023-hl-sa-q7').rows[0].contextNote).toMatch(/etc\.$/);
    expect(get('he-2023-hl-sa-q6').questionText).toBe('Outline two benefits of including high fibre foods in the diet of adults.');
    const bacteria = get('he-2023-hl-sa-q3');
    expect(bacteria.figure?.solution).toBe(true);
    expect(bacteria.rows[0].parts?.map(p => p.marks)).toEqual([2, 1, 2, 1]);
    expect(bacteria.figure?.alt).toContain('Clostridium perfringens/welchii: vegetables');
  });

  it('maps both new short tasks into their existing Atlas question and curriculum topic', () => {
    for (const [id, n] of [['he-2023-hl-sa-q4-factors', '4'], ['he-2023-hl-sa-q8-uses', '8']]) {
      const card = get(id);
      const row = runtime.questionMappings.find(q => q[0] === 'h' && q[1] === 'e' && q[2] === 2023
        && q[4] === 'LC098ALP014EV.pdf' && q[5] === n)!;
      const topics = (row[6] as number[]).map(i => runtime.topicIds[i]);
      expect(topics.some(t => (crosswalk as Record<string, string[]>)[t]?.includes(card.topicId)), id).toBe(true);
    }
  });

  it('keeps fish preservation as one open choice with every published process', () => {
    const card = get('he-2023-hl-sb-q2b');
    expect(card.totalMarks).toBe(18);
    expect(card.questionText).toContain('one process');
    expect(card.questionText).toContain('underlying principle');
    expect(card.answerVariants?.map(v => v.label)).toEqual([
      'Freezing', 'Salting/Brining', 'Smoking', 'Canning', 'Vacuum packing', 'Another valid process',
    ]);
    for (const variant of card.answerVariants ?? []) {
      expect(tariffReconciles({ ...card, rows: variant.rows })).toBe(true);
      expect(variant.rows.map(row => row.marks)).toEqual([3, 9, 6]);
      expect(variant.rows[1].parts).toHaveLength(3);
      expect(variant.rows[2].parts).toHaveLength(2);
      for (const row of variant.rows.slice(1)) {
        for (const part of row.parts ?? []) expect(part.permittedMarks).toEqual([0, 2, 3]);
      }
    }
    expect(card.answerVariants?.find(v => v.id === 'canning')?.rows[2].contextNote).toContain('canned in brine');
    expect(card.answerVariants?.find(v => v.id === 'vacuum-packing')?.rows[2].contextNote).toContain('increased salt and/or fat');
  });

  it('retains all six production points and the complete packaging guidance', () => {
    const card = get('he-2023-hl-sb-q3b');
    expect(card.questionText).toMatch(/^Profile an added value food/);
    expect(card.totalMarks).toBe(26);
    expect(card.answerVariants?.map(v => v.id)).toEqual(['cheese', 'margarine', 'another-food']);
    for (const variant of card.answerVariants ?? []) {
      expect(tariffReconciles({ ...card, rows: variant.rows })).toBe(true);
      expect(variant.rows.map(row => row.marks)).toEqual([2, 18, 6]);
      expect(variant.rows[1].parts).toHaveLength(6);
      expect(variant.rows[2].contextNote).toContain('wrapped in foil');
      expect(variant.rows[2].contextNote).toContain('allergen information');
    }
    expect(card.answerVariants?.[0].rows[1].contextNote).toContain('stored in controlled conditions for 3-12 months');
    expect(card.answerVariants?.[1].rows[1].contextNote).toContain('votator');
  });

  it('keeps the career detail criterion and its printed partial credit', () => {
    const card = get('he-2023-hl-sc-q2cii');
    expect(card.totalMarks).toBe(6);
    expect(tariffReconciles(card)).toBe(true);
    expect(card.rows[0].group?.options).toHaveLength(11);
    expect(card.rows[0].group?.claimMax).toBe(1);
    expect(card.rows[1].permittedMarks).toEqual([0, 2, 4]);
    expect(card.rows[1].contextNote).toContain('does not print an example detail answer');
  });

  it('opens Section C Q2 on page 6 and its own scheme pages, never Section B Q2', () => {
    const question = anchors.q.find(q => q.n === '7')!;
    expect(question.label).toBe('Section C · Q2');
    expect(question.pP).toBe(6);
    expect(question.region.map(r => r.p)).toEqual([21, 22]);
    expect(paperRegionFor((anchors as PaperAnswerMap).q, '7')?.map(r => r.p)).toEqual([6]);
    expect(preferredAnswersUrl('home-economics-s-and-s', 2023, 'LC098ALP039EV.pdf', 'stale-storage-url'))
      .toBe('/paper-answers/2023/LC098ALP039EV.pdf.json');
    expect(anchors.q.find(q => q.n === '2')?.pP).toBe(3);
    expect(schemeRegionFor((anchors as PaperAnswerMap).q.find(q => q.n === '5')!).map(r => r.p)).toEqual([17]);
    expect(anchors.q.map(q => q.n)).toEqual(['1', '2', '3', '4', '5', '6', '7', '8', '9']);
  });

  it('places every 2023 Higher B/C Mark Bank card in its own Atlas question and canonical topic', () => {
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s'
      && p.year === 2023 && p.level === 'higher' && p.lang === 'ev' && p.fileid === 'LC098ALP039EV.pdf')!;
    const cards = CARDS.filter(c => /^2023 HL Section [BC] /.test(c.questionRef) && !c.questionRef.includes('Deferred'));
    expect(cards).toHaveLength(43);
    for (const card of cards) {
      const match = card.questionRef.match(/Section ([BC]) (?:E\d )?Q(\d+)/)!;
      const n = String(Number(match[2]) + (match[1] === 'C' ? 5 : 0));
      const question = paper.q.find(q => q.n === n)!;
      const topics = browseTopicIdsForQuestion(paper, question);
      expect(topics.some(t => (crosswalk as Record<string, string[]>)[t]?.includes(card.topicId)), card.id).toBe(true);
    }
    const b2 = runtime.questionMappings.find(q => q[0] === 'h' && q[1] === 'e' && q[2] === 2023
      && q[4] === 'LC098ALP039EV.pdf' && q[5] === '2')!;
    expect((b2[6] as number[]).map(i => runtime.topicIds[i])).not.toContain('home-economics-s-and-s-higher-elective-2-patterns-fashion');
  });
});
