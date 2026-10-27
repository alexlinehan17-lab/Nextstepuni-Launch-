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
  GeographyChoiceOption,
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

// ---------------------------------------------------------------------------
// Reviewed criteria, 2010–2026.
//
// Since the 2010–2026 review (scripts/markbank/authoring/geography_review.py
// and its per-sitting ledgers) every Geography card carries one criterion per
// published allocation line, each with the marks the scheme can award
// (`permittedMarks`). The reveal still printed each criterion's lines as grey
// text over number buttons. This section cuts one criterion's lines into rows
// the way the whole-question parser above does, under two gates instead of
// one: the rows reach the criterion's printed maximum, and every total they
// can produce is a mark the reviewed ledger permits. The parser and the
// ledger read the same scheme page independently, so they have to agree.
//
// The lines arrive as the review lifted them, the printed cells of one row
// joined by " · ". The shapes read, beyond the notations above:
//   Mid-Ocean Ridge · E · 2 marks                  answer cells, then the price
//   (ii) · 5 marks · Transform /Transverse /Tear   the price before the answer
//   4 features @ 4 marks each: · Shown 3 marks (graded 3/1/0)   one unit of several:
//                                                  a price larger than the
//                                                  criterion is its heading
//   Five terms @ 2 marks each as follows: / Crater an answer the scheme prices
//                                                  only in its heading, so at
//                                                  the reviewed criterion's value
//   Explaining how acid rain occurs / 2 SRPs @ 3 marks each · 6 marks
//                                                  a label line, then its SRPs
//   Number of aspects · 3 @ 20 marks each · 4 @ 15 marks each / For each aspect:
//                                                  two routes, one column each
//   Overall coherence: · 7/6 marks graded          per-unit alternatives; the
//                                                  criterion's total picks one
//   Excellent · 20 · Excellent, comprehensive response …   a band table

export interface GeographyCriterionSource {
  maxMarks: number;
  permittedMarks: readonly number[];
  guidanceKind: 'exact' | 'srp';
  guidance: readonly string[];
}

export interface GeographyCriterionContext {
  level: 'higher' | 'ordinary';
  questionText: string;
  /** The card's column headings ("Bar Chart · Pie Chart"), where one of its
   *  criteria prints them over a two-route table and the others do not. */
  columnLabels?: readonly string[];
  /** The last answer of the criterion before this one, for a criterion whose
   *  line is only a second price for the same printed slot ("2 + 2 marks"
   *  under "Any two valid challenges explained @ 4 marks each 2 + 2 marks"). */
  previousRowText?: string;
  /** The printed part the card practises, "(i)" or "(ii)", for a Part One
   *  table the scheme prints as two columns on one line. */
  part?: string;
}

const CELL = ' · ';
const CRITERION_PART = /^\(((?:i|ii|iii|iv|v|vi|vii|viii|ix|x)|[a-h])\)\s*(?:·\s*)?/i;
const BAND_LINE = /^(Excellent|Very Good|Good|Fair|Weak|Poor)\s+·\s+(\d+)\s+·\s+(.+)$/;
const COUNT = `(\\d+|${NUMBER_WORD})`;
const UNIT = String.raw`\s*(?:marks?|m)\b`;
const LADDER = String.raw`(?:\s+graded\*?)?(?:\s*\(\s*(?:graded\s*)?(\d+(?:\s*\/\s*\d+)+)\s*\))?`;
/** "Total 10m", "Sub-total 25 marks", "5 marks total": furniture on a criterion. */
const CRITERION_TOTAL = /\b(?:sub\s*[-–]?\s*)?total\s*:?\s*\d+\s*(?:marks?|m)\b\.?|\b\d+\s*(?:marks?|m)\s+total\b\.?/gi;
/** A cell that is nothing but a price ("4 marks", "8 x SRPs", "3 @ 20 marks
 *  each", "1+1 mark (Circle & Centred)"): one column of a two-route table. */
const PRICE_CELL = new RegExp(String.raw`^(?:${COUNT}\s*@\s*)?\d+(?:\s*[/+]\s*\d+)*\s*(?:x\s*SRP'?s?|(?:marks?|m)\b(?:\s+each)?(?:\s+graded\*?)?(?:\s*\([^)]*\))?)\.?$`, 'i');
const HEADING_PHRASE = /^(?:each question|sketch|.*\bas follows|.*:)$/i;
/** The scheme prices a slot without printing an answer for it: "Tectonic
 *  plate named", "Two definitions", or a numbered slot ("Use 1", "Reason 2"). */
const CRITERION_TARIFF_WORDS = new RegExp(`${TARIFF_ONLY.source.replace(/\)\\b$/, ')s?\\b')}|\\b(?:definition|statement|location|evidence|reference)s?\\b|\\b(?:naming|identifying|correctly)\\b|^[A-Z][a-z]+(?: [a-z]+)? \\d$`, 'i');
/** …unless it prints an example after all ("Any valid extrusive igneous rock e.g. Basalt"). */
const isTariff = (text: string) => CRITERION_TARIFF_WORDS.test(text) && !/\be\.g\./i.test(text);

type Scan =
  | { kind: 'row'; marks: number; steps?: number[]; alternatives?: number[] }
  | { kind: 'srp'; count: number; min?: number; marks: number; total?: number }
  | { kind: 'each'; unit: number; count?: number; total?: number; graded?: number[] | 'any' }
  | { kind: 'times'; count: number; unit: number; steps: number[] };

interface Scanned { text: string; raw: string; price: Scan; newCell: boolean }

/**
 * Every price on one line, most specific first so "9 SRPs @ 3 marks each 27
 * marks" is one SRP part, not a 27-mark answer:
 *   SRP@   9 SRPs @ 3 marks each 27 marks      SRPn   Impact identified 1 SRP 3m
 *   SRPx   14 x SRPs · 6/7 x SRPs              TIMES  2 x (2 marks graded + 1 mark)
 *   N@     3 @ 20 marks each · 7 @ 3 marks each 21 marks
 *   @      Two examples @ 2m each 4m           EACH   2m each graded (2/1/0)
 *   SUM    3 marks + 2 marks · 1+1m            ALT    7/6 marks graded
 *   GRADED 4 marks (Graded 4-2-0) · 3 marks graded · 4 marks (4/0)
 *   LADDER 3/1/0m                              BARE   2 marks
 */
