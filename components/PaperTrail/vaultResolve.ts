/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — resolve a topic sibling (subject/year/level/lang/fileid) to
 * its Storage URLs via the committed index. Pure lookup, no fetching.
 */

import { type PaperAnswerMap } from '../../types/paperTrail';
import { PAPER_TRAIL_INDEX, PAPER_TRAIL_SUBJECTS } from '../../paperTrailData';
import { paperAnswersPath, paperStoragePath, paperUrl } from './storage';
import { type TopicSibling } from './topics';

export interface ResolvedSibling {
  paperUrl: string;
  /** Null when the index has no scheme for this paper. */
  schemeUrl: string | null;
  answersUrl: string;
  /** Hosted paper-side-only anchor sidecar (public/paper-anchors/, deployed
   *  with the app — no Storage object). Tried when `answersUrl` misses; same
   *  PaperAnswerMap schema with mode:'pagejump' throughout, so the card gets
   *  its paper crop while the answer toggle stays on the honest
   *  "Open beside its marking scheme" fallback. */
  anchorsUrl: string;
  paperLabel: string;
  /** True when the hosted anchors must be tried before the Storage sidecar
   *  (numbering-conflict subject — see VAULT_PREFER_ANCHORS). */
  preferAnchors: boolean;
}

/** Hosting path for a paper's committed paper-anchors sidecar. Year + fileid
 *  is unique (fileids recur across years but encode exam/subject/level/
 *  component/lang), mirroring scripts/paper-trail/answers/<year>/<fileid>.json. */
export const hostedAnchorsUrl = (year: number, fileid: string) =>
  `/paper-anchors/${year}/${encodeURIComponent(fileid)}.json`;

/**
 * A small, audited set of rich answer maps is shipped with Hosting while its
 * corresponding Storage object is missing or stale.  Unlike paper-anchors,
 * these maps retain the verified marking-scheme regions, so both Topic Atlas
 * and the full-paper Answers tool can reveal the correct scheme crop.
 *
 * Keep this list deliberately narrow: each entry must have been visually
 * reviewed and must exist under public/paper-answers/.  Once the identical
 * Storage object is live, an entry can be removed without changing callers.
 */
export const HOSTED_ANSWER_OVERRIDES = new Set([
  'physics|2012|LC021ALP000EV.pdf',
  'physics|2024|LC021ALP000EV.pdf',
  'physics|2024|LC021ALP000IV.pdf',
  'physics|2025|LC021ALP000EV.pdf',
  'physics|2025|LC021ALP000IV.pdf',
  'physics|2025|LC021GLP000EV.pdf',
  'physics|2025|LC021GLP000IV.pdf',
  // Art's 2023–2026 written-paper cards were added during the factual-topic
  // audit. The corresponding Storage sidecars are absent/stale, so serve the
  // regenerated, visually reviewed maps from Hosting until Storage catches up.
  'art|2023|LC014ALP000EV.pdf',
  'art|2023|LC014ALP000IV.pdf',
  'art|2023|LC014GLP000EV.pdf',
  'art|2023|LC014GLP000IV.pdf',
  'art|2024|LC014ALP000EV.pdf',
  'art|2024|LC014ALP000IV.pdf',
  'art|2024|LC014GLP000EV.pdf',
  'art|2024|LC014GLP000IV.pdf',
  'art|2025|LC014ALP000EV.pdf',
  'art|2025|LC014ALP000IV.pdf',
  'art|2025|LC014GLP000EV.pdf',
  'art|2025|LC014GLP000IV.pdf',
  'art|2026|LC014ALP000EV.pdf',
  'art|2026|LC014ALP000IV.pdf',
  'art|2026|LC014GLP000EV.pdf',
  'art|2026|LC014GLP000IV.pdf',
]);

export const hostedAnswersUrl = (year: number, fileid: string) =>
  `/paper-answers/${year}/${encodeURIComponent(fileid)}.json`;

/** Prefer a committed, visually audited answer map over a missing/stale live
 * Storage sidecar. All other papers continue to use Storage. */
export const preferredAnswersUrl = (
  subjectId: string,
  year: number,
  fileid: string,
  storageUrl: string,
) => HOSTED_ANSWER_OVERRIDES.has(`${subjectId}|${year}|${fileid}`)
  ? hostedAnswersUrl(year, fileid)
  : storageUrl;

