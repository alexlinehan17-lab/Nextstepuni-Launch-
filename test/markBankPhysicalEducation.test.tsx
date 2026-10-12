/** @license SPDX-License-Identifier: Apache-2.0 */
import { describe, expect, it, vi } from 'vitest';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { fireEvent, render, screen, within, waitFor } from '@testing-library/react';
import { CARDS as HIGHER } from '../components/MarkBank/cards/physical-education/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/physical-education/ordinary';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/physical-education/factory';
import legacy from '../scripts/markbank/authored/physical-education.json';
import audit from '../scripts/markbank/authored/physical-education-reviewed-audit.json';
import { tariffReconciles } from '../types/markBank';
import { physicalEducationMarks } from '../components/MarkBank/physicalEducationScoring';
import SessionScreen, { suggestRubricGrade } from '../components/MarkBank/SessionScreen';
import { vaultPdf } from '../components/PaperTrail/vaultDocs';
import { PHYSICAL_EDUCATION_TASKS, fullPaperQuestionFor } from '../components/PaperTrail/physicalEducationTasks';
import { questionsForTopics, siblingsFor, topicsForSubject, subjectAtlasStats } from '../components/PaperTrail/topics';
import { findCanonicalTopic, resolveCurriculumSpecification } from '../curriculumRegistry';
import { examTopicDefinition } from '../data/examTopics/registry';
import VaultQuestionCard from '../components/PaperTrail/VaultQuestionCard';

vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

const reviewed2020 = REVIEWED_CARDS.filter(card => card.year === 2020);
// A printed choice is ONE card (AGENTS.md, 2026-10-12): the printed question with
// its whole pool and the scheme's own grid, never a card per option or pair.
const expectOneChoiceCard = (id: string, marks: number) => {
  const family = REVIEWED_CARDS.filter(card => card.id === id || card.id.startsWith(`${id}-`));
  expect(family.map(card => card.id), id).toEqual([id]);
  expect(family[0].totalMarks, id).toBe(marks);
  expect(family[0].questionText, id).not.toMatch(/Practice route|practice pair/i);
  return family[0];
};
const get = (part: string) => reviewed2020.find(card => card.id === `pe-2020-hl-q${part}`)!;

