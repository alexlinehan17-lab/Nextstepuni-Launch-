import React from 'react';

/** Display the original paper illustrations as white ink and orange in dark mode.
 * Remove the near-white matte without recolouring orange or touching source files.
 * Keep the filter in the document for Safari as well as Chromium.
 */
export default function IllustrationTheme() {
  return <svg aria-hidden="true" width="0" height="0" className="illustration-theme-defs">
    <defs>
      <filter id="nsu-dark-illustration" colorInterpolationFilters="sRGB">
        <feColorMatrix in="SourceGraphic" type="matrix"
          values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  -4 -4 -4 0 10.8" result="withoutPaper" />
        <feComposite in="withoutPaper" in2="SourceGraphic" operator="in" result="artwork" />
        <feColorMatrix in="SourceGraphic" type="matrix"
          values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  -4 0 0 0 1.5" result="whiteInk" />
        <feComposite in="whiteInk" in2="artwork" operator="in" result="ink" />
        <feMerge><feMergeNode in="artwork" /><feMergeNode in="ink" /></feMerge>
      </filter>
    </defs>
  </svg>;
}
