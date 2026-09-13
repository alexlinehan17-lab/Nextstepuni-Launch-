import React, { useEffect, useLayoutEffect, useRef, useState } from "react";
import { useReducedMotion } from "../Motion";
import { useModal } from "../../hooks/useModal";
import {
  DAYS_OF_WEEK,
  type StudentSubjectProfile,
  type YearGroup,
} from "../subjectData";
import {
  getActiveCategories,
  getVisionCardsForLevel,
} from "../../northStarData";
import { isLcaYear } from "../../utils/authUtils";
import { trackFunnel } from "../../utils/funnel";
import type { NorthStar } from "../../types";
import {
  buildNorthStar,
  buildProfile,
  choiceReady,
  choicesFor,
  cycleFor,
  daysUntil,
  draftKey,
  emptyChoice,
  hasGrades,
  legacyDraftKey,
  needsDate,
  pointsFor,
  readDraft,
  subjectsFor,
  type SetupDraft,
  type SetupStep,
  type SubjectChoice,
} from "./model";
import { guestStorage } from "./guest";

export interface OnboardingProps {
  userId: string;
  userName: string;
  onComplete: (
    profile: StudentSubjectProfile,
    northStar?: NorthStar,
    essentialsMode?: boolean,
  ) => void | Promise<void>;
  onSkip: () => void;
  mode?: "fresh" | "transition-to-senior";
  transitionTargetYear?: "TY" | "5th";
  /** Guest setup (no account): the draft lives in sessionStorage via ./guest.ts,
   *  nothing is written to Firestore, and the final button reads "Dive in". */
  guest?: boolean;
}

