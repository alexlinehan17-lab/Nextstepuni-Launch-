/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Which printed Topic Atlas question each Mark Bank card belongs to, for every subject: the address rules the
 * per-subject Atlas tests and committed join files already use, gathered in one place (ported from the 17 November
 * 2026 audit's 05_resolve.mjs). Build and check code only: the app reads the generated topic record
 * (components/PaperTrail/atlasModel.ts), never these join files, so none of this reaches a student's download.
 *
 * Rule classes: 'test' = copied from a committed test; 'join' = a committed join file; 'inferred' = the printed
 * question number in the card's reference (the audit's own inference, listed as such).
 */
import spanishAtlas from '../markbank/authoring/spanish-atlas.json';
import japaneseAtlas from '../markbank/authoring/japanese-atlas.json';
import italianAtlas from '../markbank/authoring/italian-atlas.json';
import irishSectionCredit from './irish-section-credit.json';
import physicalEducationTasks from '../../data/paperTrail/physicalEducationTasks.json';
import accountingAuthored from '../../components/MarkBank/cards/accounting/authored.json';
import agsciRuntime from '../../data/examTopics/agricultural-science-question-runtime.json';
import englishHigher from '../../components/MarkBank/cards/english/published-higher.json';
import englishOrdinary from '../../components/MarkBank/cards/english/published-ordinary.json';
import frenchTasks from '../../data/examTopics/french-reviewed-tasks.json';
import politicsTasks from '../../data/examTopics/politics-tasks.json';
import { historyAtlasQuestion } from '../../components/MarkBank/historyAtlas';
import type { SecCard } from '../../types/markBank';

export interface AtlasAddress {
  /** The Atlas subject the question is filed in (History's cards span two). */
  atlas?: string;
  fileid: string;
  /** Candidate printed numbers, first match wins; {ifHas, n} applies only when the paper lists ifHas. */
  cands: Array<string | { ifHas: string; n: string }>;
  cls: 'test' | 'join' | 'inferred';
  /** Parent rows a card also counts toward (an Irish part credits its question). */
  extraCredit?: string[];
  /** Further booklets the card's question is also printed in (English). */
  extraPlacements?: Array<{ fileid: string; n: string }>;
  /** Physical Education: the Atlas question IS the reviewed task row. */
  peTask?: boolean;
}
export type AddressResult = AtlasAddress | { fail: string; cls: string };

type Json = Record<string, unknown>;
const irishFiles = import.meta.glob('../../components/MarkBank/cards/irish/*authored.json', { eager: true, import: 'default' }) as Record<string, { cards?: Json[] }>;
const economicsReviews = import.meta.glob('../markbank/authoring/reviews/economics-*-ev.json', { eager: true, import: 'default' }) as Record<string, { fileid: string; questions: Array<{ n: string; tasks?: Array<{ cardId?: string }> }> }>;

const spanish = (spanishAtlas as { cards: Record<string, { fileid: string; n: string }> }).cards;
const japanese = (japaneseAtlas as { cards: Record<string, { fileid: string; n: string | null }> }).cards;
const italian = (italianAtlas as { cards: Record<string, { fileid: string; n: string | null }> }).cards;
const peByCard = new Map((physicalEducationTasks as Array<{ cardId: string; fileid: string; n: string }>).map(t => [t.cardId, t]));
const accByCard = new Map(((accountingAuthored as { cards: Json[] }).cards).map(c => [String(c.id), c]));
const agsciByCard = new Map(((agsciRuntime as { markBankCards: Json[] }).markBankCards).map(r => [String(r.cardId), r]));
const englishByCard = new Map([...(englishHigher as { cards: Json[] }).cards, ...(englishOrdinary as { cards: Json[] }).cards].map(c => [String(c.id), c]));
const frenchByCard = new Map((frenchTasks as Json[]).map(t => [String(t.cardId), t]));
const irishByCard = new Map(Object.values(irishFiles).flatMap(f => f.cards ?? []).map(c => [String(c.id), c]));
// Irish rows a card's own row also stands for: whole sections and choices, older whole-question rows, the scheme's
// language-accuracy rows (scripts/atlas-model/build-irish-section-credit.mjs; coordinator, 21 Nov).
const irishCredit = (irishSectionCredit as { papers: Record<string, Record<string, string[]>> }).papers;
const econByCard = new Map<string, { n: string }>();
for (const review of Object.values(economicsReviews)) for (const q of review.questions) for (const t of q.tasks ?? []) if (t.cardId) econByCard.set(t.cardId, { n: q.n });
const politicsByCard = new Map((politicsTasks as Json[]).map(t => [String(t.id), t]));

