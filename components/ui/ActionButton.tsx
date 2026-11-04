import React from 'react';
import './controls.css';

export interface ActionButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  intent?: 'accent' | 'primary' | 'secondary' | 'quiet' | 'danger';
  pending?: boolean;
  pendingLabel?: string;
}

/** Shared interaction states; the caller owns saving and workflow policy. */
const ActionButton = React.forwardRef<HTMLButtonElement, ActionButtonProps>(({ intent = 'primary', pending = false, pendingLabel, disabled, className = '', children, type = 'button', ...props }, ref) => (
  <button {...props} ref={ref} type={type} disabled={disabled || pending} aria-busy={pending || undefined} className={`product-action product-action--${intent} ${className}`}>
    {pending && pendingLabel ? pendingLabel : children}
  </button>
));
ActionButton.displayName = 'ActionButton';
export default ActionButton;
