/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Exam Reps — the Rep Card bank.
 *
 * Cards are AGENT-FORGED from real State Examinations Commission sources via a
 * forge → verify → repair → re-verify pipeline. Question text reproduced
 * faithfully; the real marking scheme rebuilt as checkable "mark ribbons"
 * whose non-gate marks sum to the tariff; every lesson examiner-cited.
 *
 * ⚠️ HARD CONTENT RULE — cards MUST be SELF-CONTAINED: answerable from the
 * student's own knowledge, or with ALL needed data in the stem. NEVER a
 * question depending on an external case study (Business ABQ), comprehension
 * passage (English Paper 1), or accompanying data/map/diagram not reproduced
 * here. English/History essays are self-contained: the student supplies the
 * studied text / topic.
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
    "id": "business-hl-2025-s1-q5-cgt-cat",
    "subject": "business",
    "subjectLabel": "Business",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 Section 1 Q5",
    "questionText": "Distinguish between Capital Gains Tax and Capital Acquisitions Tax.",
    "marks": 10,
    "minutes": 5,
    "answerKind": "written",
    "commandWord": {
      "word": "Distinguish",
      "reminder": "State a clear point of difference for EACH term — define both and make the contrast explicit; one definition alone does not 'distinguish'."
    },
    "ribbons": [
      {
        "label": "Capital Gains Tax explained (e.g. a tax you pay on any capital gain/profit made when you dispose of an asset)",
        "marks": 3,
        "kind": "explain"
      },
      {
        "label": "CGT point developed/distinguished (e.g. charged on disposal of an asset, not on receipt of a gift)",
        "marks": 2,
        "kind": "explain"
      },
      {
        "label": "Capital Acquisitions Tax explained (e.g. a tax on gifts and inheritances)",
        "marks": 3,
        "kind": "explain"
      },
      {
        "label": "CAT point developed/distinguished (e.g. amount you can receive tax-free depends on your relationship to the person you get them from)",
        "marks": 2,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "'Distinguish' questions reward a clear contrast, not two parallel definitions. The 2015 Chief Examiner repeatedly flagged that 'recall of definitions has merit... however the requirement to build on the definitions to answer the actual questions set at the Higher level was not always evident' — define both taxes, then make the difference between them explicit.",
      "source": "Chief Examiner 2015, p.16-17; Marking scheme 2025 Section 1 Q5 (3+2)(3+2)"
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
    "id": "business-hl-2025-s1-q6-ethical-practice",
    "subject": "business",
    "subjectLabel": "Business",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 Section 1 Q6",
    "questionText": "Outline two methods a business may use to encourage ethical business practice.",
    "marks": 10,
    "minutes": 5,
    "answerKind": "written",
    "commandWord": {
      "word": "Outline",
      "reminder": "'Outline' needs a developed point, not a one-word answer — name each method (3) AND explain how it encourages ethical practice (2). Two distinct methods are required; a second variation of the same point earns nothing extra."
    },
    "ribbons": [
      {
        "label": "First method named (e.g. develop a code of ethics / training / rewards / senior managers lead by example / clear disciplinary procedures)",
        "marks": 3,
        "kind": "name"
      },
      {
        "label": "First method explained (how it encourages ethical behaviour, e.g. a code in the employment contract discourages unethical conduct)",
        "marks": 2,
        "kind": "explain"
      },
      {
        "label": "Second, distinct method named",
        "marks": 3,
        "kind": "name"
      },
      {
        "label": "Second method explained",
        "marks": 2,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "The cue 'Outline' expects two developed points, each scored Name (3) + Explain (2). Reviewing the 2015 paper, the Chief Examiner warned that 'only one valid point is often given when two or three points are required' and that cues such as 'outline' and 'explain' 'are often not addressed adequately' — pick two genuinely different methods and develop each rather than repeating one.",
      "source": "Chief Examiner 2015, p.20; Marking scheme 2025 Section 1 Q6 2@(3+2)"
    }
  },
  {
    "id": "lc-maths-ol-2019-p1-q1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2019,
    "questionRef": "2019 Leaving Certificate, Mathematics, Paper 1, Ordinary Level, Section A, Question 1 (25 marks)",
    "questionText": "Eimear earns a gross wage of €40 000 per annum with Company A.\n(a) Eimear pays income tax at a rate of 20% on income up to the standard rate cut-off point of €35 300. She pays tax at a rate of 40% on the remainder. She has annual tax credits of €1650. Find how much income tax she pays per annum.\n(b) Eimear pays her health insurance which costs her €1500 net. Find her annual income after paying income tax and health insurance (i.e. her net annual income).\n(c) Eimear is planning to change jobs. She is offered a job by Company B with a gross wage of €38 000 and a bonus of €1500 (tax free to Eimear) to be paid by the company, which she would use to pay her health insurance. Her tax rates and credits would remain the same. Find by how much Eimear’s net annual income (after paying income tax and health insurance) will increase if she accepts the job with Company B.",
    "marks": 25,
    "minutes": 13,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "'Find' here means work through the income-tax steps and show them. Lay out: gross tax at 20% on the cut-off + 40% on the remainder, then subtract tax credits to get the tax due. Method marks are given for each correct step (standard-rate tax, higher-rate tax, subtracting credits), so never just write a final figure."
    },
    "ribbons": [
      {
        "label": "(a) Tax: 35 300 × 0·2 = €7060 and 4700 × 0·4 = €1880; 7060 + 1880 = €8940; 8940 − 1650 = €7290 net tax (Scale 10D)",
        "marks": 10,
        "kind": "method"
      },
      {
        "label": "(b) Net income: 40 000 − (7290 + 1500) = €31 210 (Scale 5C)",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(c) Company B: 35 300 × 0·2 + 2700 × 0·4 = 8140; 8140 − 1650 = 6490; 38 000 − 6490 = 31 510; 31 510 − 31 210 = €300 increase (Scale 10D)",
        "marks": 10,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "Income tax is a three-step routine: (1) gross tax = 20% of the cut-off + 40% of whatever is above it, (2) tax payable = gross tax − tax credits, (3) net income = gross wage − tax payable. The marking scheme gives 'Low Partial Credit' just for 'use of 20%, 40% or similar', so always start the layout even if unsure – each correct step earns marks. The standard-rate tax is on €35 300, the 40% rate only on the €4700 remainder.",
      "source": "SEC Leaving Certificate 2019 Mathematics Ordinary Level Marking Scheme, Paper 1, Q1 model solution (examinations.ie; copy hosted at educateplus.ie)"
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
    "id": "eng-hl-p2-singletext-hamlet-2012",
    "subject": "english",
    "subjectLabel": "English",
    "level": "higher",
    "year": 2012,
    "questionRef": "LC English HL 2012, Paper 2, Section I (The Single Text), Hamlet, Q1",
    "questionText": "\"Hamlet's madness, whether genuine or not, adds to the fascination of his character for the audience.\" Discuss this statement, supporting your answer with suitable reference to the play, Hamlet. (60 marks)",
    "marks": 60,
    "minutes": 50,
    "answerKind": "paper",
    "commandWord": {
      "word": "Discuss",
      "reminder": "Take a clear, sustained position on the precise terms of the statement (here: that Hamlet's madness 'adds to the fascination of his character for the audience'). Weigh the 'whether genuine or not' tension, develop an argument across the whole play, and anchor every point in apt, judicious quotation. This is a discursive literary essay, not a plot retelling or a general character sketch."
    },
    "ribbons": [
      {
        "label": "P - Clarity of Purpose: engages directly with the precise statement (madness as a source of 'fascination' for the audience; the genuine/feigned question) and sustains a focused, on-task argument throughout, avoiding unfocused narrative",
        "marks": 18,
        "kind": "explain"
      },
      {
        "label": "C - Coherence of Delivery: a structured, logically developed response (clear line of argument, ordered paragraphs, effective linkage) that stays on the question rather than drifting into general plot summary",
        "marks": 18,
        "kind": "link"
      },
      {
        "label": "L - Efficiency of Language Use: controlled, fluent critical register appropriate to a literary essay, with apt and judicious quotation/reference from Hamlet used to illustrate points",
        "marks": 18,
        "kind": "quote"
      },
      {
        "label": "M - Accuracy of Mechanics: accurate spelling, grammar and syntax (the 'nuts and bolts' of the writing)",
        "marks": 6,
        "kind": "other"
      }
    ],
    "lesson": {
      "text": "A recurring warning across SEC English reports is that, in the Single Text section, 'unfocused narrative remained a feature of the less successful attempts.' Whatever the prescribed play, the strongest answers avoid simple character sketches and plot retelling and instead build a focused discussion that engages clearly with the exact terms of the question, using apt quotation to drive an argument.",
      "source": "SEC Chief Examiner's Report, Leaving Certificate English, Higher Level, Section 3.3 (The Single Text) — general Single Text technique; the quoted line on 'unfocused narrative' is verbatim from the 2008 report, examinations.ie"
    }
  },
  {
    "id": "lc-maths-ol-2024-p1-q1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2024,
    "questionRef": "2024 Leaving Certificate, Mathematics, Paper 1, Ordinary Level, Section A, Question 1 (30 marks)",
    "questionText": "(a) A farmer buys a new machine for €30 000. It depreciates (decreases in value) by 20% each year.\n  (i) Find the value of the machine after 1 year.\n  (ii) Hence, or otherwise, find the value of the machine after 2 years.\n(b) A farmer bought some livestock for €4716, including VAT. The cost of the livestock was €4500, excluding VAT. Calculate the percentage VAT rate used.\n(c) The farmer also bought land. One year later its value had increased by 12·5% and was now €52 875. Find the value of the land when the farmer bought it.",
    "marks": 30,
    "minutes": 12,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "'Find' (and 'Calculate') means show the steps that produce the value, not just write the answer. The SEC awards method marks for relevant working even when the final number is wrong, so set out each step (the depreciation multiplier, the VAT subtraction/fraction, the reverse-percentage division)."
    },
    "ribbons": [
      {
        "label": "(a) Depreciation: €30 000 × 0·8 = €24 000 after 1 year, then €24 000 × 0·8 = €19 200 after 2 years (Scale 10D)",
        "marks": 10,
        "kind": "method"
      },
      {
        "label": "(b) VAT rate: 4716 − 4500 = 216, then (216 ÷ 4500) × 100 = 4·8% (Scale 10C)",
        "marks": 10,
        "kind": "method"
      },
      {
        "label": "(c) Reverse percentage: 52 875 ÷ 112·5 × 100 = €47 000 (Scale 10C)",
        "marks": 10,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "Always show supporting work. The marking scheme states that 'an answer without sufficient supporting work is generally awarded the lowest non-zero level of credit', so a bare correct figure can lose most of the marks. For part (c), the safe method is reverse-percentage: divide by 112·5 and multiply by 100 (€47 000) – do NOT just take 12·5% of €52 875, which is the most common error.",
      "source": "SEC Leaving Certificate 2024 Mathematics Ordinary Level Marking Scheme, Paper 1, Q1 model solution and marking-scheme structure note (examinations.ie; copy hosted at educateplus.ie)"
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
    "id": "hist-hl-2019-s3t4-q1",
    "subject": "history",
    "subjectLabel": "History",
    "level": "higher",
    "year": 2019,
    "questionRef": "2019 LC History HL, Section 3, Europe and the wider world: Topic 4 (Division and realignment in Europe, 1945-1992), Q1",
    "questionText": "How did the Cold War develop in Europe and how did it end? (100)",
    "marks": 100,
    "minutes": 40,
    "answerKind": "paper",
    "commandWord": {
      "word": "How",
      "reminder": "\"How... and how...\" signals TWO linked tasks: trace how the Cold War DEVELOPED in Europe AND how it ENDED. You must build a cumulative case (paragraph by paragraph) that does both — pure narrative storytelling caps your Overall Evaluation."
    },
    "ribbons": [
      {
        "label": "Cumulative Mark (CM): accurate, relevant historical content marked paragraph-by-paragraph (max 12 per paragraph: Excellent 11-12, Very good 8-10, Good 6-7, Fair 3-5, Poor 0-2). Sustain roughly 5+ strong paragraphs.",
        "marks": 60,
        "kind": "method"
      },
      {
        "label": "Overall Evaluation (OE): quality of the whole answer in context of the set question — does it analyse (more than narrative), marshal relevant evidence, and argue a case reaching a conclusion?",
        "marks": 40,
        "kind": "evaluation"
      },
      {
        "label": "GATE: BOTH elements present (how it DEVELOPED + how it ENDED). If only ONE element is addressed, maximum CM is capped at 50 (not 60).",
        "marks": 0,
        "kind": "gate"
      }
    ],
    "lesson": {
      "text": "Examiners recommend that \"Candidates should learn to be aware from what perspective(s) a question is asked and what narrative and/or analytical demands the question is making\" and \"should be prepared to engage in historical argument.\" A two-part \"how... and how...\" question makes BOTH a narrative demand (developments) and an analytical one — cover both elements or CM is capped, and argue rather than merely retell to score the Overall Evaluation.",
      "source": "SEC Leaving Certificate 2006 History Chief Examiner's Report, Higher Level, Recommendations to Teachers and Candidates (p.31); 2019 HL Marking Scheme, Section 3 Topic 4 Q1 (TWO elements develop+end; if only ONE, Max CM=50)."
    }
  },
  {
    "id": "eng-hl-p2-comparative-themeissue-keymoments-2008",
    "subject": "english",
    "subjectLabel": "English",
    "level": "higher",
    "year": 2008,
    "questionRef": "LC English HL 2008, Paper 2, Section II (The Comparative Study), Mode A: Theme or Issue, Q2",
    "questionText": "Compare how key moments brought a theme or issue into sharp focus in the texts you have studied as part of your comparative course. (70 marks)",
    "marks": 70,
    "minutes": 55,
    "answerKind": "paper",
    "commandWord": {
      "word": "Compare",
      "reminder": "This demands genuine comparison, not separate text summaries. Choose key moments from each of your comparative texts and show how each brings the same theme or issue into 'sharp focus'. Link the texts continuously (similarities and differences), keep the 'sharp focus' element central, and support with reference to the texts. A general overview of the theme without the comparative key-moments lens will not score."
    },
    "ribbons": [
      {
        "label": "P - Clarity of Purpose: keeps the 'sharp focus' / key-moments element central and engages directly with the chosen theme or issue, rather than taking a general approach to the texts",
        "marks": 21,
        "kind": "explain"
      },
      {
        "label": "C - Coherence of Delivery: sustains genuine comparison across the comparative texts (continuous linking of similarities/differences) with a clear, well-organised structure built around selected key moments",
        "marks": 21,
        "kind": "link"
      },
      {
        "label": "L - Efficiency of Language Use: fluent, analytical critical language appropriate to the comparative mode, with apt reference to the key moments in each text",
        "marks": 21,
        "kind": "quote"
      },
      {
        "label": "M - Accuracy of Mechanics: accurate spelling, grammar and syntax",
        "marks": 7,
        "kind": "other"
      }
    ],
    "lesson": {
      "text": "On this exact question examiners noted many worthwhile answers offered 'a focused analysis of texts in the light of the wording of the question. However, some candidates lost sight of the \"sharp focus\" element and took a very general approach.' The best comparative answers address the nuances within the wording and make insightful, continuous comparisons rather than outlining broad similarities and differences.",
      "source": "SEC Chief Examiner's Report 2008, Leaving Certificate English, Higher Level, Section 3.3 (Section II, The Comparative Study, Theme or Issue, Q2), examinations.ie"
    }
  },
  {
    "id": "hist-hl-2019-s3t3-q1",
    "subject": "history",
    "subjectLabel": "History",
    "level": "higher",
    "year": 2019,
    "questionRef": "2019 LC History HL, Section 3, Europe and the wider world: Topic 3 (Dictatorship and democracy in Europe, 1920-1945), Q1",
    "questionText": "During the inter-war years, what were the characteristics of fascist regimes in Europe? (100)",
    "marks": 100,
    "minutes": 40,
    "answerKind": "paper",
    "commandWord": {
      "word": "characteristics",
      "reminder": "\"characteristics of fascist regimes\" is plural — you must discuss MORE THAN ONE regime (e.g. Mussolini's Italy AND Hitler's Germany). Identify shared features (one-party state, leader cult, propaganda, terror, nationalism, anti-communism) and support each with specific factual detail; do not just narrate one country's story."
    },
    "ribbons": [
      {
        "label": "Cumulative Mark (CM): accurate, relevant historical content marked paragraph-by-paragraph (max 12 per paragraph: Excellent 11-12, Very good 8-10, Good 6-7, Fair 3-5, Poor 0-2) — each characteristic backed by factual references.",
        "marks": 60,
        "kind": "method"
      },
      {
        "label": "Overall Evaluation (OE): quality of the whole answer in context of the set question — analysis of what defines fascism (more than narrative), relevant evidence marshalled, and a case argued to a conclusion.",
        "marks": 40,
        "kind": "evaluation"
      },
      {
        "label": "GATE: regimes (PLURAL) treated — more than one fascist regime discussed. If only ONE regime is covered, maximum CM is capped at 50 (not 60).",
        "marks": 0,
        "kind": "gate"
      }
    ],
    "lesson": {
      "text": "Examiners warn that some candidates \"offered historical content which was irrelevant to the set question\" and \"ignored the date parameters of the question,\" advising that \"Candidates should read each question carefully and answer it as it is set.\" Here that means staying inside the inter-war frame, covering the PLURAL \"regimes\" (so CM is not capped at 50), and answering the analytical word \"characteristics\" rather than narrating one dictator's rise to power.",
      "source": "SEC Leaving Certificate 2006 History Chief Examiner's Report, Higher Level, Conclusions (p.30) and Recommendations to Teachers and Candidates (p.31); 2019 HL Marking Scheme, Section 3 Topic 3 Q1 (Regimes plural; if only ONE regime, Max CM=50)."
    }
  }
];
