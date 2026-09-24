/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Fire-and-forget client for NextStepUni's first-party programme measurement.
 * The server owns identity, cohort metadata and retention. This client can send
 * only a small structured vocabulary: never names, email, free text, answers,
 * exact timestamps or exact study duration.
 */
import { getFunctions, httpsCallable } from 'firebase/functions';
import app from '../firebase';
import { logError } from './logError';

export type ProgrammeEventName =
  | 'account_registered'
  | 'session_started'
  | 'feature_exposed'
  | 'feature_started'
  | 'feature_completed'
  | 'module_started'
  | 'module_completed'
  | 'plan_activity_completed'
  | 'study_session_started'
  | 'study_session_completed'
  | 'practice_attempt_completed';

export type ProgrammeEventDetails = {
  featureId?: string;
  moduleId?: string;
  source?: 'app' | 'launchpad' | 'module' | 'study' | 'timetable' | 'registration' | 'practice';
  subjectId?: string;
  topicId?: string;
  accuracyBand?: 'none' | 'partial' | 'strong' | 'full';
  durationBucket?: 'under_5m' | '5_14m' | '15_29m' | '30_59m' | '60m_plus';
  confidenceScore?: number;
  sessionType?: 'new-learning' | 'practice' | 'revision';
};

type EventInput = ProgrammeEventDetails & {
  clientEventId: string;
  name: ProgrammeEventName;
  sessionId: string;
  platform: 'web' | 'ios' | 'android';
  appVersion: string;
};

const SESSION_KEY = 'nsu:programme-measurement-session';
const EXPOSURE_KEY = 'nsu:programme-measurement-exposure';
const SESSION_START_KEY = 'nsu:programme-measurement-session-started';
const PROGRAMME_MEASUREMENT_ENABLED = import.meta.env.VITE_PROGRAMME_MEASUREMENT_ENABLED === 'true';
let memorySessionId = '';
let sessionStartSent = false;
let sessionStartInFlight = false;
let analyticsEpoch = 0;
const memoryExposures = new Set<string>();
const inFlightExposures = new Set<string>();
const retryTimers = new Set<number>();
const RETRY_DELAYS_MS = [1_000, 5_000];

