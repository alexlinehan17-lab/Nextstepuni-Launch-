/** A dated, minute-bounded plan. Scheduling policy is configurable product logic, not a scientifically validated dose. */
import {
  DAYS_OF_WEEK,
  JC_BANDS,
  gradeSteps,
  type StudentSubjectProfile,
  type StudyBlock,
  type WeeklyTimetable,
} from "../components/subjectData";
import {
  examinationYearFromDate,
  resolveCurriculumSpecification,
} from "../curriculumRegistry";

export interface DayCapacity {
  windowMinutes: number;
  breakMinutes: number;
  assignedMinutes: number;
  bufferMinutes: number;
}
export interface PlanSettings {
  days: DayCapacity[];
  revisionMinutes: number;
  preferredMinutes: number;
  exceptions: Record<string, DayCapacity>;
  confirmed: boolean;
}
export interface TopicEvidence {
  specificationId: string;
  topicId: string;
  subjectName: string;
  topicName: string;
  taught: boolean;
  confidence?: "shaky" | "solid" | "not-started";
  result?: "failed" | "partial" | "independent";
  observedOn?: string;
  dueOn?: string;
  successfulReviews?: number;
}
export interface CardReviewNeed {
  id: string;
  subjectName: string;
  dueOn: string;
  cardIds: string[];
  minutes: number;
}
export interface PlanDeadline {
  id: string;
  subjectName: string;
  title: string;
  dueOn: string;
  minutes: number;
}
export interface PlanRequirement {
  subjectName: string;
  note: string;
}
export interface PlanInputs {
  profile: StudentSubjectProfile;
  settings: PlanSettings;
  evidence: TopicEvidence[];
  cards: CardReviewNeed[];
  deadlines: PlanDeadline[];
  requirements: PlanRequirement[];
  lastContact: Record<string, string>;
}
export interface PlanTask extends StudyBlock {
  id: string;
  sourceId: string;
  date: string;
  earliest: string;
  deadline?: string;
  topicKey?: string;
  cardIds?: string[];
  afterSourceId?: string;
  title: string;
  why: string;
  steps: string[];
  next: string;
  status: "planned" | "completed" | "dropped";
  locked?: boolean;
  kind: "practice" | "retrieval" | "maintenance" | "deadline" | "cards";
}
export interface PlanDay extends DayCapacity {
  date: string;
  capacity: number;
  planned: number;
  overload: number;
}
export interface StudyPlan {
  version: 1;
  start: string;
  tasks: PlanTask[];
  days: PlanDay[];
  unscheduled: {
    id: string;
    subjectName: string;
    title: string;
    reason: string;
    minutes: number;
  }[];
  notices: string[];
}
export const minutes = (n: number) =>
  Number.isFinite(n) ? Math.max(0, Math.round(n)) : 0;
