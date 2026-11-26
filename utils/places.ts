/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The five places and what every screen is (navigation.md, "Three kinds of
 * screen"). One answer for the tab bar, the laptop sidebar and the top bar:
 *
 *   placeOf(screen)      which of the five places a screen belongs to: the tab
 *                        the phone's tab bar marks while it is showing
 *   isPlace(screen)      the screen IS one of the five: it shows no leave control
 *   parentOf(screen)     where Back goes when there is no history to go back
 *                        through (a reload, a deep link, a shared URL)
 *
 * A screen is the app's navigation state (contexts/NavigationContext.tsx):
 * there is no router, one ViewState plus the module, category and tool.
 */

export type PlaceId = 'tree' | 'dashboard' | 'study-session' | 'my-journey' | 'innovation-zone';

/** Always the same five, in the same order, with the same names on every device. */
export const PLACE_IDS: readonly PlaceId[] = ['tree', 'dashboard', 'study-session', 'my-journey', 'innovation-zone'];

export interface ScreenRef {
  viewState: string;
  activeTool?: string | null;
  currentCategory?: string | null;
  currentModuleId?: string | null;
  cameFromJourney?: boolean;
}

/** Pages a student reaches from Home (its content, or the account sheet opened
 *  on Home): the tab bar keeps Home marked while they are open. */
const HOME_PAGES = new Set([
  'tree', 'modules', 'category', 'module', 'learning-paths', 'year-plans', 'your-setup',
  'accreditation', 'settings', 'my-direction', 'cut-content', 'wip-tools', 'jc-coming-soon',
]);

export function placeOf(screen: ScreenRef): PlaceId | null {
  const { viewState } = screen;
  if (viewState === 'dashboard' || viewState === 'insights') return 'dashboard';
  if (viewState === 'study-session') return 'study-session';
  if (viewState === 'my-journey') return 'my-journey';
  if (viewState === 'innovation-zone') return 'innovation-zone';
  if (HOME_PAGES.has(viewState)) return 'tree';
  return null;
}

/** One of the five places itself: no Back, no Close. The Launchpad is a place;
 *  a tool opened from it is a page. */
export function isPlace(screen: ScreenRef): boolean {
  const { viewState } = screen;
  if (viewState === 'innovation-zone') return !screen.activeTool;
  return viewState === 'tree' || viewState === 'dashboard' || viewState === 'study-session' || viewState === 'my-journey';
}

/** The screen a page sits under, for Back when there is no history. A place
 *  has no parent. */
export function parentOf(screen: ScreenRef): ScreenRef | null {
  if (isPlace(screen)) return null;
  switch (screen.viewState) {
    case 'innovation-zone':
      return { viewState: 'innovation-zone', activeTool: null };
    case 'module':
      if (screen.cameFromJourney) return { viewState: 'innovation-zone', activeTool: 'journey' };
      return screen.currentCategory ? { viewState: 'category', currentCategory: screen.currentCategory } : { viewState: 'modules' };
    case 'category':
    case 'jc-coming-soon':
      return { viewState: 'modules' };
    case 'insights':
      return { viewState: 'dashboard' };
    default:
      return { viewState: 'tree' };
  }
}

/** The laptop sidebar, "sidebar B" (agreed 25 Nov 2026): the five places,
 *  then Workspace. Ten rows; everything else lives under the student's name,
 *  on Home or in the Launchpad. */
export type SidebarItemId =
  | 'home' | 'modules' | 'study' | 'progress' | 'island'
  | 'launchpad' | 'mark-bank' | 'planner' | 'topic-atlas' | 'paper-trail';

export const SIDEBAR_PLACES: readonly SidebarItemId[] = ['home', 'modules', 'study', 'progress', 'island'];
export const SIDEBAR_WORKSPACE: readonly SidebarItemId[] = ['launchpad', 'mark-bank', 'planner', 'topic-atlas', 'paper-trail'];

/** The four Workspace tools with their own row; every other tool is the Launchpad's. */
const WORKSPACE_TOOLS = new Set(['mark-bank', 'planner', 'topic-atlas', 'paper-trail']);

/** The sidebar row shaded for a screen, or none (a page opened from the menu
 *  under the student's name, such as Settings or Year Plans, shades no row). */
export function sidebarItemFor(screen: ScreenRef): SidebarItemId | null {
  switch (screen.viewState) {
    case 'tree': return 'home';
    case 'modules': case 'category': case 'module': return 'modules';
    case 'study-session': return 'study';
    case 'dashboard': case 'insights': return 'progress';
    case 'my-journey': return 'island';
    case 'innovation-zone':
      return screen.activeTool && WORKSPACE_TOOLS.has(screen.activeTool) ? screen.activeTool as SidebarItemId : 'launchpad';
    default: return null;
  }
}