const pdf = (f: unknown) => `${String(f).replace(/\.pdf$/i, '')}.pdf`;
const qnum = (ref: string) => (/\bQ\s*(\d+)/.exec(ref) ?? [])[1];

/** Per-subject context read off the subject's own cards (German's straight-through counts, RE's printed sections). */
export function addressContext(cards: SecCard[]) {
  const GERMAN_TEXT: Record<string, string> = { T1: 'I', T2: 'II', T3: 'III' };
  const germanPrinted = new Map<string, Record<string, number>>();
  const reSections = new Map<string, string[]>();
  for (const c of cards) {
    const k = `${c.year}|${c.level}|${c.paperFileid}`;
    if (c.subjectId === 'german') {
      const m = /^\d{4} (?:HL|OL) Section (\w+) Q(\d*)/.exec(c.questionRef);
      if (m && GERMAN_TEXT[m[1]] && m[2]) { const counts = germanPrinted.get(k) ?? {}; counts[m[1]] = Math.max(counts[m[1]] ?? 0, Number(m[2])); germanPrinted.set(k, counts); }
    }
    if (c.subjectId === 'religious-education') { const set = reSections.get(k) ?? []; if (!set.includes(c.section)) set.push(c.section); reSections.set(k, set); }
  }
  for (const [k, v] of reSections) reSections.set(k, v.sort());
  return { GERMAN_TEXT, germanPrinted, reSections };
}

