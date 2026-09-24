/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * First-party programme measurement for a child-focused service.
 *
 * Raw events are server-only, pseudonymous, structured and time-limited. The
 * client never chooses cohort metadata and the admin UI receives aggregates,
 * not event rows. Names, email addresses, free text, answers and exact study
 * durations are outside this contract by design.
 */
import { randomUUID } from "crypto";
import { FieldValue, Timestamp, getFirestore } from "firebase-admin/firestore";
import { defineBoolean } from "firebase-functions/params";
import { HttpsError, onCall } from "firebase-functions/v2/https";
import { CALLABLE_OPTIONS, assertUnrevokedAuth, isVerifiedAdminToken } from "./security";
import {
  academicYearFor,
  PROGRAMME_SMALL_CELL_MINIMUM,
  reportableProgrammeCell,
  reportableProgrammeRatio,
  validateProgrammeEventBatch,
  type ProgrammeEventInput,
} from "./programmeAnalyticsPolicy";

const ANALYTICS_RETENTION_DAYS = 400;
const RATE_LIMIT_RETENTION_DAYS = 2;
const DAILY_EVENT_LIMIT = 300;
const SMALL_CELL_MINIMUM = PROGRAMME_SMALL_CELL_MINIMUM;
const ACTIVATION_EVENTS = new Set(["feature_started", "module_started", "study_session_started"]);
const PROGRAMME_MEASUREMENT_ENABLED = defineBoolean("PROGRAMME_MEASUREMENT_ENABLED", {
  default: false,
  description: "Enable first-party programme measurement after controller approval and updated-notice rollout.",
});

type StoredEvent = Omit<ProgrammeEventInput, "name" | "clientEventId"> & {
  eventName: ProgrammeEventInput["name"];
  analyticsId: string;
  day: string;
  weekStart: string;
  schoolId: string;
  yearGroup: string;
  academicYear: string;
  rolloutCohort: string;
  occurredAt: Timestamp;
};

type UserRow = {
  uid: string;
  role?: string;
  isAdmin?: boolean;
  school?: string;
  yearGroup?: string;
  createdAt?: unknown;
};

function dublinDay(date: Date): string {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Europe/Dublin",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).formatToParts(date);
  const part = (type: "year" | "month" | "day") => parts.find(item => item.type === type)?.value || "";
  return `${part("year")}-${part("month")}-${part("day")}`;
}

function shiftDay(day: string, delta: number): string {
  const date = new Date(`${day}T12:00:00Z`);
  date.setUTCDate(date.getUTCDate() + delta);
  return date.toISOString().slice(0, 10);
}

function weekStart(day: string): string {
  const date = new Date(`${day}T12:00:00Z`);
  const weekday = date.getUTCDay();
  return shiftDay(day, -(weekday === 0 ? 6 : weekday - 1));
}

function timestampMillis(value: unknown): number | null {
  if (typeof value === "string") {
    const ms = Date.parse(value);
    return Number.isFinite(ms) ? ms : null;
  }
  if (value instanceof Timestamp) return value.toMillis();
  if (value && typeof value === "object" && "toDate" in value && typeof (value as { toDate?: unknown }).toDate === "function") {
    const ms = (value as { toDate: () => Date }).toDate().getTime();
    return Number.isFinite(ms) ? ms : null;
  }
  return null;
}

function percent(numerator: number, denominator: number): number | null {
  return denominator > 0 ? Math.round((numerator / denominator) * 100) : null;
}

function reportableCount(events: StoredEvent[]): number | null {
  const contributors = new Set(events.map(event => event.analyticsId)).size;
  return contributors >= SMALL_CELL_MINIMUM || events.length === 0 ? events.length : null;
}

function isStudent(data: Record<string, unknown>): boolean {
  return data.isAdmin !== true && !["admin", "gc", "staff"].includes(String(data.role || "student"));
}

function safeCohortValue(value: unknown, fallback: string): string {
  if (typeof value !== "string") return fallback;
  const trimmed = value.trim();
  return /^[A-Za-z0-9_-]{1,64}$/.test(trimmed) ? trimmed : fallback;
}

function eventFeatureKey(event: StoredEvent): string | null {
  if (event.featureId) return event.featureId;
  if (event.moduleId) return `module:${event.moduleId}`;
  if (event.eventName === "study_session_started" || event.eventName === "study_session_completed") return "study-session";
  return null;
}

