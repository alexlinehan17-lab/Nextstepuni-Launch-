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
  group?: { claimMax: number; perOption: number; options: string[] };
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
  section: 'A' | 'B' | 'C';
  /** Real paper numbering, e.g. "2025 HL Q6(a)–(b)". */
  questionRef: string;
  /** Optional lead-in the paper prints before the question proper. */
  stem?: string;
  /** Verbatim from the QUESTION PAPER — not the scheme. Required, always. */
  questionText: string;
  tariffModel: TariffModel;
  /** The tariff printed on the paper. Row marks must reconcile against this. */
  totalMarks: number;
  /** Capped at five: it keeps one card close to one memory, forces dependency
   *  splitting, and is what makes the card fit a 360px phone. */
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

/** Max rows on one card. See the note on `rows`. */
export const MAX_ROWS = 5;

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
 */
export function isContentFreeRow(verbatim: string): boolean {
  const t = verbatim.trim().toLowerCase();
  if (!t) return true;
  if (/^\d+\s*(items?|points?|answers?)?[,\s]*\d*\s*marks?\s*(each)?\.?$/.test(t)) return true;
  return /^(named piece of apparatus( used)?|control named( and setup described)?|safety precaution described|correct (sketch|matching result|position)|suitable (time|temperature|volume)|left for a (suitable )?time|any correct|the description earns)/.test(t)
    || /^(three|four|five|six|two)\s+(items?|points?|answers?)\b.*\bmarks?\b/.test(t);
}

/**
 * Do a card's row marks reconcile against the tariff printed on the paper?
 *
 * `fixed` must sum exactly. `bestNofParts` sums only the claimable subset, which
 * is what catches six rows × 4m displaying 24 marks on a 20-mark question.
 * `orderedSplit` cannot be checked, because the scheme does not define per-row
 * values — so we assert the rows carry none rather than pretending.
 */
export function tariffReconciles(card: SecCard): boolean {
  const { tariffModel: t, rows, totalMarks } = card;
  if (t.kind === 'orderedSplit') return rows.every(r => r.marks === null);
  if (t.kind === 'bestNofParts') return t.answer * t.perPart === totalMarks;
  // Asterisked rows count: the asterisk constrains the wording, not the value.
  const worth = (r: MarkRow) =>
    r.kind === 'anyN' && r.group ? r.group.claimMax * r.group.perOption : (r.marks ?? 0);
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
