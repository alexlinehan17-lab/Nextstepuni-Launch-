/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Local, scheme-point matching. Award only whole, published marking points;
 * partial credit is the sum of the points supported by the student's answer.
 * A failed match means "not recognised", not proof that the answer is wrong.
 * Printed alternatives and common grammatical forms are accepted, but a bag
 * containing 60% of a scheme sentence is no longer treated as its meaning.
 */
export interface MarkPoint {
  id: string;
  verbatim: string;
  marks: number;
  /** Each alternative is a list of phrases that must all be supported. */
  accept?: string[][];
  /** Optional labels binding a point to its part of a multipart response. */
  labels?: string[];
}
export interface PointHit {
  id: string;
  marks: number;
  matched: boolean;
}
export interface MarkResult {
  earned: number;
  total: number;
  hits: PointHit[];
}

// Grammatical filler only. Meaningful qualifiers (not, same, opposite, only,
// high, low, direct, inverse, ...) must survive matching.
const STOP = new Set(
  "a an the and or of to in on at by for with from as is are was were be been being it its this that these those their they them he she his her we our you your i my into during after before which who what such can will would could may should has have had having do does did e.g i.e etc also used use name explain named accept".split(
    /\s+/,
  ),
);
const FORMS: Record<string, string> = {
  detect: "detect",
  detects: "detect",
  detected: "detect",
  detecting: "detect",
  detection: "detect",
  charge: "charge",
  charged: "charge",
  charges: "charge",
  broken: "break",
  breaks: "break",
  breaking: "break",
  measure: "measure",
  measures: "measure",
  measured: "measure",
  measuring: "measure",
  measurement: "measure",
  lose: "loss",
  loses: "loss",
  losing: "loss",
  lost: "loss",
  loss: "loss",
  gain: "gain",
  gains: "gain",
  gained: "gain",
  gaining: "gain",
  absorb: "absorb",
  absorbs: "absorb",
  absorbed: "absorb",
  absorbing: "absorb",
  absorption: "absorb",
  contract: "contract",
  contracts: "contract",
  contracting: "contract",
  contraction: "contract",
  contractions: "contract",
  protect: "protect",
  protects: "protect",
  protected: "protect",
  protecting: "protect",
  protection: "protect",
  increase: "increase",
  increases: "increase",
  increased: "increase",
  increasing: "increase",
  decrease: "decrease",
  decreases: "decrease",
  decreased: "decrease",
  decreasing: "decrease",
  move: "motion",
  moves: "motion",
  moving: "motion",
  movement: "motion",
  motion: "motion",
  multiply: "multiply",
  multiplied: "multiply",
  multiplying: "multiply",
  times: "multiply",
  carry: "carry",
  carries: "carry",
  carried: "carry",
  carrying: "carry",
  cause: "cause",
  causes: "cause",
  caused: "cause",
  causing: "cause",
  change: "change",
  changes: "change",
  changed: "change",
  changing: "change",
  produce: "produce",
  produces: "produce",
  produced: "produce",
  producing: "produce",
  production: "produce",
  remove: "remove",
  removes: "remove",
  removed: "remove",
  removing: "remove",
  removal: "remove",
  stop: "stop",
  stops: "stop",
  stopped: "stop",
  stopping: "stop",
  flow: "flow",
  flows: "flow",
  flowing: "flow",
  directly: "direct",
  inversely: "inverse",
  esophagus: "oesophagus",
  sulphur: "sulfur",
  sulphate: "sulfate",
  fiber: "fibre",
  fibers: "fibre",
  zero: "0",
  one: "1",
  two: "2",
  three: "3",
  four: "4",
  five: "5",
  six: "6",
  seven: "7",
  eight: "8",
  nine: "9",
  ten: "10",
  twenty: "20",
};
const CANONICAL = new Set(Object.values(FORMS));
const stem = (word: string): string =>
  FORMS[word] ??
  (CANONICAL.has(word) || word.length <= 3 || /\d/.test(word)
    ? word
    : word
        .replace(/ies$/, "y")
        .replace(/(sses|shes|ches|xes)$/, (m) => m.slice(0, -2))
        .replace(/(ing|ed|ly)$/, "")
        .replace(/s$/, ""));

