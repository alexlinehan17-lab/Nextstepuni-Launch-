/** @license SPDX-License-Identifier: Apache-2.0 */
import { describe, expect, it } from 'vitest';
import {
  CURRICULUM_SPECIFICATIONS,
  curriculumSubjectsForYear,
  findCanonicalTopic,
  getCurriculumCohortNotice,
  resolveCurriculumSpecification,
  specificationContainsId,
} from '../curriculumRegistry';
import {
  SUBJECTS as MARK_BANK_SUBJECTS,
  builtDecks,
  loadCards,
} from '../components/MarkBank/deck';

describe('versioned curriculum registry', () => {
  it('has unique specification and node ids within each specification', () => {
    expect(new Set(CURRICULUM_SPECIFICATIONS.map((spec) => spec.id)).size)
      .toBe(CURRICULUM_SPECIFICATIONS.length);

    for (const spec of CURRICULUM_SPECIFICATIONS) {
      const ids = spec.groups.flatMap((group) => [group.id, ...group.topics.map((topic) => topic.id)]);
      expect(new Set(ids).size, `${spec.id} contains duplicate canonical node ids`).toBe(ids.length);
    }
  });

  it('keeps programme catalogues separate', () => {
    const leavingCertificate = curriculumSubjectsForYear(2027, ['leaving-certificate-established']);
    expect(leavingCertificate.some((subject) => subject.id === 'biology')).toBe(true);
    expect(leavingCertificate.some((subject) => subject.id.startsWith('jc-'))).toBe(false);
    expect(leavingCertificate.some((subject) => subject.id.startsWith('lca-'))).toBe(false);
    expect(leavingCertificate.some((subject) => subject.id === 'bulgarian')).toBe(false);

    const juniorCycle = curriculumSubjectsForYear(2027, ['junior-cycle']);
    expect(juniorCycle.length).toBeGreaterThan(0);
    expect(juniorCycle.every((subject) => subject.id.startsWith('jc-'))).toBe(true);
  });

  it('resolves specification transitions by examination year', () => {
    const outgoingBiology = resolveCurriculumSpecification('Biology', 2026);
    expect(outgoingBiology?.id).toBe('biology:legacy-current');
    expect(outgoingBiology?.status).toBe('verified');
    expect(resolveCurriculumSpecification('Biology', 2027)?.id).toBe('biology:2027');
    expect(resolveCurriculumSpecification('Chemistry', 2027)?.id).toBe('chemistry:2027');
    expect(resolveCurriculumSpecification('Physics', 2027)?.id).toBe('physics:2027');
    expect(resolveCurriculumSpecification('Business', 2027)?.id).toBe('business:2027');
  });

  it('keeps the outgoing classical-language syllabi in the 2026 cohort', () => {
    const expected = [
      ['Ancient Greek', 'ancient-greek:outgoing-2026', 'Language and texts'],
      ['Latin', 'latin:outgoing-2026', 'Language and texts'],
      ['Arabic', 'arabic:outgoing-2026', 'Reading and directed writing'],
    ] as const;

    for (const [subject, id, firstGroup] of expected) {
      const specification = resolveCurriculumSpecification(subject, 2026)!;
      expect(specification.id).toBe(id);
      expect(specification.lastExamYear).toBe(2026);
      expect(specification.groups[0].title).toBe(firstGroup);
      expect(specification.groups.some((group) => group.title.startsWith('Strand 1:'))).toBe(false);
      expect(resolveCurriculumSpecification(subject, 2027)).toBeUndefined();
    }
  });

  it('keeps official provenance on every verified specification', () => {
    for (const spec of CURRICULUM_SPECIFICATIONS.filter((entry) => entry.status === 'verified')) {
      expect(spec.sources.length, `${spec.id} has no official source`).toBeGreaterThan(0);
      for (const source of spec.sources) {
        expect(source.url, `${spec.id} has a non-official source`).toMatch(/^https:\/\/(www\.)?curriculumonline\.ie\//);
      }
    }
  });

  it('represents Religious Education examination choices explicitly', () => {
    const spec = resolveCurriculumSpecification('Religious Education', 2027)!;
    expect(spec.selectionRules?.map((rule) => rule.choose ?? rule.requiredGroupIds?.length))
      .toEqual([1, 2, 1]);
    for (const rule of spec.selectionRules ?? []) {
      for (const id of [...(rule.requiredGroupIds ?? []), ...(rule.fromGroupIds ?? [])]) {
        expect(specificationContainsId(spec, id), `${id} is not in ${spec.id}`).toBe(true);
      }
    }
  });

  it('keeps Applied Mathematics distinct and models its official assessment contract', () => {
    const applied = resolveCurriculumSpecification('Applied Maths', 2027)!;
    const mathematics = resolveCurriculumSpecification('Mathematics', 2027)!;

    expect(applied.id).toBe('applied-mathematics:current');
    expect(applied.status).toBe('verified');
    expect(applied.recommendedClassHours).toBe(180);
    expect(applied.groups.map((group) => group.title)).toEqual([
      'Strand 1: Mathematical Modelling',
      'Strand 2: Mathematical Modelling with Networks and Graphs',
      'Strand 3: Mathematically Modelling the Physical World; Kinematics and Dynamics',
      'Strand 4: Mathematically Modelling a Changing World',
    ]);
    expect(applied.groups.flatMap((group) => group.topics).some((topic) =>
      mathematics.groups.some((group) => group.topics.some((entry) => entry.id === topic.id)),
    )).toBe(false);
    expect(applied.assessmentComponents?.map(({ title, weighting }) => ({ title, weighting }))).toEqual([
      { title: 'Modelling project', weighting: 20 },
      { title: 'Written examination', weighting: 80 },
    ]);
    expect(applied.assessmentComponents?.reduce((sum, component) => sum + component.weighting, 0)).toBe(100);
  });

  it('requires complete percentage allocations whenever assessment components are declared', () => {
    for (const spec of CURRICULUM_SPECIFICATIONS.filter((entry) => entry.assessmentComponents)) {
      const total = spec.assessmentComponents!.reduce((sum, component) => sum + component.weighting, 0);
      expect(total, `${spec.id} assessment weighting does not total 100%`).toBe(100);
    }
  });

  it('encodes the verified coursework split for History, Geography and Home Economics', () => {
    const expected = [
      ['History', 'Research study report'],
      ['Geography', 'Report on the geographical investigation'],
      ['Home Economics', 'Practical coursework'],
    ] as const;

    for (const [subject, courseworkTitle] of expected) {
      const spec = resolveCurriculumSpecification(subject, 2027)!;
      expect(spec.status).toBe('verified');
      expect(spec.assessmentComponents?.map(({ title, weighting }) => ({ title, weighting }))).toEqual([
        { title: courseworkTitle, weighting: 20 },
        { title: 'Written examination', weighting: 80 },
      ]);
    }
  });

  it('resolves the Geography replacement without carrying over the outgoing taxonomy', () => {
    expect(resolveCurriculumSpecification('Geography', 2027)?.id).toBe('geography:outgoing');
    const replacement = resolveCurriculumSpecification('Geography', 2028);
    expect(replacement?.id).toBe('geography:2028');
    expect(replacement?.groups.map((group) => group.title)).toEqual([
      'Applying geographical thinking and skills',
      'The physical environment',
      'The human environment',
      'The global environment',
    ]);
    expect(replacement?.assessmentComponents?.map(({ weighting }) => weighting)).toEqual([40, 60]);
  });

  it('does not silently carry outgoing specifications into replacement cohorts', () => {
    expect(resolveCurriculumSpecification('Construction Studies', 2027)?.id).toBe('construction-studies:outgoing');
    const constructionTechnology = resolveCurriculumSpecification('Construction Technology', 2028);
    expect(constructionTechnology?.id).toBe('construction-technology:2028');
    expect(constructionTechnology?.groups.map((group) => group.title)).toEqual([
      'Built Environment',
      'Design, Materials, and Craft Skills',
      'Building Fabric',
      'Services and Control Technology',
    ]);
    expect(constructionTechnology?.assessmentComponents?.map(({ weighting }) => weighting)).toEqual([30, 20, 50]);
    const engineering = resolveCurriculumSpecification('Engineering', 2028);
    expect(engineering?.id).toBe('engineering:2028');
    expect(engineering?.groups.map(({ title }) => title)).toEqual([
      'Engineering Processes',
      'Automation and Control Systems',
      'Design Capability',
      'Engineering Principles and Energy',
    ]);
    expect(engineering?.assessmentComponents?.map(({ weighting }) => weighting)).toEqual([50, 50]);

    const physicalEducation = resolveCurriculumSpecification('LCPE', 2028);
    expect(physicalEducation?.id).toBe('physical-education:2028');
    expect(physicalEducation?.groups.map(({ title }) => title)).toEqual([
      'Skill learning, participation and performance',
      'Physical and psychological demands of performance',
      'Factors influencing participation in physical activity',
    ]);
    expect(physicalEducation?.assessmentComponents?.map(({ weighting }) => weighting)).toEqual([50, 50]);

    const lifeCommunityWork = resolveCurriculumSpecification('LCVP', 2028);
    expect(lifeCommunityWork?.id).toBe('lcvp-link-modules:2028');
    expect(lifeCommunityWork?.subjectName).toBe('Life, Community and Work');
    expect(lifeCommunityWork?.assessmentComponents?.map(({ weighting }) => weighting)).toEqual([60, 40]);
    expect(resolveCurriculumSpecification('English', 2028)?.id).toBe('english:outgoing');
    expect(resolveCurriculumSpecification('English', 2029)).toBeUndefined();
    expect(resolveCurriculumSpecification('Accounting', 2028)?.id).toBe('accounting:outgoing');
    expect(resolveCurriculumSpecification('Accounting', 2029)).toBeUndefined();
  });

  it('puts explicit cohort notices on outgoing maps and blocks expired maps', () => {
    for (const subject of ['Construction Studies', 'Engineering', 'Geography', 'LCPE', 'LCVP']) {
      const notice = getCurriculumCohortNotice(subject, 2027);
      expect(notice?.kind, subject).toBe('outgoing');
      expect(notice?.title, subject).toBe('For 2027 exam candidates only');
      expect(notice?.message, subject).toContain('first examined in 2028');
    }

    const mathematics = getCurriculumCohortNotice('Mathematics', 2028);
    expect(mathematics?.title).toBe('Current specification — exams through 2028');
    expect(mathematics?.message).toContain('first examined in 2029');
    expect(resolveCurriculumSpecification('Mathematics', 2029)).toBeUndefined();

    const english = getCurriculumCohortNotice('English', 2028);
    expect(english?.message).toContain('earliest possible first examination year');
    expect(getCurriculumCohortNotice('Geography', 2028)).toBeUndefined();
  });

  it('models the official Computer Science certification split', () => {
    const specification = resolveCurriculumSpecification('Computer Science', 2027)!;
    expect(specification.id).toBe('computer-science:2025');
    expect(specification.assessmentComponents?.map(({ weighting }) => weighting)).toEqual([70, 30]);
  });

  it('models verified certification splits for Economics, Politics and Society, and Art', () => {
    const expected: Record<string, number[]> = {
      Economics: [20, 80],
      'Politics and Society': [20, 80],
      Art: [50, 20, 30],
    };

    for (const [subject, weightings] of Object.entries(expected)) {
      const specification = resolveCurriculumSpecification(subject, 2027)!;
      expect(specification.status).toBe('verified');
      expect(specification.assessmentComponents?.map(({ weighting }) => weighting)).toEqual(weightings);
    }
  });

  it('models verified Classical Studies, DCG, Technology and Music contracts', () => {
    expect(resolveCurriculumSpecification('Classical Studies', 2026)?.assessmentComponents
      ?.map(({ weighting }) => weighting)).toEqual([20, 80]);
    expect(resolveCurriculumSpecification('DCG', 2026)?.assessmentComponents
      ?.map(({ weighting }) => weighting)).toEqual([40, 60]);

    const technology = resolveCurriculumSpecification('Technology', 2026)!;
    expect(technology.assessmentComponents?.map(({ weighting }) => weighting)).toEqual([50, 50]);
    expect(technology.selectionRules?.[0]).toMatchObject({
      choose: 2,
      fromGroupIds: ['technology-7', 'technology-8', 'technology-9', 'technology-10', 'technology-11'],
    });

    const music = resolveCurriculumSpecification('Music', 2026)!;
    expect(music.selectionRules?.[0]).toMatchObject({
      choose: 1,
      fromGroupIds: ['music-0', 'music-1', 'music-2'],
    });
    expect(music.assessmentComponents).toBeUndefined();
  });

  it('models the official Gaeilge oral weighting without losing the June assessment', () => {
    const specification = resolveCurriculumSpecification('Gaeilge', 2027)!;
    expect(specification.id).toBe('irish:current');
    expect(specification.assessmentComponents?.map(({ title, weighting }) => ({ title, weighting }))).toEqual([
      { title: 'Oral examination', weighting: 40 },
      { title: 'Aural and written examinations', weighting: 60 },
    ]);
  });

  it('resolves every Mark Bank card into the correct canonical specification', async () => {
    const subjectForTopic = new Map<string, string>();
    for (const subject of MARK_BANK_SUBJECTS) {
      for (const topic of subject.strands.flatMap((strand) => strand.topics)) {
        subjectForTopic.set(topic.id, subject.id);
      }
    }

    for (const deck of builtDecks()) {
      const cards = await loadCards(deck.subjectId, deck.level);
      for (const card of cards) {
        const subjectId = subjectForTopic.get(card.topicId);
        expect(subjectId, `${card.id}: no subject owns ${card.topicId}`).toBe(deck.subjectId);
        const spec = resolveCurriculumSpecification(subjectId!, Math.max(2027, card.year))!;
        expect(findCanonicalTopic(spec, card.topicId), `${card.id}: ${card.topicId} absent from ${spec.id}`).toBeDefined();
      }
    }
  });
});
