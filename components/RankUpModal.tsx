/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * RankUpModal — editorial cream level-up takeover.
 *
 * Replaces the previous saturated teal full-screen treatment. The rank
 * name does the visual work: huge serif, full black, single line, on flat
 * cream. Everything else (eyebrow level chip, journey bar, reward card,
 * action buttons) is restrained and centred so the moment lands.
 *
 * Layout (top → bottom, all centred):
 *   1. "LEVEL X OF 8" eyebrow + terracotta accent rule, close X top-right
 *   2. The rank title (96–120px serif)
 *   3. Hairline rule (140px wide)
 *   4. 2-line sub-headline
 *   5. 8-node dashed journey bar with terracotta current node + flag at 8
 *   6. Reward card (island illustration + "Your island is growing")
 *   7. Black "Continue" + cream outlined "View My Journey"
 */

import React from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { type AthleteRank, ATHLETE_RANKS } from '../gamificationConfig';
import { X } from 'lucide-react';
import { useModal } from '../hooks/useModal';

const SERIF: React.CSSProperties = { fontFamily: "'Source Serif 4', serif" };
const SANS: React.CSSProperties = { fontFamily: "'DM Sans', system-ui, sans-serif" };
const TERRACOTTA = '#D85F47';
const CREAM = '#FAFBF6';
const NODE_BG = '#F5EFE3';
const TEXT = '#1a1a1a';

// Rank copy — split per the new editorial header into a short italic
// terracotta tagline and a longer DM Sans body description. Indexed by
// rank position; rank id/title/minPoints stay in gamificationConfig.
interface RankCopy {
  tagline: string;
  body: string;
}
const RANK_COPY: RankCopy[] = [
  {
    tagline: 'Your journey starts here.',
    body: 'Every expert was once a beginner. The work begins one small step at a time.',
  },
  {
    tagline: "You're picking up the patterns.",
    body: 'The first habits are taking hold. Keep showing up — that is where it builds from.',
  },
  {
    tagline: "You're finding your rhythm.",
    body: 'Small steps, repeated with intention, create a path that keeps moving forward.',
  },
  {
    tagline: "You're past the early hill.",
    body: 'The view from here is different. You have earned a kind of momentum that cannot be faked.',
  },
  {
    tagline: "You're not most people.",
    body: 'Most stop somewhere behind you. You kept going when there was no obvious reason to.',
  },
  {
    tagline: "You've earned your confidence.",
    body: 'What used to be effort is now instinct. Keep climbing — there is still terrain ahead.',
  },
  {
    tagline: 'This is rare air.',
    body: "You're competing with your former self now. The bar that mattered most is the one you set.",
  },
  {
    tagline: "You've reached the top.",
    body: 'The work was the point. Everything from here is the view you have earned.',
  },
];

interface RankUpModalProps {
  isOpen: boolean;
  newRank: AthleteRank | null;
  onClose: () => void;
  onGoToJourney?: () => void;
}

