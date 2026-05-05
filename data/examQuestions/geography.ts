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
      },
      {
        id: 'q1c-second',
        type: 'short-text',
        prompt: 'Name a second feature in a different Irish location, with a real place name.',
        hint: 'Antrim Coast, Bray Head, Dargle, Liffey valley, Inistioge…',
      },
      {
        id: 'q1c-mechanism',
        type: 'short-text',
        prompt: 'In one sentence: what is the mechanism of isostasy in post-glacial Ireland?',
        hint: 'Ice load → crustal depression → ice melt → rebound.',
      },
    ],
    topAnswerIncludes: [
      "Definition: isostasy is the vertical adjustment of the Earth's crust in response to changes in load (ice, sediment, water).",
      'Mechanism: during the last Ice Age, ice sheets several hundred metres thick depressed the Irish landmass into the underlying mantle. As ice melted ~10,000 years ago, the land began rebounding upward — a process still ongoing today.',
      'Feature 1 — Raised beaches: former shorelines now elevated above current sea level, common along the north Antrim coast (Portrush, Cushendun).',
      'Feature 2 — Fossil/relic cliffs: cliffs no longer facing the sea due to land emergence, e.g. inland from Bray Head or Howth Head.',
      'Feature 3 — Rejuvenation features (knickpoints, waterfalls, river terraces): rivers re-cut their channels into uplifted land — Dargle waterfall in Wicklow, terraces along the Liffey.',
      'Feature 4 — Incised meanders: meanders cut deep into bedrock as land rose, e.g. River Nore at Inistioge.',
      'Two named Irish examples in different locations earns the +2 SRPs example credit.',
      'Labelled diagram showing ice load → depression → melt → rebound, with arrows and labelled crust/mantle/ice. Additional labelled detail (timeframe, depth) earns the +2 SRPs diagram-info bonus.',
    ],
    commonTraps: [
      'Writing about isostasy as a theoretical process without anchoring to Ireland — caps at 2 SRPs (4 marks). The marking scheme is explicit on this.',
      'Using foreign examples (Scotland, Norway, Hudson Bay) — 0 marks here; the question is tied to Ireland.',
      'Confusing isostasy with eustasy — coastal emergence is accepted but the explanation must be isostatic, not sea-level change.',
      'Diagram without labels — 0 marks. The diagram bonus only applies when fully labelled.',
      'Repeating the same Irish location for every feature — the +2 SRPs requires two DIFFERENT examples.',
      'Listing features without explaining the isostatic mechanism — partial credit only. Each feature needs identification (2 marks) plus mechanism explanation (SRPs).',
    ],
  },

  {
    id: 'geo-2025-hl-q2bi',
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
      },
      {
        id: 'q2bi-mechanisms',
        type: 'short-text',
        prompt: 'Name 3 deposition mechanisms (NOT erosion processes) that contribute to your landform.',
        hint: 'For a spit: longshore drift, prevailing wind, sediment supply. For a drumlin: sub-glacial deposition, ice flow direction, till.',
      },
      {
        id: 'q2bi-example',
        type: 'short-text',
        prompt: 'Specific named example with location for the +1 SRP.',
        hint: 'Spurn Head (England), Inch Strand (Kerry), Clew Bay drumlin field, Mississippi levees…',
      },
    ],
    topAnswerIncludes: [
      "Landform clearly named and identified as a deposition feature (e.g. 'A spit is a long, narrow ridge of deposited sediment extending from the coast…').",
      'EXAMPLE — Spit: longshore drift carries sediment along coast in zig-zag pattern (swash up at angle, backwash straight back); where coastline changes direction, sediment continues in original direction; deposited in calmer water, gradually building outward; recurved end forms from secondary winds; e.g. Inch Strand (Kerry), Rossbeigh, Spurn Head.',
      'EXAMPLE — Levee: river floods over banks; energy drops sharply on contact with floodplain; coarse sediment dropped first at edges, finer carried further; over repeated floods, banks build above floodplain level; e.g. Mississippi, Po, lower Shannon.',
      'EXAMPLE — Drumlin: sub-glacial deposition of till, moulded by ice flow into elongated egg-shape; steep stoss side faces ice direction, gentle lee side; deposition occurs when ice loses competence to carry load; e.g. Clew Bay drumlin field, Co. Down "Basket of Eggs" topography.',
      'Specific named example with location (+1 SRP).',
      'Labelled diagram showing the deposition process building the landform (cross-section with arrows showing sediment movement, deposition zones marked). Additional labelled detail earns +2 SRPs.',
      'Repeated explicit reference to deposition as the formative process — not just deposition mentioned once and then narrative drift.',
    ],
    commonTraps: [
      'Writing about EROSION processes (hydraulic action, abrasion, attrition, solution) — 0 marks per the marking scheme.',
      'Picking a landform formed mainly by erosion (waterfall, sea stack, corrie, U-shaped valley) — wrong category. Even a perfect answer scores low.',
      'Just describing what the landform looks like without explaining how deposition formed it — caps at 2 SRPs (4 marks).',
      'Mentioning deposition once at the start then drifting into general landform narrative — each SRP needs to engage with deposition.',
      'Diagram without labels — 0 marks for the diagram.',
      'No specific named example — losing 1 free SRP.',
    ],
  },

  {
    id: 'geo-2025-hl-q2c',
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
      },
      {
        id: 'q2c-conditions',
        type: 'short-text',
        prompt: 'For each process: list 3 conditions or inputs needed (temperature, water, gas).',
        hint: 'Freeze-thaw: water, jointed rock, temp fluctuation around 0°C. Carbonation: rainwater + atmospheric CO₂ + limestone.',
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
      },
    ],
    topAnswerIncludes: [
      'PHYSICAL — Freeze-thaw (frost shattering): water enters cracks/joints in rock; overnight temperatures drop below 0°C; water freezes and expands by ~9%; expansion exerts pressure on surrounding rock; cracks widen with each cycle; over many cycles, fragments break off; produces angular scree at base of slopes; common in upland Ireland (Wicklow Mountains, Errigal) and high mountain regions.',
      'CHEMICAL — Carbonation: rainwater absorbs CO₂ to form weak carbonic acid (H₂O + CO₂ → H₂CO₃); acid reacts with calcium carbonate in limestone (CaCO₃ + H₂CO₃ → Ca(HCO₃)₂); calcium bicarbonate is soluble and carried away in solution; widens joints and bedding planes; produces karst landscapes (the Burren) with clints, grikes, swallow holes, caves.',
      'Alternative physical: exfoliation/onion-skin — diurnal heating/cooling causes outer rock layers to expand and contract differently from interior, eventually peeling off (granite domes in arid regions like Yosemite, Uluru).',
      'Alternative chemical: oxidation — iron-bearing minerals react with oxygen in presence of water, forming iron oxide (rust); weakens rock structure; common in granite with biotite mica or in basalt.',
      'Specific examples (the Burren for carbonation; Wicklow scree slopes for freeze-thaw) — +1 SRP each.',
      'Labelled diagrams of both processes — cross-sections with arrows showing water entry, freezing, expansion (physical) or chemical reaction zones (chemical). Diagram without labels: 0 marks.',
    ],
    commonTraps: [
      'Doing only one process — caps at 7 SRPs (14 marks of 30). The "and" is enforced by the marking scheme.',
      'Mixing up the two categories — labelling carbonation as physical, or freeze-thaw as chemical. The 2-mark naming credit is at risk.',
      'Naming the process but not explaining the mechanism — saying "freeze-thaw breaks down rock" without the freezing/expansion/9%/repeated-cycles steps.',
      'Confusing weathering (in situ breakdown) with erosion (transport of weathered material).',
      'Diagrams without labels — 0 marks each.',
      'Generic "water gets in cracks and breaks rock" answers without specifying temperature, expansion percentage, or repeated cycles — reads as description, not explanation.',
    ],
  },

  {
    id: 'geo-2025-hl-q4b',
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
      },
      {
        id: 'q4b-factors',
        type: 'short-text',
        prompt: 'Name your two factors. Mix is fine — physical (climate, soil, relief) and/or human (technology, government policy, market access, labour).',
        hint: 'For India: Indian monsoon climate + Green Revolution technology. For US Midwest: prairie soils + market access via rail.',
      },
      {
        id: 'q4b-not-europe',
        type: 'multiple-choice',
        prompt: 'You write a brilliant answer about primary activity in France. Mark out of 30?',
        options: ['30', '20', '10', '0'],
        correctAnswer: '0',
      },
    ],
    topAnswerIncludes: [
      "Region clearly named and located (e.g. 'India, focusing on the Indo-Gangetic Plain' or 'the US Midwest Corn Belt').",
      'FACTOR 1 (Climate, India): Indian monsoon system — kharif season (Jun-Sept) brings heavy rainfall to Ganges plain enabling rice paddy cultivation; rabi season (Oct-Mar) cooler conditions support wheat in Punjab and Haryana; drought-prone Deccan Plateau limited to drought-resistant millet and sorghum; rainfall variability creates risk for farmers.',
      'FACTOR 2 (Soil, India): deep alluvial soils of Indo-Gangetic Plain deposited by Himalayan rivers — extremely fertile, high water retention, support intensive multi-crop rotation (rice, wheat, sugarcane); thinner black regur soils on Deccan suit cotton; laterite soils in south require fertiliser inputs.',
      'FACTOR 2 alternative (Government policy, India): Green Revolution from 1960s — HYV seeds, irrigation expansion, subsidised fertilisers, improved storage and credit; transformed Punjab into India\'s breadbasket; doubled wheat yields 1965-80.',
      'Specific examples of primary activity (rice paddies of West Bengal, wheat farms of Punjab, beef ranching in Brazilian cerrado, corn in Iowa) — +2 SRPs.',
      'Sketch map of region with major agricultural zones / climate regions labelled (+1 SRP map, +1 SRP additional labelled info).',
    ],
    commonTraps: [
      'Writing about Ireland, France, Germany, or any European region — 0 MARKS. The "not in Europe" constraint is absolute. The most common way students score 0 on this question.',
      'Vague references to "Asia" or "Africa" without naming a specific region — 0 marks per the scheme: "Examination without link to a named or clearly inferred region 0 marks."',
      'Doing only one factor — caps at 7 SRPs (14 marks).',
      'Just describing the factor (e.g. "the climate is hot and wet") without linking it to the development of primary activity — caps at 1 SRP per factor.',
      'Confusing primary (farming, fishing, mining, forestry) with secondary (manufacturing) or tertiary (services).',
      'Sketch map without labels — loses the diagram credit.',
    ],
  },
];
