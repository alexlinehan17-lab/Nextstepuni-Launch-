/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Foundation official answers as claimable rows.
 *
 * The Foundation builders write each listening, matching and reading part as one "Freagra" criterion whose guidance
 * is the scheme's answer (and, for some reading parts, the scheme's other accepted answers and part-mark answers).
 * A priced scheme answer is a claimable row carrying its marks, never a direction, so each such criterion becomes the
 * official-answer row model the Higher and Ordinary listening and reading cards use: one part at the criterion's
 * printed tariff, one row per printed answer at its printed mark, any one of which earns it (the part is an answer
 * list, so the best claimed row counts), and the scheme's rules (penalties, "Glactar le córas eile …", "= 0" answers)
 * as directions. Every row and direction is a slice of the card's own lifted guidance: the table below is checked
 * against it when the module loads, so a row the scheme does not print cannot ship.
 */
import type { IrishAllocation, IrishAnswerRow, IrishCriterion } from '../../../../types/markBank';
import { splitSlashRows } from './slashSplits';

type Row = readonly [text: string, marks: number];
/** A priced item, or the scheme's own "X = 0" ruling (a direction, never a claimable row). */
type Priced = Row | readonly [direction: string];
interface Reviewed { rows: readonly Row[]; directions: readonly string[] }

const squash = (value: string) => value.replace(/\s+/g, ' ').trim();

/**
 * Reading parts whose scheme prints more than one accepted answer or a part-mark answer in a shape the general
 * reader below does not cut: the accepted-answer lists the 2010 and 2011 text layers run together (the page sets one
 * answer per line; a two-line answer quotes two lines of the poem), and lines that mix answers, "= 0" answers and
 * penalties. Each entry was read against the scheme page. Marks are the printed ones.
 */
const REVIEWED: Record<string, Reviewed> = {
  'irish-2010-fl-r-3a-3': {
    rows: [['Ceol traidisiúnta', 6], ['traidisiúnta', 6], ['Ní rac ná miotal trom a sheinneann Sharon ach ceol traidisiúnta', 6],
      ['ceol traidisiúnta bunaithe ar thraidisiún na hÉireann (agus ar thraidisiún na cruinne)', 6], ['An t-alt iomlán', 6],
      ['Ceol draíochta', 4]],
    directions: ['Bosca ceoil = 0', 'Ceol = 0'],
  },
  'irish-2010-fl-r-3b-2': {
    rows: [['Chun dul ar bord loinge lena hathair', 6], ['chun dul ar bord loinge', 6],
      ['ghearr sí an ghruaig fhada rua a bhí uirthi chun dul ar bord loinge', 6],
      ['ghearr sí an ghruaig fhada rua a bhí uirthi chun dul ar bord loinge (lena hathair)', 6]],
    directions: ['Má bhíonn iomarcaíocht sa fhreagra: (6 - 2) i gcás freagra ina bhfuil eolas iomarcach.'],
  },
  'irish-2010-fl-r-3c-4': {
    rows: [['Síol', 6], ['D’ith sé síol', 6], ['(Is) d’ith sé síol go craosach', 6], ['Má scríobhtar dhá líne', 4]],
    directions: ['Má scríobhtar an véarsa ar fad: 6 - 6 = 0'],
  },
  'irish-2011-fl-r-3a-2': {
    rows: [['D’oibrigh sé i siopa búistéara', 6], ['D’oibrigh sé i siopa búistéara nuair a bhí sé ina dhéagóir', 6],
      ['Búistéar', 6], ['(Post) Mar bhúistéar', 6], ['Búistéar, sorcas, thiomáin sé bád', 6]],
    directions: ['Iomarcaíocht: abairt sa bhreis: -2 ; dhá abairt sa bhreis: - 4; trí abairt sa bhreis: -6.'],
  },
  'irish-2011-fl-r-3b-4': {
    rows: [['D’fhill Willie ar Chontae an Chláir', 6], ['D’fhill Willie ar Chontae an Chláir (sa bhliain 1957)', 6],
      ['D’fhill sé ar Chontae an Chláir', 6], ['D’fhill sé abhaile (ó Londain/go Contae an Chláir)', 6],
      ['D’fhill Willie ar Chontae an Chláir (sa bhliain 1957. D’fhoghlaim na mílte ceoltóirí uaidh.', 6]],
    directions: ['Iomarcaíocht: abairt sa bhreis: -2 ; dhá abairt sa bhreis: - 4; trí abairt sa bhreis: -6.'],
  },
  'irish-2011-fl-r-3c-2': {
    rows: [['Níor ith sé dada feadh dhá lá', 6], ['Níor ith sé dada feadh dhá lá Is bhí an t-ocras mór dá chrá', 6]],
    directions: ['Iomarcaíocht: abairt sa bhreis: -2 ; dhá abairt sa bhreis: - 4; trí abairt sa bhreis: -6.'],
  },
  // "Clárú = 6 mharc. Is gá … = 6 mharc." then a two-sentence answer the scheme prices whole.
  'irish-2021-fl-r-3b-5': {
    rows: [['Clárú isteach', 6], ['Clárú', 6], ['Is gá don chuairteoir clárú isteach i ngach gailearaí', 6],
      ['Faigheann gach cuairteoir pas ag dul isteach sa mhúsaem. Is gá don chuairteoir clárú isteach i ngach gailearaí', 6]],
    directions: [],
  },
  // Two pairs of lines from the last verse, each priced "Iomarcaíocht 6-2 = 4 mharc": answers at 4, not penalties.
  'irish-2021-fl-r-3c-5': {
    rows: [['An aois', 6], ['Líne 2 agus Líne 3 as an véarsa deireanach', 4], ['Líne 3 agus Líne 4 as an véarsa deireanach', 4]],
    directions: [],
  },
};

