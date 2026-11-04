import React, { Suspense, useEffect, useRef } from "react";
import { createRoot } from "react-dom/client";
import { NavigationProvider } from "./contexts/NavigationContext";
import { DEMO_STUDENT_UID } from "./data/devStudent";
import { DEMO_PROFILE } from "./components/landing/glass/demoProfile";
import type { UserSettings } from "./types";
import "./index.css";
import "./components/landing/landing.css";
import PaperAnswerDemo from "./components/landing/glass/PaperAnswerDemo";
import PreviewReady, { PREVIEW_PLAYBACK } from "./components/landing/glass/PreviewReady";

const Launchpad = React.lazy(() => import("./components/InnovationZone"));
const ActiveRecall = React.lazy(
  () => import("./components/MasteringActiveRecallModule"),
);
const params = new URLSearchParams(window.location.search);
const view = params.get("view") ?? "papertrail";
const settings: UserSettings = {
  language: "en",
  avatar: "",
  darkMode: false,
  cardStyle: "default",
  defaultWorkMinutes: 25,
  showDashboard: false,
};
const progress = { unlockedSection: 1 };
const noop = () => undefined;

/** A short tour of real controls. Contained in its own document so module
 * focus, Launchpad navigation and scrolling never move the landing page. */
function Tour({ kind }: { kind: "launchpad" | "module" }) {
  const host = useRef<HTMLDivElement>(null);
  useEffect(() => {
    let settlingTimer = 0;
    let step = 0,
      playing = !matchMedia("(prefers-reduced-motion: reduce)").matches;
    const steps =
      kind === "launchpad"
        ? [
            "All",
            "scroll",
            "Understand",
            "scroll",
            "Practice",
            "scroll",
            "Plan",
            "Track",
          ]
        : [
            "Passive Review",
            "Active Recall",
            "Passive Review",
            "Active Recall",
          ];
    const positionExperiment = (
      target: HTMLElement,
      behavior: ScrollBehavior,
    ) => {
      const card = target.closest<HTMLElement>(".my-10") ?? target;
      let scroller = card.parentElement;
      while (
        scroller &&
        !/auto|scroll/.test(getComputedStyle(scroller).overflowY)
      )
        scroller = scroller.parentElement;
      if (scroller)
        scroller.scrollTo({
          top:
            scroller.scrollTop +
            card.getBoundingClientRect().top -
            scroller.getBoundingClientRect().top -
            55,
          behavior,
        });
      else
        window.scrollTo({
          top: card.getBoundingClientRect().top + scrollY - 65,
          behavior,
        });
    };
    // The experiment is the first frame, including when motion is disabled.
    const prepare = () => {
      const button = [
        ...(host.current?.querySelectorAll<HTMLButtonElement>("button") ?? []),
      ].find((b) => b.textContent?.trim() === "Passive Review");
      if (kind !== "module" || !button) return;
      observer.disconnect();
      host.current
        ?.querySelector<HTMLButtonElement>(
          '[aria-label="Collapse module navigation"]',
        )
        ?.click();
      positionExperiment(button, "instant");
      settlingTimer = window.setTimeout(
        () => positionExperiment(button, "instant"),
        400,
      );
    };
    const observer = new MutationObserver(prepare);
    if (kind === "module" && host.current) {
      observer.observe(host.current, { childList: true, subtree: true });
      prepare();
    }
    const tick = () => {
      if (!playing || document.hidden || !host.current) return;
      const next = steps[step % steps.length];
      if (next === "scroll") window.scrollBy({ top: 350, behavior: "smooth" });
      else {
        const selector = kind === "launchpad" ? '[role="tab"]' : "button";
        const target = [
          ...host.current.querySelectorAll<HTMLButtonElement>(selector),
        ].find((b) => b.textContent?.trim() === next);
        if (!target) return;
        if (kind === "module") positionExperiment(target, "smooth");
        else window.scrollTo({ top: 0, behavior: "smooth" });
        target.click();
      }
      step++;
    };
    const timer = window.setInterval(tick, 3200);
    const playback = (e: MessageEvent) => {
      if (
        e.origin === location.origin &&
        e.source === parent &&
        e.data?.type === PREVIEW_PLAYBACK
      )
        playing = !!e.data.playing;
    };
    window.addEventListener("message", playback);
    return () => {
      observer.disconnect();
      clearInterval(timer);
      clearTimeout(settlingTimer);
      window.removeEventListener("message", playback);
    };
  }, [kind]);
  return (
    <div ref={host}>
      <Suspense fallback={<p className="p-6">Opening the app…</p>}>
        <PreviewReady />
        {kind === "launchpad" ? (
          <NavigationProvider>
            <Launchpad
              onBack={noop}
              user={{
                uid: DEMO_STUDENT_UID,
                yearGroup: "6th",
                curriculumLevel: "senior",
              }}
              initialSubjectProfile={DEMO_PROFILE}
              settings={settings}
              updateSetting={noop}
            />
          </NavigationProvider>
        ) : (
          <ActiveRecall
            onBack={noop}
            progress={progress}
            onProgressUpdate={noop}
          />
        )}
      </Suspense>
    </div>
  );
}
createRoot(document.getElementById("root")!).render(
  view === "innovation-zone" ? (
    <Tour kind="launchpad" />
  ) : view === "module" ? (
    <Tour kind="module" />
  ) : (
    <PaperAnswerDemo />
  ),
);
