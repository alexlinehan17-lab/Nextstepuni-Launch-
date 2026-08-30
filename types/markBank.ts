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
 *  - `questionTotal` — the scheme prices the QUESTION and states its points
 *    without printing how those marks divide across its parts. Computer Science
 *    Section A does this throughout: a five-mark question prints (a) and (b),
 *    and the scheme answers each without ever saying what either is worth.
 *    A card citing the question can state the total and the points; it cannot
 *    state a split, and it must not present the parts' separate answers as
 *    ALTERNATIVES to one another — "five marks for any one of these" is a claim
 *    the scheme never made and, for a question whose parts ask different
 *    things, is false.
 *
 * PARSED from the notation printed in the scheme. Never inferred, never defaulted.
 */
export type TariffModel =
  | { kind: 'fixed' }
  | { kind: 'bestNofParts'; answer: number; ofParts: number; perPart: number }
  | { kind: 'orderedSplit'; notation: string }
  | { kind: 'questionTotal' };

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
  /** Verbatim from the QUESTION PAPER — not the scheme. Required, always. */
  questionText: string;
  tariffModel: TariffModel;
  /** The tariff printed on the paper. Row marks must reconcile against this. */
  totalMarks: number;
  /** Capped at five REQUIRED rows: it keeps one card close to one memory, forces
   *  dependency splitting, and is what makes the card fit a 360px phone.
   *
   *  A best-N-of-M card is the one exception, capped at MAX_OPTION_ROWS instead.
   *  Its extra rows are a menu the student chooses from, not a list they must
   *  recall — "identify any four of these six breeds" shows six photographs
   *  because that is what the paper prints, and trimming to five would
   *  misrepresent the question rather than lighten it. */
  rows: MarkRow[];
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

/** A prose/short-answer SEC card. */
export interface SecQuestionCard extends SecCardBase {
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
export interface SecDiagramCard extends SecCardBase {
  kind: 'diagram';
  figure: CardFigure;
  labelKey: LabelKey[];
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

export type MarkBankCard = SecQuestionCard | SecDiagramCard | StudentCard;
export type SecCard = SecQuestionCard | SecDiagramCard;

export const isSecCard = (c: MarkBankCard): c is SecCard => c.source === 'sec';
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
 * `orderedSplit` and `questionTotal` cannot be checked, because the scheme does
 * not define per-row values — so we assert the rows carry none rather than
 * pretending.
 */
/** What one bounded group is worth when fully claimed. */
export function groupMarks(g: { claimMax: number; perOption: number; perOptionSteps?: number[] }): number {
  return g.perOptionSteps
    ? g.perOptionSteps.slice(0, g.claimMax).reduce((n, m) => n + m, 0)
    : g.claimMax * g.perOption;
}

export function tariffReconciles(card: SecCard): boolean {
  const { tariffModel: t, rows, totalMarks } = card;
  if (t.kind === 'orderedSplit' || t.kind === 'questionTotal') {
    return rows.every(r => r.marks === null);
  }
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
