import React, { useEffect, useMemo, useRef, useState } from "react";
import {
  ArrowRight,
  BarChart3,
  Check,
  HelpCircle,
  RotateCcw,
  Share2,
  X,
} from "lucide-react";
import Nav from "../landing/sections/Nav";
import CertleCompanion from "./CertleCompanion";
import { CertleLogo, MarksBoard } from "./CertleIdentity";
import ShareResult from "./ShareResult";
import { resultShareData } from "./sharing";
import {
  dublinDay,
  formatDay,
  nextDublinMidnight,
  questionNumber,
} from "../landing/fx-e/dublin";
import {
  MAX_ATTEMPTS,
  POOL_URL,
  schemePoints,
  type CertlePool,
  type CertleQuestion,
} from "./data";
import {
  bestResult,
  GAME_KEY,
  loadStats,
  readStored,
  recordResult,
  restoreGame,
  resultsFor,
  saveStored,
  STATS_KEY,
  statsSummary,
  submitAnswer,
  type Game,
  type Stats,
} from "./game";

function Modal({
  open,
  title,
  onClose,
  children,
}: {
  open: boolean;
  title: string;
  onClose: () => void;
  children: React.ReactNode;
}) {
  const ref = useRef<HTMLDialogElement>(null);
  useEffect(() => {
    const dialog = ref.current;
    if (!dialog) return;
    if (open && !dialog.open) dialog.showModal();
    else if (!open && dialog.open) dialog.close();
  }, [open]);
  return (
    <dialog
      ref={ref}
      className="certle-dialog"
      aria-label={title}
      onCancel={onClose}
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div className="certle-dialog-heading">
        <h2>{title}</h2>
        <button
          type="button"
          className="certle-icon-button"
          aria-label={`Close ${title}`}
          onClick={onClose}
        >
          <X size={20} />
        </button>
      </div>
      {children}
    </dialog>
  );
}
const draftKey = (day: string, id: string) =>
  `nextstepuni.certle.draft:${day}:${id}`;
const plural = (count: number, word: string) =>
  `${count} ${word}${count === 1 ? "" : "s"}`;

