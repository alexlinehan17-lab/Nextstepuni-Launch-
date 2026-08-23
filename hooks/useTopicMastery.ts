/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback } from 'react';
import { doc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { useFreshProgress } from './useFreshProgress';
import { type TopicMasteryMap, type TopicMasteryV2, type UnifiedConfidence, type TopicMasteryEntry } from '../types';
import { getSyllabusTopicRefs } from '../components/syllabusTopics';
import {
  canonicalMasteryForSpecification,
  emptyTopicMasteryV2,
  mergeTopicMasteryV2,
  migrateTopicMastery,
  projectTopicMastery,
  upsertCanonicalMastery,
} from '../services/topicMasteryMigration';
import { examinationYearFromDate, resolveCurriculumSpecification } from '../curriculumRegistry';
import { reportSaveError } from '../utils/logError';
import { useProgress } from '../contexts/ProgressContext';
import { DEMO_STUDENT_UID } from '../data/devStudent';

export function useTopicMastery(uid: string | undefined, examDate?: string | null) {
  const { updateDemoProgress } = useProgress();
  const isDemo = uid === DEMO_STUDENT_UID;
  const { doc: rawProgressDoc, loaded: progressLoaded } = useFreshProgress(uid);
  const [mastery, setMastery] = useState<TopicMasteryMap>({});
  const [canonicalMastery, setCanonicalMastery] = useState<TopicMasteryV2>(emptyTopicMasteryV2);
  const [isLoaded, setIsLoaded] = useState(false);

  // Load + one-time migration from old data
  useEffect(() => {
    if (!progressLoaded) return;
    if (!uid) { setIsLoaded(true); return; }

    const data = rawProgressDoc;

    let legacyMastery: TopicMasteryMap;
    if (data?.topicMastery) {
      // Already migrated
      legacyMastery = data.topicMastery as TopicMasteryMap;
    } else {
      // Migrate from old formats
      const merged: TopicMasteryMap = {};
      const now = Date.now();

      // Preserve confidence recorded in the retired standalone coverage tool.
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

      legacyMastery = merged;

      // Save migrated data if we had any old data
      if (Object.keys(merged).length > 0) {
        if (isDemo) updateDemoProgress(current => ({ ...current, topicMastery: merged }));
        else setDoc(doc(db, 'progress', uid), { topicMastery: merged }, { merge: true }).catch((e) => reportSaveError('useTopicMastery.save', e));
      }
    }
    const migratedLegacy = migrateTopicMastery(legacyMastery, examDate);
    const storedV2 = data?.topicMasteryV2 as TopicMasteryV2 | undefined;
    const v2 = storedV2?.schemaVersion === 2
      ? mergeTopicMasteryV2(storedV2, migratedLegacy)
      : migratedLegacy;
    const projected = projectTopicMastery(v2);
    for (const [subject, topics] of Object.entries(legacyMastery)) {
      projected[subject] = { ...(projected[subject] ?? {}), ...topics };
    }
    setCanonicalMastery(v2);
    setMastery(projected);
    if (!storedV2 && (Object.keys(v2.topics).length || Object.keys(v2.unresolved).length)) {
      if (isDemo) updateDemoProgress(current => ({ ...current, topicMasteryV2: v2 }));
      else setDoc(doc(db, 'progress', uid), { topicMasteryV2: v2 }, { merge: true })
          .catch((e) => reportSaveError('useTopicMastery.saveV2Migration', e));
    }
    setIsLoaded(true);
  }, [uid, progressLoaded, rawProgressDoc, examDate, isDemo, updateDemoProgress]);

  const persist = useCallback((nextV2: TopicMasteryV2) => {
    if (!uid) return;
    const nextLegacy = projectTopicMastery(nextV2);
    setCanonicalMastery(nextV2);
    setMastery(nextLegacy);
    if (isDemo) updateDemoProgress(current => ({ ...current, topicMasteryV2: nextV2, topicMastery: nextLegacy }));
    else setDoc(doc(db, 'progress', uid), { topicMasteryV2: nextV2, topicMastery: nextLegacy }, { merge: true })
        .catch((e) => reportSaveError('useTopicMastery.save', e));
  }, [uid, isDemo, updateDemoProgress]);

  const setTopicConfidence = useCallback((
    subject: string,
    topic: string,
    confidence: UnifiedConfidence,
    source: TopicMasteryEntry['source'] = 'manual'
  ) => {
    if (!uid) return;
    const entry = { confidence, updatedAt: Date.now(), source };
    persist(upsertCanonicalMastery(canonicalMastery, subject, topic, entry, examDate));
  }, [uid, canonicalMastery, examDate, persist]);

  const importSyllabusTopics = useCallback((subject: string, examDate?: string | null) => {
    if (!uid) return;
    const topics = getSyllabusTopicRefs(subject, examDate);
    if (!topics || topics.length === 0) return;

    let nextV2 = canonicalMastery;
    const subjectMap = mastery[subject] ?? {};
    const now = Date.now();
    let added = false;
    for (const topic of topics) {
      if (!subjectMap[topic.name]) {
        nextV2 = upsertCanonicalMastery(nextV2, subject, topic.name, { confidence: 'not-started', updatedAt: now, source: 'import' }, examDate);
        added = true;
      }
    }
    if (!added) return;
    persist(nextV2);
  }, [uid, mastery, canonicalMastery, examDate, persist]);

  const bulkUpdate = useCallback((subject: string, updates: Record<string, UnifiedConfidence>) => {
    if (!uid) return;
    let nextV2 = canonicalMastery;
    const now = Date.now();
    for (const [topic, confidence] of Object.entries(updates)) {
      nextV2 = upsertCanonicalMastery(nextV2, subject, topic, {
        ...(mastery[subject]?.[topic] ?? {}),
        confidence,
        updatedAt: now,
        source: 'manual',
      }, examDate);
    }
    persist(nextV2);
  }, [uid, mastery, canonicalMastery, examDate, persist]);

  const getTopicConfidence = useCallback((subject: string, topic: string): UnifiedConfidence => {
    return mastery[subject]?.[topic]?.confidence ?? 'not-started';
  }, [mastery]);

  const getSubjectTopics = useCallback((subject: string): Record<string, TopicMasteryEntry> => {
    return mastery[subject] ?? {};
  }, [mastery]);

  const getCanonicalSubjectTopics = useCallback((subject: string) => {
    const specification = resolveCurriculumSpecification(subject, examinationYearFromDate(examDate));
    return specification ? canonicalMasteryForSpecification(canonicalMastery, specification.id) : {};
  }, [canonicalMastery, examDate]);

  return { mastery, canonicalMastery, isLoaded, setTopicConfidence, importSyllabusTopics, bulkUpdate, getTopicConfidence, getSubjectTopics, getCanonicalSubjectTopics };
}
