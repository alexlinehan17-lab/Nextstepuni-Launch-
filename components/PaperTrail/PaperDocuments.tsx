import type { PaperEntry, PaperItem, PaperTrailSubject } from '../../types/paperTrail';
import { paperStoragePath, paperUrl } from './storage';

/* The preview dialog ("The paper. The points.", Inspect, View as a pair) is
   gone with the agreed page (area 6a, 27 Nov 2026): each paper's and scheme's
   real cover, its size and its Open button are on the page itself, and
   pressing a cover opens that document. Every route of the dialog ended at the
   same Open. */

export type DocumentSide = 'paper' | 'scheme';
export const documentUrl = (subject: PaperTrailSubject, entry: PaperEntry, item: PaperItem, side: DocumentSide) => {
  const file = side === 'scheme' ? item.scheme : item.doc;
  return file ? paperUrl(paperStoragePath(subject.cycle, subject.id, entry.year, side, file.f)) : '';
};
