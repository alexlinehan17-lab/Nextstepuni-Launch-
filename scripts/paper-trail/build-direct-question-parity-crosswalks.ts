/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Build exact StudyClix-heading → entitled SEC-card evidence for the six
 * subjects whose factual headings are already parsed directly in registry.ts.
 * Mock questions are not inputs. A heading is matched only when every printed
 * task represented by it exists in an answer-anchored local paper.
 */

import fs from 'node:fs';
import path from 'node:path';
import { PAPER_TRAIL_INDEX } from '../../paperTrailData';
import { paperKeyOf } from '../../components/PaperTrail/topics';
import {
  examQuestionPartReferencesForSubject,
  examTopicTaxonomyFor,
  type ExamQuestionPartReference,
} from '../../data/examTopics/registry';

const ROOT = path.resolve(process.cwd());
const DATA = path.join(ROOT, 'data/examTopics');

const SUBJECT_FILES = [
  ['accounting', 'accounting'],
  ['agricultural-science', 'agricultural-science'],
  ['applied-mathematics', 'applied-mathematics'],
  ['classical-studies', 'classical-studies'],
  ['link-modules', 'link-modules'],
  ['politics-and-society', 'politics-and-society'],
] as const;

type ReferenceTopic = {
  id: string;
  label: string;
  officialQuestionHeadings?: string[];
  officialQuestions?: string[];
};

type LocalTarget = {
  level: string;
  lang: string;
  year: number;
  paperKey: string;
  fileid: string;
  n: string;
};

type DirectRuntimeSubject = {
  subjectId: string;
  topicIds: string[];
  questionMappings: Array<[
    level: string,
    lang: string,
    year: number,
    paperKey: string,
    fileid: string,
    n: string,
    topicIndexes: number[],
  ]>;
};

const readJson = (file: string) => JSON.parse(fs.readFileSync(file, 'utf8')) as unknown;
const writeJson = (file: string, value: unknown) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);

const referenceTopics = (root: unknown): ReferenceTopic[] => {
  const topics: ReferenceTopic[] = [];
  const seen = new Set<string>();
  const visit = (value: unknown) => {
    if (!value || typeof value !== 'object') return;
    if (!Array.isArray(value)) {
      const record = value as Record<string, unknown>;
      const hasOfficial = Array.isArray(record.officialQuestionHeadings) || Array.isArray(record.officialQuestions);
      if (typeof record.id === 'string' && typeof record.label === 'string' && hasOfficial) {
        if (seen.has(record.id)) throw new Error(`Duplicate reference topic: ${record.id}`);
        seen.add(record.id);
        topics.push(record as ReferenceTopic);
        return;
      }
    }
    for (const child of Array.isArray(value) ? value : Object.values(value)) visit(child);
  };
  visit(root);
  return topics;
};

const localTargetsFor = (subjectId: string) => {
  const byQuestion = new Map<string, LocalTarget[]>();
  let paperVariants = 0;
  let physicalMappings = 0;
  const logical = new Set<string>();

  for (const entry of PAPER_TRAIL_INDEX[subjectId] ?? []) {
    for (const paper of entry.papers) {
      if (paper.answers !== 1) continue;
      // Read the QA-passed answer sidecar directly. Deriving local card
      // existence from topicsForPaper() would create a circular dependency:
      // runtime supplementation itself consumes the crosswalk this builder
      // writes, so one partial build could progressively erase valid cards.
      const sidecarFile = path.join(
        ROOT,
        'scripts/paper-trail/answers',
        String(entry.year),
        `${paper.doc.f}.json`,
      );
      if (!fs.existsSync(sidecarFile)) {
        throw new Error(`${subjectId}: answers:1 without sidecar ${sidecarFile}`);
      }
      const sidecar = readJson(sidecarFile) as { q?: Array<{ n: string | number }> };
      const questions = sidecar.q ?? [];
      if (!questions.length) throw new Error(`${subjectId}: empty answer sidecar ${sidecarFile}`);
      paperVariants += 1;
      physicalMappings += questions.length;
      const paperKey = paperKeyOf(paper.label);
      for (const question of questions) {
        const number = String(question.n);
        const target: LocalTarget = {
          level: entry.level,
          lang: entry.lang,
          year: entry.year,
          paperKey,
          fileid: paper.doc.f,
          n: number,
        };
        const key = `${entry.level}|${entry.year}|${paperKey}|${number}`;
        const targets = byQuestion.get(key) ?? [];
        targets.push(target);
        byQuestion.set(key, targets);
        logical.add(key);
      }
    }
  }
  return { byQuestion, paperVariants, physicalMappings, logicalQuestions: logical.size };
};

const representativeTarget = (targets: LocalTarget[]) =>
  [...targets].sort((a, b) => a.lang.localeCompare(b.lang) || a.fileid.localeCompare(b.fileid))[0];

