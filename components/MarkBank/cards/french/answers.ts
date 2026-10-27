/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * French answer rows.
 *
 * A French listening, reading or cloze card carries its scheme as
 * `answerGuide`: lines lifted from the SEC marking scheme by
 * scripts/markbank/authoring/fr_{listening,reading,cloze}.py, each one
 * re-lifted by tests/test_fr_sec_wording.py. Until October 2026 the reveal
 * printed them as paragraphs in a details box over a 0..total dropdown, so a
 * student read "• Go out in nature — 3 Marks" as prose and then had to find
 * the matching number in a `<select>`. The rule since then: an answer the
 * scheme prices is a claimable row showing the answer and its marks; prose is
 * only for the examiner's directions.
 *
 * This module cuts the lifted lines into those rows. It adds no words: a row's
 * text is one scheme line without its list marker and its price, a part label
 * is the scheme's own "(a)" or "(ii) Restaurant", and a direction is a scheme
 * line or the bracketed note a line ends with. A card is structured only when
 * the rows reconcile with the printed total (count × full mark, a header
 * ladder, or the aural higher-segment rule); any card the parser cannot place
 * exactly keeps the list fallback, and test/frenchAnswers.test.ts pins how
 * many cards that is so the number can only fall.
 *
 * The shapes it reads, all from the 2010–2026 schemes:
 *   • Go out in nature — 3 Marks            a full-credit answer (bullet)
 *   - Hiking/Walking — 2 Marks              a partial answer (dash); 0 Marks happens
 *   18 5 marks · (c) 5 marks                an older listening answer, no marker
 *   - At the market — 4 marks / - Locally   the older Ordinary stroke convention:
 *                                           alternatives on separate lines share the
 *                                           price printed against one of them
 *   * Local shop — 1 mark                   a partial answer (asterisk) in that convention
 *   Either of the following 5 marks         the price of each answer under it
 *   Accept any two of the following: — 4+4 marks     one price per answer, two answers
 *   Any two of the following, award 5 Marks /
 *   Any one of the following, award 3 Marks          a ladder by how many are right
 *   Two correct answers needed for 8 marks (7+1)     the 2010–2015 Ordinary ladder (a rule line)
 *   Any two of: / Agree: / • … / Disagree: / • …      an opinion question's accepted points, priced only
 *                                                   in the general rule: the total shared equally per
 *                                                   point, placed at "Award 2 marks if partially correct"
 *   ➢ Incorrect year = -1 Mark              a deduction the student can apply
 *   ➢ If more than one answer offered = 0 Marks      a priced condition
 *   One correct day plus one incorrect day = 1 Mark  the same, unmarked
 *   (a) / (ii) Restaurant                   a sub-part heading
 *   1. ta · 10 gaps for 3 marks each · Careless transcription … deduct 1 mark   cloze
 */

import type { FrenchAllocation, FrenchAnswerRow, FrenchRubric, SecRubricCard } from '../../../../types/markBank';

export interface FrenchAnswerSource {
  id: string;
  totalMarks: number;
  questionText: string;
  answerGuide: readonly string[];
  taskRequirements: readonly string[];
  markingGuideNote: string;
  permittedMarks: readonly number[];
}

export type FrenchAnswerResult =
  | { ok: true; allocation: FrenchAllocation }
  | { ok: false; reason: string };

const NUMBER_WORDS: Record<string, number> = { one: 1, either: 1, two: 2, both: 2, three: 3, four: 4 };

/** The list markers the lifted lines carry (the PDF Symbol-font ones are mapped by the generator). */
const MARKER = /^([•\-–−‑*∗➢])\s*/;
const STAR_MARKERS = new Set(['*', '∗']);

/** "3 Marks", "1 Mark", "4 marks", "5 Mar" (one 2025 line is cut short), with or without a stop. */
const MARK = String.raw`[Mm]ar(?:ks?)?\b\.?`;
/** A trailing price, optionally followed by a bracketed or asterisked note:
 * "4 marks (Minus 1 mark for each extraneous element)", "3 Marks * Accept the Conditional / Present." */