export const recordProgrammeEvents = onCall(
  { ...CALLABLE_OPTIONS, maxInstances: 20 },
  async request => {
    if (!request.auth) throw new HttpsError("unauthenticated", "Must be logged in.");
    await assertUnrevokedAuth(request.auth);
    if (!PROGRAMME_MEASUREMENT_ENABLED.value()) {
      throw new HttpsError("failed-precondition", "Programme measurement is not enabled.");
    }

    const validation = validateProgrammeEventBatch(request.data);
    if (!validation.ok) throw new HttpsError("invalid-argument", `Invalid measurement event: ${validation.reason}.`);

    const db = getFirestore();
    const userRef = db.collection("users").doc(request.auth.uid);
    const subjectRef = db.collection("analyticsSubjects").doc(request.auth.uid);
    const [userSnapshot, progressSnapshot] = await Promise.all([
      userRef.get(),
      db.collection("progress").doc(request.auth.uid).get(),
    ]);
    const user = userSnapshot.data() || {};
    if (!userSnapshot.exists || !isStudent(user)) {
      throw new HttpsError("permission-denied", "Programme measurement is available only to student accounts.");
    }

    const now = new Date();
    const day = dublinDay(now);
    const expiresAt = Timestamp.fromDate(new Date(now.getTime() + ANALYTICS_RETENTION_DAYS * 24 * 60 * 60 * 1000));
    const rateExpiresAt = Timestamp.fromDate(new Date(now.getTime() + RATE_LIMIT_RETENTION_DAYS * 24 * 60 * 60 * 1000));
    const proposedAnalyticsId = randomUUID().replaceAll("-", "");
    const schoolId = safeCohortValue(user.school, "not-set");
    const progress = progressSnapshot.data() || {};
    const subjectProfile = progress.subjectProfile && typeof progress.subjectProfile === "object"
      ? progress.subjectProfile as Record<string, unknown>
      : {};
    const yearGroup = safeCohortValue(user.yearGroup ?? subjectProfile.yearGroup, "not-set");
    const academicYear = academicYearFor(now);
    const rolloutCohort = safeCohortValue(user.rolloutCohort, academicYear);

    await db.runTransaction(async transaction => {
      const subjectSnapshot = await transaction.get(subjectRef);
      const analyticsId = subjectSnapshot.exists
        ? String(subjectSnapshot.data()?.analyticsId || "")
        : proposedAnalyticsId;
      if (!/^[a-f0-9]{32}$/.test(analyticsId)) {
        throw new HttpsError("failed-precondition", "The measurement identifier is invalid.");
      }

      const rateRef = db.collection("programmeEventRateLimits").doc(`${analyticsId}_${day}`);
      const rateSnapshot = await transaction.get(rateRef);
      const currentCount = rateSnapshot.exists ? Number(rateSnapshot.data()?.count || 0) : 0;
      if (currentCount + validation.value.events.length > DAILY_EVENT_LIMIT) {
        throw new HttpsError("resource-exhausted", "The daily measurement limit has been reached.");
      }

      if (!subjectSnapshot.exists) {
        transaction.create(subjectRef, {
          analyticsId,
          createdAt: FieldValue.serverTimestamp(),
        });
      }
      transaction.set(rateRef, {
        analyticsId,
        day,
        count: currentCount + validation.value.events.length,
        expiresAt: rateExpiresAt,
      });

      for (const event of validation.value.events) {
        const eventRef = db.collection("programmeEvents").doc(`${analyticsId}_${event.clientEventId}`);
        transaction.set(eventRef, {
          eventVersion: 1,
          analyticsId,
          eventName: event.name,
          day,
          weekStart: weekStart(day),
          occurredAt: FieldValue.serverTimestamp(),
          expiresAt,
          schoolId,
          yearGroup,
          academicYear,
          rolloutCohort,
          sessionId: event.sessionId,
          platform: event.platform,
          appVersion: event.appVersion,
          ...(event.featureId ? { featureId: event.featureId } : {}),
          ...(event.moduleId ? { moduleId: event.moduleId } : {}),
          ...(event.source ? { source: event.source } : {}),
          ...(event.subjectId ? { subjectId: event.subjectId } : {}),
          ...(event.topicId ? { topicId: event.topicId } : {}),
          ...(event.accuracyBand ? { accuracyBand: event.accuracyBand } : {}),
          ...(event.durationBucket ? { durationBucket: event.durationBucket } : {}),
          ...(event.confidenceScore ? { confidenceScore: event.confidenceScore } : {}),
          ...(event.sessionType ? { sessionType: event.sessionType } : {}),
        });
      }
    });

    return { accepted: validation.value.events.length };
  },
);

