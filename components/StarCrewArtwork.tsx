import React, { useState } from 'react';
import type { StarCrewArtwork as Artwork } from '../data/starCrewTypes';
import './star-crew.css';

interface Props {
  artwork: Artwork;
  alt?: string;
  className?: string;
  style?: React.CSSProperties;
  loading?: 'eager' | 'lazy';
  fallback: React.ReactNode;
}

/** Preserve the original illustration while centring its ink inside the circle. */
export default function StarCrewArtwork({ artwork, alt = '', className = '', style, fallback, loading = 'lazy' }: Props) {
  const [failedSource, setFailedSource] = useState<string>();
  const { frame } = artwork;
  const tiled = frame.tile !== undefined;
  return <span className={`star-crew-avatar ${className}`} style={style} role={alt ? 'img' : undefined} aria-label={alt || undefined} aria-hidden={alt ? undefined : true}>
    {failedSource === artwork.src ? fallback : <span className="star-crew-frame" style={{ width: `${frame.width}%`, height: `${frame.width}%`, left: `${frame.left}%`, top: `${frame.top}%` }}>
      <img src={artwork.src} alt="" loading={loading} decoding="async" draggable={false}
        style={{ width: tiled ? '200%' : '100%', height: tiled ? '200%' : '100%', left: tiled && frame.tile! % 2 ? '-100%' : 0, top: tiled && frame.tile! > 1 ? '-100%' : 0 }}
        onError={() => setFailedSource(artwork.src)} />
    </span>}
  </span>;
}
