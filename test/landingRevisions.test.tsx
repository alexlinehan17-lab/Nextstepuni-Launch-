import React from "react";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import ExaminerWants from "../components/landing/fx-d/ExaminerWants";
import GlassStage from "../components/landing/glass/GlassStage";

afterEach(cleanup);
describe("Landing page revisions", () => {
  it("starts with the shorter 2024 Business answer and keeps 2021 second", () => {
    render(<ExaminerWants />);
    const tabs = screen.getAllByRole("tab");
    expect(tabs[0]).toHaveTextContent("Business · 2024");
    expect(tabs[0]).toHaveAttribute("aria-selected", "true");
    expect(tabs[1]).toHaveTextContent("Business · 2021");
    expect(
      screen.getByText("Distinguish between an Embargo and a Quota."),
    ).toBeInTheDocument();
    fireEvent.click(tabs[1]);
    expect(
      screen.getByText(
        "Describe the first four stages involved in the development process of a new product.",
      ),
    ).toBeInTheDocument();
  });
  it("lets a nested pane use the mouse wheel when the outer glass is at its boundary", () => {
    const { container } = render(
      <GlassStage active={false}>
        <div data-testid="pane" style={{ overflowY: "auto" }}>
          <span>Paper content</span>
        </div>
      </GlassStage>,
    );
    const outer = container.querySelector(".landing-glass")!,
      pane = screen.getByTestId("pane");
    Object.defineProperties(outer, {
      scrollHeight: { value: 500 },
      clientHeight: { value: 500 },
    });
    Object.defineProperties(pane, {
      scrollHeight: { value: 1800 },
      clientHeight: { value: 400 },
      scrollTop: { value: 200, writable: true },
    });
    const event = new WheelEvent("wheel", {
      bubbles: true,
      cancelable: true,
      deltaY: 100,
    });
    pane.dispatchEvent(event);
    expect(event.defaultPrevented).toBe(false);
    pane.scrollTop = 1400;
    const end = new WheelEvent("wheel", {
      bubbles: true,
      cancelable: true,
      deltaY: 100,
    });
    pane.dispatchEvent(end);
    expect(end.defaultPrevented).toBe(true);
  });
});