const referenceSubdivision = (subjectId: string, heading: string, level: string) => {
  const question = heading.match(/Question\s+([A-Z]|\d+)/i);
  if (subjectId === 'link-modules' || subjectId === 'politics-and-society') {
    return heading.replace(/^\d{4}\s*-\s*/, '').trim();
  }
  if (!question) throw new Error(`${subjectId}: unparseable reference heading ${heading}`);
  if (subjectId === 'classical-studies') {
    return heading.slice((question.index ?? 0) + question[0].length)
      .replace(/^\s*-\s*/, '')
      .trim();
  }
  const beforeQuestion = heading.slice(4, question.index)
    .replace(/(?:Sample Paper|Deferred Exam Paper|Paper)/gi, '')
    .replace(/^\s*-\s*|\s*-\s*$/g, '')
    .trim();
  const afterQuestion = heading.slice((question.index ?? 0) + question[0].length)
    .replace(/^\s*-\s*/, '')
    .trim();
  if (subjectId === 'agricultural-science' && level === 'higher' && /^[A-Z]$/i.test(question[1])) {
    return [beforeQuestion, `Short question ${question[1].toUpperCase()}`, afterQuestion]
      .filter(Boolean)
      .join(' · ');
  }
  return [beforeQuestion, afterQuestion].filter(Boolean).join(' · ');
};

const referenceYearAndSitting = (heading: string) => ({
  year: Number(heading.match(/^(\d{4})/)?.[1]),
  sitting: /Sample Paper/i.test(heading)
    ? 'sample'
    : /Deferred Exam Paper/i.test(heading)
      ? 'deferred'
      : 'main',
});

const singleQuestionNumber = (subjectId: string, heading: string, level: string) => {
  if (subjectId === 'link-modules' || subjectId === 'politics-and-society') return '';
  const printed = heading.match(/Question\s+([A-Z]|\d+)/i)?.[1];
  if (!printed) throw new Error(`${subjectId}: missing question number in ${heading}`);
  return subjectId === 'agricultural-science' && level === 'higher' && /^[A-Z]$/i.test(printed)
    ? '1'
    : printed;
};

const blockReason = (references: ExamQuestionPartReference[], earliestLocalYear: number) => {
  if (references.some(reference => reference.sitting === 'sample')) return 'official-sample-paper-not-in-local-corpus';
  if (references.some(reference => reference.sitting === 'deferred')) return 'deferred-sitting-not-in-local-corpus';
  if (references.some(reference => reference.year < earliestLocalYear)) return 'before-local-corpus';
  return 'local-paper-or-card-missing';
};

const runtimeSubjects: DirectRuntimeSubject[] = [];

