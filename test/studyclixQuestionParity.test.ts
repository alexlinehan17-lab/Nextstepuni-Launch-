/** @license SPDX-License-Identifier: Apache-2.0 */

import fs from 'node:fs';
import path from 'node:path';
import { beforeAll, describe, expect, it } from 'vitest';
import { browseTopicIdsForQuestion, topicsForPaper } from '../components/PaperTrail/topics';
import parityJson from '../data/examTopics/studyclix-question-parity.json';
import mathsTopicDifferences from './fixtures/studyclixMathsTopicDifferences.json';
import { examTopicDefinition } from '../data/examTopics/registry';
import { PAPER_TRAIL_INDEX } from '../paperTrailData';
import { atlasHeadings, isModelSubject, loadAllAtlasModels } from '../components/PaperTrail/atlasModel';
import type { PaperLang, PaperLevel } from '../types/paperTrail';

interface CrosswalkTarget {
  fileid: string;
  lang: PaperLang;
  level: PaperLevel;
  year?: number;
  n?: string | number;
  questionNumber?: string | number;
  questionNumbers?: Array<string | number>;
}

interface CrosswalkAssociation {
  topicId: string;
  heading: string;
  year?: number;
  resolution: 'matched' | 'source-blocked' | 'reference-anomaly';
  reason?: string;
  target?: CrosswalkTarget;
  targets?: CrosswalkTarget[];
}

interface Crosswalk {
  subjectId: string;
  associations?: CrosswalkAssociation[];
}

const ROOT = process.cwd();

// Maths files each part by what it asks since the 2026-11-18 release (Alex R9,
// 18 Nov): these StudyClix headings no longer reach their topic. Pinned and
// shrink-only: never add a key; a key whose heading resolves again must come
// out. The uniform-heading rollout re-files every Maths part (its Stage 2).
const PINNED_MATHS_TOPIC_DIFFERENCES = new Set<string>(mathsTopicDifferences.keys);

// The single model (Alex, 18 Nov 2026): a switched-on subject shows ONE heading list and files every part by what
// it asks. A StudyClix topic that is not on that list (the other course) is not shown at all, so it is not checked;
// a StudyClix heading whose question the model files elsewhere is a filing difference, listed per subject in
// test/fixtures/studyclixModelTopicDifferences.json. Shrink-only like the Maths list: a new difference fails, and a
// listed one that resolves must come off. STUDYCLIX_MODEL_DIFFERENCES_WRITE=1 rewrites the file; it refuses to grow
// a subject already listed and adds a newly switched-on subject.
const MODEL_FIXTURE = path.join(__dirname, 'fixtures', 'studyclixModelTopicDifferences.json');
const modelPinned: Record<string, string[]> = fs.existsSync(MODEL_FIXTURE)
  ? (JSON.parse(fs.readFileSync(MODEL_FIXTURE, 'utf8')) as { subjects: Record<string, string[]> }).subjects : {};
beforeAll(() => loadAllAtlasModels());
const physicalCardCache = new Map<string, Set<string>>();

const physicalCardNumbers = (year: number, fileid: string): Set<string> => {
  const key = `${year}|${fileid}`;
  const cached = physicalCardCache.get(key);
  if (cached) return cached;
  const candidates = [
    path.join(ROOT, 'scripts/paper-trail/answers', String(year), `${fileid}.json`),
    path.join(ROOT, 'public/paper-anchors', String(year), `${fileid}.json`),
  ];
  const numbers = new Set<string>();
  for (const candidate of candidates) {
    if (!fs.existsSync(candidate)) continue;
    const sidecar = JSON.parse(fs.readFileSync(candidate, 'utf8')) as { q?: Array<{ n: string | number }> };
    for (const question of sidecar.q ?? []) numbers.add(String(question.n));
  }
  physicalCardCache.set(key, numbers);
  return numbers;
};

const targetQuestionNumbers = (target: CrosswalkTarget): string[] => {
  const values = target.n !== undefined
    ? [target.n]
    : target.questionNumber !== undefined
      ? [target.questionNumber]
      : target.questionNumbers ?? [];
  return values.flatMap(value => String(value).split(',')).map(value => value.trim()).filter(Boolean);
};

