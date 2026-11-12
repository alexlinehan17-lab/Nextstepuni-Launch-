import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/lcvp/common';
import { tariffReconciles } from '../types/markBank';
import authored from '../scripts/markbank/authored/lcvp.json';
import review from '../scripts/markbank/authoring/lcvp/2016-cl-main-review.json';
import anchors from '../scripts/paper-trail/answers/2016/LC462CLPO00EV.pdf.json';
import local from '../data/examTopics/link-modules-local-crosswalk.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';

const all = CARDS.filter(c => c.id.startsWith('lcvp-2016-cl-'));
const get = (suffix: string) => {
  const card = all.find(c => c.id === `lcvp-2016-cl-${suffix}`);
  if (!card || card.kind !== 'question') throw new Error(suffix);
  return card;
};

describe('LCVP 2016: complete source tasks and original Atlas identities', () => {
  it('reconciles 40 leaves into 39 whole tasks and emits every authored field unchanged', () => {
    expect(review.manualOriginalLeaves).toBe(40);
    expect(review.manualPricedTasks).toBe(39);
    expect(review.manualSectionTasks).toEqual({ A: 8, B: 5, C: 26 });
    expect(review.rawReaderAudit.capturedTariffSum).toBe(44);
    expect(review.candidateWrittenMarks).toBe(160);
    expect(review.originalMarkBankCards).toBe(0);
    expect(all).toHaveLength(39);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(210);
    const expected = authored.filter(c => c.year === 2016);
    expect(all.map(c => c.id).sort()).toEqual(expected.map(c => c.id).sort());
    for (const source of expected) {
      const emitted = get(source.id.replace('lcvp-2016-cl-', ''));
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

  it('retains the original video, full binary contrast pool and six feedback responses', () => {
    const video = get('a1').videoMaterial;
    expect(video?.canonicalUrl).toBe('https://www.examinations.ie/archive/exampapers/2016/LC462CLP031EV.mp4');
    for (const card of all.filter(c => c.section === 'A')) {
      if (card.kind !== 'question') throw new Error(card.id);
      expect(card.videoMaterial).toEqual(video);
      expect(card.audioMaterial).toBeUndefined();
      expect(card.additionalSourceMaterials?.[0].pages).toEqual([2]);
    }
    expect(get('a1').rows[0].verbatim).toBe('TechMed Pro is a company which manufactures medical devices.');
    expect(get('a1').rows[0].marks).toBe(2);
    expect(get('a5').rows[0].group).toMatchObject({ claimMax: 2, perOption: 2 });
    expect(get('a5').rows[0].contextNote).toContain('0/2');
    expect(get('a5').sourceMaterial?.pages).toEqual([4, 5]);
    expect(get('a7').rows[0].group).toMatchObject({ claimMax: 3, perOption: 2 });
    expect(get('a7').rows[0].group?.options).toEqual([
      'Controls — Inspires/motivates', 'Focuses on task in hand — Sees the bigger picture',
      'Strict with people/apathy/disengaged — Empathetic', 'Tells them what to do — Facilities creativity',
    ]);
    expect(get('a8').rows[0].group).toMatchObject({ claimMax: 6, perOption: 1 });
    expect(get('a8').rows[0].group?.options).toHaveLength(6);
    expect(get('a8').rows[0].contextNote).toContain('both positive and negative');
  });

  it('keeps the whole case, all stakeholder models and both unresolved whole tasks', () => {
    for (const suffix of ['b1', 'b2a', 'b2b', 'b3a', 'b3b']) {
      const card = get(suffix);
      expect(card.stem).toContain(get('b1').stem);
      expect(card.stem!.length).toBeGreaterThan(3500);
      for (const phrase of ['mobile catering', 'Ratlow Forest Park', 'Rathlow Park', 'Tree Top']) expect(card.stem).toContain(phrase);
      expect(card.sourceMaterial?.pages).toEqual([8]);
    }
    expect(get('b1').rows[0].group?.options).toHaveLength(12);
    expect(get('b2a').questionText).toContain('(i) Outline what benefits');
    expect(get('b2a').questionText).toContain('(ii) Give two benefits');
    expect(get('b2a').stem).toContain(get('b1').questionText);
    expect(get('b2a').rows.filter(r => r.id.startsWith('contribution-'))).toHaveLength(8);
    expect(get('b2a').rows.filter(r => r.id.startsWith('benefit-'))).toHaveLength(9);
    expect(get('b2a').rows[0].contextNote).toContain('(If not linked; mark both and disallow the lower mark)');
    expect(get('c3d').rows.map(r => r.verbatim)).toEqual([
      'Career Aspirations', 'Future Studies', 'What has been learned can be applied to work in the: Home', 'School', 'Community',
    ]);
    expect(get('c3d').rows[0].contextNote).toContain('4 @ 2m (0/2)');
    expect(get('c3d').rows[0].contextNote).toContain('1 @ 1m');
    for (const suffix of ['b2a', 'c3d']) {
      const card = get(suffix);
      expect(card.tariffModel.kind).toBe('questionTotal');
      for (const row of card.rows) {
        expect(row.marks).toBeNull();
        expect(row.parts).toBeUndefined();
        expect(row.group).toBeUndefined();
        expect(row.permittedMarks).toBeUndefined();
      }
    }
    expect(get('b3b').rows.map(r => r.marks)).toEqual([1, 5]);
    expect(get('b3b').rows[1].group?.options).toHaveLength(11);
    expect(get('b3b').questionText).toContain('short and long term success');
    const priced = all.filter(c => c.tariffModel.kind === 'fixed');
    expect(priced.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(195);
  });

  it('keeps the complete advertisement, exactly four underlined choices and all three interview periods', () => {
    for (const suffix of ['c4a', 'c4b', 'c4c', 'c4d']) {
      const card = get(suffix);
      expect(card.stem).toContain('chocopersonnel@eircom.net');
      expect(card.stem).toContain('06 June, 2016');
      expect(card.sourceMaterial?.pages).toEqual([23]);
    }
    expect(get('c4b').additionalSourceMaterials?.[0].pages).toEqual([23, 24]);
    expect(get('c4b').rows).toHaveLength(2);
    for (const row of get('c4b').rows) {
      expect(row.parts?.map(p => p.permittedMarks)).toEqual([[0, 2], [0, 1]]);
      for (const term of ['Interpersonal skills', 'Covering letter', 'References', 'Personnel Manager']) expect(row.contextNote).toContain(`${term}:`);
      expect(row.contextNote).toContain('CV and equal opportunities employer are bold, not underlined');
    }
    expect(get('c4d').rows.map(r => r.verbatim)).toEqual(['Before', 'On the day', 'During the interview']);
    expect(get('c4d').rows.map(r => r.group?.options.length)).toEqual([6, 4, 6]);
    for (const row of get('c4d').rows) expect(row.group).toMatchObject({ claimMax: 2, perOptionSteps: [2, 1] });
  });

  it('retains full optional pools and exact definition, agenda, presentation and business allocations', () => {
    expect(get('c1aii').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 2], [0, 2]]);
    expect(get('c1b').rows[0].contextNote).toContain('Future-focused');
    expect(get('c1b').rows[0].contextNote).toContain('List is not exhaustive');
    expect(get('c2b').rows[0].contextNote).toContain('Advertising the enterprise');
    expect(get('c2d').rows[0].contextNote).toContain('No repetition of points');
    expect(get('c5b').rows.map(r => r.marks)).toEqual([1, 6, 1]);
    expect(get('c5b').rows[1].group?.options).toHaveLength(7);
    expect([get('c5di').totalMarks, get('c5dii').totalMarks]).toEqual([2, 6]);
    expect(get('c6a').rows.map(r => r.marks)).toEqual([1, 3]);
    expect(get('c6a').rows[1].parts?.map(p => p.permittedMarks)).toEqual([[0, 2], [0, 1]]);
    expect(get('c6b').rows[0].contextNote).toContain('Business owner has links');
    expect(get('c6d').rows[0].contextNote).toContain('Safe Pass');
    for (const row of get('c6d').rows) expect(row.parts?.map(p => p.permittedMarks)).toEqual([[0, 2], [0, 1]]);
    for (const letter of ['b', 'c', 'd']) expect(get(`c6${letter}`).stem).toContain(get('c6a').questionText);
  });

  it('retains every original Atlas identity and membership with complete original page ranges', () => {
    expect(anchors.paperFileid).toBe('LC462CLPO00EV.pdf');
    expect(anchors.schemeFileid).toBe('LC462CLP000EV.pdf');
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 17 }, (_, i) => String(i + 1)));
    expect(anchors.q.slice(11).map(q => [q.pP, q.endP])).toEqual([[14, 16], [17, 19], [20, 22], [23, 25], [26, 28], [29, 31]]);
    expect(anchors.q.find(q => q.n === '5')?.endP).toBe(5);
    expect(anchors.q.find(q => q.n === '10')?.endP).toBe(11);
    expect(anchors.q.find(q => q.n === '11')?.endP).toBe(12);
    expect(anchors.q.find(q => q.n === '17')?.region.map(r => r.p)).toEqual([15, 16]);
    expect(local.reviewedEnglish2016.markBankMappings).toHaveLength(39);
    expect(Object.keys(local.reviewedEnglish2016.originalAtlasTopicIds)).toHaveLength(17);
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'link-modules' && p.year === 2016 && p.lang === 'ev' && p.fileid === 'LC462CLPO00EV.pdf')!;
    for (const [n, topics] of Object.entries(local.reviewedEnglish2016.originalAtlasTopicIds)) expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!)).toEqual(expect.arrayContaining(topics));
    for (const mapping of local.reviewedEnglish2016.markBankMappings) {
      const topics = browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === mapping.n)!);
      expect(topics, mapping.id).toEqual(expect.arrayContaining(mapping.atlasTopicIds));
      expect(topics.some(t => curriculumNodeIdsForExamTopic(t).includes(mapping.topicId)), mapping.id).toBe(true);
    }
  });
});
