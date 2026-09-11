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
import { comparableScheme, claimMatches } from '../scripts/markbank/schemeText.mjs';
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
import { CARDS as HE_HIGHER } from '../components/MarkBank/cards/home-economics/higher';
import { CARDS as HE_ORDINARY } from '../components/MarkBank/cards/home-economics/ordinary';
import { CARDS as ECON_HIGHER } from '../components/MarkBank/cards/economics/higher';
import { CARDS as ECON_ORDINARY } from '../components/MarkBank/cards/economics/ordinary';
import { CARDS as CONS_HIGHER } from '../components/MarkBank/cards/construction-studies/higher';
import { CARDS as CONS_ORDINARY } from '../components/MarkBank/cards/construction-studies/ordinary';
import { CARDS as MATHS_HIGHER } from '../components/MarkBank/cards/maths/higher';
import { CARDS as MATHS_ORDINARY } from '../components/MarkBank/cards/maths/ordinary';
import { CARDS as ENGLISH_HIGHER } from '../components/MarkBank/cards/english/higher';
import { CARDS as ENGLISH_ORDINARY } from '../components/MarkBank/cards/english/ordinary';
import { CARDS as IRISH_HIGHER } from '../components/MarkBank/cards/irish/higher';
import { CARDS as IRISH_ORDINARY } from '../components/MarkBank/cards/irish/ordinary';
import { CARDS as ART_HIGHER } from '../components/MarkBank/cards/art/higher';
import { CARDS as ART_ORDINARY } from '../components/MarkBank/cards/art/ordinary';
import { CARDS as GEOGRAPHY_HIGHER } from '../components/MarkBank/cards/geography/higher';
import { CARDS as GEOGRAPHY_ORDINARY } from '../components/MarkBank/cards/geography/ordinary';
import { CARDS as CS_HIGHER } from '../components/MarkBank/cards/computer-science/higher';
import { CARDS as CS_ORDINARY } from '../components/MarkBank/cards/computer-science/ordinary';
import { CARDS as ENG_HIGHER } from '../components/MarkBank/cards/engineering/higher';
import { CARDS as ENG_ORDINARY } from '../components/MarkBank/cards/engineering/ordinary';
import { CARDS as HISTORY_HIGHER } from '../components/MarkBank/cards/history/higher';
import { CARDS as HISTORY_ORDINARY } from '../components/MarkBank/cards/history/ordinary';
import { CARDS as RE_HIGHER } from '../components/MarkBank/cards/religious-education/higher';
import { CARDS as RE_ORDINARY } from '../components/MarkBank/cards/religious-education/ordinary';
import { CARDS as LCVP_COMMON } from '../components/MarkBank/cards/lcvp/common';
import { CARDS as FRENCH_HIGHER } from '../components/MarkBank/cards/french/higher';
import { CARDS as FRENCH_ORDINARY } from '../components/MarkBank/cards/french/ordinary';
import { CARDS as GERMAN_HIGHER } from '../components/MarkBank/cards/german/higher';
import { CARDS as GERMAN_ORDINARY } from '../components/MarkBank/cards/german/ordinary';
import { CARDS as ITALIAN_HIGHER } from '../components/MarkBank/cards/italian/higher';
import { CARDS as ITALIAN_ORDINARY } from '../components/MarkBank/cards/italian/ordinary';
import { CARDS as RUSSIAN_HIGHER } from '../components/MarkBank/cards/russian/higher';
import { CARDS as RUSSIAN_ORDINARY } from '../components/MarkBank/cards/russian/ordinary';
import { CARDS as TECH_HIGHER } from '../components/MarkBank/cards/technology/higher';
import { CARDS as TECH_ORDINARY } from '../components/MarkBank/cards/technology/ordinary';
import { CARDS as JAPANESE_HIGHER } from '../components/MarkBank/cards/japanese/higher';
import { CARDS as JAPANESE_ORDINARY } from '../components/MarkBank/cards/japanese/ordinary';
import { CARDS as POLISH_HIGHER } from '../components/MarkBank/cards/polish/higher';
import { CARDS as POLISH_ORDINARY } from '../components/MarkBank/cards/polish/ordinary';
import { CARDS as PORTUGUESE_HIGHER } from '../components/MarkBank/cards/portuguese/higher';
import { CARDS as PORTUGUESE_ORDINARY } from '../components/MarkBank/cards/portuguese/ordinary';
import { CARDS as ROMANIAN_HIGHER } from '../components/MarkBank/cards/romanian/higher';
import { CARDS as DUTCH_HIGHER } from '../components/MarkBank/cards/dutch/higher';
import { CARDS as LITHUANIAN_HIGHER } from '../components/MarkBank/cards/lithuanian/higher';
import { CARDS as LITHUANIAN_ORDINARY } from '../components/MarkBank/cards/lithuanian/ordinary';
import { CARDS as LATVIAN_HIGHER } from '../components/MarkBank/cards/latvian/higher';
import { CARDS as CZECH_HIGHER } from '../components/MarkBank/cards/czech/higher';
import { CARDS as HUNGARIAN_HIGHER } from '../components/MarkBank/cards/hungarian/higher';
import { CARDS as BULGARIAN_HIGHER } from '../components/MarkBank/cards/bulgarian/higher';
import { CARDS as SLOVAKIAN_HIGHER } from '../components/MarkBank/cards/slovakian/higher';
import { CARDS as SWEDISH_HIGHER } from '../components/MarkBank/cards/swedish/higher';
import { CARDS as ESTONIAN_HIGHER } from '../components/MarkBank/cards/estonian/higher';
import { CARDS as FINNISH_HIGHER } from '../components/MarkBank/cards/finnish/higher';
import { CARDS as CROATIAN_HIGHER } from '../components/MarkBank/cards/croatian/higher';
import { CARDS as DANISH_HIGHER } from '../components/MarkBank/cards/danish/higher';
import { CARDS as SLOVENIAN_HIGHER } from '../components/MarkBank/cards/slovenian/higher';
import { CARDS as ARABIC_HIGHER } from '../components/MarkBank/cards/arabic/higher';
import { CARDS as ARABIC_ORDINARY } from '../components/MarkBank/cards/arabic/ordinary';
import { CARDS as AM_HIGHER } from '../components/MarkBank/cards/applied-maths/higher';
import { CARDS as AM_ORDINARY } from '../components/MarkBank/cards/applied-maths/ordinary';
import { CARDS as CLAS_HIGHER } from '../components/MarkBank/cards/classical-studies/higher';
import { CARDS as CLAS_ORDINARY } from '../components/MarkBank/cards/classical-studies/ordinary';
import { CARDS as LATIN_HIGHER } from '../components/MarkBank/cards/latin/higher';
import { CARDS as LATIN_ORDINARY } from '../components/MarkBank/cards/latin/ordinary';
import { CARDS as AGREEK_HIGHER } from '../components/MarkBank/cards/ancient-greek/higher';
import { CARDS as AGREEK_ORDINARY } from '../components/MarkBank/cards/ancient-greek/ordinary';
import { CARDS as MGREEK_HIGHER } from '../components/MarkBank/cards/modern-greek/higher';
import { CARDS as MANDARIN_HIGHER } from '../components/MarkBank/cards/mandarin-chinese/higher';
import { CARDS as MANDARIN_ORDINARY } from '../components/MarkBank/cards/mandarin-chinese/ordinary';
import { CARDS as UKRAINIAN_HIGHER } from '../components/MarkBank/cards/ukrainian/higher';
import { CARDS as DCG_HIGHER } from '../components/MarkBank/cards/dcg/higher';
import { CARDS as DCG_ORDINARY } from '../components/MarkBank/cards/dcg/ordinary';

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
  ...BUS_HIGHER, ...BUS_ORDINARY, ...HE_HIGHER, ...HE_ORDINARY,
  ...ECON_HIGHER, ...ECON_ORDINARY, ...CONS_HIGHER, ...CONS_ORDINARY,
  ...MATHS_HIGHER, ...MATHS_ORDINARY, ...ENGLISH_HIGHER, ...ENGLISH_ORDINARY,
  ...IRISH_HIGHER, ...IRISH_ORDINARY,
  ...ART_HIGHER, ...ART_ORDINARY,
  ...GEOGRAPHY_HIGHER, ...GEOGRAPHY_ORDINARY,
  ...CS_HIGHER, ...CS_ORDINARY, ...ENG_HIGHER, ...ENG_ORDINARY,
  ...RE_HIGHER, ...RE_ORDINARY,
  ...HISTORY_HIGHER, ...HISTORY_ORDINARY,
  ...ITALIAN_HIGHER, ...ITALIAN_ORDINARY,
  ...RUSSIAN_HIGHER, ...RUSSIAN_ORDINARY,
  ...JAPANESE_HIGHER, ...JAPANESE_ORDINARY,
  ...POLISH_HIGHER, ...POLISH_ORDINARY,
  ...LITHUANIAN_HIGHER, ...LITHUANIAN_ORDINARY,
  ...LATVIAN_HIGHER, ...CZECH_HIGHER,
  ...CLAS_HIGHER, ...CLAS_ORDINARY,
  ...LATIN_HIGHER, ...LATIN_ORDINARY,
  ...ARABIC_HIGHER, ...ARABIC_ORDINARY,
  ...AGREEK_HIGHER, ...AGREEK_ORDINARY,
  // Higher only: Modern Greek is examined at ONE level and there is no
  // Ordinary paper in any year of the corpus.
  ...MGREEK_HIGHER,
  ...MANDARIN_HIGHER, ...MANDARIN_ORDINARY,
  // Higher only: Maltese and Ukrainian are each examined at ONE level and
  // there is no Ordinary paper in any year of the corpus.
  ...UKRAINIAN_HIGHER,
  ...DCG_HIGHER, ...DCG_ORDINARY,
];
import {
  isDiagramCard, isContentFreeRow, isPointCard, looksLikeSectionLabel, tariffReconciles,
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
  'agsci-2024-hl-q15av', 'agsci-2024-ol-q16b', 'agsci-2024-ol-q17aiii',
]);

