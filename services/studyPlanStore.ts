import {
  addDays,
  buildStudyPlan,
  dateKey,
  recordRetrieval,
  type PlanInputs,
  type PlanTask,
  type StudyPlan,
  type TopicEvidence,
} from "./studyPlanEngine";

export interface SavedStudyPlan {
  version: 1;
  inputs: PlanInputs;
  plan: StudyPlan;
  saved: boolean;
  error?: string;
  sync?: "loading" | "saving" | "synced" | "offline" | "error";
}
const cache = new Map<string, SavedStudyPlan>();
const listeners = new Set<() => void>();
export const planStorageKey = (scope: string) => `nsu:dated-plan:v1:${scope}`;
export const subscribeStudyPlan = (fn: () => void) => {
  listeners.add(fn);
  return () => {
    listeners.delete(fn);
  };
};
export function readStudyPlan(scope: string): SavedStudyPlan | undefined {
  if (cache.has(scope)) return cache.get(scope);
  try {
    const raw = localStorage.getItem(planStorageKey(scope));
    if (raw) {
      const data = JSON.parse(raw);
      if (
        data.version === 1 &&
        data.plan?.version === 1 &&
        Array.isArray(data.plan.tasks) &&
        Array.isArray(data.inputs?.profile?.subjects) &&
        Array.isArray(data.inputs?.settings?.days) &&
        data.inputs.settings.days.length === 7
      ) {
        cache.set(scope, data);
        return data;
      }
    }
  } catch {
    /* No usable saved plan; show an explicit save status after the next write. */
  }
  return undefined;
}
export function saveStudyPlan(
  scope: string,
  inputs: PlanInputs,
  plan: StudyPlan,
): SavedStudyPlan {
  let value: SavedStudyPlan = {
    version: 1,
    inputs,
    plan,
    saved: true,
    sync: cache.get(scope)?.sync,
  };
  try {
    localStorage.setItem(planStorageKey(scope), JSON.stringify(value));
  } catch {
    value = {
      ...value,
      saved: false,
      error:
        "This plan could not be saved on this device. Keep this tab open until account saving is confirmed.",
    };
  }
  cache.set(scope, value);
  listeners.forEach((fn) => fn());
  return value;
}
export function createStudyPlan(
  scope: string,
  inputs: PlanInputs,
  start: string,
  today = start,
  reset = false,
): SavedStudyPlan {
  const previous = reset ? undefined : readStudyPlan(scope)?.plan;
  return saveStudyPlan(
    scope,
    inputs,
    buildStudyPlan(inputs, start, previous, today),
  );
}
export function updateStudyPlan(
  scope: string,
  update: (value: SavedStudyPlan) => SavedStudyPlan,
): void {
  const current = readStudyPlan(scope);
  if (!current) return;
  const next = update(current);
  saveStudyPlan(scope, next.inputs, next.plan);
}
export function setTaskStatus(
  scope: string,
  id: string,
  status: PlanTask["status"],
): void {
  updateStudyPlan(scope, (value) => {
    const source = value.plan.tasks.find((t) => t.id === id)?.sourceId;
    const tasks = value.plan.tasks.map((t) =>
      t.id === id
        ? { ...t, status, locked: true }
        : status === "dropped" &&
            t.afterSourceId === source &&
            t.status === "planned"
          ? { ...t, status: "dropped" as const, locked: true }
          : t,
    );
    return {
      ...value,
      plan: {
        ...value.plan,
        tasks,
        days: value.plan.days.map((d) => ({
          ...d,
          planned: tasks
            .filter((t) => t.date === d.date && t.status !== "dropped")
            .reduce((sum, t) => sum + t.durationMinutes, 0),
        })),
      },
    };
  });
}
export function movePlanTask(
  scope: string,
  id: string,
  date: string,
  duration?: number,
): string | undefined {
  const value = readStudyPlan(scope);
  if (!value) return "Plan unavailable.";
  const task = value.plan.tasks.find((t) => t.id === id);
  const day = value.plan.days.find((d) => d.date === date);
  if (!task || !day) return "Choose a date in this fortnight.";
  if (task.status === "completed")
    return "A completed session stays on the date it happened.";
  const requested = duration ?? task.durationMinutes;
  const predecessor = task.afterSourceId
    ? value.plan.tasks.find(
        (t) => t.sourceId === task.afterSourceId && t.status !== "dropped",
      )
    : undefined;
  if (
    task.afterSourceId &&
    (!predecessor || date < addDays(predecessor.date, 3))
  )
    return "Keep this check at least three days after its practice session, or move the practice first.";
  const dependent = value.plan.tasks.find(
    (t) =>
      t.afterSourceId === task.sourceId &&
      t.status !== "dropped" &&
      t.date < addDays(date, 3),
  );
  if (dependent)
    return "Move the delayed check later first, so it stays at least three days after this practice.";
  if (
    (task.kind === "cards" || task.kind === "deadline") &&
    requested !== task.durationMinutes
  )
    return "This task needs its full planned time. Change the scope in your settings instead.";
  if (
    !Number.isFinite(requested) ||
    requested < 10 ||
    requested > task.durationMinutes
  )
    return "Choose between 10 minutes and the original task length.";
  if (date < task.earliest)
    return `This review is not due before ${task.earliest}.`;
  if (task.deadline && date >= task.deadline)
    return `This task needs room before ${task.deadline}.`;
  const others = value.plan.tasks.filter(
    (t) => t.id !== id && t.status !== "dropped",
  );
  if (
    others
      .filter((t) => t.date === date)
      .reduce((n, t) => n + t.durationMinutes, 0) +
      requested >
    day.capacity
  )
    return "That day does not have enough available minutes.";
  const week = Math.floor(value.plan.days.indexOf(day) / 7);
  const dates = new Set(
    value.plan.days.slice(week * 7, week * 7 + 7).map((d) => d.date),
  );
  if (
    others
      .filter((t) => dates.has(t.date))
      .reduce((n, t) => n + t.durationMinutes, 0) +
      requested >
    value.inputs.settings.revisionMinutes
  )
    return "That move exceeds the agreed weekly revision commitment.";
  if (
    task.topicKey &&
    others.some((t) => t.topicKey === task.topicKey && t.date === date)
  )
    return "Choose a separate day for this topic’s retrieval.";
  updateStudyPlan(scope, (v) => ({
    ...v,
    plan: {
      ...v.plan,
      tasks: v.plan.tasks.map((t) =>
        t.id === id
          ? {
              ...t,
              date,
              durationMinutes: requested,
              locked: true,
              status: "planned",
            }
          : t,
      ),
      days: v.plan.days.map((d) => ({
        ...d,
        planned:
          v.plan.tasks
            .filter(
              (t) => t.id !== id && t.date === d.date && t.status !== "dropped",
            )
            .reduce((sum, t) => sum + t.durationMinutes, 0) +
          (d.date === date ? requested : 0),
      })),
    },
  }));
  return undefined;
}
export function saveRetrievalResult(
  scope: string,
  taskId: string,
  result: NonNullable<TopicEvidence["result"]>,
  on = dateKey(new Date()),
): void {
  const value = readStudyPlan(scope);
  const task = value?.plan.tasks.find((t) => t.id === taskId);
  if (!value || !task?.topicKey || task.kind === "cards") return;
  const inputs = {
    ...value.inputs,
    evidence: value.inputs.evidence.map((e) =>
      `${e.specificationId}::${e.topicId}` === task.topicKey
        ? recordRetrieval(e, result, on, value.inputs.profile.examStartDate)
        : e,
    ),
  };
  const previous = {
    ...value.plan,
    tasks: value.plan.tasks.map((t) =>
      t.id === taskId ? { ...t, status: "completed" as const } : t,
    ),
  };
  saveStudyPlan(
    scope,
    inputs,
    buildStudyPlan(inputs, previous.start, previous, on),
  );
}
if (typeof window !== "undefined")
  window.addEventListener("storage", (event) => {
    if (event.key === null) {
      cache.clear();
      listeners.forEach((fn) => fn());
    }
    if (event.key?.startsWith("nsu:dated-plan:v1:")) {
      cache.delete(event.key.slice("nsu:dated-plan:v1:".length));
      listeners.forEach((fn) => fn());
    }
  });

export function setPlanSyncState(
  scope: string,
  sync: SavedStudyPlan["sync"],
): void {
  const current = readStudyPlan(scope);
  if (!current || current.sync === sync) return;
  cache.set(scope, { ...current, sync });
  listeners.forEach((fn) => fn());
}
if (typeof window !== "undefined")
  window.addEventListener("nextstepuni:session-cleared", () => {
    for (const scope of cache.keys())
      try {
        localStorage.removeItem(planStorageKey(scope));
      } catch {
        /* Memory is cleared too. */
      }
    cache.clear();
    listeners.forEach((fn) => fn());
  });