export default function CertlePage() {
  const [now, setNow] = useState(() => new Date());
  const day = dublinDay(now),
    n = questionNumber(day);
  const midnight = useMemo(() => nextDublinMidnight(new Date()), [day]);
  const seconds = Math.max(0, Math.ceil((midnight - now.getTime()) / 1000));
  const countdown = [
    Math.floor(seconds / 3600),
    Math.floor((seconds % 3600) / 60),
    seconds % 60,
  ]
    .map((v) => String(v).padStart(2, "0"))
    .join(":");
  const [pool, setPool] = useState<CertleQuestion[]>([]),
    [failed, setFailed] = useState(false),
    [reload, setReload] = useState(0);
  const [game, setGame] = useState<Game | null>(null),
    [answer, setAnswer] = useState("");
  const [stats, setStats] = useState<Stats>(() => loadStats());
  const [dialog, setDialog] = useState<"help" | "stats" | "share" | null>(null),
    [notice, setNotice] = useState(""),
    [localOnly, setLocalOnly] = useState(false);
  const field = useRef<HTMLTextAreaElement>(null);
  const entry = pool.length ? pool[(n - 1) % pool.length] : null;
  const ready = !!entry && game?.day === day && game.id === entry.id;
  const results = useMemo(
    () => (ready ? resultsFor(game!, entry!) : []),
    [ready, game, entry],
  );
  const best = bestResult(results),
    total = entry?.points.reduce((s, p) => s + p.marks, 0) ?? 0;
  const summary = statsSummary(stats, day);
  const remaining = MAX_ATTEMPTS - (ready ? game!.answers.length : 0);
  const finished = ready && game!.finished;
  const bestIndex = best ? results.indexOf(best) : -1;
  const shareData = useMemo(
    () => (finished && game && entry ? resultShareData(n, game, entry) : null),
    [finished, game, entry, n],
  );
  const resultHeading = useRef<HTMLHeadingElement>(null);
  const previousFinished = useRef(false);
  useEffect(() => {
    if (finished && !previousFinished.current)
      resultHeading.current?.focus({ preventScroll: true });
    previousFinished.current = finished;
  }, [finished]);

  useEffect(() => {
    const tick = () => setNow(new Date());
    const timer = window.setInterval(tick, 1000);
    window.addEventListener("focus", tick);
    return () => {
      window.clearInterval(timer);
      window.removeEventListener("focus", tick);
    };
  }, []);
  useEffect(() => {
    const controller = new AbortController();
    setFailed(false);
    fetch(POOL_URL, { signal: controller.signal })
      .then((r) => {
        if (!r.ok) throw new Error("pool");
        return r.json() as Promise<CertlePool>;
      })
      .then((data) => {
        if (
          !Array.isArray(data.entries) ||
          !data.entries.length ||
          !data.entries.every(
            (e) =>
              typeof e.id === "string" &&
              typeof e.question === "string" &&
              Array.isArray(e.points) &&
              e.points.length &&
              e.points.every(
                (p) =>
                  typeof p.verbatim === "string" &&
                  Number.isInteger(p.marks) &&
                  p.marks > 0,
              ),
          )
        )
          throw new Error("invalid pool");
        setPool(data.entries);
      })
      .catch((e) => {
        if (e.name !== "AbortError") setFailed(true);
      });
    return () => controller.abort();
  }, [reload]);
  useEffect(() => {
    if (!entry) return;
    const restored = restoreGame(day, entry);
    setGame(restored);
    const draft = readStored<unknown>(draftKey(day, entry.id));
    setAnswer(typeof draft === "string" ? draft.slice(0, 3000) : "");
    setNotice("");
    setDialog(null);
    if (restored.finished) {
      const saved = recordResult(loadStats(), restored, entry);
      setStats(saved);
      saveStored(STATS_KEY, saved);
    }
  }, [day, entry]);
  useEffect(() => {
    const sync = (e: StorageEvent) => {
      if (e.key === GAME_KEY && entry) {
        setGame(restoreGame(day, entry));
        setStats(loadStats());
      }
      if (e.key === STATS_KEY) setStats(loadStats());
    };
    window.addEventListener("storage", sync);
    return () => window.removeEventListener("storage", sync);
  }, [day, entry]);
  const commit = (next: Game) => {
    if (!entry) return;
    setGame(next);
    if (!saveStored(GAME_KEY, next)) setLocalOnly(true);
    if (next.finished) {
      const updated = recordResult(loadStats(), next, entry);
      setStats(updated);
      if (!saveStored(STATS_KEY, updated)) setLocalOnly(true);
    }
  };
  const check = () => {
    if (!entry || !ready || finished) return;
    const stored = restoreGame(day, entry);
    const current =
      stored.answers.length > game!.answers.length || stored.finished
        ? stored
        : game!;
    const next = submitAnswer(current, entry, answer);
    if (next === current) {
      setGame(current);
      setNotice(
        current.finished
          ? "Today’s result is already complete."
          : !answer.trim()
            ? "Write an answer first."
            : "You’ve tried that answer. Add or change something before checking again.",
      );
      return;
    }
    setNotice("");
    commit(next);
    if (!next.finished) requestAnimationFrame(() => field.current?.focus());
  };
  const finish = () => {
    if (entry && ready && game!.answers.length && !finished) {
      const stored = restoreGame(day, entry);
      const current =
        stored.answers.length > game!.answers.length || stored.finished
          ? stored
          : game!;
      commit({ ...current, finished: true });
    }
  };
  return (
    <div className="landing-page certle-page">
      <Nav page="certle" />
      <main className="certle-main">
        <header className="certle-heading">
          <p className="certle-eyebrow">The daily Leaving Cert challenge</p>
          <div className="certle-name">
            <h1 aria-label="CERTLE">
              <CertleLogo />
            </h1>
          </div>
          <CertleCompanion />
          <p className="certle-tagline">
            One question. Three attempts. <strong>Every mark counts.</strong>
          </p>
        </header>
        <div className="certle-toolbar">
          <div className="certle-date">
            <span>No. {String(n).padStart(3, "0")}</span>
            <time dateTime={day}>{formatDay(day)}</time>
          </div>
          <div className="certle-tools">
            <button
              type="button"
              className="certle-tool-button"
              aria-label="How to play"
              onClick={() => setDialog("help")}
            >
              <HelpCircle size={18} />
              <span>How to play</span>
            </button>
            <button
              type="button"
              className="certle-tool-button"
              aria-label="Your statistics"
              onClick={() => setDialog("stats")}
            >
              <BarChart3 size={18} />
              <span>Your record</span>
            </button>
          </div>
        </div>
        <section
          className={`certle-play${finished ? " is-finished" : ""}`}
          aria-label="Daily question"
        >
          {failed ? (
            <div className="certle-load" role="alert">
              <h2>Let’s try that again.</h2>
              <p>
                Today’s question couldn’t load. Your saved result is still here.
              </p>
              <button
                className="certle-primary"
                type="button"
                onClick={() => setReload((r) => r + 1)}
              >
                <RotateCcw size={17} />
                Retry
              </button>
            </div>
          ) : !ready ? (
            <div className="certle-load" role="status">
              <span className="certle-loading-tiles" aria-hidden="true">
                <i />
                <i />
                <i />
              </span>
              Finding today’s question…
            </div>
          ) : (
            <>
              <div className="certle-question-sheet">
                <div className="certle-paper-top">
                  <p className="certle-eyebrow">{entry!.subject}</p>
                  <span className="certle-tariff">{plural(total, "mark")}</span>
                </div>
                <h2
                  className={`certle-question${entry!.question.length > 100 ? " is-long" : ""}`}
                >
                  {entry!.question}
                </h2>
                {entry!.figure && (
                  <figure className="certle-figure">
                    <img src={entry!.figure.src} alt={entry!.figure.alt} />
                    <figcaption>Figure from the original SEC paper.</figcaption>
                  </figure>
                )}
                <div className="certle-paper-source">
                  <span className="certle-eyebrow">From the exam paper</span>
                  <p>
                    <span>
                      {entry!.year} · {entry!.level}
                    </span>
                    <span>{entry!.ref.replace(/^\d{4}\s+(HL|OL)\s+/, "")}</span>
                  </p>
                </div>
              </div>
              <div className="certle-workspace">
                {finished ? (
                  <div className="certle-result-heading">
                    <p className="certle-eyebrow">Today’s result</p>
                    <div className="certle-score-display">
                      <strong>
                        {best?.earned ?? 0}
                        <span>/{total}</span>
                      </strong>
                      <span>marks</span>
                    </div>
                    <h2 ref={resultHeading} tabIndex={-1}>
                      {best?.earned === total
                        ? "Full marks. Nicely done."
                        : "That’s today’s CERTLE."}
                    </h2>
                    <p>
                      {best?.earned === total
                        ? `You got there in ${plural(game!.answers.length, "attempt")}.`
                        : "Your best attempt counts. See how it matches the scheme below."}
                    </p>
                  </div>
                ) : (
                  <div className="certle-board-heading">
                    <h3>Your marks</h3>
                    <span>One square = one mark</span>
                  </div>
                )}
                <MarksBoard
                  results={results}
                  total={total}
                  current={game!.answers.length}
                  finished={finished}
                />
                {!finished ? (
                  <>
                    <div
                      className="certle-result-line"
                      aria-live="polite"
                      aria-atomic="true"
                    >
                      {best ? (
                        <>
                          <strong>
                            {best.earned > 0
                              ? `${best.earned} of ${total} marks earned.`
                              : "No scheme points matched yet."}
                          </strong>
                          <p>
                            {plural(remaining, "attempt")} left.{" "}
                            {best.earned > 0
                              ? "Add to your answer. Your best score is safe."
                              : "Try adding more of the detail asked for."}
                          </p>
                        </>
                      ) : (
                        <p>Earn marks, then add to your answer.</p>
                      )}
                    </div>
                    <form
                      onSubmit={(e) => {
                        e.preventDefault();
                        check();
                      }}
                      className="certle-answer-form"
                    >
                      <div className="certle-answer-heading">
                        <label htmlFor="certle-answer">
                          {game!.answers.length
                            ? "Improve your answer"
                            : "Your answer"}
                        </label>
                        <span>
                          ATTEMPT {game!.answers.length + 1} / {MAX_ATTEMPTS}
                        </span>
                      </div>
                      <textarea
                        ref={field}
                        id="certle-answer"
                        value={answer}
                        onChange={(e) => {
                          setAnswer(e.target.value);
                          if (
                            !saveStored(
                              draftKey(day, entry!.id),
                              e.target.value,
                            )
                          )
                            setLocalOnly(true);
                          setNotice("");
                        }}
                        onKeyDown={(e) => {
                          if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
                            e.preventDefault();
                            check();
                          }
                        }}
                        rows={3}
                        maxLength={3000}
                        placeholder={
                          schemePoints(entry!).some(
                            (point) => point.partIndex !== undefined,
                          )
                            ? "(i) …\n(ii) …\n(iii) …"
                            : "Write what you know…"
                        }
                        autoComplete="off"
                        spellCheck
                        aria-describedby="certle-answer-hint"
                      />
                      <div className="certle-form-bottom">
                        <p id="certle-answer-hint">
                          Checked against the
                          <br />
                          SEC marking scheme.
                        </p>
                        <button
                          type="submit"
                          disabled={!answer.trim()}
                          className="certle-primary"
                        >
                          Check my answer
                          <ArrowRight size={18} />
                        </button>
                      </div>
                      {notice && (
                        <p className="certle-notice" role="alert">
                          {notice}
                        </p>
                      )}
                      {game!.answers.length > 0 && (
                        <button
                          type="button"
                          className="certle-text-button certle-finish"
                          onClick={finish}
                        >
                          Finish & see the scheme
                        </button>
                      )}
                    </form>
                  </>
                ) : (
                  <div className="certle-finished-actions">
                    <button
                      type="button"
                      className="certle-primary"
                      onClick={() => setDialog("share")}
                    >
                      <Share2 size={18} />
                      Share my result
                      <ArrowRight size={18} />
                    </button>
                    <span>Your squares. No spoilers.</span>
                  </div>
                )}
                {game!.answers.length > 0 && (
                  <details className="certle-answer-history">
                    <summary>
                      Your {plural(game!.answers.length, "attempt")}
                    </summary>
                    {game!.answers.map((a, i) => (
                      <div key={i}>
                        <b>
                          Attempt {i + 1} · {results[i].earned}/{total}
                          {i === bestIndex ? " · Best" : ""}
                        </b>
                        <p>{a}</p>
                      </div>
                    ))}
                  </details>
                )}
              </div>
            </>
          )}
        </section>
        <div className="certle-daily-foot">
          <p>
            A new question every day. <span>Midnight, Irish time.</span>
          </p>
          <span className="certle-next">
            Next in{" "}
            <time
              aria-label={`${Math.floor(seconds / 3600)} hours and ${Math.floor((seconds % 3600) / 60)} minutes until the next question`}
            >
              {countdown}
            </time>
          </span>
        </div>
        {finished && entry && best && (
          <section
            className="certle-scheme"
            aria-labelledby="certle-scheme-title"
          >
            <div className="certle-scheme-title">
              <div>
                <p className="certle-eyebrow">The marking scheme</p>
                <h2 id="certle-scheme-title">Here’s where the marks are.</h2>
              </div>
              <span>
                {best.earned}/{total} matched
              </span>
            </div>
            <p className="certle-scheme-intro">
              The SEC’s scheme points, compared with your best attempt.
              Automatic matching can miss valid wording, so check any unmatched
              points against your response.
            </p>
            <ul>
              {schemePoints(entry).map((point, i) => {
                const hit = best.hits[i].matched;
                return (
                  <li key={point.id} className={hit ? "is-earned" : ""}>
                    <span className="certle-scheme-status">
                      {hit ? (
                        <Check size={17} />
                      ) : (
                        <span aria-hidden="true">—</span>
                      )}
                    </span>
                    <div>
                      <p>{point.verbatim}</p>
                      <small>
                        {hit
                          ? "Matched in your answer"
                          : "Not recognised automatically"}
                      </small>
                    </div>
                    <strong>
                      {hit ? point.marks : 0}
                      <span> / {plural(point.marks, "mark")}</span>
                    </strong>
                  </li>
                );
              })}
            </ul>
            <p className="certle-attribution">
              {entry.attribution}. Marks are awarded in the groups set by the
              scheme.
            </p>
          </section>
        )}
        {localOnly && (
          <p className="certle-notice" role="status">
            Your browser couldn’t save your progress. It is available for this
            visit only.
          </p>
        )}
        <footer className="certle-footer">
          <a href="/landing">
            <span>nextstepuni</span>More ways to practise
            <ArrowRight size={16} />
          </a>
        </footer>
      </main>
      <Modal
        open={dialog === "share"}
        title="Share your result."
        onClose={() => setDialog(null)}
      >
        {dialog === "share" && shareData && <ShareResult data={shareData} />}
      </Modal>
      <Modal
        open={dialog === "help"}
        title="How to play CERTLE"
        onClose={() => setDialog(null)}
      >
        <div className="certle-help">
          <p className="certle-help-intro">
            One real Leaving Cert question for everyone. A new one arrives at
            midnight in Ireland.
          </p>
          <ol className="certle-help-steps" role="list">
            <li>
              <span className="certle-help-number" aria-hidden="true">
                  1
                </span>
              <div>
                <strong>Answer in your own words.</strong>
                <p>You have three attempts to earn the marks.</p>
              </div>
            </li>
            <li>
              <span className="certle-help-number" aria-hidden="true">
                  2
                </span>
              <div>
                <strong>Build on each attempt.</strong>
                <p>
                  Check your answer, earn partial credit and improve it.
                  Your best attempt is the score that counts.
                </p>
              </div>
            </li>
            <li>
              <span className="certle-help-number" aria-hidden="true">
                  3
                </span>
              <div>
                <strong>Review and share.</strong>
                <p>
                  Once you finish, see the SEC marking scheme and share your
                  result without revealing the answer.
                </p>
              </div>
            </li>
          </ol>
          <div className="certle-help-scoring">
            <div
              className="certle-help-example"
              role="img"
              aria-label="Example: 3 of 6 marks earned"
            >
              {Array.from({ length: 6 }, (_, i) => (
                <span
                  key={i}
                  className={i < 3 ? "is-earned" : undefined}
                  aria-hidden="true"
                />
              ))}
              <strong aria-hidden="true">3 / 6</strong>
            </div>
            <p>
              Each orange square is one earned mark. Marks follow the scheme’s
              groups: a three-mark point earns all three squares together.
            </p>
          </div>
          <p className="certle-dialog-note">
            Hyphens, spacing and small typing slips are allowed. Automatic
            matching can still miss valid wording; check the scheme when you
            finish.
          </p>
          <button
            type="button"
            className="certle-primary"
            onClick={() => setDialog(null)}
          >
            Let’s play
            <ArrowRight size={17} />
          </button>
        </div>
      </Modal>
      <Modal
        open={dialog === "stats"}
        title="Your CERTLE record"
        onClose={() => setDialog(null)}
      >
        <div className="certle-stat-grid">
          <div>
            <strong>{summary.played}</strong>
            <span>Played</span>
          </div>
          <div>
            <strong>{summary.winRate}%</strong>
            <span>Full marks</span>
          </div>
          <div>
            <strong>{summary.streak}</strong>
            <span>Day streak</span>
          </div>
        </div>
        <h3>Full marks by attempt</h3>
        <div className="certle-distribution">
          {[1, 2, 3].map((attempt) => {
            const count = stats.results.filter(
              (r) => r.complete && r.attempts === attempt,
            ).length;
            return (
              <div
                key={attempt}
                role="img"
                aria-label={`Attempt ${attempt}: ${count} full-mark games`}
              >
                <span aria-hidden="true">{attempt}</span>
                <div className="certle-distribution-track" aria-hidden="true">
                  <div
                    className="certle-distribution-fill"
                    style={{
                      width: `${summary.fullMarks ? (count / summary.fullMarks) * 100 : 0}%`,
                    }}
                  />
                </div>
                <span className="certle-distribution-count" aria-hidden="true">
                  {count}
                </span>
              </div>
            );
          })}
        </div>
        <p className="certle-dialog-note">
          Your record is saved in this browser. A streak counts consecutive days
          you finish a question, whether you earn full marks or partial marks.
        </p>
      </Modal>
    </div>
  );
}
