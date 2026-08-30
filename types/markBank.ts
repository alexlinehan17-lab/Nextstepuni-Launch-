/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — the card model.
 *
 * One card is a real SEC exam question in the examiner's own words, plus the
 * actual answer broken into the discrete points the examiner awards marks for.
 *
 * Every field here exists because of a specific way the tools this replaces
 * failed. Three in particular are worth stating outright, because the type is
 * what stops them recurring:
 *
 *  - **`questionText` is required and verbatim.** Answer Architect's card type
 *    had no question field at all, so its cards rendered a section header —
 *    literally "Section A short answer (10m)" — as the question. A card without
 *    a real question is now unrepresentable.
 *
 *  - **A diagram card cannot exist without its answer key.** Diagram Vault could
 *    not tell a student what the letters meant, because its type had no field
 *    that could hold one. Here the diagram variant *requires* `labelKey`, so the
 *    compiler rejects a figure card that leaves a student guessing.
 *
 *  - **Figures bind by machine-emitted id, never a typed path.** Four Biology
 *    figures ship the wrong image today because a verifying agent hand-copied a
 *    crop path. `srcHash` exists so the build can fail when two cards claim the
 *    same source crop.
 *
 * Marking-scheme reproduction is licensed: rights are cleared for SEC papers and
 * marking schemes, and every card carries attribution.
 */

/**
 * Which SEC tariff convention governs a card.
 *
 * This is not over-engineering — a flat "one row, one mark value" model is
 * arithmetically wrong for a large share of the corpus, and would print totals
 * that disagree with the paper:
 *
 *  - `fixed` — each row carries its own stated marks. The only model that may
 *    render per-row mark chips and a mark-loss total.
 *  - `bestNofParts` — "Best five answers from (a)–(f)", six parts each printed 4:
 *    six rows × 4m displays 24 marks on a 20-mark question.
 *  - `orderedSplit` — "2(5) + 5(2)", where the scheme awards the first two
 *    correct answers 5 marks each and the rest 2. A point's value depends on how
 *    many the student got right, not which point it is, so per-row values do not
 *    exist and must not be invented.
 *
 * PARSED from the notation printed in the scheme. Never inferred, never defaulted.
 */
export type TariffModel =
  | { kind: 'fixed' }
  | { kind: 'bestNofParts'; answer: number; ofParts: number; perPart: number }
  | { kind: 'orderedSplit'; notation: string };

/**
 * What kind of thing one marking row is.
 *
 * `band` (tiered drawing rubrics such as "[Any one missing = 3] 6, 3, 0") is
 * deliberately ABSENT. Drawing and graph-shape cards are out of v1, and carrying
 * a variant no renderer handles is how a future authoring pass ships cards the
 * UI cannot display. Add it together with its renderer, not before.
 */
export type RowKind =
  /** One solidus-separated marking point. */
  | 'point'
  /** One point with alternatives the scheme itself prints ("saprophytic or heterotrophic"). */
  | 'alt'
  /** One mark for a complete set — all elements or nothing. */
  | 'allOf'
  /** A bounded group: "Any four 4(3)". */
  | 'anyN'
  /** A judgement rather than a phrase. Section B / practical work only. */
  | 'criterion'
  /** Asterisked in the scheme: only the exact scientific term scores, and adding
   *  a wrong answer alongside it cancels THIS row's mark. It carries its own real
   *  marks (the 2025 scheme awards "A: *Sporangium 1") and does not zero the rest
   *  of the question — each asterisked item stands or falls alone. */
  | 'gate';

