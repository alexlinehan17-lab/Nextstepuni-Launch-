/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The single model (plan section 5; Alex, 18 Nov 2026: "if it is under x in Mark Bank, it's under x in Topic
 * Atlas"): one topic record per ask, read by the Mark Bank and the Topic Atlas alike.
 *
 * - M1. The unit is the ask; its id is the card id. A printed question is the group of its asks.
 * - M2. One heading list per subject, shown the same in both tools (data/atlasModel/headings.json, small, eager).
 * - M3. Each ask's headings are stored once (data/atlasModel/<subject>.json, generated from
 *   scripts/atlas-model/filings/<subject>.json); a printed question's headings are its parts' headings. A subject's
 *   asks load only when that subject opens (loadAtlasModel), so no student downloads another subject's filing.
 * - M4. The link both ways: a card knows its Atlas question and heading; an Atlas question knows its cards.
 *
 * Free of the Atlas's tag files and the exam-topic registry, so the Mark Bank can import it without pulling the
 * Atlas into its chunk. Curriculum ids stay where they were (card.topicId, modules, quizzes, progress).
 */
import manifest from '../../data/atlasModel/headings.json';

interface ManifestSubject {
  subjectId: string;
  /** Atlas subjects that show this subject's questions (History: history and history-early-modern). */
  atlasIds: string[];
  headingSource: string;
  groups: Array<{ id: string; level: string; label: string; atlasId: string; topics: number[] }>;
  topics: Array<{ id: string; level: string; code: string; title: string }>;
}

interface AskTopicFile {
  v: 2;
  subjectId: string;
  /** [Atlas subject, year, level, booklet, printed question number, [[card id, [topic index…]]…]] */
  questions: Array<[string, number, string, string, string, Array<[string, number[]]>]>;
  /** Asks whose printed question the Atlas does not list yet. */
  unplaced: Array<[string, number[]]>;
}

export interface ModelHeading { id: string; level: string; code: string; title: string; label: string }
export interface ModelHeadingGroup { id: string; level: string; label: string; atlasId: string; topics: ModelHeading[] }

export interface AskRecord {
  cardId: string;
  subjectId: string;
  atlasSubjectId: string;
  year: number;
  level: string;
  /** The question booklet, as the Atlas files it ("LC025ALP040EV.pdf"); '' when the Atlas does not list it yet. */
  fileid: string;
  /** The printed question number the Atlas lists; '' when it does not list it yet. */
  n: string;
  topics: ModelHeading[];
}

const SUBJECTS = (manifest as { subjects: ManifestSubject[] }).subjects;
const bySubject = new Map<string, { entry: ManifestSubject; headings: ModelHeading[]; groups: ModelHeadingGroup[] }>();
const subjectOfAtlas = new Map<string, string>();
for (const entry of SUBJECTS) {
  const headings = entry.topics.map(t => ({ ...t, label: t.code ? `${t.code} ${t.title}` : t.title }));
  const groups = entry.groups.map(g => ({ id: g.id, level: g.level, label: g.label, atlasId: g.atlasId, topics: g.topics.map(i => headings[i]) }));
  bySubject.set(entry.subjectId, { entry, headings, groups });
  for (const atlasId of entry.atlasIds) subjectOfAtlas.set(atlasId, entry.subjectId);
}
/** The model subject (Mark Bank id) behind a Mark Bank or Atlas subject id. */
const modelSubjectOf = (id: string): string | undefined => (bySubject.has(id) ? id : subjectOfAtlas.get(id));

// Vite (the app, the checks) turns this into one lazy loader per subject. A script bundled without Vite has no
// import.meta.glob and registers the files itself (registerAtlasModelFile; scripts/landing/ask-topics.mjs).
let LOADERS: Record<string, () => Promise<unknown>> = {};
try {
  LOADERS = import.meta.glob(['../../data/atlasModel/*.json', '!../../data/atlasModel/headings.json'], { import: 'default' }) as Record<string, () => Promise<unknown>>;
} catch { LOADERS = {}; }
const loaded = new Map<string, Promise<void>>();
const ready = new Set<string>();
let version = 0;
const askById = new Map<string, AskRecord>();
const asksByQuestion = new Map<string, AskRecord[]>();

