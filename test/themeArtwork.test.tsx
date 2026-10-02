import React from 'react';
import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import ThemeArtwork from '../components/ThemeArtwork';
import { DARK_ARTWORK } from '../data/darkArtwork';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';

const source = '/assets/star-crew/subjects/applied-mathematics.png';
const darkSource = '/assets/dark/star-crew/subjects/applied-mathematics.png';
afterEach(() => { cleanup(); document.documentElement.className = ''; });

describe('filled artwork across appearance changes', () => {
  it('packages every paired asset with alpha, original dimensions and unmodified source files', () => {
    const manifest = JSON.parse(readFileSync('public/assets/dark/artwork-manifest.json', 'utf8'));
    expect(manifest).toHaveLength(Object.keys(DARK_ARTWORK).length);
    for (const entry of manifest) {
      const original = readFileSync('public' + entry.source);
      const paired = readFileSync('public' + entry.dark);
      expect(DARK_ARTWORK[entry.source]).toBe(entry.dark);
      expect(paired.subarray(1,4).toString()).toBe('PNG');
      expect(paired[25]).toBe(6); // PNG RGBA colour type, rather than a painted checkerboard.
      expect(paired.readUInt32BE(16)).toBe(original.readUInt32BE(16));
      expect(paired.readUInt32BE(20)).toBe(original.readUInt32BE(20));
      expect(createHash('sha256').update(original).digest('hex')).toBe(entry.sourceSha256);
    }
  });
  it('switches both ways without remounting or changing the accessible name', async () => {
    render(<ThemeArtwork src={source} alt="Applied Maths" />);
    const image = screen.getByRole('img', { name: 'Applied Maths' });
    expect(image).toHaveAttribute('src', source);
    await act(async () => { document.documentElement.classList.add('dark'); });
    expect(image).toHaveAttribute('src', darkSource);
    await act(async () => { document.documentElement.classList.remove('dark'); });
    expect(image).toHaveAttribute('src', source);
  });

  it('keeps explicitly light entry screens original despite a saved dark preference', () => {
    document.documentElement.classList.add('dark');
    render(<div className="account-entry"><ThemeArtwork src={source} alt="Applied Maths" /></div>);
    expect(screen.getByRole('img')).toHaveAttribute('src', source);
  });

  it('uses the filled pair on a dark banner independently of global appearance', () => {
    render(<ThemeArtwork src={source} alt="Applied Maths" darkSurface />);
    expect(screen.getByRole('img')).toHaveAttribute('src', darkSource);
  });

  it('recovers from a missing dark asset, retaining the existing original-image fallback', async () => {
    const onError = vi.fn();
    document.documentElement.classList.add('dark');
    const view = render(<ThemeArtwork src={source} alt="Applied Maths" onError={onError} />);
    fireEvent.error(screen.getByRole('img'));
    expect(screen.getByRole('img')).toHaveAttribute('src', source);
    expect(onError).not.toHaveBeenCalled();
    fireEvent.error(screen.getByRole('img'));
    expect(onError).toHaveBeenCalledOnce();
    view.rerender(<ThemeArtwork src="/assets/star-crew/subjects/art.png" alt="Art" onError={onError} />);
    await waitFor(() => expect(screen.getByRole('img')).toHaveAttribute('src', '/assets/dark/star-crew/subjects/art.png'));
  });

  it('does not substitute unrelated artwork for already transparent or unknown sources', () => {
    document.documentElement.classList.add('dark');
    render(<ThemeArtwork src="/assets/tools/paper-trail.png" alt="Paper Trail" />);
    expect(screen.getByRole('img')).toHaveAttribute('src', '/assets/tools/paper-trail.png');
  });
});
