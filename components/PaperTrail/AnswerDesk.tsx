import React, { useState } from "react";
import {
  ArrowRight,
  Check,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Download,
  Eye,
  EyeOff,
  Hand,
  Highlighter,
  Keyboard,
  NotebookPen,
  PenLine,
  Undo2,
  Eraser,
  Minus,
  Plus,
} from "lucide-react";
import KobraScope, { Button, Textarea } from "../approved-ui-runtime";
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
            <Button
              variant="outline"
              aria-pressed={p.inkView === view}
              onClick={() => p.onInkView(view)}
            >
              View {view === "first" ? "first" : "second"} attempt on paper
            </Button>
          )}
        </div>
      )}
    </section>
  );
  const next = p.questions[p.questions.findIndex((q) => q.n === p.id) + 1];
  return (
    <aside
      className="ad-pane"
      id="paper-answer-drawer"
      data-collapsed={p.collapsed || undefined}
      aria-label="Your answer desk"
    >
      <KobraScope className="ad-scope" sound={false}>
        <header className="ad-header">
          <div>
            <p className="ad-eyebrow">YOUR ANSWER DESK</p>
            <h2>Your work comes first.</h2>
          </div>
          {p.collapsed && r.mode === "ink" && r.phase !== "done" && (
            <Button
              variant="outline"
              className="ad-mobile-tool"
              aria-label={p.tool === "move" ? "Use pen" : "Move page"}
              onClick={() => p.onTool(p.tool === "move" ? "pen" : "move")}
            >
              {p.tool === "move" ? <PenLine size={17} /> : <Hand size={17} />}
            </Button>
          )}
          <Button
            variant="outline"
            className="ad-collapse"
            aria-label={
              p.collapsed ? "Expand answer desk" : "Minimise answer desk"
            }
            aria-expanded={!p.collapsed}
            onClick={p.onCollapse}
          >
            {p.wide ? (
              p.collapsed ? (
                <ChevronLeft size={17} />
              ) : (
                <ChevronRight size={17} />
              )
            ) : (
              <ChevronDown size={17} />
            )}
          </Button>
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
            <Button
              variant="outline"
              size="icon"
              aria-label="Download my work"
              onClick={download}
            >
              <Download size={16} />
            </Button>
          </div>
          {!p.questions.length && (
            <div className="ad-unmapped">
              <p>
                Question links aren’t available for this paper. Keep an attempt
                against a page and open the full scheme when ready.
              </p>
              {p.id !== `page:${p.page}` && (
                <Button
                  variant="outline"
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
                <span>0{i + 1}</span>
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
                    { id: "type", label: "Type", Icon: Keyboard },
                    { id: "ink", label: "Write on paper", Icon: PenLine },
                    { id: "copybook", label: "Copybook", Icon: NotebookPen },
                  ] as const
                ).map(({ id, label, Icon }) => (
                  <Button
                    variant="outline"
                    key={id}
                    aria-pressed={r.mode === id}
                    onClick={() => {
                      write({ mode: id });
                      if (id === "ink") p.onTool("pen");
                    }}
                  >
                    <Icon size={15} />
                    {label}
                  </Button>
                ))}
              </div>
              {r.mode === "ink" ? (
                <p className="ad-intro">
                  Write on the exam page. Use Move page to scroll without
                  drawing.
                </p>
              ) : (
                <>
                  <label className="ad-label" htmlFor="answer-desk-text">
                    {r.mode === "copybook"
                      ? "A note to find your work"
                      : r.phase === "retry"
                        ? "Your second attempt"
                        : "Your attempt"}
                  </label>
                  <Textarea
                    id="answer-desk-text"
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
                </>
              )}
              {r.phase === "attempt" && (
                <fieldset className="ad-confidence">
                  <legend>
                    How sure are you? <span>Optional</span>
                  </legend>
                  <div>
                    {["Finding my way", "Nearly there", "Confident"].map(
                      (value) => (
                        <Button
                          variant="outline"
                          key={value}
                          aria-pressed={r.confidence === value}
                          onClick={() => write({ confidence: value })}
                        >
                          {value}
                        </Button>
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
                <Button
                  variant="outline"
                  size="icon"
                  key={id}
                  aria-label={label}
                  aria-pressed={p.tool === id}
                  onClick={() => p.onTool(id)}
                >
                  <Icon size={17} />
                </Button>
              ))}
              <Button
                variant="outline"
                size="icon"
                disabled={!p.canUndo}
                aria-label="Undo last stroke on this page"
                onClick={p.onUndo}
              >
                <Undo2 size={17} />
              </Button>
              <span>Page {p.page}</span>
            </div>
          )}
          {r.phase === "attempt" && (
            <div className="ad-next">
              <p>
                <EyeOff size={14} />
                Scheme hidden until you choose to reveal.
              </p>
              <Button disabled={!p.hasScheme} onClick={p.onReveal}>
                Keep my attempt & reveal <ArrowRight size={16} />
              </Button>
              {!p.hasScheme && (
                <p>No marking scheme is linked to this document.</p>
              )}
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
                    <Button
                      variant="outline"
                      size="icon"
                      aria-label="Smaller scheme"
                      disabled={schemeZoom <= 1}
                      onClick={() =>
                        setSchemeZoom((z) => Math.max(1, z - 0.25))
                      }
                    >
                      <Minus size={14} />
                    </Button>
                    <Button
                      variant="outline"
                      size="icon"
                      aria-label="Larger scheme"
                      disabled={schemeZoom >= 2}
                      onClick={() =>
                        setSchemeZoom((z) => Math.min(2, z + 0.25))
                      }
                    >
                      <Plus size={14} />
                    </Button>
                  </div>
                  {p.schemeErrored ? (
                    <>
                      <p>
                        Couldn’t load the scheme. Your attempt is still here.
                      </p>
                      <Button variant="outline" onClick={p.onRetryScheme}>
                        Try loading the scheme again
                      </Button>
                    </>
                  ) : question?.mode === "pagejump" ? (
                    <Button variant="outline" onClick={p.onFullScheme}>
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
                  <Button variant="outline" onClick={p.onHide}>
                    <EyeOff size={14} />
                    Hide scheme
                  </Button>
                </section>
              ) : (
                <Button
                  variant="outline"
                  className="ad-reopen"
                  onClick={p.onReveal}
                >
                  <Eye size={15} />
                  Reopen the marking scheme
                </Button>
              )}
              <label className="ad-label" htmlFor="answer-desk-correction">
                One thing to take into the next attempt.
              </label>
              <Textarea
                id="answer-desk-correction"
                maxLength={50000}
                value={r.correction}
                onChange={(e) => write({ correction: e.target.value })}
                placeholder="What was missing, or what would you do differently?"
              />
              <Button
                variant="outline"
                className="ad-correct-ink"
                onClick={() => {
                  write({ mode: "ink" });
                  p.onTool("pen");
                }}
              >
                Add a correction on the paper <PenLine size={15} />
              </Button>
              <div className="ad-next">
                <p>
                  Your original stays intact. The next attempt starts fresh.
                </p>
                <Button
                  onClick={() => {
                    write({ phase: "retry" });
                    p.onHide();
                  }}
                >
                  Try again without the scheme <ArrowRight size={16} />
                </Button>
              </div>
            </>
          )}
          {r.phase === "retry" && (
            <div className="ad-next">
              <p>
                <EyeOff size={14} />
                Scheme and comparison hidden.
              </p>
              <Button
                onClick={() => {
                  write({ phase: "done" });
                  p.onHide();
                }}
              >
                Keep both attempts <Check size={16} />
              </Button>
              <Button
                variant="outline"
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
                variant="outline"
                onClick={() => write({ phase: "compare" })}
              >
                Reopen my comparison
              </Button>
              {next && (
                <Button
                  className="ad-next-question"
                  onClick={() => p.onQuestion(next.n)}
                >
                  Next question <ArrowRight size={16} />
                </Button>
              )}
            </>
          )}
        </div>
      </KobraScope>
    </aside>
  );
}
