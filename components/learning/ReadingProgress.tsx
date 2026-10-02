import { motion, useReducedMotion } from 'motion/react';
import './progress-directions.css';
export function ReadingProgress({
  done,
  total,
}: {
  done: number;
  total: number;
}) {
  const reduced = useReducedMotion();
  const read = Math.min(Math.max(done, 0), total);
  const remaining = total - read;
  const fraction = total > 0 ? read / total : 0;
  const transition = { duration: reduced ? 0 : 0.55, ease: [0.22, 1, 0.36, 1] as const };
  const remainingText =
    remaining === 0
      ? 'All read. Yours to revisit.'
      : `${remaining} ${remaining === 1 ? 'section' : 'sections'} to go`;
  return (
    <div
      className="mr-reading-progress mr-progress-pencil"
      role="progressbar"
      aria-label="Module completion"
      aria-valuemin={0}
      aria-valuemax={total}
      aria-valuenow={read}
      aria-valuetext={`${read} of ${total} sections read. ${remainingText}`}
    >
      {(
        <>
          <div className="mr-progress-caption">
            <span>
              <strong>{read}</strong> of {total} read
            </span>
            <small>{remaining === 0 ? 'Complete' : `${remaining} to go`}</small>
          </div>
          <svg
            className="mr-pencil-line"
            viewBox="0 0 260 18"
            preserveAspectRatio="none"
            aria-hidden="true"
          >
            <line x1={3} y1={9} x2={257} y2={9} className="mr-pencil-track" />
            <motion.line
              x1={3} y1={9} y2={9}
              initial={false}
              animate={{ x2: 3 + fraction * 254 }}
              transition={transition}
              className="mr-pencil-ink"
            />
            <motion.line
              y1={13} y2={5}
              initial={false}
              animate={{ x1: 2 + Math.max(0, fraction * 254 - 4), x2: 4 + Math.max(0, fraction * 254 - 4), opacity: read > 0 ? 1 : 0 }}
              transition={transition}
              className="mr-pencil-tip"
            />
          </svg>
        </>
      )}
    </div>
  );
}
