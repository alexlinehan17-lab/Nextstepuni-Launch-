#!/usr/bin/env node
/**
 * Import the completed, metadata-only StudyClix Construction Studies audit.
 *
 * The browser checkpoint contains factual headings, hierarchy, counts, and
 * source classifications only. It contains no question text, solutions,
 * notes, media, or PDFs.
 *
 * Use --freeze-baseline exactly once, before changing Construction Studies
 * topic tags, to preserve every pre-migration Paper Trail card identity.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const SNAPSHOT_PATH = path.join(ROOT, 'data/examTopics/studyclix-subject-taxonomy.json');
const CHECKPOINT_PATH = '/private/tmp/nextstepuni-construction-studies-audit-progress.json';
const OUTPUT_PATH = path.join(ROOT, 'data/examTopics/construction-studies.json');
const TAGS_PATH = path.join(HERE, 'topic-tags/tags/construction-studies.json');
const BASELINE_PATH = path.join(ROOT, 'test/fixtures/constructionStudiesTopicQuestionBaseline.json');

const EXPECTED_VARIANTS = {
  higher: 23,
  ordinary: 16,
  'higher-new-course': 32,
  'ordinary-new-course': 32,
};
const EXPECTED_TOTALS = {
  reported: 2336,
  state: 1396,
  mock: 940,
  providerSample: 0,
};
const VARIANT_LABELS = {
  higher: 'Higher Level · Outgoing Course',
  ordinary: 'Ordinary Level · Outgoing Course',
  'higher-new-course': 'Higher Level · New Course',
  'ordinary-new-course': 'Ordinary Level · New Course',
};

const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const snapshot = readJson(SNAPSHOT_PATH);
if (!fs.existsSync(CHECKPOINT_PATH)) {
  throw new Error(`Missing browser audit checkpoint: ${CHECKPOINT_PATH}`);
}
const captured = readJson(CHECKPOINT_PATH);
const sourceVariants = snapshot.variants.filter(
  variant => variant.subjectSlug === 'construction-studies',
);

if (sourceVariants.length !== 4) {
  throw new Error(`Expected 4 Construction Studies variants, found ${sourceVariants.length}`);
}

const allSourceTopics = sourceVariants.flatMap(variant => variant.topics);
if (allSourceTopics.length !== 103 || Object.keys(captured).length !== 103) {
  throw new Error(
    `Construction Studies audit must contain 103 topics; hierarchy=${allSourceTopics.length}, capture=${Object.keys(captured).length}`,
  );
}

const totals = { reported: 0, state: 0, mock: 0, providerSample: 0 };
const variants = {};
for (const sourceVariant of sourceVariants) {
  const variant = sourceVariant.variant;
  if (!(variant in EXPECTED_VARIANTS)) {
    throw new Error(`Unexpected Construction Studies variant: ${variant}`);
  }
  if (sourceVariant.topics.length !== EXPECTED_VARIANTS[variant]) {
    throw new Error(
      `${variant}: expected ${EXPECTED_VARIANTS[variant]} topics, found ${sourceVariant.topics.length}`,
    );
  }

  const topics = sourceVariant.topics.map(sourceTopic => {
    const audit = captured[sourceTopic.sourcePath];
    if (!audit) throw new Error(`${variant}: missing ${sourceTopic.sourcePath}`);
    if (audit.variant !== variant || audit.label !== sourceTopic.label) {
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
      id: `construction-studies-${variant}-${sourceTopic.id}`,
      label: sourceTopic.label,
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
    groups: sourceVariant.groups.map(group => ({
      id: `construction-studies-${variant}-${group.id}`,
      label: group.label,
      topicIds: group.topicIds.map(
        topicId => `construction-studies-${variant}-${topicId}`,
      ),
    })),
    topics,
  };
}

if (JSON.stringify(totals) !== JSON.stringify(EXPECTED_TOTALS)) {
  throw new Error(
    `Construction Studies aggregate mismatch: ${JSON.stringify(totals)} !== ${JSON.stringify(EXPECTED_TOTALS)}`,
  );
}

const output = {
  schemaVersion: 1,
  subjectId: 'construction-studies',
  reference: {
    provider: 'StudyClix',
    scope: 'Factual topic labels, hierarchy, reported counts, and source classification only.',
    excludedContent: 'Question text, solutions, notes, videos, images, and PDFs were not copied.',
    providerSamplePolicy: 'StudyClix Sample Exams are counted for reconciliation only and are excluded from NextStepUni question mappings.',
  },
  capturedAt: '2026-09-04',
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
    questions: paper.q.map(question => question.n),
  }));
  if (fs.existsSync(BASELINE_PATH)) {
    const existing = readJson(BASELINE_PATH);
    if (JSON.stringify(existing) !== JSON.stringify(baseline)) {
      throw new Error('Refusing to replace the established Construction Studies preservation baseline');
    }
  } else {
    fs.writeFileSync(BASELINE_PATH, `${JSON.stringify(baseline, null, 2)}\n`);
  }
}

console.log(JSON.stringify({
  output: path.relative(ROOT, OUTPUT_PATH),
  topics: allSourceTopics.length,
  groups: sourceVariants.reduce((sum, variant) => sum + variant.groups.length, 0),
  totals,
  baselineFrozen: process.argv.includes('--freeze-baseline'),
}, null, 2));
