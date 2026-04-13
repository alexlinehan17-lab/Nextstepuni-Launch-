/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback } from 'react';
import { doc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { useProgress } from '../contexts/ProgressContext';
import { type TopicMasteryMap, type UnifiedConfidence, type TopicMasteryEntry } from '../types';
import { getSyllabusTopics } from '../components/syllabusTopics';

export function useTopicMastery(uid: string | undefined) {
  const { rawProgressDoc, progressLoaded } = useProgress();
  const [mastery, setMastery] = useState<TopicMasteryMap>({});
  const [isLoaded, setIsLoaded] = useState(false);

  // Load + one-time migration from old data
  useEffect(() => {
    if (!progressLoaded) return;
    if (!uid) { setIsLoaded(true); return; }

    const data = rawProgressDoc;

    if (data?.topicMastery) {
      // Already migrated
      setMastery(data.topicMastery);
    } else {
      // Migrate from old formats
      const merged: TopicMasteryMap = {};
      const now = Date.now();

      // Migrate SyllabusXRay mastery
      if (data?.syllabusXRayMastery) {
        const sxr = data.syllabusXRayMastery as Record<string, Record<string, string>>;
        for (const [subject, topics] of Object.entries(sxr)) {
          if (!merged[subject]) merged[subject] = {};
          for (const [topic, status] of Object.entries(topics)) {
            const confidence: UnifiedConfidence =
              status === 'confident' ? 'solid' :
              status === 'in-progress' ? 'shaky' : 'not-started';
            merged[subject][topic] = { confidence, updatedAt: now, source: 'import' };
          }
        }
      }

      // Merge WarRoom topicMap (takes precedence for overlapping topics if more recent)
      if (data?.warRoom?.topicMap) {
        const wr = data.warRoom.topicMap as Record<string, Array<{ name: string; confidence: string; updatedAt?: number }>>;
        for (const [subject, topics] of Object.entries(wr)) {
          if (!merged[subject]) merged[subject] = {};
          for (const t of topics) {
            const confidence = (t.confidence === 'solid' || t.confidence === 'shaky' || t.confidence === 'not-started')
              ? t.confidence as UnifiedConfidence
              : 'not-started';
            const existing = merged[subject][t.name];
            if (!existing || (t.updatedAt && t.updatedAt > existing.updatedAt)) {
              merged[subject][t.name] = { confidence, updatedAt: t.updatedAt || now, source: 'import' };
            }
          }
        }
      }

      setMastery(merged);

      // Save migrated data if we had any old data
      if (Object.keys(merged).length > 0) {
        setDoc(doc(db, 'progress', uid), { topicMastery: merged }, { merge: true }).catch(() => {});
      }
    }
    setIsLoaded(true);
  }, [uid, progressLoaded, rawProgressDoc]);

  const setTopicConfidence = useCallback((
    subject: string,
    topic: string,
    confidence: UnifiedConfidence,
    source: TopicMasteryEntry['source'] = 'manual'
  ) => {
    if (!uid) return;
    let next: TopicMasteryMap;
    setMastery(prev => {
      next = { ...prev };
      if (!next[subject]) next[subject] = {};
      next[subject] = {
        ...next[subject],
        [topic]: { confidence, updatedAt: Date.now(), source },
      };
      return next;
    });
    setDoc(doc(db, 'progress', uid), { topicMastery: next! }, { merge: true }).catch(() => {});
  }, [uid]);

  const importSyllabusTopics = useCallback((subject: string) => {
    if (!uid) return;
    const topics = getSyllabusTopics(subject);
    if (!topics || topics.length === 0) return;

    let next: TopicMasteryMap;
    setMastery(prev => {
      next = { ...prev };
      if (!next[subject]) next[subject] = {};
      const now = Date.now();
      for (const topicName of topics) {
        // Don't overwrite existing entries
        if (!next[subject][topicName]) {
          next[subject][topicName] = { confidence: 'not-started', updatedAt: now, source: 'import' };
        }
      }
      return next;
    });
    setDoc(doc(db, 'progress', uid), { topicMastery: next! }, { merge: true }).catch(() => {});
  }, [uid]);

  const bulkUpdate = useCallback((subject: string, updates: Record<string, UnifiedConfidence>) => {
    if (!uid) return;
    let next: TopicMasteryMap;
    setMastery(prev => {
      next = { ...prev };
      if (!next[subject]) next[subject] = {};
      const now = Date.now();
      for (const [topic, confidence] of Object.entries(updates)) {
        next[subject][topic] = {
          ...next[subject][topic],
          confidence,
          updatedAt: now,
          source: 'manual',
        };
      }
      return next;
    });
    setDoc(doc(db, 'progress', uid), { topicMastery: next! }, { merge: true }).catch(() => {});
  }, [uid]);

  const getTopicConfidence = useCallback((subject: string, topic: string): UnifiedConfidence => {
    return mastery[subject]?.[topic]?.confidence ?? 'not-started';
  }, [mastery]);

  const getSubjectTopics = useCallback((subject: string): Record<string, TopicMasteryEntry> => {
    return mastery[subject] ?? {};
  }, [mastery]);

  return { mastery, isLoaded, setTopicConfidence, importSyllabusTopics, bulkUpdate, getTopicConfidence, getSubjectTopics };
}
