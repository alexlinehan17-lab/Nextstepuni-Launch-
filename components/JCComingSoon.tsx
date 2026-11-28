/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { MotionDiv } from './Motion';
import { TopBar } from './ui/Bars';

interface JCComingSoonProps {
  /** ID of the Decode/strategy module the user clicked, so we can name it
   *  in the placeholder. Optional — if absent, generic copy is shown. */
  fromCourseTitle?: string;
  onBack: () => void;
}

/** A page (navigation.md): one Back at the top left of the bar, in place of the old "Back to Library"
 *  button under the text (its words are the Back's name). The words on the page, no box (area 9). */
const JCComingSoon: React.FC<JCComingSoonProps> = ({ fromCourseTitle, onBack }) => {
  return (
    <div className="min-h-screen bg-white dark:bg-surface-canvas flex flex-col">
      <TopBar leave={{ kind: 'back', onPress: onBack, label: 'Back to Library' }} />
      <MotionDiv
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
        className="w-full max-w-lg mx-auto px-6 pt-6 pb-10 flex flex-col gap-2"
      >
        <h1 className="t-title text-[var(--ink-primary)]">
          Coming soon for Junior Cycle
        </h1>

        {fromCourseTitle && (
          <p className="t-label text-[var(--ink-muted)]">
            {fromCourseTitle}
          </p>
        )}

        <p className="t-body text-[var(--ink-primary)] mt-4">
          This module is being built for Junior Cycle students. We're working on Junior Cycle versions of all our subject Decode tools — they'll cover the exam structure, marking schemes, and study techniques specific to your Junior Cert.
        </p>
        <p className="t-sub mt-2">
          In the meantime, check out the modules and tools that ARE ready for you in the Library.
        </p>
      </MotionDiv>
    </div>
  );
};

export default JCComingSoon;
