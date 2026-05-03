/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * PointsPanel — reference panel for the Innovation Zone, surfaced via
 * a `?` tooltip icon in the IZ header rather than autoshown inline.
 *
 * Visual register matches the home dashboard SectionCards:
 *   - Painted-blob + ink-illustration tile per item (not a tinted dot)
 *   - Cream card surface with soft teal border
 *   - Source Serif 4 display + DM Sans UI; no Lucide on the surface
 *
 * Each item icon is a self-contained inline SVG with a Bezier blob fill
 * at 0.75 opacity and a black-ink illustration on top, drawn in the
 * same vocabulary as components/sectionIcons.tsx.
 */
import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const TEAL = '#2A7D6F';

// ── Item icons — painted-blob + ink-illustration, 100x100 viewBox ───────
const StudySessionIcon: React.FC = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%" aria-hidden="true">
    <path
      d="M 12 28 Q 6 50 14 72 Q 28 88 50 86 Q 78 84 84 62 Q 90 38 76 22 Q 58 10 36 16 Q 18 22 12 28 Z"
      fill="#B8DDC8"
      opacity="0.75"
    />
    <g>
      <circle cx="50" cy="50" r="22" fill="white" stroke="#1a1a1a" strokeWidth="1.5" />
      <line x1="50" y1="50" x2="50" y2="36" stroke="#1a1a1a" strokeWidth="1.6" strokeLinecap="round" />
      <line x1="50" y1="50" x2="60" y2="56" stroke="#1a1a1a" strokeWidth="1.4" strokeLinecap="round" />
      <circle cx="50" cy="50" r="1.5" fill="#1a1a1a" />
      <circle cx="50" cy="32" r="0.9" fill="#1a1a1a" />
      <circle cx="68" cy="50" r="0.9" fill="#1a1a1a" />
      <circle cx="50" cy="68" r="0.9" fill="#1a1a1a" />
      <circle cx="32" cy="50" r="0.9" fill="#1a1a1a" />
    </g>
  </svg>
);

const ModuleSectionIcon: React.FC = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%" aria-hidden="true">
    <path
      d="M 14 26 Q 8 48 14 70 Q 26 86 48 84 Q 76 82 82 62 Q 88 38 78 24 Q 62 12 38 16 Q 20 22 14 26 Z"
      fill="#F5C9A8"
      opacity="0.75"
    />
    <g>
      <path
        d="M 32 22 L 60 22 L 72 34 L 72 80 L 32 80 Z"
        fill="white"
        stroke="#1a1a1a"
        strokeWidth="1.5"
        strokeLinejoin="round"
      />
      <path d="M 60 22 L 60 34 L 72 34" fill="none" stroke="#1a1a1a" strokeWidth="1.5" strokeLinejoin="round" />
      <line x1="38" y1="44" x2="60" y2="44" stroke="#1a1a1a" strokeWidth="1.2" strokeLinecap="round" />
      <line x1="38" y1="52" x2="66" y2="52" stroke="#1a1a1a" strokeWidth="1.2" strokeLinecap="round" />
      <line x1="38" y1="60" x2="62" y2="60" stroke="#1a1a1a" strokeWidth="1.2" strokeLinecap="round" />
      <line x1="38" y1="68" x2="56" y2="68" stroke="#1a1a1a" strokeWidth="1.2" strokeLinecap="round" />
    </g>
  </svg>
);

const CompleteModuleIcon: React.FC = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%" aria-hidden="true">
    <path
      d="M 14 28 Q 8 48 16 68 Q 28 84 50 84 Q 76 84 84 64 Q 90 40 78 24 Q 60 12 38 18 Q 20 24 14 28 Z"
      fill="#D4B978"
      opacity="0.75"
    />
    <g>
      <line x1="32" y1="22" x2="32" y2="80" stroke="#1a1a1a" strokeWidth="1.6" strokeLinecap="round" />
      <path
        d="M 32 22 L 70 28 L 60 38 L 70 48 L 32 48 Z"
        fill="white"
        stroke="#1a1a1a"
        strokeWidth="1.5"
        strokeLinejoin="round"
      />
      <path
        d="M 44 32 L 50 38 L 60 28"
        fill="none"
        stroke="#1a1a1a"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </g>
  </svg>
);