export const tokens = (value: string): string[] =>
  value
    .normalize("NFKC")
    .toLowerCase()
    .replace(/[’]/g, "'")
    .replace(
      /\b(can't|cannot|isn't|aren't|doesn't|don't|won't|wouldn't)\b/g,
      " not ",
    )
    .replace(/[’'`]/g, "")
    .replace(/[−–—‐]/g, "-")
    .replace(/×/g, " multiply ")
    .replace(/(?<=[a-z])-(?=[a-z])/g, " ")
    .replace(/[^a-z0-9%°+\-=/().,\s]/g, " ")
    .replace(/[(),]/g, " ")
    .replace(/[.!?;:](?=\s|$)/g, " ")
    .replace(/(?<=\D)[./](?=\D)/g, " ")
    .split(/\s+/)
    .filter(Boolean)
    .map(stem);
const content = (value: string): string[] => [
  ...new Set(tokens(value).filter((t) => !STOP.has(t))),
];
const negative = (value: string): boolean =>
  /\b(no|not|never|without|cannot|can't|isn't|aren't|doesn't|don't|won't)\b/i.test(
    value.replace(/[’]/g, "'"),
  );

/**
 * Alternatives such as "detecting or measuring charge" have a shared noun:
 * detect charge OR measure charge. "Soil sampler or corer" has two complete
 * noun phrases. Slash notation is expanded only outside numbers/formulae.
 */
function printedAlternatives(value: string): string[] {
  const pieces = value
    .split(/\s+or\s+|\s*\/\s*(?!\d)/i)
    .map((s) => s.trim())
    .filter(Boolean);
  if (pieces.length === 1) return pieces;
  const last = pieces[pieces.length - 1].split(/\s+/);
  return pieces.map((piece, i) => {
    if (i === pieces.length - 1 || /\s/.test(piece) || last.length < 2)
      return piece;
    // Share the object only across parallel verbs/adjectives, not arbitrary
    // noun alternatives ("Pt / carbon" must remain an alternative).
    if (
      /ing$|^(detect|measure|clean|disinfect|high|low|red|blue|green)$/i.test(
        piece,
      )
    )
      return `${piece} ${last.slice(1).join(" ")}`;
    return piece;
  });
}

function phrases(point: MarkPoint): string[][] {
  const raw = point.accept?.length ? point.accept : [[point.verbatim]];
  return raw.flatMap((group) => {
    let variants: string[][] = [[]];
    for (const original of group) {
      const main = original
        .replace(/\([^)]*\)/g, " ")
        .replace(/\s+/g, " ")
        .trim();
      const alts = printedAlternatives(main || original);
      // Only explicitly printed alternatives in brackets are inferred. A
      // parenthetical explanation, unit or condition is not a new answer.
      for (const [, inside] of original.matchAll(/\(([^)]*)\)/g)) {
        if (
          /^(or|accept)\s+/i.test(inside) &&
          !/\b(named|described|example)\b/i.test(inside)
        )
          alts.push(
            ...printedAlternatives(inside.replace(/^(or|accept)\s+/i, "")),
          );
      }
      variants = variants.flatMap((v) => alts.map((a) => [...v, a]));
    }
    return variants;
  });
}

const clauses = (answer: string): string[] =>
  answer
    .split(/\n|;|[.!?](?:\s|$)|\bbut\b/i)
    .map((s) => s.trim())
    .filter(Boolean);

function scopedAnswer(
  answer: string,
  point: MarkPoint,
  points: MarkPoint[],
): string {
  if (!point.labels?.length) return answer;
  const labelled = points.filter((p) => p.labels?.length);
  const lines = answer.split(/\n|;|\b(?:and|but)\b/i);
  const labelledLines = lines.filter((line) =>
    labelled.some((p) =>
      p.labels!.some((label) => new RegExp(`\\b${label}\\b`, "i").test(line)),
    ),
  );
  if (!labelledLines.length) return answer;
  return labelledLines
    .filter((line) =>
      point.labels!.some((label) =>
        new RegExp(`\\b${label}\\b`, "i").test(line),
      ),
    )
    .join("; ");
}

function matchPoint(answer: string, point: MarkPoint): boolean {
  const parts = clauses(answer);
  return phrases(point).some((group) =>
    group.every((phrase) => {
      const symbol = /^[A-Z][a-z]?$/.test(phrase.trim());
      const required = symbol ? tokens(phrase) : content(phrase);
      if (!required.length) return false;
      // A one-letter symbol must actually be offered as a symbol, rather than
      // accidentally matching the article "a" or the pronoun "I" in prose.
      if (required.length === 1 && /^[a-z]$/.test(required[0])) {
        return new RegExp(
          `(?:^|[,;]|\\b(?:vitamin|symbol|element)\\s+)\\s*${required[0]}(?:\\s*[.,]|$|\\s+(?:and|or)\\s+)`,
          "i",
        ).test(answer);
      }
      const supporting = parts.filter((part) => {
        const qualified = required.some((t) =>
          [
            "same",
            "opposite",
            "high",
            "low",
            "only",
            "direct",
            "inverse",
          ].includes(t),
        );
        const statements = qualified ? part.split(/\band\b|,/i) : [part];
        return statements.some((statement) => {
          const set = new Set(symbol ? tokens(statement) : content(statement));
          return required.every((t) => set.has(t));
        });
      });
      const expectedNegative = negative(phrase);
      // Do not award a point for a negated claim or an answer that explicitly
      // states both a claim and its contradiction.
      if (supporting.some((part) => negative(part) !== expectedNegative))
        return false;
      return supporting.some((part) => negative(part) === expectedNegative);
    }),
  );
}

export const markAnswer = (answer: string, points: MarkPoint[]): MarkResult => {
  const hits = points.map((point) => ({
    id: point.id,
    marks: point.marks,
    matched:
      !!answer.trim() && matchPoint(scopedAnswer(answer, point, points), point),
  }));
  return {
    earned: hits.reduce((n, h) => n + (h.matched ? h.marks : 0), 0),
    total: points.reduce((n, p) => n + p.marks, 0),
    hits,
  };
};
export const squares = (result: MarkResult): string =>
  result.hits.map((h) => (h.matched ? "🟧" : "⬜")).join("");
