/** Validate the official English LCVP video identity before deck publication.
 * The original 2015 listing uses letter O in O31; do not normalise its filename.
 * A successful identity check does not replace the authoring source/media review.
 */
export function videoMaterialFault(card, subjectId) {
  const source = card.videoMaterial;
  if (source === undefined) return null;
  if (!source || typeof source !== 'object' || source.kind !== 'source-video') {
    return 'videoMaterial must be a source-video object';
  }
  if (subjectId !== 'lcvp' || card.level !== 'common') {
    return 'videoMaterial currently requires a verified LCVP common-level source';
  }
  if (card.audioMaterial) return 'videoMaterial includes its own audio; do not substitute a separate audio recording';
  for (const key of ['label', 'title', 'playbackUrl', 'secFileid', 'canonicalUrl', 'attribution', 'presentationNote']) {
    if (typeof source[key] !== 'string' || !source[key].trim()) return `videoMaterial.${key} is empty`;
  }
  let canonical;
  try {
    canonical = new URL(source.canonicalUrl);
    const playback = new URL(source.playbackUrl);
    if (canonical.protocol !== 'https:' || playback.protocol !== 'https:'
      || canonical.username || canonical.password || playback.username || playback.password) {
      return 'videoMaterial URLs must use HTTPS without embedded credentials';
    }
  } catch {
    return 'videoMaterial URLs must be absolute HTTPS URLs';
  }
  const identity = canonical.pathname.match(/^\/archive\/(exampapers|deferredexams)\/(\d{4})\/(LC462CLP[0O]31EV\.(?:mov|mp4))$/);
  if (canonical.hostname !== 'www.examinations.ie' || canonical.search || canonical.hash || !identity
    || Number(identity[2]) !== card.year || identity[3] !== source.secFileid) {
    return 'videoMaterial canonical URL must match the original English LCVP filename and examination year';
  }
  if (card.id.includes('-deferred-') !== (identity[1] === 'deferredexams')) {
    return 'videoMaterial recording sitting does not match the card';
  }
  return null;
}
