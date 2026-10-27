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

/** One priced component of a criterion row; see `MarkRow.parts`. */
export interface MarkRowPart {
  id: string;
  /** The component as the scheme prints it: "point", "discussion", "Scale". */
  verbatim: string;
  marks: number;
  /** Including zero and the part's maximum; the printed ladder where the scheme gives one. */
  permittedMarks: number[];
}

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
  /** Explicit partial-credit steps printed for one criterion, including zero
   * and its maximum. A diagram marked6/3/0 must not become a binary6-mark tick.
   * Only fixed-tariff criterion rows may use these; never inferred. */
  permittedMarks?: number[];
  /**
   * The named components a criterion row is priced in — "Design feature 1
   * (2 for point, 4 for discussion)" — each placed on its own marks, so a
   * student who had the point but not the discussion can say so. The row's
   * claim is the parts' sum. Only a fixed-tariff criterion row carries parts,
   * their marks add up to the row's, and every part is the scheme's own word
   * (cards/construction-studies: construction_rows.py).
   */
  parts?: MarkRowPart[];
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
     * Ordered per-option values, where the scheme does not pay the same for
     * every option claimed. Preserve their printed order: Agricultural Science
     * 2010 OL Q7 explicitly awards five 1s followed by five 3s.
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
  /** For question-side figures only. False means this is an illustration and
   * the written stem and prompt must remain visible. Omitted means the crop
   * contains the complete printed question and replaces that text. */
  includesPrompt?: boolean;
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
export interface SupplementaryReading {
  title: string;
  author: string;
  /** Preserve the edition's stanza and line breaks. */
  stanzas: string[][];
  edition: string;
  sourceUrl: string;
}

export interface LinkedReading {
  title: string;
  author: string;
  edition: string;
  /** Page-aware link to the publisher's reading copy, opened in a new tab. */
  sourceUrl: string;
  location: string;
}

export interface CardSourceMaterial {
  kind: 'source-text' | 'source-illustration' | 'source-data' | 'exam-material' | 'marking-scheme' | 'source-paper' | 'source-scheme' | 'source-table' | 'supplementary-text' | 'linked-reading';
  /** The paper's own identity for the source, e.g. "TEXT 1". */
  label: string;
  /** Human title printed in the reader header. */
  title: string;
  /** One-based PDF pages, in reading order; empty for supplementary texts. */
  pages: number[];
  /** Additional clockwise rotation for sideways material printed inside a
   * portrait page. Applied to the PDF viewport, preserving the source bytes. */
  pageRotations?: Record<number, 90 | 180 | 270>;
  /** Optional inspected crops, one per page; coordinates are PDF fractions. */
  regions?: Array<[number, number, number, number] | { p: number; r: [number, number, number, number]; rotate?: 0 | 90 | 180 | 270 }>;
  /** Attributed reading editions for named studied works absent from the paper. */
  texts?: SupplementaryReading[];
  /** Published reading copies for named studied works absent from this paper. */
  readings?: LinkedReading[];
  /**
   * A separate official SEC document when the required material is not inside
   * the question paper itself. Art publishes its illustrations as a companion
   * booklet; defaulting to `SecCardBase.paperFileid` would silently open the
   * wrong PDF. Omitted for passages that live in the question paper.
   */
  sourceFileid?: string;
  /** Examination year of a verified reading copy from another paper. */
  sourceYear?: number;
  /** The author/publication acknowledgement printed by the SEC. */
  attribution: string;
  /** Clarifies that the displayed layout is the official examination version. */
  presentationNote: string;
}

/**
 * A real recording required to answer a listening-comprehension card.
 *
 * Audio is deliberately modelled separately from a PDF source.  Treating the
 * listening booklet as if it were the source would leave the question looking
 * complete while withholding the one thing the student actually has to hear.
 * `playbackUrl` points at a verified mirror of the SEC recording; the canonical
 * SEC identity remains explicit so a mirror can be replaced without changing
 * the card or its progress history.
 */
export interface CardAudioMaterial {
  kind: 'source-audio';
  /** The paper's own section identity, e.g. "Cuid B · Comhrá a hAon". */
  label: string;
  title: string;
  /** Verified playback copy of the official recording. */
  playbackUrl: string;
  /** Stable filename published by the State Examinations Commission. */
  secFileid: string;
  /** Canonical SEC archive URL, retained even when its hot-link is gated. */
  canonicalUrl: string;
  attribution: string;
  presentationNote: string;
}

