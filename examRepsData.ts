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
  },
  {
    "id": "maths-hl-0-0-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2017,
    "questionRef": "2017 HL P2 Q4",
    "questionText": "A four-digit security code is to be formed using digits from the set {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}.\n\n(a) How many four-digit codes can be formed if each digit may be used more than once and the code may start with 0? Give a reason for your answer.\n\n(b) How many four-digit codes can be formed if no digit may be repeated and the code may not start with 0?\n\n(c) A code is said to be \"even\" if its last digit is one of 0, 2, 4, 6 or 8. Using the conditions in part (b) (no repeated digit and the code may not start with 0), find how many of the codes are even.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Work out the numerical answer, showing the counting reasoning."
    },
    "ribbons": [
      {
        "label": "(a) Attempt: some use of 10 as a choice count, e.g. 10 × 10 or a partial product",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(a) Full: 10⁴ = 10 000 with valid reason (Fundamental Principle / independent choices)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(b) Attempt: recognises first digit has 9 choices OR sets up a product without repetition",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(b) Full: 9 × 9 × 8 × 7 = 4 536",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Attempt: identifies last digit ∈ {0,2,4,6,8} and/or that 0 must be treated separately",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(c) Partial: one case fully evaluated (504 or 1 792), or both cases set up with one slip",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(c) Full: both cases correct and summed to 2 296",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The classic error is to fix the last digit at \"5 choices\" (0,2,4,6,8) and the first digit at \"8 choices\" and multiply 5 × 8 × 8 × 7 = 2 240, forgetting that when 0 is the last digit it does NOT reduce the first-digit count (0 was already banned from the front). The digit 0 is \"doubly special\" — it is the only even digit barred from the leading position — so it must be handled in its own case. Whenever a \"no leading zero\" rule overlaps with a condition that itself involves 0, split into cases rather than multiplying a single chain of choices.",
      "source": "2017 HL P2 Q4 worked solution and examiner notes"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-0"
  },
  {
    "id": "maths-hl-0-0-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2019,
    "questionRef": "2019 HL P2 Q3",
    "questionText": "A committee of 5 people is to be chosen from a group of 7 women and 5 men.\n\n(a) In how many ways can the committee be chosen if there are no restrictions?\n\n(b) In how many ways can the committee be chosen if it must contain exactly 3 women and 2 men?\n\n(c) In how many ways can the committee be chosen if it must contain at least 4 women?\n\n(d) Two of the 12 people are a married couple. In how many ways can the committee of 5 be chosen so that this couple are not both on the committee together?",
    "marks": 20,
    "minutes": 20,
    "answerKind": "steps",
    "commandWord": {
      "word": "Choose",
      "reminder": "Count the number of ways to select the committee (order does not matter, use combinations)."
    },
    "ribbons": [
      {
        "label": "(a) Attempt: recognises combinations are needed / writes C(12,5)",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(a) Full: C(12,5) = 792",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Attempt: writes C(7,3) or C(5,2) or product structure",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(b) Full: C(7,3) × C(5,2) = 350",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Attempt: identifies \"at least 4\" = (4W,1M) and (5W,0M) cases",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(c) Partial: one case correct (175 or 21)",
        "marks": 1,
        "kind": "method"
      },
      {
        "label": "(c) Full: 175 + 21 = 196",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(d) Attempt: chooses a valid method (complement or direct cases)",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(d) Partial: finds \"both on committee\" = 120, or one direct case correct",
        "marks": 1,
        "kind": "method"
      },
      {
        "label": "(d) Full: 792 − 120 = 672",
        "marks": 2,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "Two errors recur here. First, in part (c) students treat \"at least 4 women\" as a single combination instead of summing the disjoint cases (4W,1M) and (5W,0M) — and a few wrongly add a \"0 men\" man-choice as 0 rather than C(5,0)=1. Second, in part (d) the natural instinct is C(12,5) − C(10,3): this is correct only because the \"both present\" count fixes the 2 couple seats and chooses 3 from the remaining 10. The frequent slip is to compute C(10,4) (choosing 4 more, forgetting that placing both of the couple already uses 2 of the 5 seats). Always check how many seats remain after a forced selection.",
      "source": "2019 HL P2 Q3 worked solution and examiner notes"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-0"
  },
  {
    "id": "maths-ol-0-0-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2017,
    "questionRef": "2017 OL P2 Q1",
    "questionText": "A restaurant offers a \"Build Your Own\" lunch deal. A customer must choose exactly one item from each of the following:\n- a Starter (there are 4 to choose from)\n- a Main course (there are 6 to choose from)\n- a Drink (there are 3 to choose from)\n\n(a) Using the Fundamental Principle of Counting, find the total number of different lunch deals a customer can make.\n\n(b) The restaurant decides to add a Dessert option to the deal, where the customer chooses exactly one Dessert from a choice of 5. Find how many different lunch deals are now possible.\n\n(c) A customer is a vegetarian and will only eat 2 of the 6 main courses. All other choices stay the same as in part (b). Find how many different lunch deals are available to this customer.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Work out the numerical answer, showing the calculation."
    },
    "ribbons": [
      {
        "label": "(a) Multiplies the correct three numbers (4 x 6 x 3) to get 72",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(b) Multiplies result by 5 (4 x 6 x 3 x 5) to get 360",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(c) Replaces 6 with 2 and multiplies 4 x 2 x 3 x 5 to get 120",
        "marks": 5,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The single most common error is ADDING the numbers of choices instead of MULTIPLYING them. The Fundamental Principle of Counting applies when you make one choice AND another choice AND another - each independent stage multiplies the running total. Students only add when counting mutually exclusive options (\"either... or...\"). Here every customer picks a starter and a main and a drink, so the operation is multiplication.",
      "source": "Fundamental Principle of Counting"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-0"
  },
  {
    "id": "maths-ol-0-0-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2019,
    "questionRef": "2019 OL P2 Q4",
    "questionText": "A club is forming a committee and filling officer positions from its members.\n\n(a) The club has 8 members. Three different officer positions are to be filled: Chairperson, Secretary and Treasurer. No member can hold more than one position. In how many different ways can these three positions be filled?\n\n(b) Separately, the club wants to choose a sub-committee of 3 members from the same 8 members. In a sub-committee, no one holds a special title - the 3 members are all equal. In how many different ways can this sub-committee of 3 be chosen?\n\n(c) Explain clearly why your answer to part (a) is larger than your answer to part (b).",
    "marks": 20,
    "minutes": 20,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find / Explain",
      "reminder": "Compute the counts, then give a clear reason for the difference."
    },
    "ribbons": [
      {
        "label": "(a) Recognises order matters and computes 8 x 7 x 6 (8P3) = 336",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(b) Recognises order does not matter and sets up 8C3 = (8 x 7 x 6)/(3 x 2 x 1) = 56",
        "marks": 10,
        "kind": "method"
      },
      {
        "label": "(c) Explains each selection of 3 corresponds to 3! = 6 orderings, so (a) over-counts by a factor of 6",
        "marks": 5,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "The classic mistake is treating both parts identically - either using permutations for both or combinations for both. The deciding question is always: \"Does the order (or the labelling) of the chosen items matter?\" Distinct titles (Chairperson, Secretary, Treasurer) mean order matters, so use nPr (or the multiplication 8 x 7 x 6). An unlabelled group where everyone is equal means order does not matter, so use nCr and divide by the arrangements of the chosen group (3!). Forgetting to divide by 3! - leaving the answer as 336 in part (b) - is the most frequently lost mark.",
      "source": "Permutations vs Combinations"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-0"
  },
  {
    "id": "maths-hl-0-1-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2016,
    "questionRef": "2016 HL P2 Q1",
    "questionText": "A bag contains 5 red discs, 4 green discs and 3 yellow discs. The discs are identical apart from colour. Two discs are drawn at random from the bag, one after the other, without replacement.\n\n(a) Find the probability that both discs drawn are red.\n\n(b) Find the probability that the two discs drawn are of different colours.\n\n(c) Given that the two discs drawn are of the same colour, find the probability that they are both green.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Work out the value and show the calculation that produces it."
    },
    "ribbons": [
      {
        "label": "(a) Recognises product of two fractions without replacement, e.g. (5/12) × (·/11)",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(a) Arrives at P(both red) = 5/33 (= 20/132)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(b) Identifies same/different-colour approach with one correct same-colour term, e.g. (4/12)(3/11)",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(b) All three same-colour terms summed to 19/66 and complement taken: 47/66",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Writes conditional ratio P(both green)/P(same colour) with numerator or denominator correct",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(c) Correct ratio (12/132)/(38/132) simplified to 6/19",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The classic error in part (c) is to compute the unconditional P(both green) = 12/132 = 1/11 instead of conditioning. The phrase \"Given that … are of the same colour\" restricts the sample space: you must divide by P(same colour), not by 1. A second frequent slip in part (a)/(b) is to use /12 again on the second draw (treating it as with replacement) — \"without replacement\" means the denominator drops to 11.",
      "source": "2016 HL P2 Q1"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-1"
  },
  {
    "id": "maths-hl-0-1-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2018,
    "questionRef": "2018 HL P2 Q4",
    "questionText": "In a game at a school fundraiser, a player rolls a single fair six-sided die once and is paid according to the number shown:\n\n- If a 6 is rolled, the player wins €5.\n- If a 4 or a 5 is rolled, the player wins €2.\n- If a 1, 2 or 3 is rolled, the player wins nothing (€0).\n\nIt costs €2 to play the game.\n\n(a) Complete a probability distribution table for X, the amount paid out to the player (before the cost of playing is considered), and hence find E(X), the expected payout per game.\n\n(b) The game is described as \"fair\" if, on average, a player neither wins nor loses money in the long run. By considering the €2 cost to play, determine whether this game is fair. Justify your answer.\n\n(c) The organisers want to make an average profit of exactly €0.50 per game by changing only the prize for rolling a 6 (keeping all other prizes and the €2 cost unchanged). Find the new prize that should be paid for rolling a 6.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Work out the value, showing the working that produces it (here: complete the table, then determine and find)."
    },
    "ribbons": [
      {
        "label": "(a) Correct probabilities for at least two payouts, or a correctly grouped table, e.g. P(0)=1/2, P(2)=1/3",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(a) Complete distribution table: P(0)=1/2, P(2)=1/3, P(5)=1/6 summing to 1",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(a) Applies E(X) = Σ x·P(x) to obtain E(X) = €1.50",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Forms net comparison E(X) versus cost, e.g. 1.50 − 2 or states fairness criterion",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(b) Obtains −€0.50 and concludes, justified, that the game is NOT fair",
        "marks": 3,
        "kind": "explain"
      },
      {
        "label": "(c) Sets up E(X) = 2/3 + k/6 with k as the unknown prize",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(c) Forms correct equation linking profit to 0.50, e.g. 2 − (2/3 + k/6) = 0.5",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(c) Solves to k = €5 with valid check/justification",
        "marks": 2,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The most common mistake is sign confusion between \"expected payout to the player\" and \"expected profit to the organisers\" — they are opposite in sign. Students frequently forget to subtract the €2 stake in part (b), reporting €1.50 and wrongly calling the game favourable to the player. Define clearly whose point of view you are taking: a game is fair when E(net to player) = 0, i.e. E(payout) = cost. In part (c), be careful that \"profit to the organiser\" = cost − expected payout, not the other way around.",
      "source": "2018 HL P2 Q4"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-1"
  },
  {
    "id": "maths-ol-0-1-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2016,
    "questionRef": "2016 OL P2 Q4(a)",
    "questionText": "A box contains 12 counters that are identical except for colour. There are 5 red counters, 3 blue counters and 4 green counters. One counter is drawn at random from the box.\n(a) Find the probability that the counter drawn is blue.\n(b) Find the probability that the counter drawn is red or green.\n(c) The 12 counters are placed in the box again. Aoife says, \"The probability of drawing a yellow counter is 0.\" Explain why Aoife is correct.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find / Explain",
      "reminder": "Find: work out the value. Explain: give a clear reason linked to the result."
    },
    "ribbons": [
      {
        "label": "(a) Correct probability 3/12 or 1/4 or 0.25",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(b) Correct probability 9/12 or 3/4 or 0.75",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(c) Valid explanation: no yellow counters / impossible event / probability 0",
        "marks": 5,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "The most common error is in part (b): students compute P(red) and P(green) correctly but then multiply (5/12 x 4/12) instead of adding, confusing \"or\" with \"and\". For mutually exclusive events the word \"or\" signals addition. A quick sanity check is that an \"or\" probability of two events must be larger than either single event — multiplying gives a smaller number, which should immediately look wrong.",
      "source": "2016 OL P2 Q4(a)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-1"
  },
  {
    "id": "maths-ol-0-1-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2018,
    "questionRef": "2018 OL P2 Q3(b)",
    "questionText": "A fair six-sided die has its faces numbered 1, 2, 3, 4, 5 and 6. The die is rolled once.\n(a) List all the possible outcomes (the sample space) when the die is rolled.\n(b) Find the probability of rolling a number greater than 4.\n(c) The die is now rolled 300 times. Based on the probability in part (b), how many times would you expect to roll a number greater than 4?\n(d) When the die was actually rolled 300 times, a number greater than 4 came up 86 times. Give one reason why this result differs from your answer in part (c).",
    "marks": 20,
    "minutes": 20,
    "answerKind": "steps",
    "commandWord": {
      "word": "List / Find / Give",
      "reminder": "List: write out every item. Find: work out the value. Give: state a valid reason."
    },
    "ribbons": [
      {
        "label": "(a) Sample space fully and correctly listed {1,2,3,4,5,6}",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(b) Correct probability 2/6 or 1/3 or 0.33",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(c) Correct expected value 100 (= 1/3 x 300)",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(d) Valid reason: random/chance variation, theoretical vs actual, finite trials",
        "marks": 5,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "The most common mistake is in part (b): students read \"greater than 4\" as including 4, giving 3 outcomes {4, 5, 6} and an answer of 3/6 = 1/2. \"Greater than\" is strict and excludes the boundary value; \"4 or more\" / \"at least 4\" would include it. Underlining the exact inequality wording before counting outcomes prevents this off-by-one error. In part (d), avoid blaming the die (\"it was biased\") — the die is stated to be fair, so the correct reason is ordinary random variation.",
      "source": "2018 OL P2 Q3(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-1"
  },
  {
    "id": "maths-hl-0-2-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2017,
    "questionRef": "2017 HL P2 Q4",
    "questionText": "A bag contains 12 discs that are identical except for colour. There are 5 red discs, 4 blue discs and 3 green discs. Two discs are drawn at random from the bag, one after the other, without replacement.\n(a) Draw a tree diagram to represent this experiment, showing the probability on every branch. (Leave the probabilities as fractions.)\n(b) Find the probability that the two discs drawn are the same colour.\n(c) Find the probability that at least one of the two discs drawn is green.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "paper",
    "commandWord": {
      "word": "Find",
      "reminder": "Work out the value or probability, showing the calculation that produces it."
    },
    "ribbons": [
      {
        "label": "(a) Attempt: first-draw branches with correct probabilities",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(a) Full: all second-draw branches with correct conditional probabilities (denominator 11)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(b) Attempt: one correct same-colour product, e.g. (5/12)(4/11), or correct method stated",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(b) Full: all three products correct and summed to 19/66 (or 38/132)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(c) Attempt: recognises P(at least one green) = 1 - P(no green) or sets up valid direct method",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(c) Full: P(no green) = (9/12)(8/11) = 6/11 and final answer 5/11",
        "marks": 5,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The single most common error is forgetting \"without replacement\" - students reuse 12 as the denominator and a full count of each colour on the second draw, instead of reducing the total to 11 and reducing the count of the colour already drawn. In part (c), the slick route is the complement (1 - P(no green)); students who instead add up every case containing a green (GG, GR, RG, GB, BG) frequently drop a case or double-count, so always prefer the complement when the phrase \"at least one\" appears.",
      "source": "2017 HL P2 Q4"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-2"
  },
  {
    "id": "maths-hl-0-2-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2019,
    "questionRef": "2019 HL P2 Q3",
    "questionText": "A spinner is divided into sectors numbered 1, 2, 3 and 4. The spinner is biased. The table below shows the probability of the spinner landing on each of three of the numbers:\nNumber 1: probability 0.15\nNumber 2: probability 0.30\nNumber 3: probability 0.25\nNumber 4: probability not given.\n(a) Find the probability that the spinner lands on the number 4.\n(b) The spinner is spun once. Find the probability that it lands on an even number.\n(c) The spinner is spun twice. Find the probability that the sum of the two numbers it lands on is exactly 5. (Assume the two spins are independent.)",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Work out the value or probability, showing the calculation that produces it."
    },
    "ribbons": [
      {
        "label": "(a) Attempt: uses the idea that probabilities sum to 1 (e.g. writes 1 - [...])",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(a) Full: correct answer 0.30",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Full: P(2) + P(4) = 0.60",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Attempt: identifies at least one correct ordered pair summing to 5 and multiplies its probabilities, or lists the pairs",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(c) Full: all four ordered pairs found, probabilities multiplied and summed correctly to 0.24",
        "marks": 4,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "In part (c) the classic mistake is listing only the unordered combinations {1,4} and {2,3} and so computing 0.045 + 0.075 = 0.12, which halves the true answer. On two distinct spins, order matters: (1,4) and (4,1) are separate outcomes, as are (2,3) and (3,2). Students must also remember to multiply (independent spins) and then add (mutually exclusive cases) - confusing these two operations, or doing only one of them, is the other frequent error.",
      "source": "2019 HL P2 Q3"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-2"
  },
  {
    "id": "maths-ol-0-2-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2016,
    "questionRef": "2016 OL P2 Q2",
    "questionText": "A bag contains 5 red discs, 3 blue discs and 2 yellow discs. The discs are identical apart from colour. A disc is drawn at random from the bag.\n(a) How many discs are in the bag in total?\n(b) Find the probability that the disc drawn is blue.\n(c) Find the probability that the disc drawn is red or yellow.\n(d) Find the probability that the disc drawn is not blue.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Work out the value or probability and show your reasoning."
    },
    "ribbons": [
      {
        "label": "(a) Attempt: adds two of the three values / partial addition",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(a) Full: correct total 10",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(b) Attempt: denominator 10 OR numerator 3 / sets up fraction",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(b) Full: 3/10 (or 0.3 / 30%)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Attempt: identifies 5 + 2 = 7 favourable OR uses 1 − 3/10",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(c) Full: 7/10 (or 0.7 / 70%)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(d) Attempt: writes 1 − P(blue) OR 1 − 3/10",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(d) Full: 7/10 (or 0.7 / 70%)",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The most common error is forgetting to count ALL outcomes when forming the denominator — students often divide by the number of colours (3) or by a single colour count rather than by the total of 10 discs. Always establish the total sample space first, then count favourable outcomes for the numerator. Probabilities must lie between 0 and 1, so a quick sanity check (a fraction over 10 here) catches slips immediately.",
      "source": "SEC Project Maths Ordinary Level — Probability"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-2"
  },
  {
    "id": "maths-ol-0-2-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2018,
    "questionRef": "2018 OL P2 Q4",
    "questionText": "A fair six-sided die, with faces numbered 1, 2, 3, 4, 5 and 6, is rolled once.\n(a) List all the possible outcomes when the die is rolled.\n(b) Find the probability that the number rolled is even.\n(c) Find the probability that the number rolled is greater than 4.\n(d) Find the probability that the number rolled is an even number greater than 4.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "List the sample space, then work out each probability with reasoning."
    },
    "ribbons": [
      {
        "label": "(a) Attempt: lists at least some outcomes / shows 1–6 partially",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(a) Full: all six outcomes {1, 2, 3, 4, 5, 6} listed",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Attempt: identifies even numbers 2, 4, 6 OR numerator 3 / denominator 6 seen",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(b) Full: 3/6 or 1/2 (or 0.5 / 50%)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Attempt: identifies 5 and 6 (does not include 4) OR sets up fraction over 6",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(c) Full: 2/6 or 1/3",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(d) Attempt: finds the intersection idea / lists {5, 6} or {2, 4, 6}",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(d) Full: identifies 6 as the only outcome and states 1/6",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The classic trap is in part (c)/(d) with the phrase \"greater than 4\": students wrongly include 4 itself (that would be \"4 or greater\" / \"at least 4\"). \"Greater than\" is strict, so 4 is excluded and only {5, 6} count. The second common error in part (d) is treating \"even AND greater than 4\" as two separate events to add together, or adding the probabilities from (b) and (c); instead you must find the outcomes satisfying BOTH conditions simultaneously (the intersection), which here is just {6}. Read compound conditions carefully and list the qualifying outcomes explicitly.",
      "source": "SEC Project Maths Ordinary Level — Probability"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-2"
  },
  {
    "id": "maths-hl-0-3-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2018,
    "questionRef": "2018 HL P2 Q6 (representative)",
    "questionText": "A national newspaper publishes the following headline based on an online poll it ran on its website: \"75% of Irish adults support a new tax on sugary drinks.\"\n\nThe detail accompanying the article states the following:\n- The poll was conducted by inviting readers of the newspaper's website to click a link and vote \"Yes\" or \"No\" over a 24-hour period.\n- A total of 1,200 people responded, of whom 900 voted \"Yes\".\n- The newspaper claims the result is accurate to within a margin of error of ±2.9% at the 95% confidence level.\n\n(a) Using the data given, verify the figure of 75% quoted in the headline. (5 marks)\n\n(b) The newspaper's poll is described as a sample of \"Irish adults\". Identify the population the newspaper is generalising to, and identify the sample that was actually used. (5 marks)\n\n(c) Give TWO distinct reasons, based on how the data was collected, why this poll may NOT give a reliable estimate of the true level of support among all Irish adults. In each case, explain clearly the effect the issue could have on the result. (10 marks)\n\n(d) The newspaper quotes a margin of error of ±2.9%. A statistician argues that, even if this margin of error has been calculated correctly using the standard formula, quoting it in this context is misleading. State the standard formula a poll of this size would use for the margin of error at 95% confidence, verify the ±2.9% figure, and explain in one sentence why the statistician says quoting it here is misleading. (5 marks)",
    "marks": 25,
    "minutes": 25,
    "answerKind": "steps",
    "commandWord": {
      "word": "Verify / Identify / Give / Explain / State",
      "reminder": "Verify = show the calculation produces the stated figure; Identify/State = name precisely; Give/Explain = state and justify clearly."
    },
    "ribbons": [
      {
        "label": "(a) Attempt: writes 900/1200 or equivalent ratio",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(a) Full credit: shows = 0.75 = 75%",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Population correctly identified (all Irish adults)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(b) Sample correctly identified (the 1,200 self-selected website voters)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) First valid reason stated",
        "marks": 3,
        "kind": "explain"
      },
      {
        "label": "(c) Effect of first reason explained",
        "marks": 2,
        "kind": "explain"
      },
      {
        "label": "(c) Second valid reason stated",
        "marks": 3,
        "kind": "explain"
      },
      {
        "label": "(c) Effect of second reason explained",
        "marks": 2,
        "kind": "explain"
      },
      {
        "label": "(d) States formula 1/√n",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(d) Verifies ≈ 2.9%",
        "marks": 1,
        "kind": "method"
      },
      {
        "label": "(d) Explains why misleading (sample not random / self-selected)",
        "marks": 2,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "The classic error here is treating the margin of error as if it fixes the poll. Candidates correctly compute ±2.9% and then conclude the poll is \"accurate to ±2.9%\", missing the central point: the margin of error formula only accounts for random sampling variation and assumes a properly randomised sample. It says nothing about bias. A self-selected online poll can be wildly wrong no matter how small the margin of error, because bias is not reduced by the formula. Examiners reward the candidate who explicitly distinguishes random error (which the margin of error captures) from bias (which it does not).",
      "source": "2018 HL P2 Q6 (representative)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-3"
  },
  {
    "id": "maths-hl-0-3-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2017,
    "questionRef": "2017 HL P2 Q9 (representative)",
    "questionText": "A health-supplements company runs an advertisement that says: \"In a study, people who took our daily vitamin had 30% fewer colds than people who did not. Take our vitamin to avoid colds this winter!\"\n\nThe study referred to was a survey. Researchers contacted 1,000 adults in January and asked them (i) whether they had taken a daily vitamin supplement throughout the previous winter, and (ii) how many colds they had during that winter. The adults were not assigned to take or not take the vitamin; they simply reported what they had done. The researchers then compared the two groups.\n\n(a) State whether this study is an observational study or a designed experiment, and give one reason for your answer. (5 marks)\n\n(b) The advertisement uses the result to claim that taking the vitamin will cause a person to have fewer colds. Explain why the design of this study does not justify a claim of cause and effect. (5 marks)\n\n(c) Describe one specific confounding variable that could explain the difference between the two groups, and explain clearly how it could produce the observed 30% difference without the vitamin having any real effect. (5 marks)\n\n(d) Describe how the researchers could have designed a study that WOULD allow a valid cause-and-effect conclusion to be drawn. Your answer should refer to randomisation and to a control group, and should explain the role of each. (10 marks)",
    "marks": 25,
    "minutes": 25,
    "answerKind": "written",
    "commandWord": {
      "word": "State / Explain / Describe",
      "reminder": "State = give a clear decision; Explain = give reasons with justification; Describe = set out the design/feature in detail, including the role of each element."
    },
    "ribbons": [
      {
        "label": "(a) States observational study",
        "marks": 2,
        "kind": "name"
      },
      {
        "label": "(a) Valid reason: subjects not assigned a treatment / researcher only observed",
        "marks": 3,
        "kind": "explain"
      },
      {
        "label": "(b) Attempt: partial idea that \"other factors\" exist",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(b) Full explanation: non-random groups mean confounders prevent inferring cause (association ≠ causation)",
        "marks": 3,
        "kind": "explain"
      },
      {
        "label": "(c) Names a specific valid confounder",
        "marks": 2,
        "kind": "name"
      },
      {
        "label": "(c) Explains how it produces the difference with no real vitamin effect",
        "marks": 3,
        "kind": "explain"
      },
      {
        "label": "(d) States randomised controlled experiment / RCT",
        "marks": 2,
        "kind": "name"
      },
      {
        "label": "(d) Describes random assignment and states its role (balances confounders)",
        "marks": 4,
        "kind": "explain"
      },
      {
        "label": "(d) Describes control/placebo group and states its role (comparison baseline)",
        "marks": 4,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "The most common and most heavily penalised mistake is confusing the roles of the control group and randomisation in part (d). Many candidates say \"use a control group\" and stop, or claim randomisation \"removes bias\" without saying what it actually does. Examiners want two distinct ideas: the control group provides the comparison (the baseline for \"what happens without the vitamin\"), while randomisation is what balances out confounding variables between the groups so that the comparison is fair. A design with a control group but no randomisation still allows confounding; randomisation is the specific feature that licenses a cause-and-effect conclusion. State both roles separately and explicitly.",
      "source": "2017 HL P2 Q9 (representative)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-3"
  },
  {
    "id": "maths-ol-0-3-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2017,
    "questionRef": "2017 OL P2 Q4 (representative)",
    "questionText": "A national newspaper publishes the following headline above an advertisement for \"BrightWhite\" toothpaste:\n\n\"9 out of 10 dentists recommend BrightWhite!\"\n\nThe small print at the bottom of the advertisement states the following:\n\"Survey carried out by the makers of BrightWhite. 10 dentists were asked. Each dentist was given a free year's supply of BrightWhite before being asked the question.\"\n\n(a) The advertisement claims to be based on a survey. State the population that the makers of BrightWhite would need to survey in order to make a fair claim about all dentists.\n\n(b) Give TWO different reasons why this survey may be biased. In each case, refer to the information given above.\n\n(c) The makers say the sample was \"random\". A sample of only 10 dentists was used. Give one reason why a sample of 10 dentists is too small to draw a reliable conclusion about all dentists in the country.\n\n(d) Suggest one improvement the makers could make so that the survey would give a more trustworthy result.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "written",
    "commandWord": {
      "word": "State / Give / Suggest",
      "reminder": "State = name it clearly; Give/Suggest = provide a valid reason or improvement, using the specific information in the question."
    },
    "ribbons": [
      {
        "label": "(a) Identifies correct population (all dentists in the country / all registered dentists)",
        "marks": 5,
        "kind": "name"
      },
      {
        "label": "(b) Two valid, distinct reasons for bias, each referring to the given information (3 marks each)",
        "marks": 6,
        "kind": "explain"
      },
      {
        "label": "(c) Valid reason why n = 10 is too small (too small a fraction / one dentist = 10% / not representative)",
        "marks": 5,
        "kind": "explain"
      },
      {
        "label": "(d) One sensible improvement that addresses a stated flaw (0 if it just repeats the flawed method)",
        "marks": 4,
        "kind": "application"
      }
    ],
    "lesson": {
      "text": "The most common mistake is giving vague answers that do not USE the information in the question. \"The sample is biased because it's too small\" is not enough for part (b) - the marking scheme rewards candidates who point to the SPECIFIC features given (the makers ran it themselves; the dentists got a free gift). Always quote the detail in the stem (\"because each dentist was given a free year's supply...\") rather than writing a generic textbook sentence. Also, do not confuse \"population\" (the whole group the claim is about) with \"sample\" (the part actually surveyed).",
      "source": "2017 OL P2 Q4 (representative)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-3"
  },
  {
    "id": "maths-hl-0-4-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2017,
    "questionRef": "2017 HL P2 Q1",
    "questionText": "A researcher wants to investigate how many hours per week students in a large secondary school (with 1,200 students across six year groups: First Year to Sixth Year) spend on part-time paid work.\n\n(a) The researcher decides to use a sample of 60 students rather than surveying all 1,200 students. Give one advantage and one disadvantage of using a sample instead of carrying out a census.\n\n(b) The researcher considers the following method: \"Stand at the school's main exit at 4 p.m. on a Friday and ask the first 60 students who leave how many hours they work each week.\" State, with a reason, whether this is likely to produce a representative sample of the school's students.\n\n(c) The number of students in each year group is shown below:\nFirst Year: 240, Second Year: 220, Third Year: 200, Fourth Year: 160, Fifth Year: 200, Sixth Year: 180.\nThe researcher decides instead to take a stratified random sample of 60 students, with the year groups as the strata. Calculate the number of students that should be selected from each year group.\n\n(d) Explain briefly how the researcher could select the required number of students from the Sixth Year group using simple random sampling.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "steps",
    "commandWord": {
      "word": "Calculate",
      "reminder": "Work out the value, showing your steps."
    },
    "ribbons": [
      {
        "label": "(a) One valid advantage AND one valid disadvantage of a sample vs census",
        "marks": 5,
        "kind": "explain"
      },
      {
        "label": "(b) Judgement 'not representative' with valid bias reason (non-random / excludes late-leavers)",
        "marks": 5,
        "kind": "explain"
      },
      {
        "label": "(c) Find sampling fraction 1/20 or one stratum correct",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(c) Apply fraction to all six strata, values totalling 60 (12, 11, 10, 8, 10, 9)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(d) Number the 180 students AND use random numbers to pick 9 distinct students",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The most common error in stratified sampling is rounding each stratum independently so the parts fail to sum to the required sample size (here 60). Always find the single sampling fraction (60/1200 = 1/20) and apply it to every stratum; then verify the strata add back exactly to the total sample. A second frequent loss is in part (b): students name the sampling method (\"convenience\") but do not explain WHY it causes bias — the marks are for identifying who is systematically excluded, not for the label.",
      "source": "2017 HL P2 Q1"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-4"
  },
  {
    "id": "maths-hl-0-4-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2019,
    "questionRef": "2019 HL P2 Q2",
    "questionText": "A market-research company is designing a questionnaire to investigate the eating habits of adults in a town.\n\n(a) The company plans to include the following question on its questionnaire:\n\"Don't you agree that eating too much fast food, which everyone knows is unhealthy, is a bad habit? Yes / No\"\nState one reason why this is a poorly designed survey question, and rewrite it as a suitable unbiased question.\n\n(b) One of the variables the company wishes to record is the type of data each question produces. For each of the following questions, state whether the data collected is numerical (quantitative) or categorical (qualitative), and if it is numerical, state whether it is discrete or continuous.\n (i) \"How many portions of vegetables did you eat yesterday?\"\n (ii) \"What is your favourite type of takeaway?\"\n (iii) \"How long (in minutes) did you spend preparing your evening meal yesterday?\"\n\n(c) The company will gather the data by stopping shoppers in the town's main shopping centre on a weekday morning and interviewing those willing to take part.\nState whether this is an example of primary or secondary data, and give one reason why this sampling approach may not give a representative picture of all adults in the town.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "written",
    "commandWord": {
      "word": "State",
      "reminder": "Give a brief, definite answer; no working needed."
    },
    "ribbons": [
      {
        "label": "(a) Valid reason (leading/biased wording) AND a suitable neutral rewrite with answer options",
        "marks": 6,
        "kind": "explain"
      },
      {
        "label": "(b)(i) Numerical and discrete",
        "marks": 2,
        "kind": "name"
      },
      {
        "label": "(b)(ii) Categorical",
        "marks": 2,
        "kind": "name"
      },
      {
        "label": "(b)(iii) Numerical and continuous",
        "marks": 2,
        "kind": "name"
      },
      {
        "label": "(c) Primary data AND valid reason for non-representativeness",
        "marks": 3,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "In part (b) the single most common mistake is confusing discrete and continuous numerical data. The test is whether the variable is COUNTED (whole numbers only → discrete, e.g. number of portions) or MEASURED on a scale where any value is possible (→ continuous, e.g. time in minutes, even if respondents round to whole minutes). The fact that an answer is written as a whole number does NOT make it discrete — time is continuous because, in principle, it can take any value between two points. A second frequent slip in part (a) is rewriting the question to still be closed/leading; an unbiased rewrite must remove the persuasive wording AND offer balanced, non-judgemental response options.",
      "source": "2019 HL P2 Q2"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-4"
  },
  {
    "id": "maths-ol-0-4-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2017,
    "questionRef": "2017 OL P2 Q1",
    "questionText": "Aoife is carrying out a survey about how students in her school travel to school each morning. She decides to ask the first 30 students who arrive at the school gate before 8 a.m.\n\n(a) Aoife's data is an example of primary data. Explain what is meant by primary data.\n\n(b) State whether each of the following variables is categorical or numerical:\n   (i) the colour of each student's school bag\n   (ii) the number of students living in each student's household\n   (iii) the distance, in km, each student travels to school\n   (iv) the type of transport (bus, car, walk, cycle) each student uses.\n\n(c) Aoife's sample is a biased sample. Give one reason why her method of choosing the sample may not give a fair (representative) picture of how all students in the school travel to school.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "written",
    "commandWord": {
      "word": "Explain / State / Give",
      "reminder": "Explain: give a clear meaning. State: say briefly. Give: provide one reason."
    },
    "ribbons": [
      {
        "label": "(a) Correct explanation of primary data (data collected yourself / first-hand / from the original source)",
        "marks": 3,
        "kind": "explain"
      },
      {
        "label": "(b) Correct categorical/numerical classification of all four variables (2 marks each)",
        "marks": 8,
        "kind": "name"
      },
      {
        "label": "(c) One valid reason for bias clearly stated",
        "marks": 4,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "In part (b) the most common error is calling variables like \"number of students in the household\" categorical because the values are written as words or grouped — but if the variable is a genuine count or measurement that can be added or averaged, it is numerical. Ask yourself: \"Does the value answer 'how many / how much' with a number?\" If yes, it is numerical; if it only names a group or label, it is categorical.",
      "source": "2017 OL P2 Q1"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-4"
  },
  {
    "id": "maths-ol-0-4-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2018,
    "questionRef": "2018 OL P2 Q2",
    "questionText": "A teacher recorded the number of text messages that each of 24 students sent during one school day. The results are listed below:\n\n12, 8, 15, 22, 9, 14, 18, 25, 11, 7, 16, 20, 13, 19, 24, 6, 10, 17, 21, 23, 8, 14, 12, 26\n\n(a) Copy and complete the grouped frequency table below by sorting the data into the given class intervals. Use intervals of the form 0–5, 5–10, etc., where 5–10 means \"5 or more, but less than 10\".\n   Number of texts:  0–5,  5–10,  10–15,  15–20,  20–25,  25–30\n   Frequency:        __,   __,    __,     __,     __,     __\n\n(b) State how many students sent fewer than 15 text messages.\n\n(c) Tony says: \"From this grouped frequency table, I can tell exactly how many students sent exactly 20 text messages.\" State whether Tony is correct, and give a reason for your answer.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Complete / State",
      "reminder": "Complete: fill in the table. State: say briefly (with a reason where asked)."
    },
    "ribbons": [
      {
        "label": "(a) Grouped frequency table fully correct — all six frequencies (0, 5, 7, 5, 5, 2) right and totalling 24",
        "marks": 8,
        "kind": "method"
      },
      {
        "label": "(b) Correct value 12, consistent with their table",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(c) States \"No / not correct\" with a valid reason (grouping loses individual values)",
        "marks": 3,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "The single most common mistake here is mishandling the class boundaries. With intervals written \"5–10, 10–15, …\" a value that lands on a boundary (such as 10, 15 or 20) belongs to the interval that STARTS with it, not the one that ends with it — so 15 goes into 15–20, not 10–15. Students who double-count or mis-place these boundary values get a frequency total that is not 24; always add your frequencies and check they equal the number of data values before moving on.",
      "source": "2018 OL P2 Q2"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-4"
  },
  {
    "id": "maths-hl-0-5-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2017,
    "questionRef": "2017 HL P2 Q1",
    "questionText": "A market researcher records the number of cups of coffee that each of 80 office workers drinks in a typical day. The results are shown in the frequency table below.\n\n  Number of cups (x):  0   1   2   3   4   5\n  Frequency (f):       6  14  22  18  12   8\n\n(a) (i) Calculate the mean number of cups of coffee drunk per day.\n    (ii) Find the median number of cups.\n    (iii) Write down the mode.\n\n(b) (i) Calculate the standard deviation of the data, correct to two decimal places.\n    (ii) The researcher states: \"More than half of the workers drink at least 3 cups per day.\" By referring to the data, state whether this statement is true or false, giving a reason for your answer.",
    "marks": 25,
    "minutes": 25,
    "answerKind": "steps",
    "commandWord": {
      "word": "Calculate",
      "reminder": "Work out a numerical value, showing your steps."
    },
    "ribbons": [
      {
        "label": "(a)(i) Mean: attempt at Sigma(fx) or correct method",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(a)(i) Mean = 2.5 correctly obtained",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(a)(ii) Median: cumulative frequencies or 40th/41st position",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(a)(ii) Median = 2 correctly identified",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(a)(iii) Mode = 2 (greatest frequency)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b)(i) SD: correct deviations/squares or formula with x-bar = 2.5",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b)(i) Variance = 1.95 found / sigma un-rounded",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b)(i) sigma = 1.40 (two decimal places)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(b)(ii) Computes 18+12+8 = 38 or states 'at least 3' correctly",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(b)(ii) States FALSE with valid numerical reason (38 < 40)",
        "marks": 2,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "The single most common error is mishandling \"at least 3\" in part (b)(ii). Many candidates read \"at least 3\" as \"more than 3\" and add only 12 + 8 = 20, or they confuse it with \"at most 3\". \"At least 3\" is the inclusive tail 3, 4, 5. Equally, in (b)(i) candidates routinely lose the high-partial mark by forgetting the final square root (quoting the variance 1.95 as the standard deviation) or by rounding 1.3964 to 1.39 instead of 1.40 - always carry the unrounded value to the last step and round once.",
      "source": "2017 HL P2 Q1"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-5"
  },
  {
    "id": "maths-hl-0-5-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2019,
    "questionRef": "2019 HL P2 Q2",
    "questionText": "A school principal records the time, in minutes, that each of 100 students spends travelling to school each morning. The data are grouped in the frequency table below. (Note: 10 <= t < 20 means a time of at least 10 minutes but less than 20 minutes.)\n\n  Time (minutes)      Number of students\n   0 <= t < 10               8\n  10 <= t < 20              17\n  20 <= t < 30              30\n  30 <= t < 40              25\n  40 <= t < 50              14\n  50 <= t < 60               6\n\n(a) Using the mid-interval values, calculate an estimate of the mean travel time. Give your answer correct to one decimal place.\n\n(b) Draw a cumulative frequency curve (ogive) to represent the data. Use a scale of 1 cm = 5 minutes on the horizontal axis and 1 cm = 10 students on the vertical axis.\n\n(c) Use your curve to estimate:\n    (i) the median travel time,\n    (ii) the interquartile range,\n    (iii) the number of students who spend more than 35 minutes travelling to school.\n\n(d) The school wants to identify the 10% of students with the longest travel times for a special \"early bus\" scheme. Use your curve to estimate the minimum travel time a student must have to be included in this scheme.",
    "marks": 25,
    "minutes": 25,
    "answerKind": "paper",
    "commandWord": {
      "word": "Draw",
      "reminder": "Produce an accurate diagram/graph (here, an ogive) and read values from it."
    },
    "ribbons": [
      {
        "label": "(a) Mid-interval values listed or Sigma f(mid) partly computed",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(a) Mean = 28.8 min",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(b) Correct cumulative frequencies or some points plotted",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(b) All 7 points plotted at upper boundaries (minor slip)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(b) All points at upper class boundaries joined as smooth ogive, correct scales",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c)(i) Median ~28 min read from curve",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c)(ii) One of Q1 ~20 or Q3 ~38 found",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(c)(ii) IQR ~18 min from Q3 - Q1",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(c)(iii) cf at t = 35 read (~68), 100 - 68 ~32 students",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(d) Longest 10%: cf = 90 (90th percentile) gives ~47 min",
        "marks": 2,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The classic ogive errors are (1) plotting the cumulative frequencies at the mid-interval value instead of the UPPER class boundary - the cf for \"30 <= t < 40\" is the number of students with time less than 40, so it must be plotted at t = 40, not 35; and (2) in part (d), confusing \"the 10% with the LONGEST times\" with the 10th percentile. The longest-10% threshold is the 90th percentile (cf = 90), read by going up from cf = 90 - not cf = 10. Candidates who go to cf = 10 answer the opposite question and lose all the marks despite a perfect curve.",
      "source": "2019 HL P2 Q2"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-5"
  },
  {
    "id": "maths-ol-0-5-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2017,
    "questionRef": "2017 OL P2 Q1",
    "questionText": "A teacher recorded the number of text messages that each of 20 students sent during one school day. The data are listed below.\n\n12, 8, 25, 31, 19, 7, 22, 14, 33, 28, 16, 9, 21, 5, 27, 18, 30, 11, 24, 17\n\n(a) Using the data above, complete an ordered stem-and-leaf plot on paper. Use the tens digit as the stem. Include a key.\n\n(b) Write down the mode of the data, or state if there is no mode. Give a reason for your answer.\n\n(c) Find the median number of text messages sent.\n\n(d) Find the range of the data.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "paper",
    "commandWord": {
      "word": "Find",
      "reminder": "Work out the value, showing your steps."
    },
    "ribbons": [
      {
        "label": "(a) Attempt: stem-and-leaf structure started with correct stems (0,1,2,3) and some leaves placed",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(a) Partial: plot essentially correct but unordered leaves, a leaf or two misplaced/omitted, or key missing",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(a) Full: all 20 leaves correctly placed, ordered within each row, and correct key shown",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Partial: states 'no mode' with no/weak reason",
        "marks": 1,
        "kind": "attempt"
      },
      {
        "label": "(b) Full: 'no mode' with valid reason (no value repeats / all values distinct)",
        "marks": 2,
        "kind": "explain"
      },
      {
        "label": "(c) Attempt: identifies need for 10th and 11th values, or selects a single middle value",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(c) Partial: middle values 18 and 19 identified but not averaged, or arithmetic slip",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(c) Full: median = 18.5 correctly stated",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(d) Partial: correct subtraction set up (33 - 5) or one correct extreme identified",
        "marks": 1,
        "kind": "attempt"
      },
      {
        "label": "(d) Full: range = 28",
        "marks": 2,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The single most common error here is on the median. Students frequently forget that with an even number of data values (n = 20) the median lies between two values and must be averaged - they wrongly pick a single 'middle' leaf off the diagram (often the 10th value, 18) and report it as the median. A close second is leaving the leaves unordered in the stem-and-leaf plot: the command word 'ordered' requires the leaves in each row to be sorted, and unordered leaves lose marks even when all the data is present.",
      "source": "2017 OL P2 Q1 examiner report"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-5"
  },
  {
    "id": "maths-ol-0-5-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2018,
    "questionRef": "2018 OL P2 Q4",
    "questionText": "The table below shows the times, in minutes, that 50 customers spent in a particular shop. The times are grouped into class intervals. (Note: a - b means a or more but less than b.)\n\n| Time (minutes) | 0 - 5 | 5 - 10 | 10 - 15 | 15 - 20 | 20 - 25 |\n|----------------|-------|--------|---------|---------|---------|\n| Number of customers | 6 | 14 | 18 | 8 | 4 |\n\n(a) Draw a histogram to represent the data above. (The class intervals are of equal width, so the height of each bar is the frequency.)\n\n(b) Write down the modal class interval.\n\n(c) Using the mid-interval values, calculate the mean time, in minutes, that a customer spent in the shop. Give your answer correct to one decimal place.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "paper",
    "commandWord": {
      "word": "Draw",
      "reminder": "Produce an accurate diagram/graph using the data, with labelled axes."
    },
    "ribbons": [
      {
        "label": "(a) Attempt: axes drawn with a sensible/labelled scale, or at least one bar at correct height",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(a) Partial: most bars (3 or 4) at correct heights, or all five bars correct but with gaps / axes unlabelled",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(a) Full: all five bars at correct heights (6, 14, 18, 8, 4), equal widths, no gaps, axes labelled with uniform scale",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(b) Partial: states frequency 18, or names a wrong interval showing some understanding (e.g. mid-value 12.5 only)",
        "marks": 1,
        "kind": "attempt"
      },
      {
        "label": "(b) Full: modal class interval = 10 - 15",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(c) Attempt: at least two correct mid-interval values found, or correct method (Sigma fx / Sigma f) indicated",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(c) Low partial: all mid-interval values correct and at least three f x x products correct",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(c) High partial: correct Sigma fx = 575 obtained but not divided, or divided with an arithmetic slip",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(c) Full: mean = 11.5 minutes",
        "marks": 1,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The most common mistake in part (c) is using the wrong x-values: weaker students multiply the frequency by the class width, by the lower boundary (0, 5, 10, 15, 20) or by the upper boundary instead of the mid-interval value - all of which give a wrong mean. They must use the midpoint of each interval (2.5, 7.5, 12.5, 17.5, 22.5). A frequent histogram error in part (a) is leaving gaps between the bars: because the data is continuous (grouped intervals), the bars must touch - a histogram is not a bar chart.",
      "source": "2018 OL P2 Q4 examiner report"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-5"
  },
  {
    "id": "maths-hl-0-6-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2018,
    "questionRef": "2018 HL P2 Q5",
    "questionText": "The lengths of time, in minutes, that a large number of students spend studying each evening are normally distributed with a mean of 95 minutes and a standard deviation of 18 minutes.\n\n(a) Using the Empirical Rule (the 68-95-99.7% rule), estimate the percentage of students who spend between 59 minutes and 131 minutes studying each evening.\n\n(b) Niamh spends 122 minutes studying. Calculate Niamh's standard score (z-score), correct to two decimal places, and state, with a reason, whether her study time would be regarded as unusually high.\n\n(c) On a particular evening, 2000 students study. Using the Empirical Rule, estimate how many of these students spend more than 113 minutes studying. Give your answer correct to the nearest whole number.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Calculate",
      "reminder": "Work out the value, showing your steps (here the z-score, plus estimates for parts a and c)."
    },
    "ribbons": [
      {
        "label": "(a) Recognises interval is mu +/- 2sigma (59 = mu - 2sigma, 131 = mu + 2sigma)",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(a) States 95%",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(b) Correct z-score z = (122 - 95)/18 = 1.50",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(b) Valid reasoning that |z| < 2 so not unusual",
        "marks": 3,
        "kind": "explain"
      },
      {
        "label": "(c) Identifies 113 = mu + 1sigma and that 16% lies above",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(c) Correct final answer 320 students",
        "marks": 2,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The single most common error is halving incorrectly in tail problems. Students correctly recall that 68% lies within mu +/- 1sigma, but then forget that the leftover 32% must be SPLIT between BOTH tails - they write 32% instead of 16%, giving 640 instead of 320. Always sketch the bell curve and shade the one tail you actually want before converting to a number.",
      "source": "2018 HL P2 Q5"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-6"
  },
  {
    "id": "maths-hl-0-6-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2017,
    "questionRef": "2017 HL P2 Q4",
    "questionText": "A coffee shop owner records the maximum daily temperature (C) and the number of hot coffees sold on eight randomly chosen days. The data are shown below.\n\nTemperature (C):   4    6    9   11   14   17   20   23\nHot coffees sold:  142  138  120  118  101   95   74   66\n\n(a) Describe the relationship between the maximum daily temperature and the number of hot coffees sold, referring to both the direction and the strength of the relationship.\n\n(b) The correlation coefficient for this data is r = -0.99 (correct to two decimal places). Explain what this value tells you about the relationship between the two variables.\n\n(c) The equation of the line of best fit for this data is\n        y = 160.4 - 4.07x,\nwhere x is the maximum daily temperature (C) and y is the number of hot coffees sold.\n   (i) Use the line of best fit to estimate the number of hot coffees sold on a day when the maximum temperature is 12 C. Give your answer correct to the nearest whole number.\n   (ii) Explain why it would not be reliable to use this equation to estimate the number of hot coffees sold on a day when the maximum temperature is 35 C.\n\n(d) The owner says: \"This data proves that lower temperatures cause people to buy more hot coffees.\" Comment on this statement.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "steps",
    "commandWord": {
      "word": "Describe",
      "reminder": "Give an account of the relationship in words - here naming both its direction and strength."
    },
    "ribbons": [
      {
        "label": "(a) States direction (negative) AND strength (strong), with reference to the data",
        "marks": 5,
        "kind": "explain"
      },
      {
        "label": "(b) Interprets r = -0.99 correctly (very strong AND negative, near -1)",
        "marks": 5,
        "kind": "explain"
      },
      {
        "label": "(c)(i) Correct substitution and arithmetic giving 112",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(c)(ii) Identifies extrapolation / outside range of data as the reason",
        "marks": 3,
        "kind": "explain"
      },
      {
        "label": "(d) States correlation does not imply causation with a valid justification",
        "marks": 2,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "The most common loss of marks is at part (d): students who have just calculated a strong correlation instinctively treat it as proof of cause and effect. The examiner specifically rewards the phrase \"correlation does not imply causation\" backed by a plausible alternative explanation or confounding variable. A close second is part (c)(ii): many students say 35 C \"gives a silly answer\" rather than naming the real statistical reason - extrapolation beyond the range of the data - which is the point being tested.",
      "source": "2017 HL P2 Q4"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-6"
  },
  {
    "id": "maths-ol-0-6-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2017,
    "questionRef": "2017 OL P2 Q4",
    "questionText": "A teacher recorded the number of days each of 15 students in a class was absent during one school term. The data are shown below:\n\n0, 1, 1, 2, 2, 2, 3, 3, 4, 4, 5, 6, 7, 8, 12\n\n(a) Find the mode of this data.\n(b) Find the median number of days absent.\n(c) Calculate the mean number of days absent. Give your answer correct to one decimal place.\n(d) The teacher claims that \"the average student in this class was absent for more than 4 days.\" State whether you agree with the teacher. Give a reason for your answer, referring to your results above.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find / Calculate / State",
      "reminder": "Work out each statistic from the data and shown working; for the claim, state a position and justify it with your results."
    },
    "ribbons": [
      {
        "label": "(a) Mode: correct mode stated (2 days)",
        "marks": 4,
        "kind": "attempt"
      },
      {
        "label": "(b) Median: identify middle (8th) value, correct median (3 days)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(c) Mean — find the sum: correct total of 60 (clear correct addition)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(c) Mean — final value: divide sum by 15, give 4.0 to one decimal place",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(d) Inference: state do not agree with a valid reason linked to mean/median/outlier",
        "marks": 4,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "The most common mistake is on part (b)/(d). Students frequently forget to order the data before reading off the median (here it is already ordered, but in many versions it is not), and in the inference part they answer \"yes/no\" with no statistical reason — SEC awards the high partial credit ONLY when the conclusion is explicitly justified by the calculated values. Also watch the mean: the single large value (12) is an outlier that drags the mean up to 4.0, so quoting the mean alone misrepresents the \"typical\" student — examiners reward candidates who notice the skewing effect of the outlier.",
      "source": "2017 OL P2 Q4 examiner commentary"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-6"
  },
  {
    "id": "maths-ol-0-6-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2018,
    "questionRef": "2018 OL P2 Q5",
    "questionText": "The back-to-back stem-and-leaf plot below shows the resting heart rate (in beats per minute) of a group of athletes and a group of non-athletes.\n\n                Athletes | Stem | Non-athletes\n            9  8  6  5  4 |  4   |\n                  3  2  1 |  5   |  8  9\n                       0  |  6   |  2  4  5  7  8\n                          |  7   |  1  3  3  6\n                          |  8   |  0  2\n\nKey: For Athletes, 5 | 4 means 45 beats per minute. For Non-athletes, 5 | 8 means 58 beats per minute.\n\n(a) How many athletes are in the group?\n(b) Write down the lowest resting heart rate recorded among the non-athletes.\n(c) Find the median resting heart rate of the athletes.\n(d) Find the range of the resting heart rates of the non-athletes.\n(e) Based on the data, which group tends to have lower resting heart rates? Give a reason for your answer.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "steps",
    "commandWord": {
      "word": "How many / Write down / Find / Give a reason",
      "reminder": "Read values from the plot, work out each statistic with shown working, and for (e) name the group and back it with a statistic (median or range)."
    },
    "ribbons": [
      {
        "label": "(a) Count: correct number of athletes (9)",
        "marks": 4,
        "kind": "attempt"
      },
      {
        "label": "(b) Lowest value: correct lowest non-athlete value (58)",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(c) Median: list/order athlete data, identify 5th value, correct median (49)",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(d) Range: highest − lowest (82 − 58) correct range (24)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(e) Comparison: identify athletes with a valid data-based reason (median/spread)",
        "marks": 4,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "The classic error on a back-to-back stem-and-leaf plot is misreading the left-hand (athletes') side: the leaves are written right-to-left (largest nearest the edge, smallest nearest the stem), so students must read carefully and re-order before finding the median — many take the leaves in printed order and pick the wrong middle value. In part (e), a bare \"athletes\" earns only half marks; SEC requires the comparison to be backed by a statistic (median or range) or a clear statement about where each group's data are clustered.",
      "source": "2018 OL P2 Q5 examiner commentary"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-6"
  },
  {
    "id": "maths-hl-1-0-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2017,
    "questionRef": "2017 HL P2 Q4(a)",
    "questionText": "In the triangle ABC, the point D lies on the side BC. The line segment AD is drawn so that |AB| = |AD|. The angle ABD = 50°, and the angle DAC = 35°.\n\n(a) Find the measure of the angle ADB. Give a reason for your answer.\n\n(b) Hence, find the measure of the angle BAD.\n\n(c) Find the measure of the angle ACD, the angle at C in the triangle ABC. Show your reasoning.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Work out the value; here also give a reason / show your reasoning to justify each step."
    },
    "ribbons": [
      {
        "label": "(a) Identifies isosceles triangle ABD and states angle ADB = 50° with valid reason (angles opposite equal sides are equal)",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(b) Uses angle sum of triangle ABD = 180° to get angle BAD = 80°",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(c) Uses straight angle at D (angle ADC = 130°) and angle sum of triangle ADC to get angle ACD = 15°",
        "marks": 5,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The single most common error is pairing the wrong angle with the wrong side in the isosceles step — students see |AB| = |AD| and wrongly conclude angle ABD = angle BAD (the two angles \"at the equal sides\") instead of the angles OPPOSITE those sides. The equal sides are AB and AD; the equal base angles are the ones at B and at D (angle ABD and angle ADB), NOT the apex angle BAD. Always identify which angle sits OPPOSITE each equal side before declaring two angles equal, and quote the theorem (\"angles opposite the equal sides are equal\") to earn the reason mark.",
      "source": "2017 HL P2 Q4(a)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-0"
  },
  {
    "id": "maths-hl-1-0-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2016,
    "questionRef": "2016 HL P2 Q5(b)",
    "questionText": "The points A, B, C and D lie on a circle with centre O. The chord BD is a diameter of the circle, so B, O and D are collinear. The angle DBC = 28° and the angle ADB = 41°, where these are the angles of the triangles inscribed in the circle.\n\n(a) Write down the measure of the angle BAD and the measure of the angle BCD. In each case give a reason.\n\n(b) Find the measure of the angle BDC.\n\n(c) The angle ABD is subtended by the same arc AD as one other angle marked in the figure. Find the measure of the angle ABD, and name the angle equal to it, giving a reason.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Work out the value (also \"write down\" where stated); give a reason to justify each result."
    },
    "ribbons": [
      {
        "label": "(a) Both angle BAD = 90° and angle BCD = 90°, each justified by \"angle in a semicircle\"",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(b) Angle sum of triangle BCD to obtain angle BDC = 62°",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(c) Angle sum of triangle ABD to obtain angle ABD = 49°",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(c) Names angle ACD as equal to angle ABD with reason \"same arc / same segment\"",
        "marks": 5,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "The most common mistake is misapplying the \"angle in a semicircle\" theorem — students must check that the angle actually STANDS ON THE DIAMETER (its two arms pass through the two endpoints of the diameter, here B and D), not on some other chord. A vertex on the circle does not automatically give 90°; only the angle subtended by the diameter does. The second frequent slip in part (c) is confusing \"same arc\" (angles equal) with the central-angle theorem (angle at centre = twice angle at circumference) when no central angle is involved — name the precise theorem that matches the configuration.",
      "source": "2016 HL P2 Q5(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-0"
  },
  {
    "id": "maths-ol-1-0-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2017,
    "questionRef": "2017 OL P2 Q4",
    "questionText": "In a triangle the three angles are: angle A = 3x, angle B = 2x and angle C = (x + 30)°.\n(a) Using the fact that the angles of a triangle add up to 180°, write an equation in x and solve it.\n(b) Hence find the size of each of the angles A, B and C.\n(c) Explain what is meant by a scalene triangle.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Solve / Find / Explain",
      "reminder": "Form and solve the equation showing your steps, work out each angle, then state the meaning of the term."
    },
    "ribbons": [
      {
        "label": "Writes any relevant angle-sum statement, e.g. uses 180° or adds the three expressions",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "Correct equation 6x + 30 = 180 solved to x = 25",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "One or two angles correctly evaluated",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "All three angles correct (75°, 50°, 55°) with sum = 180°",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Correct explanation: all three sides different lengths",
        "marks": 3,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "The most common error is forgetting the constant term when collecting like terms — students write 6x = 180 (dropping the +30), giving x = 30 and angles that do not sum to 180°. Always combine the variable terms and the constants separately, then sanity-check by confirming your three final angles add to exactly 180°.",
      "source": "2017 OL P2 Q4"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-0"
  },
  {
    "id": "maths-ol-1-0-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2016,
    "questionRef": "2016 OL P2 Q5",
    "questionText": "A circle has centre O. A and B are two points on the circle, so that [AB] is a chord. The point T lies on the circle. The angle AOB (the angle at the centre, standing on the arc AB on the same side as T) is 110°.\n(a) Find the size of the angle ATB (the angle at the point T on the circle, standing on the same arc AB). Give a reason for your answer.\n(b) The point C also lies on the circle, on the same arc as T. Write down the size of the angle ACB, and give a reason for your answer.\n(c) D is a point on the circle on the opposite arc, so that ATBD is a cyclic quadrilateral. Find the size of the angle ADB. Give a reason for your answer.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "written",
    "commandWord": {
      "word": "Find / Write down / Give a reason",
      "reminder": "Work out each angle and justify it by naming the relevant circle theorem."
    },
    "ribbons": [
      {
        "label": "Uses the centre/circumference relationship (e.g. writes 110 ÷ 2 or 2 × angle)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Angle ATB = 55° with correct reason (angle at centre is twice angle at circumference)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Angle ACB = 55° with correct reason (angles in the same segment are equal)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Uses 180° for opposite angles of cyclic quadrilateral (e.g. writes 180 − 55)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Angle ADB = 125° with correct reason (opposite angles of cyclic quadrilateral sum to 180°)",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The classic mistake is confusing the two circle theorems — students either halve when they should leave the angle equal (part b) or treat the same-segment angles as supplementary. Anchor each step to the arc the angle \"stands on\": same arc + at the centre vs at the circumference means halve; same arc + both at the circumference means equal; opposite vertices of a cyclic quadrilateral means add to 180°.",
      "source": "2016 OL P2 Q5"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-0"
  },
  {
    "id": "maths-hl-1-1-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2019,
    "questionRef": "2019 HL P2 Q4",
    "questionText": "A circle c has equation x² + y² − 6x + 4y − 12 = 0.\n(a) Write down the coordinates of the centre and the length of the radius of c.\n(b) Show that the point T(7, 1) lies on the circle c.\n(c) Find the equation of the tangent to c at the point T(7, 1), giving your answer in the form ax + by + c = 0 where a, b, c ∈ ℤ.\n(d) The line l: 3x − 4y + 8 = 0 touches the circle. Verify that l is a tangent to c by showing that the perpendicular distance from the centre of c to l equals the radius.",
    "marks": 25,
    "minutes": 25,
    "answerKind": "steps",
    "commandWord": {
      "word": "Verify",
      "reminder": "Confirm a given result is true by carrying out the calculation/check and stating the conclusion."
    },
    "ribbons": [
      {
        "label": "(a) Correct g, f read off (g = −3, f = 2) or completing-the-square setup",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(a) Centre (3, −2) and radius 5",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Substitutes T(7, 1) into the circle equation",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(b) Shows LHS = 0 and concludes T lies on c",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Correct slope of radius (3/4)",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(c) Correct tangent slope (−4/3) and uses T",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(c) Tangent 4x + 3y − 31 = 0 in required integer form",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(d) Perpendicular-distance formula with centre and line substituted",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(d) d = 5 shown to equal radius, with conclusion \"tangent\"",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "In part (c) the most common mistake is to forget the tangent–radius perpendicularity and instead use the radius slope (3/4) itself for the tangent, or to take only the negative (−3/4) rather than the negative reciprocal (−4/3). In part (d), students frequently drop the modulus (absolute value) in the distance formula and get a negative \"distance,\" or mis-square the denominator (using 3² + 4² = 25, so √25 = 5 — getting this denominator wrong is the usual slip). Always evaluate |centre substituted| and divide by √(a² + b²).",
      "source": "2019 HL P2 Q4"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-1"
  },
  {
    "id": "maths-ol-1-1-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2017,
    "questionRef": "2017 OL P2 Q1",
    "questionText": "The line l has equation 2x - 3y + 6 = 0.\n(a) Find the slope of l.\n(b) The line k passes through the point (3, 1) and is perpendicular to l. Find the equation of k.\n(c) Verify that the point (1, 4) lies on the line k.",
    "marks": 25,
    "minutes": 25,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find / Verify",
      "reminder": "Find: work out the value or equation showing your steps. Verify: substitute and show the statement is true."
    },
    "ribbons": [
      {
        "label": "(a) Attempt to rearrange to y = mx + c or use -a/b (e.g. -3y = -2x - 6)",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(a) Slope of l = 2/3 correctly stated",
        "marks": 7,
        "kind": "method"
      },
      {
        "label": "(b) Find perpendicular slope -3/2 correctly",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(b) Substitute point and slope into line formula to reach 3x + 2y - 11 = 0",
        "marks": 6,
        "kind": "method"
      },
      {
        "label": "(c) Substitute x = 1, y = 4 into k",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(c) Evaluate to 0 and conclude the point lies on k",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The most common mistake is mishandling the slope when rearranging. Students frequently divide -3y = -2x - 6 by -3 but forget to change the sign of every term, getting slope -2/3 instead of +2/3, or they read the slope straight off \"2x - 3y + 6\" as 2 (the x-coefficient) without isolating y. Always fully isolate y first, then the coefficient of x is the slope. A second frequent slip is using the same slope for k instead of the negative reciprocal - remember perpendicular means \"flip and change sign,\" and check by confirming m1 x m2 = -1.",
      "source": "2017 OL P2 Q1"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-1"
  },
  {
    "id": "maths-ol-1-1-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2016,
    "questionRef": "2016 OL P2 Q2",
    "questionText": "A(-2, 1) and B(4, 9) are two points.\n(a) Find the coordinates of the midpoint of [AB].\n(b) Find |AB|, the length of the line segment [AB]. Give your answer in the form a√b, where a, b ∈ ℕ.\n(c) The point C has coordinates (4, 1). Find the area of the triangle ABC.",
    "marks": 25,
    "minutes": 25,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Work out the value showing the formula and your substitution steps."
    },
    "ribbons": [
      {
        "label": "(a) Correct midpoint formula with at least one coordinate-pair substituted",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(a) Midpoint (1, 5) correct",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(b) Correct distance formula with values substituted",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Reaches √(36 + 64) or √100",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) |AB| = 10",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Correct area formula with the two translated points (or any valid method set up)",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(c) Area = 24 square units",
        "marks": 5,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "In part (c) the most common error is forgetting to translate one vertex to the origin before using Area = 1/2|x1y2 - x2y1|. That formula only works when one vertex is at (0, 0); students who plug in the raw coordinates A(-2,1), B(4,9), C(4,1) directly get a wrong answer. Always subtract one chosen vertex's coordinates from the other two first. A reliable check is the base x height method whenever two of the points share an x- or y-coordinate.",
      "source": "2016 OL P2 Q2"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-1"
  },
  {
    "id": "maths-hl-1-2-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2017,
    "questionRef": "2017 HL P2 Q4",
    "questionText": "The triangle ABC has |AC| = 7.2 cm and |AB| = 9.6 cm. The angle BAC = 68°.\n(a) Find |BC|, the length of the third side of the triangle. Give your answer correct to one decimal place.\n(b) Find the area of the triangle ABC, correct to one decimal place.\n(c) Hence, or otherwise, find the measure of the angle ABC, correct to the nearest degree.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Work out the value using a valid method and show your steps."
    },
    "ribbons": [
      {
        "label": "(a) Correct substitution into cosine rule a² = b² + c² − 2bc·cos A",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(a) Correct evaluation and answer 9.6 cm (1 dp)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(b) Correct area formula ½bc·sin A with substitution and answer 32.0 cm²",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(c) Correct sine-rule set-up sin B/b = sin A/a with values",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Correct evaluation and angle ≈ 44°",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The most common error is rounding |BC| to 9.6 in part (a) and then re-using that rounded value in the part (c) sine rule, which can push the angle to the wrong whole degree. Always carry the unrounded value (9.6028…) in your calculator memory for later parts and only round at the very end. A second frequent slip is mismatching which angle is opposite which side when substituting into the sine rule.",
      "source": "Trigonometry — non-right-angled triangles (cosine rule, area, sine rule)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-2"
  },
  {
    "id": "maths-hl-1-2-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2019,
    "questionRef": "2019 HL P2 Q5",
    "questionText": "Solve the equation 2 cos²x + sin x = 1, where 0° ≤ x ≤ 360°.\nGive all solutions in degrees.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "steps",
    "commandWord": {
      "word": "Solve",
      "reminder": "Find all values of the unknown that satisfy the equation, within the stated range."
    },
    "ribbons": [
      {
        "label": "Correct use of identity cos²x = 1 − sin²x to obtain a quadratic in sin x",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Correct quadratic 2 sin²x − sin x − 1 = 0 and valid method to solve (factor or formula)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Correct values sin x = 1 and sin x = −½",
        "marks": 1,
        "kind": "method"
      },
      {
        "label": "All correct angles in range: 90°, 210°, 330°",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The classic mistake is finding only one solution for sin x = −½ (typically 210°) and forgetting the second quadrant where sine takes the same sign — here the fourth-quadrant value 330°. Always identify which two quadrants give the correct sign, then state both. A secondary error is taking the square root of cos²x prematurely (introducing ±cos x) instead of substituting the identity to form a single quadratic in sin x.",
      "source": "Trigonometry — identities and solving trig equations over an interval"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-2"
  },
  {
    "id": "maths-ol-1-2-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2017,
    "questionRef": "2017 OL P2 Q4",
    "questionText": "A vertical flagpole [AB] stands on level horizontal ground. A is the top of the pole and B is the base. A point C is on the level ground, in a straight line out from the base B, at a distance of 24 m from B. From C, the angle of elevation of the top of the pole, A, is 35°.\n\n(a) Draw a rough sketch of the right-angled triangle ABC, showing clearly the right angle at B, the angle of elevation of 35° at C, and the distance |BC| = 24 m.\n\n(b) Find the height of the flagpole, |AB|. Give your answer correct to one decimal place.\n\n(c) Find the length of [AC], the straight-line distance from C to the top of the pole, A. Give your answer correct to one decimal place.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Draw / Find",
      "reminder": "Draw = produce a clear labelled sketch; Find = work out the value, showing the trig method and rounding as asked."
    },
    "ribbons": [
      {
        "label": "Correct labelled right-angled sketch (right angle at B, 35° at C, 24 m on BC)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Correct trig ratio chosen with 35° and 24, e.g. tan 35° = AB/24",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(b) Correctly solves to |AB| ≈ 16.8 m",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(c) Correct method for the hypotenuse, e.g. cos 35° = 24/AC or Pythagoras with found AB",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(c) Correctly obtains |AC| ≈ 29.3 m",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The single most common error is choosing the wrong trig ratio because students don't first label which side is opposite, adjacent and hypotenuse relative to the given angle. Here BC = 24 is adjacent (not opposite) to 35°, so the height uses tan (opp/adj), not sin. A close second is mode error: the calculator must be in DEGREES, not radians — always confirm 'DEG' is showing before computing tan 35°.",
      "source": "2017 OL P2 Q4"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-2"
  },
  {
    "id": "maths-ol-1-2-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2016,
    "questionRef": "2016 OL P2 Q5",
    "questionText": "In triangle PQR, |PQ| = 9 cm, |QR| = 13 cm, and the angle PQR (the angle at Q, between sides PQ and QR) is 110°. (This is NOT a right-angled triangle.)\n\n(a) Find the area of triangle PQR. Give your answer correct to one decimal place.\n\n(b) Find |PR|, the length of the third side. Give your answer correct to one decimal place.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Find = work out the value, showing the area-formula / cosine-rule substitution and rounding as asked."
    },
    "ribbons": [
      {
        "label": "(a) Substitutes correctly into Area = ½ab sin C with 9, 13 and 110°",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(a) Evaluates to Area ≈ 55.0 cm²",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(b) Correct cosine-rule statement and substitution, e.g. PR² = 81 + 169 − 234 cos 110°",
        "marks": 4,
        "kind": "attempt"
      },
      {
        "label": "(b) Handles the negative cosine correctly to reach |PR|² ≈ 330.03",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(b) |PR| ≈ 18.2 cm",
        "marks": 2,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The single most common — and most heavily penalised — error in cosine-rule questions with an obtuse angle is dropping the minus sign on cos 110°. Because cos(110°) is negative, the term −2ab·cos C becomes a PLUS, so the side comes out LONGER than the given sides. Students who treat cos 110° as positive get |PR|² = 250 − 80 = 170 and a wrong answer of about 13.0 cm, which is impossible since PR must be the longest side (it faces the obtuse angle). Always keep the calculator's sign, and sanity-check that the side opposite the biggest angle is the longest side.",
      "source": "2016 OL P2 Q5"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-2"
  },
  {
    "id": "maths-hl-1-3-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2017,
    "questionRef": "2017 HL P2 Q4 (representative)",
    "questionText": "The triangle T has vertices A(2, 1), B(6, 1) and C(4, 4). T is mapped onto the triangle T' under an enlargement with centre O(0, 0) and scale factor k = 2.\n(a) Find the co-ordinates of the images A', B' and C' of the points A, B and C respectively under this enlargement.\n(b) Find the area of the triangle T.\n(c) Hence, or otherwise, find the area of the triangle T'.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Work out and state the value(s); show your working."
    },
    "ribbons": [
      {
        "label": "(a) Attempt: multiply a coordinate by 2 / one correct image point",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(a) All three images A'(4, 2), B'(12, 2), C'(8, 8) correct",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Attempt: correct method stated (½·base·height or area formula with values)",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(b) Area of T = 6 square units",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Attempt: uses k² or multiplies area by a scale factor",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(c) Area of T' = 24 square units (via k² relationship or direct)",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The single most common error in part (c) is scaling the area by k instead of k² — students multiply 6 by 2 to get 12 rather than by 2² = 4 to get 24. Lengths scale by k, but areas scale by k². Whenever you enlarge, ask \"lengths or area?\" — area always carries the squared factor.",
      "source": "Enlargements: lengths scale by k, areas scale by k²"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-3"
  },
  {
    "id": "maths-ol-1-3-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2017,
    "questionRef": "2017 OL P2 Q6 (representative)",
    "questionText": "A photograph is enlarged. The original photograph is a rectangle measuring 6 cm by 4 cm. After the enlargement, the longer side of the photograph measures 15 cm.\n\n(a) Find the scale factor of the enlargement.\n\n(b) Find the length of the shorter side of the enlarged photograph.\n\n(c) The area of the original photograph is 24 cm². Find the area of the enlarged photograph.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Work it out and give the result (show your working)."
    },
    "ribbons": [
      {
        "label": "(a) Attempt: writes a ratio of corresponding sides, e.g. 15/6, or any relevant division",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(a) Full: k = 2.5 (or 5/2)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Attempt: identifies 4 as the side to be scaled, or multiplies a side by their k",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(b) Full: 10 cm (follow-through on their k)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Attempt: any use of k or k², or 15 × 10, or 24 × k",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(c) Full: 150 cm² (area scales by k² = 6.25)",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The single most common error in part (c) is multiplying the original area by the scale factor k instead of k². Lengths scale by k, but areas scale by k² (and volumes by k³). Students who write 24 × 2.5 = 60 lose the high partial credit. Drill the rule: \"length × k, area × k², volume × k³.\"",
      "source": "2017 OL P2 Q6 (representative)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-3"
  },
  {
    "id": "maths-ol-1-3-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2019,
    "questionRef": "2019 OL P2 Q4 (representative)",
    "questionText": "The triangle T has vertices A(2, 1), B(4, 1) and C(2, 4). An enlargement with centre of enlargement at the origin O(0, 0) and scale factor 2 maps triangle T onto triangle T′.\n\n(a) Find the co-ordinates of the images A′, B′ and C′ of the three vertices A, B and C under this enlargement.\n\n(b) On graph paper, plot triangle T and its image triangle T′, and clearly label all six vertices.\n\n(c) The area of triangle T is 3 square units. Using the scale factor, find the area of triangle T′.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "paper",
    "commandWord": {
      "word": "Find / Plot",
      "reminder": "Find: work out the result. Plot: mark the points accurately on the graph and label them."
    },
    "ribbons": [
      {
        "label": "(a) Attempt: multiplies at least one coordinate by 2, or states rule (x, y) → (2x, 2y)",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(a) Partial: two of three image points correct (or all three with one slip)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(a) Full: all three correct — A′(4, 2), B′(8, 2), C′(4, 8)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Attempt: plots triangle T correctly, or plots at least two image points",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(b) Full: both triangles plotted correctly with all six vertices labelled (follow-through)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Attempt: any use of scale factor — e.g. 3 × 2, or k², or recomputing from coordinates",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(c) Full: 12 square units (area scales by k² = 4)",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "Two classic errors here. First, in part (a) students forget the centre matters: the rule (x, y) → (kx, ky) is only valid when the centre of enlargement is the origin — many wrongly apply it for an arbitrary centre. Second, in part (c) they again scale the area by k instead of k², giving 6 instead of 12. Emphasise that for a centre-at-origin enlargement you simply multiply each coordinate by k, but area always scales by k².",
      "source": "2019 OL P2 Q4 (representative)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-3"
  },
  {
    "id": "maths-hl-3-0-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2017,
    "questionRef": "2017 HL P1 Q2(a)",
    "questionText": "Write the expression below as a single fraction in its simplest form.\n\n3/(x − 2) + 2/(x + 1) − 1",
    "marks": 10,
    "minutes": 10,
    "answerKind": "steps",
    "commandWord": {
      "word": "Write",
      "reminder": "Express the result in the stated form — here as one combined fraction, fully simplified."
    },
    "ribbons": [
      {
        "label": "Identify common denominator (x − 2)(x + 1), or rewrite at least one term over it",
        "marks": 4,
        "kind": "attempt"
      },
      {
        "label": "All three terms placed over the common denominator and numerator multiplications attempted",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Fully correct single fraction (−x² + 6x + 1)/[(x − 2)(x + 1)]",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The single most common error is sign mishandling when subtracting the product (x − 2)(x + 1). Candidates expand it correctly to x² − x − 2 but then fail to distribute the leading minus to every term, writing \"− x² − x − 2\" instead of \"− x² + x + 2.\" Always bracket the expanded product first, then change every sign, before collecting like terms.",
      "source": "2017 HL P1 Q2(a)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-0"
  },
  {
    "id": "maths-hl-3-0-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2019,
    "questionRef": "2019 HL P1 Q4",
    "questionText": "The expression 2x² − 12x + 23 can be written in the form a(x − h)² + k, where a, h and k are constants.\n\n(a) Find the value of a, the value of h and the value of k.\n\n(b) Hence, or otherwise, write down the minimum value of the expression 2x² − 12x + 23 and the value of x at which this minimum occurs.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Determine the values by completing the square; then write down the minimum and where it occurs."
    },
    "ribbons": [
      {
        "label": "(a) Factor a = 2 from the x-terms: 2(x² − 6x) + 23",
        "marks": 4,
        "kind": "attempt"
      },
      {
        "label": "(a) Complete the square inside the bracket: (x − 3)² − 9",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(a) Fully correct: a = 2, h = 3, k = 5",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Correct method shown (minimum when squared term is zero / at x = h), or one of the two answers correct",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(b) Minimum value = 5 AND x = 3 both stated",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The most frequent mistake is mishandling the factored coefficient when completing the square. After writing 2(x² − 6x), candidates correctly get (x − 3)² − 9 inside the bracket but forget to multiply the −9 by the 2 outside, giving k = 23 − 9 = 14 instead of 23 − 18 = 5. The −9 lives inside the bracket that is multiplied by a, so it must be doubled before combining with the +23.",
      "source": "2019 HL P1 Q4"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-0"
  },
  {
    "id": "maths-ol-3-0-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2017,
    "questionRef": "2017 OL P1 Q1",
    "questionText": "Simplify each of the following.\n(a) 5(2x + 3) − 3(x − 4)\n(b) (4a + 7) + (2a − 9)\n(c) Multiply out and simplify (x + 6)(x − 2).",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Simplify",
      "reminder": "Multiply out brackets and collect like terms to leave the expression in its tidiest form."
    },
    "ribbons": [
      {
        "label": "(a) Attempt: multiplies out at least one bracket correctly",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(a) Full: correct answer 7x + 27",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Attempt: removes brackets / writes 4a + 7 + 2a − 9",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(b) Full: correct answer 6a − 2",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Attempt: at least two of the four products correct",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(c) Full: correct answer x² + 4x − 12",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The single most common error is mishandling the sign in front of a bracket. In part (a), −3(x − 4) must give −3x + 12, not −3x − 12 — a negative times a negative is positive. Students who write the bracket out as −3x − 12 lose marks even though the rest of their work is correct. Always change the sign of EVERY term inside a bracket that has a minus in front of it.",
      "source": "2017 OL P1 Q1"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-0"
  },
  {
    "id": "maths-ol-3-0-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2019,
    "questionRef": "2019 OL P1 Q2",
    "questionText": "Karl is working with the expression 3x² − 5x + 8.\n(a) Find the value of the expression when x = 4.\n(b) Write the expression 3x² − 5x + 8 in the form a + bx + cx² and hence write down the values of a, b and c.\n(c) Karl adds the expression 3x² − 5x + 8 to the expression 2x² + 5x − 1. Write the result of this addition in its simplest form.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Substitute, rewrite, and simplify as directed — show the value or simplest-form expression."
    },
    "ribbons": [
      {
        "label": "(a) Attempt: substitutes x = 4 into at least one term (e.g. 3(4)²)",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(a) Full: correct value 36",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Attempt: reorders to begin with the constant, e.g. 8 − 5x + …",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(b) Full: 8 − 5x + 3x² with a = 8, b = −5, c = 3",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Attempt: groups at least one pair of like terms correctly",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(c) Full: correct answer 5x² + 7",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "In part (a) the most frequent mistake is order-of-operations: students compute 3 × 4² as if it were (3 × 4)² = 12² = 144, instead of squaring first (4² = 16) and then multiplying by 3 to get 48. The power applies only to the x, not to the coefficient. Square the number first, then multiply by the coefficient. A second common slip in (c) is failing to notice that −5x and +5x cancel, leaving the answer with a phantom x-term.",
      "source": "2019 OL P1 Q2"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-0"
  },
  {
    "id": "maths-hl-3-1-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2017,
    "questionRef": "2017 HL P1 Q2",
    "questionText": "(a) Solve the simultaneous equations\n3x + 2y − z = 7\n2x − y + 2z = −5\nx + 3y + z = 8.\n(b) Hence, or otherwise, verify your solution by substituting your values into the second equation.",
    "marks": 25,
    "minutes": 25,
    "answerKind": "steps",
    "commandWord": {
      "word": "Solve",
      "reminder": "Work out the values of all the unknowns, showing your method."
    },
    "ribbons": [
      {
        "label": "One correct elimination producing a valid two-variable equation",
        "marks": 5,
        "kind": "attempt"
      },
      {
        "label": "Second correct elimination giving a second equation in the same pair",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "Solve the resulting 2×2 system for two variables (e.g. x = 0, y = 3)",
        "marks": 10,
        "kind": "method"
      },
      {
        "label": "Back-substitute to find the third variable (z = −1) and state the full solution",
        "marks": 5,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The most common error is a sign slip when eliminating a variable whose coefficient is negative (here −z and −y). Candidates routinely add equations when they should subtract (or forget to change the sign of every term in the equation being subtracted). Always rewrite the multiplied-out equation in full before adding/subtracting, and check the eliminated variable's coefficients truly cancel to zero before proceeding.",
      "source": "Examiner lesson"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-1"
  },
  {
    "id": "maths-hl-3-1-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2019,
    "questionRef": "2019 HL P1 Q3",
    "questionText": "(a) The equation 2x² + kx + 8 = 0, where k ∈ ℝ, has two equal real roots. Find the two possible values of k.\n(b) For the larger of these values of k, solve the equation 2x² + kx + 8 = 0.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Obtain the value(s); show enough working to justify the answer."
    },
    "ribbons": [
      {
        "label": "States/uses the equal-roots condition b² − 4ac = 0 with correct a, b or c",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "Forms the correct equation k² − 64 = 0 (or k² = 64)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Solves to obtain both values k = 8 and k = −8",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Substitutes k = 8 to get 2x² + 8x + 8 = 0 and begins a valid solving method",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Obtains x = −2",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The classic mistake is treating 'two equal real roots' as requiring b² − 4ac > 0 (distinct real roots) or even ≥ 0; the equal-roots case is exactly b² − 4ac = 0. A second frequent error in part (b) is reporting 'two roots' x = −2 and x = −2 as if they were distinct solutions, or losing the negative value of k in part (a) by taking only the positive square root of 64. Always write k = ±8 explicitly.",
      "source": "Examiner lesson"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-1"
  },
  {
    "id": "maths-ol-3-1-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2017,
    "questionRef": "2017 OL P1 Q1",
    "questionText": "(a) Solve the equation 3(2x − 5) = 4x + 7.\n(b) Solve the simultaneous equations\n    2x + 3y = 12\n    5x − y = 13.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Solve",
      "reminder": "Find the value(s) of the unknown(s) that make the equation(s) true, showing your working."
    },
    "ribbons": [
      {
        "label": "(a) Attempt: expands the bracket OR shows a valid first step (e.g. 6x − 15)",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(a) Partial: correctly gathers terms to 2x = 22 (or equivalent)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(a) Full: x = 11",
        "marks": 1,
        "kind": "method"
      },
      {
        "label": "(b) Attempt: valid strategy — multiplies one equation to match a coefficient, or rearranges to substitute",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(b) Partial: eliminates one variable correctly and finds its value (x = 3 or y = 2)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(b) Full: both x = 3 and y = 2 stated",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "In part (a) the most common error is multiplying only the first term inside the bracket — writing 6x − 5 instead of 6x − 15. The factor outside multiplies EVERY term inside, including the constant. In part (b), students often subtract equations when they should add (or vice versa): line up the signs of the variable being eliminated first, and add if those signs are opposite, subtract if they are the same.",
      "source": "2017 OL P1 Q1 marking-scheme lesson"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-1"
  },
  {
    "id": "maths-ol-3-1-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2019,
    "questionRef": "2019 OL P1 Q4",
    "questionText": "A ball is thrown upwards. Its height above the ground, h metres, after t seconds is given by the formula\n    h = 20t − 5t².\n(a) Find the value of t when the ball is at a height of 15 metres, by solving the equation 20t − 5t² = 15. Give both values of t.\n(b) Use your answers from part (a) to explain why there are two different times at which the ball is 15 metres above the ground.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find / explain",
      "reminder": "Work out the value(s) requested, then give a reasoned account of why the result occurs."
    },
    "ribbons": [
      {
        "label": "(a) Attempt: forms the quadratic, e.g. 20t − 5t² − 15 = 0 or any correct rearrangement to one side",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(a) Partial: reduces to a correct simplified quadratic such as t² − 4t + 3 = 0 (or works the unsimplified form correctly)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(a) Partial: correct factors (t − 1)(t − 3) = 0, or correct substitution into the quadratic formula",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(a) Full: t = 1 and t = 3, both values stated",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Partial: refers to the ball going up and coming down (or mentions the two times)",
        "marks": 2,
        "kind": "explain"
      },
      {
        "label": "(b) Full: clear explanation linking t = 1 to rising and t = 3 to falling, so 15 m is reached on the way up and again on the way down",
        "marks": 3,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "The most common mistake is dividing through by −5 but forgetting to change the sign of every term — students often write t² − 4t − 3 = 0 (leaving the constant negative) instead of t² − 4t + 3 = 0. Dividing −15 by −5 gives +3, not −3. A second frequent error is giving only one solution: a quadratic set to zero can have two roots, and this question explicitly asks for both values of t, so stopping at t = 1 loses marks.",
      "source": "2019 OL P1 Q4 marking-scheme lesson"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-1"
  },
  {
    "id": "maths-hl-3-2-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2018,
    "questionRef": "2018 HL P1 Q4 (representative)",
    "questionText": "(a) Solve the inequality 2x² − x − 6 ≤ 0, where x ∈ ℝ. Give your answer in the form a ≤ x ≤ b.\n\n(b) Hence, or otherwise, find the set of all real values of x for which 2x² − x − 6 ≤ 0 and 3x − 1 > 0 are both true. Give your answer in the form { x | … , x ∈ ℝ }.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Solve",
      "reminder": "Work out the values of x that satisfy the inequality, showing your method and stating the solution interval."
    },
    "ribbons": [
      {
        "label": "Attempt at factorising / finding roots (e.g. correct product −12 or quadratic formula set-up)",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "Correct factors (2x + 3)(x − 2) or correct roots x = −3/2 and x = 2",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Correct inequality solution for (a): −3/2 ≤ x ≤ 2, with correct direction (between the roots, inclusive)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Solving 3x − 1 > 0 to get x > 1/3",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Correct intersection giving { x | 1/3 < x ≤ 2 }, with correct open/closed endpoints",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The single most common error is getting the DIRECTION of the solution wrong — students correctly find the roots but then write x ≤ −3/2 or x ≥ 2 (the \"outside\" region) when the inequality is ≤ 0. Because the x² coefficient is positive, the curve dips BELOW the axis between the roots, so ≤ 0 gives the inside interval and ≥ 0 gives the two outside rays. Always sketch the upward parabola and read off the region; and in part (b), watch the endpoint at 1/3 — a strict inequality (>) means it must be EXCLUDED, so the answer is 1/3 < x, not 1/3 ≤ x.",
      "source": "2018 HL P1 Q4 (representative)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-2"
  },
  {
    "id": "maths-hl-3-2-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2017,
    "questionRef": "2017 HL P1 Q5 (representative)",
    "questionText": "The cost of running a small workshop for x hours per day is modelled by C(x) = x² − 14x + 58 (in units of €10), and the workshop must operate for at least some part of the day.\n\n(a) Show that C(x) can be written in the form (x − p)² + q, where p, q ∈ ℝ, and hence write down the least possible daily cost.\n\n(b) For safety and budget reasons, the daily cost (in units of €10) must be kept below 13; that is, C(x) < 13. Find the range of values of x (number of hours) for which this is satisfied. Give your answer correct to two decimal places.\n\n(c) The workshop can physically run for at most 10 hours in a day, so x must also satisfy 0 < x ≤ 10. Taking this together with part (b), state the largest number of hours (to two decimal places) for which the cost condition C(x) < 13 holds.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "steps",
    "commandWord": {
      "word": "Show that",
      "reminder": "Demonstrate the stated result with clear working, then find and state the required values."
    },
    "ribbons": [
      {
        "label": "(a) Attempt to complete the square (correct (x − 7)² term or correct value of p = 7)",
        "marks": 4,
        "kind": "attempt"
      },
      {
        "label": "(a) Fully correct (x − 7)² + 9 and least cost stated as 9 units / €90",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Correct inequality reduced to x² − 14x + 45 < 0",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Correct roots x = 5 and x = 9 (formula or factors)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Correct strict solution 5 < x < 9 to two d.p. (between the roots)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(c) Correct intersection with 0 < x ≤ 10 giving 5 < x < 9 and identifying upper boundary 9.00 (excluded)",
        "marks": 5,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The classic mistake here is mishandling the STRICT inequality and the endpoints. Because C(x) < 13 (not ≤), the roots x = 5 and x = 9 are NOT part of the solution — at exactly those values C(x) = 13, which fails the \"< 13\" test. Students frequently write 5 ≤ x ≤ 9. A second, subtler error in part (c) is assuming the physical limit x ≤ 10 must \"tighten\" the answer; here it does not, because 9 < 10, so the binding upper limit comes from the inequality, not the physical cap — always compare the two upper bounds and take the SMALLER. Also note: completing the square in (a) is the efficient route, but it is the quadratic-inequality work in (b) that earns the bulk of the marks, so do not stop at the vertex.",
      "source": "2017 HL P1 Q5 (representative)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-2"
  },
  {
    "id": "maths-ol-3-2-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2017,
    "questionRef": "2017 OL P1 Q2",
    "questionText": "(a) Solve the inequality 5x - 7 ≤ 3x + 9, where x ∈ R (the set of real numbers).\n(b) Show your solution to part (a) on the number line.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "steps",
    "commandWord": {
      "word": "Solve",
      "reminder": "Find the value(s) of x that make the inequality true; show your working."
    },
    "ribbons": [
      {
        "label": "Attempt: gathers x-terms on one side or number terms on the other (e.g. reaches 2x - 7 ≤ 9)",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "Partial credit (low): correct simplification to 2x ≤ 16 but not finished, or a sign/transposition slip carried",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Partial credit (high): fully correct solution x ≤ 8",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Number line: closed dot at 8 (1) and shading/arrow to the left (1)",
        "marks": 2,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The most common error here is mishandling the number line, not the algebra: students frequently use an OPEN (hollow) dot at 8 even though the inequality is ≤ (which includes 8 and therefore requires a CLOSED dot), or they shade in the wrong direction. Rule of thumb: ≤ and ≥ → closed dot; < and > → open dot. Then test a simple value (e.g. x = 0) to decide which way to shade — if it satisfies the inequality, shade the side containing it.",
      "source": "LESSON"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-2"
  },
  {
    "id": "maths-ol-3-2-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2019,
    "questionRef": "2019 OL P1 Q4",
    "questionText": "List all the integer values of x that satisfy the inequality -4 < 2x - 1 ≤ 7, where x ∈ Z (the set of integers).",
    "marks": 10,
    "minutes": 10,
    "answerKind": "steps",
    "commandWord": {
      "word": "List",
      "reminder": "Write out every value in the solution set — none missing, no extras."
    },
    "ribbons": [
      {
        "label": "Attempt: performs a correct operation on the compound inequality (e.g. adds 1 to all parts to reach -3 < 2x ≤ 8) or correctly handles at least one inequality",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "Partial credit (low): correctly reduces to -1.5 < x ≤ 4 (algebra finished)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Partial credit (high): lists the correct integer set but with one endpoint error",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Full listing: correct complete set {-1, 0, 1, 2, 3, 4} with no extras and none missing",
        "marks": 2,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The classic mistakes are (1) flipping or losing the strictness of one end — students often wrongly include x = -2 by forgetting that -1.5 < x is STRICT (so -2 is too small and -1 is the smallest valid integer), or wrongly exclude x = 4 by forgetting that ≤ INCLUDES the endpoint; and (2) operating on only the middle and one side while ignoring the other part of the compound inequality. Always apply each operation to ALL THREE parts simultaneously, and at the end test both boundary integers to confirm which are in and which are out.",
      "source": "LESSON"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-2"
  },
  {
    "id": "maths-hl-3-3-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2016,
    "questionRef": "2016 HL P1 Q2",
    "questionText": "Let z = 2 − 3i, where i² = −1.\n\n(a) Express each of the following in the form a + bi, where a, b ∈ ℝ:\n   (i) z + z̄ (the complex number z plus its conjugate)\n   (ii) z · z̄\n   (iii) z / (1 + i)\n\n(b) The complex number w satisfies (3 + 2i)w = 13. Find w in the form a + bi, where a, b ∈ ℝ.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Express / Find",
      "reminder": "Express: write in the required form a + bi. Find: determine the value, showing working."
    },
    "ribbons": [
      {
        "label": "(a)(i) Conjugate z̄ = 2 + 3i identified and z + z̄ = 4",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(a)(ii) Sets up product (2−3i)(2+3i) and obtains z·z̄ = 13",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(a)(iii) States intention to multiply by conjugate of denominator (low partial)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(a)(iii) Multiplies by (1−i), correct numerator −1−5i and denominator 2, final −1/2 − (5/2)i",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(b) Isolates w = 13/(3+2i) and multiplies by (3−2i) (high partial)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Final answer w = 3 − 2i",
        "marks": 2,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The single most common error here is mishandling i² when expanding. Students very often write (2 − 3i)(1 − i) and leave the +3i² term as −3 (forgetting i² = −1 means +3i² = −3, which is actually correct) OR worse, treat i² as +1, turning −9i² into −9 in part (ii) and getting 4 − 9 = −5 instead of 13. Always substitute i² = −1 explicitly as a written step. A second frequent slip in division is multiplying only the numerator (or only the denominator) by the conjugate — you must multiply BOTH by the same factor so you are effectively multiplying by 1.",
      "source": "2016 HL P1 Q2"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-3"
  },
  {
    "id": "maths-hl-3-3-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2018,
    "questionRef": "2018 HL P1 Q3",
    "questionText": "(a) (i) Use De Moivre's Theorem to express (1 + i)⁸ in the form a + bi, where a, b ∈ ℝ. Show your working, including the modulus and argument of (1 + i).\n\n(b) Two of the roots of the equation z³ + bz² + cz + d = 0, where b, c, d ∈ ℝ, are z = 4 and z = 2 + i.\n   (i) Write down the third root of the equation.\n   (ii) Find the values of b, c and d.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "steps",
    "commandWord": {
      "word": "Use / Express / Write down / Find",
      "reminder": "Use De Moivre's Theorem: you must apply that named method. Write down: state the answer, no working needed. Find: determine the values, showing working."
    },
    "ribbons": [
      {
        "label": "(a) Correct modulus √2 and argument π/4 (low partial)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(a) Correct De Moivre set-up (√2)⁸[cos(8·π/4) + i sin(8·π/4)] (mid partial)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(a) (√2)⁸ = 16, argument 2π and final answer 16",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(b)(i) Third root 2 − i stated",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b)(ii) Forms conjugate-pair quadratic z² − 4z + 5 and begins product with (z − 4) (high partial)",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(b)(ii) Correct expansion giving b = −8, c = 21, d = −20",
        "marks": 2,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "In part (a) the most common mistake is an arithmetic error on the modulus power: students correctly find r = √2 but then compute (√2)⁸ wrongly — writing 2⁸ = 256 or √(2⁸) = 16 by luck without justification. Convert to a fractional index, (2^(1/2))⁸ = 2⁴ = 16, to keep it watertight. In part (b), the classic error is forgetting that real coefficients force the conjugate 2 − i to be a root, and instead trying to find a real third root by guesswork; also, when expanding, students drop the i² = −1 sign and get z² − 4z + 3 for the conjugate-pair quadratic. Pair the conjugate factors FIRST using ((z−2)² − i²) to avoid sign errors.",
      "source": "2018 HL P1 Q3"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-3"
  },
  {
    "id": "maths-ol-3-3-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2016,
    "questionRef": "2016 OL P1 Q3",
    "questionText": "Two complex numbers are given as z = 4 + 3i and w = 2 − 5i, where i² = −1.\n(a) Write z + w in the form a + bi, where a, b ∈ ℝ.\n(b) Write zw in the form a + bi, where a, b ∈ ℝ.\n(c) Find |z|, the modulus of z.\n(d) Plot z and w on an Argand diagram. (Answer on paper.)",
    "marks": 20,
    "minutes": 20,
    "answerKind": "paper",
    "commandWord": {
      "word": "Write / Find / Plot",
      "reminder": "Write/Find: give the result in the required form; Plot: mark and label the points on the diagram."
    },
    "ribbons": [
      {
        "label": "(a) Attempt: adds real or imaginary parts correctly but not both",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(a) Full: z + w = 6 − 2i",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Attempt: expands brackets with at least two correct product terms",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(b) Full: uses i² = −1 and reaches 23 − 14i",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Attempt: writes √(4² + 3²) or √(16 + 9)",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(c) Full: |z| = 5",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(d) Attempt: one point plotted correctly, or axes drawn with attempt",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(d) Full: both z and w correctly plotted and labelled",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The single most common error in part (b) is forgetting that i² = −1 and leaving the answer as 8 − 14i − 15i² (or treating −15i² as −15). You must replace i² with −1, which flips the sign, turning −15i² into +15 and pushing the real part from 8 to 23. Always do the i² substitution as a separate, explicit line before collecting real and imaginary parts.",
      "source": "2016 OL P1 Q3"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-3"
  },
  {
    "id": "maths-ol-3-3-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2018,
    "questionRef": "2018 OL P1 Q5",
    "questionText": "The complex number z = 3 + i is a root of the equation z² + bz + c = 0, where b, c ∈ ℝ and i² = −1.\n(a) Verify that z = 3 + i is a root of the equation z² − 6z + 10 = 0.\n(b) Write down the second root of the equation z² − 6z + 10 = 0. (Both roots of an equation with real coefficients occur as a conjugate pair.)\n(c) The complex number 3 + i is multiplied by i. Investigate, using an Argand diagram or otherwise, the effect that multiplying by i has on the complex number 3 + i. State the new complex number and describe the geometric change in words.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "steps",
    "commandWord": {
      "word": "Verify / Write down / Investigate",
      "reminder": "Verify: substitute and show the LHS reduces to 0, then state it is a root; Write down: state the answer; Investigate: explore and describe the effect."
    },
    "ribbons": [
      {
        "label": "(a) Attempt: substitutes z = 3 + i and attempts (3 + i)², e.g. shows 9 + 6i + i²",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(a) Mid: correctly gets z² = 8 + 6i and −6z = −18 − 6i",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(a) Full: combines to show 8 + 6i − 18 − 6i + 10 = 0, with conclusion stated",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Attempt: states roots are a conjugate pair / writes 3 ± i",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(b) Full: 3 − i",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Attempt: computes i(3 + i) and reaches −1 + 3i (or shows the plotted point)",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(c) Full: correct new number −1 + 3i AND states the effect is a 90° anticlockwise rotation about the origin",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "In part (a), students lose marks by stopping after computing (3 + i)² and not driving the full expression to exactly 0 — a \"verify\" instruction requires you to substitute everything and show the left-hand side reduces to 0 (and say so). A second frequent slip is mishandling (3 + i)²: writing it as 9 + i² (forgetting the middle term 2·3·i = 6i) — always expand a squared bracket as a full FOIL or use a² + 2ab + b², never just square each term.",
      "source": "2018 OL P1 Q5"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-3"
  },
  {
    "id": "maths-hl-4-0-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2017,
    "questionRef": "2017 HL P1 Q7",
    "questionText": "The cubic function h is defined as h(x) = x³ − 6x² + 9x − 2, where x ∈ ℝ.\n\n(a) Show that x = 2 is a root of h(x), and hence find the other two roots of h(x) = 0, giving your answers in the form a ± √b, where a, b ∈ ℕ.\n\n(b) Find the co-ordinates of the local maximum point and the local minimum point of the graph of h. (You may use calculus.)\n\n(c) The graph of h cuts the y-axis at the point c. Write down the co-ordinates of c, and using all of the above, sketch the graph of h in the domain −1 ≤ x ≤ 5.",
    "marks": 25,
    "minutes": 25,
    "answerKind": "paper",
    "commandWord": {
      "word": "Show ... find ... sketch",
      "reminder": "Show: demonstrate the stated result with working. Find: work out the values. Sketch: draw a correctly shaped graph through the key points."
    },
    "ribbons": [
      {
        "label": "(a) Show h(2) = 0 (substitute x = 2 and evaluate to 0)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(a) Factorise/divide to quadratic x² − 4x + 1 and solve to roots 2 ± √3",
        "marks": 7,
        "kind": "method"
      },
      {
        "label": "(b) Differentiate and solve h′(x) = 0 to get x = 1 and x = 3",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(b) Find y-values and classify local max (1, 2) and local min (3, −2)",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(c) State c = (0, −2) and produce correct sketch through all key points",
        "marks": 5,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The most common mistake is mis-classifying the turning points — students find x = 1 and x = 3 correctly but then assume the smaller x-value is automatically the maximum, or guess without justification. For a positive-leading cubic the first turning point (smaller x) is the local maximum and the second is the local minimum, but examiners award the classification marks only when it is justified, either by the second-derivative test (sign of h″) or by checking the sign of h′ on either side. A second frequent slip is arithmetic in h(3): forgetting that 6(9) = 54 and writing −36, which gives the wrong y-value and a distorted sketch.",
      "source": "2017 HL P1 Q7"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-4-0"
  },
  {
    "id": "maths-ol-4-0-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2017,
    "questionRef": "2017 OL P1 Q6 (representative)",
    "questionText": "The function f is defined as f(x) = 2x² − 3x − 5, where x ∈ ℝ.\n\n(a) Find the value of f(0).\n\n(b) Find the value of f(−2).\n\n(c) The graph of f cuts the x-axis at two points. Use the function to find the co-ordinates of the two points where the graph of f cuts the x-axis. Give your answers in fraction form where necessary.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Work out the value/co-ordinates and show your working."
    },
    "ribbons": [
      {
        "label": "(a) Correct evaluation f(0) = −5",
        "marks": 5,
        "kind": "evaluation"
      },
      {
        "label": "(b) Correct evaluation f(−2) = 9",
        "marks": 5,
        "kind": "evaluation"
      },
      {
        "label": "(c) Sets f(x) = 0 / starts a valid solving method",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(c) Solves correctly to obtain both x-values x = 5/2 and x = −1",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(c) States both points as co-ordinates (5/2, 0) and (−1, 0)",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The single most common error in part (c) is giving the answer as bare x-values (x = 5/2, x = −1) instead of co-ordinates. The question asks for the POINTS where the graph cuts the x-axis, so each answer must be an ordered pair with the y-coordinate written explicitly as 0: (5/2, 0) and (−1, 0). A close second is mishandling signs when substituting a negative number in part (b) — remember (−2)² is +4, not −4, and −3 × (−2) is +6, not −6.",
      "source": "2017 OL P1 Q6 (representative)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-4-0"
  },
  {
    "id": "maths-ol-4-0-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2016,
    "questionRef": "2016 OL P1 Q7 (representative)",
    "questionText": "Two functions f and g are defined for x ∈ ℝ as:\n   f(x) = 3x + 1\n   g(x) = 9 − x\n\n(a) Complete the table below to show the value of each function for the given values of x.\n\n      x        −1        0        2        4\n   f(x)  =  3x + 1\n   g(x)  =  9 − x\n\n(b) On the same diagram, draw the graphs of f and g for −1 ≤ x ≤ 4. Use the same axes and label each line. (Answer on graph paper.)\n\n(c) Use your graphs to estimate the co-ordinates of the point of intersection of the two lines, i.e. the point where f(x) = g(x).\n\n(d) Verify your answer to part (c) using algebra.",
    "marks": 25,
    "minutes": 25,
    "answerKind": "paper",
    "commandWord": {
      "word": "Verify",
      "reminder": "Confirm the result by working it through, here algebraically, and show it matches."
    },
    "ribbons": [
      {
        "label": "(a) Table f-row correct (−2, 1, 7, 13)",
        "marks": 4,
        "kind": "evaluation"
      },
      {
        "label": "(a) Table g-row correct (10, 9, 7, 5)",
        "marks": 4,
        "kind": "evaluation"
      },
      {
        "label": "(b) Both lines drawn from candidate's points and correctly labelled",
        "marks": 7,
        "kind": "application"
      },
      {
        "label": "(c) States intersection co-ordinates ≈ (2, 7) read from the graph",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(d) Sets f(x) = g(x) and solves to x = 2",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(d) Finds y = 7 and states full point (2, 7) confirming part (c)",
        "marks": 2,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The most common mistakes here are (i) the sign slip at g(−1): students compute 9 − (−1) as 8 instead of 10, forgetting that subtracting a negative adds; and (ii) in part (d), stopping at x = 2 without substituting back to find y, so they never state the full point of intersection. \"Verify\" demands the complete co-ordinate (2, 7) and a clear statement that it matches the graphical reading — an x-value alone earns only partial credit.",
      "source": "2016 OL P1 Q7 (representative)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-4-0"
  },
  {
    "id": "maths-hl-4-1-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2018,
    "questionRef": "2018 HL P1 Q6",
    "questionText": "The function f is defined for x ∈ ℝ as f(x) = 2x³ − 9x² + 12x − 3.\n(a) Find f′(x), the derivative of f(x).\n(b) Find the coordinates of the local maximum point and the local minimum point of the curve y = f(x). Use the second derivative to justify, in each case, whether the point is a local maximum or a local minimum.\n(c) Find the range of values of x for which the curve y = f(x) is decreasing.",
    "marks": 25,
    "minutes": 25,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Work out the answer, showing the calculation that produces it."
    },
    "ribbons": [
      {
        "label": "(a) Attempt: differentiates at least one term correctly (e.g. 6x² obtained)",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(a) Full: f′(x) = 6x² − 18x + 12 fully correct",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(b) x-values of turning points: sets f′(x) = 0",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(b) x-values: x = 1 and x = 2 found correctly",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Partial: both y-values correct OR f″(x) found and tested",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(b) Full: points (1, 2) and (2, 1) correct AND f″ used to classify each (max/min)",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(c) Attempt: states condition f′(x) < 0 or uses turning points",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(c) Full: decreasing for 1 < x < 2",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The most common error is giving only the x-values and forgetting the full coordinates, or — when \"use the second derivative to justify\" is explicitly required — classifying max/min by inspection or a sign table instead. If the question names a method, you must use that method to earn the justification marks; in part (c) the answer is a strict inequality between the roots (1 < x < 2), not x < 1 or x > 2.",
      "source": "2018 HL P1 Q6"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-4-1"
  },
  {
    "id": "maths-hl-4-1-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2017,
    "questionRef": "2017 HL P1 Q8",
    "questionText": "A particle moves in a straight line. Its displacement from a fixed point O, in metres, is given by s(t) = t³ − 6t² + 9t + 4, where t is the time in seconds, t ≥ 0.\n(a) Find the velocity of the particle, in terms of t.\n(b) Find the times at which the particle is instantaneously at rest.\n(c) Find the acceleration of the particle when t = 4 seconds.\n(d) Find the total distance travelled by the particle in the first 3 seconds of its motion.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Work out the answer, showing the calculation that produces it."
    },
    "ribbons": [
      {
        "label": "(a) Attempt: one term differentiated correctly",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(a) Full: v(t) = 3t² − 12t + 9",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Attempt: sets v(t) = 0",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(b) Full: t = 1 and t = 3",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Partial: a(t) = 6t − 12 correct",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) Full: a(4) = 12 m/s²",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(d) Attempt: computes relevant positions (e.g. s(0), s(1), s(3)) or recognises change of direction at t = 1",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "(d) Full: correctly splits at t = 1 and obtains 8 m",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The classic trap in part (d) is computing s(3) − s(0) = 0 and reporting \"0 m\" (or treating the journey as one leg). \"Total distance travelled\" requires checking for a change of direction inside the interval (where v = 0 and changes sign), then summing the absolute distance of each leg. Here the particle goes out 4 m then comes back 4 m, giving 8 m even though the net displacement is 0.",
      "source": "2017 HL P1 Q8"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-4-1"
  },
  {
    "id": "maths-ol-4-1-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2018,
    "questionRef": "2018 OL P1 Q7",
    "questionText": "The function f(x) = x³ − 6x² + 9x + 2 is defined for x ∈ ℝ.\n\n(a) Find f '(x), the derivative of f(x).\n\n(b) Find the co-ordinates of the two turning points of the curve y = f(x).\n\n(c) Determine, using the second derivative, whether each turning point is a local maximum or a local minimum.",
    "marks": 25,
    "minutes": 25,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find / Determine",
      "reminder": "Find: state the result. Determine: decide and justify (here, max or min using the second derivative)."
    },
    "ribbons": [
      {
        "label": "Differentiate f(x): one term correct (low partial), full f '(x) = 3x² − 12x + 9",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "Set f '(x) = 0 and solve: equate to 0 (attempt 3), factorise quadratic (mid 7), x = 1 and x = 3 (full 10)",
        "marks": 10,
        "kind": "method"
      },
      {
        "label": "Find y-co-ordinates by substituting into f(x): one point (partial 2), both points (1, 6) and (3, 2)",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "Classify using f ''(x) = 6x − 12: found (attempt 2), max at (1, 6) and min at (3, 2) with sign reasoning (full 5)",
        "marks": 5,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The single most common error is stopping at the x-values and presenting them as \"the turning points.\" A turning point is a CO-ORDINATE — students lose the y-mark by failing to substitute x = 1 and x = 3 back into the ORIGINAL f(x) (not f '(x)). A second frequent slip in part (c) is substituting into f '(x) instead of f ''(x), or stating the result without showing the sign that justifies max vs min.",
      "source": "2018 OL P1 Q7 examiner lesson"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-4-1"
  },
  {
    "id": "maths-ol-4-1-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2017,
    "questionRef": "2017 OL P1 Q6",
    "questionText": "A ball is thrown vertically upwards. Its height above the ground, in metres, after t seconds is given by\n\nh(t) = 20t − 5t²,  for 0 ≤ t ≤ 4.\n\n(a) Find the speed of the ball, in metres per second, at the instant it is thrown (i.e. at t = 0). [Speed is given by h '(t).]\n\n(b) Find the value of t at which the ball reaches its maximum height, and find this maximum height.\n\n(c) Find the speed of the ball when it hits the ground.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Find: carry out the calculation and state the result, with correct units."
    },
    "ribbons": [
      {
        "label": "Differentiate and evaluate at t = 0: h '(t) = 20 − 10t (attempt 2), h '(0) = 20 m/s (full 5)",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "Maximum height: set h '(t) = 0 (attempt 3), t = 2 (mid 6), t = 2 s AND max height = 20 m via h(t) (full 10)",
        "marks": 10,
        "kind": "method"
      },
      {
        "label": "Speed at ground: find t = 4 or substitute into h '(t) (attempt 2), obtain −20 (partial 4), speed = 20 m/s (full 5)",
        "marks": 5,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The classic mistake here is a conceptual mix-up between the two functions: students substitute t = 2 into h '(t) to get the maximum HEIGHT (getting 0, the velocity) instead of into h(t). Remember: h(t) gives height (metres), h '(t) gives speed/velocity (m/s). In part (c) the other common error is reporting the answer as −20 m/s — velocity can be negative, but SPEED is always the positive magnitude, so the expected answer is 20 m/s.",
      "source": "2017 OL P1 Q6 examiner lesson"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-4-1"
  },
  {
    "id": "maths-hl-2-0-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2018,
    "questionRef": "2018 HL P1 Q2",
    "questionText": "(a) Express each of the following in the form a + bi, where a, b ∈ ℝ and i² = −1.\n   (i) (3 − 2i)(4 + 5i)\n   (ii) (5 + 3i) / (2 − i)\n(b) z = 1 + i is one root of the equation z² + bz + c = 0, where b, c ∈ ℝ. Find the value of b and the value of c.\n(c) Verify that |z₁z₂| = |z₁| · |z₂|, where z₁ = 3 − 2i and z₂ = 4 + 5i.",
    "marks": 25,
    "minutes": 25,
    "answerKind": "steps",
    "commandWord": {
      "word": "Express / Find / Verify",
      "reminder": "Express: rewrite in the required a + bi form. Find: compute the values. Verify: compute both sides independently and explicitly state they are equal."
    },
    "ribbons": [
      {
        "label": "(a)(i) Expand and simplify using i² = −1 to reach 22 + 7i",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(a)(ii) Multiply by conjugate, denominator 5 and numerator 7 + 11i, final form",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(b) Other root = 1 − i and use of sum/product (or substitution) to find b and c",
        "marks": 7,
        "kind": "method"
      },
      {
        "label": "(c) Correct |z₁z₂| = √533 and |z₁|·|z₂| = √533 with conclusion stated",
        "marks": 8,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The most common error in part (a)(ii) is forgetting to multiply the numerator AND denominator by the conjugate, or mishandling the sign in i² so the denominator is taken as 4 − 1 = 3 instead of 4 + 1 = 5. In part (c), \"verify\" demands you compute both sides independently and explicitly state they are equal — students who only compute one side, or who write |z₁z₂| = |z₁|·|z₂| as if assuming it, lose the conclusion mark.",
      "source": "2018 HL P1 Q2 examiner report"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-0"
  },
  {
    "id": "maths-hl-2-1-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2017,
    "questionRef": "2017 HL P1 Q1",
    "questionText": "(a) Write each of the following in the form 2^k, where k is a rational number.\n(i) ⁴√8\n(ii) (16 × √2) / 8^(2/3)\n\n(b) Express (5 + 3√2) / (4 − √2) in the form a + b√2, where a, b ∈ ℚ.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Write / Express ... in the form",
      "reminder": "Manipulate the expression into the exact stated form, giving the required values/components."
    },
    "ribbons": [
      {
        "label": "(a)(i) Attempt: writes 8 as 2^3 or uses 8^(1/4); full credit for 2^(3/4)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(a)(ii) Low partial: at least two of three factors converted to base 2 (e.g. 16 = 2^4, 8^(2/3) = 2^2)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(a)(ii) High partial/full: all factors converted and exponents combined to 2^(5/2)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Attempt: multiplies numerator and denominator by the conjugate (4 + √2)",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(b) Correct denominator 14",
        "marks": 1,
        "kind": "method"
      },
      {
        "label": "(b) Numerator expansion 26 + 17√2 and final form 13/7 + (17/14)√2",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The single most common error is mishandling 8^(2/3) — students write it as 2^(2/3) (cubing/cube-rooting the index rather than the base) or treat it as 8 × 2/3. The clean method is to rewrite every term to the common prime base first (8 = 2^3, so 8^(2/3) = 2^(3 × 2/3) = 2^2), THEN combine indices. In part (b), the second frequent slip is forgetting to multiply BOTH the numerator and denominator by the conjugate, or sign-errors in the middle terms of the expansion; keep the four product terms explicit.",
      "source": "2017 HL P1 Q1"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-1"
  },
  {
    "id": "maths-hl-2-2-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2018,
    "questionRef": "2018 HL P1 Q2",
    "questionText": "A new car is bought for €27,500. Its value depreciates by 12% in the first year, by 10% in the second year, and by 8% in the third year.\n\n(a) Find the value of the car at the end of the third year, correct to the nearest euro.\n\n(b) An investor places €15,000 in an account that pays compound interest at an Annual Equivalent Rate (AER) of 3.5%. Find the amount in the account at the end of 4 years, correct to the nearest cent.\n\n(c) The investor in part (b) actually wants the account to grow to €20,000 in those same 4 years. Find the AER, correct to one decimal place, that would be required to achieve this.",
    "marks": 25,
    "minutes": 25,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Work out the value/amount/rate and show the steps that produce it."
    },
    "ribbons": [
      {
        "label": "(a) Attempt: any correct year-1 reducing multiplier (×0.88 or 27,500 − 12%)",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(a) Full: all three reducing multipliers applied (0.88 × 0.90 × 0.92) and rounded to €20,038",
        "marks": 7,
        "kind": "method"
      },
      {
        "label": "(b) Correct use of F = P(1+i)^4 with i = 0.035 giving €17,212.85",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(c) Attempt: sets up (1+i)^4 = 20000/15000 = 1.3333",
        "marks": 4,
        "kind": "attempt"
      },
      {
        "label": "(c) Full: takes the fourth root and states AER = 7.5%",
        "marks": 6,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The most common error is treating depreciation/compound interest as simple (linear) rather than compound — e.g. adding 12% + 10% + 8% = 30% and taking 30% off the original price, or doing 27,500 × 0.70. Each year's percentage must act on the *previous* year's value, so you multiply successive reducing factors (0.88 × 0.90 × 0.92). A second frequent slip is reversing the factor: using 0.12 instead of 0.88 (the amount *lost* rather than the amount *retained*). In part (c), students often forget the index is 4, taking a square root or no root at all, instead of the **fourth** root.",
      "source": "2018 HL P1 Q2"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-2"
  },
  {
    "id": "maths-hl-2-2-3",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2017,
    "questionRef": "2017 HL P1 Q1",
    "questionText": "A bureau de change in Dublin displays the following rates for converting euro (€):\n- £1 (sterling) = €1.18\n- US $1 = €0.92\n\nThe bureau charges a commission of 2% on every transaction, deducted from the euro amount before the currency is converted.\n\n(a) A customer wishes to convert €600 into US dollars. Calculate how many US dollars the customer receives, correct to the nearest cent.\n\n(b) A second customer changes some euro into sterling and, after the 2% commission, receives £250 (sterling). Calculate, correct to the nearest cent, how many euro the customer handed over.\n\n(c) A tourist buys an item in London priced at £80. The same item is on sale in New York for $96. Using the rates above (ignoring commission), determine in which city the item is cheaper, and by how much in euro, correct to the nearest cent.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "steps",
    "commandWord": {
      "word": "Calculate",
      "reminder": "Work out the numerical answer (and for part c decide which city), showing the conversions used."
    },
    "ribbons": [
      {
        "label": "(a) Attempt: deducts 2% commission (600 × 0.98 = 588) OR correctly divides by 0.92",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(a) Full: combines both correctly to get $639.13",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(b) Attempt: works backwards from £250, e.g. 250 × 1.18 = 295",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(b) Full: divides by 0.98 to undo commission, €301.02",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(c) Converts both prices to euro (€94.40 and €88.32)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) States New York cheaper and difference €6.08",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The classic mistake is using the exchange rate the wrong way round — multiplying when you should divide. The rate \"$1 = €0.92\" tells you that going *from dollars to euro* you multiply by 0.92, so going *from euro to dollars* you must **divide** by 0.92 (one euro is worth more than one dollar here, so you should get more dollars than euro — a quick sanity check). In part (b), the second trap is applying commission in the wrong direction: because €250-worth is the amount *after* a 2% deduction, you must divide by 0.98 (not multiply), since the original handed-over amount is larger than the converted amount.",
      "source": "2017 HL P1 Q1"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-2"
  },
  {
    "id": "maths-ol-0-3-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2018,
    "questionRef": "2018 OL P2 Q9 (representative)",
    "questionText": "A national newspaper publishes the following headline:\n\n\"POLL SHOWS 54% OF IRISH ADULTS SUPPORT THE NEW RECYCLING LAW\"\n\nUnderneath the headline, the newspaper prints the following note about how the poll was carried out:\n\n\"1,100 adults were surveyed. The poll has a margin of error of ±3% at a confidence level of 95%.\"\n\n(a) The newspaper claims that \"a clear majority of all Irish adults support the new law.\" Using the figures given, explain whether the margin of error supports this claim. Justify your answer fully.\n\n(b) Write down the interval (range of percentages) within which the true level of support in the whole adult population is likely to lie.\n\n(c) A reader makes the following statement: \"Because the margin of error is only ±3%, we can be 100% certain that the true support is between those two values.\" State whether the reader is correct, and explain your answer with reference to the confidence level.\n\n(d) The newspaper wants to reduce the margin of error for its next poll. State one thing it could do to achieve this, and explain why it would work.",
    "marks": 25,
    "minutes": 25,
    "answerKind": "written",
    "commandWord": {
      "word": "explain",
      "reminder": "Give clear reasons; show how the figures justify your answer."
    },
    "ribbons": [
      {
        "label": "(a) Calculates lower bound 54 − 3 = 51%",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(a) Compares with 50% and states majority is supported",
        "marks": 4,
        "kind": "explain"
      },
      {
        "label": "(b) States lower value 51%",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) States upper value 57%",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(c) States reader is incorrect",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(c) Explanation referring to 95% (not 100%) / 1-in-20 chance outside",
        "marks": 4,
        "kind": "explain"
      },
      {
        "label": "(d) States increase the sample size",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(d) Correct reason (larger sample → smaller margin of error)",
        "marks": 2,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "The most common error in part (a) is to argue from the headline figure of 54% alone (\"54% is more than 50%, so yes\"). That earns no credit for the reasoning — the whole point of the margin of error is that you must test the WORST case. Always subtract the margin of error first (54 − 3 = 51) and compare the LOWER bound to 50%. The claim only holds if the entire interval stays above 50%. Had the figure been, say, 52% with ±3%, the lower bound (49%) would dip below 50% and the \"clear majority\" claim would NOT be supported.",
      "source": "2018 OL P2 Q9 (representative)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-3"
  },
  {
    "id": "maths-ol-0-3-3",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2017,
    "questionRef": "2017 OL P2 Q8 (representative)",
    "questionText": "A company that sells a sports drink runs an advertisement. The advertisement makes the following claim:\n\n\"9 OUT OF 10 ATHLETES PREFER our drink to any other!\"\n\nThe small print at the bottom of the advertisement gives the following details about how this result was found:\n\n• 20 people were asked.\n• All 20 people were members of a team that is sponsored by (paid by) the sports-drink company.\n• The 20 people were asked the question: \"Don't you agree that our amazing drink is the best you have ever tasted?\"\n\n(a) The advertisement says \"9 out of 10 athletes prefer our drink.\" Write \"9 out of 10\" as a percentage.\n\n(b) Give TWO different reasons why this survey is biased (not fair), and for each reason explain clearly how it could affect the result.\n\n(c) The advertisement suggests the result applies to athletes in general. Explain why the sample used is too small and unsuitable to support a claim about \"athletes\" as a whole.\n\n(d) Describe one specific change the company could make to carry out a fairer survey. Explain why your change would improve the survey.",
    "marks": 25,
    "minutes": 25,
    "answerKind": "written",
    "commandWord": {
      "word": "explain",
      "reminder": "Give clear reasons; for bias, attack from different angles (who, how, how many)."
    },
    "ribbons": [
      {
        "label": "(a) Correct percentage 90%",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(b) Reason 1: valid reason stated",
        "marks": 2,
        "kind": "explain"
      },
      {
        "label": "(b) Reason 1: explanation of effect on result",
        "marks": 3,
        "kind": "explain"
      },
      {
        "label": "(b) Reason 2: valid (different) reason stated",
        "marks": 2,
        "kind": "explain"
      },
      {
        "label": "(b) Reason 2: explanation of effect on result",
        "marks": 3,
        "kind": "explain"
      },
      {
        "label": "(c) States 20 is too small / not representative",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(c) Valid explanation (unreliable / cannot generalise / large effect per person)",
        "marks": 3,
        "kind": "explain"
      },
      {
        "label": "(d) States a specific, valid change",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(d) Explanation of why it improves the survey",
        "marks": 2,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "In part (b) students very often give two versions of the SAME reason — for example \"the question is unfair\" and \"the words are pushy\" — and lose half the marks because the examiner counts them as one point. Train yourself to attack a biased survey from DIFFERENT angles: (1) WHO was asked (the sample — biased, not random, vested interest), (2) HOW they were asked (the question — leading/loaded), and (3) HOW MANY were asked (sample size). One reason from each angle guarantees two distinct, creditworthy points.",
      "source": "2017 OL P2 Q8 (representative)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-3"
  },
  {
    "id": "maths-hl-1-1-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2018,
    "questionRef": "2018 HL P2 Q2 (representative)",
    "questionText": "The points A(−2, 5) and B(6, 1) are two vertices of a triangle in the coordinate plane.\n\n(a) Find the coordinates of M, the midpoint of [AB].\n\n(b) The line k is the perpendicular bisector of [AB]. Show that the equation of k is 2x − y − 1 = 0.\n\n(c) A third point, C(4, 7), is the remaining vertex of the triangle. Verify that C lies on the line k, and hence explain what this tells you about the lengths |CA| and |CB|.\n\n(d) Find the area of triangle ABC.\n\n(e) Find the perpendicular distance from the origin O(0, 0) to the line k. Give your answer in the form a√5⁄5, where a ∈ ℚ.",
    "marks": 25,
    "minutes": 25,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Work out the value or expression, showing your steps."
    },
    "ribbons": [
      {
        "label": "(a) Midpoint correct",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(b) Slope of AB and perpendicular slope (2), substituted through M to obtain stated equation",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(c) Correct substitution showing C on k AND correct conclusion |CA| = |CB| (isosceles)",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(d) Area formula applied correctly with right substitution → 20",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(e) Distance-from-point-to-line formula applied → √5/5",
        "marks": 5,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "In part (e) the most common error is forgetting that the perpendicular-distance formula requires the line in the form ax + by + c = 0 and then dividing by √(a² + b²) — students routinely divide by the wrong quantity (e.g. by a + b, or omit the square root). In part (b), \"Show that\" means you must derive the equation independently and arrive at the exact given form; just verifying a point satisfies it earns no marks.",
      "source": "2018 HL P2 Q2 (representative)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-1"
  },
  {
    "id": "maths-hl-1-1-3",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2019,
    "questionRef": "2019 HL P2 Q4 (representative)",
    "questionText": "A circle c has equation x² + y² − 6x + 4y − 12 = 0.\n\n(a) Find the coordinates of the centre and the length of the radius of c.\n\n(b) Verify that the point P(7, 1) lies on the circle c, and find the equation of the tangent to c at P. Give your answer in the form ax + by + d = 0, where a, b, d ∈ ℤ.\n\n(c) The line L: x − 2y − 2 = 0 intersects the circle c at two points. Find the coordinates of these two points of intersection.\n\n(d) Hence, or otherwise, find the length of the chord that L cuts on the circle, in the form k√5, k ∈ ℕ.",
    "marks": 30,
    "minutes": 30,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Work out the value or expression, showing your steps."
    },
    "ribbons": [
      {
        "label": "(a) Centre (3, −2) correct",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(a) Radius = 5 correct",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(b) Verify P on c AND obtain tangent slope −4/3 from perpendicular radius",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(b) Correct tangent equation 4x + 3y − 31 = 0 in required form",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(c) Substitute L into c, solve quadratic, both points found correctly",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(d) Correct chord length 4√5",
        "marks": 5,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "In part (b) candidates frequently use the slope of the radius directly as the tangent slope, forgetting the tangent is perpendicular to the radius at the point of contact (so they must take the negative reciprocal). In part (c) the most common loss of marks is solving the quadratic for one variable and then forgetting to back-substitute to find the partner coordinate — you must give full (x, y) coordinate pairs, not just the y-values. A quick sanity check (each found point should satisfy the original circle equation) catches sign slips.",
      "source": "2019 HL P2 Q4 (representative)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-1"
  },
  {
    "id": "maths-hl-1-3-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2017,
    "questionRef": "2017 HL P2 Q4 (representative)",
    "questionText": "A triangle has vertices A(2, 1), B(6, 1) and C(2, 4). A second triangle has vertices A′(−1, −2), B′(11, −2) and C′(−1, 7). The triangle ABC is mapped onto the triangle A′B′C′ by an enlargement.\n\n(a) Find the scale factor k of the enlargement.\n\n(b) Find the coordinates of the centre of enlargement O.\n\n(c) The area of triangle ABC is 6 square units. Find the area of triangle A′B′C′.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Work it out and give the result."
    },
    "ribbons": [
      {
        "label": "(a) Correct length of one object side AND its image side computed",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(a) Correct k = 3 from the ratio",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(b) Correct method/relation linking O, P and P′ via factor k set up",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(b) Correct O_x = 3.5",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(b) Correct O_y = 2.5",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(c) States/uses area factor k²",
        "marks": 1,
        "kind": "method"
      },
      {
        "label": "(c) Correct answer 54 square units",
        "marks": 2,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The most common error in part (b) is averaging the object and image coordinates or guessing the midpoint — students forget the centre is the unique fixed point and that O divides each ray in the ratio 1 : (k−1). Use the relation P′ − O = k(P − O) and solve for O; never assume the centre lies at the origin or at the midpoint of AA′. A second frequent slip is in (c): multiplying the area by k (=3) instead of k² (=9). Area always scales by the square of the linear scale factor.",
      "source": "LESSON"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-3"
  },
  {
    "id": "maths-hl-1-3-3",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2019,
    "questionRef": "2019 HL P2 Q3 (representative)",
    "questionText": "An enlargement has centre O(1, 2) and scale factor k = −2 (a negative scale factor, so the image appears on the opposite side of the centre and is inverted).\n\n(a) The point P has coordinates (4, 6). Find the coordinates of its image P′ under this enlargement.\n\n(b) A second point Q has image Q′(7, −4) under the same enlargement. Find the coordinates of Q.\n\n(c) A line segment in the object has length 5 cm. State the length of its image. State also, with a reason, whether the image segment is parallel to the object segment.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find / State",
      "reminder": "Work out P′ and Q; state the image length and parallel reason."
    },
    "ribbons": [
      {
        "label": "(a) Vector P − O found using P′ = O + k(P − O)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(a) Correct multiplication by −2",
        "marks": 1,
        "kind": "method"
      },
      {
        "label": "(a) Correct P′ = (−5, −6)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(b) Correct rearrangement Q = O + (Q′ − O)/k",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(b) Correct (Q′ − O)/k = (−3, 3)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(b) Correct Q = (−2, 5)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(c) Correct image length 10 cm using |k|",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(c) States parallel",
        "marks": 1,
        "kind": "explain"
      },
      {
        "label": "(c) Valid reason that enlargements preserve direction/slope",
        "marks": 1,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "With a negative scale factor students routinely make two errors. First, they treat k as if it were +2 and place the image on the same side of the centre as the object — you must keep the minus sign, so the image is on the opposite side and inverted. Second, for lengths and areas they forget that distance uses the magnitude |k| (here length multiplies by 2, area by k² = 4), since a length can never be negative. When working backwards from image to object (part b), divide by k including its sign — do not multiply — or you will land four times too far from the centre on the wrong side.",
      "source": "LESSON"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-3"
  },
  {
    "id": "maths-hl-4-0-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2017,
    "questionRef": "2017 HL P1 Q5 (representative)",
    "questionText": "The function f is defined for all real numbers x as f(x) = 2x² − 5x − 3.\n\n(a) Find f(−2).\n\n(b) Show that x = 3 is a root of f(x), and hence find the other value of x for which f(x) = 0.\n\n(c) The function g is defined for all real numbers x as g(x) = x + 1. Find an expression in x for the composite function f(g(x)), and write it in the form ax² + bx + c.",
    "marks": 25,
    "minutes": 25,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Work it out and give the result"
    },
    "ribbons": [
      {
        "label": "Correct substitution and evaluation f(−2) = 15",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "Shows f(3) = 0 by substitution",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "Correct factorisation / valid method to find second root",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "States other root x = −1/2",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Correct substitution f(x + 1) and expansion of (x + 1)²",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Correct simplified answer 2x² − x − 6",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "In part (c) the most common error is computing g(f(x)) instead of f(g(x)), or substituting only into the squared term and forgetting the linear term — students write 2(x+1)² − 5x − 3. The inner function must replace x EVERYWHERE in f, including the −5x term, giving −5(x+1). Always rewrite f with empty brackets first: f(▢) = 2(▢)² − 5(▢) − 3, then drop g(x) into every box.",
      "source": "LESSON"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-4-0"
  },
  {
    "id": "maths-hl-4-0-3",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2019,
    "questionRef": "2019 HL P1 Q4 (representative)",
    "questionText": "The function h is defined as h(x) = (3x − 4) / (x + 2), where x ∈ ℝ, x ≠ −2.\n\n(a) Evaluate h(0).\n\n(b) Find h⁻¹(x), the inverse function of h.\n\n(c) Using your answer to part (b), or otherwise, find the value of x for which h(x) = 5.\n\n(d) State the value of x that must be excluded from the domain of h⁻¹(x), and explain briefly why.",
    "marks": 25,
    "minutes": 25,
    "answerKind": "steps",
    "commandWord": {
      "word": "Find",
      "reminder": "Work it out and give the result"
    },
    "ribbons": [
      {
        "label": "Correct evaluation h(0) = −2",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Sets y = h(x) and clears the fraction (multiplies by x + 2)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Correctly gathers x-terms and factors out x",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "Correct inverse h⁻¹(x) = (−2x − 4)/(x − 3) (or equivalent)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Correct value x = −7 (by either method)",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "States x = 3 excluded with valid reason (denominator zero / not an output of h)",
        "marks": 3,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "In part (b) the classic mistake is failing to collect ALL the x-terms on one side before factoring — students leave an x on each side and cannot isolate it. After cross-multiplying you must move every term containing x to one side (yx − 3x) and everything else to the other, then factor x out as a common factor; you cannot \"divide across\" while x still appears in two places. A quick reliability check (verify h⁻¹ undoes h using the part (a) point) catches sign slips that are extremely common in rational inverses.",
      "source": "LESSON"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-4-0"
  }
];
