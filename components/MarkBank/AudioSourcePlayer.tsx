/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The listening source for Irish cards.  The real SEC recording stays on the
 * question side of the reveal, just as a printed passage does.  Native audio
 * controls are intentional: they retain scrubbing, playback-rate support and
 * VoiceOver behaviour inside both Safari and the iOS WKWebView shell.
 * An SEC recording plays from the app's verified copy where one has been
 * uploaded (audioStorage.ts), because the SEC blocks other sites from
 * embedding its own address; the copy is credited to the SEC.
 */

import React, { useState } from 'react';
import type { CardAudioMaterial } from '../../types/markBank';
import { audioPlaybackUrl, hostedAudioPath } from './audioStorage';

interface AudioSourcePlayerProps {
  source: CardAudioMaterial;
}

const AudioWaveIcon = () => (
  <svg width="22" height="22" viewBox="0 0 22 22" fill="none" aria-hidden="true">
    <path d="M3 12.5v-3M7 15.5v-9M11 18v-14M15 15.5v-9M19 12.5v-3"
      stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" />
  </svg>
);

const AudioSourcePlayer: React.FC<AudioSourcePlayerProps> = ({ source }) => {
  const [failed, setFailed] = useState(false);
  const hosted = hostedAudioPath(source.canonicalUrl) !== null;

  return (
    <section
      aria-label={`${source.label}, official listening recording`}
      style={{
        marginTop: 15,
        padding: '13px 14px 14px',
        border: '1px solid var(--outline-soft)',
        borderRadius: 'var(--r-box)',
        background: 'var(--surface-paper)',
      }}
    >
      <div style={{ display: 'grid', gridTemplateColumns: '28px 1fr', gap: 9, alignItems: 'center' }}>
        <span style={{ color: 'var(--ink-primary)', display: 'grid', placeItems: 'center' }}>
          <AudioWaveIcon />
        </span>
        <div>
          <span style={{
            display: 'block', font: '400 11px/14px var(--font-ui)',
            letterSpacing: '.1em', textTransform: 'uppercase', color: 'var(--ink-muted)',
          }}>
            {source.label} · official audio
          </span>
          <strong style={{
            display: 'block', marginTop: 2, font: '400 15px/21px var(--font-ui)',
            color: 'var(--ink-primary)',
          }}>
            {source.title}
          </strong>
        </div>
      </div>

      <audio
        controls
        preload="metadata"
        src={audioPlaybackUrl(source)}
        onError={() => setFailed(true)}
        onCanPlay={() => setFailed(false)}
        style={{ display: 'block', width: '100%', height: 40, marginTop: 11 }}
      >
        Your browser does not support audio playback.
      </audio>

      {failed ? (
        <p style={{ margin: '8px 0 0', font: '400 13px/18px var(--font-ui)', color: 'var(--ink-secondary)' }}>
          The embedded recording could not be loaded.{' '}
          <a href={source.canonicalUrl} target="_blank" rel="noreferrer" style={{ color: 'var(--ink-primary)', textDecoration: 'underline', textUnderlineOffset: 3 }}>
            Open the SEC recording
          </a>
          .
        </p>
      ) : (
        <p style={{ margin: '7px 0 0', font: '400 13px/18px var(--font-ui)', color: 'var(--ink-muted)' }}>
          {source.presentationNote}{hosted ? ` ${source.attribution}` : null}
        </p>
      )}
    </section>
  );
};

export default AudioSourcePlayer;
