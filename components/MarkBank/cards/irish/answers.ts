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
/** "(dhá phointe eolais anseo = 2 mharc + 1 mharc = 3 mharc)" inside an answer, and "( “craiceann geal” fágtha ar lár san
 *  abairt = 0)" (2014 Higher A 2(b)(ii)): what an answer is worth without a word, at a bare 0. */
const NOTE = /\(([^()]*=\s*(?:\d+\s*m?h?arc|0(?=\s*\)))[^()]*)\)/g;
/** "An chéad phointe eolais atá ceart", "an dara húsáid atá ceart", and the first rule as 2017 Ordinary Reading B 3(b) prints
 *  it, "Fáth amháin atá ceart = 3 mharc; an dara fáth atá ceart = 2 mharc". */
const RULE = /^(?:(?:an\s+)?(?:chéad|dara|tríú|ceathrú)\s.*\s|[A-ZÁÉÍÓÚa-záéíóú]+ amháin atá\s)(?:ceart|cheart)$/i;
/** "Aon dá cheann de na rudaí ón liosta thíos = 3 mharc + 2 mharc", "2 cheann ón liosta = 3 mharc + 2 mharc" (2017 Ordinary
 *  Reading A 2(a), A 5(b), B 5(b)), "Dhá phíosa eolais ag teastáil = 3 mharc + 2 mharc" (2014 Ordinary Reading A 3(b)): how the
 *  list after it is priced, a rule, never an answer. */
const LIST_RULE = /^(?:Aon\s+)?(?:dá|dhá|\d+)\s+cheann\b[^•=]*\bliosta\b|^Dhá (?:phointe|phíosa) eolais ag teastáil$/i;
/** "2 phointe ag teastáil = 3 mharc + 2 mharc", "Dhá chúis = 3 mharc + 2 mharc" (2015 Ordinary Reading A 3(a), A 5(a)): how many
 *  points the part wants and how they are priced, a rule as LIST_RULE's line is, never an answer. */
const COUNT_RULE = /^(?:dá|dhá|\d+)\s+(?:phointe(?:\s+ag teastáil)?|chúis)$/i;
/** "Gan ach cúis cheart amháin luaite, bronn 3 mharc uirthi.", "Ceann amháin den dá rud (leictreachas nó teas) i gceart, bronn 2
 *  mharc air" (2015 Ordinary Reading A 4(a), A 5(a); Cluastuiscint Comhrá 1): what a partial answer earns, said as an instruction
 *  to the examiner after the answers, a direction as "(Má fhágtar … is fiú 3 mharc an freagra.)" is (2017 Ordinary A 3(b)).
 *  "Bronn 3 mharc ar an gcéad phointe atá ceart agus 2 mharc ar an dara pointe atá ceart" (A 3(a)): the ladder said again. */
const AWARD_RULE = /(?<=^|\s)(?:(?:Gan ach|Ceann amháin)\s[^•=]*?,\s*bronn\s+\d+\s*m?h?arc\s+(?:air|uirthi)\b\.?|Bronn\s+\d+\s*m?h?arc ar an gcéad [^•=+]*?(?:ceart|cheart)\s+agus\s+\d+\s*m?h?arc ar an dara [^•=+]*?(?:ceart|cheart)\b\.?)/gi;
/** "Dhá phointe eolais as an liosta seo = 3 mharc + 2 mharc = 5 mharc", "Na pointí seo a leanas:" (2016 Ordinary): the scheme's
 *  heading over a list of accepted points, not one of them. So are "Dhá cheann as na critéir seo a leanas:", "Rud amháin as na
 *  rudaí seo a leanas:" and "An dá phointe eolais seo:" (2015 Higher A 3(a), A 3(b)(i), B 2(a)). */
const DIRECTION = /^(?:Bainfear\b|Glacfar\b|Ní mór\b|Gearrfar\b|Tabharfar\b|Tá .* mharc ag gabháil\b|Dhá (?:phointe|phíosa) eolais as an liosta seo\b|Na pointí seo a leanas\b|[^•=]{1,60}\bseo a leanas:$|An dá phointe eolais seo:$|Dhá rud as na rudaí seo a leanas\b|Dhá phíosa eolais as na pointí seo a leanas\b|Dhá phíosa eolais$|Rud amháin as na rudaí seo a leanas\b)/i;
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

interface Draft { prompt?: string; tariff: number; ladder?: number[]; rows: { text: string; marks?: number; steps?: number[] }[]; ruled?: number[]; unprinted?: boolean }

/** A reviewed card's criterion carries its own sub-question first, then lines that are not its answers:
 *  the scheme's "Nóta: …" for the part ("Má tá dhá phointe eolais i gceist, tá 3 mharc …"), which is an
 *  examiner direction, and the tariff summary for the whole section ("Freagair Léamhthuiscint A agus
 *  Léamhthuiscint B. Tá Ceist 1 – 5 ar cómharc, 7 marc …") or the card's note on an order-dependent
 *  award, which the part's own tariff and ladder already show. None of their prices is this part's. */
const PART_NOTE = /^Nóta:/;
/** A listening card's criterion (its questionRef names the section): its key prints one answer line per question. */
const LISTENING = /\bCluastuiscint\b/;
const SECTION_SUMMARY = /^(?:Freagair Léamhthuiscint|Tá Ceist \d+\s*[–-]\s*\d+ ar cómharc|Order-dependent award)/;
/** "(Is leor aon trí cinn as na ceithre cinn: …)", "(Ní mór ‘…’ a bheith sa fhreagra chun an dara marc a
 *  ghnóthú)", "(Tá gá le ‘conradh’ … a lua sa fhreagra chun an dá mharc a bhronnadh.)", "(Má fhágtar ainmfhocal nó aidiacht
 *  amháin ar lár is fiú 3 mharc an freagra.)" (2017 Ordinary Reading A 3(b)), "(Tá an dá rud - … ag teastáil chun 5 mharc a bhronnadh
 *  ar an bhfreagra.)" (2016 Ordinary B 5(a)), "(Tá an dara habairt inghlactha mar phointe eolais má bhíonn an chéad phointe leis. …)"
 *  (2015 Higher B 2(a)) after an answer: how much of it suffices, what it must contain or what it is worth
 *  without a word, a direction. */
const SUFFICES = /\((?:Is leor|aon|Ní mór|Tá gá le|Má fhágtar|Tá an dá rud|Tá an dara habairt|Cealú anseo)\s[^()]*(?:\([^()]*\)[^()]*)*\)/g;
/** "… nó áitiúla = 1 mharc (gan ‘in 2024’ sa fhreagra)", "… = 2 mharc (Gan ainmneacha an dá thír luaite, …)": the qualifier is the condition of the answer it
 *  follows, as "= 0 marc (gá le cáiliú)" (2018 Higher B 1(b)(ii)) and "… @ gaelscoileanna.ie = 2 mharc ( seoladh ceart
 *  riachtanach)" (2013 Higher Fógra a hAon 3) are. It stays on that row, as a second slice: "… nó áitiúla: (gan ‘in 2024’ sa
 *  fhreagra) · 1m". */
const QUALIFIED_PRICE = /\s*(=\s*\d+\s*m?h?arc\b)\s*(\((?:[Gg]an|gá le)\s[^()=]*\)|\(\s*[^()=]*\briachtanach\))/g;
/** "… in áit faoi leith (2 mharc) in imeacht tréimhse áirithe ama (1 mharc) = 3 mharc" (2020 Higher A 1(a)): one answer
 *  printing how its own price divides. Where the bracketed prices add up to the price after them they are part of the
 *  answer's text, not tariffs: a word joiner (U+2060) holds each one together until the rows are cut, then goes. */
const INLINE_SPLIT = /(?:[^•=()]*\(\d+\s*m?h?arc\)){2,}[^•=()]*(?==\s*(\d+)\s*m?h?arc\b)/g;
const HELD = '\u2060';
/** "{2 mharc} • D’ísligh sé an cíos (1 mharc) agus dháil sé bia … (1 mharc)" (2019 Higher A 2(b)(i)): the part's one answer
 *  printing how its price divides, with no price after it. Where the bracketed prices add up to the brace they are the
 *  answer's text, held as INLINE_SPLIT holds them, and the brace prices the answer. */
const BRACED_SPLIT = /(\{(\d+)\s*m?h?arc\}\s*•\s*)((?:[^•=(){}]*\(\d+\s*m?h?arc\)){2,}[^•=(){}]*?)\s*$/;
/** "Gálaí = 1m + cáiliú (móra) = 1 mharc" (2013 Higher Comhrá a Dó, An Chéad Mhír 1(b)): one answer, its noun at the first
 *  price and its printed qualifier at the second. The answer is one row at their sum, "Gálaí: cáiliú (móra)" (two slices of
 *  the print), that steps through the noun's price (0/1/2); an invisible separator (U+2063) marks the row until the rows are
 *  cut, then goes. */
const NOUN_AND_QUALIFIER = /([^=•]+?)\s*=\s*(\d+)m\s*\+\s*(cáiliú\s*\([^()=]*\))\s*=\s*(\d+)\s*m?h?arc\b/g;
const STEPPED = '\u2063';
/** "• Na pobail Ghaeltachta (1 mharc) + Gaeilgeoirí (ar fud na tíre) (1 mharc)" (2013 Higher Léamhthuiscint B 2(b)(ii)): one
 *  bullet printing the two answers a "{2 mharc, 1 mharc+1 mharc}" part asks for, each at its bracketed price: two answers. */
const PRICED_PAIR = /•\s*([^•()=+]+?)\s*\(\s*(\d+)\s*m?h?arc\s*\)\s*\+\s*([^•=+]+?)\s*\(\s*(\d+)\s*m?h?arc\s*\)(?=\s*(?:•|$))/g;
/** A deficient answer's bracketed price (2013 Higher Léamhthuiscint): "(1 mharc) (easnamhach)", "( 2- 1 mharc=1 mharc
 *  easnamhach)", "(2-1 mharc=1 mharc) (easnamhach)". The answer is worth the price after its "="; "easnamhach" stays on the row
 *  as its qualifier: "…: (easnamhach) · 1m". */
const DEFICIENT_PRICE = /\s*\(\s*(?:\d+\s*-\s*\d+\s*m?h?arc\s*=\s*)?(\d+)\s*m?h?arc\s*(?:easnamhach\s*\)|\)\s*\(easnamhach\))/g;
/** "• Níor thaitin an fhoghlaim fhoirmiúil leis. (2 mharc)", "{2mharc} Bíonn siad ag caint … in Sydney. (2 mharc)" (2013 Higher
 *  Léamhthuiscint): an answer's price printed in brackets after it, closing the answer (before the next bullet, brace or
 *  sub-question, or at the end). It reads as the answer's "= 2 mharc". An answer that prints another bracketed price inside it
 *  ("… againn (2 mharc) le tabhairt … (1 mharc)", 2018 Higher B 1(a)) is not one. */