const CRITERION_PRICE = new RegExp(String.raw`(.*?)\s*(?:` +
  String.raw`${COUNT}\s*SRP'?s?\s*@\s*(\d+)${UNIT}(?:\s*each)?(?:\s+graded)?\.?(?:\s*⟨?\s*((?:\d+${UNIT}\s*\+\s*)*\d+)${UNIT}\s*⟩?)?` +
  String.raw`|${COUNT}\s*SRP'?s?\s*⟨?\s*((?:\d+${UNIT}\s*\+\s*)*\d+)${UNIT}\s*⟩?` +
  String.raw`|(\d+)(?:\s*\/\s*(\d+))?\s*x\s*SRP'?s?\.?` +
  String.raw`|${COUNT}\s*x\s*\(\s*((?:\d+${UNIT}(?:\s+graded)?\s*\+\s*)+\d+${UNIT}(?:\s+graded)?)\s*\)` +
  String.raw`|${COUNT}\s*@\s*(\d+)${UNIT}(?:\s*each)?${LADDER}\.?(?:\s*(\d+)${UNIT})?` +
  String.raw`|@\s*(\d+)${UNIT}(?:\s+each)?${LADDER}\.?(?:\s*(\d+)${UNIT}(?:\s+(?:graded|each)\b)?)?` +
  String.raw`|(\d+)${UNIT}\s+each\b${LADDER}\.?` +
  String.raw`|((?:\d+(?:${UNIT})?\s*\+\s*)+\d+)${UNIT}` +
  String.raw`|(\d+(?:\/\d+)+)${UNIT}\s+graded\b\*?` +
  String.raw`|⟨?\s*(\d+)${UNIT}\s*(?:graded\*?)?\s*\(\s*(?:graded\s*)?(\d+(?:\s*[/-]\s*\d+)+)\s*\)?\s*⟩?` +
  String.raw`|(\d+)${UNIT}\s+graded\b\*?` +
  String.raw`|(\d+(?:\/\d+)+)\s*m\b` +
  String.raw`|⟨?\s*(\d+)${UNIT}\s*⟩?` +
  String.raw`)`, 'gi');

const numberOf = (value: string) => NUMBER_WORDS[value.toLowerCase()] ?? Number(value);
const ladderOf = (value: string) => [...new Set(value.split(/\s*[/-]\s*/).map(Number))]
  .filter(step => step > 0).sort((a, b) => a - b);
