/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The page must scroll again once every modal, reader and drawer has closed,
 * whatever order they open and close in.
 */
import React from 'react';
import { afterEach, describe, expect, test } from 'vitest';
import { render } from '@testing-library/react';
import { lockBodyScroll, resetBodyScrollLock } from '../utils/bodyScrollLock';
import { useModal } from '../hooks/useModal';

afterEach(() => { resetBodyScrollLock(); document.body.style.overflow = ''; });

function Modal({ open }: { open: boolean }) {
  useModal(open, () => {});
  return open ? <div role="dialog" aria-modal="true" /> : null;
}

describe('body scroll lock', () => {
  test('overlapping holders release in any order and the page scrolls again', () => {
    const first = lockBodyScroll();
    const second = lockBodyScroll();
    expect(document.body.style.overflow).toBe('hidden');
    first();
    expect(document.body.style.overflow).toBe('hidden');
    second();
    expect(document.body.style.overflow).toBe('');
  });

  test('a reader opened inside a modal cannot strand the lock when the modal closes first', () => {
    const modal = render(<Modal open />);
    const releaseReader = lockBodyScroll();
    modal.rerender(<Modal open={false} />);
    expect(document.body.style.overflow).toBe('hidden');
    releaseReader();
    expect(document.body.style.overflow).toBe('');
  });

  test('releasing twice does not unlock someone else', () => {
    const a = lockBodyScroll();
    const b = lockBodyScroll();
    a(); a();
    expect(document.body.style.overflow).toBe('hidden');
    b();
    expect(document.body.style.overflow).toBe('');
  });

  test('restores a page that was already set to something else', () => {
    document.body.style.overflow = 'scroll';
    const release = lockBodyScroll();
    release();
    expect(document.body.style.overflow).toBe('scroll');
  });
});