export const dateKey = (d: Date) =>
  `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
export function localDate(key: string): Date {
  const [y, m, d] = key.split("-").map(Number);
  return new Date(y, m - 1, d, 12);
}
export function addDays(key: string, n: number): string {
  const d = localDate(key);
  d.setDate(d.getDate() + n);
  return dateKey(d);
}
export function dayDistance(a: string, b: string): number {
  const ordinal = (k: string) => {
    const [y, m, d] = k.split("-").map(Number);
    return Date.UTC(y, m - 1, d) / 86400000;
  };
  return ordinal(b) - ordinal(a);
}
export function mondayOf(key: string): string {
  return addDays(key, -((localDate(key).getDay() + 6) % 7));
}
export function dayCapacity(day: DayCapacity): number {
  return Math.max(
    0,
    minutes(day.windowMinutes) -
      minutes(day.breakMinutes) -
      minutes(day.assignedMinutes) -
      minutes(day.bufferMinutes),
  );
}
/** Legacy availability is retained. Proposed minutes require explicit confirmation. */
export function initialPlanSettings(
  profile: StudentSubjectProfile,
): PlanSettings {
  // Availability must come from the student, never an invented year-group quota.
  return {
    days: DAYS_OF_WEEK.map(() => ({
      windowMinutes: 0,
      breakMinutes: 0,
      assignedMinutes: 0,
      bufferMinutes: 0,
    })),
    revisionMinutes: 0,
    preferredMinutes: profile.defaultBlockDuration ?? 45,
    exceptions: {},
    confirmed: false,
  };
}
export function validEvidence(input: PlanInputs): TopicEvidence[] {
  const year = examinationYearFromDate(input.profile.examStartDate);
  return input.evidence.filter((e) => {
    const spec = resolveCurriculumSpecification(e.subjectName, year);
    return (
      input.profile.curriculumLevel !== "junior" &&
      input.profile.yearGroup !== "LCA1" &&
      input.profile.yearGroup !== "LCA2" &&
      e.taught &&
      spec?.id === e.specificationId &&
      spec.groups.some(
        (g) => g.id === e.topicId || g.topics.some((t) => t.id === e.topicId),
      )
    );
  });
}
type Candidate = Omit<PlanTask, "date" | "status"> & {
  due: string;
  priority: number;
  coverage: boolean;
  afterSourceId?: string;
};
const token = (value: string) => encodeURIComponent(value);

export function buildStudyPlan(
  input: PlanInputs,
  start: string,
  previous?: StudyPlan,
  today = start,
): StudyPlan {
  const days: PlanDay[] = Array.from({ length: 14 }, (_, i) => {
    const date = addDays(start, i);
    const d =
      input.settings.exceptions[date] ??
      input.settings.days[(localDate(date).getDay() + 6) % 7];
    const safe: DayCapacity = {
      windowMinutes: minutes(d?.windowMinutes ?? 0),
      breakMinutes: minutes(d?.breakMinutes ?? 0),
      assignedMinutes: minutes(d?.assignedMinutes ?? 0),
      bufferMinutes: minutes(d?.bufferMinutes ?? 0),
    };
    return {
      ...safe,
      date,
      capacity: dayCapacity(safe),
      planned: 0,
      overload: Math.max(
        0,
        safe.assignedMinutes +
          safe.breakMinutes +
          safe.bufferMinutes -
          safe.windowMinutes,
      ),
    };
  });
  const end = addDays(start, 13);
  const tasks = (previous?.tasks ?? [])
    .filter(
      (t) =>
        (t.status !== "planned" || t.locked || t.date < today) &&
        t.date >= addDays(start, -28),
    )
    .map((t) => ({ ...t }));
  const unscheduled: StudyPlan["unscheduled"] = [];
  const notices: string[] = [];
  const evidence = validEvidence(input);
  const invalid =
    input.evidence.filter((e) => e.taught).length - evidence.length;
  if (invalid)
    notices.push(
      `${invalid} topic record(s) need curriculum matching before they can guide the plan.`,
    );
  if (!input.settings.confirmed)
    notices.push(
      "Set your available time to build your plan. There is no required number of study hours.",
    );
  if (days.some((d) => d.overload))
    notices.push(
      "Assigned work, breaks or buffer exceed a day window. No extra revision is added to that day.",
    );
  const active = input.profile.subjects;
  const candidates: Candidate[] = [];
  const contact = { ...input.lastContact };
  for (const t of tasks.filter((t) => t.status === "completed"))
    if (!contact[t.subjectName] || contact[t.subjectName] < t.date)
      contact[t.subjectName] = t.date;
  function add(
    subjectName: string,
    sourceId: string,
    title: string,
    kind: PlanTask["kind"],
    due: string,
    duration: number,
    priority: number,
    why: string,
    extra: Partial<Candidate> = {},
  ) {
    candidates.push({
      id: `${subjectName}|plan|${token(sourceId)}`,
      sourceId,
      subjectName,
      title,
      kind,
      due,
      earliest: start,
      durationMinutes: duration,
      priority,
      coverage: false,
      sessionType: kind === "practice" ? "practice" : "revision",
      why,
      steps:
        kind === "practice"
          ? [
              "Try the task without notes.",
              "Check a worked example or marking scheme.",
              "Correct one mistake and explain the change.",
            ]
          : [
              "Recall before opening your notes.",
              "Check the answer and correct a gap.",
              "Record what you could do independently.",
            ],
      next: "Record a retrieval result. Completion alone does not postpone a review.",
      ...extra,
    });
  }
  const preferred = Math.max(
    10,
    Math.min(90, minutes(input.settings.preferredMinutes)),
  );
  for (const s of active) {
    const req = input.requirements.find((r) => r.subjectName === s.subjectName);
    const gap =
      input.profile.curriculumLevel === "junior"
        ? s.currentBand && s.targetBand
          ? Math.min(
              4,
              Math.max(
                0,
                JC_BANDS.indexOf(s.currentBand) -
                  JC_BANDS.indexOf(s.targetBand),
              ),
            )
          : 0
        : s.currentGrade && s.targetGrade
          ? Math.min(4, gradeSteps(s.currentGrade, s.targetGrade))
          : 0;
    const target =
      s.currentGrade && s.targetGrade
        ? `${s.currentGrade} → ${s.targetGrade}`
        : s.currentBand && s.targetBand
          ? `${s.currentBand} → ${s.targetBand}`
          : "Grades not supplied";
    const topics = evidence.filter((e) => e.subjectName === s.subjectName);
    const staleContact = contact[s.subjectName]
      ? Math.min(90, Math.max(0, dayDistance(contact[s.subjectName], start)))
      : 30;
    for (let week = 0; week < 2; week++) {
      const anchor = addDays(start, week * 7);
      // A coverage opportunity is not a diagnosis that untaught material is weak.
      add(
        s.subjectName,
        `contact-${anchor}`,
        "A short check of recent classwork",
        "maintenance",
        anchor,
        15,
        28 + staleContact + gap + (req ? 15 : 0) - week * 5,
        `${req ? `Entry requirement: ${req.note}. ` : ""}${target}. ${contact[s.subjectName] ? `Last recorded contact: ${contact[s.subjectName]}.` : "No recent subject contact recorded."} Keep a place for this subject across the fortnight.`,
        {
          earliest: anchor,
          coverage: true,
          next: "Choose something already taught. Use the result to decide what needs practice.",
        },
      );
      for (const e of topics) {
        const key = `${e.specificationId}::${e.topicId}`;
        const due =
          e.dueOn ?? (e.result ? addDays(e.observedOn ?? anchor, 7) : anchor);
        if (due > addDays(anchor, 6) || (week === 1 && due < anchor)) continue;
        // A successful future review is never pulled forward just to fill spare time.
        const needsPractice = e.result === "failed" || e.result === "partial";
        const stale = e.observedOn
          ? dayDistance(e.observedOn, anchor) >= 14
          : true;
        if (!needsPractice && !stale && week > 0 && due < anchor) continue;
        const kind = needsPractice ? "practice" : "retrieval";
        const dueDate = due < anchor ? anchor : due;
        const reason = e.result
          ? `Last independent attempt: ${e.result}, ${e.observedOn}. Review due ${due}.`
          : "No independent retrieval result yet; start with a short check.";
        const practiceSource = `${key}-${due}-${e.observedOn ?? "unknown"}-${e.dueOn ?? "unknown"}-${e.result ?? "unknown"}`;
        add(
          s.subjectName,
          practiceSource,
          e.topicName,
          kind,
          dueDate,
          needsPractice ? preferred : 15,
          55 +
            (e.result === "failed" ? 35 : e.result === "partial" ? 22 : 0) +
            Math.min(20, Math.max(0, dayDistance(due, anchor))) +
            gap * 2 +
            (req ? 10 : 0),
          `${reason} ${target}.${e.confidence ? ` Confidence is ${e.confidence}; it is not used as proof of recall.` : ""}`,
          { earliest: dueDate, topicKey: key, suggestedTopics: [e.topicName] },
        );
        if (needsPractice && week === 0)
          add(
            s.subjectName,
            `${practiceSource}-check`,
            `${e.topicName} · delayed check`,
            "retrieval",
            addDays(dueDate, 3),
            15,
            65 + gap,
            "A brief check on a separate calendar day after correction. This is a planned check, not an assumed successful result.",
            {
              earliest: addDays(dueDate, 3),
              topicKey: key,
              suggestedTopics: [e.topicName],
              afterSourceId: practiceSource,
            },
          );
      }
    }
  }
  for (const c of input.cards)
    if (c.dueOn <= end && active.some((s) => s.subjectName === c.subjectName))
      add(
        c.subjectName,
        `cards-${c.id}`,
        "Mark Bank · due questions",
        "cards",
        c.dueOn,
        Math.max(10, c.minutes),
        110,
        `${c.cardIds.length} previously studied questions. Due ${c.dueOn} according to Mark Bank’s existing scheduler.`,
        {
          earliest: c.dueOn > start ? c.dueOn : start,
          cardIds: c.cardIds,
          next: "Grade the questions in Mark Bank. It remains the owner of their next review dates.",
        },
      );
  for (const d of input.deadlines)
    if (
      d.dueOn >= today &&
      d.dueOn <= end &&
      active.some((s) => s.subjectName === d.subjectName)
    )
      add(
        d.subjectName,
        `deadline-${d.id}`,
        d.title,
        "deadline",
        d.dueOn,
        Math.max(10, d.minutes),
        180,
        `You entered a deadline of ${d.dueOn}; preparation is placed before that date. This is additional preparation, not work already counted in the assigned-work estimate.`,
        {
          deadline: d.dueOn,
          next: "Check the milestone with your teacher. Record completion without inventing retrieval evidence.",
        },
      );
  for (const t of tasks.filter((t) => t.status !== "dropped")) {
    const d = days.find((d) => d.date === t.date);
    if (d) d.planned += t.durationMinutes;
  }
  const weekUsed = (w: number) =>
    days.slice(w * 7, w * 7 + 7).reduce((n, d) => n + d.planned, 0);
  const cap = (w: number) =>
    Math.min(
      minutes(input.settings.revisionMinutes),
      days.slice(w * 7, w * 7 + 7).reduce((n, d) => n + d.capacity, 0),
    );
  const subjectUsed = (subject: string, w: number) =>
    tasks
      .filter(
        (t) =>
          t.status !== "dropped" &&
          t.subjectName === subject &&
          t.date >= addDays(start, w * 7) &&
          t.date <= addDays(start, w * 7 + 6),
      )
      .reduce((n, t) => n + t.durationMinutes, 0);
  const pending = candidates.filter(
    (c) =>
      !tasks.some(
        (t) =>
          t.id === c.id ||
          ((c.kind === "deadline" || c.kind === "cards") &&
            t.status === "completed" &&
            t.sourceId === c.sourceId),
      ),
  );
  // Ensure scarce coverage rotates towards subjects absent from the preceding fortnight.
  pending.sort(
    (a, b) =>
      b.priority - a.priority ||
      a.due.localeCompare(b.due) ||
      a.id.localeCompare(b.id),
  );
  while (pending.length) {
    pending.sort((a, b) => {
      const score = (c: Candidate) => {
        const already = tasks.some(
          (t) =>
            t.status !== "dropped" &&
            t.subjectName === c.subjectName &&
            t.date >= start &&
            t.date <= end,
        );
        return (
          c.priority +
          (c.coverage && !already ? 20 : 0) -
          (already && c.coverage ? 50 : 0)
        );
      };
      return (
        score(b) - score(a) ||
        a.due.localeCompare(b.due) ||
        a.id.localeCompare(b.id)
      );
    });
    const c = pending.shift()!;
    const predecessor = c.afterSourceId
      ? tasks.find(
          (t) => t.sourceId === c.afterSourceId && t.status !== "dropped",
        )
      : undefined;
    const earliest = predecessor
      ? [c.earliest, addDays(predecessor.date, 3)].sort().at(-1)!
      : c.earliest;
    const options = days
      .filter(
        (d) =>
          (!c.afterSourceId || !!predecessor) &&
          d.date >= today &&
          d.date >= earliest &&
          (!c.deadline || d.date < c.deadline),
      )
      .map((d) => {
        const w = Math.floor(dayDistance(start, d.date) / 7);
        const subjectCap = Math.max(
          15,
          Math.floor(cap(w) * Math.max(0.4, 1 / Math.max(1, active.length))),
        );
        const room = Math.min(
          d.capacity - d.planned,
          cap(w) - weekUsed(w),
          c.kind === "deadline"
            ? Infinity
            : subjectCap - subjectUsed(c.subjectName, w),
        );
        const sameTopic = tasks.some(
          (t) =>
            t.status !== "dropped" &&
            t.date === d.date &&
            c.topicKey &&
            t.topicKey === c.topicKey,
        );
        const sameSubject = tasks.some(
          (t) =>
            t.status !== "dropped" &&
            t.date === d.date &&
            t.subjectName === c.subjectName,
        );
        const score =
          Math.abs(dayDistance(c.due, d.date)) * 5 +
          d.planned / 20 +
          (sameSubject ? 4 : 0);
        return { d, room, score, sameTopic };
      })
      .filter((o) => o.room >= 10 && !o.sameTopic)
      .sort((a, b) => a.score - b.score || a.d.date.localeCompare(b.d.date));
    const chosen =
      c.kind === "deadline" || c.kind === "cards"
        ? options.find((o) => o.room >= c.durationMinutes)
        : options[0];
    // A deadline/card batch is indivisible here: disclose overflow rather than hide part of it.
    if (
      !chosen ||
      ((c.kind === "deadline" || c.kind === "cards") &&
        chosen.room < c.durationMinutes)
    ) {
      unscheduled.push({
        id: c.id,
        subjectName: c.subjectName,
        title: c.title,
        minutes: c.durationMinutes,
        reason: c.deadline
          ? `No room before ${c.deadline}. Change the scope or discuss the deadline.`
          : "No suitable room within the agreed minutes, spacing and subject balance. Not added to tomorrow.",
      });
      continue;
    }
    const duration = Math.min(c.durationMinutes, chosen.room);
    const { due: _due, priority: _priority, coverage: _coverage, ...task } = c;
    tasks.push({
      ...task,
      date: chosen.d.date,
      durationMinutes: duration,
      status: "planned",
      why: `${c.why}${duration < c.durationMinutes ? ` Shortened to ${duration} minutes to fit the available time; do one small task.` : ""}`,
    });
    chosen.d.planned += duration;
  }
  for (const d of days)
    if (d.planned > d.capacity)
      notices.push(
        `${d.date}: preserved completed or manually moved work exceeds the revised day capacity by ${d.planned - d.capacity} minutes.`,
      );
  if (days.filter((d) => d.capacity > 0).length <= 2)
    notices.push(
      "With only one available day per week, within-week spacing is limited. No extra study day has been invented.",
    );
  for (let week = 0; week < 2; week++)
    if (weekUsed(week) > cap(week))
      notices.push(
        `Week ${week + 1}: preserved work exceeds the new weekly limit by ${weekUsed(week) - cap(week)} minutes. Completed work has been kept.`,
      );
  const missing = active.filter(
    (s) =>
      !tasks.some(
        (t) =>
          t.status !== "dropped" &&
          t.subjectName === s.subjectName &&
          t.date >= start &&
          t.date <= end,
      ),
  );
  if (missing.length)
    notices.push(
      `No contact fits this fortnight for ${missing.map((s) => s.subjectName).join(", ")}. These subjects stay visible for the next planning decision.`,
    );
  return {
    version: 1,
    start,
    tasks: tasks.sort(
      (a, b) => a.date.localeCompare(b.date) || a.id.localeCompare(b.id),
    ),
    days,
    unscheduled,
    notices,
  };
}

export function recordRetrieval(
  e: TopicEvidence,
  result: NonNullable<TopicEvidence["result"]>,
  on: string,
  examDate?: string | null,
): TopicEvidence {
  const successes =
    result === "independent" ? (e.successfulReviews ?? 0) + 1 : 0;
  const interval =
    result === "failed"
      ? 1
      : result === "partial"
        ? 2
        : Math.min(
            35,
            Math.max(2, Math.round(3 * Math.pow(1.8, successes - 1))),
          );
  const bounded =
    examDate && examDate > on
      ? Math.min(
          interval,
          Math.max(1, Math.floor(dayDistance(on, examDate) / 2)),
        )
      : interval;
  return {
    ...e,
    result,
    observedOn: on,
    dueOn: addDays(on, bounded),
    successfulReviews: successes,
  };
}
export function planTimetable(plan: StudyPlan, week = 0): WeeklyTimetable {
  return DAYS_OF_WEEK.map((day, i) => ({
    day,
    blocks: plan.tasks.filter(
      (t) =>
        t.date === addDays(plan.start, week * 7 + i) && t.status !== "dropped",
    ),
  }));
}

/** Keep legacy completion records visible during the local pilot; never rewrite their IDs. */
export function preserveLegacyCompletions(
  inputs: PlanInputs,
  start: string,
  completions: Record<string, string[]>,
  previous?: StudyPlan,
): StudyPlan | undefined {
  const end = addDays(start, 13);
  const tasks = [...(previous?.tasks ?? [])];
  let changed = false;
  for (const [date, ids] of Object.entries(completions)) {
    if (date < start || date > end) continue;
    for (const id of ids) {
      const existing = tasks.find((t) => t.id === id && t.date === date);
      if (existing) {
        if (existing.status !== "completed") {
          tasks[tasks.indexOf(existing)] = { ...existing, status: "completed" };
          changed = true;
        }
        continue;
      }
      const [subjectName, sessionType] = id.split("|");
      if (
        !inputs.profile.subjects.some((s) => s.subjectName === subjectName) ||
        !["practice", "revision", "new-learning"].includes(sessionType)
      )
        continue;
      tasks.push({
        id,
        sourceId: `legacy-${date}-${id}`,
        date,
        earliest: date,
        subjectName,
        sessionType: sessionType as StudyBlock["sessionType"],
        durationMinutes: inputs.profile.defaultBlockDuration ?? 45,
        title: "Previously completed session",
        kind: "maintenance",
        status: "completed",
        why: "Retained from the earlier timetable. Duration uses the saved preferred block length; the original completion did not store exact minutes.",
        steps: [],
        next: "This completion has been preserved. No recall result has been inferred.",
      });
      changed = true;
    }
  }
  return changed
    ? {
        version: 1,
        start,
        tasks,
        days: previous?.days ?? [],
        unscheduled: previous?.unscheduled ?? [],
        notices: previous?.notices ?? [],
      }
    : previous;
}
