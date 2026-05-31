/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Exam Reps — the Rep Card bank.
 *
 * Cards are AGENT-FORGED from real State Examinations Commission sources
 * (examiner-reports/ + examinations.ie) through a forge → verify → repair →
 * re-verify pipeline: question text reproduced faithfully, the real marking
 * scheme rebuilt as checkable "mark ribbons" whose non-gate marks sum to the
 * tariff, and every lesson carries a citation. Only re-verified-clean cards
 * are committed here.
 *
 * ⚠️ Cycle-dated reference content — re-verify against current marking
 * schemes/reports each year. Chief Examiner report recency varies by subject;
 * lessons cite the year so the vintage is honest.
 */
import { type RepCard } from './types/examReps';

export const REP_CARDS: RepCard[] = [
  {
    "id": "eng-hl-2019-p1-text2-qa-i",
    "subject": "english",
    "subjectLabel": "English (Higher Level)",
    "level": "higher",
    "year": 2019,
    "questionRef": "2019 LC English HL — Paper 1, Section I Comprehending, Text 2 'A Photographer's Perspective', Question A (i)",
    "questionText": "Based on your reading of page 4 of TEXT 2, explain three points the character, Tom, makes about the value and power of \"proper\" photographs. Support your response with reference to the text. (15)",
    "marks": 15,
    "minutes": 12,
    "answerKind": "written",
    "commandWord": {
      "word": "explain",
      "reminder": "Don't just name the point — make Tom's meaning clear and back it with a reference/quotation from the text. The scheme says 'Pay particular attention to the quality of the explanation' — examiners reward the explanation, not the spotting."
    },
    "ribbons": [
      {
        "label": "GATE: Three DISTINCT points identified about the value/power of \"proper\" photographs (the scheme requires candidates to 'identify and explain three distinct points'; a repeated point counts once)",
        "marks": 0,
        "kind": "gate"
      },
      {
        "label": "Three distinct points each EXPLAINED — Tom's meaning made clear, not merely listed (scheme: 'Pay particular attention to the quality of the explanation'). Indicative material: 'proper' photographs spring 'from thoughtful creative decisions and a particular way of seeing'; the right image can achieve iconic status / 'impact on our consciousness' / effect change; they encapsulate a life/history/experiences; a 'proper' photograph 'steps forward' / 'will always exist'",
        "marks": 8,
        "kind": "explain"
      },
      {
        "label": "Each point SUPPORTED with reference/quotation to page 4 of the text (scheme: 'Responses should be supported by reference to the text')",
        "marks": 4,
        "kind": "quote"
      },
      {
        "label": "Holistic quality of expression — focus, coherence and language controlled to the analytical register of comprehension. NOTE: this 15-mark answer is graded HOLISTICALLY, 'ex 15 by reference to the criteria for assessment' on the H1–H8 grid (15-14 / 12 / 11 / 9 / 8 / 6 / 5 / 4-0), NOT split into discrete P/C/L/M sub-marks — discrete P/C/L/M awarding applies only to the 50-mark Question B (P15/C15/L15/M5) and the 100-mark compositions (P30/C30/L30/M10)",
        "marks": 3,
        "kind": "srp"
      }
    ],
    "lesson": {
      "text": "In comprehension Question A, identifying the point is not enough — the quality of your EXPLANATION is what scores, and the answer is judged as a single holistic grade against the four assessment criteria, not as separate P/C/L/M sub-marks. The Chief Examiner stresses that candidates must \"carefully read and correctly comprehend every question\" and that the highest-scoring candidates were those \"able to analyse and evaluate the language and concepts they encountered in texts\" rather than answer at a surface level. Guard against an \"overly literal\" reading: explain what Tom MEANS by the value and power, then tie it to the text.",
      "source": "SEC Chief Examiner's Report, Leaving Certificate English 2013, p.14 (Comprehension skills section)"
    }
  },
  {
    "id": "business-hl-2025-abq-a-entrepreneurial-skills",
    "subject": "business",
    "subjectLabel": "Business",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 Section 2 (ABQ Inis Bia) Part (A)",
    "questionText": "Outline the entrepreneurial skills/characteristics displayed by Trisha. Refer to the text in your answer.",
    "marks": 20,
    "minutes": 9,
    "answerKind": "written",
    "commandWord": {
      "word": "Outline",
      "reminder": "Develop each point — name it, explain the theory, and anchor it with a direct quote from the ABQ. 'Outline' wants developed points, not a bare list."
    },
    "ribbons": [
      {
        "label": "Name a valid entrepreneurial skill/characteristic (e.g. Risk taker, Innovative, Decision making) — 2m each x 4",
        "marks": 8,
        "kind": "name"
      },
      {
        "label": "Explain the theory of each named skill correctly (2m each x 4)",
        "marks": 8,
        "kind": "explain"
      },
      {
        "label": "Link each skill with a SEPARATE direct quote/phrase from the Inis Bia text, e.g. 'She opted to convert her shed into a mini factory...' (1m each x 4)",
        "marks": 4,
        "kind": "link"
      }
    ],
    "lesson": {
      "text": "The marking scheme requires separate links in each section and awards no link mark without relevant theory. The 2025 insights extend this: a single quote can't be reused across multiple ABQ skill answers — each named skill needs its own quote. The scheme also warns: candidates who rewrite chunks of the case with no theory, OR write pure theory with no case reference, score nothing.",
      "source": "Marking scheme 2025, p.6 ('Separate links are required in each section. No link awarded without relevant theory.'); 2025-insights.md p.6 note (a single quote can't be reused across multiple ABQ skill answers); Chief Examiner 2015, p.15"
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
    "id": "business-hl-2025-q8c-breakeven-chart",
    "subject": "business",
    "subjectLabel": "Business",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 Section 3 Q8(C) Business in Action",
    "questionText": "Illustrate the following by means of a breakeven chart: (i) Breakeven point (ii) Margin of safety at the forecast output (iii) Profit at forecast output.",
    "marks": 25,
    "minutes": 11,
    "answerKind": "paper",
    "commandWord": {
      "word": "Illustrate",
      "reminder": "'Illustrate ... by means of a breakeven chart' requires the chart drawn. Calculations alone cap you at 12/25 — the chart is the majority of the marks."
    },
    "ribbons": [
      {
        "label": "Title the chart (2m) + label both axes (1m per axis = 2m)",
        "marks": 4,
        "kind": "name"
      },
      {
        "label": "Draw Fixed Costs line (3m) + Total Costs line (3m) + Total Revenue line (3m)",
        "marks": 9,
        "kind": "method"
      },
      {
        "label": "Mark Breakeven Point on the chart (4m)",
        "marks": 4,
        "kind": "application"
      },
      {
        "label": "Mark Profit at forecast output on the chart (4m)",
        "marks": 4,
        "kind": "application"
      },
      {
        "label": "Mark Margin of Safety at forecast output on the chart (4m)",
        "marks": 4,
        "kind": "application"
      }
    ],
    "lesson": {
      "text": "If you do calculations only and skip the chart, the scheme caps you at BEP 4m + Profit 4m + MoS 4m = 12 of 25 marks — under half. The chart carries 13 of the 25 marks, and missing the title alone costs 2m, missing an axis label costs 1m each. Use graph paper.",
      "source": "Marking scheme 2025, Q8(C) grid p.11/51 ('OR Calculations only: BEP 4m / Profit at FO 4m / MoS 4m'); Chief Examiner 2015, p.18 (charts lose marks for missing title/labels)"
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
    "id": "eng-hl-2019-p1-composing-1-descriptive",
    "subject": "english",
    "subjectLabel": "English (Higher Level)",
    "level": "higher",
    "year": 2019,
    "questionRef": "2019 LC English HL — Paper 1, Section II Composing, Composition 1 (Descriptive essay)",
    "questionText": "In TEXT 2, Tom expresses the view that people favour photographs that feature sunsets. Write a descriptive essay which captures a sense of the difference between dawn and dusk and celebrates both the beginning and the end of the day. (100)",
    "marks": 100,
    "minutes": 80,
    "answerKind": "written",
    "commandWord": {
      "word": "Write a descriptive essay",
      "reminder": "Genre is graded under P. A descriptive essay may contain other elements (e.g. narrative) but the FOCUS must stay on descriptive writing — imagery, atmosphere, detail. Both tasks must be met: capture the difference AND celebrate beginning and end of day."
    },
    "ribbons": [
      {
        "label": "P — Clarity of Purpose (30): clear focus on a descriptive essay that captures the difference between dawn and dusk AND celebrates both beginning and end of day; understanding of genre (figurative language, imagery, setting, mood, quality of observation); relevance, originality and freshness",
        "marks": 30,
        "kind": "method"
      },
      {
        "label": "C — Coherence of Delivery (30): the descriptive writing is successfully shaped, developed and sustained across the whole essay; sequencing and management of ideas; the response holds together start to finish (C cannot exceed P)",
        "marks": 30,
        "kind": "explain"
      },
      {
        "label": "L — Efficiency of Language Use (30): quality and control of language — style, vocabulary, syntax, punctuation; lively, energetic, interesting phrasing appropriate to descriptive register (L cannot exceed P)",
        "marks": 30,
        "kind": "srp"
      },
      {
        "label": "M — Accuracy of Mechanics (10): accuracy in spelling and grammatical patterns appropriate to the register",
        "marks": 10,
        "kind": "other"
      }
    ],
    "lesson": {
      "text": "Marks for Coherence (C) or Language (L) CANNOT exceed the marks awarded for Clarity of Purpose (P) — P has primacy. So a beautifully written essay that drifts off-task (e.g. tells a story instead of describing, or describes only dawn) is self-capped. The Chief Examiner adds that creative, thoughtful users of language \"were rewarded\" and that high-scoring candidates \"were skilled in shaping their own writing... in the appropriate register and genre\" — lock onto the descriptive genre and the twin task before chasing fine phrasing.",
      "source": "SEC 2019 LC English HL Marking Scheme, p.3 (primacy of Clarity of Purpose); SEC Chief Examiner's Report, LC English 2013, p.14 (reward for genre/register control)"
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
  },
  {
    "id": "business-hl-2025-abq-b-i-eval-control",
    "subject": "business",
    "subjectLabel": "Business",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 HL · ABQ (B)(i)",
    "questionText": "Evaluate the effectiveness of the types of management control in place at Inis Bia. Refer to the text in your answer.",
    "marks": 28,
    "minutes": 13,
    "answerKind": "written",
    "taskType": "abq-evaluate",
    "commandWord": {
      "word": "Evaluate",
      "reminder": "“Evaluate” means for each control you must JUDGE whether it was effective or not and justify it. Naming + explaining + a case quote earns only 4 of the 7 marks per point; the 3-mark judgement is the heaviest part and where most stop short."
    },
    "ribbons": [
      {
        "id": "name",
        "label": "Name a valid type of management control (Quality / Stock / Financial / Credit) — 1m × 4 points",
        "marks": 4,
        "kind": "name"
      },
      {
        "id": "explain",
        "label": "Explain the theory of that control — 2m × 4 points",
        "marks": 8,
        "kind": "explain"
      },
      {
        "id": "link",
        "label": "Link a relevant quote from the Inis Bia text for each — 1m × 4 points",
        "marks": 4,
        "kind": "link"
      },
      {
        "id": "evaluation",
        "label": "Evaluate the effectiveness of each (judgement + justification) — 3m × 4 points",
        "marks": 12,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "Evaluation is the single most heavily-weighted component here (3 of 7 marks per point) yet the Chief Examiner calls it the weakest: “Some evaluations continue to be very superficial and some candidates do not evaluate at all.” Naming, explaining and quoting earns only 4 of 7 per point — you forfeit 12 of the 28 marks unless you finish each point with an effectiveness judgement.",
      "source": "Chief Examiner 2015, p.16 · Marking scheme 2025, p.6 & p.20"
    }
  }
];
