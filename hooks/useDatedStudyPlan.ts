import { useEffect, useMemo, useState, useSyncExternalStore } from "react";
import { useLocalDateKey } from "./useLocalDateKey";
import { useAuth } from "../contexts/AuthContext";
import { useOptionalProgress } from "../contexts/ProgressContext";
import type { StudentSubjectProfile } from "../components/subjectData";
import {
  buildStudyPlan,
  preserveLegacyCompletions,
  initialPlanSettings,
  dateKey,
  mondayOf,
  planTimetable,
  type PlanInputs,
  type TopicEvidence,
} from "../services/studyPlanEngine";
import {
  saveStudyPlan,
  readStudyPlan,
  subscribeStudyPlan,
} from "../services/studyPlanStore";
import {
  readLocal,
  memoryFor,
  fetchDeck,
  mergeDecks,
  writeLocal,
} from "../components/MarkBank/store";
import { CARD_ID_ALIASES } from "../components/MarkBank/cardAliases";
import { dueAt, retentionFor } from "../components/MarkBank/scheduler";
import { levelsFor } from "../components/MarkBank/deck";
import { connectStudyPlan } from "../services/studyPlanSync";
import { DEMO_STUDENT_UID } from "../data/devStudent";
import { resolveSubjectId } from "../curriculumRegistry";