const ROOT = resolve(__dirname, '..');

/**
 * Sub- and superscript digits stand for the digits they look like.
 *
 * SEC PDFs extract formulae as plain ASCII — "H2SO4" — while an author writing
 * the same answer out is liable to typeset it properly as "H₂SO₄". Without this
 * the two normalise to "h2so4" and "hso", and a correct card reads as untraceable.
 *
 * claimMatches() is the whole comparison, imported rather than rebuilt here: it
 * also compares around the "tt" an SEC font prints as a single t ("pipete").
 */
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
    const over = SAMPLE_CARDS.filter(isPointCard).flatMap(card =>
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

  /* Sixty seconds, not the thirty every other test gets. This one walks EVERY
   * card in the bank against a document read off disk, so its cost grows with
   * the bank: adding Polish — the twenty-fourth subject, 238 cards and nine
   * more scheme files — pushed it past thirty seconds under the full suite's
   * parallel load, while it still finishes in fourteen on its own. Raising the
   * ceiling for the two whole-bank tests keeps the global thirty in place for
   * everything else, where a test that runs long really is hung. */
  test('every marking point appears in its own scheme', () => {
    const bad: string[] = [];
    for (const card of SAMPLE_CARDS.filter(isPointCard)) {
      const scheme = schemeText(card);
      for (const row of card.rows) {
        const claims = row.kind === 'anyN' && row.group
          ? row.group.options
          // Rows read "Label — answer"; the answer is what the scheme prints.
          : [row.verbatim.split(/\s[—-]\s/).pop() ?? row.verbatim];
        for (const claim of claims) {
          if (!claimMatches(scheme, claim)) bad.push(`${card.questionRef}: "${claim}"`);
        }
      }
    }
    expect(bad, show(bad)).toEqual([]);
    // Its own timeout, because its work grows with the whole bank: every
    // marking row of every card is searched for inside its own scheme's text.
    // At 15,600 cards it runs a little over the 30s default, and a timeout
    // here reads as a provenance failure when it is only a big bank.
  }, 180_000);

  test('marks reconcile against the printed tariff', () => {
    const bad = SAMPLE_CARDS.filter(c => !tariffReconciles(c)).map(c => c.questionRef);
    expect(bad, show(bad)).toEqual([]);
  });
});

