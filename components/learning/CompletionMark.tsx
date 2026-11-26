import './completion-markers.css';
/** A step's mark (area 5 of the design build; boards c-read-flow, c-read-desk, r5-module-world):
 *  a step read is a green disc with a white tick, the step you are on is ink with its number, the
 *  rest a hairline ring with its number in the mono. The adjacent text supplies the accessible state. */
export function CompletionMark({
  number,
  complete,
  current = false,
}: {
  /** Kept for callers of the old marker set; there is one mark now. */
  direction?: 'tabs';
  number: number;
  complete: boolean;
  current?: boolean;
}) {
  return (
    <span className="cm-mark" data-complete={complete} data-current={current} aria-hidden="true">
      {complete && !current
        ? <svg viewBox="0 0 12 12" focusable="false"><path d="M2.5 6.2l2.4 2.4 4.6-5" /></svg>
        : <span>{String(number).padStart(2, '0')}</span>}
    </span>
  );
}
