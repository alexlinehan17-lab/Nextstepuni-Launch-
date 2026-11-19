/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Every listening recording a student can press play on is a hosted, verified
 * copy of the SEC's own recording.
 *
 * The SEC blocks other sites from playing its mp3s, so the player loads a copy
 * kept in the app's Firebase Storage (components/MarkBank/audioStorage.ts).
 * scripts/markbank/audio-hosting/host_audio.py records each copy in
 * audio-manifest.json only after checking it: the bytes the SEC sent, their
 * sha256, that they decode as MPEG audio, and that the object read back from
 * the bucket has the same size and MD5. A card whose recording has no such
 * entry would play nothing, so it fails here, naming the recording.
 */

import { readFileSync } from 'node:fs';
import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import AudioSourcePlayer from '../components/MarkBank/AudioSourcePlayer';
import { audioPlaybackUrl, secAudioStoragePath } from '../components/MarkBank/audioStorage';
import { builtDecks, loadCards } from '../components/MarkBank/deck';
import frenchAudio from '../data/frenchAudio.json';
import germanAudio from '../data/germanAudio.json';
import spanishAudio from '../data/spanishAudio.json';
import manifest from '../scripts/markbank/audio-hosting/audio-manifest.json';
import type { CardAudioMaterial } from '../types/markBank';

interface HostedRecording {
  path: string;
  secFileid: string;
  canonicalUrl: string;
  bytes: number;
  sha256: string;
  md5: string;
  durationSeconds: number;
  storage?: {
    object: string;
    size: number;
    md5Hash: string;
    sha256Metadata: string;
    contentType: string;
  };
}

const HOSTED = manifest as Record<string, HostedRecording>;
const BUCKET = 'nextstepuni-app.firebasestorage.app';
const storageUrl = (path: string) =>
  `https://firebasestorage.googleapis.com/v0/b/${BUCKET}/o/${encodeURIComponent(path)}?alt=media`;

/** Why this recording would not play from a verified copy, or null. */
function unhosted(audio: CardAudioMaterial): string | null {
  const path = secAudioStoragePath(audio.canonicalUrl);
  if (!path) return `not an SEC archive recording: ${audio.canonicalUrl}`;
  const entry = HOSTED[path];
  if (!entry?.storage) return `${path} has no uploaded, verified copy`;
  if (entry.canonicalUrl !== audio.canonicalUrl) return `${path} is a copy of ${entry.canonicalUrl}`;
  if (entry.secFileid !== audio.secFileid) return `${path} holds ${entry.secFileid}, the card names ${audio.secFileid}`;
  if (audioPlaybackUrl(audio) !== storageUrl(path)) return `${path} is not what the player loads`;
  return null;
}

describe('hosted SEC listening recordings', () => {
  it('stores June recordings by year and file id, and deferred ones beside them', () => {
    expect(secAudioStoragePath('https://www.examinations.ie/archive/exampapers/2012/LC011ZLPO17EV.mp3'))
      .toBe('audio/2012/LC011ZLPO17EV.mp3');
    // The SEC reuses the June file id for the deferred sitting's recording.
    expect(secAudioStoragePath('https://www.examinations.ie/archive/deferredexams/2022/LC001ZLP017IV.mp3'))
      .toBe('audio/2022/LC001ZLP017IV-deferred.mp3');
    expect(secAudioStoragePath('https://example.com/2022/LC001ZLP017IV.mp3')).toBeNull();
    const elsewhere = {
      kind: 'source-audio', label: 'x', title: 'x', playbackUrl: 'https://example.com/a.mp3',
      secFileid: 'a.mp3', canonicalUrl: 'https://example.com/a.mp3', attribution: 'x', presentationNote: 'x',
    } as const;
    expect(audioPlaybackUrl(elsewhere)).toBe('https://example.com/a.mp3');
  });

  it('records only copies whose upload was read back and matched', () => {
    const entries = Object.entries(HOSTED);
    expect(entries.length).toBeGreaterThan(0);
    const wrong = entries.filter(([path, e]) => !(
      path === e.path
      && secAudioStoragePath(e.canonicalUrl) === path
      && e.canonicalUrl.endsWith(`/${e.secFileid}`)
      && /^[0-9a-f]{64}$/.test(e.sha256)
      && e.bytes > 0
      && e.durationSeconds > 60
      && e.storage?.object === `gs://${BUCKET}/${path}`
      && e.storage.size === e.bytes
      && e.storage.md5Hash === e.md5
      && e.storage.sha256Metadata === e.sha256
      && e.storage.contentType === 'audio/mpeg'
    )).map(([path]) => path);
    expect(wrong).toEqual([]);
  });

  it('gives every live listening card a verified copy of its own recording', async () => {
    const problems = new Set<string>();
    let cards = 0;
    for (const deck of builtDecks()) {
      for (const card of await loadCards(deck.subjectId, deck.level)) {
        if (!card.audioMaterial) continue;
        cards += 1;
        const problem = unhosted(card.audioMaterial);
        if (problem) problems.add(problem);
      }
    }
    expect(cards).toBeGreaterThan(0);
    expect([...problems].sort()).toEqual([]);
  }, 180_000);

  it('gives every Topic Atlas listening paper a verified copy of its recording', () => {
    const sources = [...frenchAudio, ...germanAudio, ...spanishAudio].map(r => r.source as CardAudioMaterial);
    expect(sources.length).toBeGreaterThan(0);
    expect(sources.map(unhosted).filter(Boolean)).toEqual([]);
  });

  it('plays the hosted copy, credits the SEC, and still links to the SEC recording', () => {
    const source = germanAudio[0].source as CardAudioMaterial;
    const { container } = render(<AudioSourcePlayer source={source} />);
    const player = container.querySelector('audio')!;
    expect(player).toHaveAttribute('src', storageUrl(secAudioStoragePath(source.canonicalUrl)!));
    expect(container.textContent).toContain(source.attribution);
    fireEvent.error(player);
    expect(screen.getByRole('link', { name: 'Open the SEC recording' })).toHaveAttribute('href', source.canonicalUrl);
  });

  it('lets every page load media from Firebase Storage', () => {
    const config = JSON.parse(readFileSync('firebase.json', 'utf8')) as {
      hosting: { headers: { headers: { key: string; value: string }[] }[] };
    };
    const policies = config.hosting.headers.flatMap(h => h.headers)
      .filter(h => h.key === 'Content-Security-Policy').map(h => h.value);
    expect(policies.length).toBeGreaterThan(0);
    for (const policy of policies) {
      const media = policy.split(';').map(d => d.trim()).find(d => d.startsWith('media-src'));
      expect(media?.split(/\s+/)).toContain('https://firebasestorage.googleapis.com');
    }
  });
});
