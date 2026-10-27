/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Politics and Society answers as ladders and rows.
 *
 * A Politics card carries its scheme as one lifted block (`schemeGuidance`,
 * readable scheme text from scripts/markbank/authoring/politics_author.py)
 * and its criteria with their maxima; essays carry their descriptor bands on
 * the criteria themselves. Until October 2026 the reveal hid the block in a
 * closed details box over a `<select>`, so a student never saw that the
 * scheme prices "Very good explanation" at 8–10 and "Fair" at 0–3, nor the
 * points it lists. The rule since then: what the scheme prices is a button;
 * the scheme's indicative points are a visible list, never a checklist.
 *
 * This module cuts the block into parts, one per criterion (or several
 * inside one criterion priced "3 marks + 2 marks"). It adds no words: a
 * band's label and descriptor are the scheme's lines, a row is a scheme
 * line, a caption is the scheme's own statement of what is asked; where the
 * scheme prices a criterion without printing an answer the row carries the
 * criterion's name and says so. A card is structured only when every
 * criterion gets a ladder whose top mark is its maximum, or rows that fit
 * it; anything else keeps the list fallback, and
 * test/markBankAnswerClarity.test.ts pins how many cards that is.
 *
 * The shapes it reads, from the 2018–2026 schemes:
 *   Very good explanation / 8 - 10M · Very good description 3M      a band
 *   Very Good / 24 - 30M / focused, insightful                       a band with its descriptor
 *   3 marks + 2 marks  then  Very good 3M · Good 2M · Good 2M · Fair 1M · Fair 1M
 *                                           two ladders printed interleaved
 *   2 marks + 1 mark + 1 mark  then one ladder   the ladder, then its lower bands, per term
 *   5 marks + 5 marks  then one ladder     the same ladder for each parallel criterion
 *   Conclusions … Use of documents …       a section per criterion label
 *   Authorship / Two relevant points: 5 marks (x 2)   a section for a criterion group
 *   Responses may make reference to: • …   indicative points (a list)
 *   Answer: 24% · European Parliament / 5M · UNCRC: United Nations …  exact rows
 *   Turkey / Uganda under 3 marks + 2 marks                           rows priced by order
 *   Both nationalities must be named 1M · Name (2M)                   a priced condition / tariff
 *   Note: If the first point is awarded 2M or less…                  a direction
 *   (c) (i) One fact 2 marks · (c) (ii) One fact 1 mark              one criterion priced in sub-tariff headings
 *   One supranational body named 2 marks / Valid explanation 3 marks   (corrections.ts restores a lost price)
 *   The European Court … is responsible for ensuring 1 mark + 1 mark  an answer sentence with its split tariff
 *   Quantitative data  (under "qualitative or quantitative data?")   the alternative the question offers
 *   Use of documents to support evaluation                           a criterion's label heading its ladder
 *   Name  (bare, over a two-mark Name)                               the tariff as the row
 *   Answer: 71.5%… / … 2 marks + 2 marks / Two observations… / 2 marks + 2 marks
 *                                           a sibling's answer and tariff before the card's own ask
 */

import type { PoliticsAllocation, PoliticsAnswerRow, PoliticsBand, PoliticsCriterion, PoliticsPart, PoliticsRubric, SecRubricCard } from '../../../../types/markBank';

export interface PoliticsAnswerSource {
  id: string;
  totalMarks: number;
  questionText: string;
  criteria: readonly PoliticsCriterion[];
  schemeGuidance: readonly string[];
}

export type PoliticsAnswerResult =
  | { ok: true; allocation: PoliticsAllocation }
  | { ok: false; reason: string };

const QUALITY = /^(?:[A-Z][a-z]+:\s*)?(Excellent|Very\s+good|Good|Fair|Weak|Irrelevant)\b(.*)$/i;
/** "16 - 20M independent, insightful comment": a marks line with its descriptor after it. */
const MARKS_DESCRIBED = /^(\d+)(?:\s*[-–]\s*(\d+))?\s*M\s+(\S.*)$/;
const MARKS = /^(\d+)(?:\s*[-–]\s*(\d+))?\s*M$/;
const INLINE_MARKS = /^(.*?)\s+(\d+)(?:\s*[-–]\s*(\d+))?\s*M$/;
/** "Very good commentary 16 - 20M independent, insightful comment": a band with its descriptor after the marks. */
const INLINE_BAND = /^((?:Excellent|Very\s+good|Good|Fair|Weak|Irrelevant)(?:\s+[a-z]+)*)\s+(\d+)(?:\s*[-–]\s*(\d+))?\s*M\s+(\S.*)$/i;
const SPLIT_RANGE = /^(\d+)\s*[-–]$/;
const ALLOC_SUM = /(\d+)(?:\s*(?:marks?|M))?(?:\s*\+\s*\d+(?:\s*(?:marks?|M))?)+\s*(?:marks?|M)\b/i;
const ALLOC_TIMES = /(\d+)\s*(?:x|×|@)\s*(\d+)\s*(?:marks?|M)\b|(\d+)\s*marks?\s*\(\s*x\s*(\d+)\s*\)/i;
const SUB_ALLOC = /^([A-Za-z][^:]{0,60}):\s*(\d+)\s*(?:M|marks?)$/;
const TARIFF_LINE = /^(.+?)\s*\((\d+)\s*M\)(.*)$/;
const BULLET = /^[•∗]\s*(.*)$/;
const LEAD = /^(?:Responses may make reference|Answers may make reference|Candidates may|Possible responses|e\.g\.?$|Examples?:?$|Responses must make reference|Answers must make reference)/i;
const NOTE = /^(?:Note:|Alternative answers|Other valid|Each .*? must\b|.*\bmust be\b.*\bfor full marks|\d+m to the first\b|Award \d+ marks? to\b|Description must match)/i;
const ANSWER_PREFIX = /^Answer:\s*/i;
const KEYED = /^([A-Z]{2,8}|\d{4}):\s+(\S.*)$/;
const ORDINAL: Record<string, number> = { first: 0, second: 1, third: 2, fourth: 3, fifth: 4 };
/** A criterion whose answer is a name the scheme prints bare: a thinker, theory, model, organisation, term. */
const NAME_KIND = /\b(?:thinker|theorist|theory|model|organisation|organisations|name|named|group|term|act|law|right|example|concept)\b/i;
/** "One valid reason", "Two supranational organisations": a count of what is asked, not an answer. */
const COUNT_PHRASE = /^(?:one|two|three|four|a|an)\b/i;
/** A caption that asks or describes rather than names: the sibling's prompt or a ladder's heading. */
const PROMPT_LIKE = /^(?:outline|description|explanation|explain|describe|evaluation|evaluate|identify|the\s|a\s|an\s|how\b|what\b|why\b)/i;
/** Label words that name the same thing in the scheme's two spellings. */
const SAME_WORD: Record<string, string[]> = { thinker: ['theorist'], theorist: ['thinker'], organisation: ['body', 'organisations'], information: ['piece'] };
const labelWords = (label: string) => words(label).flatMap(word => [word, ...(SAME_WORD[word] ?? [])]);
/** A name the scheme prints bare: two capitalised words ("Paulo Freire"), a keyed name ("Name: Martha Nussbaum") or its tariff words ("Named theorist"). */
const PRINTED_NAME = /^(?:Named?\b|[^:]{1,30}:\s*\S)|\b[A-Z][a-zé]+\s+(?:[a-z]+\s+)?[A-Z][a-zé]+/;