const TRAILING_PRICE = new RegExp(String.raw`\s*(?:[—–-]\s*)?(\d+)\s*${MARK}\s*(?:[([]\s*(.*?)\s*[)\]]|[*∗]\s*(\S.*?))?\s*$`);
/** "= -1 Mark", ", minus 1 mark.", "= minus one Mark", "= minus 1." */
const DEDUCTION = new RegExp(String.raw`^(.*?)[,:]?\s*(?:=\s*)?(?:[-−–]\s*(\d+)|minus\s+(\d+|one|two))\s*(?:${MARK})?\s*$`, 'i');
const DEDUCTION_CUE = /(?:=\s*[-−–]|\bminus\b)/i;
/** "… = 0 Marks.", "…, award 2 Marks.", "Award 2 marks if …" */
const CONDITION_TAIL = new RegExp(String.raw`^(.*?)\s*(?:=|,?\s*award)\s*(\d+)\s*${MARK}\s*(.*)$`, 'i');
const CONDITION_HEAD = new RegExp(String.raw`^Award\s+(\d+)\s*${MARK}\s+\S`, 'i');
const CONDITION_CUE = /\s=\s|\baward\b|^(?:if|note)\b/i;
/** A list header that prices the answers under it; its wording, then its price(s). */
const HEADER = new RegExp(String.raw`^(.*?)\s*:?\s*(?:[—–-]\s*)?((?:\d+\s*\+\s*)*\d+)\s*${MARK}\s*$`);
const HEADER_HEAD = /^(?:accept\b|(?:any|either|both|one|two|three|four)\s+(?:(?:one|two|three|four)\s+)?of\s+(?:the\s+)?following\b|(?:any|either|both)\s+(?:one|two|three|four)?\s*of\b)/i;
const COUNT_WORD = new RegExp(String.raw`\b(${Object.keys(NUMBER_WORDS).join('|')})\b`, 'i');
/** The 2010–2015 Ordinary rule line: "Two correct answers needed for 8 marks (7+1)." */
const RULE_LADDER = /\b(one|two|three|four)\s+correct answers?\b.*?\bfor\s+(\d+)\s*marks?\s*\((\d+(?:\s*\+\s*\d+)+)\)/i;
const PART = /^\((?:[a-z]|i{1,3}|iv|vi{0,3})\)(?:\s+\S.*)?$/i;
const PART_WORD = /^[A-Z][^:]{0,40}:$/;
/** List furniture that is implied once the answers are rows. */
const FURNITURE = /^(?:(?:one|two|any\s+\w+|either|both|accept any\s+\w+)\s+of(?:\s+the\s+following(?:\s+points)?)?\s*:?|etc\.?,?\s*etc\.?|note\s*:)$/i;
const COUNT_HEADER = /^(?:(one|two|three|four|either|both)|any\s+(one|two|three|four))\s+of\b/i;
/** A bare line that cannot be the answer itself. */
const NOT_AN_ANSWER = /^(?:note|accept|n\.?b\.?|if|where|candidates|appropriate|correct|direct|award|etc)\b/i;
const SEGMENT_RULE = /higher mark is to be awarded to each segment/i;
const CLOZE_TARIFF = /^(\d+)\s+gaps\s+for\s+(\d+)\s+marks?\s+each$/i;
const CLOZE_DEDUCT = /deduct\s+(\d+)\s+marks?/i;
/** "1. ta", "2. passe/serai", "6 travaille" (2019 prints no stop), "10." (2022 prints a blank). */
const CLOZE_ENTRY = /^(\d+)(?:\.\s*|\s+)(.*)$/;
const TWO_ASKED = /\b(?:two|deux)\b|\(two details\)/i;

const tidy = (value: string) => value.replace(/\s+/g, ' ').replace(/\s*[—–]\s*$/, '').trim();

