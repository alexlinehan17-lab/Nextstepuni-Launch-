import React from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from "@testing-library/react";
import CertlePage from "../components/certle/CertlePage";
import { dublinDay } from "../components/landing/fx-e/dublin";
import { GAME_KEY, STATS_KEY } from "../components/certle/game";
import type { CertleQuestion } from "../components/certle/data";

// jsdom does not implement the native dialog lifecycle. Browser checks cover
// top-layer rendering, focus and the real close controls.
Object.defineProperties(HTMLDialogElement.prototype, {
  showModal: { configurable: true, value() { this.setAttribute("open", ""); } },
  close: { configurable: true, value() { this.removeAttribute("open"); } },
});

const question: CertleQuestion = {
  id: "certle-ui-fixture",
  subject: "Biology",
  year: 2025,
  level: "Higher Level",
  ref: "Q1",
  question: "Name the process and describe how food is moved along the gut.",
  points: [
    { id: "process", verbatim: "Peristalsis", marks: 3 },
    { id: "action", verbatim: "Muscular contractions", marks: 3 },
  ],
  attribution: "SEC scheme — test fixture",
};
const response = () =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({ entries: [question] }),
  });
beforeEach(() => {
  localStorage.clear();
  vi.stubGlobal("fetch", vi.fn(response));
});
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});
async function open() {
  render(<CertlePage />);
  return screen.findByRole("textbox", { name: "Your answer" });
}
async function answer(value: string) {
  fireEvent.change(screen.getByRole("textbox"), { target: { value } });
  fireEvent.click(screen.getByRole("button", { name: "Check my answer" }));
}

