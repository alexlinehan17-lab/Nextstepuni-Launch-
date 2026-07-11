/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Marking Lens — Design & Communication Graphics (written paper, Higher Level).
 *
 * Sources of truth (both in examiner-reports/dcg/, md cross-checked against the
 * SEC PDFs page by page):
 *  - 2024-marking-scheme.md / .pdf — SEC Marking Scheme 2024, DCG Higher Level
 *  - 2025-marking-scheme.md / .pdf — SEC Marking Scheme 2025, DCG Higher Level
 *
 * The DCG scheme has no compact "3 @ 5m" shorthand: every question is an
 * additive ladder of named roman-numeral construction steps, each carrying an
 * explicit numeral, with printed part subtotals and "Total = 60". `notation`
 * therefore quotes the step numerals verbatim keyed by the scheme's roman
 * indices; the steps' graphical names are restated faithfully in `decoded`.
 *
 * Keys (year/level/lang/fileid/n) match the Topic Vault tags exactly. The tags
 * cover ONLY the Section B & C answer booklet (LC562ALP039EV/IV.pdf); tag n
 * '1'–'8' maps in order to the scheme's printed labels
 * [B-1, B-2, B-3, C-1, C-2, C-3, C-4, C-5]. Mapping verified per year against
 * the curriculum topic labels (scripts/paper-trail/topic-tags/tags/
 * design-and-communication-graphics.json + curriculum.ts):
 *  - 2024: n2 Developments+Conics ↔ B-2 salad-box development + ellipse;
 *    n3 Axonometric ↔ B-3 trimetric; n4 Geologic ↔ C-1 earthworks;
 *    n5 Structural Forms ↔ C-2 hyperbolic paraboloid; n7 Dynamic Mechanisms ↔
 *    C-4 epicycloid/spiral loci; n8 Assemblies ↔ C-5 sectional elevation.
 *  - 2025: n1 Conic Sections ↔ B-1 parabola bridge; n2 Intersecting Planes ↔
 *    B-2 dihedral angle/traces; n3 Perspective ↔ B-3 kiosk perspective;
 *    n4 Geologic ↔ C-1 earthworks + strike/dip; n7 Dynamic Mechanisms ↔
 *    C-4 cam + locus; n8 Assemblies ↔ C-5 sectional elevation.
 *
 * NOT covered (deliberately):
 *  - Section A (A-1..A-4, 20 marks each): its pre-printed answer booklet
 *    (LC562ALP014*) is not tagged in the Topic Vault, so Section A lenses would
 *    be orphans — the scheme evidence exists but there is no key to attach it to.
 *  - Ordinary Level: tagged, but no OL scheme is filed in examiner-reports/dcg/.
 */

import { type QuestionLens, type SubjectLens } from './types';

const CITE_2024 = (q: string) =>
  `SEC Marking Scheme 2024, Design & Communication Graphics Higher Level, Question ${q}`;
const CITE_2025 = (q: string) =>
  `SEC Marking Scheme 2025, Design & Communication Graphics Higher Level, Question ${q}`;

// The IV paper is the same exam marked by the same scheme — mirror EV entries.
const mirrorIV = (entries: QuestionLens[], fileid: string): QuestionLens[] =>
  entries.map(e => ({ ...e, lang: 'iv', fileid }));

// ── 2024 HL — Section B & C booklet (tag n '1'–'8' = B-1..B-3, C-1..C-5) ─────

