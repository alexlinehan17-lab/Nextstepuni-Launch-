import React from 'react';
import { ChevronDown } from 'lucide-react';
import './launchpad.css';

/** Native selection and keyboard behaviour with consistently centred chrome. */
export default function LaunchpadSelect({
  className = '',
  children,
  ...props
}: React.SelectHTMLAttributes<HTMLSelectElement>) {
  return (
    <span className={`lp-select ${className}`}>
      <select {...props}>{children}</select>
      <ChevronDown size={16} strokeWidth={1.8} aria-hidden="true" />
    </span>
  );
}
