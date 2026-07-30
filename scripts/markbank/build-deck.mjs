#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — compile authored cards into the deck module.
 *
 * Input is the JSON produced by the authoring workflow. This script does the one
 * thing an authoring agent is never allowed to do: bind a figure. Agents name a
 * figure by KEY only; the real path, hash and attribution are resolved here from
 * the file on disk. Both historical figure corruptions in this repo entered
 * through a hand-transcribed path, so no path in the output was ever typed by a
 * model.
 *
 *   node scripts/markbank/build-deck.mjs <cards.json> > components/MarkBank/cards2025hl.ts
 */

import { readFileSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const FIG_DIR = 'public/exam-figures/biology';

/** Figures that hold a neighbour's crop, or whose crop truncates a label the
 *  question asks about. Never bindable. Mirrors BLOCKED_FIGURES in deck.ts. */
const BLOCKED = new Set([
  'alveolus-gas-exchange', 'lymphocyte', 'shoulder-joint', 'neuron',
  'root-longitudinal-section', 'cell-membrane',
]);

/**
 * Alt text for the figures actually looked at. A figure with no entry here has
 * not been inspected, so it cannot be bound — describing an image nobody opened
 * is how Diagram Vault ended up confidently captioning bread mould as an alveolus.
 */
const ALT = {
  "digestive-system": "Outline of a human torso showing the digestive tract. A leader line marks the tube running down the neck and chest; a second marks an organ below the liver. The pancreas and small intestine are named on the diagram.",
  "rhizopus": "Rhizopus growing on a substrate: rounded heads on upright stalks, a cluster of small spores being released at the right, and a horizontal filament running across the surface.",
  "cell-division": "A cell late in division: two daughter nuclei have formed, each with chromosomes drawn on a spindle, and the cell is pinching in at the middle.",
  "circulatory-system": "A whole-body circulatory diagram: the heart at the centre, lungs above, and vessels running to the liver, gut, kidneys and the capillary beds of the head and lower body.",
  "pupil-eyes": "Two eyes side by side, drawn identically except that the pupil is small in the left and much larger in the right.",
  "mitochondrion": "Cross-section of a mitochondrion: a smooth outer membrane and an inner membrane folded into long finger-like cristae, with small dots scattered through the interior.",
  "chloroplast": "Cross-section of a chloroplast: an outer envelope enclosing four stacks of disc-shaped compartments joined by flattened channels, with small dots in the surrounding fluid. No parts are lettered.",
  "embryo-sac": "A carpel in section on the left, with an arrow enlarging its ovule on the right. Inside the enlarged ovule, leader lines mark P at a pair of central nuclei and Q at a cell below them.",
  "neurons": "Two neurons drawn side by side. Neuron X has a branched cell body at the top and runs down to a block of muscle cells; Neuron Y runs from a patch of skin at the bottom up past its cell body. A brace marks Z at the fine branches at the top of Y, and arrows name the Schwann cells along both axons.",
  "sperm-sem": "Electron micrograph of a single sperm cell against a dark background, with a 2 micrometre scale bar. An arrow marks A at the rounded head and a second marks B partway along the tail.",
  "fermenter": "Photograph of an industrial stainless-steel fermenter: a sealed cylindrical vessel on a wheeled frame, with pipework, valves and gauges around it. No parts are lettered.",
};

const cardsPath = process.argv[2];
if (!cardsPath) {
  console.error('usage: build-deck.mjs <cards.json>');
  process.exit(1);
}

const input = JSON.parse(readFileSync(cardsPath, 'utf8'));
const cards = Array.isArray(input) ? input : (input.accepted ?? input.cards ?? []);

const figureRecord = (key) => {
  if (BLOCKED.has(key)) return { error: `figure "${key}" is on the blocklist` };
  if (!ALT[key]) return { error: `figure "${key}" has not been inspected, so it has no verified alt text` };
  const rel = `${FIG_DIR}/biology-2025-hl-${key}.png`;
  const abs = resolve(ROOT, rel);
  if (!existsSync(abs)) return { error: `figure file missing: ${rel}` };
  return {
    candId: `biology-2025-hl-${key}`,
    src: `/exam-figures/biology/biology-2025-hl-${key}.png`,
    srcHash: createHash('md5').update(readFileSync(abs)).digest('hex'),
    alt: ALT[key],
    attribution: 'SEC Leaving Certificate Biology 2025 Higher Level — © State Examinations Commission',
  };
};

const q = (s) => JSON.stringify(String(s));

/**
 * A row that states only what the marks are worth, with no answer in it. Roughly
 * a third of Section B scheme rows read this way ("Control named and setup
 * described"), and transcribing them is precisely how Answer Architect failed.
 * Mirrors isContentFreeRow in types/markBank.ts.
 */
const isContentFree = (v) => {
  const t = String(v).trim().toLowerCase();
  if (!t) return true;
  if (/^\d+\s*(items?|points?|answers?)?[,\s]*\d*\s*marks?\s*(each)?\.?$/.test(t)) return true;
  return /^(named piece of apparatus( used)?|control named( and setup described)?|safety precaution described|correct (sketch|matching result|position)|suitable (time|temperature|volume)|left for a (suitable )?time|any correct|the description earns|description how|matching result)/.test(t);
};

const out = [];
const dropped = [];
const seenId = new Set();
const seenHash = new Map();

for (const c of cards) {
  if (seenId.has(c.id)) { dropped.push(`${c.id}: duplicate id`); continue; }

  const contentFree = c.rows.filter(r => r.kind !== 'anyN' && isContentFree(r.verbatim));
  if (contentFree.length) {
    dropped.push(`${c.id}: ${contentFree.length} content-free row(s), e.g. "${contentFree[0].verbatim}"`);
    continue;
  }

  let figure = null;
  let labelKey = null;
  if (c.figureKey) {
    const rec = figureRecord(c.figureKey);
    if (rec.error) { dropped.push(`${c.id}: ${rec.error}`); continue; }
    // A lettered figure MUST decode its letters; an unlettered one has nothing
    // to decode and rides on a plain question card instead.
    const lettered = Array.isArray(c.labelKey) && c.labelKey.length > 0;
    const prev = seenHash.get(rec.srcHash);
    if (prev && prev !== c.figureKey) { dropped.push(`${c.id}: crop already bound as "${prev}"`); continue; }
    seenHash.set(rec.srcHash, c.figureKey);
    figure = { ...rec, lettersVisible: lettered ? c.labelKey.map(k => k.letter) : [] };
    labelKey = lettered ? c.labelKey : null;
  }

  seenId.add(c.id);
  const rows = c.rows.map(r => {
    const parts = [`id: ${q(r.id)}`, `kind: ${q(r.kind)}`, `verbatim: ${q(r.verbatim)}`,
      `marks: ${r.marks === null || r.marks === undefined ? 'null' : r.marks}`];
    if (r.accepts?.length) parts.push(`accepts: ${JSON.stringify(r.accepts)}`);
    if (r.contextNote) parts.push(`contextNote: ${q(r.contextNote)}`);
    if (r.openList) parts.push('openList: true');
    if (r.exactTermRequired) parts.push('exactTermRequired: true');
    if (r.dependsOn) parts.push(`dependsOn: ${q(r.dependsOn)}`);
    if (r.group) parts.push(`group: ${JSON.stringify(r.group)}`);
    return `    { ${parts.join(', ')} },`;
  }).join('\n');

  out.push(`  {
    ...base, kind: ${q(labelKey ? 'diagram' : 'question')},
    id: ${q(c.id)}, topicId: ${q(c.topicId)}, conceptId: ${q(c.conceptId)},
    section: ${q(c.section)}, questionRef: ${q(c.questionRef)},${c.paperFileid ? `\n    paperFileid: ${q(c.paperFileid)},` : ''}${c.stem ? `\n    stem: ${q(c.stem)},` : ''}
    questionText: ${q(c.questionText)},
    tariffModel: ${JSON.stringify(c.tariffModel)}, totalMarks: ${c.totalMarks},
    rows: [
${rows}
    ],${figure ? `\n    figure: ${JSON.stringify(figure, null, 6).replace(/\n/g, '\n    ')},` : ''}${labelKey ? `\n    labelKey: ${JSON.stringify(labelKey)},` : ''}
  } as SecCard,`);
}

process.stderr.write(`built ${out.length} cards, dropped ${dropped.length}\n`);
for (const d of dropped) process.stderr.write(`  DROPPED ${d}\n`);

console.log(`/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — cards from the 2025 Higher Level Biology paper.
 *
 * GENERATED by scripts/markbank/build-deck.mjs. Do not edit by hand.
 *
 * Every question, marking point and mark value is transcribed from
 * examiner-reports/biology/2025-hl-marking-scheme.md and independently checked
 * against it. Figure paths and hashes are resolved from the files on disk by the
 * build script — never typed — because both historical figure corruptions in this
 * repo entered through a hand-transcribed path.
 *
 * Cards are tagged to the REDEVELOPED specification's units, not the retired
 * Unit One/Two/Three syllabus.
 */

import type { SecCard } from '../../types/markBank';

const base = {
  source: 'sec' as const,
  subjectId: 'biology',
  level: 'higher' as const,
  year: 2025,
  paperFileid: 'LC025ALP038EV',
  specVersion: 'lc-biology-2002',
  qa: { gates: ['verbatim', 'tariff', 'figure'], humanReviewedBy: 'agent-verified', humanReviewedAt: '2026-07-30' },
  schemeCitation: 'Marking points quoted from the SEC marking scheme, Biology 2025 Higher Level — © State Examinations Commission.',
};

export const CARDS_2025_HL: SecCard[] = [
${out.join('\n')}
];
`);
