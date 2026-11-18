/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The two automatic checks of the single model (plan section 5, M5), across every subject:
 *   1. every card reaches a Topic Atlas question under the same topic;
 *   2. every Topic Atlas question in scope (2010-2026; the English papers, Irish's own papers) has a card.
 * They return today's misses; test/atlasModelChecks.test.ts holds them to test/fixtures/atlasModelKnownMisses.json,
 * a list that may shrink and never grow.
 *
 * "Same topic", per subject:
 * - in the model (components/PaperTrail/atlasModel.ts): the card's own topic record names its question, and the
 *   question's Atlas headings are its parts' headings;
 * - Atlas exam-topic headings elsewhere: the card's curriculum topic (after curriculumRegistry's own aliases) is
 *   crosswalked to headings of the card's level (ExamTopicDefinition.curriculumNodeIds), and one of them is a heading
 *   of the question (or the same heading in the subject's other course list, numbering aside);
 * - curriculum headings elsewhere: the card's topic is one of the question's tags.
 * A card whose topic has no recorded route into the Atlas's headings is a miss of its own ('no-topic-link'): the
 * two lists are not joined for it yet.
 */
import { SUBJECTS, levelsFor, loadCards } from '../../components/MarkBank/deck';
import {
  browseTopicIdsForQuestion, logicalQuestionIdentity, questionsForTopics, topicLabel, topicsForPaper,
} from '../../components/PaperTrail/topics';
import { askRecord, isModelSubject } from '../../components/PaperTrail/atlasModel';
import { physicalEducationTask } from '../../components/PaperTrail/physicalEducationTasks';
import { curriculumNodeIdsForExamTopic, examTopicDefinition, examTopicTaxonomyFor } from '../../data/examTopics/registry';
import { PAPER_TRAIL_SUBJECTS } from '../../paperTrailData';
import { CURRICULUM } from '../../curriculum';
import { resolveSubjectId, specificationsForSubject } from '../../curriculumRegistry';
import type { PaperLang, PaperLevel } from '../../types/paperTrail';
import type { SecCard } from '../../types/markBank';
import { addressContext, atlasAddress } from './cardAtlasAddress';

export type CardMissReason = 'no-address-rule' | 'no-own-atlas-question' | 'no-join-entry' | 'unreadable-ref'
  | 'no-atlas-paper' | 'no-atlas-question' | 'no-heading' | 'no-heading-at-level' | 'no-topic-record'
  | 'no-topic-link' | 'topic-differs';

export interface CheckResult {
  /** Mark Bank subject -> reason -> card ids. */
  cards: Record<string, Partial<Record<CardMissReason, string[]>>>;
  /** Atlas subject -> question keys (year|level|booklet|n) with no card. */
  questions: Record<string, string[]>;
  totals: { cards: number; cardsReaching: number; atlasQuestions: number; atlasQuestionsWithCard: number };
}

const LC = PAPER_TRAIL_SUBJECTS.filter(s => s.cycle === 'lc');
export function atlasSubjectFor(bankId: string): string | null {
  const canonical = resolveSubjectId(bankId) ?? bankId;
  return LC.find(s => (s.curriculumId ?? s.id) === canonical)?.id ?? null;
}

const norm = (s: string) => s.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9]+/g, ' ').trim();
const headingName = (id: string) => norm(topicLabel(id)).replace(/^\d+( \d+)* /, '');

function aliasExpander(bankId: string) {
  const g = new Map<string, Set<string>>();
  const link = (a: string, b: string) => { if (!a || !b || a === b) return; for (const [x, y] of [[a, b], [b, a]]) { const s = g.get(x) ?? new Set(); s.add(y); g.set(x, s); } };
  for (const spec of specificationsForSubject(bankId)) {
    for (const [k, v] of Object.entries(spec.legacyTopicAliases ?? {})) link(k, v);
    for (const group of spec.groups) for (const t of group.topics) for (const a of t.aliases ?? []) link(t.id, a);
  }
  return (id: string) => { const seen = new Set([id]); const stack = [id]; while (stack.length) for (const n of g.get(stack.pop()!) ?? []) if (!seen.has(n)) { seen.add(n); stack.push(n); } return seen; };
}

