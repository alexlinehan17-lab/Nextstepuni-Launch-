/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The page must scroll again once every modal, reader and drawer has closed,
 * whatever order they open and close in, and whatever else writes overflow.
 */
import React from 'react';
import { afterEach, describe, expect, test } from 'vitest';
import { render } from '@testing-library/react';
import { SCROLL_LOCK_ATTRIBUTE, lockBodyScroll, resetBodyScrollLock } from '../utils/bodyScrollLock';
import { useModal } from '../hooks/useModal';

const locked = () => document.body.hasAttribute(SCROLL_LOCK_ATTRIBUTE);
afterEach(() => { resetBodyScrollLock(); document.body.style.overflow = ''; });

function Modal({ open }: { open: boolean }) {
  useModal(open, () => {});
  return open ? <div role="dialog" aria-modal="true" /> : null;
}

describe('body scroll lock', () => {
  test('overlapping holders release in any order and the page scrolls again', () => {
    const first = lockBodyScroll();
    const second = lockBodyScroll();
    expect(locked()).toBe(true);
    first();
    expect(locked()).toBe(true);
    second();
    expect(locked()).toBe(false);
  });

  test('a reader opened inside a modal cannot strand the lock when the modal closes first', () => {
    const modal = render(<Modal open />);
    const releaseReader = lockBodyScroll();
    modal.rerender(<Modal open={false} />);
    expect(locked()).toBe(true);
    releaseReader();
    expect(locked()).toBe(false);
  });

  test('another dialog writing overflow in between cannot strand the lock', () => {
    // The Kobra dialog sets and restores body overflow itself. Plan settings
    // closes one and opens a modal in the same instant.
    document.body.style.overflow = 'hidden';
    const modal = render(<Modal open />);
    document.body.style.overflow = '';
    modal.rerender(<Modal open={false} />);
    expect(locked()).toBe(false);
    expect(document.body.style.overflow).toBe('');
  });

  test('releasing twice does not unlock someone else', () => {
    const a = lockBodyScroll();
    const b = lockBodyScroll();
    a(); a();
    expect(locked()).toBe(true);
    b();
    expect(locked()).toBe(false);
  });
});
