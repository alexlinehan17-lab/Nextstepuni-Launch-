import type { SVGProps } from 'react';
import {
  House, BookOpen, Route, Timer, Calendar, CalendarRange, Layers, Map as MapIcon, FileText,
  Target, Signpost, ChartNoAxesColumn, Mountain, Compass, Stamp, BookMarked, SlidersHorizontal,
  Coins, User, Bell, Keyboard, Languages, Moon, CircleHelp, MessageSquare, LogOut, Lightbulb, Star,
  PanelLeft, ChevronsUpDown,
} from 'lucide-react';

// Sidebar B (agreed 25 Nov 2026) uses the app's one icon set: lucide outline
// glyphs, 20px at 1.75px. The current place is not a filled icon: it is ink
// on a shaded row (navigation.md; components.md, "Icons").
const outlineIcons = {
  home: House,
  modules: BookOpen,
  paths: Route,
  timer: Timer,
  planner: Calendar,
  yearplans: CalendarRange,
  marks: Layers,
  atlas: MapIcon,
  papers: FileText,
  target: Target,
  directions: Signpost,
  progress: ChartNoAxesColumn,
  island: Mountain,
  compass: Compass,
  passport: Stamp,
  references: BookMarked,
  setup: SlidersHorizontal,
  points: Coins,
  account: User,
  bell: Bell,
  keyboard: Keyboard,
  language: Languages,
  theme: Moon,
  help: CircleHelp,
  feedback: MessageSquare,
  logout: LogOut,
  insights: Lightbulb,
  direction: Star,
  panel: PanelLeft,
  updown: ChevronsUpDown,
} as const;

export type NavigationIconName = keyof typeof outlineIcons;

export function NavigationIcon({ name, active = false, size = 20, ...props }: Omit<SVGProps<SVGSVGElement>, 'ref'> & { name: NavigationIconName; active?: boolean; size?: number }) {
  const Icon = outlineIcons[name];
  return <Icon width={size} height={size} strokeWidth={1.75} aria-hidden="true" focusable="false" data-navigation-icon={name} data-active={active || undefined} {...props} />;
}
