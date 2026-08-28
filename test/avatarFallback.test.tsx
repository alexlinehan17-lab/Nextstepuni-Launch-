/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Avatars come from a third-party CDN on a network the school controls. The
 * property that matters is not "does the remote image load" — we cannot make
 * that true — but "does something always render". Eight empty boxes on the
 * registration avatar picker is a hard stop in signup, not a cosmetic problem.
 */
import { describe, expect, it } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';

import Avatar from '@/components/Avatar';
import { getAvatarFallback, getAvatarUrl, AVATAR_SEEDS } from '@/utils/authUtils';

describe('Avatar', () => {
  it('uses the remote avatar while it is working', () => {
    render(<Avatar seed="Maya Angelou" alt="Maya Angelou" />);
    expect(screen.getByAltText('Maya Angelou')).toHaveAttribute('src', getAvatarUrl('Maya Angelou'));
  });

  it('falls back to a local image when the CDN fails', () => {
    render(<Avatar seed="Maya Angelou" alt="Maya Angelou" />);
    const img = screen.getByAltText('Maya Angelou');
    fireEvent.error(img);
    expect(img).toHaveAttribute('src', getAvatarFallback('Maya Angelou'));
  });

  it('falls back to something that needs no network, so it cannot fail in turn', () => {
    // A remote fallback would fail for exactly the same reason as the original.
    expect(getAvatarFallback('Maya Angelou')).toMatch(/^data:image\/svg\+xml,/);
  });

  it('keeps every picker seed distinguishable when they have all fallen back', () => {
    // The picker's whole job is letting a student tell the options apart, and
    // four of these begin with M — a single-initial fallback collapsed them.
    const rendered = AVATAR_SEEDS.map(getAvatarFallback);
    expect(new Set(rendered).size).toBe(AVATAR_SEEDS.length);
  });

  it('reads correctly for a real name, not just the seed list', () => {
    expect(decodeURIComponent(getAvatarFallback('Alex Linehan'))).toContain('>AL<');
    expect(decodeURIComponent(getAvatarFallback('Prince'))).toContain('>PR<');
    expect(decodeURIComponent(getAvatarFallback(''))).toContain('>?<');
  });

  it('retries the CDN when the seed changes', () => {
    // Otherwise one failure would poison every later avatar in the same slot.
    const { rerender } = render(<Avatar seed="Mary Baker" alt="a" />);
    fireEvent.error(screen.getByAltText('a'));
    expect(screen.getByAltText('a')).toHaveAttribute('src', getAvatarFallback('Mary Baker'));

    rerender(<Avatar seed="Ma Rainey" alt="a" />);
    expect(screen.getByAltText('a')).toHaveAttribute('src', getAvatarUrl('Ma Rainey'));
  });
});
