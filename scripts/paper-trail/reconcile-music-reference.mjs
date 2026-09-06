#!/usr/bin/env node
/** @license SPDX-License-Identifier: Apache-2.0 */
/**
 * Inventory Music reference headings against entitled local SEC sources.
 * This is a review queue, not a runtime topic map or a completeness claim.
 * Component and physical booklet identities are retained because every Music
 * booklet restarts its question numbering. Practical section numbers must not
 * be joined to the old flattened local card numbers without visual review.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const read = relative => JSON.parse(fs.readFileSync(path.join(ROOT, relative), 'utf8'));
const reference = read('data/examTopics/music.json');
const snapshot = read('data/examTopics/studyclix-subject-taxonomy.json');
const baseline = read('test/fixtures/musicTopicQuestionBaseline.json');
// This artifact intentionally records the fixed pre-migration boundary. Do
// not read the expanding live tag wave here: rerunning the inventory after the
// additive migration must not rewrite history and report the new cards as if
// they had existed at capture time.
const tags = baseline.map(paper => ({ ...paper, q: paper.questions }));
const paperId = p => [p.level, p.lang, p.year, p.paperKey, p.fileid].join('|');
const inventory = [];
const corpusRoot = path.join(ROOT, 'paper-trail-corpus/exampapers');
for (const year of fs.readdirSync(corpusRoot).filter(y => /^\d{4}$/.test(y)).sort()) {
  for (const fileid of fs.readdirSync(path.join(corpusRoot, year)).sort()) {
    const match = fileid.match(/^LC067([AG])LP(006|007|008|U00)(EV|IV)\.pdf$/);
    if (!match) continue;
    const level = match[1] === 'A' ? 'higher' : 'ordinary';
    const lang = match[3].toLowerCase();
    const paper = tags.find(p => p.year === Number(year) && p.fileid === fileid);
    const sidecarPath = `scripts/paper-trail/answers/${year}/${fileid}.json`;
    const sidecar = fs.existsSync(path.join(ROOT, sidecarPath)) ? read(sidecarPath) : null;
    inventory.push({ year: Number(year), level, lang, fileid, component: match[2],
      taggedCardCount: paper?.q.length ?? 0,
      answerMapCardCount: sidecar?.q.length ?? 0,
      hasHostedPaperMap: Boolean(paper && match[2] !== '006'),
    });
  }
}

let preservedCards = 0;
for (const frozen of baseline) {
  const live = tags.find(p => paperId(p) === paperId(frozen));
  if (!live) throw new Error(`Missing frozen Music paper: ${paperId(frozen)}`);
  for (const expected of frozen.questions) {
    const actual = live.q.find(q => q.n === expected.n);
    if (!actual || actual.primary !== expected.primary || actual.secondary !== expected.secondary) {
      throw new Error(`Changed frozen Music card: ${paperId(frozen)}|${expected.n}`);
    }
    preservedCards++;
  }
}

const rows = [];
const counts = { topics: 0, reported: 0, official: 0, excludedMocks: 0, excludedProviderSamples: 0 };
for (const [level, variant] of Object.entries(reference.variants)) {
  const expected = snapshot.variants.find(v => v.subjectSlug === 'music' && v.variant === level);
  if (!expected || JSON.stringify(variant.topics.map(t => [t.label, t.sourcePath]))
    !== JSON.stringify(expected.topics.map(t => [t.label, t.sourcePath]))) {
    throw new Error(`Music ${level} hierarchy mismatch`);
  }
  for (const topic of variant.topics) {
    const extracted = topic.officialQuestionHeadings.length + topic.mockQuestionCount
      + topic.providerSampleQuestionCount;
    if (topic.reportedQuestionCount !== extracted || topic.extractedQuestionCount !== extracted) {
      throw new Error(`Unreconciled Music topic: ${topic.id}`);
    }
    counts.topics++;
    counts.reported += extracted;
    counts.official += topic.officialQuestionHeadings.length;
    counts.excludedMocks += topic.mockQuestionCount;
    counts.excludedProviderSamples += topic.providerSampleQuestionCount;
    for (const heading of topic.officialQuestionHeadings) {
      if (/mock/i.test(heading)) throw new Error(`Mock title in official Music references: ${heading}`);
      const year = Number(heading.match(/^(\d{4}) - /)?.[1]);
      if (!year) throw new Error(`Missing year: ${heading}`);
      const sitting = /deferred/i.test(heading) ? 'deferred' : /sample/i.test(heading) ? 'sample' : 'main';
      const component = /Unprepared/i.test(heading) ? 'U00'
        : /Composing/i.test(heading) ? '006'
          : /Listening/i.test(heading) || topic.sourcePath.includes('/listening-') ? '008' : null;
      if (!component) throw new Error(`Unclassified Music component: ${heading}`);
      // These are candidate joins only. Preserve the original heading and
      // require SEC review before a reference classification affects students.
      const numericQuestion = heading.match(/\bQuestion (\d+)\b/)?.[1];
      const sectionQuestion = component === '008' ? heading.match(/\bSection ([1-6]) - Question [A-Za-z]/)?.[1] : null;
      const composingPart = component === '006' ? heading.match(/\bQuestion [AB] - Part ([1-6])$/)?.[1] : null;
      const question = component === 'U00' ? null : numericQuestion ?? sectionQuestion ?? composingPart ?? null;
      const localSources = sitting === 'main'
        ? inventory.filter(p => p.year === year && p.level === level && p.component === component) : [];
      const candidateCards = question === null ? [] : localSources.flatMap(source => {
        const tagged = tags.find(p => p.year === year && p.fileid === source.fileid);
        return tagged?.q.some(q => q.n === question)
          ? [{ fileid: source.fileid, lang: source.lang, paperKey: tagged.paperKey, n: question }] : [];
      });
      const status = !localSources.length ? 'official-source-required'
        : component === 'U00' || question === null ? 'question-identity-review-required'
          : candidateCards.length ? 'candidate-local-card-review-required' : 'local-topic-cards-required';
      rows.push({ topicId: topic.id, level, heading, year, sitting, component, question,
        status, localFileids: localSources.map(p => p.fileid), candidateCards });
    }
  }
}
const statusCounts = Object.fromEntries([...new Set(rows.map(r => r.status))].sort()
  .map(status => [status, rows.filter(r => r.status === status).length]));
const report = {
  schemaVersion: 1, subjectId: 'music', capturedAt: reference.capturedAt,
  status: 'pre-migration-review-snapshot',
  reviewPolicy: 'This reproducible snapshot freezes the pre-migration source boundary. Candidate identities were not activated directly; the additive runtime generator separately verifies component-aware local joins. Practical section/question numbers are not joined to flattened legacy card IDs.',
  counts: { ...counts, ...statusCounts, preservedVariants: baseline.length,
    preservedCards, localPaperVariants: inventory.length,
    taggedVariants: inventory.filter(p => p.taggedCardCount > 0).length,
    untaggedVariants: inventory.filter(p => p.taggedCardCount === 0).length,
    variantsWithAnswerMaps: inventory.filter(p => p.answerMapCardCount > 0).length },
  inventory, references: rows,
};
const output = path.join(ROOT, 'data/examTopics/music-audit-reconciliation.json');
fs.writeFileSync(output, `${JSON.stringify(report, null, 2)}\n`);
console.log(JSON.stringify(report.counts, null, 2));
