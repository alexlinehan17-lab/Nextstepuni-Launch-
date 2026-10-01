import React from 'react';
import BackButton from './BackButton';
import { useMobileAppDesign } from '../../hooks/useMobileAppDesign';

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

/** Shared navigation frame for top-level student destinations. */
const PageHeader: React.FC<PageHeaderProps> = ({
  onBack,
  eyebrow,
  title,
  subtitle,
  actions,
  className = '',
  compact = false,
  backLabel = 'Back to home',
}) => {
  const mobileAppDesign = useMobileAppDesign();
  return (
  <header className={`flex items-start justify-between gap-4 ${className}`}>
    <div className="flex min-w-0 items-start gap-3 sm:gap-4">
      <BackButton onClick={onBack} label={backLabel} showLabel={!mobileAppDesign} />
      <div className="hidden h-10 w-px shrink-0 bg-[#DDD8D2] sm:block dark:bg-zinc-700" aria-hidden="true" />
      <div className="min-w-0 pt-0.5">
        {eyebrow && (
          <p className="mb-1 text-[10px] font-bold uppercase tracking-[0.18em] text-[#8D857E] dark:text-zinc-500">
            {eyebrow}
          </p>
        )}
        <h1 className={`truncate font-serif font-semibold leading-none tracking-[-0.025em] text-[#1A1A1A] dark:text-white ${compact ? 'text-xl sm:text-2xl' : 'text-2xl sm:text-4xl'}`}>
          {title}
        </h1>
        {subtitle && <p className="mt-2 max-w-2xl text-sm leading-relaxed text-[#706A64] dark:text-zinc-400">{subtitle}</p>}
      </div>
    </div>
    {actions && <div className="flex shrink-0 items-center gap-2">{actions}</div>}
  </header>
  );
};

export default PageHeader;
