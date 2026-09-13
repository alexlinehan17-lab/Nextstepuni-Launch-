import React, { type RefObject } from "react";
import { ArrowRight } from "lucide-react";
import {
  choicesFor,
  choiceReady,
  cycleFor,
  emptyChoice,
  pointsFor,
  type GradeChoice,
  type SetupDraft,
  type SubjectChoice,
} from "./model";
import type { Level } from "../subjectData";
import { getSubjectFill } from "../../utils/subjectColors";
import "./grade-options.css";

export type GradeLayout = "sheet" | "buttons" | "sliders" | "single";
export const gradeLayouts: {
  id: GradeLayout;
  title: string;
  description: string;
}[] = [
  {
    id: "sheet",
    title: "A · Grade sheet",
    description:
      "Compact rows. Tab through every subject. My pick for the clearest desktop overview.",
  },
  {
    id: "buttons",
    title: "B · Tap grades",
    description:
      "Every grade is visible. One click per choice, with no menus to open.",
  },
  {
    id: "sliders",
    title: "C · Visual targets",
    description:
      "Move the two handles for each subject. More playful, with the grade shown as you move.",
  },
  {
    id: "single",
    title: "Original · One by one",
    description:
      "The original flow, with larger grade bars. One subject per screen.",
  },
];

export function GradeLayoutPicker({
  layout,
  onChange,
}: {
  layout: GradeLayout;
  onChange: (layout: GradeLayout) => void;
}) {
  return (
    <aside className="grade-layout-picker" aria-label="Compare grade layouts">
      <div className="grade-layout-buttons">
        <span>TRY A LAYOUT</span>
        {gradeLayouts.map((item) => (
          <button
            key={item.id}
            type="button"
            aria-pressed={layout === item.id}
            onClick={() => onChange(item.id)}
          >
            {item.title}
          </button>
        ))}
      </div>
      <p>
        {gradeLayouts.find((item) => item.id === layout)?.description}
        <span>Your choices carry across all four views.</span>
      </p>
    </aside>
  );
}

interface Props {
  draft: SetupDraft;
  layout: Exclude<GradeLayout, "single">;
  headingRef: RefObject<HTMLHeadingElement | null>;
  onUpdate: (name: string, value: Partial<SubjectChoice>) => void;
  onDefer: () => void;
}

