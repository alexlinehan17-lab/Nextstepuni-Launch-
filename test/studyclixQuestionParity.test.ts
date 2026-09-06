/** @license SPDX-License-Identifier: Apache-2.0 */

import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { browseTopicIdsForQuestion, topicsForPaper } from '../components/PaperTrail/topics';
import parityJson from '../data/examTopics/studyclix-question-parity.json';
import { examTopicDefinition } from '../data/examTopics/registry';
import { PAPER_TRAIL_INDEX } from '../paperTrailData';
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

          const indexedPaper = (PAPER_TRAIL_INDEX[crosswalk.subjectId] ?? [])
            .find(entry => entry.year === year && entry.level === target.level && entry.lang === target.lang)
            ?.papers.find(paper => paper.doc.f === target.fileid);
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