export interface MarkRow {
  id: string;
  kind: RowKind;
  /**
   * The scheme's answer content, verbatim. This is the field Answer Architect's
   * authoring rule forbade — it kept only the mark tariff and deleted
   * "A: Bale wrapper / B: Stomach tube / C: Head gate" from a scheme that
   * printed it. A row whose text is a tariff rather than an answer is a defect.
   */
  verbatim: string;
  /**
   * Where the scheme relies on examiner training rather than printing the
   * requirement. The SEC's own worked example: a candidate who writes "Water is
   * drawn up the xylem by osmosis" has used two accepted terms and still scores
   * 3 of 6, because the statement is wrong. A tick list cannot see that, so the
   * requirement is spelled out on the row.
   */
  contextNote?: string;
  /** Marks for this row, exactly as the scheme awards them. `null` only when the
   *  tariff model leaves per-row values undefined — render no chip rather than a
   *  wrong one. */
  marks: number | null;
  /** Alternatives the scheme prints explicitly. */
  accepts?: string[];
  /**
   * The scheme's list ends in an ellipsis, meaning it is non-exhaustive. A
   * student who answered "cartilage" where the scheme listed "muscles or tendons
   * or ligament…" was correct, and must be able to say so.
   */
  openList?: boolean;
  /** Asterisked: exact term required, so synonym claiming is disabled. */
  exactTermRequired?: boolean;
  /**
   * Unclaimable until `dependsOn` is claimed — a "justify" mark is genuinely
   * unreachable if the structure it justifies was named wrongly.
   *
   * Set this ONLY where the scheme itself gates one mark on another. Where the
   * scheme simply lists two marks in sequence ("Name: Peristalsis 3 /
   * Description: … 3") they are independent, and inventing a dependency denies a
   * student a mark the examiner would have awarded.
   */
  dependsOn?: string;
  /**
   * Mutually exclusive answer routes, from the SEC's double solidus.
   *
   * Chemistry schemes use `//` where `/` means "equally acceptable": "a double
   * solidus separates answers which are mutually exclusive. A partial answer
   * from one side of the // may not be taken in conjunction with a partial
   * answer from the other side."
   *
   * So a question may accept two different complete routes to the answer, and a
   * student who takes points from both is not entitled to the marks. Rows
   * sharing a `route` belong to the same side; claiming any row commits the card
   * to that route and locks the others.
   */
  route?: string;
  /** `anyN` only: how many of the listed options may be claimed, and for how much. */
  group?: {
    claimMax: number;
    perOption: number;
    options: string[];
    /**
     * Descending per-option values, where the scheme does not pay the same for
     * every option claimed.
     *
     * Economics is built on this: "Discuss two economic consequences" prices the
     * first at 6 and the second at 4, and it is the commonest tariff on the
     * paper — four of the five long parts of one 2024 question. Without it the
     * choice was to state a per-option value that is wrong for one of the two,
     * or to card half of each question.
     *
     * When present it has exactly claimMax entries and supersedes perOption for
     * both scoring and display; perOption stays as the first step so anything
     * reading only that is never wrong by more than the tail.
     */
    perOptionSteps?: number[];
  };
}

/** What every letter on a figure means — including letters this question never asks
 *  about, so a student always leaves with the whole diagram decoded. */
export interface LabelKey {
  letter: string;
  meaning: string;
  askedInThisQuestion: boolean;
}

export interface CardFigure {
  /** Machine-emitted candidate id. The verifying agent may accept, reject or
   *  label it — never retype it. Both historical figure corruptions entered
   *  through a hand-authored string. */
  candId: string;
  src: string;
  /** Hash of the SOURCE crop. The build fails if two cards share one, which is
   *  what catches the four duplicated Biology figures. */
  srcHash: string;
  alt: string;
  /** Letters visible in the crop. Must be a superset of the letters the question
   *  asks about — the guard against a crop that cuts off a label being examined. */
  lettersVisible: string[];
  attribution: string;
  /** True when the crop IS the scheme's worked solution. A solution shown in
   *  the question area before reveal answers the question for the student, so
   *  the session screen holds these back until the scheme is revealed. */
  solution?: boolean;
  /** Named in the paper's acknowledgements, where a figure is third-party. */
  thirdPartyRights?: string;
}

/**
 * Printed material a student must read before answering a card.
 *
 * This is deliberately separate from `CardFigure`. A source passage can span
 * several pages and belongs on the QUESTION side of the reveal, whereas a
 * figure is one bounded image and may itself be a worked solution. The pages
 * are rendered from the real paper PDF already held by Paper Trail: no retyped
 * passage, no fabricated facsimile, and no second copy bundled into the app.
 */
export interface CardSourceMaterial {
  kind: 'source-text';
  /** The paper's own identity for the source, e.g. "TEXT 1". */
  label: string;
  /** Human title printed in the reader header. */
  title: string;
  /** One-based PDF pages, in reading order. */
  pages: number[];
  /** The author/publication acknowledgement printed by the SEC. */
  attribution: string;
  /** Clarifies that the displayed layout is the official examination version. */
  presentationNote: string;
}

