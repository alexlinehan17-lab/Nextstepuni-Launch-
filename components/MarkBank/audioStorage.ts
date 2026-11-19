/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Where a listening card's recording is played from.
 *
 * Cards name the SEC's own recording (`canonicalUrl`, `secFileid`). The SEC
 * lets its mp3s play on its own pages but blocks them when another site embeds
 * them, so a student pressing play on www.examinations.ie's address got an
 * error. A verified copy of each recording (same bytes, checked by sha256) is
 * kept in the app's Firebase Storage bucket, credited to the SEC, and played
 * from there. The card itself never changes: its SEC address and file id stay
 * the SEC's, and the player still links to the SEC's own copy.
 *
 * Layout, as Paper Trail's papers: `audio/<year>/<secFileid>`. The SEC reuses
 * the June file id for a deferred sitting's recording in the same year, so a
 * deferred recording is `audio/<year>/<stem>-deferred.mp3`, the rule
 * scripts/paper-trail/build-index.py applies to deferred papers. The upload,
 * and the record of every copy, is scripts/markbank/audio-hosting/.
 */

import type { CardAudioMaterial } from '../../types/markBank';
import { paperUrl } from '../PaperTrail/storage';

const SEC_ARCHIVE_RECORDING =
  /^https:\/\/www\.examinations\.ie\/archive\/(exampapers|deferredexams)\/(\d{4})\/([A-Za-z0-9]+\.mp3)$/;

/** The Storage object holding the hosted copy of an SEC archive recording,
 *  or null when the address is not one. */
export function secAudioStoragePath(canonicalUrl: string): string | null {
  const match = SEC_ARCHIVE_RECORDING.exec(canonicalUrl);
  if (!match) return null;
  const [, archive, year, fileid] = match;
  const name = archive === 'deferredexams' ? fileid.replace(/\.mp3$/i, '-deferred.mp3') : fileid;
  return `audio/${year}/${name}`;
}

/** The address the audio player loads: the hosted copy of an SEC recording,
 *  otherwise the card's own playback address. */
export function audioPlaybackUrl(source: Pick<CardAudioMaterial, 'canonicalUrl' | 'playbackUrl'>): string {
  const path = secAudioStoragePath(source.canonicalUrl);
  return path ? paperUrl(path) : source.playbackUrl;
}
