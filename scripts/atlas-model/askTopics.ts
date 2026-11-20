/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The single model's topic record (plan section 5; Alex, 18 Nov 2026: "if it is under x in Mark Bank, it's under x
 * in Topic Atlas"). Every subject has ONE heading list, and every ask (card) is filed under the heading for what that
 * part asks. The decisions live in scripts/atlas-model/filings/<subject>.json (how each was decided:
 * CARD-STANDARD.md section 9); this module turns a filing into data/atlasModel/<subject>.json, which the Mark Bank
 * and the Topic Atlas both read (components/PaperTrail/atlasModel.ts). It is also what the automatic check re-runs,
 * so the committed record can never drift from the deck, the filing or the Atlas.
 */
import { SUBJECTS, loadCards, levelsFor } from '../../components/MarkBank/deck';
import { topicsForPaper } from '../../components/PaperTrail/topics';
import { examTopicDefinition } from '../../data/examTopics/registry';
import { CURRICULUM } from '../../curriculum';
import type { PaperLang, PaperLevel } from '../../types/paperTrail';
import type { SecCard } from '../../types/markBank';
import { addressContext, atlasAddress } from './cardAtlasAddress';
import { atlasSubjectFor } from './checks';

/** How a filing was decided: x = the card's topic crosswalks to one heading; xa = to several, narrowed to one by the
 *  Atlas question; j = a one-to-one join of the subject's two topic lists; r2 = two independent readers agreed;
 *  r1 = one reader, whose heading agrees with both the card's topic and the Atlas listing (not sampled for a second);
 *  r3 = a third reader settled a difference; rs = settled by evidence and confirmed by a sampled second reading. */
export type FilingHow = 'x' | 'xa' | 'j' | 'r1' | 'r2' | 'r3' | 'rs';

export interface SubjectFiling {
  v: 1;
  subject: string;
  /** Where the heading list comes from, in words. */
  headingSource: string;
  groups: Array<{ id: string; level: string; label: string; topics: string[] }>;
  /** card id -> [heading ids, how decided] */
  asks: Record<string, [string[], FilingHow]>;
}

export interface AskTopicFile {
  v: 2;
  subjectId: string;
  headingSource: string;
  groups: Array<{ id: string; level: string; label: string; topics: number[] }>;
  topics: Array<{ id: string; level: string; code: string; title: string }>;
  /** [Atlas subject, year, level, booklet, printed question number, [[card id, [topic index…]]…]] */
  questions: Array<[string, number, string, string, string, Array<[string, number[]]>]>;
  /** Asks whose printed question the Atlas does not list yet: [card id, [topic index…]]. */
  unplaced: Array<[string, number[]]>;
}

const FILINGS = import.meta.glob('./filings/*.json', { eager: true, import: 'default' }) as Record<string, SubjectFiling>;
export const FILED_SUBJECTS: string[] = Object.values(FILINGS).map(f => f.subject).sort();
/** Subjects the app reads (data/atlasModel/headings.json lists exactly these). Subjects join a few per pull request;
 *  physics, home-economics, maths, japanese, russian and lcvp join after the Codex release lands. */
export const MODEL_SUBJECTS: readonly string[] = ['biology', 'chemistry', 'agricultural-science',
  'business', 'accounting', 'economics', 'politics-and-society', 'religious-education', 'history',
  'maths', 'physics', 'lcvp', 'russian', 'home-economics'];
export const filingFor = (subject: string): SubjectFiling | null => Object.values(FILINGS).find(f => f.subject === subject) ?? null;

const curriculumLabel = new Map(CURRICULUM.flatMap(c => c.strands.flatMap(s => s.subtopics.map(t => [t.id, t.name] as const))));
const labelOf = (id: string) => examTopicDefinition(id)?.label ?? curriculumLabel.get(id) ?? null;
const splitLabel = (label: string) => {
  const m = /^((?:\d+(?:\.\d+)*\.?)|(?:U\d+)|(?:[A-J][.:])|(?:EUR\d\.)|(?:\d\.\s?IRL))\s+(.*)$/.exec(label.trim());
  return m ? { code: m[1].replace(/[.:]$/, ''), title: m[2] } : { code: '', title: label.trim() };
};

