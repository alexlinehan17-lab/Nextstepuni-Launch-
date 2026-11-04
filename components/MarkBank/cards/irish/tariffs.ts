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

const MARC = String.raw`(\d+)\s*m?h?arc\b`;
const SUM = String.raw`((?:\s*\+\s*\d+\s*m?h?arc\b)*)`;
/** A sub-question marker before its prompt: "(i)", "(b) (i)", "6. (a)", "(b)" before a capital. */
const SUB = /(?<=^|\s)(?:\d\.\s*)?(?:\(?[a-f]\)\s*)?\((?:i|ii|iii|iv|v)\)\s|(?<=^|\s)(?:\d\.\s*)?\(?[a-f]\)\s(?=[A-ZÁÉÍÓÚ‘(])/g;
/** What opens or closes a part: "(9 marc)", "{3 mharc: 2 mharc + 1 mharc}", "{6 mharc + 6 mharc}", "Eolas = 13 mharc". */
const OPENER = new RegExp(String.raw`\(\s*${MARC}\s*\)|\{\s*${MARC}(?::\s*((?:\d+\s*m?h?arc\b\s*\+?\s*)+))?${SUM}\s*\}|(?<=^|\s)Eolas\s*=\s*${MARC}${SUM}`, 'g');
/** A priced phrase: "X = 13 mharc", "X = 4 mharc + 4 mharc", "Pointe eolais 1 = Plé … = 5 mharc". */
const PRICED = new RegExp(String.raw`([^•¶\n]{2,400}?)\s*=\s*${MARC}${SUM}(?!\s*(?:ar|an|ceann)\b)`, 'g');
const SAMPLES = /\b(?:Freagraí samplacha|Pointí eolais féideartha|Samplaí|Freagra samplach|Sampla cruinn:)\s*:?\s*/i;
const BAND_TABLE = /\bCatagóir\b[\s\S]*?Lag\/An-lag[^•]*?\d+\s*-\s*\d+(?:\s+\d+\s*-\s*\d+)*/;
/** "5 phointe eolais ag teastáil (5 mharc an ceann ar an gcéad trí phointe eolais + 4 mharc an ceann ar an dá phointe eolais eile)". */
const LADDER = /(\d+)\s*phointe eolais ag teastáil\s*\(\s*(\d+)\s*m?h?arc an ceann ar an g?c?[ée]ad\s+(\w+)\s+phointe eolais(?:\s*\+\s*(\d+)\s*m?h?arc an ceann ar (?:an|na)\s+(\w+)\s+phointe eolais eile)?\s*\)/i;
const NOTE = /(?<=^|\s|\()(?:Nóta:|Ní mór(?=\s)|Is leor(?=\s)|Caithfidh(?=\s)|Bainfear(?=\s)|Gearrfar(?=\s)|Glacfar(?=\s)|Tabharfar(?=\s)|Mura mbíonn(?=\s)|Cuir lúibíní(?=\s)|Dá bharr sin(?=\s)|Gan tréith(?=\s)|Tá [^\s]+ mharc ag gabháil(?=\s)|Sampla cruinn gan(?=\s)|Is samplaí de fhreagraí(?=\s)|Léirigh na marcanna(?=\s)|Ag bun(?=\s))[^•{}¶]*?(?:[.?!](?=\s|\)|$)|(?=\s\(?(?:i|ii|iii|iv|v)\)\s|\sNóta:|\sTreoir:|\s•|\s¶|\s\(\d+\s*m?h?arc\)|\s\{\d|$))/g;
const DEDUCTION = /\[Gaeilge lochtach:[^\]]*\]/g;
/** "Trí phointe eolais ag teastáil anseo: 2 mharc an ceann ar na trí phointe eolais": how a row divides, a direction. */
const COUNT_NOTE = /\b(?:Dhá|Trí|Ceithre|Cúig|\d+)\s+phointe eolais ag teastáil(?: anseo)?:?\s*\d+\s*m?h?arc an ceann ar (?:an|na)[^•=(]*?(?=\s[A-ZÁÉÍÓÚ(]|$)/g;
/** "5 mharc = 2 mharc ar lomphointe eolais + 3 mharc ar fhorbairt": how one point's marks divide, a direction. */
const SPLIT_NOTE = /\b\d+\s*m?h?arc\s*=\s*\d+\s*m?h?arc\s+ar\s[^•]*?(?=\s(?:\d+\s*m?h?arc\s*=|\(|[A-ZÁÉÍÓÚ][^\s=]*(?:\s[^\s=]+){0,6}\s*=)|$)/g;
const FURNITURE = /\b(?:Léirigh mionbhriseadh na marcanna|Eolas\s*\(\d+\)\s*=\s*Gaeilge|E\s*\(\d+\)\s*=|An Mharcáil:|T\d\s*\(\d\)\s*\+\s*S\d|C\s*\d\s*\([A-B]\)\s*\(\d+\)\s*=)[\s\S]*$/;
/** The band header the scheme prints under each sub-question without its ranges: "Catagóir Marc as 4 Sármhaith An-mhaith Maith Measartha Lag/An-lag". */
const BAND_HEADER = /\bCatagóir Marc as \d+\s+Sármhaith\s+An-mhaith\s+Maith\s+Measartha\s+Lag\/An-lag(?:\s+\d+\s*-\s*\d+)*/g;
/** The Gaeilge criterion's descriptor table, printed after each Eolas table: "(5 mharc) Sárchumas … Cumas lag/an-lag … (gramadach, …)". */
const GAEILGE_TABLE = /(?:Gaeilge\s*)?\(\d+\s*m?h?arc\)\s*Sárchumas[\s\S]*?Cumas lag\/an-lag[^.•(]*(?:\([^)]*\))?/g;
const WORDS: Record<string, number> = { aon: 1, amháin: 1, dá: 2, dhá: 2, trí: 3, ceithre: 4, cúig: 5, sé: 6 };

const tidy = (value: string) => value.replace(/¶/g, ' ').replace(/\s+/g, ' ').replace(/^[\s,;:.•–-]+|[\s,;:–-]+$/g, '').trim();
const cumulative = (values: number[]): number[] => {
  const out = [0];
  for (const value of values) out.push(out[out.length - 1] + value);
  return out;
};
const range = (marks: number) => Array.from({ length: marks + 1 }, (_, index) => index);
const stripMarker = (value: string) => tidy(value.replace(/^(?:\d\.\s*)?(?:\(?[a-f]\)\s*)?(?:\(\s*(?:i|ii|iii|iv|v)\s*\)\s*)?/, ''));

interface Draft { prompt?: string; tariff: number; ladder?: number[]; rows: IrishAnswerRow[]; samples: string[]; unpriced?: string }
type Token = { kind: 'open'; tariff: number; ladder?: number[]; at: number; end: number }
  | { kind: 'row'; text: string; marks: number; steps?: number[]; at: number; end: number };

/** The guidance of one criterion as parts of rows, or the reason it cannot be. */
export function parseIrishTariffs(source: IrishAnswerSource, debug?: string[]): IrishAnswerResult {
  const directions: string[] = [];
  let text = source.guidance.join(' ').replace(/[\uf0a7\uf0b7\u25aa\u2022]/g, ' • ').replace(/\s+/g, ' ').trim();
  text = text.replace(DEDUCTION, rule => { directions.push(tidy(rule)); return ' ¶ '; });
  text = text.replace(GAEILGE_TABLE, ' ¶ ');
  text = text.replace(BAND_HEADER, ' ¶ ');
  text = text.replace(FURNITURE, ' ¶ ');
  const bands: string[] = [];
  text = text.replace(BAND_TABLE, table => { bands.push(tidy(table)); return ' ¶ '; });
  text = text.replace(NOTE, note => { directions.push(tidy(note)); return ' ¶ '; });
  text = text.replace(SPLIT_NOTE, note => { directions.push(tidy(note)); return ' ¶ '; });
  text = text.replace(COUNT_NOTE, note => { directions.push(tidy(note)); return ' ¶ '; });
  text = text.replace(/\s+/g, ' ');

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
  const closeLoose = (tariff: number, prompt: string | undefined): boolean => {
    const sum = loose.reduce((acc, row) => acc + row.marks, 0);
    if (loose.length === 0 || sum !== tariff) return false;
    parts.push({ prompt, tariff, rows: loose, samples: [] });
    loose = [];
    return true;
  };
  for (const [segmentIndex, segment] of segments.entries()) {
    let body = segment;
    let samples: string[] = [];
    const sampleMark = SAMPLES.exec(body);
    if (sampleMark) {
      samples = body.slice(sampleMark.index + sampleMark[0].length).split(/[•¶]/).map(tidy).filter(Boolean);
      body = body.slice(0, sampleMark.index);
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
      const boundary = raw.search(/[.:;!?)]\s+(?=[A-ZÁÉÍÓÚ(])(?:[^.:;!?(]|\([^)]*\)|\((?![^)]*\)))*$/);
      const clause = boundary >= 0 ? raw.slice(boundary).replace(/^[.:;!?)]\s+/, '') : raw;
      if (clause.length < raw.length) directions.push(stripMarker(raw.slice(0, raw.length - clause.length)));
      let phrase = stripMarker(clause);
      phrase = phrase.replace(/^[^A-Za-zÁÉÍÓÚáéíóú]+/, '');
      if (!phrase || /^\d+\s*m?h?arc$/i.test(phrase)) continue;
      const first = Number(match[2]);
      const more = (match[3].match(/\d+/g) ?? []).map(Number);
      const marks = first + more.reduce((acc, value) => acc + value, 0);
      const row: IrishAnswerRow = { id: '', text: phrase, marks };
      if (more.length) row.steps = cumulative([first, ...more]);
      tokens.push({ kind: 'row', ...row, at: phraseStart + (raw.length - clause.length), end: match.index! + match[0].length });
    }
    tokens.sort((a, b) => a.at - b.at);
    debug?.push(...tokens.map(token => token.kind === 'open' ? `  OPEN ${token.tariff} ladder=${token.ladder ?? ''} @${token.at}` : `  ROW ${token.marks} steps=${token.steps ?? ''} "${token.text.slice(0, 60)}" @${token.at}`));
    // The prompt is the sub-question as printed, up to the first note the scheme sets inside it
    // ("(Is leor 60 focal.)"); what the scheme prints after the note and before the tariff is a direction.
    const promptPieces = (tokens.length ? body.slice(0, tokens[0].at) : body).split('¶').map(stripMarker).filter(Boolean);
    const promptText = promptPieces[0] ?? '';
    directions.push(...promptPieces.slice(1).filter(piece => piece !== promptText));
    // "5 phointe eolais ag teastáil (…)" after a row prices that row in steps.
    const ladderText = LADDER.exec(body);
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
        const opensSubQuestion = index === 0 && Boolean(promptText);
        // "(25 marc)" on the option's title line, with the sub-questions' own tariffs after it: the criterion, not a part.
        const subTariffs = openerTariffs.filter(tariff => tariff !== source.totalMarks);
        if (token.tariff === source.totalMarks && subTariffs.length && subTariffs.reduce((acc, tariff) => acc + tariff, 0) === source.totalMarks
          && !tokens.slice(index + 1).some(t => t.kind === 'row' && t.at < (tokens.slice(index + 1).find(n => n.kind === 'open')?.at ?? Infinity))) continue;
        // "(23 marc) (2 mharc)" printed together before the rows: the tariff summary, not two parts.
        const run: number[] = [token.tariff];
        for (let k = index + 1; k < tokens.length && tokens[k].kind === 'open' && !tidy(body.slice(tokens[k - 1].end, tokens[k].at)); k += 1) run.push((tokens[k] as { tariff: number }).tariff);
        if (run.length > 1 && run.reduce((acc, value) => acc + value, 0) === source.totalMarks) { skipped.add(index); for (let k = 1; k < run.length; k += 1) skipped.add(index + k); continue; }
        if (skipped.has(index)) continue;
        // "Eolas = 25 marc" printed again for the option's alternative text (scannán nó dráma): one judgement, not two.
        if (token.tariff === source.totalMarks && parts.some(part => part.tariff === source.totalMarks)) { open = parts.find(part => part.tariff === source.totalMarks); continue; }
        // A tariff printed after the rows it totals closes them; printed before, it opens a part.
        if (loose.length && closeLoose(token.tariff, open ? undefined : loosePrompt ?? segmentPrompt)) { loosePrompt = undefined; segmentPrompt = undefined; continue; }
        if (open && open.rows.length === 0 && open.tariff === token.tariff && !opensSubQuestion) continue; // "(23 marc)" repeating the opener
        // "(2 mharc)" straight after "Teideal = 1 mharc Ainm = 1 mharc": the subtotal of the last rows placed, not a
        // new part. A tariff with a prompt before it opens a sub-question even when it equals the last rows' sum.
        if (open && open.rows.length && !open.ladder && !opensSubQuestion) {
          let tail = 0;
          let subtotal = false;
          for (let k = open.rows.length - 1; k >= 0; k -= 1) { tail += open.rows[k].marks; if (tail === token.tariff) { subtotal = true; break; } if (tail > token.tariff) break; }
          if (subtotal) continue;
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
      const answered = placedRows.find(placed => placed.marks === token.marks && /^[ =:]/.test(token.text.slice(placed.text.length)) && token.text.startsWith(placed.text) && token.text.length > placed.text.length + 2);
      if (answered) { answered.text = `${answered.text}: ${token.text.slice(answered.text.length).replace(/^\s*[=:]\s*/, '').trim()}`; continue; }
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
  }
  if (loose.length) {
    // Rows under no printed tariff: the criterion's own remainder, if they add up to it.
    const used = parts.reduce((acc, part) => acc + part.tariff, 0);
    if (!closeLoose(source.totalMarks - used, loosePrompt)) return { ok: false, reason: `rows without a tariff add to ${loose.reduce((acc, row) => acc + row.marks, 0)}, ${source.totalMarks - used} is left` };
  }
  for (const band of bands) directions.push(band);
  let kept = parts.filter(part => part.rows.length || part.prompt || part.ladder);
  const half = kept.length / 2;
  if (kept.length >= 2 && kept.length % 2 === 0 && kept.reduce((acc, part) => acc + part.tariff, 0) === 2 * source.totalMarks
    && kept.slice(0, half).every((part, i) => part.tariff === kept[half + i].tariff)) {
    // The option printed twice for its alternative texts (scannán nó dráma): one set of parts.
    kept = kept.slice(0, half);
  }
  parts.length = 0; parts.push(...kept);
  if (parts.length === 0) return { ok: false, reason: 'no priced sub-question' };

  const built: IrishAnswerPart[] = [];
  let total = 0;
  for (const [index, part] of parts.entries()) {
    const sum = part.rows.reduce((acc, row) => acc + row.marks, 0);
    if (part.ladder) {
      if (part.rows.length === 0) {
        // "{3 mharc: 2 mharc + 1 mharc}" over "Sampla de X: …" answers: the unpriced samples are the rows the ladder prices.
        const answers = part.samples.length ? part.samples : (part.unpriced ?? '').split(/\s(?=Sampla\b)/).map(tidy).filter(Boolean);
        if (!answers.length) return { ok: false, reason: 'ladder without rows' };
        part.rows = answers.map(answer => ({ id: '', text: answer, marks: 0 }));
        part.samples = [];
      }
      if (part.ladder[part.ladder.length - 1] !== part.tariff) return { ok: false, reason: `ladder ends at ${part.ladder[part.ladder.length - 1]}, tariff is ${part.tariff}` };
    } else if (part.rows.length === 0) {
      // A sub-question priced whole with nothing under it: its own words are the row, placed in steps.
      part.rows.push({ id: '', text: part.prompt ?? 'Eolas', marks: part.tariff, steps: range(part.tariff) });
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

export function irishTariffsFor(source: IrishAnswerSource): IrishAllocation | undefined {
  const result = parseIrishTariffs(source);
  return result.ok ? result.allocation : undefined;
}
