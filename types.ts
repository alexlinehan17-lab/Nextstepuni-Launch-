/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export type AccentThemeId = 'terracotta' | 'ocean' | 'sage' | 'midnight' | 'dusk-rose' | 'golden' | 'arctic' | 'obsidian';
export type CardStyleId = 'default' | 'glass' | 'neon' | 'flat' | 'gradient';

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

export interface CosmeticUnlocks {
  avatarSeeds: string[];
  themeColors: string[];
  cardStyles: string[];
}

export interface EarnedRest {
  skippedSessions: string[];
  restDayPasses: string[];
}

export interface UserSettings {
  language: string;
  avatar: string;
  darkMode: boolean;
  accentTheme: AccentThemeId;
  cardStyle: CardStyleId;
  defaultWorkMinutes: number;
  flaresToggle?: boolean;
  showDashboard?: boolean;
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

export interface JourneyProgress {
  unlockedMilestones: number;  // 0-12
  totalSpent: number;
  lastUnlockTimestamp: string;
}

export type ShopItemCategory = 'terrain' | 'building' | 'path' | 'nature' | 'furniture' | 'vehicle' | 'atmosphere';

export interface ShopItem {
  id: string;
  name: string;
  description: string;
  model: string;
  category: ShopItemCategory;
  type: 'hex' | 'decoration';
  price: number;
  exclusiveTo?: NorthStarCategory;
  defaultScale?: number;
}

export interface IslandPlacement {
  itemId: string;
  model: string;
  type: 'hex' | 'decoration';
  q: number;
  r: number;
  rotation?: number;
  scale?: number;
  offsetX?: number;
  offsetZ?: number;
  purchasedAt: string;
  isStarter?: boolean;
}

export interface IslandState {
  category: NorthStarCategory;
  placements: IslandPlacement[];
  totalSpent: number;
  purchaseHistory: string[];
  lastPurchaseTimestamp: string;
  claimedRewards?: string[];
}

// ── Strategy Mastery ──────────────────────────────────────

export type MasteryTier = 'none' | 'learned' | 'practiced' | 'applied' | 'habitual';

export interface StrategyMasteryRecord {
  tier: MasteryTier;
  learnedAt?: string;
  appliedAt?: string;
  habitualAt?: string;
  sessionCount: number;
  subjectsSeen: string[];
}

export type StrategyMasteryMap = Record<string, StrategyMasteryRecord>;

// ── Unified Topic Mastery ────────────────────────────────────
export type UnifiedConfidence = 'not-started' | 'shaky' | 'solid';

export interface TopicMasteryEntry {
  confidence: UnifiedConfidence;
  updatedAt: number;
  source: 'manual' | 'debrief' | 'import';
  lastDebriefDate?: string;
  sm2Quality?: number;
}

export type SubjectTopicMastery = Record<string, TopicMasteryEntry>;
export type TopicMasteryMap = Record<string, SubjectTopicMastery>;

// ── Unified Mock Results ─────────────────────────────────────
export interface UnifiedMockResult {
  id: string;
  label: string;
  date: string;
  entries: { subjectName: string; grade: string; level: string }[];
  totalPoints: number;
  timestamp: number;
}
