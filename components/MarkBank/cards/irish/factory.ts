/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Irish cards retain the marking grammar printed by the SEC.  Exact listening
 * and reading answers, indicative literature material, composition quality
 * criteria and Ordinary-Level language deductions are deliberately distinct.
 */

import type {
  CardAudioMaterial,
  CardSourceMaterial,
  IrishAllocation,
  IrishAnswerPart,
  IrishCriterion,
  SecRubricCard,
} from '../../../../types/markBank';
import authored from './authored.json';
import higher2026P1 from './higher-2026-p1-authored.json';
import higher2026P2 from './higher-2026-p2-authored.json';
import ordinary2026P1 from './ordinary-2026-p1-authored.json';
import ordinary2026P2 from './ordinary-2026-p2-authored.json';
import higher2025P2 from './higher-2025-p2-authored.json';
import ordinary2025P2 from './ordinary-2025-p2-authored.json';
import ordinary2024P2 from './ordinary-2024-p2-authored.json';
import higher2023P2 from './higher-2023-p2-authored.json';
import ordinary2023P2 from './ordinary-2023-p2-authored.json';
import ordinary2022P2 from './ordinary-2022-p2-authored.json';
import higher2022P2 from './higher-2022-p2-authored.json';
import higher2021P2 from './higher-2021-p2-authored.json';
import ordinary2021P2 from './ordinary-2021-p2-authored.json';
import higher2020P1 from './higher-2020-p1-authored.json';
import higher2020P2 from './higher-2020-p2-authored.json';
import ordinary2020P1 from './ordinary-2020-p1-authored.json';
import ordinary2020P2 from './ordinary-2020-p2-authored.json';
import higher2019P1 from './higher-2019-p1-authored.json';
import higher2019P2 from './higher-2019-p2-authored.json';
import ordinary2019P1 from './ordinary-2019-p1-authored.json';
import ordinary2019P2 from './ordinary-2019-p2-authored.json';
import higher2018P1 from './higher-2018-p1-authored.json';
import higher2018P2 from './higher-2018-p2-authored.json';
import ordinary2018P1 from './ordinary-2018-p1-authored.json';
import ordinary2018P2 from './ordinary-2018-p2-authored.json';
import higher2017P1 from './higher-2017-p1-authored.json';
import higher2017P2 from './higher-2017-p2-authored.json';
import ordinary2017P1 from './ordinary-2017-p1-authored.json';
import ordinary2017P2 from './ordinary-2017-p2-authored.json';
import higher2016P1 from './higher-2016-p1-authored.json';
import higher2016P2 from './higher-2016-p2-authored.json';
import ordinary2016P1 from './ordinary-2016-p1-authored.json';
import ordinary2016P2 from './ordinary-2016-p2-authored.json';
import higher2015P1 from './higher-2015-p1-authored.json';
import higher2015P2 from './higher-2015-p2-authored.json';
import ordinary2015P1 from './ordinary-2015-p1-authored.json';
import { irishAnswersFor, stepSingleAnswerLadders } from './answers';
import { irishTariffsFor, stepPrintedScales } from './tariffs';
import { resolveCurriculumSpecification } from '../../../../curriculumRegistry';

type IrishLevel = 'higher' | 'ordinary';

interface AuthoredIrishCard {
  id: string;
  year: number;
  level: IrishLevel;
  paper: 1 | 2;
  section: '1' | '2';
  questionRef: string;
  /** The lead-in the paper prints before the question proper, e.g. 2B's "Níl cead aon ábhar …" restriction. */
  stem?: string;
  questionText: string;
  /** What a one-answer practice card practises, in English ("One of the two answers (answer 1, 1 mark)"). */
  practiceFocus?: string;
  totalMarks: number;
  topicId: string;
  additionalTopicIds?: string[];
  conceptId: string;
  paperFileid: string;
  schemePage: number;
  schemePages?: number[];
  reviewedAt?: string;
  taskRequirements: string[];
  criteria: IrishCriterion[];
  markingGuideNote: string;
  sourceMaterial?: CardSourceMaterial;
  audioMaterial?: CardAudioMaterial;
}

