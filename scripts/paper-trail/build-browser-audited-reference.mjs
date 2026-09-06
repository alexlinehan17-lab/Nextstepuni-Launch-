#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Import a completed metadata-only StudyClix topic sweep. Browser checkpoints
 * contain factual hierarchy, displayed counts, source classifications and
 * official question headings only. They never contain question text, answers,
 * notes, images, audio, video or provider-hosted documents.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const SNAPSHOT_PATH = path.join(ROOT, 'data/examTopics/studyclix-subject-taxonomy.json');

const SUBJECTS = {
  english: {
    outputFile: 'english.json',
    subjectId: 'english',
  },
  geography: {
    outputFile: 'geography.json',
    subjectId: 'geography',
  },
  'home-economics': {
    outputFile: 'home-economics.json',
    subjectId: 'home-economics-s-and-s',
  },
  mathematics: {
    outputFile: 'mathematics.json',
    subjectId: 'mathematics',
  },
  'physical-education': {
    outputFile: 'physical-education.json',
    subjectId: 'physical-education',
  },
};

const referenceSlug = process.argv[2];
const config = SUBJECTS[referenceSlug];
if (!config) {
  throw new Error(`Usage: build-browser-audited-reference.mjs ${Object.keys(SUBJECTS).join('|')}`);
}

const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const displayLabelForVariant = (variant, hasCourseTransition) => {
  const level = variant.startsWith('higher')
    ? 'Higher Level'
    : variant.startsWith('foundation')
      ? 'Foundation Level'
      : 'Ordinary Level';
  if (!hasCourseTransition) return level;
  return `${level} · ${variant.endsWith('new-course') ? 'New Course' : 'Outgoing Course'}`;
};
const snapshot = readJson(SNAPSHOT_PATH);
const checkpointPath = `/private/tmp/nextstepuni-${referenceSlug}-audit-progress.json`;
if (!fs.existsSync(checkpointPath)) {
  throw new Error(`Missing browser audit checkpoint: ${checkpointPath}`);
}
const checkpoint = readJson(checkpointPath);
const captured = checkpoint.audit ?? checkpoint;
const sourceVariants = snapshot.variants.filter(variant => variant.subjectSlug === referenceSlug);
const sourceTopics = sourceVariants.flatMap(variant => variant.topics);
const hasCourseTransition = sourceVariants.some(variant => variant.variant.endsWith('new-course'));

if (!sourceVariants.length) throw new Error(`No hierarchy snapshot for ${referenceSlug}`);
if (checkpoint.captured !== sourceTopics.length || checkpoint.total !== sourceTopics.length) {
  throw new Error(
    `${referenceSlug} browser audit is incomplete: ${checkpoint.captured}/${checkpoint.total}; expected ${sourceTopics.length}`,
  );
}
if (Object.keys(captured).length !== sourceTopics.length) {
  throw new Error(`${referenceSlug}: duplicate or missing captured topic paths`);
}

const totals = {
  reported: 0,
  state: 0,
  mock: 0,
  providerSample: 0,
  sourceLabelConflicts: 0,
  sourceUnavailableTopics: 0,
};
const variants = {};
for (const sourceVariant of sourceVariants) {
  const topics = sourceVariant.topics.map(sourceTopic => {
    const audit = captured[sourceTopic.sourcePath];
    if (!audit) throw new Error(`Missing ${sourceTopic.sourcePath}`);
    if (
      audit.variant !== sourceVariant.variant
      || audit.label !== sourceTopic.label
      || audit.groupId !== (sourceTopic.groupId ?? null)
      || (!audit.sourceUnavailable && audit.pageTitle && audit.pageTitle !== sourceTopic.label)
    ) {
      throw new Error(`${sourceTopic.sourcePath}: hierarchy/capture mismatch`);
    }
    if (audit.sourceUnavailable) {
      totals.sourceUnavailableTopics += 1;
      return {
        id: `${config.subjectId}-${sourceVariant.variant}-${sourceTopic.id}`,
        label: sourceTopic.label,
        groupId: sourceTopic.groupId ?? null,
        sourcePath: sourceTopic.sourcePath,
        reportedQuestionCount: 0,
        officialQuestionHeadings: [],
        mockQuestionCount: 0,
        providerSampleQuestionCount: 0,
        extractedQuestionCount: 0,
        sourceLabelConflictCount: 0,
        sourceUnavailable: audit.sourceUnavailable,
      };
    }
    if (audit.countMismatch || audit.unknownQuestionHeadings.length) {
      throw new Error(`${sourceTopic.sourcePath}: unresolved browser audit row`);
    }
    const extractedQuestionCount = audit.officialQuestionHeadings.length
      + audit.mockQuestionCount
      + audit.providerSampleQuestionCount;
    if (audit.reportedQuestionCount !== extractedQuestionCount) {
      throw new Error(`${sourceTopic.sourcePath}: displayed count does not reconcile`);
    }
    totals.reported += audit.reportedQuestionCount;
    totals.state += audit.officialQuestionHeadings.length;
    totals.mock += audit.mockQuestionCount;
    totals.providerSample += audit.providerSampleQuestionCount;
    totals.sourceLabelConflicts += audit.sourceLabelConflictCount ?? 0;
    return {
      id: `${config.subjectId}-${sourceVariant.variant}-${sourceTopic.id}`,
      label: sourceTopic.label,
      groupId: sourceTopic.groupId ?? null,
      sourcePath: sourceTopic.sourcePath,
      reportedQuestionCount: audit.reportedQuestionCount,
      officialQuestionHeadings: audit.officialQuestionHeadings,
      mockQuestionCount: audit.mockQuestionCount,
      providerSampleQuestionCount: audit.providerSampleQuestionCount,
      extractedQuestionCount,
      sourceLabelConflictCount: audit.sourceLabelConflictCount ?? 0,
    };
  });
  variants[sourceVariant.variant] = {
    label: displayLabelForVariant(sourceVariant.variant, hasCourseTransition),
    sourcePath: sourceVariant.sourcePath,
    groups: sourceVariant.groups.map(group => ({
      id: `${config.subjectId}-${sourceVariant.variant}-${group.id}`,
      label: group.label,
      topicIds: group.topicIds.map(topicId => (
        `${config.subjectId}-${sourceVariant.variant}-${topicId}`
      )),
    })),
    topics,
  };
}

const output = {
  schemaVersion: 1,
  subjectId: config.subjectId,
  referenceSlug,
  reference: {
    provider: 'StudyClix',
    scope: 'Factual topic labels, hierarchy, displayed counts and official question headings only.',
    excludedContent: 'Question text, solutions, notes, videos, images, audio and PDFs were not copied.',
    providerSamplePolicy: 'Provider-authored samples are counted only and excluded from NextStepUni mappings.',
    sourceLabelConflictPolicy: 'A title containing Mock is excluded even when its displayed source badge conflicts.',
  },
  capturedAt: checkpoint.capturedAt ?? '2026-09-05',
  totals,
  variants,
};
const outputPath = path.join(ROOT, 'data/examTopics', config.outputFile);
fs.writeFileSync(outputPath, `${JSON.stringify(output, null, 2)}\n`);
console.log(JSON.stringify({
  output: path.relative(ROOT, outputPath),
  variants: sourceVariants.length,
  groups: sourceVariants.reduce((sum, variant) => sum + variant.groups.length, 0),
  topics: sourceTopics.length,
  totals,
}, null, 2));
