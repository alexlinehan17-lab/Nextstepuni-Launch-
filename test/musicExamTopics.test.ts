/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Music reference-parity, exact-component joins and preservation gates.
 */

import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import * as pdfjs from 'pdfjs-dist/legacy/build/pdf.mjs';
import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import reference from '../data/examTopics/music.json';
import crosswalk from '../data/examTopics/music-local-crosswalk.json';
import curriculumCrosswalk from '../data/examTopics/music-curriculum-crosswalk.json';
import reconciliation from '../data/examTopics/music-audit-reconciliation.json';
import runtime from '../data/examTopics/music-runtime.json';
import snapshot from '../data/examTopics/studyclix-subject-taxonomy.json';
import baselineJson from './fixtures/musicTopicQuestionBaseline.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import {
  questionsForTopics,
  subjectAtlasStats,
  topicsForPaper,
  topicsForSubject,
} from '../components/PaperTrail/topics';
import {
  curriculumNodeIdsForExamTopic,
  examQuestionPartReferencesForSubject,
  examQuestionTopicMappingsForSubject,
  examTopicIdsForQuestion,
  examTopicTaxonomyFor,
} from '../data/examTopics/registry';

type Baseline = Array<{
  level: 'higher' | 'ordinary';
  lang: 'ev' | 'iv';
  year: number;
  fileid: string;
  paperKey: string;
  questions: Array<{ n: string; primary: string; secondary?: string }>;
}>;