/** Fields every card shares, whatever its provenance. */
interface CardBase {
  /** No dots: a dot is a Firestore field-path separator, and card ids are used as
   *  map keys in `updateDoc` paths. Enforced by `isValidCardId`. */
  id: string;
  subjectId: string;
  level: 'higher' | 'ordinary';
  /** PART-level curriculum id. A card may never inherit its parent question's
   *  tag — the alternative parts of one Section C question routinely span
   *  different topics, and inheriting would file bread mould under the
   *  breathing system. */
  topicId: string;
  /**
   * Level-independent concept identity, shared by an HL card and its OL sibling.
   * Costs one field now and cannot be retrofitted. Students drop from Higher to
   * Ordinary in spring, disproportionately in DEIS schools; without this, that
   * student opens an empty deck in March with every trace of a year's work gone.
   */
  conceptId: string;
}

/** A question card built from a real SEC paper and its marking scheme. */
export interface SecCardBase extends CardBase {
  source: 'sec';
  year: number;
  /**
   * SEC file id of the QUESTION PAPER, resolved from Paper Trail's harvested
   * index by the build script — never typed by an author. Null where that index
   * has no paper for the card's year and level; a guessed id is worse than none,
   * because the first Biology build defaulted this field to a literal that turned
   * out to be the marking SCHEME's id, which would have deep-linked a student
   * straight to the answers.
   *
   * Not unique on its own: the SEC reuses ids across years and disambiguates by
   * folder, so it identifies a paper only alongside subjectId, year and level.
   */
  paperFileid: string | null;
  /** The paper's own section. Lettered in the sciences, numbered in Business —
   *  whose Section 1 and Section 3 both count from Q1, which is why questionRef
   *  carries the section too. */
  section: 'A' | 'B' | 'C' | '1' | '2' | '3';
  /** Real paper numbering, e.g. "2025 HL Q6(a)–(b)". */
  questionRef: string;
  /** Optional lead-in the paper prints before the question proper. */
  stem?: string;
  /** Required reading carried by the question. It is available before reveal
   *  and is rendered page-for-page from `paperFileid`. */
  sourceMaterial?: CardSourceMaterial;
  /** Verbatim from the QUESTION PAPER — not the scheme. Required, always. */
  questionText: string;
  /** The tariff printed on the paper. Row marks must reconcile against this. */
  totalMarks: number;
  schemeCitation: string;
  /** Pixel escape hatch into the real scheme PDF, so any card can be checked
   *  against its source in one tap. Keeps faith with Paper Trail's charter. */
  schemeRegion?: { schemeFileid: string; p: number; r: [number, number, number, number] };
  /** Section B answers are AUTHORED, because the scheme prints content-free
   *  criteria there ("Control named and setup described"). Transcribing those
   *  mechanically is precisely how Answer Architect failed, so authored content
   *  is labelled and cited separately. */
  authored?: { sources: string[]; author: string; reviewedAt: string };
  specVersion: string;
  qa: { gates: string[]; humanReviewedBy: string; humanReviewedAt: string };
}

/**
 * The established exact-point assessment used by sciences, Business and the
 * other subjects whose schemes price identifiable answers.
 *
 * Kept out of `SecCardBase` deliberately: an English PCLM answer is not a bag
 * of binary marking points. Making every SEC card carry rows encouraged the
 * exact failure Mark Bank exists to prevent — turning non-exhaustive English
 * indicative material into a fabricated answer checklist.
 */
export interface SecPointCardBase extends SecCardBase {
  tariffModel: TariffModel;
  /** Capped at five REQUIRED rows: it keeps one card close to one memory, forces
   *  dependency splitting, and is what makes the card fit a 360px phone.
   *
   *  A best-N-of-M card is the one exception, capped at MAX_OPTION_ROWS instead.
   *  Its extra rows are a menu the student chooses from, not a list they must
   *  recall — "identify any four of these six breeds" shows six photographs
   *  because that is what the paper prints, and trimming to five would
   *  misrepresent the question rather than lighten it. */
  rows: MarkRow[];
}

export type PclmCriterionId = 'purpose' | 'coherence' | 'language' | 'mechanics';

/** One score family exactly as the SEC grade grid prints it. */
export interface PclmGradeBand {
  grade:
    | 'H1' | 'H2' | 'H3' | 'H4' | 'H5' | 'H6' | 'H7' | 'H8'
    | 'O1' | 'O2' | 'O3' | 'O4' | 'O5' | 'O6' | 'O7' | 'O8';
  /** Every mark the published grid permits in this band. */
  marks: number[];
}