const QuestsIcon: React.FC = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%" aria-hidden="true">
    <path
      d="M 12 30 Q 6 52 16 72 Q 28 88 52 84 Q 78 80 84 60 Q 90 36 76 20 Q 58 10 36 18 Q 20 24 12 30 Z"
      fill="#D9A9C2"
      opacity="0.75"
    />
    <g>
      <circle cx="50" cy="50" r="24" fill="white" stroke="#1a1a1a" strokeWidth="1.5" />
      <circle cx="50" cy="50" r="15" fill="none" stroke="#1a1a1a" strokeWidth="1.2" />
      <circle cx="50" cy="50" r="6" fill="#1a1a1a" />
    </g>
  </svg>
);

const IslandShopIcon: React.FC = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%" aria-hidden="true">
    <path
      d="M 14 28 Q 8 50 16 70 Q 28 88 50 86 Q 76 84 84 62 Q 90 38 76 22 Q 58 10 36 16 Q 18 22 14 28 Z"
      fill="#A8C9A0"
      opacity="0.75"
    />
    <g>
      <path
        d="M 32 24 L 78 24 L 78 50 L 54 78 L 22 50 L 22 34 Z"
        fill="white"
        stroke="#1a1a1a"
        strokeWidth="1.5"
        strokeLinejoin="round"
      />
      <circle cx="34" cy="36" r="3.5" fill="#FAFBF6" stroke="#1a1a1a" strokeWidth="1.3" />
    </g>
  </svg>
);

const SkipBlockIcon: React.FC = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%" aria-hidden="true">
    <path
      d="M 12 28 Q 6 50 14 72 Q 28 88 52 86 Q 80 82 86 60 Q 90 36 76 22 Q 58 10 36 16 Q 18 22 12 28 Z"
      fill="#9DB7CC"
      opacity="0.75"
    />
    <g>
      <path d="M 28 28 L 50 50 L 28 72" fill="none" stroke="#1a1a1a" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M 50 28 L 72 50 L 50 72" fill="none" stroke="#1a1a1a" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
    </g>
  </svg>
);

const RestDayIcon: React.FC = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%" aria-hidden="true">
    <path
      d="M 14 28 Q 8 50 16 70 Q 28 88 50 86 Q 78 84 84 62 Q 90 38 76 22 Q 58 10 36 16 Q 20 22 14 28 Z"
      fill="#B8C9E5"
      opacity="0.75"
    />
    <g>
      <path
        d="M 72 52 A 24 24 0 1 1 48 28 A 18 18 0 0 0 72 52 Z"
        fill="white"
        stroke="#1a1a1a"
        strokeWidth="1.5"
        strokeLinejoin="round"
      />
      <circle cx="78" cy="30" r="1.2" fill="#1a1a1a" />
      <circle cx="32" cy="22" r="1" fill="#1a1a1a" />
    </g>
  </svg>
);

const CloseIcon: React.FC = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M18 6 6 18M6 6l12 12" />
  </svg>
);

// ── Item data ──────────────────────────────────────────────────────────
interface Item {
  Icon: React.FC;
  label: string;
  value: string;
  sub: string;
}

const EARN_ITEMS: Item[] = [
  { Icon: StudySessionIcon,   label: 'Study session',        value: '15 pts',     sub: 'Per 10 min' },
  { Icon: ModuleSectionIcon,  label: 'Module section',       value: '10 pts',     sub: 'Each section' },
  { Icon: CompleteModuleIcon, label: 'Complete a module',    value: '+30 bonus',  sub: 'On finish' },
  { Icon: QuestsIcon,         label: 'Quests & challenges',  value: '25–200 pts', sub: 'Varies' },
];

const SPEND_ITEMS: Item[] = [
  { Icon: IslandShopIcon, label: 'Island shop',   value: 'Varies', sub: 'Build your island' },
  { Icon: SkipBlockIcon,  label: 'Skip a block',  value: '20 pts', sub: 'Skip one session' },
  { Icon: RestDayIcon,    label: 'Rest day pass', value: '60 pts', sub: 'Day off, streak safe' },
];

