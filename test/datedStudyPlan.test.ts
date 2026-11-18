import { describe, it, expect } from "vitest";
import { studyPlannerSample, SAMPLE_START } from "../data/studyPlannerSamples";
import {
  addDays,
  buildStudyPlan,
  dayDistance,
  recordRetrieval,
  planTimetable,
} from "../services/studyPlanEngine";
import {
  createStudyPlan,
  readStudyPlan,
  movePlanTask,
  setTaskStatus,
  saveRetrievalResult,
  planStorageKey,
} from "../services/studyPlanStore";
import { getBlockId } from "../components/subjectData";

describe("dated study capacity", () => {
  for (const available of [0, 1, 2, 3, 4, 5, 6, 7])
    it(`respects exactly ${available} available days, including zero`, () => {
      const input = studyPlannerSample("sixth");
      input.settings.days = input.settings.days.map((_, i) => ({
        windowMinutes: i < available ? 67 : 0,
        breakMinutes: 7,
        assignedMinutes: 20,
        bufferMinutes: 5,
      }));
      const plan = buildStudyPlan(input, SAMPLE_START);
      for (const day of plan.days) {
        const used = plan.tasks
          .filter((t) => t.date === day.date)
          .reduce((n, t) => n + t.durationMinutes, 0);
        expect(used).toBeLessThanOrEqual(Math.max(0, day.windowMinutes - 32));
      }
      if (!available) {
        expect(plan.tasks).toHaveLength(0);
        expect(plan.unscheduled.length).toBeGreaterThan(0);
      }
    });
  for (const duration of [25, 45, 90])
    it(`${duration}-minute preference cannot inflate either ceiling`, () => {
      const input = studyPlannerSample("fifth");
      input.settings.preferredMinutes = duration;
      input.settings.revisionMinutes = 110;
      const plan = buildStudyPlan(input, SAMPLE_START);
      for (let w = 0; w < 2; w++) {
        const keys = new Set(
          plan.days.slice(w * 7, w * 7 + 7).map((d) => d.date),
        );
        expect(
          plan.tasks
            .filter((t) => keys.has(t.date))
            .reduce((n, t) => n + t.durationMinutes, 0),
        ).toBeLessThanOrEqual(110);
      }
      expect(plan.days.slice(0, 7).reduce((n, d) => n + d.capacity, 0)).toBe(
        300,
      );
    });
  it("excludes breaks, assigned work, buffer and date exceptions exactly once", () => {
    const input = studyPlannerSample("sixth");
    input.settings.exceptions[SAMPLE_START] = {
      windowMinutes: 100,
      breakMinutes: 10,
      assignedMinutes: 60,
      bufferMinutes: 15,
    };
    const plan = buildStudyPlan(input, SAMPLE_START);
    expect(plan.days[0].capacity).toBe(15);
    expect(plan.days[0].planned).toBeLessThanOrEqual(15);
    input.settings.exceptions[SAMPLE_START].assignedMinutes = 200;
    const overloaded = buildStudyPlan(input, SAMPLE_START);
    expect(overloaded.days[0].capacity).toBe(0);
    expect(overloaded.days[0].overload).toBe(125);
  });
  it("synthetic fixtures have different user budgets without prescribing hours from exam proximity", () => {
    const fifth = studyPlannerSample("fifth"),
      sixth = studyPlannerSample("sixth");
    sixth.profile.examStartDate = fifth.profile.examStartDate;
    expect(fifth.settings.revisionMinutes).toBe(300);
    expect(sixth.settings.revisionMinutes).toBe(480);
  });
});
describe("evidence, dates and coverage", () => {
  it("does not schedule a successful future review early", () => {
    const input = studyPlannerSample("sixth");
    const e = input.evidence.find((e) => e.subjectName === "English")!;
    const plan = buildStudyPlan(input, SAMPLE_START);
    const tasks = plan.tasks.filter(
      (t) => t.topicKey === `${e.specificationId}::${e.topicId}`,
    );
    expect(tasks.length).toBeGreaterThan(0);
    expect(tasks.every((t) => t.date >= e.dueOn!)).toBe(true);
    e.dueOn = "2027-01-01";
    expect(
      buildStudyPlan(input, SAMPLE_START).tasks.some(
        (t) => t.topicKey === `${e.specificationId}::${e.topicId}`,
      ),
    ).toBe(false);
  });
  it("does not treat untaught or mismatched curriculum topics as gaps", () => {
    const input = studyPlannerSample("sixth");
    const untaught = input.evidence.find((e) => !e.taught)!;
    input.evidence[0].specificationId = "wrong-cohort";
    const plan = buildStudyPlan(input, SAMPLE_START);
    expect(
      plan.tasks.some(
        (t) =>
          t.topicKey === `${untaught.specificationId}::${untaught.topicId}`,
      ),
    ).toBe(false);
    expect(plan.tasks.some((t) => t.topicKey?.startsWith("wrong-cohort"))).toBe(
      false,
    );
    expect(plan.notices.join(" ")).toContain("curriculum matching");
  });
  it("protects required Irish, rotates coverage, and discloses omissions", () => {
    const input = studyPlannerSample("sixth");
    const plan = buildStudyPlan(input, SAMPLE_START);
    expect(
      plan.tasks.some(
        (t) => t.subjectName === "Irish" && t.why.includes("requirement"),
      ),
    ).toBe(true);
    for (const s of input.profile.subjects)
      expect(plan.tasks.some((t) => t.subjectName === s.subjectName)).toBe(
        true,
      );
    input.settings.revisionMinutes = 15;
    const tiny = buildStudyPlan(input, SAMPLE_START);
    expect(tiny.unscheduled.length).toBeGreaterThan(0);
    expect(tiny.notices.join(" ")).toContain("No contact fits");
  });
  it("puts deadlines before their date or explicitly leaves them unscheduled", () => {
    const input = studyPlannerSample("three");
    const plan = buildStudyPlan(input, SAMPLE_START);
    const task = plan.tasks.find((t) => t.kind === "deadline");
    expect(task).toBeDefined();
    expect(task!.date < input.deadlines[0].dueOn).toBe(true);
    input.settings.revisionMinutes = 0;
    expect(
      buildStudyPlan(input, SAMPLE_START).unscheduled.some(
        (t) => t.title.includes("algebra") && t.reason.includes("before"),
      ),
    ).toBe(true);
  });
  it("keeps repeat retrieval on separate calendar dates, including DST", () => {
    const plan = buildStudyPlan(studyPlannerSample("sixth"), SAMPLE_START);
    const seen = new Set();
    for (const task of plan.tasks.filter((t) => t.topicKey)) {
      const key = `${task.topicKey}:${task.date}`;
      expect(seen.has(key)).toBe(false);
      seen.add(key);
    }
    expect(addDays("2026-10-24", 2)).toBe("2026-10-26");
    expect(dayDistance("2026-10-24", "2026-10-26")).toBe(2);
    expect(addDays("2027-03-27", 2)).toBe("2027-03-29");
  });
  it("a failed retrieval brings a previously successful topic forward without touching confidence", () => {
    const e = studyPlannerSample("sixth").evidence.find(
      (e) => e.result === "independent",
    )!;
    const failed = recordRetrieval(e, "failed", SAMPLE_START);
    expect(failed.dueOn).toBe("2026-11-03");
    expect(failed.successfulReviews).toBe(0);
    expect(failed.confidence).toBe("solid");
  });
  it("all subjects at target and missing grades still get honest coverage", () => {
    const input = studyPlannerSample("sixth");
    input.profile.subjects = input.profile.subjects.map((s) => ({
      ...s,
      currentGrade: s.targetGrade,
    }));
    input.evidence = [];
    expect(
      new Set(
        buildStudyPlan(input, SAMPLE_START).tasks.map((t) => t.subjectName),
      ).size,
    ).toBe(7);
    input.profile.subjects = input.profile.subjects.map((s) => ({
      ...s,
      currentGrade: undefined,
      targetGrade: undefined,
    }));
    expect(buildStudyPlan(input, SAMPLE_START).tasks.length).toBeGreaterThan(0);
  });
});
describe("a single persisted plan", () => {
  it("keeps completion IDs and manual edits on regeneration, including capacity reduction", () => {
    const scope = "test-preservation";
    const input = studyPlannerSample("sixth");
    const saved = createStudyPlan(
      scope,
      input,
      SAMPLE_START,
      SAMPLE_START,
      true,
    );
    const task = saved.plan.tasks[0];
    setTaskStatus(scope, task.id, "completed");
    input.settings.revisionMinutes = 0;
    const next = createStudyPlan(scope, input, SAMPLE_START);
    expect(next.plan.tasks.find((t) => t.id === task.id)?.status).toBe(
      "completed",
    );
    expect(next.plan.tasks.find((t) => t.id === task.id)?.date).toBe(task.date);
    expect(
      JSON.parse(localStorage.getItem(planStorageKey(scope))!).plan.tasks.some(
        (t: { id: string }) => t.id === task.id,
      ),
    ).toBe(true);
  });
  it("never resurrects deliberately dropped tasks", () => {
    const scope = "test-drop",
      input = studyPlannerSample("sixth");
    const saved = createStudyPlan(
      scope,
      input,
      SAMPLE_START,
      SAMPLE_START,
      true,
    );
    const task = saved.plan.tasks[0];
    setTaskStatus(scope, task.id, "dropped");
    const next = createStudyPlan(scope, input, SAMPLE_START);
    expect(next.plan.tasks.filter((t) => t.id === task.id)).toHaveLength(1);
    expect(next.plan.tasks.find((t) => t.id === task.id)?.status).toBe(
      "dropped",
    );
  });
  it("all consumers use the persisted identity regardless of array order", () => {
    const scope = "test-identity";
    createStudyPlan(
      scope,
      studyPlannerSample("sixth"),
      SAMPLE_START,
      SAMPLE_START,
      true,
    );
    const plan = readStudyPlan(scope)!.plan;
    const block = planTimetable(plan).flatMap((d) => d.blocks)[0];
    expect(getBlockId(block, 0)).toBe(getBlockId(block, 8));
    expect(getBlockId(block, 0)).toBe(
      plan.tasks.find((t) => t.id === block.id)!.id,
    );
  });
  it("rejects a move into an unavailable day and preserves the original task", () => {
    const scope = "test-move";
    const saved = createStudyPlan(
      scope,
      studyPlannerSample("three"),
      SAMPLE_START,
      SAMPLE_START,
      true,
    );
    const task = saved.plan.tasks[0];
    expect(movePlanTask(scope, task.id, SAMPLE_START)).toBeDefined();
    expect(
      readStudyPlan(scope)!.plan.tasks.find((t) => t.id === task.id)?.date,
    ).toBe(task.date);
  });
  it("completion alone changes no review dates, but a recorded outcome does", () => {
    const scope = "test-outcome";
    const saved = createStudyPlan(
      scope,
      studyPlannerSample("sixth"),
      SAMPLE_START,
      SAMPLE_START,
      true,
    );
    const task = saved.plan.tasks.find((t) => t.topicKey)!;
    const before = JSON.stringify(saved.inputs.evidence);
    setTaskStatus(scope, task.id, "completed");
    expect(JSON.stringify(readStudyPlan(scope)!.inputs.evidence)).toBe(before);
    saveRetrievalResult(scope, task.id, "failed", task.date);
    expect(
      readStudyPlan(scope)!.inputs.evidence.find(
        (e) => `${e.specificationId}::${e.topicId}` === task.topicKey,
      )?.dueOn,
    ).toBe(addDays(task.date, 1));
  });
});
