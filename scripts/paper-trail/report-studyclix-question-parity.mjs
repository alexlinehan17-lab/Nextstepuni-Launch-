#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Build the question-by-question StudyClix parity ledger.
 *
 * The browser-audited reference files contain factual State-exam headings and
 * topic membership only. Subject crosswalks record whether each heading has an
 * exact, entitled SEC-paper target in NextStepUni. Commercial mock questions
 * are deliberately excluded from this report.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const DATA = path.join(ROOT, 'data/examTopics');
const DOCS = path.join(ROOT, 'docs');

const SUBJECT_FILES = [
  'accounting',
  'agricultural-science',
  'applied-mathematics',
  'art',
  'biology',
  'business',
  'chemistry',
  'classical-studies',
  'computer-science',
  'construction-studies',
  'design-and-communication-graphics',
  'economics',
  'engineering',
  'english',
  'french',
  'geography',
  'german',
  'history',
  'home-economics',
  'irish',
  'italian',
  'japanese',
  'link-modules',
  'mathematics',
  'music',
  'physical-education',
  'physics',
  'physics-and-chemistry',
  'politics-and-society',
  'religious-education',
  'spanish',
  'technology',
];

const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);

const topicRecords = root => {
  const topics = [];
  const seen = new Set();

  const visit = value => {
    if (!value || typeof value !== 'object') return;
    if (!Array.isArray(value)) {
      const official = Array.isArray(value.officialQuestionHeadings)
        ? value.officialQuestionHeadings
        : Array.isArray(value.officialQuestions)
          ? value.officialQuestions
          : null;
      if (typeof value.id === 'string' && typeof value.label === 'string' && official) {
        if (seen.has(value.id)) throw new Error(`Duplicate reference topic id: ${value.id}`);
        seen.add(value.id);
        topics.push({
          id: value.id,
          label: value.label,
          sourcePath: value.sourcePath ?? null,
          sourceUnavailable: value.sourceUnavailable ?? null,
          official,
        });
        return;
      }
    }
    for (const child of Array.isArray(value) ? value : Object.values(value)) visit(child);
  };

  visit(root);
  return topics;
};

const associationKey = (topicId, heading) => `${topicId}\u0000${heading}`;

const resultRank = {
  matched: 0,
  'source-blocked': 1,
  'reference-anomaly': 2,
  unreviewed: 3,
};

const subjectRows = SUBJECT_FILES.map(fileStem => {
  const referenceFile = path.join(DATA, `${fileStem}.json`);
  const reference = readJson(referenceFile);
  const subjectId = reference.subjectId;
  if (!subjectId) throw new Error(`${referenceFile}: missing subjectId`);

  const crosswalkFile = path.join(DATA, `${subjectId}-local-crosswalk.json`);
  const hasCrosswalk = fs.existsSync(crosswalkFile);
  const crosswalk = hasCrosswalk ? readJson(crosswalkFile) : null;
  const resolutions = new Map();

  for (const association of crosswalk?.associations ?? []) {
    if (!association.topicId || !association.heading || !association.resolution) continue;
    const key = associationKey(association.topicId, association.heading);
    const existing = resolutions.get(key);
    if (existing && existing !== association.resolution) {
      throw new Error(`${subjectId}: conflicting resolutions for ${key}`);
    }
    resolutions.set(key, association.resolution);
  }

  const topics = topicRecords(reference).map(topic => {
    const counts = { matched: 0, sourceBlocked: 0, referenceAnomaly: 0, unreviewed: 0 };
    const gaps = [];
    for (const heading of topic.official) {
      const resolution = resolutions.get(associationKey(topic.id, heading)) ?? 'unreviewed';
      if (resolution === 'matched') counts.matched += 1;
      else if (resolution === 'source-blocked') counts.sourceBlocked += 1;
      else if (resolution === 'reference-anomaly') counts.referenceAnomaly += 1;
      else counts.unreviewed += 1;
      if (resolution !== 'matched') gaps.push({ heading, resolution });
    }
    gaps.sort((a, b) => resultRank[a.resolution] - resultRank[b.resolution] || a.heading.localeCompare(b.heading));
    return {
      id: topic.id,
      label: topic.label,
      sourcePath: topic.sourcePath,
      referenceOfficialAssociations: topic.official.length,
      ...counts,
      ...(topic.sourceUnavailable ? { sourceUnavailable: topic.sourceUnavailable } : {}),
      gaps,
    };
  });

  const totals = topics.reduce((sum, topic) => ({
    referenceTopics: sum.referenceTopics + 1,
    referenceOfficialAssociations: sum.referenceOfficialAssociations + topic.referenceOfficialAssociations,
    matched: sum.matched + topic.matched,
    sourceBlocked: sum.sourceBlocked + topic.sourceBlocked,
    referenceAnomaly: sum.referenceAnomaly + topic.referenceAnomaly,
    unreviewed: sum.unreviewed + topic.unreviewed,
    sourceUnavailableTopics: sum.sourceUnavailableTopics + Number(Boolean(topic.sourceUnavailable)),
    topicsWithGaps: sum.topicsWithGaps + Number(topic.gaps.length > 0 || Boolean(topic.sourceUnavailable)),
  }), {
    referenceTopics: 0,
    referenceOfficialAssociations: 0,
    matched: 0,
    sourceBlocked: 0,
    referenceAnomaly: 0,
    unreviewed: 0,
    sourceUnavailableTopics: 0,
    topicsWithGaps: 0,
  });

  if (hasCrosswalk) {
    const crosswalkTotal = (crosswalk.associations ?? []).length;
    const accounted = totals.matched + totals.sourceBlocked + totals.referenceAnomaly;
    if (crosswalkTotal !== accounted || totals.unreviewed !== 0) {
      throw new Error(
        `${subjectId}: reference/crosswalk mismatch (${crosswalkTotal} crosswalk, ${accounted} accounted, ${totals.unreviewed} unreviewed)`,
      );
    }
  }

  return {
    subjectId,
    referenceFile: path.relative(ROOT, referenceFile),
    crosswalkFile: hasCrosswalk ? path.relative(ROOT, crosswalkFile) : null,
    totals,
    topics,
  };
});

