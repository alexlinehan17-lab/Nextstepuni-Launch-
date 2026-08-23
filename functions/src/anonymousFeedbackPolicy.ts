/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { createHash } from "crypto";

export const MAX_FEEDBACK_SUBMISSIONS_PER_DAY = 5;
export const FEEDBACK_RETENTION_DAYS = 365;

const CATEGORIES = new Set(["broken", "confusing", "idea", "other"]);
const PLATFORMS = new Set(["web", "ios", "android"]);

export interface FeedbackRequest {
  category?: unknown;
  message?: unknown;
  context?: unknown;
  platform?: unknown;
  appVersion?: unknown;
}

export interface SanitizedFeedback {
  category: string;
  message: string;
  context: Record<string, string> | null;
  platform: string;
  appVersion: string;
}

export type FeedbackValidationResult =
  | { ok: true; value: SanitizedFeedback }
  | { ok: false; reason: "category" | "message" | "platform" };

function boundedString(value: unknown, maxLength: number): string | null {
  if (typeof value !== "string") return null;
  const cleaned = Array.from(value).filter(character => {
    const code = character.charCodeAt(0);
    return code === 9 || code === 10 || code === 13 || (code >= 32 && code !== 127);
  }).join("").trim();
  if (!cleaned || cleaned.length > maxLength) return null;
  return cleaned;
}

function sanitizeContext(value: unknown): Record<string, string> | null {
  if (!value || typeof value !== "object" || Array.isArray(value)) return null;
  const input = value as Record<string, unknown>;
  const surface = boundedString(input.surface, 80);
  if (!surface) return null;

  const context: Record<string, string> = { surface };
  const moduleId = boundedString(input.moduleId, 120);
  const moduleTitle = boundedString(input.moduleTitle, 160);
  if (moduleId) context.moduleId = moduleId;
  if (moduleTitle) context.moduleTitle = moduleTitle;
  return context;
}

export function validateFeedbackRequest(data: FeedbackRequest): FeedbackValidationResult {
  const category = boundedString(data.category, 20);
  const message = boundedString(data.message, 2000);
  const platform = boundedString(data.platform, 20);
  const appVersion = boundedString(data.appVersion, 40) || "unknown";

  if (!category || !CATEGORIES.has(category)) return { ok: false, reason: "category" };
  if (!message || message.length < 10) return { ok: false, reason: "message" };
  if (!platform || !PLATFORMS.has(platform)) return { ok: false, reason: "platform" };

  return {
    ok: true,
    value: {
      category,
      message,
      context: data.context === null ? null : sanitizeContext(data.context),
      platform,
      appVersion,
    },
  };
}

/**
 * A rotating pseudonymous account marker used only in the server-only rate
 * limit collection. It changes daily and is never copied to feedback records.
 */
export function feedbackRateLimitId(uid: string, utcDay: string): string {
  return createHash("sha256")
    .update(`nextstepuni-feedback-rate-v1:${utcDay}:${uid}`)
    .digest("hex");
}

export function feedbackLimitReached(currentCount: number): boolean {
  return currentCount >= MAX_FEEDBACK_SUBMISSIONS_PER_DAY;
}

export function isEligibleFeedbackUser(userData: Record<string, unknown> | undefined): boolean {
  if (!userData) return false;
  const role = userData.role;
  return typeof userData.school === "string"
    && userData.school.trim().length > 0
    && userData.accountDisabled !== true
    && userData.isAdmin !== true
    && role !== "admin"
    && role !== "gc"
    && role !== "staff";
}
