/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Centralised Framer Motion component casts.
 * React 19 + Framer Motion have type incompatibilities — these `as any` casts
 * are the standard workaround. Centralising them here avoids 100+ duplicate
 * declarations across the codebase.
 */

import { motion, AnimatePresence as FramerAnimatePresence } from 'framer-motion';

export const AnimatePresence = FramerAnimatePresence;
export const MotionDiv = motion.div as any;
export const MotionButton = motion.button as any;
export const MotionSpan = motion.span as any;
export const MotionP = motion.p as any;
export const MotionPolygon = motion.polygon as any;
export const MotionCircle = motion.circle as any;