const totals = subjectRows.reduce((sum, subject) => {
  for (const [key, value] of Object.entries(subject.totals)) sum[key] = (sum[key] ?? 0) + value;
  return sum;
}, { subjects: subjectRows.length, subjectsWithExactCrosswalks: subjectRows.filter(row => row.crosswalkFile).length });

const ledger = {
  schemaVersion: 1,
  generatedAt: new Date().toISOString(),
  scope: {
    included: 'Factual State-exam topic associations captured from every current StudyClix Leaving Certificate topic page.',
    excluded: 'Commercial mock questions and all provider-owned question text, solutions, notes, media and PDFs.',
    completionRule: 'Complete only when every official association is matched to an entitled SEC-paper task and every paper/scheme boundary passes visual QA.',
  },
  totals,
  subjects: subjectRows,
};

writeJson(path.join(DATA, 'studyclix-question-parity.json'), ledger);

const fmt = value => value.toLocaleString('en-IE');
const lines = [
  '# StudyClix official-question parity ledger',
  '',
  `Generated: ${ledger.generatedAt}`,
  '',
  'This is the question-level completion ledger. Mock questions are excluded. A',
  'topic is complete only when every factual StudyClix State-exam heading points',
  'to the matching task in NextStepUni’s entitled SEC paper corpus and that',
  'paper/marking-scheme boundary has been visually checked.',
  '',
  '| Subject | Topics | Official associations | Matched | Source blocked | Unreviewed | Topics with gaps |',
  '| --- | ---: | ---: | ---: | ---: | ---: | ---: |',
  ...subjectRows.map(subject => {
    const t = subject.totals;
    return `| ${subject.subjectId} | ${fmt(t.referenceTopics)} | ${fmt(t.referenceOfficialAssociations)} | ${fmt(t.matched)} | ${fmt(t.sourceBlocked)} | ${fmt(t.unreviewed)} | ${fmt(t.topicsWithGaps)} |`;
  }),
  '',
  `Total: **${fmt(totals.referenceTopics)} topics**, **${fmt(totals.referenceOfficialAssociations)} official topic associations**, `,
  `**${fmt(totals.matched)} matched**, **${fmt(totals.sourceBlocked)} source blocked**, and **${fmt(totals.unreviewed)} awaiting exact crosswalk review**.`,
  '',
  'The machine-readable companion contains every non-matched heading under its',
  'exact subject and topic: `data/examTopics/studyclix-question-parity.json`.',
  '',
];

fs.writeFileSync(path.join(DOCS, 'studyclix-question-parity.md'), `${lines.join('\n')}\n`);

console.log(JSON.stringify(totals, null, 2));
