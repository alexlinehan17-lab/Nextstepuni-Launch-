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
  /** The whole card's marks, where a reviewed card prices one printed question across several criteria. */
  cardTotal?: number;
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
/** "An chéad phointe eolais atá ceart", "an dara húsáid atá ceart", and the first rule as 2017 Ordinary Reading B 3(b) prints
 *  it, "Fáth amháin atá ceart = 3 mharc; an dara fáth atá ceart = 2 mharc". */
const RULE = /^(?:(?:an\s+)?(?:chéad|dara|tríú|ceathrú)\s.*\s|[A-ZÁÉÍÓÚa-záéíóú]+ amháin atá\s)(?:ceart|cheart)$/i;
/** "Aon dá cheann de na rudaí ón liosta thíos = 3 mharc + 2 mharc", "2 cheann ón liosta = 3 mharc + 2 mharc" (2017 Ordinary
 *  Reading A 2(a), A 5(b), B 5(b)): how the list after it is priced, a rule, never an answer. */
const LIST_RULE = /^(?:Aon\s+)?(?:dá|dhá|\d+)\s+cheann\b[^•=]*\bliosta\b/i;
/** "Dhá phointe eolais as an liosta seo = 3 mharc + 2 mharc = 5 mharc", "Na pointí seo a leanas:" (2016 Ordinary): the scheme's
 *  heading over a list of accepted points, not one of them. So are "Dhá cheann as na critéir seo a leanas:", "Rud amháin as na
 *  rudaí seo a leanas:" and "An dá phointe eolais seo:" (2015 Higher A 3(a), A 3(b)(i), B 2(a)). */