/** An Irish-language edition is the same printed question as its English one. */
const englishBooklet = (fileid: string) => fileid.replace(/IV(?=\.pdf$)/i, 'EV');
const questionKey = (atlasId: string, year: number, level: string, fileid: string, n: string) =>
  `${atlasId}|${year}|${level}|${englishBooklet(fileid)}|${n}`;

function register(file: AskTopicFile) {
  const subject = bySubject.get(file.subjectId);
  if (!subject || file.v !== 2) return;
  const { headings } = subject;
  for (const [atlasSubjectId, year, level, fileid, n, asks] of file.questions) {
    const group: AskRecord[] = [];
    for (const [cardId, topics] of asks) {
      const record: AskRecord = { cardId, subjectId: file.subjectId, atlasSubjectId, year, level, fileid, n, topics: topics.map(i => headings[i]) };
      askById.set(cardId, record);
      group.push(record);
    }
    asksByQuestion.set(questionKey(atlasSubjectId, year, level, fileid, n), group);
  }
  for (const [cardId, topics] of file.unplaced) {
    askById.set(cardId, { cardId, subjectId: file.subjectId, atlasSubjectId: subject.entry.atlasIds[0], year: 0, level: '', fileid: '', n: '', topics: topics.map(i => headings[i]) });
  }
}

/** Register one subject's filing that was read some other way (a build script without Vite). */
export function registerAtlasModelFile(file: unknown): void {
  const f = file as AskTopicFile;
  if (!f || f.v !== 2 || !bySubject.has(f.subjectId) || ready.has(f.subjectId)) return;
  register(f);
  ready.add(f.subjectId);
  loaded.set(f.subjectId, Promise.resolve());
  version++;
}

/** Does this subject (Mark Bank or Atlas id) read the one topic record? Known without loading anything. */
export const isModelSubject = (id: string): boolean => modelSubjectOf(id) !== undefined;

/** Have this subject's asks been loaded (loadAtlasModel)? */
export const isModelLoaded = (id: string): boolean => { const s = modelSubjectOf(id); return s !== undefined && ready.has(s); };

/** Bumped each time a subject's asks arrive, so memoised Atlas aggregates know to recompute. */
export const atlasModelVersion = (): number => version;

/** Load one subject's asks (Mark Bank or Atlas id). Resolves at once for a subject outside the model. */
export function loadAtlasModel(id: string): Promise<void> {
  const subjectId = modelSubjectOf(id);
  if (!subjectId) return Promise.resolve();
  let promise = loaded.get(subjectId);
  if (!promise) {
    const loader = Object.entries(LOADERS).find(([path]) => path.endsWith(`/${subjectId}.json`))?.[1];
    promise = (loader ? loader() : Promise.resolve(null)).then(file => {
      if (file) register(file as AskTopicFile);
      ready.add(subjectId);
      version++;
    });
    loaded.set(subjectId, promise);
  }
  return promise;
}

/** Every subject's asks: for build scripts and the automatic checks, never for a student's page. */
export const loadAllAtlasModels = (): Promise<void> => Promise.all(SUBJECTS.map(s => loadAtlasModel(s.subjectId))).then(() => undefined);

/** The record for one ask (card), or null outside the model or before its subject has loaded. */
export const askRecord = (cardId: string): AskRecord | null => askById.get(cardId) ?? null;

/** Every ask of one printed question (by its Atlas subject id), in card-id order. */
export const asksForQuestion = (atlasId: string, year: number, level: string, fileid: string, n: string): AskRecord[] =>
  asksByQuestion.get(questionKey(atlasId, year, level, fileid, n)) ?? [];

/** A printed question's headings are its parts' headings; null when the question has no asks loaded. */
export function modelTopicsForQuestion(atlasId: string, year: number, level: string, fileid: string, n: string): string[] | null {
  const asks = asksForQuestion(atlasId, year, level, fileid, n);
  if (!asks.length) return null;
  return [...new Set(asks.flatMap(ask => ask.topics.map(t => t.id)))];
}

