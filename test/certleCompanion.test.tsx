import React from "react";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";
import type { StarguySignals } from "../components/landing/starguy/StarguyFigure";
import CertleCompanion from "../components/certle/CertleCompanion";
const rig = vi.hoisted(() => ({ fail: false, signals: null as unknown }));
vi.mock("../components/landing/starguy/StarguyFigure", () => ({
  default: (props: StarguySignals) => {
    rig.signals = props;
    if (rig.fail) throw new Error("Rive unavailable");
    return <span data-testid="live-starguy" />;
  },
}));
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
  rig.fail = false;
  rig.signals = null;
});
function motionPreference(enabled: boolean) {
  vi.stubGlobal("matchMedia", () => ({
    matches: enabled,
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
  }));
}
it("provides every motion signal required by the existing Rive rig", async () => {
  motionPreference(true);
  render(<CertleCompanion />);
  expect(await screen.findByTestId("live-starguy")).toBeInTheDocument();
  const signals = rig.signals as StarguySignals;
  for (const name of ["speed", "lean", "squash", "lookX", "lookY"] as const)
    expect(typeof signals[name]?.get()).toBe("number");
});
it("shows the actual still character when reduced motion is requested", () => {
  motionPreference(false);
  const { container } = render(<CertleCompanion />);
  expect(screen.queryByTestId("live-starguy")).not.toBeInTheDocument();
  expect(container.querySelector("img")).toHaveAttribute(
    "src",
    "/assets/landing/starguy-512.png",
  );
});
it("contains a failed animation so the surrounding game stays usable", async () => {
  motionPreference(true);
  rig.fail = true;
  vi.spyOn(console, "error").mockImplementation(() => {});
  const { container } = render(
    <>
      <CertleCompanion />
      <button>Check my answer</button>
    </>,
  );
  expect(
    await screen.findByRole("button", { name: "Check my answer" }),
  ).toBeEnabled();
  expect(container.querySelector("img")).toHaveAttribute(
    "src",
    "/assets/landing/starguy-512.png",
  );
});
