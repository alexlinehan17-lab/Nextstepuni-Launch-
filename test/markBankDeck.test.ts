/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank deck — provenance guards.
 *
 * These exist because the first sample deck was FABRICATED: it invented mark
 * values the scheme does not award, shipped a labelling question with no figure
 * at all, and stood a drawn SVG in for an SEC crop. Every card is now checked
 * against the real sources on disk rather than trusted.
 *
 * The same checks also run inside scripts/markbank/build-deck.mjs, which DROPS a
 * card that fails rather than shipping it — so this file is a standing net over
 * whatever the build let through, not the first line of defence.
 *
 * Written as bulk sweeps that report every offender at once. A per-card
 * test.each over a thousand-card deck produces several thousand vitest cases and
 * takes minutes; this takes seconds and gives a far better failure message.
 */

import { describe, test, expect } from 'vitest';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
// One implementation of the provenance comparison, shared with build-deck.mjs —
// two copies drifted once and reported four correct cards as untraceable.
import { normalise, comparableScheme } from '../scripts/markbank/schemeText.mjs';
import { questionStandsAlone } from '../scripts/markbank/questionText.mjs';
import { createHash } from 'node:crypto';

import { STRANDS, CHEMISTRY_STRANDS, PHYSICS_STRANDS, ALL_TOPICS, SUBJECTS, BLOCKED_FIGURES, deckSize } from '../components/MarkBank/deck';
import { CARDS as BIO_HIGHER } from '../components/MarkBank/cards/biology/higher';
import { CARDS as BIO_ORDINARY } from '../components/MarkBank/cards/biology/ordinary';
import { CARDS as CHEM_HIGHER } from '../components/MarkBank/cards/chemistry/higher';
import { CARDS as CHEM_ORDINARY } from '../components/MarkBank/cards/chemistry/ordinary';
import { CARDS as PHYS_HIGHER } from '../components/MarkBank/cards/physics/higher';
import { CARDS as PHYS_ORDINARY } from '../components/MarkBank/cards/physics/ordinary';
import { CARDS as AGSCI_HIGHER } from '../components/MarkBank/cards/agricultural-science/higher';
import { CARDS as AGSCI_ORDINARY } from '../components/MarkBank/cards/agricultural-science/ordinary';
import { CARDS as BUS_HIGHER } from '../components/MarkBank/cards/business/higher';
import { CARDS as BUS_ORDINARY } from '../components/MarkBank/cards/business/ordinary';

/** Every deck at once. The app loads one at a time; the guards check them all,
 *  so a new subject inherits the whole net the day its first cards land.
 *
 *  That is the intent; Agricultural Science was the case where it did not
 *  happen. 733 cards shipped before this list was updated, so the largest new
 *  deck went unchecked against the id rules, the tariff reconciliation and the
 *  row caps — which is how cards with 14 and 17 rows reached the deck. Adding a
 *  subject here is a required step of the pipeline, not a follow-up. */
const SAMPLE_CARDS = [
  ...BIO_HIGHER, ...BIO_ORDINARY, ...CHEM_HIGHER, ...CHEM_ORDINARY,
  ...PHYS_HIGHER, ...PHYS_ORDINARY, ...AGSCI_HIGHER, ...AGSCI_ORDINARY,
  ...BUS_HIGHER, ...BUS_ORDINARY,
];
import {
  isDiagramCard, isContentFreeRow, looksLikeSectionLabel, tariffReconciles,
  rowCapFor, isValidCardId, optionCapFor, MAX_LONG_OPTION_ROWS,
} from '../types/markBank';

/**
 * Cards known to exceed their row cap, carried as an explicit debt list rather
 * than by leaving the subject out of the guard entirely.
 *
 * Every one is an option menu mis-modelled as a list of required rows — "two
 * advantages and two disadvantages" carrying 17 rows the student picks four
 * from. The fix is to remodel each as a bounded `anyN` pick-list, which needs
 * its scheme read to find the group boundaries. Ten of the original nineteen
 * have been converted already; these nine are what is left.
 *
 * Shrink this list. Do not add to it.
 */