describe("CERTLE player flow", () => {
  it("awards partial marks, hides the scheme, and lets the player improve to full marks", async () => {
    await open();
    expect(
      screen.getByRole("button", { name: "Check my answer" }),
    ).toBeDisabled();
    await answer("peristalsis");
    expect(
      screen.getByLabelText("Attempt 1: 3 of 6 marks"),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("textbox", { name: "Improve your answer" }),
    ).toHaveValue("peristalsis");
    expect(
      screen.queryByRole("heading", { name: "Here’s where the marks are." }),
    ).not.toBeInTheDocument();
    expect(screen.queryByText("Muscular contractions")).not.toBeInTheDocument();
    await answer("peristalsis, muscles contract");
    expect(
      screen.getByLabelText("Attempt 2: 6 of 6 marks"),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "Here’s where the marks are." }),
    ).toBeInTheDocument();
    expect(screen.queryByRole("textbox")).not.toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Share my result" }),
    ).toBeInTheDocument();
    expect(JSON.parse(localStorage.getItem(STATS_KEY)!).results).toHaveLength(
      1,
    );
  });
  it("restores an unfinished game and draft after a reload and ends on the third attempt", async () => {
    await open();
    await answer("peristalsis");
    cleanup();
    render(<CertlePage />);
    expect(
      await screen.findByRole("textbox", { name: "Improve your answer" }),
    ).toHaveValue("peristalsis");
    await answer("peristalsis");
    expect(screen.getByRole("alert")).toHaveTextContent(
      "You’ve tried that answer",
    );
    expect(screen.getByText("ATTEMPT 2 / 3")).toBeInTheDocument();
    await answer("muscles contract");
    await answer("unsure");
    expect(screen.queryByRole("textbox")).not.toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "Here’s where the marks are." }),
    ).toBeInTheDocument();
    const saved = JSON.parse(localStorage.getItem(GAME_KEY)!);
    expect(saved.answers).toHaveLength(3);
    expect(saved.finished).toBe(true);
    const final = JSON.parse(localStorage.getItem(STATS_KEY)!).results[0];
    expect(final.earned).toBe(3);
  });
  it("allows the player to finish early and keeps the result final on reopening", async () => {
    await open();
    await answer("peristalsis");
    fireEvent.click(
      screen.getByRole("button", { name: "Finish & see the scheme" }),
    );
    expect(screen.getByText("Muscular contractions")).toBeInTheDocument();
    cleanup();
    render(<CertlePage />);
    expect(
      await screen.findByRole("button", { name: "Share my result" }),
    ).toBeInTheDocument();
    expect(screen.queryByRole("textbox")).not.toBeInTheDocument();
    expect(JSON.parse(localStorage.getItem(STATS_KEY)!).results).toHaveLength(
      1,
    );
  });
  it("rescans a saved answer and updates today’s record without adding a game", async () => {
    const day = dublinDay(new Date());
    localStorage.setItem(GAME_KEY, JSON.stringify({
      version: 2, day, id: question.id,
      answers: ["Peristalssis, muscular contracitons"], finished: true,
    }));
    localStorage.setItem(STATS_KEY, JSON.stringify({ results: [
      { day, id: question.id, earned: 0, total: 6, attempts: 1, complete: false },
    ] }));
    render(<CertlePage />);
    expect(await screen.findByLabelText("Attempt 1: 6 of 6 marks")).toBeInTheDocument();
    await waitFor(() => expect(JSON.parse(localStorage.getItem(STATS_KEY)!).results).toEqual([
      { day, id: question.id, earned: 6, total: 6, attempts: 1, complete: true },
    ]));
  });
  it("explains the rules in three readable steps and returns to play", async () => {
    await open();
    fireEvent.click(screen.getByRole("button", { name: "How to play" }));
    const help = screen.getByRole("dialog", { name: "How to play CERTLE" });
    expect(within(help).getAllByRole("listitem")).toHaveLength(3);
    expect(within(help).getByText(/best attempt is the score/)).toBeInTheDocument();
    expect(within(help).getByLabelText("Example: 3 of 6 marks earned")).toBeInTheDocument();
    fireEvent.click(within(help).getByRole("button", { name: "Let’s play" }));
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(screen.getByRole("textbox", { name: "Your answer" })).toBeInTheDocument();
  });
  it("shows every attempt count, including zeros, with proportional bars", async () => {
    localStorage.setItem(STATS_KEY, JSON.stringify({ results: [
      { day: "2026-09-01", id: "old-1", earned: 3, total: 3, attempts: 1, complete: true },
      { day: "2026-09-02", id: "old-2", earned: 3, total: 3, attempts: 1, complete: true },
      { day: "2026-09-03", id: "old-3", earned: 3, total: 3, attempts: 3, complete: true },
    ] }));
    await open();
    fireEvent.click(screen.getByRole("button", { name: "Your statistics" }));
    const record = screen.getByRole("dialog", { name: "Your CERTLE record" });
    for (const [attempt, count] of [[1, 2], [2, 0], [3, 1]]) {
      const row = within(record).getByLabelText(`Attempt ${attempt}: ${count} full-mark games`);
      expect(row.querySelector<HTMLElement>(".certle-distribution-fill")!.style.width).toBe(`${count / 3 * 100}%`);
    }
  });
  it("recovers from a failed question load without erasing saved data", async () => {
    vi.mocked(fetch).mockRejectedValueOnce(new Error("offline"));
    localStorage.setItem("untouched-key", "saved");
    render(<CertlePage />);
    expect(await screen.findByRole("alert")).toHaveTextContent("couldn’t load");
    fireEvent.click(screen.getByRole("button", { name: "Retry" }));
    expect(
      await screen.findByRole("textbox", { name: "Your answer" }),
    ).toBeInTheDocument();
    expect(localStorage.getItem("untouched-key")).toBe("saved");
  });
  it("ignores malformed drafts rather than crashing the page", async () => {
    localStorage.setItem(
      `nextstepuni.certle.draft:${dublinDay(new Date())}:${question.id}`,
      JSON.stringify({ invalid: true }),
    );
    expect(await open()).toHaveValue("");
  });
  it("keeps navigation back to landing sections and includes CERTLE in the mobile menu", async () => {
    await open();
    const primary = screen.getByRole("navigation", { name: "Primary" });
    expect(
      within(primary).getByRole("link", { name: "CERTLE" }),
    ).toHaveAttribute("href", "/certle");
    expect(
      within(primary).getByRole("link", { name: "What's inside" }),
    ).toHaveAttribute("href", "/landing#chapters");
    fireEvent.click(screen.getByRole("button", { name: "Menu" }));
    await waitFor(() =>
      expect(screen.getAllByRole("link", { name: "CERTLE" })).toHaveLength(2),
    );
  });
});
