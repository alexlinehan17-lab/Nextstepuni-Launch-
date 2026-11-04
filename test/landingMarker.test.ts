import { describe, expect, it } from "vitest";
import {
  markAnswer,
  squares,
  tokens,
} from "../components/landing/marking/marker";
import { schemePoints, type CertleQuestion } from "../components/certle/data";
import pool from "../public/assets/landing/today/pool.json";
const question = (id: string) =>
  pool.entries.find((q) => q.id === id)! as CertleQuestion;
const score = (id: string, answer: string) =>
  markAnswer(answer, schemePoints(question(id)));

describe("scheme-point marking", () => {
  it("keeps formulae and light inflections", () => {
    expect(tokens("The cells were digested")).toEqual([
      "the",
      "cell",
      "were",
      "digest",
    ]);
    expect(tokens("Cx(H2O)y")).toEqual(["cx", "h2o", "y"]);
  });
  it("awards partial credit only at the scheme’s published point boundaries", () => {
    const id = "bio-2021-hl-q14-b-vii";
    const partial = score(id, "Peristalsis");
    expect(partial.earned).toBe(3);
    expect(partial.total).toBe(6);
    expect(squares(partial)).toBe("🟧⬜");
    expect(
      score(id, "Peristalsis moves food when the muscles contract.").earned,
    ).toBe(6);
  });
  it.each([
    "detect charge",
    "It detects electrical charge.",
    "measuring charge",
    "It can detect if an object is charged.",
  ])("accepts an individual printed electroscope alternative: %s", (answer) => {
    expect(score("phys-2025-ol-q14c-iii", answer).earned).toBe(6);
  });
  it("does not invent fractional credit inside a single six-mark point", () => {
    expect(score("phys-2025-ol-q14c-iii", "charge").earned).toBe(0);
  });
  it("accepts printed bracketed alternatives and explicit formula alternatives", () => {
    expect(score("bio-2021-hl-q8-b-i-2", "violet").earned).toBe(3);
    expect(score("bio-2022-hl-q15-b-i", "insulation").earned).toBe(3);
    expect(score("bio-2025-hl-q1-a", "Cn(H2O)n").earned).toBe(4);
    expect(score("bio-2025-hl-q1-a", "carbon and water").earned).toBe(0);
  });
  it("accepts spelling variants and point-local equivalent wording", () => {
    expect(
      markAnswer("esophagus", [{ id: "a", verbatim: "Oesophagus", marks: 3 }])
        .earned,
    ).toBe(3);
    expect(score("bio-2021-hl-q14-a-i", "Food is broken down.").earned).toBe(3);
    expect(
      score("phys-2025-ol-q14b-iv", "the frequency is the same").earned,
    ).toBe(3);
    expect(score("bus-2025-ol-s2-q3ci", "CPI").earned).toBe(1);
  });
  it("recognises grammatical changes without conflating different scientific terms", () => {
    expect(
      score("chem-2021-ol-q10-b-i-ii", "Oxidation loses electrons.").earned,
    ).toBe(4);
    expect(score("bio-2025-hl-q3-c", "adenosine diphosphate").earned).toBe(0);
  });
  it.each([
    "Adenosine Tri-Phosphate",
    "adenosine tri phosphate",
    "adenosine tri - phosphate",
    "Adenosine Tri‑Phosphate",
    "adenosinetriphosphate",
    "  ADENOSINE   TRIPHOSPHATE!  ",
  ])("accepts equivalent word breaks across ATP questions: %s", (answer) => {
    for (const id of ["bio-2025-hl-q3-c", "bio-2022-hl-q14-b-vi"])
      expect(score(id, answer).earned).toBe(score(id, "Adenosine triphosphate").total);
  });
  it.each([
    ["bio-2021-hl-q14-b-vii", "Peristalsi", 3],
    ["bio-2021-hl-q14-b-vii", "Peristalssis", 3],
    ["bio-2021-hl-q14-b-vii", "Peristalsis, muscular contracitons", 6],
    ["bio-2025-ol-q9-a-ii", "Temperture", 3],
    ["bio-2025-hl-q3-c", "Adenosien triphosphate", 3],
    ["bio-2022-ol-q9-a-ii", "Carbondioxide", 3],
    ["phys-2023-ol-q8-vii", "longsightedness", 5],
    ["phys-2023-ol-q8-vii", "long sightedness", 5],
  ])("allows small typing slips or joined words: %s / %s", (id, answer, marks) => {
    expect(score(id, answer).earned).toBe(marks);
  });
  it.each([
    ["Adenosine diphosphate", "Adenosine triphosphate"],
    ["adenosine mono phosphate", "Adenosine triphosphate"],
    ["chlorine", "chloride"],
    ["silver nitrite", "silver nitrate"],
    ["sulfite", "sulfate"],
    ["propene", "propane"],
    ["meiosis", "mitosis"],
    ["contact", "contract"],
    ["muscles contacting", "muscles contracting"],
    ["ADP", "ATP"],
    ["H2", "H2O"],
    ["x - y", "x + y"],
    ["24 Hz", "24 kHz"],
    ["carbon not dioxide", "carbon dioxide"],
    ["tri not phosphate", "triphosphate"],
    ["tri and phosphate", "triphosphate"],
    ["tri something phosphate", "triphosphate"],
    ["No peristalssis", "Peristalsis"],
    ["Peristalsis. Not peristalssis.", "Peristalsis"],
  ])("does not turn a different meaning into a typo: %s / %s", (answer, expected) => {
    expect(markAnswer(answer, [{ id: "meaning", verbatim: expected, marks: 3 }]).earned).toBe(0);
  });
  it("does not mark reversed oxidation/reduction definitions as correct", () => {
    expect(
      score(
        "chem-2021-ol-q10-b-i-ii",
        "Oxidation gains electrons and reduction loses electrons.",
      ).earned,
    ).toBe(0);
    expect(
      score(
        "chem-2021-ol-q10-b-i-ii",
        "Oxidation loses electrons and reduction gains electrons.",
      ).earned,
    ).toBe(7);
  });
  it("does not award positive scheme points for negated or contradictory statements", () => {
    const id = "phys-2025-ol-q14c-iii";
    expect(score(id, "It cannot detect charge.").earned).toBe(0);
    expect(
      score(id, "It detects charge. It does not detect charge.").earned,
    ).toBe(0);
    expect(
      score("phys-2022-hl-q7-i", "The extension is not proportional to force.")
        .earned,
    ).toBeLessThan(6);
  });
  it("keeps meaningful qualifiers rather than granting 60% keyword overlap", () => {
    expect(score("chem-2021-ol-q4-e", "inversely proportional").earned).toBe(0);
    expect(score("chem-2025-hl-q6-a-i", "double bonds").earned).toBe(0);
    expect(
      score("phys-2023-hl-q12a-i", "different mass and same charge").earned,
    ).toBe(0);
  });
  it("keeps numbers, signs and units distinct", () => {
    expect(
      markAnswer("0.", [{ id: "z", verbatim: "0", marks: 3, accept: [["0"]] }])
        .earned,
    ).toBe(3);
    expect(score("bio-2024-ol-q3-e", "two").earned).toBe(3);
    expect(score("bio-2024-ol-q3-e", "-2").earned).toBe(0);
    expect(score("phys-2025-ol-q14b-iv", "2.4 Hz").earned).toBe(0);
    expect(score("phys-2025-ol-q14b-iv", "2.4 kHz").earned).toBe(3);
  });
  it("does not confuse an article or pronoun with a one-letter answer", () => {
    const id = "bio-2024-hl-q1-f";
    expect(score(id, "A").earned).toBe(4);
    expect(score(id, "vitamin D").earned).toBe(4);
    expect(score(id, "a potato contains starch").earned).toBe(0);
    expect(score(id, "I think a banana").earned).toBe(0);
  });
  it("recognises negative equivalents and typographic apostrophes", () => {
    expect(
      score("phys-2025-ol-q14c-iii", "It doesn’t detect charge.").earned,
    ).toBe(0);
    expect(
      markAnswer("He", [{ id: "helium", verbatim: "He", marks: 3 }]).earned,
    ).toBe(3);
    expect(
      markAnswer("No bubbles", [
        {
          id: "gas",
          verbatim: "No more bubbles",
          marks: 3,
          accept: [["no bubbles"]],
        },
      ]).earned,
    ).toBe(3);
    expect(
      score("phys-2025-ol-q14b-iv", "Different frequency but same mass").earned,
    ).toBe(0);
  });
  it("returns no points for empty or unrelated text", () => {
    expect(score("phys-2025-ol-q14c-iii", "").earned).toBe(0);
    expect(
      score("phys-2025-ol-q14c-iii", "to measure temperature").earned,
    ).toBe(0);
  });
});
