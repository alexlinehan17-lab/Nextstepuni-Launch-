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
import { normalise, comparableScheme, claimMatches } from './schemeText.mjs';
import { optionCapFor, MAX_LONG_OPTION_ROWS } from './optionCap.mjs';
import { isContentFreeRow } from './contentFree.mjs';
import { questionStandsAlone } from './questionText.mjs';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

/** Per-subject facts the generated module needs. Adding a subject means adding
 *  a row here, and nothing else in this script changes. */
const SUBJECTS = {
  maths: {
    title: 'Mathematics',
    /* The syllabus examined from 2015. Its redevelopment is scheduled but not
     * yet examined, so there is nothing later to tag against. */
    specVersion: 'lc-maths-2015',
    specNote: 'Cards are tagged to the strands of the Mathematics syllabus examined from 2015.\n * Higher and Ordinary sit two papers, and a citation names which.',
    figureDir: 'public/exam-figures/maths',
    blocked: new Set(),
  },
  'construction-studies': {
    title: 'Construction Studies',
    /* The syllabus these papers were actually sat under. Its replacement,
     * Construction Technology, is first examined 2028, so unlike the science
     * subjects there is no redeveloped specification to tag against and the
     * cards are filed where a student revising them is actually studying. */
    specVersion: 'lc-construction-studies-syllabus',
    specNote: 'Cards are tagged to the sections of the Construction Studies syllabus these\n * papers were sat under. Construction Technology replaces it from 2028.',
    figureDir: 'public/exam-figures/construction-studies',
    blocked: new Set(),
  },
  biology: {
    title: 'Biology',
    specVersion: 'lc-biology-2002',
    specNote: 'Cards are tagged to the units of the REDEVELOPED Biology specification, first\n * examined June 2027, not to the syllabus the 2021-2025 papers were sat under.',
    figureDir: 'public/exam-figures/biology',
    /** Crops that hold a neighbour's image, or truncate a label the question
     *  asks about. Never bindable. Mirrors BLOCKED_FIGURES in deck.ts. */
    blocked: new Set([
      'alveolus-gas-exchange', 'lymphocyte', 'shoulder-joint', 'neuron',
      'root-longitudinal-section', 'cell-membrane',
    ]),
  },
  physics: {
    title: 'Physics',
    /* The syllabus examined before the 2027 redevelopment, named by what it is
     * rather than by a year — its publication year is unverified here, and an
     * unverified date in a provenance field is worse than none. */
    specVersion: 'lc-physics-legacy',
    specNote: 'Cards are tagged to the units of the REDEVELOPED Physics specification, first\n * examined June 2027, not to the syllabus the 2021-2025 papers were sat under.',
    figureDir: 'public/exam-figures/physics',
    blocked: new Set(),
  },
  chemistry: {
    title: 'Chemistry',
    /* The syllabus examined before the 2027 redevelopment. Named by what it is
     * rather than by a year, because I have not verified its publication year
     * and an unverified date in a provenance field is worse than none. */
    specVersion: 'lc-chemistry-legacy',
    specNote: 'Cards are tagged to the units of the REDEVELOPED Chemistry specification, first\n * examined June 2027, not to the syllabus the 2021-2025 papers were sat under.',
    figureDir: 'public/exam-figures/chemistry',
    blocked: new Set(),
  },
  business: {
    title: 'Business',
    /* The 1999 syllabus, still examined. Named by year because it is verified:
     * every paper in the corpus (2021-2025) sits on it. */
    specVersion: 'lc-business-1999',
    specNote: 'Cards are tagged to the units of the REDEVELOPED Business specification, first\n * examined June 2027, not to the syllabus the 2021-2025 papers were sat under.',
    figureDir: 'public/exam-figures/business',
    blocked: new Set(),
  },
  'home-economics': {
    title: 'Home Economics',
    /* The syllabus examined before the 2027 redevelopment. Named by what it is
     * rather than by a year, because its publication year is unverified here. */
    specVersion: 'lc-home-economics-legacy',
    specNote: 'Cards are tagged to the areas of the Scientific and Social syllabus, which is the\n * one these papers were sat under and the one still being sat: the NCCA schedule\n * introduces a replacement in 2027 for first examination in 2029.',
    figureDir: 'public/exam-figures/home-economics',
    blocked: new Set(),
  },
  economics: {
    title: 'Economics',
    /* The NCCA specification published February 2019 and first examined in 2021
     * — dated because it IS verified: every paper in the corpus (2021-2025) sits
     * on it, with no syllabus change to straddle. */
    specVersion: 'lc-economics-2019',
    specNote: 'Cards are tagged to the strands of the specification the papers were actually sat\n * under. Economics was first examined on it in 2021, so the whole 2021-2025\n * corpus sits on one syllabus with nothing to straddle.',
    figureDir: 'public/exam-figures/economics',
    blocked: new Set(),
  },
  'agricultural-science': {
    title: 'Agricultural Science',
    /* The NCCA specification published 2019 and first examined in 2021 — dated
     * here because it IS verified: every paper in the corpus (2021-2025) sits on
     * it, with no syllabus change to straddle. */
    specVersion: 'lc-agricultural-science-2019',
    specNote: 'Cards are tagged to the strands of the specification the papers were actually sat\n * under: this one has been the examined specification since 2021.',
    figureDir: 'public/exam-figures/agricultural-science',
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

function schemeFor(subjectId, card) {
  const stem = `${card.year ?? 2025}-${(card.level ?? 'higher') === 'higher' ? 'hl' : 'ol'}`;
  const file = resolve(ROOT, 'examiner-reports', subjectId, 'schemes', `${stem}.md`);
  if (!schemeCache.has(file)) {
    const raw = existsSync(file) ? readFileSync(file, 'utf8') : '';
    schemeCache.set(file, comparableScheme(raw));
  }
  return schemeCache.get(file);
}

/**
 * Row kinds the deck's own type accepts.
 *
 * Nothing validated this, and it showed: the authored Home Economics file had
 * drifted to kinds ("required", "explain") that are not in RowKind, which the
 * build happily emitted and typecheck then rejected — after the deck had been
 * written. Caught here the card is dropped with a reason instead.
 * Mirrors RowKind in types/markBank.ts.
 */
/** The glyph a broken subset font left behind, if the card still shows one.
 *
 * Word embeds its fonts as subsets whose ToUnicode map is wrong, so a scheme's
 * text layer spells "tan" in Oriya and "Certificate" as "CerƟficate".
 * derive_glyphs.py repairs what it can prove; this refuses to ship the rest.
 * A card that reads "h^(ᇱᇱ)(x)" where the scheme prints "h''(x)" is not a
 * smaller version of the right card, it is the wrong one, and it went out
 * looking poor because nothing was checking. Greek is genuinely Greek here,
 * and the two combining marks carry p-hat and z-bar. */
const REAL = /[\u0370-\u03FF\u0302\u0305\u02B0-\u02FF]/;
const BROKEN = /[\u0100-\u1FFF\uE000-\uF8FF\uFB00-\uFB4F]/g;
/** Undo a subset font's broken ToUnicode map, using the table derived from the
 * schemes themselves by scripts/markbank/authoring/derive_glyphs.py. Applied
 * here as well as at authoring time so every subject benefits from a re-derived
 * table on its next build, without ten reader scripts each having to know. */
const GLYPHS = JSON.parse(readFileSync(
  resolve(ROOT, 'scripts/markbank/authoring/glyphmap.json'), 'utf8'));

function repairText(text) {
  if (typeof text !== 'string' || !BROKEN.test(text)) return text;
  BROKEN.lastIndex = 0;
  return [...text].map(ch => GLYPHS[ch] ?? ch).join('');
}

/* Every string on the card, not a list of the fields that were mangled the
 * last time someone looked. Naming them missed contextNote, which is where the
 * business deck kept its "the word set as GiOen is often" asides -- text that
 * exists only because the mangling was not being repaired. Ids and keys are
 * ASCII, so walking them costs a failed regex test and changes nothing. */
function walkStrings(node, fn) {
  if (Array.isArray(node)) {
    node.forEach((v, i) => {
      if (typeof v === 'string') node[i] = fn(v);
      else if (v && typeof v === 'object') walkStrings(v, fn);
    });
  } else if (node && typeof node === 'object') {
    for (const k of Object.keys(node)) {
      const v = node[k];
      if (typeof v === 'string') node[k] = fn(v);
      else if (v && typeof v === 'object') walkStrings(v, fn);
    }
  }
}

function repairGlyphs(card) { walkStrings(card, repairText); }

function brokenGlyphs(text) {
  const hits = (text.match(BROKEN) ?? []).filter(ch => !REAL.test(ch));
  if (!hits.length) return null;
  const uniq = [...new Set(hits)];
  return `${hits.length} unreadable glyph(s) from a broken font subset, e.g. `
    + uniq.slice(0, 4).map(ch => `U+${ch.codePointAt(0).toString(16).toUpperCase().padStart(4, '0')}`).join(' ');
}

function mangledText(card) {
  const seen = [];
  walkStrings(card, (v) => { seen.push(v); return v; });
  return brokenGlyphs(seen.join(' '));
}

const ROW_KINDS = new Set(['point', 'alt', 'allOf', 'anyN', 'criterion', 'gate']);

function badRowKind(c) {
  for (const r of c.rows) {
    if (!ROW_KINDS.has(r.kind)) {
      return `row "${r.id}" has kind "${r.kind}", which is not one of ${[...ROW_KINDS].join(', ')}`;
    }
  }
  return null;
}

/** Text that is a table fragment or a header rather than an answerable question. */
function badQuestion(text, card) {
  const t = String(text).trim();
  if (!questionStandsAlone(card)) return 'question text is too short to stand alone';
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
  // Mirrors groupMarks() in types/markBank.ts: a descending tariff pays its
  // steps, not claimMax times one value.
  const worth = (r) => (r.kind === 'anyN' && r.group
    ? (r.group.perOptionSteps
        ? r.group.perOptionSteps.slice(0, r.group.claimMax).reduce((n, m) => n + m, 0)
        : r.group.claimMax * r.group.perOption)
    : (r.marks ?? 0));
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
 * A tariff sentence standing where a marking point should be: "Any two rights,
 * 5 marks each (3 for the right + 2 for explaining it)".
 *
 * An anyN row's own verbatim is the one string the build does NOT check against
 * the scheme — the options carry the marking points, so the field looks free.
 * Twelve Business cards used it to restate the tariff, which the session never
 * renders, so the split it described reached nobody.
 */
const TARIFF_PROSE = /\bmarks? each\b|^\s*any (one|two|three|four|five|\d+)\b[^.]*\bmarks?\b/i;

/** Faults in a bounded pick-list that arithmetic can settle without an agent. */
function groupFault(c) {
  for (const r of c.rows) {
    if (r.kind !== 'anyN' || !r.group) continue;
    const g = r.group;
    if (g.options.length < g.claimMax) {
      return `row "${r.id}" lets a student claim ${g.claimMax} but lists ${g.options.length} option(s)`;
    }
    // The session prints "Any 2 of these — 7 marks each" from these two numbers,
    // so a group worth more than the question tells the student a false total.
    const groupWorth = g.perOptionSteps
      ? g.perOptionSteps.slice(0, g.claimMax).reduce((n, m) => n + m, 0)
      : g.claimMax * g.perOption;
    if (groupWorth > c.totalMarks) {
      return `row "${r.id}" offers ${groupWorth} marks on a ${c.totalMarks}-mark question`;
    }
    // A descending tariff must state exactly as many steps as it lets a student
    // claim, or the renderer pays the tail of a shorter list to nobody.
    if (g.perOptionSteps && g.perOptionSteps.length !== g.claimMax) {
      return `row "${r.id}" lists ${g.perOptionSteps.length} mark step(s) for ${g.claimMax} claimable option(s)`;
    }
    // Nothing enforced this before: rowCapFor() caps how many ROWS a card has,
    // and a menu's options live inside ONE row, so a group could list any number
    // at all. Ten Business groups had drifted past the cap unnoticed.
    //
    // Refused outright only past the LONG-question ceiling, which is a wall of
    // text on any paper. Between the short cap and that ceiling it is reported
    // instead of dropped: the count was only ever a proxy for reading load, and
    // ten one-word options ("pure", "solid", "soluble") are lighter than eight
    // paragraphs. Losing a working card to a proxy is the worse outcome.
    if (g.options.length > MAX_LONG_OPTION_ROWS) {
      return `row "${r.id}" shows ${g.options.length} options, past the ${MAX_LONG_OPTION_ROWS} any question may show`;
    }
    if (TARIFF_PROSE.test(r.verbatim ?? '')) {
      return `row "${r.id}" states its tariff where its marking point should be: "${r.verbatim}"`;
    }
  }
  return null;
}

/**
 * On a MATCHING card, a label marked "asked" must be one of the answers.
 *
 * LabelKeyPanel deliberately shows only the labels the question leaves alone —
 * repeating one the student is self-marking would give the row away. On a card
 * whose rows ARE the letters ("1. Merger — D"), a letter marked asked but
 * claimed by no row is the distractor the paper warns about, and flagging it
 * asked hides the only decoding of it the student would ever see.
 *
 * Narrow on purpose. Where the question names the label itself — "Identify the
 * structure located at B", answer "Silage (pit)" — the label is genuinely asked
 * and no row repeats it, which is why this only speaks up once some OTHER label
 * has been found in the rows.
 */
function relabelDistractors(c) {
  const keys = Array.isArray(c.labelKey) ? c.labelKey : [];
  if (!keys.length) return null;
  const body = c.rows.map(r => `${r.verbatim ?? ''} ${(r.group?.options ?? []).join(' ')}`).join(' ');
  const claimed = (k) => new RegExp(`(^|[^A-Za-z0-9])${k.letter.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}([^A-Za-z0-9]|$)`).test(body);
  if (!keys.some(claimed)) return null;   // not a matching card; the letters live in the question
  const orphan = keys.filter(k => k.askedInThisQuestion && !claimed(k));
  if (!orphan.length) return null;
  // Corrected rather than dropped. No row self-marks this letter, so showing it
  // in the panel gives nothing away — and losing the whole card over one flag
  // costs the student far more than the flag ever did.
  for (const k of orphan) k.askedInThisQuestion = false;
  return `${c.id}: ${orphan.map(k => `"${k.letter}"`).join(', ')} claimed by no row — shown in the label key instead of hidden`;
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
const repaired = [];
const overCap = [];
const seenId = new Set();
const seenHash = new Map();
let unresolvedPapers = 0;

for (const c of cards) {
  if (byQuestion.get(c.questionRef) !== c) {
    dropped.push(`${c.id}: superseded for ${c.questionRef} by a card carrying its figure`);
    continue;
  }
  if (seenId.has(c.id)) { dropped.push(`${c.id}: duplicate id`); continue; }

  const contentFree = c.rows.filter(r => r.kind !== 'anyN' && isContentFreeRow(r.verbatim));
  if (contentFree.length) {
    dropped.push(`${c.id}: ${contentFree.length} content-free row(s), e.g. "${contentFree[0].verbatim}"`);
    continue;
  }

  const badQ = badQuestion(c.questionText, c);
  if (badQ) { dropped.push(`${c.id}: ${badQ} — "${c.questionText}"`); continue; }

  const badTariff = tariffFault(c);
  if (badTariff) { dropped.push(`${c.id}: ${badTariff}`); continue; }

  const badGroup = groupFault(c);
  if (badGroup) { dropped.push(`${c.id}: ${badGroup}`); continue; }

  const relabelled = relabelDistractors(c);
  if (relabelled) repaired.push(relabelled);

  for (const r of c.rows) {
    const cap = optionCapFor(c.section);
    if (r.group && r.group.options.length > cap) {
      overCap.push(`${c.id}: row "${r.id}" shows ${r.group.options.length} options in section ${c.section}, over the ${cap} agreed for a short question`);
    }
  }

  /* A row id repeated inside one card is not cosmetic: rowId() keys the claims
   * map, so two rows sharing an id are one claim to the scorer — ticking either
   * credits both — and React collapses them to a single element. Seen in the
   * wild, so the build refuses it rather than the deck carrying it. */
  const rowIds = new Set();
  const dupeRow = c.rows.map(r => r.id).find(id => rowIds.has(id) || (rowIds.add(id), false));
  if (dupeRow) { dropped.push(`${c.id}: row id "${dupeRow}" appears twice`); continue; }

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

  const kindFault = badRowKind(c);
  if (kindFault) { dropped.push(`${c.id}: ${kindFault}`); continue; }

  // Every marking point must actually appear in its own scheme.
  const scheme = schemeFor(SUBJECT_ID, c);
  if (!scheme) { dropped.push(`${c.id}: no scheme on disk for ${c.year} ${c.level}`); continue; }
  const untraceable = [];
  for (const r of c.rows) {
    const claims = r.kind === 'anyN' && r.group ? r.group.options : [String(r.verbatim).split(/\s[—-]\s/).pop()];
    for (const claim of claims) {
      if (!claimMatches(scheme, claim)) untraceable.push(claim);
    }
  }
  if (untraceable.length) {
    dropped.push(`${c.id}: ${untraceable.length} marking point(s) not found in the ${c.year} ${c.level} scheme, e.g. "${String(untraceable[0]).slice(0, 60)}"`);
    continue;
  }

  /* Repaired after the provenance check, never before: the check reads the
   * scheme's own text layer, so a card matched against it must still be
   * spelled the way that layer spells things. What ships is the repaired
   * text, which is what the scheme actually PRINTS -- the mangling is the
   * PDF's broken ToUnicode map, not the examiner's writing. */
  repairGlyphs(c);
  const mangled = mangledText(c);
  if (mangled) { dropped.push(`${c.id}: ${mangled}`); continue; }

  let figure = null;
  let labelKey = null;
  if (c.figureKey) {
    const rec = figureRecord(c.figureKey);
    if (rec.error) { dropped.push(`${c.id}: ${rec.error}`); continue; }
    rec.alt = repairText(rec.alt ?? '');
    const figMangled = brokenGlyphs(rec.alt);
    if (figMangled) { dropped.push(`${c.id}: figure alt text — ${figMangled}`); continue; }
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
for (const r of repaired) process.stderr.write(`  REPAIRED ${r}\n`);
for (const o of overCap) process.stderr.write(`  OVER CAP ${o}\n`);
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
 * ${SUBJECT.specNote}
 */

import type { SecCard } from '../../../../types/markBank';
${cards.length ? `
const base = {
  source: 'sec' as const,
  subjectId: ${q(SUBJECT_ID)},
  specVersion: ${q(SUBJECT.specVersion)},
  qa: { gates: ['verbatim', 'tariff', 'figure'], humanReviewedBy: 'agent-verified', humanReviewedAt: '2026-07-31' },
};
` : ''}
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
