#!/usr/bin/env node
/**
 * Build the many-to-many bridge from the audited Business practice taxonomy
 * to the two official curriculum specifications it spans.
 *
 * New-course labels are the specification's numbered learning areas and map
 * to stable 2027 nodes. Old-course labels map to the established syllabus
 * summary nodes already used by Mark Bank. The broad initials bucket is an
 * indexing convenience rather than a syllabus topic, so it deliberately
 * reaches every outgoing content node (but not the ABQ assessment bucket).
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const REFERENCE_PATH = path.join(ROOT, 'data/examTopics/business.json');
const OUTPUT_PATH = path.join(
  ROOT,
  'data/examTopics/business-curriculum-crosswalk.json',
);

const reference = JSON.parse(fs.readFileSync(REFERENCE_PATH, 'utf8'));
const variants = [
  'higher-new-course',
  'higher-old-course',
  'ordinary-new-course',
  'ordinary-old-course',
];

const outgoingByCode = {
  '1.1': 'business-0-12',
  '1.2': 'business-0-13',
  '1.3': 'business-0-14',
  '2.1': 'business-1-5',
  '3.1': 'business-2-11',
  '3.2': 'business-2-12',
  '3.3': 'business-2-13',
  '4.1': 'business-3-16',
  '4.2': 'business-3-17',
  '4.3': 'business-3-18',
  '4.4': 'business-3-19',
  '4.5': 'business-3-20',
  '4.6': 'business-3-21',
  '5.1': 'business-4-14',
  '5.2': 'business-4-15',
  '5.3': 'business-4-16',
  '5.4': 'business-4-17',
  '5.5': 'business-4-18',
  '6.1': 'business-5-13',
  '6.2': 'business-5-14',
  '6.3': 'business-5-15',
  '6.4': 'business-5-16',
  '6.5': 'business-5-17',
  '7.1': 'business-6-13',
  '7.2': 'business-6-14',
  '7.3': 'business-6-15',
};
const outgoingContentNodes = Object.values(outgoingByCode);

const result = {};
for (const variant of variants) {
  const isNew = variant.includes('new-course');
  for (const topic of reference.variants[variant].topics) {
    let nodes;
    if (isNew) {
      const match = topic.label.match(/^(?:U(\d+)\.|([1-4])\.(\d+))(?:\s|$)/i);
      if (!match) throw new Error(`${topic.id}: missing 2027 specification code`);
      nodes = [match[1]
        ? `business-2027-u${match[1]}`
        : `business-2027-${match[2]}-${match[3]}`];
    } else if (/^ABQ\b/i.test(topic.label)) {
      nodes = ['business-4-19'];
    } else if (/^What do these initials stand for\?$/i.test(topic.label)) {
      nodes = outgoingContentNodes;
    } else {
      const code = topic.label.match(/^(\d\.\d)\b/)?.[1];
      const node = code ? outgoingByCode[code] : undefined;
      if (!node) throw new Error(`${topic.id}: unknown outgoing syllabus code`);
      nodes = [node];
    }
    result[topic.id] = [...new Set(nodes)];
  }
}

const expectedIds = variants.flatMap(variant => (
  reference.variants[variant].topics.map(topic => topic.id)
));
if (expectedIds.length !== 105 || Object.keys(result).length !== 105) {
  throw new Error('Business curriculum crosswalk must cover all 105 topics');
}
if (expectedIds.some(id => !result[id]?.length)) {
  throw new Error('Business curriculum crosswalk contains an empty topic');
}

fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify(result, null, 2)}\n`);
console.log(JSON.stringify({
  output: path.relative(ROOT, OUTPUT_PATH),
  topics: Object.keys(result).length,
  outgoingNodes: new Set(Object.values(result).flat().filter(id => !id.startsWith('business-2027-'))).size,
  redevelopedNodes: new Set(Object.values(result).flat().filter(id => id.startsWith('business-2027-'))).size,
}, null, 2));
