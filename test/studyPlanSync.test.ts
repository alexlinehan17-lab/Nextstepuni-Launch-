import type * as FirestoreModule from "firebase/firestore";
import { afterEach, beforeEach, expect, test, vi } from "vitest";
import {
  createStudyPlan,
  readStudyPlan,
  setTaskStatus,
} from "../services/studyPlanStore";
import {
  connectStudyPlan,
  planCloudPatch,
  mergeCloudPlan,
  cloudKey,
  type PlanCloudData,
} from "../services/studyPlanSync";
import { studyPlannerSample, SAMPLE_START } from "../data/studyPlannerSamples";

type Snapshot = {
  exists: () => boolean;
  data: () => PlanCloudData | undefined;
  metadata: { fromCache: boolean; hasPendingWrites: boolean };
};
const transport = vi.hoisted(() => ({
  next: undefined as undefined | ((snap: Snapshot) => void),
  error: undefined as undefined | (() => void),
  stop: vi.fn(),
  write: vi.fn<(...args: unknown[]) => Promise<void>>(() => Promise.resolve()),
}));
vi.mock("firebase/firestore", async (importOriginal) => ({
  ...(await importOriginal<typeof FirestoreModule>()),
  doc: (_db: unknown, ...parts: string[]) => parts.join("/"),
  setDoc: (...args: unknown[]) => transport.write(...args),
  onSnapshot: (
    _ref: unknown,
    _options: unknown,
    next: (snap: Snapshot) => void,
    error: () => void,
  ) => {
    transport.next = next;
    transport.error = error;
    return transport.stop;
  },
}));
let disconnect: (() => void) | undefined;
beforeEach(() => {
  vi.clearAllMocks();
  vi.useFakeTimers();
  vi.setSystemTime(new Date(`${SAMPLE_START}T12:00:00Z`));
  transport.write.mockImplementation(() => Promise.resolve());
});
afterEach(() => {
  disconnect?.();
  disconnect = undefined;
  vi.useRealTimers();
});
const emit = (data?: PlanCloudData, fromCache = false) =>
  transport.next!({
    exists: () => !!data,
    data: () => data,
    metadata: { fromCache, hasPendingWrites: false },
  });
const settle = async () => {
  await Promise.resolve();
  await Promise.resolve();
};

test("quiz evidence survives account sync and an older not-started confidence record", () => {
  const input = studyPlannerSample("sixth");
  const topic = input.evidence.find(e => e.taught)!;
  topic.taught = false;
  topic.confidence = "not-started";
  const local = createStudyPlan("sync-quiz-evidence", input, SAMPLE_START, SAMPLE_START, true);
  const evidence = { ...topic, taught: true, result: "self-assessed" as const,
    observedOn: SAMPLE_START, dueOn: "2026-11-05", successfulReviews: 0,
    assessment: { source: "study-quiz" as const, sessionId: "quiz-a", recordedAt: Date.now(), questionCount: 1, marksClaimed: 6, marksAvailable: 6 },
  };
  const incoming = planCloudPatch(local, { ...local, inputs: { ...local.inputs, evidence: [evidence] } });
  const merged = mergeCloudPlan(local, incoming, SAMPLE_START);
  const synced = merged.inputs.evidence.find(e => e.topicId === topic.topicId)!;
  expect(synced).toMatchObject({ taught: true, confidence: "not-started", result: "self-assessed", successfulReviews: 0, assessment: evidence.assessment });
  expect(merged.plan.tasks.some(t => t.topicKey === `${topic.specificationId}::${topic.topicId}`)).toBe(true);
});

test("waits for account hydration, then patches only the task actually changed", async () => {
  const uid = "sync-owner",
    local = createStudyPlan(
      uid,
      studyPlannerSample("sixth"),
      SAMPLE_START,
      SAMPLE_START,
      true,
    );
  disconnect = connectStudyPlan(uid);
  emit(undefined, true);
  expect(transport.write).not.toHaveBeenCalled();
  emit(planCloudPatch(undefined, local));
  expect(transport.write).not.toHaveBeenCalled();
  setTaskStatus(uid, local.plan.tasks[0].id, "completed");
  expect(transport.write).toHaveBeenCalledTimes(1);
  const [path, patch, options] = transport.write.mock.calls[0] as unknown as [
    string,
    PlanCloudData,
    { mergeFields: unknown[] },
  ];
  expect(path).toBe(`progress/${uid}/studyPlans/current`);
  expect(Object.keys(patch.tasks ?? {})).toEqual([
    cloudKey(local.plan.tasks[0].id),
  ]);
  expect(options.mergeFields).toHaveLength(2);
  await settle();
  expect(readStudyPlan(uid)?.sync).toBe("synced");
});
test("a local edit made while account loading survives the first remote snapshot", async () => {
  const uid = "sync-loading",
    local = createStudyPlan(
      uid,
      studyPlannerSample("sixth"),
      SAMPLE_START,
      SAMPLE_START,
      true,
    );
  disconnect = connectStudyPlan(uid);
  setTaskStatus(uid, local.plan.tasks[0].id, "completed");
  expect(transport.write).not.toHaveBeenCalled();
  emit(planCloudPatch(undefined, local));
  expect(readStudyPlan(uid)?.plan.tasks[0].status).toBe("completed");
  expect(transport.write).toHaveBeenCalledTimes(1);
  await settle();
});
test("a rejected write remains visible and can be retried without losing the edit", async () => {
  const uid = "sync-retry",
    local = createStudyPlan(
      uid,
      studyPlannerSample("sixth"),
      SAMPLE_START,
      SAMPLE_START,
      true,
    );
  disconnect = connectStudyPlan(uid);
  emit(planCloudPatch(undefined, local));
  transport.write.mockRejectedValueOnce(
    new Error("offline permission failure"),
  );
  setTaskStatus(uid, local.plan.tasks[0].id, "completed");
  await settle();
  expect(readStudyPlan(uid)?.sync).toBe("error");
  window.dispatchEvent(new Event("nsu:retry-plan-save"));
  await settle();
  expect(transport.write).toHaveBeenCalledTimes(2);
  expect(readStudyPlan(uid)?.plan.tasks[0].status).toBe("completed");
  expect(readStudyPlan(uid)?.sync).toBe("synced");
});
test("two mounted consumers share one subscription and release it only after both leave", () => {
  const uid = "sync-shared";
  createStudyPlan(
    uid,
    studyPlannerSample("sixth"),
    SAMPLE_START,
    SAMPLE_START,
    true,
  );
  const first = connectStudyPlan(uid);
  disconnect = connectStudyPlan(uid);
  first();
  expect(transport.stop).not.toHaveBeenCalled();
  disconnect();
  disconnect = undefined;
  expect(transport.stop).toHaveBeenCalledTimes(1);
});

test("a save acknowledged after navigation clears its outbox without recreating logged-out data", async () => {
  const uid = "sync-unmount",
    local = createStudyPlan(
      uid,
      studyPlannerSample("sixth"),
      SAMPLE_START,
      SAMPLE_START,
      true,
    );
  disconnect = connectStudyPlan(uid);
  emit(planCloudPatch(undefined, local));
  let resolve!: () => void;
  transport.write.mockImplementationOnce(
    () =>
      new Promise<void>((done) => {
        resolve = done;
      }),
  );
  setTaskStatus(uid, local.plan.tasks[0].id, "completed");
  disconnect();
  disconnect = undefined;
  resolve();
  await settle();
  expect(
    JSON.parse(localStorage.getItem(`nsu:dated-plan-outbox:v1:${uid}`)!),
  ).toEqual({ version: 1 });
});