/**
 * Subjects whose classic Storage sidecar uses a DIFFERENT question numbering
 * than the Topic Vault tags, so the hosted paper-anchors (generated to match
 * the tags) must be tried FIRST — otherwise the vault serves crops the tags
 * don't describe.
 *
 * Geography: the classic sidecar (built for the full-paper Viewer) numbers the
 * Part-Two structured/essay questions 1..12; the vault tags number the Part-One
 * short questions 1..12 — the same paper carries two "Q1..12" runs. Without this
 * preference the vault shows a Part-Two essay crop under a Part-One topic.
 * (jc-italian / jc-french have the mirror problem the other way — their hosted
 * anchors are printed-numbered while the tags are reading-section-numbered — so
 * those anchors are REMOVED rather than preferred; see the audit.)
 *
 * Irish (TV-12): the LIVE Storage sidecars for Paper 2 (HL and OL) are STALE
 * early maps that anchor the léamhthuiscint passage's numbered PARAGRAPHS
 * (HL: 6 q, non-monotonic; OL: 5 q on the passage pages) — not the reading
 * questions the tags number 1..12 / 1..10. The corrected scheme-mapped
 * sidecars exist in scripts/paper-trail/answers/ but can't be uploaded while
 * Storage credentials are blocked (task #94), so without this preference the
 * vault serves paragraph crops. Every tagged irish fileid has hosted anchors
 * (HL P2 2013-25, OL P2 2013-25, foundation aural 2010-11 — the latter's
 * Storage sidecar 404s anyway, so it changes nothing there). When #94 lands
 * and the corrected answers/ sidecars go live, remove 'irish' from this map
 * to restore the richer crop+reveal maps.
 *
 * Japanese: the complete audited repair set currently lives in the repo while
 * Storage still carries a mixture of absent and pre-repair sidecars. Generated
 * hosted anchors preserve all 93 paper variants plus the additive
 * section-restart/end-bound metadata, so prefer those honest paper crops until
 * the audited Storage upload completes. This temporarily withholds inline
 * Japanese answer reveals rather than serving stale or mismatched scheme crops.
 *
 * German: the legacy Topic Atlas numbering enumerates reading questions while
 * several Storage maps insert grammar and short-writing cards into the same
 * numeric run. The complete audited hosted set uses stable semantic identities
 * for all 100 written/aural variants, so it must win until matching answer maps
 * are uploaded; otherwise (for example) a retained Reading Q5 can open the
 * Storage map's Grammar Q5.
 *
 * Religious Education: the classic sidecars are uneven section maps (some
 * editions expose only the numbered Section-A questions, others omit whole
 * lettered sections). The audited hosted maps use one stable card for every
 * printed section across all 58 local editions, including the five index
 * variants without a classic answer map. Prefer them until the complete
 * section maps are uploaded; inline answer reveal remains honestly disabled.
 *
 * The preference is PER-FILEID, not per-subject (TV-Q audit finding 1): the
 * geography dual-numbering conflict only exists on the combined-era single
 * booklets (…LP000…, one PDF carrying both Part One 1..12 and Part Two 1..12).
 * The split-era 2020+ booklets (…LP042/LP043…) have unambiguous numbering,
 * correct Storage sidecars, and NO hosted anchors — a blanket subject rule
 * starved them into the "can't be shown as a crop yet" fallback.
 */
export const VAULT_PREFER_ANCHORS = new Map<string, (fileid: string) => boolean>([
  ['geography', fileid => fileid.includes('LP000')],
  ['german', () => true],
  ['irish', () => true],
  ['japanese', () => true],
  ['religious-education', () => true],
]);

/** Ordered answer-map candidates. Normally the verified Storage sidecar first
 *  (it may carry scheme crops), then the hosted paper-only anchors. But for a
 *  numbering-conflict subject (VAULT_PREFER_ANCHORS) the classic Storage sidecar
 *  is systematically numbered against a DIFFERENT question run than the tags
 *  (geography: Part-Two essays vs the tags' Part-One shorts), so it is WRONG for
 *  every vault tag — we use only the hosted anchors, and a paper with no anchor
 *  falls back honestly to "open in the full paper" rather than showing the wrong
 *  crop. */
export const answerMapUrls = (r: ResolvedSibling): string[] =>
  r.preferAnchors ? [r.anchorsUrl] : [r.answersUrl, r.anchorsUrl];

/**
 * Shape guard for a fetched answer map. Firebase Hosting rewrites every
 * unknown path to index.html with HTTP 200, so a missing hosted sidecar comes
 * back as HTML (JSON parse fails) — and any other valid-JSON-but-wrong-shape
 * response must also read as a miss, never reach the renderer.
 */
