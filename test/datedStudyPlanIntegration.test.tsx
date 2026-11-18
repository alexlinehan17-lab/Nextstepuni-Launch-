import {
  act,
  cleanup,
  render,
  screen,
} from "@testing-library/react";
import { afterEach, expect, test, vi } from "vitest";
import { writeLocal } from "../components/MarkBank/store";
import { NEW_CARD } from "../components/MarkBank/scheduler";
import {
  currentCardNeeds,
  useDatedStudyPlan,
} from "../hooks/useDatedStudyPlan";
import { studyPlannerSample, SAMPLE_START } from "../data/studyPlannerSamples";
import {
  createStudyPlan,
  readStudyPlan,
  setTaskStatus,
} from "../services/studyPlanStore";
import {
  preserveLegacyCompletions,
  buildStudyPlan,
} from "../services/studyPlanEngine";


vi.mock("../contexts/ProgressContext", () => ({
  useOptionalProgress: () => null,
}));
afterEach(() => {
  cleanup();
  vi.useRealTimers();
});

test("two different views observe the same task IDs and completion immediately", () => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date("2026-11-02T12:00:00Z"));
  const input = studyPlannerSample("sixth");
  createStudyPlan("consumer-parity", input, SAMPLE_START, SAMPLE_START, true);
  function Consumer({ name }: { name: string }) {
    const { saved } = useDatedStudyPlan(input.profile, "consumer-parity");
    return (
      <output aria-label={name}>
        {saved?.plan.tasks.map((t) => `${t.id}:${t.status}`).join("\n")}
      </output>
    );
  }
  render(
    <>
      <Consumer name="Home" />
      <Consumer name="Planner" />
    </>,
  );
  expect(screen.getByLabelText("Home").textContent).toBe(
    screen.getByLabelText("Planner").textContent,
  );
  const task = readStudyPlan("consumer-parity")!.plan.tasks[0];
  act(() => setTaskStatus("consumer-parity", task.id, "completed"));
  expect(screen.getByLabelText("Home").textContent).toContain(
    `${task.id}:completed`,
  );
  expect(screen.getByLabelText("Home").textContent).toBe(
    screen.getByLabelText("Planner").textContent,
  );
});
test("legacy completions survive activation with their original IDs and visible uncertainty", () => {
  const inputs = studyPlannerSample("fifth");
  const id = "Mathematics|revision|2";
  const previous = preserveLegacyCompletions(inputs, SAMPLE_START, {
    [SAMPLE_START]: [id],
  });
  const plan = buildStudyPlan(inputs, SAMPLE_START, previous);
  expect(plan.tasks.find((t) => t.id === id)).toMatchObject({
    date: SAMPLE_START,
    status: "completed",
  });
  expect(plan.tasks.find((t) => t.id === id)!.why).toContain(
    "did not store exact minutes",
  );
});

test("Mark Bank aliases contribute one canonical review without changing card memory", () => {
  const profile = studyPlannerSample("sixth").profile;
  const old = {
    ...NEW_CARD,
    last: new Date("2026-10-20T12:00:00Z").getTime(),
    state: 2 as const,
    s: 2,
    reps: 2,
  };
  writeLocal("alias-review", "biology-higher", {
    v: 1,
    cards: { "bio-2024-hl-q8-b2": old, "bio-2024-hl-q8-b1": old },
    updatedAt: old.last,
  });
  const needs = currentCardNeeds("alias-review", profile).filter(
    (c) => c.subjectName === "Biology",
  );
  expect(needs.flatMap((c) => c.cardIds)).toEqual(["bio-2024-hl-q8-b1"]);
});

test("shared plan consumers observe the new local day across midnight", () => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date("2026-11-02T23:59:59Z"));
  const input = studyPlannerSample("sixth");
  function ClockConsumer() {
    const { today } = useDatedStudyPlan(input.profile, "midnight-review");
    return <output aria-label="Planner local day">{today}</output>;
  }
  render(<ClockConsumer />);
  expect(screen.getByLabelText("Planner local day")).toHaveTextContent(
    "2026-11-02",
  );
  act(() => vi.advanceTimersByTime(1200));
  expect(screen.getByLabelText("Planner local day")).toHaveTextContent(
    "2026-11-03",
  );
});
