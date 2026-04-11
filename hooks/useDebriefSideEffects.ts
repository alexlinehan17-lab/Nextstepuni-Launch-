/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { doc, getDoc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { type UnifiedConfidence } from '../types';
import { type DebriefEntry } from '../components/StudyDebrief';
import { qualityFromDebrief, updateSM2, initSM2States, type SubjectSM2State } from '../components/timetableAlgorithm';

/**
 * Process all side effects when a study debrief is submitted.
 * - Updates topic mastery based on confidence gain
 * - Updates SM-2 spaced repetition state
 * - Auto-adds the hardest topic to mastery if not present
 */
export async function processDebriefSideEffects(
  uid: string,
  entry: DebriefEntry,
): Promise<void> {
  try {
    const progressRef = doc(db, 'progress', uid);
    const snap = await getDoc(progressRef);
    const data = snap.data() || {};

    const updates: Record<string, any> = {};

    // 1. Update topic mastery
    const topicMastery = data.topicMastery || {};
    const subject = entry.subject;
    const topic = entry.hardestTopic;

    if (topic && topic !== 'Not specified') {
      if (!topicMastery[subject]) topicMastery[subject] = {};

      const existing = topicMastery[subject][topic];
      let newConfidence: UnifiedConfidence = 'shaky';

      if (entry.confidenceAfter >= 4 && entry.confidenceAfter > entry.confidenceBefore) {
        newConfidence = 'solid';
      } else if (entry.confidenceAfter >= 3) {
        newConfidence = 'shaky';
      } else {
        newConfidence = existing?.confidence || 'shaky';
      }

      // Only advance confidence, never regress from debrief
      if (existing?.confidence === 'solid' && newConfidence !== 'solid') {
        newConfidence = 'solid';
      }

      topicMastery[subject][topic] = {
        confidence: newConfidence,
        updatedAt: Date.now(),
        source: 'debrief' as const,
        lastDebriefDate: entry.date,
        sm2Quality: qualityFromDebrief(entry.confidenceBefore, entry.confidenceAfter, true),
      };

      updates.topicMastery = topicMastery;
    }

    // 1b. Update topicMastery for additionally covered topics (timestamp update only)
    if (entry.topicsCovered && entry.topicsCovered.length > 0) {
      if (!topicMastery[subject]) topicMastery[subject] = {};
      const now = Date.now();
      for (const coveredTopic of entry.topicsCovered) {
        if (coveredTopic === topic) continue; // already handled above
        const existing = topicMastery[subject][coveredTopic];
        // Don't change confidence — just update the timestamp to show it was studied
        topicMastery[subject][coveredTopic] = {
          confidence: existing?.confidence || 'shaky',
          updatedAt: now,
          source: 'debrief' as const,
          lastDebriefDate: entry.date,
        };
      }
      updates.topicMastery = topicMastery;
    }

    // 2. Update SM-2 state for the subject
    let sm2States: SubjectSM2State[] = data.sm2States || [];
    let subjectState = sm2States.find(s => s.subjectName === subject);

    if (!subjectState) {
      // Initialize SM-2 state for this subject
      const newStates = initSM2States([subject]);
      subjectState = newStates[0];
      sm2States.push(subjectState);
    }

    const quality = qualityFromDebrief(entry.confidenceBefore, entry.confidenceAfter, true);
    const updatedState = updateSM2(subjectState, quality);

    sm2States = sm2States.map(s =>
      s.subjectName === subject ? updatedState : s
    );

    updates.sm2States = sm2States;

    // 3. Write all updates at once
    if (Object.keys(updates).length > 0) {
      await setDoc(progressRef, updates, { merge: true });
    }
  } catch {
    console.error('Failed to process debrief side effects:');
  }
}
