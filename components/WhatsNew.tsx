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
import { CHANGELOG, LATEST_CHANGELOG_ID } from '../data/changelog';
import ModalFrame from './ui/ModalFrame';

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
  return (
    <ModalFrame open={open} onClose={onClose} title="What’s new" eyebrow="Latest changes" width="sm">
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
    </ModalFrame>
  );
};

export default WhatsNew;
