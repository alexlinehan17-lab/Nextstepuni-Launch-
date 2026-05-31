/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Exam Reps — the Rep Card bank. AGENT-FORGED from real SEC sources via a
 * forge → verify → repair → re-verify pipeline. Each card is tagged
 * subjectId · level · topicId against curriculum.ts.
 *
 * ⚠️ HARD RULES: SELF-CONTAINED (no external case/passage/data); every card
 * carries a valid curriculum topicId. Re-verify yearly.
 */
import { type RepCard } from './types/examReps';

export const REP_CARDS: RepCard[] = [
  {
    "id": "maths-ol-2015-p1-q1c",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2015,
    "questionRef": "2015 OL · P1 Q1(c)",
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
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-2"
  },
  {
    "id": "business-hl-2025-s1-q5-cgt-cat",
    "subject": "business",
    "subjectLabel": "Business",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 HL · Q5",
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
    },
    "subjectId": "business",
    "topicId": "business-3-3"
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
    },
    "subjectId": "geography",
    "topicId": "geography-1-1"
  },
  {
    "id": "business-hl-2025-s1-q6-ethical-practice",
    "subject": "business",
    "subjectLabel": "Business",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 HL · Q6",
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
    },
    "subjectId": "business",
    "topicId": "business-5-11"
  },
  {
    "id": "lc-maths-ol-2019-p1-q1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2019,
    "questionRef": "2019 OL · P1 Q1",
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
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-2"
  },
  {
    "id": "geog-hl-2023-q3b-tectonic-cycle",
    "subject": "geography",
    "subjectLabel": "Geography",
    "level": "higher",
    "year": 2023,
    "questionRef": "2023 HL · Q3B",
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
    },
    "subjectId": "geography",
    "topicId": "geography-0-0"
  },
  {
    "id": "eng-hl-p2-singletext-hamlet-2012",
    "subject": "english",
    "subjectLabel": "English",
    "level": "higher",
    "year": 2012,
    "questionRef": "2012 HL · Hamlet",
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
    },
    "subjectId": "english",
    "topicId": "english-6-1"
  },
  {
    "id": "lc-maths-ol-2024-p1-q1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2024,
    "questionRef": "2024 OL · P1 Q1",
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
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-2"
  },
  {
    "id": "geog-hl-2023-q1b-igneous-rocks",
    "subject": "geography",
    "subjectLabel": "Geography",
    "level": "higher",
    "year": 2023,
    "questionRef": "2023 HL · Q1B",
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
    },
    "subjectId": "geography",
    "topicId": "geography-0-1"
  },
  {
    "id": "hist-hl-2019-s3t4-q1",
    "subject": "history",
    "subjectLabel": "History",
    "level": "higher",
    "year": 2019,
    "questionRef": "2019 HL · Q1",
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
    },
    "subjectId": "history",
    "topicId": "history-3-12"
  },
  {
    "id": "eng-hl-p2-comparative-themeissue-keymoments-2008",
    "subject": "english",
    "subjectLabel": "English",
    "level": "higher",
    "year": 2008,
    "questionRef": "2008 HL · Comparative",
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
    },
    "subjectId": "english",
    "topicId": "english-7-0"
  },
  {
    "id": "hist-hl-2019-s3t3-q1",
    "subject": "history",
    "subjectLabel": "History",
    "level": "higher",
    "year": 2019,
    "questionRef": "2019 HL · Q1",
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
    },
    "subjectId": "history",
    "topicId": "history-3-8"
  },
  {
    "id": "maths-hl-2-0-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2017,
    "questionRef": "2017 HL P1 Q1",
    "questionText": "(a) Write each of the following numbers in the form a + b, where a is an integer and b is an irrational number written in the form k√3 (k a rational number), and hence show that the sum is irrational:\n   (2 + √27) + (5 − √12).\n(b) Prove, by contradiction, that √3 is irrational. In your proof, you may assume that if 3 divides p², then 3 divides p, where p is a natural number.",
    "marks": 25,
    "minutes": 25,
    "answerKind": "steps",
    "commandWord": {
      "word": "Prove",
      "reminder": "Give rigorous logical argument; justify every step"
    },
    "ribbons": [
      {
        "label": "Some correct simplification of at least one surd (√27 = 3√3 or √12 = 2√3) OR a correct opening statement of the contradiction in (b)",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(a) Low partial: both surds correctly simplified to 3√3 and 2√3, not yet combined",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(a) High partial: correct sum 7 + √3 obtained AND a valid reason it is irrational",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Setup: assumes √3 = p/q rational in lowest terms and squares to reach p² = 3q²",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(b) Mid credit: deduces 3 | p, substitutes p = 3m, and reaches 3m² = q²",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(b) Completion: deduces 3 | q, identifies common-factor contradiction, concludes √3 is irrational",
        "marks": 6,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The most common error in part (b) is forgetting to state at the outset that p/q is in its lowest terms (or that p, q share no common factor). Without that assumption there is no contradiction to reach at the end — the whole proof collapses because finding \"3 divides both p and q\" is only contradictory if you began by ruling out common factors. Examiners withhold the high partial credit when this lowest-terms condition is missing or only implied.",
      "source": "SEC Chief Examiner's Report"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-0"
  },
  {
    "id": "maths-ol-2-0-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2018,
    "questionRef": "2018 OL P1 Q1",
    "questionText": "(a) The number 360 can be written as a product of its prime factors in the form 2^a x 3^b x 5^c. Find the value of a, the value of b and the value of c.\n\n(b)(i) Write the number 0.000 47 in the form a x 10^n, where 1 ≤ a < 10 and n is an integer.\n(ii) Write the number 3.6 x 10^5 as a natural number (i.e. without using powers of 10).\n\n(c) Two whole numbers are written as products of their prime factors:\n   P = 2^3 x 3^2 x 5\n   Q = 2^2 x 3 x 5^2\nUse these prime factorisations to find the Highest Common Factor (HCF) of P and Q.",
    "marks": 25,
    "minutes": 25,
    "answerKind": "steps",
    "commandWord": {
      "word": "Express / Write",
      "reminder": "Rewrite the number in required form"
    },
    "ribbons": [
      {
        "label": "(a) Attempt: any correct division by a prime, or factor tree begun",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(a) Full: a = 3, b = 2, c = 1 all correct",
        "marks": 7,
        "kind": "method"
      },
      {
        "label": "(b)(i) 4.7 x 10^(-4) fully correct (3 for correct digits, wrong index)",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(b)(ii) 360 000 fully correct (3 for method with one place-value slip)",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(c) HCF = 60 correct (2 for identifying common primes)",
        "marks": 5,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The single most common error is confusing HCF with LCM. For HCF you take the LOWEST power of each shared prime (giving 60 here); for LCM you take the HIGHEST power of every prime that appears in either number (which would give 2^3 x 3^2 x 5^2 = 1800). Students who \"multiply everything\" get 1800 and lose the marks. Underline whether the question asks for Highest Common Factor or Lowest Common Multiple before answering.",
      "source": "SEC Chief Examiner's Report"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-0"
  },
  {
    "id": "maths-ol-2-0-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2017,
    "questionRef": "2017 OL P1 Q2",
    "questionText": "The natural numbers (N), integers (Z), rational numbers (Q) and real numbers (R) are different number sets.\n\n(a) State which of the following numbers are rational and which are irrational. Give a reason in each case.\n   (i) 0.75   (ii) √16   (iii) √7   (iv) π\n\n(b) A rational number is any number that can be written in the form p/q, where p and q are integers and q ≠ 0.\n   (i) Write the recurring decimal 0.4444... (0.4 recurring) as a fraction in the form p/q in its simplest form.\n   (ii) Hence, or otherwise, state whether 0.4444... is rational or irrational.\n\n(c) Two students are discussing the number √7. Aoife says: \"√7 lies between 2 and 3.\" Brian says: \"√7 lies between 2.6 and 2.7.\" By squaring, investigate whether each statement is true. State clearly who, if anyone, is correct.",
    "marks": 25,
    "minutes": 25,
    "answerKind": "steps",
    "commandWord": {
      "word": "Investigate / Show / Write",
      "reminder": "Test the claims and state outcome"
    },
    "ribbons": [
      {
        "label": "(a) 2.5 per part: correct classification with valid reason (×4)",
        "marks": 10,
        "kind": "explain"
      },
      {
        "label": "(b)(i) Attempt: sets up x = 0.444... and 10x = 4.444...",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(b)(i) Full: reaches 9x = 4 and x = 4/9 in simplest form",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(b)(ii) States rational, consistent with part (i)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(c) Both squarings (6.76 and 7.29) correct, compared to 7, conclusion",
        "marks": 5,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "In part (c) the classic mistake is to \"check\" √7 by squaring √7 itself (getting 7) rather than squaring the BOUNDARY values and comparing them with 7. The valid method is: to test whether a < √7 < b, square the bounds to get a^2 < 7 < b^2. Also, in part (a) students frequently lose marks by giving the right classification with NO reason — the SEC scheme explicitly requires a reason, so always justify (perfect square / not a perfect square / terminating or recurring decimal).",
      "source": "SEC Chief Examiner's Report"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-0"
  },
  {
    "id": "maths-hl-2-1-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2017,
    "questionRef": "2017 HL P1 Q2",
    "questionText": "Express each of the following in the form 2^k, where k is a rational number. (a) √8 × 4. (b) (1/16) ÷ (⁴√2). Hence, or otherwise, solve the equation (√8 × 4)^x ÷ 2^5 = (1/16) ÷ (⁴√2), giving your answer as a fraction in its lowest terms.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Express ... Hence ... solve",
      "reminder": "Rewrite as power, then solve equation"
    },
    "ribbons": [
      {
        "label": "(a) Write √8 or 4 as power of 2 (e.g. 2^(3/2) or 2^2)",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(a) Correct answer 2^(7/2)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Write 1/16 = 2^(-4) or ⁴√2 = 2^(1/4)",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(b) Correct answer 2^(-17/4)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Form 2^(7x/2 - 5) or equate exponents 7x/2 - 5 = -17/4",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(c) x = 3/14",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The most common error is mishandling the index when a power is divided or raised to a further power. Students routinely write (2^(7/2))^x as 2^(7/2 + x) (adding instead of multiplying), or treat ÷ 2^5 as subtracting 5 from the base rather than from the exponent. Multiply exponents when raising a power to a power; subtract exponents when dividing. Keep everything as a single power of 2 before equating exponents, and never equate exponents until the bases are identical.",
      "source": "SEC Chief Examiner's Report"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-1"
  },
  {
    "id": "maths-ol-2-1-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2016,
    "questionRef": "2016 OL P1 Q1",
    "questionText": "(a) Evaluate each of the following without using a calculator. Give each answer as a natural number.\n    (i)  5^3\n    (ii) 2^(-2)\n    (iii) 36^(1/2)\n(b) Write 27^(2/3) in the form 3^n, where n is a natural number, and hence evaluate 27^(2/3).",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Evaluate",
      "reminder": "Work out the exact numerical value"
    },
    "ribbons": [
      {
        "label": "(a)(i) 5^3 = 125 (attempt at repeated multiplication 1 mark)",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(a)(ii) recognise negative index as reciprocal; 2^(-2) = 1/4",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(a)(iii) recognise power 1/2 as square root; 36^(1/2) = 6",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) express 27 as 3^3 / set up (3^3)^(2/3) (low partial credit)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) apply index rule to get 3^2 and evaluate as 9 (high partial credit)",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The single most common error here is mishandling fractional and negative indices. Students frequently compute 2^(-2) as -4 (treating the negative index as a sign change instead of a reciprocal) and read 36^(1/2) as \"36 divided by 2 = 18\" instead of the square root. Remember: a negative index flips to a fraction (a^(-n) = 1/a^n) and never makes the answer negative, while a fractional index a^(p/q) means the q-th root raised to the power p. For part (b), always rewrite the base as a power of the target (27 = 3^3) BEFORE applying (a^m)^n = a^(mn) — multiply the indices, never add them.",
      "source": "SEC Chief Examiner's Report"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-1"
  },
  {
    "id": "maths-ol-2-1-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2018,
    "questionRef": "2018 OL P1 Q3",
    "questionText": "(a) Simplify (2^5 x 2^4) / 2^7, giving your answer in the form 2^n where n is a natural number, and evaluate it.\n(b) Solve the equation 3^(x+1) = 81 for x. (Hint: write 81 as a power of 3.)",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Solve",
      "reminder": "Find the value of the unknown"
    },
    "ribbons": [
      {
        "label": "(a) multiply numerator: 2^5 x 2^4 = 2^9 (attempt adds indices 1 mark)",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(a) divide by subtracting indices to get 2^2",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(a) evaluate 2^2 = 4",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(b) write 81 = 3^4 (low partial credit)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) equate indices: x + 1 = 4",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(b) solve to get x = 3",
        "marks": 2,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The classic mistake in part (a) is to ADD the index in the denominator instead of subtracting it (writing 2^(5+4+7) = 2^16) or to \"cancel\" by dividing the indices (2^9 / 2^7 = 2^(9/7)). The rule for division is to SUBTRACT indices: a^m / a^n = a^(m-n). In part (b), the most common error is forgetting that the whole exponent is (x+1): students set x = 4 directly instead of x + 1 = 4. Always rewrite both sides to the same base first, then equate the FULL exponents and solve the resulting equation carefully.",
      "source": "SEC Chief Examiner's Report"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-1"
  },
  {
    "id": "maths-hl-2-2-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2018,
    "questionRef": "2018 HL P1 Q1",
    "questionText": "A person invests €18,000 in an account that earns compound interest at an Annual Equivalent Rate (AER) of 3.75%.\n(a) Calculate, correct to the nearest euro, the value of the investment at the end of 4 years.\n(b) The same person wishes instead to have €25,000 in the account at the end of 4 years. Calculate, correct to the nearest euro, the additional amount they would need to invest at the start, at the same AER of 3.75%.\n(c) A different financial product offers a nominal annual interest rate that is compounded monthly. The AER of this product is 3.75%. Find the monthly interest rate, correct to four significant figures, and hence find the nominal annual interest rate compounded monthly, correct to two decimal places.",
    "marks": 25,
    "minutes": 25,
    "answerKind": "steps",
    "commandWord": {
      "word": "Calculate / Find",
      "reminder": "Work out the numerical value shown"
    },
    "ribbons": [
      {
        "label": "(a) Correct formula with values substituted, P(1.0375)^4",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(a) Correct evaluation to €20,856",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(b) Sets up P = 25000/(1.0375)^4 and evaluates ≈ €21,577",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(b) Subtracts 18000 to get additional €3,577",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(c) Forms (1+i)^12 = 1.0375 and finds monthly rate 0.003072",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(c) Multiplies by 12 for nominal rate 3.69%",
        "marks": 4,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The most common error is in part (c): students confuse the AER with the nominal rate and either multiply 3.75% by 12 or divide by 12 directly. The AER is what one full year of monthly compounding actually produces, so you must take the 12th root of 1.0375 (not divide 3.75% by 12) to get the monthly rate, then multiply that monthly rate by 12 for the nominal rate. A second frequent slip is rounding (1.0375)^4 too early — keep full calculator accuracy until the final line, or the \"nearest euro\" answer drifts by several euro.",
      "source": "SEC Chief Examiner's Report"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-2"
  },
  {
    "id": "maths-ol-2-2-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2017,
    "questionRef": "2017 OL P1 Q1",
    "questionText": "A car is bought for €18 500. In the first year its value depreciates (loses value) by 12% of the purchase price. In the second year its value depreciates by a further 9% of its value at the end of the first year.\n(a) Find the value of the car at the end of the first year.\n(b) Find the value of the car at the end of the second year. Give your answer correct to the nearest euro.\n(c) Find the overall percentage of the original purchase price that the car has lost in value over the two years. Give your answer correct to one decimal place.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Work out and state the value"
    },
    "ribbons": [
      {
        "label": "(a) Attempt: writes 12% of 18 500 or 0.12 × 18 500 or finds 2 220",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(a) Full: correct value €16 280",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Attempt: finds 9% of 16 280 (1 465.20) or uses 0.91 × Year-1 value",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(b) Partial: correct unrounded value 14 814.80",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(b) Full: rounded correctly to €14 815",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Partial: correct loss 3 685.20 AND divides by 18 500 (or uses 0.8008 multiplier)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Full: correct answer 19.9%",
        "marks": 2,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The most common error is treating the second year's 9% as 9% of the original €18 500 rather than 9% of the reduced Year-1 value (€16 280). Depreciation compounds on the most recent value each year. A second frequent slip in part (c) is adding the percentages (12% + 9% = 21%) — this is wrong because the two percentages are taken of different amounts; the true loss (19.9%) is less than 21%.",
      "source": "SEC Chief Examiner's Report"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-2"
  },
  {
    "id": "maths-ol-2-2-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2019,
    "questionRef": "2019 OL P1 Q2",
    "questionText": "Aoife invests €4 000 in an account that pays compound interest at a rate of 3% per annum. The interest is added to the account at the end of each year.\n(a) Find the amount of money in the account at the end of 2 years.\n(b) Find the total interest earned over the 2 years.\n(c) Aoife must pay DIRT (Deposit Interest Retention Tax) at a rate of 33% on the interest she earns. Calculate the amount of DIRT she must pay on the interest earned over the 2 years.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find / Calculate",
      "reminder": "Work out and state the amount"
    },
    "ribbons": [
      {
        "label": "(a) Attempt: correct substitution into F = P(1+i)^t, i.e. 4 000 × (1.03)^2, or correct Year-1 amount 4 120",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(a) Partial: correct method fully shown but one slip, or (1.03)^2 = 1.0609 found",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(a) Full: correct amount €4 243.60",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Attempt: subtracts principal from their final amount (final − 4 000)",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(b) Full: correct interest €243.60",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Attempt: writes 33% of their interest, i.e. 0.33 × 243.60",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(c) Full: correct DIRT €80.39",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The most common mistake is calculating simple interest instead of compound interest — students multiply 4 000 × 0.03 × 2 = €240 and lose the extra \"interest on interest\" (the €3.60 difference here). With compound interest you must apply the rate to the growing balance each year, or use F = P(1 + i)^t. A second common error in part (c) is applying the 33% DIRT to the full account balance (€4 243.60) rather than only to the interest earned (€243.60) — DIRT is a tax on interest, not on the whole investment.",
      "source": "SEC Chief Examiner's Report"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-2"
  },
  {
    "id": "maths-hl-2-3-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2017,
    "questionRef": "2017 HL P2 Q4 (representative)",
    "questionText": "A solid metal object is made by attaching a right circular cone exactly on top of a hemisphere, so that the flat circular face of the cone coincides with the flat circular face of the hemisphere. Both the cone and the hemisphere have radius r = 6 cm. The perpendicular height of the cone is 8 cm.\n\n(a) Show that the slant height of the cone is 10 cm.\n\n(b) Calculate the total surface area of the solid object (the curved surface of the cone plus the curved surface of the hemisphere). Give your answer in terms of π.\n\n(c) The solid object is melted down and recast, without any loss of metal, into a single solid sphere. Calculate the radius of this sphere, giving your answer correct to two decimal places.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Calculate",
      "reminder": "Work out the numerical value, showing working"
    },
    "ribbons": [
      {
        "label": "(a) Sets up l² = r² + h² with values substituted, e.g. l = √(6²+8²)",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(a) Shows l = √100 = 10 cm",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) One correct curved area: πrl = 60π OR 2πr² = 72π",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(b) Both curved areas correct and summed (flat faces excluded): 60π + 72π = 132π cm²",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Correct total volume 240π (or both components 96π and 144π), or correct equation (4/3)πR³ = volume",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(c) Solves to R = ∛180 ≈ 5.65 cm to two decimals",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The single most common error is counting the flat circular faces in the surface area. Because the cone sits exactly on the hemisphere, the two flat circles are joined internally and form NO part of the outside surface — so you use only the curved areas (πrl and 2πr²), never πr² for either base. Students reflexively add πr² 'for the base' and lose marks. A close second: using the perpendicular height (8) instead of the slant height (10) in the cone's curved surface area πrl.",
      "source": "SEC Chief Examiner's Report"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-3"
  },
  {
    "id": "maths-hl-2-3-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2019,
    "questionRef": "2019 HL P2 Q5 (representative)",
    "questionText": "A sector of a circle has a radius of 9 cm and the angle at the centre of the sector is 120°. Take π = 3.14 where a decimal value is required, unless stated otherwise.\n\n(a) Find the length of the arc of this sector. Give your answer in terms of π.\n\n(b) Find the area of this sector. Give your answer in terms of π.\n\n(c) The sector is rolled up and the two straight edges (the two radii) are joined together to form the curved surface of a right circular cone, with the arc of the sector becoming the circumference of the circular base of the cone.\n   (i) Find the radius of the base of the cone formed, giving your answer as a fraction or exact value.\n   (ii) Hence find the vertical (perpendicular) height of the cone, correct to two decimal places.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Obtain the answer, showing necessary working"
    },
    "ribbons": [
      {
        "label": "(a) Uses θ/360 = 1/3, or formula (θ/360)(2πR) with substitution",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(a) Arc length = 6π cm",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Formula (θ/360)(πR²) with values substituted, or 81π seen",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(b) Sector area = 27π cm²",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c)(i) Recognises base circumference = arc length: sets 2πr = 6π",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(c)(i) r = 3 cm",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c)(ii) Recognises slant height = 9 and writes h² = 9² − 3² (h² = l² − r²)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(c)(ii) h = √72 = 6√2 ≈ 8.49 cm",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The classic mistake in the 'roll the sector into a cone' question is mixing up which length becomes what. You must recognise two transfers: the sector's RADIUS (9 cm) becomes the cone's SLANT height (not the vertical height), and the sector's ARC LENGTH (6π) becomes the base CIRCUMFERENCE (not the base radius). The frequent error is treating 9 cm as the perpendicular height, or setting the arc length equal to the radius. Once r = 3 and l = 9 are correctly identified, h is found from h² = l² − r² (NOT l² + r²) — another common slip is adding instead of subtracting because the slant height is the hypotenuse.",
      "source": "SEC Chief Examiner's Report"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-3"
  },
  {
    "id": "maths-ol-2-3-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2017,
    "questionRef": "2017 OL P2 Q4",
    "questionText": "A cylindrical water tank has a circular base of radius 0.6 m and a height of 1.4 m.\n(a) Calculate the volume of the tank, in cubic metres. Give your answer correct to two decimal places. Take pi = 3.14.\n(b) Water is poured into the empty tank at a rate of 0.05 cubic metres per minute. Find, correct to the nearest minute, how long it takes to fill the tank completely.\n(c) The curved surface of the tank (not including the top or bottom) is to be painted. Calculate the area of the curved surface, in square metres, correct to two decimal places. Take pi = 3.14.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Calculate / Find",
      "reminder": "Work out the numerical value shown"
    },
    "ribbons": [
      {
        "label": "(a) Attempt: correct formula V = pi r^2 h with a value substituted, or r^2 = 0.36 found",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(a) Full credit: V = 1.58 m^3 correct to 2 d.p.",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Attempt: divides a volume by 0.05, or sets up Time = Volume / rate",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(b) Full credit: 32 minutes, correctly rounded",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Attempt: correct CSA formula 2 pi r h with a value substituted",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(c) Full credit: 5.28 m^2 correct to 2 d.p.",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The single most common error is mixing up the formulae: students use 2 pi r h for volume or pi r^2 h for surface area. Anchor it by units — volume needs three lengths multiplied (gives m^3: r x r x h), area needs two (gives m^2: r x h or r x r). A second frequent slip in part (b) is rounding the volume to 1.58 before dividing; carry the full unrounded value through the calculation and only round the final answer.",
      "source": "SEC Chief Examiner's Report"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-3"
  },
  {
    "id": "maths-ol-2-3-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2019,
    "questionRef": "2019 OL P2 Q3",
    "questionText": "A rectangular field is 80 m long and 55 m wide.\n(a) Calculate the perimeter of the field, in metres.\n(b) Calculate the area of the field, in square metres.\n(c) A path 2 m wide is built along the inside of the entire boundary of the field, all the way around. The rest of the field (the inner rectangle surrounded by the path) is grass. Calculate the area of grass, in square metres.\n(d) Grass seed is sold in bags. One bag covers 250 square metres. Calculate the smallest number of full bags needed to seed the grass area found in part (c).",
    "marks": 20,
    "minutes": 20,
    "answerKind": "steps",
    "commandWord": {
      "word": "Calculate",
      "reminder": "Work out the numerical value shown"
    },
    "ribbons": [
      {
        "label": "(a) Attempt: adds two or more sides, or uses 2(l + w) with a value in",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(a) Full credit: 270 m",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Attempt: multiplies length by width",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(b) Full credit: 4400 m^2",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Attempt: reduces at least one dimension by the path width",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(c) Full credit: 3876 m^2 (76 x 51)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(d) Attempt: divides grass area by 250",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(d) Full credit: 16 bags, correctly rounded up",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "In part (c) the classic mistake is subtracting the path width only once (80 - 2) instead of twice (80 - 2 - 2), forgetting the path runs along BOTH opposite edges. Sketch the rectangle and mark the 2 m strip on all four sides — that makes it obvious each dimension loses 2 + 2 = 4 m. In part (d) the other trap is rounding 15.504 down to 15; because partial bags can't be bought and 15 bags fall short, you must always round UP for \"how many full bags are needed\".",
      "source": "SEC Chief Examiner's Report"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-3"
  }
];