const ROOT = process.cwd();
const baseline = baselineJson as Baseline;
const referenceTopics = Object.values(reference.variants).flatMap(variant => variant.topics);
const paperIdentity = (paper: { year: number; fileid: string }) => `${paper.year}|${paper.fileid}`;
const hasPython = (() => {
  try {
    execFileSync('python3', ['--version'], { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
})();

describe('Music exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('music')!;

  it('pins all 34 factual reference topics and nine explicit local archive shelves', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups.map(group => [group.id, group.label, group.level])).toEqual([
      ['music-higher', 'Higher Level', 'higher'],
      ['music-ordinary', 'Ordinary Level', 'ordinary'],
    ]);
    expect(taxonomy.topics).toHaveLength(43);
    expect(taxonomy.topics.slice(0, 34).map(topic => topic.id))
      .toEqual(referenceTopics.map(topic => topic.id));
    expect(taxonomy.topics.slice(0, 34).map(topic => topic.label))
      .toEqual(referenceTopics.map(topic => topic.label));
    expect(taxonomy.topics.slice(0, 34).map(topic => topic.sourcePath))
      .toEqual(referenceTopics.map(topic => topic.sourcePath));
    expect(taxonomy.topics.slice(34).map(topic => topic.id)).toEqual([
      'music-higher-listening-tchaikovsky-archive',
      'music-higher-listening-gerald-barry-archive',
      'music-higher-listening-freddie-mercury-archive',
      'music-higher-listening-bach-archive',
      'music-higher-listening-elective-archive',
      'music-ordinary-listening-tchaikovsky-archive',
      'music-ordinary-listening-gerald-barry-archive',
      'music-ordinary-listening-freddie-mercury-archive',
      'music-ordinary-listening-bach-archive',
    ]);
    expect(taxonomy.topics.slice(34).every(topic => topic.sourcePath.startsWith('/nextstepuni-preservation/')))
      .toBe(true);
    expect(topicsForSubject('music')).toHaveLength(43);
  });

  it('reconciles every factual heading and excluded mock to the visible counts', () => {
    expect(referenceTopics).toHaveLength(34);
    expect(reference.variants.higher.topics).toHaveLength(21);
    expect(reference.variants.ordinary.topics).toHaveLength(13);
    expect(referenceTopics.reduce((sum, topic) => sum + topic.reportedQuestionCount, 0)).toBe(1127);
    expect(referenceTopics.reduce((sum, topic) => sum + topic.officialQuestionHeadings.length, 0)).toBe(646);
    expect(referenceTopics.reduce((sum, topic) => sum + topic.mockQuestionCount, 0)).toBe(481);
    expect(referenceTopics.reduce((sum, topic) => sum + topic.sourceLabelConflictCount, 0)).toBe(6);
    expect(referenceTopics.filter(topic => topic.reportedQuestionCount === 0).map(topic => topic.id))
      .toEqual(['music-higher-practicals', 'music-ordinary-practicals']);

    for (const [level, variant] of Object.entries(reference.variants)) {
      const source = snapshot.variants.find(item => item.subjectSlug === 'music' && item.variant === level)!;
      expect(variant.topics.map(topic => [topic.label, topic.sourcePath]))
        .toEqual(source.topics.map(topic => [topic.label, topic.sourcePath]));
      for (const topic of variant.topics) {
        expect(topic.officialQuestionHeadings.length + topic.mockQuestionCount
          + topic.providerSampleQuestionCount).toBe(topic.reportedQuestionCount);
        expect(topic.officialQuestionHeadings.some(heading => /mock/i.test(heading))).toBe(false);
        expect(reconciliation.references.filter(row => row.topicId === topic.id).map(row => row.heading))
          .toEqual(topic.officialQuestionHeadings);
      }
    }
  });

  it('bridges every reference and archive shelf to canonical Music curriculum nodes', () => {
    const canonicalIds = new Set(
      CURRICULUM.find(subject => subject.id === 'music')!
        .strands.flatMap(strand => strand.subtopics.map(topic => topic.id)),
    );
    expect(Object.keys(curriculumCrosswalk)).toHaveLength(43);
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids, topic.id).toEqual(curriculumCrosswalk[topic.id as keyof typeof curriculumCrosswalk]);
      expect(ids.length, topic.id).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), topic.id).toEqual([]);
    }
  });

  it('retains all 646 factual headings without using them as collision-prone generic joins', () => {
    const references = examQuestionPartReferencesForSubject('music');
    const expected = referenceTopics.flatMap(topic => (
      topic.officialQuestionHeadings.map(heading => `${topic.id}|${heading}`)
    )).sort();
    const actual = references.map(item => `${item.topicId}|${item.subdivision}`).sort();
    expect(references).toHaveLength(646);
    expect(actual).toEqual(expected);
    expect(references.filter(item => item.fileid)).toHaveLength(459);
    expect(references.filter(item => !item.fileid)).toHaveLength(187);
    expect(references.every(item => item.paperKey === 'single')).toBe(true);
    expect(taxonomy.topics.every(topic => topic.officialQuestionKeys.length === 0)).toBe(true);
  });

  it('keeps component and sitting distinct in the pre-migration review snapshot', () => {
    expect(reconciliation.status).toBe('pre-migration-review-snapshot');
    expect(reconciliation.counts).toMatchObject({
      localPaperVariants: 178,
      taggedVariants: 20,
      untaggedVariants: 158,
      variantsWithAnswerMaps: 132,
      preservedVariants: 20,
      preservedCards: 184,
    });
    for (const row of reconciliation.references) {
      if (row.sitting !== 'main') {
        expect(row.localFileids).toEqual([]);
        expect(row.candidateCards).toEqual([]);
        expect(row.status).toBe('official-source-required');
      }
      for (const fileid of row.localFileids) {
        expect(fileid.slice(8, 11)).toBe(row.component);
        expect(fs.existsSync(path.join(ROOT, 'paper-trail-corpus/exampapers', String(row.year), fileid)))
          .toBe(true);
      }
    }
    const listening = reconciliation.references.find(row => row.level === 'higher'
      && row.heading === '2021 - Listening Paper - Section 6 - Question E1 - Part (a - b)')!;
    expect(listening.component).toBe('008');
    expect(listening.question).toBe('6');
    const composing = reconciliation.references.find(row => (
      row.heading === '2020 - Composing Paper - Question B - Part 6'
    ))!;
    expect(composing.component).toBe('006');
    expect(composing.question).toBe('6');
    expect(reconciliation.references.filter(row => row.component === 'U00')).toHaveLength(34);
  });

  it('preserves all 184 frozen cards and their canonical tags verbatim', () => {
    expect(baseline).toHaveLength(20);
    expect(baseline.reduce((sum, paper) => sum + paper.questions.length, 0)).toBe(184);
    for (const expected of baseline) {
      const live = topicsForPaper('music', expected.year, expected.level, expected.lang, expected.fileid);
      expect(live, paperIdentity(expected)).not.toBeNull();
      expect(live!.paperKey).toBe(expected.paperKey);
      for (const question of expected.questions) {
        expect(live!.q, `${paperIdentity(expected)} Q${question.n}`).toContainEqual(question);
      }
    }
  });

  it('adds all 178 exact SEC paper variants and all 978 physical question mappings', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'music');
    expect(crosswalk.summary).toMatchObject({
      referenceTopics: 34,
      archiveTopics: 9,
      totalRuntimeTopics: 43,
      referenceOfficialAssociations: 646,
      matchedAssociations: 459,
      sourceBlockedAssociations: 187,
      localPaperVariants: 178,
      localPhysicalMappings: 978,
      distinctStudentFacingQuestions: 500,
      hostedPaperAnchorMaps: 178,
      preservedHostedAnchorMaps: 19,
      generatedHostedAnchorMaps: 159,
      existingAnswerSidecarMaps: 161,
      existingAnswerSidecarCrops: 775,
      completeExistingAnswerSidecarMaps: 152,
      partialExistingAnswerSidecarMaps: 9,
      preservedBaselineVariants: 20,
      preservedBaselineCards: 184,
      newlyAddedPaperVariants: 158,
      newlyAddedPhysicalMappings: 794,
    });
    expect(crosswalk.status).toBe('runtime-mapped-source-completion-pending');
    expect(crosswalk.policy.excludedContent).toContain('No commercial mock question');
    expect(papers).toHaveLength(178);
    expect(papers.reduce((sum, paper) => sum + paper.q.length, 0)).toBe(978);
    expect(runtime.questionMappings).toHaveLength(978);
    const mappings = examQuestionTopicMappingsForSubject('music');
    expect(mappings).toHaveLength(978);
    expect(mappings.every(mapping => mapping.fileid && mapping.lang !== 'any')).toBe(true);
    expect(subjectAtlasStats('music')).toMatchObject({
      questions: 500,
      topics: 43,
      yearMin: 2010,
      yearMax: 2026,
    });
    expect(questionsForTopics('music', null)).toHaveLength(500);
  });

  it('keeps same-number composing, listening and elective cards isolated by file ID', () => {
    const composing = examTopicIdsForQuestion(
      'music', 'higher', 2025, 'main', '1', 'single', 'ev', 'LC067ALP006EV.pdf',
    );
    const elective = examTopicIdsForQuestion(
      'music', 'higher', 2025, 'main', '1', 'single', 'ev', 'LC067ALP007EV.pdf',
    );
    const listening = examTopicIdsForQuestion(
      'music', 'higher', 2025, 'main', '1', 'single', 'ev', 'LC067ALP008EV.pdf',
    );
    expect(composing).toContain('music-higher-composing-continuation-of-a-given-opening');
    expect(elective).toEqual(['music-higher-listening-elective-archive']);
    expect(listening).toContain('music-higher-listening-tchaikovsky-archive');
    expect(new Set([composing.join('|'), elective.join('|'), listening.join('|')]).size).toBe(3);
    expect(examTopicIdsForQuestion('music', 'higher', 2025, 'main', '1', 'single', 'ev'))
      .toEqual([]);
  });

  it('uses truthful current and historic set works plus the shared Irish/aural shelves', () => {
    expect(examTopicIdsForQuestion(
      'music', 'higher', 2026, 'main', '1', 'single', 'ev', 'LC067ALP008EV.pdf',
    )).toContain('music-higher-listening-berlioz');
    expect(examTopicIdsForQuestion(
      'music', 'ordinary', 2024, 'main', '2', 'single', 'iv', 'LC067GLP008IV.pdf',
    )).toContain('music-ordinary-listening-bach-archive');
    expect(examTopicIdsForQuestion(
      'music', 'higher', 2025, 'main', '5', 'single', 'ev', 'LC067ALP008EV.pdf',
    )).toEqual(expect.arrayContaining([
      'music-higher-listening-irish-music',
      'music-higher-listening-irish-music-essay',
    ]));
    expect(examTopicIdsForQuestion(
      'music', 'ordinary', 2025, 'main', '6', 'single', 'iv', 'LC067GLP008IV.pdf',
    )).toContain('music-ordinary-listening-aural-skills-unheard');
  });

  it('pins every visually checked elective start, including the 2026 layout change', () => {
    const electives = PAPER_TOPIC_TAGS.filter(item => (
      item.subjectId === 'music' && item.fileid.slice(8, 11) === '007'
    ));
    expect(electives).toHaveLength(32);
    for (const paper of electives) {
      const anchor = JSON.parse(fs.readFileSync(path.join(
        ROOT, 'public/paper-anchors', String(paper.year), `${paper.fileid}.json`,
      ), 'utf8'));
      const expectedPage = paper.year === 2026 ? 4 : 2;
      expect(anchor.q[0].pP).toBe(expectedPage);
      expect(anchor.q[0].paperRegion).toEqual([{ p: expectedPage, r: [0, 0, 1, 1] }]);
    }
  });

  it('starts 2018 listening Question 2 after Question 1 ends in every edition', () => {
    for (const level of ['A', 'G']) {
      for (const lang of ['EV', 'IV']) {
        const anchor = JSON.parse(fs.readFileSync(path.join(
          ROOT, 'public/paper-anchors/2018', `LC067${level}LP008${lang}.pdf.json`,
        ), 'utf8'));
        expect(anchor.q.find((question: { n: string }) => question.n === '1').paperRegion)
          .toEqual([
            { p: 2, r: [0, 0, 1, 1] },
            { p: 3, r: [0, 0, 1, 1] },
          ]);
        expect(anchor.q.find((question: { n: string }) => question.n === '2').pP).toBe(4);
      }
    }
  });

  it('pins all visually checked unprepared-test card pages and crop ordering', () => {
    const unprepared = PAPER_TOPIC_TAGS.filter(item => (
      item.subjectId === 'music' && item.fileid.slice(8, 11) === 'U00'
    ));
    expect(unprepared).toHaveLength(14);
    expect(unprepared.reduce((sum, paper) => sum + paper.q.length, 0)).toBe(154);
    for (const paper of unprepared) {
      const anchor = JSON.parse(fs.readFileSync(path.join(
        ROOT, 'public/paper-anchors', String(paper.year), `${paper.fileid}.json`,
      ), 'utf8'));
      const firstPage = paper.year === 2016 && paper.level === 'higher' ? 2 : 3;
      const expectedPages = paper.q.map((_, index) => firstPage + Math.floor(index / 4));
      expect(anchor.q.map((question: { pP: number }) => question.pP)).toEqual(expectedPages);

      for (const page of new Set(expectedPages)) {
        const pageQuestions = anchor.q.filter((question: { pP: number }) => question.pP === page);
        for (let index = 0; index < pageQuestions.length; index += 1) {
          const [start, end] = pageQuestions[index].pY;
          expect(start).toBeGreaterThanOrEqual(0);
          expect(end).toBeLessThanOrEqual(1);
          expect(end).toBeGreaterThan(start);
          if (index > 0) expect(start).toBeGreaterThanOrEqual(pageQuestions[index - 1].pY[1]);
        }
      }
    }
  });

  it('ships a finite, exact-card paper map for every Music booklet', () => {
    for (const paper of PAPER_TOPIC_TAGS.filter(item => item.subjectId === 'music')) {
      const anchorPath = path.join(ROOT, 'public/paper-anchors', String(paper.year), `${paper.fileid}.json`);
      expect(fs.existsSync(anchorPath), anchorPath).toBe(true);
      const anchor = JSON.parse(fs.readFileSync(anchorPath, 'utf8'));
      expect(anchor.paperFileid).toBe(paper.fileid);
      expect(anchor.paperOnly).toBe(1);
      expect(anchor.schemeFileid).toBe('');
      expect(anchor.q.map((question: { n: string }) => question.n)).toEqual(paper.q.map(question => question.n));
      for (const question of anchor.q) {
        expect(Number.isFinite(question.pP)).toBe(true);
        expect(question.pP).toBeGreaterThan(0);
        expect(question.pY).toHaveLength(2);
        expect(question.pY.every((value: number) => Number.isFinite(value))).toBe(true);
        expect(question.mode).toBe('pagejump');
        expect(question.conf).toBeLessThan(0.6);
      }
    }
  });

  it('keeps all hosted Music page references within their entitled paper PDFs', async () => {
    for (const paper of PAPER_TOPIC_TAGS.filter(item => item.subjectId === 'music')) {
      const anchorPath = path.join(ROOT, 'public/paper-anchors', String(paper.year), `${paper.fileid}.json`);
      const paperPath = path.join(ROOT, 'paper-trail-corpus/exampapers', String(paper.year), paper.fileid);
      const anchor = JSON.parse(fs.readFileSync(anchorPath, 'utf8'));
      const loadingTask = pdfjs.getDocument({
        data: new Uint8Array(fs.readFileSync(paperPath)),
      });
      const document = await loadingTask.promise;
      const pages = anchor.q.flatMap((question: {
        pP: number;
        paperRegion?: Array<{ p: number }>;
      }) => [question.pP, ...(question.paperRegion ?? []).map(segment => segment.p)]);
      expect(Math.min(...pages), paperIdentity(paper)).toBeGreaterThanOrEqual(1);
      expect(Math.max(...pages), paperIdentity(paper)).toBeLessThanOrEqual(document.numPages);
      await loadingTask.destroy();
    }
  }, 30_000);

  it('accounts for existing verified answer sidecars without promoting them into hosted anchors', async () => {
    let maps = 0;
    let crops = 0;
    let complete = 0;
    const schemePageCounts = new Map<string, number>();
    const answerRegionOwners = new Map<string, { component: string; fileid: string }>();
    for (const paper of PAPER_TOPIC_TAGS.filter(item => item.subjectId === 'music')) {
      const sidecarPath = path.join(
        ROOT, 'scripts/paper-trail/answers', String(paper.year), `${paper.fileid}.json`,
      );
      if (!fs.existsSync(sidecarPath)) continue;
      maps += 1;
      const sidecar = JSON.parse(fs.readFileSync(sidecarPath, 'utf8'));
      const expectedNumbers = new Set(paper.q.map(question => question.n));
      const actualNumbers = sidecar.q.map((question: { n: string }) => question.n);
      crops += actualNumbers.length;
      if (actualNumbers.length === expectedNumbers.size) complete += 1;
      expect(sidecar.paperFileid).toBe(paper.fileid);
      expect(sidecar.schemeFileid).not.toBe('');
      const schemePath = path.join(
        ROOT, 'paper-trail-corpus/markingschemes', String(paper.year), sidecar.schemeFileid,
      );
      expect(fs.existsSync(schemePath)).toBe(true);
      let schemePages = schemePageCounts.get(schemePath);
      if (!schemePages) {
        const loadingTask = pdfjs.getDocument({
          data: new Uint8Array(fs.readFileSync(schemePath)),
        });
        const document = await loadingTask.promise;
        schemePages = document.numPages;
        schemePageCounts.set(schemePath, schemePages);
        await loadingTask.destroy();
      }
      expect(new Set(actualNumbers).size).toBe(actualNumbers.length);
      expect(actualNumbers.every((number: string) => expectedNumbers.has(number))).toBe(true);
      let previousQuestionEnd: { page: number; y: number } | null = null;
      for (const question of sidecar.q as Array<{
        n: string;
        mode: string;
        conf: number;
        region: Array<{ p: number; r: number[] }>;
      }>) {
        expect(question.mode, `${paperIdentity(paper)} Q${question.n}`).toBe('crop');
        expect(question.conf, `${paperIdentity(paper)} Q${question.n}`).toBeGreaterThanOrEqual(0.9);
        expect(question.region.length, `${paperIdentity(paper)} Q${question.n}`).toBeGreaterThan(0);
        let totalArea = 0;
        let firstStart: { page: number; y: number } | null = null;
        let previousEnd: { page: number; y: number } | null = null;
        for (const segment of question.region) {
          expect(Number.isInteger(segment.p), `${paperIdentity(paper)} Q${question.n}`).toBe(true);
          expect(segment.p, `${paperIdentity(paper)} Q${question.n}`).toBeGreaterThan(0);
          expect(segment.p, `${paperIdentity(paper)} Q${question.n}`).toBeLessThanOrEqual(schemePages);
          expect(segment.r, `${paperIdentity(paper)} Q${question.n}`).toHaveLength(4);
          const [x0, y0, x1, y1] = segment.r;
          expect(segment.r.every(value => Number.isFinite(value) && value >= 0 && value <= 1),
            `${paperIdentity(paper)} Q${question.n}`).toBe(true);
          expect(x1, `${paperIdentity(paper)} Q${question.n}`).toBeGreaterThan(x0);
          expect(y1, `${paperIdentity(paper)} Q${question.n}`).toBeGreaterThan(y0);
          if (previousEnd) {
            expect(
              segment.p > previousEnd.page
                || (segment.p === previousEnd.page && y0 >= previousEnd.y),
              `${paperIdentity(paper)} Q${question.n} scheme regions run backwards`,
            ).toBe(true);
          }
          firstStart ??= { page: segment.p, y: y0 };
          previousEnd = { page: segment.p, y: y1 };
          totalArea += (x1 - x0) * (y1 - y0);
        }
        expect(totalArea, `${paperIdentity(paper)} Q${question.n}`).toBeGreaterThanOrEqual(0.12);
        if (previousQuestionEnd && firstStart) {
          const pageDelta = firstStart.page - previousQuestionEnd.page;
          expect(
            (pageDelta === 0
              && firstStart.y >= previousQuestionEnd.y - 0.0121
              && firstStart.y <= previousQuestionEnd.y + 0.02)
              || (pageDelta === 1
                && previousQuestionEnd.y >= 0.99
                && firstStart.y <= 0.01),
            `${paperIdentity(paper)} Q${question.n} is not contiguous with the previous scheme crop`,
          ).toBe(true);
        }
        previousQuestionEnd = previousEnd;
      }

      const component = paper.fileid.slice(8, 11);
      const regionIdentity = [
        paper.year,
        paper.level,
        paper.lang,
        sidecar.schemeFileid,
        JSON.stringify(sidecar.q.map((question: { n: string; region: unknown }) => ({
          n: question.n,
          region: question.region,
        }))),
      ].join('|');
      const existingOwner = answerRegionOwners.get(regionIdentity);
      if (existingOwner) {
        expect(existingOwner.component, `${paper.fileid} duplicates ${existingOwner.fileid}`)
          .toBe(component);
      }
      answerRegionOwners.set(regionIdentity, { component, fileid: paper.fileid });

      const anchorPath = path.join(ROOT, 'public/paper-anchors', String(paper.year), `${paper.fileid}.json`);
      const anchor = JSON.parse(fs.readFileSync(anchorPath, 'utf8'));
      expect(anchor.paperOnly).toBe(1);
      expect(anchor.schemeFileid).toBe('');
    }
    expect({ maps, crops, complete, partial: maps - complete }).toEqual({
      maps: 161,
      crops: 775,
      complete: 152,
      partial: 9,
    });
    expect(schemePageCounts.size).toBe(65);
  }, 30_000);

  it.skipIf(!hasPython)('reproduces all 29 recovered scheme maps and keeps only honest paper-only gaps', () => {
    const check = execFileSync('python3', [
      path.join(ROOT, 'scripts/paper-trail/music_sections.py'), '--check-recovered',
    ], { cwd: ROOT, encoding: 'utf8' });
    expect(JSON.parse(check.trim().split('\n').at(-1)!)).toEqual({ checked: 29, mismatched: 0 });

    const paperOnly = PAPER_TOPIC_TAGS.filter(paper => (
      paper.subjectId === 'music'
      && !fs.existsSync(path.join(
        ROOT, 'scripts/paper-trail/answers', String(paper.year), `${paper.fileid}.json`,
      ))
    ));
    expect(paperOnly.map(paper => `${paper.year}|${paper.fileid}`).sort()).toEqual([
      '2010|LC067ALP006IV.pdf',
      '2010|LC067ALP007IV.pdf',
      '2010|LC067ALP008IV.pdf',
      '2013|LC067ALPU00EV.pdf',
      '2013|LC067GLPU00EV.pdf',
      '2014|LC067ALPU00EV.pdf',
      '2014|LC067ALPU00IV.pdf',
      '2014|LC067GLPU00EV.pdf',
      '2014|LC067GLPU00IV.pdf',
      '2015|LC067ALPU00EV.pdf',
      '2015|LC067ALPU00IV.pdf',
      '2015|LC067GLPU00EV.pdf',
      '2015|LC067GLPU00IV.pdf',
      '2016|LC067ALPU00EV.pdf',
      '2016|LC067ALPU00IV.pdf',
      '2016|LC067GLPU00EV.pdf',
      '2016|LC067GLPU00IV.pdf',
    ]);
    expect(paperOnly.filter(paper => paper.fileid.slice(8, 11) === 'U00')).toHaveLength(14);
  }, 30_000);

  it('pins the fourteen original Music component-band repairs', () => {
    const expectedStarts: Array<[number, string, number[], [number, number]]> = [
      [2013, 'LC067ALP008EV.pdf', [8, 9, 9, 9, 10, 11], [8, 12]],
      [2013, 'LC067ALP008IV.pdf', [8, 9, 9, 9, 10, 11], [8, 12]],
      [2017, 'LC067GLP006IV.pdf', [3, 4, 5, 6, 7, 8], [3, 9]],
      [2018, 'LC067ALP006EV.pdf', [3, 4, 5, 6, 7, 8], [3, 9]],
      [2018, 'LC067ALP006IV.pdf', [3, 4, 5, 6, 7, 8], [3, 9]],
      [2018, 'LC067GLP008IV.pdf', [12, 14, 15, 16, 17, 18], [12, 19]],
      [2019, 'LC067ALP006IV.pdf', [3, 4, 5, 6, 7, 8], [3, 9]],
      [2019, 'LC067GLP006IV.pdf', [3, 4, 5, 7, 8, 9], [3, 10]],
      [2020, 'LC067ALP006IV.pdf', [3, 4, 5, 6, 7, 8], [3, 9]],
      [2022, 'LC067ALP006EV.pdf', [3, 4, 5, 6, 7, 8], [3, 9]],
      [2022, 'LC067ALP006IV.pdf', [3, 4, 5, 6, 7, 8], [3, 9]],
      [2022, 'LC067ALP008IV.pdf', [11, 13, 14, 15, 16, 18], [11, 20]],
      [2023, 'LC067ALP006IV.pdf', [3, 4, 5, 6, 7, 8], [3, 9]],
      [2024, 'LC067ALP008IV.pdf', [14, 16, 17, 18, 19, 21], [14, 23]],
    ];

    for (const [year, fileid, starts, band] of expectedStarts) {
      const sidecar = JSON.parse(fs.readFileSync(path.join(
        ROOT, 'scripts/paper-trail/answers', String(year), `${fileid}.json`,
      ), 'utf8'));
      expect(sidecar.q.map((question: { n: string }) => question.n), `${year}|${fileid}`)
        .toEqual(['1', '2', '3', '4', '5', '6']);
      expect(sidecar.q.map((question: { region: Array<{ p: number }> }) => question.region[0].p),
        `${year}|${fileid}`).toEqual(starts);
      expect(sidecar.band, `${year}|${fileid}`).toEqual(band);
      expect(Math.max(...sidecar.q.flatMap((question: { region: Array<{ p: number }> }) => (
        question.region.map(segment => segment.p)
      ))), `${year}|${fileid}`).toBeLessThan(band[1]);
    }

    const ordinaryIrish2018 = JSON.parse(fs.readFileSync(path.join(
      ROOT, 'scripts/paper-trail/answers/2018/LC067GLP008IV.pdf.json',
    ), 'utf8'));
    expect(ordinaryIrish2018.q[1].region.map((segment: { p: number }) => segment.p)).toEqual([14, 15]);
    expect(ordinaryIrish2018.q[1].region[0].r[1]).toBeLessThan(ordinaryIrish2018.q[1].region[0].r[3]);

  });

  it('pins nine rendered listening-table repairs at their real row starts', () => {
    const expectedStarts: Array<[number, string, Array<[number, number]>]> = [
      [2010, 'LC067GLP008EV.pdf', [[5, 0], [6, 0], [6, 0.3316], [6, 0.5888], [7, 0], [8, 0]]],
      [2011, 'LC067ALP008EV.pdf', [[8, 0], [8, 0.6443], [9, 0], [9, 0.5431], [10, 0], [11, 0]]],
      [2011, 'LC067ALP008IV.pdf', [[8, 0], [8, 0.6496]]],
      [2013, 'LC067ALP008EV.pdf', [[8, 0], [9, 0], [9, 0.3864], [9, 0.6224], [10, 0], [11, 0]]],
      [2013, 'LC067ALP008IV.pdf', [[8, 0], [9, 0], [9, 0.3973], [9, 0.6341], [10, 0], [11, 0]]],
      [2013, 'LC067GLP008EV.pdf', [[5, 0], [6, 0], [6, 0.3386], [6, 0.6219], [7, 0], [8, 0]]],
      [2014, 'LC067ALP008IV.pdf', [[11, 0], [12, 0.374], [13, 0]]],
      [2014, 'LC067GLP008EV.pdf', [[7, 0], [8, 0], [9, 0], [10, 0], [11, 0], [12, 0]]],
      [2014, 'LC067GLP008IV.pdf', [[7, 0], [8, 0]]],
    ];

    for (const [year, fileid, starts] of expectedStarts) {
      const sidecar = JSON.parse(fs.readFileSync(path.join(
        ROOT, 'scripts/paper-trail/answers', String(year), `${fileid}.json`,
      ), 'utf8'));
      expect(sidecar.q.map((question: { region: Array<{ p: number; r: number[] }> }) => (
        [question.region[0].p, question.region[0].r[1]]
      )), `${year}|${fileid}`).toEqual(starts);
    }
  });

  it('pins twenty-three rendered composing-table repairs at their real row starts', () => {
    const expectedStarts: Array<[number, string, Array<[number, number]>]> = [
      [2010, 'LC067GLP006EV.pdf', [[3, 0], [3, 0.3907], [3, 0.6641], [4, 0], [4, 0.2906], [4, 0.589]]],
      [2010, 'LC067GLP006IV.pdf', [[2, 0], [2, 0.3787], [2, 0.652], [3, 0], [3, 0.2896], [3, 0.588]]],
      [2011, 'LC067ALP006EV.pdf', [[3, 0], [3, 0.5471], [4, 0], [5, 0], [5, 0.6443], [6, 0]]],
      [2011, 'LC067ALP006IV.pdf', [[3, 0], [3, 0.5527], [4, 0], [5, 0], [5, 0.6445], [6, 0]]],
      [2011, 'LC067GLP006EV.pdf', [[3, 0], [3, 0.4001], [3, 0.6439], [4, 0], [4, 0.3011], [4, 0.5197]]],
      [2011, 'LC067GLP006IV.pdf', [[3, 0], [3, 0.4001], [3, 0.6453], [4, 0], [4, 0.3011], [4, 0.5197]]],
      [2013, 'LC067ALP006EV.pdf', [[3, 0], [3, 0.5473], [4, 0], [5, 0], [5, 0.6445], [6, 0]]],
      [2013, 'LC067ALP006IV.pdf', [[3, 0], [3, 0.5527], [4, 0], [5, 0], [5, 0.6445], [6, 0]]],
      [2013, 'LC067GLP006EV.pdf', [[3, 0], [3, 0.4001], [3, 0.6439], [4, 0], [4, 0.3011], [4, 0.5197]]],
      [2013, 'LC067GLP006IV.pdf', [[3, 0], [3, 0.4001], [3, 0.6453], [4, 0], [4, 0.3011], [4, 0.5197]]],
      [2014, 'LC067ALP006EV.pdf', [[3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0]]],
      [2014, 'LC067ALP006IV.pdf', [[3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0]]],
      [2014, 'LC067GLP006EV.pdf', [[3, 0], [4, 0], [5, 0], [6, 0], [6, 0.3741], [6, 0.6476]]],
      [2014, 'LC067GLP006IV.pdf', [[3, 0], [4, 0], [5, 0], [6, 0], [6, 0.3641], [6, 0.6377]]],
      [2015, 'LC067ALP006EV.pdf', [[3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0]]],
      [2016, 'LC067ALP006EV.pdf', [[3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0]]],
      [2017, 'LC067ALP006EV.pdf', [[3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0]]],
      [2017, 'LC067ALP006IV.pdf', [[3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0]]],
      [2019, 'LC067ALP006EV.pdf', [[3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0]]],
      [2023, 'LC067ALP006IV.pdf', [[3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0]]],
      [2024, 'LC067ALP006EV.pdf', [[3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [9, 0]]],
      [2024, 'LC067ALP006IV.pdf', [[3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [9, 0]]],
      [2025, 'LC067ALP006EV.pdf', [[3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0]]],
    ];

    for (const [year, fileid, starts] of expectedStarts) {
      const sidecar = JSON.parse(fs.readFileSync(path.join(
        ROOT, 'scripts/paper-trail/answers', String(year), `${fileid}.json`,
      ), 'utf8'));
      expect(sidecar.q.map((question: { region: Array<{ p: number; r: number[] }> }) => (
        [question.region[0].p, question.region[0].r[1]]
      )), `${year}|${fileid}`).toEqual(starts);
    }
  });

  it('ends all nine intentionally partial Irish listening maps before the next unmapped answer', () => {
    const expectedEnds: Array<[number, string, string, Array<{ p: number; r: number[] }>]> = [
      [2010, 'LC067GLP008IV.pdf', '2', [{ p: 5, r: [0, 0, 1, 0.3305] }]],
      [2011, 'LC067ALP008IV.pdf', '2', [{ p: 8, r: [0, 0.6496, 1, 1] }]],
      [2013, 'LC067GLP008IV.pdf', '2', [{ p: 6, r: [0, 0, 1, 0.3369] }]],
      [2014, 'LC067ALP008IV.pdf', '3', [{ p: 13, r: [0, 0, 1, 1] }]],
      [2014, 'LC067GLP008IV.pdf', '2', [{ p: 8, r: [0, 0, 1, 1] }]],
      [2015, 'LC067ALP008IV.pdf', '2', [{ p: 12, r: [0, 0, 1, 1] }]],
      [2015, 'LC067GLP008IV.pdf', '1', [{ p: 10, r: [0, 0, 1, 1] }]],
      [2016, 'LC067ALP008IV.pdf', '2', [{ p: 12, r: [0, 0, 1, 1] }]],
      [2016, 'LC067GLP008IV.pdf', '2', [{ p: 11, r: [0, 0, 1, 1] }]],
    ];

    for (const [year, fileid, finalNumber, expectedRegion] of expectedEnds) {
      const sidecar = JSON.parse(fs.readFileSync(path.join(
        ROOT, 'scripts/paper-trail/answers', String(year), `${fileid}.json`,
      ), 'utf8'));
      expect(sidecar.q.at(-1).n, `${year}|${fileid}`).toBe(finalNumber);
      expect(sidecar.q.at(-1).region, `${year}|${fileid}`).toEqual(expectedRegion);
    }
  });

  it.skipIf(!hasPython)('keeps every Music sidecar reconciled with the audited repair source', () => {
    const check = execFileSync('python3', [
      path.join(ROOT, 'scripts/paper-trail/repair-music-answer-sidecars.py'), '--check',
    ], { cwd: ROOT, encoding: 'utf8' });
    expect(JSON.parse(check)).toMatchObject({ auditedSchemeRepairs: 52, changedFiles: 0 });
  });
});
