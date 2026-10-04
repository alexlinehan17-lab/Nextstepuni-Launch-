import React from 'react';

/** Frame the full-resolution alpha artwork without cropping or resampling it. */
export default function StudySnoozer({ artworkRef, className = '' }: {
  artworkRef?: React.Ref<SVGSVGElement>;
  className?: string;
}) {
  return <svg ref={artworkRef} className={`study-snoozer ${className}`} viewBox="285 216 690 824" width="690" height="824" aria-hidden="true">
    <image href="/assets/dark/star-crew/personal/11-snoozer.png" width="1254" height="1254" />
  </svg>;
}
