import React, { useEffect, useRef, useState } from "react";
import { useInView, useReducedMotion } from "framer-motion";
import { Pause, Play } from "lucide-react";
import ScaledSurface from "./ScaledSurface";
import { FONT, L } from "../theme";
import { PREVIEW_PLAYBACK, PREVIEW_READY } from "./PreviewReady";

const CONFIG = {
  papertrail: {
    view: "papertrail",
    title: "Biology 2024 — interactive Paper Trail",
    height: 850,
    caption: "Try it: click the orange-edged Mark scheme ribbon on Question 1.",
  },
  launchpad: {
    view: "innovation-zone",
    title: "Launchpad — tools and categories tour",
    height: 720,
    caption: "A tour of the Launchpad’s tools and categories.",
  },
  lab: {
    view: "module",
    title: "Mastering Active Recall — memory strength experiment",
    height: 680,
    caption: "Inside a module: compare passive review with active recall.",
  },
} as const;
export default function ChapterPreview({ id }: { id: keyof typeof CONFIG }) {
  const c = CONFIG[id],
    interactive = id === "papertrail";
  const host = useRef<HTMLDivElement>(null),
    frame = useRef<HTMLIFrameElement>(null);
  const visible = useInView(host, { amount: 0.1, margin: "120px 0px" });
  const reduce = useReducedMotion();
  const [playing, setPlaying] = useState(!reduce);
  const [status, setStatus] = useState<"loading" | "ready" | "error">("loading");
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    if (!visible) return;
    setStatus("loading");
    const timeout = window.setTimeout(() => setStatus("error"), 20_000);
    const ready = (event: MessageEvent) => {
      if (event.origin !== window.location.origin ||
          event.source !== frame.current?.contentWindow ||
          event.data?.type !== PREVIEW_READY) return;
      clearTimeout(timeout);
      setStatus("ready");
    };
    window.addEventListener("message", ready);
    return () => {
      clearTimeout(timeout);
      window.removeEventListener("message", ready);
    };
  }, [visible, attempt]);

  useEffect(() => {
    if (!("serviceWorker" in navigator)) return;
    // An updated worker can repair a previously blocked iframe without
    // reloading the page or losing the reader's scroll position.
    const recover = () => setAttempt(value => value + 1);
    navigator.serviceWorker.addEventListener("controllerchange", recover);
    return () => navigator.serviceWorker.removeEventListener("controllerchange", recover);
  }, []);

  useEffect(() => {
    if (status !== "ready") return;
    frame.current?.contentWindow?.postMessage(
      { type: PREVIEW_PLAYBACK, playing },
      window.location.origin,
    );
  }, [playing, status]);

  return (
    <div ref={host} data-lenis-prevent data-preview-status={status}>
      <ScaledSurface width={820} height={c.height}>
        {visible && (
          <iframe
            key={attempt}
            ref={frame}
            title={c.title}
            src={`/landing-demo.html?view=${c.view}`}
            width={820}
            height={c.height}
            onError={() => setStatus("error")}
            tabIndex={interactive && status === "ready" ? 0 : -1}
            aria-hidden={interactive && status === "ready" ? undefined : true}
            style={{
              border: 0,
              display: "block",
              width: 820,
              height: c.height,
              background: "#fff",
              opacity: status === "ready" ? 1 : 0,
              pointerEvents: interactive && status === "ready" ? "auto" : "none",
            }}
          />
        )}
        {visible && status !== "ready" && (
          <div
            role={status === "error" ? "alert" : "status"}
            style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 20, padding: 32, background: L.paper, color: L.ink, fontFamily: FONT.sans, fontSize: 22, textAlign: "center" }}
          >
            <p style={{ margin: 0 }}>{status === "error" ? "This preview couldn’t load." : "Opening preview…"}</p>
            {status === "error" && (
              <button
                type="button"
                onClick={() => setAttempt(value => value + 1)}
                style={{ padding: "12px 24px", border: 0, borderRadius: 999, background: L.ink, color: L.paper, fontFamily: FONT.sans, fontSize: 20, cursor: "pointer" }}
              >Try again</button>
            )}
          </div>
        )}
      </ScaledSurface>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 12,
          padding: "12px 14px",
          borderTop: `1px solid ${L.hairline}`,
          fontFamily: FONT.sans,
          fontSize: 12,
          lineHeight: 1.5,
          color: L.muted,
        }}
      >
        <p style={{ margin: 0 }}>{c.caption}</p>
        {!interactive && (
          <button
            type="button"
            aria-label={`${playing ? "Pause" : "Play"} ${id === "lab" ? "Learning Lab" : "Launchpad"} preview`}
            onClick={() => setPlaying(!playing)}
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              minWidth: 40,
              minHeight: 40,
              border: `1px solid ${L.hairline}`,
              borderRadius: 7,
              background: "#fff",
              color: L.ink,
              cursor: "pointer",
            }}
          >
            {playing ? <Pause size={16} /> : <Play size={16} />}
          </button>
        )}
      </div>
    </div>
  );
}