export default function GradeOptions({
  draft,
  layout,
  headingRef,
  onUpdate,
  onDefer,
}: Props) {
  const junior = cycleFor(draft.year) === "junior";
  const counted = {
    ...draft,
    configs: Object.fromEntries(
      Object.entries(draft.configs).map(([name, c]) => [
        name,
        { ...c, reviewed: choiceReady(draft.year, c) },
      ]),
    ),
  };
  const points = pointsFor(counted);
  const complete = draft.subjects.filter((name) =>
    choiceReady(draft.year, draft.configs[name]),
  ).length;
  const display = (value: GradeChoice) =>
    value === "later" ? "Later" : value || "—";
  const setLevel = (name: string, level: Level) =>
    onUpdate(name, { level, ...(junior ? {} : { current: "", target: "" }) });
  const levelControl = (name: string, config: SubjectChoice) => (
    <label className="grade-level">
      <span className="sr-only">{name} level</span>
      {config.level === "common" ? (
        <span>Common</span>
      ) : (
        <select
          aria-label={`${name} level`}
          value={config.level || ""}
          onChange={(event) => setLevel(name, event.target.value as Level)}
        >
          <option value="" disabled>
            Level
          </option>
          <option value="higher">Higher</option>
          <option value="ordinary">Ordinary</option>
        </select>
      )}
    </label>
  );
  const gradeControl = (
    name: string,
    config: SubjectChoice,
    field: "current" | "target",
  ) => {
    const grades = choicesFor(draft.year, config.level);
    const accessible = `${name} ${field} ${junior ? "band" : "grade"}`;
    if (layout === "sheet")
      return (
        <label className={`grade-value grade-value-${field}`}>
          <span className="sr-only">{accessible}</span>
          <select
            aria-label={accessible}
            disabled={!config.level}
            value={config[field]}
            onChange={(event) =>
              onUpdate(name, { [field]: event.target.value as GradeChoice })
            }
          >
            <option value="" disabled>
              Choose
            </option>
            {grades.map((grade) => (
              <option value={grade} key={grade}>
                {grade}
              </option>
            ))}
            <option value="later">Set later</option>
          </select>
        </label>
      );
    if (layout === "buttons")
      return (
        <fieldset className={`grade-button-line grade-button-${field}`}>
          <legend>{field === "current" ? "Current" : "Target"}</legend>
          <div className="grade-button-choices">
            {grades.map((grade) => (
              <button
                key={grade}
                type="button"
                aria-label={`${name} ${field}: ${grade}`}
                aria-pressed={config[field] === grade}
                onClick={() =>
                  onUpdate(name, { [field]: grade as GradeChoice })
                }
              >
                {grade}
              </button>
            ))}
            <button
              type="button"
              disabled={!config.level}
              className="grade-later"
              aria-label={`${name} ${field}: set later`}
              aria-pressed={config[field] === "later"}
              onClick={() => onUpdate(name, { [field]: "later" })}
            >
              Later
            </button>
          </div>
        </fieldset>
      );
    const ascending = [...grades].reverse();
    const value = Math.max(0, ascending.indexOf(config[field]) + 1);
    return (
      <div className={`grade-slider grade-slider-${field}`}>
        <label>
          <span>
            {field === "current" ? "Current" : "Target"}
            <strong>{display(config[field])}</strong>
          </span>
          <input
            type="range"
            min={0}
            max={Math.max(1, ascending.length)}
            step={1}
            value={value}
            disabled={!config.level}
            aria-label={accessible}
            aria-valuetext={config[field] ? display(config[field]) : "Not set"}
            style={
              {
                "--grade-position": `${ascending.length ? (value / ascending.length) * 100 : 0}%`,
              } as React.CSSProperties
            }
            onChange={(event) =>
              onUpdate(name, {
                [field]: (ascending[Number(event.target.value) - 1] ||
                  "") as GradeChoice,
              })
            }
          />
        </label>
        <div className="grade-slider-scale">
          <span>—</span>
          <span>{ascending[0] || "Choose a level"}</span>
          <span>{ascending[ascending.length - 1]}</span>
          <button
            type="button"
            disabled={!config.level}
            onClick={() => onUpdate(name, { [field]: "later" })}
            aria-label={`${name} ${field}: set later`}
          >
            Set later
          </button>
        </div>
      </div>
    );
  };
  return (
    <>
      <section className="desk-story grade-overview">
        <p className="setup-eyebrow">Your subjects & goals</p>
        <h1 ref={headingRef} tabIndex={-1}>
          Your grades.
        </h1>
        <p className="desk-introduction">
          Where you are now.
          <br />
          Where you want to go.
        </p>
        {!junior ? (
          <>
            <div className="grade-points-bars" aria-label="Live points preview">
              {(["current", "target"] as const).map((field) => (
                <div key={field}>
                  <div className="grade-points-rail">
                    <div
                      data-target={field === "target"}
                      style={{ height: `${(points[field] / 625) * 100}%` }}
                    />
                  </div>
                  <strong>{points.count ? points[field] : "—"}</strong>
                  <span>
                    {field === "current" ? "Current points" : "Target points"}
                  </span>
                </div>
              ))}
            </div>
            <p className="grade-points-caption">
              {points.count
                ? `Best-six total from ${points.count} subjects with both grades set.`
                : "Add your grades to see your points take shape."}
            </p>
            {points.count > 0 && (
              <p className="grade-points-gain">
                <ArrowRight size={16} />
                {points.target - points.current > 0 ? "+" : ""}
                {points.target - points.current} points to aim for
              </p>
            )}
          </>
        ) : (
          <img
            className="desk-story-art"
            src="/icons/onboarding/subjects.png"
            alt=""
          />
        )}
        <div className="grade-completion">
          <span>
            {complete} of {draft.subjects.length} subjects ready
          </span>
          <div>
            <span
              style={{
                width: `${draft.subjects.length ? (complete / draft.subjects.length) * 100 : 0}%`,
              }}
            />
          </div>
        </div>
      </section>
      <section
        className={`desk-choices grade-workspace grade-workspace-${layout}`}
        aria-label="All subject grades"
      >
        <div className="grade-workspace-heading">
          <h2>All subjects, one page.</h2>
          <p>Grades can change. This is just a starting point.</p>
        </div>
        {layout === "sheet" && (
          <div className="grade-sheet-head" aria-hidden="true">
            <span>Subject</span>
            <span>Level</span>
            <span>Current</span>
            <span>Target</span>
          </div>
        )}
        <div className="grade-rows">
          {draft.subjects.map((name) => {
            const config = draft.configs[name] ?? emptyChoice(draft.year, name);
            return (
              <section
                className="grade-subject-row"
                key={name}
                aria-label={name}
              >
                <div className="grade-subject-heading">
                  <h3>
                    <i style={{ background: getSubjectFill(name) }} />
                    {name}
                  </h3>
                  {layout !== "sheet" && levelControl(name, config)}
                </div>
                {layout === "sheet" && levelControl(name, config)}
                {layout !== "sheet" && !config.level ? (
                  <p className="grade-needs-level">
                    Choose a level to see the grades.
                  </p>
                ) : (
                  <div className="grade-pair">
                    {gradeControl(name, config, "current")}
                    {gradeControl(name, config, "target")}
                  </div>
                )}
              </section>
            );
          })}
        </div>
        <div className="grade-workspace-footer">
          <button type="button" onClick={onDefer}>
            Leave unfilled grades for later
          </button>
          <span>Your level stays saved.</span>
        </div>
      </section>
    </>
  );
}