/** Fields every card shares, whatever its provenance. */
interface CardBase {
  /** No dots: a dot is a Firestore field-path separator, and card ids are used as
   *  map keys in `updateDoc` paths. Enforced by `isValidCardId`. */
  id: string;
  subjectId: string;
  /**
   * 'common' is not a third grade of difficulty. A handful of Leaving
   * Certificate subjects are examined at ONE level — LCVP's Link Modules is
   * one, and the SEC says so on the paper's own cover and in its file id
   * (LC462CLP000EV.pdf, level letter C). Filing such a deck under 'higher'
   * would make every card cite a Higher Level paper that does not exist, and
   * would hide it from a student whose profile says anything else.
   */
  level: 'higher' | 'ordinary' | 'common';
  /** PART-level curriculum id. A card may never inherit its parent question's
   *  tag — the alternative parts of one Section C question routinely span
   *  different topics, and inheriting would file bread mould under the
   *  breathing system. */
  topicId: string;
  /** Other canonical topics assessed by the same indivisible marked task.
   * Cross-list the existing card; never duplicate its identity or progress. */
  additionalTopicIds?: string[];
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
   *  carries the section too. Religious Education runs A-J: its paper is ten
   *  lettered sections inside three units, and eight of the ten number no
   *  question at all, so the section IS the address there.
   *
   *  German's sections are the paper's own TEXTS rather than letters or
   *  numbers: TEXT I, TEXT II and (at Ordinary) TEXT III each set a reading
   *  comprehension numbering its questions from 1, and Angewandte Grammatik
   *  sets a further pair of alternatives, so a bare question number addresses
   *  nothing and the section carries the address exactly as it does in
   *  Business.
   *
   *  Russian goes one step further and names the printed QUESTION, because it
   *  numbers "Question 1" three times in one sitting — once in Section I, once
   *  in Section II and once in the Listening Comprehension Test. C1 and C2 are
   *  Higher's two comprehensions, LA1, LA2 and CA1 its language- and
   *  cultural-awareness questions, IR1 and IR2 Ordinary's two retrieval texts
   *  and CD its comprehension. See UNIT_NAME in ru_scheme.py, which is where
   *  the same tokens are defined for the readers.
   *
   *  Classical Studies adds a TOPIC form for the syllabus examined to 2022.
   *  That paper prints no sections and no question numbers at all: ten topics,
   *  each setting questions "(i)" to "(iv)" with lettered parts under them, so
   *  the topic and the roman together are the address — "Topic 1(i)", cited as
   *  "2021 HL Topic 1(i) Q(a)". Its 2023 paper numbers Questions 1-16 straight
   *  through Sections A and B, and files under 'A' and 'B'.
   *
   *  Arabic adds '4'. Its paper prints four parts — الجزء الأول to الجزء
   *  الرابع — and numbers its questions 1 to 15 straight through them, so the
   *  part is not part of the address and never appears in a citation; it is
   *  what the card says a student is looking at. Part 4 is the composition,
   *  which is why the union needed a fourth number it had never had. */
  section: 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J'
  | '1' | '2' | '3' | '4' | 'T1' | 'T2' | 'T3' | 'AG' | 'C1' | 'C2' | 'CD'
  | 'IR1' | 'IR2' | 'LA1' | 'LA2' | 'CA1'
  // Latin's paper prints no lettered sections a card could be filed under:
  // it prints five QUESTIONS, and the "Section A"/"Section B" beneath three
  // of them is a CHOICE of routes through one question rather than a division
  // of the paper. So the section is the printed question — the unit a student
  // navigates by, and the unit each of the syllabus's task types belongs to.
  | 'Q1' | 'Q2' | 'Q3' | 'Q4' | 'Q5'
  // Lithuanian, Latvian and Czech print no lettered section a card could be
  // filed under either: "Dalis A" and "Dalis B" divide reading from writing
  // and nothing else, while the unit a student navigates by is the TASK —
  // "Pirma užduotis", "Antra užduotis" — one printed text with up to eleven
  // asks on it. So the section is that task, 'U1' to 'U3', and the old
  // examination's single-text I DALIS is 'U1'.
  | 'U1' | 'U2' | 'U3'
  | `Topic ${number}(${'i' | 'ii' | 'iii' | 'iv' | 'v'})`;
  /** Real paper numbering, e.g. "2025 HL Q6(a)–(b)". */
  questionRef: string;
  /** Optional lead-in the paper prints before the question proper. */
  stem?: string;
  /** Required reading carried by the question. It is available before reveal
   *  and is rendered page-for-page from `paperFileid`. */
  sourceMaterial?: CardSourceMaterial;
  /**
   * Further official documents needed beside `sourceMaterial`.
   *
   * Geography can require the printed question page, a separate OS map, and
   * its separate legend for one task. Keeping those as distinct SEC documents
   * avoids flattening or fabricating a composite while still putting every
   * required source on the question side of the reveal.
   */
  additionalSourceMaterials?: CardSourceMaterial[];
  /** Required listening recording, available on the question side. */
  audioMaterial?: CardAudioMaterial;
  /** Verbatim from the QUESTION PAPER — not the scheme. Required, always. */
  questionText: string;
  /** Names a separately priced task within a shared printed instruction. */
  practiceFocus?: string;
  /** Printed MCQ options, in paper order; no answer key is included here. */
  questionChoices?: string[];
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
  /** Exam-year registry identity; topicId remains the current practice filter. */
  specificationId?: string;
  curriculumNodeIds?: string[];
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
  /** Capped at six REQUIRED rows. Keep separately marked tasks split, while
   *  retaining all six marking groups in a published three-comparison route.
   *
   *  Menu-class tariffs are the exception — see rowCapFor. A best-N-of-M card
   *  is capped at MAX_OPTION_ROWS: its extra rows are a menu the student
   *  chooses from, not a list they must recall — "identify any four of these
   *  six breeds" shows six photographs because that is what the paper prints,
   *  and trimming to five would misrepresent the question rather than lighten
   *  it. orderedSplit and questionTotal rows are likewise the scheme's own
   *  printed candidates, bounded by the notation or the question total, and
   *  share the long-question ceiling. */
  rows: MarkRow[];
  /** A source-published whole-question bonus, assessed separately from tasks.
   * It is never silently credited: the student applies the printed rule. */
  questionBonus?: {
    id: string;
    kind: 'criterion';
    verbatim: string;
    contextNote: string;
    marks: number;
    permittedMarks: number[];
  };
  /** A complete finite assessment route assembled from separately practicable
   * tasks. Each group retains its source task, published maximum and up to five
   * marking rows. Groups partition the rows in display order. */
  taskGroups?: Array<{
    sourceCardId: string;
    label: string;
    marks: number;
    rowIds: string[];
    tariffModel?: { kind: 'orderedSplit'; notation: string };
    responseCounts?: number[];
  }>;
  /**
   * Official marking-scheme routes for an open printed choice.
   *
   * Some questions ask for one self-selected example (for example, one method
   * of cooking meat) and the scheme publishes a different set of points for
   * each accepted route. Those are not separate exam questions and must not be
   * scheduled as duplicate cards. The student selects the route they actually
   * answered before reveal, and only that route's rows are assessed.
   */
  answerVariants?: Array<{
    id: string;
    label: string;
    rows: MarkRow[];
  }>;
}

export type PclmCriterionId = 'purpose' | 'coherence' | 'language' | 'mechanics';

/**
 * Grade labels exactly as each year's SEC grid prints them: the modern H1–H8
 * and O1–O8 scales (2017 onward), the 2010–2016 Higher Level A+/B/C/D/E-
 * anchors, and the 2010–2016 Ordinary Level A–F and N/G (F/NG on the combined
 * grid) bands.
 */
export type PclmGradeLabel =
  | 'H1' | 'H2' | 'H3' | 'H4' | 'H5' | 'H6' | 'H7' | 'H8'
  | 'O1' | 'O2' | 'O3' | 'O4' | 'O5' | 'O6' | 'O7' | 'O8'
  | 'A+' | 'A' | 'B' | 'C' | 'D' | 'E' | 'E-' | 'F' | 'N/G' | 'F/NG';

/** One score family exactly as the SEC grade grid prints it. */
export interface PclmGradeBand {
  grade: PclmGradeLabel;
  /** Every mark the published grid permits in this band. */
  marks: number[];
}

