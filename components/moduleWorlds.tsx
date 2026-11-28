/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The five module worlds, as Modules and a world's page show them (area 5 of
 * the design build; boards c-modules-pick, c-modules-world, r5-modules,
 * r5-module-world). One place for each world's words, its drawing, its ink and
 * its marks, so the door on Modules and the world's own page say the same
 * thing in the same way.
 *
 *   <WorldArt world={world} size={80} />                the world's drawing on its paint
 *   <Marks total={13} on={5} part={1} />                one mark per module (or per section)
 *   worldProgress(world.id, courses, progress)          done / partly read / total
 *
 * Colour: each world keeps its own ink for its small labels (worldPalette.ts,
 * the one home of the five palettes), passed in as --w-ink and --w-blob.
 */
import React, { type CSSProperties } from 'react';
import type { CategoryType } from './KnowledgeTree';
import type { CourseData } from './Library';
import type { UserProgress } from '../types';
import { WorldIconBlob, type WorldId } from './WorldIconBlob';
import { WORLD_TONES } from './worldPalette';
import { sectionsFor } from './learning/data';
import './module-cards.css';

export interface ModuleWorld {
  id: CategoryType;
  worldKey: WorldId;
  /** "01" */
  number: string;
  /** "Mind" */
  name: string;
  /** "The Architecture" */
  place: string;
  /** "Psychological foundations" */
  blurb: string;
  description: string;
}

/** The five worlds in the app's order (moved here from ModulesView and ModuleShowcase, words unchanged). */
export const MODULE_WORLDS: ModuleWorld[] = [
  { id: 'architecture-mindset', worldKey: 'mind', number: '01', name: 'Mind', place: 'The Architecture', blurb: 'Psychological foundations',
    description: 'Identity, beliefs, and emotional regulation — the foundation everything else stands on.' },
  { id: 'science-growth', worldKey: 'growth', number: '02', name: 'Growth', place: 'The Garden', blurb: 'How effort changes the brain',
    description: 'The neuroscience of mastery — neuroplasticity, deliberate practice, the cost and reward of struggle.' },
  { id: 'learning-cheat-codes', worldKey: 'learn', number: '03', name: 'Learn', place: 'The Cheat Codes', blurb: 'Techniques that compound',
    description: 'Active recall, spaced repetition, interleaving — the practical strategies that separate high performers.' },
  { id: 'subject-specific-science', worldKey: 'decode', number: '04', name: 'Decode', place: 'The Decoder', blurb: 'Subject by subject',
    description: 'How each exam paper actually works — marking schemes, examiner patterns, hidden curriculum.' },
  { id: 'exam-zone', worldKey: 'exam', number: '05', name: 'Exam', place: 'The Arena', blurb: 'Performance under pressure',
    description: 'Pacing, nerves, recovery — the psychology and strategy of executing on the day.' },
];

export function worldOf(id: string | null | undefined): ModuleWorld | undefined {
  return MODULE_WORLDS.find(world => world.id === id);
}

/** The world's ink (its small labels) and paint, for the active theme, as CSS variables. */
export function worldStyle(world: ModuleWorld, dark: boolean): CSSProperties {
  const tones = WORLD_TONES[world.id];
  return { ['--w-ink' as string]: dark ? tones.deepDark : tones.deep, ['--w-blob' as string]: tones.blob };
}

const sectionCount = (course: CourseData, progress: UserProgress) =>
  Math.min(course.sectionsCount, Math.max(0, progress[course.id]?.unlockedSection ?? 0));
export const isModuleDone = (course: CourseData, progress: UserProgress) =>
  course.sectionsCount > 0 && sectionCount(course, progress) >= course.sectionsCount;
export const isModuleStarted = (course: CourseData, progress: UserProgress) =>
  sectionCount(course, progress) > 0 && !isModuleDone(course, progress);

/** A world's progress: modules finished, modules partly read, and how many it has. */
export function worldProgress(id: CategoryType, courses: CourseData[], progress: UserProgress) {
  const inWorld = courses.filter(course => course.category === id);
  return {
    done: inWorld.filter(course => isModuleDone(course, progress)).length,
    part: inWorld.filter(course => isModuleStarted(course, progress)).length,
    total: inWorld.length,
  };
}

/** Where a module picks up: the step the student is on (1-based), its title, and how many steps are read. */
export function moduleResumePoint(course: CourseData, progress: UserProgress) {
  const sections = sectionsFor(course);
  const entry = progress[course.id];
  const read = sectionCount(course, progress);
  const index = Math.min(sections.length - 1, Math.max(0, entry?.reading?.lastSectionIndex ?? read));
  return { step: index + 1, steps: course.sectionsCount, title: sections[index]?.title ?? `Section ${index + 1}`, read };
}

/** One mark per module (or per step): read is ink, partly read is grey, the rest the empty track.
 *  The fill is its own element so it can draw in from the left once, on arrival. */
export function Marks({ total, on, part = 0, className = '' }: { total: number; on: number; part?: number; className?: string }) {
  return (
    <span className={`mw-marks ${className}`.trim()} aria-hidden="true">
      {Array.from({ length: Math.max(0, total) }, (_, index) => (
        <i key={index} className={index < on ? 'is-on' : index < on + part ? 'is-part' : undefined}>
          {index < on + part ? <b /> : null}
        </i>
      ))}
    </span>
  );
}

/** The world's drawing on its paint, at a real size, bare on the page (no tile). */
export function WorldArt({ world, size, className = '' }: { world: ModuleWorld; size: number; className?: string }) {
  return (
    <span className={`mw-art ${className}`.trim()} style={{ width: size, height: size }} data-world-art={world.worldKey} aria-hidden="true">
      <WorldIconBlob world={world.worldKey} size={size} />
    </span>
  );
}

/** "27 of 58 done": the readout in the mono, one baseline. */
export function Readout({ children, className = '' }: { children: React.ReactNode; className?: string }) {
  return <span className={`t-readout mw-readout ${className}`.trim()}>{children}</span>;
}
