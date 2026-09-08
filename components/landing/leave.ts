/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * He walks out of the landing page into the app. "Open the app" is a real
 * navigation to the app document; with both documents opted into
 * cross-document view transitions (leave.css here, index.html there), the
 * browser morphs whichever starguy is on screen — the live traveller, or the
 * hero's static copy — into the small figure the app paints by its door.
 * Coming back, the app names its figure and this page names the hero's, so
 * he walks home again. Same origin only; anywhere the API is missing this
 * file does nothing and the link is just a link.
 */

import './leave.css';

const APP_PATHS = new Set(['/', '/index.html']);
const NAME = 'starguy';

type NavEvent = Event & { viewTransition?: { types?: Set<string>; finished: Promise<void> }; activation?: { entry?: { url: string } | null } | null };

const goesToApp = (e: NavEvent): boolean => {
  const url = e.activation?.entry?.url;
  if (!url) return false;
  try { const u = new URL(url, location.href); return u.origin === location.origin && APP_PATHS.has(u.pathname); } catch { return false; }
};

/** The starguy the reader can see: the traveller when live, else the hero's copy. */
const visibleStarguy = (): HTMLElement | null => {
  const live = document.querySelector<HTMLElement>('.landing-traveller');
  if (live) return live;
  const hero = document.querySelector<HTMLElement>('[data-starguy-slot="hero"]');
  return hero && hero.getBoundingClientRect().width > 0 ? hero : null;
};

let installed = false;
export const installLeave = (): void => {
  if (installed || typeof window === 'undefined') return;
  installed = true;
  window.addEventListener('pageswap', (e: NavEvent) => {
    if (!e.viewTransition || !goesToApp(e)) return;
    const el = visibleStarguy();
    if (el) el.style.viewTransitionName = NAME;
    e.viewTransition.types?.add('to-app');
  });
  window.addEventListener('pagereveal', (e: NavEvent) => {
    if (!e.viewTransition) return;
    // Home again: the hero's copy takes the name so he can land on it.
    const el = visibleStarguy();
    if (!el) return;
    el.style.viewTransitionName = NAME;
    e.viewTransition.finished.finally(() => { el.style.viewTransitionName = ''; });
  });
  // Have the app ready before the click, so the morph lands on a painted page.
  try {
    const s = document.createElement('script');
    s.type = 'speculationrules';
    s.textContent = JSON.stringify({ prerender: [{ urls: ['/?from=landing'], eagerness: 'moderate' }] });
    document.head.appendChild(s);
  } catch { /* optional */ }
};
