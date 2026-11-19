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
 * Only a recording listed in hostedAudio.json plays from Storage. That list is
 * written by scripts/markbank/audio-hosting/host_audio.py after an upload has
 * been read back and matched; any other recording plays exactly as before.
 *
 * Layout, as Paper Trail's papers: `audio/<year>/<secFileid>`. The SEC reuses
 * the June file id for a deferred sitting's recording in the same year, so a
 * deferred recording is `audio/<year>/<stem>-deferred.mp3`, the rule
 * scripts/paper-trail/build-index.py applies to deferred papers.
 */

import type { CardAudioMaterial } from '../../types/markBank';
import { paperUrl } from '../PaperTrail/storage';
import HOSTED_AUDIO from './hostedAudio.json';

const HOSTED = new Set<string>(HOSTED_AUDIO);

const SEC_ARCHIVE_RECORDING =
  /^https:\/\/www\.examinations\.ie\/archive\/(exampapers|deferredexams)\/(\d{4})\/([A-Za-z0-9]+\.mp3)$/;

/** The Storage object for a copy of an SEC archive recording, or null when
 *  the address is not one. Says nothing about whether the copy exists. */
export function secAudioStoragePath(canonicalUrl: string): string | null {
  const match = SEC_ARCHIVE_RECORDING.exec(canonicalUrl);
  if (!match) return null;
  const [, archive, year, fileid] = match;
  const name = archive === 'deferredexams' ? fileid.replace(/\.mp3$/i, '-deferred.mp3') : fileid;
  return `audio/${year}/${name}`;
}

/** The Storage object of a verified, uploaded copy of this recording, or null. */
export function hostedAudioPath(canonicalUrl: string): string | null {
  const path = secAudioStoragePath(canonicalUrl);
  return path && HOSTED.has(path) ? path : null;
}

/** The address the audio player loads: the hosted copy where one has been
 *  uploaded and verified, otherwise the card's own playback address. */
export function audioPlaybackUrl(source: Pick<CardAudioMaterial, 'canonicalUrl' | 'playbackUrl'>): string {
  const path = hostedAudioPath(source.canonicalUrl);
  return path ? paperUrl(path) : source.playbackUrl;
}
