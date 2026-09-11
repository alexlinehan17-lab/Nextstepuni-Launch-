import type { MarkPoint } from "../landing/marking/marker";

export interface CertleQuestion {
  id: string;
  subject: string;
  year: number;
  level: string;
  ref: string;
  question: string;
  points: MarkPoint[];
  attribution: string;
  figure?: { src: string; alt: string; attribution: string };
}
export interface CertlePool {
  entries: CertleQuestion[];
}
export const POOL_URL = "/assets/landing/today/pool.json";
export const MAX_ATTEMPTS = 3;
export const CERTLE_URL = "/certle";

/**
 * Point-local equivalent wording, tied to existing scheme text. These do not
 * change the scheme, tariff or card corpus. Keep each mapping narrow: a
 * global fuzzy matcher can confuse different scientific terms.
 */
const EQUIVALENTS: Record<string, string[][]> = {
  "population control": [
    ["control", "population"],
    ["regulate", "population"],
    ["keep", "population", "check"],
  ],
  "adenosine triphosphate": [["adenosine", "triphosphate"]],
  "consumer price index.": [["consumer", "price", "index"], ["cpi"]],
  "muscular contractions": [["muscle", "contract"]],
  "explain — muscular contractions": [["muscle", "contract"]],
  "name — peristalsis": [["peristalsis"]],
  "hears the same note": [
    ["same", "frequency"],
    ["same", "note"],
    ["unchanged", "frequency"],
  ],
  "mass multiplied by velocity": [
    ["mass", "multiply", "velocity"],
    ["mass", "velocity", "product"],
    ["mv"],
  ],
  "mass × velocity": [
    ["mass", "multiply", "velocity"],
    ["mass", "velocity", "product"],
    ["mv"],
  ],
  "the breakdown of food": [
    ["break", "down", "food"],
    ["breakdown", "food"],
  ],
  "growth response (of plants) to light": [
    ["growth", "light"],
    ["grow", "light"],
  ],
  "disease causing": [["cause", "disease"]],
  "no more bubbles": [
    ["no", "bubbles"],
    ["bubbling", "stop"],
  ],
  "process never stops": [
    ["never", "stop"],
    ["continuous"],
    ["without", "stopping"],
  ],
  "to absorb (or trap) light (energy)": [
    ["absorb", "light"],
    ["trap", "light"],
  ],
  "messenger rna (mrna)": [["messenger", "rna"], ["mrna"]],
  "transfer rna (trna)": [["transfer", "rna"], ["trna"]],
  "nitrogen (n)": [["nitrogen"], ["N"]],
  "twenty (20)": [["20"]],
  "cx(h2o)y": [["Cx(H2O)y"], ["Cn(H2O)n"]],
  "j.j. thomson": [["Thomson"]],
  uv: [["uv"], ["ultraviolet"]],
};

export function schemePoints(question: CertleQuestion): MarkPoint[] {
  return question.points.map((p, i) => {
    const extra = EQUIVALENTS[p.verbatim.toLowerCase()];
    const point: MarkPoint = {
      ...p,
      ...(extra
        ? {
            accept: [
              ...(p.accept ?? [[p.verbatim]]),
              ...extra.map((terms) => [terms.join(" ")]),
            ],
          }
        : {}),
    };
    if (question.id === "chem-2021-ol-q10-b-i-ii")
      point.labels = [i === 0 ? "oxidation" : "reduction"];
    if (question.id === "bus-2022-ol-s1-q2") {
      // The printed '(i) —' is a part label, not part of the category name.
      // Preserve the scheme verbatim for review and bind credit to its image.
      point.partIndex = i;
      point.accept = [[p.verbatim.replace(/^\([ivx]+\)\s*[—–-]\s*/i, "")]];
    }
    return point;
  });
}
