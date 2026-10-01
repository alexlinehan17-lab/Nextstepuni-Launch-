import React from 'react';
import { ArrowLeft } from 'lucide-react';
import './controls.css';

/** Parent or previous-step navigation. Workflow exits use a separate action. */
const BackButton = React.forwardRef<HTMLButtonElement, {
  onClick: () => void; label?: string; showLabel?: boolean;
}>(({ onClick, label = 'Back', showLabel = false }, ref) => (
  <button ref={ref} type="button" className={`product-back-button${showLabel ? ' product-back-button--label' : ''}`} aria-label={label} onClick={onClick}>
    <ArrowLeft size={18} strokeWidth={1.8} aria-hidden="true" />
    {showLabel && <span>{label}</span>}
  </button>
));
BackButton.displayName = 'BackButton';
export default BackButton;
