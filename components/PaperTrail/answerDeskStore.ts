/** Student-authored work is separate from triage/self-mark data.
 * The shared-device policy clears local drafts on sign-out; the desk explains
 * this and offers an export. There is no additional practice-history expiry. */
export interface InkStroke {
  points: [number, number][];
  kind: "pen" | "highlight";
  colour: string;
}
export type PageInk = Record<string, InkStroke[]>;
export interface WrittenResponse {
  text: string;
  ink: PageInk;
}
export interface AnswerRecord {
  v: 1;
  revision: number;
  updatedAt: number;
  draft: WrittenResponse;
  first: WrittenResponse | null;
  retry: WrittenResponse;
  correction: string;
  correctionInk: PageInk;
  confidence: string;
  phase: "attempt" | "compare" | "retry" | "done";
  mode: "type" | "ink" | "copybook";
}
export const emptyResponse = (): WrittenResponse => ({ text: "", ink: {} });
export const emptyAnswer = (): AnswerRecord => ({
  v: 1,
  revision: 0,
  updatedAt: 0,
  draft: emptyResponse(),
  first: null,
  retry: emptyResponse(),
  correction: "",
  correctionInk: {},
  confidence: "",
  phase: "attempt",
  mode: "type",
});
const responseKey = (ns: string, id: string) =>
  `pt:written:v1:${encodeURIComponent(ns)}:${encodeURIComponent(id)}`;
const preferenceKey = (ns: string) =>
  `pt:attempt-first:v1:${encodeURIComponent(ns.split("|")[0])}`;
export function loadAttemptFirst(ns: string): boolean {
  try {
    return localStorage.getItem(preferenceKey(ns)) !== "off";
  } catch {
    return true;
  }
}
export function saveAttemptFirst(ns: string, on: boolean): boolean {
  try {
    localStorage.setItem(preferenceKey(ns), on ? "on" : "off");
    return true;
  } catch {
    return false;
  }
}
export function loadDeskQuestion(ns: string): string | null {
  try {
    return localStorage.getItem(`pt:written-place:${ns}`);
  } catch {
    return null;
  }
}
export function saveDeskQuestion(ns: string, id: string) {
  try {
    localStorage.setItem(`pt:written-place:${ns}`, id);
  } catch {
    /* Work has its own save status. */
  }
}
function validInk(value: unknown): value is PageInk {
  return (
    !!value &&
    typeof value === "object" &&
    !Array.isArray(value) &&
    Object.entries(value).every(
      ([page, strokes]) =>
        /^\d+$/.test(page) &&
        Number(page) > 0 &&
        Array.isArray(strokes) &&
        strokes.every(
          (s) =>
            s &&
            ["pen", "highlight"].includes(s.kind) &&
            /^#[0-9a-f]{6}$/i.test(s.colour) &&
            Array.isArray(s.points) &&
            s.points.every(
              (p: unknown) =>
                Array.isArray(p) &&
                p.length === 2 &&
                p.every(
                  (v) =>
                    typeof v === "number" &&
                    Number.isFinite(v) &&
                    v >= 0 &&
                    v <= 1,
                ),
            ),
        ),
    )
  );
}
function validResponse(value: unknown): value is WrittenResponse {
  const r = value as WrittenResponse;
  return !!r && typeof r.text === "string" && validInk(r.ink);
}
function validRecord(value: unknown): value is AnswerRecord {
  const r = value as AnswerRecord;
  return (
    !!r &&
    r.v === 1 &&
    Number.isInteger(r.revision) &&
    r.revision >= 0 &&
    Number.isFinite(r.updatedAt) &&
    validResponse(r.draft) &&
    (r.first === null || validResponse(r.first)) &&
    validResponse(r.retry) &&
    validInk(r.correctionInk) &&
    typeof r.correction === "string" &&
    typeof r.confidence === "string" &&
    ["attempt", "compare", "retry", "done"].includes(r.phase) &&
    ["type", "ink", "copybook"].includes(r.mode)
  );
}
export function readAnswer(
  ns: string,
  id: string,
): { record: AnswerRecord; problem?: string } {
  try {
    const raw = localStorage.getItem(responseKey(ns, id));
    if (!raw) return { record: emptyAnswer() };
    const record: unknown = JSON.parse(raw);
    if (!validRecord(record)) throw Error("invalid");
    return { record };
  } catch {
    return {
      record: emptyAnswer(),
      problem:
        "This browser could not read the saved attempt. Download your new work before leaving.",
    };
  }
}
export function writeAnswer(
  ns: string,
  id: string,
  record: AnswerRecord,
): { record: AnswerRecord; problem?: string } {
  const current = readAnswer(ns, id);
  if (current.problem) return { record, problem: current.problem };
  if (current.record.revision !== record.revision)
    return {
      record,
      problem:
        "This attempt changed in another tab. Your current work is still here; download it before leaving.",
    };
  const next = {
    ...record,
    revision: record.revision + 1,
    updatedAt: Date.now(),
  };
  try {
    localStorage.setItem(responseKey(ns, id), JSON.stringify(next));
    return { record: next };
  } catch {
    return {
      record,
      problem:
        "This browser could not save your latest work. Keep this tab open and download a copy.",
    };
  }
}
export function keepFirstAttempt(record: AnswerRecord): AnswerRecord {
  return {
    ...record,
    first: record.first ?? JSON.parse(JSON.stringify(record.draft)),
    phase: "compare",
  };
}
export const hasResponse = (r: WrittenResponse) =>
  !!r.text.trim() || Object.values(r.ink).some((strokes) => strokes.length > 0);
