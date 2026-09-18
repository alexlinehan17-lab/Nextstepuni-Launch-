/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
/** A profile avatar with local Star Crew artwork and legacy CDN fallback. */
import React, { useEffect, useState } from 'react';

import { getAvatarUrl, getAvatarFallback } from '../utils/authUtils';
import { getPersonalStarCrew } from '../data/personalStarCrew';
import StarCrewArtwork from './StarCrewArtwork';

interface AvatarProps {
  /** Avatar seed, e.g. a SessionUser's `avatar` field. */
  seed: string;
  alt?: string;
  className?: string;
  style?: React.CSSProperties;
}

const Avatar: React.FC<AvatarProps> = ({ seed, alt = '', className = '', style }) => {
  const [failed, setFailed] = useState(false);

  // A changed seed is a different person/choice, so give the remote URL another
  // go rather than inheriting the previous seed's failure.
  useEffect(() => { setFailed(false); }, [seed]);

  const artwork = getPersonalStarCrew(seed);
  // Profile and picker portraits must be ready as the account sheet opens;
  // lazy loading can leave an absolutely positioned portrait blank until tapped.
  if (artwork) return <StarCrewArtwork key={seed} artwork={artwork} alt={alt} className={className} style={style} loading="eager" fallback={<img className="star-crew-fallback" src={getAvatarFallback(seed)} alt="" />} />;

  return (
    <img
      src={failed ? getAvatarFallback(seed) : getAvatarUrl(seed)}
      alt={alt}
      className={className}
      style={style}
      onError={() => setFailed(true)}
    />
  );
};

export default Avatar;