// Paper-reviewed components ship as their own files beside the legacy census output.
const DATA = [...authored.cards, ...higher2026P1.cards, ...higher2026P2.cards, ...ordinary2026P1.cards, ...ordinary2026P2.cards, ...higher2025P2.cards, ...ordinary2025P2.cards, ...ordinary2024P2.cards, ...higher2023P2.cards, ...ordinary2023P2.cards, ...ordinary2022P2.cards, ...higher2022P2.cards, ...higher2021P2.cards, ...ordinary2021P2.cards, ...higher2020P1.cards, ...higher2020P2.cards, ...ordinary2020P1.cards, ...ordinary2020P2.cards, ...higher2019P1.cards, ...higher2019P2.cards, ...ordinary2019P1.cards, ...ordinary2019P2.cards, ...higher2018P1.cards, ...higher2018P2.cards, ...ordinary2018P1.cards, ...ordinary2018P2.cards, ...higher2017P1.cards, ...higher2017P2.cards, ...ordinary2017P1.cards, ...ordinary2017P2.cards, ...higher2016P1.cards, ...higher2016P2.cards, ...ordinary2016P1.cards, ...ordinary2016P2.cards, ...higher2015P1.cards, ...higher2015P2.cards, ...ordinary2015P1.cards] as AuthoredIrishCard[];

/** Listening and reading cards carry the scheme's exact answers; cut them
 *  into rows where the parts add up to the criterion (cards/irish/answers.ts).
 *  The 2026 Paper 1 question cards cite the extract itself ("Cuid A · Fógra a hAon · Ceist 1(a)"). */
const EXACT_ANSWER_CARD = /Cluastuiscint|Léamhthuiscint|Paper 1 Cuid [ABC] · (?:Fógra|Comhrá|Píosa)/;

/** Literature cards price what the student must do rather than list answers;
 *  their Eolas tariff is cut into rows by cards/irish/tariffs.ts, as is the last
 *  reading question's composite tariff when the answer cutter cannot read it.
 *  Reviewed cards cite the paper's own Irish headings (Prós, Filíocht, Litríocht),
 *  the generated corpus the English ones; both name the same printed questions. */
const LITERATURE_CARD = /Prose|Poetry|Literature|Prós|Filíocht|Litríocht/;
const COMPOSITE_READING = /Léamhthuiscint .* Ceist 6/;
const PRICED = /\d+\s*m?h?arc\b/;

/** The 2022 and 2024 Higher prose routes (irish_higher_routes.py) open each Eolas criterion with the whole of the
 *  section's first scheme page: its notes on the 25 + 5 split and its band table, ending at the last band
 *  ("Lag/ An-lag … 0-9", then the Gaeilge column's descriptor in 2022). That page is the section's furniture, the
 *  same for every route; its "(30 marc)", "Eolas (25 marc)" and "Gaeilge (5 mharc)" headings are never a part of
 *  this criterion. The rows are read from what follows it, the route's own scheme text. */
const SECTION_PAGE = /^Nóta: I gcás na gceisteanna 2 \(Prós\)[\s\S]*?Lag\/ ?An-lag[^•]*?\d+\s*-\s*\d+(?:\s+\d+\s*-\s*\d+)*(?:\s+Cumas lag\/an-lag maidir leis na príomhghnéithe de cheart na teanga \([^)]*\))?\s*/;
const ownGuidance = (criterion: AuthoredIrishCard['criteria'][number]) =>
  criterion.guidance.map((line, index) => (index === 0 ? line.replace(SECTION_PAGE, '') : line)).filter(line => line.trim());

