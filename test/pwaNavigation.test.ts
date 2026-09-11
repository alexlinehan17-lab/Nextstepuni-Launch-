import { describe, expect, it } from 'vitest';
import { NavigationRoute } from 'workbox-routing/NavigationRoute.js';
import { standaloneDocumentRoutes } from '../utils/pwaNavigation';

// Use the real Workbox matcher: it tests pathname + search, rather than just
// pathname. Ignoring search in a hand-written matcher hid the iframe outage.
const fallback = new NavigationRoute(async () => new Response('App shell'), {
  denylist: standaloneDocumentRoutes,
});
const usesAppShell = (path: string, origin = 'https://nextstepuni.com') => {
  const url = new URL(path, origin);
  const request = new Request(url);
  Object.defineProperty(request, 'mode', { value: 'navigate' });
  return fallback.match({ url, request, sameOrigin: true, event: {} as never });
};

describe('Standalone documents under an installed app worker', () => {
  it.each(['innovation-zone', 'module', 'papertrail'])('never puts the app shell in the %s chapter window', view => {
    for (const origin of ['https://nextstepuni.com', 'https://nextstepuni-app.web.app']) {
      expect(usesAppShell(`/landing-demo.html?view=${view}`, origin)).toBe(false);
      expect(usesAppShell(`/landing-demo.html?view=${view}&ref=chapter`, origin)).toBe(false);
    }
  });
  it.each(['/landing', '/landing-dev.html', '/landing-demo.html', '/certle', '/certle/', '/certle.html', '/privacy', '/privacy.html', '/terms', '/terms.html'])('preserves %s with and without query parameters', path => {
    expect(usesAppShell(path)).toBe(false);
    expect(usesAppShell(`${path}?from=landing`)).toBe(false);
  });
  it.each(['/', '/?view=innovation-zone', '/?from=landing', '/landing-tools', '/certle-results'])('retains the app navigation fallback for %s', path => {
    expect(usesAppShell(path)).toBe(true);
  });
});