const RankUpModal: React.FC<RankUpModalProps> = ({ isOpen, newRank, onClose, onGoToJourney }) => {
  useModal(isOpen, onClose);
  if (!newRank) return null;

  const rankIndex = ATHLETE_RANKS.findIndex(r => r.id === newRank.id);
  const levelNumber = rankIndex + 1;
  const copy = RANK_COPY[rankIndex] ?? RANK_COPY[0];
  const isLegendCelebration = rankIndex === ATHLETE_RANKS.length - 1;

  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
          className="fixed inset-0 z-[300] overflow-y-auto"
          style={{ backgroundColor: CREAM }}
        >
          {/* Close button — top-right, neutral outline */}
          <button
            onClick={onClose}
            aria-label="Close"
            className="absolute top-6 right-6 w-9 h-9 rounded-full flex items-center justify-center transition-colors hover:bg-black/[0.04]"
            style={{ border: '1px solid rgba(0,0,0,0.15)', color: 'rgba(0,0,0,0.6)' }}
          >
            <X size={16} strokeWidth={2} />
          </button>

          <div className="min-h-screen flex flex-col items-center px-6 pt-8 pb-12">
            {/* ── Editorial two-column hero ── */}
            <MotionDiv
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1, duration: 0.5, ease: [0.16, 1, 0.3, 1] as number[] }}
              style={{
                width: '100%',
                maxWidth: 1240,
                display: 'flex',
                flexDirection: 'row',
                alignItems: 'stretch',
                gap: 24,
                flexWrap: 'wrap',
                justifyContent: 'center',
              }}
            >
              {/* Left column — badge row + composed title block */}
              <div
                style={{
                  flex: '1 1 480px',
                  minWidth: 0,
                  display: 'flex',
                  flexDirection: 'column',
                }}
              >
                {/* Badge + level eyebrow */}
                <div style={{ display: 'flex', alignItems: 'center', gap: 18 }}>
                  <LevelBadgeIcon />
                  <div style={{ display: 'flex', flexDirection: 'column' }}>
                    <span
                      className="uppercase"
                      style={{
                        ...SANS,
                        fontSize: 13,
                        fontWeight: 500,
                        letterSpacing: '2.4px',
                        color: 'rgba(0,0,0,0.55)',
                      }}
                    >
                      Level {levelNumber} of {ATHLETE_RANKS.length}
                    </span>
                    <img
                      src="/assets/level-up/eyebrow-rule.png"
                      alt=""
                      style={{
                        display: 'block',
                        width: 132,
                        height: 'auto',
                        marginTop: 6,
                      }}
                      draggable={false}
                    />
                  </div>
                </div>

                {/* Title block — pushed toward column bottom so it sits
                    around the illustration's vertical centre */}
                <div style={{ marginTop: 'auto', paddingTop: 56 }}>
                  {/* Title with matching-width hairline + sparkle below */}
                  <div style={{ width: 'fit-content', maxWidth: '100%' }}>
                    <h1
                      style={{
                        ...SERIF,
                        fontWeight: 500,
                        fontSize: 'clamp(72px, 11vw, 152px)',
                        letterSpacing: '-1.5px',
                        color: TEXT,
                        margin: 0,
                        lineHeight: 1,
                      }}
                    >
                      {newRank.title}
                    </h1>
                    <HairlineWithSparkle />
                  </div>

                  <MotionDiv
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.45, duration: 0.4 }}
                  >
                    <p
                      style={{
                        ...SERIF,
                        fontStyle: 'italic',
                        fontSize: 'clamp(22px, 2.6vw, 32px)',
                        color: TERRACOTTA,
                        margin: 0,
                        marginTop: 6,
                        lineHeight: 1.25,
                      }}
                    >
                      {copy.tagline}
                    </p>
                    <p
                      style={{
                        ...SANS,
                        fontSize: 15,
                        color: 'rgba(0,0,0,0.55)',
                        lineHeight: 1.6,
                        margin: 0,
                        marginTop: 18,
                        maxWidth: 460,
                      }}
                    >
                      {copy.body}
                    </p>
                  </MotionDiv>
                </div>
              </div>

              {/* Right column — illustration */}
              <div
                style={{
                  flex: '1 1 460px',
                  width: '100%',
                  maxWidth: 560,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <HeaderIllustrationPlaceholder />
              </div>
            </MotionDiv>

            {/* ── 5. Journey progress bar ── */}
            <MotionDiv
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6, duration: 0.4 }}
              style={{ marginTop: 56, width: '100%', maxWidth: 880 }}
            >
              <JourneyBar
                currentIndex={rankIndex}
                totalRanks={ATHLETE_RANKS.length}
                isLegendCelebration={isLegendCelebration}
              />
            </MotionDiv>

            {/* ── 6. Reward card ── */}
            <MotionDiv
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8, duration: 0.4, ease: [0.16, 1, 0.3, 1] as number[] }}
              style={{ marginTop: 64, width: '100%', maxWidth: 600 }}
            >
              <div
                style={{
                  backgroundColor: CREAM,
                  border: '1px solid rgba(0,0,0,0.1)',
                  borderRadius: 14,
                  padding: '24px 28px',
                  boxShadow: '0 2px 8px rgba(0,0,0,0.04)',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 20,
                }}
              >
                <IslandIllustration />
                <div style={{ flex: 1, minWidth: 0 }}>
                  <h3
                    style={{
                      ...SERIF,
                      fontSize: 18,
                      fontWeight: 500,
                      color: TEXT,
                      margin: 0,
                      lineHeight: 1.25,
                    }}
                  >
                    Your island is growing
                  </h3>
                  <p
                    style={{
                      ...SANS,
                      fontSize: 14,
                      color: 'rgba(0,0,0,0.6)',
                      lineHeight: 1.5,
                      margin: 0,
                      marginTop: 6,
                    }}
                  >
                    3 new tiles added to your island. Visit My Journey to see it expand.
                  </p>
                </div>
              </div>
            </MotionDiv>

            {/* ── 7. Action buttons ── */}
            <MotionDiv
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.9, duration: 0.4 }}
              style={{
                marginTop: 32,
                width: '100%',
                maxWidth: 360,
                display: 'flex',
                flexDirection: 'column',
                gap: 12,
              }}
            >
              <button
                onClick={onClose}
                style={{
                  ...SANS,
                  backgroundColor: TEXT,
                  color: '#FFFFFF',
                  fontSize: 15,
                  fontWeight: 500,
                  padding: '14px 64px',
                  borderRadius: 10,
                  border: 'none',
                  boxShadow: '0 2px 6px rgba(0,0,0,0.15)',
                  cursor: 'pointer',
                  width: '100%',
                }}
              >
                Continue
              </button>
              {onGoToJourney && (
                <button
                  onClick={() => { onClose(); onGoToJourney(); }}
                  style={{
                    ...SANS,
                    backgroundColor: CREAM,
                    color: TEXT,
                    fontSize: 15,
                    fontWeight: 500,
                    padding: '14px 64px',
                    borderRadius: 10,
                    border: '1px solid rgba(0,0,0,0.15)',
                    cursor: 'pointer',
                    width: '100%',
                  }}
                >
                  View My Journey
                </button>
              )}
            </MotionDiv>
          </div>
        </motion.div>
      )}
    </AnimatePresence>,
    document.body
  );
};

