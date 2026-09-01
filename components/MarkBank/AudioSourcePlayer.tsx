/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The listening source for Irish cards.  The real SEC recording stays on the
 * question side of the reveal, just as a printed passage does.  Native audio
 * controls are intentional: they retain scrubbing, playback-rate support and
 * VoiceOver behaviour inside both Safari and the iOS WKWebView shell.
 */

import React, { useState } from 'react';
import type { CardAudioMaterial } from '../../types/markBank';

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

  return (
    <section
      aria-label={`${source.label}, official listening recording`}
      style={{
        marginTop: 15,
        padding: '13px 14px 14px',
        border: '1px solid var(--mb-muted-border, #ddd8d1)',
        borderRadius: 12,
        background: 'var(--mb-raised)',
      }}
    >
      <div style={{ display: 'grid', gridTemplateColumns: '28px 1fr', gap: 9, alignItems: 'center' }}>
        <span style={{ color: 'var(--mb-ink, #26211d)', display: 'grid', placeItems: 'center' }}>
          <AudioWaveIcon />
        </span>
        <div>
          <span style={{
            display: 'block', fontSize: 9.5, fontWeight: 750, lineHeight: 1.4,
            letterSpacing: '.11em', textTransform: 'uppercase', color: 'var(--mb-label, #756e66)',
          }}>
            {source.label} · official audio
          </span>
          <strong style={{
            display: 'block', marginTop: 2, fontSize: 13.5, lineHeight: 1.35,
            color: 'var(--mb-ink, #26211d)',
          }}>
            {source.title}
          </strong>
        </div>
      </div>

      <audio
        controls
        preload="metadata"
        src={source.playbackUrl}
        onError={() => setFailed(true)}
        onCanPlay={() => setFailed(false)}
        style={{ display: 'block', width: '100%', height: 40, marginTop: 11 }}
      >
        Your browser does not support audio playback.
      </audio>

      {failed ? (
        <p style={{ margin: '8px 0 0', fontSize: 11.5, lineHeight: 1.45, color: 'var(--mb-muted, #756e66)' }}>
          The embedded recording could not be loaded.{' '}
          <a href={source.canonicalUrl} target="_blank" rel="noreferrer" style={{ color: 'inherit', fontWeight: 700 }}>
            Open the SEC recording
          </a>
          .
        </p>
      ) : (
        <p style={{ margin: '7px 0 0', fontSize: 10.5, lineHeight: 1.45, color: 'var(--mb-label, #756e66)' }}>
          {source.presentationNote}
        </p>
      )}
    </section>
  );
};

export default AudioSourcePlayer;
