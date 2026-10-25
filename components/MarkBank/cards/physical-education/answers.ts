/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Physical Education answers as bands and rows.
 *
 * A PE criterion carries its reviewed guidance as one or two sentences
 * ("Good description: 2; fair description: 1. Do NOT accept …") over its
 * permitted marks. Until October 2026 the reveal printed the sentence as
 * prose and offered bare number buttons, so a student had to read "Very
 * good: 5–6; good: 3–4; fair: 1–2" and then find the number. The rule since
 * then: what the scheme prices is a button with its words on it.
 *
 * This module cuts each criterion's guidance into bands (quality levels the
 * student places themselves on), rows (things they claim: an exact answer,
 * a named component, a counted allocation) and notes. It adds no words:
 * every label, row and note is a slice of the guidance. A criterion is
 * structured only when the marks its bands and rows can reach are exactly
 * its permitted marks; anything else keeps prose over the number buttons,
 * and test/markBankAnswerClarity.test.ts pins how many criteria that is.
 *
 * The shapes it reads:
 *   Very good: 5–6; good: 3–4; fair: 1–2.                     bands with ranges
 *   Good description: 2; fair description: 1.                  bands (max = criterion)
 *   Principle identified: 1; brief description: 1.             components (sum = criterion)
 *   Phase named: 1; contribution … explained: good 2, fair 1.  a component, then bands
 *   Published descending allocation: 4 marks + 2 marks         a counted row (steps 4, 6)
 *   3 × 2 marks. Load: javelin; effort: tricep; fulcrum: elbow. three named rows
 *   Vector. · Accurate explanation of adapted physical activity. one row at the maximum
 *   Use the published … descriptors: 10–12, 7–9, 4–6, 1–3; …  bands named by their ranges
 */

import type { PhysicalEducationAllocation, PhysicalEducationRubric, SecRubricCard } from '../../../../types/markBank';

type Criterion = PhysicalEducationRubric['criteria'][number];

export type PhysicalEducationAnswerResult =
  | { ok: true; allocation: PhysicalEducationAllocation }
  | { ok: false; reason: string };

/** The quality words that make an item a band rather than a component. */
const QUALITY = /^(?:very\s+good|good|fair|poor|excellent|weak)\b/i;
/** "label: 3–4" items separated by ";" and closed by "." */
const ITEM = /([^:;.]+?):\s*(\d+)(?:\s*[–-]\s*(\d+))?(?:\s*marks?)?/g;
const SUB_LADDER = /:\s*((?:(?:very\s+good|good|fair|poor|excellent)\s+\d+\s*,?\s*)+)\.?/i;
/** "4 marks + 2 marks", "4 + 3 + 3", "6 marks (3 + 3)": a descending allocation over counted answers. */
const COUNTED = /\(?((?:\d+\s*(?:marks?)?\s*\+\s*)+\d+(?:\s*marks?)?)\)?/i;
const GENERIC_HEAD = /^(?:published\s+descending\s+allocation|\d+\s*marks?|allocation)$/i;
const RANGES_FOR = /(\d+)\s*[–-]\s*(\d+)\s+for\s+([^;.]+)/g;
const TIMES = /(\d+)\s*[×x]\s*(\d+)\s*marks?\.?/i;
const RANGES_ONLY = /descriptors?:\s*((?:\d+\s*[–-]\s*\d+\s*,?\s*)+)(?:;\s*([^.]*?):\s*0)?\.?/i;
const KEYED = /([A-Za-z][^:;.]{0,40}):\s*([^;.]+)/g;

const range = (lo: number, hi: number) => Array.from({ length: Math.abs(hi - lo) + 1 }, (_, index) => Math.min(lo, hi) + index);
const cumulative = (terms: number[]) => terms.map((_, index) => terms.slice(0, index + 1).reduce((a, b) => a + b, 0));
const tidy = (value: string) => value.replace(/\s+/g, ' ').replace(/^[\s;,.]+|[\s;,]+$/g, '').trim();
const sameSet = (a: number[], b: readonly number[]) => {
  const x = [...new Set(a)].sort((p, q) => p - q);
  const y = [...new Set(b)].sort((p, q) => p - q);
  return x.length === y.length && x.every((value, index) => value === y[index]);
};

/** All marks a criterion can reach from its bands and rows, plus 0. */
function reachable(allocation: PhysicalEducationAllocation): number[] {
  let sums = new Set<number>([0]);
  for (const row of allocation.rows ?? []) {
    const values = row.steps ?? [row.marks];
    const next = new Set<number>(sums);
    for (const sum of sums) for (const value of values) next.add(sum + value);
    sums = next;
  }
  const bandMarks = (allocation.bands ?? []).flatMap(band => band.marks);
  if (bandMarks.length) {
    const next = new Set<number>(sums);
    for (const sum of sums) for (const mark of bandMarks) next.add(sum + mark);
    sums = next;
  }
  return [...sums];
}