export interface PclmCriterion {
  id: PclmCriterionId;
  label: string;
  maxMarks: number;
  /** SEC task-specific guidance, not an invented generic success criterion. */
  guidance: string[];
  /** Marks selectable on the published grade grid for this criterion. */
  permittedMarks: number[];
}

/** Shared identity for one separately marked part of a linked English question. */
interface PclmComponentBase {
  /** Stable within the card, e.g. `a`, `a-i` or `b`. */
  id: string;
  /** The paper's own part label. */
  label: string;
  totalMarks: number;
}

/** A short linked part which receives one mark on the SEC combined grid. */
export interface PclmCombinedComponent extends PclmComponentBase {
  mode: 'combined';
  bands: PclmGradeBand[];
  criteria: string[];
}

/** A substantial linked part which receives separate P, C, L and M marks. */
export interface PclmDiscreteComponent extends PclmComponentBase {
  mode: 'discrete';
  bands: PclmGradeBand[];
  criteria: PclmCriterion[];
  /** C and L may not exceed P within this component. */
  primacyOfPurpose: true;
}

export type PclmComponent = PclmCombinedComponent | PclmDiscreteComponent;

export type PclmAssessment =
  | {
      /** Short Paper 1 answers are judged as one combined mark. */
      mode: 'combined';
      bands: PclmGradeBand[];
      criteria: string[];
    }
  | {
      /** Longer responses receive separate P, C, L and M marks. */
      mode: 'discrete';
      bands: PclmGradeBand[];
      criteria: PclmCriterion[];
      /** C and L may not exceed P. */
      primacyOfPurpose: true;
    }
  | {
      /**
       * A selected question containing compulsory parts that the SEC marks on
       * separate grids.  A component can itself be combined (for example OL
       * Single Text Q1(a)) or discrete (for example the 40-mark part of an OL
       * Comparative question).  The parts stay together because later wording
       * often depends on an earlier choice, but their marks must never be
       * collapsed into a fabricated holistic total.
       */
      mode: 'composite';
      components: PclmComponent[];
    };

export interface PclmRubric {
  system: 'pclm';
  /** Things the printed task explicitly requires. They carry no marks alone. */
  taskRequirements: string[];
  assessment: PclmAssessment;
  /**
   * Examples the SEC gives examiners. Never rendered as claimable answers and
   * always accompanied by `indicativeMaterialNote`.
   */
  indicativeMaterial?: string[];
  indicativeMaterialNote: string;
}

/** A prose/short-answer SEC card. */
export interface SecQuestionCard extends SecPointCardBase {
  kind: 'question';
  figure?: CardFigure;
  /** The SEC's own print of the ask and its setup, cropped from the paper.
   *  Shown BEFORE the reveal — it is the question, never the answer — and it
   *  replaces the text stem for Maths, where retold stems attached the wrong
   *  part's context and flattened the typeset notation. */
  questionFigure?: CardFigure;
}

/**
 * A figure-labelling SEC card. `figure` and `labelKey` are both REQUIRED — this
 * is the type-level fix for the complaint that a diagram card never told the
 * student what its labels meant.
 */
export interface SecDiagramCard extends SecPointCardBase {
  kind: 'diagram';
  figure: CardFigure;
  labelKey: LabelKey[];
}

/**
 * A real SEC English question marked holistically with the published PCLM
 * grammar. This variant has a renderer and scoring path of its own; it does
 * not expose `rows`, so indicative examples cannot accidentally become binary
 * marks in some future consumer.
 */
export interface SecRubricCard extends SecCardBase {
  kind: 'rubric';
  rubric: PclmRubric;
}

/**
 * A card the student wrote themselves, migrated from Paper Trail's flashcard
 * deck. Those cards are the student's own words, so they carry no marking points
 * and no attribution, and they reveal in one flip rather than mark by mark. They
 * share the scheduler, and folding them in is what finally gives them a Firestore
 * mirror — today they live only in localStorage, so changing phone destroys them.
 */
export interface StudentCard extends CardBase {
  source: 'student';
  kind: 'own';
  front: string;
  back: string;
  addedTs: number;
}

export type MarkBankCard = SecQuestionCard | SecDiagramCard | SecRubricCard | StudentCard;
export type SecPointCard = SecQuestionCard | SecDiagramCard;
export type SecCard = SecPointCard | SecRubricCard;

