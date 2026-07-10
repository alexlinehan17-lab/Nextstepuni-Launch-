/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Marking Lens — Physics (Higher Level, 2023 & 2025).
 *
 * Sources of truth:
 *  - examiner-reports/physics/2023-marking-scheme.md
 *    (SEC Marking Scheme 2023, Physics Higher Level)
 *  - examiner-reports/physics/2025-marking-scheme.md
 *    (SEC Marking Scheme 2025, Physics Higher Level)
 *
 * Every notation below is verbatim from the filed scheme (normalised spacing
 * only); each entry's parts sum exactly to the question total, which is the
 * sum of the scheme's printed granules (40 marks for the Section A experiment
 * questions Q1–5; 56 marks for the Section B questions) — machine-checked in
 * test/markingLens.test.ts. Pitfalls quote the scheme's own general marking
 * instructions (p.3 of each scheme; identical wording across both years —
 * see examiner-reports/physics/2023-verification.md and 2025-insights.md).
 *
 * Deliberately OMITTED (no honest single ladder sums to the printed total):
 *  - Q6 both years ("Answer any eight of the following parts" — 8 × 7m of 12
 *    lettered options; every option's granules sum to 7).
 *  - Q12 both years (internal choice: answer (a) OR (b); each branch's
 *    granules sum to 56 independently).
 *  - Q14 both years ("Answer any two of the following parts (a)–(d)";
 *    each part's granules sum to 28).
 *  - Ordinary Level (tagged in the Topic Vault, but no OL scheme is filed).
 *
 * Keys (year/level/lang/fileid/n) match the Topic Vault tags exactly; the IV
 * papers are the same exams marked by the same schemes, so EV entries are
 * mirrored (as in business.ts).
 */

import { type QuestionLens, type SubjectLens } from './types';

const CITE_23 = (q: string) => `SEC Marking Scheme 2023, Physics Higher Level, ${q}`;
const CITE_25 = (q: string) => `SEC Marking Scheme 2025, Physics Higher Level, ${q}`;

// The IV paper is the same exam marked by the same scheme — mirror EV entries.
const mirrorIV = (entries: QuestionLens[]): QuestionLens[] =>
  entries.map(e => ({ ...e, lang: 'iv', fileid: 'LC021ALP000IV.pdf' }));

// ── 2023 Higher Level (English version) ──────────────────────────────────────

const HL_2023_EV: QuestionLens[] = [
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: 'LC021ALP000EV.pdf', n: '1',
    totalMarks: 40,
    headline: 'A 40-mark experiment question (g by free fall): mostly 3-mark granules for apparatus, procedure and graph; the closing "why" carries two 2-mark elements.',
    parts: [
      { part: '(i)', task: 'Draw a labelled diagram of the apparatus', notation: 'any three correct items merit 3 × 3 [–1 if no label present on diagram]', decoded: 'Any three of: object, release mechanism, pressure plate/trapdoor, means of measuring distance/time — 3 marks each; one mark deducted if the diagram has no label.', marks: 9 },
      { part: '(ii)', task: 'Indicate the distance s on the diagram', notation: '[3]', decoded: 'One 3-mark element: s shown from (the bottom of) the object to the plate.', marks: 3 },
      { part: '(iii)', task: 'Describe how the time interval t was measured', notation: '[3] + [3]', decoded: 'Two 3-mark elements: (electronic) timer; started when the object is released and stopped when it hits the plate.', marks: 6 },
      { part: '(iv)', task: 'Draw a suitable graph to show the relationship between s and t', notation: '[3] + [3] + [3] + [3]', decoded: 'Four 3-mark elements: t² values, labelled axes, 6 points plotted, straight line with good fit.', marks: 12 },
      { part: '(v)', task: 'Use the graph to calculate a value for g', notation: '[3] + [3]', decoded: 'Slope formula / s = ut + ½at² (3m); g ≈ 9.8 m s⁻² from calculation (3m).', marks: 6 },
      { part: '(vi)', task: 'Explain why the object used was a smooth metal sphere', notation: '[2] + [2]', decoded: 'Two 2-mark elements: to reduce air resistance; high density / magnetic / conductor.', marks: 4 },
    ],
    pitfall: {
      text: 'The scheme applies a fixed graph deduction: "When drawing graphs, one mark is deducted for use of an inappropriate scale."',
      cite: 'SEC Marking Scheme 2023 (Physics HL), general instruction 7, p.3',
    },
    cite: CITE_23('Q1'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: 'LC021ALP000EV.pdf', n: '2',
    totalMarks: 40,
    headline: 'A 40-mark experiment question (focal length of a concave mirror); the calculation with all the data is a ladder of 2-mark granules.',
    parts: [
      { part: '(i)', task: 'How did the student find an approximate value for f?', notation: '[6] + [3]', decoded: 'Focus the image of a distant object on a screen (6m); measure the distance from the screen to the mirror (3m).', marks: 9 },
      { part: '(ii)', task: 'Why did the student find an approximate value for f?', notation: '[3]', decoded: 'One 3-mark element: object must be outside the focal point / to get an image on the screen / to check the answer.', marks: 3 },
      { part: '(iii)', task: 'Draw a labelled diagram of the apparatus, showing u and v', notation: '[3] + [3] + [3]', decoded: 'Object, screen, mirror (3m); u shown (3m); v shown (3m).', marks: 9 },
      { part: '(iv)', task: 'Describe how the student determined and measured v', notation: '[3] + [3] + [3]', decoded: 'Move object/screen/mirror (3m); until a (sharp) image is formed on the screen (3m); measure v with a metre stick (3m).', marks: 9 },
      { part: '(v)', task: 'Use all of the data to calculate f', notation: '[2] + [2] + [2] + [2 × 1] + [2]', decoded: '1/u + 1/v = 1/f (2m); substitution for u and v, once (2m); first calculation of f (2m); two further calculations of f (1m each); average of values, f = 15.4 cm (2m).', marks: 10 },
    ],
    cite: CITE_23('Q2'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: 'LC021ALP000EV.pdf', n: '3',
    totalMarks: 40,
    headline: 'A 40-mark experiment question (wavelength by diffraction grating): 3-mark granules through the wavelength ladder, then 4/4/2 for the three pattern changes.',
    parts: [
      { part: '(i)', task: 'Draw a labelled diagram of the apparatus arrangement', notation: '[3] + [3] + [3] + [3] [–1 if no label present on diagram]', decoded: 'Source of light, screen/spectrometer, diffraction grating, arrangement — 3 marks each; one mark deducted if the diagram has no label.', marks: 12 },
      { part: '(ii)', task: 'How were the third order images identified?', notation: '[3]', decoded: 'One 3-mark element: third image on both sides of the central image.', marks: 3 },
      { part: '(iii)', task: 'Calculate the grating constant d', notation: '[3]', decoded: 'One 3-mark element: 1/300000 ≈ 3.33 × 10⁻⁶ m.', marks: 3 },
      { part: '(iv)', task: 'Calculate the wavelength of the red light', notation: '[3] + [3] + [3] + [3]', decoded: 'nλ = d sinθ (3m); 1.04/2 = 0.52 (m) (3m); θ = 34.74° (3m); λ = 6.33 × 10⁻⁷ m (3m).', marks: 12 },
      { part: '(v)', task: 'Describe how the pattern changes for (a) fewer lines per mm, (b) green light, (c) screen moved further away', notation: '[4] + [4] + [2]', decoded: '(a) images are closer together (4m); (b) images are closer together (4m); (c) images are further apart (2m).', marks: 10 },
    ],
    cite: CITE_23('Q3'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: 'LC021ALP000EV.pdf', n: '4',
    totalMarks: 40,
    headline: 'A 40-mark experiment question (latent heat of vaporisation): four how/why elements at 3 marks each, then a 16-mark calculation with its data values at 1 mark apiece.',
    parts: [
      { part: '(i)', task: 'Draw a labelled diagram of the apparatus arrangement', notation: '[3] + [3] + [3] + [3] [–1 if no label present on diagram]', decoded: 'Steam generator and delivery tube, calorimeter with water, thermometer, arrangement — 3 marks each; one mark deducted if the diagram has no label.', marks: 12 },
      { part: '(ii)', task: 'How did the student cool the water?', notation: '[3]', decoded: 'One 3-mark element: refrigeration / ice bucket / adding ice which was allowed to melt completely / etc.', marks: 3 },
      { part: '(iii)', task: 'How did the student dry the steam?', notation: '[3]', decoded: 'One 3-mark element: steam trap / delivery tube sloped upwards / insulated delivery tube.', marks: 3 },
      { part: '(iv)', task: 'Why did the student cool the water?', notation: '[3]', decoded: 'One 3-mark element: so energy lost to the surroundings cancelled energy gained / so the steam condensed more quickly.', marks: 3 },
      { part: '(v)', task: 'Why did the student dry the steam?', notation: '[3]', decoded: 'One 3-mark element: so the steam had not lost its latent heat before being added / so no water is added.', marks: 3 },
      { part: '(vi)', task: 'Use the data to calculate the specific latent heat of vaporisation of water', notation: '[6 + 3] + [4 × 1] + [3]', decoded: 'mcΔθ; ml (6 + 3); the four data values mw, ms, Δθw, Δθs (1 mark each); l = 2.22 × 10⁶ J kg⁻¹ (3m).', marks: 16 },
    ],
    cite: CITE_23('Q4'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: 'LC021ALP000EV.pdf', n: '5',
    totalMarks: 40,
    headline: 'A 40-mark experiment question (diode I–V): 3-mark granules for both circuits and the forward-bias graph; the reverse-bias sketch ends on a 4-mark shape granule.',
    parts: [
      { part: '(i)', task: 'Draw a circuit diagram with the diode in forward bias', notation: '[3] + [3] + [3] + [3]', decoded: 'Source of voltage; diode in forward bias; voltmeter across the diode; (milli)ammeter in series — 3 marks each.', marks: 12 },
      { part: '(ii)', task: 'Draw a suitable graph of I against V for a diode in forward bias', notation: '[3] + [3] + [3]', decoded: 'Labelled axes; 6 points plotted; curve with good fit — 3 marks each.', marks: 9 },
      { part: '(iii)', task: 'Is Ohm’s law obeyed for this diode? Justify your answer', notation: '[3] + [3]', decoded: 'No (3m); not a straight line (3m).', marks: 6 },
      { part: '(iv)', task: 'Draw a circuit diagram with the diode in reverse bias', notation: '[3] + [3]', decoded: 'Diode in reverse bias (3m); voltmeter across the diode and (micro)ammeter (3m).', marks: 6 },
      { part: '(v)', task: 'Sketch a graph of I against V for a diode in reverse bias', notation: '[3] + [4]', decoded: 'Axes labelled (3m); correct shape (4m).', marks: 7 },
    ],
    cite: CITE_23('Q5'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: 'LC021ALP000EV.pdf', n: '7',
    totalMarks: 56,
    headline: 'A 56-mark mechanics question (Newton’s laws, golf ball projectile): statements and derivation in 3-mark granules; the later calculations step down to 2-mark granules.',
    parts: [
      { part: '(i)', task: 'State Newton’s third law of motion', notation: '[3] + [3]', decoded: 'When object A applies a force on object B // every action (3m); object B applies an equal but opposite force on object A // equal but opposite reaction (3m).', marks: 6 },
      { part: '(ii)', task: 'Show that F = ma is a special case of Newton’s second law', notation: '[3] + [3] + [3] + [3]', decoded: 'F ∝ (mv − mu)/t; F = k(mv − mu)/t; F = kma; k = 1 from the definition of the newton — 3 marks each.', marks: 12 },
      { part: '(iii)', task: 'Calculate the velocity of the ball immediately after impact', notation: '[3] + [3]', decoded: 'F = (mv − mu)/t (3m); v = 76.05 m s⁻¹ (3m).', marks: 6 },
      { part: '(iv)(a)', task: 'Draw the forces acting on the ball during impact', notation: '[3] + [3]', decoded: 'Weight down (3m); force applied by club (3m).', marks: 6 },
      { part: '(iv)(b)', task: 'Draw the forces acting on the ball immediately after impact', notation: '[3]', decoded: 'One 3-mark element: weight down.', marks: 3 },
      { part: '(v)', task: 'Calculate the maximum height reached by the ball', notation: '[3] + [3] + [3]', decoded: 'uy = 76.05 sin 15° (3m); v² = u² + 2as (3m); s = 19.77 m (3m).', marks: 9 },
      { part: '(vi)', task: 'Calculate the time to travel a horizontal distance of 280 m', notation: '[2] + [2] + [2]', decoded: 'vx = 76.05 cos 15° (2m); v = s/t (2m); t = 3.81 s (2m).', marks: 6 },
      { part: '(vii)', task: 'Calculate the magnitude and direction of the wind velocity', notation: '[2] + [2] + [2] + [2]', decoded: 'a² = b² + c² (2m); v = 9.0 m s⁻¹ (2m); tan θ = opposite/adjacent (2m); θ = 24.3° (N of E) (2m).', marks: 8 },
    ],
    pitfall: {
      text: 'The scheme’s fixed unit rule applies to every final answer here: "For omission of appropriate units (or for incorrect units) in final answers, one mark is deducted, unless otherwise indicated."',
      cite: 'SEC Marking Scheme 2023 (Physics HL), general instruction 6, p.3',
    },
    cite: CITE_23('Q7'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: 'LC021ALP000EV.pdf', n: '8',
    totalMarks: 56,
    headline: 'A 56-mark waves question (resonance, stretched string): each sketch graph and each “factor of four” effect is a 2 + 2 pair.',
    parts: [
      { part: '(i)', task: 'What is resonance?', notation: '[3] + [3]', decoded: 'The transfer of energy (3m); between two systems with the same (natural) frequency (3m).', marks: 6 },
      { part: '(ii)', task: 'Describe a laboratory experiment to demonstrate resonance', notation: '[3] + [3] + [3]', decoded: 'Apparatus (3m); method (3m); observation (3m).', marks: 9 },
      { part: '(iii)(a)', task: 'Sketch a graph of the relationship between f and T', notation: '[2] + [2]', decoded: 'Labelled axis f and √T (2m); straight line through the origin (2m).', marks: 4 },
      { part: '(iii)(b)', task: 'Sketch a graph of the relationship between f and l', notation: '[2] + [2]', decoded: 'Labelled axis f and 1/l (2m); straight line through the origin (2m).', marks: 4 },
      { part: '(iii)(c)', task: 'Sketch a graph of the relationship between f and µ', notation: '[2] + [2]', decoded: 'Labelled axis f and 1/√µ (2m); straight line through the origin (2m).', marks: 4 },
      { part: '(iv)(a)', task: 'Effect on f if T is increased by a factor of four', notation: '[2] + [2]', decoded: 'Increases (2m); by a factor of 2 (2m).', marks: 4 },
      { part: '(iv)(b)', task: 'Effect on f if l is increased by a factor of four', notation: '[2] + [2]', decoded: 'Decreases (2m); by a factor of 4 (2m).', marks: 4 },
      { part: '(iv)(c)', task: 'Effect on f if µ is increased by a factor of four', notation: '[2] + [2]', decoded: 'Decreases (2m); by a factor of 2 (2m).', marks: 4 },
      { part: '(v)', task: 'What are harmonics?', notation: '[3] + [2]', decoded: 'Frequencies (3m); which are multiples of the fundamental (2m).', marks: 5 },
      { part: '(vi)', task: 'Draw the string vibrating at its third harmonic', notation: '[3] + [3]', decoded: 'Node at both ends (3m); two additional nodes in correct arrangement (3m).', marks: 6 },
      { part: '(vii)', task: 'Calculate the frequency at the third harmonic', notation: '[2] + [2] + [2]', decoded: 'λ = 0.62/1.5 = 0.4133 m (2m); c = fλ (2m); f = 919.4 Hz (2m).', marks: 6 },
    ],
    cite: CITE_23('Q8'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: 'LC021ALP000EV.pdf', n: '9',
    totalMarks: 56,
    headline: 'A 56-mark nuclear question (Voyager, plutonium-238): the decay equation is eight 1-mark pieces with a stated −3 penalty; the calculations are 3-mark ladders.',
    parts: [
      { part: '(i)', task: 'Write a nuclear equation for the alpha decay of plutonium-238', notation: '[8 × 1] [–3 for each additional incorrect species]', decoded: 'Eight 1-mark elements of the equation ²³⁸₉₄Pu → ²³⁴₉₂U + ⁴₂He; 3 marks deducted for each additional incorrect species.', marks: 8 },
      { part: '(ii)', task: 'Calculate the energy released during each decay, in MeV', notation: '[3] + [3] + [3] + [3] + [3]', decoded: 'Conversion from u to kg; mass defect (= 9.95757 × 10⁻³⁰ kg); E = mc²; E = 8.95 × 10⁻¹³ J; E = 5.6 MeV — 3 marks each.', marks: 15 },
      { part: '(iii)', task: 'State the thermometric property of a thermocouple', notation: '[3]', decoded: 'One 3-mark element: emf / voltage.', marks: 3 },
      { part: '(iv)', task: 'Draw a labelled diagram of the arrangement of a thermocouple', notation: '[3] + [3] + [3] [–1 if no label present on diagram]', decoded: 'Two different metals; first junction at one temperature; second junction at a different temperature — 3 marks each; one mark deducted if no label.', marks: 9 },
      { part: '(v)', task: 'Calculate the rate of decay of the plutonium in each generator in 1977', notation: '[3] + [3] + [3] + [3] + [2]', decoded: 'λ = ln 2/T½ (3m); A = λN (3m); T½ in seconds = 2.77 × 10⁹ s (3m); N = 1.012 × 10²⁵ atoms (3m); A = 2.53 × 10¹⁵ Bq (2m).', marks: 14 },
      { part: '(vi)', task: 'Calculate the year when only 1 kg of the plutonium will remain', notation: '[2] + [2]', decoded: 'Reference to two half-lives (2m); 1977 + 2 × 87.8 = 2152 (2m).', marks: 4 },
      { part: '(vii)', task: 'Use one of Newton’s laws to explain the constant velocities', notation: '[3]', decoded: 'One 3-mark element: no force acting on it.', marks: 3 },
    ],
    pitfall: {
      text: 'On multi-step calculations like these, the scheme’s fixed rule is per slip, not per answer: "Each time an arithmetical slip occurs in a calculation, one mark is deducted."',
      cite: 'SEC Marking Scheme 2023 (Physics HL), general instruction 8, p.3',
    },
    cite: CITE_23('Q9'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: 'LC021ALP000EV.pdf', n: '10',
    totalMarks: 56,
    headline: 'A 56-mark electrostatics question (Van de Graaff, X-ray tube): 3-mark granules throughout, with the X-ray tube diagram marked as four 2-mark features.',
    parts: [
      { part: '(i)', task: 'Describe how point discharge occurs', notation: '[3] + [3] + [3]', decoded: 'Accumulation of charge at a point; large electric field generated / ionisation of the air; unlike charges attract and like charges repel — 3 marks each.', marks: 9 },
      { part: '(ii)', task: 'Describe a laboratory experiment to demonstrate point discharge', notation: '[3] + [3] + [3]', decoded: 'Apparatus (3m); method (3m); observation (3m).', marks: 9 },
      { part: '(iii)', task: 'Draw the electric field around the dome', notation: '[3] + [3]', decoded: 'Radial field lines (3m); away from the dome (3m).', marks: 6 },
      { part: '(iv)', task: 'Calculate the electric field strength at the surface of the dome', notation: '[3] + [3] + [3]', decoded: 'F = q₁q₂/4πεd² (3m); r = 16 cm (3m); E = 7.0 × 10⁴ N C⁻¹ (3m).', marks: 9 },
      { part: '(v)', task: 'Calculate the force on an electron at the surface of the dome', notation: '[3] + [3]', decoded: 'E = F/q (3m); F = 1.12 × 10⁻¹⁴ N towards the centre of the dome (3m).', marks: 6 },
      { part: '(vi)', task: 'Calculate the maximum speed of the electrons produced in the tube', notation: '[3] + [3] + [3]', decoded: 'qV / ½mv² (3m); qV = ½mv² (3m); v = 1.57 × 10⁸ m s⁻¹ (3m).', marks: 9 },
      { part: '(vii)', task: 'Draw a labelled diagram of an X-ray tube', notation: '[2] + [2] + [2] + [2]', decoded: 'Low voltage filament / heating coil; cathode & anode/target; (high) voltage between cathode & anode; cooling / shielding / window / (partial) vacuum — 2 marks each.', marks: 8 },
    ],
    cite: CITE_23('Q10'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: 'LC021ALP000EV.pdf', n: '11',
    totalMarks: 56,
    headline: 'A 56-mark electromagnetic induction question (metal detectors): law statements are 3 + 3 pairs and the coil calculations are 3-mark ladders.',
    parts: [
      { part: '(i)', task: 'Explain in detail how a current is induced in the detected metal', notation: '[3] + [3] + [3] + [3]', decoded: 'Changing magnetic field; cutting the metal; emf induced; current flows — 3 marks each.', marks: 12 },
      { part: '(ii)', task: 'State Faraday’s law of electromagnetic induction', notation: '[3] + [3]', decoded: '(Size of) emf induced is proportional to // formula (3m); the rate of change of magnetic flux // notation (3m).', marks: 6 },
      { part: '(iii)', task: 'State Lenz’s law of electromagnetic induction', notation: '[3] + [3]', decoded: 'Direction of an induced current/emf (3m); is such as to oppose the change causing it (3m).', marks: 6 },
      { part: '(iv)', task: 'Describe a laboratory experiment to demonstrate either law', notation: '[3] + [3] + [3]', decoded: 'Apparatus (3m); method (3m); observation (3m).', marks: 9 },
      { part: '(v)', task: 'Calculate the time taken for the coil to fully enter the field', notation: '[3] + [3]', decoded: 'v = s/t (3m); t = 0.015 s (3m).', marks: 6 },
      { part: '(vi)', task: 'Calculate the average emf induced as the coil enters the field', notation: '[3] + [3] + [3] + [3]', decoded: 'A = πr² (3m); Ø = BA (3m); E = (−)ΔØ/Δt (3m); E = 1.70 V (3m).', marks: 12 },
      { part: '(vii)', task: 'Calculate the average current in the coil as it enters the field', notation: '[3] + [2]', decoded: 'V = IR (3m); I = 0.74 A (2m).', marks: 5 },
    ],
    pitfall: {
      text: 'The law statements here are marked with the double solidus: "Answers that are separated by a double solidus, //, are answers which are mutually exclusive. A partial answer from one side of the // may not be taken in conjunction with a partial answer from the other side."',
      cite: 'SEC Marking Scheme 2023 (Physics HL), general instruction 3, p.3',
    },
    cite: CITE_23('Q11'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: 'LC021ALP000EV.pdf', n: '13',
    totalMarks: 56,
    headline: 'A 56-mark comprehension question (energy storage passage): each calculation is a short formula + answer pair, and two parts carry a 4 + 3 split.',
    parts: [
      { part: '(i)(a)', task: 'Calculate the mass of water in the upper reservoir', notation: '[3] + [3]', decoded: 'ρ = m/V (3m); m = 2.29 × 10⁹ kg (3m).', marks: 6 },
      { part: '(i)(b)', task: 'Calculate the potential energy stored in the reservoir', notation: '[2] + [2]', decoded: 'E = mgh (2m); E = 7.21 × 10¹² J (2m).', marks: 4 },
      { part: '(i)(c)', task: 'Calculate the maximum power if emptied in 24 hours', notation: '[2] + [2]', decoded: 'P = E/t (2m); P = 8.35 × 10⁷ W (2m).', marks: 4 },
      { part: '(ii)', task: 'State the main energy conversion at position A and at position B', notation: '[4 + 3]', decoded: '(a) gravitational/potential to kinetic and (b) kinetic to electrical, split 4 + 3.', marks: 7 },
      { part: '(iii)', task: 'Describe an experiment demonstrating the force on a current-carrying conductor in a magnetic field', notation: '[3] + [2] + [2]', decoded: 'Apparatus (3m); method (2m); observation (2m).', marks: 7 },
      { part: '(iv)(a)', task: 'Calculate the period of the flywheel’s motion', notation: '[3] + [3]', decoded: 'T = 1/f (3m); T = 0.012 s (3m).', marks: 6 },
      { part: '(iv)(b)', task: 'Calculate the angular velocity of the flywheel', notation: '[2] + [2]', decoded: 'T = 2π/ω (2m); ω = 523.6 radians s⁻¹ (2m).', marks: 4 },
      { part: '(iv)(c)', task: 'Calculate the centripetal acceleration at the circumference', notation: '[2] + [2]', decoded: 'a = rω² (2m); a = 1.9 × 10⁵ m s⁻² towards the centre (2m).', marks: 4 },
      { part: '(v)', task: 'Name two other sources of emf', notation: '[4 + 3]', decoded: 'Two sources (e.g. mains, solar cell, thermocouple), split 4 + 3.', marks: 7 },
      { part: '(vi)', task: 'Explain why energy storage matters more with renewable generation', notation: '[7]', decoded: 'One 7-mark element: renewable sources are more likely to vary in the rate at which they produce electricity.', marks: 7 },
    ],
    cite: CITE_23('Q13'),
  },
];

// ── 2025 Higher Level (English version) ──────────────────────────────────────

const HL_2025_EV: QuestionLens[] = [
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC021ALP000EV.pdf', n: '1',
    totalMarks: 40,
    headline: 'A 40-mark experiment question (laws of equilibrium): the force diagram is six 1-mark arrows, and the moments calculation explicitly banks “any one moment” before the sums.',
    parts: [
      { part: '(i)', task: 'Describe how the student found the centre of gravity of the metre stick', notation: '[3]', decoded: 'One 3-mark element: balance on a pivot.', marks: 3 },
      { part: '(ii)', task: 'How did the student know the metre stick was in equilibrium?', notation: '[3]', decoded: 'One 3-mark element: not accelerating.', marks: 3 },
      { part: '(iii)', task: 'Draw a labelled diagram of all the forces acting on the metre stick', notation: '[6 x 1]', decoded: 'Six 1-mark elements: two forces up and four forces down, with the weight arrow labelled.', marks: 6 },
      { part: '(iv)', task: 'Why was it important that the forces were applied vertically?', notation: '[3]', decoded: 'One 3-mark element: (distance to each force position is) a perpendicular distance.', marks: 3 },
      { part: '(v)', task: 'Calculate the net force acting on the metre stick', notation: '[3] + [3] + [3]', decoded: 'Forces up = 8.9 N (3m); forces down = 8.96 N (3m); net force (= 0.06 N) ≈ 0 (3m).', marks: 9 },
      { part: '(vi)', task: 'Calculate the sums of the clockwise and anticlockwise moments about the 5 cm mark', notation: '[3] + [3] + [3] + [3]', decoded: 'M = Fd (3m); any one moment calculated (3m); clockwise moments calculated (3m); anticlockwise moments calculated (3m).', marks: 12 },
      { part: '(vii)', task: 'Use the results to verify the laws of equilibrium', notation: '[2 + 2]', decoded: 'Total force up ≈ total force down (2m); total clockwise moment ≈ total anticlockwise moment (2m).', marks: 4 },
    ],
    cite: CITE_25('Q1'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC021ALP000EV.pdf', n: '2',
    totalMarks: 40,
    headline: 'A 40-mark experiment question (conservation of momentum): 3-mark granules, with the velocity pair at 2 + 1 and the error-minimising description at 2 + 2.',
    parts: [
      { part: '(i)', task: 'Explain how the masses could have been measured', notation: '[3]', decoded: 'One 3-mark element: (electronic) balance.', marks: 3 },
      { part: '(ii)', task: 'Describe how the constant velocity of a trolley can be determined', notation: '[3] + [3] + [3]', decoded: '(Measure) length l of card // distance between dots (3m); (measure) time for l // time between dots (3m); v = l/t (3m).', marks: 9 },
      { part: '(iii)', task: 'Calculate the velocity of trolley A and of trolley B after release', notation: '[2 + 1]', decoded: 'vA = 0.54 m s⁻¹ and vB = 0.42 m s⁻¹, split 2 + 1.', marks: 3 },
      { part: '(iv)', task: 'What is the total momentum of the trolleys before release?', notation: '[3]', decoded: 'One 3-mark element: zero.', marks: 3 },
      { part: '(v)', task: 'Show that the experiment verifies conservation of momentum', notation: '[3] + [3] + [3]', decoded: 'p = mv (3m); pA = 0.108 / pB = 0.105 kg m s⁻¹ (3m); p_total (= 0.003 kg m s⁻¹) ≈ 0 (3m).', marks: 9 },
      { part: '(vi)(a)', task: 'State two principal external forces that should be minimised', notation: '[3 + 3]', decoded: 'Frictional and gravitational forces, 3 marks each.', marks: 6 },
      { part: '(vi)(b)', task: 'Describe how the effect of these forces could be minimised', notation: '[2] + [2] [allow 4 marks for adjust the track until frictional force = gravitational force]', decoded: 'Cushion of air / clean air track // oil wheels / clean track (2m); horizontal air track // slope track (2m); the stated alternative earns the full 4.', marks: 4 },
      { part: '(vii)', task: 'State one other way to improve the accuracy of the experiment', notation: '[3]', decoded: 'One 3-mark element: e.g. repeat the experiment / reduce the error of parallax / more accurate balance/timer.', marks: 3 },
    ],
    cite: CITE_25('Q2'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC021ALP000EV.pdf', n: '3',
    totalMarks: 40,
    headline: 'A 40-mark experiment question (speed of sound in air): unusually, the apparatus diagram carries 4-mark granules; the graph calculation is a four-step 3-mark ladder.',
    parts: [
      { part: '(i)', task: 'Draw a labelled diagram of the arrangement of the apparatus', notation: '[4] + [4] + [4] [–1 if no label present on diagram]', decoded: 'Tube; means of varying length l; tuning fork / metre stick — 4 marks each; one mark deducted if the diagram has no label.', marks: 12 },
      { part: '(ii)', task: 'Describe how the first position of resonance was found', notation: '[3] + [3]', decoded: 'Increase length of the pipe (from l = 0 cm) (3m); until a (loud) sound is heard (3m).', marks: 6 },
      { part: '(iii)', task: 'Describe how the frequency values were determined', notation: '[3]', decoded: 'One 3-mark element: (read) the tuning fork(s).', marks: 3 },
      { part: '(iv)', task: 'Use the graph to calculate the speed of sound in air', notation: '[3] + [3] + [3] + [3]', decoded: 'Slope formula (3m); calculate slope (3m); v = 4 × slope or c = fλ (3m); v ≈ 343.7 m s⁻¹ (3m).', marks: 12 },
      { part: '(v)', task: 'Why does the graph not go through the origin?', notation: '[3]', decoded: 'One 3-mark element: end correction / antinode forms outside the opening of the pipe.', marks: 3 },
      { part: '(vi)', task: 'Identify the frequency of the tuning fork with the lowest frequency', notation: '[4]', decoded: 'One 4-mark element: f = 200 Hz.', marks: 4 },
    ],
    cite: CITE_25('Q3'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC021ALP000EV.pdf', n: '4',
    totalMarks: 40,
    headline: 'A 40-mark experiment question (Snell’s law): ray diagram and graph each carry four 3-mark granules — the sine values are a marked granule of the graph itself.',
    parts: [
      { part: '(i)', task: 'Show the path of the ray through the glass block, indicating r', notation: '[3] + [3] + [3] + [3]', decoded: 'Normal drawn at point of entry; ray refracted (towards normal); emergent ray; angle r indicated — 3 marks each.', marks: 12 },
      { part: '(ii)', task: 'Draw a suitable graph to show the relationship between i and r', notation: '[3] + [3] + [3] + [3]', decoded: 'Values of sin i and sin r; axes labelled; points plotted; line of best fit — 3 marks each.', marks: 12 },
      { part: '(iii)', task: 'Explain how the graph verifies Snell’s law', notation: '[3]', decoded: 'One 3-mark element: straight line through origin / sin i ∝ sin r.', marks: 3 },
      { part: '(iv)', task: 'Use the graph to calculate the refractive index of the glass', notation: '[3] + [3]', decoded: 'Slope formula (3m); n = 1.5 (3m).', marks: 6 },
      { part: '(v)', task: 'Explain why the block was placed flat and not on a narrow face', notation: '[3]', decoded: 'One 3-mark element: reduce (percentage) error (in r).', marks: 3 },
      { part: '(vi)', task: 'Describe what would be observed if the incident ray was perpendicular to the block', notation: '[4]', decoded: 'One 4-mark element: ray would pass straight through.', marks: 4 },
    ],
    pitfall: {
      text: 'The scheme applies a fixed graph deduction: "When drawing graphs, one mark is deducted for use of an inappropriate scale."',
      cite: 'SEC Marking Scheme 2025 (Physics HL), general instruction 7, p.3',
    },
    cite: CITE_25('Q4'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC021ALP000EV.pdf', n: '5',
    totalMarks: 40,
    headline: 'A 40-mark experiment question (filament bulb I–V): one 3-mark formula granule serves both resistance calculations, and the final explanation is a 4 + 4 pair.',
    parts: [
      { part: '(i)', task: 'Draw a circuit diagram for this experiment', notation: '[3] + [3] + [3] + [3]', decoded: 'Power supply; voltmeter in parallel with the bulb; ammeter in series with the bulb; means of changing voltage — 3 marks each.', marks: 12 },
      { part: '(ii)', task: 'Draw a suitable graph to show the relationship between V and I', notation: '[3] + [3] + [3]', decoded: 'Axes labelled; points plotted; curve of best fit drawn — 3 marks each.', marks: 9 },
      { part: '(iii)', task: 'Does the graph show Ohm’s law is obeyed? Justify your answer', notation: '[2] + [2]', decoded: 'No (2m); not a straight line (2m).', marks: 4 },
      { part: '(iv)', task: 'Calculate the resistance of the bulb at 40 mA and at 90 mA', notation: '[3] + [2] + [2]', decoded: 'R = V/I (3m); (a) R ≈ 43 Ω (2m); (b) R ≈ 54 Ω (2m).', marks: 7 },
      { part: '(v)', task: 'Explain what happens to the resistance of the bulb as the current increases', notation: '[4 + 4]', decoded: '(Increase in current causes) increase in temperature (4m); (increase in temperature causes) increase in resistance (4m).', marks: 8 },
    ],
    cite: CITE_25('Q5'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC021ALP000EV.pdf', n: '7',
    totalMarks: 56,
    headline: 'A 56-mark circular motion and gravitation question: definitions and calculations in 3-mark granules; the equator calculations step down to 2-mark granules.',
    parts: [
      { part: '(i)(a)', task: 'Explain what is meant by weight', notation: '[3]', decoded: 'One 3-mark element: gravitational force acting on a mass // W = mg & notation.', marks: 3 },
      { part: '(i)(b)', task: 'Explain what is meant by centripetal force', notation: '[3] + [3]', decoded: 'Force towards centre of circle (3m); (that keeps) object moving in a circle (3m); the scheme allows 3 marks for F = mv²/r.', marks: 6 },
      { part: '(ii)', task: 'State Newton’s law of universal gravitation', notation: '[3] + [3]', decoded: 'Force proportional to the product of two masses // F ∝ m₁m₂/d² (3m); inversely proportional to square of distance // notation (3m).', marks: 6 },
      { part: '(iii)', task: 'Derive an equation for angular velocity in terms of linear velocity', notation: '[2] + [2] + [2]', decoded: 'θ = s/r or v = s/t or ω = θ/t (2m); combination of two formulae (2m); ω = v/r (2m).', marks: 6 },
      { part: '(iv)(a)', task: 'Calculate the angular velocity of the Moon', notation: '[3] + [3]', decoded: 'θ = 2π (3m); ω = 2.664 × 10⁻⁶ rad s⁻¹ (3m).', marks: 6 },
      { part: '(iv)(b)', task: 'Calculate the linear velocity of the Moon', notation: '[3] + [3]', decoded: 'v = rω (3m); v = 1023 m s⁻¹ (3m).', marks: 6 },
      { part: '(v)', task: 'Calculate the force of gravity the Earth exerts on the Moon', notation: '[3] + [3]', decoded: 'F = Gm₁m₂/d² (3m); force = 1.986 × 10²⁰ N towards the centre of the Earth (3m).', marks: 6 },
      { part: '(vi)', task: 'Why does the Moon not fall down to Earth?', notation: '[5]', decoded: 'One 5-mark element: (tangential) velocity // gravitational force is too weak.', marks: 5 },
      { part: '(vii)', task: 'Calculate the centripetal force on the person at the equator (scheme solution: F = mv²/r)', notation: '[2] + [2]', decoded: 'F_centripetal = mv²/r (2m); F_centripetal = 2.68 N (2m).', marks: 4 },
      { part: '(viii)', task: 'Calculate the normal force on the person (scheme solution: W − F_centripetal)', notation: '[2] + [2]', decoded: 'W = mg (2m); F_normal = (W − F_centripetal) = 781.32 N (2m).', marks: 4 },
      { part: '(ix)', task: 'Forces on the person (scheme credits weight and normal/reaction force)', notation: '[2 + 2] [–1 mark if no label present on diagram] & [–1 mark for additional incorrect forces]', decoded: 'Weight (2m); (approximately) equals normal/reaction force (2m); one-mark deductions for a missing label or additional incorrect forces.', marks: 4 },
    ],
    pitfall: {
      text: 'The scheme’s fixed unit rule applies to every final answer here: "For omission of appropriate units (or for incorrect units) in final answers, one mark is deducted, unless otherwise indicated."',
      cite: 'SEC Marking Scheme 2025 (Physics HL), general instruction 6, p.3',
    },
    cite: CITE_25('Q7'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC021ALP000EV.pdf', n: '8',
    totalMarks: 56,
    headline: 'A 56-mark waves question (transverse waves, diffraction): several parts split unevenly (4 + 2, 6 + 3), and the grating calculation is a 6/3/3 ladder.',
    parts: [
      { part: '(i)', task: 'Explain what is meant by a transverse wave', notation: '[3] + [3]', decoded: 'Vibration is perpendicular (3m); to the direction of travel (3m).', marks: 6 },
      { part: '(ii)', task: 'Describe an experiment to show light waves are transverse', notation: '[3] + [3] + [3]', decoded: 'Apparatus: two pieces of polaroid and a light source (3m); method: rotate one polaroid relative to the other (3m); result: light intensity decreases (3m).', marks: 9 },
      { part: '(iii)', task: 'State two conditions necessary for total destructive interference', notation: '[4 + 2]', decoded: 'Same amplitude (4m); crest meets trough (2m).', marks: 6 },
      { part: '(iv)', task: 'Explain how the interference pattern is formed from the laser light', notation: '[6 + 3]', decoded: 'Each slit acts as a source / waves diffract / waves meet (6m); constructive interference gives bright fringes (3m).', marks: 9 },
      { part: '(v)', task: 'Calculate the number of lines per mm on the diffraction grating', notation: '[6] + [3] + [3]', decoded: 'nλ = d sin θ (6m); θ = 24.5° (3m); number of lines/mm = 300 (3m).', marks: 12 },
      { part: '(vi)', task: 'Calculate the maximum number of images that could be observed', notation: '[3] + [2] + [1]', decoded: 'n_max = d/λ (3m); n_max = 4 (2m); maximum number of images = (4 + 1 + 4) = 9 (1m).', marks: 6 },
      { part: '(vii)', task: 'Describe the effect on the pattern of (a) longer wavelength, (b) more lines per mm', notation: '[4 + 2]', decoded: '(a) distance between fringes increases / fewer images (4m); (b) distance between fringes increases / fewer images (2m).', marks: 6 },
      { part: '(viii)', task: 'State one type of electromagnetic radiation with a shorter wavelength than visible light', notation: '[2]', decoded: 'One 2-mark element: UV / X-rays / gamma rays.', marks: 2 },
    ],
    cite: CITE_25('Q8'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC021ALP000EV.pdf', n: '9',
    totalMarks: 56,
    headline: 'A 56-mark photoelectric effect question: Einstein’s explanation and the photocell diagram carry three 3-mark granules each; each calculation is a formula + answer pair.',
    parts: [
      { part: '(i)(a)', task: 'Explain what is meant by a photon', notation: '[3]', decoded: 'One 3-mark element: a bundle of energy // E = hf & notation.', marks: 3 },
      { part: '(i)(b)', task: 'Explain what is meant by the photoelectric effect', notation: '[3] + [3]', decoded: 'Emission of electrons from a metal surface (3m); by electromagnetic radiation of a suitable frequency (3m).', marks: 6 },
      { part: '(ii)', task: 'Outline Einstein’s explanation of the photoelectric effect', notation: '[3] + [3] + [3]', decoded: 'Electromagnetic radiation consists of photons; an electron absorbs the energy of one photon only; energy gained ≥ work function / formula & notation — 3 marks each.', marks: 9 },
      { part: '(iii)', task: 'Draw a labelled diagram of the structure of a photocell', notation: '[3 + 3 + 3] [–1 if no label present on diagram]', decoded: 'Vacuum in tube, cathode, anode — 3 marks each; one mark deducted if the diagram has no label.', marks: 9 },
      { part: '(iv)(a)', task: 'Calculate the energy of a photon falling on the photocell', notation: '[3] + [3] + [3]', decoded: 'Ф = 4.33 × 10⁻¹⁹ J (3m); E = Φ + ½mv² (3m); E = 6.57 × 10⁻¹⁹ J (3m).', marks: 9 },
      { part: '(iv)(b)', task: 'Calculate the frequency of the photon', notation: '[3] + [3]', decoded: 'f_photon = E_photon/h (3m); f_photon = 9.91 × 10¹⁴ Hz (3m).', marks: 6 },
      { part: '(iv)(c)', task: 'Calculate the number of electrons emitted per second', notation: '[3] + [3]', decoded: 'q = It (3m); number of electrons per second = 3.12 × 10¹³ (3m).', marks: 6 },
      { part: '(v)', task: 'Explain how thermionic emission differs from photoelectric emission', notation: '[2 + 2]', decoded: 'Thermionic emission due to heat (2m); photoelectric effect due to electromagnetic radiation (2m).', marks: 4 },
      { part: '(vi)', task: 'Explain why X-ray production is the inverse of the photoelectric effect', notation: '[2 + 2]', decoded: 'X-ray production: electrons produce X-rays (2m); photoelectric effect: X-rays produce electrons (2m).', marks: 4 },
    ],
    cite: CITE_25('Q9'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC021ALP000EV.pdf', n: '10',
    totalMarks: 56,
    headline: 'A 56-mark heat question: paired definitions at 3 + 3, a three-stage calorimetry calculation, and a single 6-mark granule for the Celsius-scale equation.',
    parts: [
      { part: '(i)(a)', task: 'Explain what is meant by specific heat capacity', notation: '[3] + [3]', decoded: 'Energy // c = ΔE/mΔθ (3m); required to raise the temperature of 1 kg by 1 K // notation (3m).', marks: 6 },
      { part: '(i)(b)', task: 'Explain what is meant by specific latent heat', notation: '[3] + [3]', decoded: 'Energy // l = ΔE/m (3m); required to change the state of 1 kg of substance // notation (3m).', marks: 6 },
      { part: '(ii)(a)', task: 'Calculate the energy gained by the calorimeter', notation: '[3] + [3]', decoded: 'ΔE_cal = mcΔθ (3m); ΔE_cal = 1560 J (3m).', marks: 6 },
      { part: '(ii)(b)', task: 'Calculate the energy needed to melt the ice', notation: '[3] + [3]', decoded: 'ΔE_ice = ml_ice (3m); ΔE_ice = 16500 J (3m).', marks: 6 },
      { part: '(ii)(c)', task: 'Calculate the mass of steam added to the water', notation: '[3] + [2] + [2] + [2]', decoded: 'ΔE_steam = (1560 + 16500 + (0.5)(4180)(20)) = 59860 J (3m); (ml)_steam = 2.3 × 10⁶ m (2m); (mcΔθ)_condensed steam = 334400 m (2m); m_steam = 0.0227 kg (2m).', marks: 9 },
      { part: '(iii)', task: 'State the equation that defines temperature on the Celsius scale', notation: '[6] [accept reference to 273(.15) for 3 marks]', decoded: 'θ/°C = T/K − 273.15 (6m); a reference to 273(.15) earns 3 of the 6.', marks: 6 },
      { part: '(iv)', task: 'Suggest a reason why the Celsius scale is used for everyday purposes', notation: '[3]', decoded: 'One 3-mark element: developed before the Kelvin scale / based on melting & freezing point of water.', marks: 3 },
      { part: '(v)', task: 'Calculate the length of the mercury column at 42 °C', notation: '[3] + [3] + [2] + [2]', decoded: '100 units = 27 cm // axes labelled (3m); 1 unit = 0.27 cm // points plotted (3m); 42 units = 11.34 cm // line of best fit (2m); length = (11.34 + 3) = 14.34 cm // length ≈ 14.34 cm (2m).', marks: 10 },
      { part: '(vi)', task: 'Explain why it is necessary to have a standard thermometer', notation: '[4]', decoded: 'One 4-mark element: different thermometers have different thermometric properties.', marks: 4 },
    ],
    pitfall: {
      text: 'On multi-step calculations like these, the scheme’s fixed rule is per slip, not per answer: "Each time an arithmetical slip occurs in a calculation, one mark is deducted."',
      cite: 'SEC Marking Scheme 2025 (Physics HL), general instruction 8, p.3',
    },
    cite: CITE_25('Q10'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC021ALP000EV.pdf', n: '11',
    totalMarks: 56,
    headline: 'A 56-mark electricity question (circuits, potential divider): the two definitions are 4 + 2 splits, and each circuit calculation is a 3-mark ladder.',
    parts: [
      { part: '(i)(a)', task: 'Explain what is meant by resistance', notation: '[4 + 2]', decoded: 'Voltage // R = V/I (4m); per unit current // notation (2m).', marks: 6 },
      { part: '(i)(b)', task: 'Explain what is meant by potential difference', notation: '[4 + 2]', decoded: 'Work done // V = W/q (4m); per unit charge // notation (2m).', marks: 6 },
      { part: '(ii)', task: 'Derive an expression for the total resistance of R₁ and R₂ (in parallel)', notation: '[3] + [3] + [3]', decoded: 'I_tot = I₁ + I₂ (3m); I = V/R (3m); 1/R_tot = 1/R₁ + 1/R₂ (3m).', marks: 9 },
      { part: '(iii)', task: 'Calculate the total resistance of the circuit when the switch is closed', notation: '[3] + [3]', decoded: 'R_parallel = 2.67 Ω (3m); R_circuit = 10.67 Ω (3m).', marks: 6 },
      { part: '(iv)', task: 'Calculate the potential difference between X and Y when the switch is closed', notation: '[3] + [3]', decoded: 'I = (V/R = 12/10.67) = 1.125 A // 2.67/10.67 (3m); V_XY = (R × I) = 3 V // (0.25 × 12) = 3 V (3m).', marks: 6 },
      { part: '(v)', task: 'What happens to the potential difference between X and Y when the switch is opened?', notation: '[4]', decoded: 'One 4-mark element: potential difference increases.', marks: 4 },
      { part: '(vi)', task: 'Explain what is meant by a thermistor', notation: '[3] + [3]', decoded: 'Resistance changes (3m); (significantly) with temperature (3m).', marks: 6 },
      { part: '(vii)', task: 'Calculate the minimum thermistor resistance required to switch on the heater', notation: '[3] + [3] + [3]', decoded: 'R₂/R₁ = V₂/V₁ (3m); R₂ = 5000(8/4) (3m); R₂ = 10000 Ω (3m).', marks: 9 },
      { part: '(viii)', task: 'What change to the variable resistor makes the heater switch on at a higher temperature?', notation: '[4]', decoded: 'One 4-mark element: resistance must decrease. (Scheme note: valid reference to a PTC thermistor is acceptable for full marks.)', marks: 4 },
    ],
    pitfall: {
      text: 'The definitions here are marked with the double solidus: "Answers that are separated by a double solidus, //, are answers which are mutually exclusive. A partial answer from one side of the // may not be taken in conjunction with a partial answer from the other side."',
      cite: 'SEC Marking Scheme 2025 (Physics HL), general instruction 3, p.3',
    },
    cite: CITE_25('Q11'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC021ALP000EV.pdf', n: '13',
    totalMarks: 56,
    headline: 'A 56-mark comprehension question (Faraday passage): explanation pairs at 4 + 3, and the wire calculations in 2-mark granules including one for the force’s direction.',
    parts: [
      { part: '(i)', task: 'Explain what is meant by (a) a magnetic field, (b) a magnetic field line', notation: '[4 + 3]', decoded: '(a) space in which magnetic force is experienced (4m); (b) line showing direction of magnetic field (3m).', marks: 7 },
      { part: '(ii)', task: 'Distinguish between scalar and vector quantities', notation: '[4 + 3]', decoded: 'Scalar has magnitude only (4m); vector has magnitude and direction (3m).', marks: 7 },
      { part: '(iii)(a)', task: 'Calculate the resistance of the wire', notation: '[2] + [2] + [2]', decoded: 'A = 1.119 × 10⁻⁷ m² (2m); ρ = RA/l (2m); R = 0.5 Ω (2m).', marks: 6 },
      { part: '(iii)(b)', task: 'Calculate the force acting on the wire', notation: '[2] + [2] + [2] + [2]', decoded: 'I = V/R = 0.45 A (2m); F = BIl (2m); F = 3.375 × 10⁻³ N (2m); out of the page (2m).', marks: 8 },
      { part: '(iv)', task: 'Calculate the average EMF induced in the coil', notation: '[4] + [3]', decoded: 'E = (−)dΦ/dt (4m); E = 61.4 V (3m).', marks: 7 },
      { part: '(v)(a)', task: 'Explain what is meant by self-induction', notation: '[3] + [2]', decoded: 'Changing current in a coil / changing magnetic field produced by a coil (3m); induces a (back) emf in the coil itself (2m).', marks: 5 },
      { part: '(v)(b)', task: 'State one practical use of self-induction', notation: '[2]', decoded: 'One 2-mark element: e.g. smoothing in power supply units / tuning circuits / stage lighting.', marks: 2 },
      { part: '(vi)(a)', task: 'State the turns ratio of the step-down transformer', notation: '[3] + [2]', decoded: 'Ns/Np (3m); 1500:1 (2m).', marks: 5 },
      { part: '(vi)(b)', task: 'Explain why a transformer does not work with direct current', notation: '[2]', decoded: 'One 2-mark element: no changing current / no changing magnetic field.', marks: 2 },
      { part: '(vii)', task: 'Calculate the RMS current flowing in the appliance', notation: '[4] + [3]', decoded: 'I_rms = I₀/√2 (4m); I_rms = 5.65 A (3m).', marks: 7 },
    ],
    cite: CITE_25('Q13'),
  },
];

const PHYSICS_LENS: SubjectLens = {
  subjectId: 'physics',
  entries: [
    ...HL_2023_EV,
    ...mirrorIV(HL_2023_EV),
    ...HL_2025_EV,
    ...mirrorIV(HL_2025_EV),
  ],
};

export default PHYSICS_LENS;