export function isAnswerMap(v: unknown): v is PaperAnswerMap {
  if (typeof v !== 'object' || v === null) return false;
  const m = v as Record<string, unknown>;
  if (typeof m.paperFileid !== 'string' || !Array.isArray(m.q) || m.q.length === 0) return false;
  if (
    m.maxCropPages !== undefined
    && (!Number.isInteger(m.maxCropPages) || (m.maxCropPages as number) < 1 || (m.maxCropPages as number) > 10)
  ) return false;
  return m.q.every((q: unknown) => {
    if (typeof q !== 'object' || q === null) return false;
    const x = q as Record<string, unknown>;
    return (
      typeof x.n === 'string' &&
      typeof x.pP === 'number' && x.pP >= 1 &&
      Array.isArray(x.pY) && x.pY.length === 2 && x.pY.every(y => typeof y === 'number') &&
      Array.isArray(x.region) &&
      (x.mode === 'crop' || x.mode === 'pagejump')
    );
  });
}

/**
 * Preserve a verified scheme map while overlaying the independently audited
 * paper-side coordinates from a hosted paper-only map. This matters when the
 * classic answer map has a correct scheme crop but only a one-page paper start
 * anchor (for example Computer Science Section C). No scheme field is taken
 * from the paper-only map.
 */
export function mergePaperAnchorMetadata(
  answerMap: PaperAnswerMap,
  paperMap: PaperAnswerMap,
  n: string,
): PaperAnswerMap {
  if (
    paperMap.paperOnly !== 1
    || answerMap.paperOnly === 1
    || answerMap.paperFileid !== paperMap.paperFileid
  ) return answerMap;
  const answerQuestion = answerMap.q.find(question => question.n === n);
  const paperQuestion = paperMap.q.find(question => question.n === n);
  if (!answerQuestion || !paperQuestion) return answerMap;

  const mergedQuestion = {
    ...answerQuestion,
    pP: paperQuestion.pP,
    pY: [...paperQuestion.pY] as [number, number],
    ...(paperQuestion.paperRegion ? { paperRegion: paperQuestion.paperRegion } : {}),
    ...(paperQuestion.endP !== undefined ? { endP: paperQuestion.endP } : {}),
    ...(paperQuestion.endY !== undefined ? { endY: paperQuestion.endY } : {}),
    ...(paperQuestion.printOrder !== undefined ? { printOrder: paperQuestion.printOrder } : {}),
    ...(paperQuestion.label ? { label: paperQuestion.label } : {}),
  };
  const maxCropPages = Math.max(
    answerMap.maxCropPages ?? 0,
    paperMap.maxCropPages ?? 0,
  );
  return {
    ...answerMap,
    ...(maxCropPages ? { maxCropPages } : {}),
    q: answerMap.q.map(question => question.n === n ? mergedQuestion : question),
  };
}

const cycleById = new Map(PAPER_TRAIL_SUBJECTS.map(s => [s.id, s.cycle]));

/** In-memory memo — the vault feed resolves the same tuple repeatedly. */
const memo = new Map<string, ResolvedSibling | null>();

export function resolveSibling(t: TopicSibling): ResolvedSibling | null {
  const key = `${t.subjectId}|${t.year}|${t.level}|${t.lang}|${t.fileid}`;
  if (memo.has(key)) return memo.get(key)!;
  const cycle = cycleById.get(t.subjectId);
  const entry = (PAPER_TRAIL_INDEX[t.subjectId] ?? []).find(
    e => e.year === t.year && e.level === t.level && e.lang === t.lang,
  );
  const item = entry?.papers.find(p => p.doc.f === t.fileid);
  const out: ResolvedSibling | null = cycle && item
    ? {
        paperUrl: paperUrl(paperStoragePath(cycle, t.subjectId, t.year, 'paper', item.doc.f)),
        schemeUrl: item.scheme
          ? paperUrl(paperStoragePath(cycle, t.subjectId, t.year, 'scheme', item.scheme.f))
          : null,
        answersUrl: preferredAnswersUrl(
          t.subjectId,
          t.year,
          item.doc.f,
          paperUrl(paperAnswersPath(cycle, t.subjectId, t.year, item.doc.f)),
        ),
        anchorsUrl: hostedAnchorsUrl(t.year, item.doc.f),
        paperLabel: item.label,
        preferAnchors: VAULT_PREFER_ANCHORS.get(t.subjectId)?.(item.doc.f) ?? false,
      }
    : null;
  memo.set(key, out);
  return out;
}
