#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Import the completed metadata-only StudyClix German audit. The browser
 * checkpoint contains factual hierarchy, counts, source classifications and
 * official question headings only. It contains no question text, solutions,
 * notes, media or PDFs.
 *
 * Use --freeze-baseline exactly once before changing German topic tags.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const SNAPSHOT_PATH = path.join(ROOT, 'data/examTopics/studyclix-subject-taxonomy.json');
const CHECKPOINT_PATH = '/private/tmp/nextstepuni-german-audit-progress.json';
const OUTPUT_PATH = path.join(ROOT, 'data/examTopics/german.json');
const TAGS_PATH = path.join(HERE, 'topic-tags/tags/german.json');
const BASELINE_PATH = path.join(ROOT, 'test/fixtures/germanTopicQuestionBaseline.json');

const EXPECTED_VARIANTS = { higher: 10, ordinary: 15 };
const EXPECTED_GROUPS = { higher: 2, ordinary: 2 };
const EXPECTED_TOTALS = { reported: 820, state: 479, mock: 341, providerSample: 0 };
const VARIANT_LABELS = { higher: 'Higher Level', ordinary: 'Ordinary Level' };

const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const snapshot = readJson(SNAPSHOT_PATH);
if (!fs.existsSync(CHECKPOINT_PATH)) {
  throw new Error(`Missing browser audit checkpoint: ${CHECKPOINT_PATH}`);
}
const checkpoint = readJson(CHECKPOINT_PATH);
const captured = checkpoint.audit ?? checkpoint;
const sourceVariants = snapshot.variants.filter(variant => variant.subjectSlug === 'german');

if (sourceVariants.length !== 2) {
  throw new Error(`Expected 2 German variants, found ${sourceVariants.length}`);
}
if (checkpoint.audit && (checkpoint.index !== 25 || checkpoint.total !== 25)) {
  throw new Error(`German browser audit is incomplete: ${checkpoint.index}/${checkpoint.total}`);
}
const sourceTopics = sourceVariants.flatMap(variant => variant.topics);
if (sourceTopics.length !== 25 || Object.keys(captured).length !== 25) {
  throw new Error(
    `German audit must contain 25 topics; hierarchy=${sourceTopics.length}, capture=${Object.keys(captured).length}`,
  );
}

const totals = { reported: 0, state: 0, mock: 0, providerSample: 0 };
const variants = {};
for (const sourceVariant of sourceVariants) {
  const { variant } = sourceVariant;
  if (!(variant in EXPECTED_VARIANTS)) throw new Error(`Unexpected German variant: ${variant}`);
  if (sourceVariant.groups.length !== EXPECTED_GROUPS[variant]) {
    throw new Error(
      `${variant}: expected ${EXPECTED_GROUPS[variant]} groups, found ${sourceVariant.groups.length}`,
    );
  }
  if (sourceVariant.topics.length !== EXPECTED_VARIANTS[variant]) {
    throw new Error(
      `${variant}: expected ${EXPECTED_VARIANTS[variant]} topics, found ${sourceVariant.topics.length}`,
    );
  }

  const topics = sourceVariant.topics.map(sourceTopic => {
    const audit = captured[sourceTopic.sourcePath];
    if (!audit) throw new Error(`${variant}: missing ${sourceTopic.sourcePath}`);
    if (
      audit.variant !== variant
      || audit.label !== sourceTopic.label
      || audit.groupId !== (sourceTopic.groupId ?? null)
    ) {
      throw new Error(`${sourceTopic.sourcePath}: hierarchy/capture mismatch`);
    }
    if (audit.countMismatch || audit.unknownQuestionHeadings.length) {
      throw new Error(`${sourceTopic.sourcePath}: unresolved audit row`);
    }
    const extractedQuestionCount = audit.officialQuestionHeadings.length
      + audit.mockQuestionCount
      + audit.providerSampleQuestionCount;
    if (audit.reportedQuestionCount !== extractedQuestionCount) {
      throw new Error(`${sourceTopic.sourcePath}: reported count does not reconcile`);
    }
    totals.reported += audit.reportedQuestionCount;
    totals.state += audit.officialQuestionHeadings.length;
    totals.mock += audit.mockQuestionCount;
    totals.providerSample += audit.providerSampleQuestionCount;
    return {
      id: `german-${variant}-${sourceTopic.id}`,
      label: sourceTopic.label,
      groupId: sourceTopic.groupId,
      sourcePath: sourceTopic.sourcePath,
      reportedQuestionCount: audit.reportedQuestionCount,
      officialQuestionHeadings: audit.officialQuestionHeadings,
      mockQuestionCount: audit.mockQuestionCount,
      providerSampleQuestionCount: audit.providerSampleQuestionCount,
      extractedQuestionCount,
    };
  });

  variants[variant] = {
    label: VARIANT_LABELS[variant],
    sourcePath: sourceVariant.sourcePath,
    groups: sourceVariant.groups,
    topics,
  };
}

if (JSON.stringify(totals) !== JSON.stringify(EXPECTED_TOTALS)) {
  throw new Error(
    `German aggregate mismatch: ${JSON.stringify(totals)} !== ${JSON.stringify(EXPECTED_TOTALS)}`,
  );
}

const output = {
  schemaVersion: 1,
  subjectId: 'german',
  reference: {
    provider: 'StudyClix',
    scope: 'Factual topic labels, hierarchy, reported counts and official question headings only.',
    excludedContent: 'Question text, solutions, notes, videos, images and PDFs were not copied.',
    providerSamplePolicy: 'Provider-authored samples are counted only and excluded from NextStepUni mappings.',
  },
  capturedAt: '2026-09-05',
  variants,
};
fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify(output, null, 2)}\n`);

if (process.argv.includes('--freeze-baseline')) {
  const tags = readJson(TAGS_PATH);
  const baseline = tags.map(paper => ({
    level: paper.level,
    lang: paper.lang,
    year: paper.year,
    fileid: paper.fileid,
    paperKey: paper.paperKey,
    questions: paper.q.map(question => ({
      n: question.n,
      primary: question.primary,
      ...(question.secondary ? { secondary: question.secondary } : {}),
    })),
  }));
  if (fs.existsSync(BASELINE_PATH)) {
    const existing = readJson(BASELINE_PATH);
    if (JSON.stringify(existing) !== JSON.stringify(baseline)) {
      throw new Error('Refusing to replace the established German preservation baseline');
    }
  } else {
    fs.writeFileSync(BASELINE_PATH, `${JSON.stringify(baseline, null, 2)}\n`);
  }
}

console.log(JSON.stringify({
  output: path.relative(ROOT, OUTPUT_PATH),
  groups: sourceVariants.reduce((sum, variant) => sum + variant.groups.length, 0),
  topics: sourceTopics.length,
  totals,
  baselineFrozen: process.argv.includes('--freeze-baseline'),
}, null, 2));
