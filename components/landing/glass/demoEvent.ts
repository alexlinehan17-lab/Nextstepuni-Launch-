/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "Try it in the playground": any part of the page can ask the playground to
 * open a product (and a mode) and scroll to it.
 */

import type { PlaygroundTabId } from '../copy';

export const DEMO_EVENT = 'landing:demo';
export interface DemoEventDetail { demo: PlaygroundTabId; mode?: string }

export const openDemo = (demo: PlaygroundTabId, mode?: string): void => {
  window.dispatchEvent(new CustomEvent<DemoEventDetail>(DEMO_EVENT, { detail: { demo, mode } }));
};
