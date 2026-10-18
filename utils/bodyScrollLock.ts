/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * One shared, counted lock for page scrolling behind modals, drawers and
 * readers.
 *
 * useModal counted its own holders, but the Mark Bank source reader, the Ways
 * In workspace and the GC drawer each remembered the page's overflow on open
 * and put it back on close. When one of them opened while a modal was open,
 * it remembered "hidden" as the original; if the modal closed first, the page
 * stayed locked after everything closed and only a refresh freed it ("you
 * can't scroll down on a page", 18 Oct 2026).
 *
 * Counting every holder in one place fixes the class: the first holder
 * remembers the real value and the last one to let go restores it, in any
 * order. Releasing twice is harmless.
 */

let holders = 0;
let original = '';

/** Stop the page scrolling. Returns a release function; call it once, any time. */
export function lockBodyScroll(): () => void {
  if (typeof document === 'undefined') return () => {};
  if (holders === 0) original = document.body.style.overflow;
  holders += 1;
  document.body.style.overflow = 'hidden';
  let released = false;
  return () => {
    if (released) return;
    released = true;
    holders = Math.max(0, holders - 1);
    if (holders === 0) document.body.style.overflow = original;
  };
}

/** For tests: forget every holder. */
export function resetBodyScrollLock(): void {
  holders = 0;
  original = '';
}
