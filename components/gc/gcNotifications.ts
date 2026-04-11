/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { db } from '../../firebase';
import { doc, getDoc, runTransaction } from 'firebase/firestore';

// ─── Types ──────────────────────────────────────────────────────────────────

export type NotificationType =
  | 'gc-recommendation'
  | 'gc-kudos'
  | 'comeback'
  | 'streak-milestone'
  | 'study-insight'
  | 'subject-neglect'
  | 'gc-broadcast';

export interface AppNotification {
  id: string;
  type: NotificationType;
  title: string;
  body: string;
  timestamp: number;
  read: boolean;
  actionToolId?: string;
  fromGCName?: string;
  severity?: 'info' | 'success' | 'warning';
}

// ─── Helpers ────────────────────────────────────────────────────────────────

const MAX_ITEMS = 200;

function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

/** Read notifications for a user, sorted newest-first. */
export async function getNotifications(uid: string): Promise<AppNotification[]> {
  try {
    const snap = await getDoc(doc(db, 'notifications', uid));
    if (!snap.exists()) return [];
    const items = (snap.data().items || []) as AppNotification[];
    return items.sort((a, b) => b.timestamp - a.timestamp);
  } catch {
    console.error('Failed to read notifications:');
    return [];
  }
}

/** Add a notification to a user's doc using a transaction (trim to MAX_ITEMS). */
export async function addNotification(uid: string, notification: Omit<AppNotification, 'id' | 'timestamp' | 'read'>): Promise<void> {
  const ref = doc(db, 'notifications', uid);
  try {
    await runTransaction(db, async (txn) => {
      const snap = await txn.get(ref);
      const existing: AppNotification[] = snap.exists() ? (snap.data().items || []) : [];
      const newItem: AppNotification = {
        ...notification,
        id: generateId(),
        timestamp: Date.now(),
        read: false,
      };
      const updated = [newItem, ...existing].slice(0, MAX_ITEMS);
      txn.set(ref, { items: updated });
    });
  } catch {
    console.error('Failed to add notification:');
  }
}

/** Mark a single notification as read. */
export async function markNotificationRead(uid: string, notificationId: string): Promise<void> {
  const ref = doc(db, 'notifications', uid);
  try {
    await runTransaction(db, async (txn) => {
      const snap = await txn.get(ref);
      if (!snap.exists()) return;
      const items: AppNotification[] = snap.data().items || [];
      const updated = items.map(n => n.id === notificationId ? { ...n, read: true } : n);
      txn.set(ref, { items: updated });
    });
  } catch {
    console.error('Failed to mark notification read:');
  }
}

/** Mark all notifications as read. */
export async function markAllRead(uid: string): Promise<void> {
  const ref = doc(db, 'notifications', uid);
  try {
    await runTransaction(db, async (txn) => {
      const snap = await txn.get(ref);
      if (!snap.exists()) return;
      const items: AppNotification[] = snap.data().items || [];
      const updated = items.map(n => ({ ...n, read: true }));
      txn.set(ref, { items: updated });
    });
  } catch {
    console.error('Failed to mark all read:');
  }
}

/** Broadcast a notification to multiple students. */
export async function addNotificationToMultiple(
  uids: string[],
  notification: Omit<AppNotification, 'id' | 'timestamp' | 'read'>
): Promise<void> {
  await Promise.allSettled(uids.map(uid => addNotification(uid, notification)));
}

/** Check if a notification of a given type already exists within N days. */
export function hasDuplicateNotification(
  items: AppNotification[],
  type: NotificationType,
  withinDays: number
): boolean {
  const cutoff = Date.now() - withinDays * 86400000;
  return items.some(n => n.type === type && n.timestamp >= cutoff);
}

// ─── Auto-Notification Generator ────────────────────────────────────────────

interface ProgressData {
  timetableCompletions?: Record<string, string[]>;
  timetableStreak?: { currentStreak: number; lastActiveDate: string; longestStreak: number };
  subjectProfile?: {
    subjects: { subjectName: string; level: string; currentGrade: string; targetGrade: string }[];
  };
  studyDebriefs?: { subject: string; strategy: string; confidenceAfter: number; date: string }[];
}