const allocationFor = (card: AuthoredIrishCard, criterion: AuthoredIrishCard['criteria'][number]) => {
  const source = { id: card.id, totalMarks: criterion.maxMarks, cardTotal: card.totalMarks, questionRef: card.questionRef, questionText: card.questionText, guidance: ownGuidance(criterion) };
  if (criterion.guidanceKind === 'exact' && EXACT_ANSWER_CARD.test(card.questionRef)) {
    return irishAnswersFor(source) ?? (COMPOSITE_READING.test(card.questionRef) ? irishTariffsFor(source) : undefined);
  }
  // Literature tariffs are read for every priced criterion: the reviewed cards also price the title and
  // author ("Teideal an úrscéil = 1 mharc Ainm an údair = 1 mharc") as an exact criterion of their own.
  if ((criterion.guidanceKind === 'indicative' || criterion.guidanceKind === 'exact') && LITERATURE_CARD.test(card.questionRef)
    && criterion.guidance.some(line => PRICED.test(line))) {
    return irishTariffsFor(source);
  }
  // A reading question's opinion or account priced as a whole (Ceist 6(b)) on its own criterion.
  if (criterion.guidanceKind === 'indicative' && EXACT_ANSWER_CARD.test(card.questionRef) && criterion.guidance.some(line => PRICED.test(line))) {
    return irishTariffsFor(source);
  }
  return undefined;
};

type Criterion = AuthoredIrishCard['criteria'][number];
const pricedAward = (criterion: Criterion) => criterion.kind === 'award' && criterion.guidanceKind !== 'quality'
  && criterion.guidance.some(line => PRICED.test(line));

/** A reviewed card can price one printed sub-question across several criteria that all carry its whole
 *  scheme ("Tréith 1 a lua = 2 mharc + sampla … = 4 mharc Tréith 2 a lua = 2 mharc + …" on Tréith 1 and on
 *  Tréith 2), or print a sibling's tariff inside its own ("An príomhthéama = 2 mharc An plé … = 23 marc" on
 *  the 23-mark criterion). Read the guidance at the siblings' joint total, then cut its rows in print order
 *  into runs that add up to each sibling's marks exactly; the criterion takes its own run. No run that does
 *  not add up is ever assigned, and no word is added: the rows are the reader's own slices. */
const siblingAllocation = (card: AuthoredIrishCard, criterion: Criterion): IrishAllocation | undefined => {
  if (!pricedAward(criterion)) return undefined;
  const index = card.criteria.indexOf(criterion);
  const groups: Criterion[][] = [];
  const shared = card.criteria.filter(other => pricedAward(other) && other.guidance[0] === criterion.guidance[0]);
  if (shared.length > 1) groups.push(shared);
  for (let start = index - 1; start >= 0 && pricedAward(card.criteria[start]); start--) groups.push(card.criteria.slice(start, index + 1));
  for (const group of groups) {
    const source = { id: card.id, totalMarks: group.reduce((sum, member) => sum + member.maxMarks, 0), cardTotal: card.totalMarks,
      questionRef: card.questionRef, questionText: card.questionText, guidance: ownGuidance(criterion) };
    const readings = [criterion.guidanceKind === 'exact' ? irishAnswersFor(source) : undefined, irishTariffsFor(source)];
    for (const parsed of readings) {
      if (!parsed || parsed.parts.some(part => part.ladder)) continue;
      const rows = parsed.parts.flatMap(part => part.rows);
      const runs: typeof rows[] = [];
      let next = 0;
      for (const member of group) {
        const run: typeof rows = [];
        let sum = 0;
        while (next < rows.length && sum < member.maxMarks) { sum += rows[next].marks; run.push(rows[next]); next += 1; }
        if (sum !== member.maxMarks) break;
        runs.push(run);
      }
      if (runs.length !== group.length || next !== rows.length) continue;
      const position = group.indexOf(criterion);
      const first = position === 0;
      const samples = first ? parsed.parts.flatMap(part => part.samples ?? []) : [];
      return {
        parts: [{ id: 'p1', ...(first && parsed.parts[0].prompt ? { prompt: parsed.parts[0].prompt } : {}), tariff: criterion.maxMarks,
          rows: runs[position].map((row, rowIndex) => ({ ...row, id: `r${rowIndex + 1}` })), ...(samples.length ? { samples } : {}) }],
        directions: first ? parsed.directions : [],
      };
    }
  }
  return undefined;
};

