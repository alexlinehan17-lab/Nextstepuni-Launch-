/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Listening recordings play from a hosted, verified copy of the SEC's own
 * recording wherever one has been uploaded, and exactly as before elsewhere.
 *
 * The SEC blocks other sites from playing its mp3s, so the player loads a copy
 * kept in the app's Firebase Storage (components/MarkBank/audioStorage.ts).
 * scripts/markbank/audio-hosting/host_audio.py records each copy in
 * audio-manifest.json only after checking it: the bytes the SEC sent, their
 * sha256 against every earlier fingerprint, that they decode as MPEG audio,
 * and that the object read back from the bucket has the same size and MD5.
 * The app bundles just the uploaded paths (hostedAudio.json).
 *
 * Recordings still without a copy are pinned in
 * test/fixtures/hostedAudioMissing.ts, a list that only shrinks: a card whose
 * recording is neither hosted nor pinned fails here, and so does a pinned
 * recording that has since been uploaded.
 */

import { readFileSync } from 'node:fs';
import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import AudioSourcePlayer from '../components/MarkBank/AudioSourcePlayer';
import { audioPlaybackUrl, hostedAudioPath, secAudioStoragePath } from '../components/MarkBank/audioStorage';
import { builtDecks, loadCards } from '../components/MarkBank/deck';
import HOSTED_AUDIO from '../components/MarkBank/hostedAudio.json';
import manifest from '../scripts/markbank/audio-hosting/audio-manifest.json';
import type { CardAudioMaterial } from '../types/markBank';
import { HOSTED_AUDIO_MISSING } from './fixtures/hostedAudioMissing';

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

const MANIFEST = manifest as Record<string, HostedRecording>;
const BUCKET = 'nextstepuni-app.firebasestorage.app';
const storageUrl = (path: string) =>
  `https://firebasestorage.googleapis.com/v0/b/${BUCKET}/o/${encodeURIComponent(path)}?alt=media`;
// Every Topic Atlas recording file (data/frenchAudio.json, japaneseAudio.json, ...), new ones included.
const ATLAS_FILES = import.meta.glob<{ source: CardAudioMaterial }[]>('../data/*Audio.json', { eager: true, import: 'default' });
const ATLAS_SOURCES = Object.values(ATLAS_FILES).flatMap(recordings => recordings.map(r => r.source));

describe('hosted SEC listening recordings', () => {
  it('stores June recordings by year and file id, and deferred ones beside them', () => {
    expect(secAudioStoragePath('https://www.examinations.ie/archive/exampapers/2012/LC011ZLPO17EV.mp3'))
      .toBe('audio/2012/LC011ZLPO17EV.mp3');
    // The SEC reuses the June file id for the deferred sitting's recording.
    expect(secAudioStoragePath('https://www.examinations.ie/archive/deferredexams/2022/LC001ZLP017IV.mp3'))
      .toBe('audio/2022/LC001ZLP017IV-deferred.mp3');
    expect(secAudioStoragePath('https://example.com/2022/LC001ZLP017IV.mp3')).toBeNull();
    const elsewhere = { playbackUrl: 'https://example.com/a.mp3', canonicalUrl: 'https://example.com/a.mp3' };
    expect(audioPlaybackUrl(elsewhere)).toBe('https://example.com/a.mp3');
  });

  it('plays the hosted copy only where a verified upload is listed', () => {
    const hosted = 'https://www.examinations.ie/archive/exampapers/2012/LC011ZLPO17EV.mp3';
    expect(HOSTED_AUDIO).toContain('audio/2012/LC011ZLPO17EV.mp3');
    expect(audioPlaybackUrl({ canonicalUrl: hosted, playbackUrl: hosted })).toBe(storageUrl('audio/2012/LC011ZLPO17EV.mp3'));
    const pinned = HOSTED_AUDIO_MISSING[0];
    const [, year, file] = /^audio\/(\d{4})\/(.+)$/.exec(pinned)!;
    const sec = `https://www.examinations.ie/archive/exampapers/${year}/${file}`;
    expect(hostedAudioPath(sec)).toBeNull();
    expect(audioPlaybackUrl({ canonicalUrl: sec, playbackUrl: sec })).toBe(sec);
  });

  it('lists in the app exactly the copies whose upload was read back and matched', () => {
    const entries = Object.entries(MANIFEST);
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
    expect([...HOSTED_AUDIO]).toEqual(entries.filter(([, e]) => e.storage).map(([path]) => path).sort());
  });

  it('hosts every live listening recording, or pins it as still missing', async () => {
    const sources: CardAudioMaterial[] = [...ATLAS_SOURCES];
    for (const deck of builtDecks()) {
      for (const card of await loadCards(deck.subjectId, deck.level)) {
        if (card.audioMaterial) sources.push(card.audioMaterial);
      }
    }
    expect(sources.length).toBeGreaterThan(ATLAS_SOURCES.length);
    const problems = new Set<string>();
    const missing = new Set<string>();
    for (const audio of sources) {
      const path = secAudioStoragePath(audio.canonicalUrl);
      if (!path) { problems.add(`not an SEC archive recording: ${audio.canonicalUrl}`); continue; }
      const entry = MANIFEST[path];
      if (!hostedAudioPath(audio.canonicalUrl)) { missing.add(path); continue; }
      if (entry.canonicalUrl !== audio.canonicalUrl) problems.add(`${path} is a copy of ${entry.canonicalUrl}`);
      if (entry.secFileid !== audio.secFileid) problems.add(`${path} holds ${entry.secFileid}, the card names ${audio.secFileid}`);
      if (audioPlaybackUrl(audio) !== storageUrl(path)) problems.add(`${path} is not what the player loads`);
    }
    expect([...problems].sort()).toEqual([]);
    const pinned = new Set(HOSTED_AUDIO_MISSING);
    // A card whose recording has no copy and is not pinned: upload it.
    expect([...missing].filter(path => !pinned.has(path)).sort()).toEqual([]);
    // A pinned recording that is uploaded, or no longer used: take it off the list.
    expect([...pinned].filter(path => !missing.has(path)).sort()).toEqual([]);
  }, 180_000);

  it('plays a hosted copy credited to the SEC, still linking to the SEC recording', () => {
    const source = ATLAS_SOURCES.find(s => hostedAudioPath(s.canonicalUrl))!;
    const { container } = render(<AudioSourcePlayer source={source} />);
    const player = container.querySelector('audio')!;
    expect(player).toHaveAttribute('src', storageUrl(secAudioStoragePath(source.canonicalUrl)!));
    expect(container.textContent).toContain(`${source.presentationNote} ${source.attribution}`);
    fireEvent.error(player);
    expect(screen.getByRole('link', { name: 'Open the SEC recording' })).toHaveAttribute('href', source.canonicalUrl);
  });

  it('plays a recording without a copy exactly as before', () => {
    const source = ATLAS_SOURCES.find(s => !hostedAudioPath(s.canonicalUrl))!;
    const { container } = render(<AudioSourcePlayer source={source} />);
    const player = container.querySelector('audio')!;
    expect(player).toHaveAttribute('src', source.playbackUrl);
    expect(container.querySelector('p')!.textContent).toBe(source.presentationNote);
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
