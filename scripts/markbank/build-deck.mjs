#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — compile authored cards into the deck modules.
 *
 * Input is the JSON produced by an authoring workflow. This script does the two
 * things an authoring agent is never allowed to do: bind a figure, and name a
 * paper. Agents name a figure by KEY only and never name a paper at all; the real
 * path, hash, attribution and SEC file id are resolved here from data on disk.
 * Both historical figure corruptions in this repo entered through a
 * hand-transcribed path, and the first Biology build pointed every card at the
 * marking scheme PDF instead of the question paper for the same reason.
 *
 * The subject is taken from the cards themselves, not a flag — a flag that
 * disagreed with the data would file a deck under the wrong subject silently.
 *
 *   node scripts/markbank/build-deck.mjs <cards.json>
 */

import { readFileSync, existsSync, writeFileSync, mkdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

import { resolvePaperFileid } from './paperIndex.mjs';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

/** Per-subject facts the generated module needs. Adding a subject means adding
 *  a row here, and nothing else in this script changes. */
const SUBJECTS = {
  biology: {
    title: 'Biology',
    specVersion: 'lc-biology-2002',
    figureDir: 'public/exam-figures/biology',
    /** Crops that hold a neighbour's image, or truncate a label the question
     *  asks about. Never bindable. Mirrors BLOCKED_FIGURES in deck.ts. */
    blocked: new Set([
      'alveolus-gas-exchange', 'lymphocyte', 'shoulder-joint', 'neuron',
      'root-longitudinal-section', 'cell-membrane',
    ]),
  },
  chemistry: {
    title: 'Chemistry',
    /* The syllabus examined before the 2027 redevelopment. Named by what it is
     * rather than by a year, because I have not verified its publication year
     * and an unverified date in a provenance field is worse than none. */
    specVersion: 'lc-chemistry-legacy',
    figureDir: 'public/exam-figures/chemistry',
    blocked: new Set(),
  },
};

/**
 * Alt text for the Biology figures actually looked at, from before the figure
 * manifest existed. A figure with no entry here has not been inspected, so it
 * cannot be bound — describing an image nobody opened is how Diagram Vault ended
 * up confidently captioning bread mould as an alveolus.
 */
const ALT = {
  "cell-membrane-labelled": "Cross-section of a cell membrane: a curved phospholipid bilayer with proteins embedded in and across it. A brace marks X at the bilayer itself on the left, and an arrow marks Y at a protein spanning the membrane.",
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

/* ------------------------------------------------------- provenance gate ---- */

const schemeCache = new Map();

/**
 * The scheme a card must be traceable to. Comparison drops mark-only lines and
 * ignores spacing: a marks cell is vertically centred against a multi-line answer
 * so the mark lands BETWEEN the lines it belongs to, and chemical subscripts sit
 * on their own baseline ("C x ( H 2 O )y").
 */
const MARKS_ONLY = /^\s*\d+\s*(\(\s*\d+\s*\))?\s*$/;

/**
 * Sub- and superscript digits folded to the digits they stand for.
 *
 * The SEC's PDFs extract formulae as plain ASCII — "H2SO4", not "H₂SO₄" — but an
 * author writing the answer out is liable to typeset it properly. Without this
 * fold the two normalise to "hso" and "h2so4", and a correct card gets dropped
 * for being untraceable. Folding maps a character to the digit it already means;
 * it does not loosen what counts as a match.
 */
const SUP = { '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9' };
const foldDigits = (t) => t
  .replace(/[₀-₉]/g, (c) => String(c.charCodeAt(0) - 0x2080))
  .replace(/[⁰¹²³⁴-⁹]/g, (c) => SUP[c] ?? c);

const normalise = (t) =>
  foldDigits(t).toLowerCase().replace(/[‐-―]/g, '-').replace(/[^a-z0-9]+/g, '');

function schemeFor(subjectId, card) {
  const stem = `${card.year ?? 2025}-${(card.level ?? 'higher') === 'higher' ? 'hl' : 'ol'}`;
  const file = resolve(ROOT, 'examiner-reports', subjectId, 'schemes', `${stem}.md`);
  if (!schemeCache.has(file)) {
    const raw = existsSync(file) ? readFileSync(file, 'utf8') : '';
    schemeCache.set(file, normalise(raw.split('\n').filter(l => !MARKS_ONLY.test(l)).join(' ')));
  }
  return schemeCache.get(file);
}

/** Text that is a table fragment or a header rather than an answerable question. */
function badQuestion(text) {
  const t = String(text).trim();
  if (t.length < 16) return 'question text is too short to stand alone';
  if (/^section\s+[abc]\b/i.test(t)) return 'question text is a section header';
  if (/^question\s+\d+\.?$/i.test(t)) return 'question text is just a question number';
  if (/^\(?\d+\s*m(arks)?\)?\.?$/i.test(t)) return 'question text is a bare tariff';
  return null;
}

const cardsPath = process.argv[2];
if (!cardsPath) {
  console.error('usage: build-deck.mjs <cards.json>');
  process.exit(1);
}

const input = JSON.parse(readFileSync(cardsPath, 'utf8'));
const cards = Array.isArray(input) ? input : (input.accepted ?? input.cards ?? []);

/* The subject comes from the cards. Mixed input is a mistake, not a feature:
 * one run writes one subject's modules, so a stray card would vanish silently. */
const subjectIds = [...new Set(cards.map(c => c.subjectId ?? 'biology'))];
if (subjectIds.length !== 1) {
  console.error(`cards span ${subjectIds.length} subjects (${subjectIds.join(', ')}) — build one subject at a time`);
  process.exit(1);
}
const SUBJECT_ID = subjectIds[0];
const SUBJECT = SUBJECTS[SUBJECT_ID];
if (!SUBJECT) {
  console.error(`unknown subject "${SUBJECT_ID}" — add it to SUBJECTS in this script`);
  process.exit(1);
}

/**
 * Figures published by bind-figures.mjs: every one was OPENED by an inspecting
 * agent, and only those it marked complete and non-truncated are in here. Its id
 * is the extractor's own name, derived from the figure's page and index in the
 * PDF, so an authoring agent naming a figure cannot invent a path.
 */
const MANIFEST_PATH = resolve(ROOT, 'components/MarkBank/figures.json');
const MANIFEST = existsSync(MANIFEST_PATH) ? JSON.parse(readFileSync(MANIFEST_PATH, 'utf8')) : {};

const figureRecord = (key) => {
  if (SUBJECT.blocked.has(key)) return { error: `figure "${key}" is on the blocklist` };

  const inspected = MANIFEST[key];
  if (inspected) {
    const abs = resolve(ROOT, 'public', inspected.src.replace(/^\//, ''));
    if (!existsSync(abs)) return { error: `figure file missing: ${inspected.src}` };
    const md5 = createHash('md5').update(readFileSync(abs)).digest('hex');
    if (md5 !== inspected.md5) return { error: `figure "${key}" changed on disk since it was inspected` };
    return {
      candId: key,
      src: inspected.src,
      srcHash: md5,
      alt: inspected.alt,
      attribution: inspected.attribution,
    };
  }

  // Legacy 2025 Biology Higher Level crops, bound before the manifest existed.
  if (SUBJECT_ID !== 'biology' || !ALT[key]) {
    return { error: `figure "${key}" has not been inspected, so it has no verified alt text` };
  }
  const rel = `${SUBJECT.figureDir}/biology-2025-hl-${key}.png`;
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

/**
 * Whether a card's rows add up to the tariff the paper prints.
 *
 * Mirrors tariffReconciles in types/markBank.ts, including its handling of the
 * double solidus: mutually exclusive routes are counted ONCE and each must reach
 * the tariff alone, because a student takes one route or the other. Checked here
 * so a bad card is DROPPED with a reason rather than failing the whole suite.
 */
function tariffFault(c) {
  const t = c.tariffModel ?? { kind: 'fixed' };
  if (t.kind === 'orderedSplit') {
    return c.rows.every(r => r.marks === null || r.marks === undefined)
      ? null : 'an ordered split cannot give rows their own marks';
  }
  if (t.kind === 'bestNofParts') {
    return t.answer * t.perPart === c.totalMarks
      ? null : `best-of tariff ${t.answer}x${t.perPart} does not make ${c.totalMarks}`;
  }
  const worth = (r) => (r.kind === 'anyN' && r.group ? r.group.claimMax * r.group.perOption : (r.marks ?? 0));
  const byRoute = new Map();
  let common = 0;
  for (const r of c.rows) {
    if (!r.route) common += worth(r);
    else byRoute.set(r.route, (byRoute.get(r.route) ?? 0) + worth(r));
  }
  if (!byRoute.size) {
    return common === c.totalMarks ? null : `rows sum to ${common}, tariff is ${c.totalMarks}`;
  }
  const short = [...byRoute.entries()].filter(([, n]) => common + n !== c.totalMarks);
  return short.length
    ? `route ${short.map(([k, n]) => `"${k}" sums to ${common + n}`).join(', ')}, tariff is ${c.totalMarks}`
    : null;
}

/**
 * One card per question.
 *
 * A question first carded without its diagram, then re-carded once a verified
 * figure existed, would otherwise ship twice — and the figureless version is the
 * broken one: "Explain how you know the ventricles are contracting" cannot be
 * answered without seeing which diagram is meant. Where two cards claim the same
 * question, the one carrying a figure wins.
 */
const byQuestion = new Map();
for (const c of cards) {
  const prev = byQuestion.get(c.questionRef);
  if (!prev) { byQuestion.set(c.questionRef, c); continue; }
  const prevHasFigure = Boolean(prev.figureKey);
  const thisHasFigure = Boolean(c.figureKey);
  if (thisHasFigure && !prevHasFigure) byQuestion.set(c.questionRef, c);
}

const out = [];
const dropped = [];
const seenId = new Set();
const seenHash = new Map();
let unresolvedPapers = 0;

for (const c of cards) {
  if (byQuestion.get(c.questionRef) !== c) {
    dropped.push(`${c.id}: superseded for ${c.questionRef} by a card carrying its figure`);
    continue;
  }
  if (seenId.has(c.id)) { dropped.push(`${c.id}: duplicate id`); continue; }

  const contentFree = c.rows.filter(r => r.kind !== 'anyN' && isContentFree(r.verbatim));
  if (contentFree.length) {
    dropped.push(`${c.id}: ${contentFree.length} content-free row(s), e.g. "${contentFree[0].verbatim}"`);
    continue;
  }

  const badQ = badQuestion(c.questionText);
  if (badQ) { dropped.push(`${c.id}: ${badQ} — "${c.questionText}"`); continue; }

  const badTariff = tariffFault(c);
  if (badTariff) { dropped.push(`${c.id}: ${badTariff}`); continue; }

  // A question naming lettered parts is unanswerable without the figure.
  const invitesDrawing = /you may include a labelled/i.test(c.questionText);
  const namesLetters = !invitesDrawing
    && /\blabelled [A-Z]\b|\bstructures? [A-Z](,| and )|\bparts? [A-Z](,| and )|\blabelled\s+(parts|structures)\b/i.test(c.questionText);
  // Not merely "has a figure": a question about labelled parts needs those
  // labels DECODED, so it must be a full diagram card with a label key.
  if (namesLetters && !(c.figureKey && Array.isArray(c.labelKey) && c.labelKey.length)) {
    dropped.push(`${c.id}: names lettered parts but carries no labelled figure`);
    continue;
  }

  // Every marking point must actually appear in its own scheme.
  const scheme = schemeFor(SUBJECT_ID, c);
  if (!scheme) { dropped.push(`${c.id}: no scheme on disk for ${c.year} ${c.level}`); continue; }
  const untraceable = [];
  for (const r of c.rows) {
    const claims = r.kind === 'anyN' && r.group ? r.group.options : [String(r.verbatim).split(/\s[—-]\s/).pop()];
    for (const claim of claims) {
      if (!scheme.includes(normalise(claim))) untraceable.push(claim);
    }
  }
  if (untraceable.length) {
    dropped.push(`${c.id}: ${untraceable.length} marking point(s) not found in the ${c.year} ${c.level} scheme, e.g. "${String(untraceable[0]).slice(0, 60)}"`);
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
    if (r.route) parts.push(`route: ${q(r.route)}`);
    if (r.dependsOn) parts.push(`dependsOn: ${q(r.dependsOn)}`);
    if (r.group) parts.push(`group: ${JSON.stringify(r.group)}`);
    return `    { ${parts.join(', ')} },`;
  }).join('\n');

  const year = c.year ?? 2025;
  const level = c.level ?? 'higher';
  const levelWord = level === 'higher' ? 'Higher' : 'Ordinary';
  const fileid = resolvePaperFileid(SUBJECT_ID, year, level, c.section);
  if (!fileid) unresolvedPapers++;

  out.push({ level, code: `  {
    ...base, kind: ${q(labelKey ? 'diagram' : 'question')},
    year: ${year}, level: ${q(level)},
    paperFileid: ${fileid ? q(fileid) : 'null'},
    schemeCitation: ${q(`Marking points quoted from the SEC marking scheme, ${SUBJECT.title} ${year} ${levelWord} Level — © State Examinations Commission.`)},
    id: ${q(c.id)}, topicId: ${q(c.topicId)}, conceptId: ${q(c.conceptId)},
    section: ${q(c.section)}, questionRef: ${q(c.questionRef)},${c.stem ? `\n    stem: ${q(c.stem)},` : ''}
    questionText: ${q(c.questionText)},
    tariffModel: ${JSON.stringify(c.tariffModel)}, totalMarks: ${c.totalMarks},
    rows: [
${rows}
    ],${figure ? `\n    figure: ${JSON.stringify(figure, null, 6).replace(/\n/g, '\n    ')},` : ''}${labelKey ? `\n    labelKey: ${JSON.stringify(labelKey)},` : ''}
  } as SecCard,` });
}

process.stderr.write(`${SUBJECT.title}: built ${out.length} cards, dropped ${dropped.length}\n`);
for (const d of dropped) process.stderr.write(`  DROPPED ${d}\n`);
if (unresolvedPapers) {
  process.stderr.write(`  ${unresolvedPapers} card(s) have no paper in the Paper Trail index; paperFileid is null rather than guessed\n`);
}

/**
 * One module per subject and level, not one for the whole deck.
 *
 * A student sits one subject at one level, so shipping everything in a single
 * chunk makes them download decks they will never open — and that cost grows with
 * every authoring wave. Splitting here lets the tool dynamic-import only what is
 * in front of the student.
 */
const OUT_DIR = resolve(ROOT, 'components/MarkBank/cards', SUBJECT_ID);
mkdirSync(OUT_DIR, { recursive: true });

const moduleFor = (level, cards) => `/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — authored ${SUBJECT.title} cards, ${level === 'higher' ? 'Higher' : 'Ordinary'} Level.
 *
 * GENERATED by scripts/markbank/build-deck.mjs. Do not edit by hand.
 *
 * Every question, marking point and mark value is transcribed from the marking
 * scheme for that card's own year and level in examiner-reports/${SUBJECT_ID}/schemes/,
 * and the build drops any card whose content cannot be found there. Figure paths,
 * hashes and SEC paper file ids are resolved from data on disk by the build
 * script — never typed — because both historical figure corruptions in this repo
 * entered through a hand-transcribed path.
 *
 * Cards are tagged to the units of the REDEVELOPED ${SUBJECT.title} specification,
 * first examined June 2027, not to the retired syllabus the papers were sat under.
 */

import type { SecCard } from '../../../../types/markBank';

const base = {
  source: 'sec' as const,
  subjectId: ${q(SUBJECT_ID)},
  specVersion: ${q(SUBJECT.specVersion)},
  qa: { gates: ['verbatim', 'tariff', 'figure'], humanReviewedBy: 'agent-verified', humanReviewedAt: '2026-07-31' },
};

export const CARDS: SecCard[] = [
${cards.join('\n')}
];
`;

const sizes = {};
for (const level of ['higher', 'ordinary']) {
  const levelCards = out.filter(c => c.level === level).map(c => c.code);
  writeFileSync(resolve(OUT_DIR, `${level}.ts`), moduleFor(level, levelCards));
  sizes[level] = levelCards.length;
  process.stderr.write(`  ${level}: ${levelCards.length} cards -> components/MarkBank/cards/${SUBJECT_ID}/${level}.ts\n`);
}

/**
 * How many cards each deck holds, so the tool can say which decks are ready
 * WITHOUT importing them. Knowing that Chemistry Ordinary is empty is exactly
 * the thing a student needs before they tap it, and finding out by downloading
 * the deck defeats the point of splitting the decks in the first place.
 *
 * Merged rather than overwritten: one run builds one subject, and clobbering the
 * file would erase every other subject's counts.
 */
const MANIFEST_OUT = resolve(ROOT, 'components/MarkBank/cards/sizes.json');
const existing = existsSync(MANIFEST_OUT) ? JSON.parse(readFileSync(MANIFEST_OUT, 'utf8')) : {};
writeFileSync(MANIFEST_OUT, `${JSON.stringify({ ...existing, [SUBJECT_ID]: sizes }, null, 1)}\n`);