export function PointsCount({ from, to }: { from: number; to: number }) {
  const reduced = useReducedMotion();
  const [value, setValue] = useState(from);
  useEffect(() => {
    if (reduced || from === to) {
      setValue(to);
      return;
    }
    setValue(from);
    const start = performance.now();
    let frame = 0;
    const tick = (now: number) => {
      const amount = Math.min(1, Math.max(0, (now - start) / 1450));
      setValue(Math.round(from + (to - from) * (1 - (1 - amount) ** 3)));
      if (amount < 1) frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [from, to, reduced]);
  return (
    <>
      <span className="setup-points-number" aria-hidden="true">
        {value}
      </span>
      <span className="sr-only">
        {to} target points, from {from} current points
      </span>
    </>
  );
}

export function useSetupFlow(
  {
    userId,
    userName,
    onComplete,
    onSkip,
    mode = "fresh",
    transitionTargetYear,
    guest = false,
  }: OnboardingProps,
  desktop = false,
) {
  const transition = mode === "transition-to-senior";
  // A guest's draft is tab-scoped and survives the unauthenticated-boot clear.
  const storage = guest ? guestStorage : localStorage;
  const [draft, setDraft] = useState(() =>
    readDraft(
      userId,
      mode,
      transition ? (transitionTargetYear ?? "5th") : undefined,
      storage,
    ),
  );
  const bulkGrades = desktop && draft.step === "grades";
  const [query, setQuery] = useState("");
  const [subjectGroup, setSubjectGroup] = useState("languages");
  const [visionGroup, setVisionGroup] = useState<string>("");
  const [editSnapshot, setEditSnapshot] = useState<SetupDraft | null>(null);
  const [pendingYear, setPendingYear] = useState<YearGroup | null>(null);
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState("");
  const scroller = useRef<HTMLDivElement>(null);
  const yearDialog = useRef<HTMLElement>(null);
  useModal(Boolean(pendingYear), () => setPendingYear(null), yearDialog);
  const heading = useRef<HTMLHeadingElement>(null);
  const savingRef = useRef(false);
  const latest = useRef(draft);
  const reduced = useReducedMotion();
  const junior = cycleFor(draft.year) === "junior";
  const lca = isLcaYear(draft.year ?? undefined);
  const categories = getActiveCategories(cycleFor(draft.year));
  const category = categories.find((c) => c.id === draft.category);
  const visions = getVisionCardsForLevel(cycleFor(draft.year));
  const maxVision = junior ? 3 : 5;
  const subjectList = subjectsFor(draft.year);
  const currentSubject =
    draft.gradeSubject && draft.subjects.includes(draft.gradeSubject)
      ? draft.gradeSubject
      : draft.subjects[0];
  const subjectIndex = draft.subjects.indexOf(currentSubject);
  const nextSubject = draft.subjects[subjectIndex + 1];
  const gradeStepSubject = draft.step === "grades" ? currentSubject : null;
  const config =
    draft.configs[currentSubject] ?? emptyChoice(draft.year, currentSubject);
  const gradeChoices = choicesFor(draft.year, config.level);
  const unreviewed = draft.subjects.filter(
    (name) => !draft.configs[name]?.reviewed,
  );
  const points = pointsFor(draft);
  const studyDays = DAYS_OF_WEEK.filter((day) => !draft.rest.includes(day));
  const route: SetupStep[] = transition
    ? ["subjects", "grades", "north", "vision", "schedule", "summary"]
    : [
        "welcome",
        "year",
        "north",
        "vision",
        "subjects",
        ...(lca ? [] : ["grades" as const]),
        "schedule",
        "summary",
      ];
  const stage = transition
    ? Math.max(1, route.indexOf(draft.step) + 1)
    : {
        welcome: 1,
        year: 2,
        north: 3,
        vision: 3,
        subjects: 4,
        grades: 5,
        schedule: lca ? 5 : 6,
        summary: lca ? 6 : 7,
      }[draft.step];
  const stages = transition ? route.length : lca ? 6 : 7;
  const surface =
    draft.step === "summary"
      ? "ink"
      : ["welcome", "north", "schedule"].includes(draft.step)
        ? "orange"
        : "paper";
  const patch = (value: Partial<SetupDraft>) =>
    setDraft((prev) => ({ ...prev, ...value }));

  // Persist before painting. While editing a review section, reload restores the
  // last committed review, not a half-finished edit with no Cancel route.
  useLayoutEffect(() => {
    latest.current = editSnapshot ?? draft;
    try {
      storage.setItem(draftKey(userId, mode), JSON.stringify(latest.current));
    } catch {
      /* Private browsing may block storage. */
    }
  }, [draft, editSnapshot, userId, mode, storage]);
  useEffect(() => {
    const persist = () => {
      try {
        storage.setItem(draftKey(userId, mode), JSON.stringify(latest.current));
      } catch {
        /* Keep the in-memory draft. */
      }
    };
    window.addEventListener("pagehide", persist);
    document.addEventListener("visibilitychange", persist);
    return () => {
      window.removeEventListener("pagehide", persist);
      document.removeEventListener("visibilitychange", persist);
    };
  }, [userId, mode, storage]);
  useLayoutEffect(() => {
    if (scroller.current) scroller.current.scrollTop = 0;
    heading.current?.focus({ preventScroll: true });
  }, [draft.step, gradeStepSubject]);
  useEffect(() => {
    const region = scroller.current;
    if (!region) return;
    let x = 0,
      y = 0;
    const start = (event: TouchEvent) => {
      const touch = event.touches[0];
      if (touch) {
        x = touch.clientX;
        y = touch.clientY;
      }
    };
    const move = (event: TouchEvent) => {
      const touch = event.touches[0];
      if (!touch || Math.abs(touch.clientY - y) <= Math.abs(touch.clientX - x))
        return;
      if (
        (region.scrollTop <= 0 && touch.clientY > y) ||
        (Math.ceil(region.scrollTop + region.clientHeight) >=
          region.scrollHeight &&
          touch.clientY < y)
      )
        event.preventDefault();
    };
    region.addEventListener("touchstart", start, { passive: true });
    region.addEventListener("touchmove", move, { passive: false });
    return () => {
      region.removeEventListener("touchstart", start);
      region.removeEventListener("touchmove", move);
    };
  }, []);
  useEffect(() => {
    trackFunnel("onboarding_started");
  }, []);
  useEffect(() => {
    if (draft.step === "subjects") trackFunnel("onboarding_reached_subjects");
    if (draft.step === "schedule") trackFunnel("onboarding_reached_exam_date");
  }, [draft.step]);

  const edit = (step: SetupStep, subject?: string) => {
    setEditSnapshot(draft);
    setSaveError("");
    patch({ step, ...(subject ? { gradeSubject: subject } : {}) });
  };
  const cancelEdit = () => {
    if (editSnapshot) setDraft(editSnapshot);
    setEditSnapshot(null);
    setSaveError("");
  };
  const changeYear = (year: YearGroup) => {
    const different =
      cycleFor(year) !== cycleFor(draft.year) || isLcaYear(year) !== lca;
    if (different) {
      patch({
        year,
        subjects: [],
        configs: {},
        category: null,
        vision: [],
        gradeSubject: null,
        dateConfirmed: false,
      });
      setSubjectGroup("languages");
      setVisionGroup("");
    } else patch({ year, dateConfirmed: false });
    setPendingYear(null);
  };
  const selectYear = (year: YearGroup) => {
    if (
      draft.year &&
      (draft.subjects.length || draft.category) &&
      (cycleFor(year) !== cycleFor(draft.year) || isLcaYear(year) !== lca)
    )
      setPendingYear(year);
    else changeYear(year);
  };
  const toggleSubject = (name: string) =>
    setDraft((prev) => ({
      ...prev,
      subjects: prev.subjects.includes(name)
        ? prev.subjects.filter((s) => s !== name)
        : [...prev.subjects, name],
      configs: {
        ...prev.configs,
        [name]: prev.configs[name] ?? emptyChoice(prev.year, name),
      },
    }));
  const updateGrade = (value: Partial<SubjectChoice>) =>
    setDraft((prev) => ({
      ...prev,
      configs: {
        ...prev.configs,
        [currentSubject]: { ...config, ...value, reviewed: false },
      },
    }));
  const updateBulkGrade = (name: string, value: Partial<SubjectChoice>) =>
    setDraft((prev) => {
      const updated = {
        ...(prev.configs[name] ?? emptyChoice(prev.year, name)),
        ...value,
      };
      return {
        ...prev,
        configs: {
          ...prev.configs,
          [name]: { ...updated, reviewed: choiceReady(prev.year, updated) },
        },
      };
    });
  const deferUnfilledGrades = () =>
    setDraft((prev) => ({
      ...prev,
      configs: Object.fromEntries(
        prev.subjects.map((name) => {
          const value = prev.configs[name] ?? emptyChoice(prev.year, name);
          const updated = {
            ...value,
            current: value.current || ("later" as const),
            target: value.target || ("later" as const),
          };
          return [
            name,
            { ...updated, reviewed: choiceReady(prev.year, updated) },
          ];
        }),
      ),
    }));
  const saveGrade = (later = false) => {
    const nextConfig = {
      ...config,
      ...(later ? { current: "later" as const, target: "later" as const } : {}),
      reviewed: true,
    };
    if (!choiceReady(draft.year, nextConfig)) return;
    const nextName = nextSubject;
    patch({
      configs: { ...draft.configs, [currentSubject]: nextConfig },
      gradeSubject: editSnapshot
        ? currentSubject
        : (nextName ?? currentSubject),
      step: editSnapshot
        ? "summary"
        : nextName
          ? "grades"
          : transition
            ? "north"
            : "schedule",
    });
    setEditSnapshot(null);
  };
  const validation = () => {
    if (bulkGrades) {
      const missingLevels = draft.subjects.filter(
        (name) => !draft.configs[name]?.level,
      );
      const unfinished = draft.subjects.filter(
        (name) => !choiceReady(draft.year, draft.configs[name]),
      );
      if (missingLevels.length)
        return `Choose a level for ${missingLevels.length} ${missingLevels.length === 1 ? "subject" : "subjects"}. Grades can wait.`;
      if (unfinished.length)
        return `Finish ${unfinished.length} ${unfinished.length === 1 ? "subject" : "subjects"}, or leave unfilled grades for later.`;
      return "";
    }

    if (draft.step === "year" && !draft.year)
      return "Choose your school year to continue.";
    if (draft.step === "north" && !category)
      return "Choose the reason that matters most to you.";
    if (draft.step === "vision" && !draft.vision.length)
      return "Choose at least one idea. You can change it later.";
    if (draft.step === "subjects" && !draft.subjects.length)
      return "Choose at least one subject.";
    if (draft.step === "grades" && !config.level)
      return "Choose your level. Grades can be added later.";
    if (draft.step === "grades" && !choiceReady(draft.year, config))
      return "Choose your grades, or set them later.";
    if (draft.step === "schedule" && !studyDays.length)
      return "Choose at least one study day.";
    if (
      draft.step === "schedule" &&
      needsDate(draft.year) &&
      !(daysUntil(draft.date) > 0)
    )
      return "Choose a future exam date.";
    if (
      draft.step === "schedule" &&
      needsDate(draft.year) &&
      !draft.dateConfirmed
    )
      return "Confirm your exam date to continue.";
    if (draft.step === "summary") {
      if (
        !draft.year ||
        !draft.subjects.length ||
        !category ||
        !draft.vision.length
      )
        return "Finish your year, subjects and motivation before starting.";
      if (!lca && unreviewed.length)
        return `Review ${unreviewed.length === 1 ? "the remaining subject" : `${unreviewed.length} remaining subjects`}. Grades can be set later.`;
      if (
        !studyDays.length ||
        (needsDate(draft.year) &&
          (!draft.dateConfirmed || !(daysUntil(draft.date) > 0)))
      )
        return "Review your study days and exam date.";
    }
    return "";
  };
  const problem = validation();
  const next = async () => {
    if (problem || savingRef.current) return;
    if (bulkGrades) {
      patch({
        configs: Object.fromEntries(
          Object.entries(draft.configs).map(([name, c]) => [
            name,
            { ...c, reviewed: choiceReady(draft.year, c) },
          ]),
        ),
        step: editSnapshot ? "summary" : transition ? "north" : "schedule",
      });
      setEditSnapshot(null);
      return;
    }
    if (draft.step === "grades") {
      saveGrade();
      return;
    }
    if (editSnapshot) {
      patch({ step: "summary" });
      setEditSnapshot(null);
      return;
    }
    if (draft.step === "summary") {
      savingRef.current = true;
      setSaving(true);
      setSaveError("");
      try {
        await onComplete(buildProfile(draft), buildNorthStar(draft), false);
        trackFunnel("onboarding_completed");
        // Keep this account-scoped draft for a delayed offline-write rollback.
        // The app's completed-onboarding gate, not local storage, owns success.
      } catch {
        setSaveError(
          "We couldn’t save your setup. Your answers are still here. Please try again.",
        );
      } finally {
        savingRef.current = false;
        setSaving(false);
      }
      return;
    }
    const step = route[route.indexOf(draft.step) + 1];
    patch({
      step,
      ...(step === "grades"
        ? { gradeSubject: unreviewed[0] ?? draft.subjects[0] }
        : {}),
    });
  };
  const back = () => {
    if (editSnapshot) {
      cancelEdit();
      return;
    }
    if (draft.step === "grades" && !bulkGrades && subjectIndex > 0) {
      patch({ gradeSubject: draft.subjects[subjectIndex - 1] });
      return;
    }
    if (draft.step === "welcome") {
      trackFunnel("onboarding_skipped");
      try {
        storage.removeItem(draftKey(userId, mode));
        storage.removeItem(legacyDraftKey(userId, mode));
      } catch {
        /* Optional storage. */
      }
      onSkip();
      return;
    }
    patch({ step: route[Math.max(0, route.indexOf(draft.step) - 1)] });
  };
  const title = {
    welcome: "Make your mark.",
    year: "Where are you now?",
    north: "What’s driving you?",
    vision: "Picture your future.",
    subjects: "Make it yours.",
    grades: currentSubject || "Your grades.",
    schedule: "Make room for progress.",
    summary: guest
      ? "You’re ready."
      : `You’re ready, ${userName.trim().split(/\s+/)[0] || "let’s go"}.`,
  }[draft.step];
  const intro = {
    welcome: "Your future. Your next step.",
    year: "Your starting point",
    north: "Your North Star · 1 of 2",
    vision: "Your North Star · 2 of 2",
    subjects: "Your subjects",
    grades: `Subject ${Math.max(1, draft.subjects.indexOf(currentSubject) + 1)} of ${draft.subjects.length}`,
    schedule: "A rhythm that works for you",
    summary: "This is your starting line",
  }[draft.step];
  const gradeLabel = (name: string) => {
    const value = draft.configs[name];
    if (!value?.reviewed) return "Not reviewed";
    const format = (grade: string) => (grade === "later" ? "Set later" : grade);
    return hasGrades(draft.year, value)
      ? `${value.current} → ${value.target}`
      : `${format(value.current)} → ${format(value.target)}`;
  };

  return {
    draft,
    setDraft,
    patch,
    query,
    setQuery,
    subjectGroup,
    setSubjectGroup,
    visionGroup,
    setVisionGroup,
    editSnapshot,
    pendingYear,
    setPendingYear,
    saving,
    saveError,
    scroller,
    heading,
    yearDialog,
    reduced,
    junior,
    lca,
    categories,
    category,
    visions,
    maxVision,
    subjectList,
    currentSubject,
    nextSubject,
    config,
    gradeChoices,
    points,
    studyDays,
    stage,
    stages,
    surface,
    edit,
    updateGrade,
    saveGrade,
    changeYear,
    selectYear,
    toggleSubject,
    problem,
    next,
    back,
    title,
    intro,
    gradeLabel,
    transition,
    guest,
    userName,
    bulkGrades,
    updateBulkGrade,
    deferUnfilledGrades,
  };
}
