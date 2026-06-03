/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Shared deck glyphs — the icon/colour identity for the immersive card decks,
 * centralised so Career Paths + Your Possible Life agree (and How They Did It
 * can reuse the palette). Replaces the old emoji glyphs with clean Lucide line
 * icons (careers) and initials (people), per the 2026-06-03 hybrid redesign.
 */
import {
  Stethoscope, PawPrint, Code2, Cog, Scale, Brain, BarChart3, GraduationCap,
  Ruler, FlaskConical, Wrench, Palette, type LucideIcon,
} from 'lucide-react';
import { type CareerField } from '../../types/careerPaths';
import { WORLDS, type ColorWorld } from './colorWorlds';

/** Each career field owns a colour world. */
export const FIELD_WORLD: Record<CareerField, ColorWorld> = {
  health: WORLDS.teal,
  animals: WORLDS.forest,
  tech: WORLDS.ocean,
  engineering: WORLDS.slate,
  law: WORLDS.indigo,
  psychology: WORLDS.rose,
  business: WORLDS.denim,
  education: WORLDS.terracotta,
  design: WORLDS.rust,
  science: WORLDS.pine,
  trades: WORLDS.cocoa,
  creative: WORLDS.claret,
};

/** Each career field owns a clean line icon (rendered white on the colour band). */
export const FIELD_ICON: Record<CareerField, LucideIcon> = {
  health: Stethoscope,
  animals: PawPrint,
  tech: Code2,
  engineering: Cog,
  law: Scale,
  psychology: Brain,
  business: BarChart3,
  education: GraduationCap,
  design: Ruler,
  science: FlaskConical,
  trades: Wrench,
  creative: Palette,
};

/** First-letter initials from a person's name, e.g. "Kellie Harrington" → "KH". */
export function initials(name: string): string {
  const parts = name.trim().split(/\s+/).filter(Boolean);
  if (parts.length === 0) return '?';
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}
