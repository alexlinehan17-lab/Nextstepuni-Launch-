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
import { irishAnswersFor } from './answers';
import { irishTariffsFor } from './tariffs';
import { resolveCurriculumSpecification } from '../../../../curriculumRegistry';

type IrishLevel = 'higher' | 'ordinary';

interface AuthoredIrishCard {
  id: string;
  year: number;
  level: IrishLevel;
  paper: 1 | 2;
  section: '1' | '2';
  questionRef: string;
  questionText: string;
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
const DATA = [...authored.cards, ...higher2026P1.cards, ...higher2026P2.cards, ...ordinary2026P1.cards, ...ordinary2026P2.cards, ...higher2025P2.cards, ...ordinary2025P2.cards, ...ordinary2024P2.cards, ...higher2023P2.cards, ...ordinary2023P2.cards] as AuthoredIrishCard[];

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
/** The 2024 Higher reading builder (irish_reading.py) opens each Léargas criterion with its own summary of the
 *  scheme's tariff, not the scheme's words; the scheme's own "Léargas 1 (L1) = 2 mharc + míniú … = 4 mharc" follows
 *  it. Rows are never read from the summary, so no row a student claims is worded by us. */
const BUILDER_SUMMARY = /^An léargas seo = 2 mharc; míniú i d’fhocail féin le sampla cruinn = 4 mharc\. Gan léargas luaite\/intuigthe, ní féidir glacadh leis an sampla\.\s*/;
const ownGuidance = (criterion: AuthoredIrishCard['criteria'][number]) =>
  criterion.guidance.map((line, index) => (index === 0 ? line.replace(SECTION_PAGE, '').replace(BUILDER_SUMMARY, '') : line)).filter(line => line.trim());

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

const cloneCriteria = (card: AuthoredIrishCard): IrishCriterion[] =>
  card.criteria.map(criterion => {
    const allocation = allocationFor(card, criterion) ?? siblingAllocation(card, criterion);
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
  questionText: card.questionText,
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
