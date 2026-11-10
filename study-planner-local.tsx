import { useState, useSyncExternalStore } from "react";
import { createRoot } from "react-dom/client";
import DatedPlanner from "./components/launchpad/DatedPlanner";
import {
  SAMPLE_CASES,
  SAMPLE_START,
  studyPlannerSample,
  sampleGradeOptions,
  type StudySample,
} from "./data/studyPlannerSamples";
import {
  createStudyPlan,
  readStudyPlan,
  subscribeStudyPlan,
} from "./services/studyPlanStore";
import type { Grade } from "./components/subjectData";
import "./index.css";

const scopeFor = (key: StudySample) => `local-review-${key}`;
for (const key of Object.keys(SAMPLE_CASES) as StudySample[])
  if (!readStudyPlan(scopeFor(key)))
    createStudyPlan(
      scopeFor(key),
      studyPlannerSample(key),
      SAMPLE_START,
      SAMPLE_START,
      true,
    );
function Review() {
  const [sample, setSample] = useState<StudySample>("fifth");
  const scope = scopeFor(sample);
  const saved = useSyncExternalStore(
    subscribeStudyPlan,
    () => readStudyPlan(scope),
    () => undefined,
  )!;
  const [missed, setMissed] = useState(false);
  const changeGrade = (
    subject: string,
    field: "currentGrade" | "targetGrade",
    value: string,
  ) =>
    createStudyPlan(
      scope,
      {
        ...saved.inputs,
        profile: {
          ...saved.inputs.profile,
          subjects: saved.inputs.profile.subjects.map((s) =>
            s.subjectName === subject ? { ...s, [field]: value as Grade } : s,
          ),
        },
      },
      SAMPLE_START,
      SAMPLE_START,
    );
  return (
    <>
      <div className="dp-review-bar">
        <div>
          <strong>LOCAL WORKING REVIEW / SAMPLE DATA ONLY</strong>
          <select
            aria-label="Test student"
            value={sample}
            onChange={(e) => {
              setSample(e.target.value as StudySample);
              setMissed(false);
            }}
          >
            {Object.entries(SAMPLE_CASES).map(([id, title]) => (
              <option key={id} value={id}>
                {title}
              </option>
            ))}
          </select>
          <button
            onClick={() =>
              createStudyPlan(
                scope,
                studyPlannerSample(sample),
                SAMPLE_START,
                SAMPLE_START,
                true,
              )
            }
          >
            Reset this sample
          </button>
          <button aria-pressed={missed} onClick={() => setMissed(!missed)}>
            {missed ? "Return to Monday" : "View after a missed Monday"}
          </button>
          <button
            onClick={() => document.documentElement.classList.toggle("dark")}
          >
            Switch theme
          </button>
        </div>
      </div>
      <div className="dp-review-inputs">
        <details>
          <summary>
            The student behind this timetable — subjects, targets and evidence
          </summary>
          <p>
            A synthetic {saved.inputs.profile.yearGroup}-year student, week
            beginning 2 November 2026. No live account is connected. Change a
            grade, open “Shape my week”, record a retrieval result, move a task
            or test a smaller week. Changes persist separately for each sample
            on this browser.
          </p>
          <div className="dp-table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Subject</th>
                  <th>Current</th>
                  <th>Target</th>
                  <th>Learning evidence that affects the plan</th>
                </tr>
              </thead>
              <tbody>
                {saved.inputs.profile.subjects.map((s) => (
                  <tr key={s.subjectName}>
                    <td>
                      {s.subjectName}
                      <br />
                      <small>{s.level}</small>
                    </td>
                    {(["currentGrade", "targetGrade"] as const).map((field) => (
                      <td key={field}>
                        <select
                          aria-label={`${s.subjectName} ${field}`}
                          value={s[field]}
                          onChange={(e) =>
                            changeGrade(s.subjectName, field, e.target.value)
                          }
                        >
                          {sampleGradeOptions(s[field]).map((g) => (
                            <option key={g}>{g}</option>
                          ))}
                        </select>
                      </td>
                    ))}
                    <td>
                      {saved.inputs.evidence
                        .filter((e) => e.subjectName === s.subjectName)
                        .map((e) => (
                          <div key={e.topicId}>
                            {e.topicName}:{" "}
                            {e.taught
                              ? `${e.result ?? "no independent result"} · due ${e.dueOn}`
                              : "not yet taught — excluded"}
                          </div>
                        ))}
                      {s.subjectName === "History" &&
                        "Last contact 18 days ago; short maintenance, no invented topic gap."}
                      {s.subjectName === "Irish" && (
                        <div>
                          Explicit O2 entry requirement, regardless of best-six
                          points.
                        </div>
                      )}
                      {s.subjectName === "French" && (
                        <div>
                          Four sample Mark Bank questions due 4 November; their
                          scheduler owns the dates.
                        </div>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p>
            Mathematics also has a 25-minute class-test preparation deadline on
            Thursday 5 November. The fifth-year example has 12 hours of focused
            schoolwork available, 7 already assigned and a 5-hour revision
            commitment; clock windows additionally reserve breaks. The engine
            can leave time unused when suitable evidence-based tasks do not fill
            it.
          </p>
        </details>
      </div>
      <DatedPlanner
        key={scope}
        scope={scope}
        sample
        today={missed ? "2026-11-03" : SAMPLE_START}
      />
    </>
  );
}
createRoot(document.getElementById("root")!).render(<Review />);