const escape = (s: string) =>
  s.replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ]!,
  );
function inkHtml(ink: PageInk): string {
  return Object.entries(ink)
    .filter(([, s]) => s.length)
    .map(
      ([p, strokes]) =>
        `<h3>Handwriting · page ${escape(p)}</h3><svg viewBox="0 0 1000 1414" xmlns="http://www.w3.org/2000/svg">${strokes.map((s) => `<polyline fill="none" stroke="${escape(s.colour)}" stroke-width="${s.kind === "highlight" ? 20 : 3}" opacity="${s.kind === "highlight" ? 0.25 : 1}" stroke-linecap="round" stroke-linejoin="round" points="${s.points.map(([x, y]) => `${x * 1000},${y * 1414}`).join(" ")}"/>`).join("")}</svg>`,
    )
    .join("");
}
export function answerCopy(
  title: string,
  label: string,
  r: AnswerRecord,
): string {
  const section = (heading: string, response: WrittenResponse) =>
    `<section><h2>${heading}</h2><pre>${escape(response.text || "No typed response.")}</pre>${inkHtml(response.ink)}</section>`;
  return `<!doctype html><html lang="en"><meta charset="utf-8"><title>${escape(title)} — ${escape(label)}</title><style>body{font:16px/1.6 system-ui;max-width:850px;margin:40px auto;padding:20px;color:#222}h1,h2{font-family:Georgia}pre{white-space:pre-wrap;font:inherit}section{border-top:1px solid #bbb;margin-top:30px}svg{width:100%;max-height:800px;border:1px solid #bbb;background:#fff}p{color:#555}</style><h1>${escape(title)}</h1><p>${escape(label)} · NextStepUni practice work</p>${section(r.first ? "First attempt" : "Current attempt", r.first ?? r.draft)}${r.first ? section("Latest working", r.draft) : ""}<section><h2>What I noticed</h2><pre>${escape(r.correction)}</pre>${inkHtml(r.correctionInk)}</section>${hasResponse(r.retry) ? section("Second attempt", r.retry) : ""}<p>Handwriting is exported separately from the original exam page. Keep the paper beside this copy. This is student practice work, not an official marked script.</p></html>`;
}
