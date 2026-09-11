import React, { useEffect, useMemo, useRef, useState } from "react";
import {
  ArrowLeft,
  ArrowRight,
  BarChart3,
  Check,
  Copy,
  HelpCircle,
  RotateCcw,
  Share2,
  X,
} from "lucide-react";
import Nav from "../landing/sections/Nav";
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
  shareText,
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
  const [dialog, setDialog] = useState<"help" | "stats" | null>(null),
    [notice, setNotice] = useState(""),
    [shareNotice, setShareNotice] = useState(""),
    [localOnly, setLocalOnly] = useState(false);
  const [copyFallback, setCopyFallback] = useState("");
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
    setShareNotice("");
    setCopyFallback("");
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
  const share = async (copy = false) => {
    if (!entry || !game || !finished) return;
    const text = shareText(n, game, entry, window.location.origin);
    if (!copy && typeof navigator.share === "function") {
      try {
        await navigator.share({ text });
        setShareNotice("Shared.");
        return;
      } catch (e) {
        if ((e as Error).name === "AbortError") return;
      }
    }
    try {
      await navigator.clipboard.writeText(text);
      setShareNotice("Result copied.");
    } catch {
      setCopyFallback(text);
      setShareNotice("Select and copy your result below.");
    }
  };

  return (
    <div className="landing-page certle-page">
      <Nav page="certle" />
      <main className="certle-main">
        <div className="certle-utility">
          <a href="/landing">
            <ArrowLeft size={15} />
            Back to Nextstepuni
          </a>
          <div>
            <button
              type="button"
              className="certle-icon-button"
              aria-label="How to play"
              onClick={() => setDialog("help")}
            >
              <HelpCircle size={20} />
            </button>
            <button
              type="button"
              className="certle-icon-button"
              aria-label="Your statistics"
              onClick={() => setDialog("stats")}
            >
              <BarChart3 size={20} />
            </button>
          </div>
        </div>
        <header className="certle-heading">
          <p className="certle-eyebrow">YOUR DAILY LEAVING CERT CHALLENGE</p>
          <div className="certle-name">
            <h1 aria-label="CERTLE">
              {"CERTLE".split("").map((letter, i) => (
                <span
                  aria-hidden="true"
                  className={`certle-letter certle-letter-${i}`}
                  key={i}
                >
                  {letter}
                </span>
              ))}
            </h1>
            <img
              src="/assets/landing/starguy-512.png"
              alt="Nextstepuni’s star character"
              width={72}
              height={106}
            />
          </div>
          <p>One question. Three attempts. Every mark counts.</p>
          <div className="certle-date">
            <span>NO. {String(n).padStart(3, "0")}</span>
            <span aria-hidden="true">/</span>
            <time dateTime={day}>{formatDay(day)}</time>
          </div>
        </header>
        <div className="certle-layout">
          <section className="certle-play" aria-label="Daily question">
            {failed ? (
              <div className="certle-load" role="alert">
                <h2>Let’s try that again.</h2>
                <p>
                  Today’s question couldn’t load. Your saved result is still
                  here.
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
                Finding today’s question…
              </div>
            ) : (
              <>
                <div className="certle-paper-top">
                  <div>
                    <p className="certle-eyebrow">TODAY’S PAPER</p>
                    <h2>{entry!.subject}</h2>
                  </div>
                  <span className="certle-tariff">
                    {total}
                    <small>{total === 1 ? "mark" : "marks"}</small>
                  </span>
                </div>
                <div className="certle-paper">
                  <p className="certle-source">
                    {entry!.year} · {entry!.level} ·{" "}
                    {entry!.ref.replace(/^\d{4}\s+(HL|OL)\s+/, "")}
                  </p>
                  <h3 className="certle-question">{entry!.question}</h3>
                  {entry!.figure && (
                    <figure className="certle-figure">
                      <img src={entry!.figure.src} alt={entry!.figure.alt} />
                      <figcaption>
                        Figure from the original SEC paper.
                      </figcaption>
                    </figure>
                  )}
                  <div className="certle-attempts" aria-label="Your attempts">
                    {Array.from({ length: MAX_ATTEMPTS }, (_, i) => {
                      const r = results[i];
                      const cells = r
                        ? r.hits.flatMap((h) =>
                            Array.from({ length: h.marks }, () => h.matched),
                          )
                        : Array.from({ length: total }, () => false);
                      return (
                        <div
                          className={`certle-attempt${r ? " is-played" : ""}${!finished && i === game!.answers.length ? " is-current" : ""}`}
                          key={i}
                          aria-label={`Attempt ${i + 1}: ${r ? `${r.earned} of ${r.total} marks` : "not played"}`}
                        >
                          <span className="certle-attempt-number">
                            0{i + 1}
                          </span>
                          <div
                            className="certle-squares"
                            style={{ "--marks": total } as React.CSSProperties}
                          >
                            {cells.map((hit, j) => (
                              <span
                                aria-hidden="true"
                                key={j}
                                className={
                                  hit ? "is-earned" : r ? "is-unmatched" : ""
                                }
                              >
                                {hit ? <Check size={14} /> : null}
                              </span>
                            ))}
                          </div>
                          <span className="certle-attempt-score">
                            {r ? `${r.earned}/${r.total}` : "—"}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                  <div
                    className="certle-result-line"
                    aria-live="polite"
                    aria-atomic="true"
                  >
                    {best ? (
                      <>
                        <strong>
                          {best.earned === total
                            ? "Full marks. Nicely done."
                            : best.earned > 0
                              ? `${best.earned} of ${total} marks. ${finished ? "A little more learned." : "Keep building."}`
                              : "No scheme points matched yet."}
                        </strong>
                        <p>
                          {finished
                            ? best.earned === total
                              ? `You got there in ${plural(game!.answers.length, "attempt")}. Come back tomorrow for a new subject.`
                              : "Your best attempt counts. Compare your wording with the scheme below."
                            : `${plural(remaining, "attempt")} left. ${best.earned > 0 ? "Your best score is safe." : "Try adding the detail the question asks for."}`}
                        </p>
                      </>
                    ) : (
                      <p>Each square is one mark. How many can you earn?</p>
                    )}
                  </div>
                  {!finished ? (
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
                          saveStored(draftKey(day, entry!.id), e.target.value);
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
                        placeholder="Think it through. Write what you know."
                        autoComplete="off"
                        spellCheck
                        aria-describedby="certle-answer-hint"
                      />
                      <div className="certle-form-bottom">
                        <p id="certle-answer-hint">
                          A short answer is fine.
                          <br />
                          Use your own words.
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
                  ) : (
                    <div className="certle-finished">
                      <div className="certle-final-score">
                        <span>YOUR BEST SCORE</span>
                        <strong>
                          {best?.earned ?? 0}
                          <small>/{total}</small>
                        </strong>
                        <p>
                          {best?.earned === total
                            ? "Every mark earned."
                            : "A little more learned."}
                        </p>
                      </div>
                      <button
                        type="button"
                        className="certle-primary"
                        onClick={() => void share()}
                      >
                        <Share2 size={17} />
                        Share my result
                      </button>
                      <button
                        type="button"
                        className="certle-text-button"
                        onClick={() => void share(true)}
                      >
                        <Copy size={14} />
                        Copy result
                      </button>
                      <p className="certle-share-notice" role="status">
                        {shareNotice}
                      </p>
                      {copyFallback && (
                        <textarea
                          aria-label="Result to copy"
                          className="certle-share-fallback"
                          readOnly
                          value={copyFallback}
                          onFocus={(e) => e.target.select()}
                        />
                      )}
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
          <aside className="certle-aside">
            <section className="certle-record">
              <p className="certle-eyebrow">YOUR DAILY RECORD</p>
              <div className="certle-stat-grid">
                <div>
                  <strong>{summary.played}</strong>
                  <span>Played</span>
                </div>
                <div>
                  <strong>{summary.fullMarks}</strong>
                  <span>Full marks</span>
                </div>
                <div>
                  <strong>{summary.streak}</strong>
                  <span>Day streak</span>
                </div>
              </div>
              <p>Small steps, every day.</p>
            </section>
            <section className="certle-guide">
              <p className="certle-eyebrow">THE IDEA IS SIMPLE</p>
              <ol>
                <li>
                  <span>01</span>
                  <p>Answer one real Leaving Cert question.</p>
                </li>
                <li>
                  <span>02</span>
                  <p>Earn the marks you know. You have three attempts.</p>
                </li>
                <li>
                  <span>03</span>
                  <p>
                    Read the scheme. Share your squares. Come back tomorrow.
                  </p>
                </li>
              </ol>
              <div className="certle-key">
                <span>
                  <i className="earned" />
                  Mark earned
                </span>
                <span>
                  <i />
                  Not matched yet
                </span>
              </div>
            </section>
            <section className="certle-next">
              <p className="certle-eyebrow">YOUR NEXT QUESTION IN</p>
              <time
                aria-label={`${Math.floor(seconds / 3600)} hours and ${Math.floor((seconds % 3600) / 60)} minutes until the next question`}
              >
                {countdown}
              </time>
              <p>
                Midnight, Irish time.
                <br />A fresh question for everyone.
              </p>
            </section>
          </aside>
        </div>
        {finished && entry && best && (
          <section
            className="certle-scheme"
            aria-labelledby="certle-scheme-title"
          >
            <div className="certle-scheme-title">
              <div>
                <p className="certle-eyebrow">
                  AFTER THE ANSWER, THE UNDERSTANDING.
                </p>
                <h2 id="certle-scheme-title">Here’s where the marks are.</h2>
              </div>
              <span>
                {best.earned}/{total} matched
              </span>
            </div>
            <p className="certle-scheme-intro">
              The SEC’s own scheme points, compared with your best attempt. A
              valid answer can use different wording; an unmatched point is
              worth checking against your response.
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
            Your browser couldn’t save this result. It is available for this
            visit only.
          </p>
        )}
        <footer className="certle-footer">
          <p>Real questions. Real marking schemes. A little progress, daily.</p>
          <a href="/landing">
            More ways to practise with Nextstepuni
            <ArrowRight size={14} />
          </a>
        </footer>
      </main>
      <Modal
        open={dialog === "help"}
        title="How to play CERTLE"
        onClose={() => setDialog(null)}
      >
        <p>
          Everyone gets the same real Leaving Cert question, changing at
          midnight in Ireland.
        </p>
        <ol>
          <li>Write an answer in your own words.</li>
          <li>
            You have three attempts. Partial credit comes from the individual
            SEC scheme points you earn.
          </li>
          <li>
            Improve your answer after each check. Your best attempt is the score
            that counts.
          </li>
          <li>
            Once you finish, see the scheme and share your result without
            revealing the answer.
          </li>
        </ol>
        <p>
          One orange square is one earned mark. The scheme decides how marks are
          grouped; a point worth three marks is awarded as a group.
        </p>
        <p className="certle-dialog-note">
          Automatic matching recognises scheme alternatives and common
          equivalent wording. It can still miss a valid response: the final
          scheme review lets you check that wording yourself.
        </p>
        <button
          type="button"
          className="certle-primary"
          onClick={() => setDialog(null)}
        >
          Let’s play
          <ArrowRight size={17} />
        </button>
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
              <div key={attempt}>
                <span>{attempt}</span>
                <div
                  style={{
                    width: `${Math.max(12, summary.fullMarks ? (count / summary.fullMarks) * 100 : 12)}%`,
                  }}
                >
                  {count}
                </div>
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
