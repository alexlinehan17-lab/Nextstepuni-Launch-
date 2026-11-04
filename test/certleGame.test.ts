import { beforeEach, describe, expect, it } from "vitest";
import {
  bestResult,
  emptyGame,
  GAME_KEY,
  recordResult,
  restoreGame,
  resultsFor,
  shareText,
  statsSummary,
  submitAnswer,
} from "../components/certle/game";
import type { CertleQuestion } from "../components/certle/data";
import {
  dublinDay,
  nextDublinMidnight,
} from "../components/landing/fx-e/dublin";
const q: CertleQuestion = {
  id: "test",
  subject: "Biology",
  year: 2025,
  level: "Higher Level",
  ref: "Q1",
  question: "Name the process and how it works.",
  points: [
    { id: "a", verbatim: "Peristalsis", marks: 3 },
    { id: "b", verbatim: "Muscular contractions", marks: 3 },
  ],
  attribution: "Test fixture",
};
const DAY = "2026-09-11";
beforeEach(() => localStorage.clear());
describe("CERTLE attempts and persistence", () => {
  it("keeps partial credit and allows an improved attempt", () => {
    const first = submitAnswer(emptyGame(DAY, q.id), q, "peristalsis");
    expect(first.finished).toBe(false);
    expect(resultsFor(first, q)[0].earned).toBe(3);
    const next = submitAnswer(first, q, "peristalsis, muscles contract");
    expect(next.finished).toBe(true);
    expect(next.answers).toHaveLength(2);
    expect(bestResult(resultsFor(next, q))?.earned).toBe(6);
  });
  it("retains the best full response instead of combining unrelated attempts", () => {
    const first = submitAnswer(emptyGame(DAY, q.id), q, "peristalsis");
    const next = submitAnswer(first, q, "muscles contract");
    expect(bestResult(resultsFor(next, q))?.earned).toBe(3);
    expect(next.finished).toBe(false);
  });
  it("ends after three attempts and rejects empty or repeated submissions without using an attempt", () => {
    const game = emptyGame(DAY, q.id);
    expect(submitAnswer(game, q, " ")).toBe(game);
    const a = submitAnswer(game, q, "unknown");
    expect(submitAnswer(a, q, " UNKNOWN ")).toBe(a);
    const b = submitAnswer(a, q, "something else"),
      c = submitAnswer(b, q, "still unsure");
    expect(c.finished).toBe(true);
    expect(c.answers).toHaveLength(3);
    expect(submitAnswer(c, q, "peristalsis")).toBe(c);
  });
  it("restores today’s attempts, starts afresh tomorrow, and survives invalid storage", () => {
    const game = submitAnswer(emptyGame(DAY, q.id), q, "peristalsis");
    localStorage.setItem(GAME_KEY, JSON.stringify(game));
    expect(restoreGame(DAY, q)).toEqual(game);
    expect(restoreGame("2026-09-12", q).answers).toEqual([]);
    localStorage.setItem(GAME_KEY, "invalid json");
    expect(restoreGame(DAY, q).answers).toEqual([]);
  });
  it("preserves a legacy result as finished because the scheme was already revealed", () => {
    localStorage.setItem(
      "landing.today.v1",
      JSON.stringify({ day: DAY, id: q.id, answer: "peristalsis" }),
    );
    expect(restoreGame(DAY, q)).toMatchObject({
      answers: ["peristalsis"],
      finished: true,
    });
  });
  it("counts a completed day once and builds a participation streak", () => {
    const game = {
      ...submitAnswer(emptyGame(DAY, q.id), q, "peristalsis"),
      finished: true,
    };
    const yesterday = recordResult(
      { results: [] },
      { ...game, day: "2026-09-10" },
      q,
    );
    const stats = recordResult(recordResult(yesterday, game, q), game, q);
    expect(stats.results).toHaveLength(2);
    expect(statsSummary(stats, DAY)).toMatchObject({
      streak: 2,
      fullMarks: 0,
      played: 2,
    });
    expect(statsSummary(stats, "2026-09-13").streak).toBe(0);
  });
  it("shares scores and attempts without the question’s answer", () => {
    const game = {
      ...submitAnswer(emptyGame(DAY, q.id), q, "peristalsis"),
      finished: true,
    };
    const text = shareText(11, game, q, "https://example.test");
    expect(text).toContain("CERTLE #11");
    expect(text).toContain("3/6 marks");
    expect(text).toContain("1/3 attempts");
    expect(text).toContain("https://example.test/certle");
    expect(text).not.toContain("peristalsis");
    expect(text).toContain("🟧🟧🟧⬜⬜⬜");
  });
});
describe("Irish daily rollover", () => {
  it.each([
    ["2026-09-11T12:00:00Z", "2026-09-11T23:00:00Z"],
    ["2026-03-29T00:30:00Z", "2026-03-29T23:00:00Z"],
    ["2026-10-25T00:30:00Z", "2026-10-26T00:00:00Z"],
  ])("finds midnight including daylight saving transitions: %s", (now, end) => {
    expect(new Date(nextDublinMidnight(new Date(now))).toISOString()).toBe(
      new Date(end).toISOString(),
    );
  });
  it("changes the daily question at Irish midnight", () => {
    expect(dublinDay(new Date("2026-09-11T22:59:59Z"))).toBe("2026-09-11");
    expect(dublinDay(new Date("2026-09-11T23:00:00Z"))).toBe("2026-09-12");
  });
});

describe("CERTLE numbered image answers", () => {
  const industry: CertleQuestion = {
    id: "bus-2022-ol-s1-q2",
    subject: "Business",
    year: 2022,
    level: "Ordinary Level",
    ref: "Section 1 Q2",
    question:
      "Identify the category of industry most appropriate to each of the images shown below.",
    points: [
      { id: "r-1", verbatim: "(i) — Secondary", marks: 5 },
      { id: "r-2", verbatim: "(ii) — Tertiary/Services", marks: 5 },
      { id: "r-3", verbatim: "(iii) — Primary", marks: 5 },
    ],
    attribution: "SEC Business 2022 OL",
  };
  const grade = (answer: string) =>
    resultsFor(
      submitAnswer(emptyGame(DAY, industry.id), industry, answer),
      industry,
    )[0].earned;
  it("accepts categories in image order without requiring printed punctuation", () => {
    expect(
      grade("Secondary industry; tertiary industry; primary industry."),
    ).toBe(15);
    expect(grade("Secondary, services, primary")).toBe(15);
    expect(grade("Secondary")).toBe(5);
  });
  it("binds explicit part labels even when the parts are written out of order", () => {
    expect(grade("(iii) Primary (i) Secondary (ii) Services")).toBe(15);
    expect(grade("2. Services")).toBe(5);
    expect(grade("1. Secondary\n2. Tertiary\n3. Primary")).toBe(15);
  });
  it("does not award marks for correct categories attached to the wrong images", () => {
    expect(grade("Primary; Secondary; Tertiary")).toBe(0);
    expect(grade("(i) Primary (ii) Secondary (iii) Tertiary")).toBe(0);
    expect(grade("Secondary; Primary; Tertiary")).toBe(5);
    expect(grade("Secondary tertiary primary")).toBe(5);
  });
});