export const getProgrammeAnalyticsSummary = onCall(
  { ...CALLABLE_OPTIONS, maxInstances: 5 },
  async request => {
    if (!request.auth) throw new HttpsError("unauthenticated", "Must be logged in.");
    await assertUnrevokedAuth(request.auth, true);
    if (!isVerifiedAdminToken(request.auth.token)) {
      throw new HttpsError("permission-denied", "Administrator access is required.");
    }

    const input = (request.data || {}) as { rangeDays?: unknown; schoolId?: unknown; yearGroup?: unknown };
    const rangeDays = input.rangeDays === 7 || input.rangeDays === 28 || input.rangeDays === 84
      ? input.rangeDays
      : 28;
    if (!PROGRAMME_MEASUREMENT_ENABLED.value()) {
      return {
        enabled: false,
        rangeDays,
        generatedAt: new Date().toISOString(),
        suppressed: false,
        suppressionMinimum: SMALL_CELL_MINIMUM,
        registeredStudents: null,
      };
    }
    const schoolFilter = typeof input.schoolId === "string" && input.schoolId !== "all" ? input.schoolId : null;
    const yearFilter = typeof input.yearGroup === "string" && input.yearGroup !== "all" ? input.yearGroup : null;
    if (schoolFilter && !/^[A-Za-z0-9_-]{1,64}$/.test(schoolFilter)) throw new HttpsError("invalid-argument", "Invalid school filter.");
    if (yearFilter && !/^[A-Za-z0-9_-]{1,64}$/.test(yearFilter)) throw new HttpsError("invalid-argument", "Invalid year-group filter.");

    const db = getFirestore();
    const today = dublinDay(new Date());
    const rangeStart = shiftDay(today, -(rangeDays - 1));
    const historyStart = shiftDay(today, -(ANALYTICS_RETENTION_DAYS - 1));
    const activeWeekStart = shiftDay(today, -6);

    const [userSnapshot, progressSnapshot, subjectSnapshot, eventSnapshot] = await Promise.all([
      db.collection("users").get(),
      db.collection("progress").get(),
      db.collection("analyticsSubjects").get(),
      db.collection("programmeEvents").where("day", ">=", historyStart).get(),
    ]);

    const progressYearByUid = new Map<string, string>();
    progressSnapshot.docs.forEach(doc => {
      const profile = doc.data().subjectProfile;
      if (!profile || typeof profile !== "object") return;
      const yearGroup = (profile as Record<string, unknown>).yearGroup;
      if (typeof yearGroup === "string") progressYearByUid.set(doc.id, yearGroup);
    });

    const users: UserRow[] = userSnapshot.docs
      .filter(doc => isStudent(doc.data()))
      .map(doc => {
        const data = doc.data();
        return {
          uid: doc.id,
          ...data,
          yearGroup: typeof data.yearGroup === "string" ? data.yearGroup : progressYearByUid.get(doc.id),
        } as UserRow;
      });
    const filteredUsers = users.filter(user => (
      (!schoolFilter || (user.school || "not-set") === schoolFilter)
      && (!yearFilter || (user.yearGroup || "not-set") === yearFilter)
    ));
    const hasSmallPartition = (values: string[]) => {
      const counts = new Map<string, number>();
      values.forEach(value => counts.set(value, (counts.get(value) || 0) + 1));
      return [...counts.values()].some(count => count > 0 && count < SMALL_CELL_MINIMUM);
    };
    const secondarySuppression = (
      (!schoolFilter && hasSmallPartition(filteredUsers.map(user => user.school || "not-set")))
      || (!yearFilter && hasSmallPartition(filteredUsers.map(user => user.yearGroup || "not-set")))
    );
    const suppressed = (
      (filteredUsers.length > 0 && filteredUsers.length < SMALL_CELL_MINIMUM)
      || secondarySuppression
    );

    const analyticsIdByUid = new Map<string, string>();
    subjectSnapshot.docs.forEach(doc => {
      const id = doc.data().analyticsId;
      if (typeof id === "string") analyticsIdByUid.set(doc.id, id);
    });

    const storedEvents = eventSnapshot.docs.map(doc => doc.data() as StoredEvent);
    const measurementStartedOn = storedEvents.reduce<string | null>((earliest, event) => (
      !earliest || event.day < earliest ? event.day : earliest
    ), null);
    const allEvents = storedEvents
      .filter(event => (
        (!schoolFilter || event.schoolId === schoolFilter)
        && (!yearFilter || event.yearGroup === yearFilter)
      ));

    if (suppressed) {
      return {
        rangeDays,
        generatedAt: new Date().toISOString(),
        suppressed: true,
        suppressionMinimum: SMALL_CELL_MINIMUM,
        registeredStudents: null,
      };
    }

    const rangeEvents = allEvents.filter(event => event.day >= rangeStart && event.day <= today);
    const activationEvents = allEvents.filter(event => ACTIVATION_EVENTS.has(event.eventName));
    const firstActivationById = new Map<string, number>();
    for (const event of activationEvents) {
      const ms = timestampMillis(event.occurredAt);
      if (ms === null) continue;
      const current = firstActivationById.get(event.analyticsId);
      if (current === undefined || ms < current) firstActivationById.set(event.analyticsId, ms);
    }

    let activationEligible = 0;
    let activatedWithinSevenDays = 0;
    const nowMs = Date.now();
    const matureActivationCutoff = nowMs - 7 * 24 * 60 * 60 * 1000;
    for (const user of filteredUsers) {
      const createdMs = timestampMillis(user.createdAt);
      const analyticsId = analyticsIdByUid.get(user.uid);
      if (
        createdMs === null
        || !measurementStartedOn
        || createdMs < Date.parse(`${measurementStartedOn}T00:00:00Z`)
        || createdMs > matureActivationCutoff
      ) continue;
      activationEligible++;
      const firstActivation = analyticsId ? firstActivationById.get(analyticsId) : undefined;
      if (firstActivation !== undefined && firstActivation >= createdMs && firstActivation <= createdMs + 7 * 24 * 60 * 60 * 1000) {
        activatedWithinSevenDays++;
      }
    }

    const activatedIds = new Set(activationEvents.map(event => event.analyticsId));
    const weeklyActiveIds = new Set(
      allEvents
        .filter(event => event.eventName === "session_started" && event.day >= activeWeekStart && event.day <= today)
        .map(event => event.analyticsId),
    );
    const participatingIds = new Set([...weeklyActiveIds].filter(id => activatedIds.has(id)));

    const retentionCandidates = [...firstActivationById.entries()].filter(([, activatedAt]) => {
      const ageDays = (nowMs - activatedAt) / (24 * 60 * 60 * 1000);
      return ageDays >= 28;
    });
    let retainedAtWeekFour = 0;
    for (const [analyticsId, activatedAt] of retentionCandidates) {
      const weekFourStart = activatedAt + 21 * 24 * 60 * 60 * 1000;
      const weekFourEnd = activatedAt + 28 * 24 * 60 * 60 * 1000;
      if (allEvents.some(event => {
        if (event.analyticsId !== analyticsId || event.eventName !== "session_started") return false;
        const occurred = timestampMillis(event.occurredAt);
        return occurred !== null && occurred >= weekFourStart && occurred < weekFourEnd;
      })) retainedAtWeekFour++;
    }

    const featureStats = new Map<string, { exposed: Set<string>; started: Set<string>; completed: Set<string> }>();
    for (const event of rangeEvents) {
      const key = eventFeatureKey(event);
      if (!key) continue;
      const current = featureStats.get(key) || { exposed: new Set<string>(), started: new Set<string>(), completed: new Set<string>() };
      if (event.eventName === "feature_exposed") current.exposed.add(event.analyticsId);
      if (["feature_started", "module_started", "study_session_started"].includes(event.eventName)) current.started.add(event.analyticsId);
      if (["feature_completed", "module_completed", "study_session_completed", "plan_activity_completed"].includes(event.eventName)) current.completed.add(event.analyticsId);
      featureStats.set(key, current);
    }
    const featureRows = [...featureStats.entries()]
      .filter(([, stats]) => stats.started.size >= SMALL_CELL_MINIMUM)
      .map(([id, stats]) => {
        // A finish is counted as successful only when the same student also
        // started that flow inside the selected period. This keeps the rate
        // bounded and avoids attributing old starts to the current window.
        const successfulStarters = new Set(
          [...stats.completed].filter(analyticsId => stats.started.has(analyticsId)),
        );
        const completionInstrumented = id.startsWith("module:") || id === "study-session";
        return {
          id,
          exposed: reportableProgrammeCell(stats.exposed.size),
          started: stats.started.size,
          completed: completionInstrumented ? reportableProgrammeCell(successfulStarters.size) : null,
          successRate: completionInstrumented && (successfulStarters.size === 0 || successfulStarters.size >= SMALL_CELL_MINIMUM)
            ? percent(successfulStarters.size, stats.started.size)
            : null,
        };
      })
      .sort((a, b) => b.started - a.started || (b.completed ?? 0) - (a.completed ?? 0))
      .slice(0, 20);

    const confidenceScores = rangeEvents
      .filter(event => event.eventName === "study_session_completed" && typeof event.confidenceScore === "number")
      .map(event => event.confidenceScore as number);
    const averageConfidence = confidenceScores.length > 0
      ? Math.round((confidenceScores.reduce((sum, score) => sum + score, 0) / confidenceScores.length) * 10) / 10
      : null;
    const practiceAttempts = rangeEvents.filter(event => event.eventName === "practice_attempt_completed");
    const strongPracticeEvents = practiceAttempts.filter(event => event.accuracyBand === "strong" || event.accuracyBand === "full");
    const strongPracticeAttempts = strongPracticeEvents.length;
    const practiceContributors = new Set(practiceAttempts.map(event => event.analyticsId)).size;
    const confidenceContributors = new Set(
      rangeEvents
        .filter(event => event.eventName === "study_session_completed" && typeof event.confidenceScore === "number")
        .map(event => event.analyticsId),
    ).size;
    const canReportPractice = practiceAttempts.length === 0 || practiceContributors >= SMALL_CELL_MINIMUM;
    const canReportConfidence = confidenceScores.length === 0 || confidenceContributors >= SMALL_CELL_MINIMUM;
    const rangeContributors = new Set(rangeEvents.map(event => event.analyticsId)).size;
    const canReportEventVolume = rangeEvents.length === 0 || rangeContributors >= SMALL_CELL_MINIMUM;
    const strongPracticeContributors = new Set(strongPracticeEvents.map(event => event.analyticsId)).size;
    const canReportStrongPractice = strongPracticeAttempts === 0 || strongPracticeContributors >= SMALL_CELL_MINIMUM;

    const weeklyTrend = Array.from({ length: 12 }, (_, index) => {
      const start = shiftDay(weekStart(today), -(11 - index) * 7);
      const end = shiftDay(start, 6);
      const active = new Set(
        allEvents
          .filter(event => event.eventName === "session_started" && event.day >= start && event.day <= end)
          .map(event => event.analyticsId),
      );
      return { weekStart: start, activeStudents: reportableProgrammeCell(active.size) };
    });

    return {
      enabled: true,
      rangeDays,
      rangeStart,
      rangeEnd: today,
      generatedAt: new Date().toISOString(),
      suppressed: false,
      suppressionMinimum: SMALL_CELL_MINIMUM,
      measurementStartedOn,
      registeredStudents: filteredUsers.length,
      eligibleStudents: null,
      activation: reportableProgrammeRatio(activatedWithinSevenDays, activationEligible),
      weeklyParticipation: reportableProgrammeRatio(participatingIds.size, activatedIds.size),
      fourWeekRetention: reportableProgrammeRatio(retainedAtWeekFour, retentionCandidates.length),
      planActivitiesCompleted: reportableCount(rangeEvents.filter(event => event.eventName === "plan_activity_completed")),
      studySessionsCompleted: reportableCount(rangeEvents.filter(event => event.eventName === "study_session_completed")),
      practiceAttemptsCompleted: canReportPractice ? practiceAttempts.length : null,
      strongPracticeAttempts: canReportPractice && canReportStrongPractice ? strongPracticeAttempts : null,
      strongPracticePercentage: canReportPractice && canReportStrongPractice
        ? percent(strongPracticeAttempts, practiceAttempts.length)
        : null,
      averageConfidence: canReportConfidence ? averageConfidence : null,
      confidenceResponses: canReportConfidence ? confidenceScores.length : null,
      featureRows,
      weeklyTrend,
      coverage: {
        eventCount: canReportEventVolume ? rangeEvents.length : null,
        studentsWithAnalyticsId: reportableProgrammeCell(
          filteredUsers.filter(user => analyticsIdByUid.has(user.uid)).length,
        ),
        studentsWithRegistrationDate: reportableProgrammeCell(
          filteredUsers.filter(user => timestampMillis(user.createdAt) !== null).length,
        ),
      },
      awaitingProgrammeInput: [
        "Eligible or invited student counts",
        "Baseline and endline confidence survey",
        "Baseline and endline decision-readiness survey",
        "Feature and programme helpfulness prompts",
        "School rollout milestones",
        "Verified educational outcomes",
        "School continuation decision",
        "Structured reliability and failure telemetry",
      ],
    };
  },
);