/** The Mark Bank subject's one heading list (every level). */
export function modelHeadings(subjectId: string): ModelHeading[] | null {
  const id = modelSubjectOf(subjectId);
  return id ? bySubject.get(id)!.headings : null;
}

/** The Mark Bank's heading groups at one level ('all' groups too), in list order. */
export function modelHeadingGroups(subjectId: string, level: string): ModelHeadingGroup[] {
  const id = modelSubjectOf(subjectId);
  if (!id) return [];
  return bySubject.get(id)!.groups.filter(g => g.level === level || g.level === 'all')
    .map(g => ({ ...g, topics: g.topics.filter(t => t.level === level || t.level === 'all' || t.level === 'common' || level === 'common') }))
    .filter(g => g.topics.length);
}

/** The headings one Atlas subject shows (History's Later Modern list under history, Early Modern under
 *  history-early-modern), every level; null outside the model. */
export function atlasHeadingGroups(atlasId: string): ModelHeadingGroup[] | null {
  const id = subjectOfAtlas.get(atlasId);
  if (!id) return null;
  return bySubject.get(id)!.groups.filter(g => g.atlasId === atlasId);
}
export const atlasHeadings = (atlasId: string): ModelHeading[] | null => {
  const groups = atlasHeadingGroups(atlasId);
  return groups ? [...new Set(groups.flatMap(g => g.topics))] : null;
};

export const modelHeading = (id: string, topicId: string): ModelHeading | null =>
  modelHeadings(id)?.find(t => t.id === topicId) ?? null;

const LEVEL_WORD: Record<string, string> = { higher: 'Higher', ordinary: 'Ordinary', foundation: 'Foundation', common: 'Common' };

/** Where a card sits in the Topic Atlas, as a link the Mark Bank opens (the Atlas's own deep link, plus the
 *  question's year, level and number so the topic opens on it). Null until the card's subject has loaded. */
export function atlasLinkForCard(cardId: string): { href: string; heading: ModelHeading; question: string } | null {
  const ask = askRecord(cardId);
  if (!ask || !ask.topics.length || !ask.n) return null;
  const heading = ask.topics[0];
  const p = new URLSearchParams({ view: 'innovation-zone', tool: 'paper-trail', subject: ask.atlasSubjectId, topic: heading.id, year: String(ask.year), level: ask.level, q: ask.n });
  // Some Atlas lists number a paper's questions or parts in their own way (Agricultural Science 1001, 1002…;
  // Russian c1-1-i): name the printed question only when the Atlas number is one, the card shows its own citation.
  // A 2010-2019 Geography booklet files Part One as 1000 + its printed number (topics.ts questionLabel).
  const geographyPartOne = /^LC005[AG]LP000(EV|IV)\.pdf$/.test(ask.fileid) && Number(ask.n) > 1000 ? Number(ask.n) - 1000 : 0;
  const printed = geographyPartOne ? ` Part One Question ${geographyPartOne}`
    : /^\d{1,2}[a-z]?$|^[A-Z]{1,3}\d{0,2}$|^S\dQ\d{1,2}$|^\d{1,2}[A-Z]?\([a-z]+\)/.test(ask.n) ? ` Question ${ask.n}` : '';
  return { href: `/?${p.toString()}`, heading, question: `${ask.year} ${LEVEL_WORD[ask.level] ?? ask.level}${printed}` };
}

/** A link that opens the Mark Bank on exactly these cards (read once at boot by markBankDeepLink.ts). */
export function markBankLinkForCards(cardIds: string[]): string {
  const first = askRecord(cardIds[0] ?? '');
  const p = new URLSearchParams({ view: 'innovation-zone', tool: 'mark-bank', ...(first ? { mbsubject: first.subjectId, mblevel: first.level } : {}), cards: cardIds.join(',') });
  return `/?${p.toString()}`;
}
