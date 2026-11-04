import React, { Suspense, useState } from "react";
import PreviewReady from "./PreviewReady";
import { PAPER_TRAIL_INDEX } from "../../../paperTrailData";
import {
  paperAnswersPath,
  paperStoragePath,
  paperUrl,
} from "../../PaperTrail/storage";
const Viewer = React.lazy(() => import("../../PaperTrail/Viewer"));

// Biology 2024 has a short, single-page first question and a compact verified
// scheme crop. Both documents and their map use the main app's corpus.
const entry = PAPER_TRAIL_INDEX.biology.find(
  (e) => e.year === 2024 && e.level === "higher" && e.lang === "ev",
)!;
const paper = entry.papers.find((p) => p.doc.f === "LC025ALP038EV.pdf")!;
export default function PaperAnswerDemo() {
  const [open, setOpen] = useState(true);
  return open ? (
    <Suspense fallback={<p className="p-6">Opening Biology 2024…</p>}>
      <PreviewReady />
      <Viewer
        title="Biology · 2024"
        subtitle="Section A&B · Higher"
        paper={{
          url: paperUrl(
            paperStoragePath("lc", "biology", 2024, "paper", paper.doc.f),
          ),
          label: "Section A&B",
          bytes: paper.doc.b,
        }}
        scheme={{
          url: paperUrl(
            paperStoragePath("lc", "biology", 2024, "scheme", paper.scheme!.f),
          ),
          label: "Marking scheme",
          bytes: paper.scheme!.b,
        }}
        answersUrl={paperUrl(
          paperAnswersPath("lc", "biology", 2024, paper.doc.f),
        )}
        initialPaperPage={3}
        initialAnswersOn
        onClose={() => setOpen(false)}
      />
    </Suspense>
  ) : (
    <div className="p-8 text-center">
      <p className="mb-5">Biology · 2024 · Higher level</p>
      <button
        className="rounded-lg bg-orange-500 px-5 py-3 text-black"
        onClick={() => setOpen(true)}
      >
        Open the paper again
      </button>
    </div>
  );
}
