

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React from 'react';
import { motion } from 'framer-motion';
import { Loader } from 'lucide-react';

// FIX: Cast motion components to any to bypass broken type definitions
const MotionDiv = motion.div as any;

export const LoadingSpinner: React.FC = () => (
  <div className="flex items-center justify-center min-h-screen w-full">
    <MotionDiv
      animate={{ rotate: 360 }}
      transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
    >
      <Loader size={36} className="text-stone-300 dark:text-stone-700" />
    </MotionDiv>
  </div>
);
