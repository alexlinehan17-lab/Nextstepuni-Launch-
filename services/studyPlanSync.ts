/** Account persistence. Per-task/per-topic patches preserve unrelated device edits. */
import {
  doc,
  onSnapshot,
  setDoc,
  deleteField,
  FieldPath,
} from "firebase/firestore";
import { db } from "../firebase";
import {
  addDays,
  buildStudyPlan,
  dateKey,
  mondayOf,
  type PlanInputs,
  type PlanTask,
  type TopicEvidence,
} from "./studyPlanEngine";
import {
  readStudyPlan,
  saveStudyPlan,
  subscribeStudyPlan,
  setPlanSyncState,
  type SavedStudyPlan,
} from "./studyPlanStore";

export interface PlanCloudData {
  version: 1;
  settings?: PlanInputs["settings"];
  requirements?: PlanInputs["requirements"];
  deadlines?: PlanInputs["deadlines"];
  evidence?: Record<string, TopicEvidence>;
  tasks?: Record<string, PlanTask & { removed?: boolean }>;
}
// A Firestore map key, not a path. Avoid dots and slash-containing curriculum IDs.
export const cloudKey = (id: string) =>
  Array.from(new TextEncoder().encode(id), (b) =>
    b.toString(16).padStart(2, "0"),
  ).join("");
const equal = (a: unknown, b: unknown) =>
  JSON.stringify(a) === JSON.stringify(b);
export function planCloudPatch(
  before: SavedStudyPlan | undefined,
  after: SavedStudyPlan,
): PlanCloudData {
  const patch: PlanCloudData = { version: 1 };
  for (const key of ["settings", "requirements", "deadlines"] as const) {
    if (!equal(before?.inputs[key], after.inputs[key]))
      Object.assign(patch, { [key]: after.inputs[key] });
  }
  for (const evidence of after.inputs.evidence) {
    // Confidence/taught status belongs to ProgressContext, not a second cloud owner.
    if (!evidence.result) continue;
    const id = `${evidence.specificationId}::${evidence.topicId}`;
    const previous = before?.inputs.evidence.find(
      (e) => `${e.specificationId}::${e.topicId}` === id,
    );
    if (!equal(previous, evidence))
      (patch.evidence ??= {})[cloudKey(id)] = evidence;
  }
  for (const task of after.plan.tasks) {
    const previous = before?.plan.tasks.find((t) => t.id === task.id);
    if (!equal(previous, task)) (patch.tasks ??= {})[cloudKey(task.id)] = task;
  }
  for (const task of before?.plan.tasks ?? []) {
    if (!after.plan.tasks.some((t) => t.id === task.id))
      (patch.tasks ??= {})[cloudKey(task.id)] = { ...task, removed: true };
  }
  return patch;
}
export function mergeCloudPlan(
  local: SavedStudyPlan,
  remote: PlanCloudData,
  today: string,
): SavedStudyPlan {
  const evidence = new Map(
    local.inputs.evidence.map((e) => [`${e.specificationId}::${e.topicId}`, e]),
  );
  for (const e of Object.values(remote.evidence ?? {})) {
    const key = `${e.specificationId}::${e.topicId}`;
    const current = evidence.get(key);
    evidence.set(key, {
      ...e,
      ...(current
        ? { taught: current.taught, confidence: current.confidence }
        : {}),
    });
  }
  const inputs: PlanInputs = {
    ...local.inputs,
    settings: remote.settings ?? local.inputs.settings,
    requirements: remote.requirements ?? local.inputs.requirements,
    deadlines: remote.deadlines ?? local.inputs.deadlines,
    evidence: [...evidence.values()],
  };
  const tasks = new Map(local.plan.tasks.map((t) => [t.id, t]));
  for (const task of Object.values(remote.tasks ?? {})) {
    if (task.removed) tasks.delete(task.id);
    else tasks.set(task.id, task);
  }
  const plan = buildStudyPlan(
    inputs,
    mondayOf(today),
    { ...local.plan, tasks: [...tasks.values()] },
    today,
  );
  return { ...local, inputs, plan };
}