// ── Item card ──────────────────────────────────────────────────────────
const ItemCard: React.FC<{ item: Item }> = ({ item }) => (
  <div
    className="rounded-xl"
    style={{
      background: '#FAFBF6',
      border: `1px solid ${TEAL}26`,
      padding: 18,
    }}
  >
    <div style={{ width: 56, height: 56 }}>
      <item.Icon />
    </div>
    <p
      style={{
        fontFamily: "'DM Sans', system-ui, sans-serif",
        fontSize: 14,
        fontWeight: 500,
        color: 'rgba(0,0,0,0.85)',
        margin: 0,
        marginTop: 14,
        lineHeight: 1.3,
      }}
    >
      {item.label}
    </p>
    <p
      className="font-serif"
      style={{
        fontSize: 22,
        fontWeight: 500,
        color: TEAL,
        margin: 0,
        marginTop: 4,
        lineHeight: 1.15,
        letterSpacing: '-0.3px',
      }}
    >
      {item.value}
    </p>
    <p
      style={{
        fontFamily: "'DM Sans', system-ui, sans-serif",
        fontSize: 12,
        color: 'rgba(0,0,0,0.55)',
        margin: 0,
        marginTop: 4,
        lineHeight: 1.4,
      }}
    >
      {item.sub}
    </p>
  </div>
);

// ── Main panel ─────────────────────────────────────────────────────────
interface PointsPanelProps {
  open: boolean;
  onHide: () => void;
}

const PointsPanel: React.FC<PointsPanelProps> = ({ open, onHide }) => (
  <AnimatePresence initial={false}>
    {open && (
      <motion.section
        initial={{ height: 0, opacity: 0, marginBottom: 0 }}
        animate={{ height: 'auto', opacity: 1, marginBottom: 32 }}
        exit={{ height: 0, opacity: 0, marginBottom: 0 }}
        transition={{ duration: 0.32, ease: [0.16, 1, 0.3, 1] }}
        className="overflow-hidden"
        aria-label="How points work"
      >
        <div
          className="rounded-[18px]"
          style={{
            background: '#FAFBF6',
            border: `1px solid ${TEAL}40`,
            boxShadow: '0 2px 8px rgba(0,0,0,0.04)',
            padding: 32,
          }}
        >
          {/* Header row */}
          <div className="flex items-start justify-between gap-4 mb-5">
            <div className="min-w-0">
              <p
                style={{
                  fontFamily: "'DM Sans', system-ui, sans-serif",
                  fontSize: 11,
                  fontWeight: 500,
                  letterSpacing: '0.2em',
                  textTransform: 'uppercase',
                  color: 'rgba(0,0,0,0.5)',
                  margin: 0,
                  marginBottom: 12,
                }}
              >
                Your points
              </p>
              <h2
                className="font-serif"
                style={{
                  fontSize: 32,
                  fontWeight: 500,
                  letterSpacing: '-0.6px',
                  lineHeight: 1.05,
                  color: '#1A1A1A',
                  margin: 0,
                }}
              >
                Study more, earn more.
              </h2>
              <p
                className="font-serif italic"
                style={{
                  fontSize: 18,
                  color: TEAL,
                  margin: 0,
                  marginTop: 6,
                  lineHeight: 1.35,
                }}
              >
                Every session builds your island.
              </p>
            </div>
            <button
              onClick={onHide}
              className="shrink-0 inline-flex items-center gap-1.5 px-2 py-1 -mr-2 rounded-md transition-colors hover:text-[#1A1A1A] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(42,125,111,0.4)]"
              style={{
                fontFamily: "'DM Sans', system-ui, sans-serif",
                fontSize: 13,
                color: 'rgba(0,0,0,0.55)',
              }}
              aria-label="Hide points panel"
            >
              Hide
              <CloseIcon />
            </button>
          </div>

          <div className="h-px w-full" style={{ background: 'rgba(0,0,0,0.08)' }} />

          {/* Earn */}
          <p
            style={{
              fontFamily: "'DM Sans', system-ui, sans-serif",
              fontSize: 11,
              fontWeight: 700,
              letterSpacing: '0.22em',
              textTransform: 'uppercase',
              color: TEAL,
              margin: 0,
              marginTop: 24,
              marginBottom: 12,
            }}
          >
            Earn
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {EARN_ITEMS.map(item => (
              <ItemCard key={item.label} item={item} />
            ))}
          </div>

          {/* Spend */}
          <p
            style={{
              fontFamily: "'DM Sans', system-ui, sans-serif",
              fontSize: 11,
              fontWeight: 700,
              letterSpacing: '0.22em',
              textTransform: 'uppercase',
              color: TEAL,
              margin: 0,
              marginTop: 24,
              marginBottom: 12,
            }}
          >
            Spend
          </p>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {SPEND_ITEMS.map(item => (
              <ItemCard key={item.label} item={item} />
            ))}
          </div>
        </div>
      </motion.section>
    )}
  </AnimatePresence>
);

export default PointsPanel;
