/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Marking Lens — Engineering (Materials and Technology), Higher Level.
 *
 * Sources of truth (all in examiner-reports/engineering/):
 *  - 2024-marking-scheme.md — SEC Marking Scheme 2024, Engineering HL
 *  - 2025-marking-scheme.md — SEC Marking Scheme 2025, Engineering HL
 * Every notation below is verbatim from the named document (the p.6 mark grid
 * cross-checked against the per-question body pages, which repeat each part's
 * notation under its model answer); every entry's parts sum to the printed
 * 50-mark question total (machine-checked).
 *
 * Paper model: HL written paper = 9 questions x 50 marks, "Answer any six
 * questions." Q1 is the short-answer menu ("Any ten @ 5 marks each" from
 * thirteen printed parts); Q2-Q9 are structured long questions. Several final
 * parts print an OR fork — two mutually exclusive routes to the same 16 marks —
 * modelled here as a single row so the ladder still sums honestly.
 *
 * Keys (year/level/lang/fileid/n) match the Topic Vault tags exactly:
 *  - 2024 HL (LC027ALP000EV + IV mirror) Q1-9
 *  - 2025 HL (LC027ALP000EV + IV mirror) Q1-9
 * EV/IV are English/Irish language versions of the SAME paper marked by the
 * same scheme, so EV entries are mirrored to the IV fileid (business.ts
 * pattern). No Ordinary Level scheme is filed, so OL sittings carry no lens.
 *
 * No pitfall entries: no Chief Examiner's Report exists for LC Engineering
 * (see examiner-reports/engineering/2025-insights.md — "No recent Irish LC
 * Engineering Chief Examiner's Report was locatable").
 */

import { type QuestionLens, type SubjectLens } from './types';

const CITE_2024 = (q: string) =>
  `SEC Marking Scheme 2024, Engineering (Materials and Technology) Higher Level, ${q}`;
const CITE_2025 = (q: string) =>
  `SEC Marking Scheme 2025, Engineering (Materials and Technology) Higher Level, ${q}`;

// The IV paper is the same exam marked by the same scheme — mirror EV entries.
const mirrorIV = (entries: QuestionLens[], fileid: string): QuestionLens[] =>
  entries.map(e => ({ ...e, lang: 'iv', fileid }));

// ════════════════════════════════════════════════════════════════════════════
// 2024 Higher Level — written paper (LC027ALP000EV, Q1-9, 50 marks each)
// Source: examiner-reports/engineering/2024-marking-scheme.md
// ════════════════════════════════════════════════════════════════════════════

const HL_2024_EV: QuestionLens[] = [
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC027ALP000EV.pdf', n: '1',
    totalMarks: 50,
    headline: 'The short-answer menu: thirteen parts (a)-(m) printed, only the best ten count at 5 marks each.',
    parts: [
      {
        part: '',
        task: 'Thirteen short-answer parts (a)-(m) — facial recognition, adhesive safety, parallax error, standing desks, engineers (any one of three), implant materials, aluminium, elastomers, extrusion, hardness tests, pyro- vs hydrometallurgy, cordless tools, solar-panel tilt mechanism',
        notation: 'Any ten @ 5 marks each.',
        decoded: 'Only the best ten of the thirteen parts count, 5 marks each. The scheme marks each part either as a single 5 or split 3 + 2 (e.g. (a) 3 + 2, (c) 5, (e) Any one @ 5, (m) 5).',
        marks: 50,
      },
    ],
    cite: CITE_2024('Q1'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC027ALP000EV.pdf', n: '2',
    totalMarks: 50,
    headline: 'Container-ships question: eight 5-mark parts plus a closing "Any two @ 5 + 5" menu.',
    parts: [
      { part: '(a)(i)', task: 'Why container ships are extensively used to move goods', notation: '3 + 2', decoded: 'Main point 3 marks + development 2 marks.', marks: 5 },
      { part: '(a)(ii)', task: 'Hazards faced by container ships at sea', notation: '3 + 2', decoded: 'Main point 3 marks + development 2 marks.', marks: 5 },
      { part: '(b)(i)', task: 'What TEU stands for and its standard basis', notation: '5', decoded: 'A single 5-mark granule for the answer.', marks: 5 },
      { part: '(b)(ii)', task: 'Describe container ship types (Feeder, Panamax, ULCV)', notation: '5', decoded: 'A single 5-mark granule for the answer.', marks: 5 },
      { part: '(c)(i)', task: 'Suitability of bronze for ship propellers', notation: '3 + 2', decoded: 'Main point 3 marks + development 2 marks.', marks: 5 },
      { part: '(c)(ii)', task: 'Ship stability: centre of gravity and hull shape', notation: '5', decoded: 'A single 5-mark granule for the answer.', marks: 5 },
      { part: '(d)(i)', task: 'Two-stroke diesel engines: speed and propulsion of container ships', notation: '5', decoded: 'A single 5-mark granule for the answer.', marks: 5 },
      { part: '(d)(ii)', task: 'How a container ship is steered (rudder / steering gear)', notation: '5', decoded: 'A single 5-mark granule for the answer.', marks: 5 },
      { part: '(e)', task: 'Environmental impact of container ships: ballast water management, oil leakage, emissions', notation: 'Any two @ 5 + 5', decoded: 'The best two of the three listed topics count, 5 marks each.', marks: 10 },
    ],
    cite: CITE_2024('Q2'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC027ALP000EV.pdf', n: '3',
    totalMarks: 50,
    headline: 'Materials-testing question: the stress-strain graph alone carries 10 of the 50 marks.',
    parts: [
      { part: '(a)(i)', task: 'Benefits of a custom-made carbon fibre shin guard', notation: '2 + 2', decoded: 'Two elements, 2 marks each.', marks: 4 },
      { part: '(a)(ii)', task: 'Define material toughness', notation: '4', decoded: 'A single 4-mark granule for the definition.', marks: 4 },
      { part: '(a)(iii)', task: 'Describe impact testing (Izod / Charpy)', notation: '8', decoded: 'A single 8-mark granule for the description.', marks: 8 },
      { part: '(b)(i)', task: 'Draw the stress-strain graph from the tabled data', notation: '10', decoded: 'Ten marks for the plotted graph.', marks: 10 },
      { part: '(b)(ii)', task: 'Calculate Young’s Modulus of Elasticity', notation: '4', decoded: 'Four marks for the calculation (the model shows formula, substitution and answer with unit: 90 kN/mm²).', marks: 4 },
      { part: '(b)(iii)', task: 'Explain necking and cup-and-cone fracture', notation: '2 + 2', decoded: 'Each of the two terms earns 2 marks.', marks: 4 },
      { part: '(c)(i)', task: 'Reasons for non-destructive testing (NDT) of the linkage arm', notation: '4 + 4', decoded: 'Two reasons, 4 marks each.', marks: 8 },
      { part: '(c)(ii)', task: 'Describe radiography (X-ray) NDT', notation: '8', decoded: 'A single 8-mark granule for the description.', marks: 8 },
    ],
    cite: CITE_2024('Q3'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC027ALP000EV.pdf', n: '4',
    totalMarks: 50,
    headline: 'Heat-treatment question: five 1-mark diagram labels, then an "Any two @ 8 + 8" closing menu.',
    parts: [
      { part: '(a)(i)', task: 'Reasons for hardening and tempering the brake disc', notation: '8', decoded: 'A single 8-mark granule covering both treatments.', marks: 8 },
      { part: '(a)(ii)', task: 'Describe induction hardening', notation: '8', decoded: 'A single 8-mark granule for the description.', marks: 8 },
      { part: '(b)(i)', task: 'Identify regions A-E of the iron-carbon thermal equilibrium diagram', notation: '1 + 1 + 1 + 1 + 1', decoded: 'Each of the five labels earns 1 mark.', marks: 5 },
      { part: '(b)(ii)', task: 'Describe annealing of 0.6% carbon steel', notation: '7', decoded: 'A single 7-mark granule for the description.', marks: 7 },
      { part: '(b)(iii)', task: 'Effects of full annealing on the metal', notation: '3 + 3', decoded: 'Two elements, 3 marks each.', marks: 6 },
      { part: '(c)', task: 'Work hardening; safety hazards of flame hardening; eutectic vs eutectoid point', notation: 'Any two @ 8 + 8', decoded: 'The best two of the three listed topics count, 8 marks each.', marks: 16 },
    ],
    cite: CITE_2024('Q4'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC027ALP000EV.pdf', n: '5',
    totalMarks: 50,
    headline: 'Crystal-structures question: the thermal equilibrium diagram carries 10 marks, closing on "Any two @ 8 + 8".',
    parts: [
      { part: '(a)(i)', task: 'Describe dendritic growth', notation: '8', decoded: 'A single 8-mark granule for the description.', marks: 8 },
      { part: '(a)(ii)', task: 'Impact of a line defect (dislocations) in crystal structures', notation: '8', decoded: 'A single 8-mark granule for the answer.', marks: 8 },
      { part: '(b)(i)', task: 'Draw the thermal equilibrium diagram from the tabled data', notation: '10', decoded: 'Ten marks for the drawn diagram.', marks: 10 },
      { part: '(b)(ii)', task: 'Sketch the cooling curve for the alloy of 30% metal B', notation: '4', decoded: 'Four marks for the cooling curve.', marks: 4 },
      { part: '(b)(iii)', task: 'Determine temperatures A and B from the diagram', notation: '2 + 2', decoded: 'Each of the two temperatures earns 2 marks.', marks: 4 },
      { part: '(c)', task: 'Sacrificial protection for offshore wind farms; protecting steel from corrosion; FCC structure and ductility', notation: 'Any two @ 8 + 8', decoded: 'The best two of the three listed topics count, 8 marks each.', marks: 16 },
    ],
    cite: CITE_2024('Q5'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC027ALP000EV.pdf', n: '6',
    totalMarks: 50,
    headline: 'Welding question: answer (a) and (b) and EITHER part of (c) — both (c) routes are worth the same 16 marks.',
    parts: [
      { part: '(a)(i)', task: 'Reasons for TIG welding the stainless steel storage tank', notation: 'Any two @ 3 + 3', decoded: 'The best two reasons count, 3 marks each.', marks: 6 },
      { part: '(a)(ii)', task: 'Describe the TIG welding process', notation: '10', decoded: 'A single 10-mark granule for the description.', marks: 10 },
      { part: '(b)', task: 'Welding items menu: electric-shock/light/fume safety; spot welding; inert gas in MIG; X-ray porosity check; transformer operation', notation: 'Any three @ 6 + 6 + 6', decoded: 'The best three of the five listed items count, 6 marks each.', marks: 18 },
      { part: '(c)', task: 'EITHER oxy-acetylene welding (equipment, flame types, safety features, applications) OR (i) benefits of robotic pipe inspection (ii) remote visual inspection applications', notation: '16 · OR (i) 4 + 4 (ii) 4 + 4', decoded: 'One route only: the oxy-acetylene description is a single 16-mark granule; the alternative route splits the same 16 as two 4-mark points in each of (i) and (ii).', marks: 16 },
    ],
    cite: CITE_2024('Q6'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC027ALP000EV.pdf', n: '7',
    totalMarks: 50,
    headline: 'Polymers question: paired 3 + 3 identifications, an "Any three @ 6 + 6 + 6" menu, then bioplastics.',
    parts: [
      { part: '(a)(i)', task: 'Name the manufacturing process for the hose reel and the hose pipe', notation: '3 + 3', decoded: 'Each named process earns 3 marks.', marks: 6 },
      { part: '(a)(ii)', task: 'Describe plastic extrusion', notation: '8', decoded: 'A single 8-mark granule for the description.', marks: 8 },
      { part: '(a)(iii)', task: 'Function of plasticisers and stabilisers as additives', notation: '3 + 3', decoded: 'Each of the two additives earns 3 marks.', marks: 6 },
      { part: '(b)', task: 'Polymer items menu: upcycling plastics; glass transition temperature; polymer lamination; thermosetting polymers; blow moulding', notation: 'Any three @ 6 + 6 + 6', decoded: 'The best three of the five listed items count, 6 marks each.', marks: 18 },
      { part: '(c)(i)', task: 'Explain bioplastic', notation: '6', decoded: 'A single 6-mark granule for the explanation.', marks: 6 },
      { part: '(c)(ii)', task: 'Advantages of rapid prototyping techniques', notation: '2 + 2 + 2', decoded: 'Three advantages, 2 marks each.', marks: 6 },
    ],
    cite: CITE_2024('Q7'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC027ALP000EV.pdf', n: '8',
    totalMarks: 50,
    headline: 'Machining question: answer (a) and (b) and EITHER part of (c) — both (c) routes total 16 marks.',
    parts: [
      { part: '(a)(i)', task: 'Lathe processes used to manufacture the component (three shown)', notation: '3 + 3 + 3', decoded: 'Each of the three processes earns 3 marks.', marks: 9 },
      { part: '(a)(ii)', task: 'Factors affecting material surface finish on a lathe', notation: '4 + 3', decoded: 'First element 4 marks, second element 3 marks.', marks: 7 },
      { part: '(b)', task: 'Machining items menu: generating vs forming; balancing a grinding wheel; clearance and rake angles; magnetic chuck; countersunk vs counterbored holes', notation: 'Any three @ 6 + 6 + 6', decoded: 'The best three of the five listed items count, 6 marks each.', marks: 18 },
      { part: '(c)', task: 'EITHER (i) reasons for a sealed lubrication system (ii) lubricating materials OR (i) CNC milling vs laser cutting (ii) safety features of computerised machines', notation: '(i) 4 + 4 (ii) 4 + 4 · OR (i) 8 (ii) 4 + 4', decoded: 'One route only, 16 marks either way: the first route pays two 4-mark points in each sub-part; the alternative pays a single 8 then two 4-mark points.', marks: 16 },
    ],
    cite: CITE_2024('Q8'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC027ALP000EV.pdf', n: '9',
    totalMarks: 50,
    headline: 'Mechanisms/electronics question: two 8-mark design answers, a five-item menu, then an OR fork worth 16.',
    parts: [
      { part: '(a)(i)', task: 'Operation of the automatic sliding doors (belt-and-pulley system)', notation: '8', decoded: 'A single 8-mark granule for the description.', marks: 8 },
      { part: '(a)(ii)', task: 'Suggest an alternative mechanism to open/close the sliding doors (model: rack and pinion)', notation: '8', decoded: 'Eight marks for a viable suggested mechanism — the scheme accepts other valid solutions.', marks: 8 },
      { part: '(b)', task: 'Mechanisms/electronics menu: LDR; universal joint; helical vs spur gears; clutch mechanism; relay', notation: 'Any three @ 6 + 6 + 6', decoded: 'The best three of the five listed items count, 6 marks each.', marks: 18 },
      { part: '(c)', task: 'EITHER (i) design features of a racing-car safety harness (ii) suitable harness material OR (i) benefits of LED lights (ii) advantages of sensor-activated lighting', notation: '(i) 4 + 4 (ii) 8 · OR (i) 4 + 4 (ii) 4 + 4', decoded: 'One route only, 16 marks either way: the harness route pays two 4-mark features then a single 8 for the material; the LED route pays two 4-mark points in each sub-part.', marks: 16 },
    ],
    cite: CITE_2024('Q9'),
  },
];

// ════════════════════════════════════════════════════════════════════════════
// 2025 Higher Level — written paper (LC027ALP000EV, Q1-9, 50 marks each)
// Source: examiner-reports/engineering/2025-marking-scheme.md
// ════════════════════════════════════════════════════════════════════════════

const HL_2025_EV: QuestionLens[] = [
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC027ALP000EV.pdf', n: '1',
    totalMarks: 50,
    headline: 'The short-answer menu: thirteen parts (a)-(m) printed, only the best ten count at 5 marks each.',
    parts: [
      {
        part: '',
        task: 'Thirteen short-answer parts (a)-(m) — voice-activated technology, heatsink function, cutting-fluid safety, cast iron kettlebells, engineers (any one of three), Deposit Return Scheme, absolute vs incremental dimensioning, anodised aluminium, factor of safety, lathe processes, electromagnet operation, pneumatic dentistry equipment, stainless steel braces',
        notation: 'Any ten @ 5 marks each.',
        decoded: 'Only the best ten of the thirteen parts count, 5 marks each. The scheme marks each part either as a single 5 or split 3 + 2 (e.g. (a) 3 + 2, (b) 5, (e) Any one @ 5, (g) 5).',
        marks: 50,
      },
    ],
    cite: CITE_2025('Q1'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC027ALP000EV.pdf', n: '2',
    totalMarks: 50,
    headline: 'Hydrogen-energy question: six 5-mark parts, a 10-mark fuel-cell description, and an "Any two @ 5 + 5" menu.',
    parts: [
      { part: '(a)(i)', task: 'Main properties of hydrogen', notation: '5', decoded: 'A single 5-mark granule for the answer.', marks: 5 },
      { part: '(a)(ii)', task: 'Advantages of using hydrogen as a fuel source', notation: '3 + 2', decoded: 'Main point 3 marks + development 2 marks.', marks: 5 },
      { part: '(b)(i)', task: 'Describe steam methane reforming (SMR)', notation: '5', decoded: 'A single 5-mark granule for the description.', marks: 5 },
      { part: '(b)(ii)', task: 'SMR data: feedstocks, energy input, emissions', notation: '5', decoded: 'A single 5-mark granule for the answer.', marks: 5 },
      { part: '(c)(i)', task: 'Importance of research and development in hydrogen energy technology', notation: '3 + 2', decoded: 'Main point 3 marks + development 2 marks.', marks: 5 },
      { part: '(c)(ii)', task: 'Hydrogen energy use in data centres vs agriculture', notation: '5', decoded: 'A single 5-mark granule for the answer.', marks: 5 },
      { part: '(d)', task: 'Principle of operation of a hydrogen fuel cell', notation: '10', decoded: 'A single 10-mark granule for the description.', marks: 10 },
      { part: '(e)', task: 'Hydrogen topics: green hydrogen production, energy storage, safety concerns', notation: 'Any two @ 5 + 5', decoded: 'The best two of the three listed topics count, 5 marks each.', marks: 10 },
    ],
    cite: CITE_2025('Q2'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC027ALP000EV.pdf', n: '3',
    totalMarks: 50,
    headline: 'Materials-testing question: the load-extension graph carries 10 marks plus 2 + 2 + 2 for its marked features.',
    parts: [
      { part: '(a)(i)', task: 'Explain metal fatigue', notation: '4', decoded: 'A single 4-mark granule for the explanation.', marks: 4 },
      { part: '(a)(ii)', task: 'Explain thermal creep', notation: '4', decoded: 'A single 4-mark granule for the explanation.', marks: 4 },
      { part: '(a)(iii)', task: 'Describe tensile testing', notation: '6', decoded: 'A single 6-mark granule for the description.', marks: 6 },
      { part: '(b)(i)', task: 'Draw the load-extension graph from the tabled data', notation: '10', decoded: 'Ten marks for the plotted graph.', marks: 10 },
      { part: '(b)(ii)', task: 'Indicate features on the graph (elastic limit, start of necking, fracture point)', notation: '2 + 2 + 2', decoded: 'Each of the three marked features earns 2 marks.', marks: 6 },
      { part: '(b)(iii)', task: 'Calculate the ultimate tensile strength', notation: '4', decoded: 'Four marks for the calculation (the model shows formula, substitution and answer with unit: 1.6 kN/mm²).', marks: 4 },
      { part: '(c)(i)', task: 'Macroscopic vs microscopic examination of metals', notation: '8', decoded: 'A single 8-mark granule for the answer.', marks: 8 },
      { part: '(c)(ii)', task: 'Describe radiography (X-ray) NDT', notation: '8', decoded: 'A single 8-mark granule for the description.', marks: 8 },
    ],
    cite: CITE_2025('Q3'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC027ALP000EV.pdf', n: '4',
    totalMarks: 50,
    headline: 'Heat-treatment question: paired 4 + 4 on surface hardening, then an "Any two @ 8 + 8" closing menu.',
    parts: [
      { part: '(a)(i)', task: 'Why surface hardening suits plough points (hard surface, tough core)', notation: '4 + 4', decoded: 'Two elements, 4 marks each.', marks: 8 },
      { part: '(a)(ii)', task: 'Describe induction hardening', notation: '8', decoded: 'A single 8-mark granule for the description.', marks: 8 },
      { part: '(b)(i)', task: 'Identify lines A and B (upper / lower critical temperature) on the iron-carbon diagram', notation: '2 + 2', decoded: 'Each of the two lines earns 2 marks.', marks: 4 },
      { part: '(b)(ii)', task: 'Name and explain point C (the eutectoid point)', notation: '6', decoded: 'A single 6-mark granule for the answer.', marks: 6 },
      { part: '(b)(iii)', task: 'Describe annealing of 1.2% carbon steel', notation: '8', decoded: 'A single 8-mark granule for the description.', marks: 8 },
      { part: '(c)', task: 'Optical pyrometer; quenching media; benefits of forged metal components', notation: 'Any two @ 8 + 8', decoded: 'The best two of the three listed topics count, 8 marks each.', marks: 16 },
    ],
    cite: CITE_2025('Q4'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC027ALP000EV.pdf', n: '5',
    totalMarks: 50,
    headline: 'Crystal-structures question: the equilibrium diagram is 8 marks plus two separately-credited 1-mark labels.',
    parts: [
      { part: '(a)(i)', task: 'Explain allotropy', notation: '4', decoded: 'A single 4-mark granule for the explanation.', marks: 4 },
      { part: '(a)(ii)', task: 'Name crystal structures A, B and C (BCC, FCC, CPH)', notation: '2 + 2 + 2', decoded: 'Each of the three named structures earns 2 marks.', marks: 6 },
      { part: '(a)(iii)', task: 'Describe the BCC and FCC unit cells', notation: '6', decoded: 'A single 6-mark granule for the description.', marks: 6 },
      { part: '(b)(i)', task: 'Draw and label the thermal equilibrium diagram', notation: '8 + 1 + 1', decoded: 'Eight marks for the drawn diagram plus 1 mark each for the two labels (solidus line, liquidus lines).', marks: 10 },
      { part: '(b)(ii)', task: 'Determine the ratio of the phases at 300°C for 60% zinc', notation: '4', decoded: 'Four marks for the calculation (the model reads A, B, C off the diagram and forms |AB|/|BC| = 26/40).', marks: 4 },
      { part: '(b)(iii)', task: 'Name and explain the eutectic point', notation: '4', decoded: 'A single 4-mark granule for the answer.', marks: 4 },
      { part: '(c)', task: 'The metal recycling process; benefits of upcycling metal components; aluminium electrometallurgy', notation: 'Any two @ 8 + 8', decoded: 'The best two of the three listed topics count, 8 marks each.', marks: 16 },
    ],
    cite: CITE_2025('Q5'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC027ALP000EV.pdf', n: '6',
    totalMarks: 50,
    headline: 'Welding question: a 10-mark SAW description, a five-item menu, then an OR fork worth 16 either way.',
    parts: [
      { part: '(a)(i)', task: 'Describe submerged arc welding (SAW)', notation: '10', decoded: 'A single 10-mark granule for the description.', marks: 10 },
      { part: '(a)(ii)', task: 'Why SAW suits welding the rolled-steel wind turbine tower segment', notation: '3 + 3', decoded: 'Two elements, 3 marks each.', marks: 6 },
      { part: '(b)', task: 'Welding items menu: joint preparation; electrode coating functions; acetylene storage; friction welding; distortion', notation: 'Any three @ 6 + 6 + 6', decoded: 'The best three of the five listed items count, 6 marks each.', marks: 18 },
      { part: '(c)', task: 'EITHER compare resistance spot welding and resistance seam welding (electrode shape, procedure, safety, applications) OR (i) benefits of AI visual weld inspection (ii) advantages of VR headsets in welder training', notation: '16 · OR (i) 4 + 4 (ii) 4 + 4', decoded: 'One route only: the spot-vs-seam comparison is a single 16-mark granule; the alternative route splits the same 16 as two 4-mark points in each of (i) and (ii).', marks: 16 },
    ],
    cite: CITE_2025('Q6'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC027ALP000EV.pdf', n: '7',
    totalMarks: 50,
    headline: 'Polymers question: rotational moulding carries 8 marks; the part-(b) menu credits the best three of five at 6 each.',
    parts: [
      { part: '(a)(i)', task: 'Reasons for the hollow design of the plastic road barriers', notation: '2 + 2', decoded: 'Two reasons, 2 marks each.', marks: 4 },
      { part: '(a)(ii)', task: 'Describe rotational moulding', notation: '8', decoded: 'A single 8-mark granule for the description.', marks: 8 },
      { part: '(a)(iii)', task: 'Suitability of HDPE for manufacturing the barriers', notation: '2 + 2', decoded: 'Two elements, 2 marks each.', marks: 4 },
      { part: '(b)', task: 'Polymer items menu: carbon composites in aircraft panels; elastic memory; catalyst vs inhibitor; foaming agents; polyurethane skateboard wheels', notation: 'Any three @ 6 + 6 + 6', decoded: 'The best three of the five listed items count, 6 marks each.', marks: 18 },
      { part: '(c)(i)', task: 'Negative effects of plastic waste on marine life', notation: '8', decoded: 'A single 8-mark granule for the answer.', marks: 8 },
      { part: '(c)(ii)', task: 'Recycling thermoplastics vs thermosetting plastics', notation: '8', decoded: 'A single 8-mark granule for the answer.', marks: 8 },
    ],
    cite: CITE_2025('Q7'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC027ALP000EV.pdf', n: '8',
    totalMarks: 50,
    headline: 'Machining question: a 10-mark grinding description, a five-item menu, then an OR fork worth 16 either way.',
    parts: [
      { part: '(a)(i)', task: 'Describe precision surface grinding', notation: '10', decoded: 'A single 10-mark granule for the description.', marks: 10 },
      { part: '(a)(ii)', task: 'Safety hazards associated with using a grinding machine', notation: '3 + 3', decoded: 'Two hazards, 3 marks each.', marks: 6 },
      { part: '(b)', task: 'Machining items menu: T-slot and dovetail cutters; tungsten carbide insert tips; prolonging tool life; laser measuring in CNC; rancidity of cutting fluid', notation: 'Any three @ 6 + 6 + 6', decoded: 'The best three of the five listed items count, 6 marks each.', marks: 18 },
      { part: '(c)', task: 'EITHER (i) continuous vs discontinuous chips (ii) built-up edge OR (i) stepper motors and feedback sensors in robotic CNC milling (ii) subtractive manufacturing', notation: '(i) 8 (ii) 8 · OR (i) 4 + 4 (ii) 8', decoded: 'One route only, 16 marks either way: the first route pays a single 8 in each sub-part; the alternative pays two 4-mark points then a single 8.', marks: 16 },
    ],
    cite: CITE_2025('Q8'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC027ALP000EV.pdf', n: '9',
    totalMarks: 50,
    headline: 'Mechanisms/electronics question: a 10-mark mechanism design, a five-item menu, then an OR fork worth 16.',
    parts: [
      { part: '(a)(i)', task: 'Suggest mechanisms to tilt and rotate the camera unit (model: servomotor tilt, motor + belt-drive rotation)', notation: '10', decoded: 'Ten marks for a viable suggested solution — the scheme accepts other valid solutions.', marks: 10 },
      { part: '(a)(ii)', task: 'Uses of remote control robots', notation: '6', decoded: 'A single 6-mark granule for the answer.', marks: 6 },
      { part: '(b)', task: 'Mechanisms/electronics menu: bevel gears; thermostatic heating control; ratchet and pawl; single-acting cylinder; capacitor', notation: 'Any three @ 6 + 6 + 6', decoded: 'The best three of the five listed items count, 6 marks each.', marks: 18 },
      { part: '(c)', task: 'EITHER (i) mechanism to raise/lower the 3D printing head (model: leadscrew) (ii) function of the limit switch OR (i) benefits of the solar carport (ii) how solar energy charges an electric vehicle', notation: '(i) 8 (ii) 8 · OR (i) 4 + 4 (ii) 8', decoded: 'One route only, 16 marks either way: the first route pays a single 8 in each sub-part; the alternative pays two 4-mark points then a single 8.', marks: 16 },
    ],
    cite: CITE_2025('Q9'),
  },
];

const ENGINEERING_LENS: SubjectLens = {
  subjectId: 'engineering',
  entries: [
    ...HL_2024_EV,
    ...mirrorIV(HL_2024_EV, 'LC027ALP000IV.pdf'),
    ...HL_2025_EV,
    ...mirrorIV(HL_2025_EV, 'LC027ALP000IV.pdf'),
  ],
};

export default ENGINEERING_LENS;
