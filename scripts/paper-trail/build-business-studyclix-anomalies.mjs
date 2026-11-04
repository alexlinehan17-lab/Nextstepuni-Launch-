#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Record each Business StudyClix heading whose outgoing-course topic the SEC
 * paper and scheme do not support, with the reviewed topic and its reason.
 *
 *   node scripts/paper-trail/build-business-studyclix-anomalies.mjs
 *   node scripts/paper-trail/build-business-exam-topic-crosswalk.mjs
 *   node scripts/paper-trail/report-studyclix-question-parity.mjs
 *
 * Writes data/examTopics/business-studyclix-anomalies.json, which the
 * crosswalk builder applies as reviewed reference-anomaly records. Re-running
 * the three commands on committed files leaves every output byte-identical.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { build } from 'esbuild';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const bundle = await build({
  entryPoints: [path.join(root, 'scripts/paper-trail/businessStudyclixAnomalies.ts')],
  bundle: true, format: 'esm', platform: 'node', write: false, logLevel: 'silent',
});
const { businessStudyclixAnomalies } = await import(
  `data:text/javascript;base64,${Buffer.from(bundle.outputFiles[0].text).toString('base64')}`);

const readJson = file => JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'));
const crosswalk = readJson('data/examTopics/business-local-crosswalk.json');
const reviews = readJson('data/examTopics/business-source-reviewed-topics.json').questions;
const cards = readJson('components/MarkBank/cards/business/rubric-authored.json').cards;

const anomalies = businessStudyclixAnomalies(crosswalk.associations, reviews, cards);
const out = {
  schemaVersion: 1,
  subjectId: 'business',
  sources: [
    'data/examTopics/business-source-reviewed-topics.json',
    'components/MarkBank/cards/business/rubric-authored.json',
  ],
  rule: 'A StudyClix heading is matched only when its topic is one the reviewed question carries. '
    + 'Every other heading on a directly reviewed Business question is recorded here as a reference-anomaly.',
  count: anomalies.length,
  anomalies,
};
fs.writeFileSync(path.join(root, 'data/examTopics/business-studyclix-anomalies.json'), `${JSON.stringify(out, null, 2)}\n`);
console.log(`${anomalies.length} Business StudyClix headings recorded as reviewed reference anomalies`);