const associationYear = (association: CrosswalkAssociation, target: CrosswalkTarget): number | null => {
  if (target.year) return target.year;
  if (association.year) return association.year;
  const match = association.heading.match(/\b(?:19|20)\d{2}\b/);
  return match ? Number(match[0]) : null;
};

describe('StudyClix official-question parity', () => {
  it('accounts for every captured State-exam association without including mocks', () => {
    expect(parityJson.totals.subjects).toBe(32);
    expect(parityJson.totals.subjectsWithExactCrosswalks).toBe(32);
    expect(parityJson.totals.unreviewed).toBe(0);
    expect(parityJson.totals.referenceOfficialAssociations).toBe(
      parityJson.totals.matched + parityJson.totals.sourceBlocked + parityJson.totals.referenceAnomaly,
    );

    for (const subject of parityJson.subjects) {
      expect(subject.crosswalkFile, subject.subjectId).toBeTruthy();
      expect(subject.totals.unreviewed, subject.subjectId).toBe(0);
      for (const topic of subject.topics) {
        expect(
          topic.gaps.filter(gap => /\bmock\b/i.test(gap.heading)),
          `${subject.subjectId}|${topic.id}`,
        ).toEqual([]);
      }
    }
  });

  it('resolves every matched StudyClix heading to its official NextStepUni paper card and live-course topic', () => {
    const failures: string[] = [];
    const pinnedStillDiffering = new Set<string>();
    const modelDiffering: Record<string, string[]> = {};

    for (const subject of parityJson.subjects) {
      if (!subject.crosswalkFile) continue;
      const crosswalk = JSON.parse(
        fs.readFileSync(path.join(ROOT, subject.crosswalkFile), 'utf8'),
      ) as Crosswalk;

      for (const association of crosswalk.associations ?? []) {
        if (association.resolution !== 'matched') continue;
        const targets = association.targets ?? (association.target ? [association.target] : []);
        if (!targets.length) {
          failures.push(`${crosswalk.subjectId}|${association.topicId}|${association.heading}: no target`);
          continue;
        }

        for (const target of targets) {
          const year = associationYear(association, target);
          const numbers = targetQuestionNumbers(target);
          if (!year || !numbers.length) {
            failures.push(`${crosswalk.subjectId}|${association.topicId}|${association.heading}: incomplete target`);
            continue;
          }

          // A year can hold two entries, June's and the deferred sitting's
          // (listed after it): the target's own file id picks the paper.
          const indexedPaper = (PAPER_TRAIL_INDEX[crosswalk.subjectId] ?? [])
            .filter(entry => entry.year === year && entry.level === target.level && entry.lang === target.lang)
            .flatMap(entry => entry.papers)
            .find(paper => paper.doc.f === target.fileid);
          if (!indexedPaper) {
            failures.push(`${crosswalk.subjectId}|${association.topicId}|${association.heading}: unindexed ${target.fileid}`);
            continue;
          }

          const physicalNumbers = physicalCardNumbers(year, target.fileid);
          for (const number of numbers) {
            if (!physicalNumbers.has(number)) {
              failures.push(`${crosswalk.subjectId}|${association.topicId}|${association.heading}: absent ${target.fileid} Q${number}`);
            }
          }

          // Geography and PE already expose their 2028 replacement-course
          // menus. StudyClix retrospectively lists old-course questions there,
          // but NextStepUni deliberately keeps those papers on the outgoing
          // syllabus. Their physical-card existence is still checked above.
          const topic = examTopicDefinition(association.topicId);
          const isPreLaunchReplacementTopic = (
            (crosswalk.subjectId === 'geography' || crosswalk.subjectId === 'physical-education')
            && topic?.course === 'new'
            && year < 2028
          );
          if (isPreLaunchReplacementTopic) continue;

          const paper = topicsForPaper(
            crosswalk.subjectId,
            year,
            target.level,
            target.lang,
            target.fileid,
          );
          if (!paper) {
            failures.push(`${crosswalk.subjectId}|${association.topicId}|${association.heading}: missing ${target.fileid}`);
            continue;
          }

          for (const number of numbers) {
            const question = paper.q.find(candidate => candidate.n === number);
            if (!question) {
              failures.push(`${crosswalk.subjectId}|${association.topicId}|${association.heading}: missing ${target.fileid} Q${number}`);
              continue;
            }
            const topicIds = browseTopicIdsForQuestion(paper, question);
            const pinKey = `${crosswalk.subjectId}|${association.topicId}|${association.heading}|${target.fileid}|Q${number}`;
            if (isModelSubject(crosswalk.subjectId)) {
              const onList = (atlasHeadings(crosswalk.subjectId) ?? []).some(topic => topic.id === association.topicId);
              if (onList && !topicIds.includes(association.topicId)) (modelDiffering[crosswalk.subjectId] ??= []).push(pinKey);
              continue;
            }
            if (!topicIds.includes(association.topicId) && PINNED_MATHS_TOPIC_DIFFERENCES.has(pinKey)) {
              pinnedStillDiffering.add(pinKey);
              continue;
            }
            if (!topicIds.includes(association.topicId)) {
              failures.push(
                `${crosswalk.subjectId}|${association.topicId}|${association.heading}: ${target.fileid} Q${number} maps to ${topicIds.join(', ') || '(none)'}`,
              );
            }
          }
        }
      }
    }

    const failureCounts = Object.fromEntries(
      [...new Set(failures.map(failure => failure.split('|')[0]))]
        .sort()
        .map(subjectId => [subjectId, failures.filter(failure => failure.startsWith(`${subjectId}|`)).length]),
    );
    expect(failures.slice(0, 100), `${failures.length} failures: ${JSON.stringify(failureCounts)}`).toEqual([]);
    // Shrink-only: a pinned Maths difference that resolves leaves the list.
    expect(
      [...PINNED_MATHS_TOPIC_DIFFERENCES].filter(key => !pinnedStillDiffering.has(key)),
      'resolved: remove from test/fixtures/studyclixMathsTopicDifferences.json',
    ).toEqual([]);
    expect(PINNED_MATHS_TOPIC_DIFFERENCES.size).toBeLessThanOrEqual(174);

    const differing = Object.fromEntries(Object.entries(modelDiffering).map(([s, keys]) => [s, [...new Set(keys)].sort()]));
    if (process.env.STUDYCLIX_MODEL_DIFFERENCES_WRITE) {
      const grows = Object.entries(differing).flatMap(([s, keys]) => (s in modelPinned ? keys.filter(k => !modelPinned[s].includes(k)) : []));
      if (grows.length) throw new Error(`refusing to grow the model differences list: ${grows.slice(0, 5).join('; ')}`);
      fs.writeFileSync(MODEL_FIXTURE, `${JSON.stringify({
        note: 'Shrink-only (test/studyclixQuestionParity.test.ts). StudyClix headings, in a subject switched on in the single model, whose question the model files under other headings of the one list (each part by what it asks).',
        subjects: differing,
      }, null, 1)}\n`);
    }
    const newlyDiffering = Object.entries(differing).flatMap(([s, keys]) => keys.filter(k => !modelPinned[s]?.includes(k)));
    const resolved = Object.entries(modelPinned).flatMap(([s, keys]) => keys.filter(k => !differing[s]?.includes(k)));
    expect(newlyDiffering.slice(0, 50), `${newlyDiffering.length} StudyClix headings newly filed elsewhere in a model subject`).toEqual([]);
    expect(resolved.slice(0, 50), 'resolved: rewrite test/fixtures/studyclixModelTopicDifferences.json (STUDYCLIX_MODEL_DIFFERENCES_WRITE=1)').toEqual([]);
  });

  it('has no heading left under the generic local-paper/card-missing state', () => {
    const failures: string[] = [];
    for (const subject of parityJson.subjects) {
      if (!subject.crosswalkFile) continue;
      const crosswalk = JSON.parse(
        fs.readFileSync(path.join(ROOT, subject.crosswalkFile), 'utf8'),
      ) as Crosswalk;
      for (const association of crosswalk.associations ?? []) {
        if (association.resolution === 'source-blocked' && association.reason === 'local-paper-or-card-missing') {
          failures.push(`${crosswalk.subjectId}|${association.topicId}|${association.heading}`);
        }
      }
    }
    expect(failures).toEqual([]);
  });
});
