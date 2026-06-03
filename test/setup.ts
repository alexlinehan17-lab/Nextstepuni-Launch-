/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Vitest setup — jest-dom matchers + a global Firebase stub so importing any
 * component never spins up real Auth/Firestore (IndexedDB/network) in jsdom,
 * plus the jsdom globals Framer Motion / scroll components expect.
 */
import '@testing-library/jest-dom/vitest';
import { vi } from 'vitest';

// Stub the firebase.ts singletons so initializeApp/initializeAuth/Firestore
// never run under test.
vi.mock('@/firebase', () => ({
  auth: { currentUser: null, authStateReady: () => Promise.resolve() },
  db: {},
  default: {},
}));

// jsdom lacks matchMedia / IntersectionObserver / ResizeObserver, which Framer
// Motion and some scroll components touch on mount.
if (typeof window !== 'undefined' && !window.matchMedia) {
  window.matchMedia = ((query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addEventListener: () => {},
    removeEventListener: () => {},
    addListener: () => {},
    removeListener: () => {},
    dispatchEvent: () => false,
  })) as unknown as typeof window.matchMedia;
}

class MockObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
  takeRecords() { return []; }
}
const g = globalThis as Record<string, unknown>;
g.IntersectionObserver ||= MockObserver;
g.ResizeObserver ||= MockObserver;
