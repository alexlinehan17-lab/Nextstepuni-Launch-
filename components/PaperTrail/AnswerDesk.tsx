import React, { useState } from "react";
import {
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Download,
  EyeOff,
  Hand,
  Highlighter,
  PenLine,
  Undo2,
  Eraser,
  Minus,
  Plus,
} from "lucide-react";
import { Button, IconButton } from "../ui/Button";
import { ChoiceTile } from "../ui/Choice";
import { AreaField } from "../ui/Field";
import CropView from "./CropView";
import { schemeRegionFor } from "./paperRegion";
import {
  answerCopy,
  type AnswerRecord,
  type WrittenResponse,
} from "./answerDeskStore";
import type { InkTool } from "./AnswerInk";
import type { PaperAnswerQuestion } from "../../types/paperTrail";
import type { PDFDocumentProxy } from "pdfjs-dist";
import "./answer-desk.css";
interface Props {
  title: string;
  id: string;
  questions: PaperAnswerQuestion[];
  page: number;
  record: AnswerRecord;
  problem?: string;
  onChange: (update: (r: AnswerRecord) => AnswerRecord) => void;
  onQuestion: (id: string) => void;
  onReveal: () => void;
  onHide: () => void;
  schemeVisible: boolean;
  hasScheme: boolean;
  schemePdf: PDFDocumentProxy | null;
  schemeErrored: boolean;
  onRetryScheme: () => void;
  onFullScheme: () => void;
  tool: InkTool;
  onTool: (tool: InkTool) => void;
  onUndo: () => void;
  canUndo: boolean;
  collapsed: boolean;
  wide: boolean;
  onCollapse: () => void;
  inkView: "first" | "retry";
  onInkView: (view: "first" | "retry") => void;
}
export default function AnswerDesk(p: Props) {
  const [schemeZoom, setSchemeZoom] = useState(1);
  const r = p.record;
  const question = p.questions.find((q) => q.n === p.id);
  const label =
    question?.label ??
    (p.id.startsWith("page:") ? `Page ${p.id.slice(5)}` : `Question ${p.id}`);
  const write = (patch: Partial<AnswerRecord>) =>
    p.onChange((old) => ({ ...old, ...patch }));
  const editing = r.phase === "attempt" || r.phase === "retry";
  const response = r.phase === "retry" ? r.retry : r.draft;
  const setText = (text: string) =>
    p.onChange((old) => ({
      ...old,
      [old.phase === "retry" ? "retry" : "draft"]: {
        ...(old.phase === "retry" ? old.retry : old.draft),
        text,
      },
    }));
  const download = () => {
    const url = URL.createObjectURL(
      new Blob([answerCopy(p.title, label, r)], {
        type: "text/html;charset=utf-8",
      }),
    );
    const a = document.createElement("a");
    a.href = url;
    a.download = "nextstepuni-my-attempt.html";
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  };
  const glyph = (Icon: typeof PenLine, size: 20 | 24 = 20) => (
    <Icon className="ui-icon" width={size} height={size} strokeWidth={1.75} aria-hidden="true" focusable="false" />
  );
  // Work kept from an earlier step: on the page under a small label, not in a box.
  const captured = (
    title: string,
    value: WrittenResponse,
    view?: "first" | "retry",
  ) => (
    <section className="ad-kept">
      <span className="ad-eyebrow">{title}</span>
      <p className="ad-response-text">{value.text || "No typed response."}</p>
      {Object.values(value.ink).some((x) => x.length > 0) && (
        <div>
          <p className="ad-fine">
            Handwriting is kept on the paper beside this answer.
          </p>
          {view && (
            <ChoiceTile
              compact
              kind="toggle"
              chosen={p.inkView === view}
              onClick={() => p.onInkView(view)}
              label={`View ${view === "first" ? "first" : "second"} attempt on paper`}
            />
          )}
        </div>
      )}
    </section>
  );
  const currentIndex = p.questions.findIndex((q) => q.n === p.id);
  const next = currentIndex < 0 ? undefined : p.questions[currentIndex + 1];
  return (
    <aside
      className="ad-pane"
      id="paper-answer-drawer"
      data-collapsed={p.collapsed || undefined}
      aria-label="Your answer desk"
    >
      <div className="ad-scope ui-part">
        <header className="ad-header">
          <div>
            <p className="ad-eyebrow">YOUR ANSWER DESK</p>
            <h2>Your work comes first.</h2>
          </div>
          {p.collapsed && r.mode === "ink" && r.phase !== "done" && (
            <IconButton
              className="ad-mobile-tool"
              label={p.tool === "move" ? "Use pen" : "Move page"}
              onClick={() => p.onTool(p.tool === "move" ? "pen" : "move")}
              icon={p.tool === "move" ? glyph(PenLine) : glyph(Hand)}
            />
          )}
          <IconButton
            className="ad-collapse"
            label={
              p.collapsed ? "Expand answer desk" : "Minimise answer desk"
            }
            aria-expanded={!p.collapsed}
            onClick={p.onCollapse}
            icon={p.wide ? (
              p.collapsed ? (
                glyph(ChevronLeft, 24)
              ) : (
                glyph(ChevronRight, 24)
              )
            ) : (
              glyph(ChevronDown, 24)
            )}
          />
        </header>
        {p.collapsed && <span className="ad-rail-label">Answer desk</span>}
        <div className="ad-content" hidden={p.collapsed}>
          <div className="ad-question">
            <label htmlFor="answer-desk-question">Working on</label>
            <select
              id="answer-desk-question"
              value={p.id}
              onChange={(e) => p.onQuestion(e.target.value)}
            >
              {!question && <option value={p.id}>{label}</option>}
              {p.questions.map((q) => (
                <option key={q.n} value={q.n}>
                  {q.label ?? `Question ${q.n}`}
                </option>
              ))}
            </select>
            <IconButton
              label="Download my work"
              onClick={download}
              icon={glyph(Download)}
            />
          </div>
          {!p.questions.length && (
            <div className="ad-unmapped">
              <p>
                Question links aren’t available for this paper. Keep an attempt
                against a page and open the full scheme when ready.
              </p>
              {p.id !== `page:${p.page}` && (
                <Button
                  onClick={() => p.onQuestion(`page:${p.page}`)}
                >
                  Work on page {p.page}
                </Button>
              )}
            </div>
          )}
          <ol className="ad-steps" aria-label="Attempt progress">
            {["attempt", "compare", "retry"].map((phase, i) => (
              <li
                key={phase}
                aria-current={
                  (r.phase === "done" ? "retry" : r.phase) === phase
                    ? "step"
                    : undefined
                }
              >
                <span className="ui-readout">0{i + 1}</span>
                {["Attempt", "Compare", "Try again"][i]}
              </li>
            ))}
          </ol>
          {p.problem ? (
            <p role="alert" className="ad-save-error">
              {p.problem}
            </p>
          ) : (
            <p className="ad-save-status" role="status">
              {r.updatedAt
                ? "Saved for this sign-in"
                : "Auto-saves during this sign-in"}{" "}
              · download to keep a copy after signing out
            </p>
          )}
          {editing && (
            <>
              <div className="ad-modes" role="group" aria-label="How to answer">
                {(
                  [
                    { id: "type", label: "Type" },
                    { id: "ink", label: "Write on paper" },
                    { id: "copybook", label: "Copybook" },
                  ] as const
                ).map(({ id, label }) => (
                  <ChoiceTile
                    compact
                    kind="toggle"
                    key={id}
                    chosen={r.mode === id}
                    onClick={() => {
                      write({ mode: id });
                      if (id === "ink") p.onTool("pen");
                    }}
                    label={label}
                  />
                ))}
              </div>
              {r.mode === "ink" ? (
                <p className="ad-intro">
                  Write on the exam page. Use Move page to scroll without
                  drawing.
                </p>
              ) : (
                <AreaField
                  className="ad-answer"
                  id="answer-desk-text"
                  label={
                    r.mode === "copybook"
                      ? "A note to find your work"
                      : r.phase === "retry"
                        ? "Your second attempt"
                        : "Your attempt"
                  }
                  value={response.text}
                  maxLength={50000}
                  onChange={(e) => setText(e.target.value)}
                  placeholder={
                    r.mode === "copybook"
                      ? "e.g. Blue copybook, page 18. Your actual answer can stay on paper."
                      : r.phase === "retry"
                        ? "Have another go, with the scheme hidden…"
                        : "A first step, a full answer, or anything in between…"
                  }
                />
              )}
              {r.phase === "attempt" && (
                <fieldset className="ad-confidence">
                  <legend>
                    How sure are you? <span>Optional</span>
                  </legend>
                  <div>
                    {["Finding my way", "Nearly there", "Confident"].map(
                      (value) => (
                        <ChoiceTile
                          compact
                          kind="toggle"
                          key={value}
                          chosen={r.confidence === value}
                          onClick={() => write({ confidence: value })}
                          label={value}
                        />
                      ),
                    )}
                  </div>
                </fieldset>
              )}
            </>
          )}
          {r.mode === "ink" && r.phase !== "done" && (
            <div
              className="ad-ink-tools"
              role="group"
              aria-label="Handwriting tools"
            >
              {(
                [
                  { id: "pen", label: "Pen", Icon: PenLine },
                  { id: "highlight", label: "Highlight", Icon: Highlighter },
                  { id: "erase", label: "Eraser", Icon: Eraser },
                  { id: "move", label: "Move page", Icon: Hand },
                ] as const
              ).map(({ id, label, Icon }) => (
                <ChoiceTile
                  compact
                  kind="toggle"
                  key={id}
                  aria-label={label}
                  chosen={p.tool === id}
                  onClick={() => p.onTool(id)}
                  label={glyph(Icon)}
                />
              ))}
              <IconButton
                aria-disabled={!p.canUndo || undefined}
                label="Undo last stroke on this page"
                onClick={() => { if (p.canUndo) p.onUndo(); }}
                icon={glyph(Undo2)}
              />
              <span className="ui-readout">Page {p.page}</span>
            </div>
          )}
          {r.phase === "attempt" && (
            <div className="ad-next">
              <p>
                <EyeOff size={16} aria-hidden="true" />
                Scheme hidden until you choose to reveal.
              </p>
              <Button kind="main" block arrow="forward" onClick={p.onReveal}
                unavailable={p.hasScheme ? undefined : "No marking scheme is linked to this document."}>
                Keep my attempt & reveal
              </Button>
              <small>Using a copybook? You can reveal without typing.</small>
            </div>
          )}
          {r.phase === "compare" && (
            <>
              {captured("BEFORE THE REVEAL", r.first ?? r.draft)}
              {r.confidence && (
                <p className="ad-fine">
                  You felt: {r.confidence.toLowerCase()}
                </p>
              )}
              {p.schemeVisible ? (
                <section className="ad-scheme">
                  <div className="ad-scheme-top">
                    <span className="ad-eyebrow">SEC MARKING SCHEME</span>
                    <span className="pv-zoom" role="group" aria-label="Scheme size">
                      <IconButton
                        label="Smaller scheme"
                        aria-disabled={schemeZoom <= 1 || undefined}
                        onClick={() => {
                          if (schemeZoom > 1) setSchemeZoom((z) => Math.max(1, z - 0.25));
                        }}
                        icon={glyph(Minus)}
                      />
                      <IconButton
                        label="Larger scheme"
                        aria-disabled={schemeZoom >= 2 || undefined}
                        onClick={() => {
                          if (schemeZoom < 2) setSchemeZoom((z) => Math.min(2, z + 0.25));
                        }}
                        icon={glyph(Plus)}
                      />
                    </span>
                  </div>
                  {p.schemeErrored ? (
                    <>
                      <p>
                        Couldn’t load the scheme. Your attempt is still here.
                      </p>
                      <Button onClick={p.onRetryScheme}>
                        Try loading the scheme again
                      </Button>
                    </>
                  ) : question?.mode === "pagejump" ? (
                    <Button onClick={p.onFullScheme}>
                      Open the scheme at this question
                    </Button>
                  ) : p.schemePdf && question ? (
                    <div className="ad-scheme-crop">
                      <CropView
                        pdf={p.schemePdf}
                        region={schemeRegionFor(question)}
                        trim
                        responsive
                        zoom={schemeZoom}
                      />
                    </div>
                  ) : (
                    <p role="status">Loading the marking scheme…</p>
                  )}
                  <Button size="sm" onClick={p.onHide}>
                    Hide scheme
                  </Button>
                </section>
              ) : (
                <Button
                  className="ad-reopen"
                  onClick={p.onReveal}
                >
                  Reopen the marking scheme
                </Button>
              )}
              <AreaField
                className="ad-answer"
                id="answer-desk-correction"
                label="One thing to take into the next attempt."
                maxLength={50000}
                value={r.correction}
                onChange={(e) => write({ correction: e.target.value })}
                placeholder="What was missing, or what would you do differently?"
              />
              <Button
                className="ad-correct-ink"
                onClick={() => {
                  write({ mode: "ink" });
                  p.onTool("pen");
                }}
              >
                Add a correction on the paper
              </Button>
              <div className="ad-next">
                <p>
                  Your original stays intact. The next attempt starts fresh.
                </p>
                <Button
                  kind="main"
                  block
                  arrow="forward"
                  onClick={() => {
                    write({ phase: "retry" });
                    p.onHide();
                  }}
                >
                  Try again without the scheme
                </Button>
                {next && (
                  <Button block arrow="forward" onClick={() => p.onQuestion(next.n)}>
                    Move to next question
                  </Button>
                )}
              </div>
            </>
          )}
          {r.phase === "retry" && (
            <div className="ad-next">
              <p>
                <EyeOff size={16} aria-hidden="true" />
                Scheme and comparison hidden.
              </p>
              <Button
                kind="main"
                block
                onClick={() => {
                  write({ phase: "done" });
                  p.onHide();
                }}
              >
                Keep both attempts
              </Button>
              <Button
                block
                onClick={() => {
                  write({ phase: "compare" });
                  p.onReveal();
                }}
              >
                Look back at my comparison
              </Button>
            </div>
          )}
          {r.phase === "done" && (
            <>
              <h3 className="ad-done-title">
                Two attempts.
                <br />A clearer picture.
              </h3>
              {captured("FIRST ATTEMPT", r.first ?? r.draft, "first")}
              {captured("SECOND ATTEMPT", r.retry, "retry")}
              {r.correction && (
                <div className="ad-reflection">
                  <span className="ad-eyebrow">WHAT I NOTICED</span>
                  <p>{r.correction}</p>
                </div>
              )}
              <Button
                block
                onClick={() => write({ phase: "compare" })}
              >
                Reopen my comparison
              </Button>
              {next && (
                <Button
                  kind="main"
                  block
                  arrow="forward"
                  className="ad-next-question"
                  onClick={() => p.onQuestion(next.n)}
                >
                  Next question
                </Button>
              )}
            </>
          )}
        </div>
      </div>
    </aside>
  );
}
