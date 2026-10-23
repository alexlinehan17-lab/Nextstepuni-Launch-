/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Geography allocation rows.
 *
 * A Geography card's scheme lines are lifted from the SEC marking scheme by
 * scripts/markbank/authoring/geography_cards.py. Until October 2026 the reveal
 * printed them as grey prose over one 0–total slider, so a student read
 * "(i) What was the magnitude of the earthquake in Afghanistan? 6.1 ⟨3m⟩" as a
 * paragraph and had to find the answer inside it. The rule since then: an
 * answer the scheme prices is a claimable row showing the answer and its
 * marks; prose is only for examiner directions (caps, named-example rules,
 * diagram conditions).
 *
 * This module cuts the lifted lines into those rows. It adds no words: a row's
 * text is a slice of one scheme line, the prompt over a group is the paper's
 * own sub-question, and where the scheme prices an answer without printing one
 * ("Tectonic plate named 3m") the row carries the scheme's wording and says so.
 * A card is structured only when its rows and SRP counts add up to the printed
 * total; any line the parser cannot place exactly keeps the whole card on the
 * prose fallback, and test/markBankGeography.test.ts pins how many cards that
 * is so the number can only fall.
 *
 * The shapes it reads, all from the 2021–2026 schemes:
 *   (i) Donegal ⟨3m⟩ · People killed ⟨3m⟩ People injured ⟨3m⟩   priced answers
 *   Two valid effects listed 3m+3m · Valid explanation 2 + 2 marks  split rows
 *   Shown 4m graded (4/2/0)                                       graded rows
 *   Two examples @ 2m each 4m                                      counted rows
 *   Description/Explanation 9 SRP's @ 3m each 27m · Discussion 12 x SRP's
 *   Explanation of formation of rock 1 6/7 x SRP's                 a shared SRP pool
 *   Formation of any two landforms @ 20m each. / For each landform: …   repeats
 */

import type {
  GeographyAllocation,
  GeographyAllocationGroup,
  GeographyAnswerRow,
  GeographySrpAllocation,
} from '../../../../types/markBank';

export interface GeographyAllocationSource {
  level: 'higher' | 'ordinary';
  totalMarks: number;
  questionText: string;
  schemeGuidance: readonly string[];
}

export type GeographyAllocationResult =
  | { ok: true; allocation: GeographyAllocation }
  | { ok: false; reason: string };

/** The mark value of one SRP on each paper, as the schemes price them. */
export const GEOGRAPHY_SRP_MARKS = { higher: 2, ordinary: 3 } as const;

const ROMAN = '(?:i|ii|iii|iv|v|vi|vii|viii|ix|x)';
const PART_LABEL = new RegExp(`^\\((${ROMAN})\\)\\s*`, 'i');
const NUMBER_WORDS: Record<string, number> = {
  one: 1, two: 2, three: 3, four: 4, five: 5, six: 6,
  seven: 7, eight: 8, nine: 9, ten: 10, eleven: 11, twelve: 12,
};
const NUMBER_WORD = Object.keys(NUMBER_WORDS).join('|');

/**
 * One priced item and the text before it. The alternatives, most specific
 * first, so "3m + 3m" is never read as "3m" twice and "9 SRP's @ 3m each 27m"
 * is never read as a 27-mark answer:
 *   SRP@   nine SRP's @ 3m each 27m      SRPx   12 x SRP's · 6/7 x SRP's
 *   SRP=   Box: 1 x SRP = 2 marks        EACH   @ 2m each 4m · @ 20m each.
 *   SUM    3m + 3m · 2 + 2 marks         GRADED 4m graded (4/2/0)
 *   BARE   3m · 2 marks
 */
