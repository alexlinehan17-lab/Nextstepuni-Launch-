/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Pure validation and date helpers for first-party programme measurement.
 * Kept free of Firebase imports so the event contract can be tested without
 * loading the Functions runtime.
 */

export const PROGRAMME_EVENT_NAMES = [
  "account_registered",
  "session_started",
  "feature_exposed",
  "feature_started",
  "feature_completed",
  "module_started",
  "module_completed",
  "plan_activity_completed",
  "study_session_started",
  "study_session_completed",
  "practice_attempt_completed",
] as const;

export type ProgrammeEventName = (typeof PROGRAMME_EVENT_NAMES)[number];
export type ProgrammePlatform = "web" | "ios" | "android";
export type SessionType = "new-learning" | "practice" | "revision";
export type DurationBucket = "under_5m" | "5_14m" | "15_29m" | "30_59m" | "60m_plus";
export const PROGRAMME_SMALL_CELL_MINIMUM = 5;

export interface ProgrammeEventInput {
  clientEventId: string;
  name: ProgrammeEventName;
  sessionId: string;
  platform: ProgrammePlatform;
  appVersion: string;
  featureId?: string;
  moduleId?: string;
  source?: "app" | "launchpad" | "module" | "study" | "timetable" | "registration" | "practice";
  subjectId?: string;
  topicId?: string;
  accuracyBand?: "none" | "partial" | "strong" | "full";
  durationBucket?: DurationBucket;
  confidenceScore?: number;
  sessionType?: SessionType;
}

export interface ProgrammeEventBatch {
  events: ProgrammeEventInput[];
}

const EVENT_KEYS = new Set([
  "clientEventId",
  "name",
  "sessionId",
  "platform",
  "appVersion",
  "featureId",
  "moduleId",
  "source",
  "subjectId",
  "topicId",
  "accuracyBand",
  "durationBucket",
  "confidenceScore",
  "sessionType",
]);
const BASE_EVENT_KEYS = new Set(["clientEventId", "name", "sessionId", "platform", "appVersion"]);
const EVENT_DETAILS: Record<ProgrammeEventName, { allowed: Set<string>; required: Set<string>; source: string }> = {
  account_registered: { allowed: new Set(["source"]), required: new Set(), source: "registration" },
  session_started: { allowed: new Set(["source"]), required: new Set(), source: "app" },
  feature_exposed: { allowed: new Set(["featureId", "source"]), required: new Set(["featureId"]), source: "launchpad" },
  feature_started: { allowed: new Set(["featureId", "source"]), required: new Set(["featureId"]), source: "launchpad" },
  feature_completed: { allowed: new Set(["featureId", "source"]), required: new Set(["featureId"]), source: "launchpad" },
  module_started: { allowed: new Set(["moduleId", "source"]), required: new Set(["moduleId"]), source: "module" },
  module_completed: { allowed: new Set(["moduleId", "source"]), required: new Set(["moduleId"]), source: "module" },
  plan_activity_completed: { allowed: new Set(["source"]), required: new Set(), source: "timetable" },
  study_session_started: { allowed: new Set(["source", "sessionType"]), required: new Set(["sessionType"]), source: "study" },
  study_session_completed: {
    allowed: new Set(["source", "sessionType", "durationBucket", "confidenceScore"]),
    required: new Set(["sessionType", "durationBucket"]),
    source: "study",
  },
  practice_attempt_completed: {
    allowed: new Set(["source", "subjectId", "topicId", "accuracyBand"]),
    required: new Set(["subjectId", "topicId", "accuracyBand"]),
    source: "practice",
  },
};
const ID_RE = /^[a-z0-9][a-z0-9-]{0,63}$/;
const CLIENT_EVENT_ID_RE = /^[A-Za-z0-9-]{16,64}$/;
const SESSION_ID_RE = /^[A-Za-z0-9-]{8,64}$/;
const APP_VERSION_RE = /^[A-Za-z0-9._+-]{1,32}$/;
const SOURCES = new Set(["app", "launchpad", "module", "study", "timetable", "registration", "practice"]);
const ACCURACY_BANDS = new Set(["none", "partial", "strong", "full"]);
const PLATFORMS = new Set<ProgrammePlatform>(["web", "ios", "android"]);
const DURATION_BUCKETS = new Set<DurationBucket>(["under_5m", "5_14m", "15_29m", "30_59m", "60m_plus"]);
const SESSION_TYPES = new Set<SessionType>(["new-learning", "practice", "revision"]);

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function validOptionalId(value: unknown): value is string | undefined {
  return value === undefined || (typeof value === "string" && ID_RE.test(value));
}

