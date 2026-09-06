#!/usr/bin/env node
/**
 * Import the completed, metadata-only StudyClix Physics audit.
 *
 * The browser capture deliberately contains only factual headings, hierarchy,
 * counts, and source classifications. It never stores question text, answers,
 * notes, media, or PDFs. The finished JSON is the durable audit record; the
 * temporary checkpoint is only the hand-off from the authenticated browser.
 *
 * Use --freeze-baseline exactly once, before changing physics topic tags, to
 * preserve every pre-migration Paper Trail card identity.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const SNAPSHOT_PATH = path.join(
  ROOT, 'data/examTopics/studyclix-subject-taxonomy.json',
);
const CHECKPOINT_PATH = '/private/tmp/nextstepuni-physics-audit-progress.json';
const OUTPUT_PATH = path.join(ROOT, 'data/examTopics/physics.json');
const TAGS_PATH = path.join(HERE, 'topic-tags/tags/physics.json');
const BASELINE_PATH = path.join(
  ROOT, 'test/fixtures/physicsTopicQuestionBaseline.json',
);

const EXPECTED_VARIANTS = {
  'higher-new-course': 25,
  'higher-old-course': 34,
  'ordinary-new-course': 28,
  'ordinary-old-course': 26,
};
const EXPECTED_TOTALS = {
  reported: 4701,
  state: 2482,
  mock: 2051,
  providerSample: 168,
};
const VARIANT_LABELS = {
  'higher-new-course': 'Higher Level · New Course',
  'higher-old-course': 'Higher Level · Old Course',
  'ordinary-new-course': 'Ordinary Level · New Course',
  'ordinary-old-course': 'Ordinary Level · Old Course',
};

const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const snapshot = readJson(SNAPSHOT_PATH);
if (!fs.existsSync(CHECKPOINT_PATH)) {
  throw new Error(`Missing browser audit checkpoint: ${CHECKPOINT_PATH}`);
}
const captured = readJson(CHECKPOINT_PATH);
const sourceVariants = snapshot.variants.filter(
  variant => variant.subjectSlug === 'physics',
);

if (sourceVariants.length !== 4) {
  throw new Error(`Expected 4 Physics variants, found ${sourceVariants.length}`);
}

const allSourceTopics = sourceVariants.flatMap(variant => variant.topics);
if (allSourceTopics.length !== 113 || Object.keys(captured).length !== 113) {
  throw new Error(
    `Physics audit must contain 113 topics; hierarchy=${allSourceTopics.length}, capture=${Object.keys(captured).length}`,
  );
}

const totals = { reported: 0, state: 0, mock: 0, providerSample: 0 };
const variants = {};
for (const sourceVariant of sourceVariants) {
  const variant = sourceVariant.variant;
  if (!(variant in EXPECTED_VARIANTS)) {
    throw new Error(`Unexpected Physics variant: ${variant}`);
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
      id: `physics-${variant}-${sourceTopic.id}`,
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
      id: `physics-${variant}-${group.id}`,
      label: group.label,
      topicIds: group.topicIds.map(topicId => `physics-${variant}-${topicId}`),
    })),
    topics,
  };
}

if (JSON.stringify(totals) !== JSON.stringify(EXPECTED_TOTALS)) {
  throw new Error(
    `Physics aggregate mismatch: ${JSON.stringify(totals)} !== ${JSON.stringify(EXPECTED_TOTALS)}`,
  );
}

const output = {
  schemaVersion: 1,
  subjectId: 'physics',
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
      throw new Error('Refusing to replace the established Physics preservation baseline');
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
