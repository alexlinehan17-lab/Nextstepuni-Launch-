import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/lcvp/common';
import { tariffReconciles } from '../types/markBank';
import review from '../scripts/markbank/authoring/lcvp/2019-cl-main-review.json';
import authored from '../scripts/markbank/authored/lcvp.json';
import anchors from '../scripts/paper-trail/answers/2019/LC462CLP000EV.pdf.json';
import local from '../data/examTopics/link-modules-local-crosswalk.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';

const all = CARDS.filter(c => c.id.startsWith('lcvp-2019-cl-'));
const get = (suffix: string) => {
  const card = all.find(c => c.id === `lcvp-2019-cl-${suffix}`);
  if (!card || card.kind !== 'question') throw new Error(suffix);
  return card;
};

describe('LCVP 2019: complete original tasks and unresolved ICT allocation', () => {
  it('reconciles the independent 45-leaf census and restores six omissions and the named-enterprise mark', () => {
    expect(review.manualOriginalLeaves).toBe(45);
    expect(review.manualSectionLeaves).toEqual({ A: 9, B: 6, C: 30 });
    expect(review.rawCensusClassification.rawLeaves).toBe(45);
    expect(review.candidateWrittenMarks).toBe(160);
    expect(all).toHaveLength(45);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(210);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    const expected = authored.filter(c => c.year === 2019);
    expect(all.map(c => c.id).sort()).toEqual(expected.map(c => c.id).sort());
    for (const source of expected) {
      const emitted = get(source.id.replace('lcvp-2019-cl-', ''));
      expect(emitted.questionText, source.id).toBe(source.questionText);
      expect(emitted.stem ?? '', source.id).toBe(source.stem ?? '');
      expect(emitted.rows, source.id).toEqual(source.rows);
      expect(emitted.tariffModel, source.id).toEqual(source.tariffModel);
      expect(emitted.totalMarks, source.id).toBe(source.totalMarks);
      expect(emitted.conceptId, source.id).toBe(source.conceptId);
      expect(emitted.topicId, source.id).toBe(source.topicId);
      expect(emitted.sourceMaterial, source.id).toEqual(source.sourceMaterial);
      expect(emitted.additionalSourceMaterials, source.id).toEqual(source.additionalSourceMaterials);
      expect(emitted.videoMaterial, source.id).toEqual(source.videoMaterial);
    }
    expect(['b3ii', 'c3ai', 'c3aii', 'c4a', 'c5ai', 'c5d'].map(s => get(s).totalMarks)).toEqual([9, 1, 3, 3, 2, 6]);
    expect(get('b3i').rows.map(r => r.marks)).toEqual([1, 2]);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      expect(c.questionText + c.stem).not.toMatch(/Leaving Certificate Vocational Programme 2019|Link Modules Examination/);
    }
  });

  it('binds all nine apprenticeship tasks to the original MP4 and retains full model choices', () => {
    const video = get('a1').videoMaterial;
    expect(video?.canonicalUrl).toBe('https://www.examinations.ie/archive/exampapers/2019/LC462CLP031EV.mp4');
    for (const c of all.filter(c => c.id.startsWith('lcvp-2019-cl-a'))) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(c.videoMaterial).toEqual(video);
      expect(c.audioMaterial).toBeUndefined();
      expect(c.additionalSourceMaterials?.[0].pages).toEqual([3]);
    }
    expect(['a2', 'a3', 'a4', 'a8'].map(s => get(s).rows[0].group?.options.length)).toEqual([6, 4, 5, 7]);
    expect(get('a6').rows[0].parts).toHaveLength(4);
    expect(get('a7').rows[0].parts).toHaveLength(6);
    expect(get('a6').rows[0].contextNote).toContain('Assessments to ensure the required standards are reached');
    expect(get('a7').rows[0].contextNote).toContain('Allows them to change career');
    for (const suffix of ['a6', 'a7']) expect(get(suffix).rows[0].contextNote).toContain('Etc.');
    expect(get('a5i').rows[0].verbatim).toBe('2 / 3 / 4 years');
    expect(get('a5ii').rows[0].verbatim).toBe('Level 8 NFQ / a degree');
  });

  it('keeps the whole community case and all four plan headings with the original dependent requirements', () => {
    expect(get('b1').stem).toContain('Ballytiernan Community Co-operative');
    expect(get('b1').stem).toContain('glamping');
    expect(get('b1').sourceMaterial?.pages).toEqual([9]);
    expect(get('b2iii').rows[0].contextNote).toContain('MUST link');
    expect(get('b2iii').stem).toContain(get('b2ii').questionText);
    expect(get('b3i').rows[0].contextNote).toContain('SCHOOL BASED ACTIVITY/ENTERPRISE');
    for (const suffix of ['b3i', 'b3ii']) expect(get(suffix).stem).toContain('One of the local schools is interested in using the land.');
    expect(get('b3ii').rows[0].parts).toHaveLength(3);
    for (const heading of ['Product / service', 'Financial details', 'Management/People', 'Marketing']) {
      expect(get('b3ii').rows[0].contextNote).toContain(heading);
    }
    expect(get('b3ii').stem).toContain(get('b3i').questionText);
  });

  it('preserves every questionnaire choice, required finance question and layout-only exception', () => {
    const card = get('c2c');
    expect(card.rows.map(r => r.marks)).toEqual([1, 1, 1, 1, 4]);
    expect(card.rows[3].verbatim).toBe('Compulsory question relating to finance');
    expect(card.rows[4].parts).toHaveLength(4);
    const model = card.rows[0].contextNote ?? '';
    for (const text of ['Q.1', 'Male', 'Female', 'Q.2', 'Yes', 'No', 'Q.3', 'Blue', 'Red', 'Grey', 'Q.4', 'Q.5', 'Full zip', 'No zip', 'Q.6*', 'pay for a hoodie']) expect(model).toContain(text);
    expect(model.match(/☐/g)).toHaveLength(11);
    expect(model).toContain('LAYOUT ONLY');
    expect(card.rows[4].contextNote).toContain('no question-content marks');
    expect(get('c2dii').rows[0].contextNote).toContain('Repetition will not score');
  });

  it('retains complete linked activity, role and challenge responses without invented personal models', () => {
    expect(get('c3aii').rows.map(r => r.marks)).toEqual([1, 2]);
    expect(get('c3aii').stem).toContain(get('c3ai').questionText);
    expect(get('c3b').stem).toContain(get('c3ai').questionText);
    expect(get('c3b').rows[1].group?.options).toHaveLength(8);
    expect(get('c3dii').stem).toContain(get('c3di').questionText);
    expect(get('c4a').rows.map(r => r.marks)).toEqual([1, 2]);
    expect(get('c5d').rows).toHaveLength(3);
    for (const row of get('c5d').rows) expect(row.parts?.map(p => p.marks)).toEqual([1, 1]);
    expect(get('c5d').rows[0].contextNote).toContain('Finding a suitable location');
    expect(get('c5d').rows[0].contextNote).toContain('no completed solution examples');
  });

  it('retains source-specific binary steps and complete two-column and cross-page pools', () => {
    expect(get('c1a').rows[1].group?.options).toEqual(['Personal details', 'Skills/qualities', 'Education/qualifications', 'Work experience', 'Hobbies/interests', 'Achievements', 'Referees']);
    expect(get('c1c').rows[0].contextNote).toContain('summary of the Protection of Young Person’s');
    expect(get('c1c').rows[0].contextNote).toContain('Etc.');
    expect(get('c4b').rows[0].group?.claimMax).toBe(4);
    expect(get('c4b').rows[0].group?.perOption).toBe(2);
    expect(get('c4b').rows[0].contextNote).toContain('2 or 0 marks');
    const work = get('c4d').rows[0].contextNote ?? '';
    for (const value of ['YES or NO', 'Problem solving', 'Time management', 'Motivation', 'Organisation skills']) expect(work).toContain(value);
    expect(get('c6a').rows[0].group?.options).toHaveLength(13);
    expect(get('c6a').rows[0].group?.options[11]).toBe('Production of portfolio items/reports/printing');
    expect(get('c6c').rows[0].contextNote).toContain('Provide free WiFi to attract customers');
    expect(get('c6c').rows[0].contextNote).toContain('Powerpoint keynote presentations');
    expect(get('c6d').rows[0].contextNote).toContain('Negative/bad reviews of the business from customers/service/bad ratings');
  });

  it('holds the entire contradictory ICT task without converting unassessed responses to zero marks', () => {
    expect(all.filter(c => c.kind === 'question' && c.tariffModel.kind === 'questionTotal').map(c => c.id)).toEqual(['lcvp-2019-cl-c6b']);
    const card = get('c6b');
    expect(card.totalMarks).toBe(4);
    expect(card.questionText).toBe('Why are ICT skills necessary for an employee in today’s working environment?');
    expect(card.rows).toHaveLength(8);
    expect(card.rows[7].verbatim).toBe('Etc.');
    for (const row of card.rows) {
      expect(row.marks).toBeNull();
      expect(row.parts).toBeUndefined();
      expect(row.group).toBeUndefined();
    }
    expect(card.rows[0].contextNote).toContain('Two relevant answers; 4 x 1 mark');
    expect(card.rows[0].contextNote).toContain('confidence review only');
  });

  it('preserves all 17 original Atlas identities and memberships while linking final canonical topics', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 17 }, (_, i) => String(i + 1)));
    expect(anchors.q.slice(11).map(q => [q.pP, q.endP])).toEqual([[16, 18], [19, 21], [22, 24], [25, 27], [28, 30], [31, 33]]);
    expect(anchors.q.find(q => q.n === '10')?.region.map(r => r.p)).toEqual([6, 7]);
    expect(anchors.q.find(q => q.n === '17')?.region.map(r => r.p)).toEqual([17, 18]);
    expect(local.reviewedEnglish2019.markBankMappings).toHaveLength(45);
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'link-modules' && p.year === 2019 && p.lang === 'ev' && p.fileid === 'LC462CLP000EV.pdf')!;
    for (const [n, original] of Object.entries(local.reviewedEnglish2019.originalAtlasTopicIds)) {
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!)).toEqual(expect.arrayContaining(original));
    }
    for (const mapping of local.reviewedEnglish2019.markBankMappings) {
      const topics = browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === mapping.n)!);
      expect(topics, mapping.id).toEqual(expect.arrayContaining(mapping.atlasTopicIds));
      expect(topics.some(t => curriculumNodeIdsForExamTopic(t).includes(mapping.topicId)), mapping.id).toBe(true);
    }
    expect(['c3ai', 'c3aii', 'c3b', 'c3c', 'c3di', 'c3dii'].map(s => get(s).topicId)).toEqual(Array(6).fill('lcvp-link-modules-1-0'));
    expect(['c6a', 'c6b', 'c6c', 'c6d'].map(s => get(s).topicId)).toEqual(Array(4).fill('lcvp-link-modules-0-0'));
  });
});
