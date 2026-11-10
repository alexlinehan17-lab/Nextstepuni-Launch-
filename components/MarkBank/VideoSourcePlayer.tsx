/** Official examination video, with native playback, seeking and fullscreen. */
import React, { useState } from 'react';
import type { CardVideoMaterial } from '../../types/markBank';

const VideoSourcePlayer: React.FC<{ source: CardVideoMaterial }> = ({ source }) => {
  const [failedUrl, setFailedUrl] = useState<string | null>(null);
  return (
    <section aria-label={`${source.label}, official examination video`} style={{
      marginTop: 15, padding: '13px 14px 14px', border: '1px solid var(--mb-muted-border, #d4d4d4)',
      borderRadius: 12, background: 'var(--mb-raised)',
    }}>
      <span style={{
        display: 'block', fontSize: 9.5, fontWeight: 750, lineHeight: 1.4,
        letterSpacing: '.11em', textTransform: 'uppercase', color: 'var(--mb-label, #6b6b6b)',
      }}>{source.label} · official video</span>
      <strong style={{ display: 'block', marginTop: 2, fontSize: 13.5, lineHeight: 1.35,
        color: 'var(--mb-ink, #242424)' }}>{source.title}</strong>
      <video
        key={source.playbackUrl}
        aria-label={source.title}
        controls
        playsInline
        preload="metadata"
        src={source.playbackUrl}
        onError={() => setFailedUrl(source.playbackUrl)}
        onCanPlay={() => setFailedUrl(null)}
        style={{ display: 'block', width: '100%', maxHeight: 430, marginTop: 11, background: '#000' }}
      >Your browser does not support video playback.</video>
      <p style={{ margin: '8px 0 0', fontSize: 11.5, lineHeight: 1.45, color: 'var(--mb-muted, #6b6b6b)' }}>
        {source.presentationNote}
      </p>
      {failedUrl === source.playbackUrl && (
        <p role="status" style={{ margin: '8px 0 0', fontSize: 11.5, lineHeight: 1.45,
          color: 'var(--mb-muted, #6b6b6b)' }}>
          This video could not be played here. Open the official SEC video to use another player.
        </p>
      )}
      <p style={{ margin: '7px 0 0', fontSize: 10.5, lineHeight: 1.45, color: 'var(--mb-label, #6b6b6b)' }}>
        {source.attribution}{' '}
        <a href={source.canonicalUrl} target="_blank" rel="noreferrer" style={{ color: 'inherit', fontWeight: 700 }}>
          Open the official SEC video
        </a>
      </p>
    </section>
  );
};

export default VideoSourcePlayer;
