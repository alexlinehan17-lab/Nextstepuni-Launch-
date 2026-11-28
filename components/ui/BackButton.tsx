import React from 'react';
import { ChevronLeft } from 'lucide-react';
import { IconButton } from './Button';
import { useScreenLeave } from '../navigation/useScreenLeave';

/** The one Back (navigation.md): a bare chevron in a 44 x 44 target, top left.
 *  It is not drawn on one of the five places. `onClick` is the screen's Back;
 *  the app passes its one Back (the screen you came from, else the parent).
 *  `showLabel` is kept for old callers and draws nothing: the agreed bar has
 *  the chevron alone on every device; `label` is its accessible name. */
const BackButton = React.forwardRef<HTMLButtonElement, {
  onClick: () => void; label?: string; showLabel?: boolean;
}>(({ onClick, label = 'Back' }, ref) => {
  const leave = useScreenLeave(onClick, label);
  if (!leave) return null;
  return (
    <IconButton ref={ref} label={label} onClick={leave.onPress} className="ui-back"
      icon={<ChevronLeft className="ui-icon" width={24} height={24} strokeWidth={1.75} aria-hidden="true" focusable="false" />} />
  );
});
BackButton.displayName = 'BackButton';
export default BackButton;
