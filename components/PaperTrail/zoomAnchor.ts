/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail viewer — keep the reading position through a zoom. Zoom changes
 * the width of every page, and page heights follow the width, so an unchanged
 * scrollTop lands on a different page (page 14 became page 8 on zooming in).
 * Before the zoom, note the point at the middle of the reader as a page and a
 * fraction of that page; after it, scroll that same point back to the middle.
 */

export interface ZoomAnchor {
  /** Page under the vertical middle of the reader (1-based). */
  page: number;
  /** How far down that page the middle sits, 0 (top) to 1 (bottom). */
  down: number;
  /** Horizontal middle of the reader as a fraction of the content width. */
  across: number;
}

const clamp01 = (n: number) => Math.min(1, Math.max(0, n));

/** The page and point under the middle of `scroller`, whose page elements
 *  carry `data-page` and are positioned against it (offsetTop). The page
 *  choice matches the viewer's page counter. */
export function captureZoomAnchor(scroller: HTMLElement): ZoomAnchor | null {
  const pages = scroller.querySelectorAll<HTMLElement>('[data-page]');
  if (!pages.length) return null;
  const middle = scroller.scrollTop + scroller.clientHeight / 2;
  let hit = pages[0];
  for (const page of pages) {
    if (page.offsetTop <= middle) hit = page;
    else break;
  }
  const height = hit.offsetHeight;
  return {
    page: Number(hit.dataset.page),
    down: height > 0 ? clamp01((middle - hit.offsetTop) / height) : 0,
    across: scroller.scrollWidth > 0
      ? clamp01((scroller.scrollLeft + scroller.clientWidth / 2) / scroller.scrollWidth)
      : 0.5,
  };
}

/** Scroll `scroller` so the anchored point is back under its middle. */
export function restoreZoomAnchor(scroller: HTMLElement, anchor: ZoomAnchor): void {
  const page = scroller.querySelector<HTMLElement>(`[data-page="${anchor.page}"]`);
  if (!page) return;
  scroller.scrollTop = Math.max(0, page.offsetTop + anchor.down * page.offsetHeight - scroller.clientHeight / 2);
  scroller.scrollLeft = Math.max(0, anchor.across * scroller.scrollWidth - scroller.clientWidth / 2);
}