describe('reviewed Construction Studies boundaries stay on their printed tasks', () => {
  test('2017 HL Q4(a) marks three functional requirements, not Q4(b) wall comparisons', () => {
    const card = CONS_HIGHER.find(candidate => candidate.id === 'cons-2017-hl-q4-a');
    expect(card).toBeDefined();
    expect(card && isPointCard(card)).toBe(true);
    if (!card || !isPointCard(card)) return;

    expect(card.totalMarks).toBe(24);
    expect(card.rows).toHaveLength(1);
    expect(card.rows[0].group).toMatchObject({ claimMax: 3, perOption: 8 });
    expect(card.rows[0].group?.options).toHaveLength(16);
    expect(card.rows[0].group?.options.join(' ')).not.toMatch(/Concrete block wall|Positives|Negatives/);
  });

  test('2017 OL Q9(c) remains the ten-mark patio question', () => {
    const card = CONS_ORDINARY.find(candidate => candidate.id === 'cons-2017-ol-q9-c');
    expect(card).toBeDefined();
    expect(card && isPointCard(card)).toBe(true);
    if (!card || !isPointCard(card)) return;

    expect(card.totalMarks).toBe(10);
    expect(card.questionText).toMatch(/external patio/i);
    expect(card.rows[0].group).toMatchObject({ claimMax: 2, perOption: 5 });
    expect(card.rows[0].group?.options).toHaveLength(8);
    expect(card.rows.map(row => row.verbatim).join(' ')).not.toMatch(/practical project|craft skills|portfolio/i);
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
    for (const card of SAMPLE_CARDS.filter(isPointCard)) {
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
    const bad = SAMPLE_CARDS.filter(isPointCard)
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
      return !c || !isPointCard(c) || c.rows.length <= rowCapFor(c.tariffModel.kind);
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
      const hasQuestionFigure = 'questionFigure' in c && Boolean(c.questionFigure);
      return namesLetters && !isDiagramCard(c) && !hasQuestionFigure && !c.sourceMaterial;
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
  test('required source material has a real paper and ordered page numbers', () => {
    const bad: string[] = [];
    for (const card of SAMPLE_CARDS) {
      const source = card.sourceMaterial;
      if (!source) continue;
      const pagesAreValid = source.pages.length > 0
        && source.pages.every(page => Number.isInteger(page) && page > 0)
        && new Set(source.pages).size === source.pages.length
        && source.pages.every((page, index) => index === 0 || page > source.pages[index - 1]);
      if (!card.paperFileid) bad.push(`${card.questionRef}: source pages have no question-paper file id`);
      if (!pagesAreValid) bad.push(`${card.questionRef}: invalid source pages ${JSON.stringify(source.pages)}`);
      if (!source.label.trim() || !source.title.trim() || !source.attribution.trim()) {
        bad.push(`${card.questionRef}: source identity or attribution is blank`);
      }
    }
    expect(bad, show(bad)).toEqual([]);
  });

  test('never at the marking scheme', async () => {
    // The first Biology build defaulted paperFileid to a literal, and that
    // literal was the SCHEME's id — so a deep link would have opened the answers
    // instead of the question, on 1,104 of 1,112 cards. Nothing read the field
    // yet, which is exactly why it went unnoticed.
    const { paperEntry, corpusSubjectFor } =
      await import('../scripts/markbank/paperIndex.mjs');
    const bad: string[] = [];
    for (const card of SAMPLE_CARDS) {
      if (card.paperFileid === null) continue;
      // History is sat in one of two FIELDS OF STUDY, printed as separate
      // papers under separate SEC subject codes; the citation names which,
      // and the corpus key follows it. Same helper the build uses.
      const entry = paperEntry(
        corpusSubjectFor(card.subjectId, card.questionRef), card.year, card.level);
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
    const { resolvePaperFileid, corpusSubjectFor } =
      await import('../scripts/markbank/paperIndex.mjs');
    const bad = SAMPLE_CARDS
      .filter(c => {
        // Maths uses A/B for marking-scheme tariff sections, while the source
        // documents are Paper 1 and Paper 2. Resolve from the explicit paper
        // number exactly as build-deck does; never reinterpret B as Paper 2.
        const sourceSection = c.subjectId === 'maths'
          ? c.questionRef.match(/\bPaper\s+([12])\b/i)?.[1] ?? c.section
          : c.section;
        return c.paperFileid !== null
          && c.paperFileid !== resolvePaperFileid(
            corpusSubjectFor(c.subjectId, c.questionRef),
            c.year, c.level, sourceSection);
      })
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
    ['agricultural-science', 'higher', AGSCI_HIGHER],
    ['agricultural-science', 'ordinary', AGSCI_ORDINARY],
    ['business', 'higher', BUS_HIGHER],
    ['business', 'ordinary', BUS_ORDINARY],
    ['home-economics', 'higher', HE_HIGHER],
    ['home-economics', 'ordinary', HE_ORDINARY],
    ['economics', 'higher', ECON_HIGHER],
    ['economics', 'ordinary', ECON_ORDINARY],
    ['construction-studies', 'higher', CONS_HIGHER],
    ['construction-studies', 'ordinary', CONS_ORDINARY],
    ['maths', 'higher', MATHS_HIGHER],
    ['maths', 'ordinary', MATHS_ORDINARY],
    ['english', 'higher', ENGLISH_HIGHER],
    ['english', 'ordinary', ENGLISH_ORDINARY],
    ['irish', 'higher', IRISH_HIGHER],
    ['irish', 'ordinary', IRISH_ORDINARY],
    ['art', 'higher', ART_HIGHER],
    ['art', 'ordinary', ART_ORDINARY],
    ['geography', 'higher', GEOGRAPHY_HIGHER],
    ['geography', 'ordinary', GEOGRAPHY_ORDINARY],
    ['computer-science', 'higher', CS_HIGHER],
    ['computer-science', 'ordinary', CS_ORDINARY],
    ['engineering', 'higher', ENG_HIGHER],
    ['engineering', 'ordinary', ENG_ORDINARY],
    ['history', 'higher', HISTORY_HIGHER],
    ['history', 'ordinary', HISTORY_ORDINARY],
    ['religious-education', 'higher', RE_HIGHER],
    ['religious-education', 'ordinary', RE_ORDINARY],
    // LCVP is examined at one level; there is no Higher/Ordinary pair to pin.
    ['lcvp', 'common', LCVP_COMMON],
    ['technology', 'higher', TECH_HIGHER],
    ['technology', 'ordinary', TECH_ORDINARY],
    ['french', 'higher', FRENCH_HIGHER],
    ['french', 'ordinary', FRENCH_ORDINARY],
    ['german', 'higher', GERMAN_HIGHER],
    ['german', 'ordinary', GERMAN_ORDINARY],
    ['italian', 'higher', ITALIAN_HIGHER],
    ['italian', 'ordinary', ITALIAN_ORDINARY],
    ['russian', 'higher', RUSSIAN_HIGHER],
    ['russian', 'ordinary', RUSSIAN_ORDINARY],
    ['japanese', 'higher', JAPANESE_HIGHER],
    ['japanese', 'ordinary', JAPANESE_ORDINARY],
    ['polish', 'higher', POLISH_HIGHER],
    ['polish', 'ordinary', POLISH_ORDINARY],
    ['portuguese', 'higher', PORTUGUESE_HIGHER],
    ['portuguese', 'ordinary', PORTUGUESE_ORDINARY],
    ['romanian', 'higher', ROMANIAN_HIGHER],
    ['dutch', 'higher', DUTCH_HIGHER],
    ['lithuanian', 'higher', LITHUANIAN_HIGHER],
    ['lithuanian', 'ordinary', LITHUANIAN_ORDINARY],
    ['latvian', 'higher', LATVIAN_HIGHER],
    ['czech', 'higher', CZECH_HIGHER],
    ['hungarian', 'higher', HUNGARIAN_HIGHER],
    ['bulgarian', 'higher', BULGARIAN_HIGHER],
    ['slovakian', 'higher', SLOVAKIAN_HIGHER],
    ['swedish', 'higher', SWEDISH_HIGHER],
    ['estonian', 'higher', ESTONIAN_HIGHER],
    ['finnish', 'higher', FINNISH_HIGHER],
    ['croatian', 'higher', CROATIAN_HIGHER],
    ['danish', 'higher', DANISH_HIGHER],
    ['slovenian', 'higher', SLOVENIAN_HIGHER],
    ['arabic', 'higher', ARABIC_HIGHER],
    ['arabic', 'ordinary', ARABIC_ORDINARY],
    ['applied-maths', 'higher', AM_HIGHER],
    ['applied-maths', 'ordinary', AM_ORDINARY],
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
      'home-economics': 'home-economics-', economics: 'economics-',
      'construction-studies': 'cons-',
      maths: 'maths-',
      english: 'english-',
      irish: 'irish-',
      art: 'art-',
      geography: 'geography-',
      'computer-science': 'cs-',
      engineering: 'eng-',
      history: 'hist-',
      'religious-education': 're-',
      lcvp: 'lcvp-',
      technology: 'tech-',
      // French files its cards under the published French taxonomy itself
      // (curriculum.ts -> curriculumRegistry.ts), so its ids carry the
      // subject's own name rather than an abbreviation.
      french: 'french-',
      // German files its cards under the published German taxonomy itself, for
      // the reason French does.
      german: 'german-',
      // Italian files its cards under the published Italian taxonomy itself
      // (curriculum.ts -> curriculumRegistry.ts), so its ids carry the
      // subject's own name rather than an abbreviation, as French's do.
      italian: 'italian-',
      // Japanese files its cards under the published Japanese taxonomy itself
      // (curriculum.ts -> curriculumRegistry.ts), as French and Italian do.
      japanese: 'japanese-',
      // Applied Maths files against the CANONICAL curriculum's own ids, which
      // are 'applied-mathematics-<strand>-<topic>' — the subject id in the
      // deck is the SEC's shorter name for the same subject.
      'applied-maths': 'applied-mathematics-',
      // Spanish files its cards under the published Spanish taxonomy itself
      // (curriculum.ts -> curriculumRegistry.ts), as French does, so its ids
      // carry the subject's own name rather than an abbreviation.
      spanish: 'spanish-',
      // Russian files its cards under the published Russian taxonomy itself
      // (curriculum.ts), as French does, so its ids carry the subject's own
      // name rather than an abbreviation.
      russian: 'russian-',
      polish: 'polish-',
      // Portuguese files its cards under the published Portuguese taxonomy
      // itself (curriculum.ts), as Polish does, so its ids carry the
      // subject's own name rather than an abbreviation.
      portuguese: 'portuguese-',
      // Romanian and Dutch file their cards under their own published
      // taxonomies (curriculum.ts), as Portuguese does.
      romanian: 'romanian-',
      dutch: 'dutch-',
      // Lithuanian files its cards under the published Lithuanian taxonomy
      // itself (curriculum.ts -> curriculumRegistry.ts), as Polish does.
      lithuanian: 'lithuanian-',
      // Latvian and Czech file their cards under their own published
      // taxonomies, as Lithuanian and Polish do.
      latvian: 'latvian-',
      czech: 'czech-',
      hungarian: 'hungarian-',
      bulgarian: 'bulgarian-',
      slovakian: 'slovakian-',
      swedish: 'swedish-',
      estonian: 'estonian-',
      finnish: 'finnish-',
      croatian: 'croatian-',
      danish: 'danish-',
      slovenian: 'slovenian-',
      // Classical Studies files its cards under the published Classical
      // Studies taxonomy itself, as French does — and under one further
      // strand, 'classical-studies-legacy-*', for the ten-topic syllabus the
      // 2021 and 2022 papers were sat on, which the canonical curriculum
      // (a description of the CURRENT specification) does not carry.
      'classical-studies': 'classical-studies-',
      // Latin files its cards under the published Latin taxonomy itself, as
      // French does. Its cards tag against one strand of it — 'latin-3-*',
      // the legacy written paper's task types — because that is the paper
      // every sitting in the bank was sat on; the other three strands ship
      // unused so a student sees the whole shape of the course.
      latin: 'latin-',
      // Arabic files its cards under the published Arabic taxonomy itself.
      arabic: 'arabic-',
      // Ancient Greek files its cards under the published Ancient Greek
      // taxonomy itself, as Latin does. Its cards tag against one strand of
      // it — 'ancient-greek-4-*', the legacy written paper's task types —
      // because that is the paper every sitting in the bank was sat on; the
      // other four strands ship unused so a student sees the whole course.
      'ancient-greek': 'ancient-greek-',
      // Modern Greek files its cards under the published Modern Greek
      // taxonomy itself, whose two strands are the paper's own two halves.
      'modern-greek': 'modern-greek-',
      // Mandarin Chinese files its cards under the published Mandarin Chinese
      // specification itself. Cards tag against one strand of it —
      // 'mandarin-chinese-3-*', the written paper's task types — because that
      // is what a written card can be about; the other three strands cover
      // the oral, the portfolio and the course's competences and ship unused.
      'mandarin-chinese': 'mandarin-chinese-',
      // Maltese and Ukrainian file their cards under their own published
      // taxonomies, whose two strands are each paper's own two halves.
      ukrainian: 'ukrainian-',
      // Design & Communication Graphics files its cards under the published
      // DCG taxonomy itself (curriculum.ts -> curriculumRegistry.ts), as
      // Applied Maths does — the subject id in the deck is the abbreviation
      // the SEC prints on the paper and students use for the same subject.
      dcg: 'design-and-communication-graphics-',
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
