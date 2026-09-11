import React from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, render, screen, waitFor } from "@testing-library/react";
import Lenis from "lenis";
import Viewer from "../components/PaperTrail/Viewer";
vi.mock("../components/PaperTrail/pdfjsLoader", () => ({
  loadPdfjs: () => new Promise(() => {}),
}));
vi.mock("../components/PaperTrail/pdfCache", () => ({
  fetchPdfCached: vi.fn(() => Promise.resolve(null)),
}));
const paper = { url: "/test-paper.pdf", label: "Paper", bytes: 100 };
const scheme = { url: "/test-scheme.pdf", label: "Scheme", bytes: 100 };
beforeEach(() => {
  vi.stubGlobal(
    "fetch",
    vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ v: 1, q: [] }),
      }),
    ),
  );
});
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});
describe("Paper Trail previews", () => {
  it("exempts the portalled viewer from the landing page scroll controller", () => {
    render(<Viewer title="Test paper" paper={paper} onClose={() => {}} />);
    const pageScroll = new Lenis();
    pageScroll.stop();
    try {
      const outside = new WheelEvent("wheel", {
        bubbles: true,
        cancelable: true,
        deltaY: 120,
      });
      document.body.dispatchEvent(outside);
      expect(outside.defaultPrevented).toBe(true);
      const inside = new WheelEvent("wheel", {
        bubbles: true,
        cancelable: true,
        deltaY: 120,
      });
      screen.getByRole("dialog").dispatchEvent(inside);
      expect(inside.defaultPrevented).toBe(false);
    } finally {
      pageScroll.destroy();
    }
  });
  it("opens with Answers enabled and requests its map without requiring a click", async () => {
    render(
      <Viewer
        title="Test paper"
        paper={paper}
        scheme={scheme}
        answersUrl="/answer-map.json"
        initialAnswersOn
        onClose={() => {}}
      />,
    );
    expect(
      screen.getByRole("button", {
        name: "Show the marking scheme beside each question",
      }),
    ).toHaveAttribute("aria-pressed", "true");
    await waitFor(() => expect(fetch).toHaveBeenCalledWith("/answer-map.json"));
    expect(fetch).toHaveBeenCalledTimes(1);
  });
  it("leaves normal app opens unchanged, with Answers off", () => {
    render(
      <Viewer
        title="Test paper"
        paper={paper}
        scheme={scheme}
        answersUrl="/answer-map.json"
        onClose={() => {}}
      />,
    );
    expect(
      screen.getByRole("button", {
        name: "Show the marking scheme beside each question",
      }),
    ).toHaveAttribute("aria-pressed", "false");
    expect(fetch).not.toHaveBeenCalled();
  });
});