/**
 * How Coherence and Language are limited, exactly as the year's criteria page
 * prints it. The modern rule (C and L cannot exceed P) must not be projected
 * onto years that print a different rule or none:
 * - `purpose-primacy`: C and L cannot exceed P (2016 onward where printed).
 * - `language-at-d-band`: 2010–2015 Ordinary Level — only when BOTH P and C
 *   fall below the D band is L limited, to the top of its D band.
 * - `none`: the scheme prints no cap (2010–2015 Higher, 2018 Ordinary).
 * Mechanics is always assessed on its own merits.
 */
export type PclmCapRule =
  | { kind: 'purpose-primacy' }
  | { kind: 'none' }
  | { kind: 'language-at-d-band'; purposeBelow: number; coherenceBelow: number; languageMax: number };

/** Where a card's grid was transcribed from, when it is a year-specific print. */
export interface PclmPrintedGrid {
  /** `<year>-<level>`, e.g. `2015-ordinary`. */
  sitting: string;
  /** Marking-scheme PDF pages that print the grid. */
  schemePages: number[];
  /** Adjacent printed cells share a mark (2010–2016 Ordinary Level grid). */
  overlapping?: true;
  /** Lowest printed mark when it is not 0 (2010–2016 OL 10-mark F/NG prints 1). */
  lowestMark?: number;
}

/** The cap a discrete assessment declares, defaulting legacy cards to C/L <= P. */
export function pclmCapRule(assessment: { primacyOfPurpose?: true; capRule?: PclmCapRule }): PclmCapRule {
  return assessment.capRule ?? (assessment.primacyOfPurpose ? { kind: 'purpose-primacy' } : { kind: 'none' });
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
  primacyOfPurpose?: true;
  /** The year's printed cap rule; absent on legacy cards (C/L <= P). */
  capRule?: PclmCapRule;
}

export type PclmComponent = PclmCombinedComponent | PclmDiscreteComponent;