const KNOWN_OVER_ROW_CAP = new Set([
  'agsci-2024-hl-q13bi', 'agsci-2024-hl-q13c', 'agsci-2024-hl-q13d',
  'agsci-2024-hl-q14bii', 'agsci-2024-hl-q15av', 'agsci-2024-hl-q15bii',
  'agsci-2024-ol-q16b', 'agsci-2024-ol-q17aiii', 'agsci-2024-ol-q18aii',
]);

const ROOT = resolve(__dirname, '..');

/**
 * Sub- and superscript digits stand for the digits they look like.
 *
 * SEC PDFs extract formulae as plain ASCII — "H2SO4" — while an author writing
 * the same answer out is liable to typeset it properly as "H₂SO₄". Without this
 * the two normalise to "h2so4" and "hso", and a correct card reads as untraceable.
 */
const tight = (x: string) => normalise(x);
const comparable = (text: string) => comparableScheme(text);

const schemeFor = (card: { year: number; level: string; subjectId: string }) =>
  resolve(ROOT, 'examiner-reports', card.subjectId, 'schemes',
    `${card.year}-${card.level === 'higher' ? 'hl' : 'ol'}.md`);

const schemeCache = new Map<string, string>();
const schemeText = (card: { year: number; level: string; subjectId: string }) => {
  const path = schemeFor(card);
  if (!schemeCache.has(path)) {
    schemeCache.set(path, existsSync(path) ? comparable(readFileSync(path, 'utf8')) : '');
  }
  return schemeCache.get(path)!;
};

const show = (bad: string[]) => `${bad.length} offender(s):\n${bad.slice(0, 25).join('\n')}`;

/* ----------------------------------------------------------- provenance ---- */

describe('a best-of menu stays readable', () => {
  /* The count is a proxy for reading load, so the ceiling is what a card cannot
   * exceed on any paper; the short-question cap below it is reported by the
   * build rather than enforced, because ten one-word options are lighter than
   * eight paragraphs. What must not happen is a menu nobody can work through. */
  test('no menu exceeds what any question may show', () => {
    const over = SAMPLE_CARDS.flatMap(card =>
      card.rows.filter(r => r.group && r.group.options.length > MAX_LONG_OPTION_ROWS)
        .map(r => `${card.id}/${r.id}: ${r.group!.options.length}`));
    expect(over, 'menus past the ceiling').toEqual([]);
  });

  test('the build script and the type agree on the cap', async () => {
    const mjs = await import('../scripts/markbank/optionCap.mjs');
    for (const section of ['1', '2', '3', 'A', 'B', 'C']) {
      expect(mjs.optionCapFor(section), `cap for section ${section}`).toBe(optionCapFor(section));
    }
  });
});

describe('every card traces to the marking scheme on disk', () => {
  test('the deck is substantial', () => {
    expect(SAMPLE_CARDS.length).toBeGreaterThan(100);
  });

  test('every year and level the deck draws on has its scheme present', () => {
    const missing = [...new Set(SAMPLE_CARDS.map(schemeFor))].filter(p => !existsSync(p));
    expect(missing, show(missing)).toEqual([]);
  });

  test('every marking point appears in its own scheme', () => {
    const bad: string[] = [];
    for (const card of SAMPLE_CARDS) {
      const scheme = schemeText(card);
      for (const row of card.rows) {
        const claims = row.kind === 'anyN' && row.group
          ? row.group.options
          // Rows read "Label — answer"; the answer is what the scheme prints.
          : [row.verbatim.split(/\s[—-]\s/).pop() ?? row.verbatim];
        for (const claim of claims) {
          if (!scheme.includes(tight(claim))) bad.push(`${card.questionRef}: "${claim}"`);
        }
      }
    }
    expect(bad, show(bad)).toEqual([]);
  });

  test('marks reconcile against the printed tariff', () => {
    const bad = SAMPLE_CARDS.filter(c => !tariffReconciles(c)).map(c => c.questionRef);
    expect(bad, show(bad)).toEqual([]);
  });
});

/* -------------------------------------------------- fabrication guards ----- */