const HL_2024_EV: QuestionLens[] = [
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC562ALP039EV.pdf', n: '1',
    totalMarks: 60,
    headline: 'B-1 (studio desk): four lettered parts (20 + 20 + 13 + 7); every mark names one auxiliary-view construction step.',
    parts: [
      {
        part: '(a)', task: 'Plan and Elevation of studio desk',
        notation: '(i) 12 + (ii) 8',
        decoded: 'Drawing the given outline plan of the inverted square-based pyramid carries 12 marks; drawing its given elevation carries 8.',
        marks: 20,
      },
      {
        part: '(b)', task: 'Dihedral Angle between surfaces A and B',
        notation: '(iii) 6 + (iv) 4 + (v) 5 + (vi) 5',
        decoded: 'X1Y1 parallel to the line of intersection (6), projection of the planes and line of intersection on the new X1Y1 (4), new X2Y2 perpendicular to the line of intersection (5), projection of the planes as lines and indicating the dihedral angle (5).',
        marks: 20,
      },
      {
        part: '(c)', task: 'Inclination of surface B to horizontal plane and true shape of surface B',
        notation: '(vii) 3 + (viii) 3 + (ix) 2 + (x) 2 + (xi) 3',
        decoded: 'X1Y1 perpendicular to the strike line on surface B (3), projection of surface B to the auxiliary view (3), determining the true inclination to the horizontal plane (2), X2Y2 parallel to the edge view of surface B (2), projection of the true shape to the auxiliary view (3).',
        marks: 13,
      },
      {
        part: '(d)', task: 'Elevation and Plan of a line inclined at 50° to HP from point P',
        notation: '(xii) 2 + (xiii) 2 + (xiv) 2 + (xv) 1',
        decoded: 'Establishing the 50° inclination from P to HP in elevation (2), projections of the true angle in the plan view (2), projections of the required line in plan (2) and in elevation (1).',
        marks: 7,
      },
    ],
    cite: CITE_2024('B-1'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC562ALP039EV.pdf', n: '2',
    totalMarks: 60,
    headline: 'B-2 (salad box): three lettered parts (16 + 18 + 26); development first, then the ellipse construction, then the projected views.',
    parts: [
      {
        part: '(a)', task: 'Draw given surface development of salad box',
        notation: '(i) 4 + (ii) 8 + (iii) 4',
        decoded: 'The base of the salad box (4), its sides (8) and its top (4).',
        marks: 16,
      },
      {
        part: '(b)', task: 'Draw the elliptical plastic window',
        notation: '(iv) 2 + (v) 2 + (vi) 3 + (vii) 8 + (viii) 3 (any = 1)',
        decoded: 'Establishing the major axis (2), locating point P (2), determining the length of the minor axis (3), the construction to determine points on the ellipse (8), drawing the elliptical curve (3, "any = 1").',
        marks: 18,
      },
      {
        part: '(c)', task: 'Draw elevation and plan of salad box',
        notation: '(ix) 2 + (x) 4 + (xi) 4 + (xii) 2 + (xiii) 6 + (xiv) 3 + (xv) 2 + (xvi) 2 + (xvii) 1',
        decoded: 'Height of the box in elevation (2), elevation outline (4), points on the elliptical curve in elevation (4), the elevation curve (2, "any = 1"), plan outline (6), the elliptical curve on the top surface in plan (3), points on the front-surface curve in plan (2), that curve (2, "any = 1"), hidden detail (1).',
        marks: 26,
      },
    ],
    cite: CITE_2024('B-2'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC562ALP039EV.pdf', n: '3',
    totalMarks: 60,
    headline: 'B-3 (puzzle stand): four lettered parts (8 + 23 + 25 + 4); the trimetric build-up is marked plane by plane, curve points before curves.',
    parts: [
      {
        part: '(a)', task: 'Axonometric axes and scalene triangle',
        notation: '(i) 2 (1,1) + (ii) 4 + (iii) 2',
        decoded: 'Axonometric axes X and Y as orientated (1 mark each), the scalene triangle abc (4), the Z axis (2).',
        marks: 8,
      },
      {
        part: '(b)', task: 'Draw plan and end elevation, orientated as shown',
        notation: '(iv) 6 + (v) 6 + (vi) 6 + (vii) 5',
        decoded: 'Correct development of the YZ plane in the required orientation (6), the end elevation as given (6), correct development of the XZ plane (6), the plan as given (5).',
        marks: 23,
      },
      {
        part: '(c)', task: 'Complete the trimetric projection of the puzzle stand',
        notation: '(viii) 4 + (ix) 7 + (x) 5 + (xi) 2 + (xii) 3 + (xiii) 2 + (xiv) 2',
        decoded: 'Projections from the end elevation and plan (4), the axonometric of the triangular prism (7), points on the top circular curve (5), that curve (2, "Any = 1"), points on the curve of intersection with the inclined surface (3), that curved line (2, "Any = 1"), completing the cylindrical holder (2).',
        marks: 25,
      },
      {
        part: '(d)', task: 'Complete the trimetric projection of the sphere',
        notation: '(xv) 4',
        decoded: 'Locating and drawing the sphere (4).',
        marks: 4,
      },
    ],
    cite: CITE_2024('B-3'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC562ALP039EV.pdf', n: '4',
    totalMarks: 60,
    headline: 'C-1 (rafting course): earthworks marked stretch by stretch (39), then the profile (13) and pole height (8) — interval lines first, contour-intersection curves second.',
    parts: [
      {
        part: '(a)', task: 'Earthworks on rafting course',
        notation: '(i) 4 + (ii) 4 + (iii) 4 + (iv) 4 + (v) 3 + (vi) 3 + (vii) 2 + (viii) 3 + (ix) 3 + (x) 3 + (xi) 2 + (xii) 2 + (xiii) 2',
        decoded: 'Each stretch is marked in two moves — draw the parallel lines/arcs at the stated interval (7.5 mm embankment, 10 mm cutting), then identify the intersections with the contours and draw the curves: A–B level embankment (4 + 4), A–B level cutting (4 + 4), B–C curved cutting (3 + 3); the rising C–D cutting adds establishing the 55 m height (2) and the repositioned 10 mm arc with tangent (3) before its lines (3) and curve (3); the C–D embankment takes the 7.5 mm arc at C with tangent (2), its lines (2) and curve (2).',
        marks: 39,
      },
      {
        part: '(b)', task: 'Profile on EF',
        notation: '(xiv) 2 + (xv) 2 + (xvi) 4 + (xvii) 5',
        decoded: 'Height lines at 5 mm intervals (2), projections from the intersections of line EF with the contours (2), the curved profile through the contours (4), its intersection with the course cuttings and the level rafting course (5).',
        marks: 13,
      },
      {
        part: '(c)', task: 'Height for zipline support pole above point F',
        notation: '(xviii) 2 + (xix) 4 + (xx) 2',
        decoded: 'Locating the tower height at E (2), the circle of radius 10 m above the highest position with its tangent (4), determining and indicating the required pole height at F (2).',
        marks: 8,
      },
    ],
    cite: CITE_2024('C-1'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC562ALP039EV.pdf', n: '5',
    totalMarks: 60,
    headline: 'C-2 (hyperbolic paraboloid): four lettered parts (18 + 10 + 20 + 12); the element and point constructions carry the marks before each curve is drawn.',
    parts: [
      {
        part: '(a)', task: 'Draw given elevation including elements',
        notation: '(i) 6 + (ii) 6 + (iii) 6',
        decoded: 'Parallelogram ABCD (6), locating and drawing the elements of the hyperbolic paraboloid (6), completing the elevation outline of the net (6).',
        marks: 18,
      },
      {
        part: '(b)', task: 'Project end view of surface ABCD',
        notation: '(iv) 4 + (v) 6',
        decoded: 'The outline elements of the hyperbolic paraboloid (4), locating and drawing the inner elements (6).',
        marks: 10,
      },
      {
        part: '(c)', task: 'Complete end view by extending elements',
        notation: '(vi) 4 + (vii) 8 + (viii) 2 + (ix) 3 + (x) 3 (any = 1)',
        decoded: 'Extending the elements in elevation (4), establishing points in the end view by extending elements (8), the construction to determine point P (2), the construction for an intermediate point in the end view (3), drawing the required curve AP (3, "any = 1").',
        marks: 20,
      },
      {
        part: '(d)', task: 'Curvature of the surface through points D and B',
        notation: '(xi) 2 + (xii) 3 + (xiii) 4 + (xiv) 3 (any = 1)',
        decoded: 'Use of the line joining B and D in elevation (2), projections from its intersections with the elements to plan (3), establishing the widths in plan (4), drawing the required curvature (3, "any = 1").',
        marks: 12,
      },
    ],
    cite: CITE_2024('C-2'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC562ALP039EV.pdf', n: '6',
    totalMarks: 60,
    headline: 'C-3 (chimena): four lettered parts (23 + 13 + 19 + 5); each surface development follows a fixed ladder — apex/size, generators, elements, completion.',
    parts: [
      {
        part: '(a)', task: 'Draw the given plan and elevation of the chimena',
        notation: '(i) 4 + (ii) 3 + (iii) 5 + (iv) 6 + (v) 5',
        decoded: 'Plan of the chimena body and chimney (4), position and length of the legs in plan (3), the elevation outline (5), locating the centre for the opening and drawing it (6), the legs in elevation with their intersection points located in plan (5).',
        marks: 23,
      },
      {
        part: '(b)', task: 'Surface development of conical surface A',
        notation: '(vi) 2 + (vii) 2 + (viii) 4 + (ix) 2 + (x) 3',
        decoded: 'Locating the apex on the development (2), transferring the longest generator length (2), establishing 12 elements in the development (4), transferring the cut generator lengths (2), completing the surface development (3).',
        marks: 13,
      },
      {
        part: '(c)', task: 'Surface development of cylindrical surface B',
        notation: '(xi) 5 + (xii) 2 + (xiii) 4 + (xiv) 5 + (xv) 3',
        decoded: 'Establishing the overall length and height of the development (5), projecting the heights of the opening (2), establishing the length and position of the opening (4), determining the development of the arc at the top of the opening (5), completing the surface development (3).',
        marks: 19,
      },
      {
        part: '(d)', task: 'Determine and indicate inclination of leg to HP',
        notation: '(xvi) 2 + (xvii) 3',
        decoded: 'Use of an appropriate method to determine the inclination of the leg to the HP (2), then determining and indicating that inclination (3).',
        marks: 5,
      },
    ],
    cite: CITE_2024('C-3'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC562ALP039EV.pdf', n: '7',
    totalMarks: 60,
    headline: 'C-4 (loci): two parts (32 + 28); the largest single allocations are the rolling-circle locus points (12) and the intermediate spiral radii (8).',
    parts: [
      {
        part: '(a)', task: 'Plot the epicycloid',
        notation: '(i) 6 + (ii) 4 + (iii) 6 + (iv) 12 + (v) 4 (any = 1)',
        decoded: 'Drawing the given arc PA and circle C (6), dividing circle C into equal parts — 12 minimum (4), dividing arc PA into a corresponding number of parts (6), locating points on the locus as the circle rolls along the arc (12), drawing the epicycloid (4, "any = 1").',
        marks: 32,
      },
      {
        part: '(b)', task: 'Archimedean spiral of a spiral galaxy',
        notation: '(vi) 4 + (vii) 4 + (viii) 4 + (ix) 4 + (x) 8 + (xi) 4 (any = 1)',
        decoded: 'Drawing the given diagram — points O, A and B (4), determining the radius-vector length at 30° (4), stepping the radius-vector length to determine point C (4), establishing 12 equal 30° divisions (4), the corresponding intermediate radii on the angular divisions (8), drawing the Archimedean spiral (4, "any = 1").',
        marks: 28,
      },
    ],
    cite: CITE_2024('C-4'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC562ALP039EV.pdf', n: '8',
    totalMarks: 60,
    headline: 'C-5 (ratchet assembly): one 60-mark sectional elevation marked component by component — outline and inner detail carry separate marks, presentation/hatching the final 6.',
    parts: [
      { part: 'Assembly', task: 'Relative positioning of main components', notation: '(i) 6', decoded: 'Correct relative positioning of the main components (6).', marks: 6 },
      { part: 'Main Body', task: 'Outline and inner detail of the main body', notation: '(ii) 8 + (iii) 4', decoded: 'The complete outline of the main body (8) and its inner detail (4).', marks: 12 },
      { part: 'Ratchet Pulley', task: 'Outline and inner detail of the pulley', notation: '(iv) 6 + (v) 6', decoded: 'The outline of the pulley (6) and its inner detail (6).', marks: 12 },
      { part: 'Washers', task: 'Outline of two washers on axle', notation: '(vi) 2 (1,1)', decoded: 'One mark per washer on the axle.', marks: 2 },
      { part: 'Axle Bolt', task: 'Required detail of the axle bolt', notation: '(vii) 4', decoded: 'The required detail of the axle bolt (4).', marks: 4 },
      { part: 'Pin', task: 'Outline of the pin in axle', notation: '(viii) 2', decoded: 'The outline of the pin in the axle (2).', marks: 2 },
      { part: 'Handle', task: 'Vertical arm, inner detail and horizontal handle', notation: '(ix) 4 + (x) 2 + (xi) 2', decoded: 'The outline of the vertical arm of the handle (4), its inner detail (2), the horizontal handle (2).', marks: 8 },
      { part: 'Pawl', task: 'Representation of the pawl', notation: '(xii) 3', decoded: 'The representation of the pawl (3).', marks: 3 },
      { part: 'M6 x 20 Set Screws', task: 'Set screw in axle and set screw in pawl', notation: '(xiii) 2 + (xiv) 2', decoded: 'Representing the set screw in the axle (2) and in the pawl (2).', marks: 4 },
      { part: 'Plain nut', task: 'Representation of the nut', notation: '(xv) 1', decoded: 'The representation of the nut (1).', marks: 1 },
      { part: 'Completion of drawing', task: 'Presentation, hatching and centre lines', notation: '(xvi) 6', decoded: 'Presentation, hatching and centre lines (6).', marks: 6 },
    ],
    cite: CITE_2024('C-5'),
  },
];

// ── 2025 HL — Section B & C booklet (tag n '1'–'8' = B-1..B-3, C-1..C-5) ─────

const HL_2025_EV: QuestionLens[] = [
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC562ALP039EV.pdf', n: '1',
    totalMarks: 60,
    headline: 'B-1 (parabolic bridge): three lettered parts (16 + 29 + 15); the parabola construction, the projected views and the rotated position are each step-laddered.',
    parts: [
      {
        part: '(a)', task: 'Draw the given elevation',
        notation: '(i) 3 + (ii) 7 + (iii) 3 + (iv) 3',
        decoded: 'The rectangular outline of the parabola (3), the construction to determine points on parabola ABC in elevation (7), the parabolic curve ABC (3), the support cables (3).',
        marks: 16,
      },
      {
        part: '(b)', task: 'Project plan and end view of bridge in closed position',
        notation: '(v) 3 + (vi) 3 + (vii) 3 + (viii) 2 + (ix) 2 + (x) 6 + (xi) 3 + (xii) 2 + (xiii) 5',
        decoded: 'Centreline AC in plan (3), the centre point of arc ADC in plan (3), the circular arc ADC (3), the end view of ADC (2), completing the end-view outline (2), the projection of curve ABC to plan (6), curve ABC in plan (3), the support cables in plan (2) and their end view (5).',
        marks: 29,
      },
      {
        part: '(c)', task: 'Draw end view of rotated bridge and projection of elevation',
        notation: '(xiv) 3 + (xv) 3 + (xvi) 3 + (xvii) 3 + (xviii) 3',
        decoded: 'The end view of the bridge in the rotated position (3), the cables in the rotated position (3), projecting the endpoints of the cables on ABC to elevation (3), the elevation of curve ABC (3) and of curve ADC (3) in the rotated position.',
        marks: 15,
      },
    ],
    cite: CITE_2025('B-1'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC562ALP039EV.pdf', n: '2',
    totalMarks: 60,
    headline: 'B-2 (intersecting planes): four lettered parts (16 + 17 + 17 + 10); dihedral angle, true shape and traces each follow a fixed auxiliary-view ladder.',
    parts: [
      {
        part: '(a)', task: 'Elevation and plan of intersecting planes ABC, BCD, and CDE',
        notation: '(i) 8 + (ii) 8',
        decoded: 'Using the given coordinates to draw the elevation of ABC, BCD and CDE (8), then drawing the plan of the three planes (8).',
        marks: 16,
      },
      {
        part: '(b)', task: 'Dihedral Angle between surfaces ABC and BCD',
        notation: '(iii) 4 + (iv) 4 + (v) 4 + (vi) 5',
        decoded: 'X1Y1 parallel to the line of intersection BC (4), projection of the planes and BC on the new X1Y1 (4), new X2Y2 perpendicular to BC (4), projecting planes ABC and BCD as lines and determining the dihedral angle (5).',
        marks: 17,
      },
      {
        part: '(c)', task: 'True shape of surface CDE',
        notation: '(vii) 3 + (viii) 3 + (ix) 3 + (x) 3 + (xi) 5',
        decoded: 'Projections of a horizontal line on CDE (3), X1Y1 perpendicular to the plan of the correct strike line (3), projection of plane CDE to the auxiliary view (3), X2Y2 parallel to the edge view of CDE (3), projection of the true shape to the auxiliary view (5).',
        marks: 17,
      },
      {
        part: '(d)', task: 'Determine horizontal and vertical traces of plane ABC',
        notation: '(xii) 3 + (xiii) 2 + (xiv) 3 + (xv) 2',
        decoded: 'Establishing a second point on the horizontal trace (3) and drawing it (2); determining a second point on the vertical trace (3) and drawing it (2).',
        marks: 10,
      },
    ],
    cite: CITE_2025('B-2'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC562ALP039EV.pdf', n: '3',
    totalMarks: 60,
    headline: 'B-3 (kiosk): perspective marked as a build sequence — the given plan (9), then 46 marks across eleven perspective steps, then the height of point C (5).',
    parts: [
      {
        part: '(a)', task: 'Draw given plan',
        notation: '(i) 9',
        decoded: 'Drawing the given plan of the kiosk (9).',
        marks: 9,
      },
      {
        part: '(b)', task: 'Draw perspective of Kiosk',
        notation: '(ii) 4 + (iii) 4 + (iv) 4 + (v) 1 + (vi) 4 + (vii) 2 + (viii) 7 + (ix) 6 + (x) 5 + (xi) 7 + (xii) 2',
        decoded: 'Positioning the spectator and the plan of the picture plane (4), the plan of the vanishing points (4), the ground line, horizon line and vanishing points in elevation (4), establishing corner A in the perspective view (1), the perspective of the base lines (4), applying heights above corner A (2), completing the outline of the kiosk (7), establishing the heights for the washing windows (6), completing the windows in perspective (5), use of the AVP for the perspective of sloping surface B (7), completing the perspective drawing (2).',
        marks: 46,
      },
      {
        part: '(c)', task: 'Determine and indicate height of point C',
        notation: '(xiii) 3 + (xiv) 2',
        decoded: 'Establishing the height for point C (3) and indicating the correct height (2).',
        marks: 5,
      },
    ],
    cite: CITE_2025('B-3'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC562ALP039EV.pdf', n: '4',
    totalMarks: 60,
    headline: 'C-1 (roadway): earthworks as ten uniform 4-mark steps (40), then a six-step strike/dip/thickness ladder (20).',
    parts: [
      {
        part: '(a)', task: 'Earthworks on roadway',
        notation: '(i) 4 + (ii) 4 + (iii) 4 + (iv) 4 + (v) 4 + (vi) 4 + (vii) 4 + (viii) 4 + (ix) 4 + (x) 4',
        decoded: 'Ten 4-mark steps across the three stretches — A–B level embankment: parallel lines at 7.5 mm intervals, then the curves at the contour intersections; A–B level cutting: 5 mm-interval lines to the corner and their curve, then from the corner to B and their curve; B–C falling embankment: establishing the 70 m height on the roadway, the 7.5 mm arc at B with tangent, the 7.5 mm-interval lines, and the curves at the contour intersections.',
        marks: 40,
      },
      {
        part: '(b)', task: 'Strike, Dip and Thickness of stratum',
        notation: '(xi) 2 + (xii) 2 + (xiii) 2 + (xiv) 3 + (xv) 3 + (xvi) 8',
        decoded: 'A line from Sh parallel to RfSf (or Sf parallel to RhSh) in elevation (2) and in plan (2), a horizontal line on either plane in elevation (2), determining the strike line in plan (3), X1Y1 perpendicular to the strike line (3), establishing the required dip angle and the thickness of the stratum (8).',
        marks: 20,
      },
    ],
    cite: CITE_2025('C-1'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC562ALP039EV.pdf', n: '5',
    totalMarks: 60,
    headline: 'C-2 (hyperboloid): three lettered parts (39 + 15 + 6); the hyperbola point constructions carry the big marks before any curve is drawn.',
    parts: [
      {
        part: '(a)', task: 'Draw given plan and elevation',
        notation: '(i) 2 + (ii) 3 + (iii) 5 + (iv) 8 + (v) 4 + (vi) 2 + (vii) 5 + (viii) 2 + (ix) 5 + (x) 3',
        decoded: 'The base circle in plan (2), the base and top circles in elevation (3), locating the throat circle in plan and elevation (5), the construction to determine points on one branch of the hyperbola in elevation (8), the points on the second branch (4), the 30° cut in elevation (2), the hyperbolic curves (5), the end point of the top-cut curve in plan (2), additional points on it (5), drawing the top-cut curve in plan (3).',
        marks: 39,
      },
      {
        part: '(b)', task: 'Project end view',
        notation: '(xi) 2 + (xii) 4 + (xiii) 2 + (xiv) 4 + (xv) 3',
        decoded: 'The base circle in the end view (2), points on the outline hyperbola curves (4), the hyperbolic curves (2), points on the top-cut surface (4), the top-cut curve (3).',
        marks: 15,
      },
      {
        part: '(c)', task: 'Directrix and focal point',
        notation: '(xvi) 3 + (xvii) 3',
        decoded: 'The construction to determine the required directrix (3) and the required focal point (3).',
        marks: 6,
      },
    ],
    cite: CITE_2025('C-2'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC562ALP039EV.pdf', n: '6',
    totalMarks: 60,
    headline: 'C-3 (jug): four lettered parts (24 + 16 + 10 + 10); views, dihedral angle and two surface developments, each a named-step ladder.',
    parts: [
      {
        part: '(a)', task: 'Draw the given plan and elevation',
        notation: '(i) 2 + (ii) 6 + (iii) 4 + (iv) 6 + (v) 4 + (vi) 1 + (vii) 1',
        decoded: 'The octagonal outline in plan (2), the elevation of the conical base, body outline and top of the jug (6), the elevation of the handle and spout (4), the plan of the conical base, body and top (6), the plan of the handle and spout (4), hidden detail in plan (1), completing the elevation of the main body (1).',
        marks: 24,
      },
      {
        part: '(b)', task: 'Dihedral angle between surfaces A and B',
        notation: '(viii) 4 + (ix) 4 + (x) 4 + (xi) 4',
        decoded: 'X1Y1 parallel to the line of intersection (4), projection of surfaces A and B and the line of intersection on the new X1Y1 (4), new X2Y2 perpendicular to the line of intersection (4), projecting both surfaces as lines and determining the dihedral angle (4).',
        marks: 16,
      },
      {
        part: '(c)', task: 'Surface development of conical surface C',
        notation: '(xii) 1 + (xiii) 2 + (xiv) 4 + (xv) 1 + (xvi) 2',
        decoded: 'Locating the apex on the development, to ensure accuracy (1), transferring the longest generator length (2), establishing 12 elements in the development (4), transferring the cut generator lengths (1), completing the surface development (2).',
        marks: 10,
      },
      {
        part: '(d)', task: 'Surface development of the lid',
        notation: '(xvii) 2 + (xviii) 4 + (xix) 4',
        decoded: 'Establishing the true length of the lid edge (2), the correct construction to determine the development (4), completing the surface development (4).',
        marks: 10,
      },
    ],
    cite: CITE_2025('C-3'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC562ALP039EV.pdf', n: '7',
    totalMarks: 60,
    headline: 'C-4 (cam + locus): two parts (35 + 25); each motion (U.A.R., uniform velocity, S.H.M.) carries its own construction marks before the cam profile.',
    parts: [
      {
        part: '(a)', task: 'Displacement Diagram and Cam Profile',
        notation: '(i) 1 + (ii) 2 + (iii) 3 + (iv) 6 + (v) 3 + (vi) 6 + (vii) 3 + (viii) 2 + (ix) 6 + (x) 3',
        decoded: 'The camshaft (1), establishing the "nearest approach" on the cam diagram (2), the horizontal divisions on the displacement diagram (3), the construction for U.A.R. on the displacement diagram — minimum 7 points including end points (6), the uniform-velocity line (3), the construction for S.H.M. (6), dividing the circle into 12 equal 30° parts (3), the required intermediate 20° divisions for the U.A.R. (2), transferring the heights from the displacement diagram to the cam diagram (6), completing the cam diagram (3).',
        marks: 35,
      },
      {
        part: '(b)', task: 'Line Diagram and Locus of point P for one revolution',
        notation: '(xi) 8 + (xii) 3 + (xiii) 3 + (xiv) 6 + (xv) 2 + (xvi) 3',
        decoded: 'The given diagram — points A, B, C, D, E and P (8), dividing the circle into equal parts, 12 minimum (3), the arc with centre B and radius BC (3), using those divisions and that arc to determine points on the locus (6), establishing the turning points of the locus (2), drawing the required locus (3).',
        marks: 25,
      },
    ],
    cite: CITE_2025('C-4'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC562ALP039EV.pdf', n: '8',
    totalMarks: 60,
    headline: 'C-5 (potato-cutter assembly): one 60-mark sectional elevation marked component by component — outline and inner detail carry separate marks, presentation/hatching the final 6.',
    parts: [
      { part: 'Assembly', task: 'Relative positioning of main components', notation: '(i) 7', decoded: 'Correct relative positioning of the main components (7).', marks: 7 },
      { part: 'End Cutter', task: 'Outline and inner detail of the main body', notation: '(ii) 2 + (iii) 5', decoded: 'The complete outline of the main body (2) and its inner detail (5).', marks: 7 },
      { part: 'Right-Hand Cap', task: 'Outline and inner detail of the right-hand cap', notation: '(iv) 5 + (v) 2', decoded: 'The outline of the right-hand cap (5) and its inner detail (2).', marks: 7 },
      { part: 'Plunger Guide Bars', task: 'Outline of the plunger guide bars', notation: '(vi) 3', decoded: 'The outline of the plunger guide bars (3).', marks: 3 },
      { part: 'Potato Guide Bar', task: 'Outline of the potato guide bars', notation: '(vii) 4', decoded: 'The outline of the potato guide bars (4).', marks: 4 },
      { part: 'Sliding Plunger', task: 'Main body of the plunger and its guide arms', notation: '(viii) 5 + (ix) 4', decoded: 'The outline of the main body of the plunger (5) and the detail of the top and bottom guide arms (4).', marks: 9 },
      { part: 'Handle', task: 'Outline and inner detail of handle', notation: '(x) 4 + (xi) 2', decoded: 'The outline of the handle (4) and its inner detail (2).', marks: 6 },
      { part: 'Link Arm', task: 'Outline and inner detail of link arm', notation: '(xii) 2 + (xiii) 3', decoded: 'The outline of the link arm (2) and its inner detail (3).', marks: 5 },
      { part: 'Washers', task: 'Representation of the washers', notation: '(xiv) 3', decoded: 'The representation of the washers (3).', marks: 3 },
      { part: 'M4 x 16 Set Screws', task: 'Representation of the set screws', notation: '(xv) 3', decoded: 'The representation of the set screws (3).', marks: 3 },
      { part: 'Completion of drawing', task: 'Presentation, hatching and centre lines', notation: '(xvi) 6', decoded: 'Presentation, hatching and centre lines (6).', marks: 6 },
    ],
    cite: CITE_2025('C-5'),
  },
];

const DCG_LENS: SubjectLens = {
  subjectId: 'design-and-communication-graphics',
  entries: [
    ...HL_2024_EV,
    ...mirrorIV(HL_2024_EV, 'LC562ALP039IV.pdf'),
    ...HL_2025_EV,
    ...mirrorIV(HL_2025_EV, 'LC562ALP039IV.pdf'),
  ],
};

export default DCG_LENS;