export function atlasAddress(c: SecCard, atlas: string, ctx: ReturnType<typeof addressContext>): AddressResult {
  const fid = pdf(c.paperFileid);
  const ref = c.questionRef;
  switch (c.subjectId) {
    case 'history': {
      const a = historyAtlasQuestion(c);
      return a ? { atlas: a.subjectId, fileid: a.fileid, cands: [a.n], cls: 'test' } : { fail: 'unreadable-ref', cls: 'test' };
    }
    case 'technology': {
      const m = /Section ([ABC]) Q(\d+)/.exec(ref); if (!m) return { fail: 'unreadable-ref', cls: 'test' };
      return { fileid: fid, cands: [m[1] === 'A' ? m[2] : `${m[1]}${m[2]}`], cls: 'test' };
    }
    case 'dcg': {
      const m = /Section ([ABC]) Q(\d)/.exec(ref); if (!m) return { fail: 'unreadable-ref', cls: 'test' };
      return { fileid: fid, cands: [m[1] === 'A' ? m[2] : String(m[1] === 'B' ? +m[2] : +m[2] + 3)], cls: 'test' };
    }
    case 'german': {
      const m = /^\d{4} (?:HL|OL) Section (\w+) Q(\d*)(?:\(([ab])\))?/.exec(ref); if (!m) return { fail: 'unreadable-ref', cls: 'test' };
      const [, section, q, letter] = m; let n: string | null = null;
      if (ctx.GERMAN_TEXT[section]) n = `${ctx.GERMAN_TEXT[section]}${q}`;
      else if (section === 'AG') n = 'G';
      else if ((section === 'AT' || section === 'SP') && letter) n = `${section === 'AT' ? 'T' : 'P'}-${letter.toUpperCase()}`;
      else if (/^L[1-4]$/.test(section)) n = section.slice(1);
      if (!n) return { fail: 'unreadable-ref', cls: 'test' };
      const cands: AtlasAddress['cands'] = [n];
      if (ctx.GERMAN_TEXT[section] && q) {
        const counts = ctx.germanPrinted.get(`${c.year}|${c.level}|${c.paperFileid}`) ?? {};
        const before = ['T1', 'T2', 'T3'].slice(0, ['T1', 'T2', 'T3'].indexOf(section));
        cands.push({ ifHas: '1', n: String(before.reduce((s, u) => s + (counts[u] ?? 0), 0) + Number(q)) });
        cands.push(ctx.GERMAN_TEXT[section]);
      }
      return { fileid: fid, cands, cls: 'test' };
    }
    case 'spanish': { const e = spanish[c.id]; return e ? { fileid: e.fileid, cands: [e.n], cls: 'join' } : { fail: 'no-join-entry', cls: 'join' }; }
    case 'physical-education': { const t = peByCard.get(c.id); return t ? { fileid: t.fileid, cands: [t.n], cls: 'join', peTask: true } : { fail: 'no-join-entry', cls: 'join' }; }
    case 'accounting': {
      const a = accByCard.get(c.id); if (!a) return { fail: 'no-join-entry', cls: 'join' };
      return { fileid: pdf(a.paperFileid), cands: [String(a.taskKey)], cls: 'join', extraCredit: [String(a.questionNumber)] };
    }
    case 'agricultural-science': {
      const a = agsciByCard.get(c.id); if (!a) return { fail: 'no-join-entry', cls: 'join' };
      return { fileid: pdf(a.fileid), cands: [String(a.n)], cls: 'join', extraCredit: [qnum(ref) ?? ''] };
    }
    case 'english': {
      const r = englishByCard.get(c.id) as { atlas?: { fileid: string; n: string }; atlasPlacements?: Array<{ fileid: string; n: string }> } | undefined;
      if (!r?.atlas) return { fail: 'no-join-entry', cls: 'join' };
      return { fileid: pdf(r.atlas.fileid), cands: [r.atlas.n], cls: 'join', extraPlacements: r.atlasPlacements ?? [] };
    }
    case 'french': {
      const t = frenchByCard.get(c.id);
      if (!t) {
        // A whole-question card the reviewed-task join does not list (Ordinary Section B Q1(a), the letter gap-fill,
        // 2021 and 2023-2025): the Atlas lists the question itself as B1A, over its gap rows.
        const m = /\bSection ([AB]) Q(\d+)\(([a-z])\)$/.exec(ref);
        if (!m) return { fail: 'no-join-entry', cls: 'join' };
        return { fileid: fid, cands: [`${m[1]}${m[2]}${m[3].toUpperCase()}`], cls: 'inferred' };
      }
      return { fileid: pdf(t.fileid), cands: [String(t.n)], cls: 'join', extraCredit: t.parent && t.parent !== t.n ? [String(t.parent)] : [] };
    }
    case 'irish': {
      const a = irishByCard.get(c.id) as { atlasQuestionId?: string } | undefined;
      if (!a?.atlasQuestionId) return { fail: 'no-join-entry', cls: 'join' };
      const parts = a.atlasQuestionId.split('-'); const chain: string[] = [];
      for (let i = parts.length - 1; i > 0; i--) chain.push(parts.slice(0, i).join('-'));
      const covering = irishCredit[`${c.year}|${fid}`]?.[a.atlasQuestionId] ?? [];
      return { fileid: fid, cands: [a.atlasQuestionId], cls: 'join', extraCredit: [...new Set([...chain, ...covering])] };
    }
    case 'economics': {
      const e = econByCard.get(c.id); if (e) return { fileid: fid, cands: [e.n], cls: 'join' };
      const q = qnum(ref); if (!q) return { fail: 'unreadable-ref', cls: 'inferred' };
      return { fileid: fid, cands: c.section === 'B' ? [`B${q}`, q] : [q], cls: 'inferred' };
    }
    case 'business': {
      const q = qnum(ref);
      if (/\bABQ\b/.test(ref)) return { fileid: fid, cands: ['ABQ'], cls: 'test' };
      if (!q) return { fail: 'unreadable-ref', cls: 'test' };
      if (c.year < 2020 && c.section === '3') return { fileid: fid, cands: [`S3Q${q}`], cls: 'test' };
      if (c.year < 2020 && c.section === '2') return { fileid: fid, cands: [`S2Q${q}`], cls: 'test' };
      return { fileid: fid, cands: [q], cls: 'test' };
    }
    case 'geography': {
      const m = /Part ([12]) Q(\d+)/.exec(ref); if (!m) return { fail: 'unreadable-ref', cls: 'test' };
      return { fileid: fid, cands: [c.year < 2020 && m[1] === '1' ? String(1000 + Number(m[2])) : m[2]], cls: 'test' };
    }
    case 'politics-and-society': { const t = politicsByCard.get(c.id); return t ? { fileid: pdf(t.fileid), cands: [String(t.n)], cls: 'join' } : { fail: 'no-join-entry', cls: 'join' }; }
    case 'art': { const m = /\bQ(\d+)/.exec(ref.split(' · ')[0]); return m ? { fileid: fid, cands: [m[1]], cls: 'test' } : { fail: 'unreadable-ref', cls: 'test' }; }
    case 'biology': case 'physics': case 'applied-maths': case 'construction-studies': case 'engineering': {
      const q = qnum(ref); return q ? { fileid: fid, cands: [q], cls: 'test' } : { fail: 'unreadable-ref', cls: 'test' };
    }
    case 'lcvp': {
      const q = qnum(ref); const off = ({ A: 0, B: 8, C: 11 } as Record<string, number>)[c.section];
      return q && off !== undefined ? { fileid: fid, cands: [String(off + Number(q))], cls: 'inferred' } : { fail: 'unreadable-ref', cls: 'inferred' };
    }
    case 'home-economics': {
      // Sections B and C share one booklet and both restart at Q1; the Atlas lists n 1-5 once, so a Section C card
      // has no Atlas question of its own.
      // Since the 19 Nov release some papers list Section C after Section B's five questions (2024: C Q1 is n 6).
      // The 2010-2019 paper (one booklet, LC098[AG]LP000EV) is listed straight through: Section A 1-12, Section B
      // 13-17, Section C 18-20. Where the card's own booklet lists row 13, Section B Qk is 12+k and Section C Qk 17+k;
      // the 2020-2026 Section B and C booklet (…039…) lists no row 13 and keeps the rule above (coordinator, 21 Nov).
      const k = qnum(ref); if (!k) return { fail: 'unreadable-ref', cls: 'inferred' };
      const n = Number(k);
      if (c.section === 'B') return { fileid: fid, cands: [{ ifHas: '13', n: String(12 + n) }, k], cls: 'inferred' };
      if (c.section === 'C') {
        return { fileid: fid, cands: [{ ifHas: '13', n: String(17 + n) }, { ifHas: String(5 + n), n: String(5 + n) }], cls: 'inferred' };
      }
      return { fileid: fid, cands: [k], cls: 'inferred' };
    }
    case 'religious-education': {
      const printed = ctx.reSections.get(`${c.year}|${c.level}|${c.paperFileid}`);
      const k = printed ? printed.indexOf(c.section) : -1;
      return k >= 0 ? { fileid: fid, cands: [String(k + 1)], cls: 'inferred' } : { fail: 'unreadable-ref', cls: 'inferred' };
    }
    case 'classical-studies': {
      const t = /\bTopic (\d{1,2})\(/.exec(ref); if (t) return { fileid: fid, cands: [t[1]], cls: 'inferred' };
      const q = qnum(ref); return q ? { fileid: fid, cands: [q], cls: 'inferred' } : { fail: 'unreadable-ref', cls: 'inferred' };
    }
    case 'russian': {
      // The Atlas numbers Russian parts by the card id's own suffix (c1-1-i, la1-ii, sd); 2019-2020 aural lists 1-4.
      const m = /^ru-\d{4}-(?:hl|ol)-(?:deferred-)?(.+)$/.exec(c.id);
      if (!m) return { fail: 'unreadable-ref', cls: 'inferred' };
      const aural = /^l(\d)$/.exec(m[1]);
      return { fileid: fid, cands: aural ? [m[1], { ifHas: aural[1], n: aural[1] }] : [m[1]], cls: 'inferred' };
    }
    case 'japanese': {
      // The Atlas numbers each Japanese paper straight through, with labels that change by year: a committed join.
      const e = japanese[c.id];
      return e?.n ? { fileid: e.fileid, cands: [e.n], cls: 'join' } : { fail: e ? 'no-atlas-question' : 'no-join-entry', cls: 'join' };
    }
    case 'italian': {
      // The Atlas numbers each Italian paper straight through by section: a committed join, like Japanese.
      const e = italian[c.id];
      return e?.n ? { fileid: e.fileid, cands: [e.n], cls: 'join' } : { fail: e ? 'no-atlas-question' : 'no-join-entry', cls: 'join' };
    }
    case 'bulgarian': case 'croatian': case 'czech': case 'danish': case 'dutch': case 'estonian': case 'finnish':
    case 'hungarian': case 'latvian': case 'maltese': case 'modern-greek': case 'romanian': case 'slovakian':
    case 'slovenian': case 'swedish': case 'ukrainian': {
      // The Atlas lists only Part I (Q1-Q6) for these sixteen languages: a Section II or III card restarts at Q1 and
      // must not land on Part I's question (Modern Greek prints its sections as 1, 2, 3). Unlinked until the
      // small-languages lane adds the Part II/III rows and its section-qualified rule (coordinator, 20 Nov); listed
      // with that reason in test/fixtures/atlasModelRuledMisses.json.
      if (/\bSection (?:II|III|2|3)\b/.test(ref)) return { fail: 'no-atlas-question', cls: 'inferred' };
      const q = qnum(ref); return q ? { fileid: fid, cands: [q], cls: 'inferred' } : { fail: 'unreadable-ref', cls: 'inferred' };
    }
    case 'polish': case 'portuguese': {
      // A listening card cites "Section L<A-E> Q<n>" and carries the listening booklet's file id (…LPA00…, build-deck's
      // resolver, queue 3); the Atlas lists that booklet one row per part, A to E. The card's own Q<n> numbers the
      // question inside its part, so it never addresses the booklet's rows.
      const l = /\bSection L([A-E])\b/.exec(ref);
      if (l) return { fileid: fid, cands: [String('ABCDE'.indexOf(l[1]) + 1)], cls: 'inferred' };
      // The old Portuguese paper (2010-2021): Section I's questions are Atlas 1-6, then Section II (the commentary) is
      // Atlas 7 and Section III (the discursive essay) Atlas 8; their own Q<n> restarts at 1 (coordinator, 20 Nov).
      const later = c.subjectId === 'portuguese' && c.year <= 2021 ? /\bSection (II|III)\b/.exec(ref) : null;
      if (later) return { fileid: fid, cands: [later[1] === 'II' ? '7' : '8'], cls: 'inferred' };
      // The Polish paper to 2021: the Atlas lists it by part. 2010-2020: Część I, II, III (two Część III rows in some
      // years, one per essay title); 2021: Section I's six questions, then Część II as row 7. A card's own Q<n> restarts
      // in every section, so it addresses its part's row, never Section I's question or part of the same number.
      const part = c.subjectId === 'polish' && c.year <= 2021 ? /\bSection (I{1,3})\b/.exec(ref)?.[1] : undefined;
      if (part && c.year === 2021 && part !== 'I') return { fileid: fid, cands: ['7'], cls: 'inferred' };
      if (part && c.year <= 2020) {
        const cands = part === 'I' ? ['1'] : part === 'II' ? ['2'] : qnum(ref) === '2' ? ['4', '3'] : ['3'];
        return { fileid: fid, cands, cls: 'inferred' };
      }
      const q = qnum(ref); return q ? { fileid: fid, cands: [q], cls: 'inferred' } : { fail: 'unreadable-ref', cls: 'inferred' };
    }
    default: {
      void atlas;
      const q = qnum(ref); return q ? { fileid: fid, cands: [q], cls: 'inferred' } : { fail: 'unreadable-ref', cls: 'inferred' };
    }
  }
}
