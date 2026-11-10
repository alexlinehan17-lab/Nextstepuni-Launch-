import { preparePlannedStudy } from "../services/plannedStudyLaunch";
import { peekTopicStudy } from "../utils/topicLaunch";
import { readPlannerTodos } from "../components/launchpad/plannerTodos";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, expect, test } from "vitest";
import HomeNextStep from "../components/HomeNextStep";
import { studyPlannerSample, SAMPLE_START } from "../data/studyPlannerSamples";
import {
  addDays,
  buildStudyPlan,
  initialPlanSettings,
} from "../services/studyPlanEngine";
import {
  createStudyPlan,
  movePlanTask,
  readStudyPlan,
  setTaskStatus,
} from "../services/studyPlanStore";
import {
  acknowledgePatch,
  cloudKey,
  mergeCloudPatch,
  mergeCloudPlan,
  planCloudPatch,
} from "../services/studyPlanSync";

afterEach(cleanup);
test("Home recognises canonical completion IDs and out-of-order completed tasks", () => {
  const input = studyPlannerSample("sixth");
  const tasks = buildStudyPlan(input, SAMPLE_START).tasks.slice(0, 2);
  render(
    <HomeNextStep
      blocks={tasks}
      completions={[tasks[1].id]}
      hasProfile
      onProgress={() => {}}
    />,
  );
  expect(screen.getByText(/Done/)).toBeInTheDocument();
  expect(
    screen.getByRole("button", {
      name: new RegExp(`Review ${tasks[1].subjectName}:`),
    }),
  ).toBeInTheDocument();
});
test("Home sees an account-synced completion even before legacy progress reloads", () => {
  const task = {
    ...buildStudyPlan(studyPlannerSample("sixth"), SAMPLE_START).tasks[0],
    status: "completed" as const,
  };
  render(
    <HomeNextStep
      blocks={[task]}
      completions={[]}
      hasProfile
      onProgress={() => {}}
    />,
  );
  expect(
    screen.getByText(/Your planned sessions are done/),
  ).toBeInTheDocument();
});
test("availability is entered by students in every supported year, never inferred from grades", () => {
  for (const yearGroup of [
    "1st",
    "2nd",
    "3rd",
    "TY",
    "5th",
    "6th",
    "LCA1",
    "LCA2",
  ] as const) {
    const profile = { ...studyPlannerSample("sixth").profile, yearGroup };
    expect(
      initialPlanSettings(profile).days.every((d) => d.windowMinutes === 0),
    ).toBe(true);
    expect(initialPlanSettings(profile).revisionMinutes).toBe(0);
  }
});
test("a contact keeps its ID when next week becomes this week", () => {
  const input = studyPlannerSample("sixth");
  input.evidence = [];
  input.cards = [];
  input.deadlines = [];
  const first = buildStudyPlan(input, SAMPLE_START);
  const nextWeek = addDays(SAMPLE_START, 7);
  const task = first.tasks.find((t) => t.sourceId === `contact-${nextWeek}`)!;
  const second = buildStudyPlan(input, nextWeek);
  expect(second.tasks.some((t) => t.id === task.id)).toBe(true);
});
test("moving practice cannot put its delayed check before practice, and dropping practice drops its check", () => {
  const scope = "dependency-regression",
    input = studyPlannerSample("sixth");
  input.settings.days = input.settings.days.map(() => ({
    windowMinutes: 300,
    assignedMinutes: 0,
    breakMinutes: 0,
    bufferMinutes: 0,
  }));
  input.settings.revisionMinutes = 2000;
  const saved = createStudyPlan(scope, input, SAMPLE_START, SAMPLE_START, true);
  const check = saved.plan.tasks.find((t) => t.afterSourceId)!;
  expect(check).toBeDefined();
  const practice = saved.plan.tasks.find(
    (t) => t.sourceId === check.afterSourceId,
  )!;
  expect(movePlanTask(scope, practice.id, addDays(check.date, 1))).toMatch(
    /delayed check/,
  );
  setTaskStatus(scope, practice.id, "dropped");
  expect(
    readStudyPlan(scope)!.plan.tasks.find((t) => t.id === check.id)?.status,
  ).toBe("dropped");
});
test("different device task changes merge without losing a completion or manual move", () => {
  const local = createStudyPlan(
    "cloud-merge",
    studyPlannerSample("sixth"),
    SAMPLE_START,
    SAMPLE_START,
    true,
  );
  const [a, b] = local.plan.tasks;
  const remote = {
    version: 1 as const,
    tasks: { [cloudKey(a.id)]: { ...a, status: "completed" as const } },
  };
  const moved = { ...b, locked: true, date: addDays(b.date, 1) };
  const combined = mergeCloudPatch(remote, {
    version: 1,
    tasks: { [cloudKey(b.id)]: moved },
  });
  const merged = mergeCloudPlan(local, combined, SAMPLE_START);
  expect(merged.plan.tasks.find((t) => t.id === a.id)?.status).toBe(
    "completed",
  );
  expect(merged.plan.tasks.find((t) => t.id === b.id)?.date).toBe(moved.date);
});
test("no-op sync writes never send empty maps that erase cloud state", () => {
  expect(mergeCloudPatch({ version: 1 }, { version: 1 })).toEqual({
    version: 1,
  });
  const local = createStudyPlan(
    "cloud-noop",
    studyPlannerSample("sixth"),
    SAMPLE_START,
    SAMPLE_START,
    true,
  );
  expect(planCloudPatch(local, { ...local, sync: "synced" })).toEqual({
    version: 1,
  });
});
test("acknowledging an earlier write preserves a newer offline edit", () => {
  const local = createStudyPlan(
    "ack",
    studyPlannerSample("sixth"),
    SAMPLE_START,
    SAMPLE_START,
    true,
  );
  const t = local.plan.tasks[0],
    key = cloudKey(t.id);
  const sent = {
    version: 1 as const,
    tasks: { [key]: { ...t, status: "completed" as const } },
  };
  const queued = mergeCloudPatch(sent, {
    version: 1,
    tasks: { [key]: { ...t, status: "planned" as const, locked: true } },
  });
  expect(acknowledgePatch(queued, sent).tasks?.[key].status).toBe("planned");
});
test("signing out clears in-memory plans as well as local storage", () => {
  createStudyPlan(
    "session-clear",
    studyPlannerSample("sixth"),
    SAMPLE_START,
    SAMPLE_START,
    true,
  );
  window.dispatchEvent(new Event("nextstepuni:session-cleared"));
  expect(readStudyPlan("session-clear")).toBeUndefined();
});

