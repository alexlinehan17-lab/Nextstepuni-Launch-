import type { CSSProperties } from 'react';
export type BookDirection = 'open-pages' | 'field-notes' | 'page-turn' | 'bookmark';

/** NextStepUni pocket notebook. Hand-drawn geometry, solid paper, charcoal ink and brand orange. */
export function BrandBook({
  direction = 'field-notes',
  size = 28,
  className = '',
}: {
  direction?: BookDirection;
  size?: number;
  className?: string;
}) {
  const style = {
    '--ib-paper': '#fffdf7',
    '--ib-ink': '#25241f',
    '--ib-orange': '#eb692a',
  } as CSSProperties;
  const silhouettes = {
    'open-pages': 'M5 10 Q14 6 24 12 Q34 7 43 10 L42 37 Q33 34 24 40 Q14 35 5 38 Z',
    'field-notes': 'M11 6 L34 4 Q38 4 38 8 L40 37 Q40 41 35 42 L13 44 Q8 44 8 39 L6 12 Q6 7 11 6Z',
    'page-turn': 'M5 11 Q14 7 24 12 L38 5 L43 14 L42 38 Q33 34 24 40 Q14 35 5 38Z',
    bookmark: 'M5 11 Q15 6 24 12 Q33 7 43 10 L42 38 Q33 35 24 41 Q14 35 5 38Z',
  };
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 48 48"
      aria-hidden="true"
      className={`ib-book ${className}`}
      style={style}
      fill="none"
      stroke="var(--ib-ink)"
      strokeWidth="2.7"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d={silhouettes[direction]} stroke="var(--ib-rim, transparent)" strokeWidth="5.5" />
      {direction === 'open-pages' && (
        <>
          <path d={silhouettes[direction]} fill="var(--ib-paper)" />
          <path d="M24 12 Q23 25 24 40 M9 16 Q15 14 19 17 M9 23 Q15 21 19 24" />
          <path d="M29 13 L36 11 L36 28 L32 25 L28 28Z" fill="var(--ib-orange)" strokeWidth="2" />
          <path d="M10 31 Q15 29 19 32 M29 33 L37 31" strokeWidth="2" />
        </>
      )}
      {direction === 'field-notes' && (
        <>
          <path d={silhouettes[direction]} fill="var(--ib-paper)" />
          <path
            d="M12 6 L34 4 Q38 4 38 8 L40 35 L15 38 Q10 38 9 42 L6 12 Q6 7 12 6Z"
            fill="var(--ib-orange)"
          />
          <path d="M12 9 L14 35 M15 41 L34 39" strokeWidth="2" />
          <path d="M18 14 L32 12 L33 23 L18 25Z" fill="var(--ib-paper)" strokeWidth="2" />
          <path d="M22 18 L28 17 M22 21 L27 20" strokeWidth="1.7" />
        </>
      )}
      {direction === 'page-turn' && (
        <>
          <path
            d="M5 11 Q14 7 24 12 Q35 8 43 14 L42 38 Q33 34 24 40 Q14 35 5 38Z"
            fill="var(--ib-paper)"
          />
          <path d="M24 12 L38 5 L37 30 L24 40Z" fill="var(--ib-orange)" />
          <path
            d="M10 18 Q15 16 19 19 M10 26 Q15 24 19 27 M29 15 L33 13 M29 22 L33 20"
            strokeWidth="2"
          />
        </>
      )}
      {direction === 'bookmark' && (
        <>
          <path d={silhouettes[direction]} fill="var(--ib-paper)" />
          <path
            d="M24 12 Q23 26 24 41 M9 19 Q15 17 19 20 M9 28 Q15 26 19 29 M29 29 Q34 26 38 27"
            strokeWidth="2.2"
          />
          <path
            d="M28 10 Q32 8 36 9 L36 24 L32 21 L28 25Z"
            fill="var(--ib-orange)"
            strokeWidth="2.2"
          />
        </>
      )}
    </svg>
  );
}
