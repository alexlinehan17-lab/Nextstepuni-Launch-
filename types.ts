/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export type CardStyleId = 'default' | 'glass' | 'neon' | 'flat' | 'gradient';

export type ModuleProgress = {
  unlockedSection: number;
};

/** The five-point confidence scale captured after a study session. */
export type StudyConfidenceLabel = 'lost' | 'shaky' | 'okay' | 'good' | 'confident';

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
  /** Structured analytics fields. Optional so historic reflections still load. */
  confidenceAfter?: number;
  confidenceLabel?: StudyConfidenceLabel;
  reflectionMode?: 'quick' | 'full';
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
  /** Reading comfort: multiplier on module reading text (0.9–1.2, default 1). */
  readingScale?: number;
  /** Reading comfort: 'relaxed' opens up line spacing in module reading text. */
  readingSpacing?: 'normal' | 'relaxed';
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
  /** True only when the student supplied the wording themselves. Legacy
   * statements are preserved, but category copy is never presented as a
   * student-authored quotation. */
  authoredByStudent?: boolean;
  reviewedAt?: string;
}

export type DirectionItemState = 'curious' | 'exploring' | 'serious-option' | 'current-target' | 'not-for-me' | 'achieved';

export interface DirectionVisionItem {
  id: string;
  source: 'onboarding' | 'future-finder' | 'exploring-options' | 'student';
  state: DirectionItemState;
  addedAt: string;
  updatedAt: string;
}

export interface DirectionProfile {
  version: 2;
  northStar: NorthStar;
  visionItems: DirectionVisionItem[];
  reviewedAt: string;
}

export interface JourneyProgress {
  unlockedMilestones: number;  // 0-12
  totalSpent: number;
  lastUnlockTimestamp: string;
}

export type ShopItemCategory = 'terrain' | 'building' | 'path' | 'nature' | 'furniture' | 'vehicle' | 'atmosphere';
export type IslandPlacementLayer = 'terrain' | 'structure' | 'decoration';
export type IslandTerrainKind = 'grass' | 'dirt' | 'sand' | 'stone' | 'hill' | 'mountain' | 'path' | 'water' | 'unknown';

export interface PlacementRules {
  layer: IslandPlacementLayer;
  allowedTerrain?: IslandTerrainKind[];
  blockedTerrain?: IslandTerrainKind[];
  preferredTerrain?: IslandTerrainKind[];
  maximumPerTile?: number;
  requiresAdjacentTerrain?: IslandTerrainKind[];
  /** Requires at least one neighbouring water/frontier edge. */
  requiresCoast?: boolean;
  /** Keeps large landmarks from being visually boxed in. */
  minimumOpenNeighbours?: number;
}

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
  placementRules?: PlacementRules;
}

export interface IslandPlacement {
  /** Stable identity used by Build Mode for move, rotate and put-away operations. */
  placementId?: string;
  itemId: string;
  model: string;
  type: 'hex' | 'decoration';
  /** Explicit render/placement layer. Optional only for legacy stored islands. */
  layer?: IslandPlacementLayer;
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

export type IslandItemSource = 'purchase' | 'milestone' | 'gift' | 'stored';

export interface IslandInventoryItem {
  inventoryId: string;
  itemId: string;
  source: IslandItemSource;
  acquiredAt: string;
  giftId?: string;
}

export interface IslandState {
  /** Schema 2 introduces stable placement IDs and explicit placement layers. */
  schemaVersion?: number;
  category: NorthStarCategory;
  placements: IslandPlacement[];
  totalSpent: number;
  purchaseHistory: string[];
  lastPurchaseTimestamp: string;
  claimedRewards?: string[];
  /** Owned objects waiting to be positioned in Build Mode. */
  inventory?: IslandInventoryItem[];
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

/**
 * Stable curriculum-keyed mastery. `topicMastery` remains the backwards-
 * compatible display-name projection while consumers move to this schema.
 */
export interface CanonicalTopicMasteryEntry extends TopicMasteryEntry {
  subjectId: string;
  subjectName: string;
  specificationId: string;
  topicId: string;
  topicName: string;
}

export interface TopicMasteryV2 {
  schemaVersion: 2;
  /** Keyed by `${specificationId}::${topicId}`. */
  topics: Record<string, CanonicalTopicMasteryEntry>;
  /** Legacy/custom records which cannot be mapped without guessing. */
  unresolved: TopicMasteryMap;
}

// ── Unified Mock Results ─────────────────────────────────────
export interface UnifiedMockResult {
  id: string;
  label: string;
  date: string;
  entries: { subjectName: string; grade: string; level: string }[];
  totalPoints: number;
  timestamp: number;
}

// ── College Compass ──────────────────────────────────────────
// Per-user state for the College Compass tool. Lives namespaced under the
// `collegeCompass` field on the shared progress/{uid} doc. Store ONLY
// IDs/codes/booleans — content (stops, dates, labels) is rehydrated from
// collegeCompassData.ts at render time.
export interface CollegeCompassState {
  /**
   * checklistItem id ("<stopId>:<itemId>") -> 'in-progress' | 'done'.
   * Absent key = not started. Live mode (6th) only. Legacy docs stored the
   * boolean `true` for done; useCollegeCompass normalises that to 'done' on read.
   */
  checklist: Record<string, 'in-progress' | 'done'>;
  /** Optional: institution codes for the "set my target colleges" picker. */
  targetInstitutionCodes?: string[];
  /** Optional: last-used HEAR meter indicator selection (ids only). */
  hearIndicators?: string[];
  /** Optional: last-used DARE category id. */
  dareCategoryId?: string;
  /** Stops the student has hidden (e.g. DARE if not applicable). */
  dismissedStops?: string[];
  updatedAt: string; // ISO timestamp
}
