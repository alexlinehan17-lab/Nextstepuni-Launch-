/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export type ModuleProgress = {
  unlockedSection: number;
};

export type UserProgress = {
  [moduleId: string]: ModuleProgress;
};

export interface SectionDefinition {
  id: string;
  title: string;
  eyebrow: string;
  icon: React.ComponentType<{ size?: number }>;
}

export interface ModuleTheme {
  // Highlight
  highlightBg: string;
  highlightText: string;
  highlightDecor: string;
  highlightHover: string;
  tooltipAccent: string;

  // ReadingSection
  readingIconColor: string;
  readingEyebrowBg: string;
  readingEyebrowText: string;

  // MicroCommitment
  microBg: string;
  microBorder: string;
  microIconBg: string;
  microIconShadow: string;
  microTitle: string;

  // Sidebar
  sidebarModuleText: string;
  sidebarProgressBg: string;
  sidebarProgressShadow: string;
  sidebarActiveBg: string;
  sidebarCompletedBg: string;
  sidebarCompletedBorder: string;
  sidebarActiveBorder: string;
  sidebarActiveText: string;
  sidebarActiveEyebrow: string;

  // Footer
  footerHoverBg: string;

  // ActivityRing
  activityRingColor: string;
}

export interface StudyReflection {
  dateKey: string;
  blockId: string;
  subjectName: string;
  sessionType: 'new-learning' | 'practice' | 'revision';
  reflection: string;
  pointsEarned: number;
  timestamp: number;
}

export interface PointsData {
  totalEarned: number;
  totalSpent: number;
}

export interface PointsTransaction {
  type: 'skip-session' | 'rest-day-pass' | 'unlock-avatar' | 'unlock-theme';
  cost: number;
  dateKey: string;
  detail?: string;
  timestamp: number;
}

export interface CosmeticUnlocks {
  avatarSeeds: string[];
  themeColors: string[];
}

export interface EarnedRest {
  skippedSessions: string[];
  restDayPasses: string[];
}

export interface UserSettings {
  language: string;
  avatar: string;
  darkMode: boolean;

  defaultWorkMinutes: number;
}

export type NorthStarCategory =
  | 'independence' | 'family-community' | 'career-craft'
  | 'college-learning' | 'prove-myself' | 'options-freedom';

export interface NorthStarVisionCard {
  id: string;
  label: string;
  icon: string;
  category: NorthStarCategory;
}

export interface NorthStar {
  category: NorthStarCategory;
  statement: string;
  visionBoard: string[];
  createdAt: string;
  updatedAt: string;
}
