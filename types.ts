/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

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
  cardStyle: CardStyleId;
  defaultWorkMinutes: number;
  showDashboard?: boolean;
  essentialsMode?: boolean;
}

export type NorthStarCategory =
  // Senior cycle (6)
  | 'independence' | 'family-community' | 'career-craft'
  | 'college-learning' | 'prove-myself' | 'options-freedom'
  // Junior cycle (4) — Phase 5
  | 'family-people' | 'prove-myself-jc' | 'curiosity-craft' | 'future-doors';

export interface NorthStarVisionCard {
  id: string;
  label: string;
  icon: string;
  category: NorthStarCategory;
  /** Phase 5: which curriculum level(s) can see this card. Default 'senior'
   *  for any existing card without the field. */
  curriculum?: 'junior' | 'senior' | 'both';
}

// ─── Past JC archive (Phase 8) ──────────────────────────────────────────
//
// When a 3rd-year JC user transitions into senior cycle (TY or 5th), their
// JC band data and JC North Star are moved out of the active subjectProfile
// /northStar fields and parked on users/{uid}.pastJCData. The active
// profile is then cleared so the senior re-onboarding picks fresh LC
// subjects / grades / NS without legacy data leaking through.
//
// Nothing in Phase 8 surfaces this archive in the UI — it's stored for
// potential future "Your JC journey" features and as a manual rollback
// path for GC/admin if a student transitions by mistake.
import type { StudentSubject } from './components/subjectData';

export interface PastJCData {
  transitionedAt: string;       // ISO timestamp of the transition
  jcYearGroup: '3rd';            // always 3rd at time of transition
  jcSubjects: StudentSubject[]; // JC subjects with currentBand/targetBand intact
  jcNorthStar?: NorthStar;       // their JC NS at time of transition (may be unset)
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
  // Optional: present on the owner's own placements (used for the
  // "newly purchased" animation in HexIsland.tsx). Absent on placements
  // loaded from /islandPublic/{uid} for peer view, by design.
  purchasedAt?: string;
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