// ────────────────────────────────────────────────────────────────────────
// Journey bar — 7 numbered nodes + ink flag, threaded by a wavy dashed
// path. Current node is solid terracotta with a small terracotta down-
// arrow above it. Renders as a single scalable SVG (viewBox 1080×220).
// ────────────────────────────────────────────────────────────────────────

interface JourneyBarProps {
  currentIndex: number;
  totalRanks: number;
  /** When true, the bar performs the Legend climax: terracotta sweeps the
   *  whole path, every numbered node lights up in sequence, and the flag
   *  unfurls inside a radiating burst. */
  isLegendCelebration: boolean;
}

// Animation timing for the Legend celebration. Other ranks ignore these.
const LEGEND_PATH_DELAY = 0.5;
const LEGEND_PATH_DURATION = 1.5;
const LEGEND_NODE_BASE_DELAY = 0.65;
const LEGEND_NODE_STAGGER = 0.13;
const LEGEND_FLAG_DELAY = 1.95;

// Hand-tuned positions inside the 1080×220 viewBox. The path undulates
// gently up/down so the journey reads as a real route rather than a
// straight line of pips.
const NODE_POSITIONS: { x: number; y: number }[] = [
  { x: 70,   y: 150 }, // 1
  { x: 215,  y: 110 }, // 2 (example current)
  { x: 360,  y: 95  }, // 3
  { x: 500,  y: 155 }, // 4
  { x: 645,  y: 95  }, // 5
  { x: 785,  y: 160 }, // 6
  { x: 925,  y: 105 }, // 7
  { x: 1035, y: 105 }, // flag (8)
];