export const isSecCard = (c: MarkBankCard): c is SecCard => c.source === 'sec';
export const isPointCard = (c: SecCard): c is SecPointCard => c.kind === 'question' || c.kind === 'diagram';
export const isRubricCard = (c: SecCard): c is SecRubricCard => c.kind === 'rubric';
export const isDiagramCard = (c: MarkBankCard): c is SecDiagramCard =>
  c.source === 'sec' && c.kind === 'diagram';

/** Max rows on one card when every row is required. See the note on `rows`. */
export const MAX_ROWS = 5;

/**
 * Max rows on a best-N-of-M card, where the surplus rows are options rather
 * than things to recall. Higher than MAX_ROWS because the cognitive load is a
 * choice, not a list — but still bounded: a 14-row menu for a 2-mark answer is
 * a wall of text, not a question.
 */
export const MAX_OPTION_ROWS = 8;

/**
 * The same menu on a LONG question, where eight is not enough.
 *
 * A Business Section 3 part asks for three essential elements of a valid
 * contract and the examiner prints nine; another lists thirteen. Cutting the
 * menu to eight does real harm: a student who wrote the ninth wrote a correct
 * answer the examiner would have paid for, and cannot find it to claim it.
 * openList softens that — they can record it as another valid point — but a
 * menu that omits answers the scheme states is misrepresenting the marking,
 * which is the one thing this tool exists not to do.
 *
 * Still bounded. Fourteen is the ceiling because no SEC long question in the
 * corpus prints more, not because fifteen would be unreadable.
 */
export const MAX_LONG_OPTION_ROWS = 14;

/** The row cap that actually applies to a card, given its tariff. */
export const rowCapFor = (kind: TariffModel['kind']): number =>
  kind === 'bestNofParts' ? MAX_OPTION_ROWS : MAX_ROWS;

/**
 * How many options one best-of menu may show.
 *
 * Keyed on the SECTION, not on what the part is worth. A long question's parts
 * are individually small — a Section 3 (c)(ii) can be 10 marks — but it is the
 * question they belong to that makes the examiner print a long menu, and a
 * mark-value threshold cuts exactly the cards this cap was raised for.
 *
 * Long-question sections: Business Section 3 at Higher and Section 2 at
 * Ordinary (there is no ABQ at Ordinary); Sections B and C in the sciences.
 */
const LONG_SECTIONS = new Set(['2', '3', 'B', 'C']);
export const optionCapFor = (section: string): number =>
  LONG_SECTIONS.has(section) ? MAX_LONG_OPTION_ROWS : MAX_OPTION_ROWS;

/**
 * Card ids are used as Firestore map keys inside dotted `updateDoc` paths, so a
 * dot in an id would silently write to the wrong nested field.
 */
export function isValidCardId(id: string): boolean {
  return id.length > 0 && !id.includes('.') && !id.includes('/') && !id.includes('__');
}

/** Stable id for a row, falling back to its index. */
export function rowId(row: Pick<MarkRow, 'id'>, index: number): string {
  return row.id || `r${index}`;
}

/**
 * Text that looks like a section header or a bare tariff rather than a question.
 * This is the exact shape that shipped as a card's question 24 times in one
 * subject file, so it is a named, tested predicate rather than a comment.
 */
export function looksLikeSectionLabel(text: string): boolean {
  const t = text.trim();
  if (!t) return true;
  return /^section\s+[abc]\b/i.test(t)
    || /^(short|long)\s+answer/i.test(t)
    || /^\(?\d+\s*m(arks)?\)?\.?$/i.test(t)
    || /^question\s+\d+\.?$/i.test(t);
}

/**
 * A marking row that states only what the marks are worth, with no answer in it.
 * These are the rows that made Answer Architect unusable; ~32% of Section B
 * scheme rows read this way, which is why Section B content is authored.
 *
 * The build applies the same rule from `scripts/markbank/contentFree.mjs`, which
 * carries the reasoning behind each opening. This copy exists because app code
 * must not import out of scripts/; `test/markBankContentFree.test.ts` asserts
 * the two stay identical. They HAD drifted — the build knew "matching result"
 * and "description how" while this did not, and this knew "Three points, 2 marks
 * each" while the build did not — so a row of either shape would have been
 * written by a build that accepted it into a suite that rejected it.
 */
