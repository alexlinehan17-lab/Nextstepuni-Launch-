import { useState, useSyncExternalStore } from "react";
import {
  ArrowUpRight,
  Check,
  ChevronLeft,
  ChevronRight,
  Settings2,
} from "lucide-react";
import KobraScope, {
  Button,
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "../approved-ui-runtime";
import { StudySubjectArtwork } from "../study/StudySubjectPicker";
import { DAYS_OF_WEEK } from "../subjectData";
import {
  addDays,
  dayCapacity,
  dateKey,
  localDate,
  type PlanInputs,
  type PlanSettings,
  type PlanTask,
} from "../../services/studyPlanEngine";
import {
  createStudyPlan,
  movePlanTask,
  readStudyPlan,
  saveRetrievalResult,
  setTaskStatus,
  subscribeStudyPlan,
  updateStudyPlan,
} from "../../services/studyPlanStore";
import { SessionTodos } from "../study/SessionTodos";
import type { SchoolEvent } from "../gc/GCKeyEvents";
import { STUDY_EVIDENCE } from "../../data/studyEvidence";
import "./dated-planner.css";

export const planTime = (n: number) =>
  n < 60 ? `${n}m` : `${Math.floor(n / 60)}h${n % 60 ? ` ${n % 60}m` : ""}`;
const label = (key: string) =>
  localDate(key).toLocaleDateString("en-IE", {
    day: "numeric",
    month: "short",
  });
const kindLabel = {
  practice: "Focused practice",
  retrieval: "Retrieval check",
  maintenance: "Keep in touch",
  cards: "Mark Bank",
  deadline: "Deadline preparation",
};
export default function DatedPlanner({
  scope,
  today = dateKey(new Date()),
  sample = false,
  onStudy,
  onComplete,
  schoolEvents = [],
  onEditSubjects,
}: {
  scope: string;
  today?: string;
  sample?: boolean;
  schoolEvents?: SchoolEvent[];
  onEditSubjects?: () => void;
  onStudy?: (task: PlanTask) => void;
  onComplete?: (date: string, id: string, done: boolean) => void;
}) {
  const saved = useSyncExternalStore(
    subscribeStudyPlan,
    () => readStudyPlan(scope),
    () => undefined,
  );
  const [editingTodos, setEditingTodos] = useState(false);
  const [week, setWeek] = useState(0);
  const [selectedId, setSelectedId] = useState("");
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [draft, setDraft] = useState<PlanSettings>();
  const [inputsDraft, setInputsDraft] = useState<PlanInputs>();
  const [moveDate, setMoveDate] = useState("");
  const [shortMinutes, setShortMinutes] = useState(15);
  const [message, setMessage] = useState("");
  if (!saved) return <p>Preparing your dated plan…</p>;
  const { plan, inputs } = saved;
  const dates = plan.days.slice(week * 7, week * 7 + 7);
  const tasks = plan.tasks.filter(
    (t) => dates.some((d) => d.date === t.date) && t.status !== "dropped",
  );
  const selected =
    tasks.find((t) => t.id === selectedId) ??
    tasks.find((t) => t.status === "planned") ??
    tasks[0];
  const capacity = dates.reduce((n, d) => n + d.capacity, 0);
  const total = tasks.reduce((n, t) => n + t.durationMinutes, 0);
  const assigned = dates.reduce((n, d) => n + d.assignedMinutes, 0);
  const budget = Math.min(capacity, inputs.settings.revisionMinutes);
  const complete = (task: PlanTask, done: boolean) => {
    setTaskStatus(scope, task.id, done ? "completed" : "planned");
    onComplete?.(task.date, task.id, done);
  };
  const openSettings = () => {
    setDraft(structuredClone(inputs.settings));
    setInputsDraft(structuredClone(inputs));
    setSettingsOpen(true);
  };
  const select = (task: PlanTask) => {
    setSelectedId(task.id);
    setMoveDate(task.date);
    setShortMinutes(Math.min(15, task.durationMinutes));
    setMessage("");
    if (window.matchMedia("(max-width: 780px)").matches)
      document
        .getElementById("dated-session-details")
        ?.scrollIntoView({ behavior: "smooth", block: "start" });
  };
  const changeDay = (
    index: number,
    key: keyof PlanSettings["days"][number],
    value: string,
  ) =>
    setDraft((d) =>
      d
        ? {
            ...d,
            days: d.days.map((day, i) =>
              i === index
                ? { ...day, [key]: Math.max(0, Number(value) || 0) }
                : day,
            ),
          }
        : d,
    );
  return (
    <KobraScope className="dated-planner">
      <main className="dp-main">
        <header className="dp-hero">
          <div>
            <span className="dp-eyebrow">YOUR LAUNCHPAD / THE PLANNER</span>
            <h1>
              Your week.
              <br />
              <em>Room to learn.</em>
            </h1>
            <p>Start with the time you have. Make the next step count.</p>
          </div>
          <div className="dp-hero-side">
            <StudySubjectArtwork subject="Mathematics" size={120} />
            <span>
              {sample
                ? "Sample student · local review"
                : "Your saved study plan"}
            </span>
            <small role="status">
              {saved.sync === "synced"
                ? "Saved to your account"
                : saved.sync === "saving"
                  ? "Saved here · waiting for account sync"
                  : saved.sync === "loading"
                    ? "Loading your account plan…"
                    : saved.sync === "offline"
                      ? "Offline · saved on this device"
                      : saved.sync === "error"
                        ? "Account save failed · changes kept here"
                        : saved.saved
                          ? "Saved on this device"
                          : "Available in this tab only"}
            </small>
          </div>
        </header>
        {saved.sync === "error" && (
          <Button
            variant="outline"
            onClick={() =>
              window.dispatchEvent(new Event("nsu:retry-plan-save"))
            }
          >
            Retry account save
          </Button>
        )}
        {saved.error && (
          <p className="dp-notice" role="alert">
            {saved.error}
          </p>
        )}
        <div className="dp-ledger">
          <div>
            <span>Already assigned</span>
            <strong>{planTime(assigned)}</strong>
            <small>Homework & coursework, counted once</small>
          </div>
          <div>
            <span>Revision capacity</span>
            <strong>{planTime(capacity)}</strong>
            <small>After assigned work, breaks & buffer</small>
          </div>
          <div>
            <span>Your commitment</span>
            <strong>{planTime(inputs.settings.revisionMinutes)}</strong>
            <small>
              {inputs.settings.revisionMinutes > capacity
                ? `${planTime(inputs.settings.revisionMinutes - capacity)} does not fit this week`
                : "A limit you choose, not an obligation"}
            </small>
          </div>
          <div>
            <span>Actually planned</span>
            <strong>{planTime(total)}</strong>
            <small>
              {planTime(Math.max(0, budget - total))} left within the limit
            </small>
          </div>
        </div>
        {!inputs.settings.confirmed && (
          <Button variant="outline" onClick={openSettings}>
            Set my available time
          </Button>
        )}
        {plan.notices.map((notice, i) => (
          <p className="dp-notice" key={i}>
            {notice}
          </p>
        ))}
        <div className="dp-toolbar">
          <div>
            <Button
              variant="outline"
              size="icon"
              aria-label="Previous week"
              disabled={!week}
              onClick={() => setWeek(0)}
            >
              <ChevronLeft />
            </Button>
            <h2>
              {label(dates[0].date)} — {label(dates[6].date)}
              <small>
                {week ? "The following week" : "The first week"} ·{" "}
                {tasks.filter((t) => t.status === "completed").length}/
                {tasks.length} done
              </small>
            </h2>
            <Button
              variant="outline"
              size="icon"
              aria-label="Next week"
              disabled={!!week}
              onClick={() => setWeek(1)}
            >
              <ChevronRight />
            </Button>
          </div>
          <Button variant="outline" onClick={openSettings}>
            <Settings2 size={16} /> Shape my week
          </Button>
        </div>
        <div className="dp-layout">
          <section
            id="dated-week"
            className="dp-week"
            aria-label="Dated timetable"
          >
            {dates.map((day, i) => {
              const entries = tasks.filter((t) => t.date === day.date);
              const used = entries.reduce((n, t) => n + t.durationMinutes, 0);
              return (
                <article className="dp-day" key={day.date}>
                  <header>
                    <h3>
                      {DAYS_OF_WEEK[i]}{" "}
                      <span>{localDate(day.date).getDate()}</span>
                    </h3>
                    <small>
                      {used} / {day.capacity} min
                    </small>
                  </header>
                  {schoolEvents
                    .filter((event) => event.date === day.date)
                    .map((event) => (
                      <p className="dp-notice" key={event.id}>
                        {event.title}
                      </p>
                    ))}
                  <div className="dp-day-track">
                    <i
                      style={{
                        width: `${Math.min(100, (used / Math.max(1, day.capacity)) * 100)}%`,
                      }}
                    />
                  </div>
                  {entries.length ? (
                    entries.map((task) => (
                      <button
                        className="dp-task"
                        key={task.id}
                        data-selected={selected?.id === task.id}
                        data-complete={task.status === "completed"}
                        onClick={() => select(task)}
                        aria-pressed={selected?.id === task.id}
                      >
                        <span className="dp-task-top">
                          <StudySubjectArtwork
                            subject={task.subjectName}
                            size={36}
                          />
                          <strong>{task.subjectName}</strong>
                          {task.status === "completed" ? (
                            <Check size={17} />
                          ) : (
                            <ArrowUpRight size={17} />
                          )}
                        </span>
                        <span>{task.title}</span>
                        <small>
                          {task.durationMinutes} min · {kindLabel[task.kind]}
                          {task.date < today && task.status === "planned"
                            ? " · Not done yet"
                            : ""}
                        </small>
                      </button>
                    ))
                  ) : (
                    <p className="dp-rest">
                      {day.capacity
                        ? "Space remains. No task needs to be invented."
                        : day.windowMinutes
                          ? "Assigned work has this day."
                          : "Room for life."}
                    </p>
                  )}
                  <footer>
                    {day.assignedMinutes > 0
                      ? `${day.assignedMinutes}m already assigned`
                      : "No assigned work entered"}
                    {day.breakMinutes > 0
                      ? ` · ${day.breakMinutes}m breaks`
                      : ""}
                  </footer>
                </article>
              );
            })}
          </section>
          <aside
            id="dated-session-details"
            className="dp-detail"
            aria-label="Session details"
          >
            <a className="dp-back-week" href="#dated-week">
              Back to the week ↑
            </a>
            {selected ? (
              <>
                <span className="dp-eyebrow">
                  {kindLabel[selected.kind]} / {label(selected.date)}
                </span>
                <StudySubjectArtwork
                  subject={selected.subjectName}
                  size={105}
                />
                <h2>{selected.title}</h2>
                <p>
                  {selected.subjectName} · {selected.durationMinutes} minutes
                </p>
                <div className="dp-reason">
                  <span>WHY THIS, NOW?</span>
                  <p>{selected.why}</p>
                </div>
                <ol>
                  {selected.steps.map((step) => (
                    <li key={step}>{step}</li>
                  ))}
                </ol>
                <p className="dp-next">
                  <strong>What happens next</strong>
                  {selected.next}
                </p>
                <div className="dp-actions">
                  <Button
                    variant="outline"
                    onClick={() => setEditingTodos(true)}
                  >
                    Edit to-dos
                  </Button>
                  {onStudy && selected.status === "planned" && (
                    <Button onClick={() => onStudy(selected)}>
                      Study this block <ArrowUpRight size={16} />
                    </Button>
                  )}
                  <Button
                    variant="outline"
                    disabled={!sample && selected.date > today}
                    onClick={() =>
                      complete(selected, selected.status !== "completed")
                    }
                  >
                    {selected.status === "completed"
                      ? "Undo completion"
                      : "Mark as done"}
                  </Button>
                </div>
                {selected.topicKey && selected.status !== "completed" && (
                  <details className="dp-disclosure">
                    <summary>Record the retrieval result</summary>
                    <p>
                      Use this after trying without notes and checking your
                      answer. Confidence and time spent are separate.
                    </p>
                    <div className="dp-result-buttons">
                      {(["failed", "partial", "independent"] as const).map(
                        (result) => (
                          <Button
                            key={result}
                            variant="outline"
                            disabled={!sample && selected.date > today}
                            onClick={() => {
                              saveRetrievalResult(
                                scope,
                                selected.id,
                                result,
                                sample ? selected.date : today,
                              );
                              onComplete?.(selected.date, selected.id, true);
                              setMessage(
                                `Recorded ${result} retrieval. Future topic reviews have been recalculated.`,
                              );
                            }}
                          >
                            {result === "failed"
                              ? "Needed help"
                              : result === "partial"
                                ? "Partly recalled"
                                : "Recalled independently"}
                          </Button>
                        ),
                      )}
                    </div>
                  </details>
                )}
                {selected.status !== "completed" && (
                  <details className="dp-disclosure">
                    <summary>
                      {selected.date < today
                        ? "Missed this? Choose what happens."
                        : "Move, shorten or leave this one."}
                    </summary>
                    <p>
                      A missed block does not become automatic debt tomorrow.
                    </p>
                    <label>
                      Move to
                      <select
                        value={moveDate || selected.date}
                        onChange={(e) => setMoveDate(e.target.value)}
                      >
                        {plan.days.map((d) => (
                          <option value={d.date} key={d.date}>
                            {label(d.date)}
                          </option>
                        ))}
                      </select>
                    </label>
                    <label>
                      Minutes
                      <input
                        type="number"
                        min={10}
                        max={selected.durationMinutes}
                        value={shortMinutes}
                        onChange={(e) =>
                          setShortMinutes(Number(e.target.value))
                        }
                      />
                    </label>
                    <Button
                      variant="outline"
                      onClick={() =>
                        setMessage(
                          movePlanTask(
                            scope,
                            selected.id,
                            moveDate || selected.date,
                            shortMinutes,
                          ) ??
                            "Session moved. Its identity and notes stay with it.",
                        )
                      }
                    >
                      Save this change
                    </Button>
                    <Button
                      variant="ghost"
                      onClick={() => {
                        setTaskStatus(scope, selected.id, "dropped");
                        setMessage(
                          "Left out of this fortnight. It has not been added to another day.",
                        );
                      }}
                    >
                      Leave it out this time
                    </Button>
                  </details>
                )}
              </>
            ) : (
              <>
                <h2>A little breathing room.</h2>
                <p>
                  No tasks fit these settings. Adjust your available minutes or
                  keep this as a rest week.
                </p>
              </>
            )}
            {message && (
              <p role="status" className="dp-message">
                {message}
              </p>
            )}
          </aside>
        </div>
        <section className="dp-bottom">
          <div>
            <span className="dp-eyebrow">THE ACTUAL ALLOCATION</span>
            <h2>A place for each subject.</h2>
            {inputs.profile.subjects.map((s) => {
              const n = tasks
                .filter((t) => t.subjectName === s.subjectName)
                .reduce((sum, t) => sum + t.durationMinutes, 0);
              return (
                <div className="dp-subject-line" key={s.subjectName}>
                  <span>
                    {s.subjectName}
                    <small>
                      {s.currentGrade ?? s.currentBand ?? "No grade"} →{" "}
                      {s.targetGrade ?? s.targetBand ?? "No target"}
                    </small>
                  </span>
                  <div>
                    <i
                      style={{ width: `${(n / Math.max(1, total)) * 100}%` }}
                    />
                  </div>
                  <strong>{planTime(n)}</strong>
                </div>
              );
            })}
          </div>
          <div>
            <span className="dp-eyebrow">KEPT VISIBLE</span>
            <h2>What didn’t fit.</h2>
            <p>
              These are opportunities, not extra homework. They are not carried
              onto tomorrow automatically.
            </p>
            {plan.unscheduled.length ? (
              <details className="dp-disclosure">
                <summary>
                  {plan.unscheduled.length} unscheduled opportunities
                </summary>
                {plan.unscheduled.map((item) => (
                  <article className="dp-unplaced" key={item.id}>
                    <strong>
                      {item.subjectName} · {item.title}
                    </strong>
                    <span>{item.minutes} min</span>
                    <p>{item.reason}</p>
                  </article>
                ))}
              </details>
            ) : (
              <p>All identified work fits within this fortnight.</p>
            )}
            <details className="dp-disclosure">
              <summary>What this plan knows</summary>
              <p>
                {inputs.profile.yearGroup} year · exam cohort{" "}
                {inputs.profile.examStartDate?.slice(0, 4)}. Grades come from
                the subject profile. Targets guide attention; they do not
                determine required hours.
              </p>
              {inputs.requirements.map((r) => (
                <p key={r.subjectName}>
                  <strong>{r.subjectName} requirement:</strong> {r.note}
                </p>
              ))}
              {inputs.evidence.map((e) => (
                <p key={`${e.specificationId}:${e.topicId}`}>
                  <strong>
                    {e.subjectName} / {e.topicName}
                  </strong>
                  <br />
                  {e.taught
                    ? e.result
                      ? `${e.result} retrieval on ${e.observedOn}`
                      : "No independent result recorded"
                    : "Not taught — excluded from gap allocation"}
                  {e.dueOn ? ` · due ${e.dueOn}` : ""}
                </p>
              ))}
              <p>
                Priority weights, session lengths and exact review dates are
                planning choices, not scientifically established doses. This
                plan does not predict grades.
              </p>
            </details>
          </div>
        </section>
        <section className="dp-science">
          <details className="dp-disclosure">
            <summary>Why these study suggestions?</summary>
            <p>
              Start with material you have been taught. Try to recall it, check
              your answer, then revisit it on another day. These principles have
              support in learning research; this particular planner has not been
              tested as an intervention.
            </p>
            {STUDY_EVIDENCE.map((source) => (
              <article key={source.id}>
                <h3>{source.title}</h3>
                <p>
                  {source.guidance} {source.context}
                </p>
                <a href={source.url} target="_blank" rel="noreferrer">
                  {source.citation} — primary study
                </a>
              </article>
            ))}
            <p>
              Your hours and session lengths are adjustable. Subject balance and
              exact review intervals are scheduling rules, not proven optima for
              every student or subject. The plan does not predict grades.
              Subject rotation helps coverage; it is not the same as mixing
              problem types within a subject.
            </p>
          </details>
        </section>
        {editingTodos && selected && (
          <SessionTodos
            key={selected.id}
            steps={selected.steps.map((label) => ({ label }))}
            onClose={() => setEditingTodos(false)}
            onSave={(steps) => {
              updateStudyPlan(scope, (value) => ({
                ...value,
                plan: {
                  ...value.plan,
                  tasks: value.plan.tasks.map((t) =>
                    t.id === selected.id
                      ? {
                          ...t,
                          steps: steps.map((step) => step.label),
                          locked: true,
                        }
                      : t,
                  ),
                },
              }));
              setEditingTodos(false);
            }}
          />
        )}
        <Dialog open={settingsOpen} onOpenChange={setSettingsOpen}>
          <DialogContent className="dp-settings">
            <DialogHeader>
              <DialogTitle>Make room for your real week.</DialogTitle>
              <DialogDescription>
                Enter clock minutes, then reserve breaks and existing work.
                Include supervised study once. Zero days is allowed.
              </DialogDescription>
            </DialogHeader>
            {draft && inputsDraft && (
              <>
                <div className="dp-capacity-table">
                  <div className="dp-capacity-head">
                    <span>Day</span>
                    <span>Window</span>
                    <span>Breaks</span>
                    <span>Assigned</span>
                    <span>Buffer</span>
                    <span>Revision</span>
                  </div>
                  {draft.days.map((day, i) => (
                    <div className="dp-capacity-row" key={i}>
                      <strong>{DAYS_OF_WEEK[i].slice(0, 3)}</strong>
                      {(
                        [
                          "windowMinutes",
                          "breakMinutes",
                          "assignedMinutes",
                          "bufferMinutes",
                        ] as const
                      ).map((key) => (
                        <input
                          key={key}
                          aria-label={`${DAYS_OF_WEEK[i]} ${key}`}
                          type="number"
                          min={0}
                          max={1440}
                          step={5}
                          value={day[key]}
                          onChange={(e) => changeDay(i, key, e.target.value)}
                        />
                      ))}
                      <span>{dayCapacity(day)}m</span>
                    </div>
                  ))}
                </div>
                <div className="dp-settings-pair">
                  <label>
                    Weekly revision commitment (minutes)
                    <input
                      type="number"
                      min={0}
                      max={2400}
                      step={15}
                      value={draft.revisionMinutes}
                      onChange={(e) =>
                        setDraft({
                          ...draft,
                          revisionMinutes: Number(e.target.value),
                        })
                      }
                    />
                  </label>
                  <label>
                    Preferred practice length
                    <select
                      value={draft.preferredMinutes}
                      onChange={(e) =>
                        setDraft({
                          ...draft,
                          preferredMinutes: Number(e.target.value),
                        })
                      }
                    >
                      {[25, 45, 60, 90].map((n) => (
                        <option key={n} value={n}>
                          {n} minutes
                        </option>
                      ))}
                    </select>
                  </label>
                </div>
                <p>
                  Short retrieval checks may use 10–15 minutes. These lengths
                  are practical defaults, not scientifically optimal durations.
                  A longer preference never raises your time limit.
                </p>
                <details className="dp-disclosure">
                  <summary>A date that is different</summary>
                  {plan.days.map((day) => (
                    <label className="dp-exception" key={day.date}>
                      {label(day.date)}
                      <input
                        type="number"
                        min={0}
                        aria-label={`Window on ${day.date}`}
                        placeholder={String(day.windowMinutes)}
                        value={draft.exceptions[day.date]?.windowMinutes ?? ""}
                        onChange={(e) => {
                          const exceptions = { ...draft.exceptions };
                          if (e.target.value === "")
                            delete exceptions[day.date];
                          else
                            exceptions[day.date] = {
                              ...day,
                              windowMinutes: Number(e.target.value),
                            };
                          setDraft({ ...draft, exceptions });
                        }}
                      />
                      <span>
                        clock minutes; breaks and assigned work retained
                      </span>
                    </label>
                  ))}
                </details>
                <details className="dp-disclosure">
                  <summary>Entry requirements & deadlines</summary>
                  {inputs.profile.subjects.map((s) => (
                    <label key={s.subjectName}>
                      {s.subjectName} requirement (optional)
                      <input
                        value={
                          inputsDraft.requirements.find(
                            (r) => r.subjectName === s.subjectName,
                          )?.note ?? ""
                        }
                        onChange={(e) =>
                          setInputsDraft({
                            ...inputsDraft,
                            requirements: [
                              ...inputsDraft.requirements.filter(
                                (r) => r.subjectName !== s.subjectName,
                              ),
                              ...(e.target.value
                                ? [
                                    {
                                      subjectName: s.subjectName,
                                      note: e.target.value,
                                    },
                                  ]
                                : []),
                            ],
                          })
                        }
                      />
                    </label>
                  ))}
                  {inputsDraft.deadlines.map((d, i) => (
                    <div className="dp-deadline-edit" key={d.id}>
                      <label>
                        Preparation task
                        <input
                          value={d.title}
                          onChange={(e) =>
                            setInputsDraft({
                              ...inputsDraft,
                              deadlines: inputsDraft.deadlines.map((x, j) =>
                                j === i ? { ...x, title: e.target.value } : x,
                              ),
                            })
                          }
                        />
                      </label>
                      <label>
                        Due date
                        <input
                          type="date"
                          value={d.dueOn}
                          onChange={(e) =>
                            setInputsDraft({
                              ...inputsDraft,
                              deadlines: inputsDraft.deadlines.map((x, j) =>
                                j === i ? { ...x, dueOn: e.target.value } : x,
                              ),
                            })
                          }
                        />
                      </label>
                      <label>
                        Additional minutes
                        <input
                          type="number"
                          min={10}
                          value={d.minutes}
                          onChange={(e) =>
                            setInputsDraft({
                              ...inputsDraft,
                              deadlines: inputsDraft.deadlines.map((x, j) =>
                                j === i
                                  ? { ...x, minutes: Number(e.target.value) }
                                  : x,
                              ),
                            })
                          }
                        />
                      </label>
                      <label>
                        Subject
                        <select
                          value={d.subjectName}
                          onChange={(e) =>
                            setInputsDraft({
                              ...inputsDraft,
                              deadlines: inputsDraft.deadlines.map((x, j) =>
                                j === i
                                  ? { ...x, subjectName: e.target.value }
                                  : x,
                              ),
                            })
                          }
                        >
                          {inputs.profile.subjects.map((s) => (
                            <option key={s.subjectName}>{s.subjectName}</option>
                          ))}
                        </select>
                      </label>
                      <Button
                        variant="ghost"
                        onClick={() =>
                          setInputsDraft({
                            ...inputsDraft,
                            deadlines: inputsDraft.deadlines.filter(
                              (x) => x.id !== d.id,
                            ),
                          })
                        }
                      >
                        Remove this deadline
                      </Button>
                    </div>
                  ))}
                  <Button
                    variant="outline"
                    disabled={!inputs.profile.subjects.length}
                    onClick={() =>
                      setInputsDraft({
                        ...inputsDraft,
                        deadlines: [
                          ...inputsDraft.deadlines,
                          {
                            id: crypto.randomUUID(),
                            title: "Prepare for a class test",
                            subjectName:
                              inputs.profile.subjects[0]?.subjectName ?? "",
                            dueOn: addDays(plan.start, 4),
                            minutes: 25,
                          },
                        ],
                      })
                    }
                  >
                    Add deadline preparation
                  </Button>
                  <p>
                    Only enter additional preparation here. Work already
                    included in “Assigned” must not be counted again.
                  </p>
                </details>
                {onEditSubjects && (
                  <Button
                    variant="outline"
                    onClick={() => {
                      setSettingsOpen(false);
                      onEditSubjects();
                    }}
                  >
                    Edit subjects and grades
                  </Button>
                )}
                <Button
                  onClick={() => {
                    createStudyPlan(
                      scope,
                      {
                        ...inputsDraft,
                        settings: { ...draft, confirmed: true },
                      },
                      plan.start,
                      today,
                    );
                    setSettingsOpen(false);
                  }}
                >
                  Save & fit my plan
                </Button>
              </>
            )}
          </DialogContent>
        </Dialog>
      </main>
    </KobraScope>
  );
}
