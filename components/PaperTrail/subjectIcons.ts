/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Topic Atlas subject glyphs. The app's visual language uses restrained
 * Lucide line art inside soft colour fields, so these stay legible at the
 * 44px shelf size without falling back to initials or emoji.
 *
 * Junior Cycle and LCA ids are normalised to their subject name so the same
 * discipline keeps the same visual identity across programmes.
 */

import {
  Atom,
  Baby,
  BookMarked,
  BookOpen,
  BookOpenText,
  BriefcaseBusiness,
  Calculator,
  ChartNoAxesCombined,
  ClipboardList,
  Clover,
  Code2,
  Cog,
  Columns3,
  CookingPot,
  Cpu,
  Dna,
  DraftingCompass,
  Dumbbell,
  Earth,
  FlaskConical,
  Hand,
  Hammer,
  HardHat,
  HeartHandshake,
  Hotel,
  House,
  Languages,
  Landmark,
  MessageCircle,
  MessagesSquare,
  Microscope,
  MonitorCog,
  Music2,
  Palette,
  Ruler,
  Scale,
  Scissors,
  ScrollText,
  Sigma,
  Sparkles,
  Sprout,
  Store,
  TestTubes,
  Tractor,
  UsersRound,
  Waypoints,
  Wheat,
  type LucideIcon,
} from 'lucide-react';

const normaliseSubjectId = (subjectId: string) => subjectId.replace(/^(?:jc|lca)-/, '');

// Modern-language papers share the universal translation glyph. Keeping this
// culturally neutral also makes the shelf easier to scan as one language family.
const LANGUAGE_SUBJECTS = new Set([
  'arabic',
  'bulgarian',
  'croatian',
  'czech',
  'danish',
  'dutch',
  'estonian',
  'finnish',
  'french',
  'german',
  'hungarian',
  'italian',
  'japanese',
  'latvian',
  'lithuanian',
  'maltese',
  'mandarin-chinese',
  'modern-greek',
  'polish',
  'portuguese',
  'romanian',
  'russian',
  'slovakian',
  'slovenian',
  'spanish',
  'swedish',
  'ukrainian',
]);

const SUBJECT_ICONS: Record<string, LucideIcon> = {
  accounting: Calculator,
  'active-leisure-studies': Dumbbell,
  'agricultural-economics': Tractor,
  'agricultural-science': Wheat,
  'agriculture-horticulture': Sprout,
  'ancient-greek': Columns3,
  'applied-mathematics': Sigma,
  'applied-technology': Cpu,
  art: Palette,
  biology: Dna,
  business: BriefcaseBusiness,
  'business-studies': Store,
  chemistry: FlaskConical,
  'childcare-community-care': Baby,
  'classical-studies': Landmark,
  classics: Landmark,
  'computer-science': Code2,
  'construction-studies': HardHat,
  'crafts-and-design': Scissors,
  'design-and-communication-graphics': DraftingCompass,
  economics: ChartNoAxesCombined,
  engineering: Cog,
  english: BookOpenText,
  'english-and-communications': MessagesSquare,
  'gaeilge-chumarsaideach': MessageCircle,
  geography: Earth,
  'graphics-and-construction-studies': Ruler,
  'hair-and-beauty': Sparkles,
  history: ScrollText,
  'history-early-modern': ScrollText,
  'home-economics': CookingPot,
  'home-economics-s-and-s': House,
  'hotel-catering-and-tourism': Hotel,
  'information-and-communication-tech': MonitorCog,
  irish: Clover,
  'irish-t1': Clover,
  'jewish-studies': BookMarked,
  latin: Columns3,
  'link-modules': Waypoints,
  'mathematical-applications': Calculator,
  mathematics: Sigma,
  music: Music2,
  'office-admin-and-customer': ClipboardList,
  'physical-education': Dumbbell,
  physics: Atom,
  'physics-and-chemistry': TestTubes,
  'politics-and-society': Scale,
  'religious-education': HeartHandshake,
  science: Microscope,
  'sign-language': Hand,
  'social-education': UsersRound,
  technology: Cpu,
  'wood-technology': Hammer,
};

/** True when a subject has an intentional glyph rather than the safe fallback. */
export const hasAtlasSubjectIcon = (subjectId: string): boolean => {
  const id = normaliseSubjectId(subjectId);
  return LANGUAGE_SUBJECTS.has(id) || Object.hasOwn(SUBJECT_ICONS, id);
};

/** Resolve a subject to its crisp, programme-independent Atlas glyph. */
export const atlasSubjectIcon = (subjectId: string): LucideIcon => {
  const id = normaliseSubjectId(subjectId);
  if (LANGUAGE_SUBJECTS.has(id)) return Languages;
  return SUBJECT_ICONS[id] ?? BookOpen;
};