/** A practice card derived from a printed question (its id extends the question card's: "…-q1-bi-1" for one
 *  of the two answers (b)(i) asks for, "…-q6-b-1" for one trait, "…-3a-a-i" for part (i)). */
const CARD_IDS = new Set(DATA.map(card => card.id));
const derivedFrom = (id: string): boolean => {
  for (let cut = id.lastIndexOf('-'); cut > 0; cut = id.lastIndexOf('-', cut - 1)) if (CARD_IDS.has(id.slice(0, cut))) return true;
  return false;
};
const primaryAllocation = (card: AuthoredIrishCard, criterion: Criterion) => allocationFor(card, criterion) ?? siblingAllocation(card, criterion);
const sameCriterion = (a: Criterion, b: Criterion) => a.id === b.id && a.maxMarks === b.maxMarks
  && a.guidance.length === b.guidance.length && a.guidance.every((line, index) => line === b.guidance[index]);
const FREAGRAI = /^(.*?)\((\d+)\s*m?h?arc(?:\s*\+\s*(\d+)\s*m?h?arc)?\)\s*Freagraí(?: [Ss]amplacha)?:\s*(.+)$/;

/** Rows for a derived practice card whose own criterion the readers cannot cut (it is a slot of a part, or the
 *  part alone), always from the same printed scheme and never added to:
 *  - the identical criterion on the question's own card (one trait of two: "Tréith 1 a lua = 2 mharc + …");
 *  - one answer of a part priced "{2 mharc: 1 mharc + 1 mharc}": the part's printed answers, one of them claimed;
 *  - a part whose answers the scheme lists after "Freagraí:", one sub-question at a time, each answer at its price. */
const derivedAllocation = (card: AuthoredIrishCard, criterion: Criterion): IrishAllocation | undefined => {
  if (!derivedFrom(card.id) || !pricedAward(criterion)) return undefined;
  for (const other of DATA) {
    if (other === card || !card.id.startsWith(other.id + '-')) continue;
    const twin = other.criteria.find(candidate => sameCriterion(candidate, criterion));
    const shared = twin && primaryAllocation(other, twin);
    if (shared) return shared;
  }
  const source = { id: card.id, totalMarks: criterion.maxMarks, cardTotal: card.totalMarks, questionRef: card.questionRef,
    questionText: card.questionText, guidance: ownGuidance(criterion) };
  for (const times of [2, 3]) {
    const whole = irishAnswersFor({ ...source, totalMarks: criterion.maxMarks * times });
    const part = whole?.parts.length === 1 ? whole.parts[0] : undefined;
    if (part?.ladder && part.ladder.length === times && part.ladder.every((step, index) => step === criterion.maxMarks * (index + 1))) {
      // A ladder prices how many printed answers are right, so on the one-answer card any one of them earns the
      // card's mark: the rows keep their printed text and take their marks from the ladder, as answers.ts's do.
      return { parts: [{ ...part, tariff: criterion.maxMarks, ladder: [criterion.maxMarks], rows: part.rows.map(row => ({ ...row, marks: 0 })) }],
        directions: whole!.directions };
    }
  }
  return freagraiAllocation(criterion);
};

/** A literature sub-question list the scheme prices as "(a) … (2 mharc) Freagraí: x… y…" (or "Freagraí samplacha:"
 *  with bullets): each printed sub-question a part, each listed answer a row at the part's per-answer price. Any card's
 *  priced criterion of that shape gets these rows, the parent question's as well as its one-part practice cards'. */