const normalise = (value: string) => value.toLowerCase().replace(/[^a-z0-9]+/g, '');
const words = (value: string) => value.toLowerCase().split(/[^a-z]+/).filter(word => word.length > 3);
const range = (lo: number, hi: number) => Array.from({ length: Math.abs(hi - lo) + 1 }, (_, index) => Math.min(lo, hi) + index);
const cumulative = (terms: number[]) => terms.map((_, index) => terms.slice(0, index + 1).reduce((a, b) => a + b, 0));
const tidy = (value: string) => value.replace(/\s+/g, ' ').trim();

type Token =
  | { kind: 'band'; label: string; marks: number[]; descriptor?: string; caption?: string }
  | { kind: 'alloc'; terms: number[]; inline?: boolean }
  | { kind: 'times'; count: number; each: number }
  | { kind: 'section'; label: string; max?: number }
  | { kind: 'priced'; label: string; max: number; line: string }
  | { kind: 'bullet'; text: string }
  | { kind: 'row'; text: string; marks?: number }
  | { kind: 'note'; text: string }
  | { kind: 'lead' }
  | { kind: 'text'; text: string };

/** Read the block line by line into tokens, joining a band label with the marks line under it. */
function tokenise(lines: string[], labels: string[]): Token[] {
  const tokens: Token[] = [];
  const labelOf = (line: string) => {
    const key = normalise(line);
    if (!key) return undefined;
    if (labels.some(label => normalise(label) === key)) return line;
    // "Use of documents to support evaluation" opens the Use of documents criterion: a label of two or more words
    // with the scheme's own words after it, and no price on the line.
    const headed = labels.find(label => label.trim().split(/\s+/).length >= 2 && line.toLowerCase().startsWith(label.toLowerCase())
      && /^\s+[a-z]/.test(line.slice(label.length)) && !/\d\s*M\b|\d+\s*marks?\b/i.test(line));
    if (headed) return headed;
    // "Authorship" names the group "Authorship: first point", "Authorship: second point".
    const group = labels.filter(label => normalise(label).startsWith(key) && /[:(]/.test(label));
    return group.length >= 2 ? line : undefined;
  };
  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    const next = lines[index + 1];
    if (/^etc\.?,?(?:\s*etc\.?)?$/i.test(line.replace(BULLET, '$1').trim())) continue; // "Etc" closes a list
    // A bullet glyph on a line of its own: the answer is the line under it.
    if (/^[•∗]$/.test(line) && next) { tokens.push({ kind: 'bullet', text: tidy(next) }); index += 1; continue; }
    const bullet = BULLET.exec(line);
    if (bullet) { tokens.push({ kind: 'bullet', text: tidy(bullet[1]) }); continue; }
    if (NOTE.test(line)) { tokens.push({ kind: 'note', text: line }); continue; }
    if (LEAD.test(line)) { tokens.push({ kind: 'lead' }); continue; }
    const sub = SUB_ALLOC.exec(line);
    if (sub && !QUALITY.test(line)) { tokens.push({ kind: 'section', label: tidy(sub[1]), max: Number(sub[2]) }); continue; }
    // "(c) (i) One fact 2 marks", "Valid explanation of the role 3 marks": a sub-part's heading with its price read
    // across the baseline from the scheme's margin column (corrections.ts restores the ones the block lost).
    // The same shape also prints a question with its whole price ("Is it important to vote in an election? 10 marks")
    // on a shared block; parsePoliticsAnswers keeps those as the text they were and opens a sub-part only when the
    // card's one criterion is priced in these headings.
    const headedPrice = /^(?:\([a-z]\)\s*)?(?:\((?:i{1,3}|iv|v)\)\s*)?([A-Za-z].*?)\s+(\d+)\s*marks?$/i.exec(line);
    if (headedPrice && !/[+()]|\b[x×]\b|\d\s*marks?\b/i.test(headedPrice[1]) && !QUALITY.test(headedPrice[1]) && !ALLOC_SUM.test(line) && !ALLOC_TIMES.test(line)) {
      tokens.push({ kind: 'priced', label: tidy(headedPrice[1]), max: Number(headedPrice[2]), line });
      continue;
    }
    const section = labelOf(line);
    if (section) { tokens.push({ kind: 'section', label: section }); continue; }
    const times = ALLOC_TIMES.exec(line);
    if (times) {
      tokens.push({ kind: 'times', count: Number(times[1] ?? times[4]), each: Number(times[2] ?? times[3]) });
      const head = tidy(line.slice(0, times.index));
      if (head && !/^\s*$/.test(head)) tokens.push({ kind: 'text', text: head.replace(/:$/, '') });
      const tail = tidy(line.slice(times.index + times[0].length));
      if (tail && QUALITY.test(tail)) lines.splice(index + 1, 0, tail);
      continue;
    }
    const sum = ALLOC_SUM.exec(line);
    if (sum) {
      const terms = [...sum[0].matchAll(/\d+/g)].map(m => Number(m[0]));
      const head = tidy(line.slice(0, sum.index));
      if (head) tokens.push({ kind: 'text', text: head });
      // "The European Court of Human Rights is responsible for ensuring 1 mark + 1 mark": a tariff printed inside
      // a sentence of eight words or more, not a count of what is asked ("Two reasons for why … 2 marks + 2 marks").
      tokens.push({ kind: 'alloc', terms, ...(head && head.split(/\s+/).length >= 8 && !COUNT_PHRASE.test(head) && !head.endsWith('?') ? { inline: true } : {}) });
      continue;
    }
    const quality = QUALITY.exec(line);
    if (quality) {
      const inline = INLINE_MARKS.exec(line);
      const inlineWithDescriptor = INLINE_BAND.exec(line);
      let label = line.replace(/^[A-Z][a-z]+:\s*/, '');
      let marks: number[] | undefined;
      let inlineDescriptor: string | undefined;
      if (inline) { label = tidy(inline[1]); marks = range(Number(inline[2]), Number(inline[3] ?? inline[2])); }
      else if (inlineWithDescriptor) { label = tidy(inlineWithDescriptor[1]); marks = range(Number(inlineWithDescriptor[2]), Number(inlineWithDescriptor[3] ?? inlineWithDescriptor[2])); inlineDescriptor = tidy(inlineWithDescriptor[4]); }
      else if (next && MARKS.test(next)) {
        const m = MARKS.exec(next)!;
        marks = range(Number(m[1]), Number(m[2] ?? m[1]));
        index += 1;
      } else if (next && MARKS_DESCRIBED.test(next)) {
        const m = MARKS_DESCRIBED.exec(next)!;
        marks = range(Number(m[1]), Number(m[2] ?? m[1]));
        inlineDescriptor = tidy(m[3]);
        index += 1;
      } else if (next && SPLIT_RANGE.test(next) && lines[index + 2] && MARKS.test(lines[index + 2])) {
        // "Very good explanation" / "4 -" / "5M": a range the text layer broke over two lines.
        marks = range(Number(SPLIT_RANGE.exec(next)![1]), Number(MARKS.exec(lines[index + 2])![1]));
        index += 2;
      }
      if (marks && inlineDescriptor) { tokens.push({ kind: 'band', label, marks, descriptor: inlineDescriptor }); continue; }
      if (marks) {
        const after = lines[index + 1];
        let descriptor: string | undefined;
        if (after && /^[a-z]/.test(after) && !BULLET.test(after) && !QUALITY.test(after) && !MARKS.test(after) && !NOTE.test(after)) {
          descriptor = after;
          index += 1;
        }
        tokens.push({ kind: 'band', label, marks, ...(descriptor ? { descriptor } : {}) });
        continue;
      }
    }
    if (next && MARKS.test(next)) {
      // "European Parliament" / "5M": an exact answer with its own price.
      const m = MARKS.exec(next)!;
      if (!m[2]) { tokens.push({ kind: 'row', text: tidy(line.replace(ANSWER_PREFIX, '')), marks: Number(m[1]) }); index += 1; continue; }
    }
    const inlineRow = INLINE_MARKS.exec(line);
    if (inlineRow && !inlineRow[3]) {
      // "Both non-Irish nationalities must be named 1M": a priced condition.
      tokens.push({ kind: 'row', text: tidy(inlineRow[1]), marks: Number(inlineRow[2]) });
      continue;
    }
    const tariff = TARIFF_LINE.exec(line);
    if (tariff && labels.some(label => normalise(tariff[1]).includes(normalise(label)) || normalise(label).includes(normalise(tariff[1])))) {
      // "Name (2M) and description (3M) of a model…": the first criterion's tariff.
      tokens.push({ kind: 'section', label: tidy(tariff[1]), max: Number(tariff[2]) });
      continue;
    }
    if (ANSWER_PREFIX.test(line) || KEYED.test(line)) { tokens.push({ kind: 'row', text: tidy(line.replace(ANSWER_PREFIX, '')) }); continue; }
    tokens.push({ kind: 'text', text: line });
  }
  return tokens;
}

