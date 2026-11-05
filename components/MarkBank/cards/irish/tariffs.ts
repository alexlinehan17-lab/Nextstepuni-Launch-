/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * An Irish scheme's PRICED TARIFF, cut into sub-questions and rows.
 *
 * The literature schemes (Prós, Filíocht, Litríocht) and the last reading
 * question print no answer list: they price what the student must do —
 * "Príomhthéama = 2 mharc", "Dhá phointe eolais = 4 mharc + 4 mharc",
 * "Tréith 1 = 13 mharc" with a band table under it — and add sample points
 * ("Freagraí samplacha: • …") that the scheme itself calls a sample. Carded
 * whole, all of that sat as prose over a 0–25 slider. Alex's rule
 * (2026-10-23): what the scheme prices is a row with its marks on it.
 *
 * So each priced phrase becomes a row in the scheme's own words: a phrase
 * priced whole claims its marks, a phrase priced in slots ("4 mharc + 4
 * mharc") or under a band table places on steps, a sub-question's "(9 marc)"
 * or "Eolas = 13 mharc" opens a part whose rows must add up to it (and a
 * "(2 mharc)" printed AFTER two one-mark rows closes them as one), the
 * samples stay a list under the part, and the rule sentences ("Nóta: …",
 * "Ní mór teideal …", "[Gaeilge lochtach: …]") are directions. Nothing is
 * typed: every row, prompt, sample and direction is a slice of the guidance.
 */
import type { IrishAllocation, IrishAnswerPart, IrishAnswerRow } from '../../../../types/markBank';
import type { IrishAnswerResult, IrishAnswerSource } from './answers';
import { parseIrishAnswers } from './answers';

const MARC = String.raw`(\d+)\s*m?h?arc\b`;
const SUM = String.raw`((?:\s*\+\s*\d+\s*m?h?arc\b)*)`;
/** A sub-question marker before its prompt: "(i)", "(b) (i)", "6. (a)", "(b)" before a capital. */
const SUB = /(?<=^|\s)(?:\d\.\s*)?(?:\(?[a-f]\)\s*)?\((?:i|ii|iii|iv|v)\)\s|(?<=^|\s)(?:\d\.\s*)?\(?[a-f]\)\s(?=[A-ZÁÉÍÓÚ‘(])/g;
/** What opens or closes a part: "(9 marc)", "{3 mharc: 2 mharc + 1 mharc}", "{6 mharc + 6 mharc}", "Eolas = 13 mharc". */
const OPENER = new RegExp(String.raw`\(\s*${MARC}\s*\)|\{\s*${MARC}(?::\s*((?:\d+\s*m?h?arc\b\s*\+?\s*)+))?${SUM}\s*\}|(?<=^|\s)Eolas\s*=\s*${MARC}${SUM}`, 'g');
/** A priced phrase: "X = 13 mharc", "X = 4 mharc + 4 mharc", "Pointe eolais 1 = Plé … = 5 mharc". */
const PRICED = new RegExp(String.raw`([^•¶\n]{2,400}?)\s*=\s*${MARC}${SUM}(?!\s*(?:ar|an|ceann)\b)`, 'g');
/** "Tréithe samplacha:" and "Ábhair imní:" (2014 Higher A and B 6(b)) head their lists as "Samplaí" does, and so does "B’fhéidir go
 *  mbeadh rudaí mar seo luaite," (2012 Higher A 6(b)). */
const SAMPLES = /(?:\b(?:Freagraí samplacha|Pointí eolais féideartha|(?<!\bas\s)(?<!\bag tabhairt\s)Samplaí|Freagra samplach|Sampla cruinn:|Tréithe samplacha|B’fhéidir go mbeadh rudaí mar seo luaite,)|(?<![A-Za-zÁÉÍÓÚáéíóú])Ábhair imní(?=:))\s*:?\s*/i;
/** Where a sample list ends because a split-priced phrase follows it: "Samplaí: Brón, … bród… Dhá shampla = 4 mharc + 4 mharc", or a
 *  numbered point's price: "Samplaí : Doicheall, … teannas… Pointe eolais 1 = 3 mharc" (2015 Higher 4F(iii)).
 *  Only a split ("a + b"), and never a verse reference, which stays inside its sample list whatever its price ("… gheal…
 *  Véarsa a haon, Línte 3 + 4 = 2 mharc", 2018 Ordinary 3A(a)(i); "… maidí rámha… Véarsa a ceathair, Línte 1 - 7 = 2 mharc +
 *  2 mharc", 2017 Ordinary 3A(b)(i)(c)). */
const SAMPLES_RESUME = /…\s+(?=(?!Véarsa\b)[A-ZÁÉÍÓÚ][^•¶=…]{0,60}=\s*\d+\s*m?h?arc\s*\+\s*\d+\s*m?h?arc\b|Pointe eolais \d+\s*=\s*\d+\s*m?h?arc\b)/;
/** "Cén uair a bhíonn an spailpín … i véarsa a haon? 2 mharc Freagraí Samplacha: Go moch ar maidin = 2 mharc … Go moch = 1 mharc"
 *  (2016 Ordinary 3A(b)(i)): a question's bare price, then its answers each at its own price under the heading: an answer key
 *  of alternatives, which the answer reader cuts (cards/irish/answers.ts). The heading is not an answer's text. */
const ANSWER_KEY = /([?.])\s+(\d+\s*m?h?arc\b)\s+Freagraí [Ss]amplacha:\s*(?=[^•¶=]{1,120}?=\s*\d+\s*m?h?arc\b)/g;
const BAND_TABLE = /\bCatagóir\b[\s\S]*?Lag\/An-lag[^•]*?\d+\s*-\s*\d+(?:\s+\d+\s*-\s*\d+)*/;
/** "Dhá cheann le freagairt-an ceann is fearr a mharcáil as 13 mharc agus an ceann eile a mharcáil as 12 mharc" (2016 Higher
 *  2A, 2B): what the scheme marks "out of N" (a mharcáil as N), from the clause's start. "a mheas as N" (the Gaeilge
 *  assessment) is not read, nor "an t-eolas a mharcáil as N" (Ceist 4A–E), which the Ceist 4 rule prices. */
const MARK_AS = /(?:^|\bagus\s+|[.;:]\s+|-\s?(?=an\s))((?:an|na)\s[^.;:]*?)\s+a mharcáil as (\d+)\s*m?h?arc\b/gi;
/** "5 phointe eolais ag teastáil (5 mharc an ceann ar an gcéad trí phointe eolais + 4 mharc an ceann ar an dá phointe eolais eile)",
 *  also printed with a full stop before the bracket closes ("… ar na trí phointe eolais eile.)", 2017 Ordinary 2B(a)).
 *  The counts are words with fadas ("dá", "trí"), so they are read as \S+: a \w+ never matched them. */
const LADDER = /(\d+)\s*phointe eolais ag teastáil\s*\(\s*(\d+)\s*m?h?arc an ceann ar an g?c?[ée]ad\s+(\S+)\s+phointe eolais(?:\s*\+\s*(\d+)\s*m?h?arc an ceann ar (?:an|na)\s+(\S+)\s+phointe eolais eile)?\.?\s*\)/i;
const NOTE = /(?<=^|\s|\()(?:Nóta:|Ní mór(?=\s)|Is leor(?=\s)|Caithfidh(?=\s)|Bainfear(?=\s)|Gearrfar(?=\s)|Glacfar(?=\s)|Tabharfar(?=\s)|Mura mbíonn(?=\s)|Cuir lúibíní(?=\s)|Dá bharr sin(?=\s)|Gan tréith(?=\s)|Tá [^\s]+ mharc ag gabháil(?=\s)|Sampla cruinn gan(?=\s)|Is samplaí de fhreagraí(?=\s)|Léirigh na marcanna(?=\s)|Ag bun(?=\s))[^•{}¶]*?(?:[.?!](?=\s|\)|$)|(?=\s\(?(?:i|ii|iii|iv|v)\)\s|\sNóta:|\sTreoir:|\s•|\s¶|\s\(\d+\s*m?h?arc\)|\s\{\d|$))/g;
const DEDUCTION = /\[Gaeilge lochtach:[^\]]*\]/g;
/** "Nóta: 1. Mura bhfuil an téama luaite … (3+3) 2. Téama luaite (2 mharc) agus … (2+2). 3. Gan an téama luaite … = 0" (2015
 *  Ordinary 3A(a)(i)): a numbered note runs through its numbered items to the next sub-question; NOTE alone stops at "1.". */
const NUMBERED_NOTE = /(?<=^|\s)Nóta:\s*1\.\s[^•{}¶]*?\s2\.\s[^•{}¶]*?(?=\s\(?(?:i|ii|iii|iv|v)\)\s|\s•|\s¶|$)/g;
/** "Is maith / Ní maith = (1 mharc) + dhá fháth = (4 mharc + 4 mharc)" (2015 Ordinary 3A and 3B (iii)): a price printed in
 *  brackets after its "=" is that phrase's price, not a sub-question's tariff. */
const BRACKETED_PRICE = /=\s*\(\s*(\d+\s*m?h?arc\b(?:\s*\+\s*\d+\s*m?h?arc\b)*)\s*\)/g;
/** 2015 Higher 6(b) prices each part with an arrow: "Tuairim (2) ► 2 mharc", "Cúis 1 (2 mharc) + Sampla 1 (3 mharc) ► 5 mharc".
 *  Each named piece is a row at its bracketed price, where the pieces add up to the arrow's. */
const ARROW = /([A-ZÁÉÍÓÚ][^\s•¶=►(){}.:;?!]*(?:\s[^\s•¶=►(){}.:;?!]+){0,3}?)\s*\((\d+)(?:\s*(m?h?arc))?\)(?:\s*\+\s*([A-ZÁÉÍÓÚ][^\s•¶=►(){}.:;?!]*(?:\s[^\s•¶=►(){}.:;?!]+){0,3}?)\s*\((\d+)\s*(m?h?arc)\))?\s*►\s*(\d+)\s*(m?h?arc)\b/g;
/** The examiner's box printed after each of those prices ("T =", "C (1) + S (1) =", "C(2) =", "T1 (2) + S1 (3) ="): the marking
 *  panel, never the scheme's text. Read only where the arrows are. */
const ARROW_BOX = /(?<=\bm?h?arc)\s+[A-Z]\d?\s*(?:\(\s*\d+\s*\))?(?:\s*\+\s*[A-Z]\d?\s*\(\s*\d+\s*\))*\s*=(?=\s|$)/g;
/** "Línte cuí ón dán gan rian an iarrthóra orthu = 2 mharc + 2 mharc" printed straight after a price, with no "Nóta:" before it
 *  (2017 Ordinary 3A(b)(iii)): what lines lifted without the candidate's own words earn instead, a direction as its "Nóta:"
 *  form is, never a row. */
const LIFTED_LINES = /(?<=\bm?h?arc\s)Línte cuí(?=\s)[^•=¶]*?=\s*\d+\s*m?h?arc\b(?:\s*\+\s*\d+\s*m?h?arc\b)*/g;
/** "Trí phointe eolais ag teastáil anseo: 2 mharc an ceann ar na trí phointe eolais": how a row divides, a direction. */
const COUNT_NOTE = /\b(?:Dhá|Trí|Ceithre|Cúig|\d+)\s+phointe eolais ag teastáil(?: anseo)?:?\s*\d+\s*m?h?arc an ceann ar (?:an|na)[^•=(]*?(?=\s[A-ZÁÉÍÓÚ(]|$)/g;
/** "5 mharc = 2 mharc ar lomphointe eolais + 3 mharc ar fhorbairt": how one point's marks divide, a direction. */
const SPLIT_NOTE = /\b(?:\d+\s*m?h?arc\s*\/\s*)?\d+\s*m?h?arc\s*=\s*\d+\s*m?h?arc\s+ar\s[^•]*?(?=\s(?:\d+\s*m?h?arc\s*=|\(|[A-ZÁÉÍÓÚ][^\s=]*(?:\s[^\s=]+){0,6}\s*=)|$)/g;
const FURNITURE = /\b(?:Léirigh mionbhriseadh na marcanna|Eolas\s*\(\d+\)\s*=\s*Gaeilge|E\s*\(\d+\)\s*=|An Mharcáil:|T\d\s*\(\d\)\s*\+\s*S\d|C\s*\d\s*\([A-B]\)\s*\(\d+\)\s*=)[\s\S]*$/;
/** The band header the scheme prints under each sub-question without its ranges: "Catagóir Marc as 4 Sármhaith An-mhaith Maith Measartha Lag/An-lag". */
const BAND_HEADER = /\bCatagóir Marc as \d+\s+Sármhaith\s+An-mhaith\s+Maith\s+Measartha\s+Lag\/An-lag(?:\s+\d+\s*-\s*\d+)*/g;
/** The same header over a criterion's points rather than its total (2022 Higher 4F(ii)): "Catagóir Pointe eolais 1
 *  (4 mharc) Pointe eolais 2 (4 mharc) Sár-mhaith … Lag/An-lag". Its "(4 mharc)" columns are the bands' grid, not parts. */
const POINT_BAND_HEADER = /\bCatagóir(?:\s+Pointe eolais \d+\s*\(\d+\s*m?h?arc\))+\s+Sár-?mhaith\s+An-mhaith\s+Maith\s+Measartha\s+Lag\/An-lag/g;
/** The Gaeilge criterion's descriptor table, printed after each Eolas table: "(5 mharc) Sárchumas … Cumas lag/an-lag … (gramadach, …)". */
const GAEILGE_TABLE = /(?:Gaeilge\s*)?\(\d+\s*m?h?arc\)\s*Sárchumas[\s\S]*?Cumas lag\/an-lag[^.•(]*(?:\([^)]*\))?/g;
const WORDS: Record<string, number> = { aon: 1, amháin: 1, dá: 2, dhá: 2, trí: 3, ceithre: 4, cúig: 5, sé: 6 };
/** "5 phointe eolais: 7 marc an ceann ar thrí phointe eolais agus 2 mharc ar an dá cheann eile." (2015 Ordinary 2A) and "5 phointe
 *  eolais: 7 marc ar an gcéad dá phointe eolais, 5 mharc ar an tríú pointe eolais agus 2 mharc ar an dá cheann eile." (2B): the
 *  points the answer wants and each clause's price per point, read clause by clause (SHARE). */
const POINT_SHARES = /(\d+)\s*phointe eolais:\s*([^.]*?\bcheann eile)\./i;
const SHARE = /^(\d+)\s*m?h?arc (?:an ceann )?ar (?:an\s+)?(?:g?c[ée]ad\s+)?(?:(\S+)\s+(?:phointe eolais|cheann eile)|tríú pointe eolais)$/i;

/** What `text` adds to an already placed row's `label` ("Ainm an fhile" → "Ainm an fhile = Caitlín Maude": "Caitlín
 *  Maude"), or undefined when it is not that row. Read past a séimhiú the scheme drops ("Ainm an file = …"). */
const unlenite = (value: string) => value.replace(/(?<=^|\s)([bcdfgmpstBCDFGMPST])h/g, '$1');
const answerOf = (label: string, text: string): string | undefined => {
  for (const [head, full] of [[label, text], [unlenite(label), unlenite(text)]]) {
    if (full.startsWith(head) && /^[ =:]/.test(full.slice(head.length)) && full.length > head.length + 2) {
      const at = text.length - (full.length - head.length);
      return text.slice(at).replace(/^\s*[=:]\s*/, '').trim();
    }
  }
  return undefined;
};
const tidy = (value: string) => value.replace(/¶/g, ' ').replace(/\s+/g, ' ').replace(/^[\s,;:.•–-]+|[\s,;:–-]+$/g, '').trim();
const cumulative = (values: number[]): number[] => {
  const out = [0];
  for (const value of values) out.push(out[out.length - 1] + value);
  return out;
};
const range = (marks: number) => Array.from({ length: marks + 1 }, (_, index) => index);
/** Each point's price in print order, or undefined unless every clause reads and the clauses count the printed number of points. */
const pointShares = (match: RegExpExecArray): number[] | undefined => {
  const values: number[] = [];
  for (const clause of match[2].split(/,\s*|\s+agus\s+/)) {
    const share = SHARE.exec(clause.trim());
    if (!share) return undefined;
    const count = share[2] === undefined ? 1 : WORDS[share[2].toLowerCase()] ?? WORDS[unlenite(share[2]).toLowerCase()];
    if (!count) return undefined;
    values.push(...Array(count).fill(Number(share[1])));
  }
  return values.length === Number(match[1]) ? values : undefined;
};
const stripMarker = (value: string) => tidy(value.replace(/^(?:\d\.\s*)?(?:\(?[a-f]\)\s*)?(?:\(\s*(?:i|ii|iii|iv|v)\s*\)\s*)?/, ''));

interface Draft { prompt?: string; tariff: number; ladder?: number[]; rows: IrishAnswerRow[]; samples: string[]; unpriced?: string }
type Token = { kind: 'open'; tariff: number; ladder?: number[]; at: number; end: number }
  | { kind: 'row'; text: string; marks: number; steps?: number[]; at: number; end: number };

/** Lines after a reviewed criterion's own guidance that summarise the whole section's tariffs
 *  ("Freagair Léamhthuiscint A agus Léamhthuiscint B. Tá Ceist 1 – 5 ar cómharc …") or restate an
 *  order-dependent award: never this criterion's prices (cards/irish/answers.ts reads them the same way). */
const SECTION_SUMMARY = /^(?:Freagair Léamhthuiscint|Tá Ceist \d+\s*[–-]\s*\d+ ar cómharc|Order-dependent award)/;

/** The guidance of one criterion as parts of rows, or the reason it cannot be. */
export function parseIrishTariffs(source: IrishAnswerSource, debug?: string[]): IrishAnswerResult {
  if (source.guidance.some(line => new RegExp(ANSWER_KEY.source).test(line))) {
    return parseIrishAnswers({ ...source, guidance: source.guidance.map(line => line.replace(ANSWER_KEY, '$1 $2 ')) });
  }
  const directions: string[] = [];
  let text = source.guidance.filter((line, index) => index === 0 || !SECTION_SUMMARY.test(line.trim())).join(' ').replace(/[\uf0a7\uf0b7\u25aa\u2022]/g, ' • ').replace(/\s+/g, ' ').trim();
  // "Ní mór teideal an dáin sin, mar aon le hainm an fhile, a scríobh síos go soiléir. (2 mharc)" alone (2012 and 2013 Ordinary
  // 2B and 3B): the title line printed with its price and nothing under it is the ask that price is for, never a note: its own
  // words are the row, claimed whole (the scheme prints no split).
  const titleAsk = /^(Ní mór teideal [^=•¶()]*?\.)\s*\(\s*(\d+)\s*m?h?arc\s*\)$/.exec(text);
  if (titleAsk && Number(titleAsk[2]) === source.totalMarks) {
    return { ok: true, allocation: { parts: [{ id: 'p1', tariff: source.totalMarks, rows: [{ id: 'r1', text: titleAsk[1], marks: source.totalMarks }] }], directions: [] } };
  }
  // "(i) (a) Cad as don ainmhí seo? (Géibheann thíos) (b) Cá bhfuil an t-ainmhí anois, dar leat? (c) … (d) … (8 marc)" (2012
  // Ordinary 3A(i)): printed questions (a)–(d) that the scheme prices only together, with nothing else printed: one sub-question,
  // its questions the prompt and the row, claimed whole.
  const shared = /^\(\s*(?:i|ii|iii|iv|v)\s*\)\s*(\(a\)\s[^=•¶]*?)\s*\(\s*(\d+)\s*m?h?arc\s*\)$/.exec(text);
  if (shared && Number(shared[2]) === source.totalMarks && !/\d+\s*m?h?arc\b/.test(shared[1])) {
    const questions = shared[1].split(/\s(?=\([b-f]\)\s)/);
    if (questions.length >= 2 && questions.every((question, index) => question.startsWith(`(${'abcdef'[index]}) `) && /\?(?:\s*\([^()]*\))?$/.test(question.trim()))) {
      const asked = tidy(shared[1]);
      return { ok: true, allocation: { parts: [{ id: 'p1', prompt: asked, tariff: source.totalMarks, rows: [{ id: 'r1', text: asked, marks: source.totalMarks }] }], directions: [] } };
    }
  }
  // "6 phointe eolais. ( 5 mharc ar an gcéad phointe + 5 phointe eile ar 4 mharc an ceann)." and "4 phointe eolais. (7 marc ar an
  // gcéad phointe + 6 mharc an ceann ar trí phointe eile)." (2012 Ordinary 2A(a), 2A(b)): the points the answer needs, the first at
  // its own price and each of the rest at theirs. Where the counts agree it reads as that row's split ("6 phointe eolais = 5 mharc
  // + 4 mharc + …"): one row in the scheme's words, one step a point ([0, 5, 9, 13, 17, 21, 25]).
  text = text.replace(/(\d+)\s*phointe eolais\.\s*\(\s*(\d+)\s*(m?h?arc) ar an gcéad phointe\s*\+\s*(?:(\S+)\s+phointe eile ar (\d+)\s*m?h?arc an ceann|(\d+)\s*m?h?arc an ceann ar (\S+)\s+phointe eile)\s*\)\.?/gi,
    (whole: string, count: string, first: string, unit: string, restA?: string, eachA?: string, eachB?: string, restB?: string) => {
      const restWord = (restA ?? restB)!;
      const rest = WORDS[restWord.toLowerCase()] ?? Number(restWord);
      if (!rest || 1 + rest !== Number(count)) return whole;
      return `${count} phointe eolais = ` + [Number(first), ...Array(rest).fill(Number(eachA ?? eachB))].map(value => `${value} ${unit}`).join(' + ');
    });
  // "Tréith 1 ( 2 mharc) + Sampla 1 ( 4 mharc) ► 6 mharc" (2014 Higher A and B 6(b)): one half's split, each piece priced in
  // brackets and their total after the arrow. Where the pieces add up to it, it reads as the split "Tréith 1 = 2 mharc + Sampla 1
  // = 4 mharc" (2016's "Aidhm a lua = 2 mharc + Forbairt = 4 mharc"); the total is the half's own, which the slots carry.
  // Not where the examiner's box follows the arrow ("► 5 mharc T1 (2) + S1 (3) =", 2015 Higher B 6(b)): the "►" reader prices those.
  text = text.replace(/\(\s*(\d+)\s*(m?h?arc)\s*\)\s*\+\s*([^•¶►()+=]{1,60}?)\s*\(\s*(\d+)\s*(m?h?arc)\s*\)\s*►\s*(\d+)\s*m?h?arc\b(?!\s*[A-ZÁÉÍÓÚ]\d*\s*\(\s*\d+\s*\))/g,
    (whole: string, first: string, unit: string, label: string, second: string, unit2: string, total: string) =>
      (Number(first) + Number(second) === Number(total) ? `= ${first} ${unit} + ${label} = ${second} ${unit2}` : whole));
  if (text.includes('►')) {
    text = text.replace(ARROW, (whole: string, first: string, a: string, unitA: string | undefined, second: string | undefined, b: string | undefined,
      unitB: string | undefined, total: string, unit: string) => {
      if (Number(a) + Number(b ?? 0) !== Number(total)) return whole;
      return second ? `${first} = ${a} ${unitA ?? unit} ${second} = ${b} ${unitB}` : `${first} = ${total} ${unit}`;
    }).replace(ARROW_BOX, ' ');
  }
  text = text.replace(DEDUCTION, rule => { directions.push(tidy(rule)); return ' ¶ '; });
  text = text.replace(BRACKETED_PRICE, '= $1');
  text = text.replace(GAEILGE_TABLE, ' ¶ ');
  text = text.replace(BAND_HEADER, ' ¶ ');
  text = text.replace(POINT_BAND_HEADER, ' ¶ ');
  text = text.replace(FURNITURE, ' ¶ ');
  const bands: string[] = [];
  text = text.replace(BAND_TABLE, table => { bands.push(tidy(table)); return ' ¶ '; });
  text = text.replace(NUMBERED_NOTE, note => { directions.push(tidy(note)); return ' ¶ '; });
  // "Ní mór teideal an scannáin sin, mar aon le hainm an scríbhneora, a scríobh síos go soiléir Teideal an scannáin = 1 mharc"
  // (2013 Ordinary 2B(a)): the title requirement printed without its full stop before the rows that price it. The requirement
  // ends where its first row begins, as where the full stop is printed; the rows are never read into the note.
  text = text.replace(/(\bNí mór teideal [^.•¶=]*?a scríobh síos go (?:soiléir|cruinn))\s+(?=Teideal\b[^.•¶=]{0,40}=\s*\d+\s*m?h?arc\b)/g, '$1 ¶ ');
  // "(5 mharc ar an gceann is fearr + 4 mharc ar an gceann eile)" (2013 Ordinary 3A(a)(iii)): the better of the two answers the
  // question asks for at the first price, the other at the second. Each is a row at its printed price, in the scheme's words.
  text = text.replace(/\(\s*(\d+)\s*(m?h?arc) (ar )(an gceann is fearr) \+ (\d+)\s*(m?h?arc) (ar )(an gceann eile)\s*\)/g,
    (_, best: string, unit: string, _ar: string, bestText: string, other: string, unit2: string, _ar2: string, otherText: string) =>
      ` ¶ ${bestText} = ${best} ${unit} ¶ ${otherText} = ${other} ${unit2} ¶ `);
  // "Mothú a lua=1 mharc + dhá fháth :3 mharc + 2 mharc" (2013 Ordinary 3B(b)(ii)): the reasons' price printed after a colon,
  // read as "… + dhá fháth = 3 mharc + 2 mharc" is (2013 3A(b)(iii)).
  text = text.replace(/(\bdhá fháth)\s*:\s*(?=\d+\s*m?h?arc\s*\+\s*\d+\s*m?h?arc\b)/g, '$1 = ');
  // "(2 mharc) Cluain Meala; Tiobraid Árann; …; Margadh na saoire, aonach hireálta. (1 mharc + 1 mharc)" (2013 Ordinary
  // 3A(b)(i)(b)): the accepted answers listed between the question's tariff and how it divides. The split is the part's ladder
  // and each listed answer one of its rows, claimed in order; only where the split adds up to the tariff.
  text = text.replace(/\(\s*(\d+)\s*(m?h?arc)\s*\)\s+([^•¶=(){};]+(?:;[^•¶=(){};]+)+?)\s*\(\s*(\d+)\s*m?h?arc\s*\+\s*(\d+)\s*m?h?arc\s*\)/g,
    (whole: string, total: string, unit: string, list: string, first: string, second: string) => (Number(first) + Number(second) === Number(total)
      ? `{${total} ${unit}: ${first} mharc + ${second} mharc} ${list.split(';').map(item => item.trim()).filter(Boolean).map(item => `• ${item}`).join(' ')} ¶ `
      : whole));
  text = text.replace(NOTE, note => { directions.push(tidy(note)); return ' ¶ '; });
  // "Mura luaitear ach ceann amhain marcáil an freagra as 8 marc. Más lom insint ón sliocht atá ann marcáil as 7 marc." (2012 Higher
  // A 6(b)): what an answer naming one view, or retelling the passage, is marked out of: directions.
  text = text.replace(/(?:Mura luaitear ach ceann amh[aá]in|Más lom insint ón sliocht atá ann) marcáil (?:an freagra )?as \d+ marc\./g,
    note => { directions.push(tidy(note)); return ' ¶ '; });
  // "Treoir: Ní mór don iarrthóir …" (2015 Ordinary 2B(a)): the note went to the directions above; its heading is not a prompt.
  text = text.replace(/(?<=^|\s)Treoir:\s*(?=¶)/g, ' ');
  text = text.replace(SPLIT_NOTE, note => { directions.push(tidy(note)); return ' ¶ '; });
  text = text.replace(COUNT_NOTE, note => { directions.push(tidy(note)); return ' ¶ '; });
  text = text.replace(LIFTED_LINES, note => { directions.push(tidy(note)); return ' ¶ '; });
  // "2 phointe eolais ag teastáil 2 Lomphointe = 2 mharc (1 mharc + 1 mharc) Forbairt = 5 mharc …" (2014 Ordinary 3B(a)(i)): how
  // many points the answer needs, on its own line over the rows that price them, a direction.
  text = text.replace(/\b\d+\s+phointe eolais ag teastáil(?=\s+\d+\s+[A-ZÁÉÍÓÚ])/g, note => { directions.push(tidy(note)); return ' ¶ '; });
  // A note the scheme sets in brackets ("(Is leor dhá phointe eolais.)") leaves its brackets behind: they go with it.
  text = text.replace(/\(\s*¶\s*\)/g, ' ¶ ');
  // "Cuir fáthanna le do fhreagra. (Is leor dhá fháth) (7 marc)" (2012 Ordinary 3B): a bracketed note printed with no full stop
  // inside it runs to the part's price and takes its own close; its opening bracket goes with it.
  text = text.replace(/\(\s*¶(?=\s*\(\s*\d+\s*m?h?arc\s*\))/g, ' ¶ ');
  // A note that closes a bracket the prompt opened ("(Bíodh an freagra i d’fhocail féin. Is leor 60 focal.)", Higher 6(b) in
  // 2014, 2015 and 2019) leaves the bracket's close behind: it closes the prompt, never a direction of its own.
  text = text.replace(/(\([^()¶]*?[^\s(¶])\s*¶\s*\)/g, '$1) ¶ ');
  // "Treoir: Ní mór …" whose note went to the directions leaves its heading behind: it goes with it.
  text = text.replace(/\bTreoir:\s*¶/g, ' ¶ ');
  text = text.replace(/\s+/g, ' ');
  // "Teideal an úrscéil = 1 mharc (2 mharc) Ainm an údair = 1 mharc" (2014 Ordinary 2B(a)): the subtotal printed at the right of
  // the first row's line, before the last row it totals. Where the two rows add up to it, it is read after them, as printed
  // elsewhere ("Teideal … = 1 mharc Ainm … = 1 mharc (2 mharc)").
  text = text.replace(/(=\s*(\d+)\s*m?h?arc\b)\s*\((\d+)\s*(m?h?arc)\)\s+([^=•¶()]{1,40}?=\s*(\d+)\s*m?h?arc\b)(?=\s*(?:¶|$))/g,
    (whole: string, price: string, first: string, total: string, unit: string, next: string, second: string) =>
      (Number(first) + Number(second) === Number(total) ? `${price} ${next} (${total} ${unit})` : whole));

  // One pass over the sub-question markers: each segment is a prompt, then its openers and priced phrases in print order.
  const cuts = [0, ...[...text.matchAll(SUB)].map(match => match.index!)];
  // Segments keep the ¶ boundaries a removed note leaves; tidy() drops them only from the rows and prompts cut out.
  const segments = cuts.map((start, index) => text.slice(start, cuts[index + 1] ?? text.length)).map(segment => segment.replace(/\s+/g, ' ').trim()).filter(segment => segment.replace(/¶/g, '').trim());
  debug?.push(`TEXT ${text}`, ...segments.map(segment => `SEG ${segment}`));

  const openerTariffs = [...text.matchAll(OPENER)].map(match => Number(match[1] ?? match[2] ?? match[5]));
  const parts: Draft[] = [];
  let open: Draft | undefined;
  let loose: IrishAnswerRow[] = [];
  let loosePrompt: string | undefined;
  let looseSamples: string[] = [];
  const closeLoose = (tariff: number, prompt: string | undefined): boolean => {
    const sum = loose.reduce((acc, row) => acc + row.marks, 0);
    if (loose.length === 0 || sum !== tariff) return false;
    // The sample list printed under rows that close against the criterion ("Ábhair imní: Alt 2 An Ghaeilge …", 2014 Higher B
    // 6(b)) stays with them (coordinator ruling 2, batch 6), unless one of its items welds in a printed heading ("…
    // Níorbh fhiú Bliain Eorpach na hÓige a bheith ann Pointí eolais féideartha", 2023 Higher B 6(b)): then none does.
    parts.push({ prompt, tariff, rows: loose, samples: looseSamples.some(sample => SAMPLES.test(sample)) ? [] : looseSamples });
    loose = [];
    looseSamples = [];
    return true;
  };
  for (const [segmentIndex, segment] of segments.entries()) {
    let body = segment;
    const samples: string[] = [];
    // "… le samplaí mura bhfuil tuairim luaite faoin eagraíocht." (2015 Higher A 6(b)): the word inside a sentence, not a list's
    // heading; what follows it is never a sample list for rows that close against the criterion.
    let samplesInSentence = false;
    // A sample list runs to the end of the segment, unless a priced phrase follows it ("An mothúchán is láidre = 1 mharc
    // Samplaí: Brón, … bród… Dhá shampla = 4 mharc + 4 mharc Freagraí Samplacha: …", 2016 Ordinary 3A(b)(iii)): then the list
    // ends where the phrase begins, and the phrase and what follows it are read on.
    for (let sampleMark = SAMPLES.exec(body); sampleMark; sampleMark = SAMPLES.exec(body)) {
      if (!samples.length && /\ble\s$/.test(body.slice(0, sampleMark.index))) samplesInSentence = true;
      const after = body.slice(sampleMark.index + sampleMark[0].length);
      const resume = SAMPLES_RESUME.exec(after);
      if (!resume) {
        samples.push(...after.split(/[•¶]/).map(tidy).filter(Boolean));
        body = body.slice(0, sampleMark.index);
        break;
      }
      samples.push(...after.slice(0, resume.index + 1).split(/[•¶]/).map(tidy).filter(Boolean));
      body = `${body.slice(0, sampleMark.index)} ${after.slice(resume.index + resume[0].length)}`;
    }
    const tokens: Token[] = [];
    for (const match of body.matchAll(OPENER)) {
      const first = Number(match[1] ?? match[2] ?? match[5]);
      const more = ((match[2] !== undefined ? match[4] : match[6]) ?? '').match(/\d+/g)?.map(Number) ?? [];
      const ladder = match[3] ? cumulative(match[3].match(/\d+/g)!.map(Number)).slice(1) : undefined;
      tokens.push({ kind: 'open', tariff: first + more.reduce((acc, value) => acc + value, 0), ladder, at: match.index!, end: match.index! + match[0].length });
    }
    for (const match of body.matchAll(PRICED)) {
      // A phrase never runs back over an opener: it starts after the last opener it would cross.
      const crossed = tokens.filter(token => token.kind === 'open' && match.index! < token.end && match.index! + match[1].length > token.at);
      const phraseStart = crossed.length ? Math.max(...crossed.map(token => token.end)) : match.index!;
      if (phraseStart >= match.index! + match[1].length) continue; // the price belongs to the opener itself
      // The phrase is the last clause before its price; what was printed before it is a direction.
      const raw = body.slice(phraseStart, match.index! + match[1].length);
      // The alternatives are disjoint (a "(" is read by exactly one), so the scan is linear in the clause.
      // A clause may open with its count ("… sa dán. 2 Íomhá / 2 phictiúr a lua = 2 mharc", 2014 Ordinary 3B(a)(ii)).
      const boundary = raw.search(/[.:;!?)]\s+(?=[A-ZÁÉÍÓÚ(]|\d+\s+[A-ZÁÉÍÓÚa-záéíóú])(?:[^.:;!?(]|\([^)]*\)|\((?![^)]*\)))*$/);
      const clause = boundary >= 0 ? raw.slice(boundary).replace(/^[.:;!?)]\s+/, '') : raw;
      if (clause.length < raw.length) directions.push(stripMarker(raw.slice(0, raw.length - clause.length)));
      let phrase = stripMarker(clause);
      // A count the phrase opens with is its own ("2 shampla = 8 marc (4 mharc + 4 mharc)", 2014 Ordinary 3B); other leading
      // marks are not.
      if (!/^\d+\s+[A-Za-zÁÉÍÓÚáéíóú]/.test(phrase)) phrase = phrase.replace(/^[^A-Za-zÁÉÍÓÚáéíóú]+/, '');
      if (!phrase || /^\d+\s*m?h?arc$/i.test(phrase)) continue;
      const first = Number(match[2]);
      const more = (match[3].match(/\d+/g) ?? []).map(Number);
      const marks = first + more.reduce((acc, value) => acc + value, 0);
      const row: IrishAnswerRow = { id: '', text: phrase, marks };
      if (more.length) row.steps = cumulative([first, ...more]);
      tokens.push({ kind: 'row', ...row, at: phraseStart + (raw.length - clause.length), end: match.index! + match[0].length });
    }
    // "5 phointe eolais agus 5 mharc ar gach pointe eolais" with nothing priced before it (2019 Ordinary 2A(b) An Lasair Choille,
    // whose key opens on the title alone, with no "(25 marc)"): the points' own words are the criterion's row, at the total
    // they add to; what precedes them is the prompt. stepPrintedScales steps it at the totals the printed points make.
    const eachPoint = /(\d+)\s*phointe eolais agus (\d+)\s*m?h?arc ar gach pointe eolais/i.exec(body);
    if (eachPoint && tokens.length === 0 && !parts.length && !loose.length && Number(eachPoint[1]) * Number(eachPoint[2]) === source.totalMarks) {
      tokens.push({ kind: 'row', text: tidy(eachPoint[0]), marks: source.totalMarks, at: eachPoint.index, end: eachPoint.index + eachPoint[0].length });
    } else if (eachPoint && tokens.length === 0 && !parts.length && !loose.length && Number(eachPoint[1]) > 1 && Number(eachPoint[2]) === source.totalMarks) {
      // The same rule on a criterion worth one point (2014 Ordinary 2A(a) Hurlamaboc prints five points to cover and prices the
      // summary "5 phointe eolais agus 5 mharc ar gach pointe eolais"; each printed point is a criterion at 5): the rule's price
      // of one point is the row, stepped at its printed split where one is printed; the point's own words before it are the prompt.
      const one = /(\d+)\s*m?h?arc ar gach pointe eolais/i.exec(eachPoint[0])!;
      tokens.push({ kind: 'row', text: tidy(one[0]), marks: source.totalMarks, at: eachPoint.index, end: eachPoint.index + eachPoint[0].length });
    }
    // "(2 phointe eolais ar 4 mharc an ceann)" with nothing else priced (2014 Ordinary 3A(a)(ii)): the points the answer needs at
    // their own price, where they add up to the criterion's marks: one row in the scheme's words, one step a point ([0, 4, 8]).
    const bracketPoints = /\((\d+)\s*phointe eolais ar (\d+)\s*m?h?arc an ceann\)/i.exec(body);
    if (bracketPoints && tokens.length === 0 && !parts.length && !loose.length && Number(bracketPoints[1]) > 1
      && Number(bracketPoints[1]) * Number(bracketPoints[2]) === source.totalMarks) {
      tokens.push({ kind: 'row', text: tidy(bracketPoints[0].slice(1, -1)), marks: source.totalMarks,
        steps: cumulative(Array(Number(bracketPoints[1])).fill(Number(bracketPoints[2]))), at: bracketPoints.index, end: bracketPoints.index + bracketPoints[0].length });
    }
    // "Na heachtraí is mó a tharlaíonn don duine sin = 22 marc 5 phointe eolais ag teastáil (5 mharc an ceann ar an gcéad dhá
    // phointe eolais + 4 mharc an ceann ar na trí phointe eolais eile)" (Ordinary 2B, 2018-2026): the priced line names what
    // the points are about and the ladder printed straight after its price prices them. The ladder's own words are the row,
    // in the ladder's steps ([0, 5, 10, 14, 18, 22]), as where the scheme prints the ladder alone (2020 2B(b)); the line is
    // the part's lead where nothing is printed before it, and otherwise a note, as printed with its price. Only where the
    // ladder follows the line's price directly and adds up to exactly that price.
    const leadLadder = LADDER.exec(body);
    const ladderedRow = leadLadder && tokens.find((token): token is Extract<Token, { kind: 'row' }> => token.kind === 'row'
      && !token.steps && token.end <= leadLadder.index && body.slice(token.end, leadLadder.index).trim() === '');
    if (leadLadder && ladderedRow) {
      const firstCount = WORDS[leadLadder[3].toLowerCase()] ?? Number(leadLadder[3]);
      const values = [...Array(firstCount).fill(Number(leadLadder[2])),
        ...Array(Math.max(0, Number(leadLadder[1]) - firstCount)).fill(leadLadder[4] ? Number(leadLadder[4]) : Number(leadLadder[2]))];
      if (values.reduce((acc, value) => acc + value, 0) === ladderedRow.marks) {
        const first = tokens.every(token => token === ladderedRow || token.at > ladderedRow.at);
        if (!first) directions.push(tidy(body.slice(ladderedRow.at, ladderedRow.end)));
        tokens.splice(tokens.indexOf(ladderedRow), 1, { kind: 'row', text: tidy(leadLadder[0].slice(0, leadLadder[0].indexOf('('))),
          marks: ladderedRow.marks, steps: cumulative(values), at: first ? leadLadder.index : ladderedRow.at, end: leadLadder.index + leadLadder[0].length });
      }
    }
    // "4 phointe eolais ag teastáil (5 mharc an ceann) = 20 marc" (2017 Ordinary 2B(b)): the price of each point, printed with
    // the row's price. The row keeps its printed count and steps one point at a time ([0, 5, 10, 15, 20]), only where the
    // points add up to the row's marks exactly.
    // "Lomphointe + Forbairt= 2 phointe ar 4 mharc an ceann = 8 marc" (2013 Ordinary 3B(b)(i)): a row whose own words print the
    // price of each of its points steps one point at a time ([0, 4, 8]), only where the points add up to the row's marks.
    for (const token of tokens) {
      const perPoint = token.kind === 'row' && !token.steps ? /(\d+)\s*phointe ar (\d+)\s*m?h?arc an ceann$/i.exec(token.text) : null;
      if (token.kind === 'row' && perPoint && Number(perPoint[1]) > 1 && Number(perPoint[1]) * Number(perPoint[2]) === token.marks) {
        token.steps = cumulative(Array(Number(perPoint[1])).fill(Number(perPoint[2])));
      }
    }
    const eachPrice = /(\d+)\s*phointe eolais ag teastáil\s*\(\s*(\d+)\s*m?h?arc an ceann\s*\)(?=\s*=\s*\d+\s*m?h?arc\b)/i.exec(body);
    if (eachPrice) {
      const counted = tokens.find((token): token is Extract<Token, { kind: 'row' }> => token.kind === 'row' && !token.steps
        && token.at <= eachPrice.index + eachPrice[0].length && token.end > eachPrice.index);
      const [count, each] = [Number(eachPrice[1]), Number(eachPrice[2])];
      if (counted && count > 1 && count * each === counted.marks) {
        counted.text = tidy(eachPrice[0]);
        counted.steps = cumulative(Array(count).fill(each));
      }
    }
    // "Príomhthéama (2) = Forbairt (23) =" (2015 Higher 2B, the play): the scheme's score boxes, each part of the answer at its
    // printed price, where nothing else in the text is priced. The boxes that add up to the criterion are its rows ("Tréithe
    // agus Léiriú (25) = Gaeilge (5) =", the film: the Gaeilge box is the other criterion's). The examiner's "an marc ar eolas
    // as 25 marc" judges the criterion out of its marks, every mark from 0: its judged row, the largest, steps in single marks.
    if (tokens.length === 0 && !parts.length && !loose.length && !bands.length) {
      const boxes = [...body.matchAll(/([A-ZÁÉÍÓÚ][^()=¶.]*?)\s*\((\d+)\)\s*=(?=\s|$)/g)];
      const taken: RegExpMatchArray[] = [];
      let boxed = 0;
      for (const box of boxes) {
        if (boxed >= source.totalMarks) break;
        taken.push(box);
        boxed += Number(box[2]);
      }
      const judgedOutOf = /an t-eolas a mharcáil as (\d+) marc|an marc ar eolas as (\d+) marc/.exec(source.guidance.join(' '));
      if (taken.length && boxed === source.totalMarks) {
        const largest = Math.max(...taken.map(box => Number(box[2])));
        const judged = Number(judgedOutOf?.[1] ?? judgedOutOf?.[2]) === source.totalMarks;
        for (const box of taken) {
          const marks = Number(box[2]);
          tokens.push({ kind: 'row', text: tidy(box[1]), marks, ...(judged && marks === largest && marks > 1 ? { steps: range(marks) } : {}),
            at: box.index!, end: box.index! + box[0].length });
        }
      }
    }
    // Where nothing else in the text is priced and no band table prices it, each thing marked "out of N" is a judged row at N
    // in single marks (MARK_AS).
    if (tokens.length === 0 && !parts.length && !loose.length && !bands.length) {
      for (const match of body.matchAll(MARK_AS)) {
        // "an t-eolas a mharcáil as 35 marc" (Ceist 4A–E, 2016 and 2017) is the whole criterion's price: the Ceist 4 rule
        // below makes the criterion's own printed words its judged row, as 2017 and 2018 4A–E have.
        if (/^an t-eolas$/i.test(match[1].trim())) continue;
        const at = match.index! + match[0].indexOf(match[1]);
        tokens.push({ kind: 'row', text: tidy(match[1]), marks: Number(match[2]), steps: range(Number(match[2])), at, end: match.index! + match[0].length });
      }
    }
    // "(6 mharc) Pointe amháin eolais a mharcáil as 5 mharc" (2013 Higher 3A(ii)): the paper's tariff for the part, then the one
    // point the scheme marks out of the criterion's own marks. It is a judged row at those marks in single marks, as MARK_AS reads
    // "an … a mharcáil as N" where nothing else is priced.
    const pointAs = /\bPointe amháin eolais a mharcáil as (\d+)\s*m?h?arc\b/.exec(body);
    if (pointAs && Number(pointAs[1]) === source.totalMarks && !tokens.some(token => token.kind === 'row')) {
      tokens.push({ kind: 'row', text: 'Pointe amháin eolais', marks: source.totalMarks, steps: range(source.totalMarks),
        at: pointAs.index, end: pointAs.index + pointAs[0].length });
    }
    // The 2015 point shares with nothing else priced: the priced sentence is the criterion's row, in its points' steps
    // ([0, 7, 14, 21, 23, 25]), only where the points add up to the criterion exactly.
    const shares = POINT_SHARES.exec(body);
    const shared = shares && !tokens.some(token => token.kind === 'row') ? pointShares(shares) : undefined;
    if (shares && shared && shared.reduce((acc, value) => acc + value, 0) === source.totalMarks) {
      tokens.push({ kind: 'row', text: tidy(shares[0].replace(/\.$/, '')), marks: source.totalMarks, steps: cumulative(shared),
        at: shares.index, end: shares.index + shares[0].length });
    }
    tokens.sort((a, b) => a.at - b.at);
    // "(ii) Roghnaigh dhá íomhá (phictiúr) … (8 marc) Íomhá / pictiúr a lua = 1 mharc Forbairt = 3 mharc 2 íomhá / phictiúr ar 4
    // mharc an ceann" (2013 Ordinary 3B(a)(ii)): the rows price one of the things the question asks for, and the line after them
    // how many it asks for at that price. Each row counts once per thing ([0, 1, 2], [0, 3, 6]), only where the rows add up to
    // the price of one and the things to the part's tariff; the count line is a direction.
    const things = /(?<=\bm?h?arc\s)(\d+)\s+[^=•¶()]{1,40}?\s+ar\s+(\d+)\s*m?h?arc an ceann\s*$/i.exec(body);
    const thingRows = tokens.filter((token): token is Extract<Token, { kind: 'row' }> => token.kind === 'row');
    const thingOpen = tokens.find(token => token.kind === 'open');
    if (things && thingOpen && thingRows.length > 1 && thingRows.every(row => !row.steps && row.end <= things.index)
      && thingRows.reduce((acc, row) => acc + row.marks, 0) === Number(things[2]) && Number(things[1]) * Number(things[2]) === thingOpen.tariff) {
      const count = Number(things[1]);
      for (const row of thingRows) { row.steps = cumulative(Array(count).fill(row.marks)); row.marks *= count; }
      directions.push(tidy(things[0]));
    }
    // "(ii) Inis i d’fhocail féin, cén sórt saoil a bhí ag an spailpín? (Is leor dhá phointe eolais.) = (4 mharc +4 mharc)" (2013
    // Ordinary 3A(b)(ii)): a split printed under the question with no words of its own, the note before it read as a direction.
    // The sub-question's own words are the row, in the split's steps ([0, 4, 8]), only where nothing else prices it and the
    // split adds up to the criterion.
    const bareSplit = /^(.*[?.])\s*¶\s*=\s*(\d+)\s*m?h?arc\s*\+\s*(\d+)\s*m?h?arc\s*$/.exec(body);
    if (bareSplit && tokens.length === 0 && !parts.length && !loose.length && Number(bareSplit[2]) + Number(bareSplit[3]) === source.totalMarks) {
      const at = body.lastIndexOf('=');
      tokens.push({ kind: 'row', text: stripMarker(bareSplit[1]), marks: source.totalMarks, steps: cumulative([Number(bareSplit[2]), Number(bareSplit[3])]),
        at, end: body.length });
    }
    // "Aidhm 1 + Forbairt = 6 mharc   Aidhm a lua = 2 mharc + Forbairt = 4 mharc" (2016 Higher A 6(b)): a priced line followed
    // straight away by a printed split ("… = 2 mharc + … = 4 mharc") that adds up to exactly its own price is the split's
    // heading, not one more answer: the split's rows stay and the heading goes to the directions.
    for (let index = 0; index < tokens.length; index += 1) {
      const head = tokens[index];
      const joined = (token: Token) => /^\s*\+/.test(body.slice(token.at, token.end));
      if (head.kind !== 'row' || head.steps || tokens[index + 1]?.kind !== 'row' || joined(tokens[index + 1])) continue;
      let sum = 0;
      let k = index + 1;
      while (k < tokens.length && tokens[k].kind === 'row' && sum < head.marks && (k === index + 1 || joined(tokens[k]))) {
        sum += (tokens[k] as { marks: number }).marks;
        k += 1;
      }
      if (k - index > 2 && sum === head.marks) {
        directions.push(tidy(body.slice(head.at, head.end)));
        tokens.splice(index, 1);
      }
    }
    debug?.push(...tokens.map(token => token.kind === 'open' ? `  OPEN ${token.tariff} ladder=${token.ladder ?? ''} @${token.at}` : `  ROW ${token.marks} steps=${token.steps ?? ''} "${token.text.slice(0, 60)}" @${token.at}`));
    // The prompt is the sub-question as printed, up to the first note the scheme sets inside it
    // ("(Is leor 60 focal.)"); what the scheme prints after the note and before the tariff is a direction.
    const promptPieces = (tokens.length ? body.slice(0, tokens[0].at) : body).split('¶').map(stripMarker).filter(Boolean);
    const promptText = promptPieces[0] ?? '';
    directions.push(...promptPieces.slice(1).filter(piece => piece !== promptText));
    // "5 phointe eolais ag teastáil (…)" after a row prices that row in steps.
    const ladderText = LADDER.exec(body);
    // "5 phointe eolais ag teastáil (5 mharc … + 4 mharc …)" with no "Na heachtraí … = 22 marc" printed before it
    // (2020 Ordinary 2B(b)): the ladder's own words are the criterion's row, at the total its points add to, in its steps.
    const ladderWords = /(\d+)\s*phointe eolais ag teastáil\s*\(\s*(\d+)\s*m?h?arc an ceann ar an g?c?[ée]ad\s+(\S+)\s+phointe eolais(?:\s*\+\s*(\d+)\s*m?h?arc an ceann ar (?:an|na)\s+(\S+)\s+phointe eolais eile)?\.?\s*\)/i.exec(body);
    if (ladderWords && !tokens.some(token => token.kind === 'row')) {
      const firstCount = WORDS[ladderWords[3].toLowerCase()] ?? Number(ladderWords[3]);
      const values = [...Array(firstCount).fill(Number(ladderWords[2])), ...Array(Math.max(0, Number(ladderWords[1]) - firstCount)).fill(ladderWords[4] ? Number(ladderWords[4]) : Number(ladderWords[2]))];
      if (values.reduce((acc, value) => acc + value, 0) === source.totalMarks) {
        tokens.push({ kind: 'row', text: tidy(ladderWords[0].slice(0, ladderWords[0].indexOf('('))), marks: source.totalMarks, steps: cumulative(values),
          at: ladderWords.index, end: ladderWords.index + ladderWords[0].length });
        tokens.sort((x, y) => x.at - y.at);
      }
    }
    if (tokens.length === 0) {
      if (!open && !loose.length) loosePrompt = loosePrompt ?? promptText;
      else directions.push(promptText);
      if (samples.length && open) open.samples.push(...samples);
      continue;
    }
    let segmentPrompt: string | undefined = promptText || undefined;
    // A sub-question whose rows come with no tariff of their own ("(b) … C (2) = 2 mharc Pointe eolais 1 = … = 5 mharc"):
    // its rows are not the previous part's; they close against the criterion's remainder.
    if (tokens[0].kind === 'row' && segmentIndex > 0 && SUB.test(segment.slice(0, 12) + ' ')) { open = undefined; loosePrompt = segmentPrompt; }
    SUB.lastIndex = 0;
    const skipped = new Set<number>();
    for (const [index, token] of tokens.entries()) {
      if (token.kind === 'open') {
        // "(25 marc)" printed on the option's title line, read on a criterion worth less (a reviewed card
        // prices "An phríomhphearsa a ainmniú = 1 mharc" apart from its account): the card's total, not a part.
        if (source.cardTotal && token.tariff === source.cardTotal && source.totalMarks < source.cardTotal) continue;
        // "(23 marc)" after "An cineál saoil … = 22 marc": the printed question's tariff, which also covers a sibling
        // criterion's mark (An phríomhphearsa a ainmniú = 1 mharc). No part of this criterion can be worth more than it.
        if (token.tariff > source.totalMarks) continue;
        const opensSubQuestion = index === 0 && Boolean(promptText);
        // "(25 marc)" on the option's title line, with the sub-questions' own tariffs after it: the criterion, not a part.
        const subTariffs = openerTariffs.filter(tariff => tariff !== source.totalMarks);
        if (token.tariff === source.totalMarks && subTariffs.length && subTariffs.reduce((acc, tariff) => acc + tariff, 0) === source.totalMarks
          && !tokens.slice(index + 1).some(t => t.kind === 'row' && t.at < (tokens.slice(index + 1).find(n => n.kind === 'open')?.at ?? Infinity))) continue;
        // "(23 marc) (2 mharc)" printed together before the rows: the tariff summary, not two parts.
        const run: number[] = [token.tariff];
        for (let k = index + 1; k < tokens.length && tokens[k].kind === 'open' && !tidy(body.slice(tokens[k - 1].end, tokens[k].at)); k += 1) run.push((tokens[k] as { tariff: number }).tariff);
        // On a reviewed card the summary can price the whole card, the sibling criterion's tariff included, when the
        // criterion's own priced rows follow it ("(23 marc) (2 mharc) Príomhimeachtaí (príomhrudaí) = 23 marc").
        const runTotal = run.reduce((acc, value) => acc + value, 0);
        const cardSummary = source.cardTotal !== undefined && runTotal === source.cardTotal && run.includes(source.totalMarks)
          && tokens[index + run.length]?.kind === 'row';
        if (run.length > 1 && (runTotal === source.totalMarks || cardSummary)) { skipped.add(index); for (let k = 1; k < run.length; k += 1) skipped.add(index + k); continue; }
        if (skipped.has(index)) continue;
        // A tariff printed after the rows it totals closes them; printed before, it opens a part.
        if (loose.length && closeLoose(token.tariff, open ? undefined : loosePrompt ?? segmentPrompt)) { loosePrompt = undefined; segmentPrompt = undefined; continue; }
        // "Eolas = 25 marc" printed again for the option's alternative text (scannán nó dráma): one judgement, not two.
        if (token.tariff === source.totalMarks && parts.some(part => part.tariff === source.totalMarks)) { open = parts.find(part => part.tariff === source.totalMarks); continue; }
        // "Catagóir An plé (23 marc)" after "An príomhthéama = 2 mharc An plé … = 23 marc": the band table restating the
        // last loose row's tariff, not a new part (the rows still close against the criterion's remainder).
        if (!open && loose.length > 1 && !opensSubQuestion && loose[loose.length - 1].marks === token.tariff) continue;
        if (open && open.rows.length === 0 && open.tariff === token.tariff && !opensSubQuestion) continue; // "(23 marc)" repeating the opener
        // "(2 mharc)" straight after "Teideal = 1 mharc Ainm = 1 mharc": the subtotal of the last rows placed, not a
        // new part. A tariff with a prompt before it opens a sub-question even when it equals the last rows' sum.
        if (open && open.rows.length && !open.ladder && !opensSubQuestion) {
          let tail = 0;
          let subtotal = false;
          for (let k = open.rows.length - 1; k >= 0; k -= 1) { tail += open.rows[k].marks; if (tail === token.tariff) { subtotal = true; break; } if (tail > token.tariff) break; }
          if (subtotal) continue;
        }
        // "Eolas = 5 mharc Tuairim = 1 mharc Eolas = 4 mharc" (2020 Higher 3A(ii), 3B(ii)): an "Eolas =" that completes the
        // open part's rows is that part's last row, the scheme's word for the point, not a new part.
        if (open && open.rows.length && !open.ladder && !opensSubQuestion && /^Eolas\s*=/.test(body.slice(token.at, token.end))
          && open.rows.reduce((acc, row) => acc + row.marks, 0) + token.tariff === open.tariff) {
          open.rows.push({ id: '', text: tidy(body.slice(token.at, token.end).replace(/\s*=[\s\S]*$/, '')), marks: token.tariff });
          continue;
        }
        const after = tokens.slice(index + 1).find(next => next.kind === 'row' || next.kind === 'open');
        open = { prompt: index === 0 ? segmentPrompt : undefined, tariff: token.tariff, ladder: token.ladder, rows: [], samples: [],
          unpriced: token.ladder ? tidy(body.slice(token.end, after ? after.at : body.length)) : undefined };
        segmentPrompt = undefined;
        parts.push(open);
        continue;
      }
      const row: IrishAnswerRow = { id: '', text: token.text, marks: token.marks, ...(token.steps ? { steps: token.steps } : {}) };
      // "Dhá thréith = 6 mharc + 6 mharc" over "Tréith 1 a lua = 2 … sampla = 4 … Tréith 2 …": the subtotal of what
      // follows, not a row; so is a count-word line worth exactly the rows after it.
      const rest = tokens.slice(index + 1).filter(t => t.kind === 'row') as Array<Token & { kind: 'row' }>;
      const restSum = (n: number) => rest.slice(0, n).reduce((acc, t) => acc + t.marks, 0);
      const subtotalOfRest = rest.length > 1 && [2, 3, 4, 5, 6].some(n => n <= rest.length && restSum(n) === token.marks) && /^(?:Dhá|Trí|Ceithre|Cúig|An dá|Na)(?=\s)/i.test(token.text);
      if (subtotalOfRest) { debug?.push(`  SKIP subtotal-of-rest ${token.marks} "${token.text.slice(0, 40)}"`); continue; }
      // "Ainm an fhile = Caitlín Maude = 1 mharc" after "Ainm an fhile = 1 mharc": the answer printed for a row already
      // placed, kept on that row. An exact repeat is dropped only where it would overfill the part.
      const placedRows = open?.rows ?? loose;
      // The 2020 Higher scheme prints that answer as "Ainm an file = Nuala Ní Dhomhnaill = 1 mharc" (no lenition after
      // "Ainm an fhile = 1 mharc"): the same row, read past the séimhiú. The row keeps the spelling it was placed with.
      const answered = placedRows.find(placed => placed.marks === token.marks && answerOf(placed.text, token.text) !== undefined);
      if (answered) { answered.text = `${answered.text}: ${answerOf(answered.text, token.text)}`; continue; }
      // "Saol agus saothar an fhile = 2 mharc + 2 mharc + 2 mharc = 6 mharc" after "Saol an fhile agus saothar an fhile = 6 mharc"
      // (2017 Higher 3A and 3B (iii)): the split of a row already placed, printed again after the note on how it divides. It
      // gives that row its steps; it is not a second row. Only where a second row at that price would overfill the part.
      const restated = token.steps && open ? placedRows.find(placed => !placed.steps && placed.marks === token.marks) : undefined;
      if (restated && open && placedRows.reduce((acc, placed) => acc + placed.marks, 0) + token.marks > open.tariff) {
        restated.steps = token.steps;
        debug?.push(`  STEPS restated ${token.marks} onto "${restated.text.slice(0, 40)}"`);
        continue;
      }
      if (open && placedRows.some(placed => placed.text === token.text && placed.marks === token.marks) && placedRows.reduce((acc, placed) => acc + placed.marks, 0) + token.marks > open.tariff) continue;
      if (open) {
        if (open.rows.length === 0 && token.marks === open.tariff && rest.length > 1) { debug?.push(`  SKIP subtotal-of-part ${token.marks}`); continue; }
        if (ladderText && open.rows.length === 0 && token.marks === open.tariff - (tokens.filter(t => t.kind === 'row' && t !== token).reduce((acc, t) => acc + (t as { marks: number }).marks, 0))) {
          const count = Number(ladderText[1]);
          const firstMarks = Number(ladderText[2]);
          const firstCount = WORDS[ladderText[3].toLowerCase()] ?? Number(ladderText[3]);
          const restMarks = ladderText[4] ? Number(ladderText[4]) : firstMarks;
          const values = [...Array(firstCount).fill(firstMarks), ...Array(Math.max(0, count - firstCount)).fill(restMarks)];
          if (values.reduce((acc, value) => acc + value, 0) === token.marks) row.steps = cumulative(values);
        }
        if (!row.steps && bands.length && row.marks >= 8) row.steps = range(row.marks);
        open.rows.push(row);
      } else {
        loose.push(row);
        if (!loosePrompt && segmentPrompt) loosePrompt = segmentPrompt;
      }
    }
    if (samples.length && open) open.samples.push(...samples);
    else if (samples.length && loose.length && !samplesInSentence) looseSamples.push(...samples);
  }
  if (loose.length) {
    // Rows under no printed tariff: the criterion's own remainder, if they add up to it.
    const used = parts.reduce((acc, part) => acc + part.tariff, 0);
    // Rows left over after every part is closed, each at the price of a row already placed ("Pointe amháin eolais faoin
    // mothúchán ag tagairt do théacs an dáin = 4 mharc" after "Pointe amháin eolais = 4 mharc Eolas = 5 mharc", 2016 Higher
    // 3A(ii) and 4F(iii)): the scheme restating what that row asks for, a note under it, not one more answer.
    const placed = new Set(parts.flatMap(part => part.rows.map(row => row.marks)));
    if (source.totalMarks === used && loose.every(row => placed.has(row.marks))) {
      directions.push(...loose.map(row => row.text));
      loose = [];
    }
    if (loose.length && !closeLoose(source.totalMarks - used, loosePrompt)) return { ok: false, reason: `rows without a tariff add to ${loose.reduce((acc, row) => acc + row.marks, 0)}, ${source.totalMarks - used} is left` };
  }
  for (const band of bands) directions.push(band);
  // A lone "Eolas = 25 marc" that prices the whole criterion is kept even when the route's text starts at it (the
  // 2022 Higher prose routes are cut after the work's title): one judgement over the criterion, in steps.
  let kept = parts.filter(part => part.rows.length || part.prompt || part.ladder || (parts.length === 1 && part.tariff === source.totalMarks));
  const half = kept.length / 2;
  if (kept.length >= 2 && kept.length % 2 === 0 && kept.reduce((acc, part) => acc + part.tariff, 0) === 2 * source.totalMarks
    && kept.slice(0, half).every((part, i) => part.tariff === kept[half + i].tariff)) {
    // The option printed twice for its alternative texts (scannán nó dráma): one set of parts.
    kept = kept.slice(0, half);
  }
  parts.length = 0; parts.push(...kept);
  // A criterion whose only printed price is its band table's header (2018 Higher Ceist 4A–E and 2B print no "Eolas = 35 marc"
  // of their own; "Catagóir Eolas (35 marc) Gaeilge (5 mharc)" prices them): one judgement over the criterion, its own words
  // the row, as a sub-question priced whole with nothing under it. Only where nothing else priced it.
  // 2017 prints no band table for Ceist 4A–E either: its Ceist 4 Treoracha price them ("an t-eolas a mharcáil as 35 marc"). 2015
  // prints nothing else for 2A and 2B but the examiner's closing note ("Ní mór don Scrúdaitheoir an marc ar eolas as 25 marc …").
  // 2012 prints only the note after both prose questions: "Caithfidh an Scrúdaitheoir an marc as 25 (Ábhar) agus as 5 (Gaeilge) a
  // thaispeáint" (Higher 2A, 2B).
  const treoirPrice = /an t-eolas a mharcáil as (\d+) marc|an marc ar eolas as (\d+) marc|an marc as (\d+) \(Ábhar\)/.exec(source.guidance.join(' '));
  if (parts.length === 0 && !loose.length && loosePrompt
    && (bands.some(band => Number(/^Catagóir\s+Eolas\s*\((\d+)\s*m?h?arc\)/.exec(band)?.[1]) === source.totalMarks)
      || Number(treoirPrice?.[1] ?? treoirPrice?.[2] ?? treoirPrice?.[3]) === source.totalMarks)) {
    parts.push({ prompt: loosePrompt, tariff: source.totalMarks, rows: [], samples: [] });
  }
  if (parts.length === 0) return { ok: false, reason: 'no priced sub-question' };

  const built: IrishAnswerPart[] = [];
  let total = 0;
  for (const [index, part] of parts.entries()) {
    const sum = part.rows.reduce((acc, row) => acc + row.marks, 0);
    if (part.ladder) {
      if (part.rows.length === 0) {
        // "{3 mharc: 2 mharc + 1 mharc}" over "Sampla de X: …" answers: the unpriced samples are the rows the ladder prices.
        const answers = part.samples.length ? part.samples : (part.unpriced ?? '').split(/\s(?=Sampla\b)|\s•\s/).map(tidy).filter(Boolean);
        if (!answers.length) return { ok: false, reason: 'ladder without rows' };
        part.rows = answers.map(answer => ({ id: '', text: answer, marks: 0 }));
        part.samples = [];
      }
      if (part.ladder[part.ladder.length - 1] !== part.tariff) return { ok: false, reason: `ladder ends at ${part.ladder[part.ladder.length - 1]}, tariff is ${part.tariff}` };
    } else if (part.rows.length === 0) {
      // A sub-question priced whole with nothing under it: its own words are the row, claimed whole. A step the scheme does
      // not print is never inferred (coordinator correction, batch 6: "(2 mharc)" over sample answers is 0/2);
      // stepPrintedScales steps the row where the criterion's own guidance prints a partial or a scale for it.
      part.rows.push({ id: '', text: part.prompt ?? 'Eolas', marks: part.tariff });
    } else if (sum === 2 * part.tariff && part.rows.length % 2 === 0
      && part.rows.slice(0, part.rows.length / 2).every((row, i) => row.marks === part.rows[part.rows.length / 2 + i].marks)) {
      // The scheme prints the option's tariff twice, once per alternative text (scannán nó dráma): one set of rows.
      part.rows = part.rows.slice(0, part.rows.length / 2);
    } else if (sum !== part.tariff) {
      return { ok: false, reason: `rows add to ${sum}, sub-question is ${part.tariff}` };
    }
    total += part.tariff;
    built.push({
      id: `p${index + 1}`, ...(part.prompt ? { prompt: part.prompt } : {}), tariff: part.tariff,
      ...(part.ladder ? { ladder: part.ladder } : {}),
      rows: part.rows.map((row, rowIndex) => ({ ...row, id: `r${rowIndex + 1}` })),
      ...(part.samples.length ? { samples: part.samples } : {}),
    });
  }
  if (total !== source.totalMarks) return { ok: false, reason: `sub-questions add to ${total}, criterion is ${source.totalMarks}` };
  const seen = new Set<string>();
  return { ok: true, allocation: { parts: built, directions: directions.filter(note => note && !seen.has(note) && seen.add(note)) } };
}

/** The marks a printed band table's values cover: "6-7 … 5 … 4 … 3 … 0-2", "10, 11 … 0, 1, 2, 3". */
const bandValues = (table: string): Set<number> => {
  const values = new Set<number>();
  for (const match of table.matchAll(/(\d+)\s*[-–]\s*(\d+)|(\d+)/g)) {
    if (match[3] !== undefined) values.add(Number(match[3]));
    else for (let value = Number(match[1]); value <= Number(match[2]); value++) values.add(value);
  }
  return values;
};
const covers = (values: Set<number>, top: number) => Array.from({ length: top + 1 }, (_, value) => value).every(value => values.has(value));
const subsetSums = (terms: number[]) => [...terms.reduce((sums, term) => new Set([...sums, ...[...sums].map(sum => sum + term)]), new Set([0]))].sort((a, b) => a - b);

/** Steps a row whose marks the scheme prints a scale for, where the row is still one tick worth 0 or all of it
 *  (coordinator decision, batch 4: step only where the scheme prints a per-point price or a ladder; never infer one):
 *  - a count note, "Trí phointe eolais ag teastáil anseo: 2 mharc an ceann ar na trí phointe eolais", for the row's
 *    marks: one step per point ([0, 2, 4, 6]);
 *  - the row's own printed split, "Forbairt = 7 marc (4 mharc + 3 mharc)": the totals its parts make ([0, 3, 4, 7]),
 *    or every mark where a band table prices each part in single marks ("Dhá phointe eolais = 6 mharc = 3 mharc +
 *    3 mharc" under "Catagóir Marc as 3 Sármhaith 3 An-mhaith/Maith 2 Measartha 1 Lag/An-lag 0");
 *  - a band table headed by the row's marks whose printed values cover every mark from 0 ("Catagóir Marc as 7
 *    Sármhaith 6-7 … Lag/An-lag 0-2", "Catagóir An plé (23 marc) … 21-23 … 0-9", "Pointe eolais Marc as 6 Léiriú
 *    sármhaith 6 … Léiriú an-lag 0-1"): every mark.
 *  - a bare point and its development priced apart, "2 mharc ar lomphointe eolais agus 3 mharc ar fhorbairt (5 mharc)",
 *    "(5 mharc = 2 mharc ar lomphointe eolais agus 3 mharc ar fhorbairt.)", for a row at their sum: the totals its parts make
 *    ([0, 2, 3, 5]);
 *  - points at a printed price each, "5 phointe eolais agus 5 mharc ar gach pointe eolais", for a row at their total: every
 *    total the points can make, each point at the totals its own printed split makes where one is printed ([0, 2, 3, 4, …]),
 *    otherwise one step a point;
 *  - the examiner's judgement of the row out of its own marks, "an t-eolas a mharcáil as 35 marc", "an marc ar eolas as 25
 *    marc", "Déan measúnú ar fhiúntas an eolais/an phlé as 18 marc": every mark, where the row is the criterion's largest.
 *  A printed price is claimable at every level (coordinator, batch 5: no floor). A row with steps or under a ladder is
 *  never touched; nothing is read from outside the criterion's own guidance. Nothing else steps a row (coordinator
 *  correction, batch 6: a step the scheme does not print is never inferred). */
export const stepPrintedScales = (allocation: IrishAllocation, guidance: string[], section: string[] = []): IrishAllocation => {
  const text = guidance.join(' ').replace(/\s+/g, ' ');
  // The examiner's ready reckoner, where the scheme says it governs the answers: "Moltar do scrúdaitheoirí … úsáid a bhaint as
  // an réríomhaire (cf lch 25) agus iad ag teacht ar chinneadh faoi cad is fiú freagra" (2012 Higher, PDF 25 note 3, for the
  // answers to Ceisteanna 2-4) over "Grádú Marcála sna Ceisteanna … GRÁD 200 160 … 18 A 170 136 … D 80 64 … 8 GRÁD 17 16 … 5 …"
  // (PDF 26). Read from the card's own section (its criteria), as printed for it: a row priced at one of the table's totals,
  // its criterion's largest, steps at the marks the table prints for that total, its grades D, C, B and A, and the total
  // (coordinator, batch 7: never every mark between them); a total with no column in the table is not stepped by it.
  const sectionText = section.join(' ').replace(/\s+/g, ' ');
  const reckoner = new Map<number, number[]>();
  if (/úsáid a bhaint as an réríomhaire/.test(sectionText)) {
    for (const block of sectionText.matchAll(/GRÁD((?:\s+\d+)+)\s+A((?:\s+\d+)+)\s+B((?:\s+\d+)+)\s+C((?:\s+\d+)+)\s+D((?:\s+\d+)+)/g)) {
      const [totals, ...grades] = block.slice(1, 6).map(cells => cells.trim().split(/\s+/).map(Number));
      if (!grades.every(cells => cells.length >= totals.length)) continue;
      totals.forEach((total, column) => reckoner.set(total,
        [...new Set([0, ...grades.map(cells => cells[column]), total])].sort((a, b) => a - b)));
    }
  }
  const counts = new Map<number, number[]>();
  for (const match of text.matchAll(/(\S+)\s+phointe eolais ag teastáil(?: anseo)?:?\s*(\d+)\s*m?h?arc an ceann ar (?:an|na)\s+(\S+)\s+phointe eolais/gi)) {
    const count = WORDS[match[1].toLowerCase()] ?? Number(match[1]);
    const each = Number(match[2]);
    if (count > 1 && each > 0 && (WORDS[match[3].toLowerCase()] ?? Number(match[3])) === count) counts.set(count * each, cumulative(Array(count).fill(each)));
  }
  const bands = new Map<number, Set<number>>();
  const headed = /(?:Catagóir\s+Marc as (\d+)(?!\s+Marc as)|Catagóir\s+(?:An plé|Plé|Eolas|Cur síos)\s*\((\d+)\s*m?h?arc\)|Pointe eolais Marc as (\d+)|Catagóir\s+Plé\s+(?=Marcanna))([\s\S]*?(?:Lag\/\s?An-lag|Léiriú an-lag)[^0-9]*?(?:\d+\s*[-–]\s*\d+|\d+(?:\s*,\s*\d+)*))/g;
  for (const match of text.matchAll(headed)) {
    const values = bandValues(match[4].replace(/\([^)]*\)/g, ' '));
    // "Catagóir Plé Marcanna …" (2026) prints no price in its header: its top printed value is the price it scales.
    const top = Number(match[1] ?? match[2] ?? match[3] ?? Math.max(...values));
    if (covers(values, top) && Math.max(...values) === top) bands.set(top, values);
  }
  // A table with one column per point, "Catagóir Marc as 5 Marc as 4 Sármhaith 5 4 An-mhaith 4 3 … Lag/An-lag 0-1 0"
  // (Higher 4F(iii), Pointe Eolais 1 and 2): each band's cells go to the columns in print order, and each column scales the
  // row priced at its own header.
  for (const match of text.matchAll(/Catagóir((?:\s+Marc as \d+){2,})\s+([\s\S]*?Lag\/\s?An-lag\s+(?:(?:\d+\s*[-–]\s*\d+|\d+(?:\s*,\s*\d+)*)\s*){2,})/g)) {
    const tops = [...match[1].matchAll(/\d+/g)].map(top => Number(top[0]));
    const cells = [...match[2].matchAll(/\d+\s*[-–]\s*\d+|\d+(?:\s*,\s*\d+)*/g)].map(cell => cell[0]);
    if (cells.length % tops.length !== 0) continue;
    tops.forEach((top, column) => {
      const values = bandValues(cells.filter((_, index) => index % tops.length === column).join(' '));
      if (covers(values, top) && Math.max(...values) === top) bands.set(top, values);
    });
  }
  const splitOf = (row: IrishAnswerRow): number[] | undefined => {
    const at = text.indexOf(row.text.slice(0, 30));
    if (at < 0) return undefined;
    const price = new RegExp(String.raw`^[^=]{0,200}?=\s*${row.marks}\s*m?h?arc\s*(?:=\s*|\(\s*)(\d+\s*m?h?arc(?:\s*\+\s*\d+\s*m?h?arc)+)`).exec(text.slice(at));
    return price ? price[1].match(/\d+/g)!.map(Number) : undefined;
  };
  // "Dhá phointe eolais = 4 mharc + 4 mharc" (2025 Higher 4F(iii)): the split printed as the row's own price.
  const pointsOf = (row: IrishAnswerRow): number[] | undefined => {
    const price = new RegExp(String.raw`(?:^|\s)${row.text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\s*=\s*(\d+\s*m?h?arc(?:\s*\+\s*\d+\s*m?h?arc)+)`).exec(text);
    return price ? price[1].match(/\d+/g)!.map(Number) : splitOf(row);
  };
  const pointSplits = new Map<number, number[]>();
  for (const match of text.matchAll(/(\d+)\s*m?h?arc ar lomphointe eolais\s*(?:agus|\+)\s*(\d+)\s*m?h?arc ar fhorbairt/gi)) {
    pointSplits.set(Number(match[1]) + Number(match[2]), [Number(match[1]), Number(match[2])]);
  }
  const pointPrices = new Map<number, number[]>();
  for (const match of text.matchAll(/(\d+)\s*phointe eolais agus (\d+)\s*m?h?arc ar gach pointe eolais/gi)) {
    const [count, each] = [Number(match[1]), Number(match[2])];
    const one = pointSplits.has(each) ? subsetSums(pointSplits.get(each)!) : [0, each];
    let totals = [0];
    for (let point = 0; point < count; point++) totals = [...new Set(totals.flatMap(total => one.map(value => total + value)))];
    if (count > 1) pointPrices.set(count * each, totals.sort((a, b) => a - b));
  }
  const judged = new Set([...text.matchAll(/(?:an t-eolas a mharcáil|an marc ar eolas|marcáil an t-eolas|marcáiltear an t-eolas|an phlé sa fhreagra|fhiúntas an eolais\/an phlé|Blocmharcáil) as (\d+)\s*m?h?arc\b/gi)]
    .map(match => Number(match[1])));
  const largest = Math.max(0, ...allocation.parts.flatMap(part => part.rows.map(row => row.marks)));
  const stepsFor = (row: IrishAnswerRow): number[] | undefined => {
    const counted = counts.get(row.marks);
    if (counted) return counted;
    const pointSplit = pointSplits.get(row.marks);
    if (pointSplit) return subsetSums(pointSplit);
    const pointPrice = pointPrices.get(row.marks);
    if (pointPrice) return pointPrice;
    const split = splitOf(row);
    if (split && split.reduce((a, b) => a + b, 0) === row.marks) {
      return split.every(part => bands.has(part)) ? range(row.marks) : subsetSums(split);
    }
    if (bands.has(row.marks)) return range(row.marks);
    if (reckoner.has(row.marks) && row.marks === largest) return reckoner.get(row.marks);
    return judged.has(row.marks) && row.marks === largest ? range(row.marks) : undefined;
  };
  return {
    ...allocation,
    parts: allocation.parts.map(part => (part.ladder ? part : {
      ...part,
      rows: part.rows.map(row => {
        // A row the scheme splits into points ("Dhá phointe eolais = 4 mharc + 4 mharc") steps a point at a time; where a band
        // table prices each of those points in single marks ("Catagóir Marc as 4 Sármhaith 4 … Lag/An-lag 0", 2025 Higher
        // 4F(iii)), it steps every mark.
        const split = row.steps && bands.size ? pointsOf(row) : undefined;
        if (row.steps && split && split.reduce((a, b) => a + b, 0) === row.marks && split.every(value => bands.has(value))
          && row.steps.join() === cumulative(split).join()) return { ...row, steps: range(row.marks) };
        if (row.steps || row.marks < 2) return row;
        const steps = stepsFor(row);
        return steps && steps.length > 2 ? { ...row, steps } : row;
      }),
    })),
  };
};

/** A note or prompt cut inside a bracket keeps the bracket the scheme prints round it, and never a half of one: a direction
 *  missing the "(" the scheme prints straight before it ("Ní mór Ceist 6 (b) a fhreagairt … den scrúdpháipéar)", "5 mharc = 2
 *  mharc ar lomphointe eolais agus 3 mharc ar fhorbairt.)") takes it back, as one missing the ")" printed straight after it
 *  ("… tréithe an fhir.", 2023 Higher 3A(a)(i)) does; a prompt cut just after a "(" its note took ("… ionat féin? (", 2019
 *  Higher 3B(ii)) drops it. Only from the criterion's own guidance; nothing else changes. */
export const closeBrackets = (allocation: IrishAllocation, guidance: string[]): IrishAllocation => {
  const text = guidance.join(' ').replace(/\s+/g, ' ');
  const count = (value: string, mark: string) => value.split(mark).length - 1;
  const close = (note: string) => {
    if (count(note, ')') === count(note, '(') + 1 && text.includes(`(${note}`)) return `(${note}`;
    // "( 5 mharc= 2 mharc ar lomphointe eolais agus 3 mharc ar fhorbairt.)" (2013 Ordinary An Lasair Choille): the bracket printed
    // with a space inside it.
    if (count(note, ')') === count(note, '(') + 1 && text.includes(`( ${note}`)) return `(${note}`;
    if (count(note, '(') === count(note, ')') + 1 && text.includes(`${note})`)) return `${note})`;
    return note;
  };
  return {
    ...allocation,
    parts: allocation.parts.map(part => (part.prompt && /\s\($/.test(part.prompt) && count(part.prompt, '(') > count(part.prompt, ')')
      ? { ...part, prompt: part.prompt.replace(/\s\($/, '') } : part)),
    directions: allocation.directions.map(close),
  };
};

export function irishTariffsFor(source: IrishAnswerSource): IrishAllocation | undefined {
  const result = parseIrishTariffs(source);
  return result.ok ? result.allocation : undefined;
}
