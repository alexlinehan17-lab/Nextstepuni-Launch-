/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * PointsPanel — inline reference panel for the Innovation Zone landing
 * page. Replaces the old <PointsExplainer> modal which interrupted the
 * user with reference content disguised as a checkpoint.
 *
 * Sits above the IZ tool grid by default; "Hide" persists dismissal via
 * the existing `dismissedGuides` mechanism. A small "How points work"
 * link in the IZ header (rendered by InnovationZone, not here) toggles
 * a local override so the panel can be re-opened after dismissal
 * without resetting the persisted flag.
 *
 * Visual register matches the rest of the cream + paint-blob system:
 * cream card, soft teal border, ink-style inline SVG icons sat on small
 * teal-tinted blobs (no Lucide).
 */
import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const TEAL = '#2A7D6F';

// ── Inline ink-style icons ──────────────────────────────────────────────
// Drawn rather than imported from Lucide so the line weight, terminals,
// and proportions match the rest of the illustrated icons in the app.
const ClockIcon: React.FC = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <circle cx="12" cy="12" r="9" />
    <path d="M12 7v5l3 2" />
  </svg>
);
const PageIcon: React.FC = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M6 3h9l3 3v15H6z" />
    <line x1="9" y1="10" x2="14" y2="10" />
    <line x1="9" y1="14" x2="15" y2="14" />
    <line x1="9" y1="18" x2="13" y2="18" />
  </svg>
);
const FlagIcon: React.FC = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M5 21V4M5 4l11 4-3 3 3 3H5" />
  </svg>
);
const TargetIcon: React.FC = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" aria-hidden="true">
    <circle cx="12" cy="12" r="9" />
    <circle cx="12" cy="12" r="5" />
    <circle cx="12" cy="12" r="1.5" fill="currentColor" />
  </svg>
);
const TagIcon: React.FC = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M3 12V3h9l9 9-9 9z" />
    <circle cx="7.5" cy="7.5" r="1.5" />
  </svg>
);
const ChevronsRightIcon: React.FC = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M6 6l6 6-6 6M13 6l6 6-6 6" />
  </svg>
);
const MoonIcon: React.FC = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M21 13.5A9 9 0 1 1 10.5 3a7 7 0 0 0 10.5 10.5z" />
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
  { Icon: ClockIcon,  label: 'Study session',     value: '15 pts',     sub: 'Per 10 min' },
  { Icon: PageIcon,   label: 'Module section',    value: '10 pts',     sub: 'Each section' },
  { Icon: FlagIcon,   label: 'Complete a module', value: '+30 bonus',  sub: 'On finish' },
  { Icon: TargetIcon, label: 'Quests & challenges', value: '25–200 pts', sub: 'Varies' },
];

const SPEND_ITEMS: Item[] = [
  { Icon: TagIcon,            label: 'Island shop',   value: 'Varies', sub: 'Build your island' },
  { Icon: ChevronsRightIcon,  label: 'Skip a block',  value: '20 pts', sub: 'Skip one session' },
  { Icon: MoonIcon,           label: 'Rest day pass', value: '60 pts', sub: 'Day off, streak safe' },
];

// ── Subcomponents ──────────────────────────────────────────────────────
const TealBlob: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="relative shrink-0" style={{ width: 36, height: 36 }}>
    <div
      className="absolute inset-0 rounded-full"
      style={{ background: `${TEAL}26` }}
      aria-hidden="true"
    />
    <span
      className="absolute inset-0 flex items-center justify-center"
      style={{ color: TEAL }}
    >
      {children}
    </span>
  </div>
);

const ItemCard: React.FC<{ item: Item }> = ({ item }) => (
  <div
    className="rounded-xl"
    style={{
      background: '#FDF8F0',
      border: `1px solid ${TEAL}2E`,
      padding: 16,
    }}
  >
    <TealBlob><item.Icon /></TealBlob>
    <p
      className="mt-3"
      style={{
        fontFamily: "'DM Sans', system-ui, sans-serif",
        fontSize: 14,
        fontWeight: 500,
        color: 'rgba(0,0,0,0.85)',
        margin: 0,
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
        marginTop: 2,
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
        marginTop: 2,
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
            background: '#FDF8F0',
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

          {/* Hairline */}
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
