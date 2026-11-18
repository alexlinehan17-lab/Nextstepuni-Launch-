/** Explicitly synthetic review fixtures. Curriculum identities are resolved from the shared registry. */
import {
  examinationYearFromDate,
  resolveCurriculumSpecification,
} from "../curriculumRegistry";
import type { Grade, StudentSubjectProfile } from "../components/subjectData";
import {
  addDays,
  initialPlanSettings,
  type PlanInputs,
  type TopicEvidence,
} from "../services/studyPlanEngine";

export const SAMPLE_START = "2026-11-02";
export const SAMPLE_CASES = {
  fifth: "Fifth year · 5h commitment",
  sixth: "Sixth year · 8h commitment",
  three: "Three days · a constrained week",
  coursework: "Coursework week · very little room",
};
export type StudySample = keyof typeof SAMPLE_CASES;
export function studyPlannerSample(key: StudySample): PlanInputs {
  const year = key === "fifth" ? "5th" : "6th";
  const profile: StudentSubjectProfile = {
    yearGroup: year,
    curriculumLevel: "senior",
    examStartDate: year === "5th" ? "2028-06-07" : "2027-06-09",
    restDays: year === "5th" ? ["Friday"] : [],
    defaultBlockDuration: 45,
    createdAt: SAMPLE_START,
    updatedAt: SAMPLE_START,
    subjects: [
      {
        subjectName: "Mathematics",
        level: "higher",
        currentGrade: "H5",
        targetGrade: "H2",
      },
      {
        subjectName: "Biology",
        level: "higher",
        currentGrade: "H4",
        targetGrade: "H2",
      },
      {
        subjectName: "English",
        level: "higher",
        currentGrade: "H3",
        targetGrade: "H2",
      },
      {
        subjectName: "Irish",
        level: "ordinary",
        currentGrade: "O4",
        targetGrade: "O2",
      },
      {
        subjectName: "French",
        level: "higher",
        currentGrade: "H4",
        targetGrade: "H3",
      },
      {
        subjectName: "History",
        level: "higher",
        currentGrade: "H3",
        targetGrade: "H2",
      },
      {
        subjectName: "Geography",
        level: "higher",
        currentGrade: "H3",
        targetGrade: "H2",
      },
    ],
  };
  const settings = initialPlanSettings(profile);
  settings.confirmed = true;
  const sixth = year === "6th";
  const windows = sixth
    ? [165, 165, 135, 165, 75, 270, 165]
    : [135, 135, 105, 135, 0, 200, 100];
  const assigned = sixth
    ? [90, 90, 120, 90, 60, 60, 30]
    : [75, 75, 90, 75, 0, 60, 45];
  const breaks = sixth
    ? [15, 15, 15, 15, 15, 30, 15]
    : [15, 15, 15, 15, 0, 20, 10];
  settings.days = windows.map((windowMinutes, i) => ({
    windowMinutes,
    assignedMinutes: assigned[i],
    breakMinutes: breaks[i],
    bufferMinutes: 0,
  }));
  settings.revisionMinutes = sixth ? 480 : 300;
  if (key === "three") {
    settings.days = settings.days.map((d, i) =>
      [1, 3, 5].includes(i)
        ? {
            ...d,
            windowMinutes: i === 5 ? 195 : 135,
            breakMinutes: 15,
            assignedMinutes: 60,
          }
        : {
            windowMinutes: 0,
            breakMinutes: 0,
            assignedMinutes: 0,
            bufferMinutes: 0,
          },
    );
    settings.revisionMinutes = 300;
  }
  if (key === "coursework") {
    settings.days = settings.days.map((d, i) => ({
      ...d,
      assignedMinutes: Math.max(
        0,
        d.windowMinutes - d.breakMinutes - ([1, 5].includes(i) ? 30 : 0),
      ),
    }));
    settings.revisionMinutes = 180;
  }
  const evidence: TopicEvidence[] = [];
  const add = (
    subjectName: string,
    pattern: RegExp,
    result: TopicEvidence["result"],
    due: number,
    taught = true,
  ) => {
    const spec = resolveCurriculumSpecification(
      subjectName,
      examinationYearFromDate(profile.examStartDate),
    );
    if (!spec) throw new Error(`Missing sample specification: ${subjectName}`);
    const nodes = spec.groups.flatMap((g) => [
      ...g.topics,
      { id: g.id, title: g.title },
    ]);
    const topic = nodes.find((t) => pattern.test(t.title)) ?? nodes[0];
    if (!topic) throw new Error(`Missing sample topic: ${subjectName}`);
    evidence.push({
      specificationId: spec.id,
      topicId: topic.id,
      subjectName,
      topicName: topic.title,
      taught,
      result,
      observedOn: addDays(SAMPLE_START, -4),
      dueOn: addDays(SAMPLE_START, due),
      confidence: result === "independent" ? "solid" : "shaky",
      successfulReviews: result === "independent" ? 2 : 0,
    });
  };
  add("Mathematics", /algebra/i, "failed", 0);
  add("Mathematics", /trigon/i, "partial", 3);
  add("Biology", /genetic|inherit|continuity/i, "partial", 1);
  add("English", /poetry|poet/i, "independent", 9);
  add("Irish", /oral|spoken|communication/i, "partial", 2);
  add("French", /reading|reception/i, "independent", 4);
  add("Geography", /tectonic|physical/i, undefined, 0);
  add("Biology", /ecolog|environment/i, undefined, 0, false);
  return {
    profile,
    settings,
    evidence,
    requirements: [
      {
        subjectName: "Irish",
        note: "O2 target for the sample student’s stated entry requirement; protect it even outside the best six.",
      },
    ],
    deadlines: [
      {
        id: "maths-class-test",
        subjectName: "Mathematics",
        title: "Prepare for the algebra class test",
        dueOn: addDays(SAMPLE_START, 3),
        minutes: 25,
      },
    ],
    cards: [
      {
        id: "sample-french-questions",
        subjectName: "French",
        dueOn: addDays(SAMPLE_START, 2),
        cardIds: [
          "sample-french-1",
          "sample-french-2",
          "sample-french-3",
          "sample-french-4",
        ],
        minutes: 15,
      },
    ],
    lastContact: Object.fromEntries(
      profile.subjects.map((s, i) => [
        s.subjectName,
        addDays(SAMPLE_START, -(i === 5 ? 18 : i + 3)),
      ]),
    ),
  };
}
export function sampleGradeOptions(grade?: Grade): Grade[] {
  return (
    grade?.startsWith("O")
      ? ["O1", "O2", "O3", "O4", "O5", "O6", "O7", "O8"]
      : ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8"]
  ) as Grade[];
}