export function isContentFreeRow(verbatim: string): boolean {
  const t = verbatim.trim().toLowerCase();
  if (!t) return true;
  if (/^\d+\s*(items?|points?|answers?)?[,\s]*\d*\s*marks?\s*(each)?\.?$/.test(t)) return true;
  // "correct position" bare is a criterion; "Correct position of leaf (or leaf
  // disc) on lid" names the thing and where it goes, which is the recallable
  // content of that experiment. The SEC writes the criterion bare and names the
  // thing when it wants it named, so "of" is the distinction.
  return /^(named piece of apparatus( used)?|control named( and setup described)?|safety precaution described|correct (sketch|matching result)|correct position(?! of )|suitable (time|temperature|volume)|left for a (suitable )?time|any correct|the description earns|description how|matching result)/.test(t)
    || /^(two|three|four|five|six)\s+(items?|points?|answers?)\b.*\bmarks?\b/.test(t);
}

/**
 * Do a card's row marks reconcile against the tariff printed on the paper?
 *
 * `fixed` must sum exactly. `bestNofParts` sums only the claimable subset, which
 * is what catches six rows × 4m displaying 24 marks on a 20-mark question.
 * `orderedSplit` cannot be checked, because the scheme does not define per-row
 * values — so we assert the rows carry none rather than pretending.
 */
/** What one bounded group is worth when fully claimed. */
export function groupMarks(g: { claimMax: number; perOption: number; perOptionSteps?: number[] }): number {
  return g.perOptionSteps
    ? g.perOptionSteps.slice(0, g.claimMax).reduce((n, m) => n + m, 0)
    : g.claimMax * g.perOption;
}

export function tariffReconciles(card: SecCard): boolean {
  if (isRubricCard(card)) {
    const { assessment } = card.rubric;
    const bandsReconcile = (bands: PclmGradeBand[], total: number) => {
      const marks = bands.flatMap(band => band.marks);
      return marks.length > 0
        && Math.min(...marks) === 0
        && Math.max(...marks) === total
        && new Set(marks).size === marks.length;
    };
    if (assessment.mode === 'combined') {
      return bandsReconcile(assessment.bands, card.totalMarks);
    }
    if (assessment.mode === 'composite') {
      const criteriaReconcile = (criteria: PclmCriterion[], total: number) =>
        criteria.reduce((sum, criterion) => sum + criterion.maxMarks, 0) === total
        && criteria.every(criterion =>
          criterion.permittedMarks.length > 0
          && Math.min(...criterion.permittedMarks) === 0
          && Math.max(...criterion.permittedMarks) === criterion.maxMarks
          && new Set(criterion.permittedMarks).size === criterion.permittedMarks.length);
      return assessment.components.length > 0
        && new Set(assessment.components.map(component => component.id)).size
          === assessment.components.length
        && assessment.components.reduce((sum, component) => sum + component.totalMarks, 0)
          === card.totalMarks
        && assessment.components.every(component =>
          bandsReconcile(component.bands, component.totalMarks)
          && (component.mode === 'combined'
            || criteriaReconcile(component.criteria, component.totalMarks)));
    }
    const max = assessment.criteria.reduce((sum, criterion) => sum + criterion.maxMarks, 0);
    return max === card.totalMarks
      && assessment.criteria.every(criterion =>
        criterion.permittedMarks.length > 0
        && Math.min(...criterion.permittedMarks) === 0
        && Math.max(...criterion.permittedMarks) === criterion.maxMarks
        && new Set(criterion.permittedMarks).size === criterion.permittedMarks.length);
  }
  const { tariffModel: t, rows, totalMarks } = card;
  if (t.kind === 'orderedSplit') return rows.every(r => r.marks === null);
  if (t.kind === 'bestNofParts') return t.answer * t.perPart === totalMarks;
  // Asterisked rows count: the asterisk constrains the wording, not the value.
  const worth = (r: MarkRow) =>
    r.kind === 'anyN' && r.group ? groupMarks(r.group) : (r.marks ?? 0);
  // Mutually exclusive routes are counted ONCE, and each must reach the tariff on
  // its own — a student takes one route or the other, never a total of both.
  const byRoute = new Map<string, number>();
  let common = 0;
  for (const r of rows) {
    if (!r.route) common += worth(r);
    else byRoute.set(r.route, (byRoute.get(r.route) ?? 0) + worth(r));
  }
  if (!byRoute.size) return common === totalMarks;
  return [...byRoute.values()].every(n => common + n === totalMarks);
}
