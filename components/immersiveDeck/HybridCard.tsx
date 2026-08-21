/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Hybrid card primitives — the shared building blocks for the 2026-06-03 deck
 * redesign. Each immersive deck (How They Did It, Career Paths, Your Possible
 * Life) is now a LIGHT white card (bold #1a1a1a border, chunky shadow) with a
 * brightened colour HEADER BAND (Lucide icon for careers / initials for people)
 * over a white body of ink text, the field colour kept to the header + tinted
 * accents, and orange chunky CTAs — same family as the rest of the app rather
 * than a full-bleed dark colour world. Use these so all three stay identical.
 */
import React from 'react';
import { type LucideIcon } from 'lucide-react';
import { type ColorWorld, paperInk } from './colorWorlds';
import { useSettingsContext } from '../../contexts/SettingsContext';

export const SERIF = "'Source Serif 4', serif";
export const INK = 'var(--deck-ink)';
export const BODY = 'var(--deck-body)';
export const MUTED = 'var(--deck-muted)';
export const LABEL = 'var(--deck-label)';
export const HAIRLINE = 'var(--deck-hairline)';
export const CARD_SHADOW = 'var(--deck-shadow)';
/** App accent (orange) for primary CTAs. */
export const ACCENT = '#F26B1F';
export const ACCENT_DARK = '#B54D14';

/** Ink for a world's coloured glyphs/text on the deck paper -- flips with the theme. */
export const usePaperInk = (): ((w: ColorWorld) => string) => {
  const dark = useSettingsContext()?.settings.darkMode ?? false;
  return React.useCallback((w: ColorWorld) => paperInk(w, dark), [dark]);
};

/** White card shell — bold border + chunky offset shadow, on the light canvas. */
export const HybridCard: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className }) => (
  <div className={`immersive-deck-theme relative rounded-[24px] border-2 overflow-hidden bg-[var(--deck-paper)] ${className ?? ''}`} style={{ borderColor: INK, boxShadow: CARD_SHADOW }}>
    {children}
  </div>
);

/** Dark progress dots, sized to sit on a white header. */
export const ProgressDots: React.FC<{ total: number; active: number }> = ({ total, active }) => (
  <div className="flex items-center gap-1.5 pt-2 shrink-0">
    {Array.from({ length: total }).map((_, s) => (
      <span key={s} className="h-1.5 rounded-full transition-all" style={{ width: s === active ? 16 : 6, backgroundColor: s <= active ? INK : '#dcd8d2' }} />
    ))}
  </div>
);

// Soft organic blob shapes (same language as the Innovation Zone tool tiles /
// ToolIconBlob). The glyph sits over a low-opacity field-colour blob on white.
const BLOBS = [
  'M 6 24 Q -2 52 8 78 Q 24 98 52 94 Q 86 90 94 62 Q 100 30 84 10 Q 60 -4 32 4 Q 12 12 6 24 Z',
  'M 8 26 Q 0 50 8 78 Q 22 96 54 96 Q 88 94 96 64 Q 100 32 80 10 Q 56 -2 28 8 Q 12 16 8 26 Z',
  'M 6 26 Q 0 52 10 80 Q 26 98 54 94 Q 88 90 96 60 Q 100 28 82 8 Q 56 -4 30 8 Q 12 16 6 26 Z',
];
const blobFor = (seed: string) => BLOBS[(seed ? seed.charCodeAt(0) + seed.length : 0) % BLOBS.length];

/** Line icon (careers) or serif initials (people) over a soft pastel blob — the app's tool-tile icon language. */
export const BlobIcon: React.FC<{ wd: ColorWorld; icon?: LucideIcon; initials?: string; image?: string; size?: number; seed?: string }> = ({ wd, icon: Icon, initials, image, size = 46, seed }) => {
  const [imgError, setImgError] = React.useState(false);
  /* The glyph sits on the deck paper, not on a tint chip, so it needs the
     theme-aware ink -- `wd.deep` is invisible on the dark paper. */
  const ink = usePaperInk()(wd);
  const showImg = !!image && !imgError;
  return (
    <span className="relative inline-flex items-center justify-center shrink-0" style={{ width: size, height: size }}>
      <svg viewBox="0 0 100 100" width={size} height={size} className="absolute inset-0" aria-hidden="true">
        <path d={blobFor(seed ?? initials ?? '')} fill={wd.bg} opacity={0.18} />
      </svg>
      {showImg ? (
        <img src={image} alt="" width={Math.round(size * 0.82)} height={Math.round(size * 0.82)} className="relative object-contain" onError={() => setImgError(true)} />
      ) : Icon ? (
        <Icon size={Math.round(size * 0.46)} color={ink} strokeWidth={2} className="relative" />
      ) : initials ? (
        <span className="relative font-bold leading-none" style={{ fontFamily: SERIF, color: ink, fontSize: Math.round(size * 0.34) }}>{initials}</span>
      ) : null}
    </span>
  );
};