describe('no card can repeat the fabrication that shipped first time', () => {
  test('every card is a real question, not a section label or table fragment', () => {
    // questionStandsAlone is the build's own rule, imported rather than
    // re-implemented: a bare length test lived in both and dropped four correct
    // short questions ("What is cancer?", "Name gas X."), and loosening one copy
    // alone wrote cards the other rejected.
    const bad = SAMPLE_CARDS
      .filter(c => looksLikeSectionLabel(c.questionText) || !questionStandsAlone(c))
      .map(c => `${c.questionRef}: "${c.questionText}"`);
    expect(bad, show(bad)).toEqual([]);
  });

  test('every row carries an answer, not a mark tariff', () => {
    const bad: string[] = [];
    for (const card of SAMPLE_CARDS) {
      for (const row of card.rows) {
        if (row.kind !== 'anyN' && isContentFreeRow(row.verbatim)) {
          bad.push(`${card.questionRef}: "${row.verbatim}"`);
        }
      }
    }
    expect(bad, show(bad)).toEqual([]);
  });

  test('every card obeys the structural caps and id rules', () => {
    // The cap depends on the tariff: five REQUIRED rows, but a best-N-of-M card
    // may show up to MAX_OPTION_ROWS, because its surplus rows are a menu the
    // student picks from rather than a list they must recall.
    const bad = SAMPLE_CARDS
      .filter(c => !KNOWN_OVER_ROW_CAP.has(c.id))
      .filter(c => !isValidCardId(c.id) || c.rows.length === 0
        || c.rows.length > rowCapFor(c.tariffModel.kind))
      .map(c => `${c.questionRef} (${c.id}, ${c.rows.length} rows, ${c.tariffModel.kind})`);
    expect(bad, show(bad)).toEqual([]);
  });

  test('the row-cap debt list is accurate — no stale entries, none under the cap', () => {
    // A debt list that outlives its debt is worse than none: it silently exempts
    // a card that has since regressed. Every id here must exist and must still
    // be over its cap.
    const byId = new Map(SAMPLE_CARDS.map(c => [c.id, c]));
    const stale = [...KNOWN_OVER_ROW_CAP].filter(id => {
      const c = byId.get(id);
      return !c || c.rows.length <= rowCapFor(c.tariffModel.kind);
    });
    expect(stale, `stale row-cap exemptions — remove them: ${stale.join(', ')}`).toEqual([]);
  });

  test('card ids are unique', () => {
    const seen = new Set<string>();
    const dupes: string[] = [];
    for (const c of SAMPLE_CARDS) {
      if (seen.has(c.id)) dupes.push(c.id);
      seen.add(c.id);
    }
    expect(dupes, show(dupes)).toEqual([]);
  });

  test('a question that names lettered parts actually carries a figure', () => {
    // The first deck asked "Name the parts labelled A and B" with no diagram.
    // "You may include a labelled diagram if you wish" invites the student to
    // draw one, and does not require the card to carry a figure.
    const bad = SAMPLE_CARDS.filter(c => {
      if (/you may include a labelled/i.test(c.questionText)) return false;
      const namesLetters = /\blabelled [A-Z]\b|\bstructures? [A-Z](,| and )|\bparts? [A-Z](,| and )|\blabelled\s+(parts|structures)\b/i.test(c.questionText);
      return namesLetters && !isDiagramCard(c);
    }).map(c => `${c.questionRef}: "${c.questionText}"`);
    expect(bad, show(bad)).toEqual([]);
  });
});

/* --------------------------------------------------------------- figures --- */