export async function runAtlasModelChecks(): Promise<CheckResult> {
  const result: CheckResult = { cards: {}, questions: {}, totals: { cards: 0, cardsReaching: 0, atlasQuestions: 0, atlasQuestionsWithCard: 0 } };
  const credited = new Map<string, Set<string>>(); // atlas subject -> logical identities with a card
  const credit = (atlas: string, identity: string) => { const s = credited.get(atlas) ?? new Set(); s.add(identity); credited.set(atlas, s); };
  for (const subject of SUBJECTS) {
    const cards: SecCard[] = [];
    for (const level of levelsFor(subject.id)) cards.push(...await loadCards(subject.id, level as never));
    if (!cards.length) continue;
    const homeAtlas = atlasSubjectFor(subject.id);
    const ctx = addressContext(cards);
    const expand = aliasExpander(subject.id);
    const misses: CheckResult['cards'][string] = {};
    const miss = (reason: CardMissReason, id: string) => { (misses[reason] ??= []).push(id); };
    for (const card of cards) {
      result.totals.cards++;
      const a = atlasAddress(card, homeAtlas ?? '', ctx);
      if ('fail' in a) { miss(a.fail as CardMissReason, card.id); continue; }
      const atlas = a.atlas ?? homeAtlas;
      if (!atlas) { miss('no-atlas-paper', card.id); continue; }
      let paper = null as ReturnType<typeof topicsForPaper>;
      for (const lang of ['ev', 'iv'] as PaperLang[]) { paper = topicsForPaper(atlas, card.year, card.level as PaperLevel, lang, a.fileid); if (paper) break; }
      let headings: string[]; let n: string; let identity: string;
      if (a.peTask) {
        const task = physicalEducationTask({ subjectId: atlas, level: card.level as PaperLevel, year: card.year, lang: 'ev', fileid: a.fileid, n: String(a.cands[0]) });
        if (!task) { miss('no-atlas-question', card.id); continue; }
        n = task.n; headings = browseTopicIdsForQuestion(task, { n: task.n, primary: '' });
        identity = logicalQuestionIdentity({ subjectId: atlas, level: task.level, year: task.year, paperKey: task.paperKey, fileid: task.fileid, n: task.n });
      } else {
        if (!paper) { miss('no-atlas-paper', card.id); continue; }
        let q = null as (typeof paper.q)[number] | null;
        for (const cand of a.cands) {
          if (typeof cand === 'string') q = paper.q.find(x => x.n === cand) ?? null;
          else if (paper.q.some(x => x.n === cand.ifHas)) q = paper.q.find(x => x.n === cand.n) ?? null;
          if (q) break;
        }
        if (!q) { miss('no-atlas-question', card.id); continue; }
        n = q.n; headings = browseTopicIdsForQuestion(paper, q);
        identity = logicalQuestionIdentity({ subjectId: paper.subjectId, level: paper.level, year: paper.year, paperKey: paper.paperKey, fileid: paper.fileid, n: q.n });
        const p = paper;
        for (const extra of a.extraCredit ?? []) if (extra && p.q.some(x => x.n === extra)) credit(atlas, logicalQuestionIdentity({ subjectId: p.subjectId, level: p.level, year: p.year, paperKey: p.paperKey, fileid: p.fileid, n: extra }));
        for (const placed of a.extraPlacements ?? []) {
          const other = topicsForPaper(atlas, card.year, card.level as PaperLevel, 'ev', `${placed.fileid.replace(/\.pdf$/i, '')}.pdf`);
          if (other?.q.some(x => x.n === placed.n)) credit(atlas, logicalQuestionIdentity({ subjectId: other.subjectId, level: other.level, year: other.year, paperKey: other.paperKey, fileid: other.fileid, n: placed.n }));
        }
      }
      credit(atlas, identity);
      if (!headings.length) { miss('no-heading', card.id); continue; }
      const defs = headings.map(id => examTopicDefinition(id)).filter(Boolean);
      if (defs.length && !defs.some(d => d!.level === card.level)) { miss('no-heading-at-level', card.id); continue; }
      // Same topic.
      if (isModelSubject(atlas)) {
        const record = askRecord(card.id);
        if (!record || record.n !== n || record.year !== card.year) { miss('no-topic-record', card.id); continue; }
        if (!record.topics.some(t => headings.includes(t.id))) { miss('topic-differs', card.id); continue; }
        result.totals.cardsReaching++; continue;
      }
      const own = [card.topicId, ...(card.additionalTopicIds ?? [])].flatMap(id => [...expand(id)]);
      const taxonomy = examTopicTaxonomyFor(atlas);
      let mapped: string[];
      if (taxonomy) {
        mapped = taxonomy.topics.filter(t => (t.level === card.level || t.level === 'common' || card.level === 'common')
          && curriculumNodeIdsForExamTopic(t.id).some(node => own.includes(node))).map(t => t.id);
      } else {
        const ids = new Set(CURRICULUM.filter(c => c.id === atlas || c.id === (resolveSubjectId(subject.id) ?? subject.id))
          .flatMap(c => c.strands.flatMap(s => s.subtopics.map(t => t.id))));
        mapped = own.filter(id => ids.has(id));
      }
      if (!mapped.length) { miss('no-topic-link', card.id); continue; }
      const names = new Set(mapped.map(headingName));
      if (!headings.some(h => mapped.includes(h) || names.has(headingName(h)))) { miss('topic-differs', card.id); continue; }
      result.totals.cardsReaching++;
    }
    if (Object.keys(misses).length) result.cards[subject.id] = Object.fromEntries(Object.entries(misses).map(([k, v]) => [k, [...v!].sort()]));
  }
  // Check 2: every Atlas question in scope has a card.
  for (const s of LC) {
    const lang: PaperLang = s.id === 'irish' ? 'iv' : 'ev';
    const inScope = questionsForTopics(s.id, null).filter(q => q.year >= 2010 && q.year <= 2026 && q.lang === lang);
    if (!inScope.length) continue;
    const have = credited.get(s.id) ?? new Set();
    const missing: string[] = [];
    for (const q of inScope) {
      result.totals.atlasQuestions++;
      if (have.has(logicalQuestionIdentity(q))) result.totals.atlasQuestionsWithCard++;
      else missing.push(`${q.year}|${q.level}|${q.fileid}|${q.n}`);
    }
    if (missing.length) result.questions[s.id] = missing.sort();
  }
  return result;
}
