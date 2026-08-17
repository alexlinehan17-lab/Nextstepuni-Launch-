/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { type NorthStar } from '../types';
import { type CurriculumLevel } from '../utils/authUtils';
import NorthStarOnboarding from './NorthStarOnboarding';
import ModalFrame from './ui/ModalFrame';

interface NorthStarEditModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (northStar: NorthStar) => void;
  currentNorthStar: NorthStar | null;
  /** Must be passed so JC users see the 4 JC themes when editing their NS
   *  post-onboarding (not the 6 senior themes). Defaults to 'senior' if absent
   *  to preserve pre-Phase-5 behaviour. */
  curriculumLevel?: CurriculumLevel;
}

const NorthStarEditModal: React.FC<NorthStarEditModalProps> = ({ isOpen, onClose, onSave, currentNorthStar, curriculumLevel }) => {
  return (
    <ModalFrame open={isOpen} onClose={onClose} title="Edit My North Star" eyebrow="Your vision" width="md">
      <NorthStarOnboarding
        onComplete={(ns) => { onSave(ns); onClose(); }}
        initialData={currentNorthStar}
        curriculumLevel={curriculumLevel ?? 'senior'}
      />
    </ModalFrame>
  );
};

export default NorthStarEditModal;