describe('Physical Education independent paper review', () => {
  it('retains every previous card ID exactly once after the complete review', () => {
    const live = [...HIGHER, ...ORDINARY];
    expect(new Set(live.map(card => card.id)).size).toBe(live.length);
    expect(legacy.filter(card => !live.some(entry => entry.id === card.id))).toEqual([]);
    expect(audit.status).toBe('complete');
    expect(audit.reviewedPapers).toHaveLength(13);
    expect(live).toHaveLength(772);
    expect(audit.retainedLegacyCardCount).toBe(221);
    for (const [level, hash] of [
      ['higher', '2b937885f9ae0c9d7c2952d43c0c2cb44275bd31414d813dee6c98d20bb8525e'],
      ['ordinary', '9f4fab469becb01ab3ce73e4b6301a270e68ea5310bd0225322b0cb65a1ca23f'],
    ]) {
      const retained = legacy.filter(card => card.level === level).map(card => card.id).sort();
      expect(createHash('sha256').update(retained.join('\n')).digest('hex')).toBe(hash);
    }
    expect(audit.corpusPaperCount).toBe(13);
  });

  it('covers the independently reviewed 2020 tasks and keeps each six-group choice as one card', () => {
    expect(reviewed2020).toHaveLength(49);
    expect(audit.reviewedPapers[0].taskCount).toBe(49);
    // Published per-question maxima, independently checked on the scheme pages.
    const maxima = [2,6,6,8,8,8,8,10,12,12,50,40,40,40,40,40];
    for (let question = 1; question <= 16; question++) {
      const baseTasks = reviewed2020.filter(card =>
        new RegExp(`^pe-2020-hl-q${question}(?:[a-z]+)?$`).test(card.id));
      expect(baseTasks.reduce((sum, card) => sum + card.totalMarks, 0), `Q${question}`).toBe(maxima[question-1]);
    }
    for (const part of ['15ci','15cii']) {
      const card = expectOneChoiceCard(`pe-2020-hl-q${part}`, part === '15ci' ? 6 : 12);
      // The printed 15(c) lead-in carries the group list and the different-group note.
      expect(card.stem).toContain('with reference to a different group for each part');
      expect(card.stem).toContain('• Different socio-economic groups');
      expect(card.rubric.taskRequirements).toEqual([]);
    }
  });

  it('corrects the verified incomplete tariffs and cross-part contamination', () => {
    expect(get('4').totalMarks).toBe(8);
    expect(get('11bi').totalMarks).toBe(6);
    expect(get('12aii').totalMarks).toBe(4);
    expect(get('13cii').totalMarks).toBe(8);
    expect(get('14a').totalMarks).toBe(8);
    expect(get('11ai').questionText).not.toContain('impact on the skill level');
    expect(get('11aiii').stem).toContain('Figure 5');
    expect(get('16biii').sourceMaterial?.pages).toEqual([30,31]);
  });

  it('covers the 2021 Higher tasks, both alternative pools and published fixed scores', () => {
    const cards = REVIEWED_CARDS.filter(card => card.year === 2021 && card.level === 'higher');
    expect(cards).toHaveLength(56);
    expect(audit.reviewedPapers.find(paper => paper.year === 2021)?.taskCount).toBe(56);
    const byPart = (part: string) => cards.find(card => card.id === `pe-2021-hl-q${part}`)!;
    for (let n=1; n<=18; n++) {
      const tasks=cards.filter(card => new RegExp(`^pe-2021-hl-q${n}(?:[a-z]+)?$`).test(card.id));
      expect(tasks.reduce((total, card) => total+card.totalMarks,0), `2021 Q${n}`).toBe(n<13?8:n===13?50:40);
    }
    for (const part of ['10','13dii']) expectOneChoiceCard(`pe-2021-hl-q${part}`, part==='10'?8:4);
    expect(byPart('13e').totalMarks).toBe(9);
    expect(byPart('13e').sourceMaterial?.pages).toEqual([12,13,17]);
    expect(byPart('13b').totalMarks).toBe(8);
    expect(byPart('15d').totalMarks).toBe(12);
    expect(byPart('17ci').totalMarks).toBe(6);
    expect(byPart('17d').totalMarks).toBe(10);
    expect(byPart('14di').rubric.criteria[0].permittedMarks).toEqual([0,2,5,8]);
    expect(byPart('14c').rubric.criteria[0].permittedMarks).not.toContain(4);
    expect(byPart('16b').rubric.criteria).toHaveLength(4);
    expect(cards.every(tariffReconciles)).toBe(true);
  });

  it('covers 2021 Ordinary tasks, separate MCQs and the body-type choice as one card', () => {
    const cards=REVIEWED_CARDS.filter(card => card.year===2021 && card.level==='ordinary');
    const paper=audit.reviewedPapers.find(paper => paper.year===2021 && paper.level==='ordinary')!;
    expect(cards).toHaveLength(59);
    expect(paper.taskCount).toBe(59);
    for (let n=1; n<=18; n++) {
      const tasks=cards.filter(card => new RegExp(`^pe-2021-ol-q${n}(?:[a-z]+)?$`).test(card.id));
      expect(tasks.reduce((total,card)=>total+card.totalMarks,0),`2021 OL Q${n}`).toBe(n<13?8:n===13?50:40);
    }
    const get=(part:string)=>cards.find(card=>card.id===`pe-2021-ol-q${part}`)!;
    expect(get('3').questionRef).toBe('2021 OL Q3(a)');
    for (const part of ['3','3b','3c','3d']) {
      expect(get(part).totalMarks).toBe(2);
      expect(get(part).questionText).toContain('Choose one answer');
      expect(get(part).rubric.criteria[0].permittedMarks).toEqual([0,2]);
    }
    const bodyType=expectOneChoiceCard('pe-2021-ol-q17cii',6);
    expect(bodyType.sourceMaterial?.pages[0]).toBe(27);
    expect(bodyType.stem).toBe('Question 17(c)(i): Label the body types shown in Figure 8.');
    expect(get('7').totalMarks).toBe(8);
    expect(get('14aii').totalMarks).toBe(12);
    expect(get('13eii').totalMarks).toBe(6);
    expect(get('13eii').sourceMaterial?.pages).toEqual([10,11,15]);
    expect(get('18cii').sourceMaterial?.pages).toEqual([31,32]);
    expect(get('16d').sourceMaterial?.pages).toEqual([24]);
    expect(get('14aiii').rubric.schemeMaterial.pages).toEqual([10]);
    expect(get('17ci').rubric.criteria[0].permittedMarks).toEqual([0,1,2]);
    expect(get('15b').rubric.criteria).toHaveLength(4);
    expect(cards.every(tariffReconciles)).toBe(true);
  });

  it('covers 2022 Higher, including six-group pools, the lever choice and visible scheme amendments', () => {
    const cards=REVIEWED_CARDS.filter(card => card.year===2022 && card.level==='higher');
    const get=(part:string)=>cards.find(card=>card.id===`pe-2022-hl-q${part}`)!;
    expect(cards).toHaveLength(61);
    expect(audit.reviewedPapers.find(paper=>paper.year===2022 && paper.level==='higher')?.taskCount).toBe(61);
    for(let n=1;n<=18;n++) {
      const tasks=cards.filter(card=>new RegExp(`^pe-2022-hl-q${n}(?:[a-z]+)?$`).test(card.id));
      expect(tasks.reduce((total,card)=>total+card.totalMarks,0),`2022 HL Q${n}`).toBe(n<13?8:n===13?50:40);
    }
    for(const part of ['5','15b','18b','18aii']) expectOneChoiceCard(`pe-2022-hl-q${part}`, part==='18aii'?4:8);
    expect(get('13ai').rubric.criteria[0].permittedMarks).toEqual([0,3]);
    expect(get('13b').totalMarks).toBe(9);
    expect(get('16c').totalMarks).toBe(12);
    expect(get('16aii').totalMarks).toBe(5);
    expect(get('14ci').rubric.criteria[0].guidance[0]).toContain('struck out');
    expect(get('13cii').sourceMaterial?.pages).toEqual([15,16,19]);
    expect(get('15b').sourceMaterial?.pages).toEqual([27]);
    expect(get('14d').rubric.schemeMaterial.pages).toEqual([13,14]);
    expect(get('17c').rubric.criteria).toHaveLength(4);
  });

  it('covers 2022 Ordinary with the any-two ethics task, feedback choice and distinct group choices', () => {
    const cards=REVIEWED_CARDS.filter(card=>card.year===2022 && card.level==='ordinary');
    const get=(part:string)=>cards.find(card=>card.id===`pe-2022-ol-q${part}`)!;
    expect(cards).toHaveLength(72);
    expect(audit.reviewedPapers.find(paper=>paper.year===2022 && paper.level==='ordinary')?.taskCount).toBe(72);
    for(let n=1;n<=18;n++) {
      const tasks=cards.filter(card=>new RegExp(`^pe-2022-ol-q${n}(?:[a-z]+)?$`).test(card.id));
      expect(tasks.reduce((total,card)=>total+card.totalMarks,0),`2022 OL Q${n}`).toBe(n<13?8:n===13?50:40);
    }
    const ethics=expectOneChoiceCard('pe-2022-ol-q16c',8);
    expect(ethics.questionText).toContain('Integrity, respect, fairness and equity');
    expect(ethics.rubric.taskRequirements).toEqual(['Discuss the importance of any two of these principles of ethical practice in relation to a named physical activity.']);
    expect(ethics.rubric.criteria.map(c=>[c.label,c.maxMarks])).toEqual([['First principle you chose',4],['Second principle you chose',4]]);
    for(const part of ['17b','17c']) {
      const card=expectOneChoiceCard(`pe-2022-ol-q${part}`, part==='17b'?6:8);
      expect(card.questionText).toMatch(/different socio-economic groups/i);
    }
    expect(get('17c').questionText).toContain('You may not use the same group as used in (b).');
    expectOneChoiceCard('pe-2022-ol-q9c',4);
    expect(get('6').questionRef).toBe('2022 OL Q6(a)');
    expect(['6','6b','6c','6d'].map(part=>get(part).totalMarks)).toEqual([2,2,2,2]);
    expect(get('18aii').totalMarks).toBe(2);
    expect(get('18biii').totalMarks).toBe(8);
    expect(get('15cii').rubric.criteria.map(c=>c.maxMarks)).toEqual([2,4]);
    expect(get('17c').rubric.criteria[0].permittedMarks).toEqual([0,2,6,8]);
    expect(get('13biii').rubric.criteria[0].permittedMarks).toEqual([0,2,3,4]);
    expect(get('13biv').sourceMaterial?.pages).toEqual([15,16,17,18,19]);
    expect(get('14a').sourceMaterial?.pages).toEqual([23]);
    expect(get('18d').sourceMaterial?.pages).toEqual([38,39]);
  });

  it('covers all 2023 Higher boundaries with the published allocations and source context', () => {
    const cards=REVIEWED_CARDS.filter(card => card.year===2023 && card.level==='higher');
    const get=(part:string) => cards.find(card => card.id===`pe-2023-hl-q${part}`)!;
    expect(cards).toHaveLength(54);
    for (let n=1;n<=18;n++) {
      const tasks=cards.filter(card => new RegExp(`^pe-2023-hl-q${n}(?:[a-z]+)?$`).test(card.id));
      expect(tasks.reduce((sum,card) => sum+card.totalMarks,0), `Q${n}`).toBe(n<13?8:n===13?50:40);
    }
    expect(get('8').rubric.criteria.map(c => c.maxMarks)).toEqual([3,3,2]);
    expect(get('17aiii').totalMarks).toBe(2);
    expect(get('18b').totalMarks).toBe(8);
    expect(get('13e').sourceMaterial?.pages).toEqual([15,16,20]);
    expect(get('15ciii').sourceMaterial?.pages).toEqual([27,28]);
    expect(get('15dii').sourceMaterial?.pages).toEqual([26,29]);
    expect(get('17aiii').sourceMaterial?.pages).toEqual([34]);
    expect(get('17b').questionText).toContain('not permitted to use hydration or sports drinks');
    expect(get('18dii').stem).toContain('those same characteristics');
    expect(cards.every(card => card.rubric.taskRequirements?.length===0)).toBe(true);
  });

  it('keeps both 2023 Ordinary choose-two tasks as one card and splits the separately marked matching and true/false items', () => {
    const cards=REVIEWED_CARDS.filter(card => card.year===2023 && card.level==='ordinary');
    const get=(part:string) => cards.find(card => card.id===`pe-2023-ol-q${part}`)!;
    expect(cards).toHaveLength(60);
    for (let n=1;n<=18;n++) {
      const tasks=cards.filter(card => new RegExp(`^pe-2023-ol-q${n}(?:[a-z]+)?$`).test(card.id));
      expect(tasks.reduce((sum,card) => sum+card.totalMarks,0), `Q${n}`).toBe(n<13?8:n===13?50:40);
    }
    for (const [part,pool,marks,slot] of [
      ['10',['sports endorsement','sports merchandising','sports related advertising'],8,'term'],
      ['16c',['confidence','anxiety','motivation','concentration'],16,'factor'],
    ] as const) {
      const card=expectOneChoiceCard(`pe-2023-ol-q${part}`,marks);
      for (const item of pool) expect(card.questionText).toContain(item);
      expect(card.rubric.criteria.map(c => c.label)).toEqual([`First ${slot} you chose`,`Second ${slot} you chose`]);
      expect(card.rubric.taskRequirements).toHaveLength(1);
    }
    expect(['9','9b','9c','9d'].map(part => get(part).totalMarks)).toEqual([2,2,2,2]);
    expect(['12','12b','12c','12d'].map(part => get(part).rubric.criteria[0].guidance[0])).toEqual(['True.','False.','False.','True.']);
    expect(get('9').questionRef).toBe('2023 OL Q9 · row 1');
    expect(get('12d').questionRef).toBe('2023 OL Q12 · statement 4');
    expect(get('5').totalMarks).toBe(8);
    expect(get('14ai').totalMarks).toBe(8);
    expect(get('13di').totalMarks).toBe(6);
    expect(get('13dii').totalMarks).toBe(6);
    expect(get('13diii').sourceMaterial?.pages).toEqual([10,11,15,16]);
    expect(get('18aii').sourceMaterial?.pages).toEqual([27,28]);
    expect(get('18ci').sourceMaterial?.pages).toEqual([30]);
    expect(get('13c').rubric.criteria[0].permittedMarks).toEqual([0,1,2,3,4,6]);
    expect(get('16c').rubric.criteria.every(c => JSON.stringify(c.permittedMarks)==='[0,2,4,8]')).toBe(true);
  });

  it('covers 2024 Higher with the complete case, graph, test battery and verified tariffs', () => {
    const cards=REVIEWED_CARDS.filter(card=>card.year===2024 && card.level==='higher');
    const get=(part:string)=>cards.find(card=>card.id===`pe-2024-hl-q${part}`)!;
    expect(cards).toHaveLength(56);
    expect(audit.reviewedPapers.find(paper=>paper.year===2024 && paper.level==='higher')?.taskCount).toBe(56);
    for(let n=1;n<=18;n++) {
      const tasks=cards.filter(card=>new RegExp(`^pe-2024-hl-q${n}(?:[a-z]+)?$`).test(card.id));
      expect(tasks.reduce((total,card)=>total+card.totalMarks,0),`2024 HL Q${n}`).toBe(n<13?8:n===13?50:40);
    }
    for(const part of ['4','7','15b']) expect(get(part).totalMarks).toBe(8);
    expect(get('15aii').totalMarks).toBe(6);
    expect(get('17c').totalMarks).toBe(12);
    expect(get('17c').rubric.criteria).toHaveLength(6);
    expect(get('13ciii').totalMarks).toBe(5);
    expect(get('13ciii').rubric.criteria[0].permittedMarks).toEqual([0,1,3,5]);
    expect(get('13cii').sourceMaterial?.pages).toEqual([14,17]);
    expect(get('13cii').rubric.criteria[0].guidance[0]).toContain('400 ÷ 8.13');
    expect(get('15ai').sourceMaterial?.pages).toEqual([24]);
    expect(get('15c').rubric.criteria).toHaveLength(9);
    expect(get('16ai').sourceMaterial?.pages).toEqual([28]);
    expect(get('14d').rubric.criteria[0].permittedMarks).toEqual([0,3,6,9,12]);
    expect(cards.filter(card=>card.section==='B').every(card=>card.sourceMaterial?.pages.includes(14))).toBe(true);
  });

  it('covers 2024 Ordinary, its any-two officiating task, MCQ and original visual tasks', () => {
    const cards=REVIEWED_CARDS.filter(card=>card.year===2024 && card.level==='ordinary');
    const get=(part:string)=>cards.find(card=>card.id===`pe-2024-ol-q${part}`)!;
    expect(cards).toHaveLength(60);
    expect(audit.reviewedPapers.find(paper=>paper.year===2024 && paper.level==='ordinary')?.taskCount).toBe(60);
    for(let n=1;n<=18;n++) {
      const tasks=cards.filter(card=>new RegExp(`^pe-2024-ol-q${n}(?:[a-z]+)?$`).test(card.id));
      expect(tasks.reduce((total,card)=>total+card.totalMarks,0),`2024 OL Q${n}`).toBe(n<13?8:n===13?50:40);
    }
    const officiating=expectOneChoiceCard('pe-2024-ol-q18bi',8);
    expect(officiating.sourceMaterial?.pages[0]).toBe(32);
    expect(officiating.questionText).toContain('personal fitness; psychological readiness; personal attire');
    expect(officiating.rubric.criteria.map(c=>[c.label,c.maxMarks])).toEqual([['First heading you chose',4],['Second heading you chose',4]]);
    expect(get('6a').questionText).toContain('(iii)');
    expect(get('6a').rubric.criteria[0].permittedMarks).toEqual([0,4]);
    expect(get('1').totalMarks).toBe(8);
    expect(get('13di').totalMarks).toBe(4);
    expect(get('14ciii').totalMarks).toBe(4);
    expect(get('18cii').totalMarks).toBe(6);
    expect(get('14cii').sourceMaterial?.pages).toEqual([20]);
    expect(get('17bi').totalMarks).toBe(6);
    expect(get('17bi').sourceMaterial?.pages).toEqual([28]);
    expect(get('17bii').totalMarks).toBe(2);
    expect(get('13ciii').sourceMaterial?.pages).toEqual([12,13,14,15]);
    expect(get('18biii').sourceMaterial?.pages).toEqual([32,33]);
    expect(cards.filter(card=>card.section==='B').every(card=>card.sourceMaterial?.pages.includes(12)&&card.sourceMaterial?.pages.includes(13))).toBe(true);
  });

  it('covers 2025 Higher with every printed choice as one card, including the two-of-six comparison', () => {
    const cards=REVIEWED_CARDS.filter(card=>card.year===2025 && card.level==='higher');
    const get=(part:string)=>cards.find(card=>card.id===`pe-2025-hl-q${part}`)!;
    expect(cards).toHaveLength(60);
    expect(audit.reviewedPapers.find(paper=>paper.year===2025 && paper.level==='higher')?.taskCount).toBe(60);
    for(let n=1;n<=18;n++) {
      const tasks=cards.filter(card=>new RegExp(`^pe-2025-hl-q${n}(?:[a-z]+)?$`).test(card.id));
      expect(tasks.reduce((total,card)=>total+card.totalMarks,0),`2025 HL Q${n}`).toBe(n<13?8:n===13?50:40);
    }
    for(const [part,marks] of [['7b',6],['11',8],['14aii',4],['14bi',2],['14c',10],['15aii',4],['18d',12]] as const) {
      expectOneChoiceCard(`pe-2025-hl-q${part}`,marks);
    }
    // Printed wording, including the paper's own slips ("than", "one the following").
    expect(get('7b').questionText).toContain('Tick the box to indicate which context you are answering in - school or community.');
    expect(get('11').questionText).toContain('two strategies than can help');
    expect(get('14aii').questionText).toContain('to one the following components');
    // The scheme prices one holistic 12-mark comparison of the two groups.
    expect(get('18d').rubric.criteria.map(c=>[c.label,c.maxMarks])).toEqual([['Comparison',12]]);
    expect(get('18d').rubric.taskRequirements).toEqual(['Compare the barriers to physical activity participation for two of the following groups:']);
    expect(get('12b').totalMarks).toBe(2);
    expect(get('13ciii').totalMarks).toBe(2);
    expect(get('17a').totalMarks).toBe(8);
    expect(get('17c').rubric.criteria.map(c=>c.maxMarks)).toEqual([4,3,3]);
    expect(get('17d').rubric.criteria.map(c=>c.maxMarks)).toEqual([12,2]);
    expect(get('13di').sourceMaterial?.pages).toEqual([14,15,19]);
    expect(get('13dii').sourceMaterial?.pages).toEqual([14,15,19]);
    expect(get('13ai').rubric.criteria.map(c=>c.maxMarks)).toEqual([3,3]);
    expect(get('5').questionText).toContain('not permitted to use anabolic steroids');
    expect(get('18aii').questionText).toContain('cannot use faking injury');
  });

  it('covers 2025 Ordinary, independently scored blanks and inherited group choices', () => {
    const cards=REVIEWED_CARDS.filter(card=>card.year===2025 && card.level==='ordinary');
    const paper=audit.reviewedPapers.find(paper=>paper.year===2025 && paper.level==='ordinary')!;
    const get=(part:string)=>cards.find(card=>card.id===`pe-2025-ol-q${part}`)!;
    expect(cards).toHaveLength(77);
    expect(paper.taskCount).toBe(77);
    const baseTasks=[...new Map(paper.cards.map(card=>[card.part,card])).values()];
    for(let n=1;n<=18;n++) {
      const tasks=baseTasks.filter(card=>Number(card.part.match(/^\d+/)?.[0])===n);
      expect(tasks.reduce((total,card)=>total+card.totalMarks,0),`2025 OL Q${n}`).toBe(n<13?8:n===13?50:40);
    }
    for(const part of ['15ci','15cii']) {
      const card=expectOneChoiceCard(`pe-2025-ol-q${part}`,part==='15ci'?1:8);
      expect(card.sourceMaterial?.pages).toContain(21);
    }
    expect(get('15ci').questionText).toContain('On the timeline below, identify three major developments');
    expect(get('15cii').stem).toContain('Question 15(c)(i): On the timeline below');
    for(let i=1;i<=8;i++) {
      const card=get(i===1?'18ai':`18ai-blank-${i}`);
      expect(card.questionText).toContain(`blank ${i}`);
      expect(card.questionRef).toBe(`2025 OL Q18(a)(i) · blank ${i}`);
      expect(card.totalMarks).toBe(2);
      expect(card.rubric.criteria[0].permittedMarks).toEqual([0,2]);
      expect(card.stem).toContain('[1] __________');
      expect(card.stem).toContain('[8] __________');
      expect(card.stem).toContain('resources (given)');
      expect(card.sourceMaterial?.pages).toEqual([31]);
    }
    for(const part of ['4','10','11','13dii','13eii']) {
      expect(get(part).rubric.criteria).toHaveLength(1);
      expect(get(part).rubric.criteria[0].permittedMarks).toEqual([0,3,6,8]);
    }
    expect(get('1').totalMarks).toBe(2);
    expect(get('5').totalMarks).toBe(2);
    expect(get('12').totalMarks).toBe(8);
    expect(get('16aiii').sourceMaterial?.pages).toEqual([23,24]);
    expect(get('16aii').rubric.criteria[0].permittedMarks).toEqual([0,4]);
    expect(get('14ci').questionText).toContain('cannot use racquet size');
    expect(get('18ci').questionText).toContain('cannot use running');
    expect(get('7a').topicId).toBe('physical-education-1-11');
    expect(get('13ei').topicId).toBe('physical-education-1-13');
    expect(cards.filter(card=>card.section==='B').every(card=>card.sourceMaterial?.pages.includes(10))).toBe(true);
  });

  it('covers both 2026 papers with each printed choice as one card and every fixed table row', () => {
    for(const [level,short,count,tasks] of [['higher','hl',46,46],['ordinary','ol',62,62]] as const) {
      const cards=REVIEWED_CARDS.filter(card=>card.year===2026 && card.level===level);
      const paper=audit.reviewedPapers.find(paper=>paper.year===2026 && paper.level===level)!;
      expect(cards).toHaveLength(count);
      expect(paper.taskCount).toBe(tasks);
      const baseTasks=[...new Map(paper.cards.map(card=>[card.part,card])).values()];
      for(let n=1;n<=18;n++) {
        expect(baseTasks.filter(card=>Number(card.part.match(/^\d+/)?.[0])===n).reduce((sum,card)=>sum+card.totalMarks,0),`2026 ${short} Q${n}`).toBe(n<13?8:n===13?50:40);
      }
      expect(cards.filter(card=>card.section==='B').every(card=>card.sourceMaterial?.pages.includes(short==='hl'?16:10))).toBe(true);
    }
    const get=(short:string,part:string)=>REVIEWED_CARDS.find(card=>card.id===`pe-2026-${short}-q${part}`)!;
    for(const [short,part,marks] of [['hl','6',8],['hl','16c',10],['ol','8',8],['ol','13ci',8]] as const) {
      expectOneChoiceCard(`pe-2026-${short}-q${part}`,marks);
    }
    expect(get('hl','6').questionText).toContain('component from the following:\nbalance\ncoordination\nflexibility');
    expect(get('ol','8').questionText).toContain('one type of practice, from the list below,');
    expect(get('hl','6').rubric.criteria.map(c=>c.maxMarks)).toEqual([1,1,6]);
    expect(get('hl','14a').rubric.criteria[0].permittedMarks).toEqual([0,1,2,4]);
    expect(get('hl','14d').sourceMaterial?.pages).toEqual([23]);
    expect(get('hl','17d').questionText).toContain('each component');
    expect(get('hl','16b').questionText).toContain('may not use creatine');
    expect(get('hl','13d').questionText).toContain('may not refer to swimming');
    expect(get('ol','1a').totalMarks).toBe(1);
    expect(get('ol','7').totalMarks).toBe(2);
    expect(get('ol','13dii').sourceMaterial?.pages).toEqual([10,13]);
    expect(get('ol','14cvi').sourceMaterial?.pages).toEqual([15,16]);
    expect(get('ol','14cvi').stem).toContain('other than coordination or muscular endurance');
    expect(get('ol','17a').rubric.criteria[2].permittedMarks).toEqual([0,1,2,4]);
    expect(get('ol','18aii').topicId).toBe('physical-education-1-21');
    for(const part of ['15ai','15ai-row-2','15ai-row-3']) {
      expect(get('ol',part).totalMarks).toBe(4);
      expect(get('ol',part).questionText).toContain('mass-participation sports; play; outdoor and adventure');
    }
  });

  it('gives every reviewed Mark Bank card an Atlas task with the same canonical topic and specification', () => {
    const atlas=questionsForTopics('physical-education',null);
    const anchors = new Map<string, string[]>();
    expect(PHYSICAL_EDUCATION_TASKS).toHaveLength(REVIEWED_CARDS.length);
    for (const task of PHYSICAL_EDUCATION_TASKS) {
      const card=REVIEWED_CARDS.find(card => card.id===task.cardId)!;
      expect(card,task.cardId).toBeDefined();
      expect(task.canonicalTopicId).toBe(card.topicId);
      const spec=resolveCurriculumSpecification(card.subjectId,card.year)!;
      expect(spec.id).toBe(task.specificationId);
      expect(findCanonicalTopic(spec,card.topicId)).toBeDefined();
      expect(task.paperPages).toEqual(card.sourceMaterial?.pages);
      expect(task.schemePages).toEqual(card.rubric.schemeMaterial.pages);
      expect(task.totalMarks).toBe(card.totalMarks);
      expect(atlas.filter(q => q.year===task.year && q.level===task.level && q.n===task.n)).toHaveLength(1);
      for (const topic of task.examTopicIds) {
        expect(examTopicDefinition(topic)).toBeDefined();
        expect(siblingsFor('physical-education',topic).some(q => q.year===task.year && q.level===task.level && q.n===task.n)).toBe(true);
      }
      expect(questionsForTopics('physical-education',[card.topicId]).some(q => q.year===task.year && q.level===task.level && q.n===task.n)).toBe(true);
      expect(fullPaperQuestionFor(task)).toBe(task.parentQuestion);
      const anchorPath = `scripts/paper-trail/answers/${task.year}/${task.fileid}.json`;
      if (!anchors.has(anchorPath)) {
        const map = JSON.parse(readFileSync(anchorPath, 'utf8')) as { q: Array<{ n: string }> };
        anchors.set(anchorPath, map.q.map(q => q.n));
      }
      // The full-paper jump uses the answer map, independent of legacy topic
      // tags (the 2022 OL English paper has anchors but no legacy tag row).
      expect(anchors.get(anchorPath), task.cardId).toContain(task.parentQuestion);
    }
    expect(atlas.filter(q => q.year===2020 && q.level==='higher')).toHaveLength(49);
    expect(atlas.filter(q => q.year===2021 && q.level==='higher')).toHaveLength(56);
    expect(atlas.filter(q => q.year===2021 && q.level==='ordinary')).toHaveLength(59);
    expect(subjectAtlasStats('physical-education').questions).toBe(atlas.length);
    const biomech='physical-education-higher-1-learning-and-improving-skill-technique-biomechanics';
    expect(siblingsFor('physical-education',biomech).some(q => q.year===2021 && q.n==='14(a)')).toBe(false);
    expect(topicsForSubject('physical-education').find(topic => topic.subtopicId===biomech)?.count).toBe(questionsForTopics('physical-education',[biomech]).length);
  });

  it('renders the shared task in Atlas without exposing its marking scheme before reveal', async () => {
    const task=PHYSICAL_EDUCATION_TASKS.find(task => task.cardId==='pe-2021-hl-q13dii')!;
    const save=vi.fn(), open=vi.fn();
    render(<VaultQuestionCard sibling={task} saved={false} onToggleReview={save} onOpenInPaper={open} />);
    expect(await screen.findByText(/Outline how one of the measures named by you/)).toBeInTheDocument();
    expect(screen.queryByText(/Practice route/)).not.toBeInTheDocument();
    expect(screen.queryByRole('button',{name:/published marking guide/i})).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button',{name:'Add to daily review'}));
    expect(save).toHaveBeenCalledOnce();
    fireEvent.click(screen.getByRole('button',{name:'Full paper'}));
    expect(open).toHaveBeenCalledOnce();
    fireEvent.click(screen.getByRole('button',{name:'Show marking scheme'}));
    expect(screen.getByRole('button',{name:/published marking guide/i})).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button',{name:'Set Outline to 4 marks'}));
    expect(screen.getByRole('button',{name:'Set Outline to 4 marks'})).toHaveAttribute('aria-pressed','true');
  });

  it('never publishes a printed choice as route siblings', () => {
    // A printed question is never published twice in one sitting, and no card
    // names a practice route in place of the printed wording.
    const refs = REVIEWED_CARDS.map(card => `${card.year}|${card.level}|${card.questionRef}`);
    expect(refs.filter((ref, index) => refs.indexOf(ref) !== index)).toEqual([]);
    expect(REVIEWED_CARDS.filter(card => /Practice route|practice pair/i.test(`${card.questionText} ${card.stem}`))).toEqual([]);
    // One card per declared choice family; choose-N cards carry the printed
    // instruction and either N per-item slots or the scheme's own holistic grid.
    const choices = audit.reviewedPapers.flatMap(paper => paper.cards.filter(card => card.choice));
    expect(choices).toHaveLength(29);
    expect(choices.filter(card => card.choice!.choose > 1)).toHaveLength(6);
    for (const entry of choices) {
      const card = REVIEWED_CARDS.find(card => card.id === entry.cardId)!;
      expectOneChoiceCard(entry.cardId, entry.totalMarks);
      if (entry.choice!.choose > 1) expect(card.rubric.taskRequirements, entry.cardId).toEqual([entry.choice!.instruction]);
    }
  });

  it('provides the complete question material, rotated chart and original answer diagrams', () => {
    expect(reviewed2020.every(tariffReconciles)).toBe(true);
    expect(get('11bi').sourceMaterial?.pages).toEqual([12,13,15]);
    expect(get('11bi').sourceMaterial?.pageRotations?.[13]).toBe(90);
    const diagram = get('5b');
    expect(diagram.rubric.system).toBe('physical-education');
    if (diagram.rubric.system !== 'physical-education') throw Error('wrong rubric');
    expect(diagram.rubric.schemeMaterial.pages).toEqual([5]);
    expect(diagram.rubric.criteria[0].permittedMarks).toEqual([0,2,4,6]);
    expect(physicalEducationMarks(diagram, {'pe:c1':3})).toBe(0);
    expect(physicalEducationMarks(diagram, {'pe:c1':6})).toBe(6);
    expect(suggestRubricGrade(diagram, {'pe:c1':6})).toBe('got');
  });

  it('opens and closes the paper before reveal and the scheme only after reveal', async () => {
    render(<SessionScreen cards={[get('5b')]} subjectLabel="Physical Education" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    expect(screen.queryByRole('button', {name:/published marking guide/i})).not.toBeInTheDocument();
    const paperTrigger = screen.getByRole('button', {name:/original paper/i});
    fireEvent.click(paperTrigger);
    const paperDialog=screen.getByRole('dialog');
    const paperLink=within(paperDialog).getByRole('link', {name:'Open the original paper'});
    expect(decodeURIComponent(paperLink.getAttribute('href')!)).toContain('/paper/LC225ALP000EV.pdf');
    fireEvent.keyDown(paperDialog,{key:'Escape'});
    await waitFor(()=>expect(paperTrigger).toHaveFocus());
    fireEvent.click(screen.getByRole('button',{name:/Reveal the marking scheme/i}));
    expect(screen.getByText(/No Physical Education criteria placement selected yet/)).toBeInTheDocument();
    expect(screen.queryByText(/No Geography allocation/)).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button',{name:/published marking guide/i}));
    const schemeDialog=screen.getByRole('dialog');
    const schemeLink=within(schemeDialog).getByRole('link',{name:'Open the original marking scheme'});
    expect(decodeURIComponent(schemeLink.getAttribute('href')!)).toContain('/scheme/LC225ALP000EV.pdf');
    expect(vaultPdf).toHaveBeenCalled();
    fireEvent.click(within(schemeDialog).getByRole('button',{name:'Close marking scheme'}));
    fireEvent.click(screen.getByRole('button',{name:'Set Labels to 6 marks'}));
    expect(screen.getByRole('button',{name:'Set Labels to 6 marks'})).toHaveAttribute('aria-pressed','true');
  });
});
