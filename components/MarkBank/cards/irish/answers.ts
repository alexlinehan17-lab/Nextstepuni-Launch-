/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Irish answer rows.
 *
 * An Irish listening or reading card carries its scheme as one to three
 * strings of exact guidance, lifted from the SEC marking scheme by
 * scripts/markbank/authoring/irish_cards.py and welded as the page prints
 * them: "1. Cad atá á lorg ag Ollscoil na hÉireann, Gaillimh? 2 mharc
 * Oifigeach Gaeilge = 2 mharc Oifigeach = 1 mharc 2. Cén dualgas…". Until
 * October 2026 the reveal printed that string as one bullet over a 0..total
 * scale. The rule since then: an answer the scheme prices is a claimable row
 * showing the answer and its marks; prose is only for the examiner's rules.
 *
 * This module cuts the welded text at its prices. It adds no words: a part's
 * prompt is the scheme's own sub-question, a row's text is the scheme's words
 * before "= 2 mharc", a direction is a scheme sentence. A card is structured
 * only when its parts' tariffs add up to the criterion and every part has
 * rows that fit its tariff; anything else keeps the prose fallback, and
 * test/markBankAnswerClarity.test.ts pins how many cards that is.
 *
 * The grammar, from the 2021–2025 schemes:
 *   FÓGRA A hAON (8 marc)                          a section header (dropped)
 *   1. Cad atá á lorg…? 2 mharc                     a sub-question and its tariff
 *   Cén ollscoil…? (Ollscoil) na hÉireann 3 mharc   Ordinary grid: the answer before the tariff
 *   Oifigeach Gaeilge = 2 mharc · Oifigeach = 1 mharc   answers, full and partial
 *   3. Scríobh síos dhá cháilíocht… 2 mharc + 2 mharc   two answers asked
 *   (Alt 1) {3 mharc} · {3 mharc: 2 mharc + 1 mharc}    reading tariffs; the second is
 *                                                   a ladder: first right 2, second 1
 *   3 mharc + 2 mharc = 5 mharc                    the Ordinary form of that ladder
 *   An chéad phointe eolais atá ceart = 2 mharc    a rule sentence, not an answer
 *    D’fhág an Ríocht Aontaithe…                  bullets: answers under a ladder
 *   Bainfear ó 0 go 3 ar chaighdeán na Gaeilge.    a rule sentence (direction)
 */

import type { IrishAllocation, IrishAnswerPart, IrishAnswerRow } from '../../../../types/markBank';

export interface IrishAnswerSource {
  id: string;
  totalMarks: number;
  questionRef: string;
  questionText: string;
  guidance: readonly string[];
}

export type IrishAnswerResult =
  | { ok: true; allocation: IrishAllocation }
  | { ok: false; reason: string };

