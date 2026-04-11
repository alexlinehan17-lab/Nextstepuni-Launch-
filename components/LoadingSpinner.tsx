

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React from 'react';
import { MotionDiv } from './Motion';
import { Loader } from 'lucide-react';

// FIX: Cast motion components to any to bypass broken type definitions

export const LoadingSpinner: React.FC = () => (
  <div className="flex items-center justify-center min-h-screen w-full">
    <MotionDiv
      animate={{ rotate: 360 }}
      transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
    >
      <Loader size={36} className="text-zinc-300 dark:text-zinc-700" />
    </MotionDiv>
  </div>
);
