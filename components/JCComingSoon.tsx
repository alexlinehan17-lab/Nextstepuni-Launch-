/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { MotionDiv } from './Motion';
import { ArrowLeft, Sparkles } from 'lucide-react';
import { COLORS } from '../design/tokens';

interface JCComingSoonProps {
  /** ID of the Decode/strategy module the user clicked, so we can name it
   *  in the placeholder. Optional — if absent, generic copy is shown. */
  fromCourseTitle?: string;
  onBack: () => void;
}

const JCComingSoon: React.FC<JCComingSoonProps> = ({ fromCourseTitle, onBack }) => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 py-10" style={{ backgroundColor: '#FDF8F0' }}>
      <MotionDiv
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
        className="w-full max-w-lg mx-auto text-center"
      >
        {/* Sparkles icon */}
        <div
          className="w-16 h-16 mx-auto mb-6 rounded-2xl flex items-center justify-center"
          style={{ backgroundColor: 'rgba(242,107,31,0.1)' }}
        >
          <Sparkles size={32} style={{ color: COLORS.accent }} />
        </div>

        <h1 className="font-serif text-3xl sm:text-4xl font-bold mb-3 text-[#1A1A1A]">
          Coming soon for Junior Cycle
        </h1>

        {fromCourseTitle && (
          <p className="text-sm font-semibold uppercase tracking-widest mb-6 text-[#F26B1F]">
            {fromCourseTitle}
          </p>
        )}

        <div className="text-left rounded-2xl p-6 mb-8" style={{ backgroundColor: '#FFFFFF', border: '2px solid #1A1A1A', boxShadow: '4px 4px 0 0 #1A1A1A' }}>
          <p className="text-[15px] leading-relaxed text-[#1A1A1A] mb-4">
            This module is being built for Junior Cycle students. We're working on Junior Cycle versions of all our subject Decode tools — they'll cover the exam structure, marking schemes, and study techniques specific to your Junior Cert.
          </p>
          <p className="text-[15px] leading-relaxed text-[#78716C]">
            In the meantime, check out the modules and tools that ARE ready for you in the Library.
          </p>
        </div>

        <button
          onClick={onBack}
          className="inline-flex items-center gap-2 px-7 py-3.5 rounded-2xl border-2 border-[#1A1A1A] bg-[#F26B1F] text-[#FDF8F0] font-sans font-semibold text-[15px] shadow-[4px_4px_0_0_#1A1A1A] hover:shadow-[6px_6px_0_0_#1A1A1A] active:translate-x-1 active:translate-y-1 active:shadow-[0_0_0_0_#1A1A1A] transition-all duration-150"
        >
          <ArrowLeft size={18} />
          Back to Library
        </button>
      </MotionDiv>
    </div>
  );
};

export default JCComingSoon;
