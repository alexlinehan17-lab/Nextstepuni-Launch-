import { PAPER_TRAIL_INDEX } from '../../paperTrailData';

/** Resolve only an exact indexed document; a malformed link stays in the archive. */
export function resolvePaperDeepLink(subjectId: string, read: (name: string) => string | null) {
  const entry = (PAPER_TRAIL_INDEX[subjectId] ?? []).find(candidate =>
    candidate.year === Number(read('year')) && candidate.level === read('level') && candidate.lang === read('lang'));
  const item = entry?.papers.find(candidate => candidate.doc.f === read('paper'));
  if (!entry || !item) return null;
  const side = read('side') === 'scheme' && item.scheme ? 'scheme' : 'paper';
  return { entry, item, side } as const;
}
