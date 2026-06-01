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
    "id": "maths-hl-0-0-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 HL P1 Q6(a)",
    "questionText": "Write down, in descending powers of p, the first 3 terms in the binomial expansion of:\n(2p + 3)⁷\nGive each term in its simplest form. For example, the first term should be of the form a p⁷, where a is a constant.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Write down",
      "reminder": "State the first three simplified terms; no extended working expected."
    },
    "ribbons": [
      {
        "label": "Set up the binomial terms with correct coefficients C(7,0), C(7,1), C(7,2) and powers of (2p) and 3",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Evaluate the first term 128p⁷ and one further term correctly",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Give all three simplified terms: 128p⁷ + 1344p⁶ + 6048p⁵",
        "marks": 2,
        "kind": "srp"
      }
    ],
    "lesson": {
      "text": "A frequent error is mishandling the (2p) so the powers of 2 are dropped, or letting the powers in each term add to the wrong total. Each term must combine the binomial coefficient, the correct power of 2p, and the correct power of 3.",
      "source": "SEC 2025 HL Marking Scheme, Q6(a)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-0"
  },
  {
    "id": "maths-hl-0-0-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2024,
    "questionRef": "2024 HL P2 Q6(c)",
    "questionText": "In a co-ordinate diagram, 16 points are marked. These are all of the points of the form (m, n), where m, n ∈ N and m, n ≤ 4 (i.e. the 4×4 grid of points with each coordinate from 1 to 4).\n\nA pair of these points is picked at random.\n\n(i) How many different pairs of points can be picked from these 16 points?\n(ii) The two points that are picked are joined with a straight line. Find the probability that this line is horizontal.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "written",
    "commandWord": {
      "word": "Find",
      "reminder": "Count combinations, then count the horizontal-line favourable pairs."
    },
    "ribbons": [
      {
        "label": "(i) Number of pairs = C(16,2) = 120",
        "marks": 6,
        "kind": "method"
      },
      {
        "label": "(ii) Horizontal pairs: choose 2 of 4 points in a row, × 4 rows = C(4,2)×4 = 24",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(ii) Probability = 24/120 = 1/5",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Pairs treated as ordered in one part and unordered in the other → HPC at most",
        "marks": 0,
        "kind": "gate"
      }
    ],
    "lesson": {
      "text": "A horizontal line needs both points in the same row (same y-value): there are 4 rows and C(4,2)=6 pairs per row, giving 24 favourable out of C(16,2)=120. Whether you count pairs as ordered or unordered, be consistent across both parts or the probability is penalised.",
      "source": "SEC 2024 HL Marking Scheme, Q6(c)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-0"
  },
  {
    "id": "maths-ol-0-0-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2025,
    "questionRef": "2025 OL P2 Q10(b)",
    "questionText": "Point A is the start and end point for all swims. There are six markers A, B, C, D, E, and F.\n\n(ii) Aoibhe wants to swim, starting at A, to each of the five markers (B, C, D, E, and F) once and only once and finishing back at A. Work out how many such routes are possible.\n\n(iii) On a particular day Aoibhe wants to start at A, swim to two markers other than A, and then return to A (for example, A to E to B to A). Work out how many such routes are possible.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Work out",
      "reminder": "Count the arrangements."
    },
    "ribbons": [
      {
        "label": "Number of full routes = 5! ",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "5! = 120 routes",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Two-marker routes = 5 x 4 (or 5P2)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "= 20 routes",
        "marks": 2,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "Visiting all five markers once is an arrangement of 5 items: 5! = 120. Choosing and ordering 2 of the 5 markers is 5P2 = 5 x 4 = 20 - order matters here because A-E-B and A-B-E are different routes.",
      "source": "SEC 2025 OL Marking Scheme, Q10(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-0"
  },
  {
    "id": "maths-ol-0-0-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2024,
    "questionRef": "2024 OL P2 Q9(a)(i)(ii)",
    "questionText": "Diarmuid sells ice cream with 7 different flavours, 4 different toppings, and 2 containers (a cone or a tub).\n(i) How many different choices are available if you must choose only one flavour, one topping, and either a cone or a tub?\n(ii) Diarmuid wants to maximise the number of choices available to his customers. He can only add either an extra flavour or an extra topping. Should he add an extra flavour or an extra topping? Use calculations to support your answer.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "written",
    "commandWord": {
      "word": "Use calculations to support",
      "reminder": "Count with the multiplication principle, then compare both options numerically before deciding."
    },
    "ribbons": [
      {
        "label": "Work of merit, e.g. some relevant multiplication in (i) or (ii), or correct box ticked without justification",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "Work of merit in (i) AND (ii), or one part correct",
        "marks": 2,
        "kind": "srp"
      },
      {
        "label": "(i) 7 × 4 × 2 = 56",
        "marks": 5,
        "kind": "srp"
      },
      {
        "label": "(ii) Extra topping: 7 × 5 × 2 = 70 beats extra flavour: 8 × 4 × 2 = 64, so add an extra topping",
        "marks": 5,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "Use the fundamental counting principle (multiply the options): 7 × 4 × 2 = 56. To decide, compute both alternatives — an extra topping (70) beats an extra flavour (64) — because multiplying by the smaller current factor gains more.",
      "source": "SEC 2024 OL Marking Scheme, Q9(a)(i)(ii)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-0"
  },
  {
    "id": "maths-hl-0-1-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 HL P2 Q3(a)",
    "questionText": "240 people were surveyed about which of three countries, A, B, or C, they had been to. A Venn diagram shows the number of people who had been to each combination. The region counts are: only A = 23, only B = 56, only C = 41, A∩B only = 18, A∩C only = 13, B∩C only = 16, A∩B∩C = 6, and none of the three = 67. (So the universal set has 240 people.) The event A is the event that a person picked at random from the 240 had been to country A, and so on. (i) Show that P(A) = 1/4. (ii) Verify that, for the values in this diagram: P(A∪C) = P(A) + P(C) − P(A∩C). (iii) Are A and B independent events? Use calculations to justify your answer.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "written",
    "commandWord": {
      "word": "Show / Verify / Justify",
      "reminder": "Demonstrate each result with calculations."
    },
    "ribbons": [
      {
        "label": "(i) Show P(A) = (23+18+6+13)/240 = 60/240 = 1/4",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(ii) Find P(A∪C) = 117/240, P(C) = 76/240, P(A∩C) = 19/240 and verify the sum",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(iii) Compute P(A∩B) = 24/240 = 1/10 and P(A)×P(B) = (1/4)(2/5) = 1/10, conclude YES independent",
        "marks": 5,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "For independence you must test P(A∩B) = P(A)×P(B) (or P(A|B) = P(A)) with actual numbers — a verbal claim with no calculation scores Low Partial Credit at most; here both equal 1/10 so the events ARE independent.",
      "source": "SEC 2025 HL Marking Scheme, Q3(a)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-1"
  },
  {
    "id": "maths-hl-0-1-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2024,
    "questionRef": "2024 HL P2 Q2(c)",
    "questionText": "C and D are two other events, with universal set U.\nP(C) = 0·5 and P(D) = 0·7.\n\nFind the maximum value of P[(C∪D)′].\n\nNote: (C∪D)′ is the complement of the set C∪D in the set U.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Find",
      "reminder": "Maximise the complement by minimising C∪D."
    },
    "ribbons": [
      {
        "label": "Recognise: to maximise (C∪D)′ minimise C∪D, i.e. maximise C∩D (one set subset of the other)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "C∩D = 0·5 so C∪D = 0·7",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Max P[(C∪D)′] = 1 − 0·7 = 0·3",
        "marks": 4,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The complement of C∪D is largest when C∪D is smallest, which happens when C is entirely inside D (maximum overlap). Then C∪D = P(D) = 0·7 and the complement is 0·3. Students who assume independence or add the probabilities go wrong.",
      "source": "SEC 2024 HL Marking Scheme, Q2(c)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-1"
  },
  {
    "id": "maths-ol-0-1-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2024,
    "questionRef": "2024 OL P2 Q2(c)(d)",
    "questionText": "Seán is playing a game with 14 cards. 7 of the cards are green (G), numbered 1 to 7. The other 7 cards are red (R), numbered 1 to 7.\n(c) Seán picks a card at random and doesn't replace it. It is Red 5 (R5). He then picks a second card at random. What is the probability that the second card is a green card?\n(d) Seán puts back the two cards. Seán then picks a card at random and doesn't replace it. He then picks a second card at random. Find the probability that the second card is a different colour and a different number from the first card.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "written",
    "commandWord": {
      "word": "Find",
      "reminder": "State each probability as a fraction with supporting reasoning."
    },
    "ribbons": [
      {
        "label": "Work of merit, e.g. 7 or 13 correctly placed in (c), or 6 or 13 correctly placed in (d), or a relevant partial listing",
        "marks": 4,
        "kind": "attempt"
      },
      {
        "label": "Part (c) or part (d) correct (one part fully right)",
        "marks": 4,
        "kind": "srp"
      },
      {
        "label": "(c) Second card green = 7/13 (after R5 removed, 7 greens remain of 13 cards)",
        "marks": 3,
        "kind": "srp"
      },
      {
        "label": "(d) Different colour and different number = 6/13",
        "marks": 4,
        "kind": "srp"
      }
    ],
    "lesson": {
      "text": "After one card is removed, the denominator drops to 13. In (d), once the first card is fixed, exactly 6 of the remaining 13 cards have both a different colour AND a different number (the 7 of the other colour, minus the one sharing the first card's number).",
      "source": "SEC 2024 OL Marking Scheme, Q2(c)(d)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-1"
  },
  {
    "id": "maths-ol-0-1-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2022,
    "questionRef": "2022 OL P2 Q7(b)",
    "questionText": "The table below shows the breakdown of the animals in an animal shelter, by type of animal (cat or dog) and by sex (male or female), on a particular Monday.\n            Male   Female   Total\nCats         5       9       14\nDogs        11       ?        ?\nTotal        ?       ?       40\n\nComplete the table by filling in the four missing values.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Complete",
      "reminder": "Use row and column totals: each row/column must sum to the given total."
    },
    "ribbons": [
      {
        "label": "Female Dogs = 15 (since total animals 40 − 14 cats = 26 dogs; 26 − 11 = 15)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Total Dogs = 26",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Total Male = 16 (5 + 11)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Total Female = 24 (9 + 15)",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "In a two-way table every row and column must add to its total and the grand total (40) ties everything together. Start from a row or column with two known entries: 40 total − 14 cats = 26 dogs, then 26 − 11 male dogs = 15 female dogs, and complete the column totals. Marks here are awarded for consistent work, so check your row and column sums.",
      "source": "SEC 2022 OL Marking Scheme, Q7(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-1"
  },
  {
    "id": "maths-hl-0-2-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 HL P2 Q10(e)",
    "questionText": "For one question on a test, students are given a mark of 0, 1, 2, or 3. The proportion of students who get each mark is: mark 0 → 0·19; mark 1 → p; mark 2 → 2r; mark 3 → r, where p, r ∈ R and p, r ≥ 0. A student is picked at random. The expected value of their mark will depend on the values of p and r. Find the largest value that the expected value of their mark could be.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "written",
    "commandWord": {
      "word": "Find",
      "reminder": "Maximise the expected value."
    },
    "ribbons": [
      {
        "label": "Recognise that to maximise E[X] you set p = 0 (mass moved to higher marks)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Use total probability = 1: 0·19 + 0 + 2r + r = 1, so 3r = 0·81",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Solve r = 0·27",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Compute E[X]max = 0(0·19) + 1(0) + 2(0·54) + 3(0·27) = 1·89",
        "marks": 5,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "Because mark 1 carries the lowest non-zero weight in the expectation, you maximise E[X] by setting p = 0 and pushing all remaining probability onto the higher marks; the constraint that probabilities sum to 1 then fixes r = 0·27, giving E[X]max = 1·89.",
      "source": "SEC 2025 HL Marking Scheme, Q10(e)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-2"
  },
  {
    "id": "maths-hl-0-2-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2024,
    "questionRef": "2024 HL P2 Q2(a)",
    "questionText": "The table below shows the prizes, in euro, that a player can win in a game, as well as the probability of winning each prize. The player wins at most one prize each time that she plays. Some of the prizes are given in terms of x ∈ R.\n\nPrize (€):     None    2      x−10    x\nProbability:   30%     40%    28%     2%\n\nIt costs €10 to play the game once. The game is fair – that is, the expected value of the winnings, taking the cost into account, is €0.\n\nWork out the value of x.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Work out",
      "reminder": "Set up the expected value equation and solve for x."
    },
    "ribbons": [
      {
        "label": "Form E(X): (0)(0·3) + (2)(0·4) + (x−10)(0·28) + (x)(0·02) = 10",
        "marks": 6,
        "kind": "method"
      },
      {
        "label": "Simplify to 0·3x = 12 and solve to get x = 40",
        "marks": 4,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "A 'fair' game means the expected winnings equal the cost (€10), so set the sum of prize×probability equal to 10 rather than to 0. High partial credit needs the fully correct expected-value equation before any simplification.",
      "source": "SEC 2024 HL Marking Scheme, Q2(a)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-2"
  },
  {
    "id": "maths-ol-0-2-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2025,
    "questionRef": "2025 OL P2 Q7(b)",
    "questionText": "Sarah plays tennis. Each time that Sarah plays a service game, the probability that she wins is 0.78. Assume that winning each service game is independent.\n\n(i) What is the probability that Sarah will lose her next service game (that is, that she won't win her next service game)?\n\n(ii) What is the probability that the first service game that Sarah loses is her third service game? Give your answer correct to 3 decimal places.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Find (What is the probability)",
      "reminder": "Calculate the probabilities."
    },
    "ribbons": [
      {
        "label": "P(loses a service game) = 1 - 0.78 = 0.22",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Set up P(win, win, lose) = 0.78 x 0.78 x 0.22",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "= 0.133848 = 0.134 (3 d.p.)",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "For the first loss to be the third game, Sarah must win the first two and lose the third: 0.78 x 0.78 x 0.22 = 0.134. A common error is to use 0.22 three times or to forget that the first two games must be wins.",
      "source": "SEC 2025 OL Marking Scheme, Q7(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-2"
  },
  {
    "id": "maths-ol-0-2-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2024,
    "questionRef": "2024 OL P2 Q5(b)(i)(ii)",
    "questionText": "Owen records the number of hours of sleep that he gets each night for several weeks. Based on this, he calculates that he gets the recommended amount of sleep 10% of the time.\n(i) What is the probability that he does not get the recommended amount of sleep on a particular night?\n(ii) Beginning on a Sunday night, Owen records his sleep each night for a week. Find the probability that Owen gets the recommended amount of sleep for the first time on Tuesday night (the third night). Assume that the number of hours of sleep Owen gets on different nights are independent.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "written",
    "commandWord": {
      "word": "Find",
      "reminder": "Give each probability with the multiplication of independent events shown."
    },
    "ribbons": [
      {
        "label": "Work of merit in (i) (mentions 1) or in (ii) (two relevant probabilities multiplied)",
        "marks": 4,
        "kind": "attempt"
      },
      {
        "label": "Work of merit in (i) AND (ii), or one part fully correct",
        "marks": 2,
        "kind": "srp"
      },
      {
        "label": "(i) P(not recommended) = 1 − 0·1 = 0·9 (90%)",
        "marks": 5,
        "kind": "srp"
      },
      {
        "label": "(ii) P = (0·9)(0·9)(0·1) = 0·081 (8·1%)",
        "marks": 4,
        "kind": "srp"
      }
    ],
    "lesson": {
      "text": "'First time on the third night' means fail, fail, then succeed: (0·9)(0·9)(0·1) = 0·081. The two earlier nights must NOT be recommended, so you multiply two 0·9s before the single 0·1.",
      "source": "SEC 2024 OL Marking Scheme, Q5(b)(i)(ii)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-2"
  },
  {
    "id": "maths-hl-0-3-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2024,
    "questionRef": "2024 HL P2 Q7(d)",
    "questionText": "In 2020, PK Hotels were rated the best hotel chain in Europe by 75% of their customers.\n\nIn 2024, PK Hotels carried out a survey of a random sample of 1000 of their customers to see if this percentage had changed. Of these, 765 rated PK Hotels the best hotel chain in Europe.\n\nCarry out a hypothesis test at the 5% level of significance to see if this shows a change in the percentage of their customers who rate PK Hotels the best chain in Europe.\n\nState your null hypothesis and your alternative hypothesis, state your conclusion, and give a reason for your conclusion.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "steps",
    "commandWord": {
      "word": "Carry out",
      "reminder": "\"Carry out a hypothesis test\" requires the full four-part structure — H0, H1, conclusion, reason — and the reason must be based on relevant calculations, not just asserted."
    },
    "ribbons": [
      {
        "label": "Work of merit in one step (e.g. one hypothesis, or the sample proportion 0·765, or a relevant substitution)",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "Two of the four steps correct",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Three of the four steps correct",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "All four steps: H0 (p = 0·75), H1 (p ≠ 0·75), conclusion (fail to reject H0 / percentage has not changed), and reason (0·75 lies inside the interval 0·7334 < p < 0·7966)",
        "marks": 3,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "This is a proportion hypothesis test using the quick margin of error E = 1/√n = 1/√1000 ≈ 0·0316, giving the interval 0·765 ± 0·0316 = (0·7334, 0·7966). Because 0·75 falls inside that interval, the verdict is the opposite of the previous two questions — you fail to reject H0, so 'the percentage has not changed'. Students primed to 'find a difference' often force a rejection; the marking scheme rewards correctly concluding no change. The scheme also accepts the more accurate margin 1·96√(p̂(1−p̂)/n) instead of 1/√n. The most important rule it states: 'if either a confidence interval or test statistic is not found, a conclusion cannot be drawn' — and if your hypotheses are wrong, the conclusion step is capped at Mid Partial Credit even if everything downstream is right. The reason must name the calculation: '0·75 is within the interval'.",
      "source": "SEC 2024 HL Marking Scheme, Q7(d)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-3"
  },
  {
    "id": "maths-hl-0-3-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2023,
    "questionRef": "2023 HL P2 Q8(b)",
    "questionText": "In Ireland, players' scores in an online word game are approximately normally distributed, with a mean of 3·87 and a standard deviation of 0·36.\n\nA random sample of 64 Galway players has a mean score of 3·74. Based on this, a local newspaper claims that Galway players have a different mean score to players in Ireland.\n\n(i) Use the information about this sample to construct a 95% confidence interval for the mean score of all Galway players. Use the standard deviation of 0·36 in your calculations.\n\n(ii) Carry out a hypothesis test at the 5% level of significance to test the newspaper's claim that Galway players have a different mean score to players in Ireland.\n\nState your null hypothesis, state your alternative hypothesis, state your conclusion, and give a reason for your conclusion.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "steps",
    "commandWord": {
      "word": "Construct / Carry out",
      "reminder": "\"Construct a confidence interval\" means build the interval from the formula with full substitution shown; \"Carry out a hypothesis test\" means you must produce all four parts — H0, H1, a conclusion, and a reason tied to your calculations — not just a yes/no."
    },
    "ribbons": [
      {
        "label": "Some correct substitution into the confidence-interval formula",
        "marks": 4,
        "kind": "attempt"
      },
      {
        "label": "Confidence interval fully substituted (or one endpoint found)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Both endpoints of the 95% interval found correctly",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "State H0 and H1 correctly",
        "marks": 2,
        "kind": "name"
      },
      {
        "label": "Reach the correct conclusion with a matching reason (3·87 not in the interval, or z = −2·89 in the rejection region)",
        "marks": 3,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "This is the model 'statistically aware consumer' question: a newspaper makes a claim and you test it. The marking scheme awards the four hypothesis-test parts (H0, H1, conclusion, reason) as a unit and notes that a conclusion is 'not considered correct without some relevant calculations' — so the verdict 'Galway players are different' earns nothing unless you have already shown 3·87 falls outside [3·6518, 3·8282] or that z = −2·89 sits beyond −1·96. The scheme also says 'If H0 and H1 are reversed, treat as one error', so swapping them costs only one mark, but inventing a one-sided alternative when the claim is 'different' breaks the test. Crucially, the confidence interval in (i) is the engine for (ii): if you build it correctly you can answer (ii) by simply observing the population mean 3·87 lies outside it.",
      "source": "SEC 2023 HL Marking Scheme, Q8(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-3"
  },
  {
    "id": "maths-ol-0-3-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2025,
    "questionRef": "2025 OL P1 Q7(c)",
    "questionText": "Later in the year, Liam predicts the value of one share. The error in his prediction is €1·50, which is a percentage error of 16·3%. Find the value of one share at this time. Give your answer correct to the nearest cent.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Find",
      "reminder": "Percentage error = error ÷ true value; rearrange for true value."
    },
    "ribbons": [
      {
        "label": "Correct relationship: 1·50 / true value = 0·163",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Rearrange to true value = 1·50 ÷ 0·163",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Evaluate to €9·20 (accept €9·18 to €9·23)",
        "marks": 3,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "Percentage error is the error as a fraction of the TRUE value, so true value = 1·50 ÷ 0·163 ≈ €9·20. Forming the equation 1·50/true value = 0·163 earns high partial credit.",
      "source": "SEC 2025 OL Marking Scheme, Q7(c)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-3"
  },
  {
    "id": "maths-ol-0-3-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2023,
    "questionRef": "2023 OL P2 Q9(b)(i)",
    "questionText": "A random sample of 500 students in Cork took a statistics test. 61 of these students were given a rating of Excellent. Work out the percentage of students in this sample who were given a rating of Excellent.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Work out",
      "reminder": "Convert the proportion to a percentage"
    },
    "ribbons": [
      {
        "label": "Form the proportion p-hat = 61/500",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Multiply by 100: 0.122 x 100",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "State 12.2%",
        "marks": 4,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The sample proportion is 61/500 = 0.122, and multiplying by 100 gives 12.2%. Keep the full decimal before converting so you can quote it to one decimal place.",
      "source": "SEC 2023 OL Marking Scheme, Q9(b)(i)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-3"
  },
  {
    "id": "maths-hl-0-4-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 HL P2 Q10(d)",
    "questionText": "In country Z, 50% of all students have a pet in their home and 50% do not. A sample of 2520 students is taken from country Z. Describe how the sample of 2520 students could be taken as a stratified random sample with respect to having a pet in the home, and explain why it is probably not useful to do this when looking at these students' maths scores.",
    "marks": 5,
    "minutes": 5,
    "answerKind": "written",
    "commandWord": {
      "word": "Describe / Explain",
      "reminder": "Describe the method and explain why it is not useful."
    },
    "ribbons": [
      {
        "label": "How to: from all students who own a pet take a random sample of 2520/2 = 1260, and from all who do not own a pet take a random sample of 1260",
        "marks": 3,
        "kind": "explain"
      },
      {
        "label": "Why not useful: there is probably no connection between owning a pet and maths scores",
        "marks": 2,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "Stratified sampling means splitting the population into strata (pet / no pet) and taking a random sample from each in proportion to the strata sizes (here 1260 from each); it is only worthwhile when the stratifying variable relates to what you're measuring, and pet ownership has no plausible link to maths scores. Omitting 'random' selection is a Full Credit −1.",
      "source": "SEC 2025 HL Marking Scheme, Q10(d)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-4"
  },
  {
    "id": "maths-hl-0-4-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 HL P2 Q10(d)",
    "questionText": "In country Z, 50% of all students have a pet in their home and 50% do not.\n\nDescribe how the sample of 2520 students from country Z could be taken as a stratified random sample with respect to having a pet in the home, and explain why it is probably not useful to do this when looking at these students' maths scores.\n\nHow to take as a stratified random sample:\n\nWhy this would not be useful:",
    "marks": 5,
    "minutes": 5,
    "answerKind": "written",
    "commandWord": {
      "word": "Describe / explain",
      "reminder": "Two distinct command words in one part. 'Describe how' wants the actual mechanism of stratified random sampling (split the population into the two strata, then RANDOMLY sample from each in proportion); 'explain why' wants a reason grounded in the context (no plausible link between pet ownership and maths score). Each command word earns its own marks - answering only one caps you at 2 of 5."
    },
    "ribbons": [
      {
        "label": "Method: split into the two strata (pet / no pet) and take a random sample of 2520/2 = 1260 from each",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Explain: pet ownership probably has no connection with maths scores, so stratifying by it gains nothing",
        "marks": 2,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "This is a Scale 5B question (marks of 0, 2 or 5), so there is effectively no half-credit middle ground - you either land most of it or you scrape a Partial Credit of 2. The marking scheme awards that Partial Credit of 2 for 'a general explanation of how to carry out stratified random sampling' OR for getting just one of the two parts right; full marks need BOTH the method and the 'why not useful' reason. Two things separate a full-credit answer here. First, the word 'random' is load-bearing: the scheme applies a Full Credit -1 penalty if 'random selection is not mentioned' - describing the 50/50 split into strata without saying you then sample randomly within each stratum costs you a mark. The model answer is explicit: 'From all students who own a pet... take a random sample of 1260. From all students who do not own a pet, do the same.' Second, the 'why not useful' half is a one-liner that must name the missing link, not waffle: the scheme accepts 'Probably no connection between owning a pet and maths scores.' Candidates who can execute confidence intervals and hypothesis tests (parts a-c of this same question) routinely drop marks on this 5-mark sampling part because it tests the data-collection design skill, not calculation - stratifying is only worthwhile when the stratifying variable is expected to relate to what you are measuring.",
      "source": "SEC 2025 HL Marking Scheme, Q10(d)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-4"
  },
  {
    "id": "maths-ol-0-4-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2023,
    "questionRef": "2023 OL P2 Q9(a)(iii)",
    "questionText": "A group of students investigated the average reading time of students in Ireland. One Monday morning, they asked the first 200 students who came into their school how long, on average, they spend reading each day. Explain why the method of choosing the students for this survey could limit the validity of the conclusions.",
    "marks": 5,
    "minutes": 5,
    "answerKind": "written",
    "commandWord": {
      "word": "Explain",
      "reminder": "Identify a sampling bias in the method"
    },
    "ribbons": [
      {
        "label": "Identify a sampling-bias issue, e.g. only early-arriving students sampled",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Link it to non-representativeness of Irish students generally",
        "marks": 2,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The sample is biased: the first 200 students might be local pupils or those arriving by bus, leaving out latecomers, and one school cannot represent all of Ireland. Name a specific selection-bias reason rather than a vague 'too small' comment.",
      "source": "SEC 2023 OL Marking Scheme, Q9(a)(iii)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-4"
  },
  {
    "id": "maths-ol-0-4-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2022,
    "questionRef": "2022 OL P2 Q10(a)",
    "questionText": "A survey was carried out to investigate the amount and type of exercise that adults in Ireland are taking in 2022. This survey was carried out on a sample of adults in Ireland.\n\nWrite down one advantage and one disadvantage of carrying out a survey on a sample instead of a population.",
    "marks": 5,
    "minutes": 5,
    "answerKind": "written",
    "commandWord": {
      "word": "Write down",
      "reminder": "State one valid advantage and one valid disadvantage of sampling."
    },
    "ribbons": [
      {
        "label": "One valid advantage of sampling (e.g. cheaper, faster, more practical)",
        "marks": 3,
        "kind": "explain"
      },
      {
        "label": "One valid disadvantage of sampling (e.g. less accurate, sampling bias)",
        "marks": 2,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "Sampling trades completeness for practicality: an advantage is that it is cheaper, faster or more practical than surveying the whole population; a disadvantage is that it is less accurate and can suffer from sampling bias. Partial credit is given for just one of the two, so always give both.",
      "source": "SEC 2022 OL Marking Scheme, Q10(a)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-4"
  },
  {
    "id": "maths-hl-0-5-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 HL P2 Q4(a)",
    "questionText": "The ages of twelve people in a class are given below, in ascending order, where x ∈ N: 11, 12, 12, 14, 15, x, 18, 18, 19, 22, 25, 30. (i) The median age is 17·5. Find the value of x. (ii) The first quartile (Q1) is 13. Work out the interquartile range of the ages.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "written",
    "commandWord": {
      "word": "Find / Work out",
      "reminder": "Calculate the value, showing work."
    },
    "ribbons": [
      {
        "label": "(i) Median = (x + 18)/2, set equal to 17·5 and solve for x = 17",
        "marks": 6,
        "kind": "method"
      },
      {
        "label": "(ii) Q3 = (19 + 22)/2 = 20·5",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(ii) IQR = Q3 − Q1 = 20·5 − 13 = 7·5",
        "marks": 4,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "With 12 values the median is the average of the 6th and 7th values, so the median equation is (x + 18)/2 = 17·5; the upper quartile is the median of the top six values, the average of the 9th and 10th values (19 and 22).",
      "source": "SEC 2025 HL Marking Scheme, Q4(a)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-5"
  },
  {
    "id": "maths-hl-0-5-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2024,
    "questionRef": "2024 HL P2 Q1(a)",
    "questionText": "A group of 22 students was tested to see how far, in metres, each of them could swim without stopping for a rest. The results of the testing are shown in the ordered stem and leaf plot below. Four of the entries have been replaced with the letters a, b, c, and d.\n\n2 | b 2 7\n3 | a 4 4 5 8\n4 | 0 1 d 5 6 9\n5 | 2 3 7 7 8\n6 | 1 8 c\n\nKey: 2|7 = 27 metres\n\n(i) The mode of the data is 34 metres. Use this to write down the value of a.\n(ii) The range of the data is 49 metres. Use this to find the value of b and the value of c.\n(iii) The median of the data is 43·5 metres. Use this to find the value of d.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "written",
    "commandWord": {
      "word": "find",
      "reminder": "Work out the value, showing how each statistic determines the missing digit."
    },
    "ribbons": [
      {
        "label": "Mode = 34, so a = 4",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Range = 49 (69 − 20), so b = 0 and c = 9",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "Median between '4d' and 45: ('4d' + 45)/2 = 43·5, so '4d' = 42, d = 2",
        "marks": 6,
        "kind": "method"
      },
      {
        "label": "Give the second digit only (not both digits) in parts (ii) and (iii)",
        "marks": 0,
        "kind": "gate"
      }
    ],
    "lesson": {
      "text": "Each statistic pins down exactly one missing digit: the mode fixes the repeated leaf, the range fixes the smallest and largest leaves, and the median for 22 values is the mean of the 11th and 12th ordered values. Examiners apply a * if you write both digits of a stem-and-leaf entry instead of just the leaf.",
      "source": "SEC 2024 HL Marking Scheme, Q1(a)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-5"
  },
  {
    "id": "maths-ol-0-5-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2025,
    "questionRef": "2025 OL P2 Q1(a)",
    "questionText": "The table below shows the total monthly rainfall for Athenry for 2023. Each value is rounded to the nearest mm.\n\nMonth: Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sept, Oct, Nov, Dec\nTotal rainfall (mm): 114, 42, 186, 93, 64, 94, 224, 129, 148, 180, 114, 203\n\n(i) The total rainfall in Athenry for June 2023 was 94 mm. The total rainfall in Athenry for June 2024 was 72 mm. Find the percentage decrease in rainfall from June 2023 to June 2024. Give your answer correct to 1 decimal place.\n\n(ii) Work out the mean and the standard deviation of the total monthly rainfall for Athenry from the table above. Give both answers correct to the nearest whole number.\nMean = _____________\nStandard deviation = ____________",
    "marks": 20,
    "minutes": 20,
    "answerKind": "written",
    "commandWord": {
      "word": "Find / Work out",
      "reminder": "Calculate and show the working."
    },
    "ribbons": [
      {
        "label": "Find difference 94 - 72 = 22 and set up fraction 22/94",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Percentage decrease = 22/94 x 100 = 23.4%",
        "marks": 6,
        "kind": "method"
      },
      {
        "label": "Mean of the 12 values = 133 mm (nearest whole number)",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "Standard deviation = 54 mm (nearest whole number)",
        "marks": 5,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "For the percentage decrease the original (2023) value 94 must be the denominator, not the new value: 22/94 x 100 = 23.4%. For (ii), the marking scheme awards High Partial for just one correct answer or one correctly substituted formula, and applies a star (Full Credit -1) for no/incorrect rounding or missing units.",
      "source": "SEC 2025 OL Marking Scheme, Q1(a)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-5"
  },
  {
    "id": "maths-ol-0-5-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2024,
    "questionRef": "2024 OL P2 Q1(b)",
    "questionText": "A different group of five students did a maths question. Their scores were as follows, where t ∈ N:\n15, 16, 19, t, 26\nThe mean of the five scores is 19·6.\nWork out the value of t.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Work out",
      "reminder": "Show the working that leads to t; a bare answer earns only the lowest non-zero credit."
    },
    "ribbons": [
      {
        "label": "Write/use the correct mean formula: (15 + 16 + 19 + t + 26)/5 = 19·6",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Fully substitute and reduce to 76 + t = 98",
        "marks": 2,
        "kind": "srp"
      },
      {
        "label": "Solve to get t = 22",
        "marks": 4,
        "kind": "srp"
      }
    ],
    "lesson": {
      "text": "Multiply the mean by the number of values to get the total (19·6 × 5 = 98), then subtract the known scores (76) to isolate t = 22. Setting up the equation as sum/5 = 19·6 is the key step the scheme rewards.",
      "source": "SEC 2024 OL Marking Scheme, Q1(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-5"
  },
  {
    "id": "maths-hl-0-6-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 HL P2 Q10(a)(ii)",
    "questionText": "Worldwide, scores on a maths test are normally distributed with a mean score of 400 and a standard deviation of 60. Use the normal distribution to work out the proportion of students worldwide who would score above 420 on the test. Give your answer correct to 2 decimal places.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Work out",
      "reminder": "Use the normal distribution, give to 2 d.p."
    },
    "ribbons": [
      {
        "label": "Find z-score: z = (420 − 400)/60 = 1/3 = 0·33",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Find P(z < 0·33) = 0·6293 from tables",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "P(score > 420) = 1 − 0·6293 = 0·37 (2 d.p.)",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "Standardise with z = (x − μ)/σ = 20/60 = 0·33, look up Φ(0·33) = 0·6293, then subtract from 1 because the question asks for 'above'. Forgetting the final 1 − Φ step gives the proportion below 420 instead.",
      "source": "SEC 2025 HL Marking Scheme, Q10(a)(ii)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-6"
  },
  {
    "id": "maths-hl-0-6-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2024,
    "questionRef": "2024 HL P2 Q7(a)",
    "questionText": "PK Hotels is a hotel chain in Europe. The ages of the people who stayed in a PK Hotel in 2023 are roughly normally distributed, with a mean age of 48·2 years and a standard deviation of 10·6 years.\n\n(i) One person is picked at random from the people who stayed in a PK Hotel in 2023. Find the probability that this person is less than 50 years old.\n\n(ii) Exactly 10% of people who stayed in a PK Hotel in 2023 are at least A years old. Find the value of A, correct to the nearest whole number.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "written",
    "commandWord": {
      "word": "Find",
      "reminder": "Standardise to z-scores using the tables booklet."
    },
    "ribbons": [
      {
        "label": "(i) z = (50−48·2)/10·6 = 0·17 and P(z<0·17) = 0·5675",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(ii) Top 10% means 90% below A, so z = 1·28 (or 1·29)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(ii) Solve 1·28 = (A−48·2)/10·6 for A",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(ii) A = 62 (nearest whole number)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Incorrect or no rounding",
        "marks": 0,
        "kind": "gate"
      }
    ],
    "lesson": {
      "text": "For the 'at least A, top 10%' part, look up the z-value for 0·90 (= 1·28), not 0·10 — the table gives area to the left. Reversing this is the standard error in inverse-normal questions.",
      "source": "SEC 2024 HL Marking Scheme, Q7(a)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-6"
  },
  {
    "id": "maths-ol-0-6-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2024,
    "questionRef": "2024 OL P2 Q5(a)(ii)",
    "questionText": "A large group of 17-year-olds had hours of sleep that were normally distributed, with the middle 68% sleeping between 7·2 and 8·4 hours (so the mean is 7·8 hours and the standard deviation is 0·6 hours). Research says that a 17-year-old should get at least 9 hours of sleep each night. Using the empirical rule, what percentage of this sample got at least 9 hours of sleep on the previous night?",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "What percentage",
      "reminder": "Use the empirical rule percentages; show how you reach the tail value."
    },
    "ribbons": [
      {
        "label": "Work of merit, e.g. shades the correct area, writes μ + 2σ, or 95% (work of merit)",
        "marks": 4,
        "kind": "attempt"
      },
      {
        "label": "Reaches 5% or 97·5% (the value at μ + 2σ)",
        "marks": 1,
        "kind": "srp"
      },
      {
        "label": "100% − 97·5% = 2·5%",
        "marks": 5,
        "kind": "srp"
      }
    ],
    "lesson": {
      "text": "9 hours is μ + 2σ (7·8 + 2 × 0·6). Under the empirical rule 97·5% lie below μ + 2σ, so the upper tail is 100% − 97·5% = 2·5%. Using a Z-score table instead of the empirical rule earns at most low credit here.",
      "source": "SEC 2024 OL Marking Scheme, Q5(a)(ii)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-6"
  },
  {
    "id": "maths-ol-0-6-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2022,
    "questionRef": "2022 OL P2 Q4(b)",
    "questionText": "A large group of people took a reading test. The scores were normally distributed, with a mean of 100 and a standard deviation of 20. Use the empirical rule to answer parts (i) and (ii).\n\n(i) What percentage of the people had scores between 80 and 120?\n\n(ii) The top 2.5% of scores were given a grade of 'Exceptional'. What was the least score that was needed to get this grade?",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Use the empirical rule",
      "reminder": "Apply the 68-95-99.7 rule: ±1σ ≈ 68%, ±2σ ≈ 95%."
    },
    "ribbons": [
      {
        "label": "(i) Recognises 80 to 120 is mean ± 1 standard deviation",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(i) Answer: 68%",
        "marks": 3,
        "kind": "evaluation"
      },
      {
        "label": "(ii) Recognises top 2.5% is above mean + 2 standard deviations (100 + 2×20)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "(ii) Least score = 140",
        "marks": 3,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "The empirical rule: about 68% of data lies within 1 standard deviation of the mean and about 95% within 2 standard deviations. Scores 80-120 are mean ±1σ = 68%. The top 2.5% sits beyond +2σ (since 95% lies within ±2σ, leaving 2.5% in each tail), so the cutoff is 100 + 2(20) = 140.",
      "source": "SEC 2022 OL Marking Scheme, Q4(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-0-6"
  },
  {
    "id": "maths-hl-1-0-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2024,
    "questionRef": "2024 HL P2 Q4(b)",
    "questionText": "Three lines are parallel. They cut off equal segments on one transversal line.\n\nProve that if three parallel lines cut off equal segments on some transversal line, then they will cut off equal segments on any other transversal.\n\nGive a reason for each statement that you make in your proof, as appropriate.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "written",
    "commandWord": {
      "word": "Prove",
      "reminder": "This is a named curriculum theorem — \"Prove\" here means reproduce the standard proof, including the construction line and a justification at every step. The scheme explicitly bands answers by how many steps carry a reason, so unjustified statements cap your mark."
    },
    "ribbons": [
      {
        "label": "Work of merit: correct construction indicated, parallelograms identified, or reference to congruency",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Construction plus 2 correct steps establishing congruency of the two triangles (no justifications)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Construction plus 3 correct steps (including the correct matching side) with at least one justification",
        "marks": 4,
        "kind": "explain"
      },
      {
        "label": "Complete proof: ASA congruency of the two triangles, plus opposite-sides-of-a-parallelogram to transfer the equal segments to the second transversal",
        "marks": 3,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "This is one of the prescribed proofs (the \"three parallel lines / equal intercepts\" theorem), so it is examinable as bookwork — the marks reward a memorised, reason-by-reason reconstruction, not improvisation. The model solution starts with the essential CONSTRUCTION: draw a line through one intercept point parallel to the second transversal, creating two triangles that are congruent by ASA (one pair of sides equal by the given, two angle pairs equal by alternate angles and vertically opposite angles). The final move — the step most candidates omit — is to convert the congruent sides into the required equal segments using \"opposite sides of a parallelogram are equal\". The 15D scale tracks justifications, not just statements: \"Fully correct logical statements, but no justifications\" is held at high partial credit, never full. Every \"...alternate angles\", \"...vertically opposite\", \"...ASA\", \"...opposite sides of a parallelogram\" tag is a mark.",
      "source": "SEC 2024 HL Marking Scheme, Q4(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-0"
  },
  {
    "id": "maths-hl-1-0-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2023,
    "questionRef": "2023 HL P2 Q6(a)",
    "questionText": "State whether the following statement is true or false:\nTwo angles are vertically opposite if, and only if, they are equal in size.\nJustify your answer.",
    "marks": 5,
    "minutes": 5,
    "answerKind": "written",
    "commandWord": {
      "word": "State / Justify",
      "reminder": "Give the verdict, then back it with a valid reason or counterexample."
    },
    "ribbons": [
      {
        "label": "Answer: FALSE",
        "marks": 2,
        "kind": "attempt"
      },
      {
        "label": "Justify with a counterexample of equal angles that are not vertically opposite (e.g. base angles of an isosceles triangle, opposite angles of a parallelogram)",
        "marks": 3,
        "kind": "explain"
      }
    ],
    "lesson": {
      "text": "The 'if and only if' makes the statement false: vertically opposite angles ARE equal, but equal angles need NOT be vertically opposite (e.g. the equal base angles of an isosceles triangle). A counterexample to the converse direction is the whole justification.",
      "source": "SEC 2023 HL Marking Scheme, Q6(a)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-0"
  },
  {
    "id": "maths-ol-1-0-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2025,
    "questionRef": "2025 OL P2 Q5(b)",
    "questionText": "ABC is an isosceles triangle where |AB| = |AC|. D is the midpoint of [BC]. AD is perpendicular to BC. |AB| = 9 cm and |BC| = 5 cm.\n\n(i) Use the theorem of Pythagoras to work out the distance from A to D, that is, find |AD|. Give your answer correct to 1 decimal place.\n\n(ii) Show that the triangles ABD and ACD are congruent. Give a reason for any statement you make.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "written",
    "commandWord": {
      "word": "Work out / Show",
      "reminder": "Calculate, then justify the congruence."
    },
    "ribbons": [
      {
        "label": "|BD| = 2.5 and set up 2.5^2 + |AD|^2 = 9^2",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "|AD|^2 = 81 - 6.25 = 56 (correct substitution)",
        "marks": 1,
        "kind": "method"
      },
      {
        "label": "|AD| = sqrt(56) = 7.483... = 7.5 cm (1 d.p.)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "State two valid congruence elements with reasons (e.g. |AB|=|AC| given; |BD|=|DC| midpoint)",
        "marks": 10,
        "kind": "method"
      },
      {
        "label": "Complete proof with third element |AD|=|AD| common and conclusion triangle ABD congruent to ACD (SSS)",
        "marks": 5,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "D is the midpoint so |BD| = 5/2 = 2.5, giving |AD| = sqrt(9^2 - 2.5^2) = sqrt(56) = 7.5 cm. For the congruence each of the three statements (|AB|=|AC| given, |BD|=|DC| midpoint, |AD|=|AD| common) needs its reason; the scheme applies a star for a missing reason or missing conclusion (SSS).",
      "source": "SEC 2025 OL Marking Scheme, Q5(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-0"
  },
  {
    "id": "maths-ol-1-0-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2023,
    "questionRef": "2023 OL P2 Q6(c)",
    "questionText": "State whether the following statement is true or false. Justify your answer.\nStatement: \"Every square is a parallelogram.\" True or false? (Tick one box only) and give a justification.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "State / Justify",
      "reminder": "Give a verdict and a supporting geometric reason"
    },
    "ribbons": [
      {
        "label": "Tick True",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Justification: opposite sides are parallel and equal in length (or other valid reason)",
        "marks": 6,
        "kind": "method"
      },
      {
        "label": "Gate: a correct box with no justification of merit caps at low partial credit",
        "marks": 0,
        "kind": "gate"
      }
    ],
    "lesson": {
      "text": "The statement is True: a square satisfies the definition of a parallelogram (both pairs of opposite sides parallel and equal). A bare tick without a property-based justification only earns low partial credit - always name the defining property.",
      "source": "SEC 2023 OL Marking Scheme, Q6(c)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-0"
  },
  {
    "id": "maths-hl-1-1-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 HL P1 Q10(c)",
    "questionText": "A sequence of dot patterns is built so that Pattern 1 has dots at all integer points a distance of 1 unit from (0, 0), and Pattern n+1 has a dot at every integer point a distance of 1 unit from a point in Pattern n. The point (m, m) first appears in the pattern according to the rule that (1, 1) is in Pattern 2, (2, 2) is in Pattern 4, (3, 3) is in Pattern 6, and so on.\nWhat is the smallest value of n ∈ N for which the point (4, 4) is in Pattern n?",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "What is",
      "reminder": "Determine the smallest pattern number containing (4, 4)."
    },
    "ribbons": [
      {
        "label": "Recognise the pattern: (1,1) in P2, (2,2) in P4, (3,3) in P6",
        "marks": 6,
        "kind": "method"
      },
      {
        "label": "Extend to (4, 4) in P8, so n = 8",
        "marks": 4,
        "kind": "srp"
      }
    ],
    "lesson": {
      "text": "The diagonal point (m, m) first appears in Pattern 2m, so (4, 4) appears in Pattern 8. The relationship n = 2m follows from each step extending reachability by one unit in taxicab/distance terms.",
      "source": "SEC 2025 HL Marking Scheme, Q10(c)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-1"
  },
  {
    "id": "maths-hl-1-1-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2024,
    "questionRef": "2024 HL P2 Q5(a)",
    "questionText": "The circle s has equation:\nx² + y² + 4x − 6y + 5 = 0\n\n(i) Write down the centre and radius of the circle s.\n\n(ii) The circle c has equation:\n(x−2)² + (y+1)² = 72\n\nShow that the circles s and c touch internally.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "written",
    "commandWord": {
      "word": "Show that",
      "reminder": "Compare the distance between centres with the difference of the radii."
    },
    "ribbons": [
      {
        "label": "Centre of s = (−2, 3) and radius of s = √(4+9−5) = 2√2",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "Centre of c = (2, −1) and radius of c = √72 = 6√2",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "Distance between centres = √(16+16) = 4√2",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "Difference of radii = 6√2 − 2√2 = 4√2, equal to distance, so circles touch internally",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "No conclusion or incorrect conclusion stated",
        "marks": 0,
        "kind": "gate"
      }
    ],
    "lesson": {
      "text": "Two circles touch internally when the distance between their centres equals the difference of their radii (touch externally when it equals the sum). You must state the conclusion explicitly — the scheme applies a * if the comparison is done but no conclusion is written.",
      "source": "SEC 2024 HL Marking Scheme, Q5(a)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-1"
  },
  {
    "id": "maths-ol-1-1-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2025,
    "questionRef": "2025 OL P2 Q3(b)",
    "questionText": "The circle c has centre (3, -4) and radius 7. Write down the equation of c.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Write down",
      "reminder": "State the answer; minimal working expected."
    },
    "ribbons": [
      {
        "label": "Use the form (x - h)^2 + (y - k)^2 = r^2 with h, k, r identified",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Substitute two of the elements correctly",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Equation: (x - 3)^2 + (y + 4)^2 = 49",
        "marks": 4,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "With centre (3, -4) the y-term becomes (y - (-4))^2 = (y + 4)^2, and the right side must be r^2 = 49, not 7. The most common slip is leaving the radius unsquared.",
      "source": "SEC 2025 OL Marking Scheme, Q3(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-1"
  },
  {
    "id": "maths-ol-1-1-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2024,
    "questionRef": "2024 OL P2 Q4(c)",
    "questionText": "The point (2, 1) is the lowest point on the circle s with centre c. The y-axis is a tangent to the circle s. Work out the radius and the centre of the circle s.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Work out",
      "reminder": "Show the reasoning that gives the radius and centre, not just the values."
    },
    "ribbons": [
      {
        "label": "Work of merit, e.g. one ordinate of the centre correct, or relevant work on the diagram",
        "marks": 4,
        "kind": "attempt"
      },
      {
        "label": "Centre OR radius correct",
        "marks": 1,
        "kind": "srp"
      },
      {
        "label": "Radius = 2 (the y-axis tangent means the centre is one radius from x = 0, and (2, 1) is the lowest point so the centre's x = 2)",
        "marks": 5,
        "kind": "srp"
      }
    ],
    "lesson": {
      "text": "The y-axis is a tangent, so the radius equals the centre's x-coordinate. Since (2, 1) is the lowest point, the centre lies directly above it at the same x = 2, giving radius = 2 and centre = (2, 3) — i.e. one radius vertically above the lowest point.",
      "source": "SEC 2024 OL Marking Scheme, Q4(c)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-1"
  },
  {
    "id": "maths-hl-1-2-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 HL P1 Q8(c)-(d)",
    "questionText": "Jacob takes part in a race involving kayaking and running. He must get from point S in the sea to point F on the coastline. A is another point on the coastline. |SA| = 2 km, |AF| = 8 km, and the angle at A (∠SAF) is a right angle. Jacob kayaks at an average speed of 6 km/hour and runs at an average speed of 12 km/hour.\n(c) Find how long it would take Jacob in total to kayak from S to A, and then run from A to F.\n(d) Find how long it would take Jacob to kayak directly from S to F, correct to the nearest minute.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "written",
    "commandWord": {
      "word": "Find",
      "reminder": "Compute each travel time using distance ÷ speed (and Pythagoras for SF)."
    },
    "ribbons": [
      {
        "label": "(c) Time = 2/6 + 8/12 = 1 hour",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(d) Use Pythagoras: |SF| = √(8² + 2²) = √68 km",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(d) Time = √68/6 = 1·37... hours = 82 minutes (nearest minute)",
        "marks": 5,
        "kind": "srp"
      }
    ],
    "lesson": {
      "text": "In (c) keep the two legs at their own speeds (kayak 6, run 12) — 2/6 + 8/12 = 1 hour exactly. In (d) the direct sea distance needs Pythagoras (√68), then divide by 6 km/h; giving (d) only in hours rather than nearest minute caps you at High Partial Credit.",
      "source": "SEC 2025 HL Marking Scheme, Q8(c)-(d)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-2"
  },
  {
    "id": "maths-hl-1-2-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2024,
    "questionRef": "2024 HL P1 Q8(e)",
    "questionText": "C(t) = S(t) − 2·4 + 0·03t models daily sales of scarves, where t is time in days from 1 January 2024 and 2π/365 is in radians. The derivative of C(t) is given by:\n\nC′(t) = 0·03 − (38π/365) sin(2πt/365)\n\nFind the value of t that gives the first local maximum of C, that is, the first time that C′(t) = 0. Give your answer correct to the nearest day.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Find",
      "reminder": "Set the derivative to zero and solve the resulting trigonometric equation for the smallest positive t."
    },
    "ribbons": [
      {
        "label": "Work of merit, e.g. sets up the equation C′(t) = 0",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Isolate the sine: 0·03(365)/(38π) = sin(2πt/365)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Solve using sin⁻¹ and round to give t = 5 days",
        "marks": 4,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "Setting C′(t) = 0 and isolating gives sin(2πt/365) = 0·03(365)/(38π); taking the inverse sine and solving for t gives 5·336, which rounds to 5 days. The scheme applies a deduction (Full Credit −1) if the calculator is in the wrong mode (degrees instead of radians).",
      "source": "SEC 2024 HL Marking Scheme, Q8(e)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-2"
  },
  {
    "id": "maths-ol-1-2-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2025,
    "questionRef": "2025 OL P2 Q2(a)",
    "questionText": "There are two angles, A and 2A, in a right-angled triangle. The right angle is the third angle of the triangle. The lengths of two of the sides are x and 10 cm: the side x is opposite the angle A, and the side 10 cm is adjacent to angle A (the side between angle A and the right angle).\n\n(i) Show that the size of the angle A is 30 degrees.\n\n(ii) Using A = 30 degrees, find the value of x, correct to 2 decimal places.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "written",
    "commandWord": {
      "word": "Show / Find",
      "reminder": "Demonstrate the stated result, then calculate."
    },
    "ribbons": [
      {
        "label": "Set up A + 2A = 90 so 3A = 90, giving A = 30 degrees",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "Use tan 30 = x/10 (correct trig ratio)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "x = 10 tan 30 = 5.7735... = 5.77 cm (2 d.p.)",
        "marks": 6,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The three angles sum to 180, with one being 90, so A + 2A = 90 gives 3A = 90 and A = 30. In (ii) tan 30 = opposite/adjacent = x/10; the marking scheme applies a star (Full Credit -1) for no/incorrect rounding or no units.",
      "source": "SEC 2025 OL Marking Scheme, Q2(a)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-2"
  },
  {
    "id": "maths-ol-1-2-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2024,
    "questionRef": "2024 OL P2 Q8(a)(i)",
    "questionText": "A fish shop has a vertical sign [FH] with |FH| = 3 m, standing on horizontal ground. A cable is tied at the top of the sign, F, and is secured at the point G on the ground, where G is 1·4 m from the base of the sign H (so triangle FGH is right-angled at H). Use the Theorem of Pythagoras to find the length of the cable, |FG|. Give your answer in metres, correct to 1 decimal place.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Use the Theorem of Pythagoras to find",
      "reminder": "Apply a² + b² = c² with the right two sides; round to 1 d.p. as instructed."
    },
    "ribbons": [
      {
        "label": "Correct relevant formula (Pythagoras); using the cosine rule earns at most low partial credit",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Correct formula fully substituted, or one error in substitution but finishes correctly",
        "marks": 1,
        "kind": "srp"
      },
      {
        "label": "|FG|² = 1·4² + 3² = 10·96, so |FG| = √10·96 = 3·3 m (to 1 d.p.)",
        "marks": 5,
        "kind": "srp"
      }
    ],
    "lesson": {
      "text": "The cable is the hypotenuse: |FG|² = 1·4² + 3² = 10·96, so |FG| = 3·3 m. The question names Pythagoras, so using the cosine rule instead caps you at low partial credit.",
      "source": "SEC 2024 OL Marking Scheme, Q8(a)(i)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-2"
  },
  {
    "id": "maths-hl-1-3-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2024,
    "questionRef": "2024 HL P1 Q10(c)(ii)",
    "questionText": "The function s is defined by s(x) = 2x − x², and k is the image of s under axial symmetry in the y-axis. The function k can be written in the form k(x) = −x² + bx + c, where b, c ∈ R are constants. Find the value of b and the value of c.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "written",
    "commandWord": {
      "word": "Find",
      "reminder": "Reflection in the y-axis replaces x with −x; apply k(x) = s(−x) and simplify."
    },
    "ribbons": [
      {
        "label": "Some work of merit, e.g. references s(−x)",
        "marks": 6,
        "kind": "method"
      },
      {
        "label": "Either b or c correct (e.g. compute k(x) = s(−x) = −2x − x²)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "State both b = −2 and c = 0",
        "marks": 7,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "Axial symmetry in the y-axis means k(x) = s(−x). So k(x) = 2(−x) − (−x)² = −2x − x², giving b = −2 and c = 0. The deduction (Full Credit −1) applies if k(x) is written correctly but b and c are not explicitly identified — the question asks for the constants by name.",
      "source": "SEC 2024 HL Marking Scheme, Q10(c)(ii)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-3"
  },
  {
    "id": "maths-hl-1-3-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 HL P2 Q5(b)(i)",
    "questionText": "A parallelogram PQRS is enlarged using the point X as the centre of enlargement, producing the image P′Q′R′S′. The points X, Q and Q′ are collinear, with Q lying between X and Q′.\n\n|XQ| = 8 cm and |QQ′| = 4 cm.\n\nShow that the scale factor of the enlargement, k, is 1·5.",
    "marks": 5,
    "minutes": 5,
    "answerKind": "steps",
    "commandWord": {
      "word": "Show that",
      "reminder": "\"Show that\" gives you the target answer (1·5) — you must produce the working that arrives at it; quoting the answer alone earns nothing."
    },
    "ribbons": [
      {
        "label": "Work of merit, e.g. states k = |XQ′|/|XQ| or finds |XQ′| = 8 + 4 = 12",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Completes to k = 12/8 = 1·5 with full working",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The scale factor of an enlargement is the ratio of image distance to object distance from the centre: k = |XQ′| / |XQ|. The trap is the data — you are given |XQ| = 8 and the gap |QQ′| = 4, not |XQ′| directly. Because Q lies between the centre X and its image Q′, the full image distance is |XQ′| = 8 + 4 = 12, so k = 12/8 = 1·5. The marking scheme gives 2 of the 5 marks merely for writing the ratio formula or finding |XQ′| = 12, which means students who jump straight to 4/8 or 8/4 lose the chance to show the correct ratio set-up. In a 'show that' part, write the formula and substitute the numbers explicitly — the examiner needs to see the structure, not just the final 1·5.",
      "source": "SEC 2025 HL Marking Scheme, Q5(b)(i)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-3"
  },
  {
    "id": "maths-ol-1-3-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2025,
    "questionRef": "2025 OL P2 Q9(b)",
    "questionText": "Finn is making a pair of triangular tables, one bigger than the other. The bigger table-top is an enlargement of the smaller table-top. The scale factor of the enlargement is k.\n\n(i) The longest side of the bigger table-top is 45 cm. The longest side of the smaller table-top is 36 cm. Show the scale factor k = 1.25.\n\n(ii) The shortest side of the smaller table-top is 25.5 cm. Work out the length of the shortest side of the bigger table-top, correct to 1 decimal place.\n\n(iii) The area of the bigger table-top is 724 cm squared. Use k = 1.25 to find the area of the smaller table-top. Give your answer correct to the nearest cm squared.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "written",
    "commandWord": {
      "word": "Show / Work out / Find",
      "reminder": "Use the scale factor for length and area."
    },
    "ribbons": [
      {
        "label": "Scale factor k = 45/36 = 1.25",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Shortest side of bigger = 25.5 x 1.25 = 31.875 = 31.9 cm (1 d.p.)",
        "marks": 7,
        "kind": "method"
      },
      {
        "label": "Area relationship: 724 = (1.25)^2 x (smaller area)",
        "marks": 6,
        "kind": "method"
      },
      {
        "label": "Smaller area = 724/1.5625 = 463.36 = 463 cm squared",
        "marks": 4,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "Lengths scale by k but areas scale by k squared: to go from the bigger area to the smaller you divide by k^2 = 1.5625, giving 724/1.5625 = 463 cm squared. Forgetting to square the scale factor for area is the classic error.",
      "source": "SEC 2025 OL Marking Scheme, Q9(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-3"
  },
  {
    "id": "maths-ol-1-3-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2024,
    "questionRef": "2024 OL P2 Q6(b)(i)(ii)",
    "questionText": "The triangle A′ is the image of the triangle A under enlargement. In triangle A, |BD| = 4 units; in the image triangle A′, the corresponding side |B′D′| = 14 units.\n(i) Use |BD| and |B′D′| to show the scale factor is 3·5.\n(ii) |AC| = 6 units. Use the scale factor to find the distance from C to E, that is, find |CE|, given the image of |AC| = 6 maps so that |A′C′| = (scale factor) × 6 and CE is the extra length beyond the original 6 units.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Show / Find",
      "reminder": "Demonstrate the scale factor from the ratio, then apply it."
    },
    "ribbons": [
      {
        "label": "Work of merit in (i) (links object length to image length) or in (ii) (some relevant use of the scale factor)",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "Work of merit in (i) AND (ii), or one item correct",
        "marks": 2,
        "kind": "srp"
      },
      {
        "label": "(i) Scale factor = 14/4 = 3·5",
        "marks": 2,
        "kind": "srp"
      },
      {
        "label": "(ii) |A′C′| = 6 × 3·5 = 21, so |CE| = 21 − 6 = 15",
        "marks": 3,
        "kind": "srp"
      }
    ],
    "lesson": {
      "text": "The scale factor is image ÷ object = 14/4 = 3·5. To find |CE| you scale the 6-unit length to 21, then subtract the original 6, giving 15 — the common error is forgetting to subtract the original length.",
      "source": "SEC 2024 OL Marking Scheme, Q6(b)(i)(ii)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-1-3"
  },
  {
    "id": "maths-hl-2-0-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2023,
    "questionRef": "2023 HL P1 Q3(a)",
    "questionText": "Prove that √2 is not a rational number.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Prove",
      "reminder": "Give a rigorous argument from definitions."
    },
    "ribbons": [
      {
        "label": "Assume √2 = a/b with a, b∈Z, b≠0 and HCF(a,b) = 1",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Show a is even (from 2b² = a²)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Show b is also even (from b² = 2k²)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "State the contradiction of the HCF = 1 assumption",
        "marks": 2,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "Proof by contradiction must start from a fraction in lowest terms (HCF = 1). Mid Partial Credit only shows a is even; the proof is incomplete until you also show b is even, producing the common-factor contradiction.",
      "source": "SEC 2023 HL Marking Scheme, Q3(a)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-0"
  },
  {
    "id": "maths-ol-2-0-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2025,
    "questionRef": "2025 OL P1 Q6(b)",
    "questionText": "Write each of the following numbers in the form a × 10ⁿ, where 1 ≤ a < 10, n ∈ Z.\n\n58 000 =\n\n0·036 =",
    "marks": 10,
    "minutes": 10,
    "answerKind": "steps",
    "commandWord": {
      "word": "Write",
      "reminder": "\"Write ... in the form a × 10ⁿ\" asks only for correct scientific notation: a single digit before the decimal point (1 ≤ a < 10) and the matching power of 10 — positive for large numbers, negative for numbers below 1."
    },
    "ribbons": [
      {
        "label": "Write 58 000 = 5·8 × 10⁴",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "Write 0·036 = 3·6 × 10⁻²",
        "marks": 5,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "Graded on a 10C scale (0,4,6,10). The scheme gives low partial credit just for writing 5·8 or 3·6, or for showing any understanding of scientific notation, and high partial credit for one of the two answers fully correct. The recurring slip is the power of ten: 58 000 needs 10⁴ (count four places left from after the leading digit), while 0·036 needs 10⁻² because it is less than 1 (move the point two places right to reach 3·6). Students who write the right digits but the wrong exponent — or who leave a outside the 1-to-under-10 band — drop the final marks.",
      "source": "SEC 2025 OL Marking Scheme, Q6(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-0"
  },
  {
    "id": "maths-ol-2-0-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2022,
    "questionRef": "2022 OL P1 Q5(a)",
    "questionText": "Write each of the following values in the form a × 10ⁿ where 1 ≤ a < 10 and n ∈ Z.\n\n(i) 1200\n\n(ii) 0·27",
    "marks": 10,
    "minutes": 10,
    "answerKind": "steps",
    "commandWord": {
      "word": "Write",
      "reminder": "\"Write ... in the form a × 10ⁿ\" wants the value re-expressed in scientific notation only — no calculation needed, just the correct mantissa a (between 1 and 10) and the correct power of 10."
    },
    "ribbons": [
      {
        "label": "Write 1200 = 1·2 × 10³",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "Write 0·27 = 2·7 × 10⁻¹",
        "marks": 5,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "Two marks here, one per value, on a 10C scale (0,3,7,10). Low partial credit is given even for getting a or n right in one part, or for writing the number in a × 10ⁿ form but with a < 1 or a > 10 (e.g. 12 × 10² or 0·12 × 10⁴) — so the single most common error is misplacing the decimal point so that a falls outside the 1 ≤ a < 10 range. For 1200 the power is positive (10³); for 0·27 the power is negative (10⁻¹) because the number is less than 1. The scheme also credits writing 1000 or 1/10 as work of merit, showing students reach high partial credit by handling one value fully and only stumbling on the sign or size of a in the other.",
      "source": "SEC 2022 OL Marking Scheme, Q5(a)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-0"
  },
  {
    "id": "maths-hl-2-1-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 HL P1 Q5(b)",
    "questionText": "p is a positive constant.\nUse the laws of logs to write the expression:\nln[(e³p)⁵]\nin the form c + d ln p, where c, d ∈ Z are constants.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "write",
      "reminder": "Apply log laws to reach the c + d ln p form."
    },
    "ribbons": [
      {
        "label": "Deal with the power of 5: ln[(e³p)⁵] = 5 ln(e³p)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Split the product and use ln e³ = 3: 5(3 + ln p)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Simplify to 15 + 5 ln p",
        "marks": 2,
        "kind": "srp"
      }
    ],
    "lesson": {
      "text": "Either bring the power 5 outside first or expand to ln(e¹⁵p⁵) — both routes need the fact ln e = 1 to collapse ln e¹⁵ to 15. The exam answer is 15 + 5 ln p.",
      "source": "SEC 2025 HL Marking Scheme, Q5(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-1"
  },
  {
    "id": "maths-hl-2-1-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2023,
    "questionRef": "2023 HL P1 Q3(b)",
    "questionText": "t is a positive real number, with:\n log₃t + log₉t + log₂₇t + log₈₁t = 10\nFind the value of t. Give your answer in the form 3ʳ, where r∈Q.\nHint: use the formula logₐb = (log_c b)/(log_c a).",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Find",
      "reminder": "Solve for t in the form 3ʳ."
    },
    "ribbons": [
      {
        "label": "Change all logs to base 3 (or base t)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Simplify to a single-log equation: 25·log₃t = 120 (or equivalent)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Isolate log₃t = 120/25",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Find t = 3^(24/5)",
        "marks": 3,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "Rewrite log₉, log₂₇, log₈₁ as (1/2), (1/3), (1/4) of log₃t using the change-of-base formula — they all become multiples of log₃t. Low Partial Credit is given just for writing 9, 27 or 81 as a power of 3.",
      "source": "SEC 2023 HL Marking Scheme, Q3(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-1"
  },
  {
    "id": "maths-ol-2-1-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2025,
    "questionRef": "2025 OL P1 Q6(b)",
    "questionText": "Write each of the following numbers in the form a × 10ⁿ, where 1 ≤ a < 10, n ∈ Z.\n58 000 =\n0·036 =",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Write",
      "reminder": "Scientific notation: a between 1 and 10."
    },
    "ribbons": [
      {
        "label": "58 000 = 5·8 × 10⁴",
        "marks": 5,
        "kind": "evaluation"
      },
      {
        "label": "0·036 = 3·6 × 10⁻²",
        "marks": 5,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "The common error is the sign of the exponent for numbers below 1: 0·036 = 3·6 × 10⁻² (negative power). High partial credit is awarded for one of the two correct.",
      "source": "SEC 2025 OL Marking Scheme, Q6(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-1"
  },
  {
    "id": "maths-ol-2-1-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2024,
    "questionRef": "2024 OL P1 Q4(c)",
    "questionText": "(i) Write 128 in the form 2^k, where k ∈ N.\n(ii) Hence, or otherwise, solve the following equation, where x ∈ R: 2^(4x+1) = 128.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Write … solve",
      "reminder": "Express as a power, then solve."
    },
    "ribbons": [
      {
        "label": "(i) Write 128 = 2^7",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "(ii) Equate indices: 4x + 1 = 7",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(ii) Solve: x = 1.5",
        "marks": 3,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "Once both sides share base 2, equate the exponents: 4x + 1 = 7. The scheme accepts part (ii) solved by trialling the correct value once part (i) is correct, but the index-equating method is the reliable route.",
      "source": "SEC 2024 OL Marking Scheme, Q4(c)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-1"
  },
  {
    "id": "maths-hl-2-2-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 HL P1 Q7(a)(ii)-(iii)",
    "questionText": "The numbers A(1), A(2), A(3), ... form an arithmetic sequence, with A(1) = 15·8, A(2) = 22, A(3) = 28·2.\n(ii) Find an expression in n for A(n), where n ∈ N.\n(iii) Hence, or otherwise, find the value of A(100).",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Find",
      "reminder": "Build the general term, then evaluate it at n = 100."
    },
    "ribbons": [
      {
        "label": "Identify a = 15·8 and common difference d = 6·2",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Write A(n) = 15·8 + (n − 1)(6·2) = 6·2n + 9·6",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Evaluate A(100) = 6·2(100) + 9·6 = 629·6",
        "marks": 3,
        "kind": "srp"
      }
    ],
    "lesson": {
      "text": "The common difference is d = 6·2 (constant across A(1) to A(3)); use a = 15·8 in Tₙ = a + (n − 1)d. A(100) = 629·6 follows by direct substitution.",
      "source": "SEC 2025 HL Marking Scheme, Q7(a)(ii)-(iii)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-2"
  },
  {
    "id": "maths-hl-2-2-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2024,
    "questionRef": "2024 HL P1 Q7(a)",
    "questionText": "Fiadh has a gross annual salary of €54 000. She pays income tax at a rate of 20% on the first €40 000 of her salary and at a rate of 40% on the remainder. She has an annual tax credit of €1775.\n\nWork out her net annual pay, assuming that there are no other deductions.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Work out",
      "reminder": "Compute the gross tax in two bands, apply the tax credit, then subtract from gross pay."
    },
    "ribbons": [
      {
        "label": "Step 1: find gross tax = 20% of 40000 + 40% of 14000 = 8000 + 5600 = 13600",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Step 2: subtract tax from gross income",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Step 3: deal with the tax credit and finish: 54000 − (13600 − 1775) = €42 175",
        "marks": 3,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "Tax is charged in two bands: 20% on the first €40 000 and 40% on the remaining €14 000, giving gross tax €13 600. The tax credit of €1775 reduces the tax payable (not the income), so net pay = 54000 − (13600 − 1775) = €42 175.",
      "source": "SEC 2024 HL Marking Scheme, Q7(a)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-2"
  },
  {
    "id": "maths-ol-2-2-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2025,
    "questionRef": "2025 OL P1 Q1(a)",
    "questionText": "Seán is buying a power bank and a USB-C cable.\n(i) One power bank costs €30 before VAT at 23% has been added. Find the cost of the power bank after VAT has been added.\n(ii) Seán is going to buy a different power bank that costs €26, and a USB-C cable that costs €9. Seán sees a special offer to buy the power bank and USB-C cable together for €28. Work out the percentage discount of this special offer.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "written",
    "commandWord": {
      "word": "Find / Work out",
      "reminder": "Find = compute and state the value."
    },
    "ribbons": [
      {
        "label": "(i) Multiply 30 by 1·23 to add 23% VAT (gives €36·90)",
        "marks": 6,
        "kind": "method"
      },
      {
        "label": "(i) Correct VAT-inclusive price €36·90",
        "marks": 4,
        "kind": "evaluation"
      },
      {
        "label": "(ii) Find the discount amount 35 − 28 = 7",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(ii) Divide by original total and ×100: (7/35)×100 = 20%",
        "marks": 5,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "Part (ii) trips students because the discount must be a percentage of the FULL combined price (€26+€9=€35), not of €28. The marking scheme awards high partial credit only once you have written the fraction 7/35.",
      "source": "SEC 2025 OL Marking Scheme, Q1(a)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-2"
  },
  {
    "id": "maths-ol-2-2-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2024,
    "questionRef": "2024 OL P2 Q10(a)(i)(ii)(iii)",
    "questionText": "The fastest women's serve at Wimbledon 2023 was 121 miles per hour.\n(i) Use the conversion rate of 1 mile = 1·61 km to convert 121 miles to km.\n(ii) Convert one hour to seconds.\n(iii) Use your answers to parts (i) and (ii) to convert 121 miles per hour to metres per second. Give your answer correct to 2 decimal places.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Convert",
      "reminder": "Carry out each unit conversion step by step; round the final m/s to 2 d.p."
    },
    "ribbons": [
      {
        "label": "Work of merit in (i), (ii) or (iii)",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "Work of merit in two parts, or one part correct",
        "marks": 2,
        "kind": "srp"
      },
      {
        "label": "(i) 121 × 1·61 = 194·81 km and (ii) 1 hour = 60 × 60 = 3600 s",
        "marks": 2,
        "kind": "srp"
      },
      {
        "label": "(iii) 194 810 m / 3600 s = 54·11 m/s (to 2 d.p.)",
        "marks": 3,
        "kind": "srp"
      }
    ],
    "lesson": {
      "text": "Convert miles to km (121 × 1·61 = 194·81 km = 194 810 m), and 1 hour to 3600 s, then divide metres by seconds: 194 810 / 3600 = 54·11 m/s. The km-to-m step (×1000) is the one most often dropped.",
      "source": "SEC 2024 OL Marking Scheme, Q10(a)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-2"
  },
  {
    "id": "maths-hl-2-3-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 HL P2 Q7(b)",
    "questionText": "A submarine body is made of a hemisphere, a cylinder, and a cone, all with radius x (where x ∈ R), arranged in a row. The cylinder has length 7x and the cone has length 4x; the hemisphere adds a length of x. This submarine has a volume of 6738 m³, correct to the nearest m³. By solving an equation in x, find the total length of this submarine. Give your answer in metres, correct to 1 decimal place.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Find",
      "reminder": "Solve an equation in x, then give the length."
    },
    "ribbons": [
      {
        "label": "Set up volume equation: (2/3)πx³ + πx²(7x) + (1/3)πx²(4x) = 6738",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Simplify to 9πx³ = 6738 and isolate x³",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Solve x = ∛(6738/9π) ≈ 6·19, then total length = 12x ≈ 74·4 m",
        "marks": 2,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The three volume formulas combine to the clean form 9πx³ = 6738; the total length is hemisphere (x) + cylinder (7x) + cone (4x) = 12x, so finding x alone without multiplying by 12 is only Full Credit −1.",
      "source": "SEC 2025 HL Marking Scheme, Q7(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-3"
  },
  {
    "id": "maths-hl-2-3-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2024,
    "questionRef": "2024 HL P1 Q9(c)",
    "questionText": "A hemisphere has a diameter of x cm. V(x), the volume of this hemisphere in cm³, is given by:\n\nV(x) = (π/12) x³\n\nFind the value of x when the volume of the hemisphere is 3 litres. Give your answer correct to 1 decimal place.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "written",
    "commandWord": {
      "word": "Find",
      "reminder": "Convert litres to cm³ first, then solve the cubic equation for x."
    },
    "ribbons": [
      {
        "label": "Work of merit setting up the equation, e.g. states 3 litres = 3000 cm³",
        "marks": 6,
        "kind": "method"
      },
      {
        "label": "Rearrange to find x³ = 3000(12)/π",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Take the cube root to give x = 22·5 cm (to 1 d.p.)",
        "marks": 7,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "The unit conversion is the gateway: 3 litres = 3000 cm³, not 3. Then (π/12)x³ = 3000 gives x³ = 36000/π, so x = ∛(36000/π) ≈ 22·5 cm. Forgetting the litres-to-cm³ conversion gives a wildly wrong answer; the scheme rewards stating 3 litres = 3000 cm³.",
      "source": "SEC 2024 HL Marking Scheme, Q9(c)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-3"
  },
  {
    "id": "maths-ol-2-3-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2025,
    "questionRef": "2025 OL P1 Q10(a)(ii)",
    "questionText": "A factory makes closed boxes. The box is a rectangular cuboid with side lengths 70 cm, 30 cm and 20 cm. Work out the surface area of this box, in cm².",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Work out",
      "reminder": "Sum the areas of all six faces of the cuboid."
    },
    "ribbons": [
      {
        "label": "Areas of the three distinct faces: 70×30 = 2100, 70×20 = 1400, 20×30 = 600",
        "marks": 6,
        "kind": "method"
      },
      {
        "label": "Double the total for opposite faces: (2100+1400+600) × 2",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Surface area = 8200 cm²",
        "marks": 2,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "A closed box has three pairs of equal faces, so compute the three distinct rectangle areas then multiply the sum by 2 (= 8200 cm²). The scheme awards NO credit for finding the volume instead.",
      "source": "SEC 2025 OL Marking Scheme, Q10(a)(ii)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-3"
  },
  {
    "id": "maths-ol-2-3-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2024,
    "questionRef": "2024 OL P2 Q9(d)(i)",
    "questionText": "An ice-cream-cone logo is made up of a sector of a circle of radius 20 cm and two identical right-angled triangles. The two triangles each have an angle of 70° at the centre point, and these two 70° angles sit between the two straight edges of the sector. The arc of the sector is labelled s. Find the size of the sector angle θ and hence find the length of the arc s. Give the length in cm, correct to 1 decimal place.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Find ... hence find",
      "reminder": "First get θ from the angles around the point, then use the arc-length fraction of the circumference; round to 1 d.p."
    },
    "ribbons": [
      {
        "label": "Work of merit, e.g. new relevant angle found, or correct relevant formula",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "θ = 220 found AND the arc-length formula fully substituted",
        "marks": 1,
        "kind": "srp"
      },
      {
        "label": "θ = 360 − 2(70) = 220°, arc s = (220/360)[2π(20)] = 76·8 cm (to 1 d.p.)",
        "marks": 5,
        "kind": "srp"
      }
    ],
    "lesson": {
      "text": "The sector angle is what's left after the two 70° triangle angles: θ = 360 − 2(70) = 220°. Then arc s = (θ/360) × 2πr = (220/360) × 2π(20) = 76·8 cm. Forgetting to subtract both 70° angles is the main slip.",
      "source": "SEC 2024 OL Marking Scheme, Q9(d)(i)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-2-3"
  },
  {
    "id": "maths-hl-3-0-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 HL P1 Q1(b)",
    "questionText": "Multiply out and simplify:\n(4x − 10√x)(2x + 5√x − 7)",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Multiply out and simplify",
      "reminder": "Expand all brackets, then collect like terms into simplest form."
    },
    "ribbons": [
      {
        "label": "Distribute correctly, producing the 6 expansion terms (e.g. 8x² + 20x√x − 28x − 20x√x − 50x + 70√x)",
        "marks": 6,
        "kind": "method"
      },
      {
        "label": "Collect like terms and cancel the ±20x√x to reach 8x² − 78x + 70√x with no excess terms",
        "marks": 4,
        "kind": "srp"
      }
    ],
    "lesson": {
      "text": "There are 9 terms to check across the last two lines; for full credit there must be NO excess terms — students lose marks by failing to cancel the +20x√x and −20x√x pair. Substituting y = √x first can make the algebra cleaner.",
      "source": "SEC 2025 HL Marking Scheme, Q1(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-0"
  },
  {
    "id": "maths-hl-3-0-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2024,
    "questionRef": "2024 HL P1 Q1(b)",
    "questionText": "Write the following expression as a single fraction in terms of t:\n\n4/(2t + 1) − 7/(12t)",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Write … as a single fraction",
      "reminder": "Combine the two fractions over a common denominator and simplify the numerator."
    },
    "ribbons": [
      {
        "label": "Identify the common denominator (2t + 1)(12t) or the combined numerator",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Write 4(12t) − 7(2t + 1) over (2t + 1)(12t)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Simplify numerator to give (34t − 7)/[(2t + 1)(12t)]",
        "marks": 4,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "High partial credit is reached just by writing 4(12t) − 7(2t+1) over the common denominator (2t+1)(12t); the final marks come from expanding and collecting the numerator correctly to 34t − 7. Watch the sign on the −7(2t+1) term.",
      "source": "SEC 2024 HL Marking Scheme, Q1(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-0"
  },
  {
    "id": "maths-ol-3-0-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2025,
    "questionRef": "2025 OL P1 Q3(c)",
    "questionText": "k × t = 12, where k, t ∈ Z.\n(i) Write down a possible value of k and the corresponding value of t.\n(ii) Use your values for k and t from part (c)(i) to find the value of b in the equation below:\n(x + k)(x + t) = x² + bx + 12",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Write down / find",
      "reminder": "Pick a factor pair, then expand to read off b."
    },
    "ribbons": [
      {
        "label": "(i) A valid factor pair, e.g. k = 6, t = 2 (or similar with product 12)",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(ii) Expand (x + k)(x + t) using chosen values",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "(ii) Read off b as the coefficient of x, e.g. b = 8",
        "marks": 2,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "b is the sum of the two factors (k + t), so consistency matters: the answer in (ii) must match the pair chosen in (i). Low partial credit in (i) is given just for stating one factor of 12.",
      "source": "SEC 2025 OL Marking Scheme, Q3(c)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-0"
  },
  {
    "id": "maths-ol-3-0-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2023,
    "questionRef": "2023 OL P1 Q6(b)",
    "questionText": "Expand and simplify (2x − 4)² − 6.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Expand and simplify",
      "reminder": "Multiply out and collect terms."
    },
    "ribbons": [
      {
        "label": "One term correct in expansion, or writes (2x − 4)(2x − 4)",
        "marks": 4,
        "kind": "attempt"
      },
      {
        "label": "Writes full expansion 4x² − 8x − 8x + 16",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Simplifies including the −6: 4x² − 16x + 10",
        "marks": 4,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "Square the bracket as (2x − 4)(2x − 4) to capture the middle term −16x — the scheme penalises ignoring twice the product (writing 4x² ∓ 16). Don't forget to combine the −6 with +16 to get +10.",
      "source": "SEC 2023 OL Marking Scheme, Q6(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-0"
  },
  {
    "id": "maths-hl-3-1-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 HL P1 Q1(c)",
    "questionText": "(2x + 3) is a factor of 4x³ − 12x² − 7x + 30.\nUse this information to find the three solutions to the following equation in x:\n4x³ − 12x² − 7x + 30 = 0",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "find",
      "reminder": "Work out and state all three solution values."
    },
    "ribbons": [
      {
        "label": "Set up long division / array / product to divide the cubic by (2x + 3)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Obtain the quadratic quotient 2x² − 9x + 10",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Factorise the quadratic to (2x − 5)(x − 2)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "State all three solutions x = −3/2, x = 5/2, x = 2",
        "marks": 2,
        "kind": "srp"
      }
    ],
    "lesson": {
      "text": "The scheme treats this as 5 steps; finding the quadratic quotient 2x² − 9x + 10 is the pivotal step. Correct answers without supporting work earn only Low Partial Credit — the division or array must be shown.",
      "source": "SEC 2025 HL Marking Scheme, Q1(c)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-1"
  },
  {
    "id": "maths-hl-3-1-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2024,
    "questionRef": "2024 HL P1 Q1(a)",
    "questionText": "Solve the following equation for n ∈ N:\n\nn − 3 = √(3n + 1)",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Solve",
      "reminder": "Find the value(s) of the unknown that satisfy the equation; here only natural-number solutions are valid, so reject extraneous roots."
    },
    "ribbons": [
      {
        "label": "Square both sides and form a fully correct quadratic n² − 9n + 8 = 0",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "Factorise the quadratic (n − 8)(n − 1) = 0 and solve for n",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Identify n = 8 only, rejecting n = 1 because it gives −2 = √4 (extraneous)",
        "marks": 3,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "Squaring both sides introduces an extraneous root: n = 1 satisfies the squared equation but not the original because it would give −2 = √4. The marking scheme applies a deduction (Full Credit −1) if an incorrect solution is not eliminated — you must check both roots back in the original equation.",
      "source": "SEC 2024 HL Marking Scheme, Q1(a)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-1"
  },
  {
    "id": "maths-ol-3-1-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2025,
    "questionRef": "2025 OL P1 Q5(a)",
    "questionText": "Use algebra to solve the simultaneous equations:\n3x + 2y = 11\nx − 4y = −1",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Use algebra to solve",
      "reminder": "Eliminate one variable, then back-substitute."
    },
    "ribbons": [
      {
        "label": "Scale an equation so a variable cancels (e.g. multiply 3x+2y=11 by 2)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Reduce to one variable and solve (x = 3)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Back-substitute to find the second variable (y = 1)",
        "marks": 3,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "Marked in four steps: scale to cancel a variable, form a single-variable equation, solve it, then find the second variable. 'Use algebra' rules out a graphical/trial answer for full marks.",
      "source": "SEC 2025 OL Marking Scheme, Q5(a)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-1"
  },
  {
    "id": "maths-ol-3-1-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2024,
    "questionRef": "2024 OL P1 Q3(c)",
    "questionText": "Use algebra to solve the simultaneous equations:\n2x + y = 5\nx² + y² = 25\nHint: first, use 2x + y = 5 to write y in terms of x.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "written",
    "commandWord": {
      "word": "Solve",
      "reminder": "Find the x and y values."
    },
    "ribbons": [
      {
        "label": "Write y in terms of x: y = 5 − 2x",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "Substitute into the quadratic and simplify to 5x² − 20x = 0",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Solve for both x values: x = 0 or x = 4",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Find both co-ordinate sets: (0, 5) and (4, −3)",
        "marks": 4,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "Substitute the linear equation into the quadratic to get one equation in x. A frequent slip is stopping after finding the x-values and forgetting to find the matching y-values — the final marks need both full co-ordinate pairs.",
      "source": "SEC 2024 OL Marking Scheme, Q3(c)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-1"
  },
  {
    "id": "maths-hl-3-2-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 HL P1 Q1(a)",
    "questionText": "Solve the following inequality for x ∈ R:\n|x − 3| ≤ 12",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Solve",
      "reminder": "Find all values of x that satisfy it; give the full solution set."
    },
    "ribbons": [
      {
        "label": "Set up the two cases x − 3 ≤ 12 and x − 3 ≥ −12 (or square both sides to get a quadratic inequality)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Find both boundary values x = 15 and x = −9",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Write the solution as the combined interval −9 ≤ x ≤ 15 (use 'and' / ∩, keep inequalities non-strict)",
        "marks": 3,
        "kind": "srp"
      }
    ],
    "lesson": {
      "text": "Examiners apply a deduction (Full Credit −1) if a strict inequality is used instead of ≤, or if the linking 'and'/∩ is omitted in the two-case method — the answer must be the closed interval −9 ≤ x ≤ 15.",
      "source": "SEC 2025 HL Marking Scheme, Q1(a)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-2"
  },
  {
    "id": "maths-hl-3-2-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2024,
    "questionRef": "2024 HL P1 Q10(b)",
    "questionText": "The height of a plant can be modelled by P(x), where x is the number of days after the plant starts to grow. The derivative of this function is:\n\nP′(x) = 1·1 + 2·73x − 0·078x²\n\nFind the range of values of x for which P′(x) > 24. In your answer, give each value correct to the nearest whole number.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Find",
      "reminder": "Form a quadratic inequality, find the roots, then determine the interval where it holds."
    },
    "ribbons": [
      {
        "label": "GATE: for a linear inequality, award Low Partial Credit at most",
        "marks": 0,
        "kind": "gate"
      },
      {
        "label": "Formulate the inequality correctly: 0·078x² − 2·73x + 22·9 < 0",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Find the roots of the quadratic, x ≈ 13·94 and 21·06 (e.g. by formula)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "State the solution set 14 ≤ x ≤ 21",
        "marks": 3,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "Rearrange P′(x) > 24 to 0·078x² − 2·73x + 22·9 < 0, find the roots (≈13·94 and 21·06), and because the parabola opens upward the inequality holds between the roots, giving 14 ≤ x ≤ 21. Treating it as a linear inequality caps the marks at Low Partial Credit — it is a quadratic.",
      "source": "SEC 2024 HL Marking Scheme, Q10(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-2"
  },
  {
    "id": "maths-ol-3-2-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2025,
    "questionRef": "2025 OL P1 Q3(b)",
    "questionText": "Solve the inequality for x ∈ R:\n2x + 4 ≥ 6x − 8",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Solve",
      "reminder": "Solve = isolate x; flip the sign when dividing by a negative."
    },
    "ribbons": [
      {
        "label": "One correct transposition of terms (e.g. 2x − 6x ≥ −8 − 4)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Reach −4x ≥ −12 (equivalently 4x ≤ 12)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Correct solution x ≤ 3 (inequality reversed when dividing by −4)",
        "marks": 4,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "The classic error is forgetting to reverse the inequality sign when dividing by −4: −4x ≥ −12 becomes x ≤ 3, not x ≥ 3. High partial credit stops at −4x ≥ −12.",
      "source": "SEC 2025 OL Marking Scheme, Q3(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-2"
  },
  {
    "id": "maths-ol-3-2-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2022,
    "questionRef": "2022 OL P1 Q6(b)",
    "questionText": "The nth term of an arithmetic sequence is given by Tₙ = −254 + (n − 1)(4), for n ∈ N.\n\nFind the smallest value of n ∈ N for which\n\n−254 + (n − 1)(4) > 0",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Find",
      "reminder": "Find the smallest natural number n satisfying the inequality."
    },
    "ribbons": [
      {
        "label": "One correct operation carried out, or trial and improvement",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "Correctly isolates n (i.e. 4n > 254 + 4)",
        "marks": 7,
        "kind": "method"
      },
      {
        "label": "Concludes n > 64·5 so the smallest n = 65",
        "marks": 0,
        "kind": "gate"
      }
    ],
    "lesson": {
      "text": "Expand and solve: −254 + 4n − 4 > 0 gives 4n > 258, so n > 64·5. Because n must be a natural number, round up to the next whole number: n = 65. The scheme applies a star (Full Credit −1) if you leave the answer as 64·5 — for 'smallest n' you must give the integer, not the boundary value.",
      "source": "SEC 2022 OL Marking Scheme, Q6(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-2"
  },
  {
    "id": "maths-hl-3-3-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 HL P1 Q4(b)",
    "questionText": "In this question, i² = −1.\nUse de Moivre's theorem and the expression (cos θ + i sin θ)² to prove that the following is true, for any angle θ:\ncos 2θ = cos²θ − sin²θ",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "prove",
      "reminder": "Give a complete logical argument establishing the identity."
    },
    "ribbons": [
      {
        "label": "By de Moivre: (cos θ + i sin θ)² = cos 2θ + i sin 2θ; expand the LHS as a product",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Expand to cos²θ + 2i cos θ sin θ + i² sin²θ = cos²θ − sin²θ + 2i cos θ sin θ",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Equate real parts to conclude cos 2θ = cos²θ − sin²θ",
        "marks": 2,
        "kind": "srp"
      }
    ],
    "lesson": {
      "text": "The proof hinges on equating the REAL parts of the two equal expressions; High Partial Credit is reached only once the expanded form cos²θ + 2i cos θ sin θ + i² sin²θ is correctly written.",
      "source": "SEC 2025 HL Marking Scheme, Q4(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-3"
  },
  {
    "id": "maths-hl-3-3-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2024,
    "questionRef": "2024 HL P1 Q2(b)",
    "questionText": "In this question, i² = −1.\n\nUse de Moivre's theorem to write (1 − √3 i)⁹ in the form a + bi, where a, b ∈ R.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Use de Moivre's theorem to write",
      "reminder": "You must convert to polar form and apply de Moivre's theorem — an algebraic expansion is not credited."
    },
    "ribbons": [
      {
        "label": "GATE: must engage with polar form or de Moivre's theorem to receive any credit",
        "marks": 0,
        "kind": "gate"
      },
      {
        "label": "Step 1: find the modulus r = 2",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Step 2: find the argument θ (e.g. 300° or 5π/3)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Step 3: apply de Moivre's theorem to get 2⁹(cos 9θ + i sin 9θ)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Step 4: finish in rectangular form, answer −512",
        "marks": 2,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "Candidates must engage with polar form or de Moivre's theorem to be awarded any credit — directly expanding the binomial earns nothing. The four steps are: find r = 2, find θ, raise to the 9th power, and convert 512(−1 + 0i) back to the answer −512.",
      "source": "SEC 2024 HL Marking Scheme, Q2(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-3"
  },
  {
    "id": "maths-ol-3-3-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2025,
    "questionRef": "2025 OL P1 Q2(b)",
    "questionText": "In this question, i² = −1. u and v are two complex numbers.\nu = 4 − 6i\nv = 1 + i\nWrite u/v in the form a + bi, where a, b ∈ Z.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Write",
      "reminder": "Write in the form a + bi means divide and simplify."
    },
    "ribbons": [
      {
        "label": "Multiply top and bottom by the conjugate (1 − i)",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Correct multiplication giving numerator −2 − 10i and denominator 2",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Simplify to a + bi form: −1 − 5i",
        "marks": 3,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "The standard method is to multiply numerator and denominator by the conjugate of v (1 − i). Leaving the answer as (−2 − 10i)/2 instead of simplifying to −1 − 5i earns only Full Credit −1 (a * is applied).",
      "source": "SEC 2025 OL Marking Scheme, Q2(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-3"
  },
  {
    "id": "maths-ol-3-3-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2024,
    "questionRef": "2024 OL P1 Q2(b)",
    "questionText": "In this question, i² = −1. v = 15 / (1 + 2i). Write v in the form a + bi, where a, b ∈ Z.",
    "marks": 15,
    "minutes": 15,
    "answerKind": "written",
    "commandWord": {
      "word": "Write",
      "reminder": "Give it in the stated form."
    },
    "ribbons": [
      {
        "label": "Multiply above and below by the conjugate (1 − 2i)",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "Simplify numerator/denominator: (15 − 30i) / 5",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Write final answer in a + bi form: 3 − 6i",
        "marks": 7,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "To divide complex numbers, multiply top and bottom by the conjugate of the denominator (1 − 2i). The scheme applies a * (Full Credit -1) if the answer is left as (15 − 30i)/5 instead of being simplified to 3 − 6i.",
      "source": "SEC 2024 OL Marking Scheme, Q2(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-3-3"
  },
  {
    "id": "maths-hl-4-0-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2024,
    "questionRef": "2024 HL P1 Q6(b)(iii)",
    "questionText": "Two functions are defined for x ∈ R, x > 0 as f(x) = e⁹ˣ and g(x) = ln √x.\n\nWrite the function g(f(x)) in terms of x, in its simplest form.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Write … in its simplest form",
      "reminder": "Compose the functions (substitute f into g) and simplify using log and index laws."
    },
    "ribbons": [
      {
        "label": "Some correct substitution into the composite function, g(f(x)) = ln √(e⁹ˣ)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Write ln √(e⁹ˣ) as ln(e⁹ˣ)^(1/2) or equivalent",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Simplify to 9x/2 (or 4·5x)",
        "marks": 4,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "Compose by putting f inside g: g(f(x)) = ln √(e⁹ˣ) = ln(e⁹ˣ)^(1/2) = (9x/2) ln e = 9x/2. The ln and e are inverse operations, and the square root halves the exponent — together they collapse to a simple linear expression 4·5x.",
      "source": "SEC 2024 HL Marking Scheme, Q6(b)(iii)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-4-0"
  },
  {
    "id": "maths-hl-4-0-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2023,
    "questionRef": "2023 HL P2 Q7(c)",
    "questionText": "When Olga is resting, the volume of air, V, in her lungs after t seconds can be modelled by:\nV(t) = 2 − 0.4 cos((π/2)t),\nwhere V is in litres, t ≥ 0 is the time in seconds, and (π/2)t is in radians.\n\nFind the values marked a and b on the graph, the minimum and maximum values of V.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Find",
      "reminder": "Determine both extreme values."
    },
    "ribbons": [
      {
        "label": "Recognise the range is 2 ± 0.4 (amplitude 0.4 about the line V=2)",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "Minimum a = 1.6 litres",
        "marks": 3,
        "kind": "evaluation"
      },
      {
        "label": "Maximum b = 2.4 litres",
        "marks": 2,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "For V = 2 − 0.4cos(...), the cosine ranges over [−1, 1], so V ranges over 2 ± 0.4: minimum a = 1.6 (when cos = +1) and maximum b = 2.4 (when cos = −1). No calculus is needed — reading off the amplitude and midline suffices.",
      "source": "SEC 2023 HL Marking Scheme, Q7(c)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-4-0"
  },
  {
    "id": "maths-ol-4-0-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2023,
    "questionRef": "2023 OL P1 Q7(a)(i)",
    "questionText": "When it rains on land, some of the rain soaks into the land, and the rest runs off the land. The runoff curve number, C, is a number used when estimating the amount of rain that runs off a particular area of land. C is given by:\nC = 1000 / (S + 10)\n\nwhere S is a measure of the maximum amount of rain that can soak into the soil.\n\nFind the value of C when S = 15.",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Find",
      "reminder": "Substitute and evaluate."
    },
    "ribbons": [
      {
        "label": "Work of merit, e.g. substitutes 15, or writes 15 + 10",
        "marks": 7,
        "kind": "attempt"
      },
      {
        "label": "Evaluates: 1000 / (15 + 10) = 40",
        "marks": 3,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "Add inside the denominator first: S + 10 = 25, so C = 1000/25 = 40. The scheme stars the slip of writing 1000/25 wrongly; a correct answer without work earns full credit.",
      "source": "SEC 2023 OL Marking Scheme, Q7(a)(i)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-4-0"
  },
  {
    "id": "maths-ol-4-0-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2022,
    "questionRef": "2022 OL P1 Q10(a)(i)(ii)",
    "questionText": "Keith hits a hurling ball. The height of the ball could be modelled by the quadratic function\n\nh = −2t² + 5t + 1·2\n\nwhere h is the height of the ball, in metres, t seconds after being hit, and t ∈ R.\n\n(i) How high, in metres, was the ball when it was hit (when t = 0)?\n(ii) The ball was caught after 2·4 seconds. How high, in metres, was the ball when it was caught?",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "How high",
      "reminder": "Evaluate h at t = 0 and t = 2·4."
    },
    "ribbons": [
      {
        "label": "(i) Substitutes t = 0, giving h(0) = 1·2 m",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "(ii) Substitutes t = 2·4 into h = −2t² + 5t + 1·2",
        "marks": 3,
        "kind": "attempt"
      },
      {
        "label": "(ii) Computes h(2·4) = −2(2·4)² + 5(2·4) + 1·2 = 1·68 m",
        "marks": 2,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "Evaluating the model at t = 0 gives the launch height: h(0) = 1·2 m (the constant term). At t = 2·4, h = −2(2·4)² + 5(2·4) + 1·2 = −11·52 + 12 + 1·2 = 1·68 m. Watch the order of operations: square 2·4 before multiplying by −2.",
      "source": "SEC 2022 OL Marking Scheme, Q10(a)(i)(ii)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-4-0"
  },
  {
    "id": "maths-hl-4-1-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2025,
    "questionRef": "2025 HL P1 Q2(a)(ii)",
    "questionText": "A function is defined for x ∈ R by:\nf(x) = 6 + x² + sin 4x\nFind the equation of the tangent to the curve y = f(x) at the point where x = 0.\nGive your answer in the form ax + by + c = 0, where a, b, c ∈ Z.\n(Note: f′(x) = 2x + 4 cos 4x.)",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Find",
      "reminder": "Determine the tangent line equation and give it in the required integer form."
    },
    "ribbons": [
      {
        "label": "Find the slope of the tangent at x = 0: f′(0) = 4",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Find the y-value at x = 0: f(0) = 6, so point of contact is (0, 6)",
        "marks": 2,
        "kind": "method"
      },
      {
        "label": "Substitute slope and point into y − y₁ = m(x − x₁)",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Write in required form: 4x − y + 6 = 0",
        "marks": 2,
        "kind": "srp"
      }
    ],
    "lesson": {
      "text": "Both the slope f′(0) and the y-value f(0) are needed before any credit is awarded for substituting into the line formula — a value for the slope is specifically required to earn the final 'required form' mark.",
      "source": "SEC 2025 HL Marking Scheme, Q2(a)(ii)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-4-1"
  },
  {
    "id": "maths-hl-4-1-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "higher",
    "year": 2024,
    "questionRef": "2024 HL P1 Q4(a)",
    "questionText": "Differentiate the following function from first principles, with respect to x:\n\nf(x) = x² − 7x − 10",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Differentiate … from first principles",
      "reminder": "You must use the limit definition of the derivative — using the rule for differentiation earns no credit."
    },
    "ribbons": [
      {
        "label": "GATE: no credit if first principles (the limit definition) is not used",
        "marks": 0,
        "kind": "gate"
      },
      {
        "label": "Form and correctly expand f(x + h) = x² + 2hx + h² − 7x − 7h − 10",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Simplify f(x + h) − f(x) = 2hx + h² − 7h",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Divide by h and take the limit as h → 0 to get f′(x) = 2x − 7",
        "marks": 3,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "There is no credit unless the first-principles limit definition is actually used — differentiating by rule scores zero. Note the scheme applies a deduction if a student writes 'lim h = 0' or 'lim h → ∞' instead of the correct 'lim h → 0', even when the algebra is otherwise correct.",
      "source": "SEC 2024 HL Marking Scheme, Q4(a)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-4-1"
  },
  {
    "id": "maths-ol-4-1-1",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2025,
    "questionRef": "2025 OL P1 Q4(b)",
    "questionText": "The function f(x) is defined as f(x) = x³ − 3x² + 4x − 8, where x ∈ R.\nFind f′(x), the derivative of f(x). Hence, find the slope of the tangent to f(x) at the point (2, −4).",
    "marks": 10,
    "minutes": 10,
    "answerKind": "written",
    "commandWord": {
      "word": "Find / Hence find",
      "reminder": "Differentiate, then substitute x = 2 into f′(x)."
    },
    "ribbons": [
      {
        "label": "Correct differentiation: f′(x) = 3x² − 6x + 4",
        "marks": 4,
        "kind": "method"
      },
      {
        "label": "Substitute x = 2 into f′(x): 3(2)² − 6(2) + 4",
        "marks": 3,
        "kind": "method"
      },
      {
        "label": "Slope of tangent = 4",
        "marks": 3,
        "kind": "evaluation"
      }
    ],
    "lesson": {
      "text": "The examiner explicitly notes ZERO credit for substituting 2 into f(x) instead of f′(x): the slope of a tangent comes from the derivative, not the original function.",
      "source": "SEC 2025 OL Marking Scheme, Q4(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-4-1"
  },
  {
    "id": "maths-ol-4-1-2",
    "subject": "maths",
    "subjectLabel": "Mathematics",
    "level": "ordinary",
    "year": 2024,
    "questionRef": "2024 OL P1 Q5(b)",
    "questionText": "The function f is defined as f(x) = 5x² − 20x + 2, where x ∈ R. Use calculus to find the co-ordinates of the local minimum point of f.",
    "marks": 20,
    "minutes": 20,
    "answerKind": "written",
    "commandWord": {
      "word": "Find",
      "reminder": "Give the (x, y) co-ordinates."
    },
    "ribbons": [
      {
        "label": "Differentiate: f′(x) = 10x − 20",
        "marks": 7,
        "kind": "method"
      },
      {
        "label": "Set f′(x) = 0 and solve: x = 2",
        "marks": 5,
        "kind": "method"
      },
      {
        "label": "Find f(2) = 5(2)² − 20(2) + 2 = −18, giving the point (2, −18)",
        "marks": 8,
        "kind": "method"
      }
    ],
    "lesson": {
      "text": "The local minimum occurs where f′(x) = 0; differentiate first, solve for x, then substitute back into the ORIGINAL f(x) to get the y-coordinate. Giving only x = 2 (without finding the y-value −18) leaves the answer incomplete.",
      "source": "SEC 2024 OL Marking Scheme, Q5(b)"
    },
    "subjectId": "mathematics",
    "topicId": "mathematics-4-1"
  }
];
