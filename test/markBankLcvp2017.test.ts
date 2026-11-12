import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/lcvp/common';
import { tariffReconciles } from '../types/markBank';
import authored from '../scripts/markbank/authored/lcvp.json';
import review from '../scripts/markbank/authoring/lcvp/2017-cl-main-review.json';
import anchors from '../scripts/paper-trail/answers/2017/LC462CLPO00EV.pdf.json';
import local from '../data/examTopics/link-modules-local-crosswalk.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';

const all = CARDS.filter(c => c.id.startsWith('lcvp-2017-cl-'));
const get = (suffix: string) => {
  const card = all.find(c => c.id === `lcvp-2017-cl-${suffix}`);
  if (!card || card.kind !== 'question') throw new Error(suffix);
  return card;
};

describe('LCVP 2017: complete original tasks, component tariffs and unchanged Atlas identities', () => {
  it('covers all 38 independently reviewed tasks and emits the complete authored fields', () => {
    expect(review.manualOriginalLeaves).toBe(38);
    expect(review.manualPricedTasks).toBe(38);
    expect(review.manualSectionTasks).toEqual({ A: 8, B: 6, C: 24 });
    expect(review.candidateWrittenMarks).toBe(160);
    expect(review.rawReaderAudit.capturedTariffSum).toBe(44);
    expect(review.originalMarkBankCards).toBe(0);
    expect(all).toHaveLength(38);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(210);
    const expected = authored.filter(c => c.year === 2017);
    expect(all.map(c => c.id).sort()).toEqual(expected.map(c => c.id).sort());
    for (const source of expected) {
      const emitted = get(source.id.replace('lcvp-2017-cl-', ''));
      expect(tariffReconciles(emitted), source.id).toBe(true);
      expect(emitted.questionText, source.id).toBe(source.questionText);
      expect(emitted.stem ?? '', source.id).toBe(source.stem ?? '');
      expect(`${emitted.questionText} ${emitted.stem ?? ''}`, source.id).not.toMatch(/Office|Only|Page \d+ of 32|\b1 2\b/);
      expect(emitted.rows, source.id).toEqual(source.rows);
      expect(emitted.tariffModel, source.id).toEqual(source.tariffModel);
      expect(emitted.totalMarks, source.id).toBe(source.totalMarks);
      expect(emitted.conceptId, source.id).toBe(source.conceptId);
      expect(emitted.topicId, source.id).toBe(source.topicId);
      expect(emitted.sourceMaterial, source.id).toEqual(source.sourceMaterial);
      expect(emitted.additionalSourceMaterials, source.id).toEqual(source.additionalSourceMaterials);
      expect(emitted.videoMaterial, source.id).toEqual(source.videoMaterial);
    }
  });

  it('binds all eight video tasks and keeps the original unequal reasons tariff without rewriting the why-question', () => {
    const video = get('a1').videoMaterial;
    expect(video?.canonicalUrl).toBe('https://www.examinations.ie/archive/exampapers/2017/LC462CLP031EV.mp4');
    for (const card of all.filter(c => c.id.startsWith('lcvp-2017-cl-a'))) {
      if (card.kind !== 'question') throw new Error(card.id);
      expect(card.videoMaterial).toEqual(video);
      expect(card.audioMaterial).toBeUndefined();
      expect(card.additionalSourceMaterials?.[0].pages).toEqual([2]);
    }
    expect(get('a2').rows[0].verbatim).toBe('Mixed Bag Gaming');
    expect(get('a2').rows[0].marks).toBe(2);
    expect(get('a2').rows[0].parts).toBeUndefined();
    expect(get('a3').questionText).toBe('Why does Emily like to take on work experience students?');
    expect(get('a3').rows[0].group).toMatchObject({ claimMax: 2, perOptionSteps: [2, 1] });
    expect(get('a3').rows[0].group?.options).toHaveLength(3);
    expect(get('a5').rows.map(r => r.marks)).toEqual([1, 3]);
    expect(get('a5').rows[0].verbatim).toBe('YES/NO');
    expect(get('a5').rows[1].group?.options).toHaveLength(5);
    expect(get('a5').sourceMaterial?.pages).toEqual([4, 5]);
    expect(get('a6').rows[0].group?.options).toHaveLength(6);
    expect(get('a7').rows[0].group?.options).toHaveLength(7);
    expect(get('a8').rows[0].group?.options).toHaveLength(6);
  });

  it('retains the whole Amy case, every course model and both sides of all ten complete contrasts', () => {
    for (const suffix of ['b1', 'b2a', 'b2b', 'b2c', 'b3a', 'b3b']) {
      const card = get(suffix);
      expect(card.stem).toBe(get('b1').stem);
      expect(card.stem).toContain('Amy graduated from college with a languages degree');
      expect(card.stem).toContain('future business success.');
      expect(card.stem!.length).toBeGreaterThan(3500);
      expect(card.sourceMaterial?.pages).toEqual([8]);
    }
    expect(['b2a', 'b2b', 'b2c', 'b3a', 'b3b'].map(s => get(s).totalMarks)).toEqual([2, 6, 4, 2, 10]);
    expect(get('b2b').rows[0].group).toMatchObject({ claimMax: 3, perOption: 2 });
    expect(get('b2b').rows[0].group?.options).toHaveLength(9);
    expect(get('b3a').rows[0].group).toMatchObject({ claimMax: 2, perOption: 1 });
    const contrasts = get('b3a').rows[0].group!.options;
    expect(contrasts).toHaveLength(10);
    for (const value of contrasts) {
      expect(value.split(' — ')).toHaveLength(2);
      expect(value.split(' — ').every(cell => cell.trim())).toBe(true);
    }
    expect(contrasts[7]).toContain('to finance the running of the business');
    expect(contrasts[8]).toContain('Health and Safety statement');
    expect(contrasts[9]).toContain('holidays — Set holidays/hours of work');
    expect(get('b3a').rows[0].contextNote).toContain('Both entrepreneur and employee sides');
    expect(get('b3a').rows[0].contextNote).toContain('ENTREPRENEUR — EMPLOYEE');
  });

  it('keeps binary two-mark components and the separately controlled 3,3,2 presentation responses', () => {
    expect(get('c1a').rows.map(r => r.marks)).toEqual([2, 2]);
    expect(get('c1b').rows.map(r => r.marks)).toEqual([2, 2]);
    expect(get('c1b').sourceMaterial?.pages).toEqual([14, 15]);
    for (const number of [1, 4]) {
      for (const letter of ['b', 'c', 'd']) expect(get(`c${number}${letter}`).stem).toContain(get(`c${number}a`).questionText);
    }
    for (const suffix of ['c1d', 'c2c', 'c5d']) {
      const rows = get(suffix).rows;
      expect(rows.map(r => r.marks)).toEqual([3, 3, 3]);
      for (const row of rows) expect(row.parts?.map(p => p.permittedMarks)).toEqual([[0, 1], [0, 2]]);
    }
    expect(get('c2d').rows.map(r => r.marks)).toEqual([3, 3, 2]);
    expect(get('c2d').rows.map(r => r.parts?.map(p => p.marks))).toEqual([[1, 2], [1, 2], [1, 1]]);
    expect(get('c2d').rows[0].contextNote).toContain('2@3m(1+2) and 1@2(1+1)');
    expect(get('c3a').rows.map(r => r.marks)).toEqual([1, 2]);
    expect(get('c3a').rows[1].permittedMarks).toBeUndefined();
    expect(get('c3b').rows[0].group).toMatchObject({ claimMax: 3, perOption: 2 });
    expect(get('c3b').rows[0].group?.options).toHaveLength(8);
    expect(get('c5a').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 2], [0, 2]]);
  });

  it('keeps all ten letter criteria and the complete cross-page alternative pools', () => {
    const letter = get('c4c').rows[0];
    expect(letter.marks).toBe(10);
    expect(letter.parts).toHaveLength(10);
    expect(letter.parts?.map(p => p.verbatim).sort()).toEqual([
      'Own address & Business address', 'Date', 'Opening & closing salutation', 'Introduction',
      'Request for permission to visit', 'Date of visit', 'Closing', 'Layout/neatness', 'Spelling',
      'Grammar/paragraphs/punctuation',
    ].sort());
    for (const part of letter.parts!) expect(part).toMatchObject({ marks: 1, permittedMarks: [0, 1] });
    expect(letter.contextNote).toContain('together receive ONE mark');
    expect(get('c3d').rows[0].contextNote).toContain('Word of mouth');
    expect(get('c4d').rows[0].contextNote).toContain('Communication/interpersonal skills are improved.');
    expect(get('c5d').rows[0].contextNote).toContain('Team-player');
    expect(get('c5c').rows[0].group?.options).toHaveLength(9);
  });

  it('keeps three open planning headings and method-plus-two-statements evaluation controls', () => {
    expect(get('c6b').rows.map(r => r.marks)).toEqual([2, 2, 2]);
    for (const row of get('c6b').rows) {
      expect(row.parts?.map(p => p.permittedMarks)).toEqual([[0, 1], [0, 1]]);
      expect(row.group).toBeUndefined();
      for (const heading of ['Aims/Objectives', 'Research Methods', 'Analysis of Research', 'Action Steps', 'Schedule of Time', 'Schedule of Costs', 'Evaluation Methods']) expect(row.contextNote).toContain(heading);
      expect(row.contextNote).toContain('no marks for headings');
    }
    expect(get('c6d').rows.map(r => r.marks)).toEqual([3, 3, 3]);
    for (const row of get('c6d').rows) {
      expect(row.parts?.map(p => p.marks)).toEqual([1, 1, 1]);
      expect(row.parts?.map(p => p.verbatim)).toEqual(['Method', 'Statement 1', 'Statement 2']);
      expect(row.contextNote).toContain('Method +2 statements');
    }
  });

  it('retains every original Atlas identity and spelling while covering complete page ranges', () => {
    expect(anchors.paperFileid).toBe('LC462CLPO00EV.pdf');
    expect(anchors.schemeFileid).toBe('LC462CLP000EV.pdf');
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 17 }, (_, i) => String(i + 1)));
    expect(anchors.q.slice(11).map(q => [q.pP, q.endP])).toEqual([[14, 16], [17, 19], [20, 22], [23, 25], [26, 28], [29, 31]]);
    expect(anchors.q.find(q => q.n === '5')?.endP).toBe(5);
    expect(anchors.q.find(q => q.n === '10')?.endP).toBe(11);
    expect(anchors.q.find(q => q.n === '11')?.endP).toBe(12);
    expect(anchors.q.find(q => q.n === '14')?.region.map(r => r.p)).toEqual([11, 12]);
    expect(local.reviewedEnglish2017.markBankMappings).toHaveLength(38);
    expect(Object.keys(local.reviewedEnglish2017.originalAtlasTopicIds)).toHaveLength(17);
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'link-modules' && p.year === 2017 && p.lang === 'ev' && p.fileid === 'LC462CLPO00EV.pdf')!;
    for (const [n, topics] of Object.entries(local.reviewedEnglish2017.originalAtlasTopicIds)) expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!)).toEqual(expect.arrayContaining(topics));
    for (const mapping of local.reviewedEnglish2017.markBankMappings) {
      const topics = browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === mapping.n)!);
      expect(topics, mapping.id).toEqual(expect.arrayContaining(mapping.atlasTopicIds));
      expect(topics.some(t => curriculumNodeIdsForExamTopic(t).includes(mapping.topicId)), mapping.id).toBe(true);
    }
  });
});