const DIRECTION = /^(?:Bainfear\b|Glacfar\b|Ní mór\b|Gearrfar\b|Tabharfar\b|Tá .* mharc ag gabháil\b|Dhá (?:phointe|phíosa) eolais as an liosta seo\b|Na pointí seo a leanas\b|[^•=]{1,60}\bseo a leanas:$|An dá phointe eolais seo:$)/i;
/** Where the lifted excerpt runs on into the scheme's next section. */
const FURNITURE = /^(?:Eolas\s*\(|Iomlán|Móriomlán|Cuid [ABC]\b|I gcás\b|\d+ Roinn\b|An Tasc\b|An tÁbhar\b|Marcanna\b|An Mharcáil\b)/i;
const PROMPT = /^(?:An (?:Chéad|Dara|Tríú) Mhír\s*)?(?:\d+\.\s|\(?[a-z]\)\s|\((?:i|ii|iii|iv)\)\s)/i;
/** A sub-question starting inside a bullet's text: "… sa saol acadúil (b) (i) Cén toradh…?". */
const INNER_PROMPT = /\s(?=(?:(?:\([b-d]\)\s|\((?:i|ii|iii|iv)\)\s|(?:An (?:Dara|Tríú) Mhír\s*)?\d+\.\s(?:\(a\)\s)?[A-ZÁÉÍÓÚ])[^•]*(?:\?|\(Alt \d+\)|\.)|(?:Luaigh|Scríobh síos|Tabhair|Cén|Cad|Cá|Conas|Cathain|Cé)\s[^•]*\(Alt \d+\))\s*$)/;
/** A question number: one or two digits, so a year ending a sentence ("ar an 20 Iúil 1969. Tabhair …", 2019 Higher B 1(a)) is not one. */
const NEXT_QUESTION = /(?:^|\s)(\d{1,2})\.\s+(?:\(a\)\s+)?[A-ZÁÉÍÓÚ]/g;
/** Where the lifted excerpt runs on into the scheme's next section, and the rule it ends with. */
const LEAK = /\s(?=(?:Eolas\s*\(\d+\)|Móriomlán|Iomlán\b|Freagair do rogha|I gcás A, B|\d+ Roinn ar an bpáipéar|An Mharcáil:|Cuid [ABC]\s*\(\d+|Léirigh na marcanna|Don Scrúdaitheoir|Na hIomláin|CEIST \d+ \(A \+ B\)|LÉAMHTHUISCINT - \d+ marc))/;
/** The language deduction the scheme prints beside the answers: Higher as a sentence, Ordinary in square brackets. */
const LANGUAGE_RULE = /\bBainfear ó \d+ go \d+ ar chaighdeán na Gaeilge\.?|\[Gaeilge lochtach:[^\]]*\]/;
const BULLET = '';

const tidy = (value: string) => value.replace(/\s+/g, ' ').replace(/^[\s;,.•]+|[\s;,]+$/g, '').trim();
const cumulative = (terms: number[]) => terms.map((_, index) => terms.slice(0, index + 1).reduce((a, b) => a + b, 0));

interface Draft { prompt?: string; tariff: number; ladder?: number[]; rows: { text: string; marks?: number }[]; ruled?: number[] }

/** A reviewed card's criterion carries its own sub-question first, then lines that are not its answers:
 *  the scheme's "Nóta: …" for the part ("Má tá dhá phointe eolais i gceist, tá 3 mharc …"), which is an
 *  examiner direction, and the tariff summary for the whole section ("Freagair Léamhthuiscint A agus
 *  Léamhthuiscint B. Tá Ceist 1 – 5 ar cómharc, 7 marc …") or the card's note on an order-dependent
 *  award, which the part's own tariff and ladder already show. None of their prices is this part's. */
const PART_NOTE = /^Nóta:/;
const SECTION_SUMMARY = /^(?:Freagair Léamhthuiscint|Tá Ceist \d+\s*[–-]\s*\d+ ar cómharc|Order-dependent award)/;
/** "(Is leor aon trí cinn as na ceithre cinn: …)", "(Ní mór ‘…’ a bheith sa fhreagra chun an dara marc a
 *  ghnóthú)", "(Tá gá le ‘conradh’ … a lua sa fhreagra chun an dá mharc a bhronnadh.)", "(Má fhágtar ainmfhocal nó aidiacht
 *  amháin ar lár is fiú 3 mharc an freagra.)" (2017 Ordinary Reading A 3(b)), "(Tá an dá rud - … ag teastáil chun 5 mharc a bhronnadh
 *  ar an bhfreagra.)" (2016 Ordinary B 5(a)), "(Tá an dara habairt inghlactha mar phointe eolais má bhíonn an chéad phointe leis. …)"
 *  (2015 Higher B 2(a)) after an answer: how much of it suffices, what it must contain or what it is worth
 *  without a word, a direction. */
const SUFFICES = /\((?:Is leor|aon|Ní mór|Tá gá le|Má fhágtar|Tá an dá rud|Tá an dara habairt)\s[^()]*(?:\([^()]*\)[^()]*)*\)/g;
/** "… nó áitiúla = 1 mharc (gan ‘in 2024’ sa fhreagra)", "… = 2 mharc (Gan ainmneacha an dá thír luaite, …)": the qualifier is the condition of the answer it
 *  follows, as "= 0 marc (gá le cáiliú)" (2018 Higher B 1(b)(ii)) is. It stays on that row, as a second slice:
 *  "… nó áitiúla: (gan ‘in 2024’ sa fhreagra) · 1m". */
const QUALIFIED_PRICE = /\s*(=\s*\d+\s*m?h?arc\b)\s*(\((?:[Gg]an|gá le)\s[^()=]*\))/g;
/** "… in áit faoi leith (2 mharc) in imeacht tréimhse áirithe ama (1 mharc) = 3 mharc" (2020 Higher A 1(a)): one answer
 *  printing how its own price divides. Where the bracketed prices add up to the price after them they are part of the
 *  answer's text, not tariffs: a word joiner (U+2060) holds each one together until the rows are cut, then goes. */
const INLINE_SPLIT = /(?:[^•=()]*\(\d+\s*m?h?arc\)){2,}[^•=()]*(?==\s*(\d+)\s*m?h?arc\b)/g;
const HELD = '\u2060';
/** "{2 mharc} • D’ísligh sé an cíos (1 mharc) agus dháil sé bia … (1 mharc)" (2019 Higher A 2(b)(i)): the part's one answer
 *  printing how its price divides, with no price after it. Where the bracketed prices add up to the brace they are the
 *  answer's text, held as INLINE_SPLIT holds them, and the brace prices the answer. */
const BRACED_SPLIT = /(\{(\d+)\s*m?h?arc\}\s*•\s*)((?:[^•=(){}]*\(\d+\s*m?h?arc\)){2,}[^•=(){}]*?)\s*$/;

/** "Báisteach/fearthainn = 2 mharc (báisteach/fearthainn throm = 3 mharc)" (2019 Ordinary Fógra a Dó 2(a)): a bracketed answer
 *  at its own single price, printed straight after another answer's price, is one more answer, not a note. A bracketed
 *  direction or qualifier ("(Is leor …", "(Ní mór …", "(Gan …", "(Tá gá le …") is never an answer. */
const BRACKETED_ANSWER = /(=\s*\d+\s*m?h?arc\b)\s*\((?!\s*(?:Is leor|aon|Ní mór|[Gg]an|Tá gá le)\s)([^()=+:]+?)\s*(=\s*\d+\s*m?h?arc\b)\)/g;

/** Whether a line is the card's printed question, read past the paper's hyphens and spacing. */
const letters = (value: string) => value.toLowerCase().replace(/[^a-záéíóú]+/g, '');
const printedQuestion = (questionText: string, line: string) => letters(line).length > 12 && letters(questionText).includes(letters(line));

/** Cut one criterion's exact guidance into parts and rows, or say why not. */
export function parseIrishAnswers(source: IrishAnswerSource): IrishAnswerResult {
  const directions: string[] = [];
  const ownLines = source.guidance.filter((line, index) => {
    if (index === 0) return true;
    if (SECTION_SUMMARY.test(line.trim())) return false;
    if (!PART_NOTE.test(line.trim())) return true;
    directions.push(tidy(line));
    return false;
  });
  // A SymbolMT bullet the builders have not yet repaired (U+F0B7) and a repaired one (•) cut alike.
  let text = ownLines.join(' ').split(BULLET).join(' • ').replace(/•/g, ' • ');
  text = text.replace(QUALIFIED_PRICE, (_, price: string, qualifier: string) => `: ${qualifier} ${price}`);
  text = text.replace(INLINE_SPLIT, (answer: string, total: string) => {
    const split = [...answer.matchAll(/\((\d+)\s*m?h?arc\)/g)].reduce((sum, m) => sum + Number(m[1]), 0);
    return split === Number(total) ? answer.replace(/\((\d+)\s*(m?h?arc)\)/g, `($1${HELD}$2)`) : answer;
  });
  text = text.replace(BRACED_SPLIT, (whole: string, head: string, total: string, answer: string) => {
    const split = [...answer.matchAll(/\((\d+)\s*m?h?arc\)/g)].reduce((sum, m) => sum + Number(m[1]), 0);
    return split === Number(total) ? `${head}${answer.replace(/\((\d+)\s*(m?h?arc)\)/g, `($1${HELD}$2)`)} = ${total} mharc` : whole;
  });
  // A price printed inside the qualifier's brackets, "(gan aon cháiliú = 1 mharc)", reads as the qualified price above.
  text = text.replace(/\s*\((gan\s[^()=]*?)\s*(=\s*\d+\s*m?h?arc\b)\)/g, (_, qualifier: string, price: string) => `: (${qualifier}) ${price}`);
  // "(dhá cheann) {1 mharc + 1 mharc = 2 mharc}" (2017 Higher A 1(b)(i)): the brace prints its split before its total; it is
  // the brace "{2 mharc: 1 mharc + 1 mharc}" where the split adds up to the total.
  text = text.replace(/\{\s*(\d+\s*m?h?arc\b(?:\s*\+\s*\d+\s*m?h?arc\b)+)\s*=\s*(\d+)\s*(m?h?arc\b)\s*\}/g, (whole: string, split: string, total: string, unit: string) =>
    ([...split.matchAll(/\d+/g)].reduce((sum, m) => sum + Number(m[0]), 0) === Number(total) ? `{${total} ${unit}: ${split}}` : whole));
  // A split printed before the brace, "(Dhá bhealach: 2 mharc + 1 mharc) {3 mharc}", is the brace's own split.
  text = text.replace(/\((Dhá\s[^():]*):\s*(\d+\s*m?h?arc\b(?:\s*\+\s*\d+\s*m?h?arc\b)+)\)\s*\{\s*(\d+\s*m?h?arc\b)\s*\}/g,
    (_, label: string, split: string, total: string) => `(${label}) {${total}: ${split}}`);
  // "(2 mharc) (2 cheist dhomhanda) {1 mharc + 1 mharc}" and "{2 mharc} (2 phointe eolais) {1 mharc + 1 mharc}" (2015 Higher
  // A 1(b)(ii), A 5(b)(i)): the part's tariff, a note on what it asks for, then how the tariff splits. One brace with its split;
  // the note is a direction, so the prompt stays the printed line it ends ("… (Alt 1)").
  text = text.replace(/[({]\s*(\d+)\s*(m?h?arc\b)\s*[)}]\s*(\([^()]*\))\s*\{\s*(\d+\s*m?h?arc\b(?:\s*\+\s*\d+\s*m?h?arc\b)+)\s*\}/g,
    (whole: string, total: string, unit: string, note: string, split: string) => {
      if ([...split.matchAll(/\d+/g)].reduce((sum, m) => sum + Number(m[0]), 0) !== Number(total)) return whole;
      directions.push(tidy(note));
      return `{${total} ${unit}: ${split}}`;
    });
  // "(b) Cén dáta a bheidh an clár nua ag tosú? An dara lá déag de Bhealtaine = 2 mharc 2 mharc 12 Bealtaine = 2 mharc …" (2015
  // Higher Fógra a hAon 1(b)): the question's tariff, printed in the margin beside its first answer, is read after that answer.
  text = text.replace(/\?\s+([^•=?]{1,80}?=\s*\d+\s*m?h?arc\b)\s+(\d+\s*m?h?arc\b)(?!\s*[+=])/g, (_, answer: string, tariff: string) => `? ${tariff} ${answer}`);
  text = text.replace(BRACKETED_ANSWER, (_, price: string, answer: string, own: string) => `${price} ${answer.trim()} ${own}`);
  // A refused answer the scheme prints at a bare 0 ("Deireadh Fómhair = 0"; the grid's "T-léine 3 mharc Léine 0", 2016 Ordinary):
  // an answer at 0 marks, as "= 0 marc (gá le cáiliú)" is.
  text = text.replace(/=\s*0(?=\s*(?:•|$))/g, '= 0 marc').replace(/(\d\s*m?h?arc\s+[^•=?\d]{1,40}?)\s+0(?=\s*(?:•|$))/g, '$1 0 marc');
  // "3 mharc ar an gcéad chúis cheart + 2 mharc ar an dara cúis cheart = 5 mharc" (2016 Ordinary B 1(a)): the ladder said again
  // as a sentence, a direction. "X = 3 mharc nó 2 mharc" (A 3(b)): one point at 3 or 2 by its order, which the ladder carries.
  text = text.replace(/\b\d+\s*m?h?arc ar an gcéad [^+=•]+\+\s*\d+\s*m?h?arc ar an dara [^+=•]+=\s*\d+\s*m?h?arc\b/g, rule => { directions.push(tidy(rule)); return ' '; });
  text = text.replace(/(=\s*\d+\s*m?h?arc\b)\s+nó\s+\d+\s*m?h?arc\b/g, '$1');
  text = text.replace(SUFFICES, note => { directions.push(tidy(note)); return ' '; });
  text = text.replace(/\s+/g, ' ').trim().replace(HEADER, '');
  text = text.replace(NOTE, (_, note: string) => { directions.push(tidy(note)); return ' '; });
  text = text.replace(LANGUAGE_RULE, rule => { directions.push(tidy(rule)); return ' '; });
  const leak = LEAK.exec(text);
  if (leak) text = text.slice(0, leak.index);
  // "Tuairim (2) ► 2 mharc T = Cúis 1 (2 mharc) + Sampla 1 (3 mharc) ► 5 mharc …" (2015 Higher 6(b)) prices what the answer must
  // do, with the examiner's boxes between the prices: the tariff reader's grammar (tariffs.ts ARROW), never an answer list.
  if (text.includes('►')) return { ok: false, reason: 'arrow-priced tariff' };

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
    if (!current) {
      // "5. (a) Tabhair dhá phíosa eolais … (Alt 5) An chéad phointe eolais atá ceart = 3 mharc; an dara … = 2 mharc" (2016 Ordinary
      // A 5(a)): the question prints no tariff of its own, only the rules that price it. It opens at the criterion's marks, and
      // the rules ladder it as they do under a printed tariff.
      const ruled = /^(.*(?:\(Alt \d+\)|\?))\s+((?:an\s+)?(?:chéad|dara)\s.*\s(?:ceart|cheart))$/i.exec(items[0]);
      if (ruled && PROMPT.test(ruled[1]) && marks !== undefined) { open(tidy(ruled[1]), source.totalMarks); items[0] = ruled[2]; }
    }
    if (!current) return 'answer before any sub-question';
    let answers = 0;
    for (const [index, item] of items.entries()) {
      // "• Gearrann obair Foodcloud … = 2 mharc nó • Faigheann na bochtáin cabhair riachtanach = 2 mharc" (2015 Higher A 4(b)(ii)):
      // the word between two answers, not one.
      if (item === 'nó') continue;
      if (RULE.test(item)) {
        directions.push(item);
        // "5 mharc An chéad phíosa eolais atá ceart = 3 mharc; an dara píosa eolais atá ceart = 2 mharc" (2018 Ordinary
        // Reading B 1(b)): the rules price the part's ladder where no "3 mharc + 2 mharc = 5 mharc" does. Their prices
        // become the ladder once they add up to the part's tariff, so its answers are claimed in order, first 3 then 2.
        if (marks !== undefined && index === items.length - 1 && !current.ladder && current.rows.length === 0) {
          current.ruled = [...(current.ruled ?? []), marks];
          const ruled = current.ruled;
          if (ruled.length > 1 && ruled.reduce((a, b) => a + b, 0) === current.tariff) current.ladder = cumulative(ruled);
        }
        continue;
      }
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
      // "Aon dá cheann … ón liosta … = 3 mharc + 2 mharc": the list's rule, a direction; its price is the part's ladder where the
      // part has none yet and the price adds up to the part's tariff, and the listed answers after it are claimed by count.
      const listed = splitBullets(segment);
      if (current && plus && LIST_RULE.test(listed.lead) && listed.bullets.length === 0) {
        directions.push(listed.lead);
        const terms = [Number(answer), ...[...plus.matchAll(/\d+/g)].map(m => Number(m[0]))];
        if (!current.ladder && terms.reduce((a, b) => a + b, 0) === current.tariff) current.ladder = cumulative(terms);
        continue;
      }
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
      // "5 mharc 3 mharc + 2 mharc = 5 mharc" (2016 Ordinary B 4(a)): the open part's tariff, then how it divides: its ladder.
      // "2 mharc 1 mharc + 1 mharc" (2015 Higher Comhrá a Dó 2) divides it into equal halves, which the answers' own prices carry.
      if (!lead && current && !current.ladder && current.rows.length === 0 && terms[0] + terms[1] === current.tariff) {
        if (terms[0] !== terms[1]) current.ladder = cumulative(terms);
        continue;
      }
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
    const question = head.lastIndexOf('?');
    // "1. (a) Cén t-ainm atá ar an stáisiún raidió atá luaite san fhógra? Raidió Fáilte 2 mharc" (2015 Higher Fógra a hAon): a
    // numbered question and its one answer before the tariff, as the Ordinary grid prints them.
    if (PROMPT.test(head) && question > 0 && /^[A-ZÁÉÍÓÚ]/.test(tidy(head.slice(question + 1))) && !/[.?]$/.test(head)) {
      open(tidy(head.slice(0, question + 1)), tariff);
      current!.rows.push({ text: tidy(head.slice(question + 1)), marks: tariff });
      continue;
    }
    if (/\?$/.test(head) || PROMPT.test(head)) { open(head, tariff); continue; }
    if (question >= 0) {
      open(tidy(head.slice(0, question + 1)), tariff);
      current!.rows.push({ text: tidy(head.slice(question + 1)), marks: tariff });
      continue;
    }
    // A grid row the paper prints as a statement ("Scríobh síos lá amháin … gach seachtain. Déardaoin 3 mharc",
    // 2020 Ordinary Fógra a hAon): the card's printed question, then its first answer at that price.
    const statement = head.indexOf('. ');
    if (!current && statement > 0 && printedQuestion(source.questionText, head.slice(0, statement + 1))) {
      open(tidy(head.slice(0, statement + 1)), tariff);
      current!.rows.push({ text: tidy(head.slice(statement + 1)), marks: tariff });
      continue;
    }
    // The 2026 question cards open with the question as the paper prints it ("Luaigh cúis amháin … ar Phól. 2 mharc"):
    // a statement, not a question, but the card's own sub-question all the same.
    if (!current && head && printedQuestion(source.questionText, head)) { open(head, tariff); continue; }
    if (!current) return { ok: false, reason: 'tariff before any sub-question' };
    if (!head) continue;
    current.rows.push({ text: head, marks: tariff });
  }
  if (!stopped) {
    const tail = text.slice(pos);
    const { lead, bullets } = splitBullets(tail);
    // Under a heading such as "Rud amháin as na rudaí seo a leanas:" (2015 Higher A 3(b)(i)) every bullet is an accepted answer,
    // however long ("• Éisteann na Comhairleoirí le díospóireachtaí (na dtoscairí óga)").
    const listed = /\bseo a leanas:$/.test(lead);
    for (const item of lead ? [lead, ...bullets] : bullets) {
      if (!current) break;
      if (FURNITURE.test(item)) break;
      if (RULE.test(item) || DIRECTION.test(item)) { directions.push(item); continue; }
      // "• Gearrann obair Foodcloud … = 2 mharc nó • Faigheann na bochtáin …" (2015 Higher A 4(b)(ii)): the word between two
      // answers, not one.
      if (item === 'nó') continue;
      // "Tá trí mharc ar fáil as dhá mhír ghramadaí a aithint; … Sampla d’ainmfhocal … = …Átha; … Sampla de bhriathar … = Tá; Is"
      // (2015 Higher 6(a)): under a ladder, the rule and then one sample answer for each item the ladder counts.
      const pieces = current.ladder ? item.split(/\s(?=Sampla\b)/) : [item];
      if (pieces.length > 1) {
        if (!/^Sampla\b/.test(pieces[0])) directions.push(tidy(pieces.shift()!));
        pieces.forEach(piece => current!.rows.push({ text: tidy(piece) }));
        continue;
      }
      if (!listed && /^[A-ZÁÉÍÓÚ]/.test(item) && !/[=]/.test(item) && !current.ladder && current.rows.length > 0 && item.length > 60) directions.push(item);
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
    const rows: IrishAnswerRow[] = part.rows.map((row, rowIndex) => ({ id: `r${rowIndex + 1}`, text: row.text.split(HELD).join(' '), marks: row.marks ?? 0 }));
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

/** One printed answer carrying every point a ladder prices ("… ar oíche áirithe (pointe amháin eolais) agus eolas cruinn …
 *  (an dara pointe eolais)", 2018 Higher A 1(a)): on the card the student claims how many of its points they made, so the
 *  answer steps through the ladder ([0, 2, 3]) rather than paying its first rung alone. Applied where a card's criterion
 *  takes its rows (factory.ts), after any slot card has read the part's ladder. */
export const stepSingleAnswerLadders = (allocation: IrishAllocation): IrishAllocation => ({
  ...allocation,
  parts: allocation.parts.map(part => (part.ladder && part.ladder.length > 1 && part.rows.length === 1
    ? { id: part.id, ...(part.prompt ? { prompt: part.prompt } : {}), tariff: part.tariff, ...(part.samples ? { samples: part.samples } : {}),
      rows: [{ ...part.rows[0], marks: part.tariff, steps: [0, ...part.ladder] }] }
    : part)),
});

export function irishAnswersFor(source: IrishAnswerSource): IrishAllocation | undefined {
  const result = parseIrishAnswers(source);
  return result.ok ? result.allocation : undefined;
}
