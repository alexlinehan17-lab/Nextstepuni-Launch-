/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Where a card's SEC recording or video is played from.
 *
 * Cards name the SEC's own file (`canonicalUrl`, `secFileid`). The SEC lets
 * its mp3s and videos (mp4, mov) play on its own pages but blocks them when
 * another site embeds them, so a student pressing play on
 * www.examinations.ie's address got an error. A verified copy of each file (same bytes, checked by sha256) is
 * kept in the app's Firebase Storage bucket, credited to the SEC, and played
 * from there. The card itself never changes: its SEC address and file id stay
 * the SEC's, and the player still links to the SEC's own copy.
 *
 * Only a file listed in hostedAudio.json plays from Storage. That list is
 * written by scripts/markbank/audio-hosting/host_audio.py after an upload has
 * been read back and matched; any other file plays exactly as before.
 *
 * Layout, as Paper Trail's papers: `audio/<year>/<secFileid>` for recordings,
 * `video/<year>/<secFileid>` for videos. The SEC reuses the June file id for a
 * deferred sitting's file in the same year, so a deferred one is
 * `<folder>/<year>/<stem>-deferred.<ext>`, the rule
 * scripts/paper-trail/build-index.py applies to deferred papers.
 */

import type { CardAudioMaterial } from '../../types/markBank';
import { paperUrl } from '../PaperTrail/storage';
import HOSTED_MEDIA from './hostedAudio.json';

const HOSTED = new Set<string>(HOSTED_MEDIA);

const SEC_ARCHIVE_MEDIA =
  /^https:\/\/www\.examinations\.ie\/archive\/(exampapers|deferredexams)\/(\d{4})\/([A-Za-z0-9]+)\.(mp3|mp4|mov)$/;

/** The Storage object for a copy of an SEC archive recording or video, or
 *  null when the address is not one. Says nothing about whether it exists. */
export function secAudioStoragePath(canonicalUrl: string): string | null {
  const match = SEC_ARCHIVE_MEDIA.exec(canonicalUrl);
  if (!match) return null;
  const [, archive, year, stem, extension] = match;
  const folder = extension === 'mp3' ? 'audio' : 'video';
  return `${folder}/${year}/${stem}${archive === 'deferredexams' ? '-deferred' : ''}.${extension}`;
}

/** The Storage object of a verified, uploaded copy of this file, or null. */
export function hostedAudioPath(canonicalUrl: string): string | null {
  const path = secAudioStoragePath(canonicalUrl);
  return path && HOSTED.has(path) ? path : null;
}

/** The address the audio or video player loads: the hosted copy where one has
 *  been uploaded and verified, otherwise the card's own playback address. */
export function audioPlaybackUrl(source: Pick<CardAudioMaterial, 'canonicalUrl' | 'playbackUrl'>): string {
  const path = hostedAudioPath(source.canonicalUrl);
  return path ? paperUrl(path) : source.playbackUrl;
}
