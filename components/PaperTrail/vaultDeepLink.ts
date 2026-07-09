/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Topic Vault deep links — open the vault straight at a subject + topic from a
 * shared URL, and build such a URL to share.
 *
 * SAFE BY CONSTRUCTION: this only reads the boot-time URL snapshot
 * (utils/bootParams, captured before NavigationContext rewrites the URL) and
 * builds strings. It never touches window.history / popstate, so the worst case
 * is a link that simply doesn't restore (a missing feature) — never broken app
 * navigation. The subject-only case is left to Paper Trail's existing paper-list
 * deep link; this adds the `topic` dimension.
 */

import { getBootParam } from '../../utils/bootParams';
import { topicsForSubject } from './topics';

export interface VaultLocation {
  subjectId: string;
  subtopicId: string;
}

/** Validate a (subject, topic) pair against the committed tags. */
function validLocation(subjectId: string | null, topic: string | null): VaultLocation | null {
  if (!subjectId || !topic) return null;
  return topicsForSubject(subjectId).some(t => t.subtopicId === topic)
    ? { subjectId, subtopicId: topic }
    : null;
}

/** Is there a valid topic deep link to open the vault at? Non-consuming, so the
 *  host view can decide to mount the vault before the feed consumes the target. */
export function hasInitialVaultTopic(): boolean {
  return validLocation(getBootParam('subject'), getBootParam('topic')) !== null;
}

let consumed = false;

/** The subject + topic to open from a shared link — ONCE per page load. Returns
 *  null after the first read so normal in-app navigation to the vault isn't
 *  hijacked back to the deep-linked topic. */
export function consumeInitialVaultLocation(): VaultLocation | null {
  if (consumed) return null;
  consumed = true;
  return validLocation(getBootParam('subject'), getBootParam('topic'));
}

/** Reset the once-guard — test-only. */
export function __resetVaultDeepLinkForTest(): void {
  consumed = false;
}

/** A shareable absolute URL that reopens the vault at this topic. Mirrors the
 *  app's own nav params (view=innovation-zone, tool=paper-trail) so the tool
 *  mounts, then the topic/subject deep-link params it carries are read at boot. */
export function buildVaultLink(subjectId: string, subtopicId: string, origin?: string, pathname?: string): string {
  const p = new URLSearchParams();
  p.set('view', 'innovation-zone');
  p.set('tool', 'paper-trail');
  p.set('subject', subjectId);
  p.set('topic', subtopicId);
  const base = `${origin ?? window.location.origin}${pathname ?? window.location.pathname}`;
  return `${base}?${p.toString()}`;
}
