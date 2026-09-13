import React from "react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import Onboarding from "../components/Onboarding";
import {
  draftKey,
  initialDraft,
  type SetupDraft,
} from "../components/onboarding/model";
vi.mock("../utils/funnel", () => ({ trackFunnel: vi.fn() }));
vi.mock("../hooks/useMobileAppDesign", () => ({
  useMobileAppDesign: () => false,
}));
const uid = "desktop-release-test";
const grades = (): SetupDraft => ({
  ...initialDraft(),
  step: "grades",
  year: "5th",
  date: "2030-06-05",
  dateConfirmed: true,
  rest: ["Sunday"],
  category: "college-learning",
  vision: ["campus"],
  subjects: ["English", "Irish"],
  configs: {
    English: { level: null, current: "", target: "", reviewed: false },
    Irish: { level: null, current: "", target: "", reviewed: false },
  },
});
function mount(draft?: SetupDraft, complete = vi.fn()) {
  if (draft)
    localStorage.setItem(draftKey(uid, "fresh"), JSON.stringify(draft));
  return render(
    <Onboarding
      userId={uid}
      userName="Alex"
      onComplete={complete}
      onSkip={vi.fn()}
    />,
  );
}
beforeEach(() => {
  localStorage.clear();
  sessionStorage.clear();
});
describe("live desktop onboarding", () => {
  it("opens the approved desktop layout with an empty account-scoped draft", () => {
    const view = mount();
    expect(view.container.querySelector(".desk-flow")).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "Make your mark." }),
    ).toBeInTheDocument();
    expect(
      JSON.parse(localStorage.getItem(draftKey(uid, "fresh"))!).subjects,
    ).toEqual([]);
    expect(
      screen.queryByRole("complementary", { name: "Compare grade layouts" }),
    ).not.toBeInTheDocument();
  });
  it("requires every level and lets students defer grades without inventing them", () => {
    mount(grades());
    expect(
      screen.getByRole("button", { name: "Continue to schedule" }),
    ).toBeDisabled();
    fireEvent.change(screen.getByLabelText("English level"), {
      target: { value: "higher" },
    });
    fireEvent.change(screen.getByLabelText("Irish level"), {
      target: { value: "ordinary" },
    });
    fireEvent.change(screen.getByLabelText("English current grade"), {
      target: { value: "H3" },
    });
    fireEvent.click(
      screen.getByRole("button", { name: "Leave unfilled grades for later" }),
    );
    fireEvent.click(
      screen.getByRole("button", { name: "Continue to schedule" }),
    );
    expect(
      screen.getByRole("heading", { name: "Make room for progress." }),
    ).toBeInTheDocument();
    const saved = JSON.parse(localStorage.getItem(draftKey(uid, "fresh"))!);
    expect(saved.configs.English).toEqual({
      level: "higher",
      current: "H3",
      target: "later",
      reviewed: true,
    });
    expect(saved.configs.Irish).toEqual({
      level: "ordinary",
      current: "later",
      target: "later",
      reviewed: true,
    });
  });
  it("submits real profile data and preserves answers when the save fails", async () => {
    const complete = vi.fn().mockRejectedValue(new Error("offline"));
    const draft = grades();
    draft.step = "summary";
    draft.configs = {
      English: { level: "higher", current: "H3", target: "H1", reviewed: true },
      Irish: {
        level: "ordinary",
        current: "later",
        target: "later",
        reviewed: true,
      },
    };
    mount(draft, complete);
    fireEvent.click(screen.getByRole("button", { name: "Start Learning" }));
    await waitFor(() =>
      expect(screen.getByText(/couldn’t save your setup/)).toBeInTheDocument(),
    );
    expect(complete.mock.calls[0][0].subjects).toEqual([
      {
        subjectName: "English",
        level: "higher",
        currentGrade: "H3",
        targetGrade: "H1",
      },
      { subjectName: "Irish", level: "ordinary" },
    ]);
    expect(JSON.parse(localStorage.getItem(draftKey(uid, "fresh"))!).step).toBe(
      "summary",
    );
  });
  it("cancels bulk grade edits back to the committed review on reload", () => {
    const draft = grades();
    draft.step = "summary";
    draft.configs = {
      English: { level: "higher", current: "H3", target: "H1", reviewed: true },
      Irish: {
        level: "ordinary",
        current: "later",
        target: "later",
        reviewed: true,
      },
    };
    const view = mount(draft);
    fireEvent.click(
      screen.getByRole("button", { name: "Edit English grades" }),
    );
    fireEvent.change(screen.getByLabelText("English target grade"), {
      target: { value: "H2" },
    });
    view.unmount();
    mount();
    expect(
      screen.getByRole("heading", { name: "You’re ready, Alex." }),
    ).toBeInTheDocument();
    expect(screen.getByText("H3 → H1")).toBeInTheDocument();
  });
});