type BandToken = Extract<Token, { kind: 'band' }>;

/**
 * Group a run of bands into the ladder sets the scheme prints: a set is one
 * ladder, or several printed interleaved ("Very good 3M · Good 2M · Good 2M
 * · Fair 1M · Fair 1M"), where the n-th repeat of a label belongs to the
 * n-th ladder. A band with a new label whose marks do not fall below the
 * ladder's last band starts the next set ("… Irrelevant 0M · Good
 * description 2M …").
 */
function ladderSets(bands: BandToken[]): { ladders: PoliticsBand[][]; caption?: string }[] {
  const sets: { ladders: PoliticsBand[][]; caption?: string }[] = [];
  let current: PoliticsBand[][] = [];
  let caption: string | undefined;
  let seen = new Map<string, number>();
  for (const band of bands) {
    const key = normalise(band.label);
    const entry: PoliticsBand = { label: band.label, marks: band.marks, ...(band.descriptor ? { descriptor: band.descriptor } : {}) };
    const n = seen.get(key) ?? 0;
    const last = current[0]?.[current[0].length - 1];
    if (n === 0 && last && Math.max(...band.marks) >= Math.min(...last.marks)) {
      sets.push({ ladders: current, ...(caption ? { caption } : {}) });
      current = [];
      caption = undefined;
      seen = new Map();
    }
    if (current.length === 0) caption = band.caption;
    const index = seen.get(key) ?? 0;
    seen.set(key, index + 1);
    (current[index] ??= []).push(entry);
  }
  if (current.length) sets.push({ ladders: current, ...(caption ? { caption } : {}) });
  return sets;
}

const ladderMax = (ladder: PoliticsBand[]) => Math.max(...ladder.flatMap(band => band.marks));
const subLadder = (ladder: PoliticsBand[], top: number): PoliticsBand[] =>
  ladder.map(band => ({ ...band, marks: band.marks.filter(mark => mark <= top) })).filter(band => band.marks.length > 0);

interface Region {
  labels: string[];
  max?: number;
  bands: BandToken[];
  rows: { text: string; marks?: number }[];
  bullets: string[];
  captions: string[];
  alloc?: number[];
  allocInline?: boolean;
  times?: { count: number; each: number };
}

