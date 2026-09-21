import React from 'react';
import { ArrowLeft } from 'lucide-react';

/** One mobile back control, including overlays and review sessions. */
const BackButton = React.forwardRef<HTMLButtonElement, {
  onClick: () => void; label?: string;
}>(({ onClick, label = 'Back' }, ref) => (
  <button ref={ref} type="button" className="editorial-back-button" aria-label={label} onClick={onClick}>
    <ArrowLeft size={18} strokeWidth={1.8} aria-hidden="true" />
  </button>
));
BackButton.displayName = 'BackButton';
export default BackButton;
