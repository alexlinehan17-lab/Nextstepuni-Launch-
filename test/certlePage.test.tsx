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
