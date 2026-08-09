/** @license SPDX-License-Identifier: Apache-2.0 */
import {
  examinationYearFromDate,
  resolveCurriculumSpecification,
  resolveSubjectId,
} from '../curriculumRegistry';
import { getSyllabusTopicRefs, type SyllabusCoverageTopic } from '../components/syllabusTopics';
import type {
  CanonicalTopicMasteryEntry,
  TopicMasteryEntry,
  TopicMasteryMap,
  TopicMasteryV2,
} from '../types';

export const TOPIC_MASTERY_SCHEMA_VERSION = 2 as const;

const normalise = (value: string) => value.trim().toLowerCase().replace(/[–—]/g, '-').replace(/\s+/g, ' ');

export function canonicalMasteryKey(specificationId: string, topicId: string): string {
  return `${specificationId}::${topicId}`;
}

export function emptyTopicMasteryV2(): TopicMasteryV2 {
  return { schemaVersion: TOPIC_MASTERY_SCHEMA_VERSION, topics: {}, unresolved: {} };
}

function uniqueLabelMatch(refs: SyllabusCoverageTopic[], label: string): SyllabusCoverageTopic | undefined {
  const target = normalise(label);
  const matches = refs.filter((ref) => normalise(ref.name) === target || (ref.code && normalise(ref.code) === target));
  return matches.length === 1 ? matches[0] : undefined;
}

function retainNewest<T extends TopicMasteryEntry>(existing: T | undefined, candidate: T): T {
  return !existing || candidate.updatedAt >= existing.updatedAt ? candidate : existing;
}

/**
 * Lossless migration: only exact, unique labels enter the canonical namespace.
 * Everything else is preserved byte-for-byte in `unresolved`.
 */
export function migrateTopicMastery(
  legacy: TopicMasteryMap | undefined,
  examDate?: string | null,
): TopicMasteryV2 {
  const next = emptyTopicMasteryV2();
  for (const [subjectName, subjectTopics] of Object.entries(legacy ?? {})) {
    const subjectId = resolveSubjectId(subjectName);
    const specification = subjectId
      ? resolveCurriculumSpecification(subjectId, examinationYearFromDate(examDate))
      : undefined;
    const refs = specification ? getSyllabusTopicRefs(subjectName, examDate) : [];

    for (const [topicName, entry] of Object.entries(subjectTopics)) {
      const ref = uniqueLabelMatch(refs, topicName);
      if (subjectId && specification && ref) {
        const key = canonicalMasteryKey(specification.id, ref.id);
        const canonical: CanonicalTopicMasteryEntry = {
          ...entry,
          subjectId,
          subjectName: specification.subjectName,
          specificationId: specification.id,
          topicId: ref.id,
          topicName: ref.name,
        };
        next.topics[key] = retainNewest(next.topics[key], canonical);
      } else {
        next.unresolved[subjectName] ??= {};
        next.unresolved[subjectName][topicName] = entry;
      }
    }
  }
  return next;
}

/** Display-name projection retained for existing timetable/recommendation UI. */
export function projectTopicMastery(v2: TopicMasteryV2): TopicMasteryMap {
  const projected: TopicMasteryMap = {};
  for (const entry of Object.values(v2.topics)) {
    projected[entry.subjectName] ??= {};
    const legacyEntry: TopicMasteryEntry = {
      confidence: entry.confidence,
      updatedAt: entry.updatedAt,
      source: entry.source,
      ...(entry.lastDebriefDate ? { lastDebriefDate: entry.lastDebriefDate } : {}),
      ...(entry.sm2Quality !== undefined ? { sm2Quality: entry.sm2Quality } : {}),
    };
    projected[entry.subjectName][entry.topicName] = retainNewest(
      projected[entry.subjectName][entry.topicName],
      legacyEntry,
    );
  }
  for (const [subject, topics] of Object.entries(v2.unresolved)) {
    projected[subject] ??= {};
    for (const [topic, entry] of Object.entries(topics)) {
      projected[subject][topic] = retainNewest(projected[subject][topic], entry);
    }
  }
  return projected;
}

/** Reconciles writes from legacy consumers without allowing stale data to win. */
export function mergeTopicMasteryV2(base: TopicMasteryV2, incoming: TopicMasteryV2): TopicMasteryV2 {
  const merged: TopicMasteryV2 = {
    schemaVersion: TOPIC_MASTERY_SCHEMA_VERSION,
    topics: { ...base.topics },
    unresolved: { ...base.unresolved },
  };
  for (const [key, entry] of Object.entries(incoming.topics)) {
    merged.topics[key] = retainNewest(merged.topics[key], entry);
  }
  for (const [subject, topics] of Object.entries(incoming.unresolved)) {
    merged.unresolved[subject] = { ...(merged.unresolved[subject] ?? {}) };
    for (const [topic, entry] of Object.entries(topics)) {
      merged.unresolved[subject][topic] = retainNewest(merged.unresolved[subject][topic], entry);
    }
  }
  return merged;
}

export function upsertCanonicalMastery(
  current: TopicMasteryV2,
  subject: string,
  topic: string,
  entry: TopicMasteryEntry,
  examDate?: string | null,
): TopicMasteryV2 {
  const next: TopicMasteryV2 = {
    schemaVersion: TOPIC_MASTERY_SCHEMA_VERSION,
    topics: { ...current.topics },
    unresolved: { ...current.unresolved },
  };
  const subjectId = resolveSubjectId(subject);
  const specification = subjectId
    ? resolveCurriculumSpecification(subjectId, examinationYearFromDate(examDate))
    : undefined;
  const ref = specification ? uniqueLabelMatch(getSyllabusTopicRefs(subject, examDate), topic) : undefined;
  if (subjectId && specification && ref) {
    const key = canonicalMasteryKey(specification.id, ref.id);
    next.topics[key] = {
      ...entry,
      subjectId,
      subjectName: specification.subjectName,
      specificationId: specification.id,
      topicId: ref.id,
      topicName: ref.name,
    };
    return next;
  }
  next.unresolved[subject] = { ...(next.unresolved[subject] ?? {}), [topic]: entry };
  return next;
}

export function canonicalMasteryForSpecification(
  v2: TopicMasteryV2,
  specificationId: string,
): Record<string, CanonicalTopicMasteryEntry> {
  return Object.fromEntries(Object.values(v2.topics)
    .filter((entry) => entry.specificationId === specificationId)
    .map((entry) => [entry.topicId, entry]));
}