for (const [subjectId, fileStem] of SUBJECT_FILES) {
  const reference = readJson(path.join(DATA, `${fileStem}.json`));
  const topics = referenceTopics(reference);
  const taxonomy = examTopicTaxonomyFor(subjectId);
  if (!taxonomy) throw new Error(`${subjectId}: missing runtime taxonomy`);
  const topicLevel = new Map(taxonomy.topics.map(topic => [topic.id, topic.level]));
  const partReferences = examQuestionPartReferencesForSubject(subjectId);
  const partsByHeading = new Map<string, ExamQuestionPartReference[]>();
  for (const referencePart of partReferences) {
    const key = [
      referencePart.topicId,
      referencePart.year,
      referencePart.sitting,
      referencePart.subdivision ?? '',
      singleQuestionNumber(subjectId, `Question ${referencePart.n}`, referencePart.level),
    ].join('\u0000');
    const parts = partsByHeading.get(key) ?? [];
    parts.push(referencePart);
    partsByHeading.set(key, parts);
  }
  const local = localTargetsFor(subjectId);
  const earliestLocalYear = Math.min(
    ...[...(PAPER_TRAIL_INDEX[subjectId] ?? [])].map(entry => entry.year),
  );
  const exactRuntimeTopics = new Map<string, Set<string>>();

  const associations = [];
  for (const topic of topics) {
    const headings = topic.officialQuestionHeadings ?? topic.officialQuestions ?? [];
    for (const heading of headings) {
      let parts: ExamQuestionPartReference[];
      if (subjectId === 'accounting') {
        const [year, sitting, n] = heading.split('|');
        parts = [{
          subjectId,
          level: topicLevel.get(topic.id)!,
          year: Number(year),
          sitting: sitting as ExamQuestionPartReference['sitting'],
          paperKey: 'single',
          n,
          subdivision: heading,
          topicId: topic.id,
        }];
      } else {
        const subdivision = referenceSubdivision(subjectId, heading, topicLevel.get(topic.id)!);
        const identity = referenceYearAndSitting(heading);
        parts = partsByHeading.get([
          topic.id,
          identity.year,
          identity.sitting,
          subdivision,
          singleQuestionNumber(subjectId, heading, topicLevel.get(topic.id)!),
        ].join('\u0000')) ?? [];
      }
      if (!parts.length) throw new Error(`${subjectId}: no parsed parts for ${topic.id} | ${heading}`);

      const partResults = parts.map(part => {
        if (part.sitting !== 'main') return { part, target: null };
        const key = `${part.level}|${part.year}|${part.paperKey}|${part.n}`;
        const candidates = local.byQuestion.get(key) ?? [];
        return { part, target: candidates.length ? representativeTarget(candidates) : null };
      });
      const complete = partResults.every(result => result.target);
      if (complete) {
        for (const part of parts) {
          const key = `${part.level}|${part.year}|${part.paperKey}|${part.n}`;
          for (const target of local.byQuestion.get(key) ?? []) {
            const exactKey = [
              target.level,
              target.lang,
              target.year,
              target.paperKey,
              target.fileid,
              target.n,
            ].join('\u0000');
            const topicIds = exactRuntimeTopics.get(exactKey) ?? new Set<string>();
            topicIds.add(topic.id);
            exactRuntimeTopics.set(exactKey, topicIds);
          }
        }
      }
      const targets = [...new Map(
        partResults
          .filter((result): result is typeof result & { target: LocalTarget } => Boolean(result.target))
          .map(result => [`${result.target.level}|${result.target.year}|${result.target.paperKey}|${result.target.n}`, result.target]),
      ).values()];
      associations.push({
        topicId: topic.id,
        heading,
        resolution: complete ? 'matched' : 'source-blocked',
        ...(complete ? { targets } : {
          reason: blockReason(parts, earliestLocalYear),
          missingParts: partResults.filter(result => !result.target).map(result => ({
            level: result.part.level,
            year: result.part.year,
            sitting: result.part.sitting,
            paperKey: result.part.paperKey,
            n: result.part.n,
          })),
          ...(targets.length ? { matchedTargets: targets } : {}),
        }),
      });
    }
  }

  const matched = associations.filter(association => association.resolution === 'matched');
  const blocked = associations.filter(association => association.resolution === 'source-blocked');
  const sourceBlockedByReason = Object.fromEntries(
    [...new Set(blocked.map(association => association.reason!))]
      .sort()
      .map(reason => [reason, blocked.filter(association => association.reason === reason).length]),
  );
  const matchedLocalCardLinks = matched.reduce((sum, association) => sum + association.targets!.length, 0);

  const output = {
    schemaVersion: 1,
    subjectId,
    generatedAt: new Date().toISOString(),
    status: blocked.length ? 'exact-current-corpus-mapped-source-completion-pending' : 'complete',
    summary: {
      referenceTopics: topics.length,
      referenceOfficialAssociations: associations.length,
      matchedAssociations: matched.length,
      sourceBlockedAssociations: blocked.length,
      sourceBlockedByReason,
      matchedLocalCardLinks,
      localPaperVariants: local.paperVariants,
      localPhysicalMappings: local.physicalMappings,
      distinctStudentFacingQuestions: local.logicalQuestions,
    },
    policy: {
      matchedSource: 'Entitled local State Examinations Commission corpus only.',
      excludedContent: 'No commercial mock question, solution, note, question text, image, media or provider-hosted PDF is copied.',
      completion: 'A reference heading is matched only when every represented printed task exists in an answer-anchored local paper.',
    },
    associations,
  };
  writeJson(path.join(DATA, `${subjectId}-local-crosswalk.json`), output);
  const runtimeTopicIds = taxonomy.topics.map(topic => topic.id);
  const runtimeTopicIndex = new Map(runtimeTopicIds.map((topicId, index) => [topicId, index]));
  runtimeSubjects.push({
    subjectId,
    topicIds: runtimeTopicIds,
    questionMappings: [...exactRuntimeTopics]
      .map(([key, topicIds]) => {
        const [level, lang, year, paperKey, fileid, n] = key.split('\u0000');
        return [
          level,
          lang,
          Number(year),
          paperKey,
          fileid,
          n,
          [...topicIds].map(topicId => runtimeTopicIndex.get(topicId)!),
        ] as DirectRuntimeSubject['questionMappings'][number];
      })
      .sort((a, b) => b[2] - a[2] || a[0].localeCompare(b[0]) || a[4].localeCompare(b[4]) || Number(a[5]) - Number(b[5])),
  });
  console.log(`${subjectId}: ${matched.length}/${associations.length} matched, ${blocked.length} source blocked`);
}

writeJson(path.join(DATA, 'direct-question-runtime.json'), {
  v: 1,
  subjects: runtimeSubjects,
});