const ITEM = new RegExp(String.raw`(.*?)\s*(?:` +
  String.raw`⟨?\s*(\d+|${NUMBER_WORD})\s*SRP'?s?\s*@\s*(\d+)\s*m\s*(?:each)?\.?(?:\s*⟨?\s*(\d+)\s*m(?:\s*\+\s*(\d+)\s*m)?\s*⟩?)?\s*⟩?\.?` +
  String.raw`|(\d+)(?:\/(\d+))?\s*x\s*SRP'?s?\.?` +
  String.raw`|:\s*(\d+)\s*x\s*SRP\s*=\s*(\d+)\s*marks?\.?` +
  String.raw`|@\s*(\d+)\s*(?:m|marks?)\s+each(?:\s+graded\s*\((\d+(?:\/\d+)+)\))?(?:\s+(\d+)\s*(?:m|marks?)\b)?\.?` +
  String.raw`|⟨?\s*(\d+)\s*m\s*\+\s*(\d+)\s*m\s*⟩?\.?` +
  String.raw`|⟨?\s*(\d+)\s*\+\s*(\d+)\s*(?:m|marks?)\b\s*⟩?\.?` +
  String.raw`|⟨?\s*(\d+)\s*(?:m|marks?)\s+(?:graded\s*\((\d+(?:\/\d+)+)\)|\(graded\s*(\d+(?:\/\d+)+)\)|\((\d+(?:\/\d+)+)\))\s*⟩?\.?` +
  String.raw`|(\d+(?:\/\d+)+)\s*m\b` +
  String.raw`|⟨?\s*(\d+)\s*m\b\s*⟩?\.?` +
  String.raw`|⟨?\s*(\d+)\s*marks?\b\s*⟩?\.?` +
  String.raw`)`, 'gi');

