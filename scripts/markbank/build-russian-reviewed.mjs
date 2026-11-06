#!/usr/bin/env node
/** Bind source-reviewed Russian data to the harvested SEC document identities. */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { paperEntry, resolvePaperFileid, resolveCompanionFileid } from './paperIndex.mjs';
import { audioMaterialFault } from './audioMaterial.mjs';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const read = relative => JSON.parse(readFileSync(resolve(ROOT, relative), 'utf8'));
const authored = read('scripts/markbank/authored/russian-reviewed.json');
const legacy = read('scripts/markbank/authored/russian.json');
const ids = new Set();
const records = [];
const cards = authored.map(({ review, ...card }) => {
  if (ids.has(card.id) || card.subjectId !== 'russian') throw new Error(`Invalid reviewed identity ${card.id}`);
  ids.add(card.id);
  const previous = legacy.find(original => original.id === card.id);
  if (previous && !review.correctsExisting) throw new Error(`Russian correction must be explicit: ${card.id}`);
  if (review.correctsExisting && !previous) throw new Error(`Stale Russian correction: ${card.id}`);
  const paperFileid = review.component === 'A00'
    ? resolveCompanionFileid('russian', card.year, card.level, 'Aural Paper')
    : resolvePaperFileid('russian', card.year, card.level, card.section);
  const entry = paperEntry('russian', card.year, card.level);
  const paper = entry?.papers.find(item => item.doc.f === `${paperFileid}.pdf`);
  if (!paper?.scheme?.f || !review.paperPages.length || !review.schemePages.length) throw new Error(`Unbound Russian source ${card.id}`);
  const audioFault = audioMaterialFault(card, 'russian');
  if (audioFault || (review.component === 'A00' && !card.audioMaterial)) throw new Error(`${card.id}: ${audioFault ?? 'missing recording'}`);
  records.push({ id: card.id, year: card.year, level: card.level, questionRef: card.questionRef,
    topicId: card.topicId, paperFileid: paper.doc.f, schemeFileid: paper.scheme.f, ...review });
  return { ...card, source: 'sec', paperFileid, specVersion: 'lc-russian-syllabus',
    schemeCitation: `SEC Russian ${card.year} ${card.level === 'higher' ? 'Higher' : 'Ordinary'} Level marking scheme, pages ${review.schemePages.join(', ')} — © State Examinations Commission.`,
    schemeRegion: { schemeFileid: paper.scheme.f, p: review.schemePages[0], r: [0, 0, 1, 1] },
    qa: { gates: ['original-pdf-review', 'printed-task-census', 'source-defined-tariff', ...(previous ? ['reviewed-card-correction'] : [])],
      humanReviewedBy: 'Codex source review; browser QA pending', humanReviewedAt: '2026-11-06' } };
});
const out = resolve(ROOT, 'components/MarkBank/cards/russian');
mkdirSync(out, { recursive: true });
writeFileSync(resolve(out, 'reviewed.json'), JSON.stringify(cards, null, 2) + '\n');
writeFileSync(resolve(ROOT, 'scripts/markbank/authoring/russian-reviewed-sources.json'), JSON.stringify(records, null, 2) + '\n');
console.log(`Russian reviewed overlay: ${cards.length} cards; ${cards.filter(card => !legacy.some(original => original.id === card.id)).length} additions, ${cards.filter(card => legacy.some(original => original.id === card.id)).length} explicit corrections.`);