/** Cut one criterion's guidance, or say why not. */
export function parsePhysicalEducationAnswers(criterion: Criterion): PhysicalEducationAnswerResult {
  const text = tidy(criterion.guidance.join(' '));
  if (!text) return { ok: false, reason: 'no guidance' };
  const notes: string[] = [];
  const allocation: PhysicalEducationAllocation = { notes };
  const finish = (): PhysicalEducationAnswerResult => {
    if (!allocation.bands?.length && !allocation.rows?.length) return { ok: false, reason: 'nothing priced' };
    const reach = reachable(allocation);
    if (Math.max(...reach) !== criterion.maxMarks) return { ok: false, reason: `reaches ${Math.max(...reach)}, criterion is ${criterion.maxMarks}` };
    if (!sameSet(reach, criterion.permittedMarks)) return { ok: false, reason: `reaches ${reach.sort((a, b) => a - b).join(',')}, permitted ${criterion.permittedMarks.join(',')}` };
    return { ok: true, allocation };
  };

  // "Use the published … descriptors: 10–12, 7–9, 4–6, 1–3; no relevant content: 0."
  const ranges = RANGES_ONLY.exec(text);
  if (ranges) {
    const bands = [...ranges[1].matchAll(/(\d+)\s*[–-]\s*(\d+)/g)].map(m => ({ label: `${m[1]}–${m[2]}`, marks: range(Number(m[1]), Number(m[2])) }));
    allocation.caption = tidy(text.slice(0, ranges.index + ranges[0].indexOf(':')));
    allocation.bands = bands;
    const rest = tidy(text.slice(ranges.index + ranges[0].length));
    if (rest) notes.push(rest);
    return finish();
  }

  // "3 × 2 marks. Load: javelin; effort: tricep; fulcrum: elbow."
  const times = TIMES.exec(text);
  if (times) {
    const count = Number(times[1]);
    const each = Number(times[2]);
    const after = text.slice(times.index + times[0].length);
    const keyed = [...after.matchAll(KEYED)].map(m => ({ text: tidy(`${m[1]}: ${m[2]}`) }));
    const head = tidy(text.slice(0, times.index));
    if (keyed.length === count) {
      allocation.rows = keyed.map((item, index) => ({ id: `r${index + 1}`, text: item.text, marks: each }));
      const consumed = keyed.reduce((end, item) => Math.max(end, after.indexOf(item.text.split(':')[0]) + item.text.length), 0);
      const rest = tidy(after.slice(consumed));
      if (head) allocation.caption = head;
      if (rest) notes.push(rest);
    } else {
      allocation.rows = [{ id: 'r1', text: head || criterion.label, marks: each * count, steps: cumulative(Array.from({ length: count }, () => each)) }];
      const rest = tidy(after);
      if (rest) notes.push(rest);
    }
    return finish();
  }

  // "4–6 for knowledge with some detail …; 1–3 for basic knowledge …; no relevant content: 0."
  const forRanges = [...text.matchAll(RANGES_FOR)];
  if (forRanges.length >= 2) {
    allocation.bands = forRanges.map(m => ({ label: tidy(m[3]), marks: range(Number(m[1]), Number(m[2])) }));
    const caption = tidy(text.slice(0, forRanges[0].index).replace(/[.:;]\s*$/, ''));
    if (caption) allocation.caption = caption;
    const last = forRanges[forRanges.length - 1];
    const rest = tidy(text.slice(last.index + last[0].length).replace(/^;?\s*no relevant content[^.]*\.?/i, ''));
    if (rest) notes.push(rest);
    return finish();
  }

  // "Published descending allocation: 4 marks + 2 marks" / "Two types of feedback: 1 + 1 marks. Examples include …"
  // / "Using evidence to draw a conclusion …: 6 marks (3 + 3)."
  const counted = COUNTED.exec(text);
  if (counted) {
    const terms = [...counted[1].matchAll(/\d+/g)].map(m => Number(m[0]));
    const sentences = text.split(/(?<=[.!?])\s+(?=[A-Z“(])/);
    const index = sentences.findIndex(sentence => sentence.includes(counted[0]));
    const sentence = sentences[index] ?? text;
    const at = sentence.indexOf(counted[0]);
    let head = tidy(sentence.slice(0, at).replace(/(?::|\s+\d+\s*marks?\s*)$/i, '').replace(/:\s*$/, ''));
    const tail = tidy(sentence.slice(at + counted[0].length).replace(/^[.)]/, ''));
    const others = sentences.filter((_, i) => i !== index).map(tidy).filter(Boolean);
    if (!head || GENERIC_HEAD.test(head)) {
      // "Relevant reasons suggested. Published descending allocation: 4 marks + 2 marks."
      const previous = index > 0 ? tidy(sentences[index - 1].replace(/\.$/, '')) : '';
      head = previous || criterion.label;
      allocation.rows = [{ id: 'r1', text: head, marks: terms.reduce((a, b) => a + b, 0), steps: cumulative(terms) }];
      notes.push(...others.filter(sentence => tidy(sentence.replace(/\.$/, '')) !== head));
    } else {
      allocation.rows = [{ id: 'r1', text: head, marks: terms.reduce((a, b) => a + b, 0), steps: cumulative(terms) }];
      notes.push(...others);
    }
    if (tail) notes.push(tail);
    return finish();
  }

  // Items "label: N" / "label: N–M" up to the first full stop after the last item.
  const items: { label: string; lo: number; hi: number; end: number; start: number }[] = [];
  ITEM.lastIndex = 0;
  for (const match of text.matchAll(ITEM)) {
    const label = tidy(match[1]);
    if (!label) continue;
    items.push({ label, lo: Number(match[2]), hi: Number(match[3] ?? match[2]), start: match.index, end: match.index + match[0].length });
  }
  // A trailing "good 2, fair 1" sub-ladder after the last colon.
  const sub = SUB_LADDER.exec(text);
  const subBands = sub ? [...sub[1].matchAll(/(very\s+good|good|fair|poor|excellent)\s+(\d+)/gi)].map(m => ({ label: m[1], marks: [Number(m[2])] })) : [];

  if (items.length || subBands.length) {
    const ladderItems = items.filter(item => !(sub && item.start >= sub.index));
    const componentLike = ladderItems.filter(item => item.lo === item.hi && !QUALITY.test(item.label));
    const first = ladderItems[0]?.start ?? sub!.index;
    const lastEnd = sub ? sub.index + sub[0].length : ladderItems[ladderItems.length - 1].end;
    const caption = tidy(text.slice(0, first).replace(/[.;:]\s*$/, ''));
    const rest = tidy(text.slice(lastEnd).replace(/^[.;]\s*/, ''));
    if (caption) allocation.caption = caption;
    if (rest) notes.push(rest);
    const bandsOf = (list: typeof ladderItems) => list.map(item => ({ label: item.label, marks: range(item.lo, item.hi) }));
    if (subBands.length) {
      // Components, then a quality ladder for the last one.
      const components = ladderItems;
      allocation.rows = components.map((item, index) => ({ id: `r${index + 1}`, text: item.label, marks: item.hi }));
      // The ladder's own heading ("contribution of the relevant energy systems explained") captions it.
      const subLabel = sub ? tidy(text.slice(components.length ? components[components.length - 1].end : 0, sub.index)) : '';
      if (subLabel && !allocation.caption) allocation.caption = subLabel;
      allocation.bands = subBands.map(band => ({ label: band.label, marks: band.marks }));
      return finish();
    }
    const sum = ladderItems.reduce((total, item) => total + item.hi, 0);
    const top = Math.max(...ladderItems.map(item => item.hi));
    const allQuality = ladderItems.every(item => QUALITY.test(item.label));
    if (ladderItems.length >= 2 && sum === criterion.maxMarks && !allQuality && (componentLike.length === ladderItems.length || top !== criterion.maxMarks)) {
      allocation.rows = ladderItems.map((item, index) => ({ id: `r${index + 1}`, text: item.label, marks: item.hi }));
      return finish();
    }
    if (top === criterion.maxMarks) {
      allocation.bands = bandsOf(ladderItems);
      return finish();
    }
    // Leading components plus a trailing ladder: "Phase named: 1; description: good 2…" handled above; here try one component + bands.
    if (ladderItems.length >= 3 && componentLike.length >= 1) {
      const head = ladderItems.slice(0, componentLike.length);
      const tail = ladderItems.slice(componentLike.length);
      if (head.reduce((t, item) => t + item.hi, 0) + Math.max(...tail.map(item => item.hi)) === criterion.maxMarks) {
        allocation.rows = head.map((item, index) => ({ id: `r${index + 1}`, text: item.label, marks: item.hi }));
        allocation.bands = bandsOf(tail);
        return finish();
      }
    }
    return { ok: false, reason: `items add to ${sum}, top ${top}, criterion ${criterion.maxMarks}` };
  }

  // One sentence and one price: the answer, or the criterion's own words, as a single row.
  if (sameSet([0, criterion.maxMarks], criterion.permittedMarks)) {
    const [sentence, ...others] = text.split(/(?<=[.!?])\s+(?=[A-Z“(])/);
    allocation.rows = [{ id: 'r1', text: tidy(sentence.replace(/\.$/, '')), marks: criterion.maxMarks }];
    if (others.length) notes.push(tidy(others.join(' ')));
    return finish();
  }
  return { ok: false, reason: 'prose over several permitted marks' };
}

export function withPhysicalEducationAnswers<T extends SecRubricCard & { rubric: PhysicalEducationRubric }>(card: T): T {
  return {
    ...card,
    rubric: {
      ...card.rubric,
      criteria: card.rubric.criteria.map(criterion => {
        const result = parsePhysicalEducationAnswers(criterion);
        return result.ok ? { ...criterion, allocation: result.allocation } : criterion;
      }),
    },
  };
}