export type PclmAssessment =
  | {
      /** Short Paper 1 answers are judged as one combined mark. */
      mode: 'combined';
      bands: PclmGradeBand[];
      criteria: string[];
      printedGrid?: PclmPrintedGrid;
    }
  | {
      /** Longer responses receive separate P, C, L and M marks. */
      mode: 'discrete';
      bands: PclmGradeBand[];
      criteria: PclmCriterion[];
      /** C and L may not exceed P. */
      primacyOfPurpose?: true;
      /** The year's printed cap rule; absent on legacy cards (C/L <= P). */
      capRule?: PclmCapRule;
      printedGrid?: PclmPrintedGrid;
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

export type IrishGuidanceKind =
  /** A bounded answer or tariff printed by the scheme. */
  | 'exact'
  /** Non-exhaustive possible content which must never become a checklist. */
  | 'indicative'
  /** A published quality band such as Cumas/Cruinneas Gaeilge. */
  | 'quality';

/** One answer of an Irish listening or reading scheme, cut from the exact
 * guidance by cards/irish/answers.ts: the scheme's words before "= 2 mharc". */
export interface IrishAnswerRow {
  id: string;
  text: string;
  /** Marks the row earns; 0 when the part's ladder prices the rows instead. */
  marks: number;
  /** A row the scheme prices in steps rather than whole: "Dhá phointe eolais
   * = 4 mharc + 4 mharc" places at 0, 4 or 8; "Tréith 1 = 13 mharc" with a
   * published band table places anywhere from 0 to 13. Including 0 and `marks`. */
  steps?: number[];
}

/** One sub-question of the scheme ("1. Cad atá á lorg…? 2 mharc") with its answers. */
export interface IrishAnswerPart {
  id: string;
  /** The sub-question as the scheme prints it, with any "(Alt 2)" reference. */
  prompt?: string;
  /** The marks the scheme gives this sub-question. */
  tariff: number;
  /** "{3 mharc: 2 mharc + 1 mharc}": marks for 1..n right answers. */
  ladder?: number[];
  rows: IrishAnswerRow[];
  /** "Freagraí samplacha: • …": the scheme's sample points for this
   * sub-question. Indicative, never a checklist; shown under the rows. */
  samples?: string[];
}

export interface IrishAllocation {
  parts: IrishAnswerPart[];
  /** Lifted scheme sentences that are rules, not answers. */
  directions: string[];
}

/** One independently placed part of the SEC Irish marking scheme. */
export interface IrishCriterion {
  id: string;
  label: string;
  /** Awards add to the mark; deductions are subtracted from it. */
  kind: 'award' | 'deduction';
  maxMarks: number;
  permittedMarks: number[];
  guidanceKind: IrishGuidanceKind;
  /** Verbatim or tightly bounded scheme guidance, never invented content. */
  guidance: string[];
  /** The exact guidance as claimable rows, where cards/irish/answers.ts could
   * cut it so the parts add up to the criterion. Absent: prose over a scale. */
  allocation?: IrishAllocation;
}

/**
 * Irish has its own published grammar: Eolas/Ábhar, Cumas Gaeilge, task/style
 * marks and (at Ordinary Level literature) explicit language deductions.  It
 * is not PCLM and cannot truthfully be rendered as English's grade grid.
 */
export interface IrishRubric {
  system: 'irish';
  /** Things the printed task explicitly requires. They carry no marks alone. */
  taskRequirements: string[];
  criteria: IrishCriterion[];
  /** Explains whether displayed examples are exhaustive or indicative. */
  markingGuideNote: string;
}

export type ArtBandLevel = 'low' | 'moderate' | 'high';

/** One published Art descriptor band and every mark it permits. */
export interface ArtBand {
  level: ArtBandLevel;
  marks: number[];
  /** The scheme's printed lead-in to the band's bullets, where audited. */
  lead?: string;
  /** SEC descriptor guidance: the bullets exactly as the scheme prints them. */
  guidance: string[];
}

/**
 * One independently awarded Art component.
 *
 * The 2021–2022 History and Appreciation schemes allocate marks to named
 * components without quality bands. The 2023+ Visual Studies schemes retain
 * components for Section A and publish low/moderate/high bands; Sections B and
 * C use four holistic criteria. One type represents both grammars without
 * pretending either is English PCLM.
 */
export interface ArtCriterion {
  id: string;
  label: string;
  maxMarks: number;
  permittedMarks: number[];
  /** Question-specific allocation or focus printed by the marking scheme. */
  guidance: string[];
  /**
   * 2021–2022 schemes: the Marks column printed beside each guidance row
   * (parallel to `guidance`), and the Notes column where the scheme prints
   * any note for this component ('' for a row without one).
   */
  rowMarks?: number[];
  rowNotes?: string[];
  /** Absent where the SEC printed an allocation but no descriptor bands. */
  bands?: ArtBand[];
  /**
   * 2021–2022 schemes: the printed rows cut into what the scheme prices
   * (cards/art/answers.ts), so the student places marks on each row or on
   * the parts its Notes cell splits it into, never on the component as a
   * whole. Absent on 2023+ descriptor criteria.
   */
  allocation?: ArtAllocation;
}

/** One priced part of an Art row: "name · 5m" from "5 for name, 10 for description". */
export interface ArtAllocationPart {
  id: string;
  /** The note's own phrase, or the row's words for a remainder the note leaves unlabelled. */
  text: string;
  marks: number;
  /** "1st" / "2nd" where the note prices the same word twice ("names (3/2)"). */
  tag?: string;
}

/** One printed row of an Art component with the Marks cell beside it. */
export interface ArtAllocationRow {
  id: string;
  text: string;
  marks: number;
  /** The Notes cell's split of the row's marks; the parts add up to `marks`. */
  parts?: ArtAllocationPart[];
  /** A Notes cell that prices nothing by itself ("Max 3 for partially correct name."). */
  note?: string;
}

export interface ArtAllocation {
  rows: ArtAllocationRow[];
}

export interface ArtRubric {
  system: 'art';
  /** Things the printed task explicitly requires. They carry no marks alone. */
  taskRequirements: string[];
  criteria: ArtCriterion[];
  /** The scheme's own printed note on applying the descriptors, or ''. */
  markingGuideNote: string;
  /** NextStepUni's guidance for using the card; not part of the SEC scheme. */
  practiceNotes?: string[];
}

export type GeographyGuidanceKind =
  /** A bounded answer or allocation printed by the scheme. */
  | 'exact'
  /** Significant Relevant Points: valid alternatives remain creditable. */
  | 'srp';

/**
 * One Geography mark placement.
 *
 * Geography schemes mix exact short answers, named components, graded map
 * work and Significant Relevant Points.  An SRP is evidence emerging from a
 * coherent response, not a model-answer bullet to tick.  Keeping that grammar
 * explicit prevents the scheme's non-exhaustive examples becoming a fabricated
 * checklist while still letting a student place their work on the real tariff.
 */
/**
 * One claimable answer on a Geography card: a slice of a scheme line and the
 * marks the scheme prints beside it.
 */
export interface GeographyAnswerRow {
  id: string;
  /** The printed answer, or the scheme's tariff wording when it prints none. */
  text: string;
  marks: number;
  /** The values a student may claim when the scheme splits the row
   *  ("2 + 2 marks", "4m graded (4/2/0)"). Omitted means all or nothing. */
  steps?: number[];
  /** The scheme prices the answer without printing one ("Tectonic plate
   *  named 3m"). The row shows the scheme's words and says any correct answer
   *  scores; it never carries an example the scheme did not print. */
  tariffOnly?: boolean;
}

/** A Significant Relevant Point allocation: how many the scheme counts, at
 *  what value each. Rendered as a counter, never as a list to tick. */
export interface GeographySrpAllocation {
  id: string;
  /** The scheme's label for the part ("Description/Explanation"), or ''. */
  label: string;
  /** The most SRPs this part can earn. */
  count: number;
  marks: number;
  /** Set when the scheme prints a range ("6/7 x SRP's"): this part and its
   *  siblings share `GeographyAllocation.srpPool`, which caps their sum. */
  min?: number;
}

/** The rows and SRP counts under one printed sub-question. */
export interface GeographyAllocationGroup {
  /** The paper's label, "(i)". */
  part?: string;
  /** The sub-question as printed. */
  prompt?: string;
  rows: GeographyAnswerRow[];
  srp: GeographySrpAllocation[];
  /**
   * The scheme prices one unit and asks for several ("Formation of any two
   * landforms @ 20m each. For each landform: …"). The group's rows and SRPs
   * are claimed once per unit; `unit` is the scheme's own noun for one.
   */
  repeat?: { count: number; unit: string; marks: number };
}

/**
 * A Geography criterion cut into claimable rows. Present only when the rows
 * and SRP counts add up to the card's total (cards/geography/allocation.ts);
 * otherwise the reveal falls back to the guidance lines and a mark control.
 */
export interface GeographyAllocation {
  groups: GeographyAllocationGroup[];
  /** Examiner directions: caps, named-example rules, diagram conditions. */
  directions: string[];
  /** Where parts print SRP ranges, the SRPs they share between them. */
  srpPool?: { count: number; marks: number };
  /** The scheme prices this criterion one of several ways and the student
   *  claims exactly one: a column of a two-route table ("3 @ 20 marks each" /
   *  "4 @ 15 marks each"), or a quality band ("Very Good · 17"). */
  choice?: GeographyAllocationChoice;
}

/** One way the scheme prices a criterion, claimed instead of the others. */
export interface GeographyChoiceOption {
  id: string;
  /** The scheme's words for it: a column heading or a band's name. */
  label: string;
  /** A band's marks, earned by choosing it. */
  marks?: number;
  /** A band's descriptor, as printed. */
  note?: string;
  /** A column's own rows and SRP counts, claimed once the column is chosen. */
  allocation?: GeographyAllocation;
}

export interface GeographyAllocationChoice {
  /** route: a column of a two-route table; band: a quality band; alternative:
   *  one printed answer or another, each at its own price. */
  kind: 'route' | 'band' | 'alternative';
  /** The scheme's heading over the options ("Number of aspects"), or ''. */
  prompt: string;
  options: GeographyChoiceOption[];
}

export interface GeographyCriterion {
  id: string;
  label: string;
  maxMarks: number;
  permittedMarks: number[];
  guidanceKind: GeographyGuidanceKind;
  /** Published allocation and examiner directions for this task, as lifted. */
  guidance: string[];
  /** The same allocation as claimable rows, where it reconciles to
   *  `maxMarks` and (for a reviewed criterion) to `permittedMarks`. */
  allocation?: GeographyAllocation;
}

export interface GeographyRubric {
  system: 'geography';
  /** Finite route or other instruction selected on this card. */
  taskRequirements: string[];
  criteria: GeographyCriterion[];
  /** The mark value of one SRP on this paper, where SRPs govern the answer. */
  srpMarks?: number;
  /** Printed marks the published scheme allocates to no line (2020 OL 9C
   *  prices 27 of its printed 30). They stay in the card's `totalMarks` and
   *  are never derived into a criterion, so the criteria reach
   *  `totalMarks - unpricedMarks`; the marking guide note says so. */
  unpricedMarks?: number;
  /** The scheme's own examiner directions (credit rules, caps, deductions)
   *  for this task, lifted verbatim. They qualify the criteria; they carry
   *  no marks of their own. */
  directions?: string[];
  markingGuideNote: string;
}

/** Politics answers mix exact allocations, quality bands and six essay criteria. */
export interface PoliticsCriterion {
  id: string;
  label: string;
  maxMarks: number;
  permittedMarks: number[];
  guidance: string[];
  bands?: Array<{ label: string; marks: number[]; guidance: string }>;
}

/** One quality band of a Politics ladder as the scheme prints it:
 * "Very good explanation" at 8–10M, with its descriptor where printed. */
export interface PoliticsBand {
  label: string;
  marks: number[];
  descriptor?: string;
}

export interface PoliticsAnswerRow {
  id: string;
  text: string;
  marks: number;
  /** The scheme prices this answer without printing one: the row shows the
   * criterion's own words and the reveal says any correct answer scores. */
  tariffOnly?: boolean;
}

/** One independently priced part of a Politics answer, cut from the lifted
 * scheme block by cards/politics-and-society/answers.ts: a quality ladder the
 * student places themselves on, or exact answers they claim. */
export interface PoliticsPart {
  id: string;
  /** The criterion this part scores. */
  label: string;
  /** The scheme's own words for what the part asks ("Two valid actions"). */
  caption?: string;
  max: number;
  bands?: PoliticsBand[];
  rows?: PoliticsAnswerRow[];
  /** How many rows count when the part is a list of exact answers. */
  count?: number;
  /** "3 marks + 2 marks" over a list of answers: marks for 1..count rows claimed. */
  ladder?: number[];
}

export interface PoliticsAllocation {
  parts: PoliticsPart[];
  /** The scheme's indicative points ("Responses may make reference to"), shown as a list; never a checklist. */
  examples: string[];
  /** Lifted scheme sentences that are rules, not answers. */
  directions: string[];
}

export interface PoliticsRubric {
  system: 'politics';
  taskRequirements: string[];
  criteria: PoliticsCriterion[];
  /** Shared published guidance, shown once even when several criteria apply. */
  schemeGuidance?: string[];
  /** The guidance and bands as placeable ladders and claimable rows, where
   * cards/politics-and-society/answers.ts could cut them so the parts add up
   * to the card. Absent: the lines show as a list over mark buttons. */
  allocation?: PoliticsAllocation;
  markingGuideNote: string;
  /** Exact scheme pages remain available after reveal, including grade grids. */
  schemePages: number[];
  schemeFileid: string;
}

/** PE mixes exact allocations, descending tariffs and quality bands. The
 * original scheme remains available after reveal, including answer diagrams
 * and tick tables which must not be flattened into a guessed text answer. */
/** One PE criterion's reviewed guidance cut into what the scheme prices
 * (cards/physical-education/answers.ts): quality bands the student places
 * themselves on ("Good description: 2; fair description: 1."), and rows they
 * claim ("Vector.", "Phase named: 1", "4 marks + 2 marks" as steps). */
export interface PhysicalEducationAllocation {
  /** The guidance's own statement of what is asked, where it has one. */
  caption?: string;
  bands?: Array<{ label: string; marks: number[] }>;
  rows?: Array<{ id: string; text: string; marks: number; steps?: number[] }>;
  /** The rest of the guidance: accept/do-not-accept rules, scheme examples. */
  notes: string[];
}

export interface PhysicalEducationRubric {
  system: 'physical-education';
  taskRequirements: string[];
  criteria: Array<{
    id: string;
    label: string;
    maxMarks: number;
    permittedMarks: number[];
    guidance: string[];
    allocation?: PhysicalEducationAllocation;
  }>;
  schemeMaterial: CardSourceMaterial & { kind: 'marking-scheme' };
  markingGuideNote: string;
}

/** Mathematical working and drawings remain in their original SEC layout.
 * Each allocation is one published step or scale, with its actual credit
 * values. Error deductions apply within that allocation, never to neighbours. */
export interface AppliedMathematicsRubric {
  system: 'applied-mathematics';
  solution: Omit<CardSourceMaterial, 'regions'> & { kind: 'source-scheme'; regions?: Array<[number, number, number, number]> };
  allocations: Array<{
    id: string;
    label: string;
    credit: number[];
    guidance?: string;
  }>;
  markingGuideNote: string;
}

/** Accounting awards marks within worked accounts, including transfer and
 * calculation penalties. Preserve the printed layout and allocation rather
 * than turning each correct final figure into an all-or-nothing checklist. */
export interface AccountingRubric {
  system: 'accounting';
  solution: Omit<CardSourceMaterial, 'regions'> & { kind: 'marking-scheme'; regions?: Array<{ p: number; r: [number, number, number, number]; rotate?: 0 | 90 | 180 | 270 }> };
  allocationNote: string;
  /** A separately priced output within a shared printed instruction. */
  taskFocus?: string;
}

/** A published Business allocation within one response, e.g. Name/Explain/Link. */
export interface BusinessAllocation {
  id: string;
  label: string;
  maxMarks: number;
  permittedMarks: number[];
  /** The SEC forbids an ABQ link without relevant theory in that response. */
  requiresAnyOf?: string[];
}

/** One response the SEC's scheme prints for a Business part — a bullet, a
 * numbered line or a heading with the prose under it — lifted from the cited
 * "Possible Responses" / "Support Notes" page by bus_expected.py. The scheme
 * calls these a sample, never an exhaustive list, so a row is what the scheme
 * printed, not the only answer that scores. */
export interface BusinessExpectedItem {
  id: string;
  text: string;
  /** The lines the scheme prints under a heading: the explanation and its case link. */
  detail?: string[];
}

export interface BusinessExpected {
  /** The scheme page the items were read from. */
  page: number;
  items: BusinessExpectedItem[];
}

export interface BusinessRubric {
  system: 'business';
  taskRequirements: string[];
  guidance: string[];
  responses: Array<{
    id: string;
    label: string;
    allocations: BusinessAllocation[];
  }>;
  /** The scheme's printed responses for this part, as rows the student can
   * claim; absent where bus_expected.py could not lift them (listed in
   * scripts/markbank/authored/business-expected-review.json). */
  expected?: BusinessExpected;
  /** Exact official support notes, shown only after the scheme is revealed. */
  schemeFileid: string;
  schemePages: number[];
  markingGuideNote: string;
}

/** French writing combines communicative tasks, language quality and format.
 * A band describes the whole response; it is never a claimable answer. */
export interface FrenchCriterion {
  id: string;
  label: string;
  maxMarks: number;
  permittedMarks: number[];
  guidance: string[];
  bands?: { label: string; marks: number[]; guidance: string[] }[];
  /** The SEC withholds language marks if no communicative task is attempted. */
  requiresAttempt?: boolean;
}

/** One answer of a French listening, reading or cloze scheme, cut from a
 * lifted `answerGuide` line by cards/french/answers.ts. The text is the
 * scheme's own words without the list marker and the price. */
export interface FrenchAnswerRow {
  id: string;
  text: string;
  /** Marks the row earns when claimed; negative for a printed deduction
   * ("➢ Incorrect year = -1 Mark"); 0 for an answer the scheme prices at 0. */
  marks: number;
  /** A row the student places at one of several printed values (cloze: 3, or
   * 2 after the scheme's careless-transcription deduction). */
  steps?: number[];
  /** A dash or asterisk line: the scheme's partial-credit alternative. */
  partial?: boolean;
  /** The sub-part heading the scheme prints over this row ("(a)", "(ii) Restaurant"). */
  part?: string;
}

/** A French card's scheme cut into claimable rows. */
export interface FrenchAllocation {
  /** How many answers the task asks for: at most this many positive rows count. */
  count: number;
  rows: FrenchAnswerRow[];
  /** A list the scheme prices by how many are right ("Any two of the following,
   * award 5 Marks / Any one … 3 Marks"; "Two correct answers needed for 8 marks
   * (7+1)"): marks for 1..count ticked rows. The rows then carry no price. */
  ladder?: number[];
  /** The aural rule printed for named tasks: where less than full marks is
   * achieved in either segment, the higher mark is awarded to each segment. */
  scoring?: 'higher-segment-both';
  /** Lifted scheme lines that are not answers: acceptances, conventions, notes. */
  directions: string[];
}

export interface FrenchRubric {
  system: 'french';
  taskRequirements: string[];
  /** Complete accepted answers, partial-credit ladder and question-specific rules. */
  answerGuide?: string[];
  /** The answerGuide as claimable rows, where cards/french/answers.ts could cut
   * it so the rows reconcile with the printed total. Absent: the lines show as
   * a list and the response is placed on the permitted marks. */
  allocation?: FrenchAllocation;
  criteria: FrenchCriterion[];
  markingGuideNote: string;
  /** NextStepUni's own practice guidance. Never SEC text: rendered apart from
   *  the scheme under an explicit app label. Every other field of this rubric
   *  shows the SEC's printed wording. */
  practiceNotes?: string[];
}

export type SecRubric = PclmRubric | IrishRubric | ArtRubric | GeographyRubric | PoliticsRubric | PhysicalEducationRubric | AppliedMathematicsRubric | AccountingRubric | FrenchRubric | BusinessRubric;

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
 * A real SEC question governed by a published subject-specific rubric rather
 * than a list of exact answer points. This variant has a renderer and scoring
 * path of its own; it does not expose `rows`, so indicative examples cannot
 * accidentally become binary marks in some future consumer.
 */
export interface SecRubricCard extends SecCardBase {
  kind: 'rubric';
  rubric: SecRubric;
  /** A crop of an official document shown on the card. A `solution` crop
   *  (the scheme's own answer drawing) is held back until the reveal. Used by
   *  Geography for a map crop around the grid reference asked about and for a
   *  scheme's labelled diagram. */
  figure?: CardFigure;
  /** The paper's own print of the ask, as on `SecQuestionCard`: shown before
   *  the reveal in place of the typeset stem, never a solution. Used by
   *  Geography for a diagram question whose blanks are the ask. */
  questionFigure?: CardFigure;
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
// Agricultural Science 2010 HL Q8(c): three comparisons with two separately
// priced marking groups each. Six rows preserve the full printed route.
export const MAX_ROWS = 6;

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
 * Still bounded. Seventeen is the ceiling because Agricultural Science 2010 HL
 * Q5(a)(ii) prints seventeen accepted footrot points. The bound follows the
 * largest verified SEC menu rather than deleting correct answers for neatness.
 */
export const MAX_LONG_OPTION_ROWS = 17;

/** The row cap that actually applies to a card, given its tariff.
 *
 * The six-row cap is for REQUIRED recall — a list the student must produce in
 * full. An orderedSplit or questionTotal card's rows are a different thing:
 * the scheme's own printed candidate points, where what a student claims is
 * bounded by the notation or the question's total rather than by the row
 * count. Computer Science Section A answers a whole multi-part question in one
 * scheme block ("state two differences" then lists nine), and trimming that
 * list to five would misrepresent the scheme, not lighten the card. Those two
 * kinds share the menu ceiling: the most any SEC long question prints. */
export const rowCapFor = (kind: TariffModel['kind']): number =>
  kind === 'bestNofParts' ? MAX_OPTION_ROWS
    : kind === 'orderedSplit' || kind === 'questionTotal' ? MAX_LONG_OPTION_ROWS
      : MAX_ROWS;

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
// German's reading comprehensions are long questions whose PARTS are small:
// the 2022 Higher TEXT I theme question prints twenty-six accepted points
// for ten marks and its 1(a) prints nine for six, so the section tokens the
// German deck cites — TEXT I, II and III — belong here too.
// Russian's reading and language-awareness questions are long questions whose
// PARTS are small: the 2025 Higher summary question prints seventeen accepted
// points for its eight content marks, and the semantic-field task prints
// eighteen Russian words for ten. Its section tokens name the printed
// question rather than a letter (see UNIT_NAME in ru_scheme.py), so they
// belong here too: C1 and C2 are Higher's two comprehensions, IR1 and IR2
// Ordinary's retrieval texts, CD its comprehension, and LA1/LA2/CA1 the
// language- and cultural-awareness tasks.
// Latin's Questions 3 and 5 are long questions: the scheme answers a ten-mark
// prescribed-text part and a twenty-five-mark civilisation essay with pages of
// Indicative Notes, and 2025 Higher prints twenty-one separate points for one
// twenty-five-mark question on Augustus. Questions 1, 2 and 4 are short —
// Question 1 Section B is twelve comprehension asks of four to fourteen marks.
// The Baltic languages' reading tasks are long questions whose PARTS are
// small: 2024 Higher Lithuanian answers a five-mark "find one past-frequentative
// verb" with eleven verbs and 2022 Ordinary answers a five-mark "write one thing
// Jonas does in New York" with thirteen. One task is one printed text with up to
// eleven asks on it, which is what makes the examiner print a long menu, so the
// task tokens 'U1' to 'U3' (užduotis — the paper's own word for it) belong here.
const LONG_SECTIONS = new Set(['2', '3', 'B', 'C', 'T1', 'T2', 'T3',
  'C1', 'C2', 'CD', 'IR1', 'IR2', 'LA1', 'LA2', 'CA1', 'Q3', 'Q5',
  'U1', 'U2', 'U3']);
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
 * `orderedSplit` and `questionTotal` cannot be checked by summing rows, because
 * the scheme does not define per-row values — so we assert the rows carry none
 * rather than pretending.
 */
/** What one bounded group is worth when fully claimed. */
export function groupMarks(g: { claimMax: number; perOption: number; perOptionSteps?: number[] }): number {
  return g.perOptionSteps
    ? g.perOptionSteps.slice(0, g.claimMax).reduce((n, m) => n + m, 0)
    : g.claimMax * g.perOption;
}

/** A criterion row's parts add up to its marks, with ids of their own and steps from 0 to each part's marks. */
export function rowPartsReconcile(row: MarkRow): boolean {
  const parts = row.parts;
  if (!parts || !row.permittedMarks || row.kind !== 'criterion' || row.marks === null) return false;
  if (parts.length < 2 || new Set(parts.map(part => part.id)).size !== parts.length) return false;
  if (parts.reduce((sum, part) => sum + part.marks, 0) !== row.marks) return false;
  return parts.every(part => part.id && part.verbatim.trim()
    && Number.isInteger(part.marks) && part.marks > 0
    && part.permittedMarks.length >= 2
    && part.permittedMarks[0] === 0
    && part.permittedMarks.at(-1) === part.marks
    && part.permittedMarks.every((mark, index, steps) => Number.isInteger(mark) && mark >= 0 && (index === 0 || mark > steps[index - 1])));
}

export function tariffReconciles(card: SecCard): boolean {
  if (isRubricCard(card)) {
    if (card.rubric.system === 'politics') {
      const { criteria, schemePages, schemeFileid } = card.rubric;
      return Boolean(schemeFileid)
        && schemePages.length > 0
        && schemePages.every(page => Number.isInteger(page) && page > 0)
        && criteria.length > 0
        && new Set(criteria.map(criterion => criterion.id)).size === criteria.length
        && criteria.reduce((sum, criterion) => sum + criterion.maxMarks, 0) === card.totalMarks
        && criteria.every(criterion => {
          const permitted = criterion.permittedMarks;
          if (!permitted.length || Math.min(...permitted) !== 0
              || Math.max(...permitted) !== criterion.maxMarks
              || new Set(permitted).size !== permitted.length
              || permitted.some(mark => !Number.isInteger(mark) || mark < 0)) return false;
          if (!criterion.bands) return true;
          const marks = criterion.bands.flatMap(band => band.marks).sort((a, b) => a - b);
          return marks.length === permitted.length
            && new Set(marks).size === marks.length
            && marks.every((mark, index) => mark === [...permitted].sort((a, b) => a - b)[index]);
        });
    }
    if (card.rubric.system === 'applied-mathematics') {
      const { allocations, solution } = card.rubric;
      return allocations.length > 0
        && new Set(allocations.map(item => item.id)).size === allocations.length
        && allocations.every(item => item.credit.length > 1
          && item.credit[0] === 0
          && item.credit.every((mark, index) => Number.isInteger(mark) && mark >= 0
            && (index === 0 || mark > item.credit[index - 1])))
        && allocations.reduce((sum, item) => sum + Math.max(...item.credit), 0) === card.totalMarks
        && solution.kind === 'source-scheme'
        && solution.pages.length > 0
        && solution.pages.every(page => Number.isInteger(page) && page > 0)
        && (!solution.regions || (solution.regions.length === solution.pages.length
          && solution.regions.every(rect => Array.isArray(rect) && rect.length === 4
            && rect.every(value => Number.isFinite(value) && value >= 0 && value <= 1)
            && rect[0] < rect[2] && rect[1] < rect[3])));
    }
    if (card.rubric.system === 'accounting') {
      const { solution, allocationNote } = card.rubric;
      return Number.isFinite(card.totalMarks) && card.totalMarks > 0
        && solution.kind === 'marking-scheme'
        && Boolean(solution.sourceFileid) && Boolean(allocationNote.trim())
        && solution.pages.length > 0
        && solution.pages.every(page => Number.isInteger(page) && page > 0);
    }
    if (card.rubric.system === 'business') {
      const { responses } = card.rubric;
      return responses.length > 0
        && new Set(responses.map(response => response.id)).size === responses.length
        && responses.flatMap(response => response.allocations)
          .reduce((sum, allocation) => sum + allocation.maxMarks, 0) === card.totalMarks
        && responses.every(response => response.allocations.length > 0
          && new Set(response.allocations.map(allocation => allocation.id)).size === response.allocations.length
          && response.allocations.every(allocation =>
            allocation.permittedMarks.length > 0
            && Math.min(...allocation.permittedMarks) === 0
            && Math.max(...allocation.permittedMarks) === allocation.maxMarks
            && new Set(allocation.permittedMarks).size === allocation.permittedMarks.length
            && allocation.permittedMarks.every(mark => Number.isInteger(mark) && mark >= 0)
            && (!allocation.requiresAnyOf || (allocation.requiresAnyOf.length > 0
              && allocation.requiresAnyOf.every(id => response.allocations.some(candidate =>
                candidate.id === id && !candidate.requiresAnyOf && candidate.id !== allocation.id))))));
    }
    if (card.rubric.system === 'irish') {
      const { criteria } = card.rubric;
      const awardMaximum = criteria
        .filter(criterion => criterion.kind === 'award')
        .reduce((sum, criterion) => sum + criterion.maxMarks, 0);
      return criteria.length > 0
        && new Set(criteria.map(criterion => criterion.id)).size === criteria.length
        && awardMaximum === card.totalMarks
        && criteria.every(criterion =>
          criterion.permittedMarks.length > 0
          && Math.min(...criterion.permittedMarks) === 0
          && Math.max(...criterion.permittedMarks) === criterion.maxMarks
          && new Set(criterion.permittedMarks).size === criterion.permittedMarks.length);
    }
    if (card.rubric.system === 'art') {
      const { criteria } = card.rubric;
      return criteria.length > 0
        && new Set(criteria.map(criterion => criterion.id)).size === criteria.length
        && criteria.reduce((sum, criterion) => sum + criterion.maxMarks, 0) === card.totalMarks
        && criteria.every(criterion => {
          const permitted = criterion.permittedMarks;
          if (permitted.length === 0
            || Math.min(...permitted) !== 0
            || Math.max(...permitted) !== criterion.maxMarks
            || new Set(permitted).size !== permitted.length) return false;
          if (!criterion.bands) return true;
          const bandMarks = criterion.bands.flatMap(band => band.marks);
          return criterion.bands.length === 3
            && new Set(criterion.bands.map(band => band.level)).size === 3
            && bandMarks.length === permitted.length
            && new Set(bandMarks).size === bandMarks.length
            && [...bandMarks].sort((a, b) => a - b)
              .every((mark, index) => mark === [...permitted].sort((a, b) => a - b)[index]);
        });
    }
    if (card.rubric.system === 'french') {
      const { criteria } = card.rubric;
      return criteria.length > 0
        && new Set(criteria.map(criterion => criterion.id)).size === criteria.length
        && criteria.reduce((sum, criterion) => sum + criterion.maxMarks, 0) === card.totalMarks
        && criteria.every(criterion => {
          const allowed = criterion.permittedMarks;
          if (!allowed.length || Math.min(...allowed) !== 0
            || Math.max(...allowed) !== criterion.maxMarks
            || new Set(allowed).size !== allowed.length
            || allowed.some(mark => !Number.isInteger(mark) || mark < 0)) return false;
          if (!criterion.bands) return true;
          const marks = criterion.bands.flatMap(band => band.marks);
          return marks.length === allowed.length && new Set(marks).size === marks.length
            && marks.every(mark => allowed.includes(mark));
        });
    }
    if (card.rubric.system === 'geography' || card.rubric.system === 'physical-education') {
      const criteria: Array<{ id: string; maxMarks: number; permittedMarks: number[] }> = card.rubric.criteria;
      // A printed remainder the scheme prices on no line is declared, never derived.
      const unpriced = card.rubric.system === 'geography' ? card.rubric.unpricedMarks ?? 0 : 0;
      return criteria.length > 0
        && Number.isInteger(unpriced) && unpriced >= 0 && unpriced < card.totalMarks
        && new Set(criteria.map(criterion => criterion.id)).size === criteria.length
        && criteria.reduce((sum, criterion) => sum + criterion.maxMarks, 0) + unpriced === card.totalMarks
        && criteria.every(criterion =>
          criterion.permittedMarks.length > 0
          && Math.min(...criterion.permittedMarks) === 0
          && Math.max(...criterion.permittedMarks) === criterion.maxMarks
          && criterion.permittedMarks.every(mark => Number.isInteger(mark) && mark >= 0 && mark <= criterion.maxMarks)
          && new Set(criterion.permittedMarks).size === criterion.permittedMarks.length);
    }
    const { assessment } = card.rubric;
    const bandsReconcile = (bands: PclmGradeBand[], total: number, printed?: PclmPrintedGrid) => {
      const marks = bands.flatMap(band => band.marks);
      // A year-specific print may share a mark between adjacent cells or start
      // above 0; only a card that declares that printed grid may do so.
      return marks.length > 0
        && Math.min(...marks) === (printed?.lowestMark ?? 0)
        && Math.max(...marks) === total
        && (printed?.overlapping ? true : new Set(marks).size === marks.length);
    };
    if (assessment.mode === 'combined') {
      return bandsReconcile(assessment.bands, card.totalMarks, assessment.printedGrid);
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
  const bonus = card.questionBonus;
  if (bonus && (t.kind !== 'fixed' || !card.taskGroups?.length
    || !bonus.id || rows.some(row => row.id === bonus.id)
    || bonus.kind !== 'criterion' || !bonus.verbatim.trim() || !bonus.contextNote.trim()
    || !Number.isFinite(bonus.marks) || bonus.marks <= 0
    || !Array.isArray(bonus.permittedMarks) || bonus.permittedMarks.length < 2
    || bonus.permittedMarks[0] !== 0 || bonus.permittedMarks.at(-1) !== bonus.marks
    || bonus.permittedMarks.some((mark, index, steps) => !Number.isFinite(mark)
      || mark < 0 || (index > 0 && mark <= steps[index - 1])))) return false;

  if (rows.some(row => row.permittedMarks && (
    t.kind !== 'fixed' || row.kind !== 'criterion' || row.marks === null
    || row.permittedMarks.length < 2
    || row.permittedMarks[0] !== 0
    || row.permittedMarks.at(-1) !== row.marks
    || row.permittedMarks.some((mark, index, steps) => !Number.isFinite(mark)
      || mark < 0 || (index > 0 && mark <= steps[index - 1]))
  ))) return false;
  // Parts are a criterion row's own split: they add up to it, each on printed steps.
  if (rows.some(row => row.parts && !rowPartsReconcile(row))) return false;
  if (t.kind === 'orderedSplit') return rows.every(r => r.marks === null);
  // The scheme never printed a split, so a row carrying its own marks is a
  // value the card invented — the tariff lives on the question alone.
  if (t.kind === 'questionTotal') return rows.every(r => r.marks === null);
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
  common += bonus?.marks ?? 0;
  if (!byRoute.size) return common === totalMarks;
  return [...byRoute.values()].every(n => common + n === totalMarks);
}
