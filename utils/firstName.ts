/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * Reduce a full name to its first token (given name only).
 *
 * Used at every point where a student's name is exposed to their PEERS (the
 * island projection, kudos/gifts sender labels) so classmates never see each
 * other's full names — a data-minimisation measure for a minors' platform
 * (security review 2026-07-18). Staff-facing views keep the full name.
 */
export function firstName(full: string | undefined | null): string {
  if (!full) return '';
  const trimmed = full.trim();
  if (!trimmed) return '';
  return trimmed.split(/\s+/)[0];
}