// Smooth cubic Bézier path through the 8 control points; ends just shy
// of the flag pole so a tiny gap sits between the dashed line and the
// pole, matching the reference.
const PATH_D = [
  `M ${NODE_POSITIONS[0].x} ${NODE_POSITIONS[0].y}`,
  'C 140 150, 145 110, 215 110',
  'C 275 110, 305 95, 360 95',
  'C 420 95, 440 165, 500 155',
  'C 560 145, 580 85, 645 95',
  'C 705 105, 725 170, 785 160',
  'C 845 150, 865 95, 925 105',
  'L 1015 105',
].join(' ');

const NODE_R = 26;

const JourneyBar: React.FC<JourneyBarProps> = ({ currentIndex, totalRanks, isLegendCelebration }) => {
  return (
    <svg
      viewBox="0 0 1080 220"
      preserveAspectRatio="xMidYMid meet"
      aria-hidden="true"
      style={{ width: '100%', height: 'auto', display: 'block', overflow: 'visible' }}
    >
      {/* Wavy dashed gray path — always rendered */}
      <path
        d={PATH_D}
        fill="none"
        stroke="rgba(0,0,0,0.4)"
        strokeWidth="1.8"
        strokeDasharray="9 7"
        strokeLinecap="round"
      />

      {/* Legend climax — terracotta path drawing left-to-right over the dashed gray */}
      {isLegendCelebration && (
        <motion.path
          d={PATH_D}
          fill="none"
          stroke={TERRACOTTA}
          strokeWidth="2.4"
          strokeLinecap="round"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ delay: LEGEND_PATH_DELAY, duration: LEGEND_PATH_DURATION, ease: 'easeOut' }}
        />
      )}

      {NODE_POSITIONS.map((pos, i) => {
        const isCurrent = i === currentIndex;
        const isFlag = i === totalRanks - 1;
        return (
          <g key={i} transform={`translate(${pos.x} ${pos.y})`}>
            {isFlag ? (
              <FlagSvg isLegendCelebration={isLegendCelebration} />
            ) : (
              <NumberNodeSvg
                number={i + 1}
                isCurrent={isCurrent}
                isLegendCelebration={isLegendCelebration}
              />
            )}
          </g>
        );
      })}
    </svg>
  );
};

interface NumberNodeSvgProps {
  number: number;
  isCurrent: boolean;
  isLegendCelebration: boolean;
}

const NumberNodeSvg: React.FC<NumberNodeSvgProps> = ({ number, isCurrent, isLegendCelebration }) => {
  // Base inactive node — cream fill, dark thin stroke, dark number.
  const inactiveNode = (
    <>
      <circle r={NODE_R} cx={0} cy={0} fill={NODE_BG} stroke="rgba(0,0,0,0.45)" strokeWidth="1.6" />
      <text
        x="0"
        y="0"
        textAnchor="middle"
        dominantBaseline="central"
        style={{ ...SANS, fontSize: 18, fontWeight: 500, fill: TEXT }}
      >
        {number}
      </text>
    </>
  );

  // Legend climax — every numbered node activates in sequence as the
  // terracotta sweep reaches it. Render the inactive node, then a
  // terracotta overlay that fades in on cue, with a small pop scale.
  if (isLegendCelebration) {
    const delay = LEGEND_NODE_BASE_DELAY + (number - 1) * LEGEND_NODE_STAGGER;
    return (
      <g>
        {inactiveNode}
        <motion.g
          initial={{ opacity: 0, scale: 0.85 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay, duration: 0.35, ease: [0.34, 1.56, 0.64, 1] as number[] }}
        >
          <circle r={NODE_R} cx={0} cy={0} fill={TERRACOTTA} />
          <text
            x="0"
            y="0"
            textAnchor="middle"
            dominantBaseline="central"
            style={{ ...SANS, fontSize: 18, fontWeight: 500, fill: '#FFFFFF' }}
          >
            {number}
          </text>
        </motion.g>
      </g>
    );
  }

  if (isCurrent) {
    return (
      <g>
        {/* Down arrow above the node */}
        <g transform={`translate(0 ${-NODE_R - 22})`}>
          <line x1="0" y1="0" x2="0" y2="14" stroke={TERRACOTTA} strokeWidth="2" strokeLinecap="round" />
          <polyline
            points="-5,9 0,14 5,9"
            fill="none"
            stroke={TERRACOTTA}
            strokeWidth="2"
            strokeLinejoin="round"
            strokeLinecap="round"
          />
        </g>
        <motion.circle
          r={NODE_R}
          cx={0}
          cy={0}
          fill={TERRACOTTA}
          initial={{ scale: 1 }}
          animate={{ scale: [1, 1.15, 1] }}
          transition={{ delay: 0.7, duration: 0.6, ease: [0.34, 1.56, 0.64, 1] as number[] }}
        />
        <text
          x="0"
          y="0"
          textAnchor="middle"
          dominantBaseline="central"
          style={{ ...SANS, fontSize: 18, fontWeight: 500, fill: '#FFFFFF' }}
        >
          {number}
        </text>
      </g>
    );
  }

  return <g>{inactiveNode}</g>;
};