const PRICE = /(\d+)\s*mh?arc\s*:\s*/g;
const PENALTY = /pionós|Iomarcaíocht|[Gg]lac(?:tar|far) le córas eile/;

/** The answers one guidance line prices, or undefined where the line is a rule. */
const pricedSegments = (line: string): Priced[] | undefined => {
  // "6 mharc: A; B. 4 mharc: C." — a price, then the answers it buys, cut at "; " (never inside brackets, where the
  // scheme lists the forms of one answer). A trailing "X = 0" ("Bialann. Téann sí lena cairde = 0") is a ruling.
  if (/^\s*\d+\s*mh?arc\s*:/.test(line)) {
    const rows: Priced[] = [];
    const pieces = line.split(PRICE).slice(1);
    for (let index = 0; index < pieces.length; index += 2) {
      const marks = Number(pieces[index]);
      for (const answer of pieces[index + 1].split(/;\s*(?![^()]*\))/)) {
        const text = answer.trim().replace(/\.$/, '').trim();
        const ruling = /^(.*?)\.\s+(\S.*=\s*0)$/.exec(text);
        if (ruling) rows.push([ruling[1].trim(), marks], [ruling[2].trim()]);
        else if (/=\s*0$/.test(text)) rows.push([text]);
        else if (text) rows.push([text, marks]);
      }
    }
    return rows;
  }
  // "Páirt i scannáin mhóra: 7 marc. Páirt i Ros na Rún: 5 mharc." / "Ranganna Céilí — 5 mharc." / "Clárú = 6 mharc."
  const pairs = [...line.matchAll(/([^.:=—]+?)\s*(?::|=|—)\s*(\d+)\s*mh?arc\b\.?/g)];
  if (pairs.length && squash(line.replace(/([^.:=—]+?)\s*(?::|=|—)\s*(\d+)\s*mh?arc\b\.?/g, '')) === '') {
    return pairs.map(match => [match[1].trim(), Number(match[2])] as Row);
  }
  return undefined;
};

const rowsOf = (rows: readonly Row[]): IrishAnswerRow[] =>
  rows.map(([text, marks], index) => ({ id: `r${index + 1}`, text, marks }));

