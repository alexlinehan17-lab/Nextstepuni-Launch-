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
