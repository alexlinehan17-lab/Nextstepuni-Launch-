import { expect, test } from "vitest";
import { studyPlannerSample } from "../data/studyPlannerSamples";
import { DAYS_OF_WEEK } from "../components/subjectData";
import { addDays, buildStudyPlan, dayDistance, planTimetable, profilePlanSettings } from "../services/studyPlanEngine";

const start = "2026-11-09";
function inputFor(duration: number, restDays = ["Sunday"]) {
  const input = studyPlannerSample("sixth");
  input.profile = { ...input.profile, defaultBlockDuration: duration, restDays, examStartDate: "2027-06-07" };
  input.settings = profilePlanSettings(input.profile);
  input.evidence = []; input.cards = []; input.deadlines = []; input.requirements = []; input.lastContact = {};
  return input;
}

test("25-minute practice stays whole and repeats a balanced, spaced week without halving week two", () => {
  const input = inputFor(25);
  const plan = buildStudyPlan(input, start);
  for (const week of [0, 1]) {
    const days = planTimetable(plan, week);
    const tasks = days.flatMap(d => d.blocks);
    expect(tasks).toHaveLength(14);
    expect(tasks.reduce((sum, t) => sum + t.durationMinutes, 0)).toBe(350);
    expect(tasks.every(t => t.durationMinutes === 25)).toBe(true);
    expect(days.slice(0, 6).every(d => d.blocks.length > 0)).toBe(true);
    expect(days[6].blocks).toHaveLength(0);
    for (const subject of input.profile.subjects)
      expect(tasks.filter(t => t.subjectName === subject.subjectName)).toHaveLength(2);
  }
  for (const task of plan.tasks.filter(t => t.afterSourceId)) {
    const parent = plan.tasks.find(t => t.sourceId === task.afterSourceId && t.subjectName === task.subjectName)!;
    expect(parent).toBeDefined();
    expect(dayDistance(parent.date, task.date)).toBeGreaterThanOrEqual(3);
  }
});

test("45-minute routine work uses Friday and Saturday while retaining the weekly ceiling", () => {
  const plan = buildStudyPlan(inputFor(45), start);
  for (const week of [0, 1]) {
    const days = plan.days.slice(week * 7, week * 7 + 7);
    expect(days.slice(0, 6).every(d => d.planned >= 45)).toBe(true);
    expect(days.reduce((sum, d) => sum + d.planned, 0)).toBe(360);
  }
});

test("scarce 90-minute slots rotate through all subjects across the fortnight", () => {
  const input = inputFor(90);
  const plan = buildStudyPlan(input, start);
  expect(new Set(plan.tasks.map(t => t.subjectName)).size).toBe(input.profile.subjects.length);
  expect(plan.tasks.every(t => t.durationMinutes === 90)).toBe(true);
  for (const week of [0, 1]) expect(planTimetable(plan, week).flatMap(d => d.blocks)).toHaveLength(4);
});

test("unplaced routine work does not overflow into the following week's opportunities", () => {
  const input = inputFor(25);
  for (let i = 0; i < 7; i++) input.settings.exceptions[addDays(start, i)] = { windowMinutes: 0, assignedMinutes: 0, breakMinutes: 0, bufferMinutes: 0 };
  const plan = buildStudyPlan(input, start);
  expect(plan.tasks.some(t => t.sourceId.includes(start))).toBe(false);
  expect(planTimetable(plan, 1).flatMap(d => d.blocks)).toHaveLength(14);
  expect(plan.unscheduled.length).toBeGreaterThan(0);
});

test("rest days, whole blocks and day/week limits hold across duration and availability combinations", () => {
  for (const duration of [15, 25, 45, 60, 90]) for (let available = 0; available <= 7; available++) {
    const input = inputFor(duration, DAYS_OF_WEEK.slice(available));
    const plan = buildStudyPlan(input, start);
    expect(plan.tasks.every(t => t.durationMinutes === duration)).toBe(true);
    expect(plan.days.every(d => d.planned <= d.capacity)).toBe(true);
    for (const week of [0, 1])
      expect(plan.days.slice(week * 7, week * 7 + 7).reduce((sum, d) => sum + d.planned, 0)).toBeLessThanOrEqual(input.settings.revisionMinutes);
  }
});

test("a real due card keeps its short duration and is never pulled forward to fill routine space", () => {
  const input = inputFor(45);
  input.cards = [{ id: "french-review", subjectName: "French", dueOn: "2026-11-19", cardIds: ["card-a"], minutes: 15 }];
  const plan = buildStudyPlan(input, start);
  expect(plan.tasks.find(t => t.kind === "cards")).toMatchObject({ date: "2026-11-19", durationMinutes: 15 });
  expect(plan.tasks.filter(t => t.kind !== "cards").every(t => t.durationMinutes === 45)).toBe(true);
});

test("balancing overdue routine contact cannot displace a whole dated deadline task", () => {
  const input = inputFor(45);
  input.settings.revisionMinutes = 90;
  input.lastContact = Object.fromEntries(input.profile.subjects.map(s => [s.subjectName, "2026-01-01"]));
  input.deadlines = [{ id: "test-prep", subjectName: "Mathematics", title: "Class test preparation", dueOn: "2026-11-11", minutes: 90 }];
  const plan = buildStudyPlan(input, start);
  expect(plan.tasks.find(t => t.kind === "deadline")).toMatchObject({ durationMinutes: 90 });
  expect(plan.tasks.find(t => t.kind === "deadline")!.date < "2026-11-11").toBe(true);
});