// ────────────────────────────────────────────────────────────────────────
// Final flag — hand-drawn PNG with terracotta triangle + black pole.
// The original 1254×1254 source was split into:
//   - legend-flag.png         (pole + flag triangle, beams masked out)
//   - legend-beam-{0..6}.png  (each ray cropped to its bbox + 4px pad)
//
// The PNG is mapped into the journey-bar SVG via an `<image>` element. We
// align the pole base with the local origin (0,0), so the dashed path
// ends right at the flag's foot.
//
// In Legend mode, the 7 beam PNGs render around the flag in order of
// clockwise angle, each fading in with a small stagger so the rays read
// as appearing one by one.
// ────────────────────────────────────────────────────────────────────────

// Size of the original 1254×1254 source canvas in journey-bar viewBox
// units. Tuned so the visible flag reads at roughly the same height as
// the inline ink flag it replaces (~50 vbx tall).
const FLAG_CANVAS_VBX = 92;
// Pole-base midpoint in source canvas coords (sampled from the PNG).
const FLAG_BASE_X_PCT = 555 / 1254;
const FLAG_BASE_Y_PCT = 1078 / 1254;
const FLAG_OFFSET_X = -FLAG_BASE_X_PCT * FLAG_CANVAS_VBX;
const FLAG_OFFSET_Y = -FLAG_BASE_Y_PCT * FLAG_CANVAS_VBX;

// Each beam's bbox in the source canvas, expressed as percentages.
// Sorted by clockwise angle from the flag centre so they appear in
// rotational order.
const BEAM_META: { x: number; y: number; w: number; h: number }[] = [
  { x: 0.1244, y: 0.4171, w: 0.1571, h: 0.0239 }, // far-left horizontal
  { x: 0.2313, y: 0.1467, w: 0.1308, h: 0.1284 }, // top-left diagonal
  { x: 0.5032, y: 0.0263, w: 0.0247, h: 0.1794 }, // top centre vertical
  { x: 0.6635, y: 0.1667, w: 0.1284, h: 0.1196 }, // top-right diagonal
  { x: 0.7520, y: 0.4171, w: 0.1523, h: 0.0223 }, // far-right horizontal
  { x: 0.6906, y: 0.5909, w: 0.1069, h: 0.1180 }, // bottom-right diagonal
  { x: 0.2225, y: 0.5909, w: 0.1077, h: 0.1124 }, // bottom-left diagonal
];

