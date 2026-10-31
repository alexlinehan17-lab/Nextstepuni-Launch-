import { beforeEach, afterEach, describe, it, expect, vi } from "vitest";
import {
  emptyAnswer,
  readAnswer,
  writeAnswer,
  keepFirstAttempt,
  loadAttemptFirst,
  saveAttemptFirst,
  answerCopy,
  type InkStroke,
} from "../components/PaperTrail/answerDeskStore";
const ns = "student-a|maths|2026|ordinary|paper1";
const ink: InkStroke = {
  points: [
    [0.2, 0.3],
    [0.4, 0.5],
  ],
  kind: "pen",
  colour: "#162d4d",
};
beforeEach(() => localStorage.clear());
afterEach(() => vi.restoreAllMocks());
describe("Attempt-first preference", () => {
  it("defaults on, remembers an explicit off across papers, and isolates accounts", () => {
    expect(loadAttemptFirst(ns)).toBe(true);
    expect(saveAttemptFirst(ns, false)).toBe(true);
    expect(loadAttemptFirst("student-a|english|paper2")).toBe(false);
    expect(loadAttemptFirst("student-b|maths|paper1")).toBe(true);
    saveAttemptFirst(ns, true);
    expect(loadAttemptFirst(ns)).toBe(true);
  });
  it("stays on if storage cannot be read and reports a failed preference save", () => {
    vi.spyOn(Storage.prototype, "getItem").mockImplementation(() => {
      throw Error("blocked");
    });
    vi.spyOn(Storage.prototype, "setItem").mockImplementation(() => {
      throw Error("blocked");
    });
    expect(loadAttemptFirst(ns)).toBe(true);
    expect(saveAttemptFirst(ns, false)).toBe(false);
  });
});
describe("Student-authored work", () => {
  it("isolates every account, paper and question and roundtrips handwritten working", () => {
    const r = emptyAnswer();
    r.draft = { text: "My method", ink: { 4: [ink] } };
    const saved = writeAnswer(ns, "1", r);
    expect(saved.problem).toBeUndefined();
    expect(readAnswer(ns, "1").record.draft).toEqual(r.draft);
    for (const [space, id] of [
      [ns, "2"],
      ["student-b|maths|2026|ordinary|paper1", "1"],
      ["student-a|maths|2026|ordinary|paper2", "1"],
    ])
      expect(readAnswer(space, id).record.draft.text).toBe("");
  });
  it("freezes the first attempt by value and keeps retry and correction separate", () => {
    const draft = emptyAnswer();
    draft.draft = { text: "€7.62", ink: { 4: [structuredClone(ink)] } };
    const first = keepFirstAttempt(draft);
    draft.draft.text = "€71.12";
    draft.draft.ink[4][0].points[0][0] = 0.9;
    first.retry = { text: "€71.12", ink: { 4: [ink] } };
    first.correction = "Include the original cost.";
    const reopened = keepFirstAttempt(first);
    expect(reopened.first).toEqual({ text: "€7.62", ink: { 4: [ink] } });
    expect(reopened.retry.text).toBe("€71.12");
    expect(reopened.correction).toBe("Include the original cost.");
  });
  it("refuses to overwrite a newer revision from another tab", () => {
    const old = emptyAnswer();
    const fresh = writeAnswer(ns, "1", {
      ...old,
      draft: { text: "Other tab", ink: {} },
    });
    const stale = writeAnswer(ns, "1", {
      ...old,
      draft: { text: "This tab", ink: {} },
    });
    expect(stale.problem).toContain("another tab");
    expect(stale.record.draft.text).toBe("This tab");
    expect(readAnswer(ns, "1").record).toEqual(fresh.record);
  });
  it("preserves corrupt saved data instead of silently replacing it", () => {
    const key = `pt:written:v1:${encodeURIComponent(ns)}:1`;
    localStorage.setItem(key, "{broken");
    expect(readAnswer(ns, "1").problem).toBeTruthy();
    expect(writeAnswer(ns, "1", emptyAnswer()).problem).toBeTruthy();
    expect(localStorage.getItem(key)).toBe("{broken");
  });
  it("keeps the latest work in memory and the last saved copy intact when storage fills", () => {
    const saved = writeAnswer(ns, "1", emptyAnswer()).record;
    vi.spyOn(Storage.prototype, "setItem").mockImplementation(() => {
      throw new DOMException("full", "QuotaExceededError");
    });
    const result = writeAnswer(ns, "1", {
      ...saved,
      draft: { text: "New unsaved work", ink: { 4: [ink] } },
    });
    expect(result.problem).toContain("could not save");
    expect(result.record.draft.text).toBe("New unsaved work");
    expect(readAnswer(ns, "1").record).toEqual(saved);
  });
  it("exports escaped student text, both attempts, reflection and handwriting", () => {
    const r = emptyAnswer();
    r.draft = { text: "<script>alert(1)</script>", ink: { 4: [ink] } };
    const kept = keepFirstAttempt(r);
    kept.retry.text = "Second answer";
    kept.correction = "Use the total.";
    const html = answerCopy("Maths", "Question 1", kept);
    expect(html).not.toContain("<script>");
    expect(html).toContain("&lt;script&gt;");
    expect(html).toContain("Second answer");
    expect(html).toContain("Use the total.");
    expect(html).toContain("<polyline");
  });
});
