import React from 'react';
import { TopBar } from './Bars';
import { useScreenLeave } from '../navigation/useScreenLeave';

interface PageHeaderProps {
  onBack: () => void;
  eyebrow?: string;
  title: string;
  subtitle?: string;
  actions?: React.ReactNode;
  className?: string;
  compact?: boolean;
  backLabel?: string;
}

/** The shared header of a student page, drawn as the agreed top bar
 *  (navigation.md, "Top bar"): one Back at the top left (none on one of the
 *  five places), the small line over the name, one action at the right. On a
 *  place it is the place's opening instead: its small label over its name,
 *  with no leave control. It pads itself below the status bar (frame-bar);
 *  the wrapper decides whether it is sticky. */
const PageHeader: React.FC<PageHeaderProps> = ({
  onBack,
  eyebrow,
  title,
  subtitle,
  actions,
  className = '',
  backLabel = 'Back',
}) => {
  const leave = useScreenLeave(onBack, backLabel);
  if (!leave) {
    return (
      <header className={`ui-part frame-bar ui-place-head ${className}`.trim()}>
        {eyebrow ? <p className="ui-place-label">{eyebrow}</p> : null}
        <div className="ui-place-row">
          <h1 className="ui-place-name">{title}</h1>
          {actions ? <div className="ui-place-actions">{actions}</div> : null}
        </div>
        {subtitle ? <p className="ui-place-sub">{subtitle}</p> : null}
      </header>
    );
  }
  return (
    <>
      <TopBar ruled className={className} leave={leave} over={eyebrow} title={title} action={actions} />
      {subtitle ? <p className="ui-part ui-bar-sub">{subtitle}</p> : null}
    </>
  );
};

export default PageHeader;