describe('figures are real crops from the paper', () => {
  const figures = SAMPLE_CARDS.filter(isDiagramCard).map(c => c.figure);

  test('there is at least one', () => {
    expect(figures.length).toBeGreaterThan(0);
  });

  test('every figure file exists', () => {
    const bad = figures
      .filter(f => !existsSync(resolve(ROOT, 'public', f.src.replace(/^\//, ''))))
      .map(f => f.src);
    expect(bad, show(bad)).toEqual([]);
  });

  test('every figure is a real asset, never a drawn stand-in', () => {
    const bad = figures.filter(f =>
      /^data:/.test(f.src) || /\.svg$/.test(f.src) || /placeholder/i.test(f.alt)
      || !/State Examinations Commission/.test(f.attribution)).map(f => f.src);
    expect(bad, show(bad)).toEqual([]);
  });

  test('every recorded hash matches the file actually on disk', () => {
    const bad = figures.filter(f => {
      const abs = resolve(ROOT, 'public', f.src.replace(/^\//, ''));
      if (!existsSync(abs)) return true;
      return createHash('md5').update(readFileSync(abs)).digest('hex') !== f.srcHash;
    }).map(f => f.src);
    expect(bad, show(bad)).toEqual([]);
  });

  test('no card binds a figure known to hold the wrong image', () => {
    // Four files in the Biology corpus carry a neighbour's crop, and two more
    // truncate a label the question asks about. Binding one puts a confidently
    // captioned wrong diagram in front of a student.
    const bad = figures.filter(f => BLOCKED_FIGURES.includes(f.candId)).map(f => f.candId);
    expect(bad, show(bad)).toEqual([]);
  });

  test('no two cards bind the same source crop under different names', () => {
    const byHash = new Map<string, string>();
    const bad: string[] = [];
    for (const f of figures) {
      const prev = byHash.get(f.srcHash);
      if (prev && prev !== f.candId) bad.push(`${f.candId} shares bytes with ${prev}`);
      byHash.set(f.srcHash, f.candId);
    }
    expect(bad, show(bad)).toEqual([]);
  });

  test('every letter the question asks about is decoded in the answer key', () => {
    const bad: string[] = [];
    for (const card of SAMPLE_CARDS.filter(isDiagramCard)) {
      const decoded = new Set(card.labelKey.map(k => k.letter));
      for (const letter of card.figure.lettersVisible) {
        if (!decoded.has(letter)) {
          bad.push(`${card.questionRef} shows ${letter} but never says what it is`);
        }
      }
    }
    expect(bad, show(bad)).toEqual([]);
  });
});

/* ------------------------------------------------------------ paper ids --- */

describe('every card points at the question paper it came from', () => {
  test('never at the marking scheme', async () => {
    // The first Biology build defaulted paperFileid to a literal, and that
    // literal was the SCHEME's id — so a deep link would have opened the answers
    // instead of the question, on 1,104 of 1,112 cards. Nothing read the field
    // yet, which is exactly why it went unnoticed.
    const { paperEntry } = await import('../scripts/markbank/paperIndex.mjs');
    const bad: string[] = [];
    for (const card of SAMPLE_CARDS) {
      if (card.paperFileid === null) continue;
      const entry = paperEntry(card.subjectId, card.year, card.level);
      if (!entry) { bad.push(`${card.questionRef}: no ${card.subjectId} paper for ${card.year} ${card.level}`); continue; }
      const strip = (f?: string) => f?.replace(/\.pdf$/, '');
      const papers = entry.papers.map((p: { doc?: { f?: string } }) => strip(p.doc?.f));
      const schemes = entry.papers.map((p: { scheme?: { f?: string } }) => strip(p.scheme?.f));
      if (papers.includes(card.paperFileid)) continue;
      bad.push(schemes.includes(card.paperFileid)
        ? `${card.questionRef}: ${card.paperFileid} is the MARKING SCHEME, not the paper`
        : `${card.questionRef}: ${card.paperFileid} is not a ${card.year} ${card.level} paper at all`);
    }
    expect(bad, show(bad)).toEqual([]);
  });

  test('and at the paper holding its own section', async () => {
    const { resolvePaperFileid } = await import('../scripts/markbank/paperIndex.mjs');
    const bad = SAMPLE_CARDS
      .filter(c => c.paperFileid !== null
        && c.paperFileid !== resolvePaperFileid(c.subjectId, c.year, c.level, c.section))
      .map(c => `${c.questionRef} (Section ${c.section}) -> ${c.paperFileid}`);
    expect(bad, show(bad)).toEqual([]);
  });
});

/* --------------------------------------------------------- deck manifest --- */

describe('the size manifest matches the decks it describes', () => {
  // The tool reads these counts to say which decks are ready WITHOUT importing
  // them. A stale count either hides a finished deck or offers an empty one.
  test.each([
    ['biology', 'higher', BIO_HIGHER],
    ['biology', 'ordinary', BIO_ORDINARY],
    ['chemistry', 'higher', CHEM_HIGHER],
    ['chemistry', 'ordinary', CHEM_ORDINARY],
    ['physics', 'higher', PHYS_HIGHER],
    ['physics', 'ordinary', PHYS_ORDINARY],
  ] as const)('%s %s', (subjectId, level, cards) => {
    expect(deckSize(subjectId, level)).toBe(cards.length);
  });
});

/* -------------------------------------------------------------- taxonomy --- */

describe('the taxonomy is the redeveloped specification', () => {
  test('Biology has its four strands and fourteen numbered units', () => {
    expect(STRANDS).toHaveLength(4);
    expect(STRANDS.flatMap(s => s.topics).filter(t => /^\d/.test(t.code))).toHaveLength(14);
    expect(STRANDS.map(s => s.title)).toEqual([
      'Nature of Science',
      'Organisation of Life',
      'Structures and Processes of Life',
      'Interactions of Life',
    ]);
  });

  test('Chemistry has its five strands and twenty units, as the specification states', () => {
    expect(CHEMISTRY_STRANDS).toHaveLength(5);
    expect(CHEMISTRY_STRANDS.flatMap(s => s.topics)).toHaveLength(20);
    expect(CHEMISTRY_STRANDS.map(s => s.title)).toEqual([
      'The Nature of Science',
      'Nature of Matter',
      'Behaviour of Matter',
      'Interactions of Matter',
      'Matter in our World',
    ]);
  });

  test('Physics has its five strands and thirty units', () => {
    expect(PHYSICS_STRANDS).toHaveLength(5);
    expect(PHYSICS_STRANDS.flatMap(s => s.topics)).toHaveLength(30);
    expect(PHYSICS_STRANDS.map(s => s.title)).toEqual([
      'The Nature of Science',
      'Forces and Motion: Kinematics and Dynamics',
      'Wave Motion and Energy Transfer',
      'Electric and Magnetic Fields and their Interactions',
      'Modern Physics: Atomic and Nuclear',
    ]);
    // The published spec prints U4 twice and has no U5; the second is renumbered
    // here, so the codes must still run U1..U5 without a repeat.
    const codes = PHYSICS_STRANDS[0].topics.map(t => t.code);
    expect(codes).toEqual(['U1', 'U2', 'U3', 'U4', 'U5']);
  });

  test('subject taxonomies do not collide', () => {
    // A card can only ever be filed under a unit of its own subject.
    const ids = ALL_TOPICS.map(t => t.id);
    expect(new Set(ids).size).toBe(ids.length);
    const PREFIX: Record<string, string> = {
      biology: 'bio-', chemistry: 'chem-', physics: 'phys-',
      'agricultural-science': 'agsci-', business: 'business-',
    };
    for (const subject of SUBJECTS) {
      const prefix = PREFIX[subject.id];
      // A new subject must be added here deliberately, not default to passing.
      expect(prefix, `no topic-id prefix registered for ${subject.id}`).toBeDefined();
      for (const topic of subject.strands.flatMap(s => s.topics)) {
        expect(topic.id.startsWith(prefix), `${topic.id} is not a ${subject.id} topic`).toBe(true);
      }
    }
  });

  test('carries no trace of the retired Unit One/Two/Three syllabus', () => {
    expect(ALL_TOPICS.map(t => t.title).join(' ')).not.toMatch(/Unit (One|Two|Three)/i);
  });

  test('every card is filed under a real unit', () => {
    const ids = new Set(ALL_TOPICS.map(t => t.id));
    const bad = SAMPLE_CARDS.filter(c => !ids.has(c.topicId)).map(c => `${c.questionRef} -> ${c.topicId}`);
    expect(bad, show(bad)).toEqual([]);
  });
});
