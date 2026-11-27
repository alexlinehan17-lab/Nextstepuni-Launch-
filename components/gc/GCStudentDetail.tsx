/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * One student, as their counsellor sees them (area 8a): a page of its own with Back on a phone,
 * the side tray with Close on a laptop (the dashboard wraps it in the shared OverScreen). The
 * student's character, name and status at the top; their warnings as notices; the figures as
 * ruled rows; every section of today's profile below, laid on the page between hairlines; the
 * three actions pinned at the bottom on a phone and under the student on a laptop. How things
 * are SHOWN only: every read, write, callable and preset id is as it was.
 */
import React, { useState, useEffect, useRef, type ReactNode } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { Check, CheckCircle, MinusCircle, MoreHorizontal } from 'lucide-react';
import { type CourseData } from '../Library';
import { type CategoryType } from '../KnowledgeTree';
import { getPointsForGrade, LC_SUBJECTS } from '../subjectData';
import { ARCHETYPES, CAPABILITY_KEYS, JOURNEY_SCORING_VERSION, STAT_LABELS, type CapabilityKey } from '../journeySimulatorData';
import { NORTH_STAR_CATEGORIES, VISION_CARDS } from '../../northStarData';
import { type GCStudentFullData, type StudentStatus } from './gcTypes';
import { hydrateCourses } from '../futureFinderData';
import { computeCompassProgress } from '../../collegeCompassData';
import { type EarlyWarningAlert } from './gcAlerts';
import {
  getOverallProgress,
  getCategoryProgress,
  getStudentCurrentCAO,
  getStudentTargetCAO,
  getDaysUntilLC,
  getStudentStatus,
  getEngagementTimeline,
  getVisibleCourses,
  hasCAOGrades,
  getStudentSubjectsCovered,
  getStudentTopBandsCount,
  getStudentTargetTopBandsCount,
} from './gcUtils';
import { getStatusReasons } from '../../utils/studentStatus';
import { type FlagData, type FlagPriority } from '../../hooks/useGCFlags';
import { type SessionUser } from '../../utils/authUtils';
import { PentagonRadar } from './PentagonRadar';
import { getFunctions, httpsCallable } from 'firebase/functions';
import app from '../../firebase';
import { logError } from '../../utils/logError';
import {
  STAFF_ENCOURAGEMENT,
  STAFF_RECOMMENDATION_NOTES,
  isKnownStaffMessage,
} from '../../data/staffEncouragement';
import SubjectAvatar from '../SubjectAvatar';
import { TopBar, PinnedFooter } from '../ui/Bars';
import { MenuAction, MenuPanel, MenuRadioRows } from '../ui/Menu';
import { Sheet } from '../ui/Sheet';
import { ChoiceTile } from '../ui/Choice';
import { Button, TextButton } from '../ui/Button';
import { List, Row } from '../ui/List';
import { StudentArt, StatusWords, Fig, Pct, STATUS_WORDS, SEVERITY_WORDS } from './gcView';

const CUSTOM_EASE = [0.16, 1, 0.3, 1] as const;

// ─── Categories ─────────────────────────────────────────────────────────────

const CATEGORIES: { id: CategoryType; title: string }[] = [
  { id: 'architecture-mindset', title: 'The Architecture of your Mindset' },
  { id: 'science-growth', title: 'The Science of Growth' },
  { id: 'learning-cheat-codes', title: 'The Science of Learning Effectively' },
  { id: 'subject-specific-science', title: 'Decoding the Subjects' },
  { id: 'exam-zone', title: 'Exam Strategy and Points Maximisation' },
];

// ─── Component ──────────────────────────────────────────────────────────────

interface GCFlagsAPI {
  flags: Record<string, FlagData>;
  flagStudent: (uid: string, priority?: FlagPriority) => Promise<void>;
  unflagStudent: (uid: string) => Promise<void>;
  updateFlagPriority: (uid: string, priority: FlagPriority) => Promise<void>;
  isFlagged: (uid: string) => boolean;
  getFlagData: (uid: string) => FlagData | null;
  flaggedStudentUids: string[];
}

interface GCStudentDetailProps {
  student: GCStudentFullData;
  allCourses: CourseData[];
  onBack: () => void;
  school?: string;
  isTrayMode?: boolean;
  alerts?: EarlyWarningAlert[];
  gcFlags?: GCFlagsAPI;
  /** The laptop's side tray (Close, actions under the student); a phone's page when false or left out. */
  wide?: boolean;
  onDismissAlert?: (alert: EarlyWarningAlert) => void;
  onResetPassword?: (studentUid: string) => void;
  onDeleteStudent?: (user: SessionUser) => void;
}

// Recommendable IZ tools, tagged by curriculum so the recommend-tool modal
// can hide senior-only tools when the recommended student is JC. 'both' =
// tool works for both curricula (Spaced Rep Timetable, Comeback Engine,
// Future Finder/Subject Explorer per Phase 2 builds).
const INNOVATION_TOOLS: { id: string; title: string; jcTitle?: string; curriculum: 'junior' | 'senior' | 'both' }[] = [
  { id: 'journey',          title: 'Academic Journey Simulator', curriculum: 'senior' },
  { id: 'cao-simulator',    title: 'Points Passport · Grade Planner', curriculum: 'senior' },
  { id: 'flashcards',       title: 'Flashcard Studio',           curriculum: 'both' },
  { id: 'planner',          title: 'Planner & Study', curriculum: 'both' },
  { id: 'war-room',         title: 'War Room',                   curriculum: 'senior' },
  { id: 'comeback',         title: 'Comeback Engine',            curriculum: 'both' },
  { id: 'future-finder',    title: 'Future Finder', jcTitle: 'Subject Explorer', curriculum: 'both' },
  { id: 'learning-dna',     title: 'Learning DNA',               curriculum: 'both' },
  { id: 'first-gen-intel',  title: 'First Gen Intel',            curriculum: 'senior' },
];

