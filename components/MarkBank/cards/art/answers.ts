/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Art components as rows the student places marks on.
 *
 * A 2010–2022 Art card's component ("Part B · 15") carries the scheme's own
 * table: one to three printed rows ("Name, description and discussion of
 * one other work by Michelangelo"), the Marks cell beside each row and,
 * where the scheme prints one, a Notes cell ("5 for name, 10 for
 * description & discussion."). Until October 2026 the reveal printed that
 * table as grey text over one slider for the whole component, so the
 * student could not see what the 15 marks were for, let alone take them
 * one by one. The rule since then: what the scheme prices is a row with
 * its marks on it.
 *
 * This module cuts each row into what the scheme prices: the row at its
 * printed marks and, where the Notes cell splits those marks, one part per
 * split. It adds no words: every part is the note's own phrase, a heading
 * the row prints, or the row's own words for a remainder the note leaves
 * unlabelled; the parts of a row add up to its marks and the rows to the
 * component. A note that prices nothing, or prices more than the row, stays
 * a note under the row. The shapes it reads:
 *   5 for name, 10 for description & discussion.      parts by "N for X"
 *   5 for names (3/2).                                  the same word priced twice
 *   5 for name                                          a part; the row's words take the other 10
 *   10/10/10 beside "… using headings: • subject matter • composition • style"
 *                                                       one part per printed heading
 *   6/6 6/7 beside "• subject matter and composition • colour and techniques"
 *                                                       a heading splits on "and"
 *   3/2 for name of the work, name of artist 10 for …  a split labelled by the phrase after it
 *   2 x 5 for functions                                 counted parts with their noun
 *   Location - 5 Function - 5 Structure - 15            parts by "Label – N"
 *   Max 3 for partially correct name.                   a note on the row
 */

import type { ArtAllocation, ArtAllocationPart, ArtAllocationRow, ArtCriterion } from '../../../../types/markBank';

export type ArtAnswerResult =
  | { ok: true; allocation: ArtAllocation }
  | { ok: false; reason: string };

/** "Max 3 for partially correct name", "3 max. for partially correct name": a rule, not a price. */
const MAX_RULE = /(?:\bmax\.?\s*\d+\s*for\b[^.;,]*|\b\d+\s*max\.?\s*for\b[^.;,]*)/gi;
/** A sentence the cell adds after its prices ("Features must be relevant to the question"): a note. */
const SENTENCE = /\s+(?=[A-Z][a-z]+\s+(?:must|should|may|are|is)\b)/;
/** "(3/2)" inside a part: the same word priced twice. */
const PAIR = /\(\s*(\d+)\s*\/\s*(\d+)\s*,?\s*\)/;
/** A bare split such as "10/10/10" or "6/6 6/7", outside parentheses. */
const SPLIT = /(?<![(\d/])\b(\d+(?:\/\d+)+(?:\s+\d+(?:\/\d+)+)*)\b(?![\d/]*\))/;
/** The phrase a bare split is printed with: "3/2 for name of the work, name of artist", "3/2 names". */
const PHRASE = /^\s*(?:for\s+)?([A-Za-z][^.\d]*?)(?=\s*\d+\s*for\b|\.|$)/;
/** "N for X" repeated with any separator or none: "5 for name 10 for discussion". */
const FOR = /(\d+)\s*for\s+(.+?)(?=(?:,|;|\.|\band\b|\/)?\s*\d+\s*for\s+|$)/g;
/** A phrase the Notes cell cut short ("3 for 1st named tomb an"): not a part. */
const DANGLING = /\b(?:a|an|and|the|of|for|or|with)$/i;
/** "2 x 5 for features" inside a longer cell. */
const COUNT = /(\d+)\s*[x×]\s*(\d+)\s*for\s+([A-Za-z][^,.;\d]*)/g;
/** "2 x 5 for functions", "4 points x 5 marks". */
const TIMES = /^(\d+)\s*(points?\s*)?[x×]\s*(\d+)(?:\s*marks?)?(?:\s*for\s+(.+))?$/i;
/** "Location - 5 Function -5 Structure - 15", "Interior – 15 Exterior – 15". */
const LABELLED = /([A-Za-z][^–\-\d]*?)\s*[–-]\s*(\d+)/g;
/** The headings a row prints after its bullets. */
const BULLET = /[•●]/;
/** The items a row lists without bullets: "referring to material, techniques and decoration", "relating to part B and part C". */
const LIST = /(?:referring to|relating to|(?:under|using) (?:the )?(?:following )?headings:?|using headings:?)\s*(.+)$/i;

const ORDINAL = ['1st', '2nd', '3rd', '4th', '5th'];
const tidy = (value: string) => value.replace(/\s+/g, ' ').replace(/^[\s,;./]+|[\s,;./]+$/g, '').trim();
const sum = (values: readonly { marks: number }[] | readonly number[]) =>
  (values as readonly (number | { marks: number })[]).reduce<number>((total, value) => total + (typeof value === 'number' ? value : value.marks), 0);

/** The candidate label lists a row prints: its bullets, those split on "and" ("6/6 6/7"), or a list after "referring to". */
function headings(row: string): string[][] {
  const bullets = row.split(BULLET).slice(1).map(tidy).filter(Boolean);
  if (bullets.length) {
    const split = bullets.flatMap(heading => heading.split(/\s+and\s+/).map(tidy).filter(Boolean));
    return split.length === bullets.length ? [bullets] : [bullets, split];
  }
  const list = LIST.exec(row);
  if (!list) return [];
  const items = list[1].split(/\s*,\s*|\s+and\s+/).map(tidy).filter(Boolean);
  return items.length > 1 ? [items] : [];
}

/** Labels for a split: the phrase printed with it ("for name of the work, name of artist"; "names") or the row's own headings. */
function labelsFor(values: number[], phrase: string | undefined, row: string): string[] | undefined {
  if (phrase) {
    const items = phrase.split(/\s*,\s*|\s+and\s+/).map(tidy).filter(Boolean);
    if (items.length === values.length) return items;
    if (items.length === 1) return values.map(() => items[0]);
    return undefined;
  }
  return headings(row).find(candidates => candidates.length === values.length);
}

interface Priced { text: string; marks: number; tag?: string }

/**
 * What a Notes cell prices, in print order, and what it says besides; undefined
 * when it prices nothing (a rule, a cap, a count without a noun).
 */
function pieces(note: string, row: string, marks: number): { parts: Priced[]; notes: string[] } | undefined {
  const notes = (note.match(MAX_RULE) ?? []).map(tidy).filter(Boolean);
  const [body, ...sentences] = note.replace(MAX_RULE, ' ').split(SENTENCE);
  notes.push(...sentences.map(tidy).filter(Boolean));
  let text = tidy(body);
  if (!text) return undefined;

  const times = TIMES.exec(text);
  if (times) {
    const [count, each] = [Number(times[1]), Number(times[3])];
    const noun = tidy(times[4] ?? times[2] ?? '');
    if (count * each !== marks || !noun) return undefined;
    return { parts: Array.from({ length: count }, (_, index) => ({ text: noun, marks: each, tag: `${index + 1} of ${count}` })), notes };
  }

  // A bare split and the phrase it is printed with come out before the "N for X" scan.
  let split: { values: number[]; phrase?: string; printed: string; first: boolean } | undefined;
  const bare = SPLIT.exec(text);
  if (bare) {
    const after = text.slice(bare.index + bare[0].length);
    const phrase = PHRASE.exec(after);
    split = {
      values: bare[1].split(/[\s/]+/).map(Number),
      phrase: phrase?.[1] ? tidy(phrase[1]) : undefined,
      printed: tidy(bare[0] + (phrase?.[0] ?? '')),
      first: bare.index === 0,
    };
    text = tidy(`${text.slice(0, bare.index)} ${after.slice(phrase?.[0].length ?? 0)}`);
  }

  const parts: Priced[] = [];
  // "5 for name 2 x 5 for features": a count inside a longer cell comes out first, in place.
  const counted: { at: number; parts: Priced[] }[] = [];
  text = text.replace(COUNT, (whole, count: string, each: string, noun: string, at: number) => {
    const word = tidy(noun);
    counted.push({ at, parts: Array.from({ length: Number(count) }, (_, index) => ({ text: word, marks: Number(each), tag: `${index + 1} of ${count}` })) });
    return ' ';
  });
  for (const match of text.matchAll(FOR)) {
    const price = Number(match[1]);
    const words = tidy(match[2]);
    // "5 for each" prices nothing the row names; "3 for 1st named tomb an" is a cell cut short.
    if (/^each$/i.test(words) || DANGLING.test(words)) return undefined;
    const pair = PAIR.exec(words);
    if (pair && Number(pair[1]) + Number(pair[2]) === price) {
      const word = tidy(words.replace(PAIR, ' '));
      parts.push({ text: word, marks: Number(pair[1]), tag: '1st' }, { text: word, marks: Number(pair[2]), tag: '2nd' });
    } else if (words) {
      parts.push({ text: words, marks: price });
    }
  }
  for (const { at, parts: countedParts } of counted.reverse()) {
    const before = [...text.slice(0, at).matchAll(FOR)].length;
    parts.splice(before, 0, ...countedParts);
  }
  if (!parts.length && !split) {
    const labelled = [...text.matchAll(LABELLED)].map(match => ({ text: tidy(match[1]), marks: Number(match[2]) })).filter(part => part.text);
    if (labelled.length && sum(labelled) <= marks) parts.push(...labelled);
  }
  if (sum(parts) > marks) return undefined;

  if (split) {
    const total = sum(split.values);
    const labels = labelsFor(split.values, split.phrase, row);
    const owner = parts.findIndex(part => part.marks === total);
    const splitParts = labels ? split.values.map((value, index) => ({ text: labels[index], marks: value })) : [];
    // "20 for description and discussion. 6/7/7": the split prices that part again, by heading.
    if (labels && sum(parts) === marks && owner >= 0) parts.splice(owner, 1, ...splitParts);
    else if (labels && sum(parts) + total === marks) parts[split.first ? 'unshift' : 'push'](...splitParts);
    else notes.unshift(split.printed);
  }
  if (!parts.length) return undefined;
  const remainder = marks - sum(parts);
  if (remainder > 0) {
    // "10 for description and discussion of each artefact" on a 25-mark row with "5 for name": each artefact is a part.
    const each = parts.find(part => /\beach\b/i.test(part.text) && remainder % part.marks === 0);
    if (each) parts.splice(parts.indexOf(each) + 1, 0, ...Array.from({ length: remainder / each.marks }, () => ({ ...each })));
    else parts.push({ text: row.replace(/\s+/g, ' ').trim(), marks: remainder });
  }
  return { parts, notes };
}

/** The printed rows of a 2010–2022 component, each cut into what its Notes cell prices. */
export function parseArtAllocation(criterion: Pick<ArtCriterion, 'guidance' | 'maxMarks' | 'permittedMarks' | 'rowMarks' | 'rowNotes'>): ArtAnswerResult {
  const { guidance, rowMarks, rowNotes, maxMarks, permittedMarks } = criterion;
  if (!rowMarks?.length) return { ok: false, reason: 'no marks column' };
  if (rowMarks.length !== guidance.length) return { ok: false, reason: 'marks column does not match the rows' };
  if (sum(rowMarks) !== maxMarks) return { ok: false, reason: 'rows do not add up to the component' };
  const every = Array.from({ length: maxMarks + 1 }, (_, mark) => mark);
  if (permittedMarks.length !== every.length || every.some(mark => !permittedMarks.includes(mark))) return { ok: false, reason: 'permitted marks are not every mark' };
  const rows: ArtAllocationRow[] = guidance.map((text, index) => {
    const marks = rowMarks[index];
    const note = tidy(rowNotes?.[index] ?? '');
    const row: ArtAllocationRow = { id: `r${index + 1}`, text: text.replace(/\s+/g, ' ').trim(), marks };
    const cut = note ? pieces(note, text, marks) : undefined;
    if (cut && cut.parts.length > 1 && sum(cut.parts) === marks) {
      row.parts = cut.parts.map((part, partIndex): ArtAllocationPart => ({ id: `p${partIndex + 1}`, ...part }));
      // "3/2 names": the same word priced twice is told apart by its order.
      for (const part of row.parts) {
        const twins = row.parts.filter(other => other.text === part.text && !other.tag);
        if (twins.length > 1) twins.forEach((twin, index) => { twin.tag = ORDINAL[index] ?? `${index + 1}th`; });
      }
      if (cut.notes.length) row.note = cut.notes.join('. ');
    } else if (note) {
      row.note = note;
    }
    return row;
  });
  return { ok: true, allocation: { rows } };
}
