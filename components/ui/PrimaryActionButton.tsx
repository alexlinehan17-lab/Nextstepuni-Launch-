/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { type LucideIcon } from 'lucide-react';
import ActionButton, { type ActionButtonProps } from './ActionButton';

interface PrimaryActionButtonProps extends Omit<ActionButtonProps, 'children' | 'intent'> {
  label: string;
  icon?: LucideIcon;
  variant?: 'accent' | 'teal' | 'dark';
}

const PrimaryActionButton: React.FC<PrimaryActionButtonProps> = ({ label, icon: Icon, variant = 'accent', ...props }) => (
  <ActionButton {...props} intent={variant === 'dark' ? 'primary' : 'accent'}>
    {Icon && <Icon size={18} aria-hidden="true" />}
    {label}
  </ActionButton>
);
export default PrimaryActionButton;
