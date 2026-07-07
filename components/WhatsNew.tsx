/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "What's new" — a small popover card fed by data/changelog.ts. The app
 * changes under students' feet constantly; two or three lines per release
 * makes that feel deliberate instead of disorienting. An accent dot on the
 * sidebar button marks unseen entries (localStorage per account).
 */

import React from 'react';
import { X, Sparkles } from 'lucide-react';
import { CHANGELOG, LATEST_CHANGELOG_ID } from '../data/changelog';

const KEY = 'nsu-whatsnew:';

export const hasUnseenChangelog = (uid?: string): boolean => {
  try {
    return localStorage.getItem(KEY + (uid || 'anon')) !== LATEST_CHANGELOG_ID;
  } catch {
    return false;
  }
};

export const markChangelogSeen = (uid?: string): void => {
  try {
    localStorage.setItem(KEY + (uid || 'anon'), LATEST_CHANGELOG_ID);
  } catch { /* private mode */ }
};

interface Props {
  open: boolean;
  onClose: () => void;
}

const WhatsNew: React.FC<Props> = ({ open, onClose }) => {
  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-[126] flex items-center justify-center px-4"
      role="dialog"
      aria-modal="true"
      aria-label="What's new"
      onMouseDown={e => { if (e.target === e.currentTarget) onClose(); }}
    >
      <div className="absolute inset-0 bg-black/45" onMouseDown={onClose} />
      <div
        className="relative w-full max-w-[440px] rounded-2xl bg-white px-5 py-4 max-h-[70vh] overflow-y-auto"
        style={{ border: '2px solid #1a1a1a', boxShadow: '0 4px 0 rgba(0,0,0,0.4)' }}
      >
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Sparkles size={16} style={{ color: '#F26B1F' }} />
            <h3 className="text-[18px] font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>
              What&rsquo;s new
            </h3>
          </div>
          <button onClick={onClose} aria-label="Close" className="p-1 rounded-lg" style={{ color: '#9e9186' }}>
            <X size={16} />
          </button>
        </div>

        <div className="flex flex-col gap-4">
          {CHANGELOG.slice(0, 5).map(entry => (
            <div key={entry.id}>
              <p className="text-[10px] font-bold uppercase tracking-[0.12em] mb-0.5" style={{ color: '#9e9186' }}>
                {entry.date}
              </p>
              <h4 className="text-[15px] font-semibold mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>
                {entry.title}
              </h4>
              <ul className="flex flex-col gap-1">
                {entry.lines.map(line => (
                  <li key={line} className="flex items-start gap-2 text-[13px] leading-relaxed" style={{ color: '#5a5550' }}>
                    <span className="mt-[7px] w-1 h-1 rounded-full shrink-0" style={{ backgroundColor: '#F26B1F' }} />
                    {line}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default WhatsNew;