/** A section's small label (the group it opens) over its heading, and a quiet figure at the right. */
function SecHead({ title, over, end }: { title: ReactNode; over?: string; end?: ReactNode }) {
  return (
    <div className="gc8-sechead">
      <div className="gc8-sechead-col">
        {over ? <p className="gc8-label">{over}</p> : null}
        <h3 className="gc8-h">{title}</h3>
      </div>
      {end ? <span className="gc8-meta">{end}</span> : null}
    </div>
  );
}

export const GCStudentDetail: React.FC<GCStudentDetailProps> = ({ student, allCourses, onBack, isTrayMode, alerts = [], gcFlags, wide = false, onDismissAlert, onResetPassword, onDeleteStudent }) => {
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set());
  const [openStops, setOpenStops] = useState<Set<string>>(new Set());
  const [showRecommendModal, setShowRecommendModal] = useState(false);
  const [showKudosModal, setShowKudosModal] = useState(false);
  const [recommendToolId, setRecommendToolId] = useState<string | null>(null);
  // Preset ids, never prose: staff cannot send free text to a student.
  // See data/staffEncouragement.ts (owner decision 2026-08-17).
  const [recommendNoteId, setRecommendNoteId] = useState('');
  const [kudosMessageId, setKudosMessageId] = useState('');
  const [isSendingAction, setIsSendingAction] = useState(false);
  const recommendToolsRef = useRef<HTMLDivElement>(null);
  const kudosMessagesRef = useRef<HTMLDivElement>(null);

  // Score the student against the modules THEY can open, not the full
  // catalogue — a 7-subject senior who had finished everything available to
  // them was being shown to their counsellor as ~73% complete, and a JC
  // student as ~20%. `visibleCourses` is the same list the student's own
  // progress counter uses (utils/courseVisibility).
  const visibleCourses = getVisibleCourses(student, allCourses);
  const overallProgress = getOverallProgress(student.progress, visibleCourses);
  const hasGrades = hasCAOGrades(student);
  const currentCAO = getStudentCurrentCAO(student);
  const targetCAO = getStudentTargetCAO(student);
  const daysUntilLC = getDaysUntilLC();
  const status = getStudentStatus(student, visibleCourses);
  const statusReasons = getStatusReasons(student, visibleCourses);
  const supportReasons = statusReasons;

  // ─── Curriculum branch (Phase 6) ────────────────────────────────────────
  // For JC students we hide CAO-based sections (CAO Current/Target cards,
  // CAO bar, points-gain column, CAO Simulator recommendations) and surface
  // the band-based subject profile instead. The student.curriculumLevel is
  // populated by Phase 1 plumbing; we fall back to deriving from yearGroup.
  const isJunior = student.curriculumLevel === 'junior'
    || (student.yearGroup === '1st' || student.yearGroup === '2nd' || student.yearGroup === '3rd');
  // Phase 8: graduated students should show a muted "Graduated" badge
  // and have the days-to-LC tile suppressed (the countdown is meaningless
  // post-LC).
  const isGraduated = student.yearGroup === 'graduated';

  // ─── Status transition tracking (localStorage, GC-only) ──────────────
  const [previousStatus, setPreviousStatus] = useState<StudentStatus | null>(null);

  useEffect(() => {
    const key = `gc-status-${student.user.uid}`;
    try {
      const raw = localStorage.getItem(key);
      if (raw) {
        const data = JSON.parse(raw) as { status: StudentStatus; at: number };
        const daysSince = (Date.now() - data.at) / 86400000;
        if (data.status !== status && daysSince <= 7) {
          setPreviousStatus(data.status);
        } else {
          setPreviousStatus(null);
        }
      }
      // Save current status
      localStorage.setItem(key, JSON.stringify({ status, at: Date.now() }));
    } catch (err) {
      console.error('Failed to read previous status:', err);
      setPreviousStatus(null);
    }
  }, [student.user.uid, status]);

  const flagData = gcFlags?.getFlagData(student.user.uid);
  const name = student.user.name;

  // ─── The student: their year (and cycle, where the year does not say it) and flag ───
  //
  // Today's year/curriculum badge and flag bar, said in one small line over the name.
  const yearLabel = (() => {
    if (isGraduated) return 'Graduated';
    const yg = student.yearGroup;
    const cycle = isJunior ? 'Junior Cycle' : 'Senior Cycle';
    if (!yg) return student.curriculumLevel ? cycle : null;
    const year = yg === 'TY' || yg.startsWith('LCA') ? yg : `${yg} Year`;
    const yearSaysJunior = yg === '1st' || yg === '2nd' || yg === '3rd' ? true : yg === 'TY' ? null : false;
    return yearSaysJunior === isJunior ? year : `${cycle} · ${year}`;
  })();
  const flagLabel = flagData ? (flagData.priority === 'high' ? 'Flagged, high' : 'Flagged') : null;
  const whoLabel = [yearLabel, flagLabel].filter(Boolean).join(' · ');
  const statusMore = [
    previousStatus ? `Was ${STATUS_WORDS[previousStatus].toLowerCase()}` : null,
    student.streak?.lastActiveDate ? `Last active ${student.streak.lastActiveDate}` : null,
  ].filter(Boolean);

  const renderStudent = () => (
    <div className="gc8-sd-head">
      <div className="gc8-sd-who">
        <StudentArt seed={student.user.avatar} size={56} />
        <div className="gc8-sd-whocopy">
          {whoLabel ? <p className="gc8-label">{whoLabel}</p> : null}
          <h2 className="gc8-name">{name}</h2>
        </div>
      </div>
      <p className="gc8-sub">
        <StatusWords status={status}>{statusMore.length ? `. ${statusMore.join('. ')}.` : '.'}</StatusWords>
      </p>
    </div>
  );

  // ─── Notices: each early warning, and the reasons this student needs support ───

  const renderNotices = () => {
    // Needs Support (at-risk / drifting). Audit 2026-06-01: previously compared
    // to 'needs-support', which is not in the StudentStatus union, so this
    // tray panel never rendered.
    const needsSupport = (status === 'at-risk' || status === 'drifting') && supportReasons.length > 0;
    if (alerts.length === 0 && !needsSupport) return null;
    return (
      <div className="gc8-sd-notices">
        {alerts.map(alert => (
          <div key={alert.id} className="gc8-sd-notice">
            <p className="gc8-label">Early warning · {SEVERITY_WORDS[alert.severity]}</p>
            <p className="gc8-sub"><span className="gc8-strong">{alert.title}.</span> {alert.description}</p>
            {onDismissAlert ? <TextButton tone="quiet" onClick={() => onDismissAlert(alert)}>Dismiss warning</TextButton> : null}
          </div>
        ))}
        {needsSupport && (
          <div className="gc8-sd-notice">
            <p className="gc8-label">Needs support</p>
            <ul>
              {supportReasons.map((reason, i) => (
                <li key={i} className="gc8-sub">{reason}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  };

  // ─── Figures (shared by the phone and the laptop) ────────────────────
  //
  // These used to be duplicated: the full-page copy was curriculum-guarded and
  // the tray copy was not. Since GCDashboard only ever renders the TRAY, the
  // guard was dead code — every Junior Cycle student was shown "Current CAO 0 /
  // Target CAO 0" and an LC countdown, and every LCA student fell through to the
  // CAO path too (LCA maps to 'senior'). One renderer, so the guard can't drift
  // out of the branch that's actually on screen again.
  const renderFigures = () => (
    <div className="gc8-figrows">
      <div>
        <span className="gc8-sub">Progress</span>
        <Fig className="gc8-num" value={overallProgress.toFixed(0)} unit="%" />
      </div>

      {/* Junior Cycle: bands, not points. */}
      {isJunior ? (() => {
        const subjectsCovered = getStudentSubjectsCovered(student);
        const atMerit = getStudentTopBandsCount(student);
        const targetMerit = getStudentTargetTopBandsCount(student);
        return (
          <>
            <div>
              <span className="gc8-sub">Subjects</span>
              <span className="gc8-num">{subjectsCovered || '—'}</span>
            </div>
            <div>
              <span className="gc8-figrows-col">
                <span className="gc8-sub">At Merit+</span>
                <span className="gc8-meta">Target Merit+ {subjectsCovered ? `${targetMerit}/${subjectsCovered}` : '—'}</span>
              </span>
              <span className="gc8-num">{subjectsCovered ? `${atMerit}/${subjectsCovered}` : '—'}</span>
            </div>
          </>
        );
      })() : (
        <>
          {/* hasCAOGrades, not "has a profile": an LCA profile is complete and
              valid but has no H/O grade anywhere, so the CAO total is not 0 —
              it doesn't exist. An em-dash says that; a 0 lies about it. */}
          <div>
            <span className="gc8-figrows-col">
              <span className="gc8-sub">CAO points</span>
              <span className="gc8-meta">
                Target {hasGrades ? targetCAO : '—'}{hasGrades && targetCAO > currentCAO ? `, ${targetCAO - currentCAO} to go` : ''}
              </span>
            </span>
            <span className="gc8-num">{hasGrades ? currentCAO : '—'}</span>
          </div>
          {isGraduated ? (
            <div>
              <span className="gc8-sub">Past cohort</span>
              <span className="gc8-sub">Best of luck</span>
            </div>
          ) : (
            <div>
              <span className="gc8-sub">Days to exam</span>
              <span className="gc8-num">{daysUntilLC}</span>
            </div>
          )}
        </>
      )}
    </div>
  );

  const toggleCategory = (id: string) => {
    setExpandedCategories(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  };

  const toggleStop = (id: string) => {
    setOpenStops(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  };

  // ─── Engagement timeline ──────────────────────────────────────────────

  const engagementTimeline = getEngagementTimeline(student.timetableCompletions);
  const maxBlocks = Math.max(1, ...engagementTimeline.map(d => d.count));
  const totalBlocks = engagementTimeline.reduce((sum, d) => sum + d.count, 0);
  const activeDays = engagementTimeline.filter(d => d.count > 0).length;

  // ─── Subject profile ────────────────────────────────────────────────

  const renderSubjectProfile = () => {
    if (!student.subjectProfile) {
      return (
        <section className="gc8-sec gc8-sd-sec">
          <SecHead over="Academic profile" title="Subject profile" />
          <p className="gc8-sub">No subject profile set up yet.</p>
        </section>
      );
    }

    const maxPoints = 625;
    const currentPct = Math.min(100, (currentCAO / maxPoints) * 100);
    const targetPct = Math.min(100, (targetCAO / maxPoints) * 100);

    return (
      <section className="gc8-sec gc8-sd-sec">
        <SecHead over="Academic profile" title="Subject profile" />

        {/* CAO bar — senior only (JC has no points concept), and only for
            students who actually have H/O grades. LCA students map to
            'senior' but are assessed on credits, so this bar used to draw a
            confident 0-of-625 for them. For JC the band-by-band breakdown in
            the rows below carries the same information without a single
            "total" number to anchor to. */}
        {!isJunior && hasGrades && (
          <div className="gc8-sd-cao">
            <div className="gc8-sd-ends gc8-meta">
              <span>Current: {currentCAO} pts</span>
              <span>Target: {targetCAO} pts</span>
            </div>
            <span className="gc8-bar gc8-sd-caobar" aria-hidden="true">
              <i style={{ width: `${currentPct}%` }} />
              {targetPct > currentPct && (
                <b style={{ left: `${currentPct}%`, width: `${targetPct - currentPct}%` }} />
              )}
            </span>
            <div className="gc8-sd-ends gc8-meta">
              <span>0</span>
              <span>625</span>
            </div>
          </div>
        )}

        {/* Each subject — Phase 6 makes the last figure curriculum-aware.
            Senior: HL/OL · current grade · target grade · Pts gain.
            Junior: Common (or HL/OL for English/Irish/Maths) · current
            band · target band · Bands gained. The level is shown for both
            but defaults to "Common" for JC subjects without a level choice. */}
        <div className="gc8-sd-subjects">
          {student.subjectProfile.subjects.map(sub => {
            // Senior path
            const isMaths = LC_SUBJECTS.find(lc => lc.name === sub.subjectName)?.isMaths ?? false;
            const currentPts = sub.currentGrade ? getPointsForGrade(sub.currentGrade, isMaths) : 0;
            const targetPts = sub.targetGrade ? getPointsForGrade(sub.targetGrade, isMaths) : 0;
            const gain = targetPts - currentPts;
            // JC path
            const jcBands = ['Distinction', 'Higher Merit', 'Merit', 'Achieved', 'Partially Achieved', 'Not Graded'];
            const currentBandIdx = sub.currentBand ? jcBands.indexOf(sub.currentBand) : -1;
            const targetBandIdx = sub.targetBand ? jcBands.indexOf(sub.targetBand) : -1;
            // Bands-gained = how many bands lower the target is from current
            // (positive = improvement, since lower index = better band)
            const bandsGained = (currentBandIdx >= 0 && targetBandIdx >= 0)
              ? currentBandIdx - targetBandIdx
              : 0;
            const levelLabel = sub.level === 'higher' ? 'HL' : sub.level === 'ordinary' ? 'OL' : 'Common';
            const now = isJunior ? (sub.currentBand ?? '—') : (sub.currentGrade ?? '—');
            const target = isJunior ? (sub.targetBand ?? '—') : (sub.targetGrade ?? '—');
            const gainWords = isJunior
              ? `Bands gained ${bandsGained > 0 ? `+${bandsGained}` : bandsGained}`
              : `Pts gain ${gain > 0 ? `+${gain}` : gain === 0 ? '0' : gain}`;
            // The thin bar: how far the current grade (band) is toward the target, drawn only
            // when both are set. The words beside it say the grades themselves.
            const lastBand = jcBands.length - 1;
            const share = isJunior
              ? (currentBandIdx >= 0 && targetBandIdx >= 0 ? Math.min(1, (lastBand - currentBandIdx) / Math.max(1, lastBand - targetBandIdx)) : null)
              : (sub.currentGrade && sub.targetGrade ? (targetPts > 0 ? Math.min(1, currentPts / targetPts) : 1) : null);
            return (
              <div key={sub.subjectName} className="gc8-sd-subject">
                <SubjectAvatar bare subject={sub.subjectName} className="gc8-art gc8-art--32" />
                <div className="gc8-sd-subject-copy">
                  <div className="gc8-who">
                    <span className="gc8-person">{sub.subjectName}</span>
                    <span className="gc8-meta">{now} now · {target} target</span>
                  </div>
                  {share !== null && (
                    <span className="gc8-bar gc8-bar--thin" aria-hidden="true"><i style={{ width: `${share * 100}%` }} /></span>
                  )}
                  <span className="gc8-meta">{levelLabel} · {gainWords}</span>
                </div>
              </div>
            );
          })}
        </div>
      </section>
    );
  };

  // ─── North Star ─────────────────────────────────────────────────────

  const renderNorthStar = () => {
    if (!student.northStar) {
      return (
        <section className="gc8-sec gc8-sd-sec">
          <SecHead title="North Star" />
          <p className="gc8-sub">Not set yet.</p>
        </section>
      );
    }

    const ns = student.northStar;
    const catOption = NORTH_STAR_CATEGORIES.find(c => c.id === ns.category);
    const visionItems = ns.visionBoard
      .map(id => VISION_CARDS.find(v => v.id === id))
      .filter(Boolean);

    return (
      <section className="gc8-sec gc8-sd-sec">
        <SecHead title="North Star" />
        {catOption && <p className="gc8-label">{catOption.label}</p>}
        {ns.statement && (
          <p className="gc8-sub gc8-strong">&ldquo;{ns.statement}&rdquo;</p>
        )}
        {visionItems.length > 0 && (
          <p className="gc8-meta">{visionItems.map(v => v!.label).join(' · ')}</p>
        )}
      </section>
    );
  };

  // ─── Module progress (rows that open in place, thin ink bars) ────────

  const renderModuleProgress = () => (
    <section className="gc8-sec gc8-sd-sec">
      <SecHead over="Learning progress" title="Module progress" />
      <List>
        {CATEGORIES.map(cat => {
          // visibleCourses, not allCourses — the per-subject Decode modules
          // for subjects this student doesn't take were being listed as
          // "Not Started" work they had never been offered.
          const catCourses = visibleCourses.filter(c => c.category === cat.id);
          const completedCount = catCourses.filter(c => {
            const p = student.progress[c.id];
            return p && p.unlockedSection >= c.sectionsCount;
          }).length;
          const catProgress = getCategoryProgress(student.progress, visibleCourses, cat.id);
          const isExpanded = expandedCategories.has(cat.id);

          return (
            <React.Fragment key={cat.id}>
              <Row
                title={cat.title}
                meta={`${completedCount}/${catCourses.length} complete`}
                progress={catProgress / 100}
                value={<Pct value={catProgress} />}
                expanded={isExpanded}
                onPress={() => toggleCategory(cat.id)}
              />
              <AnimatePresence>
                {isExpanded && (
                  <li key="courses" className="gc8-sd-more">
                    <MotionDiv
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.25, ease: CUSTOM_EASE }}
                      style={{ overflow: 'hidden' }}
                    >
                      <List label={cat.title}>
                        {catCourses.map(course => {
                          const p = student.progress[course.id];
                          const unlocked = p?.unlockedSection ?? 0;
                          const total = course.sectionsCount;
                          const pct = total > 0 ? Math.min(100, (unlocked / total) * 100) : 0;
                          const courseStatus = pct >= 100 ? 'Complete' : pct > 0 ? 'In progress' : 'Not started';
                          return (
                            <Row
                              key={course.id}
                              title={course.title}
                              progress={pct / 100}
                              value={<span className={pct >= 100 ? 'gc8-strong' : undefined}>{courseStatus}</span>}
                            />
                          );
                        })}
                      </List>
                    </MotionDiv>
                  </li>
                )}
              </AnimatePresence>
            </React.Fragment>
          );
        })}
      </List>
    </section>
  );

  // ─── Journey Simulator result ─────────────────────────────────────

  const renderJourneyResult = () => {
    const over = 'Engagement & wellbeing';
    if (!student.journeyResult) {
      return (
        <section className="gc8-sec gc8-sd-sec">
          <SecHead over={over} title="Journey Simulator" />
          <p className="gc8-sub">Not yet attempted.</p>
        </section>
      );
    }

    const jr = student.journeyResult;
    if (jr.scoringVersion !== JOURNEY_SCORING_VERSION) {
      return (
        <section className="gc8-sec gc8-sd-sec">
          <SecHead over={over} title="Journey Simulator" />
          <p className="gc8-sub">This result used the retired scoring model. The student will be prompted to complete the revised simulation before a new profile is shown.</p>
        </section>
      );
    }
    const archetype = ARCHETYPES[jr.endingId];
    const stats = jr.finalStats;
    const statKeys: CapabilityKey[] = [...CAPABILITY_KEYS];

    return (
      <section className="gc8-sec gc8-sd-sec">
        <SecHead over={over} title="Journey Simulator" />

        {archetype && (
          <div className="gc8-sd-copy">
            <p className="gc8-person">{archetype.title}</p>
            <p className="gc8-sub">{archetype.description}</p>
          </div>
        )}

        {/* Capability chart — energy is intentionally separate. Drawn in ink. */}
        <div className="gc8-sd-radar">
          <PentagonRadar
            values={statKeys.map(k => stats[k])}
            labels={statKeys.map(k => STAT_LABELS[k])}
            size={isTrayMode ? 220 : 300}
            colors={{ fill: 'var(--surface-soft)', stroke: 'var(--ink-primary)' }}
          />
        </div>

        {/* Capability rows */}
        <List>
          {statKeys.map(key => (
            <Row key={key} title={STAT_LABELS[key]} value={`${stats[key]}/100`} progress={stats[key] / 100} />
          ))}
        </List>
        <div className="gc8-sd-copy">
          <div className="gc8-who">
            <span className="gc8-person">Energy reserve</span>
            <span className="gc8-readout">{stats.energy}/100</span>
          </div>
          <p className="gc8-meta">A changing resource, not a capability grade. All scores are reflective simulation signals, not academic attainment or forecasts.</p>
        </div>
      </section>
    );
  };

  // ─── Activity (30 days), then streak and points ─────────────────────

  const renderActivity = () => {
    const streak = student.streak;
    const points = student.points;
    const totalEarned = points?.totalEarned ?? 0;
    const currentStreak = streak?.currentStreak ?? 0;

    return (
      <section className="gc8-sec gc8-sd-sec">
        <SecHead title="Activity (30 days)" />
        <svg viewBox="0 0 300 60" className="gc8-sd-act" preserveAspectRatio="none">
          {engagementTimeline.map((d, i) => {
            const barW = 300 / 30 - 1.5;
            const x = i * (300 / 30) + 0.75;
            const h = d.count > 0 ? Math.max(4, (d.count / maxBlocks) * 52) : 2;
            return (
              <rect
                key={d.date}
                x={x}
                y={60 - h}
                width={barW}
                height={h}
                rx={1.5}
                className={d.count > 0 ? 'gc8-sd-on' : undefined}
              >
                <title>{d.date}: {d.count} blocks</title>
              </rect>
            );
          })}
        </svg>
        <div className="gc8-sd-ends gc8-meta">
          <span>{engagementTimeline[0]?.date}</span>
          <span>{engagementTimeline[engagementTimeline.length - 1]?.date}</span>
        </div>
        <p className="gc8-totals">
          <span><b>{totalBlocks}</b> blocks completed</span>
          <span><b>{activeDays}</b> active days</span>
        </p>

        <div className="gc8-figrows gc8-sd-words">
          <div>
            <span className="gc8-figrows-col">
              <span className="gc8-sub">Streak</span>
              <span className="gc8-meta">Longest streak: {streak?.longestStreak ?? 0} · Last active: {streak?.lastActiveDate || 'Never'}</span>
            </span>
            <Fig className="gc8-num" value={currentStreak} unit={currentStreak !== 1 ? 'days' : 'day'} />
          </div>
          <div>
            <span className="gc8-sub">Points earned</span>
            <Fig className="gc8-num" value={totalEarned} unit="total" />
          </div>
        </div>
      </section>
    );
  };

  // ─── Insights ───────────────────────────────────────────────────────
  //
  // The "Insights" label sits over the first of these four that has something to show.
  const insightsLabel: { word: string | undefined } = { word: 'Insights' };
  const takeInsightsLabel = () => {
    const word = insightsLabel.word;
    insightsLabel.word = undefined;
    return word;
  };

  // ─── Insights: Career Direction (FF picks) ─────────────────────────────

  const renderCareerDirection = () => {
    const ff = student.futureFinder;
    if (!ff?.topPicks?.length) return null;
    const courses = hydrateCourses(ff.topPicks).slice(0, 3);
    if (courses.length === 0) return null;

    // `source` matters to a counsellor reading this. Saved picks are the
    // student's own bookmarks in save-order — numbering them 1/2/3 would
    // present an arbitrary order as a ranking. Only 'ranked' is a real
    // ranking, and 'legacy' comes from the retired tool so it may be stale.
    const isRanking = ff.source === 'ranked' || ff.source === 'legacy';
    const heading = ff.source === 'saved' ? 'Courses they saved' : 'Career direction';
    const completed = ff.completedAt ? new Date(ff.completedAt) : null;

    return (
      <section className="gc8-sec gc8-sd-sec">
        <SecHead over={takeInsightsLabel()} title={heading} />
        <p className="gc8-meta">
          {ff.source === 'saved' ? 'Their own picks, in the order they saved them' : ff.source === 'ranked' ? 'Top matches from Future Finder' : 'From the earlier Future Finder — may be out of date'}
          {completed && !isNaN(completed.getTime()) ? ` · ${completed.toLocaleDateString('en-IE', { day: 'numeric', month: 'short', year: 'numeric' })}` : ''}
        </p>
        <List>
          {courses.map((c, i) => (
            <Row
              key={c.code}
              lead={isRanking ? i + 1 : '·'}
              title={c.title}
              meta={`${c.institution} · Level ${c.level}`}
              value={`${c.typicalPoints} pts`}
            />
          ))}
        </List>
      </section>
    );
  };

  // ─── Insights: College Compass (read-only mirror of the student's marks) ──

  // Derived via the SHARED selector, so the GC sees exactly what the student
  // marked — same input state -> same output, no divergence possible.
  const compassProgress = student.collegeCompass ? computeCompassProgress(student.collegeCompass) : null;
  const hasCompassActivity = !!compassProgress && compassProgress.doneItems + compassProgress.inProgressItems > 0;

  const renderCollegeCompass = () => {
    if (!compassProgress || !hasCompassActivity) return null;
    const prog = compassProgress;
    const updated = prog.updatedAt ? new Date(prog.updatedAt) : null;
    return (
      <section className="gc8-sec gc8-sd-sec">
        <SecHead over={takeInsightsLabel()} title="College Compass" end={`${prog.doneItems}/${prog.totalItems} done`} />
        <span className="gc8-bar" aria-hidden="true"><i style={{ width: `${prog.percentDone}%` }} /></span>
        <p className="gc8-meta">
          {prog.percentDone}% complete{prog.inProgressItems ? ` · ${prog.inProgressItems} in progress` : ''}{updated ? ` · updated ${updated.toLocaleDateString('en-IE', { day: 'numeric', month: 'short' })}` : ''}
        </p>
        <List>
          {prog.stops.map(s => {
            if (s.dismissed) {
              return <Row key={s.stopId} className="gc8-sd-dim" title={s.title} meta="Marked not applicable" />;
            }
            const allDone = s.total > 0 && s.done === s.total;
            const isOpen = openStops.has(s.stopId);
            return (
              <React.Fragment key={s.stopId}>
                <Row
                  title={s.title}
                  meta={s.inProgress > 0 ? `${s.inProgress} in progress` : undefined}
                  value={<>{allDone ? <Check className="ui-icon gc8-sd-tick" width={16} height={16} strokeWidth={2} aria-label="All done" /> : null}{s.done}/{s.total}</>}
                  expanded={isOpen}
                  onPress={() => toggleStop(s.stopId)}
                />
                {isOpen && (
                  <li className="gc8-sd-more">
                    <ul className="gc8-sd-items">
                      {s.items.map(it => (
                        <li key={it.key} data-state={it.status}>
                          {it.status === 'done'
                            ? <CheckCircle className="gc8-sd-ok" width={14} height={14} strokeWidth={2} aria-label="Done" />
                            : it.status === 'in-progress'
                              ? <MinusCircle width={14} height={14} strokeWidth={2} aria-label="In progress" />
                              : <span className="gc8-sd-ring" aria-hidden="true" />}
                          <span className="gc8-sd-itemtext">{it.label}</span>
                        </li>
                      ))}
                    </ul>
                  </li>
                )}
              </React.Fragment>
            );
          })}
        </List>
      </section>
    );
  };

  // ─── Insights: Mock Trajectory ─────────────────────────────────────────

  const renderMockTrajectory = () => {
    if (!student.mockResults?.length) return null;
    const sorted = [...student.mockResults].sort((a, b) => (a.date ?? '').localeCompare(b.date ?? ''));

    return (
      <section className="gc8-sec gc8-sd-sec">
        <SecHead over={takeInsightsLabel()} title="Mock trajectory" />
        <table className="gc8-sd-table">
          <thead>
            <tr>
              <th className="gc8-label">Subject</th>
              <th className="gc8-label">Grade</th>
              <th className="gc8-label">Date</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((m) => (
              <tr key={m.id}>
                <td>{m.subject}</td>
                <td className="gc8-readout">{m.grade}</td>
                <td className="gc8-readout">{m.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    );
  };

  // ─── Insights: Struggle Areas (debrief hardestTopic grouped by subject) ──

  const renderStruggleAreas = () => {
    if (!student.recentDebriefs?.length) return null;

    const grouped: Record<string, string[]> = {};
    for (const d of student.recentDebriefs) {
      if (!d.hardestTopic || d.hardestTopic === 'Not specified') continue;
      if (!grouped[d.subject]) grouped[d.subject] = [];
      if (!grouped[d.subject].includes(d.hardestTopic)) {
        grouped[d.subject].push(d.hardestTopic);
      }
    }

    const entries = Object.entries(grouped);
    if (entries.length === 0) return null;

    return (
      <section className="gc8-sec gc8-sd-sec">
        <SecHead over={takeInsightsLabel()} title="Struggle areas" />
        <div className="gc8-sd-struggle">
          {entries.map(([subject, topics]) => (
            <div key={subject}>
              <p className="gc8-person">{subject}</p>
              <ul>
                {topics.map(t => (
                  <li key={t} className="gc8-sub">{t}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>
    );
  };

  // ─── Quick Actions (Recommend / Kudos) ───────────────────────────────

  // Staff→student messages go through the sendStaffNotification callable.
  // firestore.rules denies staff writes to /notifications: the safeguarding
  // control used to live in the student's own bundle, keyed on a field the
  // sender wrote, so one setDoc from a browser console put arbitrary prose in
  // front of a minor (security review 2026-08-17). The server now composes
  // every field a student sees from the preset id.
  const sendStaffMessage = async (
    kind: 'encouragement' | 'recommendation',
    presetId: string,
    toolId?: string,
  ): Promise<boolean> => {
    try {
      const fn = httpsCallable<
        { studentUids: string[]; kind: string; messageId?: string; toolId?: string },
        { success: true; delivered: number }
      >(getFunctions(app), 'sendStaffNotification');
      const result = await fn({
        studentUids: [student.user.uid],
        kind,
        messageId: presetId || undefined,
        toolId,
      });
      return result.data.delivered > 0;
    } catch (err) {
      logError('GCStudentDetail.sendStaffMessage', err);
      return false;
    }
  };

  const handleSendRecommendation = async () => {
    if (!recommendToolId) return;
    setIsSendingAction(true);
    await sendStaffMessage('recommendation', recommendNoteId, recommendToolId);
    setIsSendingAction(false);
    setShowRecommendModal(false);
    setRecommendToolId(null);
    setRecommendNoteId('');
  };

  const handleSendKudos = async () => {
    if (!isKnownStaffMessage(kudosMessageId)) return;
    setIsSendingAction(true);
    await sendStaffMessage('encouragement', kudosMessageId);
    setIsSendingAction(false);
    setShowKudosModal(false);
    setKudosMessageId('');
  };

  // Change flag: today's flag bar (Flagged … Unflag), as a menu that can also set the flag.
  const flagMenu = gcFlags ? (
    <MenuPanel label="Change flag" face="Change flag" buttonClassName="ui-btn" side={wide ? 'bottom' : 'top'}>
      <MenuRadioRows<FlagPriority>
        label={flagData ? 'Edit student flag' : 'Flag student'}
        value={(flagData?.priority ?? '') as FlagPriority}
        onChange={priority => { void (flagData ? gcFlags.updateFlagPriority(student.user.uid, priority) : gcFlags.flagStudent(student.user.uid, priority)); }}
        options={[{ value: 'high', label: 'Flagged, high priority' }, { value: 'normal', label: 'Flagged, normal priority' }]}
      />
      {flagData && <MenuAction plain title="Remove flag" onPress={() => { void gcFlags.unflagStudent(student.user.uid); }} />}
    </MenuPanel>
  ) : null;

  const renderActions = () => (
    <>
      <Button kind="main" size="lg" block arrow="forward" onClick={() => setShowKudosModal(true)}>Send encouragement</Button>
      {flagMenu ? (
        <div className="gc8-pair">
          <Button onClick={() => setShowRecommendModal(true)}>Recommend a tool</Button>
          {flagMenu}
        </div>
      ) : (
        <Button block onClick={() => setShowRecommendModal(true)}>Recommend a tool</Button>
      )}
    </>
  );

  const renderModals = () => (
    <>
      {/* Recommend a tool */}
      <Sheet
        open={showRecommendModal}
        onClose={() => { if (!isSendingAction) setShowRecommendModal(false); }}
        title="Recommend a tool"
        meta={`For ${name}`}
        footer={
          <Button
            kind="main"
            size="lg"
            block
            missing={!recommendToolId ? { sentence: 'Choose a tool to recommend.', goTo: recommendToolsRef } : undefined}
            onClick={() => { if (!isSendingAction) void handleSendRecommendation(); }}
          >
            {isSendingAction ? 'Sending...' : 'Send'}
          </Button>
        }
      >
        <div className="gc8-sheet-body">
          <div className="gc8-sheet-group" ref={recommendToolsRef}>
            <p className="gc8-label">Tool</p>
            <div className="gc8-msgs" role="radiogroup" aria-label="Tool">
              {/* Filter to tools available to this student's curriculum so
                  a GC can't recommend a senior-only tool to a JC student. */}
              {INNOVATION_TOOLS
                .filter(t => t.curriculum === 'both' || t.curriculum === (isJunior ? 'junior' : 'senior'))
                .map(tool => (
                  <ChoiceTile
                    key={tool.id}
                    kind="one"
                    chosen={recommendToolId === tool.id}
                    label={isJunior && tool.jcTitle ? tool.jcTitle : tool.title}
                    onClick={() => setRecommendToolId(tool.id)}
                  />
                ))}
            </div>
          </div>
          <div className="gc8-sheet-group">
            <p className="gc8-label">Add a note (optional)</p>
            <div className="gc8-msgs" role="radiogroup" aria-label="Add a note (optional)">
              {STAFF_RECOMMENDATION_NOTES.map(note => (
                <ChoiceTile
                  key={note.id}
                  kind="one"
                  chosen={recommendNoteId === note.id}
                  label={note.text}
                  onClick={() => setRecommendNoteId(recommendNoteId === note.id ? '' : note.id)}
                />
              ))}
            </div>
          </div>
        </div>
      </Sheet>

      {/* Send encouragement */}
      <Sheet
        open={showKudosModal}
        onClose={() => { if (!isSendingAction) setShowKudosModal(false); }}
        title="Send encouragement"
        meta={`To ${name}`}
        footer={
          <Button
            kind="main"
            size="lg"
            block
            missing={!isKnownStaffMessage(kudosMessageId) ? { sentence: 'Choose a message.', goTo: kudosMessagesRef } : undefined}
            onClick={() => { if (!isSendingAction) void handleSendKudos(); }}
          >
            {isSendingAction ? 'Sending...' : 'Send'}
          </Button>
        }
      >
        <div className="gc8-sheet-body">
          <div className="gc8-sheet-group" ref={kudosMessagesRef}>
            <p className="gc8-label">Message</p>
            <div className="gc8-msgs" role="radiogroup" aria-label="Message">
              {STAFF_ENCOURAGEMENT.map(message => (
                <ChoiceTile
                  key={message.id}
                  kind="one"
                  chosen={kudosMessageId === message.id}
                  label={message.text}
                  onClick={() => setKudosMessageId(message.id)}
                />
              ))}
            </div>
          </div>
        </div>
      </Sheet>
    </>
  );

  // ─── Render ─────────────────────────────────────────────────────────
  //
  // One layout. The dashboard only ever opens the tray (isTrayMode); the old
  // full-page branch drew the same sections in a grid, so it now draws this too.

  const moreMenu = onResetPassword || onDeleteStudent ? (
    <MenuPanel
      label={name}
      buttonLabel={`More for ${name}`}
      buttonClassName="gc8-acts"
      className="gc8-rowmenu"
      chevron={false}
      face={<MoreHorizontal className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />}
    >
      {onResetPassword && <MenuAction plain title="Reset password" onPress={() => onResetPassword(student.user.uid)} />}
      {onDeleteStudent && <MenuAction plain tone="danger" title="Delete account" onPress={() => onDeleteStudent(student.user)} />}
    </MenuPanel>
  ) : undefined;

  return (
    <div className="gc8-sd">
      <TopBar className="gc8-sd-bar" leave={{ kind: wide ? 'close' : 'back', onPress: onBack }} action={moreMenu} />
      {renderModals()}
      <div className="gc8-sd-body">
        {renderStudent()}
        {wide && <div className="gc8-sd-acts">{renderActions()}</div>}
        {renderNotices()}
        {renderFigures()}

        {renderSubjectProfile()}
        {renderNorthStar()}
        {renderModuleProgress()}
        {renderJourneyResult()}
        {renderActivity()}
        {renderCareerDirection()}
        {renderCollegeCompass()}
        {renderMockTrajectory()}
        {renderStruggleAreas()}
      </div>
      {!wide && <PinnedFooter ruled>{renderActions()}</PinnedFooter>}
    </div>
  );
};
