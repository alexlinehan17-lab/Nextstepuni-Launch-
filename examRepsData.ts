/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Exam Reps — the Rep Card bank.
 *
 * Cards are AGENT-FORGED from real State Examinations Commission sources via a
 * forge → verify → repair → re-verify pipeline. Question text is reproduced
 * faithfully; the real marking scheme is rebuilt as checkable "mark ribbons"
 * whose non-gate marks sum to the tariff; every lesson is examiner-cited.
 *
 * ⚠️ HARD CONTENT RULE — cards MUST be SELF-CONTAINED: answerable from the
 * student's own knowledge, or with ALL needed data included in the stem.
 * NEVER use a question that depends on an external case study (Business ABQ),
 * a comprehension passage (English Paper 1), or an accompanying data table /
 * map / diagram that isn't reproduced here — it is meaningless out of context.
 *
 * ⚠️ Cycle-dated reference content — re-verify against current schemes yearly.
 */
import { type RepCard } from './types/examReps';

export const REP_CARDS: RepCard[] = [
  {
    "id": "maths-ol-2015-p1-q1c",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2015,
    "questionRef": "2015 Paper 1, Q1(c) (Ordinary Level)",
    "questionText": "Padraic wants to exchange some dollars for sterling. On a day when the euro to dollar exchange rate is €1 = $1·24 and the euro to sterling exchange rate is €1 = £0·83, find the dollar to sterling exchange rate. Write your answer in the form $1 = £ _ . _ _ .",
    "marks": 5,
    "minutes": 5,
    "answerKind": "steps",
    "commandWord": {
      "word": "find",
      "reminder": "\"Find\" requires the value plus the working — here you must bridge through the euro, not guess; marks are not awarded for an unsupported answer."
    },
    "ribbons": [
      {
        "label": "Low partial credit: work on the dollar-to-euro rate or the sterling-to-euro rate (i.e. link the two given rates through the euro)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "High partial credit: correct intermediate rate found (correct $→€ rate, e.g. $1 = €0·806, or correct £→€ rate)",
        "marks": 1,
        "kind": "method"
      },
      {
        "label": "Full credit: final answer correct — $1 = £0·67",
        "marks": 1,
        "kind": "other"
      }
    ],
    "lesson": {
      "text": "This is the exact part the Chief Examiner singled out: candidates handled single-rate conversions in (a) and (b) well, but 'when asked to convert using two exchange rates (Part (c)...), the majority were unable to successfully complete this conversion.' Part (c) runs on a 5-mark (0, 3, 4, 5) scale — 3 for working on the $→€ or £→€ rate, 4 for the correct intermediate rate, 5 for the final answer. The trick is to go via the euro: $1 = €(1/1·24) ≈ €0·806, then × 0·83 to get £0·67 — don't try to combine the two rates directly.",
      "source": "Chief Examiner 2015 p.26; Marking scheme 2015, Paper 1 Q1(c), Scale 5C (0, 3, 4, 5)"
    }
  },
  {
    "id": "geo-hl-2023-q6b",
    "subject": "geography",
    "subjectLabel": "Geography",
    "level": "higher",
    "year": 2023,
    "questionRef": "2023 HL · Q6B",
    "questionText": "Account for the development of secondary economic activity in a European region (not in Ireland) that you have studied, with reference to any two of the following factors:\n• Labour\n• Transport\n• Raw materials\n• Markets.",
    "marks": 30,
    "minutes": 20,
    "answerKind": "written",
    "taskType": "regional-economic-account",
    "commandWord": {
      "word": "Account for",
      "reminder": "“Account for” means EXPLAIN the causes — every point must link the factor to WHY the activity developed there, not just describe it."
    },
    "ribbons": [
      {
        "id": "region-gate",
        "label": "Named a valid European region (not in Ireland)",
        "marks": 0,
        "kind": "gate"
      },
      {
        "id": "factor1",
        "label": "Factor 1 examined — each point linked to WHY the activity developed (up to 8 points)",
        "marks": 16,
        "kind": "srp"
      },
      {
        "id": "factor2",
        "label": "Factor 2 examined — each point linked to development (up to 7 points)",
        "marks": 14,
        "kind": "srp"
      }
    ],
    "lesson": {
      "text": "You can write a flawless description of each factor and still be capped at just 4 marks per factor — the scheme rewards “merely describing the factor” at a maximum of 2 points. The marks live in the LINK: “Because [factor]…, [the activity] developed/located here…”. And name your European (non-Irish) region up front — an examination with no named or clearly-inferred region scores zero.",
      "source": "Chief Examiner 2012, p.27 · Marking scheme 2023, p.22"
    }
  },
  {
    "id": "geog-hl-2023-q3b-tectonic-cycle",
    "subject": "geography",
    "subjectLabel": "Geography",
    "level": "higher",
    "year": 2023,
    "questionRef": "2023 HL Part Two, Q3B (Section 1: Patterns and Processes in the Physical Environment)",
    "questionText": "Explain how the study of plate tectonics has helped us to understand the global distribution of any one of the following: Earthquakes / Volcanoes / Fold mountains. [30 marks]",
    "marks": 30,
    "minutes": 20,
    "answerKind": "written",
    "commandWord": {
      "word": "Explain",
      "reminder": "Give reasons / show HOW and WHY. Do not merely describe plate-tectonic theory — you must LINK it to the global distribution pattern you chose."
    },
    "ribbons": [
      {
        "label": "Named example of global distribution stated and identified (e.g. Pacific Ring of Fire / mid-Atlantic Ridge / Himalayas) — 2 + 2 marks",
        "marks": 4,
        "kind": "name"
      },
      {
        "label": "Explanation linking plate tectonics to the chosen global distribution — 13 SRPs × 2 marks. Reference to plate tectonics earns 1 SRP; a relevant LABELLED diagram earns 1 SRP and extra labelled info earns up to 2 more SRPs — all counted WITHIN these 13 SRPs, not as separate marks",
        "marks": 26,
        "kind": "explain"
      },
      {
        "label": "GATE: Max 2 SRPs total if the answer never refers to HOW plate tectonics explains the global distribution — i.e. theory described but not linked to distribution",
        "marks": 0,
        "kind": "gate"
      }
    ],
    "lesson": {
      "text": "Do not just describe plate-tectonic theory. The examiner flagged candidates who 'over emphasised the description of the theory of plate tectonics, and failed to link the theory to the distribution' — the marks are for the LINK, so every point should connect the process to the global pattern.",
      "source": "SEC Leaving Certificate Geography 2012 Chief Examiner's Report, Higher Level, p.25 (Q1C commentary)"
    }
  },
  {
    "id": "geog-hl-2023-q1b-igneous-rocks",
    "subject": "geography",
    "subjectLabel": "Geography",
    "level": "higher",
    "year": 2023,
    "questionRef": "2023 HL Part Two, Q1B (Section 1: Patterns and Processes in the Physical Environment)",
    "questionText": "Explain the formation of two igneous rocks, with reference to Irish examples. [30 marks]",
    "marks": 30,
    "minutes": 20,
    "answerKind": "written",
    "commandWord": {
      "word": "Explain",
      "reminder": "Show HOW the rock FORMS, with reasons. Naming or describing the rock is not enough — the marks are for the formation process."
    },
    "ribbons": [
      {
        "label": "Two Irish igneous rocks NAMED (e.g. granite, basalt) — 2 + 2 marks",
        "marks": 4,
        "kind": "name"
      },
      {
        "label": "Explanation of formation of rock 1 — 7 SRPs × 2 marks. Valid Irish location/example (e.g. Giant's Causeway, Wicklow granite) earns up to 2 SRPs and a relevant LABELLED diagram up to 1+ SRPs — counted WITHIN these 7 SRPs, not separately",
        "marks": 14,
        "kind": "explain"
      },
      {
        "label": "Explanation of formation of rock 2 — 6 SRPs × 2 marks. Irish example and any labelled-diagram credit are again counted WITHIN this bucket",
        "marks": 12,
        "kind": "explain"
      },
      {
        "label": "GATE: Max 2 SRPs if the answer merely DESCRIBES igneous rocks without referring to formation; Max 7 SRPs if only one rock is explained",
        "marks": 0,
        "kind": "gate"
      }
    ],
    "lesson": {
      "text": "Focus on the formation of the ROCK, not features or weathering. The examiner penalised candidates who 'described the formation of limestone features or described the process of weathering... instead of focusing on the formation of limestone rock' — the same trap applies to igneous rock: explain how the rock itself forms.",
      "source": "SEC Leaving Certificate Geography 2012 Chief Examiner's Report, Higher Level, p.25 (Q1B commentary)"
    }
  }
];
