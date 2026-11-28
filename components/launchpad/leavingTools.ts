/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Four tools are leaving the app for now (Alex, 24 and 25 November 2026: "We are going to remove the
 * catch up lane and I think war room is redundant with my progress"; Your Possible Life: "we are
 * removing this from the app for now"; "let's archive academic journey simulator for now").
 * "Remove their doors, keep their code and data." So every door in the interface asks this list:
 * the Launchpad's list and its categories, Meet the tools and Help me choose, the command palette,
 * Home's "Pick up where you left off", a module's tool card, Future Finder's "Explore career paths".
 * Each tool's own address still opens it (`?view=innovation-zone&tool=war-room` and the like), its
 * code and tests are untouched, and nothing a student saved in it is touched. To bring a tool back,
 * take its id out of this list.
 */
export const LEAVING_TOOL_IDS: ReadonlySet<string> = new Set([
  'catch-up-lane',
  'war-room',
  // War Room's Subject Coverage under its old name.
  'syllabus-xray',
  'your-possible-life',
  // Your Possible Life's old name (it redirects there).
  'career-paths',
  // The Academic Journey Simulator.
  'journey',
]);

/** True for a tool whose doors are gone (it still opens from its own address). */
export function isLeavingTool(toolId: string | null | undefined): boolean {
  return Boolean(toolId && LEAVING_TOOL_IDS.has(toolId));
}