export function mergeCloudPatch(
  base: PlanCloudData,
  patch: PlanCloudData,
): PlanCloudData {
  const merged = { ...base, ...patch };
  if (base.evidence || patch.evidence)
    merged.evidence = { ...base.evidence, ...patch.evidence };
  if (base.tasks || patch.tasks)
    merged.tasks = { ...base.tasks, ...patch.tasks };
  return merged;
}
const outboxKey = (uid: string) => `nsu:dated-plan-outbox:v1:${uid}`;
const readOutbox = (uid: string): PlanCloudData => {
  try {
    return JSON.parse(localStorage.getItem(outboxKey(uid)) ?? '{"version":1}');
  } catch {
    return { version: 1 };
  }
};
const saveOutbox = (uid: string, value: PlanCloudData) => {
  try {
    localStorage.setItem(outboxKey(uid), JSON.stringify(value));
  } catch {
    /* The plan store already reports local storage failures. */
  }
};
export function acknowledgePatch(
  queued: PlanCloudData,
  sent: PlanCloudData,
): PlanCloudData {
  const next = { ...queued };
  for (const key of ["settings", "requirements", "deadlines"] as const)
    if (equal(next[key], sent[key])) delete next[key];
  for (const key of ["evidence", "tasks"] as const) {
    const remaining = { ...next[key] };
    for (const [id, value] of Object.entries(sent[key] ?? {}))
      if (equal(remaining[id], value)) delete remaining[id];
    if (Object.keys(remaining).length)
      Object.assign(next, { [key]: remaining });
    else delete next[key];
  }
  return next;
}
const connections = new Map<string, { count: number; stop: () => void }>();
/** One live listener per account across Home, Planner, Progress and the study room. */
export function connectStudyPlan(uid: string): () => void {
  const existing = connections.get(uid);
  if (existing) {
    existing.count++;
    return () => release(uid);
  }
  const ref = doc(db, "progress", uid, "studyPlans", "current");
  let applying = false;
  let hydrated = false;
  let stopped = false;
  let pending = 0;
  let baseline = readStudyPlan(uid);
  let outbox = readOutbox(uid);
  const write = (patch: PlanCloudData) => {
    if (Object.keys(patch).length <= 1) return;
    outbox = mergeCloudPatch(outbox, patch);
    saveOutbox(uid, outbox);
    pending++;
    setPlanSyncState(uid, "saving");
    // Strip undefined optional fields. Firestore queues the merge offline.
    const fields = [
      new FieldPath("version"),
      ...(["settings", "requirements", "deadlines"] as const)
        .filter((key) => key in patch)
        .map((key) => new FieldPath(key)),
      ...(["tasks", "evidence"] as const).flatMap((key) =>
        Object.keys(patch[key] ?? {}).map((id) => new FieldPath(key, id)),
      ),
    ];
    void setDoc(ref, JSON.parse(JSON.stringify(patch)), { mergeFields: fields })
      .then(() => {
        pending--;
        // Acknowledgements still clear the durable outbox after navigating away.
        // A logout removes the key; never recreate it for a signed-out account.
        outbox = acknowledgePatch(readOutbox(uid), patch);
        try {
          if (localStorage.getItem(outboxKey(uid)) !== null)
            saveOutbox(uid, outbox);
        } catch {
          /* Device storage may be unavailable. */
        }
        if (!stopped && pending === 0) setPlanSyncState(uid, "synced");
      })
      .catch(() => {
        pending--;
        if (!stopped) setPlanSyncState(uid, "error");
      });
  };
  const unsubscribeStore = subscribeStudyPlan(() => {
    if (applying || stopped) return;
    const next = readStudyPlan(uid);
    if (!next || next === baseline) return;
    if (!baseline) {
      baseline = next;
      return;
    }
    const patch = planCloudPatch(baseline, next);
    baseline = next;
    if (!hydrated) {
      outbox = mergeCloudPatch(outbox, patch);
      saveOutbox(uid, outbox);
      return;
    }
    write(patch);
  });
  setPlanSyncState(uid, "loading");
  const unsubscribeRemote = onSnapshot(
    ref,
    { includeMetadataChanges: true },
    (snapshot) => {
      if (stopped) return;
      const local = readStudyPlan(uid);
      if (!local) return;
      const remote = snapshot.exists()
        ? (snapshot.data() as PlanCloudData)
        : undefined;
      // A cache miss is not proof that the account has no plan. Wait for server
      // before uploading defaults, and keep local edits queued in Firestore offline.
      if (!remote && snapshot.metadata.fromCache) return;
      if (remote && remote.version !== 1) {
        setPlanSyncState(uid, "error");
        return;
      }
      applying = true;
      if (remote) {
        // Never replace a pending local mutation with a cache/server echo. Once
        // acknowledged, the next snapshot contains the merged account state.
        if (!snapshot.metadata.hasPendingWrites) {
          const merged = mergeCloudPlan(
            local,
            mergeCloudPatch(remote, outbox),
            dateKey(new Date()),
          );
          saveStudyPlan(uid, merged.inputs, merged.plan);
        }
      }
      baseline = readStudyPlan(uid);
      const first = !hydrated;
      hydrated = true;
      applying = false;
      if (first && !remote && baseline)
        write(planCloudPatch(undefined, baseline));
      else if (first && Object.keys(outbox).length > 1) write(outbox);
      else
        setPlanSyncState(
          uid,
          snapshot.metadata.hasPendingWrites || pending
            ? "saving"
            : snapshot.metadata.fromCache
              ? "offline"
              : "synced",
        );
      // Bounded working history; actual completed sessions remain in /sessions
      // and timetableCompletions. Never delete a current task during housekeeping.
      if (
        remote &&
        !snapshot.metadata.fromCache &&
        !snapshot.metadata.hasPendingWrites
      ) {
        const cutoff = addDays(mondayOf(dateKey(new Date())), -28);
        const expired = Object.entries(remote.tasks ?? {}).filter(
          ([, task]) => task.date < cutoff,
        );
        if (expired.length)
          void setDoc(
            ref,
            {
              tasks: Object.fromEntries(
                expired.map(([key]) => [key, deleteField()]),
              ),
            },
            { merge: true },
          ).catch(() => setPlanSyncState(uid, "error"));
      }
    },
    () => {
      if (!stopped) setPlanSyncState(uid, "error");
    },
  );
  const retry = () => {
    if (!stopped && hydrated && pending === 0 && Object.keys(outbox).length > 1)
      write(outbox);
  };
  window.addEventListener("online", retry);
  window.addEventListener("nsu:retry-plan-save", retry);
  connections.set(uid, {
    count: 1,
    stop: () => {
      stopped = true;
      unsubscribeRemote();
      unsubscribeStore();
      window.removeEventListener("online", retry);
      window.removeEventListener("nsu:retry-plan-save", retry);
    },
  });
  return () => release(uid);
}
function release(uid: string) {
  const connection = connections.get(uid);
  if (connection && --connection.count === 0) {
    connection.stop();
    connections.delete(uid);
  }
}
if (typeof window !== "undefined")
  window.addEventListener("nextstepuni:session-cleared", () => {
    for (const connection of connections.values()) connection.stop();
    connections.clear();
  });
