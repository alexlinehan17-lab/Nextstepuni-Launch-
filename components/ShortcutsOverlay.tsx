/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Keyboard shortcuts cheat-sheet — opens on "?" (Shift+/) anywhere except
 * the home page, where "?" belongs to the Site Guide (which is the richer
 * answer to "where am I"). Small card in the module design register.
 */

import React, { useEffect, useState } from 'react';
import { X, Keyboard } from 'lucide-react';

const SHORTCUTS: { keys: string[]; what: string }[] = [
  { keys: ['⌘', 'K'], what: 'Jump to any module, tool or page' },
  { keys: ['?'], what: 'Home: open the Site Guide · elsewhere: this card' },
  { keys: ['←', '→'], what: 'Move through Site Guide cards and Full Loop questions' },
  { keys: ['Esc'], what: 'Close any dialog or overlay' },
];

interface Props {
  /** True on views where "?" is owned by something richer (the home page's Site Guide). */
  suppressQuestionKey?: boolean;
}

const ShortcutsOverlay: React.FC<Props> = ({ suppressQuestionKey = false }) => {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement | null;
      if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
      if (e.key === 'Escape') { setOpen(false); return; }
      if (e.key === '?' && !suppressQuestionKey) setOpen(v => !v);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [suppressQuestionKey]);

  // If the view changes to one that owns "?", drop the card rather than fight it.
  useEffect(() => {
    if (suppressQuestionKey) setOpen(false);
  }, [suppressQuestionKey]);

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-[128] flex items-center justify-center px-4"
      role="dialog"
      aria-modal="true"
      aria-label="Keyboard shortcuts"
      onMouseDown={e => { if (e.target === e.currentTarget) setOpen(false); }}
    >
      <div className="absolute inset-0 bg-black/45" onMouseDown={() => setOpen(false)} />
      <div
        className="relative w-full max-w-[420px] rounded-2xl bg-white px-5 py-4"
        style={{ border: '2px solid #1a1a1a', boxShadow: '0 4px 0 rgba(0,0,0,0.4)' }}
      >
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Keyboard size={16} style={{ color: '#F26B1F' }} />
            <h3 className="text-[17px] font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>
              Keyboard shortcuts
            </h3>
          </div>
          <button onClick={() => setOpen(false)} aria-label="Close" className="p-1 rounded-lg" style={{ color: '#9e9186' }}>
            <X size={16} />
          </button>
        </div>
        <div className="flex flex-col gap-2.5">
          {SHORTCUTS.map(s => (
            <div key={s.what} className="flex items-center gap-3">
              <span className="flex gap-1 shrink-0" style={{ minWidth: 76 }}>
                {s.keys.map(k => (
                  <kbd
                    key={k}
                    className="text-[11px] font-bold px-1.5 py-0.5 rounded"
                    style={{ backgroundColor: '#f0efec', color: '#1a1a1a', border: '1px solid #d0cdc8', borderBottomWidth: 2 }}
                  >
                    {k}
                  </kbd>
                ))}
              </span>
              <span className="text-[13px]" style={{ color: '#5a5550' }}>{s.what}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ShortcutsOverlay;