const MARC = String.raw`(\d+)\s*m?h?arc\b`;
/** No `\b` after a word ending in a fada: JavaScript's \b is ASCII-only. */
const HEADER = /^(?:FÓGRA|PÍOSA|COMHRÁ)\s[^(]*\(\d+\s*m?h?arc\)\s*/i;
/** A price token, most specific first: "= 2 mharc (+ 2 mharc)", "{…}", "3 mharc + 2 mharc (= 5 mharc)", "2 mharc". */
const TOKEN = new RegExp(String.raw`=\s*${MARC}((?:\s*\+\s*\d+\s*m?h?arc\b)*)` +
  String.raw`|\{([^}]*)\}` +
  String.raw`|${MARC}\s*\+\s*${MARC}(?:\s*=\s*\d+\s*m?h?arc\b)?` +
  String.raw`|(?<![=+:{\d])\b${MARC}`, 'g');
/** "(dhá phointe eolais anseo = 2 mharc + 1 mharc = 3 mharc)" inside an answer. */
const NOTE = /\(([^()]*=\s*\d+\s*m?h?arc[^()]*)\)/g;
/** "An chéad phointe eolais atá ceart", "an dara húsáid atá ceart". */
const RULE = /^(?:an\s+)?(?:chéad|dara|tríú|ceathrú)\s.*\s(?:ceart|cheart)$/i;
const DIRECTION = /^(?:Bainfear\b|Glacfar\b|Ní mór\b|Gearrfar\b|Tabharfar\b|Tá .* mharc ag gabháil\b)/i;
/** Where the lifted excerpt runs on into the scheme's next section. */
const FURNITURE = /^(?:Eolas\s*\(|Iomlán|Móriomlán|Cuid [ABC]\b|I gcás\b|\d+ Roinn\b|An Tasc\b|An tÁbhar\b|Marcanna\b|An Mharcáil\b)/i;
const PROMPT = /^(?:An (?:Chéad|Dara|Tríú) Mhír\s*)?(?:\d+\.\s|\(?[a-z]\)\s|\((?:i|ii|iii|iv)\)\s)/i;
/** A sub-question starting inside a bullet's text: "… sa saol acadúil (b) (i) Cén toradh…?". */
const INNER_PROMPT = /\s(?=(?:(?:\([b-d]\)\s|\((?:i|ii|iii|iv)\)\s|(?:An (?:Dara|Tríú) Mhír\s*)?\d+\.\s(?:\(a\)\s)?[A-ZÁÉÍÓÚ])[^•]*(?:\?|\(Alt \d+\)|\.)|(?:Luaigh|Scríobh síos|Tabhair|Cén|Cad|Cá|Conas|Cathain|Cé)\s[^•]*\(Alt \d+\))\s*$)/;
const NEXT_QUESTION = /(?:^|\s)(\d+)\.\s+(?:\(a\)\s+)?[A-ZÁÉÍÓÚ]/g;
/** Where the lifted excerpt runs on into the scheme's next section, and the rule it ends with. */
const LEAK = /\s(?=(?:Eolas\s*\(\d+\)|Móriomlán|Iomlán\b|Freagair do rogha|I gcás A, B|\d+ Roinn ar an bpáipéar|An Mharcáil:|Cuid [ABC]\s*\(\d+|Léirigh na marcanna|Don Scrúdaitheoir|Na hIomláin|CEIST \d+ \(A \+ B\)|LÉAMHTHUISCINT - \d+ marc))/;
const LANGUAGE_RULE = /\bBainfear ó \d+ go \d+ ar chaighdeán na Gaeilge\.?/;
const BULLET = '';

const tidy = (value: string) => value.replace(/\s+/g, ' ').replace(/^[\s;,.•]+|[\s;,]+$/g, '').trim();
const cumulative = (terms: number[]) => terms.map((_, index) => terms.slice(0, index + 1).reduce((a, b) => a + b, 0));

interface Draft { prompt?: string; tariff: number; ladder?: number[]; rows: { text: string; marks?: number }[] }

/** Cut one criterion's exact guidance into parts and rows, or say why not. */
export function parseIrishAnswers(source: IrishAnswerSource): IrishAnswerResult {
  const directions: string[] = [];
  let text = source.guidance.join(' ').split(BULLET).join(' • ');
  text = text.replace(/\s+/g, ' ').trim().replace(HEADER, '');
  text = text.replace(NOTE, (_, note: string) => { directions.push(tidy(note)); return ' '; });
  text = text.replace(LANGUAGE_RULE, rule => { directions.push(tidy(rule)); return ' '; });
  const leak = LEAK.exec(text);
  if (leak) text = text.slice(0, leak.index);

  // A reading excerpt can run on into the next question: stop at its number.
  const own = /Ceist (\d+)/.exec(source.questionRef);
  if (own) {
    const ownNumber = Number(own[1]);
    for (const match of text.matchAll(NEXT_QUESTION)) {
      if (Number(match[1]) > ownNumber) { text = text.slice(0, match.index); break; }
    }
  }

  const parts: Draft[] = [];
  let current: Draft | undefined;
  const open = (prompt: string | undefined, tariff: number, ladder?: number[]) => {
    current = { prompt: prompt || undefined, tariff, ladder, rows: [] };
    parts.push(current);
  };
  /** Bullets before a token: answers for the open part, then the next
   *  sub-question's lead-in, which the scheme may run on from the last bullet. */
  const splitBullets = (segment: string): { lead: string; bullets: string[] } => {
    const [first, ...rest] = segment.split('•');
    const bullets = rest.map(tidy).filter(Boolean);
    let lead = tidy(first);
    if (bullets.length > 0) {
      const last = bullets[bullets.length - 1];
      const inner = INNER_PROMPT.exec(last);
      if (inner && !lead) {
        bullets[bullets.length - 1] = tidy(last.slice(0, inner.index));
        lead = tidy(last.slice(inner.index));
      }
    }
    return { lead, bullets: bullets.filter(Boolean) };
  };
  const addAnswers = (segment: string, marks: number | undefined): string | undefined => {
    const { lead, bullets } = splitBullets(segment);
    const items = lead ? [lead, ...bullets] : bullets;
    if (items.length === 0) return 'price without an answer';
    if (!current) return 'answer before any sub-question';
    let answers = 0;
    for (const [index, item] of items.entries()) {
      if (RULE.test(item)) { directions.push(item); continue; }
      if (DIRECTION.test(item)) { directions.push(item); continue; }
      answers += 1;
      // The bullets before the priced one are its alternatives at the same
      // price in a listening scheme, or the full answer at the sub-question's
      // tariff in a reading scheme whose partials are priced: the tariff covers both.
      const own = index === items.length - 1 ? marks : current.ladder ? undefined : current.tariff;
      current.rows.push({ text: item, marks: own });
    }
    return answers === 0 && items.every(item => !RULE.test(item) && !DIRECTION.test(item)) ? 'price without an answer' : undefined;
  };

  let pos = 0;
  let stopped = false;
  for (const match of text.matchAll(TOKEN)) {
    const segment = text.slice(pos, match.index);
    pos = match.index + match[0].length;
    const [, answer, plus, brace, sumA, sumB, bare] = match;
    if (answer !== undefined) {
      const marks = Number(answer) + [...(plus ?? '').matchAll(/\d+/g)].reduce((sum, m) => sum + Number(m[0]), 0);
      if (marks > source.totalMarks) { stopped = true; break; }
      // "= 2 mharc + 1 mharc = 3 mharc": the second price restates the first.
      if (!tidy(segment)) continue;
      // The bullets before the priced one are its alternatives at the same price.
      const problem = addAnswers(segment, marks);
      if (problem) return { ok: false, reason: problem };
      continue;
    }
    if (brace !== undefined) {
      const numbers = [...brace.matchAll(/\d+/g)].map(m => Number(m[0]));
      if (numbers.length === 0) return { ok: false, reason: 'empty brace tariff' };
      const { lead, bullets } = splitBullets(segment);
      if (bullets.length && current) bullets.forEach(bullet => { if (RULE.test(bullet)) directions.push(bullet); else current!.rows.push({ text: bullet }); });
      // "{3 mharc: 2 mharc + 1 mharc}" and "{2 mharc = 1 mharc + 1 mharc}": the
      // tariff, then how it splits; "{6 mharc + 6 mharc}": two answers.
      if (numbers.length > 2 && numbers.slice(1).reduce((a, b) => a + b, 0) === numbers[0]) open(lead, numbers[0], cumulative(numbers.slice(1)));
      else if (brace.includes('+')) open(lead, numbers.reduce((a, b) => a + b, 0), cumulative(numbers));
      else if (!lead && current && current.rows.length === 0 && current.tariff === numbers[0]) continue; // "{3 mharc: 2+1} {3 mharc}" repeats the tariff
      else open(lead, numbers[0]);
      continue;
    }
    if (sumA !== undefined) {
      const terms = [Number(sumA), Number(sumB)];
      const { lead, bullets } = splitBullets(segment.replace(/=\s*\d+\s+\S+\s*$/, ''));
      if (bullets.length && current) bullets.forEach(bullet => { if (RULE.test(bullet)) directions.push(bullet); else current!.rows.push({ text: bullet }); });
      // "… a cheannach = 2 úsáid = 3 mharc + 2 mharc = 5 mharc" inside a bullet
      // restates the open part's ladder.
      if (!lead && current?.ladder && current.ladder.join() === cumulative(terms).join()) continue;
      if (lead && !PROMPT.test(lead) && !/[?.]$/.test(lead) && current) {
        // "Gaeilge líofa = 2 mharc + 2 mharc" was consumed as an answer above; a bare
        // sum after an answer without a prompt is a repeated tariff line.
        directions.push(lead);
        continue;
      }
      open(lead, terms[0] + terms[1], terms[0] === terms[1] ? undefined : cumulative(terms));
      continue;
    }
    // A bare tariff: a sub-question's marks, or (Ordinary grids) an answer's.
    const tariff = Number(bare);
    const lead = tidy(segment);
    if (tariff > source.totalMarks || FURNITURE.test(lead)) { stopped = true; break; }
    if (DIRECTION.test(lead)) { directions.push(lead); continue; }
    const { lead: head, bullets } = splitBullets(segment);
    if (bullets.length && current) bullets.forEach(bullet => { if (RULE.test(bullet)) directions.push(bullet); else current!.rows.push({ text: bullet }); });
    if (/\?$/.test(head) || PROMPT.test(head)) { open(head, tariff); continue; }
    const question = head.lastIndexOf('?');
    if (question >= 0) {
      open(tidy(head.slice(0, question + 1)), tariff);
      current!.rows.push({ text: tidy(head.slice(question + 1)), marks: tariff });
      continue;
    }
    if (!current) return { ok: false, reason: 'tariff before any sub-question' };
    if (!head) continue;
    current.rows.push({ text: head, marks: tariff });
  }
  if (!stopped) {
    const tail = text.slice(pos);
    const { lead, bullets } = splitBullets(tail);
    for (const item of lead ? [lead, ...bullets] : bullets) {
      if (!current) break;
      if (FURNITURE.test(item)) break;
      if (RULE.test(item) || DIRECTION.test(item)) directions.push(item);
      else if (/^[A-ZÁÉÍÓÚ]/.test(item) && !/[=]/.test(item) && !current.ladder && current.rows.length > 0 && item.length > 60) directions.push(item);
      else current.rows.push({ text: item });
    }
  }

  if (parts.length === 0) return { ok: false, reason: 'no sub-questions' };
  const sum = parts.reduce((total, part) => total + part.tariff, 0);
  if (sum !== source.totalMarks) return { ok: false, reason: `tariffs add to ${sum}, criterion is ${source.totalMarks}` };

  const built: IrishAnswerPart[] = [];
  for (const [index, part] of parts.entries()) {
    if (part.rows.length === 0) return { ok: false, reason: `sub-question without answers: ${(part.prompt ?? '').slice(0, 40)}` };
    const unpriced = part.rows.filter(row => row.marks === undefined);
    if (part.ladder) {
      part.rows.forEach(row => { row.marks = row.marks ?? 0; });
    } else if (unpriced.length === part.rows.length) {
      part.rows.forEach(row => { row.marks = part.tariff; });
    } else if (unpriced.length > 0) {
      return { ok: false, reason: 'unpriced answers beside priced ones' };
    }
    const rows: IrishAnswerRow[] = part.rows.map((row, rowIndex) => ({ id: `r${rowIndex + 1}`, text: row.text, marks: row.marks ?? 0 }));
    const max = Math.max(0, ...rows.map(row => row.marks));
    if (part.ladder) {
      if (part.ladder[part.ladder.length - 1] !== part.tariff) return { ok: false, reason: 'ladder does not reach the tariff' };
      if (max > 0 && max > part.tariff) return { ok: false, reason: 'row above its tariff' };
    } else {
      if (max <= 0) return { ok: false, reason: 'sub-question without a priced answer' };
      if (max > part.tariff) return { ok: false, reason: 'row above its tariff' };
      if (part.tariff % max !== 0) return { ok: false, reason: `tariff ${part.tariff} is not a multiple of its full answer ${max}` };
    }
    built.push({ id: `p${index + 1}`, ...(part.prompt ? { prompt: part.prompt } : {}), tariff: part.tariff, ...(part.ladder ? { ladder: part.ladder } : {}), rows });
  }
  const seen = new Set<string>();
  return { ok: true, allocation: { parts: built, directions: directions.filter(note => note && !seen.has(note) && seen.add(note)) } };
}

export function irishAnswersFor(source: IrishAnswerSource): IrishAllocation | undefined {
  const result = parseIrishAnswers(source);
  return result.ok ? result.allocation : undefined;
}