const upTo = (marks: number) => Array.from({ length: marks }, (_, index) => index + 1);
const addSets = (a: Iterable<number>, b: Iterable<number>) => {
  const out = new Set<number>();
  for (const x of a) for (const y of b) out.add(x + y);
  return out;
};
/** Every non-zero total reachable by awarding any value from each part. */
const reachable = (parts: number[][]) => {
  let totals = new Set([0]);
  for (const values of parts) totals = addSets(totals, [0, ...values]);
  return [...totals].filter(total => total > 0).sort((a, b) => a - b);
};
/** The count a heading names, never an adjective ("six figure grid reference"). */
const countOf = (text: string) => countIn(text.replace(/\b(?:six|6)[- ]figure\b/gi, ''));
/** A row or label as printed, with cell dividers, joiners and unmatched brackets trimmed. */
const tidyCell = (value: string) => {
  let out = tidy(value.replace(/\u2060/g, '').replace(/^\*\s*/, '')
    .replace(/^(?:[·:=;]\s*)+|(?:\s*[·:=;])+$/g, '')
    .replace(/\s+(?:for|=)$/i, ''));
  for (let changed = true; changed;) {
    const before = out;
    if (/^[([]/.test(out) && !/[)\]]/.test(out)) out = out.slice(1).trim();
    if (/[)\]]$/.test(out) && !/[([]/.test(out)) out = out.slice(0, -1).trim();
    if (/[([]$/.test(out)) out = out.slice(0, -1).trim();
    out = tidy(out.replace(/^(?:[·:=;]\s*)+|(?:\s*[·:=;])+$/g, ''));
    changed = out !== before;
  }
  return out;
};

/** "274m" or "2,000m" on a criterion worth 2 is a height: hide it from the price reader. */
function guardFigures(line: string, maxMarks: number): string {
  // A figure inside a sum ("4m + 3m + 3m") is a price whatever its size.
  return line.replace(/(\+\s*)?(\d+(?:[.,]\d+)*)\s*(m|marks?)\b(?!\s*\+)/gi, (whole, plus: string | undefined, digits: string, unit: string) =>
    !plus && (/[.,]/.test(digits) || Number(digits) > maxMarks) ? `${digits}\u2060${unit}` : whole);
}

/** Join a price to the cells that complete it: "@ · 3 marks each · 27 marks"
 *  reads as one price, "6.1 · 3m" as an answer and its price. Two prices in
 *  separate cells ("4 marks · 3 marks") are two columns and stay apart. */
function joinPriceCells(line: string): string {
  return line
    .replace(/\s·\s(?=@)/g, ' ').replace(/@\s·\s/g, '@ ')
    // "@ 3m + 2m" prices a sum, not one unit of several.
    .replace(/@\s*(?=\d+\s*(?:marks?|m)?\s*\+)/gi, '')
    .replace(/(\beach\.?|\bSRP'?s?|\bgraded|\))\s·\s(?=⟨?\d+\s*(?:marks?|m)\b)/gi, '$1 ')
    // "@ 20 marks = · 40 marks": the total after an equals sign.
    .replace(/(\b(?:marks?|m|each))\s*=\s*(?:·\s*)?(?=\d+\s*(?:marks?|m)\b)/gi, '$1 ')
    // "4m graded · (4/2/0)": the ladder in the next cell.
    .replace(/(\bgraded)\s·\s(?=\()/gi, '$1 ');
}

/** What one scanned price is worth at most (an SRP part at the paper's rate). */
function scannedValue(item: Scanned, srpMarks: number): number {
  const price = item.price;
  if (price.kind === 'row') return price.marks;
  if (price.kind === 'srp') return price.min === undefined ? price.count * (price.marks || srpMarks) : 0;
  if (price.kind === 'times') return price.count * price.unit;
  const count = price.count ?? countOf(item.text);
  return price.total ?? (count ? count * price.unit : price.unit);
}

export function scanCriterionLine(source: string, maxMarks: number, srpMarks = 0): { items: Scanned[]; trailing: string } {
  // A figure larger than the criterion is an answer ("50m", "274m"), not a price.
  const line = guardFigures(source, maxMarks);
  const items: Scanned[] = [];
  let last = 0;
  CRITERION_PRICE.lastIndex = 0;
  for (let match = CRITERION_PRICE.exec(line); match; match = CRITERION_PRICE.exec(line)) {
    if (match[0].length === 0) { CRITERION_PRICE.lastIndex += 1; continue; }
    const [whole, before,
      srpAtCount, srpAtEach, srpAtTotal,
      srpNCount, srpNTotal,
      srpXa, srpXb,
      timesCount, timesUnit,
      nAtCount, nAtUnit, nAtLadder, nAtTotal,
      atUnit, atLadder, atTotal,
      eachUnit, eachLadder,
      sum,
      altMarks,
      gradedMarks, gradedLadder,
      gradedAny,
      bareLadder,
      bare] = match;
    const added = (value: string) => (value.match(/\d+/g) ?? []).map(Number).reduce((a, b) => a + b, 0);
    const graded = (ladder: string | undefined) => ladder ? ladderOf(ladder) : /graded/i.test(whole) ? 'any' as const : undefined;
    let price: Scan;
    if (srpAtCount) {
      price = { kind: 'srp', count: numberOf(srpAtCount), marks: Number(srpAtEach), total: srpAtTotal ? added(srpAtTotal) : undefined };
    } else if (srpNCount) {
      const count = numberOf(srpNCount); const total = added(srpNTotal);
      price = { kind: 'srp', count, marks: total / count, total };
    } else if (srpXa) {
      const a = Number(srpXa); const b = srpXb ? Number(srpXb) : a;
      price = { kind: 'srp', count: Math.max(a, b), min: a === b ? undefined : Math.min(a, b), marks: 0 };
    } else if (timesCount) {
      // "2 x (2 marks graded + 1 mark)": each part graded or whole, the unit twice.
      const parts = timesUnit.split('+').map(part => {
        const marks = Number(part.match(/\d+/)![0]);
        return /graded/i.test(part) ? upTo(marks) : [marks];
      });
      const unit = parts.reduce((total, values) => total + Math.max(...values), 0);
      price = { kind: 'times', count: numberOf(timesCount), unit, steps: reachable(parts) };
    } else if (nAtCount) {
      price = { kind: 'each', count: numberOf(nAtCount), unit: Number(nAtUnit), total: nAtTotal ? Number(nAtTotal) : undefined, graded: graded(nAtLadder) };
    } else if (atUnit) {
      price = { kind: 'each', unit: Number(atUnit), total: atTotal ? Number(atTotal) : undefined, graded: graded(atLadder) };
    } else if (eachUnit) {
      price = { kind: 'each', unit: Number(eachUnit), graded: graded(eachLadder) };
    } else if (sum) {
      const addends = (sum.match(/\d+/g) ?? []).map(Number);
      price = { kind: 'row', marks: addends.reduce((a, b) => a + b, 0), steps: reachable(addends.map(value => [value])) };
    } else if (altMarks) {
      // "7/6 marks graded": one value per unit; the criterion's total picks it.
      const alternatives = altMarks.split('/').map(Number);
      price = { kind: 'row', marks: alternatives[0], steps: upTo(alternatives[0]), alternatives };
    } else if (gradedMarks) {
      const marks = Number(gradedMarks);
      const steps = ladderOf(gradedLadder).filter(step => step <= marks);
      price = { kind: 'row', marks, steps: steps.length > 1 ? steps : undefined };
    } else if (gradedAny) {
      const marks = Number(gradedAny);
      price = { kind: 'row', marks, steps: marks > 1 ? upTo(marks) : undefined };
    } else if (bareLadder) {
      const steps = ladderOf(bareLadder);
      price = { kind: 'row', marks: Math.max(...steps), steps: steps.length > 1 ? steps : undefined };
    } else {
      price = { kind: 'row', marks: Number(bare) };
    }
    const newCell = items.length === 0 || /·/.test(before);
    const previous = items[items.length - 1];
    // The same price printed again in the next column ("2 marks each graded ·
    // 2 marks each graded") is that column's copy, not a second answer.
    if (previous && !tidyCell(before) && whole.replace(/[\s·]/g, '') === previous.raw.slice(previous.text.length).replace(/[\s·]/g, '')) {
      last = CRITERION_PRICE.lastIndex;
      continue;
    }
    items.push({ text: before, raw: whole, price, newCell });
    last = CRITERION_PRICE.lastIndex;
  }
  // A last cell that only restates the line's total ("… 1 SRP @ 3m · 3m",
  // "Two reasons identified @ 3m + 2m · 5m") is the total, not a second answer.
  const final = items[items.length - 1];
  if (items.length > 1 && final.price.kind === 'row' && !final.price.steps && !tidyCell(final.text)) {
    const before = items.slice(0, -1).reduce((total, item) => total + scannedValue(item, srpMarks), 0);
    if (before === final.price.marks) items.pop();
  }
  return { items, trailing: line.slice(last).replace(/\u2060/g, '') };
}

/** Every total a student can claim from an allocation. */
export function geographyAchievable(allocation: GeographyAllocation): Set<number> {
  if (allocation.choice) {
    const out = new Set<number>([0]);
    for (const option of allocation.choice.options) {
      if (option.allocation) for (const mark of geographyAchievable(option.allocation)) out.add(mark);
      else if (option.marks !== undefined) out.add(option.marks);
    }
    return out;
  }
  let total = new Set([0]);
  for (const group of allocation.groups) {
    let unit = new Set([0]);
    for (const row of group.rows) unit = addSets(unit, [0, ...(row.steps ?? [row.marks])]);
    for (const srp of group.srp) {
      if (srp.min !== undefined) continue;
      unit = addSets(unit, Array.from({ length: srp.count + 1 }, (_, index) => index * srp.marks));
    }
    for (let index = 0; index < (group.repeat?.count ?? 1); index += 1) total = addSets(total, unit);
  }
  const pool = allocation.srpPool;
  if (pool) total = addSets(total, Array.from({ length: pool.count + 1 }, (_, index) => index * pool.marks));
  return total;
}

/** The most an allocation can award. */
export function geographyAllocationMax(allocation: GeographyAllocation): number {
  if (allocation.choice) {
    return Math.max(0, ...allocation.choice.options.map(option =>
      option.allocation ? geographyAllocationMax(option.allocation) : option.marks ?? 0));
  }
  let total = 0;
  for (const group of allocation.groups) {
    const unit = group.rows.reduce((sum, row) => sum + row.marks, 0)
      + group.srp.reduce((sum, srp) => sum + (srp.min === undefined ? srp.count * srp.marks : 0), 0);
    total += unit * (group.repeat?.count ?? 1);
  }
  if (allocation.srpPool) total += allocation.srpPool.count * allocation.srpPool.marks;
  return total;
}

/** The two gates: the rows reach the maximum and claim only permitted marks. */
function reconcileCriterion(allocation: GeographyAllocation, criterion: GeographyCriterionSource): string | undefined {
  const max = geographyAllocationMax(allocation);
  if (max !== criterion.maxMarks) return `rows add to ${max}, criterion is ${criterion.maxMarks}`;
  const permitted = new Set(criterion.permittedMarks);
  const achievable = geographyAchievable(allocation);
  const outside = [...achievable].filter(mark => !permitted.has(mark)).sort((a, b) => a - b);
  if (outside.length) return `rows can claim ${outside.join('/')}, which the ledger does not permit`;
  // A ledger that permits every whole mark ("graded", no ladder printed) may
  // be met by rows that are stricter; any other ledger must be met exactly.
  const everyMark = criterion.permittedMarks.length === criterion.maxMarks + 1;
  const missing = [...permitted].filter(mark => !achievable.has(mark)).sort((a, b) => a - b);
  if (!everyMark && missing.length) return `rows cannot claim ${missing.join('/')}, which the ledger permits`;
  return undefined;
}

interface UnitResult { allocation: GeographyAllocation; headings: string[] }

/**
 * Part One tables print a letter column and a process column on one line
 * ("B River · 2m + 2m", "C Q.3 (ii) (River) · 2m", "(D) Q.3 (ii) Erosion ·
 * 2m"). Keep the cell for the card's own part and that cell's price. A cell
 * in brackets is the paper's own pre-printed entry and carries no marks.
 */
const WELDED = /^(\(?[A-F]\)?)\s+(?:Q\.?\s*\d+\s*\(ii\)\s+)?(\(?[A-Z][a-z]+\)?)\s*·\s*(\d+m)(?:\s*\+\s*(\d+m))?$/;
function weldedColumn(text: string, part: string | undefined): string {
  if (part !== '(i)' && part !== '(ii)') return text;
  const match = text.match(WELDED);
  if (!match) return text;
  const [, letter, word, first, second] = match;
  const cell = part === '(i)' ? letter : word;
  if (/^\(.*\)$/.test(cell)) return text;
  return `${cell} · ${second && part === '(ii)' ? second : first}`;
}

/** One column of a criterion's lines, as rows. */
function parseCriterionUnit(lines: readonly string[], criterion: GeographyCriterionSource,
  context: GeographyCriterionContext): UnitResult | { error: string } {
  const srpMarks = GEOGRAPHY_SRP_MARKS[context.level];
  const max = criterion.maxMarks;
  const parts = subQuestions(context.questionText);
  const directions: string[] = [];
  // Headings keep the line they were printed on, so they read in print order.
  const headings: Array<{ at: number; text: string }> = [];
  const heading = (at: number, text: string) => { if (text) headings.push({ at, text: joinPriceCells(text) }); };
  let unitNoun: string | undefined;
  interface Piece extends Scanned { line: number; demoted?: boolean }
  interface Entry { at: number; clean: string; part?: string; pieces: Piece[]; text?: string }
  const entries: Entry[] = [];

  lines.forEach((raw, lineIndex) => {
    let line = raw.replace(/[’‘]/g, "'").replace(/\s+/g, ' ').trim();
    // "(Significant Relevant Point = 2 marks)" defines the SRP; it prices nothing.
    line = line.replace(/\s*\(Significant Relevant Points? = \d+ marks?\)/i, match => {
      directions.push(tidyCell(match));
      return '';
    });
    // "(5/4/4 x SRP's)" breaks an SRP count down; "award 5 marks to all
    // candidates" is a ruling. Neither prices an answer of its own.
    line = line.replace(/\s*\(\s*\d+(?:\s*\/\s*\d+)+\s*x\s*SRP'?s?\s*\)/i, match => { directions.push(tidyCell(match)); return ''; });
    line = line.replace(/\s*·?\s*(award (\d+) marks? to all candidates)\.?/i, (_match, ruling: string, marks: string) => {
      directions.push(tidyCell(ruling));
      return ` · ${marks} marks`;
    });
    // The text layer letter-spaces a word now and then ("2 mark s").
    line = line.replace(/\bmark s\b/gi, 'marks').replace(PART_TOTAL, ' ').replace(CRITERION_TOTAL, ' ');
    // An allocation note over several questions or parts ("Q4(iv), Q9(iv) &
    // Q12(iv) @ 1 + 1 mark", "Q2 & 3 Part (i) 4 parts @ 1m") prices the answer
    // under it; it is a heading, not a row.
    const note = /(?:\bQ\.?\s*\d+\b[^Q]*){2,}@|\bparts?\b[^@]*@|@[^;]*;|^\s*Q\.?\s*\d+\s*:.*@/i.test(line);
    // Question numbers and bullets are page furniture: "Q.1 ·", "Q.3, 4, 5:", "•".
    if (!note) line = line.replace(/^\s*Q\.?\s*\d+(?:\s*[,&]\s*\d+)*\s*[.:]?(?:\s*(?=\()|\s*·\s*|\s+|$)/i, '');
    line = line.replace(/^[•➢]\s*/, '');
    line = line.replace(/\s+/g, ' ').replace(/(?:\s*·)+\s*$/, '').replace(/^\s*(?:·\s*)+/, '').trim();
    if (!line) return;
    const forEach = line.match(/^for each(?: of the)?\s+(?:\w+\s+)?([^:·]+?)\s*:\s*(?:·\s*)?(.*)$/i);
    if (forEach) {
      unitNoun = tidyCell(forEach[1]);
      heading(lineIndex, tidyCell(line.slice(0, line.length - forEach[2].length)));
      line = forEach[2];
      if (!line) return;
    }
    // "(2/1/0) · (2/1/0)" under "6 items illustrated · 2 marks each graded":
    // the ladder the line above grades by, printed a line lower.
    const ladderLine = line.match(/^\((\d+(?:\/\d+)+)\)(?:\s·\s\(\1\))*$/);
    const above = [...entries].reverse().find(entry => entry.pieces.length)?.pieces.slice(-1)[0];
    if (ladderLine && above && (above.price.kind === 'each' || above.price.kind === 'row')) {
      const ladder = ladderOf(ladderLine[1]);
      if (above.price.kind === 'each') above.price.graded = ladder;
      else if (ladder.every(step => step <= (above.price as { marks: number }).marks)) above.price.steps = ladder;
      return;
    }
    const label = note ? null : line.match(CRITERION_PART);
    const part = label ? label[1].toLowerCase() : undefined;
    let rest = label ? line.slice(label[0].length) : line;
    rest = weldedColumn(rest, context.part ?? context.questionText.trim().match(/^\((?:i|ii)\)/)?.[0]);
    // A table with a "Mark" column prints the price as a bare figure: the
    // header "Magnitude · Mark" over "6.3 · 2", or "First evidence 4". A bare
    // final figure is a price only when it is the criterion's own value.
    const markHeader = rest.match(/^(.+?)\s·\s(?:Marks?)$/i);
    if (markHeader) { heading(lineIndex, tidyCell(markHeader[1])); return; }
    const bareFigure = rest.match(/^(.*\S)(?:\s·\s|\s+)(\d+)$/);
    if (bareFigure && Number(bareFigure[2]) === max && /[A-Za-z0-9]/.test(bareFigure[1])
      && !/(?:marks?|m)\b|[+@/]$/i.test(bareFigure[1].split(CELL).pop() ?? '')) {
      rest = `${bareFigure[1]} · ${bareFigure[2]} marks`;
    }
    const clean = tidyCell(line);
    // "(ii) Award 2m (ambiguous wording)": a ruling that awards the part to
    // everyone. The row is the ruling as printed, at its own price.
    const ruling = !note && rest.match(/^award\s+(\d+)\s*(?:marks?|m)\b.*$/i);
    if (ruling) {
      const price: Scan = { kind: 'row', marks: Number(ruling[1]) };
      entries.push({ at: lineIndex, clean, part, pieces: [{ text: tidyCell(rest), raw: rest, price, newCell: true, line: lineIndex }] });
      return;
    }
    const { items, trailing } = scanCriterionLine(joinPriceCells(rest), max, srpMarks);
    if (note) {
      heading(lineIndex, tidyCell(line));
      return;
    }
    if (!items.length) {
      entries.push({ at: lineIndex, clean, part, pieces: [], text: tidyCell(rest) });
      return;
    }
    // "Five terms @ 2 marks each as follows:" — the heading's own words; "Three
    // named @ 3 marks each · 9 marks" — the heading's total, larger than this criterion.
    const tail = /^\s*(?:as follows)?\s*[:=]?\s*$/i.test(trailing) || /^\s*·?\s*\d+\s*(?:marks?|m)(?:\s+graded)?\s*$/i.test(trailing)
      ? '' : tidyCell(trailing);
    if (tail) {
      const lastItem = items[items.length - 1];
      // 2010–2013 print the price first: "(ii) · 5 marks · Transform /Transverse".
      if (!tidyCell(lastItem.text)) lastItem.text = tail;
      else if (/^\(.*\)$/.test(tail)) lastItem.text = `${lastItem.text} ${tail}`;
      else { entries.push({ at: lineIndex, clean, part, pieces: [], text: `\u0000${raw}` }); return; }
    }
    entries.push({ at: lineIndex, clean, part, pieces: items.map(item => ({ ...item, line: lineIndex })) });
  });
  const broken = entries.find(entry => entry.text?.startsWith('\u0000'));
  if (broken) return { error: `text after the last price: ${broken.text!.slice(1)}` };

  const pieces = entries.flatMap(entry => entry.pieces);
  const value = (piece: Piece) => scannedValue(piece, srpMarks);
  const live = () => pieces.filter(piece => !piece.demoted);
  const sum = () => live().reduce((total, piece) => total + value(piece), 0);
  const answers = entries.filter(entry => !entry.pieces.length && entry.text && !HEADING_PHRASE.test(entry.text));

  // A heading over repeated units: "3 @ 20 marks each" over "Identifying
  // aspect 4 marks" and "Examination 8 x SRPs".
  let repeat: { count: number; marks: number } | undefined;
  const head = pieces[0];
  if (head?.price.kind === 'each' && head.price.total === undefined) {
    const count = head.price.count ?? countOf(head.text);
    const others = pieces.slice(1).reduce((total, piece) => total + value(piece), 0);
    if (count && count > 1 && count * head.price.unit === max && others === head.price.unit && pieces.length > 1) {
      repeat = { count, marks: head.price.unit };
      head.demoted = true;
    }
  }
  // A heading's words that name the price after it, where that price prints
  // none ("Any two valid challenges explained @ 4 marks each 2 + 2 marks").
  const named = new Set<Piece>();
  const lendWords = (from: Piece, to: Piece | undefined) => {
    if (!to || to.demoted || to.line !== from.line || tidyCell(to.text) || !tidyCell(from.text)) return false;
    to.text = from.text;
    named.add(from);
    return true;
  };
  if (!repeat && sum() !== max) {
    // A price larger than the criterion frames the units it is one of.
    for (const piece of pieces) if (value(piece) > max) piece.demoted = true;
    // Allocation notes above the answer ("Q1 Parts (i),(iii) & (iv) @1m + 1m;
    // Part (ii) @ 2m" over "A = North American B = Eurasian").
    if (sum() !== max && answers.length) {
      const noteLines = new Set(live().map(piece => piece.line));
      if ([...noteLines].every(index => /@|\bparts?\b/i.test(lines[index]))) {
        for (const piece of live()) piece.demoted = true;
      }
    }
    // "Way explained · 6 marks" over "Two SRPs @ 3 marks each": a labelled
    // total over its own breakdown.
    if (sum() !== max) {
      const kept = live();
      const total = kept.find((piece, index) => value(piece) === max
        && kept.slice(index + 1).reduce((acc, other) => acc + value(other), 0) === max);
      if (total) {
        total.demoted = true;
        const next = kept[kept.indexOf(total) + 1];
        if (next && !tidyCell(next.text)) { next.text = total.text; named.add(total); }
      }
    }
    // One unit of several, with no other price: "Two definitions @ 2 marks
    // each", "Showing and naming two physical features · 2 x (2 marks graded +
    // 2 marks)", "Three statements @ 4m + 3m + 3m" (the first statement's 4m).
    if (!live().length && !answers.length) {
      const unit = pieces.find(piece => ((piece.price.kind === 'each' || piece.price.kind === 'times') && piece.price.unit === max)
        || (piece.price.kind === 'row' && !piece.price.alternatives && /\+/.test(piece.raw)
          && (piece.raw.match(/\d+(?=\s*(?:marks?|m)?\s*(?:\+|$|\s))/g) ?? []).map(Number).includes(max)));
      if (unit) {
        unit.demoted = false;
        unit.price = unit.price.kind === 'times'
          ? { kind: 'row', marks: max, steps: unit.price.steps.length > 1 ? unit.price.steps : undefined }
          : { kind: 'row', marks: max };
      }
    }
    // "7/6 marks graded": take the alternative the criterion's total needs.
    if (sum() !== max) {
      const alternative = live().find(piece => piece.price.kind === 'row' && piece.price.alternatives);
      if (alternative && alternative.price.kind === 'row') {
        const others = sum() - alternative.price.marks;
        const pick = alternative.price.alternatives!.find(marks => others + marks === max);
        if (pick !== undefined) alternative.price = { kind: 'row', marks: pick, steps: upTo(pick) };
      }
    }
  }
  for (const entry of entries) {
    // A line whose every price frames the units ("Five terms @ 2 marks each as
    // follows:") is a heading as printed.
    if (entry.pieces.length && entry.pieces.every(piece => piece.demoted && !named.has(piece))) {
      heading(entry.at, entry.clean);
      continue;
    }
    entry.pieces.forEach((piece, index) => {
      if (!piece.demoted || named.has(piece)) return;
      if (lendWords(piece, entry.pieces[index + 1])) {
        heading(piece.line, tidyCell(piece.raw.slice(piece.text.length)));
        return;
      }
      heading(piece.line, tidyCell(piece.raw));
    });
  }

  const groups: GeographyAllocationGroup[] = [];
  const current = () => {
    if (!groups.length) groups.push({ rows: [], srp: [] });
    return groups[groups.length - 1];
  };
  let rowCount = 0; let srpCount = 0;
  let pooled = false;
  const pending: Array<{ at: number; text: string }> = [];
  const takePending = () => pending.pop()?.text;
  /** Plain lines after a price: the answers a tariff row stands over. */
  const after: Array<{ at: number; text: string }> = [];
  const rowLine = new Map<GeographyAnswerRow, number>();
  let awaiting: GeographyAnswerRow | undefined;
  const multiPart = parts.size > 1;
  for (const entry of entries) {
    if (entry.part) {
      const prompt = multiPart ? parts.get(entry.part.replace(/[()]/g, '')) : undefined;
      if (groups.length && (current().rows.length || current().srp.length || current().part)) {
        groups.push({ part: `(${entry.part})`, prompt, rows: [], srp: [] });
      } else {
        current().part = `(${entry.part})`;
        if (prompt) current().prompt = prompt;
      }
    }
    if (!entry.pieces.length) {
      if (!entry.text) continue;
      if (awaiting) { awaiting.text = entry.text; if (!isTariff(entry.text)) delete awaiting.tariffOnly; awaiting = undefined; continue; }
      const next = entries[entries.indexOf(entry) + 1];
      const labelsNext = next && next.pieces.length && !next.part;
      if (HEADING_PHRASE.test(entry.text) && !rowCount && !srpCount) heading(entry.at, entry.text);
      else if ((rowCount || srpCount) && !labelsNext) after.push({ at: entry.at, text: entry.text });
      else pending.push({ at: entry.at, text: entry.text });
      continue;
    }
    for (const piece of entry.pieces) {
      if (piece.demoted) continue;
      let text = tidyCell(piece.text);
      // A label line over a price that prints its own words ("Diagram (s)" over
      // "Two aspects @ 2 marks each 4 marks") heads the rows from there on.
      if (text && pending.length) {
        const label = pending.splice(0).map(line => line.text).join(CELL);
        const group = current();
        if (group.rows.length || group.srp.length) groups.push({ prompt: label, rows: [], srp: [] });
        else group.prompt = group.prompt ? `${group.prompt}${CELL}${label}` : label;
      }
      // "Relief (upland/lowland): · Named" — a labelled cell heads the row after it.
      const cells = text.split(CELL);
      const headIndex = cells.findIndex((cell, index) => index < cells.length - 1 && /:\s*$/.test(cell));
      if (headIndex >= 0) {
        heading(piece.line, tidyCell(cells.slice(0, headIndex + 1).join(CELL)));
        text = tidyCell(cells.slice(headIndex + 1).join(CELL));
      }
      // A part label inside the words means two columns of a table were read
      // across ("C Q.3 (ii) (River)"): the words no longer belong together.
      if (/\S\s+(?:Q\.?\s*\d+\s*)?\((?:i|ii|iii|iv|v|vi|vii|viii|ix|x)\)(?:\s|$)/i.test(text)) {
        return { error: `two columns read across: ${piece.raw}` };
      }
      const price = piece.price;
      if (price.kind === 'srp') {
        srpCount += 1;
        const srp: GeographySrpAllocation = {
          id: `s${srpCount}`,
          label: text || takePending() || '',
          count: price.count,
          marks: price.marks || srpMarks,
        };
        // A total may cover several units: "For each pattern: … 2 SRPs @ 3m each · 6m + 6m + 6m".
        const unitTotal = srp.count * srp.marks;
        if (price.total !== undefined && price.total !== unitTotal && !(unitNoun && price.total % unitTotal === 0)) {
          return { error: `SRP line does not multiply out: ${piece.raw}` };
        }
        if (price.min !== undefined) { srp.min = price.min; pooled = true; }
        current().srp.push(srp);
        continue;
      }
      let marks: number; let steps: number[] | undefined;
      if (price.kind === 'times') {
        marks = price.count * price.unit;
        steps = reachable(Array.from({ length: price.count }, () => price.steps));
      } else if (price.kind === 'each') {
        const count = price.count ?? countOf(text) ?? 1;
        marks = price.total ?? count * price.unit;
        if (marks % price.unit !== 0) return { error: `count line does not multiply out: ${piece.raw}` };
        const units = marks / price.unit;
        // A ladder printed with the words: "6 items illustrated (graded 2/1/0)".
        const inText = text.match(/\(graded(?:\s*(\d+(?:\/\d+)+))?\)/i);
        const ladder = price.graded ?? (inText ? (inText[1] ? ladderOf(inText[1]) : 'any' as const) : undefined);
        // "Explanation 7 @ 3 marks each 21 marks" on an SRP criterion counts SRPs.
        if (criterion.guidanceKind === 'srp' && !ladder && units > 2) {
          srpCount += 1;
          current().srp.push({ id: `s${srpCount}`, label: text.replace(/\s+\d+$/, '') || takePending() || '', count: units, marks: price.unit });
          continue;
        }
        steps = ladder === 'any' ? upTo(marks)
          : ladder ? reachable(Array.from({ length: units }, () => ladder.filter(step => step <= price.unit)))
            : Array.from({ length: units }, (_, index) => price.unit * (index + 1));
      } else {
        marks = price.marks;
        steps = price.steps;
      }
      rowCount += 1;
      const row: GeographyAnswerRow = { id: `r${rowCount}`, text: text || takePending() || '', marks };
      rowLine.set(row, piece.line);
      if (steps && steps.length > 1) row.steps = steps;
      if (!row.text) {
        // The price stands before its answer, on a line of its own ("2m" / "A").
        awaiting = row;
        row.tariffOnly = true;
      } else if (isTariff(row.text)) {
        row.tariffOnly = true;
      }
      current().rows.push(row);
    }
  }
  if (awaiting) {
    // No answer line followed: a second price for the slot above it, or for
    // the previous criterion's slot.
    const group = current();
    const previous = group.rows[group.rows.indexOf(awaiting) - 1]?.text ?? context.previousRowText;
    if (!previous) return { error: 'a price with nothing before it' };
    awaiting.text = previous;
    if (isTariff(previous)) awaiting.tariffOnly = true; else delete awaiting.tariffOnly;
  }

  // Lines that carry no price at all are the answer, priced by the heading
  // the scheme printed over them ("Five terms @ 2 marks each as follows:" /
  // "Crater") and so at the reviewed criterion's value: one row, as printed.
  if (!rowCount && !srpCount) {
    if (!pending.length) return { error: 'no priced line' };
    // Rejoin a printed answer the page wrapped ("Calm dry weather with warm" /
    // "temperature", "250,000/300,000-" / "320,000 Euro", "Plantation / Natural
    // Woodland /"); keep separate lines apart.
    const chunks: string[] = [];
    for (const { text: line } of pending.splice(0)) {
      const previous = chunks[chunks.length - 1];
      const wraps = previous !== undefined && (/[/,-]$|\b(?:or|and|with)$/i.test(previous)
        || /^(?:[a-z]|e\.g\.)/.test(line) || (previous.includes('/') && line.includes('/')));
      if (wraps) chunks[chunks.length - 1] = `${previous} ${line}`;
      else chunks.push(line);
    }
    const cellCount = (chunk: string) => chunk.split(CELL).length;
    let answer: string[] = chunks;
    if (chunks.length > 1 && cellCount(chunks[0]) > 1 && cellCount(chunks[1]) === cellCount(chunks[0])) {
      // A small table: header rows ("Example · Location") over the answer row.
      const width = cellCount(chunks[0]);
      let last = 0;
      while (last + 1 < chunks.length && cellCount(chunks[last + 1]) === width) last += 1;
      chunks.slice(0, last).forEach(chunk => heading(-1, chunk));
      answer = [chunks.slice(last).join(' ')];
    } else if (chunks.length > 1) {
      // A note printed under the answer ("Matching issues to photograph as above").
      for (const chunk of chunks.slice(1)) if (/\bas above\b|^(?:matching|note)\b/i.test(chunk)) directions.push(chunk);
      answer = chunks.filter((chunk, index) => index === 0 || !directions.includes(chunk));
    }
    const text = tidyCell(answer.join(CELL));
    const steps = criterion.permittedMarks.filter(mark => mark > 0);
    if (criterion.guidanceKind === 'srp') {
      const step = steps[0];
      if (!step || max % step !== 0 || steps.some((mark, index) => mark !== step * (index + 1))) {
        return { error: 'an SRP criterion with no SRP line' };
      }
      current().srp.push({ id: 's1', label: text, count: max / step, marks: step });
    } else {
      // A completed passage prints its answer in capitals ("The sedimentary
      // rock in the photograph is called LIMESTONE. It is weathered by the"):
      // the answer is that word.
      // Two answers on one printed line belong to two criteria in order: the
      // one after the previous criterion's answer.
      const capitals: string[] = text.match(/\b[A-Z]{4,}\b/g) ?? [];
      const next = context.previousRowText ? capitals.indexOf(context.previousRowText) + 1 : 0;
      const cloze = capitals.length > 0 && next < capitals.length && /\b[a-z]{3,}\b.*\b[a-z]{3,}\b/.test(text);
      const row: GeographyAnswerRow = { id: 'r1', text: cloze ? capitals[next] : text, marks: max };
      if (steps.length > 1) row.steps = steps;
      if (!cloze && isTariff(text)) row.tariffOnly = true;
      current().rows.push(row);
    }
  }
  // "(iii) · 2 named features @ 2 marks each · 4 marks" over "Cavern/Passage/
  // Stalactite/…": the plain lines under a tariff row are its printed answers.
  // A plain line under SRPs qualifies them ("Reason stated for one SRP").
  if (after.length && groups.some(group => group.srp.length)) directions.push(...after.splice(0).map(line => line.text));
  if (after.length) {
    const rows = groups.flatMap(group => group.rows);
    const only = rows.length === 1 && !groups.some(group => group.srp.length) ? rows[0] : undefined;
    if (!only) return { error: `text after the last price: ${after[0]}` };
    const answers = after.map(line => line.text);
    if (only.tariffOnly) {
      heading(rowLine.get(only) ?? after[0].at - 0.5, only.text);
      only.text = tidyCell(answers.join(' '));
      if (!isTariff(only.text)) delete only.tariffOnly;
    } else {
      // The answer runs on under its price ("X – Mid Atlantic Ridge or" /
      // "Constructive/divergent"), or the scheme prints a second accepted form
      // under it ("Cuan an Daingin/Dingle Harbour" / "An Chois"): the printed
      // pieces, divided like cells.
      only.text = [only.text, ...answers].join(CELL);
    }
  }
  // A label left over names the part ("Two actions" over "Action 1").
  for (const line of pending) heading(line.at, line.text);

  let srpPool: GeographyAllocation['srpPool'];
  if (pooled) {
    const fixed = groups.reduce((total, group) => total
      + group.rows.reduce((acc, row) => acc + row.marks, 0)
      + group.srp.reduce((acc, srp) => acc + (srp.min === undefined ? srp.count * srp.marks : 0), 0), 0);
    const pool = groups.flatMap(group => group.srp).filter(srp => srp.min !== undefined);
    const left = max - fixed;
    const each = pool[0].marks;
    if (left <= 0 || left % each !== 0) return { error: `SRP pool does not divide the remaining ${left} marks` };
    const count = left / each;
    const low = pool.reduce((total, srp) => total + (srp.min ?? 0), 0);
    const high = pool.reduce((total, srp) => total + srp.count, 0);
    if (count < low || count > high) return { error: `SRP pool of ${count} outside ${low}–${high}` };
    if (pool.length === 1) {
      // One part priced as a range ("Issue examined 7/6 x SRPs"): the
      // criterion's maximum says which end applies.
      delete pool[0].min;
      pool[0].count = count;
    } else {
      srpPool = { count, marks: each };
    }
  }
  if (repeat) {
    if (groups.length !== 1) return { error: 'a repeated unit over several parts' };
    const noun = unitNoun ?? tidyCell(head.text).split(/\s+/).filter(word => /^[a-z]+$/i.test(word)).pop() ?? '';
    groups[0].repeat = { count: repeat.count, unit: noun, marks: repeat.marks };
  }
  const allocation: GeographyAllocation = { groups, directions };
  if (srpPool) allocation.srpPool = srpPool;
  const printed = [...headings].sort((x, y) => x.at - y.at).map(line => line.text);
  return { allocation, headings: [...new Set(printed)] };
}

/** Headings sit over the first group, each printed piece divided like a cell. */
const withHeadings = ({ allocation, headings }: UnitResult): GeographyAllocation => {
  if (headings.length && allocation.groups.length) {
    const first = allocation.groups[0];
    first.prompt = [...headings, ...(first.prompt ? [first.prompt] : [])].join(CELL);
  }
  return allocation;
};

/** A card's column headings ("Bar Chart · Pie Chart"): a line of plain cells
 *  over a line that prints one price per cell, in any of its criteria. */
export function geographyColumnLabels(criteria: readonly GeographyCriterionSource[]): string[] | undefined {
  for (const criterion of criteria) {
    const lines = criterion.guidance;
    for (let index = 0; index < lines.length - 1; index += 1) {
      const cells = lines[index].split(CELL);
      if (cells.length < 2 || cells.some(cell => /\d/.test(cell))) continue;
      const next = joinPriceCells(lines[index + 1]).split(CELL).filter(cell => PRICE_CELL.test(guardFigures(cell, criterion.maxMarks)));
      if (next.length === cells.length) return cells.map(cell => tidyCell(cell));
    }
  }
  return undefined;
}

/**
 * Cut one reviewed criterion into rows, or say why not. A criterion is
 * structured only when its rows reach `maxMarks` and claim exactly the marks
 * the ledger permits.
 */
export function tryParseGeographyCriterionAllocation(context: GeographyCriterionContext,
  criterion: GeographyCriterionSource): GeographyAllocationResult {
  const lines = criterion.guidance.map(line => line.replace(/[’‘]/g, "'").replace(/\s+/g, ' ').trim()).filter(Boolean);
  const finish = (allocation: GeographyAllocation): GeographyAllocationResult => {
    const problem = reconcileCriterion(allocation, criterion);
    return problem ? { ok: false, reason: problem } : { ok: true, allocation };
  };

  // A band table: "Excellent · 20 · <descriptor>" down to "Poor · 0 · …".
  const bands = lines.map(line => line.match(BAND_LINE)).filter((match): match is RegExpMatchArray => !!match);
  if (bands.length >= 3) {
    const others = lines.filter(line => !BAND_LINE.test(line));
    return finish({
      groups: [],
      directions: [],
      choice: {
        kind: 'band',
        prompt: others.length ? tidyCell(others[0].split(CELL)[0]) : '',
        options: bands.map((band, index) => ({ id: `b${index + 1}`, label: band[1], marks: Number(band[2]), note: band[3].trim() })),
      },
    });
  }

  // "(ii) · ($) 400 billion · 4 marks or" over "($) 400 · 2 marks": the scheme
  // accepts one answer or the other, each at its own price.
  const orAt = lines.findIndex(line => /(?:marks?|m)\s+or$/i.test(line));
  if (orAt >= 0 && orAt + 1 < lines.length) {
    const options: GeographyChoiceOption[] = [];
    for (const [index, line] of [lines.slice(0, orAt + 1), lines.slice(orAt + 1)].map(chunk => chunk.join(' ').replace(/\s+or$/i, '')).entries()) {
      const unit = parseCriterionUnit([line], { ...criterion, maxMarks: Math.max(...criterion.permittedMarks) }, context);
      if ('error' in unit) return { ok: false, reason: unit.error };
      const rows = unit.allocation.groups.flatMap(group => group.rows);
      if (rows.length !== 1 || unit.allocation.groups.some(group => group.srp.length)) return { ok: false, reason: 'an alternative with more than one row' };
      options.push({ id: `a${index + 1}`, label: rows[0].text, marks: rows[0].marks });
    }
    return finish({ groups: [], directions: [], choice: { kind: 'alternative', prompt: '', options } });
  }

  // A two-route table: some line prints one price per column ("Identifying
  // aspect · 4 marks · 3 marks"). Each column is read on its own; columns that
  // price identically are one allocation, columns that differ are a choice.
  const isPrice = (cell: string) => PRICE_CELL.test(guardFigures(cell, criterion.maxMarks));
  const cellsOf = (line: string) => joinPriceCells(line).split(CELL).filter(cell => !/^or$/i.test(cell));
  const priceCells = (line: string) => cellsOf(line).filter(isPrice);
  const widths = new Set(lines.map(line => priceCells(line).length).filter(count => count >= 2));
  if (widths.size > 1) return { ok: false, reason: 'columns of different widths' };
  if (widths.size === 1) {
    const width = [...widths][0];
    const header = lines.find(line => priceCells(line).length === width) ?? '';
    const headerCells = cellsOf(header);
    const plainHeader = lines.find(line => line.split(CELL).length === width && !/\d/.test(line));
    const borrowed = !plainHeader && context.columnLabels?.length === width;
    const labels = plainHeader ? plainHeader.split(CELL).map(cell => tidyCell(cell))
      : borrowed ? [...context.columnLabels!]
        : headerCells.filter(isPrice).map(cell => tidyCell(cell));
    const prompt = plainHeader || borrowed ? '' : tidyCell(headerCells.filter(cell => !isPrice(cell)).join(CELL));
    const columns: GeographyAllocation[] = [];
    for (let column = 0; column < width; column += 1) {
      const columnLines = (shared: boolean) => lines.filter(line => line !== plainHeader).flatMap(line => {
        const cells = cellsOf(line);
        if (priceCells(line).length !== width) {
          // A priced line with one price belongs to the first column only when
          // the other column does not print it ("Horizontal axis named · 1 mark"
          // has no pie-chart counterpart).
          return shared || !priceCells(line).length ? [line] : [];
        }
        const price = cells.filter(isPrice)[column];
        // "1+1 mark (Circle & Centred)": the column names its own slot.
        const own = price.match(/^(.*?)\s*\(([^)]*[A-Za-z][^)]*)\)\s*$/);
        if (own) return [[own[2], own[1]].join(CELL)];
        return [[...cells.filter(cell => !isPrice(cell)), price].join(CELL)];
      });
      let result = parseCriterionUnit(columnLines(true), criterion, context);
      if (column > 0 && ('error' in result || geographyAllocationMax(result.allocation) !== criterion.maxMarks)) {
        const alone = parseCriterionUnit(columnLines(false), criterion, context);
        if (!('error' in alone) && geographyAllocationMax(alone.allocation) === criterion.maxMarks) result = alone;
      }
      if ('error' in result) return { ok: false, reason: `column ${column + 1}: ${result.error}` };
      columns.push(withHeadings(result));
    }
    if (columns.every(column => JSON.stringify(column) === JSON.stringify(columns[0]))) {
      if (plainHeader && columns[0].groups.length) {
        const first = columns[0].groups[0];
        first.prompt = first.prompt ? `${plainHeader}${CELL}${first.prompt}` : plainHeader;
      }
      return finish(columns[0]);
    }
    return finish({
      groups: [],
      directions: [],
      choice: {
        kind: 'route',
        prompt,
        options: columns.map((allocation, index) => {
          // The column's heading is the option's label, not a row heading.
          for (const group of allocation.groups) if (group.repeat) delete group.prompt;
          return { id: `o${index + 1}`, label: labels[index] ?? '', allocation };
        }),
      },
    });
  }

  const result = parseCriterionUnit(lines, criterion, context);
  if ('error' in result) return { ok: false, reason: result.error };
  return finish(withHeadings(result));
}

export const parseGeographyCriterionAllocation = (context: GeographyCriterionContext,
  criterion: GeographyCriterionSource): GeographyAllocation | undefined => {
  const result = tryParseGeographyCriterionAllocation(context, criterion);
  return result.ok ? result.allocation : undefined;
};
