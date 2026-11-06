/** Source checks for recordings carried by generated Mark Bank point cards. */
import { resolveCompanionFileid } from './paperIndex.mjs';

const SEPARATE_AURAL_SUBJECTS = new Set(['japanese', 'russian']);

/** These languages publish the listening questions in a separate booklet. */
export function audioQuestionPaperFileid(card, subjectId) {
  if (!card.audioMaterial || !SEPARATE_AURAL_SUBJECTS.has(subjectId)) return undefined;
  // The companion resolver addresses main sittings. Do not silently attach
  // a deferred question to that main booklet while admitting another sitting.
  if (card.id.includes('-deferred-')) return null;
  return resolveCompanionFileid(subjectId, card.year, card.level, 'Aural Paper');
}

export function audioMaterialFault(card, subjectId) {
  const source = card.audioMaterial;
  if (source === undefined) return null;
  if (!source || typeof source !== 'object' || source.kind !== 'source-audio') {
    return 'audioMaterial must be a source-audio object';
  }
  for (const key of ['label', 'title', 'playbackUrl', 'secFileid', 'canonicalUrl', 'attribution', 'presentationNote']) {
    if (typeof source[key] !== 'string' || !source[key].trim()) return `audioMaterial.${key} is empty`;
  }
  let canonical;
  try {
    canonical = new URL(source.canonicalUrl);
    const playback = new URL(source.playbackUrl);
    if (canonical.protocol !== 'https:' || playback.protocol !== 'https:'
      || canonical.username || canonical.password || playback.username || playback.password) {
      return 'audioMaterial URLs must use HTTPS without embedded credentials';
    }
  } catch {
    return 'audioMaterial URLs must be absolute HTTPS URLs';
  }
  const identity = canonical.pathname.match(/^\/archive\/(exampapers|deferredexams)\/(\d{4})\/(LC\d{3}[A-Z]L?P[0-9A-Z]{3,4}[BEI]V\.mp3)$/);
  if (canonical.hostname !== 'www.examinations.ie' || canonical.search || canonical.hash || !identity
    || Number(identity[2]) !== card.year || identity[3] !== source.secFileid) {
    return 'audioMaterial canonical URL must match its SEC filename and examination year';
  }
  if (card.id.includes('-deferred-') !== (identity[1] === 'deferredexams')) {
    return 'audioMaterial recording sitting does not match the card';
  }
  const booklet = audioQuestionPaperFileid(card, subjectId);
  if (booklet === null) return 'audioMaterial has no uniquely indexed Aural Paper';
  if (booklet && booklet.slice(0, 5) !== source.secFileid.slice(0, 5)) {
    return 'audioMaterial recording belongs to a different subject from the Aural Paper';
  }
  return null;
}
