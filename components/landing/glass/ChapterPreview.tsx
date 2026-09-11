import React, { useRef, useState } from "react";
import { useInView, useReducedMotion } from "framer-motion";
import { Pause, Play } from "lucide-react";
import ScaledSurface from "./ScaledSurface";
import { FONT, L } from "../theme";

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
  const playback = (next: boolean) => {
    setPlaying(next);
    frame.current?.contentWindow?.postMessage(
      { type: "landing-preview-playback", playing: next },
      window.location.origin,
    );
  };
  return (
    <div ref={host} data-lenis-prevent>
      <ScaledSurface width={820} height={c.height}>
        {visible && (
          <iframe
            ref={frame}
            title={c.title}
            src={`/landing-demo.html?view=${c.view}`}
            width={820}
            height={c.height}
            onLoad={() =>
              frame.current?.contentWindow?.postMessage(
                { type: "landing-preview-playback", playing },
                window.location.origin,
              )
            }
            tabIndex={interactive ? 0 : -1}
            aria-hidden={interactive ? undefined : true}
            style={{
              border: 0,
              display: "block",
              width: 820,
              height: c.height,
              background: "#fff",
              pointerEvents: interactive ? "auto" : "none",
            }}
          />
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
            onClick={() => playback(!playing)}
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
