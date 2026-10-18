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
 * It also clashed with the Kobra dialog, which writes body overflow itself:
 * Plan settings > "Edit subjects and grades" closes one and opens the other in
 * the same instant, each restoring a value the other had changed, and the page
 * froze after the subjects editor closed.
 *
 * So the lock no longer saves or restores a value. Holders are counted and the
 * page carries a marker, `data-scroll-lock`, that index.css turns into
 * `overflow: hidden`. The marker is there while anyone holds the lock and gone
 * when the last holder lets go, in any order, whatever else touches overflow.
 * Releasing twice is harmless.
 */

let holders = 0;

export const SCROLL_LOCK_ATTRIBUTE = 'data-scroll-lock';

/** Stop the page scrolling. Returns a release function; call it once, any time. */
export function lockBodyScroll(): () => void {
  if (typeof document === 'undefined') return () => {};
  holders += 1;
  document.body.setAttribute(SCROLL_LOCK_ATTRIBUTE, '');
  let released = false;
  return () => {
    if (released) return;
    released = true;
    holders = Math.max(0, holders - 1);
    if (holders === 0) document.body.removeAttribute(SCROLL_LOCK_ATTRIBUTE);
  };
}

/** For tests: forget every holder. */
export function resetBodyScrollLock(): void {
  holders = 0;
  if (typeof document !== 'undefined') document.body.removeAttribute(SCROLL_LOCK_ATTRIBUTE);
}
