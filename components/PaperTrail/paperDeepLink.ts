import { findIndexedItem } from './indexLookup';

/** Resolve only an exact indexed document; a malformed link stays in the archive.
 *  Deferred-sitting papers live in their own entry for the year, so the link
 *  is matched across every entry of that year/level/language. */
export function resolvePaperDeepLink(subjectId: string, read: (name: string) => string | null) {
  const found = findIndexedItem(subjectId, Number(read('year')), read('level'), read('lang'), read('paper'));
  if (!found) return null;
  const { entry, item } = found;
  const side = read('side') === 'scheme' && item.scheme ? 'scheme' : 'paper';
  return { entry, item, side } as const;
}