const FlagSvg: React.FC<{ isLegendCelebration: boolean }> = ({ isLegendCelebration }) => {
  // The flag PNG itself — same image for every rank, only its entrance
  // animation differs. Non-Legend renders it static; Legend hoists it in
  // with the rest of the climax.
  const flagImage = isLegendCelebration ? (
    <motion.image
      href="/assets/level-up/legend-flag.png"
      x={FLAG_OFFSET_X}
      y={FLAG_OFFSET_Y}
      width={FLAG_CANVAS_VBX}
      height={FLAG_CANVAS_VBX}
      preserveAspectRatio="xMidYMid meet"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: LEGEND_FLAG_DELAY, duration: 0.55, ease: [0.16, 1, 0.3, 1] as number[] }}
    />
  ) : (
    <image
      href="/assets/level-up/legend-flag.png"
      x={FLAG_OFFSET_X}
      y={FLAG_OFFSET_Y}
      width={FLAG_CANVAS_VBX}
      height={FLAG_CANVAS_VBX}
      preserveAspectRatio="xMidYMid meet"
    />
  );

  return (
    <g>
      {flagImage}
      {isLegendCelebration && BEAM_META.map((m, i) => (
        <motion.image
          key={i}
          href={`/assets/level-up/legend-beam-${i}.png`}
          x={FLAG_OFFSET_X + m.x * FLAG_CANVAS_VBX}
          y={FLAG_OFFSET_Y + m.y * FLAG_CANVAS_VBX}
          width={m.w * FLAG_CANVAS_VBX}
          height={m.h * FLAG_CANVAS_VBX}
          preserveAspectRatio="xMidYMid meet"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{
            delay: LEGEND_FLAG_DELAY + 0.55 + i * 0.09,
            duration: 0.4,
            ease: 'easeOut',
          }}
        />
      ))}
    </g>
  );
};

// ────────────────────────────────────────────────────────────────────────
// Island illustration — hand-drawn ink mountains PNG, dropped into the
// reward card via <img>. The artwork is the source of truth and isn't
// re-rendered as inline SVG.
// ────────────────────────────────────────────────────────────────────────

const IslandIllustration: React.FC = () => (
  <img
    src="/assets/level-up/island-mountains.png"
    alt=""
    width={88}
    height={88}
    style={{
      width: 88,
      height: 88,
      objectFit: 'contain',
      flexShrink: 0,
    }}
    draggable={false}
  />
);

// ────────────────────────────────────────────────────────────────────────
// Header illustration — hand-drawn mountain landscape with a winding
// path up to a flag at the summit. Loaded as a PNG so the artwork is
// the source of truth.
// ────────────────────────────────────────────────────────────────────────

const HeaderIllustrationPlaceholder: React.FC = () => (
  <img
    src="/assets/level-up/header-mountain.png"
    alt=""
    style={{
      width: '100%',
      height: '100%',
      objectFit: 'contain',
      display: 'block',
    }}
    draggable={false}
  />
);

// ────────────────────────────────────────────────────────────────────────
// Level badge — hand-drawn ink mountain + terracotta pennant inside a
// thin tan ring. PNG is the source of truth.
// ────────────────────────────────────────────────────────────────────────

const LevelBadgeIcon: React.FC = () => (
  <img
    src="/assets/level-up/level-badge.png"
    alt=""
    width={64}
    height={64}
    style={{ width: 64, height: 64, flexShrink: 0, objectFit: 'contain', display: 'block' }}
    draggable={false}
  />
);

// ────────────────────────────────────────────────────────────────────────
// Title divider — hand-drawn horizontal rule with a terracotta sunrise
// burst at its midpoint. Sits directly under the rank title; the
// wrapping div uses `width: fit-content` so the divider matches the
// title width on every rank. PNG is the source of truth.
// ────────────────────────────────────────────────────────────────────────

const HairlineWithSparkle: React.FC = () => (
  <div
    style={{
      width: '100%',
      display: 'flex',
      justifyContent: 'center',
      marginTop: 12,
    }}
  >
    <img
      src="/assets/level-up/title-divider.png"
      alt=""
      style={{
        display: 'block',
        height: 56,
        width: 'auto',
        maxWidth: '100%',
        objectFit: 'contain',
      }}
      draggable={false}
    />
  </div>
);

export default RankUpModal;