/** Read-only bridge: the Mark Bank scheduler retains ownership of every card date. */
export function currentCardNeeds(uid: string, profile: StudentSubjectProfile) {
  const now = Date.now();
  const result: PlanInputs["cards"] = [];
  if (
    profile.curriculumLevel === "junior" ||
    profile.yearGroup === "LCA1" ||
    profile.yearGroup === "LCA2"
  )
    return result;
  for (const subject of profile.subjects) {
    const id = resolveSubjectId(subject.subjectName);
    if (!id) continue;
    const levels = levelsFor(id);
    const level = levels.includes(subject.level as (typeof levels)[number])
      ? subject.level
      : levels.includes("common")
        ? "common"
        : subject.level;
    const deck = readLocal(uid, `${id}-${level}`);
    const retention = retentionFor(now, deck.examTs);
    const groups = new Map<string, string[]>();
    for (const cardId of new Set(
      Object.keys(deck.cards).map((id) => CARD_ID_ALIASES[id] ?? id),
    )) {
      const memory = memoryFor(deck, cardId);
      if (!memory.last) continue;
      const due = dateKey(new Date(dueAt(cardId, memory, retention)));
      const list = groups.get(due) ?? [];
      list.push(cardId);
      groups.set(due, list);
    }
    for (const [dueOn, cardIds] of groups)
      for (let i = 0; i < cardIds.length; i += 10) {
        const batch = cardIds.sort().slice(i, i + 10);
        result.push({
          id: `${id}-${level}-${dueOn}-${i}`,
          subjectName: subject.subjectName,
          dueOn,
          cardIds: batch,
          minutes: Math.max(10, batch.length * 3),
        });
      }
  }
  return result;
}
/** Every screen reads the same account-scoped plan; changes also sync to Firestore. */
export function useDatedStudyPlan(
  profile?: StudentSubjectProfile | null,
  uid?: string,
  weekOffset = 0,
) {
  const progress = useOptionalProgress();
  const { user } = useAuth();
  const base = progress?.studentProfile ?? profile;
  const effective = base
    ? {
        ...base,
        yearGroup: base.yearGroup ?? user?.yearGroup,
        curriculumLevel: base.curriculumLevel ?? user?.curriculumLevel,
      }
    : base;
  const scope = uid ?? progress?.progressDataUid ?? "guest";
  const saved = useSyncExternalStore(
    subscribeStudyPlan,
    () => readStudyPlan(scope),
    () => undefined,
  );
  const today = useLocalDateKey();
  const start = mondayOf(today);
  const [cardRevision, setCardRevision] = useState(0);
  useEffect(() => {
    const refresh = () => setCardRevision((n) => n + 1);
    window.addEventListener("nsu:mark-bank-review", refresh);
    return () => window.removeEventListener("nsu:mark-bank-review", refresh);
  }, []);
  const enabled = !!effective;
  useEffect(() => {
    if (
      !enabled ||
      !user?.uid ||
      user.uid !== scope ||
      scope === DEMO_STUDENT_UID
    )
      return;
    return connectStudyPlan(scope);
  }, [scope, enabled, user?.uid]);
  const profileKey = JSON.stringify(effective);
  useEffect(() => {
    if (
      !effective ||
      !user?.uid ||
      user.uid !== scope ||
      scope === DEMO_STUDENT_UID ||
      effective.curriculumLevel === "junior" ||
      effective.yearGroup?.startsWith("LCA")
    )
      return;
    let cancelled = false;
    const refresh = () => {
      void Promise.all(
        effective.subjects.map(async (subject) => {
          const id = resolveSubjectId(subject.subjectName);
          if (!id) return;
          const levels = levelsFor(id);
          const level = levels.includes(
            subject.level as (typeof levels)[number],
          )
            ? subject.level
            : levels.includes("common")
              ? "common"
              : subject.level;
          const deckId = `${id}-${level}`;
          const remote = await fetchDeck(scope, deckId);
          if (cancelled || !remote) return;
          writeLocal(
            scope,
            deckId,
            mergeDecks(readLocal(scope, deckId), remote),
          );
        }),
      ).then(() => {
        if (!cancelled) setCardRevision((n) => n + 1);
      });
    };
    refresh();
    window.addEventListener("focus", refresh);
    return () => {
      cancelled = true;
      window.removeEventListener("focus", refresh);
    };
  }, [scope, profileKey, user?.uid]);
  const mastery = progress?.topicMasteryV2;
  const masteryKey = JSON.stringify(mastery);
  const completions = progress?.timetableCompletions ?? {};
  const completionKey = JSON.stringify(completions);
  const sessions = progress?.studySessions ?? [];
  const sessionKey = JSON.stringify(
    sessions.map((s) => [s.subject, s.date, s.actualSeconds]),
  );
  useEffect(() => {
    if (!effective || !enabled) return;
    const existing = readStudyPlan(scope);
    const evidence: TopicEvidence[] = Object.values(mastery?.topics ?? {}).map(
      (e) => ({
        specificationId: e.specificationId,
        topicId: e.topicId,
        subjectName: e.subjectName,
        topicName: e.topicName,
        taught: e.confidence !== "not-started",
        confidence: e.confidence,
      }),
    );
    const merged = new Map(
      evidence.map((e) => [`${e.specificationId}::${e.topicId}`, e]),
    );
    for (const e of existing?.inputs.evidence ?? []) {
      const key = `${e.specificationId}::${e.topicId}`;
      const latest = merged.get(key);
      merged.set(key, {
        ...e,
        ...(latest
          ? { confidence: latest.confidence, taught: latest.taught }
          : {}),
      });
    }
    const settings =
      existing?.inputs.settings ?? initialPlanSettings(effective);
    const lastContact = { ...(existing?.inputs.lastContact ?? {}) };
    for (const session of sessions)
      if (
        session.actualSeconds > 0 &&
        (!lastContact[session.subject] ||
          session.date > lastContact[session.subject])
      )
        lastContact[session.subject] = session.date;
    const inputs: PlanInputs = {
      profile: effective,
      settings,
      evidence: [...merged.values()],
      cards: currentCardNeeds(scope, effective),
      deadlines: existing?.inputs.deadlines ?? [],
      requirements: existing?.inputs.requirements ?? [],
      lastContact,
    };
    const previous = preserveLegacyCompletions(
      inputs,
      start,
      completions,
      existing?.plan,
    );
    if (
      !existing ||
      existing.plan.start !== start ||
      previous !== existing.plan ||
      JSON.stringify(existing.inputs) !== JSON.stringify(inputs)
    )
      saveStudyPlan(
        scope,
        inputs,
        buildStudyPlan(inputs, start, previous, today),
      );
    // Serialised inputs prevent unrelated progress rerenders from regenerating a plan.
  }, [
    scope,
    enabled,
    profileKey,
    masteryKey,
    start,
    today,
    cardRevision,
    completionKey,
    sessionKey,
  ]);
  const timetable = useMemo(
    () => (saved ? planTimetable(saved.plan, weekOffset) : undefined),
    [saved, weekOffset],
  );
  return { scope, saved, timetable, enabled, today };
}