/** White header atop a white card: pastel blob glyph + coloured eyebrow + ink serif title. Pass `icon` (careers) OR `initials` (people). */
export const Band: React.FC<{
  wd: ColorWorld;
  icon?: LucideIcon;
  initials?: string;
  image?: string;
  eyebrow?: React.ReactNode;
  title?: string;
  subtitle?: string;
  right?: React.ReactNode;
}> = ({ wd, icon, initials, image, eyebrow, title, subtitle, right }) => {
  /* The eyebrow sits on the deck paper, so it needs the theme-aware ink. */
  const ink = usePaperInk()(wd);
  return (
  <div className="relative px-6 pt-5 pb-4 bg-[var(--deck-paper)]" style={{ borderBottom: `1px solid ${HAIRLINE}` }}>
    <div className="flex items-start justify-between gap-3">
      <div className="flex items-center gap-3 min-w-0">
        <BlobIcon wd={wd} icon={icon} initials={initials} image={image} size={46} seed={title ?? initials} />
        <div className="min-w-0">
          {eyebrow && <p className="text-[10px] font-bold uppercase tracking-[0.14em]" style={{ color: ink }}>{eyebrow}</p>}
          {title && <h2 className="text-[21px] font-semibold leading-tight" style={{ fontFamily: SERIF, color: INK }}>{title}</h2>}
          {subtitle && <p className="text-[12.5px] leading-snug" style={{ color: MUTED }}>{subtitle}</p>}
        </div>
      </div>
      {right}
    </div>
  </div>
  );
};

/** Primary CTA — the app's orange chunky pill. */
export const OrangeBtn: React.FC<{ label: string; icon?: LucideIcon; onClick: () => void; className?: string }> = ({ label, icon: Icon, onClick, className }) => (
  <button onClick={onClick} className={`inline-flex items-center justify-center gap-2 px-6 py-3 rounded-full text-[14px] font-semibold text-white transition-transform active:translate-y-[3px] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1a1a1a] ${className ?? ''}`} style={{ backgroundColor: ACCENT, boxShadow: `0 4px 0 ${ACCENT_DARK}` }}>
    {label} {Icon && <Icon size={16} />}
  </button>
);

/** Neutral / secondary action — white pill, muted border. */
export const NeutralBtn: React.FC<{ label: string; icon?: LucideIcon; onClick: () => void }> = ({ label, icon: Icon, onClick }) => (
  <button onClick={onClick} className="inline-flex items-center gap-1.5 px-5 py-3 rounded-xl text-[13.5px] font-semibold transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#F26B1F]" style={{ backgroundColor: 'var(--deck-paper)', border: '2px solid var(--deck-hairline)', color: MUTED }}>
    {Icon && <Icon size={15} />} {label}
  </button>
);

/** Uppercase section label on a white body. */
export const Eyebrow: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <p className="text-[10px] font-bold uppercase tracking-[0.14em] mb-2.5" style={{ color: LABEL }}>{children}</p>
);

/** Light segmented toggle (active pill = colour). */
export const Segment: React.FC<{ options: { value: string; label: string }[]; value: string; onChange: (v: string) => void; wd: ColorWorld }> = ({ options, value, onChange, wd }) => (
  <div role="group" className="inline-flex rounded-full p-1" style={{ backgroundColor: 'var(--deck-soft)' }}>
    {options.map((o) => {
      const active = o.value === value;
      return (
        <button key={o.value} type="button" aria-pressed={active} onClick={() => onChange(o.value)} className="px-3.5 py-1.5 rounded-full text-[12.5px] font-semibold transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#F26B1F]" style={active ? { backgroundColor: wd.bg, color: '#fff' } : { color: MUTED }}>
          {o.label}
        </button>
      );
    })}
  </div>
);

/** Back link rendered above a card on the light page. */
export const BackLink: React.FC<{ onClick: () => void; label: string }> = ({ onClick, label }) => (
  <button onClick={onClick} className="flex items-center gap-1.5 text-[13px] font-medium text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 mb-4">
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"><path d="m15 18-6-6 6-6" /></svg>
    {label}
  </button>
);