const CLOSING_PRICE = /(?<=[•}][^•={}]*?)(?<!\(\s*\d+\s*m?h?arc\s*\)[^•={}]*?)\s*\(\s*(\d+)\s*m?h?arc\s*\)(?=\s*(?:•|$|\{|\((?:i|ii|iii|[b-d])\)\s))/g;
/** "( 3 mharc- 2 mharc + 1 mharc)" (2013 Higher Léamhthuiscint A 6(a)): the part's tariff and how it divides, in brackets: the
 *  brace "{3 mharc: 2 mharc + 1 mharc}" where the split adds up to the tariff. */
/** "{2 mharc} (pointe amháin)", "{3 mharc, 2 mharc +1 mharc } ( Iolra atá i gceist = 2 phointe)" (2013 Higher Léamhthuiscint A
 *  3(b)(ii), 5(a)): what the part asks for, printed after its tariff instead of before it ("(Alt 1) (pointe amháin) {2mharc}",
 *  A 1(b)(i)). It is a direction: the sub-question's prompt stays the printed line it ends ("… (Alt 3)"). */
const BRACE_NOTE = /(\{[^{}]*\})\s*(\(\s*(?:[Pp]ointe amháin|Iolra atá i gceist\s*=\s*\d+\s*phointe)\s*\))/g;
/** "• gan Twitter a úsáid. (2 mharc+1 mharc)" (2013 Higher Léamhthuiscint A 1(a)): the part's split said again in brackets after
 *  its last answer. The brackets go; the split is read as the bare sum it restates. */
const BRACKETED_SPLIT = /\(\s*(\d+\s*m?h?arc\s*\+\s*\d+\s*m?h?arc)\s*\)(?=\s*(?:•|$))/g;
const BRACKETED_TARIFF = /\(\s*(\d+)\s*(m?h?arc)\s*-\s*(\d+\s*m?h?arc\s*\+\s*\d+\s*m?h?arc)\s*\)/g;
/** A sub-question's printed opening: its number, letter or both ("3. ", "(b) ", "3 (a) ", "2. (a) "). */
const ASKED = /^(?:\d{1,2}\.?\s+(?:\([a-z]\)\s+)?|\([a-z]\)\s+)(?=[A-ZÁÉÍÓÚ])/;

/** "Báisteach/fearthainn = 2 mharc (báisteach/fearthainn throm = 3 mharc)" (2019 Ordinary Fógra a Dó 2(a)): a bracketed answer
 *  at its own single price, printed straight after another answer's price, is one more answer, not a note. A bracketed
 *  direction or qualifier ("(Is leor …", "(Ní mór …", "(Gan …", "(Tá gá le …") is never an answer. */
const BRACKETED_ANSWER = /(=\s*\d+\s*m?h?arc\b)\s*\((?!\s*(?:Is leor|aon|Ní mór|[Gg]an|Tá gá le)\s)([^()=+:]+?)\s*(=\s*\d+\s*m?h?arc\b)\)/g;

/** Whether a line is the card's printed question, read past the paper's hyphens and spacing. */
const letters = (value: string) => value.toLowerCase().replace(/[^a-záéíóú]+/g, '');
const printedQuestion = (questionText: string, line: string) => letters(line).length > 12 && letters(questionText).includes(letters(line));

/** The 2012 Higher reading key (scheme PDF 17–21) prints no tariff for most parts (its section rule prices each (a) at 3 and each
 *  (b) question at 2) and its prices in a short unit, wherever the line ends: "An Peantatlan agus an Deacatlan =3m.", "… leis
 *  féin=(3-1)=2m.", "“…” = (3-1 marc)", "“…” 3m", "“…”2m", "… S1= 1m", "“…”1+1m" (one answer giving both points), "T1 + S1 (5m) =",
 *  "Má leantar … =(3-1) iomarcach.", "“…”(3-1m),freagra easnamhach." A part is read only where its text prints that unit
 *  ("\d m") and no "= N mharc" price. Its prompt runs to the question's "?" (and its "(Alt N)" and printed "(N mharc)"), or, where
 *  the scheme reprints the question without one, to the first quoted answer, bracket or printed tariff; each price closes the
 *  answer before it. The examiner's rules are directions: "Ní fiú marc …", "Caithfidh …", "Ná cuir pionós faoi dhó …", "Léirithe
 *  mar seo: C=2m …", "(glac le …)", "mion bhriseadh le léiriú mar seo"; a deduction for an answer not turned into the third person,
 *  "(3-1m) mura bhfuil an 3ú pearsa ann.", "Gan an 3ú pearsa (2-1m)", is a direction too, and every answer at the part's tariff
 *  steps through it (0/2/3, 0/1/2). "[Bronn 2 mharc ar an gcéad cheann atá ceart agus 1 mharc ar an dara ceann.]" and "Bronn 2m ar an
 *  gcéad ceann …" ladder the two grammar answers (6(a)), each opened by its label ("Ainmfhocal …", "Briathar saor …"). Answers the
 *  scheme prints with no price are each one answer at the part's tariff, split at their quotation marks; words printed after an
 *  answer's price that continue its quotation ("“sláinte agus áilleacht an choirp “ 1+1m agus cosaint an dúlra.”") stay with it, after
 *  a colon where the price was. */
const UNIT_PRICE: [RegExp, (m: RegExpExecArray) => { marks: number; steps?: number[]; qualifier?: string } | undefined][] = [
  [/=\s*\((\d)\s*-\s*(\d)\)\s*=\s*(\d)\s*m\b\.?/y, m => (Number(m[1]) - Number(m[2]) === Number(m[3]) ? { marks: Number(m[3]) } : undefined)],
  [/=\s*\(\s*(\d)\s*-\s*(\d)\s*marc\s*\)\.?/y, m => ({ marks: Number(m[1]) - Number(m[2]) })],
  [/=\s*\((\d)\s*-\s*(\d)\)\s*(iomarcach)\.?/y, m => ({ marks: Number(m[1]) - Number(m[2]), qualifier: m[3] })],
  [/\((\d)\s*-\s*(\d)\s*m\)\s*,?\s*(freagra easnamhach)\.?/y, m => ({ marks: Number(m[1]) - Number(m[2]), qualifier: m[3] })],
  [/\((\d)\s*-\s*(\d)\s*m\)\.?/y, m => ({ marks: Number(m[1]) - Number(m[2]) })],
  [/(\d)\s*\+\s*(\d)\s*m\b\.?/y, m => ({ marks: Number(m[1]) + Number(m[2]), steps: [0, Number(m[1]), Number(m[1]) + Number(m[2])] })],
  [/\((\d+)\s*m\)\s*=/y, m => ({ marks: Number(m[1]) })],
  [/=?\s*(\d+)\s*m\b\.?/y, m => ({ marks: Number(m[1]) })],
];
const UNIT_RULES: [RegExp, 'direction' | 'deduction' | 'ladder'][] = [
  [/\[Bronn (\d) mharc ar an gcéad cheann atá ceart agus (\d) mharc ar an dara ceann\.\]/, 'ladder'],
  [/Bronn (\d)m ar an gcéad ceann atá ceart agus (\d)m ar an dara ceann\./, 'ladder'],
  [/\((\d)\s*-\s*(\d)\s*m\)\s*(?:mura|muna)\s+bhfuil an 3ú pearsa ann\.?/, 'deduction'],
  [/Gan an 3ú pearsa \((\d)\s*-\s*(\d)\s*m\)/, 'deduction'],
  [/Ní fiú marc ar bith[^.]*\./, 'direction'],
  [/Caithfidh [^.]*?(?:\.|\b0m\b)/, 'direction'],
  [/Ná cuir pionós faoi dhó ar an bhfreagra céanna\./, 'direction'],
  [/Léirithe mar seo:[^.]*\./, 'direction'],
  [/\(glac le [^)]*\)/, 'direction'],
  [/mion bhriseadh le léiriú mar seo,?/, 'direction'],
];
const parseUnitReading = (text: string, total: number): IrishAnswerResult | undefined => {
  const directions: string[] = [];
  const ladderTerms: number[] = [];
  const deductions: [number, number][] = [];
  let body = text;
  for (const [rule, kind] of UNIT_RULES) {
    for (let match = rule.exec(body); match; match = rule.exec(body)) {
      directions.push(tidy(match[0]));
      if (kind === 'ladder') ladderTerms.splice(0, ladderTerms.length, Number(match[1]), Number(match[2]));
      if (kind === 'deduction') deductions.push([Number(match[1]), Number(match[2])]);
      body = `${body.slice(0, match.index)} ${body.slice(match.index + match[0].length)}`;
    }
  }
  body = body.replace(/\s+/g, ' ').trim();
  // The prompt: after its printed label ("1 (b) (1) ", "6.(a) "), to the question's "?", or, where the scheme reprints the question
  // without one, to the first quotation mark, bracket, tariff or grammar label.
  const label = /^\d\s*\.?\s*\(\s*[a-b]\s*\)\s*(?:\(\s*\d\s*\)\s*)?/.exec(body);
  if (!label) return { ok: false, reason: 'no part label' };
  const asked = body.slice(label[0].length);
  const question = asked.indexOf('?');
  const firstAnswer = asked.search(/[“"[]|\(\d+\s*m?h?arc\)|\b\d+\s*m?h?arc\b|\(\d\)\s|(?<=\s)(?:Ainmfhocal|Briathar saor)\b/);
  let cut = label[0].length + (question >= 0 ? question + 1 : firstAnswer);
  if (question < 0 && firstAnswer <= 0) return { ok: false, reason: 'no prompt' };
  const trailer = /^\s*(?:\(\s*Alt\s*\d+\s*\))?/.exec(body.slice(cut))!;
  cut += trailer[0].length;
  const prompt = tidy(body.slice(0, cut));
  let rest = body.slice(cut);
  // The part's printed tariff and its split ("(3 mharc)", "(2 mharc) (1+1) Dhá rud.", "(3 mharc)(2+1 marc)", "10 mharc,").
  const printed = /^\s*\(?\s*(\d+)\s*m?h?arc\)?\s*,?/.exec(rest);
  if (printed) {
    if (Number(printed[1]) !== total) return { ok: false, reason: `printed tariff ${printed[1]}, criterion is ${total}` };
    rest = rest.slice(printed[0].length);
  }
  const split = /^\s*\((\d)\s*\+\s*(\d)\s*(?:marc)?\)\s*(?:(Dhá rud\.))?/.exec(rest);
  if (split) {
    if (split[3]) directions.push(tidy(split[0]));
    else if (!ladderTerms.length) ladderTerms.push(Number(split[1]), Number(split[2]));
    rest = rest.slice(split[0].length);
  }
  const rows: { text: string; marks: number; steps?: number[] }[] = [];
  if (ladderTerms.length) {
    // Grammar: the two answers, each opened by its printed label, claimed in order.
    if (ladderTerms[0] + ladderTerms[1] !== total) return { ok: false, reason: 'ladder does not reach the tariff' };
    const answers = rest.split(/(?=\b(?:Ainmfhocal|Briathar saor)\b)/).map(tidy).filter(Boolean);
    if (answers.length !== 2) return { ok: false, reason: 'grammar answers' };
    answers.forEach(answer => rows.push({ text: answer, marks: 0 }));
    return { ok: true, allocation: { parts: [{ id: 'p1', prompt, tariff: total, ladder: cumulative(ladderTerms),
      rows: rows.map((row, index) => ({ id: `r${index + 1}`, text: row.text, marks: row.marks })) }], directions } };
  }
  let pos = 0;
  while (pos < rest.length) {
    let best: { at: number; end: number; price: { marks: number; steps?: number[]; qualifier?: string } } | undefined;
    for (let at = pos; at < rest.length && !best; at++) {
      for (const [pattern, read] of UNIT_PRICE) {
        pattern.lastIndex = at;
        const match = pattern.exec(rest);
        const price = match && read(match);
        if (match && price) { best = { at, end: at + match[0].length, price }; break; }
      }
    }
    if (!best) break;
    const answer = tidy(rest.slice(pos, best.at).replace(/=\s*$/, ''));
    if (!answer) return { ok: false, reason: 'price without an answer' };
    rows.push({ text: best.price.qualifier ? `${answer}: ${best.price.qualifier}` : answer, marks: best.price.marks,
      ...(best.price.steps ? { steps: best.price.steps } : {}) });
    pos = best.end;
  }
  const tail = tidy(rest.slice(pos));
  if (tail && rows.length && /^[a-záéíóú]/.test(tail)) {
    rows[rows.length - 1].text = `${rows[rows.length - 1].text}: ${tail}`;
  } else if (tail) {
    if (rows.length) return { ok: false, reason: `unpriced answers after priced ones: ${tail.slice(0, 40)}` };
    tail.split(/(?<=”\.?)\s+(?=“)/).map(tidy).filter(Boolean).forEach(answer => rows.push({ text: answer, marks: total }));
  }
  if (!rows.length) return { ok: false, reason: 'no answers' };
  const max = Math.max(...rows.map(row => row.marks));
  if (max > total) return { ok: false, reason: 'row above its tariff' };
  if (max < total && rows.filter(row => row.marks > 0).reduce((sum, row) => sum + row.marks, 0) < total) return { ok: false, reason: 'tariff not reachable' };
  for (const [base, minus] of deductions) {
    for (const row of rows) if (row.marks === base && base === total && !row.steps) row.steps = [0, base - minus, base];
  }
  return { ok: true, allocation: { parts: [{ id: 'p1', prompt, tariff: total,
    rows: rows.map((row, index) => ({ id: `r${index + 1}`, text: row.text, marks: row.marks, ...(row.steps ? { steps: row.steps } : {}) })) }], directions } };
};

/** The 2011 Higher reading key (Páipéar 1, scheme PDF 5–14) restates each part with its tariff and the split its marks take:
 *  "1 (a) Cén taithí a bhí ag an údar ar an bPolainn? (Alt 1) (3 mharc) (2+1)" is Eolas 2 + Ionramháil 1 (its rule, PDF 5:
 *  "Eolas + Ionramháil: 2 + 1 = 2 marc ar eolas cruinn + 1 marc ar ionramháil"), "(4 mharc) (2+1+1)" is P1 + P2 + Ionramháil
 *  (PDF 6: "4 marc ar an bhfreagra: 2 marc + 1 marc + 1 marc P1 + P2 + Ionramháil"), "Pointe amháin(2+1)" one point and its
 *  Ionramháil, "3 mharc gan ionramháil" one answer at 3, "(2+1+1) (Eachtra+Míniú+Ionramháil)" each term named. A reviewed card
 *  prices each term as a criterion of its own and carries the restated part, then the key's lines for that term one to a line;
 *  where the key heads a term itself ("Dhá thréith =1+1 (gan ionramháil)", "2 mharc gan ionramháil=céard is bun leis na
 *  tréithe", "(Eachtra=2 mharc)", "Míniú = 1 mharc"), that heading prices the criterion. A line is:
 *  - a note: wholly in brackets with no price ("(Cáiliú amháin ag teastáil …)"), or the key's heading or rule ("Dhá chuid san
 *    eachtra:", "Míniú: Pointe eolais amháin = 2 mharc", "Gan an eachtra cheart …"): a direction;
 *  - an answer priced where it is printed ("= 3 mharc", "= 3 - 1 = 2 mharc", "= 1 + 1 = 2 mharc", "= 0", a sentence of two
 *    points "(Dhá phointe eolais san abairt seo = 2 + 1)"): a row at that price, stepped at its printed split;
 *  - an answer quoted from the passage and not priced: a row at the term's price (on two points, a rung of the P1 + P2 ladder;
 *    under "=1+1", stepped one trait at a time), unless rows printed beside it at prices add up to the term (2A 5(b)'s eachtra,
 *    "= 1 mharc" + "= 1 mharc"): then it is the passage's own account of them, a sample;
 *  - the same answer in other words, not quoted ("Chaith sé mí/tamall sa Pholainn …"): a sample;
 *  - on the Ionramháil criterion, the rule "Is ionann “ionramháil” agus …" is its one row and the rules after it directions.
 *  Read only where the first line is a restated part ending at its split, or a term's own heading; anything else is not this
 *  key. Nothing is added: rows, samples and directions are the key's lines as printed. */
/** The restated part: its words to its tariff, then the split ("(Alt 2)" is not always restated; A 3(b) prints no tariff). */
const SPLIT_PART = /^\d\s*\(\s*[ab]\s*\)\s*(.+?)\s*(?:\(\s*(\d)\s*m?h?arc\s*\)\s*(.*))?$/;
const SPLIT_TERMS = /^(?:Pointe amháin\s*)?\(\s*(\d)\s*\+\s*(\d)(?:\s*\+\s*(\d))?\s*\)(?:\s*\((Eachtra)\s*\+\s*(Míniú)\s*\+\s*Ionramháil\s*\))?$/;
const SPLIT_PLAIN = /^\(?\s*(\d)\s*m?h?arc\s*\)?\s*gan ionramháil\s*\)?$/;
const SPLIT_PAIR = /^\(\s*(\d)\s*\+\s*(\d)\s*\)\s*gan ionramháil\.?$/;
/** The 2010 Higher key (scheme PDF 7–13) prints a split with no Ionramháil mark three ways: "(2 phíosa eolais gan ionramháil)
 *  (2 + 2)", "(2 + 2) (Gan ionramháil)" and "(2 + 2 gan ionramháil)", two points at 2 each; and once (2B 2(a)) "(2 + 1) (Gan
 *  ionramháil)", a split whose terms it does not name. Two equal terms are two points, each quoted answer one point at its
 *  term; two unequal terms are one answer at their sum that steps at the first, as the key splits it. Under two points the key
 *  notes a sentence "(2 phíosa eolais san abairt seo)": that sentence alone gives both, stepped one point at a time. */
const SPLIT_UNMANIPULATED = /^(?:\(\s*2 phíosa eolais gan ionramháil\s*\)\s*\(\s*(\d)\s*\+\s*(\d)\s*\)|\(\s*(\d)\s*\+\s*(\d)\s*\)\s*\(\s*Gan ionramháil\s*\)|\(\s*(\d)\s*\+\s*(\d)\s*gan ionramháil\s*\))$/;
const SPLIT_COUNT = /\s*\(2 phíosa eolais san abairt seo\)$/;
/** A point the key gives only in other words, numbered as its quotations are: "(i) D’éirigh an t-údar níos tanaí …". */
const SPLIT_NUMBERED = /^\((?:i|ii|iii|iv|v|vi|vii|viii|ix|x|xi|xii)\)\s/;
const SPLIT_HEADS: [RegExp, (match: RegExpExecArray) => { prompt: string; tariff: number; steps?: number[] }][] = [
  [/^(Dhá thréith)\s*=\s*(\d)\s*\+\s*(\d)\s*\(gan ionramháil\)$/, match => ({ prompt: match[1], tariff: Number(match[2]) + Number(match[3]),
    steps: [0, Number(match[2]), Number(match[2]) + Number(match[3])] })],
  [/^(\d)\s*mharc gan ionramháil\s*=\s*(.+)$/, match => ({ prompt: match[2], tariff: Number(match[1]) })],
  [/^\((Eachtra|Míniú)\s*=\s*(\d)\s*mharc\)$/, match => ({ prompt: match[1], tariff: Number(match[2]) })],
  [/^(Míniú)\s*=\s*(\d)\s*mharc$/, match => ({ prompt: match[1], tariff: Number(match[2]) })],
];
const SPLIT_NOTE = /^(?:\([^()=]*\)|Dhá chuid\s[^=]*:|Míniú:\s.*|Gan an\s.*)$/;
const SPLIT_IONRAMHAIL = /^Is ionann “ionramháil”/;
const SPLIT_PRICE = /\s*=\s*(?:(\d)\s*-\s*(\d)\s*=\s*|(\d)\s*\+\s*(\d)\s*=\s*|(pointe eolais amháin)\s*=\s*)?(\d)\s*mharc\b\.?\s*(\([^()]*\))?$/;
const SPLIT_ZERO = /\s*=\s*0\.?$/;
const SPLIT_POINTS = /\s*\(([^()]*=\s*(\d)\s*\+\s*(\d)\b[^()]*)\)$/;
const parseSplitReading = (source: IrishAnswerSource): IrishAnswerResult | undefined => {
  const lines = source.guidance.map(line => line.replace(/\s+/g, ' ').trim());
  const part = SPLIT_PART.exec(lines[0]);
  let prompt: string | undefined;
  let term: { tariff: number; ladder?: number[]; steps?: number[]; ionramhail?: boolean; point?: number } | undefined;
  let first = 1;
  if (part) {
    prompt = tidy(part[1]);
    const spec = (part[3] ?? '').trim();
    const terms = SPLIT_TERMS.exec(spec);
    const plain = SPLIT_PLAIN.exec(spec);
    const unmanipulated = SPLIT_UNMANIPULATED.exec(spec);
    const printed = part[2] ? Number(part[2]) : undefined;
    const head = lines[1] !== undefined ? SPLIT_HEADS.map(([rule, read]) => { const m = rule.exec(lines[1]); return m && read(m); }).find(Boolean) : undefined;
    if (head) {
      if (!SPLIT_PAIR.test(spec) && spec !== '') return { ok: false, reason: 'term heading under a split that names no terms' };
      term = { tariff: head.tariff, ...(head.steps ? { steps: head.steps } : {}) };
      first = 2;
    } else if (terms) {
      const values = [terms[1], terms[2], terms[3]].filter(Boolean).map(Number);
      if (printed !== undefined && values.reduce((a, b) => a + b, 0) !== printed) return { ok: false, reason: 'split does not add up to the part' };
      const ionramhail = lines.slice(1).some(line => SPLIT_IONRAMHAIL.test(line));
      if (ionramhail) term = { tariff: values[values.length - 1], ionramhail: true };
      else if (terms[4]) term = { tariff: values[0] };
      else if (values.length === 3) term = { tariff: values[0] + values[1], ladder: [values[0], values[0] + values[1]] };
      else term = { tariff: values[0] };
    } else if (plain) {
      if (printed !== undefined && Number(plain[1]) !== printed) return { ok: false, reason: 'split does not add up to the part' };
      term = { tariff: Number(plain[1]) };
    } else if (unmanipulated) {
      const [a, b] = unmanipulated.slice(1).filter(Boolean).map(Number);
      if (printed === undefined || a + b !== printed) return { ok: false, reason: 'split does not add up to the part' };
      term = a === b ? { tariff: a + b, point: a } : { tariff: a + b, steps: [0, a, a + b] };
    } else return undefined;
  } else {
    const head = SPLIT_HEADS.map(([rule, read]) => { const m = rule.exec(lines[0]); return m && read(m); }).find(Boolean);
    if (!head) return undefined;
    prompt = tidy(head.prompt);
    term = { tariff: head.tariff, ...(head.steps ? { steps: head.steps } : {}) };
  }
  if (term.tariff !== source.totalMarks) return { ok: false, reason: `term ${term.tariff}, criterion is ${source.totalMarks}` };
  const directions: string[] = [];
  if (term.ionramhail) {
    if (!SPLIT_IONRAMHAIL.test(lines[first] ?? '')) return { ok: false, reason: 'Ionramháil rule not first' };
    return { ok: true, allocation: { parts: [{ id: 'p1', ...(prompt ? { prompt } : {}), tariff: term.tariff,
      rows: [{ id: 'r1', text: tidy(lines[first]), marks: term.tariff }] }], directions: lines.slice(first + 1).map(tidy).filter(Boolean) } };
  }
  // The key's lines in print order: a priced answer is a row now; an unpriced quotation waits until the term's priced rows are
  // known (a row, or a sample beside rows that are the term's components); an unpriced line in other words is a sample.
  const items: ({ row: IrishAnswerRow } | { quoted: string } | { sample: string })[] = [];
  for (const raw of lines.slice(first)) {
    const line = /^\([^()]*=\s*0\)$/.test(raw) ? raw.slice(1, -1).trim() : raw;
    if (SPLIT_IONRAMHAIL.test(line)) return { ok: false, reason: 'Ionramháil rule on an answer term' };
    if (SPLIT_NOTE.test(line)) { directions.push(tidy(line)); continue; }
    const price = SPLIT_PRICE.exec(line);
    if (price) {
      const marks = Number(price[6]);
      const text = tidy(line.slice(0, price.index) + (price[5] ? `: ${price[5]}` : '') + (price[7] ? `: ${price[7]}` : ''));
      if (price[3] !== undefined && Number(price[3]) + Number(price[4]) !== marks) return { ok: false, reason: 'split price does not add up' };
      if (price[1] !== undefined && Number(price[1]) - Number(price[2]) !== marks) return { ok: false, reason: 'deduction does not add up' };
      if (marks > term.tariff) return { ok: false, reason: 'row above its term' };
      items.push({ row: { id: '', text, marks, ...(price[3] !== undefined ? { steps: [0, Number(price[3]), marks] } : {}) } });
      continue;
    }
    if (SPLIT_ZERO.test(line)) {
      // On a ladder an answer printed at 0 is never a rung: it is what the key refuses.
      if (term.ladder) directions.push(tidy(line));
      else items.push({ row: { id: '', text: tidy(line.replace(SPLIT_ZERO, '')), marks: 0 } });
      continue;
    }
    const count = SPLIT_COUNT.exec(line);
    if (count && term.point !== undefined && line.includes('“')) {
      items.push({ row: { id: '', text: tidy(line), marks: term.tariff, steps: [0, term.point, term.tariff] } });
      continue;
    }
    const points = SPLIT_POINTS.exec(line);
    if (/\d\s*m?h?arc\b|=/.test(points ? line.slice(0, points.index) : line)) return { ok: false, reason: `unread price: ${line.slice(0, 40)}` };
    if (points) {
      const [a, b] = [Number(points[2]), Number(points[3])];
      if (a + b !== term.tariff || !term.ladder) return { ok: false, reason: 'two points outside a two-point term' };
      items.push({ row: { id: '', text: tidy(line), marks: a + b, steps: [0, a, a + b] } });
      continue;
    }
    items.push(line.includes('“') ? { quoted: tidy(line) } : { sample: tidy(line) });
  }
  const priced = items.flatMap(item => ('row' in item ? [item.row] : []));
  const quoted = items.some(item => 'quoted' in item);
  // Rows printed at prices that add up to the term, each below it, are its components (1 + 1 for an eachtra of two parts).
  const components = priced.length > 1 && priced.reduce((sum, row) => sum + row.marks, 0) === term.tariff && priced.every(row => row.marks < term.tariff);
  // Two-point sentences priced in the key ("= 2 + 1") are claimed at their own steps, never as rungs of the P1 + P2 ladder.
  if (term.ladder && priced.some(row => row.marks > 0)) {
    if (quoted) return { ok: false, reason: 'unpriced answers beside priced points' };
    delete term.ladder;
  }
  // 2A 5(b) (2010, scheme PDF 10) quotes one sentence for its two points and numbers the points only in other words, "(i)
  // D’éirigh an t-údar níos tanaí …", "(ii) Mhothaigh sé …": where the quotations are fewer than the ladder's rungs, the
  // numbered points are its rows and the quotation their sample.
  const numbered = items.filter(item => 'sample' in item && SPLIT_NUMBERED.test(item.sample)).length;
  const pointsAsRows = term.ladder !== undefined && !priced.length && items.filter(item => 'quoted' in item).length < term.ladder.length
    && numbered >= term.ladder.length;
  const rows: IrishAnswerRow[] = [];
  const samples: string[] = [];
  for (const item of items) {
    if ('row' in item) rows.push(item.row);
    else if (pointsAsRows && 'sample' in item && SPLIT_NUMBERED.test(item.sample)) rows.push({ id: '', text: item.sample, marks: 0 });
    else if (pointsAsRows && 'quoted' in item) samples.push(item.quoted);
    else if ('sample' in item || components) samples.push('sample' in item ? item.sample : item.quoted);
    else rows.push({ id: '', text: item.quoted, marks: term.ladder ? 0 : term.point ?? term.tariff, ...(term.steps ? { steps: term.steps } : {}) });
  }
  if (!rows.length) return { ok: false, reason: 'no answers' };
  const points = term.point !== undefined && rows.filter(row => row.marks === term.point).length * term.point >= term.tariff;
  if (!term.ladder && !components && !points && !rows.some(row => row.steps) && Math.max(...rows.map(row => row.marks)) < term.tariff) {
    return { ok: false, reason: 'tariff not reachable' };
  }
  return { ok: true, allocation: { parts: [{ id: 'p1', ...(prompt ? { prompt } : {}), tariff: term.tariff, ...(term.ladder ? { ladder: term.ladder } : {}),
    rows: rows.map((row, index) => ({ ...row, id: `r${index + 1}` })), ...(samples.length ? { samples } : {}) }], directions } };
};

/** The 2010 Higher listening key (scheme PDF 20–25) restates each question after its printed number, then prints its answers as
 *  bullets priced with the unit "m": "1 (a) Cén cumann atá ag eagrú na siúlóide seo? • Cumann Ailse na hÉireann = 2m • Ailse =
 *  1m." Each priced answer is a row at its price, a refused one at 0 ("• Cártaí leis féin = 0m"). A bullet can print two answers
 *  at their prices ("Idirbhliain = 2m / Eatramhach = 2m", "Searmanas = 2m cuimhneacháin = 2m"), each a row; an answer and its
 *  qualifier each at a price ("Siopaí = 1m + cáiliú = 1m (de gach saghas)") are one row at their sum that steps through the
 *  noun's price, as NOUN_AND_QUALIFIER reads the 2013 key's "Gálaí = 1m + cáiliú (móra)": "Siopaí: cáiliú: (de gach saghas)",
 *  three slices of the print. A bracket printed after a price ("= 2m (cruinneas riachtanach)", "= 1m (ná glac le orr/oir.)")
 *  is that answer's condition and stays on its row after a colon, as QUALIFIED_PRICE keeps one. Read only on a listening criterion with one guidance line, its question number and "?" or "."
 *  before the first bullet, every bullet priced "= Nm" and no "marc" anywhere: no other key prints that shape. */
const BULLET_PRICE = /=\s*(\d)\s*m\b\.?/g;
const parseBulletListening = (source: IrishAnswerSource): IrishAnswerResult | undefined => {
  if (!LISTENING.test(source.questionRef) || source.guidance.length !== 1) return undefined;
  const text = source.guidance[0].replace(/\s+/g, ' ').trim();
  if (/\d\s*m?h?arc\b/.test(text) || !/=\s*\d\s*m\b/.test(text)) return undefined;
  const [lead, ...bullets] = text.split('•').map(piece => piece.trim());
  if (!bullets.length || !ASKED.test(lead) || !/[?.]$/.test(lead)) return undefined;
  const rows: { text: string; marks: number; steps?: number[] }[] = [];
  for (const bullet of bullets) {
    const prices = [...bullet.matchAll(BULLET_PRICE)];
    if (!prices.length) return { ok: false, reason: 'unpriced bullet' };
    let pos = 0;
    for (const price of prices) {
      const answer = tidy(tidy(bullet.slice(pos, price.index)).replace(/^\//, ''));
      pos = price.index! + price[0].length;
      const marks = Number(price[1]);
      const last = rows[rows.length - 1];
      if (/^\+\s*cáiliú$/.test(answer) && last && pos > price[0].length && !last.steps) {
        rows[rows.length - 1] = { text: `${last.text}: ${tidy(answer.slice(1))}`, marks: last.marks + marks, steps: [0, last.marks, last.marks + marks] };
        continue;
      }
      if (!answer || /^\(.*\)$/.test(answer) || answer.startsWith('+')) return { ok: false, reason: 'price without an answer' };
      rows.push({ text: answer, marks });
    }
    const tail = tidy(bullet.slice(pos));
    if (tail && !/^\(.*\)$/.test(tail)) return { ok: false, reason: `unpriced text after a price: ${tail.slice(0, 40)}` };
    if (tail) rows[rows.length - 1].text += `: ${tail}`;
  }
  const max = Math.max(...rows.map(row => row.marks));
  if (max > source.totalMarks) return { ok: false, reason: 'row above its tariff' };
  if (max < source.totalMarks && rows.reduce((sum, row) => sum + row.marks, 0) < source.totalMarks) return { ok: false, reason: 'tariff not reachable' };
  return { ok: true, allocation: { parts: [{ id: 'p1', prompt: tidy(lead), tariff: source.totalMarks,
    rows: rows.map((row, index) => ({ id: `r${index + 1}`, text: row.text, marks: row.marks, ...(row.steps ? { steps: row.steps } : {}) })) }], directions: [] } };
};

/** Cut one criterion's exact guidance into parts and rows, or say why not. */
/** "Fógra 1: 3 marc × 4 = 12 marc" (2012 Ordinary, scheme PDF 4–5): a listening section's printed tariff. */
const SECTION_TARIFF = /^(?:Fógra|Comhrá|Píosa) \d: (\d+) m?h?arc × (\d+) = (\d+) m?h?arc$/;
/** "Fógra a hAon 4 + 2 + 6 + 2", "Comhrá a Dó 3 + 3 + 3 + 6 + 3 + 6" (2011 Ordinary listening, scheme PDF 10): an item's
 *  question tariffs in print order, with no unit. */
const ITEM_TARIFFS = /^(?:Fógra|Comhrá|Píosa) a (?:hAon|Dó|Trí) (\d+(?:\s*\+\s*\d+)+)$/;
/** "1. (a) Cad as do thuismitheoirí Evanne Ní Choileáin (b) Dhá scoil ar fhreastail sí orthu = 10 marc" (2012 Ordinary reading,
 *  scheme PDF 9; B 2 prints "= 10 mar"): what a question asks, restated, and one price for the whole question. */
const RESTATED_QUESTION = /^\d+\.\s+([^=•]+?)\s*=\s*(\d+)\s*(?:m?h?arc|mar)$/;

export function parseIrishAnswers(source: IrishAnswerSource): IrishAnswerResult {
  const directions: string[] = [];
  // The 2011 and 2012 Ordinary schemes print no listening or reading key. A listening criterion that carries its printed question
  // and its section's tariff alone, or a reading question that carries the scheme's restatement of it and its one price, is one part at
  // that price with its own words as the row, claimed whole: the scheme prints no answer to claim beyond it, and no partial.
  if (source.guidance.length === 2 && LISTENING.test(source.questionRef)) {
    const question = tidy(source.guidance[0]);
    const tariff = SECTION_TARIFF.exec(source.guidance[1].trim());
    // 2011 prints each item's tariffs as one line of addends ("Fógra a hAon 4 + 2 + 6 + 2"): the criterion's price is one of them.
    const prices = ITEM_TARIFFS.exec(source.guidance[1].trim())?.[1].match(/\d+/g)?.map(Number) ?? [];
    if (((tariff && Number(tariff[1]) === source.totalMarks && Number(tariff[1]) * Number(tariff[2]) === Number(tariff[3]))
      || prices.includes(source.totalMarks)) && !/\d+\s*m?h?arc\b/.test(question) && printedQuestion(source.questionText, question)) {
      return { ok: true, allocation: { parts: [{ id: 'p1', prompt: question, tariff: source.totalMarks,
        rows: [{ id: 'r1', text: question, marks: source.totalMarks }] }], directions: [] } };
    }
  }
  const restated = source.guidance.length === 1 && /Léamhthuiscint/.test(source.questionRef) ? RESTATED_QUESTION.exec(source.guidance[0].trim()) : null;
  if (restated && Number(restated[2]) === source.totalMarks) {
    return { ok: true, allocation: { parts: [{ id: 'p1', tariff: source.totalMarks,
      rows: [{ id: 'r1', text: tidy(restated[1]), marks: source.totalMarks }] }], directions: [] } };
  }
  if (/Léamhthuiscint/.test(source.questionRef)) {
    const split = parseSplitReading(source);
    if (split) return split;
  }
  const bulleted = parseBulletListening(source);
  if (bulleted) return bulleted;
  const ownLines = source.guidance.filter((line, index) => {
    if (index === 0) return true;
    if (SECTION_SUMMARY.test(line.trim())) return false;
    if (!PART_NOTE.test(line.trim())) return true;
    directions.push(tidy(line));
    return false;
  });
  // A SymbolMT bullet the builders have not yet repaired (U+F0B7) and a repaired one (•) cut alike.
  let text = ownLines.join(' ').split(BULLET).join(' • ').replace(/•/g, ' • ');
  if (/Léamhthuiscint/.test(source.questionRef) && /\d\s*m\b/.test(text) && !/=\s*\d+\s*m?h?arc\b/.test(text)) {
    const unit = parseUnitReading(text.replace(/\s+/g, ' ').trim(), source.totalMarks);
    if (unit) {
      if (unit.ok) unit.allocation.directions.unshift(...directions);
      return unit;
    }
  }
  const nounSteps: number[] = [];
  // The 2012 Higher listening key (scheme PDF 7–12) prints its tariffs and prices with no unit: a question's tariff in brackets
  // after it ("Cén scoil atá i gceist san fhógra seo? (2)", "… a bheith ag iarrthóirí. (2 + 2)"), each answer "= 2", "= 0",
  // "=2", "= 2m", and an answer of two printed halves, "= 1 + 1" (a start and an end, 1 each) or "= 2 + 2" (both points of a
  // two-point question), or "= 1 + 0" where only the first half is right. Read only on a listening criterion whose text prints
  // no "marc" at all, as the priced forms it stands for; an answer of two halves steps through its first (0/1/2, 0/2/4), as
  // the noun and its qualifier do. "= 1 + 09 go dtí 4.05 = 1 + 1" is "= 1 + 0" then the next answer, "9 go dtí 4.05", run
  // together where the scheme lost a line break: every price it prints is one digit.
  if (LISTENING.test(source.questionRef) && !/\d\s*m?h?arc\b/.test(text)) {
    text = text
      .replace(/([?.:])\s*\(\s*(\d)\s*\+\s*(\d)\s*\)/g, '$1 $2 mharc + $3 mharc')
      .replace(/([?.:])\s*\(\s*(\d)\s*\)/g, '$1 $2 mharc')
      .replace(/\s*=\s*(\d)\s*\+\s*(\d)/g, (_, first: string, second: string) => {
        if (Number(second) === 0) return ` = ${first} mharc `;
        nounSteps.push(Number(first));
        return `${STEPPED} = ${Number(first) + Number(second)} mharc `;
      })
      .replace(/=\s*(\d)(?:m\b)?(?!\s*m?h?arc\b)(?![\d.,])/g, '= $1 mharc');
  }
  text = text.replace(PRICED_PAIR, (_, first: string, firstPrice: string, second: string, secondPrice: string) =>
    `• ${first.trim()} = ${firstPrice} mharc • ${second.trim()} = ${secondPrice} mharc`);
  text = text.replace(DEFICIENT_PRICE, (_, price: string) => `: (easnamhach) = ${price} mharc`);
  text = text.replace(CLOSING_PRICE, (_, price: string) => ` = ${price} mharc`);
  text = text.replace(BRACE_NOTE, (_, brace: string, note: string) => { directions.push(tidy(note)); return brace; });
  text = text.replace(BRACKETED_SPLIT, ' $1 ');
  text = text.replace(BRACKETED_TARIFF, (whole: string, total: string, unit: string, split: string) =>
    ([...split.matchAll(/\d+/g)].reduce((sum, m) => sum + Number(m[0]), 0) === Number(total) ? `{${total} ${unit}: ${split}}` : whole));
  text = text.replace(QUALIFIED_PRICE, (_, price: string, qualifier: string) => `: ${qualifier} ${price}`);
  text = text.replace(INLINE_SPLIT, (answer: string, total: string) => {
    const split = [...answer.matchAll(/\((\d+)\s*m?h?arc\)/g)].reduce((sum, m) => sum + Number(m[1]), 0);
    return split === Number(total) ? answer.replace(/\((\d+)\s*(m?h?arc)\)/g, `($1${HELD}$2)`) : answer;
  });
  text = text.replace(BRACED_SPLIT, (whole: string, head: string, total: string, answer: string) => {
    const split = [...answer.matchAll(/\((\d+)\s*m?h?arc\)/g)].reduce((sum, m) => sum + Number(m[1]), 0);
    return split === Number(total) ? `${head}${answer.replace(/\((\d+)\s*(m?h?arc)\)/g, `($1${HELD}$2)`)} = ${total} mharc` : whole;
  });
  // "{3 mharc: 2 mharc + 1 mharc} An chéad phointe eolais atá ceart = 2 mharc; … • Is rud ón am atá caite í a fhágtar le huacht
  // againn (2 mharc) le tabhairt ar aghaidh do na glúine atá le teacht (1 mharc) • …" (2018 Higher B 1(a)): a laddered part's
  // answer printing each of its points at its rung, in the ladder's order. Each point is one answer the ladder counts.
  text = text.replace(/(\{(\d+)\s*m?h?arc:\s*(\d+\s*m?h?arc\b(?:\s*\+\s*\d+\s*m?h?arc\b)+)\s*\}[^•{}]*•\s*)((?:[^•=(){}]*\(\d+\s*m?h?arc\)){2,})(?=\s*•)/g,
    (whole: string, head: string, _total: string, split: string, answer: string) => {
      const rungs = [...split.matchAll(/\d+/g)].map(m => m[0]).join(' ');
      const points = [...answer.matchAll(/([^()]*?)\s*\((\d+)\s*m?h?arc\)/g)];
      return points.map(point => point[2]).join(' ') === rungs
        ? `${head}${points.map(point => `${point[1].trim()} = ${point[2]} mharc`).join(' • ')} ` : whole;
    });
  // "• Ag breathnú roimhe/roimpi ar an Debs mar shampla ( ní mór don iarrthóir an t-athrú pearsan a dhéanamh (… pionós (-1 mharc)
  // má fhágtar “romhat” sa fhreagra •" (2014 Higher B 1(a)): the examiner's note printed inside the answer's bullet, opened and
  // never closed, is a direction, never a second answer; its opening bracket goes with it.
  text = text.replace(/\(\s*(ní mór don iarrthóir\s[^•]*?)(?=\s*•)/g, (_, note: string) => { directions.push(tidy(note)); return ' '; });
  // A price printed inside the qualifier's brackets, "(gan aon cháiliú = 1 mharc)", reads as the qualified price above.
  text = text.replace(/\s*\((gan\s[^()=]*?)\s*(=\s*\d+\s*m?h?arc\b)\)/g, (_, qualifier: string, price: string) => `: (${qualifier}) ${price}`);
  // "(dhá cheann) {1 mharc + 1 mharc = 2 mharc}" (2017 Higher A 1(b)(i)): the brace prints its split before its total; it is
  // the brace "{2 mharc: 1 mharc + 1 mharc}" where the split adds up to the total.
  text = text.replace(/\{\s*(\d+\s*m?h?arc\b(?:\s*\+\s*\d+\s*m?h?arc\b)+)\s*=\s*(\d+)\s*(m?h?arc\b)\s*\}/g, (whole: string, split: string, total: string, unit: string) =>
    ([...split.matchAll(/\d+/g)].reduce((sum, m) => sum + Number(m[0]), 0) === Number(total) ? `{${total} ${unit}: ${split}}` : whole));
  // A split printed before the brace, "(Dhá bhealach: 2 mharc + 1 mharc) {3 mharc}", is the brace's own split.
  text = text.replace(/\((Dhá\s[^():]*):\s*(\d+\s*m?h?arc\b(?:\s*\+\s*\d+\s*m?h?arc\b)+)\)\s*\{\s*(\d+\s*m?h?arc\b)\s*\}/g,
    (_, label: string, split: string, total: string) => `(${label}) {${total}: ${split}}`);
  // "(Alt 1) 3 mharc: 2 mharc + 1 mharc" (2014 Higher A 1(a)): the brace "{3 mharc: 2 mharc + 1 mharc}" printed without its
  // braces, read as the brace where the split adds up to the total.
  text = text.replace(/(?<!\{\s*)\b(\d+)\s*(m?h?arc):\s*(\d+\s*m?h?arc\b(?:\s*\+\s*\d+\s*m?h?arc\b)+)/g, (whole: string, total: string, unit: string, split: string) =>
    ([...split.matchAll(/\d+/g)].reduce((sum, m) => sum + Number(m[0]), 0) === Number(total) ? `{${total} ${unit}: ${split}}` : whole));
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
  // "Cén t-ainm a bheidh ar an gclár speisialta …? Sacar an Lae = 3 mharc 3 mharc" (2014 Ordinary Fógra a Dó 1(b)): the question
  // fills its printed line, so its tariff sits at the right of the answer's line, after the answer's own price. A bare tariff
  // printed straight after an answer's price and ending that answer is the question's: it is read before the answer.
  text = text.replace(/(\?)\s+([^?•=]{1,120}?=\s*\d+\s*m?h?arc\b)\s+(\d+\s*m?h?arc\b)(?=\s*$)/, '$1 $3 $2');
  // "061 92917 3 mharc 061 (1 mharc) + 92917 (2 mharc)" (2014 Ordinary Fógra a hAon, the grid's fourth row): under an answer, its
  // parts at their own prices, adding up to the answer's. Each part is one more answer at its price.
  text = text.replace(/(\d+)\s*(m?h?arc\b)\s+([^()•=+?]{1,40}?)\s*\((\d+)\s*m?h?arc\)\s*\+\s*([^()•=+?]{1,40}?)\s*\((\d+)\s*m?h?arc\)(?=\s*$)/,
    (whole: string, price: string, unit: string, first: string, firstPrice: string, second: string, secondPrice: string) =>
      (Number(firstPrice) + Number(secondPrice) === Number(price)
        ? `${price} ${unit} • ${first.trim()} = ${firstPrice} mharc • ${second.trim()} = ${secondPrice} mharc` : whole));
  // "Dhá ábhar = 3 mharc + 2 mharc An chéad ábhar atá cruinn = 3 mharc; an dara hábhar = 2 mharc", "An chéad scoil atá cruinn =
  // 3 mharc; an dara scoil luaite agus cruinn = 2 mharc" (2014 Ordinary Reading A 3(a), A 2(b)): how a two-point answer is priced,
  // over answers that each give both points at the part's tariff. A direction, as the 2016 sentence form of the ladder is.
  text = text.replace(/(?:\bDhá\s[^=•;]{1,30}?=\s*3\s*mharc\s*\+\s*2\s*mharc\s+)?\bAn chéad\s[^=•;]{1,40}?\satá cruinn\s*=\s*3\s*mharc;\s*an dara\s[^=•;]{1,40}?=\s*2\s*mharc\b/g,
    rule => { directions.push(tidy(rule)); return ' '; });
  // A refused answer the scheme prints at a bare 0 ("Deireadh Fómhair = 0"; the grid's "T-léine 3 mharc Léine 0", 2016 Ordinary):
  // an answer at 0 marks, as "= 0 marc (gá le cáiliú)" is.
  text = text.replace(/=\s*0(?=\s*(?:•|$))/g, '= 0 marc').replace(/(\d\s*m?h?arc\s+[^•=?\d]{1,40}?)\s+0(?=\s*(?:•|$))/g, '$1 0 marc');
  // "3 mharc ar an gcéad chúis cheart + 2 mharc ar an dara cúis cheart = 5 mharc" (2016 Ordinary B 1(a)): the ladder said again
  // as a sentence, a direction. "X = 3 mharc nó 2 mharc" (A 3(b)): one point at 3 or 2 by its order, which the ladder carries.
  text = text.replace(/\b\d+\s*m?h?arc ar an gcéad [^+=•]+\+\s*\d+\s*m?h?arc ar an dara [^+=•]+=\s*\d+\s*m?h?arc\b/g, rule => { directions.push(tidy(rule)); return ' '; });
  text = text.replace(/(=\s*\d+\s*m?h?arc\b)\s+nó\s+\d+\s*m?h?arc\b/g, '$1');
  text = text.replace(NOUN_AND_QUALIFIER, (_, noun: string, first: string, qualifier: string, second: string) => {
    nounSteps.push(Number(first));
    return `${noun.trimEnd()}: ${qualifier}${STEPPED} = ${Number(first) + Number(second)} mharc`;
  });
  text = text.replace(SUFFICES, note => { directions.push(tidy(note)); return ' '; });
  text = text.replace(AWARD_RULE, rule => { directions.push(tidy(rule)); return ' '; });
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
  let headedList = false;
  const addAnswers = (segment: string, marks: number | undefined, half?: number): string | undefined => {
    const { lead, bullets } = splitBullets(segment);
    const items = lead ? [lead, ...bullets] : bullets;
    if (items.length === 0) return 'price without an answer';
    if (!current) {
      // "5. (a) Tabhair dhá phíosa eolais … (Alt 5) An chéad phointe eolais atá ceart = 3 mharc; an dara … = 2 mharc" (2016 Ordinary
      // A 5(a)): the question prints no tariff of its own, only the rules that price it. It opens at the criterion's marks, and
      // the rules ladder it as they do under a printed tariff.
      const ruled = /^(.*(?:\(Alt \d+\)|\?))\s+((?:an\s+)?(?:chéad|dara)\s.*\s(?:ceart|cheart))$/i.exec(items[0]);
      if (ruled && PROMPT.test(ruled[1]) && marks !== undefined) { open(tidy(ruled[1]), source.totalMarks); items[0] = ruled[2]; }
      // "1. (a) Cén cuairteoir tábhachtach …? (Alt 1) • an tUachtarán Kennedy … = 5 mharc" (2013 Ordinary reading): the question
      // prints no tariff of its own, only its answers' prices. It opens at the criterion's marks and its bullets are its answers.
      else if (lead && bullets.length && PROMPT.test(lead) && /\(Alt \d+\)$/.test(lead) && marks !== undefined) { open(lead, source.totalMarks); items.shift(); }
      // "(b) Luaigh rud amháin a rinne sé mar Uachtarán agus rud amháin nár éirigh leis a dhéanamh. (Alt 4) Rud amháin a rinne sé mar
      // Uachtarán • … = 3 mharc … Rud amháin nár éirigh leis a dhéanamh = 2 mharc • … = 2 mharc" (2013 Ordinary A 4(b)): one thing of
      // each of two kinds, the key a headed list for each. The first heading opens a part at the price its answers print; the second
      // heading prints its own price and opens the second part.
      else {
        const headed = /^(.*\(Alt \d+\))\s+(Rud amháin\s[^•=?]+)$/.exec(lead);
        if (headed && PROMPT.test(headed[1]) && bullets.length && marks !== undefined && marks < source.totalMarks) {
          open(tidy(headed[2]), marks);
          headedList = true;
          items.shift();
        }
      }
    }
    if (!current && marks !== undefined && marks <= source.totalMarks && /Cluastuiscint/.test(source.questionRef)) {
      // "1. Cad a seoladh aréir? Bliainiris = 2 mharc …" (2013 Higher Cluastuiscint, scheme PDF 8–11): the scheme prints no tariff
      // after its questions (each is worth the criterion's marks, "2 mharc × 5" on the cover, PDF 3), so the printed sub-question
      // runs straight on into its first answer. It opens at the criterion's marks; the text after its "?" or "." is that answer.
      const asked = ASKED.exec(items[0]);
      const end = asked ? items[0].slice(asked[0].length).search(/[?.](?=\s+\S)/) : -1;
      if (asked && end >= 0) {
        const cut = asked[0].length + end + 1;
        open(tidy(items[0].slice(0, cut)), source.totalMarks);
        current!.unprinted = true;
        items[0] = tidy(items[0].slice(cut));
      }
    }
    if (!current) return 'answer before any sub-question';
    let answers = 0;
    for (const [index, printed] of items.entries()) {
      let item = printed;
      // "• Gearrann obair Foodcloud … = 2 mharc nó • Faigheann na bochtáin cabhair riachtanach = 2 mharc" (2015 Higher A 4(b)(ii)):
      // the word between two answers, not one.
      if (item === 'nó') continue;
      // "Cáblaí = 0 Bhí carr trí thine = 2 mharc", "Afraic (leis féin) = 0 Uisce = 0" (2013 Higher Comhrá a Dó, Fógra a Dó): under
      // a question with no printed tariff, an answer refused at a bare 0 and the next answer share one line; each is a row.
      if (current.unprinted && /=\s*0\s+\S/.test(item)) {
        const pieces = item.split(/\s*=\s*0\s+(?=\S)/);
        item = pieces.pop()!;
        pieces.map(tidy).filter(Boolean).forEach(text => current!.rows.push({ text, marks: 0 }));
      }
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
      // "Leictreachas nó teas nó teilifís nó an t- idirlíon = 1 mharc + 1 mharc = 2 mharc", "Cistí, seacláid, seodra, ealaín =
      // 1 mharc + 1 mharc" (2013 Higher Comhrá a Dó 3, Píosa a Dó 2): under a question with no printed tariff, two points asked
      // from a printed list of alternatives, each point at its half. Each alternative is a row at that half.
      if (half !== undefined && current.unprinted && index === items.length - 1 && /,\s|\snó\s/.test(item)) {
        item.split(/\s*,\s*|\s+nó\s+/).map(tidy).filter(Boolean).forEach(text => current!.rows.push({ text, marks: half }));
        continue;
      }
      const stepped = item.endsWith(STEPPED) && own !== undefined ? nounSteps.shift() : undefined;
      current.rows.push({ text: item.split(STEPPED).join(''), marks: own, ...(stepped !== undefined ? { steps: [0, stepped, own!] } : {}) });
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
      if (current && plus && (LIST_RULE.test(listed.lead) || COUNT_RULE.test(listed.lead)) && listed.bullets.length === 0) {
        directions.push(listed.lead);
        const terms = [Number(answer), ...[...plus.matchAll(/\d+/g)].map(m => Number(m[0]))];
        if (!current.ladder && terms.reduce((a, b) => a + b, 0) === current.tariff) current.ladder = cumulative(terms);
        continue;
      }
      // The second heading of a headed pair, printed with its price ("Rud amháin nár éirigh leis a dhéanamh = 2 mharc"): its part.
      if (headedList && current && /^Rud amháin\s[^•=?]+$/.test(tidy(segment))) { open(tidy(segment), marks); continue; }
      // The bullets before the priced one are its alternatives at the same price.
      // "= 1 mharc + 1 mharc": a price in two equal halves, which a question with no printed tariff takes as two points.
      const halves = [Number(answer), ...[...(plus ?? '').matchAll(/\d+/g)].map(m => Number(m[0]))];
      const problem = addAnswers(segment, marks, halves.length === 2 && halves[0] === halves[1] ? halves[0] : undefined);
      if (problem) return { ok: false, reason: problem };
      continue;
    }
    if (brace !== undefined) {
      const numbers = [...brace.matchAll(/\d+/g)].map(m => Number(m[0]));
      if (numbers.length === 0) return { ok: false, reason: 'empty brace tariff' };
      const { lead, bullets } = splitBullets(segment);
      if (bullets.length && current) bullets.forEach(bullet => { if (RULE.test(bullet)) directions.push(bullet); else current!.rows.push({ text: bullet }); });
      // "… idirnáisiúnta. (3 mharc) {3-1 =2 mharc mura mbíonn ach rud amháin luaite.}" (2013 Higher A 2(a)): after the part's one
      // answer, a deduction from its tariff for an incomplete answer, with the condition. The answer steps through the printed
      // partial (0/2/3); the brace is a direction.
      const deduction = /^\s*(\d+)\s*-\s*(\d+)\s*=\s*(\d+)\s*m?h?arc\b\s*\S/.exec(brace);
      if (deduction && current && !lead && current.rows.length === 1 && current.rows[0].marks === current.tariff
        && Number(deduction[1]) === current.tariff && Number(deduction[1]) - Number(deduction[2]) === Number(deduction[3])) {
        current.rows[0].steps = [0, Number(deduction[3]), current.tariff];
        directions.push(tidy(brace));
        continue;
      }
      // "{3 mharc} • Réitigh sé … • Ní raibh oideachas orthu. • … {2 mharc +1mharc}" (2013 Higher A 3(a)): the open part's tariff,
      // its accepted points, then how the tariff divides between two of them: the part's ladder.
      if (current && !current.ladder && !lead && bullets.length > 0 && current.rows.every(row => row.marks === undefined)
        && brace.includes('+') && numbers.length === 2 && numbers[0] + numbers[1] === current.tariff) {
        current.ladder = cumulative(numbers);
        continue;
      }
      // "{3 mharc} Dhá phointe eolais = {2 mharc + 1 mharc}" (2014 Higher A 4(a)): the open part's tariff, then how it divides
      // under its own label: the part's ladder; the label is a direction.
      if (current && !current.ladder && current.rows.length === 0 && brace.includes('+') && /=$/.test(lead)
        && numbers.reduce((a, b) => a + b, 0) === current.tariff) {
        current.ladder = cumulative(numbers);
        directions.push(tidy(lead.replace(/\s*=$/, '')));
        continue;
      }
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
      // "Dhá scil as na cinn seo a leanas: 3 mharc + 2 mharc" (2014 Ordinary Reading B 4(a)): the heading over the list of accepted
      // points, its price the open part's ladder; the points listed after it are claimed by count.
      if (lead && /^Dhá\s[^•=:]{1,30}\bas na cinn seo a leanas:?$/i.test(lead) && current && !current.ladder && current.rows.length === 0
        && terms[0] + terms[1] === current.tariff) {
        directions.push(lead);
        current.ladder = cumulative(terms);
        continue;
      }
      if (lead && !PROMPT.test(lead) && !/[?.]$/.test(lead) && current) {
        // "Gaeilge líofa = 2 mharc + 2 mharc" was consumed as an answer above; a bare
        // sum after an answer without a prompt is a repeated tariff line.
        directions.push(lead);
        continue;
      }
      // "Breac síos dhá rannóg a bheidh sa chomórtas. (i) Ceol / Amhránaíocht / Scéalaíocht (ii) Rince / Drámaíocht / Mím 2 mharc +
      // 1 mharc" and "2. Cén dá rud a deir Síle …? (i) fón (póca) (ii) raidió nó i-pod 2 mharc+1 mharc=3 mharc" (2013 Ordinary
      // Fógra a hAon, Comhrá a Dó): a listening question, its two printed answer lines, then how its tariff divides: the ladder,
      // the lines claimed in order (first correct 2, second 1).
      const twoLines = /^(.*?[?.])\s+\(i\)\s+(.+?)\s+\(ii\)\s+(.+)$/.exec(lead);
      if (!current && twoLines && LISTENING.test(source.questionRef) && terms[0] !== terms[1] && terms[0] + terms[1] === source.totalMarks) {
        open(tidy(twoLines[1]), terms[0] + terms[1], cumulative(terms));
        current!.rows.push({ text: `(i) ${tidy(twoLines[2])}` }, { text: `(ii) ${tidy(twoLines[3])}` });
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
    // numbered question and its one answer before the tariff, as the Ordinary grid prints them. A listening key's answer can open
    // with a bracketed word, a figure or a small letter ("2. Cad a dhéanfaidh Seán anocht? (cúpla uair a chloig) staidéir 3 mharc",
    // "1. Cé mhéad leathanach atá sa bhliainiris? 160 nó céad seasca 3 mharc", "2. Cá bhfuil an bhliainiris ar díol? siopaí leabhar
    // ar fud an chontae 3 mharc", 2013 Ordinary).
    const answered = tidy(head.slice(question + 1));
    if (PROMPT.test(head) && question > 0 && !/[.?]$/.test(head)
      && (/^[A-ZÁÉÍÓÚ]/.test(answered) || (LISTENING.test(source.questionRef) && /^[(\da-záéíóú€]/.test(answered) && !/^\(Alt\b/.test(answered)))) {
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
      // "20 milliún = 0" (2013 Higher Comhrá a Dó, An Dara Mír 2), left last once its "(Cealú anseo …)" note is a direction: under a
      // question with no printed tariff, refused answers at a bare 0, each a row.
      if (current.unprinted && /=\s*0$/.test(item)) {
        item.split(/\s*=\s*0(?:\s+|$)/).map(tidy).filter(Boolean).forEach(text => current!.rows.push({ text, marks: 0 }));
        continue;
      }
      // "Tá trí mharc ar fáil as dhá mhír ghramadaí a aithint; … Sampla d’ainmfhocal … = …Átha; … Sampla de bhriathar … = Tá; Is"
      // (2015 Higher 6(a)): under a ladder, the rule and then one sample answer for each item the ladder counts.
      const pieces = current.ladder ? item.split(/\s(?=Sampla\b)/) : [item];
      if (pieces.length > 1) {
        if (!/^Sampla\b/.test(pieces[0])) directions.push(tidy(pieces.shift()!));
        pieces.forEach(piece => current!.rows.push({ text: tidy(piece) }));
        continue;
      }
      // "• “Bhuail sé lena ghaolta go léir i gContae Loch Garman.”" (2013 Ordinary A 2(a)): a quotation from the passage printed after
      // the priced answers with no price of its own. The scheme prices no answer there: a note, never a claimable row.
      if (!current.ladder && current.rows.length > 0 && current.rows.every(row => row.marks !== undefined) && /^“[^“”]+”\.?$/.test(item)) directions.push(item);
      else if (!listed && /^[A-ZÁÉÍÓÚ]/.test(item) && !/[=]/.test(item) && !current.ladder && current.rows.length > 0 && item.length > 60) directions.push(item);
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
      // A ladder counts answers, so an answer the scheme prints again word for word (2018 Higher B 1(a), its first point on
      // its own after both points) is the same answer: one row.
      part.rows = part.rows.filter((row, rowIndex) => part.rows.findIndex(other => other.text === row.text) === rowIndex);
    } else if (unpriced.length === part.rows.length) {
      part.rows.forEach(row => { row.marks = part.tariff; });
    } else if (unpriced.length > 0) {
      return { ok: false, reason: 'unpriced answers beside priced ones' };
    }
    const rows: IrishAnswerRow[] = part.rows.map((row, rowIndex) => ({ id: `r${rowIndex + 1}`, text: row.text.split(HELD).join(' '), marks: row.marks ?? 0,
      ...(row.steps ? { steps: row.steps } : {}) }));
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

/** 2022's deferred Higher scheme sets some parts in layouts the reader above does not cut, or misreads (a row ") bail
 *  réasúnta maith …"). Tried where it fails or misreads, or where the answers are marked "– pointe" (2022 deferred Higher's
 *  alone), and only where the part's printed tariff is the criterion's marks. The rows are the scheme's own words at its own
 *  prices:
 *  - answers marked "– pointe" under a split price ("Dhá rud – 2mharc (1 mharc + 1 mharc) ag ól Pepsi -- pointe …", "Dhá
 *    phointe 3 mharc (2 mharc + 1 mharc) Scannáin uafáis - pointe …"): a ladder over them, one answer earning the first share;
 *  - answers run together under a split price ("Dhá phointe eolais 3 mharc (2 mharc + 1 mharc) bail réasúnta … Tá na doirse
 *    ag titim as a chéile. 3 mharc"; "(2 mharc + 1 mharc) 3 mharc Breischéim na haidiachta …"): one row in those steps;
 *  - one point among answers marked "– pointe" ("3 mharc Pointe amháin iad ag scairteadh - pointe ag caitheamh … -- pointe",
 *    "Pointe amháin 2 mharc leis an gceol nua … -- pointe"): each answer at the price;
 *  - one answer priced in halves after it ("Pointe amháin 2 mharc an baile a fhágáil … (1 mharc + 1mharc)"): those steps;
 *  - alternatives priced on the first only ("2 mharc Is aoibhinn léi … = 2 mharc Is breá léi … = 2 mharc; Tá súil aici …"):
 *    each at the part's price. */
const LR_ASKED = /^(?:\d\.\s*)?(?:\([a-z]\)\s*)?(?:\((?:i|ii|iii|iv)\)\s*)?(.*?\(Alt \d+\)|[^?.]*[?.])\s+(.*)$/;
const LR_POINT_MARK = /\s*(?:–|-{1,5})\s*pointe\b\.?/;
const LR_SPLIT_PRICE = /^[^\d]*?(\d+)\s*m?h?arc\s*\(\s*(\d+)\s*m?h?arc\s*\+\s*(\d+)\s*m?h?arc\s*\)\s+(.+)$/;
const LR_SPLIT_FIRST = /^\(\s*(\d+)\s*m?h?arc\s*\+\s*(\d+)\s*m?h?arc\s*\)\s*(\d+)\s*m?h?arc\s+(.+)$/;
const LR_ONE_POINT = /^(?:Pointe amháin\s+)?(\d+)\s*m?h?arc\s+(?:Pointe amháin\s+)?(.+)$/;
const LR_HALVES = /^Pointe amháin\s+(\d+)\s*m?h?arc\s+(.+?)\s*\(\s*(\d+)\s*m?h?arc\s*\+\s*(\d+)\s*m?h?arc\s*\)$/;
const LR_ALTERNATIVES = /^(?:\((?:pointe amháin eolais)\)\s*)?\{?\s*(\d+)\s*m?h?arc\s*\}?\s+(.+)$/;
const LR_MARKED = /\s(?:–|-{1,5})\s*pointe\b/;
const LR_SPLIT_AFTER = /^[^\d]*?\(\s*(\d+)\s*m?h?arc\s*\)\s*(\d+)\s*m?h?arc\s*\+\s*(\d+)\s*m?h?arc\s+(.+)$/;
const LR_PAIR = /^(?:\([^()]*\)\s*)?\{\s*(\d+)\s*m?h?arc\s*:\s*(\d+)\s*m?h?arc\s*\+\s*(\d+)\s*m?h?arc\s*\}\s*(An chéad [^•]*?atá ceart = \d+ mharc; an dara [^•]*?atá ceart = \d+ mharc)?\s*•?\s*(.+?)\s*\(\s*(\d+)\s*m?h?arc\s*\)\s*agus\s+(.+?)\s*\(\s*(\d+)\s*m?h?arc\s*\)$/;
const LR_ONE_PRICED = /^(?:\(?pointe amháin eolais\)?\s*)?\(\s*(\d+)\s*m?h?arc\s*\)\s+(.+)$/;
const LR_SHORT = /\s*(An dá rud de dhíth\.\s*Rud amháin\s*\(\s*(\d+)\s*-\s*(\d+)\s*\))\s*$/;

function lastResort(source: IrishAnswerSource): IrishAllocation | undefined {
  if (source.guidance.length === 0) return undefined;
  const asked = LR_ASKED.exec(source.guidance[0].trim());
  if (!asked) return undefined;
  const prompt = tidy(asked[1]);
  const rest = asked[2].trim();
  const total = source.totalMarks;
  const part = (rows: IrishAnswerRow[], ladder?: number[], directions: string[] = []): IrishAllocation => ({
    parts: [{ id: 'p1', prompt, tariff: total, ...(ladder ? { ladder } : {}), rows: rows.map((row, index) => ({ ...row, id: `r${index + 1}` })) }],
    directions,
  });
  // A run of answers under a split price: one right answer earns the first share, two the whole.
  const stepsOf = (first: number) => [...new Set([0, first, total])].sort((x, y) => x - y);
  // The price printed again after the answers ("… as a chéile. 3 mharc") is the part's, not an answer's.
  const unpriced = (text: string) => tidy(text.replace(/\s*\b\d+\s*m?h?arc\s*$/, ''));
  // "{3 mharc: 2 mharc + 1 mharc} An chéad rud atá ceart = 2 mharc; an dara rud atá ceart = 1 mharc A dheasc a fholmhú (2 mharc)
  // agus carn mór cáipéisí a chrochadh leis (1 mharc)": the two things the answer names, on the part's ladder.
  const pair = LR_PAIR.exec(rest);
  if (pair && Number(pair[1]) === total && Number(pair[2]) + Number(pair[3]) === total && pair[2] === pair[6] && pair[3] === pair[8]) {
    return part([{ id: '', text: tidy(pair[5]), marks: 0 }, { id: '', text: tidy(pair[7]), marks: 0 }], [Number(pair[2]), total],
      pair[4] ? [tidy(pair[4])] : []);
  }
  // "pointe amháin eolais (2 mharc) As sin amach …", "(pointe amháin eolais) (2 mharc) Ag déanamh taighde … An dá rud de
  // dhíth. Rud amháin (2-1)": the one answer at the price, in the step the scheme gives a half answer.
  const priced = LR_ONE_PRICED.exec(rest);
  if (priced && Number(priced[1]) === total) {
    const short = LR_SHORT.exec(priced[2]);
    const text = unpriced(short ? priced[2].slice(0, short.index) : priced[2]);
    const reduced = short && Number(short[2]) === total ? Number(short[2]) - Number(short[3]) : undefined;
    if (text) return part([{ id: '', text, marks: total, ...(reduced !== undefined ? { steps: [0, reduced, total] } : {}) }], undefined, short ? [tidy(short[1])] : []);
  }
  const split = LR_SPLIT_PRICE.exec(rest) ?? (() => {
    const first = LR_SPLIT_FIRST.exec(rest) ?? LR_SPLIT_AFTER.exec(rest);
    if (!first) return null;
    return (first[0] === LR_SPLIT_FIRST.exec(rest)?.[0]
      ? Object.assign([first[0], first[3], first[1], first[2], first[4]], { index: 0, input: rest })
      : first) as RegExpExecArray;
  })();
  if (split && Number(split[1]) === total && Number(split[2]) + Number(split[3]) === total) {
    const first = Number(split[2]);
    if (LR_MARKED.test(` ${split[4]}`)) {
      const pieces = ` ${split[4]}`.split(LR_POINT_MARK).map(tidy);
      const answers = pieces.slice(0, -1).filter(Boolean);
      const trailer = pieces[pieces.length - 1];
      if (answers.length >= 2) return part(answers.map(text => ({ id: '', text, marks: 0 })), [first, total],
        trailer && !/^\d+\s*m?h?arc$/.test(trailer) ? [trailer] : []);
    } else {
      return part([{ id: '', text: unpriced(split[4]), marks: total, steps: stepsOf(first) }]);
    }
  }
  const halves = LR_HALVES.exec(rest);
  if (halves && Number(halves[1]) === total && Number(halves[3]) + Number(halves[4]) === total) {
    return part([{ id: '', text: tidy(halves[2]), marks: total, steps: [...new Set([0, Number(halves[3]), Number(halves[4]), total])].sort((x, y) => x - y) }]);
  }
  const one = LR_ONE_POINT.exec(rest);
  if (one && Number(one[1]) === total && LR_MARKED.test(` ${one[2]}`)) {
    const answers = ` ${one[2]}`.split(LR_POINT_MARK).map(tidy).filter(Boolean);
    if (answers.length) return part(answers.map(text => ({ id: '', text, marks: total })));
  }
  const alternatives = LR_ALTERNATIVES.exec(rest);
  if (alternatives && Number(alternatives[1]) === total) {
    const price = new RegExp(`\\s*=\\s*${alternatives[1]}\\s*m?h?arc\\b[;.]?\\s*|\\s*•\\s*`);
    const answers = alternatives[2].split(price).map(tidy).filter(Boolean);
    if (answers.length >= 2 && new RegExp(`=\\s*${alternatives[1]}\\s*m?h?arc`).test(alternatives[2])) {
      return part(answers.map(text => ({ id: '', text, marks: total })));
    }
  }
  return undefined;
}

/** A reading the reader above made of a layout it does not know: a row or a note that is only a stray bracket. */
const misread = (allocation: IrishAllocation) => allocation.parts.some(part => part.rows.some(row => /^\)|\($|^\($/.test(row.text.trim())))
  || allocation.directions.some(note => /^[()]$/.test(note.trim()));

export function irishAnswersFor(source: IrishAnswerSource): IrishAllocation | undefined {
  // Answers marked "– pointe" are 2022 deferred Higher's alone, and the reader above misreads them (one row ") ag crochadóireacht
  // … -- pointe ag ól Pepsi -- pointe …"): they are read as the list they are, first.
  if (source.guidance.length && LR_MARKED.test(source.guidance[0])) {
    const listed = lastResort(source);
    if (listed) return listed;
  }
  const result = parseIrishAnswers(source);
  if (result.ok && !misread(result.allocation)) return result.allocation;
  return lastResort(source) ?? (result.ok ? result.allocation : undefined);
}

