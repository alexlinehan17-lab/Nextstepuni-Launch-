/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Transient navigation intents for the module screens (area 5 of the design
 * build), kept in a file with no imports so the app shell can set them without
 * pulling module data into its first chunk. Progress stays the authority for
 * what is read; these only say how a screen was reached.
 */

// "Pick up where you left off": a module opened by a continue action goes straight to the
// student's step; any other way in opens on its title page first (a phone, board c-read-flow).
const resumeRequests = new Set<string>();
export function requestModuleResume(moduleId: string) { resumeRequests.add(moduleId); }
export function requestedModuleResume(moduleId: string | null | undefined) { return moduleId ? resumeRequests.has(moduleId) : false; }
export function clearModuleResumeRequest(moduleId: string) { resumeRequests.delete(moduleId); }

// Back from a world to Modules closes the world into its door (board c-modules-pick, move 5):
// the world's Back says which door, and Modules plays the move if it mounts straight after.
let worldReturn: { id: string; at: number } | null = null;
export function markWorldReturn(id: string) { worldReturn = { id, at: Date.now() }; }
export function takeWorldReturn(): string | null {
  const value = worldReturn && Date.now() - worldReturn.at < 2000 ? worldReturn.id : null;
  worldReturn = null;
  return value;
}