const cumulative = (terms: number[]) => terms.map((_, index) => terms.slice(0, index + 1).reduce((a, b) => a + b, 0));

interface Draft {
  text: string;
  marks?: number;
  /** A row placed at one of several printed values (an opinion point at its partial or full mark). */
  steps?: number[];
  partial?: boolean;
  part?: string;
  /** Alternatives inherit a price only within a run of the same kind. */
  kind: 'full' | 'dash' | 'star' | 'condition' | 'deduction';
}

function parseCloze(source: FrenchAnswerSource): FrenchAnswerResult {
  const guide = source.answerGuide;
  const tariff = guide.map(line => CLOZE_TARIFF.exec(line)).find(Boolean);
  if (!tariff) return { ok: false, reason: 'cloze without its tariff line' };
  const marks = Number(tariff[2]);
  const entry = CLOZE_ENTRY.exec(guide[0] ?? '');
  if (!entry) return { ok: false, reason: 'cloze without its numbered entry' };
  let text = tidy(entry[2]);
  const directions: string[] = [];
  guide.slice(1).forEach(line => {
    // A blank entry ("10.") is answered by the scheme's completed-letter line.
    if (!text && !CLOZE_TARIFF.test(line) && !CLOZE_DEDUCT.test(line)) text = tidy(line);
    else directions.push(line);
  });
  if (!text) return { ok: false, reason: 'cloze entry has no answer' };
  const deduct = guide.map(line => CLOZE_DEDUCT.exec(line)).find(Boolean);
  const steps = deduct && marks - Number(deduct[1]) > 0 ? [marks, marks - Number(deduct[1])] : undefined;
  if (marks !== source.totalMarks) return { ok: false, reason: `cloze tariff ${marks} ≠ total ${source.totalMarks}` };
  return { ok: true, allocation: { count: 1, rows: [{ id: 'r1', text, marks, ...(steps ? { steps } : {}) }], directions } };
}