const DIRECTION = /^(?:[•➢\-–]\s*)?(?:credit|allow|accept|do not|don't|max\b|maximum|at least|the sketch|lose\b|for (?:an?|the)\b|relevant information|if\b|apply|deduct|examination without|discussion without|description without|select (?:the )?scheme|focus|naming of|the title|question is|no marks|note\b|n\.b\.|questions \d|this card practises|or\b|either\b|names may|outline map may|where features|specific examples)/i;
const FOR_EACH = /^for each\s+(.+?):?$/i;
const COUNTED_HEADER = new RegExp(`^(?:(\\d+|${NUMBER_WORD})\\s+(?:items?|features?|landforms?|aspects?|processes?|examples?|regions?|factors?)\\b.*?)(?:as follows)?:?$`, 'i');
const ANNOTATION_KEY = /^annotation use marks\b/i;
const ANNOTATION_ROW = /(?:\bN\/A\b|^valid information worth \d+ marks?\b)/i;
const TOTAL = /\b(?:sub-)?total\s+(\d+)\s*m\b\.?/gi;
const PART_TOTAL = /⟨?\[(\d+)m\]?⟩?/g;
const QUESTION_FURNITURE = /\bQ\.?\s*\d+\.?(?=\s|\()\s*/gi;

/**
 * The scheme prices an answer it does not print. The row keeps the scheme's
 * wording; the reveal says any correct answer scores. Matched on the words a
 * scheme uses for the slot, never on the absence of a word the parser expected.
 */
const TARIFF_ONLY = /\b(?:named|identified|stated|chosen|listed|explained|described|outlined|given|valid|any|answer|explanation|reason|example|suitable|appropriate|relevant|correct|title|factor|process|landform|feature|impact|shown|outline|aspect|diagram|graph)\b/i;

const normalise = (value: string) => value.toLowerCase().replace(/[^a-z0-9]+/g, '');

const tidy = (value: string) => value
  .replace(/\s+/g, ' ')
  .replace(/^[•➢]\s*/, '')
  .replace(/^[.,;:\s]+|[.,;:\s]+$/g, '')
  .trim();

/** The paper's sub-questions by roman label, first printed line of each. */
function subQuestions(questionText: string): Map<string, string> {
  const out = new Map<string, string>();
  for (const line of questionText.split('\n')) {
    const match = line.trim().match(PART_LABEL);
    if (!match) continue;
    const label = match[1].toLowerCase();
    if (!out.has(label)) out.set(label, line.trim().slice(match[0].length).trim());
  }
  return out;
}

/**
 * Split "What was the magnitude of the earthquake in Afghanistan? 6.1" into
 * the paper's sub-question and the answer after it. The split point is found
 * by matching normalised text, so the prompt comes back as the scheme line
 * prints it, never retyped.
 */
function splitPrompt(text: string, subQuestion: string | undefined): { prompt?: string; answer: string } {
  if (!subQuestion) return { answer: text };
  const target = normalise(subQuestion);
  if (!target || !normalise(text).startsWith(target)) return { answer: text };
  let consumed = '';
  let index = 0;
  while (index < text.length && normalise(consumed).length < target.length) {
    consumed += text[index];
    index += 1;
  }
  // Keep the question mark with the question, not the answer.
  const punctuation = text.slice(index).match(/^[\s?.!:;,]+/);
  if (punctuation) { consumed += punctuation[0]; index += punctuation[0].length; }
  return { prompt: tidy(consumed), answer: text.slice(index).trim() };
}

const countIn = (text: string): number | undefined => {
  const match = text.match(new RegExp(`\\b(\\d+|${NUMBER_WORD})\\b`, 'i'));
  if (!match) return undefined;
  return NUMBER_WORDS[match[1].toLowerCase()] ?? Number(match[1]);
};

type Item =
  | { kind: 'row'; text: string; marks: number; steps?: number[] }
  | { kind: 'srp'; label: string; min: number; max: number; marks: number; printedTotal?: number }
  | { kind: 'repeat'; label: string; unitMarks: number };

function itemsOf(source: string, level: GeographyAllocationSource['level'], totalMarks: number): { items: Item[]; trailing: string } | { error: string } {
  const items: Item[] = [];
  let last = 0;
  // "274m" is a height, not a price: nothing on a card is worth more than the card.
  const line = source.replace(/\b(\d+)\s*(m|marks?)\b/gi, (whole, digits: string, unit: string) =>
    Number(digits) > totalMarks ? `${digits}\u2060${unit}` : whole);
  ITEM.lastIndex = 0;
  for (let match = ITEM.exec(line); match; match = ITEM.exec(line)) {
    if (match[0].length === 0) { ITEM.lastIndex += 1; continue; }
    const [, before, srpWord, srpEach, srpTotalA, srpTotalB, srpMin, srpMax, eqCount, eqTotal, eachMarks, eachLadder, eachTotal, sumA, sumB, plusA, plusB, gradedMarks, ladderA, ladderB, ladderC, bareLadder, bareM, bareMarks] = match;
    const srpTotal = srpTotalA ? Number(srpTotalA) + Number(srpTotalB ?? 0) : undefined;
    const ladder = ladderA ?? ladderB ?? ladderC ?? bareLadder;
    // "Grid reference 3/1/0m" prices the row at the top of its ladder.
    const graded = gradedMarks ?? (bareLadder ? String(Math.max(...bareLadder.split('/').map(Number))) : undefined);
    const text = tidy(before).replace(/\u2060/g, '');
    last = ITEM.lastIndex;
    if (srpWord) {
      const count = NUMBER_WORDS[srpWord.toLowerCase()] ?? Number(srpWord);
      const marks = Number(srpEach);
      items.push({ kind: 'srp', label: text, min: count, max: count, marks, printedTotal: srpTotal });
    } else if (srpMin) {
      const a = Number(srpMin); const b = srpMax ? Number(srpMax) : a;
      items.push({ kind: 'srp', label: text, min: Math.min(a, b), max: Math.max(a, b), marks: GEOGRAPHY_SRP_MARKS[level] });
    } else if (eqCount) {
      const count = Number(eqCount); const total = Number(eqTotal);
      if (total % count !== 0) return { error: `SRP line does not multiply out: ${line}` };
      items.push({ kind: 'srp', label: text, min: count, max: count, marks: total / count });
    } else if (eachMarks) {
      const each = Number(eachMarks);
      if (eachTotal) {
        const total = Number(eachTotal);
        if (total % each !== 0) return { error: `count line does not multiply out: ${line}` };
        // "5 items @ 3m each graded (3/1/0) 15m": every item is graded, so any
        // whole number of marks up to the total can be earned.
        const steps = eachLadder
          ? Array.from({ length: total }, (_, index) => index + 1)
          : Array.from({ length: total / each }, (_, index) => each * (index + 1));
        items.push({ kind: 'row', text, marks: total, steps: steps.length > 1 ? steps : undefined });
      } else {
        items.push({ kind: 'repeat', label: text, unitMarks: each });
      }
    } else if (sumA || plusA) {
      const a = Number(sumA ?? plusA); const b = Number(sumB ?? plusB);
      items.push({ kind: 'row', text, marks: a + b, steps: [a, a + b] });
    } else if (graded) {
      const marks = Number(graded);
      const steps = [...new Set(ladder.split('/').map(Number))].filter(step => step > 0 && step <= marks).sort((a, b) => a - b);
      items.push({ kind: 'row', text, marks, steps: steps.length > 1 ? steps : undefined });
    } else {
      items.push({ kind: 'row', text, marks: Number(bareM ?? bareMarks) });
    }
  }
  const final = items[items.length - 1];
  if (items.length > 1 && final.kind === 'row' && !final.text && !final.steps) {
    const rest = items.slice(0, -1).reduce((sum, item) =>
      sum + (item.kind === 'row' ? item.marks : item.kind === 'srp' ? item.max * item.marks : 0), 0);
    if (rest === final.marks) items.pop();
  }
  return { items, trailing: line.slice(last).replace(/\u2060/g, '').trim() };
}

interface Repeat { group: GeographyAllocationGroup; unitMarks: number; count?: number }

export function tryParseGeographyAllocation(card: GeographyAllocationSource): GeographyAllocationResult {
  const parts = subQuestions(card.questionText);
  const groups: GeographyAllocationGroup[] = [];
  const directions: string[] = [];
  let printedTotal: number | undefined;
  let rowCount = 0;
  let srpCount = 0;
  let repeat: Repeat | undefined;
  let pooled = false;
  let inAnnotationKey = false;
  // What the previous line became, so a wrapped line can rejoin it.
  let last: 'direction' | 'prompt' | 'other' = 'other';

  const current = (): GeographyAllocationGroup => {
    if (repeat) return repeat.group;
    if (!groups.length) groups.push({ rows: [], srp: [] });
    return groups[groups.length - 1];
  };
  const openGroup = (part: string | undefined, prompt: string | undefined) => {
    repeat = undefined;
    groups.push({ part: part ? `(${part})` : undefined, prompt, rows: [], srp: [] });
  };
  const unitSum = (group: GeographyAllocationGroup) =>
    group.rows.reduce((sum, row) => sum + row.marks, 0) + group.srp.reduce((sum, srp) => sum + srp.count * srp.marks, 0);
  const addRow = (text: string, marks: number, steps?: number[]): string | undefined => {
    const group = current();
    let words = text;
    if (!words) {
      // The scheme prints a second price for the same slot ("2 + 2 marks" under
      // "Valid explanation 2 + 2 marks"), or prices the sub-question itself.
      words = group.rows.length ? group.rows[group.rows.length - 1].text : (group.prompt ?? '');
      if (!words) return 'a price with nothing before it';
    }
    rowCount += 1;
    const row: GeographyAnswerRow = { id: `r${rowCount}`, text: words, marks };
    if (steps) row.steps = steps;
    if (!text || TARIFF_ONLY.test(words)) row.tariffOnly = true;
    group.rows.push(row);
    if (repeat && Number.isFinite(repeat.unitMarks) && unitSum(repeat.group) >= repeat.unitMarks) repeat = undefined;
    return undefined;
  };

  const branches: number[] = [];
  // One printed line can carry the end of the question, the part's total and
  // the first allocation ("• Fold mountains ⟨[30m]⟩ Example 2 + 2 marks"):
  // cut it at each bullet and at the total so each piece is read on its own.
  const lines = card.schemeGuidance.flatMap(raw => raw.replace(/[’‘]/g, "'")
    .split(/\s(?=[•➢]\s)/)
    .flatMap(piece => piece.split(/(?<=⟨?\[\d+m\]?⟩?)\s+|\s+(?=⟨?\[\d+m\]?⟩?)/)));
  for (const raw of lines) {
    let line = raw.replace(/\s+/g, ' ').trim();
    if (!line) continue;
    if (/^or$/i.test(line)) { branches.push(groups.length); inAnnotationKey = false; repeat = undefined; continue; }

    line = line.replace(PART_TOTAL, ' ').replace(QUESTION_FURNITURE, ' ').replace(/\s+/g, ' ').trim();
    for (let match = TOTAL.exec(line); match; match = TOTAL.exec(line)) {
      if (/^total/i.test(match[0])) printedTotal = Number(match[1]);
      else if (repeat?.group.repeat) {
        // "Sub-total 25m" closes a counted unit: five items at (3 + 2) each.
        const unit = unitSum(repeat.group);
        if (!repeat.group.repeat.marks) repeat.group.repeat.marks = unit;
        if (repeat.group.repeat.count * repeat.group.repeat.marks !== Number(match[1])) {
          return { ok: false, reason: `sub-total ${match[1]}m is not ${repeat.group.repeat.count} units of ${repeat.group.repeat.marks}` };
        }
        repeat = undefined;
      }
    }
    TOTAL.lastIndex = 0;
    line = line.replace(TOTAL, ' ').replace(/\s+/g, ' ').trim();
    if (!line) continue;

    // The annotation key (how examiners mark up a script) closes a part's
    // scheme; nothing in it is an allocation. It ends at the next sub-question.
    if (ANNOTATION_KEY.test(line)) { inAnnotationKey = true; continue; }
    if (PART_LABEL.test(line)) inAnnotationKey = false;
    if (inAnnotationKey || ANNOTATION_ROW.test(line)) continue;
    // Page furniture welded onto a Part One line: "Total 10m 5", "… 4 4", "Page 12 of 60".
    line = line.replace(/\s+(?:of \d+|Page \d+)$/i, '').replace(/(?:\s+\d{1,2})+$/, '').trim();

    // A line that opens in lower case is the tail of the line above it: a
    // wrapped direction, or a wrapped sub-question.
    if (/^[a-z]/.test(line) && !PART_LABEL.test(line)) {
      if (last === 'direction' && directions.length) {
        directions[directions.length - 1] = tidy(`${directions[directions.length - 1]} ${line}`);
        continue;
      }
      if (last === 'prompt' && groups.length && groups[groups.length - 1].prompt) {
        const group = groups[groups.length - 1];
        group.prompt = tidy(`${group.prompt} ${line}`);
        continue;
      }
    }
    last = 'other';
    // "0 marks" is a direction; the 0 at the foot of a ladder ("3/1/0m") is not.
    if (/(?<![/\d])0\s*(?:marks?|m)\b|\bdeduct\b|\bmust\b/i.test(line) || DIRECTION.test(line)
      || (/\bSRP/i.test(line) && /\b(?:credit|allow|further|max|from (?:the )?(?:description|examination|discussion|explanation)|if only|in total)\b/i.test(line))) {
      directions.push(tidy(line));
      last = 'direction';
      continue;
    }

    const forEach = line.match(FOR_EACH);
    if (forEach) {
      if (repeat?.group.repeat) repeat.group.repeat.unit = tidy(forEach[1]);
      else directions.push(tidy(line));
      continue;
    }

    const scanned = itemsOf(line, card.level, card.totalMarks);
    if ('error' in scanned) return { ok: false, reason: scanned.error };
    const { items, trailing } = scanned;

    if (!items.length) {
      const label = line.match(PART_LABEL);
      const counted = line.match(COUNTED_HEADER);
      if (label) { openGroup(label[1].toLowerCase(), tidy(line.slice(label[0].length)) || parts.get(label[1].toLowerCase())); last = 'prompt'; }
      else if (counted) {
        const group: GeographyAllocationGroup = {
          prompt: tidy(line.replace(/:$/, '')),
          rows: [], srp: [],
          repeat: { count: NUMBER_WORDS[counted[1].toLowerCase()] ?? Number(counted[1]), unit: '', marks: 0 },
        };
        groups.push(group);
        repeat = { group, unitMarks: Number.POSITIVE_INFINITY, count: group.repeat!.count };
      } else { directions.push(tidy(line)); last = 'direction'; }
      continue;
    }
    if (trailing) {
      if (/^\(e\.g\./i.test(trailing)) directions.push(tidy(trailing.replace(/^\(|\)$/g, '')));
      else return { ok: false, reason: `text after the last price: ${raw}` };
    }

    for (const item of items) {
      let text = item.kind === 'srp' ? item.label : item.kind === 'repeat' ? item.label : item.text;
      // A part label after the first word means two columns of a table were
      // read across ("(i) D (ii) (Erosion) 2m"): the words no longer belong together.
      if (new RegExp(`\\S\\s+\\(${ROMAN}\\)\\s`, 'i').test(text)) {
        return { ok: false, reason: `two columns read across: ${raw}` };
      }
      const label = text.match(PART_LABEL);
      if (label) {
        const part = label[1].toLowerCase();
        const split = splitPrompt(text.slice(label[0].length).trim(), parts.get(part));
        openGroup(part, split.prompt ?? parts.get(part));
        text = split.answer;
      } else if (item.kind === 'row' && /\?/.test(text) && groups.length) {
        text = splitPrompt(text, current().prompt).answer;
      }

      if (item.kind === 'repeat') {
        const group: GeographyAllocationGroup = {
          prompt: tidy(text) || undefined,
          rows: [], srp: [],
          repeat: { count: countIn(text) ?? 0, unit: '', marks: item.unitMarks },
        };
        groups.push(group);
        repeat = { group, unitMarks: item.unitMarks, count: group.repeat!.count || undefined };
        continue;
      }
      if (item.kind === 'srp') {
        if (item.printedTotal !== undefined && item.printedTotal !== item.max * item.marks
          && !(repeat?.count && item.printedTotal === item.max * item.marks * repeat.count)) {
          return { ok: false, reason: `SRP line does not multiply out: ${raw}` };
        }
        srpCount += 1;
        const srp: GeographySrpAllocation = { id: `s${srpCount}`, label: tidy(text), count: item.max, marks: item.marks };
        if (item.min !== item.max) { srp.min = item.min; pooled = true; }
        current().srp.push(srp);
        if (repeat && Number.isFinite(repeat.unitMarks) && unitSum(repeat.group) >= repeat.unitMarks) repeat = undefined;
        continue;
      }
      const problem = addRow(tidy(text), item.marks, item.steps);
      if (problem) return { ok: false, reason: `${problem}: ${raw}` };
    }
  }

  if (branches.length) {
    // The scheme prints alternatives; the card practises one of them. Keep the
    // branch whose part label the card's question opens with.
    const wanted = card.questionText.trim().match(PART_LABEL)?.[1].toLowerCase();
    const bounds = [0, ...branches, groups.length];
    const keep = bounds.slice(0, -1).map((start, index) => groups.slice(start, bounds[index + 1]))
      .find(branch => wanted && branch.some(group => group.part === `(${wanted})`));
    if (!keep) return { ok: false, reason: 'the scheme prints alternatives and none opens with the card\'s part' };
    groups.splice(0, groups.length, ...keep);
  }
  // An SRP line that only sums the lines after it ("10 SRP's @ 3m each" over
  // "Region 1: 5 SRP's" and "Region 2: 5 SRP's") is a heading, not a third part.
  for (const group of groups) {
    for (let index = 0; index < group.srp.length; index += 1) {
      const head = group.srp[index];
      const tail = group.srp.slice(index + 1);
      const rest = tail.reduce((sum, srp) => sum + srp.count * srp.marks, 0);
      if (tail.length >= 2 && head.min === undefined && rest === head.count * head.marks) { group.srp.splice(index, 1); index -= 1; }
    }
  }
  if (printedTotal !== undefined && printedTotal !== card.totalMarks) {
    return { ok: false, reason: `scheme prints Total ${printedTotal}m on a ${card.totalMarks}-mark card` };
  }
  if (!rowCount && !srpCount) return { ok: false, reason: 'no priced line' };

  // Reconcile. A repeat counts its unit `count` times; a count the scheme
  // leaves to the total is what the other items leave over.
  let fixed = 0;
  let poolMin = 0; let poolMax = 0; let poolMarks = 0;
  const open: GeographyAllocationGroup[] = [];
  for (const group of groups) {
    if (group.repeat) {
      const unit = unitSum(group);
      if (!group.repeat.marks) group.repeat.marks = unit;
      if (unit !== group.repeat.marks) return { ok: false, reason: `repeat unit adds to ${unit}, scheme prices ${group.repeat.marks} each` };
      if (group.repeat.count) fixed += group.repeat.count * unit;
      else open.push(group);
      continue;
    }
    fixed += group.rows.reduce((sum, row) => sum + row.marks, 0);
    for (const srp of group.srp) {
      if (srp.min === undefined) fixed += srp.count * srp.marks;
      else { poolMin += srp.min; poolMax += srp.count; poolMarks = srp.marks; }
    }
  }
  if (open.length > 1) return { ok: false, reason: 'two repeats without counts' };
  if (open.length === 1) {
    const unit = unitSum(open[0]);
    const left = card.totalMarks - fixed;
    if (left <= 0 || left % unit !== 0) return { ok: false, reason: `repeat does not divide the remaining ${left} marks` };
    open[0].repeat!.count = left / unit;
    fixed += left;
  }
  let srpPool: GeographyAllocation['srpPool'];
  if (pooled) {
    const left = card.totalMarks - fixed;
    if (left <= 0 || left % poolMarks !== 0) return { ok: false, reason: `SRP pool does not divide the remaining ${left} marks` };
    const count = left / poolMarks;
    if (count < poolMin || count > poolMax) return { ok: false, reason: `SRP pool of ${count} outside ${poolMin}–${poolMax}` };
    srpPool = { count, marks: poolMarks };
    fixed += left;
  }
  if (fixed !== card.totalMarks) return { ok: false, reason: `rows add to ${fixed}, card is ${card.totalMarks}` };

  for (const group of groups) {
    if (group.repeat && !group.repeat.unit) group.repeat.unit = group.prompt ?? '';
  }
  const question = normalise(card.questionText);
  const allocation: GeographyAllocation = {
    groups: groups.filter(group => group.rows.length || group.srp.length || group.prompt),
    // A bullet that only restates the printed task is not a direction.
    directions: directions.filter(note => !question.includes(normalise(note))),
  };
  if (srpPool) allocation.srpPool = srpPool;
  return { ok: true, allocation };
}

export const parseGeographyAllocation = (card: GeographyAllocationSource): GeographyAllocation | undefined => {
  const result = tryParseGeographyAllocation(card);
  return result.ok ? result.allocation : undefined;
};