/** The official-answer rows for one Foundation answer criterion, or undefined where its guidance is not cut. */
export const foundationAllocation = (cardId: string, criterion: IrishCriterion): IrishAllocation | undefined => {
  const guidance = criterion.guidance;
  const reviewed = REVIEWED[cardId];
  if (reviewed) {
    const source = squash(guidance.join(' '));
    for (const piece of [...reviewed.rows.map(([text]) => text), ...reviewed.directions]) {
      if (!source.includes(squash(piece))) throw new Error(`Foundation row is not the scheme's words: ${cardId} "${piece}"`);
    }
    return { parts: [{ id: 'p1', tariff: criterion.maxMarks, rows: rowsOf(reviewed.rows) }], directions: [...reviewed.directions] };
  }
  const rows: Row[] = [];
  const directions: string[] = [];
  for (const [index, line] of guidance.entries()) {
    // "0 marc: líne2 leis féin." prices an answer at nothing: the scheme's ruling, not a row.
    if (index > 0 && /^\s*0\s*mh?arc\s*:/.test(line)) { directions.push(line.trim()); continue; }
    const priced = pricedSegments(line);
    if (priced) {
      for (const item of priced) {
        if (item.length === 1) { directions.push(item[0]); continue; }
        const [text, marks] = item;
        if (marks > 0 && marks <= criterion.maxMarks) rows.push([text, marks]);
        else return undefined;
      }
    } else if (index === 0) {
      rows.push([line.trim(), criterion.maxMarks]);
    } else if (PENALTY.test(line)) {
      directions.push(line.trim());
    } else {
      return undefined;
    }
  }
  if (!rows.length || !rows.some(([, marks]) => marks === criterion.maxMarks)) return undefined;
  return { parts: [{ id: 'p1', tariff: criterion.maxMarks, rows: rowsOf(rows) }], directions };
};

/** Answer criteria whose guidance is not cut into rows (listed, never guessed). */
export const FOUNDATION_UNCUT: string[] = [];

/** What a right answer with too much in it earns, as the scheme prints it: "(6 - 2) i gcás freagra ina bhfuil eolas
 *  iomarcach" (2010), "Iomarcaíocht: abairt sa bhreis: -2 ; dhá abairt sa bhreis: - 4; trí abairt sa bhreis: -6" (2011),
 *  "Iomarcaíocht: abairt bhreise — pionós −2." (2012), "pionós −2; Véarsa3 ar fad: pionós −4." (2013), "Líne bhreise amháin:
 *  pionós −2; An véarsa ar fad (-4)." (2014). A row priced whole steps at those marks, where the criterion permits them (set
 *  from the scheme) and its rows cannot yet reach them (coordinator, 12 Nov: fix the rows, never the permitted marks). */
const penaltySteps = (allocation: IrishAllocation, permitted: number[]): IrishAllocation => {
  const notes = allocation.directions.join(' ');
  const penalties = [...notes.matchAll(/\(\s*(\d+)\s*-\s*(\d+)\s*\)\s*i gcás freagra ina bhfuil eolas iomarcach|(?:sa bhreis:|pionós|ar fad)\s*\(?\s*[-−]\s*(\d+)/g)]
    .map(match => (match[3] !== undefined ? Number(match[3]) : Number(match[2])));
  if (!penalties.length) return allocation;
  const reach = new Set([0, ...allocation.parts.flatMap(part => part.rows.map(row => row.marks))]);
  const parts = allocation.parts.map(part => ({
    ...part,
    rows: part.rows.map(row => {
      if (row.steps || row.marks !== part.tariff) return row;
      const added = penalties.map(penalty => row.marks - penalty).filter(value => value > 0 && permitted.includes(value) && !reach.has(value));
      return added.length ? { ...row, steps: [...new Set([0, ...added, row.marks])].sort((x, y) => x - y) } : row;
    }),
  }));
  return { ...allocation, parts };
};

/** A Foundation criterion as the bank shows it: an answer criterion with rows is the scheme's official answer. */
export const foundationCriterion = (cardId: string, criterion: IrishCriterion): IrishCriterion => {
  if ((criterion.guidanceKind as string) !== 'exact-answer') return criterion;
  const cut = foundationAllocation(cardId, criterion);
  const allocation = cut && penaltySteps(cut, criterion.permittedMarks);
  if (!allocation) FOUNDATION_UNCUT.push(`${cardId}/${criterion.id}`);
  return { ...criterion, guidanceKind: 'exact', ...(allocation ? { allocation: splitSlashRows(cardId, criterion.id, allocation) } : {}) };
};
