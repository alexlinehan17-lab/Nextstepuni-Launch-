/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * First-run funnel instrumentation.
 *
 * ─── WHY THIS EXISTS ───────────────────────────────────────────────────────
 *
 * Until 2026-08-17 the app recorded nothing about whether students could get
 * *in*. Two separate onboarding-fatal bugs (a default exam date in the past
 * that blocked step 7, and a rollback that deleted live accounts mid-flow)
 * both shipped and sat there unseen, because nothing measured the path from
 * "account created" to "using a tool". On launch day a whole cohort arrives at
 * once; without this we would not know whether 90% or 30% of them got through,
 * and a student who bounces on day one does not come back for attempt two.
 *
 * ─── WHY NOT GOOGLE ANALYTICS ──────────────────────────────────────────────
 *
 * `measurementId` is in the Firebase config but `getAnalytics()` is
 * deliberately NOT called. Sending the behavioural data of Irish
 * under-18s to GA4 would add a third-party processor and a US transfer to a
 * DPIA that is already carrying open Schrems II questions
 * (`compliance/SUMMARY.md`). These counts are cheap to hold ourselves, so we
 * do — no third party, no new transfer, no DPIA amendment.
 *
 * ─── WHAT IS STORED ────────────────────────────────────────────────────────
 *
 * `funnelEvents/{autoId}` = `{ step, day, at, platform, sessionId }` and
 * nothing else. NO uid, name, email or school — deliberately, so this
 * collection carries no personal data and needs no retention story beyond its
 * own TTL. `sessionId` is a random per-visit value held in sessionStorage; it
 * exists only so one student's steps can be joined into a single funnel, and
 * it is not linkable to an account.
 *
 * ─── KNOWN GAP ─────────────────────────────────────────────────────────────
 *
 * Only authenticated steps are recorded. Firestore rules require auth to write
 * here, because an unauthenticated write endpoint is an open spam target. So a
 * student who abandons ON the registration form is invisible. If signup
 * abandonment turns out to matter, route the pre-auth steps through a callable
 * function rather than opening the collection.
 *
 * Fire-and-forget by contract: `trackFunnel` never throws, never blocks the UI
 * and never surfaces an error to the student. Losing a metric must never cost
 * a student their place in the flow.
 */

import { addDoc, collection, serverTimestamp } from 'firebase/firestore';
import { db } from '../firebase';
import { logError } from './logError';

/**
 * The first-run path, in order. Keep this list short and stable — it is the
 * spine of the launch-day dashboard, not a general event bus. Adding a step is
 * fine; renaming one silently breaks historical comparisons.
 */
export const FUNNEL_STEPS = [
  'register_succeeded',
  'onboarding_started',
  'onboarding_reached_subjects',
  'onboarding_reached_exam_date',
  'onboarding_completed',
  'onboarding_skipped',
  'first_tool_opened',
] as const;

export type FunnelStep = (typeof FUNNEL_STEPS)[number];

const SESSION_KEY = 'nsu:funnel-session';
const SENT_KEY = 'nsu:funnel-sent';

/**
 * A random per-visit id. Held in sessionStorage so it survives the reloads
 * onboarding can cause (iOS can evict a Capacitor WebView mid-flow) but dies
 * with the tab. Falls back to an in-memory value where storage is unavailable
 * (Safari private mode), and to a fixed placeholder if even that fails — a
 * degraded join key is better than a thrown error in a fire-and-forget path.
 */
let memorySessionId = '';

function randomId(): string {
  const globalCrypto = typeof crypto !== 'undefined' ? crypto : undefined;
  if (globalCrypto?.randomUUID) return globalCrypto.randomUUID();
  if (globalCrypto?.getRandomValues) {
    const bytes = globalCrypto.getRandomValues(new Uint8Array(16));
    return Array.from(bytes, byte => byte.toString(16).padStart(2, '0')).join('');
  }
  return `nocrypto-${Date.now()}`;
}

function sessionId(): string {
  if (memorySessionId) return memorySessionId;
  try {
    const stored = window.sessionStorage.getItem(SESSION_KEY);
    if (stored) {
      memorySessionId = stored;
      return stored;
    }
    memorySessionId = randomId();
    window.sessionStorage.setItem(SESSION_KEY, memorySessionId);
  } catch {
    memorySessionId = memorySessionId || randomId();
  }
  return memorySessionId;
}

/** Local (Irish) calendar day — never toISOString, which rolls back a day at UTC+1. */
function localDay(date: Date = new Date()): string {
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${date.getFullYear()}-${month}-${day}`;
}

function platform(): 'web' | 'ios' | 'android' {
  const agent = typeof navigator !== 'undefined' ? navigator.userAgent : '';
  if (/android/i.test(agent)) return 'android';
  if (/iphone|ipad|ipod/i.test(agent)) return 'ios';
  return 'web';
}

/**
 * Record a first-run step. Fire-and-forget: call it and move on.
 *
 * Each step is recorded at most once per session, so a re-render or a student
 * stepping backwards and forwards through onboarding cannot inflate the count.
 * That makes the numbers readable as "students who reached step N".
 */
export function trackFunnel(step: FunnelStep): void {
  try {
    const id = sessionId();
    const seenKey = `${SENT_KEY}:${id}`;
    let seen: string[] = [];
    try {
      seen = JSON.parse(window.sessionStorage.getItem(seenKey) ?? '[]') as string[];
    } catch {
      seen = [];
    }
    if (seen.includes(step)) return;
    try {
      window.sessionStorage.setItem(seenKey, JSON.stringify([...seen, step]));
    } catch {
      /* storage unavailable — still send, at worst we double-count one visit */
    }

    void addDoc(collection(db, 'funnelEvents'), {
      step,
      day: localDay(),
      at: serverTimestamp(),
      platform: platform(),
      sessionId: id,
    }).catch(err => logError(`trackFunnel.${step}`, err));
  } catch (err) {
    // A metric must never break the flow it is measuring.
    logError(`trackFunnel.${step}`, err);
  }
}

/** Exposed for tests. */
export const __testing = { localDay, randomId };
