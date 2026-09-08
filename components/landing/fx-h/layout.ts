/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The chapter scenes: which drawing each chapter stands on, and where the
 * chapters are on the page. The drawings are 1440 × 900 tiles that repeat
 * vertically (scripts/landing/scenes-svg.mjs writes them to
 * public/assets/landing/scenes/); the layout is read from the DOM —
 * article#chapter-<id> inside section#chapters — so a chapter added to
 * copy.ts gets its scene without this file changing.
 */

export const SCENE_IDS = ['markbank', 'papertrail', 'atlas', 'planner', 'launchpad', 'lab', 'futurefinder'] as const;
export type SceneId = (typeof SCENE_IDS)[number];

/** The drawn tile's size in CSS px at design scale. */
export const TILE = { w: 1440, h: 900 } as const;

export const sceneUrl = (i: number): string => `/assets/landing/scenes/${SCENE_IDS[i]}.svg`;

/** A chapter's scene: its own where one is drawn, else by its place in the order. */
export const sceneIndexFor = (chapterId: string, position: number): number => {
  const i = (SCENE_IDS as readonly string[]).indexOf(chapterId);
  return i >= 0 ? i : position % SCENE_IDS.length;
};

export interface Band {
  id: string;
  /** Index into SCENE_IDS. */
  scene: number;
  /** Page px. */
  top: number;
  bottom: number;
}

export interface Layout {
  /** The window height the layout was measured against: the bleed spans and the track's reach depend on it. */
  viewportH: number;
  /** Page px of the top of main, which the track is positioned against. */
  mainTop: number;
  sectionTop: number;
  sectionBottom: number;
  bands: Band[];
  /**
   * Page px. boundaries[k] separates scene k−1 from scene k: [0] is the
   * entry (white → I), the last is the exit (last → white), the rest sit on
   * the rule between two chapters.
   */
  boundaries: number[];
}

/** Read the chapters off the page. Null until the section exists. */
export function measureLayout(viewportH: number): Layout | null {
  const main = document.querySelector<HTMLElement>('.landing-page > main');
  const section = document.getElementById('chapters');
  if (!main || !section) return null;
  const articles = Array.from(section.querySelectorAll<HTMLElement>('article[id^="chapter-"]'));
  if (articles.length === 0) return null;
  const sy = window.scrollY;
  const mr = main.getBoundingClientRect();
  const sr = section.getBoundingClientRect();
  const bands: Band[] = articles.map((a, i) => {
    const r = a.getBoundingClientRect();
    const id = a.id.slice('chapter-'.length);
    return { id, scene: sceneIndexFor(id, i), top: r.top + sy, bottom: r.bottom + sy };
  });
  const boundaries = [bands[0].top - viewportH * 0.1];
  for (let i = 1; i < bands.length; i++) boundaries.push((bands[i - 1].bottom + bands[i].top) / 2);
  boundaries.push(bands[bands.length - 1].bottom + viewportH * 0.1);
  return { viewportH, mainTop: mr.top + sy, sectionTop: sr.top + sy, sectionBottom: sr.bottom + sy, bands, boundaries };
}

export const sameLayout = (a: Layout | null, b: Layout | null): boolean => {
  if (!a || !b) return a === b;
  if (a.viewportH !== b.viewportH || a.mainTop !== b.mainTop || a.sectionTop !== b.sectionTop || a.sectionBottom !== b.sectionBottom) return false;
  if (a.bands.length !== b.bands.length) return false;
  return a.bands.every((x, i) => { const y = b.bands[i]; return x.id === y.id && x.top === y.top && x.bottom === y.bottom; });
};

/**
 * Half the scroll distance a bleed takes: a third of the viewport, or less
 * where two boundaries sit close, so no two bleeds ever overlap.
 */
export function bleedSpan(layout: Layout, viewportH: number): number {
  let gap = Infinity;
  for (let i = 1; i < layout.boundaries.length; i++) gap = Math.min(gap, layout.boundaries[i] - layout.boundaries[i - 1]);
  return Math.max(40, Math.min(viewportH * 0.3, gap * 0.45));
}

/** What the canvas shows: scene `a` with scene `b` soaked `p` of the way in (−1 is blank paper). */
export interface Mix {
  a: number;
  b: number;
  p: number;
  /** Which boundary is bleeding, so each has its own fibre. */
  seed: number;
}

/** The mix for a reader whose viewport centre is at page px `centre`. */
export function mixAt(layout: Layout, centre: number, span: number): Mix {
  const B = layout.boundaries;
  const n = layout.bands.length;
  const scene = (i: number): number => (i < 0 || i >= n ? -1 : layout.bands[i].scene);
  let k = 0;
  while (k < B.length && B[k] <= centre) k++;
  // k boundaries are behind the reader: scene k−1 is current (blank before the first, blank after the last).
  const cur = k - 1;
  if (k > 0 && centre - B[k - 1] < span) {
    return { a: scene(cur - 1), b: scene(cur), p: (centre - (B[k - 1] - span)) / (2 * span), seed: k - 1 };
  }
  if (k < B.length && B[k] - centre < span) {
    return { a: scene(cur), b: scene(cur + 1), p: (centre - (B[k] - span)) / (2 * span), seed: k };
  }
  return { a: scene(cur), b: scene(cur), p: 0, seed: k };
}