export function validateProgrammeEventBatch(input: unknown):
  | { ok: true; value: ProgrammeEventBatch }
  | { ok: false; reason: string } {
  if (!isRecord(input) || !Array.isArray(input.events)) return { ok: false, reason: "events" };
  if (input.events.length < 1 || input.events.length > 25) return { ok: false, reason: "batch-size" };

  const validated: ProgrammeEventInput[] = [];
  for (const candidate of input.events) {
    if (!isRecord(candidate)) return { ok: false, reason: "event" };
    if (Object.keys(candidate).some(key => !EVENT_KEYS.has(key))) return { ok: false, reason: "unknown-field" };
    if (typeof candidate.clientEventId !== "string" || !CLIENT_EVENT_ID_RE.test(candidate.clientEventId)) {
      return { ok: false, reason: "client-event-id" };
    }
    if (typeof candidate.name !== "string" || !(PROGRAMME_EVENT_NAMES as readonly string[]).includes(candidate.name)) {
      return { ok: false, reason: "name" };
    }
    const eventName = candidate.name as ProgrammeEventName;
    const detailPolicy = EVENT_DETAILS[eventName];
    if (Object.keys(candidate).some(key => !BASE_EVENT_KEYS.has(key) && !detailPolicy.allowed.has(key))) {
      return { ok: false, reason: "event-field" };
    }
    if ([...detailPolicy.required].some(key => candidate[key] === undefined)) {
      return { ok: false, reason: "event-required-field" };
    }
    if (typeof candidate.sessionId !== "string" || !SESSION_ID_RE.test(candidate.sessionId)) {
      return { ok: false, reason: "session-id" };
    }
    if (typeof candidate.platform !== "string" || !PLATFORMS.has(candidate.platform as ProgrammePlatform)) {
      return { ok: false, reason: "platform" };
    }
    if (typeof candidate.appVersion !== "string" || !APP_VERSION_RE.test(candidate.appVersion)) {
      return { ok: false, reason: "app-version" };
    }
    if (!validOptionalId(candidate.featureId) || !validOptionalId(candidate.moduleId)
      || !validOptionalId(candidate.subjectId) || !validOptionalId(candidate.topicId)) {
      return { ok: false, reason: "content-id" };
    }
    if (candidate.source !== undefined && (typeof candidate.source !== "string" || !SOURCES.has(candidate.source))) {
      return { ok: false, reason: "source" };
    }
    if (candidate.source !== detailPolicy.source) return { ok: false, reason: "event-source" };
    if (candidate.durationBucket !== undefined && (
      typeof candidate.durationBucket !== "string"
      || !DURATION_BUCKETS.has(candidate.durationBucket as DurationBucket)
    )) return { ok: false, reason: "duration" };
    if (candidate.accuracyBand !== undefined && (
      typeof candidate.accuracyBand !== "string" || !ACCURACY_BANDS.has(candidate.accuracyBand)
    )) return { ok: false, reason: "accuracy" };
    if (candidate.sessionType !== undefined && (
      typeof candidate.sessionType !== "string"
      || !SESSION_TYPES.has(candidate.sessionType as SessionType)
    )) return { ok: false, reason: "session-type" };
    if (candidate.confidenceScore !== undefined && (
      typeof candidate.confidenceScore !== "number"
      || !Number.isInteger(candidate.confidenceScore)
      || candidate.confidenceScore < 1
      || candidate.confidenceScore > 5
    )) return { ok: false, reason: "confidence" };

    validated.push(candidate as unknown as ProgrammeEventInput);
  }

  return { ok: true, value: { events: validated } };
}

export function durationBucket(seconds: number): DurationBucket {
  if (!Number.isFinite(seconds) || seconds < 5 * 60) return "under_5m";
  if (seconds < 15 * 60) return "5_14m";
  if (seconds < 30 * 60) return "15_29m";
  if (seconds < 60 * 60) return "30_59m";
  return "60m_plus";
}

export function academicYearFor(date: Date): string {
  const year = date.getUTCFullYear();
  const start = date.getUTCMonth() >= 7 ? year : year - 1;
  return `${start}-${start + 1}`;
}

export function reportableProgrammeCell(value: number): number | null {
  return value === 0 || value >= PROGRAMME_SMALL_CELL_MINIMUM ? value : null;
}

export function reportableProgrammeRatio(numerator: number, denominator: number) {
  if (
    (denominator > 0 && denominator < PROGRAMME_SMALL_CELL_MINIMUM)
    || (numerator > 0 && numerator < PROGRAMME_SMALL_CELL_MINIMUM)
    || (denominator - numerator > 0 && denominator - numerator < PROGRAMME_SMALL_CELL_MINIMUM)
  ) {
    return { numerator: null, denominator: null, percentage: null, suppressed: true };
  }
  return {
    numerator,
    denominator,
    percentage: denominator > 0 ? Math.round((numerator / denominator) * 100) : null,
    suppressed: false,
  };
}
