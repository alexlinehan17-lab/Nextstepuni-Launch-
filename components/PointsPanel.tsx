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

const ACCENT = '#F26B1F'; // Brand accent (orange).

// ── Item icons — painted-blob + ink-illustration, 100x100 viewBox ───────
const StudySessionIcon: React.FC = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%" aria-hidden="true">
    <path d="M13 28C8 43 9 69 22 80c13 11 41 9 54-3 13-13 14-42 1-55C62 8 26 13 13 28Z" fill="#B8DDC8" opacity=".78" />
    <path d="M43 22c1-5 14-5 16 0l-1 7" fill="#FAFBF6" stroke="#20201F" strokeWidth="3" strokeLinecap="round" />
    <path d="M27 53c0-17 9-26 24-27 16-1 25 11 24 27-1 17-10 25-25 25S27 69 27 53Z" fill="#FAFBF6" stroke="#20201F" strokeWidth="3" strokeLinejoin="round" />
    <path d="M51 35c7 0 13 4 17 9L51 53Z" fill="#F26B1F" opacity=".86" />
    <path d="m51 36-1 17 12 7" fill="none" stroke="#20201F" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
    <circle cx="50" cy="53" r="3" fill="#20201F" />
  </svg>
);

const ModuleSectionIcon: React.FC = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%" aria-hidden="true">
    <path d="M14 25C8 44 10 69 23 79c15 11 43 8 55-7 11-14 10-39-2-50C62 10 28 13 14 25Z" fill="#F5C9A8" opacity=".78" />
    <path d="M31 18c11 1 23 0 31 2l12 13c-1 14 1 33-2 48-13 2-27 1-41 0-2-19-1-43 0-63Z" fill="#FAFBF6" stroke="#20201F" strokeWidth="3" strokeLinejoin="round" />
    <path d="m62 20-1 14 13-1" fill="none" stroke="#20201F" strokeWidth="3" strokeLinejoin="round" />
    <path d="M39 45c8-1 18 0 26 0M39 55c9 0 17 1 25 0M39 66c7 0 14-1 20 0" fill="none" stroke="#20201F" strokeWidth="2.7" strokeLinecap="round" />
    <path d="M39 73c7 1 15 0 22 0" fill="none" stroke="#F26B1F" strokeWidth="3" strokeLinecap="round" />
  </svg>
);

const CompleteModuleIcon: React.FC = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%" aria-hidden="true">
    <path d="M14 28C8 46 11 70 25 79c15 10 42 8 54-7 11-14 8-38-3-50C61 9 28 15 14 28Z" fill="#D4B978" opacity=".78" />
    <path d="M31 81c1-17-1-43 1-62" fill="none" stroke="#20201F" strokeWidth="3.2" strokeLinecap="round" />
    <path d="M33 22c13 0 26 4 39 5l-10 11 10 13c-14-2-26-5-40-4" fill="#FAFBF6" stroke="#20201F" strokeWidth="3" strokeLinejoin="round" />
    <path d="m45 33 7 6 10-10" fill="none" stroke="#F26B1F" strokeWidth="3.4" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const QuestsIcon: React.FC = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%" aria-hidden="true">
    <path d="M13 28C7 47 10 71 23 81c14 10 43 7 56-8 11-14 9-39-4-52C59 9 27 15 13 28Z" fill="#D9A9C2" opacity=".78" />
    <path d="M26 51c0-16 10-25 25-25 16 0 25 10 24 26-1 15-10 24-25 24S26 67 26 51Z" fill="#FAFBF6" stroke="#20201F" strokeWidth="3" />
    <path d="M36 51c0-9 5-15 14-15 10 0 15 6 15 15 0 10-6 15-15 15s-14-6-14-15Z" fill="none" stroke="#20201F" strokeWidth="2.7" />
    <circle cx="50" cy="51" r="6" fill="#F26B1F" />
    <path d="m54 46 20-20m-2 0h7m-7 0v-7" fill="none" stroke="#20201F" strokeWidth="3" strokeLinecap="round" />
  </svg>
);

const IslandShopIcon: React.FC = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%" aria-hidden="true">
    <path d="M13 27C8 45 10 69 23 80c14 11 43 8 55-7 12-14 10-39-3-51C60 10 27 14 13 27Z" fill="#A8C9A0" opacity=".78" />
    <path d="m22 45 27-16 29 15-28 18Z" fill="#FAFBF6" stroke="#20201F" strokeWidth="3" strokeLinejoin="round" />
    <path d="m22 45 1 11 27 18 28-18V44M50 62v12" fill="none" stroke="#20201F" strokeWidth="3" strokeLinejoin="round" />
    <path d="M50 29V16m1 1c8 0 13 2 18 5-6 4-12 5-18 5" fill="#F26B1F" stroke="#20201F" strokeWidth="2.7" strokeLinecap="round" strokeLinejoin="round" />
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
  { Icon: StudySessionIcon,   label: 'Study session',        value: '15 JP',      sub: 'Per 10 min' },
  { Icon: ModuleSectionIcon,  label: 'Module section',       value: '10 JP',      sub: 'Each section' },
  { Icon: CompleteModuleIcon, label: 'Complete a module',    value: '+30 bonus',  sub: 'On finish' },
  { Icon: QuestsIcon,         label: 'Quests & challenges',  value: '25–200 JP',  sub: 'Varies' },
];

const SPEND_ITEMS: Item[] = [
  { Icon: IslandShopIcon, label: 'Island shop', value: 'Varies', sub: 'Terrain and objects for your island' },
];

// ── Item card ──────────────────────────────────────────────────────────
const ItemCard: React.FC<{ item: Item }> = ({ item }) => (
  <div
    className="rounded-xl"
    style={{
      background: '#ffffff',
      border: `1px solid ${ACCENT}26`,
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
        color: ACCENT,
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
            background: '#ffffff',
            border: `1px solid ${ACCENT}40`,
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
                  color: ACCENT,
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
              className="shrink-0 inline-flex items-center gap-1.5 px-2 py-1 -mr-2 rounded-md transition-colors hover:text-[#1A1A1A] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(242,107,31,0.4)]"
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
              color: ACCENT,
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
              color: ACCENT,
              margin: 0,
              marginTop: 24,
              marginBottom: 12,
            }}
          >
            Spend
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
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
