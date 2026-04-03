/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';

type Variant = 'teal' | 'dark';

const VARIANTS: Record<Variant, { fill: string; depth: string }> = {
  teal: { fill: '#2A7D6F', depth: '#1F5F54' },
  dark: { fill: '#1C1C1C', depth: '#000000' },
};

interface PrimaryActionButtonProps extends Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, 'style'> {
  label: string;
  onClick: () => void;
  icon?: React.ElementType;
  variant?: Variant;
}

const PrimaryActionButton: React.FC<PrimaryActionButtonProps> = ({
  label,
  onClick,
  icon: Icon,
  variant = 'teal',
  disabled,
  className = '',
  ...rest
}) => {
  const v = VARIANTS[variant];

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`inline-flex items-center justify-center gap-2.5 rounded-full text-white font-semibold tracking-wide select-none transition-all duration-[120ms] ease-out disabled:opacity-50 disabled:pointer-events-none ${className}`}
      style={{
        fontSize: 16,
        padding: '14px 32px',
        backgroundColor: v.fill,
        border: 'none',
        boxShadow: `3px 4px 0 0 ${v.depth}`,
        borderRadius: 9999,
        transform: 'translateY(0) scale(1)',
      }}
      onMouseEnter={(e) => {
        if (disabled) return;
        const el = e.currentTarget;
        el.style.transform = 'translateY(1px) translateX(1px) scale(1.02)';
        el.style.boxShadow = `2px 3px 0 0 ${v.depth}`;
      }}
      onMouseLeave={(e) => {
        const el = e.currentTarget;
        el.style.transform = 'translateY(0) scale(1)';
        el.style.boxShadow = `3px 4px 0 0 ${v.depth}`;
      }}
      onMouseDown={(e) => {
        if (disabled) return;
        const el = e.currentTarget;
        el.style.transform = 'translateY(4px) translateX(3px) scale(1)';
        el.style.boxShadow = `0px 0px 0 0 ${v.depth}`;
      }}
      onMouseUp={(e) => {
        const el = e.currentTarget;
        el.style.transform = 'translateY(1px) translateX(1px) scale(1.02)';
        el.style.boxShadow = `2px 3px 0 0 ${v.depth}`;
      }}
      {...rest}
    >
      {Icon && <Icon size={18} />}
      {label}
    </button>
  );
};

export default PrimaryActionButton;
