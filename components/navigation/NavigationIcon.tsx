import type { SVGProps } from 'react';
import {
  IconHome2, IconHome2Filled, IconBook2, IconBookFilled, IconRoute2,
  IconStopwatch, IconCalendarWeek, IconCalendarWeekFilled, IconCalendarMonth,
  IconCalendarMonthFilled, IconStack2, IconStack2Filled, IconChartBar,
  IconMountain, IconMountainFilled, IconCompass, IconCompassFilled,
  IconRubberStamp, IconBookmark, IconBookmarkFilled, IconCoins,
  IconUser, IconBell, IconKeyboard, IconLanguage, IconMoon,
  IconLifebuoy, IconMessageCircle, IconLogout,
  IconMap2, IconFiles, IconFilesFilled, IconTarget, IconDirections, IconDirectionsFilled,
} from '@tabler/icons-react';

// Use the same professionally drawn, 24-unit family as the purchased Kobra
// controls. Keep their original geometry and optical spacing at navigation size.
const outlineIcons = {
  home: IconHome2,
  modules: IconBook2,
  paths: IconRoute2,
  timer: IconStopwatch,
  planner: IconCalendarWeek,
  yearplans: IconCalendarMonth,
  marks: IconStack2,
  atlas: IconMap2,
  papers: IconFiles,
  target: IconTarget,
  directions: IconDirections,
  progress: IconChartBar,
  island: IconMountain,
  compass: IconCompass,
  passport: IconRubberStamp,
  references: IconBookmark,
  points: IconCoins,
  account: IconUser,
  bell: IconBell,
  keyboard: IconKeyboard,
  language: IconLanguage,
  theme: IconMoon,
  help: IconLifebuoy,
  feedback: IconMessageCircle,
  logout: IconLogout,
} as const;

export type NavigationIconName = keyof typeof outlineIcons;
const filledIcons: Partial<typeof outlineIcons> = {
  home: IconHome2Filled,
  modules: IconBookFilled,
  planner: IconCalendarWeekFilled,
  yearplans: IconCalendarMonthFilled,
  marks: IconStack2Filled,
  papers: IconFilesFilled,
  directions: IconDirectionsFilled,
  island: IconMountainFilled,
  compass: IconCompassFilled,
  references: IconBookmarkFilled,
};

export function NavigationIcon({ name, active = false, ...props }: SVGProps<SVGSVGElement> & { name: NavigationIconName; active?: boolean }) {
  const Icon = active ? filledIcons[name] ?? outlineIcons[name] : outlineIcons[name];
  return <Icon size={20} stroke={1.8} aria-hidden="true" data-navigation-icon={name} data-active={active || undefined} {...props} />;
}