const freagraiAllocation = (criterion: Criterion): IrishAllocation | undefined => {
  const parts: IrishAnswerPart[] = [];
  const directions: string[] = [];
  for (const line of ownGuidance(criterion)) {
    if (/^Nóta:/.test(line)) { directions.push(line); continue; }
    for (const segment of line.split(/\s(?=\([a-f]\)\s)/)) {
      const text = segment.replace(/^\((?:i|ii|iii)\)\s*/, '').trim();
      if (!text) continue; // the part's own label, "(i)", before its sub-questions
      const match = FREAGRAI.exec(text);
      if (!match) return undefined;
      const each = Number(match[2]);
      const tariff = each + (match[3] ? Number(match[3]) : 0);
      // A bulleted list is cut at its bullets; otherwise at each "…", never inside a quoted answer (‘… …’).
      const answers = (match[4].includes('•') ? match[4].split('•') : match[4].split(/…(?![^‘’]*’)/))
        .map(answer => answer.trim()).filter(Boolean);
      if (!answers.length) return undefined;
      parts.push({ id: `p${parts.length + 1}`, prompt: match[1].trim(), tariff,
        rows: answers.map((text, index) => ({ id: `r${index + 1}`, text, marks: each })) });
    }
  }
  return parts.length && parts.reduce((sum, part) => sum + part.tariff, 0) === criterion.maxMarks ? { parts, directions } : undefined;
};

const cloneCriteria = (card: AuthoredIrishCard): IrishCriterion[] =>
  card.criteria.map(criterion => {
    const found = primaryAllocation(card, criterion) ?? derivedAllocation(card, criterion)
      ?? (pricedAward(criterion) ? freagraiAllocation(criterion) : undefined);
    const allocation = found && stepPrintedScales(stepSingleAnswerLadders(found), criterion.guidance);
    return {
      ...criterion,
      permittedMarks: [...criterion.permittedMarks],
      guidance: [...criterion.guidance],
      ...(allocation ? { allocation } : {}),
    };
  });

const makeCard = (card: AuthoredIrishCard): SecRubricCard => ({
  id: card.id,
  subjectId: 'irish',
  level: card.level,
  topicId: card.topicId,
  additionalTopicIds: card.additionalTopicIds ? [...card.additionalTopicIds] : undefined,
  conceptId: card.conceptId,
  source: 'sec',
  kind: 'rubric',
  year: card.year,
  paperFileid: card.paperFileid,
  section: card.section,
  questionRef: card.questionRef,
  ...(card.stem ? { stem: card.stem } : {}),
  questionText: card.questionText,
  ...(card.practiceFocus ? { practiceFocus: card.practiceFocus } : {}),
  sourceMaterial: card.sourceMaterial,
  audioMaterial: card.audioMaterial,
  totalMarks: card.totalMarks,
  schemeCitation:
    `SEC Gaeilge ${card.level === 'higher' ? 'Ardleibhéal' : 'Gnáthleibhéal'} ` +
    `marking scheme ${card.year}, p.${card.schemePage}` +
    (card.schemePages && card.schemePages.length > 1 ? `–${card.schemePages.at(-1)}` : '') +
    ' — © State Examinations Commission.',
  specVersion: resolveCurriculumSpecification('irish', card.year)!.id,
  qa: {
    gates: [
      'verbatim-paper-prompt',
      'irish-published-rubric',
      'required-source-complete',
      'paper-census',
    ],
    humanReviewedBy: 'corpus-verified',
    humanReviewedAt: card.reviewedAt ?? '2026-08-30',
  },
  rubric: {
    system: 'irish',
    taskRequirements: [...card.taskRequirements],
    criteria: cloneCriteria(card),
    markingGuideNote: card.markingGuideNote,
  },
});

export const generatedCardsForLevel = (level: IrishLevel): SecRubricCard[] =>
  DATA.filter(card => card.level === level).map(makeCard);

export const IRISH_AUTHORED_CARD_COUNT = DATA.length;