/** Run fire-and-forget after login. Generates auto-notifications with 7-day dedup. */
export async function generateAutoNotifications(uid: string, progressData: ProgressData): Promise<void> {
  try {
    const existing = await getNotifications(uid);

    // 1. Comeback: >5 days since last timetable activity
    if (!hasDuplicateNotification(existing, 'comeback', 7)) {
      const completions = progressData.timetableCompletions || {};
      const lastDate = Object.keys(completions)
        .filter(k => (completions[k]?.length ?? 0) > 0)
        .sort()
        .pop();
      if (lastDate) {
        const daysSince = Math.floor((Date.now() - new Date(lastDate).getTime()) / 86400000);
        if (daysSince > 5) {
          await addNotification(uid, {
            type: 'comeback',
            title: 'Welcome back!',
            body: `You've been away ${daysSince} days \u2014 pick up where you left off.`,
            severity: 'warning',
          });
        }
      }
    }

    // 2. Streak milestones: 7, 14, 30
    if (!hasDuplicateNotification(existing, 'streak-milestone', 7)) {
      const streak = progressData.timetableStreak?.currentStreak ?? 0;
      const milestone = [30, 14, 7].find(m => streak >= m);
      if (milestone) {
        await addNotification(uid, {
          type: 'streak-milestone',
          title: `${streak}-day streak!`,
          body: 'Amazing consistency \u2014 keep it going!',
          severity: 'success',
        });
      }
    }

    // 3. Subject neglect: highest CAO-bargain subject not studied 10+ days
    if (!hasDuplicateNotification(existing, 'subject-neglect', 7)) {
      const subjects = progressData.subjectProfile?.subjects || [];
      const completions = progressData.timetableCompletions || {};
      if (subjects.length > 0) {
        // Find last study date per subject from completions block IDs
        const lastStudiedMap: Record<string, string> = {};
        for (const [dateKey, blocks] of Object.entries(completions)) {
          for (const blockId of blocks) {
            // Block IDs typically contain subject name
            for (const subj of subjects) {
              if (blockId.toLowerCase().includes(subj.subjectName.toLowerCase())) {
                if (!lastStudiedMap[subj.subjectName] || dateKey > lastStudiedMap[subj.subjectName]) {
                  lastStudiedMap[subj.subjectName] = dateKey;
                }
              }
            }
          }
        }
        // Find most neglected subject
        const gradePoints: Record<string, number> = { 'H1': 100, 'H2': 88, 'H3': 77, 'H4': 66, 'H5': 56, 'H6': 46, 'H7': 37, 'H8': 0, 'O1': 56, 'O2': 46, 'O3': 37, 'O4': 28, 'O5': 20, 'O6': 12, 'O7': 0, 'O8': 0 };
        const bestBargain = subjects
          .map(s => ({
            name: s.subjectName,
            gap: (gradePoints[s.targetGrade] ?? 0) - (gradePoints[s.currentGrade] ?? 0),
            lastStudied: lastStudiedMap[s.subjectName],
          }))
          .filter(s => s.gap > 0)
          .sort((a, b) => b.gap - a.gap)[0];

        if (bestBargain && bestBargain.lastStudied) {
          const daysSince = Math.floor((Date.now() - new Date(bestBargain.lastStudied).getTime()) / 86400000);
          if (daysSince >= 10) {
            await addNotification(uid, {
              type: 'subject-neglect',
              title: `${bestBargain.name} needs attention`,
              body: `You haven't studied ${bestBargain.name} in ${daysSince} days \u2014 it's your biggest points opportunity.`,
              severity: 'warning',
            });
          }
        }
      }
    }

    // 4. Study insight: best strategy per subject from debriefs
    if (!hasDuplicateNotification(existing, 'study-insight', 7)) {
      const debriefs = progressData.studyDebriefs || [];
      if (debriefs.length >= 5) {
        // Group by subject, find best strategy
        const bySubject: Record<string, Record<string, { total: number; count: number }>> = {};
        for (const d of debriefs) {
          if (!d.strategy || !d.subject) continue;
          if (!bySubject[d.subject]) bySubject[d.subject] = {};
          if (!bySubject[d.subject][d.strategy]) bySubject[d.subject][d.strategy] = { total: 0, count: 0 };
          bySubject[d.subject][d.strategy].total += d.confidenceAfter;
          bySubject[d.subject][d.strategy].count += 1;
        }
        // Find a subject with a clear best strategy
        for (const [subject, strategies] of Object.entries(bySubject)) {
          const ranked = Object.entries(strategies)
            .map(([name, data]) => ({ name, avg: data.total / data.count }))
            .sort((a, b) => b.avg - a.avg);
          if (ranked.length >= 2 && ranked[0].avg - ranked[1].avg >= 1) {
            // Find another subject that hasn't tried this strategy much
            const bestStrategy = ranked[0].name;
            for (const [otherSubject, otherStrategies] of Object.entries(bySubject)) {
              if (otherSubject === subject) continue;
              const usage = otherStrategies[bestStrategy]?.count ?? 0;
              if (usage < 2) {
                await addNotification(uid, {
                  type: 'study-insight',
                  title: 'Study insight',
                  body: `${bestStrategy} worked best for ${subject} \u2014 try it for ${otherSubject} too.`,
                  severity: 'info',
                });
                return; // Only one insight per login
              }
            }
          }
        }
      }
    }
  } catch {
    console.error('Auto-notification generation failed:');
  }
}
