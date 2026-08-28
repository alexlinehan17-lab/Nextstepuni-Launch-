/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * One avatar image, with a fallback that always renders.
 *
 * Avatars come from api.dicebear.com — a third party, on a network the school
 * controls and we do not. When that request fails, a bare <img> renders an
 * empty box, and 21 of the 24 avatar <img> tags in the app had no onError at
 * all. On the registration avatar picker that meant eight empty boxes and no
 * way to tell which one you were choosing, which is a hard stop in signup
 * rather than a cosmetic problem.
 *
 * getAvatarFallback() already existed and was already used by
 * UserProfileMenu; it just was not used anywhere else. This component makes
 * the protected path the default one, so a blocked or slow CDN degrades to
 * initials on a coloured disc instead of nothing.
 *
 * Note the fallback is a data URI, so it needs no network and cannot itself
 * fail. If avatars are blank in production the real fix is upstream — find why
 * api.dicebear.com is unreachable from that network — but no student should be
 * blocked from signing up while that is investigated.
 */
import React, { useEffect, useState } from 'react';

import { getAvatarUrl, getAvatarFallback } from '../utils/authUtils';

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
