/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Future Finder — RIASEC + work-values item bank (Phase B of the redesign).
 *
 * 60 RIASEC interest items (10 per scale) + 12 work-values items (2 per value).
 * Design follows the O*NET Interest Profiler development report:
 *  - ACTIVITY statements, never job titles (title items amplify gender/ethnic
 *    stereotypes and narrow horizons; activity items expand the option range).
 *  - plain ~8th-grade reading level, Irish/Leaving-Cert context.
 *  - rated on a 5-point "dislike → like" scale (set in the component).
 *
 * The "Quick" version uses the best 5 items/scale (flagged `quick: true`) — a
 * curated subset, exactly how O*NET ships a Long form + a Short form.
 *
 * NOTE on gender balance: items are written to avoid stereotyped framing, but
 * true endorsement-balance screening (O*NET's rule: no male–female mean
 * difference > .30) requires real response data — a recommended follow-up once
 * the tool has been live and we can analyse responses.
 */
import { type RiasecLetter, type WorkValue } from './futureFinderRiasec';

export interface RiasecItem {
  id: string;
  scale: RiasecLetter;
  /** Activity statement, rated "How much would you enjoy this?" */
  text: string;
  /** In the Quick (short-form) version. Exactly 5 per scale. */
  quick: boolean;
}

export interface ValueItem {
  id: string;
  value: WorkValue;
  /** Rated "How important is this to you?" */
  text: string;
}

const R = (id: string, text: string, quick = false): RiasecItem => ({ id, scale: 'R', text, quick });
const I = (id: string, text: string, quick = false): RiasecItem => ({ id, scale: 'I', text, quick });
const A = (id: string, text: string, quick = false): RiasecItem => ({ id, scale: 'A', text, quick });
const S = (id: string, text: string, quick = false): RiasecItem => ({ id, scale: 'S', text, quick });
const E = (id: string, text: string, quick = false): RiasecItem => ({ id, scale: 'E', text, quick });
const C = (id: string, text: string, quick = false): RiasecItem => ({ id, scale: 'C', text, quick });

export const RIASEC_ITEMS: RiasecItem[] = [
  // Realistic — building, fixing, tools, machines, physical, outdoors
  R('R1', 'Build or fix something with your hands', true),
  R('R2', 'Repair a bike, an engine, or a machine', true),
  R('R3', 'Work outdoors — on a farm, a site, or in nature', true),
  R('R4', 'Take a gadget apart to see how it works', true),
  R('R5', 'Train hard and compete in a physical sport', true),
  R('R6', 'Use power tools or machinery'),
  R('R7', 'Set up and wire electronics or cabling'),
  R('R8', 'Look after animals or grow plants'),
  R('R9', 'Lay tiles, bricks, or build a structure'),
  R('R10', 'Drive or operate heavy equipment'),

  // Investigative — science, research, analysis, problem-solving, ideas
  I('I1', 'Run an experiment to test an idea', true),
  I('I2', 'Solve a tricky maths or logic problem', true),
  I('I3', 'Figure out why something works the way it does', true),
  I('I4', 'Analyse data to spot patterns others miss', true),
  I('I5', 'Write code to solve a problem', true),
  I('I6', 'Research a question deeply and write up what you find'),
  I('I7', 'Work out what is wrong with a patient or a system'),
  I('I8', 'Study how the body or the brain works'),
  I('I9', 'Read about a new scientific discovery'),
  I('I10', 'Design a study to answer a question'),

  // Artistic — creative, design, expression, music, writing, visual
  A('A1', 'Design a poster, a logo, or a website', true),
  A('A2', 'Write a story, a song, or a script', true),
  A('A3', 'Draw, paint, or make digital art', true),
  A('A4', 'Play an instrument or perform on stage', true),
  A('A5', 'Come up with original ideas for a project', true),
  A('A6', 'Take and edit photos or video'),
  A('A7', 'Act in, or direct, a play or a film'),
  A('A8', 'Design the look of a room, a product, or an outfit'),
  A('A9', 'Choreograph or perform a dance routine'),
  A('A10', 'Style or decorate a space creatively'),

  // Social — helping, teaching, caring, working with people
  S('S1', 'Help someone through a difficult time', true),
  S('S2', 'Teach or coach someone a new skill', true),
  S('S3', 'Care for people who are sick or vulnerable', true),
  S('S4', 'Explain something patiently until someone gets it', true),
  S('S5', 'Volunteer for a community or charity cause', true),
  S('S6', 'Listen to a friend’s problems and give advice'),
  S('S7', 'Coach a kids’ sports team or run a youth group'),
  S('S8', 'Work with children or older people'),
  S('S9', 'Help someone learn a language or a new skill'),
  S('S10', 'Help two people settle a disagreement'),

  // Enterprising — persuading, leading, selling, business
  E('E1', 'Start and run your own business', true),
  E('E2', 'Persuade people to back your idea', true),
  E('E3', 'Lead a team or a project', true),
  E('E4', 'Pitch a product and win customers', true),
  E('E5', 'Argue a case and win people over', true),
  E('E6', 'Organise and promote an event'),
  E('E7', 'Negotiate a deal'),
  E('E8', 'Invest money and try to grow it'),
  E('E9', 'Speak in public to a big group'),
  E('E10', 'Set goals and drive a group to hit them'),

  // Conventional — organising, data, records, structure, finance, admin
  C('C1', 'Keep records or accounts accurate to the cent', true),
  C('C2', 'Organise messy information into a clear system', true),
  C('C3', 'Work with numbers, budgets, or spreadsheets', true),
  C('C4', 'Follow a precise procedure step by step', true),
  C('C5', 'Plan and track a budget', true),
  C('C6', 'Check work carefully for errors and fix them'),
  C('C7', 'Manage a schedule, files, or stock'),
  C('C8', 'Process payments or handle paperwork'),
  C('C9', 'Sort and file documents or data'),
  C('C10', 'Make sure rules and standards are followed'),
];

const V = (id: string, value: WorkValue, text: string): ValueItem => ({ id, value, text });

export const VALUE_ITEMS: ValueItem[] = [
  V('VA1', 'achievement', 'Being good at what you do and seeing real results'),
  V('VA2', 'achievement', 'Taking on challenging work that stretches you'),
  V('VI1', 'independence', 'Making your own decisions about how you work'),
  V('VI2', 'independence', 'Having freedom rather than being closely managed'),
  V('VR1', 'recognition', 'Chances to advance and earn more over time'),
  V('VR2', 'recognition', 'Being respected and recognised for your work'),
  V('VL1', 'relationships', 'Doing work that helps other people'),
  V('VL2', 'relationships', 'Working alongside people you get on with'),
  V('VS1', 'support', 'Good training and supportive managers'),
  V('VS2', 'support', 'Clear guidance and backing when you need it'),
  V('VW1', 'working-conditions', 'Job security and steady pay'),
  V('VW2', 'working-conditions', 'Good conditions and variety in the work'),
];

/** Items for a run: all 60, or the Quick 30-item subset. */
export function riasecItems(quickOnly: boolean): RiasecItem[] {
  return quickOnly ? RIASEC_ITEMS.filter((i) => i.quick) : RIASEC_ITEMS;
}