/** Cut a card's lifted scheme lines into claimable rows, or say why not. */
export function parseFrenchAnswers(source: FrenchAnswerSource): FrenchAnswerResult {
  const guide = source.answerGuide.map(line => line.trim()).filter(Boolean);
  if (guide.length === 0) return { ok: false, reason: 'no answerGuide' };
  if (guide.some(line => CLOZE_TARIFF.test(line))) return parseCloze(source);

  const stroke = /\bstroke\b/i.test(source.markingGuideNote);
  const drafts: Draft[] = [];
  const directions: string[] = [];
  const candidates: string[] = [];
  let part: string | undefined;
  let perRow: number | undefined;
  let headerCount: number | undefined;
  let ladderTerms: number[] | undefined;
  const ladderEntries = new Map<number, number>();

  const pushPriced = (bare: string, kind: Draft['kind'], partial: boolean) => {
    const priced = TRAILING_PRICE.exec(bare);
    if (!priced) return false;
    const text = tidy(bare.slice(0, priced.index));
    if (!text) return false;
    drafts.push({ text, marks: Number(priced[1]), kind, part, ...(partial ? { partial: true } : {}) });
    const footnote = priced[2] ?? priced[3];
    if (footnote) directions.push(tidy(footnote));
    return true;
  };

  for (const line of guide) {
    const markerMatch = MARKER.exec(line);
    const marker = markerMatch?.[1];
    const bare = tidy(line.replace(MARKER, ''));
    if (!bare) continue;
    const priced = TRAILING_PRICE.test(bare);

    if (!marker) {
      if (FURNITURE.test(bare)) {
        const count = COUNT_HEADER.exec(bare);
        if (count) headerCount = NUMBER_WORDS[(count[1] ?? count[2]).toLowerCase()];
        continue;
      }
      // "Any two of: YES:" — the count header with the first part heading on its line.
      const headed = /^((?:any\s+)?(?:one|two|three|four)\s+of\s*:)\s*([A-Z][^:]{0,40}:)$/i.exec(bare);
      if (headed && FURNITURE.test(headed[1])) {
        const count = COUNT_HEADER.exec(headed[1]);
        if (count) headerCount = NUMBER_WORDS[(count[1] ?? count[2]).toLowerCase()];
        part = headed[2];
        continue;
      }
      if (!priced && (PART.test(bare) || PART_WORD.test(bare))) { part = bare; continue; }
      const header = HEADER.exec(bare);
      if (header && HEADER_HEAD.test(header[1])) {
        const terms = header[2].split('+').map(value => Number(value.trim()));
        const word = COUNT_WORD.exec(header[1]);
        const asked = word ? NUMBER_WORDS[word[1].toLowerCase()] : undefined;
        if (terms.length > 1) {
          if (terms.every(term => term === terms[0])) { perRow = terms[0]; headerCount = terms.length; }
          else { ladderTerms = terms; headerCount = terms.length; }
        } else if (asked !== undefined && asked * terms[0] === source.totalMarks) {
          perRow = terms[0]; headerCount = asked;
        } else if (asked !== undefined) {
          ladderEntries.set(asked, terms[0]);
        } else {
          perRow = terms[0];
        }
        continue;
      }
    }

    if (DEDUCTION_CUE.test(bare)) {
      const deduction = DEDUCTION.exec(bare);
      if (deduction) {
        const figure = deduction[2] ?? deduction[3];
        const amount = /^\d+$/.test(figure) ? Number(figure) : NUMBER_WORDS[figure.toLowerCase()];
        const text = tidy(deduction[1].replace(/^Note\s*:?\s*/i, ''));
        if (text && amount) { drafts.push({ text, marks: -amount, kind: 'deduction', part }); continue; }
      }
    }

    if (marker === '➢' || CONDITION_CUE.test(bare)) {
      const head = CONDITION_HEAD.exec(bare);
      const tail = CONDITION_TAIL.exec(bare);
      if (head) { drafts.push({ text: bare, marks: Number(head[1]), kind: 'condition', part }); continue; }
      if (tail) {
        const text = tail[3].trim() ? bare : tidy(tail[1].replace(/^Note\s*:?\s*/i, '').replace(/[,.;:]\s*$/, ''));
        if (text) { drafts.push({ text, marks: Number(tail[2]), kind: 'condition', part }); continue; }
      }
      if (!priced || marker === '➢') { directions.push(line); continue; }
    }

    if (!marker) {
      // An older listening scheme prints no markers: "18 5 marks" is the answer.
      if (pushPriced(bare, 'full', false)) continue;
      if (NOT_AN_ANSWER.test(bare)) directions.push(line);
      else candidates.push(line);
      continue;
    }
    if (marker === '➢') { directions.push(line); continue; }
    if (STAR_MARKERS.has(marker) && !stroke) {
      // Under the bullet convention an asterisk is a footnote, not an answer.
      directions.push(line);
      continue;
    }
    const kind: Draft['kind'] = marker === '•' || (stroke && !STAR_MARKERS.has(marker)) ? 'full'
      : STAR_MARKERS.has(marker) ? 'star' : 'dash';
    if (pushPriced(bare, kind, kind !== 'full')) continue;
    drafts.push({ text: bare, kind, part, ...(kind !== 'full' ? { partial: true } : {}) });
  }

  // A scheme that prints one bare answer and no price at all ("Mon/Ma/Mes")
  // prices it at the paper's own tariff for the question.
  if (drafts.every(draft => draft.kind === 'deduction') && candidates.length === 1 && !ladderTerms && ladderEntries.size === 0) {
    drafts.unshift({ text: tidy(candidates[0]), marks: source.totalMarks, kind: 'full' });
  } else {
    directions.push(...candidates);
  }

  const answers = drafts.filter(draft => draft.kind !== 'deduction');
  if (answers.length === 0) return { ok: false, reason: 'no answer rows' };

  // Price the rows the scheme lists without a price of their own.
  const unpriced = answers.filter(draft => draft.marks === undefined);
  let ladder: number[] | undefined;
  if (ladderTerms || ladderEntries.size > 0) {
    if (answers.some(draft => draft.marks !== undefined)) return { ok: false, reason: 'ladder header over priced rows' };
    if (ladderTerms) ladder = cumulative(ladderTerms);
    else {
      const count = Math.max(...ladderEntries.keys());
      const steps = Array.from({ length: count }, (_, index) => ladderEntries.get(index + 1));
      if (steps.some(step => step === undefined)) return { ok: false, reason: 'ladder header misses a step' };
      ladder = steps as number[];
    }
    unpriced.forEach(draft => { draft.marks = 0; });
  } else if (unpriced.length > 0 && unpriced.length === answers.filter(draft => draft.kind !== 'condition').length && perRow === undefined && !stroke
    && (headerCount ?? (TWO_ASKED.test(source.questionText) ? 2 : undefined)) !== undefined) {
    // "Award 2 marks if answer is partially correct" beside an opinion list is the partial-credit rule, not a row.
    for (const condition of answers.filter(draft => draft.kind === 'condition')) { directions.push(condition.text); drafts.splice(drafts.indexOf(condition), 1); }
    // An opinion question ("Do you agree? … Two points"): the scheme lists the points it will accept
    // under "Any two of:" and prices them only in its general rule, so each point is the total shared
    // equally — taken only where the ledger permits that step, never typed otherwise. "Award 2 marks
    // if answer is partially correct" makes each point a row placed at 2 or at its full mark.
    const asked = headerCount ?? 2;
    const per = source.totalMarks / asked;
    if (!Number.isInteger(per) || !source.permittedMarks.includes(per)) return { ok: false, reason: `opinion points at ${per} each are not a permitted mark` };
    const partialRule = directions.map(note => /\bAward (\d+) marks? if answer is partially correct/i.exec(note)).find(Boolean);
    const partial = partialRule ? Number(partialRule[1]) : undefined;
    headerCount = asked;
    unpriced.forEach(draft => { draft.marks = per; if (partial !== undefined && partial < per && source.permittedMarks.includes(partial)) draft.steps = [partial, per]; });
  } else if (unpriced.length > 0) {
    if (perRow !== undefined) {
      unpriced.forEach(draft => { draft.marks = perRow; });
    } else if (stroke) {
      // Alternatives on consecutive stroke (or asterisk) lines share the price
      // printed against one of them; a card that prints none takes the paper's
      // own tariff, or the rule line's ladder.
      for (const draft of unpriced) {
        const index = answers.indexOf(draft);
        let lo = index; while (lo > 0 && answers[lo - 1].kind === draft.kind) lo -= 1;
        let hi = index; while (hi < answers.length - 1 && answers[hi + 1].kind === draft.kind) hi += 1;
        const run = answers.slice(lo, hi + 1).filter(other => other.marks !== undefined);
        if (run.length > 0) {
          if (new Set(run.map(other => other.marks)).size > 1) return { ok: false, reason: 'stroke alternatives at two prices' };
          draft.marks = run[0].marks;
        } else if (draft.kind !== 'full') {
          return { ok: false, reason: 'unpriced partial answer' };
        }
      }
      const still = unpriced.filter(draft => draft.marks === undefined);
      if (still.length > 0) {
        const rule = source.taskRequirements.map(line => RULE_LADDER.exec(line)).find(Boolean);
        if (rule) {
          ladderTerms = rule[3].split('+').map(value => Number(value.trim()));
          ladder = cumulative(ladderTerms);
          headerCount = NUMBER_WORDS[rule[1].toLowerCase()];
          if (ladder.length !== headerCount || ladder[ladder.length - 1] !== Number(rule[2])) return { ok: false, reason: 'rule ladder does not add up' };
          if (answers.some(draft => draft.marks !== undefined)) return { ok: false, reason: 'rule ladder over priced rows' };
          still.forEach(draft => { draft.marks = 0; });
        } else {
          const asked = headerCount ?? (TWO_ASKED.test(source.questionText) ? 2 : 1);
          if (source.totalMarks % asked !== 0) return { ok: false, reason: 'paper tariff does not split' };
          still.forEach(draft => { draft.marks = source.totalMarks / asked; });
          headerCount = asked;
        }
      }
    } else {
      return { ok: false, reason: 'unpriced bullets' };
    }
  }

  const rows: FrenchAnswerRow[] = drafts.map((draft, index) => ({
    id: `r${index + 1}`,
    text: draft.text,
    marks: draft.marks ?? 0,
    ...(draft.steps ? { steps: draft.steps } : {}),
    ...(draft.partial ? { partial: true } : {}),
    ...(draft.part ? { part: draft.part } : {}),
  }));
  const seen = new Set<string>();
  const notes = directions.filter(note => note && !seen.has(note) && seen.add(note));

  if (ladder) {
    const count = ladder.length;
    if (ladder[count - 1] !== source.totalMarks) return { ok: false, reason: `ladder ends at ${ladder[count - 1]}, total ${source.totalMarks}` };
    if (headerCount !== undefined && headerCount !== count) return { ok: false, reason: 'ladder length ≠ header count' };
    return { ok: true, allocation: { count, rows, ladder, directions: notes } };
  }

  const positive = rows.filter(row => row.marks > 0);
  const max = Math.max(0, ...positive.map(row => row.marks));
  if (max <= 0) return { ok: false, reason: 'no priced answer' };

  // The aural rule for named tasks: the higher segment score goes to both. A
  // task under it can only reach even totals, which an ordinary two-detail
  // task with the same rows cannot.
  if (source.taskRequirements.some(line => SEGMENT_RULE.test(line)) && max * 2 === source.totalMarks) {
    const plain = new Set<number>([0]);
    rows.filter(row => row.marks >= 0).forEach((row, i, all) => {
      plain.add(row.marks);
      all.slice(i + 1).forEach(other => plain.add(Math.min(source.totalMarks, row.marks + other.marks)));
    });
    const permitted = [...source.permittedMarks];
    const evenOnly = permitted.every(mark => mark % 2 === 0);
    const matchesPlain = permitted.length === plain.size && permitted.every(mark => plain.has(mark));
    if (evenOnly && !matchesPlain) {
      return { ok: true, allocation: { count: 2, rows, scoring: 'higher-segment-both', directions: notes } };
    }
  }

  if (source.totalMarks % max !== 0) return { ok: false, reason: `full mark ${max} does not divide total ${source.totalMarks}` };
  const count = source.totalMarks / max;
  if (headerCount !== undefined && headerCount !== count) return { ok: false, reason: `header says ${headerCount} answers, prices say ${count}` };
  return { ok: true, allocation: { count, rows, directions: notes } };
}

/** The allocation a card ships with, or nothing when the parser cannot place its lines. */
export function frenchAnswersFor(source: FrenchAnswerSource): FrenchAllocation | undefined {
  const result = parseFrenchAnswers(source);
  return result.ok ? result.allocation : undefined;
}

type FrenchGuidedCard = SecRubricCard & { rubric: FrenchRubric };

export const frenchAnswerSource = (card: FrenchGuidedCard): FrenchAnswerSource => ({
  id: card.id,
  totalMarks: card.totalMarks,
  questionText: card.questionText,
  answerGuide: card.rubric.answerGuide ?? [],
  taskRequirements: card.rubric.taskRequirements,
  markingGuideNote: card.rubric.markingGuideNote,
  permittedMarks: card.rubric.criteria[0]?.permittedMarks ?? [],
});

/** The card as shipped: its scheme cut into rows where the lines reconcile, untouched otherwise. */
export function withFrenchAnswers<T extends FrenchGuidedCard>(card: T): T {
  if (!card.rubric.answerGuide?.length) return card;
  const allocation = frenchAnswersFor(frenchAnswerSource(card));
  return allocation ? { ...card, rubric: { ...card.rubric, allocation } } : card;
}