export interface AskDerivation { file: AskTopicFile; problems: string[] }

export async function deriveAskTopics(subjectId: string): Promise<AskDerivation> {
  const filing = filingFor(subjectId);
  if (!filing) throw new Error(`${subjectId} has no filing (scripts/atlas-model/filings/${subjectId}.json)`);
  const problems: string[] = [];
  const topicIds = [...new Set(filing.groups.flatMap(g => g.topics))];
  const index = new Map(topicIds.map((id, i) => [id, i]));
  const topics = topicIds.map(id => {
    const label = labelOf(id);
    if (!label) problems.push(`heading ${id} is neither an Atlas exam topic nor a curriculum topic`);
    const level = examTopicDefinition(id)?.level ?? 'all';
    return { id, level, ...splitLabel(label ?? id) };
  });
  const levelOk = (id: string, level: string) => { const l = topics[index.get(id)!].level; return l === 'all' || l === level || l === 'common' || level === 'common'; };
  const cards: SecCard[] = [];
  for (const level of levelsFor(subjectId)) cards.push(...await loadCards(subjectId, level));
  const ids = new Set(cards.map(c => c.id));
  for (const id of Object.keys(filing.asks)) if (!ids.has(id)) problems.push(`${id}: filed but not a card`);
  const home = atlasSubjectFor(subjectId) ?? subjectId;
  const ctx = addressContext(cards);
  const byQuestion = new Map<string, AskTopicFile['questions'][number]>();
  const unplaced: AskTopicFile['unplaced'] = [];
  for (const card of [...cards].sort((a, b) => a.id.localeCompare(b.id))) {
    const filed = filing.asks[card.id];
    if (!filed || !filed[0].length) { problems.push(`${card.id}: not filed`); continue; }
    const bad = filed[0].filter(id => !index.has(id) || !levelOk(id, card.level));
    if (bad.length) { problems.push(`${card.id}: ${bad.join(', ')} not a ${card.level} heading of the list`); continue; }
    const at = filed[0].map(id => index.get(id)!).sort((a, b) => a - b);
    const a = atlasAddress(card, home, ctx);
    let placed = false;
    if (!('fail' in a)) {
      const atlas = a.atlas ?? home;
      for (const lang of ['ev', 'iv'] as PaperLang[]) {
        const paper = topicsForPaper(atlas, card.year, card.level as PaperLevel, lang, a.fileid);
        if (!paper) continue;
        let n: string | undefined;
        for (const cand of a.cands) {
          if (typeof cand === 'string') n = paper.q.find(x => x.n === cand)?.n;
          else if (paper.q.some(x => x.n === cand.ifHas)) n = paper.q.find(x => x.n === cand.n)?.n;
          if (n) break;
        }
        if (!n) break;
        const key = `${atlas}|${card.year}|${card.level}|${paper.fileid}|${n}`;
        const entry = byQuestion.get(key) ?? [atlas, card.year, card.level, paper.fileid, n, []];
        entry[5].push([card.id, at]);
        byQuestion.set(key, entry);
        placed = true;
        break;
      }
    }
    if (!placed) unplaced.push([card.id, at]);
  }
  const questions = [...byQuestion.values()].sort((a, b) => a[0].localeCompare(b[0]) || b[1] - a[1] || a[2].localeCompare(b[2])
    || a[3].localeCompare(b[3]) || a[4].localeCompare(b[4], undefined, { numeric: true }));
  return {
    problems,
    file: {
      v: 2, subjectId, headingSource: filing.headingSource,
      groups: filing.groups.map(g => ({ id: g.id, level: g.level, label: g.label, topics: g.topics.map(id => index.get(id)!) })),
      topics, questions, unplaced,
    },
  };
}

/** Every Mark Bank subject with cards, for the coverage check that every one has a filing. */
export const CARDED_SUBJECTS = SUBJECTS.map(s => s.id);