test("starting a planned topic carries its identity and to-dos into the existing Study Room", () => {
  const uid = "launch-regression";
  const saved = createStudyPlan(
    uid,
    studyPlannerSample("sixth"),
    SAMPLE_START,
    SAMPLE_START,
    true,
  );
  const task =
    saved.plan.tasks.find((t) => t.topicKey?.includes("mathematics")) ??
    saved.plan.tasks.find((t) => t.topicKey)!;
  preparePlannedStudy(uid, task.id, task.date);
  expect(peekTopicStudy(uid)?.topicIds).toContain(
    task.topicKey!.split("::")[1],
  );
  expect(
    readPlannerTodos(uid, task.date, task.id)?.map((step) => step.label),
  ).toEqual(task.steps);
  expect(peekTopicStudy("another-account")).toBeUndefined();
});

test("a task removed by replanning cannot reappear as missed work on another device", () => {
  const before = createStudyPlan(
    "removed-remote",
    studyPlannerSample("sixth"),
    SAMPLE_START,
    SAMPLE_START,
    true,
  );
  const input = {
    ...before.inputs,
    settings: { ...before.inputs.settings, revisionMinutes: 0 },
  };
  const after = {
    ...before,
    inputs: input,
    plan: buildStudyPlan(input, SAMPLE_START, before.plan, SAMPLE_START),
  };
  const remote = mergeCloudPatch(
    planCloudPatch(undefined, before),
    planCloudPatch(before, after),
  );
  const reopened = mergeCloudPlan(before, remote, addDays(SAMPLE_START, 2));
  expect(reopened.plan.tasks).toHaveLength(0);
});

test("Junior Cycle uses the saved achievement bands without importing senior topics or CAO grades", () => {
  const inputs = studyPlannerSample("sixth");
  inputs.profile = {
    ...inputs.profile,
    yearGroup: "3rd",
    curriculumLevel: "junior",
    subjects: [
      {
        subjectName: "Mathematics",
        level: "higher",
        currentBand: "Partially Achieved",
        targetBand: "Distinction",
      },
    ],
  };
  const plan = buildStudyPlan(inputs, SAMPLE_START);
  expect(
    plan.tasks.some((t) => t.why.includes("Partially Achieved → Distinction")),
  ).toBe(true);
  expect(plan.tasks.some((t) => t.topicKey)).toBe(false);
});
