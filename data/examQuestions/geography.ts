/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Leaving Cert Geography exam questions for the Exam Strategiser.
 * 2025 Higher Level Paper 2 (Part Two: 320 marks, ~140 mins).
 * Source: SEC paper + marking scheme. Question text and allocation rules
 * taken verbatim from the marking scheme.
 */

import { type ExamQuestion } from '../../types/examStrategiser';

export const geographyQuestions: ExamQuestion[] = [
  {
    id: 'geo-2025-hl-q1c',
    taskType: 'geography-physical-process-explanation',
    subject: 'geography',
    year: 2025,
    paper: 'Paper 2',
    section: 'Section 1 — Patterns and Processes — Isostasy',
    questionNumber: '1C',
    level: 'higher',
    marks: 30,
    totalPaperMarks: 320,
    totalPaperMinutes: 140,
    commandWords: ['Describe and explain'],
    questionText: [
      {
        type: 'paragraph',
        content: [
          { text: 'Describe and explain', annotation: { type: 'command', note: 'Two-part instruction. Both DESCRIBE the process AND EXPLAIN how it shaped the landscape. Doing only one half caps you well below full marks.' } },
          { text: ' how ' },
          { text: 'isostasy', annotation: { type: 'keyword', note: "The vertical adjustment of the Earth's crust in response to changes in load (ice, sediment, water). Different from eustasy (sea level change from water volume)." } },
          { text: ' has shaped ' },
          { text: 'the Irish landscape', annotation: { type: 'trap', note: 'TIED TO IRELAND. Marking scheme: "Max 2 x SRPs if there is merely a description of isostasy without a reference to the impact on the Irish landscape." Foreign examples (Scotland, Scandinavia, Hudson Bay) earn 0 marks for this question — the science is identical but the question is Ireland-specific.' } },
          { text: '. ' },
          { text: '(30)', annotation: { type: 'marks-allocation', note: 'Impact/feature identified: 2 marks. Description/explanation: 14 SRPs. Bonuses: +1 SRP for second feature, +2 SRPs for two named Irish examples, +1 SRP for labelled diagram, +2 SRPs for additional info on labelled diagram. Diagram without labels = 0 marks. Coastal emergence and rejuvenation features accepted.' } },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'q1c-feature',
        type: 'short-text',
        prompt: "Name one specific Irish landscape feature you'd attribute to isostasy.",
        hint: 'Raised beach, fossil cliff, river terrace, knickpoint, incised meander…',
        debrief: {
          strategicPrinciple: 'The first 2 marks come from naming a recognised isostatic feature in Ireland (raised beach, fossil cliff, river terrace, knickpoint, incised meander). Generic "a coastline" or "a beach" without specifying the isostatic origin earns the feature credit only.',
          commonWrongAnswer: {
            answer: 'An eroded coastline',
            reason: 'Vague non-specific feature — the marking scheme awards 2 marks for a recognised isostatic feature, not for any coastal landform. Erosion features (sea stacks, sea cliffs) aren\'t isostatic and don\'t score on this question.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'q1c-second',
        type: 'short-text',
        prompt: 'Name a second feature in a different Irish location, with a real place name.',
        hint: 'Antrim Coast, Bray Head, Dargle, Liffey valley, Inistioge…',
        debrief: {
          strategicPrinciple: 'Two named examples in DIFFERENT locations earns the +2 SRPs bonus. The bonus only fires if the examples are genuinely distinct — not the same coast or the same valley named twice.',
          commonWrongAnswer: {
            answer: 'The Antrim coast (a raised beach there) and the Antrim coast (a fossil cliff there)',
            reason: 'Repeating the same location for both features misses the +2 SRPs example bonus — the marking scheme rewards two distinct Irish locations, not two features in the same place.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'q1c-mechanism',
        type: 'short-text',
        prompt: 'In one sentence: what is the mechanism of isostasy in post-glacial Ireland?',
        hint: 'Ice load → crustal depression → ice melt → rebound.',
        debrief: {
          strategicPrinciple: 'Mechanism = ice load → crustal depression → ice melt ~10,000 years ago → ongoing rebound. The 2025 marking scheme caps at 2 SRPs for any explanation that describes the mechanism without anchoring it to the Irish landscape.',
          commonWrongAnswer: {
            answer: 'Tectonic plates move and cause the land to rise',
            reason: 'Confusing tectonics with isostasy. Isostasy is vertical adjustment in response to LOAD changes (ice, water, sediment), not plate motion. The 2025 scheme distinguishes isostasy from eustasy (sea-level change); a tectonic answer earns nothing in either category.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
    ],
    biggestMistake: {
      title: 'Writing isostasy theory without anchoring to Ireland',
      body: 'The 2025 marking scheme is explicit: "Max 2 x SRPs if there is merely a description of isostasy without a reference to the impact on the Irish landscape." A textbook-perfect mechanism explanation that never names an Irish location caps at 4 of 30 marks. Lead with Ireland — pick your features first (raised beach in Antrim, fossil cliff at Bray, incised meander at Inistioge), then walk through the isostatic mechanism that produced each one.',
      source: { year: 2025, type: 'marking-scheme' },
    },
  },

  {
    id: 'geo-2025-hl-q2bi',
    taskType: 'geography-physical-process-explanation',
    subject: 'geography',
    year: 2025,
    paper: 'Paper 2',
    section: 'Section 1 — Surface Processes — Deposition',
    questionNumber: '2B(i)',
    level: 'higher',
    marks: 30,
    totalPaperMarks: 320,
    totalPaperMinutes: 140,
    commandWords: ['Examine'],
    questionText: [
      {
        type: 'paragraph',
        content: [
          { text: 'Examine', annotation: { type: 'command', note: 'Detailed analysis required — engage with HOW deposition formed the landform, not just narrate features.' } },
          { text: ' the role of the ' },
          { text: 'process of deposition', annotation: { type: 'keyword', note: 'DEPOSITION ONLY. Marking scheme: "Examination of processes of erosion 0 marks." Half the cohort instinctively writes about erosion when they see a landform question — that earns nothing here.' } },
          { text: ' on the ' },
          { text: 'formation', annotation: { type: 'keyword', note: 'Must link deposition to formation. Marking scheme: "Max of 2 x SRPs if there is merely a description of landform without a reference to formation."' } },
          { text: ' of ' },
          { text: 'one fluvial landform or one coastal landform or one glacial landform', annotation: { type: 'keyword', note: 'Pick ONE. Must be deposition-formed (levee, beach, spit, tombolo, bar, drumlin, esker, moraine, outwash plain, delta, floodplain). NOT erosion-formed (waterfall, sea stack, corrie, U-shaped valley) — wrong category.' } },
          { text: ' that you have studied. ' },
          { text: '(30)', annotation: { type: 'marks-allocation', note: 'Landform named: 2 marks. Examination: 14 SRPs. Mandatory: first 2 SRPs for reference to the role of deposition. +1 SRP for specific named example. +1 SRP for labelled diagram, +2 SRPs for additional info on labelled diagram. Diagram without labels = 0 marks. Not tied to Ireland.' } },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'q2bi-landform',
        type: 'short-text',
        prompt: 'Pick your strongest deposition-formed landform — fluvial, coastal, or glacial.',
        hint: 'Fluvial: levee, floodplain, delta. Coastal: beach, spit, tombolo, bar. Glacial: drumlin, esker, moraine, outwash plain.',
        debrief: {
          strategicPrinciple: 'Pick a landform formed BY deposition (levee, beach, spit, tombolo, bar, drumlin, esker, moraine, outwash plain, delta, floodplain). The 2025 marking scheme caps any examination of erosion processes at 0 marks on this question — wrong category is unrecoverable.',
          commonWrongAnswer: {
            answer: 'A waterfall',
            reason: 'Erosion-formed feature. The 2025 marking scheme states: "Examination of processes of erosion 0 marks." Even a perfectly executed erosion explanation scores nothing — the question examines deposition only.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'q2bi-mechanisms',
        type: 'short-text',
        prompt: 'Name 3 deposition mechanisms (NOT erosion processes) that contribute to your landform.',
        hint: 'For a spit: longshore drift, prevailing wind, sediment supply. For a drumlin: sub-glacial deposition, ice flow direction, till.',
        debrief: {
          strategicPrinciple: 'Each SRP needs to engage with HOW deposition forms the landform — not just describe its appearance. The 2025 marking scheme caps at 2 SRPs for description without formation. Three deposition mechanisms specific to your landform (for a spit: longshore drift, swash/backwash angle, sediment supply at headland) anchors every SRP.',
          commonWrongAnswer: {
            answer: 'Hydraulic action, abrasion, attrition',
            reason: 'All three are erosion processes — they earn 0 marks on this question. Even where erosion and deposition co-occur (longshore drift involves both), the SRPs must be framed around the depositional output, not the erosional input.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'q2bi-example',
        type: 'short-text',
        prompt: 'Specific named example with location for the +1 SRP.',
        hint: 'Spurn Head (England), Inch Strand (Kerry), Clew Bay drumlin field, Mississippi levees…',
        debrief: {
          strategicPrinciple: 'A specific named example with location is worth +1 SRP under the 2025 marking scheme. The marker awards the bonus for a recognisable place — Spurn Head, Inch Strand, Rossbeigh, Clew Bay, Mississippi delta — not for generic location language.',
          commonWrongAnswer: {
            answer: 'Various beaches in Ireland',
            reason: 'Vague — the +1 SRP example bonus requires a specific named location. "Various beaches" identifies without specifying; doesn\'t earn the bonus.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
    ],
    biggestMistake: {
      title: 'Writing about erosion when the question demands deposition',
      body: 'The 2025 marking scheme is unambiguous: "Examination of processes of erosion 0 marks." Half the cohort sees "landform" in the prompt and writes about whatever erosion processes they know best — and earns nothing for technically excellent erosion exposition. Pick your landform first, verify it\'s deposition-formed (levee, beach, spit, drumlin, delta), and frame every SRP around the depositional mechanism that built it.',
      source: { year: 2025, type: 'marking-scheme' },
    },
  },

  {
    id: 'geo-2025-hl-q2c',
    taskType: 'geography-physical-process-explanation',
    subject: 'geography',
    year: 2025,
    paper: 'Paper 2',
    section: 'Section 1 — Weathering',
    questionNumber: '2C',
    level: 'higher',
    marks: 30,
    totalPaperMarks: 320,
    totalPaperMinutes: 140,
    commandWords: ['Explain'],
    questionText: [
      {
        type: 'paragraph',
        content: [
          { text: 'Explain', annotation: { type: 'command', note: 'Mechanism required — name the process, then explain how it actually works step by step. Description alone is insufficient.' } },
          { text: ' ' },
          { text: 'one process of physical weathering', annotation: { type: 'keyword', note: 'Mechanical breakdown without chemical change — freeze-thaw, exfoliation, frost shattering. Naming earns 2 marks; the explanation earns SRPs.' } },
          { text: ' and ' },
          { text: 'one process of chemical weathering', annotation: { type: 'trap', note: 'AND not OR. Marking scheme: "If only physical weathering process or chemical weathering process explained max 7 x SRPs." That caps you at ~14 marks of 30 — half marks gone before you start.' } },
          { text: '. ' },
          { text: '(30)', annotation: { type: 'marks-allocation', note: 'Physical process named: 2 marks. Chemical process named: 2 marks. Explanation of physical: 7/6 SRPs. Explanation of chemical: 6/7 SRPs (examiner allocates the extra SRP to the more developed half). +1 SRP for example. +1 SRP for labelled diagram, +2 SRPs for additional info. Diagram without labels = 0 marks. Not tied to Ireland.' } },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'q2c-pair',
        type: 'short-text',
        prompt: 'Name your one physical AND one chemical process. State the rock type each typically affects.',
        hint: 'Physical examples: freeze-thaw (any jointed rock); exfoliation (granite). Chemical: carbonation (limestone); oxidation (iron-rich rocks); hydrolysis (granite/feldspar).',
        debrief: {
          strategicPrinciple: 'Each process named earns 2 marks (4 marks total for both names). The 2025 marking scheme requires BOTH a physical and a chemical process — "if only physical weathering process or chemical weathering process explained max 7 x SRPs," capping you at roughly half marks before you start.',
          commonWrongAnswer: {
            answer: 'Freeze-thaw and exfoliation',
            reason: 'Both are physical processes — misses the "and a chemical process" requirement entirely. The 2025 marking scheme caps you at 7 SRPs (~14 of 30 marks) for doing only one category, regardless of how well each process is explained.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'q2c-conditions',
        type: 'short-text',
        prompt: 'For each process: list 3 conditions or inputs needed (temperature, water, gas).',
        hint: 'Freeze-thaw: water, jointed rock, temp fluctuation around 0°C. Carbonation: rainwater + atmospheric CO₂ + limestone.',
        debrief: {
          strategicPrinciple: 'Naming the process earns 2 marks; the SRPs come from the mechanism. Each condition or input is an SRP opportunity (freeze-thaw needs water, jointed rock, temperature fluctuation around 0°C, repeated cycles). Generic "rock breaks down" earns no SRP because there\'s no mechanism to credit.',
          commonWrongAnswer: {
            answer: 'Water gets in cracks and breaks the rock',
            reason: 'Reads as description, not explanation — no temperature, no expansion percentage, no repeated cycles. The 2025 marking scheme rewards SRPs that name the conditions and the step-by-step process; a one-line summary earns at most the identification mark.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'q2c-distinguish',
        type: 'multiple-choice',
        prompt: 'Which is chemical weathering, which is physical?',
        options: [
          'Freeze-thaw is chemical, carbonation is physical',
          'Freeze-thaw is physical, carbonation is chemical',
          'Both are physical',
          'Both are chemical',
        ],
        correctAnswer: 'Freeze-thaw is physical, carbonation is chemical',
        debrief: {
          strategicPrinciple: 'Physical weathering = mechanical breakdown without chemical change (freeze-thaw, exfoliation, frost shattering). Chemical weathering = rock chemistry alters (carbonation, oxidation, hydrolysis). Mixing the categories puts the 2-mark naming credit at risk.',
          commonWrongAnswer: {
            answer: 'Freeze-thaw is chemical, carbonation is physical',
            reason: 'Inverted classification — freeze-thaw involves no chemical reaction (water just changes phase), while carbonation involves an acid-base reaction (H₂CO₃ + CaCO₃). Getting this wrong loses the 2-mark naming credit for both processes.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
    ],
    biggestMistake: {
      title: 'Doing only one weathering type — capped at half marks',
      body: 'The 2025 marking scheme is explicit: "If only physical weathering process or chemical weathering process explained max 7 x SRPs." The "and" in the question is enforced — doing only one process (no matter how thoroughly) caps you at roughly 14 marks of 30 before any other consideration. Author both halves to a similar standard; the marker allocates the extra SRP to whichever you developed better, but you need both on the page.',
      source: { year: 2025, type: 'marking-scheme' },
    },
  },

  {
    id: 'geo-2025-hl-q4b',
    taskType: 'geography-regional-economic-activity',
    subject: 'geography',
    year: 2025,
    paper: 'Paper 2',
    section: 'Section 2 — Regional Geography — Primary Economic Activity',
    questionNumber: '4B',
    level: 'higher',
    marks: 30,
    totalPaperMarks: 320,
    totalPaperMinutes: 140,
    commandWords: ['Examine'],
    questionText: [
      {
        type: 'paragraph',
        content: [
          { text: 'Examine', annotation: { type: 'command', note: 'Detailed analysis — each SRP must engage with how the factor influenced primary activity development, not just describe the factor in isolation.' } },
          { text: ' ' },
          { text: 'two factors', annotation: { type: 'keyword', note: 'TWO factors required. Marking scheme: "Max 7 x SRPs if there is only one factor examined." Doing only one caps you at 14 marks of 30. Factors can be physical (climate, soil, relief) and/or human (technology, market access, government policy, labour).' } },
          { text: ' that have influenced the development of ' },
          { text: 'primary economic activity', annotation: { type: 'keyword', note: 'Primary = farming, fishing, mining, forestry, quarrying. NOT secondary (manufacturing) or tertiary (services). Confusing categories loses marks.' } },
          { text: ' in a ' },
          { text: 'Continental / Sub-Continental region', annotation: { type: 'keyword', note: 'A large land-based region (India, Brazil, US Midwest, Sahel, Amazon Basin). Marking scheme: "Examination without link to a named or clearly inferred region 0 marks." Generic "Asia" or "Africa" earns 0 marks.' } },
          { text: ' ' },
          { text: '(not in Europe)', annotation: { type: 'trap', note: 'BIGGEST REGIONAL TRAP ON THE PAPER. Marking scheme: "Do not accept examination of primary activity in an Irish or European region." If you write about France, Germany, or Ireland here, you score 0. Choose your region BEFORE you start writing.' } },
          { text: ' that you have studied. ' },
          { text: '(30)', annotation: { type: 'marks-allocation', note: 'Factors identified: 2+2 marks. Examination of Factor 1: 7/6 SRPs. Examination of Factor 2: 6/7 SRPs (extra SRP allocated to better-developed factor). +2 SRPs for specific examples of primary economic activity. +1 SRP for labelled sketch map, +1 SRP for additional info on sketch map. Max 1 SRP per factor if merely describing the factor without linking to development of primary activity.' } },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'q4b-region',
        type: 'short-text',
        prompt: 'Name your Continental/Sub-Continental region (NOT in Europe).',
        hint: 'India? Brazil? US Midwest? Sahel? Amazon Basin? Be specific — "Asia" alone is 0 marks.',
        debrief: {
          strategicPrinciple: 'The region must be specifically named and located. The 2025 marking scheme states: "Examination without link to a named or clearly inferred region 0 marks." Generic "Asia" or "Africa" earns nothing — you need India / Brazil / US Midwest / Sahel / Amazon Basin level of specificity.',
          commonWrongAnswer: {
            answer: 'Asia',
            reason: 'Too generic — "Asia" spans the Indian monsoon belt, Siberian permafrost, Saudi desert, and Indonesian rainforest. The marker can\'t award SRPs to a region this loose. The 2025 marking scheme requires a named or clearly inferred sub-region.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'q4b-factors',
        type: 'short-text',
        prompt: 'Name your two factors. Mix is fine — physical (climate, soil, relief) and/or human (technology, government policy, market access, labour).',
        hint: 'For India: Indian monsoon climate + Green Revolution technology. For US Midwest: prairie soils + market access via rail.',
        debrief: {
          strategicPrinciple: 'Two factors are required and each one must link explicitly to the development of primary activity. The 2025 marking scheme: "Max 1 SRP per factor if merely describing the factor without linking to development of primary activity." Describing the climate is not enough — show how the climate enabled a specific primary activity.',
          commonWrongAnswer: {
            answer: 'The climate is hot and wet',
            reason: 'Describes the factor without linking it to primary activity development. The 2025 scheme caps this at 1 SRP per factor — you need the chain "hot and wet → enables rice paddy cultivation in the kharif season → sustains intensive multi-crop rotation in the Ganges plain."',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'q4b-not-europe',
        type: 'multiple-choice',
        prompt: 'You write a brilliant answer about primary activity in France. Mark out of 30?',
        options: ['30', '20', '10', '0'],
        correctAnswer: '0',
        debrief: {
          strategicPrinciple: 'The "not in Europe" constraint is absolute. The 2025 marking scheme states: "Do not accept examination of primary activity in an Irish or European region." Even a perfect answer about France or Germany scores 0 because the question excludes European regions entirely.',
          commonWrongAnswer: {
            answer: '20',
            reason: 'Underestimates the severity of the regional constraint. Some constraints reduce marks proportionally — this one zeroes the question. The 2025 scheme is binary on region: in-scope = scored normally, out-of-scope = 0. Author always answers in writing should verify region BEFORE committing to a paragraph.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
    ],
    biggestMistake: {
      title: 'Writing about a European region — 0 marks regardless of quality',
      body: 'The 2025 marking scheme is unambiguous: "Do not accept examination of primary activity in an Irish or European region." A brilliantly argued answer about French viticulture or German Bavarian dairy farming scores 0 of 30 because the question excludes Europe. This is the single most common way students lose this question. Pick your region (India, Brazil, US Midwest, Sahel) BEFORE you start writing, and write the region name at the top of your answer as a self-check.',
      source: { year: 2025, type: 'marking-scheme' },
    },
  },
];
