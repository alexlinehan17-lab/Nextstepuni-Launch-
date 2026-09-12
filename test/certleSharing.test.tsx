import React from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from "@testing-library/react";
import { emptyGame, submitAnswer } from "../components/certle/game";
import {
  resultShareData,
  socialShareUrl,
  PUBLIC_CERTLE_URL,
  createResultImage,
} from "../components/certle/sharing";
import type * as Sharing from "../components/certle/sharing";
import ShareResult from "../components/certle/ShareResult";
import type { CertleQuestion } from "../components/certle/data";

vi.mock("../components/certle/sharing", async (importOriginal) => ({
  ...(await importOriginal<typeof Sharing>()),
  createResultImage: vi.fn(),
}));
const question: CertleQuestion = {
  id: "share-fixture",
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
const partial = submitAnswer(
  emptyGame("2026-09-11", question.id),
  question,
  "peristalsis",
);
const complete = submitAnswer(
  partial,
  question,
  "peristalsis, muscles contract",
);
const data = resultShareData(11, complete, question);
const file = new File(["result-image"], "certle-2026-09-11.png", {
  type: "image/png",
});
let copy: ReturnType<typeof vi.fn>;
beforeEach(() => {
  copy = vi.fn().mockResolvedValue(undefined);
  vi.stubGlobal("navigator", { clipboard: { writeText: copy } });
  vi.stubGlobal(
    "URL",
    class extends URL {
      static createObjectURL = vi.fn(() => "blob:certle-fixture");
      static revokeObjectURL = vi.fn();
    },
  );
  vi.mocked(createResultImage).mockResolvedValue(file);
});
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  vi.clearAllMocks();
});

describe("CERTLE spoiler-free sharing", () => {
  it("exports actual partial and full mark rows without responses or the scheme", () => {
    expect(data.earned).toBe(6);
    expect(data.rows).toEqual([
      [true, true, true, false, false, false],
      [true, true, true, true, true, true],
    ]);
    expect(data.text).toContain("6/6 marks · 2/3 attempts");
    expect(data.text).toContain(PUBLIC_CERTLE_URL);
    expect(JSON.stringify(data).toLowerCase()).not.toMatch(
      /peristalsis|muscular|along the gut/,
    );
    expect(() => resultShareData(11, partial, question)).toThrow("Finish");
  });
  it("encodes multiline scores and includes only the public URL in Facebook and LinkedIn previews", () => {
    for (const platform of ["Facebook", "LinkedIn"] as const) {
      const url = new URL(socialShareUrl(platform, data.text));
      expect([...url.searchParams.values()]).toEqual([PUBLIC_CERTLE_URL]);
    }
    for (const platform of ["X", "WhatsApp"] as const) {
      expect(
        new URL(socialShareUrl(platform, data.text)).searchParams.get("text"),
      ).toBe(data.text);
    }
  });
  it("copies the result when a Facebook or LinkedIn composer is opened", async () => {
    render(<ShareResult data={data} />);
    const link = screen.getByRole("link", { name: "Share on LinkedIn" });
    expect(link).toHaveAttribute("target", "_blank");
    fireEvent.click(link);
    await waitFor(() => expect(copy).toHaveBeenCalledWith(data.text));
    expect(await screen.findByRole("status")).toHaveTextContent(
      "Paste it into your post",
    );
    expect(
      screen.getByRole("link", { name: "Share by email" }).getAttribute("href"),
    ).toContain(encodeURIComponent(data.text));
  });
  it("provides selectable text when clipboard access is denied", async () => {
    copy.mockRejectedValue(new Error("denied"));
    render(<ShareResult data={data} />);
    fireEvent.click(screen.getByRole("button", { name: "Copy result" }));
    expect(
      await screen.findByRole("textbox", { name: "Result to copy" }),
    ).toHaveValue(data.text);
  });
  it("shares the prepared PNG when the device supports files and treats cancel quietly", async () => {
    const share = vi
      .fn()
      .mockRejectedValue(new DOMException("Cancelled", "AbortError"));
    vi.stubGlobal("navigator", {
      clipboard: { writeText: copy },
      share,
      canShare: vi.fn(() => true),
    });
    render(<ShareResult data={data} />);
    await waitFor(() =>
      expect(screen.getByRole("button", { name: "Save image" })).toBeEnabled(),
    );
    fireEvent.click(
      screen.getByRole("button", { name: "More sharing options" }),
    );
    await waitFor(() =>
      expect(share).toHaveBeenCalledWith({
        files: [file],
        title: "My CERTLE result",
        text: data.text,
      }),
    );
    expect(copy).not.toHaveBeenCalled();
  });
  it("keeps text sharing available when image creation fails or native sharing fails", async () => {
    vi.mocked(createResultImage).mockRejectedValue(
      new Error("canvas unavailable"),
    );
    const share = vi.fn().mockRejectedValue(new Error("sharing unavailable"));
    vi.stubGlobal("navigator", { clipboard: { writeText: copy }, share });
    render(<ShareResult data={data} />);
    expect(
      await screen.findByRole("button", { name: "Image unavailable" }),
    ).toBeDisabled();
    fireEvent.click(
      screen.getByRole("button", { name: "More sharing options" }),
    );
    await waitFor(() => expect(copy).toHaveBeenCalledWith(data.text));
    expect(share).toHaveBeenCalledWith({
      title: "My CERTLE result",
      text: data.text,
    });
  });
});