function randomId(): string {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) return crypto.randomUUID();
  if (typeof crypto !== 'undefined' && crypto.getRandomValues) {
    const bytes = crypto.getRandomValues(new Uint8Array(16));
    return Array.from(bytes, value => value.toString(16).padStart(2, '0')).join('');
  }
  return `event-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function sessionId(): string {
  if (memorySessionId) return memorySessionId;
  try {
    const stored = window.sessionStorage.getItem(SESSION_KEY);
    if (stored) return (memorySessionId = stored);
    memorySessionId = randomId();
    window.sessionStorage.setItem(SESSION_KEY, memorySessionId);
  } catch {
    memorySessionId = randomId();
  }
  return memorySessionId;
}

function platform(): 'web' | 'ios' | 'android' {
  const agent = typeof navigator === 'undefined' ? '' : navigator.userAgent;
  if (/android/i.test(agent)) return 'android';
  if (/iphone|ipad|ipod/i.test(agent)) return 'ios';
  return 'web';
}

async function retryDelay(milliseconds: number, expectedEpoch: number): Promise<boolean> {
  return new Promise(resolve => {
    const timer = window.setTimeout(() => {
      retryTimers.delete(timer);
      resolve(expectedEpoch === analyticsEpoch);
    }, milliseconds);
    retryTimers.add(timer);
  });
}

async function send(events: EventInput[]): Promise<boolean> {
  if (!PROGRAMME_MEASUREMENT_ENABLED || events.length === 0) return false;
  const expectedEpoch = analyticsEpoch;
  for (let attempt = 0; attempt <= RETRY_DELAYS_MS.length; attempt++) {
    if (expectedEpoch !== analyticsEpoch) return false;
    try {
      const record = httpsCallable<{ events: EventInput[] }, { accepted: number }>(
        getFunctions(app),
        'recordProgrammeEvents',
      );
      await record({ events });
      return expectedEpoch === analyticsEpoch;
    } catch (error) {
      if (attempt >= RETRY_DELAYS_MS.length) {
        // Measurement must never interrupt the student action being measured.
        logError('programmeAnalytics.record', error);
        return false;
      }
      if (!await retryDelay(RETRY_DELAYS_MS[attempt], expectedEpoch)) return false;
    }
  }
  return false;
}

function createEvent(name: ProgrammeEventName, details: ProgrammeEventDetails): EventInput {
  return {
    clientEventId: randomId(),
    name,
    sessionId: sessionId(),
    platform: platform(),
    appVersion: '0.0.0',
    ...details,
  };
}

export function trackProgrammeEvent(name: ProgrammeEventName, details: ProgrammeEventDetails = {}): void {
  if (!PROGRAMME_MEASUREMENT_ENABLED) return;
  void send([createEvent(name, details)]);
}

export function trackProgrammeSessionStarted(): void {
  if (!PROGRAMME_MEASUREMENT_ENABLED || sessionStartSent || sessionStartInFlight) return;
  const currentSessionId = sessionId();
  try {
    if (window.sessionStorage.getItem(SESSION_START_KEY) === currentSessionId) {
      sessionStartSent = true;
      return;
    }
  } catch {
    // The in-memory guard still prevents re-render inflation in private mode.
  }
  sessionStartInFlight = true;
  const sessionEpoch = analyticsEpoch;
  void send([createEvent('session_started', { source: 'app' })]).then(accepted => {
    if (sessionEpoch !== analyticsEpoch) return;
    sessionStartInFlight = false;
    if (!accepted) return;
    sessionStartSent = true;
    try { window.sessionStorage.setItem(SESSION_START_KEY, currentSessionId); } catch { /* optional */ }
  });
}

export function trackProgrammeExposures(featureIds: string[]): void {
  if (!PROGRAMME_MEASUREMENT_ENABLED) return;
  const unseen: string[] = [];
  let stored = new Set<string>();
  try {
    stored = new Set(JSON.parse(window.sessionStorage.getItem(EXPOSURE_KEY) || '[]') as string[]);
  } catch {
    stored = new Set<string>();
  }
  featureIds.forEach(id => {
    if (stored.has(id) || memoryExposures.has(id) || inFlightExposures.has(id)) return;
    inFlightExposures.add(id);
    unseen.push(id);
  });
  for (let index = 0; index < unseen.length; index += 25) {
    const batchIds = unseen.slice(index, index + 25);
    const exposureEpoch = analyticsEpoch;
    void send(batchIds.map(featureId => createEvent('feature_exposed', {
      featureId,
      source: 'launchpad',
    }))).then(accepted => {
      if (exposureEpoch !== analyticsEpoch) return;
      batchIds.forEach(id => inFlightExposures.delete(id));
      if (!accepted) return;
      batchIds.forEach(id => {
        stored.add(id);
        memoryExposures.add(id);
      });
      try { window.sessionStorage.setItem(EXPOSURE_KEY, JSON.stringify([...stored])); } catch { /* optional */ }
    });
  }
}

export function analyticsDurationBucket(seconds: number): NonNullable<ProgrammeEventDetails['durationBucket']> {
  if (!Number.isFinite(seconds) || seconds < 5 * 60) return 'under_5m';
  if (seconds < 15 * 60) return '5_14m';
  if (seconds < 30 * 60) return '15_29m';
  if (seconds < 60 * 60) return '30_59m';
  return '60m_plus';
}

export function resetProgrammeAnalyticsSession(): void {
  analyticsEpoch += 1;
  memorySessionId = '';
  sessionStartSent = false;
  sessionStartInFlight = false;
  memoryExposures.clear();
  inFlightExposures.clear();
  try {
    window.sessionStorage.removeItem(SESSION_KEY);
    window.sessionStorage.removeItem(EXPOSURE_KEY);
    window.sessionStorage.removeItem(SESSION_START_KEY);
  } catch {
    // Shared-device cleanup is best-effort when storage is unavailable.
  }
}

export const __testing = { randomId, platform, enabled: PROGRAMME_MEASUREMENT_ENABLED };
