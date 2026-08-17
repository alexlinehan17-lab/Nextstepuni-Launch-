/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export const FEEDBACK_CATEGORIES = [
  'broken',
  'confusing',
  'idea',
  'other',
] as const;

export type FeedbackCategory = (typeof FEEDBACK_CATEGORIES)[number];

export const FEEDBACK_CATEGORY_LABELS: Record<FeedbackCategory, string> = {
  broken: 'Something is broken',
  confusing: 'Something is confusing',
  idea: 'Feature idea',
  other: 'Something else',
};

export const FEEDBACK_STATUSES = [
  'new',
  'reviewing',
  'planned',
  'fixed',
  'archived',
] as const;

export type FeedbackStatus = (typeof FEEDBACK_STATUSES)[number];

export const FEEDBACK_STATUS_LABELS: Record<FeedbackStatus, string> = {
  new: 'New',
  reviewing: 'Reviewing',
  planned: 'Planned',
  fixed: 'Fixed',
  archived: 'Archived',
};

export type FeedbackPlatform = 'web' | 'ios' | 'android';

export function getFeedbackPlatform(userAgent: string): FeedbackPlatform {
  if (/android/i.test(userAgent)) return 'android';
  if (/iPad|iPhone|iPod/i.test(userAgent)) return 'ios';
  return 'web';
}