/** Cut one card's block into parts, one per criterion, or say why not. */
export function parsePoliticsAnswers(source: PoliticsAnswerSource): PoliticsAnswerResult {
  const criteria = source.criteria;
  if (criteria.length === 0) return { ok: false, reason: 'no criteria' };

  // Essays and any card whose criteria carry their bands are structured by data.
  if (criteria.every(criterion => criterion.bands?.length)) {
    const parts: PoliticsPart[] = criteria.map((criterion, index) => ({
      id: `p${index + 1}`,
      label: criterion.label,
      max: criterion.maxMarks,
      bands: criterion.bands!.map(band => ({ label: band.label, marks: [...band.marks], ...(band.guidance ? { descriptor: band.guidance } : {}) })),
    }));
    return { ok: true, allocation: { parts, examples: [], directions: [] } };
  }
  if (criteria.some(criterion => criterion.bands?.length)) return { ok: false, reason: 'bands on some criteria only' };

  const lines = source.schemeGuidance.flatMap(block => block.split('\n')).map(tidy).filter(Boolean);
  if (lines.length === 0) return { ok: false, reason: 'no scheme block' };
  const read = tokenise(lines, criteria.map(criterion => criterion.label));
  // Headings priced in the margin open sub-parts only when they price the card's one criterion between them
  // ("(c) (i) One fact 2 marks", "(c) (ii) One fact 1 mark", "(c) (iii) One fact 1 mark" on a four-mark response);
  // otherwise they are the lines they were (a sibling's question with its total on a shared block).
  const pricedHeads = read.filter((token): token is Extract<Token, { kind: 'priced' }> => token.kind === 'priced');
  const subTariffs = criteria.length === 1 && pricedHeads.length >= 2 && pricedHeads.reduce((sum, token) => sum + token.max, 0) === criteria[0].maxMarks
    && pricedHeads.every(token => !normalise(source.questionText).includes(normalise(token.label)));
  const tokens: Token[] = read.map(token => token.kind !== 'priced' ? token : subTariffs ? { kind: 'section', label: token.label, max: token.max } : { kind: 'text', text: token.line });

  // Regions: a section label or a sub-allocation opens the next criterion's
  // region (two labels in a row name a group); bands, rows and bullets before
  // any section belong to the first.
  const regions: Region[] = [{ labels: [], bands: [], rows: [], bullets: [], captions: [] }];
  const examples: string[] = [];
  const directions: string[] = [];
  const question = normalise(source.questionText);
  let region = regions[0];
  let leadOpen = false;
  let lastText: string | undefined;
  let allocAfterCaption = false;
  /** One of the alternatives the question itself offers ("qualitative or quantitative data?"). */
  const offered = (text: string) => {
    const first = words(text)[0];
    return criteria.length === 1 && criteria[0].maxMarks <= 2 && first !== undefined && text.split(/\s+/).length <= 3
      && new RegExp(`\\b${first}\\b\\s+or\\b|\\bor\\s+${first}\\b`, 'i').test(source.questionText);
  };
  /** The card's own ask in the scheme's words: most of the line's words are the question's. */
  const echoesQuestion = (text: string) => {
    const own = words(text); const asked = new Set(words(source.questionText));
    const shared = own.filter(word => asked.has(word));
    return own.length >= 3 && shared.length >= 3 && shared.length >= own.length * 0.6;
  };
  const empty = (r: Region) => !r.bands.length && !r.rows.length && !r.bullets.length;
  for (const [tokenIndex, token] of tokens.entries()) {
    switch (token.kind) {
      case 'section':
        if (empty(region) && region.labels.length && region.max === undefined && token.max === undefined) {
          region.labels.push(token.label);
        } else if (!empty(region) || region.labels.length) {
          region = { labels: [token.label], max: token.max, bands: [], rows: [], bullets: [], captions: [] };
          regions.push(region);
        } else { region.labels = [token.label]; region.max = token.max; }
        leadOpen = false;
        lastText = undefined;
        break;
      case 'band':
        // A ladder after a sub-allocation of a different size ("Identify a
        // relevant right: 2M … Very good description 6 - 8M") scores the next criterion.
        if (region.max !== undefined && region.bands.length === 0 && Math.max(...token.marks) > region.max) {
          region = { labels: [], bands: [], rows: [], bullets: [], captions: [] };
          regions.push(region);
        }
        region.bands.push({ ...token, ...(lastText ? { caption: lastText } : {}) });
        leadOpen = false;
        break;
      case 'alloc': region.alloc = token.terms; region.allocInline = token.inline; allocAfterCaption = Boolean(token.inline) && lastText !== undefined; break;
      case 'times': region.times = { count: token.count, each: token.each }; break;
      case 'bullet': if (leadOpen || region.rows.length === 0) region.bullets.push(token.text); else region.rows.push({ text: token.text }); break;
      case 'row': region.rows.push({ text: token.text, marks: token.marks }); lastText = undefined; break;
      case 'note': directions.push(token.text); break;
      case 'lead': leadOpen = true; break;
      case 'text': {
        // "…is responsible for ensuring 1 mark + 1 mark" / "the implementation of…": the sentence the tariff
        // interrupted goes on under it.
        if (allocAfterCaption && /^[a-z]/.test(token.text) && region.captions.length) { region.captions.push(token.text); allocAfterCaption = false; break; }
        allocAfterCaption = false;
        // The card's own ask restated after a sibling's answer and tariff on a shared block ("Answer: 71.5%…" /
        // "One advantage and one disadvantage… 2 marks + 2 marks" / "Two observations about the presentation of
        // data in the graphic." / "2 marks + 2 marks"): what came before is the siblings', and the block starts here.
        if (regions.length === 1 && !region.labels.length && !region.bands.length && (region.rows.length || region.alloc) && echoesQuestion(token.text) && tokens[tokenIndex + 1]?.kind === 'alloc') {
          directions.push(...region.rows.map(row => row.text), ...region.captions);
          region = { labels: [], bands: [], rows: [], bullets: [], captions: [] };
          regions.splice(0, 1, region);
        }
        // The scheme restating the question is not a caption; a short statement of what is asked is. The answer
        // to a question that offers it ("qualitative or quantitative data?" / "Quantitative data") is.
        if (criteria.some(criterion => normalise(criterion.label) === normalise(token.text))) { directions.push(token.text); break; }
        if (offered(token.text)) { region.rows.push({ text: token.text }); break; }
        if (question.includes(normalise(token.text))) break;
        if (token.text.endsWith('?')) break;
        if (region.bands.length || region.rows.length) { directions.push(token.text); break; }
        region.captions.push(token.text);
        lastText = token.text;
        break;
      }
      default: break;
    }
  }

  const parts: PoliticsPart[] = [];
  const pending = [...criteria];
  const push = (part: Omit<PoliticsPart, 'id'>) => parts.push({ id: `p${parts.length + 1}`, ...part });
  const take = (criterion: PoliticsCriterion) => { pending.splice(pending.indexOf(criterion), 1); };
  const checkLadder = (ladder: PoliticsBand[], criterion: PoliticsCriterion, max: number): string | undefined => {
    if (ladderMax(ladder) !== max) return `ladder tops at ${ladderMax(ladder)}, criterion ${criterion.label} is ${max}`;
    const marks = ladder.flatMap(band => band.marks);
    if (marks.some(mark => !criterion.permittedMarks.includes(mark))) return `ladder mark outside ${criterion.label}'s permitted marks`;
    if (new Set(marks).size !== marks.length) return 'ladder marks overlap';
    return undefined;
  };
  const claimedLater = (from: number) => new Set(regions.slice(from + 1).flatMap(later => later.labels.map(normalise)));
  const matches = (label: string, criterion: PoliticsCriterion) =>
    normalise(criterion.label) === normalise(label) || (normalise(criterion.label).startsWith(normalise(label)) && /[:(]/.test(criterion.label));

  // A single criterion priced in printed sub-tariffs ("(c) (i) One fact 2 marks … (c) (ii) One fact 1 mark …",
  // "One supranational body named 2 marks / Valid explanation of the role 3 marks"): one part per sub-tariff. A
  // sub-part whose price a printed ladder tops is placed on that ladder and its fact is an indicative point; one
  // with a printed answer claims it; one with neither carries its heading as the tariff. Any other ladder is a rule.
  const priced = regions.filter(current => current.max !== undefined && current.labels.length);
  const bandsOnly = (current: Region) => !current.labels.length && !current.rows.length && !current.bullets.length && !current.captions.length && !current.alloc;
  if (criteria.length === 1 && priced.length >= 2 && priced.reduce((sum, current) => sum + current.max!, 0) === criteria[0].maxMarks
      && regions.every(current => priced.includes(current) || bandsOnly(current))) {
    const criterion = criteria[0];
    const strays = regions.flatMap(current => ladderSets(current.bands).flatMap(set => set.ladders).filter(ladder => ladderMax(ladder) !== current.max));
    for (const current of priced) {
      const own = ladderSets(current.bands).flatMap(set => set.ladders).find(ladder => ladderMax(ladder) === current.max)
        ?? (priced.filter(other => other.max === current.max).length === 1 && strays.filter(ladder => ladderMax(ladder) === current.max).length === 1
          ? strays.splice(strays.findIndex(ladder => ladderMax(ladder) === current.max), 1)[0] : undefined);
      const heading = current.labels[0];
      // A fact the text layer wrapped: a line starting lower-case continues the one before it.
      const joined: string[] = [];
      for (const text of current.captions) {
        if (joined.length && /^[a-z]/.test(text)) joined[joined.length - 1] = `${joined[joined.length - 1]} ${text}`;
        else joined.push(text);
      }
      examples.push(...current.bullets, ...joined.filter(text => /^Example:/i.test(text)));
      const facts = joined.filter(text => !/^Example:/i.test(text) && text.split(/\s+/).length >= 3);
      if (own) {
        const problem = checkLadder(own, criterion, current.max!);
        if (problem) return { ok: false, reason: problem };
        push({ label: criterion.label, caption: heading, max: current.max!, bands: own.map(band => ({ ...band, marks: [...band.marks] })) });
        examples.push(...facts);
        continue;
      }
      const answers = current.rows.length ? current.rows.map(row => row.text) : facts;
      if (answers.length) push({ label: criterion.label, caption: heading, max: current.max!, rows: answers.map((text, index) => ({ id: `r${index + 1}`, text, marks: current.max! })), count: 1 });
      else push({ label: criterion.label, max: current.max!, rows: [{ id: 'r1', text: heading, marks: current.max!, tariffOnly: true }], count: 1 });
    }
    for (const ladder of strays) directions.push(...ladder.flatMap(band => [band.label, ...(band.descriptor ? [band.descriptor] : [])]));
    take(criterion);
    regions.length = 0;
  }

  for (const [regionIndex, current] of regions.entries()) {
    let scoped: PoliticsCriterion[] | undefined;
    if (current.labels.length) {
      const byLabel = pending.filter(candidate => current.labels.some(label => matches(label, candidate)));
      const byMax = current.max !== undefined ? pending.filter(candidate => candidate.maxMarks === current.max) : [];
      scoped = byLabel.length ? byLabel : byMax.length === 1 ? byMax : [];
      if (scoped.length === 0) { directions.push(...current.captions); continue; }
    }
    const later = claimedLater(regionIndex);
    const candidates = () => scoped ? scoped.filter(candidate => pending.includes(candidate)) : pending.filter(candidate => !later.has(normalise(candidate.label)));
    const caption = current.captions[0];
    const sets = ladderSets(current.bands);
    let foreign = false;

    // Priced rows printed beside a ladder ("First name 2M … Second name 1M" between two "Explanation 1M /
    // Irrelevant 0M" ladders): each row scores the criterion whose label shares its words and its mark.
    if (sets.length && current.rows.length) {
      const tops = sets.flatMap(set => set.ladders.map(ladderMax));
      for (const row of [...current.rows]) {
        if (row.marks === undefined) continue;
        const pool = candidates();
        const target = pool.find(candidate => candidate.maxMarks === row.marks && words(row.text).some(word => normalise(candidate.label).includes(word)));
        if (target && tops.includes(row.marks) && !/[a-z]\s[a-z]/i.test(row.text)) {
          // "Explanation 8M" over "Very good answer 6 - 8M": the ladder's tariff line, and the ladder scores it.
          directions.push(row.text);
          current.rows.splice(current.rows.indexOf(row), 1);
        } else if (target) {
          push({ label: target.label, max: target.maxMarks, rows: [{ id: 'r1', text: row.text, marks: row.marks, tariffOnly: true }], count: 1 });
          take(target);
          current.rows.splice(current.rows.indexOf(row), 1);
        } else if (!pool.some(candidate => candidate.maxMarks === row.marks) || (tops.includes(row.marks) && !/[a-z]\s[a-z]/i.test(row.text.replace(/^[A-Z][a-z]+$/, '')))) {
          // A sibling card's priced line on the shared block ("Name: Martha Nussbaum 2M" under the explanation
          // card), or the ladder's own tariff line ("Explanation 8M" over "Very good answer 6 - 8M"): a direction.
          directions.push(row.text);
          current.rows.splice(current.rows.indexOf(row), 1);
        }
      }
    }
    // "1 + 1 mark" printed under a caption with nothing else: the caption's words are the tariff rows of
    // the criteria the terms price, in order ("Two supranational organisations" over First / Second organisation).
    if (current.alloc && !current.rows.length && !current.bullets.length && (sets.length === 0 || current.alloc.length > 1)) {
      const pool = candidates();
      const terms = current.alloc;
      const chosen: PoliticsCriterion[] = [];
      const targets = terms.map(term => { const found = pool.find(candidate => candidate.maxMarks === term && !chosen.includes(candidate)); if (found) chosen.push(found); return found; });
      const distinct = new Set(targets);
      const ordinal = targets.every(target => target && ORDINAL[target.label.toLowerCase().split(/\s+/)[0]] !== undefined);
      const tariffText = caption && !(sets.length && caption === current.captions[current.captions.length - 1]) ? caption : undefined;
      // A ladder captioned with another pending criterion's words ("Valid description" over Description 5M) is
      // spoken for, so terms of its size still price their own criteria ("5 marks + 5 marks" for the two pieces).
      const spokenFor = sets.every(set => set.caption && pool.some(candidate => !chosen.includes(candidate)
        && set.ladders.some(ladder => ladderMax(ladder) === candidate.maxMarks) && words(set.caption).some(word => normalise(candidate.label).includes(word))));
      if (targets.every(Boolean) && distinct.size === targets.length && targets.every(target => target!.maxMarks <= (ordinal ? 5 : 3)) && (sets.length === 0 || spokenFor || !targets.some(target => sets.flatMap(set => set.ladders.map(ladderMax)).includes(target!.maxMarks)))) {
        for (const target of targets) {
          push({ label: target!.label, max: target!.maxMarks, rows: [{ id: 'r1', text: tariffText ?? target!.label, marks: target!.maxMarks, tariffOnly: true }], count: 1 });
          take(target!);
        }
        current.alloc = undefined;
        if (caption) current.captions.shift();
      }
    }
    // An answer sentence carrying its own split tariff ("The European Court of Human Rights is responsible for
    // ensuring 1 mark + 1 mark" / "the implementation of the European Convention…"): the sentence is the band a
    // student places the printed marks on, its wrapped remainder the descriptor.
    if (current.alloc && current.allocInline && criteria.length === 1 && pending.includes(criteria[0]) && current.alloc.reduce((a, b) => a + b, 0) === criteria[0].maxMarks
        && current.captions.length && !current.rows.length && !current.bullets.length
        && !sets.some(set => set.ladders.some(ladder => ladderMax(ladder) === criteria[0].maxMarks || current.alloc!.includes(ladderMax(ladder))))) {
      const [head, next] = current.captions;
      if (head.split(/\s+/).length >= 8 && !COUNT_PHRASE.test(head) && !head.endsWith('?')) {
        const descriptor = next && /^[a-z]/.test(next) ? next : undefined;
        push({ label: criteria[0].label, max: criteria[0].maxMarks, bands: [{ label: head, marks: cumulative(current.alloc), ...(descriptor ? { descriptor } : {}) }] });
        take(criteria[0]);
        current.captions.splice(0, descriptor ? 2 : 1);
        current.alloc = undefined;
      }
    }
    // Scheme words printed as a name-kind criterion's answer ("Paulo Freire" over Thinker 1M,
    // "Kathleen Lynch, Sylvia Walby..." over Thinker 2M): a row at the criterion's mark.
    if (criteria.length === 1 && criteria[0].maxMarks <= 2 && pending.includes(criteria[0]) && current.captions.length && !current.rows.length && !current.bullets.length) {
      const answer = current.captions[0];
      if (answer.split(/\s+/).length <= 4 && !PROMPT_LIKE.test(answer) && !COUNT_PHRASE.test(answer) && (!question.includes(normalise(answer)) || offered(answer)) && !(sets.length && current.captions.length === 1)) {
        push({ label: criteria[0].label, max: criteria[0].maxMarks, rows: [{ id: 'r1', text: answer, marks: criteria[0].maxMarks }], count: 1 });
        take(criteria[0]);
        current.captions.shift();
      }
    }
    if (current.captions.length) {
      // The caption a ladder sits under is the ladder's, not an answer.
      const ladderCaption = sets.length ? current.captions[current.captions.length - 1] : undefined;
      for (const text of [...current.captions]) {
        const pool = candidates();
        const target = pool.find(candidate => candidate.maxMarks <= 2 && NAME_KIND.test(candidate.label));
        const named = PRINTED_NAME.test(text) || words(target?.label ?? '').some(word => normalise(text).includes(word));
        if (!target || text === ladderCaption || text.split(/\s+/).length > 10 || COUNT_PHRASE.test(text) || PROMPT_LIKE.test(text) || !named || question.includes(normalise(text))) break;
        push({ label: target.label, max: target.maxMarks, rows: [{ id: 'r1', text, marks: target.maxMarks }], count: 1 });
        take(target);
        current.captions.splice(current.captions.indexOf(text), 1);
      }
    }

    // Bullets before a ladder that scores the next criterion are the first
    // criterion's possible answers ("Name (2M) … • Hart's Ladder … Description 3M").
    if (sets.length && current.bullets.length && current.rows.length === 0) {
      const pool = candidates();
      const first = pool[0];
      const tops = sets.flatMap(set => set.ladders.map(ladderMax));
      const nameless = pool.filter(candidate => !tops.includes(candidate.maxMarks));
      if (first && !tops.includes(first.maxMarks) && pool[1] && tops.includes(pool[1].maxMarks) && (current.max === undefined || current.max === first.maxMarks)) {
        push({ label: first.label, max: first.maxMarks, rows: current.bullets.map((text, index) => ({ id: `r${index + 1}`, text, marks: first.maxMarks })), count: 1 });
        take(first);
        current.bullets = [];
      } else if (nameless.length > 1 && nameless.length < pool.length && nameless.every(candidate => candidate.maxMarks === nameless[0].maxMarks) && current.bullets.length >= nameless.length) {
        // "1 + 1 marks" over a list of departments, then the ladder for the work of one: the list answers both names.
        const each = nameless[0].maxMarks;
        push({ label: `${nameless[0].label} … ${nameless[nameless.length - 1].label}`, max: each * nameless.length, rows: current.bullets.map((text, index) => ({ id: `r${index + 1}`, text, marks: each })), count: nameless.length });
        nameless.forEach(take);
        current.bullets = [];
      }
    }

    for (const set of sets) {
      const setCaption = set.caption ?? caption;
      const pool = candidates();
      if (pool.length === 0) break; // the rest of the block belongs to a sibling card
      const first = pool[0];
      const tops = set.ladders.map(ladderMax);
      const cap = setCaption ? { caption: setCaption } : {};
      if (set.ladders.length > 1) {
        const total = tops.reduce((a, b) => a + b, 0);
        if (first.maxMarks === total && !tops.includes(first.maxMarks)) {
          // Interleaved ladders priced inside one criterion ("3 marks + 2 marks" on one 5-mark response).
          for (const ladder of set.ladders) {
            const marks = ladder.flatMap(band => band.marks);
            if (new Set(marks).size !== marks.length) return { ok: false, reason: 'ladder marks overlap' };
            push({ label: first.label, ...cap, max: ladderMax(ladder), bands: ladder });
          }
          take(first);
          continue;
        }
        // Otherwise each criterion takes the ladder of its own top mark, reused where printed once.
        for (const criterion of pool) {
          const ladder = set.ladders.find(candidate => ladderMax(candidate) === criterion.maxMarks);
          if (!ladder) break;
          const problem = checkLadder(ladder, criterion, criterion.maxMarks);
          if (problem) return { ok: false, reason: problem };
          push({ label: criterion.label, ...cap, max: criterion.maxMarks, bands: ladder.map(band => ({ ...band, marks: [...band.marks] })) });
          take(criterion);
        }
        continue;
      }
      const ladder = set.ladders[0];
      const top = tops[0];
      const equalTerms = current.alloc ? current.alloc.filter(term => term === top).length : 0;
      // A ladder captioned with a criterion's own words ("One reason" over Reason 2M) scores that criterion first.
      const captioned = setCaption ? pool.find(candidate => candidate.maxMarks === top && words(setCaption).some(word => normalise(candidate.label).includes(word))) : undefined;
      const parallel = [...(captioned ? [captioned] : []), ...pool.filter(candidate => candidate.maxMarks === top && candidate !== captioned)];
      if (parallel.length > 0) {
        // One printed ladder for each parallel criterion of its top mark.
        const limit = current.times?.count ?? (equalTerms > 1 ? equalTerms : undefined);
        for (const criterion of (scoped ? parallel : parallel.slice(0, limit ?? parallel.length))) {
          const problem = checkLadder(ladder, criterion, top);
          if (problem) return { ok: false, reason: problem };
          push({ label: criterion.label, ...cap, max: top, bands: ladder.map(band => ({ ...band, marks: [...band.marks] })) });
          take(criterion);
        }
        continue;
      }
      const terms = current.alloc && current.alloc.reduce((a, b) => a + b, 0) === first.maxMarks ? current.alloc
        : current.times && current.times.each * current.times.count === first.maxMarks ? Array.from({ length: current.times.count }, () => current.times!.each)
        : undefined;
      if (terms && terms[0] === top && terms.every(term => term <= top)) {
        // "2 marks + 1 mark + 1 mark" over one printed ladder: each term takes the ladder's bands up to it.
        for (const term of terms) {
          const bands = subLadder(ladder, term);
          const problem = checkLadder(bands, first, term);
          if (problem) return { ok: false, reason: problem };
          push({ label: first.label, ...cap, max: term, bands });
        }
        take(first);
        continue;
      }
      // "2 marks + 3 marks" over one printed ladder whose top is one of the terms: the other term is the
      // example or name the scheme prices without a ladder — its bullets, or its own words as a tariff row.
      if (current.alloc && current.alloc.reduce((a, b) => a + b, 0) === first.maxMarks && current.alloc.includes(top) && !current.alloc.every(term => term === top)) {
        for (const term of current.alloc.filter(term => term !== top)) {
          const rows = current.bullets.length
            ? current.bullets.map((text, index) => ({ id: `r${index + 1}`, text, marks: term }))
            : [{ id: 'r1', text: setCaption ?? first.label, marks: term, tariffOnly: true as const }];
          push({ label: first.label, ...cap, max: term, rows, count: 1 });
        }
        current.bullets = [];
        push({ label: first.label, ...cap, max: top, bands: ladder.map(band => ({ ...band, marks: [...band.marks] })) });
        take(first);
        continue;
      }
      // "22%" then a three-mark ladder on a four-mark response: the short printed answer is the remainder's row.
      if (pool.length === 1 && first.maxMarks - top >= 1 && first.maxMarks - top <= 2 && !current.alloc && current.captions.length <= 2) {
        const answer = current.captions.find(text => text !== setCaption && text.split(/\s+/).length <= 4 && /^[A-Z0-9]/.test(text) && !/\.$/.test(text) && !PROMPT_LIKE.test(text) && !COUNT_PHRASE.test(text));
        if (answer) {
          push({ label: first.label, ...cap, max: first.maxMarks - top, rows: [{ id: 'r1', text: answer, marks: first.maxMarks - top }], count: 1 });
          push({ label: first.label, ...cap, max: top, bands: ladder.map(band => ({ ...band, marks: [...band.marks] })) });
          take(first);
          continue;
        }
      }
      // A ladder that tops at no criterion of this card is the sibling's, printed on the shared block of a
      // split question: it stays a direction and the bullets or rows under it are this card's answers.
      if (!pool.some(candidate => candidate.maxMarks === top) && (current.bullets.length || current.rows.length || pool.every(candidate => candidate.maxMarks < top))) {
        directions.push(...ladder.flatMap(band => [band.label, ...(band.descriptor ? [band.descriptor] : [])]));
        foreign = true;
        continue;
      }
      return { ok: false, reason: `ladder tops at ${top}, criterion ${first.label} is ${first.maxMarks}` };
    }
    if (current.bullets.length && sets.length && !foreign) examples.push(...current.bullets);
    if (sets.length && current.rows.length && !foreign) return { ok: false, reason: 'rows beside a ladder' };
    if (sets.length && !foreign) continue;

    const items: { text: string; marks?: number }[] = current.rows.length ? current.rows : current.bullets.map(text => ({ text }));
    const pool = candidates();
    if (items.length === 0) {
      // A sub-allocation with nothing printed under it ("Name (2M)"): the tariff is the row.
      // A sub-allocation with nothing printed under it ("Name (2M)"), or a bare "Name" over a one- or two-mark
      // name the scheme prints no answer for: the tariff is the row.
      if (scoped && pool.length && (current.max !== undefined || (pool[0].maxMarks <= 2 && NAME_KIND.test(pool[0].label) && current.labels.length === 1))) {
        const criterion = pool[0];
        push({ label: criterion.label, ...(caption ? { caption } : {}), max: criterion.maxMarks, rows: [{ id: 'r1', text: current.labels[0], marks: criterion.maxMarks, tariffOnly: true }], count: 1 });
        take(criterion);
      } else {
        directions.push(...current.captions);
      }
      continue;
    }
    const criterion = pool[0];
    if (!criterion) return { ok: false, reason: 'answers with no criterion left to score' };
    const ordinal = ORDINAL[criterion.label.toLowerCase().split(/\s+/)[0]];
    let chosen = items;
    if (new Set(items.map(item => normalise(item.text))).size !== items.length) {
      // "True / True / True" under "2 marks + 2 marks + 1 mark": the n-th statement's answer.
      if (ordinal !== undefined && current.alloc && items.length === current.alloc.length && items[ordinal]) chosen = [items[ordinal]];
      else return { ok: false, reason: 'repeated answer lines' };
    }
    const parallel = pool.filter(candidate => candidate.maxMarks === criterion.maxMarks);
    const orderPriced = !current.times && current.alloc && current.alloc.length > 1 && chosen.length >= current.alloc.length
      && chosen.every(item => item.marks === undefined) && current.alloc.reduce((a, b) => a + b, 0) === criterion.maxMarks;
    if (orderPriced) {
      // "Turkey / Uganda" under "3 marks + 2 marks": the first right answer earns 3, the second 2.
      push({ label: criterion.label, ...(caption ? { caption } : {}), max: criterion.maxMarks, rows: chosen.map((item, index) => ({ id: `r${index + 1}`, text: item.text, marks: 0 })), count: current.alloc!.length, ladder: cumulative(current.alloc!) });
      take(criterion);
      continue;
    }
    const each = current.times?.each ?? current.max ?? (chosen.every(item => item.marks !== undefined) ? undefined : criterion.maxMarks);
    const count = current.times?.count ?? (parallel.length > 1 && chosen.length >= parallel.length && !scoped ? parallel.length : 1);
    const covered = count > 1 ? parallel.slice(0, count) : [criterion];
    const max = covered.reduce((sum, item) => sum + item.maxMarks, 0);
    const priced: PoliticsAnswerRow[] = chosen.map((item, index) => ({ id: `r${index + 1}`, text: item.text, marks: item.marks ?? each ?? 0 }));
    if (priced.some(row => row.marks > max)) return { ok: false, reason: 'row above its criterion' };
    push({ label: covered.length > 1 ? `${covered[0].label} … ${covered[covered.length - 1].label}` : criterion.label, ...(caption ? { caption } : {}), max, rows: priced, count });
    covered.forEach(take);
  }

  // A block that prices its criteria without printing any answer or ladder
  // ("Nine grounds of discrimination / 2 marks + 1 mark + 1 mark + 1 mark").
  const printedAnything = regions.some(current => current.bands.length || current.rows.length || current.bullets.length);
  if (pending.length > 0 && !printedAnything) {
    for (const criterion of [...pending]) {
      push({ label: criterion.label, max: criterion.maxMarks, rows: [{ id: 'r1', text: criterion.label, marks: criterion.maxMarks, tariffOnly: true }], count: 1 });
      take(criterion);
    }
  }
  for (const criterion of [...pending]) {
    if (criterion.maxMarks > 2 || !NAME_KIND.test(criterion.label)) continue;
    const printed = directions.find(note => !PROMPT_LIKE.test(note) && labelWords(criterion.label).some(word => normalise(note).includes(word)) && note.split(/\s+/).length <= 12);
    if (!printed) continue;
    push({ label: criterion.label, max: criterion.maxMarks, rows: [{ id: 'r1', text: printed, marks: criterion.maxMarks, ...(PRINTED_NAME.test(printed) && !/^Named?\b/.test(printed) ? {} : { tariffOnly: true }) }], count: 1 });
    take(criterion);
    directions.splice(directions.indexOf(printed), 1);
  }
  if (pending.length > 0) return { ok: false, reason: `no ladder or rows for ${pending.map(criterion => criterion.label).join(', ')}` };
  const sum = parts.reduce((total, part) => total + part.max, 0);
  if (sum !== source.totalMarks) return { ok: false, reason: `parts add to ${sum}, card is ${source.totalMarks}` };
  void words;
  const seen = new Set<string>();
  return { ok: true, allocation: { parts, examples, directions: directions.filter(note => !seen.has(note) && seen.add(note)) } };
}

type PoliticsCard = SecRubricCard & { rubric: PoliticsRubric };

export const politicsAnswerSource = (card: PoliticsCard): PoliticsAnswerSource => ({
  id: card.id,
  totalMarks: card.totalMarks,
  questionText: card.questionText,
  criteria: card.rubric.criteria,
  schemeGuidance: card.rubric.schemeGuidance ?? [],
});

/** The card as shipped: its scheme as ladders and rows where they reconcile, untouched otherwise. */
export function withPoliticsAnswers<T extends PoliticsCard>(card: T): T {
  const result = parsePoliticsAnswers(politicsAnswerSource(card));
  return result.ok ? { ...card, rubric: { ...card.rubric, allocation: result.allocation } } : card;
}
